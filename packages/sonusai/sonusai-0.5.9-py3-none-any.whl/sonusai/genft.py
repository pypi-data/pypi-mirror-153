"""sonusai genft

usage: genft [-hvs] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database JSON file.
    -i MIXID, --mixid MIXID         Mixture IDs JSON file.
    -o OUTPUT, --output OUTPUT      Output HDF5 file.
    -s, --segsnr                    Save segsnr. [default: False].

Generate a SonusAI feature/truth file from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database JSON file.
    MIXID       A JSON file containing a list of mixture IDs. The list should be named 'mixid'.
                If no file is provided, then all mixtures in the database will be generated.

Outputs:
    OUTPUT.h5   A SonusAI feature HDF5 file. Contains:
                    dataset:    feature
                    dataset:    truth_f
                    dataset:    segsnr (optional)
                    attribute:  mixdb
    genft.log

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
from pyaaware import FeatureGenerator
from pyaaware import ForwardTransform
from tqdm import tqdm

import sonusai
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
from sonusai.mixture import truth_reduction
from sonusai.utils import grouper
from sonusai.utils import human_readable_size
from sonusai.utils import int16_to_float
from sonusai.utils import p_tqdm_map
from sonusai.utils import seconds_to_hms
from sonusai.utils import to_numpy_array
from sonusai.utils import trim_docstring

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


# noinspection PyGlobalUndefined

def mp_init(feature_: multiprocessing.Array,
            truth_f_: multiprocessing.Array,
            segsnr_: multiprocessing.Array) -> None:
    global mp_feature
    global mp_truth_f
    global mp_segsnr

    mp_feature = feature_
    mp_truth_f = truth_f_
    mp_segsnr = segsnr_


def init(mixdb: dict,
         mixid: Union[str, List[int]],
         logging: bool = True) -> (dict, int, int, int):
    mixdb_out = new_mixdb_from_mixid(mixdb=mixdb, mixid=mixid)

    total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])
    transform_frames = total_samples // mixdb_out['frame_size']
    feature_frames = total_samples // mixdb_out['feature_step_samples']

    if logging:
        logger.info('')
        logger.info(f'Found {len(mixdb_out["mixtures"]):,} mixtures to process')
        logger.info(f'{total_samples:,} samples, '
                    f'{transform_frames:,} transform frames, '
                    f'{feature_frames:,} feature frames')

    return mixdb_out, total_samples, transform_frames, feature_frames


def genft(mixdb: dict,
          mixid: Union[str, List[int]],
          compute_segsnr: bool = False,
          logging: bool = True,
          show_progress: bool = False,
          progress: tqdm = None,
          initial_i_sample_offset: int = 0,
          initial_i_frame_offset: int = 0,
          initial_o_frame_offset: int = 0) -> (np.ndarray, np.ndarray, dict):
    mixdb_out, total_samples, transform_frames, feature_frames = init(mixdb=mixdb, mixid=mixid, logging=logging)

    MP_DICT['mixdb'] = mixdb_out
    MP_DICT['feature_frames'] = feature_frames
    MP_DICT['compute_segsnr'] = compute_segsnr
    MP_DICT['target_audios'] = build_target_audio_db(mixdb=mixdb_out, show_progress=show_progress)
    MP_DICT['noise_audios'] = build_noise_audio_db(mixdb=mixdb_out, show_progress=show_progress)

    fg = FeatureGenerator(frame_size=mixdb_out['frame_size'],
                          feature_mode=mixdb_out['feature'],
                          num_classes=mixdb_out['num_classes'],
                          truth_mutex=mixdb_out['truth_mutex'])
    mp_feature = multiprocessing.Array(ctypes.c_float, feature_frames * fg.stride * fg.num_bands)
    mp_truth_f = multiprocessing.Array(ctypes.c_float, feature_frames * fg.num_classes)
    if compute_segsnr:
        mp_segsnr = multiprocessing.Array(ctypes.c_float, transform_frames)
    else:
        mp_segsnr = multiprocessing.Array(ctypes.c_float, 0)

    feature = to_numpy_array(mp_feature, dtype=np.single).reshape((feature_frames, fg.stride, fg.num_bands))
    truth_f = to_numpy_array(mp_truth_f, dtype=np.single).reshape((feature_frames, fg.num_classes))
    if compute_segsnr:
        segsnr = to_numpy_array(mp_segsnr, dtype=np.single)
    else:
        segsnr = np.empty(0, dtype=np.single)

    # First pass to get offsets
    set_mixture_offsets(mixdb=mixdb_out,
                        initial_i_sample_offset=initial_i_sample_offset,
                        initial_i_frame_offset=initial_i_frame_offset,
                        initial_o_frame_offset=initial_o_frame_offset)

    # Second pass to get feature and truth_f
    progress_needs_close = False
    if progress is None:
        progress = tqdm(total=len(mixdb_out['mixtures']), desc='genft', disable=not show_progress)
        progress_needs_close = True

    p_tqdm_map(_process_mixture,
               list(range(len(mixdb_out['mixtures']))),
               progress=progress,
               initializer=mp_init,
               initargs=(mp_feature, mp_truth_f, mp_segsnr))

    if progress_needs_close:
        progress.close()

    mixdb_out['class_count'] = get_total_class_count(mixdb_out)

    duration = total_samples / sonusai.mixture.SAMPLE_RATE
    if logging:
        logger.info('')
        logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
        logger.info(f'feature:  {human_readable_size(feature.nbytes, 1)}')
        logger.info(f'truth_f:  {human_readable_size(truth_f.nbytes, 1)}')
        if compute_segsnr:
            logger.info(f'segsnr:   {human_readable_size(segsnr.nbytes, 1)}')

    return feature, truth_f, segsnr, mixdb_out


def _process_mixture(mixid: int) -> None:
    mixdb = MP_DICT['mixdb']
    feature_frames = MP_DICT['feature_frames']
    target_audios = MP_DICT['target_audios']
    noise_audios = MP_DICT['noise_audios']
    compute_segsnr = MP_DICT['compute_segsnr']

    fft = ForwardTransform(N=mixdb['frame_size'] * 4,
                           R=mixdb['frame_size'])

    fg = FeatureGenerator(frame_size=mixdb['frame_size'],
                          feature_mode=mixdb['feature'],
                          num_classes=mixdb['num_classes'],
                          truth_mutex=mixdb['truth_mutex'])

    feature = to_numpy_array(mp_feature, dtype=np.single)
    feature = feature.reshape((feature_frames, fg.stride, fg.num_bands))

    truth_f = to_numpy_array(mp_truth_f, dtype=np.single)
    truth_f = truth_f.reshape((feature_frames, fg.num_classes))

    segsnr = to_numpy_array(mp_segsnr, dtype=np.single)

    record = mixdb['mixtures'][mixid]
    first_i_frame_offset = mixdb['mixtures'][0]['i_frame_offset']
    transform_frames = get_transform_frames_in_mixture(mixdb, mixid)

    frame_indices = slice(record['i_frame_offset'] - first_i_frame_offset,
                          record['i_frame_offset'] - first_i_frame_offset + transform_frames)

    (mixture_td,
     truth_t,
     _,
     _,
     segsnr[frame_indices]) = get_audio_and_truth_t(mixdb=mixdb,
                                                    record=record,
                                                    target_audios=target_audios,
                                                    noise_audios=noise_audios,
                                                    compute_truth=True,
                                                    compute_segsnr=compute_segsnr,
                                                    frame_based_segnsr=True)

    first_o_frame_offset = mixdb['mixtures'][0]['o_frame_offset']
    feature_frame = record['o_frame_offset'] - first_o_frame_offset
    for transform_frame in range(transform_frames):
        indices = slice(transform_frame * mixdb['frame_size'],
                        (transform_frame + 1) * mixdb['frame_size'])
        mixture_fd = fft.execute(int16_to_float(mixture_td[indices]))

        fg.execute(mixture_fd, truth_reduction(truth_t[indices], mixdb['truth_reduction_function']))

        if fg.eof():
            feature[feature_frame] = fg.feature()
            truth_f[feature_frame] = fg.truth()
            feature_frame += 1


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        mixid_name = args['--mixid']
        output_name = args['--output']
        compute_segsnr = args['--segsnr']

        if not output_name:
            output_name = splitext(mixdb_name)[0] + '.h5'

        start_time = time.monotonic()

        log_name = 'genft.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('genft')

        logger.info(f'\nLoad mixture database from {mixdb_name}')
        mixdb = load_mixdb(name=mixdb_name)
        mixid = load_mixid(name=mixid_name, mixdb=mixdb)

        mixdb_out, total_samples, transform_frames, feature_frames = init(mixdb=mixdb,
                                                                          mixid=mixid,
                                                                          logging=True)

        check_audio_files_exist(mixdb)

        fg = FeatureGenerator(frame_size=mixdb_out['frame_size'],
                              feature_mode=mixdb_out['feature'],
                              num_classes=mixdb_out['num_classes'],
                              truth_mutex=mixdb_out['truth_mutex'])

        with h5py.File(output_name, 'w') as f:
            f.create_dataset(name='feature',
                             shape=(feature_frames, fg.stride, fg.num_bands),
                             dtype=np.single)
            f.create_dataset(name='truth_f',
                             shape=(feature_frames, fg.num_classes),
                             dtype=np.single)
            if compute_segsnr:
                f.create_dataset(name='segsnr',
                                 shape=(transform_frames,),
                                 dtype=np.single)

        chunk_size = 100
        progress = tqdm(total=len(mixid), desc='genft')
        mixid = grouper(range(len(mixdb_out['mixtures'])), chunk_size)
        mixdb_out['class_count'] = [0] * mixdb_out['num_classes']

        i_sample_offset = 0
        i_frame_offset = 0
        o_frame_offset = 0
        for m in mixid:
            feature, truth_f, segsnr, mixdb_tmp = genft(mixdb=mixdb_out,
                                                        mixid=m,
                                                        compute_segsnr=compute_segsnr,
                                                        logging=False,
                                                        progress=progress,
                                                        initial_i_sample_offset=i_sample_offset,
                                                        initial_i_frame_offset=i_frame_offset,
                                                        initial_o_frame_offset=o_frame_offset)
            o_frames = feature.shape[0]
            if o_frames != truth_f.shape[0]:
                logger.exception(f'truth_f frames does not match feature frames: {truth_f.shape[0]} != {o_frames}')
                raise SystemExit(1)

            with h5py.File(output_name, 'a') as f:
                indices = slice(o_frame_offset, o_frame_offset + o_frames)

                feature_dataset = f['feature']
                feature_dataset[indices] = feature

                truth_dataset = f['truth_f']
                truth_dataset[indices] = truth_f

                if compute_segsnr:
                    segsnr_dataset = f['segsnr']
                    segsnr_dataset[i_frame_offset:i_frame_offset + segsnr.shape[0]] = segsnr

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
        logger.info(f'feature:  {human_readable_size(o_frame_offset * fg.stride * fg.num_bands * 4, 1)}')
        logger.info(f'truth_f:  {human_readable_size(o_frame_offset * fg.num_classes * 4, 1)}')
        if compute_segsnr:
            logger.info(f'segsnr:   {human_readable_size(i_frame_offset * 4, 1)}')

        end_time = time.monotonic()
        logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
