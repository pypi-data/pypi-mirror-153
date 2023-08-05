# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2019, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************
from .version import __version__

import ctypes
import os

if os.name != "nt":
    from ctypes.util import find_library

    lib_name = find_library("mpi")
    ctypes.CDLL(lib_name, mode=ctypes.RTLD_GLOBAL)

mpi_vars = {"OMPI_COMM_WORLD_LOCAL_RANK": 0}
mpi_init_status = True

# Ensure all the necessary ENV variables are available;
# else don't initialize SnapML & restrict SnapML API invocations.
for var in mpi_vars:
    val = os.getenv(var)
    if val is None:
        mpi_init_status = False
        break
    mpi_vars[var] = val

if mpi_init_status:
    val = os.getenv("DLI_SNAPML_MPI")
    if val:
        rank_local = mpi_vars["OMPI_COMM_WORLD_LOCAL_RANK"]
        os.environ["CUDA_VISIBLE_DEVICES"] = rank_local

# Local code
from snapml.LogisticRegression import LogisticRegression
from snapml.LinearRegression import LinearRegression
from snapml.SupportVectorMachine import SupportVectorMachine
from snapml.DecisionTreeClassifier import DecisionTreeClassifier
from snapml.DecisionTreeRegressor import DecisionTreeRegressor
from snapml.RandomForestClassifier import RandomForestClassifier
from snapml.RandomForestRegressor import RandomForestRegressor
from snapml.BoostingMachine import BoostingMachine
from snapml.BoostingMachineClassifier import BoostingMachineClassifier
from snapml.BoostingMachineRegressor import BoostingMachineRegressor
from snapml.RBFSampler import RBFSampler
from snapml.MultiOutputCalibratedClassifier import MultiOutputCalibratedClassifier

# expose prefix classes for Lale/AutoAI
class SnapDecisionTreeRegressor(DecisionTreeRegressor):
    pass


class SnapDecisionTreeClassifier(DecisionTreeClassifier):
    pass


class SnapRandomForestRegressor(RandomForestRegressor):
    pass


class SnapRandomForestClassifier(RandomForestClassifier):
    pass


class SnapBoostingMachineRegressor(BoostingMachineRegressor):
    pass


class SnapBoostingMachineClassifier(BoostingMachineClassifier):
    pass


class SnapLogisticRegression(LogisticRegression):
    pass


class SnapSVMClassifier(SupportVectorMachine):
    pass


from snapml.BatchedTreeEnsemble import (
    BatchedTreeEnsembleClassifier,
    BatchedTreeEnsembleRegressor,
)

if mpi_init_status:
    # This is only specific to mpi and n/a for local
    from snapml.utils import read_from_snap_format, dump_to_snap_format
else:
    # This is only specific to local
    from snapml.utils import get_gpu_count
    from snapml import io
