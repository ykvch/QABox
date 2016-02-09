#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import string

'''
Rationale:

Imagine we need to run the same test steps multiple times, but each time with different
parameter combinations.
For example: Testing all combinations of A=(0,1,2) and B=['a','b','c'] would require 9 tests as follows:
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
1) Import MultiTestMeta (or MultiTestMixin) from this file.
2) Create a test class with `__metaclass__ = MultiTest` (or inherit it from MultiTestMixin)
3) Inside it create test case methods that accept extra params for A and B
and decorate them as follows:

@with_combined(A=[0,1,2], B='abc')
def method(self, A, B):...

Note1: that extra params after `self` have to conform the one's in decorator.
Note2: these do NOT HAVE to be only the named params, just make sure that their
    amount and naming fit `method` arguments.
Note3: there can be multiple decorated test methods in each test class.
Note4: no need for `test_` prefix, our metaclass will add that automatically
    (this way we make sure that unittest will not try to mess with our
    decorated test-methods and their "missing" extra params).
Note5: these generated tests CAN BE RUN SEPARATELY as if they really
    exist in the file (just make sure shell won't try to interpret spaces
    in generated method name, i.e. place qoutes or backslashes where needed).

That's all. Our metaclass will then spawn extra 9 methods each containing
a `method` call, but with different param combinations (as shown below):
test_method(A=0, B='a'); test_method(A=0, B='b'); test_method(A=0, B='c');
test_method(A=1, B='a'); test_method(A=1, B='b'); ... test_method(A=2, B='c');

Should work fine with python -m unittest your_generated_tests_file
OR with nose tests runner.

Any questions? Contact me on github. User: yan123
'''

def mix_params(args_kwargs):
    '''Takes args/kwargs tuple and returns all param combinations inside.
    Each item inside args or kwargs is expected to be an iterable
    of all desired values for that certain parameter'''
    args, kwargs = args_kwargs
    args_len = len(args)
    # values() is guaranteed to have the same order as keys(), we exploit that below
    for i in itertools.product(*itertools.chain(args, kwargs.values())):
        yield tuple(i[:args_len]), dict(zip(kwargs.keys(), i[args_len:]))

def with_combined(*args, **kwargs):
    '''Decorator. Adds _metatest_params=(args, kwargs) field to decorated method.
    _metatest_params is a marker for MultiTest class to see which
    methods have to be spawned into multiple tests'''
    def hook_args_kwargs(method):
        method._metatest_params = (args, kwargs)
        return method
    return hook_args_kwargs

class MultiTestMeta(type):
    '''Spawns multiple tests for every `with_combined` decorated method in subtyped class.
    Adds test_ prefix to each method, so it can be recognized as a test'''
    def __new__(cls, name, bases, attrs):
        for method in attrs.values():
            if callable(method) and hasattr(method, '_metatest_params'):
                for test_args, test_kwargs in mix_params(method._metatest_params):
                    # Closure here, using default args trick!!!
                    def actual_test(self, me=method, ar=test_args, kw=test_kwargs):
                        return me(self, *ar, **kw)

                    sub_dict = dict(('arg'+str(num), val) for num, val in enumerate(test_args))
                    sub_dict.update(test_kwargs)
                    actual_test.__doc__ = string.Template(method.__doc__).safe_substitute(sub_dict)

                    method_name = ('test_'+ method.__name__ +
                            (' ' if test_args or test_kwargs else '') +
                            ', '.join(str(a) for a in test_args) +
                            (', ' if test_args and test_kwargs else '') +
                            ', '.join(str(k)+'='+str(v) for k,v in test_kwargs.items()))
                    actual_test.__name__ = method_name
                    attrs[method_name] = actual_test

        return super(MultiTestMeta, cls).__new__(cls, name, bases, attrs)

class MultiTestMixin(object):
    '''Enables spawning multiple tests methods via with_combined
    decorator via inheritance'''
    __metaclass__ = MultiTestMeta

if __name__ == '__main__':
    # Usage example:
    import unittest

    class SuiteExample(unittest.TestCase, MultiTestMixin):
        # __metaclass__ = MultiTestMeta # forces use of test generator
        # runTest = lambda *args: True # for debugging purposes only

        def setUp(self):
            print '\nrunning setup'

        def tearDown(self):
            print '\ndoing cleanup after test'

        # Decorator means: produce 18 tests, each containing one method call
        # e.g. (the 1st test): steps2execute(self, 1, col='a', extra='+')
        # or (the 18th test): steps2execute(self, 3, col='c', extra='-')
        @with_combined((1,2,3), col=['a','b','c'], extra='+-')
        def steps2execute(self, row, col, extra):
            '''test steps *args[0]=$arg0 col=$col extra=$extra params'''
            print 'doing some steps with: row='+str(row)+', col='+col+', extra='+extra
            self.assertFalse(row*col+extra)

    # Just a dummy test suite without decorators:
    class T2(unittest.TestCase):
        def test_case_two(self):
            assert True

    unittest.main()
