"""
Boltzmann
"""

import numpy as np

from scipy.constants import Boltzmann, Avogadro, atmosphere
import scipy.constants

__all__ = [
    'AVOGADRO',
    'BOLTZMANN'
]


AVOGADRO = scipy.constants.Avogadro
BOLTZMANN = scipy.constants.Boltzmann


# TODO make this easily usable.
class GasConstant:
    def __init__(self):
        pass

    @property
    def kcal_per_K_mol(self):
        return per_mole(joule_to_kcal(BOLTZMANN))


# Joule to kcal conversion
def joule_to_kcal(x):
    """
    Convert joule to kcal. 1 J = 1 / 4184. kcal

    Parameters
    ----------
    x : float
        Joule.

    Returns
    -------
    float
        kcal.
    """

    return x / 4184.


# kcal to Joule conversion
def kcal_to_joule(x):
    """
    Convert kcal to joule. 1 kcal = 4184 J.

    Parameters
    ----------
    x : float
        kcal.

    Returns
    -------
    float
        Joule.
    """

    return 4184. * x


def per_mole(x):
    """
    Convert quantity to per mole. Divide by NA.

    Parameters
    ----------
    x : float
        Quantity.

    Returns
    -------
    float
        Quantity per mole.
    """

    return x * AVOGADRO


# Boltzmann constant in kcal/K/mol
BOLTZMANN_KCAL_K_MOL = per_mole(joule_to_kcal(BOLTZMANN))
BOLTZMANN_KCAL_MOL_K = BOLTZMANN_KCAL_K_MOL
np.testing.assert_almost_equal(BOLTZMANN * AVOGADRO / 4184., BOLTZMANN_KCAL_K_MOL)

# Pressure
pressure = Avogadro * atmosphere / 1e30 / 4184.  # 1e-30 m^3 per A^3, 4184 J per kcal

if __name__ == '__main__':
    print(f'kb={BOLTZMANN_KCAL_MOL_K} kcal/mol')
