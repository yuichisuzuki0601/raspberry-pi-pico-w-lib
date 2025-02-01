from network import WLAN, STA_IF, STAT_IDLE, STAT_GOT_IP, AP_IF
from utime import sleep

class Wlan:
    CONNECT_MAX_WAIT = 10#[s]

    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        print(f'ssid: {ssid}, password: {password}')

    def connect(self):
        wlan = WLAN(STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)

        max_wait = Wlan.CONNECT_MAX_WAIT
        while max_wait > 0:
            if wlan.status() < STAT_IDLE or wlan.status() >= STAT_GOT_IP:
                break
            max_wait -= 1
            print('waiting for network connection...')
            sleep(1)
            
        if wlan.status() == STAT_GOT_IP:
            status = wlan.ifconfig()
            print('network connected: ip = ' + status[0])
        else:
            raise Exception('ERR: network connection failed.')

    def launch_as_access_point(self):
        wlan = WLAN(AP_IF)
        wlan.config(essid = self.ssid, password = self.password)
        wlan.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.1'))  
        wlan.active(True)
        print('\nIP Address: {}\nNet Mask: {}\nGateway: {}\nDNS: {}\n'.format(*wlan.ifconfig()))
