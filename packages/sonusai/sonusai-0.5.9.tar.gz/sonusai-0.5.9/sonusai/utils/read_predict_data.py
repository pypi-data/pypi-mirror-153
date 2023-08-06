import h5py
import numpy as np

from sonusai import SonusAIError
from sonusai import logger


def read_predict_data(filename: str) -> np.ndarray:
    """Read predict data from given HDF5 file and return it."""
    logger.debug(f'Reading prediction data from {filename}')
    with h5py.File(name=filename, mode='r') as f:
        # prediction data is either [frames, num_classes], or [frames, timesteps, num_classes]
        predict = np.array(f['predict'])

        if predict.ndim == 2:
            return predict

        if predict.ndim == 3:
            frames, timesteps, num_classes = predict.shape

            logger.debug(
                f'Reshaping prediction data in {filename} from [{frames}, {timesteps}, {num_classes}] to [{frames * timesteps}, {num_classes}]')
            predict = np.reshape(predict, [frames * timesteps, num_classes], order='F')
            return predict

        raise SonusAIError(f'Ignoring prediction data in {filename} due to invalid dimensions')
