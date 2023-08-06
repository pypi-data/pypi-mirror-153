from typing import List
from typing import Union

import numpy as np
import pandas as pd

from sonusai.metrics.one_hot import one_hot
from sonusai.mixture.get_mixid_data import get_mixid_data


def class_summary(mixdb: dict,
                  mixid: Union[str, List[int]],
                  truth_f,
                  predict,
                  pred_thr=0,
                  truth_thr=0.5,
                  timesteps=0):
    """ Calculate table of metrics per class, and averages for a list
        of mixtures using truth and prediction data features x num_classes
        Example:
        Generate multi-class metric summary into table, for example:
                        PPV     TPR      F1     FPR     ACC   AP  AUC  Support
            Class 1     0.71    0.80    0.75    0.00    0.99            44
            Class 2     0.90    0.76    0.82    0.00    0.99            128
            Class 3     0.86    0.82    0.84    0.04    0.93            789
            Other       0.94    0.96    0.95    0.18    0.92            2807

          micro-avg                     0.92    0.027                   3768
          macro avg     0.85    0.83    0.84    0.05    0.96            3768
          micro-avgwo
    """
    num_classes = truth_f.shape[1]

    ytrue, ypred = get_mixid_data(mixdb, mixid, truth_f, predict)
    # file_frame_segments = get_file_frame_segments(mixdb, mixid)
    # total_frames = sum([file_frame_segments[m].length for m in file_frame_segments])
    # ytrue = np.empty((total_frames, num_classes), dtype=np.single)
    # ypred = np.empty((total_frames, num_classes), dtype=np.single)
    # start = 0
    # for m in file_frame_segments:
    #     length = file_frame_segments[m].length
    #     ytrue[start:start + length] = truth_f[file_frame_segments[m].get_slice()]
    #     ypred[start:start + length] = predict[file_frame_segments[m].get_slice()]
    #     start += length

    if not mixdb['truth_mutex'] and num_classes > 1:
        if np.ndim(pred_thr) == 0 and pred_thr == 0:
            pred_thr = 0.5

        if np.ndim(pred_thr) == 1 and len(pred_thr) == 1:
            if pred_thr[0] == 0:
                pred_thr = 0.5

    _, metrics, _, _, _, metavg = one_hot(ytrue, ypred, pred_thr, truth_thr, timesteps)

    # [ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP, AP, AUC]
    tableidx = np.array([2, 1, 6, 4, 12, 13, 0, 9])
    col_n = ['PPV', 'TPR', 'F1', 'FPR', 'ACC', 'AP', 'AUC', 'Support']
    if mixdb['truth_mutex']:
        if len(mixdb['class_labels']) >= num_classes - 1:  # labels exist with or wo Other
            row_n = mixdb['class_labels']
            if len(mixdb['class_labels']) == num_classes - 1:  # Other label does not exist, so add it
                row_n.append('Other')
        else:
            row_n = ([f'Class {i}' for i in range(1, num_classes)])
            row_n.append('Other')
    else:
        if len(mixdb['class_labels']) == num_classes:
            row_n = mixdb['class_labels']
        else:
            row_n = ([f'Class {i}' for i in range(1, num_classes + 1)])

    df = pd.DataFrame(metrics[:, tableidx], columns=col_n, index=row_n)

    # [miPPV, miTPR, miF1, miFPR, miACC, miAP, miAUC, TPSUM]
    avg_row_n = ['Macro-avg', 'Micro-avg', 'Weighted-avg']
    dfavg = pd.DataFrame(metavg, columns=col_n, index=avg_row_n)

    # dfblank = pd.DataFrame([''])
    # pd.concat([df, dfblank, dfblank, dfavg])

    classdf = pd.concat([df, dfavg])
    # classdf = classdf.round(2)
    classdf['Support'] = classdf['Support'].astype(int)

    return classdf
