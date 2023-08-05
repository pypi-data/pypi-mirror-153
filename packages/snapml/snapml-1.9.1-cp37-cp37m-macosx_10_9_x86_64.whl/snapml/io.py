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

## @file
# @ingroup pythonutils

import sys
import os
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
import struct
import math

from snapml.Loaders import *
from snapml.Writers import *

from snapml.utils import _is_mpi_enabled, read_from_snap_format

_mpi_enabled = _is_mpi_enabled()

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(_mpi_enabled)


def load_svmlight_file(filename, num_ft=None, num_chunks=None):
    """
    Data loading from svmlight format file.
    It supports both local and distributed(MPI) method of loading data.
    For MPI execution this can be used for distributed SnapML training and inference.

    Parameters
    ----------
    filename : str
        The file where the data resides.

    num_ft : int
        Expected number of features

    num_chunks : int
        Number of chunks per partition

    Returns
    -------
    X : scipy.sparse matrix of shape (n_samples, n_features)
    y : ndarray of shape (n_samples,)
    """
    if num_ft == None:
        num_ft = 1  # default value

    if num_chunks == None:
        num_chunks = 1

    data = libsnapml.load_svmlight_file(filename, num_ft, num_chunks)

    num_ex = data[0][0]
    num_ft = data[0][1]
    val = data[1]
    indices = data[2]
    indptr = data[3]
    y = data[4]

    X = csr_matrix((val, indices, indptr), shape=(num_ex, num_ft))
    return X, y


def load_snap_file(filename, num_chunks=None):
    """
    Data loading from Snap formatted data file.
    It supports both local and distributed(MPI) method of loading data.
    For MPI execution this can be used for distributed SnapML training and inference.

    Parameters
    ----------
    filename : str
        The file where the data resides in snap format.

    num_chunks : int
        Number of chunks per partition

    Returns
    -------
    X : scipy.sparse matrix or ndarray of shape (n_samples, n_features)
    y : ndarray of shape (n_samples,)
    """
    if not _mpi_enabled:
        # load for snap-ml-local
        X, y = read_from_snap_format(filename)
    else:

        if num_chunks == None:
            num_chunks = 1

        # load for snap-ml-mpi in a distributed manner
        with open(filename, "rb") as f:
            data_type = struct.unpack("I", f.read(4))[0]
            col_major = struct.unpack("?", f.read(1))[0]

        if data_type == 0:
            data = libsnapml.load_dense_snap_file(filename, 1, num_chunks)
        elif data_type == 1:
            data = libsnapml.load_sparse_snap_file(filename, 1, num_chunks)
        elif data_type == 2:
            raise ("l2sparse snap format is not supported.")
        else:
            raise ("Unrecognized data type in snap format.")

        num_ex = data[0][0]
        num_ft = data[0][1]
        val = data[1]
        indices = data[2]
        indptr = data[3]
        y = data[4]

        # Dense Format
        if data_type == 0:
            X = val
        else:  # Sparse Format
            if col_major:
                X = csc_matrix((val, indices, indptr), shape=(num_ex, num_ft))
            else:
                X = csr_matrix((val, indices, indptr), shape=(num_ex, num_ft))

    return X, y


def copy_as_gpu_cmatrix(in_cuDF):
    """
    Create a C contiguous deviceNDArray from the input cuDF.

    Parameters
    ----------
    in_cuDF : cuDF
        Input cuDF dataframe

    Returns
    -------
    dndA_C : DeviceNDArray
        C contiguous deviceNDArray created from the input cuDF.
    """

    # Check if the data-types of data in_cuDF are all float32
    if (len(in_cuDF.dtypes.unique()) != 1) or (
        np.dtype("float32") not in in_cuDF.dtypes.unique()
    ):
        raise TypeError(
            "snapML only supports float32 dtype. Found dtypes : {}.".format(
                in_cuDF.dtypes
            )
        )

    from snap_ml.utils_gpu import (
        _create_device_array,
        _copy_DeviceNDArray,
        _cuda_synchronize,
    )

    # Create a C contiguous deviceNDArray of same shape as input cuDF
    da_C = _create_device_array(in_cuDF)

    threadsperblock = (32, 32)
    blockspergrid_x = math.ceil(in_cuDF.shape[0] / threadsperblock[0])
    blockspergrid_y = math.ceil(in_cuDF.shape[1] / threadsperblock[1])
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    _copy_DeviceNDArray[blockspergrid, threadsperblock](in_cuDF.as_gpu_matrix(), da_C)
    _cuda_synchronize()

    return da_C
