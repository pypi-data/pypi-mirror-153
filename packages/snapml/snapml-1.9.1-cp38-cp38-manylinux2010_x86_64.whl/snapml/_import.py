# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2021. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************
from importlib import import_module
import warnings
import os
from ctypes import CDLL
import platform

try:
    from numpy.core._multiarray_umath import __cpu_features__ as cpu_features
except:
    warnings.warn(
        "Cannot detect CPU features info from numpy; AVX2 will not be used.",
        category=UserWarning,
    )
    cpu_features = None


def import_libutils():
    if cpu_features is not None and cpu_features["AVX2"]:
        return import_module("snapml.libsnapmlutils_avx2")
    else:
        return import_module("snapml.libsnapmlutils")


def import_libsnapml(mpi_enabled=False):

    if platform.machine() == "s390x":
        CDLL(os.path.join(os.path.dirname(__file__), "libzdnninternal.so"))

    if cpu_features is not None and cpu_features["AVX2"]:
        if mpi_enabled:
            return import_module("snapml.libsnapmlmpi3_avx2")
        else:
            return import_module("snapml.libsnapmllocal3_avx2")
    else:
        if mpi_enabled:
            return import_module("snapml.libsnapmlmpi3")
        else:
            return import_module("snapml.libsnapmllocal3")
