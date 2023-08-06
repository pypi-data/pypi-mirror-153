"""
structure.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .errata import pivot
from .trajectory import Trajectory

from molecular.analysis.protein.hydrophobicity import rmsd
from molecular.external import stride

from glovebox import GloveBox
import numpy as np
import os

# os.environ["MODIN_ENGINE"] = 'dask'
# import modin.pandas as pd
import pandas as pd


# Structure class
class Structure:
    """
    A `Structure` is an object that stores a single three-dimensional "structure"

    "Structure" can be used loosely here because it applies to proteins, proteins in water baths, proteins in lipid
    environments, ligands in water, etc.

    The `Structure` instance generally follows PDB format [1] in that in contains,
      - id
      - x
      - y
      - z
      - alpha
      - beta
    """

    # Required columns
    columns = [
        'atom_id',
        'atom',
        'residue',
        'chain',
        'residue_id',
        'x',
        'y',
        'z',
        'alpha',
        'beta',
        'segment',
        'element',
    ]

    # Initialize class instance
    def __init__(self, data=None, topology=None):
        """
        Initialize class instance
        """

        # TODO should this be protected?
        # Save data or create blank DataFrame
        self._data = data if data is not None else pd.DataFrame(columns=self.columns)

        # Construct topology
        self.topology = None

    # Add
    def __add__(self, other):
        """
        Add constant to Cartesian coordinates of Structure instance.

        Parameters
        ----------
        other

        Returns
        -------

        """

        for column in ['x', 'y', 'z']:
            self._data[column] += other

        return self.copy()

    # Get attribute
    def __getattr__(self, item):
        if item not in self._data:
            raise AttributeError('%s not in Structure' % item)

        return self._data[item].values

    # Get atom from Structure by index
    def __getitem__(self, item):
        """

        Parameters
        ----------
        item

        Returns
        -------

        """

        # Make sure that item a valid atom_id
        if item not in self._data['atom_id']:
            raise AttributeError('%s not a valid atom_id' % item)

        # Create copy of the row
        data = self._data[self._data['atom_id'] == item].copy()

        # Sanity
        if len(data) != 1:
            raise AttributeError('multiple atom_id %s found in Structure' % item)

        # Return (as Series)
        return data.iloc[0, :]

    # Length of structure (returns number of atoms)
    def __len__(self):
        """
        Number of atoms in the Structure instance.

        Returns
        -------
        int
            Number of atoms in the Structure instance.
        """

        return len(self._data)

    # Add new atoms from list
    def add_atoms(self, **kwargs):
        """

        Parameters
        ----------
        kwargs

        Returns
        -------
        """

        # _add_atoms(self.data, self.columns, kwargs)
        pass

    # Apply
    def apply(self, function):
        return function(self)

    # TODO is this too specific? Evaluate if Structure should be more generalized
    # Compute secondary structure
    def compute_secondary_structure(self, recompute=False, executable='stride'):
        # If secondary_structure is not in the Structure, or recompute is true, compute
        if 'secondary_structure' not in self._data or recompute:
            # TODO in lieu of directly porting stride to Python, how can this be sped up?
            # Write out PDB of structure to glovebox
            gb = GloveBox('molecular-stride', persist=True)
            temp_pdb = os.path.join(gb.path, 'temp.pdb')
            self.to_pdb(temp_pdb)

            # Run STRIDE
            secondary_structure = stride(temp_pdb, executable=executable)[['residue_id', 'secondary_structure']]

            # Clean glovebox
            gb.clean()

            # Drop secondary_structure if it's already in self._data
            self._data = self._data.drop(columns='secondary_structure', errors='ignore')

            # Merge STRIDE results with Structure to store
            self._data = self._data.merge(secondary_structure, how='inner', on='residue_id', validate='m:1')

        # Return
        return self._data[['residue_id', 'secondary_structure']].drop_duplicates()

    # Copy
    def copy(self):
        """
        Create a copy of Structure instance.

        Returns
        -------
        molecular.Structure
            Copy of instance.
        """

        return Structure(self._data.copy())

    # Pivot
    def pivot(self, index, columns=None, values=None, aggfunc='mean'):
        return pivot(self._data, index=index, columns=columns, values=values, aggfunc=aggfunc)

    # TODO should this return a Structure or Trajectory? TBD
    # TODO what if there were an intermediate object, like a Query class that knew how to handle subindexing / setting
    # Query
    def query(self, text):
        # TODO make this so it's customizable
        # Run macros
        text = text.lower().replace('peptide', 'residue in ["ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", ' +
                                    '"HIS", "HSD", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", ' +
                                    '"SER", "THR", "TRP", "TYR", "VAL"]')

        # Get indices and parsed data
        indices = self._data.query(text).index.values
        data = self._data.loc[self._data.index.isin(indices), :]

        # If self is Trajectory, return a Trajectory
        if isinstance(self, Trajectory):
            result = Trajectory(data)
        else:
            result = Structure(data)

        # Return to user
        return result

    # TODO extend this to another trajecotry
    # Compute RMSD
    def rmsd(self, structure):
        """
        Compute root-mean-square deviation (RMSD) with another structure.

        Parameters
        ----------
        structure :

        Returns
        -------

        """

        return rmsd(self.xyz, structure.xyz)

    # Set topology
    def set_topology(self, topology):
        """
        Set topology

        Parameters
        ----------
        topology : Topology
            Instance of Topology class
        """

        self.topology = topology

    # Write to CSV
    def to_csv(self, path, topology=False):
        pass

    # Save as PDB
    def to_pdb(self, filename_or_buffer):
        """

        Parameters
        ----------
        filename_or_buffer

        Returns
        -------

        """

        # Create a copy of the data
        data = self._data.copy()

        # Add ATOM record
        data['record'] = 'ATOM'

        # TODO this should also be done for residue id probably
        # Change base-0 to base-1 for atom_id
        if data['atom_id'].min() == 0:
            data['atom_id'] += 1

        # Format atom
        i = data['atom'].str.len() == 1
        data.loc[i, 'atom'] = ' ' + data.loc[i, 'atom'] + '  '

        i = data['atom'].str.len() == 2
        data.loc[i, 'atom'] = ' ' + data.loc[i, 'atom'] + ' '

        # Select pertinent columns
        data = data[['record', 'atom_id', 'atom', 'residue', 'chain', 'residue_id',
                     'x', 'y', 'z', 'alpha', 'beta', 'segment', 'element']]

        # Write out PDB file
        np.savetxt(
            filename_or_buffer,
            data,
            fmt='%-6s%5i %4s%4s%2s%4i%12.3f%8.3f%8.3f%6.2f%6.2f%9s%2s',
            header='CRYST1    0.000    0.000    0.000  90.00  90.00  90.00 P 1           1',
            footer='END',
            comments=''
        )

    # Convert to trajectory
    def to_trajectory(self, structure_id=None):
        # Create and/or update structure_id if necessary
        if 'structure_id' not in self._data:
            structure_id = 0
        if structure_id is not None:
            self._data['structure_id'] = structure_id

        # Return Trajectory
        return Trajectory(self._data)

    # Get coordinates
    @property
    def xyz(self):
        """

        Returns
        -------

        """

        return self._data[['x', 'y', 'z']].values


# Trajectory cannot simply be a list of Structures
# class Trajectory(Structure):
#     """
#
#     """
#
#     # Initialize instance of Trajectory class
#     # noinspection PyMissingConstructor
#     def __init__(self, data=None):
#         if isinstance(data, pd.DataFrame):
#             self._data = data
#
#     # Get Structure from Trajectory
#     def __getitem__(self, item):
#         """
#
#
#         Parameters
#         ----------
#         item
#
#         Returns
#         -------
#
#         """
#
#         # Convert item to integer array if not already
#         item = np.array(item, dtype='int').reshape(-1)
#         if len(item) not in [1, 2]:
#             raise AttributeError('index must be structure_id or list with [structure_id, atom_id]')
#
#         # First, get structure
#         result = self.get_structure(item[0])
#
#         # If there's a second dimension, get an atom
#         if len(item) == 2:
#             result = result[item[1]]
#
#         # Return
#         return result
#
#     # Get number of structures in Trajectory
#     def __len__(self):
#         """
#         Number of structures in Trajectory.
#
#         """
#
#         return self._data['structure_id'].nunique()
#
#     # Add a structure
#     # noinspection PyProtectedMember
#     def add_structure(self, structure):
#         structure._data['structure_id'] = self._data['structure_id'].max() + 1
#         self._data = pd.concat([self._data, structure._data])
#
#     # TODO this can be parallelized
#     # Apply
#     def apply(self, function):
#         result = None
#         for structure_id in self._data['structure_id'].unique():
#             # Run the apply function from the Structure with structure_id
#             result_ = self.get_structure(structure_id).apply(function)
#
#             # If the result is a series, convert to frame and use structure_id as the index
#             if isinstance(result_, pd.Series):
#                 result_ = result_.to_frame().T
#                 result_.index = [structure_id]
#                 result_.index.name = 'structure_id'
#
#             if result is None:
#                 result = result_
#             else:
#                 if isinstance(result, pd.DataFrame):
#                     result = pd.concat([result, result_])
#                 elif isinstance(result, list):
#                     result.append(result_)
#                 else:
#                     result = [result, result_]
#
#         return result
#
#     # TODO this can be parallelized
#     # Compute secondary structure
#     def compute_secondary_structure(self, recompute=False, executable='stride'):
#         for structure_id in self._data['structure_id'].unique():
#             self.get_structure(structure_id).compute_secondary_structure(recompute=recompute, executable=executable)
#
#     # Get structure
#     def get_structure(self, structure_id):
#         # Make sure structure_id is an array
#         structure_id = np.array(structure_id, dtype='int').reshape(-1)
#
#         # Parse DataFrame for appropriate rows and return as Structure
#         return Structure(self._data.loc[self._data['structure_id'].isin(structure_id), :])
