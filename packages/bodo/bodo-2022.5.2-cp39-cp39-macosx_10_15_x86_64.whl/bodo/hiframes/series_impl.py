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
            amtc__ykupv = bodo.hiframes.pd_series_ext.get_series_data(s)
            bprno__tilm = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                amtc__ykupv)
            return bprno__tilm
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
            quq__zijn = list()
            for lwzz__gymn in range(len(S)):
                quq__zijn.append(S.iat[lwzz__gymn])
            return quq__zijn
        return impl_float

    def impl(S):
        quq__zijn = list()
        for lwzz__gymn in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, lwzz__gymn):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            quq__zijn.append(S.iat[lwzz__gymn])
        return quq__zijn
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    jrnkc__arf = dict(dtype=dtype, copy=copy, na_value=na_value)
    cpgh__fjpk = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    jrnkc__arf = dict(name=name, inplace=inplace)
    cpgh__fjpk = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', jrnkc__arf, cpgh__fjpk,
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
        gdqiq__qzpk = ', '.join(['index_arrs[{}]'.format(lwzz__gymn) for
            lwzz__gymn in range(S.index.nlevels)])
    else:
        gdqiq__qzpk = '    bodo.utils.conversion.index_to_array(index)\n'
    ziy__elf = 'index' if 'index' != series_name else 'level_0'
    cth__vke = get_index_names(S.index, 'Series.reset_index()', ziy__elf)
    columns = [name for name in cth__vke]
    columns.append(series_name)
    ugdxt__zbfzo = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    ugdxt__zbfzo += (
        '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ugdxt__zbfzo += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        ugdxt__zbfzo += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    ugdxt__zbfzo += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    ugdxt__zbfzo += '    col_var = {}\n'.format(gen_const_tup(columns))
    ugdxt__zbfzo += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({gdqiq__qzpk}, arr), df_index, col_var)
