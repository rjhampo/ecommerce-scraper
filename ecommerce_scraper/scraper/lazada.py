import json, time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from curl_cffi import requests
from requests import HTTPError

from ecommerce_scraper.scraper.base import BaseScraper
from ecommerce_scraper import scraper_logger


class LazadaScraper(BaseScraper):
    def __init__(self, home_url, search_query, proxy_config,
                 default_timeout = ..., delay_mean = ..., delay_std = ...):
        super().__init__(home_url, search_query, proxy_config, default_timeout, delay_mean, delay_std)

    def _get_browser_info(self) -> list:
        scraper_logger.debug(f'Getting browser data from {self.home_url} through proxy {self.proxy_config.current_proxy}')
        with Stealth().use_sync(sync_playwright()) as p:
            browser = p.firefox.launch(proxy={'server': self.proxy_config.current_proxy, 'username': self.proxy_config.proxy_user, 'password': self.proxy_config.proxy_passw}, headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(self.default_timeout)
            page.goto(self.home_url)
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
    
    def _get_new_session(self) -> requests.Session:
        self.proxy_config.current_proxy = self.proxy_config.get_proxy()
        scraper_logger.info(f'Opening browser... Answer any CAPTCHAs that may appear during this time. Press "Resume" in Playwright inspector to continue execution after answering CAPTCHA')
        browser_data = self._get_browser_info()
        headers = self._get_headers()
        headers['X-CSRF-TOKEN'] = browser_data['csrf_token']
        scraper_logger.debug(f'Obtained new cookies and new header = {headers}')
        new_session = requests.Session()
        scraper_logger.debug(f'Obtained new session')
        new_session.cookies.update(browser_data['cookiejar'])
        new_session.proxies = {'https': self.proxy_config.current_proxy}
        new_session.headers = headers
        
        return new_session
    
    def run_page_scraper(self, item: str, proxy_settings: dict, pagination: int | None = 1) -> list:
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
                curr_session = self._get_new_session(html_url, proxy_settings)
                newSession = True

            try:
                self._random_delay()
                response = curr_session.request('GET', api_url, impersonate='chrome')
                response.raise_for_status()
            except HTTPError as error:
                scraper_logger.error(f'Failed to get from API with due to {error}', exc_info=True)
            
            response_json = response.json()
            self._random_delay()
            try:
                noMorePages = response_json['mainInfo'].get('noMorePages')
                if totalPages is None:
                    totalPages = int(response_json['mainInfo'].get('totalResults')) / int(response_json['mainInfo'].get('pageSize'))
            except KeyError:
                scraper_logger.error(f'Response JSON has no key "mainInfo". Possible that scraper is detected. Renewing session...')
                curr_session.close()
                newSession = False
                continue
            scrape_data.append(response_json)
            
            scraper_logger.info(f'Successfully scraped data from API in page {pagination} out of {totalPages:.0f} pages')
            pagination += 1
        
        
        with open('page_data.txt', 'w') as output:
            output.write(json.dumps(scrape_data))
        end_time = time.time()
        scraper_logger.info(f'Done scraping data for query in {end_time - start_time} seconds')

        return scrape_data