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
        vim__njel = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = vim__njel
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        vim__njel = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = vim__njel
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
            qxkjc__ddeeb = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            qxkjc__ddeeb[ind + 1] = qxkjc__ddeeb[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            qxkjc__ddeeb = bodo.libs.array_item_arr_ext.get_offsets(arr)
            qxkjc__ddeeb[ind + 1] = qxkjc__ddeeb[ind]
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
    vmuta__acyj = arr_tup.count
    axbx__kbz = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(vmuta__acyj):
        axbx__kbz += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    axbx__kbz += '  return\n'
    qaupu__oeqx = {}
    exec(axbx__kbz, {'setna': setna}, qaupu__oeqx)
    impl = qaupu__oeqx['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        jgza__reo = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(jgza__reo.start, jgza__reo.stop, jgza__reo.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        iaacd__edkv = 'n'
        cgcdg__bmusf = 'n_pes'
        wyrkt__ljvhg = 'min_op'
    else:
        iaacd__edkv = 'n-1, -1, -1'
        cgcdg__bmusf = '-1'
        wyrkt__ljvhg = 'max_op'
    axbx__kbz = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {cgcdg__bmusf}
    for i in range({iaacd__edkv}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {wyrkt__ljvhg}))
        if possible_valid_rank != {cgcdg__bmusf}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    qaupu__oeqx = {}
    exec(axbx__kbz, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        qaupu__oeqx)
    impl = qaupu__oeqx['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    xqr__qnjxl = array_to_info(arr)
    _median_series_computation(res, xqr__qnjxl, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xqr__qnjxl)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    xqr__qnjxl = array_to_info(arr)
    _autocorr_series_computation(res, xqr__qnjxl, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xqr__qnjxl)


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
    xqr__qnjxl = array_to_info(arr)
    _compute_series_monotonicity(res, xqr__qnjxl, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xqr__qnjxl)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    xgb__cad = res[0] > 0.5
    return xgb__cad


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        scme__pyci = '-'
        uaiyb__lngae = 'index_arr[0] > threshhold_date'
        iaacd__edkv = '1, n+1'
        oanl__qxfuh = 'index_arr[-i] <= threshhold_date'
        zpmd__sib = 'i - 1'
    else:
        scme__pyci = '+'
        uaiyb__lngae = 'index_arr[-1] < threshhold_date'
        iaacd__edkv = 'n'
        oanl__qxfuh = 'index_arr[i] >= threshhold_date'
        zpmd__sib = 'i'
    axbx__kbz = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        axbx__kbz += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        axbx__kbz += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            axbx__kbz += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            axbx__kbz += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            axbx__kbz += '    else:\n'
            axbx__kbz += '      threshhold_date = initial_date + date_offset\n'
        else:
            axbx__kbz += (
                f'    threshhold_date = initial_date {scme__pyci} date_offset\n'
                )
    else:
        axbx__kbz += f'  threshhold_date = initial_date {scme__pyci} offset\n'
    axbx__kbz += '  local_valid = 0\n'
    axbx__kbz += f'  n = len(index_arr)\n'
    axbx__kbz += f'  if n:\n'
    axbx__kbz += f'    if {uaiyb__lngae}:\n'
    axbx__kbz += '      loc_valid = n\n'
    axbx__kbz += '    else:\n'
    axbx__kbz += f'      for i in range({iaacd__edkv}):\n'
    axbx__kbz += f'        if {oanl__qxfuh}:\n'
    axbx__kbz += f'          loc_valid = {zpmd__sib}\n'
    axbx__kbz += '          break\n'
    axbx__kbz += '  if is_parallel:\n'
    axbx__kbz += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    axbx__kbz += '    return total_valid\n'
    axbx__kbz += '  else:\n'
    axbx__kbz += '    return loc_valid\n'
    qaupu__oeqx = {}
    exec(axbx__kbz, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, qaupu__oeqx)
    return qaupu__oeqx['impl']


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
    nvah__njrcw = numba_to_c_type(sig.args[0].dtype)
    elhps__asbr = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), nvah__njrcw))
    zor__adwt = args[0]
    wlbt__aox = sig.args[0]
    if isinstance(wlbt__aox, (IntegerArrayType, BooleanArrayType)):
        zor__adwt = cgutils.create_struct_proxy(wlbt__aox)(context, builder,
            zor__adwt).data
        wlbt__aox = types.Array(wlbt__aox.dtype, 1, 'C')
    assert wlbt__aox.ndim == 1
    arr = make_array(wlbt__aox)(context, builder, zor__adwt)
    eju__jtwa = builder.extract_value(arr.shape, 0)
    qxwzi__ayud = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        eju__jtwa, args[1], builder.load(elhps__asbr)]
    aqeia__gvgi = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    vjt__skxv = lir.FunctionType(lir.DoubleType(), aqeia__gvgi)
    hflv__vbjdo = cgutils.get_or_insert_function(builder.module, vjt__skxv,
        name='quantile_sequential')
    lkbki__dwmb = builder.call(hflv__vbjdo, qxwzi__ayud)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return lkbki__dwmb


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    nvah__njrcw = numba_to_c_type(sig.args[0].dtype)
    elhps__asbr = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), nvah__njrcw))
    zor__adwt = args[0]
    wlbt__aox = sig.args[0]
    if isinstance(wlbt__aox, (IntegerArrayType, BooleanArrayType)):
        zor__adwt = cgutils.create_struct_proxy(wlbt__aox)(context, builder,
            zor__adwt).data
        wlbt__aox = types.Array(wlbt__aox.dtype, 1, 'C')
    assert wlbt__aox.ndim == 1
    arr = make_array(wlbt__aox)(context, builder, zor__adwt)
    eju__jtwa = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        vdbyk__eimom = args[2]
    else:
        vdbyk__eimom = eju__jtwa
    qxwzi__ayud = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        eju__jtwa, vdbyk__eimom, args[1], builder.load(elhps__asbr)]
    aqeia__gvgi = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    vjt__skxv = lir.FunctionType(lir.DoubleType(), aqeia__gvgi)
    hflv__vbjdo = cgutils.get_or_insert_function(builder.module, vjt__skxv,
        name='quantile_parallel')
    lkbki__dwmb = builder.call(hflv__vbjdo, qxwzi__ayud)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return lkbki__dwmb


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    qpv__low = start
    frjw__cihz = 2 * start + 1
    weuwz__wgnk = 2 * start + 2
    if frjw__cihz < n and not cmp_f(arr[frjw__cihz], arr[qpv__low]):
        qpv__low = frjw__cihz
    if weuwz__wgnk < n and not cmp_f(arr[weuwz__wgnk], arr[qpv__low]):
        qpv__low = weuwz__wgnk
    if qpv__low != start:
        arr[start], arr[qpv__low] = arr[qpv__low], arr[start]
        ind_arr[start], ind_arr[qpv__low] = ind_arr[qpv__low], ind_arr[start]
        min_heapify(arr, ind_arr, n, qpv__low, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        riajy__lhyhn = np.empty(k, A.dtype)
        edmq__jwge = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                riajy__lhyhn[ind] = A[i]
                edmq__jwge[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            riajy__lhyhn = riajy__lhyhn[:ind]
            edmq__jwge = edmq__jwge[:ind]
        return riajy__lhyhn, edmq__jwge, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        axv__rtwtp = np.sort(A)
        iqxc__ebpcv = index_arr[np.argsort(A)]
        yomt__imt = pd.Series(axv__rtwtp).notna().values
        axv__rtwtp = axv__rtwtp[yomt__imt]
        iqxc__ebpcv = iqxc__ebpcv[yomt__imt]
        if is_largest:
            axv__rtwtp = axv__rtwtp[::-1]
            iqxc__ebpcv = iqxc__ebpcv[::-1]
        return np.ascontiguousarray(axv__rtwtp), np.ascontiguousarray(
            iqxc__ebpcv)
    riajy__lhyhn, edmq__jwge, start = select_k_nonan(A, index_arr, m, k)
    edmq__jwge = edmq__jwge[riajy__lhyhn.argsort()]
    riajy__lhyhn.sort()
    if not is_largest:
        riajy__lhyhn = np.ascontiguousarray(riajy__lhyhn[::-1])
        edmq__jwge = np.ascontiguousarray(edmq__jwge[::-1])
    for i in range(start, m):
        if cmp_f(A[i], riajy__lhyhn[0]):
            riajy__lhyhn[0] = A[i]
            edmq__jwge[0] = index_arr[i]
            min_heapify(riajy__lhyhn, edmq__jwge, k, 0, cmp_f)
    edmq__jwge = edmq__jwge[riajy__lhyhn.argsort()]
    riajy__lhyhn.sort()
    if is_largest:
        riajy__lhyhn = riajy__lhyhn[::-1]
        edmq__jwge = edmq__jwge[::-1]
    return np.ascontiguousarray(riajy__lhyhn), np.ascontiguousarray(edmq__jwge)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    qrnvi__nrhkw = bodo.libs.distributed_api.get_rank()
    qcgc__glbl, udn__fxcwg = nlargest(A, I, k, is_largest, cmp_f)
    mwhyh__ycmop = bodo.libs.distributed_api.gatherv(qcgc__glbl)
    bfr__jvqz = bodo.libs.distributed_api.gatherv(udn__fxcwg)
    if qrnvi__nrhkw == MPI_ROOT:
        res, dny__fsu = nlargest(mwhyh__ycmop, bfr__jvqz, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        dny__fsu = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(dny__fsu)
    return res, dny__fsu


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    fqna__ibhsd, zmski__vcncx = mat.shape
    wqv__bhs = np.empty((zmski__vcncx, zmski__vcncx), dtype=np.float64)
    for xdfb__snxu in range(zmski__vcncx):
        for sem__kzr in range(xdfb__snxu + 1):
            xogtn__czi = 0
            tmnz__tiiz = egpv__afay = uqh__pfhix = lnlc__kogxa = 0.0
            for i in range(fqna__ibhsd):
                if np.isfinite(mat[i, xdfb__snxu]) and np.isfinite(mat[i,
                    sem__kzr]):
                    nap__wrgqu = mat[i, xdfb__snxu]
                    qmtbo__fwi = mat[i, sem__kzr]
                    xogtn__czi += 1
                    uqh__pfhix += nap__wrgqu
                    lnlc__kogxa += qmtbo__fwi
            if parallel:
                xogtn__czi = bodo.libs.distributed_api.dist_reduce(xogtn__czi,
                    sum_op)
                uqh__pfhix = bodo.libs.distributed_api.dist_reduce(uqh__pfhix,
                    sum_op)
                lnlc__kogxa = bodo.libs.distributed_api.dist_reduce(lnlc__kogxa
                    , sum_op)
            if xogtn__czi < minpv:
                wqv__bhs[xdfb__snxu, sem__kzr] = wqv__bhs[sem__kzr, xdfb__snxu
                    ] = np.nan
            else:
                cahgs__mkocs = uqh__pfhix / xogtn__czi
                sjnl__dmp = lnlc__kogxa / xogtn__czi
                uqh__pfhix = 0.0
                for i in range(fqna__ibhsd):
                    if np.isfinite(mat[i, xdfb__snxu]) and np.isfinite(mat[
                        i, sem__kzr]):
                        nap__wrgqu = mat[i, xdfb__snxu] - cahgs__mkocs
                        qmtbo__fwi = mat[i, sem__kzr] - sjnl__dmp
                        uqh__pfhix += nap__wrgqu * qmtbo__fwi
                        tmnz__tiiz += nap__wrgqu * nap__wrgqu
                        egpv__afay += qmtbo__fwi * qmtbo__fwi
                if parallel:
                    uqh__pfhix = bodo.libs.distributed_api.dist_reduce(
                        uqh__pfhix, sum_op)
                    tmnz__tiiz = bodo.libs.distributed_api.dist_reduce(
                        tmnz__tiiz, sum_op)
                    egpv__afay = bodo.libs.distributed_api.dist_reduce(
                        egpv__afay, sum_op)
                qixyc__opwxy = xogtn__czi - 1.0 if cov else sqrt(tmnz__tiiz *
                    egpv__afay)
                if qixyc__opwxy != 0.0:
                    wqv__bhs[xdfb__snxu, sem__kzr] = wqv__bhs[sem__kzr,
                        xdfb__snxu] = uqh__pfhix / qixyc__opwxy
                else:
                    wqv__bhs[xdfb__snxu, sem__kzr] = wqv__bhs[sem__kzr,
                        xdfb__snxu] = np.nan
    return wqv__bhs


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    ycc__fpc = n != 1
    axbx__kbz = 'def impl(data, parallel=False):\n'
    axbx__kbz += '  if parallel:\n'
    mvwf__qaxh = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    axbx__kbz += f'    cpp_table = arr_info_list_to_table([{mvwf__qaxh}])\n'
    axbx__kbz += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    ybpm__embzh = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    axbx__kbz += f'    data = ({ybpm__embzh},)\n'
    axbx__kbz += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    axbx__kbz += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    axbx__kbz += '    bodo.libs.array.delete_table(cpp_table)\n'
    axbx__kbz += '  n = len(data[0])\n'
    axbx__kbz += '  out = np.empty(n, np.bool_)\n'
    axbx__kbz += '  uniqs = dict()\n'
    if ycc__fpc:
        axbx__kbz += '  for i in range(n):\n'
        iinf__bbu = ', '.join(f'data[{i}][i]' for i in range(n))
        ifct__pfrg = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        axbx__kbz += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({iinf__bbu},), ({ifct__pfrg},))
"""
        axbx__kbz += '    if val in uniqs:\n'
        axbx__kbz += '      out[i] = True\n'
        axbx__kbz += '    else:\n'
        axbx__kbz += '      out[i] = False\n'
        axbx__kbz += '      uniqs[val] = 0\n'
    else:
        axbx__kbz += '  data = data[0]\n'
        axbx__kbz += '  hasna = False\n'
        axbx__kbz += '  for i in range(n):\n'
        axbx__kbz += '    if bodo.libs.array_kernels.isna(data, i):\n'
        axbx__kbz += '      out[i] = hasna\n'
        axbx__kbz += '      hasna = True\n'
        axbx__kbz += '    else:\n'
        axbx__kbz += '      val = data[i]\n'
        axbx__kbz += '      if val in uniqs:\n'
        axbx__kbz += '        out[i] = True\n'
        axbx__kbz += '      else:\n'
        axbx__kbz += '        out[i] = False\n'
        axbx__kbz += '        uniqs[val] = 0\n'
    axbx__kbz += '  if parallel:\n'
    axbx__kbz += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    axbx__kbz += '  return out\n'
    qaupu__oeqx = {}
    exec(axbx__kbz, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, qaupu__oeqx)
    impl = qaupu__oeqx['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    vmuta__acyj = len(data)
    axbx__kbz = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    axbx__kbz += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        vmuta__acyj)))
    axbx__kbz += '  table_total = arr_info_list_to_table(info_list_total)\n'
    axbx__kbz += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(vmuta__acyj))
    for jmhli__irtd in range(vmuta__acyj):
        axbx__kbz += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(jmhli__irtd, jmhli__irtd, jmhli__irtd))
    axbx__kbz += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(vmuta__acyj))
    axbx__kbz += '  delete_table(out_table)\n'
    axbx__kbz += '  delete_table(table_total)\n'
    axbx__kbz += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(vmuta__acyj)))
    qaupu__oeqx = {}
    exec(axbx__kbz, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, qaupu__oeqx)
    impl = qaupu__oeqx['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    vmuta__acyj = len(data)
    axbx__kbz = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    axbx__kbz += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        vmuta__acyj)))
    axbx__kbz += '  table_total = arr_info_list_to_table(info_list_total)\n'
    axbx__kbz += '  keep_i = 0\n'
    axbx__kbz += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for jmhli__irtd in range(vmuta__acyj):
        axbx__kbz += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(jmhli__irtd, jmhli__irtd, jmhli__irtd))
    axbx__kbz += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(vmuta__acyj))
    axbx__kbz += '  delete_table(out_table)\n'
    axbx__kbz += '  delete_table(table_total)\n'
    axbx__kbz += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(vmuta__acyj)))
    qaupu__oeqx = {}
    exec(axbx__kbz, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, qaupu__oeqx)
    impl = qaupu__oeqx['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        myb__tky = [array_to_info(data_arr)]
        gdi__lefj = arr_info_list_to_table(myb__tky)
        vavke__qkjd = 0
        wtnx__gdy = drop_duplicates_table(gdi__lefj, parallel, 1,
            vavke__qkjd, False, True)
        zlgyy__fbtlu = info_to_array(info_from_table(wtnx__gdy, 0), data_arr)
        delete_table(wtnx__gdy)
        delete_table(gdi__lefj)
        return zlgyy__fbtlu
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    pqtle__wvczw = len(data.types)
    lkdmi__kog = [('out' + str(i)) for i in range(pqtle__wvczw)]
    rbrl__nmx = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    memp__zduxp = ['isna(data[{}], i)'.format(i) for i in rbrl__nmx]
    mzu__ludiu = 'not ({})'.format(' or '.join(memp__zduxp))
    if not is_overload_none(thresh):
        mzu__ludiu = '(({}) <= ({}) - thresh)'.format(' + '.join(
            memp__zduxp), pqtle__wvczw - 1)
    elif how == 'all':
        mzu__ludiu = 'not ({})'.format(' and '.join(memp__zduxp))
    axbx__kbz = 'def _dropna_imp(data, how, thresh, subset):\n'
    axbx__kbz += '  old_len = len(data[0])\n'
    axbx__kbz += '  new_len = 0\n'
    axbx__kbz += '  for i in range(old_len):\n'
    axbx__kbz += '    if {}:\n'.format(mzu__ludiu)
    axbx__kbz += '      new_len += 1\n'
    for i, out in enumerate(lkdmi__kog):
        if isinstance(data[i], bodo.CategoricalArrayType):
            axbx__kbz += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            axbx__kbz += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    axbx__kbz += '  curr_ind = 0\n'
    axbx__kbz += '  for i in range(old_len):\n'
    axbx__kbz += '    if {}:\n'.format(mzu__ludiu)
    for i in range(pqtle__wvczw):
        axbx__kbz += '      if isna(data[{}], i):\n'.format(i)
        axbx__kbz += '        setna({}, curr_ind)\n'.format(lkdmi__kog[i])
        axbx__kbz += '      else:\n'
        axbx__kbz += '        {}[curr_ind] = data[{}][i]\n'.format(lkdmi__kog
            [i], i)
    axbx__kbz += '      curr_ind += 1\n'
    axbx__kbz += '  return {}\n'.format(', '.join(lkdmi__kog))
    qaupu__oeqx = {}
    xueft__bkrp = {'t{}'.format(i): ddc__iej for i, ddc__iej in enumerate(
        data.types)}
    xueft__bkrp.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(axbx__kbz, xueft__bkrp, qaupu__oeqx)
    kjvlf__ram = qaupu__oeqx['_dropna_imp']
    return kjvlf__ram


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        wlbt__aox = arr.dtype
        uwvvg__xmiko = wlbt__aox.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            tppv__wpzsi = init_nested_counts(uwvvg__xmiko)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                tppv__wpzsi = add_nested_counts(tppv__wpzsi, val[ind])
            zlgyy__fbtlu = bodo.utils.utils.alloc_type(n, wlbt__aox,
                tppv__wpzsi)
            for jmq__ach in range(n):
                if bodo.libs.array_kernels.isna(arr, jmq__ach):
                    setna(zlgyy__fbtlu, jmq__ach)
                    continue
                val = arr[jmq__ach]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(zlgyy__fbtlu, jmq__ach)
                    continue
                zlgyy__fbtlu[jmq__ach] = val[ind]
            return zlgyy__fbtlu
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    ajd__ddel = _to_readonly(arr_types.types[0])
    return all(isinstance(ddc__iej, CategoricalArrayType) and _to_readonly(
        ddc__iej) == ajd__ddel for ddc__iej in arr_types.types)


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
        wblez__vtkn = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            asox__wapbl = 0
            xgcfx__mzei = []
            for A in arr_list:
                pdfoy__mcyh = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                xgcfx__mzei.append(bodo.libs.array_item_arr_ext.get_data(A))
                asox__wapbl += pdfoy__mcyh
            xslof__kbkuj = np.empty(asox__wapbl + 1, offset_type)
            ocyt__blfp = bodo.libs.array_kernels.concat(xgcfx__mzei)
            oesft__pfdxo = np.empty(asox__wapbl + 7 >> 3, np.uint8)
            tpo__ovlr = 0
            poba__rmfb = 0
            for A in arr_list:
                toxf__cjc = bodo.libs.array_item_arr_ext.get_offsets(A)
                znc__rsz = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                pdfoy__mcyh = len(A)
                ded__ewcqx = toxf__cjc[pdfoy__mcyh]
                for i in range(pdfoy__mcyh):
                    xslof__kbkuj[i + tpo__ovlr] = toxf__cjc[i] + poba__rmfb
                    letng__bpjpw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        znc__rsz, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(oesft__pfdxo, i +
                        tpo__ovlr, letng__bpjpw)
                tpo__ovlr += pdfoy__mcyh
                poba__rmfb += ded__ewcqx
            xslof__kbkuj[tpo__ovlr] = poba__rmfb
            zlgyy__fbtlu = bodo.libs.array_item_arr_ext.init_array_item_array(
                asox__wapbl, ocyt__blfp, xslof__kbkuj, oesft__pfdxo)
            return zlgyy__fbtlu
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        owu__dltwv = arr_list.dtype.names
        axbx__kbz = 'def struct_array_concat_impl(arr_list):\n'
        axbx__kbz += f'    n_all = 0\n'
        for i in range(len(owu__dltwv)):
            axbx__kbz += f'    concat_list{i} = []\n'
        axbx__kbz += '    for A in arr_list:\n'
        axbx__kbz += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(owu__dltwv)):
            axbx__kbz += f'        concat_list{i}.append(data_tuple[{i}])\n'
        axbx__kbz += '        n_all += len(A)\n'
        axbx__kbz += '    n_bytes = (n_all + 7) >> 3\n'
        axbx__kbz += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        axbx__kbz += '    curr_bit = 0\n'
        axbx__kbz += '    for A in arr_list:\n'
        axbx__kbz += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        axbx__kbz += '        for j in range(len(A)):\n'
        axbx__kbz += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        axbx__kbz += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        axbx__kbz += '            curr_bit += 1\n'
        axbx__kbz += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        znlb__jcl = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(owu__dltwv))])
        axbx__kbz += f'        ({znlb__jcl},),\n'
        axbx__kbz += '        new_mask,\n'
        axbx__kbz += f'        {owu__dltwv},\n'
        axbx__kbz += '    )\n'
        qaupu__oeqx = {}
        exec(axbx__kbz, {'bodo': bodo, 'np': np}, qaupu__oeqx)
        return qaupu__oeqx['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            xjbgr__qttb = 0
            for A in arr_list:
                xjbgr__qttb += len(A)
            mik__pwmgk = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(xjbgr__qttb))
            sefgo__bzwgl = 0
            for A in arr_list:
                for i in range(len(A)):
                    mik__pwmgk._data[i + sefgo__bzwgl] = A._data[i]
                    letng__bpjpw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mik__pwmgk.
                        _null_bitmap, i + sefgo__bzwgl, letng__bpjpw)
                sefgo__bzwgl += len(A)
            return mik__pwmgk
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            xjbgr__qttb = 0
            for A in arr_list:
                xjbgr__qttb += len(A)
            mik__pwmgk = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(xjbgr__qttb))
            sefgo__bzwgl = 0
            for A in arr_list:
                for i in range(len(A)):
                    mik__pwmgk._days_data[i + sefgo__bzwgl] = A._days_data[i]
                    mik__pwmgk._seconds_data[i + sefgo__bzwgl
                        ] = A._seconds_data[i]
                    mik__pwmgk._microseconds_data[i + sefgo__bzwgl
                        ] = A._microseconds_data[i]
                    letng__bpjpw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mik__pwmgk.
                        _null_bitmap, i + sefgo__bzwgl, letng__bpjpw)
                sefgo__bzwgl += len(A)
            return mik__pwmgk
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        kij__jmqr = arr_list.dtype.precision
        xxs__ukyt = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            xjbgr__qttb = 0
            for A in arr_list:
                xjbgr__qttb += len(A)
            mik__pwmgk = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                xjbgr__qttb, kij__jmqr, xxs__ukyt)
            sefgo__bzwgl = 0
            for A in arr_list:
                for i in range(len(A)):
                    mik__pwmgk._data[i + sefgo__bzwgl] = A._data[i]
                    letng__bpjpw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mik__pwmgk.
                        _null_bitmap, i + sefgo__bzwgl, letng__bpjpw)
                sefgo__bzwgl += len(A)
            return mik__pwmgk
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        ddc__iej) for ddc__iej in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            ijyf__ein = arr_list.types[0]
        else:
            ijyf__ein = arr_list.dtype
        ijyf__ein = to_str_arr_if_dict_array(ijyf__ein)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            luyl__kulah = 0
            mdajd__xer = 0
            for A in arr_list:
                arr = A
                luyl__kulah += len(arr)
                mdajd__xer += bodo.libs.str_arr_ext.num_total_chars(arr)
            zlgyy__fbtlu = bodo.utils.utils.alloc_type(luyl__kulah,
                ijyf__ein, (mdajd__xer,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(zlgyy__fbtlu, -1)
            gjyd__xersm = 0
            krpjc__kabn = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(zlgyy__fbtlu,
                    arr, gjyd__xersm, krpjc__kabn)
                gjyd__xersm += len(arr)
                krpjc__kabn += bodo.libs.str_arr_ext.num_total_chars(arr)
            return zlgyy__fbtlu
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(ddc__iej.dtype, types.Integer) for
        ddc__iej in arr_list.types) and any(isinstance(ddc__iej,
        IntegerArrayType) for ddc__iej in arr_list.types):

        def impl_int_arr_list(arr_list):
            ijg__uhem = convert_to_nullable_tup(arr_list)
            pspjs__ruw = []
            itf__gzrbh = 0
            for A in ijg__uhem:
                pspjs__ruw.append(A._data)
                itf__gzrbh += len(A)
            ocyt__blfp = bodo.libs.array_kernels.concat(pspjs__ruw)
            muvj__whv = itf__gzrbh + 7 >> 3
            ovevw__krft = np.empty(muvj__whv, np.uint8)
            niwxf__mbpx = 0
            for A in ijg__uhem:
                cuwe__ciis = A._null_bitmap
                for jmq__ach in range(len(A)):
                    letng__bpjpw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        cuwe__ciis, jmq__ach)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ovevw__krft,
                        niwxf__mbpx, letng__bpjpw)
                    niwxf__mbpx += 1
            return bodo.libs.int_arr_ext.init_integer_array(ocyt__blfp,
                ovevw__krft)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(ddc__iej.dtype == types.bool_ for ddc__iej in
        arr_list.types) and any(ddc__iej == boolean_array for ddc__iej in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            ijg__uhem = convert_to_nullable_tup(arr_list)
            pspjs__ruw = []
            itf__gzrbh = 0
            for A in ijg__uhem:
                pspjs__ruw.append(A._data)
                itf__gzrbh += len(A)
            ocyt__blfp = bodo.libs.array_kernels.concat(pspjs__ruw)
            muvj__whv = itf__gzrbh + 7 >> 3
            ovevw__krft = np.empty(muvj__whv, np.uint8)
            niwxf__mbpx = 0
            for A in ijg__uhem:
                cuwe__ciis = A._null_bitmap
                for jmq__ach in range(len(A)):
                    letng__bpjpw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        cuwe__ciis, jmq__ach)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ovevw__krft,
                        niwxf__mbpx, letng__bpjpw)
                    niwxf__mbpx += 1
            return bodo.libs.bool_arr_ext.init_bool_array(ocyt__blfp,
                ovevw__krft)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            oal__vxm = []
            for A in arr_list:
                oal__vxm.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                oal__vxm), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        dvax__qsx = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        axbx__kbz = 'def impl(arr_list):\n'
        axbx__kbz += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({dvax__qsx},)), arr_list[0].dtype)
"""
        pymoh__vymzq = {}
        exec(axbx__kbz, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, pymoh__vymzq)
        return pymoh__vymzq['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            itf__gzrbh = 0
            for A in arr_list:
                itf__gzrbh += len(A)
            zlgyy__fbtlu = np.empty(itf__gzrbh, dtype)
            yebl__nvq = 0
            for A in arr_list:
                n = len(A)
                zlgyy__fbtlu[yebl__nvq:yebl__nvq + n] = A
                yebl__nvq += n
            return zlgyy__fbtlu
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(ddc__iej, (
        types.Array, IntegerArrayType)) and isinstance(ddc__iej.dtype,
        types.Integer) for ddc__iej in arr_list.types) and any(isinstance(
        ddc__iej, types.Array) and isinstance(ddc__iej.dtype, types.Float) for
        ddc__iej in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            bqgi__vpiyv = []
            for A in arr_list:
                bqgi__vpiyv.append(A._data)
            vtd__yid = bodo.libs.array_kernels.concat(bqgi__vpiyv)
            wqv__bhs = bodo.libs.map_arr_ext.init_map_arr(vtd__yid)
            return wqv__bhs
        return impl_map_arr_list
    for cmfak__ssyf in arr_list:
        if not isinstance(cmfak__ssyf, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(ddc__iej.astype(np.float64) for ddc__iej in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    vmuta__acyj = len(arr_tup.types)
    axbx__kbz = 'def f(arr_tup):\n'
    axbx__kbz += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        vmuta__acyj)), ',' if vmuta__acyj == 1 else '')
    qaupu__oeqx = {}
    exec(axbx__kbz, {'np': np}, qaupu__oeqx)
    uwnkg__dancy = qaupu__oeqx['f']
    return uwnkg__dancy


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    vmuta__acyj = len(arr_tup.types)
    wpq__tkdd = find_common_np_dtype(arr_tup.types)
    uwvvg__xmiko = None
    qxwx__firt = ''
    if isinstance(wpq__tkdd, types.Integer):
        uwvvg__xmiko = bodo.libs.int_arr_ext.IntDtype(wpq__tkdd)
        qxwx__firt = '.astype(out_dtype, False)'
    axbx__kbz = 'def f(arr_tup):\n'
    axbx__kbz += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, qxwx__firt) for i in range(vmuta__acyj)), ',' if 
        vmuta__acyj == 1 else '')
    qaupu__oeqx = {}
    exec(axbx__kbz, {'bodo': bodo, 'out_dtype': uwvvg__xmiko}, qaupu__oeqx)
    nhf__tnmqz = qaupu__oeqx['f']
    return nhf__tnmqz


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, zgyek__zdc = build_set_seen_na(A)
        return len(s) + int(not dropna and zgyek__zdc)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        shvpa__qsvd = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        gryd__jeso = len(shvpa__qsvd)
        return bodo.libs.distributed_api.dist_reduce(gryd__jeso, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([enp__xcrxc for enp__xcrxc in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        bhhb__whrv = np.finfo(A.dtype(1).dtype).max
    else:
        bhhb__whrv = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        zlgyy__fbtlu = np.empty(n, A.dtype)
        msdw__ehf = bhhb__whrv
        for i in range(n):
            msdw__ehf = min(msdw__ehf, A[i])
            zlgyy__fbtlu[i] = msdw__ehf
        return zlgyy__fbtlu
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        bhhb__whrv = np.finfo(A.dtype(1).dtype).min
    else:
        bhhb__whrv = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        zlgyy__fbtlu = np.empty(n, A.dtype)
        msdw__ehf = bhhb__whrv
        for i in range(n):
            msdw__ehf = max(msdw__ehf, A[i])
            zlgyy__fbtlu[i] = msdw__ehf
        return zlgyy__fbtlu
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        gruy__zhmw = arr_info_list_to_table([array_to_info(A)])
        nsmt__guvh = 1
        vavke__qkjd = 0
        wtnx__gdy = drop_duplicates_table(gruy__zhmw, parallel, nsmt__guvh,
            vavke__qkjd, dropna, True)
        zlgyy__fbtlu = info_to_array(info_from_table(wtnx__gdy, 0), A)
        delete_table(gruy__zhmw)
        delete_table(wtnx__gdy)
        return zlgyy__fbtlu
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    wblez__vtkn = bodo.utils.typing.to_nullable_type(arr.dtype)
    xak__vhd = index_arr
    kcnka__skuxp = xak__vhd.dtype

    def impl(arr, index_arr):
        n = len(arr)
        tppv__wpzsi = init_nested_counts(wblez__vtkn)
        aga__ouc = init_nested_counts(kcnka__skuxp)
        for i in range(n):
            secjx__tav = index_arr[i]
            if isna(arr, i):
                tppv__wpzsi = (tppv__wpzsi[0] + 1,) + tppv__wpzsi[1:]
                aga__ouc = add_nested_counts(aga__ouc, secjx__tav)
                continue
            vvuqp__swth = arr[i]
            if len(vvuqp__swth) == 0:
                tppv__wpzsi = (tppv__wpzsi[0] + 1,) + tppv__wpzsi[1:]
                aga__ouc = add_nested_counts(aga__ouc, secjx__tav)
                continue
            tppv__wpzsi = add_nested_counts(tppv__wpzsi, vvuqp__swth)
            for eadcm__ffxx in range(len(vvuqp__swth)):
                aga__ouc = add_nested_counts(aga__ouc, secjx__tav)
        zlgyy__fbtlu = bodo.utils.utils.alloc_type(tppv__wpzsi[0],
            wblez__vtkn, tppv__wpzsi[1:])
        ylm__zqwph = bodo.utils.utils.alloc_type(tppv__wpzsi[0], xak__vhd,
            aga__ouc)
        poba__rmfb = 0
        for i in range(n):
            if isna(arr, i):
                setna(zlgyy__fbtlu, poba__rmfb)
                ylm__zqwph[poba__rmfb] = index_arr[i]
                poba__rmfb += 1
                continue
            vvuqp__swth = arr[i]
            ded__ewcqx = len(vvuqp__swth)
            if ded__ewcqx == 0:
                setna(zlgyy__fbtlu, poba__rmfb)
                ylm__zqwph[poba__rmfb] = index_arr[i]
                poba__rmfb += 1
                continue
            zlgyy__fbtlu[poba__rmfb:poba__rmfb + ded__ewcqx] = vvuqp__swth
            ylm__zqwph[poba__rmfb:poba__rmfb + ded__ewcqx] = index_arr[i]
            poba__rmfb += ded__ewcqx
        return zlgyy__fbtlu, ylm__zqwph
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    wblez__vtkn = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        tppv__wpzsi = init_nested_counts(wblez__vtkn)
        for i in range(n):
            if isna(arr, i):
                tppv__wpzsi = (tppv__wpzsi[0] + 1,) + tppv__wpzsi[1:]
                yti__lykpy = 1
            else:
                vvuqp__swth = arr[i]
                dzc__uow = len(vvuqp__swth)
                if dzc__uow == 0:
                    tppv__wpzsi = (tppv__wpzsi[0] + 1,) + tppv__wpzsi[1:]
                    yti__lykpy = 1
                    continue
                else:
                    tppv__wpzsi = add_nested_counts(tppv__wpzsi, vvuqp__swth)
                    yti__lykpy = dzc__uow
            if counts[i] != yti__lykpy:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        zlgyy__fbtlu = bodo.utils.utils.alloc_type(tppv__wpzsi[0],
            wblez__vtkn, tppv__wpzsi[1:])
        poba__rmfb = 0
        for i in range(n):
            if isna(arr, i):
                setna(zlgyy__fbtlu, poba__rmfb)
                poba__rmfb += 1
                continue
            vvuqp__swth = arr[i]
            ded__ewcqx = len(vvuqp__swth)
            if ded__ewcqx == 0:
                setna(zlgyy__fbtlu, poba__rmfb)
                poba__rmfb += 1
                continue
            zlgyy__fbtlu[poba__rmfb:poba__rmfb + ded__ewcqx] = vvuqp__swth
            poba__rmfb += ded__ewcqx
        return zlgyy__fbtlu
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(gbkut__wil) for gbkut__wil in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        wkn__neqdj = 'np.empty(n, np.int64)'
        edwwm__oxfcz = 'out_arr[i] = 1'
        wra__hnwu = 'max(len(arr[i]), 1)'
    else:
        wkn__neqdj = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        edwwm__oxfcz = 'bodo.libs.array_kernels.setna(out_arr, i)'
        wra__hnwu = 'len(arr[i])'
    axbx__kbz = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {wkn__neqdj}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {edwwm__oxfcz}
        else:
            out_arr[i] = {wra__hnwu}
    return out_arr
    """
    qaupu__oeqx = {}
    exec(axbx__kbz, {'bodo': bodo, 'numba': numba, 'np': np}, qaupu__oeqx)
    impl = qaupu__oeqx['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    xak__vhd = index_arr
    kcnka__skuxp = xak__vhd.dtype

    def impl(arr, pat, n, index_arr):
        qxuf__awlew = pat is not None and len(pat) > 1
        if qxuf__awlew:
            jpexe__bbe = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        iqkkh__wxhuw = len(arr)
        luyl__kulah = 0
        mdajd__xer = 0
        aga__ouc = init_nested_counts(kcnka__skuxp)
        for i in range(iqkkh__wxhuw):
            secjx__tav = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                luyl__kulah += 1
                aga__ouc = add_nested_counts(aga__ouc, secjx__tav)
                continue
            if qxuf__awlew:
                ygwus__kgta = jpexe__bbe.split(arr[i], maxsplit=n)
            else:
                ygwus__kgta = arr[i].split(pat, n)
            luyl__kulah += len(ygwus__kgta)
            for s in ygwus__kgta:
                aga__ouc = add_nested_counts(aga__ouc, secjx__tav)
                mdajd__xer += bodo.libs.str_arr_ext.get_utf8_size(s)
        zlgyy__fbtlu = bodo.libs.str_arr_ext.pre_alloc_string_array(luyl__kulah
            , mdajd__xer)
        ylm__zqwph = bodo.utils.utils.alloc_type(luyl__kulah, xak__vhd,
            aga__ouc)
        srwtt__dfdpc = 0
        for jmq__ach in range(iqkkh__wxhuw):
            if isna(arr, jmq__ach):
                zlgyy__fbtlu[srwtt__dfdpc] = ''
                bodo.libs.array_kernels.setna(zlgyy__fbtlu, srwtt__dfdpc)
                ylm__zqwph[srwtt__dfdpc] = index_arr[jmq__ach]
                srwtt__dfdpc += 1
                continue
            if qxuf__awlew:
                ygwus__kgta = jpexe__bbe.split(arr[jmq__ach], maxsplit=n)
            else:
                ygwus__kgta = arr[jmq__ach].split(pat, n)
            xovcd__dof = len(ygwus__kgta)
            zlgyy__fbtlu[srwtt__dfdpc:srwtt__dfdpc + xovcd__dof] = ygwus__kgta
            ylm__zqwph[srwtt__dfdpc:srwtt__dfdpc + xovcd__dof] = index_arr[
                jmq__ach]
            srwtt__dfdpc += xovcd__dof
        return zlgyy__fbtlu, ylm__zqwph
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
            zlgyy__fbtlu = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                zlgyy__fbtlu[i] = np.nan
            return zlgyy__fbtlu
        return impl_float
    swqu__velw = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        zlgyy__fbtlu = bodo.utils.utils.alloc_type(n, swqu__velw, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(zlgyy__fbtlu, i)
        return zlgyy__fbtlu
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
    exuqc__wnl = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            zlgyy__fbtlu = bodo.utils.utils.alloc_type(new_len, exuqc__wnl)
            bodo.libs.str_arr_ext.str_copy_ptr(zlgyy__fbtlu.ctypes, 0, A.
                ctypes, old_size)
            return zlgyy__fbtlu
        return impl_char

    def impl(A, old_size, new_len):
        zlgyy__fbtlu = bodo.utils.utils.alloc_type(new_len, exuqc__wnl, (-1,))
        zlgyy__fbtlu[:old_size] = A[:old_size]
        return zlgyy__fbtlu
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    xqpxn__tiymc = math.ceil((stop - start) / step)
    return int(max(xqpxn__tiymc, 0))


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
    if any(isinstance(enp__xcrxc, types.Complex) for enp__xcrxc in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            wqcyl__zrya = (stop - start) / step
            xqpxn__tiymc = math.ceil(wqcyl__zrya.real)
            yuee__xez = math.ceil(wqcyl__zrya.imag)
            tzoym__ela = int(max(min(yuee__xez, xqpxn__tiymc), 0))
            arr = np.empty(tzoym__ela, dtype)
            for i in numba.parfors.parfor.internal_prange(tzoym__ela):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            tzoym__ela = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(tzoym__ela, dtype)
            for i in numba.parfors.parfor.internal_prange(tzoym__ela):
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
        akhuc__ksf = arr,
        if not inplace:
            akhuc__ksf = arr.copy(),
        hmtno__ilqbn = bodo.libs.str_arr_ext.to_list_if_immutable_arr(
            akhuc__ksf)
        bplew__fwdxx = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data,
            True)
        bodo.libs.timsort.sort(hmtno__ilqbn, 0, n, bplew__fwdxx)
        if not ascending:
            bodo.libs.timsort.reverseRange(hmtno__ilqbn, 0, n, bplew__fwdxx)
        bodo.libs.str_arr_ext.cp_str_list_to_array(akhuc__ksf, hmtno__ilqbn)
        return akhuc__ksf[0]
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
        wqv__bhs = []
        for i in range(n):
            if A[i]:
                wqv__bhs.append(i + offset)
        return np.array(wqv__bhs, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    exuqc__wnl = element_type(A)
    if exuqc__wnl == types.unicode_type:
        null_value = '""'
    elif exuqc__wnl == types.bool_:
        null_value = 'False'
    elif exuqc__wnl == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif exuqc__wnl == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    srwtt__dfdpc = 'i'
    cbf__ejd = False
    rmlp__snkco = get_overload_const_str(method)
    if rmlp__snkco in ('ffill', 'pad'):
        spwj__fqrpd = 'n'
        send_right = True
    elif rmlp__snkco in ('backfill', 'bfill'):
        spwj__fqrpd = 'n-1, -1, -1'
        send_right = False
        if exuqc__wnl == types.unicode_type:
            srwtt__dfdpc = '(n - 1) - i'
            cbf__ejd = True
    axbx__kbz = 'def impl(A, method, parallel=False):\n'
    axbx__kbz += '  A = decode_if_dict_array(A)\n'
    axbx__kbz += '  has_last_value = False\n'
    axbx__kbz += f'  last_value = {null_value}\n'
    axbx__kbz += '  if parallel:\n'
    axbx__kbz += '    rank = bodo.libs.distributed_api.get_rank()\n'
    axbx__kbz += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    axbx__kbz += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    axbx__kbz += '  n = len(A)\n'
    axbx__kbz += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    axbx__kbz += f'  for i in range({spwj__fqrpd}):\n'
    axbx__kbz += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    axbx__kbz += (
        f'      bodo.libs.array_kernels.setna(out_arr, {srwtt__dfdpc})\n')
    axbx__kbz += '      continue\n'
    axbx__kbz += '    s = A[i]\n'
    axbx__kbz += '    if bodo.libs.array_kernels.isna(A, i):\n'
    axbx__kbz += '      s = last_value\n'
    axbx__kbz += f'    out_arr[{srwtt__dfdpc}] = s\n'
    axbx__kbz += '    last_value = s\n'
    axbx__kbz += '    has_last_value = True\n'
    if cbf__ejd:
        axbx__kbz += '  return out_arr[::-1]\n'
    else:
        axbx__kbz += '  return out_arr\n'
    puoq__fhe = {}
    exec(axbx__kbz, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, puoq__fhe)
    impl = puoq__fhe['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        ppqzr__fhynu = 0
        mhm__zajs = n_pes - 1
        cxjl__ccvaz = np.int32(rank + 1)
        ihh__xqzq = np.int32(rank - 1)
        xcwhh__nngy = len(in_arr) - 1
        drv__huo = -1
        fduhv__dyj = -1
    else:
        ppqzr__fhynu = n_pes - 1
        mhm__zajs = 0
        cxjl__ccvaz = np.int32(rank - 1)
        ihh__xqzq = np.int32(rank + 1)
        xcwhh__nngy = 0
        drv__huo = len(in_arr)
        fduhv__dyj = 1
    qnzdi__bjpne = np.int32(bodo.hiframes.rolling.comm_border_tag)
    hblgq__lkg = np.empty(1, dtype=np.bool_)
    szp__opcr = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    nhq__oziyi = np.empty(1, dtype=np.bool_)
    bnm__hyh = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    ixeuo__nveu = False
    qxq__swmdv = null_value
    for i in range(xcwhh__nngy, drv__huo, fduhv__dyj):
        if not isna(in_arr, i):
            ixeuo__nveu = True
            qxq__swmdv = in_arr[i]
            break
    if rank != ppqzr__fhynu:
        hcz__hzo = bodo.libs.distributed_api.irecv(hblgq__lkg, 1, ihh__xqzq,
            qnzdi__bjpne, True)
        bodo.libs.distributed_api.wait(hcz__hzo, True)
        ghq__ulmog = bodo.libs.distributed_api.irecv(szp__opcr, 1,
            ihh__xqzq, qnzdi__bjpne, True)
        bodo.libs.distributed_api.wait(ghq__ulmog, True)
        pfoy__intrj = hblgq__lkg[0]
        uvyn__ujmax = szp__opcr[0]
    else:
        pfoy__intrj = False
        uvyn__ujmax = null_value
    if ixeuo__nveu:
        nhq__oziyi[0] = ixeuo__nveu
        bnm__hyh[0] = qxq__swmdv
    else:
        nhq__oziyi[0] = pfoy__intrj
        bnm__hyh[0] = uvyn__ujmax
    if rank != mhm__zajs:
        czb__epk = bodo.libs.distributed_api.isend(nhq__oziyi, 1,
            cxjl__ccvaz, qnzdi__bjpne, True)
        cna__dcghu = bodo.libs.distributed_api.isend(bnm__hyh, 1,
            cxjl__ccvaz, qnzdi__bjpne, True)
    return pfoy__intrj, uvyn__ujmax


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    xfr__feln = {'axis': axis, 'kind': kind, 'order': order}
    fqvfc__ely = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', xfr__feln, fqvfc__ely, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    exuqc__wnl = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            iqkkh__wxhuw = len(A)
            zlgyy__fbtlu = bodo.utils.utils.alloc_type(iqkkh__wxhuw *
                repeats, exuqc__wnl, (-1,))
            for i in range(iqkkh__wxhuw):
                srwtt__dfdpc = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for jmq__ach in range(repeats):
                        bodo.libs.array_kernels.setna(zlgyy__fbtlu, 
                            srwtt__dfdpc + jmq__ach)
                else:
                    zlgyy__fbtlu[srwtt__dfdpc:srwtt__dfdpc + repeats] = A[i]
            return zlgyy__fbtlu
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        iqkkh__wxhuw = len(A)
        zlgyy__fbtlu = bodo.utils.utils.alloc_type(repeats.sum(),
            exuqc__wnl, (-1,))
        srwtt__dfdpc = 0
        for i in range(iqkkh__wxhuw):
            jrpx__onme = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for jmq__ach in range(jrpx__onme):
                    bodo.libs.array_kernels.setna(zlgyy__fbtlu, 
                        srwtt__dfdpc + jmq__ach)
            else:
                zlgyy__fbtlu[srwtt__dfdpc:srwtt__dfdpc + jrpx__onme] = A[i]
            srwtt__dfdpc += jrpx__onme
        return zlgyy__fbtlu
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
        pkmfq__xqq = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(pkmfq__xqq, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        oszct__zow = bodo.libs.array_kernels.concat([A1, A2])
        gdru__xipil = bodo.libs.array_kernels.unique(oszct__zow)
        return pd.Series(gdru__xipil).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    xfr__feln = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    fqvfc__ely = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', xfr__feln, fqvfc__ely, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        dlh__uplg = bodo.libs.array_kernels.unique(A1)
        unyjp__fobkj = bodo.libs.array_kernels.unique(A2)
        oszct__zow = bodo.libs.array_kernels.concat([dlh__uplg, unyjp__fobkj])
        xpxij__ccjmg = pd.Series(oszct__zow).sort_values().values
        return slice_array_intersect1d(xpxij__ccjmg)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    yomt__imt = arr[1:] == arr[:-1]
    return arr[:-1][yomt__imt]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    xfr__feln = {'assume_unique': assume_unique}
    fqvfc__ely = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', xfr__feln, fqvfc__ely, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        dlh__uplg = bodo.libs.array_kernels.unique(A1)
        unyjp__fobkj = bodo.libs.array_kernels.unique(A2)
        yomt__imt = calculate_mask_setdiff1d(dlh__uplg, unyjp__fobkj)
        return pd.Series(dlh__uplg[yomt__imt]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    yomt__imt = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        yomt__imt &= A1 != A2[i]
    return yomt__imt


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    xfr__feln = {'retstep': retstep, 'axis': axis}
    fqvfc__ely = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', xfr__feln, fqvfc__ely, 'numpy')
    xncvf__dkqn = False
    if is_overload_none(dtype):
        exuqc__wnl = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            xncvf__dkqn = True
        exuqc__wnl = numba.np.numpy_support.as_dtype(dtype).type
    if xncvf__dkqn:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            spr__dhzwm = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            zlgyy__fbtlu = np.empty(num, exuqc__wnl)
            for i in numba.parfors.parfor.internal_prange(num):
                zlgyy__fbtlu[i] = exuqc__wnl(np.floor(start + i * spr__dhzwm))
            return zlgyy__fbtlu
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            spr__dhzwm = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            zlgyy__fbtlu = np.empty(num, exuqc__wnl)
            for i in numba.parfors.parfor.internal_prange(num):
                zlgyy__fbtlu[i] = exuqc__wnl(start + i * spr__dhzwm)
            return zlgyy__fbtlu
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
        vmuta__acyj = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                vmuta__acyj += A[i] == val
        return vmuta__acyj > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    xfr__feln = {'axis': axis, 'out': out, 'keepdims': keepdims}
    fqvfc__ely = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', xfr__feln, fqvfc__ely, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        vmuta__acyj = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                vmuta__acyj += int(bool(A[i]))
        return vmuta__acyj > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    xfr__feln = {'axis': axis, 'out': out, 'keepdims': keepdims}
    fqvfc__ely = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', xfr__feln, fqvfc__ely, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        vmuta__acyj = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                vmuta__acyj += int(bool(A[i]))
        return vmuta__acyj == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    xfr__feln = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    fqvfc__ely = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', xfr__feln, fqvfc__ely, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        bjzf__rsqo = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            zlgyy__fbtlu = np.empty(n, bjzf__rsqo)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(zlgyy__fbtlu, i)
                    continue
                zlgyy__fbtlu[i] = np_cbrt_scalar(A[i], bjzf__rsqo)
            return zlgyy__fbtlu
        return impl_arr
    bjzf__rsqo = np.promote_types(numba.np.numpy_support.as_dtype(A), numba
        .np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, bjzf__rsqo)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    szdfr__ivvhn = x < 0
    if szdfr__ivvhn:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if szdfr__ivvhn:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    etuf__tnu = isinstance(tup, (types.BaseTuple, types.List))
    hahyy__kwupj = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for cmfak__ssyf in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                cmfak__ssyf, 'numpy.hstack()')
            etuf__tnu = etuf__tnu and bodo.utils.utils.is_array_typ(cmfak__ssyf
                , False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        etuf__tnu = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif hahyy__kwupj:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        lbym__trj = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for cmfak__ssyf in lbym__trj.types:
            hahyy__kwupj = hahyy__kwupj and bodo.utils.utils.is_array_typ(
                cmfak__ssyf, False)
    if not (etuf__tnu or hahyy__kwupj):
        return
    if hahyy__kwupj:

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
    xfr__feln = {'check_valid': check_valid, 'tol': tol}
    fqvfc__ely = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', xfr__feln,
        fqvfc__ely, 'numpy')
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
        fqna__ibhsd = mean.shape[0]
        fhc__ejfw = size, fqna__ibhsd
        zees__cxstm = np.random.standard_normal(fhc__ejfw)
        cov = cov.astype(np.float64)
        ioqkm__miv, s, bqemk__olt = np.linalg.svd(cov)
        res = np.dot(zees__cxstm, np.sqrt(s).reshape(fqna__ibhsd, 1) *
            bqemk__olt)
        ape__ztan = res + mean
        return ape__ztan
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
            cgcdg__bmusf = bodo.hiframes.series_kernels._get_type_max_value(arr
                )
            ijjbn__zhjnm = typing.builtins.IndexValue(-1, cgcdg__bmusf)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                jkjes__atnud = typing.builtins.IndexValue(i, arr[i])
                ijjbn__zhjnm = min(ijjbn__zhjnm, jkjes__atnud)
            return ijjbn__zhjnm.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        aszpr__jbqix = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            vqmi__qkpj = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            cgcdg__bmusf = aszpr__jbqix(len(arr.dtype.categories) + 1)
            ijjbn__zhjnm = typing.builtins.IndexValue(-1, cgcdg__bmusf)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                jkjes__atnud = typing.builtins.IndexValue(i, vqmi__qkpj[i])
                ijjbn__zhjnm = min(ijjbn__zhjnm, jkjes__atnud)
            return ijjbn__zhjnm.index
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
            cgcdg__bmusf = bodo.hiframes.series_kernels._get_type_min_value(arr
                )
            ijjbn__zhjnm = typing.builtins.IndexValue(-1, cgcdg__bmusf)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                jkjes__atnud = typing.builtins.IndexValue(i, arr[i])
                ijjbn__zhjnm = max(ijjbn__zhjnm, jkjes__atnud)
            return ijjbn__zhjnm.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        aszpr__jbqix = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            n = len(arr)
            vqmi__qkpj = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            cgcdg__bmusf = aszpr__jbqix(-1)
            ijjbn__zhjnm = typing.builtins.IndexValue(-1, cgcdg__bmusf)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                jkjes__atnud = typing.builtins.IndexValue(i, vqmi__qkpj[i])
                ijjbn__zhjnm = max(ijjbn__zhjnm, jkjes__atnud)
            return ijjbn__zhjnm.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
