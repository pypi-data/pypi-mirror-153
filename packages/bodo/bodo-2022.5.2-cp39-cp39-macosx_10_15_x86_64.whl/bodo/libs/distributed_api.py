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
    rkob__snsk = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, rkob__snsk, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    rkob__snsk = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, rkob__snsk, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            rkob__snsk = get_type_enum(arr)
            return _isend(arr.ctypes, size, rkob__snsk, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        rkob__snsk = np.int32(numba_to_c_type(arr.dtype))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            cezpf__xmim = size + 7 >> 3
            mrfd__elmvr = _isend(arr._data.ctypes, size, rkob__snsk, pe,
                tag, cond)
            mvoyl__otu = _isend(arr._null_bitmap.ctypes, cezpf__xmim,
                kzcj__hjrj, pe, tag, cond)
            return mrfd__elmvr, mvoyl__otu
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        hgajj__pjfuu = np.int32(numba_to_c_type(offset_type))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            alxl__jkn = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(alxl__jkn, pe, tag - 1)
            cezpf__xmim = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                hgajj__pjfuu, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), alxl__jkn,
                kzcj__hjrj, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                cezpf__xmim, kzcj__hjrj, pe, tag)
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
            rkob__snsk = get_type_enum(arr)
            return _irecv(arr.ctypes, size, rkob__snsk, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        rkob__snsk = np.int32(numba_to_c_type(arr.dtype))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            cezpf__xmim = size + 7 >> 3
            mrfd__elmvr = _irecv(arr._data.ctypes, size, rkob__snsk, pe,
                tag, cond)
            mvoyl__otu = _irecv(arr._null_bitmap.ctypes, cezpf__xmim,
                kzcj__hjrj, pe, tag, cond)
            return mrfd__elmvr, mvoyl__otu
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        hgajj__pjfuu = np.int32(numba_to_c_type(offset_type))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            vwf__ohy = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            vwf__ohy = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        ysz__flik = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {vwf__ohy}(size, n_chars)
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
        kdgq__xoz = dict()
        exec(ysz__flik, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            hgajj__pjfuu, 'char_typ_enum': kzcj__hjrj}, kdgq__xoz)
        impl = kdgq__xoz['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    rkob__snsk = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), rkob__snsk)


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
        qzgn__bwd = n_pes if rank == root or allgather else 0
        ccqi__vcg = np.empty(qzgn__bwd, dtype)
        c_gather_scalar(send.ctypes, ccqi__vcg.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return ccqi__vcg
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
        lxld__obgua = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], lxld__obgua)
        return builder.bitcast(lxld__obgua, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        lxld__obgua = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(lxld__obgua)
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
    avch__lvprt = types.unliteral(value)
    if isinstance(avch__lvprt, IndexValueType):
        avch__lvprt = avch__lvprt.val_typ
        mlxyw__thtuj = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            mlxyw__thtuj.append(types.int64)
            mlxyw__thtuj.append(bodo.datetime64ns)
            mlxyw__thtuj.append(bodo.timedelta64ns)
            mlxyw__thtuj.append(bodo.datetime_date_type)
        if avch__lvprt not in mlxyw__thtuj:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(avch__lvprt))
    typ_enum = np.int32(numba_to_c_type(avch__lvprt))

    def impl(value, reduce_op):
        iqzrc__xbfkp = value_to_ptr(value)
        zuqlw__leymr = value_to_ptr(value)
        _dist_reduce(iqzrc__xbfkp, zuqlw__leymr, reduce_op, typ_enum)
        return load_val_ptr(zuqlw__leymr, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    avch__lvprt = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(avch__lvprt))
    zoyo__rtage = avch__lvprt(0)

    def impl(value, reduce_op):
        iqzrc__xbfkp = value_to_ptr(value)
        zuqlw__leymr = value_to_ptr(zoyo__rtage)
        _dist_exscan(iqzrc__xbfkp, zuqlw__leymr, reduce_op, typ_enum)
        return load_val_ptr(zuqlw__leymr, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    zwfl__xbao = 0
    wjspn__wea = 0
    for i in range(len(recv_counts)):
        dkk__jgs = recv_counts[i]
        cezpf__xmim = recv_counts_nulls[i]
        nxb__xge = tmp_null_bytes[zwfl__xbao:zwfl__xbao + cezpf__xmim]
        for ybe__cyaba in range(dkk__jgs):
            set_bit_to(null_bitmap_ptr, wjspn__wea, get_bit(nxb__xge,
                ybe__cyaba))
            wjspn__wea += 1
        zwfl__xbao += cezpf__xmim


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            dokc__orvfo = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                dokc__orvfo, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            mmo__nnfkd = data.size
            recv_counts = gather_scalar(np.int32(mmo__nnfkd), allgather,
                root=root)
            kkx__xncvp = recv_counts.sum()
            sfem__ypc = empty_like_type(kkx__xncvp, data)
            qxtd__fsql = np.empty(1, np.int32)
            if rank == root or allgather:
                qxtd__fsql = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(mmo__nnfkd), sfem__ypc.ctypes,
                recv_counts.ctypes, qxtd__fsql.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return sfem__ypc.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            sfem__ypc = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(sfem__ypc)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            sfem__ypc = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(sfem__ypc)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            mmo__nnfkd = len(data)
            cezpf__xmim = mmo__nnfkd + 7 >> 3
            recv_counts = gather_scalar(np.int32(mmo__nnfkd), allgather,
                root=root)
            kkx__xncvp = recv_counts.sum()
            sfem__ypc = empty_like_type(kkx__xncvp, data)
            qxtd__fsql = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            zsrin__ssil = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                qxtd__fsql = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                zsrin__ssil = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(mmo__nnfkd),
                sfem__ypc._days_data.ctypes, recv_counts.ctypes, qxtd__fsql
                .ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(mmo__nnfkd),
                sfem__ypc._seconds_data.ctypes, recv_counts.ctypes,
                qxtd__fsql.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(mmo__nnfkd),
                sfem__ypc._microseconds_data.ctypes, recv_counts.ctypes,
                qxtd__fsql.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(cezpf__xmim),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                zsrin__ssil.ctypes, kzcj__hjrj, allgather, np.int32(root))
            copy_gathered_null_bytes(sfem__ypc._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return sfem__ypc
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            mmo__nnfkd = len(data)
            cezpf__xmim = mmo__nnfkd + 7 >> 3
            recv_counts = gather_scalar(np.int32(mmo__nnfkd), allgather,
                root=root)
            kkx__xncvp = recv_counts.sum()
            sfem__ypc = empty_like_type(kkx__xncvp, data)
            qxtd__fsql = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            zsrin__ssil = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                qxtd__fsql = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                zsrin__ssil = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(mmo__nnfkd), sfem__ypc.
                _data.ctypes, recv_counts.ctypes, qxtd__fsql.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(cezpf__xmim),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                zsrin__ssil.ctypes, kzcj__hjrj, allgather, np.int32(root))
            copy_gathered_null_bytes(sfem__ypc._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return sfem__ypc
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        umj__cliqg = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            kaf__flf = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                kaf__flf, umj__cliqg)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            duucy__wzjq = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            yxvu__dzu = bodo.gatherv(data._right, allgather, warn_if_rep, root)
            return bodo.libs.interval_arr_ext.init_interval_array(duucy__wzjq,
                yxvu__dzu)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            xhvi__ttrem = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            rpsg__hqy = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rpsg__hqy, xhvi__ttrem)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        suz__cso = np.iinfo(np.int64).max
        lfwpd__fig = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            dydx__zzyc = data._start
            yccwh__sdnst = data._stop
            if len(data) == 0:
                dydx__zzyc = suz__cso
                yccwh__sdnst = lfwpd__fig
            dydx__zzyc = bodo.libs.distributed_api.dist_reduce(dydx__zzyc,
                np.int32(Reduce_Type.Min.value))
            yccwh__sdnst = bodo.libs.distributed_api.dist_reduce(yccwh__sdnst,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if dydx__zzyc == suz__cso and yccwh__sdnst == lfwpd__fig:
                dydx__zzyc = 0
                yccwh__sdnst = 0
            pnkvt__xrpng = max(0, -(-(yccwh__sdnst - dydx__zzyc) // data._step)
                )
            if pnkvt__xrpng < total_len:
                yccwh__sdnst = dydx__zzyc + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                dydx__zzyc = 0
                yccwh__sdnst = 0
            return bodo.hiframes.pd_index_ext.init_range_index(dydx__zzyc,
                yccwh__sdnst, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            dzbbp__kqrtd = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, dzbbp__kqrtd)
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
            sfem__ypc = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(sfem__ypc,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        pfb__vnsi = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        ysz__flik = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        ysz__flik += '  T = data\n'
        ysz__flik += '  T2 = init_table(T, True)\n'
        for uime__bgcab in data.type_to_blk.values():
            pfb__vnsi[f'arr_inds_{uime__bgcab}'] = np.array(data.
                block_to_arr_ind[uime__bgcab], dtype=np.int64)
            ysz__flik += (
                f'  arr_list_{uime__bgcab} = get_table_block(T, {uime__bgcab})\n'
                )
            ysz__flik += f"""  out_arr_list_{uime__bgcab} = alloc_list_like(arr_list_{uime__bgcab}, True)
"""
            ysz__flik += f'  for i in range(len(arr_list_{uime__bgcab})):\n'
            ysz__flik += (
                f'    arr_ind_{uime__bgcab} = arr_inds_{uime__bgcab}[i]\n')
            ysz__flik += f"""    ensure_column_unboxed(T, arr_list_{uime__bgcab}, i, arr_ind_{uime__bgcab})
"""
            ysz__flik += f"""    out_arr_{uime__bgcab} = bodo.gatherv(arr_list_{uime__bgcab}[i], allgather, warn_if_rep, root)
"""
            ysz__flik += (
                f'    out_arr_list_{uime__bgcab}[i] = out_arr_{uime__bgcab}\n')
            ysz__flik += (
                f'  T2 = set_table_block(T2, out_arr_list_{uime__bgcab}, {uime__bgcab})\n'
                )
        ysz__flik += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        ysz__flik += f'  T2 = set_table_len(T2, length)\n'
        ysz__flik += f'  return T2\n'
        kdgq__xoz = {}
        exec(ysz__flik, pfb__vnsi, kdgq__xoz)
        xvonf__mgg = kdgq__xoz['impl_table']
        return xvonf__mgg
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ccq__sps = len(data.columns)
        if ccq__sps == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                bvia__giy = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    bvia__giy, ())
            return impl
        kiwul__tntqe = ', '.join(f'g_data_{i}' for i in range(ccq__sps))
        tjx__vpmm = bodo.utils.transform.gen_const_tup(data.columns)
        ysz__flik = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            vacrc__ngtv = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            pfb__vnsi = {'bodo': bodo, 'df_type': vacrc__ngtv}
            kiwul__tntqe = 'T2'
            tjx__vpmm = 'df_type'
            ysz__flik += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            ysz__flik += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            pfb__vnsi = {'bodo': bodo}
            for i in range(ccq__sps):
                ysz__flik += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                ysz__flik += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        ysz__flik += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        ysz__flik += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        ysz__flik += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(kiwul__tntqe, tjx__vpmm))
        kdgq__xoz = {}
        exec(ysz__flik, pfb__vnsi, kdgq__xoz)
        zdb__adfy = kdgq__xoz['impl_df']
        return zdb__adfy
    if isinstance(data, ArrayItemArrayType):
        fqk__pxdoa = np.int32(numba_to_c_type(types.int32))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            oyoz__jne = bodo.libs.array_item_arr_ext.get_offsets(data)
            qur__lwd = bodo.libs.array_item_arr_ext.get_data(data)
            qur__lwd = qur__lwd[:oyoz__jne[-1]]
            rwny__krtm = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            mmo__nnfkd = len(data)
            jdtn__xyr = np.empty(mmo__nnfkd, np.uint32)
            cezpf__xmim = mmo__nnfkd + 7 >> 3
            for i in range(mmo__nnfkd):
                jdtn__xyr[i] = oyoz__jne[i + 1] - oyoz__jne[i]
            recv_counts = gather_scalar(np.int32(mmo__nnfkd), allgather,
                root=root)
            kkx__xncvp = recv_counts.sum()
            qxtd__fsql = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            zsrin__ssil = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                qxtd__fsql = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for ilvv__sctd in range(len(recv_counts)):
                    recv_counts_nulls[ilvv__sctd] = recv_counts[ilvv__sctd
                        ] + 7 >> 3
                zsrin__ssil = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            cbbiv__sja = np.empty(kkx__xncvp + 1, np.uint32)
            avpg__bwy = bodo.gatherv(qur__lwd, allgather, warn_if_rep, root)
            idxb__feh = np.empty(kkx__xncvp + 7 >> 3, np.uint8)
            c_gatherv(jdtn__xyr.ctypes, np.int32(mmo__nnfkd), cbbiv__sja.
                ctypes, recv_counts.ctypes, qxtd__fsql.ctypes, fqk__pxdoa,
                allgather, np.int32(root))
            c_gatherv(rwny__krtm.ctypes, np.int32(cezpf__xmim),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                zsrin__ssil.ctypes, kzcj__hjrj, allgather, np.int32(root))
            dummy_use(data)
            tqa__ltxy = np.empty(kkx__xncvp + 1, np.uint64)
            convert_len_arr_to_offset(cbbiv__sja.ctypes, tqa__ltxy.ctypes,
                kkx__xncvp)
            copy_gathered_null_bytes(idxb__feh.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                kkx__xncvp, avpg__bwy, tqa__ltxy, idxb__feh)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        nwhlz__gos = data.names
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            lcesf__lkg = bodo.libs.struct_arr_ext.get_data(data)
            vupzn__jtvof = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            urxcd__tvfr = bodo.gatherv(lcesf__lkg, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            mmo__nnfkd = len(data)
            cezpf__xmim = mmo__nnfkd + 7 >> 3
            recv_counts = gather_scalar(np.int32(mmo__nnfkd), allgather,
                root=root)
            kkx__xncvp = recv_counts.sum()
            iypa__rhvqt = np.empty(kkx__xncvp + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            zsrin__ssil = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                zsrin__ssil = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(vupzn__jtvof.ctypes, np.int32(cezpf__xmim),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                zsrin__ssil.ctypes, kzcj__hjrj, allgather, np.int32(root))
            copy_gathered_null_bytes(iypa__rhvqt.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(urxcd__tvfr,
                iypa__rhvqt, nwhlz__gos)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            sfem__ypc = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(sfem__ypc)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            sfem__ypc = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(sfem__ypc)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            sfem__ypc = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(sfem__ypc)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            sfem__ypc = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            gpz__tipk = bodo.gatherv(data.indices, allgather, warn_if_rep, root
                )
            xsf__hsu = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            jzgs__rhwni = gather_scalar(data.shape[0], allgather, root=root)
            vfpd__nja = jzgs__rhwni.sum()
            ccq__sps = bodo.libs.distributed_api.dist_reduce(data.shape[1],
                np.int32(Reduce_Type.Max.value))
            bdmu__stbsj = np.empty(vfpd__nja + 1, np.int64)
            gpz__tipk = gpz__tipk.astype(np.int64)
            bdmu__stbsj[0] = 0
            sdkn__gsj = 1
            gcu__rfwjh = 0
            for iuom__jgac in jzgs__rhwni:
                for tqi__lgdge in range(iuom__jgac):
                    onzyb__vtb = xsf__hsu[gcu__rfwjh + 1] - xsf__hsu[gcu__rfwjh
                        ]
                    bdmu__stbsj[sdkn__gsj] = bdmu__stbsj[sdkn__gsj - 1
                        ] + onzyb__vtb
                    sdkn__gsj += 1
                    gcu__rfwjh += 1
                gcu__rfwjh += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(sfem__ypc,
                gpz__tipk, bdmu__stbsj, (vfpd__nja, ccq__sps))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        ysz__flik = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        ysz__flik += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        kdgq__xoz = {}
        exec(ysz__flik, {'bodo': bodo}, kdgq__xoz)
        pvj__vlikr = kdgq__xoz['impl_tuple']
        return pvj__vlikr
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    ysz__flik = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    ysz__flik += '    if random:\n'
    ysz__flik += '        if random_seed is None:\n'
    ysz__flik += '            random = 1\n'
    ysz__flik += '        else:\n'
    ysz__flik += '            random = 2\n'
    ysz__flik += '    if random_seed is None:\n'
    ysz__flik += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        vtt__bflsa = data
        ccq__sps = len(vtt__bflsa.columns)
        for i in range(ccq__sps):
            ysz__flik += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        ysz__flik += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        kiwul__tntqe = ', '.join(f'data_{i}' for i in range(ccq__sps))
        ysz__flik += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(zsgk__fymb) for
            zsgk__fymb in range(ccq__sps))))
        ysz__flik += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        ysz__flik += '    if dests is None:\n'
        ysz__flik += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        ysz__flik += '    else:\n'
        ysz__flik += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for rpo__dhw in range(ccq__sps):
            ysz__flik += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(rpo__dhw))
        ysz__flik += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(ccq__sps))
        ysz__flik += '    delete_table(out_table)\n'
        ysz__flik += '    if parallel:\n'
        ysz__flik += '        delete_table(table_total)\n'
        kiwul__tntqe = ', '.join('out_arr_{}'.format(i) for i in range(
            ccq__sps))
        tjx__vpmm = bodo.utils.transform.gen_const_tup(vtt__bflsa.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        ysz__flik += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(kiwul__tntqe, index, tjx__vpmm))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        ysz__flik += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        ysz__flik += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        ysz__flik += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        ysz__flik += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        ysz__flik += '    if dests is None:\n'
        ysz__flik += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        ysz__flik += '    else:\n'
        ysz__flik += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        ysz__flik += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        ysz__flik += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        ysz__flik += '    delete_table(out_table)\n'
        ysz__flik += '    if parallel:\n'
        ysz__flik += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        ysz__flik += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        ysz__flik += '    if not parallel:\n'
        ysz__flik += '        return data\n'
        ysz__flik += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        ysz__flik += '    if dests is None:\n'
        ysz__flik += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        ysz__flik += '    elif bodo.get_rank() not in dests:\n'
        ysz__flik += '        dim0_local_size = 0\n'
        ysz__flik += '    else:\n'
        ysz__flik += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        ysz__flik += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        ysz__flik += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        ysz__flik += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        ysz__flik += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        ysz__flik += '    if dests is None:\n'
        ysz__flik += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        ysz__flik += '    else:\n'
        ysz__flik += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        ysz__flik += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        ysz__flik += '    delete_table(out_table)\n'
        ysz__flik += '    if parallel:\n'
        ysz__flik += '        delete_table(table_total)\n'
        ysz__flik += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    kdgq__xoz = {}
    exec(ysz__flik, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}, kdgq__xoz
        )
    impl = kdgq__xoz['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    ysz__flik = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        ysz__flik += '    if seed is None:\n'
        ysz__flik += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        ysz__flik += '    np.random.seed(seed)\n'
        ysz__flik += '    if not parallel:\n'
        ysz__flik += '        data = data.copy()\n'
        ysz__flik += '        np.random.shuffle(data)\n'
        ysz__flik += '        return data\n'
        ysz__flik += '    else:\n'
        ysz__flik += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        ysz__flik += '        permutation = np.arange(dim0_global_size)\n'
        ysz__flik += '        np.random.shuffle(permutation)\n'
        ysz__flik += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        ysz__flik += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        ysz__flik += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        ysz__flik += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        ysz__flik += '        return output\n'
    else:
        ysz__flik += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    kdgq__xoz = {}
    exec(ysz__flik, {'np': np, 'bodo': bodo}, kdgq__xoz)
    impl = kdgq__xoz['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    iugh__xblu = np.empty(sendcounts_nulls.sum(), np.uint8)
    zwfl__xbao = 0
    wjspn__wea = 0
    for awe__drg in range(len(sendcounts)):
        dkk__jgs = sendcounts[awe__drg]
        cezpf__xmim = sendcounts_nulls[awe__drg]
        nxb__xge = iugh__xblu[zwfl__xbao:zwfl__xbao + cezpf__xmim]
        for ybe__cyaba in range(dkk__jgs):
            set_bit_to_arr(nxb__xge, ybe__cyaba, get_bit_bitmap(
                null_bitmap_ptr, wjspn__wea))
            wjspn__wea += 1
        zwfl__xbao += cezpf__xmim
    return iugh__xblu


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    ayupe__uty = MPI.COMM_WORLD
    data = ayupe__uty.bcast(data, root)
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
    cqstw__pop = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    xrqig__eim = (0,) * cqstw__pop

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        bnim__ywr = np.ascontiguousarray(data)
        deq__ofymu = data.ctypes
        vulre__bsu = xrqig__eim
        if rank == MPI_ROOT:
            vulre__bsu = bnim__ywr.shape
        vulre__bsu = bcast_tuple(vulre__bsu)
        muan__edza = get_tuple_prod(vulre__bsu[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            vulre__bsu[0])
        send_counts *= muan__edza
        mmo__nnfkd = send_counts[rank]
        ntghe__skrc = np.empty(mmo__nnfkd, dtype)
        qxtd__fsql = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(deq__ofymu, send_counts.ctypes, qxtd__fsql.ctypes,
            ntghe__skrc.ctypes, np.int32(mmo__nnfkd), np.int32(typ_val))
        return ntghe__skrc.reshape((-1,) + vulre__bsu[1:])
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
        agz__qaxhl = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], agz__qaxhl)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        xhvi__ttrem = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=xhvi__ttrem)
        lrf__nybgj = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(lrf__nybgj)
        return pd.Index(arr, name=xhvi__ttrem)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        xhvi__ttrem = _get_name_value_for_type(dtype.name_typ)
        nwhlz__gos = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        trbps__tnd = tuple(get_value_for_type(t) for t in dtype.array_types)
        trbps__tnd = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in trbps__tnd)
        val = pd.MultiIndex.from_arrays(trbps__tnd, names=nwhlz__gos)
        val.name = xhvi__ttrem
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        xhvi__ttrem = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=xhvi__ttrem)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        trbps__tnd = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({xhvi__ttrem: arr for xhvi__ttrem, arr in zip(
            dtype.columns, trbps__tnd)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        lrf__nybgj = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(lrf__nybgj[0],
            lrf__nybgj[0])])
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
        fqk__pxdoa = np.int32(numba_to_c_type(types.int32))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            vwf__ohy = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            vwf__ohy = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        ysz__flik = f"""def impl(
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
            recv_arr = {vwf__ohy}(n_loc, n_loc_char)

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
        kdgq__xoz = dict()
        exec(ysz__flik, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            fqk__pxdoa, 'char_typ_enum': kzcj__hjrj, 'decode_if_dict_array':
            decode_if_dict_array}, kdgq__xoz)
        impl = kdgq__xoz['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        fqk__pxdoa = np.int32(numba_to_c_type(types.int32))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            gop__pkjz = bodo.libs.array_item_arr_ext.get_offsets(data)
            kcga__unzfn = bodo.libs.array_item_arr_ext.get_data(data)
            kcga__unzfn = kcga__unzfn[:gop__pkjz[-1]]
            vdnm__kggj = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            mlc__rvljk = bcast_scalar(len(data))
            btj__hqczh = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                btj__hqczh[i] = gop__pkjz[i + 1] - gop__pkjz[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                mlc__rvljk)
            qxtd__fsql = bodo.ir.join.calc_disp(send_counts)
            bfxrm__dkai = np.empty(n_pes, np.int32)
            if rank == 0:
                hcdx__oej = 0
                for i in range(n_pes):
                    kbd__vlif = 0
                    for tqi__lgdge in range(send_counts[i]):
                        kbd__vlif += btj__hqczh[hcdx__oej]
                        hcdx__oej += 1
                    bfxrm__dkai[i] = kbd__vlif
            bcast(bfxrm__dkai)
            qiny__pwyg = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                qiny__pwyg[i] = send_counts[i] + 7 >> 3
            zsrin__ssil = bodo.ir.join.calc_disp(qiny__pwyg)
            mmo__nnfkd = send_counts[rank]
            trp__wmlh = np.empty(mmo__nnfkd + 1, np_offset_type)
            ryprl__pbat = bodo.libs.distributed_api.scatterv_impl(kcga__unzfn,
                bfxrm__dkai)
            jtyym__kkvvu = mmo__nnfkd + 7 >> 3
            jko__ukr = np.empty(jtyym__kkvvu, np.uint8)
            pfcs__xtk = np.empty(mmo__nnfkd, np.uint32)
            c_scatterv(btj__hqczh.ctypes, send_counts.ctypes, qxtd__fsql.
                ctypes, pfcs__xtk.ctypes, np.int32(mmo__nnfkd), fqk__pxdoa)
            convert_len_arr_to_offset(pfcs__xtk.ctypes, trp__wmlh.ctypes,
                mmo__nnfkd)
            dir__ocrq = get_scatter_null_bytes_buff(vdnm__kggj.ctypes,
                send_counts, qiny__pwyg)
            c_scatterv(dir__ocrq.ctypes, qiny__pwyg.ctypes, zsrin__ssil.
                ctypes, jko__ukr.ctypes, np.int32(jtyym__kkvvu), kzcj__hjrj)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                mmo__nnfkd, ryprl__pbat, trp__wmlh, jko__ukr)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            mwrh__xilyz = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            mwrh__xilyz = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            mwrh__xilyz = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            mwrh__xilyz = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            bnim__ywr = data._data
            vupzn__jtvof = data._null_bitmap
            qzfj__kdv = len(bnim__ywr)
            ukea__bdwji = _scatterv_np(bnim__ywr, send_counts)
            mlc__rvljk = bcast_scalar(qzfj__kdv)
            umxf__wzm = len(ukea__bdwji) + 7 >> 3
            jra__ehip = np.empty(umxf__wzm, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                mlc__rvljk)
            qiny__pwyg = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                qiny__pwyg[i] = send_counts[i] + 7 >> 3
            zsrin__ssil = bodo.ir.join.calc_disp(qiny__pwyg)
            dir__ocrq = get_scatter_null_bytes_buff(vupzn__jtvof.ctypes,
                send_counts, qiny__pwyg)
            c_scatterv(dir__ocrq.ctypes, qiny__pwyg.ctypes, zsrin__ssil.
                ctypes, jra__ehip.ctypes, np.int32(umxf__wzm), kzcj__hjrj)
            return mwrh__xilyz(ukea__bdwji, jra__ehip)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            humq__vhgmy = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            fltm__wrqzc = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(humq__vhgmy,
                fltm__wrqzc)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            dydx__zzyc = data._start
            yccwh__sdnst = data._stop
            eza__lspo = data._step
            xhvi__ttrem = data._name
            xhvi__ttrem = bcast_scalar(xhvi__ttrem)
            dydx__zzyc = bcast_scalar(dydx__zzyc)
            yccwh__sdnst = bcast_scalar(yccwh__sdnst)
            eza__lspo = bcast_scalar(eza__lspo)
            dfmik__qbjhe = bodo.libs.array_kernels.calc_nitems(dydx__zzyc,
                yccwh__sdnst, eza__lspo)
            chunk_start = bodo.libs.distributed_api.get_start(dfmik__qbjhe,
                n_pes, rank)
            yecw__lifyt = bodo.libs.distributed_api.get_node_portion(
                dfmik__qbjhe, n_pes, rank)
            vvm__jlmt = dydx__zzyc + eza__lspo * chunk_start
            iih__pvu = dydx__zzyc + eza__lspo * (chunk_start + yecw__lifyt)
            iih__pvu = min(iih__pvu, yccwh__sdnst)
            return bodo.hiframes.pd_index_ext.init_range_index(vvm__jlmt,
                iih__pvu, eza__lspo, xhvi__ttrem)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        dzbbp__kqrtd = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            bnim__ywr = data._data
            xhvi__ttrem = data._name
            xhvi__ttrem = bcast_scalar(xhvi__ttrem)
            arr = bodo.libs.distributed_api.scatterv_impl(bnim__ywr,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                xhvi__ttrem, dzbbp__kqrtd)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            bnim__ywr = data._data
            xhvi__ttrem = data._name
            xhvi__ttrem = bcast_scalar(xhvi__ttrem)
            arr = bodo.libs.distributed_api.scatterv_impl(bnim__ywr,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, xhvi__ttrem)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            sfem__ypc = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            xhvi__ttrem = bcast_scalar(data._name)
            nwhlz__gos = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(sfem__ypc,
                nwhlz__gos, xhvi__ttrem)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            xhvi__ttrem = bodo.hiframes.pd_series_ext.get_series_name(data)
            hrtvf__aqgy = bcast_scalar(xhvi__ttrem)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            rpsg__hqy = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rpsg__hqy, hrtvf__aqgy)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ccq__sps = len(data.columns)
        kiwul__tntqe = ', '.join('g_data_{}'.format(i) for i in range(ccq__sps)
            )
        tjx__vpmm = bodo.utils.transform.gen_const_tup(data.columns)
        ysz__flik = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        for i in range(ccq__sps):
            ysz__flik += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            ysz__flik += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        ysz__flik += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        ysz__flik += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        ysz__flik += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(kiwul__tntqe, tjx__vpmm))
        kdgq__xoz = {}
        exec(ysz__flik, {'bodo': bodo}, kdgq__xoz)
        zdb__adfy = kdgq__xoz['impl_df']
        return zdb__adfy
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            dokc__orvfo = bodo.libs.distributed_api.scatterv_impl(data.
                codes, send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                dokc__orvfo, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        ysz__flik = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        ysz__flik += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        kdgq__xoz = {}
        exec(ysz__flik, {'bodo': bodo}, kdgq__xoz)
        pvj__vlikr = kdgq__xoz['impl_tuple']
        return pvj__vlikr
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
        hgajj__pjfuu = np.int32(numba_to_c_type(offset_type))
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            mmo__nnfkd = len(data)
            sks__orzv = num_total_chars(data)
            assert mmo__nnfkd < INT_MAX
            assert sks__orzv < INT_MAX
            xdco__odsy = get_offset_ptr(data)
            deq__ofymu = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            cezpf__xmim = mmo__nnfkd + 7 >> 3
            c_bcast(xdco__odsy, np.int32(mmo__nnfkd + 1), hgajj__pjfuu, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(deq__ofymu, np.int32(sks__orzv), kzcj__hjrj, np.array([
                -1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(cezpf__xmim), kzcj__hjrj, np.
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
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                sjo__yusy = 0
                aauvd__abm = np.empty(0, np.uint8).ctypes
            else:
                aauvd__abm, sjo__yusy = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            sjo__yusy = bodo.libs.distributed_api.bcast_scalar(sjo__yusy, root)
            if rank != root:
                ytfuc__zmhte = np.empty(sjo__yusy + 1, np.uint8)
                ytfuc__zmhte[sjo__yusy] = 0
                aauvd__abm = ytfuc__zmhte.ctypes
            c_bcast(aauvd__abm, np.int32(sjo__yusy), kzcj__hjrj, np.array([
                -1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(aauvd__abm, sjo__yusy)
        return impl_str
    typ_val = numba_to_c_type(val)
    ysz__flik = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    kdgq__xoz = {}
    exec(ysz__flik, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, kdgq__xoz)
    down__ylerr = kdgq__xoz['bcast_scalar_impl']
    return down__ylerr


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    yvp__meh = len(val)
    ysz__flik = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    ysz__flik += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(yvp__meh)), 
        ',' if yvp__meh else '')
    kdgq__xoz = {}
    exec(ysz__flik, {'bcast_scalar': bcast_scalar}, kdgq__xoz)
    kfd__wuug = kdgq__xoz['bcast_tuple_impl']
    return kfd__wuug


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            mmo__nnfkd = bcast_scalar(len(arr), root)
            cym__cll = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(mmo__nnfkd, cym__cll)
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
        dydx__zzyc = slice_index.start
        eza__lspo = slice_index.step
        vnfs__wbip = 0 if eza__lspo == 1 or dydx__zzyc > arr_start else abs(
            eza__lspo - arr_start % eza__lspo) % eza__lspo
        vvm__jlmt = max(arr_start, slice_index.start) - arr_start + vnfs__wbip
        iih__pvu = max(slice_index.stop - arr_start, 0)
        return slice(vvm__jlmt, iih__pvu, eza__lspo)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        jta__hqv = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[jta__hqv])
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
        scsjx__fpecg = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        kzcj__hjrj = np.int32(numba_to_c_type(types.uint8))
        lfr__oeob = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            rjg__fqhpg = np.int32(10)
            tag = np.int32(11)
            sqfi__xnnbm = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                qur__lwd = arr._data
                mrn__sss = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    qur__lwd, ind)
                uxn__etep = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    qur__lwd, ind + 1)
                length = uxn__etep - mrn__sss
                lxld__obgua = qur__lwd[ind]
                sqfi__xnnbm[0] = length
                isend(sqfi__xnnbm, np.int32(1), root, rjg__fqhpg, True)
                isend(lxld__obgua, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(lfr__oeob,
                scsjx__fpecg, 0, 1)
            pnkvt__xrpng = 0
            if rank == root:
                pnkvt__xrpng = recv(np.int64, ANY_SOURCE, rjg__fqhpg)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    lfr__oeob, scsjx__fpecg, pnkvt__xrpng, 1)
                deq__ofymu = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(deq__ofymu, np.int32(pnkvt__xrpng), kzcj__hjrj,
                    ANY_SOURCE, tag)
            dummy_use(sqfi__xnnbm)
            pnkvt__xrpng = bcast_scalar(pnkvt__xrpng)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    lfr__oeob, scsjx__fpecg, pnkvt__xrpng, 1)
            deq__ofymu = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(deq__ofymu, np.int32(pnkvt__xrpng), kzcj__hjrj, np.
                array([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, pnkvt__xrpng)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        lyxh__gnvs = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, lyxh__gnvs)
            if arr_start <= ind < arr_start + len(arr):
                dokc__orvfo = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = dokc__orvfo[ind - arr_start]
                send_arr = np.full(1, data, lyxh__gnvs)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = lyxh__gnvs(-1)
            if rank == root:
                val = recv(lyxh__gnvs, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            naui__rcqio = arr.dtype.categories[max(val, 0)]
            return naui__rcqio
        return cat_getitem_impl
    xfb__bqb = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, xfb__bqb)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, xfb__bqb)[0]
        if rank == root:
            val = recv(xfb__bqb, ANY_SOURCE, tag)
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
    theh__emzz = get_type_enum(out_data)
    assert typ_enum == theh__emzz
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
    ysz__flik = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        ysz__flik += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    ysz__flik += '  return\n'
    kdgq__xoz = {}
    exec(ysz__flik, {'alltoallv': alltoallv}, kdgq__xoz)
    ldqpu__yfjm = kdgq__xoz['f']
    return ldqpu__yfjm


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    dydx__zzyc = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return dydx__zzyc, count


@numba.njit
def get_start(total_size, pes, rank):
    ccqi__vcg = total_size % pes
    ivdwy__anept = (total_size - ccqi__vcg) // pes
    return rank * ivdwy__anept + min(rank, ccqi__vcg)


@numba.njit
def get_end(total_size, pes, rank):
    ccqi__vcg = total_size % pes
    ivdwy__anept = (total_size - ccqi__vcg) // pes
    return (rank + 1) * ivdwy__anept + min(rank + 1, ccqi__vcg)


@numba.njit
def get_node_portion(total_size, pes, rank):
    ccqi__vcg = total_size % pes
    ivdwy__anept = (total_size - ccqi__vcg) // pes
    if rank < ccqi__vcg:
        return ivdwy__anept + 1
    else:
        return ivdwy__anept


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    zoyo__rtage = in_arr.dtype(0)
    dwj__lkmv = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        kbd__vlif = zoyo__rtage
        for lrgim__btxz in np.nditer(in_arr):
            kbd__vlif += lrgim__btxz.item()
        yeza__xjt = dist_exscan(kbd__vlif, dwj__lkmv)
        for i in range(in_arr.size):
            yeza__xjt += in_arr[i]
            out_arr[i] = yeza__xjt
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    zym__nejay = in_arr.dtype(1)
    dwj__lkmv = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        kbd__vlif = zym__nejay
        for lrgim__btxz in np.nditer(in_arr):
            kbd__vlif *= lrgim__btxz.item()
        yeza__xjt = dist_exscan(kbd__vlif, dwj__lkmv)
        if get_rank() == 0:
            yeza__xjt = zym__nejay
        for i in range(in_arr.size):
            yeza__xjt *= in_arr[i]
            out_arr[i] = yeza__xjt
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        zym__nejay = np.finfo(in_arr.dtype(1).dtype).max
    else:
        zym__nejay = np.iinfo(in_arr.dtype(1).dtype).max
    dwj__lkmv = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        kbd__vlif = zym__nejay
        for lrgim__btxz in np.nditer(in_arr):
            kbd__vlif = min(kbd__vlif, lrgim__btxz.item())
        yeza__xjt = dist_exscan(kbd__vlif, dwj__lkmv)
        if get_rank() == 0:
            yeza__xjt = zym__nejay
        for i in range(in_arr.size):
            yeza__xjt = min(yeza__xjt, in_arr[i])
            out_arr[i] = yeza__xjt
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        zym__nejay = np.finfo(in_arr.dtype(1).dtype).min
    else:
        zym__nejay = np.iinfo(in_arr.dtype(1).dtype).min
    zym__nejay = in_arr.dtype(1)
    dwj__lkmv = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        kbd__vlif = zym__nejay
        for lrgim__btxz in np.nditer(in_arr):
            kbd__vlif = max(kbd__vlif, lrgim__btxz.item())
        yeza__xjt = dist_exscan(kbd__vlif, dwj__lkmv)
        if get_rank() == 0:
            yeza__xjt = zym__nejay
        for i in range(in_arr.size):
            yeza__xjt = max(yeza__xjt, in_arr[i])
            out_arr[i] = yeza__xjt
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    rkob__snsk = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), rkob__snsk)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    krin__uyj = args[0]
    if equiv_set.has_shape(krin__uyj):
        return ArrayAnalysis.AnalyzeResult(shape=krin__uyj, pre=[])
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
    tupuc__syw = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, wkqg__xgu in enumerate(args) if is_array_typ(wkqg__xgu) or
        isinstance(wkqg__xgu, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    ysz__flik = f"""def impl(*args):
    if {tupuc__syw} or bodo.get_rank() == 0:
        print(*args)"""
    kdgq__xoz = {}
    exec(ysz__flik, globals(), kdgq__xoz)
    impl = kdgq__xoz['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        mmo__rswd = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        ysz__flik = 'def f(req, cond=True):\n'
        ysz__flik += f'  return {mmo__rswd}\n'
        kdgq__xoz = {}
        exec(ysz__flik, {'_wait': _wait}, kdgq__xoz)
        impl = kdgq__xoz['f']
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
        ccqi__vcg = 1
        for a in t:
            ccqi__vcg *= a
        return ccqi__vcg
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    wmf__wyhn = np.ascontiguousarray(in_arr)
    fwhfx__txii = get_tuple_prod(wmf__wyhn.shape[1:])
    dfy__zaa = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        oouz__zgkn = np.array(dest_ranks, dtype=np.int32)
    else:
        oouz__zgkn = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, wmf__wyhn.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * dfy__zaa, dtype_size * fwhfx__txii, len(
        oouz__zgkn), oouz__zgkn.ctypes)
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
    vps__yevj = np.ascontiguousarray(rhs)
    wbs__ctdt = get_tuple_prod(vps__yevj.shape[1:])
    qcvp__qchv = dtype_size * wbs__ctdt
    permutation_array_index(lhs.ctypes, lhs_len, qcvp__qchv, vps__yevj.
        ctypes, vps__yevj.shape[0], p.ctypes, p_len)
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
        ysz__flik = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        kdgq__xoz = {}
        exec(ysz__flik, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, kdgq__xoz)
        down__ylerr = kdgq__xoz['bcast_scalar_impl']
        return down__ylerr
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ccq__sps = len(data.columns)
        kiwul__tntqe = ', '.join('g_data_{}'.format(i) for i in range(ccq__sps)
            )
        tjx__vpmm = bodo.utils.transform.gen_const_tup(data.columns)
        ysz__flik = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(ccq__sps):
            ysz__flik += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            ysz__flik += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        ysz__flik += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        ysz__flik += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        ysz__flik += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(kiwul__tntqe, tjx__vpmm))
        kdgq__xoz = {}
        exec(ysz__flik, {'bodo': bodo}, kdgq__xoz)
        zdb__adfy = kdgq__xoz['impl_df']
        return zdb__adfy
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            dydx__zzyc = data._start
            yccwh__sdnst = data._stop
            eza__lspo = data._step
            xhvi__ttrem = data._name
            xhvi__ttrem = bcast_scalar(xhvi__ttrem, root)
            dydx__zzyc = bcast_scalar(dydx__zzyc, root)
            yccwh__sdnst = bcast_scalar(yccwh__sdnst, root)
            eza__lspo = bcast_scalar(eza__lspo, root)
            dfmik__qbjhe = bodo.libs.array_kernels.calc_nitems(dydx__zzyc,
                yccwh__sdnst, eza__lspo)
            chunk_start = bodo.libs.distributed_api.get_start(dfmik__qbjhe,
                n_pes, rank)
            yecw__lifyt = bodo.libs.distributed_api.get_node_portion(
                dfmik__qbjhe, n_pes, rank)
            vvm__jlmt = dydx__zzyc + eza__lspo * chunk_start
            iih__pvu = dydx__zzyc + eza__lspo * (chunk_start + yecw__lifyt)
            iih__pvu = min(iih__pvu, yccwh__sdnst)
            return bodo.hiframes.pd_index_ext.init_range_index(vvm__jlmt,
                iih__pvu, eza__lspo, xhvi__ttrem)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            bnim__ywr = data._data
            xhvi__ttrem = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(bnim__ywr,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, xhvi__ttrem)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            xhvi__ttrem = bodo.hiframes.pd_series_ext.get_series_name(data)
            hrtvf__aqgy = bodo.libs.distributed_api.bcast_comm_impl(xhvi__ttrem
                , comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            rpsg__hqy = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rpsg__hqy, hrtvf__aqgy)
        return impl_series
    if isinstance(data, types.BaseTuple):
        ysz__flik = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        ysz__flik += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        kdgq__xoz = {}
        exec(ysz__flik, {'bcast_comm_impl': bcast_comm_impl}, kdgq__xoz)
        pvj__vlikr = kdgq__xoz['impl_tuple']
        return pvj__vlikr
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    cqstw__pop = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    xrqig__eim = (0,) * cqstw__pop

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        bnim__ywr = np.ascontiguousarray(data)
        deq__ofymu = data.ctypes
        vulre__bsu = xrqig__eim
        if rank == root:
            vulre__bsu = bnim__ywr.shape
        vulre__bsu = bcast_tuple(vulre__bsu, root)
        muan__edza = get_tuple_prod(vulre__bsu[1:])
        send_counts = vulre__bsu[0] * muan__edza
        ntghe__skrc = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(deq__ofymu, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(ntghe__skrc.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return ntghe__skrc.reshape((-1,) + vulre__bsu[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        ayupe__uty = MPI.COMM_WORLD
        karx__loy = MPI.Get_processor_name()
        satc__zsgvv = ayupe__uty.allgather(karx__loy)
        node_ranks = defaultdict(list)
        for i, eow__ecl in enumerate(satc__zsgvv):
            node_ranks[eow__ecl].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    ayupe__uty = MPI.COMM_WORLD
    ssho__clzg = ayupe__uty.Get_group()
    ssc__kfwjw = ssho__clzg.Incl(comm_ranks)
    txmc__mim = ayupe__uty.Create_group(ssc__kfwjw)
    return txmc__mim


def get_nodes_first_ranks():
    sjxq__xde = get_host_ranks()
    return np.array([cxtyr__ikj[0] for cxtyr__ikj in sjxq__xde.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
