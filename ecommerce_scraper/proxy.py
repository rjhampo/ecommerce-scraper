from typing import Iterable, Iterator, Union


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
    
    def _get_proxy_endpoint(self):
        yield self.proxy_factory
