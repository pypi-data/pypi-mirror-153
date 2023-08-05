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

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(False)

from abc import ABC, abstractmethod

from snapml.CommonModel import CommonModel

## @ingroup pythonclasses
class DecisionTree(CommonModel):
    @abstractmethod
    def __init__(self):
        # just for reference
        self.criterion = None
        self.splitter = None
        self.max_depth = None
        self.min_samples_leaf = None
        self.max_features = None
        self.random_state = None
        self.n_jobs = None
        self.use_histograms = None
        self.hist_nbins = None
        self.use_gpu = None
        self.gpu_id = None
        self.verbose = None
        self.task_type_ = None
        self.params = None
        self.n_features_in_ = None

    def check_gpu(self):
        pass

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

        # Run model training
        return libsnapml.dtc_fit(
            self.task_type_,
            self.criterion,
            max_depth,
            min_samples_leaf,
            max_features,
            random_state,
            self.verbose,
            self.n_jobs,
            self.use_histograms,
            self.hist_nbins,
            self.use_gpu,
            self.gpu_id,
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

    def c_predict(
        self, num_ex, num_ft, indptr, indices, data, n_jobs, proba, num_classes
    ):

        # Generate predictions
        return libsnapml.dtc_predict(
            num_ex,
            num_ft,
            indptr,
            indices,
            data,
            self.model_,
            self.model_size_,
            n_jobs,
            proba,
            num_classes,
        )
