import warnings

import numpy as np
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_auc_score

from sonusai import logger
from sonusai.utils.reshape import reshape_truth_predict


def one_hot(truth: np.ndarray,
            predict: np.ndarray,
            predict_thr: float = 0,
            truth_thr: float = 0.5,
            timesteps: int = -1) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    """ Calculates metrics from one-hot prediction and truth data (numpy float arrays) where
        both are one-hot probabilities (or quantized decisions) for each class
        with size frames x num_classes or frames x timesteps x num_classes.
        For metrics that require it, truth and pred decisions will be made using threshold >= pthr.
        Some metrics like AP and AUC do not depend on pthr for predict, but still use truth >= pthr

        pred_thr sets the decision threshold(s) applied to predict data for some metrics, thus allowing
        the input to be continuous probabilities, for AUC-type metrics and root mean square error (rmse).
        1. Default = 0 (multiclass or binary) which infers:
           binary (nclass = 1)         use >= 0.5 for truth and pred (same as argmax() for binary)
           multi-class/single-label    if truth_mutex= = true, use argmax() used on both truth and pred
           note multi-label metrics are disabled for pthr = 0, must set pthr > 0

        2. pthr > 0 (multilabel or binary) scalar or a vector num_class x 1 then use
           pthr as a binary decision threshold in each class:
           binary (nclass = 1)         use >= pthr[0] for pred and pthr[num_classes+1] for truth
                                       if it exists, else use >= 0.5 for truth
           multi-label                 use >= pthr for pred if scalar, or pthr[class_idx] if vector
                                       use >= pthr[num_classes+1] for truth if exists, else 0.5
           note multi-class/single-label inputs are meaningless in this mode, use pthr = 0 argmax mode

        num_classes is inferred from 1D, 2D or 3D truth inputs by default (default tstep = -1 or 0).
        Only set tstep > 0 in case of ambiguous binary 2D case where input frames x timesteps,
        then it must set to the number of timesteps = TSTEPS (which will be > 0).
        It is safe to always set tstep <= 0 for binary inputs, and if truth_shape[2] exists

        returns metrics over all frames + timesteps:
        mcm      num_classes x 2 x 2         multiclass confusion matrix count ove
        metrics  num_classes x 14            [ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP, AP, AUC]
        cm, cmn: num_classes x num_classes   confusion matrix, normalized confusion matrix
        rmse:    num_classes x 1             RMS error over all frames + timesteps, before threshold decision
        mavg:    3x8 averages                macro,micro,weighted [PPV, TPR, F1, FPR, ACC, mAP, mAUC, TPSUM]
    """
    if truth.shape != predict.shape:
        logger.error('Shape of truth and predict are not equal')
        exit()

    truth, predict, num_classes = reshape_truth_predict(truth, predict, timesteps)

    # Regression metric root-mean-square-error always works
    rmse = np.sqrt(np.mean(np.square(truth - predict), axis=0))

    # Calc default predict decision thresholds based on mode
    if not np.ndim(predict_thr) and predict_thr == 0:
        # if scalar and 0, set defaults
        if num_classes == 1:
            # binary case default >= 0.5 which is equiv to argmax()
            predict_thr = np.atleast_1d(0.5)
        else:
            # multiclass, single-label (argmax mode)
            predict_thr = np.atleast_1d(0)
    else:
        if np.ndim(predict_thr) > 1:
            # multi-label with custom thr vector
            assert predict_thr.shape[0] == num_classes
        else:
            if predict_thr == 0:
                # binary or multi-label scalar default
                predict_thr = np.atleast_1d(0.5)
            else:
                # user specified binary or multi-label scalar
                predict_thr = np.atleast_1d(predict_thr)

    # if predict_thr[0] == 0 and num_classes > 1:  # if scalar
    #     pthr = 0.5  # multiclass, single-label (argmax) or multilabel case default
    # else:
    #     if num_classes == 1 and predict_thr[0] == 0:
    #         pthr = 0.5  # binary case default >= 0.5 which is equiv to argmax()
    #     else:
    #         pthr = pthr  # any case using specified threshold

    # Convert continuous probabilities to binary via argmax() or threshold comparison
    # and create labels of int encoded (0:num_classes-1), and then equivalent one-hot
    if num_classes == 1:  # If binary
        binary_mode = True
        labels = ([i for i in range(0, 2)])  # int encoded 0,1
        plabel = np.int8(predict >= predict_thr)  # frames x 1, default 0.5 is equiv. to argmax()
        tlabel = np.int8(truth >= truth_thr)  # frames x 1
        predb = plabel
        truthb = tlabel
    else:
        binary_mode = False
        labels = ([i for i in range(0, num_classes)])  # int encoded 0,...,num_classes-1
        if predict_thr[0] == 0:  # multiclass single-label (mutex), use argmax
            plabel = np.argmax(predict, axis=-1)  # frames x 1 labels
            tlabel = np.argmax(truth, axis=-1)  # frames x 1 labels
            predb = np.zeros(predict.shape, dtype=np.int8)  # frames x num_classes one-hot binary
            truthb = np.zeros(truth.shape, dtype=np.int8)  # frames x num_classes one-hot binary
            predb[np.arange(predb.shape[0]), plabel] = 1  # single-label frames x num_classes
            if np.sum(truth):  # special case all zero truth leave tlabel all zeros
                truthb[np.arange(truthb.shape[0]), tlabel] = 1  # single-label frames x num_classes
        else:  # multi-label prob threshold comparison (multiple classes)
            predb = np.int8(predict >= predict_thr.transpose())  # frames x num_classes multilabel one-hot decision
            truthb = np.int8(truth >= truth_thr)  # frames x num_classes multilabel one-hot decision
            # Return argmax() for optional single-label confusion matrix metrics
            plabel = np.argmax(predict, axis=-1)  # frames x 1 labels
            tlabel = np.argmax(truth, axis=-1)  # frames x 1 labels

    # debug checks to understand ap, auc:
    # from sklearn.metrics import roc_curve
    # fpr, tpr, thr = roc_curve(truthb[:,0],predict[:,0],drop_intermediate=False)
    # from sklearn.metrics import precision_recall_curve
    # precision, recall, thr  = precision_recall_curve(truthb[:,0], predict[:,0])
    # from sklearn.metrics import RocCurveDisplay
    # RocCurveDisplay.from_predictions(truthb[:,0],predict[:,0])  # Plot ROC class0

    # Create nclass x 2 x 2 multi-label confusion matrix (mcm)
    # Note - must include labels or sklearn func. will omit non-exiting classes
    mcm = multilabel_confusion_matrix(truthb, predb, labels=labels)

    if num_classes == 1:
        mcm = mcm[1:]  # remove dim 0 if binary

    # Create num_classes x num_classes normalized confusion matrix
    cmn = confusion_matrix(tlabel, plabel, labels=labels, normalize='true')

    # Create num_classes x num_classes confusion matrix
    cm = confusion_matrix(tlabel, plabel, labels=labels)

    # Combine all per-class metrics into a single array
    # [ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP, AP, AUC]
    metrics = np.zeros((num_classes, 14))
    # threshold_optpr = np.zeros((num_classes, 1))
    eps = np.finfo(float).eps
    for nci in range(num_classes):
        # True negative
        TN = mcm[nci, 0, 0]
        # False positive
        FP = mcm[nci, 0, 1]
        # False negative
        FN = mcm[nci, 1, 0]
        # True positive
        TP = mcm[nci, 1, 1]
        # Accuracy
        ACC = (TP + TN) / (TP + TN + FP + FN + eps)
        # True positive rate, sensitivity, recall, hit rate (note eps in numerator)
        # When ``true positive + false negative == 0``, recall is undefined, set to 0
        TPR = (TP) / (TP + FN + eps)
        # Precision, positive predictive value
        # When ``true positive + false positive == 0``, precision is undefined, set to 0
        PPV = TP / (TP + FP + eps)
        # Specificity i.e., selectivity, or true negative rate
        TNR = TN / (TN + FP + eps)
        # False positive rate = 1-specificity, roc x-axis
        FPR = FP / (TN + FP + eps)
        # HitFA used by some separation research, close match to MCC
        HITFA = TPR - FPR
        # F1 harmonic mean of precision, recall = 2*PPV*TPR / (PPV + TPR)
        F1 = 2 * TP / (2 * TP + FP + FN + eps)
        # Matthew correlation coefficient
        MCC = (TP * TN - FP * FN) / (np.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) + eps)
        # Num. negatives total (truth), also = TN+FP denom of FPR
        NT = sum(mcm[nci, 0,])
        # Num. positives total (truth), also = FN+TP denom of TPR, precision
        PT = sum(mcm[nci, 1,])
        # Average Precision also called area under the PR curve AUCPR and
        # AUC ROC curve using binary-ized truth and continuous prediction probabilities
        # sklearn returns nan if no active truth in a class but w/un-suppressible div-by-zero warning
        if np.sum(truthb[:, nci]) == 0:  # if no active classes both sklearn will fail, set to NaN
            AUC = np.NaN
            AP = np.NaN
            # threshold_optpr[nci] = np.NaN
        else:
            AP = average_precision_score(truthb[:, nci], predict[:, nci], average=None)
            if len(np.unique(truthb[:, nci])) < 2:  # if active classes not > 1 AUC must be NaN
                AUC = np.NaN  # i.e. all ones sklearn auc will fail
            else:
                AUC = roc_auc_score(truthb[:, nci], predict[:, nci], average=None)
            # # Optimal threshold from PR curve, optimizes f-score
            # precision, recall, thresholds = precision_recall_curve(truthb[:, nci], predict[:, nci])
            # fscore = (2 * precision * recall) / (precision + recall)
            # ix = argmax(fscore)  # index of largest f1 score
            # threshold_optpr[nci] = thresholds[ix]

        metrics[nci] = [ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP, AP, AUC]

    # Calculate averages into single array, 3 types for now Macro, Micro, Weighted
    mavg = np.zeros((3, 8), dtype=np.single)
    s = np.sum(metrics[:, 9].astype(int))  # support = sum (true pos total = FN+TP ) over classes

    # macro average [PPV, TPR, F1, FPR, ACC, mAP, mAUC, TPSUM]
    with warnings.catch_warnings():
        warnings.filterwarnings(action='ignore', message='Mean of empty slice')
        mavg[0,] = [np.mean(metrics[:, 2]), np.mean(metrics[:, 1]), np.mean(metrics[:, 6]), np.mean(metrics[:, 4]),
                    np.mean(metrics[:, 0]), np.nanmean(metrics[:, 12]), np.nanmean(metrics[:, 13]), s]

    # micro average, micro-F1 = micro-precision = micro-recall = accuracy
    if num_classes > 1:
        tp_sum = np.sum(metrics[:, 10])  # TP all classes
        rm = tp_sum / (np.sum(metrics[:, 9]) + eps)  # micro mean PPV = TP / (PT=FN+TP)
        fp_sum = np.sum(metrics[:, 11])  # FP false-positives all classes
        fpm = fp_sum / (np.sum(metrics[:, 8]) + eps)  # micro mean FPR = FP / (NT=TN+FP)
        pm = tp_sum / (tp_sum + fp_sum + eps)  # micro mean TPR = TP / (TP+FP) (note: same as rm for micro-avg)
        fn_sum = sum(mcm[:, 1, 0])
        f1m = 2 * tp_sum / (2 * tp_sum + fp_sum + fn_sum + eps)
        tn_sum = sum(mcm[:, 0, 0])
        accm = (tp_sum + tn_sum) / (tp_sum + tn_sum + fp_sum + fn_sum + eps)
        with warnings.catch_warnings():
            warnings.filterwarnings(action='ignore', message='invalid value encountered in true_divide')
            miap = average_precision_score(truthb, predict, average='micro')
        if np.sum(truthb):  # no activity over all classes
            miauc = roc_auc_score(truthb, predict, average='micro')
        else:
            miauc = np.NaN

        # [miPPV, miTPR, miF1, miFPR, miACC, miAP, miAUC, TPSUM]
        mavg[1,] = [pm, rm, f1m, fpm, accm, miap, miauc, s]  # specific format, last 3 are unique

        # weighted average TBD
        wp, wr, wf1, _ = precision_recall_fscore_support(truthb, predb, average='weighted', zero_division=0)
        if np.sum(truthb):
            taidx = np.sum(truthb, axis=0) > 0
            wap = average_precision_score(truthb[:, taidx], predict[:, taidx], average='weighted')
            if len(np.unique(truthb[:, taidx])) < 2:
                wauc = np.NaN
            else:
                wauc = roc_auc_score(truthb[:, taidx], predict[:, taidx], average='weighted')
        else:
            wap = np.NaN
            wauc = np.NaN

        mavg[2, :] = [wp, wr, wf1, 0, 0, wap, wauc, s]
    else:  # binary case, all are same
        mavg[1,] = mavg[0,]
        mavg[2,] = mavg[0,]

    return mcm, metrics, cm, cmn, rmse, mavg
