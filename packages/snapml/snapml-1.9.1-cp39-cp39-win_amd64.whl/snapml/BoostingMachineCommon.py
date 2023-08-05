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

from sklearn.base import BaseEstimator
from snapml import BoostingMachine

## @ingroup pythonclasses
class BoostingMachineCommon(BaseEstimator):
    """! This class implements common parts of the regressor and the classifier."""

    ## Documentation of the method
    #  @brief This method converts a parameter list
    def make_boosting_params(self):
        params = {
            "boosting_params": {
                "num_threads": self.n_jobs,
                "num_round": self.num_round,
                "objective": self.objective,
                "min_max_depth": self.min_max_depth
                if self.max_depth is None
                else self.max_depth,
                "max_max_depth": self.max_max_depth
                if self.max_depth is None
                else self.max_depth,
                "early_stopping_rounds": self.early_stopping_rounds,
                "random_state": self.random_state,
                "base_score": self.base_score,
                "learning_rate": self.learning_rate,
                "verbose": self.verbose,
                "compress_trees": self.compress_trees,
            },
            "tree_params": {
                "use_histograms": self.use_histograms,
                "hist_nbins": self.hist_nbins,
                "use_gpu": self.use_gpu,
                "gpu_ids": self.gpu_ids if hasattr(self, "gpu_ids") else [self.gpu_id],
                "colsample_bytree": self.colsample_bytree,
                "subsample": self.subsample,
                "lambda_l2": self.lambda_l2,
                "select_probability": self.tree_select_probability,
            },
            "ridge_params": {
                "regularizer": self.regularizer,
                "fit_intercept": self.fit_intercept,
            },
            "kernel_params": {
                "gamma": self.gamma,
                "n_components": self.n_components,
            },
        }
        return params

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
        """
        If self.booster_ has not been created a parameter check is performed
        when fit() is called and self.booster_ is created.
        If self.booster_ exists a parameter change is happening after the fit()
        call and therefore a paramter check is required.
        """
        if hasattr(self, "booster_"):
            try:
                self.booster_.set_param(self.make_boosting_params())
            except:
                super().set_params(**params_copy)
                raise

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

        self.booster_.optimize_trees(tree_format, X)

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

        self.booster_ = BoostingMachine(self.make_boosting_params())

        self.booster_.import_model(input_file, input_type, tree_format, X)

        return self

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

        # export model
        self.booster_.export_model(output_file, output_type)
