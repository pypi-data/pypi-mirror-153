def _is_sorted_numpy(x):
    import numpy as np
    return np.all(np.diff(x) >= 0)


def _is_sorted(x):
    return sorted(x) == x


def is_sorted(x):
    if isinstance(x, list) or isinstance(x, tuple):
        return _is_sorted(x)
    elif x.__class__.__name__ == 'ndarray':
        return _is_sorted_numpy(x)
    else:
        raise NotImplementedError
