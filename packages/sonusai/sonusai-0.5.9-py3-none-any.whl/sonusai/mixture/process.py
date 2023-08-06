from typing import List

import numpy as np

from sonusai.mixture.augmentation import apply_augmentation
from sonusai.mixture.class_count import get_class_count
from sonusai.mixture.get_next_noise import get_next_noise


def _process_target_audio(mixdb: dict, record: dict, raw_target_audio: List[np.ndarray]) -> np.ndarray:
    """Apply augmentation and update target metadata."""
    target_augmentation = mixdb['target_augmentations'][record['target_augmentation_index']]

    augmented_target_audio = apply_augmentation(audio_in=raw_target_audio[record['target_file_index']],
                                                augmentation=target_augmentation,
                                                length_common_denominator=mixdb['feature_step_samples'])

    record['samples'] = len(augmented_target_audio)

    # target_gain is used to back out the gain augmentation in order to return the target audio
    # to its normalized level when calculating truth.
    if 'gain' in target_augmentation:
        record['target_gain'] = 10 ** (target_augmentation['gain'] / 20)
    else:
        record['target_gain'] = 1
    record['class_count'] = get_class_count(mixdb=mixdb, record=record, audio=augmented_target_audio)

    return augmented_target_audio


def process_target(record: dict, mixdb: dict, raw_target_audio: List[np.ndarray]) -> dict:
    """Apply augmentation and update target metadata."""
    _process_target_audio(mixdb, record, raw_target_audio)
    return record


def process_mixture(record: dict,
                    mixdb: dict,
                    raw_target_audio: List[np.ndarray],
                    augmented_noise_audio: np.ndarray) -> dict:
    augmented_target_audio = _process_target_audio(mixdb, record, raw_target_audio)

    noise_segment, _ = get_next_noise(offset_in=record['noise_offset'],
                                      length=len(augmented_target_audio),
                                      audio_in=augmented_noise_audio)

    if record['snr'] < -96:
        # Special case for zeroing out target data
        record['target_snr_gain'] = 0
        record['noise_snr_gain'] = 1
        record['class_count'] = [[0] * len(inner) for inner in record['class_count']]
        # Setting target_gain to zero will cause the truth to be all zeros.
        record['target_gain'] = 0
    elif record['snr'] > 96:
        # Special case for zeroing out noise data
        record['target_snr_gain'] = 1
        record['noise_snr_gain'] = 0
    else:
        target_energy = np.mean(np.square(np.single(augmented_target_audio)))
        noise_energy = np.mean(np.square(np.single(noise_segment)))
        noise_gain = np.sqrt(target_energy / noise_energy) / 10 ** (
                record['snr'] / 20)

        # Check for noise_gain > 1 to avoid clipping
        if noise_gain > 1:
            record['target_snr_gain'] = 1 / noise_gain
            record['noise_snr_gain'] = 1
        else:
            record['target_snr_gain'] = 1
            record['noise_snr_gain'] = noise_gain

    # Check for clipping in mixture
    gain_adjusted_target_audio = np.single(augmented_target_audio) * record['target_snr_gain']
    gain_adjusted_noise_audio = np.single(noise_segment) * record['noise_snr_gain']
    mixture_audio = gain_adjusted_target_audio + gain_adjusted_noise_audio

    if any(abs(mixture_audio) >= 32768):
        # Clipping occurred; lower gains to bring audio within int16 bounds
        gain_adjustment = 32760 / max(abs(mixture_audio))
        record['target_snr_gain'] *= gain_adjustment
        record['noise_snr_gain'] *= gain_adjustment

    return record
