# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2018, 2019. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# *****************************************************************

## @file
# @ingroup pythonutils

import sys
from snapml._import import import_libsnapml

libsnapmlmpi = import_libsnapml(True)


def Comm_get_info():
    """
    Function for extracting the MPI communicator size and the rank ID.

    Returns
    -------
    (comm_size, rank_id) : (int, int)
        Returns the MPI communicator size and the rank ID of the calling
        MPI process.
    """
    (comm_size, rank) = libsnapmlmpi.MPI_get_info()
    return (comm_size, rank)
