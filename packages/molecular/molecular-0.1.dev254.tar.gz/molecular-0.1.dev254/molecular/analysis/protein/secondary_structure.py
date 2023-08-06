"""
secondary_structure.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.core import Quantity, Trajectory
from molecular.external import StrideError, stride
from molecular.statistics import Block

from functools import lru_cache, partial
from glovebox import GloveBox
import logging
import numpy as np
import os
import pandas as pd

logger = logging.getLogger('molecular.analysis')


def _expand_secondary_structure(data):
    """
    Expands secondary structure strings from condensed format (ex: CCCC) to expanded format (ex: C C C C, where each
    residue has its own DataFrame column).

    Parameters
    ----------
    data : pandas.Series
        Secondary structure in condensed format.

    Returns
    -------
    pandas.DataFrame
        Secondary structure in expanded format.
    """

    # This method only works on Series
    if not isinstance(data, pd.Series):
        raise AttributeError('data must be Series')

    # Convert from condensed to expanded format
    data = data.str.join(',').str.split(',', expand=True)
    data.index.name = 'structure'
    data.columns.name = 'residue'

    # Return
    return data


# Class to store secondary structure results
class SecondaryStructure:
    """
    Store the result of secondary structure computation through STRIDE.

    By itself, an instance of `SecondaryStructure` is not a `Quantity`. There are several options for converting an
    instance of `SecondaryStructure` to a `Quantity`.
    """

    # STRIDE secondary structure codes
    codes = ['H', 'G', 'I', 'E', 'B', 'b', 'T', 'C']

    # Initialize instance of SecondaryStructure
    def __init__(self, data, condensed=False):
        """
        Initialize instance of SecondaryStructure class.

        Parameters
        ----------
        data : pandas.Series or pandas.DataFrame
            The secondary structure data from STRIDE. Contains a column for each residue_id, and contains a row for
            each observation. Element represent the secondary structure code from STRIDE.
        condensed : bool
            Is `data` condensed as pandas.Series, or expanded as pandas.DataFrame? (Default: False)
        """

        # Convert condensed Series to expanded DataFrame
        if condensed:
            data = _expand_secondary_structure(data)
            logger.info(f'expanded secondary structure to shape {data.shape}')

        # At this point, we must have a DataFrame
        if not isinstance(data, pd.DataFrame):
            raise AttributeError('must be pandas DataFrame, not %s' % type(data))

        # Set instance value
        self._data = data
        self._data_long = None
        self._data_condensed = None

    @classmethod
    def from_csv(cls, fname):
        """
        Read secondary structure from CSV.

        Parameters
        ----------
        fname : str
            Name of file

        Returns
        -------
        SecondaryStructure
        """

        cls(pd.read_csv(fname))

    def __getitem__(self, item):
        data = self._data.iloc[item, :].to_frame().T
        return SecondaryStructure(data)

    # Override __repr__
    def __repr__(self):
        # return str(self._data.agg(''.join, axis=1).values)
        # return self._condense_data()
        return str(self._data)

    def _condense_data(self):
        if self._data_condensed is None:
            self._data_condensed = self._data.agg(''.join, axis=1)
        return self._data_condensed

    # Handle codes
    @staticmethod
    def _handle_codes(codes):
        # If codes is not defined, use the global codes
        if codes is None:
            codes = SecondaryStructure.codes

        # Convert codes to numpy array for simplicity
        codes = np.array(codes).reshape(-1)

        # Make sure that all codes are permissible
        if ~np.isin(codes, SecondaryStructure.codes).all():
            bad_codes = [code for code in codes if code not in SecondaryStructure.codes]
            raise AttributeError('bad codes %s were provided' % bad_codes)

        # Return
        return codes

    # Convert from wide to long
    def _wide_to_long(self):
        """
        Convert from wide to long format.

        Returns
        -------
        pandas.DataFrame
            Secondary structure in long format.
        """

        # Convert to (residue, structure, code) format
        if self._data_long is None:
            self._data_long = self._data.stack().to_frame('code').reset_index()

        # Return
        return self._data_long

    # Count
    # TODO this could be memoized
    @lru_cache(maxsize=None)
    def count(self, axis=0):
        """
        Compute the count of secondary structure types. If axis=0, the count per residue is returned. If axis=1, the
        count per structure is returned. If count is None

        Parameters
        ----------
        axis : int or None
            (Default: 0)


        Returns
        -------
        pandas.Series or pandas.DataFrame

        """

        # Convert from wide to long
        data = self._wide_to_long()

        # axis=0 is residue
        if axis == 0:
            result = pd.crosstab(data['residue'], data['code'])

        # axis=1 is structure
        elif axis == 1:
            result = pd.crosstab(data['structure'], data['code'])

        # axis is None is count over all residues and structures
        elif axis is None:
            result = data.value_counts('code')

        # if we've made it here, something is wrong
        else:
            raise AttributeError(f'axis {axis} not understood')

        # Log
        logger.info(f'computed secondary structure count')

        # Return
        return result

    # Mean
    def mean(self, axis=0):
        """
        Compute the average secondary structure by code for the entire protein (axis = None), each structure (axis = 0),
        or each residue (axis = 1).

        Parameters
        ----------
        axis : None or int.
            Designates if the average should be computed for the entire protein (axis = None), each structure
            (axis = 0), or each residue (axis = 1). (Default: 0)

        Returns
        -------
        pandas.Series or pandas.DataFrame
            If axis = None, pandas.Series is returned. Otherwise, the result will be pandas.DataFrame.
        """

        # Get the axis counts
        data = self.count(axis=axis)

        # If axis 0 or 1
        if axis in [0, 1]:
            # noinspection PyArgumentList
            result = data.div(data.sum(axis=1), axis=0).fillna(0)

        # Otherwise, if axis is None
        else:
            result = data / data.sum()

        # Log
        logger.info(f'computed secondary structure mean')

        # Return
        return result

    # Replace
    def replace(self, old_code, new_code):
        """
        Global replacement of secondary structure type.

        Parameters
        ----------
        old_code : str
        new_code : str

        Returns
        -------

        Examples
        --------
        >>> ss = SecondaryStructure(...)
        >>> ss.replace('G', 'H')
        """

        # Log the changes
        logger.info(f'replacing secondary structure {old_code} with {new_code}')

        # Replace and store the data
        self._data = self._data.replace(old_code, new_code)

    # SEM from block averaging
    def sem_block(self, n_blocks=10):
        # Block data
        blocks = Block(self._data, n_blocks=n_blocks)

        # Convert to long format
        # noinspection PyProtectedMember
        data = blocks._data.reset_index().set_index(['structure', 'block']).stack().to_frame('code').reset_index()

        # Get counts
        counts = data.pivot_table(index=['block', 'residue'], columns='code', values='structure', aggfunc='count')\
            .fillna(0)

        # Get averages
        averages = counts.div(counts.sum(axis=1), axis=0).fillna(0.).reset_index()

        # Get std
        std = averages.pivot_table(index='residue', values=counts.columns, aggfunc=partial(np.std, ddof=1, axis=0))

        # Compute SEM
        sem = std / np.sqrt(n_blocks)

        # Log
        logger.info(f'computed secondary structure SEM with n_blocks = {n_blocks}')

        # Compute SEM
        return sem

    # Standard deviation
    def std(self, axis=None, codes=None):
        pass

    # Sum
    def sum(self, axis=None, codes=None):
        # Handle codes
        codes = self._handle_codes(codes)

        # x
        result = {}
        for code in codes:
            if axis in [0, 1]:
                result[code] = (self._data == code).sum(axis=axis)
            else:
                result[code] = (self._data == code).sum(axis=0).sum()
        return result

    # Do residues have code?
    def residues_with_code(self, code, residue_id=None):
        """
        `Quantity`

        Parameters
        ----------
        code
        residue_id

        Returns
        -------

        """

        # Handle code
        if code is None:
            raise AttributeError('code cannot be None')
        code = self._handle_codes(code)

        # Handle residue_id
        if residue_id is None:
            residue_id = self._data.columns
        residue_id = np.array(residue_id, dtype='int').reshape(-1)

        # Return as Quantity
        return Quantity(self._data[residue_id].isin(code))

    @property
    def sequence(self):
        return self._condense_data().values

    def to_csv(self, fname):
        """
        Write secondary structure object to comma-separated file.

        Parameters
        ----------
        fname

        Returns
        -------

        """

        self._data.to_csv(fname)


# Compute secondary structure using stride for a trajectory
def secondary_structure(trajectory, executable='stride', progress_bar=False):
    """
    Compute the secondary structure for :class:`molecular.Trajectory`.

    Parameters
    ----------
    trajectory : Trajectory
        An instance of Structure or Trajectory
    executable : str
        Path to stride executable. (Default: stride)
    progress_bar : bool
        Should we show a progress bar? (Default: False)

    Returns
    -------
    SecondaryStructure
        The secondary structure for the object.
    """

    # If not Trajectory, throw an error
    if not isinstance(trajectory, Trajectory):
        raise AttributeError('cannot interpret %s' % trajectory)

    # Filter only peptide atoms out of Trajectory
    peptide_trajectory = trajectory.query('peptide', only_index=False)

    # Return the result applied to the peptide as SecondaryStructure instance
    result = pd.DataFrame(peptide_trajectory.apply(partial(_compute_secondary_structure, executable=executable),
                                                   progress_bar=progress_bar))
    result['structure_id'] = np.arange(peptide_trajectory.n_structures)
    return SecondaryStructure(result.set_index('structure_id'))


# Compute the secondary structure for a single structure
def _compute_secondary_structure(structure, executable='stride', errors='ignore'):
    """
    Compute the secondary structure for a :func:`molecular.Structure` instance

    Parameters
    ----------
    structure : Structure
        Instance of Structure class.
    executable : str
        Path to STRIDE executable.

    Returns
    -------
    pandas.Series
        The secondary structure
    """

    # Create temporary PDB in glovebox
    gb = GloveBox('molecular-stride', persist=True)
    temp_pdb = os.path.join(gb.path, 'temp.pdb')
    structure.to_pdb(temp_pdb)

    # Run STRIDE
    # result = stride(temp_pdb, executable=executable)[['residue_id', 'secondary_structure']]
    try:
        result = stride(temp_pdb, executable=executable)[['residue_id', 'secondary_structure']]
    except StrideError as e:
        if 'ignore' in errors.lower():
            n_res = structure.select(name='CA').count()
            result = pd.DataFrame({
                'residue_id': range(n_res),
                'secondary_structure': 'X' * n_res
            })
        else:
            raise e

    # Clean out the glovebox
    gb.clean()

    # Return
    return result.set_index('residue_id').iloc[:, 0]
