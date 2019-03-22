import http
import socketserver
import threading
import uuid
import os
import ssl

class TestWebServer():
    def __init__(self, routes, ssl_cert_file=None, ssl_key_file=None):
        super().__init__()
        if routes is None:
            routes = {}
        self.routes = routes
        self.ssl_cert_file = ssl_cert_file
        self.ssl_key_file = ssl_key_file

    def start(self):
        # Start a little web server for testing against for the url methods.
        http_server_port = 8002
        # handler = http.server
        self.inst_id = uuid.uuid4()
        class TestServer(http.server.HTTPServer):
            allow_reuse_address = True


        # assign routes locally so the following class can pick them
        # up simply by closure.
        routes = self.routes
        
        class MyHandler(http.server.SimpleHTTPRequestHandler):
            def do_HEAD(self): 
                route = routes.get(self.path, None)
                if route is None: 
                    route = {
                        'status': {
                            'code': 404,
                            'message': 'Not Found'
                        },
                        'header': {
                            'Content-Type': 'text/plain',
                            'Content-Length': 100
                        }
                    }

                self.send_response(route['status']['code'], message=route['status']['message'])

                for (name, value) in route['header'].items():
                    self.send_header(name, value)

                self.end_headers()
                
        self.httpd = TestServer(("localhost", http_server_port), MyHandler)

        if self.ssl_cert_file:
            self.httpd.socket = ssl.wrap_socket(self.httpd.socket, certfile=self.ssl_cert_file, keyfile=self.ssl_key_file, server_side=True)

        self.httpd_thread = threading.Thread(target=self.httpd.serve_forever)
        self.httpd_thread.setDaemon(True)
        self.httpd_thread.start()
    
    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.httpd_thread.join()