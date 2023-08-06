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
    ujfo__twgox = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(ujfo__twgox.ctypes,
        arr, parallel, skipna)
    return ujfo__twgox[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ridcy__dqrv = len(arr)
        qdx__ustq = np.empty(ridcy__dqrv, np.bool_)
        for azujx__fuq in numba.parfors.parfor.internal_prange(ridcy__dqrv):
            qdx__ustq[azujx__fuq] = bodo.libs.array_kernels.isna(arr,
                azujx__fuq)
        return qdx__ustq
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jva__moig = 0
        for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
            bjix__zcb = 0
            if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                bjix__zcb = 1
            jva__moig += bjix__zcb
        ujfo__twgox = jva__moig
        return ujfo__twgox
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    tqn__bwxj = array_op_count(arr)
    luwxn__mfh = array_op_min(arr)
    imxj__qsdgf = array_op_max(arr)
    jljia__usn = array_op_mean(arr)
    ekav__bju = array_op_std(arr)
    bacb__bwmw = array_op_quantile(arr, 0.25)
    chez__yaqu = array_op_quantile(arr, 0.5)
    mjva__povw = array_op_quantile(arr, 0.75)
    return (tqn__bwxj, jljia__usn, ekav__bju, luwxn__mfh, bacb__bwmw,
        chez__yaqu, mjva__povw, imxj__qsdgf)


def array_op_describe_dt_impl(arr):
    tqn__bwxj = array_op_count(arr)
    luwxn__mfh = array_op_min(arr)
    imxj__qsdgf = array_op_max(arr)
    jljia__usn = array_op_mean(arr)
    bacb__bwmw = array_op_quantile(arr, 0.25)
    chez__yaqu = array_op_quantile(arr, 0.5)
    mjva__povw = array_op_quantile(arr, 0.75)
    return (tqn__bwxj, jljia__usn, luwxn__mfh, bacb__bwmw, chez__yaqu,
        mjva__povw, imxj__qsdgf)


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
            dqv__qlxy = numba.cpython.builtins.get_type_max_value(np.int64)
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dqv__qlxy
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[azujx__fuq]))
                    bjix__zcb = 1
                dqv__qlxy = min(dqv__qlxy, qnub__yzdfe)
                jva__moig += bjix__zcb
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(dqv__qlxy,
                jva__moig)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = numba.cpython.builtins.get_type_max_value(np.int64)
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dqv__qlxy
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[azujx__fuq]))
                    bjix__zcb = 1
                dqv__qlxy = min(dqv__qlxy, qnub__yzdfe)
                jva__moig += bjix__zcb
            return bodo.hiframes.pd_index_ext._dti_val_finalize(dqv__qlxy,
                jva__moig)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            emtwx__tfeps = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            dqv__qlxy = numba.cpython.builtins.get_type_max_value(np.int64)
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(
                emtwx__tfeps)):
                sayh__rdwt = emtwx__tfeps[azujx__fuq]
                if sayh__rdwt == -1:
                    continue
                dqv__qlxy = min(dqv__qlxy, sayh__rdwt)
                jva__moig += 1
            ujfo__twgox = bodo.hiframes.series_kernels._box_cat_val(dqv__qlxy,
                arr.dtype, jva__moig)
            return ujfo__twgox
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = bodo.hiframes.series_kernels._get_date_max_value()
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dqv__qlxy
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = arr[azujx__fuq]
                    bjix__zcb = 1
                dqv__qlxy = min(dqv__qlxy, qnub__yzdfe)
                jva__moig += bjix__zcb
            ujfo__twgox = bodo.hiframes.series_kernels._sum_handle_nan(
                dqv__qlxy, jva__moig)
            return ujfo__twgox
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dqv__qlxy = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype)
        jva__moig = 0
        for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
            qnub__yzdfe = dqv__qlxy
            bjix__zcb = 0
            if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                qnub__yzdfe = arr[azujx__fuq]
                bjix__zcb = 1
            dqv__qlxy = min(dqv__qlxy, qnub__yzdfe)
            jva__moig += bjix__zcb
        ujfo__twgox = bodo.hiframes.series_kernels._sum_handle_nan(dqv__qlxy,
            jva__moig)
        return ujfo__twgox
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = numba.cpython.builtins.get_type_min_value(np.int64)
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dqv__qlxy
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[azujx__fuq]))
                    bjix__zcb = 1
                dqv__qlxy = max(dqv__qlxy, qnub__yzdfe)
                jva__moig += bjix__zcb
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(dqv__qlxy,
                jva__moig)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = numba.cpython.builtins.get_type_min_value(np.int64)
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dqv__qlxy
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[azujx__fuq]))
                    bjix__zcb = 1
                dqv__qlxy = max(dqv__qlxy, qnub__yzdfe)
                jva__moig += bjix__zcb
            return bodo.hiframes.pd_index_ext._dti_val_finalize(dqv__qlxy,
                jva__moig)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            emtwx__tfeps = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            dqv__qlxy = -1
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(
                emtwx__tfeps)):
                dqv__qlxy = max(dqv__qlxy, emtwx__tfeps[azujx__fuq])
            ujfo__twgox = bodo.hiframes.series_kernels._box_cat_val(dqv__qlxy,
                arr.dtype, 1)
            return ujfo__twgox
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = bodo.hiframes.series_kernels._get_date_min_value()
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dqv__qlxy
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = arr[azujx__fuq]
                    bjix__zcb = 1
                dqv__qlxy = max(dqv__qlxy, qnub__yzdfe)
                jva__moig += bjix__zcb
            ujfo__twgox = bodo.hiframes.series_kernels._sum_handle_nan(
                dqv__qlxy, jva__moig)
            return ujfo__twgox
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dqv__qlxy = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype)
        jva__moig = 0
        for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
            qnub__yzdfe = dqv__qlxy
            bjix__zcb = 0
            if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                qnub__yzdfe = arr[azujx__fuq]
                bjix__zcb = 1
            dqv__qlxy = max(dqv__qlxy, qnub__yzdfe)
            jva__moig += bjix__zcb
        ujfo__twgox = bodo.hiframes.series_kernels._sum_handle_nan(dqv__qlxy,
            jva__moig)
        return ujfo__twgox
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
    mbzkx__fwd = types.float64
    xjau__remjr = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        mbzkx__fwd = types.float32
        xjau__remjr = types.float32
    jmmbz__ovskz = mbzkx__fwd(0)
    eum__sxmgi = xjau__remjr(0)
    dsj__namel = xjau__remjr(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dqv__qlxy = jmmbz__ovskz
        jva__moig = eum__sxmgi
        for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
            qnub__yzdfe = jmmbz__ovskz
            bjix__zcb = eum__sxmgi
            if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                qnub__yzdfe = arr[azujx__fuq]
                bjix__zcb = dsj__namel
            dqv__qlxy += qnub__yzdfe
            jva__moig += bjix__zcb
        ujfo__twgox = bodo.hiframes.series_kernels._mean_handle_nan(dqv__qlxy,
            jva__moig)
        return ujfo__twgox
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        rvjt__ompk = 0.0
        vanrv__pzfsj = 0.0
        jva__moig = 0
        for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
            qnub__yzdfe = 0.0
            bjix__zcb = 0
            if not bodo.libs.array_kernels.isna(arr, azujx__fuq) or not skipna:
                qnub__yzdfe = arr[azujx__fuq]
                bjix__zcb = 1
            rvjt__ompk += qnub__yzdfe
            vanrv__pzfsj += qnub__yzdfe * qnub__yzdfe
            jva__moig += bjix__zcb
        ujfo__twgox = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            rvjt__ompk, vanrv__pzfsj, jva__moig, ddof)
        return ujfo__twgox
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
                qdx__ustq = np.empty(len(q), np.int64)
                for azujx__fuq in range(len(q)):
                    mkds__qlyem = np.float64(q[azujx__fuq])
                    qdx__ustq[azujx__fuq] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), mkds__qlyem)
                return qdx__ustq.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            qdx__ustq = np.empty(len(q), np.float64)
            for azujx__fuq in range(len(q)):
                mkds__qlyem = np.float64(q[azujx__fuq])
                qdx__ustq[azujx__fuq] = bodo.libs.array_kernels.quantile(arr,
                    mkds__qlyem)
            return qdx__ustq
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
        rsrsg__yufts = types.intp
    elif arr.dtype == types.bool_:
        rsrsg__yufts = np.int64
    else:
        rsrsg__yufts = arr.dtype
    wpnj__yqxzt = rsrsg__yufts(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = wpnj__yqxzt
            ridcy__dqrv = len(arr)
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(ridcy__dqrv
                ):
                qnub__yzdfe = wpnj__yqxzt
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq
                    ) or not skipna:
                    qnub__yzdfe = arr[azujx__fuq]
                    bjix__zcb = 1
                dqv__qlxy += qnub__yzdfe
                jva__moig += bjix__zcb
            ujfo__twgox = bodo.hiframes.series_kernels._var_handle_mincount(
                dqv__qlxy, jva__moig, min_count)
            return ujfo__twgox
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = wpnj__yqxzt
            ridcy__dqrv = len(arr)
            for azujx__fuq in numba.parfors.parfor.internal_prange(ridcy__dqrv
                ):
                qnub__yzdfe = wpnj__yqxzt
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = arr[azujx__fuq]
                dqv__qlxy += qnub__yzdfe
            return dqv__qlxy
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    dmng__jbm = arr.dtype(1)
    if arr.dtype == types.bool_:
        dmng__jbm = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = dmng__jbm
            jva__moig = 0
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dmng__jbm
                bjix__zcb = 0
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq
                    ) or not skipna:
                    qnub__yzdfe = arr[azujx__fuq]
                    bjix__zcb = 1
                jva__moig += bjix__zcb
                dqv__qlxy *= qnub__yzdfe
            ujfo__twgox = bodo.hiframes.series_kernels._var_handle_mincount(
                dqv__qlxy, jva__moig, min_count)
            return ujfo__twgox
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqv__qlxy = dmng__jbm
            for azujx__fuq in numba.parfors.parfor.internal_prange(len(arr)):
                qnub__yzdfe = dmng__jbm
                if not bodo.libs.array_kernels.isna(arr, azujx__fuq):
                    qnub__yzdfe = arr[azujx__fuq]
                dqv__qlxy *= qnub__yzdfe
            return dqv__qlxy
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        azujx__fuq = bodo.libs.array_kernels._nan_argmax(arr)
        return index[azujx__fuq]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        azujx__fuq = bodo.libs.array_kernels._nan_argmin(arr)
        return index[azujx__fuq]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            uza__jrb = {}
            for flq__vtz in values:
                uza__jrb[bodo.utils.conversion.box_if_dt64(flq__vtz)] = 0
            return uza__jrb
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
        ridcy__dqrv = len(arr)
        qdx__ustq = np.empty(ridcy__dqrv, np.bool_)
        for azujx__fuq in numba.parfors.parfor.internal_prange(ridcy__dqrv):
            qdx__ustq[azujx__fuq] = bodo.utils.conversion.box_if_dt64(arr[
                azujx__fuq]) in values
        return qdx__ustq
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    tghsi__aela = len(in_arr_tup) != 1
    lhx__wwbk = list(in_arr_tup.types)
    mis__lyymj = 'def impl(in_arr_tup):\n'
    mis__lyymj += '  n = len(in_arr_tup[0])\n'
    if tghsi__aela:
        pzo__esz = ', '.join([f'in_arr_tup[{azujx__fuq}][unused]' for
            azujx__fuq in range(len(in_arr_tup))])
        ucxks__uzfle = ', '.join(['False' for regg__zpj in range(len(
            in_arr_tup))])
        mis__lyymj += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({pzo__esz},), ({ucxks__uzfle},)): 0 for unused in range(0)}}
