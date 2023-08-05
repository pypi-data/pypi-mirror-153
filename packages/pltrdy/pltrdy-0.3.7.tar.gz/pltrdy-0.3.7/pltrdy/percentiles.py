import numpy as np


def percentiles(data, n):
    """Return all (n-1) values of n-ciles over the data
       i.e. if n=10, it returns deciles therefore 9 values.
       i.e. percentiles(data, n)[int((n/2)-1)] = median(percentiles)

    """
    prct = 100 / n
    cur = prct
    q = []
    while cur < 100:
        q.append(cur)
        cur += prct

    p = list(np.percentile(data, q))
    assert len(p) == (n - 1)
    return p


def deciles(data):
    return percentiles(data, n=10)


def quartiles(data):
    return percentiles(data, n=4)
