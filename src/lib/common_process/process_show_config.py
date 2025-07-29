from board.fs import read, read_as_binary
from board.html_server import HtmlServer
from board.wlan import Wlan
import config

def process(
        ap_ssid: str, 
        ap_password: str,
        title: str = 'Show Config'):

    index_html = read('lib/public/show-config/index.html')
    favicon_ico = read_as_binary('lib/public/common/favicon.ico')
    style_css = read('lib/public/common/style.css')

    html_server = HtmlServer()

    def handle_index(_):
        configs = '\n'.join(f"{key}: {value}" for key, value in config.list().items())
        html = (index_html
                .replace('{title}', title)
                .replace('{configs}', str(configs) or '')
        )
        return html, True

    def handle_favion_ico(_):
        return favicon_ico, False

    def handle_style_css(_):
        return style_css, False

    html_server.add_mapping('/show-config', handle_index)
    html_server.add_mapping('/favicon.ico', handle_favion_ico)
    html_server.add_mapping('/style.css', handle_style_css)

    # =====

    print('=== Show Config Process Start ===')

    Wlan(ap_ssid, ap_password).launch_as_access_point()

    try:
        while True:
            html_server.observe()
    except BaseException as e:
        html_server.close()
        raise e
