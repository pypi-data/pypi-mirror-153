"""sonusai genmixdb

usage: genmixdb [-hv] CONFIG...

options:
   -h, --help
   -v, --verbose    Be verbose.

Create mixture database data for training and evaluation.

genmixdb creates a database of training and evaluation feature and truth data generation information. It allows
the choice of audio neural-network feature types that are supported by the Aaware real-time front-end and truth
data that is synchronized frame-by-frame with the feature data.

Here are some examples:

#### Adding target data
Suppose you have an audio file which is an example, or target, of what you want to
recognize or detect. Of course, for training a NN you also need truth data for that
file (also called labels). If you don't already have it, genmixdb can create truth using
energy-based sound detection on each frame of the feature data. You can also select
different feature types. Here's an example:

genmixdb target_gfr32ts2.yml

where target_gfr32ts2.yml contains:
---
targets:
  - data/target.wav

feature: gfr32ts2

target_augmentations:
  -
    normalize: -3.5
...

The mixture database is written to a JSON file that inherits the base name of the config file.

#### Target data mix with noise and augmentation

genmixdb mix_gfr32ts2.yml

where mix_gfr32ts2.yml contains:
---
targets:
  - data/target.wav

noise_mix:
  files:
    - data/noise.wav
  augmentations:
    - normalize: -3.5
  snrs:
    - 20

feature: gfr32ts2

output: data/my_mix.h5

target_augmentations:
  - normalize: -3.5
    pitch: [-3, 0, 3]
    tempo: [0.8, 1, 1.2]
...

In this example a time-domain mixture is created and feature data is calculated as
specified by 'feature: gfr32ts2'. Various feature types are available which vary in
spectral and temporal resolution (4 ms or higher), and other feature algorithm
parameters. The total feature size, dimension, and #frames for mixture is reported
in the log file (the log file name is derived from the output file base name; in this
case it would be mix_gfr32ts2.log).

Truth (labels) can be automatically created per feature output frame based on sound
energy detection. By default, these are appended to the feature data in a single HDF5
output file. By default, truth/label generation is turned on with default algorithm
and threshold levels (see truth section) and a single class, i.e., detecting a single
type of sound. The truth format is a single float per class representing the
probability of activity/presence, and multi-class truth/labels are possible by
specifying the number of classes and either a scalar index or a vector of indices in
which to put the truth result. For example, 'num_class: 3' and  'truth_index: 2' adds
a 1x3 vector to the feature data with truth put in index 2 (others would be 0) for
data/target.wav being an audio clip from sound type of class 2.

The mixture is created with potential data augmentation functions in the following way:
1. apply noise augmentation rule
2. apply target augmentation rule
3. adjust noise gain for specific SNR
4. add augmented noise to augmented target

The mixture length is the target length by default, and the noise signal is repeated
if it is shorter, or trimmed if longer.

#### Target and noise using path lists

Target and noise audio is specified as a list containing text files, audio files, and
file globs. Text files are processed with items on each line where each item can be a
text file, an audio file, or a file glob. Each item will be searched for audio files
which can be WAV, MP3, FLAC, AIFF, or OGG format with any sample rate, bit depth, or
channel count. All audio files will be converted to 16 kHz, 16-bit, single channel
format before processing. For example,

genmixdb dog-bark.yml

where dog-bark.yml contains:
---
targets:
  - slib/dog-outside/*.wav
  - slib/dog-inside/*.wav

will find all .wav files in the specified directories and process them as targets.

"""
import json
import time
from os.path import splitext
from random import seed

import yaml
from docopt import docopt
from tqdm import tqdm

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import apply_augmentation
from sonusai.mixture import estimate_audio_length
from sonusai.mixture import get_augmentations
from sonusai.mixture import get_class_weights_threshold
from sonusai.mixture import get_feature_stats
from sonusai.mixture import get_input_files
from sonusai.mixture import get_max_class
from sonusai.mixture import get_total_class_count
from sonusai.mixture import load_config
from sonusai.mixture import log_duration_and_sizes
from sonusai.mixture import process_mixture
from sonusai.mixture import process_target
from sonusai.mixture import read_all_audio
from sonusai.mixture import update_truth_settings
from sonusai.utils import p_tqdm_map
from sonusai.utils import seconds_to_hms
from sonusai.utils import trim_docstring

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


