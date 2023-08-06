"""
stride.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np
import pandas as pd
import os
import re
import shutil
import subprocess


class StrideError(Exception):
    pass


class Stride:
    """
    Store the results from stride.
    """

    # Initialize class instance
    def __init__(self, raw):
        """
        Initialize Stride instance.

        Parameters
        ----------
        raw : str
            Raw stride output.
        """

        # Initialize hidden variables
        self._raw = None
        self._data = None

        # Sets raw and creates processed data
        self.raw = raw

    # Slice data
    def __getitem__(self, item):
        return self._data[item]

    # Override __repr__
    def __repr__(self):
        return self._raw

    # Returns processed pandas DataFrame
    @property
    def data(self):
        """
        Raw data processed into pandas.DataFrame

        Returns
        -------
        pandas.DataFrame
            Processed data.
        """

        return self._data

    @data.setter
    def data(self, value):
        raise NotImplemented

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, raw):
        self._raw = raw

        # Filter for pertinent records in output
        records = re.sub(r'^(?!ASG).*$', '', raw, flags=re.MULTILINE).replace('\n\n', '\n').lstrip()

        # Sections of output
        sections = np.array([
            (3, 'record', '<U3'),
            (5, 'residue', '<U5'),
            (2, 'chain', '<U2'),
            (5, 'residue_id', 'int'),
            (5, 'residue_id2', 'int'),
            (5, 'secondary_structure', '<U4'),
            (14, 'secondary_structure_text', '<U14'),
            (10, 'phi', 'float'),
            (10, 'psi', 'float'),
            (10, 'area', 'float'),
            (10, 'extra', '<U10')
        ], dtype=[('width', 'i1'), ('column', '<U24'), ('type', '<U10')])

        # Parse records and return as DataFrame
        data = np.genfromtxt(records.split('\n'), delimiter=sections['width'], dtype=sections['type'], autostrip=True)
        data = pd.DataFrame(data.tolist(), columns=sections['column'])

        # Drop extraneous columns
        data = data.drop(columns=['record', 'residue_id2', 'extra'])

        # Return data
        self._data = data


# TODO it would be great to eventually bind stride to Python directly (as opposed to going through subprocess)
# Compute secondary structure with stride
def stride(fname, executable='stride'):
    """
    Compute the secondary structure using STRIDE

    In addition to the secondary structure, STRIDE outputs phi and psi dihedral angles as well as the solvent-accessible
    surface area.

    Parameters
    ----------
    fname : str
        Path to PDB file.
    executable : str
        Location of stride executable (Default: stride).

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the results of STRIDE. Columns include: residue_id, chain, secondary_structure,
        secondary_structure_text, phi, psi, and area.

    Examples
    --------
    Computing the secondary structure as you would on the command line with STRIDE.
    >>> from molecular.external import stride
    >>> ss = stride('my.pdb')['secondary_structure'].values

    Computing the secondary structure on a Structure (or Trajectory)
    >>> from molecular.analysis import secondary_structure
    >>> from molecular.io import read_pdb
    >>> ss = secondary_structure(read_pdb('my.pdb'))
    """

    # Make sure executable exists
    if shutil.which('stride') is None and not os.path.exists(executable):
        raise AttributeError('executable %s not found. Download at http://webclu.bio.wzw.tum.de/stride/' % executable)
    
    # Run STRIDE and capture output
    process = subprocess.Popen([executable, fname], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    # Error check; make sure STRIDE finishes successfully
    if process.wait() != 0:
        raise StrideError('stride failed')

    # Return raw output
    return Stride(output.decode('ASCII'))
