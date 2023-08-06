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
    ujk__cfhh = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, ujk__cfhh, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    ujk__cfhh = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, ujk__cfhh, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            ujk__cfhh = get_type_enum(arr)
            return _isend(arr.ctypes, size, ujk__cfhh, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        ujk__cfhh = np.int32(numba_to_c_type(arr.dtype))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            eyp__pdsqc = size + 7 >> 3
            okdd__tkam = _isend(arr._data.ctypes, size, ujk__cfhh, pe, tag,
                cond)
            cqv__vpuqg = _isend(arr._null_bitmap.ctypes, eyp__pdsqc,
                tgsq__qah, pe, tag, cond)
            return okdd__tkam, cqv__vpuqg
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        hiwu__mbh = np.int32(numba_to_c_type(offset_type))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            xmuzj__czt = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(xmuzj__czt, pe, tag - 1)
            eyp__pdsqc = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                hiwu__mbh, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), xmuzj__czt,
                tgsq__qah, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                eyp__pdsqc, tgsq__qah, pe, tag)
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
            ujk__cfhh = get_type_enum(arr)
            return _irecv(arr.ctypes, size, ujk__cfhh, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        ujk__cfhh = np.int32(numba_to_c_type(arr.dtype))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            eyp__pdsqc = size + 7 >> 3
            okdd__tkam = _irecv(arr._data.ctypes, size, ujk__cfhh, pe, tag,
                cond)
            cqv__vpuqg = _irecv(arr._null_bitmap.ctypes, eyp__pdsqc,
                tgsq__qah, pe, tag, cond)
            return okdd__tkam, cqv__vpuqg
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        hiwu__mbh = np.int32(numba_to_c_type(offset_type))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            nnmzl__ukzq = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            nnmzl__ukzq = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        ujt__izvv = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {nnmzl__ukzq}(size, n_chars)
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
        ghx__hqgc = dict()
        exec(ujt__izvv, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            hiwu__mbh, 'char_typ_enum': tgsq__qah}, ghx__hqgc)
        impl = ghx__hqgc['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    ujk__cfhh = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), ujk__cfhh)


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
        rflsp__hdvs = n_pes if rank == root or allgather else 0
        mzrm__gks = np.empty(rflsp__hdvs, dtype)
        c_gather_scalar(send.ctypes, mzrm__gks.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return mzrm__gks
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
        uqu__brji = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], uqu__brji)
        return builder.bitcast(uqu__brji, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        uqu__brji = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(uqu__brji)
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
    kzplv__kquh = types.unliteral(value)
    if isinstance(kzplv__kquh, IndexValueType):
        kzplv__kquh = kzplv__kquh.val_typ
        fwg__dsbyf = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            fwg__dsbyf.append(types.int64)
            fwg__dsbyf.append(bodo.datetime64ns)
            fwg__dsbyf.append(bodo.timedelta64ns)
            fwg__dsbyf.append(bodo.datetime_date_type)
        if kzplv__kquh not in fwg__dsbyf:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(kzplv__kquh))
    typ_enum = np.int32(numba_to_c_type(kzplv__kquh))

    def impl(value, reduce_op):
        xyrw__wya = value_to_ptr(value)
        dksdz__pockc = value_to_ptr(value)
        _dist_reduce(xyrw__wya, dksdz__pockc, reduce_op, typ_enum)
        return load_val_ptr(dksdz__pockc, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    kzplv__kquh = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(kzplv__kquh))
    cgghv__mrw = kzplv__kquh(0)

    def impl(value, reduce_op):
        xyrw__wya = value_to_ptr(value)
        dksdz__pockc = value_to_ptr(cgghv__mrw)
        _dist_exscan(xyrw__wya, dksdz__pockc, reduce_op, typ_enum)
        return load_val_ptr(dksdz__pockc, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    hbe__kuerx = 0
    dfyax__kldxo = 0
    for i in range(len(recv_counts)):
        wtq__eyysn = recv_counts[i]
        eyp__pdsqc = recv_counts_nulls[i]
        bheq__ogf = tmp_null_bytes[hbe__kuerx:hbe__kuerx + eyp__pdsqc]
        for qqngw__cgi in range(wtq__eyysn):
            set_bit_to(null_bitmap_ptr, dfyax__kldxo, get_bit(bheq__ogf,
                qqngw__cgi))
            dfyax__kldxo += 1
        hbe__kuerx += eyp__pdsqc


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            rwe__lylus = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                rwe__lylus, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            pqa__keyy = data.size
            recv_counts = gather_scalar(np.int32(pqa__keyy), allgather,
                root=root)
            igjib__crwss = recv_counts.sum()
            cvte__rgdx = empty_like_type(igjib__crwss, data)
            axedk__nhq = np.empty(1, np.int32)
            if rank == root or allgather:
                axedk__nhq = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(pqa__keyy), cvte__rgdx.ctypes,
                recv_counts.ctypes, axedk__nhq.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return cvte__rgdx.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            cvte__rgdx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(cvte__rgdx)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            cvte__rgdx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(cvte__rgdx)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pqa__keyy = len(data)
            eyp__pdsqc = pqa__keyy + 7 >> 3
            recv_counts = gather_scalar(np.int32(pqa__keyy), allgather,
                root=root)
            igjib__crwss = recv_counts.sum()
            cvte__rgdx = empty_like_type(igjib__crwss, data)
            axedk__nhq = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            owwvd__kxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                axedk__nhq = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                owwvd__kxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(pqa__keyy),
                cvte__rgdx._days_data.ctypes, recv_counts.ctypes,
                axedk__nhq.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._seconds_data.ctypes, np.int32(pqa__keyy),
                cvte__rgdx._seconds_data.ctypes, recv_counts.ctypes,
                axedk__nhq.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(pqa__keyy),
                cvte__rgdx._microseconds_data.ctypes, recv_counts.ctypes,
                axedk__nhq.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(eyp__pdsqc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, owwvd__kxc
                .ctypes, tgsq__qah, allgather, np.int32(root))
            copy_gathered_null_bytes(cvte__rgdx._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return cvte__rgdx
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pqa__keyy = len(data)
            eyp__pdsqc = pqa__keyy + 7 >> 3
            recv_counts = gather_scalar(np.int32(pqa__keyy), allgather,
                root=root)
            igjib__crwss = recv_counts.sum()
            cvte__rgdx = empty_like_type(igjib__crwss, data)
            axedk__nhq = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            owwvd__kxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                axedk__nhq = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                owwvd__kxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(pqa__keyy), cvte__rgdx.
                _data.ctypes, recv_counts.ctypes, axedk__nhq.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(eyp__pdsqc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, owwvd__kxc
                .ctypes, tgsq__qah, allgather, np.int32(root))
            copy_gathered_null_bytes(cvte__rgdx._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return cvte__rgdx
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        mou__gul = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            qvxu__rrmxk = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                qvxu__rrmxk, mou__gul)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            fsyqi__oauoh = bodo.gatherv(data._left, allgather, warn_if_rep,
                root)
            akrf__xnzx = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(fsyqi__oauoh,
                akrf__xnzx)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ihx__mvsd = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            fikt__vws = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fikt__vws, ihx__mvsd)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        spcpc__iion = np.iinfo(np.int64).max
        oxuqy__bzuw = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = spcpc__iion
                stop = oxuqy__bzuw
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == spcpc__iion and stop == oxuqy__bzuw:
                start = 0
                stop = 0
            wzim__noqh = max(0, -(-(stop - start) // data._step))
            if wzim__noqh < total_len:
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
            pdete__mbv = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, pdete__mbv)
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
            cvte__rgdx = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(cvte__rgdx
                , data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        vtqbj__yepxr = {'bodo': bodo, 'get_table_block': bodo.hiframes.
            table.get_table_block, 'ensure_column_unboxed': bodo.hiframes.
            table.ensure_column_unboxed, 'set_table_block': bodo.hiframes.
            table.set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        ujt__izvv = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        ujt__izvv += '  T = data\n'
        ujt__izvv += '  T2 = init_table(T, True)\n'
        for pzol__gajyf in data.type_to_blk.values():
            vtqbj__yepxr[f'arr_inds_{pzol__gajyf}'] = np.array(data.
                block_to_arr_ind[pzol__gajyf], dtype=np.int64)
            ujt__izvv += (
                f'  arr_list_{pzol__gajyf} = get_table_block(T, {pzol__gajyf})\n'
                )
            ujt__izvv += f"""  out_arr_list_{pzol__gajyf} = alloc_list_like(arr_list_{pzol__gajyf}, True)
"""
            ujt__izvv += f'  for i in range(len(arr_list_{pzol__gajyf})):\n'
            ujt__izvv += (
                f'    arr_ind_{pzol__gajyf} = arr_inds_{pzol__gajyf}[i]\n')
            ujt__izvv += f"""    ensure_column_unboxed(T, arr_list_{pzol__gajyf}, i, arr_ind_{pzol__gajyf})
"""
            ujt__izvv += f"""    out_arr_{pzol__gajyf} = bodo.gatherv(arr_list_{pzol__gajyf}[i], allgather, warn_if_rep, root)
"""
            ujt__izvv += (
                f'    out_arr_list_{pzol__gajyf}[i] = out_arr_{pzol__gajyf}\n')
            ujt__izvv += (
                f'  T2 = set_table_block(T2, out_arr_list_{pzol__gajyf}, {pzol__gajyf})\n'
                )
        ujt__izvv += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        ujt__izvv += f'  T2 = set_table_len(T2, length)\n'
        ujt__izvv += f'  return T2\n'
        ghx__hqgc = {}
        exec(ujt__izvv, vtqbj__yepxr, ghx__hqgc)
        odlfn__breqd = ghx__hqgc['impl_table']
        return odlfn__breqd
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xqb__dfpue = len(data.columns)
        if xqb__dfpue == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                yyp__ozv = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    yyp__ozv, ())
            return impl
        kmbbg__xvmp = ', '.join(f'g_data_{i}' for i in range(xqb__dfpue))
        juk__xhpm = bodo.utils.transform.gen_const_tup(data.columns)
        ujt__izvv = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            bpvt__qirxe = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            vtqbj__yepxr = {'bodo': bodo, 'df_type': bpvt__qirxe}
            kmbbg__xvmp = 'T2'
            juk__xhpm = 'df_type'
            ujt__izvv += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            ujt__izvv += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            vtqbj__yepxr = {'bodo': bodo}
            for i in range(xqb__dfpue):
                ujt__izvv += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                ujt__izvv += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        ujt__izvv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        ujt__izvv += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        ujt__izvv += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(kmbbg__xvmp, juk__xhpm))
        ghx__hqgc = {}
        exec(ujt__izvv, vtqbj__yepxr, ghx__hqgc)
        asis__pdxnb = ghx__hqgc['impl_df']
        return asis__pdxnb
    if isinstance(data, ArrayItemArrayType):
        nxsoy__vrp = np.int32(numba_to_c_type(types.int32))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            ukkvx__dcq = bodo.libs.array_item_arr_ext.get_offsets(data)
            jyrq__kkq = bodo.libs.array_item_arr_ext.get_data(data)
            jyrq__kkq = jyrq__kkq[:ukkvx__dcq[-1]]
            nvhe__tdzhb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            pqa__keyy = len(data)
            mzi__cjahy = np.empty(pqa__keyy, np.uint32)
            eyp__pdsqc = pqa__keyy + 7 >> 3
            for i in range(pqa__keyy):
                mzi__cjahy[i] = ukkvx__dcq[i + 1] - ukkvx__dcq[i]
            recv_counts = gather_scalar(np.int32(pqa__keyy), allgather,
                root=root)
            igjib__crwss = recv_counts.sum()
            axedk__nhq = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            owwvd__kxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                axedk__nhq = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for usf__mae in range(len(recv_counts)):
                    recv_counts_nulls[usf__mae] = recv_counts[usf__mae
                        ] + 7 >> 3
                owwvd__kxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            azncf__rsin = np.empty(igjib__crwss + 1, np.uint32)
            tohen__higze = bodo.gatherv(jyrq__kkq, allgather, warn_if_rep, root
                )
            rzuac__cuvy = np.empty(igjib__crwss + 7 >> 3, np.uint8)
            c_gatherv(mzi__cjahy.ctypes, np.int32(pqa__keyy), azncf__rsin.
                ctypes, recv_counts.ctypes, axedk__nhq.ctypes, nxsoy__vrp,
                allgather, np.int32(root))
            c_gatherv(nvhe__tdzhb.ctypes, np.int32(eyp__pdsqc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, owwvd__kxc
                .ctypes, tgsq__qah, allgather, np.int32(root))
            dummy_use(data)
            soc__zuec = np.empty(igjib__crwss + 1, np.uint64)
            convert_len_arr_to_offset(azncf__rsin.ctypes, soc__zuec.ctypes,
                igjib__crwss)
            copy_gathered_null_bytes(rzuac__cuvy.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                igjib__crwss, tohen__higze, soc__zuec, rzuac__cuvy)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        cgiih__kapdg = data.names
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            bztw__lub = bodo.libs.struct_arr_ext.get_data(data)
            ddr__pth = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            bzu__kudzb = bodo.gatherv(bztw__lub, allgather=allgather, root=root
                )
            rank = bodo.libs.distributed_api.get_rank()
            pqa__keyy = len(data)
            eyp__pdsqc = pqa__keyy + 7 >> 3
            recv_counts = gather_scalar(np.int32(pqa__keyy), allgather,
                root=root)
            igjib__crwss = recv_counts.sum()
            kmsf__ihpkx = np.empty(igjib__crwss + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            owwvd__kxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                owwvd__kxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(ddr__pth.ctypes, np.int32(eyp__pdsqc), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, owwvd__kxc.ctypes,
                tgsq__qah, allgather, np.int32(root))
            copy_gathered_null_bytes(kmsf__ihpkx.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(bzu__kudzb,
                kmsf__ihpkx, cgiih__kapdg)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            cvte__rgdx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(cvte__rgdx)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cvte__rgdx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(cvte__rgdx)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            cvte__rgdx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(cvte__rgdx)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cvte__rgdx = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            ihq__wiojs = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            dpqcb__sed = bodo.gatherv(data.indptr, allgather, warn_if_rep, root
                )
            lrsis__mfztt = gather_scalar(data.shape[0], allgather, root=root)
            lksn__nrtc = lrsis__mfztt.sum()
            xqb__dfpue = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            ayce__darh = np.empty(lksn__nrtc + 1, np.int64)
            ihq__wiojs = ihq__wiojs.astype(np.int64)
            ayce__darh[0] = 0
            akb__ttojo = 1
            klraq__egttg = 0
            for ynwv__gme in lrsis__mfztt:
                for ahzb__haey in range(ynwv__gme):
                    gqo__qdf = dpqcb__sed[klraq__egttg + 1] - dpqcb__sed[
                        klraq__egttg]
                    ayce__darh[akb__ttojo] = ayce__darh[akb__ttojo - 1
                        ] + gqo__qdf
                    akb__ttojo += 1
                    klraq__egttg += 1
                klraq__egttg += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(cvte__rgdx,
                ihq__wiojs, ayce__darh, (lksn__nrtc, xqb__dfpue))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        ujt__izvv = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        ujt__izvv += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        ghx__hqgc = {}
        exec(ujt__izvv, {'bodo': bodo}, ghx__hqgc)
        cujla__oud = ghx__hqgc['impl_tuple']
        return cujla__oud
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    ujt__izvv = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    ujt__izvv += '    if random:\n'
    ujt__izvv += '        if random_seed is None:\n'
    ujt__izvv += '            random = 1\n'
    ujt__izvv += '        else:\n'
    ujt__izvv += '            random = 2\n'
    ujt__izvv += '    if random_seed is None:\n'
    ujt__izvv += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        hqhzj__azeiz = data
        xqb__dfpue = len(hqhzj__azeiz.columns)
        for i in range(xqb__dfpue):
            ujt__izvv += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        ujt__izvv += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        kmbbg__xvmp = ', '.join(f'data_{i}' for i in range(xqb__dfpue))
        ujt__izvv += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(oest__aajrw) for
            oest__aajrw in range(xqb__dfpue))))
        ujt__izvv += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        ujt__izvv += '    if dests is None:\n'
        ujt__izvv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        ujt__izvv += '    else:\n'
        ujt__izvv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for nes__ykx in range(xqb__dfpue):
            ujt__izvv += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(nes__ykx))
        ujt__izvv += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(xqb__dfpue))
        ujt__izvv += '    delete_table(out_table)\n'
        ujt__izvv += '    if parallel:\n'
        ujt__izvv += '        delete_table(table_total)\n'
        kmbbg__xvmp = ', '.join('out_arr_{}'.format(i) for i in range(
            xqb__dfpue))
        juk__xhpm = bodo.utils.transform.gen_const_tup(hqhzj__azeiz.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        ujt__izvv += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(kmbbg__xvmp, index, juk__xhpm))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        ujt__izvv += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        ujt__izvv += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        ujt__izvv += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        ujt__izvv += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        ujt__izvv += '    if dests is None:\n'
        ujt__izvv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        ujt__izvv += '    else:\n'
        ujt__izvv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        ujt__izvv += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        ujt__izvv += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        ujt__izvv += '    delete_table(out_table)\n'
        ujt__izvv += '    if parallel:\n'
        ujt__izvv += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        ujt__izvv += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        ujt__izvv += '    if not parallel:\n'
        ujt__izvv += '        return data\n'
        ujt__izvv += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        ujt__izvv += '    if dests is None:\n'
        ujt__izvv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        ujt__izvv += '    elif bodo.get_rank() not in dests:\n'
        ujt__izvv += '        dim0_local_size = 0\n'
        ujt__izvv += '    else:\n'
        ujt__izvv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        ujt__izvv += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        ujt__izvv += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        ujt__izvv += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        ujt__izvv += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        ujt__izvv += '    if dests is None:\n'
        ujt__izvv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        ujt__izvv += '    else:\n'
        ujt__izvv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        ujt__izvv += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        ujt__izvv += '    delete_table(out_table)\n'
        ujt__izvv += '    if parallel:\n'
        ujt__izvv += '        delete_table(table_total)\n'
        ujt__izvv += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    ghx__hqgc = {}
    exec(ujt__izvv, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}, ghx__hqgc
        )
    impl = ghx__hqgc['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    ujt__izvv = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        ujt__izvv += '    if seed is None:\n'
        ujt__izvv += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        ujt__izvv += '    np.random.seed(seed)\n'
        ujt__izvv += '    if not parallel:\n'
        ujt__izvv += '        data = data.copy()\n'
        ujt__izvv += '        np.random.shuffle(data)\n'
        ujt__izvv += '        return data\n'
        ujt__izvv += '    else:\n'
        ujt__izvv += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        ujt__izvv += '        permutation = np.arange(dim0_global_size)\n'
        ujt__izvv += '        np.random.shuffle(permutation)\n'
        ujt__izvv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        ujt__izvv += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        ujt__izvv += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        ujt__izvv += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        ujt__izvv += '        return output\n'
    else:
        ujt__izvv += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    ghx__hqgc = {}
    exec(ujt__izvv, {'np': np, 'bodo': bodo}, ghx__hqgc)
    impl = ghx__hqgc['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    vubii__zpsln = np.empty(sendcounts_nulls.sum(), np.uint8)
    hbe__kuerx = 0
    dfyax__kldxo = 0
    for aubyg__dpvo in range(len(sendcounts)):
        wtq__eyysn = sendcounts[aubyg__dpvo]
        eyp__pdsqc = sendcounts_nulls[aubyg__dpvo]
        bheq__ogf = vubii__zpsln[hbe__kuerx:hbe__kuerx + eyp__pdsqc]
        for qqngw__cgi in range(wtq__eyysn):
            set_bit_to_arr(bheq__ogf, qqngw__cgi, get_bit_bitmap(
                null_bitmap_ptr, dfyax__kldxo))
            dfyax__kldxo += 1
        hbe__kuerx += eyp__pdsqc
    return vubii__zpsln


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    kbcmo__ctu = MPI.COMM_WORLD
    data = kbcmo__ctu.bcast(data, root)
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
    wyin__lyjvt = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    blrwg__cmq = (0,) * wyin__lyjvt

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        fqsim__sdz = np.ascontiguousarray(data)
        wmvzz__ralvp = data.ctypes
        nynrf__gaknh = blrwg__cmq
        if rank == MPI_ROOT:
            nynrf__gaknh = fqsim__sdz.shape
        nynrf__gaknh = bcast_tuple(nynrf__gaknh)
        qldxx__cvxi = get_tuple_prod(nynrf__gaknh[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            nynrf__gaknh[0])
        send_counts *= qldxx__cvxi
        pqa__keyy = send_counts[rank]
        shvoj__eee = np.empty(pqa__keyy, dtype)
        axedk__nhq = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(wmvzz__ralvp, send_counts.ctypes, axedk__nhq.ctypes,
            shvoj__eee.ctypes, np.int32(pqa__keyy), np.int32(typ_val))
        return shvoj__eee.reshape((-1,) + nynrf__gaknh[1:])
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
        mos__icx = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], mos__icx)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        ihx__mvsd = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=ihx__mvsd)
        xeks__abws = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(xeks__abws)
        return pd.Index(arr, name=ihx__mvsd)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        ihx__mvsd = _get_name_value_for_type(dtype.name_typ)
        cgiih__kapdg = tuple(_get_name_value_for_type(t) for t in dtype.
            names_typ)
        lyvgx__iyu = tuple(get_value_for_type(t) for t in dtype.array_types)
        lyvgx__iyu = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in lyvgx__iyu)
        val = pd.MultiIndex.from_arrays(lyvgx__iyu, names=cgiih__kapdg)
        val.name = ihx__mvsd
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        ihx__mvsd = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=ihx__mvsd)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        lyvgx__iyu = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({ihx__mvsd: arr for ihx__mvsd, arr in zip(dtype
            .columns, lyvgx__iyu)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        xeks__abws = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(xeks__abws[0],
            xeks__abws[0])])
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
        nxsoy__vrp = np.int32(numba_to_c_type(types.int32))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            nnmzl__ukzq = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            nnmzl__ukzq = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        ujt__izvv = f"""def impl(
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
            recv_arr = {nnmzl__ukzq}(n_loc, n_loc_char)

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
        ghx__hqgc = dict()
        exec(ujt__izvv, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            nxsoy__vrp, 'char_typ_enum': tgsq__qah, 'decode_if_dict_array':
            decode_if_dict_array}, ghx__hqgc)
        impl = ghx__hqgc['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        nxsoy__vrp = np.int32(numba_to_c_type(types.int32))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            acrxb__gxip = bodo.libs.array_item_arr_ext.get_offsets(data)
            tkm__wqsxm = bodo.libs.array_item_arr_ext.get_data(data)
            tkm__wqsxm = tkm__wqsxm[:acrxb__gxip[-1]]
            tsx__srtd = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            ekl__xzkp = bcast_scalar(len(data))
            ofib__bwtfe = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                ofib__bwtfe[i] = acrxb__gxip[i + 1] - acrxb__gxip[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                ekl__xzkp)
            axedk__nhq = bodo.ir.join.calc_disp(send_counts)
            qoi__eimd = np.empty(n_pes, np.int32)
            if rank == 0:
                vtcyt__bljq = 0
                for i in range(n_pes):
                    jhgwa__awqm = 0
                    for ahzb__haey in range(send_counts[i]):
                        jhgwa__awqm += ofib__bwtfe[vtcyt__bljq]
                        vtcyt__bljq += 1
                    qoi__eimd[i] = jhgwa__awqm
            bcast(qoi__eimd)
            pprej__cjhvq = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                pprej__cjhvq[i] = send_counts[i] + 7 >> 3
            owwvd__kxc = bodo.ir.join.calc_disp(pprej__cjhvq)
            pqa__keyy = send_counts[rank]
            klyyf__bmxj = np.empty(pqa__keyy + 1, np_offset_type)
            nqz__lujr = bodo.libs.distributed_api.scatterv_impl(tkm__wqsxm,
                qoi__eimd)
            nei__cgjci = pqa__keyy + 7 >> 3
            pku__dlgac = np.empty(nei__cgjci, np.uint8)
            dbow__fxzup = np.empty(pqa__keyy, np.uint32)
            c_scatterv(ofib__bwtfe.ctypes, send_counts.ctypes, axedk__nhq.
                ctypes, dbow__fxzup.ctypes, np.int32(pqa__keyy), nxsoy__vrp)
            convert_len_arr_to_offset(dbow__fxzup.ctypes, klyyf__bmxj.
                ctypes, pqa__keyy)
            chyi__azxw = get_scatter_null_bytes_buff(tsx__srtd.ctypes,
                send_counts, pprej__cjhvq)
            c_scatterv(chyi__azxw.ctypes, pprej__cjhvq.ctypes, owwvd__kxc.
                ctypes, pku__dlgac.ctypes, np.int32(nei__cgjci), tgsq__qah)
            return bodo.libs.array_item_arr_ext.init_array_item_array(pqa__keyy
                , nqz__lujr, klyyf__bmxj, pku__dlgac)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            krgx__gua = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            krgx__gua = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            krgx__gua = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            krgx__gua = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            fqsim__sdz = data._data
            ddr__pth = data._null_bitmap
            nuq__cop = len(fqsim__sdz)
            iosnq__rqek = _scatterv_np(fqsim__sdz, send_counts)
            ekl__xzkp = bcast_scalar(nuq__cop)
            olgg__enxmo = len(iosnq__rqek) + 7 >> 3
            iuu__airz = np.empty(olgg__enxmo, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                ekl__xzkp)
            pprej__cjhvq = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                pprej__cjhvq[i] = send_counts[i] + 7 >> 3
            owwvd__kxc = bodo.ir.join.calc_disp(pprej__cjhvq)
            chyi__azxw = get_scatter_null_bytes_buff(ddr__pth.ctypes,
                send_counts, pprej__cjhvq)
            c_scatterv(chyi__azxw.ctypes, pprej__cjhvq.ctypes, owwvd__kxc.
                ctypes, iuu__airz.ctypes, np.int32(olgg__enxmo), tgsq__qah)
            return krgx__gua(iosnq__rqek, iuu__airz)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            deqi__pgqxm = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            vio__gesi = bodo.libs.distributed_api.scatterv_impl(data._right,
                send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(deqi__pgqxm,
                vio__gesi)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            anpkp__tlxjf = data._step
            ihx__mvsd = data._name
            ihx__mvsd = bcast_scalar(ihx__mvsd)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            anpkp__tlxjf = bcast_scalar(anpkp__tlxjf)
            oqj__tnj = bodo.libs.array_kernels.calc_nitems(start, stop,
                anpkp__tlxjf)
            chunk_start = bodo.libs.distributed_api.get_start(oqj__tnj,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(oqj__tnj,
                n_pes, rank)
            jurt__lifrl = start + anpkp__tlxjf * chunk_start
            pudh__zcwl = start + anpkp__tlxjf * (chunk_start + chunk_count)
            pudh__zcwl = min(pudh__zcwl, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(jurt__lifrl,
                pudh__zcwl, anpkp__tlxjf, ihx__mvsd)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        pdete__mbv = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            fqsim__sdz = data._data
            ihx__mvsd = data._name
            ihx__mvsd = bcast_scalar(ihx__mvsd)
            arr = bodo.libs.distributed_api.scatterv_impl(fqsim__sdz,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                ihx__mvsd, pdete__mbv)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            fqsim__sdz = data._data
            ihx__mvsd = data._name
            ihx__mvsd = bcast_scalar(ihx__mvsd)
            arr = bodo.libs.distributed_api.scatterv_impl(fqsim__sdz,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, ihx__mvsd)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            cvte__rgdx = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            ihx__mvsd = bcast_scalar(data._name)
            cgiih__kapdg = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(cvte__rgdx
                , cgiih__kapdg, ihx__mvsd)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ihx__mvsd = bodo.hiframes.pd_series_ext.get_series_name(data)
            gvbt__suhko = bcast_scalar(ihx__mvsd)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            fikt__vws = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fikt__vws, gvbt__suhko)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xqb__dfpue = len(data.columns)
        kmbbg__xvmp = ', '.join('g_data_{}'.format(i) for i in range(
            xqb__dfpue))
        juk__xhpm = bodo.utils.transform.gen_const_tup(data.columns)
        ujt__izvv = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        for i in range(xqb__dfpue):
            ujt__izvv += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            ujt__izvv += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        ujt__izvv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        ujt__izvv += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        ujt__izvv += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(kmbbg__xvmp, juk__xhpm))
        ghx__hqgc = {}
        exec(ujt__izvv, {'bodo': bodo}, ghx__hqgc)
        asis__pdxnb = ghx__hqgc['impl_df']
        return asis__pdxnb
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            rwe__lylus = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                rwe__lylus, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        ujt__izvv = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        ujt__izvv += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        ghx__hqgc = {}
        exec(ujt__izvv, {'bodo': bodo}, ghx__hqgc)
        cujla__oud = ghx__hqgc['impl_tuple']
        return cujla__oud
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
        hiwu__mbh = np.int32(numba_to_c_type(offset_type))
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            pqa__keyy = len(data)
            aex__vfprn = num_total_chars(data)
            assert pqa__keyy < INT_MAX
            assert aex__vfprn < INT_MAX
            cqljj__oan = get_offset_ptr(data)
            wmvzz__ralvp = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            eyp__pdsqc = pqa__keyy + 7 >> 3
            c_bcast(cqljj__oan, np.int32(pqa__keyy + 1), hiwu__mbh, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(wmvzz__ralvp, np.int32(aex__vfprn), tgsq__qah, np.array
                ([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(eyp__pdsqc), tgsq__qah, np.
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
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                jiwv__lpxlu = 0
                gpgv__brh = np.empty(0, np.uint8).ctypes
            else:
                gpgv__brh, jiwv__lpxlu = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            jiwv__lpxlu = bodo.libs.distributed_api.bcast_scalar(jiwv__lpxlu,
                root)
            if rank != root:
                fkoz__rujid = np.empty(jiwv__lpxlu + 1, np.uint8)
                fkoz__rujid[jiwv__lpxlu] = 0
                gpgv__brh = fkoz__rujid.ctypes
            c_bcast(gpgv__brh, np.int32(jiwv__lpxlu), tgsq__qah, np.array([
                -1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(gpgv__brh, jiwv__lpxlu)
        return impl_str
    typ_val = numba_to_c_type(val)
    ujt__izvv = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    ghx__hqgc = {}
    exec(ujt__izvv, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, ghx__hqgc)
    bask__gxzeo = ghx__hqgc['bcast_scalar_impl']
    return bask__gxzeo


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    ocl__tutul = len(val)
    ujt__izvv = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    ujt__izvv += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(ocl__tutul)),
        ',' if ocl__tutul else '')
    ghx__hqgc = {}
    exec(ujt__izvv, {'bcast_scalar': bcast_scalar}, ghx__hqgc)
    npa__bmj = ghx__hqgc['bcast_tuple_impl']
    return npa__bmj


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pqa__keyy = bcast_scalar(len(arr), root)
            fvpf__ewah = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(pqa__keyy, fvpf__ewah)
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
        anpkp__tlxjf = slice_index.step
        shx__nxthm = 0 if anpkp__tlxjf == 1 or start > arr_start else abs(
            anpkp__tlxjf - arr_start % anpkp__tlxjf) % anpkp__tlxjf
        jurt__lifrl = max(arr_start, slice_index.start
            ) - arr_start + shx__nxthm
        pudh__zcwl = max(slice_index.stop - arr_start, 0)
        return slice(jurt__lifrl, pudh__zcwl, anpkp__tlxjf)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        oteh__pns = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[oteh__pns])
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
        iqz__dhsk = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        tgsq__qah = np.int32(numba_to_c_type(types.uint8))
        dsmtf__obck = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            tzhav__pqn = np.int32(10)
            tag = np.int32(11)
            ttsrd__jlwwy = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                jyrq__kkq = arr._data
                ouezj__aoaft = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    jyrq__kkq, ind)
                anih__bslz = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    jyrq__kkq, ind + 1)
                length = anih__bslz - ouezj__aoaft
                uqu__brji = jyrq__kkq[ind]
                ttsrd__jlwwy[0] = length
                isend(ttsrd__jlwwy, np.int32(1), root, tzhav__pqn, True)
                isend(uqu__brji, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                dsmtf__obck, iqz__dhsk, 0, 1)
            wzim__noqh = 0
            if rank == root:
                wzim__noqh = recv(np.int64, ANY_SOURCE, tzhav__pqn)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    dsmtf__obck, iqz__dhsk, wzim__noqh, 1)
                wmvzz__ralvp = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(wmvzz__ralvp, np.int32(wzim__noqh), tgsq__qah,
                    ANY_SOURCE, tag)
            dummy_use(ttsrd__jlwwy)
            wzim__noqh = bcast_scalar(wzim__noqh)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    dsmtf__obck, iqz__dhsk, wzim__noqh, 1)
            wmvzz__ralvp = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(wmvzz__ralvp, np.int32(wzim__noqh), tgsq__qah, np.array
                ([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, wzim__noqh)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        vvr__ota = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, vvr__ota)
            if arr_start <= ind < arr_start + len(arr):
                rwe__lylus = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = rwe__lylus[ind - arr_start]
                send_arr = np.full(1, data, vvr__ota)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = vvr__ota(-1)
            if rank == root:
                val = recv(vvr__ota, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            mpmgb__mcbep = arr.dtype.categories[max(val, 0)]
            return mpmgb__mcbep
        return cat_getitem_impl
    vxotj__njn = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, vxotj__njn)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, vxotj__njn)[0]
        if rank == root:
            val = recv(vxotj__njn, ANY_SOURCE, tag)
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
    utdw__roe = get_type_enum(out_data)
    assert typ_enum == utdw__roe
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
    ujt__izvv = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        ujt__izvv += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    ujt__izvv += '  return\n'
    ghx__hqgc = {}
    exec(ujt__izvv, {'alltoallv': alltoallv}, ghx__hqgc)
    qnlhb__ved = ghx__hqgc['f']
    return qnlhb__ved


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    mzrm__gks = total_size % pes
    qgshx__ecy = (total_size - mzrm__gks) // pes
    return rank * qgshx__ecy + min(rank, mzrm__gks)


@numba.njit
def get_end(total_size, pes, rank):
    mzrm__gks = total_size % pes
    qgshx__ecy = (total_size - mzrm__gks) // pes
    return (rank + 1) * qgshx__ecy + min(rank + 1, mzrm__gks)


@numba.njit
def get_node_portion(total_size, pes, rank):
    mzrm__gks = total_size % pes
    qgshx__ecy = (total_size - mzrm__gks) // pes
    if rank < mzrm__gks:
        return qgshx__ecy + 1
    else:
        return qgshx__ecy


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    cgghv__mrw = in_arr.dtype(0)
    gsdoi__wda = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        jhgwa__awqm = cgghv__mrw
        for daec__umhyq in np.nditer(in_arr):
            jhgwa__awqm += daec__umhyq.item()
        anz__siz = dist_exscan(jhgwa__awqm, gsdoi__wda)
        for i in range(in_arr.size):
            anz__siz += in_arr[i]
            out_arr[i] = anz__siz
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    cdfof__ofx = in_arr.dtype(1)
    gsdoi__wda = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        jhgwa__awqm = cdfof__ofx
        for daec__umhyq in np.nditer(in_arr):
            jhgwa__awqm *= daec__umhyq.item()
        anz__siz = dist_exscan(jhgwa__awqm, gsdoi__wda)
        if get_rank() == 0:
            anz__siz = cdfof__ofx
        for i in range(in_arr.size):
            anz__siz *= in_arr[i]
            out_arr[i] = anz__siz
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        cdfof__ofx = np.finfo(in_arr.dtype(1).dtype).max
    else:
        cdfof__ofx = np.iinfo(in_arr.dtype(1).dtype).max
    gsdoi__wda = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        jhgwa__awqm = cdfof__ofx
        for daec__umhyq in np.nditer(in_arr):
            jhgwa__awqm = min(jhgwa__awqm, daec__umhyq.item())
        anz__siz = dist_exscan(jhgwa__awqm, gsdoi__wda)
        if get_rank() == 0:
            anz__siz = cdfof__ofx
        for i in range(in_arr.size):
            anz__siz = min(anz__siz, in_arr[i])
            out_arr[i] = anz__siz
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        cdfof__ofx = np.finfo(in_arr.dtype(1).dtype).min
    else:
        cdfof__ofx = np.iinfo(in_arr.dtype(1).dtype).min
    cdfof__ofx = in_arr.dtype(1)
    gsdoi__wda = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        jhgwa__awqm = cdfof__ofx
        for daec__umhyq in np.nditer(in_arr):
            jhgwa__awqm = max(jhgwa__awqm, daec__umhyq.item())
        anz__siz = dist_exscan(jhgwa__awqm, gsdoi__wda)
        if get_rank() == 0:
            anz__siz = cdfof__ofx
        for i in range(in_arr.size):
            anz__siz = max(anz__siz, in_arr[i])
            out_arr[i] = anz__siz
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    ujk__cfhh = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), ujk__cfhh)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    nyn__csn = args[0]
    if equiv_set.has_shape(nyn__csn):
        return ArrayAnalysis.AnalyzeResult(shape=nyn__csn, pre=[])
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
    fvdz__hhtep = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for
        i, ntqs__xvs in enumerate(args) if is_array_typ(ntqs__xvs) or
        isinstance(ntqs__xvs, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    ujt__izvv = f"""def impl(*args):
    if {fvdz__hhtep} or bodo.get_rank() == 0:
        print(*args)"""
    ghx__hqgc = {}
    exec(ujt__izvv, globals(), ghx__hqgc)
    impl = ghx__hqgc['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        okcs__vdprf = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        ujt__izvv = 'def f(req, cond=True):\n'
        ujt__izvv += f'  return {okcs__vdprf}\n'
        ghx__hqgc = {}
        exec(ujt__izvv, {'_wait': _wait}, ghx__hqgc)
        impl = ghx__hqgc['f']
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
    jurt__lifrl = max(start, chunk_start)
    pudh__zcwl = min(stop, chunk_start + chunk_count)
    xkdbi__iwmgp = jurt__lifrl - chunk_start
    zaoe__utpoy = pudh__zcwl - chunk_start
    if xkdbi__iwmgp < 0 or zaoe__utpoy < 0:
        xkdbi__iwmgp = 1
        zaoe__utpoy = 0
    return xkdbi__iwmgp, zaoe__utpoy


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
        mzrm__gks = 1
        for a in t:
            mzrm__gks *= a
        return mzrm__gks
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    lqksz__lfyfp = np.ascontiguousarray(in_arr)
    gpjgn__fwurc = get_tuple_prod(lqksz__lfyfp.shape[1:])
    ezbb__vyhh = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        lorbd__wcuj = np.array(dest_ranks, dtype=np.int32)
    else:
        lorbd__wcuj = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, lqksz__lfyfp.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * ezbb__vyhh, 
        dtype_size * gpjgn__fwurc, len(lorbd__wcuj), lorbd__wcuj.ctypes)
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
    pkwup__wgcav = np.ascontiguousarray(rhs)
    aefj__dxc = get_tuple_prod(pkwup__wgcav.shape[1:])
    bkwog__iod = dtype_size * aefj__dxc
    permutation_array_index(lhs.ctypes, lhs_len, bkwog__iod, pkwup__wgcav.
        ctypes, pkwup__wgcav.shape[0], p.ctypes, p_len)
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
        ujt__izvv = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        ghx__hqgc = {}
        exec(ujt__izvv, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, ghx__hqgc)
        bask__gxzeo = ghx__hqgc['bcast_scalar_impl']
        return bask__gxzeo
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xqb__dfpue = len(data.columns)
        kmbbg__xvmp = ', '.join('g_data_{}'.format(i) for i in range(
            xqb__dfpue))
        juk__xhpm = bodo.utils.transform.gen_const_tup(data.columns)
        ujt__izvv = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(xqb__dfpue):
            ujt__izvv += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            ujt__izvv += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        ujt__izvv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        ujt__izvv += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        ujt__izvv += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(kmbbg__xvmp, juk__xhpm))
        ghx__hqgc = {}
        exec(ujt__izvv, {'bodo': bodo}, ghx__hqgc)
        asis__pdxnb = ghx__hqgc['impl_df']
        return asis__pdxnb
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            anpkp__tlxjf = data._step
            ihx__mvsd = data._name
            ihx__mvsd = bcast_scalar(ihx__mvsd, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            anpkp__tlxjf = bcast_scalar(anpkp__tlxjf, root)
            oqj__tnj = bodo.libs.array_kernels.calc_nitems(start, stop,
                anpkp__tlxjf)
            chunk_start = bodo.libs.distributed_api.get_start(oqj__tnj,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(oqj__tnj,
                n_pes, rank)
            jurt__lifrl = start + anpkp__tlxjf * chunk_start
            pudh__zcwl = start + anpkp__tlxjf * (chunk_start + chunk_count)
            pudh__zcwl = min(pudh__zcwl, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(jurt__lifrl,
                pudh__zcwl, anpkp__tlxjf, ihx__mvsd)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            fqsim__sdz = data._data
            ihx__mvsd = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(fqsim__sdz,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, ihx__mvsd)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ihx__mvsd = bodo.hiframes.pd_series_ext.get_series_name(data)
            gvbt__suhko = bodo.libs.distributed_api.bcast_comm_impl(ihx__mvsd,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            fikt__vws = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fikt__vws, gvbt__suhko)
        return impl_series
    if isinstance(data, types.BaseTuple):
        ujt__izvv = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        ujt__izvv += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        ghx__hqgc = {}
        exec(ujt__izvv, {'bcast_comm_impl': bcast_comm_impl}, ghx__hqgc)
        cujla__oud = ghx__hqgc['impl_tuple']
        return cujla__oud
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    wyin__lyjvt = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    blrwg__cmq = (0,) * wyin__lyjvt

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        fqsim__sdz = np.ascontiguousarray(data)
        wmvzz__ralvp = data.ctypes
        nynrf__gaknh = blrwg__cmq
        if rank == root:
            nynrf__gaknh = fqsim__sdz.shape
        nynrf__gaknh = bcast_tuple(nynrf__gaknh, root)
        qldxx__cvxi = get_tuple_prod(nynrf__gaknh[1:])
        send_counts = nynrf__gaknh[0] * qldxx__cvxi
        shvoj__eee = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(wmvzz__ralvp, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(shvoj__eee.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return shvoj__eee.reshape((-1,) + nynrf__gaknh[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        kbcmo__ctu = MPI.COMM_WORLD
        fftel__vjt = MPI.Get_processor_name()
        lkhuo__rnjm = kbcmo__ctu.allgather(fftel__vjt)
        node_ranks = defaultdict(list)
        for i, jpujz__odv in enumerate(lkhuo__rnjm):
            node_ranks[jpujz__odv].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    kbcmo__ctu = MPI.COMM_WORLD
    xmg__qsma = kbcmo__ctu.Get_group()
    ezbjp__joubi = xmg__qsma.Incl(comm_ranks)
    jouv__yowzs = kbcmo__ctu.Create_group(ezbjp__joubi)
    return jouv__yowzs


def get_nodes_first_ranks():
    acxqh__jauc = get_host_ranks()
    return np.array([uuzci__jzek[0] for uuzci__jzek in acxqh__jauc.values()
        ], dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
