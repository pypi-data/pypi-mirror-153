from itertools import tee


try:
    from itertools import zip_longest
except Exception:
    from itertools import izip_longest as zip_longest


def pairwise(iterable, longest=False):
    a, b = tee(iterable, 2)
    next(b, None)
    if longest:
        return zip_longest(a, b)
    else:
        return zip(a, b)


def triplewise(iterable, longest=False):
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    if longest:
        return zip_longest(a, b, c)
    else:
        return zip(a, b, c)
