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
        benn__xrobe = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = benn__xrobe
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        benn__xrobe = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = benn__xrobe
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
            jew__anx = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            jew__anx[ind + 1] = jew__anx[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            jew__anx = bodo.libs.array_item_arr_ext.get_offsets(arr)
            jew__anx[ind + 1] = jew__anx[ind]
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
    xlkcj__oycf = arr_tup.count
    gqwa__lhka = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(xlkcj__oycf):
        gqwa__lhka += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    gqwa__lhka += '  return\n'
    muxv__ogdp = {}
    exec(gqwa__lhka, {'setna': setna}, muxv__ogdp)
    impl = muxv__ogdp['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        koujn__esq = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(koujn__esq.start, koujn__esq.stop, koujn__esq.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        pzosv__fbjmr = 'n'
        phf__vzubh = 'n_pes'
        thwr__xbf = 'min_op'
    else:
        pzosv__fbjmr = 'n-1, -1, -1'
        phf__vzubh = '-1'
        thwr__xbf = 'max_op'
    gqwa__lhka = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {phf__vzubh}
    for i in range({pzosv__fbjmr}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {thwr__xbf}))
        if possible_valid_rank != {phf__vzubh}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    muxv__ogdp = {}
    exec(gqwa__lhka, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, muxv__ogdp)
    impl = muxv__ogdp['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    kpagh__dpg = array_to_info(arr)
    _median_series_computation(res, kpagh__dpg, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(kpagh__dpg)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    kpagh__dpg = array_to_info(arr)
    _autocorr_series_computation(res, kpagh__dpg, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(kpagh__dpg)


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
    kpagh__dpg = array_to_info(arr)
    _compute_series_monotonicity(res, kpagh__dpg, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(kpagh__dpg)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    dshq__jolas = res[0] > 0.5
    return dshq__jolas


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        cxwjd__lfnsm = '-'
        yzlg__tykxe = 'index_arr[0] > threshhold_date'
        pzosv__fbjmr = '1, n+1'
        xlvwm__univ = 'index_arr[-i] <= threshhold_date'
        tky__rjhm = 'i - 1'
    else:
        cxwjd__lfnsm = '+'
        yzlg__tykxe = 'index_arr[-1] < threshhold_date'
        pzosv__fbjmr = 'n'
        xlvwm__univ = 'index_arr[i] >= threshhold_date'
        tky__rjhm = 'i'
    gqwa__lhka = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        gqwa__lhka += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        gqwa__lhka += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            gqwa__lhka += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            gqwa__lhka += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            gqwa__lhka += '    else:\n'
            gqwa__lhka += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            gqwa__lhka += (
                f'    threshhold_date = initial_date {cxwjd__lfnsm} date_offset\n'
                )
    else:
        gqwa__lhka += (
            f'  threshhold_date = initial_date {cxwjd__lfnsm} offset\n')
    gqwa__lhka += '  local_valid = 0\n'
    gqwa__lhka += f'  n = len(index_arr)\n'
    gqwa__lhka += f'  if n:\n'
    gqwa__lhka += f'    if {yzlg__tykxe}:\n'
    gqwa__lhka += '      loc_valid = n\n'
    gqwa__lhka += '    else:\n'
    gqwa__lhka += f'      for i in range({pzosv__fbjmr}):\n'
    gqwa__lhka += f'        if {xlvwm__univ}:\n'
    gqwa__lhka += f'          loc_valid = {tky__rjhm}\n'
    gqwa__lhka += '          break\n'
    gqwa__lhka += '  if is_parallel:\n'
    gqwa__lhka += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    gqwa__lhka += '    return total_valid\n'
    gqwa__lhka += '  else:\n'
    gqwa__lhka += '    return loc_valid\n'
    muxv__ogdp = {}
    exec(gqwa__lhka, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, muxv__ogdp)
    return muxv__ogdp['impl']


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
    zyci__zcf = numba_to_c_type(sig.args[0].dtype)
    mwvl__ehjz = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), zyci__zcf))
    otewf__vmhdn = args[0]
    eia__sugd = sig.args[0]
    if isinstance(eia__sugd, (IntegerArrayType, BooleanArrayType)):
        otewf__vmhdn = cgutils.create_struct_proxy(eia__sugd)(context,
            builder, otewf__vmhdn).data
        eia__sugd = types.Array(eia__sugd.dtype, 1, 'C')
    assert eia__sugd.ndim == 1
    arr = make_array(eia__sugd)(context, builder, otewf__vmhdn)
    rrtya__sfufv = builder.extract_value(arr.shape, 0)
    xefid__mpr = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        rrtya__sfufv, args[1], builder.load(mwvl__ehjz)]
    jnbgs__ekx = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    myb__zwm = lir.FunctionType(lir.DoubleType(), jnbgs__ekx)
    pdc__ddwnr = cgutils.get_or_insert_function(builder.module, myb__zwm,
        name='quantile_sequential')
    mqrxa__jmgw = builder.call(pdc__ddwnr, xefid__mpr)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return mqrxa__jmgw


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    zyci__zcf = numba_to_c_type(sig.args[0].dtype)
    mwvl__ehjz = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), zyci__zcf))
    otewf__vmhdn = args[0]
    eia__sugd = sig.args[0]
    if isinstance(eia__sugd, (IntegerArrayType, BooleanArrayType)):
        otewf__vmhdn = cgutils.create_struct_proxy(eia__sugd)(context,
            builder, otewf__vmhdn).data
        eia__sugd = types.Array(eia__sugd.dtype, 1, 'C')
    assert eia__sugd.ndim == 1
    arr = make_array(eia__sugd)(context, builder, otewf__vmhdn)
    rrtya__sfufv = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        gphq__glxc = args[2]
    else:
        gphq__glxc = rrtya__sfufv
    xefid__mpr = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        rrtya__sfufv, gphq__glxc, args[1], builder.load(mwvl__ehjz)]
    jnbgs__ekx = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType
        (64), lir.DoubleType(), lir.IntType(32)]
    myb__zwm = lir.FunctionType(lir.DoubleType(), jnbgs__ekx)
    pdc__ddwnr = cgutils.get_or_insert_function(builder.module, myb__zwm,
        name='quantile_parallel')
    mqrxa__jmgw = builder.call(pdc__ddwnr, xefid__mpr)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return mqrxa__jmgw


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    zdn__eeuv = start
    yimeq__wkkch = 2 * start + 1
    pcvgg__ggjyq = 2 * start + 2
    if yimeq__wkkch < n and not cmp_f(arr[yimeq__wkkch], arr[zdn__eeuv]):
        zdn__eeuv = yimeq__wkkch
    if pcvgg__ggjyq < n and not cmp_f(arr[pcvgg__ggjyq], arr[zdn__eeuv]):
        zdn__eeuv = pcvgg__ggjyq
    if zdn__eeuv != start:
        arr[start], arr[zdn__eeuv] = arr[zdn__eeuv], arr[start]
        ind_arr[start], ind_arr[zdn__eeuv] = ind_arr[zdn__eeuv], ind_arr[start]
        min_heapify(arr, ind_arr, n, zdn__eeuv, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        ihf__rja = np.empty(k, A.dtype)
        kbl__psoqf = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                ihf__rja[ind] = A[i]
                kbl__psoqf[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            ihf__rja = ihf__rja[:ind]
            kbl__psoqf = kbl__psoqf[:ind]
        return ihf__rja, kbl__psoqf, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        cvf__ido = np.sort(A)
        vrv__zfz = index_arr[np.argsort(A)]
        hrkg__ayj = pd.Series(cvf__ido).notna().values
        cvf__ido = cvf__ido[hrkg__ayj]
        vrv__zfz = vrv__zfz[hrkg__ayj]
        if is_largest:
            cvf__ido = cvf__ido[::-1]
            vrv__zfz = vrv__zfz[::-1]
        return np.ascontiguousarray(cvf__ido), np.ascontiguousarray(vrv__zfz)
    ihf__rja, kbl__psoqf, start = select_k_nonan(A, index_arr, m, k)
    kbl__psoqf = kbl__psoqf[ihf__rja.argsort()]
    ihf__rja.sort()
    if not is_largest:
        ihf__rja = np.ascontiguousarray(ihf__rja[::-1])
        kbl__psoqf = np.ascontiguousarray(kbl__psoqf[::-1])
    for i in range(start, m):
        if cmp_f(A[i], ihf__rja[0]):
            ihf__rja[0] = A[i]
            kbl__psoqf[0] = index_arr[i]
            min_heapify(ihf__rja, kbl__psoqf, k, 0, cmp_f)
    kbl__psoqf = kbl__psoqf[ihf__rja.argsort()]
    ihf__rja.sort()
    if is_largest:
        ihf__rja = ihf__rja[::-1]
        kbl__psoqf = kbl__psoqf[::-1]
    return np.ascontiguousarray(ihf__rja), np.ascontiguousarray(kbl__psoqf)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    zhsim__hkan = bodo.libs.distributed_api.get_rank()
    hci__xqwre, rwc__dmv = nlargest(A, I, k, is_largest, cmp_f)
    mugn__krqqo = bodo.libs.distributed_api.gatherv(hci__xqwre)
    nbohg__zsa = bodo.libs.distributed_api.gatherv(rwc__dmv)
    if zhsim__hkan == MPI_ROOT:
        res, wjhh__wglyg = nlargest(mugn__krqqo, nbohg__zsa, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        wjhh__wglyg = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(wjhh__wglyg)
    return res, wjhh__wglyg


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    uzhxp__lym, ogxye__jkj = mat.shape
    kovs__wprs = np.empty((ogxye__jkj, ogxye__jkj), dtype=np.float64)
    for kdhu__qunr in range(ogxye__jkj):
        for qpjr__ndsn in range(kdhu__qunr + 1):
            bps__xjaq = 0
            uqsit__qut = wysy__ztkdu = rjy__krb = oqv__abd = 0.0
            for i in range(uzhxp__lym):
                if np.isfinite(mat[i, kdhu__qunr]) and np.isfinite(mat[i,
                    qpjr__ndsn]):
                    nmm__prnf = mat[i, kdhu__qunr]
                    lbkq__tkt = mat[i, qpjr__ndsn]
                    bps__xjaq += 1
                    rjy__krb += nmm__prnf
                    oqv__abd += lbkq__tkt
            if parallel:
                bps__xjaq = bodo.libs.distributed_api.dist_reduce(bps__xjaq,
                    sum_op)
                rjy__krb = bodo.libs.distributed_api.dist_reduce(rjy__krb,
                    sum_op)
                oqv__abd = bodo.libs.distributed_api.dist_reduce(oqv__abd,
                    sum_op)
            if bps__xjaq < minpv:
                kovs__wprs[kdhu__qunr, qpjr__ndsn] = kovs__wprs[qpjr__ndsn,
                    kdhu__qunr] = np.nan
            else:
                gyz__utbo = rjy__krb / bps__xjaq
                eakwr__blg = oqv__abd / bps__xjaq
                rjy__krb = 0.0
                for i in range(uzhxp__lym):
                    if np.isfinite(mat[i, kdhu__qunr]) and np.isfinite(mat[
                        i, qpjr__ndsn]):
                        nmm__prnf = mat[i, kdhu__qunr] - gyz__utbo
                        lbkq__tkt = mat[i, qpjr__ndsn] - eakwr__blg
                        rjy__krb += nmm__prnf * lbkq__tkt
                        uqsit__qut += nmm__prnf * nmm__prnf
                        wysy__ztkdu += lbkq__tkt * lbkq__tkt
                if parallel:
                    rjy__krb = bodo.libs.distributed_api.dist_reduce(rjy__krb,
                        sum_op)
                    uqsit__qut = bodo.libs.distributed_api.dist_reduce(
                        uqsit__qut, sum_op)
                    wysy__ztkdu = bodo.libs.distributed_api.dist_reduce(
                        wysy__ztkdu, sum_op)
                pixmy__zeqto = bps__xjaq - 1.0 if cov else sqrt(uqsit__qut *
                    wysy__ztkdu)
                if pixmy__zeqto != 0.0:
                    kovs__wprs[kdhu__qunr, qpjr__ndsn] = kovs__wprs[
                        qpjr__ndsn, kdhu__qunr] = rjy__krb / pixmy__zeqto
                else:
                    kovs__wprs[kdhu__qunr, qpjr__ndsn] = kovs__wprs[
                        qpjr__ndsn, kdhu__qunr] = np.nan
    return kovs__wprs


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    rzz__hqnb = n != 1
    gqwa__lhka = 'def impl(data, parallel=False):\n'
    gqwa__lhka += '  if parallel:\n'
    zof__nneks = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    gqwa__lhka += f'    cpp_table = arr_info_list_to_table([{zof__nneks}])\n'
    gqwa__lhka += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    nvmtv__zyyth = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    gqwa__lhka += f'    data = ({nvmtv__zyyth},)\n'
    gqwa__lhka += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    gqwa__lhka += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    gqwa__lhka += '    bodo.libs.array.delete_table(cpp_table)\n'
    gqwa__lhka += '  n = len(data[0])\n'
    gqwa__lhka += '  out = np.empty(n, np.bool_)\n'
    gqwa__lhka += '  uniqs = dict()\n'
    if rzz__hqnb:
        gqwa__lhka += '  for i in range(n):\n'
        bbefq__sdd = ', '.join(f'data[{i}][i]' for i in range(n))
        lgugk__satjk = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        gqwa__lhka += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({bbefq__sdd},), ({lgugk__satjk},))
"""
        gqwa__lhka += '    if val in uniqs:\n'
        gqwa__lhka += '      out[i] = True\n'
        gqwa__lhka += '    else:\n'
        gqwa__lhka += '      out[i] = False\n'
        gqwa__lhka += '      uniqs[val] = 0\n'
    else:
        gqwa__lhka += '  data = data[0]\n'
        gqwa__lhka += '  hasna = False\n'
        gqwa__lhka += '  for i in range(n):\n'
        gqwa__lhka += '    if bodo.libs.array_kernels.isna(data, i):\n'
        gqwa__lhka += '      out[i] = hasna\n'
        gqwa__lhka += '      hasna = True\n'
        gqwa__lhka += '    else:\n'
        gqwa__lhka += '      val = data[i]\n'
        gqwa__lhka += '      if val in uniqs:\n'
        gqwa__lhka += '        out[i] = True\n'
        gqwa__lhka += '      else:\n'
        gqwa__lhka += '        out[i] = False\n'
        gqwa__lhka += '        uniqs[val] = 0\n'
    gqwa__lhka += '  if parallel:\n'
    gqwa__lhka += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    gqwa__lhka += '  return out\n'
    muxv__ogdp = {}
    exec(gqwa__lhka, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        muxv__ogdp)
    impl = muxv__ogdp['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    xlkcj__oycf = len(data)
    gqwa__lhka = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    gqwa__lhka += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        xlkcj__oycf)))
    gqwa__lhka += '  table_total = arr_info_list_to_table(info_list_total)\n'
    gqwa__lhka += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(xlkcj__oycf))
    for zixu__khh in range(xlkcj__oycf):
        gqwa__lhka += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(zixu__khh, zixu__khh, zixu__khh))
    gqwa__lhka += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(xlkcj__oycf))
    gqwa__lhka += '  delete_table(out_table)\n'
    gqwa__lhka += '  delete_table(table_total)\n'
    gqwa__lhka += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(xlkcj__oycf)))
    muxv__ogdp = {}
    exec(gqwa__lhka, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, muxv__ogdp)
    impl = muxv__ogdp['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    xlkcj__oycf = len(data)
    gqwa__lhka = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    gqwa__lhka += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        xlkcj__oycf)))
    gqwa__lhka += '  table_total = arr_info_list_to_table(info_list_total)\n'
    gqwa__lhka += '  keep_i = 0\n'
    gqwa__lhka += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for zixu__khh in range(xlkcj__oycf):
        gqwa__lhka += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(zixu__khh, zixu__khh, zixu__khh))
    gqwa__lhka += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(xlkcj__oycf))
    gqwa__lhka += '  delete_table(out_table)\n'
    gqwa__lhka += '  delete_table(table_total)\n'
    gqwa__lhka += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(xlkcj__oycf)))
    muxv__ogdp = {}
    exec(gqwa__lhka, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, muxv__ogdp)
    impl = muxv__ogdp['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        led__cvsg = [array_to_info(data_arr)]
        wju__pjqy = arr_info_list_to_table(led__cvsg)
        amrw__vdi = 0
        qjmab__lpbz = drop_duplicates_table(wju__pjqy, parallel, 1,
            amrw__vdi, False, True)
        gfe__xokhe = info_to_array(info_from_table(qjmab__lpbz, 0), data_arr)
        delete_table(qjmab__lpbz)
        delete_table(wju__pjqy)
        return gfe__xokhe
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    jsm__lrfjv = len(data.types)
    hwfpg__dhvh = [('out' + str(i)) for i in range(jsm__lrfjv)]
    ccth__kxm = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    rima__vdsz = ['isna(data[{}], i)'.format(i) for i in ccth__kxm]
    aqmbr__cdrb = 'not ({})'.format(' or '.join(rima__vdsz))
    if not is_overload_none(thresh):
        aqmbr__cdrb = '(({}) <= ({}) - thresh)'.format(' + '.join(
            rima__vdsz), jsm__lrfjv - 1)
    elif how == 'all':
        aqmbr__cdrb = 'not ({})'.format(' and '.join(rima__vdsz))
    gqwa__lhka = 'def _dropna_imp(data, how, thresh, subset):\n'
    gqwa__lhka += '  old_len = len(data[0])\n'
    gqwa__lhka += '  new_len = 0\n'
    gqwa__lhka += '  for i in range(old_len):\n'
    gqwa__lhka += '    if {}:\n'.format(aqmbr__cdrb)
    gqwa__lhka += '      new_len += 1\n'
    for i, out in enumerate(hwfpg__dhvh):
        if isinstance(data[i], bodo.CategoricalArrayType):
            gqwa__lhka += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            gqwa__lhka += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    gqwa__lhka += '  curr_ind = 0\n'
    gqwa__lhka += '  for i in range(old_len):\n'
    gqwa__lhka += '    if {}:\n'.format(aqmbr__cdrb)
    for i in range(jsm__lrfjv):
        gqwa__lhka += '      if isna(data[{}], i):\n'.format(i)
        gqwa__lhka += '        setna({}, curr_ind)\n'.format(hwfpg__dhvh[i])
        gqwa__lhka += '      else:\n'
        gqwa__lhka += '        {}[curr_ind] = data[{}][i]\n'.format(hwfpg__dhvh
            [i], i)
    gqwa__lhka += '      curr_ind += 1\n'
    gqwa__lhka += '  return {}\n'.format(', '.join(hwfpg__dhvh))
    muxv__ogdp = {}
    vgf__sdb = {'t{}'.format(i): bzxy__feql for i, bzxy__feql in enumerate(
        data.types)}
    vgf__sdb.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(gqwa__lhka, vgf__sdb, muxv__ogdp)
    lmu__glvfa = muxv__ogdp['_dropna_imp']
    return lmu__glvfa


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        eia__sugd = arr.dtype
        ogzgt__zgvk = eia__sugd.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            qts__ostrr = init_nested_counts(ogzgt__zgvk)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                qts__ostrr = add_nested_counts(qts__ostrr, val[ind])
            gfe__xokhe = bodo.utils.utils.alloc_type(n, eia__sugd, qts__ostrr)
            for uvc__alsa in range(n):
                if bodo.libs.array_kernels.isna(arr, uvc__alsa):
                    setna(gfe__xokhe, uvc__alsa)
                    continue
                val = arr[uvc__alsa]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(gfe__xokhe, uvc__alsa)
                    continue
                gfe__xokhe[uvc__alsa] = val[ind]
            return gfe__xokhe
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    dhiz__gipy = _to_readonly(arr_types.types[0])
    return all(isinstance(bzxy__feql, CategoricalArrayType) and 
        _to_readonly(bzxy__feql) == dhiz__gipy for bzxy__feql in arr_types.
        types)


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
        awlls__ozpq = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            rzrvx__ymc = 0
            yyn__nzc = []
            for A in arr_list:
                rqw__ruyy = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                yyn__nzc.append(bodo.libs.array_item_arr_ext.get_data(A))
                rzrvx__ymc += rqw__ruyy
            izb__juqmw = np.empty(rzrvx__ymc + 1, offset_type)
            qhnya__tcr = bodo.libs.array_kernels.concat(yyn__nzc)
            vgvke__gwvjw = np.empty(rzrvx__ymc + 7 >> 3, np.uint8)
            fpjjf__gkrdr = 0
            xep__auy = 0
            for A in arr_list:
                ddfx__pola = bodo.libs.array_item_arr_ext.get_offsets(A)
                xha__oxu = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                rqw__ruyy = len(A)
                hmdq__ctr = ddfx__pola[rqw__ruyy]
                for i in range(rqw__ruyy):
                    izb__juqmw[i + fpjjf__gkrdr] = ddfx__pola[i] + xep__auy
                    knx__paw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        xha__oxu, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vgvke__gwvjw, i +
                        fpjjf__gkrdr, knx__paw)
                fpjjf__gkrdr += rqw__ruyy
                xep__auy += hmdq__ctr
            izb__juqmw[fpjjf__gkrdr] = xep__auy
            gfe__xokhe = bodo.libs.array_item_arr_ext.init_array_item_array(
                rzrvx__ymc, qhnya__tcr, izb__juqmw, vgvke__gwvjw)
            return gfe__xokhe
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        uym__xtlgb = arr_list.dtype.names
        gqwa__lhka = 'def struct_array_concat_impl(arr_list):\n'
        gqwa__lhka += f'    n_all = 0\n'
        for i in range(len(uym__xtlgb)):
            gqwa__lhka += f'    concat_list{i} = []\n'
        gqwa__lhka += '    for A in arr_list:\n'
        gqwa__lhka += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(uym__xtlgb)):
            gqwa__lhka += f'        concat_list{i}.append(data_tuple[{i}])\n'
        gqwa__lhka += '        n_all += len(A)\n'
        gqwa__lhka += '    n_bytes = (n_all + 7) >> 3\n'
        gqwa__lhka += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        gqwa__lhka += '    curr_bit = 0\n'
        gqwa__lhka += '    for A in arr_list:\n'
        gqwa__lhka += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        gqwa__lhka += '        for j in range(len(A)):\n'
        gqwa__lhka += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        gqwa__lhka += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        gqwa__lhka += '            curr_bit += 1\n'
        gqwa__lhka += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        biar__dkiif = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(uym__xtlgb))])
        gqwa__lhka += f'        ({biar__dkiif},),\n'
        gqwa__lhka += '        new_mask,\n'
        gqwa__lhka += f'        {uym__xtlgb},\n'
        gqwa__lhka += '    )\n'
        muxv__ogdp = {}
        exec(gqwa__lhka, {'bodo': bodo, 'np': np}, muxv__ogdp)
        return muxv__ogdp['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            ehy__qohc = 0
            for A in arr_list:
                ehy__qohc += len(A)
            xhq__tua = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(ehy__qohc))
            xilw__scz = 0
            for A in arr_list:
                for i in range(len(A)):
                    xhq__tua._data[i + xilw__scz] = A._data[i]
                    knx__paw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(xhq__tua.
                        _null_bitmap, i + xilw__scz, knx__paw)
                xilw__scz += len(A)
            return xhq__tua
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            ehy__qohc = 0
            for A in arr_list:
                ehy__qohc += len(A)
            xhq__tua = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(ehy__qohc))
            xilw__scz = 0
            for A in arr_list:
                for i in range(len(A)):
                    xhq__tua._days_data[i + xilw__scz] = A._days_data[i]
                    xhq__tua._seconds_data[i + xilw__scz] = A._seconds_data[i]
                    xhq__tua._microseconds_data[i + xilw__scz
                        ] = A._microseconds_data[i]
                    knx__paw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(xhq__tua.
                        _null_bitmap, i + xilw__scz, knx__paw)
                xilw__scz += len(A)
            return xhq__tua
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        eqaie__gvb = arr_list.dtype.precision
        nxjst__drs = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            ehy__qohc = 0
            for A in arr_list:
                ehy__qohc += len(A)
            xhq__tua = bodo.libs.decimal_arr_ext.alloc_decimal_array(ehy__qohc,
                eqaie__gvb, nxjst__drs)
            xilw__scz = 0
            for A in arr_list:
                for i in range(len(A)):
                    xhq__tua._data[i + xilw__scz] = A._data[i]
                    knx__paw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(xhq__tua.
                        _null_bitmap, i + xilw__scz, knx__paw)
                xilw__scz += len(A)
            return xhq__tua
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        bzxy__feql) for bzxy__feql in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            bpe__qvg = arr_list.types[0]
        else:
            bpe__qvg = arr_list.dtype
        bpe__qvg = to_str_arr_if_dict_array(bpe__qvg)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            gkku__sxvyd = 0
            mgi__cvarv = 0
            for A in arr_list:
                arr = A
                gkku__sxvyd += len(arr)
                mgi__cvarv += bodo.libs.str_arr_ext.num_total_chars(arr)
            gfe__xokhe = bodo.utils.utils.alloc_type(gkku__sxvyd, bpe__qvg,
                (mgi__cvarv,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(gfe__xokhe, -1)
            dbhr__qcza = 0
            wbt__mrv = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(gfe__xokhe,
                    arr, dbhr__qcza, wbt__mrv)
                dbhr__qcza += len(arr)
                wbt__mrv += bodo.libs.str_arr_ext.num_total_chars(arr)
            return gfe__xokhe
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(bzxy__feql.dtype, types.Integer) for
        bzxy__feql in arr_list.types) and any(isinstance(bzxy__feql,
        IntegerArrayType) for bzxy__feql in arr_list.types):

        def impl_int_arr_list(arr_list):
            inpgg__eari = convert_to_nullable_tup(arr_list)
            magt__tdbj = []
            xkju__tyqoq = 0
            for A in inpgg__eari:
                magt__tdbj.append(A._data)
                xkju__tyqoq += len(A)
            qhnya__tcr = bodo.libs.array_kernels.concat(magt__tdbj)
            siu__szzqz = xkju__tyqoq + 7 >> 3
            hfdwk__yced = np.empty(siu__szzqz, np.uint8)
            gvihq__jdeh = 0
            for A in inpgg__eari:
                lbvk__dot = A._null_bitmap
                for uvc__alsa in range(len(A)):
                    knx__paw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        lbvk__dot, uvc__alsa)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hfdwk__yced,
                        gvihq__jdeh, knx__paw)
                    gvihq__jdeh += 1
            return bodo.libs.int_arr_ext.init_integer_array(qhnya__tcr,
                hfdwk__yced)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(bzxy__feql.dtype == types.bool_ for bzxy__feql in
        arr_list.types) and any(bzxy__feql == boolean_array for bzxy__feql in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            inpgg__eari = convert_to_nullable_tup(arr_list)
            magt__tdbj = []
            xkju__tyqoq = 0
            for A in inpgg__eari:
                magt__tdbj.append(A._data)
                xkju__tyqoq += len(A)
            qhnya__tcr = bodo.libs.array_kernels.concat(magt__tdbj)
            siu__szzqz = xkju__tyqoq + 7 >> 3
            hfdwk__yced = np.empty(siu__szzqz, np.uint8)
            gvihq__jdeh = 0
            for A in inpgg__eari:
                lbvk__dot = A._null_bitmap
                for uvc__alsa in range(len(A)):
                    knx__paw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        lbvk__dot, uvc__alsa)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hfdwk__yced,
                        gvihq__jdeh, knx__paw)
                    gvihq__jdeh += 1
            return bodo.libs.bool_arr_ext.init_bool_array(qhnya__tcr,
                hfdwk__yced)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            yitv__gff = []
            for A in arr_list:
                yitv__gff.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                yitv__gff), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        lcs__qecw = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        gqwa__lhka = 'def impl(arr_list):\n'
        gqwa__lhka += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({lcs__qecw},)), arr_list[0].dtype)
"""
        mmi__dpo = {}
        exec(gqwa__lhka, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, mmi__dpo)
        return mmi__dpo['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            xkju__tyqoq = 0
            for A in arr_list:
                xkju__tyqoq += len(A)
            gfe__xokhe = np.empty(xkju__tyqoq, dtype)
            qck__bny = 0
            for A in arr_list:
                n = len(A)
                gfe__xokhe[qck__bny:qck__bny + n] = A
                qck__bny += n
            return gfe__xokhe
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(bzxy__feql,
        (types.Array, IntegerArrayType)) and isinstance(bzxy__feql.dtype,
        types.Integer) for bzxy__feql in arr_list.types) and any(isinstance
        (bzxy__feql, types.Array) and isinstance(bzxy__feql.dtype, types.
        Float) for bzxy__feql in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            sqcip__hvk = []
            for A in arr_list:
                sqcip__hvk.append(A._data)
            nolt__wbapa = bodo.libs.array_kernels.concat(sqcip__hvk)
            kovs__wprs = bodo.libs.map_arr_ext.init_map_arr(nolt__wbapa)
            return kovs__wprs
        return impl_map_arr_list
    for srsmr__fgd in arr_list:
        if not isinstance(srsmr__fgd, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(bzxy__feql.astype(np.float64) for bzxy__feql in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    xlkcj__oycf = len(arr_tup.types)
    gqwa__lhka = 'def f(arr_tup):\n'
    gqwa__lhka += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        xlkcj__oycf)), ',' if xlkcj__oycf == 1 else '')
    muxv__ogdp = {}
    exec(gqwa__lhka, {'np': np}, muxv__ogdp)
    zqqtf__xvy = muxv__ogdp['f']
    return zqqtf__xvy


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    xlkcj__oycf = len(arr_tup.types)
    hylqj__gghnn = find_common_np_dtype(arr_tup.types)
    ogzgt__zgvk = None
    pejho__imro = ''
    if isinstance(hylqj__gghnn, types.Integer):
        ogzgt__zgvk = bodo.libs.int_arr_ext.IntDtype(hylqj__gghnn)
        pejho__imro = '.astype(out_dtype, False)'
    gqwa__lhka = 'def f(arr_tup):\n'
    gqwa__lhka += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, pejho__imro) for i in range(xlkcj__oycf)), ',' if 
        xlkcj__oycf == 1 else '')
    muxv__ogdp = {}
    exec(gqwa__lhka, {'bodo': bodo, 'out_dtype': ogzgt__zgvk}, muxv__ogdp)
    kio__iptmt = muxv__ogdp['f']
    return kio__iptmt


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, wmd__bngd = build_set_seen_na(A)
        return len(s) + int(not dropna and wmd__bngd)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        djfy__aedr = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        trp__bttet = len(djfy__aedr)
        return bodo.libs.distributed_api.dist_reduce(trp__bttet, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([jmhn__xtv for jmhn__xtv in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        nkqhv__hfkcy = np.finfo(A.dtype(1).dtype).max
    else:
        nkqhv__hfkcy = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        gfe__xokhe = np.empty(n, A.dtype)
        mzfpb__baw = nkqhv__hfkcy
        for i in range(n):
            mzfpb__baw = min(mzfpb__baw, A[i])
            gfe__xokhe[i] = mzfpb__baw
        return gfe__xokhe
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        nkqhv__hfkcy = np.finfo(A.dtype(1).dtype).min
    else:
        nkqhv__hfkcy = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        gfe__xokhe = np.empty(n, A.dtype)
        mzfpb__baw = nkqhv__hfkcy
        for i in range(n):
            mzfpb__baw = max(mzfpb__baw, A[i])
            gfe__xokhe[i] = mzfpb__baw
        return gfe__xokhe
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        muir__pik = arr_info_list_to_table([array_to_info(A)])
        uhhl__mhc = 1
        amrw__vdi = 0
        qjmab__lpbz = drop_duplicates_table(muir__pik, parallel, uhhl__mhc,
            amrw__vdi, dropna, True)
        gfe__xokhe = info_to_array(info_from_table(qjmab__lpbz, 0), A)
        delete_table(muir__pik)
        delete_table(qjmab__lpbz)
        return gfe__xokhe
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    awlls__ozpq = bodo.utils.typing.to_nullable_type(arr.dtype)
    rvjb__vnwe = index_arr
    whb__fefkj = rvjb__vnwe.dtype

    def impl(arr, index_arr):
        n = len(arr)
        qts__ostrr = init_nested_counts(awlls__ozpq)
        vaon__wlqn = init_nested_counts(whb__fefkj)
        for i in range(n):
            aeg__tnh = index_arr[i]
            if isna(arr, i):
                qts__ostrr = (qts__ostrr[0] + 1,) + qts__ostrr[1:]
                vaon__wlqn = add_nested_counts(vaon__wlqn, aeg__tnh)
                continue
            hzg__eqkcg = arr[i]
            if len(hzg__eqkcg) == 0:
                qts__ostrr = (qts__ostrr[0] + 1,) + qts__ostrr[1:]
                vaon__wlqn = add_nested_counts(vaon__wlqn, aeg__tnh)
                continue
            qts__ostrr = add_nested_counts(qts__ostrr, hzg__eqkcg)
            for ikm__xyszx in range(len(hzg__eqkcg)):
                vaon__wlqn = add_nested_counts(vaon__wlqn, aeg__tnh)
        gfe__xokhe = bodo.utils.utils.alloc_type(qts__ostrr[0], awlls__ozpq,
            qts__ostrr[1:])
        jstdp__sqze = bodo.utils.utils.alloc_type(qts__ostrr[0], rvjb__vnwe,
            vaon__wlqn)
        xep__auy = 0
        for i in range(n):
            if isna(arr, i):
                setna(gfe__xokhe, xep__auy)
                jstdp__sqze[xep__auy] = index_arr[i]
                xep__auy += 1
                continue
            hzg__eqkcg = arr[i]
            hmdq__ctr = len(hzg__eqkcg)
            if hmdq__ctr == 0:
                setna(gfe__xokhe, xep__auy)
                jstdp__sqze[xep__auy] = index_arr[i]
                xep__auy += 1
                continue
            gfe__xokhe[xep__auy:xep__auy + hmdq__ctr] = hzg__eqkcg
            jstdp__sqze[xep__auy:xep__auy + hmdq__ctr] = index_arr[i]
            xep__auy += hmdq__ctr
        return gfe__xokhe, jstdp__sqze
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    awlls__ozpq = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        qts__ostrr = init_nested_counts(awlls__ozpq)
        for i in range(n):
            if isna(arr, i):
                qts__ostrr = (qts__ostrr[0] + 1,) + qts__ostrr[1:]
                tobw__moz = 1
            else:
                hzg__eqkcg = arr[i]
                uqjo__hqfhy = len(hzg__eqkcg)
                if uqjo__hqfhy == 0:
                    qts__ostrr = (qts__ostrr[0] + 1,) + qts__ostrr[1:]
                    tobw__moz = 1
                    continue
                else:
                    qts__ostrr = add_nested_counts(qts__ostrr, hzg__eqkcg)
                    tobw__moz = uqjo__hqfhy
            if counts[i] != tobw__moz:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        gfe__xokhe = bodo.utils.utils.alloc_type(qts__ostrr[0], awlls__ozpq,
            qts__ostrr[1:])
        xep__auy = 0
        for i in range(n):
            if isna(arr, i):
                setna(gfe__xokhe, xep__auy)
                xep__auy += 1
                continue
            hzg__eqkcg = arr[i]
            hmdq__ctr = len(hzg__eqkcg)
            if hmdq__ctr == 0:
                setna(gfe__xokhe, xep__auy)
                xep__auy += 1
                continue
            gfe__xokhe[xep__auy:xep__auy + hmdq__ctr] = hzg__eqkcg
            xep__auy += hmdq__ctr
        return gfe__xokhe
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(hlx__nzks) for hlx__nzks in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        nkif__nhy = 'np.empty(n, np.int64)'
        sys__ldu = 'out_arr[i] = 1'
        ymroo__nimeh = 'max(len(arr[i]), 1)'
    else:
        nkif__nhy = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        sys__ldu = 'bodo.libs.array_kernels.setna(out_arr, i)'
        ymroo__nimeh = 'len(arr[i])'
    gqwa__lhka = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {nkif__nhy}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {sys__ldu}
        else:
            out_arr[i] = {ymroo__nimeh}
    return out_arr
    """
    muxv__ogdp = {}
    exec(gqwa__lhka, {'bodo': bodo, 'numba': numba, 'np': np}, muxv__ogdp)
    impl = muxv__ogdp['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    rvjb__vnwe = index_arr
    whb__fefkj = rvjb__vnwe.dtype

    def impl(arr, pat, n, index_arr):
        jshg__wvmeg = pat is not None and len(pat) > 1
        if jshg__wvmeg:
            sdqt__wly = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        ipm__fli = len(arr)
        gkku__sxvyd = 0
        mgi__cvarv = 0
        vaon__wlqn = init_nested_counts(whb__fefkj)
        for i in range(ipm__fli):
            aeg__tnh = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                gkku__sxvyd += 1
                vaon__wlqn = add_nested_counts(vaon__wlqn, aeg__tnh)
                continue
            if jshg__wvmeg:
                asfbj__hrd = sdqt__wly.split(arr[i], maxsplit=n)
            else:
                asfbj__hrd = arr[i].split(pat, n)
            gkku__sxvyd += len(asfbj__hrd)
            for s in asfbj__hrd:
                vaon__wlqn = add_nested_counts(vaon__wlqn, aeg__tnh)
                mgi__cvarv += bodo.libs.str_arr_ext.get_utf8_size(s)
        gfe__xokhe = bodo.libs.str_arr_ext.pre_alloc_string_array(gkku__sxvyd,
            mgi__cvarv)
        jstdp__sqze = bodo.utils.utils.alloc_type(gkku__sxvyd, rvjb__vnwe,
            vaon__wlqn)
        zqf__zefj = 0
        for uvc__alsa in range(ipm__fli):
            if isna(arr, uvc__alsa):
                gfe__xokhe[zqf__zefj] = ''
                bodo.libs.array_kernels.setna(gfe__xokhe, zqf__zefj)
                jstdp__sqze[zqf__zefj] = index_arr[uvc__alsa]
                zqf__zefj += 1
                continue
            if jshg__wvmeg:
                asfbj__hrd = sdqt__wly.split(arr[uvc__alsa], maxsplit=n)
            else:
                asfbj__hrd = arr[uvc__alsa].split(pat, n)
            qjjk__plf = len(asfbj__hrd)
            gfe__xokhe[zqf__zefj:zqf__zefj + qjjk__plf] = asfbj__hrd
            jstdp__sqze[zqf__zefj:zqf__zefj + qjjk__plf] = index_arr[uvc__alsa]
            zqf__zefj += qjjk__plf
        return gfe__xokhe, jstdp__sqze
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
            gfe__xokhe = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                gfe__xokhe[i] = np.nan
            return gfe__xokhe
        return impl_float
    pfh__azqfq = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        gfe__xokhe = bodo.utils.utils.alloc_type(n, pfh__azqfq, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(gfe__xokhe, i)
        return gfe__xokhe
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
    fjqjx__eec = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            gfe__xokhe = bodo.utils.utils.alloc_type(new_len, fjqjx__eec)
            bodo.libs.str_arr_ext.str_copy_ptr(gfe__xokhe.ctypes, 0, A.
                ctypes, old_size)
            return gfe__xokhe
        return impl_char

    def impl(A, old_size, new_len):
        gfe__xokhe = bodo.utils.utils.alloc_type(new_len, fjqjx__eec, (-1,))
        gfe__xokhe[:old_size] = A[:old_size]
        return gfe__xokhe
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    uneu__mrwiq = math.ceil((stop - start) / step)
    return int(max(uneu__mrwiq, 0))


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
    if any(isinstance(jmhn__xtv, types.Complex) for jmhn__xtv in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            lyhh__zgc = (stop - start) / step
            uneu__mrwiq = math.ceil(lyhh__zgc.real)
            qlx__xzzy = math.ceil(lyhh__zgc.imag)
            ookks__srglr = int(max(min(qlx__xzzy, uneu__mrwiq), 0))
            arr = np.empty(ookks__srglr, dtype)
            for i in numba.parfors.parfor.internal_prange(ookks__srglr):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            ookks__srglr = bodo.libs.array_kernels.calc_nitems(start, stop,
                step)
            arr = np.empty(ookks__srglr, dtype)
            for i in numba.parfors.parfor.internal_prange(ookks__srglr):
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
        gjsh__fsch = arr,
        if not inplace:
            gjsh__fsch = arr.copy(),
        yspz__vpj = bodo.libs.str_arr_ext.to_list_if_immutable_arr(gjsh__fsch)
        bkjgi__axyb = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True
            )
        bodo.libs.timsort.sort(yspz__vpj, 0, n, bkjgi__axyb)
        if not ascending:
            bodo.libs.timsort.reverseRange(yspz__vpj, 0, n, bkjgi__axyb)
        bodo.libs.str_arr_ext.cp_str_list_to_array(gjsh__fsch, yspz__vpj)
        return gjsh__fsch[0]
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
        kovs__wprs = []
        for i in range(n):
            if A[i]:
                kovs__wprs.append(i + offset)
        return np.array(kovs__wprs, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    fjqjx__eec = element_type(A)
    if fjqjx__eec == types.unicode_type:
        null_value = '""'
    elif fjqjx__eec == types.bool_:
        null_value = 'False'
    elif fjqjx__eec == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif fjqjx__eec == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    zqf__zefj = 'i'
    cap__iemgb = False
    tqbf__ydtf = get_overload_const_str(method)
    if tqbf__ydtf in ('ffill', 'pad'):
        qihc__spgn = 'n'
        send_right = True
    elif tqbf__ydtf in ('backfill', 'bfill'):
        qihc__spgn = 'n-1, -1, -1'
        send_right = False
        if fjqjx__eec == types.unicode_type:
            zqf__zefj = '(n - 1) - i'
            cap__iemgb = True
    gqwa__lhka = 'def impl(A, method, parallel=False):\n'
    gqwa__lhka += '  A = decode_if_dict_array(A)\n'
    gqwa__lhka += '  has_last_value = False\n'
    gqwa__lhka += f'  last_value = {null_value}\n'
    gqwa__lhka += '  if parallel:\n'
    gqwa__lhka += '    rank = bodo.libs.distributed_api.get_rank()\n'
    gqwa__lhka += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    gqwa__lhka += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    gqwa__lhka += '  n = len(A)\n'
    gqwa__lhka += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    gqwa__lhka += f'  for i in range({qihc__spgn}):\n'
    gqwa__lhka += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    gqwa__lhka += (
        f'      bodo.libs.array_kernels.setna(out_arr, {zqf__zefj})\n')
    gqwa__lhka += '      continue\n'
    gqwa__lhka += '    s = A[i]\n'
    gqwa__lhka += '    if bodo.libs.array_kernels.isna(A, i):\n'
    gqwa__lhka += '      s = last_value\n'
    gqwa__lhka += f'    out_arr[{zqf__zefj}] = s\n'
    gqwa__lhka += '    last_value = s\n'
    gqwa__lhka += '    has_last_value = True\n'
    if cap__iemgb:
        gqwa__lhka += '  return out_arr[::-1]\n'
    else:
        gqwa__lhka += '  return out_arr\n'
    krt__hwks = {}
    exec(gqwa__lhka, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, krt__hwks)
    impl = krt__hwks['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        cuw__midua = 0
        vhlst__ukfd = n_pes - 1
        dcem__ulve = np.int32(rank + 1)
        doh__ehch = np.int32(rank - 1)
        hgw__nmrvx = len(in_arr) - 1
        pfurf__kibvc = -1
        puyaa__fkfd = -1
    else:
        cuw__midua = n_pes - 1
        vhlst__ukfd = 0
        dcem__ulve = np.int32(rank - 1)
        doh__ehch = np.int32(rank + 1)
        hgw__nmrvx = 0
        pfurf__kibvc = len(in_arr)
        puyaa__fkfd = 1
    qxawe__ryjr = np.int32(bodo.hiframes.rolling.comm_border_tag)
    gyo__thbk = np.empty(1, dtype=np.bool_)
    kmr__yzsmr = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    rgjb__pkn = np.empty(1, dtype=np.bool_)
    qtvc__kcbot = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    czhnu__mfi = False
    zmesl__ybetf = null_value
    for i in range(hgw__nmrvx, pfurf__kibvc, puyaa__fkfd):
        if not isna(in_arr, i):
            czhnu__mfi = True
            zmesl__ybetf = in_arr[i]
            break
    if rank != cuw__midua:
        qhyk__bgf = bodo.libs.distributed_api.irecv(gyo__thbk, 1, doh__ehch,
            qxawe__ryjr, True)
        bodo.libs.distributed_api.wait(qhyk__bgf, True)
        dwhmz__cxdou = bodo.libs.distributed_api.irecv(kmr__yzsmr, 1,
            doh__ehch, qxawe__ryjr, True)
        bodo.libs.distributed_api.wait(dwhmz__cxdou, True)
        fxv__keyq = gyo__thbk[0]
        cwg__rdvq = kmr__yzsmr[0]
    else:
        fxv__keyq = False
        cwg__rdvq = null_value
    if czhnu__mfi:
        rgjb__pkn[0] = czhnu__mfi
        qtvc__kcbot[0] = zmesl__ybetf
    else:
        rgjb__pkn[0] = fxv__keyq
        qtvc__kcbot[0] = cwg__rdvq
    if rank != vhlst__ukfd:
        lsitt__bxfg = bodo.libs.distributed_api.isend(rgjb__pkn, 1,
            dcem__ulve, qxawe__ryjr, True)
        jgz__zrjfs = bodo.libs.distributed_api.isend(qtvc__kcbot, 1,
            dcem__ulve, qxawe__ryjr, True)
    return fxv__keyq, cwg__rdvq


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    hihv__edxgz = {'axis': axis, 'kind': kind, 'order': order}
    kvs__pvw = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', hihv__edxgz, kvs__pvw, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    fjqjx__eec = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            ipm__fli = len(A)
            gfe__xokhe = bodo.utils.utils.alloc_type(ipm__fli * repeats,
                fjqjx__eec, (-1,))
            for i in range(ipm__fli):
                zqf__zefj = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for uvc__alsa in range(repeats):
                        bodo.libs.array_kernels.setna(gfe__xokhe, zqf__zefj +
                            uvc__alsa)
                else:
                    gfe__xokhe[zqf__zefj:zqf__zefj + repeats] = A[i]
            return gfe__xokhe
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        ipm__fli = len(A)
        gfe__xokhe = bodo.utils.utils.alloc_type(repeats.sum(), fjqjx__eec,
            (-1,))
        zqf__zefj = 0
        for i in range(ipm__fli):
            rmxxr__mmp = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for uvc__alsa in range(rmxxr__mmp):
                    bodo.libs.array_kernels.setna(gfe__xokhe, zqf__zefj +
                        uvc__alsa)
            else:
                gfe__xokhe[zqf__zefj:zqf__zefj + rmxxr__mmp] = A[i]
            zqf__zefj += rmxxr__mmp
        return gfe__xokhe
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
        anvm__sizmv = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(anvm__sizmv, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        biom__bhd = bodo.libs.array_kernels.concat([A1, A2])
        loypx__nuao = bodo.libs.array_kernels.unique(biom__bhd)
        return pd.Series(loypx__nuao).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    hihv__edxgz = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    kvs__pvw = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', hihv__edxgz, kvs__pvw, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        xie__wycp = bodo.libs.array_kernels.unique(A1)
        onknq__wxxdj = bodo.libs.array_kernels.unique(A2)
        biom__bhd = bodo.libs.array_kernels.concat([xie__wycp, onknq__wxxdj])
        hikh__mrnt = pd.Series(biom__bhd).sort_values().values
        return slice_array_intersect1d(hikh__mrnt)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    hrkg__ayj = arr[1:] == arr[:-1]
    return arr[:-1][hrkg__ayj]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    hihv__edxgz = {'assume_unique': assume_unique}
    kvs__pvw = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', hihv__edxgz, kvs__pvw, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        xie__wycp = bodo.libs.array_kernels.unique(A1)
        onknq__wxxdj = bodo.libs.array_kernels.unique(A2)
        hrkg__ayj = calculate_mask_setdiff1d(xie__wycp, onknq__wxxdj)
        return pd.Series(xie__wycp[hrkg__ayj]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    hrkg__ayj = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        hrkg__ayj &= A1 != A2[i]
    return hrkg__ayj


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    hihv__edxgz = {'retstep': retstep, 'axis': axis}
    kvs__pvw = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', hihv__edxgz, kvs__pvw, 'numpy')
    xjhc__uxlat = False
    if is_overload_none(dtype):
        fjqjx__eec = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            xjhc__uxlat = True
        fjqjx__eec = numba.np.numpy_support.as_dtype(dtype).type
    if xjhc__uxlat:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            syiin__bckw = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            gfe__xokhe = np.empty(num, fjqjx__eec)
            for i in numba.parfors.parfor.internal_prange(num):
                gfe__xokhe[i] = fjqjx__eec(np.floor(start + i * syiin__bckw))
            return gfe__xokhe
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            syiin__bckw = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            gfe__xokhe = np.empty(num, fjqjx__eec)
            for i in numba.parfors.parfor.internal_prange(num):
                gfe__xokhe[i] = fjqjx__eec(start + i * syiin__bckw)
            return gfe__xokhe
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
        xlkcj__oycf = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                xlkcj__oycf += A[i] == val
        return xlkcj__oycf > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    hihv__edxgz = {'axis': axis, 'out': out, 'keepdims': keepdims}
    kvs__pvw = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', hihv__edxgz, kvs__pvw, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        xlkcj__oycf = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                xlkcj__oycf += int(bool(A[i]))
        return xlkcj__oycf > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    hihv__edxgz = {'axis': axis, 'out': out, 'keepdims': keepdims}
    kvs__pvw = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', hihv__edxgz, kvs__pvw, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        xlkcj__oycf = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                xlkcj__oycf += int(bool(A[i]))
        return xlkcj__oycf == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    hihv__edxgz = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    kvs__pvw = {'out': None, 'where': True, 'casting': 'same_kind', 'order':
        'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', hihv__edxgz, kvs__pvw, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        taxme__osih = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            gfe__xokhe = np.empty(n, taxme__osih)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(gfe__xokhe, i)
                    continue
                gfe__xokhe[i] = np_cbrt_scalar(A[i], taxme__osih)
            return gfe__xokhe
        return impl_arr
    taxme__osih = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, taxme__osih)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    rbz__zdmwh = x < 0
    if rbz__zdmwh:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if rbz__zdmwh:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    noo__bbf = isinstance(tup, (types.BaseTuple, types.List))
    buq__nct = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for srsmr__fgd in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                srsmr__fgd, 'numpy.hstack()')
            noo__bbf = noo__bbf and bodo.utils.utils.is_array_typ(srsmr__fgd,
                False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        noo__bbf = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif buq__nct:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        zdmg__srcb = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for srsmr__fgd in zdmg__srcb.types:
            buq__nct = buq__nct and bodo.utils.utils.is_array_typ(srsmr__fgd,
                False)
    if not (noo__bbf or buq__nct):
        return
    if buq__nct:

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
    hihv__edxgz = {'check_valid': check_valid, 'tol': tol}
    kvs__pvw = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', hihv__edxgz,
        kvs__pvw, 'numpy')
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
        uzhxp__lym = mean.shape[0]
        zoqof__fchuc = size, uzhxp__lym
        dnjv__rhq = np.random.standard_normal(zoqof__fchuc)
        cov = cov.astype(np.float64)
        slluf__ofp, s, dlo__orf = np.linalg.svd(cov)
        res = np.dot(dnjv__rhq, np.sqrt(s).reshape(uzhxp__lym, 1) * dlo__orf)
        fxyot__kxs = res + mean
        return fxyot__kxs
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
            phf__vzubh = bodo.hiframes.series_kernels._get_type_max_value(arr)
            oab__fckr = typing.builtins.IndexValue(-1, phf__vzubh)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mvyvl__pfol = typing.builtins.IndexValue(i, arr[i])
                oab__fckr = min(oab__fckr, mvyvl__pfol)
            return oab__fckr.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        mobk__osyn = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            pigue__wepot = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            phf__vzubh = mobk__osyn(len(arr.dtype.categories) + 1)
            oab__fckr = typing.builtins.IndexValue(-1, phf__vzubh)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mvyvl__pfol = typing.builtins.IndexValue(i, pigue__wepot[i])
                oab__fckr = min(oab__fckr, mvyvl__pfol)
            return oab__fckr.index
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
            phf__vzubh = bodo.hiframes.series_kernels._get_type_min_value(arr)
            oab__fckr = typing.builtins.IndexValue(-1, phf__vzubh)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mvyvl__pfol = typing.builtins.IndexValue(i, arr[i])
                oab__fckr = max(oab__fckr, mvyvl__pfol)
            return oab__fckr.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        mobk__osyn = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            pigue__wepot = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            phf__vzubh = mobk__osyn(-1)
            oab__fckr = typing.builtins.IndexValue(-1, phf__vzubh)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mvyvl__pfol = typing.builtins.IndexValue(i, pigue__wepot[i])
                oab__fckr = max(oab__fckr, mvyvl__pfol)
            return oab__fckr.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
