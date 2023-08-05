# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2021. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np

from sklearn.multioutput import MultiOutputClassifier
from sklearn.calibration import CalibratedClassifierCV

from snapml import SupportVectorMachine as snapSVM
from snapml import LogisticRegression as snapLR
from sklearn.svm import LinearSVC as sklearnSVM
from sklearn.linear_model import LogisticRegression as sklearnLR

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(False)

estimator_types = [CalibratedClassifierCV]
base_estimator_types = [snapSVM, snapLR, sklearnSVM, sklearnLR]

## @ingroup pythonclasses
class MultiOutputCalibratedClassifier(MultiOutputClassifier):

    """
    Multi Output Calibrated Classifier used for multi-target classification.

    This model fits one classifier per target. It can be used for classifiers
    that do not have native support for multi-target classification.


    Parameters
    ----------
    estimator : estimator object
        A scikit-learn CalibratedClassifierCV object.

    n_jobs : int or None, optional (default=None)
        The number of jobs to run in parallel.
        :meth:`fit` and :meth:`predict` will be parallelized for each target.
        When individual estimators are fast to train or predict,
        using ``n_jobs > 1`` can result in slower performance due
        to the parallelism overhead.
        ``None`` means `1` unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all available processes / threads.


    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        Class labels.

    estimators_ : list of ``n_output`` estimators
        Estimators used for predictions.

    n_features_in_ : int
        Number of features seen during :term:`fit`. Only defined if the
        underlying `base_estimator` of the CalibratedClassifierCV `estimator`
        exposes such an attribute when fit.

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Only defined if the
        underlying `base_estimator` of the CalibratedClassifierCV `estimator`
        exposes such an attribute when fit.
    """

    def __init__(self, estimator, *, n_jobs=None):
        if type(estimator) not in estimator_types:
            estimator_parents_types = estimator.__class__.__bases__
            if not (set(estimator_parents_types) & set(estimator_types)):
                raise TypeError("Estimator not supported : ", type(estimator))

        estimator_params = estimator.get_params(deep=False)
        if type(estimator_params["base_estimator"]) not in base_estimator_types:
            base_estimator_parents_types = estimator_params[
                "base_estimator"
            ].__class__.__bases__
            if not (set(base_estimator_parents_types) & set(base_estimator_types)):
                raise TypeError(
                    "Base estimator not supported: ",
                    base_estimator_types,
                )

        super().__init__(estimator, n_jobs=n_jobs)

    def fit(self, X, Y, sample_weight=None, optimize_for_inference=True, **fit_params):

        """
        Fit the model to the feature matrix X and labels Y.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The train data.

        Y : array-like of shape (n_samples, n_classes)
            The train labels.

        sample_weight : array-like of shape (n_samples,), default=None
            The sample weights. If `None`, all samples have the same weight.
            Only supported if the underlying classifier supports sample
            weights.

        optimize_for_inference : bool, default=True
            If True, save the model and calibration coefficients as attributes
            to be used at predict_proba time. It is recommended to use the
            default setting for performance-optimized inference.

        **fit_params : dict of string -> object
            Parameters passed to the ``estimator.fit`` method of each step.

        Returns
        -------
        self : object
            Returns a fitted instance.
        """

        super().fit(X, Y, sample_weight, **fit_params)

        if optimize_for_inference:
            self.optimize_for_inference()

        return self

    def optimize_for_inference(self):

        self.intercepts_ = []
        self.coefs_ = []
        self.As_ = []
        self.Bs_ = []

        # if intercept is float, training was run with fit_intercept False
        fit_intercept_false = isinstance(
            self.estimators_[0].calibrated_classifiers_[0].base_estimator.intercept_,
            float,
        )

        # extract the model coefficients, intercepts, and calibration coefficients
        for x in self.estimators_:
            if fit_intercept_false:
                self.intercepts_.append(
                    x.calibrated_classifiers_[0].base_estimator.intercept_
                )
            else:
                self.intercepts_.append(
                    x.calibrated_classifiers_[0].base_estimator.intercept_[0]
                )
            self.coefs_.append(x.calibrated_classifiers_[0].base_estimator.coef_[0])
            self.As_.append(x.calibrated_classifiers_[0].calibrators[0].a_)
            self.Bs_.append(x.calibrated_classifiers_[0].calibrators[0].b_)

        self.intercepts_ = np.array(self.intercepts_).astype(np.float32)
        self.coefs_ = np.array(self.coefs_).astype(np.float32)
        self.coefs_ = np.asfortranarray(self.coefs_)
        self.As_ = np.array(self.As_).astype(np.float32)
        self.Bs_ = np.array(self.Bs_).astype(np.float32)

    def predict_proba(self, X):

        """
        Predict class probabilities for each output.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        p : array of shape (n_samples, n_classes)
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute :term:`classes_`.
        """

        if not hasattr(self, "coefs_"):
            preds = super().predict_proba(X)
            preds = np.array(list(map(lambda x: x[:, 1], preds))).T
            return preds

        preds = X.astype(np.float32).dot(self.coefs_.T)
        preds += self.intercepts_
        preds *= self.As_
        preds += self.Bs_
        preds = 1.0 / (1.0 + np.exp(preds))

        # required if the upstream frameworks use json to serialize the predicted classes
        preds = preds.astype(np.float64)

        return preds
