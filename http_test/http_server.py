#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import socket
import random
import string
import json
import threading
import BaseHTTPServer

ADDRESS = ('localhost', 8081)
CODES = (200, 200, 200, 300, 400) # gives ~60% probability to get 200 OK

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''Random response HTTP server'''

    protocol_version = 'HTTP/1.1'

    def do_GET(self):
        self.send_response(random.choice(CODES))
        self.send_header('Content-Type', 'application/json')
        random_str = ''.join(random.sample(string.printable, 10))
        data = json.dumps({'request_path': self.path, 'data': random_str})+'\r\n'
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    do_POST = do_GET


class ThreadHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, addr, handler):
        BaseHTTPServer.HTTPServer.__init__(self, addr, handler, bind_and_activate=False)

    def run(self):
        self.thread = threading.Thread(target=self.serve_forever)
        self.thread.daemon = True
        self.server_bind()
        self.server_activate()
        self.thread.start()

    def stop(self):
        self.shutdown()
        self.thread.join()
        self.server_close()
        self.socket = socket(self.address_family, self.socket_type)

server = ThreadHTTPServer(ADDRESS, RequestHandler)
