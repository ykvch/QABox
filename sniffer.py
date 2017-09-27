# coding: utf-8

import sys
import time
from threading import Event, Thread
from collections import namedtuple
import pcap

LogItem = namedtuple('LogItem', 'timestamp data')


class Sniffer():
    """Sample pcap sniffer capable to detect FreeBSD localhost"""

    def __init__(self):
        self._pcap = None
        self.l2_prefix = 0  # amount of data to strip from raw packets
        self._done = Event()
        self.log = []

    def start(self, iface):
        self.stop()  # stop previous sniffing session
        self._pcap = pcap.pcapObject()
        self._pcap.open_live(iface, 1600, 0, 100)
        # pcap.setfilter
        self.l2_prefix = 14 if self._pcap.datalink() else 4  # BSD DLT_NULL !!!
        self.thread = Thread(target=self.sniff)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._done.set()
        time.sleep(0.5)
        del self._pcap
        self._pcap = None

    def sniff(self):
        """Single iteration of pcap activity"""
        while not self._done.is_set():
            self._pcap.dispatch(1, self.dispatch)

    def dispatch(self, pkglen, data, timestamp):
        self.log.append(LogItem(timestamp, data[self.l2_prefix:]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage {} <iface-name>".format(sys.argv[0]))

    s = Sniffer()
    s.start(sys.argv[1])
    time.sleep(5)
    s.stop()

    for i in s.log:
        print("{}: {}".format(i.timestamp, i.data[:10]))
