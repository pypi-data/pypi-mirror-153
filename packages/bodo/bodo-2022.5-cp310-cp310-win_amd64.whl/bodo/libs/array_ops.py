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
    ucjah__bls = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(ucjah__bls.ctypes,
        arr, parallel, skipna)
    return ucjah__bls[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ppj__kill = len(arr)
        avp__gjb = np.empty(ppj__kill, np.bool_)
        for nngz__xykoy in numba.parfors.parfor.internal_prange(ppj__kill):
            avp__gjb[nngz__xykoy] = bodo.libs.array_kernels.isna(arr,
                nngz__xykoy)
        return avp__gjb
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        eomtf__uxgj = 0
        for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
            dlmu__ooqyo = 0
            if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                dlmu__ooqyo = 1
            eomtf__uxgj += dlmu__ooqyo
        ucjah__bls = eomtf__uxgj
        return ucjah__bls
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    upbo__idb = array_op_count(arr)
    zkdrd__oaq = array_op_min(arr)
    esyyz__dxhan = array_op_max(arr)
    sbkwi__ujlye = array_op_mean(arr)
    fjbgl__ozb = array_op_std(arr)
    ipzp__ofdc = array_op_quantile(arr, 0.25)
    wpky__rqu = array_op_quantile(arr, 0.5)
    efq__lpgbz = array_op_quantile(arr, 0.75)
    return (upbo__idb, sbkwi__ujlye, fjbgl__ozb, zkdrd__oaq, ipzp__ofdc,
        wpky__rqu, efq__lpgbz, esyyz__dxhan)


def array_op_describe_dt_impl(arr):
    upbo__idb = array_op_count(arr)
    zkdrd__oaq = array_op_min(arr)
    esyyz__dxhan = array_op_max(arr)
    sbkwi__ujlye = array_op_mean(arr)
    ipzp__ofdc = array_op_quantile(arr, 0.25)
    wpky__rqu = array_op_quantile(arr, 0.5)
    efq__lpgbz = array_op_quantile(arr, 0.75)
    return (upbo__idb, sbkwi__ujlye, zkdrd__oaq, ipzp__ofdc, wpky__rqu,
        efq__lpgbz, esyyz__dxhan)


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
            vjuj__hyez = numba.cpython.builtins.get_type_max_value(np.int64)
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = vjuj__hyez
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[nngz__xykoy]))
                    dlmu__ooqyo = 1
                vjuj__hyez = min(vjuj__hyez, nzqon__laee)
                eomtf__uxgj += dlmu__ooqyo
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(vjuj__hyez,
                eomtf__uxgj)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = numba.cpython.builtins.get_type_max_value(np.int64)
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = vjuj__hyez
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[nngz__xykoy]))
                    dlmu__ooqyo = 1
                vjuj__hyez = min(vjuj__hyez, nzqon__laee)
                eomtf__uxgj += dlmu__ooqyo
            return bodo.hiframes.pd_index_ext._dti_val_finalize(vjuj__hyez,
                eomtf__uxgj)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            lxv__bmfw = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            vjuj__hyez = numba.cpython.builtins.get_type_max_value(np.int64)
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(
                lxv__bmfw)):
                opr__dmh = lxv__bmfw[nngz__xykoy]
                if opr__dmh == -1:
                    continue
                vjuj__hyez = min(vjuj__hyez, opr__dmh)
                eomtf__uxgj += 1
            ucjah__bls = bodo.hiframes.series_kernels._box_cat_val(vjuj__hyez,
                arr.dtype, eomtf__uxgj)
            return ucjah__bls
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = bodo.hiframes.series_kernels._get_date_max_value()
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = vjuj__hyez
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = arr[nngz__xykoy]
                    dlmu__ooqyo = 1
                vjuj__hyez = min(vjuj__hyez, nzqon__laee)
                eomtf__uxgj += dlmu__ooqyo
            ucjah__bls = bodo.hiframes.series_kernels._sum_handle_nan(
                vjuj__hyez, eomtf__uxgj)
            return ucjah__bls
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        vjuj__hyez = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        eomtf__uxgj = 0
        for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
            nzqon__laee = vjuj__hyez
            dlmu__ooqyo = 0
            if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                nzqon__laee = arr[nngz__xykoy]
                dlmu__ooqyo = 1
            vjuj__hyez = min(vjuj__hyez, nzqon__laee)
            eomtf__uxgj += dlmu__ooqyo
        ucjah__bls = bodo.hiframes.series_kernels._sum_handle_nan(vjuj__hyez,
            eomtf__uxgj)
        return ucjah__bls
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = numba.cpython.builtins.get_type_min_value(np.int64)
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = vjuj__hyez
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[nngz__xykoy]))
                    dlmu__ooqyo = 1
                vjuj__hyez = max(vjuj__hyez, nzqon__laee)
                eomtf__uxgj += dlmu__ooqyo
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(vjuj__hyez,
                eomtf__uxgj)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = numba.cpython.builtins.get_type_min_value(np.int64)
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = vjuj__hyez
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[nngz__xykoy]))
                    dlmu__ooqyo = 1
                vjuj__hyez = max(vjuj__hyez, nzqon__laee)
                eomtf__uxgj += dlmu__ooqyo
            return bodo.hiframes.pd_index_ext._dti_val_finalize(vjuj__hyez,
                eomtf__uxgj)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            lxv__bmfw = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            vjuj__hyez = -1
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(
                lxv__bmfw)):
                vjuj__hyez = max(vjuj__hyez, lxv__bmfw[nngz__xykoy])
            ucjah__bls = bodo.hiframes.series_kernels._box_cat_val(vjuj__hyez,
                arr.dtype, 1)
            return ucjah__bls
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = bodo.hiframes.series_kernels._get_date_min_value()
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = vjuj__hyez
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = arr[nngz__xykoy]
                    dlmu__ooqyo = 1
                vjuj__hyez = max(vjuj__hyez, nzqon__laee)
                eomtf__uxgj += dlmu__ooqyo
            ucjah__bls = bodo.hiframes.series_kernels._sum_handle_nan(
                vjuj__hyez, eomtf__uxgj)
            return ucjah__bls
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        vjuj__hyez = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        eomtf__uxgj = 0
        for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
            nzqon__laee = vjuj__hyez
            dlmu__ooqyo = 0
            if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                nzqon__laee = arr[nngz__xykoy]
                dlmu__ooqyo = 1
            vjuj__hyez = max(vjuj__hyez, nzqon__laee)
            eomtf__uxgj += dlmu__ooqyo
        ucjah__bls = bodo.hiframes.series_kernels._sum_handle_nan(vjuj__hyez,
            eomtf__uxgj)
        return ucjah__bls
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
    dcj__msaav = types.float64
    luoy__rpzso = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        dcj__msaav = types.float32
        luoy__rpzso = types.float32
    rkid__yfiy = dcj__msaav(0)
    esjo__qjy = luoy__rpzso(0)
    mgepd__bmf = luoy__rpzso(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        vjuj__hyez = rkid__yfiy
        eomtf__uxgj = esjo__qjy
        for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
            nzqon__laee = rkid__yfiy
            dlmu__ooqyo = esjo__qjy
            if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                nzqon__laee = arr[nngz__xykoy]
                dlmu__ooqyo = mgepd__bmf
            vjuj__hyez += nzqon__laee
            eomtf__uxgj += dlmu__ooqyo
        ucjah__bls = bodo.hiframes.series_kernels._mean_handle_nan(vjuj__hyez,
            eomtf__uxgj)
        return ucjah__bls
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        alev__eohcz = 0.0
        nrzv__vbwg = 0.0
        eomtf__uxgj = 0
        for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
            nzqon__laee = 0.0
            dlmu__ooqyo = 0
            if not bodo.libs.array_kernels.isna(arr, nngz__xykoy
                ) or not skipna:
                nzqon__laee = arr[nngz__xykoy]
                dlmu__ooqyo = 1
            alev__eohcz += nzqon__laee
            nrzv__vbwg += nzqon__laee * nzqon__laee
            eomtf__uxgj += dlmu__ooqyo
        ucjah__bls = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            alev__eohcz, nrzv__vbwg, eomtf__uxgj, ddof)
        return ucjah__bls
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
                avp__gjb = np.empty(len(q), np.int64)
                for nngz__xykoy in range(len(q)):
                    bca__cpwd = np.float64(q[nngz__xykoy])
                    avp__gjb[nngz__xykoy] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), bca__cpwd)
                return avp__gjb.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            avp__gjb = np.empty(len(q), np.float64)
            for nngz__xykoy in range(len(q)):
                bca__cpwd = np.float64(q[nngz__xykoy])
                avp__gjb[nngz__xykoy] = bodo.libs.array_kernels.quantile(arr,
                    bca__cpwd)
            return avp__gjb
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
        ovaey__ypwx = types.intp
    elif arr.dtype == types.bool_:
        ovaey__ypwx = np.int64
    else:
        ovaey__ypwx = arr.dtype
    toyb__atqd = ovaey__ypwx(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = toyb__atqd
            ppj__kill = len(arr)
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(ppj__kill):
                nzqon__laee = toyb__atqd
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy
                    ) or not skipna:
                    nzqon__laee = arr[nngz__xykoy]
                    dlmu__ooqyo = 1
                vjuj__hyez += nzqon__laee
                eomtf__uxgj += dlmu__ooqyo
            ucjah__bls = bodo.hiframes.series_kernels._var_handle_mincount(
                vjuj__hyez, eomtf__uxgj, min_count)
            return ucjah__bls
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = toyb__atqd
            ppj__kill = len(arr)
            for nngz__xykoy in numba.parfors.parfor.internal_prange(ppj__kill):
                nzqon__laee = toyb__atqd
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = arr[nngz__xykoy]
                vjuj__hyez += nzqon__laee
            return vjuj__hyez
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    qdc__icvdj = arr.dtype(1)
    if arr.dtype == types.bool_:
        qdc__icvdj = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = qdc__icvdj
            eomtf__uxgj = 0
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = qdc__icvdj
                dlmu__ooqyo = 0
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy
                    ) or not skipna:
                    nzqon__laee = arr[nngz__xykoy]
                    dlmu__ooqyo = 1
                eomtf__uxgj += dlmu__ooqyo
                vjuj__hyez *= nzqon__laee
            ucjah__bls = bodo.hiframes.series_kernels._var_handle_mincount(
                vjuj__hyez, eomtf__uxgj, min_count)
            return ucjah__bls
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            vjuj__hyez = qdc__icvdj
            for nngz__xykoy in numba.parfors.parfor.internal_prange(len(arr)):
                nzqon__laee = qdc__icvdj
                if not bodo.libs.array_kernels.isna(arr, nngz__xykoy):
                    nzqon__laee = arr[nngz__xykoy]
                vjuj__hyez *= nzqon__laee
            return vjuj__hyez
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        nngz__xykoy = bodo.libs.array_kernels._nan_argmax(arr)
        return index[nngz__xykoy]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        nngz__xykoy = bodo.libs.array_kernels._nan_argmin(arr)
        return index[nngz__xykoy]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            qyqwv__esh = {}
            for dqse__jhuwy in values:
                qyqwv__esh[bodo.utils.conversion.box_if_dt64(dqse__jhuwy)] = 0
            return qyqwv__esh
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
        ppj__kill = len(arr)
        avp__gjb = np.empty(ppj__kill, np.bool_)
        for nngz__xykoy in numba.parfors.parfor.internal_prange(ppj__kill):
            avp__gjb[nngz__xykoy] = bodo.utils.conversion.box_if_dt64(arr[
                nngz__xykoy]) in values
        return avp__gjb
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    gme__pzllh = len(in_arr_tup) != 1
    dzng__vuzbd = list(in_arr_tup.types)
    uxtae__rknm = 'def impl(in_arr_tup):\n'
    uxtae__rknm += '  n = len(in_arr_tup[0])\n'
    if gme__pzllh:
        nsu__sak = ', '.join([f'in_arr_tup[{nngz__xykoy}][unused]' for
            nngz__xykoy in range(len(in_arr_tup))])
        haoq__cfu = ', '.join(['False' for fot__wxu in range(len(in_arr_tup))])
        uxtae__rknm += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({nsu__sak},), ({haoq__cfu},)): 0 for unused in range(0)}}
