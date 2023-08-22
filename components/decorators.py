# Deco for routes realization
class AppRoute:
    def __init__(self, routes, url):
        """
        Save value of transferred parameter
        :param routes: dict with urls
        :param url: path that is needed to be included into dict 'routes'
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Decorator itself.
        Key is route, value is cls-object.
        :param cls: class-controller object that we decorate
        """
        self.routes[self.url] = cls()
