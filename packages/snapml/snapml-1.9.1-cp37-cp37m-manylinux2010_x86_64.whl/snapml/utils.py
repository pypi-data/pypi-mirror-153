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

from __future__ import print_function

import sys
import struct
import numbers
import numpy as np
from scipy import sparse, stats
import os
from snapml._import import import_libutils, import_libsnapml

libutils = import_libutils()
libsnapml = import_libsnapml(False)

# Return predefined config information & enterprise_license checks
#        predefined ERROR messages
#        predefined INFO messages
def get_config():
    return (
        libutils.max_nodes_base,
        libutils.max_gpus_base,
        libutils.check_enterprise_license(),
        libutils.nodes_errmsg,
        libutils.gpus_errmsg,
        libutils.processes_errmsg,
        libutils.nodes_infomsg,
        libutils.gpus_infomsg,
        libutils.processes_infomsg,
    )


# Returns:  0, if enterprise_license exist
#          -1, if enterprise_license doesn't exist
def check_enterprise_license():
    return libutils.check_enterprise_license()


def get_gpu_count():
    return libsnapml.get_gpu_count()


def read_from_snap_format(filename):
    with open(filename, "rb") as f:

        data_type = struct.unpack("I", f.read(4))[0]

        if data_type == 0:
            # dense data
            # print("Reading dense data from snap format")
            col_major = struct.unpack("?", f.read(1))[0]
            num_ex = struct.unpack("I", f.read(4))[0]
            num_ft = struct.unpack("I", f.read(4))[0]
            y = np.frombuffer(f.read(4 * num_ex), dtype=np.float32)
            X = np.frombuffer(f.read(4 * num_ex * num_ft), dtype=np.float32)

            if col_major:
                X.shape = (num_ft, num_ex)
                X = X.T.copy()
            else:
                X.shape = (num_ex, num_ft)

            return X, y

        elif data_type == 1:
            # sparse data
            # print("Reading sparse data from snap format")
            col_major = struct.unpack("?", f.read(1))[0]
            num_ex = struct.unpack("I", f.read(4))[0]
            num_ft = struct.unpack("I", f.read(4))[0]

            if col_major:
                count = np.frombuffer(f.read(4 * num_ft), dtype=np.uint32)
            else:
                count = np.frombuffer(f.read(4 * num_ex), dtype=np.uint32)

            num_nz = np.sum(count)
            indptr = np.cumsum(np.insert(count, 0, 0))
            num_bytes = 4 * num_nz
            y = np.frombuffer(f.read(4 * num_ex), dtype=np.float32)
            ind = np.frombuffer(f.read(num_bytes.astype(np.uint64)), dtype=np.uint32)
            val = np.frombuffer(f.read(num_bytes.astype(np.uint64)), dtype=np.float32)

            if col_major:
                X = sparse.csc.csc_matrix((val, ind, indptr), shape=(num_ex, num_ft))
            else:
                X = sparse.csr.csr_matrix((val, ind, indptr), shape=(num_ex, num_ft))

            return X, y

        elif data_type == 2:
            # l2-sparse data
            raise Exception(
                "Sparse data with implicit values not supported by numpy/scipy"
            )
        else:
            # not recognized
            raise Exception("Unrecognized data type")


def dump_to_snap_format(X, y, filename, col_major=False, implicit_vals=False):

    num_ex = X.shape[0]
    num_ft = X.shape[1]
    assert y.shape[0] == num_ex

    assert type(y) is np.ndarray
    y = y.astype(np.float32)

    if type(X) is np.ndarray:
        # print("Writing Dense dataset to snap format")

        # set order
        if col_major:
            X = np.asfortranarray(X, dtype=np.float32)
        else:
            X = np.ascontiguousarray(X, dtype=np.float32)

        with open(filename, "wb") as f:
            f.write(struct.pack("I", 0))
            f.write(struct.pack("?", col_major))
            f.write(struct.pack("I", num_ex))
            f.write(struct.pack("I", num_ft))
            f.write(y.data)
            if col_major:
                for ft in range(0, num_ft):
                    f.write(X[:, ft])
            else:
                f.write(X.data)

    elif type(X) is sparse.csr.csr_matrix:

        # print("Writing Sparse dataset to snap format")
        if col_major:
            X = X.tocsc()

        ind = X.indices.astype(np.uint32)
        val = X.data.astype(np.float32)
        count = np.diff(X.indptr).astype(np.uint32)

        with open(filename, "wb") as f:
            if implicit_vals:
                f.write(struct.pack("I", 2))
            else:
                f.write(struct.pack("I", 1))
            f.write(struct.pack("?", col_major))
            f.write(struct.pack("I", num_ex))
            f.write(struct.pack("I", num_ft))
            f.write(count.data)
            f.write(y.data)
            f.write(ind.data)

            if not implicit_vals:
                f.write(val.data)
    else:
        print("Unrecognized type; cannot write to snap format")


"""


num_ex = 10
num_ft = 30
import numpy as np
X = np.random.rand(num_ex,num_ft)
y = np.random.rand(num_ex)


X = sparse.random(num_ex, num_ft, 0.1, format='csr', data_rvs=stats.uniform(0,1).rvs)

print(X)
Y = X.tocsc()
print(Y.indptr)
print(Y.indices)

dump_to_snap_format(X,y,"test.snap", col_major=True)

X_chk, y_chk = read_from_snap_format("test.snap")

print(X)
"""


def _is_mpi_enabled():
    val = os.getenv("OMPI_COMM_WORLD_LOCAL_RANK")
    if val is None:
        return False
    else:
        return True


