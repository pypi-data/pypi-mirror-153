import atexit
import datetime
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload, register_jitable
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, is_array_typ, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    gxx__ijm = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, gxx__ijm, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    gxx__ijm = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, gxx__ijm, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            gxx__ijm = get_type_enum(arr)
            return _isend(arr.ctypes, size, gxx__ijm, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        gxx__ijm = np.int32(numba_to_c_type(arr.dtype))
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            xnj__rqal = size + 7 >> 3
            goe__fgzqg = _isend(arr._data.ctypes, size, gxx__ijm, pe, tag, cond
                )
            spie__rgrc = _isend(arr._null_bitmap.ctypes, xnj__rqal,
                mean__wks, pe, tag, cond)
            return goe__fgzqg, spie__rgrc
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        fbro__qkxg = np.int32(numba_to_c_type(offset_type))
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            qldl__duv = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(qldl__duv, pe, tag - 1)
            xnj__rqal = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                fbro__qkxg, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), qldl__duv,
                mean__wks, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), xnj__rqal,
                mean__wks, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            gxx__ijm = get_type_enum(arr)
            return _irecv(arr.ctypes, size, gxx__ijm, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        gxx__ijm = np.int32(numba_to_c_type(arr.dtype))
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            xnj__rqal = size + 7 >> 3
            goe__fgzqg = _irecv(arr._data.ctypes, size, gxx__ijm, pe, tag, cond
                )
            spie__rgrc = _irecv(arr._null_bitmap.ctypes, xnj__rqal,
                mean__wks, pe, tag, cond)
            return goe__fgzqg, spie__rgrc
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        fbro__qkxg = np.int32(numba_to_c_type(offset_type))
        mean__wks = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            guif__gdbk = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            guif__gdbk = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        hvl__lttcy = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {guif__gdbk}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        tqi__pdknl = dict()
        exec(hvl__lttcy, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            fbro__qkxg, 'char_typ_enum': mean__wks}, tqi__pdknl)
        impl = tqi__pdknl['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    gxx__ijm = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), gxx__ijm)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        ywjyd__xxbvd = n_pes if rank == root or allgather else 0
        kcm__ivyw = np.empty(ywjyd__xxbvd, dtype)
        c_gather_scalar(send.ctypes, kcm__ivyw.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return kcm__ivyw
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        ihto__ieh = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], ihto__ieh)
        return builder.bitcast(ihto__ieh, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        ihto__ieh = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(ihto__ieh)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    uzykv__oami = types.unliteral(value)
    if isinstance(uzykv__oami, IndexValueType):
        uzykv__oami = uzykv__oami.val_typ
        uxjlq__vai = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            uxjlq__vai.append(types.int64)
            uxjlq__vai.append(bodo.datetime64ns)
            uxjlq__vai.append(bodo.timedelta64ns)
            uxjlq__vai.append(bodo.datetime_date_type)
        if uzykv__oami not in uxjlq__vai:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(uzykv__oami))
    typ_enum = np.int32(numba_to_c_type(uzykv__oami))

    def impl(value, reduce_op):
        pyvrm__qcl = value_to_ptr(value)
        rhj__zco = value_to_ptr(value)
        _dist_reduce(pyvrm__qcl, rhj__zco, reduce_op, typ_enum)
        return load_val_ptr(rhj__zco, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    uzykv__oami = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(uzykv__oami))
    tvcl__rxt = uzykv__oami(0)

    def impl(value, reduce_op):
        pyvrm__qcl = value_to_ptr(value)
        rhj__zco = value_to_ptr(tvcl__rxt)
        _dist_exscan(pyvrm__qcl, rhj__zco, reduce_op, typ_enum)
        return load_val_ptr(rhj__zco, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    vbfh__rvcla = 0
    zmeaq__cdk = 0
    for i in range(len(recv_counts)):
        uzzn__fhp = recv_counts[i]
        xnj__rqal = recv_counts_nulls[i]
        vzk__woypl = tmp_null_bytes[vbfh__rvcla:vbfh__rvcla + xnj__rqal]
        for utk__trjx in range(uzzn__fhp):
            set_bit_to(null_bitmap_ptr, zmeaq__cdk, get_bit(vzk__woypl,
                utk__trjx))
            zmeaq__cdk += 1
        vbfh__rvcla += xnj__rqal


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            adma__mib = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                adma__mib, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            ggi__kei = data.size
            recv_counts = gather_scalar(np.int32(ggi__kei), allgather, root
                =root)
            srch__dro = recv_counts.sum()
            byjxv__gsp = empty_like_type(srch__dro, data)
            pbwnq__kry = np.empty(1, np.int32)
            if rank == root or allgather:
                pbwnq__kry = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(ggi__kei), byjxv__gsp.ctypes,
                recv_counts.ctypes, pbwnq__kry.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return byjxv__gsp.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            byjxv__gsp = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(byjxv__gsp)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            byjxv__gsp = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(byjxv__gsp)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            ggi__kei = len(data)
            xnj__rqal = ggi__kei + 7 >> 3
            recv_counts = gather_scalar(np.int32(ggi__kei), allgather, root
                =root)
            srch__dro = recv_counts.sum()
            byjxv__gsp = empty_like_type(srch__dro, data)
            pbwnq__kry = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            lkiq__mffgp = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                pbwnq__kry = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                lkiq__mffgp = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(ggi__kei),
                byjxv__gsp._days_data.ctypes, recv_counts.ctypes,
                pbwnq__kry.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._seconds_data.ctypes, np.int32(ggi__kei),
                byjxv__gsp._seconds_data.ctypes, recv_counts.ctypes,
                pbwnq__kry.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(ggi__kei),
                byjxv__gsp._microseconds_data.ctypes, recv_counts.ctypes,
                pbwnq__kry.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(xnj__rqal),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lkiq__mffgp.ctypes, mean__wks, allgather, np.int32(root))
            copy_gathered_null_bytes(byjxv__gsp._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return byjxv__gsp
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            ggi__kei = len(data)
            xnj__rqal = ggi__kei + 7 >> 3
            recv_counts = gather_scalar(np.int32(ggi__kei), allgather, root
                =root)
            srch__dro = recv_counts.sum()
            byjxv__gsp = empty_like_type(srch__dro, data)
            pbwnq__kry = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            lkiq__mffgp = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                pbwnq__kry = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                lkiq__mffgp = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(ggi__kei), byjxv__gsp.
                _data.ctypes, recv_counts.ctypes, pbwnq__kry.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(xnj__rqal),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lkiq__mffgp.ctypes, mean__wks, allgather, np.int32(root))
            copy_gathered_null_bytes(byjxv__gsp._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return byjxv__gsp
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        ihpo__jbrjs = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            eetn__ryftm = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                eetn__ryftm, ihpo__jbrjs)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            npa__lerft = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            ctl__bthkj = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(npa__lerft,
                ctl__bthkj)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            nqfa__efux = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            xybv__tvdho = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                xybv__tvdho, nqfa__efux)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        tuy__ktibe = np.iinfo(np.int64).max
        wmphb__edev = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            erqb__dkv = data._start
            dvto__xnz = data._stop
            if len(data) == 0:
                erqb__dkv = tuy__ktibe
                dvto__xnz = wmphb__edev
            erqb__dkv = bodo.libs.distributed_api.dist_reduce(erqb__dkv, np
                .int32(Reduce_Type.Min.value))
            dvto__xnz = bodo.libs.distributed_api.dist_reduce(dvto__xnz, np
                .int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if erqb__dkv == tuy__ktibe and dvto__xnz == wmphb__edev:
                erqb__dkv = 0
                dvto__xnz = 0
            gsrcp__zcnrq = max(0, -(-(dvto__xnz - erqb__dkv) // data._step))
            if gsrcp__zcnrq < total_len:
                dvto__xnz = erqb__dkv + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                erqb__dkv = 0
                dvto__xnz = 0
            return bodo.hiframes.pd_index_ext.init_range_index(erqb__dkv,
                dvto__xnz, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            ipvu__ybu = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, ipvu__ybu)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            byjxv__gsp = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(byjxv__gsp
                , data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        lyjp__kdp = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        hvl__lttcy = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        hvl__lttcy += '  T = data\n'
        hvl__lttcy += '  T2 = init_table(T, True)\n'
        for fzx__hfewn in data.type_to_blk.values():
            lyjp__kdp[f'arr_inds_{fzx__hfewn}'] = np.array(data.
                block_to_arr_ind[fzx__hfewn], dtype=np.int64)
            hvl__lttcy += (
                f'  arr_list_{fzx__hfewn} = get_table_block(T, {fzx__hfewn})\n'
                )
            hvl__lttcy += f"""  out_arr_list_{fzx__hfewn} = alloc_list_like(arr_list_{fzx__hfewn}, True)
"""
            hvl__lttcy += f'  for i in range(len(arr_list_{fzx__hfewn})):\n'
            hvl__lttcy += (
                f'    arr_ind_{fzx__hfewn} = arr_inds_{fzx__hfewn}[i]\n')
            hvl__lttcy += f"""    ensure_column_unboxed(T, arr_list_{fzx__hfewn}, i, arr_ind_{fzx__hfewn})
"""
            hvl__lttcy += f"""    out_arr_{fzx__hfewn} = bodo.gatherv(arr_list_{fzx__hfewn}[i], allgather, warn_if_rep, root)
"""
            hvl__lttcy += (
                f'    out_arr_list_{fzx__hfewn}[i] = out_arr_{fzx__hfewn}\n')
            hvl__lttcy += (
                f'  T2 = set_table_block(T2, out_arr_list_{fzx__hfewn}, {fzx__hfewn})\n'
                )
        hvl__lttcy += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        hvl__lttcy += f'  T2 = set_table_len(T2, length)\n'
        hvl__lttcy += f'  return T2\n'
        tqi__pdknl = {}
        exec(hvl__lttcy, lyjp__kdp, tqi__pdknl)
        rfzmv__xrxmp = tqi__pdknl['impl_table']
        return rfzmv__xrxmp
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ivq__thc = len(data.columns)
        if ivq__thc == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                onyvq__zfez = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    onyvq__zfez, ())
            return impl
        eqhkq__igotx = ', '.join(f'g_data_{i}' for i in range(ivq__thc))
        zcd__jcdn = bodo.utils.transform.gen_const_tup(data.columns)
        hvl__lttcy = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            guw__jih = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            lyjp__kdp = {'bodo': bodo, 'df_type': guw__jih}
            eqhkq__igotx = 'T2'
            zcd__jcdn = 'df_type'
            hvl__lttcy += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            hvl__lttcy += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            lyjp__kdp = {'bodo': bodo}
            for i in range(ivq__thc):
                hvl__lttcy += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                hvl__lttcy += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        hvl__lttcy += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        hvl__lttcy += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        hvl__lttcy += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(eqhkq__igotx, zcd__jcdn))
        tqi__pdknl = {}
        exec(hvl__lttcy, lyjp__kdp, tqi__pdknl)
        vbr__leb = tqi__pdknl['impl_df']
        return vbr__leb
    if isinstance(data, ArrayItemArrayType):
        nji__czjxk = np.int32(numba_to_c_type(types.int32))
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            rtn__keo = bodo.libs.array_item_arr_ext.get_offsets(data)
            npjwh__xrbk = bodo.libs.array_item_arr_ext.get_data(data)
            npjwh__xrbk = npjwh__xrbk[:rtn__keo[-1]]
            gfgj__wta = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            ggi__kei = len(data)
            fjo__obmu = np.empty(ggi__kei, np.uint32)
            xnj__rqal = ggi__kei + 7 >> 3
            for i in range(ggi__kei):
                fjo__obmu[i] = rtn__keo[i + 1] - rtn__keo[i]
            recv_counts = gather_scalar(np.int32(ggi__kei), allgather, root
                =root)
            srch__dro = recv_counts.sum()
            pbwnq__kry = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            lkiq__mffgp = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                pbwnq__kry = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for ati__owq in range(len(recv_counts)):
                    recv_counts_nulls[ati__owq] = recv_counts[ati__owq
                        ] + 7 >> 3
                lkiq__mffgp = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            bzi__akp = np.empty(srch__dro + 1, np.uint32)
            yoxff__szit = bodo.gatherv(npjwh__xrbk, allgather, warn_if_rep,
                root)
            sdfv__eoyql = np.empty(srch__dro + 7 >> 3, np.uint8)
            c_gatherv(fjo__obmu.ctypes, np.int32(ggi__kei), bzi__akp.ctypes,
                recv_counts.ctypes, pbwnq__kry.ctypes, nji__czjxk,
                allgather, np.int32(root))
            c_gatherv(gfgj__wta.ctypes, np.int32(xnj__rqal), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, lkiq__mffgp.ctypes,
                mean__wks, allgather, np.int32(root))
            dummy_use(data)
            ldfzu__ypf = np.empty(srch__dro + 1, np.uint64)
            convert_len_arr_to_offset(bzi__akp.ctypes, ldfzu__ypf.ctypes,
                srch__dro)
            copy_gathered_null_bytes(sdfv__eoyql.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                srch__dro, yoxff__szit, ldfzu__ypf, sdfv__eoyql)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        krjbf__gtvvw = data.names
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            qrsc__udv = bodo.libs.struct_arr_ext.get_data(data)
            xneo__pybl = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            nxrp__kgtv = bodo.gatherv(qrsc__udv, allgather=allgather, root=root
                )
            rank = bodo.libs.distributed_api.get_rank()
            ggi__kei = len(data)
            xnj__rqal = ggi__kei + 7 >> 3
            recv_counts = gather_scalar(np.int32(ggi__kei), allgather, root
                =root)
            srch__dro = recv_counts.sum()
            ogut__oaerb = np.empty(srch__dro + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            lkiq__mffgp = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                lkiq__mffgp = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(xneo__pybl.ctypes, np.int32(xnj__rqal),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lkiq__mffgp.ctypes, mean__wks, allgather, np.int32(root))
            copy_gathered_null_bytes(ogut__oaerb.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(nxrp__kgtv,
                ogut__oaerb, krjbf__gtvvw)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            byjxv__gsp = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(byjxv__gsp)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            byjxv__gsp = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(byjxv__gsp)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            byjxv__gsp = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(byjxv__gsp)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            byjxv__gsp = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            zooj__ntcyg = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            vozm__odnsi = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            welze__mcocc = gather_scalar(data.shape[0], allgather, root=root)
            mhjp__tzdct = welze__mcocc.sum()
            ivq__thc = bodo.libs.distributed_api.dist_reduce(data.shape[1],
                np.int32(Reduce_Type.Max.value))
            rohxz__wef = np.empty(mhjp__tzdct + 1, np.int64)
            zooj__ntcyg = zooj__ntcyg.astype(np.int64)
            rohxz__wef[0] = 0
            pdffb__lpqt = 1
            ugnou__cyt = 0
            for gcssy__ghxhh in welze__mcocc:
                for upyof__fsip in range(gcssy__ghxhh):
                    tptol__ozrih = vozm__odnsi[ugnou__cyt + 1] - vozm__odnsi[
                        ugnou__cyt]
                    rohxz__wef[pdffb__lpqt] = rohxz__wef[pdffb__lpqt - 1
                        ] + tptol__ozrih
                    pdffb__lpqt += 1
                    ugnou__cyt += 1
                ugnou__cyt += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(byjxv__gsp,
                zooj__ntcyg, rohxz__wef, (mhjp__tzdct, ivq__thc))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        hvl__lttcy = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        hvl__lttcy += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        tqi__pdknl = {}
        exec(hvl__lttcy, {'bodo': bodo}, tqi__pdknl)
        dihjp__jurg = tqi__pdknl['impl_tuple']
        return dihjp__jurg
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    hvl__lttcy = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    hvl__lttcy += '    if random:\n'
    hvl__lttcy += '        if random_seed is None:\n'
    hvl__lttcy += '            random = 1\n'
    hvl__lttcy += '        else:\n'
    hvl__lttcy += '            random = 2\n'
    hvl__lttcy += '    if random_seed is None:\n'
    hvl__lttcy += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mwpq__eza = data
        ivq__thc = len(mwpq__eza.columns)
        for i in range(ivq__thc):
            hvl__lttcy += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        hvl__lttcy += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        eqhkq__igotx = ', '.join(f'data_{i}' for i in range(ivq__thc))
        hvl__lttcy += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(oilfo__fgb) for
            oilfo__fgb in range(ivq__thc))))
        hvl__lttcy += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        hvl__lttcy += '    if dests is None:\n'
        hvl__lttcy += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        hvl__lttcy += '    else:\n'
        hvl__lttcy += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for pjt__frgx in range(ivq__thc):
            hvl__lttcy += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(pjt__frgx))
        hvl__lttcy += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(ivq__thc))
        hvl__lttcy += '    delete_table(out_table)\n'
        hvl__lttcy += '    if parallel:\n'
        hvl__lttcy += '        delete_table(table_total)\n'
        eqhkq__igotx = ', '.join('out_arr_{}'.format(i) for i in range(
            ivq__thc))
        zcd__jcdn = bodo.utils.transform.gen_const_tup(mwpq__eza.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        hvl__lttcy += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(eqhkq__igotx, index, zcd__jcdn))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        hvl__lttcy += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        hvl__lttcy += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        hvl__lttcy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        hvl__lttcy += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        hvl__lttcy += '    if dests is None:\n'
        hvl__lttcy += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        hvl__lttcy += '    else:\n'
        hvl__lttcy += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        hvl__lttcy += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        hvl__lttcy += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        hvl__lttcy += '    delete_table(out_table)\n'
        hvl__lttcy += '    if parallel:\n'
        hvl__lttcy += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        hvl__lttcy += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        hvl__lttcy += '    if not parallel:\n'
        hvl__lttcy += '        return data\n'
        hvl__lttcy += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        hvl__lttcy += '    if dests is None:\n'
        hvl__lttcy += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        hvl__lttcy += '    elif bodo.get_rank() not in dests:\n'
        hvl__lttcy += '        dim0_local_size = 0\n'
        hvl__lttcy += '    else:\n'
        hvl__lttcy += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        hvl__lttcy += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        hvl__lttcy += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        hvl__lttcy += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        hvl__lttcy += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        hvl__lttcy += '    if dests is None:\n'
        hvl__lttcy += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        hvl__lttcy += '    else:\n'
        hvl__lttcy += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        hvl__lttcy += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        hvl__lttcy += '    delete_table(out_table)\n'
        hvl__lttcy += '    if parallel:\n'
        hvl__lttcy += '        delete_table(table_total)\n'
        hvl__lttcy += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    tqi__pdknl = {}
    exec(hvl__lttcy, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        tqi__pdknl)
    impl = tqi__pdknl['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    hvl__lttcy = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        hvl__lttcy += '    if seed is None:\n'
        hvl__lttcy += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        hvl__lttcy += '    np.random.seed(seed)\n'
        hvl__lttcy += '    if not parallel:\n'
        hvl__lttcy += '        data = data.copy()\n'
        hvl__lttcy += '        np.random.shuffle(data)\n'
        hvl__lttcy += '        return data\n'
        hvl__lttcy += '    else:\n'
        hvl__lttcy += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        hvl__lttcy += '        permutation = np.arange(dim0_global_size)\n'
        hvl__lttcy += '        np.random.shuffle(permutation)\n'
        hvl__lttcy += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        hvl__lttcy += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        hvl__lttcy += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        hvl__lttcy += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        hvl__lttcy += '        return output\n'
    else:
        hvl__lttcy += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    tqi__pdknl = {}
    exec(hvl__lttcy, {'np': np, 'bodo': bodo}, tqi__pdknl)
    impl = tqi__pdknl['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    izq__tff = np.empty(sendcounts_nulls.sum(), np.uint8)
    vbfh__rvcla = 0
    zmeaq__cdk = 0
    for hmd__vblb in range(len(sendcounts)):
        uzzn__fhp = sendcounts[hmd__vblb]
        xnj__rqal = sendcounts_nulls[hmd__vblb]
        vzk__woypl = izq__tff[vbfh__rvcla:vbfh__rvcla + xnj__rqal]
        for utk__trjx in range(uzzn__fhp):
            set_bit_to_arr(vzk__woypl, utk__trjx, get_bit_bitmap(
                null_bitmap_ptr, zmeaq__cdk))
            zmeaq__cdk += 1
        vbfh__rvcla += xnj__rqal
    return izq__tff


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    lmw__vluwi = MPI.COMM_WORLD
    data = lmw__vluwi.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    eou__sjxed = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    oob__tqp = (0,) * eou__sjxed

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        nixm__sis = np.ascontiguousarray(data)
        ncley__pkke = data.ctypes
        ttg__mgo = oob__tqp
        if rank == MPI_ROOT:
            ttg__mgo = nixm__sis.shape
        ttg__mgo = bcast_tuple(ttg__mgo)
        zhjp__atnkk = get_tuple_prod(ttg__mgo[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes, ttg__mgo[0]
            )
        send_counts *= zhjp__atnkk
        ggi__kei = send_counts[rank]
        nbbiz__scyg = np.empty(ggi__kei, dtype)
        pbwnq__kry = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(ncley__pkke, send_counts.ctypes, pbwnq__kry.ctypes,
            nbbiz__scyg.ctypes, np.int32(ggi__kei), np.int32(typ_val))
        return nbbiz__scyg.reshape((-1,) + ttg__mgo[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        ulbrs__nzmol = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], ulbrs__nzmol)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        nqfa__efux = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=nqfa__efux)
        csziv__yfq = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(csziv__yfq)
        return pd.Index(arr, name=nqfa__efux)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        nqfa__efux = _get_name_value_for_type(dtype.name_typ)
        krjbf__gtvvw = tuple(_get_name_value_for_type(t) for t in dtype.
            names_typ)
        qbo__mstk = tuple(get_value_for_type(t) for t in dtype.array_types)
        qbo__mstk = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in qbo__mstk)
        val = pd.MultiIndex.from_arrays(qbo__mstk, names=krjbf__gtvvw)
        val.name = nqfa__efux
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        nqfa__efux = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=nqfa__efux)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qbo__mstk = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({nqfa__efux: arr for nqfa__efux, arr in zip(
            dtype.columns, qbo__mstk)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        csziv__yfq = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(csziv__yfq[0],
            csziv__yfq[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if is_str_arr_type(data) or data == binary_array_type:
        nji__czjxk = np.int32(numba_to_c_type(types.int32))
        mean__wks = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            guif__gdbk = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            guif__gdbk = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        hvl__lttcy = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            data = decode_if_dict_array(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {guif__gdbk}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        tqi__pdknl = dict()
        exec(hvl__lttcy, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            nji__czjxk, 'char_typ_enum': mean__wks, 'decode_if_dict_array':
            decode_if_dict_array}, tqi__pdknl)
        impl = tqi__pdknl['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        nji__czjxk = np.int32(numba_to_c_type(types.int32))
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            uig__tfdkp = bodo.libs.array_item_arr_ext.get_offsets(data)
            sgij__bbbb = bodo.libs.array_item_arr_ext.get_data(data)
            sgij__bbbb = sgij__bbbb[:uig__tfdkp[-1]]
            tjna__ugjw = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            awji__pprx = bcast_scalar(len(data))
            wumuw__mvhmx = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                wumuw__mvhmx[i] = uig__tfdkp[i + 1] - uig__tfdkp[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                awji__pprx)
            pbwnq__kry = bodo.ir.join.calc_disp(send_counts)
            ihoyf__uur = np.empty(n_pes, np.int32)
            if rank == 0:
                kej__xav = 0
                for i in range(n_pes):
                    pkzz__esp = 0
                    for upyof__fsip in range(send_counts[i]):
                        pkzz__esp += wumuw__mvhmx[kej__xav]
                        kej__xav += 1
                    ihoyf__uur[i] = pkzz__esp
            bcast(ihoyf__uur)
            iwsmr__jyazb = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                iwsmr__jyazb[i] = send_counts[i] + 7 >> 3
            lkiq__mffgp = bodo.ir.join.calc_disp(iwsmr__jyazb)
            ggi__kei = send_counts[rank]
            gpnc__vdc = np.empty(ggi__kei + 1, np_offset_type)
            pth__xwdoc = bodo.libs.distributed_api.scatterv_impl(sgij__bbbb,
                ihoyf__uur)
            sszve__gqgsr = ggi__kei + 7 >> 3
            sgkb__wquvf = np.empty(sszve__gqgsr, np.uint8)
            jjcf__rxei = np.empty(ggi__kei, np.uint32)
            c_scatterv(wumuw__mvhmx.ctypes, send_counts.ctypes, pbwnq__kry.
                ctypes, jjcf__rxei.ctypes, np.int32(ggi__kei), nji__czjxk)
            convert_len_arr_to_offset(jjcf__rxei.ctypes, gpnc__vdc.ctypes,
                ggi__kei)
            oworo__lho = get_scatter_null_bytes_buff(tjna__ugjw.ctypes,
                send_counts, iwsmr__jyazb)
            c_scatterv(oworo__lho.ctypes, iwsmr__jyazb.ctypes, lkiq__mffgp.
                ctypes, sgkb__wquvf.ctypes, np.int32(sszve__gqgsr), mean__wks)
            return bodo.libs.array_item_arr_ext.init_array_item_array(ggi__kei,
                pth__xwdoc, gpnc__vdc, sgkb__wquvf)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        mean__wks = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            ytm__inzrb = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            ytm__inzrb = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            ytm__inzrb = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            ytm__inzrb = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            nixm__sis = data._data
            xneo__pybl = data._null_bitmap
            sfh__bixu = len(nixm__sis)
            vzykk__hnsi = _scatterv_np(nixm__sis, send_counts)
            awji__pprx = bcast_scalar(sfh__bixu)
            hcxk__ygnan = len(vzykk__hnsi) + 7 >> 3
            pczqu__mwcum = np.empty(hcxk__ygnan, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                awji__pprx)
            iwsmr__jyazb = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                iwsmr__jyazb[i] = send_counts[i] + 7 >> 3
            lkiq__mffgp = bodo.ir.join.calc_disp(iwsmr__jyazb)
            oworo__lho = get_scatter_null_bytes_buff(xneo__pybl.ctypes,
                send_counts, iwsmr__jyazb)
            c_scatterv(oworo__lho.ctypes, iwsmr__jyazb.ctypes, lkiq__mffgp.
                ctypes, pczqu__mwcum.ctypes, np.int32(hcxk__ygnan), mean__wks)
            return ytm__inzrb(vzykk__hnsi, pczqu__mwcum)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            jqnly__mitj = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            pee__locbw = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(jqnly__mitj,
                pee__locbw)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            erqb__dkv = data._start
            dvto__xnz = data._stop
            grbbq__dxbj = data._step
            nqfa__efux = data._name
            nqfa__efux = bcast_scalar(nqfa__efux)
            erqb__dkv = bcast_scalar(erqb__dkv)
            dvto__xnz = bcast_scalar(dvto__xnz)
            grbbq__dxbj = bcast_scalar(grbbq__dxbj)
            ejyzq__sou = bodo.libs.array_kernels.calc_nitems(erqb__dkv,
                dvto__xnz, grbbq__dxbj)
            chunk_start = bodo.libs.distributed_api.get_start(ejyzq__sou,
                n_pes, rank)
            llt__iwa = bodo.libs.distributed_api.get_node_portion(ejyzq__sou,
                n_pes, rank)
            pebd__uwt = erqb__dkv + grbbq__dxbj * chunk_start
            mnjqb__nuqre = erqb__dkv + grbbq__dxbj * (chunk_start + llt__iwa)
            mnjqb__nuqre = min(mnjqb__nuqre, dvto__xnz)
            return bodo.hiframes.pd_index_ext.init_range_index(pebd__uwt,
                mnjqb__nuqre, grbbq__dxbj, nqfa__efux)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        ipvu__ybu = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            nixm__sis = data._data
            nqfa__efux = data._name
            nqfa__efux = bcast_scalar(nqfa__efux)
            arr = bodo.libs.distributed_api.scatterv_impl(nixm__sis,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                nqfa__efux, ipvu__ybu)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            nixm__sis = data._data
            nqfa__efux = data._name
            nqfa__efux = bcast_scalar(nqfa__efux)
            arr = bodo.libs.distributed_api.scatterv_impl(nixm__sis,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, nqfa__efux)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            byjxv__gsp = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            nqfa__efux = bcast_scalar(data._name)
            krjbf__gtvvw = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(byjxv__gsp
                , krjbf__gtvvw, nqfa__efux)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            nqfa__efux = bodo.hiframes.pd_series_ext.get_series_name(data)
            ungy__iroi = bcast_scalar(nqfa__efux)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            xybv__tvdho = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                xybv__tvdho, ungy__iroi)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ivq__thc = len(data.columns)
        eqhkq__igotx = ', '.join('g_data_{}'.format(i) for i in range(ivq__thc)
            )
        zcd__jcdn = bodo.utils.transform.gen_const_tup(data.columns)
        hvl__lttcy = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(ivq__thc):
            hvl__lttcy += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            hvl__lttcy += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        hvl__lttcy += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        hvl__lttcy += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        hvl__lttcy += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(eqhkq__igotx, zcd__jcdn))
        tqi__pdknl = {}
        exec(hvl__lttcy, {'bodo': bodo}, tqi__pdknl)
        vbr__leb = tqi__pdknl['impl_df']
        return vbr__leb
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            adma__mib = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                adma__mib, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        hvl__lttcy = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        hvl__lttcy += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        tqi__pdknl = {}
        exec(hvl__lttcy, {'bodo': bodo}, tqi__pdknl)
        dihjp__jurg = tqi__pdknl['impl_tuple']
        return dihjp__jurg
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.bcast()')
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, IntegerArrayType) or data in (boolean_array,
        datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if is_str_arr_type(data) or data == binary_array_type:
        fbro__qkxg = np.int32(numba_to_c_type(offset_type))
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            ggi__kei = len(data)
            jrrfp__imgrm = num_total_chars(data)
            assert ggi__kei < INT_MAX
            assert jrrfp__imgrm < INT_MAX
            yqd__tsmqx = get_offset_ptr(data)
            ncley__pkke = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            xnj__rqal = ggi__kei + 7 >> 3
            c_bcast(yqd__tsmqx, np.int32(ggi__kei + 1), fbro__qkxg, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(ncley__pkke, np.int32(jrrfp__imgrm), mean__wks, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(xnj__rqal), mean__wks, np.
                array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        mean__wks = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                ktnxn__oqz = 0
                ncbrk__xdgqd = np.empty(0, np.uint8).ctypes
            else:
                ncbrk__xdgqd, ktnxn__oqz = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            ktnxn__oqz = bodo.libs.distributed_api.bcast_scalar(ktnxn__oqz,
                root)
            if rank != root:
                zgzt__yugvx = np.empty(ktnxn__oqz + 1, np.uint8)
                zgzt__yugvx[ktnxn__oqz] = 0
                ncbrk__xdgqd = zgzt__yugvx.ctypes
            c_bcast(ncbrk__xdgqd, np.int32(ktnxn__oqz), mean__wks, np.array
                ([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(ncbrk__xdgqd, ktnxn__oqz)
        return impl_str
    typ_val = numba_to_c_type(val)
    hvl__lttcy = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    tqi__pdknl = {}
    exec(hvl__lttcy, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, tqi__pdknl)
    iblay__rzs = tqi__pdknl['bcast_scalar_impl']
    return iblay__rzs


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    jpahp__suxe = len(val)
    hvl__lttcy = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    hvl__lttcy += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(jpahp__suxe)
        ), ',' if jpahp__suxe else '')
    tqi__pdknl = {}
    exec(hvl__lttcy, {'bcast_scalar': bcast_scalar}, tqi__pdknl)
    pjwl__kiys = tqi__pdknl['bcast_tuple_impl']
    return pjwl__kiys


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            ggi__kei = bcast_scalar(len(arr), root)
            noq__fkz = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(ggi__kei, noq__fkz)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):

    def impl(idx, arr_start, total_len):
        slice_index = numba.cpython.unicode._normalize_slice(idx, total_len)
        erqb__dkv = slice_index.start
        grbbq__dxbj = slice_index.step
        jlq__mwfqm = 0 if grbbq__dxbj == 1 or erqb__dkv > arr_start else abs(
            grbbq__dxbj - arr_start % grbbq__dxbj) % grbbq__dxbj
        pebd__uwt = max(arr_start, slice_index.start) - arr_start + jlq__mwfqm
        mnjqb__nuqre = max(slice_index.stop - arr_start, 0)
        return slice(pebd__uwt, mnjqb__nuqre, grbbq__dxbj)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        hutm__ukk = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[hutm__ukk])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        wxdf__smaf = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        mean__wks = np.int32(numba_to_c_type(types.uint8))
        nga__lcx = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            kxun__fji = np.int32(10)
            tag = np.int32(11)
            ekgy__hsyey = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                npjwh__xrbk = arr._data
                dyj__wsm = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    npjwh__xrbk, ind)
                xcnc__ias = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    npjwh__xrbk, ind + 1)
                length = xcnc__ias - dyj__wsm
                ihto__ieh = npjwh__xrbk[ind]
                ekgy__hsyey[0] = length
                isend(ekgy__hsyey, np.int32(1), root, kxun__fji, True)
                isend(ihto__ieh, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(nga__lcx,
                wxdf__smaf, 0, 1)
            gsrcp__zcnrq = 0
            if rank == root:
                gsrcp__zcnrq = recv(np.int64, ANY_SOURCE, kxun__fji)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    nga__lcx, wxdf__smaf, gsrcp__zcnrq, 1)
                ncley__pkke = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(ncley__pkke, np.int32(gsrcp__zcnrq), mean__wks,
                    ANY_SOURCE, tag)
            dummy_use(ekgy__hsyey)
            gsrcp__zcnrq = bcast_scalar(gsrcp__zcnrq)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    nga__lcx, wxdf__smaf, gsrcp__zcnrq, 1)
            ncley__pkke = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(ncley__pkke, np.int32(gsrcp__zcnrq), mean__wks, np.
                array([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, gsrcp__zcnrq)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        vzp__dvt = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, vzp__dvt)
            if arr_start <= ind < arr_start + len(arr):
                adma__mib = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = adma__mib[ind - arr_start]
                send_arr = np.full(1, data, vzp__dvt)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = vzp__dvt(-1)
            if rank == root:
                val = recv(vzp__dvt, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            nfpl__kyelr = arr.dtype.categories[max(val, 0)]
            return nfpl__kyelr
        return cat_getitem_impl
    cbfl__nftxe = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, cbfl__nftxe)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, cbfl__nftxe)[0]
        if rank == root:
            val = recv(cbfl__nftxe, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    xzhqn__xfs = get_type_enum(out_data)
    assert typ_enum == xzhqn__xfs
    if isinstance(send_data, (IntegerArrayType, DecimalArrayType)
        ) or send_data in (boolean_array, datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    hvl__lttcy = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        hvl__lttcy += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    hvl__lttcy += '  return\n'
    tqi__pdknl = {}
    exec(hvl__lttcy, {'alltoallv': alltoallv}, tqi__pdknl)
    puie__vumaq = tqi__pdknl['f']
    return puie__vumaq


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    erqb__dkv = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return erqb__dkv, count


@numba.njit
def get_start(total_size, pes, rank):
    kcm__ivyw = total_size % pes
    mvlqv__ocyb = (total_size - kcm__ivyw) // pes
    return rank * mvlqv__ocyb + min(rank, kcm__ivyw)


@numba.njit
def get_end(total_size, pes, rank):
    kcm__ivyw = total_size % pes
    mvlqv__ocyb = (total_size - kcm__ivyw) // pes
    return (rank + 1) * mvlqv__ocyb + min(rank + 1, kcm__ivyw)


@numba.njit
def get_node_portion(total_size, pes, rank):
    kcm__ivyw = total_size % pes
    mvlqv__ocyb = (total_size - kcm__ivyw) // pes
    if rank < kcm__ivyw:
        return mvlqv__ocyb + 1
    else:
        return mvlqv__ocyb


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    tvcl__rxt = in_arr.dtype(0)
    bvfh__enpg = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        pkzz__esp = tvcl__rxt
        for kla__vgos in np.nditer(in_arr):
            pkzz__esp += kla__vgos.item()
        ewp__qvnb = dist_exscan(pkzz__esp, bvfh__enpg)
        for i in range(in_arr.size):
            ewp__qvnb += in_arr[i]
            out_arr[i] = ewp__qvnb
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    dnpxl__vzsj = in_arr.dtype(1)
    bvfh__enpg = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        pkzz__esp = dnpxl__vzsj
        for kla__vgos in np.nditer(in_arr):
            pkzz__esp *= kla__vgos.item()
        ewp__qvnb = dist_exscan(pkzz__esp, bvfh__enpg)
        if get_rank() == 0:
            ewp__qvnb = dnpxl__vzsj
        for i in range(in_arr.size):
            ewp__qvnb *= in_arr[i]
            out_arr[i] = ewp__qvnb
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        dnpxl__vzsj = np.finfo(in_arr.dtype(1).dtype).max
    else:
        dnpxl__vzsj = np.iinfo(in_arr.dtype(1).dtype).max
    bvfh__enpg = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        pkzz__esp = dnpxl__vzsj
        for kla__vgos in np.nditer(in_arr):
            pkzz__esp = min(pkzz__esp, kla__vgos.item())
        ewp__qvnb = dist_exscan(pkzz__esp, bvfh__enpg)
        if get_rank() == 0:
            ewp__qvnb = dnpxl__vzsj
        for i in range(in_arr.size):
            ewp__qvnb = min(ewp__qvnb, in_arr[i])
            out_arr[i] = ewp__qvnb
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        dnpxl__vzsj = np.finfo(in_arr.dtype(1).dtype).min
    else:
        dnpxl__vzsj = np.iinfo(in_arr.dtype(1).dtype).min
    dnpxl__vzsj = in_arr.dtype(1)
    bvfh__enpg = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        pkzz__esp = dnpxl__vzsj
        for kla__vgos in np.nditer(in_arr):
            pkzz__esp = max(pkzz__esp, kla__vgos.item())
        ewp__qvnb = dist_exscan(pkzz__esp, bvfh__enpg)
        if get_rank() == 0:
            ewp__qvnb = dnpxl__vzsj
        for i in range(in_arr.size):
            ewp__qvnb = max(ewp__qvnb, in_arr[i])
            out_arr[i] = ewp__qvnb
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    gxx__ijm = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), gxx__ijm)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    gom__oinoz = args[0]
    if equiv_set.has_shape(gom__oinoz):
        return ArrayAnalysis.AnalyzeResult(shape=gom__oinoz, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


def print_if_not_empty(args):
    pass


@overload(print_if_not_empty)
def overload_print_if_not_empty(*args):
    cbk__ujy = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for i,
        hzmn__rmm in enumerate(args) if is_array_typ(hzmn__rmm) or
        isinstance(hzmn__rmm, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    hvl__lttcy = f"""def impl(*args):
    if {cbk__ujy} or bodo.get_rank() == 0:
        print(*args)"""
    tqi__pdknl = {}
    exec(hvl__lttcy, globals(), tqi__pdknl)
    impl = tqi__pdknl['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        dht__pvor = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        hvl__lttcy = 'def f(req, cond=True):\n'
        hvl__lttcy += f'  return {dht__pvor}\n'
        tqi__pdknl = {}
        exec(hvl__lttcy, {'_wait': _wait}, tqi__pdknl)
        impl = tqi__pdknl['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        kcm__ivyw = 1
        for a in t:
            kcm__ivyw *= a
        return kcm__ivyw
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    jra__fvp = np.ascontiguousarray(in_arr)
    yywp__xxm = get_tuple_prod(jra__fvp.shape[1:])
    vspb__axlp = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        bzvsb__qspx = np.array(dest_ranks, dtype=np.int32)
    else:
        bzvsb__qspx = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, jra__fvp.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * vspb__axlp, dtype_size * yywp__xxm, len(
        bzvsb__qspx), bzvsb__qspx.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len):
    wzgpf__jfykt = np.ascontiguousarray(rhs)
    erx__yokju = get_tuple_prod(wzgpf__jfykt.shape[1:])
    hdg__eeaec = dtype_size * erx__yokju
    permutation_array_index(lhs.ctypes, lhs_len, hdg__eeaec, wzgpf__jfykt.
        ctypes, wzgpf__jfykt.shape[0], p.ctypes, p_len)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader, s3_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_s3', s3_reader.finalize_s3)
finalize_s3 = types.ExternalFunction('finalize_s3', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def call_finalize():
    finalize()
    finalize_s3()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        hvl__lttcy = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        tqi__pdknl = {}
        exec(hvl__lttcy, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, tqi__pdknl)
        iblay__rzs = tqi__pdknl['bcast_scalar_impl']
        return iblay__rzs
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ivq__thc = len(data.columns)
        eqhkq__igotx = ', '.join('g_data_{}'.format(i) for i in range(ivq__thc)
            )
        zcd__jcdn = bodo.utils.transform.gen_const_tup(data.columns)
        hvl__lttcy = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(ivq__thc):
            hvl__lttcy += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            hvl__lttcy += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        hvl__lttcy += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        hvl__lttcy += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        hvl__lttcy += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(eqhkq__igotx, zcd__jcdn))
        tqi__pdknl = {}
        exec(hvl__lttcy, {'bodo': bodo}, tqi__pdknl)
        vbr__leb = tqi__pdknl['impl_df']
        return vbr__leb
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            erqb__dkv = data._start
            dvto__xnz = data._stop
            grbbq__dxbj = data._step
            nqfa__efux = data._name
            nqfa__efux = bcast_scalar(nqfa__efux, root)
            erqb__dkv = bcast_scalar(erqb__dkv, root)
            dvto__xnz = bcast_scalar(dvto__xnz, root)
            grbbq__dxbj = bcast_scalar(grbbq__dxbj, root)
            ejyzq__sou = bodo.libs.array_kernels.calc_nitems(erqb__dkv,
                dvto__xnz, grbbq__dxbj)
            chunk_start = bodo.libs.distributed_api.get_start(ejyzq__sou,
                n_pes, rank)
            llt__iwa = bodo.libs.distributed_api.get_node_portion(ejyzq__sou,
                n_pes, rank)
            pebd__uwt = erqb__dkv + grbbq__dxbj * chunk_start
            mnjqb__nuqre = erqb__dkv + grbbq__dxbj * (chunk_start + llt__iwa)
            mnjqb__nuqre = min(mnjqb__nuqre, dvto__xnz)
            return bodo.hiframes.pd_index_ext.init_range_index(pebd__uwt,
                mnjqb__nuqre, grbbq__dxbj, nqfa__efux)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            nixm__sis = data._data
            nqfa__efux = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(nixm__sis,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, nqfa__efux)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            nqfa__efux = bodo.hiframes.pd_series_ext.get_series_name(data)
            ungy__iroi = bodo.libs.distributed_api.bcast_comm_impl(nqfa__efux,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            xybv__tvdho = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                xybv__tvdho, ungy__iroi)
        return impl_series
    if isinstance(data, types.BaseTuple):
        hvl__lttcy = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        hvl__lttcy += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        tqi__pdknl = {}
        exec(hvl__lttcy, {'bcast_comm_impl': bcast_comm_impl}, tqi__pdknl)
        dihjp__jurg = tqi__pdknl['impl_tuple']
        return dihjp__jurg
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    eou__sjxed = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    oob__tqp = (0,) * eou__sjxed

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        nixm__sis = np.ascontiguousarray(data)
        ncley__pkke = data.ctypes
        ttg__mgo = oob__tqp
        if rank == root:
            ttg__mgo = nixm__sis.shape
        ttg__mgo = bcast_tuple(ttg__mgo, root)
        zhjp__atnkk = get_tuple_prod(ttg__mgo[1:])
        send_counts = ttg__mgo[0] * zhjp__atnkk
        nbbiz__scyg = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(ncley__pkke, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(nbbiz__scyg.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return nbbiz__scyg.reshape((-1,) + ttg__mgo[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        lmw__vluwi = MPI.COMM_WORLD
        mcvyl__lbyls = MPI.Get_processor_name()
        bqjt__bif = lmw__vluwi.allgather(mcvyl__lbyls)
        node_ranks = defaultdict(list)
        for i, dwn__jzu in enumerate(bqjt__bif):
            node_ranks[dwn__jzu].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    lmw__vluwi = MPI.COMM_WORLD
    vneya__wwrp = lmw__vluwi.Get_group()
    gzx__uvnk = vneya__wwrp.Incl(comm_ranks)
    upkwm__quqnb = lmw__vluwi.Create_group(gzx__uvnk)
    return upkwm__quqnb


def get_nodes_first_ranks():
    vaskr__jjesa = get_host_ranks()
    return np.array([evpc__gmlm[0] for evpc__gmlm in vaskr__jjesa.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
