#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys
import socket
import asyncore
import logging

LOG = logging.getLogger('registry_server')
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level='INFO')

MAGIC_SEQUENCE = 'thank you'

class RegHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, master):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.master = master
        self.buffer = ''

    def handle_read(self):
        head, sep, tail = self.recv(1024).partition('\n')

        while sep: # handle case of multiple lines in one recv
            if head == MAGIC_SEQUENCE: # shut down the server
                for m in asyncore.socket_map.values():
                    m.close()
            self.send_response(self.buffer+head)
            self.buffer = ''
            head, sep, tail = tail.partition('\n')
        # if something remains without \n, store it for the next handle_read
        self.buffer = head

    def send_response(self, item):
        taken_already = item in self.master.registry
        if not taken_already:
            self.master.registry.add(item)
        self.send('{0} {1:d}\n'.format(item, taken_already))
        LOG.info('{0}: {1} {2}'.format(self.addr, item,
                'already taken' if taken_already else 'OK'))


class RegServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.registry = set()

    def handle_accept(self):
        sock_addr = self.accept()
        if sock_addr is None: return
        sock, addr = sock_addr
        LOG.info('Incoming connection from {0}'.format(addr))
        RegHandler(sock, self)

if __name__ == '__main__':
    args = dict(zip(('progname', 'host', 'port'), sys.argv))
    server = RegServer(args.get('host', 'localhost'), int(args.get('port', 8888)))
    asyncore.loop()
