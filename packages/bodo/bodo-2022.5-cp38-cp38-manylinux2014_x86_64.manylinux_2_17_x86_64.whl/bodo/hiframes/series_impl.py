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
            vmoi__egn = bodo.hiframes.pd_series_ext.get_series_data(s)
            swj__hlzw = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(vmoi__egn
                )
            return swj__hlzw
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
            jkp__nncd = list()
            for yuqmk__tlty in range(len(S)):
                jkp__nncd.append(S.iat[yuqmk__tlty])
            return jkp__nncd
        return impl_float

    def impl(S):
        jkp__nncd = list()
        for yuqmk__tlty in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, yuqmk__tlty):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            jkp__nncd.append(S.iat[yuqmk__tlty])
        return jkp__nncd
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    gku__vydb = dict(dtype=dtype, copy=copy, na_value=na_value)
    cgy__lkwyl = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    gku__vydb = dict(name=name, inplace=inplace)
    cgy__lkwyl = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', gku__vydb, cgy__lkwyl,
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
        iwuid__hdg = ', '.join(['index_arrs[{}]'.format(yuqmk__tlty) for
            yuqmk__tlty in range(S.index.nlevels)])
    else:
        iwuid__hdg = '    bodo.utils.conversion.index_to_array(index)\n'
    ljau__fjzav = 'index' if 'index' != series_name else 'level_0'
    dek__xqn = get_index_names(S.index, 'Series.reset_index()', ljau__fjzav)
    columns = [name for name in dek__xqn]
    columns.append(series_name)
    rqe__jpv = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    rqe__jpv += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    rqe__jpv += '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        rqe__jpv += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    rqe__jpv += (
        '    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)\n'
        )
    rqe__jpv += '    col_var = {}\n'.format(gen_const_tup(columns))
    rqe__jpv += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({iwuid__hdg}, arr), df_index, col_var)
