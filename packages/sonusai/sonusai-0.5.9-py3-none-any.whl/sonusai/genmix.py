"""sonusai genmix

usage: genmix [-hvts] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database JSON file.
    -i MIXID, --mixid MIXID         Mixture IDs JSON file.
    -o OUTPUT, --output OUTPUT      Output HDF5 file.
    -t, --truth                     Save truth_t. [default: False].
    -s, --segsnr                    Save segsnr. [default: False].

Generate a SonusAI mixture file from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database JSON file.
    MIXID       A JSON file containing a list of mixture IDs. The list should be named 'mixid'.
                If no file is provided, then all mixtures in the database will be generated.

Outputs:
    OUTPUT.h5   A SonusAI mixture HDF5 file. Contains:
                    dataset:    mixture
                    dataset:    truth_t (optional)
                    dataset:    target
                    dataset:    noise
                    dataset:    segsnr (optional)
                    attribute:  mixdb
    genmix.log
"""
import ctypes
import json
import multiprocessing
import time
from os.path import splitext
from typing import List
from typing import Union

import h5py
import numpy as np
from docopt import docopt
from tqdm import tqdm

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import build_noise_audio_db
from sonusai.mixture import build_target_audio_db
from sonusai.mixture import check_audio_files_exist
from sonusai.mixture import get_audio_and_truth_t
from sonusai.mixture import get_feature_frames_in_mixture
from sonusai.mixture import get_samples_in_mixture
from sonusai.mixture import get_total_class_count
from sonusai.mixture import get_transform_frames_in_mixture
from sonusai.mixture import load_mixdb
from sonusai.mixture import load_mixid
from sonusai.mixture import new_mixdb_from_mixid
from sonusai.mixture import set_mixture_offsets
from sonusai.utils import grouper
from sonusai.utils import human_readable_size
from sonusai.utils import p_tqdm_map
from sonusai.utils import seconds_to_hms
from sonusai.utils import to_numpy_array
from sonusai.utils import trim_docstring

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


# noinspection PyGlobalUndefined

def mp_init(mixture_: multiprocessing.Array,
            truth_t_: multiprocessing.Array,
            target_: multiprocessing.Array,
            noise_: multiprocessing.Array,
            segsnr_: multiprocessing.Array) -> None:
    global mp_mixture
    global mp_truth_t
    global mp_target
    global mp_noise
    global mp_segsnr

    mp_mixture = mixture_
    mp_truth_t = truth_t_
    mp_target = target_
    mp_noise = noise_
    mp_segsnr = segsnr_


def init(mixdb: dict,
         mixid: Union[str, List[int]],
         logging: bool = True) -> (dict, int):
    mixdb_out = new_mixdb_from_mixid(mixdb=mixdb, mixid=mixid)

    total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])

    if logging:
        logger.info('')
        logger.info(f'Found {len(mixdb_out["mixtures"]):,} mixtures to process')
        logger.info(f'{total_samples:,} samples')

    return mixdb_out, total_samples


