#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer

class PrettyProxy(object):
    def __init__(self, *args, **kwargs):
        self._real_proxy = ServerProxy(*args, **kwargs)

    def __getattr__(self, name):
        return lambda *args, **kwargs: getattr(self._real_proxy, name)(args, kwargs)

class PrettyServer(SimpleXMLRPCServer):
    def _dispatch(self, method, params):
        '''Changes logic of parent _dispatch method to handle params as
        a tuple of (args, kwargs)'''
        # TODO: missing methods handling as in parent class
        func = self.funcs[method]
        return func(*params[0], **params[1])
