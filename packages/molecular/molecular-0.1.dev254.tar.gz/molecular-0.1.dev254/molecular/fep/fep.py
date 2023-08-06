import numpy as np
import pandas as pd


class Residue:
    """

    """

    # This should just be a dataframe
    def __init__(self, name, charge):
        self._name = name
        self._charge = charge
        self._atoms = pd.DataFrame(columns=['group', 'name', 'kind', 'charge', 'comment'])
        self._bonds = pd.DataFrame(columns=['name0', 'name1'])
        self._impropers = pd.DataFrame(columns=['name0', 'name1', 'name2', 'name3'])

    @property
    def atoms(self):
        return self._atoms

    @property
    def bonds(self):
        return self._bonds

    @property
    def impropers(self):
        return self._impropers

    def add_atom(self, group, name, kind, charge, comment=''):
        self._atoms.loc[len(self._atoms)] = {
            'group': group,
            'name': name,
            'kind': kind,
            'charge': charge,
            'comment': comment
        }

    def add_bond(self, name0, name1):
        self._bonds.loc[len(self._bonds)] = {
            'name0': name0,
            'name1': name1
        }

    def add_improper(self, name0, name1, name2, name3):
        self._impropers.loc[len(self._impropers)] = {
            'name0': name0,
            'name1': name1,
            'name2': name2,
            'name3': name3
        }

    def compare_atoms(self, other):
        self_atoms = self.atoms.drop(columns='comment')
        other_atoms = other.atoms.drop(columns='comment')
        return self_atoms.merge(other_atoms, how='outer', indicator=True)

    def compare_bonds(self, other):
        bonds = self.bonds.merge(other.bonds, how='outer', indicator=True)
        return bonds

    def compare_impropers(self, other):
        return self.impropers.merge(other.impropers, how='outer', indicator=True)

    def copy(self):
        copy = Residue(name=self._name, charge=self._charge)
        copy._atoms = self._atoms.copy()
        copy._bonds = self._bonds.copy()
        copy._impropers = self._impropers.copy()
        return copy

    def find_bonds(self, names):
        bonds = self.bonds[np.max(np.isin(self._bonds, names), axis=1)]
        unique_bonds = np.unique(bonds.to_numpy().ravel())
        mask = ~np.isin(unique_bonds, names)
        return unique_bonds[mask]

    # Rename atom names in Residue
    def rename(self, old_to_new):
        """
        Rename atom names in this Residue. This includes ATOM information and BOND/IMPR information.

        Parameters
        ----------
        old_to_new : dict
            Old name is the key, new name is the value.
        """

        # Loop over all key/value pairs provided
        for old_name, new_name in old_to_new.items():
            # First check that new_name isn't already in the molecule
            if new_name in self.atoms['name']:
                raise AttributeError(f'cannot rename {old_name} to {new_name} because it already exists')

            # Make the change with atoms
            self.atoms.loc[self.atoms['name'] == old_name, 'name'] = new_name

            # Make the change with bonds
            self.bonds.loc[self.bonds['name0'] == old_name, 'name0'] = new_name
            self.bonds.loc[self.bonds['name1'] == old_name, 'name1'] = new_name

            # Make the change with impropers
            self.impropers.loc[self.impropers['name0'] == old_name, 'name0'] = new_name
            self.impropers.loc[self.impropers['name1'] == old_name, 'name1'] = new_name
            self.impropers.loc[self.impropers['name2'] == old_name, 'name2'] = new_name
            self.impropers.loc[self.impropers['name3'] == old_name, 'name3'] = new_name

    # Sort bonds
    def sort_bonds(self):
        # For convenience
        bonds = self.bonds

        # First, correct "order of order" bonds. Note that hydrogens are not sorted this way
        out_of_order = (bonds['name0'].str[0] == 'H') | \
                       ((bonds['name0'] > bonds['name1']) & (bonds['name1'].str[0] != 'H'))
        bonds['temp'] = bonds['name0']
        bonds.loc[out_of_order, 'name0'] = bonds.loc[out_of_order, 'name1']
        bonds.loc[out_of_order, 'name1'] = bonds.loc[out_of_order, 'temp']

        # Second, sort within DataFrame
        bonds['has_hydrogen'] = bonds['name1'].str[0] == 'H'
        bonds.sort_values(['has_hydrogen', 'name0', 'name1'], inplace=True)

        # Drop temp columns and reset index
        bonds.drop(columns=['temp', 'has_hydrogen'], inplace=True)
        bonds.reset_index(drop=True, inplace=True)