def genmix(mixdb: dict,
           mixid: Union[str, List[int]],
           compute_segsnr: bool = False,
           compute_truth: bool = False,
           logging: bool = False,
           show_progress: bool = False,
           progress: tqdm = None,
           initial_i_sample_offset: int = 0,
           initial_i_frame_offset: int = 0,
           initial_o_frame_offset: int = 0) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict):
    mixdb_out, total_samples = init(mixdb=mixdb, mixid=mixid, logging=logging)

    MP_DICT['mixdb'] = mixdb_out
    MP_DICT['total_samples'] = total_samples
    MP_DICT['compute_truth'] = compute_truth
    MP_DICT['compute_segsnr'] = compute_segsnr
    MP_DICT['target_audios'] = build_target_audio_db(mixdb=mixdb_out, show_progress=show_progress)
    MP_DICT['noise_audios'] = build_noise_audio_db(mixdb=mixdb_out, show_progress=show_progress)

    mp_mixture = multiprocessing.Array(ctypes.c_int16, total_samples)
    if compute_truth:
        mp_truth_t = multiprocessing.Array(ctypes.c_float, total_samples * mixdb_out['num_classes'])
    else:
        mp_truth_t = multiprocessing.Array(ctypes.c_float, 0)
    mp_target = multiprocessing.Array(ctypes.c_int16, total_samples)
    mp_noise = multiprocessing.Array(ctypes.c_int16, total_samples)
    if compute_segsnr:
        mp_segsnr = multiprocessing.Array(ctypes.c_float, total_samples)
    else:
        mp_segsnr = multiprocessing.Array(ctypes.c_float, 0)

    mixture = to_numpy_array(mp_mixture, dtype=np.int16)
    if compute_truth:
        truth_t = to_numpy_array(mp_truth_t, dtype=np.single).reshape((total_samples, mixdb_out['num_classes']))
    else:
        truth_t = np.empty(0, dtype=np.single)

    target = to_numpy_array(mp_target, dtype=np.int16)
    noise = to_numpy_array(mp_noise, dtype=np.int16)
    if compute_segsnr:
        segsnr = to_numpy_array(mp_segsnr, dtype=np.single)
    else:
        segsnr = np.empty(0, dtype=np.single)

    # First pass to get offsets
    set_mixture_offsets(mixdb=mixdb_out,
                        initial_i_sample_offset=initial_i_sample_offset,
                        initial_i_frame_offset=initial_i_frame_offset,
                        initial_o_frame_offset=initial_o_frame_offset)

    # Second pass to get mixture and truth_t
    progress_needs_close = False
    if progress is None:
        progress = tqdm(total=len(mixdb_out['mixtures']), desc='genmix', disable=not show_progress)
        progress_needs_close = True

    p_tqdm_map(_process_mixture,
               list(range(len(mixdb_out['mixtures']))),
               progress=progress,
               initializer=mp_init,
               initargs=(mp_mixture, mp_truth_t, mp_target, mp_noise, mp_segsnr))

    if progress_needs_close:
        progress.close()

    mixdb_out['class_count'] = get_total_class_count(mixdb_out)

    duration = len(mixture) / sonusai.mixture.SAMPLE_RATE
    if logging:
        logger.info('')
        logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
        logger.info(f'mixture:  {human_readable_size(mixture.nbytes, 1)}')
        if compute_truth:
            logger.info(f'truth_t:  {human_readable_size(truth_t.nbytes, 1)}')
        if compute_segsnr:
            logger.info(f'segsnr:   {human_readable_size(segsnr.nbytes, 1)}')

    return mixture, truth_t, target, noise, segsnr, mixdb_out


