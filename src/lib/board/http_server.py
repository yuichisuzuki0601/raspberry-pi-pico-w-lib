from usocket import socket, AF_INET, SOCK_STREAM

class HttpServer():
    _PORT     = 80
    MIME_TEXT = 'text/plain'
    MIME_HTML = 'text/html'
    MIME_ICO  = 'image/x-icon'
    MIME_CSS  = 'text/css'
    MIME_JS   = 'application/javascript'

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', HttpServer._PORT))
        self.socket.listen()
        self.handlers = {}
        self.default_handler = None

    def add_mapping(self, path: str, handler):
        self.handlers[path] = handler

    def set_default_handler(self, handler):
        self.default_handler = handler

    def _build_response_header(self, mime: str, content_length: int):
        return (
            'HTTP/1.1 200 OK\r\n'
            f'Content-Type: {mime}\r\n'
            f'Content-Length: {content_length}\r\n'
            'Connection: close\r\n'
        )

    def observe(self): 
        conn, addr = self.socket.accept()

        request = conn.recv(1024).decode('utf-8')
        print(f'=== Request from {addr} ===')
        print(request)

        mime = HttpServer.MIME_TEXT
        content = ''
        found = False

        for path, handler in self.handlers.items():
            if f'GET {path}' in request:
                mime, content = handler(request)
                found = True
                break

        if not found and self.default_handler:
            mime, content = self.default_handler(request)

        response_header = self._build_response_header(mime, len(content))
        print(f'=== Rsponse to {addr} ===')
        print(response_header)

        response = f'{response_header}\r\n{content}'.encode('utf-8')
        conn.send(response)
        conn.close()

    def close(self):
        self.socket.close()