def genmixdb(file: str = None,
             config: dict = None,
             logging: bool = True,
             show_progress: bool = False) -> dict:
    if (file is None and config is None) or (file is not None and config is not None):
        raise SonusAIError(f'Must specify either file name or config.')

    if file is not None:
        config = load_config(file)

    seed(config['seed'])

    if logging:
        logger.debug(f'Seed: {config["seed"]}')
        logger.debug('Configuration:')
        logger.debug(yaml.dump(config))

    if logging:
        logger.info('Collecting targets')
    targets = get_input_files(records=config['targets'], truth_settings=config['truth_settings'])
    if len(targets) == 0:
        raise SonusAIError('Canceled due to no targets')

    if logging:
        logger.debug('List of targets:')
        logger.debug(yaml.dump([sub['name'] for sub in targets], default_flow_style=False))

    if logging:
        logger.info('Collecting noises')
    noises = get_input_files(records=config['noise_mix']['files'])
    if logging:
        logger.debug('List of noises:')
        logger.debug(yaml.dump([sub['name'] for sub in noises], default_flow_style=False))

    if logging:
        logger.info('Collecting target augmentations')
    target_augmentations = get_augmentations(rules=config['target_augmentations'], target=True)
    expanded_target_augmentations = ''
    for augmentation in target_augmentations:
        expanded_target_augmentations += f'- {augmentation}\n'
    if logging:
        logger.debug('Expanded list of target augmentations:')
        logger.debug(expanded_target_augmentations)

    if logging:
        logger.info('Collecting noise augmentations')
    noise_augmentations = get_augmentations(config['noise_mix']['augmentations'], target=False)
    expanded_noise_augmentations = ''
    for augmentation in noise_augmentations:
        expanded_noise_augmentations += f'- {augmentation}\n'
    if logging:
        logger.debug('Expanded list of noise augmentations:')
        logger.debug(expanded_noise_augmentations)

    if logging:
        logger.debug(f'SNRs: {config["noise_mix"]["snrs"]}\n')
        logger.debug(f'Exhaustive noise: {config["noise_mix"]["exhaustive"]}\n')

    if config['truth_mode'] not in ['normal', 'mutex']:
        raise SonusAIError(f'invalid truth_mode: {config["truth_mode"]}')
    truth_mutex = config['truth_mode'] == 'mutex'
    max_class = get_max_class(config['num_classes'], truth_mutex)

    (feature_ms,
     feature_samples,
     feature_step_ms,
     feature_step_samples,
     num_bands,
     stride) = get_feature_stats(feature_mode=config['feature'],
                                 frame_size=config['frame_size'],
                                 num_classes=config['num_classes'],
                                 truth_mutex=truth_mutex)

    mixdb = {
        'class_balancing_augmentation': config['class_balancing_augmentation'],
        'class_count':                  list(),
        'class_labels':                 config['class_labels'],
        'class_weights_threshold':      get_class_weights_threshold(config),
        'feature':                      config['feature'],
        'feature_samples':              feature_samples,
        'feature_step_samples':         feature_step_samples,
        'frame_size':                   config['frame_size'],
        'mixtures':                     list(),
        'noise_mix':                    {
            'augmentations': noise_augmentations,
            'exhaustive':    config['noise_mix']['exhaustive'],
            'files':         noises,
            'snrs':          config['noise_mix']['snrs'],
        },
        'num_classes':                  config['num_classes'],
        'seed':                         config['seed'],
        'target_augmentations':         target_augmentations,
        'targets':                      targets,
        'truth_mutex':                  truth_mutex,
        'truth_reduction_function':     config['truth_reduction_function'],
        'truth_settings':               config['truth_settings'],
    }

    MP_DICT['mixdb'] = mixdb
    MP_DICT['config'] = config

    raw_noise_audio, raw_target_audio = read_all_audio(noises=noises, targets=targets, show_progress=show_progress)

    MP_DICT['raw_target_audio'] = raw_target_audio

    noise_sets = len(noises) * len(noise_augmentations)
    target_sets = len(targets) * len(target_augmentations) * len(config['noise_mix']['snrs'])
    total_mixtures = noise_sets * target_sets
    if logging:
        logger.info('')
        logger.info(f'Found {total_mixtures:,} mixtures to process')

    total_duration = 0
    for duration in [sub['duration'] for sub in targets]:
        for augmentation in target_augmentations:
            length = int(duration * sonusai.mixture.SAMPLE_RATE)
            if 'tempo' in augmentation:
                length /= augmentation['tempo']
            if length % feature_step_samples:
                length += feature_step_samples - int(length % feature_step_samples)
            total_duration += float(length) / sonusai.mixture.SAMPLE_RATE
    total_duration *= noise_sets
    total_duration *= len(config['noise_mix']['snrs'])

    if logging:
        log_duration_and_sizes(total_duration=total_duration,
                               num_classes=config['num_classes'],
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
            for target_index, target in enumerate(targets):
                for target_augmentation_index, target_augmentation in enumerate(target_augmentations):
                    if not isinstance(target['truth_settings'], list):
                        target['truth_settings'] = [target['truth_settings']]

                    update_truth_settings(target['truth_settings'], config['truth_settings'])

                    for truth_setting in target['truth_settings']:
                        if not isinstance(truth_setting['index'], list):
                            truth_setting['index'] = [truth_setting['index']]

                        if any(idx > max_class for idx in truth_setting['index']):
                            raise SonusAIError('invalid truth index')

                    for snr in config['noise_mix']['snrs']:
                        mixtures[n_id][t_id] = {
                            'target_file_index':         target_index,
                            'noise_file_index':          noise_index,
                            'noise_offset':              noise_offset,
                            'target_augmentation_index': target_augmentation_index,
                            'noise_augmentation_index':  noise_augmentation_index,
                            'snr':                       snr,
                        }
                        t_id += 1

                        target_length = estimate_audio_length(audio_in=raw_target_audio[target_index],
                                                              augmentation=target_augmentation,
                                                              length_common_denominator=feature_step_samples)
                        noise_offset = int((noise_offset + target_length) % noise_length)

            n_id += 1

    # Fill in the details
    progress = tqdm(total=total_mixtures, desc='genmixdb', disable=not show_progress)
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


def get_output_from_config(config: dict, config_name: str) -> str:
    try:
        config_base = splitext(config_name)[0]
        name = str(splitext(config['output'])[0])
        name = name.replace('${config}', config_base)
        return name
    except Exception as e:
        raise SonusAIError(f'Error getting genmixdb base name: {e}')


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

        for config_file in args['CONFIG']:
            start_time = time.monotonic()
            logger.info(f'Creating mixture database for {config_file}')
            config = load_config(config_file)
            output = get_output_from_config(config, config_file)

            log_name = output + '.log'
            create_file_handler(log_name)
            update_console_handler(verbose)
            initial_log_messages('genmixdb')

            mixdb = genmixdb(config=config, show_progress=True)

            json_name = output + '.json'
            with open(file=json_name, mode='w') as file:
                json.dump(mixdb, file, indent=2)
                logger.info(f'Wrote mixture database for {config_file} to {json_name}')

            end_time = time.monotonic()
            logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
