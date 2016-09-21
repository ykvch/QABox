import logging
import os
import socket

from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.registry')

SERVER = 'localhost', 8888

class RegistryClient(Plugin):
    name = 'registry'

    def configure(self, options, conf):
        super(RegistryClient, self).configure(options, conf)
        if not self.enabled: return
        self.sock = socket.socket()
        self.sock.settimeout(100)
        self.sock.connect(SERVER)

    def finalize(self, result):
        self.sock.close()

    def wantFile(self, fname):
        bname = os.path.basename(fname)
        self.sock.send(bname+'\n')
        data = ''

        resp = self.sock.recv(1024)
        while '\n' not in resp:
            data += resp
            resp  = self.sock.recv(1024)
        data += resp

        recv_name, in_registry = data.rsplit()[-2:]
        assert recv_name == bname, 'Got incorrect filename from registry server'

        if int(in_registry): # already registrered by someone else
            return False # so we don't want that file
        # else: return None # meaning: let the selector decide
