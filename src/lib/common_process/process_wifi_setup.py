from board.fs import read, read_as_binary
from lib.board.http_server import HttpServer
from board.wlan import Wlan
from circuit_element.led import Led
from circuit_element.tact_switch import TactSwitch
import config

def process(
        ap_ssid: str, 
        ap_password: str, 
        tact_switch_enter_wifi_setup_mode: TactSwitch, 
        on_check_pin_number: int, 
        on_request_pin_number: int,
        title: str = 'Wifi Setup'):
    led_on_check = Led('led_on_check', on_check_pin_number)
    led_on_request = Led('on_request', on_request_pin_number)

    index_html = read('lib/public/wifi-setup/index.html')
    favicon_ico = read_as_binary('lib/public/common/favicon.ico')
    style_css = read('lib/public/common/style.css')
    common_js = read('lib/public/common/common.js')
    result_html = read('lib/public/wifi-setup/result.html')

    http_server = HttpServer()

    def handle_index(_):
        led_on_request.flash()
        wifi_ssid = config.get('wifi_ssid')
        wifi_password = config.get('wifi_password')
        html = (index_html
                .replace('{title}', title)
                .replace('{wifiSsid}', wifi_ssid or '')
                .replace('{wifiPassword}', wifi_password or '')
        )
        return HttpServer.MIME_HTML, html

    def handle_favion_ico(_):
        return HttpServer.MIME_ICO, favicon_ico

    def handle_style_css(_):
        return HttpServer.MIME_CSS, style_css

    def handle_common_js(_):
        return HttpServer.MIME_JS, common_js

    def handle_save(request):
        led_on_request.flash()
        data = request.split(' ')[1].replace('/save?', '').split('&')
        wifi_ssid = data[0].replace('wifi-ssid=', '')
        wifi_password = data[1].replace('wifi-password=', '')
        config.set('wifi_ssid', wifi_ssid)
        config.set('wifi_password', wifi_password)
        html = (result_html
                .replace('{wifiSsid}', wifi_ssid)
                .replace('{wifiPassword}', wifi_password)
        )
        return HttpServer.MIME_HTML, html

    def handle_redirect(_):
        redirect_header = 'HTTP/1.1 302 Found\r\nLocation: http://192.168.4.1/wifi-setup\r\n'
        return HttpServer.MIME_HTML, redirect_header

    http_server.add_mapping('/wifi-setup', handle_index)
    http_server.add_mapping('/favicon.ico', handle_favion_ico)
    http_server.add_mapping('/style.css', handle_style_css)
    http_server.add_mapping('/common/common.js', handle_common_js)
    http_server.add_mapping('/save', handle_save)
    http_server.set_default_handler(handle_redirect)

    tact_switch_enter_wifi_setup_mode.on_click(lambda: [
        led_on_check.flash(),
        print(f'wifi_ssid: {config.get('wifi_ssid')}, wifi_password: {config.get('wifi_password')}')
    ])

    # =====

    print('=== Wifi Setup Process Start ===')

    Wlan(ap_ssid, ap_password).launch_as_access_point()

    try:
        while True:
            http_server.observe()
    except BaseException as e:
        http_server.close()
        raise e
