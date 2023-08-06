import multiprocessing as mp
from typing import List
from typing import Union

import numpy as np
from tqdm import tqdm

import sonusai.mixture
from sonusai import SonusAIError
from sonusai import logger
from sonusai.mixture.augmentation import get_augmentations
from sonusai.mixture.class_count import compute_total_class_count
from sonusai.mixture.get_targets_for_truth_index import get_targets_for_truth_index
from sonusai.mixture.process import process_target
from sonusai.utils import seconds_to_hms
from sonusai.utils.parallel import p_map

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


def balance_classes(mixdb: dict,
                    raw_target_audio: list,
                    logging: bool = True,
                    show_progress: bool = False) -> List[dict]:
    """Add target augmentations until the class count values are balanced."""
    first_cba_index = len(mixdb['target_augmentations'])

    MP_DICT['mixdb'] = mixdb
    MP_DICT['raw_target_audio'] = raw_target_audio

    augmented_targets = get_augmented_targets(mixdb)
    class_balancing_samples = get_class_balancing_samples(mixdb, augmented_targets)
    if logging:
        logger.info('')
        label_digits = max([len(get_class_label(mixdb, item)) for item in range(len(class_balancing_samples))])
        samples_digits = np.ceil(np.log10(float(max(class_balancing_samples))))
        samples_digits = int(samples_digits + np.ceil(samples_digits / 3))
        for class_index, required_samples in enumerate(class_balancing_samples):
            logger.info(f'Class {get_class_label(mixdb, class_index):>{label_digits}} '
                        f'needs {required_samples:>{samples_digits},} more active truth samples '
                        f' - {seconds_to_hms(required_samples / sonusai.mixture.SAMPLE_RATE)}')
        logger.info('')

    for class_index, required_samples in enumerate(class_balancing_samples):
        augmented_targets = _balance_class(mixdb=mixdb,
                                           augmented_targets=augmented_targets,
                                           first_cba_index=first_cba_index,
                                           class_index=class_index,
                                           required_samples=required_samples,
                                           logging=logging,
                                           show_progress=show_progress)

    return augmented_targets


def _balance_class(mixdb: dict,
                   augmented_targets: List[dict],
                   first_cba_index: int,
                   class_index: int,
                   required_samples: int,
                   logging: bool = True,
                   show_progress: bool = False) -> List[dict]:
    """Add target augmentations for a single class until the required samples are satisfied."""
    if required_samples == 0:
        return augmented_targets

    class_label = get_class_label(mixdb, class_index)

    # Get list of targets for this class
    target_indices = get_targets_for_truth_index(mixdb, class_index)
    if not target_indices:
        raise SonusAIError(f'Could not find single-class targets for class index {class_index}')

    num_cpus = mp.cpu_count()

    remaining_samples = required_samples
    added_samples = 0
    added_targets = 0
    progress = tqdm(total=required_samples, desc=f'Balance class {class_label}', disable=not show_progress)
    while True:
        records = []
        while len(records) < num_cpus:
            for target_index in target_indices:
                augmentation_indices = get_unused_balancing_augmentations(mixdb=mixdb,
                                                                          augmented_targets=augmented_targets,
                                                                          first_cba_index=first_cba_index,
                                                                          target_file_index=target_index,
                                                                          amount=num_cpus)
                for augmentation_index in augmentation_indices:
                    records.append({
                        'target_file_index':         target_index,
                        'target_augmentation_index': augmentation_index,
                    })

        records = records[0:num_cpus]
        records = p_map(_process_target, records)

        for record in records:
            new_samples = np.sum(np.sum(record['class_count']))
            remaining_samples -= new_samples

            # If the current record will overshoot the required samples then add it only if
            # overshooting results in a sample count closer to the required than not overshooting.
            add_record = remaining_samples >= 0 or -remaining_samples < remaining_samples + new_samples

            if add_record:
                augmented_targets.append(record)
                added_samples += new_samples
                added_targets += 1
                progress.update(new_samples)

            if remaining_samples <= 0:
                remove_unused_augmentations(mixdb=mixdb, records=augmented_targets)
                progress.update(required_samples - added_samples)
                progress.close()
                if logging:
                    logger.info(f'Added {added_targets:,} new augmented targets for class {class_label}')
                return augmented_targets


def _process_target(record: dict) -> dict:
    return process_target(record=record, mixdb=MP_DICT['mixdb'], raw_target_audio=MP_DICT['raw_target_audio'])


def get_class_balancing_samples(mixdb: dict, augmented_targets: List[dict]) -> List[int]:
    """Determine the number of additional active truth samples needed for each class in order for
    all classes to be represented evenly over all mixtures.

    If the truth mode is mutually exclusive, ignore the last class (i.e., set to zero).
    """
    class_count = compute_total_class_count(mixdb, augmented_targets)

    if mixdb['truth_mutex']:
        class_count = class_count[:-1]

    result = list(np.max(class_count) - class_count)

    if mixdb['truth_mutex']:
        result.append(0)

    return result


def get_unused_balancing_augmentations(mixdb: dict,
                                       augmented_targets: List[dict],
                                       first_cba_index: int,
                                       target_file_index: int,
                                       amount: int = 1) -> List[int]:
    """Get a list of unused balancing augmentations for a given target file index."""
    balancing_augmentations = [item for item in range(len(mixdb['target_augmentations'])) if
                               item >= first_cba_index]
    used_balancing_augmentations = [sub['target_augmentation_index'] for sub in augmented_targets if
                                    sub['target_file_index'] == target_file_index and
                                    sub['target_augmentation_index'] in balancing_augmentations]

    augmentation_indices = [item for item in balancing_augmentations if item not in used_balancing_augmentations]
    class_balancing_augmentation = get_class_balancing_augmentation(mixdb=mixdb, target_file_index=target_file_index)

    while len(augmentation_indices) < amount:
        new_augmentation = get_augmentations(class_balancing_augmentation)[0]
        mixdb['target_augmentations'].append(new_augmentation)
        augmentation_indices.append(len(mixdb['target_augmentations']) - 1)

    return augmentation_indices


def remove_unused_augmentations(mixdb: dict, records: List[dict]) -> None:
    """Remove any unused target augmentation rules from the end of the database."""
    max_used_augmentation = max([sub['target_augmentation_index'] for sub in records]) + 1
    mixdb['target_augmentations'] = mixdb['target_augmentations'][0:max_used_augmentation]


def get_class_balancing_augmentation(mixdb: dict, target_file_index: int) -> Union[dict, None]:
    """Get the class balancing augmentation rule for the given target."""
    class_balancing_augmentation = mixdb['class_balancing_augmentation']
    if 'class_balancing_augmentation' in mixdb['targets'][target_file_index]:
        class_balancing_augmentation = mixdb['targets'][target_file_index]['class_balancing_augmentation']
    return class_balancing_augmentation


def get_augmented_targets(mixdb: dict) -> List[dict]:
    """Get a list of augmented targets from a mixture database."""
    augmented_targets = list()
    keys = [
        'target_file_index',
        'target_augmentation_index',
        'samples',
        'target_gain',
        'class_count',
    ]
    snr = max(mixdb['noise_mix']['snrs'])
    mixtures = [sub for sub in mixdb['mixtures'] if sub['snr'] == snr and sub['noise_file_index'] == 0]
    for mixture in mixtures:
        record = dict()
        for key in keys:
            record[key] = mixture[key]
        augmented_targets.append(record)

    return augmented_targets


def get_class_label(mixdb: dict, class_index: int) -> str:
    if mixdb['class_labels']:
        return mixdb['class_labels'][class_index]

    return str(class_index)
