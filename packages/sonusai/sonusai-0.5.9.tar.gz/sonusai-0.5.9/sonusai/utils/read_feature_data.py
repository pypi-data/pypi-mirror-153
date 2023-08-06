import json

import h5py
import numpy as np


def read_feature_data(filename: str) -> (dict, np.ndarray, np.ndarray, np.ndarray):
    """Read mixdb, feature, truth_f, and segsnr data from given HDF5 file and return them as a tuple."""
    with h5py.File(name=filename, mode='r') as f:
        return json.loads(f.attrs['mixdb']), np.array(f['feature']), np.array(f['truth_f']), np.array(f['segsnr'])
