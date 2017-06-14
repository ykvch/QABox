#!/usr/bin/env python


def attach_tests(source_class):
    """Class decorator that adds test_* methods to decorated class

    Params:
        source_class: a source class with test_* methods to add to decorated class
    """
    def wrapper(target_class):
        suffix = getattr(target_class, 'SUFFIX')
        suffix = '_' + suffix if suffix else ''
        for name, m in vars(source_class).items():
            if callable(m) and name.startswith('test_'):
                target_method = overcome_bubble(m)
                target_method.__doc__ = m.__doc__.format(**vars(target_class))
                target_method.__name__ = name + suffix
                setattr(target_class, name + suffix, target_method)
        return target_class
    return wrapper


def overcome_bubble(method):
    """Helper function to create extra closure around lambda"""
    return lambda *args, **kwargs: method(*args, **kwargs)
