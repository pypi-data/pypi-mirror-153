"""
geometry.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import logging
import numpy as np
from scipy.spatial.distance import squareform

# Get the molecular.geometry logger
logger = logging.getLogger('molecular.geometry')


# Compute angle between three points
# TODO introduce signed angles
def angle(a, b, c=None, method='atan2', degrees=False):
    r"""
    Compute the angle between two vectors or three vertices.

    If method = 'atan2',

    ..math :: \theta = atan2(norm(cross(a, b)), dot(a, b))

    If method = 'acos',

    ..math :: \theta = acos \frac{a \dot b}{|a| |b|}


    Parameters
    ----------
    a, b, c : ArrayLike
        Vectors with same dimensionality. Both `a` and `b` must be provided. If `c` is provided, all three are taken as
        vertices. Otherwise, `a` and `b` are assumed to be Euclidean vectors.
    method : str
        Method to compute angle, see :func:`~vangle` for options.
    degrees : bool
        Should the output be in degrees? (Default: False)

    Returns
    -------
    float or numpy.ndarray
        Angle between vectors
    """

    # If c is provided, compute Euclidean vectors
    # noinspection DuplicatedCode
    if c is not None:
        a = vector(a, b)
        b = vector(c, b)

    # Vectors must have at least 2 dimensions
    n_dim = _get_dimensions(a, b)
    if np.min(n_dim) < 2:
        raise AttributeError('angles can only be computed with 2D or 3D vectors (n_dim = %s)' % n_dim)

    # Coerce to a 2D form
    a, b, needs_ravel = _coerce_to_2d(a, b)

    # Format the method
    method = str(method).lower()

    # Compute the angle
    if method == 'atan2':
        cross_ = cross(a, b)
        if _has_dimensions(a, b, n_dim=2):
            if a.ndim == 2 and b.ndim == 2:
                cross_ = cross_.reshape(-1, 1)
            else:
                cross_ = [cross_]
        result = np.arctan2(norm(cross_), dot(a, b))

    elif method == 'acos':
        result = np.arccos(cos_angle(a, b))

    else:
        raise AttributeError('method %s unknown' % method)

    # Convert from radians to degrees?
    if degrees:
        result = np.rad2deg(result)

    # Return
    return _array_result(result, needs_ravel)


# Compute the gradient of an angle
# noinspection DuplicatedCode
def angle_gradient(a, b, c=None):
    """
    Gradient of angle with respect to vertices.

    Parameters
    ----------
    a, b, c : ArrayLike
        Cartesian coordinates.

    Returns
    -------
    """

    # If c is provided, compute Euclidean vectors
    if c is not None:
        a = vector(a, b)
        b = vector(c, b)

    # Vectors must have at least 2 dimensions
    n_dim = _get_dimensions(a, b)
    if np.min(n_dim) < 2:
        raise AttributeError('angles can only be computed with 2D or 3D vectors (n_dim = %s)' % n_dim)

    # Coerce to a 2D form
    a, b, needs_ravel = _coerce_to_2d(a, b)

    # Compute angle and factors
    cos_theta = cos_angle(a, b).reshape(-1, 1)
    inv_sin_theta = (1. / np.sqrt(1. - cos_theta * cos_theta)).reshape(-1, 1)
    inv_a_norm = (1. / norm(a)).reshape(-1, 1)
    inv_b_norm = (1. / norm(b)).reshape(-1, 1)
    a_unit = a * inv_a_norm
    b_unit = b * inv_b_norm

    # Compute gradients (here, gradient_a, gradient_b, and gradient_c stand for vertices)
    gradient_a = inv_sin_theta * inv_a_norm * (a_unit * cos_theta - a_unit)
    gradient_c = inv_sin_theta * inv_b_norm * (b_unit * cos_theta - b_unit)
    gradient_b = -1. * (gradient_a + gradient_c)

    # Return
    return np.array([
        _array_result(gradient_a, needs_ravel),
        _array_result(gradient_b, needs_ravel),
        _array_result(gradient_c, needs_ravel)
    ])


# Convert Cartesian to polar coordinates
def cartesian_to_polar(a):
    """
    Convert Cartesian to polar coordinates.

    Parameters
    ----------
    a : ArrayLike
        Cartesian coordinates.

    Returns
    -------
    numpy.ndarray
        Polar coordinates in same shape as `a`
    """

    # Coerce input
    a, needs_ravel = _coerce_to_2d(a)

    n_dim = a.shape[1]
    if n_dim in (2, 3):
        r = norm(a)
        result = [r, np.arctan2(a[:, 1], a[:, 0])]
        if n_dim == 3:
            result.append(np.arccos(a[:, 2] / r))

    else:
        raise AttributeError('cannot compute for %s dimensions' % n_dim)

    return _array_result(np.array(result).T, needs_ravel)


def condensed_to_square(a):
    return squareform(a)


# Compute angle between three points
def cos_angle(a, b, c=None):
    r"""
    Compute cosine of the angle between three points :math:`\angle ABC`.

    Parameters
    ----------
    a, b, c : ArrayLike
        Vectors

    Returns
    -------
    float or numpy.ndarray
        Cosine angle of points
    """

    if c is not None:
        a, b = vector(a, b), vector(c, b)

    # Coerce
    a, b, needs_ravel = _coerce_to_2d(a, b)

    # Return
    # TODO should cos_angle=np.clip(dot_prod/(len1*len2),-1.,1.)
    return _array_result(dot(a, b) / (norm(a) * norm(b)), needs_ravel)


# Cross product
def cross(a, b):
    """
    Compute cross product between vectors `a` and `b`. Points to :func:`numpy.cross`

    Parameters
    ----------
    a, b : ArrayLike
        Vectors

    Returns
    -------
    float or numpy.ndarray
        Cross product of u and v
    """

    return np.cross(a, b)


# Dihedral angle between 4 points
def dihedral(a, b, c, d=None):
    """
    Compute dihedral angle between four points.

    TODO add equation for sanity checking

    Parameters
    ----------
    a, b, c, d : ArrayLike
        Cartesian coordinates. If only `a`, `b`, and `c` are supplied, they are taken as vectors. If `d` is included,
        they are taken as vertices.

    Returns
    -------
    float or numpy.ndarray
        Dihedral angle
    """

    if d is not None:
        a, b, c = vector(b, a), vector(c, b), vector(d, c)

    _check_dimensions(a, b, c, n_dim=3)

    u = cross(a, b)
    v = cross(b, c)

    return angle(u, v, method='acos')


def vecadd(a, b):
    """
    Add two vectors together
    
    Parameters
    ----------
    a : array
    b : array

    Returns
    -------
    numpy.ndarray
    """

    logger.info('adding vectors')

    return a + b


# Compute the distance between two vectors
# naming inspired by VMD
def vecdist(a, b=None):
    """
    Compute the Euclidean distance between two vectors.

    Parameters
    ----------
    a : ArrayLike
        Vector
    b : ArrayLike
        (Optional) Vector. If None, `b` is set to 0 and the distance to the origin is computed.

    Returns
    -------
    float
        Distance
    """

    # Coerce
    a, needs_ravel = _coerce_to_2d(a)

    # If y is not supplied, set to zeros; then coerce
    if b is None:
        b = np.zeros(a.shape)
    b, _ = _coerce_to_2d(b)

    logger.info('computed vector distance')

    # Return distance
    return _array_result(np.sqrt(np.sum(np.square(vector(a, b)), axis=1)), needs_ravel)


def vecsub(a, b):
    """
    Add two vectors together

    Parameters
    ----------
    a : array
    b : array

    Returns
    -------
    numpy.ndarray
    """

    logger.info('subtracting vectors')

    return a - b


# Dot product
def dot(a, b, axis=1):
    """
    Compute vector dot product.

    Parameters
    ----------
    a, b : ArrayLike
        Vectors
    axis : int
        Axis to apply sum over.

    Returns
    -------
    float or numpy.ndarray
        Vector dot product
    """

    a, b, needs_ravel = _coerce_to_2d(a, b)

    return _array_result(np.sum(np.multiply(a, b), axis=axis), needs_ravel)


# Normed vector
def norm(a):
    r"""
    Compute vector norm.

    .. math :: |a| = \sqrt{a_x^2 + a_y^2 + a_z^2}

    Parameters
    ----------
    a : ArrayLike
        Vector

    Returns
    -------
    float or numpy.ndarray
        Normed vector
    """

    # a, needs_ravel = _coerce_to_2d(a)
    #
    # return _array_result(np.linalg.norm(a, axis=1), needs_ravel)
    return vecdist(a)


# Compute the normal between three points
# FIXME is this confusing? normal = cross
def normal(a, b, c=None):
    """
    Compute normal vector between three points.

    Parameters
    ----------
    a, b, c : ArrayLike
        Cartesian coordinates.

    Returns
    -------
    numpy.ndarray
        Vector normal
    """

    if c is not None:
        a, b = vector(a, b), vector(c, b)

    return cross(a, b)


# Polar to cartesian coordinates
def polar_to_cartesian(a):
    """
    Convert polar to Cartesian coordinates.

    Parameters
    ----------
    a : ArrayLike
        Polar coordinates

    Returns
    -------
    float or numpy.ndarray
        Cartesian coordinates, same shape as `a`
    """

    #
    # a = np.array(a).reshape(-1)

    # Coerce
    a, needs_ravel = _coerce_to_2d(a)
    # if b is not None:
    #     b = np.array(b).reshape(-1)
    #     b, _ = _coerce_to_2d(b)
    #     a = np.hstack([a, b])

    n_dim = a.shape[1]
    if n_dim in (2, 3):
        result = np.array([np.cos(a[:, 1]), np.sin(a[:, 1])])
        if n_dim == 3:
            result *= np.sin(a[:, 2])
            result = np.vstack([result, np.cos(a[:, 2])])
        result *= a[:, 0]

    else:
        raise AttributeError('cannot compute for %s dimensions' % n_dim)

    return _array_result(np.array(result).T, needs_ravel)


# Create unit vector
def unit_vector(a):
    r"""
    Compute unit vector.

    .. math :: \^{a} = \frac{a}{|a|}

    Parameters
    ----------
    a : ArrayLike
        Vector

    Returns
    -------
    numpy.ndarray
        Unit vector
    """

    a, needs_ravel = _coerce_to_2d(a)
    return _array_result(a / norm(a).reshape(-1, 1), needs_ravel)


#
def vangle_gradient(u, v):
    """

    Parameters
    ----------
    u
    v

    Returns
    -------

    """

    cos_theta = cos_angle(u, v)
    inv_sin_theta = 1. / np.sqrt(1. - cos_theta * cos_theta)
    inv_u_norm = 1. / norm(u)
    inv_v_norm = 1. / norm(v)
    u_unit = u * inv_u_norm
    v_unit = v * inv_v_norm

    gradient_a = inv_sin_theta * inv_u_norm * (u_unit * cos_theta - v_unit)
    gradient_c = inv_sin_theta * inv_v_norm * (v_unit * cos_theta - u_unit)
    gradient_b = -1. * (gradient_a + gradient_c)

    print(gradient_a)


# Compute vector between 2 sets of points
def vector(a, b, normed=False):
    """
    Compute vector between two sets of points.

    .. math:: vector = a - b

    Parameters
    ----------
    a, b : ArrayLike
        Cartesian coordinates.
    normed : bool
        Should the unit vector be computed? (Default: False)

    Returns
    -------
    numpy.ndarray
        Vector between `a` and `b`.
    """

    # Coerce input
    a, b, needs_ravel = _coerce_to_2d(a, b)

    v = np.subtract(a, b)
    if normed:
        v /= norm(v).reshape(-1, 1)

    return _array_result(v, needs_ravel)


# Helper function to ravel array result
def _array_result(a, needs_ravel=False):
    if needs_ravel:
        if a.ndim > 1:
            a = a.ravel()
        else:
            a = a[0]
    return a


def _check_dimensions(*args, n_dim=3):
    if not _has_dimensions(*args, n_dim=n_dim):
        raise AttributeError('must be %sD' % n_dim)


def _coerce_to_2d(a, *args):
    # Coerce a to 2d
    a = np.array(a)
    needs_ravel = False
    if a.ndim == 1:
        needs_ravel = True
        a = a.reshape(1, -1)
    result = [a]

    # Do the same for kwargs
    for arg in args:
        b, _ = _coerce_to_2d(arg)
        if a.shape != b.shape:
            raise AttributeError('vectors must be same shapes')
        result.append(b)

    # Add in needs_ravel flag
    result.append(needs_ravel)

    # Return
    return result


def _get_dimensions(*args, n_dim=3):
    result = []
    for arg in args:
        arg = np.array(arg)
        n_dim = 1
        if arg.ndim > 1:
            n_dim = arg.shape[1]
        elif arg.ndim == 1:
            n_dim = arg.shape[0]
        result.append(n_dim)
    return result


# Helper function to check dimensionality
def _has_dimensions(*args, n_dim=3):
    result = []
    for arg in args:
        arg = np.array(arg)
        result.append((arg.ndim > 1 and arg.shape[1] == n_dim) or (arg.ndim == 1 and arg.shape[0] == n_dim))
    return all(result)


if __name__ == '__main__':
    import numpy as np
    a = np.random.rand(100, 3)
    b = np.random.rand(100, 3)
    vecadd(a, b)
    vecsub(a, b)
    vecdist(a, b)