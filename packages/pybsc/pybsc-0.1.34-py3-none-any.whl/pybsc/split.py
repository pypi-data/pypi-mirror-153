from __future__ import division


def nsplit(xlst, n):
    """Split input list into n.

    Parameters
    ----------
    xlst : list[object]
        input list
    n : int
       number of divide.

    Returns
    -------
    ret : list[list[object]]
        n list.

    Examples
    --------
    >>> from pybsc import nsplit
    >>> nsplit([1, 2, 3], 3)
    [[1], [2], [3]]
    >>> nsplit([1, 2, 3], 2)
    [[1, 2], [3]]
    """
    total_n = len(xlst)
    d = int((total_n + n - 1) / n)
    i = 0
    ret = []
    while i < total_n:
        ret.append(xlst[i:i + d])
        i += d
    return ret