class Parameters:
    def __init__(self):
        self._bonds = pd.DataFrame(columns=['kind0', 'kind1', 'u', 'r', 'comment'])
        self._angles = pd.DataFrame(columns=['kind0', 'kind1', 'kind2', 'u', 'r', 'comment'])
        self._dihedrals = pd.DataFrame(columns=['kind0', 'kind1', 'kind2', 'kind3', 'u', 'n', 'r', 'comment'])

    @property
    def angles(self):
        return self._angles

    @property
    def bonds(self):
        return self._bonds

    @property
    def dihedrals(self):
        return self._dihedrals

    def add_angle(self, kind0, kind1, kind2, u, r, comment=''):
        self._angles.loc[len(self._angles)] = {
            'kind0': kind0,
            'kind1': kind1,
            'kind2': kind2,
            'u': u,
            'r': r,
            'comment': comment
        }

    def add_bond(self, kind0, kind1, u, r, comment=''):
        self._bonds.loc[len(self._bonds)] = {
            'kind0': kind0,
            'kind1': kind1,
            'u': u,
            'r': r,
            'comment': comment
        }

    def add_dihedral(self, kind0, kind1, kind2, kind3, u, n, r, comment=''):
        self._dihedrals.loc[len(self._dihedrals)] = {
            'kind0': kind0,
            'kind1': kind1,
            'kind2': kind2,
            'kind3': kind3,
            'u': u,
            'n': n,
            'r': r,
            'comment': comment
        }

    def copy(self):
        params = Parameters()
        params._bonds = self._bonds.copy()
        params._angles = self._angles.copy()
        params._dihedrals = self._dihedrals.copy()
        return params

    def merge(self, other):
        # Create new parameter set
        params = Parameters()

        # Bonds
        params._bonds = pd.concat([self.bonds, other.bonds], ignore_index=True).drop_duplicates()  # noqa
        params._bonds['has_hydrogen0'] = params._bonds['kind0'].str[0] == 'H'
        params._bonds['has_hydrogen1'] = params._bonds['kind1'].str[0] == 'H'
        params._bonds.sort_values(['has_hydrogen0', 'kind0', 'has_hydrogen1', 'kind1'], inplace=True)
        params._bonds.drop(columns=['has_hydrogen0', 'has_hydrogen1'], inplace=True)
        params._bonds.reset_index(drop=True, inplace=True)  # noqa

        # Angles
        params._angles = pd.concat([self.angles, other.angles], ignore_index=True).drop_duplicates()
        params._angles['has_hydrogen0'] = params._angles['kind0'].str[0] == 'H'
        params._angles['has_hydrogen1'] = params._angles['kind1'].str[0] == 'H'
        params._angles['has_hydrogen2'] = params._angles['kind2'].str[0] == 'H'
        params._angles.sort_values(['has_hydrogen0', 'kind0', 'has_hydrogen1', 'kind1', 'has_hydrogen2', 'kind2'],
                                   inplace=True)
        params._angles.drop(columns=['has_hydrogen0', 'has_hydrogen1', 'has_hydrogen2'], inplace=True)
        params._angles.reset_index(drop=True, inplace=True)  # noqa

        # Dihedrals
        params._dihedrals = pd.concat([self.dihedrals, other.dihedrals], ignore_index=True).drop_duplicates()
        params._dihedrals['has_hydrogen0'] = params._dihedrals['kind0'].str[0] == 'H'
        params._dihedrals['has_hydrogen1'] = params._dihedrals['kind1'].str[0] == 'H'
        params._dihedrals['has_hydrogen2'] = params._dihedrals['kind2'].str[0] == 'H'
        params._dihedrals['has_hydrogen3'] = params._dihedrals['kind3'].str[0] == 'H'
        params._dihedrals.sort_values \
            (['has_hydrogen0', 'kind0', 'has_hydrogen1', 'kind1', 'has_hydrogen2', 'kind2', 'has_hydrogen3', 'kind3',
              'n'], inplace=True)
        params._dihedrals.drop(columns=['has_hydrogen0', 'has_hydrogen1', 'has_hydrogen2', 'has_hydrogen3'],
                               inplace=True)
        params._dihedrals.reset_index(drop=True, inplace=True)

        # Return
        return params


