from copy import deepcopy
from typing import List
from typing import Union

import h5py
import numpy as np
from pyaaware import ForwardTransform
from pyaaware import SED

from sonusai import SonusAIError
from sonusai.mixture.get_mixtures_from_mixid import convert_mixid_to_list
from sonusai.utils import int16_to_float


def _strictly_decreasing(list_to_check: list) -> bool:
    return all(x > y for x, y in zip(list_to_check, list_to_check[1:]))


def generate_truth(mixdb: dict,
                   record: dict,
                   target: np.ndarray,
                   compute: bool = True) -> np.ndarray:
    if not compute:
        return np.empty(0, dtype=np.single)

    truth = np.zeros((len(target), mixdb['num_classes']), dtype=np.single)
    for truth_setting in mixdb['targets'][record['target_file_index']]['truth_settings']:
        config = deepcopy(truth_setting)
        config['frame_size'] = mixdb['frame_size']
        config['num_classes'] = mixdb['num_classes']
        config['mutex'] = mixdb['truth_mutex']
        config['target_gain'] = record['target_gain']
        if 'target_snr_gain' in record and not np.isnan(record['target_snr_gain']):
            config['target_gain'] *= record['target_snr_gain']
        truth += truth_function(target=target, config=config)

    return truth


def truth_function(target: np.ndarray,
                   config: dict) -> np.ndarray:
    truth = np.zeros((len(target), config['num_classes']), dtype=np.single)

    if config['function'] == 'sed':
        if len(target) % config['frame_size'] != 0:
            raise SonusAIError(f'Number of samples in audio is not a multiple of {config["frame_size"]}')

        if 'config' not in config:
            raise SonusAIError('Truth function SED missing config')

        parameters = ['thresholds']
        for parameter in parameters:
            if parameter not in config['config']:
                raise SonusAIError(f'Truth function SED config missing required parameter: {parameter}')

        thresholds = config['config']['thresholds']
        if not _strictly_decreasing(thresholds):
            raise SonusAIError(f'Truth function SED thresholds are not strictly decreasing: {thresholds}')

        if config['target_gain'] == 0:
            return truth

        fft = ForwardTransform(N=config['frame_size'] * 4, R=config['frame_size'])
        sed = SED(thresholds=thresholds,
                  index=config['index'],
                  frame_size=config['frame_size'],
                  num_classes=config['num_classes'],
                  mutex=config['mutex'])

        audio = np.int16(np.single(target) / config['target_gain'])
        for offset in range(0, len(audio), config['frame_size']):
            indices = slice(offset, offset + config['frame_size'])
            new_truth = sed.execute(fft.energy(int16_to_float(audio[indices])))
            truth[indices] = np.reshape(new_truth, (1, len(new_truth)))

        return truth

    elif config['function'] == 'file':
        if 'config' not in config:
            raise SonusAIError('Truth function file missing config')

        parameters = ['file']
        for parameter in parameters:
            if parameter not in config['config']:
                raise SonusAIError(f'Truth function file config missing required parameter: {parameter}')

        with h5py.File(name=config['config']['file'], mode='r') as f:
            truth_in = f['/truth_t'][:]

        if truth_in.ndim != 2:
            raise SonusAIError('Truth file data is not 2 dimensions')

        if truth_in.shape[0] != len(target):
            raise SonusAIError('Truth file does not contain the right amount of samples')

        if config['target_gain'] == 0:
            return truth

        if isinstance(config['index'], list):
            if len(config['index']) != truth_in.shape[1]:
                raise SonusAIError('Truth file does not contain the right amount of classes')

            truth[:, config['index']] = truth_in
        else:
            if config['index'] + truth_in.shape[1] > config['num_classes']:
                raise SonusAIError('Truth file contains too many classes')

            truth[:, config['index']:config['index'] + truth_in.shape[1]] = truth_in

        return truth

    elif config['function'] == 'energy':
        if config['target_gain'] == 0:
            return truth

        fft = ForwardTransform(N=config['frame_size'] * 4, R=config['frame_size'])
        for offset in range(0, len(target), config['frame_size']):
            target_energy = fft.energy(int16_to_float(target[offset:offset + config['frame_size']]))
            truth[offset:offset + config['frame_size'], config['index']] = np.single(target_energy)

        return truth

    elif config['function'] == 'phoneme':
        # Read in .txt transcript and run a Python function to generate text grid data
        # (indicating which phonemes are active)
        # Then generate truth based on this data and put in the correct classes based on config['index']
        raise SonusAIError('Truth function phoneme is not supported yet')

    raise SonusAIError(f'Unsupported truth function: {config["function"]}')


def get_truth_indices_for_mixid(mixdb: dict, mixid: Union[str, List[int]]) -> List[List[int]]:
    """Get a list of truth indices for a given mixture."""
    indices = list()

    for m in convert_mixid_to_list(mixdb, mixid):
        indices.append(get_truth_indices_for_target(mixdb, mixdb['mixtures'][m]['target_file_index']))

    return indices


def get_truth_indices_for_target(mixdb: dict, target_file_index: int) -> List[int]:
    """Get a list of truth indices for a given target index."""
    index = [sub['index'] for sub in mixdb['targets'][target_file_index]['truth_settings']]

    # flatten, uniquify, and sort
    return sorted(list(set([item for sublist in index for item in sublist])))
