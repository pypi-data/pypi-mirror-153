"""sonusai evaluate

usage: evaluate [-hv] (-f FEATURE) (-n PREDICT) [-t PTHR] [-p PLOTNUM]

options:
   -h, --help
   -v, --verbose                    Be verbose.
   -f FEATURE, --feature FEATURE    Feature + truth .h5 data file
   -n PREDICT, --predict PREDICT    Predict .h5 data file.
   -t PTHR, --thr PTHR              Optional prediction decision threshold, 0 = argmax(). [default: 0].
   -p PLOTNUM, --plotnum PLOTNUM    Optional plot mixture results (-1 is plot all, 0 is plot none) [default: 0].

Evaluate calculates performance metrics of neural-network models from model prediction data and the associated
feature+truth data file.

Inputs:
    FEATURE     A SonusAI feature+truth HDF5 file. Contains:
                    attribute:  mixdb
                    dataset:    feature   Note: not required for metrics
                    dataset:    truth_f
                    dataset:    segsnr    Optional
    PREDICT     A SonusAI predict HDF5 file. Contains:
                    dataset:    predict (either [frames, num_classes] or [frames, timesteps, num_classes])
"""
import json
from datetime import datetime
from os import mkdir
from os.path import join
from pathlib import Path
from typing import Union

import h5py
import numpy as np
from docopt import docopt

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.metrics import calculate_optimal_thresholds
from sonusai.metrics import class_summary
from sonusai.metrics import snr_summary
from sonusai.queries.queries import get_mixids_from_snr
from sonusai.utils import human_readable_size
from sonusai.utils import read_predict_data
from sonusai.utils import reshape_truth_predict
from sonusai.utils import seconds_to_hms
from sonusai.utils import trim_docstring


