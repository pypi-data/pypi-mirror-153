"""
pdb.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.analysis.rmsd import rmsd
# noinspection PyProtectedMember
from molecular.io.read import _read_pdb

import numpy as np
from urllib.request import urlopen


# noinspection PyPep8Naming,SpellCheckingInspection
def RCSB(pdb_id, most_common=False):
    """
    Download PDB from RCSB.

    Parameters
    ----------
    pdb_id : str
        Reference ID for the PDB structure.
    most_common : bool
        Extract only the PDB structure with the lowest internal RMSD.

    Returns
    -------
    molecular.Trajectory
        Instance of Trajectory object.
    """

    # Read RCSB and return molecular Trajectory
    result = _read_pdb(urlopen('http://files.rcsb.org/download/' + pdb_id + '.pdb').read().decode('utf-8'))

    # If most_common, compute the pairwise RMSD and select structure structure with minimum average value
    if most_common:
        r = rmsd(result, paired=False, fit=True)
        i = np.argmin(r.mean(axis=0))
        result = result[i]

    # Return
    return result
