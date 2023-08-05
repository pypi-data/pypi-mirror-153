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

from snapml.utils import _is_mpi_enabled

_mpi_enabled = _is_mpi_enabled()

from snapml.GeneralizedLinearModel import GeneralizedLinearModel

## @ingroup pythonclasses
class GeneralizedLinearModelRegressor(GeneralizedLinearModel):
    def set_classes(self, y_train):
        pass

    def check_and_modify_labels(self, y_train):
        return y_train.astype(np.float32)

    def post_training(self, training_metadata, X_train, _mpi_enabled):
        pass

    def post_predict(self, pred):
        return pred

    def set_intercept(self):
        if self.fit_intercept == True:
            self.intercept_ = self.model_[0, -1]
        else:
            self.intercept_ = 0.0
