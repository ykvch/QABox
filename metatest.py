#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import itertools
import sys

def mix_params(args_kwargs):
    args, kwargs = args_kwargs
    args_len = len(args)
    for i in itertools.product(*itertools.chain(args, kwargs.values())):
        yield tuple(i[:args_len]), dict(zip(kwargs.keys(), i[args_len:]))

def with_combinations(*args, **kwargs):
    def hook_args_kwargs(method):
        method.metatest_params = (args, kwargs)
        return method
    return hook_args_kwargs


class MetaTest(type):

    def __new__(cls, name, bases, attrs):
        for method in attrs.values():
            if callable(method) and hasattr(method, 'metatest_params'):
                for arg, kw in mix_params(method.metatest_params):
                    print arg, kw # Closure here!!!!
                    def test_steps(self, a=arg, k=kw): return method(self, *a, **k)
                    test_steps.__name__ = 'test_case ' + ', '.join(arg) + ' ' + ', '.join(str(k)+'='+str(v) for k,v in kw.items())
                    attrs[test_steps.__name__] = test_steps
        print (cls, name, bases, attrs)
        return super(MetaTest, cls).__new__(cls, name, bases, attrs)

class SuiteOne(TestCase):
    __metaclass__ = MetaTest

    def setUp(self):
        print 'running setup'

    @with_combinations(row='123', col='abc')
    def one(self, row, col):
        self.assertFalse(row)

    runTest = lambda *args: True

class T2(TestCase):
    def test_case_two(self):
        assert True
