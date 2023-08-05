# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2018, 2019. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# *****************************************************************

## @file
# @ingroup pythonutils

import sys
import numpy as np
from snapml.utils import _is_mpi_enabled, _is_data_snapml_partition_type

_mpi_enabled = _is_mpi_enabled()

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(_mpi_enabled)


def log_loss(data, proba):
    """
    Distributed logistic loss or cross-entropy loss metric.
    It supports both local and distributed(MPI) implementation.

    This metric is a loss function often used in logistic regression.
    It is defined as the negative log-likelihood of the true labels
    given the probabilities predicted by a classifier. In the current
    version it is defined for two labels only. This metric is implemented
    in a distributed manner for MPI execution.

    Parameters
    ----------
    data : Supports the following input data-types :
            1. Dense matrix (ndarray) of correct labels.
            2. SnapML data partition. This includes the correct labels.

    proba : Predicted probabilities of the two classes.
        array-like, shape = (n_samples, 2) for local implementation.
        array-like, shape = (n_samples,) for MPI implementation.

    Returns
    -------
    loss_value : float
        Returns the log loss of the predicted probabilities (proba) when
        compared with the true labels (data)
    """
    num_ex = 0
    data_ = np.array([])
    data_ptr_ = ""
    data_type_ = -1

    if not _mpi_enabled:
        # For snap-ml-local, get the probability of true case as required by library API
        proba = proba[:, 1].copy()

    if _is_data_snapml_partition_type(data):
        data_ptr_ = data.ptr_
        data_type_ = data.type_
    else:
        num_ex = data.shape[0]

        if type(data).__name__ == "ndarray":
            data_ = data.astype(np.float32)
        else:
            raise ValueError("data should be in ndarray format.")

    return libsnapml.log_loss(num_ex, data_, data_ptr_, data_type_, proba)


def accuracy_score(data, pred):
    """
    Distributed accuracy classification score.
    It supports both local and distributed(MPI) implementation.

    This metric is often used in multi-class classification to compute the
    class prediction accuracy. It currently supports binary classification only.
    The metric is implemented in a distributed manner for MPI execution.

    Parameters
    ----------
    data : Supports the following input data-types :
            1. Dense matrix (ndarray) of correct labels.
            2. SnapML data partition. This includes the correct labels.

    pred : Predicted classes.
        array-like, shape = (n_samples,)

    Returns
    -------
    accuracy_value : float
        Returns the accuracy score of the predicted classes (pred)
        when compared with the true labels (data).
    """

    num_ex = 0
    data_ = np.array([])
    data_ptr_ = ""
    data_type_ = -1
    if _is_data_snapml_partition_type(data):
        data_ptr_ = data.ptr_
        data_type_ = data.type_
    else:
        num_ex = data.shape[0]

        if type(data).__name__ == "ndarray":
            data_ = data.astype(np.float32)
        else:
            raise ValueError("data should be in ndarray format.")

    pred = pred.astype(float)
    return libsnapml.accuracy(num_ex, data_, data_ptr_, data_type_, pred)


def mean_squared_error(data, pred):
    """
    Distributed mean squared error regression loss.
    It supports both local and distributed(MPI) implementation.

    This metric is often used in multi-class classification to compute the
    mean squared error of the predicted target values when compared with the
    true labels. It currently supports binary classification only.
    The metric is implemented in a distributed manner for MPI execution.

    Parameters
    ----------
    data : Supports the following input data-types :
            1. Dense matrix (ndarray) of correct labels.
            2. SnapML data partition. This includes the correct labels.

    pred : Predicted target values.
        array-like, shape = (n_samples,)

    Returns
    -------
    mean_squared_error_value : float
        Returns the mean squared error of the predicted target values (pred)
        when compared with the true values (data).
    """

    num_ex = 0
    data_ = np.array([])
    data_ptr_ = ""
    data_type_ = -1
    if _is_data_snapml_partition_type(data):
        data_ptr_ = data.ptr_
        data_type_ = data.type_
    else:
        num_ex = data.shape[0]

        if type(data).__name__ == "ndarray":
            data_ = data.astype(np.float32)
        else:
            raise ValueError("data should be in ndarray format.")

    return libsnapml.mean_squared_error(num_ex, data_, data_ptr_, data_type_, pred)


def hinge_loss(data, pred_decision):
    """
    Distributed average hinge loss metric.
    It supports both local and distributed(MPI) implementation.

    It supports only binary classification. If the true labels are encoded with
    +1 and -1, then the hinge loss of a sample is computed as 1 - true_label * predicted_decision.
    The predicted_decision is the output of the decision_function predict function (the distance
    of the samples in data to the separating hyperplane). The average hinge loss is the average of
    (1 - true_label * predicted_decision) across samples.
    The metric is implemented in a distributed manner for MPI execution.

    Parameters
    ----------
    data : Supports the following input data-types :
            1. Dense matrix (ndarray) of correct labels.
            2. SnapML data partition. This includes the correct labels.

    pred_decision : Predicted values of the decision function.
        array-like, shape = (n_samples,)

    Returns
    -------
    hinge_loss_value : float
        Returns the average hinge loss of the samples in data.
    """

    num_ex = 0
    data_ = np.array([])
    data_ptr_ = ""
    data_type_ = -1
    if _is_data_snapml_partition_type(data):
        data_ptr_ = data.ptr_
        data_type_ = data.type_
    else:
        num_ex = data.shape[0]

        if type(data).__name__ == "ndarray":
            data_ = data.astype(np.float32)
        else:
            raise ValueError("data should be in ndarray format.")

    return libsnapml.hinge_loss(num_ex, data_, data_ptr_, data_type_, pred_decision)