"""
    qycqg__solyt = {}
    exec(rqe__jpv, {'bodo': bodo}, qycqg__solyt)
    yayol__suudx = qycqg__solyt['_impl']
    return yayol__suudx


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qnsu__yaxsa = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
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
        qnsu__yaxsa = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[yuqmk__tlty]):
                bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
            else:
                qnsu__yaxsa[yuqmk__tlty] = np.round(arr[yuqmk__tlty], decimals)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    cgy__lkwyl = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        fqtnj__hdki = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = 0
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty):
                qrai__ovj = int(A[yuqmk__tlty])
            fqtnj__hdki += qrai__ovj
        return fqtnj__hdki != 0
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
        nce__ljq = bodo.hiframes.pd_series_ext.get_series_data(S)
        fmw__nfk = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        fqtnj__hdki = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(nce__ljq)):
            qrai__ovj = 0
            btqy__dsh = bodo.libs.array_kernels.isna(nce__ljq, yuqmk__tlty)
            muhxa__efk = bodo.libs.array_kernels.isna(fmw__nfk, yuqmk__tlty)
            if btqy__dsh and not muhxa__efk or not btqy__dsh and muhxa__efk:
                qrai__ovj = 1
            elif not btqy__dsh:
                if nce__ljq[yuqmk__tlty] != fmw__nfk[yuqmk__tlty]:
                    qrai__ovj = 1
            fqtnj__hdki += qrai__ovj
        return fqtnj__hdki == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    gku__vydb = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    cgy__lkwyl = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        fqtnj__hdki = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = 0
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty):
                qrai__ovj = int(not A[yuqmk__tlty])
            fqtnj__hdki += qrai__ovj
        return fqtnj__hdki == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    gku__vydb = dict(level=level)
    cgy__lkwyl = dict(level=None)
    check_unsupported_args('Series.mad', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    fba__lptbe = types.float64
    swtf__mdtv = types.float64
    if S.dtype == types.float32:
        fba__lptbe = types.float32
        swtf__mdtv = types.float32
    bjn__cnxkq = fba__lptbe(0)
    udy__dnsn = swtf__mdtv(0)
    yslmf__bbzig = swtf__mdtv(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        opw__fqhnr = bjn__cnxkq
        fqtnj__hdki = udy__dnsn
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = bjn__cnxkq
            bzbzj__lljdt = udy__dnsn
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty) or not skipna:
                qrai__ovj = A[yuqmk__tlty]
                bzbzj__lljdt = yslmf__bbzig
            opw__fqhnr += qrai__ovj
            fqtnj__hdki += bzbzj__lljdt
        slfi__xsj = bodo.hiframes.series_kernels._mean_handle_nan(opw__fqhnr,
            fqtnj__hdki)
        rugq__amr = bjn__cnxkq
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = bjn__cnxkq
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty) or not skipna:
                qrai__ovj = abs(A[yuqmk__tlty] - slfi__xsj)
            rugq__amr += qrai__ovj
        hdtab__awek = bodo.hiframes.series_kernels._mean_handle_nan(rugq__amr,
            fqtnj__hdki)
        return hdtab__awek
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    gku__vydb = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', gku__vydb, cgy__lkwyl,
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
        yjy__lto = 0
        diuwa__vcvt = 0
        fqtnj__hdki = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = 0
            bzbzj__lljdt = 0
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty) or not skipna:
                qrai__ovj = A[yuqmk__tlty]
                bzbzj__lljdt = 1
            yjy__lto += qrai__ovj
            diuwa__vcvt += qrai__ovj * qrai__ovj
            fqtnj__hdki += bzbzj__lljdt
        lcg__lkwr = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            yjy__lto, diuwa__vcvt, fqtnj__hdki, ddof)
        izkzf__dpoed = bodo.hiframes.series_kernels._sem_handle_nan(lcg__lkwr,
            fqtnj__hdki)
        return izkzf__dpoed
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', gku__vydb, cgy__lkwyl,
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
        yjy__lto = 0.0
        diuwa__vcvt = 0.0
        varj__acd = 0.0
        pqa__vzxyq = 0.0
        fqtnj__hdki = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = 0.0
            bzbzj__lljdt = 0
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty) or not skipna:
                qrai__ovj = np.float64(A[yuqmk__tlty])
                bzbzj__lljdt = 1
            yjy__lto += qrai__ovj
            diuwa__vcvt += qrai__ovj ** 2
            varj__acd += qrai__ovj ** 3
            pqa__vzxyq += qrai__ovj ** 4
            fqtnj__hdki += bzbzj__lljdt
        lcg__lkwr = bodo.hiframes.series_kernels.compute_kurt(yjy__lto,
            diuwa__vcvt, varj__acd, pqa__vzxyq, fqtnj__hdki)
        return lcg__lkwr
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', gku__vydb, cgy__lkwyl,
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
        yjy__lto = 0.0
        diuwa__vcvt = 0.0
        varj__acd = 0.0
        fqtnj__hdki = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(A)):
            qrai__ovj = 0.0
            bzbzj__lljdt = 0
            if not bodo.libs.array_kernels.isna(A, yuqmk__tlty) or not skipna:
                qrai__ovj = np.float64(A[yuqmk__tlty])
                bzbzj__lljdt = 1
            yjy__lto += qrai__ovj
            diuwa__vcvt += qrai__ovj ** 2
            varj__acd += qrai__ovj ** 3
            fqtnj__hdki += bzbzj__lljdt
        lcg__lkwr = bodo.hiframes.series_kernels.compute_skew(yjy__lto,
            diuwa__vcvt, varj__acd, fqtnj__hdki)
        return lcg__lkwr
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', gku__vydb, cgy__lkwyl,
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
        nce__ljq = bodo.hiframes.pd_series_ext.get_series_data(S)
        fmw__nfk = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        qbp__skexn = 0
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(nce__ljq)):
            ogo__ugz = nce__ljq[yuqmk__tlty]
            bnlc__zobvb = fmw__nfk[yuqmk__tlty]
            qbp__skexn += ogo__ugz * bnlc__zobvb
        return qbp__skexn
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    gku__vydb = dict(skipna=skipna)
    cgy__lkwyl = dict(skipna=True)
    check_unsupported_args('Series.cumsum', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(skipna=skipna)
    cgy__lkwyl = dict(skipna=True)
    check_unsupported_args('Series.cumprod', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(skipna=skipna)
    cgy__lkwyl = dict(skipna=True)
    check_unsupported_args('Series.cummin', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(skipna=skipna)
    cgy__lkwyl = dict(skipna=True)
    check_unsupported_args('Series.cummax', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    cgy__lkwyl = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        ytout__wuvd = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, ytout__wuvd, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    gku__vydb = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    cgy__lkwyl = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(level=level)
    cgy__lkwyl = dict(level=None)
    check_unsupported_args('Series.count', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    gku__vydb = dict(method=method, min_periods=min_periods)
    cgy__lkwyl = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        zvx__avsqu = S.sum()
        wgro__vbnd = other.sum()
        a = n * (S * other).sum() - zvx__avsqu * wgro__vbnd
        mpko__ifr = n * (S ** 2).sum() - zvx__avsqu ** 2
        tzeh__ebooe = n * (other ** 2).sum() - wgro__vbnd ** 2
        return a / np.sqrt(mpko__ifr * tzeh__ebooe)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    gku__vydb = dict(min_periods=min_periods)
    cgy__lkwyl = dict(min_periods=None)
    check_unsupported_args('Series.cov', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        zvx__avsqu = S.mean()
        wgro__vbnd = other.mean()
        xatjg__jkh = ((S - zvx__avsqu) * (other - wgro__vbnd)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(xatjg__jkh, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            hbu__mxt = np.sign(sum_val)
            return np.inf * hbu__mxt
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    gku__vydb = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(axis=axis, skipna=skipna)
    cgy__lkwyl = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(axis=axis, skipna=skipna)
    cgy__lkwyl = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', gku__vydb, cgy__lkwyl,
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
    gku__vydb = dict(level=level, numeric_only=numeric_only)
    cgy__lkwyl = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', gku__vydb, cgy__lkwyl,
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
        czy__hzpls = arr[:n]
        ske__hnqmh = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(czy__hzpls,
            ske__hnqmh, name)
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
        tev__xbcp = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        czy__hzpls = arr[tev__xbcp:]
        ske__hnqmh = index[tev__xbcp:]
        return bodo.hiframes.pd_series_ext.init_series(czy__hzpls,
            ske__hnqmh, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    zqa__ugchs = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in zqa__ugchs:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            jndtl__lhpmb = index[0]
            osum__qshkx = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                jndtl__lhpmb, False))
        else:
            osum__qshkx = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        czy__hzpls = arr[:osum__qshkx]
        ske__hnqmh = index[:osum__qshkx]
        return bodo.hiframes.pd_series_ext.init_series(czy__hzpls,
            ske__hnqmh, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    zqa__ugchs = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in zqa__ugchs:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            ebwl__ijard = index[-1]
            osum__qshkx = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                ebwl__ijard, True))
        else:
            osum__qshkx = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        czy__hzpls = arr[len(arr) - osum__qshkx:]
        ske__hnqmh = index[len(arr) - osum__qshkx:]
        return bodo.hiframes.pd_series_ext.init_series(czy__hzpls,
            ske__hnqmh, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hmnj__tcdp = bodo.utils.conversion.index_to_array(index)
        ryns__swh, fdaum__xdvw = (bodo.libs.array_kernels.
            first_last_valid_index(arr, hmnj__tcdp))
        return fdaum__xdvw if ryns__swh else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hmnj__tcdp = bodo.utils.conversion.index_to_array(index)
        ryns__swh, fdaum__xdvw = (bodo.libs.array_kernels.
            first_last_valid_index(arr, hmnj__tcdp, False))
        return fdaum__xdvw if ryns__swh else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    gku__vydb = dict(keep=keep)
    cgy__lkwyl = dict(keep='first')
    check_unsupported_args('Series.nlargest', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hmnj__tcdp = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qnsu__yaxsa, mji__gmet = bodo.libs.array_kernels.nlargest(arr,
            hmnj__tcdp, n, True, bodo.hiframes.series_kernels.gt_f)
        hhd__yyj = bodo.utils.conversion.convert_to_index(mji__gmet)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
            hhd__yyj, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    gku__vydb = dict(keep=keep)
    cgy__lkwyl = dict(keep='first')
    check_unsupported_args('Series.nsmallest', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hmnj__tcdp = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qnsu__yaxsa, mji__gmet = bodo.libs.array_kernels.nlargest(arr,
            hmnj__tcdp, n, False, bodo.hiframes.series_kernels.lt_f)
        hhd__yyj = bodo.utils.conversion.convert_to_index(mji__gmet)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
            hhd__yyj, name)
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
    gku__vydb = dict(errors=errors)
    cgy__lkwyl = dict(errors='raise')
    check_unsupported_args('Series.astype', gku__vydb, cgy__lkwyl,
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
        qnsu__yaxsa = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    gku__vydb = dict(axis=axis, is_copy=is_copy)
    cgy__lkwyl = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        hkzhx__kylta = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[hkzhx__kylta],
            index[hkzhx__kylta], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    gku__vydb = dict(axis=axis, kind=kind, order=order)
    cgy__lkwyl = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        tirl__thgv = S.notna().values
        if not tirl__thgv.all():
            qnsu__yaxsa = np.full(n, -1, np.int64)
            qnsu__yaxsa[tirl__thgv] = argsort(arr[tirl__thgv])
        else:
            qnsu__yaxsa = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    gku__vydb = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    cgy__lkwyl = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', gku__vydb, cgy__lkwyl,
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
        zwfj__mqyjq = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        cuiv__rkudu = zwfj__mqyjq.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        qnsu__yaxsa = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            cuiv__rkudu, 0)
        hhd__yyj = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            cuiv__rkudu)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
            hhd__yyj, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    gku__vydb = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    cgy__lkwyl = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', gku__vydb, cgy__lkwyl,
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
        zwfj__mqyjq = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        cuiv__rkudu = zwfj__mqyjq.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        qnsu__yaxsa = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            cuiv__rkudu, 0)
        hhd__yyj = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            cuiv__rkudu)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
            hhd__yyj, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    jsnmq__ceq = is_overload_true(is_nullable)
    rqe__jpv = 'def impl(bins, arr, is_nullable=True, include_lowest=True):\n'
    rqe__jpv += '  numba.parfors.parfor.init_prange()\n'
    rqe__jpv += '  n = len(arr)\n'
    if jsnmq__ceq:
        rqe__jpv += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        rqe__jpv += '  out_arr = np.empty(n, np.int64)\n'
    rqe__jpv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    rqe__jpv += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if jsnmq__ceq:
        rqe__jpv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        rqe__jpv += '      out_arr[i] = -1\n'
    rqe__jpv += '      continue\n'
    rqe__jpv += '    val = arr[i]\n'
    rqe__jpv += '    if include_lowest and val == bins[0]:\n'
    rqe__jpv += '      ind = 1\n'
    rqe__jpv += '    else:\n'
    rqe__jpv += '      ind = np.searchsorted(bins, val)\n'
    rqe__jpv += '    if ind == 0 or ind == len(bins):\n'
    if jsnmq__ceq:
        rqe__jpv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        rqe__jpv += '      out_arr[i] = -1\n'
    rqe__jpv += '    else:\n'
    rqe__jpv += '      out_arr[i] = ind - 1\n'
    rqe__jpv += '  return out_arr\n'
    qycqg__solyt = {}
    exec(rqe__jpv, {'bodo': bodo, 'np': np, 'numba': numba}, qycqg__solyt)
    impl = qycqg__solyt['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        urxqn__nbzlf, zcdq__yxskx = np.divmod(x, 1)
        if urxqn__nbzlf == 0:
            vrf__jfut = -int(np.floor(np.log10(abs(zcdq__yxskx)))
                ) - 1 + precision
        else:
            vrf__jfut = precision
        return np.around(x, vrf__jfut)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        bruwe__tfs = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(bruwe__tfs)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        dow__piu = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            ahc__gzgwh = bins.copy()
            if right and include_lowest:
                ahc__gzgwh[0] = ahc__gzgwh[0] - dow__piu
            ahjry__queo = bodo.libs.interval_arr_ext.init_interval_array(
                ahc__gzgwh[:-1], ahc__gzgwh[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(ahjry__queo,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        ahc__gzgwh = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            ahc__gzgwh[0] = ahc__gzgwh[0] - 10.0 ** -precision
        ahjry__queo = bodo.libs.interval_arr_ext.init_interval_array(ahc__gzgwh
            [:-1], ahc__gzgwh[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(ahjry__queo, None
            )
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        vysy__ozyez = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        jssbw__vsse = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        qnsu__yaxsa = np.zeros(nbins, np.int64)
        for yuqmk__tlty in range(len(vysy__ozyez)):
            qnsu__yaxsa[jssbw__vsse[yuqmk__tlty]] = vysy__ozyez[yuqmk__tlty]
        return qnsu__yaxsa
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
            oifds__ytnr = (max_val - min_val) * 0.001
            if right:
                bins[0] -= oifds__ytnr
            else:
                bins[-1] += oifds__ytnr
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    gku__vydb = dict(dropna=dropna)
    cgy__lkwyl = dict(dropna=True)
    check_unsupported_args('Series.value_counts', gku__vydb, cgy__lkwyl,
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
    ztwr__lsrh = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    rqe__jpv = 'def impl(\n'
    rqe__jpv += '    S,\n'
    rqe__jpv += '    normalize=False,\n'
    rqe__jpv += '    sort=True,\n'
    rqe__jpv += '    ascending=False,\n'
    rqe__jpv += '    bins=None,\n'
    rqe__jpv += '    dropna=True,\n'
    rqe__jpv += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    rqe__jpv += '):\n'
    rqe__jpv += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    rqe__jpv += '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    rqe__jpv += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if ztwr__lsrh:
        rqe__jpv += '    right = True\n'
        rqe__jpv += _gen_bins_handling(bins, S.dtype)
        rqe__jpv += '    arr = get_bin_inds(bins, arr)\n'
    rqe__jpv += '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n'
    rqe__jpv += "        (arr,), index, ('$_bodo_col2_',)\n"
    rqe__jpv += '    )\n'
    rqe__jpv += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if ztwr__lsrh:
        rqe__jpv += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        rqe__jpv += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        rqe__jpv += '    index = get_bin_labels(bins)\n'
    else:
        rqe__jpv += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        rqe__jpv += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        rqe__jpv += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        rqe__jpv += '    )\n'
        rqe__jpv += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    rqe__jpv += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        rqe__jpv += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        ymsu__fvs = 'len(S)' if ztwr__lsrh else 'count_arr.sum()'
        rqe__jpv += f'    res = res / float({ymsu__fvs})\n'
    rqe__jpv += '    return res\n'
    qycqg__solyt = {}
    exec(rqe__jpv, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, qycqg__solyt)
    impl = qycqg__solyt['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    rqe__jpv = ''
    if isinstance(bins, types.Integer):
        rqe__jpv += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        rqe__jpv += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            rqe__jpv += '    min_val = min_val.value\n'
            rqe__jpv += '    max_val = max_val.value\n'
        rqe__jpv += '    bins = compute_bins(bins, min_val, max_val, right)\n'
        if dtype == bodo.datetime64ns:
            rqe__jpv += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        rqe__jpv += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return rqe__jpv


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    gku__vydb = dict(right=right, labels=labels, retbins=retbins, precision
        =precision, duplicates=duplicates, ordered=ordered)
    cgy__lkwyl = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    rqe__jpv = 'def impl(\n'
    rqe__jpv += '    x,\n'
    rqe__jpv += '    bins,\n'
    rqe__jpv += '    right=True,\n'
    rqe__jpv += '    labels=None,\n'
    rqe__jpv += '    retbins=False,\n'
    rqe__jpv += '    precision=3,\n'
    rqe__jpv += '    include_lowest=False,\n'
    rqe__jpv += "    duplicates='raise',\n"
    rqe__jpv += '    ordered=True\n'
    rqe__jpv += '):\n'
    if isinstance(x, SeriesType):
        rqe__jpv += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        rqe__jpv += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        rqe__jpv += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        rqe__jpv += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    rqe__jpv += _gen_bins_handling(bins, x.dtype)
    rqe__jpv += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    rqe__jpv += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    rqe__jpv += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    rqe__jpv += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        rqe__jpv += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        rqe__jpv += '    return res\n'
    else:
        rqe__jpv += '    return out_arr\n'
    qycqg__solyt = {}
    exec(rqe__jpv, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, qycqg__solyt)
    impl = qycqg__solyt['impl']
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
    gku__vydb = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    cgy__lkwyl = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        egopt__psol = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, egopt__psol)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    gku__vydb = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    cgy__lkwyl = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', gku__vydb, cgy__lkwyl,
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
            jkbi__peex = bodo.utils.conversion.coerce_to_array(index)
            zwfj__mqyjq = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                jkbi__peex, arr), index, (' ', ''))
            return zwfj__mqyjq.groupby(' ')['']
        return impl_index
    dfp__vwilq = by
    if isinstance(by, SeriesType):
        dfp__vwilq = by.data
    if isinstance(dfp__vwilq, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        jkbi__peex = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        zwfj__mqyjq = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            jkbi__peex, arr), index, (' ', ''))
        return zwfj__mqyjq.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    gku__vydb = dict(verify_integrity=verify_integrity)
    cgy__lkwyl = dict(verify_integrity=False)
    check_unsupported_args('Series.append', gku__vydb, cgy__lkwyl,
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
            zddi__zlm = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            qnsu__yaxsa = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(qnsu__yaxsa, A, zddi__zlm, False)
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qnsu__yaxsa = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    gku__vydb = dict(interpolation=interpolation)
    cgy__lkwyl = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            qnsu__yaxsa = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
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
        ifa__owlu = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(ifa__owlu, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    gku__vydb = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    cgy__lkwyl = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', gku__vydb, cgy__lkwyl,
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
        hcl__lzlrm = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        hcl__lzlrm = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    rqe__jpv = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {hcl__lzlrm}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    stzl__wzi = dict()
    exec(rqe__jpv, {'bodo': bodo, 'numba': numba}, stzl__wzi)
    kmm__wpbex = stzl__wzi['impl']
    return kmm__wpbex


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        hcl__lzlrm = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        hcl__lzlrm = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    rqe__jpv = 'def impl(S,\n'
    rqe__jpv += '     value=None,\n'
    rqe__jpv += '    method=None,\n'
    rqe__jpv += '    axis=None,\n'
    rqe__jpv += '    inplace=False,\n'
    rqe__jpv += '    limit=None,\n'
    rqe__jpv += '   downcast=None,\n'
    rqe__jpv += '):\n'
    rqe__jpv += '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    rqe__jpv += '    n = len(in_arr)\n'
    rqe__jpv += f'    out_arr = {hcl__lzlrm}(n, -1)\n'
    rqe__jpv += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    rqe__jpv += '        s = in_arr[j]\n'
    rqe__jpv += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    rqe__jpv += '            s = value\n'
    rqe__jpv += '        out_arr[j] = s\n'
    rqe__jpv += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    stzl__wzi = dict()
    exec(rqe__jpv, {'bodo': bodo, 'numba': numba}, stzl__wzi)
    kmm__wpbex = stzl__wzi['impl']
    return kmm__wpbex


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
    nlcu__irfg = bodo.hiframes.pd_series_ext.get_series_data(value)
    for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(rnpvt__hqs)):
        s = rnpvt__hqs[yuqmk__tlty]
        if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty
            ) and not bodo.libs.array_kernels.isna(nlcu__irfg, yuqmk__tlty):
            s = nlcu__irfg[yuqmk__tlty]
        rnpvt__hqs[yuqmk__tlty] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
    for yuqmk__tlty in numba.parfors.parfor.internal_prange(len(rnpvt__hqs)):
        s = rnpvt__hqs[yuqmk__tlty]
        if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty):
            s = value
        rnpvt__hqs[yuqmk__tlty] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nlcu__irfg = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(rnpvt__hqs)
    qnsu__yaxsa = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for vhac__jwtg in numba.parfors.parfor.internal_prange(n):
        s = rnpvt__hqs[vhac__jwtg]
        if bodo.libs.array_kernels.isna(rnpvt__hqs, vhac__jwtg
            ) and not bodo.libs.array_kernels.isna(nlcu__irfg, vhac__jwtg):
            s = nlcu__irfg[vhac__jwtg]
        qnsu__yaxsa[vhac__jwtg] = s
        if bodo.libs.array_kernels.isna(rnpvt__hqs, vhac__jwtg
            ) and bodo.libs.array_kernels.isna(nlcu__irfg, vhac__jwtg):
            bodo.libs.array_kernels.setna(qnsu__yaxsa, vhac__jwtg)
    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nlcu__irfg = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(rnpvt__hqs)
    qnsu__yaxsa = bodo.utils.utils.alloc_type(n, rnpvt__hqs.dtype, (-1,))
    for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
        s = rnpvt__hqs[yuqmk__tlty]
        if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty
            ) and not bodo.libs.array_kernels.isna(nlcu__irfg, yuqmk__tlty):
            s = nlcu__irfg[yuqmk__tlty]
        qnsu__yaxsa[yuqmk__tlty] = s
    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    gku__vydb = dict(limit=limit, downcast=downcast)
    cgy__lkwyl = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')
    etsi__ckime = not is_overload_none(value)
    droq__mdymc = not is_overload_none(method)
    if etsi__ckime and droq__mdymc:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not etsi__ckime and not droq__mdymc:
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
    if droq__mdymc:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        yme__cqnc = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(yme__cqnc)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(yme__cqnc)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    yzbph__chli = element_type(S.data)
    fofq__jux = None
    if etsi__ckime:
        fofq__jux = element_type(types.unliteral(value))
    if fofq__jux and not can_replace(yzbph__chli, fofq__jux):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {fofq__jux} with series type {yzbph__chli}'
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
        nids__wip = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                nlcu__irfg = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(rnpvt__hqs)
                qnsu__yaxsa = bodo.utils.utils.alloc_type(n, nids__wip, (-1,))
                for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty
                        ) and bodo.libs.array_kernels.isna(nlcu__irfg,
                        yuqmk__tlty):
                        bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                        continue
                    if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty):
                        qnsu__yaxsa[yuqmk__tlty
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            nlcu__irfg[yuqmk__tlty])
                        continue
                    qnsu__yaxsa[yuqmk__tlty
                        ] = bodo.utils.conversion.unbox_if_timestamp(rnpvt__hqs
                        [yuqmk__tlty])
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return fillna_series_impl
        if droq__mdymc:
            ygr__zegp = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(yzbph__chli, (types.Integer, types.Float)
                ) and yzbph__chli not in ygr__zegp:
                raise BodoError(
                    f"Series.fillna(): series of type {yzbph__chli} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                qnsu__yaxsa = bodo.libs.array_kernels.ffill_bfill_arr(
                    rnpvt__hqs, method)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(rnpvt__hqs)
            qnsu__yaxsa = bodo.utils.utils.alloc_type(n, nids__wip, (-1,))
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(rnpvt__hqs[
                    yuqmk__tlty])
                if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty):
                    s = value
                qnsu__yaxsa[yuqmk__tlty] = s
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        twwon__xswh = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        gku__vydb = dict(limit=limit, downcast=downcast)
        cgy__lkwyl = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', gku__vydb,
            cgy__lkwyl, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        yzbph__chli = element_type(S.data)
        ygr__zegp = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(yzbph__chli, (types.Integer, types.Float)
            ) and yzbph__chli not in ygr__zegp:
            raise BodoError(
                f'Series.{overload_name}(): series of type {yzbph__chli} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            qnsu__yaxsa = bodo.libs.array_kernels.ffill_bfill_arr(rnpvt__hqs,
                twwon__xswh)
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        axaac__chort = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            axaac__chort)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        rhl__nea = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(rhl__nea)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        rhl__nea = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(rhl__nea)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        rhl__nea = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(rhl__nea)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    gku__vydb = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    anng__rqjd = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', gku__vydb, anng__rqjd,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    yzbph__chli = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        lza__mta = element_type(to_replace.key_type)
        fofq__jux = element_type(to_replace.value_type)
    else:
        lza__mta = element_type(to_replace)
        fofq__jux = element_type(value)
    mdrs__aylpc = None
    if yzbph__chli != types.unliteral(lza__mta):
        if bodo.utils.typing.equality_always_false(yzbph__chli, types.
            unliteral(lza__mta)
            ) or not bodo.utils.typing.types_equality_exists(yzbph__chli,
            lza__mta):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(yzbph__chli, (types.Float, types.Integer)
            ) or yzbph__chli == np.bool_:
            mdrs__aylpc = yzbph__chli
    if not can_replace(yzbph__chli, types.unliteral(fofq__jux)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    dilbq__dfy = to_str_arr_if_dict_array(S.data)
    if isinstance(dilbq__dfy, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(rnpvt__hqs.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(rnpvt__hqs)
        qnsu__yaxsa = bodo.utils.utils.alloc_type(n, dilbq__dfy, (-1,))
        nsg__rntkx = build_replace_dict(to_replace, value, mdrs__aylpc)
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(rnpvt__hqs, yuqmk__tlty):
                bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                continue
            s = rnpvt__hqs[yuqmk__tlty]
            if s in nsg__rntkx:
                s = nsg__rntkx[s]
            qnsu__yaxsa[yuqmk__tlty] = s
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    xlm__ctxiq = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    gnb__uujck = is_iterable_type(to_replace)
    mue__hgjg = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    olerl__nke = is_iterable_type(value)
    if xlm__ctxiq and mue__hgjg:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                nsg__rntkx = {}
                nsg__rntkx[key_dtype_conv(to_replace)] = value
                return nsg__rntkx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            nsg__rntkx = {}
            nsg__rntkx[to_replace] = value
            return nsg__rntkx
        return impl
    if gnb__uujck and mue__hgjg:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                nsg__rntkx = {}
                for kjus__srrkm in to_replace:
                    nsg__rntkx[key_dtype_conv(kjus__srrkm)] = value
                return nsg__rntkx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            nsg__rntkx = {}
            for kjus__srrkm in to_replace:
                nsg__rntkx[kjus__srrkm] = value
            return nsg__rntkx
        return impl
    if gnb__uujck and olerl__nke:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                nsg__rntkx = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for yuqmk__tlty in range(len(to_replace)):
                    nsg__rntkx[key_dtype_conv(to_replace[yuqmk__tlty])
                        ] = value[yuqmk__tlty]
                return nsg__rntkx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            nsg__rntkx = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for yuqmk__tlty in range(len(to_replace)):
                nsg__rntkx[to_replace[yuqmk__tlty]] = value[yuqmk__tlty]
            return nsg__rntkx
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
            qnsu__yaxsa = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qnsu__yaxsa = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    gku__vydb = dict(ignore_index=ignore_index)
    loh__iwupl = dict(ignore_index=False)
    check_unsupported_args('Series.explode', gku__vydb, loh__iwupl,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hmnj__tcdp = bodo.utils.conversion.index_to_array(index)
        qnsu__yaxsa, lsroh__ocjk = bodo.libs.array_kernels.explode(arr,
            hmnj__tcdp)
        hhd__yyj = bodo.utils.conversion.index_from_array(lsroh__ocjk)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
            hhd__yyj, name)
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
            vwy__xvcgr = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                vwy__xvcgr[yuqmk__tlty] = np.argmax(a[yuqmk__tlty])
            return vwy__xvcgr
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            nqi__zqkzx = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                nqi__zqkzx[yuqmk__tlty] = np.argmin(a[yuqmk__tlty])
            return nqi__zqkzx
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
    gku__vydb = dict(axis=axis, inplace=inplace, how=how)
    wktm__dtnh = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', gku__vydb, wktm__dtnh,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            tirl__thgv = S.notna().values
            hmnj__tcdp = bodo.utils.conversion.extract_index_array(S)
            hhd__yyj = bodo.utils.conversion.convert_to_index(hmnj__tcdp[
                tirl__thgv])
            qnsu__yaxsa = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(rnpvt__hqs))
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                hhd__yyj, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            hmnj__tcdp = bodo.utils.conversion.extract_index_array(S)
            tirl__thgv = S.notna().values
            hhd__yyj = bodo.utils.conversion.convert_to_index(hmnj__tcdp[
                tirl__thgv])
            qnsu__yaxsa = rnpvt__hqs[tirl__thgv]
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                hhd__yyj, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    gku__vydb = dict(freq=freq, axis=axis, fill_value=fill_value)
    cgy__lkwyl = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', gku__vydb, cgy__lkwyl,
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
        qnsu__yaxsa = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    gku__vydb = dict(fill_method=fill_method, limit=limit, freq=freq)
    cgy__lkwyl = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', gku__vydb, cgy__lkwyl,
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
        qnsu__yaxsa = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
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
            znxev__hqdea = 'None'
        else:
            znxev__hqdea = 'other'
        rqe__jpv = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            rqe__jpv += '  cond = ~cond\n'
        rqe__jpv += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        rqe__jpv += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rqe__jpv += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
        rqe__jpv += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {znxev__hqdea})\n'
            )
        rqe__jpv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        qycqg__solyt = {}
        exec(rqe__jpv, {'bodo': bodo, 'np': np}, qycqg__solyt)
        impl = qycqg__solyt['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        axaac__chort = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(axaac__chort)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    gku__vydb = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    cgy__lkwyl = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', gku__vydb, cgy__lkwyl,
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
    hnq__nqu = is_overload_constant_nan(other)
    if not (is_default or hnq__nqu or is_scalar_type(other) or isinstance(
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
            kts__azr = arr.dtype.elem_type
        else:
            kts__azr = arr.dtype
        if is_iterable_type(other):
            pokv__gcvn = other.dtype
        elif hnq__nqu:
            pokv__gcvn = types.float64
        else:
            pokv__gcvn = types.unliteral(other)
        if not hnq__nqu and not is_common_scalar_dtype([kts__azr, pokv__gcvn]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        gku__vydb = dict(level=level, axis=axis)
        cgy__lkwyl = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), gku__vydb,
            cgy__lkwyl, package_name='pandas', module_name='Series')
        qdvgc__gnhl = other == string_type or is_overload_constant_str(other)
        botq__ezws = is_iterable_type(other) and other.dtype == string_type
        emxw__luyq = S.dtype == string_type and (op == operator.add and (
            qdvgc__gnhl or botq__ezws) or op == operator.mul and isinstance
            (other, types.Integer))
        gtm__rih = S.dtype == bodo.timedelta64ns
        wlx__gdc = S.dtype == bodo.datetime64ns
        pti__ton = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        crmnr__ahgv = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        eiu__lpena = gtm__rih and (pti__ton or crmnr__ahgv
            ) or wlx__gdc and pti__ton
        eiu__lpena = eiu__lpena and op == operator.add
        if not (isinstance(S.dtype, types.Number) or emxw__luyq or eiu__lpena):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        dbf__pakht = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            dilbq__dfy = dbf__pakht.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and dilbq__dfy == types.Array(types.bool_, 1, 'C'):
                dilbq__dfy = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                qnsu__yaxsa = bodo.utils.utils.alloc_type(n, dilbq__dfy, (-1,))
                for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                    feu__rhfd = bodo.libs.array_kernels.isna(arr, yuqmk__tlty)
                    if feu__rhfd:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(qnsu__yaxsa,
                                yuqmk__tlty)
                        else:
                            qnsu__yaxsa[yuqmk__tlty] = op(fill_value, other)
                    else:
                        qnsu__yaxsa[yuqmk__tlty] = op(arr[yuqmk__tlty], other)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        dilbq__dfy = dbf__pakht.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and dilbq__dfy == types.Array(
            types.bool_, 1, 'C'):
            dilbq__dfy = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ruy__rojh = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            qnsu__yaxsa = bodo.utils.utils.alloc_type(n, dilbq__dfy, (-1,))
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                feu__rhfd = bodo.libs.array_kernels.isna(arr, yuqmk__tlty)
                axt__aiwwj = bodo.libs.array_kernels.isna(ruy__rojh,
                    yuqmk__tlty)
                if feu__rhfd and axt__aiwwj:
                    bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                elif feu__rhfd:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                    else:
                        qnsu__yaxsa[yuqmk__tlty] = op(fill_value, ruy__rojh
                            [yuqmk__tlty])
                elif axt__aiwwj:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                    else:
                        qnsu__yaxsa[yuqmk__tlty] = op(arr[yuqmk__tlty],
                            fill_value)
                else:
                    qnsu__yaxsa[yuqmk__tlty] = op(arr[yuqmk__tlty],
                        ruy__rojh[yuqmk__tlty])
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
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
        dbf__pakht = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            dilbq__dfy = dbf__pakht.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and dilbq__dfy == types.Array(types.bool_, 1, 'C'):
                dilbq__dfy = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                qnsu__yaxsa = bodo.utils.utils.alloc_type(n, dilbq__dfy, None)
                for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                    feu__rhfd = bodo.libs.array_kernels.isna(arr, yuqmk__tlty)
                    if feu__rhfd:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(qnsu__yaxsa,
                                yuqmk__tlty)
                        else:
                            qnsu__yaxsa[yuqmk__tlty] = op(other, fill_value)
                    else:
                        qnsu__yaxsa[yuqmk__tlty] = op(other, arr[yuqmk__tlty])
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        dilbq__dfy = dbf__pakht.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and dilbq__dfy == types.Array(
            types.bool_, 1, 'C'):
            dilbq__dfy = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ruy__rojh = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            qnsu__yaxsa = bodo.utils.utils.alloc_type(n, dilbq__dfy, None)
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                feu__rhfd = bodo.libs.array_kernels.isna(arr, yuqmk__tlty)
                axt__aiwwj = bodo.libs.array_kernels.isna(ruy__rojh,
                    yuqmk__tlty)
                qnsu__yaxsa[yuqmk__tlty] = op(ruy__rojh[yuqmk__tlty], arr[
                    yuqmk__tlty])
                if feu__rhfd and axt__aiwwj:
                    bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                elif feu__rhfd:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                    else:
                        qnsu__yaxsa[yuqmk__tlty] = op(ruy__rojh[yuqmk__tlty
                            ], fill_value)
                elif axt__aiwwj:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                    else:
                        qnsu__yaxsa[yuqmk__tlty] = op(fill_value, arr[
                            yuqmk__tlty])
                else:
                    qnsu__yaxsa[yuqmk__tlty] = op(ruy__rojh[yuqmk__tlty],
                        arr[yuqmk__tlty])
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
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
    for op, vgzro__hxza in explicit_binop_funcs_two_ways.items():
        for name in vgzro__hxza:
            axaac__chort = create_explicit_binary_op_overload(op)
            krds__ikh = create_explicit_binary_reverse_op_overload(op)
            tcmex__xemz = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(axaac__chort)
            overload_method(SeriesType, tcmex__xemz, no_unliteral=True)(
                krds__ikh)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        axaac__chort = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(axaac__chort)
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
                bfkjd__xnheo = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                qnsu__yaxsa = dt64_arr_sub(arr, bfkjd__xnheo)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
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
                qnsu__yaxsa = np.empty(n, np.dtype('datetime64[ns]'))
                for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, yuqmk__tlty):
                        bodo.libs.array_kernels.setna(qnsu__yaxsa, yuqmk__tlty)
                        continue
                    onq__xcna = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[yuqmk__tlty]))
                    ehh__yvnxn = op(onq__xcna, rhs)
                    qnsu__yaxsa[yuqmk__tlty
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        ehh__yvnxn.value)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
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
                    bfkjd__xnheo = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    qnsu__yaxsa = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(bfkjd__xnheo))
                    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                bfkjd__xnheo = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                qnsu__yaxsa = op(arr, bfkjd__xnheo)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    xndcl__nlz = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    qnsu__yaxsa = op(bodo.utils.conversion.
                        unbox_if_timestamp(xndcl__nlz), arr)
                    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xndcl__nlz = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                qnsu__yaxsa = op(xndcl__nlz, arr)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        axaac__chort = create_binary_op_overload(op)
        overload(op)(axaac__chort)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    lbz__zagep = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, lbz__zagep)
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, yuqmk__tlty
                ) or bodo.libs.array_kernels.isna(arg2, yuqmk__tlty):
                bodo.libs.array_kernels.setna(S, yuqmk__tlty)
                continue
            S[yuqmk__tlty
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                yuqmk__tlty]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[yuqmk__tlty]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                ruy__rojh = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, ruy__rojh)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        axaac__chort = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(axaac__chort)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                qnsu__yaxsa = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        axaac__chort = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(axaac__chort)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    qnsu__yaxsa = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
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
                    ruy__rojh = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    qnsu__yaxsa = ufunc(arr, ruy__rojh)
                    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    ruy__rojh = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    qnsu__yaxsa = ufunc(arr, ruy__rojh)
                    return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        axaac__chort = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(axaac__chort)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        fis__txd = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        vmoi__egn = np.arange(n),
        bodo.libs.timsort.sort(fis__txd, 0, n, vmoi__egn)
        return vmoi__egn[0]
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
        gfe__ozb = get_overload_const_str(downcast)
        if gfe__ozb in ('integer', 'signed'):
            out_dtype = types.int64
        elif gfe__ozb == 'unsigned':
            out_dtype = types.uint64
        else:
            assert gfe__ozb == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            rnpvt__hqs = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            qnsu__yaxsa = pd.to_numeric(rnpvt__hqs, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            gwx__valn = np.empty(n, np.float64)
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, yuqmk__tlty):
                    bodo.libs.array_kernels.setna(gwx__valn, yuqmk__tlty)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(gwx__valn,
                        yuqmk__tlty, arg_a, yuqmk__tlty)
            return gwx__valn
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            gwx__valn = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, yuqmk__tlty):
                    bodo.libs.array_kernels.setna(gwx__valn, yuqmk__tlty)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(gwx__valn,
                        yuqmk__tlty, arg_a, yuqmk__tlty)
            return gwx__valn
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        ylhcr__cbwo = if_series_to_array_type(args[0])
        if isinstance(ylhcr__cbwo, types.Array) and isinstance(ylhcr__cbwo.
            dtype, types.Integer):
            ylhcr__cbwo = types.Array(types.float64, 1, 'C')
        return ylhcr__cbwo(*args)


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
    nnkbb__hzuku = bodo.utils.utils.is_array_typ(x, True)
    zbz__hlxpb = bodo.utils.utils.is_array_typ(y, True)
    rqe__jpv = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        rqe__jpv += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if nnkbb__hzuku and not bodo.utils.utils.is_array_typ(x, False):
        rqe__jpv += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if zbz__hlxpb and not bodo.utils.utils.is_array_typ(y, False):
        rqe__jpv += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    rqe__jpv += '  n = len(condition)\n'
    ewx__axakp = x.dtype if nnkbb__hzuku else types.unliteral(x)
    sutn__tmlu = y.dtype if zbz__hlxpb else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        ewx__axakp = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        sutn__tmlu = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    fkb__ihn = get_data(x)
    yqhbw__mehs = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(vmoi__egn) for
        vmoi__egn in [fkb__ihn, yqhbw__mehs])
    if yqhbw__mehs == types.none:
        if isinstance(ewx__axakp, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif fkb__ihn == yqhbw__mehs and not is_nullable:
        out_dtype = dtype_to_array_type(ewx__axakp)
    elif ewx__axakp == string_type or sutn__tmlu == string_type:
        out_dtype = bodo.string_array_type
    elif fkb__ihn == bytes_type or (nnkbb__hzuku and ewx__axakp == bytes_type
        ) and (yqhbw__mehs == bytes_type or zbz__hlxpb and sutn__tmlu ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(ewx__axakp, bodo.PDCategoricalDtype):
        out_dtype = None
    elif ewx__axakp in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(ewx__axakp, 1, 'C')
    elif sutn__tmlu in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(sutn__tmlu, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(ewx__axakp), numba.np.numpy_support.
            as_dtype(sutn__tmlu)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(ewx__axakp, bodo.PDCategoricalDtype):
        ann__vxa = 'x'
    else:
        ann__vxa = 'out_dtype'
    rqe__jpv += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {ann__vxa}, (-1,))\n')
    if isinstance(ewx__axakp, bodo.PDCategoricalDtype):
        rqe__jpv += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        rqe__jpv += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    rqe__jpv += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    rqe__jpv += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if nnkbb__hzuku:
        rqe__jpv += '      if bodo.libs.array_kernels.isna(x, j):\n'
        rqe__jpv += '        setna(out_arr, j)\n'
        rqe__jpv += '        continue\n'
    if isinstance(ewx__axakp, bodo.PDCategoricalDtype):
        rqe__jpv += '      out_codes[j] = x_codes[j]\n'
    else:
        rqe__jpv += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if nnkbb__hzuku else 'x'))
    rqe__jpv += '    else:\n'
    if zbz__hlxpb:
        rqe__jpv += '      if bodo.libs.array_kernels.isna(y, j):\n'
        rqe__jpv += '        setna(out_arr, j)\n'
        rqe__jpv += '        continue\n'
    if yqhbw__mehs == types.none:
        if isinstance(ewx__axakp, bodo.PDCategoricalDtype):
            rqe__jpv += '      out_codes[j] = -1\n'
        else:
            rqe__jpv += '      setna(out_arr, j)\n'
    else:
        rqe__jpv += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if zbz__hlxpb else 'y'))
    rqe__jpv += '  return out_arr\n'
    qycqg__solyt = {}
    exec(rqe__jpv, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, qycqg__solyt)
    yayol__suudx = qycqg__solyt['_impl']
    return yayol__suudx


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
        xdrf__rbkhj = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(xdrf__rbkhj, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(xdrf__rbkhj):
            kamvk__esr = xdrf__rbkhj.data.dtype
        else:
            kamvk__esr = xdrf__rbkhj.dtype
        if isinstance(kamvk__esr, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        nkua__bmpog = xdrf__rbkhj
    else:
        naoz__uer = []
        for xdrf__rbkhj in choicelist:
            if not bodo.utils.utils.is_array_typ(xdrf__rbkhj, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(xdrf__rbkhj):
                kamvk__esr = xdrf__rbkhj.data.dtype
            else:
                kamvk__esr = xdrf__rbkhj.dtype
            if isinstance(kamvk__esr, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            naoz__uer.append(kamvk__esr)
        if not is_common_scalar_dtype(naoz__uer):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        nkua__bmpog = choicelist[0]
    if is_series_type(nkua__bmpog):
        nkua__bmpog = nkua__bmpog.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, nkua__bmpog.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(nkua__bmpog, types.Array) or isinstance(nkua__bmpog,
        BooleanArrayType) or isinstance(nkua__bmpog, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(nkua__bmpog, False) and nkua__bmpog.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {nkua__bmpog} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    vke__lqa = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        hpdov__gous = choicelist.dtype
    else:
        vkk__hxap = False
        naoz__uer = []
        for xdrf__rbkhj in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                xdrf__rbkhj, 'numpy.select()')
            if is_nullable_type(xdrf__rbkhj):
                vkk__hxap = True
            if is_series_type(xdrf__rbkhj):
                kamvk__esr = xdrf__rbkhj.data.dtype
            else:
                kamvk__esr = xdrf__rbkhj.dtype
            if isinstance(kamvk__esr, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            naoz__uer.append(kamvk__esr)
        bzs__upru, wntdw__uoli = get_common_scalar_dtype(naoz__uer)
        if not wntdw__uoli:
            raise BodoError('Internal error in overload_np_select')
        ohjgx__det = dtype_to_array_type(bzs__upru)
        if vkk__hxap:
            ohjgx__det = to_nullable_type(ohjgx__det)
        hpdov__gous = ohjgx__det
    if isinstance(hpdov__gous, SeriesType):
        hpdov__gous = hpdov__gous.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        kriev__vlz = True
    else:
        kriev__vlz = False
    cun__kej = False
    xjfh__udd = False
    if kriev__vlz:
        if isinstance(hpdov__gous.dtype, types.Number):
            pass
        elif hpdov__gous.dtype == types.bool_:
            xjfh__udd = True
        else:
            cun__kej = True
            hpdov__gous = to_nullable_type(hpdov__gous)
    elif default == types.none or is_overload_constant_nan(default):
        cun__kej = True
        hpdov__gous = to_nullable_type(hpdov__gous)
    rqe__jpv = 'def np_select_impl(condlist, choicelist, default=0):\n'
    rqe__jpv += '  if len(condlist) != len(choicelist):\n'
    rqe__jpv += (
        "    raise ValueError('list of cases must be same length as list of conditions')\n"
        )
    rqe__jpv += '  output_len = len(choicelist[0])\n'
    rqe__jpv += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    rqe__jpv += '  for i in range(output_len):\n'
    if cun__kej:
        rqe__jpv += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif xjfh__udd:
        rqe__jpv += '    out[i] = False\n'
    else:
        rqe__jpv += '    out[i] = default\n'
    if vke__lqa:
        rqe__jpv += '  for i in range(len(condlist) - 1, -1, -1):\n'
        rqe__jpv += '    cond = condlist[i]\n'
        rqe__jpv += '    choice = choicelist[i]\n'
        rqe__jpv += '    out = np.where(cond, choice, out)\n'
    else:
        for yuqmk__tlty in range(len(choicelist) - 1, -1, -1):
            rqe__jpv += f'  cond = condlist[{yuqmk__tlty}]\n'
            rqe__jpv += f'  choice = choicelist[{yuqmk__tlty}]\n'
            rqe__jpv += f'  out = np.where(cond, choice, out)\n'
    rqe__jpv += '  return out'
    qycqg__solyt = dict()
    exec(rqe__jpv, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': hpdov__gous}, qycqg__solyt)
    impl = qycqg__solyt['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qnsu__yaxsa = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    gku__vydb = dict(subset=subset, keep=keep, inplace=inplace)
    cgy__lkwyl = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', gku__vydb, cgy__lkwyl,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        kudss__kybs = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (kudss__kybs,), hmnj__tcdp = bodo.libs.array_kernels.drop_duplicates((
            kudss__kybs,), index, 1)
        index = bodo.utils.conversion.index_from_array(hmnj__tcdp)
        return bodo.hiframes.pd_series_ext.init_series(kudss__kybs, index, name
            )
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    ajct__jdzmv = element_type(S.data)
    if not is_common_scalar_dtype([ajct__jdzmv, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([ajct__jdzmv, right]):
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
        qnsu__yaxsa = np.empty(n, np.bool_)
        for yuqmk__tlty in numba.parfors.parfor.internal_prange(n):
            qrai__ovj = bodo.utils.conversion.box_if_dt64(arr[yuqmk__tlty])
            if inclusive == 'both':
                qnsu__yaxsa[yuqmk__tlty
                    ] = qrai__ovj <= right and qrai__ovj >= left
            else:
                qnsu__yaxsa[yuqmk__tlty
                    ] = qrai__ovj < right and qrai__ovj > left
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    gku__vydb = dict(axis=axis)
    cgy__lkwyl = dict(axis=None)
    check_unsupported_args('Series.repeat', gku__vydb, cgy__lkwyl,
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
            hmnj__tcdp = bodo.utils.conversion.index_to_array(index)
            qnsu__yaxsa = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            lsroh__ocjk = bodo.libs.array_kernels.repeat_kernel(hmnj__tcdp,
                repeats)
            hhd__yyj = bodo.utils.conversion.index_from_array(lsroh__ocjk)
            return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
                hhd__yyj, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hmnj__tcdp = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        qnsu__yaxsa = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        lsroh__ocjk = bodo.libs.array_kernels.repeat_kernel(hmnj__tcdp, repeats
            )
        hhd__yyj = bodo.utils.conversion.index_from_array(lsroh__ocjk)
        return bodo.hiframes.pd_series_ext.init_series(qnsu__yaxsa,
            hhd__yyj, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        vmoi__egn = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(vmoi__egn)
        mkxig__ktr = {}
        for yuqmk__tlty in range(n):
            qrai__ovj = bodo.utils.conversion.box_if_dt64(vmoi__egn[
                yuqmk__tlty])
            mkxig__ktr[index[yuqmk__tlty]] = qrai__ovj
        return mkxig__ktr
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    yme__cqnc = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            cesd__bhk = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(yme__cqnc)
    elif is_literal_type(name):
        cesd__bhk = get_literal_value(name)
    else:
        raise_bodo_error(yme__cqnc)
    cesd__bhk = 0 if cesd__bhk is None else cesd__bhk

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (cesd__bhk,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
