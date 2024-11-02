from ecommerce_scraper.proxy import Proxy


class BaseScraper:
    def __init__(self, proxy_config: dict | None):
        """Initialize scraper with proxy_config dict having at least 
           one of the following items: proxy (which either contains a url string or 
           a generator), proxy_user, and proxy_passw"""
        self.proxy_config = Proxy(proxy=proxy_config.get('proxy'), proxy_user=proxy_config.get('proxy_user'),
                                  proxy_passw=proxy_config.get('proxy_passw'))

    def _get_browser_info(self):
        """Gets the necessary cookies and headers to 
           help the scraper pass as a human"""
        pass

    def page_scraper(self):
        """For scraping pages from a search result; 
           Sufficient for broad data gathering; Use item_scraper
           for more details on entries obtained from this"""
        pass

    def item_scraper(self):
        """For scraping item pages"""
        pass