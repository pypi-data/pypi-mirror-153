"""Some kernels for Series related functions. This is a legacy file that needs to be
refactored.
"""
import datetime
import numba
import numpy as np
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.int_arr_ext import IntDtype
from bodo.utils.typing import decode_if_dict_array


def _column_filter_impl(B, ind):
    bwvpn__pkt = bodo.hiframes.rolling.alloc_shift(len(B), B, (-1,))
    for grnfa__djnb in numba.parfors.parfor.internal_prange(len(bwvpn__pkt)):
        if ind[grnfa__djnb]:
            bwvpn__pkt[grnfa__djnb] = B[grnfa__djnb]
        else:
            bodo.libs.array_kernels.setna(bwvpn__pkt, grnfa__djnb)
    return bwvpn__pkt


@numba.njit(no_cpython_wrapper=True)
def _series_dropna_str_alloc_impl_inner(B):
    B = decode_if_dict_array(B)
    xnzb__mvcun = len(B)
    lkd__wzlmc = 0
    for grnfa__djnb in range(len(B)):
        if bodo.libs.str_arr_ext.str_arr_is_na(B, grnfa__djnb):
            lkd__wzlmc += 1
    jwl__ickp = xnzb__mvcun - lkd__wzlmc
    utrt__ixq = bodo.libs.str_arr_ext.num_total_chars(B)
    bwvpn__pkt = bodo.libs.str_arr_ext.pre_alloc_string_array(jwl__ickp,
        utrt__ixq)
    bodo.libs.str_arr_ext.copy_non_null_offsets(bwvpn__pkt, B)
    bodo.libs.str_arr_ext.copy_data(bwvpn__pkt, B)
    bodo.libs.str_arr_ext.set_null_bits_to_value(bwvpn__pkt, -1)
    return bwvpn__pkt


def _get_nan(val):
    return np.nan


@overload(_get_nan, no_unliteral=True)
def _get_nan_overload(val):
    if isinstance(val, (types.NPDatetime, types.NPTimedelta)):
        nat = val('NaT')
        return lambda val: nat
    if isinstance(val, types.Float):
        return lambda val: np.nan
    return lambda val: val


def _get_type_max_value(dtype):
    return 0


@overload(_get_type_max_value, inline='always', no_unliteral=True)
def _get_type_max_value_overload(dtype):
    if isinstance(dtype, (bodo.IntegerArrayType, IntDtype)):
        _dtype = dtype.dtype
        return lambda dtype: numba.cpython.builtins.get_type_max_value(_dtype)
    if dtype == bodo.datetime_date_array_type:
        return lambda dtype: _get_date_max_value()
    if isinstance(dtype.dtype, types.NPDatetime):
        return lambda dtype: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
            numba.cpython.builtins.get_type_max_value(numba.core.types.int64))
    if isinstance(dtype.dtype, types.NPTimedelta):
        return (lambda dtype: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(numba.cpython.builtins.
            get_type_max_value(numba.core.types.int64)))
    if dtype.dtype == types.bool_:
        return lambda dtype: True
    return lambda dtype: numba.cpython.builtins.get_type_max_value(dtype)


@register_jitable
def _get_date_max_value():
    return datetime.date(datetime.MAXYEAR, 12, 31)


def _get_type_min_value(dtype):
    return 0


@overload(_get_type_min_value, inline='always', no_unliteral=True)
def _get_type_min_value_overload(dtype):
    if isinstance(dtype, (bodo.IntegerArrayType, IntDtype)):
        _dtype = dtype.dtype
        return lambda dtype: numba.cpython.builtins.get_type_min_value(_dtype)
    if dtype == bodo.datetime_date_array_type:
        return lambda dtype: _get_date_min_value()
    if isinstance(dtype.dtype, types.NPDatetime):
        return lambda dtype: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
            numba.cpython.builtins.get_type_min_value(numba.core.types.int64))
    if isinstance(dtype.dtype, types.NPTimedelta):
        return (lambda dtype: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(numba.cpython.builtins.
            get_type_min_value(numba.core.types.uint64)))
    if dtype.dtype == types.bool_:
        return lambda dtype: False
    return lambda dtype: numba.cpython.builtins.get_type_min_value(dtype)


@register_jitable
def _get_date_min_value():
    return datetime.date(datetime.MINYEAR, 1, 1)


@overload(min)
def indval_min(a1, a2):
    if a1 == types.bool_ and a2 == types.bool_:

        def min_impl(a1, a2):
            if a1 > a2:
                return a2
            return a1
        return min_impl


@overload(max)
def indval_max(a1, a2):
    if a1 == types.bool_ and a2 == types.bool_:

        def max_impl(a1, a2):
            if a2 > a1:
                return a2
            return a1
        return max_impl


@numba.njit
def _sum_handle_nan(s, count):
    if not count:
        s = bodo.hiframes.series_kernels._get_nan(s)
    return s


@numba.njit
def _box_cat_val(s, cat_dtype, count):
    if s == -1 or count == 0:
        return bodo.hiframes.series_kernels._get_nan(cat_dtype.categories[0])
    return cat_dtype.categories[s]


@numba.generated_jit
def get_float_nan(s):
    nan = np.nan
    if s == types.float32:
        nan = np.float32('nan')
    return lambda s: nan


@numba.njit
def _mean_handle_nan(s, count):
    if not count:
        s = get_float_nan(s)
    else:
        s = s / count
    return s


@numba.njit
def _var_handle_mincount(s, count, min_count):
    if count < min_count:
        res = np.nan
    else:
        res = s
    return res


@numba.njit
def _compute_var_nan_count_ddof(first_moment, second_moment, count, ddof):
    if count == 0 or count <= ddof:
        s = np.nan
    else:
        s = second_moment - first_moment * first_moment / count
        s = s / (count - ddof)
    return s


@numba.njit
def _sem_handle_nan(res, count):
    if count < 1:
        myihb__ddlm = np.nan
    else:
        myihb__ddlm = (res / count) ** 0.5
    return myihb__ddlm


@numba.njit
def lt_f(a, b):
    return a < b


@numba.njit
def gt_f(a, b):
    return a > b


@numba.njit
def compute_skew(first_moment, second_moment, third_moment, count):
    if count < 3:
        return np.nan
    fva__qtco = first_moment / count
    htb__wbt = (third_moment - 3 * second_moment * fva__qtco + 2 * count * 
        fva__qtco ** 3)
    vuzh__tce = second_moment - fva__qtco * first_moment
    s = count * (count - 1) ** 1.5 / (count - 2) * htb__wbt / vuzh__tce ** 1.5
    s = s / (count - 1)
    return s


@numba.njit
def compute_kurt(first_moment, second_moment, third_moment, fourth_moment,
    count):
    if count < 4:
        return np.nan
    fva__qtco = first_moment / count
    azr__ttoum = (fourth_moment - 4 * third_moment * fva__qtco + 6 *
        second_moment * fva__qtco ** 2 - 3 * count * fva__qtco ** 4)
    ccqsw__qzo = second_moment - fva__qtco * first_moment
    vmc__qcwz = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))
    ojrp__zavrp = count * (count + 1) * (count - 1) * azr__ttoum
    druw__ieu = (count - 2) * (count - 3) * ccqsw__qzo ** 2
    s = (count - 1) * (ojrp__zavrp / druw__ieu - vmc__qcwz)
    s = s / (count - 1)
    return s
