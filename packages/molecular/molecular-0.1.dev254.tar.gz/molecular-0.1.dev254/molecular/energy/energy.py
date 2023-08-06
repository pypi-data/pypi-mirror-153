"""
energy.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.geometry import *

from abc import ABCMeta
import numpy as np


# TODO allow computation to work with only distances? Need a way to speed up calculations using REMD

def lennard_jones(epsilon, r_min, r):
    return epsilon * ((r_min / r) ** 12. - 2 * (r_min / r) ** 6.)


# Metaclass that defines structure of each energy term
class EnergyTerm(metaclass=ABCMeta):
    """
    Metaclass that defines structure of each energy term.
    """

    # Initialize class instance
    def __init__(self):
        self._energy = None
        self._force = None

    def _compute_energy(self):
        raise NotImplementedError

    def _compute_force(self):
        raise NotImplementedError

    @property
    def energy(self):
        """
        The computed energy term

        Returns
        -------
        numpy.ndarray
            Energy
        """

        if self._energy is None:
            self._energy = result = self._compute_energy()
        else:
            result = self._energy
        return result

    @property
    def force(self):
        """
        The computed force vector

        Returns
        -------
        numpy.ndarray
            Force vector
        """

        if self._force is None:
            result = self._force = self._compute_force()
        else:
            result = self._force
        return result


# Bond energy term
class Bond(EnergyTerm):
    r"""
    Compute the bond potential energy according to Hooke's law

    The energy :math:`U` can be computed from the difference in the measured distance :math:`r` from the ideal distance
    :math:`r_0`, scaled by the spring constant :math:`k`.

    .. math:: U = \frac{1}{2} k (r - r_0)^2

    Since :math:`r` can be separated out into components :math:`x`, :math:`y`, and :math:`z`, we must compute the
    partial derivatives of :math:`\delta U`. Then, :math:`F = -\delta U / \delta \Delta x`.

    .. math:: F = -\frac{\delta U}{\delta \Delta x} = -k(r-r_0)\frac{\Delta x}{r}

    For the derivation:

    .. math:: \delta U = k(r-r_0) \delta r
    .. math:: r = \sqrt{r^2}
    .. math:: \delta r = \frac{1}{2}(r^2)^{-1/2} \delta r^2
    .. math:: r^2 = (\Delta x)^2 + (\Delta y)^2 + (\Delta z)^2
    .. math:: \frac{\delta r^2}{\delta \Delta x} = 2 \Delta x

    The same for above can be computed for :math:`y` or :math:`z`.

    Examples
    --------
    >>> from molecular import Bond
    >>> bond = Bond(atom1, atom2, idval)
    >>> bond.energy
    >>> bond.derivative
    >>> bond.force
    """

    def __init__(self, a, b, ideal_value=1., force_constant=1.):
        """
        Initialize instance of Bond class.

        Parameters
        ----------
        a, b : ArrayLike
            Cartesian coordinates
        ideal_value : ArrayLike
            The ideal distance between the particles.
        force_constant : ArrayLike
            The spring constant describing the particles.
        """

        # Coerce shapes
        a, b = _coerce_xyz(a, b)

        # Compute
        self._vector = vector(a, b)
        self._distance = distance(a, b)
        self._offset = self._distance - ideal_value

        # Save parameters
        EnergyTerm.__init__(self)
        self._ideal_value = ideal_value
        self._force_constant = force_constant

    def _compute_energy(self):
        return 0.5 * self._force_constant * np.square(self._offset)

    def _compute_force(self):
        return -1. * self._force_constant * self._offset[:, None] * self._vector / self._distance[:, None]


class Angle(EnergyTerm):
    r"""
    Compute the potential energy of an angle.

    The energy of an angle follows the harmonic potential:

    .. math:: U = \frac{1}{2} k (\theta - \theta_0)^2

    The derivative must be split by the components of vectors :math:`u` and :math:`v`, which are used to compute the
    angle :math:`\theta`:

    .. math:: F = -\frac{\delta U}{\delta x} = k (\theta - \theta_0) sin^{-1}(\theta) / |v|



    .. math:: \frac{\delta U}{\delta v_x} = -k (\theta - \theta_0) sin^{-1}(\theta) / |u|

    The derivation:

    .. math:: \frac{\delta U}{\delta \theta} = k (\theta - \theta_0)
    .. math:: \theta = acos(\hat{u_{ij}} \cdot \hat{u_{jk}})
    .. math:: \frac{\delta \theta}{\delta u \cdot v} = \frac{-1}{\sqrt{1 - (\hat{u} \cdot \hat{v})^2}}
                                               = \frac{-1}{\sqrt{1 - cos^2(\theta)}}
                                               = \frac{-1}{\sqrt{sin^2(\theta)}}
                                               = \frac{-1}{sin(\theta)}
                                               = sin^{-1}(\theta)

    .. math:: u_i = [x, y, z]
    .. math:: \frac{\delta u_i}{\delta x} = 1

    .. math:: u \cdot v = u_x v_x + u_y v_y + u_z v_z
    .. math:: \delta (\^{u} \cdot \^{v}) = u \frac{dv}{dx} v \frac{du}{dx}

    .. math:: \delta (\^{u} \cdot \^{v}) = u \frac{dv}{dx} v \frac{du}{dx}
    .. math:: u = [\Delta x, \Delta y, \Delta z]

    f1 = dth/duv / |u| * (u * (cos th / |u|) - v / |v|) = dth/duv / |u| * (u * costh - v)
    f3 = dth/duv / |v| * (v * (cos th / |v|) - u / |u|) = dth/duv / |v| * (v * costh - u)
    f2 = -1 * (f1 + f3)


    .. math:: \frac{\delta u}{\delta \Delta x} = [1, 1, 1]

    .. math:: \frac{\delta (u \cdot v)}{\delta u_x} = v_x
    .. math:: \frac{\delta (u \cdot v)}{\delta v_x} = u_x

    Parameters
    ----------
    xyz0
    xyz1
    xyz2
    ideal_value
    force_constant

    Returns
    -------

    """

    def __init__(self, xyz0, xyz1, xyz2, ideal_value=1., force_constant=1.):
        """
        Parameters
        ----------
        xyz0 : ArrayLike
            Cartesian coordinates for first particle.
        xyz1 : ArrayLike
            Cartesian coordinates for second particle.
        xyz2 : ArrayLike
            Cartesian coordinates for third particle.
        ideal_value : ArrayLike
            The ideal angle between the particles.
        force_constant : ArrayLike
            The spring constant describing the particles.
        """

        # Coerce shapes
        xyz0, xyz1, xyz2 = _coerce_xyz(xyz0, xyz1, xyz2)

        # Compute angle
        self._angle = angle(xyz0, xyz1, xyz2)
        self._offset = self._angle - ideal_value

        # Save parameters
        EnergyTerm.__init__(self)
        self._ideal_value = ideal_value
        self._force_constant = force_constant

    def _compute_energy(self):
        return 0.5 * self._force_constant * np.square(self._offset)

    def _compute_force(self):
        pass


class Dihedral(EnergyTerm):
    pass


# TODO LJ with pairlists
class LennardJones(EnergyTerm):
    r"""

    .. math:: U = 4\epsilon [(\frac{\sigma}{r})^{12} - (\frac{\sigma}{r})^6]
    .. math:: F = -\frac{\delta U}{\delta x} = -24\frac{\epsilon \Delta x}{r}[2(\frac{\sigma}{r})^{12} - (\frac{\sigma}{r})^6]

    .. math:: U = 4\epsilon [z^{12} - z^6]
    .. math:: dU/dx = 4e [12z^{11} - 6z^5] dz
    .. math:: dU/dx = 24e [2z^{11} - z^5] dz
    .. math:: z = s / r = sr^{-1}
    .. math:: dz/dx = -sr^{-2} dr
    .. math:: r = sqrt(delta x + delta y + delta z)
    .. math:: dr/dx = 1/2(r^2)^(-1/2) * d(r^2)
    .. math:: r2 = delta x + delta y + delta z
    .. math:: d(r^2)/dx = delta x


    .. math:: \frac{\delta U}{\delta x} = 4\epsilon [12(\frac{\sigma}{r})^{11} - 6(\frac{\sigma}{r})^5] *
    """

    def __init__(self, xyz0, xyz1, sigma=1., epsilon=-1):
        """
        Parameters
        ----------
        xyz0 : ArrayLike
            Cartesian coordinates for first particle.
        xyz1 : ArrayLike
            Cartesian coordinates for second particle.
        sigma : float
        epsilon : float
        """

        # Coerce shapes
        xyz0, xyz1 = _coerce_xyz(xyz0, xyz1)

        # Compute distance
        self._vector = vector(xyz0, xyz1)
        self._distance = norm(self._vector)
        if self._distance < 1e-7:
            r = 1000.
        else:
            r = sigma / self._distance
        self._r6 = np.power(r, 6)
        self._r12 = np.power(self._r6, 2)

        # Save parameters
        EnergyTerm.__init__(self)
        self._sigma = sigma
        self._epsilon = epsilon

    # TODO save some of these intermediary calculations for force
    def _compute_energy(self):
        return 4. * self._epsilon * (self._r12 - self._r6)

    def _compute_force(self):
        return -24. * self._vector * self._epsilon / self._distance * (2. * self._r12 - self._r6)


class FullElectrostatic(EnergyTerm):
    pass



# Coerce coordinates into an acceptable form
def _coerce_xyz(*args):
    # Place to store results
    results = []

    # Loop over all coordinates in arguments
    shape = None
    for i in range(len(args)):
        # Make sure we're dealing with a 2D array
        xyz = np.array(args[i])
        if xyz.ndim == 1:
            xyz = xyz.reshape(1, -1)

        # Make sure coordinates are the same shape
        if shape is None:
            shape = xyz.shape
        elif shape != xyz.shape:
            raise AttributeError('coordinates must be same shapes')

        # Save coerced coordinates
        results.append(xyz)

    # Return
    return results


class HarmonicOscillator:
    """

    """

    __slots__ = ('_ideal_value', '_force_constant')

    def __init__(self, ideal_value, force_constant):
        self._ideal_value = ideal_value
        self._force_constant = force_constant

    def energy(self, instantaneous_value):
        return 0.5 * self._force_constant * np.square(instantaneous_value - self._ideal_value)

    def force(self, instantaneous_value):
        return self._force_constant * (instantaneous_value - self._ideal_value)