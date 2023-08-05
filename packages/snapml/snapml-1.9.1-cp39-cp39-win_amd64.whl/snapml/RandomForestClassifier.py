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
import warnings

from sklearn.base import BaseEstimator, ClassifierMixin

from snapml.utils import _param_check
from snapml.RandomForest import RandomForest

## @ingroup pythonclasses
class RandomForestClassifier(RandomForest, BaseEstimator, ClassifierMixin):

    """
    Random Forest Classifier

    This class implements a random forest classifier using the IBM Snap ML library.
    It can be used for binary and multi-class classification problems.

    Parameters
    ----------
    n_estimators : integer, default=10
        This parameter defines the number of trees in forest.

    criterion : string, default="gini"
        This function measures the quality of a split. The currently supported criterion is "gini".

    max_depth : integer or None, default=None
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than min_samples_leaf samples.

    min_samples_leaf : int or float, default=1
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.
        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a fraction and
        `ceil(min_samples_leaf * n_samples)` are the minimum number of samples for each node.

    max_features : int, float, string or None, default='auto'
        The number of features to consider when looking for the best split:
            - If int, then consider `max_features` features at each split.
            - If float, then `max_features` is a fraction and
              `int(max_features * n_features)` features are considered at each
              split.
            - If "auto", then `max_features=sqrt(n_features)`.
            - If "sqrt", then `max_features=sqrt(n_features)`.
            - If "log2", then `max_features=log2(n_features)`.
            - If None, then `max_features=n_features`.

    bootstrap : boolean, default=True
        This parameter determines whether bootstrap samples are used when building trees.

    n_jobs : integer, default=1
        The number of jobs to run in parallel the fit function.

    random_state : integer, or None, default=None
        If integer, random_state is the seed used by the random number generator.
        If None, the random number generator is the RandomState instance used by `np.random`.

    verbose : boolean, default=False
        If True, it prints debugging information while training.
        Warning: this will increase the training time. For performance evaluation, use verbose=False.

    use_histograms : boolean, default=False
        Use histogram-based splits rather than exact splits.

    hist_nbins : int, default=256
        Number of histogram bins.

    use_gpu : boolean, default=False
        Use GPU acceleration (only supported for histogram-based splits).

    gpu_ids : array-like of int, default: [0]
        Device IDs of the GPUs which will be used when GPU acceleration is enabled.

    compress_trees : bool, default=False
        Compress trees after training for fast inference.

    Attributes
    ----------

    """

    PARAMS = [
        {"name": "n_estimators", "attr": [{"type": "int", "ge": 1}]},
        {
            "name": "criterion",
            "attr": [{"values": ("gini")}],
        },  # and (not criterion == 'entropy'):
        {"name": "max_depth", "attr": [{"values": [None]}, {"type": "int", "gt": 0}]},
        {
            "name": "min_samples_leaf",
            "attr": [{"type": "int", "gt": 0}, {"type": "float", "gt": 0, "le": 1}],
        },
        {
            "name": "max_features",
            "attr": [
                {"values": [None, "log2", "sqrt", "auto"]},
                {"type": "int", "gt": 0},
                {"type": "float", "gt": 0, "le": 1},
            ],
        },
        {"name": "bootstrap", "attr": [{"type": "bool"}]},
        {
            "name": "n_jobs",
            "attr": [{"type": "int", "gt": 0}],
        },  # TODO: scikit-learn -1 not yet covered
        {"name": "random_state", "attr": [{"values": [None]}, {"type": "int"}]},
        {"name": "verbose", "attr": [{"type": "bool"}]},
        {"name": "use_histograms", "attr": [{"type": "bool"}]},
        {"name": "hist_nbins", "attr": [{"type": "int", "gt": 0, "le": 256}]},
        {"name": "use_gpu", "attr": [{"type": "bool"}]},
        {"name": "gpu_ids", "attr": [{"type": "list"}]},
        {"name": "compress_trees", "attr": [{"type": "bool"}]},
    ]

    def __init__(
        self,
        n_estimators=10,
        criterion="gini",
        max_depth=None,
        min_samples_leaf=1,
        max_features="auto",
        bootstrap=True,
        n_jobs=1,
        random_state=None,
        verbose=False,
        use_histograms=False,
        hist_nbins=256,
        use_gpu=False,
        gpu_ids=[0],
        compress_trees=False,
    ):

        self.n_estimators = n_estimators
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose
        self.use_histograms = use_histograms
        self.hist_nbins = hist_nbins
        self.use_gpu = use_gpu
        self.gpu_ids = gpu_ids
        self.task_type_ = "classification"
        self.params = RandomForestClassifier.PARAMS
        self.n_features_in_ = 0
        self.compress_trees = compress_trees
        self.cache_id_ = 0

    def extract_and_check_labels(self, y_train):
        # Extract set of unique labels from y_train
        self.classes_ = np.unique(y_train)
        self.n_classes_ = len(self.classes_)

        # Check the labels of y_train and train model(s)
        if len(self.classes_) == 1:
            raise ValueError(
                "There must be at least two unique label values in the train dataset."
            )

        labs = np.zeros_like(y_train, dtype=np.float32)

        self.ind2class_ = {}
        for i, c in enumerate(self.classes_):
            self.ind2class_[i] = c
            labs[y_train == c] = i

        if (self.use_gpu == True) and (self.n_classes_ > 2):
            raise ValueError(
                "GPU acceleration not supported for multiclass classification."
            )

        return labs

    def check_value_of_max_features(self, num_ft):
        # Check the value of max_features
        if self.max_features is None:
            max_features = 0  # all features
        elif self.max_features in ["auto", "sqrt"]:
            max_features = int(np.sqrt(num_ft))
        elif self.max_features == "log2":
            import math

            max_features = int(math.log2(num_ft))
        elif isinstance(self.max_features, (int)):
            max_features = self.max_features
        elif isinstance(self.max_features, (float)):
            max_features = int(self.max_features * num_ft)
        else:
            raise ValueError("Parameter max_features: unable to parse.")

        max_features = int(max_features)
        if max_features > num_ft:
            raise ValueError(
                "Parameter max_features: invalid value. The value of max_features is larger than the number o features in the train dataset."
            )

        return max_features

    def create_class(self, pred):

        pred_out = np.zeros_like(pred)
        pred_out = pred_out.astype(self.ind2class_[0].__class__)

        for i, c in self.ind2class_.items():
            if self.n_classes_ == 2:
                pred_out[(pred > 0) == i] = c
            else:
                pred_out[pred == i] = c

        return pred_out

    def predict_proba(self, X, n_jobs=None):

        """
        Predict class probabilities.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting probabilities.
        n_jobs : int, default=None
            By default the value of the class attribute is used..
        Returns
        -------
        proba: array-like, shape = (n_samples, n_classes)
            Returns the predicted probabilities the sample.
        """

        if n_jobs is not None:
            warnings.warn(
                "Setting n_jobs as an argument to predict_proba may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_params method before calling predict_proba, e.g.: set_params(n_jobs=4)",
                FutureWarning,
            )
            _param_check(RandomForestClassifier.PARAMS, "n_jobs", n_jobs)
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

        data = X.astype(np.float32)
        data = np.ascontiguousarray(data)  # ensure row-major format

        # Generate predictions
        proba = self.c_predict(
            X.shape[0],
            X.shape[1],
            np.array([]),
            np.array([]),
            data,
            n_jobs,
            True,
            self.n_classes_,
        )

        if self.n_classes_ == 2:
            out = np.zeros((proba.shape[0], 2))
            out[:, 0] = 1 - proba
            out[:, 1] = proba
        else:
            out = np.reshape(proba, (X.shape[0], self.n_classes_ - 1))
            new_col = 1.0 - out.sum(axis=1)
            new_col = new_col.reshape((-1, 1))
            out = np.append(out, new_col, axis=1)

        return out
