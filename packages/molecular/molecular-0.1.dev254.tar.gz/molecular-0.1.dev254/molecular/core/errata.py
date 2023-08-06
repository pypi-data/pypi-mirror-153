"""
errata.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import pandas as pd
from privatize import privatize
import numpy as np


class ReservedDataFrame:
    def __init__(self, data, columns=None):
        self._data = pd.DataFrame(data, columns=columns)


# TODO since this also appears in `izzy`, assess if this should be modularized
# Extended pandas pivot tables
def pivot(df, index=None, columns=None, values=None, aggfunc=None):
    # First of, convert aggfunc to lowercase if it is a string
    if isinstance(aggfunc, str):
        aggfunc = aggfunc.lower()

    # TODO define this with Cython or C
    # Define new aggfunc
    if aggfunc == 'range':
        def _range(x):
            return np.max(x) - np.min(x)
        aggfunc = _range

    # Return call to pandas pivot_table function
    return df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)
