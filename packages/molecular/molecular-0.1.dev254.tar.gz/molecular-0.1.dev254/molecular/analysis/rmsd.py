"""
rmsd.py
written in Python3
author: C. Lockhart

>>> from molecular import read_pdb, rmsd
>>> trajectory = read_pdb('trajectory1.pdb')
>>> first_structure = trajectory[0]
>>> rmsd = rmsd(trajectory, first_structure)

"""


# noinspection PyProtectedMember
from molecular.transform.transform import _fit

import logging
from itertools import product
import numpy as np


# Get the logger
logger = logging.getLogger('molecular.analysis')


# Compute the RMSD between 2 Trajectories
def rmsd(a, b=None, paired=False, fit=True):
    """
    Compute the RMSD.

    If only `a` is provided, then the RMSD is computed between all structures in the Trajectory.
    Otherwise, if `a` and `b` are provided, we compute the RMSD between all structures in `a` and all structures in `b`.


    Parameters
    ----------
    a : molecular.Trajectory
    b : molecular.Trajectory
        (Optional)
    paired : bool
        Are `a` and `b` paired? That is, should we compute RMSD between (a[0], b[0]), (a[1], b[1]), etc.? If False, the
        Cartesian product of a and b are taken (Default: False)
    fit : bool
        Should structures be fit before RMSD is computed? (Default: True)

    Returns
    -------


    See Also
    --------
    http://manual.gromacs.org/documentation/current/onlinehelp/gmx-rms.html
    """

    # If `b` is None, then select `a`. Also, make sure we're not paired.
    if b is None:
        b = a
        if paired:
            logger.warning('setting paired=False because Trajectory b was not specified')
        paired = False

    # Number of atoms between a and b must be identical
    n_atoms = a.n_atoms
    if n_atoms != b.n_atoms:
        raise AttributeError('a and b must have same number of atoms')

    # Get coordinates
    a_xyz = a.xyz
    b_xyz = b.xyz

    # Assign indices of pairs from a and b
    a_index = a.structure_ids
    b_index = b.structure_ids
    if paired:
        if len(a) != len(b):
            raise AttributeError('cannot compute paired RMSD because a and b have different number of structures')

    else:
        # FIXME the problem with this that it's memory-intensive; could move to iterable, but then we'd have to loop
        # iterable = product(range(a.n_structures), range(b.n_structures))
        a_index, b_index = np.transpose(list(product(a_index, b_index)))

    # Expand a_xyz and b_xyz so they have the same dimensions and become "paired"
    a_xyz = a_xyz.loc[a_index, :, :]
    b_xyz = b_xyz.loc[b_index, :, :]

    # Should we fit the two structures?
    if fit:
        b_xyz = _fit(a_xyz, b_xyz)

    # Compute the difference between a and b
    # diff = a_xyz[a_index, :, :] - b_xyz[b_index, :, :]

    # Actually Compute RMSD
    result = np.sqrt((a_xyz - b_xyz).pow(2).to_numpy().sum() / n_atoms)
    # result = np.zeros((a.n_structures, b.n_structures))
    # for i, j in iterable:
    #     result[i, j] = np.sqrt(np.mean((a_xyz[i, :, :] - b_xyz[j, :, :]) ** 2))

    # Pivot into wide form
    # https://stackoverflow.com/questions/17028329/python-create-a-pivot-table
    # rows, row_pos = np.unique(a_index, return_inverse=True)
    # cols, col_pos = np.unique(b_index, return_inverse=True)
    # pivot_table = np.zeros((len(rows), len(cols)))
    # pivot_table[row_pos, col_pos] = result
    if not paired:
        result = result.reshape(a.n_structures, b.n_structures)

    # Return
    return result

#
# def _rmsd(a, b, paired=False, fit=True):
#     """
#
#     Parameters
#     ----------
#     a
#     b
#
#     Returns
#     -------
#
#     """
#
#     # Get the number of elements in a and b
#     n_a = len(a)
#     n_b = len(b)
#
#     a_xyz = a.xyz
#     b_xyz = b.xyz
#
#     # Should we fit the two structures?
#     if fit:
#         b_xyz = _fit(a, b)
#
#     result = np.zeros((n_a, n_b))
#     if not paired:
#         iterable = product(range(n_a), range(n_b))
#     else:
#         iterable = zip(range(n_a), range(n_b))
#     for i, j in iterable:
#         result[i, j] = np.sqrt(np.mean((a_xyz[i, :, :] - b_xyz[j, :, :]) ** 2))
#
#     return result


if __name__ == '__main__':
    import molecular as mol

    trj = mol.read_pdb('../tests/samples/trajectory.pdb')
    print(rmsd(trj, trj[0], paired=False, fit=False).ravel())

    import mdtraj
    x = mdtraj.load('../tests/samples/trajectory.pdb')
    print(mdtraj.rmsd(x, x[0]))
