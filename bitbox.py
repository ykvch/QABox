#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BitBox(object):
    '''
    Represent and manipulate char-string as bit list
    (with 0 index indicating the very 1st bit of given string)
    '''
    # NOTE: string is immutable, so copy has to be created
    # for manipulations. Is it possible to optimize that?
    # NOTE: possibly implement __getslice__ and __setslice__ magic
    def __init__(self, data_str=''):
        self._bf = [ord(i) for i in data_str]

    def __getitem__(self, index):
        # index is the bit num, first find out in which byte it belongs:
        byte = self._bf[index >> 3]
        # NOTE: In order to preserve bit order similar to byte order
        # (which is "left-to-right") we pretend that bit order is big-endian
        return (byte << (index & 7) >> 7) & 0b1

    def __setitem__(self, index, value):
        # same as getitem: index is bit num, NOT byte
        byte_index = index >> 3
        value = (value & 0b1) << 7 >> (index & 7)
        mask = 0b10000000 >> (index & 7)
        self._bf[byte_index] = (self._bf[byte_index] & ~mask) | value

    def __str__(self):
        return ''.join(chr(c) for c in self._bf)

    def append(self, str_item):
        '''Append string, stringifiable or BitBox object'''
        self._bf += [ord(c) for c in str(str_item)]

    @property
    def bitstring(self):
        return ''.join('{0:08b}'.format(c) for c in self._bf)

    @property
    def bytelist(self):
        return self._bf
