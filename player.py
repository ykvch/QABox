#!/usr/bin/env
# -*- coding: utf-8 -*-

'''Video player abstraction'''

import time
from collections import deque
import requests

# Manifest -> Buffer -> Player

class Manifest(object):
    '''Produces Manifests to download'''
    def __init__(self, uri):
        self.uri = uri
        self.update_playlists()

    def update_playlists(self):
        pass

class Data(object):
    '''Consumes URLs, produces data'''
    def __init__(self, master):
        self.master = master
        self.data = deque()
        self.available = 0
        self.low = 1

    def __next__(self):
        '''Buffered read as iterator'''
        retry = 5
        while retry > 0 and self.available < self.low:
            retry -= 1
            # chunk = next(src)
            chunk = self.master.read(next(self.master.manifest))
            if chunk:
                self.available += len(chunk)
                self.data.append(chunk)

        ret = self.data.popleft()
        available -= len(ret)
        return ret

    next = __next__ # Py3

class Player(object):
    '''Consumes data'''
    def __init__(self, uri):
        self.manifest = auto_uri(uri)
        self.read = detect_readmethod(uri)
        self.data = Data(self)
        self.current_pos = 0
        self.current_ts = 0

    def play_live(self):
        for i in self.data:
            self.sleep(i.duration)
            self.current_pos += i.duration

    def play_chunk(self):
        pass

    def sleep(self, duration):
        '''Sleep until <duration> seconds since last sleep pass'''
        self.current_pos = (self.current_pos or time.time()) + duration
        time.sleep(self.current_pos-time.time())


def auto_uri(uri):
    '''Detect Manifest producer'''
    return Manifest(uri)

def detect_readmethod(uri):
    if uri.startswith('http'):
        return requests.get
    raise RuntimeError('Unknown read method for URI: {0}'.format(uri))

class IterBuffer(object):
    retry = 5
    low = 1

    def __init__(self):
        self.buffer = deque()

    def __iter__(self):
        return self

    def next(self):
        '''Buffered read as generator'''
        print 'data.next...'
        retry = self.retry
        while (retry > 0) and self.is_low():
            print 'retry ...', retry
            retry -= 1
            self.update_buffer()

        return self.read_buffer()

    __next__ = next # Py3

    def is_low(self):
        return len(self.buffer) < self.low

    def update_buffer(self):
        self.buffer.append(None)

    def read_buffer(self):
        return self.buffer.popleft()

