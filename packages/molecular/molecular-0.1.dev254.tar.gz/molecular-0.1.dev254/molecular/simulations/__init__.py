
from .replica_exchange import *

__all__ = [
    'ExchangeHistory',
    'get_pme_size',
    'temp_schedule',
]


# TODO move this to a better location
# TODO does this actually belong in the package namdtools?
def get_pme_size(a):
    """
    Given a box length, figure out the grid size for PME. We are looking for the PME size that's ~1 grid spacing, while
    with only small prime factors 2, 3, and 5.

    Parameters
    ----------
    a : numeric
        Size of box length.

    Returns
    -------
    int
        Size of PME grid length.
    """

    # To reduce runtime, import this here
    # TODO can this be replaced with a numpy or scipy package?
    from sympy.ntheory import factorint

    # If a is a decimal, round up
    a = int(np.ceil(a))

    # We want to find larger number that has only factors 2, 3, and 5
    # noinspection PyShadowingNames
    def _has_only_factors(a):
        factors = np.array(list(factorint(a).keys()))
        for factor in [2, 3, 5]:
            factors = np.delete(factors, np.where(factors == factor))
        return len(factors) == 0

    # Keep on increasing a until we find the right number
    while not _has_only_factors(a):
        a += 1

    # Return
    return a


if __name__ == '__main__':
    print(get_pme_size(68.))
