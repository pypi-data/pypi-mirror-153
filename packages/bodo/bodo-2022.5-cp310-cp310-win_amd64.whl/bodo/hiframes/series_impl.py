"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import gen_const_tup, is_var_size_item_array_type
from bodo.utils.typing import BodoError, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_index_names, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            xbwpn__nzlip = bodo.hiframes.pd_series_ext.get_series_data(s)
            smvyw__vhi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                xbwpn__nzlip)
            return smvyw__vhi
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s, 'Series.dtype'
        )
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s,
        'Series.dtypes')
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            bgym__fhuju = list()
            for lbtep__txyn in range(len(S)):
                bgym__fhuju.append(S.iat[lbtep__txyn])
            return bgym__fhuju
        return impl_float

    def impl(S):
        bgym__fhuju = list()
        for lbtep__txyn in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, lbtep__txyn):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            bgym__fhuju.append(S.iat[lbtep__txyn])
        return bgym__fhuju
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    ygrk__izt = dict(dtype=dtype, copy=copy, na_value=na_value)
    zkd__wbpoi = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    ygrk__izt = dict(name=name, inplace=inplace)
    zkd__wbpoi = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        vctm__vbz = ', '.join(['index_arrs[{}]'.format(lbtep__txyn) for
            lbtep__txyn in range(S.index.nlevels)])
    else:
        vctm__vbz = '    bodo.utils.conversion.index_to_array(index)\n'
    vlt__tyleq = 'index' if 'index' != series_name else 'level_0'
    yup__spfp = get_index_names(S.index, 'Series.reset_index()', vlt__tyleq)
    columns = [name for name in yup__spfp]
    columns.append(series_name)
    npz__rpqxf = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    npz__rpqxf += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    npz__rpqxf += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        npz__rpqxf += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    npz__rpqxf += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    npz__rpqxf += '    col_var = {}\n'.format(gen_const_tup(columns))
    npz__rpqxf += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({vctm__vbz}, arr), df_index, col_var)
