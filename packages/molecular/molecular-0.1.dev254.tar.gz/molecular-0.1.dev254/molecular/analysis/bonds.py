
import numpy as np

def angle(atom0, atom1, atom2, method='atan2', degrees=False):
    assert atom0.shape == atom1.shape == atom2.shape

    a = atom0.xyz.to_numpy() - atom1.xyz.to_numpy()
    b = atom2.xyz.to_numpy() - atom1.xyz.to_numpy()

    if method.lower() in 'atan2':
        results = np.arctan2(np.linalg.norm(np.cross(a, b, axis=1), axis=1), np.sum(a * b, axis=1))
    elif method.lower() in 'acos':
        results =  np.arccos(np.sum(a * b, axis=1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)))
    else:
        raise AttributeError(f'method {method} not understood')

    if degrees:
        results = np.rad2deg(results)

    return results