"""
contacts.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.geometry import distance


# Compute the contacts between groups
def _distance_matrix(xyz0, xyz1):
    return distance(xyz0, xyz1)



