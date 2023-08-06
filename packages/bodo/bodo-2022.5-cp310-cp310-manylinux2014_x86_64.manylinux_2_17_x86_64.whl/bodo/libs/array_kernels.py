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
        idxwy__czec = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = idxwy__czec
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        idxwy__czec = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = idxwy__czec
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
            xjf__wcdz = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            xjf__wcdz[ind + 1] = xjf__wcdz[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            xjf__wcdz = bodo.libs.array_item_arr_ext.get_offsets(arr)
            xjf__wcdz[ind + 1] = xjf__wcdz[ind]
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
    pfrh__yjp = arr_tup.count
    owaat__voq = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(pfrh__yjp):
        owaat__voq += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    owaat__voq += '  return\n'
    uov__ktfi = {}
    exec(owaat__voq, {'setna': setna}, uov__ktfi)
    impl = uov__ktfi['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        gtowg__jghf = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(gtowg__jghf.start, gtowg__jghf.stop, gtowg__jghf.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        qeqa__jgvxd = 'n'
        vvhnn__tgev = 'n_pes'
        fme__pvf = 'min_op'
    else:
        qeqa__jgvxd = 'n-1, -1, -1'
        vvhnn__tgev = '-1'
        fme__pvf = 'max_op'
    owaat__voq = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {vvhnn__tgev}
    for i in range({qeqa__jgvxd}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {fme__pvf}))
        if possible_valid_rank != {vvhnn__tgev}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    uov__ktfi = {}
    exec(owaat__voq, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, uov__ktfi)
    impl = uov__ktfi['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    yzvpm__allp = array_to_info(arr)
    _median_series_computation(res, yzvpm__allp, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(yzvpm__allp)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    yzvpm__allp = array_to_info(arr)
    _autocorr_series_computation(res, yzvpm__allp, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(yzvpm__allp)


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
    yzvpm__allp = array_to_info(arr)
    _compute_series_monotonicity(res, yzvpm__allp, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(yzvpm__allp)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    esib__gnt = res[0] > 0.5
    return esib__gnt


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        kvbtr__pigk = '-'
        gcpx__pgsu = 'index_arr[0] > threshhold_date'
        qeqa__jgvxd = '1, n+1'
        lut__mna = 'index_arr[-i] <= threshhold_date'
        lewq__zfhx = 'i - 1'
    else:
        kvbtr__pigk = '+'
        gcpx__pgsu = 'index_arr[-1] < threshhold_date'
        qeqa__jgvxd = 'n'
        lut__mna = 'index_arr[i] >= threshhold_date'
        lewq__zfhx = 'i'
    owaat__voq = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        owaat__voq += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        owaat__voq += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            owaat__voq += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            owaat__voq += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            owaat__voq += '    else:\n'
            owaat__voq += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            owaat__voq += (
                f'    threshhold_date = initial_date {kvbtr__pigk} date_offset\n'
                )
    else:
        owaat__voq += (
            f'  threshhold_date = initial_date {kvbtr__pigk} offset\n')
    owaat__voq += '  local_valid = 0\n'
    owaat__voq += f'  n = len(index_arr)\n'
    owaat__voq += f'  if n:\n'
    owaat__voq += f'    if {gcpx__pgsu}:\n'
    owaat__voq += '      loc_valid = n\n'
    owaat__voq += '    else:\n'
    owaat__voq += f'      for i in range({qeqa__jgvxd}):\n'
    owaat__voq += f'        if {lut__mna}:\n'
    owaat__voq += f'          loc_valid = {lewq__zfhx}\n'
    owaat__voq += '          break\n'
    owaat__voq += '  if is_parallel:\n'
    owaat__voq += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    owaat__voq += '    return total_valid\n'
    owaat__voq += '  else:\n'
    owaat__voq += '    return loc_valid\n'
    uov__ktfi = {}
    exec(owaat__voq, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, uov__ktfi)
    return uov__ktfi['impl']


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
    skbgl__lkqah = numba_to_c_type(sig.args[0].dtype)
    jdak__myb = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), skbgl__lkqah))
    ordcv__vjw = args[0]
    xuqt__jeoin = sig.args[0]
    if isinstance(xuqt__jeoin, (IntegerArrayType, BooleanArrayType)):
        ordcv__vjw = cgutils.create_struct_proxy(xuqt__jeoin)(context,
            builder, ordcv__vjw).data
        xuqt__jeoin = types.Array(xuqt__jeoin.dtype, 1, 'C')
    assert xuqt__jeoin.ndim == 1
    arr = make_array(xuqt__jeoin)(context, builder, ordcv__vjw)
    ytxdz__mbvp = builder.extract_value(arr.shape, 0)
    hxays__hunrd = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        ytxdz__mbvp, args[1], builder.load(jdak__myb)]
    jrnu__qjiw = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    kwkhp__sykc = lir.FunctionType(lir.DoubleType(), jrnu__qjiw)
    nere__tfwyb = cgutils.get_or_insert_function(builder.module,
        kwkhp__sykc, name='quantile_sequential')
    gti__gvwpx = builder.call(nere__tfwyb, hxays__hunrd)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return gti__gvwpx


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    skbgl__lkqah = numba_to_c_type(sig.args[0].dtype)
    jdak__myb = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), skbgl__lkqah))
    ordcv__vjw = args[0]
    xuqt__jeoin = sig.args[0]
    if isinstance(xuqt__jeoin, (IntegerArrayType, BooleanArrayType)):
        ordcv__vjw = cgutils.create_struct_proxy(xuqt__jeoin)(context,
            builder, ordcv__vjw).data
        xuqt__jeoin = types.Array(xuqt__jeoin.dtype, 1, 'C')
    assert xuqt__jeoin.ndim == 1
    arr = make_array(xuqt__jeoin)(context, builder, ordcv__vjw)
    ytxdz__mbvp = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        hwb__dusup = args[2]
    else:
        hwb__dusup = ytxdz__mbvp
    hxays__hunrd = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        ytxdz__mbvp, hwb__dusup, args[1], builder.load(jdak__myb)]
    jrnu__qjiw = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType
        (64), lir.DoubleType(), lir.IntType(32)]
    kwkhp__sykc = lir.FunctionType(lir.DoubleType(), jrnu__qjiw)
    nere__tfwyb = cgutils.get_or_insert_function(builder.module,
        kwkhp__sykc, name='quantile_parallel')
    gti__gvwpx = builder.call(nere__tfwyb, hxays__hunrd)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return gti__gvwpx


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    urm__ihtu = start
    nzvf__irn = 2 * start + 1
    gcgdi__bon = 2 * start + 2
    if nzvf__irn < n and not cmp_f(arr[nzvf__irn], arr[urm__ihtu]):
        urm__ihtu = nzvf__irn
    if gcgdi__bon < n and not cmp_f(arr[gcgdi__bon], arr[urm__ihtu]):
        urm__ihtu = gcgdi__bon
    if urm__ihtu != start:
        arr[start], arr[urm__ihtu] = arr[urm__ihtu], arr[start]
        ind_arr[start], ind_arr[urm__ihtu] = ind_arr[urm__ihtu], ind_arr[start]
        min_heapify(arr, ind_arr, n, urm__ihtu, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        mttt__dnju = np.empty(k, A.dtype)
        zryr__hwq = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                mttt__dnju[ind] = A[i]
                zryr__hwq[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            mttt__dnju = mttt__dnju[:ind]
            zryr__hwq = zryr__hwq[:ind]
        return mttt__dnju, zryr__hwq, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        lfi__plt = np.sort(A)
        lbdo__kvvx = index_arr[np.argsort(A)]
        spqwv__qgnh = pd.Series(lfi__plt).notna().values
        lfi__plt = lfi__plt[spqwv__qgnh]
        lbdo__kvvx = lbdo__kvvx[spqwv__qgnh]
        if is_largest:
            lfi__plt = lfi__plt[::-1]
            lbdo__kvvx = lbdo__kvvx[::-1]
        return np.ascontiguousarray(lfi__plt), np.ascontiguousarray(lbdo__kvvx)
    mttt__dnju, zryr__hwq, start = select_k_nonan(A, index_arr, m, k)
    zryr__hwq = zryr__hwq[mttt__dnju.argsort()]
    mttt__dnju.sort()
    if not is_largest:
        mttt__dnju = np.ascontiguousarray(mttt__dnju[::-1])
        zryr__hwq = np.ascontiguousarray(zryr__hwq[::-1])
    for i in range(start, m):
        if cmp_f(A[i], mttt__dnju[0]):
            mttt__dnju[0] = A[i]
            zryr__hwq[0] = index_arr[i]
            min_heapify(mttt__dnju, zryr__hwq, k, 0, cmp_f)
    zryr__hwq = zryr__hwq[mttt__dnju.argsort()]
    mttt__dnju.sort()
    if is_largest:
        mttt__dnju = mttt__dnju[::-1]
        zryr__hwq = zryr__hwq[::-1]
    return np.ascontiguousarray(mttt__dnju), np.ascontiguousarray(zryr__hwq)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    ksr__ljaky = bodo.libs.distributed_api.get_rank()
    ejzbo__hrf, ytt__mjvhj = nlargest(A, I, k, is_largest, cmp_f)
    roji__jeas = bodo.libs.distributed_api.gatherv(ejzbo__hrf)
    uxg__rewd = bodo.libs.distributed_api.gatherv(ytt__mjvhj)
    if ksr__ljaky == MPI_ROOT:
        res, qbgs__ulks = nlargest(roji__jeas, uxg__rewd, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        qbgs__ulks = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(qbgs__ulks)
    return res, qbgs__ulks


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    pgb__evu, xlmjz__ehhvj = mat.shape
    lmo__gykju = np.empty((xlmjz__ehhvj, xlmjz__ehhvj), dtype=np.float64)
    for qsfh__gqf in range(xlmjz__ehhvj):
        for fmn__vnkku in range(qsfh__gqf + 1):
            phjk__xkyoh = 0
            vyqa__dkiw = drmbo__dqm = wun__dro = nwydq__pqzuh = 0.0
            for i in range(pgb__evu):
                if np.isfinite(mat[i, qsfh__gqf]) and np.isfinite(mat[i,
                    fmn__vnkku]):
                    vcckl__rqide = mat[i, qsfh__gqf]
                    jhcou__lxm = mat[i, fmn__vnkku]
                    phjk__xkyoh += 1
                    wun__dro += vcckl__rqide
                    nwydq__pqzuh += jhcou__lxm
            if parallel:
                phjk__xkyoh = bodo.libs.distributed_api.dist_reduce(phjk__xkyoh
                    , sum_op)
                wun__dro = bodo.libs.distributed_api.dist_reduce(wun__dro,
                    sum_op)
                nwydq__pqzuh = bodo.libs.distributed_api.dist_reduce(
                    nwydq__pqzuh, sum_op)
            if phjk__xkyoh < minpv:
                lmo__gykju[qsfh__gqf, fmn__vnkku] = lmo__gykju[fmn__vnkku,
                    qsfh__gqf] = np.nan
            else:
                lka__cmr = wun__dro / phjk__xkyoh
                cuvs__dllyv = nwydq__pqzuh / phjk__xkyoh
                wun__dro = 0.0
                for i in range(pgb__evu):
                    if np.isfinite(mat[i, qsfh__gqf]) and np.isfinite(mat[i,
                        fmn__vnkku]):
                        vcckl__rqide = mat[i, qsfh__gqf] - lka__cmr
                        jhcou__lxm = mat[i, fmn__vnkku] - cuvs__dllyv
                        wun__dro += vcckl__rqide * jhcou__lxm
                        vyqa__dkiw += vcckl__rqide * vcckl__rqide
                        drmbo__dqm += jhcou__lxm * jhcou__lxm
                if parallel:
                    wun__dro = bodo.libs.distributed_api.dist_reduce(wun__dro,
                        sum_op)
                    vyqa__dkiw = bodo.libs.distributed_api.dist_reduce(
                        vyqa__dkiw, sum_op)
                    drmbo__dqm = bodo.libs.distributed_api.dist_reduce(
                        drmbo__dqm, sum_op)
                wbpgp__oyf = phjk__xkyoh - 1.0 if cov else sqrt(vyqa__dkiw *
                    drmbo__dqm)
                if wbpgp__oyf != 0.0:
                    lmo__gykju[qsfh__gqf, fmn__vnkku] = lmo__gykju[
                        fmn__vnkku, qsfh__gqf] = wun__dro / wbpgp__oyf
                else:
                    lmo__gykju[qsfh__gqf, fmn__vnkku] = lmo__gykju[
                        fmn__vnkku, qsfh__gqf] = np.nan
    return lmo__gykju


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    korr__cti = n != 1
    owaat__voq = 'def impl(data, parallel=False):\n'
    owaat__voq += '  if parallel:\n'
    fhpvf__yck = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    owaat__voq += f'    cpp_table = arr_info_list_to_table([{fhpvf__yck}])\n'
    owaat__voq += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    yyo__vabv = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    owaat__voq += f'    data = ({yyo__vabv},)\n'
    owaat__voq += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    owaat__voq += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    owaat__voq += '    bodo.libs.array.delete_table(cpp_table)\n'
    owaat__voq += '  n = len(data[0])\n'
    owaat__voq += '  out = np.empty(n, np.bool_)\n'
    owaat__voq += '  uniqs = dict()\n'
    if korr__cti:
        owaat__voq += '  for i in range(n):\n'
        wku__rvqol = ', '.join(f'data[{i}][i]' for i in range(n))
        wpbl__dja = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        owaat__voq += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({wku__rvqol},), ({wpbl__dja},))
"""
        owaat__voq += '    if val in uniqs:\n'
        owaat__voq += '      out[i] = True\n'
        owaat__voq += '    else:\n'
        owaat__voq += '      out[i] = False\n'
        owaat__voq += '      uniqs[val] = 0\n'
    else:
        owaat__voq += '  data = data[0]\n'
        owaat__voq += '  hasna = False\n'
        owaat__voq += '  for i in range(n):\n'
        owaat__voq += '    if bodo.libs.array_kernels.isna(data, i):\n'
        owaat__voq += '      out[i] = hasna\n'
        owaat__voq += '      hasna = True\n'
        owaat__voq += '    else:\n'
        owaat__voq += '      val = data[i]\n'
        owaat__voq += '      if val in uniqs:\n'
        owaat__voq += '        out[i] = True\n'
        owaat__voq += '      else:\n'
        owaat__voq += '        out[i] = False\n'
        owaat__voq += '        uniqs[val] = 0\n'
    owaat__voq += '  if parallel:\n'
    owaat__voq += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    owaat__voq += '  return out\n'
    uov__ktfi = {}
    exec(owaat__voq, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        uov__ktfi)
    impl = uov__ktfi['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    pfrh__yjp = len(data)
    owaat__voq = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    owaat__voq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        pfrh__yjp)))
    owaat__voq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    owaat__voq += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(pfrh__yjp))
    for cvyz__rlnpu in range(pfrh__yjp):
        owaat__voq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(cvyz__rlnpu, cvyz__rlnpu, cvyz__rlnpu))
    owaat__voq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(pfrh__yjp))
    owaat__voq += '  delete_table(out_table)\n'
    owaat__voq += '  delete_table(table_total)\n'
    owaat__voq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(pfrh__yjp)))
    uov__ktfi = {}
    exec(owaat__voq, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, uov__ktfi)
    impl = uov__ktfi['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    pfrh__yjp = len(data)
    owaat__voq = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    owaat__voq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        pfrh__yjp)))
    owaat__voq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    owaat__voq += '  keep_i = 0\n'
    owaat__voq += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for cvyz__rlnpu in range(pfrh__yjp):
        owaat__voq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(cvyz__rlnpu, cvyz__rlnpu, cvyz__rlnpu))
    owaat__voq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(pfrh__yjp))
    owaat__voq += '  delete_table(out_table)\n'
    owaat__voq += '  delete_table(table_total)\n'
    owaat__voq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(pfrh__yjp)))
    uov__ktfi = {}
    exec(owaat__voq, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, uov__ktfi)
    impl = uov__ktfi['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        ddkg__rpgb = [array_to_info(data_arr)]
        iopt__uqx = arr_info_list_to_table(ddkg__rpgb)
        jaizo__sfcvw = 0
        aumk__cyruc = drop_duplicates_table(iopt__uqx, parallel, 1,
            jaizo__sfcvw, False, True)
        sixi__sztht = info_to_array(info_from_table(aumk__cyruc, 0), data_arr)
        delete_table(aumk__cyruc)
        delete_table(iopt__uqx)
        return sixi__sztht
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    xlru__bmaj = len(data.types)
    mbfn__oacc = [('out' + str(i)) for i in range(xlru__bmaj)]
    hpf__jmbg = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    fjuzh__rkmuh = ['isna(data[{}], i)'.format(i) for i in hpf__jmbg]
    pwe__krq = 'not ({})'.format(' or '.join(fjuzh__rkmuh))
    if not is_overload_none(thresh):
        pwe__krq = '(({}) <= ({}) - thresh)'.format(' + '.join(fjuzh__rkmuh
            ), xlru__bmaj - 1)
    elif how == 'all':
        pwe__krq = 'not ({})'.format(' and '.join(fjuzh__rkmuh))
    owaat__voq = 'def _dropna_imp(data, how, thresh, subset):\n'
    owaat__voq += '  old_len = len(data[0])\n'
    owaat__voq += '  new_len = 0\n'
    owaat__voq += '  for i in range(old_len):\n'
    owaat__voq += '    if {}:\n'.format(pwe__krq)
    owaat__voq += '      new_len += 1\n'
    for i, out in enumerate(mbfn__oacc):
        if isinstance(data[i], bodo.CategoricalArrayType):
            owaat__voq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            owaat__voq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    owaat__voq += '  curr_ind = 0\n'
    owaat__voq += '  for i in range(old_len):\n'
    owaat__voq += '    if {}:\n'.format(pwe__krq)
    for i in range(xlru__bmaj):
        owaat__voq += '      if isna(data[{}], i):\n'.format(i)
        owaat__voq += '        setna({}, curr_ind)\n'.format(mbfn__oacc[i])
        owaat__voq += '      else:\n'
        owaat__voq += '        {}[curr_ind] = data[{}][i]\n'.format(mbfn__oacc
            [i], i)
    owaat__voq += '      curr_ind += 1\n'
    owaat__voq += '  return {}\n'.format(', '.join(mbfn__oacc))
    uov__ktfi = {}
    claw__ych = {'t{}'.format(i): bhlt__pqdak for i, bhlt__pqdak in
        enumerate(data.types)}
    claw__ych.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(owaat__voq, claw__ych, uov__ktfi)
    pijjq__anz = uov__ktfi['_dropna_imp']
    return pijjq__anz


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        xuqt__jeoin = arr.dtype
        jwoxh__snl = xuqt__jeoin.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            yhcbf__sbfwx = init_nested_counts(jwoxh__snl)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                yhcbf__sbfwx = add_nested_counts(yhcbf__sbfwx, val[ind])
            sixi__sztht = bodo.utils.utils.alloc_type(n, xuqt__jeoin,
                yhcbf__sbfwx)
            for sdwm__sesgn in range(n):
                if bodo.libs.array_kernels.isna(arr, sdwm__sesgn):
                    setna(sixi__sztht, sdwm__sesgn)
                    continue
                val = arr[sdwm__sesgn]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(sixi__sztht, sdwm__sesgn)
                    continue
                sixi__sztht[sdwm__sesgn] = val[ind]
            return sixi__sztht
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    jnu__rjwuv = _to_readonly(arr_types.types[0])
    return all(isinstance(bhlt__pqdak, CategoricalArrayType) and 
        _to_readonly(bhlt__pqdak) == jnu__rjwuv for bhlt__pqdak in
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
        fxqx__ipat = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            nwtbl__xjka = 0
            olz__ulyu = []
            for A in arr_list:
                clmg__yhvb = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                olz__ulyu.append(bodo.libs.array_item_arr_ext.get_data(A))
                nwtbl__xjka += clmg__yhvb
            wqcgk__jurlj = np.empty(nwtbl__xjka + 1, offset_type)
            zyw__tyuvh = bodo.libs.array_kernels.concat(olz__ulyu)
            ysb__mozn = np.empty(nwtbl__xjka + 7 >> 3, np.uint8)
            efaly__xeua = 0
            leqzr__xjucl = 0
            for A in arr_list:
                sixw__uhasy = bodo.libs.array_item_arr_ext.get_offsets(A)
                eag__iqrqu = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                clmg__yhvb = len(A)
                kmp__wisd = sixw__uhasy[clmg__yhvb]
                for i in range(clmg__yhvb):
                    wqcgk__jurlj[i + efaly__xeua] = sixw__uhasy[i
                        ] + leqzr__xjucl
                    eyq__rvg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        eag__iqrqu, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ysb__mozn, i +
                        efaly__xeua, eyq__rvg)
                efaly__xeua += clmg__yhvb
                leqzr__xjucl += kmp__wisd
            wqcgk__jurlj[efaly__xeua] = leqzr__xjucl
            sixi__sztht = bodo.libs.array_item_arr_ext.init_array_item_array(
                nwtbl__xjka, zyw__tyuvh, wqcgk__jurlj, ysb__mozn)
            return sixi__sztht
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        zpsu__qqqr = arr_list.dtype.names
        owaat__voq = 'def struct_array_concat_impl(arr_list):\n'
        owaat__voq += f'    n_all = 0\n'
        for i in range(len(zpsu__qqqr)):
            owaat__voq += f'    concat_list{i} = []\n'
        owaat__voq += '    for A in arr_list:\n'
        owaat__voq += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(zpsu__qqqr)):
            owaat__voq += f'        concat_list{i}.append(data_tuple[{i}])\n'
        owaat__voq += '        n_all += len(A)\n'
        owaat__voq += '    n_bytes = (n_all + 7) >> 3\n'
        owaat__voq += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        owaat__voq += '    curr_bit = 0\n'
        owaat__voq += '    for A in arr_list:\n'
        owaat__voq += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        owaat__voq += '        for j in range(len(A)):\n'
        owaat__voq += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        owaat__voq += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        owaat__voq += '            curr_bit += 1\n'
        owaat__voq += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        bzem__mhgu = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(zpsu__qqqr))])
        owaat__voq += f'        ({bzem__mhgu},),\n'
        owaat__voq += '        new_mask,\n'
        owaat__voq += f'        {zpsu__qqqr},\n'
        owaat__voq += '    )\n'
        uov__ktfi = {}
        exec(owaat__voq, {'bodo': bodo, 'np': np}, uov__ktfi)
        return uov__ktfi['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            zud__qzhsp = 0
            for A in arr_list:
                zud__qzhsp += len(A)
            iscf__esh = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(zud__qzhsp))
            lmuuy__slwmi = 0
            for A in arr_list:
                for i in range(len(A)):
                    iscf__esh._data[i + lmuuy__slwmi] = A._data[i]
                    eyq__rvg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iscf__esh.
                        _null_bitmap, i + lmuuy__slwmi, eyq__rvg)
                lmuuy__slwmi += len(A)
            return iscf__esh
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            zud__qzhsp = 0
            for A in arr_list:
                zud__qzhsp += len(A)
            iscf__esh = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(zud__qzhsp))
            lmuuy__slwmi = 0
            for A in arr_list:
                for i in range(len(A)):
                    iscf__esh._days_data[i + lmuuy__slwmi] = A._days_data[i]
                    iscf__esh._seconds_data[i + lmuuy__slwmi
                        ] = A._seconds_data[i]
                    iscf__esh._microseconds_data[i + lmuuy__slwmi
                        ] = A._microseconds_data[i]
                    eyq__rvg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iscf__esh.
                        _null_bitmap, i + lmuuy__slwmi, eyq__rvg)
                lmuuy__slwmi += len(A)
            return iscf__esh
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        eycon__cxgc = arr_list.dtype.precision
        xuqmg__cjj = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            zud__qzhsp = 0
            for A in arr_list:
                zud__qzhsp += len(A)
            iscf__esh = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                zud__qzhsp, eycon__cxgc, xuqmg__cjj)
            lmuuy__slwmi = 0
            for A in arr_list:
                for i in range(len(A)):
                    iscf__esh._data[i + lmuuy__slwmi] = A._data[i]
                    eyq__rvg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iscf__esh.
                        _null_bitmap, i + lmuuy__slwmi, eyq__rvg)
                lmuuy__slwmi += len(A)
            return iscf__esh
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        bhlt__pqdak) for bhlt__pqdak in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            jsod__yetd = arr_list.types[0]
        else:
            jsod__yetd = arr_list.dtype
        jsod__yetd = to_str_arr_if_dict_array(jsod__yetd)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            shi__szvv = 0
            bjpcn__ecvhe = 0
            for A in arr_list:
                arr = A
                shi__szvv += len(arr)
                bjpcn__ecvhe += bodo.libs.str_arr_ext.num_total_chars(arr)
            sixi__sztht = bodo.utils.utils.alloc_type(shi__szvv, jsod__yetd,
                (bjpcn__ecvhe,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(sixi__sztht, -1)
            qic__rfm = 0
            uqfr__jza = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(sixi__sztht,
                    arr, qic__rfm, uqfr__jza)
                qic__rfm += len(arr)
                uqfr__jza += bodo.libs.str_arr_ext.num_total_chars(arr)
            return sixi__sztht
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(bhlt__pqdak.dtype, types.Integer) for
        bhlt__pqdak in arr_list.types) and any(isinstance(bhlt__pqdak,
        IntegerArrayType) for bhlt__pqdak in arr_list.types):

        def impl_int_arr_list(arr_list):
            vqjk__fvsou = convert_to_nullable_tup(arr_list)
            qidpg__ojtfa = []
            bzdvk__yey = 0
            for A in vqjk__fvsou:
                qidpg__ojtfa.append(A._data)
                bzdvk__yey += len(A)
            zyw__tyuvh = bodo.libs.array_kernels.concat(qidpg__ojtfa)
            xpbx__nijb = bzdvk__yey + 7 >> 3
            fhfs__tflxv = np.empty(xpbx__nijb, np.uint8)
            iwu__wcvq = 0
            for A in vqjk__fvsou:
                otqk__vicj = A._null_bitmap
                for sdwm__sesgn in range(len(A)):
                    eyq__rvg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        otqk__vicj, sdwm__sesgn)
                    bodo.libs.int_arr_ext.set_bit_to_arr(fhfs__tflxv,
                        iwu__wcvq, eyq__rvg)
                    iwu__wcvq += 1
            return bodo.libs.int_arr_ext.init_integer_array(zyw__tyuvh,
                fhfs__tflxv)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(bhlt__pqdak.dtype == types.bool_ for
        bhlt__pqdak in arr_list.types) and any(bhlt__pqdak == boolean_array for
        bhlt__pqdak in arr_list.types):

        def impl_bool_arr_list(arr_list):
            vqjk__fvsou = convert_to_nullable_tup(arr_list)
            qidpg__ojtfa = []
            bzdvk__yey = 0
            for A in vqjk__fvsou:
                qidpg__ojtfa.append(A._data)
                bzdvk__yey += len(A)
            zyw__tyuvh = bodo.libs.array_kernels.concat(qidpg__ojtfa)
            xpbx__nijb = bzdvk__yey + 7 >> 3
            fhfs__tflxv = np.empty(xpbx__nijb, np.uint8)
            iwu__wcvq = 0
            for A in vqjk__fvsou:
                otqk__vicj = A._null_bitmap
                for sdwm__sesgn in range(len(A)):
                    eyq__rvg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        otqk__vicj, sdwm__sesgn)
                    bodo.libs.int_arr_ext.set_bit_to_arr(fhfs__tflxv,
                        iwu__wcvq, eyq__rvg)
                    iwu__wcvq += 1
            return bodo.libs.bool_arr_ext.init_bool_array(zyw__tyuvh,
                fhfs__tflxv)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            xdbrz__utymw = []
            for A in arr_list:
                xdbrz__utymw.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                xdbrz__utymw), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        lqpaj__qzrya = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        owaat__voq = 'def impl(arr_list):\n'
        owaat__voq += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({lqpaj__qzrya},)), arr_list[0].dtype)
"""
        ncah__nnd = {}
        exec(owaat__voq, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, ncah__nnd)
        return ncah__nnd['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            bzdvk__yey = 0
            for A in arr_list:
                bzdvk__yey += len(A)
            sixi__sztht = np.empty(bzdvk__yey, dtype)
            jvkcp__yfnr = 0
            for A in arr_list:
                n = len(A)
                sixi__sztht[jvkcp__yfnr:jvkcp__yfnr + n] = A
                jvkcp__yfnr += n
            return sixi__sztht
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(bhlt__pqdak,
        (types.Array, IntegerArrayType)) and isinstance(bhlt__pqdak.dtype,
        types.Integer) for bhlt__pqdak in arr_list.types) and any(
        isinstance(bhlt__pqdak, types.Array) and isinstance(bhlt__pqdak.
        dtype, types.Float) for bhlt__pqdak in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            aqfny__mhy = []
            for A in arr_list:
                aqfny__mhy.append(A._data)
            qikgu__khq = bodo.libs.array_kernels.concat(aqfny__mhy)
            lmo__gykju = bodo.libs.map_arr_ext.init_map_arr(qikgu__khq)
            return lmo__gykju
        return impl_map_arr_list
    for fme__nxx in arr_list:
        if not isinstance(fme__nxx, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(bhlt__pqdak.astype(np.float64) for bhlt__pqdak in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    pfrh__yjp = len(arr_tup.types)
    owaat__voq = 'def f(arr_tup):\n'
    owaat__voq += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(pfrh__yjp
        )), ',' if pfrh__yjp == 1 else '')
    uov__ktfi = {}
    exec(owaat__voq, {'np': np}, uov__ktfi)
    fzbs__edi = uov__ktfi['f']
    return fzbs__edi


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    pfrh__yjp = len(arr_tup.types)
    smifb__vtahp = find_common_np_dtype(arr_tup.types)
    jwoxh__snl = None
    lpnh__iegd = ''
    if isinstance(smifb__vtahp, types.Integer):
        jwoxh__snl = bodo.libs.int_arr_ext.IntDtype(smifb__vtahp)
        lpnh__iegd = '.astype(out_dtype, False)'
    owaat__voq = 'def f(arr_tup):\n'
    owaat__voq += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, lpnh__iegd) for i in range(pfrh__yjp)), ',' if pfrh__yjp ==
        1 else '')
    uov__ktfi = {}
    exec(owaat__voq, {'bodo': bodo, 'out_dtype': jwoxh__snl}, uov__ktfi)
    zqt__oyo = uov__ktfi['f']
    return zqt__oyo


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, ovd__ofzol = build_set_seen_na(A)
        return len(s) + int(not dropna and ovd__ofzol)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        eicz__rsjwr = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        ydnt__mkvn = len(eicz__rsjwr)
        return bodo.libs.distributed_api.dist_reduce(ydnt__mkvn, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([crsyh__dpr for crsyh__dpr in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        egtb__oke = np.finfo(A.dtype(1).dtype).max
    else:
        egtb__oke = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        sixi__sztht = np.empty(n, A.dtype)
        fds__ntn = egtb__oke
        for i in range(n):
            fds__ntn = min(fds__ntn, A[i])
            sixi__sztht[i] = fds__ntn
        return sixi__sztht
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        egtb__oke = np.finfo(A.dtype(1).dtype).min
    else:
        egtb__oke = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        sixi__sztht = np.empty(n, A.dtype)
        fds__ntn = egtb__oke
        for i in range(n):
            fds__ntn = max(fds__ntn, A[i])
            sixi__sztht[i] = fds__ntn
        return sixi__sztht
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        uwpm__vws = arr_info_list_to_table([array_to_info(A)])
        xtqqn__qcoui = 1
        jaizo__sfcvw = 0
        aumk__cyruc = drop_duplicates_table(uwpm__vws, parallel,
            xtqqn__qcoui, jaizo__sfcvw, dropna, True)
        sixi__sztht = info_to_array(info_from_table(aumk__cyruc, 0), A)
        delete_table(uwpm__vws)
        delete_table(aumk__cyruc)
        return sixi__sztht
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    fxqx__ipat = bodo.utils.typing.to_nullable_type(arr.dtype)
    zqpr__zrjqj = index_arr
    xpq__ecab = zqpr__zrjqj.dtype

    def impl(arr, index_arr):
        n = len(arr)
        yhcbf__sbfwx = init_nested_counts(fxqx__ipat)
        yujrj__ofhk = init_nested_counts(xpq__ecab)
        for i in range(n):
            kaj__bljmv = index_arr[i]
            if isna(arr, i):
                yhcbf__sbfwx = (yhcbf__sbfwx[0] + 1,) + yhcbf__sbfwx[1:]
                yujrj__ofhk = add_nested_counts(yujrj__ofhk, kaj__bljmv)
                continue
            tcabu__ehre = arr[i]
            if len(tcabu__ehre) == 0:
                yhcbf__sbfwx = (yhcbf__sbfwx[0] + 1,) + yhcbf__sbfwx[1:]
                yujrj__ofhk = add_nested_counts(yujrj__ofhk, kaj__bljmv)
                continue
            yhcbf__sbfwx = add_nested_counts(yhcbf__sbfwx, tcabu__ehre)
            for dnh__hsc in range(len(tcabu__ehre)):
                yujrj__ofhk = add_nested_counts(yujrj__ofhk, kaj__bljmv)
        sixi__sztht = bodo.utils.utils.alloc_type(yhcbf__sbfwx[0],
            fxqx__ipat, yhcbf__sbfwx[1:])
        bdyl__bwwo = bodo.utils.utils.alloc_type(yhcbf__sbfwx[0],
            zqpr__zrjqj, yujrj__ofhk)
        leqzr__xjucl = 0
        for i in range(n):
            if isna(arr, i):
                setna(sixi__sztht, leqzr__xjucl)
                bdyl__bwwo[leqzr__xjucl] = index_arr[i]
                leqzr__xjucl += 1
                continue
            tcabu__ehre = arr[i]
            kmp__wisd = len(tcabu__ehre)
            if kmp__wisd == 0:
                setna(sixi__sztht, leqzr__xjucl)
                bdyl__bwwo[leqzr__xjucl] = index_arr[i]
                leqzr__xjucl += 1
                continue
            sixi__sztht[leqzr__xjucl:leqzr__xjucl + kmp__wisd] = tcabu__ehre
            bdyl__bwwo[leqzr__xjucl:leqzr__xjucl + kmp__wisd] = index_arr[i]
            leqzr__xjucl += kmp__wisd
        return sixi__sztht, bdyl__bwwo
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    fxqx__ipat = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        yhcbf__sbfwx = init_nested_counts(fxqx__ipat)
        for i in range(n):
            if isna(arr, i):
                yhcbf__sbfwx = (yhcbf__sbfwx[0] + 1,) + yhcbf__sbfwx[1:]
                bwud__uodmq = 1
            else:
                tcabu__ehre = arr[i]
                sswz__ziy = len(tcabu__ehre)
                if sswz__ziy == 0:
                    yhcbf__sbfwx = (yhcbf__sbfwx[0] + 1,) + yhcbf__sbfwx[1:]
                    bwud__uodmq = 1
                    continue
                else:
                    yhcbf__sbfwx = add_nested_counts(yhcbf__sbfwx, tcabu__ehre)
                    bwud__uodmq = sswz__ziy
            if counts[i] != bwud__uodmq:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        sixi__sztht = bodo.utils.utils.alloc_type(yhcbf__sbfwx[0],
            fxqx__ipat, yhcbf__sbfwx[1:])
        leqzr__xjucl = 0
        for i in range(n):
            if isna(arr, i):
                setna(sixi__sztht, leqzr__xjucl)
                leqzr__xjucl += 1
                continue
            tcabu__ehre = arr[i]
            kmp__wisd = len(tcabu__ehre)
            if kmp__wisd == 0:
                setna(sixi__sztht, leqzr__xjucl)
                leqzr__xjucl += 1
                continue
            sixi__sztht[leqzr__xjucl:leqzr__xjucl + kmp__wisd] = tcabu__ehre
            leqzr__xjucl += kmp__wisd
        return sixi__sztht
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(eqhhs__fenqn) for eqhhs__fenqn in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        mobgj__nbum = 'np.empty(n, np.int64)'
        pxa__nhien = 'out_arr[i] = 1'
        tmk__kau = 'max(len(arr[i]), 1)'
    else:
        mobgj__nbum = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        pxa__nhien = 'bodo.libs.array_kernels.setna(out_arr, i)'
        tmk__kau = 'len(arr[i])'
    owaat__voq = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {mobgj__nbum}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {pxa__nhien}
        else:
            out_arr[i] = {tmk__kau}
    return out_arr
    """
    uov__ktfi = {}
    exec(owaat__voq, {'bodo': bodo, 'numba': numba, 'np': np}, uov__ktfi)
    impl = uov__ktfi['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    zqpr__zrjqj = index_arr
    xpq__ecab = zqpr__zrjqj.dtype

    def impl(arr, pat, n, index_arr):
        wennk__vkq = pat is not None and len(pat) > 1
        if wennk__vkq:
            uxpgz__yoe = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        kxff__rgujq = len(arr)
        shi__szvv = 0
        bjpcn__ecvhe = 0
        yujrj__ofhk = init_nested_counts(xpq__ecab)
        for i in range(kxff__rgujq):
            kaj__bljmv = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                shi__szvv += 1
                yujrj__ofhk = add_nested_counts(yujrj__ofhk, kaj__bljmv)
                continue
            if wennk__vkq:
                sumtk__ywb = uxpgz__yoe.split(arr[i], maxsplit=n)
            else:
                sumtk__ywb = arr[i].split(pat, n)
            shi__szvv += len(sumtk__ywb)
            for s in sumtk__ywb:
                yujrj__ofhk = add_nested_counts(yujrj__ofhk, kaj__bljmv)
                bjpcn__ecvhe += bodo.libs.str_arr_ext.get_utf8_size(s)
        sixi__sztht = bodo.libs.str_arr_ext.pre_alloc_string_array(shi__szvv,
            bjpcn__ecvhe)
        bdyl__bwwo = bodo.utils.utils.alloc_type(shi__szvv, zqpr__zrjqj,
            yujrj__ofhk)
        ybqx__csh = 0
        for sdwm__sesgn in range(kxff__rgujq):
            if isna(arr, sdwm__sesgn):
                sixi__sztht[ybqx__csh] = ''
                bodo.libs.array_kernels.setna(sixi__sztht, ybqx__csh)
                bdyl__bwwo[ybqx__csh] = index_arr[sdwm__sesgn]
                ybqx__csh += 1
                continue
            if wennk__vkq:
                sumtk__ywb = uxpgz__yoe.split(arr[sdwm__sesgn], maxsplit=n)
            else:
                sumtk__ywb = arr[sdwm__sesgn].split(pat, n)
            qqfm__hkqr = len(sumtk__ywb)
            sixi__sztht[ybqx__csh:ybqx__csh + qqfm__hkqr] = sumtk__ywb
            bdyl__bwwo[ybqx__csh:ybqx__csh + qqfm__hkqr] = index_arr[
                sdwm__sesgn]
            ybqx__csh += qqfm__hkqr
        return sixi__sztht, bdyl__bwwo
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
            sixi__sztht = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                sixi__sztht[i] = np.nan
            return sixi__sztht
        return impl_float
    rld__cveio = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        sixi__sztht = bodo.utils.utils.alloc_type(n, rld__cveio, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(sixi__sztht, i)
        return sixi__sztht
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
    vyq__gxe = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            sixi__sztht = bodo.utils.utils.alloc_type(new_len, vyq__gxe)
            bodo.libs.str_arr_ext.str_copy_ptr(sixi__sztht.ctypes, 0, A.
                ctypes, old_size)
            return sixi__sztht
        return impl_char

    def impl(A, old_size, new_len):
        sixi__sztht = bodo.utils.utils.alloc_type(new_len, vyq__gxe, (-1,))
        sixi__sztht[:old_size] = A[:old_size]
        return sixi__sztht
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    xvthp__xpfwd = math.ceil((stop - start) / step)
    return int(max(xvthp__xpfwd, 0))


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
    if any(isinstance(crsyh__dpr, types.Complex) for crsyh__dpr in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            eeumj__uta = (stop - start) / step
            xvthp__xpfwd = math.ceil(eeumj__uta.real)
            gcqxr__aum = math.ceil(eeumj__uta.imag)
            itlq__znz = int(max(min(gcqxr__aum, xvthp__xpfwd), 0))
            arr = np.empty(itlq__znz, dtype)
            for i in numba.parfors.parfor.internal_prange(itlq__znz):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            itlq__znz = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(itlq__znz, dtype)
            for i in numba.parfors.parfor.internal_prange(itlq__znz):
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
        kpghr__nsdre = arr,
        if not inplace:
            kpghr__nsdre = arr.copy(),
        lbear__joa = bodo.libs.str_arr_ext.to_list_if_immutable_arr(
            kpghr__nsdre)
        dsco__kjg = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(lbear__joa, 0, n, dsco__kjg)
        if not ascending:
            bodo.libs.timsort.reverseRange(lbear__joa, 0, n, dsco__kjg)
        bodo.libs.str_arr_ext.cp_str_list_to_array(kpghr__nsdre, lbear__joa)
        return kpghr__nsdre[0]
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
        lmo__gykju = []
        for i in range(n):
            if A[i]:
                lmo__gykju.append(i + offset)
        return np.array(lmo__gykju, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    vyq__gxe = element_type(A)
    if vyq__gxe == types.unicode_type:
        null_value = '""'
    elif vyq__gxe == types.bool_:
        null_value = 'False'
    elif vyq__gxe == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif vyq__gxe == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    ybqx__csh = 'i'
    sdvaj__sbqlv = False
    fgsa__jfy = get_overload_const_str(method)
    if fgsa__jfy in ('ffill', 'pad'):
        xozfd__caynk = 'n'
        send_right = True
    elif fgsa__jfy in ('backfill', 'bfill'):
        xozfd__caynk = 'n-1, -1, -1'
        send_right = False
        if vyq__gxe == types.unicode_type:
            ybqx__csh = '(n - 1) - i'
            sdvaj__sbqlv = True
    owaat__voq = 'def impl(A, method, parallel=False):\n'
    owaat__voq += '  A = decode_if_dict_array(A)\n'
    owaat__voq += '  has_last_value = False\n'
    owaat__voq += f'  last_value = {null_value}\n'
    owaat__voq += '  if parallel:\n'
    owaat__voq += '    rank = bodo.libs.distributed_api.get_rank()\n'
    owaat__voq += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    owaat__voq += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    owaat__voq += '  n = len(A)\n'
    owaat__voq += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    owaat__voq += f'  for i in range({xozfd__caynk}):\n'
    owaat__voq += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    owaat__voq += (
        f'      bodo.libs.array_kernels.setna(out_arr, {ybqx__csh})\n')
    owaat__voq += '      continue\n'
    owaat__voq += '    s = A[i]\n'
    owaat__voq += '    if bodo.libs.array_kernels.isna(A, i):\n'
    owaat__voq += '      s = last_value\n'
    owaat__voq += f'    out_arr[{ybqx__csh}] = s\n'
    owaat__voq += '    last_value = s\n'
    owaat__voq += '    has_last_value = True\n'
    if sdvaj__sbqlv:
        owaat__voq += '  return out_arr[::-1]\n'
    else:
        owaat__voq += '  return out_arr\n'
    aayqu__dbxk = {}
    exec(owaat__voq, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, aayqu__dbxk)
    impl = aayqu__dbxk['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        ytif__rfq = 0
        grk__ffo = n_pes - 1
        kmlue__vtlx = np.int32(rank + 1)
        sjcag__pdxl = np.int32(rank - 1)
        ahex__zpk = len(in_arr) - 1
        ifb__eykhv = -1
        mkqo__qwq = -1
    else:
        ytif__rfq = n_pes - 1
        grk__ffo = 0
        kmlue__vtlx = np.int32(rank - 1)
        sjcag__pdxl = np.int32(rank + 1)
        ahex__zpk = 0
        ifb__eykhv = len(in_arr)
        mkqo__qwq = 1
    dnxgg__tho = np.int32(bodo.hiframes.rolling.comm_border_tag)
    olran__gdlfo = np.empty(1, dtype=np.bool_)
    dtaqh__mhiet = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    adrt__irh = np.empty(1, dtype=np.bool_)
    diqp__yrwiv = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    sgqwo__ripvj = False
    mvfgz__mblx = null_value
    for i in range(ahex__zpk, ifb__eykhv, mkqo__qwq):
        if not isna(in_arr, i):
            sgqwo__ripvj = True
            mvfgz__mblx = in_arr[i]
            break
    if rank != ytif__rfq:
        ucgja__rblku = bodo.libs.distributed_api.irecv(olran__gdlfo, 1,
            sjcag__pdxl, dnxgg__tho, True)
        bodo.libs.distributed_api.wait(ucgja__rblku, True)
        acvj__hvivz = bodo.libs.distributed_api.irecv(dtaqh__mhiet, 1,
            sjcag__pdxl, dnxgg__tho, True)
        bodo.libs.distributed_api.wait(acvj__hvivz, True)
        fwk__xgqcz = olran__gdlfo[0]
        dmxuy__znf = dtaqh__mhiet[0]
    else:
        fwk__xgqcz = False
        dmxuy__znf = null_value
    if sgqwo__ripvj:
        adrt__irh[0] = sgqwo__ripvj
        diqp__yrwiv[0] = mvfgz__mblx
    else:
        adrt__irh[0] = fwk__xgqcz
        diqp__yrwiv[0] = dmxuy__znf
    if rank != grk__ffo:
        rebz__puly = bodo.libs.distributed_api.isend(adrt__irh, 1,
            kmlue__vtlx, dnxgg__tho, True)
        bnts__vxbsi = bodo.libs.distributed_api.isend(diqp__yrwiv, 1,
            kmlue__vtlx, dnxgg__tho, True)
    return fwk__xgqcz, dmxuy__znf


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    wgwq__rbiuw = {'axis': axis, 'kind': kind, 'order': order}
    sim__jei = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', wgwq__rbiuw, sim__jei, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    vyq__gxe = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            kxff__rgujq = len(A)
            sixi__sztht = bodo.utils.utils.alloc_type(kxff__rgujq * repeats,
                vyq__gxe, (-1,))
            for i in range(kxff__rgujq):
                ybqx__csh = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for sdwm__sesgn in range(repeats):
                        bodo.libs.array_kernels.setna(sixi__sztht, 
                            ybqx__csh + sdwm__sesgn)
                else:
                    sixi__sztht[ybqx__csh:ybqx__csh + repeats] = A[i]
            return sixi__sztht
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        kxff__rgujq = len(A)
        sixi__sztht = bodo.utils.utils.alloc_type(repeats.sum(), vyq__gxe,
            (-1,))
        ybqx__csh = 0
        for i in range(kxff__rgujq):
            iij__otv = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for sdwm__sesgn in range(iij__otv):
                    bodo.libs.array_kernels.setna(sixi__sztht, ybqx__csh +
                        sdwm__sesgn)
            else:
                sixi__sztht[ybqx__csh:ybqx__csh + iij__otv] = A[i]
            ybqx__csh += iij__otv
        return sixi__sztht
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
        ovtpy__zxjmr = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(ovtpy__zxjmr, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        djnxd__ujecg = bodo.libs.array_kernels.concat([A1, A2])
        pgzs__bxybu = bodo.libs.array_kernels.unique(djnxd__ujecg)
        return pd.Series(pgzs__bxybu).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    wgwq__rbiuw = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    sim__jei = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', wgwq__rbiuw, sim__jei, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        lzj__dnfc = bodo.libs.array_kernels.unique(A1)
        hnog__ontp = bodo.libs.array_kernels.unique(A2)
        djnxd__ujecg = bodo.libs.array_kernels.concat([lzj__dnfc, hnog__ontp])
        nbzq__ceyn = pd.Series(djnxd__ujecg).sort_values().values
        return slice_array_intersect1d(nbzq__ceyn)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    spqwv__qgnh = arr[1:] == arr[:-1]
    return arr[:-1][spqwv__qgnh]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    wgwq__rbiuw = {'assume_unique': assume_unique}
    sim__jei = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', wgwq__rbiuw, sim__jei, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        lzj__dnfc = bodo.libs.array_kernels.unique(A1)
        hnog__ontp = bodo.libs.array_kernels.unique(A2)
        spqwv__qgnh = calculate_mask_setdiff1d(lzj__dnfc, hnog__ontp)
        return pd.Series(lzj__dnfc[spqwv__qgnh]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    spqwv__qgnh = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        spqwv__qgnh &= A1 != A2[i]
    return spqwv__qgnh


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    wgwq__rbiuw = {'retstep': retstep, 'axis': axis}
    sim__jei = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', wgwq__rbiuw, sim__jei, 'numpy')
    tsxw__csq = False
    if is_overload_none(dtype):
        vyq__gxe = np.promote_types(np.promote_types(numba.np.numpy_support
            .as_dtype(start), numba.np.numpy_support.as_dtype(stop)), numba
            .np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            tsxw__csq = True
        vyq__gxe = numba.np.numpy_support.as_dtype(dtype).type
    if tsxw__csq:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            bmsip__lryo = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            sixi__sztht = np.empty(num, vyq__gxe)
            for i in numba.parfors.parfor.internal_prange(num):
                sixi__sztht[i] = vyq__gxe(np.floor(start + i * bmsip__lryo))
            return sixi__sztht
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            bmsip__lryo = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            sixi__sztht = np.empty(num, vyq__gxe)
            for i in numba.parfors.parfor.internal_prange(num):
                sixi__sztht[i] = vyq__gxe(start + i * bmsip__lryo)
            return sixi__sztht
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
        pfrh__yjp = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                pfrh__yjp += A[i] == val
        return pfrh__yjp > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    wgwq__rbiuw = {'axis': axis, 'out': out, 'keepdims': keepdims}
    sim__jei = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', wgwq__rbiuw, sim__jei, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        pfrh__yjp = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                pfrh__yjp += int(bool(A[i]))
        return pfrh__yjp > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    wgwq__rbiuw = {'axis': axis, 'out': out, 'keepdims': keepdims}
    sim__jei = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', wgwq__rbiuw, sim__jei, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        pfrh__yjp = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                pfrh__yjp += int(bool(A[i]))
        return pfrh__yjp == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    wgwq__rbiuw = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    sim__jei = {'out': None, 'where': True, 'casting': 'same_kind', 'order':
        'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', wgwq__rbiuw, sim__jei, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        kiggv__hnx = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            sixi__sztht = np.empty(n, kiggv__hnx)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(sixi__sztht, i)
                    continue
                sixi__sztht[i] = np_cbrt_scalar(A[i], kiggv__hnx)
            return sixi__sztht
        return impl_arr
    kiggv__hnx = np.promote_types(numba.np.numpy_support.as_dtype(A), numba
        .np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, kiggv__hnx)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    qdztd__unqak = x < 0
    if qdztd__unqak:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if qdztd__unqak:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    jaf__onm = isinstance(tup, (types.BaseTuple, types.List))
    gasp__hyhk = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for fme__nxx in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(fme__nxx,
                'numpy.hstack()')
            jaf__onm = jaf__onm and bodo.utils.utils.is_array_typ(fme__nxx,
                False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        jaf__onm = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif gasp__hyhk:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        lamya__wpjk = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for fme__nxx in lamya__wpjk.types:
            gasp__hyhk = gasp__hyhk and bodo.utils.utils.is_array_typ(fme__nxx,
                False)
    if not (jaf__onm or gasp__hyhk):
        return
    if gasp__hyhk:

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
    wgwq__rbiuw = {'check_valid': check_valid, 'tol': tol}
    sim__jei = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', wgwq__rbiuw,
        sim__jei, 'numpy')
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
        pgb__evu = mean.shape[0]
        acdxv__drvmn = size, pgb__evu
        lzqor__elj = np.random.standard_normal(acdxv__drvmn)
        cov = cov.astype(np.float64)
        pafur__gbh, s, xssab__vbkt = np.linalg.svd(cov)
        res = np.dot(lzqor__elj, np.sqrt(s).reshape(pgb__evu, 1) * xssab__vbkt)
        acri__rekbq = res + mean
        return acri__rekbq
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
            vvhnn__tgev = bodo.hiframes.series_kernels._get_type_max_value(arr)
            ubuw__nenle = typing.builtins.IndexValue(-1, vvhnn__tgev)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xdb__bncb = typing.builtins.IndexValue(i, arr[i])
                ubuw__nenle = min(ubuw__nenle, xdb__bncb)
            return ubuw__nenle.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        fyask__hao = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            gkhj__ucea = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            vvhnn__tgev = fyask__hao(len(arr.dtype.categories) + 1)
            ubuw__nenle = typing.builtins.IndexValue(-1, vvhnn__tgev)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xdb__bncb = typing.builtins.IndexValue(i, gkhj__ucea[i])
                ubuw__nenle = min(ubuw__nenle, xdb__bncb)
            return ubuw__nenle.index
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
            vvhnn__tgev = bodo.hiframes.series_kernels._get_type_min_value(arr)
            ubuw__nenle = typing.builtins.IndexValue(-1, vvhnn__tgev)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xdb__bncb = typing.builtins.IndexValue(i, arr[i])
                ubuw__nenle = max(ubuw__nenle, xdb__bncb)
            return ubuw__nenle.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        fyask__hao = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            gkhj__ucea = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            vvhnn__tgev = fyask__hao(-1)
            ubuw__nenle = typing.builtins.IndexValue(-1, vvhnn__tgev)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xdb__bncb = typing.builtins.IndexValue(i, gkhj__ucea[i])
                ubuw__nenle = max(ubuw__nenle, xdb__bncb)
            return ubuw__nenle.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