"""
    sgoz__vnn = {}
    exec(ugdxt__zbfzo, {'bodo': bodo}, sgoz__vnn)
    ozh__cfc = sgoz__vnn['_impl']
    return ozh__cfc


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        szp__ofzwz = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
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
        szp__ofzwz = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[lwzz__gymn]):
                bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
            else:
                szp__ofzwz[lwzz__gymn] = np.round(arr[lwzz__gymn], decimals)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    cpgh__fjpk = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        oekrr__yaavs = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = 0
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn):
                nif__rho = int(A[lwzz__gymn])
            oekrr__yaavs += nif__rho
        return oekrr__yaavs != 0
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
        qyx__sdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rhltl__ojqdb = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        oekrr__yaavs = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(qyx__sdb)):
            nif__rho = 0
            mzyr__ull = bodo.libs.array_kernels.isna(qyx__sdb, lwzz__gymn)
            nvqvb__gpnje = bodo.libs.array_kernels.isna(rhltl__ojqdb,
                lwzz__gymn)
            if (mzyr__ull and not nvqvb__gpnje or not mzyr__ull and
                nvqvb__gpnje):
                nif__rho = 1
            elif not mzyr__ull:
                if qyx__sdb[lwzz__gymn] != rhltl__ojqdb[lwzz__gymn]:
                    nif__rho = 1
            oekrr__yaavs += nif__rho
        return oekrr__yaavs == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    jrnkc__arf = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    cpgh__fjpk = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        oekrr__yaavs = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = 0
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn):
                nif__rho = int(not A[lwzz__gymn])
            oekrr__yaavs += nif__rho
        return oekrr__yaavs == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    jrnkc__arf = dict(level=level)
    cpgh__fjpk = dict(level=None)
    check_unsupported_args('Series.mad', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    jwffr__bsr = types.float64
    elos__egrpf = types.float64
    if S.dtype == types.float32:
        jwffr__bsr = types.float32
        elos__egrpf = types.float32
    odk__xcth = jwffr__bsr(0)
    ixtmh__dhyub = elos__egrpf(0)
    mze__ldgyo = elos__egrpf(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        vazbx__nqfj = odk__xcth
        oekrr__yaavs = ixtmh__dhyub
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = odk__xcth
            tyjok__eeima = ixtmh__dhyub
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn) or not skipna:
                nif__rho = A[lwzz__gymn]
                tyjok__eeima = mze__ldgyo
            vazbx__nqfj += nif__rho
            oekrr__yaavs += tyjok__eeima
        khpi__abqi = bodo.hiframes.series_kernels._mean_handle_nan(vazbx__nqfj,
            oekrr__yaavs)
        pbvpj__rkis = odk__xcth
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = odk__xcth
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn) or not skipna:
                nif__rho = abs(A[lwzz__gymn] - khpi__abqi)
            pbvpj__rkis += nif__rho
        btej__etc = bodo.hiframes.series_kernels._mean_handle_nan(pbvpj__rkis,
            oekrr__yaavs)
        return btej__etc
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    jrnkc__arf = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', jrnkc__arf, cpgh__fjpk,
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
        uuh__rqz = 0
        vya__tmpa = 0
        oekrr__yaavs = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = 0
            tyjok__eeima = 0
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn) or not skipna:
                nif__rho = A[lwzz__gymn]
                tyjok__eeima = 1
            uuh__rqz += nif__rho
            vya__tmpa += nif__rho * nif__rho
            oekrr__yaavs += tyjok__eeima
        cfit__jvo = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            uuh__rqz, vya__tmpa, oekrr__yaavs, ddof)
        ist__npmcv = bodo.hiframes.series_kernels._sem_handle_nan(cfit__jvo,
            oekrr__yaavs)
        return ist__npmcv
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', jrnkc__arf, cpgh__fjpk,
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
        uuh__rqz = 0.0
        vya__tmpa = 0.0
        cub__tjco = 0.0
        hnbr__odc = 0.0
        oekrr__yaavs = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = 0.0
            tyjok__eeima = 0
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn) or not skipna:
                nif__rho = np.float64(A[lwzz__gymn])
                tyjok__eeima = 1
            uuh__rqz += nif__rho
            vya__tmpa += nif__rho ** 2
            cub__tjco += nif__rho ** 3
            hnbr__odc += nif__rho ** 4
            oekrr__yaavs += tyjok__eeima
        cfit__jvo = bodo.hiframes.series_kernels.compute_kurt(uuh__rqz,
            vya__tmpa, cub__tjco, hnbr__odc, oekrr__yaavs)
        return cfit__jvo
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', jrnkc__arf, cpgh__fjpk,
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
        uuh__rqz = 0.0
        vya__tmpa = 0.0
        cub__tjco = 0.0
        oekrr__yaavs = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(A)):
            nif__rho = 0.0
            tyjok__eeima = 0
            if not bodo.libs.array_kernels.isna(A, lwzz__gymn) or not skipna:
                nif__rho = np.float64(A[lwzz__gymn])
                tyjok__eeima = 1
            uuh__rqz += nif__rho
            vya__tmpa += nif__rho ** 2
            cub__tjco += nif__rho ** 3
            oekrr__yaavs += tyjok__eeima
        cfit__jvo = bodo.hiframes.series_kernels.compute_skew(uuh__rqz,
            vya__tmpa, cub__tjco, oekrr__yaavs)
        return cfit__jvo
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', jrnkc__arf, cpgh__fjpk,
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
        qyx__sdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rhltl__ojqdb = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        sudl__wkr = 0
        for lwzz__gymn in numba.parfors.parfor.internal_prange(len(qyx__sdb)):
            ncs__lisno = qyx__sdb[lwzz__gymn]
            ila__qawia = rhltl__ojqdb[lwzz__gymn]
            sudl__wkr += ncs__lisno * ila__qawia
        return sudl__wkr
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    jrnkc__arf = dict(skipna=skipna)
    cpgh__fjpk = dict(skipna=True)
    check_unsupported_args('Series.cumsum', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(skipna=skipna)
    cpgh__fjpk = dict(skipna=True)
    check_unsupported_args('Series.cumprod', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(skipna=skipna)
    cpgh__fjpk = dict(skipna=True)
    check_unsupported_args('Series.cummin', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(skipna=skipna)
    cpgh__fjpk = dict(skipna=True)
    check_unsupported_args('Series.cummax', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    cpgh__fjpk = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        fervp__crw = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, fervp__crw, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    jrnkc__arf = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    cpgh__fjpk = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(level=level)
    cpgh__fjpk = dict(level=None)
    check_unsupported_args('Series.count', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    jrnkc__arf = dict(method=method, min_periods=min_periods)
    cpgh__fjpk = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        nhnf__uvg = S.sum()
        yky__bqzb = other.sum()
        a = n * (S * other).sum() - nhnf__uvg * yky__bqzb
        yuxs__ykuy = n * (S ** 2).sum() - nhnf__uvg ** 2
        wfgjz__nclyn = n * (other ** 2).sum() - yky__bqzb ** 2
        return a / np.sqrt(yuxs__ykuy * wfgjz__nclyn)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    jrnkc__arf = dict(min_periods=min_periods)
    cpgh__fjpk = dict(min_periods=None)
    check_unsupported_args('Series.cov', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        nhnf__uvg = S.mean()
        yky__bqzb = other.mean()
        kbemg__rbwqt = ((S - nhnf__uvg) * (other - yky__bqzb)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(kbemg__rbwqt, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            gvt__kgdi = np.sign(sum_val)
            return np.inf * gvt__kgdi
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    jrnkc__arf = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(axis=axis, skipna=skipna)
    cpgh__fjpk = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(axis=axis, skipna=skipna)
    cpgh__fjpk = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', jrnkc__arf, cpgh__fjpk,
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
    jrnkc__arf = dict(level=level, numeric_only=numeric_only)
    cpgh__fjpk = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', jrnkc__arf, cpgh__fjpk,
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
        cvb__jro = arr[:n]
        kzrz__wxx = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(cvb__jro, kzrz__wxx,
            name)
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
        paq__sgfju = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvb__jro = arr[paq__sgfju:]
        kzrz__wxx = index[paq__sgfju:]
        return bodo.hiframes.pd_series_ext.init_series(cvb__jro, kzrz__wxx,
            name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    ghuc__prxjy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ghuc__prxjy:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            hrqbd__lnml = index[0]
            nnits__laa = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                hrqbd__lnml, False))
        else:
            nnits__laa = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvb__jro = arr[:nnits__laa]
        kzrz__wxx = index[:nnits__laa]
        return bodo.hiframes.pd_series_ext.init_series(cvb__jro, kzrz__wxx,
            name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    ghuc__prxjy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ghuc__prxjy:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            qnd__cgfb = index[-1]
            nnits__laa = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, qnd__cgfb,
                True))
        else:
            nnits__laa = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvb__jro = arr[len(arr) - nnits__laa:]
        kzrz__wxx = index[len(arr) - nnits__laa:]
        return bodo.hiframes.pd_series_ext.init_series(cvb__jro, kzrz__wxx,
            name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        taxbg__dqm = bodo.utils.conversion.index_to_array(index)
        itqe__iifw, lqsa__cabb = (bodo.libs.array_kernels.
            first_last_valid_index(arr, taxbg__dqm))
        return lqsa__cabb if itqe__iifw else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        taxbg__dqm = bodo.utils.conversion.index_to_array(index)
        itqe__iifw, lqsa__cabb = (bodo.libs.array_kernels.
            first_last_valid_index(arr, taxbg__dqm, False))
        return lqsa__cabb if itqe__iifw else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    jrnkc__arf = dict(keep=keep)
    cpgh__fjpk = dict(keep='first')
    check_unsupported_args('Series.nlargest', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        taxbg__dqm = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        szp__ofzwz, avkkb__ilmz = bodo.libs.array_kernels.nlargest(arr,
            taxbg__dqm, n, True, bodo.hiframes.series_kernels.gt_f)
        kepaf__eutjv = bodo.utils.conversion.convert_to_index(avkkb__ilmz)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
            kepaf__eutjv, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    jrnkc__arf = dict(keep=keep)
    cpgh__fjpk = dict(keep='first')
    check_unsupported_args('Series.nsmallest', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        taxbg__dqm = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        szp__ofzwz, avkkb__ilmz = bodo.libs.array_kernels.nlargest(arr,
            taxbg__dqm, n, False, bodo.hiframes.series_kernels.lt_f)
        kepaf__eutjv = bodo.utils.conversion.convert_to_index(avkkb__ilmz)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
            kepaf__eutjv, name)
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
    jrnkc__arf = dict(errors=errors)
    cpgh__fjpk = dict(errors='raise')
    check_unsupported_args('Series.astype', jrnkc__arf, cpgh__fjpk,
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
        szp__ofzwz = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    jrnkc__arf = dict(axis=axis, is_copy=is_copy)
    cpgh__fjpk = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        jnbbq__gbwee = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[jnbbq__gbwee],
            index[jnbbq__gbwee], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    jrnkc__arf = dict(axis=axis, kind=kind, order=order)
    cpgh__fjpk = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wgxw__acrg = S.notna().values
        if not wgxw__acrg.all():
            szp__ofzwz = np.full(n, -1, np.int64)
            szp__ofzwz[wgxw__acrg] = argsort(arr[wgxw__acrg])
        else:
            szp__ofzwz = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    jrnkc__arf = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    cpgh__fjpk = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', jrnkc__arf, cpgh__fjpk,
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
        gtkvd__lmhr = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        qfbz__nkv = gtkvd__lmhr.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        szp__ofzwz = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            qfbz__nkv, 0)
        kepaf__eutjv = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            qfbz__nkv)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
            kepaf__eutjv, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    jrnkc__arf = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    cpgh__fjpk = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', jrnkc__arf, cpgh__fjpk,
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
        gtkvd__lmhr = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        qfbz__nkv = gtkvd__lmhr.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        szp__ofzwz = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            qfbz__nkv, 0)
        kepaf__eutjv = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            qfbz__nkv)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
            kepaf__eutjv, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    slnx__yqp = is_overload_true(is_nullable)
    ugdxt__zbfzo = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    ugdxt__zbfzo += '  numba.parfors.parfor.init_prange()\n'
    ugdxt__zbfzo += '  n = len(arr)\n'
    if slnx__yqp:
        ugdxt__zbfzo += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        ugdxt__zbfzo += '  out_arr = np.empty(n, np.int64)\n'
    ugdxt__zbfzo += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    ugdxt__zbfzo += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if slnx__yqp:
        ugdxt__zbfzo += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        ugdxt__zbfzo += '      out_arr[i] = -1\n'
    ugdxt__zbfzo += '      continue\n'
    ugdxt__zbfzo += '    val = arr[i]\n'
    ugdxt__zbfzo += '    if include_lowest and val == bins[0]:\n'
    ugdxt__zbfzo += '      ind = 1\n'
    ugdxt__zbfzo += '    else:\n'
    ugdxt__zbfzo += '      ind = np.searchsorted(bins, val)\n'
    ugdxt__zbfzo += '    if ind == 0 or ind == len(bins):\n'
    if slnx__yqp:
        ugdxt__zbfzo += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        ugdxt__zbfzo += '      out_arr[i] = -1\n'
    ugdxt__zbfzo += '    else:\n'
    ugdxt__zbfzo += '      out_arr[i] = ind - 1\n'
    ugdxt__zbfzo += '  return out_arr\n'
    sgoz__vnn = {}
    exec(ugdxt__zbfzo, {'bodo': bodo, 'np': np, 'numba': numba}, sgoz__vnn)
    impl = sgoz__vnn['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        yvxl__wfmm, wxry__kad = np.divmod(x, 1)
        if yvxl__wfmm == 0:
            awiso__jgy = -int(np.floor(np.log10(abs(wxry__kad)))
                ) - 1 + precision
        else:
            awiso__jgy = precision
        return np.around(x, awiso__jgy)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        atiic__mdoy = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(atiic__mdoy)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        rni__iktra = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            cxsxh__loe = bins.copy()
            if right and include_lowest:
                cxsxh__loe[0] = cxsxh__loe[0] - rni__iktra
            aepvq__pcp = bodo.libs.interval_arr_ext.init_interval_array(
                cxsxh__loe[:-1], cxsxh__loe[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(aepvq__pcp,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        cxsxh__loe = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            cxsxh__loe[0] = cxsxh__loe[0] - 10.0 ** -precision
        aepvq__pcp = bodo.libs.interval_arr_ext.init_interval_array(cxsxh__loe
            [:-1], cxsxh__loe[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(aepvq__pcp, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        lydqp__bkk = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        don__ssai = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        szp__ofzwz = np.zeros(nbins, np.int64)
        for lwzz__gymn in range(len(lydqp__bkk)):
            szp__ofzwz[don__ssai[lwzz__gymn]] = lydqp__bkk[lwzz__gymn]
        return szp__ofzwz
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
            cvfkr__owl = (max_val - min_val) * 0.001
            if right:
                bins[0] -= cvfkr__owl
            else:
                bins[-1] += cvfkr__owl
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    jrnkc__arf = dict(dropna=dropna)
    cpgh__fjpk = dict(dropna=True)
    check_unsupported_args('Series.value_counts', jrnkc__arf, cpgh__fjpk,
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
    wxuj__tpjh = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    ugdxt__zbfzo = 'def impl(\n'
    ugdxt__zbfzo += '    S,\n'
    ugdxt__zbfzo += '    normalize=False,\n'
    ugdxt__zbfzo += '    sort=True,\n'
    ugdxt__zbfzo += '    ascending=False,\n'
    ugdxt__zbfzo += '    bins=None,\n'
    ugdxt__zbfzo += '    dropna=True,\n'
    ugdxt__zbfzo += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    ugdxt__zbfzo += '):\n'
    ugdxt__zbfzo += (
        '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ugdxt__zbfzo += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    ugdxt__zbfzo += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if wxuj__tpjh:
        ugdxt__zbfzo += '    right = True\n'
        ugdxt__zbfzo += _gen_bins_handling(bins, S.dtype)
        ugdxt__zbfzo += '    arr = get_bin_inds(bins, arr)\n'
    ugdxt__zbfzo += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    ugdxt__zbfzo += "        (arr,), index, ('$_bodo_col2_',)\n"
    ugdxt__zbfzo += '    )\n'
    ugdxt__zbfzo += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if wxuj__tpjh:
        ugdxt__zbfzo += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        ugdxt__zbfzo += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        ugdxt__zbfzo += '    index = get_bin_labels(bins)\n'
    else:
        ugdxt__zbfzo += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        ugdxt__zbfzo += (
            '    ind_arr = bodo.utils.conversion.coerce_to_array(\n')
        ugdxt__zbfzo += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        ugdxt__zbfzo += '    )\n'
        ugdxt__zbfzo += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    ugdxt__zbfzo += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        ugdxt__zbfzo += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        maag__ssx = 'len(S)' if wxuj__tpjh else 'count_arr.sum()'
        ugdxt__zbfzo += f'    res = res / float({maag__ssx})\n'
    ugdxt__zbfzo += '    return res\n'
    sgoz__vnn = {}
    exec(ugdxt__zbfzo, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, sgoz__vnn)
    impl = sgoz__vnn['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    ugdxt__zbfzo = ''
    if isinstance(bins, types.Integer):
        ugdxt__zbfzo += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        ugdxt__zbfzo += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            ugdxt__zbfzo += '    min_val = min_val.value\n'
            ugdxt__zbfzo += '    max_val = max_val.value\n'
        ugdxt__zbfzo += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            ugdxt__zbfzo += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        ugdxt__zbfzo += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return ugdxt__zbfzo


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    jrnkc__arf = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    cpgh__fjpk = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    ugdxt__zbfzo = 'def impl(\n'
    ugdxt__zbfzo += '    x,\n'
    ugdxt__zbfzo += '    bins,\n'
    ugdxt__zbfzo += '    right=True,\n'
    ugdxt__zbfzo += '    labels=None,\n'
    ugdxt__zbfzo += '    retbins=False,\n'
    ugdxt__zbfzo += '    precision=3,\n'
    ugdxt__zbfzo += '    include_lowest=False,\n'
    ugdxt__zbfzo += "    duplicates='raise',\n"
    ugdxt__zbfzo += '    ordered=True\n'
    ugdxt__zbfzo += '):\n'
    if isinstance(x, SeriesType):
        ugdxt__zbfzo += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        ugdxt__zbfzo += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        ugdxt__zbfzo += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        ugdxt__zbfzo += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    ugdxt__zbfzo += _gen_bins_handling(bins, x.dtype)
    ugdxt__zbfzo += (
        '    arr = get_bin_inds(bins, arr, False, include_lowest)\n')
    ugdxt__zbfzo += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    ugdxt__zbfzo += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    ugdxt__zbfzo += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        ugdxt__zbfzo += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        ugdxt__zbfzo += '    return res\n'
    else:
        ugdxt__zbfzo += '    return out_arr\n'
    sgoz__vnn = {}
    exec(ugdxt__zbfzo, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, sgoz__vnn)
    impl = sgoz__vnn['impl']
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
    jrnkc__arf = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    cpgh__fjpk = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        hor__hojlz = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, hor__hojlz)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    jrnkc__arf = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    cpgh__fjpk = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', jrnkc__arf, cpgh__fjpk,
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
            ykfo__okgr = bodo.utils.conversion.coerce_to_array(index)
            gtkvd__lmhr = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                ykfo__okgr, arr), index, (' ', ''))
            return gtkvd__lmhr.groupby(' ')['']
        return impl_index
    ygn__ywjpo = by
    if isinstance(by, SeriesType):
        ygn__ywjpo = by.data
    if isinstance(ygn__ywjpo, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        ykfo__okgr = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        gtkvd__lmhr = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            ykfo__okgr, arr), index, (' ', ''))
        return gtkvd__lmhr.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    jrnkc__arf = dict(verify_integrity=verify_integrity)
    cpgh__fjpk = dict(verify_integrity=False)
    check_unsupported_args('Series.append', jrnkc__arf, cpgh__fjpk,
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
            mqmb__ohbre = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            szp__ofzwz = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(szp__ofzwz, A, mqmb__ohbre, False)
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        szp__ofzwz = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    jrnkc__arf = dict(interpolation=interpolation)
    cpgh__fjpk = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            szp__ofzwz = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
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
        fqw__lnj = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(fqw__lnj, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    jrnkc__arf = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    cpgh__fjpk = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', jrnkc__arf, cpgh__fjpk,
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
        zgn__yjsk = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        zgn__yjsk = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    ugdxt__zbfzo = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {zgn__yjsk}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    rwtmn__zuz = dict()
    exec(ugdxt__zbfzo, {'bodo': bodo, 'numba': numba}, rwtmn__zuz)
    duuq__esk = rwtmn__zuz['impl']
    return duuq__esk


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        zgn__yjsk = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        zgn__yjsk = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    ugdxt__zbfzo = 'def impl(S,\n'
    ugdxt__zbfzo += '     value=None,\n'
    ugdxt__zbfzo += '    method=None,\n'
    ugdxt__zbfzo += '    axis=None,\n'
    ugdxt__zbfzo += '    inplace=False,\n'
    ugdxt__zbfzo += '    limit=None,\n'
    ugdxt__zbfzo += '   downcast=None,\n'
    ugdxt__zbfzo += '):\n'
    ugdxt__zbfzo += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ugdxt__zbfzo += '    n = len(in_arr)\n'
    ugdxt__zbfzo += f'    out_arr = {zgn__yjsk}(n, -1)\n'
    ugdxt__zbfzo += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    ugdxt__zbfzo += '        s = in_arr[j]\n'
    ugdxt__zbfzo += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    ugdxt__zbfzo += '            s = value\n'
    ugdxt__zbfzo += '        out_arr[j] = s\n'
    ugdxt__zbfzo += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    rwtmn__zuz = dict()
    exec(ugdxt__zbfzo, {'bodo': bodo, 'numba': numba}, rwtmn__zuz)
    duuq__esk = rwtmn__zuz['impl']
    return duuq__esk


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
    ondk__jqsir = bodo.hiframes.pd_series_ext.get_series_data(value)
    for lwzz__gymn in numba.parfors.parfor.internal_prange(len(aicr__kqv)):
        s = aicr__kqv[lwzz__gymn]
        if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn
            ) and not bodo.libs.array_kernels.isna(ondk__jqsir, lwzz__gymn):
            s = ondk__jqsir[lwzz__gymn]
        aicr__kqv[lwzz__gymn] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
    for lwzz__gymn in numba.parfors.parfor.internal_prange(len(aicr__kqv)):
        s = aicr__kqv[lwzz__gymn]
        if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn):
            s = value
        aicr__kqv[lwzz__gymn] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    ondk__jqsir = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(aicr__kqv)
    szp__ofzwz = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for qugi__lta in numba.parfors.parfor.internal_prange(n):
        s = aicr__kqv[qugi__lta]
        if bodo.libs.array_kernels.isna(aicr__kqv, qugi__lta
            ) and not bodo.libs.array_kernels.isna(ondk__jqsir, qugi__lta):
            s = ondk__jqsir[qugi__lta]
        szp__ofzwz[qugi__lta] = s
        if bodo.libs.array_kernels.isna(aicr__kqv, qugi__lta
            ) and bodo.libs.array_kernels.isna(ondk__jqsir, qugi__lta):
            bodo.libs.array_kernels.setna(szp__ofzwz, qugi__lta)
    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    ondk__jqsir = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(aicr__kqv)
    szp__ofzwz = bodo.utils.utils.alloc_type(n, aicr__kqv.dtype, (-1,))
    for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
        s = aicr__kqv[lwzz__gymn]
        if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn
            ) and not bodo.libs.array_kernels.isna(ondk__jqsir, lwzz__gymn):
            s = ondk__jqsir[lwzz__gymn]
        szp__ofzwz[lwzz__gymn] = s
    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    jrnkc__arf = dict(limit=limit, downcast=downcast)
    cpgh__fjpk = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')
    tbhr__ysnl = not is_overload_none(value)
    zex__inrdq = not is_overload_none(method)
    if tbhr__ysnl and zex__inrdq:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not tbhr__ysnl and not zex__inrdq:
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
    if zex__inrdq:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        znxyd__fmkz = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(znxyd__fmkz)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(znxyd__fmkz)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    uwyd__gxcqr = element_type(S.data)
    tuzu__lptth = None
    if tbhr__ysnl:
        tuzu__lptth = element_type(types.unliteral(value))
    if tuzu__lptth and not can_replace(uwyd__gxcqr, tuzu__lptth):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {tuzu__lptth} with series type {uwyd__gxcqr}'
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
        kebsi__yqr = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ondk__jqsir = bodo.hiframes.pd_series_ext.get_series_data(value
                    )
                n = len(aicr__kqv)
                szp__ofzwz = bodo.utils.utils.alloc_type(n, kebsi__yqr, (-1,))
                for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn
                        ) and bodo.libs.array_kernels.isna(ondk__jqsir,
                        lwzz__gymn):
                        bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                        continue
                    if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn):
                        szp__ofzwz[lwzz__gymn
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            ondk__jqsir[lwzz__gymn])
                        continue
                    szp__ofzwz[lwzz__gymn
                        ] = bodo.utils.conversion.unbox_if_timestamp(aicr__kqv
                        [lwzz__gymn])
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return fillna_series_impl
        if zex__inrdq:
            qfdu__wuqeu = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(uwyd__gxcqr, (types.Integer, types.Float)
                ) and uwyd__gxcqr not in qfdu__wuqeu:
                raise BodoError(
                    f"Series.fillna(): series of type {uwyd__gxcqr} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                szp__ofzwz = bodo.libs.array_kernels.ffill_bfill_arr(aicr__kqv,
                    method)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(aicr__kqv)
            szp__ofzwz = bodo.utils.utils.alloc_type(n, kebsi__yqr, (-1,))
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(aicr__kqv[
                    lwzz__gymn])
                if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn):
                    s = value
                szp__ofzwz[lwzz__gymn] = s
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        cbw__lro = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        jrnkc__arf = dict(limit=limit, downcast=downcast)
        cpgh__fjpk = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', jrnkc__arf,
            cpgh__fjpk, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        uwyd__gxcqr = element_type(S.data)
        qfdu__wuqeu = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(uwyd__gxcqr, (types.Integer, types.Float)
            ) and uwyd__gxcqr not in qfdu__wuqeu:
            raise BodoError(
                f'Series.{overload_name}(): series of type {uwyd__gxcqr} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            szp__ofzwz = bodo.libs.array_kernels.ffill_bfill_arr(aicr__kqv,
                cbw__lro)
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        did__lhrw = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(did__lhrw
            )


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        xxcvs__ysfzg = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(xxcvs__ysfzg)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        xxcvs__ysfzg = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(xxcvs__ysfzg)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        xxcvs__ysfzg = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(xxcvs__ysfzg)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    jrnkc__arf = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    jmmey__nkiox = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', jrnkc__arf, jmmey__nkiox,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    uwyd__gxcqr = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        plhs__jstlq = element_type(to_replace.key_type)
        tuzu__lptth = element_type(to_replace.value_type)
    else:
        plhs__jstlq = element_type(to_replace)
        tuzu__lptth = element_type(value)
    ujnw__ujkix = None
    if uwyd__gxcqr != types.unliteral(plhs__jstlq):
        if bodo.utils.typing.equality_always_false(uwyd__gxcqr, types.
            unliteral(plhs__jstlq)
            ) or not bodo.utils.typing.types_equality_exists(uwyd__gxcqr,
            plhs__jstlq):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(uwyd__gxcqr, (types.Float, types.Integer)
            ) or uwyd__gxcqr == np.bool_:
            ujnw__ujkix = uwyd__gxcqr
    if not can_replace(uwyd__gxcqr, types.unliteral(tuzu__lptth)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    zxt__tkam = to_str_arr_if_dict_array(S.data)
    if isinstance(zxt__tkam, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(aicr__kqv.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(aicr__kqv)
        szp__ofzwz = bodo.utils.utils.alloc_type(n, zxt__tkam, (-1,))
        hcjn__vyqft = build_replace_dict(to_replace, value, ujnw__ujkix)
        for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(aicr__kqv, lwzz__gymn):
                bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                continue
            s = aicr__kqv[lwzz__gymn]
            if s in hcjn__vyqft:
                s = hcjn__vyqft[s]
            szp__ofzwz[lwzz__gymn] = s
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    mtpk__vig = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    xeb__gaowt = is_iterable_type(to_replace)
    topw__qxv = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    olxze__wactp = is_iterable_type(value)
    if mtpk__vig and topw__qxv:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                hcjn__vyqft = {}
                hcjn__vyqft[key_dtype_conv(to_replace)] = value
                return hcjn__vyqft
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            hcjn__vyqft = {}
            hcjn__vyqft[to_replace] = value
            return hcjn__vyqft
        return impl
    if xeb__gaowt and topw__qxv:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                hcjn__vyqft = {}
                for jpmkb__lqrje in to_replace:
                    hcjn__vyqft[key_dtype_conv(jpmkb__lqrje)] = value
                return hcjn__vyqft
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            hcjn__vyqft = {}
            for jpmkb__lqrje in to_replace:
                hcjn__vyqft[jpmkb__lqrje] = value
            return hcjn__vyqft
        return impl
    if xeb__gaowt and olxze__wactp:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                hcjn__vyqft = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for lwzz__gymn in range(len(to_replace)):
                    hcjn__vyqft[key_dtype_conv(to_replace[lwzz__gymn])
                        ] = value[lwzz__gymn]
                return hcjn__vyqft
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            hcjn__vyqft = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for lwzz__gymn in range(len(to_replace)):
                hcjn__vyqft[to_replace[lwzz__gymn]] = value[lwzz__gymn]
            return hcjn__vyqft
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
            szp__ofzwz = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        szp__ofzwz = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    jrnkc__arf = dict(ignore_index=ignore_index)
    wauye__dzpk = dict(ignore_index=False)
    check_unsupported_args('Series.explode', jrnkc__arf, wauye__dzpk,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        taxbg__dqm = bodo.utils.conversion.index_to_array(index)
        szp__ofzwz, phno__nfiyy = bodo.libs.array_kernels.explode(arr,
            taxbg__dqm)
        kepaf__eutjv = bodo.utils.conversion.index_from_array(phno__nfiyy)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
            kepaf__eutjv, name)
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
            algb__qbcc = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                algb__qbcc[lwzz__gymn] = np.argmax(a[lwzz__gymn])
            return algb__qbcc
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            znd__ohoti = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                znd__ohoti[lwzz__gymn] = np.argmin(a[lwzz__gymn])
            return znd__ohoti
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
    jrnkc__arf = dict(axis=axis, inplace=inplace, how=how)
    hmzz__ceurf = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', jrnkc__arf, hmzz__ceurf,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            wgxw__acrg = S.notna().values
            taxbg__dqm = bodo.utils.conversion.extract_index_array(S)
            kepaf__eutjv = bodo.utils.conversion.convert_to_index(taxbg__dqm
                [wgxw__acrg])
            szp__ofzwz = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(aicr__kqv))
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                kepaf__eutjv, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            taxbg__dqm = bodo.utils.conversion.extract_index_array(S)
            wgxw__acrg = S.notna().values
            kepaf__eutjv = bodo.utils.conversion.convert_to_index(taxbg__dqm
                [wgxw__acrg])
            szp__ofzwz = aicr__kqv[wgxw__acrg]
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                kepaf__eutjv, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    jrnkc__arf = dict(freq=freq, axis=axis, fill_value=fill_value)
    cpgh__fjpk = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', jrnkc__arf, cpgh__fjpk,
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
        szp__ofzwz = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    jrnkc__arf = dict(fill_method=fill_method, limit=limit, freq=freq)
    cpgh__fjpk = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', jrnkc__arf, cpgh__fjpk,
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
        szp__ofzwz = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
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
            ernpr__jlfyl = 'None'
        else:
            ernpr__jlfyl = 'other'
        ugdxt__zbfzo = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            ugdxt__zbfzo += '  cond = ~cond\n'
        ugdxt__zbfzo += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ugdxt__zbfzo += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ugdxt__zbfzo += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ugdxt__zbfzo += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {ernpr__jlfyl})
"""
        ugdxt__zbfzo += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        sgoz__vnn = {}
        exec(ugdxt__zbfzo, {'bodo': bodo, 'np': np}, sgoz__vnn)
        impl = sgoz__vnn['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        did__lhrw = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(did__lhrw)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    jrnkc__arf = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    cpgh__fjpk = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', jrnkc__arf, cpgh__fjpk,
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
    nvjid__ljyre = is_overload_constant_nan(other)
    if not (is_default or nvjid__ljyre or is_scalar_type(other) or 
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
            eezq__nyvwg = arr.dtype.elem_type
        else:
            eezq__nyvwg = arr.dtype
        if is_iterable_type(other):
            xegy__xalg = other.dtype
        elif nvjid__ljyre:
            xegy__xalg = types.float64
        else:
            xegy__xalg = types.unliteral(other)
        if not nvjid__ljyre and not is_common_scalar_dtype([eezq__nyvwg,
            xegy__xalg]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        jrnkc__arf = dict(level=level, axis=axis)
        cpgh__fjpk = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), jrnkc__arf,
            cpgh__fjpk, package_name='pandas', module_name='Series')
        maeg__jdodt = other == string_type or is_overload_constant_str(other)
        eau__ooh = is_iterable_type(other) and other.dtype == string_type
        jeb__efkh = S.dtype == string_type and (op == operator.add and (
            maeg__jdodt or eau__ooh) or op == operator.mul and isinstance(
            other, types.Integer))
        jsmf__xgqxe = S.dtype == bodo.timedelta64ns
        wspyz__hzs = S.dtype == bodo.datetime64ns
        afo__xyb = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        oizws__vvjyv = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        wukdl__tpu = jsmf__xgqxe and (afo__xyb or oizws__vvjyv
            ) or wspyz__hzs and afo__xyb
        wukdl__tpu = wukdl__tpu and op == operator.add
        if not (isinstance(S.dtype, types.Number) or jeb__efkh or wukdl__tpu):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        wrmat__pcy = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            zxt__tkam = wrmat__pcy.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and zxt__tkam == types.Array(types.bool_, 1, 'C'):
                zxt__tkam = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                szp__ofzwz = bodo.utils.utils.alloc_type(n, zxt__tkam, (-1,))
                for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                    cze__pikgo = bodo.libs.array_kernels.isna(arr, lwzz__gymn)
                    if cze__pikgo:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(szp__ofzwz,
                                lwzz__gymn)
                        else:
                            szp__ofzwz[lwzz__gymn] = op(fill_value, other)
                    else:
                        szp__ofzwz[lwzz__gymn] = op(arr[lwzz__gymn], other)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        zxt__tkam = wrmat__pcy.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and zxt__tkam == types.Array(
            types.bool_, 1, 'C'):
            zxt__tkam = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            twnf__fiorj = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            szp__ofzwz = bodo.utils.utils.alloc_type(n, zxt__tkam, (-1,))
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                cze__pikgo = bodo.libs.array_kernels.isna(arr, lwzz__gymn)
                vgaen__tdw = bodo.libs.array_kernels.isna(twnf__fiorj,
                    lwzz__gymn)
                if cze__pikgo and vgaen__tdw:
                    bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                elif cze__pikgo:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                    else:
                        szp__ofzwz[lwzz__gymn] = op(fill_value, twnf__fiorj
                            [lwzz__gymn])
                elif vgaen__tdw:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                    else:
                        szp__ofzwz[lwzz__gymn] = op(arr[lwzz__gymn], fill_value
                            )
                else:
                    szp__ofzwz[lwzz__gymn] = op(arr[lwzz__gymn],
                        twnf__fiorj[lwzz__gymn])
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
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
        wrmat__pcy = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            zxt__tkam = wrmat__pcy.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and zxt__tkam == types.Array(types.bool_, 1, 'C'):
                zxt__tkam = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                szp__ofzwz = bodo.utils.utils.alloc_type(n, zxt__tkam, None)
                for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                    cze__pikgo = bodo.libs.array_kernels.isna(arr, lwzz__gymn)
                    if cze__pikgo:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(szp__ofzwz,
                                lwzz__gymn)
                        else:
                            szp__ofzwz[lwzz__gymn] = op(other, fill_value)
                    else:
                        szp__ofzwz[lwzz__gymn] = op(other, arr[lwzz__gymn])
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        zxt__tkam = wrmat__pcy.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and zxt__tkam == types.Array(
            types.bool_, 1, 'C'):
            zxt__tkam = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            twnf__fiorj = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            szp__ofzwz = bodo.utils.utils.alloc_type(n, zxt__tkam, None)
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                cze__pikgo = bodo.libs.array_kernels.isna(arr, lwzz__gymn)
                vgaen__tdw = bodo.libs.array_kernels.isna(twnf__fiorj,
                    lwzz__gymn)
                szp__ofzwz[lwzz__gymn] = op(twnf__fiorj[lwzz__gymn], arr[
                    lwzz__gymn])
                if cze__pikgo and vgaen__tdw:
                    bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                elif cze__pikgo:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                    else:
                        szp__ofzwz[lwzz__gymn] = op(twnf__fiorj[lwzz__gymn],
                            fill_value)
                elif vgaen__tdw:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                    else:
                        szp__ofzwz[lwzz__gymn] = op(fill_value, arr[lwzz__gymn]
                            )
                else:
                    szp__ofzwz[lwzz__gymn] = op(twnf__fiorj[lwzz__gymn],
                        arr[lwzz__gymn])
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
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
    for op, dug__iinq in explicit_binop_funcs_two_ways.items():
        for name in dug__iinq:
            did__lhrw = create_explicit_binary_op_overload(op)
            ynm__xodoh = create_explicit_binary_reverse_op_overload(op)
            fgofo__axb = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(did__lhrw)
            overload_method(SeriesType, fgofo__axb, no_unliteral=True)(
                ynm__xodoh)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        did__lhrw = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(did__lhrw)
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
                qgj__src = bodo.utils.conversion.get_array_if_series_or_index(
                    rhs)
                szp__ofzwz = dt64_arr_sub(arr, qgj__src)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
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
                szp__ofzwz = np.empty(n, np.dtype('datetime64[ns]'))
                for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, lwzz__gymn):
                        bodo.libs.array_kernels.setna(szp__ofzwz, lwzz__gymn)
                        continue
                    nitqv__ardmp = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[lwzz__gymn]))
                    pmz__pahek = op(nitqv__ardmp, rhs)
                    szp__ofzwz[lwzz__gymn
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        pmz__pahek.value)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
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
                    qgj__src = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    szp__ofzwz = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(qgj__src))
                    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                qgj__src = bodo.utils.conversion.get_array_if_series_or_index(
                    rhs)
                szp__ofzwz = op(arr, qgj__src)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    fcn__wvur = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    szp__ofzwz = op(bodo.utils.conversion.
                        unbox_if_timestamp(fcn__wvur), arr)
                    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                fcn__wvur = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                szp__ofzwz = op(fcn__wvur, arr)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        did__lhrw = create_binary_op_overload(op)
        overload(op)(did__lhrw)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    gckk__hin = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, gckk__hin)
        for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, lwzz__gymn
                ) or bodo.libs.array_kernels.isna(arg2, lwzz__gymn):
                bodo.libs.array_kernels.setna(S, lwzz__gymn)
                continue
            S[lwzz__gymn
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                lwzz__gymn]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[lwzz__gymn]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                twnf__fiorj = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, twnf__fiorj)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        did__lhrw = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(did__lhrw)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                szp__ofzwz = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        did__lhrw = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(did__lhrw)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    szp__ofzwz = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
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
                    twnf__fiorj = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    szp__ofzwz = ufunc(arr, twnf__fiorj)
                    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    twnf__fiorj = bodo.hiframes.pd_series_ext.get_series_data(
                        S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    szp__ofzwz = ufunc(arr, twnf__fiorj)
                    return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        did__lhrw = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(did__lhrw)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        jvcl__fqe = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        amtc__ykupv = np.arange(n),
        bodo.libs.timsort.sort(jvcl__fqe, 0, n, amtc__ykupv)
        return amtc__ykupv[0]
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
        dim__mlcnr = get_overload_const_str(downcast)
        if dim__mlcnr in ('integer', 'signed'):
            out_dtype = types.int64
        elif dim__mlcnr == 'unsigned':
            out_dtype = types.uint64
        else:
            assert dim__mlcnr == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            aicr__kqv = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            szp__ofzwz = pd.to_numeric(aicr__kqv, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            ruge__jovuu = np.empty(n, np.float64)
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, lwzz__gymn):
                    bodo.libs.array_kernels.setna(ruge__jovuu, lwzz__gymn)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(ruge__jovuu,
                        lwzz__gymn, arg_a, lwzz__gymn)
            return ruge__jovuu
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            ruge__jovuu = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, lwzz__gymn):
                    bodo.libs.array_kernels.setna(ruge__jovuu, lwzz__gymn)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(ruge__jovuu,
                        lwzz__gymn, arg_a, lwzz__gymn)
            return ruge__jovuu
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        khh__alres = if_series_to_array_type(args[0])
        if isinstance(khh__alres, types.Array) and isinstance(khh__alres.
            dtype, types.Integer):
            khh__alres = types.Array(types.float64, 1, 'C')
        return khh__alres(*args)


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
    zvi__lcfx = bodo.utils.utils.is_array_typ(x, True)
    bfbxj__dxunc = bodo.utils.utils.is_array_typ(y, True)
    ugdxt__zbfzo = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        ugdxt__zbfzo += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if zvi__lcfx and not bodo.utils.utils.is_array_typ(x, False):
        ugdxt__zbfzo += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if bfbxj__dxunc and not bodo.utils.utils.is_array_typ(y, False):
        ugdxt__zbfzo += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    ugdxt__zbfzo += '  n = len(condition)\n'
    trmz__wgequ = x.dtype if zvi__lcfx else types.unliteral(x)
    kxndb__pcb = y.dtype if bfbxj__dxunc else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        trmz__wgequ = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        kxndb__pcb = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    agzb__fnkod = get_data(x)
    dmfmg__upg = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(amtc__ykupv) for
        amtc__ykupv in [agzb__fnkod, dmfmg__upg])
    if dmfmg__upg == types.none:
        if isinstance(trmz__wgequ, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif agzb__fnkod == dmfmg__upg and not is_nullable:
        out_dtype = dtype_to_array_type(trmz__wgequ)
    elif trmz__wgequ == string_type or kxndb__pcb == string_type:
        out_dtype = bodo.string_array_type
    elif agzb__fnkod == bytes_type or (zvi__lcfx and trmz__wgequ == bytes_type
        ) and (dmfmg__upg == bytes_type or bfbxj__dxunc and kxndb__pcb ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(trmz__wgequ, bodo.PDCategoricalDtype):
        out_dtype = None
    elif trmz__wgequ in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(trmz__wgequ, 1, 'C')
    elif kxndb__pcb in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(kxndb__pcb, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(trmz__wgequ), numba.np.numpy_support.
            as_dtype(kxndb__pcb)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(trmz__wgequ, bodo.PDCategoricalDtype):
        xwpi__rmtl = 'x'
    else:
        xwpi__rmtl = 'out_dtype'
    ugdxt__zbfzo += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {xwpi__rmtl}, (-1,))\n')
    if isinstance(trmz__wgequ, bodo.PDCategoricalDtype):
        ugdxt__zbfzo += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        ugdxt__zbfzo += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    ugdxt__zbfzo += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    ugdxt__zbfzo += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if zvi__lcfx:
        ugdxt__zbfzo += '      if bodo.libs.array_kernels.isna(x, j):\n'
        ugdxt__zbfzo += '        setna(out_arr, j)\n'
        ugdxt__zbfzo += '        continue\n'
    if isinstance(trmz__wgequ, bodo.PDCategoricalDtype):
        ugdxt__zbfzo += '      out_codes[j] = x_codes[j]\n'
    else:
        ugdxt__zbfzo += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if zvi__lcfx else 'x'))
    ugdxt__zbfzo += '    else:\n'
    if bfbxj__dxunc:
        ugdxt__zbfzo += '      if bodo.libs.array_kernels.isna(y, j):\n'
        ugdxt__zbfzo += '        setna(out_arr, j)\n'
        ugdxt__zbfzo += '        continue\n'
    if dmfmg__upg == types.none:
        if isinstance(trmz__wgequ, bodo.PDCategoricalDtype):
            ugdxt__zbfzo += '      out_codes[j] = -1\n'
        else:
            ugdxt__zbfzo += '      setna(out_arr, j)\n'
    else:
        ugdxt__zbfzo += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if bfbxj__dxunc else 'y'))
    ugdxt__zbfzo += '  return out_arr\n'
    sgoz__vnn = {}
    exec(ugdxt__zbfzo, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, sgoz__vnn)
    ozh__cfc = sgoz__vnn['_impl']
    return ozh__cfc


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
        wxeon__meer = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(wxeon__meer, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(wxeon__meer):
            ittbz__ecp = wxeon__meer.data.dtype
        else:
            ittbz__ecp = wxeon__meer.dtype
        if isinstance(ittbz__ecp, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        eqmzh__ytt = wxeon__meer
    else:
        ffmx__vzh = []
        for wxeon__meer in choicelist:
            if not bodo.utils.utils.is_array_typ(wxeon__meer, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(wxeon__meer):
                ittbz__ecp = wxeon__meer.data.dtype
            else:
                ittbz__ecp = wxeon__meer.dtype
            if isinstance(ittbz__ecp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            ffmx__vzh.append(ittbz__ecp)
        if not is_common_scalar_dtype(ffmx__vzh):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        eqmzh__ytt = choicelist[0]
    if is_series_type(eqmzh__ytt):
        eqmzh__ytt = eqmzh__ytt.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, eqmzh__ytt.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(eqmzh__ytt, types.Array) or isinstance(eqmzh__ytt,
        BooleanArrayType) or isinstance(eqmzh__ytt, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(eqmzh__ytt, False) and eqmzh__ytt.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {eqmzh__ytt} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    ugfdg__vwaw = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        nroo__rpmx = choicelist.dtype
    else:
        tgilf__cscud = False
        ffmx__vzh = []
        for wxeon__meer in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                wxeon__meer, 'numpy.select()')
            if is_nullable_type(wxeon__meer):
                tgilf__cscud = True
            if is_series_type(wxeon__meer):
                ittbz__ecp = wxeon__meer.data.dtype
            else:
                ittbz__ecp = wxeon__meer.dtype
            if isinstance(ittbz__ecp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            ffmx__vzh.append(ittbz__ecp)
        ofnb__icem, yce__tshup = get_common_scalar_dtype(ffmx__vzh)
        if not yce__tshup:
            raise BodoError('Internal error in overload_np_select')
        iiql__hvnr = dtype_to_array_type(ofnb__icem)
        if tgilf__cscud:
            iiql__hvnr = to_nullable_type(iiql__hvnr)
        nroo__rpmx = iiql__hvnr
    if isinstance(nroo__rpmx, SeriesType):
        nroo__rpmx = nroo__rpmx.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        wodl__eovm = True
    else:
        wodl__eovm = False
    nmv__shqc = False
    lhmlh__vyigi = False
    if wodl__eovm:
        if isinstance(nroo__rpmx.dtype, types.Number):
            pass
        elif nroo__rpmx.dtype == types.bool_:
            lhmlh__vyigi = True
        else:
            nmv__shqc = True
            nroo__rpmx = to_nullable_type(nroo__rpmx)
    elif default == types.none or is_overload_constant_nan(default):
        nmv__shqc = True
        nroo__rpmx = to_nullable_type(nroo__rpmx)
    ugdxt__zbfzo = 'def np_select_impl(condlist, choicelist, default=0):\n'
    ugdxt__zbfzo += '  if len(condlist) != len(choicelist):\n'
    ugdxt__zbfzo += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    ugdxt__zbfzo += '  output_len = len(choicelist[0])\n'
    ugdxt__zbfzo += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    ugdxt__zbfzo += '  for i in range(output_len):\n'
    if nmv__shqc:
        ugdxt__zbfzo += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif lhmlh__vyigi:
        ugdxt__zbfzo += '    out[i] = False\n'
    else:
        ugdxt__zbfzo += '    out[i] = default\n'
    if ugfdg__vwaw:
        ugdxt__zbfzo += '  for i in range(len(condlist) - 1, -1, -1):\n'
        ugdxt__zbfzo += '    cond = condlist[i]\n'
        ugdxt__zbfzo += '    choice = choicelist[i]\n'
        ugdxt__zbfzo += '    out = np.where(cond, choice, out)\n'
    else:
        for lwzz__gymn in range(len(choicelist) - 1, -1, -1):
            ugdxt__zbfzo += f'  cond = condlist[{lwzz__gymn}]\n'
            ugdxt__zbfzo += f'  choice = choicelist[{lwzz__gymn}]\n'
            ugdxt__zbfzo += f'  out = np.where(cond, choice, out)\n'
    ugdxt__zbfzo += '  return out'
    sgoz__vnn = dict()
    exec(ugdxt__zbfzo, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': nroo__rpmx}, sgoz__vnn)
    impl = sgoz__vnn['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        szp__ofzwz = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    jrnkc__arf = dict(subset=subset, keep=keep, inplace=inplace)
    cpgh__fjpk = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', jrnkc__arf, cpgh__fjpk,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        qot__nkvft = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (qot__nkvft,), taxbg__dqm = bodo.libs.array_kernels.drop_duplicates((
            qot__nkvft,), index, 1)
        index = bodo.utils.conversion.index_from_array(taxbg__dqm)
        return bodo.hiframes.pd_series_ext.init_series(qot__nkvft, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    reveo__ghgs = element_type(S.data)
    if not is_common_scalar_dtype([reveo__ghgs, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([reveo__ghgs, right]):
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
        szp__ofzwz = np.empty(n, np.bool_)
        for lwzz__gymn in numba.parfors.parfor.internal_prange(n):
            nif__rho = bodo.utils.conversion.box_if_dt64(arr[lwzz__gymn])
            if inclusive == 'both':
                szp__ofzwz[lwzz__gymn] = nif__rho <= right and nif__rho >= left
            else:
                szp__ofzwz[lwzz__gymn] = nif__rho < right and nif__rho > left
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    jrnkc__arf = dict(axis=axis)
    cpgh__fjpk = dict(axis=None)
    check_unsupported_args('Series.repeat', jrnkc__arf, cpgh__fjpk,
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
            taxbg__dqm = bodo.utils.conversion.index_to_array(index)
            szp__ofzwz = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            phno__nfiyy = bodo.libs.array_kernels.repeat_kernel(taxbg__dqm,
                repeats)
            kepaf__eutjv = bodo.utils.conversion.index_from_array(phno__nfiyy)
            return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
                kepaf__eutjv, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        taxbg__dqm = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        szp__ofzwz = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        phno__nfiyy = bodo.libs.array_kernels.repeat_kernel(taxbg__dqm, repeats
            )
        kepaf__eutjv = bodo.utils.conversion.index_from_array(phno__nfiyy)
        return bodo.hiframes.pd_series_ext.init_series(szp__ofzwz,
            kepaf__eutjv, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        amtc__ykupv = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(amtc__ykupv)
        lcd__bzx = {}
        for lwzz__gymn in range(n):
            nif__rho = bodo.utils.conversion.box_if_dt64(amtc__ykupv[
                lwzz__gymn])
            lcd__bzx[index[lwzz__gymn]] = nif__rho
        return lcd__bzx
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    znxyd__fmkz = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            lgd__gdiy = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(znxyd__fmkz)
    elif is_literal_type(name):
        lgd__gdiy = get_literal_value(name)
    else:
        raise_bodo_error(znxyd__fmkz)
    lgd__gdiy = 0 if lgd__gdiy is None else lgd__gdiy

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (lgd__gdiy,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