class Stream:
    def __init__(self, fname=None):
        self._fname = fname
        self._header_rtf = ''
        self._header_prm = ''
        self._residue = None
        self._params = Parameters()

    @property
    def params(self):
        return self._params

    @property
    def residue(self):
        return self._residue

    # Create a copy of Stream object
    def copy(self):
        """
        Create a copy of the Stream object.
        """

        copy = Stream(self._fname)
        copy._header_rtf = self._header_rtf
        copy._header_prm = self._header_prm
        copy._residue = self._residue.copy()
        copy._params = self._params.copy()
        return copy

    def compare(self, other, errors='raise'):
        return self.equals(other, errors=errors)

    def equals(self, other, ignore_order=False, errors='raise'):
        # Are all atoms accounted for?
        diff_atoms = self.residue.compare_atoms(other.residue).query('_merge != "both"')
        if len(diff_atoms) != 0:
            if 'raise' in errors:
                raise AttributeError(diff_atoms)
            return False

        # Is the order of atoms the same?
        # noinspection PyUnresolvedReferences
        if not ignore_order and (self.residue.atoms['name'].to_numpy() != other.residue.atoms['name'].to_numpy()).any():
            return False

        # Are all bonds accounted for?
        self.residue.sort_bonds()
        other.residue.sort_bonds()
        diff_bonds = self.residue.compare_bonds(other.residue).query('_merge != "both"')
        if len(diff_bonds) != 0:
            if 'raise' in errors:
                raise AttributeError(diff_bonds)
            return False

        # Are all impropers accounted for?
        diff_imprs = self.residue.compare_impropers(other.residue).query('_merge != "both"')
        if len(diff_imprs) != 0:
            if 'raise' in errors:
                raise AttributeError(diff_imprs)
            return False

        # Are all bond parameters accounted for?
        self_bonds = self.params.bonds.drop(columns='comment')
        other_bonds = other.params.bonds.drop(columns='comment')
        diff_bonds = self_bonds.merge(other_bonds, how='outer', indicator=True).query('_merge != "both"')
        if len(diff_bonds) != 0:
            if 'raise' in errors:
                raise AttributeError(diff_bonds)
            return False

        # Are all angle parameters accounted for?
        self_angles = self.params.angles.drop(columns='comment')
        other_angles = other.params.angles.drop(columns='comment')
        diff_angles = self_angles.merge(other_angles, how='outer', indicator=True).query('_merge != "both"')
        if len(diff_angles) != 0:
            if 'raise' in errors:
                raise AttributeError(diff_angles)
            return False

        # Are all dihedral parameters accounted for?
        self_dihedrals = self.params.dihedrals.drop(columns='comment')
        other_dihedrals = other.params.dihedrals.drop(columns='comment')
        diff_dihedrals = self_dihedrals.merge(other_dihedrals, how='outer', indicator=True).query('_merge != "both"')
        if len(diff_dihedrals) != 0:
            if 'raise' in errors:
                raise AttributeError(diff_dihedrals)
            return False

        # Otherwise, return True
        return True

    def to_stream(self, fname):
        # Save
        with open(fname, 'w') as buf:
            buf.write(self._header_rtf)
            buf.write('RESI %-4s          %6s\n' % (self.residue._name, self.residue._charge))
            for group in self.residue.atoms['group'].unique():
                buf.write('GROUP\n')
                atoms = self.residue.atoms.query('group == %s' % group).copy()
                atoms['label'] = 'ATOM'
                # atoms[['label', 'name', 'kind', 'charge']].to_csv(buf, sep=' ', index=False, header=None)
                np.savetxt(buf, atoms[['label', 'name', 'kind', 'charge', 'comment']], fmt='%s %-6s %-6s %6s %s')
            buf.write('\n')
            bonds = self.residue.bonds.copy()
            bonds['label'] = 'BOND'
            # bonds[['label', 'name0', 'name1']].to_csv(buf, sep=' ', index=False, header=None)
            np.savetxt(buf, bonds[['label', 'name0', 'name1']], fmt='%s %-4s %-4s')
            buf.write('\n')
            imprs = self.residue.impropers.copy()
            imprs['label'] = 'IMPR'
            # imprs[['label', 'name0', 'name1', 'name2', 'name3']].to_csv(buf, sep=' ', index=False, header=None)
            np.savetxt(buf, imprs[['label', 'name0', 'name1', 'name2', 'name3']], fmt='%s %-6s %-6s %-6s %-6s')
            buf.write('\nEND\n')
            buf.write(self._header_prm)
            params = self.params.copy()
            buf.write('BONDS\n')
            # params.bonds[['kind0', 'kind1', 'u', 'r']].to_csv(buf, sep=' ', index=False, header=None)
            np.savetxt(buf, params.bonds[['kind0', 'kind1', 'u', 'r', 'comment']], fmt='%-6s %-6s %7s %10s %s')
            buf.write('\n')
            buf.write('ANGLES\n')
            # params.angles[['kind0', 'kind1', 'kind2', 'u', 'r']].to_csv(buf, sep=' ', index=False, header=None)
            np.savetxt(buf, params.angles[['kind0', 'kind1', 'kind2', 'u', 'r', 'comment']],
                       fmt='%-6s %-6s %-6s %7s %9s %s')
            buf.write('\n')
            buf.write('DIHEDRALS\n')
            # params.dihedrals[['kind0', 'kind1', 'kind2', 'kind3', 'u', 'n', 'r']].to_csv(buf, sep=' ', index=False, header=None)
            np.savetxt(buf, params.dihedrals[['kind0', 'kind1', 'kind2', 'kind3', 'u', 'n', 'r', 'comment']],
                       fmt='%-6s %-6s %-6s %-6s %10s %2s %8s %s')
            buf.write('\n')
            buf.write('IMPROPERS\n\nEND\nRETURN\n')


