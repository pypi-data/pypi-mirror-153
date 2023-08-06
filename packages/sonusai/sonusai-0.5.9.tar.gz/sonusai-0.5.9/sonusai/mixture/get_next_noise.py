import numpy as np


def get_next_noise(offset_in: int, length: int, audio_in: np.ndarray) -> (np.ndarray, int):
    audio_out = np.take(audio_in, range(offset_in, offset_in + length), mode='wrap')
    offset_out = (offset_in + length) % len(audio_in)
    return audio_out, offset_out
