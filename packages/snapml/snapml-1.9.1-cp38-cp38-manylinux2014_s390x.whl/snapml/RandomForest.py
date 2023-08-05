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
import math

from snapml._import import import_libsnapml

from .version import __version__

libsnapml = import_libsnapml(False)

from abc import ABC, abstractmethod

from snapml.CommonModel import CommonModel

## @ingroup pythonclasses
class RandomForest(CommonModel):
    @abstractmethod
    def __init__(self):
        # just for reference
        self.n_estimators = None
        self.criterion = None
        self.max_depth = None
        self.min_samples_leaf = None
        self.max_features = None
        self.bootstrap = None
        self.n_jobs = None
        self.random_state = None
        self.verbose = None
        self.use_histograms = None
        self.hist_nbins = None
        self.use_gpu = None
        self.gpu_ids = None
        self.task_type_ = None
        self.params = None
        self.n_features_in_ = None
        self.compress_trees = None
        self.n_classes_ = None

    def __setstate__(self, d):

        # if the model was trained, let's rebuild the cache
        if "model_size_" in d.keys() and d["model_size_"] > 0:
            d["cache_id_"] = libsnapml.rfc_cache(d["model_"], d["model_size_"])
        else:
            d["cache_id_"] = 0

        self.__dict__ = d

    def __del__(self):
        # if the forest was cached, let's ensure that it gets destroyed in C++
        if hasattr(self, "cache_id_") and self.cache_id_ > 0:
            libsnapml.rfc_delete(self.cache_id_)

    def check_gpu(self):
        if (self.use_gpu == True) and (self.max_depth is None or self.max_depth > 16):
            print(
                "GPU acceleration only supported for bounded max_depth <= 16; forest will be built with max_depth=16"
            )
            self.max_depth = 16

        self.gpu_ids = np.array(self.gpu_ids).astype(np.uint32)
        if self.use_gpu and len(self.gpu_ids) == 0:
            raise ValueError("Please provide at least one gpu_id.")

        for gpu_id in self.gpu_ids:
            if gpu_id < 0:
                raise ValueError("Invalid gpu_id")

    def c_fit(
        self,
        max_depth,
        min_samples_leaf,
        max_features,
        random_state,
        num_ex,
        num_ft,
        num_nz,
        indptr,
        indices,
        data,
        labs,
        num_classes,
        sample_weight,
    ):

        model, model_size, feature_importances, self.cache_id_ = libsnapml.rfc_fit(
            self.task_type_,
            self.n_estimators,
            self.criterion,
            max_depth,
            min_samples_leaf,
            max_features,
            self.bootstrap,
            self.n_jobs,
            random_state,
            self.verbose,
            self.use_histograms,
            self.hist_nbins,
            self.use_gpu,
            self.gpu_ids,
            self.compress_trees,
            num_ex,
            num_ft,
            num_nz,
            num_classes,
            indptr,
            indices,
            data,
            labs,
            sample_weight,
        )

        return model, model_size, feature_importances

    def c_predict(
        self, num_ex, num_ft, indptr, indices, data, n_jobs, proba, num_classes
    ):

        # Generate predictions
        pred, self.cache_id_ = libsnapml.rfc_predict(
            num_ex,
            num_ft,
            n_jobs,
            indptr,
            indices,
            data,
            self.model_,
            self.model_size_,
            proba,
            num_classes,
            self.cache_id_,
        )

        return pred

    def _import_model(self, input_file, type):

        """
        Import a pre-trained forest ensemble from the given input file of the given type.

        Supported import format is (sklearn) PMML and ONNX. The corresponding input file type to be
        provided to the import_model function is 'pmml' or 'onnx' respectively.

        If the input file contains features that are not supported by the import function
        then a runtime error is thrown indicating the feature and the line number within
        the input file containing the feature.

        Parameters
        ----------
        input_file : str
            Input filename

        type : {'pmml', 'onnx'}
            Input file type

        Returns
        -------
        self : object
        """

        if (not isinstance(input_file, (str))) or (input_file == ""):
            raise Exception("Input file name not provided.")

        if (not isinstance(type, (str))) or (type == ""):
            raise Exception("Input file type not provided.")

        (
            self.model_,
            self.model_size_,
            self.classes_,
            self.n_classes_,
        ) = libsnapml.rfc_import(input_file, type, self.task_type_)

        if self.classes_ is not None:
            self.ind2class_ = {}
            for i, c in enumerate(self.classes_):
                self.ind2class_[i] = c

        return self

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
        performing the node clustering. A maximum number (Lmax) of examples is used for this task.

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
        self.model_, self.model_size_, self.cache_id_ = libsnapml.rfc_compress(
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

        # Convert trees
        self.model_, self.model_size_, self.cache_id_ = libsnapml.rfc_convert_mbit(
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
            Dataset used for compressing trees

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
        Import a pre-trained forest ensemble model and optimize the trees for fast inference.

        Supported import formats include PMML, ONNX. The corresponding input file types to be provided to the
        import_model function are 'pmml' and 'onnx' respectively.

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

        input_type : {'pmml', 'onnx'}
            Input file type

        tree_format : {'compress_trees', 'zdnn_tensors'}
            Tree format

        X : dense matrix (ndarray)
            Dataset used for compressing trees

        Returns
        -------
        self : object
        """

        # import model
        self._import_model(input_file, input_type)

        # optimize trees
        self.optimize_trees(tree_format, X)

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

        if (not isinstance(output_file, (str))) or (output_file == ""):
            raise Exception("Output file name not provided.")

        if (not isinstance(output_type, (str))) or (output_type == ""):
            raise Exception("Output file type not provided.")

        if hasattr(self, "classes_"):
            if not np.can_cast(self.classes_, np.float64):
                raise Exception("Cannot cast class labels to float for export.")
            classes = self.classes_.astype(np.float64)
        else:
            classes = np.array([], dtype=np.float64)

        libsnapml.rfc_export(
            output_file,
            output_type,
            self.model_,
            self.model_size_,
            self.cache_id_,
            classes,
            __version__,
        )
