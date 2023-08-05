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
import copy
import math
import warnings

from snapml.utils import _is_mpi_enabled, _param_check

from snapml._import import import_libsnapml

from .version import __version__

libsnapml = import_libsnapml(False)

## @ingroup pythonclasses
class BoostingMachine:

    """
    BoostingMachine

    This class implements a boosting machine that can be used to construct an ensemble of decision trees.
    It can be used for both classification and regression tasks.
    In contrast to other boosting frameworks, Snap ML's boosting machine does not utilize a fixed maximal tree depth at each boosting iteration.
    Instead, the tree depth is sampled at each boosting iteration according to a discrete uniform distribution.
    The fit and predict functions accept numpy.ndarray data structures.

    Boosting params dictionary has the following structure:

    params = {
        'boosting_params' {
            'num_threads': 1,
            'num_round': 10,
            'objective': 'mse',
            'min_max_depth: 1,
            'max_max_depth: 6,
            'early_stopping_rounds': 10,
            'random_state': 0,
            'base_score': None,
            'learning_rate':'0.1',
            'verbose': False,
            'enable_profile': False,
            'compress_trees': False,
        },
        'tree_params': {
            'use_histograms': True,
            'hist_nbins': 256,
            'use_gpu': False,
            'gpu_ids': [0],
            'colsample_bytree': 1.0,
            'subsample': 1.0,
            'lambda_l2': 0.0,
            'select_probability': 1.0
        },
        'kernel_params': {
            'gamma': 1.0,
            'n_components': 10
        },
        'ridge_params': {
            'regularizer': 1.0,
            'fit_intercept': False,
            'select_probability': 0.0
        }
    }

    For classification set 'objective' to 'logloss', and for regression use 'mse'.

    Parameters
    ----------

    params: dict

    Attributes
    ----------

    feature_importances_ : array-like, shape=(n_features,)
        Feature importances computed across trees.

    """

    PARAMS = {
        "boosting_params": [
            {"name": "num_threads", "attr": [{"type": "int", "ge": 1}]},
            {"name": "num_round", "attr": [{"type": "int", "ge": 1}]},
            {
                "name": "objective",
                "attr": [{"values": ["mse", "logloss", "cross_entropy", "softmax"]}],
            },
            {"name": "min_max_depth", "attr": [{"type": "int", "ge": 1}]},
            {"name": "max_max_depth", "attr": [{"type": "int", "ge": 1}]},
            {"name": "early_stopping_rounds", "attr": [{"type": "int", "ge": 1}]},
            {"name": "random_state", "attr": [{"type": "int"}]},
            {"name": "base_score", "attr": [{"values": [None]}, {"type": "float"}]},
            {"name": "learning_rate", "attr": [{"type": "float", "ge": 0}]},
            {"name": "verbose", "attr": [{"type": "bool"}]},
            {"name": "enable_profile", "attr": [{"type": "bool"}]},
            {"name": "compress_trees", "attr": [{"type": "bool"}]},
        ],
        "tree_params": [
            {"name": "use_histograms", "attr": [{"type": "bool"}]},
            {"name": "hist_nbins", "attr": [{"type": "int", "gt": 0, "le": 256}]},
            {"name": "use_gpu", "attr": [{"type": "bool"}]},
            {"name": "gpu_ids", "attr": [{"type": "list"}]},
            {"name": "colsample_bytree", "attr": [{"type": "float", "gt": 0, "le": 1}]},
            {"name": "subsample", "attr": [{"type": "float", "gt": 0, "le": 1}]},
            {
                "name": "parallel_by_example",
                "attr": [{"type": "bool"}],
            },  # not used anymore, just for compatibility
            {"name": "lambda_l2", "attr": [{"type": "float", "ge": 0}]},
            {
                "name": "select_probability",
                "attr": [{"type": "float", "ge": 0, "le": 1}],
            },
        ],
        "ridge_params": [
            {"name": "regularizer", "attr": [{"type": "float", "gt": 0}]},
            {"name": "fit_intercept", "attr": [{"type": "bool"}]},
            {
                "name": "select_probability",
                "attr": [{"type": "float", "ge": 0, "le": 1}],
            },
        ],
        "kernel_params": [
            {"name": "gamma", "attr": [{"type": "float"}]},
            {"name": "n_components", "attr": [{"type": "int", "ge": 1}]},
        ],
    }

    def __init__(self, params=None):

        self.cache_id_ = 0

        # params is a dictionary of dictionaries that includes all the model parameters
        # params = {boosting_params, tree_params, rbf_params, ridge_params}
        # all *_params are dictionaries
        self.params_ = {}
        self.boosting_params_ = {}
        self.tree_params_ = {}
        self.kernel_params_ = {}
        self.ridge_params_ = {}

        # define boosting model defaults
        self.boosting_params_["num_threads"] = 1
        self.boosting_params_["num_round"] = 10
        self.boosting_params_["objective"] = "mse"
        self.boosting_params_["min_max_depth"] = 1
        self.boosting_params_["max_max_depth"] = 6
        self.boosting_params_["early_stopping_rounds"] = 10
        self.boosting_params_["random_state"] = 0
        self.boosting_params_["base_score"] = None
        self.boosting_params_["learning_rate"] = 0.1
        self.boosting_params_["verbose"] = False
        self.boosting_params_["enable_profile"] = False
        self.boosting_params_["compress_trees"] = False
        self.params_["boosting_params"] = self.boosting_params_

        # define tree model defaults
        self.tree_params_["use_histograms"] = True
        self.tree_params_["hist_nbins"] = 256
        self.tree_params_["use_gpu"] = False
        self.tree_params_["gpu_ids"] = [0]
        self.tree_params_["colsample_bytree"] = 1.0
        self.tree_params_["subsample"] = 1.0
        self.tree_params_["lambda_l2"] = 0.0
        self.tree_params_["select_probability"] = 1.0
        self.params_["tree_params"] = self.tree_params_

        # define ridge regression model defaults
        self.ridge_params_["regularizer"] = 1.0
        self.ridge_params_["fit_intercept"] = False
        self.ridge_params_["select_probability"] = (
            1.0 - self.tree_params_["select_probability"]
        )
        self.params_["ridge_params"] = self.ridge_params_

        # define kernel approximator (rbf sampler) defaults
        self.kernel_params_["gamma"] = 1.0
        self.kernel_params_["n_components"] = 10
        self.params_["kernel_params"] = self.kernel_params_

        self.set_param(params)

        self.model_ = np.array([], dtype=np.float32)
        self.model_size_ = 0

    def set_param(self, params):

        """
        Set parameters for this model.

        Parameters
        ----------
        params: dict
           dict e.g. like the following to set the number of threads:
           set_param(params={"boosting_params": {"num_threads": num_threads}})
        """

        if params is None:
            return

        params_keys = params.keys()
        params_copy = copy.deepcopy(self.params_)

        # Check if the user provided keys are supported (first level)
        library_first_level_keys = list(params_copy.keys())
        unsupported_keys = list(
            np.setdiff1d(list(params_keys), library_first_level_keys)
        )
        if len(unsupported_keys) > 0:
            raise KeyError(
                "Unsupported keys in the user-defined parameters dictionary: ",
                unsupported_keys,
            )

        # Check if the user provided keys are supported (second level)
        for params_type in library_first_level_keys:
            if params_type in params_keys:
                user_keys = list(params[params_type].keys())
                library_keys = list(params_copy[params_type].keys())
                unsupported_keys = list(np.setdiff1d(user_keys, library_keys))
                if len(unsupported_keys) > 0:
                    raise KeyError(
                        "Unsupported keys in the user-defined {} parameters: {}".format(
                            params_type, unsupported_keys
                        )
                    )

        """
        Boosting-model-specific parameters
        """
        if "boosting_params" in params_keys:
            for var in params["boosting_params"].keys():
                _param_check(
                    BoostingMachine.PARAMS["boosting_params"],
                    var,
                    params["boosting_params"][var],
                )
                params_copy["boosting_params"][var] = params["boosting_params"][var]

        """
        Tree-model-specific parameters
        """
        if "tree_params" in params_keys:
            for var in params["tree_params"].keys():
                _param_check(
                    BoostingMachine.PARAMS["tree_params"],
                    var,
                    params["tree_params"][var],
                )
                params_copy["tree_params"][var] = params["tree_params"][var]

        """
        Ridge-regression-model-specific parameters
        """
        if "ridge_params" in params_keys:
            for var in params["ridge_params"].keys():
                _param_check(
                    BoostingMachine.PARAMS["ridge_params"],
                    var,
                    params["ridge_params"][var],
                )
                params_copy["ridge_params"][var] = params["ridge_params"][var]

        """
        RBF-Sampler-model-specific parameters
        """
        if "kernel_params" in params_keys:
            for var in params["kernel_params"].keys():
                _param_check(
                    BoostingMachine.PARAMS["kernel_params"],
                    var,
                    params["kernel_params"][var],
                )
                params_copy["kernel_params"][var] = params["kernel_params"][var]

        # Check for dependencies
        if (
            params_copy["boosting_params"]["max_max_depth"]
            < params_copy["boosting_params"]["min_max_depth"]
        ):
            raise ValueError(
                "Parameter boosting_params:max_max_depth should be >= boosting_params:min_max_depth."
            )

        if (
            params_copy["tree_params"]["use_gpu"] == True
            and params_copy["tree_params"]["use_histograms"] == False
        ):
            raise ValueError(
                "GPU acceleration can only be enabled if tree_params:use_histograms parameter is True."
            )

        if (
            params_copy["ridge_params"]["select_probability"]
            + params_copy["tree_params"]["select_probability"]
            != 1.0
        ):
            # print warning only if explicitely set by the user
            if "select_probability" in params["ridge_params"].keys():
                print(
                    "The sum of the tree and ridge selection probabilities should be 1.0. Updating probabilities proba(ridge) = 1 - proba(tree)."
                )
            params_copy["ridge_params"]["select_probability"] = (
                1.0 - params_copy["tree_params"]["select_probability"]
            )

        self.params_ = copy.deepcopy(params_copy)

    def __setstate__(self, d):
        # if the model was trained, let's rebuild the cache
        if "model_size_" in d.keys() and d["model_size_"] > 0:
            d["cache_id_"] = libsnapml.booster_cache(d["model_"], d["model_size_"])
        else:
            d["cache_id_"] = 0

        self.__dict__ = d

    def __del__(self):
        # if boosting machine was cached, let's ensure that it gets destroyed in C++
        if hasattr(self, "cache_id_") and self.cache_id_ > 0:
            libsnapml.booster_delete(self.cache_id_)

    def get_params(self):

        """
        Get the values of the model parameters.

        Returns
        -------
        params : dict
        """

        return self.params_

    def _import_model(self, input_file, input_type):

        """
        Import a pre-trained ensemble from the given input file of the given type.

        Supported import formats include PMML, ONNX, XGBoost json and lightGBM text. The
        corresponding input file types to be provided to the import_model function are
        'pmml', 'onnx', 'xgb_json', and 'lightgbm' respectively.

        If the input file contains features that are not supported by the import function
        then a runtime error is thrown indicating the feature and the line number within
        the input file containing the feature.

        Parameters
        ----------
        input_file : str
            Input filename

        input_type : {'pmml', 'onnx', 'xgb_json', 'lightgbm'}
            Input file type

        Returns
        -------
        self : object
        """

        if (not isinstance(input_file, (str))) or (input_file == ""):
            raise Exception("Input file name not provided.")

        if (not isinstance(input_type, (str))) or (input_type == ""):
            raise Exception("Input file type not provided.")

        (
            self.model_,
            self.model_size_,
            self.classes_,
            self.n_classes_,
        ) = libsnapml.booster_import(input_file, input_type)

        if self.classes_ is not None:
            self.ind2class_ = {}
            for i, c in enumerate(self.classes_):
                self.ind2class_[i] = c
        else:
            self.ind2class_ = None

    def export_model(self, output_file, output_type="pmml"):

        """
        Export model trained in snapml to the given output file using a format of the given type.

        Currently only PMML is supported as export format. The corresponding output file type to
        be provided to the export_model function is 'pmml'.

        Parameters
        ----------
        output_file : str
            Output filename

        output_type : {'pmml'}
            Output file type

        """

        if (not isinstance(output_file, (str))) or (output_file == ""):
            raise Exception("Output file name not provided.")

        if (not isinstance(output_type, (str))) or (output_type == ""):
            raise Exception("Output file type not provided.")

        if self.ind2class_ is not None:
            if not np.can_cast(self.ind2class_[0].__class__, np.float64):
                raise Exception("Cannot cast class labels to float for export.")
            classes = np.array(
                [v for i, v in self.ind2class_.items()], dtype=np.float64
            )
        else:
            classes = np.array([], dtype=np.float64)

        libsnapml.booster_export(
            output_file,
            output_type,
            self.model_,
            self.model_size_,
            self.cache_id_,
            classes,
            __version__,
        )

    def fit(
        self,
        X_train,
        y_train,
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
        X_train : dense matrix (ndarray)
            Train dataset

        y_train : array-like, shape = (n_samples,)
            The target vector corresponding to X_train.

        sample_weight : array-like, shape = (n_samples,)
            Training sample weights

        X_val : dense matrix (ndarray)
            Validation dataset

        y_val : array-like, shape = (n_samples,)
            The target vector corresponding to X_val.

        sample_weight_val : array-like, shape = (n_samples,)
            Validation sample weights

        aggregate_importances : bool, default=True
            If True, feature importances will be aggregated over boosting rounds.
            If False, feature importances will be available on a per-round basis.

        Returns
        -------
        self : object
        """

        # Boosting Machine model random state
        # if (self.params_['boosting_params']['random_state'] == None):
        #    # Not sure if this should be the random state
        #    random_state = np.random.get_state()[1][0]
        # else:
        # random_state = self.params_['boosting_params']['random_state']

        if type(X_train).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        if X_val is not None and type(X_val).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        # helper function to prep data
        def prep_data(X, y, name):
            num_ft = 0
            num_nz = 0
            indptr = np.array([])
            indices = np.array([])
            data = np.array([])
            labs = np.array([])

            # get number of examples/features
            num_ex = X.shape[0]
            num_ft = X.shape[1]

            # in most cases, y_train should contain all examples
            if len(y) != num_ex:
                raise ValueError(
                    "Inconsistent dimensions: X.shape[0] must equal len(y)"
                )

            if (num_ex == 0) or (num_ft == 0):
                raise ValueError(
                    "Wrong dimensions: X.shape[0] and X.shape[1] must be > 0."
                )

            num_nz = num_ex * num_ft
            data = np.ascontiguousarray(X, dtype=np.float32)

            labs = y.astype(np.float32)

            return num_ex, num_ft, num_nz, indptr, indices, data, labs

        if (
            self.params_["boosting_params"]["objective"] == "logloss"
            or self.params_["boosting_params"]["objective"] == "softmax"
        ):

            classes = np.unique(y_train)
            self.n_classes_ = len(classes)

            y_train_snap = np.zeros_like(y_train, dtype=np.float32)
            y_val_snap = np.zeros_like(y_val, dtype=np.float32)

            self.ind2class_ = {}
            for i, c in enumerate(classes):
                self.ind2class_[i] = c
                y_train_snap[y_train == c] = i
                y_val_snap[y_val == c] = i
        else:
            y_train_snap = y_train
            y_val_snap = y_val
            self.n_classes_ = 2
            self.ind2class_ = None

        # the user has not set the base score, thus we will set it so that it speeds up the learning
        if self.params_["boosting_params"]["base_score"] is None:

            # this is a regression problem
            if self.params_["boosting_params"]["objective"] == "mse":
                if sample_weight is None:
                    self.params_["boosting_params"]["base_score"] = np.average(
                        y_train_snap
                    )
                else:
                    self.params_["boosting_params"]["base_score"] = np.average(
                        y_train_snap, weights=sample_weight
                    )

            elif self.params_["boosting_params"]["objective"] == "cross_entropy":
                p = (
                    np.average(y_train_snap)
                    if sample_weight is None
                    else np.average(y_train_snap, weights=sample_weight)
                )
                self.params_["boosting_params"]["base_score"] = -np.log(1.0 / p - 1.0)

            # this is a classification problem
            elif self.params_["boosting_params"]["objective"] == "logloss":
                if sample_weight is None:
                    sum_positives = np.sum(y_train_snap > 0)
                    sum_negatives = y_train_snap.shape[0] - sum_positives
                    self.params_["boosting_params"]["base_score"] = (
                        np.log(sum_positives / sum_negatives)
                        if sum_negatives > 0 and sum_positives > 0
                        else 0.0
                    )
                else:
                    sum_positives = np.sum(sample_weight[y_train_snap > 0])
                    sum_negatives = np.sum(sample_weight) - sum_positives
                    self.params_["boosting_params"]["base_score"] = (
                        np.log(sum_positives / sum_negatives)
                        if sum_negatives > 0 and sum_positives > 0
                        else 0.0
                    )

            else:
                # in order to implement the equivalent behaviour for multiclass, we would
                # need to extend the base score from a scalar to a vector (TBD).
                self.params_["boosting_params"]["base_score"] = 0.0

        # prepare training data
        (
            train_num_ex,
            train_num_ft,
            train_num_nz,
            train_indptr,
            train_indices,
            train_data,
            train_labs,
        ) = prep_data(X_train, y_train_snap, "train")

        # prepare validation data
        if X_val is not None and y_val is not None:
            (
                val_num_ex,
                val_num_ft,
                val_num_nz,
                val_indptr,
                val_indices,
                val_data,
                val_labs,
            ) = prep_data(X_val, y_val_snap, "val")
        else:
            (
                val_num_ex,
                val_num_ft,
                val_num_nz,
                val_indptr,
                val_indices,
                val_data,
                val_labs,
            ) = (0, 0, 0, np.array([]), np.array([]), np.array([]), np.array([]))

        if not sample_weight is None:
            if type(sample_weight).__name__ != "ndarray":
                raise TypeError(
                    "Parameter sample_weight: invalid type. Supported type: ndarray."
                )
            sample_weight = sample_weight.astype(np.float32)
        else:
            sample_weight = np.array([], dtype=np.float32)

        if not sample_weight_val is None:
            if type(sample_weight_val).__name__ != "ndarray":
                raise TypeError(
                    "Parameter sample_weight_val: invalid type. Supported type: ndarray."
                )
            if X_val is None:
                raise ValueError(
                    "Parameter sample_weight_val not supported when X_val and y_val are not defined."
                )
            sample_weight_val = sample_weight_val.astype(np.float32)
        else:
            sample_weight_val = np.array([], dtype=np.float32)

        """
        if train_num_ft >= train_num_ex and self.params_['tree_params']['use_histograms']:
            print("Number of features is >= number of examples. Disabling histogram-based optimizations.")
            self.params_['tree_params']['use_histograms']=False
        """
        self.n_features_in_ = train_num_ft

        (
            self.model_,
            self.model_size_,
            self.feature_importances_,
            self.ensemble_size_,
            self.cache_id_,
        ) = libsnapml.booster_fit(
            self.params_["boosting_params"],
            self.params_["tree_params"],
            self.params_["ridge_params"],
            self.params_["kernel_params"],
            train_num_ex,
            train_num_ft,
            train_num_nz,
            train_indptr,
            train_indices,
            train_data,
            train_labs,
            val_num_ex,
            val_num_ft,
            val_num_nz,
            val_indptr,
            val_indices,
            val_data,
            val_labs,
            sample_weight,
            sample_weight_val,
            self.n_classes_,
            np.array(self.params_["tree_params"]["gpu_ids"]).astype(np.uint32),
            aggregate_importances,
        )

        return None

    def _predict(self, X, get_proba, num_threads):

        """
        Raw predictions

        If the training objective is 'mse' then it returns the predicted estimates.
        If the training objective is 'logloss' or 'cross_entropy' then it returns the predicted estimates
        before the logistic transformation (raw logits).

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting class estimates.

        get_proba : flag that indicates if output probabilities are to be computed
            0 : get raw predictions
            1 : get output probabilities (only for predict proba)

        num_threads : int
            Number of threads to use for prediction.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predicted estimates.
        """

        if num_threads is not None:
            _param_check(
                BoostingMachine.PARAMS["boosting_params"], "num_threads", num_threads
            )
        else:
            num_threads = self.params_["boosting_params"]["num_threads"]

        if type(X).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        if hasattr(self, "n_features_in_") and X.shape[1] != self.n_features_in_:
            raise ValueError(
                "Predict was passed %d features, but model was trained with %d features"
                % (X.shape[1], self.n_features_in_)
            )

        num_ex = X.shape[0]
        num_ft = X.shape[1]
        indptr = np.array([])
        indices = np.array([])
        data = np.ascontiguousarray(X, dtype=np.float32)  # enforce row-major format
        pred = []

        # Generate predictions
        pred, self.cache_id_ = libsnapml.booster_predict(
            num_ex,
            num_ft,
            num_threads,
            indptr,
            indices,
            data,
            self.model_,
            self.model_size_,
            get_proba,
            self.n_classes_,
            self.cache_id_,
        )

        # handle case of divergence
        if not np.all(np.isfinite(pred)):
            warnings.warn("Boosting diverged; Try using a smaller learning rate.")
            pred = np.nan_to_num(pred)

        if get_proba:
            if self.n_classes_ == 2:
                out = np.zeros((pred.shape[0], 2))
                out[:, 0] = 1 - pred
                out[:, 1] = pred
            else:
                out = pred.reshape(num_ex, self.n_classes_, order="F")
        else:

            if self.ind2class_ is not None:
                out = np.zeros_like(pred)
                out = out.astype(self.ind2class_[0].__class__)

                for i, c in self.ind2class_.items():
                    if self.n_classes_ == 2:
                        out[(pred > 0) == i] = c
                    else:
                        out[pred == i] = c
            else:
                out = pred

        return out

    def apply(self, X):
        """
        Map batch of examples to leaf indices and labels.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Batch of examples.

        Returns
        -------
        indices : array-like, shape = (n_samples, num_round) or (n_samples, num_round, num_classes)
            The leaf indices.
            Output is 2-dim if objective is 'mse', 'logloss' or 'cross_entropy'.
            Output is 3-dim if objective is 'softmax' (i.e., multiclass classification).


        labels : array-like, shape = (n_samples, num_round) or (n_samples, num_round, num_classes)
            The leaf labels.
            Output is 2-dim if objective is 'mse', 'logloss' or 'cross_entropy'.
            Output is 3-dim if objective is 'softmax' (i.e., multiclass classification).

        """

        if type(X).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        if hasattr(self, "n_features_in_") and X.shape[1] != self.n_features_in_:
            raise ValueError(
                "Predict was passed %d features, but model was trained with %d features"
                % (X.shape[1], self.n_features_in_)
            )

        return libsnapml.booster_apply(
            X.shape[0],
            X.shape[1],
            np.ascontiguousarray(X, dtype=np.float32),
            self.model_,
            self.model_size_,
            self.params_["boosting_params"]["num_threads"],
        )

    def predict(self, X, num_threads=None):

        """
        Raw predictions

        If the training objective is 'mse' then it returns the predicted estimates.
        If the training objective is 'logloss' or 'cross_entropy' then it returns the predicted estimates
        before the logistic transformation (raw logits).

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting class estimates.

        num_threads : int
            Number of threads to use for prediction.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predicted estimates.
        """

        if num_threads is not None:
            warnings.warn(
                'Setting num_threads as an argument to predict may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_param method before calling predict, e.g.: set_param({"boosting_params": {"num_threads": 4}})',
                FutureWarning,
            )

        return self._predict(X, 0, num_threads)

    def predict_proba(self, X, num_threads=None):

        """
        Output probabilities

        Use only if the training objective is 'logloss' (i.e., for binary classification tasks)
        or 'softmax' (i.e., for multiclass classification tasks).
        It returns the probabilities of each sample belonging to each class.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting class estimates.

        num_threads : int
            Number of threads to use for prediction.

        Returns
        -------
        proba: array-like, shape = (n_samples, n_classes)
            Returns the predicted probabilities of each sample belonging to each class.
        """

        if num_threads is not None:
            warnings.warn(
                'Setting num_threads as an argument to predict_proba may affect performance. It was deprecated in v1.8.0 and will be removed in v1.9.0. As a better alternative, please use the set_param method before calling predict_proba, e.g.: set_param({"boosting_params": {"num_threads": 4}})',
                FutureWarning,
            )

        return self._predict(X, 1, num_threads)

    def _compress_trees(self, X=None):

        """
        Compress decision trees for fast inference

        The binary decision tree ensemble created by training or by importing a pre-trained
        model is transformed into a more compact (compressed) format that enables higher inference
        performance and a smaller serialized model size.

        The transformation involves organizing the original binary decision trees into node clusters
        with specific interconnection structures based on expected node access characteristics. By
        exploiting the interconnection and node characteristics, the node clusters can be compressed
        within a minimum number of cache lines while also increasing spatial locality and, thus,
        cache performance.

        An input data set is optional and is used to predict node access characteristics for
        performing the node clustering. A maximum number (1000) of examples is used for this task.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Optional input dataset used for compressing trees

        """

        num_ex = 0
        num_ft = 0
        data = np.array([], dtype=np.float32)

        # Validate input data
        if X is not None:

            if type(X).__name__ != "ndarray":
                raise ValueError("X should be in ndarray format.")

            num_ex = X.shape[0]
            num_ft = X.shape[1]
            data = np.ascontiguousarray(X, dtype=np.float32)

        # Compress trees
        self.model_, self.model_size_, self.cache_id_ = libsnapml.booster_compress(
            num_ex, num_ft, data, self.model_, self.model_size_, self.cache_id_
        )

        return self

    def _convert_mbit(self, X=None):

        """
        Maxtrix based inference trees (MBIT) for inference using zDNN library

        The binary decision tree ensemble created by training or by importing a pre-trained
        model is transformed into a more proprietary MBIT format that enables accelerated inference
        using zAIU hardware.

        The transformation involves converting the original binary decision trees into matrices. In
        this way binary decision tree traversal is transformed into a series of matrix multiplications.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Optional input dataset used for mbi trees

        """

        num_ex = 0
        num_ft = 0
        data = np.array([], dtype=np.float32)

        # Validate input data
        if X is not None:

            if type(X).__name__ != "ndarray":
                raise ValueError("X should be in ndarray format.")

            num_ex = X.shape[0]
            num_ft = X.shape[1]
            data = np.ascontiguousarray(X, dtype=np.float32)

        # Convert trees to MBIT format
        self.model_, self.model_size_, self.cache_id_ = libsnapml.booster_convert_mbit(
            num_ex, num_ft, data, self.model_, self.model_size_, self.cache_id_
        )

        return self

    def optimize_trees(self, tree_format="compress_trees", X=None):

        """
        Optimize the trees in the ensemble for fast inference.

        Depending on the how the tree_format argument is set, this function will return a different
        optimized model format. This format determines which inference engine is used for subsequent
        calls to 'predict' or 'predict_proba'.

        If tree_format is set to 'compress_trees', the model will be optimized for execution on the CPU, using our
        compressed decision trees approach. Note: if this option is selected, an optional dataset X can be provided,
        which will be used to predict node access characteristics during node clustering.

        If tree_format is set to 'zdnn_tensors', the model will be optimized for execution on the IBM z16 AI accelerator,
        using a matrix-based inference algorithm leveraging the zDNN library.  Note: if this option is selected,
        the maximum batch size that can be scored by subsequent calls to 'predict' or 'predict_proba' will be 2^15 since
        this is the maximum tensor dimension supported by zDNN library.

        Parameters
        ----------

        tree_format : {'compress_trees', 'zdnn_tensors'}
            Tree format

        X : dense matrix (ndarray)
            Optional input dataset used for compressing trees

        Returns
        -------
        self : object
        """

        if tree_format == "compress_trees":
            # compress model
            self._compress_trees(X)
        elif tree_format == "zdnn_tensors":
            # convert to zdnn tensor format
            self._convert_mbit(X)
        else:
            raise ValueError(
                "tree_format parameter can take values 'compress_trees' or 'zdnn_tensors'"
            )

        return self

    def import_model(
        self, input_file, input_type, tree_format="compress_trees", X=None
    ):

        """
        Import a pre-trained boosted ensemble model and optimize the trees for fast inference.

        Supported import formats include PMML, ONNX, XGBoost json and lightGBM text. The
        corresponding input file types to be provided to the import_model function are
        'pmml', 'onnx', 'xgb_json', and 'lightgbm' respectively.

        Depending on the how the tree_format argument is set, this function will return a different
        optimized model format. This format determines which inference engine is used for subsequent
        calls to 'predict' or 'predict_proba'.

        If tree_format is set to 'compress_trees', the model will be optimized for execution on the CPU, using our
        compressed decision trees approach. Note: if this option is selected, an optional dataset X can be provided,
        which will be used to predict node access characteristics during node clustering.

        If tree_format is set to 'zdnn_tensors', the model will be optimized for execution on the IBM z16 AI accelerator,
        using a matrix-based inference algorithm leveraging the zDNN library.  Note: if this option is selected,
        the maximum batch size that can be scored by subsequent calls to 'predict' or 'predict_proba' will be 2^15 since
        this is the maximum tensor dimension supported by zDNN library.

        Note: If the input file contains features that are not supported by the import function, then an exception is thrown
        indicating the feature and the line number within the input file containing the feature.

        Parameters
        ----------
        input_file : str
            Input filename

        input_type : {'pmml', 'onnx', 'xgb_json', 'lightgbm'}
            Input file type

        tree_format : {'compress_trees', 'zdnn_tensors'}
            Tree format

        X : dense matrix (ndarray)
            Optional input dataset used for compressing trees

        Returns
        -------
        self : object
        """

        # import model
        self._import_model(input_file, input_type)

        # optimize trees
        self.optimize_trees(tree_format, X)

        return self
