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
    yigiw__exsv = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, yigiw__exsv, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    yigiw__exsv = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, yigiw__exsv, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            yigiw__exsv = get_type_enum(arr)
            return _isend(arr.ctypes, size, yigiw__exsv, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        yigiw__exsv = np.int32(numba_to_c_type(arr.dtype))
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            rvr__wvbph = size + 7 >> 3
            wcg__pfalh = _isend(arr._data.ctypes, size, yigiw__exsv, pe,
                tag, cond)
            seov__sflu = _isend(arr._null_bitmap.ctypes, rvr__wvbph,
                anud__etk, pe, tag, cond)
            return wcg__pfalh, seov__sflu
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        nvu__tuiod = np.int32(numba_to_c_type(offset_type))
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            mlui__leiko = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(mlui__leiko, pe, tag - 1)
            rvr__wvbph = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                nvu__tuiod, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), mlui__leiko,
                anud__etk, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                rvr__wvbph, anud__etk, pe, tag)
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
            yigiw__exsv = get_type_enum(arr)
            return _irecv(arr.ctypes, size, yigiw__exsv, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        yigiw__exsv = np.int32(numba_to_c_type(arr.dtype))
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            rvr__wvbph = size + 7 >> 3
            wcg__pfalh = _irecv(arr._data.ctypes, size, yigiw__exsv, pe,
                tag, cond)
            seov__sflu = _irecv(arr._null_bitmap.ctypes, rvr__wvbph,
                anud__etk, pe, tag, cond)
            return wcg__pfalh, seov__sflu
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        nvu__tuiod = np.int32(numba_to_c_type(offset_type))
        anud__etk = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            fkp__nmpw = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            fkp__nmpw = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        naxjp__fohv = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {fkp__nmpw}(size, n_chars)
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
        jcjqi__vaakw = dict()
        exec(naxjp__fohv, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            nvu__tuiod, 'char_typ_enum': anud__etk}, jcjqi__vaakw)
        impl = jcjqi__vaakw['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    yigiw__exsv = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), yigiw__exsv)


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
        duzkf__qxe = n_pes if rank == root or allgather else 0
        hhq__djpvf = np.empty(duzkf__qxe, dtype)
        c_gather_scalar(send.ctypes, hhq__djpvf.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return hhq__djpvf
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
        nsiz__abkb = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], nsiz__abkb)
        return builder.bitcast(nsiz__abkb, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        nsiz__abkb = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(nsiz__abkb)
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
    oief__gihrl = types.unliteral(value)
    if isinstance(oief__gihrl, IndexValueType):
        oief__gihrl = oief__gihrl.val_typ
        wfcb__cjmk = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            wfcb__cjmk.append(types.int64)
            wfcb__cjmk.append(bodo.datetime64ns)
            wfcb__cjmk.append(bodo.timedelta64ns)
            wfcb__cjmk.append(bodo.datetime_date_type)
        if oief__gihrl not in wfcb__cjmk:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(oief__gihrl))
    typ_enum = np.int32(numba_to_c_type(oief__gihrl))

    def impl(value, reduce_op):
        ermtv__bkfi = value_to_ptr(value)
        biqg__pei = value_to_ptr(value)
        _dist_reduce(ermtv__bkfi, biqg__pei, reduce_op, typ_enum)
        return load_val_ptr(biqg__pei, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    oief__gihrl = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(oief__gihrl))
    nivd__siwx = oief__gihrl(0)

    def impl(value, reduce_op):
        ermtv__bkfi = value_to_ptr(value)
        biqg__pei = value_to_ptr(nivd__siwx)
        _dist_exscan(ermtv__bkfi, biqg__pei, reduce_op, typ_enum)
        return load_val_ptr(biqg__pei, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    hbos__essp = 0
    toh__lgxkc = 0
    for i in range(len(recv_counts)):
        wmw__jmw = recv_counts[i]
        rvr__wvbph = recv_counts_nulls[i]
        wwidm__gnwi = tmp_null_bytes[hbos__essp:hbos__essp + rvr__wvbph]
        for irf__nbhee in range(wmw__jmw):
            set_bit_to(null_bitmap_ptr, toh__lgxkc, get_bit(wwidm__gnwi,
                irf__nbhee))
            toh__lgxkc += 1
        hbos__essp += rvr__wvbph


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            rtd__dsik = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                rtd__dsik, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            rayuy__ctnfm = data.size
            recv_counts = gather_scalar(np.int32(rayuy__ctnfm), allgather,
                root=root)
            usgu__brevu = recv_counts.sum()
            unoz__axsqa = empty_like_type(usgu__brevu, data)
            omqam__wuk = np.empty(1, np.int32)
            if rank == root or allgather:
                omqam__wuk = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(rayuy__ctnfm), unoz__axsqa.
                ctypes, recv_counts.ctypes, omqam__wuk.ctypes, np.int32(
                typ_val), allgather, np.int32(root))
            return unoz__axsqa.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            unoz__axsqa = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.str_arr_ext.init_str_arr(unoz__axsqa)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            unoz__axsqa = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.binary_arr_ext.init_binary_arr(unoz__axsqa)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            rayuy__ctnfm = len(data)
            rvr__wvbph = rayuy__ctnfm + 7 >> 3
            recv_counts = gather_scalar(np.int32(rayuy__ctnfm), allgather,
                root=root)
            usgu__brevu = recv_counts.sum()
            unoz__axsqa = empty_like_type(usgu__brevu, data)
            omqam__wuk = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            dus__gdng = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                omqam__wuk = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                dus__gdng = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(rayuy__ctnfm),
                unoz__axsqa._days_data.ctypes, recv_counts.ctypes,
                omqam__wuk.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._seconds_data.ctypes, np.int32(rayuy__ctnfm),
                unoz__axsqa._seconds_data.ctypes, recv_counts.ctypes,
                omqam__wuk.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(rayuy__ctnfm
                ), unoz__axsqa._microseconds_data.ctypes, recv_counts.
                ctypes, omqam__wuk.ctypes, np.int32(typ_val), allgather, np
                .int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(rvr__wvbph),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dus__gdng.
                ctypes, anud__etk, allgather, np.int32(root))
            copy_gathered_null_bytes(unoz__axsqa._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return unoz__axsqa
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            rayuy__ctnfm = len(data)
            rvr__wvbph = rayuy__ctnfm + 7 >> 3
            recv_counts = gather_scalar(np.int32(rayuy__ctnfm), allgather,
                root=root)
            usgu__brevu = recv_counts.sum()
            unoz__axsqa = empty_like_type(usgu__brevu, data)
            omqam__wuk = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            dus__gdng = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                omqam__wuk = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                dus__gdng = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(rayuy__ctnfm),
                unoz__axsqa._data.ctypes, recv_counts.ctypes, omqam__wuk.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(rvr__wvbph),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dus__gdng.
                ctypes, anud__etk, allgather, np.int32(root))
            copy_gathered_null_bytes(unoz__axsqa._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return unoz__axsqa
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        hisyl__evob = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            gsew__ckpzu = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                gsew__ckpzu, hisyl__evob)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            pht__hgcso = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            uwdku__ykhds = bodo.gatherv(data._right, allgather, warn_if_rep,
                root)
            return bodo.libs.interval_arr_ext.init_interval_array(pht__hgcso,
                uwdku__ykhds)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ppctf__mijwi = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            usiwn__zmu = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                usiwn__zmu, ppctf__mijwi)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        pcv__oawhm = np.iinfo(np.int64).max
        rfyxn__kzb = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            kmmqr__yglgm = data._start
            vmqss__inkod = data._stop
            if len(data) == 0:
                kmmqr__yglgm = pcv__oawhm
                vmqss__inkod = rfyxn__kzb
            kmmqr__yglgm = bodo.libs.distributed_api.dist_reduce(kmmqr__yglgm,
                np.int32(Reduce_Type.Min.value))
            vmqss__inkod = bodo.libs.distributed_api.dist_reduce(vmqss__inkod,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if kmmqr__yglgm == pcv__oawhm and vmqss__inkod == rfyxn__kzb:
                kmmqr__yglgm = 0
                vmqss__inkod = 0
            hqc__nvj = max(0, -(-(vmqss__inkod - kmmqr__yglgm) // data._step))
            if hqc__nvj < total_len:
                vmqss__inkod = kmmqr__yglgm + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                kmmqr__yglgm = 0
                vmqss__inkod = 0
            return bodo.hiframes.pd_index_ext.init_range_index(kmmqr__yglgm,
                vmqss__inkod, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            fbp__nhkp = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, fbp__nhkp)
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
            unoz__axsqa = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                unoz__axsqa, data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        ipwe__zcrs = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        naxjp__fohv = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        naxjp__fohv += '  T = data\n'
        naxjp__fohv += '  T2 = init_table(T, True)\n'
        for eakuv__fvgyo in data.type_to_blk.values():
            ipwe__zcrs[f'arr_inds_{eakuv__fvgyo}'] = np.array(data.
                block_to_arr_ind[eakuv__fvgyo], dtype=np.int64)
            naxjp__fohv += (
                f'  arr_list_{eakuv__fvgyo} = get_table_block(T, {eakuv__fvgyo})\n'
                )
            naxjp__fohv += f"""  out_arr_list_{eakuv__fvgyo} = alloc_list_like(arr_list_{eakuv__fvgyo}, True)
"""
            naxjp__fohv += f'  for i in range(len(arr_list_{eakuv__fvgyo})):\n'
            naxjp__fohv += (
                f'    arr_ind_{eakuv__fvgyo} = arr_inds_{eakuv__fvgyo}[i]\n')
            naxjp__fohv += f"""    ensure_column_unboxed(T, arr_list_{eakuv__fvgyo}, i, arr_ind_{eakuv__fvgyo})
"""
            naxjp__fohv += f"""    out_arr_{eakuv__fvgyo} = bodo.gatherv(arr_list_{eakuv__fvgyo}[i], allgather, warn_if_rep, root)
"""
            naxjp__fohv += (
                f'    out_arr_list_{eakuv__fvgyo}[i] = out_arr_{eakuv__fvgyo}\n'
                )
            naxjp__fohv += f"""  T2 = set_table_block(T2, out_arr_list_{eakuv__fvgyo}, {eakuv__fvgyo})
"""
        naxjp__fohv += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        naxjp__fohv += f'  T2 = set_table_len(T2, length)\n'
        naxjp__fohv += f'  return T2\n'
        jcjqi__vaakw = {}
        exec(naxjp__fohv, ipwe__zcrs, jcjqi__vaakw)
        ycn__yvlro = jcjqi__vaakw['impl_table']
        return ycn__yvlro
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        vlu__tzk = len(data.columns)
        if vlu__tzk == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                iiawa__sui = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    iiawa__sui, ())
            return impl
        pxkg__fhd = ', '.join(f'g_data_{i}' for i in range(vlu__tzk))
        rdds__olp = bodo.utils.transform.gen_const_tup(data.columns)
        naxjp__fohv = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            qwu__ymt = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            ipwe__zcrs = {'bodo': bodo, 'df_type': qwu__ymt}
            pxkg__fhd = 'T2'
            rdds__olp = 'df_type'
            naxjp__fohv += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            naxjp__fohv += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            ipwe__zcrs = {'bodo': bodo}
            for i in range(vlu__tzk):
                naxjp__fohv += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                naxjp__fohv += (
                    """  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)
"""
                    .format(i, i))
        naxjp__fohv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        naxjp__fohv += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        naxjp__fohv += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(pxkg__fhd, rdds__olp))
        jcjqi__vaakw = {}
        exec(naxjp__fohv, ipwe__zcrs, jcjqi__vaakw)
        idja__lms = jcjqi__vaakw['impl_df']
        return idja__lms
    if isinstance(data, ArrayItemArrayType):
        avxn__lfcim = np.int32(numba_to_c_type(types.int32))
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            cbvom__xvaf = bodo.libs.array_item_arr_ext.get_offsets(data)
            lbel__czdnm = bodo.libs.array_item_arr_ext.get_data(data)
            lbel__czdnm = lbel__czdnm[:cbvom__xvaf[-1]]
            kfs__ghb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rayuy__ctnfm = len(data)
            hbs__jgxlo = np.empty(rayuy__ctnfm, np.uint32)
            rvr__wvbph = rayuy__ctnfm + 7 >> 3
            for i in range(rayuy__ctnfm):
                hbs__jgxlo[i] = cbvom__xvaf[i + 1] - cbvom__xvaf[i]
            recv_counts = gather_scalar(np.int32(rayuy__ctnfm), allgather,
                root=root)
            usgu__brevu = recv_counts.sum()
            omqam__wuk = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            dus__gdng = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                omqam__wuk = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for nkwpb__biqsb in range(len(recv_counts)):
                    recv_counts_nulls[nkwpb__biqsb] = recv_counts[nkwpb__biqsb
                        ] + 7 >> 3
                dus__gdng = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            upox__ack = np.empty(usgu__brevu + 1, np.uint32)
            byl__mikg = bodo.gatherv(lbel__czdnm, allgather, warn_if_rep, root)
            auggk__pgz = np.empty(usgu__brevu + 7 >> 3, np.uint8)
            c_gatherv(hbs__jgxlo.ctypes, np.int32(rayuy__ctnfm), upox__ack.
                ctypes, recv_counts.ctypes, omqam__wuk.ctypes, avxn__lfcim,
                allgather, np.int32(root))
            c_gatherv(kfs__ghb.ctypes, np.int32(rvr__wvbph), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, dus__gdng.ctypes,
                anud__etk, allgather, np.int32(root))
            dummy_use(data)
            kltns__bfr = np.empty(usgu__brevu + 1, np.uint64)
            convert_len_arr_to_offset(upox__ack.ctypes, kltns__bfr.ctypes,
                usgu__brevu)
            copy_gathered_null_bytes(auggk__pgz.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                usgu__brevu, byl__mikg, kltns__bfr, auggk__pgz)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        dcec__hueod = data.names
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            bes__zsjlo = bodo.libs.struct_arr_ext.get_data(data)
            sdguj__wmlt = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            wzq__bmed = bodo.gatherv(bes__zsjlo, allgather=allgather, root=root
                )
            rank = bodo.libs.distributed_api.get_rank()
            rayuy__ctnfm = len(data)
            rvr__wvbph = rayuy__ctnfm + 7 >> 3
            recv_counts = gather_scalar(np.int32(rayuy__ctnfm), allgather,
                root=root)
            usgu__brevu = recv_counts.sum()
            vcltc__nbf = np.empty(usgu__brevu + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            dus__gdng = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                dus__gdng = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(sdguj__wmlt.ctypes, np.int32(rvr__wvbph),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dus__gdng.
                ctypes, anud__etk, allgather, np.int32(root))
            copy_gathered_null_bytes(vcltc__nbf.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(wzq__bmed,
                vcltc__nbf, dcec__hueod)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            unoz__axsqa = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.binary_arr_ext.init_binary_arr(unoz__axsqa)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            unoz__axsqa = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.tuple_arr_ext.init_tuple_arr(unoz__axsqa)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            unoz__axsqa = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.map_arr_ext.init_map_arr(unoz__axsqa)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            unoz__axsqa = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            ecdv__iooe = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            sviq__herlm = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            mfq__rzzip = gather_scalar(data.shape[0], allgather, root=root)
            tcpg__riros = mfq__rzzip.sum()
            vlu__tzk = bodo.libs.distributed_api.dist_reduce(data.shape[1],
                np.int32(Reduce_Type.Max.value))
            qift__ilupq = np.empty(tcpg__riros + 1, np.int64)
            ecdv__iooe = ecdv__iooe.astype(np.int64)
            qift__ilupq[0] = 0
            nfnu__ptgb = 1
            skmx__bwf = 0
            for chrza__kjj in mfq__rzzip:
                for lhgya__zhbk in range(chrza__kjj):
                    xfkp__kcl = sviq__herlm[skmx__bwf + 1] - sviq__herlm[
                        skmx__bwf]
                    qift__ilupq[nfnu__ptgb] = qift__ilupq[nfnu__ptgb - 1
                        ] + xfkp__kcl
                    nfnu__ptgb += 1
                    skmx__bwf += 1
                skmx__bwf += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(unoz__axsqa,
                ecdv__iooe, qift__ilupq, (tcpg__riros, vlu__tzk))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        naxjp__fohv = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        naxjp__fohv += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'bodo': bodo}, jcjqi__vaakw)
        xno__hwm = jcjqi__vaakw['impl_tuple']
        return xno__hwm
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    naxjp__fohv = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    naxjp__fohv += '    if random:\n'
    naxjp__fohv += '        if random_seed is None:\n'
    naxjp__fohv += '            random = 1\n'
    naxjp__fohv += '        else:\n'
    naxjp__fohv += '            random = 2\n'
    naxjp__fohv += '    if random_seed is None:\n'
    naxjp__fohv += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ksg__xdbf = data
        vlu__tzk = len(ksg__xdbf.columns)
        for i in range(vlu__tzk):
            naxjp__fohv += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        naxjp__fohv += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        pxkg__fhd = ', '.join(f'data_{i}' for i in range(vlu__tzk))
        naxjp__fohv += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(jmxtz__yank) for
            jmxtz__yank in range(vlu__tzk))))
        naxjp__fohv += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        naxjp__fohv += '    if dests is None:\n'
        naxjp__fohv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        naxjp__fohv += '    else:\n'
        naxjp__fohv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for iut__dvmfw in range(vlu__tzk):
            naxjp__fohv += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(iut__dvmfw))
        naxjp__fohv += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(vlu__tzk))
        naxjp__fohv += '    delete_table(out_table)\n'
        naxjp__fohv += '    if parallel:\n'
        naxjp__fohv += '        delete_table(table_total)\n'
        pxkg__fhd = ', '.join('out_arr_{}'.format(i) for i in range(vlu__tzk))
        rdds__olp = bodo.utils.transform.gen_const_tup(ksg__xdbf.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        naxjp__fohv += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(pxkg__fhd, index, rdds__olp))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        naxjp__fohv += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        naxjp__fohv += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        naxjp__fohv += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        naxjp__fohv += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        naxjp__fohv += '    if dests is None:\n'
        naxjp__fohv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        naxjp__fohv += '    else:\n'
        naxjp__fohv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        naxjp__fohv += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        naxjp__fohv += """    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)
"""
        naxjp__fohv += '    delete_table(out_table)\n'
        naxjp__fohv += '    if parallel:\n'
        naxjp__fohv += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        naxjp__fohv += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        naxjp__fohv += '    if not parallel:\n'
        naxjp__fohv += '        return data\n'
        naxjp__fohv += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        naxjp__fohv += '    if dests is None:\n'
        naxjp__fohv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        naxjp__fohv += '    elif bodo.get_rank() not in dests:\n'
        naxjp__fohv += '        dim0_local_size = 0\n'
        naxjp__fohv += '    else:\n'
        naxjp__fohv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        naxjp__fohv += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        naxjp__fohv += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        naxjp__fohv += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        naxjp__fohv += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        naxjp__fohv += '    if dests is None:\n'
        naxjp__fohv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        naxjp__fohv += '    else:\n'
        naxjp__fohv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        naxjp__fohv += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        naxjp__fohv += '    delete_table(out_table)\n'
        naxjp__fohv += '    if parallel:\n'
        naxjp__fohv += '        delete_table(table_total)\n'
        naxjp__fohv += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    jcjqi__vaakw = {}
    exec(naxjp__fohv, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        jcjqi__vaakw)
    impl = jcjqi__vaakw['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    naxjp__fohv = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        naxjp__fohv += '    if seed is None:\n'
        naxjp__fohv += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        naxjp__fohv += '    np.random.seed(seed)\n'
        naxjp__fohv += '    if not parallel:\n'
        naxjp__fohv += '        data = data.copy()\n'
        naxjp__fohv += '        np.random.shuffle(data)\n'
        naxjp__fohv += '        return data\n'
        naxjp__fohv += '    else:\n'
        naxjp__fohv += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        naxjp__fohv += '        permutation = np.arange(dim0_global_size)\n'
        naxjp__fohv += '        np.random.shuffle(permutation)\n'
        naxjp__fohv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        naxjp__fohv += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        naxjp__fohv += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        naxjp__fohv += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        naxjp__fohv += '        return output\n'
    else:
        naxjp__fohv += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    jcjqi__vaakw = {}
    exec(naxjp__fohv, {'np': np, 'bodo': bodo}, jcjqi__vaakw)
    impl = jcjqi__vaakw['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    skrx__fif = np.empty(sendcounts_nulls.sum(), np.uint8)
    hbos__essp = 0
    toh__lgxkc = 0
    for bcevr__lya in range(len(sendcounts)):
        wmw__jmw = sendcounts[bcevr__lya]
        rvr__wvbph = sendcounts_nulls[bcevr__lya]
        wwidm__gnwi = skrx__fif[hbos__essp:hbos__essp + rvr__wvbph]
        for irf__nbhee in range(wmw__jmw):
            set_bit_to_arr(wwidm__gnwi, irf__nbhee, get_bit_bitmap(
                null_bitmap_ptr, toh__lgxkc))
            toh__lgxkc += 1
        hbos__essp += rvr__wvbph
    return skrx__fif


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    ammc__vdle = MPI.COMM_WORLD
    data = ammc__vdle.bcast(data, root)
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
    klrp__lvj = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    pkd__asme = (0,) * klrp__lvj

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        wrtc__ezd = np.ascontiguousarray(data)
        owslc__kcfh = data.ctypes
        secga__nljvm = pkd__asme
        if rank == MPI_ROOT:
            secga__nljvm = wrtc__ezd.shape
        secga__nljvm = bcast_tuple(secga__nljvm)
        jpg__hcxms = get_tuple_prod(secga__nljvm[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            secga__nljvm[0])
        send_counts *= jpg__hcxms
        rayuy__ctnfm = send_counts[rank]
        yrjs__myzq = np.empty(rayuy__ctnfm, dtype)
        omqam__wuk = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(owslc__kcfh, send_counts.ctypes, omqam__wuk.ctypes,
            yrjs__myzq.ctypes, np.int32(rayuy__ctnfm), np.int32(typ_val))
        return yrjs__myzq.reshape((-1,) + secga__nljvm[1:])
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
        nlgix__cmbht = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], nlgix__cmbht)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        ppctf__mijwi = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=ppctf__mijwi)
        fgkx__nsb = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(fgkx__nsb)
        return pd.Index(arr, name=ppctf__mijwi)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        ppctf__mijwi = _get_name_value_for_type(dtype.name_typ)
        dcec__hueod = tuple(_get_name_value_for_type(t) for t in dtype.
            names_typ)
        qnx__eidc = tuple(get_value_for_type(t) for t in dtype.array_types)
        qnx__eidc = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in qnx__eidc)
        val = pd.MultiIndex.from_arrays(qnx__eidc, names=dcec__hueod)
        val.name = ppctf__mijwi
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        ppctf__mijwi = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=ppctf__mijwi)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qnx__eidc = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({ppctf__mijwi: arr for ppctf__mijwi, arr in zip
            (dtype.columns, qnx__eidc)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        fgkx__nsb = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(fgkx__nsb[0], fgkx__nsb
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
        avxn__lfcim = np.int32(numba_to_c_type(types.int32))
        anud__etk = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            fkp__nmpw = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            fkp__nmpw = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        naxjp__fohv = f"""def impl(
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
            recv_arr = {fkp__nmpw}(n_loc, n_loc_char)

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
        jcjqi__vaakw = dict()
        exec(naxjp__fohv, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            avxn__lfcim, 'char_typ_enum': anud__etk, 'decode_if_dict_array':
            decode_if_dict_array}, jcjqi__vaakw)
        impl = jcjqi__vaakw['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        avxn__lfcim = np.int32(numba_to_c_type(types.int32))
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            yve__mifdu = bodo.libs.array_item_arr_ext.get_offsets(data)
            nmxc__qfwm = bodo.libs.array_item_arr_ext.get_data(data)
            nmxc__qfwm = nmxc__qfwm[:yve__mifdu[-1]]
            lihm__qmaml = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            widny__tmwra = bcast_scalar(len(data))
            qkgw__mld = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                qkgw__mld[i] = yve__mifdu[i + 1] - yve__mifdu[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                widny__tmwra)
            omqam__wuk = bodo.ir.join.calc_disp(send_counts)
            lwxdp__wwmes = np.empty(n_pes, np.int32)
            if rank == 0:
                aiso__gzuco = 0
                for i in range(n_pes):
                    ksj__hfbez = 0
                    for lhgya__zhbk in range(send_counts[i]):
                        ksj__hfbez += qkgw__mld[aiso__gzuco]
                        aiso__gzuco += 1
                    lwxdp__wwmes[i] = ksj__hfbez
            bcast(lwxdp__wwmes)
            wkzk__yerm = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                wkzk__yerm[i] = send_counts[i] + 7 >> 3
            dus__gdng = bodo.ir.join.calc_disp(wkzk__yerm)
            rayuy__ctnfm = send_counts[rank]
            ettj__tcym = np.empty(rayuy__ctnfm + 1, np_offset_type)
            htlg__pouwh = bodo.libs.distributed_api.scatterv_impl(nmxc__qfwm,
                lwxdp__wwmes)
            pxcn__sho = rayuy__ctnfm + 7 >> 3
            nut__txgrb = np.empty(pxcn__sho, np.uint8)
            xlrlp__mxwoc = np.empty(rayuy__ctnfm, np.uint32)
            c_scatterv(qkgw__mld.ctypes, send_counts.ctypes, omqam__wuk.
                ctypes, xlrlp__mxwoc.ctypes, np.int32(rayuy__ctnfm),
                avxn__lfcim)
            convert_len_arr_to_offset(xlrlp__mxwoc.ctypes, ettj__tcym.
                ctypes, rayuy__ctnfm)
            iul__dcjbh = get_scatter_null_bytes_buff(lihm__qmaml.ctypes,
                send_counts, wkzk__yerm)
            c_scatterv(iul__dcjbh.ctypes, wkzk__yerm.ctypes, dus__gdng.
                ctypes, nut__txgrb.ctypes, np.int32(pxcn__sho), anud__etk)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                rayuy__ctnfm, htlg__pouwh, ettj__tcym, nut__txgrb)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        anud__etk = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            fsy__oxkow = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            fsy__oxkow = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            fsy__oxkow = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            fsy__oxkow = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            wrtc__ezd = data._data
            sdguj__wmlt = data._null_bitmap
            tvpkr__vlo = len(wrtc__ezd)
            hgjl__hvgsi = _scatterv_np(wrtc__ezd, send_counts)
            widny__tmwra = bcast_scalar(tvpkr__vlo)
            mjkq__xdhkv = len(hgjl__hvgsi) + 7 >> 3
            xesnn__esq = np.empty(mjkq__xdhkv, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                widny__tmwra)
            wkzk__yerm = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                wkzk__yerm[i] = send_counts[i] + 7 >> 3
            dus__gdng = bodo.ir.join.calc_disp(wkzk__yerm)
            iul__dcjbh = get_scatter_null_bytes_buff(sdguj__wmlt.ctypes,
                send_counts, wkzk__yerm)
            c_scatterv(iul__dcjbh.ctypes, wkzk__yerm.ctypes, dus__gdng.
                ctypes, xesnn__esq.ctypes, np.int32(mjkq__xdhkv), anud__etk)
            return fsy__oxkow(hgjl__hvgsi, xesnn__esq)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            ncqzu__fdkw = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            qnvk__fltr = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(ncqzu__fdkw,
                qnvk__fltr)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            kmmqr__yglgm = data._start
            vmqss__inkod = data._stop
            vyb__dnbl = data._step
            ppctf__mijwi = data._name
            ppctf__mijwi = bcast_scalar(ppctf__mijwi)
            kmmqr__yglgm = bcast_scalar(kmmqr__yglgm)
            vmqss__inkod = bcast_scalar(vmqss__inkod)
            vyb__dnbl = bcast_scalar(vyb__dnbl)
            sqy__tlem = bodo.libs.array_kernels.calc_nitems(kmmqr__yglgm,
                vmqss__inkod, vyb__dnbl)
            chunk_start = bodo.libs.distributed_api.get_start(sqy__tlem,
                n_pes, rank)
            ufcz__tsxv = bodo.libs.distributed_api.get_node_portion(sqy__tlem,
                n_pes, rank)
            hsykr__yhq = kmmqr__yglgm + vyb__dnbl * chunk_start
            zjk__wrmrt = kmmqr__yglgm + vyb__dnbl * (chunk_start + ufcz__tsxv)
            zjk__wrmrt = min(zjk__wrmrt, vmqss__inkod)
            return bodo.hiframes.pd_index_ext.init_range_index(hsykr__yhq,
                zjk__wrmrt, vyb__dnbl, ppctf__mijwi)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        fbp__nhkp = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            wrtc__ezd = data._data
            ppctf__mijwi = data._name
            ppctf__mijwi = bcast_scalar(ppctf__mijwi)
            arr = bodo.libs.distributed_api.scatterv_impl(wrtc__ezd,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                ppctf__mijwi, fbp__nhkp)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            wrtc__ezd = data._data
            ppctf__mijwi = data._name
            ppctf__mijwi = bcast_scalar(ppctf__mijwi)
            arr = bodo.libs.distributed_api.scatterv_impl(wrtc__ezd,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, ppctf__mijwi)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            unoz__axsqa = bodo.libs.distributed_api.scatterv_impl(data.
                _data, send_counts)
            ppctf__mijwi = bcast_scalar(data._name)
            dcec__hueod = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                unoz__axsqa, dcec__hueod, ppctf__mijwi)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ppctf__mijwi = bodo.hiframes.pd_series_ext.get_series_name(data)
            ltwqm__brvx = bcast_scalar(ppctf__mijwi)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            usiwn__zmu = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                usiwn__zmu, ltwqm__brvx)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        vlu__tzk = len(data.columns)
        pxkg__fhd = ', '.join('g_data_{}'.format(i) for i in range(vlu__tzk))
        rdds__olp = bodo.utils.transform.gen_const_tup(data.columns)
        naxjp__fohv = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(vlu__tzk):
            naxjp__fohv += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            naxjp__fohv += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        naxjp__fohv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        naxjp__fohv += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        naxjp__fohv += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(pxkg__fhd, rdds__olp))
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'bodo': bodo}, jcjqi__vaakw)
        idja__lms = jcjqi__vaakw['impl_df']
        return idja__lms
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            rtd__dsik = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                rtd__dsik, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        naxjp__fohv = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        naxjp__fohv += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'bodo': bodo}, jcjqi__vaakw)
        xno__hwm = jcjqi__vaakw['impl_tuple']
        return xno__hwm
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
        nvu__tuiod = np.int32(numba_to_c_type(offset_type))
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            rayuy__ctnfm = len(data)
            wzduc__gtqjd = num_total_chars(data)
            assert rayuy__ctnfm < INT_MAX
            assert wzduc__gtqjd < INT_MAX
            azgku__jwsqg = get_offset_ptr(data)
            owslc__kcfh = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            rvr__wvbph = rayuy__ctnfm + 7 >> 3
            c_bcast(azgku__jwsqg, np.int32(rayuy__ctnfm + 1), nvu__tuiod,
                np.array([-1]).ctypes, 0, np.int32(root))
            c_bcast(owslc__kcfh, np.int32(wzduc__gtqjd), anud__etk, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(rvr__wvbph), anud__etk, np.
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
        anud__etk = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                cgv__usfs = 0
                wysz__jbed = np.empty(0, np.uint8).ctypes
            else:
                wysz__jbed, cgv__usfs = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            cgv__usfs = bodo.libs.distributed_api.bcast_scalar(cgv__usfs, root)
            if rank != root:
                gkrjs__ehwy = np.empty(cgv__usfs + 1, np.uint8)
                gkrjs__ehwy[cgv__usfs] = 0
                wysz__jbed = gkrjs__ehwy.ctypes
            c_bcast(wysz__jbed, np.int32(cgv__usfs), anud__etk, np.array([-
                1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(wysz__jbed, cgv__usfs)
        return impl_str
    typ_val = numba_to_c_type(val)
    naxjp__fohv = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    jcjqi__vaakw = {}
    exec(naxjp__fohv, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, jcjqi__vaakw)
    umc__ftb = jcjqi__vaakw['bcast_scalar_impl']
    return umc__ftb


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    lzrhm__ptj = len(val)
    naxjp__fohv = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    naxjp__fohv += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(lzrhm__ptj)),
        ',' if lzrhm__ptj else '')
    jcjqi__vaakw = {}
    exec(naxjp__fohv, {'bcast_scalar': bcast_scalar}, jcjqi__vaakw)
    xry__hoo = jcjqi__vaakw['bcast_tuple_impl']
    return xry__hoo


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            rayuy__ctnfm = bcast_scalar(len(arr), root)
            qevz__meaxm = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(rayuy__ctnfm, qevz__meaxm)
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
        kmmqr__yglgm = slice_index.start
        vyb__dnbl = slice_index.step
        wlhi__utogb = 0 if vyb__dnbl == 1 or kmmqr__yglgm > arr_start else abs(
            vyb__dnbl - arr_start % vyb__dnbl) % vyb__dnbl
        hsykr__yhq = max(arr_start, slice_index.start
            ) - arr_start + wlhi__utogb
        zjk__wrmrt = max(slice_index.stop - arr_start, 0)
        return slice(hsykr__yhq, zjk__wrmrt, vyb__dnbl)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        eifnx__gys = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[eifnx__gys])
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
        tng__fxxc = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        anud__etk = np.int32(numba_to_c_type(types.uint8))
        qkhs__othn = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            hcl__ezu = np.int32(10)
            tag = np.int32(11)
            xtgf__ovagq = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                lbel__czdnm = arr._data
                ihnnp__erf = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    lbel__czdnm, ind)
                rwruq__lmt = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    lbel__czdnm, ind + 1)
                length = rwruq__lmt - ihnnp__erf
                nsiz__abkb = lbel__czdnm[ind]
                xtgf__ovagq[0] = length
                isend(xtgf__ovagq, np.int32(1), root, hcl__ezu, True)
                isend(nsiz__abkb, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(qkhs__othn
                , tng__fxxc, 0, 1)
            hqc__nvj = 0
            if rank == root:
                hqc__nvj = recv(np.int64, ANY_SOURCE, hcl__ezu)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    qkhs__othn, tng__fxxc, hqc__nvj, 1)
                owslc__kcfh = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(owslc__kcfh, np.int32(hqc__nvj), anud__etk,
                    ANY_SOURCE, tag)
            dummy_use(xtgf__ovagq)
            hqc__nvj = bcast_scalar(hqc__nvj)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    qkhs__othn, tng__fxxc, hqc__nvj, 1)
            owslc__kcfh = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(owslc__kcfh, np.int32(hqc__nvj), anud__etk, np.array([-
                1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, hqc__nvj)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        ywqw__dnagv = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, ywqw__dnagv)
            if arr_start <= ind < arr_start + len(arr):
                rtd__dsik = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = rtd__dsik[ind - arr_start]
                send_arr = np.full(1, data, ywqw__dnagv)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = ywqw__dnagv(-1)
            if rank == root:
                val = recv(ywqw__dnagv, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            akaeb__eee = arr.dtype.categories[max(val, 0)]
            return akaeb__eee
        return cat_getitem_impl
    ywci__ulvuz = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, ywci__ulvuz)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, ywci__ulvuz)[0]
        if rank == root:
            val = recv(ywci__ulvuz, ANY_SOURCE, tag)
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
    gdkpq__glmf = get_type_enum(out_data)
    assert typ_enum == gdkpq__glmf
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
    naxjp__fohv = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        naxjp__fohv += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    naxjp__fohv += '  return\n'
    jcjqi__vaakw = {}
    exec(naxjp__fohv, {'alltoallv': alltoallv}, jcjqi__vaakw)
    rsi__exx = jcjqi__vaakw['f']
    return rsi__exx


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    kmmqr__yglgm = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return kmmqr__yglgm, count


@numba.njit
def get_start(total_size, pes, rank):
    hhq__djpvf = total_size % pes
    qyir__kpgar = (total_size - hhq__djpvf) // pes
    return rank * qyir__kpgar + min(rank, hhq__djpvf)


@numba.njit
def get_end(total_size, pes, rank):
    hhq__djpvf = total_size % pes
    qyir__kpgar = (total_size - hhq__djpvf) // pes
    return (rank + 1) * qyir__kpgar + min(rank + 1, hhq__djpvf)


@numba.njit
def get_node_portion(total_size, pes, rank):
    hhq__djpvf = total_size % pes
    qyir__kpgar = (total_size - hhq__djpvf) // pes
    if rank < hhq__djpvf:
        return qyir__kpgar + 1
    else:
        return qyir__kpgar


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    nivd__siwx = in_arr.dtype(0)
    vwz__gvilo = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        ksj__hfbez = nivd__siwx
        for cgkgh__bwpiv in np.nditer(in_arr):
            ksj__hfbez += cgkgh__bwpiv.item()
        rkqx__oodv = dist_exscan(ksj__hfbez, vwz__gvilo)
        for i in range(in_arr.size):
            rkqx__oodv += in_arr[i]
            out_arr[i] = rkqx__oodv
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    qwxi__gyo = in_arr.dtype(1)
    vwz__gvilo = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        ksj__hfbez = qwxi__gyo
        for cgkgh__bwpiv in np.nditer(in_arr):
            ksj__hfbez *= cgkgh__bwpiv.item()
        rkqx__oodv = dist_exscan(ksj__hfbez, vwz__gvilo)
        if get_rank() == 0:
            rkqx__oodv = qwxi__gyo
        for i in range(in_arr.size):
            rkqx__oodv *= in_arr[i]
            out_arr[i] = rkqx__oodv
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        qwxi__gyo = np.finfo(in_arr.dtype(1).dtype).max
    else:
        qwxi__gyo = np.iinfo(in_arr.dtype(1).dtype).max
    vwz__gvilo = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        ksj__hfbez = qwxi__gyo
        for cgkgh__bwpiv in np.nditer(in_arr):
            ksj__hfbez = min(ksj__hfbez, cgkgh__bwpiv.item())
        rkqx__oodv = dist_exscan(ksj__hfbez, vwz__gvilo)
        if get_rank() == 0:
            rkqx__oodv = qwxi__gyo
        for i in range(in_arr.size):
            rkqx__oodv = min(rkqx__oodv, in_arr[i])
            out_arr[i] = rkqx__oodv
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        qwxi__gyo = np.finfo(in_arr.dtype(1).dtype).min
    else:
        qwxi__gyo = np.iinfo(in_arr.dtype(1).dtype).min
    qwxi__gyo = in_arr.dtype(1)
    vwz__gvilo = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        ksj__hfbez = qwxi__gyo
        for cgkgh__bwpiv in np.nditer(in_arr):
            ksj__hfbez = max(ksj__hfbez, cgkgh__bwpiv.item())
        rkqx__oodv = dist_exscan(ksj__hfbez, vwz__gvilo)
        if get_rank() == 0:
            rkqx__oodv = qwxi__gyo
        for i in range(in_arr.size):
            rkqx__oodv = max(rkqx__oodv, in_arr[i])
            out_arr[i] = rkqx__oodv
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    yigiw__exsv = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), yigiw__exsv)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    kqb__ltz = args[0]
    if equiv_set.has_shape(kqb__ltz):
        return ArrayAnalysis.AnalyzeResult(shape=kqb__ltz, pre=[])
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
    ofsyf__ybbgm = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for
        i, inj__xya in enumerate(args) if is_array_typ(inj__xya) or
        isinstance(inj__xya, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    naxjp__fohv = f"""def impl(*args):
    if {ofsyf__ybbgm} or bodo.get_rank() == 0:
        print(*args)"""
    jcjqi__vaakw = {}
    exec(naxjp__fohv, globals(), jcjqi__vaakw)
    impl = jcjqi__vaakw['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        pzg__aqilg = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        naxjp__fohv = 'def f(req, cond=True):\n'
        naxjp__fohv += f'  return {pzg__aqilg}\n'
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'_wait': _wait}, jcjqi__vaakw)
        impl = jcjqi__vaakw['f']
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
        hhq__djpvf = 1
        for a in t:
            hhq__djpvf *= a
        return hhq__djpvf
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    eeutm__uyira = np.ascontiguousarray(in_arr)
    awha__pzi = get_tuple_prod(eeutm__uyira.shape[1:])
    zwcti__hdyw = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        xvh__ghn = np.array(dest_ranks, dtype=np.int32)
    else:
        xvh__ghn = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, eeutm__uyira.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * zwcti__hdyw, 
        dtype_size * awha__pzi, len(xvh__ghn), xvh__ghn.ctypes)
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
    icc__afwr = np.ascontiguousarray(rhs)
    pnax__yyeec = get_tuple_prod(icc__afwr.shape[1:])
    fulir__xhrj = dtype_size * pnax__yyeec
    permutation_array_index(lhs.ctypes, lhs_len, fulir__xhrj, icc__afwr.
        ctypes, icc__afwr.shape[0], p.ctypes, p_len)
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
        naxjp__fohv = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, jcjqi__vaakw)
        umc__ftb = jcjqi__vaakw['bcast_scalar_impl']
        return umc__ftb
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        vlu__tzk = len(data.columns)
        pxkg__fhd = ', '.join('g_data_{}'.format(i) for i in range(vlu__tzk))
        rdds__olp = bodo.utils.transform.gen_const_tup(data.columns)
        naxjp__fohv = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(vlu__tzk):
            naxjp__fohv += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            naxjp__fohv += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        naxjp__fohv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        naxjp__fohv += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        naxjp__fohv += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(pxkg__fhd, rdds__olp))
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'bodo': bodo}, jcjqi__vaakw)
        idja__lms = jcjqi__vaakw['impl_df']
        return idja__lms
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            kmmqr__yglgm = data._start
            vmqss__inkod = data._stop
            vyb__dnbl = data._step
            ppctf__mijwi = data._name
            ppctf__mijwi = bcast_scalar(ppctf__mijwi, root)
            kmmqr__yglgm = bcast_scalar(kmmqr__yglgm, root)
            vmqss__inkod = bcast_scalar(vmqss__inkod, root)
            vyb__dnbl = bcast_scalar(vyb__dnbl, root)
            sqy__tlem = bodo.libs.array_kernels.calc_nitems(kmmqr__yglgm,
                vmqss__inkod, vyb__dnbl)
            chunk_start = bodo.libs.distributed_api.get_start(sqy__tlem,
                n_pes, rank)
            ufcz__tsxv = bodo.libs.distributed_api.get_node_portion(sqy__tlem,
                n_pes, rank)
            hsykr__yhq = kmmqr__yglgm + vyb__dnbl * chunk_start
            zjk__wrmrt = kmmqr__yglgm + vyb__dnbl * (chunk_start + ufcz__tsxv)
            zjk__wrmrt = min(zjk__wrmrt, vmqss__inkod)
            return bodo.hiframes.pd_index_ext.init_range_index(hsykr__yhq,
                zjk__wrmrt, vyb__dnbl, ppctf__mijwi)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            wrtc__ezd = data._data
            ppctf__mijwi = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(wrtc__ezd,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, ppctf__mijwi)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            ppctf__mijwi = bodo.hiframes.pd_series_ext.get_series_name(data)
            ltwqm__brvx = bodo.libs.distributed_api.bcast_comm_impl(
                ppctf__mijwi, comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            usiwn__zmu = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                usiwn__zmu, ltwqm__brvx)
        return impl_series
    if isinstance(data, types.BaseTuple):
        naxjp__fohv = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        naxjp__fohv += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        jcjqi__vaakw = {}
        exec(naxjp__fohv, {'bcast_comm_impl': bcast_comm_impl}, jcjqi__vaakw)
        xno__hwm = jcjqi__vaakw['impl_tuple']
        return xno__hwm
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    klrp__lvj = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    pkd__asme = (0,) * klrp__lvj

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        wrtc__ezd = np.ascontiguousarray(data)
        owslc__kcfh = data.ctypes
        secga__nljvm = pkd__asme
        if rank == root:
            secga__nljvm = wrtc__ezd.shape
        secga__nljvm = bcast_tuple(secga__nljvm, root)
        jpg__hcxms = get_tuple_prod(secga__nljvm[1:])
        send_counts = secga__nljvm[0] * jpg__hcxms
        yrjs__myzq = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(owslc__kcfh, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(yrjs__myzq.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return yrjs__myzq.reshape((-1,) + secga__nljvm[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        ammc__vdle = MPI.COMM_WORLD
        afu__zzj = MPI.Get_processor_name()
        ingtp__upadp = ammc__vdle.allgather(afu__zzj)
        node_ranks = defaultdict(list)
        for i, koq__tcc in enumerate(ingtp__upadp):
            node_ranks[koq__tcc].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    ammc__vdle = MPI.COMM_WORLD
    uowr__eei = ammc__vdle.Get_group()
    awjsd__gxkcn = uowr__eei.Incl(comm_ranks)
    bfgv__ssylz = ammc__vdle.Create_group(awjsd__gxkcn)
    return bfgv__ssylz


def get_nodes_first_ranks():
    vzy__san = get_host_ranks()
    return np.array([jfksz__nsts[0] for jfksz__nsts in vzy__san.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
