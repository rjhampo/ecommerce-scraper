import os, dotenv, json, time, logging, warnings
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from curl_cffi import requests
from requests import HTTPError
from .constants import *


warnings.filterwarnings('ignore', r'Make sure*', RuntimeWarning, module='curl_cffi')
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)
dotenv.load_dotenv()



def get_cookies_headers(url: str, proxy: str, user: str, passw: str) -> list:
    logger.debug(f'Getting browser data from {url} through proxy {proxy}')
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.firefox.launch(proxy={'server': proxy, 'username': user, 'password': passw}, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        page.goto(url)
        page.pause()
        csrf_locator = page.locator('#X-CSRF-TOKEN')
        for i in range(csrf_locator.count()):
            csrf_token = csrf_locator.nth(i).get_attribute('content')
            if csrf_token: break
        cookies = context.cookies()
        context.close()
    cookiejar = {}
    for cookie in cookies:
        cookiejar[cookie['name']] = str(cookie['value'])
    return {'cookiejar': cookiejar, 'csrf_token': csrf_token}

def get_new_session(session_url: str, proxy_settings: dict) -> requests.Session:
    proxy = proxy_settings.get('proxy_url')
    if callable(proxy):
        proxy = next(proxy())
    logger.info(f'Opening browser... Answer any CAPTCHAs that may appear during this time. Press "Resume" in Playwright inspector to continue execution after answering CAPTCHA')
    browser_data = get_cookies_headers(session_url, proxy, proxy_settings.get('proxy_user'), proxy_settings.get('proxy_passw'))
    headers = rotate_header()
    headers['X-CSRF-TOKEN'] = browser_data['csrf_token']
    logger.debug(f'Obtained new cookies and new header = {headers}')
    new_session = requests.Session()
    logger.debug(f'Obtained new session')
    new_session.cookies.update(browser_data['cookiejar'])
    new_session.proxies = {'https': proxy}
    new_session.headers = headers
    
    return new_session

def run_page_scraper(item: str, proxy_settings: dict, pagination: int | None = 1) -> list:
    """proxy_settings should be dict of form {proxy_url: <str> | <generator>, proxy_user: <str>, proxy_passw: <str>}"""

    start_time = time.time()
    if item.find(' ') > -1:
        tag_search = item.replace(' ', '-')
        query_search = item.replace(' ', '%20')
    else:
        tag_search = query_search = item
    
    html_url = f'https://www.lazada.com.ph/tag/{tag_search}/?spm=a2o4l.homepage.search.d_go&q={query_search}&catalog_redirect_tag=true'
    scrape_data = []
    noMorePages: bool = False
    newSession: bool = False
    totalPages = None

    while not noMorePages:
        api_url = f'https://www.lazada.com.ph/tag/{tag_search}/?ajax=true&catalog_redirect_tag=true&page={pagination}&q={query_search}&spm=a2o4l.homepage.search.d_go'
        
        if not newSession:
            curr_session = get_new_session(html_url, proxy_settings)
            newSession = True

        try:
            random_delay()
            response = curr_session.request('GET', api_url, impersonate='chrome')
            response.raise_for_status()
        except HTTPError as error:
            logger.error(f'Failed to get from API with due to {error}', exc_info=True)
        
        response_json = response.json()
        random_delay()
        try:
            noMorePages = response_json['mainInfo'].get('noMorePages')
            if totalPages is None:
                totalPages = int(response_json['mainInfo'].get('totalResults')) / int(response_json['mainInfo'].get('pageSize'))
        except KeyError:
            logger.error(f'Response JSON has no key "mainInfo". Possible that scraper is detected. Renewing session...')
            curr_session.close()
            newSession = False
            continue
        scrape_data.append(response_json)
        
        logger.info(f'Successfully scraped data from API in page {pagination} out of {totalPages:.0f} pages')
        pagination += 1
    
    
    with open('page_data.txt', 'w') as output:
        output.write(json.dumps(scrape_data))
    end_time = time.time()
    logger.info(f'Done scraping data for query in {end_time - start_time} seconds')

    return scrape_data


class LazadaScraper:
    def __init__(self, search_item: str, proxy_settings: dict | None) -> None:
        """Initialize the object with search of interest and 
           proxy settings dictionary with keys of proxy_url, 
           proxy_user, and proxy_passw"""
        
        self.search_item = search_item
        self.proxy_user = proxy_settings.get('proxy_user')
        self.proxy_passw = proxy_settings.get('proxy_passw')
        self.proxy_url = proxy_settings.get('proxy_url')