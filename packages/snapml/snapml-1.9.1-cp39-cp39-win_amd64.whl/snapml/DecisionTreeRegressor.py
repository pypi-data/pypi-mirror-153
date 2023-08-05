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
from snapml.DecisionTree import DecisionTree

## @ingroup pythonclasses
class DecisionTreeRegressor(DecisionTree, BaseEstimator, RegressorMixin):

    """
    Decision Tree Regressor

    This class implements a decision tree regressor using the IBM Snap ML library.
    It can be used for regression tasks.

    Parameters
    ----------
    criterion : {'mse'}, default="mse"
        This function measures the quality of a split.

    splitter : string, default="best"
        This parameter defines the strategy used to choose the split at each node.
        Possible values: "best" and "random". "random" is currently not supported.

    max_depth : int or None, default=None
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than min_samples_leaf samples.

    min_samples_leaf : int or float, default=1
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it generates at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.
        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then consider `ceil(min_samples_leaf * n_samples)` as the minimum number.

    max_features : int, float, string or None, default=None
        The number of features to consider when looking for the best split:
            - If int, then consider `max_features` features at each split.
            - If float, then consider `int(max_features * n_features)` features at each split.
            - If "auto", then `max_features=n_features`.
            - If "sqrt", then `max_features=sqrt(n_features)`.
            - If "log2", then `max_features=log2(n_features)`.
            - If None, then `max_features=n_features`.

    random_state : int, or None, default=None
        If int, random_state is the seed used by the random number generator;
        If None, the random number generator is the RandomState instance used by `np.random`.

    n_jobs : integer, default=1
        The number of CPU threads to use.

    use_histograms : boolean, default=True
        Use histogram-based splits rather than exact splits.

    hist_nbins : int, default=256
        Number of histogram bins.

    use_gpu : boolean, default=False
        Use GPU acceleration (only supported for histogram-based splits).

    gpu_id : int, default=0
        Device ID of the GPU which will be used when GPU acceleration is enabled.

    verbose : bool, default=False
        If True, it prints debugging information while training. Warning: this will increase the
        training time. For performance evaluation, use verbose=False.


    Attributes
    ----------

    """

    PARAMS = [
        {
            "name": "criterion",
            "attr": [{"values": ("mse")}],
        },  # and (not criterion == 'entropy'):
        {"name": "splitter", "attr": [{"values": ("best")}]},
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
        {"name": "random_state", "attr": [{"values": [None]}, {"type": "int"}]},
        {"name": "verbose", "attr": [{"type": "bool"}]},
        {"name": "n_jobs", "attr": [{"type": "int", "ge": 1}]},
        {"name": "use_histograms", "attr": [{"type": "bool"}]},
        {"name": "hist_nbins", "attr": [{"type": "int", "gt": 0, "le": 256}]},
        {"name": "use_gpu", "attr": [{"type": "bool"}]},
        {"name": "gpu_id", "attr": [{"type": "int", "ge": 0}]},
    ]

    def __init__(
        self,
        criterion="mse",
        splitter="best",
        max_depth=None,
        min_samples_leaf=1,
        max_features=None,
        random_state=None,
        n_jobs=1,
        use_histograms=True,
        hist_nbins=256,
        use_gpu=False,
        gpu_id=0,
        verbose=False,
    ):

        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.use_histograms = use_histograms
        self.hist_nbins = hist_nbins
        self.use_gpu = use_gpu
        self.gpu_id = gpu_id
        self.verbose = verbose
        self.task_type_ = "regression"
        self.params = DecisionTreeRegressor.PARAMS
        self.n_features_in_ = 0
        # self.node_count = 1  # do not see that this is used anywhere

    def extract_and_check_labels(self, y_train):
        labs = np.array([])
        self.n_classes_ = 2
        labs = y_train.astype(np.float32)
        return labs

    def check_value_of_max_features(self, num_ft):
        # Check the value of max_features
        if self.max_features in [None, "auto"]:
            max_features = 0  # all features
        elif self.max_features in ["sqrt"]:
            max_features = np.ceil(np.sqrt(num_ft))
        elif self.max_features == "log2":
            import math

            max_features = np.ceil(math.log2(num_ft))
        elif isinstance(self.max_features, (int)):
            max_features = self.max_features
        elif isinstance(self.max_features, (float)):
            max_features = np.ceil(self.max_features * num_ft)
        else:
            raise ValueError("Parameter max_features: unable to parse.")

        max_features = int(max_features)
        if max_features > num_ft:
            raise ValueError(
                "Parameter max_features: invalid value. The value of max_features is larger than the number of features in the train dataset."
            )

        return max_features

    def create_class(self, pred):
        # dont't do anything
        return pred
