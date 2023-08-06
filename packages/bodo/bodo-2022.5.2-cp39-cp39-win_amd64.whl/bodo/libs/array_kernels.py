"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_overload_none, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type,
        datetime_timedelta_array_type, string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        jss__iqr = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = jss__iqr
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        jss__iqr = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = jss__iqr
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            prir__xid = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            prir__xid[ind + 1] = prir__xid[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            prir__xid = bodo.libs.array_item_arr_ext.get_offsets(arr)
            prir__xid[ind + 1] = prir__xid[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def setna_tup(arr_tup, ind, int_nan_const=0):
    for arr in arr_tup:
        arr[ind] = np.nan


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    iudm__cexd = arr_tup.count
    ptv__ebxq = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(iudm__cexd):
        ptv__ebxq += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    ptv__ebxq += '  return\n'
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'setna': setna}, sxqb__bouqd)
    impl = sxqb__bouqd['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        usas__cgmz = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(usas__cgmz.start, usas__cgmz.stop, usas__cgmz.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        urfhz__yla = 'n'
        fzvjg__izkqh = 'n_pes'
        gtq__yraag = 'min_op'
    else:
        urfhz__yla = 'n-1, -1, -1'
        fzvjg__izkqh = '-1'
        gtq__yraag = 'max_op'
    ptv__ebxq = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {fzvjg__izkqh}
    for i in range({urfhz__yla}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {gtq__yraag}))
        if possible_valid_rank != {fzvjg__izkqh}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        sxqb__bouqd)
    impl = sxqb__bouqd['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    qfc__vawye = array_to_info(arr)
    _median_series_computation(res, qfc__vawye, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(qfc__vawye)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    qfc__vawye = array_to_info(arr)
    _autocorr_series_computation(res, qfc__vawye, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(qfc__vawye)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    qfc__vawye = array_to_info(arr)
    _compute_series_monotonicity(res, qfc__vawye, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(qfc__vawye)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    glvoc__lyn = res[0] > 0.5
    return glvoc__lyn


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        rvfm__elsrb = '-'
        ezcjd__aos = 'index_arr[0] > threshhold_date'
        urfhz__yla = '1, n+1'
        yfy__chur = 'index_arr[-i] <= threshhold_date'
        byvmt__vhv = 'i - 1'
    else:
        rvfm__elsrb = '+'
        ezcjd__aos = 'index_arr[-1] < threshhold_date'
        urfhz__yla = 'n'
        yfy__chur = 'index_arr[i] >= threshhold_date'
        byvmt__vhv = 'i'
    ptv__ebxq = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        ptv__ebxq += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        ptv__ebxq += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            ptv__ebxq += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            ptv__ebxq += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            ptv__ebxq += '    else:\n'
            ptv__ebxq += '      threshhold_date = initial_date + date_offset\n'
        else:
            ptv__ebxq += (
                f'    threshhold_date = initial_date {rvfm__elsrb} date_offset\n'
                )
    else:
        ptv__ebxq += f'  threshhold_date = initial_date {rvfm__elsrb} offset\n'
    ptv__ebxq += '  local_valid = 0\n'
    ptv__ebxq += f'  n = len(index_arr)\n'
    ptv__ebxq += f'  if n:\n'
    ptv__ebxq += f'    if {ezcjd__aos}:\n'
    ptv__ebxq += '      loc_valid = n\n'
    ptv__ebxq += '    else:\n'
    ptv__ebxq += f'      for i in range({urfhz__yla}):\n'
    ptv__ebxq += f'        if {yfy__chur}:\n'
    ptv__ebxq += f'          loc_valid = {byvmt__vhv}\n'
    ptv__ebxq += '          break\n'
    ptv__ebxq += '  if is_parallel:\n'
    ptv__ebxq += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    ptv__ebxq += '    return total_valid\n'
    ptv__ebxq += '  else:\n'
    ptv__ebxq += '    return loc_valid\n'
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, sxqb__bouqd)
    return sxqb__bouqd['impl']


def quantile(A, q):
    return 0


def quantile_parallel(A, q):
    return 0


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    unrp__kurvd = numba_to_c_type(sig.args[0].dtype)
    niq__ggbt = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), unrp__kurvd))
    xoxyd__xjaml = args[0]
    bzv__jmsx = sig.args[0]
    if isinstance(bzv__jmsx, (IntegerArrayType, BooleanArrayType)):
        xoxyd__xjaml = cgutils.create_struct_proxy(bzv__jmsx)(context,
            builder, xoxyd__xjaml).data
        bzv__jmsx = types.Array(bzv__jmsx.dtype, 1, 'C')
    assert bzv__jmsx.ndim == 1
    arr = make_array(bzv__jmsx)(context, builder, xoxyd__xjaml)
    ubg__sjht = builder.extract_value(arr.shape, 0)
    lxmct__ehld = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        ubg__sjht, args[1], builder.load(niq__ggbt)]
    nyqng__owmt = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    hwh__ygimt = lir.FunctionType(lir.DoubleType(), nyqng__owmt)
    jjj__pkqqg = cgutils.get_or_insert_function(builder.module, hwh__ygimt,
        name='quantile_sequential')
    neaf__xpffn = builder.call(jjj__pkqqg, lxmct__ehld)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return neaf__xpffn


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    unrp__kurvd = numba_to_c_type(sig.args[0].dtype)
    niq__ggbt = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), unrp__kurvd))
    xoxyd__xjaml = args[0]
    bzv__jmsx = sig.args[0]
    if isinstance(bzv__jmsx, (IntegerArrayType, BooleanArrayType)):
        xoxyd__xjaml = cgutils.create_struct_proxy(bzv__jmsx)(context,
            builder, xoxyd__xjaml).data
        bzv__jmsx = types.Array(bzv__jmsx.dtype, 1, 'C')
    assert bzv__jmsx.ndim == 1
    arr = make_array(bzv__jmsx)(context, builder, xoxyd__xjaml)
    ubg__sjht = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        vcgbe__hkgv = args[2]
    else:
        vcgbe__hkgv = ubg__sjht
    lxmct__ehld = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        ubg__sjht, vcgbe__hkgv, args[1], builder.load(niq__ggbt)]
    nyqng__owmt = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    hwh__ygimt = lir.FunctionType(lir.DoubleType(), nyqng__owmt)
    jjj__pkqqg = cgutils.get_or_insert_function(builder.module, hwh__ygimt,
        name='quantile_parallel')
    neaf__xpffn = builder.call(jjj__pkqqg, lxmct__ehld)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return neaf__xpffn


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    twyzj__wrezy = start
    vkhgn__eysd = 2 * start + 1
    vbzmx__jinp = 2 * start + 2
    if vkhgn__eysd < n and not cmp_f(arr[vkhgn__eysd], arr[twyzj__wrezy]):
        twyzj__wrezy = vkhgn__eysd
    if vbzmx__jinp < n and not cmp_f(arr[vbzmx__jinp], arr[twyzj__wrezy]):
        twyzj__wrezy = vbzmx__jinp
    if twyzj__wrezy != start:
        arr[start], arr[twyzj__wrezy] = arr[twyzj__wrezy], arr[start]
        ind_arr[start], ind_arr[twyzj__wrezy] = ind_arr[twyzj__wrezy], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, twyzj__wrezy, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        bvv__con = np.empty(k, A.dtype)
        swv__vpa = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                bvv__con[ind] = A[i]
                swv__vpa[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            bvv__con = bvv__con[:ind]
            swv__vpa = swv__vpa[:ind]
        return bvv__con, swv__vpa, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        ttncv__gqby = np.sort(A)
        msd__acee = index_arr[np.argsort(A)]
        ebf__lbt = pd.Series(ttncv__gqby).notna().values
        ttncv__gqby = ttncv__gqby[ebf__lbt]
        msd__acee = msd__acee[ebf__lbt]
        if is_largest:
            ttncv__gqby = ttncv__gqby[::-1]
            msd__acee = msd__acee[::-1]
        return np.ascontiguousarray(ttncv__gqby), np.ascontiguousarray(
            msd__acee)
    bvv__con, swv__vpa, start = select_k_nonan(A, index_arr, m, k)
    swv__vpa = swv__vpa[bvv__con.argsort()]
    bvv__con.sort()
    if not is_largest:
        bvv__con = np.ascontiguousarray(bvv__con[::-1])
        swv__vpa = np.ascontiguousarray(swv__vpa[::-1])
    for i in range(start, m):
        if cmp_f(A[i], bvv__con[0]):
            bvv__con[0] = A[i]
            swv__vpa[0] = index_arr[i]
            min_heapify(bvv__con, swv__vpa, k, 0, cmp_f)
    swv__vpa = swv__vpa[bvv__con.argsort()]
    bvv__con.sort()
    if is_largest:
        bvv__con = bvv__con[::-1]
        swv__vpa = swv__vpa[::-1]
    return np.ascontiguousarray(bvv__con), np.ascontiguousarray(swv__vpa)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    aejww__gyfw = bodo.libs.distributed_api.get_rank()
    eakp__man, pokj__uqml = nlargest(A, I, k, is_largest, cmp_f)
    qtfyh__lrha = bodo.libs.distributed_api.gatherv(eakp__man)
    ykqar__vaka = bodo.libs.distributed_api.gatherv(pokj__uqml)
    if aejww__gyfw == MPI_ROOT:
        res, rtbn__blyn = nlargest(qtfyh__lrha, ykqar__vaka, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        rtbn__blyn = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(rtbn__blyn)
    return res, rtbn__blyn


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    hjljb__dvzu, aef__jzpkl = mat.shape
    ufz__lhz = np.empty((aef__jzpkl, aef__jzpkl), dtype=np.float64)
    for vpva__pgh in range(aef__jzpkl):
        for jdlki__qltvc in range(vpva__pgh + 1):
            zohd__jkcok = 0
            rkm__endt = akwv__tacq = ttqnx__rkiyj = siof__luo = 0.0
            for i in range(hjljb__dvzu):
                if np.isfinite(mat[i, vpva__pgh]) and np.isfinite(mat[i,
                    jdlki__qltvc]):
                    bbr__eitjz = mat[i, vpva__pgh]
                    nlr__mtiy = mat[i, jdlki__qltvc]
                    zohd__jkcok += 1
                    ttqnx__rkiyj += bbr__eitjz
                    siof__luo += nlr__mtiy
            if parallel:
                zohd__jkcok = bodo.libs.distributed_api.dist_reduce(zohd__jkcok
                    , sum_op)
                ttqnx__rkiyj = bodo.libs.distributed_api.dist_reduce(
                    ttqnx__rkiyj, sum_op)
                siof__luo = bodo.libs.distributed_api.dist_reduce(siof__luo,
                    sum_op)
            if zohd__jkcok < minpv:
                ufz__lhz[vpva__pgh, jdlki__qltvc] = ufz__lhz[jdlki__qltvc,
                    vpva__pgh] = np.nan
            else:
                lip__wrg = ttqnx__rkiyj / zohd__jkcok
                xeyn__urnc = siof__luo / zohd__jkcok
                ttqnx__rkiyj = 0.0
                for i in range(hjljb__dvzu):
                    if np.isfinite(mat[i, vpva__pgh]) and np.isfinite(mat[i,
                        jdlki__qltvc]):
                        bbr__eitjz = mat[i, vpva__pgh] - lip__wrg
                        nlr__mtiy = mat[i, jdlki__qltvc] - xeyn__urnc
                        ttqnx__rkiyj += bbr__eitjz * nlr__mtiy
                        rkm__endt += bbr__eitjz * bbr__eitjz
                        akwv__tacq += nlr__mtiy * nlr__mtiy
                if parallel:
                    ttqnx__rkiyj = bodo.libs.distributed_api.dist_reduce(
                        ttqnx__rkiyj, sum_op)
                    rkm__endt = bodo.libs.distributed_api.dist_reduce(rkm__endt
                        , sum_op)
                    akwv__tacq = bodo.libs.distributed_api.dist_reduce(
                        akwv__tacq, sum_op)
                tjh__yqt = zohd__jkcok - 1.0 if cov else sqrt(rkm__endt *
                    akwv__tacq)
                if tjh__yqt != 0.0:
                    ufz__lhz[vpva__pgh, jdlki__qltvc] = ufz__lhz[
                        jdlki__qltvc, vpva__pgh] = ttqnx__rkiyj / tjh__yqt
                else:
                    ufz__lhz[vpva__pgh, jdlki__qltvc] = ufz__lhz[
                        jdlki__qltvc, vpva__pgh] = np.nan
    return ufz__lhz


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    oiq__slo = n != 1
    ptv__ebxq = 'def impl(data, parallel=False):\n'
    ptv__ebxq += '  if parallel:\n'
    mkwbb__yeu = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    ptv__ebxq += f'    cpp_table = arr_info_list_to_table([{mkwbb__yeu}])\n'
    ptv__ebxq += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    ibxv__sjpbu = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    ptv__ebxq += f'    data = ({ibxv__sjpbu},)\n'
    ptv__ebxq += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    ptv__ebxq += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    ptv__ebxq += '    bodo.libs.array.delete_table(cpp_table)\n'
    ptv__ebxq += '  n = len(data[0])\n'
    ptv__ebxq += '  out = np.empty(n, np.bool_)\n'
    ptv__ebxq += '  uniqs = dict()\n'
    if oiq__slo:
        ptv__ebxq += '  for i in range(n):\n'
        bygka__frcpd = ', '.join(f'data[{i}][i]' for i in range(n))
        dvpea__tvpr = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        ptv__ebxq += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({bygka__frcpd},), ({dvpea__tvpr},))
"""
        ptv__ebxq += '    if val in uniqs:\n'
        ptv__ebxq += '      out[i] = True\n'
        ptv__ebxq += '    else:\n'
        ptv__ebxq += '      out[i] = False\n'
        ptv__ebxq += '      uniqs[val] = 0\n'
    else:
        ptv__ebxq += '  data = data[0]\n'
        ptv__ebxq += '  hasna = False\n'
        ptv__ebxq += '  for i in range(n):\n'
        ptv__ebxq += '    if bodo.libs.array_kernels.isna(data, i):\n'
        ptv__ebxq += '      out[i] = hasna\n'
        ptv__ebxq += '      hasna = True\n'
        ptv__ebxq += '    else:\n'
        ptv__ebxq += '      val = data[i]\n'
        ptv__ebxq += '      if val in uniqs:\n'
        ptv__ebxq += '        out[i] = True\n'
        ptv__ebxq += '      else:\n'
        ptv__ebxq += '        out[i] = False\n'
        ptv__ebxq += '        uniqs[val] = 0\n'
    ptv__ebxq += '  if parallel:\n'
    ptv__ebxq += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    ptv__ebxq += '  return out\n'
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, sxqb__bouqd)
    impl = sxqb__bouqd['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    iudm__cexd = len(data)
    ptv__ebxq = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    ptv__ebxq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        iudm__cexd)))
    ptv__ebxq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    ptv__ebxq += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(iudm__cexd))
    for fxgkr__kil in range(iudm__cexd):
        ptv__ebxq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(fxgkr__kil, fxgkr__kil, fxgkr__kil))
    ptv__ebxq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(iudm__cexd))
    ptv__ebxq += '  delete_table(out_table)\n'
    ptv__ebxq += '  delete_table(table_total)\n'
    ptv__ebxq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(iudm__cexd)))
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, sxqb__bouqd)
    impl = sxqb__bouqd['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    iudm__cexd = len(data)
    ptv__ebxq = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    ptv__ebxq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        iudm__cexd)))
    ptv__ebxq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    ptv__ebxq += '  keep_i = 0\n'
    ptv__ebxq += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for fxgkr__kil in range(iudm__cexd):
        ptv__ebxq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(fxgkr__kil, fxgkr__kil, fxgkr__kil))
    ptv__ebxq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(iudm__cexd))
    ptv__ebxq += '  delete_table(out_table)\n'
    ptv__ebxq += '  delete_table(table_total)\n'
    ptv__ebxq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(iudm__cexd)))
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, sxqb__bouqd)
    impl = sxqb__bouqd['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        dhl__jdw = [array_to_info(data_arr)]
        jnuij__aas = arr_info_list_to_table(dhl__jdw)
        kmc__dymv = 0
        qbe__taynv = drop_duplicates_table(jnuij__aas, parallel, 1,
            kmc__dymv, False, True)
        zdkzz__vvmul = info_to_array(info_from_table(qbe__taynv, 0), data_arr)
        delete_table(qbe__taynv)
        delete_table(jnuij__aas)
        return zdkzz__vvmul
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    fzg__uxsqi = len(data.types)
    seek__but = [('out' + str(i)) for i in range(fzg__uxsqi)]
    iqcsh__kdm = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    sxlvi__pgc = ['isna(data[{}], i)'.format(i) for i in iqcsh__kdm]
    umqa__pti = 'not ({})'.format(' or '.join(sxlvi__pgc))
    if not is_overload_none(thresh):
        umqa__pti = '(({}) <= ({}) - thresh)'.format(' + '.join(sxlvi__pgc),
            fzg__uxsqi - 1)
    elif how == 'all':
        umqa__pti = 'not ({})'.format(' and '.join(sxlvi__pgc))
    ptv__ebxq = 'def _dropna_imp(data, how, thresh, subset):\n'
    ptv__ebxq += '  old_len = len(data[0])\n'
    ptv__ebxq += '  new_len = 0\n'
    ptv__ebxq += '  for i in range(old_len):\n'
    ptv__ebxq += '    if {}:\n'.format(umqa__pti)
    ptv__ebxq += '      new_len += 1\n'
    for i, out in enumerate(seek__but):
        if isinstance(data[i], bodo.CategoricalArrayType):
            ptv__ebxq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            ptv__ebxq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    ptv__ebxq += '  curr_ind = 0\n'
    ptv__ebxq += '  for i in range(old_len):\n'
    ptv__ebxq += '    if {}:\n'.format(umqa__pti)
    for i in range(fzg__uxsqi):
        ptv__ebxq += '      if isna(data[{}], i):\n'.format(i)
        ptv__ebxq += '        setna({}, curr_ind)\n'.format(seek__but[i])
        ptv__ebxq += '      else:\n'
        ptv__ebxq += '        {}[curr_ind] = data[{}][i]\n'.format(seek__but
            [i], i)
    ptv__ebxq += '      curr_ind += 1\n'
    ptv__ebxq += '  return {}\n'.format(', '.join(seek__but))
    sxqb__bouqd = {}
    feug__miuqs = {'t{}'.format(i): roj__uhty for i, roj__uhty in enumerate
        (data.types)}
    feug__miuqs.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(ptv__ebxq, feug__miuqs, sxqb__bouqd)
    yxzmn__pcqpm = sxqb__bouqd['_dropna_imp']
    return yxzmn__pcqpm


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        bzv__jmsx = arr.dtype
        majzj__rbrlr = bzv__jmsx.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            sbm__fyer = init_nested_counts(majzj__rbrlr)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                sbm__fyer = add_nested_counts(sbm__fyer, val[ind])
            zdkzz__vvmul = bodo.utils.utils.alloc_type(n, bzv__jmsx, sbm__fyer)
            for bojqp__viy in range(n):
                if bodo.libs.array_kernels.isna(arr, bojqp__viy):
                    setna(zdkzz__vvmul, bojqp__viy)
                    continue
                val = arr[bojqp__viy]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(zdkzz__vvmul, bojqp__viy)
                    continue
                zdkzz__vvmul[bojqp__viy] = val[ind]
            return zdkzz__vvmul
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    hpych__cmduv = _to_readonly(arr_types.types[0])
    return all(isinstance(roj__uhty, CategoricalArrayType) and _to_readonly
        (roj__uhty) == hpych__cmduv for roj__uhty in arr_types.types)


def concat(arr_list):
    return pd.concat(arr_list)


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arr_list.
        dtype, 'bodo.concat()')
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        siqkz__twa = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            inz__yabf = 0
            hmrih__huadd = []
            for A in arr_list:
                xyitr__iei = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                hmrih__huadd.append(bodo.libs.array_item_arr_ext.get_data(A))
                inz__yabf += xyitr__iei
            zlojz__dxa = np.empty(inz__yabf + 1, offset_type)
            uebb__ixixw = bodo.libs.array_kernels.concat(hmrih__huadd)
            teat__brcj = np.empty(inz__yabf + 7 >> 3, np.uint8)
            zpyea__wett = 0
            bix__etk = 0
            for A in arr_list:
                rpfki__hqiz = bodo.libs.array_item_arr_ext.get_offsets(A)
                kul__rnnh = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                xyitr__iei = len(A)
                riuja__ovph = rpfki__hqiz[xyitr__iei]
                for i in range(xyitr__iei):
                    zlojz__dxa[i + zpyea__wett] = rpfki__hqiz[i] + bix__etk
                    tssrw__wtcu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        kul__rnnh, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(teat__brcj, i +
                        zpyea__wett, tssrw__wtcu)
                zpyea__wett += xyitr__iei
                bix__etk += riuja__ovph
            zlojz__dxa[zpyea__wett] = bix__etk
            zdkzz__vvmul = bodo.libs.array_item_arr_ext.init_array_item_array(
                inz__yabf, uebb__ixixw, zlojz__dxa, teat__brcj)
            return zdkzz__vvmul
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        tufxo__jxgs = arr_list.dtype.names
        ptv__ebxq = 'def struct_array_concat_impl(arr_list):\n'
        ptv__ebxq += f'    n_all = 0\n'
        for i in range(len(tufxo__jxgs)):
            ptv__ebxq += f'    concat_list{i} = []\n'
        ptv__ebxq += '    for A in arr_list:\n'
        ptv__ebxq += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(tufxo__jxgs)):
            ptv__ebxq += f'        concat_list{i}.append(data_tuple[{i}])\n'
        ptv__ebxq += '        n_all += len(A)\n'
        ptv__ebxq += '    n_bytes = (n_all + 7) >> 3\n'
        ptv__ebxq += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        ptv__ebxq += '    curr_bit = 0\n'
        ptv__ebxq += '    for A in arr_list:\n'
        ptv__ebxq += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        ptv__ebxq += '        for j in range(len(A)):\n'
        ptv__ebxq += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        ptv__ebxq += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        ptv__ebxq += '            curr_bit += 1\n'
        ptv__ebxq += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        egtub__tfls = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(tufxo__jxgs))])
        ptv__ebxq += f'        ({egtub__tfls},),\n'
        ptv__ebxq += '        new_mask,\n'
        ptv__ebxq += f'        {tufxo__jxgs},\n'
        ptv__ebxq += '    )\n'
        sxqb__bouqd = {}
        exec(ptv__ebxq, {'bodo': bodo, 'np': np}, sxqb__bouqd)
        return sxqb__bouqd['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            diws__gta = 0
            for A in arr_list:
                diws__gta += len(A)
            nxyld__dqvn = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(diws__gta))
            ygonb__iqhg = 0
            for A in arr_list:
                for i in range(len(A)):
                    nxyld__dqvn._data[i + ygonb__iqhg] = A._data[i]
                    tssrw__wtcu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nxyld__dqvn.
                        _null_bitmap, i + ygonb__iqhg, tssrw__wtcu)
                ygonb__iqhg += len(A)
            return nxyld__dqvn
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            diws__gta = 0
            for A in arr_list:
                diws__gta += len(A)
            nxyld__dqvn = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(diws__gta))
            ygonb__iqhg = 0
            for A in arr_list:
                for i in range(len(A)):
                    nxyld__dqvn._days_data[i + ygonb__iqhg] = A._days_data[i]
                    nxyld__dqvn._seconds_data[i + ygonb__iqhg
                        ] = A._seconds_data[i]
                    nxyld__dqvn._microseconds_data[i + ygonb__iqhg
                        ] = A._microseconds_data[i]
                    tssrw__wtcu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nxyld__dqvn.
                        _null_bitmap, i + ygonb__iqhg, tssrw__wtcu)
                ygonb__iqhg += len(A)
            return nxyld__dqvn
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        cyfis__uabi = arr_list.dtype.precision
        rda__mhym = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            diws__gta = 0
            for A in arr_list:
                diws__gta += len(A)
            nxyld__dqvn = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                diws__gta, cyfis__uabi, rda__mhym)
            ygonb__iqhg = 0
            for A in arr_list:
                for i in range(len(A)):
                    nxyld__dqvn._data[i + ygonb__iqhg] = A._data[i]
                    tssrw__wtcu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nxyld__dqvn.
                        _null_bitmap, i + ygonb__iqhg, tssrw__wtcu)
                ygonb__iqhg += len(A)
            return nxyld__dqvn
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        roj__uhty) for roj__uhty in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            zxy__tfsqw = arr_list.types[0]
        else:
            zxy__tfsqw = arr_list.dtype
        zxy__tfsqw = to_str_arr_if_dict_array(zxy__tfsqw)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            iyk__qwggs = 0
            gxnzf__zoqt = 0
            for A in arr_list:
                arr = A
                iyk__qwggs += len(arr)
                gxnzf__zoqt += bodo.libs.str_arr_ext.num_total_chars(arr)
            zdkzz__vvmul = bodo.utils.utils.alloc_type(iyk__qwggs,
                zxy__tfsqw, (gxnzf__zoqt,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(zdkzz__vvmul, -1)
            ddzv__fiv = 0
            auvge__usku = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(zdkzz__vvmul,
                    arr, ddzv__fiv, auvge__usku)
                ddzv__fiv += len(arr)
                auvge__usku += bodo.libs.str_arr_ext.num_total_chars(arr)
            return zdkzz__vvmul
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(roj__uhty.dtype, types.Integer) for
        roj__uhty in arr_list.types) and any(isinstance(roj__uhty,
        IntegerArrayType) for roj__uhty in arr_list.types):

        def impl_int_arr_list(arr_list):
            kuf__yfhf = convert_to_nullable_tup(arr_list)
            uyd__azdx = []
            aayb__ycb = 0
            for A in kuf__yfhf:
                uyd__azdx.append(A._data)
                aayb__ycb += len(A)
            uebb__ixixw = bodo.libs.array_kernels.concat(uyd__azdx)
            gfte__tutdr = aayb__ycb + 7 >> 3
            gteo__xork = np.empty(gfte__tutdr, np.uint8)
            ubcwz__dlq = 0
            for A in kuf__yfhf:
                yomb__hinqi = A._null_bitmap
                for bojqp__viy in range(len(A)):
                    tssrw__wtcu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        yomb__hinqi, bojqp__viy)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gteo__xork,
                        ubcwz__dlq, tssrw__wtcu)
                    ubcwz__dlq += 1
            return bodo.libs.int_arr_ext.init_integer_array(uebb__ixixw,
                gteo__xork)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(roj__uhty.dtype == types.bool_ for roj__uhty in
        arr_list.types) and any(roj__uhty == boolean_array for roj__uhty in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            kuf__yfhf = convert_to_nullable_tup(arr_list)
            uyd__azdx = []
            aayb__ycb = 0
            for A in kuf__yfhf:
                uyd__azdx.append(A._data)
                aayb__ycb += len(A)
            uebb__ixixw = bodo.libs.array_kernels.concat(uyd__azdx)
            gfte__tutdr = aayb__ycb + 7 >> 3
            gteo__xork = np.empty(gfte__tutdr, np.uint8)
            ubcwz__dlq = 0
            for A in kuf__yfhf:
                yomb__hinqi = A._null_bitmap
                for bojqp__viy in range(len(A)):
                    tssrw__wtcu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        yomb__hinqi, bojqp__viy)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gteo__xork,
                        ubcwz__dlq, tssrw__wtcu)
                    ubcwz__dlq += 1
            return bodo.libs.bool_arr_ext.init_bool_array(uebb__ixixw,
                gteo__xork)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            tebe__cneqj = []
            for A in arr_list:
                tebe__cneqj.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                tebe__cneqj), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        iujdl__pxvkp = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        ptv__ebxq = 'def impl(arr_list):\n'
        ptv__ebxq += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({iujdl__pxvkp},)), arr_list[0].dtype)
"""
        yeyfz__qfc = {}
        exec(ptv__ebxq, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, yeyfz__qfc)
        return yeyfz__qfc['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            aayb__ycb = 0
            for A in arr_list:
                aayb__ycb += len(A)
            zdkzz__vvmul = np.empty(aayb__ycb, dtype)
            hrkcd__zcj = 0
            for A in arr_list:
                n = len(A)
                zdkzz__vvmul[hrkcd__zcj:hrkcd__zcj + n] = A
                hrkcd__zcj += n
            return zdkzz__vvmul
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(roj__uhty,
        (types.Array, IntegerArrayType)) and isinstance(roj__uhty.dtype,
        types.Integer) for roj__uhty in arr_list.types) and any(isinstance(
        roj__uhty, types.Array) and isinstance(roj__uhty.dtype, types.Float
        ) for roj__uhty in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            icowb__zlz = []
            for A in arr_list:
                icowb__zlz.append(A._data)
            rcddt__wlzpc = bodo.libs.array_kernels.concat(icowb__zlz)
            ufz__lhz = bodo.libs.map_arr_ext.init_map_arr(rcddt__wlzpc)
            return ufz__lhz
        return impl_map_arr_list
    for fnvre__vciv in arr_list:
        if not isinstance(fnvre__vciv, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(roj__uhty.astype(np.float64) for roj__uhty in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    iudm__cexd = len(arr_tup.types)
    ptv__ebxq = 'def f(arr_tup):\n'
    ptv__ebxq += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        iudm__cexd)), ',' if iudm__cexd == 1 else '')
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'np': np}, sxqb__bouqd)
    xrco__mgudx = sxqb__bouqd['f']
    return xrco__mgudx


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    iudm__cexd = len(arr_tup.types)
    rix__prfgl = find_common_np_dtype(arr_tup.types)
    majzj__rbrlr = None
    vlo__opp = ''
    if isinstance(rix__prfgl, types.Integer):
        majzj__rbrlr = bodo.libs.int_arr_ext.IntDtype(rix__prfgl)
        vlo__opp = '.astype(out_dtype, False)'
    ptv__ebxq = 'def f(arr_tup):\n'
    ptv__ebxq += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, vlo__opp) for i in range(iudm__cexd)), ',' if iudm__cexd ==
        1 else '')
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'bodo': bodo, 'out_dtype': majzj__rbrlr}, sxqb__bouqd)
    zjyd__bai = sxqb__bouqd['f']
    return zjyd__bai


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, kptzj__zinf = build_set_seen_na(A)
        return len(s) + int(not dropna and kptzj__zinf)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        knvs__rdhx = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        kivb__tbym = len(knvs__rdhx)
        return bodo.libs.distributed_api.dist_reduce(kivb__tbym, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([vsg__msqsb for vsg__msqsb in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        dsau__psrp = np.finfo(A.dtype(1).dtype).max
    else:
        dsau__psrp = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        zdkzz__vvmul = np.empty(n, A.dtype)
        tyxvc__tzmw = dsau__psrp
        for i in range(n):
            tyxvc__tzmw = min(tyxvc__tzmw, A[i])
            zdkzz__vvmul[i] = tyxvc__tzmw
        return zdkzz__vvmul
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        dsau__psrp = np.finfo(A.dtype(1).dtype).min
    else:
        dsau__psrp = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        zdkzz__vvmul = np.empty(n, A.dtype)
        tyxvc__tzmw = dsau__psrp
        for i in range(n):
            tyxvc__tzmw = max(tyxvc__tzmw, A[i])
            zdkzz__vvmul[i] = tyxvc__tzmw
        return zdkzz__vvmul
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        vbhi__eiwmk = arr_info_list_to_table([array_to_info(A)])
        rcy__stq = 1
        kmc__dymv = 0
        qbe__taynv = drop_duplicates_table(vbhi__eiwmk, parallel, rcy__stq,
            kmc__dymv, dropna, True)
        zdkzz__vvmul = info_to_array(info_from_table(qbe__taynv, 0), A)
        delete_table(vbhi__eiwmk)
        delete_table(qbe__taynv)
        return zdkzz__vvmul
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    siqkz__twa = bodo.utils.typing.to_nullable_type(arr.dtype)
    lrl__jetv = index_arr
    axjok__gfwk = lrl__jetv.dtype

    def impl(arr, index_arr):
        n = len(arr)
        sbm__fyer = init_nested_counts(siqkz__twa)
        hywg__lyyv = init_nested_counts(axjok__gfwk)
        for i in range(n):
            dpz__kiosc = index_arr[i]
            if isna(arr, i):
                sbm__fyer = (sbm__fyer[0] + 1,) + sbm__fyer[1:]
                hywg__lyyv = add_nested_counts(hywg__lyyv, dpz__kiosc)
                continue
            yiep__bqp = arr[i]
            if len(yiep__bqp) == 0:
                sbm__fyer = (sbm__fyer[0] + 1,) + sbm__fyer[1:]
                hywg__lyyv = add_nested_counts(hywg__lyyv, dpz__kiosc)
                continue
            sbm__fyer = add_nested_counts(sbm__fyer, yiep__bqp)
            for swq__qjvw in range(len(yiep__bqp)):
                hywg__lyyv = add_nested_counts(hywg__lyyv, dpz__kiosc)
        zdkzz__vvmul = bodo.utils.utils.alloc_type(sbm__fyer[0], siqkz__twa,
            sbm__fyer[1:])
        boba__vzut = bodo.utils.utils.alloc_type(sbm__fyer[0], lrl__jetv,
            hywg__lyyv)
        bix__etk = 0
        for i in range(n):
            if isna(arr, i):
                setna(zdkzz__vvmul, bix__etk)
                boba__vzut[bix__etk] = index_arr[i]
                bix__etk += 1
                continue
            yiep__bqp = arr[i]
            riuja__ovph = len(yiep__bqp)
            if riuja__ovph == 0:
                setna(zdkzz__vvmul, bix__etk)
                boba__vzut[bix__etk] = index_arr[i]
                bix__etk += 1
                continue
            zdkzz__vvmul[bix__etk:bix__etk + riuja__ovph] = yiep__bqp
            boba__vzut[bix__etk:bix__etk + riuja__ovph] = index_arr[i]
            bix__etk += riuja__ovph
        return zdkzz__vvmul, boba__vzut
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    siqkz__twa = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        sbm__fyer = init_nested_counts(siqkz__twa)
        for i in range(n):
            if isna(arr, i):
                sbm__fyer = (sbm__fyer[0] + 1,) + sbm__fyer[1:]
                ivpn__gklw = 1
            else:
                yiep__bqp = arr[i]
                jzpw__sgjn = len(yiep__bqp)
                if jzpw__sgjn == 0:
                    sbm__fyer = (sbm__fyer[0] + 1,) + sbm__fyer[1:]
                    ivpn__gklw = 1
                    continue
                else:
                    sbm__fyer = add_nested_counts(sbm__fyer, yiep__bqp)
                    ivpn__gklw = jzpw__sgjn
            if counts[i] != ivpn__gklw:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        zdkzz__vvmul = bodo.utils.utils.alloc_type(sbm__fyer[0], siqkz__twa,
            sbm__fyer[1:])
        bix__etk = 0
        for i in range(n):
            if isna(arr, i):
                setna(zdkzz__vvmul, bix__etk)
                bix__etk += 1
                continue
            yiep__bqp = arr[i]
            riuja__ovph = len(yiep__bqp)
            if riuja__ovph == 0:
                setna(zdkzz__vvmul, bix__etk)
                bix__etk += 1
                continue
            zdkzz__vvmul[bix__etk:bix__etk + riuja__ovph] = yiep__bqp
            bix__etk += riuja__ovph
        return zdkzz__vvmul
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(mzo__loek) for mzo__loek in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        fsn__diz = 'np.empty(n, np.int64)'
        dsaqw__stdc = 'out_arr[i] = 1'
        cmsd__ttbw = 'max(len(arr[i]), 1)'
    else:
        fsn__diz = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        dsaqw__stdc = 'bodo.libs.array_kernels.setna(out_arr, i)'
        cmsd__ttbw = 'len(arr[i])'
    ptv__ebxq = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {fsn__diz}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {dsaqw__stdc}
        else:
            out_arr[i] = {cmsd__ttbw}
    return out_arr
    """
    sxqb__bouqd = {}
    exec(ptv__ebxq, {'bodo': bodo, 'numba': numba, 'np': np}, sxqb__bouqd)
    impl = sxqb__bouqd['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    lrl__jetv = index_arr
    axjok__gfwk = lrl__jetv.dtype

    def impl(arr, pat, n, index_arr):
        zwgf__igi = pat is not None and len(pat) > 1
        if zwgf__igi:
            hhqcy__dcjj = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        kjmy__boc = len(arr)
        iyk__qwggs = 0
        gxnzf__zoqt = 0
        hywg__lyyv = init_nested_counts(axjok__gfwk)
        for i in range(kjmy__boc):
            dpz__kiosc = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                iyk__qwggs += 1
                hywg__lyyv = add_nested_counts(hywg__lyyv, dpz__kiosc)
                continue
            if zwgf__igi:
                hpn__qwynz = hhqcy__dcjj.split(arr[i], maxsplit=n)
            else:
                hpn__qwynz = arr[i].split(pat, n)
            iyk__qwggs += len(hpn__qwynz)
            for s in hpn__qwynz:
                hywg__lyyv = add_nested_counts(hywg__lyyv, dpz__kiosc)
                gxnzf__zoqt += bodo.libs.str_arr_ext.get_utf8_size(s)
        zdkzz__vvmul = bodo.libs.str_arr_ext.pre_alloc_string_array(iyk__qwggs,
            gxnzf__zoqt)
        boba__vzut = bodo.utils.utils.alloc_type(iyk__qwggs, lrl__jetv,
            hywg__lyyv)
        hipm__srnuf = 0
        for bojqp__viy in range(kjmy__boc):
            if isna(arr, bojqp__viy):
                zdkzz__vvmul[hipm__srnuf] = ''
                bodo.libs.array_kernels.setna(zdkzz__vvmul, hipm__srnuf)
                boba__vzut[hipm__srnuf] = index_arr[bojqp__viy]
                hipm__srnuf += 1
                continue
            if zwgf__igi:
                hpn__qwynz = hhqcy__dcjj.split(arr[bojqp__viy], maxsplit=n)
            else:
                hpn__qwynz = arr[bojqp__viy].split(pat, n)
            gkx__bwt = len(hpn__qwynz)
            zdkzz__vvmul[hipm__srnuf:hipm__srnuf + gkx__bwt] = hpn__qwynz
            boba__vzut[hipm__srnuf:hipm__srnuf + gkx__bwt] = index_arr[
                bojqp__viy]
            hipm__srnuf += gkx__bwt
        return zdkzz__vvmul, boba__vzut
    return impl


def gen_na_array(n, arr):
    return np.full(n, np.nan)


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr):
            numba.parfors.parfor.init_prange()
            zdkzz__vvmul = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                zdkzz__vvmul[i] = np.nan
            return zdkzz__vvmul
        return impl_float
    wij__xnmdi = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        zdkzz__vvmul = bodo.utils.utils.alloc_type(n, wij__xnmdi, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(zdkzz__vvmul, i)
        return zdkzz__vvmul
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    return A


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    sgm__jud = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            zdkzz__vvmul = bodo.utils.utils.alloc_type(new_len, sgm__jud)
            bodo.libs.str_arr_ext.str_copy_ptr(zdkzz__vvmul.ctypes, 0, A.
                ctypes, old_size)
            return zdkzz__vvmul
        return impl_char

    def impl(A, old_size, new_len):
        zdkzz__vvmul = bodo.utils.utils.alloc_type(new_len, sgm__jud, (-1,))
        zdkzz__vvmul[:old_size] = A[:old_size]
        return zdkzz__vvmul
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    cmge__lnjn = math.ceil((stop - start) / step)
    return int(max(cmge__lnjn, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(vsg__msqsb, types.Complex) for vsg__msqsb in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            nuu__rhdm = (stop - start) / step
            cmge__lnjn = math.ceil(nuu__rhdm.real)
            psoi__mst = math.ceil(nuu__rhdm.imag)
            biob__vmqno = int(max(min(psoi__mst, cmge__lnjn), 0))
            arr = np.empty(biob__vmqno, dtype)
            for i in numba.parfors.parfor.internal_prange(biob__vmqno):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            biob__vmqno = bodo.libs.array_kernels.calc_nitems(start, stop, step
                )
            arr = np.empty(biob__vmqno, dtype)
            for i in numba.parfors.parfor.internal_prange(biob__vmqno):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    return np.sort(arr)


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        rwtu__pnumi = arr,
        if not inplace:
            rwtu__pnumi = arr.copy(),
        agr__aymay = bodo.libs.str_arr_ext.to_list_if_immutable_arr(rwtu__pnumi
            )
        yph__bqzdo = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(agr__aymay, 0, n, yph__bqzdo)
        if not ascending:
            bodo.libs.timsort.reverseRange(agr__aymay, 0, n, yph__bqzdo)
        bodo.libs.str_arr_ext.cp_str_list_to_array(rwtu__pnumi, agr__aymay)
        return rwtu__pnumi[0]
    return impl


def overload_array_max(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    return arr,


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        ufz__lhz = []
        for i in range(n):
            if A[i]:
                ufz__lhz.append(i + offset)
        return np.array(ufz__lhz, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    sgm__jud = element_type(A)
    if sgm__jud == types.unicode_type:
        null_value = '""'
    elif sgm__jud == types.bool_:
        null_value = 'False'
    elif sgm__jud == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif sgm__jud == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    hipm__srnuf = 'i'
    qwa__yottn = False
    ebsix__lffxg = get_overload_const_str(method)
    if ebsix__lffxg in ('ffill', 'pad'):
        zowrz__yvub = 'n'
        send_right = True
    elif ebsix__lffxg in ('backfill', 'bfill'):
        zowrz__yvub = 'n-1, -1, -1'
        send_right = False
        if sgm__jud == types.unicode_type:
            hipm__srnuf = '(n - 1) - i'
            qwa__yottn = True
    ptv__ebxq = 'def impl(A, method, parallel=False):\n'
    ptv__ebxq += '  A = decode_if_dict_array(A)\n'
    ptv__ebxq += '  has_last_value = False\n'
    ptv__ebxq += f'  last_value = {null_value}\n'
    ptv__ebxq += '  if parallel:\n'
    ptv__ebxq += '    rank = bodo.libs.distributed_api.get_rank()\n'
    ptv__ebxq += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    ptv__ebxq += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    ptv__ebxq += '  n = len(A)\n'
    ptv__ebxq += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    ptv__ebxq += f'  for i in range({zowrz__yvub}):\n'
    ptv__ebxq += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    ptv__ebxq += (
        f'      bodo.libs.array_kernels.setna(out_arr, {hipm__srnuf})\n')
    ptv__ebxq += '      continue\n'
    ptv__ebxq += '    s = A[i]\n'
    ptv__ebxq += '    if bodo.libs.array_kernels.isna(A, i):\n'
    ptv__ebxq += '      s = last_value\n'
    ptv__ebxq += f'    out_arr[{hipm__srnuf}] = s\n'
    ptv__ebxq += '    last_value = s\n'
    ptv__ebxq += '    has_last_value = True\n'
    if qwa__yottn:
        ptv__ebxq += '  return out_arr[::-1]\n'
    else:
        ptv__ebxq += '  return out_arr\n'
    uti__ulrfp = {}
    exec(ptv__ebxq, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, uti__ulrfp)
    impl = uti__ulrfp['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        wodxe__dexk = 0
        lvn__nask = n_pes - 1
        xylna__xto = np.int32(rank + 1)
        xhgj__gofu = np.int32(rank - 1)
        ubr__sfdr = len(in_arr) - 1
        afkdj__nbu = -1
        vvz__smy = -1
    else:
        wodxe__dexk = n_pes - 1
        lvn__nask = 0
        xylna__xto = np.int32(rank - 1)
        xhgj__gofu = np.int32(rank + 1)
        ubr__sfdr = 0
        afkdj__nbu = len(in_arr)
        vvz__smy = 1
    ojjm__xqm = np.int32(bodo.hiframes.rolling.comm_border_tag)
    vky__tzidu = np.empty(1, dtype=np.bool_)
    coqnw__trjwx = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    knrlc__gtkw = np.empty(1, dtype=np.bool_)
    jmn__smxi = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    oyr__unv = False
    pgt__mtfph = null_value
    for i in range(ubr__sfdr, afkdj__nbu, vvz__smy):
        if not isna(in_arr, i):
            oyr__unv = True
            pgt__mtfph = in_arr[i]
            break
    if rank != wodxe__dexk:
        clrkd__nvq = bodo.libs.distributed_api.irecv(vky__tzidu, 1,
            xhgj__gofu, ojjm__xqm, True)
        bodo.libs.distributed_api.wait(clrkd__nvq, True)
        ugl__sputm = bodo.libs.distributed_api.irecv(coqnw__trjwx, 1,
            xhgj__gofu, ojjm__xqm, True)
        bodo.libs.distributed_api.wait(ugl__sputm, True)
        xqg__fux = vky__tzidu[0]
        gmb__zoku = coqnw__trjwx[0]
    else:
        xqg__fux = False
        gmb__zoku = null_value
    if oyr__unv:
        knrlc__gtkw[0] = oyr__unv
        jmn__smxi[0] = pgt__mtfph
    else:
        knrlc__gtkw[0] = xqg__fux
        jmn__smxi[0] = gmb__zoku
    if rank != lvn__nask:
        juyc__azziz = bodo.libs.distributed_api.isend(knrlc__gtkw, 1,
            xylna__xto, ojjm__xqm, True)
        goc__moki = bodo.libs.distributed_api.isend(jmn__smxi, 1,
            xylna__xto, ojjm__xqm, True)
    return xqg__fux, gmb__zoku


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    rsau__fvdl = {'axis': axis, 'kind': kind, 'order': order}
    lfsp__wkks = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', rsau__fvdl, lfsp__wkks, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    sgm__jud = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            kjmy__boc = len(A)
            zdkzz__vvmul = bodo.utils.utils.alloc_type(kjmy__boc * repeats,
                sgm__jud, (-1,))
            for i in range(kjmy__boc):
                hipm__srnuf = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for bojqp__viy in range(repeats):
                        bodo.libs.array_kernels.setna(zdkzz__vvmul, 
                            hipm__srnuf + bojqp__viy)
                else:
                    zdkzz__vvmul[hipm__srnuf:hipm__srnuf + repeats] = A[i]
            return zdkzz__vvmul
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        kjmy__boc = len(A)
        zdkzz__vvmul = bodo.utils.utils.alloc_type(repeats.sum(), sgm__jud,
            (-1,))
        hipm__srnuf = 0
        for i in range(kjmy__boc):
            jycuh__lar = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for bojqp__viy in range(jycuh__lar):
                    bodo.libs.array_kernels.setna(zdkzz__vvmul, hipm__srnuf +
                        bojqp__viy)
            else:
                zdkzz__vvmul[hipm__srnuf:hipm__srnuf + jycuh__lar] = A[i]
            hipm__srnuf += jycuh__lar
        return zdkzz__vvmul
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        bge__suki = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(bge__suki, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        ris__thkt = bodo.libs.array_kernels.concat([A1, A2])
        pemf__egfwy = bodo.libs.array_kernels.unique(ris__thkt)
        return pd.Series(pemf__egfwy).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    rsau__fvdl = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    lfsp__wkks = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', rsau__fvdl, lfsp__wkks, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        asns__fshmm = bodo.libs.array_kernels.unique(A1)
        vqemb__lmmu = bodo.libs.array_kernels.unique(A2)
        ris__thkt = bodo.libs.array_kernels.concat([asns__fshmm, vqemb__lmmu])
        qzfc__hdx = pd.Series(ris__thkt).sort_values().values
        return slice_array_intersect1d(qzfc__hdx)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    ebf__lbt = arr[1:] == arr[:-1]
    return arr[:-1][ebf__lbt]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    rsau__fvdl = {'assume_unique': assume_unique}
    lfsp__wkks = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', rsau__fvdl, lfsp__wkks, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        asns__fshmm = bodo.libs.array_kernels.unique(A1)
        vqemb__lmmu = bodo.libs.array_kernels.unique(A2)
        ebf__lbt = calculate_mask_setdiff1d(asns__fshmm, vqemb__lmmu)
        return pd.Series(asns__fshmm[ebf__lbt]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    ebf__lbt = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        ebf__lbt &= A1 != A2[i]
    return ebf__lbt


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    rsau__fvdl = {'retstep': retstep, 'axis': axis}
    lfsp__wkks = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', rsau__fvdl, lfsp__wkks, 'numpy')
    hcqz__ozye = False
    if is_overload_none(dtype):
        sgm__jud = np.promote_types(np.promote_types(numba.np.numpy_support
            .as_dtype(start), numba.np.numpy_support.as_dtype(stop)), numba
            .np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            hcqz__ozye = True
        sgm__jud = numba.np.numpy_support.as_dtype(dtype).type
    if hcqz__ozye:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            ntzdt__ctr = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            zdkzz__vvmul = np.empty(num, sgm__jud)
            for i in numba.parfors.parfor.internal_prange(num):
                zdkzz__vvmul[i] = sgm__jud(np.floor(start + i * ntzdt__ctr))
            return zdkzz__vvmul
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            ntzdt__ctr = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            zdkzz__vvmul = np.empty(num, sgm__jud)
            for i in numba.parfors.parfor.internal_prange(num):
                zdkzz__vvmul[i] = sgm__jud(start + i * ntzdt__ctr)
            return zdkzz__vvmul
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        iudm__cexd = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                iudm__cexd += A[i] == val
        return iudm__cexd > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    rsau__fvdl = {'axis': axis, 'out': out, 'keepdims': keepdims}
    lfsp__wkks = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', rsau__fvdl, lfsp__wkks, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        iudm__cexd = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                iudm__cexd += int(bool(A[i]))
        return iudm__cexd > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    rsau__fvdl = {'axis': axis, 'out': out, 'keepdims': keepdims}
    lfsp__wkks = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', rsau__fvdl, lfsp__wkks, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        iudm__cexd = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                iudm__cexd += int(bool(A[i]))
        return iudm__cexd == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    rsau__fvdl = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    lfsp__wkks = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', rsau__fvdl, lfsp__wkks, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        beot__wpbs = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            zdkzz__vvmul = np.empty(n, beot__wpbs)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(zdkzz__vvmul, i)
                    continue
                zdkzz__vvmul[i] = np_cbrt_scalar(A[i], beot__wpbs)
            return zdkzz__vvmul
        return impl_arr
    beot__wpbs = np.promote_types(numba.np.numpy_support.as_dtype(A), numba
        .np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, beot__wpbs)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    iufwc__crzwe = x < 0
    if iufwc__crzwe:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if iufwc__crzwe:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    hjf__acwn = isinstance(tup, (types.BaseTuple, types.List))
    hye__whgm = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for fnvre__vciv in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                fnvre__vciv, 'numpy.hstack()')
            hjf__acwn = hjf__acwn and bodo.utils.utils.is_array_typ(fnvre__vciv
                , False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        hjf__acwn = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif hye__whgm:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        xgdia__wiza = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for fnvre__vciv in xgdia__wiza.types:
            hye__whgm = hye__whgm and bodo.utils.utils.is_array_typ(fnvre__vciv
                , False)
    if not (hjf__acwn or hye__whgm):
        return
    if hye__whgm:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    rsau__fvdl = {'check_valid': check_valid, 'tol': tol}
    lfsp__wkks = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', rsau__fvdl,
        lfsp__wkks, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        hjljb__dvzu = mean.shape[0]
        aynvg__ykvt = size, hjljb__dvzu
        rmfl__dvx = np.random.standard_normal(aynvg__ykvt)
        cov = cov.astype(np.float64)
        zuwy__wct, s, gsttu__zjvqk = np.linalg.svd(cov)
        res = np.dot(rmfl__dvx, np.sqrt(s).reshape(hjljb__dvzu, 1) *
            gsttu__zjvqk)
        yon__kxo = res + mean
        return yon__kxo
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            fzvjg__izkqh = bodo.hiframes.series_kernels._get_type_max_value(arr
                )
            xcx__nqd = typing.builtins.IndexValue(-1, fzvjg__izkqh)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xolw__xqpb = typing.builtins.IndexValue(i, arr[i])
                xcx__nqd = min(xcx__nqd, xolw__xqpb)
            return xcx__nqd.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        mvmpo__kqqye = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            ypc__nta = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            fzvjg__izkqh = mvmpo__kqqye(len(arr.dtype.categories) + 1)
            xcx__nqd = typing.builtins.IndexValue(-1, fzvjg__izkqh)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xolw__xqpb = typing.builtins.IndexValue(i, ypc__nta[i])
                xcx__nqd = min(xcx__nqd, xolw__xqpb)
            return xcx__nqd.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            fzvjg__izkqh = bodo.hiframes.series_kernels._get_type_min_value(arr
                )
            xcx__nqd = typing.builtins.IndexValue(-1, fzvjg__izkqh)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xolw__xqpb = typing.builtins.IndexValue(i, arr[i])
                xcx__nqd = max(xcx__nqd, xolw__xqpb)
            return xcx__nqd.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        mvmpo__kqqye = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            n = len(arr)
            ypc__nta = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            fzvjg__izkqh = mvmpo__kqqye(-1)
            xcx__nqd = typing.builtins.IndexValue(-1, fzvjg__izkqh)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xolw__xqpb = typing.builtins.IndexValue(i, ypc__nta[i])
                xcx__nqd = max(xcx__nqd, xolw__xqpb)
            return xcx__nqd.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
