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
import sys
import warnings

from snapml.utils import _is_mpi_enabled, _param_check
from snapml._predict_utils import PredictTypes

_mpi_enabled = _is_mpi_enabled()

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(_mpi_enabled)

from snapml.GeneralizedLinearModelClassifier import GeneralizedLinearModelClassifier

from sklearn.base import BaseEstimator, ClassifierMixin

## @ingroup pythonclasses
class SupportVectorMachine(
    GeneralizedLinearModelClassifier, BaseEstimator, ClassifierMixin
):

    """
    Support Vector Machine classifier

    This class implements regularized support vector machine using the IBM Snap ML solver.
    It supports both local and distributed(MPI) methods of the Snap ML solver. It
    can be used for both binary and multi-class classification problems. For multi-class
    classification it predicts classes or the decision function for each class in the model.
    It handles both dense and sparse matrix inputs. Use csr, ndarray, deviceNDArray or
    SnapML data partition format for both training and prediction. DeviceNDArray input
    data format is currently not supported for training with MPI implementation.
    The training uses the dual formulation. We recommend the user to normalize the input values.

    Parameters
    ----------

    loss : {‘hinge’, ‘squared_hinge’}, default=’hinge’
        The loss function that will be used for training.

    max_iter : int, default=1000
        Maximum number of iterations used by the solver to converge.

    regularizer : float, default=1.0
        Regularization strength. It must be a positive float.
        Larger regularization values imply stronger regularization.

    use_gpu : bool, default=False
        Flag for indicating the hardware platform used for training. If True, the training
        is performed using the GPU. If False, the training is performed using the CPU.

    device_ids : array-like of int, default=[]
        If use_gpu is True, it indicates the IDs of the GPUs used for training.
        For single GPU training, set device_ids to the GPU ID to be used for training,
        e.g., [0]. For multi-GPU training, set device_ids to a list of GPU IDs to be used
        for training, e.g., [0, 1].

    class_weight : {'balanced', None}, default=None
        If set to 'None', all classes will have weight 1.

    verbose : bool, default=False
        If True, it prints the training cost, one per iteration. Warning: this will increase
        the training time. For performance evaluation, use verbose=False.

    n_jobs : int, default=1
        The number of threads used for running the training. The value of this parameter
        should be a multiple of 32 if the training is performed on GPU (use_gpu=True).

    tol : float, default=0.001
        The tolerance parameter. Training will finish when maximum change in model coefficients is less than tol.

    generate_training_history : {'summary', 'full', None}, default=None
        Determines the level of summary statistics that are generated during training.
        By default no information is generated (None), but this parameter can be set to "summary", to obtain
        summary statistics at the end of training, or "full" to obtain a complete set of statistics
        for the entire training procedure. Note, enabling either option will result in slower training.
        generate_training_history is not supported for DeviceNDArray input format.

    fit_intercept : bool, default=False
        Add bias term -- note, may affect speed of convergence, especially for sparse datasets.

    intercept_scaling : float, default=1.0
        Scaling of bias term. The inclusion of a bias term is implemented by appending an additional feature to the
        dataset. This feature has a constant value, that can be set using this parameter.

    normalize : bool, default=False
        Normalize rows of dataset (recommended for fast convergence).

    kernel : {'rbf', 'linear'}, default='linear'
        Approximate feature map of a specified kernel function.

    gamma : float, default=1.0
        Parameter of RBF kernel: exp(-gamma * x^2)

    n_components : int, default=100
        Dimensionality of the feature space when approximating a kernel function.

    random_state : int, or None, default=None
        If int, random_state is the seed used by the random number generator;
        If None, the random number generator is the RandomState instance used by `np.random`.

    Attributes
    ----------
    coef_ : array-like, shape (n_features,) for binary classification or
        (n_features, n_classes) for multi-class classification.
        Coefficients of the features in the trained model.

    intercept_: ndarray of shape (1,) if n_classes == 2 else (n_classes,)
        Constants in the decision function.
        If fit_intercept is False, then intercept_ is 0.0.
        Otherwise it is an ndarray of shape (1,) if n_classes == 2 else (n_classes,)

    support_ : array-like,  shape (n_SV)
        indices of the support vectors.
        Currently not supported for MPI implementation.

    n_support_ : int
        Number of support vectors.
        Currently not supported for MPI implementation.

    training_history_ : dict
        Training history statistics.

    """

    PARAMS = [
        {"name": "loss", "attr": [{"values": ["hinge", "squared_hinge"]}]},
        {"name": "max_iter", "attr": [{"type": "int", "ge": 1}]},
        {"name": "regularizer", "attr": [{"type": "float", "gt": 0}]},
        {"name": "device_ids", "attr": [{"type": "list"}]},
        {"name": "verbose", "attr": [{"type": "bool"}]},
        {"name": "class_weight", "attr": [{"values": [None, "balanced"]}]},
        {"name": "use_gpu", "attr": [{"type": "bool"}]},
        {"name": "n_jobs", "attr": [{"type": "int", "ge": 1}]},
        {"name": "tol", "attr": [{"type": "float", "ge": 0}]},
        {
            "name": "generate_training_history",
            "attr": [{"values": [None, "summary", "full"]}],
        },
        {"name": "fit_intercept", "attr": [{"type": "bool"}]},
        {"name": "intercept_scaling", "attr": [{"type": "float", "gt": 0}]},
        {"name": "normalize", "attr": [{"type": "bool"}]},
        {"name": "kernel", "attr": [{"values": ["linear", "rbf"]}]},
        {"name": "gamma", "attr": [{"type": "float", "gt": 0}]},
        {"name": "n_components", "attr": [{"type": "int", "ge": 1}]},
        {"name": "random_state", "attr": [{"values": [None]}, {"type": "int"}]},
    ]

    def __init__(
        self,
        loss="hinge",
        max_iter=1000,
        regularizer=1.0,
        device_ids=[],
        verbose=False,
        use_gpu=False,
        class_weight=None,
        n_jobs=1,
        tol=0.001,
        generate_training_history=None,
        fit_intercept=False,
        intercept_scaling=1.0,
        normalize=False,
        kernel="linear",
        gamma=1.0,
        n_components=100,
        random_state=None,
    ):

        self.loss = loss
        self.max_iter = max_iter
        self.regularizer = regularizer
        self.device_ids = device_ids
        self.verbose = verbose
        self.use_gpu = use_gpu
        self.class_weight = class_weight
        self.dual = True
        self.n_jobs = n_jobs
        self.penalty = None
        self.tol = tol
        self.generate_training_history = generate_training_history
        self.privacy = False
        self.is_regression = 0
        self.fit_intercept = fit_intercept
        self.intercept_scaling = intercept_scaling
        self.labels_flag = False
        self.params = SupportVectorMachine.PARAMS
        self.standard_predict_type = PredictTypes.linear_classification
        self.normalize = normalize
        self.kernel = kernel
        self.gamma = gamma
        self.n_components = n_components
        self.random_state = random_state

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

        out_fit = libsnapml.svm_fit(
            self.max_iter,
            self.regularizer,
            1,
            self.verbose,
            balanced,
            self.use_gpu,
            n_jobs,
            not self.dual,
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
            self.device_ids,
            X_train_ptr_,
            X_train_type_,
            "",
            self.tol,
            generate_training_code,
            self.privacy,
            0.3,
            100,
            10.0,
            1,
            self.is_regression,
            self.fit_intercept,
            self.intercept_scaling,
            self.loss,
        )

        return out_fit

    def c_predict(self, n_jobs, pred_vars):
        pred = libsnapml.svm_predict(
            pred_vars.num_ex,
            pred_vars.num_ft,
            pred_vars.indptr,
            pred_vars.indices,
            pred_vars.data,
            self.model_,
            pred_vars.X_ptr_,
            pred_vars.X_type_,
            self.model_size,
            pred_vars.num_classes,
            self.is_regression,
            n_jobs,
            self.fit_intercept,
            self.intercept_scaling,
        )

        return pred

    def decision_function(self, X, n_jobs=None):

        """
        Predicts confidence scores.

        The confidence score of a sample is the signed distance of that sample to the decision boundary.

        Parameters
        ----------
        X : Dataset used for predicting distances to the decision boundary. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        n_jobs : int, default=None
            Number of threads used to run inference.
            By default the value of the class attribute is used..
            This parameter is ignored for decision_function of a single observation.

        Returns
        -------
        proba: array-like, shape = (n_samples,) or (n_sample, n_classes)
            Returns the distance to the decision boundary of the samples in X.
        """

        if n_jobs is not None:
            warnings.warn(
                "Setting n_jobs as an argument to decision_function may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_params method before calling decision_function, e.g.: set_params(n_jobs=4)",
                FutureWarning,
            )
            _param_check(SupportVectorMachine.PARAMS, "n_jobs", n_jobs)
        else:
            n_jobs = self.n_jobs

        # validate number of features
        self.validate_num_ft(X)

        # normalization
        X = self.normalize_data(X)

        # apply kernel
        X = self.apply_kernel(X)

        is_single, proba, pred_vars = self.pre_predict_is_single(
            X, _mpi_enabled, PredictTypes.linear_prediction
        )

        if is_single == False:
            # Multi-row or snap-data or MPI
            proba = libsnapml.svm_decision_function(
                pred_vars.num_ex,
                pred_vars.num_ft,
                pred_vars.indptr,
                pred_vars.indices,
                pred_vars.data,
                self.model_,
                pred_vars.X_ptr_,
                pred_vars.X_type_,
                self.model_size,
                pred_vars.num_classes,
                self.is_regression,
                n_jobs,
                self.fit_intercept,
                self.intercept_scaling,
            )

            if pred_vars.num_classes > 2:
                proba = proba.T

        return proba
