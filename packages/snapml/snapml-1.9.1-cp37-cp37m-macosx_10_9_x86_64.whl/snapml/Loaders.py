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

## @file
# @ingroup pythonutils

import sys
import struct

from snapml.utils import _is_mpi_enabled

_mpi_enabled = _is_mpi_enabled()

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(_mpi_enabled)

from snapml.Partition import (
    SparsePartition,
    DensePartition,
    ConstantValueSparsePartition,
)


def load_from_svmlight_format(filename, num_ft=None, num_chunks=None):
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
    data partition : snapml.Partition.SparsePartition
        Returns a data partition in sparse format which will be used for
        distributed snapml training and inference.

    """
    if num_ft == None:
        num_ft = 1

    if num_chunks == None:
        num_chunks = 1

    ptr = libsnapml.load_from_svmlight_format(filename, num_ft, num_chunks)
    return SparsePartition(ptr)


def load_from_snap_format(filename, num_chunks=None):
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
    data partition : snapml.Partition
        Returns a data partition in sparse, dense or compressed sparse
        format which will be used for distributed snapml training and
        inference. The type of data format (sparse, dense, compressed) is
        automatically detected from the input file header. To dump data in
        snap format, one should use the dump_to_snap_format function
        from snapml.Utils.
    """
    if num_chunks == None:
        num_chunks = 1

    # read data type from file
    with open(filename, "rb") as f:
        data_type = struct.unpack("I", f.read(4))[0]
    if data_type == 0:
        ptr = libsnapml.load_from_dense_snap_format(filename, 1, num_chunks)
        return DensePartition(ptr)
    elif data_type == 1:
        ptr = libsnapml.load_from_sparse_snap_format(filename, 1, num_chunks)
        return SparsePartition(ptr)
    elif data_type == 2:
        ptr = libsnapml.load_from_l2sparse_snap_format(filename, 1, num_chunks)
        return ConstantValueSparsePartition(ptr)
    else:
        raise ("Unrecognized data type in snap format.")