# Read stream file
# TODO move this to Cython
def read_stream(fname, sort=True):
    # Create object to store stream file data
    stream = Stream(fname)

    # Open stream file and read
    with open(fname, 'r') as buffer:
        # Start off in RTF header mode
        mode = 'header_rtf'

        # Loop over all lines
        for line in buffer.readlines():
            # Separate our lines into words surrounded by whitespace
            words = line.split()

            # Pick out the in-line comment, if it exists
            i = line.find('!')
            comment = line[i:].rstrip() if i >= 0 else ''

            # If the line is empty or we are not in header mode and find a comment, then skip
            if 'header' not in mode and (len(words) == 0 or words[0][0] == '!'):
                continue

            # Section 1 : header_rtf
            if mode == 'header_rtf' and (len(words) == 0 or words[0].lower() != 'resi'):
                stream._header_rtf += line

            # Section 2 : residue
            elif mode == 'header_rtf' and words[0].lower() == 'resi':
                mode = 'residue'
                group = -1
                stream._residue = Residue(words[1], words[2])

            elif mode == 'residue':
                if words[0].lower() == 'group':
                    group += 1
                elif words[0].lower() == 'atom':
                    stream._residue.add_atom(
                        group,
                        words[1],
                        words[2],
                        words[3],
                        # comment
                    )
                elif words[0].lower() == 'bond':
                    stream._residue.add_bond(
                        words[1],
                        words[2]
                    )
                elif words[0].lower() == 'impr':
                    stream._residue.add_improper(
                        words[1],
                        words[2],
                        words[3],
                        words[4]
                    )
                elif words[0].lower() == 'end':
                    mode = 'header_prm'
                else:
                    raise AttributeError('unexpected: %s' % line)

            # Section 3 : header_prm
            elif mode == 'header_prm' and (len(words) == 0 or words[0].lower() != 'bonds'):
                stream._header_prm += line

            # Section 4 : bonds
            elif mode == 'header_prm' and words[0].lower() == 'bonds':
                mode = 'bonds'

            elif mode == 'bonds' and words[0].lower() != 'angles':
                stream._params.add_bond(
                    words[0],
                    words[1],
                    words[2],
                    words[3],
                    comment
                )

            # Section 5 : angles
            elif mode == 'bonds' and words[0].lower() == 'angles':
                mode = 'angles'

            elif mode == 'angles' and words[0].lower() != 'dihedrals':
                stream._params.add_angle(
                    words[0],
                    words[1],
                    words[2],
                    words[3],
                    words[4],
                    comment
                )

            # Section 6 : dihedrals
            elif mode == 'angles' and words[0].lower() == 'dihedrals':
                mode = 'dihedrals'

            elif mode == 'dihedrals' and words[0].lower() != 'impropers':
                if len(words) > 7 and words[7][0] != '!':
                    raise AttributeError('unexpected: %s' % line)
                stream._params.add_dihedral(
                    words[0],
                    words[1],
                    words[2],
                    words[3],
                    words[4],
                    words[5],
                    words[6],
                    comment
                )

            # Section 7 : impropers
            elif mode == 'dihedrals' and words[0].lower() == 'impropers':
                mode = 'impropers'

            elif mode == 'impropers' and words[0].lower() not in ['end', 'return']:
                raise AttributeError('unexpected: %s' % line)

    # Sort?
    if sort:
        stream.residue.sort_bonds()

    # Return
    return stream


