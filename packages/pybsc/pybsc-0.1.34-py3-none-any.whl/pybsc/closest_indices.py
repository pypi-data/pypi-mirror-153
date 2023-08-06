from numbers import Number

import numpy as np


def _find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def argclosest(array, values):
    if isinstance(values, Number):
        return _find_nearest(array, values)

    # https://stackoverflow.com/questions/2566412/
    # find-nearest-value-in-numpy-array
    array = np.array(array)

    # get insert positions
    idxs = np.searchsorted(array, values, side="left")

    # find indexes where previous index is closer
    prev_idx_is_less = (
        (idxs == len(array))
        | (np.fabs(values - array[np.maximum(idxs - 1, 0)])
           < np.fabs(values - array[np.minimum(idxs, len(array) - 1)])))
    idxs[prev_idx_is_less] -= 1
    return idxs
