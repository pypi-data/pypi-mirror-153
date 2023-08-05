# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2019. All Rights Reserved.
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

if _mpi_enabled:
    libsnapmlmpi = import_libsnapml(True)


def write_to_snap_format(filename, data, with_implicit_vals=False):
    """
    Write dataset to binary snap format.
    This method is implemented in a distributed manner using MPI.

    Parameters
    ----------
    filename: str
        Output file

    data: snapml.Partition
        Dataset to write

    with_implicit_vals: bool
        Write sparse data without values (assumed every row is constant and L2-normalized).

    """

    if _mpi_enabled:
        libsnapmlmpi.write_to_snap_format(
            filename, data.ptr_, data.type_, with_implicit_vals
        )
    else:
        raise TypeError("Function only supported for MPI execution.")
