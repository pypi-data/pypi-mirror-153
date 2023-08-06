import numpy as np


def estimate_audio_length(audio_in: np.ndarray,
                          augmentation: dict,
                          length_common_denominator: int) -> int:
    """Estimate the length of audio after augmentation."""
    length = len(audio_in)

    if 'tempo' in augmentation:
        factor = augmentation['tempo']
        length = int(length / factor)

    if length % length_common_denominator:
        length += length_common_denominator - int(length % length_common_denominator)

    return length
