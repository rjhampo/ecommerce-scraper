from typing import Iterable, Iterator, Union
from ecommerce_scraper.exceptions import StaleProxy


class Proxy:
    def __init__(self, proxy: Union[str, Iterator, Iterable, None] = None, 
                 proxy_user: str | None = None, proxy_passw: str | None = None) -> None:
        match proxy:
            case Iterator():
                self.proxy_factory = proxy
                self.proxy_url = None
            case Iterable():
                self.proxy_factory = iter(proxy)
                self.proxy_url = None
            case str():
                self.proxy_factory = None
                self.proxy_url = proxy
            case _:
                self.proxy_url = None
                self.proxy_factory = None
        
        self.proxy_user = proxy_user
        self.proxy_passw = proxy_passw
        self.is_fresh = True
    
    def get_proxy(self):
        if not self.is_fresh and self.proxy_url:
                raise StaleProxy
        if self.proxy_url: return self.proxy_url
        else: yield self.proxy_factory