"""
        uxtae__rknm += '  map_vector = np.empty(n, np.int64)\n'
        for nngz__xykoy, mbi__hvz in enumerate(dzng__vuzbd):
            uxtae__rknm += f'  in_lst_{nngz__xykoy} = []\n'
            if is_str_arr_type(mbi__hvz):
                uxtae__rknm += f'  total_len_{nngz__xykoy} = 0\n'
            uxtae__rknm += f'  null_in_lst_{nngz__xykoy} = []\n'
        uxtae__rknm += '  for i in range(n):\n'
        ftlh__mivh = ', '.join([f'in_arr_tup[{nngz__xykoy}][i]' for
            nngz__xykoy in range(len(dzng__vuzbd))])
        ooxzn__cuceh = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{nngz__xykoy}], i)' for
            nngz__xykoy in range(len(dzng__vuzbd))])
        uxtae__rknm += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({ftlh__mivh},), ({ooxzn__cuceh},))
"""
        uxtae__rknm += '    if data_val not in arr_map:\n'
        uxtae__rknm += '      set_val = len(arr_map)\n'
        uxtae__rknm += '      values_tup = data_val._data\n'
        uxtae__rknm += '      nulls_tup = data_val._null_values\n'
        for nngz__xykoy, mbi__hvz in enumerate(dzng__vuzbd):
            uxtae__rknm += (
                f'      in_lst_{nngz__xykoy}.append(values_tup[{nngz__xykoy}])\n'
                )
            uxtae__rknm += (
                f'      null_in_lst_{nngz__xykoy}.append(nulls_tup[{nngz__xykoy}])\n'
                )
            if is_str_arr_type(mbi__hvz):
                uxtae__rknm += f"""      total_len_{nngz__xykoy}  += nulls_tup[{nngz__xykoy}] * len(values_tup[{nngz__xykoy}])
"""
        uxtae__rknm += '      arr_map[data_val] = len(arr_map)\n'
        uxtae__rknm += '    else:\n'
        uxtae__rknm += '      set_val = arr_map[data_val]\n'
        uxtae__rknm += '    map_vector[i] = set_val\n'
        uxtae__rknm += '  n_rows = len(arr_map)\n'
        for nngz__xykoy, mbi__hvz in enumerate(dzng__vuzbd):
            if is_str_arr_type(mbi__hvz):
                uxtae__rknm += f"""  out_arr_{nngz__xykoy} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{nngz__xykoy})
"""
            else:
                uxtae__rknm += f"""  out_arr_{nngz__xykoy} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{nngz__xykoy}], (-1,))
"""
        uxtae__rknm += '  for j in range(len(arr_map)):\n'
        for nngz__xykoy in range(len(dzng__vuzbd)):
            uxtae__rknm += f'    if null_in_lst_{nngz__xykoy}[j]:\n'
            uxtae__rknm += (
                f'      bodo.libs.array_kernels.setna(out_arr_{nngz__xykoy}, j)\n'
                )
            uxtae__rknm += '    else:\n'
            uxtae__rknm += (
                f'      out_arr_{nngz__xykoy}[j] = in_lst_{nngz__xykoy}[j]\n')
        yvm__ghylb = ', '.join([f'out_arr_{nngz__xykoy}' for nngz__xykoy in
            range(len(dzng__vuzbd))])
        uxtae__rknm += f'  return ({yvm__ghylb},), map_vector\n'
    else:
        uxtae__rknm += '  in_arr = in_arr_tup[0]\n'
        uxtae__rknm += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        uxtae__rknm += '  map_vector = np.empty(n, np.int64)\n'
        uxtae__rknm += '  is_na = 0\n'
        uxtae__rknm += '  in_lst = []\n'
        if is_str_arr_type(dzng__vuzbd[0]):
            uxtae__rknm += '  total_len = 0\n'
        uxtae__rknm += '  for i in range(n):\n'
        uxtae__rknm += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        uxtae__rknm += '      is_na = 1\n'
        uxtae__rknm += (
            '      # Always put NA in the last location. We can safely use\n')
        uxtae__rknm += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        uxtae__rknm += '      set_val = -1\n'
        uxtae__rknm += '    else:\n'
        uxtae__rknm += '      data_val = in_arr[i]\n'
        uxtae__rknm += '      if data_val not in arr_map:\n'
        uxtae__rknm += '        set_val = len(arr_map)\n'
        uxtae__rknm += '        in_lst.append(data_val)\n'
        if is_str_arr_type(dzng__vuzbd[0]):
            uxtae__rknm += '        total_len += len(data_val)\n'
        uxtae__rknm += '        arr_map[data_val] = len(arr_map)\n'
        uxtae__rknm += '      else:\n'
        uxtae__rknm += '        set_val = arr_map[data_val]\n'
        uxtae__rknm += '    map_vector[i] = set_val\n'
        uxtae__rknm += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(dzng__vuzbd[0]):
            uxtae__rknm += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            uxtae__rknm += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        uxtae__rknm += '  for j in range(len(arr_map)):\n'
        uxtae__rknm += '    out_arr[j] = in_lst[j]\n'
        uxtae__rknm += '  if is_na:\n'
        uxtae__rknm += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        uxtae__rknm += f'  return (out_arr,), map_vector\n'
    izr__ndu = {}
    exec(uxtae__rknm, {'bodo': bodo, 'np': np}, izr__ndu)
    impl = izr__ndu['impl']
    return impl
