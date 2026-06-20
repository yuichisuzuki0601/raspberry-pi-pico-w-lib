from board.fs import read, read_as_binary
from lib.board.http_server import HttpServer
from board.wlan import Wlan
import config

def process(
        ap_ssid: str, 
        ap_password: str,
        title: str = 'Show Config'):

    index_html = read('lib/public/show-config/index.html')
    favicon_ico = read_as_binary('lib/public/common/favicon.ico')
    style_css = read('lib/public/common/style.css')

    http_server = HttpServer()

    def handle_index(_):
        configs = '\n'.join(f'{key}: {value}' for key, value in config.list().items())
        html = (index_html
                .replace('{title}', title)
                .replace('{configs}', str(configs) or '')
        )
        return HttpServer.MIME_HTML, html

    def handle_favion_ico(_):
        return HttpServer.MIME_ICO, favicon_ico

    def handle_style_css(_):
        return HttpServer.MIME_CSS, style_css

    http_server.add_mapping('/show-config', handle_index)
    http_server.add_mapping('/favicon.ico', handle_favion_ico)
    http_server.add_mapping('/style.css', handle_style_css)

    # =====

    print('=== Show Config Process Start ===')

    Wlan(ap_ssid, ap_password).launch_as_access_point()

    try:
        while True:
            http_server.observe()
    except BaseException as e:
        http_server.close()
        raise e
