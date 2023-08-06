"""
go.py
written in Python3
Author: C. Lockhart <chris@lockhartlab.org>

>>> go = Go(10)
>>> go.add_particle()
"""

from molecular.misc import experimental

import numpy as np


@experimental
class Go:
    """


    """

    # Initialize class instance
    def __init__(self, board, mask):
        """

        Parameters
        ----------
        shape : int, tuple with 2 elements, or numpy.ndarray
            The size of the Go board
        """

        # Shape is coerced into a 2D boolean array; True marks valid locations; False are invalid
        if isinstance(board, int):
            shape = np.ones((board, board), dtype='bool')

        else:
            raise AttributeError('board type (%s) not understood' % type(board))

        self.board = board
        self.shape = self.board.shape
        self.board = np.zeros(self.shape.shape, dtype=object)  # is this the most efficient way to do this?

    def _iterate(self):
        pass

    def _random_position(self):
        shape = self.shape.shape

    def add_stone(self, stone, position=None):
        """

        Parameters
        ----------
        stone
        position

        Returns
        -------

        """

        # If position is None, place randomly
        if position is None:
            position = self._random_position()

        # Make sure position is not unavailable
        if not self.mask[position]:
            raise AttributeError('cannot place stone in this position')

        # Make sure position is not occupied
        #

        # Put the Stone in the position
        self.board[position] = stone


class Stone:
    """
    In the game of Go, the bead things are called stones. Hence, `Stone`.
    """

    def __init__(self):
        pass
