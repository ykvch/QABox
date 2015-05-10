#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''A pair of classes that should mimic ServerProxy and SimpleXMLRPCServer
behaviour as precise as possible, but try to overcome XMLRPC limitations
on passing named arguments and non-standard values.

It is achived by converting all method parameters
to ASCII string via pickle-base64encode chain.
Base64decode-depickle is then done on receiving side by
a modified _dispatch method.

This allows using variety of python's objects as function argument values
and python's native style for passing positional and named arguments
in calls to XMLRPC methods.

Any questions? Contact me on github. User: yan123'''


from xmlrpclib import ServerProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer
from pickle import dumps, loads
from base64 import b64encode, b64decode

# xmlrpc_encode = lambda obj: b64encode(dumps(obj))
# xmlrpc_decode = lambda stri: loads(b64decode(stri))

class PrettyProxy(object):
    '''Use this for the client instead of ServerProxy'''
    def __init__(self, *args, **kwargs):
        self._real_proxy = ServerProxy(*args, **kwargs)

    def __getattr__(self, name):
        return lambda *args, **kwargs: getattr(self._real_proxy, name)(b64encode(dumps((args, kwargs))))

class PrettyServer(SimpleXMLRPCServer):
    '''Use this for the server instead of SimpleXMLRPCServer,
    consider reading _dispatch method description if You intend to override it'''

    def _dispatch(self, method, args_kwargs):
        '''Mostly a copy-paste of original method, but changes
        its logic to handle params as encoded tuple of (args, kwargs).
        The _dispatch method in registered instances should get now
        a properly decoded two-element (args, kwargs) tuple instead of just
        args list.
        Packing-unpacking is done transparently for registered methods and
        should not affect them (hopefully).'''
        try:
            func = self.funcs[method]
        except KeyError:
            func = None
            if self.instance is not None:
                if hasattr(self.instance, '_dispatch'):
                    return self.instance._dispatch(method, loads(b64decode(args_kwargs)))
                try:
                    func = resolve_dotted_atribute(self.instance,
                            method,
                            self.allow_dotted_names)
                except AttributeError:
                    pass

        if func is None:
            raise Exception('method {0} is not supported'.format(method))
        args, kwargs = loads(b64decode(args_kwargs))
        return func(*args, **kwargs)
