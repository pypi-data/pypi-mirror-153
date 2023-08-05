# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2021. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

from sklearn.base import RegressorMixin
from snapml import BoostingMachine
from snapml.BoostingMachineCommon import BoostingMachineCommon
import numpy as np
import warnings

## @ingroup pythonclasses
class BoostingMachineRegressor(BoostingMachineCommon, RegressorMixin):

    """
    Boosting machine for regression tasks.

    A heterogeneous boosting machine that mixes binary decision trees (of
    stochastic max_depth) with linear models with random fourier features
    (approximation of kernel ridge regression).

    Parameters
    ----------
    num_round : int, default=100
        Number of boosting iterations.

    objective : {'mse', 'cross_entropy'}, default='mse'
        Training objective.

    learning_rate : float, default=0.1
        Learning rate / shrinkage factor.

    random_state : int, default=0
        Random seed.

    colsample_bytree : float, default=1.0
        Fraction of feature columns used at each boosting iteration.

    subsample : float, default=1.0
        Fraction of training examples used at each boosting iteration.

    verbose : bool, default=False
        Print off information during training.

    lambda_l2 : float, default=0.0
        L2-reguralization penalty used during tree-building.

    early_stopping_rounds : int, default=10
        When a validation set is provided, training will stop if the
        validation loss does not decrease after a fixed number of rounds.

    compress_trees : bool, default=False
        Compress trees after training for fast inference.

    base_score : float, default=None
        Base score to initialize boosting algorithm.
        If None then the algorithm will initialize the base score to be the
        average target (regression) or the logit of the probability of the positive
        class (binary classification).

    max_depth : int, default=None
        If set, will set min_max_depth = max_depth = max_max_depth

    min_max_depth : int, default=1
        Minimum max_depth of trees in the ensemble.

    max_max_depth : int, default=5
        Maximum max_depth of trees in the ensemble.

    n_jobs : int, default=1
        Number of threads to use during training.

    use_histograms : bool, default=True
        Use histograms to accelerate tree-building.

    hist_nbins : int, default=256
        Number of histogram bins.

    use_gpu : bool, default=False
        Use GPU for tree-building.

    gpu_id : int, default=0
        Device ID for GPU to use during training.

    tree_select_probability : float, default=1.0
        Probability of selecting a tree (rather than a kernel ridge regressor) at each boosting iteration.

    regularizer : float, default=1.0
        L2-regularization penality for the kernel ridge regressor.

    fit_intercept : bool, default=False
        Include intercept term in the kernel ridge regressor.

    gamma : float, default=1.0
        Guassian kernel parameter.

    n_components : int, default=10
        Number of components in the random projection.

    Attributes
    ----------

    feature_importances_ : array-like, shape=(n_features,)
        Feature importances computed across trees.

    """

    def __init__(
        self,
        n_jobs=1,
        num_round=100,
        objective="mse",
        max_depth=None,
        min_max_depth=1,
        max_max_depth=5,
        early_stopping_rounds=10,
        random_state=0,
        base_score=None,
        learning_rate=0.1,
        verbose=False,
        compress_trees=False,
        use_histograms=True,
        hist_nbins=256,
        use_gpu=False,
        gpu_id=0,
        colsample_bytree=1.0,
        subsample=1.0,
        lambda_l2=0.0,
        tree_select_probability=1.0,
        regularizer=1.0,
        fit_intercept=False,
        gamma=1.0,
        n_components=10,
    ):

        self.n_jobs = n_jobs
        self.num_round = num_round
        self.objective = objective
        self.max_depth = max_depth
        self.min_max_depth = min_max_depth
        self.max_max_depth = max_max_depth
        self.early_stopping_rounds = early_stopping_rounds
        self.random_state = random_state
        self.base_score = base_score
        self.learning_rate = learning_rate
        self.verbose = verbose
        self.compress_trees = compress_trees
        self.use_histograms = use_histograms
        self.hist_nbins = hist_nbins
        self.use_gpu = use_gpu
        self.gpu_id = gpu_id
        self.colsample_bytree = colsample_bytree
        self.subsample = subsample
        self.lambda_l2 = lambda_l2
        self.tree_select_probability = tree_select_probability
        self.regularizer = regularizer
        self.fit_intercept = fit_intercept
        self.gamma = gamma
        self.n_components = n_components

    def fit(
        self,
        X,
        y,
        sample_weight=None,
        X_val=None,
        y_val=None,
        sample_weight_val=None,
        aggregate_importances=True,
    ):

        """
        Fit the model according to the given train data.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Train dataset

        y : array-like, shape = (n_samples,)
            The target vector corresponding to X

        sample_weight : array-like, shape = (n_samples,)
            Training sample weights

        X_val : dense matrix (ndarray)
            Validation dataset

        y_val : array-like, shape = (n_samples,)
            The target vector corresponding to X_val.

        sample_weight_val : array-like, shape = (n_samples,)
            Validation sample weights

        aggregate_importances : bool, default=True
            Aggregate feature importances over boosting rounds

        Returns
        -------
        self : object
        """

        if self.objective not in ["mse", "cross_entropy"]:
            raise ValueError("Unsupported objective")

        self.booster_ = BoostingMachine(self.make_boosting_params())
        self.booster_.fit(
            X, y, sample_weight, X_val, y_val, sample_weight_val, aggregate_importances
        )

        self.feature_importances_ = self.booster_.feature_importances_

        return self

    def apply(self, X):
        """
        Map batch of examples to leaf indices and labels.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Batch of examples.

        Returns
        -------
        indices : array-like, shape = (n_samples, num_round)
            The leaf indices.

        labels : array-like, shape = (n_samples, num_round)
            The leaf labels.

        """

        return self.booster_.apply(X)

    def predict(self, X, n_jobs=None):

        """
        Predict estimates


        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for prediction

        n_jobs : int
            Number of threads to use for prediction.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predictions

        """

        if n_jobs is not None:
            warnings.warn(
                "Setting n_jobs as an argument to predict may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_params method before calling predict, e.g.: set_params(n_jobs=4)",
                FutureWarning,
            )

        return (
            self.booster_._predict(X, 0, n_jobs)
            if self.objective == "mse"
            else self.booster_._predict(X, 1, n_jobs)[:, 1]
        )
