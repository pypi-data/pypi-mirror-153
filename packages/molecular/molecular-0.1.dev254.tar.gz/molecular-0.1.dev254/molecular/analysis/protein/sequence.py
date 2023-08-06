"""
sequence.py
"""


def shorten(a):
    d = {
        'ALA': 'A',
        'ARG': 'R',
        'ASN': 'N',
        'ASP': 'D',
        'CYS': 'C',
        'GLN': 'Q',
        'GLU': 'E',
        'GLY': 'G',
        'HIS': 'H',
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
        'VAL': 'V'
    }
    return [d[x] for x in a]


to_letter = shorten


def sequence(a):
    """

    Parameters
    ----------
    a

    Returns
    -------

    """

    # Select C-alpha atoms
    a = a.select(atom='CA')

    # Get residue name
    return a.topology['residue']
