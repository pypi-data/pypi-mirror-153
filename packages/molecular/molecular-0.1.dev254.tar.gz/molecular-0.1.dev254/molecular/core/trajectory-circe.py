"""
trajectory.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .errata import pivot

import numpy as np
import pandas as pd
from typelike import ArrayLike, NumberLike
from tqdm import tqdm


# Trajectory class
class Trajectory(object):
    """
    `Trajectory` stores instantaneous data for a `Topology`, i.e., atomic coordinates, box information, velocity, etc.
    """

    # Initialize instance of Trajectory
    def __init__(self, xyz, box=None, topology=None):
        """


        Parameters
        ----------
        xyz : ArrayLike, three-dimensional
            Cartesian coordinates for all atoms and all structures. First axis must represent the structure index,
            second axis must represent the atom, and the third index will represent x, y, or z.
        topology : Topology
        """

        self._xyz = xyz
        self._box = box
        self._topology = topology

    # Add
    def __add__(self, other):
        if isinstance(other, NumberLike):
            self._xyz = self._xyz + other
        return self

    # Length of trajectory
    def __len__(self):
        """
        The length of the trajectory is the number of structures.

        Returns
        -------
        int
            Length of trajectory
        """

        return self.n_structures

    # Get item
    def __getitem__(self, item):
        """

        Parameters
        ----------
        item

        Returns
        -------

        """

        # If item is a slice, convert it to an array
        if isinstance(item, slice):
            item = np.arange(item.start, item.stop, item.step)

        # TODO create an IntLike object for typelike
        if isinstance(item, (int, np.int, np.int64, ArrayLike)):
            result = self.get_structure(item)

        # If we still don't know what to do, try to get from topology
        else:
            result = self.topology[item]

        return result

    # Representation of the object
    def __repr__(self):
        return """
            # structures: {0}
            # atoms: {1}
            # dimensions: {2}
        """.format(self.n_structures, self.n_atoms, self.n_dim)

    # Check topology
    def _check_topology(self):
        """
        Check that the topology is correctly set
        """

        # First off, must be Topology instance
        if not isinstance(self._topology, Topology):
            raise AttributeError('topology is not correct class (%s)' % type(self._topology))

        # Second, number of atoms must match
        if self.n_atoms != self._topology.n_atoms:
            raise AttributeError('number of atoms in topology and trajectory do not match ({0} vs {1})'
                                 .format(self.n_atoms, self._topology.n_atoms))

    # Apply
    # TODO please optimize this. Use vectorize, map, parallelization
    def apply(self, function, progress_bar=False):
        result = []
        structure_ids = np.arange(self.n_structures)
        if progress_bar:
            structure_ids = tqdm(structure_ids)
        for i in structure_ids:
            structure = self.get_structure(i)
            result.append(function(structure))
        return result

    # Compute the center of the Trajectory
    def center(self, weights=None):
        r"""
        Compute the center of every structure in the Trajectory.

        .. center = \frac{1}{N} \Epsilon w_i (x_i + y_i + z_i)

        Returns
        -------
        numpy.ndarray
            Center of every structure in the Trajectory.
        """

        return np.mean(self._xyz, axis=1)

    # Copy
    # TODO
    def copy(self):
        """
        Create a copy of the Trajectory.

        Returns
        -------
        molecular.Trajectory
            Deep copy of the Trajectory.
        """

        pass

    # Describe
    def describe(self):
        # print('protein sequence: %s' % self.topology.residues)
        print('# structures: %s' % self.n_structures)
        print('# atoms: %s' % self.n_atoms)
        print('# dimensions: %s' % self.n_dim)

    # Get atoms
    def get_atoms(self, index):
        return self.xyz[:, index, :]

    # Get structure
    def get_structure(self, index):
        index = np.array([index]).ravel()  # this sucks
        structure = Trajectory(self.xyz[index, :, :].reshape(len(index), self.n_atoms, self.n_dim),
                               topology=self.topology)
        if self.n_atoms != structure.n_atoms:
            raise AttributeError('number of atoms do not match ({0} vs {1})'.format(self.n_atoms, structure.n_atoms))
        return structure

    # Number of atoms
    @property
    def n_atoms(self):
        """
        Number of atoms in the `Trajectory`.

        Returns
        -------
        int
            Number of atoms
        """

        return self.shape[1]

    # Number of dimensions
    @property
    def n_dim(self):
        """
        Number of dimensions.

        Returns
        -------
        int
            Number of dimensions
        """

        return self.shape[2]

    # Number of structures
    @property
    def n_structures(self):
        """
        Number of structures in the `Trajectory`.

        Returns
        -------
        int
            Number of structures
        """

        return self.shape[0]

    # Query
    def query(self, expr, only_index=False):
        """
        Query the set `Topology` and return matching indices

        Parameters
        ----------
        expr : str
            Selection text. See :ref:`pandas.DataFrame.query`
        only_index : bool
            Should the entire Trajectory be returned, or only the array of indices?

        Returns
        -------
        numpy.ndarray or Trajectory
            Array of indices or Trajectory containing only expr.
        """

        # Query the topology to get pertinent data
        topology = self.topology.query(expr)

        # Extract indices
        # noinspection PyProtectedMember
        index = topology._data.index.values

        #
        if only_index:
            result = index

        else:
            # TODO does this work for when multiple structures should be returned?
            result = Trajectory(self.get_atoms(index).reshape(self.n_structures, len(index), self.n_dim),
                                topology=topology)

        # Return result
        return result

    # Recenter the trajectory
    def recenter(self, inplace=False):
        """
        Recenter all structures in the trajectory around the origin.

        Parameters
        ----------
        inplace : bool
            Make the change in place? (Default: False)
        """

        xyz = self._xyz - self.center()

        if inplace:
            self._xyz = xyz
        else:
            trajectory = Trajectory.copy()
            trajectory._xyz = xyz
            return trajectory

    # Select
    # TODO compare the efficiency of this vs query
    def select(self, **kwargs):
        """

        Parameters
        ----------


        Returns
        -------

        """

        # Save snapshot of topology data
        data = self.topology.to_frame()

        # Continuously slice the topology data
        for key in kwargs:
            item = kwargs[key]
            if not isinstance(item, ArrayLike):
                item = [item]
            data = data[data[key].isin(item)]

        # Extract indices and create a new topology
        index = data.index.values
        topology = Topology(data)

        # Return
        return Trajectory(self.get_atoms(index).reshape(self.n_structures, len(index), self.n_dim), topology=topology)

    # Shape
    @property
    def shape(self):
        """
        Shape of `Trajectory`

        Returns
        -------
        tuple
            (Number of structures, number of atoms, dimensionality)
        """

        return self._xyz.shape

    # Convert to pandas DataFrame
    def to_frame(self):
        """
        Convert `Trajectory` to pandas.DataFrame instance

        Returns
        -------
        pandas.DataFrame
            Trajectory represented as pandas DataFrame
        """

        # Prepare the data as DataFrame
        result = pd.DataFrame({
            'index': np.tile(np.arange(self.n_atoms), self.n_structures),
            'structure_id': np.repeat(np.arange(self.n_structures), self.n_atoms),
            'x': self._xyz[:, :, 0].ravel(),
            'y': self._xyz[:, :, 1].ravel(),
            'z': self._xyz[:, :, 2].ravel(),
        })

        # Return
        return result

    # Show
    def show(self):
        pass

    # Save as PDB
    def to_pdb(self, filename):
        """
        Convert `Trajectory` to PDB.

        Parameters
        ----------
        filename : str
            Name of PDB to write.
        """

        # Convert topology and trajectory to DataFrame
        topology = self.topology.to_frame()
        trajectory = self.to_frame()

        # Merge trajectory and topology
        data = trajectory.merge(topology.reset_index(), how='inner', on='index').set_index('index')

        # Sort by structure_id and then atom_id
        data = data.sort_values(['structure_id', 'atom_id'])

        # Add ATOM record
        data['record'] = 'ATOM'

        # TODO this should also be done for residue id probably
        # Change base-0 to base-1 for atom_id
        # if data['atom_id'].min() == 0:
        #     data['atom_id'] += 1

        # Format atom names
        i = data['atom'].str.len() == 1
        data.loc[i, 'atom'] = ' ' + data.loc[i, 'atom'] + '  '

        i = data['atom'].str.len() == 2
        data.loc[i, 'atom'] = ' ' + data.loc[i, 'atom'] + ' '

        # Open up the buffer
        with open(filename, 'w') as buffer:
            # Select every structure and write out
            # TODO please make this more efficient
            for structure in data['structure_id'].unique():
                is_structure = data['structure_id'] == structure

                # Select pertinent rows and columns
                structure = data.loc[is_structure, ['record', 'atom_id', 'atom', 'residue', 'chain', 'residue_id',
                                                    'x', 'y', 'z', 'alpha', 'beta', 'segment', 'element']]

                # Write out PDB file
                # TODO add box to header
                np.savetxt(
                    buffer,
                    structure,
                    fmt='%-6s%5i %4s%4s%2s%4i%12.3f%8.3f%8.3f%6.2f%6.2f%9s%2s',
                    header='CRYST1    0.000    0.000    0.000  90.00  90.00  90.00 P 1           1',
                    footer='END\n',
                    comments=''
                )

    # Convert to MDAnalysis Universe
    # mdanalysis.org
    def to_universe(self):
        pass

    # Get topology
    @property
    def topology(self):
        """
        Get the `Topology` instance.

        Returns
        -------
        Topology
            `Topology` instance associated with this `Trajectory`.
        """

        # Check the topology
        self._check_topology()

        # Return
        return self._topology

    # View
    # https://github.com/arose/nglview
    def view(self):
        pass

    # Get XYZ coordinates
    @property
    def xyz(self):
        """
        Get x, y, and z coordinates.

        Returns
        -------
        numpy.ndarray
            Cartesian coordinates.
        """

        return self._xyz


# Topology class
class Topology:
    """
    A `Topology` is an object that stores metadata for a `Trajectory`, such as atomic relationships

    "Atomic" can be used loosely here because it applies to proteins, proteins in water baths, proteins in lipid
    environments, ligands in water, etc.

    The `Topology` instance generally follows PDB format [1] in that in contains,
      - atom_id
      - atom
      - residue
      - chain
      - residue_id
      - alpha
      - beta
      - segment
      - element
    """

    # Required columns
    columns = [
        'atom_id',
        'atom',
        'residue',
        'chain',
        'residue_id',
        'alpha',
        'beta',
        'segment',
        'element',
    ]

    # Initialize class instance
    def __init__(self, data=None):
        """
        Initialize class instance
        """

        # If data is set, check that it's a DataFrame
        if data is not None and not isinstance(data, pd.DataFrame):
            raise AttributeError('data must be pandas.DataFrame')

        # Add index to data
        if isinstance(data, pd.DataFrame):
            data['index'] = (data['atom_id'].rank() - 1).astype(int)
            data = data.set_index('index')

        # TODO can this be protected?
        # Save data or create blank DataFrame
        self._data = data if data is not None else pd.DataFrame(columns=self.columns)

    # Add atom to topology
    def __add__(self, other):
        pass

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

        # First, try to see if we can ping the DataFrame
        if isinstance(item, str):
            return self._data[item].values

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

        return self.n_atoms

    # Add new atoms f
    def add_atoms(self, **kwargs):
        pass

    # Apply
    def apply(self, function):
        return function(self)

    # TODO is this too specific? Evaluate if Structure should be more generalized
    # Compute secondary structure
    # def compute_secondary_structure(self, recompute=False, executable='stride'):
    #     # If secondary_structure is not in the Structure, or recompute is true, compute
    #     if 'secondary_structure' not in self._data or recompute:
    #         # TODO in lieu of directly porting stride to Python, how can this be sped up?
    #         # Write out PDB of structure to glovebox
    #         gb = GloveBox('molecular-stride', persist=True)
    #         temp_pdb = os.path.join(gb.path, 'temp.pdb')
    #         self.to_pdb(temp_pdb)
    #
    #         # Run STRIDE
    #         secondary_structure = stride(temp_pdb, executable=executable)[['residue_id', 'secondary_structure']]
    #
    #         # Clean glovebox
    #         gb.clean()
    #
    #         # Drop secondary_structure if it's already in self._data
    #         self._data = self._data.drop(columns='secondary_structure', errors='ignore')
    #
    #         # Merge STRIDE results with Structure to store
    #         self._data = self._data.merge(secondary_structure, how='inner', on='residue_id', validate='m:1')
    #
    #     # Return
    #     return self._data[['residue_id', 'secondary_structure']].drop_duplicates()

    # Copy
    def copy(self):
        """
        Create a copy of `Topology` instance.

        Returns
        -------
        molecular.Topology
            Copy of instance.
        """

        return Topology(self._data.copy())

    # Number of atoms
    @property
    def n_atoms(self):
        """
        Get the number of atoms in the `Topology`.

        Returns
        -------
        int
            Number of atoms
        """

        return len(self._data)

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
        data = self._data.loc[self._data.index.isin(indices), :].copy()

        # Return
        return Topology(data)

    # TODO extend this to another trajectory
    # Compute RMSD
    def rmsd(self, structure):
        pass

    # Get residues
    @property
    def residues(self):
        """
        Get the residues of the Topology.

        Returns
        -------
        numpy.ndarray
            Array of residue names.
        """

        data = self._data[['residue_id', 'residue']].drop_duplicates()
        return data['residue'].values

    # Write to CSV
    def to_csv(self, path, topology=False):
        pass

    # Convert to pandas DataFrame
    def to_frame(self):
        """
        Convert to pandas.DataFrame

        Returns
        -------
        pandas.DataFrame
            `Topology` as pandas.DataFrame
        """

        return self._data.copy()

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
