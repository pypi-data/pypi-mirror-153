import numpy as np
import pandas as pd
from typelike import ArrayLike


# Assert that an array is incremental
def assert_incremental(a, increment=1):
    """
    Assert that something like an array has entries that increment by a specific value.

    Parameters
    ----------
    a : ArrayLike
        Array to check if entries increment by specific value.
    increment : int
        Increment value.

    Raises
    ------
    AssertionError
        If `a` does not have entries that increment by `increment`
    """

    assert is_incremental(a, increment=increment)


# Test if an array is incremental
def is_incremental(a, increment=1):
    return (np.diff(a) == increment).all()


# Cartesian product generator
def cartesian_product(a, offset=1):
    """
    Return the Cartesian product of `a` as a generator. However, only unique pairs will be returned. If
    :math:`n = len(a)`, then in total :math:`n(n-1)/2` elements will be returned in the generator.

    Parameters
    ----------
    a : array-like
    offset : int

    Returns
    -------
    Cartesian product
        generator
    """

    for i in range(len(a)):
        for j in range(i + offset, len(a)):
            yield a[i], a[j]


# Map, which supports dictionary mapping
def dictmap(dictionary, iterable):  # noqa
    """
    Create our own map function that allows mapping to a dictionary. This is only marginally faster than doing a
    list comprehension.

    Parameters
    ----------
    func : function or dict or pandas.Series
    iterable : iterable

    Returns
    -------
    numpy.ndarray
    """

    if isinstance(dictionary, dict):
        dictionary = pd.Series(dictionary)

    elif not isinstance(dictionary, pd.Series):
        raise AttributeError('must be dict or Series')

    if isinstance(iterable, pd.Series):
        iterable = iterable.to_numpy()

    return dictionary[iterable].to_numpy()


# Convenience zfill function
def zfill(a, width=None):
    if width is None:
        return a
    elif hasattr(a, '__getitem__'):
        return np.char.zfill(list(map(str, a)), width)
    else:
        return str(a).zfill(width)


# Convenience zfill range function
def zfillr(n, width=None):
    return zfill(range(n), width)


if __name__ == '__main__':
    print(zfill(range(5), 2))
