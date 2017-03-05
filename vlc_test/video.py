#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import time
import ctypes
import vlc

inst = vlc.Instance()


# class Player(object):
#     def __init__(self, url):
#         self.inst = inst
#         log_cb = cb.LogCb(self.logger)
#         inst.log_set(log_cb, ctypes.create_string_buffer(1024))
#         media = self.inst.media_new(url)
#         self.player = self.inst.media_player_new()
#         self.player.set_media(media)

#     def logger(self, *args):
#         print time.time(), args[3]

history = []


def logger(*args):
    item = (time.time(), args[3])
    history.append(item)
    print item


log_cb = vlc.cb.LogCb(logger)
inst.log_set(log_cb, ctypes.create_string_buffer(1024))
player = inst.media_player_new()


def open_media(url):
    media = inst.media_new(url)
    player.set_media(media)

if __name__ == '__main__':
    open_media(sys.argv[1])
    player.play()
    time.sleep(30)
    player.stop()
    sys.exit(0)
