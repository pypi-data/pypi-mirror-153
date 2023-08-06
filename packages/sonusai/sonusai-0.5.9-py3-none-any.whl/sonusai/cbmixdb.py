"""sonusai cbmixdb

usage: cbmixdb [-hv] (-d MIXDB) [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Input mixture database JSON file.
    -o OUTPUT, --output OUTPUT      Output class balanced mixture database JSON file.

Perform class balancing on a SonusAI mixture database.

Inputs:
    MIXDB   A SonusAI mixture database JSON file.

Outputs:
    OUTPUT  A SonusAI mixture database JSON file that has class balanced data.

    cbmixdb.log

"""
import json
import time
from random import seed

import numpy as np
import yaml
from docopt import docopt
from tqdm import tqdm

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import apply_augmentation
from sonusai.mixture import balance_classes
from sonusai.mixture import estimate_audio_length
from sonusai.mixture import get_feature_stats
from sonusai.mixture import get_total_class_count
from sonusai.mixture import load_mixdb
from sonusai.mixture import log_duration_and_sizes
from sonusai.mixture import process_mixture
from sonusai.mixture import process_target
from sonusai.mixture import read_all_audio
from sonusai.utils import p_tqdm_map
from sonusai.utils import seconds_to_hms
from sonusai.utils import trim_docstring

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


