"""
rtf.py

description: Read RTF from CHARMM format.
language: Python 3.x
author: C. Lockhart <chris@lockhartlab.org>
"""

"""
Topology
Trajectory

ForceField
"""


class ForceField:
    def __init__(self):
        # self.atom_types = {}
        self.residues = {}

    def __setitem__(self, key, value):
        self.residues[key] = value

    def __getitem__(self, item):
        return self.residues[item]


class Residue:
    def __init__(self, name, charge):
        self.name = str(name)
        self.charge = float(charge)
        self.atoms = {}
        self.bonds = []
        self.angles = []
        self.dihedrals = []
        self.impropers = []
        self.crossterms = []
        self.donors = []
        self.acceptors = []

    def __add__(self, atom):
        assert isinstance(atom, Atom)
        self.atoms.append(atom)
        return self

    def __repr__(self):
        s = 'ATOM    MASS    CHARGE\n'
        for atom_name, atom in self.atoms.items():
            s += f'{atom_name} {atom.mass} {atom.charge}\n'
        return s


class Patch:
    def __init__(self):
        pass


class Atom:
    # noinspection PyShadowingBuiltins
    def __init__(self, type, charge, mass):
        self.type = type
        self.charge = charge
        self.mass = mass


def read_rtf(fname, debug=False):
    """

    Parameters
    ----------
    fname

    Returns
    -------

    """

    # Read in file
    with open(fname, 'r') as stream:
        data = stream.readlines()
        # if debug:
        #     print(data)

    # Create empty ForceField
    forcefield = ForceField()

    #
    mass = {}

    # Read line-by-line
    section = 0
    for line in data:
        # print(line)
        # Skip lines with comments or blank
        if line[0] == '!' or line == '':
            continue

        # If line starts with an asterisk, print it out
        if line[0] == '*':
            print(line.strip())
            continue

        # The first line whose first character without an asterisk tells us we're ready to start
        if section == 0 and line[0] != '*':
            section = 1

        # Expect to read force field version number
        if section == 1:
            print(line.strip())
            section = 2
            continue

        # Divide line into columns
        col = line.split('!')[0].split()
        columns = col

        # If we have no columns, skip
        if len(columns) == 0:
            continue

        # Read MASS section
        if section == 2 and columns[0] == 'MASS':
            assert len(columns) >= 4
            atom_type = columns[2]
            mass[atom_type] = float(col[3].split('!')[0])
            continue
        elif section == 2 and columns[0] != 'MASS':
            section = 3

        # Read RESI section
        if section == 3 and line[:4] == 'RESI':
            residue_name = col[1]
            residue_charge = col[2].split('!')[0]
            forcefield.residues[residue_name] = Residue(name=residue_name, charge=residue_charge)
            continue
        elif section == 3 and line[:4] == 'ATOM':
            atom_name = col[1]
            atom_type = col[2]
            atom_charge = col[3].split('!')[0]
            atom_mass = mass.get(atom_type, 0.)
            # if atom_type not in forcefield.atom_types:
            #     forcefield.atom_types[atom_type] = Atom(type=atom_type, charge=atom_charge, mass=atom_mass)
            # noinspection PyUnboundLocalVariable
            # forcefield.residues[residue_name].atoms[atom_name] = forcefield.atom_types[atom_type]
            forcefield.residues[residue_name].atoms[atom_name] = Atom(type=atom_type, charge=atom_charge,
                                                                      mass=atom_mass)
            continue
        elif section == 3 and (line[:4] in ['BOND', 'DOUB', 'TRIP']):
            bond_type = 'bond'
            if line[:4] == 'DOUB':
                bond_type = 'double'
            elif line[:4] == 'TRIP':
                bond_type = 'triple'
            for i in range(1, len(col), 2):
                atom_name0 = col[i].split('!')[0]
                atom_name1 = col[i + 1].split('!')[0]
                forcefield.residues[residue_name].bonds.append([atom_name0, atom_name1, bond_type])
        elif section == 3 and line[:4] == 'ANGL':
            for i in range(1, len(col), 3):
                atom_name0 = col[i].split('!')[0]
                atom_name1 = col[i + 1].split('!')[0]
                atom_name2 = col[i + 2].split('!')[0]
                forcefield.residues[residue_name].angles.append([atom_name0, atom_name1, atom_name2])
        elif section == 3 and line[:4] == 'DIHE':
            for i in range(1, len(col), 4):
                atom_name0 = col[i].split('!')[0]
                atom_name1 = col[i + 1].split('!')[0]
                atom_name2 = col[i + 2].split('!')[0]
                atom_name3 = col[i + 3].split('!')[0]
                forcefield.residues[residue_name].dihedrals.append([atom_name0, atom_name1, atom_name2, atom_name3])
        elif section == 3 and line[:4] == 'IMPR':
            for i in range(1, len(col), 4):
                atom_name0 = col[i].split('!')[0]
                atom_name1 = col[i + 1].split('!')[0]
                atom_name2 = col[i + 2].split('!')[0]
                atom_name3 = col[i + 3].split('!')[0]
                forcefield.residues[residue_name].impropers.append([atom_name0, atom_name1, atom_name2, atom_name3])
        elif section == 3 and line[:4] == 'CMAP':
            for i in range(1, len(col), 8):
                atom_name0 = col[i].split('!')[0]
                atom_name1 = col[i + 1].split('!')[0]
                atom_name2 = col[i + 2].split('!')[0]
                atom_name3 = col[i + 3].split('!')[0]
                atom_name4 = col[i + 4].split('!')[0]
                atom_name5 = col[i + 5].split('!')[0]
                atom_name6 = col[i + 6].split('!')[0]
                atom_name7 = col[i + 7].split('!')[0]
                forcefield.residues[residue_name].crossterms.append([atom_name0, atom_name1, atom_name2, atom_name3,
                                                                     atom_name4, atom_name5, atom_name6, atom_name7])
        elif section == 3 and line[:4] == 'DONO':
            for i in range(1, len(col), 1):
                atom_name = col[i].split('!')[0]
                forcefield.residues[residue_name].donors.append(atom_name)
        elif section == 3 and line[:4] == 'ACCE':
            for i in range(1, len(col), 1):
                atom_name = col[i].split('!')[0]
                forcefield.residues[residue_name].acceptors.append(atom_name)

        # TODO read PRES section

    # We're done
    return forcefield


if __name__ == '__main__':
    import os

    include_dir = os.path.abspath(os.path.join(__file__, '../../../samples'))

    rtf = read_rtf(os.path.join(include_dir, 'top_all27_prot_lipid.inp'), debug=True)