"""
    exg__qts = {}
    exec(npz__rpqxf, {'bodo': bodo}, exg__qts)
    zcfq__kbocy = exg__qts['_impl']
    return zcfq__kbocy


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        ggo__huba = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[lbtep__txyn]):
                bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
            else:
                ggo__huba[lbtep__txyn] = np.round(arr[lbtep__txyn], decimals)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    ygrk__izt = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    zkd__wbpoi = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        jssu__bjm = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = 0
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn):
                aznxi__cphl = int(A[lbtep__txyn])
            jssu__bjm += aznxi__cphl
        return jssu__bjm != 0
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        vzp__fdlr = bodo.hiframes.pd_series_ext.get_series_data(S)
        swql__ljed = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        jssu__bjm = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(vzp__fdlr)
            ):
            aznxi__cphl = 0
            gzj__jejuv = bodo.libs.array_kernels.isna(vzp__fdlr, lbtep__txyn)
            uke__rdr = bodo.libs.array_kernels.isna(swql__ljed, lbtep__txyn)
            if gzj__jejuv and not uke__rdr or not gzj__jejuv and uke__rdr:
                aznxi__cphl = 1
            elif not gzj__jejuv:
                if vzp__fdlr[lbtep__txyn] != swql__ljed[lbtep__txyn]:
                    aznxi__cphl = 1
            jssu__bjm += aznxi__cphl
        return jssu__bjm == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    ygrk__izt = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    zkd__wbpoi = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        jssu__bjm = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = 0
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn):
                aznxi__cphl = int(not A[lbtep__txyn])
            jssu__bjm += aznxi__cphl
        return jssu__bjm == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    ygrk__izt = dict(level=level)
    zkd__wbpoi = dict(level=None)
    check_unsupported_args('Series.mad', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    usko__ooaz = types.float64
    jbr__phk = types.float64
    if S.dtype == types.float32:
        usko__ooaz = types.float32
        jbr__phk = types.float32
    nthk__vhp = usko__ooaz(0)
    ujxzu__uyus = jbr__phk(0)
    qqfg__ehavw = jbr__phk(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        qchj__nskc = nthk__vhp
        jssu__bjm = ujxzu__uyus
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = nthk__vhp
            ugql__zovcy = ujxzu__uyus
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn) or not skipna:
                aznxi__cphl = A[lbtep__txyn]
                ugql__zovcy = qqfg__ehavw
            qchj__nskc += aznxi__cphl
            jssu__bjm += ugql__zovcy
        eev__srla = bodo.hiframes.series_kernels._mean_handle_nan(qchj__nskc,
            jssu__bjm)
        uuuwk__udadb = nthk__vhp
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = nthk__vhp
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn) or not skipna:
                aznxi__cphl = abs(A[lbtep__txyn] - eev__srla)
            uuuwk__udadb += aznxi__cphl
        hxs__eek = bodo.hiframes.series_kernels._mean_handle_nan(uuuwk__udadb,
            jssu__bjm)
        return hxs__eek
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    ygrk__izt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        bneoz__mau = 0
        tahh__wpe = 0
        jssu__bjm = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = 0
            ugql__zovcy = 0
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn) or not skipna:
                aznxi__cphl = A[lbtep__txyn]
                ugql__zovcy = 1
            bneoz__mau += aznxi__cphl
            tahh__wpe += aznxi__cphl * aznxi__cphl
            jssu__bjm += ugql__zovcy
        pvymi__azz = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            bneoz__mau, tahh__wpe, jssu__bjm, ddof)
        fia__hhi = bodo.hiframes.series_kernels._sem_handle_nan(pvymi__azz,
            jssu__bjm)
        return fia__hhi
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        bneoz__mau = 0.0
        tahh__wpe = 0.0
        ucbc__hkv = 0.0
        amkb__imcar = 0.0
        jssu__bjm = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = 0.0
            ugql__zovcy = 0
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn) or not skipna:
                aznxi__cphl = np.float64(A[lbtep__txyn])
                ugql__zovcy = 1
            bneoz__mau += aznxi__cphl
            tahh__wpe += aznxi__cphl ** 2
            ucbc__hkv += aznxi__cphl ** 3
            amkb__imcar += aznxi__cphl ** 4
            jssu__bjm += ugql__zovcy
        pvymi__azz = bodo.hiframes.series_kernels.compute_kurt(bneoz__mau,
            tahh__wpe, ucbc__hkv, amkb__imcar, jssu__bjm)
        return pvymi__azz
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        bneoz__mau = 0.0
        tahh__wpe = 0.0
        ucbc__hkv = 0.0
        jssu__bjm = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(A)):
            aznxi__cphl = 0.0
            ugql__zovcy = 0
            if not bodo.libs.array_kernels.isna(A, lbtep__txyn) or not skipna:
                aznxi__cphl = np.float64(A[lbtep__txyn])
                ugql__zovcy = 1
            bneoz__mau += aznxi__cphl
            tahh__wpe += aznxi__cphl ** 2
            ucbc__hkv += aznxi__cphl ** 3
            jssu__bjm += ugql__zovcy
        pvymi__azz = bodo.hiframes.series_kernels.compute_skew(bneoz__mau,
            tahh__wpe, ucbc__hkv, jssu__bjm)
        return pvymi__azz
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        vzp__fdlr = bodo.hiframes.pd_series_ext.get_series_data(S)
        swql__ljed = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        kbf__ookcx = 0
        for lbtep__txyn in numba.parfors.parfor.internal_prange(len(vzp__fdlr)
            ):
            val__rxgf = vzp__fdlr[lbtep__txyn]
            sfs__spvs = swql__ljed[lbtep__txyn]
            kbf__ookcx += val__rxgf * sfs__spvs
        return kbf__ookcx
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    ygrk__izt = dict(skipna=skipna)
    zkd__wbpoi = dict(skipna=True)
    check_unsupported_args('Series.cumsum', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumsum(), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    ygrk__izt = dict(skipna=skipna)
    zkd__wbpoi = dict(skipna=True)
    check_unsupported_args('Series.cumprod', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumprod(), index, name
            )
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    ygrk__izt = dict(skipna=skipna)
    zkd__wbpoi = dict(skipna=True)
    check_unsupported_args('Series.cummin', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummin(arr), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    ygrk__izt = dict(skipna=skipna)
    zkd__wbpoi = dict(skipna=True)
    check_unsupported_args('Series.cummax', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummax(arr), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    ygrk__izt = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    zkd__wbpoi = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        ktnl__iyfd = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, ktnl__iyfd, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    ygrk__izt = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    zkd__wbpoi = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(np.abs(A), index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    ygrk__izt = dict(level=level)
    zkd__wbpoi = dict(level=None)
    check_unsupported_args('Series.count', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    ygrk__izt = dict(method=method, min_periods=min_periods)
    zkd__wbpoi = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        gpgr__rtd = S.sum()
        hxrmw__gri = other.sum()
        a = n * (S * other).sum() - gpgr__rtd * hxrmw__gri
        abx__vqd = n * (S ** 2).sum() - gpgr__rtd ** 2
        rjg__rad = n * (other ** 2).sum() - hxrmw__gri ** 2
        return a / np.sqrt(abx__vqd * rjg__rad)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    ygrk__izt = dict(min_periods=min_periods)
    zkd__wbpoi = dict(min_periods=None)
    check_unsupported_args('Series.cov', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        gpgr__rtd = S.mean()
        hxrmw__gri = other.mean()
        iux__lbx = ((S - gpgr__rtd) * (other - hxrmw__gri)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(iux__lbx, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            rio__qpb = np.sign(sum_val)
            return np.inf * rio__qpb
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    ygrk__izt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.min()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    ygrk__izt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.max()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    ygrk__izt = dict(axis=axis, skipna=skipna)
    zkd__wbpoi = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    ygrk__izt = dict(axis=axis, skipna=skipna)
    zkd__wbpoi = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    ygrk__izt = dict(level=level, numeric_only=numeric_only)
    zkd__wbpoi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        txzq__ixnl = arr[:n]
        tkqew__ukepg = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(txzq__ixnl,
            tkqew__ukepg, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        mxc__fvr = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        txzq__ixnl = arr[mxc__fvr:]
        tkqew__ukepg = index[mxc__fvr:]
        return bodo.hiframes.pd_series_ext.init_series(txzq__ixnl,
            tkqew__ukepg, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    pkf__uay = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in pkf__uay:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            yxu__ydcw = index[0]
            gfdib__oiq = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, yxu__ydcw,
                False))
        else:
            gfdib__oiq = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        txzq__ixnl = arr[:gfdib__oiq]
        tkqew__ukepg = index[:gfdib__oiq]
        return bodo.hiframes.pd_series_ext.init_series(txzq__ixnl,
            tkqew__ukepg, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    pkf__uay = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in pkf__uay:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            rfqd__hgcch = index[-1]
            gfdib__oiq = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                rfqd__hgcch, True))
        else:
            gfdib__oiq = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        txzq__ixnl = arr[len(arr) - gfdib__oiq:]
        tkqew__ukepg = index[len(arr) - gfdib__oiq:]
        return bodo.hiframes.pd_series_ext.init_series(txzq__ixnl,
            tkqew__ukepg, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mksv__xcayn = bodo.utils.conversion.index_to_array(index)
        kcif__fhjq, wtls__iwgo = (bodo.libs.array_kernels.
            first_last_valid_index(arr, mksv__xcayn))
        return wtls__iwgo if kcif__fhjq else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mksv__xcayn = bodo.utils.conversion.index_to_array(index)
        kcif__fhjq, wtls__iwgo = (bodo.libs.array_kernels.
            first_last_valid_index(arr, mksv__xcayn, False))
        return wtls__iwgo if kcif__fhjq else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    ygrk__izt = dict(keep=keep)
    zkd__wbpoi = dict(keep='first')
    check_unsupported_args('Series.nlargest', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mksv__xcayn = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba, tcseb__dmuu = bodo.libs.array_kernels.nlargest(arr,
            mksv__xcayn, n, True, bodo.hiframes.series_kernels.gt_f)
        nuhu__fqiwh = bodo.utils.conversion.convert_to_index(tcseb__dmuu)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
            nuhu__fqiwh, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    ygrk__izt = dict(keep=keep)
    zkd__wbpoi = dict(keep='first')
    check_unsupported_args('Series.nsmallest', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mksv__xcayn = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba, tcseb__dmuu = bodo.libs.array_kernels.nlargest(arr,
            mksv__xcayn, n, False, bodo.hiframes.series_kernels.lt_f)
        nuhu__fqiwh = bodo.utils.conversion.convert_to_index(tcseb__dmuu)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
            nuhu__fqiwh, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    ygrk__izt = dict(errors=errors)
    zkd__wbpoi = dict(errors='raise')
    check_unsupported_args('Series.astype', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    ygrk__izt = dict(axis=axis, is_copy=is_copy)
    zkd__wbpoi = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        cqxd__pqxbm = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[cqxd__pqxbm],
            index[cqxd__pqxbm], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    ygrk__izt = dict(axis=axis, kind=kind, order=order)
    zkd__wbpoi = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nxvn__dvtk = S.notna().values
        if not nxvn__dvtk.all():
            ggo__huba = np.full(n, -1, np.int64)
            ggo__huba[nxvn__dvtk] = argsort(arr[nxvn__dvtk])
        else:
            ggo__huba = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    ygrk__izt = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    zkd__wbpoi = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pfv__yyu = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        zzv__vpx = pfv__yyu.sort_index(ascending=ascending, inplace=inplace,
            na_position=na_position)
        ggo__huba = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(zzv__vpx,
            0)
        nuhu__fqiwh = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            zzv__vpx)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
            nuhu__fqiwh, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    ygrk__izt = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    zkd__wbpoi = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pfv__yyu = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        zzv__vpx = pfv__yyu.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        ggo__huba = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(zzv__vpx,
            0)
        nuhu__fqiwh = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            zzv__vpx)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
            nuhu__fqiwh, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    dku__krch = is_overload_true(is_nullable)
    npz__rpqxf = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    npz__rpqxf += '  numba.parfors.parfor.init_prange()\n'
    npz__rpqxf += '  n = len(arr)\n'
    if dku__krch:
        npz__rpqxf += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        npz__rpqxf += '  out_arr = np.empty(n, np.int64)\n'
    npz__rpqxf += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    npz__rpqxf += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if dku__krch:
        npz__rpqxf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        npz__rpqxf += '      out_arr[i] = -1\n'
    npz__rpqxf += '      continue\n'
    npz__rpqxf += '    val = arr[i]\n'
    npz__rpqxf += '    if include_lowest and val == bins[0]:\n'
    npz__rpqxf += '      ind = 1\n'
    npz__rpqxf += '    else:\n'
    npz__rpqxf += '      ind = np.searchsorted(bins, val)\n'
    npz__rpqxf += '    if ind == 0 or ind == len(bins):\n'
    if dku__krch:
        npz__rpqxf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        npz__rpqxf += '      out_arr[i] = -1\n'
    npz__rpqxf += '    else:\n'
    npz__rpqxf += '      out_arr[i] = ind - 1\n'
    npz__rpqxf += '  return out_arr\n'
    exg__qts = {}
    exec(npz__rpqxf, {'bodo': bodo, 'np': np, 'numba': numba}, exg__qts)
    impl = exg__qts['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        lqqj__zsmaz, vgxw__jdws = np.divmod(x, 1)
        if lqqj__zsmaz == 0:
            vlamg__pmnmt = -int(np.floor(np.log10(abs(vgxw__jdws)))
                ) - 1 + precision
        else:
            vlamg__pmnmt = precision
        return np.around(x, vlamg__pmnmt)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        dnkz__wbmg = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(dnkz__wbmg)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        pom__jiv = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            ebmur__dod = bins.copy()
            if right and include_lowest:
                ebmur__dod[0] = ebmur__dod[0] - pom__jiv
            pvcw__ajduh = bodo.libs.interval_arr_ext.init_interval_array(
                ebmur__dod[:-1], ebmur__dod[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(pvcw__ajduh,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        ebmur__dod = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            ebmur__dod[0] = ebmur__dod[0] - 10.0 ** -precision
        pvcw__ajduh = bodo.libs.interval_arr_ext.init_interval_array(ebmur__dod
            [:-1], ebmur__dod[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(pvcw__ajduh, None
            )
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        vwdhz__xxqo = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        hmhcl__nza = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        ggo__huba = np.zeros(nbins, np.int64)
        for lbtep__txyn in range(len(vwdhz__xxqo)):
            ggo__huba[hmhcl__nza[lbtep__txyn]] = vwdhz__xxqo[lbtep__txyn]
        return ggo__huba
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            gwytr__kxx = (max_val - min_val) * 0.001
            if right:
                bins[0] -= gwytr__kxx
            else:
                bins[-1] += gwytr__kxx
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    ygrk__izt = dict(dropna=dropna)
    zkd__wbpoi = dict(dropna=True)
    check_unsupported_args('Series.value_counts', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    ork__qohd = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    npz__rpqxf = 'def impl(\n'
    npz__rpqxf += '    S,\n'
    npz__rpqxf += '    normalize=False,\n'
    npz__rpqxf += '    sort=True,\n'
    npz__rpqxf += '    ascending=False,\n'
    npz__rpqxf += '    bins=None,\n'
    npz__rpqxf += '    dropna=True,\n'
    npz__rpqxf += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    npz__rpqxf += '):\n'
    npz__rpqxf += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    npz__rpqxf += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    npz__rpqxf += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if ork__qohd:
        npz__rpqxf += '    right = True\n'
        npz__rpqxf += _gen_bins_handling(bins, S.dtype)
        npz__rpqxf += '    arr = get_bin_inds(bins, arr)\n'
    npz__rpqxf += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    npz__rpqxf += "        (arr,), index, ('$_bodo_col2_',)\n"
    npz__rpqxf += '    )\n'
    npz__rpqxf += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if ork__qohd:
        npz__rpqxf += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        npz__rpqxf += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        npz__rpqxf += '    index = get_bin_labels(bins)\n'
    else:
        npz__rpqxf += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        npz__rpqxf += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        npz__rpqxf += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        npz__rpqxf += '    )\n'
        npz__rpqxf += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    npz__rpqxf += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        npz__rpqxf += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        hseqm__cjv = 'len(S)' if ork__qohd else 'count_arr.sum()'
        npz__rpqxf += f'    res = res / float({hseqm__cjv})\n'
    npz__rpqxf += '    return res\n'
    exg__qts = {}
    exec(npz__rpqxf, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, exg__qts)
    impl = exg__qts['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    npz__rpqxf = ''
    if isinstance(bins, types.Integer):
        npz__rpqxf += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        npz__rpqxf += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            npz__rpqxf += '    min_val = min_val.value\n'
            npz__rpqxf += '    max_val = max_val.value\n'
        npz__rpqxf += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            npz__rpqxf += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        npz__rpqxf += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return npz__rpqxf


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    ygrk__izt = dict(right=right, labels=labels, retbins=retbins, precision
        =precision, duplicates=duplicates, ordered=ordered)
    zkd__wbpoi = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    npz__rpqxf = 'def impl(\n'
    npz__rpqxf += '    x,\n'
    npz__rpqxf += '    bins,\n'
    npz__rpqxf += '    right=True,\n'
    npz__rpqxf += '    labels=None,\n'
    npz__rpqxf += '    retbins=False,\n'
    npz__rpqxf += '    precision=3,\n'
    npz__rpqxf += '    include_lowest=False,\n'
    npz__rpqxf += "    duplicates='raise',\n"
    npz__rpqxf += '    ordered=True\n'
    npz__rpqxf += '):\n'
    if isinstance(x, SeriesType):
        npz__rpqxf += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        npz__rpqxf += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        npz__rpqxf += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        npz__rpqxf += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    npz__rpqxf += _gen_bins_handling(bins, x.dtype)
    npz__rpqxf += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    npz__rpqxf += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    npz__rpqxf += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    npz__rpqxf += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        npz__rpqxf += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        npz__rpqxf += '    return res\n'
    else:
        npz__rpqxf += '    return out_arr\n'
    exg__qts = {}
    exec(npz__rpqxf, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, exg__qts)
    impl = exg__qts['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    ygrk__izt = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    zkd__wbpoi = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        nevo__qni = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, nevo__qni)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    ygrk__izt = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    zkd__wbpoi = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            ajlc__wixsz = bodo.utils.conversion.coerce_to_array(index)
            pfv__yyu = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                ajlc__wixsz, arr), index, (' ', ''))
            return pfv__yyu.groupby(' ')['']
        return impl_index
    alsh__kgxpk = by
    if isinstance(by, SeriesType):
        alsh__kgxpk = by.data
    if isinstance(alsh__kgxpk, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        ajlc__wixsz = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pfv__yyu = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            ajlc__wixsz, arr), index, (' ', ''))
        return pfv__yyu.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    ygrk__izt = dict(verify_integrity=verify_integrity)
    zkd__wbpoi = dict(verify_integrity=False)
    check_unsupported_args('Series.append', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            iifz__vonx = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            ggo__huba = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(ggo__huba, A, iifz__vonx, False)
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    ygrk__izt = dict(interpolation=interpolation)
    zkd__wbpoi = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            ggo__huba = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        bql__vvhcy = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(bql__vvhcy, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    ygrk__izt = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    zkd__wbpoi = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, IntegerArrayType):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        gojxm__orf = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        gojxm__orf = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    npz__rpqxf = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {gojxm__orf}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    sfmx__fybxx = dict()
    exec(npz__rpqxf, {'bodo': bodo, 'numba': numba}, sfmx__fybxx)
    stnie__dmqsb = sfmx__fybxx['impl']
    return stnie__dmqsb


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        gojxm__orf = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        gojxm__orf = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    npz__rpqxf = 'def impl(S,\n'
    npz__rpqxf += '     value=None,\n'
    npz__rpqxf += '    method=None,\n'
    npz__rpqxf += '    axis=None,\n'
    npz__rpqxf += '    inplace=False,\n'
    npz__rpqxf += '    limit=None,\n'
    npz__rpqxf += '   downcast=None,\n'
    npz__rpqxf += '):\n'
    npz__rpqxf += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    npz__rpqxf += '    n = len(in_arr)\n'
    npz__rpqxf += f'    out_arr = {gojxm__orf}(n, -1)\n'
    npz__rpqxf += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    npz__rpqxf += '        s = in_arr[j]\n'
    npz__rpqxf += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    npz__rpqxf += '            s = value\n'
    npz__rpqxf += '        out_arr[j] = s\n'
    npz__rpqxf += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    sfmx__fybxx = dict()
    exec(npz__rpqxf, {'bodo': bodo, 'numba': numba}, sfmx__fybxx)
    stnie__dmqsb = sfmx__fybxx['impl']
    return stnie__dmqsb


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
    isq__silx = bodo.hiframes.pd_series_ext.get_series_data(value)
    for lbtep__txyn in numba.parfors.parfor.internal_prange(len(shrk__twdig)):
        s = shrk__twdig[lbtep__txyn]
        if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn
            ) and not bodo.libs.array_kernels.isna(isq__silx, lbtep__txyn):
            s = isq__silx[lbtep__txyn]
        shrk__twdig[lbtep__txyn] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
    for lbtep__txyn in numba.parfors.parfor.internal_prange(len(shrk__twdig)):
        s = shrk__twdig[lbtep__txyn]
        if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn):
            s = value
        shrk__twdig[lbtep__txyn] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    isq__silx = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(shrk__twdig)
    ggo__huba = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for gonqn__jojz in numba.parfors.parfor.internal_prange(n):
        s = shrk__twdig[gonqn__jojz]
        if bodo.libs.array_kernels.isna(shrk__twdig, gonqn__jojz
            ) and not bodo.libs.array_kernels.isna(isq__silx, gonqn__jojz):
            s = isq__silx[gonqn__jojz]
        ggo__huba[gonqn__jojz] = s
        if bodo.libs.array_kernels.isna(shrk__twdig, gonqn__jojz
            ) and bodo.libs.array_kernels.isna(isq__silx, gonqn__jojz):
            bodo.libs.array_kernels.setna(ggo__huba, gonqn__jojz)
    return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    isq__silx = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(shrk__twdig)
    ggo__huba = bodo.utils.utils.alloc_type(n, shrk__twdig.dtype, (-1,))
    for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
        s = shrk__twdig[lbtep__txyn]
        if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn
            ) and not bodo.libs.array_kernels.isna(isq__silx, lbtep__txyn):
            s = isq__silx[lbtep__txyn]
        ggo__huba[lbtep__txyn] = s
    return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    ygrk__izt = dict(limit=limit, downcast=downcast)
    zkd__wbpoi = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    qctx__vrwlk = not is_overload_none(value)
    uxhq__uawtt = not is_overload_none(method)
    if qctx__vrwlk and uxhq__uawtt:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not qctx__vrwlk and not uxhq__uawtt:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if uxhq__uawtt:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        dxvfm__mom = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(dxvfm__mom)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(dxvfm__mom)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    mtd__okc = element_type(S.data)
    viyar__rii = None
    if qctx__vrwlk:
        viyar__rii = element_type(types.unliteral(value))
    if viyar__rii and not can_replace(mtd__okc, viyar__rii):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {viyar__rii} with series type {mtd__okc}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        nkac__brl = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                isq__silx = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(shrk__twdig)
                ggo__huba = bodo.utils.utils.alloc_type(n, nkac__brl, (-1,))
                for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn
                        ) and bodo.libs.array_kernels.isna(isq__silx,
                        lbtep__txyn):
                        bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                        continue
                    if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn):
                        ggo__huba[lbtep__txyn
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            isq__silx[lbtep__txyn])
                        continue
                    ggo__huba[lbtep__txyn
                        ] = bodo.utils.conversion.unbox_if_timestamp(
                        shrk__twdig[lbtep__txyn])
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return fillna_series_impl
        if uxhq__uawtt:
            rpwi__dfo = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(mtd__okc, (types.Integer, types.Float)
                ) and mtd__okc not in rpwi__dfo:
                raise BodoError(
                    f"Series.fillna(): series of type {mtd__okc} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ggo__huba = bodo.libs.array_kernels.ffill_bfill_arr(shrk__twdig
                    , method)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(shrk__twdig)
            ggo__huba = bodo.utils.utils.alloc_type(n, nkac__brl, (-1,))
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(shrk__twdig[
                    lbtep__txyn])
                if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn):
                    s = value
                ggo__huba[lbtep__txyn] = s
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        ptcd__udion = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        ygrk__izt = dict(limit=limit, downcast=downcast)
        zkd__wbpoi = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', ygrk__izt,
            zkd__wbpoi, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        mtd__okc = element_type(S.data)
        rpwi__dfo = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(mtd__okc, (types.Integer, types.Float)
            ) and mtd__okc not in rpwi__dfo:
            raise BodoError(
                f'Series.{overload_name}(): series of type {mtd__okc} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ggo__huba = bodo.libs.array_kernels.ffill_bfill_arr(shrk__twdig,
                ptcd__udion)
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        xukg__ziwbb = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            xukg__ziwbb)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        vgp__abxn = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(vgp__abxn)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        vgp__abxn = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(vgp__abxn)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        vgp__abxn = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(vgp__abxn)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    ygrk__izt = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    wzqmw__dxrkq = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', ygrk__izt, wzqmw__dxrkq,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    mtd__okc = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        jijy__rkcp = element_type(to_replace.key_type)
        viyar__rii = element_type(to_replace.value_type)
    else:
        jijy__rkcp = element_type(to_replace)
        viyar__rii = element_type(value)
    fjuuk__opvze = None
    if mtd__okc != types.unliteral(jijy__rkcp):
        if bodo.utils.typing.equality_always_false(mtd__okc, types.
            unliteral(jijy__rkcp)
            ) or not bodo.utils.typing.types_equality_exists(mtd__okc,
            jijy__rkcp):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(mtd__okc, (types.Float, types.Integer)
            ) or mtd__okc == np.bool_:
            fjuuk__opvze = mtd__okc
    if not can_replace(mtd__okc, types.unliteral(viyar__rii)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    dlybg__twz = to_str_arr_if_dict_array(S.data)
    if isinstance(dlybg__twz, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(shrk__twdig.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(shrk__twdig)
        ggo__huba = bodo.utils.utils.alloc_type(n, dlybg__twz, (-1,))
        jwq__ubppy = build_replace_dict(to_replace, value, fjuuk__opvze)
        for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(shrk__twdig, lbtep__txyn):
                bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                continue
            s = shrk__twdig[lbtep__txyn]
            if s in jwq__ubppy:
                s = jwq__ubppy[s]
            ggo__huba[lbtep__txyn] = s
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    xje__ieo = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    wypl__ngf = is_iterable_type(to_replace)
    uqhae__qaay = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    vcbby__npz = is_iterable_type(value)
    if xje__ieo and uqhae__qaay:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                jwq__ubppy = {}
                jwq__ubppy[key_dtype_conv(to_replace)] = value
                return jwq__ubppy
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            jwq__ubppy = {}
            jwq__ubppy[to_replace] = value
            return jwq__ubppy
        return impl
    if wypl__ngf and uqhae__qaay:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                jwq__ubppy = {}
                for ran__nce in to_replace:
                    jwq__ubppy[key_dtype_conv(ran__nce)] = value
                return jwq__ubppy
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            jwq__ubppy = {}
            for ran__nce in to_replace:
                jwq__ubppy[ran__nce] = value
            return jwq__ubppy
        return impl
    if wypl__ngf and vcbby__npz:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                jwq__ubppy = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for lbtep__txyn in range(len(to_replace)):
                    jwq__ubppy[key_dtype_conv(to_replace[lbtep__txyn])
                        ] = value[lbtep__txyn]
                return jwq__ubppy
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            jwq__ubppy = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for lbtep__txyn in range(len(to_replace)):
                jwq__ubppy[to_replace[lbtep__txyn]] = value[lbtep__txyn]
            return jwq__ubppy
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ggo__huba = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    ygrk__izt = dict(ignore_index=ignore_index)
    gyyaf__pduvr = dict(ignore_index=False)
    check_unsupported_args('Series.explode', ygrk__izt, gyyaf__pduvr,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mksv__xcayn = bodo.utils.conversion.index_to_array(index)
        ggo__huba, dthcb__tbi = bodo.libs.array_kernels.explode(arr,
            mksv__xcayn)
        nuhu__fqiwh = bodo.utils.conversion.index_from_array(dthcb__tbi)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
            nuhu__fqiwh, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            wsf__run = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                wsf__run[lbtep__txyn] = np.argmax(a[lbtep__txyn])
            return wsf__run
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            tyexb__ihr = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                tyexb__ihr[lbtep__txyn] = np.argmin(a[lbtep__txyn])
            return tyexb__ihr
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(a)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(b)
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    ygrk__izt = dict(axis=axis, inplace=inplace, how=how)
    tnbji__sex = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', ygrk__izt, tnbji__sex,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            nxvn__dvtk = S.notna().values
            mksv__xcayn = bodo.utils.conversion.extract_index_array(S)
            nuhu__fqiwh = bodo.utils.conversion.convert_to_index(mksv__xcayn
                [nxvn__dvtk])
            ggo__huba = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(shrk__twdig))
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                nuhu__fqiwh, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mksv__xcayn = bodo.utils.conversion.extract_index_array(S)
            nxvn__dvtk = S.notna().values
            nuhu__fqiwh = bodo.utils.conversion.convert_to_index(mksv__xcayn
                [nxvn__dvtk])
            ggo__huba = shrk__twdig[nxvn__dvtk]
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                nuhu__fqiwh, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    ygrk__izt = dict(freq=freq, axis=axis, fill_value=fill_value)
    zkd__wbpoi = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.shift()')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    ygrk__izt = dict(fill_method=fill_method, limit=limit, freq=freq)
    zkd__wbpoi = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', S, cond,
            other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            vzj__ypmxr = 'None'
        else:
            vzj__ypmxr = 'other'
        npz__rpqxf = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            npz__rpqxf += '  cond = ~cond\n'
        npz__rpqxf += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        npz__rpqxf += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        npz__rpqxf += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        npz__rpqxf += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {vzj__ypmxr})\n'
            )
        npz__rpqxf += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        exg__qts = {}
        exec(npz__rpqxf, {'bodo': bodo, 'np': np}, exg__qts)
        impl = exg__qts['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        xukg__ziwbb = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(xukg__ziwbb)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    ygrk__izt = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    zkd__wbpoi = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, S.data, other.data)
    else:
        _validate_self_other_mask_where(func_name, S.data, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, arr, other, max_ndim=1,
    is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or bodo.
        utils.utils.is_array_typ(arr, False) and arr.dtype in [bodo.
        string_type, bodo.bytes_type] or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type not in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.pd_timestamp_type, bodo.
        pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() Series data with type {arr} not yet supported')
    xubl__ewxcd = is_overload_constant_nan(other)
    if not (is_default or xubl__ewxcd or is_scalar_type(other) or 
        isinstance(other, types.Array) and other.ndim >= 1 and other.ndim <=
        max_ndim or isinstance(other, SeriesType) and (isinstance(arr,
        types.Array) or arr.dtype in [bodo.string_type, bodo.bytes_type]) or
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, IntegerArrayType))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for Series."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            rvcr__jesjl = arr.dtype.elem_type
        else:
            rvcr__jesjl = arr.dtype
        if is_iterable_type(other):
            neq__qxte = other.dtype
        elif xubl__ewxcd:
            neq__qxte = types.float64
        else:
            neq__qxte = types.unliteral(other)
        if not xubl__ewxcd and not is_common_scalar_dtype([rvcr__jesjl,
            neq__qxte]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        ygrk__izt = dict(level=level, axis=axis)
        zkd__wbpoi = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), ygrk__izt,
            zkd__wbpoi, package_name='pandas', module_name='Series')
        jobz__elils = other == string_type or is_overload_constant_str(other)
        vsip__lty = is_iterable_type(other) and other.dtype == string_type
        ioxtb__jzny = S.dtype == string_type and (op == operator.add and (
            jobz__elils or vsip__lty) or op == operator.mul and isinstance(
            other, types.Integer))
        jdav__dyvpl = S.dtype == bodo.timedelta64ns
        ahqz__otp = S.dtype == bodo.datetime64ns
        gktu__bqxm = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        qpq__htja = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        uig__zjej = jdav__dyvpl and (gktu__bqxm or qpq__htja
            ) or ahqz__otp and gktu__bqxm
        uig__zjej = uig__zjej and op == operator.add
        if not (isinstance(S.dtype, types.Number) or ioxtb__jzny or uig__zjej):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        hxi__pbdxh = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            dlybg__twz = hxi__pbdxh.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and dlybg__twz == types.Array(types.bool_, 1, 'C'):
                dlybg__twz = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                ggo__huba = bodo.utils.utils.alloc_type(n, dlybg__twz, (-1,))
                for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                    wqdlp__zjfg = bodo.libs.array_kernels.isna(arr, lbtep__txyn
                        )
                    if wqdlp__zjfg:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(ggo__huba,
                                lbtep__txyn)
                        else:
                            ggo__huba[lbtep__txyn] = op(fill_value, other)
                    else:
                        ggo__huba[lbtep__txyn] = op(arr[lbtep__txyn], other)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        dlybg__twz = hxi__pbdxh.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and dlybg__twz == types.Array(
            types.bool_, 1, 'C'):
            dlybg__twz = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rrb__rualr = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            ggo__huba = bodo.utils.utils.alloc_type(n, dlybg__twz, (-1,))
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                wqdlp__zjfg = bodo.libs.array_kernels.isna(arr, lbtep__txyn)
                lvl__cyb = bodo.libs.array_kernels.isna(rrb__rualr, lbtep__txyn
                    )
                if wqdlp__zjfg and lvl__cyb:
                    bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                elif wqdlp__zjfg:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                    else:
                        ggo__huba[lbtep__txyn] = op(fill_value, rrb__rualr[
                            lbtep__txyn])
                elif lvl__cyb:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                    else:
                        ggo__huba[lbtep__txyn] = op(arr[lbtep__txyn],
                            fill_value)
                else:
                    ggo__huba[lbtep__txyn] = op(arr[lbtep__txyn],
                        rrb__rualr[lbtep__txyn])
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        hxi__pbdxh = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            dlybg__twz = hxi__pbdxh.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and dlybg__twz == types.Array(types.bool_, 1, 'C'):
                dlybg__twz = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                ggo__huba = bodo.utils.utils.alloc_type(n, dlybg__twz, None)
                for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                    wqdlp__zjfg = bodo.libs.array_kernels.isna(arr, lbtep__txyn
                        )
                    if wqdlp__zjfg:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(ggo__huba,
                                lbtep__txyn)
                        else:
                            ggo__huba[lbtep__txyn] = op(other, fill_value)
                    else:
                        ggo__huba[lbtep__txyn] = op(other, arr[lbtep__txyn])
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        dlybg__twz = hxi__pbdxh.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and dlybg__twz == types.Array(
            types.bool_, 1, 'C'):
            dlybg__twz = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rrb__rualr = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            ggo__huba = bodo.utils.utils.alloc_type(n, dlybg__twz, None)
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                wqdlp__zjfg = bodo.libs.array_kernels.isna(arr, lbtep__txyn)
                lvl__cyb = bodo.libs.array_kernels.isna(rrb__rualr, lbtep__txyn
                    )
                ggo__huba[lbtep__txyn] = op(rrb__rualr[lbtep__txyn], arr[
                    lbtep__txyn])
                if wqdlp__zjfg and lvl__cyb:
                    bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                elif wqdlp__zjfg:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                    else:
                        ggo__huba[lbtep__txyn] = op(rrb__rualr[lbtep__txyn],
                            fill_value)
                elif lvl__cyb:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                    else:
                        ggo__huba[lbtep__txyn] = op(fill_value, arr[
                            lbtep__txyn])
                else:
                    ggo__huba[lbtep__txyn] = op(rrb__rualr[lbtep__txyn],
                        arr[lbtep__txyn])
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, tjhr__rdxrq in explicit_binop_funcs_two_ways.items():
        for name in tjhr__rdxrq:
            xukg__ziwbb = create_explicit_binary_op_overload(op)
            ngebh__ylnbq = create_explicit_binary_reverse_op_overload(op)
            yuchq__onxg = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(xukg__ziwbb)
            overload_method(SeriesType, yuchq__onxg, no_unliteral=True)(
                ngebh__ylnbq)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        xukg__ziwbb = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(xukg__ziwbb)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ezt__qyzab = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                ggo__huba = dt64_arr_sub(arr, ezt__qyzab)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                ggo__huba = np.empty(n, np.dtype('datetime64[ns]'))
                for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, lbtep__txyn):
                        bodo.libs.array_kernels.setna(ggo__huba, lbtep__txyn)
                        continue
                    peyw__kytz = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[lbtep__txyn]))
                    tdu__wiwr = op(peyw__kytz, rhs)
                    ggo__huba[lbtep__txyn
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        tdu__wiwr.value)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    ezt__qyzab = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    ggo__huba = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(ezt__qyzab))
                    return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ezt__qyzab = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                ggo__huba = op(arr, ezt__qyzab)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    anvpn__rkip = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    ggo__huba = op(bodo.utils.conversion.unbox_if_timestamp
                        (anvpn__rkip), arr)
                    return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                anvpn__rkip = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                ggo__huba = op(anvpn__rkip, arr)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        xukg__ziwbb = create_binary_op_overload(op)
        overload(op)(xukg__ziwbb)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    zma__hmzkl = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, zma__hmzkl)
        for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, lbtep__txyn
                ) or bodo.libs.array_kernels.isna(arg2, lbtep__txyn):
                bodo.libs.array_kernels.setna(S, lbtep__txyn)
                continue
            S[lbtep__txyn
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                lbtep__txyn]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[lbtep__txyn]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                rrb__rualr = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, rrb__rualr)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        xukg__ziwbb = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(xukg__ziwbb)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ggo__huba = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        xukg__ziwbb = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(xukg__ziwbb)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    ggo__huba = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    rrb__rualr = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    ggo__huba = ufunc(arr, rrb__rualr)
                    return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    rrb__rualr = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    ggo__huba = ufunc(arr, rrb__rualr)
                    return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        xukg__ziwbb = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(xukg__ziwbb)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        qlljo__skdnl = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        xbwpn__nzlip = np.arange(n),
        bodo.libs.timsort.sort(qlljo__skdnl, 0, n, xbwpn__nzlip)
        return xbwpn__nzlip[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        clr__tbbzv = get_overload_const_str(downcast)
        if clr__tbbzv in ('integer', 'signed'):
            out_dtype = types.int64
        elif clr__tbbzv == 'unsigned':
            out_dtype = types.uint64
        else:
            assert clr__tbbzv == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            shrk__twdig = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ggo__huba = pd.to_numeric(shrk__twdig, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index,
                name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            jlq__jigsj = np.empty(n, np.float64)
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, lbtep__txyn):
                    bodo.libs.array_kernels.setna(jlq__jigsj, lbtep__txyn)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(jlq__jigsj,
                        lbtep__txyn, arg_a, lbtep__txyn)
            return jlq__jigsj
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            jlq__jigsj = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, lbtep__txyn):
                    bodo.libs.array_kernels.setna(jlq__jigsj, lbtep__txyn)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(jlq__jigsj,
                        lbtep__txyn, arg_a, lbtep__txyn)
            return jlq__jigsj
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        exr__ngbye = if_series_to_array_type(args[0])
        if isinstance(exr__ngbye, types.Array) and isinstance(exr__ngbye.
            dtype, types.Integer):
            exr__ngbye = types.Array(types.float64, 1, 'C')
        return exr__ngbye(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    zokv__lfhq = bodo.utils.utils.is_array_typ(x, True)
    qgba__hei = bodo.utils.utils.is_array_typ(y, True)
    npz__rpqxf = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        npz__rpqxf += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if zokv__lfhq and not bodo.utils.utils.is_array_typ(x, False):
        npz__rpqxf += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if qgba__hei and not bodo.utils.utils.is_array_typ(y, False):
        npz__rpqxf += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    npz__rpqxf += '  n = len(condition)\n'
    ylckl__vobx = x.dtype if zokv__lfhq else types.unliteral(x)
    bwpz__baq = y.dtype if qgba__hei else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        ylckl__vobx = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        bwpz__baq = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    guuzb__kzed = get_data(x)
    gtmw__abeo = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(xbwpn__nzlip) for
        xbwpn__nzlip in [guuzb__kzed, gtmw__abeo])
    if gtmw__abeo == types.none:
        if isinstance(ylckl__vobx, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif guuzb__kzed == gtmw__abeo and not is_nullable:
        out_dtype = dtype_to_array_type(ylckl__vobx)
    elif ylckl__vobx == string_type or bwpz__baq == string_type:
        out_dtype = bodo.string_array_type
    elif guuzb__kzed == bytes_type or (zokv__lfhq and ylckl__vobx == bytes_type
        ) and (gtmw__abeo == bytes_type or qgba__hei and bwpz__baq ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(ylckl__vobx, bodo.PDCategoricalDtype):
        out_dtype = None
    elif ylckl__vobx in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(ylckl__vobx, 1, 'C')
    elif bwpz__baq in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(bwpz__baq, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(ylckl__vobx), numba.np.numpy_support.
            as_dtype(bwpz__baq)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(ylckl__vobx, bodo.PDCategoricalDtype):
        grvk__tcutc = 'x'
    else:
        grvk__tcutc = 'out_dtype'
    npz__rpqxf += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {grvk__tcutc}, (-1,))\n')
    if isinstance(ylckl__vobx, bodo.PDCategoricalDtype):
        npz__rpqxf += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        npz__rpqxf += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    npz__rpqxf += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    npz__rpqxf += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if zokv__lfhq:
        npz__rpqxf += '      if bodo.libs.array_kernels.isna(x, j):\n'
        npz__rpqxf += '        setna(out_arr, j)\n'
        npz__rpqxf += '        continue\n'
    if isinstance(ylckl__vobx, bodo.PDCategoricalDtype):
        npz__rpqxf += '      out_codes[j] = x_codes[j]\n'
    else:
        npz__rpqxf += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if zokv__lfhq else 'x'))
    npz__rpqxf += '    else:\n'
    if qgba__hei:
        npz__rpqxf += '      if bodo.libs.array_kernels.isna(y, j):\n'
        npz__rpqxf += '        setna(out_arr, j)\n'
        npz__rpqxf += '        continue\n'
    if gtmw__abeo == types.none:
        if isinstance(ylckl__vobx, bodo.PDCategoricalDtype):
            npz__rpqxf += '      out_codes[j] = -1\n'
        else:
            npz__rpqxf += '      setna(out_arr, j)\n'
    else:
        npz__rpqxf += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if qgba__hei else 'y'))
    npz__rpqxf += '  return out_arr\n'
    exg__qts = {}
    exec(npz__rpqxf, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, exg__qts)
    zcfq__kbocy = exg__qts['_impl']
    return zcfq__kbocy


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        slsbb__eex = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(slsbb__eex, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(slsbb__eex):
            prpd__mgfp = slsbb__eex.data.dtype
        else:
            prpd__mgfp = slsbb__eex.dtype
        if isinstance(prpd__mgfp, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        wsxot__jokk = slsbb__eex
    else:
        ueqil__poz = []
        for slsbb__eex in choicelist:
            if not bodo.utils.utils.is_array_typ(slsbb__eex, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(slsbb__eex):
                prpd__mgfp = slsbb__eex.data.dtype
            else:
                prpd__mgfp = slsbb__eex.dtype
            if isinstance(prpd__mgfp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            ueqil__poz.append(prpd__mgfp)
        if not is_common_scalar_dtype(ueqil__poz):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        wsxot__jokk = choicelist[0]
    if is_series_type(wsxot__jokk):
        wsxot__jokk = wsxot__jokk.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, wsxot__jokk.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(wsxot__jokk, types.Array) or isinstance(wsxot__jokk,
        BooleanArrayType) or isinstance(wsxot__jokk, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(wsxot__jokk, False) and wsxot__jokk.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {wsxot__jokk} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    kmmz__acpw = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        jlff__sez = choicelist.dtype
    else:
        nufnb__gib = False
        ueqil__poz = []
        for slsbb__eex in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                slsbb__eex, 'numpy.select()')
            if is_nullable_type(slsbb__eex):
                nufnb__gib = True
            if is_series_type(slsbb__eex):
                prpd__mgfp = slsbb__eex.data.dtype
            else:
                prpd__mgfp = slsbb__eex.dtype
            if isinstance(prpd__mgfp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            ueqil__poz.append(prpd__mgfp)
        erqjy__apyn, hhfm__hluv = get_common_scalar_dtype(ueqil__poz)
        if not hhfm__hluv:
            raise BodoError('Internal error in overload_np_select')
        gyp__bqlj = dtype_to_array_type(erqjy__apyn)
        if nufnb__gib:
            gyp__bqlj = to_nullable_type(gyp__bqlj)
        jlff__sez = gyp__bqlj
    if isinstance(jlff__sez, SeriesType):
        jlff__sez = jlff__sez.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        osbik__bnxj = True
    else:
        osbik__bnxj = False
    urn__fza = False
    tcg__iioc = False
    if osbik__bnxj:
        if isinstance(jlff__sez.dtype, types.Number):
            pass
        elif jlff__sez.dtype == types.bool_:
            tcg__iioc = True
        else:
            urn__fza = True
            jlff__sez = to_nullable_type(jlff__sez)
    elif default == types.none or is_overload_constant_nan(default):
        urn__fza = True
        jlff__sez = to_nullable_type(jlff__sez)
    npz__rpqxf = 'def np_select_impl(condlist, choicelist, default=0):\n'
    npz__rpqxf += '  if len(condlist) != len(choicelist):\n'
    npz__rpqxf += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    npz__rpqxf += '  output_len = len(choicelist[0])\n'
    npz__rpqxf += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    npz__rpqxf += '  for i in range(output_len):\n'
    if urn__fza:
        npz__rpqxf += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif tcg__iioc:
        npz__rpqxf += '    out[i] = False\n'
    else:
        npz__rpqxf += '    out[i] = default\n'
    if kmmz__acpw:
        npz__rpqxf += '  for i in range(len(condlist) - 1, -1, -1):\n'
        npz__rpqxf += '    cond = condlist[i]\n'
        npz__rpqxf += '    choice = choicelist[i]\n'
        npz__rpqxf += '    out = np.where(cond, choice, out)\n'
    else:
        for lbtep__txyn in range(len(choicelist) - 1, -1, -1):
            npz__rpqxf += f'  cond = condlist[{lbtep__txyn}]\n'
            npz__rpqxf += f'  choice = choicelist[{lbtep__txyn}]\n'
            npz__rpqxf += f'  out = np.where(cond, choice, out)\n'
    npz__rpqxf += '  return out'
    exg__qts = dict()
    exec(npz__rpqxf, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': jlff__sez}, exg__qts)
    impl = exg__qts['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ggo__huba = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    ygrk__izt = dict(subset=subset, keep=keep, inplace=inplace)
    zkd__wbpoi = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        gsl__hvz = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (gsl__hvz,), mksv__xcayn = bodo.libs.array_kernels.drop_duplicates((
            gsl__hvz,), index, 1)
        index = bodo.utils.conversion.index_from_array(mksv__xcayn)
        return bodo.hiframes.pd_series_ext.init_series(gsl__hvz, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    ymn__kdfin = element_type(S.data)
    if not is_common_scalar_dtype([ymn__kdfin, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([ymn__kdfin, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        ggo__huba = np.empty(n, np.bool_)
        for lbtep__txyn in numba.parfors.parfor.internal_prange(n):
            aznxi__cphl = bodo.utils.conversion.box_if_dt64(arr[lbtep__txyn])
            if inclusive == 'both':
                ggo__huba[lbtep__txyn
                    ] = aznxi__cphl <= right and aznxi__cphl >= left
            else:
                ggo__huba[lbtep__txyn
                    ] = aznxi__cphl < right and aznxi__cphl > left
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    ygrk__izt = dict(axis=axis)
    zkd__wbpoi = dict(axis=None)
    check_unsupported_args('Series.repeat', ygrk__izt, zkd__wbpoi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mksv__xcayn = bodo.utils.conversion.index_to_array(index)
            ggo__huba = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            dthcb__tbi = bodo.libs.array_kernels.repeat_kernel(mksv__xcayn,
                repeats)
            nuhu__fqiwh = bodo.utils.conversion.index_from_array(dthcb__tbi)
            return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
                nuhu__fqiwh, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mksv__xcayn = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        ggo__huba = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        dthcb__tbi = bodo.libs.array_kernels.repeat_kernel(mksv__xcayn, repeats
            )
        nuhu__fqiwh = bodo.utils.conversion.index_from_array(dthcb__tbi)
        return bodo.hiframes.pd_series_ext.init_series(ggo__huba,
            nuhu__fqiwh, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        xbwpn__nzlip = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(xbwpn__nzlip)
        wkfl__yvizy = {}
        for lbtep__txyn in range(n):
            aznxi__cphl = bodo.utils.conversion.box_if_dt64(xbwpn__nzlip[
                lbtep__txyn])
            wkfl__yvizy[index[lbtep__txyn]] = aznxi__cphl
        return wkfl__yvizy
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    dxvfm__mom = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            fbhk__mipe = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(dxvfm__mom)
    elif is_literal_type(name):
        fbhk__mipe = get_literal_value(name)
    else:
        raise_bodo_error(dxvfm__mom)
    fbhk__mipe = 0 if fbhk__mipe is None else fbhk__mipe

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (fbhk__mipe,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
