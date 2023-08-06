from typing import List
from typing import Union

import numpy as np
import pandas as pd

from sonusai.metrics.one_hot import one_hot
from sonusai.mixture.get_mixid_data import get_mixid_data


def confusion_matrix_summary(mixdb: dict,
                             mixid: Union[str, List[int]],
                             truth_f: np.ndarray,
                             predict: np.ndarray,
                             class_idx: int,
                             pred_thr: Union[float, List[float]] = 0,
                             truth_thr: float = 0.5,
                             timesteps: int = 0) -> (pd.DataFrame, pd.DataFrame):
    """Calculate confusion matrix for specified class, using truth and prediction
       data features x num_classes.

       pred_thr sets the decision threshold(s) applied to predict data, thus allowing
       predict to be continuous probabilities.

       Default pred_thr=0 will infer 0.5 for multi-label mode (truth_mutex = False), or
       if single-label mode (truth_mutex == True) then ignore and use argmax mode, and
       the confusion matrix is calculated for all classes.

       Returns pandas dataframes of confusion matrix cmdf and normalized confusion matrix cmndf.
    """
    num_classes = truth_f.shape[1]
    ytrue, ypred = get_mixid_data(mixdb=mixdb, mixid=mixid, truth_f=truth_f, predict=predict)

    # Check pred_thr array or scalar and return final scalar pred_thr value
    if not mixdb['truth_mutex'] and num_classes > 1:
        if np.ndim(pred_thr) == 0 and pred_thr == 0:
            # multi-label pred_thr scalar 0 force to 0.5 default
            pred_thr = 0.5

        if np.ndim(pred_thr) == 1:
            if len(pred_thr) == 1:
                if pred_thr[0] == 0:
                    # multi-label pred_thr array scalar 0 force to 0.5 default
                    pred_thr = 0.5
                else:
                    # multi-label pred_thr array set to scalar = array[0]
                    pred_thr = pred_thr[0]
            else:
                # multi-label pred_thr array scalar set = array[class_idx]
                pred_thr = pred_thr[class_idx]

    if len(mixdb['class_labels']) == num_classes:
        class_names = mixdb['class_labels']
    else:
        class_names = ([f'Class {i}' for i in range(1, num_classes + 1)])

    class_nums = ([f'{i}' for i in range(1, num_classes + 1)])

    if mixdb['truth_mutex']:
        # single-label mode force to argmax mode
        pred_thr = 0
        _, _, cm, cmn, _, _ = one_hot(ytrue, ypred, pred_thr, truth_thr, timesteps)
        row_n = class_names
        row_n[-1] = 'Other'
        # mux = pd.MultiIndex.from_product([['Single-label/mutex mode, truth thr = {}'.format(truth_thr)],
        #                                   class_nums])
        # mux = pd.MultiIndex.from_product([['truth thr = {}'.format(truth_thr)], class_nums])

        cmdf = pd.DataFrame(cm, index=row_n, columns=class_nums, dtype=int)
        cmndf = pd.DataFrame(cmn, index=row_n, columns=class_nums, dtype=float)

    else:
        _, _, cm, cmn, _, _ = one_hot(ytrue[:, class_idx], ypred[:, class_idx], pred_thr, truth_thr, timesteps)
        cname = class_names[class_idx]
        row_n = ['TrueN', 'TrueP']
        col_n = ['N-' + cname, 'P-' + cname]
        cmdf = pd.DataFrame(cm, index=row_n, columns=col_n, dtype=int)
        cmndf = pd.DataFrame(cmn, index=row_n, columns=col_n, dtype=float)
        # add thresholds in 3rd row
        pdnote = pd.DataFrame(np.atleast_2d([pred_thr, truth_thr]), index=['p/t thr:'], columns=col_n)
        cmdf = pd.concat([cmdf, pdnote])
        cmndf = pd.concat([cmndf, pdnote])

    return cmdf, cmndf
