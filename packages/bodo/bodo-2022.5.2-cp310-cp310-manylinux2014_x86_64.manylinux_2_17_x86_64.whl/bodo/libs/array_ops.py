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
    nhc__cjpak = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(nhc__cjpak.ctypes,
        arr, parallel, skipna)
    return nhc__cjpak[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kua__yczn = len(arr)
        owgf__qlgsf = np.empty(kua__yczn, np.bool_)
        for uhh__jooah in numba.parfors.parfor.internal_prange(kua__yczn):
            owgf__qlgsf[uhh__jooah] = bodo.libs.array_kernels.isna(arr,
                uhh__jooah)
        return owgf__qlgsf
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        vdfm__evg = 0
        for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
            ckfwo__kdm = 0
            if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                ckfwo__kdm = 1
            vdfm__evg += ckfwo__kdm
        nhc__cjpak = vdfm__evg
        return nhc__cjpak
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    coq__xaj = array_op_count(arr)
    syfhu__qvbh = array_op_min(arr)
    gyj__dgth = array_op_max(arr)
    udjk__pwv = array_op_mean(arr)
    sjeq__jhjlo = array_op_std(arr)
    anq__czi = array_op_quantile(arr, 0.25)
    ponv__xlug = array_op_quantile(arr, 0.5)
    cdt__hqev = array_op_quantile(arr, 0.75)
    return (coq__xaj, udjk__pwv, sjeq__jhjlo, syfhu__qvbh, anq__czi,
        ponv__xlug, cdt__hqev, gyj__dgth)


def array_op_describe_dt_impl(arr):
    coq__xaj = array_op_count(arr)
    syfhu__qvbh = array_op_min(arr)
    gyj__dgth = array_op_max(arr)
    udjk__pwv = array_op_mean(arr)
    anq__czi = array_op_quantile(arr, 0.25)
    ponv__xlug = array_op_quantile(arr, 0.5)
    cdt__hqev = array_op_quantile(arr, 0.75)
    return (coq__xaj, udjk__pwv, syfhu__qvbh, anq__czi, ponv__xlug,
        cdt__hqev, gyj__dgth)


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
            rqlw__zbw = numba.cpython.builtins.get_type_max_value(np.int64)
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = rqlw__zbw
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[uhh__jooah]))
                    ckfwo__kdm = 1
                rqlw__zbw = min(rqlw__zbw, mjuwi__ljovr)
                vdfm__evg += ckfwo__kdm
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(rqlw__zbw,
                vdfm__evg)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = numba.cpython.builtins.get_type_max_value(np.int64)
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = rqlw__zbw
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[uhh__jooah]))
                    ckfwo__kdm = 1
                rqlw__zbw = min(rqlw__zbw, mjuwi__ljovr)
                vdfm__evg += ckfwo__kdm
            return bodo.hiframes.pd_index_ext._dti_val_finalize(rqlw__zbw,
                vdfm__evg)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            zmik__jmm = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            rqlw__zbw = numba.cpython.builtins.get_type_max_value(np.int64)
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(
                zmik__jmm)):
                rkh__pqspe = zmik__jmm[uhh__jooah]
                if rkh__pqspe == -1:
                    continue
                rqlw__zbw = min(rqlw__zbw, rkh__pqspe)
                vdfm__evg += 1
            nhc__cjpak = bodo.hiframes.series_kernels._box_cat_val(rqlw__zbw,
                arr.dtype, vdfm__evg)
            return nhc__cjpak
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = bodo.hiframes.series_kernels._get_date_max_value()
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = rqlw__zbw
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = arr[uhh__jooah]
                    ckfwo__kdm = 1
                rqlw__zbw = min(rqlw__zbw, mjuwi__ljovr)
                vdfm__evg += ckfwo__kdm
            nhc__cjpak = bodo.hiframes.series_kernels._sum_handle_nan(rqlw__zbw
                , vdfm__evg)
            return nhc__cjpak
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        rqlw__zbw = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype)
        vdfm__evg = 0
        for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
            mjuwi__ljovr = rqlw__zbw
            ckfwo__kdm = 0
            if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                mjuwi__ljovr = arr[uhh__jooah]
                ckfwo__kdm = 1
            rqlw__zbw = min(rqlw__zbw, mjuwi__ljovr)
            vdfm__evg += ckfwo__kdm
        nhc__cjpak = bodo.hiframes.series_kernels._sum_handle_nan(rqlw__zbw,
            vdfm__evg)
        return nhc__cjpak
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = numba.cpython.builtins.get_type_min_value(np.int64)
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = rqlw__zbw
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[uhh__jooah]))
                    ckfwo__kdm = 1
                rqlw__zbw = max(rqlw__zbw, mjuwi__ljovr)
                vdfm__evg += ckfwo__kdm
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(rqlw__zbw,
                vdfm__evg)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = numba.cpython.builtins.get_type_min_value(np.int64)
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = rqlw__zbw
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[uhh__jooah]))
                    ckfwo__kdm = 1
                rqlw__zbw = max(rqlw__zbw, mjuwi__ljovr)
                vdfm__evg += ckfwo__kdm
            return bodo.hiframes.pd_index_ext._dti_val_finalize(rqlw__zbw,
                vdfm__evg)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            zmik__jmm = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            rqlw__zbw = -1
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(
                zmik__jmm)):
                rqlw__zbw = max(rqlw__zbw, zmik__jmm[uhh__jooah])
            nhc__cjpak = bodo.hiframes.series_kernels._box_cat_val(rqlw__zbw,
                arr.dtype, 1)
            return nhc__cjpak
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = bodo.hiframes.series_kernels._get_date_min_value()
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = rqlw__zbw
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = arr[uhh__jooah]
                    ckfwo__kdm = 1
                rqlw__zbw = max(rqlw__zbw, mjuwi__ljovr)
                vdfm__evg += ckfwo__kdm
            nhc__cjpak = bodo.hiframes.series_kernels._sum_handle_nan(rqlw__zbw
                , vdfm__evg)
            return nhc__cjpak
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        rqlw__zbw = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype)
        vdfm__evg = 0
        for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
            mjuwi__ljovr = rqlw__zbw
            ckfwo__kdm = 0
            if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                mjuwi__ljovr = arr[uhh__jooah]
                ckfwo__kdm = 1
            rqlw__zbw = max(rqlw__zbw, mjuwi__ljovr)
            vdfm__evg += ckfwo__kdm
        nhc__cjpak = bodo.hiframes.series_kernels._sum_handle_nan(rqlw__zbw,
            vdfm__evg)
        return nhc__cjpak
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
    rdesa__ogt = types.float64
    pjjcb__afoq = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        rdesa__ogt = types.float32
        pjjcb__afoq = types.float32
    krv__zpnjj = rdesa__ogt(0)
    ofs__evscp = pjjcb__afoq(0)
    kehtf__iohn = pjjcb__afoq(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        rqlw__zbw = krv__zpnjj
        vdfm__evg = ofs__evscp
        for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
            mjuwi__ljovr = krv__zpnjj
            ckfwo__kdm = ofs__evscp
            if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                mjuwi__ljovr = arr[uhh__jooah]
                ckfwo__kdm = kehtf__iohn
            rqlw__zbw += mjuwi__ljovr
            vdfm__evg += ckfwo__kdm
        nhc__cjpak = bodo.hiframes.series_kernels._mean_handle_nan(rqlw__zbw,
            vdfm__evg)
        return nhc__cjpak
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        aubg__yoaif = 0.0
        zgu__pkq = 0.0
        vdfm__evg = 0
        for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
            mjuwi__ljovr = 0.0
            ckfwo__kdm = 0
            if not bodo.libs.array_kernels.isna(arr, uhh__jooah) or not skipna:
                mjuwi__ljovr = arr[uhh__jooah]
                ckfwo__kdm = 1
            aubg__yoaif += mjuwi__ljovr
            zgu__pkq += mjuwi__ljovr * mjuwi__ljovr
            vdfm__evg += ckfwo__kdm
        nhc__cjpak = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            aubg__yoaif, zgu__pkq, vdfm__evg, ddof)
        return nhc__cjpak
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
                owgf__qlgsf = np.empty(len(q), np.int64)
                for uhh__jooah in range(len(q)):
                    hasom__nknd = np.float64(q[uhh__jooah])
                    owgf__qlgsf[uhh__jooah] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), hasom__nknd)
                return owgf__qlgsf.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            owgf__qlgsf = np.empty(len(q), np.float64)
            for uhh__jooah in range(len(q)):
                hasom__nknd = np.float64(q[uhh__jooah])
                owgf__qlgsf[uhh__jooah] = bodo.libs.array_kernels.quantile(arr,
                    hasom__nknd)
            return owgf__qlgsf
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
        brb__huu = types.intp
    elif arr.dtype == types.bool_:
        brb__huu = np.int64
    else:
        brb__huu = arr.dtype
    jedi__otwcn = brb__huu(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = jedi__otwcn
            kua__yczn = len(arr)
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(kua__yczn):
                mjuwi__ljovr = jedi__otwcn
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah
                    ) or not skipna:
                    mjuwi__ljovr = arr[uhh__jooah]
                    ckfwo__kdm = 1
                rqlw__zbw += mjuwi__ljovr
                vdfm__evg += ckfwo__kdm
            nhc__cjpak = bodo.hiframes.series_kernels._var_handle_mincount(
                rqlw__zbw, vdfm__evg, min_count)
            return nhc__cjpak
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = jedi__otwcn
            kua__yczn = len(arr)
            for uhh__jooah in numba.parfors.parfor.internal_prange(kua__yczn):
                mjuwi__ljovr = jedi__otwcn
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = arr[uhh__jooah]
                rqlw__zbw += mjuwi__ljovr
            return rqlw__zbw
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    jnvvr__mlgib = arr.dtype(1)
    if arr.dtype == types.bool_:
        jnvvr__mlgib = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = jnvvr__mlgib
            vdfm__evg = 0
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = jnvvr__mlgib
                ckfwo__kdm = 0
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah
                    ) or not skipna:
                    mjuwi__ljovr = arr[uhh__jooah]
                    ckfwo__kdm = 1
                vdfm__evg += ckfwo__kdm
                rqlw__zbw *= mjuwi__ljovr
            nhc__cjpak = bodo.hiframes.series_kernels._var_handle_mincount(
                rqlw__zbw, vdfm__evg, min_count)
            return nhc__cjpak
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            rqlw__zbw = jnvvr__mlgib
            for uhh__jooah in numba.parfors.parfor.internal_prange(len(arr)):
                mjuwi__ljovr = jnvvr__mlgib
                if not bodo.libs.array_kernels.isna(arr, uhh__jooah):
                    mjuwi__ljovr = arr[uhh__jooah]
                rqlw__zbw *= mjuwi__ljovr
            return rqlw__zbw
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        uhh__jooah = bodo.libs.array_kernels._nan_argmax(arr)
        return index[uhh__jooah]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        uhh__jooah = bodo.libs.array_kernels._nan_argmin(arr)
        return index[uhh__jooah]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            wvus__psgiq = {}
            for toma__pjmf in values:
                wvus__psgiq[bodo.utils.conversion.box_if_dt64(toma__pjmf)] = 0
            return wvus__psgiq
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
        kua__yczn = len(arr)
        owgf__qlgsf = np.empty(kua__yczn, np.bool_)
        for uhh__jooah in numba.parfors.parfor.internal_prange(kua__yczn):
            owgf__qlgsf[uhh__jooah] = bodo.utils.conversion.box_if_dt64(arr
                [uhh__jooah]) in values
        return owgf__qlgsf
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    qsm__qmp = len(in_arr_tup) != 1
    jvuay__mxjy = list(in_arr_tup.types)
    xbgdb__otg = 'def impl(in_arr_tup):\n'
    xbgdb__otg += '  n = len(in_arr_tup[0])\n'
    if qsm__qmp:
        ton__ewo = ', '.join([f'in_arr_tup[{uhh__jooah}][unused]' for
            uhh__jooah in range(len(in_arr_tup))])
        vquj__xhn = ', '.join(['False' for qva__hyjdp in range(len(
            in_arr_tup))])
        xbgdb__otg += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({ton__ewo},), ({vquj__xhn},)): 0 for unused in range(0)}}
