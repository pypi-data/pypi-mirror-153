# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np
import sys

from snapml.utils import (
    _is_mpi_enabled,
    _is_data_snapml_partition_type,
    _check_devicendarray_types,
)
from snapml.utils import _verify_compat_obj_dtype, _verify_inference_dtype

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(False)

## @ingroup pythonclasses
class RBFSampler:

    """
    RBFSampler

    This class approximates a feature map of an RBF kernel by Monte Carlo approximation of its Fourier transform.

    Parameters
    ----------
    gamma : float, default : 1.0
        RBF kernel parameter: exp(-gamma*X^2)

    n_components : int, default : 10
        Dimensionality of the computed feature space.

    random_state : int, default : 42
        Random State used by the random generator when generating the fourier transform features.

    Attributes
    ----------

    weights_: array-like, shape (n_examples, n_components)
        Random feature matrix

    offsets_: array-like, shape (n_components, )
        Random offset vector

    """

    def __init__(self, gamma=1.0, n_components=10, random_state=42):

        self.gamma_ = gamma

        self.n_components_ = n_components

        if n_components <= 0:
            raise ValueError("Parameter n_components: value should be positive.")

        self.random_state_ = random_state

    def get_params(self):

        """
        Get the values of the model parameters.

        Returns
        -------
        params : dict
        """

        params = {}
        params["gamma"] = self.gamma_
        params["n_components"] = self.n_components_
        params["random_state"] = self.random_state_

        return params

    def fit(self, X_train):

        """
        Fit the model with X_train.
        Samples random projection according to n_features.

        Parameters
        ----------
        X_train : Training dataset. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. TODO: DeviceNDArray. Not supported for MPI execution.
            3. TODO: SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        """

        num_ft = X_train.shape[1]

        # Train the model
        out_fit = libsnapml.rbf_fit(
            self.gamma_, self.n_components_, self.random_state_, num_ft
        )

        # We return the feature map as a 1D array of n_ex * n_components and a 1D array of n_components
        self.weights_ = np.array(out_fit[0])
        self.offsets_ = np.array(out_fit[1])
        self.weights_len_ = out_fit[2]

        # print("[Python - fit] weights_length (num_ft*n_components) = ", self.weights_len_)
        # print("[Python - fit] weights ", self.weights_)
        # print("[Python - fit] offsets ", self.offsets_)

    def transform(self, X, num_threads=1):

        """
        Apply the approximate fourier transformation to X

        Parameters
        ----------
        X : Dataset used for transformation. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. TODO: SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        num_threads : int, default : 1
            Number of threads used to run the transformation.

        Returns
        -------
        X_new: array-like, shape = (n_samples, n_components)
            Returns the new X dataset after the feature map transformation.
        """

        num_ex = 0
        num_ft = 0

        data = np.array([])

        num_ex = X.shape[0]
        num_ft = X.shape[1]

        if type(X).__name__ == "ndarray":
            data = X.astype(np.float32)
            data = np.ascontiguousarray(data)  # ensure row-major format
        else:
            raise ValueError("X should be in ndarray format.")

        # print("[Python - transform] weights ", list(self.weights_))
        # print("[Python - transform] offsets ", self.offsets_)

        # print("[Python - transform] Before X transform ", X.shape)
        # print("[Python - transform] Before X transform X = ", X)

        # Return a 1D array of shape (n_ex, n_components)
        X_new = libsnapml.rbf_transform(
            num_ex,
            num_ft,
            data,
            self.weights_,
            self.weights_len_,
            self.offsets_,
            num_threads,
            self.gamma_,
            self.n_components_,
            self.random_state_,
        )

        # print("[Python - transform] Before X_new reshape ", X_new.shape)
        # print("[Python - transform] X_new ", X_new)

        X_new = np.reshape(X_new, (num_ex, self.n_components_))

        # print("[Python - transform] After X_new reshape ", X_new.shape)
        # print("[Python - transform] X_new ", X_new)

        return X_new
