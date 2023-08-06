from molecular.geometry import dihedral
import numpy as np


# TODO make this work with multiple chains
def phi(a):
    residue_ids = np.unique(a.topology['residue_id'])
    if not np.all(np.diff(residue_ids) == 1):
        raise AttributeError('residue_id must be sequential: %s' % residue_ids)

    n_structures = a.n_structures
    n_dim = a.n_dim

    # Skip over the first residue_id
    for residue_id in residue_ids[1:]:
        residue0 = a.select(residue_id=residue_id - 1)
        residue1 = a.select(residue_id=residue_id)

        atom0 = residue0.select(atom='C').xyz.reshape(n_structures, n_dim)
        atom1 = residue1.select(atom='N').xyz.reshape(n_structures, n_dim)
        atom2 = residue1.select(atom='CA').xyz.reshape(n_structures, n_dim)
        atom3 = residue1.select(atom='C').xyz.reshape(n_structures, n_dim)

        return dihedral(atom0, atom1, atom2, atom3)
