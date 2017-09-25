#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys
import socket
import asyncore
import logging
import fnmatch

LOG = logging.getLogger('registry_server')
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level='DEBUG')

MAGIC_SEQUENCE = 'thank you'


class RegHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, master):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.master = master
        self.buffer = ''

    def handle_read(self):
        head, sep, tail = self.recv(1024).partition('\n')

        while sep:  # handle case of multiple lines in one recv
            if head == MAGIC_SEQUENCE:  # shut down the server
                for m in asyncore.socket_map.values():
                    m.close()
            self.dispatch_req(self.buffer + head)
            self.buffer = ''
            head, sep, tail = tail.partition('\n')
        # if something remains without \n, store it for the next handle_read
        self.buffer += head

    def dispatch_req(self, req):
        '''Parse request and call appropriate method to handle it
        req: request string (command arg0 arg1 arg2)
        '''
        cmd = req.split()
        LOG.debug('{0}: {1}'.format(self.addr, req))
        return getattr(self, cmd[0])(*cmd[1:])

    def take(self, item):
        # We register node only if tries to "take" file
        # Also ensures that previously deleted node would be re-registered
        node = self.master.registry.setdefault('{0}:{1}'.format(*self.addr), set())
        taken_already = any(item in r for r in self.master.registry.values())
        if not taken_already:
            node.add(item)
        self.send('{0} {1:d}\n'.format(item, taken_already))
        LOG.info('{0}: {1} {2}'.format(self.addr, item,
                                       'already taken' if taken_already else 'OK'))

    def ls(self, pattern='*', node='*'):
        for k, v in self.master.registry.items():
            if not fnmatch.fnmatch(k, node):
                continue
            fnlist = fnmatch.filter(v, pattern)
            if fnlist:
                self.send('[{0}]\n'.format(k))
                for i in fnlist:
                    self.send('{0}\n'.format(i))
        self.send('\n')

    def rm(self, pattern=''):
        k, v = self.master.registry.keys(), self.master.registry.values()
        rm_list = [fnmatch.filter(i, pattern) for i in v]
        for r, k, v in zip(rm_list, k, v):
            self.master.registry[k] = v.difference(r)
        self.send('{0}\n'.format(sum(len(x) for x in rm_list)))

    def nodes(self):
        for k, v in self.master.registry.items():
            self.send('{0} {1}\n'.format(k, len(v)))
        self.send('\n')

    def rmnode(self, node):
        if node in self.master.registry:
            del self.master.registry[node]
            self.send('1\n')
        else:
            self.send('0\n')


class RegServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.registry = {}

    def handle_accept(self):
        sock_addr = self.accept()
        if sock_addr is None:
            return
        sock, addr = sock_addr
        LOG.info('Incoming connection from {0}:{1}'.format(*addr))
        RegHandler(sock, self)

if __name__ == '__main__':
    args = dict(zip(('progname', 'host', 'port'), sys.argv))
    server = RegServer(args.get('host', 'localhost'), int(args.get('port', 8888)))
    asyncore.loop()
