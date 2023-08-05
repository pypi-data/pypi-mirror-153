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

from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor,
)
from snapml import SnapBoostingMachineClassifier, SnapBoostingMachineRegressor
from snapml import SnapRandomForestClassifier, SnapRandomForestRegressor
from sklearn.base import clone
import numpy as np
from scipy.special import expit
from snapml.utils import _param_check
import warnings

try:
    from xgboost import XGBRegressor, XGBClassifier

    found_xgboost = True
except ImportError:
    found_xgboost = False

try:
    from lightgbm import LGBMRegressor, LGBMClassifier

    found_lightgbm = True
except ImportError:
    found_lightgbm = False


class BatchedTreeEnsemble(BaseEstimator):

    """
    Batched Tree Ensemble

        Implements logic that is shared between BatchedTreeEnsembleClassifier and BatchedTreeEnsembleRegressor

    """

    PARAMS = [
        {"name": "max_sub_ensembles", "attr": [{"type": "int", "ge": 1}]},
        {"name": "inner_lr_scaling", "attr": [{"type": "float", "ge": 0.0}]},
        {"name": "outer_lr_scaling", "attr": [{"type": "float", "ge": 0.0}]},
    ]

    def __init__(
        self,
        base_ensemble,
        max_sub_ensembles,
        inner_lr_scaling,
        outer_lr_scaling,
        valid_base_ensembles,
    ):

        self.base_ensemble = base_ensemble
        self.max_sub_ensembles = max_sub_ensembles
        self.inner_lr_scaling = inner_lr_scaling
        self.outer_lr_scaling = outer_lr_scaling
        self.valid_base_ensembles = valid_base_ensembles

    def _get_base_ensemble_impl(self, base_ensemble):

        # handle case of Lale operators
        be_name = type(base_ensemble).__name__

        if be_name == "TrainedIndividualOp" or be_name == "TrainableIndividualOp":
            base_ensemble_impl = base_ensemble.impl
        else:
            base_ensemble_impl = base_ensemble

        return base_ensemble_impl

    def _validate_parameters(self):

        """
        Validate parameters (called when fitting on first batch)

        """

        for varname, value in self.get_params().items():
            if varname in map(lambda x: x["name"], BatchedTreeEnsemble.PARAMS):
                _param_check(BatchedTreeEnsemble.PARAMS, varname, value)

        base_ensemble_impl = self._get_base_ensemble_impl(self.base_ensemble)

        if not isinstance(base_ensemble_impl, self.valid_base_ensembles):
            raise ValueError("Invalid choice of base ensemble.")

        # map classifiers to regressor
        mapping = {
            "RandomForestClassifier": RandomForestRegressor,
            "ExtraTreesClassifier": ExtraTreesRegressor,
            "SnapRandomForestClassifier": SnapRandomForestRegressor,
            "SnapBoostingMachineClassifier": SnapBoostingMachineRegressor,
        }

        if found_xgboost:
            mapping["XGBClassifier"] = XGBRegressor

        if found_lightgbm:
            mapping["LGBMClassifier"] = LGBMRegressor

        if hasattr(base_ensemble_impl, "predict_proba"):
            self.base_ensemble_reg = mapping[type(base_ensemble_impl).__name__]()
            for k, v in self.base_ensemble.get_params().items():
                if k == "criterion" or k == "objective":
                    continue
                try:
                    self.base_ensemble_reg.set_params(**{k: v})
                except Exception as e:
                    pass
        else:
            self.base_ensemble_reg = clone(base_ensemble_impl)

        # get parameters of base ensemble
        be_params = self.base_ensemble_reg.get_params()

        # scale the number of trees
        tree_param = (
            "num_round"
            if isinstance(self.base_ensemble_reg, SnapBoostingMachineRegressor)
            else "n_estimators"
        )
        n_trees_per_chunk = int(be_params[tree_param] / self.max_sub_ensembles)
        self.base_ensemble_reg.set_params(**{tree_param: n_trees_per_chunk})

        if found_xgboost:
            # some versions of XGBoost don't have a default value in the scikit-learn API
            if (
                isinstance(self.base_ensemble_reg, XGBRegressor)
                and be_params["learning_rate"] is None
            ):
                be_params["learning_rate"] = 0.3

        # set the outer learning rate
        self.learning_rate = 1.0 / (self.max_sub_ensembles ** self.outer_lr_scaling)

        # scale the inner learning rate
        if "learning_rate" in be_params:
            lr_base = be_params["learning_rate"] * (
                float(self.max_sub_ensembles) ** self.inner_lr_scaling
            )
            lr_base = np.minimum(lr_base, 0.5)
            self.base_ensemble_reg.set_params(**{"learning_rate": lr_base})

        self.ensembles_ = []
        self.classes_ = None

    def fit(self, X, y, sample_weight=None):

        """
        Fit the base ensemble without batching.

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_features)
            Training data.

        y : ndarray, shape (n_samples,)
            Training labels.

        sample_weight : ndarray, shape (n_samples,), default=None
            Sample weights to be applied during training.

        Returns
        -------
        self : object
            Returns an instance of self.

        """

        if hasattr(self, "ensembles_"):
            warnings.warn(
                "This estimator has already been partially fit; call to fit is ignored.",
                category=UserWarning,
            )
            return self

        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        self.base_ensemble_ = clone(self.base_ensemble)
        self.base_ensemble_ = self.base_ensemble_.fit(X, y, sample_weight=sample_weight)
        return self

    def build_ensemble(self, X, target, weights):

        """
        Build a new sub-ensemble and insert it into model

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_features)
            Batch of training data.

        target : ndarray, shape (n_samples,)
            Boosting target.

        weights : ndarray, shape (n_samples,)
            Boosting weights.

        """

        new_ensemble = clone(self.base_ensemble_reg)

        if isinstance(new_ensemble, SnapBoostingMachineRegressor):
            new_ensemble.set_params(**{"base_score": np.mean(target)})

        if found_xgboost and isinstance(new_ensemble, XGBRegressor):
            new_ensemble.set_params(**{"base_score": np.mean(target)})

        new_ensemble.fit(X, target, sample_weight=weights)

        max_sub_ensembles = (
            self.n_classes_ * self.max_sub_ensembles
            if self.n_classes_ > 2
            else self.max_sub_ensembles
        )

        if len(self.ensembles_) < max_sub_ensembles:
            self.ensembles_.append(new_ensemble)
        else:
            self.ensembles_[-1] = new_ensemble

    def train_on_batch(self, X, y, sample_weight=None):

        """
        Train on a new batch of data

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_features)
            Batch of training data.

        y : ndarray, shape (n_samples,)
            Batch of training labels.

        sample_weight : ndarray, shape (n_samples,), default=None
            Sample weights to be applied during training.

        """

        if self.n_classes_ > 2:
            pred = np.zeros(shape=(X.shape[0], self.n_classes_))
            for i, te in enumerate(self.ensembles_):
                cls_ind = i % self.n_classes_
                pred[:, cls_ind] += self.learning_rate * te.predict(X)
        else:
            pred = np.zeros(shape=(X.shape[0],))
            for i, te in enumerate(self.ensembles_):
                pred += self.learning_rate * te.predict(X)

        target, weights = self._compute_target_weights(pred, y, sample_weight)

        if self.n_classes_ > 2:

            for c in range(self.n_classes_):
                self.build_ensemble(X, target[:, c], weights[:, c])

        else:

            self.build_ensemble(X, target, weights)


