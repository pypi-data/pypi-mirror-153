import atexit
import datetime
import operator
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
from numba.extending import intrinsic, models, overload, register_jitable, register_model
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
ll.add_symbol('comm_req_alloc', hdist.comm_req_alloc)
ll.add_symbol('comm_req_dealloc', hdist.comm_req_dealloc)
ll.add_symbol('req_array_setitem', hdist.req_array_setitem)
ll.add_symbol('dist_waitall', hdist.dist_waitall)
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
    mnde__vtc = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, mnde__vtc, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    mnde__vtc = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, mnde__vtc, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            mnde__vtc = get_type_enum(arr)
            return _isend(arr.ctypes, size, mnde__vtc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        mnde__vtc = np.int32(numba_to_c_type(arr.dtype))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            mbp__ncb = size + 7 >> 3
            mwhj__sxla = _isend(arr._data.ctypes, size, mnde__vtc, pe, tag,
                cond)
            zvfo__vinv = _isend(arr._null_bitmap.ctypes, mbp__ncb,
                wmyat__algy, pe, tag, cond)
            return mwhj__sxla, zvfo__vinv
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        sygww__qepl = np.int32(numba_to_c_type(offset_type))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            agnyz__nvysl = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(agnyz__nvysl, pe, tag - 1)
            mbp__ncb = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                sygww__qepl, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), agnyz__nvysl,
                wmyat__algy, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), mbp__ncb,
                wmyat__algy, pe, tag)
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
            mnde__vtc = get_type_enum(arr)
            return _irecv(arr.ctypes, size, mnde__vtc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        mnde__vtc = np.int32(numba_to_c_type(arr.dtype))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            mbp__ncb = size + 7 >> 3
            mwhj__sxla = _irecv(arr._data.ctypes, size, mnde__vtc, pe, tag,
                cond)
            zvfo__vinv = _irecv(arr._null_bitmap.ctypes, mbp__ncb,
                wmyat__algy, pe, tag, cond)
            return mwhj__sxla, zvfo__vinv
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        sygww__qepl = np.int32(numba_to_c_type(offset_type))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            twwjg__oqrc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            twwjg__oqrc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        wqj__ssrc = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {twwjg__oqrc}(size, n_chars)
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
        rgtnd__xmrgw = dict()
        exec(wqj__ssrc, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            sygww__qepl, 'char_typ_enum': wmyat__algy}, rgtnd__xmrgw)
        impl = rgtnd__xmrgw['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    mnde__vtc = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), mnde__vtc)


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
        hrvsg__rvch = n_pes if rank == root or allgather else 0
        tcq__fiqbg = np.empty(hrvsg__rvch, dtype)
        c_gather_scalar(send.ctypes, tcq__fiqbg.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return tcq__fiqbg
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
        gdpw__uefz = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], gdpw__uefz)
        return builder.bitcast(gdpw__uefz, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        gdpw__uefz = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(gdpw__uefz)
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
    vrm__jmwuw = types.unliteral(value)
    if isinstance(vrm__jmwuw, IndexValueType):
        vrm__jmwuw = vrm__jmwuw.val_typ
        kfcw__ycdwz = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            kfcw__ycdwz.append(types.int64)
            kfcw__ycdwz.append(bodo.datetime64ns)
            kfcw__ycdwz.append(bodo.timedelta64ns)
            kfcw__ycdwz.append(bodo.datetime_date_type)
        if vrm__jmwuw not in kfcw__ycdwz:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(vrm__jmwuw))
    typ_enum = np.int32(numba_to_c_type(vrm__jmwuw))

    def impl(value, reduce_op):
        hdwps__fnj = value_to_ptr(value)
        nep__oafry = value_to_ptr(value)
        _dist_reduce(hdwps__fnj, nep__oafry, reduce_op, typ_enum)
        return load_val_ptr(nep__oafry, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    vrm__jmwuw = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(vrm__jmwuw))
    wxt__vvmvr = vrm__jmwuw(0)

    def impl(value, reduce_op):
        hdwps__fnj = value_to_ptr(value)
        nep__oafry = value_to_ptr(wxt__vvmvr)
        _dist_exscan(hdwps__fnj, nep__oafry, reduce_op, typ_enum)
        return load_val_ptr(nep__oafry, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    yoeua__vuik = 0
    nqf__qhi = 0
    for i in range(len(recv_counts)):
        wrdl__urs = recv_counts[i]
        mbp__ncb = recv_counts_nulls[i]
        wcpdc__gbpj = tmp_null_bytes[yoeua__vuik:yoeua__vuik + mbp__ncb]
        for ptx__lxrvz in range(wrdl__urs):
            set_bit_to(null_bitmap_ptr, nqf__qhi, get_bit(wcpdc__gbpj,
                ptx__lxrvz))
            nqf__qhi += 1
        yoeua__vuik += mbp__ncb


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            jtpej__dzf = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                jtpej__dzf, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            xdvvv__bfizp = data.size
            recv_counts = gather_scalar(np.int32(xdvvv__bfizp), allgather,
                root=root)
            kypq__yui = recv_counts.sum()
            owi__cri = empty_like_type(kypq__yui, data)
            qbvtg__tlukd = np.empty(1, np.int32)
            if rank == root or allgather:
                qbvtg__tlukd = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(xdvvv__bfizp), owi__cri.ctypes,
                recv_counts.ctypes, qbvtg__tlukd.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return owi__cri.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            owi__cri = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(owi__cri)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            owi__cri = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(owi__cri)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            xdvvv__bfizp = len(data)
            mbp__ncb = xdvvv__bfizp + 7 >> 3
            recv_counts = gather_scalar(np.int32(xdvvv__bfizp), allgather,
                root=root)
            kypq__yui = recv_counts.sum()
            owi__cri = empty_like_type(kypq__yui, data)
            qbvtg__tlukd = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            znld__uol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                qbvtg__tlukd = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                znld__uol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(xdvvv__bfizp),
                owi__cri._days_data.ctypes, recv_counts.ctypes,
                qbvtg__tlukd.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._seconds_data.ctypes, np.int32(xdvvv__bfizp),
                owi__cri._seconds_data.ctypes, recv_counts.ctypes,
                qbvtg__tlukd.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(xdvvv__bfizp
                ), owi__cri._microseconds_data.ctypes, recv_counts.ctypes,
                qbvtg__tlukd.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(mbp__ncb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, znld__uol.
                ctypes, wmyat__algy, allgather, np.int32(root))
            copy_gathered_null_bytes(owi__cri._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return owi__cri
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            xdvvv__bfizp = len(data)
            mbp__ncb = xdvvv__bfizp + 7 >> 3
            recv_counts = gather_scalar(np.int32(xdvvv__bfizp), allgather,
                root=root)
            kypq__yui = recv_counts.sum()
            owi__cri = empty_like_type(kypq__yui, data)
            qbvtg__tlukd = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            znld__uol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                qbvtg__tlukd = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                znld__uol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(xdvvv__bfizp), owi__cri.
                _data.ctypes, recv_counts.ctypes, qbvtg__tlukd.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(mbp__ncb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, znld__uol.
                ctypes, wmyat__algy, allgather, np.int32(root))
            copy_gathered_null_bytes(owi__cri._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return owi__cri
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        nnqq__rfi = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            son__btczu = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                son__btczu, nnqq__rfi)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            ixaj__ixucn = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            vkqrx__jxh = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(ixaj__ixucn,
                vkqrx__jxh)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ufn__jgfw = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            wcsu__mgtlf = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                wcsu__mgtlf, ufn__jgfw)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        hls__aud = np.iinfo(np.int64).max
        utc__wvu = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = hls__aud
                stop = utc__wvu
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == hls__aud and stop == utc__wvu:
                start = 0
                stop = 0
            mdtp__odaux = max(0, -(-(stop - start) // data._step))
            if mdtp__odaux < total_len:
                stop = start + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                start = 0
                stop = 0
            return bodo.hiframes.pd_index_ext.init_range_index(start, stop,
                data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            sdaau__cjffq = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, sdaau__cjffq)
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
            owi__cri = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(owi__cri,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        epmqf__zmx = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        wqj__ssrc = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        wqj__ssrc += '  T = data\n'
        wqj__ssrc += '  T2 = init_table(T, True)\n'
        for szx__qrezv in data.type_to_blk.values():
            epmqf__zmx[f'arr_inds_{szx__qrezv}'] = np.array(data.
                block_to_arr_ind[szx__qrezv], dtype=np.int64)
            wqj__ssrc += (
                f'  arr_list_{szx__qrezv} = get_table_block(T, {szx__qrezv})\n'
                )
            wqj__ssrc += f"""  out_arr_list_{szx__qrezv} = alloc_list_like(arr_list_{szx__qrezv}, True)
"""
            wqj__ssrc += f'  for i in range(len(arr_list_{szx__qrezv})):\n'
            wqj__ssrc += (
                f'    arr_ind_{szx__qrezv} = arr_inds_{szx__qrezv}[i]\n')
            wqj__ssrc += f"""    ensure_column_unboxed(T, arr_list_{szx__qrezv}, i, arr_ind_{szx__qrezv})
"""
            wqj__ssrc += f"""    out_arr_{szx__qrezv} = bodo.gatherv(arr_list_{szx__qrezv}[i], allgather, warn_if_rep, root)
"""
            wqj__ssrc += (
                f'    out_arr_list_{szx__qrezv}[i] = out_arr_{szx__qrezv}\n')
            wqj__ssrc += (
                f'  T2 = set_table_block(T2, out_arr_list_{szx__qrezv}, {szx__qrezv})\n'
                )
        wqj__ssrc += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        wqj__ssrc += f'  T2 = set_table_len(T2, length)\n'
        wqj__ssrc += f'  return T2\n'
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, epmqf__zmx, rgtnd__xmrgw)
        jvz__plmu = rgtnd__xmrgw['impl_table']
        return jvz__plmu
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mnlk__tndn = len(data.columns)
        if mnlk__tndn == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                puy__xevp = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    puy__xevp, ())
            return impl
        fbuv__luqva = ', '.join(f'g_data_{i}' for i in range(mnlk__tndn))
        qocv__djeb = bodo.utils.transform.gen_const_tup(data.columns)
        wqj__ssrc = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            dmua__prs = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            epmqf__zmx = {'bodo': bodo, 'df_type': dmua__prs}
            fbuv__luqva = 'T2'
            qocv__djeb = 'df_type'
            wqj__ssrc += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            wqj__ssrc += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            epmqf__zmx = {'bodo': bodo}
            for i in range(mnlk__tndn):
                wqj__ssrc += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                wqj__ssrc += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        wqj__ssrc += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        wqj__ssrc += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        wqj__ssrc += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(fbuv__luqva, qocv__djeb))
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, epmqf__zmx, rgtnd__xmrgw)
        imd__vuwu = rgtnd__xmrgw['impl_df']
        return imd__vuwu
    if isinstance(data, ArrayItemArrayType):
        ice__ybn = np.int32(numba_to_c_type(types.int32))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            fsx__cdax = bodo.libs.array_item_arr_ext.get_offsets(data)
            whrx__ugpt = bodo.libs.array_item_arr_ext.get_data(data)
            whrx__ugpt = whrx__ugpt[:fsx__cdax[-1]]
            ejmvw__njs = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            xdvvv__bfizp = len(data)
            ttf__xmoam = np.empty(xdvvv__bfizp, np.uint32)
            mbp__ncb = xdvvv__bfizp + 7 >> 3
            for i in range(xdvvv__bfizp):
                ttf__xmoam[i] = fsx__cdax[i + 1] - fsx__cdax[i]
            recv_counts = gather_scalar(np.int32(xdvvv__bfizp), allgather,
                root=root)
            kypq__yui = recv_counts.sum()
            qbvtg__tlukd = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            znld__uol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                qbvtg__tlukd = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for uxwy__rhw in range(len(recv_counts)):
                    recv_counts_nulls[uxwy__rhw] = recv_counts[uxwy__rhw
                        ] + 7 >> 3
                znld__uol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            guutw__ltnp = np.empty(kypq__yui + 1, np.uint32)
            kssc__zgq = bodo.gatherv(whrx__ugpt, allgather, warn_if_rep, root)
            alnl__iykc = np.empty(kypq__yui + 7 >> 3, np.uint8)
            c_gatherv(ttf__xmoam.ctypes, np.int32(xdvvv__bfizp),
                guutw__ltnp.ctypes, recv_counts.ctypes, qbvtg__tlukd.ctypes,
                ice__ybn, allgather, np.int32(root))
            c_gatherv(ejmvw__njs.ctypes, np.int32(mbp__ncb), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, znld__uol.ctypes,
                wmyat__algy, allgather, np.int32(root))
            dummy_use(data)
            pnvms__dek = np.empty(kypq__yui + 1, np.uint64)
            convert_len_arr_to_offset(guutw__ltnp.ctypes, pnvms__dek.ctypes,
                kypq__yui)
            copy_gathered_null_bytes(alnl__iykc.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                kypq__yui, kssc__zgq, pnvms__dek, alnl__iykc)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        jcmj__zikk = data.names
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            sybxr__flqv = bodo.libs.struct_arr_ext.get_data(data)
            cibi__owivu = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            cgfrh__yej = bodo.gatherv(sybxr__flqv, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            xdvvv__bfizp = len(data)
            mbp__ncb = xdvvv__bfizp + 7 >> 3
            recv_counts = gather_scalar(np.int32(xdvvv__bfizp), allgather,
                root=root)
            kypq__yui = recv_counts.sum()
            syp__ccexe = np.empty(kypq__yui + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            znld__uol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                znld__uol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(cibi__owivu.ctypes, np.int32(mbp__ncb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, znld__uol.
                ctypes, wmyat__algy, allgather, np.int32(root))
            copy_gathered_null_bytes(syp__ccexe.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(cgfrh__yej,
                syp__ccexe, jcmj__zikk)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            owi__cri = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(owi__cri)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            owi__cri = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(owi__cri)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            owi__cri = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(owi__cri)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            owi__cri = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            eavr__xft = bodo.gatherv(data.indices, allgather, warn_if_rep, root
                )
            mfvpb__iqdc = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            assnq__qpus = gather_scalar(data.shape[0], allgather, root=root)
            czv__chtn = assnq__qpus.sum()
            mnlk__tndn = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            gby__apj = np.empty(czv__chtn + 1, np.int64)
            eavr__xft = eavr__xft.astype(np.int64)
            gby__apj[0] = 0
            gqnyl__xfots = 1
            kyl__nkhau = 0
            for bsl__zrjpo in assnq__qpus:
                for rvqz__lfraz in range(bsl__zrjpo):
                    igput__plaza = mfvpb__iqdc[kyl__nkhau + 1] - mfvpb__iqdc[
                        kyl__nkhau]
                    gby__apj[gqnyl__xfots] = gby__apj[gqnyl__xfots - 1
                        ] + igput__plaza
                    gqnyl__xfots += 1
                    kyl__nkhau += 1
                kyl__nkhau += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(owi__cri,
                eavr__xft, gby__apj, (czv__chtn, mnlk__tndn))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        wqj__ssrc = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        wqj__ssrc += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'bodo': bodo}, rgtnd__xmrgw)
        czp__ofswu = rgtnd__xmrgw['impl_tuple']
        return czp__ofswu
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    wqj__ssrc = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    wqj__ssrc += '    if random:\n'
    wqj__ssrc += '        if random_seed is None:\n'
    wqj__ssrc += '            random = 1\n'
    wqj__ssrc += '        else:\n'
    wqj__ssrc += '            random = 2\n'
    wqj__ssrc += '    if random_seed is None:\n'
    wqj__ssrc += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        lpn__wzh = data
        mnlk__tndn = len(lpn__wzh.columns)
        for i in range(mnlk__tndn):
            wqj__ssrc += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        wqj__ssrc += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        fbuv__luqva = ', '.join(f'data_{i}' for i in range(mnlk__tndn))
        wqj__ssrc += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(qfzr__ysrf) for
            qfzr__ysrf in range(mnlk__tndn))))
        wqj__ssrc += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        wqj__ssrc += '    if dests is None:\n'
        wqj__ssrc += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        wqj__ssrc += '    else:\n'
        wqj__ssrc += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for ewcq__vzs in range(mnlk__tndn):
            wqj__ssrc += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(ewcq__vzs))
        wqj__ssrc += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(mnlk__tndn))
        wqj__ssrc += '    delete_table(out_table)\n'
        wqj__ssrc += '    if parallel:\n'
        wqj__ssrc += '        delete_table(table_total)\n'
        fbuv__luqva = ', '.join('out_arr_{}'.format(i) for i in range(
            mnlk__tndn))
        qocv__djeb = bodo.utils.transform.gen_const_tup(lpn__wzh.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        wqj__ssrc += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(fbuv__luqva, index, qocv__djeb))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        wqj__ssrc += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        wqj__ssrc += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        wqj__ssrc += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        wqj__ssrc += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        wqj__ssrc += '    if dests is None:\n'
        wqj__ssrc += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        wqj__ssrc += '    else:\n'
        wqj__ssrc += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        wqj__ssrc += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        wqj__ssrc += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        wqj__ssrc += '    delete_table(out_table)\n'
        wqj__ssrc += '    if parallel:\n'
        wqj__ssrc += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        wqj__ssrc += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        wqj__ssrc += '    if not parallel:\n'
        wqj__ssrc += '        return data\n'
        wqj__ssrc += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        wqj__ssrc += '    if dests is None:\n'
        wqj__ssrc += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        wqj__ssrc += '    elif bodo.get_rank() not in dests:\n'
        wqj__ssrc += '        dim0_local_size = 0\n'
        wqj__ssrc += '    else:\n'
        wqj__ssrc += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        wqj__ssrc += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        wqj__ssrc += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        wqj__ssrc += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        wqj__ssrc += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        wqj__ssrc += '    if dests is None:\n'
        wqj__ssrc += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        wqj__ssrc += '    else:\n'
        wqj__ssrc += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        wqj__ssrc += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        wqj__ssrc += '    delete_table(out_table)\n'
        wqj__ssrc += '    if parallel:\n'
        wqj__ssrc += '        delete_table(table_total)\n'
        wqj__ssrc += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    rgtnd__xmrgw = {}
    exec(wqj__ssrc, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        rgtnd__xmrgw)
    impl = rgtnd__xmrgw['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    wqj__ssrc = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        wqj__ssrc += '    if seed is None:\n'
        wqj__ssrc += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        wqj__ssrc += '    np.random.seed(seed)\n'
        wqj__ssrc += '    if not parallel:\n'
        wqj__ssrc += '        data = data.copy()\n'
        wqj__ssrc += '        np.random.shuffle(data)\n'
        wqj__ssrc += '        return data\n'
        wqj__ssrc += '    else:\n'
        wqj__ssrc += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        wqj__ssrc += '        permutation = np.arange(dim0_global_size)\n'
        wqj__ssrc += '        np.random.shuffle(permutation)\n'
        wqj__ssrc += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        wqj__ssrc += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        wqj__ssrc += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        wqj__ssrc += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        wqj__ssrc += '        return output\n'
    else:
        wqj__ssrc += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    rgtnd__xmrgw = {}
    exec(wqj__ssrc, {'np': np, 'bodo': bodo}, rgtnd__xmrgw)
    impl = rgtnd__xmrgw['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    tekr__sdq = np.empty(sendcounts_nulls.sum(), np.uint8)
    yoeua__vuik = 0
    nqf__qhi = 0
    for boppv__fjgls in range(len(sendcounts)):
        wrdl__urs = sendcounts[boppv__fjgls]
        mbp__ncb = sendcounts_nulls[boppv__fjgls]
        wcpdc__gbpj = tekr__sdq[yoeua__vuik:yoeua__vuik + mbp__ncb]
        for ptx__lxrvz in range(wrdl__urs):
            set_bit_to_arr(wcpdc__gbpj, ptx__lxrvz, get_bit_bitmap(
                null_bitmap_ptr, nqf__qhi))
            nqf__qhi += 1
        yoeua__vuik += mbp__ncb
    return tekr__sdq


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    qmeh__dik = MPI.COMM_WORLD
    data = qmeh__dik.bcast(data, root)
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
    ezdv__fryl = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    wtzil__otwcr = (0,) * ezdv__fryl

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        urp__ixaa = np.ascontiguousarray(data)
        jdlff__wrcts = data.ctypes
        pdewd__rmiyr = wtzil__otwcr
        if rank == MPI_ROOT:
            pdewd__rmiyr = urp__ixaa.shape
        pdewd__rmiyr = bcast_tuple(pdewd__rmiyr)
        vfrnh__rmly = get_tuple_prod(pdewd__rmiyr[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            pdewd__rmiyr[0])
        send_counts *= vfrnh__rmly
        xdvvv__bfizp = send_counts[rank]
        cxgk__axedc = np.empty(xdvvv__bfizp, dtype)
        qbvtg__tlukd = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(jdlff__wrcts, send_counts.ctypes, qbvtg__tlukd.ctypes,
            cxgk__axedc.ctypes, np.int32(xdvvv__bfizp), np.int32(typ_val))
        return cxgk__axedc.reshape((-1,) + pdewd__rmiyr[1:])
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
        fxxq__zkh = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], fxxq__zkh)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        ufn__jgfw = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=ufn__jgfw)
        gcw__mvuz = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(gcw__mvuz)
        return pd.Index(arr, name=ufn__jgfw)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        ufn__jgfw = _get_name_value_for_type(dtype.name_typ)
        jcmj__zikk = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        txisw__kuwax = tuple(get_value_for_type(t) for t in dtype.array_types)
        txisw__kuwax = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in txisw__kuwax)
        val = pd.MultiIndex.from_arrays(txisw__kuwax, names=jcmj__zikk)
        val.name = ufn__jgfw
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        ufn__jgfw = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=ufn__jgfw)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        txisw__kuwax = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({ufn__jgfw: arr for ufn__jgfw, arr in zip(dtype
            .columns, txisw__kuwax)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        gcw__mvuz = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(gcw__mvuz[0], gcw__mvuz
            [0])])
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
        ice__ybn = np.int32(numba_to_c_type(types.int32))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            twwjg__oqrc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            twwjg__oqrc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        wqj__ssrc = f"""def impl(
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
            recv_arr = {twwjg__oqrc}(n_loc, n_loc_char)

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
        rgtnd__xmrgw = dict()
        exec(wqj__ssrc, {'bodo': bodo, 'np': np, 'int32_typ_enum': ice__ybn,
            'char_typ_enum': wmyat__algy, 'decode_if_dict_array':
            decode_if_dict_array}, rgtnd__xmrgw)
        impl = rgtnd__xmrgw['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        ice__ybn = np.int32(numba_to_c_type(types.int32))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            gruoz__ibjz = bodo.libs.array_item_arr_ext.get_offsets(data)
            spgj__rzlz = bodo.libs.array_item_arr_ext.get_data(data)
            spgj__rzlz = spgj__rzlz[:gruoz__ibjz[-1]]
            fbnd__vdmqb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            dicyp__lhgvv = bcast_scalar(len(data))
            tnxxd__uek = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                tnxxd__uek[i] = gruoz__ibjz[i + 1] - gruoz__ibjz[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                dicyp__lhgvv)
            qbvtg__tlukd = bodo.ir.join.calc_disp(send_counts)
            ewjy__rehtk = np.empty(n_pes, np.int32)
            if rank == 0:
                pmonh__kowev = 0
                for i in range(n_pes):
                    xguk__zgseb = 0
                    for rvqz__lfraz in range(send_counts[i]):
                        xguk__zgseb += tnxxd__uek[pmonh__kowev]
                        pmonh__kowev += 1
                    ewjy__rehtk[i] = xguk__zgseb
            bcast(ewjy__rehtk)
            krskl__kxha = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                krskl__kxha[i] = send_counts[i] + 7 >> 3
            znld__uol = bodo.ir.join.calc_disp(krskl__kxha)
            xdvvv__bfizp = send_counts[rank]
            nws__jpidh = np.empty(xdvvv__bfizp + 1, np_offset_type)
            jgtu__yxad = bodo.libs.distributed_api.scatterv_impl(spgj__rzlz,
                ewjy__rehtk)
            txkqq__qqlz = xdvvv__bfizp + 7 >> 3
            uhnc__day = np.empty(txkqq__qqlz, np.uint8)
            hxk__kgs = np.empty(xdvvv__bfizp, np.uint32)
            c_scatterv(tnxxd__uek.ctypes, send_counts.ctypes, qbvtg__tlukd.
                ctypes, hxk__kgs.ctypes, np.int32(xdvvv__bfizp), ice__ybn)
            convert_len_arr_to_offset(hxk__kgs.ctypes, nws__jpidh.ctypes,
                xdvvv__bfizp)
            thgqk__gzolg = get_scatter_null_bytes_buff(fbnd__vdmqb.ctypes,
                send_counts, krskl__kxha)
            c_scatterv(thgqk__gzolg.ctypes, krskl__kxha.ctypes, znld__uol.
                ctypes, uhnc__day.ctypes, np.int32(txkqq__qqlz), wmyat__algy)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                xdvvv__bfizp, jgtu__yxad, nws__jpidh, uhnc__day)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            ehwrk__zrq = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            ehwrk__zrq = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            ehwrk__zrq = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            ehwrk__zrq = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            urp__ixaa = data._data
            cibi__owivu = data._null_bitmap
            xsp__wnt = len(urp__ixaa)
            dbft__ehy = _scatterv_np(urp__ixaa, send_counts)
            dicyp__lhgvv = bcast_scalar(xsp__wnt)
            ldzzq__rppfl = len(dbft__ehy) + 7 >> 3
            ggdxy__feqo = np.empty(ldzzq__rppfl, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                dicyp__lhgvv)
            krskl__kxha = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                krskl__kxha[i] = send_counts[i] + 7 >> 3
            znld__uol = bodo.ir.join.calc_disp(krskl__kxha)
            thgqk__gzolg = get_scatter_null_bytes_buff(cibi__owivu.ctypes,
                send_counts, krskl__kxha)
            c_scatterv(thgqk__gzolg.ctypes, krskl__kxha.ctypes, znld__uol.
                ctypes, ggdxy__feqo.ctypes, np.int32(ldzzq__rppfl), wmyat__algy
                )
            return ehwrk__zrq(dbft__ehy, ggdxy__feqo)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            ktiwc__zyx = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            ywh__xyfwd = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(ktiwc__zyx,
                ywh__xyfwd)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            uzwjv__njz = data._step
            ufn__jgfw = data._name
            ufn__jgfw = bcast_scalar(ufn__jgfw)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            uzwjv__njz = bcast_scalar(uzwjv__njz)
            qsq__tqiw = bodo.libs.array_kernels.calc_nitems(start, stop,
                uzwjv__njz)
            chunk_start = bodo.libs.distributed_api.get_start(qsq__tqiw,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(qsq__tqiw,
                n_pes, rank)
            bhvoa__onf = start + uzwjv__njz * chunk_start
            nyomz__qnjs = start + uzwjv__njz * (chunk_start + chunk_count)
            nyomz__qnjs = min(nyomz__qnjs, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(bhvoa__onf,
                nyomz__qnjs, uzwjv__njz, ufn__jgfw)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        sdaau__cjffq = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            urp__ixaa = data._data
            ufn__jgfw = data._name
            ufn__jgfw = bcast_scalar(ufn__jgfw)
            arr = bodo.libs.distributed_api.scatterv_impl(urp__ixaa,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                ufn__jgfw, sdaau__cjffq)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            urp__ixaa = data._data
            ufn__jgfw = data._name
            ufn__jgfw = bcast_scalar(ufn__jgfw)
            arr = bodo.libs.distributed_api.scatterv_impl(urp__ixaa,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, ufn__jgfw)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            owi__cri = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            ufn__jgfw = bcast_scalar(data._name)
            jcmj__zikk = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(owi__cri,
                jcmj__zikk, ufn__jgfw)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ufn__jgfw = bodo.hiframes.pd_series_ext.get_series_name(data)
            bxs__klne = bcast_scalar(ufn__jgfw)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            wcsu__mgtlf = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                wcsu__mgtlf, bxs__klne)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mnlk__tndn = len(data.columns)
        fbuv__luqva = ', '.join('g_data_{}'.format(i) for i in range(
            mnlk__tndn))
        qocv__djeb = bodo.utils.transform.gen_const_tup(data.columns)
        wqj__ssrc = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        for i in range(mnlk__tndn):
            wqj__ssrc += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            wqj__ssrc += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        wqj__ssrc += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        wqj__ssrc += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        wqj__ssrc += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(fbuv__luqva, qocv__djeb))
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'bodo': bodo}, rgtnd__xmrgw)
        imd__vuwu = rgtnd__xmrgw['impl_df']
        return imd__vuwu
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            jtpej__dzf = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                jtpej__dzf, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        wqj__ssrc = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        wqj__ssrc += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'bodo': bodo}, rgtnd__xmrgw)
        czp__ofswu = rgtnd__xmrgw['impl_tuple']
        return czp__ofswu
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
        sygww__qepl = np.int32(numba_to_c_type(offset_type))
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            xdvvv__bfizp = len(data)
            dfz__qweq = num_total_chars(data)
            assert xdvvv__bfizp < INT_MAX
            assert dfz__qweq < INT_MAX
            afwb__qppl = get_offset_ptr(data)
            jdlff__wrcts = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            mbp__ncb = xdvvv__bfizp + 7 >> 3
            c_bcast(afwb__qppl, np.int32(xdvvv__bfizp + 1), sygww__qepl, np
                .array([-1]).ctypes, 0, np.int32(root))
            c_bcast(jdlff__wrcts, np.int32(dfz__qweq), wmyat__algy, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(mbp__ncb), wmyat__algy, np.
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
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                kkq__pzsm = 0
                zzd__ailh = np.empty(0, np.uint8).ctypes
            else:
                zzd__ailh, kkq__pzsm = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            kkq__pzsm = bodo.libs.distributed_api.bcast_scalar(kkq__pzsm, root)
            if rank != root:
                mrgid__wti = np.empty(kkq__pzsm + 1, np.uint8)
                mrgid__wti[kkq__pzsm] = 0
                zzd__ailh = mrgid__wti.ctypes
            c_bcast(zzd__ailh, np.int32(kkq__pzsm), wmyat__algy, np.array([
                -1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(zzd__ailh, kkq__pzsm)
        return impl_str
    typ_val = numba_to_c_type(val)
    wqj__ssrc = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    rgtnd__xmrgw = {}
    exec(wqj__ssrc, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, rgtnd__xmrgw)
    madz__qet = rgtnd__xmrgw['bcast_scalar_impl']
    return madz__qet


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    jwrqe__oza = len(val)
    wqj__ssrc = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    wqj__ssrc += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(jwrqe__oza)),
        ',' if jwrqe__oza else '')
    rgtnd__xmrgw = {}
    exec(wqj__ssrc, {'bcast_scalar': bcast_scalar}, rgtnd__xmrgw)
    emyzc__gpx = rgtnd__xmrgw['bcast_tuple_impl']
    return emyzc__gpx


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            xdvvv__bfizp = bcast_scalar(len(arr), root)
            buw__uhrdp = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(xdvvv__bfizp, buw__uhrdp)
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
        start = slice_index.start
        uzwjv__njz = slice_index.step
        gasc__htxp = 0 if uzwjv__njz == 1 or start > arr_start else abs(
            uzwjv__njz - arr_start % uzwjv__njz) % uzwjv__njz
        bhvoa__onf = max(arr_start, slice_index.start) - arr_start + gasc__htxp
        nyomz__qnjs = max(slice_index.stop - arr_start, 0)
        return slice(bhvoa__onf, nyomz__qnjs, uzwjv__njz)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        wbe__tocqw = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[wbe__tocqw])
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
        nvc__ehxof = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        wmyat__algy = np.int32(numba_to_c_type(types.uint8))
        wrm__wywu = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            ulgo__ggue = np.int32(10)
            tag = np.int32(11)
            bdh__qtrql = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                whrx__ugpt = arr._data
                ngi__bcekh = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    whrx__ugpt, ind)
                tdiaj__rqbl = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    whrx__ugpt, ind + 1)
                length = tdiaj__rqbl - ngi__bcekh
                gdpw__uefz = whrx__ugpt[ind]
                bdh__qtrql[0] = length
                isend(bdh__qtrql, np.int32(1), root, ulgo__ggue, True)
                isend(gdpw__uefz, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(wrm__wywu,
                nvc__ehxof, 0, 1)
            mdtp__odaux = 0
            if rank == root:
                mdtp__odaux = recv(np.int64, ANY_SOURCE, ulgo__ggue)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    wrm__wywu, nvc__ehxof, mdtp__odaux, 1)
                jdlff__wrcts = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(jdlff__wrcts, np.int32(mdtp__odaux), wmyat__algy,
                    ANY_SOURCE, tag)
            dummy_use(bdh__qtrql)
            mdtp__odaux = bcast_scalar(mdtp__odaux)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    wrm__wywu, nvc__ehxof, mdtp__odaux, 1)
            jdlff__wrcts = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(jdlff__wrcts, np.int32(mdtp__odaux), wmyat__algy, np.
                array([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, mdtp__odaux)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        inx__uhwyo = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, inx__uhwyo)
            if arr_start <= ind < arr_start + len(arr):
                jtpej__dzf = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = jtpej__dzf[ind - arr_start]
                send_arr = np.full(1, data, inx__uhwyo)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = inx__uhwyo(-1)
            if rank == root:
                val = recv(inx__uhwyo, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            cemc__epu = arr.dtype.categories[max(val, 0)]
            return cemc__epu
        return cat_getitem_impl
    hyat__cwn = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, hyat__cwn)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, hyat__cwn)[0]
        if rank == root:
            val = recv(hyat__cwn, ANY_SOURCE, tag)
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
    iqefv__aqkqo = get_type_enum(out_data)
    assert typ_enum == iqefv__aqkqo
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
    wqj__ssrc = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        wqj__ssrc += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    wqj__ssrc += '  return\n'
    rgtnd__xmrgw = {}
    exec(wqj__ssrc, {'alltoallv': alltoallv}, rgtnd__xmrgw)
    cin__vrxl = rgtnd__xmrgw['f']
    return cin__vrxl


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    tcq__fiqbg = total_size % pes
    jsyab__bsb = (total_size - tcq__fiqbg) // pes
    return rank * jsyab__bsb + min(rank, tcq__fiqbg)


@numba.njit
def get_end(total_size, pes, rank):
    tcq__fiqbg = total_size % pes
    jsyab__bsb = (total_size - tcq__fiqbg) // pes
    return (rank + 1) * jsyab__bsb + min(rank + 1, tcq__fiqbg)


@numba.njit
def get_node_portion(total_size, pes, rank):
    tcq__fiqbg = total_size % pes
    jsyab__bsb = (total_size - tcq__fiqbg) // pes
    if rank < tcq__fiqbg:
        return jsyab__bsb + 1
    else:
        return jsyab__bsb


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    wxt__vvmvr = in_arr.dtype(0)
    hjm__lmihi = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        xguk__zgseb = wxt__vvmvr
        for vrh__fcum in np.nditer(in_arr):
            xguk__zgseb += vrh__fcum.item()
        tnma__djbvr = dist_exscan(xguk__zgseb, hjm__lmihi)
        for i in range(in_arr.size):
            tnma__djbvr += in_arr[i]
            out_arr[i] = tnma__djbvr
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    nqse__myecf = in_arr.dtype(1)
    hjm__lmihi = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        xguk__zgseb = nqse__myecf
        for vrh__fcum in np.nditer(in_arr):
            xguk__zgseb *= vrh__fcum.item()
        tnma__djbvr = dist_exscan(xguk__zgseb, hjm__lmihi)
        if get_rank() == 0:
            tnma__djbvr = nqse__myecf
        for i in range(in_arr.size):
            tnma__djbvr *= in_arr[i]
            out_arr[i] = tnma__djbvr
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        nqse__myecf = np.finfo(in_arr.dtype(1).dtype).max
    else:
        nqse__myecf = np.iinfo(in_arr.dtype(1).dtype).max
    hjm__lmihi = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        xguk__zgseb = nqse__myecf
        for vrh__fcum in np.nditer(in_arr):
            xguk__zgseb = min(xguk__zgseb, vrh__fcum.item())
        tnma__djbvr = dist_exscan(xguk__zgseb, hjm__lmihi)
        if get_rank() == 0:
            tnma__djbvr = nqse__myecf
        for i in range(in_arr.size):
            tnma__djbvr = min(tnma__djbvr, in_arr[i])
            out_arr[i] = tnma__djbvr
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        nqse__myecf = np.finfo(in_arr.dtype(1).dtype).min
    else:
        nqse__myecf = np.iinfo(in_arr.dtype(1).dtype).min
    nqse__myecf = in_arr.dtype(1)
    hjm__lmihi = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        xguk__zgseb = nqse__myecf
        for vrh__fcum in np.nditer(in_arr):
            xguk__zgseb = max(xguk__zgseb, vrh__fcum.item())
        tnma__djbvr = dist_exscan(xguk__zgseb, hjm__lmihi)
        if get_rank() == 0:
            tnma__djbvr = nqse__myecf
        for i in range(in_arr.size):
            tnma__djbvr = max(tnma__djbvr, in_arr[i])
            out_arr[i] = tnma__djbvr
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    mnde__vtc = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), mnde__vtc)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    wgij__aqd = args[0]
    if equiv_set.has_shape(wgij__aqd):
        return ArrayAnalysis.AnalyzeResult(shape=wgij__aqd, pre=[])
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
    fsmes__kls = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, vfz__sanl in enumerate(args) if is_array_typ(vfz__sanl) or
        isinstance(vfz__sanl, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    wqj__ssrc = f"""def impl(*args):
    if {fsmes__kls} or bodo.get_rank() == 0:
        print(*args)"""
    rgtnd__xmrgw = {}
    exec(wqj__ssrc, globals(), rgtnd__xmrgw)
    impl = rgtnd__xmrgw['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        iawi__zjp = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        wqj__ssrc = 'def f(req, cond=True):\n'
        wqj__ssrc += f'  return {iawi__zjp}\n'
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'_wait': _wait}, rgtnd__xmrgw)
        impl = rgtnd__xmrgw['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


class ReqArrayType(types.Type):

    def __init__(self):
        super(ReqArrayType, self).__init__(name='ReqArrayType()')


req_array_type = ReqArrayType()
register_model(ReqArrayType)(models.OpaqueModel)
waitall = types.ExternalFunction('dist_waitall', types.void(types.int32,
    req_array_type))
comm_req_alloc = types.ExternalFunction('comm_req_alloc', req_array_type(
    types.int32))
comm_req_dealloc = types.ExternalFunction('comm_req_dealloc', types.void(
    req_array_type))
req_array_setitem = types.ExternalFunction('req_array_setitem', types.void(
    req_array_type, types.int64, mpi_req_numba_type))


@overload(operator.setitem, no_unliteral=True)
def overload_req_arr_setitem(A, idx, val):
    if A == req_array_type:
        assert val == mpi_req_numba_type
        return lambda A, idx, val: req_array_setitem(A, idx, val)


@numba.njit
def _get_local_range(start, stop, chunk_start, chunk_count):
    assert start >= 0 and stop > 0
    bhvoa__onf = max(start, chunk_start)
    nyomz__qnjs = min(stop, chunk_start + chunk_count)
    texox__wmoa = bhvoa__onf - chunk_start
    sske__kux = nyomz__qnjs - chunk_start
    if texox__wmoa < 0 or sske__kux < 0:
        texox__wmoa = 1
        sske__kux = 0
    return texox__wmoa, sske__kux


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
        tcq__fiqbg = 1
        for a in t:
            tcq__fiqbg *= a
        return tcq__fiqbg
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    busn__lol = np.ascontiguousarray(in_arr)
    kyqb__xnndw = get_tuple_prod(busn__lol.shape[1:])
    owawj__qmez = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        vuf__tygnw = np.array(dest_ranks, dtype=np.int32)
    else:
        vuf__tygnw = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, busn__lol.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * owawj__qmez, dtype_size * kyqb__xnndw,
        len(vuf__tygnw), vuf__tygnw.ctypes)
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
    siwr__gkgu = np.ascontiguousarray(rhs)
    bknvv__ojl = get_tuple_prod(siwr__gkgu.shape[1:])
    dtvx__ieekk = dtype_size * bknvv__ojl
    permutation_array_index(lhs.ctypes, lhs_len, dtvx__ieekk, siwr__gkgu.
        ctypes, siwr__gkgu.shape[0], p.ctypes, p_len)
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
        wqj__ssrc = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, rgtnd__xmrgw)
        madz__qet = rgtnd__xmrgw['bcast_scalar_impl']
        return madz__qet
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mnlk__tndn = len(data.columns)
        fbuv__luqva = ', '.join('g_data_{}'.format(i) for i in range(
            mnlk__tndn))
        qocv__djeb = bodo.utils.transform.gen_const_tup(data.columns)
        wqj__ssrc = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(mnlk__tndn):
            wqj__ssrc += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            wqj__ssrc += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        wqj__ssrc += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        wqj__ssrc += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        wqj__ssrc += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(fbuv__luqva, qocv__djeb))
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'bodo': bodo}, rgtnd__xmrgw)
        imd__vuwu = rgtnd__xmrgw['impl_df']
        return imd__vuwu
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            uzwjv__njz = data._step
            ufn__jgfw = data._name
            ufn__jgfw = bcast_scalar(ufn__jgfw, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            uzwjv__njz = bcast_scalar(uzwjv__njz, root)
            qsq__tqiw = bodo.libs.array_kernels.calc_nitems(start, stop,
                uzwjv__njz)
            chunk_start = bodo.libs.distributed_api.get_start(qsq__tqiw,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(qsq__tqiw,
                n_pes, rank)
            bhvoa__onf = start + uzwjv__njz * chunk_start
            nyomz__qnjs = start + uzwjv__njz * (chunk_start + chunk_count)
            nyomz__qnjs = min(nyomz__qnjs, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(bhvoa__onf,
                nyomz__qnjs, uzwjv__njz, ufn__jgfw)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            urp__ixaa = data._data
            ufn__jgfw = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(urp__ixaa,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, ufn__jgfw)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ufn__jgfw = bodo.hiframes.pd_series_ext.get_series_name(data)
            bxs__klne = bodo.libs.distributed_api.bcast_comm_impl(ufn__jgfw,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            wcsu__mgtlf = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                wcsu__mgtlf, bxs__klne)
        return impl_series
    if isinstance(data, types.BaseTuple):
        wqj__ssrc = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        wqj__ssrc += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        rgtnd__xmrgw = {}
        exec(wqj__ssrc, {'bcast_comm_impl': bcast_comm_impl}, rgtnd__xmrgw)
        czp__ofswu = rgtnd__xmrgw['impl_tuple']
        return czp__ofswu
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    ezdv__fryl = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    wtzil__otwcr = (0,) * ezdv__fryl

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        urp__ixaa = np.ascontiguousarray(data)
        jdlff__wrcts = data.ctypes
        pdewd__rmiyr = wtzil__otwcr
        if rank == root:
            pdewd__rmiyr = urp__ixaa.shape
        pdewd__rmiyr = bcast_tuple(pdewd__rmiyr, root)
        vfrnh__rmly = get_tuple_prod(pdewd__rmiyr[1:])
        send_counts = pdewd__rmiyr[0] * vfrnh__rmly
        cxgk__axedc = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(jdlff__wrcts, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(cxgk__axedc.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return cxgk__axedc.reshape((-1,) + pdewd__rmiyr[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        qmeh__dik = MPI.COMM_WORLD
        beul__tldlj = MPI.Get_processor_name()
        tllvi__hhhzg = qmeh__dik.allgather(beul__tldlj)
        node_ranks = defaultdict(list)
        for i, abs__vlic in enumerate(tllvi__hhhzg):
            node_ranks[abs__vlic].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    qmeh__dik = MPI.COMM_WORLD
    gyn__auhkc = qmeh__dik.Get_group()
    qoj__ecfqg = gyn__auhkc.Incl(comm_ranks)
    efn__jgp = qmeh__dik.Create_group(qoj__ecfqg)
    return efn__jgp


def get_nodes_first_ranks():
    gfi__stdnt = get_host_ranks()
    return np.array([krb__scsvh[0] for krb__scsvh in gfi__stdnt.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
