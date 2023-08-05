# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np
import warnings

from snapml.utils import (
    _is_mpi_enabled,
    _check_devicendarray_types,
    _is_data_snapml_partition_type,
    _param_check,
)
from snapml._predict_utils import _predict_common_processing, _lr_single_row_predict

_mpi_enabled = _is_mpi_enabled()

from abc import ABC, abstractmethod
from collections import namedtuple
from sklearn.preprocessing import normalize, StandardScaler, MaxAbsScaler
from sklearn.kernel_approximation import RBFSampler

## @ingroup pythonclasses
class GeneralizedLinearModel(ABC):
    _PredictVars = namedtuple(
        "PredictVars",
        [
            "num_ex",
            "num_ft",
            "num_classes",
            "X_ptr_",
            "X_type_",
            "indptr",
            "indices",
            "data",
            "shortcut_predict",
        ],
    )

    @abstractmethod
    def __init__(self):
        # just for reference
        self.max_iter = (None,)
        self.regularizer = None
        self.device_ids = None
        self.verbose = None
        self.use_gpu = None
        self.class_weight = None
        self.dual = None
        self.n_jobs = None
        self.penalty = None
        self.tol = None
        self.generate_training_history = None
        self.fit_intercept = None
        self.privacy = None
        self.eta = None
        self.batch_size = None
        self.grad_clip = None
        self.privacy_epsilon = None
        self.is_regression = None
        self.intercept_scaling = None
        self.model_size = None
        self.labels_flag = None
        self.params = None
        self.standard_predict_type = None
        self.kernel = None
        self.gamma = None
        self.n_components = None
        self.random_state = None
        pass

    @abstractmethod
    def set_classes(self, y_train):
        pass

    @abstractmethod
    def set_intercept(self):
        pass

    @abstractmethod
    def check_and_modify_labels(self, y_train):
        pass

    @abstractmethod
    def c_fit(
        self,
        n_jobs,
        balanced,
        col_major,
        num_ex,
        num_ft,
        num_nz,
        indptr,
        indices,
        data,
        labs,
        gpu_data_ptr,
        gpu_lab_ptr,
        gpu_matrix,
        X_train_ptr_,
        X_train_type_,
        generate_training_code,
    ):
        pass

    @abstractmethod
    def post_training(self, training_metadata, X_train, _mpi_enabled):
        pass

    @abstractmethod
    def c_predict(self, n_jobs):
        pass

    @abstractmethod
    def post_predict(self, pred):
        pass

    def normalize_data(self, X, refit=False):

        normalize_types = ["ndarray", "csr_matrix", "csc_matrix", "memmap"]

        # do *not* normalize if
        # (a) user has not requested it
        # (b) MPI is enabled
        # (c) X is not ndarray, csr_matrix or csc_matrix
        if (
            type(X).__name__ not in normalize_types
            or _mpi_enabled
            or (not self.normalize)
        ):
            return X

        if refit:
            self.scaler_ = (
                StandardScaler() if type(X).__name__ == "ndarray" else MaxAbsScaler()
            )
            self.scaler_.fit(X)

        X = self.scaler_.transform(X)
        X = normalize(X, copy=False)
        return X

    def apply_kernel(self, X, refit=False):

        kernel_types = ["ndarray", "csr_matrix", "csc_matrix", "memmap"]

        if (
            type(X).__name__ not in kernel_types
            or _mpi_enabled
            or (self.kernel == "linear")
        ):
            return X

        if refit:
            self.kernel_ = RBFSampler(
                gamma=self.gamma,
                n_components=self.n_components,
                random_state=self.random_state,
            ).fit(X)

        X = self.kernel_.transform(X).astype(np.float32)

        return X

    def validate_num_ft(self, X, refit=False):

        if _is_data_snapml_partition_type(X) or _mpi_enabled:
            return

        if refit:
            self.n_features_in_ = X.shape[1]
        else:
            if X.shape[1] != self.n_features_in_:
                raise ValueError(
                    "Predict was passed %d features, but model was trained with %d features"
                    % (X.shape[1], self.n_features_in_)
                )

    def check_params(self):

        for varname, value in self.get_params().items():
            _param_check(self.params, varname, value)

        if self.regularizer < 0.0001:
            print("[Warning] Parameter regularizer: value might be too small.")

        if any(val < 0 for val in self.device_ids):
            raise ValueError(
                "Parameter device_id: value too small. Should be an integer >= 0."
            )
        self.device_ids.sort()
        self.device_ids = np.array(self.device_ids).astype(np.uint32)

        if self.verbose:
            if self.n_jobs > 1:
                print("[Info] Multi-threaded mode.")
            else:
                print("[Info] Single-threaded mode.")

        if (self.use_gpu == False) and (len(self.device_ids) > 0) and self.verbose:
            print(
                "[Warning] Parameter device_ids will be ignored. The use_gpu parameter was set to False. Operations are performed on the CPU."
            )

        if (self.use_gpu == True) and (len(self.device_ids) == 0):
            # With MPI, we recommend snaprun instead of mpirun. snaprun gives
            # 1 GPU per process. So no need of device_ids as argument for that case.
            if not _mpi_enabled and self.verbose:
                print(
                    "[Warning] Parameter device_ids not set. The training will run on GPU 0."
                )

        if (self.penalty == "l1") and (self.dual):
            raise ValueError(
                "L1 regularization is supported only for primal optimization problems. Set dual to False."
            )

        if _mpi_enabled and self.privacy:
            raise ValueError(
                "Privacy not supported for MPI execution. Set privacy=False."
            )

        if self.privacy and self.dual:
            raise ValueError("Privacy only supported for primal objective functions.")

        if self.privacy and self.penalty == "l1":
            raise ValueError(
                "Privacy only supported for L2-regularized objective functions."
            )

        if self.privacy and self.use_gpu:
            print("[Warning] Privacy not supported by GPU solvers. Will train on CPU")

        if self.privacy and self.fit_intercept:
            raise ValueError("Privacy not supported with fit_intercept=True.")

    def fit(self, X_train, y_train=None):

        """
        Fit the model according to the given train dataset.

        Parameters
        ----------
        X_train : Train dataset. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. DeviceNDArray. Not supported for MPI execution.
            3. SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        y_train : The target corresponding to X_train.
            If X_train is sparse matrix or dense matrix, y_train should be array-like of shape = (n_samples,)
            In case of deviceNDArray, y_train should be array-like of shape = (n_samples, 1)
            If X_train is SnapML data partition type, then y_train is not required (i.e. None).

        Returns
        -------
        self : object
        """

        self.check_params()

        if hasattr(self, "class_weight") and self.class_weight == "balanced":
            balanced = True
        else:
            balanced = False

        if self.random_state == None:
            random_state = np.random.get_state()[1][0]
        else:
            random_state = self.random_state

        self.set_classes(y_train)

        # Performing all the initial checks for DeviceNDArray inputs
        _check_devicendarray_types(X_train, y_train, self)

        # if we are solving the primal case (without privacy)
        # then we need the data to be col-major
        col_major = (not self.dual) and (not self.privacy)

        # enforce col/row major
        if type(X_train).__name__ == "ndarray" or type(X_train).__name__ == "memmap":
            if col_major:
                X_train = np.asfortranarray(X_train, dtype=np.float32)
            else:
                X_train = np.ascontiguousarray(X_train, dtype=np.float32)
        elif type(X_train).__name__ == "csr_matrix":
            if col_major:
                X_train = X_train.tocsc()
        elif type(X_train).__name__ == "csc_matrix":
            if not col_major:
                X_train = X_train.tocsr()

        # define set of valid python data types depending on parameters
        if self.privacy:
            valid_types = ["ndarray", "csr_matrix"]
        else:
            valid_types = [
                "ndarray",
                "SparsePartition",
                "DensePartition",
                "ConstantValueSparsePartition",
                "memmap",
            ]

            if self.dual:
                valid_types.append("csr_matrix")
            else:
                valid_types.append("csc_matrix")

            if not _mpi_enabled:
                valid_types.append("DeviceNDArray")

        # check that the data is one of the types
        if type(X_train).__name__ not in valid_types:
            raise ValueError(
                "X_train has type %s, but for the parameter specification [_mpi_enabled: %d, dual: %d, privacy: %d] it must have one of the following types: "
                % (type(X_train).__name__, _mpi_enabled, self.dual, self.privacy),
                valid_types,
            )

        # record number of features
        self.validate_num_ft(X_train, refit=True)

        # normalization
        X_train = self.normalize_data(X_train, refit=True)

        # apply kernel
        X_train = self.apply_kernel(X_train, refit=True)

        # populate fields
        X_train_ptr_ = ""
        X_train_type_ = -1
        num_ex = 0
        num_ft = 0
        num_nz = 0
        indptr = np.array([])
        indices = np.array([])
        data = np.array([], dtype=np.float32)
        labs = np.array([])
        y_train_device = np.array([])
        # by default gpu_matrix is set to False.
        # It will be set to True if xtrain and ytrain is coming from GPU device.
        gpu_matrix = False
        gpu_data_ptr = 0
        gpu_lab_ptr = 0

        # first check if X_train is a custom Snap ML data structure
        if type(X_train).__name__ in [
            "SparsePartition",
            "DensePartition",
            "ConstantValueSparsePartition",
        ]:
            X_train_ptr_ = X_train.ptr_
            X_train_type_ = X_train.type_
        else:

            # get number of examples/features
            num_ex = X_train.shape[0]
            num_ft = X_train.shape[1]

            if (num_ex == 0) or (num_ft == 0):
                raise ValueError(
                    "Wrong dimensions: X.shape[0] and X.shape[1] must be > 0."
                )

            # check that y_train was provided
            if y_train is None:
                raise ValueError("Parameter y_train: Input data is required.")

            # in most cases, y_train should contain all examples
            if (not _mpi_enabled) or (not self.dual):
                assert len(y_train) == num_ex

            # numpy array
            if (
                type(X_train).__name__ == "ndarray"
                or type(X_train).__name__ == "memmap"
            ):
                num_nz = num_ex * num_ft
                data = X_train

            # sparse matrices
            if type(X_train).__name__ in ["csr_matrix", "csc_matrix"]:
                num_nz = X_train.nnz
                indptr = X_train.indptr.astype(np.uint64)
                data = X_train.data.astype(np.float32)
                indices = X_train.indices.astype(np.uint32)

                """
                if self.fit_intercept == True:
                    print(
                        "[Warning] May affect speed of convergence for sparse datasets as fit_intercept is set."
                    )
                """

            # deviceNDarray
            if type(X_train).__name__ == "DeviceNDArray":
                num_nz = num_ex * num_ft
                gpu_matrix = True
                gpu_data_ptr = X_train.device_ctypes_pointer.value
                y_train = y_train.copy_to_host()

            # encode labels
            labs = self.check_and_modify_labels(y_train)

            # copy encoded labels back to device
            if gpu_matrix:
                from snapml._gpu_utils import _to_device

                y_train = _to_device(y_train)
                gpu_lab_ptr = y_train.device_ctypes_pointer.value

        if self.generate_training_history is None:
            generate_training_code = 0
        elif self.generate_training_history == "summary":
            generate_training_code = 1
        else:
            generate_training_code = 2

        n_jobs = self.n_jobs
        if self.use_gpu == True:
            if not self.n_jobs % 32 == 0:
                if self.verbose:
                    print(
                        "[Info] If set n_jobs should be a multiple of 32. GPU training will run with n_jobs=256."
                    )
                n_jobs = 256

        out_fit = self.c_fit(
            n_jobs,
            balanced,
            col_major,
            num_ex,
            num_ft,
            num_nz,
            indptr,
            indices,
            data,
            labs,
            gpu_data_ptr,
            gpu_lab_ptr,
            gpu_matrix,
            X_train_ptr_,
            X_train_type_,
            generate_training_code,
        )

        self.model_ = out_fit[0]
        if generate_training_code == 0:
            self.training_history_ = None
        else:
            self.training_history_ = out_fit[1]
        if not _mpi_enabled:
            self.support_ = np.array(out_fit[2], np.int32)
            self.n_iter_ = out_fit[3]

        self.set_intercept()

        # training_metadata
        training_metadata = out_fit[4]
        self.model_size = training_metadata["model_size"]

        # Assign the model to the coef_ attribute
        self.coef_ = self.model_
        if self.fit_intercept == True:
            self.coef_ = self.coef_[:, 0:-1]
        self.post_training(training_metadata, X_train, _mpi_enabled)

        return self

    def pre_predict_is_single(self, X, _mpi_enabled, predict_type):

        pred_vars = GeneralizedLinearModel._PredictVars._make(
            _predict_common_processing(self, X, self.is_regression, _mpi_enabled)
        )

        pred = np.array([])
        # Compute predictions/probabilities
        if pred_vars.shortcut_predict and X.shape[0] == 1:
            # Inference for single row numpy or csr (local mode only)
            pred = _lr_single_row_predict(
                self.model_, self.fit_intercept, self.intercept_scaling, X, predict_type
            )
            return True, pred, pred_vars
        else:
            return False, pred, pred_vars

    def predict(self, X, n_jobs=None):

        """
        Class predictions

        The returned class estimates.

        Parameters
        ----------
        X : Dataset used for predicting estimates or class. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        n_jobs : int, default=None
            Number of threads used to run inference.
            By default the value of the class attribute is used..
            This parameter is ignored for predict of a single observation.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predicted estimate/class of the sample.

        """

        if n_jobs is not None:
            warnings.warn(
                "Setting n_jobs as an argument to predict may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_params method before calling predict, e.g.: set_params(n_jobs=4)",
                FutureWarning,
            )
            _param_check(self.params, "n_jobs", n_jobs)
        else:
            n_jobs = self.n_jobs

        # validate number of features
        self.validate_num_ft(X)

        # normalization
        X = self.normalize_data(X)

        # apply kernel
        X = self.apply_kernel(X)

        is_single, pred, pred_vars = self.pre_predict_is_single(
            X, _mpi_enabled, self.standard_predict_type
        )

        if is_single == False:
            # Multi-row or snap-data or MPI
            pred = self.c_predict(n_jobs, pred_vars)

        return self.post_predict(pred)

    def set_params(self, **params):

        """
        Set the parameters of this model.

        Valid parameter keys can be listed with ``get_params()``.

        Returns
        -------
        self

        """

        params_copy = self.get_params()
        super().set_params(**params)
        try:
            self.check_params()
        except:
            super().set_params(**params_copy)
            raise

        return self
