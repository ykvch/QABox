#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
import itertools

'''
Rationale:

Imagine we need to run the same test steps multiple times, but each time with different
parameter combinatins.
For 2 params A and B, we can represent this as a table, where columns stand for A values,
and rows for B values.
So, if we need to test all possible combinations of A=(0,1,2) and B=['a','b','c'],
that would require 9 tests as follows:
+-------------------------------+
|       |  A=0  |  A=1  |  A=2  |
+-------------------------------+
| B='a' | test0 | test1 | test2 |
+-------------------------------+
| B='b' | test3 | test4 | test5 |
+-------------------------------+
| B='c' | test6 | test7 | test8 |
+-------------------------------+

Copy-pasting, or using nose generator plugin might sometimes not be an option.

So here's the solution:
1) Import MetaTest from this file.
2) Create a test class with `__metaclass__ = MetaTest`
3) Inside it create test case methods that accept extra params for A and B
and decorate them as follows:

@with_combined(A=[0,1,2], B='abc')
def test_method(self, A, B):...

Note: that extra params after `self` have to conform the one's in decorator.
Note2: these do NOT HAVE to be only the named params, just make sure that their
amount and naming fit test_method arguments.
Note3: there can be multiple decorated test methods in each test class.

That's all. Our metaclass will then spawn extra 9 methods each containing
a `test_method` call, but with different param combinations (as shown below):
test_method(A=0, B='a'); test_method(A=0, B='b'); test_method(A=0, B='c');
test_method(A=1, B='a'); test_method(A=1, B='b'); ... test_method(A=2, B='c');

Try it with python -m unittest your_generated_tests_file
OR with nose tests runner.
'''

def mix_params(args_kwargs):
    '''Helper generator function. Takes args+kwargs tuple
    and returns all param combinations. Each item inside args or kwargs is
    expected to be an iterable of all desired input values for that certain variable'''
    args, kwargs = args_kwargs
    args_len = len(args)
    for i in itertools.product(*itertools.chain(args, kwargs.values())):
        yield tuple(i[:args_len]), dict(zip(kwargs.keys(), i[args_len:]))

def with_combined(*args, **kwargs):
    '''Decorator. Adds metatest_params=(args, kwargs) field to decorated
    function or method. metatest_params is a marker for MetaTest class to see which
    methods have to be wrapped into multiple tests'''
    def hook_args_kwargs(method):
        method.metatest_params = (args, kwargs)
        return method
    return hook_args_kwargs

class MetaTest(type):
    '''Generates multiple tests based on decorated method(s) in subtyped class.
    Adds test_ prefix to each method, so it can be recognized as a test'''
    def __new__(cls, name, bases, attrs):
        for method in attrs.values():
            if callable(method) and hasattr(method, 'metatest_params'):
                for test_args, test_kwargs in mix_params(method.metatest_params):
                    # Closure here, using default args trick!!!
                    def actual_test(self, ar=test_args, kw=test_kwargs):
                        return method(self, *ar, **kw)
                    method_name = ('test_'+ method.__name__ + ' ' +
                            ''.join(str(a)+', ' for a in test_args) +
                            ', '.join(str(k)+'='+str(v) for k,v in test_kwargs.items()))
                    actual_test.__name__ = method_name
                    attrs[method_name] = actual_test
        return super(MetaTest, cls).__new__(cls, name, bases, attrs)

# Usage example:
class SuiteExample(TestCase):
    __metaclass__ = MetaTest # forces use of test generator
    # runTest = lambda *args: True # for debugging purposes only

    def setUp(self):
        print '\nrunning setup'

    def tearDown(self):
        print '\ndoing cleanup after test'
    
    # this one is decorated, so we'll spawn many tests from it
    # this will produce 18 tests, each containing a method call
    # like (the 1st test): steps2execute(self, 1, col='a', extra='+')
    # or like (the 18th test): steps2execute(self, 3, col='c', extra='-')
    @with_combined((1,2,3), col=['a','b','c'], extra='+-')
    def steps2execute(self, row, col, extra):
        '''test steps'''
        print('doing some steps with: row='+str(row)+', col='+col+', extra='+extra)
        self.assertFalse(row*col+extra)

# Just a plain test suite without generations:
class T2(TestCase):
    def test_case_two(self):
        assert True