# Create DualStream object
# TODO name_map currently needs to be hand-mapped but in the future this could be automated
def create_dual_stream(wt, mt, name_map):
    """
    Create a dual topology Stream

    `name_map` is a dictionary that contains all atoms that change between WT and MT. If the atom name is the same in WT
    and MT, the expectation is that we will give the MT version a new name. If the atom is present in WT but not in MT,
    then it gets a value of None. If the atom is present in MT but not WT, we can keep its name.
    # First off, this is a list of all modified atoms.
    # Second, this tells us how to order modified atoms in the new dual stream and what to name them as.
    # If key and value are both values but different, this is what will be copied from WT to dual
    # If key and value are the same, this is an introduced atom in MT
    # If key is defined but value is None, then this is an atom that is removed in WT


    Parameters
    ----------
    wt : Stream
        Reference wild-type (wt) stream file
    mt : Stream
        Updated mutant (mt) stream file
    name_map : dict
        Dictionary that maps changed atom names in the current `wt` and `mt` stream files to the new combined file.

    Returns
    -------
    DualStream
    """

    # I'm not settled on this DualStream class, would it be better just to add new variables to Stream?
    return DualStream(wt, mt, name_map)


# Decompose Stream into wild-type and mutant
def decompose_dual_stream(ds, flags):
    """
    Decompose a Steam object into wild-type and mutant Stream objects.

    Parameters
    ----------
    ds : Stream
    flags : numpy.ndarray
        Follows NAMD-style where "0" represents common atom, "-1" represents wild-type atom, and "1" represent mutant
        atom.

    Returns
    -------
    Stream, Stream
        Wild-type and mutant Stream objects
    """

    # First, create copies of the Stream object fot wt and mt
    wt = ds.copy()
    mt = ds.copy()

    # Second, drop Residue info where flag False
    wt.residue._atoms = wt.residue.atoms[flags < 1].copy()
    mt.residue._atoms = mt.residue.atoms[flags > -1].copy()

    wt_atoms = wt.residue.atoms['name'].to_numpy()  # get atom names that are left
    mt_atoms = mt.residue.atoms['name'].to_numpy()

    wt.residue._bonds = wt.residue.bonds[
        (wt.residue.bonds['name0'].isin(wt_atoms)) & (wt.residue.bonds['name1'].isin(wt_atoms))]
    mt.residue._bonds = mt.residue.bonds[
        (mt.residue.bonds['name0'].isin(mt_atoms)) & (mt.residue.bonds['name1'].isin(mt_atoms))]

    wt.residue._impropers = wt.residue.impropers[
        (wt.residue.impropers['name0'].isin(wt_atoms)) & (wt.residue.impropers['name1'].isin(wt_atoms)) & (
            wt.residue.impropers['name2'].isin(wt_atoms)) & (wt.residue.impropers['name3'].isin(wt_atoms))]
    mt.residue._impropers = mt.residue.impropers[
        (mt.residue.impropers['name0'].isin(mt_atoms)) & (mt.residue.impropers['name1'].isin(mt_atoms)) & (
            mt.residue.impropers['name2'].isin(mt_atoms)) & (mt.residue.impropers['name3'].isin(mt_atoms))]

    # Third, drop Parameters where flag False
    wt_kinds = wt.residue.atoms['kind'].to_numpy()
    mt_kinds = mt.residue.atoms['kind'].to_numpy()

    wt.params._bonds = wt.params.bonds[
        (wt.params.bonds['kind0'].isin(wt_kinds)) & (wt.params.bonds['kind1'].isin(wt_kinds))]
    mt.params._bonds = mt.params.bonds[
        (mt.params.bonds['kind0'].isin(mt_kinds)) & (mt.params.bonds['kind1'].isin(mt_kinds))]

    wt.params._angles = wt.params.angles[
        (wt.params.angles['kind0'].isin(wt_kinds)) & (wt.params.angles['kind1'].isin(wt_kinds)) & (
            wt.params.angles['kind2'].isin(wt_kinds))]
    mt.params._angles = mt.params.angles[
        (mt.params.angles['kind0'].isin(mt_kinds)) & (mt.params.angles['kind1'].isin(mt_kinds)) & (
            mt.params.angles['kind2'].isin(mt_kinds))]

    wt.params._dihedrals = wt.params.dihedrals[
        (wt.params.dihedrals['kind0'].isin(wt_kinds)) & (wt.params.dihedrals['kind1'].isin(wt_kinds)) & (
            wt.params.dihedrals['kind2'].isin(wt_kinds)) & (wt.params.dihedrals['kind3'].isin(wt_kinds))]
    mt.params._dihedrals = mt.params.dihedrals[
        (mt.params.dihedrals['kind0'].isin(mt_kinds)) & (mt.params.dihedrals['kind1'].isin(mt_kinds)) & (
            mt.params.dihedrals['kind2'].isin(mt_kinds)) & (mt.params.dihedrals['kind3'].isin(mt_kinds))]

    # Return
    return wt, mt


