# -*- coding: utf-8 -*-
"""
Handy wrappers for advanced object comparing/matching.

Comparator functions bind value(s) AND compare logic into single item.
Similarly to pytest.approx(...)

NOTE: Example below is purely synthetic.
EXAMPLE: A function to validate HTTP response object attributes
>>> dir(response)
['status', 'headers', 'body', 'body_len'] # int, dict, str, int respectively

Simple validator may look like (could be oneliner):

>>> def validate(response, **kwargs):
>>>     for k, v in kwargs.items():
>>>         if getattr(response, k) == v:
>>>             continue
>>>         else:
>>>             raise AssertionError(k, v)

Usage (check if status is 200 and body is 'asdf'):
>>> validate(response, status=200, body='asdf')

Now let's make requirements a little tricky.

Check if body_len is between 300 and 400 bytes (incl) and status code is < 206.
Pushing compare logic into validator will eventually overwhelm it with complex
code, arguments or even magic.

Instead we may leave trivial method above unchanged and use comparators:
>>> from comparators import lt, within  # less-than, fits-range
>>> validate(response, status=lt(206), body_len=within(300, 400))

Now when validator tries to `==` status, it will check if its less-than 206.
When running `==` with body_len, it will check if it fits into range [300..400].
Profit!

A few steps to make things even prettier:

>>> def validate(response, **kwargs):
>>>     for k, v in kwargs2cmp(kwargs):  # arg name parsing kicks in here
>>>     # allow kwargs to be interpreted as
>>>     # <argument-name>_<compare-logic>=<expected-value>
>>>         if getattr(response, k) == v:
>>>             continue
>>>         else:
>>>             raise AssertionError(k, v)

And usage becomes even simpler:
>>> validate(response, status_lt=206, body_len_within=[300, 400])

After more refactoring validate becomes (see all_attrs doc for help):

def validate(response, **kwargs):
        if not all_attrs(response, kwargs2cmp(kwargs)):
            raise AssertionError(response, kwargs)
"""

import re


_COMPARATORS = {}  # dict of known comparator objects


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
        repr_ = lambda self_: '{0}({1})'.format(
            method.__name__, ', '.join(repr(i) for i in condition))
        return type('Cmp', (), {'__eq__': eq, '__repr__': repr_})()
    wrap.__doc__ = method.__doc__
    # Store comparator to assist kwargs2cmp function
    _COMPARATORS[method.__name__] = wrap
    return wrap


# Sample handy comparators

@comparator
def within(val, a, b):
    return a <= val <= b


@comparator
def contains(val, param):
    return param in val


@comparator
def one_of(val, condition):
    return val in condition


@comparator
def lt(val, condition):
    return val < condition


@comparator
def gt(val, condition):
    return val > condition


@comparator
def le(val, condition):
    return val <= condition


@comparator
def ge(val, condition):
    return val >= condition


@comparator  # TODO: invent better names for these
def ne(val, condition):
    return not(val == condition)


@comparator
def eq_all(val, *condition):
    return all(val == i for i in condition)


@comparator
def eq_any(val, *condition):
    return any(val == i for i in condition)


@comparator
def re_search(val, pattern):
    return re.search(pattern, val) is not None


@comparator
def re_match(val, pattern):
    return re.match(pattern, val) is not None

@comparator
def endswith(val, condition):
    return val.endswith(condition)


@comparator
def eq(val, condition):  # pylint: disable=invalid-name
    return val == condition


@comparator
def contains_dict(dict_val, *args, **kwargs):
    expected_dict = dict(*args, **kwargs)
    try:
        return all(v == dict_val[k] for k, v in expected_dict.items())
    except KeyError:
        return False


# Convenience functions to assist parsing kwargs and compare agains objects

def kwargs2cmp(kwargs):
    """Convert kwargs to comparator-s list

    Args:
        kwargs (dict): a dict taken from kwargs where each item is
            <var-name>_<comparator-name>: <value>

    Returns:
        list of (<var-name>: <comparator-name>(value))
    """
    regex = re.compile(f"^(\\w+)_({'|'.join(k for k in _COMPARATORS)})")
    retval = []
    for k, v in kwargs.items():
        match_result = regex.fullmatch(k)
        if match_result:
            var, func_name = match_result.groups()
            retval.append((var, _COMPARATORS[func_name](v)))
        else:
            retval.append((k, v))

    return retval


# XXX: think about handling exceptions from comparators
def all_items(val, pairs):
    return all(k in val and val[k] == v for k, v in pairs)


def all_attrs(obj, pairs):
    return all(hasattr(obj, k) and getattr(obj, k) == v for k, v in pairs)
