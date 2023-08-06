"""
File to support the numpy file IO API (np.fromfile(), np.tofile()).
The actual definition of fromfile is inside untyped pass with the
other IO operations.
"""
import llvmlite.binding as ll
import numpy as np
from numba.core import types
from numba.extending import intrinsic, overload, overload_method
import bodo
from bodo.libs import hio
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.utils.utils import check_java_installation
ll.add_symbol('get_file_size', hio.get_file_size)
ll.add_symbol('file_read', hio.file_read)
ll.add_symbol('file_read_parallel', hio.file_read_parallel)
ll.add_symbol('file_write', hio.file_write)
ll.add_symbol('file_write_parallel', hio.file_write_parallel)
_get_file_size = types.ExternalFunction('get_file_size', types.int64(types.
    voidptr))
_file_read = types.ExternalFunction('file_read', types.void(types.voidptr,
    types.voidptr, types.intp, types.intp))
_file_read_parallel = types.ExternalFunction('file_read_parallel', types.
    void(types.voidptr, types.voidptr, types.intp, types.intp))
file_write = types.ExternalFunction('file_write', types.void(types.voidptr,
    types.voidptr, types.intp))
_file_write_parallel = types.ExternalFunction('file_write_parallel', types.
    void(types.voidptr, types.voidptr, types.intp, types.intp, types.intp))


@intrinsic
def get_dtype_size(typingctx, dtype=None):
    assert isinstance(dtype, types.DTypeSpec)

    def codegen(context, builder, sig, args):
        fhiza__wcptb = context.get_abi_sizeof(context.get_data_type(dtype.
            dtype))
        return context.get_constant(types.intp, fhiza__wcptb)
    return types.intp(dtype), codegen


@overload_method(types.Array, 'tofile')
def tofile_overload(arr, fname):
    if fname == string_type or isinstance(fname, types.StringLiteral):

        def tofile_impl(arr, fname):
            check_java_installation(fname)
            peya__bcpt = np.ascontiguousarray(arr)
            dtype_size = get_dtype_size(peya__bcpt.dtype)
            file_write(unicode_to_utf8(fname), peya__bcpt.ctypes, 
                dtype_size * peya__bcpt.size)
            bodo.utils.utils.check_and_propagate_cpp_exception()
        return tofile_impl


def file_write_parallel(fname, arr, start, count):
    pass


@overload(file_write_parallel)
def file_write_parallel_overload(fname, arr, start, count):
    if fname == string_type:

        def _impl(fname, arr, start, count):
            peya__bcpt = np.ascontiguousarray(arr)
            dtype_size = get_dtype_size(peya__bcpt.dtype)
            zjk__nszq = dtype_size * bodo.libs.distributed_api.get_tuple_prod(
                peya__bcpt.shape[1:])
            _file_write_parallel(unicode_to_utf8(fname), peya__bcpt.ctypes,
                start, count, zjk__nszq)
            bodo.utils.utils.check_and_propagate_cpp_exception()
        return _impl


def file_read_parallel(fname, arr, start, count):
    return


@overload(file_read_parallel)
def file_read_parallel_overload(fname, arr, start, count, offset):
    if fname == string_type:

        def _impl(fname, arr, start, count, offset):
            dtype_size = get_dtype_size(arr.dtype)
            _file_read_parallel(unicode_to_utf8(fname), arr.ctypes, start *
                dtype_size + offset, count * dtype_size)
            bodo.utils.utils.check_and_propagate_cpp_exception()
        return _impl


def file_read(fname, arr, size, offset):
    return


@overload(file_read)
def file_read_overload(fname, arr, size, offset):
    if fname == string_type:

        def impl(fname, arr, size, offset):
            _file_read(unicode_to_utf8(fname), arr.ctypes, size, offset)
            bodo.utils.utils.check_and_propagate_cpp_exception()
        return impl


def get_file_size(fname, count, offset, dtype_size):
    return 0


@overload(get_file_size)
def get_file_size_overload(fname, count, offset, dtype_size):
    if fname == string_type:

        def impl(fname, count, offset, dtype_size):
            if offset < 0:
                return -1
            qbfl__amr = _get_file_size(unicode_to_utf8(fname)) - offset
            bodo.utils.utils.check_and_propagate_cpp_exception()
            if count != -1:
                qbfl__amr = min(qbfl__amr, count * dtype_size)
            if qbfl__amr < 0:
                return -1
            return qbfl__amr
        return impl
