# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2020, 2021. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np
import sys
import warnings

from snapml.utils import _is_mpi_enabled, _param_check

_mpi_enabled = _is_mpi_enabled()

from abc import ABC, abstractmethod

## @ingroup pythonclasses
class CommonModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extract_and_check_labels(self, y_train):
        pass

    @abstractmethod
    def check_value_of_max_features(self, num_ft):
        pass

    @abstractmethod
    def create_class(self, pred):
        pass

    @abstractmethod
    def check_gpu(self):
        pass

    @abstractmethod
    def c_fit(
        self,
        max_depth,
        min_samples_leaf,
        max_features,
        random_state,
        num_ex,
        num_ft,
        num_nz,
        indptr,
        indices,
        data,
        labs,
        num_classes,
        sample_weight,
    ):
        pass

    @abstractmethod
    def c_predict(
        self, num_ex, num_ft, indptr, indices, data, n_jobs, proba, num_classes
    ):
        pass

    def check_params(self):

        for varname, value in self.get_params().items():
            _param_check(self.params, varname, value)

        if (self.use_gpu == True) and (self.use_histograms == False):
            raise ValueError(
                "GPU acceleration can only be enabled if use_histograms=True"
            )

        self.check_gpu()

        if _mpi_enabled:
            raise ValueError(
                "MPI (distributed) implementation of decision tree classifiers not yet supported."
            )

    def fit(self, X_train, y_train, sample_weight=None):

        """
        Fit the model according to the given train data.

        Parameters
        ----------
        X_train : dense matrix (ndarray)
            Train dataset

        y_train : array-like, shape = (n_samples,)
            The target vector corresponding to X_train.

        sample_weight : array-like, shape = [n_samples] or None
            Sample weights. If None, then samples are equally weighted.
            TODO: Splits that would create child nodes with net zero or
            negative weight are ignored while searching for a split
            in each node.

        Returns
        -------
        self : object
        """

        self.check_params()

        if type(X_train).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        # Check if the maximum depth is limited by the user, otherwise set value to 0 (no limit)
        if self.max_depth is None:
            max_depth = 0  # Unlimited tree depth
        else:
            max_depth = self.max_depth

        # Random state
        if self.random_state == None:
            # Not sure if this should be the random state
            random_state = np.random.get_state()[1][0]
        else:
            random_state = self.random_state

        # get number of examples/features
        num_ex = X_train.shape[0]
        num_ft = X_train.shape[1]

        # in most cases, y_train should contain all examples
        if len(y_train) != num_ex:
            raise ValueError(
                "Inconsistent dimensions: X_train.shape[0] must equal len(y_train)"
            )

        if (num_ex == 0) or (num_ft == 0):
            raise ValueError("Wrong dimensions: X.shape[0] and X.shape[1] must be > 0.")

        num_nz = num_ex * num_ft
        data = np.ascontiguousarray(X_train, dtype=np.float32)
        indptr = np.array([])
        indices = np.array([])

        labs = self.extract_and_check_labels(y_train)

        # Check the value of min_samples_leaf
        if isinstance(self.min_samples_leaf, (int)):
            if self.min_samples_leaf > num_ex:
                raise ValueError(
                    "Parameter min_samples_leaf: invalid value. The value of min_samples_leaf is larger than the number of examples in the train dataset."
                )
            else:
                min_samples_leaf = self.min_samples_leaf
        else:
            min_samples_leaf = np.ceil(self.min_samples_leaf * num_ex)

        max_features = self.check_value_of_max_features(num_ft)

        # sample weight mode during training
        # default : sample_weight array is None
        if not sample_weight is None:
            if type(sample_weight).__name__ != "ndarray":
                raise TypeError(
                    "Parameter sample_weight: invalid type. Supported type: ndarray."
                )
            sample_weight = sample_weight.astype(np.float32)
        else:
            sample_weight = np.array([], dtype=np.float32)

        self.model_, self.model_size_, self.feature_importances_ = self.c_fit(
            max_depth,
            min_samples_leaf,
            max_features,
            random_state,
            num_ex,
            num_ft,
            num_nz,
            indptr,
            indices,
            data,
            labs,
            self.n_classes_,
            sample_weight,
        )

        self.n_features_in_ = num_ft

        return self

    def predict(self, X, n_jobs=None):

        """
        Class/Regression predictions

        The returned class/regression estimates.

        Parameters
        ----------
        X : dense matrix (ndarray) or memmap (np.memmap)
            Dataset used for predicting class/regression estimates.

        n_jobs : int, default=None
            Number of threads used to run inference.
            By default the value of the class attribute is used..

        Returns
        -------
        pred/proba: array-like, shape = (n_samples,)
            Returns the predicted class/values of the sample.
        """

        if n_jobs is not None:
            warnings.warn(
                "Setting n_jobs as an argument to predict may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_params method before calling predict, e.g.: set_params(n_jobs=4)",
                FutureWarning,
            )
            _param_check(self.params, "n_jobs", n_jobs)
        else:
            n_jobs = self.n_jobs

        if type(X).__name__ != "ndarray" and type(X).__name__ != "memmap":
            raise TypeError(
                "Tree-based models in Snap ML only support numpy.ndarray and numpy.memmap"
            )

        if self.n_features_in_ > 0 and X.shape[1] != self.n_features_in_:
            raise ValueError(
                "Predict was passed %d features, but model was trained with %d features"
                % (X.shape[1], self.n_features_in_)
            )

        indptr = np.array([])
        indices = np.array([])
        data = np.array([])
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
        elif type(X).__name__ == "ndarray" or type(X).__name__ == "memmap":
            data = X.astype(np.float32)
            data = np.ascontiguousarray(data)  # ensure row-major format
            indptr = np.array([])
            indices = np.array([])
        else:
            raise ValueError("X should be in csc_matrix, csr_matrix or ndarray format.")

        pred = []

        # Generate predictions
        pred = self.c_predict(
            num_ex,
            num_ft,
            indptr,
            indices,
            data,
            n_jobs,
            False,
            self.n_classes_,
        )

        pred = self.create_class(np.array(pred))

        return pred

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
