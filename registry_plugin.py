#!/usr/bin/env
# -*- coding: utf-8 -*-

import logging
import os
import fnmatch
import socket
from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.registry')

class RegistryClient(Plugin):
    name = 'registry'
    reg_addr, sock = None, None

    def configure(self, options, conf):
        super(RegistryClient, self).configure(options, conf)
        if not self.enabled: return
        self.sock = None
        host, port = options.registry_server.rsplit(':', 1)
        self.reg_addr = host, int(port)
        self.pattern = options.registry_fnmatch
        self.connect_to_server()

    def connect_to_server(self):
        '''Creates client socket and connects to registry server
        defined in plugin options (see options method)'''
        self.sock = socket.socket()
        self.sock.settimeout(10)
        try:
            self.sock.connect(self.reg_addr)
        except socket.error:
            raise RuntimeError('Failed to connect to registry server at {0}'.format(self.reg_addr))

    def options(self, parser, env):
        super(RegistryClient, self).options(parser, env)
        parser.add_option('--registry-server',
                default=env.get('REGISTRY_SERVER', 'localhost:8888'),
                dest='registry_server',
                metavar='host:port',
                help='Running registry server network address')
        parser.add_option('--registry-fnmatch',
                default=env.get('REGISTRY_FNMATCH', 'test*.py'),
                dest='registry_fnmatch',
                metavar='pattern',
                help='Pattern to match for test-containing files')

    def finalize(self, result):
        self.sock.close()

    def wantFile(self, fname):
        bname = os.path.basename(fname)
        if not fnmatch.fnmatch(bname, self.pattern):
            return False

        self.sock.send(bname+'\n')
        data = resp = self.sock.recv(1024)
        while '\n' not in resp:
            resp = self.sock.recv(1024)
            if not resp: # reconnect
                self.connect_to_server()
            data += resp

        head, _, _ = data.partition('\n')
        recv_name, in_registry = head[:-2], head[-1]
        assert recv_name == bname, 'Got incorrect filename from registry server'

        if int(in_registry): # already registrered by someone else
            return False # so we don't want that file
        # else: return None # meaning: let the selector decide
