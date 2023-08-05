# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2018, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# *****************************************************************
from __future__ import print_function

import numpy as np
from numba import cuda


def _to_device(x):
    return cuda.to_device(x)


def _cuda_synchronize():
    cuda.synchronize()


def _create_device_array(in_cuDF):
    return cuda.device_array(in_cuDF.shape, dtype=np.float32, order="C")


# CUDA kernel to convert label
@cuda.jit
def _convert_labs(dev_arry):
    rw, cl = cuda.grid(2)
    if rw < dev_arry.shape[0] and cl < dev_arry.shape[1]:
        dev_arry[rw, cl] = 2 * dev_arry[rw, cl] - 1


@cuda.jit
def _copy_DeviceNDArray(in_dndA_F, out_dndA_C):
    """
    CUDA Kernel to copy a F contiguous deviceNDArray into
    a C contiguous deviceNDArray
    """
    x, y = cuda.grid(2)
    if x < in_dndA_F.shape[0] and y < in_dndA_F.shape[1]:
        out_dndA_C[x][y] = in_dndA_F[x][y]
