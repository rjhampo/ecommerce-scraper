

class BaseScraper:
    def __init__(self):
        pass

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