"""
        mis__lyymj += '  map_vector = np.empty(n, np.int64)\n'
        for azujx__fuq, xqrdf__zyx in enumerate(lhx__wwbk):
            mis__lyymj += f'  in_lst_{azujx__fuq} = []\n'
            if is_str_arr_type(xqrdf__zyx):
                mis__lyymj += f'  total_len_{azujx__fuq} = 0\n'
            mis__lyymj += f'  null_in_lst_{azujx__fuq} = []\n'
        mis__lyymj += '  for i in range(n):\n'
        sqrgi__etzj = ', '.join([f'in_arr_tup[{azujx__fuq}][i]' for
            azujx__fuq in range(len(lhx__wwbk))])
        wus__lrw = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{azujx__fuq}], i)' for
            azujx__fuq in range(len(lhx__wwbk))])
        mis__lyymj += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({sqrgi__etzj},), ({wus__lrw},))
"""
        mis__lyymj += '    if data_val not in arr_map:\n'
        mis__lyymj += '      set_val = len(arr_map)\n'
        mis__lyymj += '      values_tup = data_val._data\n'
        mis__lyymj += '      nulls_tup = data_val._null_values\n'
        for azujx__fuq, xqrdf__zyx in enumerate(lhx__wwbk):
            mis__lyymj += (
                f'      in_lst_{azujx__fuq}.append(values_tup[{azujx__fuq}])\n'
                )
            mis__lyymj += (
                f'      null_in_lst_{azujx__fuq}.append(nulls_tup[{azujx__fuq}])\n'
                )
            if is_str_arr_type(xqrdf__zyx):
                mis__lyymj += f"""      total_len_{azujx__fuq}  += nulls_tup[{azujx__fuq}] * bodo.libs.str_arr_ext.get_utf8_size(values_tup[{azujx__fuq}])
"""
        mis__lyymj += '      arr_map[data_val] = len(arr_map)\n'
        mis__lyymj += '    else:\n'
        mis__lyymj += '      set_val = arr_map[data_val]\n'
        mis__lyymj += '    map_vector[i] = set_val\n'
        mis__lyymj += '  n_rows = len(arr_map)\n'
        for azujx__fuq, xqrdf__zyx in enumerate(lhx__wwbk):
            if is_str_arr_type(xqrdf__zyx):
                mis__lyymj += f"""  out_arr_{azujx__fuq} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{azujx__fuq})
"""
            else:
                mis__lyymj += f"""  out_arr_{azujx__fuq} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{azujx__fuq}], (-1,))
"""
        mis__lyymj += '  for j in range(len(arr_map)):\n'
        for azujx__fuq in range(len(lhx__wwbk)):
            mis__lyymj += f'    if null_in_lst_{azujx__fuq}[j]:\n'
            mis__lyymj += (
                f'      bodo.libs.array_kernels.setna(out_arr_{azujx__fuq}, j)\n'
                )
            mis__lyymj += '    else:\n'
            mis__lyymj += (
                f'      out_arr_{azujx__fuq}[j] = in_lst_{azujx__fuq}[j]\n')
        bbx__dbxem = ', '.join([f'out_arr_{azujx__fuq}' for azujx__fuq in
            range(len(lhx__wwbk))])
        mis__lyymj += f'  return ({bbx__dbxem},), map_vector\n'
    else:
        mis__lyymj += '  in_arr = in_arr_tup[0]\n'
        mis__lyymj += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        mis__lyymj += '  map_vector = np.empty(n, np.int64)\n'
        mis__lyymj += '  is_na = 0\n'
        mis__lyymj += '  in_lst = []\n'
        if is_str_arr_type(lhx__wwbk[0]):
            mis__lyymj += '  total_len = 0\n'
        mis__lyymj += '  for i in range(n):\n'
        mis__lyymj += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        mis__lyymj += '      is_na = 1\n'
        mis__lyymj += (
            '      # Always put NA in the last location. We can safely use\n')
        mis__lyymj += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        mis__lyymj += '      set_val = -1\n'
        mis__lyymj += '    else:\n'
        mis__lyymj += '      data_val = in_arr[i]\n'
        mis__lyymj += '      if data_val not in arr_map:\n'
        mis__lyymj += '        set_val = len(arr_map)\n'
        mis__lyymj += '        in_lst.append(data_val)\n'
        if is_str_arr_type(lhx__wwbk[0]):
            mis__lyymj += (
                '        total_len += bodo.libs.str_arr_ext.get_utf8_size(data_val)\n'
                )
        mis__lyymj += '        arr_map[data_val] = len(arr_map)\n'
        mis__lyymj += '      else:\n'
        mis__lyymj += '        set_val = arr_map[data_val]\n'
        mis__lyymj += '    map_vector[i] = set_val\n'
        mis__lyymj += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(lhx__wwbk[0]):
            mis__lyymj += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            mis__lyymj += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        mis__lyymj += '  for j in range(len(arr_map)):\n'
        mis__lyymj += '    out_arr[j] = in_lst[j]\n'
        mis__lyymj += '  if is_na:\n'
        mis__lyymj += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        mis__lyymj += f'  return (out_arr,), map_vector\n'
    uhx__klbgb = {}
    exec(mis__lyymj, {'bodo': bodo, 'np': np}, uhx__klbgb)
    impl = uhx__klbgb['impl']
    return impl
