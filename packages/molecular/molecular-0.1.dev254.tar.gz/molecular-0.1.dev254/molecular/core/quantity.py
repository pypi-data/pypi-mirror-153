"""
quantity.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from abc import ABCMeta
import numpy as np
import pandas as pd


class Ensemble(metaclass=ABCMeta):
    def __init__(self):
        pass


# noinspection PyPep8Naming
class NPT(Ensemble):
    def __init__(self, N, P, T):
        self.N = N
        self.P = P
        self.T = T
        Ensemble.__init__(self)


# noinspection PyPep8Naming
class NVT(Ensemble):
    def __init__(self, N, V, T):
        self.N = N
        self.V = V
        self.T = T
        Ensemble.__init__(self)


# TODO a Quantity can have an energy attached to it? That would make this a reaction coordinate. Maybe a RC is child?
# TODO a Quantity is a dependent of an Ensemble?
class Quantity:
    """
    A `Quantity` is something that has measures something (along the wide axis) versus observations (along the long
    axis).

    Because this is a proof of concept, `Quantity` is limited to two-dimensions. Higher-dimensional structures can still
    be considered as a flattened list. For instance, if you wanted to look at secondary structure per residue per
    observation, you would have to construct your wide axis as, "residue0_H, residue0_T, residue0_C, ..."

    The benefit of a `Quantity` is that it can be block-averaged, used in WHAM ...

    Examples
    --------
    1. Energy vs observations
    2. Number of residues in helical state vs observations
    3. Flag if each residue is helix vs observations
    """

    # Initialize instance of Quantity class
    def __init__(self, data, ensemble=None):
        """

        Parameters
        ----------
        data
        """

        self._data = data
        self._ensemble = ensemble

    # The length of the Quantity is equal to the number of observations
    def __len__(self):
        """
        Number of observations for the Quantity instance.

        Returns
        -------
        int
            Number of observations
        """

        # Return number of observations
        return len(self._data)

    # Represent Quantity by self._data
    def __repr__(self):
        return pd.DataFrame.__repr__(self._data)

    # Assign blocks
    def _assign_blocks(self, num_blocks, block_size):
        """

        Parameters
        ----------
        num_blocks
        block_size

        Returns
        -------

        """

        # Observations
        num_observations = len(self)
        observations = np.arange(num_observations)

        # If block_size is set, set number of blocks by dividing number of observations by block size
        if block_size is not None:
            num_blocks = np.floor(num_observations / block_size)

        # Else if num_blocks is None, set to square root of num_observations
        elif num_blocks is None:
            num_blocks = np.floor(np.sqrt(num_observations))

        # If num_observations <= num_blocks, do not move forward
        if num_observations <= num_blocks:
            raise AttributeError('num_observations cannot be <= num_blocks')

        # Create bins
        bins = np.floor(np.linspace(start=observations[0], stop=observations[-1], num=num_blocks + 1))
        bins[-1] = np.inf

        # Return blocks
        return np.digitize(observations, bins=bins, right=False) - 1

    # Compute block averages
    def block_averages(self, num_blocks=None, block_size=None, blocks=None):
        # Determine blocks
        if blocks is None:
            blocks = self._assign_blocks(num_blocks, block_size)

        # Assign block
        self._data['block'] = blocks

        # For every block, compute the average
        return self._data.astype(float).pivot_table(index='block', values=self.columns, aggfunc='mean')

    # Compute the block error
    def block_error(self, num_blocks=10, block_size=None, blocks=None):
        # Determine blocks
        if blocks is None:
            blocks = self._determine_blocks(num_blocks, block_size)
        num_blocks = len(blocks)

        # Compute block averages
        block_averages = self.block_average(num_blocks=num_blocks, block_size=block_size)

        # Compute block average of the squared quantity
        quantity_squared = Quantity(np.square(self._data))
        block_averages_squared = quantity_squared.block_average(num_blocks=num_blocks, block_size=block_size)

        # Compute the standard error
        return np.sqrt((block_averages_squared - np.square(block_averages)) / (num_blocks - 1))

    # Columns of Quantity
    @property
    def columns(self):
        return self._data.columns

    # TODO should there be an axis = None here?
    def mean(self, axis=1):
        """

        Parameters
        ----------
        axis

        Returns
        -------

        """

        return self._data.mean(axis=axis)

    def std(self, axis=None):
        pass

    def sum(self, axis=None):
        pass
