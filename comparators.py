# -*- coding: utf-8 -*-


def comparator(method):
    def wrap(*condition):
        eq = lambda slf, val: method(val, *condition)
        return type('Cmp', (), {'__eq__': eq})()
    wrap.__doc__ = method.__doc__
    return wrap


@comparator
def in_range(val, a, b):
    return a <= val <= b


@comparator
def contains(iterable_val, param):
    '''Check if iterable contains given param

    Args:
        param (any type): a sequence entry, a dict key, etc

    Returns:
        A comparator object that can check if given param in some iterable
            by using == operator
    '''
    return param in iterable_val


@comparator
def one_of(item_val, condition):
    return item_val in condition


@comparator
def lt(val, condition):
    return val < condition


@comparator
def gt(val, condition):
    return val > condition
