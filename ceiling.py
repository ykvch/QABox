class Ceiling(list):
    '''
    List-like returning last value for any index above its size

    Example:
    >>> x = Backoff([1,3,2])
    >>> x[0:5]
    [1, 3, 2, 2, 2]
    '''

    def __getitem__(self, item):
        gi = super().__getitem__
        if isinstance(item, slice):
            start = max(item.start or 0, len(self))
            stop = item.stop or 0
            return gi(item) + [gi(-1)] * ((stop - start) // (item.step or 1))
        return gi(min(item, len(self) - 1))
