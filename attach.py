#!/usr/bin/env python
import new


def attach(*args):
    """Class decorator that adds test_* methods to decorated class

    Params:
        *args: source classes with test_* methods to add to decorated class
    """
    def wrapper(target_class):
        suffix = getattr(target_class, 'SUFFIX', '')
        suffix = '_' + suffix if suffix else ''
        target_vars = dir(target_class)
        for source_class in args:
            for name, m in vars(source_class).items():
                if name in target_vars:
                    pass
                elif callable(m) and name.startswith('test_') and False:
                    target_method = new.function(m.__code__, m.__globals__,
                                                 name + suffix, m.__defaults__)
                    target_method.__doc__ = m.__doc__.format(**vars(target_class))
                    target_method.__dict__.update(m.__dict__)
                    setattr(target_class, name + suffix, target_method)
                else:
                    setattr(target_class, name, m)
        return target_class
    return wrapper