def cbmixdb(mixdb: dict,
            logging: bool = True,
            show_progress: bool = False) -> dict:
    seed(mixdb['seed'])

    if logging:
        logger.debug(f'Seed: {mixdb["seed"]}')

    targets = mixdb['targets']
    if logging:
        logger.debug('List of targets:')
        logger.debug(yaml.dump([sub['name'] for sub in targets], default_flow_style=False))

    noises = mixdb['noise_mix']['files']
    if logging:
        logger.debug('List of noises:')
        logger.debug(yaml.dump([sub['name'] for sub in noises], default_flow_style=False))

    target_augmentations = mixdb['target_augmentations']
    noise_augmentations = mixdb['noise_mix']['augmentations']

    if logging:
        logger.debug(f'SNRs: {mixdb["noise_mix"]["snrs"]}\n')
        logger.debug(f'Exhaustive noise: {mixdb["noise_mix"]["exhaustive"]}\n')

    (feature_ms,
     feature_samples,
     feature_step_ms,
     feature_step_samples,
     num_bands,
     stride) = get_feature_stats(feature_mode=mixdb['feature'],
                                 frame_size=mixdb['frame_size'],
                                 num_classes=mixdb['num_classes'],
                                 truth_mutex=mixdb['truth_mutex'])

    MP_DICT['mixdb'] = mixdb

    raw_noise_audio, raw_target_audio = read_all_audio(noises=noises, targets=targets, show_progress=show_progress)

    MP_DICT['raw_target_audio'] = raw_target_audio

    # Balance class data
    augmented_targets = balance_classes(mixdb=mixdb,
                                        raw_target_audio=raw_target_audio,
                                        show_progress=show_progress)

    noise_sets = len(noises) * len(noise_augmentations)
    target_sets = len(augmented_targets) * len(mixdb['noise_mix']['snrs'])
    total_mixtures = noise_sets * target_sets
    if logging:
        logger.info('')
        logger.info(f'Found {total_mixtures:,} mixtures to process')

    total_duration = 0
    for augmented_target in augmented_targets:
        length = int(targets[augmented_target['target_file_index']]['duration'] * sonusai.mixture.SAMPLE_RATE)
        augmentation = target_augmentations[augmented_target['target_augmentation_index']]
        if 'tempo' in augmentation:
            length /= augmentation['tempo']
        if length % feature_step_samples:
            length += feature_step_samples - int(length % feature_step_samples)
        total_duration += float(length) / sonusai.mixture.SAMPLE_RATE
    total_duration *= len(mixdb['noise_mix']['snrs'])
    total_duration *= noise_sets

    if logging:
        log_duration_and_sizes(total_duration=total_duration,
                               num_classes=mixdb['num_classes'],
                               feature_step_samples=feature_step_samples,
                               num_bands=num_bands,
                               stride=stride,
                               desc='Estimated')
        logger.info(f'Feature shape:        {stride} x {num_bands} ({stride * num_bands} total params)')
        logger.info(f'Feature samples:      {feature_samples} samples ({feature_ms} ms)')
        logger.info(f'Feature step samples: {feature_step_samples} samples ({feature_step_ms} ms)')

    # Get indices and offsets
    mixtures = [[] for _ in range(noise_sets)]
    n_id = 0
    for noise_index, noise in enumerate(noises):
        for noise_augmentation_index, noise_augmentation in enumerate(noise_augmentations):
            mixtures[n_id] = [[] for _ in range(target_sets)]
            t_id = 0
            noise_offset = 0
            noise_length = estimate_audio_length(audio_in=raw_noise_audio[noise_index],
                                                 augmentation=noise_augmentation,
                                                 length_common_denominator=1)
            for target in augmented_targets:
                target_index = target['target_file_index']
                target_augmentation_index = target['target_augmentation_index']
                target_augmentation = mixdb['target_augmentations'][target_augmentation_index]

                for snr in mixdb['noise_mix']['snrs']:
                    mixtures[n_id][t_id] = {
                        'target_file_index':         target_index,
                        'noise_file_index':          noise_index,
                        'noise_offset':              noise_offset,
                        'target_augmentation_index': target_augmentation_index,
                        'noise_augmentation_index':  noise_augmentation_index,
                        'snr':                       snr,
                        'target_snr_gain':           np.NaN,
                        'noise_snr_gain':            np.NaN,
                        'samples':                   target['samples'],
                        'target_gain':               target['target_gain'],
                        'class_count':               target['class_count'],
                    }
                    t_id += 1

                    target_length = estimate_audio_length(audio_in=raw_target_audio[target_index],
                                                          augmentation=target_augmentation,
                                                          length_common_denominator=feature_step_samples)
                    noise_offset = int((noise_offset + target_length) % noise_length)

            n_id += 1

    # Fill in the details
    progress = tqdm(total=total_mixtures, desc='cbmixdb', disable=not show_progress)
    for n_id in range(len(mixtures)):
        MP_DICT['augmented_noise_audio'] = apply_augmentation(
            audio_in=raw_noise_audio[mixtures[n_id][0]['noise_file_index']],
            augmentation=noise_augmentations[mixtures[n_id][0]['noise_augmentation_index']],
            length_common_denominator=1)
        mixtures[n_id] = p_tqdm_map(_process_mixture, mixtures[n_id], progress=progress)
    progress.close()

    # Flatten mixtures
    mixdb['mixtures'] = [item for sublist in mixtures for item in sublist]
    mixdb['class_count'] = get_total_class_count(mixdb)

    total_samples = sum([sub['samples'] for sub in mixdb['mixtures']])
    total_duration = total_samples / sonusai.mixture.SAMPLE_RATE
    if logging:
        log_duration_and_sizes(total_duration=total_duration,
                               num_classes=mixdb['num_classes'],
                               feature_step_samples=feature_step_samples,
                               num_bands=num_bands,
                               stride=stride,
                               desc='Actual')

    return mixdb


def _process_target(record: dict) -> dict:
    return process_target(record=record, mixdb=MP_DICT['mixdb'], raw_target_audio=MP_DICT['raw_target_audio'])


def _process_mixture(record: dict) -> dict:
    return process_mixture(record=record,
                           mixdb=MP_DICT['mixdb'],
                           raw_target_audio=MP_DICT['raw_target_audio'],
                           augmented_noise_audio=MP_DICT['augmented_noise_audio'])


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        output_name = args['--output']

        start_time = time.monotonic()

        log_name = 'cbmixdb.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('cbmixdb')

        logger.info(f'\nLoad mixture database from {mixdb_name}')
        mixdb = load_mixdb(mixdb_name)

        with open(file=output_name, mode='w') as file:
            json.dump(cbmixdb(mixdb=mixdb, show_progress=True), file, indent=2)
            logger.info(f'Wrote class balanced mixture database for {mixdb_name} to {output_name}')

        end_time = time.monotonic()
        logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