class BatchedTreeEnsembleClassifier(BatchedTreeEnsemble, ClassifierMixin):

    """
    Batched Tree Ensemble Classifier

    This class enables batched training of a tree ensemble classifier on large datasets.
    Given a tree ensemble classifier, provided as a base ensemble, the algorithm will split the trees into a number of sub-ensembles.
    Each sub-ensemble is trained on a different batch of data, and the boosting mechanism is applied across batches to improve accuracy.

    Parameters
    ----------
    base_ensemble : {sklearn.ensemble.RandomForestClassifier, sklearn.ensemble.ExtraTreesClassifier, snapml.SnapRandomForestClassifier, snapml.SnapBoostingMachineClassifier, xgboost.XGBClassifier, lightgbm.LGBMClassifier}, default=snapml.SnapBoostingMachineClassifier
        The base ensemble that will be split into sub-ensembles and used for batched training.

    max_sub_ensembles: int, default=10
        The maximum number of sub-ensembles to use.
        It is recommended to set this parameter roughly equal to the expected number of batches.
        If more batches are provided than the number of sub-ensembles, the last sub-ensemble will be replaced.

    outer_lr_scaling: float, default=0.5
        The boosting mechanism across batches will use learning rate 1.0/(max_sub_ensembles ** outer_lr_scaling)

    inner_lr_scaling: float, defualt=0.5
        If the base ensemble has a learning rate (e.g. it is a boosting machine), the learning rate will be scaled by a factor (max_sub_ensembles ** inner_lr_scaling)


    Attributes
    ----------

    n_classes_ : int
        The number of classes

    classes_ : ndarary, shape (n_classes, )
        Set of unique classes

    ensembles_ : list
        Trained sub-ensembles

    """

    MIN_VAL_HESSIAN = 1e-16

    def __init__(
        self,
        base_ensemble=SnapBoostingMachineClassifier(),
        max_sub_ensembles=10,
        inner_lr_scaling=0.5,
        outer_lr_scaling=0.5,
    ):
        valid_base_ensembles = (
            RandomForestClassifier,
            ExtraTreesClassifier,
            SnapRandomForestClassifier,
            SnapBoostingMachineClassifier,
            XGBClassifier,
            LGBMClassifier,
        )
        super().__init__(
            base_ensemble,
            max_sub_ensembles,
            inner_lr_scaling,
            outer_lr_scaling,
            valid_base_ensembles,
        )

    def partial_fit(self, X, y, sample_weight=None, classes=None):

        """
        Continue training the model with a new batch of data.

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_features)
            Batch of training data.

        y : ndarray, shape (n_samples,)
            Batch of training labels.

        sample_weight : ndarray, shape (n_samples,), default=None
            Sample weights to be applied during training.

        classes : ndarray, shape (n_classes,), default=None
            Set of unique classes across the entire dataset.
            This argument is only required for first call to partial fit.

        Returns
        -------
        self : object
            Returns an instance of self.

        """

        if hasattr(self, "base_ensemble_"):
            warnings.warn(
                "This estimator has already been fit; call to partial_fit is ignored.",
                category=UserWarning,
            )
            return self

        if not hasattr(self, "ensembles_"):

            super()._validate_parameters()

            if classes is None:
                raise ValueError(
                    "classes must be provided at first call to partial fit"
                )

            self.classes_ = classes
            self.n_classes_ = len(np.unique(classes))

        labs = np.zeros_like(y, dtype=np.float32)

        for i, c in enumerate(self.classes_):
            labs[y == c] = i

        self.train_on_batch(X, labs, sample_weight)

        return self

    def predict(self, X):

        """
        Predict class labels

        Parameters
        ----------
        X : ndarray, shape=(n_samples, n_features)
            Samples to be used for prediction

        Returns
        -------
        pred : ndarray, shape = (n_samples,)
            Predicted class labels

        """

        if hasattr(self, "base_ensemble_"):
            return self.base_ensemble_.predict(X)

        margin = self.__predict_margin(X)

        if self.n_classes_ > 2:
            ind = np.argmax(margin, axis=1)
        else:
            ind = np.where(margin > 0, 1, 0)

        out = np.zeros_like(ind)
        out = out.astype(self.classes_[0].__class__)
        for i, c in enumerate(self.classes_):
            out[ind == i] = c

        return out

    def predict_proba(self, X):

        """
        Predict class probabilities

        Parameters
        ----------
        X : ndarray, shape=(n_samples, n_features)
            Samples to be used for prediction

        Returns
        -------
        pred : ndarray, shape = (n_samples, n_classes)
            Predicted class probabilities

        """

        if hasattr(self, "base_ensemble_"):
            return self.base_ensemble_.predict_proba(X)

        margin = self.__predict_margin(X)

        if self.n_classes_ > 2:
            out = self.__softmax(margin)
        else:
            p1 = self.__sigmoid(margin)
            out = np.zeros(shape=(X.shape[0], 2))
            out[:, 0] = 1 - p1
            out[:, 1] = p1

        return out

    def __predict_margin(self, X):

        """
        Predict margin

        Parameters
        ----------
        X : ndarray, shape=(n_samples, n_features)
            Samples to be used for prediction

        Returns
        -------
        pred : ndarray, shape = (n_samples,) or (n_samples, n_classes)
            Predicted margin values

        """

        if self.n_classes_ > 2:
            preds = np.zeros(shape=(X.shape[0], self.n_classes_))
            for i, ensemble in enumerate(self.ensembles_):
                cls_ind = i % self.n_classes_
                preds[:, cls_ind] += self.learning_rate * ensemble.predict(X)
        else:
            preds = np.zeros(shape=(X.shape[0],))
            for ensemble in self.ensembles_:
                preds += self.learning_rate * ensemble.predict(X)

        return preds

    def __sigmoid(self, pred):

        """
        Sigmoid transformation

        Parameters
        ----------
        pred : ndarray, shape=(n_samples,)
            Margin values to be transformed.

        Returns
        -------
        out : ndarray, shape = (n_samples,)
            Probability values.

        """

        return expit(pred)

    def __softmax(self, pred):

        """
        Softmax transformation

        Parameters
        ----------
        pred : ndarray, shape=(n_samples, n_classes)
            Margin values to be transformed.

        Returns
        -------
        out : ndarray, shape = (n_samples, n_classes)
            Probability values.

        """
        pred_max = np.amax(pred, axis=1)
        pred_e = np.exp(pred - pred_max[:, np.newaxis])
        pred_norm = np.sum(pred_e, axis=1)
        prob = pred_e / pred_norm[:, np.newaxis]
        return prob

    def __compute_gradients_logloss(self, pred, y, sample_weight):

        """
        Compute first and second-order gradient statistics for logloss objective

        Parameters
        ----------
        pred : ndarray, shape=(n_samples,)
            Running predictions from boosting

        y : ndarray, shape=(n_samples,)
            Target values

        sample_weight : ndarray, shape=(n_samples,)
            Global sample-weights (provided by user)

        Returns
        -------
        g : ndarray, shape = (n_samples,)
            First-order gradient statistics

        h : ndarray, shape = (n_samples,)
            Second-order gradient statistics

        """

        prob = self.__sigmoid(pred)

        g = prob - y
        h = prob * (1.0 - prob)

        if sample_weight is not None:
            g = np.multiply(g, sample_weight)
            h = np.multiply(h, sample_weight)

        h[h < self.MIN_VAL_HESSIAN] = self.MIN_VAL_HESSIAN

        return g, h

    def __compute_gradients_softmax(self, pred, y, sample_weight):

        """
        Compute first and second-order gradient statistics for softmax objective

        Parameters
        ----------
        pred : ndarray, shape=(n_samples, n_classes)
            Running predictions from boosting

        y : ndarray, shape=(n_samples,)
            Target values

        sample_weight : ndarray, shape=(n_samples,)
            Global sample-weights (provided by user)

        Returns
        -------
        g : ndarray, shape = (n_samples, n_classes)
            First-order gradient statistics

        h : ndarray, shape = (n_samples, n_classes)
            Second-order gradient statistics

        """

        assert pred.shape[1] == self.n_classes_

        prob_e = self.__softmax(pred)

        # 1st order info
        g = prob_e - np.eye(self.n_classes_)[y.astype(int)]
        if sample_weight is not None:
            g = g * sample_weight[:, np.newaxis]

        # 2nd order info
        h = 2.0 * np.multiply(prob_e, 1 - prob_e)
        if sample_weight is not None:
            h = h * sample_weight[:, np.newaxis]
        mask = np.full_like(h, self.MIN_VAL_HESSIAN)
        h = np.maximum(h, mask)

        return g, h

    def _compute_target_weights(self, pred, y, sample_weight):

        """
        Compute boosting target and sample weights

        Parameters
        ----------
        pred : ndarray, shape=(n_samples,) or (n_samples, n_classes)
            Running predictions from boosting

        y : ndarray, shape=(n_samples,)
            Target values

        sample_weight : ndarray, shape=(n_samples,)
            Global sample-weights (provided by user)

        Returns
        -------
        target : ndarray, shape = (n_samples,) or (n_samples, n_classes)
            Regression target for next boosting iteration

        weights : ndarray, shape = (n_samples,) or (n_samples, n_classes)
            Sample weights for next boosting iteration

        """

        if self.n_classes_ == 2:
            g, h = self.__compute_gradients_logloss(pred, y, sample_weight)
        else:
            g, h = self.__compute_gradients_softmax(pred, y, sample_weight)

        target = -np.divide(g, h)
        weights = h

        return target, weights


