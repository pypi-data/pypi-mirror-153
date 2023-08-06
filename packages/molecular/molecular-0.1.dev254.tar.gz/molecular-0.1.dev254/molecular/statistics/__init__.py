
from .block import *
from .time_series import *

__all__ = [
    'acorr',
    'acov',
    'Block',
    'block_average',
    'block_error',
    'normalize',
    'sem_block',
    'sem_tcorr',
    'standardize',
    'tcorr',
]


# TODO find me a home
import numpy as np
import pandas as pd
def normalize(a):
    if isinstance(a, (pd.DataFrame, pd.Series)):
        a = a.div(a.abs().sum(axis=0), axis=1)  # noqa

    elif isinstance(a, (list, np.ndarray)):
        a = a / np.sum(np.abs(a))

    else:
        assert AttributeError('cannot normalize')

    return a


def standardize(a):
    raise NotImplementedError