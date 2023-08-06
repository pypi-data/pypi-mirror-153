"""
sequence.py

>>> abeta = Protein('YEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV')
"""

import pandas as pd
from typelike import ArrayLike


class Residue:
    def __init__(self):
        pass


class AminoAcid(Residue):
    _defaults = pd.DataFrame([
        ['ALA', 'A', 0],
        ['CYS', 'C', 0],
        ['ASP', 'D', -1],
        ['GLU', 'E', -1],
        ['PHE', 'F', 0],
        ['GLY', 'G', 0],
        ['HIS', 'H', 0],
        ['ILE', 'I', 0],
        ['LYS', 'K', 1],
        ['LEU', 'L', 0],
        ['MET', 'M', 0],
        ['ASN', 'N', 0],
        ['PRO', 'P', 0],
        ['GLN', 'Q', 0],
        ['ARG', 'R', 1],
        ['SER', 'S', 0],
        ['THR', 'T', 0],
        ['VAL', 'V', 0],
        ['TRP', 'W', 0],
        ['TYR', 'Y', 0],
    ], columns=['name', 'code', 'charge'])

    def __init__(self, name, code, charge):
        super().__init__()
        self._name = name
        self._code = code
        self._charge = charge

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code


def _get_amino_acid(name=None, code=None):
    if name is None and code is None:
        raise AttributeError('must specify name or code')

    name = name.upper()
    code = code.upper()

    _code_to_name = {
        'A': 'ALA',
        'C': 'CYS',
        'D': 'ASP',
        'E': 'GLU',
        'F': 'PHE',
        'G': 'GLY',
        'H': 'HIS',
        'I': 'ILE',
        'K': 'LYS',
        'L': 'LEu',
        'M': 'MET',
        'N': 'ASN',
        'P': 'PRO',
        'Q': 'GLN',
        'R': 'ARG',
        'S': 'SER',
        'T': 'THR',
        'V': 'VAL',
        'W': 'TRP',
        'Y': 'TYR'
    }

    _name_to_code = {name: code for code, name in _code_to_name.items()}

    if code is not None:
        name = _code_to_name[code]
    else:
        code = _name_to_code[name]

    return AminoAcid(name, code, 0.)


class Sequence:
    def __init__(self):
        pass


class Protein(Sequence):
    """
    Construct for dealing with protein sequences.
    """

    def __init__(self, sequence, ):
        """
        Initialize Protein object.

        Parameters
        ----------
        sequence : np.ndarray
            List of residues.
        """

        # Convert to list if not already list
        # super().__init__()
        # if not isinstance(sequence, ArrayLike):
        if isinstance(sequence, str):
            sequence = list(sequence)

        # Which format are these residues in?
        len_sequence = len(sequence[0])
        if len_sequence == 1:
            sequence = _letter_to_code(sequence)
        elif len_sequence != 3:
            raise AttributeError('must supply residue triplets')

        # Save
        self.sequence = sequence

    def __repr__(self):
        return str(self.sequence)

    def to_letters(self, join=False):
        code_to_letter = {
            'ALA': 'A',
            'ARG': 'R',
            'ASN': 'N',
            'ASP': 'D',
            'CYS': 'C',
            'GLN': 'Q',
            'GLU': 'E',
            'GLY': 'G',
            'HIS': 'H',
            'HSD': 'H',
            'ILE': 'I',
            'LEU': 'L',
            'LYS': 'K',
            'MET': 'M',
            'PHE': 'F',
            'PRO': 'P',
            'SER': 'S',
            'THR': 'T',
            'TRP': 'W',
            'TYR': 'Y',
            'VAL': 'V',
        }

        sequence = [code_to_letter[code] for code in self.sequence]

        if join:
            sequence = ''.join(sequence)

        return sequence

    def to_str(self):
        pass


def _letter_to_code(residues):
    # Make sure we're in the right format
    # noinspection DuplicatedCode
    letter_to_code = {
        'A': 'ALA',
        'R': 'ARG',
        'N': 'ASN',
        'D': 'ASP',
        'C': 'CYS',
        'Q': 'GLN',
        'E': 'GLU',
        'G': 'GLY',
        'H': 'HIS',
        'I': 'ILE',
        'L': 'LEU',
        'K': 'LYS',
        'M': 'MET',
        'F': 'PHE',
        'P': 'PRO',
        'S': 'SER',
        'T': 'THR',
        'W': 'TRP',
        'Y': 'TYR',
        'V': 'VAL'
    }
    return [letter_to_code.get(residue, residue) for residue in residues]


if __name__ == '__main__':
    ab = Protein('YEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV')  # noqa
