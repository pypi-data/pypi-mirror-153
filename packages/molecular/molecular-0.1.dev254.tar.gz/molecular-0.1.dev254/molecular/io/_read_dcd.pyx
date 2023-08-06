
#cython: language_level=3

# see http://www.ks.uiuc.edu/Research/vmd/plugins/doxygen/dcdplugin_8c-source.html

import numpy as np
from scipy.io import FortranFile

cimport numpy as np

def _read_dcd(fname):
    return _get_box_and_coordinates(fname)

cdef tuple _get_box_and_coordinates(fname):
    # Declarations
    cdef np.ndarray[np.int32_t, ndim=1] iarr
    cdef np.int32_t n_str, n_atoms, i
    cdef np.ndarray[np.float64_t, ndim=2] box
    cdef np.ndarray[np.float32_t, ndim=3] xyz
    cdef np.ndarray[np.float64_t, ndim=1] r8arr

    # Open FortranFile buffer
    buffer = FortranFile(fname, 'r')

    # Header
    iarr = buffer.read_record('i')
    if iarr[0] != 1146244931 or iarr[9] != 0:  # iarr[0] == int.from_bytes(bytes(b'CORD'), 'little')
        # TODO flip byte order
        raise IOError('cannot parse DCD file')
    n_str = iarr[1]

    # Title
    iarr = buffer.read_record('i')
    if iarr[0] != 2:
        raise IOError('cannot parse DCD file')

    # Atoms
    iarr = buffer.read_record('i')
    n_atoms = iarr[0]

    # Box and coordinate information
    box = np.zeros((n_str, 3), dtype=np.float64)
    xyz = np.zeros((n_str, n_atoms, 3), dtype=np.float32)
    for i in range(n_str):
        r8arr = buffer.read_record('f8')
        box[i, :] = r8arr[[0, 2, 5]]

        xyz[i, :, 0] = buffer.read_record('f')
        xyz[i, :, 1] = buffer.read_record('f')
        xyz[i, :, 2] = buffer.read_record('f')

    # Close out buffer
    buffer.close()

    # Return
    return box, xyz

