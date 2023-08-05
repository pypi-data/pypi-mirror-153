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

from sklearn.base import BaseEstimator, RegressorMixin
from snapml.RandomForest import RandomForest

## @ingroup pythonclasses
class RandomForestRegressor(RandomForest, BaseEstimator, RegressorMixin):

    """
    Random Forest Regressor

    This class implements a random forest regressor using the IBM Snap ML library.
    It can be used for regression tasks.

    Parameters
    ----------
    n_estimators : integer, default=10
        This parameter defines the number of trees in forest.

    criterion : string, default="mse"
        This function measures the quality of a split. The currently supported criterion is "mse".

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
            - If "auto", then `max_features=n_features`.
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

    use_gpu : boolean, default=True
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
            "attr": [{"values": ("mse")}],
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
        criterion="mse",
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
        self.task_type_ = "regression"
        self.params = RandomForestRegressor.PARAMS
        self.n_features_in_ = 0
        self.compress_trees = compress_trees
        self.cache_id_ = 0

    def extract_and_check_labels(self, y_train):
        # Extract set of unique labels from y_train
        self.uniq_labs_ = np.unique(y_train)

        # Check the labels of y_train and train model(s)
        if len(self.uniq_labs_) == 1:
            raise ValueError(
                "There must be at least two unique label values in the train dataset."
            )
        labs = y_train.astype(np.float32)

        self.n_classes_ = len(self.uniq_labs_)

        return labs

    def check_value_of_max_features(self, num_ft):
        # Check the value of max_features
        if self.max_features in [None]:
            max_features = 0  # all features
        elif self.max_features in ["sqrt", "auto"]:
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
        # dont't do anything
        return pred
