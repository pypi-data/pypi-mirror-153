import numpy as np

from pybsc.closest_indices import argclosest


def get_timestamp_indices_wrt_base(base_timestamps, target_timestamps,
                                   style='after'):
    """Return timestamp indices with respect to base timestamps.

    Examples
    --------
    >>> base_timestamps = np.array([0., 1., 2., 3., 4., 5.])
    >>> target_timestamps = np.array([0.21, 0.43, 1.4, 3.1])
    >>> get_timestamp_indices_wrt_base(base_timestamps, target_timestamps)
    array([0, 0, 1, 3])
    """
    if style == 'after':
        return np.maximum(
            np.searchsorted(base_timestamps,
                            target_timestamps, side="left") - 1, 0)
    elif style == 'closest':
        return argclosest(base_timestamps, target_timestamps)
    else:
        raise NotImplementedError


def sorted_timestamps(timestamps):
    """Returns a timestamp that is sorted and whose time starts at 0 seconds.

    Examples
    --------
    >>> timestamps = np.array([5, 3, 2, 1])
    >>> sorted_timestamps(timestamps)
    array([0, 1, 2, 4])
    """
    np_stamps = np.array(timestamps, dtype=np.float64)
    np_stamps = np.sort(np_stamps)
    np_stamps = np_stamps - np_stamps[0]
    return np_stamps
