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


class DensePartition:

    """
    Data partition in dense format used for distributed snapml training and inference.

    Parameters
    ----------
    ptr : str
        String representation of the value of the pointer to where the partition resides in memory.
    """

    def __init__(self, ptr):
        self.ptr_ = ptr
        self.type_ = 0


class SparsePartition:

    """
    Data partition in sparse format used for distributed snapml training and inference.

    Parameters
    ----------
    ptr : str
        String representation of the value of the pointer to where the partition resides in memory.
    """

    def __init__(self, ptr):
        self.ptr_ = ptr
        self.type_ = 1


class ConstantValueSparsePartition:

    """
    Data partition in compressed snap format used for distributed snapml training and inference.
    This format is useful for sparse datasets where all the non-zero values are equal to the same value.

    Parameters
    ----------
    ptr : str
        String representation of the value of the pointer to where the partition resides in memory.
    """

    def __init__(self, ptr):
        self.ptr_ = ptr
        self.type_ = 2