"""
        xbgdb__otg += '  map_vector = np.empty(n, np.int64)\n'
        for uhh__jooah, esl__cibd in enumerate(jvuay__mxjy):
            xbgdb__otg += f'  in_lst_{uhh__jooah} = []\n'
            if is_str_arr_type(esl__cibd):
                xbgdb__otg += f'  total_len_{uhh__jooah} = 0\n'
            xbgdb__otg += f'  null_in_lst_{uhh__jooah} = []\n'
        xbgdb__otg += '  for i in range(n):\n'
        xqqgz__xhqok = ', '.join([f'in_arr_tup[{uhh__jooah}][i]' for
            uhh__jooah in range(len(jvuay__mxjy))])
        afmfu__eirjl = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{uhh__jooah}], i)' for
            uhh__jooah in range(len(jvuay__mxjy))])
        xbgdb__otg += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({xqqgz__xhqok},), ({afmfu__eirjl},))
"""
        xbgdb__otg += '    if data_val not in arr_map:\n'
        xbgdb__otg += '      set_val = len(arr_map)\n'
        xbgdb__otg += '      values_tup = data_val._data\n'
        xbgdb__otg += '      nulls_tup = data_val._null_values\n'
        for uhh__jooah, esl__cibd in enumerate(jvuay__mxjy):
            xbgdb__otg += (
                f'      in_lst_{uhh__jooah}.append(values_tup[{uhh__jooah}])\n'
                )
            xbgdb__otg += (
                f'      null_in_lst_{uhh__jooah}.append(nulls_tup[{uhh__jooah}])\n'
                )
            if is_str_arr_type(esl__cibd):
                xbgdb__otg += f"""      total_len_{uhh__jooah}  += nulls_tup[{uhh__jooah}] * bodo.libs.str_arr_ext.get_utf8_size(values_tup[{uhh__jooah}])
"""
        xbgdb__otg += '      arr_map[data_val] = len(arr_map)\n'
        xbgdb__otg += '    else:\n'
        xbgdb__otg += '      set_val = arr_map[data_val]\n'
        xbgdb__otg += '    map_vector[i] = set_val\n'
        xbgdb__otg += '  n_rows = len(arr_map)\n'
        for uhh__jooah, esl__cibd in enumerate(jvuay__mxjy):
            if is_str_arr_type(esl__cibd):
                xbgdb__otg += f"""  out_arr_{uhh__jooah} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{uhh__jooah})
"""
            else:
                xbgdb__otg += f"""  out_arr_{uhh__jooah} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{uhh__jooah}], (-1,))
"""
        xbgdb__otg += '  for j in range(len(arr_map)):\n'
        for uhh__jooah in range(len(jvuay__mxjy)):
            xbgdb__otg += f'    if null_in_lst_{uhh__jooah}[j]:\n'
            xbgdb__otg += (
                f'      bodo.libs.array_kernels.setna(out_arr_{uhh__jooah}, j)\n'
                )
            xbgdb__otg += '    else:\n'
            xbgdb__otg += (
                f'      out_arr_{uhh__jooah}[j] = in_lst_{uhh__jooah}[j]\n')
        lcnw__yxb = ', '.join([f'out_arr_{uhh__jooah}' for uhh__jooah in
            range(len(jvuay__mxjy))])
        xbgdb__otg += f'  return ({lcnw__yxb},), map_vector\n'
    else:
        xbgdb__otg += '  in_arr = in_arr_tup[0]\n'
        xbgdb__otg += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        xbgdb__otg += '  map_vector = np.empty(n, np.int64)\n'
        xbgdb__otg += '  is_na = 0\n'
        xbgdb__otg += '  in_lst = []\n'
        if is_str_arr_type(jvuay__mxjy[0]):
            xbgdb__otg += '  total_len = 0\n'
        xbgdb__otg += '  for i in range(n):\n'
        xbgdb__otg += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        xbgdb__otg += '      is_na = 1\n'
        xbgdb__otg += (
            '      # Always put NA in the last location. We can safely use\n')
        xbgdb__otg += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        xbgdb__otg += '      set_val = -1\n'
        xbgdb__otg += '    else:\n'
        xbgdb__otg += '      data_val = in_arr[i]\n'
        xbgdb__otg += '      if data_val not in arr_map:\n'
        xbgdb__otg += '        set_val = len(arr_map)\n'
        xbgdb__otg += '        in_lst.append(data_val)\n'
        if is_str_arr_type(jvuay__mxjy[0]):
            xbgdb__otg += (
                '        total_len += bodo.libs.str_arr_ext.get_utf8_size(data_val)\n'
                )
        xbgdb__otg += '        arr_map[data_val] = len(arr_map)\n'
        xbgdb__otg += '      else:\n'
        xbgdb__otg += '        set_val = arr_map[data_val]\n'
        xbgdb__otg += '    map_vector[i] = set_val\n'
        xbgdb__otg += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(jvuay__mxjy[0]):
            xbgdb__otg += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            xbgdb__otg += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        xbgdb__otg += '  for j in range(len(arr_map)):\n'
        xbgdb__otg += '    out_arr[j] = in_lst[j]\n'
        xbgdb__otg += '  if is_na:\n'
        xbgdb__otg += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        xbgdb__otg += f'  return (out_arr,), map_vector\n'
    pcwyo__mwga = {}
    exec(xbgdb__otg, {'bodo': bodo, 'np': np}, pcwyo__mwga)
    impl = pcwyo__mwga['impl']
    return impl
