# -*- coding: utf-8 -*-
"""
Comparator object combines both the value(s) to compare with
AND the information on HOW to provide that comparison.

It allows to bind compare logic into arguments.

NOTE(!)Example below is purely synthetic, just to give an impression of usage.

Ex.: We have a validator method that checks some HTTP response object
>>> dir(response)
['status', 'headers', 'body', 'body_len'] # int, dict, str, int respectively

Simple validator may look like (could be oneliner):

def validator(response, **kwargs):
    for k, v in kwargs.items():
        if getattr(response, k) == v:
            continue
        else:
            raise AssertionError(k, v)

Usage (check if status is 200 and body is 'asdf'):
>>> validator(response, status=200, body='asdf')

Now let's make things tricky.
Let's check if body_len is in between 300 and 400 bytes (incl) and status code is < 206.
We may extend validator and eventually overwhelm it with extra logic (or even magic).

Instead we may leave this method as is and use comparators:
>>> form comparators import lt, in_range  # less-than, fits-range
>>> validator(response, status=lt(206), body_len=in_range(300, 400))

Now when validator tries to `==` status, it will check if its less-than 206 instead.
And when running `==` with body_len, it will check if it falls into range [300..400].
Profit!
"""
import re


def comparator(method):
    """
    Decorator that produces `comparator` objects

    Args:
        A function that returns True of False.
        1st function argument is the value we want to measure.
        Remaining arguments would be used as compare conditions.

    Returns:
        `comparator` object where __eq__ gets substituted by given function.
        It calls given function for every comparison of other values to it.
    """
    def wrap(*condition):
        eq = lambda self_, val: method(val, *condition)
        repr_ = lambda self_: '{0}({1})'.format(method.__name__,
                                                ', '.join(str(i) for i in condition))
        return type('Cmp', (), {'__eq__': eq, '__repr__': repr_})()
    wrap.__doc__ = method.__doc__
    return wrap


# Sample comparators

@comparator
def in_range(val, a, b):
    return a <= val <= b


@comparator
def contains(iterable_val, param):
    return param in iterable_val


@comparator
def one_of(val, condition):
    return val in condition


@comparator
def lt(val, condition):
    return val < condition


@comparator
def gt(val, condition):
    return val > condition


@comparator  # TODO: invent better names for these
def ne(val, condition):
    return not(val == condition)


@comparator
def all_match(val, *condition):
    return all(val == i for i in condition)


@comparator
def any_matches(val, *condition):
    return all(val == i for i in condition)


@comparator
def search_regex(val, pattern):
    return re.search(pattern, val) is not None


@comparator
def match_regex(val, pattern):
    return re.match(pattern, val) is not None
