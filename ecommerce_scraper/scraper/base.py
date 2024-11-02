from ecommerce_scraper import USER_AGENTS
from ecommerce_scraper.constants import DEFAULT_TIMEOUT, DELAY_MEAN, DELAY_STD
from ecommerce_scraper.proxy import Proxy
from time import sleep
import random


class BaseScraper:
    def __init__(self, home_url: str, search_query: str, proxy_config: dict | None, output_file: str | None = 'output.txt',
                 user_agents: list[str] | None = USER_AGENTS, default_timeout: float | None = DEFAULT_TIMEOUT,
                 delay_mean: float | None = DELAY_MEAN, delay_std: float | None = DELAY_STD) -> None:
        """Initialize scraper with following params:
           - home_url which takes a URL string that directs to the ecommerce website's homepage
           - search_query which takes the item to search e.g. soap, chips, etc.
             This doesn't accept regular expressions
           - output_file which takes a str Path
           - proxy_config dict having at least one of the following items: 
                + proxy (which either contains a url string or a generator)
                + proxy_user
                + proxy_passw
           - user_agents list which should contain at least one user agent
           - default_timeout - time in milliseconds for use in Playwright
           - delay_mean - time in seconds for use in delays using normal distribution
           - delay_std - time in seconds for use in delays using normal distribution
           """
        self.proxy_config = Proxy(proxy=proxy_config.get('proxy'), proxy_user=proxy_config.get('proxy_user'),
                                  proxy_passw=proxy_config.get('proxy_passw'))
        self.home_url = home_url
        self.search_query = search_query
        self.default_timeout = default_timeout
        self.delay_mean = delay_mean
        self.delay_std = delay_std
        self.output_file = output_file
        self.user_agents = user_agents

    def _get_browser_info(self):
        """All-in-one function which gets the necessary cookies, headers,
           and other info to help the scraper pass as a human"""
        pass

    def _get_new_session(self):
        """Used to re-create a session after detected by
           anti-bot measures or for initialization;
           Used for requests-like packages with session object;"""
        pass

    def _process_headers(self, header, user_agent):
        """Combine pre-defined header and user agent while preserving header item order"""
        pass

    def _random_delay(self):
        """Default delay function for careful scraping. This can be modified depending on your use case"""
        if random.random() > 0.5: sleep(abs(random.gauss(DELAY_MEAN, DELAY_STD)) * random.uniform(0.5,1.5))
        else: sleep(abs(random.gauss(DELAY_MEAN, DELAY_STD)) + random.random())

    def page_scraper(self):
        """For scraping pages from a search result; 
           Sufficient for broad data gathering; Use item_scraper
           for more details on entries obtained from this"""
        pass

    def item_scraper(self):
        """For scraping item pages"""
        pass