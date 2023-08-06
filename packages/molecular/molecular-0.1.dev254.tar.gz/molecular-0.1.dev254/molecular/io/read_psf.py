
from io import StringIO
import numpy as np
import pandas as pd


class PSF:  # this should probably be a child of Topology
    def __init__(self, atoms, bonds):
        self._atoms = atoms
        self._bonds = bonds

    def __repr__(self):
        return self._atoms.to_markdown()

    def _repr_html_(self):
        return self._atoms.to_html(max_rows=10)


def read_psf(fname):
    # Sections
    sections = {}
    counts = {}

    # Read in entire file first
    with open(fname, 'r') as buf:
        section = None
        n_remaining = 0

        # Read file taking out the good bits
        for line in buf:
            # Read section
            if section is not None and n_remaining > 0:
                sections[section] += line
                if section in ['!NTITLE', '!NATOM']:
                    n_remaining -= 1
                elif section == '!NBOND':  # at most 4 bonds per line
                    n_remaining -= 4

                # If we hit 0 (or fewer), we are done
                if n_remaining <= 0:
                    section = None

                    # Otherwise, figure out if a section is starting
            if section is None:
                data = line.strip().split()
                if len(data) > 1 and data[1] in ['!NTITLE', '!NATOM', '!NBOND:']:
                    section = data[1].replace(':', '')
                    sections[section] = ''
                    counts[section] = int(data[0])
                    n_remaining = int(data[0])

                    # Process
    atoms = pd.read_table(
        StringIO(sections['!NATOM']),
        sep='\s+',
        header=None,
        names=[
            'atom_id',
            'segment',
            'residue_id',
            'residue',
            'atom',
            'atom_type',
            'charge',
            'mass',
            'unused'
        ]
    )
    atoms.index.name = 'index'

    bonds = pd.DataFrame(
        np.array(np.array_split(sections['!NBOND'].split(), counts['!NBOND']), dtype='int'),
        columns=[
            'atom_id0',
            'atom_id1'
        ]
    )

    # Sanity
    assert len(atoms) == counts['!NATOM']
    assert len(bonds) == counts['!NBOND']

    # Return
    return PSF(
        atoms=atoms,
        bonds=bonds
    )