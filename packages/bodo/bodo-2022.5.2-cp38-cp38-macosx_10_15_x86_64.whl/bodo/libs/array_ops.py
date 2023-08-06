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
    iclye__uhbl = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(iclye__uhbl.ctypes,
        arr, parallel, skipna)
    return iclye__uhbl[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pni__xlfjk = len(arr)
        ouf__pzk = np.empty(pni__xlfjk, np.bool_)
        for qxs__xeem in numba.parfors.parfor.internal_prange(pni__xlfjk):
            ouf__pzk[qxs__xeem] = bodo.libs.array_kernels.isna(arr, qxs__xeem)
        return ouf__pzk
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        puax__xuml = 0
        for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
            foj__bxnn = 0
            if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                foj__bxnn = 1
            puax__xuml += foj__bxnn
        iclye__uhbl = puax__xuml
        return iclye__uhbl
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    oojq__qxj = array_op_count(arr)
    pnkp__cdt = array_op_min(arr)
    ulr__wtfg = array_op_max(arr)
    sbk__yxy = array_op_mean(arr)
    teegs__pcvyn = array_op_std(arr)
    vnud__daym = array_op_quantile(arr, 0.25)
    jrgvh__jous = array_op_quantile(arr, 0.5)
    hlk__ezyg = array_op_quantile(arr, 0.75)
    return (oojq__qxj, sbk__yxy, teegs__pcvyn, pnkp__cdt, vnud__daym,
        jrgvh__jous, hlk__ezyg, ulr__wtfg)


def array_op_describe_dt_impl(arr):
    oojq__qxj = array_op_count(arr)
    pnkp__cdt = array_op_min(arr)
    ulr__wtfg = array_op_max(arr)
    sbk__yxy = array_op_mean(arr)
    vnud__daym = array_op_quantile(arr, 0.25)
    jrgvh__jous = array_op_quantile(arr, 0.5)
    hlk__ezyg = array_op_quantile(arr, 0.75)
    return (oojq__qxj, sbk__yxy, pnkp__cdt, vnud__daym, jrgvh__jous,
        hlk__ezyg, ulr__wtfg)


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
            jubm__zjwd = numba.cpython.builtins.get_type_max_value(np.int64)
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = jubm__zjwd
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[qxs__xeem]))
                    foj__bxnn = 1
                jubm__zjwd = min(jubm__zjwd, hfr__ktjo)
                puax__xuml += foj__bxnn
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(jubm__zjwd,
                puax__xuml)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = numba.cpython.builtins.get_type_max_value(np.int64)
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = jubm__zjwd
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[qxs__xeem])
                    foj__bxnn = 1
                jubm__zjwd = min(jubm__zjwd, hfr__ktjo)
                puax__xuml += foj__bxnn
            return bodo.hiframes.pd_index_ext._dti_val_finalize(jubm__zjwd,
                puax__xuml)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            bzav__gng = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            jubm__zjwd = numba.cpython.builtins.get_type_max_value(np.int64)
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(
                bzav__gng)):
                xuoux__hrhit = bzav__gng[qxs__xeem]
                if xuoux__hrhit == -1:
                    continue
                jubm__zjwd = min(jubm__zjwd, xuoux__hrhit)
                puax__xuml += 1
            iclye__uhbl = bodo.hiframes.series_kernels._box_cat_val(jubm__zjwd,
                arr.dtype, puax__xuml)
            return iclye__uhbl
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = bodo.hiframes.series_kernels._get_date_max_value()
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = jubm__zjwd
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = arr[qxs__xeem]
                    foj__bxnn = 1
                jubm__zjwd = min(jubm__zjwd, hfr__ktjo)
                puax__xuml += foj__bxnn
            iclye__uhbl = bodo.hiframes.series_kernels._sum_handle_nan(
                jubm__zjwd, puax__xuml)
            return iclye__uhbl
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jubm__zjwd = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        puax__xuml = 0
        for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
            hfr__ktjo = jubm__zjwd
            foj__bxnn = 0
            if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                hfr__ktjo = arr[qxs__xeem]
                foj__bxnn = 1
            jubm__zjwd = min(jubm__zjwd, hfr__ktjo)
            puax__xuml += foj__bxnn
        iclye__uhbl = bodo.hiframes.series_kernels._sum_handle_nan(jubm__zjwd,
            puax__xuml)
        return iclye__uhbl
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = numba.cpython.builtins.get_type_min_value(np.int64)
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = jubm__zjwd
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[qxs__xeem]))
                    foj__bxnn = 1
                jubm__zjwd = max(jubm__zjwd, hfr__ktjo)
                puax__xuml += foj__bxnn
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(jubm__zjwd,
                puax__xuml)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = numba.cpython.builtins.get_type_min_value(np.int64)
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = jubm__zjwd
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[qxs__xeem])
                    foj__bxnn = 1
                jubm__zjwd = max(jubm__zjwd, hfr__ktjo)
                puax__xuml += foj__bxnn
            return bodo.hiframes.pd_index_ext._dti_val_finalize(jubm__zjwd,
                puax__xuml)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            bzav__gng = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            jubm__zjwd = -1
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(
                bzav__gng)):
                jubm__zjwd = max(jubm__zjwd, bzav__gng[qxs__xeem])
            iclye__uhbl = bodo.hiframes.series_kernels._box_cat_val(jubm__zjwd,
                arr.dtype, 1)
            return iclye__uhbl
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = bodo.hiframes.series_kernels._get_date_min_value()
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = jubm__zjwd
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = arr[qxs__xeem]
                    foj__bxnn = 1
                jubm__zjwd = max(jubm__zjwd, hfr__ktjo)
                puax__xuml += foj__bxnn
            iclye__uhbl = bodo.hiframes.series_kernels._sum_handle_nan(
                jubm__zjwd, puax__xuml)
            return iclye__uhbl
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jubm__zjwd = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        puax__xuml = 0
        for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
            hfr__ktjo = jubm__zjwd
            foj__bxnn = 0
            if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                hfr__ktjo = arr[qxs__xeem]
                foj__bxnn = 1
            jubm__zjwd = max(jubm__zjwd, hfr__ktjo)
            puax__xuml += foj__bxnn
        iclye__uhbl = bodo.hiframes.series_kernels._sum_handle_nan(jubm__zjwd,
            puax__xuml)
        return iclye__uhbl
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
    ugsie__evcp = types.float64
    rcpxr__uywm = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        ugsie__evcp = types.float32
        rcpxr__uywm = types.float32
    sayiq__wbhkf = ugsie__evcp(0)
    opfu__hkh = rcpxr__uywm(0)
    coekp__tyn = rcpxr__uywm(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jubm__zjwd = sayiq__wbhkf
        puax__xuml = opfu__hkh
        for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
            hfr__ktjo = sayiq__wbhkf
            foj__bxnn = opfu__hkh
            if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                hfr__ktjo = arr[qxs__xeem]
                foj__bxnn = coekp__tyn
            jubm__zjwd += hfr__ktjo
            puax__xuml += foj__bxnn
        iclye__uhbl = bodo.hiframes.series_kernels._mean_handle_nan(jubm__zjwd,
            puax__xuml)
        return iclye__uhbl
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        vaytp__mjfrm = 0.0
        fgdq__kbvkh = 0.0
        puax__xuml = 0
        for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
            hfr__ktjo = 0.0
            foj__bxnn = 0
            if not bodo.libs.array_kernels.isna(arr, qxs__xeem) or not skipna:
                hfr__ktjo = arr[qxs__xeem]
                foj__bxnn = 1
            vaytp__mjfrm += hfr__ktjo
            fgdq__kbvkh += hfr__ktjo * hfr__ktjo
            puax__xuml += foj__bxnn
        iclye__uhbl = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            vaytp__mjfrm, fgdq__kbvkh, puax__xuml, ddof)
        return iclye__uhbl
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
                ouf__pzk = np.empty(len(q), np.int64)
                for qxs__xeem in range(len(q)):
                    voki__ezy = np.float64(q[qxs__xeem])
                    ouf__pzk[qxs__xeem] = bodo.libs.array_kernels.quantile(arr
                        .view(np.int64), voki__ezy)
                return ouf__pzk.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            ouf__pzk = np.empty(len(q), np.float64)
            for qxs__xeem in range(len(q)):
                voki__ezy = np.float64(q[qxs__xeem])
                ouf__pzk[qxs__xeem] = bodo.libs.array_kernels.quantile(arr,
                    voki__ezy)
            return ouf__pzk
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
        dyrr__kjge = types.intp
    elif arr.dtype == types.bool_:
        dyrr__kjge = np.int64
    else:
        dyrr__kjge = arr.dtype
    kzt__hox = dyrr__kjge(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = kzt__hox
            pni__xlfjk = len(arr)
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(pni__xlfjk):
                hfr__ktjo = kzt__hox
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem
                    ) or not skipna:
                    hfr__ktjo = arr[qxs__xeem]
                    foj__bxnn = 1
                jubm__zjwd += hfr__ktjo
                puax__xuml += foj__bxnn
            iclye__uhbl = bodo.hiframes.series_kernels._var_handle_mincount(
                jubm__zjwd, puax__xuml, min_count)
            return iclye__uhbl
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = kzt__hox
            pni__xlfjk = len(arr)
            for qxs__xeem in numba.parfors.parfor.internal_prange(pni__xlfjk):
                hfr__ktjo = kzt__hox
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = arr[qxs__xeem]
                jubm__zjwd += hfr__ktjo
            return jubm__zjwd
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    zwz__swr = arr.dtype(1)
    if arr.dtype == types.bool_:
        zwz__swr = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = zwz__swr
            puax__xuml = 0
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = zwz__swr
                foj__bxnn = 0
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem
                    ) or not skipna:
                    hfr__ktjo = arr[qxs__xeem]
                    foj__bxnn = 1
                puax__xuml += foj__bxnn
                jubm__zjwd *= hfr__ktjo
            iclye__uhbl = bodo.hiframes.series_kernels._var_handle_mincount(
                jubm__zjwd, puax__xuml, min_count)
            return iclye__uhbl
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jubm__zjwd = zwz__swr
            for qxs__xeem in numba.parfors.parfor.internal_prange(len(arr)):
                hfr__ktjo = zwz__swr
                if not bodo.libs.array_kernels.isna(arr, qxs__xeem):
                    hfr__ktjo = arr[qxs__xeem]
                jubm__zjwd *= hfr__ktjo
            return jubm__zjwd
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        qxs__xeem = bodo.libs.array_kernels._nan_argmax(arr)
        return index[qxs__xeem]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        qxs__xeem = bodo.libs.array_kernels._nan_argmin(arr)
        return index[qxs__xeem]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            sje__meakh = {}
            for dqq__vsm in values:
                sje__meakh[bodo.utils.conversion.box_if_dt64(dqq__vsm)] = 0
            return sje__meakh
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
        pni__xlfjk = len(arr)
        ouf__pzk = np.empty(pni__xlfjk, np.bool_)
        for qxs__xeem in numba.parfors.parfor.internal_prange(pni__xlfjk):
            ouf__pzk[qxs__xeem] = bodo.utils.conversion.box_if_dt64(arr[
                qxs__xeem]) in values
        return ouf__pzk
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    tbk__efgt = len(in_arr_tup) != 1
    axtep__xeey = list(in_arr_tup.types)
    chn__rmygw = 'def impl(in_arr_tup):\n'
    chn__rmygw += '  n = len(in_arr_tup[0])\n'
    if tbk__efgt:
        wpvx__afda = ', '.join([f'in_arr_tup[{qxs__xeem}][unused]' for
            qxs__xeem in range(len(in_arr_tup))])
        ysmwk__wve = ', '.join(['False' for yprll__spd in range(len(
            in_arr_tup))])
        chn__rmygw += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({wpvx__afda},), ({ysmwk__wve},)): 0 for unused in range(0)}}
