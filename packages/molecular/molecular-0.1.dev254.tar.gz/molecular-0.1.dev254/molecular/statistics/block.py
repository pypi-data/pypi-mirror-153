"""
block.py

author: C. Lockhart <chris@lockhartlab.org>
language: Python3
"""

import numpy as np
import pandas as pd
from warnings import warn


class Block:
    """

    """

    def __init__(self, data, n_blocks=10, discard_remainder=True):
        """

        Parameters
        ----------
        data
        n_blocks
        discard_remainder : bool
            If the length of data is not evenly divisible by `n_blocks`, then should we include or discard the
            remainder? If we choose not to discard the remainder, the last block will be larger. (Default: True).
        """

        # Make sure data is DataFrame
        if not isinstance(data, pd.DataFrame):
            raise AttributeError('data must be pandas DataFrame')

        # Create a copy of the DataFrame
        data = data.copy()

        # Split into blocks
        if 'block' in data.columns:
            raise AttributeError('block cannot be in pandas.DataFrame')
        # block_size = len(data) / n_blocks  # should this be ceiled?
        # data['block'] = (np.arange(len(data)) / block_size).astype(int)

        block_size = np.floor(len(data) / n_blocks)
        blocks = np.repeat(np.arange(n_blocks), block_size)
        last_block = np.nan if discard_remainder else n_blocks - 1
        data['block'] = np.hstack([blocks, np.repeat(last_block, len(data) - len(blocks))])

        # Make sure that we computed the right number of blocks
        if n_blocks != data['block'].nunique():
            raise ValueError('computed wrong number of blocks')

        # Save data
        self._data = data

    @property
    def data(self):
        return self._data

    # def __getattr__(self, item, *args, **kwargs):
    #     result = getattr(self._data, item, None)
    #     if result is not None:
    #         if callable(result):
    #             result = result(*args, **kwargs)
    #         if result is not None:
    #             return result

    def count(self):
        return self._data.pivot_table(index='block', aggfunc='count')

    def mean(self):
        return self._data.pivot_table(index='block', aggfunc='mean')

    def sem(self):
        # Compute standard error around mean
        return block_error(self.mean())

    def std(self):
        return self._data.pivot_table(index='block', aggfunc='std')  # same as aggfunc=partial(np.std, ddof=1)


def block_average(df, n_blocks=10):
    return Block(df, n_blocks=n_blocks).mean()


# Shortcut function to compute block error directly from a DataFrame
def block_error(df, n_blocks=10):
    # Convert Series to DataFrame if necessary
    if isinstance(df, pd.Series):
        df = df.to_frame()

    # If block is in the DataFrame, assume we're passed block averages
    if 'block' in df.columns:
        _, counts = np.unique(df['block'], return_counts=True)
        if np.max(counts) != 1:
            raise AttributeError('cannot parse DataFrame blocks')

    # Otherwise, produce the block averages
    else:
        df = Block(df, n_blocks=n_blocks).mean()

    # Return the block error
    # TODO make this return a single number of len(df.columns) == 1
    return df.std(ddof=1) / np.sqrt(len(df))


def block_std(df, n_blocks=10):
    return Block(df, n_blocks=n_blocks).mean().std(ddof=1)


# noinspection PyShadowingNames
def sem_block(a, indices_or_sections=10, errors='ignore'):
    r"""
    Compute the block error around the mean for a 1 or 2D array. If 2D array, the second dimension is taken as a
    collection of independent measurements.

    An array :math:`a` is divided into :math:`N` blocks such that :math:`a = \{a_1, a_2, ..., a_N\}`. For any subset
    :math:`a_i`, we can compute the average over all samples :math:`j = 1 ... M_i`,

    .. math:: \overline{a_i} = \frac{1}{N}\sum_{j=1}^{M_i}a_i(j)

    This leaves us with a set of block estimators :math:`a_{block} = \{\overline{a_1}, \overline{a_2}, ...,
    \overline{a_N}\}`. We can therefore compute the average of all blocks and the sample standard deviation,

    .. math:: \overline{a_{block}} = \frac{1}{N}\sum_{i=1}^{N}\overline{a_i}

    .. math:: s = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(\overline{a_i}-\overline{a_{block}})^2}

    Finally, we compute the standard error,

    .. math:: Standard\ error = \frac{s}{\sqrt{N}}

    Note that the sample standard deviation is computed instead of the population standard deviation, assuming that
    :math:`N` is small.


    Parameters
    ----------
    a : numpy.ndarray
        One or two-dimensional array. First dimension is taken as independent samples. If there is a second dimension
        present, these correspond to independent measurements.
    indices_or_sections : int or list of lists
        Number of blocks or samples indices to divide into blocks.
    errors : str
        Should we `warn`, `raise`, or do nothing if the number of samples is indivisible by the number of proposed
        blocks?

    Returns
    -------
    float or numpy.ndarray
        If `a` is one-dimensional, a float will be returned that is the standard error. If two-dimensional, the result
        will be an array of standard errors, one for each independent measurement.

    References
    ----------
    [1] Flyvbjerg, H. & Petersen, H. G. (1989) Error estimates on averages of correlated data. *J. Chem. Phys.* **91**,
    461.

    [2] Frankel and Smit
      
    [3] Grossfield, A., & Zuckerman, D. M. (2009) Quantifying uncertainty and sampling quality in biomolecular
    simulations. *Annu. Rep.Comput. Chem.* **5**, 23-48.
    """

    # Number of dimensions must be 1 or 2
    if a.ndim not in [1, 2]:
        raise AttributeError('only 1 or 2 dimensional arrays allowed')

    # Warn, raise, or ignore if n_samples not evenly divisible by number of sections
    n_samples = a.shape[0]
    if isinstance(indices_or_sections, int) and np.mod(n_samples, indices_or_sections) != 0:
        message = f'{n_samples} not divisible by {indices_or_sections}'
        errors = str(errors).lower()
        if errors == 'warn':
            warn(message)
        elif errors == 'raise':
            raise AttributeError(message)
        elif errors != 'ignore':
            raise AttributeError(f'errors={errors} not understood')

    # Split
    blocks = np.array_split(a, indices_or_sections, axis=0)

    # Block averages
    blocks_avg = np.array([block.mean(axis=0) for block in blocks])

    # Compute error around average
    return np.std(blocks_avg, ddof=1, axis=0) / np.sqrt(len(blocks))

def _sem_block(a):
    return np.std(a, ddof=1) / np.sqrt(len(a))

# if __name__ == '__main__':
#     # 1D, equal
#     a = np.random.rand(10000)
#     print(sem_block(a, 10))
#
#     # 1D, unequal
#     a = np.random.rand(10000)
#     print(block_error(a, 3))
#
#     # 2D, equal
#     a = np.random.rand(10000, 31)
#     print(block_error(a))
#
#     # 2D, unequal
#     a = np.random.rand(10000, 31)
#     print(block_error(a, 3))
