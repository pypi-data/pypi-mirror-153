import json
from typing import List
from typing import Union

import h5py
import numpy as np

from sonusai import SonusAIError
from sonusai.mixture.get_file_frame_segments import get_file_frame_segments


def get_ft_from_file(filename: str, mixid: Union[str, List[int]] = ':') -> (np.ndarray, np.ndarray):
    """Get feature/truth frames from H5 file for given mixture ID's"""
    try:
        with h5py.File(filename, 'r') as f:
            mixdb = json.loads(f.attrs['mixdb'])
            stride = f['feature'].shape[1]
            num_bands = f['feature'].shape[2]
            num_classes = f['truth_f'].shape[1]

            file_frame_segments = get_file_frame_segments(mixdb, mixid)
            total_frames = sum([file_frame_segments[m].length for m in file_frame_segments])
            feature = np.empty((total_frames, stride, num_bands), dtype=np.single)
            truth = np.empty((total_frames, num_classes), dtype=np.single)
            start = 0
            for m in file_frame_segments:
                length = file_frame_segments[m].length
                feature[start:start + length] = f['feature'][file_frame_segments[m].get_slice()]
                truth[start:start + length] = f['truth_f'][file_frame_segments[m].get_slice()]
                start += length

            return feature, truth

    except Exception as e:
        raise SonusAIError(f'Error: {e}')
