
from .misc import *

# import molecular.flags as flags
import functools
import warnings
from scipy.spatial.distance import squareform

__all__ = [
    'cartesian_product',
    'deprecated',
    'dictmap',
    'experimental',
    'squareform',
    'zfill',
    'zfillr'
]


# Decorator to indicate if deprecated
# noinspection PyDeprecation
def deprecated(function=None):
    @functools.wraps(function)
    def execute_function(*args, **kwargs):
        warnings.warn('will be deprecated', DeprecationWarning)
        return function(*args, **kwargs)

    return execute_function


# Decorator to indicate if still in development
# TODO this should probably be moved out of __init__
# def experimental(f=None):
#     # Wrapper to run function
#     def execute_function(f):
#         @functools.wraps(f)
#         def wrapper(*args, **kwargs):
#             use_experimental = flags.use_experimental
#             # if 'use_experimental' in kwargs:
#             #     use_experimental = kwargs['use_experimental']
#             #     del kwargs['use_experimental']
#
#             # If false, then we cannot use this function
#             if not use_experimental:
#                 raise PermissionError('cannot use function because it is experimental')
#
#             return f(*args, **kwargs)
#         return wrapper
#
#     if f is None:
#         return execute_function
#     else:
#         return execute_function(f)

# Class to provide experimental warning
class ExperimentalWarning(UserWarning):
    pass


# Decorator to indicate if experimental
def experimental(obj=None):
    """
    Decorator to indicate that a class or function is experimental.

    Parameters
    ----------
    obj : None, class, or function

    Returns
    -------
    obj executed
    """

    @functools.wraps(obj)
    def execute(*args, **kwargs):
        warnings.warn('%s is experimental and is not validated' % obj.__name__, ExperimentalWarning)
        return obj(*args, **kwargs)

    return execute


if __name__ == '__main__':
    @experimental
    def test(x):
        print(x)


    test(5)
