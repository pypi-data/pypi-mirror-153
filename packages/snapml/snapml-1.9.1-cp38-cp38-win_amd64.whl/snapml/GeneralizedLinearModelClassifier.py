# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np
import math

from snapml.utils import _is_mpi_enabled, _is_data_snapml_partition_type

_mpi_enabled = _is_mpi_enabled()

from snapml.GeneralizedLinearModel import GeneralizedLinearModel

## @ingroup pythonclasses
class GeneralizedLinearModelClassifier(GeneralizedLinearModel):
    def set_classes(self, y_train):
        if _mpi_enabled or y_train is None:
            self.classes_ = None
        else:
            self.classes_ = np.unique(y_train)

    def set_intercept(self):
        if self.fit_intercept == True:
            self.intercept_ = np.asarray([self.model_[:, -1]]).reshape(
                self.model_.shape[0],
            )
        else:
            self.intercept_ = 0.0

    def get_num_classes(self):
        if self.classes_ is not None:
            return len(self.classes_)
        else:
            assert self.classes_post_ is not None
            return len(self.classes_post_)

    def check_and_modify_labels(self, y_train):

        if _mpi_enabled:
            return y_train.astype(np.float32)

        if len(self.classes_) == 1:
            raise ValueError(
                "There must be at least two unique label values in the training data"
            )

        labs = np.zeros_like(y_train, dtype=np.float32)

        # replace class with their enumeration
        for i, c in enumerate(self.classes_):
            labs[y_train == c] = i

        return labs

    def post_training(self, training_metadata, X_train, _mpi_enabled):

        if _is_data_snapml_partition_type(X_train) or _mpi_enabled:
            self.classes_post_ = np.array(training_metadata["uniq_labs"])
            self.labels_flag_ = int(training_metadata["labs_converted"])

    def post_predict(self, pred):

        # if the unique classes could be detected before calling fit
        # then we always replace the class labels with an enumeration
        # so we need to treat this case differently

        if self.classes_ is not None:

            if len(self.classes_) == 2:
                pred_ind = (pred + 1) / 2
            else:
                pred_ind = np.argmax(pred, axis=0)

            pred_out = np.zeros_like(pred_ind)
            pred_out = pred_out.astype(self.classes_[0].__class__)

            for i, c in enumerate(self.classes_):
                pred_out[pred_ind == i] = c

        else:

            if len(self.classes_post_) == 2:
                if self.labels_flag:
                    pred_out = (pred + 1) / 2
                else:
                    pred_out = pred
            else:

                pred_ind = np.argmax(pred, axis=0)
                pred_out = np.zeros_like(pred_ind)
                pred_out = pred_out.astype(self.classes_post_[0].__class__)
                for i, c in enumerate(self.classes_post_):
                    pred_out[pred_ind == i] = c

        return pred_out
