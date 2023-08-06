import multiprocessing

import numpy


def to_numpy_array(arr: multiprocessing.Array, dtype=None) -> numpy.ndarray:
    """Convert multiprocessing array to numpy array"""
    return numpy.frombuffer(arr.get_obj(), dtype=dtype)
