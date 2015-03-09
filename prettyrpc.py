#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy

class PrettyProxy(object):
    def __init__(self, *args, **kwargs):
        self._real_proxy = ServerProxy(*args, **kwargs)

    def __getattr__(self, name):
        return lambda *args, **kwargs: getattr(self._real_proxy, name)(args, kwargs)