"""
        chn__rmygw += '  map_vector = np.empty(n, np.int64)\n'
        for qxs__xeem, rfrrz__pry in enumerate(axtep__xeey):
            chn__rmygw += f'  in_lst_{qxs__xeem} = []\n'
            if is_str_arr_type(rfrrz__pry):
                chn__rmygw += f'  total_len_{qxs__xeem} = 0\n'
            chn__rmygw += f'  null_in_lst_{qxs__xeem} = []\n'
        chn__rmygw += '  for i in range(n):\n'
        gpt__ixvpm = ', '.join([f'in_arr_tup[{qxs__xeem}][i]' for qxs__xeem in
            range(len(axtep__xeey))])
        hywb__exxj = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{qxs__xeem}], i)' for
            qxs__xeem in range(len(axtep__xeey))])
        chn__rmygw += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({gpt__ixvpm},), ({hywb__exxj},))
"""
        chn__rmygw += '    if data_val not in arr_map:\n'
        chn__rmygw += '      set_val = len(arr_map)\n'
        chn__rmygw += '      values_tup = data_val._data\n'
        chn__rmygw += '      nulls_tup = data_val._null_values\n'
        for qxs__xeem, rfrrz__pry in enumerate(axtep__xeey):
            chn__rmygw += (
                f'      in_lst_{qxs__xeem}.append(values_tup[{qxs__xeem}])\n')
            chn__rmygw += (
                f'      null_in_lst_{qxs__xeem}.append(nulls_tup[{qxs__xeem}])\n'
                )
            if is_str_arr_type(rfrrz__pry):
                chn__rmygw += f"""      total_len_{qxs__xeem}  += nulls_tup[{qxs__xeem}] * bodo.libs.str_arr_ext.get_utf8_size(values_tup[{qxs__xeem}])
"""
        chn__rmygw += '      arr_map[data_val] = len(arr_map)\n'
        chn__rmygw += '    else:\n'
        chn__rmygw += '      set_val = arr_map[data_val]\n'
        chn__rmygw += '    map_vector[i] = set_val\n'
        chn__rmygw += '  n_rows = len(arr_map)\n'
        for qxs__xeem, rfrrz__pry in enumerate(axtep__xeey):
            if is_str_arr_type(rfrrz__pry):
                chn__rmygw += f"""  out_arr_{qxs__xeem} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{qxs__xeem})
"""
            else:
                chn__rmygw += f"""  out_arr_{qxs__xeem} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{qxs__xeem}], (-1,))
"""
        chn__rmygw += '  for j in range(len(arr_map)):\n'
        for qxs__xeem in range(len(axtep__xeey)):
            chn__rmygw += f'    if null_in_lst_{qxs__xeem}[j]:\n'
            chn__rmygw += (
                f'      bodo.libs.array_kernels.setna(out_arr_{qxs__xeem}, j)\n'
                )
            chn__rmygw += '    else:\n'
            chn__rmygw += (
                f'      out_arr_{qxs__xeem}[j] = in_lst_{qxs__xeem}[j]\n')
        vqhl__grpr = ', '.join([f'out_arr_{qxs__xeem}' for qxs__xeem in
            range(len(axtep__xeey))])
        chn__rmygw += f'  return ({vqhl__grpr},), map_vector\n'
    else:
        chn__rmygw += '  in_arr = in_arr_tup[0]\n'
        chn__rmygw += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        chn__rmygw += '  map_vector = np.empty(n, np.int64)\n'
        chn__rmygw += '  is_na = 0\n'
        chn__rmygw += '  in_lst = []\n'
        if is_str_arr_type(axtep__xeey[0]):
            chn__rmygw += '  total_len = 0\n'
        chn__rmygw += '  for i in range(n):\n'
        chn__rmygw += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        chn__rmygw += '      is_na = 1\n'
        chn__rmygw += (
            '      # Always put NA in the last location. We can safely use\n')
        chn__rmygw += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        chn__rmygw += '      set_val = -1\n'
        chn__rmygw += '    else:\n'
        chn__rmygw += '      data_val = in_arr[i]\n'
        chn__rmygw += '      if data_val not in arr_map:\n'
        chn__rmygw += '        set_val = len(arr_map)\n'
        chn__rmygw += '        in_lst.append(data_val)\n'
        if is_str_arr_type(axtep__xeey[0]):
            chn__rmygw += (
                '        total_len += bodo.libs.str_arr_ext.get_utf8_size(data_val)\n'
                )
        chn__rmygw += '        arr_map[data_val] = len(arr_map)\n'
        chn__rmygw += '      else:\n'
        chn__rmygw += '        set_val = arr_map[data_val]\n'
        chn__rmygw += '    map_vector[i] = set_val\n'
        chn__rmygw += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(axtep__xeey[0]):
            chn__rmygw += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            chn__rmygw += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        chn__rmygw += '  for j in range(len(arr_map)):\n'
        chn__rmygw += '    out_arr[j] = in_lst[j]\n'
        chn__rmygw += '  if is_na:\n'
        chn__rmygw += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        chn__rmygw += f'  return (out_arr,), map_vector\n'
    gfjy__ifrae = {}
    exec(chn__rmygw, {'bodo': bodo, 'np': np}, gfjy__ifrae)
    impl = gfjy__ifrae['impl']
    return impl
