"""
r1N.py

language: Python
version: 3.7
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.geometry import vecdist


# noinspection PyPep8Naming
def r1N(a):
    """

    Parameters
    ----------
    a : Trajectory

    Returns
    -------

    """

    # Extract the first and last residue_id
    residue_ids = a.topology['residue_id']
    residue_id1 = residue_ids.min()
    residue_idN = residue_ids.max()

    # Compute the center of masses
    com_id1 = a.select(residue_id=residue_id1).center()
    com_idN = a.select(residue_id=residue_idN).center()

    # Return the distances
    return vecdist(com_id1, com_idN)
