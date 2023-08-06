"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    dhhs__gxim = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(dhhs__gxim.ctypes,
        arr, parallel, skipna)
    return dhhs__gxim[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ioant__nzugu = len(arr)
        ewws__feg = np.empty(ioant__nzugu, np.bool_)
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(ioant__nzugu):
            ewws__feg[tbuc__gjhpf] = bodo.libs.array_kernels.isna(arr,
                tbuc__gjhpf)
        return ewws__feg
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ijx__pvbv = 0
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
            wmcfo__jnnjs = 0
            if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                wmcfo__jnnjs = 1
            ijx__pvbv += wmcfo__jnnjs
        dhhs__gxim = ijx__pvbv
        return dhhs__gxim
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    rrhe__kqdjy = array_op_count(arr)
    psdqx__vaew = array_op_min(arr)
    tjx__temq = array_op_max(arr)
    www__pge = array_op_mean(arr)
    aatzu__zyk = array_op_std(arr)
    ipptw__cnqsj = array_op_quantile(arr, 0.25)
    idy__oxwsl = array_op_quantile(arr, 0.5)
    wdry__zpjum = array_op_quantile(arr, 0.75)
    return (rrhe__kqdjy, www__pge, aatzu__zyk, psdqx__vaew, ipptw__cnqsj,
        idy__oxwsl, wdry__zpjum, tjx__temq)


def array_op_describe_dt_impl(arr):
    rrhe__kqdjy = array_op_count(arr)
    psdqx__vaew = array_op_min(arr)
    tjx__temq = array_op_max(arr)
    www__pge = array_op_mean(arr)
    ipptw__cnqsj = array_op_quantile(arr, 0.25)
    idy__oxwsl = array_op_quantile(arr, 0.5)
    wdry__zpjum = array_op_quantile(arr, 0.75)
    return (rrhe__kqdjy, www__pge, psdqx__vaew, ipptw__cnqsj, idy__oxwsl,
        wdry__zpjum, tjx__temq)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = numba.cpython.builtins.get_type_max_value(np.int64)
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = cxs__rtgfm
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[tbuc__gjhpf]))
                    wmcfo__jnnjs = 1
                cxs__rtgfm = min(cxs__rtgfm, glx__uif)
                ijx__pvbv += wmcfo__jnnjs
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(cxs__rtgfm,
                ijx__pvbv)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = numba.cpython.builtins.get_type_max_value(np.int64)
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = cxs__rtgfm
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[tbuc__gjhpf])
                    wmcfo__jnnjs = 1
                cxs__rtgfm = min(cxs__rtgfm, glx__uif)
                ijx__pvbv += wmcfo__jnnjs
            return bodo.hiframes.pd_index_ext._dti_val_finalize(cxs__rtgfm,
                ijx__pvbv)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            dqtk__arbc = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = numba.cpython.builtins.get_type_max_value(np.int64)
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(
                dqtk__arbc)):
                mkrtr__rou = dqtk__arbc[tbuc__gjhpf]
                if mkrtr__rou == -1:
                    continue
                cxs__rtgfm = min(cxs__rtgfm, mkrtr__rou)
                ijx__pvbv += 1
            dhhs__gxim = bodo.hiframes.series_kernels._box_cat_val(cxs__rtgfm,
                arr.dtype, ijx__pvbv)
            return dhhs__gxim
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = bodo.hiframes.series_kernels._get_date_max_value()
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = cxs__rtgfm
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = arr[tbuc__gjhpf]
                    wmcfo__jnnjs = 1
                cxs__rtgfm = min(cxs__rtgfm, glx__uif)
                ijx__pvbv += wmcfo__jnnjs
            dhhs__gxim = bodo.hiframes.series_kernels._sum_handle_nan(
                cxs__rtgfm, ijx__pvbv)
            return dhhs__gxim
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        cxs__rtgfm = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        ijx__pvbv = 0
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
            glx__uif = cxs__rtgfm
            wmcfo__jnnjs = 0
            if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                glx__uif = arr[tbuc__gjhpf]
                wmcfo__jnnjs = 1
            cxs__rtgfm = min(cxs__rtgfm, glx__uif)
            ijx__pvbv += wmcfo__jnnjs
        dhhs__gxim = bodo.hiframes.series_kernels._sum_handle_nan(cxs__rtgfm,
            ijx__pvbv)
        return dhhs__gxim
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = numba.cpython.builtins.get_type_min_value(np.int64)
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = cxs__rtgfm
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[tbuc__gjhpf]))
                    wmcfo__jnnjs = 1
                cxs__rtgfm = max(cxs__rtgfm, glx__uif)
                ijx__pvbv += wmcfo__jnnjs
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(cxs__rtgfm,
                ijx__pvbv)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = numba.cpython.builtins.get_type_min_value(np.int64)
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = cxs__rtgfm
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[tbuc__gjhpf])
                    wmcfo__jnnjs = 1
                cxs__rtgfm = max(cxs__rtgfm, glx__uif)
                ijx__pvbv += wmcfo__jnnjs
            return bodo.hiframes.pd_index_ext._dti_val_finalize(cxs__rtgfm,
                ijx__pvbv)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            dqtk__arbc = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = -1
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(
                dqtk__arbc)):
                cxs__rtgfm = max(cxs__rtgfm, dqtk__arbc[tbuc__gjhpf])
            dhhs__gxim = bodo.hiframes.series_kernels._box_cat_val(cxs__rtgfm,
                arr.dtype, 1)
            return dhhs__gxim
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = bodo.hiframes.series_kernels._get_date_min_value()
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = cxs__rtgfm
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = arr[tbuc__gjhpf]
                    wmcfo__jnnjs = 1
                cxs__rtgfm = max(cxs__rtgfm, glx__uif)
                ijx__pvbv += wmcfo__jnnjs
            dhhs__gxim = bodo.hiframes.series_kernels._sum_handle_nan(
                cxs__rtgfm, ijx__pvbv)
            return dhhs__gxim
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        cxs__rtgfm = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        ijx__pvbv = 0
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
            glx__uif = cxs__rtgfm
            wmcfo__jnnjs = 0
            if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                glx__uif = arr[tbuc__gjhpf]
                wmcfo__jnnjs = 1
            cxs__rtgfm = max(cxs__rtgfm, glx__uif)
            ijx__pvbv += wmcfo__jnnjs
        dhhs__gxim = bodo.hiframes.series_kernels._sum_handle_nan(cxs__rtgfm,
            ijx__pvbv)
        return dhhs__gxim
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    osexz__opvle = types.float64
    sru__ezck = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        osexz__opvle = types.float32
        sru__ezck = types.float32
    ecvl__cjbwv = osexz__opvle(0)
    ysbwi__dpz = sru__ezck(0)
    hujng__edxwf = sru__ezck(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        cxs__rtgfm = ecvl__cjbwv
        ijx__pvbv = ysbwi__dpz
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
            glx__uif = ecvl__cjbwv
            wmcfo__jnnjs = ysbwi__dpz
            if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                glx__uif = arr[tbuc__gjhpf]
                wmcfo__jnnjs = hujng__edxwf
            cxs__rtgfm += glx__uif
            ijx__pvbv += wmcfo__jnnjs
        dhhs__gxim = bodo.hiframes.series_kernels._mean_handle_nan(cxs__rtgfm,
            ijx__pvbv)
        return dhhs__gxim
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        dcx__puiih = 0.0
        mxzmv__iesq = 0.0
        ijx__pvbv = 0
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
            glx__uif = 0.0
            wmcfo__jnnjs = 0
            if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf
                ) or not skipna:
                glx__uif = arr[tbuc__gjhpf]
                wmcfo__jnnjs = 1
            dcx__puiih += glx__uif
            mxzmv__iesq += glx__uif * glx__uif
            ijx__pvbv += wmcfo__jnnjs
        dhhs__gxim = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            dcx__puiih, mxzmv__iesq, ijx__pvbv, ddof)
        return dhhs__gxim
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                ewws__feg = np.empty(len(q), np.int64)
                for tbuc__gjhpf in range(len(q)):
                    icj__ubpvu = np.float64(q[tbuc__gjhpf])
                    ewws__feg[tbuc__gjhpf] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), icj__ubpvu)
                return ewws__feg.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            ewws__feg = np.empty(len(q), np.float64)
            for tbuc__gjhpf in range(len(q)):
                icj__ubpvu = np.float64(q[tbuc__gjhpf])
                ewws__feg[tbuc__gjhpf] = bodo.libs.array_kernels.quantile(arr,
                    icj__ubpvu)
            return ewws__feg
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        baefr__hicit = types.intp
    elif arr.dtype == types.bool_:
        baefr__hicit = np.int64
    else:
        baefr__hicit = arr.dtype
    wrjez__lyodf = baefr__hicit(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = wrjez__lyodf
            ioant__nzugu = len(arr)
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(
                ioant__nzugu):
                glx__uif = wrjez__lyodf
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf
                    ) or not skipna:
                    glx__uif = arr[tbuc__gjhpf]
                    wmcfo__jnnjs = 1
                cxs__rtgfm += glx__uif
                ijx__pvbv += wmcfo__jnnjs
            dhhs__gxim = bodo.hiframes.series_kernels._var_handle_mincount(
                cxs__rtgfm, ijx__pvbv, min_count)
            return dhhs__gxim
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = wrjez__lyodf
            ioant__nzugu = len(arr)
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(
                ioant__nzugu):
                glx__uif = wrjez__lyodf
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = arr[tbuc__gjhpf]
                cxs__rtgfm += glx__uif
            return cxs__rtgfm
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    nsf__ugn = arr.dtype(1)
    if arr.dtype == types.bool_:
        nsf__ugn = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = nsf__ugn
            ijx__pvbv = 0
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = nsf__ugn
                wmcfo__jnnjs = 0
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf
                    ) or not skipna:
                    glx__uif = arr[tbuc__gjhpf]
                    wmcfo__jnnjs = 1
                ijx__pvbv += wmcfo__jnnjs
                cxs__rtgfm *= glx__uif
            dhhs__gxim = bodo.hiframes.series_kernels._var_handle_mincount(
                cxs__rtgfm, ijx__pvbv, min_count)
            return dhhs__gxim
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            cxs__rtgfm = nsf__ugn
            for tbuc__gjhpf in numba.parfors.parfor.internal_prange(len(arr)):
                glx__uif = nsf__ugn
                if not bodo.libs.array_kernels.isna(arr, tbuc__gjhpf):
                    glx__uif = arr[tbuc__gjhpf]
                cxs__rtgfm *= glx__uif
            return cxs__rtgfm
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        tbuc__gjhpf = bodo.libs.array_kernels._nan_argmax(arr)
        return index[tbuc__gjhpf]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        tbuc__gjhpf = bodo.libs.array_kernels._nan_argmin(arr)
        return index[tbuc__gjhpf]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            vsmdp__zod = {}
            for vence__mkjo in values:
                vsmdp__zod[bodo.utils.conversion.box_if_dt64(vence__mkjo)] = 0
            return vsmdp__zod
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        ioant__nzugu = len(arr)
        ewws__feg = np.empty(ioant__nzugu, np.bool_)
        for tbuc__gjhpf in numba.parfors.parfor.internal_prange(ioant__nzugu):
            ewws__feg[tbuc__gjhpf] = bodo.utils.conversion.box_if_dt64(arr[
                tbuc__gjhpf]) in values
        return ewws__feg
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    dqn__sgryr = len(in_arr_tup) != 1
    gyev__zkac = list(in_arr_tup.types)
    vjho__nwm = 'def impl(in_arr_tup):\n'
    vjho__nwm += '  n = len(in_arr_tup[0])\n'
    if dqn__sgryr:
        jgds__yphk = ', '.join([f'in_arr_tup[{tbuc__gjhpf}][unused]' for
            tbuc__gjhpf in range(len(in_arr_tup))])
        krfa__xef = ', '.join(['False' for iuu__amvkz in range(len(
            in_arr_tup))])
        vjho__nwm += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({jgds__yphk},), ({krfa__xef},)): 0 for unused in range(0)}}
