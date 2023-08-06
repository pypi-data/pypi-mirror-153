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
            stuc__hzl = bodo.hiframes.pd_series_ext.get_series_data(s)
            vnqo__iqtox = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                stuc__hzl)
            return vnqo__iqtox
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
            bcxb__esplt = list()
            for borj__grzi in range(len(S)):
                bcxb__esplt.append(S.iat[borj__grzi])
            return bcxb__esplt
        return impl_float

    def impl(S):
        bcxb__esplt = list()
        for borj__grzi in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, borj__grzi):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            bcxb__esplt.append(S.iat[borj__grzi])
        return bcxb__esplt
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    aqvfa__rols = dict(dtype=dtype, copy=copy, na_value=na_value)
    iuteq__bxjm = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    aqvfa__rols = dict(name=name, inplace=inplace)
    iuteq__bxjm = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', aqvfa__rols, iuteq__bxjm,
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
        iem__dnzo = ', '.join(['index_arrs[{}]'.format(borj__grzi) for
            borj__grzi in range(S.index.nlevels)])
    else:
        iem__dnzo = '    bodo.utils.conversion.index_to_array(index)\n'
    gsk__pwf = 'index' if 'index' != series_name else 'level_0'
    hmpre__dvj = get_index_names(S.index, 'Series.reset_index()', gsk__pwf)
    columns = [name for name in hmpre__dvj]
    columns.append(series_name)
    ihm__khfpz = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    ihm__khfpz += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ihm__khfpz += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        ihm__khfpz += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    ihm__khfpz += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    ihm__khfpz += '    col_var = {}\n'.format(gen_const_tup(columns))
    ihm__khfpz += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({iem__dnzo}, arr), df_index, col_var)
