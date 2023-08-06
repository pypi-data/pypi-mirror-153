
from molecular.geometry import cos_angle
from molecular.misc import experimental
import numpy as np


# Order parameter
@experimental
def ordparam(a, b):
    """
    Compute the order parameter between two sets of vectors.

    Parameters
    ----------


    Returns
    -------

    """

    # Wrangle a and b into 3D matrices (# str by #
    a, b = _handle_a_b(a, b, paired=True)


    return 1.5 * cos_angle(a, b) ** 2. - 0.5



def _handle_a_b(a, b=None, paired=False):
    # Make sure we have numpy array
    a = np.array(a)

    # If 1D, convert to 3D
    if a.ndim == 1:
        # noinspection PyArgumentList
        a = a.reshape(1, 1, -1)

    # If 2D convert to 3D
    if a.ndim == 2:
        a = a.reshape(1, *a.shape)

    # Handle b if necessary
    if b is not None:
        # noinspection PyNoneFunctionAssignment
        b = _handle_a_b(b)
        if paired and a.shape != b.shape:
            raise AttributeError('must be same number of parameters')
        a = (a, b)

    return a
