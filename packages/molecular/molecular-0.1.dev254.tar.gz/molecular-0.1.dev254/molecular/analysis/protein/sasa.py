import yaml
import os
import pandas as pd

include_dir = os.path.abspath(__file__ + '../../../../_include')


# Read relative SASA
def get_relative_sasa(sequence=None, which='Tien'):
    """
    Get relative SASA for sequence. Relative SASA is effectively the maximum SASA allowed for a residue type. It's
    typically computed in the form Gly-X-Gly, where X is the residue of interest.

    Rose


    Tien
    https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0080635&type=printable


    ala-x-ala???
    https://doi.org/10.1016/0022-2836(91)90027-4

    Parameters
    ----------
    sequence : np.ndarray or None
        If None, relative SASA for all 20 common amino acids are returned.
    which : str
        Which version of relative SASA should we use? Choices include Rose, Tien... (Default: Tien)

    Returns
    -------
    pandas.Series
        Relative SASA.
    """

    # Read in normalizing SASA values
    with open(os.path.join(include_dir, 'protein', 'relative_sasa.yml'), 'r') as stream:
        data = yaml.safe_load(stream.read())

    # Get specific normalize dataset
    data = data[which]

    # Convert to Series
    relative_sasa = pd.Series(data).rename('relative_sasa')

    # Result
    result = relative_sasa
    if sequence is not None:
        result = relative_sasa.loc[sequence]

    # Return
    return result


class SurfaceArea:
    pass


if __name__ == '__main__':
    print(get_relative_sasa())
