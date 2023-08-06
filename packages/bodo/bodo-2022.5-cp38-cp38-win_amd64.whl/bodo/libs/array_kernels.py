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
        fsi__egr = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = fsi__egr
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        fsi__egr = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = fsi__egr
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
            lzzfe__uod = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            lzzfe__uod[ind + 1] = lzzfe__uod[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            lzzfe__uod = bodo.libs.array_item_arr_ext.get_offsets(arr)
            lzzfe__uod[ind + 1] = lzzfe__uod[ind]
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
    whgk__iwd = arr_tup.count
    ogd__lgdv = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(whgk__iwd):
        ogd__lgdv += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    ogd__lgdv += '  return\n'
    cwgh__hesac = {}
    exec(ogd__lgdv, {'setna': setna}, cwgh__hesac)
    impl = cwgh__hesac['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        lxtjf__wkcam = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(lxtjf__wkcam.start, lxtjf__wkcam.stop, lxtjf__wkcam.step
            ):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        ftcf__xts = 'n'
        qbijz__ltftl = 'n_pes'
        bqd__stlc = 'min_op'
    else:
        ftcf__xts = 'n-1, -1, -1'
        qbijz__ltftl = '-1'
        bqd__stlc = 'max_op'
    ogd__lgdv = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {qbijz__ltftl}
    for i in range({ftcf__xts}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {bqd__stlc}))
        if possible_valid_rank != {qbijz__ltftl}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    cwgh__hesac = {}
    exec(ogd__lgdv, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        cwgh__hesac)
    impl = cwgh__hesac['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    cjht__odezj = array_to_info(arr)
    _median_series_computation(res, cjht__odezj, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(cjht__odezj)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    cjht__odezj = array_to_info(arr)
    _autocorr_series_computation(res, cjht__odezj, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(cjht__odezj)


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
    cjht__odezj = array_to_info(arr)
    _compute_series_monotonicity(res, cjht__odezj, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(cjht__odezj)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    oxrg__acq = res[0] > 0.5
    return oxrg__acq


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        fgw__duu = '-'
        jcvf__btrf = 'index_arr[0] > threshhold_date'
        ftcf__xts = '1, n+1'
        ulq__agw = 'index_arr[-i] <= threshhold_date'
        cigi__ntqk = 'i - 1'
    else:
        fgw__duu = '+'
        jcvf__btrf = 'index_arr[-1] < threshhold_date'
        ftcf__xts = 'n'
        ulq__agw = 'index_arr[i] >= threshhold_date'
        cigi__ntqk = 'i'
    ogd__lgdv = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        ogd__lgdv += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        ogd__lgdv += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            ogd__lgdv += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            ogd__lgdv += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            ogd__lgdv += '    else:\n'
            ogd__lgdv += '      threshhold_date = initial_date + date_offset\n'
        else:
            ogd__lgdv += (
                f'    threshhold_date = initial_date {fgw__duu} date_offset\n')
    else:
        ogd__lgdv += f'  threshhold_date = initial_date {fgw__duu} offset\n'
    ogd__lgdv += '  local_valid = 0\n'
    ogd__lgdv += f'  n = len(index_arr)\n'
    ogd__lgdv += f'  if n:\n'
    ogd__lgdv += f'    if {jcvf__btrf}:\n'
    ogd__lgdv += '      loc_valid = n\n'
    ogd__lgdv += '    else:\n'
    ogd__lgdv += f'      for i in range({ftcf__xts}):\n'
    ogd__lgdv += f'        if {ulq__agw}:\n'
    ogd__lgdv += f'          loc_valid = {cigi__ntqk}\n'
    ogd__lgdv += '          break\n'
    ogd__lgdv += '  if is_parallel:\n'
    ogd__lgdv += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    ogd__lgdv += '    return total_valid\n'
    ogd__lgdv += '  else:\n'
    ogd__lgdv += '    return loc_valid\n'
    cwgh__hesac = {}
    exec(ogd__lgdv, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, cwgh__hesac)
    return cwgh__hesac['impl']


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
    evu__milp = numba_to_c_type(sig.args[0].dtype)
    sccwc__pww = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), evu__milp))
    hcxt__sdmup = args[0]
    cymbx__dvms = sig.args[0]
    if isinstance(cymbx__dvms, (IntegerArrayType, BooleanArrayType)):
        hcxt__sdmup = cgutils.create_struct_proxy(cymbx__dvms)(context,
            builder, hcxt__sdmup).data
        cymbx__dvms = types.Array(cymbx__dvms.dtype, 1, 'C')
    assert cymbx__dvms.ndim == 1
    arr = make_array(cymbx__dvms)(context, builder, hcxt__sdmup)
    dsvr__demx = builder.extract_value(arr.shape, 0)
    jitjx__xnzyx = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        dsvr__demx, args[1], builder.load(sccwc__pww)]
    sbsb__ckuc = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    ihoye__exsn = lir.FunctionType(lir.DoubleType(), sbsb__ckuc)
    hzosj__dqdn = cgutils.get_or_insert_function(builder.module,
        ihoye__exsn, name='quantile_sequential')
    ccqpb__uwmf = builder.call(hzosj__dqdn, jitjx__xnzyx)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return ccqpb__uwmf


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    evu__milp = numba_to_c_type(sig.args[0].dtype)
    sccwc__pww = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), evu__milp))
    hcxt__sdmup = args[0]
    cymbx__dvms = sig.args[0]
    if isinstance(cymbx__dvms, (IntegerArrayType, BooleanArrayType)):
        hcxt__sdmup = cgutils.create_struct_proxy(cymbx__dvms)(context,
            builder, hcxt__sdmup).data
        cymbx__dvms = types.Array(cymbx__dvms.dtype, 1, 'C')
    assert cymbx__dvms.ndim == 1
    arr = make_array(cymbx__dvms)(context, builder, hcxt__sdmup)
    dsvr__demx = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        xpvb__oftl = args[2]
    else:
        xpvb__oftl = dsvr__demx
    jitjx__xnzyx = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        dsvr__demx, xpvb__oftl, args[1], builder.load(sccwc__pww)]
    sbsb__ckuc = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType
        (64), lir.DoubleType(), lir.IntType(32)]
    ihoye__exsn = lir.FunctionType(lir.DoubleType(), sbsb__ckuc)
    hzosj__dqdn = cgutils.get_or_insert_function(builder.module,
        ihoye__exsn, name='quantile_parallel')
    ccqpb__uwmf = builder.call(hzosj__dqdn, jitjx__xnzyx)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return ccqpb__uwmf


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    ocrg__bvo = start
    jwugl__dqy = 2 * start + 1
    dkhd__ukk = 2 * start + 2
    if jwugl__dqy < n and not cmp_f(arr[jwugl__dqy], arr[ocrg__bvo]):
        ocrg__bvo = jwugl__dqy
    if dkhd__ukk < n and not cmp_f(arr[dkhd__ukk], arr[ocrg__bvo]):
        ocrg__bvo = dkhd__ukk
    if ocrg__bvo != start:
        arr[start], arr[ocrg__bvo] = arr[ocrg__bvo], arr[start]
        ind_arr[start], ind_arr[ocrg__bvo] = ind_arr[ocrg__bvo], ind_arr[start]
        min_heapify(arr, ind_arr, n, ocrg__bvo, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        ugayv__nyd = np.empty(k, A.dtype)
        cjcgo__utrom = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                ugayv__nyd[ind] = A[i]
                cjcgo__utrom[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            ugayv__nyd = ugayv__nyd[:ind]
            cjcgo__utrom = cjcgo__utrom[:ind]
        return ugayv__nyd, cjcgo__utrom, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        ttyq__mda = np.sort(A)
        uizg__suas = index_arr[np.argsort(A)]
        ivaf__plhm = pd.Series(ttyq__mda).notna().values
        ttyq__mda = ttyq__mda[ivaf__plhm]
        uizg__suas = uizg__suas[ivaf__plhm]
        if is_largest:
            ttyq__mda = ttyq__mda[::-1]
            uizg__suas = uizg__suas[::-1]
        return np.ascontiguousarray(ttyq__mda), np.ascontiguousarray(uizg__suas
            )
    ugayv__nyd, cjcgo__utrom, start = select_k_nonan(A, index_arr, m, k)
    cjcgo__utrom = cjcgo__utrom[ugayv__nyd.argsort()]
    ugayv__nyd.sort()
    if not is_largest:
        ugayv__nyd = np.ascontiguousarray(ugayv__nyd[::-1])
        cjcgo__utrom = np.ascontiguousarray(cjcgo__utrom[::-1])
    for i in range(start, m):
        if cmp_f(A[i], ugayv__nyd[0]):
            ugayv__nyd[0] = A[i]
            cjcgo__utrom[0] = index_arr[i]
            min_heapify(ugayv__nyd, cjcgo__utrom, k, 0, cmp_f)
    cjcgo__utrom = cjcgo__utrom[ugayv__nyd.argsort()]
    ugayv__nyd.sort()
    if is_largest:
        ugayv__nyd = ugayv__nyd[::-1]
        cjcgo__utrom = cjcgo__utrom[::-1]
    return np.ascontiguousarray(ugayv__nyd), np.ascontiguousarray(cjcgo__utrom)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    ynqv__krsyx = bodo.libs.distributed_api.get_rank()
    gwofi__efe, xkaxy__oxm = nlargest(A, I, k, is_largest, cmp_f)
    vwuqi__smyy = bodo.libs.distributed_api.gatherv(gwofi__efe)
    lcxb__qtro = bodo.libs.distributed_api.gatherv(xkaxy__oxm)
    if ynqv__krsyx == MPI_ROOT:
        res, gcc__qaa = nlargest(vwuqi__smyy, lcxb__qtro, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        gcc__qaa = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(gcc__qaa)
    return res, gcc__qaa


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    ujw__poijs, rhc__yqpy = mat.shape
    rnotk__bezf = np.empty((rhc__yqpy, rhc__yqpy), dtype=np.float64)
    for qrwl__fswf in range(rhc__yqpy):
        for qgr__zhxt in range(qrwl__fswf + 1):
            cvex__ydi = 0
            pul__czmt = eehn__fiwgx = uatx__eau = zovp__ifo = 0.0
            for i in range(ujw__poijs):
                if np.isfinite(mat[i, qrwl__fswf]) and np.isfinite(mat[i,
                    qgr__zhxt]):
                    nsj__swqrx = mat[i, qrwl__fswf]
                    uve__ugy = mat[i, qgr__zhxt]
                    cvex__ydi += 1
                    uatx__eau += nsj__swqrx
                    zovp__ifo += uve__ugy
            if parallel:
                cvex__ydi = bodo.libs.distributed_api.dist_reduce(cvex__ydi,
                    sum_op)
                uatx__eau = bodo.libs.distributed_api.dist_reduce(uatx__eau,
                    sum_op)
                zovp__ifo = bodo.libs.distributed_api.dist_reduce(zovp__ifo,
                    sum_op)
            if cvex__ydi < minpv:
                rnotk__bezf[qrwl__fswf, qgr__zhxt] = rnotk__bezf[qgr__zhxt,
                    qrwl__fswf] = np.nan
            else:
                jpxf__icidi = uatx__eau / cvex__ydi
                rueap__jkco = zovp__ifo / cvex__ydi
                uatx__eau = 0.0
                for i in range(ujw__poijs):
                    if np.isfinite(mat[i, qrwl__fswf]) and np.isfinite(mat[
                        i, qgr__zhxt]):
                        nsj__swqrx = mat[i, qrwl__fswf] - jpxf__icidi
                        uve__ugy = mat[i, qgr__zhxt] - rueap__jkco
                        uatx__eau += nsj__swqrx * uve__ugy
                        pul__czmt += nsj__swqrx * nsj__swqrx
                        eehn__fiwgx += uve__ugy * uve__ugy
                if parallel:
                    uatx__eau = bodo.libs.distributed_api.dist_reduce(uatx__eau
                        , sum_op)
                    pul__czmt = bodo.libs.distributed_api.dist_reduce(pul__czmt
                        , sum_op)
                    eehn__fiwgx = bodo.libs.distributed_api.dist_reduce(
                        eehn__fiwgx, sum_op)
                vcc__ach = cvex__ydi - 1.0 if cov else sqrt(pul__czmt *
                    eehn__fiwgx)
                if vcc__ach != 0.0:
                    rnotk__bezf[qrwl__fswf, qgr__zhxt] = rnotk__bezf[
                        qgr__zhxt, qrwl__fswf] = uatx__eau / vcc__ach
                else:
                    rnotk__bezf[qrwl__fswf, qgr__zhxt] = rnotk__bezf[
                        qgr__zhxt, qrwl__fswf] = np.nan
    return rnotk__bezf


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    bax__ggz = n != 1
    ogd__lgdv = 'def impl(data, parallel=False):\n'
    ogd__lgdv += '  if parallel:\n'
    hradu__zad = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    ogd__lgdv += f'    cpp_table = arr_info_list_to_table([{hradu__zad}])\n'
    ogd__lgdv += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    iah__ncnp = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    ogd__lgdv += f'    data = ({iah__ncnp},)\n'
    ogd__lgdv += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    ogd__lgdv += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    ogd__lgdv += '    bodo.libs.array.delete_table(cpp_table)\n'
    ogd__lgdv += '  n = len(data[0])\n'
    ogd__lgdv += '  out = np.empty(n, np.bool_)\n'
    ogd__lgdv += '  uniqs = dict()\n'
    if bax__ggz:
        ogd__lgdv += '  for i in range(n):\n'
        lidfc__rpztf = ', '.join(f'data[{i}][i]' for i in range(n))
        rva__hyj = ',  '.join(f'bodo.libs.array_kernels.isna(data[{i}], i)' for
            i in range(n))
        ogd__lgdv += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({lidfc__rpztf},), ({rva__hyj},))
"""
        ogd__lgdv += '    if val in uniqs:\n'
        ogd__lgdv += '      out[i] = True\n'
        ogd__lgdv += '    else:\n'
        ogd__lgdv += '      out[i] = False\n'
        ogd__lgdv += '      uniqs[val] = 0\n'
    else:
        ogd__lgdv += '  data = data[0]\n'
        ogd__lgdv += '  hasna = False\n'
        ogd__lgdv += '  for i in range(n):\n'
        ogd__lgdv += '    if bodo.libs.array_kernels.isna(data, i):\n'
        ogd__lgdv += '      out[i] = hasna\n'
        ogd__lgdv += '      hasna = True\n'
        ogd__lgdv += '    else:\n'
        ogd__lgdv += '      val = data[i]\n'
        ogd__lgdv += '      if val in uniqs:\n'
        ogd__lgdv += '        out[i] = True\n'
        ogd__lgdv += '      else:\n'
        ogd__lgdv += '        out[i] = False\n'
        ogd__lgdv += '        uniqs[val] = 0\n'
    ogd__lgdv += '  if parallel:\n'
    ogd__lgdv += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    ogd__lgdv += '  return out\n'
    cwgh__hesac = {}
    exec(ogd__lgdv, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, cwgh__hesac)
    impl = cwgh__hesac['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    whgk__iwd = len(data)
    ogd__lgdv = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    ogd__lgdv += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        whgk__iwd)))
    ogd__lgdv += '  table_total = arr_info_list_to_table(info_list_total)\n'
    ogd__lgdv += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(whgk__iwd))
    for bug__aflo in range(whgk__iwd):
        ogd__lgdv += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(bug__aflo, bug__aflo, bug__aflo))
    ogd__lgdv += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(whgk__iwd))
    ogd__lgdv += '  delete_table(out_table)\n'
    ogd__lgdv += '  delete_table(table_total)\n'
    ogd__lgdv += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(whgk__iwd)))
    cwgh__hesac = {}
    exec(ogd__lgdv, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, cwgh__hesac)
    impl = cwgh__hesac['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    whgk__iwd = len(data)
    ogd__lgdv = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    ogd__lgdv += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        whgk__iwd)))
    ogd__lgdv += '  table_total = arr_info_list_to_table(info_list_total)\n'
    ogd__lgdv += '  keep_i = 0\n'
    ogd__lgdv += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for bug__aflo in range(whgk__iwd):
        ogd__lgdv += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(bug__aflo, bug__aflo, bug__aflo))
    ogd__lgdv += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(whgk__iwd))
    ogd__lgdv += '  delete_table(out_table)\n'
    ogd__lgdv += '  delete_table(table_total)\n'
    ogd__lgdv += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(whgk__iwd)))
    cwgh__hesac = {}
    exec(ogd__lgdv, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, cwgh__hesac)
    impl = cwgh__hesac['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        kjs__ttfvt = [array_to_info(data_arr)]
        mhc__nedlf = arr_info_list_to_table(kjs__ttfvt)
        tzz__zwtt = 0
        wfmw__uncoo = drop_duplicates_table(mhc__nedlf, parallel, 1,
            tzz__zwtt, False, True)
        dkyvl__jkkf = info_to_array(info_from_table(wfmw__uncoo, 0), data_arr)
        delete_table(wfmw__uncoo)
        delete_table(mhc__nedlf)
        return dkyvl__jkkf
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    jib__evb = len(data.types)
    ynnpr__ybr = [('out' + str(i)) for i in range(jib__evb)]
    okh__avphz = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    muob__qpcdr = ['isna(data[{}], i)'.format(i) for i in okh__avphz]
    gby__sqj = 'not ({})'.format(' or '.join(muob__qpcdr))
    if not is_overload_none(thresh):
        gby__sqj = '(({}) <= ({}) - thresh)'.format(' + '.join(muob__qpcdr),
            jib__evb - 1)
    elif how == 'all':
        gby__sqj = 'not ({})'.format(' and '.join(muob__qpcdr))
    ogd__lgdv = 'def _dropna_imp(data, how, thresh, subset):\n'
    ogd__lgdv += '  old_len = len(data[0])\n'
    ogd__lgdv += '  new_len = 0\n'
    ogd__lgdv += '  for i in range(old_len):\n'
    ogd__lgdv += '    if {}:\n'.format(gby__sqj)
    ogd__lgdv += '      new_len += 1\n'
    for i, out in enumerate(ynnpr__ybr):
        if isinstance(data[i], bodo.CategoricalArrayType):
            ogd__lgdv += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            ogd__lgdv += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    ogd__lgdv += '  curr_ind = 0\n'
    ogd__lgdv += '  for i in range(old_len):\n'
    ogd__lgdv += '    if {}:\n'.format(gby__sqj)
    for i in range(jib__evb):
        ogd__lgdv += '      if isna(data[{}], i):\n'.format(i)
        ogd__lgdv += '        setna({}, curr_ind)\n'.format(ynnpr__ybr[i])
        ogd__lgdv += '      else:\n'
        ogd__lgdv += '        {}[curr_ind] = data[{}][i]\n'.format(ynnpr__ybr
            [i], i)
    ogd__lgdv += '      curr_ind += 1\n'
    ogd__lgdv += '  return {}\n'.format(', '.join(ynnpr__ybr))
    cwgh__hesac = {}
    bht__zcr = {'t{}'.format(i): pyrbx__avpx for i, pyrbx__avpx in
        enumerate(data.types)}
    bht__zcr.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(ogd__lgdv, bht__zcr, cwgh__hesac)
    zhtma__zgfny = cwgh__hesac['_dropna_imp']
    return zhtma__zgfny


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        cymbx__dvms = arr.dtype
        sne__gktgr = cymbx__dvms.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            wzfh__kldl = init_nested_counts(sne__gktgr)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                wzfh__kldl = add_nested_counts(wzfh__kldl, val[ind])
            dkyvl__jkkf = bodo.utils.utils.alloc_type(n, cymbx__dvms,
                wzfh__kldl)
            for lmn__upf in range(n):
                if bodo.libs.array_kernels.isna(arr, lmn__upf):
                    setna(dkyvl__jkkf, lmn__upf)
                    continue
                val = arr[lmn__upf]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(dkyvl__jkkf, lmn__upf)
                    continue
                dkyvl__jkkf[lmn__upf] = val[ind]
            return dkyvl__jkkf
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    efp__ybmbf = _to_readonly(arr_types.types[0])
    return all(isinstance(pyrbx__avpx, CategoricalArrayType) and 
        _to_readonly(pyrbx__avpx) == efp__ybmbf for pyrbx__avpx in
        arr_types.types)


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
        cgb__cekah = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            nqpw__erf = 0
            hmi__sbv = []
            for A in arr_list:
                jpf__iejv = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                hmi__sbv.append(bodo.libs.array_item_arr_ext.get_data(A))
                nqpw__erf += jpf__iejv
            amh__bgull = np.empty(nqpw__erf + 1, offset_type)
            mfj__viv = bodo.libs.array_kernels.concat(hmi__sbv)
            mrj__hnplx = np.empty(nqpw__erf + 7 >> 3, np.uint8)
            kck__vvjk = 0
            wprba__vctxp = 0
            for A in arr_list:
                dtjww__emz = bodo.libs.array_item_arr_ext.get_offsets(A)
                cgx__ofw = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                jpf__iejv = len(A)
                qzzs__oueqg = dtjww__emz[jpf__iejv]
                for i in range(jpf__iejv):
                    amh__bgull[i + kck__vvjk] = dtjww__emz[i] + wprba__vctxp
                    ogtxc__zgy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        cgx__ofw, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mrj__hnplx, i +
                        kck__vvjk, ogtxc__zgy)
                kck__vvjk += jpf__iejv
                wprba__vctxp += qzzs__oueqg
            amh__bgull[kck__vvjk] = wprba__vctxp
            dkyvl__jkkf = bodo.libs.array_item_arr_ext.init_array_item_array(
                nqpw__erf, mfj__viv, amh__bgull, mrj__hnplx)
            return dkyvl__jkkf
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        jtug__pdyts = arr_list.dtype.names
        ogd__lgdv = 'def struct_array_concat_impl(arr_list):\n'
        ogd__lgdv += f'    n_all = 0\n'
        for i in range(len(jtug__pdyts)):
            ogd__lgdv += f'    concat_list{i} = []\n'
        ogd__lgdv += '    for A in arr_list:\n'
        ogd__lgdv += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(jtug__pdyts)):
            ogd__lgdv += f'        concat_list{i}.append(data_tuple[{i}])\n'
        ogd__lgdv += '        n_all += len(A)\n'
        ogd__lgdv += '    n_bytes = (n_all + 7) >> 3\n'
        ogd__lgdv += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        ogd__lgdv += '    curr_bit = 0\n'
        ogd__lgdv += '    for A in arr_list:\n'
        ogd__lgdv += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        ogd__lgdv += '        for j in range(len(A)):\n'
        ogd__lgdv += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        ogd__lgdv += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        ogd__lgdv += '            curr_bit += 1\n'
        ogd__lgdv += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        gkawt__ivnzr = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(jtug__pdyts))])
        ogd__lgdv += f'        ({gkawt__ivnzr},),\n'
        ogd__lgdv += '        new_mask,\n'
        ogd__lgdv += f'        {jtug__pdyts},\n'
        ogd__lgdv += '    )\n'
        cwgh__hesac = {}
        exec(ogd__lgdv, {'bodo': bodo, 'np': np}, cwgh__hesac)
        return cwgh__hesac['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            gcd__psdnt = 0
            for A in arr_list:
                gcd__psdnt += len(A)
            jiv__qhzp = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(gcd__psdnt))
            eocf__fzco = 0
            for A in arr_list:
                for i in range(len(A)):
                    jiv__qhzp._data[i + eocf__fzco] = A._data[i]
                    ogtxc__zgy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jiv__qhzp.
                        _null_bitmap, i + eocf__fzco, ogtxc__zgy)
                eocf__fzco += len(A)
            return jiv__qhzp
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            gcd__psdnt = 0
            for A in arr_list:
                gcd__psdnt += len(A)
            jiv__qhzp = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(gcd__psdnt))
            eocf__fzco = 0
            for A in arr_list:
                for i in range(len(A)):
                    jiv__qhzp._days_data[i + eocf__fzco] = A._days_data[i]
                    jiv__qhzp._seconds_data[i + eocf__fzco] = A._seconds_data[i
                        ]
                    jiv__qhzp._microseconds_data[i + eocf__fzco
                        ] = A._microseconds_data[i]
                    ogtxc__zgy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jiv__qhzp.
                        _null_bitmap, i + eocf__fzco, ogtxc__zgy)
                eocf__fzco += len(A)
            return jiv__qhzp
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        iof__vyhl = arr_list.dtype.precision
        vyfjd__iut = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            gcd__psdnt = 0
            for A in arr_list:
                gcd__psdnt += len(A)
            jiv__qhzp = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                gcd__psdnt, iof__vyhl, vyfjd__iut)
            eocf__fzco = 0
            for A in arr_list:
                for i in range(len(A)):
                    jiv__qhzp._data[i + eocf__fzco] = A._data[i]
                    ogtxc__zgy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jiv__qhzp.
                        _null_bitmap, i + eocf__fzco, ogtxc__zgy)
                eocf__fzco += len(A)
            return jiv__qhzp
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        pyrbx__avpx) for pyrbx__avpx in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            iys__jbzb = arr_list.types[0]
        else:
            iys__jbzb = arr_list.dtype
        iys__jbzb = to_str_arr_if_dict_array(iys__jbzb)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            xunv__whtlr = 0
            xvr__qysd = 0
            for A in arr_list:
                arr = A
                xunv__whtlr += len(arr)
                xvr__qysd += bodo.libs.str_arr_ext.num_total_chars(arr)
            dkyvl__jkkf = bodo.utils.utils.alloc_type(xunv__whtlr,
                iys__jbzb, (xvr__qysd,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(dkyvl__jkkf, -1)
            vqzu__eape = 0
            lqqh__ckmj = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(dkyvl__jkkf,
                    arr, vqzu__eape, lqqh__ckmj)
                vqzu__eape += len(arr)
                lqqh__ckmj += bodo.libs.str_arr_ext.num_total_chars(arr)
            return dkyvl__jkkf
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(pyrbx__avpx.dtype, types.Integer) for
        pyrbx__avpx in arr_list.types) and any(isinstance(pyrbx__avpx,
        IntegerArrayType) for pyrbx__avpx in arr_list.types):

        def impl_int_arr_list(arr_list):
            hcc__knfgq = convert_to_nullable_tup(arr_list)
            rjtcf__tjlc = []
            xxny__msk = 0
            for A in hcc__knfgq:
                rjtcf__tjlc.append(A._data)
                xxny__msk += len(A)
            mfj__viv = bodo.libs.array_kernels.concat(rjtcf__tjlc)
            uic__uqrrc = xxny__msk + 7 >> 3
            zzw__yfoun = np.empty(uic__uqrrc, np.uint8)
            qayxp__sfx = 0
            for A in hcc__knfgq:
                cmt__lxjts = A._null_bitmap
                for lmn__upf in range(len(A)):
                    ogtxc__zgy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        cmt__lxjts, lmn__upf)
                    bodo.libs.int_arr_ext.set_bit_to_arr(zzw__yfoun,
                        qayxp__sfx, ogtxc__zgy)
                    qayxp__sfx += 1
            return bodo.libs.int_arr_ext.init_integer_array(mfj__viv,
                zzw__yfoun)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(pyrbx__avpx.dtype == types.bool_ for
        pyrbx__avpx in arr_list.types) and any(pyrbx__avpx == boolean_array for
        pyrbx__avpx in arr_list.types):

        def impl_bool_arr_list(arr_list):
            hcc__knfgq = convert_to_nullable_tup(arr_list)
            rjtcf__tjlc = []
            xxny__msk = 0
            for A in hcc__knfgq:
                rjtcf__tjlc.append(A._data)
                xxny__msk += len(A)
            mfj__viv = bodo.libs.array_kernels.concat(rjtcf__tjlc)
            uic__uqrrc = xxny__msk + 7 >> 3
            zzw__yfoun = np.empty(uic__uqrrc, np.uint8)
            qayxp__sfx = 0
            for A in hcc__knfgq:
                cmt__lxjts = A._null_bitmap
                for lmn__upf in range(len(A)):
                    ogtxc__zgy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        cmt__lxjts, lmn__upf)
                    bodo.libs.int_arr_ext.set_bit_to_arr(zzw__yfoun,
                        qayxp__sfx, ogtxc__zgy)
                    qayxp__sfx += 1
            return bodo.libs.bool_arr_ext.init_bool_array(mfj__viv, zzw__yfoun)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            liot__muo = []
            for A in arr_list:
                liot__muo.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                liot__muo), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        dcnsd__agqlj = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        ogd__lgdv = 'def impl(arr_list):\n'
        ogd__lgdv += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({dcnsd__agqlj},)), arr_list[0].dtype)
"""
        ikgw__hjscy = {}
        exec(ogd__lgdv, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, ikgw__hjscy)
        return ikgw__hjscy['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            xxny__msk = 0
            for A in arr_list:
                xxny__msk += len(A)
            dkyvl__jkkf = np.empty(xxny__msk, dtype)
            zxdh__qhq = 0
            for A in arr_list:
                n = len(A)
                dkyvl__jkkf[zxdh__qhq:zxdh__qhq + n] = A
                zxdh__qhq += n
            return dkyvl__jkkf
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(pyrbx__avpx,
        (types.Array, IntegerArrayType)) and isinstance(pyrbx__avpx.dtype,
        types.Integer) for pyrbx__avpx in arr_list.types) and any(
        isinstance(pyrbx__avpx, types.Array) and isinstance(pyrbx__avpx.
        dtype, types.Float) for pyrbx__avpx in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            nyg__xsy = []
            for A in arr_list:
                nyg__xsy.append(A._data)
            irh__tftmf = bodo.libs.array_kernels.concat(nyg__xsy)
            rnotk__bezf = bodo.libs.map_arr_ext.init_map_arr(irh__tftmf)
            return rnotk__bezf
        return impl_map_arr_list
    for yplxq__khs in arr_list:
        if not isinstance(yplxq__khs, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(pyrbx__avpx.astype(np.float64) for pyrbx__avpx in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    whgk__iwd = len(arr_tup.types)
    ogd__lgdv = 'def f(arr_tup):\n'
    ogd__lgdv += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(whgk__iwd
        )), ',' if whgk__iwd == 1 else '')
    cwgh__hesac = {}
    exec(ogd__lgdv, {'np': np}, cwgh__hesac)
    frj__fxq = cwgh__hesac['f']
    return frj__fxq


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    whgk__iwd = len(arr_tup.types)
    fjbrq__oltau = find_common_np_dtype(arr_tup.types)
    sne__gktgr = None
    vvs__osh = ''
    if isinstance(fjbrq__oltau, types.Integer):
        sne__gktgr = bodo.libs.int_arr_ext.IntDtype(fjbrq__oltau)
        vvs__osh = '.astype(out_dtype, False)'
    ogd__lgdv = 'def f(arr_tup):\n'
    ogd__lgdv += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, vvs__osh) for i in range(whgk__iwd)), ',' if whgk__iwd ==
        1 else '')
    cwgh__hesac = {}
    exec(ogd__lgdv, {'bodo': bodo, 'out_dtype': sne__gktgr}, cwgh__hesac)
    zxm__kpt = cwgh__hesac['f']
    return zxm__kpt


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, usfz__pmmk = build_set_seen_na(A)
        return len(s) + int(not dropna and usfz__pmmk)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        atnb__zdh = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        xuo__sdvbz = len(atnb__zdh)
        return bodo.libs.distributed_api.dist_reduce(xuo__sdvbz, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([rozr__obrc for rozr__obrc in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        ackpa__onhhg = np.finfo(A.dtype(1).dtype).max
    else:
        ackpa__onhhg = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        dkyvl__jkkf = np.empty(n, A.dtype)
        haevm__tso = ackpa__onhhg
        for i in range(n):
            haevm__tso = min(haevm__tso, A[i])
            dkyvl__jkkf[i] = haevm__tso
        return dkyvl__jkkf
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        ackpa__onhhg = np.finfo(A.dtype(1).dtype).min
    else:
        ackpa__onhhg = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        dkyvl__jkkf = np.empty(n, A.dtype)
        haevm__tso = ackpa__onhhg
        for i in range(n):
            haevm__tso = max(haevm__tso, A[i])
            dkyvl__jkkf[i] = haevm__tso
        return dkyvl__jkkf
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        nzvp__noil = arr_info_list_to_table([array_to_info(A)])
        zgkh__afh = 1
        tzz__zwtt = 0
        wfmw__uncoo = drop_duplicates_table(nzvp__noil, parallel, zgkh__afh,
            tzz__zwtt, dropna, True)
        dkyvl__jkkf = info_to_array(info_from_table(wfmw__uncoo, 0), A)
        delete_table(nzvp__noil)
        delete_table(wfmw__uncoo)
        return dkyvl__jkkf
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    cgb__cekah = bodo.utils.typing.to_nullable_type(arr.dtype)
    eublt__klf = index_arr
    uzi__bzqrv = eublt__klf.dtype

    def impl(arr, index_arr):
        n = len(arr)
        wzfh__kldl = init_nested_counts(cgb__cekah)
        mljr__jwfcz = init_nested_counts(uzi__bzqrv)
        for i in range(n):
            mqs__jiv = index_arr[i]
            if isna(arr, i):
                wzfh__kldl = (wzfh__kldl[0] + 1,) + wzfh__kldl[1:]
                mljr__jwfcz = add_nested_counts(mljr__jwfcz, mqs__jiv)
                continue
            twhzf__xwg = arr[i]
            if len(twhzf__xwg) == 0:
                wzfh__kldl = (wzfh__kldl[0] + 1,) + wzfh__kldl[1:]
                mljr__jwfcz = add_nested_counts(mljr__jwfcz, mqs__jiv)
                continue
            wzfh__kldl = add_nested_counts(wzfh__kldl, twhzf__xwg)
            for zijey__ceb in range(len(twhzf__xwg)):
                mljr__jwfcz = add_nested_counts(mljr__jwfcz, mqs__jiv)
        dkyvl__jkkf = bodo.utils.utils.alloc_type(wzfh__kldl[0], cgb__cekah,
            wzfh__kldl[1:])
        aoiie__zydjt = bodo.utils.utils.alloc_type(wzfh__kldl[0],
            eublt__klf, mljr__jwfcz)
        wprba__vctxp = 0
        for i in range(n):
            if isna(arr, i):
                setna(dkyvl__jkkf, wprba__vctxp)
                aoiie__zydjt[wprba__vctxp] = index_arr[i]
                wprba__vctxp += 1
                continue
            twhzf__xwg = arr[i]
            qzzs__oueqg = len(twhzf__xwg)
            if qzzs__oueqg == 0:
                setna(dkyvl__jkkf, wprba__vctxp)
                aoiie__zydjt[wprba__vctxp] = index_arr[i]
                wprba__vctxp += 1
                continue
            dkyvl__jkkf[wprba__vctxp:wprba__vctxp + qzzs__oueqg] = twhzf__xwg
            aoiie__zydjt[wprba__vctxp:wprba__vctxp + qzzs__oueqg] = index_arr[i
                ]
            wprba__vctxp += qzzs__oueqg
        return dkyvl__jkkf, aoiie__zydjt
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    cgb__cekah = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        wzfh__kldl = init_nested_counts(cgb__cekah)
        for i in range(n):
            if isna(arr, i):
                wzfh__kldl = (wzfh__kldl[0] + 1,) + wzfh__kldl[1:]
                shqvj__cyrv = 1
            else:
                twhzf__xwg = arr[i]
                vyes__sucd = len(twhzf__xwg)
                if vyes__sucd == 0:
                    wzfh__kldl = (wzfh__kldl[0] + 1,) + wzfh__kldl[1:]
                    shqvj__cyrv = 1
                    continue
                else:
                    wzfh__kldl = add_nested_counts(wzfh__kldl, twhzf__xwg)
                    shqvj__cyrv = vyes__sucd
            if counts[i] != shqvj__cyrv:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        dkyvl__jkkf = bodo.utils.utils.alloc_type(wzfh__kldl[0], cgb__cekah,
            wzfh__kldl[1:])
        wprba__vctxp = 0
        for i in range(n):
            if isna(arr, i):
                setna(dkyvl__jkkf, wprba__vctxp)
                wprba__vctxp += 1
                continue
            twhzf__xwg = arr[i]
            qzzs__oueqg = len(twhzf__xwg)
            if qzzs__oueqg == 0:
                setna(dkyvl__jkkf, wprba__vctxp)
                wprba__vctxp += 1
                continue
            dkyvl__jkkf[wprba__vctxp:wprba__vctxp + qzzs__oueqg] = twhzf__xwg
            wprba__vctxp += qzzs__oueqg
        return dkyvl__jkkf
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(zof__yiq) for zof__yiq in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        kfjm__gie = 'np.empty(n, np.int64)'
        dfyd__ehde = 'out_arr[i] = 1'
        igff__kng = 'max(len(arr[i]), 1)'
    else:
        kfjm__gie = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        dfyd__ehde = 'bodo.libs.array_kernels.setna(out_arr, i)'
        igff__kng = 'len(arr[i])'
    ogd__lgdv = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {kfjm__gie}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {dfyd__ehde}
        else:
            out_arr[i] = {igff__kng}
    return out_arr
    """
    cwgh__hesac = {}
    exec(ogd__lgdv, {'bodo': bodo, 'numba': numba, 'np': np}, cwgh__hesac)
    impl = cwgh__hesac['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    eublt__klf = index_arr
    uzi__bzqrv = eublt__klf.dtype

    def impl(arr, pat, n, index_arr):
        cvpx__ovuxf = pat is not None and len(pat) > 1
        if cvpx__ovuxf:
            xrk__tzhp = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        fjvny__vueam = len(arr)
        xunv__whtlr = 0
        xvr__qysd = 0
        mljr__jwfcz = init_nested_counts(uzi__bzqrv)
        for i in range(fjvny__vueam):
            mqs__jiv = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                xunv__whtlr += 1
                mljr__jwfcz = add_nested_counts(mljr__jwfcz, mqs__jiv)
                continue
            if cvpx__ovuxf:
                qnvg__arg = xrk__tzhp.split(arr[i], maxsplit=n)
            else:
                qnvg__arg = arr[i].split(pat, n)
            xunv__whtlr += len(qnvg__arg)
            for s in qnvg__arg:
                mljr__jwfcz = add_nested_counts(mljr__jwfcz, mqs__jiv)
                xvr__qysd += bodo.libs.str_arr_ext.get_utf8_size(s)
        dkyvl__jkkf = bodo.libs.str_arr_ext.pre_alloc_string_array(xunv__whtlr,
            xvr__qysd)
        aoiie__zydjt = bodo.utils.utils.alloc_type(xunv__whtlr, eublt__klf,
            mljr__jwfcz)
        acluy__gxz = 0
        for lmn__upf in range(fjvny__vueam):
            if isna(arr, lmn__upf):
                dkyvl__jkkf[acluy__gxz] = ''
                bodo.libs.array_kernels.setna(dkyvl__jkkf, acluy__gxz)
                aoiie__zydjt[acluy__gxz] = index_arr[lmn__upf]
                acluy__gxz += 1
                continue
            if cvpx__ovuxf:
                qnvg__arg = xrk__tzhp.split(arr[lmn__upf], maxsplit=n)
            else:
                qnvg__arg = arr[lmn__upf].split(pat, n)
            jrxkz__wsaq = len(qnvg__arg)
            dkyvl__jkkf[acluy__gxz:acluy__gxz + jrxkz__wsaq] = qnvg__arg
            aoiie__zydjt[acluy__gxz:acluy__gxz + jrxkz__wsaq] = index_arr[
                lmn__upf]
            acluy__gxz += jrxkz__wsaq
        return dkyvl__jkkf, aoiie__zydjt
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
            dkyvl__jkkf = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                dkyvl__jkkf[i] = np.nan
            return dkyvl__jkkf
        return impl_float
    iibk__xjf = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        dkyvl__jkkf = bodo.utils.utils.alloc_type(n, iibk__xjf, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(dkyvl__jkkf, i)
        return dkyvl__jkkf
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
    yuehv__ste = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            dkyvl__jkkf = bodo.utils.utils.alloc_type(new_len, yuehv__ste)
            bodo.libs.str_arr_ext.str_copy_ptr(dkyvl__jkkf.ctypes, 0, A.
                ctypes, old_size)
            return dkyvl__jkkf
        return impl_char

    def impl(A, old_size, new_len):
        dkyvl__jkkf = bodo.utils.utils.alloc_type(new_len, yuehv__ste, (-1,))
        dkyvl__jkkf[:old_size] = A[:old_size]
        return dkyvl__jkkf
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    rlr__tlttz = math.ceil((stop - start) / step)
    return int(max(rlr__tlttz, 0))


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
    if any(isinstance(rozr__obrc, types.Complex) for rozr__obrc in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            birko__vblti = (stop - start) / step
            rlr__tlttz = math.ceil(birko__vblti.real)
            kvm__lbpj = math.ceil(birko__vblti.imag)
            ksyou__dhs = int(max(min(kvm__lbpj, rlr__tlttz), 0))
            arr = np.empty(ksyou__dhs, dtype)
            for i in numba.parfors.parfor.internal_prange(ksyou__dhs):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            ksyou__dhs = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(ksyou__dhs, dtype)
            for i in numba.parfors.parfor.internal_prange(ksyou__dhs):
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
        dyg__gsan = arr,
        if not inplace:
            dyg__gsan = arr.copy(),
        vrcn__fije = bodo.libs.str_arr_ext.to_list_if_immutable_arr(dyg__gsan)
        mpl__rvu = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(vrcn__fije, 0, n, mpl__rvu)
        if not ascending:
            bodo.libs.timsort.reverseRange(vrcn__fije, 0, n, mpl__rvu)
        bodo.libs.str_arr_ext.cp_str_list_to_array(dyg__gsan, vrcn__fije)
        return dyg__gsan[0]
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
        rnotk__bezf = []
        for i in range(n):
            if A[i]:
                rnotk__bezf.append(i + offset)
        return np.array(rnotk__bezf, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    yuehv__ste = element_type(A)
    if yuehv__ste == types.unicode_type:
        null_value = '""'
    elif yuehv__ste == types.bool_:
        null_value = 'False'
    elif yuehv__ste == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif yuehv__ste == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    acluy__gxz = 'i'
    hdjq__wob = False
    ycno__qgqz = get_overload_const_str(method)
    if ycno__qgqz in ('ffill', 'pad'):
        bfch__pohue = 'n'
        send_right = True
    elif ycno__qgqz in ('backfill', 'bfill'):
        bfch__pohue = 'n-1, -1, -1'
        send_right = False
        if yuehv__ste == types.unicode_type:
            acluy__gxz = '(n - 1) - i'
            hdjq__wob = True
    ogd__lgdv = 'def impl(A, method, parallel=False):\n'
    ogd__lgdv += '  A = decode_if_dict_array(A)\n'
    ogd__lgdv += '  has_last_value = False\n'
    ogd__lgdv += f'  last_value = {null_value}\n'
    ogd__lgdv += '  if parallel:\n'
    ogd__lgdv += '    rank = bodo.libs.distributed_api.get_rank()\n'
    ogd__lgdv += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    ogd__lgdv += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    ogd__lgdv += '  n = len(A)\n'
    ogd__lgdv += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    ogd__lgdv += f'  for i in range({bfch__pohue}):\n'
    ogd__lgdv += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    ogd__lgdv += (
        f'      bodo.libs.array_kernels.setna(out_arr, {acluy__gxz})\n')
    ogd__lgdv += '      continue\n'
    ogd__lgdv += '    s = A[i]\n'
    ogd__lgdv += '    if bodo.libs.array_kernels.isna(A, i):\n'
    ogd__lgdv += '      s = last_value\n'
    ogd__lgdv += f'    out_arr[{acluy__gxz}] = s\n'
    ogd__lgdv += '    last_value = s\n'
    ogd__lgdv += '    has_last_value = True\n'
    if hdjq__wob:
        ogd__lgdv += '  return out_arr[::-1]\n'
    else:
        ogd__lgdv += '  return out_arr\n'
    ofj__vbs = {}
    exec(ogd__lgdv, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, ofj__vbs)
    impl = ofj__vbs['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        jkum__jmz = 0
        eua__jhy = n_pes - 1
        hufy__endi = np.int32(rank + 1)
        aqnjr__upr = np.int32(rank - 1)
        kjd__njahb = len(in_arr) - 1
        uvf__xru = -1
        zjc__mgcmb = -1
    else:
        jkum__jmz = n_pes - 1
        eua__jhy = 0
        hufy__endi = np.int32(rank - 1)
        aqnjr__upr = np.int32(rank + 1)
        kjd__njahb = 0
        uvf__xru = len(in_arr)
        zjc__mgcmb = 1
    ytimy__zukwe = np.int32(bodo.hiframes.rolling.comm_border_tag)
    hhnac__fbk = np.empty(1, dtype=np.bool_)
    mcvcm__kxqtb = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    pdwcq__iqi = np.empty(1, dtype=np.bool_)
    amc__tbns = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    pep__xmfkc = False
    fmqb__qyg = null_value
    for i in range(kjd__njahb, uvf__xru, zjc__mgcmb):
        if not isna(in_arr, i):
            pep__xmfkc = True
            fmqb__qyg = in_arr[i]
            break
    if rank != jkum__jmz:
        xyegb__beju = bodo.libs.distributed_api.irecv(hhnac__fbk, 1,
            aqnjr__upr, ytimy__zukwe, True)
        bodo.libs.distributed_api.wait(xyegb__beju, True)
        iddnm__fgxuj = bodo.libs.distributed_api.irecv(mcvcm__kxqtb, 1,
            aqnjr__upr, ytimy__zukwe, True)
        bodo.libs.distributed_api.wait(iddnm__fgxuj, True)
        zdhxl__ium = hhnac__fbk[0]
        iwzhg__qxpy = mcvcm__kxqtb[0]
    else:
        zdhxl__ium = False
        iwzhg__qxpy = null_value
    if pep__xmfkc:
        pdwcq__iqi[0] = pep__xmfkc
        amc__tbns[0] = fmqb__qyg
    else:
        pdwcq__iqi[0] = zdhxl__ium
        amc__tbns[0] = iwzhg__qxpy
    if rank != eua__jhy:
        nhl__cobvu = bodo.libs.distributed_api.isend(pdwcq__iqi, 1,
            hufy__endi, ytimy__zukwe, True)
        kxd__fafm = bodo.libs.distributed_api.isend(amc__tbns, 1,
            hufy__endi, ytimy__zukwe, True)
    return zdhxl__ium, iwzhg__qxpy


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    pzybj__xegpp = {'axis': axis, 'kind': kind, 'order': order}
    kwsge__qcw = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', pzybj__xegpp, kwsge__qcw, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    yuehv__ste = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            fjvny__vueam = len(A)
            dkyvl__jkkf = bodo.utils.utils.alloc_type(fjvny__vueam *
                repeats, yuehv__ste, (-1,))
            for i in range(fjvny__vueam):
                acluy__gxz = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for lmn__upf in range(repeats):
                        bodo.libs.array_kernels.setna(dkyvl__jkkf, 
                            acluy__gxz + lmn__upf)
                else:
                    dkyvl__jkkf[acluy__gxz:acluy__gxz + repeats] = A[i]
            return dkyvl__jkkf
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        fjvny__vueam = len(A)
        dkyvl__jkkf = bodo.utils.utils.alloc_type(repeats.sum(), yuehv__ste,
            (-1,))
        acluy__gxz = 0
        for i in range(fjvny__vueam):
            tju__uzfez = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for lmn__upf in range(tju__uzfez):
                    bodo.libs.array_kernels.setna(dkyvl__jkkf, acluy__gxz +
                        lmn__upf)
            else:
                dkyvl__jkkf[acluy__gxz:acluy__gxz + tju__uzfez] = A[i]
            acluy__gxz += tju__uzfez
        return dkyvl__jkkf
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
        wrgvd__qrx = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(wrgvd__qrx, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        qqq__egd = bodo.libs.array_kernels.concat([A1, A2])
        hfez__uqm = bodo.libs.array_kernels.unique(qqq__egd)
        return pd.Series(hfez__uqm).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    pzybj__xegpp = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    kwsge__qcw = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', pzybj__xegpp, kwsge__qcw, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        dcw__izd = bodo.libs.array_kernels.unique(A1)
        nkixf__rajl = bodo.libs.array_kernels.unique(A2)
        qqq__egd = bodo.libs.array_kernels.concat([dcw__izd, nkixf__rajl])
        tcf__abu = pd.Series(qqq__egd).sort_values().values
        return slice_array_intersect1d(tcf__abu)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    ivaf__plhm = arr[1:] == arr[:-1]
    return arr[:-1][ivaf__plhm]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    pzybj__xegpp = {'assume_unique': assume_unique}
    kwsge__qcw = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', pzybj__xegpp, kwsge__qcw, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        dcw__izd = bodo.libs.array_kernels.unique(A1)
        nkixf__rajl = bodo.libs.array_kernels.unique(A2)
        ivaf__plhm = calculate_mask_setdiff1d(dcw__izd, nkixf__rajl)
        return pd.Series(dcw__izd[ivaf__plhm]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    ivaf__plhm = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        ivaf__plhm &= A1 != A2[i]
    return ivaf__plhm


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    pzybj__xegpp = {'retstep': retstep, 'axis': axis}
    kwsge__qcw = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', pzybj__xegpp, kwsge__qcw, 'numpy')
    enn__rrevm = False
    if is_overload_none(dtype):
        yuehv__ste = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            enn__rrevm = True
        yuehv__ste = numba.np.numpy_support.as_dtype(dtype).type
    if enn__rrevm:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            fbla__wemgx = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            dkyvl__jkkf = np.empty(num, yuehv__ste)
            for i in numba.parfors.parfor.internal_prange(num):
                dkyvl__jkkf[i] = yuehv__ste(np.floor(start + i * fbla__wemgx))
            return dkyvl__jkkf
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            fbla__wemgx = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            dkyvl__jkkf = np.empty(num, yuehv__ste)
            for i in numba.parfors.parfor.internal_prange(num):
                dkyvl__jkkf[i] = yuehv__ste(start + i * fbla__wemgx)
            return dkyvl__jkkf
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
        whgk__iwd = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                whgk__iwd += A[i] == val
        return whgk__iwd > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    pzybj__xegpp = {'axis': axis, 'out': out, 'keepdims': keepdims}
    kwsge__qcw = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', pzybj__xegpp, kwsge__qcw, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        whgk__iwd = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                whgk__iwd += int(bool(A[i]))
        return whgk__iwd > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    pzybj__xegpp = {'axis': axis, 'out': out, 'keepdims': keepdims}
    kwsge__qcw = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', pzybj__xegpp, kwsge__qcw, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        whgk__iwd = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                whgk__iwd += int(bool(A[i]))
        return whgk__iwd == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    pzybj__xegpp = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    kwsge__qcw = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', pzybj__xegpp, kwsge__qcw, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        ruj__jyj = np.promote_types(numba.np.numpy_support.as_dtype(A.dtype
            ), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            dkyvl__jkkf = np.empty(n, ruj__jyj)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(dkyvl__jkkf, i)
                    continue
                dkyvl__jkkf[i] = np_cbrt_scalar(A[i], ruj__jyj)
            return dkyvl__jkkf
        return impl_arr
    ruj__jyj = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, ruj__jyj)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    itsc__dtvcz = x < 0
    if itsc__dtvcz:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if itsc__dtvcz:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    dngjw__nizh = isinstance(tup, (types.BaseTuple, types.List))
    ocp__comp = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for yplxq__khs in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                yplxq__khs, 'numpy.hstack()')
            dngjw__nizh = dngjw__nizh and bodo.utils.utils.is_array_typ(
                yplxq__khs, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        dngjw__nizh = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif ocp__comp:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        kyhs__fryxy = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for yplxq__khs in kyhs__fryxy.types:
            ocp__comp = ocp__comp and bodo.utils.utils.is_array_typ(yplxq__khs,
                False)
    if not (dngjw__nizh or ocp__comp):
        return
    if ocp__comp:

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
    pzybj__xegpp = {'check_valid': check_valid, 'tol': tol}
    kwsge__qcw = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', pzybj__xegpp,
        kwsge__qcw, 'numpy')
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
        ujw__poijs = mean.shape[0]
        xpqvz__hekqu = size, ujw__poijs
        kdp__wvdt = np.random.standard_normal(xpqvz__hekqu)
        cov = cov.astype(np.float64)
        muqxe__ktin, s, lnsj__fgbo = np.linalg.svd(cov)
        res = np.dot(kdp__wvdt, np.sqrt(s).reshape(ujw__poijs, 1) * lnsj__fgbo)
        phe__qtj = res + mean
        return phe__qtj
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
            qbijz__ltftl = bodo.hiframes.series_kernels._get_type_max_value(arr
                )
            tmq__wiut = typing.builtins.IndexValue(-1, qbijz__ltftl)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                tcpbi__ijw = typing.builtins.IndexValue(i, arr[i])
                tmq__wiut = min(tmq__wiut, tcpbi__ijw)
            return tmq__wiut.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        pfdd__rui = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            aba__qyvl = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            qbijz__ltftl = pfdd__rui(len(arr.dtype.categories) + 1)
            tmq__wiut = typing.builtins.IndexValue(-1, qbijz__ltftl)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                tcpbi__ijw = typing.builtins.IndexValue(i, aba__qyvl[i])
                tmq__wiut = min(tmq__wiut, tcpbi__ijw)
            return tmq__wiut.index
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
            qbijz__ltftl = bodo.hiframes.series_kernels._get_type_min_value(arr
                )
            tmq__wiut = typing.builtins.IndexValue(-1, qbijz__ltftl)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                tcpbi__ijw = typing.builtins.IndexValue(i, arr[i])
                tmq__wiut = max(tmq__wiut, tcpbi__ijw)
            return tmq__wiut.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        pfdd__rui = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            aba__qyvl = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            qbijz__ltftl = pfdd__rui(-1)
            tmq__wiut = typing.builtins.IndexValue(-1, qbijz__ltftl)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                tcpbi__ijw = typing.builtins.IndexValue(i, aba__qyvl[i])
                tmq__wiut = max(tmq__wiut, tcpbi__ijw)
            return tmq__wiut.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
