import uasyncio
import ubinascii
import urandom
import ure
import usocket

class WebSocketClient:

    def __init__(self, hostname, port, path):
        self.hostname = hostname
        self.port = port
        self.path = path
        self.socket = usocket.socket()

    def __get_ip_address(self):
        ip_regex = ure.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if ip_regex.match(self.hostname):
            return self.hostname
        else:
            return usocket.getaddrinfo(self.hostname, self.port)[0][-1][0]

    def generate_random_bytes(self):
        return urandom.getrandbits(32).to_bytes(4, 'big')

    def __generate_websocket_key(self):
        random_bytes = b"".join(self.generate_random_bytes() for _ in range(4))
        key_base64 = ubinascii.b2a_base64(random_bytes).decode('utf-8')
        return key_base64.strip()

    def __create_websocket_request(self):
        headers = [
            "GET " + self.path + " HTTP/1.1",
            "Host: " + self.hostname + ":" + str(self.port),
            "Upgrade: websocket",
            "Connection: Upgrade",
            "Sec-WebSocket-Key: " + self.__generate_websocket_key(),
            "Sec-WebSocket-Version: 13"
        ]
        return "\r\n".join(headers) + "\r\n\r\n"

    def connect(self):
        try:
            self.socket.connect((self.__get_ip_address(), self.port))
            request = self.__create_websocket_request()
            print('=== WebSocket Handshake Request ===')
            print(request)
            self.socket.send(request)
            response = self.socket.recv(1024)
            print("=== WebSocket Handshake Response ===")
            print(response.decode('utf-8'))
        except BaseException:
            raise Exception('ERR: websocket connection failed.')

    def observe(self, on_message):
        response = self.socket.recv(1024)
        payload_length = response[1] & 0x7F
        payload_data = response[2:2+payload_length]
        decoded_data = payload_data.decode('utf-8')
        print("WebSocket Received: ", decoded_data)
        on_message(decoded_data)
