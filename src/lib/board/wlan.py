from network import WLAN, STA_IF, STAT_IDLE, STAT_GOT_IP, AP_IF
from utime import sleep

class Wlan:
    CONNECT_MAX_WAIT = 10#[s]

    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        print(f'ssid: {ssid}, password: {password}')

    def connect(self):
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        max_wait = Wlan.CONNECT_MAX_WAIT
        while max_wait > 0:
            if self.wlan.status() < STAT_IDLE or self.wlan.status() >= STAT_GOT_IP:
                break
            max_wait -= 1
            print('waiting for network connection...')
            sleep(1)
            
        if self.wlan.status() == STAT_GOT_IP:
            status = self.wlan.ifconfig()
            print('network connected: ip = ' + status[0])
        else:
            raise Exception('ERR: network connection failed.')
        
        return self

    def isconnected(self):
        return self.wlan.isconnected()

    def launch_as_access_point(self):
        wlan = WLAN(AP_IF)
        wlan.config(essid = self.ssid, password = self.password)
        wlan.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.1'))  
        wlan.active(True)
        print('\nIP Address: {}\nNet Mask: {}\nGateway: {}\nDNS: {}\n'.format(*wlan.ifconfig()))
        # TODO キャプティブポータルを一旦問題切り分けのためにコメントアウトする
        # def dns_thread():
        #     ip = '192.168.4.1'
        #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     sock.bind(('0.0.0.0', 53))
        #     while True:
        #         try:
        #             data, addr = sock.recvfrom(512)
        #             packet = data[:2] + b'\x81\x80' + data[4:6] + data[4:6] + b'\x00\x00\x00\x00' + data[12:]
        #             packet += b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
        #             packet += bytes(map(int, ip.split('.')))
        #             sock.sendto(packet, addr)
        #         except:
        #             continue
        # _thread.start_new_thread(dns_thread, ())
        # print("DNS Server started (Captive Portal mode)")
