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

from snapml.utils import _is_mpi_enabled

from snapml._predict_utils import PredictTypes

_mpi_enabled = _is_mpi_enabled()

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(_mpi_enabled)

from snapml.GeneralizedLinearModelRegressor import GeneralizedLinearModelRegressor

from sklearn.base import BaseEstimator, RegressorMixin

## @ingroup pythonclasses
class LinearRegression(GeneralizedLinearModelRegressor, BaseEstimator, RegressorMixin):

    """
    Linear Regression

    This class implements regularized linear regression using the IBM Snap ML solver.
    It supports both local and distributed(MPI) methods of the snap ML solver. It
    handles both dense and sparse matrix inputs. Use csr, csc, ndarray, deviceNDArray
    or SnapML data partition format for training and csr, ndarray or
    SnapML data partition format for prediction. DeviceNDArray input data format is
    currently not supported for training with MPI implementation.

    Parameters
    ----------
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
        For single GPU training, set device_ids to the GPU ID to be used for training, e.g., [0].
        For multi-GPU training, set device_ids to a list of GPU IDs to be used for training, e.g., [0, 1].

    dual : bool, default=True
        Dual or primal formulation.
        Recommendation: if n_samples > n_features use dual=True.

    verbose : bool, default=False
        If True, it prints the training cost, one per iteration. Warning: this will increase the
        training time. For performance evaluation, use verbose=False.

    n_jobs : int, default=1
        The number of threads used for running the training. The value of this parameter
        should be a multiple of 32 if the training is performed on GPU (use_gpu=True).

    penalty : {'l1', 'l2'}, default='l2'
        The regularization / penalty type. Possible values are "l2" for L2 regularization (RidgeRegression)
        or "l1" for L1 regularization (LassoRegression). L1 regularization is possible only for the primal
        optimization problem (dual=False).

    tol : float, default=0.001
        The tolerance parameter. Training will finish when maximum change in model coefficients is less than tol.

    generate_training_history : {'summary', 'full', None}, default=None
        Determines the level of summary statistics that are generated during training.
        By default no information is generated (None), but this parameter can be set to "summary", to obtain
        summary statistics at the end of training, or "full" to obtain a complete set of statistics
        for the entire training procedure. Note, enabling either option will result in slower training.
        generate_training_history is not supported for DeviceNDArray input format.

    privacy : bool, default=False
        Train the model using a differentially private algorithm.
        Currently not supported for MPI implementation.

    eta : float, default=0.3
        Learning rate for the differentially private training algorithm.
        Currently not supported for MPI implementation.

    batch_size : int, default=100
        Mini-batch size for the differentially private training algorithm.
        Currently not supported for MPI implementation.

    privacy_epsilon : float, default=10.0
        Target privacy gaurantee. Learned model will be (privacy_epsilon, 0.01)-private.
        Currently not supported for MPI implementation.

    grad_clip : float, default=1.0
        Gradient clipping parameter for the differentially private training algorithm.
        Currently not supported for MPI implementation.

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
    coef_ : array-like, shape (n_features,)
        Coefficients of the features in the trained model.

    intercept_ : float
        Independent term in the decision function.
        Set to 0.0 if fit_intercept == False.

    support_ : array-like
        Indices of the features that lie in the support ond contribute to the decision. (only available for L1).
        Currently not supported for MPI implementation.

    model_sparsity_ : float
        fraction of non-zeros in the model parameters. (only available for L1).
        Currently not supported for MPI implementation.

    training_history_ : dict
        Training history statistics.

    """

    PARAMS = [
        {"name": "max_iter", "attr": [{"type": "int", "ge": 1}]},
        {"name": "regularizer", "attr": [{"type": "float", "gt": 0}]},
        {"name": "device_ids", "attr": [{"type": "list"}]},
        {"name": "verbose", "attr": [{"type": "bool"}]},
        {"name": "use_gpu", "attr": [{"type": "bool"}]},
        {"name": "n_jobs", "attr": [{"type": "int", "ge": 1}]},
        {"name": "dual", "attr": [{"type": "bool"}]},
        {"name": "penalty", "attr": [{"values": ["l1", "l2"]}]},
        {"name": "tol", "attr": [{"type": "float", "ge": 0}]},
        {
            "name": "generate_training_history",
            "attr": [{"values": [None, "summary", "full"]}],
        },
        {"name": "privacy", "attr": [{"type": "bool"}]},
        {"name": "eta", "attr": [{"type": "float", "gt": 0}]},
        {"name": "batch_size", "attr": [{"type": "int", "gt": 0}]},
        {"name": "grad_clip", "attr": [{"type": "float", "ge": 0}]},
        {"name": "privacy_epsilon", "attr": [{"type": "float", "gt": 0}]},
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
        max_iter=1000,
        regularizer=1.0,
        device_ids=[],
        verbose=False,
        use_gpu=False,
        dual=True,
        n_jobs=1,
        penalty="l2",
        tol=0.001,
        generate_training_history=None,
        privacy=False,  # local only
        eta=0.3,  # local only
        batch_size=100,  # local only
        privacy_epsilon=10,  # local only
        grad_clip=1,  # local only
        fit_intercept=False,
        intercept_scaling=1.0,
        normalize=False,
        kernel="linear",
        gamma=1.0,
        n_components=100,
        random_state=None,
    ):

        self.max_iter = max_iter
        self.regularizer = regularizer
        self.device_ids = device_ids
        self.verbose = verbose
        self.use_gpu = use_gpu
        self.dual = dual
        self.n_jobs = n_jobs
        self.penalty = penalty
        self.tol = tol
        self.generate_training_history = generate_training_history
        self.privacy = privacy
        self.eta = eta
        self.batch_size = batch_size
        self.grad_clip = grad_clip
        self.privacy_epsilon = privacy_epsilon
        self.fit_intercept = fit_intercept
        self.intercept_scaling = intercept_scaling
        self.is_regression = 1
        self.params = LinearRegression.PARAMS
        self.standard_predict_type = PredictTypes.linear_prediction
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

        # Train the model
        out_fit = libsnapml.linear_fit(
            self.max_iter,
            self.regularizer,
            1,
            self.verbose,
            balanced,
            self.use_gpu,
            n_jobs,
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
            self.device_ids,
            X_train_ptr_,
            X_train_type_,
            self.penalty,
            self.tol,
            generate_training_code,
            self.privacy,
            self.eta,
            self.batch_size,
            self.grad_clip,
            self.privacy_epsilon,
            self.is_regression,
            self.fit_intercept,
            self.intercept_scaling,
            "",
        )

        return out_fit

    def c_predict(self, n_jobs, pred_vars):

        pred = libsnapml.linear_predict(
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