def _process_mixture(mixid: int) -> None:
    mixdb = MP_DICT['mixdb']
    total_samples = MP_DICT['total_samples']
    target_audios = MP_DICT['target_audios']
    noise_audios = MP_DICT['noise_audios']
    compute_truth = MP_DICT['compute_truth']
    compute_segsnr = MP_DICT['compute_segsnr']

    mixture = to_numpy_array(mp_mixture, dtype=np.int16)

    truth_t = to_numpy_array(mp_truth_t, dtype=np.single)
    truth_t = truth_t.reshape((total_samples, mixdb['num_classes']))

    target = to_numpy_array(mp_target, dtype=np.int16)

    noise = to_numpy_array(mp_noise, dtype=np.int16)

    segsnr = to_numpy_array(mp_segsnr, dtype=np.single)

    record = mixdb['mixtures'][mixid]
    first_i_sample_offset = mixdb['mixtures'][0]['i_sample_offset']
    samples = get_samples_in_mixture(mixdb, mixid)

    indices = slice(record['i_sample_offset'] - first_i_sample_offset,
                    record['i_sample_offset'] - first_i_sample_offset + samples)

    (mixture[indices],
     truth_t[indices],
     target[indices],
     noise[indices],
     segsnr[indices]) = get_audio_and_truth_t(mixdb=mixdb,
                                              record=record,
                                              target_audios=target_audios,
                                              noise_audios=noise_audios,
                                              compute_truth=compute_truth,
                                              compute_segsnr=compute_segsnr)


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        mixid_name = args['--mixid']
        output_name = args['--output']
        compute_segsnr = args['--segsnr']
        compute_truth = args['--truth']

        if not output_name:
            output_name = splitext(mixdb_name)[0] + '.h5'

        start_time = time.monotonic()

        log_name = 'genmix.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('genmix')

        logger.info(f'\nLoad mixture database from {mixdb_name}')
        mixdb = load_mixdb(name=mixdb_name)
        mixid = load_mixid(mixdb=mixdb, name=mixid_name)

        mixdb_out, total_samples = init(mixdb=mixdb,
                                        mixid=mixid,
                                        logging=True)

        check_audio_files_exist(mixdb)

        with h5py.File(output_name, 'w') as f:
            f.create_dataset(name='mixture',
                             shape=(total_samples,),
                             dtype=np.int16)
            if compute_truth:
                f.create_dataset(name='truth_t',
                                 shape=(total_samples, mixdb_out['num_classes']),
                                 dtype=np.single)
            f.create_dataset(name='target',
                             shape=(total_samples,),
                             dtype=np.int16)
            f.create_dataset(name='noise',
                             shape=(total_samples,),
                             dtype=np.int16)
            if compute_segsnr:
                f.create_dataset(name='segsnr',
                                 shape=(total_samples,),
                                 dtype=np.single)

        chunk_size = 100
        progress = tqdm(total=len(mixid), desc='genmix')
        mixid = grouper(range(len(mixdb_out['mixtures'])), chunk_size)
        mixdb_out['class_count'] = [0] * mixdb_out['num_classes']

        i_sample_offset = 0
        i_frame_offset = 0
        o_frame_offset = 0
        for m in mixid:
            mixture, truth_t, target, noise, segsnr, mixdb_tmp = genmix(mixdb=mixdb_out,
                                                                        mixid=m,
                                                                        compute_segsnr=compute_segsnr,
                                                                        compute_truth=compute_truth,
                                                                        logging=False,
                                                                        progress=progress,
                                                                        initial_i_sample_offset=i_sample_offset,
                                                                        initial_i_frame_offset=i_frame_offset,
                                                                        initial_o_frame_offset=o_frame_offset)

            samples = mixture.shape[0]
            if compute_truth:
                if samples != truth_t.shape[0]:
                    raise SonusAIError(
                        f'truth_t samples does not match mixture samples: {truth_t.shape[0]} != {samples}')
                if mixdb_out['num_classes'] != truth_t.shape[1]:
                    raise SonusAIError(
                        f'truth_t num_classes is incorrect: {truth_t.shape[1]} != {mixdb_out["num_classes"]}')
            if samples != target.shape[0]:
                raise SonusAIError(f'target samples does not match mixture samples: {target.shape[0]} != {samples}')
            if samples != noise.shape[0]:
                raise SonusAIError(f'noise samples does not match mixture samples: {noise.shape[0]} != {samples}')
            if compute_segsnr and samples != segsnr.shape[0]:
                raise SonusAIError(f'segsnr samples does not match mixture samples: {segsnr.shape[0]} != {samples}')

            with h5py.File(output_name, 'a') as f:
                indices = slice(i_sample_offset, i_sample_offset + samples)

                mixture_dataset = f['mixture']
                mixture_dataset[indices] = mixture

                if compute_truth:
                    truth_dataset = f['truth_t']
                    truth_dataset[indices] = truth_t

                target_dataset = f['target']
                target_dataset[indices] = target

                noise_dataset = f['noise']
                noise_dataset[indices] = noise

                if compute_segsnr:
                    segsnr_dataset = f['segsnr']
                    segsnr_dataset[indices] = segsnr

            for idx, val in enumerate(m):
                mixdb_out['mixtures'][val] = mixdb_tmp['mixtures'][idx]
            for idx in range(mixdb_out['num_classes']):
                mixdb_out['class_count'][idx] += mixdb_tmp['class_count'][idx]

            i_sample_offset = mixdb_out['mixtures'][m[-1]]['i_sample_offset']
            i_sample_offset += get_samples_in_mixture(mixdb_out, m[-1])
            i_frame_offset = mixdb_out['mixtures'][m[-1]]['i_frame_offset']
            i_frame_offset += get_transform_frames_in_mixture(mixdb_out, m[-1])
            o_frame_offset = mixdb_out['mixtures'][m[-1]]['o_frame_offset']
            o_frame_offset += get_feature_frames_in_mixture(mixdb_out, m[-1])

        with h5py.File(output_name, 'a') as f:
            f.attrs['mixdb'] = json.dumps(mixdb_out)

        progress.close()

        logger.info(f'Wrote {output_name}')
        duration = total_samples / sonusai.mixture.SAMPLE_RATE
        logger.info('')
        logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
        logger.info(f'mixture:  {human_readable_size(i_sample_offset * 2, 1)}')
        if compute_truth:
            logger.info(f'truth_t:  {human_readable_size(i_sample_offset * mixdb_out["num_classes"] * 4, 1)}')
        logger.info(f'target:   {human_readable_size(i_sample_offset * 2, 1)}')
        logger.info(f'noise:    {human_readable_size(i_sample_offset * 2, 1)}')
        if compute_segsnr:
            logger.info(f'segsnr:   {human_readable_size(i_sample_offset * 4, 1)}')

        end_time = time.monotonic()
        logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