def _is_data_snapml_partition_type(X):
    if X.__class__.__name__ in [
        "SparsePartition",
        "DensePartition",
        "ConstantValueSparsePartition",
    ]:
        return True
    return False


# Verify if the objective to be solved is compatible with the input data-type
def _verify_compat_obj_dtype(is_dual, dtype):
    if (is_dual == False) and (dtype == "csr_matrix"):
        raise ValueError("Primal objective can only be solved with col-major data.")
    if (is_dual == True) and (dtype == "csc_matrix"):
        raise ValueError("Dual objective can only be solved with row-major data.")
    return True


# Predict can only be performed with row-major data
def _verify_inference_dtype(dtype):
    if dtype == "csc_matrix":
        raise ValueError("Inference can only be performed with row-major data.")
    return True


# Checks if the data-type and parameters used for DeviceNDArray are supported
def _check_devicendarray_types(X, y, self):
    DEVICE_NDARRAY_MSG = "For DeviceNDArray as input"

    if type(X).__name__ == "DeviceNDArray" or type(y).__name__ == "DeviceNDArray":
        if (type(X).__name__ != "DeviceNDArray") or (
            type(y).__name__ != "DeviceNDArray"
        ):
            raise TypeError(
                DEVICE_NDARRAY_MSG + ", X_train and y_train should be of same types"
            )
        if X.dtype != "float32" or y.dtype != "float32":
            raise TypeError(
                DEVICE_NDARRAY_MSG + ", only float32 data type is supported"
            )
        if len(self.device_ids) > 1:
            raise ValueError(
                DEVICE_NDARRAY_MSG + ", training on multiple GPUs is not supported"
            )
        if len(self.device_ids) == 1 and self.device_ids[0] != 0:
            raise ValueError(
                DEVICE_NDARRAY_MSG + ", training on GPU id 0 is only supported"
            )
        if self.use_gpu == False:
            raise ValueError(DEVICE_NDARRAY_MSG + ", use_gpu true is mandatory option")
        if _is_mpi_enabled():
            raise ValueError(DEVICE_NDARRAY_MSG + ", MPI support is not provided")
        if self.generate_training_history is not None:
            raise ValueError(DEVICE_NDARRAY_MSG + ", training_history is not supported")
        if hasattr(self, "is_regression") and self.is_regression == True:
            return True
        if len(self.classes_) > 2:
            raise ValueError(
                DEVICE_NDARRAY_MSG + ", multi-class labels are not supported"
            )
    return True


# Provides parameter checking for the learning methods
def _param_print(param):
    paramstr = ""
    for attr in param["attr"]:
        if len(paramstr) > 1:
            paramstr += " or"
        if "values" in attr:
            paramstr += " in {}".format(attr["values"])
        elif "type" in attr:
            paramstr += " (type {:s}".format(attr["type"])
            if attr.get("gt") is not None:
                paramstr += ", > {}".format(attr["gt"])
            if attr.get("ge") is not None:
                paramstr += ", >= {}".format(attr["ge"])
            if attr.get("lt") is not None:
                paramstr += ", < {}".format(attr["lt"])
            if attr.get("le") is not None:
                paramstr += ", <= {}".format(attr["le"])
            paramstr += ")"
    return paramstr


def _type_matches(dest_type, value):
    if dest_type == type(value):
        return True
    if dest_type == list and type(value) == np.ndarray:
        return True
    if issubclass(dest_type, numbers.Number) and isinstance(value, numbers.Number):
        if issubclass(dest_type, numbers.Integral):
            if isinstance(value, numbers.Integral):
                return True
        elif issubclass(dest_type, numbers.Rational):
            if isinstance(value, numbers.Rational):
                return True
        elif issubclass(dest_type, numbers.Real):
            if isinstance(value, numbers.Real):
                return True
        else:
            return True
    return False


def _param_check(param_def, varname, value):
    allowed_types = ("bool", "int", "float", "str", "list", "tuple", "set", "dict")

    param = next((p for p in param_def if p["name"] == varname), None)

    if param is None:
        print("[Warning] Unknown parameter '{:s}' specified.".format(varname))
        return

    for attr in param["attr"]:
        if "values" in attr:
            if value not in attr["values"]:
                continue
            return
        elif "type" in attr:
            typestr = attr["type"]
            if typestr not in allowed_types:
                raise TypeError("Unknown type specified: {:s}.".format(typestr))

            if not _type_matches(eval(typestr), value):
                continue
            if attr.get("gt") is not None and value <= attr["gt"]:
                raise ValueError(
                    "Error: '{:s}' should be larger than {}.".format(
                        varname, attr["gt"]
                    )
                )
            if attr.get("ge") is not None and value < attr["ge"]:
                raise ValueError(
                    "Error: '{:s}' should be larger or equal {}.".format(
                        varname, attr["ge"]
                    )
                )
            if attr.get("lt") is not None and value >= attr["lt"]:
                raise ValueError(
                    "Error: '{:s}' should be smaller than {}.".format(
                        varname, attr["lt"]
                    )
                )
            if attr.get("le") is not None and value > attr["le"]:
                raise ValueError(
                    "Error: '{:s}' should be smaller or equal {}.".format(
                        varname, attr["le"]
                    )
                )
            return
        else:
            print("[Warning] Unknown attribute {}".format(attr))

    raise TypeError(
        "Error: '{:s}' should be:{:s}, value: {:s}".format(
            varname, _param_print(param), str(value)
        )
    )
