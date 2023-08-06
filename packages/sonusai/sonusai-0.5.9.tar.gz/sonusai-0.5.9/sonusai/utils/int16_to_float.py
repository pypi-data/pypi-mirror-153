import numpy as np


def int16_to_float(x: np.ndarray) -> np.ndarray:
    """Convert int16 array to floating point with range +/- 1"""
    return np.single(x) / 32768
