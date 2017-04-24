#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inotify
import daemon
import requests

URL = ""
PROXY = ""
REPORT_DIR = ""
CORE_DIR = ""  # consider using sysctl


def on_send(host, link):
    requests.post(URL,
                  json={'attachments': [{'title': 'Crash',
                                         'fields': [{'title': 'Host',
                                                     'value': host,
                                                     'short': True},
                                                    {'title': 'Report',
                                                     'value': link,
                                                     'short': True}]}]})


def create_core_report(path):
    pass


def main():
    i = inotify.adapters.Inotify()
    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event

    finally:
        i.remove_watch()


if __name__ == '__main__':
    with daemon.DaemonContext():
        main()