"""
    tqtz__slp = {}
    exec(ihm__khfpz, {'bodo': bodo}, tqtz__slp)
    xtnfm__twy = tqtz__slp['_impl']
    return xtnfm__twy


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgiof__bwj = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
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
        wgiof__bwj = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for borj__grzi in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[borj__grzi]):
                bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
            else:
                wgiof__bwj[borj__grzi] = np.round(arr[borj__grzi], decimals)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    iuteq__bxjm = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        kcxhq__wkjmu = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = 0
            if not bodo.libs.array_kernels.isna(A, borj__grzi):
                sanx__slkx = int(A[borj__grzi])
            kcxhq__wkjmu += sanx__slkx
        return kcxhq__wkjmu != 0
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
        ktaxs__mhjfj = bodo.hiframes.pd_series_ext.get_series_data(S)
        pvbf__nfmb = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        kcxhq__wkjmu = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(
            ktaxs__mhjfj)):
            sanx__slkx = 0
            ono__dbdob = bodo.libs.array_kernels.isna(ktaxs__mhjfj, borj__grzi)
            tsd__pee = bodo.libs.array_kernels.isna(pvbf__nfmb, borj__grzi)
            if ono__dbdob and not tsd__pee or not ono__dbdob and tsd__pee:
                sanx__slkx = 1
            elif not ono__dbdob:
                if ktaxs__mhjfj[borj__grzi] != pvbf__nfmb[borj__grzi]:
                    sanx__slkx = 1
            kcxhq__wkjmu += sanx__slkx
        return kcxhq__wkjmu == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    aqvfa__rols = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    iuteq__bxjm = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        kcxhq__wkjmu = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = 0
            if not bodo.libs.array_kernels.isna(A, borj__grzi):
                sanx__slkx = int(not A[borj__grzi])
            kcxhq__wkjmu += sanx__slkx
        return kcxhq__wkjmu == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    aqvfa__rols = dict(level=level)
    iuteq__bxjm = dict(level=None)
    check_unsupported_args('Series.mad', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    hdc__ufe = types.float64
    oco__hbowg = types.float64
    if S.dtype == types.float32:
        hdc__ufe = types.float32
        oco__hbowg = types.float32
    tviy__wyt = hdc__ufe(0)
    qhhl__fomq = oco__hbowg(0)
    fnfwd__annnn = oco__hbowg(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        nqpw__gli = tviy__wyt
        kcxhq__wkjmu = qhhl__fomq
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = tviy__wyt
            ddvs__mrdab = qhhl__fomq
            if not bodo.libs.array_kernels.isna(A, borj__grzi) or not skipna:
                sanx__slkx = A[borj__grzi]
                ddvs__mrdab = fnfwd__annnn
            nqpw__gli += sanx__slkx
            kcxhq__wkjmu += ddvs__mrdab
        rdzlz__ymxd = bodo.hiframes.series_kernels._mean_handle_nan(nqpw__gli,
            kcxhq__wkjmu)
        vqigx__ybpm = tviy__wyt
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = tviy__wyt
            if not bodo.libs.array_kernels.isna(A, borj__grzi) or not skipna:
                sanx__slkx = abs(A[borj__grzi] - rdzlz__ymxd)
            vqigx__ybpm += sanx__slkx
        ftx__wohqf = bodo.hiframes.series_kernels._mean_handle_nan(vqigx__ybpm,
            kcxhq__wkjmu)
        return ftx__wohqf
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    aqvfa__rols = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', aqvfa__rols, iuteq__bxjm,
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
        shu__rqv = 0
        orxb__dgzu = 0
        kcxhq__wkjmu = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = 0
            ddvs__mrdab = 0
            if not bodo.libs.array_kernels.isna(A, borj__grzi) or not skipna:
                sanx__slkx = A[borj__grzi]
                ddvs__mrdab = 1
            shu__rqv += sanx__slkx
            orxb__dgzu += sanx__slkx * sanx__slkx
            kcxhq__wkjmu += ddvs__mrdab
        tdj__uqgcy = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            shu__rqv, orxb__dgzu, kcxhq__wkjmu, ddof)
        vsq__aoc = bodo.hiframes.series_kernels._sem_handle_nan(tdj__uqgcy,
            kcxhq__wkjmu)
        return vsq__aoc
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', aqvfa__rols, iuteq__bxjm,
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
        shu__rqv = 0.0
        orxb__dgzu = 0.0
        vuwk__jngs = 0.0
        fltam__zfv = 0.0
        kcxhq__wkjmu = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = 0.0
            ddvs__mrdab = 0
            if not bodo.libs.array_kernels.isna(A, borj__grzi) or not skipna:
                sanx__slkx = np.float64(A[borj__grzi])
                ddvs__mrdab = 1
            shu__rqv += sanx__slkx
            orxb__dgzu += sanx__slkx ** 2
            vuwk__jngs += sanx__slkx ** 3
            fltam__zfv += sanx__slkx ** 4
            kcxhq__wkjmu += ddvs__mrdab
        tdj__uqgcy = bodo.hiframes.series_kernels.compute_kurt(shu__rqv,
            orxb__dgzu, vuwk__jngs, fltam__zfv, kcxhq__wkjmu)
        return tdj__uqgcy
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', aqvfa__rols, iuteq__bxjm,
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
        shu__rqv = 0.0
        orxb__dgzu = 0.0
        vuwk__jngs = 0.0
        kcxhq__wkjmu = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(A)):
            sanx__slkx = 0.0
            ddvs__mrdab = 0
            if not bodo.libs.array_kernels.isna(A, borj__grzi) or not skipna:
                sanx__slkx = np.float64(A[borj__grzi])
                ddvs__mrdab = 1
            shu__rqv += sanx__slkx
            orxb__dgzu += sanx__slkx ** 2
            vuwk__jngs += sanx__slkx ** 3
            kcxhq__wkjmu += ddvs__mrdab
        tdj__uqgcy = bodo.hiframes.series_kernels.compute_skew(shu__rqv,
            orxb__dgzu, vuwk__jngs, kcxhq__wkjmu)
        return tdj__uqgcy
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', aqvfa__rols, iuteq__bxjm,
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
        ktaxs__mhjfj = bodo.hiframes.pd_series_ext.get_series_data(S)
        pvbf__nfmb = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        xskle__vyxt = 0
        for borj__grzi in numba.parfors.parfor.internal_prange(len(
            ktaxs__mhjfj)):
            ncvg__dzs = ktaxs__mhjfj[borj__grzi]
            kvkht__gpc = pvbf__nfmb[borj__grzi]
            xskle__vyxt += ncvg__dzs * kvkht__gpc
        return xskle__vyxt
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    aqvfa__rols = dict(skipna=skipna)
    iuteq__bxjm = dict(skipna=True)
    check_unsupported_args('Series.cumsum', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(skipna=skipna)
    iuteq__bxjm = dict(skipna=True)
    check_unsupported_args('Series.cumprod', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(skipna=skipna)
    iuteq__bxjm = dict(skipna=True)
    check_unsupported_args('Series.cummin', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(skipna=skipna)
    iuteq__bxjm = dict(skipna=True)
    check_unsupported_args('Series.cummax', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    iuteq__bxjm = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        dtsg__gkvq = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, dtsg__gkvq, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    aqvfa__rols = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    iuteq__bxjm = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(level=level)
    iuteq__bxjm = dict(level=None)
    check_unsupported_args('Series.count', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    aqvfa__rols = dict(method=method, min_periods=min_periods)
    iuteq__bxjm = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        eajl__jhcq = S.sum()
        vpw__blrr = other.sum()
        a = n * (S * other).sum() - eajl__jhcq * vpw__blrr
        qzmeq__gjpaj = n * (S ** 2).sum() - eajl__jhcq ** 2
        xhn__qbo = n * (other ** 2).sum() - vpw__blrr ** 2
        return a / np.sqrt(qzmeq__gjpaj * xhn__qbo)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    aqvfa__rols = dict(min_periods=min_periods)
    iuteq__bxjm = dict(min_periods=None)
    check_unsupported_args('Series.cov', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        eajl__jhcq = S.mean()
        vpw__blrr = other.mean()
        umjff__ryd = ((S - eajl__jhcq) * (other - vpw__blrr)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(umjff__ryd, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            aqgh__spq = np.sign(sum_val)
            return np.inf * aqgh__spq
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    aqvfa__rols = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(axis=axis, skipna=skipna)
    iuteq__bxjm = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(axis=axis, skipna=skipna)
    iuteq__bxjm = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', aqvfa__rols, iuteq__bxjm,
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
    aqvfa__rols = dict(level=level, numeric_only=numeric_only)
    iuteq__bxjm = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', aqvfa__rols, iuteq__bxjm,
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
        hjch__vxnx = arr[:n]
        wnpn__fdfvt = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(hjch__vxnx,
            wnpn__fdfvt, name)
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
        glui__wgpzr = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hjch__vxnx = arr[glui__wgpzr:]
        wnpn__fdfvt = index[glui__wgpzr:]
        return bodo.hiframes.pd_series_ext.init_series(hjch__vxnx,
            wnpn__fdfvt, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    txgoc__bpki = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in txgoc__bpki:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            auhg__warq = index[0]
            qeiat__hbvd = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                auhg__warq, False))
        else:
            qeiat__hbvd = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hjch__vxnx = arr[:qeiat__hbvd]
        wnpn__fdfvt = index[:qeiat__hbvd]
        return bodo.hiframes.pd_series_ext.init_series(hjch__vxnx,
            wnpn__fdfvt, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    txgoc__bpki = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in txgoc__bpki:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            ewg__opunp = index[-1]
            qeiat__hbvd = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                ewg__opunp, True))
        else:
            qeiat__hbvd = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hjch__vxnx = arr[len(arr) - qeiat__hbvd:]
        wnpn__fdfvt = index[len(arr) - qeiat__hbvd:]
        return bodo.hiframes.pd_series_ext.init_series(hjch__vxnx,
            wnpn__fdfvt, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        qkizc__nyyis = bodo.utils.conversion.index_to_array(index)
        awtou__ezdz, vvg__tknrt = (bodo.libs.array_kernels.
            first_last_valid_index(arr, qkizc__nyyis))
        return vvg__tknrt if awtou__ezdz else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        qkizc__nyyis = bodo.utils.conversion.index_to_array(index)
        awtou__ezdz, vvg__tknrt = (bodo.libs.array_kernels.
            first_last_valid_index(arr, qkizc__nyyis, False))
        return vvg__tknrt if awtou__ezdz else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    aqvfa__rols = dict(keep=keep)
    iuteq__bxjm = dict(keep='first')
    check_unsupported_args('Series.nlargest', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        qkizc__nyyis = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgiof__bwj, ofws__lol = bodo.libs.array_kernels.nlargest(arr,
            qkizc__nyyis, n, True, bodo.hiframes.series_kernels.gt_f)
        ctf__kaz = bodo.utils.conversion.convert_to_index(ofws__lol)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, ctf__kaz,
            name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    aqvfa__rols = dict(keep=keep)
    iuteq__bxjm = dict(keep='first')
    check_unsupported_args('Series.nsmallest', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        qkizc__nyyis = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgiof__bwj, ofws__lol = bodo.libs.array_kernels.nlargest(arr,
            qkizc__nyyis, n, False, bodo.hiframes.series_kernels.lt_f)
        ctf__kaz = bodo.utils.conversion.convert_to_index(ofws__lol)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, ctf__kaz,
            name)
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
    aqvfa__rols = dict(errors=errors)
    iuteq__bxjm = dict(errors='raise')
    check_unsupported_args('Series.astype', aqvfa__rols, iuteq__bxjm,
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
        wgiof__bwj = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    aqvfa__rols = dict(axis=axis, is_copy=is_copy)
    iuteq__bxjm = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        mrv__wgh = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[mrv__wgh], index
            [mrv__wgh], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    aqvfa__rols = dict(axis=axis, kind=kind, order=order)
    iuteq__bxjm = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        sqnk__bkw = S.notna().values
        if not sqnk__bkw.all():
            wgiof__bwj = np.full(n, -1, np.int64)
            wgiof__bwj[sqnk__bkw] = argsort(arr[sqnk__bkw])
        else:
            wgiof__bwj = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    aqvfa__rols = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    iuteq__bxjm = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', aqvfa__rols, iuteq__bxjm,
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
        fgi__jjxn = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        kpi__rjsx = fgi__jjxn.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        wgiof__bwj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            kpi__rjsx, 0)
        ctf__kaz = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(kpi__rjsx
            )
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, ctf__kaz,
            name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    aqvfa__rols = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    iuteq__bxjm = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', aqvfa__rols, iuteq__bxjm,
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
        fgi__jjxn = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        kpi__rjsx = fgi__jjxn.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        wgiof__bwj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            kpi__rjsx, 0)
        ctf__kaz = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(kpi__rjsx
            )
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, ctf__kaz,
            name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    dyluq__izwt = is_overload_true(is_nullable)
    ihm__khfpz = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    ihm__khfpz += '  numba.parfors.parfor.init_prange()\n'
    ihm__khfpz += '  n = len(arr)\n'
    if dyluq__izwt:
        ihm__khfpz += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        ihm__khfpz += '  out_arr = np.empty(n, np.int64)\n'
    ihm__khfpz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    ihm__khfpz += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if dyluq__izwt:
        ihm__khfpz += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        ihm__khfpz += '      out_arr[i] = -1\n'
    ihm__khfpz += '      continue\n'
    ihm__khfpz += '    val = arr[i]\n'
    ihm__khfpz += '    if include_lowest and val == bins[0]:\n'
    ihm__khfpz += '      ind = 1\n'
    ihm__khfpz += '    else:\n'
    ihm__khfpz += '      ind = np.searchsorted(bins, val)\n'
    ihm__khfpz += '    if ind == 0 or ind == len(bins):\n'
    if dyluq__izwt:
        ihm__khfpz += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        ihm__khfpz += '      out_arr[i] = -1\n'
    ihm__khfpz += '    else:\n'
    ihm__khfpz += '      out_arr[i] = ind - 1\n'
    ihm__khfpz += '  return out_arr\n'
    tqtz__slp = {}
    exec(ihm__khfpz, {'bodo': bodo, 'np': np, 'numba': numba}, tqtz__slp)
    impl = tqtz__slp['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        prezt__mtdxr, pqm__boygi = np.divmod(x, 1)
        if prezt__mtdxr == 0:
            ngxvh__diln = -int(np.floor(np.log10(abs(pqm__boygi)))
                ) - 1 + precision
        else:
            ngxvh__diln = precision
        return np.around(x, ngxvh__diln)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        syab__bqq = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(syab__bqq)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        oichc__btvu = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            oib__uaykp = bins.copy()
            if right and include_lowest:
                oib__uaykp[0] = oib__uaykp[0] - oichc__btvu
            ver__rll = bodo.libs.interval_arr_ext.init_interval_array(
                oib__uaykp[:-1], oib__uaykp[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(ver__rll,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        oib__uaykp = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            oib__uaykp[0] = oib__uaykp[0] - 10.0 ** -precision
        ver__rll = bodo.libs.interval_arr_ext.init_interval_array(oib__uaykp
            [:-1], oib__uaykp[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(ver__rll, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        vvaw__dftju = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        gojir__ksr = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        wgiof__bwj = np.zeros(nbins, np.int64)
        for borj__grzi in range(len(vvaw__dftju)):
            wgiof__bwj[gojir__ksr[borj__grzi]] = vvaw__dftju[borj__grzi]
        return wgiof__bwj
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
            lkow__dng = (max_val - min_val) * 0.001
            if right:
                bins[0] -= lkow__dng
            else:
                bins[-1] += lkow__dng
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    aqvfa__rols = dict(dropna=dropna)
    iuteq__bxjm = dict(dropna=True)
    check_unsupported_args('Series.value_counts', aqvfa__rols, iuteq__bxjm,
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
    nyssh__daj = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    ihm__khfpz = 'def impl(\n'
    ihm__khfpz += '    S,\n'
    ihm__khfpz += '    normalize=False,\n'
    ihm__khfpz += '    sort=True,\n'
    ihm__khfpz += '    ascending=False,\n'
    ihm__khfpz += '    bins=None,\n'
    ihm__khfpz += '    dropna=True,\n'
    ihm__khfpz += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    ihm__khfpz += '):\n'
    ihm__khfpz += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ihm__khfpz += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    ihm__khfpz += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if nyssh__daj:
        ihm__khfpz += '    right = True\n'
        ihm__khfpz += _gen_bins_handling(bins, S.dtype)
        ihm__khfpz += '    arr = get_bin_inds(bins, arr)\n'
    ihm__khfpz += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    ihm__khfpz += "        (arr,), index, ('$_bodo_col2_',)\n"
    ihm__khfpz += '    )\n'
    ihm__khfpz += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if nyssh__daj:
        ihm__khfpz += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        ihm__khfpz += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        ihm__khfpz += '    index = get_bin_labels(bins)\n'
    else:
        ihm__khfpz += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        ihm__khfpz += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        ihm__khfpz += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        ihm__khfpz += '    )\n'
        ihm__khfpz += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    ihm__khfpz += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        ihm__khfpz += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        zyeag__uhnv = 'len(S)' if nyssh__daj else 'count_arr.sum()'
        ihm__khfpz += f'    res = res / float({zyeag__uhnv})\n'
    ihm__khfpz += '    return res\n'
    tqtz__slp = {}
    exec(ihm__khfpz, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, tqtz__slp)
    impl = tqtz__slp['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    ihm__khfpz = ''
    if isinstance(bins, types.Integer):
        ihm__khfpz += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        ihm__khfpz += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            ihm__khfpz += '    min_val = min_val.value\n'
            ihm__khfpz += '    max_val = max_val.value\n'
        ihm__khfpz += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            ihm__khfpz += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        ihm__khfpz += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return ihm__khfpz


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    aqvfa__rols = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    iuteq__bxjm = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    ihm__khfpz = 'def impl(\n'
    ihm__khfpz += '    x,\n'
    ihm__khfpz += '    bins,\n'
    ihm__khfpz += '    right=True,\n'
    ihm__khfpz += '    labels=None,\n'
    ihm__khfpz += '    retbins=False,\n'
    ihm__khfpz += '    precision=3,\n'
    ihm__khfpz += '    include_lowest=False,\n'
    ihm__khfpz += "    duplicates='raise',\n"
    ihm__khfpz += '    ordered=True\n'
    ihm__khfpz += '):\n'
    if isinstance(x, SeriesType):
        ihm__khfpz += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        ihm__khfpz += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        ihm__khfpz += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        ihm__khfpz += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    ihm__khfpz += _gen_bins_handling(bins, x.dtype)
    ihm__khfpz += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    ihm__khfpz += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    ihm__khfpz += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    ihm__khfpz += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        ihm__khfpz += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        ihm__khfpz += '    return res\n'
    else:
        ihm__khfpz += '    return out_arr\n'
    tqtz__slp = {}
    exec(ihm__khfpz, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, tqtz__slp)
    impl = tqtz__slp['impl']
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
    aqvfa__rols = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    iuteq__bxjm = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        kbowx__qsmwr = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, kbowx__qsmwr)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    aqvfa__rols = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze
        =squeeze, observed=observed, dropna=dropna)
    iuteq__bxjm = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', aqvfa__rols, iuteq__bxjm,
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
            nkswf__agygt = bodo.utils.conversion.coerce_to_array(index)
            fgi__jjxn = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                nkswf__agygt, arr), index, (' ', ''))
            return fgi__jjxn.groupby(' ')['']
        return impl_index
    rtyjw__bvtv = by
    if isinstance(by, SeriesType):
        rtyjw__bvtv = by.data
    if isinstance(rtyjw__bvtv, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        nkswf__agygt = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fgi__jjxn = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            nkswf__agygt, arr), index, (' ', ''))
        return fgi__jjxn.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    aqvfa__rols = dict(verify_integrity=verify_integrity)
    iuteq__bxjm = dict(verify_integrity=False)
    check_unsupported_args('Series.append', aqvfa__rols, iuteq__bxjm,
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
            nos__igi = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            wgiof__bwj = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(wgiof__bwj, A, nos__igi, False)
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgiof__bwj = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    aqvfa__rols = dict(interpolation=interpolation)
    iuteq__bxjm = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            wgiof__bwj = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
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
        lkjd__jkfhr = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(lkjd__jkfhr, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    aqvfa__rols = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    iuteq__bxjm = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', aqvfa__rols, iuteq__bxjm,
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
        dzmdh__ukgda = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        dzmdh__ukgda = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    ihm__khfpz = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {dzmdh__ukgda}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    hip__bqpku = dict()
    exec(ihm__khfpz, {'bodo': bodo, 'numba': numba}, hip__bqpku)
    rrfn__vzx = hip__bqpku['impl']
    return rrfn__vzx


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        dzmdh__ukgda = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        dzmdh__ukgda = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    ihm__khfpz = 'def impl(S,\n'
    ihm__khfpz += '     value=None,\n'
    ihm__khfpz += '    method=None,\n'
    ihm__khfpz += '    axis=None,\n'
    ihm__khfpz += '    inplace=False,\n'
    ihm__khfpz += '    limit=None,\n'
    ihm__khfpz += '   downcast=None,\n'
    ihm__khfpz += '):\n'
    ihm__khfpz += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ihm__khfpz += '    n = len(in_arr)\n'
    ihm__khfpz += f'    out_arr = {dzmdh__ukgda}(n, -1)\n'
    ihm__khfpz += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    ihm__khfpz += '        s = in_arr[j]\n'
    ihm__khfpz += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    ihm__khfpz += '            s = value\n'
    ihm__khfpz += '        out_arr[j] = s\n'
    ihm__khfpz += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    hip__bqpku = dict()
    exec(ihm__khfpz, {'bodo': bodo, 'numba': numba}, hip__bqpku)
    rrfn__vzx = hip__bqpku['impl']
    return rrfn__vzx


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
    hhcxa__rycyb = bodo.hiframes.pd_series_ext.get_series_data(value)
    for borj__grzi in numba.parfors.parfor.internal_prange(len(tsis__donu)):
        s = tsis__donu[borj__grzi]
        if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi
            ) and not bodo.libs.array_kernels.isna(hhcxa__rycyb, borj__grzi):
            s = hhcxa__rycyb[borj__grzi]
        tsis__donu[borj__grzi] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
    for borj__grzi in numba.parfors.parfor.internal_prange(len(tsis__donu)):
        s = tsis__donu[borj__grzi]
        if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi):
            s = value
        tsis__donu[borj__grzi] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    hhcxa__rycyb = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(tsis__donu)
    wgiof__bwj = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for qti__cdmn in numba.parfors.parfor.internal_prange(n):
        s = tsis__donu[qti__cdmn]
        if bodo.libs.array_kernels.isna(tsis__donu, qti__cdmn
            ) and not bodo.libs.array_kernels.isna(hhcxa__rycyb, qti__cdmn):
            s = hhcxa__rycyb[qti__cdmn]
        wgiof__bwj[qti__cdmn] = s
        if bodo.libs.array_kernels.isna(tsis__donu, qti__cdmn
            ) and bodo.libs.array_kernels.isna(hhcxa__rycyb, qti__cdmn):
            bodo.libs.array_kernels.setna(wgiof__bwj, qti__cdmn)
    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    hhcxa__rycyb = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(tsis__donu)
    wgiof__bwj = bodo.utils.utils.alloc_type(n, tsis__donu.dtype, (-1,))
    for borj__grzi in numba.parfors.parfor.internal_prange(n):
        s = tsis__donu[borj__grzi]
        if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi
            ) and not bodo.libs.array_kernels.isna(hhcxa__rycyb, borj__grzi):
            s = hhcxa__rycyb[borj__grzi]
        wgiof__bwj[borj__grzi] = s
    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    aqvfa__rols = dict(limit=limit, downcast=downcast)
    iuteq__bxjm = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', aqvfa__rols, iuteq__bxjm,
        package_name='pandas', module_name='Series')
    kvifw__ocr = not is_overload_none(value)
    ceqo__ywp = not is_overload_none(method)
    if kvifw__ocr and ceqo__ywp:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not kvifw__ocr and not ceqo__ywp:
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
    if ceqo__ywp:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        esqc__zhtml = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(esqc__zhtml)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(esqc__zhtml)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    xwxv__zqzpi = element_type(S.data)
    pbm__xijkt = None
    if kvifw__ocr:
        pbm__xijkt = element_type(types.unliteral(value))
    if pbm__xijkt and not can_replace(xwxv__zqzpi, pbm__xijkt):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {pbm__xijkt} with series type {xwxv__zqzpi}'
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
        thz__epwo = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                hhcxa__rycyb = bodo.hiframes.pd_series_ext.get_series_data(
                    value)
                n = len(tsis__donu)
                wgiof__bwj = bodo.utils.utils.alloc_type(n, thz__epwo, (-1,))
                for borj__grzi in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi
                        ) and bodo.libs.array_kernels.isna(hhcxa__rycyb,
                        borj__grzi):
                        bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                        continue
                    if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi):
                        wgiof__bwj[borj__grzi
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            hhcxa__rycyb[borj__grzi])
                        continue
                    wgiof__bwj[borj__grzi
                        ] = bodo.utils.conversion.unbox_if_timestamp(tsis__donu
                        [borj__grzi])
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return fillna_series_impl
        if ceqo__ywp:
            ppgfl__pvuea = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(xwxv__zqzpi, (types.Integer, types.Float)
                ) and xwxv__zqzpi not in ppgfl__pvuea:
                raise BodoError(
                    f"Series.fillna(): series of type {xwxv__zqzpi} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                wgiof__bwj = bodo.libs.array_kernels.ffill_bfill_arr(tsis__donu
                    , method)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(tsis__donu)
            wgiof__bwj = bodo.utils.utils.alloc_type(n, thz__epwo, (-1,))
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(tsis__donu[
                    borj__grzi])
                if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi):
                    s = value
                wgiof__bwj[borj__grzi] = s
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        cqfa__yihtx = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        aqvfa__rols = dict(limit=limit, downcast=downcast)
        iuteq__bxjm = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', aqvfa__rols,
            iuteq__bxjm, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        xwxv__zqzpi = element_type(S.data)
        ppgfl__pvuea = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(xwxv__zqzpi, (types.Integer, types.Float)
            ) and xwxv__zqzpi not in ppgfl__pvuea:
            raise BodoError(
                f'Series.{overload_name}(): series of type {xwxv__zqzpi} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            wgiof__bwj = bodo.libs.array_kernels.ffill_bfill_arr(tsis__donu,
                cqfa__yihtx)
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        yxc__khgo = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(yxc__khgo
            )


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        zkuf__znse = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(zkuf__znse)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        zkuf__znse = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(zkuf__znse)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        zkuf__znse = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(zkuf__znse)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    aqvfa__rols = dict(inplace=inplace, limit=limit, regex=regex, method=method
        )
    hphbv__nzf = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', aqvfa__rols, hphbv__nzf,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    xwxv__zqzpi = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        yjo__hcpq = element_type(to_replace.key_type)
        pbm__xijkt = element_type(to_replace.value_type)
    else:
        yjo__hcpq = element_type(to_replace)
        pbm__xijkt = element_type(value)
    pmrm__rpdh = None
    if xwxv__zqzpi != types.unliteral(yjo__hcpq):
        if bodo.utils.typing.equality_always_false(xwxv__zqzpi, types.
            unliteral(yjo__hcpq)
            ) or not bodo.utils.typing.types_equality_exists(xwxv__zqzpi,
            yjo__hcpq):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(xwxv__zqzpi, (types.Float, types.Integer)
            ) or xwxv__zqzpi == np.bool_:
            pmrm__rpdh = xwxv__zqzpi
    if not can_replace(xwxv__zqzpi, types.unliteral(pbm__xijkt)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    imtvg__hlh = to_str_arr_if_dict_array(S.data)
    if isinstance(imtvg__hlh, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(tsis__donu.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(tsis__donu)
        wgiof__bwj = bodo.utils.utils.alloc_type(n, imtvg__hlh, (-1,))
        vqoo__uxj = build_replace_dict(to_replace, value, pmrm__rpdh)
        for borj__grzi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(tsis__donu, borj__grzi):
                bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                continue
            s = tsis__donu[borj__grzi]
            if s in vqoo__uxj:
                s = vqoo__uxj[s]
            wgiof__bwj[borj__grzi] = s
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    vgue__lmbfr = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    tkezn__mmdxr = is_iterable_type(to_replace)
    txoae__qwx = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    wljl__cezza = is_iterable_type(value)
    if vgue__lmbfr and txoae__qwx:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vqoo__uxj = {}
                vqoo__uxj[key_dtype_conv(to_replace)] = value
                return vqoo__uxj
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vqoo__uxj = {}
            vqoo__uxj[to_replace] = value
            return vqoo__uxj
        return impl
    if tkezn__mmdxr and txoae__qwx:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vqoo__uxj = {}
                for hhgx__zomm in to_replace:
                    vqoo__uxj[key_dtype_conv(hhgx__zomm)] = value
                return vqoo__uxj
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vqoo__uxj = {}
            for hhgx__zomm in to_replace:
                vqoo__uxj[hhgx__zomm] = value
            return vqoo__uxj
        return impl
    if tkezn__mmdxr and wljl__cezza:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vqoo__uxj = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for borj__grzi in range(len(to_replace)):
                    vqoo__uxj[key_dtype_conv(to_replace[borj__grzi])] = value[
                        borj__grzi]
                return vqoo__uxj
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vqoo__uxj = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for borj__grzi in range(len(to_replace)):
                vqoo__uxj[to_replace[borj__grzi]] = value[borj__grzi]
            return vqoo__uxj
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
            wgiof__bwj = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgiof__bwj = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    aqvfa__rols = dict(ignore_index=ignore_index)
    wptpi__hjau = dict(ignore_index=False)
    check_unsupported_args('Series.explode', aqvfa__rols, wptpi__hjau,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qkizc__nyyis = bodo.utils.conversion.index_to_array(index)
        wgiof__bwj, opga__odct = bodo.libs.array_kernels.explode(arr,
            qkizc__nyyis)
        ctf__kaz = bodo.utils.conversion.index_from_array(opga__odct)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, ctf__kaz,
            name)
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
            hvs__zfs = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                hvs__zfs[borj__grzi] = np.argmax(a[borj__grzi])
            return hvs__zfs
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            jxtc__gxa = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                jxtc__gxa[borj__grzi] = np.argmin(a[borj__grzi])
            return jxtc__gxa
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
    aqvfa__rols = dict(axis=axis, inplace=inplace, how=how)
    xvind__ixfz = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', aqvfa__rols, xvind__ixfz,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            sqnk__bkw = S.notna().values
            qkizc__nyyis = bodo.utils.conversion.extract_index_array(S)
            ctf__kaz = bodo.utils.conversion.convert_to_index(qkizc__nyyis[
                sqnk__bkw])
            wgiof__bwj = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(tsis__donu))
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                ctf__kaz, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            qkizc__nyyis = bodo.utils.conversion.extract_index_array(S)
            sqnk__bkw = S.notna().values
            ctf__kaz = bodo.utils.conversion.convert_to_index(qkizc__nyyis[
                sqnk__bkw])
            wgiof__bwj = tsis__donu[sqnk__bkw]
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                ctf__kaz, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    aqvfa__rols = dict(freq=freq, axis=axis, fill_value=fill_value)
    iuteq__bxjm = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', aqvfa__rols, iuteq__bxjm,
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
        wgiof__bwj = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    aqvfa__rols = dict(fill_method=fill_method, limit=limit, freq=freq)
    iuteq__bxjm = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', aqvfa__rols, iuteq__bxjm,
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
        wgiof__bwj = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
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
            azgf__egmlb = 'None'
        else:
            azgf__egmlb = 'other'
        ihm__khfpz = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            ihm__khfpz += '  cond = ~cond\n'
        ihm__khfpz += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ihm__khfpz += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ihm__khfpz += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ihm__khfpz += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {azgf__egmlb})
"""
        ihm__khfpz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        tqtz__slp = {}
        exec(ihm__khfpz, {'bodo': bodo, 'np': np}, tqtz__slp)
        impl = tqtz__slp['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        yxc__khgo = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(yxc__khgo)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    aqvfa__rols = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    iuteq__bxjm = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', aqvfa__rols, iuteq__bxjm,
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
    oaot__fqx = is_overload_constant_nan(other)
    if not (is_default or oaot__fqx or is_scalar_type(other) or isinstance(
        other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
        isinstance(other, SeriesType) and (isinstance(arr, types.Array) or 
        arr.dtype in [bodo.string_type, bodo.bytes_type]) or 
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
            kxc__hsxw = arr.dtype.elem_type
        else:
            kxc__hsxw = arr.dtype
        if is_iterable_type(other):
            yccru__jmgo = other.dtype
        elif oaot__fqx:
            yccru__jmgo = types.float64
        else:
            yccru__jmgo = types.unliteral(other)
        if not oaot__fqx and not is_common_scalar_dtype([kxc__hsxw,
            yccru__jmgo]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        aqvfa__rols = dict(level=level, axis=axis)
        iuteq__bxjm = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), aqvfa__rols,
            iuteq__bxjm, package_name='pandas', module_name='Series')
        hcco__zfsuo = other == string_type or is_overload_constant_str(other)
        xrc__zzty = is_iterable_type(other) and other.dtype == string_type
        prv__oza = S.dtype == string_type and (op == operator.add and (
            hcco__zfsuo or xrc__zzty) or op == operator.mul and isinstance(
            other, types.Integer))
        grcf__qcy = S.dtype == bodo.timedelta64ns
        myl__wwy = S.dtype == bodo.datetime64ns
        vhua__fik = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        boi__dauh = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        nef__jbi = grcf__qcy and (vhua__fik or boi__dauh
            ) or myl__wwy and vhua__fik
        nef__jbi = nef__jbi and op == operator.add
        if not (isinstance(S.dtype, types.Number) or prv__oza or nef__jbi):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        yybep__ajssb = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            imtvg__hlh = yybep__ajssb.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and imtvg__hlh == types.Array(types.bool_, 1, 'C'):
                imtvg__hlh = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                wgiof__bwj = bodo.utils.utils.alloc_type(n, imtvg__hlh, (-1,))
                for borj__grzi in numba.parfors.parfor.internal_prange(n):
                    aixa__yzqz = bodo.libs.array_kernels.isna(arr, borj__grzi)
                    if aixa__yzqz:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(wgiof__bwj,
                                borj__grzi)
                        else:
                            wgiof__bwj[borj__grzi] = op(fill_value, other)
                    else:
                        wgiof__bwj[borj__grzi] = op(arr[borj__grzi], other)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        imtvg__hlh = yybep__ajssb.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType) and imtvg__hlh == types.Array(
            types.bool_, 1, 'C'):
            imtvg__hlh = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            tmxwk__paw = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            wgiof__bwj = bodo.utils.utils.alloc_type(n, imtvg__hlh, (-1,))
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                aixa__yzqz = bodo.libs.array_kernels.isna(arr, borj__grzi)
                ymg__xico = bodo.libs.array_kernels.isna(tmxwk__paw, borj__grzi
                    )
                if aixa__yzqz and ymg__xico:
                    bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                elif aixa__yzqz:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                    else:
                        wgiof__bwj[borj__grzi] = op(fill_value, tmxwk__paw[
                            borj__grzi])
                elif ymg__xico:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                    else:
                        wgiof__bwj[borj__grzi] = op(arr[borj__grzi], fill_value
                            )
                else:
                    wgiof__bwj[borj__grzi] = op(arr[borj__grzi], tmxwk__paw
                        [borj__grzi])
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
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
        yybep__ajssb = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            imtvg__hlh = yybep__ajssb.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and imtvg__hlh == types.Array(types.bool_, 1, 'C'):
                imtvg__hlh = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                wgiof__bwj = bodo.utils.utils.alloc_type(n, imtvg__hlh, None)
                for borj__grzi in numba.parfors.parfor.internal_prange(n):
                    aixa__yzqz = bodo.libs.array_kernels.isna(arr, borj__grzi)
                    if aixa__yzqz:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(wgiof__bwj,
                                borj__grzi)
                        else:
                            wgiof__bwj[borj__grzi] = op(other, fill_value)
                    else:
                        wgiof__bwj[borj__grzi] = op(other, arr[borj__grzi])
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        imtvg__hlh = yybep__ajssb.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType) and imtvg__hlh == types.Array(
            types.bool_, 1, 'C'):
            imtvg__hlh = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            tmxwk__paw = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            wgiof__bwj = bodo.utils.utils.alloc_type(n, imtvg__hlh, None)
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                aixa__yzqz = bodo.libs.array_kernels.isna(arr, borj__grzi)
                ymg__xico = bodo.libs.array_kernels.isna(tmxwk__paw, borj__grzi
                    )
                wgiof__bwj[borj__grzi] = op(tmxwk__paw[borj__grzi], arr[
                    borj__grzi])
                if aixa__yzqz and ymg__xico:
                    bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                elif aixa__yzqz:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                    else:
                        wgiof__bwj[borj__grzi] = op(tmxwk__paw[borj__grzi],
                            fill_value)
                elif ymg__xico:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                    else:
                        wgiof__bwj[borj__grzi] = op(fill_value, arr[borj__grzi]
                            )
                else:
                    wgiof__bwj[borj__grzi] = op(tmxwk__paw[borj__grzi], arr
                        [borj__grzi])
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
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
    for op, dlibn__wqmbz in explicit_binop_funcs_two_ways.items():
        for name in dlibn__wqmbz:
            yxc__khgo = create_explicit_binary_op_overload(op)
            arbs__zxq = create_explicit_binary_reverse_op_overload(op)
            jgbs__ics = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(yxc__khgo)
            overload_method(SeriesType, jgbs__ics, no_unliteral=True)(arbs__zxq
                )
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        yxc__khgo = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(yxc__khgo)
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
                lpu__zqunb = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                wgiof__bwj = dt64_arr_sub(arr, lpu__zqunb)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
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
                wgiof__bwj = np.empty(n, np.dtype('datetime64[ns]'))
                for borj__grzi in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, borj__grzi):
                        bodo.libs.array_kernels.setna(wgiof__bwj, borj__grzi)
                        continue
                    kam__fhphe = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[borj__grzi]))
                    gfprh__wzcn = op(kam__fhphe, rhs)
                    wgiof__bwj[borj__grzi
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gfprh__wzcn.value)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
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
                    lpu__zqunb = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    wgiof__bwj = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(lpu__zqunb))
                    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lpu__zqunb = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                wgiof__bwj = op(arr, lpu__zqunb)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    ijs__dxbum = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    wgiof__bwj = op(bodo.utils.conversion.
                        unbox_if_timestamp(ijs__dxbum), arr)
                    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                ijs__dxbum = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                wgiof__bwj = op(ijs__dxbum, arr)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        yxc__khgo = create_binary_op_overload(op)
        overload(op)(yxc__khgo)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    rxeq__iobk = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, rxeq__iobk)
        for borj__grzi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, borj__grzi
                ) or bodo.libs.array_kernels.isna(arg2, borj__grzi):
                bodo.libs.array_kernels.setna(S, borj__grzi)
                continue
            S[borj__grzi
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                borj__grzi]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[borj__grzi]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                tmxwk__paw = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, tmxwk__paw)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        yxc__khgo = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(yxc__khgo)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                wgiof__bwj = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        yxc__khgo = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(yxc__khgo)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    wgiof__bwj = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
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
                    tmxwk__paw = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    wgiof__bwj = ufunc(arr, tmxwk__paw)
                    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    tmxwk__paw = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    wgiof__bwj = ufunc(arr, tmxwk__paw)
                    return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        yxc__khgo = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(yxc__khgo)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        vde__hzzej = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),)
            )
        stuc__hzl = np.arange(n),
        bodo.libs.timsort.sort(vde__hzzej, 0, n, stuc__hzl)
        return stuc__hzl[0]
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
        oqmzb__isfsw = get_overload_const_str(downcast)
        if oqmzb__isfsw in ('integer', 'signed'):
            out_dtype = types.int64
        elif oqmzb__isfsw == 'unsigned':
            out_dtype = types.uint64
        else:
            assert oqmzb__isfsw == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            tsis__donu = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            wgiof__bwj = pd.to_numeric(tsis__donu, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            qxn__qqz = np.empty(n, np.float64)
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, borj__grzi):
                    bodo.libs.array_kernels.setna(qxn__qqz, borj__grzi)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(qxn__qqz,
                        borj__grzi, arg_a, borj__grzi)
            return qxn__qqz
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            qxn__qqz = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for borj__grzi in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, borj__grzi):
                    bodo.libs.array_kernels.setna(qxn__qqz, borj__grzi)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(qxn__qqz,
                        borj__grzi, arg_a, borj__grzi)
            return qxn__qqz
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        etzeh__aseah = if_series_to_array_type(args[0])
        if isinstance(etzeh__aseah, types.Array) and isinstance(etzeh__aseah
            .dtype, types.Integer):
            etzeh__aseah = types.Array(types.float64, 1, 'C')
        return etzeh__aseah(*args)


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
    vcmr__cbj = bodo.utils.utils.is_array_typ(x, True)
    wyt__mox = bodo.utils.utils.is_array_typ(y, True)
    ihm__khfpz = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        ihm__khfpz += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if vcmr__cbj and not bodo.utils.utils.is_array_typ(x, False):
        ihm__khfpz += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if wyt__mox and not bodo.utils.utils.is_array_typ(y, False):
        ihm__khfpz += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    ihm__khfpz += '  n = len(condition)\n'
    head__xiovf = x.dtype if vcmr__cbj else types.unliteral(x)
    pqvh__omraw = y.dtype if wyt__mox else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        head__xiovf = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        pqvh__omraw = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    wvpy__fkw = get_data(x)
    nzy__dtzaz = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(stuc__hzl) for
        stuc__hzl in [wvpy__fkw, nzy__dtzaz])
    if nzy__dtzaz == types.none:
        if isinstance(head__xiovf, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif wvpy__fkw == nzy__dtzaz and not is_nullable:
        out_dtype = dtype_to_array_type(head__xiovf)
    elif head__xiovf == string_type or pqvh__omraw == string_type:
        out_dtype = bodo.string_array_type
    elif wvpy__fkw == bytes_type or (vcmr__cbj and head__xiovf == bytes_type
        ) and (nzy__dtzaz == bytes_type or wyt__mox and pqvh__omraw ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(head__xiovf, bodo.PDCategoricalDtype):
        out_dtype = None
    elif head__xiovf in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(head__xiovf, 1, 'C')
    elif pqvh__omraw in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(pqvh__omraw, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(head__xiovf), numba.np.numpy_support.
            as_dtype(pqvh__omraw)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(head__xiovf, bodo.PDCategoricalDtype):
        xhu__qoqh = 'x'
    else:
        xhu__qoqh = 'out_dtype'
    ihm__khfpz += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {xhu__qoqh}, (-1,))\n')
    if isinstance(head__xiovf, bodo.PDCategoricalDtype):
        ihm__khfpz += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        ihm__khfpz += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    ihm__khfpz += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    ihm__khfpz += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if vcmr__cbj:
        ihm__khfpz += '      if bodo.libs.array_kernels.isna(x, j):\n'
        ihm__khfpz += '        setna(out_arr, j)\n'
        ihm__khfpz += '        continue\n'
    if isinstance(head__xiovf, bodo.PDCategoricalDtype):
        ihm__khfpz += '      out_codes[j] = x_codes[j]\n'
    else:
        ihm__khfpz += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if vcmr__cbj else 'x'))
    ihm__khfpz += '    else:\n'
    if wyt__mox:
        ihm__khfpz += '      if bodo.libs.array_kernels.isna(y, j):\n'
        ihm__khfpz += '        setna(out_arr, j)\n'
        ihm__khfpz += '        continue\n'
    if nzy__dtzaz == types.none:
        if isinstance(head__xiovf, bodo.PDCategoricalDtype):
            ihm__khfpz += '      out_codes[j] = -1\n'
        else:
            ihm__khfpz += '      setna(out_arr, j)\n'
    else:
        ihm__khfpz += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if wyt__mox else 'y'))
    ihm__khfpz += '  return out_arr\n'
    tqtz__slp = {}
    exec(ihm__khfpz, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, tqtz__slp)
    xtnfm__twy = tqtz__slp['_impl']
    return xtnfm__twy


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
        eeidm__debx = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(eeidm__debx, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(eeidm__debx):
            lnhf__ljir = eeidm__debx.data.dtype
        else:
            lnhf__ljir = eeidm__debx.dtype
        if isinstance(lnhf__ljir, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        hqsu__skmws = eeidm__debx
    else:
        pguv__wah = []
        for eeidm__debx in choicelist:
            if not bodo.utils.utils.is_array_typ(eeidm__debx, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(eeidm__debx):
                lnhf__ljir = eeidm__debx.data.dtype
            else:
                lnhf__ljir = eeidm__debx.dtype
            if isinstance(lnhf__ljir, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            pguv__wah.append(lnhf__ljir)
        if not is_common_scalar_dtype(pguv__wah):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        hqsu__skmws = choicelist[0]
    if is_series_type(hqsu__skmws):
        hqsu__skmws = hqsu__skmws.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, hqsu__skmws.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(hqsu__skmws, types.Array) or isinstance(hqsu__skmws,
        BooleanArrayType) or isinstance(hqsu__skmws, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(hqsu__skmws, False) and hqsu__skmws.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {hqsu__skmws} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    jerux__frsus = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        wkw__ribk = choicelist.dtype
    else:
        komnx__kuooe = False
        pguv__wah = []
        for eeidm__debx in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                eeidm__debx, 'numpy.select()')
            if is_nullable_type(eeidm__debx):
                komnx__kuooe = True
            if is_series_type(eeidm__debx):
                lnhf__ljir = eeidm__debx.data.dtype
            else:
                lnhf__ljir = eeidm__debx.dtype
            if isinstance(lnhf__ljir, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            pguv__wah.append(lnhf__ljir)
        rqpqv__wfn, aisox__huo = get_common_scalar_dtype(pguv__wah)
        if not aisox__huo:
            raise BodoError('Internal error in overload_np_select')
        jedx__xnb = dtype_to_array_type(rqpqv__wfn)
        if komnx__kuooe:
            jedx__xnb = to_nullable_type(jedx__xnb)
        wkw__ribk = jedx__xnb
    if isinstance(wkw__ribk, SeriesType):
        wkw__ribk = wkw__ribk.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        lkb__qzt = True
    else:
        lkb__qzt = False
    lpuz__jhh = False
    kvfng__hru = False
    if lkb__qzt:
        if isinstance(wkw__ribk.dtype, types.Number):
            pass
        elif wkw__ribk.dtype == types.bool_:
            kvfng__hru = True
        else:
            lpuz__jhh = True
            wkw__ribk = to_nullable_type(wkw__ribk)
    elif default == types.none or is_overload_constant_nan(default):
        lpuz__jhh = True
        wkw__ribk = to_nullable_type(wkw__ribk)
    ihm__khfpz = 'def np_select_impl(condlist, choicelist, default=0):\n'
    ihm__khfpz += '  if len(condlist) != len(choicelist):\n'
    ihm__khfpz += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    ihm__khfpz += '  output_len = len(choicelist[0])\n'
    ihm__khfpz += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    ihm__khfpz += '  for i in range(output_len):\n'
    if lpuz__jhh:
        ihm__khfpz += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif kvfng__hru:
        ihm__khfpz += '    out[i] = False\n'
    else:
        ihm__khfpz += '    out[i] = default\n'
    if jerux__frsus:
        ihm__khfpz += '  for i in range(len(condlist) - 1, -1, -1):\n'
        ihm__khfpz += '    cond = condlist[i]\n'
        ihm__khfpz += '    choice = choicelist[i]\n'
        ihm__khfpz += '    out = np.where(cond, choice, out)\n'
    else:
        for borj__grzi in range(len(choicelist) - 1, -1, -1):
            ihm__khfpz += f'  cond = condlist[{borj__grzi}]\n'
            ihm__khfpz += f'  choice = choicelist[{borj__grzi}]\n'
            ihm__khfpz += f'  out = np.where(cond, choice, out)\n'
    ihm__khfpz += '  return out'
    tqtz__slp = dict()
    exec(ihm__khfpz, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': wkw__ribk}, tqtz__slp)
    impl = tqtz__slp['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgiof__bwj = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    aqvfa__rols = dict(subset=subset, keep=keep, inplace=inplace)
    iuteq__bxjm = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', aqvfa__rols,
        iuteq__bxjm, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        jefu__gswy = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (jefu__gswy,), qkizc__nyyis = bodo.libs.array_kernels.drop_duplicates((
            jefu__gswy,), index, 1)
        index = bodo.utils.conversion.index_from_array(qkizc__nyyis)
        return bodo.hiframes.pd_series_ext.init_series(jefu__gswy, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    uyl__hby = element_type(S.data)
    if not is_common_scalar_dtype([uyl__hby, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([uyl__hby, right]):
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
        wgiof__bwj = np.empty(n, np.bool_)
        for borj__grzi in numba.parfors.parfor.internal_prange(n):
            sanx__slkx = bodo.utils.conversion.box_if_dt64(arr[borj__grzi])
            if inclusive == 'both':
                wgiof__bwj[borj__grzi
                    ] = sanx__slkx <= right and sanx__slkx >= left
            else:
                wgiof__bwj[borj__grzi
                    ] = sanx__slkx < right and sanx__slkx > left
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    aqvfa__rols = dict(axis=axis)
    iuteq__bxjm = dict(axis=None)
    check_unsupported_args('Series.repeat', aqvfa__rols, iuteq__bxjm,
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
            qkizc__nyyis = bodo.utils.conversion.index_to_array(index)
            wgiof__bwj = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            opga__odct = bodo.libs.array_kernels.repeat_kernel(qkizc__nyyis,
                repeats)
            ctf__kaz = bodo.utils.conversion.index_from_array(opga__odct)
            return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj,
                ctf__kaz, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qkizc__nyyis = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        wgiof__bwj = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        opga__odct = bodo.libs.array_kernels.repeat_kernel(qkizc__nyyis,
            repeats)
        ctf__kaz = bodo.utils.conversion.index_from_array(opga__odct)
        return bodo.hiframes.pd_series_ext.init_series(wgiof__bwj, ctf__kaz,
            name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        stuc__hzl = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(stuc__hzl)
        kai__yof = {}
        for borj__grzi in range(n):
            sanx__slkx = bodo.utils.conversion.box_if_dt64(stuc__hzl[
                borj__grzi])
            kai__yof[index[borj__grzi]] = sanx__slkx
        return kai__yof
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    esqc__zhtml = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            uek__iwz = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(esqc__zhtml)
    elif is_literal_type(name):
        uek__iwz = get_literal_value(name)
    else:
        raise_bodo_error(esqc__zhtml)
    uek__iwz = 0 if uek__iwz is None else uek__iwz

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (uek__iwz,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
