from abc import ABCMeta, abstractmethod


class Request(metaclass=ABCMeta):
    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    @abstractmethod
    def get_request_params(self, environ):
        pass


# GET-request with parameters handle
class GetRequests(Request):
    dict_value = 'get_params'

    def get_request_params(self, environ):
        # Obtain request params
        query_string = environ['QUERY_STRING']
        # Convert params into dict
        get_params = GetRequests.parse_input_data(query_string)
        return get_params


# POST-request with parameters handle
class PostRequests(Request):
    dict_value = 'data'

    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        # get body length
        content_length_data = environ.get('CONTENT_LENGTH')
        # Bring it to 'int'
        content_length = int(content_length_data) if content_length_data else 0
        # Read data if data
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        if data:
            # Deco data
            data_str = data.decode(encoding='utf-8')
            # Collect data to 'dict'
            return self.parse_input_data(data_str)
        return {}

    def get_request_params(self, environ):
        # Get data
        data = self.get_wsgi_input_data(environ)
        # Convert it to 'dict'
        data = self.parse_wsgi_input_data(data)
        return data


class GetRequestClass():
    def __new__(cls, method):
        if method == 'POST':
            return PostRequests()
        if method == 'GET':
            return GetRequests()
