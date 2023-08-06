"""
trajectory.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.core.errata import pivot
from molecular.transform import center, move

import logging
import numpy as np
import pandas as pd
from typelike import ArrayLike, NumberLike
from tqdm import tqdm

# Get the molecular.core logger
logger = logging.getLogger('molecular.core')


# https://softwareengineering.stackexchange.com/questions/386755/sharing-docstrings-between-similar-functions
def set_doc(original):
    def wrapper(target):
        target.__doc__ = original.__doc__.replace('a : molecular.Trajectory', '')
        return target

    return wrapper


# Trajectory class
class Trajectory(object):
    """
    `Trajectory` stores instantaneous data for a `Topology`, i.e., atomic coordinates, box information, velocity, etc.


    data:
        - structure_id
        - atom_id
        - x
        - y
        - z
        - vx
        - vy
        - vz
        - fx
        - fy
        - fz
        - alpha
        - beta
        - user

    config
        - structure_id
        - bx
        - by
        - bz


    """

    __slots__ = ['_data', '_configuration', '_topology']

    # Initialize instance of Trajectory
    def __init__(self, data=None, coordinates=None, box=None, topology=None):
        """


        Parameters
        ----------
        data : pandas.DataFrame
            (Optional) Structured information about Trajectory. Columns must include "structure_id", "atom_id", "x",
            "y", and "z".
        coordinates
        box
        topology : Topology
            (Optional) Topology that includes information about atoms.
        """

        # Make sure data has correct columns if available
        if isinstance(data, pd.DataFrame):
            data.reset_index(inplace=True)
            if not np.in1d(['structure_id', 'atom_id', 'x', 'y', 'z'], data.columns).any():
                raise AttributeError('data must include structure_id, atom_id, x, y, and z')
            data.set_index(['structure_id', 'atom_id'], inplace=True)
        elif data is not None:
            raise AttributeError('data must be pandas.DataFrame')

        # Process coordinates if set
        if coordinates is not None and isinstance(coordinates, np.ndarray):
            if data is None:
                data = _dummy_trajectory_data(*coordinates.shape)
            data[['x', 'y', 'z']] = coordinates.reshape(-1, 3)

        # Process box if set
        # TODO other names could be metadata... Ensemble class? System class? these names are bad SimulationParameters?
        configuration = None
        if box is not None and isinstance(box, np.ndarray):
            configuration = pd.DataFrame({
                'structure_id': np.arange(box.shape[0]),
                'bx': box[:, 0],
                'by': box[:, 1],
                'bz': box[:, 2]
            })

        # Process topology
        if topology is not None:
            if isinstance(topology, Trajectory):
                topology = topology.topology
            elif not isinstance(topology, Topology):
                raise AttributeError('topology must be Topology instance')

        # Save Trajectory data elements
        self._data = data
        self._configuration = configuration
        self._topology = topology

    # Add
    def __add__(self, other):
        if isinstance(other, NumberLike):
            self._data[['x', 'y', 'z']] = self._data[['x', 'y', 'z']] + other
        return self

    # Get item
    def __getitem__(self, item):
        """


        Parameters
        ----------
        item

        Returns
        -------

        """

        # Return
        # TODO what if item is in topology? Should we try to retrieve that?
        # TODO should this return a DataFrame or a Trajectory object?
        return self._data.loc[item]

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

    def __mul__(self, other):
        pass

    # Representation of the object
    def __repr__(self):
        return "# structures: {0}\n# atoms: {1}\n# dimensions: {2}".format(*self.shape)

    # Subtract the coordinates of this Trajectory by another coordinate system
    def __sub__(self, other):
        if isinstance(other, Trajectory):
            other = other.coordinates
        return self.move(by=-1. * other, inplace=False)

    # Get unique atom IDs (can be cached)
    @property
    def atom_ids(self) -> np.ndarray:
        """
        Get unique atom IDs in the Trajectory.

        Returns
        -------
        numpy.ndarray
            Array of atom IDs.
        """

        # noinspection PyUnresolvedReferences
        return self._data.index.levels[1]

    # Box
    @property
    def box(self):
        return self._configuration.set_index('structure_id')[['bx', 'by', 'bz']]

    # Get coordinates
    @property
    def coord(self):
        return self.coordinates

    # Set coordinates
    @coord.setter
    def coord(self, coord):
        self.coordinates = coord

    # Get coordinates
    @property
    def coordinates(self):
        """
        Get Cartesian coordinates from the Trajectory.

        Returns
        -------
        pandas.DataFrame
            Trajectory Cartesian coordinates.
        """

        return self._data[['x', 'y', 'z']]

    # Set coordinates
    @coordinates.setter
    def coordinates(self, coordinates):
        """
        Set Cartesian coordinates for the Trajectory.

        Parameters
        ----------
        coordinates : array-like
            Cartesian coordinates of same shape as Trajectory.
        """

        # Set coordinates
        self._data[['x', 'y', 'z']] = coordinates

    @property
    def columns(self):
        """

        Returns
        -------
        numpy.ndarray
        """

        return self._data.columns.to_numpy()

    # Trajectory designator
    @property
    def designator(self):
        return f'Trajectory:{self.hex_id}'

    # Hex ID of Trajectory
    @property
    def hex_id(self):
        return hex(id(self))

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

        # noinspection PyUnresolvedReferences
        return self._data.index.levshape[1]

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

        return self._data.shape[1]

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

        # noinspection PyUnresolvedReferences
        return self._data.index.levshape[0]

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

        return self.n_structures, self.n_atoms, self.n_dim

    # Get a list of structures
    @property
    def structure_ids(self) -> np.ndarray:
        """
        Get a numpy array of structure indices.

        Returns
        -------
        numpy.ndarray
            Structure indices.
        """

        # noinspection PyUnresolvedReferences
        return self._data.index.levels[0]

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

    # Get x
    @property
    def x(self):
        """
        Get x coordinates.

        Returns
        -------
        numpy.ndarray
            x coordinates.
        """

        return self._data['x']

    # Get y
    @property
    def y(self):
        """
        Get y coordinates.

        Returns
        -------
        numpy.ndarray
            y coordinates.
        """

        return self._data['y']

    # Get z
    @property
    def z(self):
        """
        Get z coordinates.

        Returns
        -------
        numpy.ndarray
            z coordinates.
        """

        return self._data['z']

    # Get xyz coordinates
    @property
    def xyz(self):
        """
        Get x, y, and z coordinates.

        Returns
        -------
        pandas.DataFrame
            Cartesian coordinates.
        """

        return self.coordinates

    @xyz.setter
    def xyz(self, xyz):
        self.coordinates = xyz

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
    @set_doc(center)
    def center(self, weights=None):
        return center(self, weights=weights)

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

        return Trajectory(data=self._data.copy(), topology=self._topology.copy())

    # Describe
    def describe(self):
        # print('protein sequence: %s' % self.topology.residues)
        print('# structures: %s' % self.n_structures)
        print('# atoms: %s' % self.n_atoms)
        print('# dimensions: %s' % self.n_dim)

    # Exclude
    def exclude(self, **kwargs):
        """
        Convenience function that passes to :func:`select`.

        Returns
        -------
        Trajectory
        """

        return self.select(exclude=True, **kwargs)

    # Get atoms
    def get_atoms(self, index):
        """
        Get specific atom indices from the Trajectory.

        Parameters
        ----------
        index : array-like
            List of atom indices.

        Returns
        -------
        pandas.DataFrame
            Trajectory information for atom indices.
        """

        # xyz will be a view if index is an int, otherwise it will be a copy...
        # TODO how will this affect behavior?
        # return self._xyz[:, index, :]
        mask = np.in1d(self._data.index.get_level_values('atom_id'), index)
        return self._data[mask].copy()  # need to do a copy here, because otherwise the view creates downstream warnings

    # Get column
    def get_column(self, column):
        return self._data[column]

    # Get structure
    def get_structure(self, index):
        """
        Get specific structure indices from the Trajectory.

        Parameters
        ----------
        index : array-like
            List of structure indices.

        Returns
        -------
        pandas.DataFrame
            Trajectory information for structure indices.
        """

        mask = np.in1d(self._data.index.get_level_values('structure_id'), index)
        return Trajectory(self._data[mask], topology=self._topology)

    def keys(self):
        return self._topology.keys()

    def min(self):
        return self.coordinates.pivot_table(index='structure_id', values=['x', 'y', 'z'], aggfunc='min')

    def max(self):
        return self.coordinates.pivot_table(index='structure_id', values=['x', 'y', 'z'], aggfunc='max')

    # Move
    @set_doc(move)
    def move(self, by=None, to=None, inplace=True):
        return move(self, by, to, inplace)

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
        index = topology._data.index.to_numpy()

        #
        if only_index:
            result = index

        else:
            # TODO does this work for when multiple structures should be returned?
            result = Trajectory(self.get_atoms(index), topology=topology)  # noqa

        # Return result
        return result

    # Select
    # TODO compare the efficiency of this vs query
    def select(self, exclude=False, **kwargs):
        """

        Parameters
        ----------


        Returns
        -------

        """

        # Save snapshot of topology data
        # noinspection DuplicatedCode,DuplicatedCode
        data = self._topology.to_frame()

        # Continuously slice the topology data
        for key in kwargs:
            item = kwargs[key]
            if not isinstance(item, ArrayLike):
                item = [item]
            mask = data[key].isin(item)
            if exclude:
                mask = ~mask
            data = data[mask]

        # Extract indices and create a new topology
        # Remember: Topology index is atom_id
        # TODO should I inforce that Topology.index = Topology.atom_id??
        index = data['atom_id'].to_numpy()  # used to be data.index, but this breaks on multiple selections
        topology = Topology(data)
        assert len(index) == len(topology)  # noqa

        # Create new Trajectory, log, and return
        # return Trajectory(self.get_atoms(index).reshape(self.n_structures, len(index), self.n_dim), topology=topology)
        trajectory = Trajectory(data=self.get_atoms(index), topology=topology)  # noqa
        logger.info(f'selected {trajectory.n_atoms} of {self.n_atoms} atoms (new Trajectory: '
                    f'{trajectory.designator}; exclude mode={exclude};'
                    f' {kwargs})')
        assert len(index) == trajectory.n_atoms  # noqa
        return trajectory

    # Recenter the Trajectory at the origin
    # TODO need to decide if this should be moved to molecular.transform
    def to_origin(self, weights=None, inplace=False):
        """
        Recenter all structures in the Trajectory around the origin.

        Parameters
        ----------
        weights : numpy.ndarray
            (Optional) Weights for atoms in the trajectory. Follows the definition from :ref:`numpy.average`.
        inplace : bool
            Make the change in place? (Default: False)
        """

        # Center xyz coordinates
        coord = self.coordinates - self.center(weights)

        # Center Trajectory in place or return a copy
        trajectory = self if inplace else self.copy()
        trajectory.coordinates = coord
        logger.info(f'centered {trajectory.designator} at origin')
        if not inplace:
            return trajectory

    # Convert to pandas DataFrame
    def to_frame(self):
        """
        Convert `Trajectory` to pandas.DataFrame instance

        Returns
        -------
        pandas.DataFrame
            Trajectory represented as pandas DataFrame
        """

        # Return
        return self._data

    # Show
    def show(self):
        pass

    # Save as PDB
    def to_pdb(self, fname):
        """
        Convert `Trajectory` to PDB.

        Parameters
        ----------
        fname : str
            Name of PDB to write.
        """

        # Convert topology and trajectory to DataFrame
        topology = self.topology.to_frame().reset_index()
        trajectory = self.to_frame().reset_index()

        # Merge trajectory and topology
        data = trajectory.merge(topology.reset_index(), how='inner', on='atom_id').set_index('atom_id').reset_index()

        # Sort by structure_id and then atom_id
        data = data.sort_values(['structure_id', 'atom_id'])

        # Add ATOM record
        data['record'] = 'ATOM'

        # TODO this should also be done for residue id probably
        # Change base-0 to base-1 for atom_id
        # if data['atom_id'].min() == 0:
        #     data['atom_id'] += 1

        # If we have more than 100000 atoms, we need to change atom_id
        # TODO this sort of sucks
        # https://github.com/MDAnalysis/mdanalysis/issues/1897
        fmt = '%-6s%5i %4s%4s%2s%4i%12.3f%8.3f%8.3f%6.2f%6.2f%9s%2s'
        if data['atom_id'].max() >= 99999:
            fmt = '%-6s%5s %4s%4s%2s%4i%12.3f%8.3f%8.3f%6.2f%6.2f%9s%2s'
            data['atom_id'] = pd.Series(np.vectorize(hex)(data['atom_id'])).str[2:]
            if data['atom_id'].str.len().max() >= 6:
                raise ValueError('cannot hex atom_id')
        else:
            # increment by 1 so atom_id starts at 1 and not 0
            data['atom_id'] = data['atom_id'] + 1

        # Format atom names
        i = data['atom'].str.len() == 1  # noqa
        data.loc[i, 'atom'] = data.loc[i, 'atom'].str.pad(2, side='left').str.pad(4, side='right')

        i = data['atom'].str.len() == 2
        data.loc[i, 'atom'] = data.loc[i, 'atom'].str.pad(3, side='left').str.pad(4, side='right')

        # Open up the buffer
        with open(fname, 'w') as buffer:
            # Select every structure and write out
            # TODO please make this more efficient
            for structure in data['structure_id'].unique():
                is_structure = data['structure_id'] == structure

                # Select pertinent rows and columns
                structure = data.loc[is_structure, ['record', 'atom_id', 'atom', 'residue', 'chain', 'residue_id',
                                                    'x', 'y', 'z', 'alpha', 'beta', 'segment', 'element']].to_numpy()

                # Write out PDB file
                # TODO add box to header
                np.savetxt(
                    buffer,
                    structure,
                    fmt=fmt,
                    header='CRYST1    0.000    0.000    0.000  90.00  90.00  90.00 P 1           1',
                    footer='END\n',
                    comments=''
                )

    # Convert to MDAnalysis Universe
    # mdanalysis.org
    def to_universe(self):
        pass

    # Update
    def update(self, xyz=None):
        if xyz is not None:
            if self.xyz.shape != xyz.shape:
                raise AttributeError('must be same shape')
            self.xyz = xyz

    # Wrap all
    def wrap_all(self, inplace=True):
        """
        Wraps all atoms in the selection to the unit cell.

        Parameters
        ----------
        inplace : bool
            Should the wrap happen in place? (Default: True)

        Returns
        -------
        Trajectory
        """

        # Wrap all atoms to the unit cell
        coord = self.coordinates
        box = self.box.rename(columns={'bx': 'x', 'by': 'y', 'bz': 'z'})
        cell = coord / box
        for col in cell.columns:
            cell[col] = cell[col].round()
        offset = box * cell
        coord_wrapped = coord - offset

        # Do in place or return a copy
        trajectory = self if inplace else self.copy()
        trajectory.coordinates = coord
        logger.info(f'wrapped all atoms of {trajectory.designator} to unit cell')
        if not inplace:
            return trajectory

    # View
    # https://github.com/arose/nglview
    def view(self):
        pass


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
        'atom_type',
        'residue',
        'chain',  # only available if read from PDB
        'residue_id',
        'alpha',  # only available if read from PDB
        'beta',  # only available if read from PDB
        'segment',
        'element',  # only available if read from PDB
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

        return self._data[item].to_numpy()

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
            return self._data[item].to_numpy()

        # Make sure that item a valid atom_id
        if item not in self._data['atom_id']:  # noqa
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

    # Trajectory designator
    @property
    def designator(self):
        return f'Topology:{self.hex_id}'

    # Hex ID
    @property
    def hex_id(self):
        return hex(id(self))

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

    # Infer elements from the Topology
    def infer_elements(self, overwrite=False, inplace=True):
        if not inplace:
            raise NotImplementedError

        # "Infer" from first letter of atom name; this will fail for two letter elements...
        # FIXME for 2 letter elements
        # TODO add warning for the fixme?
        elements = self._data['atom'].str.strip().str[0]
        logger.info(f'inferring missing elements from {self.designator} (overwrite = {overwrite})')
        if overwrite:
            self._data['element'] = elements
        else:
            mask = self._data['element'].isnull()
            self._data.loc[mask, 'element'] = elements[mask]

    def keys(self):
        return self._data.columns.to_numpy()

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
        indices = self._data.query(text).index.to_numpy()
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
        return data['residue'].to_numpy()

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

        return self._data[['x', 'y', 'z']].to_numpy()


def _dummy_trajectory_data(n_structures, n_atoms, n_dim):
    # Sanity
    if not isinstance(n_structures, int) or not isinstance(n_atoms, int) or not isinstance(n_dim, int):
        raise AttributeError(f'n_structures = {n_structures}; n_atoms = {n_atoms}; n_dim = {n_dim}')
    if n_dim != 3:
        raise AttributeError('can only process 3D information for now')

    # Turn record counts into arrays of indices
    structure_ids = np.arange(n_structures)
    atom_ids = np.arange(n_atoms)

    # Return
    return pd.DataFrame(index=pd.MultiIndex.from_product([structure_ids, atom_ids], names=['structure_id', 'atom_id']))


if __name__ == '__main__':
    import molecular as mol

    trj = mol.read_pdb('../tests/samples/trajectory.pdb')