"""
        vjho__nwm += '  map_vector = np.empty(n, np.int64)\n'
        for tbuc__gjhpf, cvwdm__pcj in enumerate(gyev__zkac):
            vjho__nwm += f'  in_lst_{tbuc__gjhpf} = []\n'
            if is_str_arr_type(cvwdm__pcj):
                vjho__nwm += f'  total_len_{tbuc__gjhpf} = 0\n'
            vjho__nwm += f'  null_in_lst_{tbuc__gjhpf} = []\n'
        vjho__nwm += '  for i in range(n):\n'
        rxgj__deh = ', '.join([f'in_arr_tup[{tbuc__gjhpf}][i]' for
            tbuc__gjhpf in range(len(gyev__zkac))])
        uzx__tcgsm = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{tbuc__gjhpf}], i)' for
            tbuc__gjhpf in range(len(gyev__zkac))])
        vjho__nwm += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({rxgj__deh},), ({uzx__tcgsm},))
"""
        vjho__nwm += '    if data_val not in arr_map:\n'
        vjho__nwm += '      set_val = len(arr_map)\n'
        vjho__nwm += '      values_tup = data_val._data\n'
        vjho__nwm += '      nulls_tup = data_val._null_values\n'
        for tbuc__gjhpf, cvwdm__pcj in enumerate(gyev__zkac):
            vjho__nwm += (
                f'      in_lst_{tbuc__gjhpf}.append(values_tup[{tbuc__gjhpf}])\n'
                )
            vjho__nwm += (
                f'      null_in_lst_{tbuc__gjhpf}.append(nulls_tup[{tbuc__gjhpf}])\n'
                )
            if is_str_arr_type(cvwdm__pcj):
                vjho__nwm += f"""      total_len_{tbuc__gjhpf}  += nulls_tup[{tbuc__gjhpf}] * len(values_tup[{tbuc__gjhpf}])
"""
        vjho__nwm += '      arr_map[data_val] = len(arr_map)\n'
        vjho__nwm += '    else:\n'
        vjho__nwm += '      set_val = arr_map[data_val]\n'
        vjho__nwm += '    map_vector[i] = set_val\n'
        vjho__nwm += '  n_rows = len(arr_map)\n'
        for tbuc__gjhpf, cvwdm__pcj in enumerate(gyev__zkac):
            if is_str_arr_type(cvwdm__pcj):
                vjho__nwm += f"""  out_arr_{tbuc__gjhpf} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{tbuc__gjhpf})
"""
            else:
                vjho__nwm += f"""  out_arr_{tbuc__gjhpf} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{tbuc__gjhpf}], (-1,))
"""
        vjho__nwm += '  for j in range(len(arr_map)):\n'
        for tbuc__gjhpf in range(len(gyev__zkac)):
            vjho__nwm += f'    if null_in_lst_{tbuc__gjhpf}[j]:\n'
            vjho__nwm += (
                f'      bodo.libs.array_kernels.setna(out_arr_{tbuc__gjhpf}, j)\n'
                )
            vjho__nwm += '    else:\n'
            vjho__nwm += (
                f'      out_arr_{tbuc__gjhpf}[j] = in_lst_{tbuc__gjhpf}[j]\n')
        zsnc__hufw = ', '.join([f'out_arr_{tbuc__gjhpf}' for tbuc__gjhpf in
            range(len(gyev__zkac))])
        vjho__nwm += f'  return ({zsnc__hufw},), map_vector\n'
    else:
        vjho__nwm += '  in_arr = in_arr_tup[0]\n'
        vjho__nwm += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        vjho__nwm += '  map_vector = np.empty(n, np.int64)\n'
        vjho__nwm += '  is_na = 0\n'
        vjho__nwm += '  in_lst = []\n'
        if is_str_arr_type(gyev__zkac[0]):
            vjho__nwm += '  total_len = 0\n'
        vjho__nwm += '  for i in range(n):\n'
        vjho__nwm += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        vjho__nwm += '      is_na = 1\n'
        vjho__nwm += (
            '      # Always put NA in the last location. We can safely use\n')
        vjho__nwm += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        vjho__nwm += '      set_val = -1\n'
        vjho__nwm += '    else:\n'
        vjho__nwm += '      data_val = in_arr[i]\n'
        vjho__nwm += '      if data_val not in arr_map:\n'
        vjho__nwm += '        set_val = len(arr_map)\n'
        vjho__nwm += '        in_lst.append(data_val)\n'
        if is_str_arr_type(gyev__zkac[0]):
            vjho__nwm += '        total_len += len(data_val)\n'
        vjho__nwm += '        arr_map[data_val] = len(arr_map)\n'
        vjho__nwm += '      else:\n'
        vjho__nwm += '        set_val = arr_map[data_val]\n'
        vjho__nwm += '    map_vector[i] = set_val\n'
        vjho__nwm += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(gyev__zkac[0]):
            vjho__nwm += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            vjho__nwm += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        vjho__nwm += '  for j in range(len(arr_map)):\n'
        vjho__nwm += '    out_arr[j] = in_lst[j]\n'
        vjho__nwm += '  if is_na:\n'
        vjho__nwm += '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n'
        vjho__nwm += f'  return (out_arr,), map_vector\n'
    ajph__gzm = {}
    exec(vjho__nwm, {'bodo': bodo, 'np': np}, ajph__gzm)
    impl = ajph__gzm['impl']
    return impl
