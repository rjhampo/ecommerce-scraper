from ecommerce_scraper.constants import DEFAULT_TIMEOUT, DELAY_MEAN, DELAY_STD
from ecommerce_scraper.proxy import Proxy


class BaseScraper:
    def __init__(self, home_url: str, search_query: str, proxy_config: dict | None,
                 default_timeout: float | None = DEFAULT_TIMEOUT, delay_mean: float | None = DEFAULT_TIMEOUT,
                 delay_std: float | None = DELAY_STD) -> None:
        """Initialize scraper with following params:
           - home_url which takes a URL string that directs to the ecommerce website's homepage
           - search_query which takes the item to search e.g. soap, chips, etc.
             This doesn't accept regular expressions
           - proxy_config dict having at least one of the following items: 
                + proxy (which either contains a url string or a generator)
                + proxy_user
                + proxy_passw
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

    def _get_browser_info(self):
        """Gets the necessary cookies, headers, and other info to 
           help the scraper pass as a human"""
        pass

    def _get_new_session(self):
        """Used to re-create a session after detected by
           anti-bot measures or for initialization;
           Used for requests-like packages with session object"""
        pass

    def page_scraper(self):
        """For scraping pages from a search result; 
           Sufficient for broad data gathering; Use item_scraper
           for more details on entries obtained from this"""
        pass

    def item_scraper(self):
        """For scraping item pages"""
        pass