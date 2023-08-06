import numpy as np
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

from sonusai import logger


def calculate_optimal_thresholds(truth: np.ndarray,
                                 predict: np.ndarray,
                                 truth_thr: float = 0.5) -> (np.ndarray, np.ndarray):
    """ Calculates optimal thresholds for each class from one-hot prediction and truth data
        (numpy float arrays) where both are one-hot probabilities (or quantized decisions)
        with size frames x num_classes or frames x timesteps x num_classes.

        Returns 2 threshold arrays num_classes x 1:
          thresholds_opt_pr:     optimal thesholds for PR-curve (F1) performance
          thresholds_opt_roc:    optimal thresholds for ROC-curve (TPR/FPR) performance

        Optional truth_thr is the decision threshold(s) applied to truth one-hot input thus allowing
        truth to optionally be continuous probabilities.  Default is 0.5.
    """
    if truth.shape != predict.shape:
        logger.error('Shape of truth and predict are not equal')
        exit()

    num_classes = -1
    # truth, predict can be either frames x num_classes, or frames x timesteps x num_classes
    # in binary case dim may not exist, detect this and set num_classes == 1
    if truth.ndim == 3 or (truth.ndim == 2 and num_classes == 1):
        if truth.ndim == 2:  # has timesteps = truth.shape[1]
            num_classes = 1
        else:
            num_classes = truth.shape[2]  # frames = truth.shape[0], timesteps = truth.shape[1]
        # reshape to remove timestep dimension
        truth = np.reshape(truth, (truth.shape[0] * truth.shape[1], truth.shape[2]))
        predict = np.reshape(predict, (predict.shape[0] * predict.shape[1], predict.shape[2]))
    else:
        if truth.ndim == 1:  # no timesteps dimension, = 0
            num_classes = 1
        else:
            num_classes = truth.shape[1]  # frames = truth.shape[0]

    # Apply decision to truth input
    truthb = np.int8(truth >= truth_thr)

    AP = np.zeros((num_classes, 1))
    AUC = np.zeros((num_classes, 1))
    thresholds_opt_pr = np.zeros((num_classes, 1))
    thresholds_opt_roc = np.zeros((num_classes, 1))
    eps = np.finfo(float).eps
    for nci in range(num_classes):
        # Average Precision also called area under the PR curve AUCPR and
        # AUC ROC curve using binary-ized truth and continuous prediction probabilities
        # sklearn returns nan if no active truth in a class but w/un-suppressible div-by-zero warning
        if sum(truthb[:, nci]) == 0:  # no active truth must be NaN
            thresholds_opt_pr[nci] = np.NaN
            thresholds_opt_roc[nci] = np.NaN
            AUC[nci] = np.NaN
            AP[nci] = np.NaN
        else:
            AP[nci] = average_precision_score(truthb[:, nci], predict[:, nci], average=None)
            AUC[nci] = roc_auc_score(truthb[:, nci], predict[:, nci], average=None)

            # Optimal threshold from PR curve, optimizes f-score
            precision, recall, thrpr = precision_recall_curve(truthb[:, nci], predict[:, nci])
            fscore = (2 * precision * recall) / (precision + recall + eps)
            ix = np.argmax(fscore)  # index of largest f1 score
            thresholds_opt_pr[nci] = thrpr[ix]

            # Optimal threshold from ROC curve, optimizes J-statistic (TPR-FPR) or gmean
            fpr, tpr, thrroc = roc_curve(truthb[:, nci], predict[:, nci])
            # J = tpr - fpr                  # J can result in thr > 1
            gmeans = np.sqrt(tpr * (1 - fpr))  # gmean seems better behaved
            ix = np.argmax(gmeans)
            thresholds_opt_roc[nci] = thrroc[ix]

    return thresholds_opt_pr, thresholds_opt_roc, AP, AUC
