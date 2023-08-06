
from glob import glob
from itertools import product
import os


class Path:
    """
    A way to hold a path (as string) but retain metadata.
    """

    __slots__ = ('_path', '_metadata')

    def __init__(self, path, **metadata):
        if isinstance(path, Path):
            metadata = path._metadata
            path = path._path

        self._path = path
        self._metadata = metadata

    def __repr__(self):
        return self._path

    def __fspath__(self):
        return self._path

    @property
    def metadata(self):
        return self._metadata


# Variable glob
def vglob(path, errors='raise', **kwargs):
    """"
    Variable glob.
    """

    # Where any kwargs supplied? If not, short-circuit and glob
    if len(kwargs) == 0:
        return glob(path)

    # Variables to iterate
    keys = kwargs.keys()
    if errors.lower() in 'raise':
        for key in keys:
            if key not in path:
                raise AttributeError('{' + f'{key}' + '}' + f' not in path="{path}"')

    # Values
    def _convert_to_list(value):
        # BUGFIX https://github.com/LockhartLab/molecular/issues/2#issue-838289328
        if not isinstance(value, range) and not hasattr(value, '__getitem__'):
            value = [value]
        return value

    values = map(_convert_to_list, kwargs.values())

    # Go through each set of values and
    files = []
    for value_set in product(*values):
        fmt = {key: value_set[i] for i, key in enumerate(keys)}
        fname = path.format(**fmt)
        if errors.lower() in 'raise' and not os.path.exists(fname):
            raise FileNotFoundError(fname)
        files.append(Path(fname, **fmt))

    # Return
    return files
