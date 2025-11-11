from ujson import dumps
import urequests

from board.timestamp import jstNow

class HttpClient:
    TIMEOUT = 2#[s]

    def __init__(self, base_url: str):
        self.base_url = base_url

    def __noop(self, _): pass

    def post(self, path: str, headers: dict, body: dict, on_success, on_error = __noop):
        print(f'POST {self.base_url}/{path} {jstNow()}')
        try:
            m_headers = dict(headers or {})
            m_headers['Content-Type'] = 'application/json'
            m_headers['User-Agent'] = 'raspberry-pi-pico'
            response = urequests.post(
                f'{self.base_url}/{path}',
                data = dumps(body).encode('utf-8'),
                headers = m_headers,
                timeout = HttpClient.TIMEOUT
            )
            on_success(response)
            response.close()
        except Exception as e:
            on_error(e)

    def put(self, path: str, headers: dict, body: dict, on_success, on_error = __noop):
        print(f'PUT {self.base_url}/{path} {jstNow()}')
        try:
            m_headers = dict(headers or {})
            m_headers['Content-Type'] = 'application/json'
            m_headers['User-Agent'] = 'raspberry-pi-pico'
            response = urequests.put(
                f'{self.base_url}/{path}',
                data = dumps(body).encode('utf-8'),
                headers = m_headers,
                timeout = HttpClient.TIMEOUT
            )
            on_success(response)
            response.close()
        except Exception as e:
            on_error(e)
