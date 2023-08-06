"""
STRIDE----

ReadPDBFile
CheckChain

BackboneAngles
DiscrPhiPsi

PlaceHydrogens
FindHydrogenBonds
NoDoubleHBond

Helix
Sheet
BetaTurn
GammaTurn
Report"""

from . import backbone_dihedrals


def stride(trajectory):
    """

    Parameters
    ----------
    trajectory : Trajectory

    Returns
    -------

    """

    # Select protein
    protein = trajectory.query('protein')
    _check_protein_topology(protein.topology)

    # Compute backbone dihedral angles
    phi = backbone_dihedrals.phi(trajectory)
    psi = backbone_dihedrals.psi(trajectory)

    # Place hydrogen if necessary; let's skip with explicit solvent CHARMM structures

    # Compute hydrogen bonds


def _check_protein_topology(topology):
    """
    check chain step

    Parameters
    ----------
    a : Topology

    Returns
    -------

    """

    # Less than 5 residues?
    if topology.n_residues < 5:
        raise AttributeError('protein contains < 5 residues')


def _hydrogen_bonds(trajectory, distance_cutoff=6.):
    topology = trajectory.topology

    donors, hydrogens = _find_hydrogen_donors(topology)
    acceptors = _find_hydrogen_acceptors(topology)

    n_structures = trajectory.n_structures
    #TODO jit or cython or fortran
    distance = np.array([cdist(donors[i, :, :], acceptors[i, :, :]) for i in range(n_structures)])
    contact = distance <= distance_cutoff

    # energetic hydrogen bond


    # rose hydrogen bond

    # baker hydrogen bond

    #
    # if energetic bond and energy < 0 or rose or baker:
    #     flag as hydrogen bond


def _grid_energy(ca2, c, o, h, n):
    pass

def _identify_helix(trajectory):
    pass

def _find_hydrogen_donors(topology):
    """

    Parameters
    ----------
    trajectory

    Returns
    -------

    """

    donors = []
    hydrogens = []

    residue_ids = np.unique(topology['residue_id'])
    for i, residue_id in enumerate(residue_ids):
        residue = a.select(residue_id=residue_id)
        if i > 0:
            last_residue = a.select(residue_id=residue_id - 1)
            donors.append([
                _Atom(residue.select(atom='N')),
                _Atom(last_residue.select(atom='C')),
                _Atom(residue.select(atom='CA'))
            ])
        hydrogens.append(_Atom(residue.select(atom='H')))

        # there are specific residue hydrogen donors too


def _find_hydrogen_acceptors(topology):
    pass


class _Atom:
    def __init__(self, topology):
        if topology.n_atoms != 1:
            raise AttributeError('expecting 1 atom')
        self.topology = topology

