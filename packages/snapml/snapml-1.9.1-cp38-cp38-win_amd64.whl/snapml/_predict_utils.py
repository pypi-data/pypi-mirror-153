# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2018, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# *****************************************************************
from __future__ import print_function

import sys
import struct
import numpy as np
from scipy import sparse, stats
import os
import enum
from sklearn.preprocessing import normalize

from snapml.utils import _is_data_snapml_partition_type, _verify_inference_dtype


class PredictTypes(enum.Enum):
    linear_prediction = 1
    linear_classification = 2
    logistic_probabilities = 3


# Common predict setup code
def _predict_common_processing(model_obj, X, _is_regression, _mpi_enabled):
    num_ex = 0
    num_ft = 0
    indptr = np.array([])
    indices = np.array([])
    data = np.array([])
    X_ptr_ = ""
    X_type_ = -1

    num_classes = 0 if _is_regression else model_obj.get_num_classes()

    _shortcut_predict = True

    if _is_data_snapml_partition_type(X):
        X_ptr_ = X.ptr_
        X_type_ = X.type_
        _shortcut_predict = False

    else:
        if _mpi_enabled:
            _verify_inference_dtype(type(X).__name__)
            _shortcut_predict = False

        num_ex = X.shape[0]
        num_ft = X.shape[1]

        if type(X).__name__ == "csc_matrix":
            X = X.tocsr()
            indptr = X.indptr.astype(np.uint64)
            data = X.data.astype(np.float32)
            indices = X.indices.astype(np.uint32)
        elif type(X).__name__ == "csr_matrix":
            indptr = X.indptr.astype(np.uint64)
            data = X.data.astype(np.float32)
            indices = X.indices.astype(np.uint32)
        elif type(X).__name__ == "ndarray":
            data = X.astype(np.float32)
            data = np.ascontiguousarray(data)  # ensure row-major format
            indptr = np.array([])
            indices = np.array([])
        else:
            raise ValueError("X should be in csc_matrix, csr_matrix or ndarray format.")

    return (
        num_ex,
        num_ft,
        num_classes,
        X_ptr_,
        X_type_,
        indptr,
        indices,
        data,
        _shortcut_predict,
    )


# Single observation prediction
def _lr_single_row_predict(model, fit_intercept, intercept_scaling, X, predict_type):
    _pred = np.empty(0)
    pred = np.empty(0)
    n_models = model.shape[0]

    # Loop to handle multi-class case
    for loop in range(n_models):
        flat_model = model[loop]
        if fit_intercept == False:
            dp = X.dot(flat_model)
        else:
            dp = X.dot(flat_model[0:-1])
            dp += flat_model[-1] * intercept_scaling
        if (n_models > 1) and (predict_type == PredictTypes.linear_classification):
            # Handle linear_classification with multi-class
            dp = 1 / (1 + np.exp(-dp))
        _pred = np.append(_pred, dp)

    if n_models == 1:
        # Binary
        if predict_type == PredictTypes.linear_prediction:
            pred = _pred.reshape(1)
        elif predict_type == PredictTypes.linear_classification:
            pred = np.where(_pred > 0.0, 1.0, -1.0)
        elif predict_type == PredictTypes.logistic_probabilities:
            proba = 1 / (1 + np.exp(-_pred[0]))
            pred = np.append(pred, (1 - proba))
            pred = np.append(pred, proba)
            pred = pred.reshape(1, 2)
    else:
        # Multiclass
        if predict_type == PredictTypes.linear_classification:
            pred = _pred.reshape(n_models, 1)  # shape required for argmax
        else:
            pred = _pred.reshape(1, n_models)
            if predict_type == PredictTypes.logistic_probabilities:
                proba = 1 / (1 + np.exp(-pred))
                pred = normalize(proba, norm="l1")

    return pred
