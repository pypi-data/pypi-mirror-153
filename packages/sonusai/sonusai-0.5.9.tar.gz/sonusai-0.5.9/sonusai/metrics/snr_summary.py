import warnings
from typing import List
from typing import Union

import numpy as np
import pandas as pd

from sonusai.metrics.one_hot import one_hot
from sonusai.mixture.get_mixid_data import get_mixid_data
from sonusai.queries.queries import get_mixids_from_snr


def snr_summary(mixdb: dict,
                mixid: Union[str, List[int]],
                truth_f: np.ndarray,
                predict: np.ndarray,
                segsnr: Union[np.ndarray, None] = None,
                pred_thr: Union[float, List[float]] = 0,
                truth_thr: float = 0.5,
                timesteps: int = 0) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, dict):
    """Calculate average-over-class metrics per SNR over specified mixture list.
       Inputs:
         mixdb        mixture database (SonusAI JSON format)
         mixid
         truth_f      truth/labels      #features x num_classes
         predict      prediction data / neural net model one-hot out,  #features x num_classes
         segsnr       segmental snr from SonusAI genft,  #transform frames x 1
         pred_thr     decision threshold(s) applied to predict data, allowing predict to be
                      continuous probabilities or decisions
         truth_thr    decision threshold(s) applied to truth data, allowing truth to be
                      continuous probabilities or decisions.  Default 0.5

       Default pred_thr=0 will infer 0.5 for multi-label mode (truth_mutex = False), or
       if single-label mode (truth_mutex == True) then ignore and use argmax mode, and
       the confusion matrix is calculated for all classes.

       Returns pandas dataframe (snrdf) of metrics per snr.
    """
    num_classes = truth_f.shape[1]

    mxid_snro = get_mixids_from_snr(mixdb=mixdb, mixid=mixid)

    # Check pred_thr array or scalar and return final scalar pred_thr value
    if not mixdb['truth_mutex'] and num_classes > 1:
        if np.ndim(pred_thr) == 0 and pred_thr == 0:
            pred_thr = 0.5  # multi-label pred_thr scalar 0 force to 0.5 default

        if np.ndim(pred_thr) == 1:
            if len(pred_thr) == 1:
                if pred_thr[0] == 0:
                    # multi-label pred_thr array scalar 0 force to 0.5 default
                    pred_thr = 0.5
                else:
                    # multi-label pred_thr array set to scalar = array[0]
                    pred_thr = pred_thr[0]

    if segsnr is not None:
        # prep segsnr if provided, transform frames to feature frames via mean()
        # expected to always be an integer
        NFF = int(segsnr.shape[0] / truth_f.shape[0])
        segsnr_f = np.mean(np.reshape(segsnr, (truth_f.shape[0], NFF)), axis=1, keepdims=True)
        ssnr_stats = np.zeros((len(mxid_snro), 3), dtype=float)

    macro_avg = np.zeros((len(mxid_snro), 7), dtype=float)
    micro_avg = np.zeros((len(mxid_snro), 7), dtype=float)
    wghtd_avg = np.zeros((len(mxid_snro), 7), dtype=float)
    ii = 0
    for snrkey in mxid_snro:
        ytrue, ypred = get_mixid_data(mixdb, mxid_snro[snrkey], truth_f, predict)
        _, metrics, _, _, _, mavg = one_hot(ytrue, ypred, pred_thr, truth_thr, timesteps)

        # mavg macro, micro, weighted: [PPV, TPR, F1, FPR, ACC, mAP, mAUC, TPSUM]
        macro_avg[ii, :] = mavg[0, 0:7]
        micro_avg[ii, :] = mavg[1, 0:7]
        wghtd_avg[ii, :] = mavg[2, 0:7]
        if segsnr is not None:
            ytrue, ysegsnr = get_mixid_data(mixdb, mxid_snro[snrkey], truth_f, segsnr_f)
            with warnings.catch_warnings():
                warnings.filterwarnings(action='ignore', message='divide by zero encountered in log10')
                # segmental SNR mean = mixture_snr and target_snr
                ssnr_stats[ii, 0] = 10 * np.log10(np.mean(ysegsnr))
                # seg SNR 80% percentile
                ssnr_stats[ii, 1] = 10 * np.log10(np.percentile(ysegsnr, 80, interpolation='midpoint'))
                # seg SNR max
                ssnr_stats[ii, 2] = 10 * np.log10(max(ysegsnr))

        ii = ii + 1

    # SNR format SNR: PPV, TPR, F1, FPR, ACC, AP, AUC, SNRSEG80P
    col_n = ['PPV', 'TPR', 'F1', 'FPR', 'ACC', 'AP', 'AUC']
    snr_macrodf = pd.DataFrame(macro_avg, index=list(mxid_snro.keys()), columns=col_n)
    snr_macrodf.sort_index(ascending=False, inplace=True)

    snr_microdf = pd.DataFrame(micro_avg, index=list(mxid_snro.keys()), columns=col_n)
    snr_microdf.sort_index(ascending=False, inplace=True)

    snr_wghtdf = pd.DataFrame(wghtd_avg, index=list(mxid_snro.keys()), columns=col_n)
    snr_wghtdf.sort_index(ascending=False, inplace=True)

    # Add segmental snr columns if provided
    if segsnr is not None:
        ssnrdf = pd.DataFrame(ssnr_stats, index=list(mxid_snro.keys()), columns=['SSNRavg', 'SSNR80p', 'SSNRmax'])
        ssnrdf.sort_index(ascending=False, inplace=True)
        snr_macrodf = pd.concat([snr_macrodf, ssnrdf], axis=1)
        snr_microdf = pd.concat([snr_microdf, ssnrdf], axis=1)
        snr_wghtdf = pd.concat([snr_wghtdf, ssnrdf], axis=1)

    return snr_macrodf, snr_microdf, snr_wghtdf, mxid_snro