class BatchedTreeEnsembleRegressor(BatchedTreeEnsemble, RegressorMixin):

    """
    Batched Tree Ensemble Regressor

    This class enables batched training of a tree ensemble regressor on large datasets.
    Given a tree ensemble regressor, provided as a base ensemble, the algorithm will split the trees into a number of sub-ensembles.
    Each sub-ensemble is trained on a different batch of data, and the boosting mechanism is applied across batches to improve accuracy.

    Parameters
    ----------
    base_ensemble : {sklearn.ensemble.RandomForestRegressor, sklearn.ensemble.ExtraTreesRegressor, snapml.SnapRandomForestRegressor, snapml.SnapBoostingMachineRegressor, xgboost.XGBRegressor, lightgbm.LGBMRegressor}, default=snapml.SnapBoostingMachineRegressor
        The base ensemble that will be split into sub-ensembles and used for batched training.

    max_sub_ensembles: int, default=10
        The maximum number of sub-ensembles to use.
        It is recommended to set this parameter roughly equal to the expected number of batches.
        If more batches are provided than the number of sub-ensembles, the last sub-ensemble will be replaced.

    outer_lr_scaling: float, default=0.5
        The boosting mechanism across batches will use learning rate 1.0/(max_sub_ensembles ** outer_lr_scaling)

    inner_lr_scaling: float, defualt=0.5
        If the base ensemble has a learning rate (e.g. it is a boosting machine), the learning rate will be scaled by a factor (max_sub_ensembles ** inner_lr_scaling)


    Attributes
    ----------

    ensembles_ : list
        Trained sub-ensembles

    """

    def __init__(
        self,
        base_ensemble=SnapBoostingMachineRegressor(),
        max_sub_ensembles=10,
        inner_lr_scaling=0.5,
        outer_lr_scaling=0.5,
    ):
        valid_base_ensembles = (
            RandomForestRegressor,
            ExtraTreesRegressor,
            SnapRandomForestRegressor,
            SnapBoostingMachineRegressor,
            XGBRegressor,
            LGBMRegressor,
        )
        super().__init__(
            base_ensemble,
            max_sub_ensembles,
            inner_lr_scaling,
            outer_lr_scaling,
            valid_base_ensembles,
        )

    def partial_fit(self, X, y, sample_weight=None):

        """
        Continue training the model with a new batch of data.

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_features)
            Batch of training data.

        y : ndarray, shape (n_samples,)
            Batch of training regression targets.

        sample_weight : ndarray, shape (n_samples,), default=None
            Sample weights to be applied during training.

        Returns
        -------
        self : object
            Returns an instance of self.

        """

        if hasattr(self, "base_ensemble_"):
            warnings.warn(
                "This estimator has already been fit; call to partial_fit is ignored.",
                category=UserWarning,
            )
            return self

        if not hasattr(self, "ensembles_"):
            super()._validate_parameters()

        self.n_classes_ = 2
        self.train_on_batch(X, y, sample_weight)
        return self

    def predict(self, X):

        """
        Predict target values

        Parameters
        ----------
        X : ndarray, shape=(n_samples, n_features)
            Samples to be used for prediction

        Returns
        -------
        pred : ndarray, shape = (n_samples,)
            Predicted target values

        """

        if hasattr(self, "base_ensemble_"):
            return self.base_ensemble_.predict(X)

        preds = np.zeros(shape=(X.shape[0],))
        for ensemble in self.ensembles_:
            preds += self.learning_rate * ensemble.predict(X)

        return preds

    def _compute_target_weights(self, pred, y, sample_weight):

        """
        Compute boosting target and sample weights

        Parameters
        ----------
        pred : ndarray, shape=(n_samples,)
            Running predictions from boosting

        y : ndarray, shape=(n_samples,)
            Target values

        sample_weight : ndarray, shape=(n_samples,)
            Global sample-weights (provided by user)

        Returns
        -------
        target : ndarray, shape = (n_samples,)
            Regression target for next boosting iteration

        weights : ndarray, shape = (n_samples,)
            Sample weights for next boosting iteration

        """

        g = 2.0 * (pred - y)
        h = np.full_like(pred, 2.0)

        if sample_weight is not None:
            g = np.multiply(g, sample_weight)
            h = np.multiply(h, sample_weight)

        target = -np.divide(g, h)
        weights = h

        return target, weights
