import quopri

from divo_framework.framework_requests import GetRequestClass


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page Not Found'


class Framework:

    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_applications = fronts_obj

    def __call__(self, environ, start_response):
        # Get the address to which user make the transition
        path = environ['PATH_INFO']

        # Closing slash checking
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        # Get all data from request
        method = environ['REQUEST_METHOD']
        request['method'] = method

        method_class = GetRequestClass(method)
        data = method_class.get_request_params(environ)
        request[method_class.dict_value] = Framework.decode_value(data)
        print(f'{method}: {Framework.decode_value(data)}')

        if path in self.routes_lst:
            view = self.routes_lst[path]

        else:
            view = PageNotFound404()

        for front_app in self.fronts_applications:
            front_app(environ, request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            value = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
            value_decode_str = quopri.decodestring(value).decode('UTF-8')
            new_data[key] = value_decode_str
        return new_data