def evaluate(mixdb: dict,
             truth: np.ndarray,
             predict: Union[None, np.ndarray],
             segsnr: Union[None, np.ndarray] = None,
             output_dir: Union[None, str, Path] = None,
             pred_thr: Union[float, np.ndarray] = 0.0,
             feature: Union[None, np.ndarray] = None,
             verbose: bool = False) -> None:
    update_console_handler(verbose)
    initial_log_messages('evaluate')

    if truth.shape[-1] != predict.shape[-1]:
        logger.exception(f'Number of classes in truth and predict are not equal. Exiting.')
        raise SystemExit(1)

    # truth, predict can be either frames x num_classes, or frames x timesteps x num_classes
    # in binary case dim may not exist, detect this and set num_classes == 1
    timesteps = -1
    truth, predict, num_classes = reshape_truth_predict(truth, predict, timesteps)

    fdiff = truth.shape[0] - predict.shape[0]
    if fdiff > 0:
        # truth = truth[0:-fdiff,:]
        predict = np.concatenate((predict, np.zeros((fdiff, num_classes))))
        logger.info(f'Truth has more feature-frames than predict, padding predict with zeros to match.')

    if fdiff < 0:
        predict = predict[0:fdiff, :]
        logger.info(f'Predict has more feature-frames than truth, trimming predict to match.')

    # Check segsnr, input is always in transform frames
    compute_segsnr = False
    if len(segsnr) > 0:
        segsnr_feature_frames = segsnr.shape[0] / (mixdb['feature_step_samples'] / mixdb['frame_size'])
        if segsnr_feature_frames == truth.shape[0]:
            compute_segsnr = True
        else:
            logger.warning('segsnr length does not match truth, ignoring.')

    # Check pred_thr array or scalar and return final scalar pred_thr value
    if not mixdb['truth_mutex']:
        if num_classes > 1:
            if np.ndim(pred_thr) == 0 and pred_thr == 0:
                pred_thr = 0.5  # multi-label pred_thr scalar 0 force to 0.5 default

            if np.ndim(pred_thr) == 1:
                if len(pred_thr) == 1:
                    if pred_thr[0] == 0:
                        pred_thr = 0.5  # multi-label pred_thr array scalar 0 force to 0.5 default
                    else:
                        pred_thr = pred_thr[0]  # multi-label pred_thr array set to scalar = array[0]

    else:
        pred_thr = 0  # single-label mode, force argmax mode

    if pred_thr == -1:
        thrpr, thrroc, _, _ = calculate_optimal_thresholds(truth, predict)
        pred_thr = np.atleast_1d(thrpr)
        pred_thr = np.maximum(pred_thr, 0.1)  # enforce lower limit 0.1
        pred_thr = np.minimum(pred_thr, 0.9)  # enforce upper limit 0.9
        pred_thr = pred_thr.round(2)

    # Summarize the mixture data
    num_mixtures = len(mixdb['mixtures'])
    total_samples = sum([sub['samples'] for sub in mixdb['mixtures']])
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Mixtures: {num_mixtures}')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'truth:    {human_readable_size(truth.nbytes, 1)}')
    logger.info(f'predict:  {human_readable_size(predict.nbytes, 1)}')
    if compute_segsnr:
        logger.info(f'segsnr:   {human_readable_size(segsnr.nbytes, 1)}')
    if feature:
        logger.info(f'feature:  {human_readable_size(feature.nbytes, 1)}')

    logger.info(f'Classes: {num_classes}')
    if mixdb['truth_mutex']:
        logger.info(f'Mode:  Single-label / truth_mutex / softmax')
    else:
        logger.info(f'Mode:  Multi-label / Binary')

    mxid_snro = get_mixids_from_snr(mixdb=mixdb)
    snrlist = list(mxid_snro.keys())
    snrlist.sort(reverse=True)
    logger.info(f'Ordered SNRs: {snrlist}\n')
    if type(pred_thr) is np.ndarray:
        logger.info(f'Prediction Threshold(s): {pred_thr.transpose()}\n')
    else:
        logger.info(f'Prediction Threshold(s): {pred_thr}\n')

    # Top-level report over all mixtures
    if compute_segsnr:
        macrodf, microdf, wghtdf, mxid_snro = snr_summary(mixdb, ':', truth, predict, segsnr, pred_thr)
    else:
        macrodf, microdf, wghtdf, mxid_snro = snr_summary(mixdb, ':', truth, predict, [], pred_thr)

    if num_classes > 1:
        logger.info(f'Metrics micro-avg per SNR over all {num_mixtures} mixtures:')
    else:
        logger.info(f'Metrics per SNR over all {num_mixtures} mixtures:')
    logger.info(microdf.round(3).to_string())
    logger.info('\n')
    if output_dir:
        microdf.round(3).to_csv(join(output_dir, 'snr.csv'))

    if mixdb['truth_mutex']:
        if compute_segsnr:
            macrodf, microdf, wghtdf, mxid_snro = snr_summary(mixdb, ':', truth[:, 0:-1], predict[:, 0:-1], segsnr,
                                                              pred_thr)
        else:
            macrodf, microdf, wghtdf, mxid_snro = snr_summary(mixdb, ':', truth[:, 0:-1], predict[:, 0:-1], [],
                                                              pred_thr)

        logger.info(f'Metrics micro-avg without "Other" class per SNR over all {num_mixtures} mixtures:')
        logger.info(microdf.round(3).to_string())
        logger.info('\n')
        if output_dir:
            microdf.round(3).to_csv(join(output_dir, 'snrwo.csv'))

    for snri in snrlist:
        mxids = mxid_snro[snri]
        classdf = class_summary(mixdb, mxids, truth, predict, pred_thr)
        logger.info(f'Metrics per class for SNR {snri} over {len(mxids)} mixtures:')
        logger.info(classdf.round(3).to_string())
        logger.info('\n')
        if output_dir:
            classdf.round(3).to_csv(join(output_dir, f'class_snr{snri}.csv'))


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        feature_name = args['--feature']
        predict_name = args['--predict']
        predict_threshold = float(args['--thr'])
        plot_number = int(args['--plotnum'])

        # create output directory
        output_dir = f'evaluate-{datetime.now():%Y%m%d}'
        try:
            mkdir(output_dir)
        except OSError as error:
            output_dir = f'evaluate-{datetime.now():%Y%m%d-%H%M%S}'
            try:
                mkdir(output_dir)
            except OSError as error:
                logger.error(f'Could not create directory, {output_dir}: {error}')
                raise SystemExit(1)

        log_name = output_dir + '/evaluate.log'
        create_file_handler(log_name)

        # mixdb, feature, truth, segsnr = read_feature_data(feature_name)
        with h5py.File(feature_name, 'r') as f:
            mixdb = json.loads(f.attrs['mixdb'])
            # feature = f['/feature'][:]  # No feature load saves significant time
            truth_f = f['/truth_f'][:]
            segsnr = f['/segsnr'][:]

        # mixture, target, noise = read_mixture_data(mixture_name)
        predict = read_predict_data(predict_name)

        evaluate(mixdb=mixdb,
                 truth=truth_f,
                 segsnr=segsnr,
                 output_dir=output_dir,
                 predict=predict,
                 pred_thr=predict_threshold,
                 verbose=args['--verbose'])

        logger.info(f'Wrote results to {output_dir}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
