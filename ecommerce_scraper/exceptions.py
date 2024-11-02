class StaleProxy(Exception):
    def __init__(self, *args):
        self.message = 'Proxy is already detected by the web page. Replace with a new URL or pass a generator next time.'
        super().__init__(self.message, *args)