# Subclass of Stream to hold dual topology streams
# TODO evaluate if this is worth it. Stream could also be used for this.
class DualStream(Stream):
    def __init__(self, wt, mt, name_map):
        # Create pointers to wt and mt Stream objects
        self._wt = wt
        self._mt = mt

        # Store name map
        self._name_map = name_map

        # Initialize this instance
        super().__init__()

        # Get mod atoms
        self._compute_mod_atoms()

        # Merge streams
        self._merge_streams()

    def _compute_mod_atoms(self):
        # For convenience
        wt = self._wt
        mt = self._mt
        name_map = self._name_map

        # Find atoms that were modified
        _mod_atoms = wt.residue.compare_atoms(mt.residue).query('_merge != "both"')['name'].unique()

        # Find hanging atoms attached to modified
        _mod_atoms_new = []
        for atom0 in _mod_atoms:
            for atom1 in wt.residue.find_bonds(atom0):
                if atom0 == atom1:
                    continue
                if len(wt.residue.find_bonds(atom1)) == 1:
                    _mod_atoms_new.append(atom1)
            for atom1 in mt.residue.find_bonds(atom0):
                if atom0 == atom1:
                    continue
                if len(mt.residue.find_bonds(atom1)) == 1:
                    _mod_atoms_new.append(atom1)
        mod_atoms = np.unique(np.hstack([_mod_atoms, np.array(_mod_atoms_new)]))

        # Mod atom sanity check; make sure that all names are accounted for
        for atom in mod_atoms:
            if atom not in name_map.keys():
                raise AttributeError('%s not found in names' % atom)
        for atom in name_map.keys():
            if atom not in mod_atoms:
                raise AttributeError('%s not found in mod_atoms' % atom)
        for atom in name_map.values():
            if atom in wt.residue.atoms['name']:
                raise AttributeError('%s in WT atoms already' % atom)

        # Save
        self._mod_atoms = mod_atoms

    #
    def _merge_streams(self):
        # For convenience
        wt = self._wt
        mt = self._mt
        name_map = self._name_map

        # Save header information
        self._header_rtf = wt._header_rtf
        self._header_prm = wt._header_prm

        # Build dual topology file
        residue = wt.residue.copy()
        for old_name, new_name in name_map.items():
            if new_name is None:
                continue
            atom = mt.residue.atoms.query('name == "%s"' % old_name)
            assert len(atom) == 1, old_name
            atom = atom.iloc[0]
            residue.add_atom(
                group=atom.group,
                name=new_name,
                kind=atom.kind,
                charge=atom.charge,
                comment=atom.comment
            )
            for _bond in mt.residue.find_bonds(old_name):
                bond = name_map.get(_bond, _bond)
                if (residue.find_bonds(new_name) == bond).any():  # noqa
                    continue
                residue.add_bond(
                    name0=new_name,
                    name1=bond
                )
            for _, _impr in mt.residue.impropers[np.max(np.isin(mt.residue.impropers, old_name), axis=1)].iterrows():
                impr = {}
                for key, value in _impr.items():
                    impr[key] = name_map.get(value, value)
                if (residue.impropers == impr).min(axis=1).sum() == 0:
                    residue.add_improper(
                        name0=impr['name0'],
                        name1=impr['name1'],
                        name2=impr['name2'],
                        name3=impr['name3']
                    )

        # Annotate dual topology
        wt_atoms = wt.residue.atoms['name'].to_numpy()
        mt_atoms = mt.residue.atoms['name'].to_numpy()
        for i, atom in enumerate(residue.atoms['name'].to_numpy()):
            in_wt = atom in wt_atoms
            in_mt = atom in mt_atoms
            lam = 0
            if (in_wt and not in_mt) or ((atom in name_map.keys()) and (atom not in name_map.values())):
                lam = -1
            elif (not in_wt and in_mt) or (atom in name_map.values()):
                lam = 1
            residue.atoms.loc[i, 'comment'] = residue.atoms.loc[i, 'comment'] + '! lam= %2s' % lam

        for old_name, new_name in name_map.items():
            mask = residue.atoms['name'] == new_name
            residue.atoms.loc[mask, 'comment'] = residue.atoms.loc[mask, 'comment'] + ', from %s (%s)' % (old_name,
                                                                                                          mt._fname)

        # Build dual parameters
        params = wt.params.merge(mt.params)

        # Save
        self._residue = residue
        self._params = params
