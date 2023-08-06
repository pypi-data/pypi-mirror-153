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
            ycpac__dkuo = bodo.hiframes.pd_series_ext.get_series_data(s)
            qklbb__kmqx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                ycpac__dkuo)
            return qklbb__kmqx
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
            aysfg__wjq = list()
            for vnff__zpr in range(len(S)):
                aysfg__wjq.append(S.iat[vnff__zpr])
            return aysfg__wjq
        return impl_float

    def impl(S):
        aysfg__wjq = list()
        for vnff__zpr in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, vnff__zpr):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            aysfg__wjq.append(S.iat[vnff__zpr])
        return aysfg__wjq
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    huocx__fpfe = dict(dtype=dtype, copy=copy, na_value=na_value)
    xjsx__fyodi = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    huocx__fpfe = dict(name=name, inplace=inplace)
    xjsx__fyodi = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', huocx__fpfe, xjsx__fyodi,
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
        ruf__cpd = ', '.join(['index_arrs[{}]'.format(vnff__zpr) for
            vnff__zpr in range(S.index.nlevels)])
    else:
        ruf__cpd = '    bodo.utils.conversion.index_to_array(index)\n'
    kzxfe__dmbb = 'index' if 'index' != series_name else 'level_0'
    nnbe__zfu = get_index_names(S.index, 'Series.reset_index()', kzxfe__dmbb)
    columns = [name for name in nnbe__zfu]
    columns.append(series_name)
    uletk__mwfb = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    uletk__mwfb += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    uletk__mwfb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        uletk__mwfb += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    uletk__mwfb += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    uletk__mwfb += '    col_var = {}\n'.format(gen_const_tup(columns))
    uletk__mwfb += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({ruf__cpd}, arr), df_index, col_var)
"""
    pjg__uypv = {}
    exec(uletk__mwfb, {'bodo': bodo}, pjg__uypv)
    lcz__pcy = pjg__uypv['_impl']
    return lcz__pcy


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rzgag__kftq = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
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
        rzgag__kftq = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for vnff__zpr in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[vnff__zpr]):
                bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
            else:
                rzgag__kftq[vnff__zpr] = np.round(arr[vnff__zpr], decimals)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    xjsx__fyodi = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        zzgkk__ozm = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = 0
            if not bodo.libs.array_kernels.isna(A, vnff__zpr):
                qfp__iffc = int(A[vnff__zpr])
            zzgkk__ozm += qfp__iffc
        return zzgkk__ozm != 0
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
        nrtm__crswc = bodo.hiframes.pd_series_ext.get_series_data(S)
        oziv__ugz = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        zzgkk__ozm = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(nrtm__crswc)
            ):
            qfp__iffc = 0
            krnv__fxldu = bodo.libs.array_kernels.isna(nrtm__crswc, vnff__zpr)
            irir__zujui = bodo.libs.array_kernels.isna(oziv__ugz, vnff__zpr)
            if (krnv__fxldu and not irir__zujui or not krnv__fxldu and
                irir__zujui):
                qfp__iffc = 1
            elif not krnv__fxldu:
                if nrtm__crswc[vnff__zpr] != oziv__ugz[vnff__zpr]:
                    qfp__iffc = 1
            zzgkk__ozm += qfp__iffc
        return zzgkk__ozm == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    huocx__fpfe = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    xjsx__fyodi = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        zzgkk__ozm = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = 0
            if not bodo.libs.array_kernels.isna(A, vnff__zpr):
                qfp__iffc = int(not A[vnff__zpr])
            zzgkk__ozm += qfp__iffc
        return zzgkk__ozm == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    huocx__fpfe = dict(level=level)
    xjsx__fyodi = dict(level=None)
    check_unsupported_args('Series.mad', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    mjyhj__wnp = types.float64
    uxom__pfby = types.float64
    if S.dtype == types.float32:
        mjyhj__wnp = types.float32
        uxom__pfby = types.float32
    kfpv__slhph = mjyhj__wnp(0)
    zhmga__opfsi = uxom__pfby(0)
    rqv__moqor = uxom__pfby(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        fcwpv__vfp = kfpv__slhph
        zzgkk__ozm = zhmga__opfsi
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = kfpv__slhph
            gcmpv__ojh = zhmga__opfsi
            if not bodo.libs.array_kernels.isna(A, vnff__zpr) or not skipna:
                qfp__iffc = A[vnff__zpr]
                gcmpv__ojh = rqv__moqor
            fcwpv__vfp += qfp__iffc
            zzgkk__ozm += gcmpv__ojh
        ten__cbwd = bodo.hiframes.series_kernels._mean_handle_nan(fcwpv__vfp,
            zzgkk__ozm)
        wdot__dfbqc = kfpv__slhph
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = kfpv__slhph
            if not bodo.libs.array_kernels.isna(A, vnff__zpr) or not skipna:
                qfp__iffc = abs(A[vnff__zpr] - ten__cbwd)
            wdot__dfbqc += qfp__iffc
        loc__rqdj = bodo.hiframes.series_kernels._mean_handle_nan(wdot__dfbqc,
            zzgkk__ozm)
        return loc__rqdj
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    huocx__fpfe = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', huocx__fpfe, xjsx__fyodi,
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
        jmjyw__smu = 0
        wlsbd__pnch = 0
        zzgkk__ozm = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = 0
            gcmpv__ojh = 0
            if not bodo.libs.array_kernels.isna(A, vnff__zpr) or not skipna:
                qfp__iffc = A[vnff__zpr]
                gcmpv__ojh = 1
            jmjyw__smu += qfp__iffc
            wlsbd__pnch += qfp__iffc * qfp__iffc
            zzgkk__ozm += gcmpv__ojh
        qcavx__txs = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            jmjyw__smu, wlsbd__pnch, zzgkk__ozm, ddof)
        nsec__zehu = bodo.hiframes.series_kernels._sem_handle_nan(qcavx__txs,
            zzgkk__ozm)
        return nsec__zehu
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', huocx__fpfe, xjsx__fyodi,
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
        jmjyw__smu = 0.0
        wlsbd__pnch = 0.0
        mxjw__xgo = 0.0
        wabxi__rug = 0.0
        zzgkk__ozm = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = 0.0
            gcmpv__ojh = 0
            if not bodo.libs.array_kernels.isna(A, vnff__zpr) or not skipna:
                qfp__iffc = np.float64(A[vnff__zpr])
                gcmpv__ojh = 1
            jmjyw__smu += qfp__iffc
            wlsbd__pnch += qfp__iffc ** 2
            mxjw__xgo += qfp__iffc ** 3
            wabxi__rug += qfp__iffc ** 4
            zzgkk__ozm += gcmpv__ojh
        qcavx__txs = bodo.hiframes.series_kernels.compute_kurt(jmjyw__smu,
            wlsbd__pnch, mxjw__xgo, wabxi__rug, zzgkk__ozm)
        return qcavx__txs
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', huocx__fpfe, xjsx__fyodi,
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
        jmjyw__smu = 0.0
        wlsbd__pnch = 0.0
        mxjw__xgo = 0.0
        zzgkk__ozm = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(A)):
            qfp__iffc = 0.0
            gcmpv__ojh = 0
            if not bodo.libs.array_kernels.isna(A, vnff__zpr) or not skipna:
                qfp__iffc = np.float64(A[vnff__zpr])
                gcmpv__ojh = 1
            jmjyw__smu += qfp__iffc
            wlsbd__pnch += qfp__iffc ** 2
            mxjw__xgo += qfp__iffc ** 3
            zzgkk__ozm += gcmpv__ojh
        qcavx__txs = bodo.hiframes.series_kernels.compute_skew(jmjyw__smu,
            wlsbd__pnch, mxjw__xgo, zzgkk__ozm)
        return qcavx__txs
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', huocx__fpfe, xjsx__fyodi,
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
        nrtm__crswc = bodo.hiframes.pd_series_ext.get_series_data(S)
        oziv__ugz = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        bevq__mtzrv = 0
        for vnff__zpr in numba.parfors.parfor.internal_prange(len(nrtm__crswc)
            ):
            jjowg__mjai = nrtm__crswc[vnff__zpr]
            odb__tlm = oziv__ugz[vnff__zpr]
            bevq__mtzrv += jjowg__mjai * odb__tlm
        return bevq__mtzrv
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    huocx__fpfe = dict(skipna=skipna)
    xjsx__fyodi = dict(skipna=True)
    check_unsupported_args('Series.cumsum', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(skipna=skipna)
    xjsx__fyodi = dict(skipna=True)
    check_unsupported_args('Series.cumprod', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(skipna=skipna)
    xjsx__fyodi = dict(skipna=True)
    check_unsupported_args('Series.cummin', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(skipna=skipna)
    xjsx__fyodi = dict(skipna=True)
    check_unsupported_args('Series.cummax', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    xjsx__fyodi = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        gtl__endq = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, gtl__endq, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    huocx__fpfe = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    xjsx__fyodi = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(level=level)
    xjsx__fyodi = dict(level=None)
    check_unsupported_args('Series.count', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    huocx__fpfe = dict(method=method, min_periods=min_periods)
    xjsx__fyodi = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        zsx__ldod = S.sum()
        jgdit__syhux = other.sum()
        a = n * (S * other).sum() - zsx__ldod * jgdit__syhux
        ufj__afpwr = n * (S ** 2).sum() - zsx__ldod ** 2
        hfk__pabx = n * (other ** 2).sum() - jgdit__syhux ** 2
        return a / np.sqrt(ufj__afpwr * hfk__pabx)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    huocx__fpfe = dict(min_periods=min_periods)
    xjsx__fyodi = dict(min_periods=None)
    check_unsupported_args('Series.cov', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        zsx__ldod = S.mean()
        jgdit__syhux = other.mean()
        jto__zuar = ((S - zsx__ldod) * (other - jgdit__syhux)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(jto__zuar, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            paydv__peumr = np.sign(sum_val)
            return np.inf * paydv__peumr
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    huocx__fpfe = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(axis=axis, skipna=skipna)
    xjsx__fyodi = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(axis=axis, skipna=skipna)
    xjsx__fyodi = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', huocx__fpfe, xjsx__fyodi,
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
    huocx__fpfe = dict(level=level, numeric_only=numeric_only)
    xjsx__fyodi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', huocx__fpfe, xjsx__fyodi,
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
        bvo__smz = arr[:n]
        bagq__oyijo = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(bvo__smz,
            bagq__oyijo, name)
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
        azbih__ybv = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bvo__smz = arr[azbih__ybv:]
        bagq__oyijo = index[azbih__ybv:]
        return bodo.hiframes.pd_series_ext.init_series(bvo__smz,
            bagq__oyijo, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    xctpb__rakoi = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in xctpb__rakoi:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            sik__dmrh = index[0]
            ygul__ehgch = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, sik__dmrh,
                False))
        else:
            ygul__ehgch = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bvo__smz = arr[:ygul__ehgch]
        bagq__oyijo = index[:ygul__ehgch]
        return bodo.hiframes.pd_series_ext.init_series(bvo__smz,
            bagq__oyijo, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    xctpb__rakoi = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in xctpb__rakoi:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            epugl__pzlhx = index[-1]
            ygul__ehgch = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                epugl__pzlhx, True))
        else:
            ygul__ehgch = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bvo__smz = arr[len(arr) - ygul__ehgch:]
        bagq__oyijo = index[len(arr) - ygul__ehgch:]
        return bodo.hiframes.pd_series_ext.init_series(bvo__smz,
            bagq__oyijo, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mnqbk__yyqvi = bodo.utils.conversion.index_to_array(index)
        zvtl__ntte, zizmr__ieurq = (bodo.libs.array_kernels.
            first_last_valid_index(arr, mnqbk__yyqvi))
        return zizmr__ieurq if zvtl__ntte else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mnqbk__yyqvi = bodo.utils.conversion.index_to_array(index)
        zvtl__ntte, zizmr__ieurq = (bodo.libs.array_kernels.
            first_last_valid_index(arr, mnqbk__yyqvi, False))
        return zizmr__ieurq if zvtl__ntte else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    huocx__fpfe = dict(keep=keep)
    xjsx__fyodi = dict(keep='first')
    check_unsupported_args('Series.nlargest', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mnqbk__yyqvi = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rzgag__kftq, mnmh__nvk = bodo.libs.array_kernels.nlargest(arr,
            mnqbk__yyqvi, n, True, bodo.hiframes.series_kernels.gt_f)
        pcqf__cip = bodo.utils.conversion.convert_to_index(mnmh__nvk)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
            pcqf__cip, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    huocx__fpfe = dict(keep=keep)
    xjsx__fyodi = dict(keep='first')
    check_unsupported_args('Series.nsmallest', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        mnqbk__yyqvi = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rzgag__kftq, mnmh__nvk = bodo.libs.array_kernels.nlargest(arr,
            mnqbk__yyqvi, n, False, bodo.hiframes.series_kernels.lt_f)
        pcqf__cip = bodo.utils.conversion.convert_to_index(mnmh__nvk)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
            pcqf__cip, name)
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
    huocx__fpfe = dict(errors=errors)
    xjsx__fyodi = dict(errors='raise')
    check_unsupported_args('Series.astype', huocx__fpfe, xjsx__fyodi,
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
        rzgag__kftq = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    huocx__fpfe = dict(axis=axis, is_copy=is_copy)
    xjsx__fyodi = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        jmhpn__bkiyg = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[jmhpn__bkiyg],
            index[jmhpn__bkiyg], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    huocx__fpfe = dict(axis=axis, kind=kind, order=order)
    xjsx__fyodi = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bytib__jmwxj = S.notna().values
        if not bytib__jmwxj.all():
            rzgag__kftq = np.full(n, -1, np.int64)
            rzgag__kftq[bytib__jmwxj] = argsort(arr[bytib__jmwxj])
        else:
            rzgag__kftq = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    huocx__fpfe = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    xjsx__fyodi = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', huocx__fpfe, xjsx__fyodi,
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
        cwg__geu = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        xgsw__xzy = cwg__geu.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        rzgag__kftq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            xgsw__xzy, 0)
        pcqf__cip = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            xgsw__xzy)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
            pcqf__cip, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    huocx__fpfe = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    xjsx__fyodi = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', huocx__fpfe, xjsx__fyodi,
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
        cwg__geu = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        xgsw__xzy = cwg__geu.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        rzgag__kftq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            xgsw__xzy, 0)
        pcqf__cip = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            xgsw__xzy)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
            pcqf__cip, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    olarm__iaar = is_overload_true(is_nullable)
    uletk__mwfb = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    uletk__mwfb += '  numba.parfors.parfor.init_prange()\n'
    uletk__mwfb += '  n = len(arr)\n'
    if olarm__iaar:
        uletk__mwfb += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        uletk__mwfb += '  out_arr = np.empty(n, np.int64)\n'
    uletk__mwfb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    uletk__mwfb += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if olarm__iaar:
        uletk__mwfb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        uletk__mwfb += '      out_arr[i] = -1\n'
    uletk__mwfb += '      continue\n'
    uletk__mwfb += '    val = arr[i]\n'
    uletk__mwfb += '    if include_lowest and val == bins[0]:\n'
    uletk__mwfb += '      ind = 1\n'
    uletk__mwfb += '    else:\n'
    uletk__mwfb += '      ind = np.searchsorted(bins, val)\n'
    uletk__mwfb += '    if ind == 0 or ind == len(bins):\n'
    if olarm__iaar:
        uletk__mwfb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        uletk__mwfb += '      out_arr[i] = -1\n'
    uletk__mwfb += '    else:\n'
    uletk__mwfb += '      out_arr[i] = ind - 1\n'
    uletk__mwfb += '  return out_arr\n'
    pjg__uypv = {}
    exec(uletk__mwfb, {'bodo': bodo, 'np': np, 'numba': numba}, pjg__uypv)
    impl = pjg__uypv['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        djuyx__nan, jvvi__lngks = np.divmod(x, 1)
        if djuyx__nan == 0:
            btww__gzsc = -int(np.floor(np.log10(abs(jvvi__lngks)))
                ) - 1 + precision
        else:
            btww__gzsc = precision
        return np.around(x, btww__gzsc)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        dpspq__dpl = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(dpspq__dpl)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        svrwx__slj = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            lizr__yfumh = bins.copy()
            if right and include_lowest:
                lizr__yfumh[0] = lizr__yfumh[0] - svrwx__slj
            naeu__xhd = bodo.libs.interval_arr_ext.init_interval_array(
                lizr__yfumh[:-1], lizr__yfumh[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(naeu__xhd,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        lizr__yfumh = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            lizr__yfumh[0] = lizr__yfumh[0] - 10.0 ** -precision
        naeu__xhd = bodo.libs.interval_arr_ext.init_interval_array(lizr__yfumh
            [:-1], lizr__yfumh[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(naeu__xhd, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        ebjqx__ljl = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        rnwh__mdmqe = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        rzgag__kftq = np.zeros(nbins, np.int64)
        for vnff__zpr in range(len(ebjqx__ljl)):
            rzgag__kftq[rnwh__mdmqe[vnff__zpr]] = ebjqx__ljl[vnff__zpr]
        return rzgag__kftq
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
            ihaf__cww = (max_val - min_val) * 0.001
            if right:
                bins[0] -= ihaf__cww
            else:
                bins[-1] += ihaf__cww
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    huocx__fpfe = dict(dropna=dropna)
    xjsx__fyodi = dict(dropna=True)
    check_unsupported_args('Series.value_counts', huocx__fpfe, xjsx__fyodi,
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
    zyih__srzam = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    uletk__mwfb = 'def impl(\n'
    uletk__mwfb += '    S,\n'
    uletk__mwfb += '    normalize=False,\n'
    uletk__mwfb += '    sort=True,\n'
    uletk__mwfb += '    ascending=False,\n'
    uletk__mwfb += '    bins=None,\n'
    uletk__mwfb += '    dropna=True,\n'
    uletk__mwfb += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    uletk__mwfb += '):\n'
    uletk__mwfb += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    uletk__mwfb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    uletk__mwfb += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if zyih__srzam:
        uletk__mwfb += '    right = True\n'
        uletk__mwfb += _gen_bins_handling(bins, S.dtype)
        uletk__mwfb += '    arr = get_bin_inds(bins, arr)\n'
    uletk__mwfb += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    uletk__mwfb += "        (arr,), index, ('$_bodo_col2_',)\n"
    uletk__mwfb += '    )\n'
    uletk__mwfb += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if zyih__srzam:
        uletk__mwfb += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        uletk__mwfb += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        uletk__mwfb += '    index = get_bin_labels(bins)\n'
    else:
        uletk__mwfb += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        uletk__mwfb += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        uletk__mwfb += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        uletk__mwfb += '    )\n'
        uletk__mwfb += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    uletk__mwfb += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        uletk__mwfb += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        ysty__egqmk = 'len(S)' if zyih__srzam else 'count_arr.sum()'
        uletk__mwfb += f'    res = res / float({ysty__egqmk})\n'
    uletk__mwfb += '    return res\n'
    pjg__uypv = {}
    exec(uletk__mwfb, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, pjg__uypv)
    impl = pjg__uypv['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    uletk__mwfb = ''
    if isinstance(bins, types.Integer):
        uletk__mwfb += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        uletk__mwfb += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            uletk__mwfb += '    min_val = min_val.value\n'
            uletk__mwfb += '    max_val = max_val.value\n'
        uletk__mwfb += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            uletk__mwfb += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        uletk__mwfb += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return uletk__mwfb


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    huocx__fpfe = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    xjsx__fyodi = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    uletk__mwfb = 'def impl(\n'
    uletk__mwfb += '    x,\n'
    uletk__mwfb += '    bins,\n'
    uletk__mwfb += '    right=True,\n'
    uletk__mwfb += '    labels=None,\n'
    uletk__mwfb += '    retbins=False,\n'
    uletk__mwfb += '    precision=3,\n'
    uletk__mwfb += '    include_lowest=False,\n'
    uletk__mwfb += "    duplicates='raise',\n"
    uletk__mwfb += '    ordered=True\n'
    uletk__mwfb += '):\n'
    if isinstance(x, SeriesType):
        uletk__mwfb += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        uletk__mwfb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        uletk__mwfb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        uletk__mwfb += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    uletk__mwfb += _gen_bins_handling(bins, x.dtype)
    uletk__mwfb += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    uletk__mwfb += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    uletk__mwfb += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    uletk__mwfb += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        uletk__mwfb += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        uletk__mwfb += '    return res\n'
    else:
        uletk__mwfb += '    return out_arr\n'
    pjg__uypv = {}
    exec(uletk__mwfb, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, pjg__uypv)
    impl = pjg__uypv['impl']
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
    huocx__fpfe = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    xjsx__fyodi = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        rlhjj__rxn = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, rlhjj__rxn)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    huocx__fpfe = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze
        =squeeze, observed=observed, dropna=dropna)
    xjsx__fyodi = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', huocx__fpfe, xjsx__fyodi,
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
            rlqi__pbbe = bodo.utils.conversion.coerce_to_array(index)
            cwg__geu = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                rlqi__pbbe, arr), index, (' ', ''))
            return cwg__geu.groupby(' ')['']
        return impl_index
    jxfk__nlpmr = by
    if isinstance(by, SeriesType):
        jxfk__nlpmr = by.data
    if isinstance(jxfk__nlpmr, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        rlqi__pbbe = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        cwg__geu = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            rlqi__pbbe, arr), index, (' ', ''))
        return cwg__geu.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    huocx__fpfe = dict(verify_integrity=verify_integrity)
    xjsx__fyodi = dict(verify_integrity=False)
    check_unsupported_args('Series.append', huocx__fpfe, xjsx__fyodi,
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
            vbyy__hnvv = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            rzgag__kftq = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(rzgag__kftq, A, vbyy__hnvv, False)
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rzgag__kftq = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    huocx__fpfe = dict(interpolation=interpolation)
    xjsx__fyodi = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            rzgag__kftq = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
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
        xzh__vrt = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(xzh__vrt, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    huocx__fpfe = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    xjsx__fyodi = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', huocx__fpfe, xjsx__fyodi,
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
        agbrh__rsyn = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        agbrh__rsyn = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    uletk__mwfb = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {agbrh__rsyn}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    wcu__kmx = dict()
    exec(uletk__mwfb, {'bodo': bodo, 'numba': numba}, wcu__kmx)
    dxnkf__cphmx = wcu__kmx['impl']
    return dxnkf__cphmx


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        agbrh__rsyn = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        agbrh__rsyn = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    uletk__mwfb = 'def impl(S,\n'
    uletk__mwfb += '     value=None,\n'
    uletk__mwfb += '    method=None,\n'
    uletk__mwfb += '    axis=None,\n'
    uletk__mwfb += '    inplace=False,\n'
    uletk__mwfb += '    limit=None,\n'
    uletk__mwfb += '   downcast=None,\n'
    uletk__mwfb += '):\n'
    uletk__mwfb += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    uletk__mwfb += '    n = len(in_arr)\n'
    uletk__mwfb += f'    out_arr = {agbrh__rsyn}(n, -1)\n'
    uletk__mwfb += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    uletk__mwfb += '        s = in_arr[j]\n'
    uletk__mwfb += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    uletk__mwfb += '            s = value\n'
    uletk__mwfb += '        out_arr[j] = s\n'
    uletk__mwfb += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    wcu__kmx = dict()
    exec(uletk__mwfb, {'bodo': bodo, 'numba': numba}, wcu__kmx)
    dxnkf__cphmx = wcu__kmx['impl']
    return dxnkf__cphmx


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
    vvwah__lguy = bodo.hiframes.pd_series_ext.get_series_data(value)
    for vnff__zpr in numba.parfors.parfor.internal_prange(len(wce__dzsoa)):
        s = wce__dzsoa[vnff__zpr]
        if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr
            ) and not bodo.libs.array_kernels.isna(vvwah__lguy, vnff__zpr):
            s = vvwah__lguy[vnff__zpr]
        wce__dzsoa[vnff__zpr] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
    for vnff__zpr in numba.parfors.parfor.internal_prange(len(wce__dzsoa)):
        s = wce__dzsoa[vnff__zpr]
        if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr):
            s = value
        wce__dzsoa[vnff__zpr] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    vvwah__lguy = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(wce__dzsoa)
    rzgag__kftq = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for yrqz__nxki in numba.parfors.parfor.internal_prange(n):
        s = wce__dzsoa[yrqz__nxki]
        if bodo.libs.array_kernels.isna(wce__dzsoa, yrqz__nxki
            ) and not bodo.libs.array_kernels.isna(vvwah__lguy, yrqz__nxki):
            s = vvwah__lguy[yrqz__nxki]
        rzgag__kftq[yrqz__nxki] = s
        if bodo.libs.array_kernels.isna(wce__dzsoa, yrqz__nxki
            ) and bodo.libs.array_kernels.isna(vvwah__lguy, yrqz__nxki):
            bodo.libs.array_kernels.setna(rzgag__kftq, yrqz__nxki)
    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    vvwah__lguy = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(wce__dzsoa)
    rzgag__kftq = bodo.utils.utils.alloc_type(n, wce__dzsoa.dtype, (-1,))
    for vnff__zpr in numba.parfors.parfor.internal_prange(n):
        s = wce__dzsoa[vnff__zpr]
        if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr
            ) and not bodo.libs.array_kernels.isna(vvwah__lguy, vnff__zpr):
            s = vvwah__lguy[vnff__zpr]
        rzgag__kftq[vnff__zpr] = s
    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    huocx__fpfe = dict(limit=limit, downcast=downcast)
    xjsx__fyodi = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', huocx__fpfe, xjsx__fyodi,
        package_name='pandas', module_name='Series')
    eiod__vab = not is_overload_none(value)
    aqpun__hxdl = not is_overload_none(method)
    if eiod__vab and aqpun__hxdl:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not eiod__vab and not aqpun__hxdl:
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
    if aqpun__hxdl:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        dlyu__ebn = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(dlyu__ebn)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(dlyu__ebn)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    gymyo__tcg = element_type(S.data)
    leie__ubqa = None
    if eiod__vab:
        leie__ubqa = element_type(types.unliteral(value))
    if leie__ubqa and not can_replace(gymyo__tcg, leie__ubqa):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {leie__ubqa} with series type {gymyo__tcg}'
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
        kio__led = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                vvwah__lguy = bodo.hiframes.pd_series_ext.get_series_data(value
                    )
                n = len(wce__dzsoa)
                rzgag__kftq = bodo.utils.utils.alloc_type(n, kio__led, (-1,))
                for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr
                        ) and bodo.libs.array_kernels.isna(vvwah__lguy,
                        vnff__zpr):
                        bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                        continue
                    if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr):
                        rzgag__kftq[vnff__zpr
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            vvwah__lguy[vnff__zpr])
                        continue
                    rzgag__kftq[vnff__zpr
                        ] = bodo.utils.conversion.unbox_if_timestamp(wce__dzsoa
                        [vnff__zpr])
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return fillna_series_impl
        if aqpun__hxdl:
            zde__ndabd = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(gymyo__tcg, (types.Integer, types.Float)
                ) and gymyo__tcg not in zde__ndabd:
                raise BodoError(
                    f"Series.fillna(): series of type {gymyo__tcg} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                rzgag__kftq = bodo.libs.array_kernels.ffill_bfill_arr(
                    wce__dzsoa, method)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(wce__dzsoa)
            rzgag__kftq = bodo.utils.utils.alloc_type(n, kio__led, (-1,))
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(wce__dzsoa[
                    vnff__zpr])
                if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr):
                    s = value
                rzgag__kftq[vnff__zpr] = s
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        ourn__uqy = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        huocx__fpfe = dict(limit=limit, downcast=downcast)
        xjsx__fyodi = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', huocx__fpfe,
            xjsx__fyodi, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        gymyo__tcg = element_type(S.data)
        zde__ndabd = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(gymyo__tcg, (types.Integer, types.Float)
            ) and gymyo__tcg not in zde__ndabd:
            raise BodoError(
                f'Series.{overload_name}(): series of type {gymyo__tcg} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rzgag__kftq = bodo.libs.array_kernels.ffill_bfill_arr(wce__dzsoa,
                ourn__uqy)
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        breje__grp = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            breje__grp)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        anq__lhmsk = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(anq__lhmsk)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        anq__lhmsk = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(anq__lhmsk)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        anq__lhmsk = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(anq__lhmsk)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    huocx__fpfe = dict(inplace=inplace, limit=limit, regex=regex, method=method
        )
    nlek__oxxgp = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', huocx__fpfe, nlek__oxxgp,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    gymyo__tcg = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        uoc__sfint = element_type(to_replace.key_type)
        leie__ubqa = element_type(to_replace.value_type)
    else:
        uoc__sfint = element_type(to_replace)
        leie__ubqa = element_type(value)
    uztm__dzl = None
    if gymyo__tcg != types.unliteral(uoc__sfint):
        if bodo.utils.typing.equality_always_false(gymyo__tcg, types.
            unliteral(uoc__sfint)
            ) or not bodo.utils.typing.types_equality_exists(gymyo__tcg,
            uoc__sfint):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(gymyo__tcg, (types.Float, types.Integer)
            ) or gymyo__tcg == np.bool_:
            uztm__dzl = gymyo__tcg
    if not can_replace(gymyo__tcg, types.unliteral(leie__ubqa)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    ipnda__hldiv = to_str_arr_if_dict_array(S.data)
    if isinstance(ipnda__hldiv, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(wce__dzsoa.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(wce__dzsoa)
        rzgag__kftq = bodo.utils.utils.alloc_type(n, ipnda__hldiv, (-1,))
        rkwnu__dmjh = build_replace_dict(to_replace, value, uztm__dzl)
        for vnff__zpr in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(wce__dzsoa, vnff__zpr):
                bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                continue
            s = wce__dzsoa[vnff__zpr]
            if s in rkwnu__dmjh:
                s = rkwnu__dmjh[s]
            rzgag__kftq[vnff__zpr] = s
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    egtg__qqtl = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    hoq__vhtd = is_iterable_type(to_replace)
    ajw__bfol = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    alrg__abnj = is_iterable_type(value)
    if egtg__qqtl and ajw__bfol:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                rkwnu__dmjh = {}
                rkwnu__dmjh[key_dtype_conv(to_replace)] = value
                return rkwnu__dmjh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            rkwnu__dmjh = {}
            rkwnu__dmjh[to_replace] = value
            return rkwnu__dmjh
        return impl
    if hoq__vhtd and ajw__bfol:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                rkwnu__dmjh = {}
                for redg__zcnb in to_replace:
                    rkwnu__dmjh[key_dtype_conv(redg__zcnb)] = value
                return rkwnu__dmjh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            rkwnu__dmjh = {}
            for redg__zcnb in to_replace:
                rkwnu__dmjh[redg__zcnb] = value
            return rkwnu__dmjh
        return impl
    if hoq__vhtd and alrg__abnj:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                rkwnu__dmjh = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for vnff__zpr in range(len(to_replace)):
                    rkwnu__dmjh[key_dtype_conv(to_replace[vnff__zpr])] = value[
                        vnff__zpr]
                return rkwnu__dmjh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            rkwnu__dmjh = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for vnff__zpr in range(len(to_replace)):
                rkwnu__dmjh[to_replace[vnff__zpr]] = value[vnff__zpr]
            return rkwnu__dmjh
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
            rzgag__kftq = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rzgag__kftq = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    huocx__fpfe = dict(ignore_index=ignore_index)
    jeuuq__hpc = dict(ignore_index=False)
    check_unsupported_args('Series.explode', huocx__fpfe, jeuuq__hpc,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mnqbk__yyqvi = bodo.utils.conversion.index_to_array(index)
        rzgag__kftq, ogml__tuo = bodo.libs.array_kernels.explode(arr,
            mnqbk__yyqvi)
        pcqf__cip = bodo.utils.conversion.index_from_array(ogml__tuo)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
            pcqf__cip, name)
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
            zgbqk__qemzr = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                zgbqk__qemzr[vnff__zpr] = np.argmax(a[vnff__zpr])
            return zgbqk__qemzr
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            zzq__ibxs = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                zzq__ibxs[vnff__zpr] = np.argmin(a[vnff__zpr])
            return zzq__ibxs
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
    huocx__fpfe = dict(axis=axis, inplace=inplace, how=how)
    ekrrk__gfo = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', huocx__fpfe, ekrrk__gfo,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            bytib__jmwxj = S.notna().values
            mnqbk__yyqvi = bodo.utils.conversion.extract_index_array(S)
            pcqf__cip = bodo.utils.conversion.convert_to_index(mnqbk__yyqvi
                [bytib__jmwxj])
            rzgag__kftq = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(wce__dzsoa))
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                pcqf__cip, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mnqbk__yyqvi = bodo.utils.conversion.extract_index_array(S)
            bytib__jmwxj = S.notna().values
            pcqf__cip = bodo.utils.conversion.convert_to_index(mnqbk__yyqvi
                [bytib__jmwxj])
            rzgag__kftq = wce__dzsoa[bytib__jmwxj]
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                pcqf__cip, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    huocx__fpfe = dict(freq=freq, axis=axis, fill_value=fill_value)
    xjsx__fyodi = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', huocx__fpfe, xjsx__fyodi,
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
        rzgag__kftq = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    huocx__fpfe = dict(fill_method=fill_method, limit=limit, freq=freq)
    xjsx__fyodi = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', huocx__fpfe, xjsx__fyodi,
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
        rzgag__kftq = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
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
            bikvs__fju = 'None'
        else:
            bikvs__fju = 'other'
        uletk__mwfb = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            uletk__mwfb += '  cond = ~cond\n'
        uletk__mwfb += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        uletk__mwfb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        uletk__mwfb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        uletk__mwfb += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {bikvs__fju})
"""
        uletk__mwfb += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        pjg__uypv = {}
        exec(uletk__mwfb, {'bodo': bodo, 'np': np}, pjg__uypv)
        impl = pjg__uypv['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        breje__grp = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(breje__grp)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    huocx__fpfe = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    xjsx__fyodi = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', huocx__fpfe, xjsx__fyodi,
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
    bowy__lybf = is_overload_constant_nan(other)
    if not (is_default or bowy__lybf or is_scalar_type(other) or isinstance
        (other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
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
            njit__gdjnk = arr.dtype.elem_type
        else:
            njit__gdjnk = arr.dtype
        if is_iterable_type(other):
            fpz__nqmi = other.dtype
        elif bowy__lybf:
            fpz__nqmi = types.float64
        else:
            fpz__nqmi = types.unliteral(other)
        if not bowy__lybf and not is_common_scalar_dtype([njit__gdjnk,
            fpz__nqmi]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        huocx__fpfe = dict(level=level, axis=axis)
        xjsx__fyodi = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), huocx__fpfe,
            xjsx__fyodi, package_name='pandas', module_name='Series')
        qcez__dxj = other == string_type or is_overload_constant_str(other)
        oespz__mwd = is_iterable_type(other) and other.dtype == string_type
        gotta__hou = S.dtype == string_type and (op == operator.add and (
            qcez__dxj or oespz__mwd) or op == operator.mul and isinstance(
            other, types.Integer))
        evbru__zgmb = S.dtype == bodo.timedelta64ns
        oxb__dexnq = S.dtype == bodo.datetime64ns
        xcups__ywyx = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        tbs__dpv = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        sdxh__uvaoo = evbru__zgmb and (xcups__ywyx or tbs__dpv
            ) or oxb__dexnq and xcups__ywyx
        sdxh__uvaoo = sdxh__uvaoo and op == operator.add
        if not (isinstance(S.dtype, types.Number) or gotta__hou or sdxh__uvaoo
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        edn__msgec = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            ipnda__hldiv = edn__msgec.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and ipnda__hldiv == types.Array(types.bool_, 1, 'C'):
                ipnda__hldiv = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                rzgag__kftq = bodo.utils.utils.alloc_type(n, ipnda__hldiv,
                    (-1,))
                for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                    khj__tezx = bodo.libs.array_kernels.isna(arr, vnff__zpr)
                    if khj__tezx:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(rzgag__kftq,
                                vnff__zpr)
                        else:
                            rzgag__kftq[vnff__zpr] = op(fill_value, other)
                    else:
                        rzgag__kftq[vnff__zpr] = op(arr[vnff__zpr], other)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        ipnda__hldiv = edn__msgec.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType
            ) and ipnda__hldiv == types.Array(types.bool_, 1, 'C'):
            ipnda__hldiv = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pcf__njbs = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            rzgag__kftq = bodo.utils.utils.alloc_type(n, ipnda__hldiv, (-1,))
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                khj__tezx = bodo.libs.array_kernels.isna(arr, vnff__zpr)
                tkz__ynve = bodo.libs.array_kernels.isna(pcf__njbs, vnff__zpr)
                if khj__tezx and tkz__ynve:
                    bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                elif khj__tezx:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                    else:
                        rzgag__kftq[vnff__zpr] = op(fill_value, pcf__njbs[
                            vnff__zpr])
                elif tkz__ynve:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                    else:
                        rzgag__kftq[vnff__zpr] = op(arr[vnff__zpr], fill_value)
                else:
                    rzgag__kftq[vnff__zpr] = op(arr[vnff__zpr], pcf__njbs[
                        vnff__zpr])
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
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
        edn__msgec = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            ipnda__hldiv = edn__msgec.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and ipnda__hldiv == types.Array(types.bool_, 1, 'C'):
                ipnda__hldiv = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                rzgag__kftq = bodo.utils.utils.alloc_type(n, ipnda__hldiv, None
                    )
                for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                    khj__tezx = bodo.libs.array_kernels.isna(arr, vnff__zpr)
                    if khj__tezx:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(rzgag__kftq,
                                vnff__zpr)
                        else:
                            rzgag__kftq[vnff__zpr] = op(other, fill_value)
                    else:
                        rzgag__kftq[vnff__zpr] = op(other, arr[vnff__zpr])
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        ipnda__hldiv = edn__msgec.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType
            ) and ipnda__hldiv == types.Array(types.bool_, 1, 'C'):
            ipnda__hldiv = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pcf__njbs = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            rzgag__kftq = bodo.utils.utils.alloc_type(n, ipnda__hldiv, None)
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                khj__tezx = bodo.libs.array_kernels.isna(arr, vnff__zpr)
                tkz__ynve = bodo.libs.array_kernels.isna(pcf__njbs, vnff__zpr)
                rzgag__kftq[vnff__zpr] = op(pcf__njbs[vnff__zpr], arr[
                    vnff__zpr])
                if khj__tezx and tkz__ynve:
                    bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                elif khj__tezx:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                    else:
                        rzgag__kftq[vnff__zpr] = op(pcf__njbs[vnff__zpr],
                            fill_value)
                elif tkz__ynve:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                    else:
                        rzgag__kftq[vnff__zpr] = op(fill_value, arr[vnff__zpr])
                else:
                    rzgag__kftq[vnff__zpr] = op(pcf__njbs[vnff__zpr], arr[
                        vnff__zpr])
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
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
    for op, lrfv__iba in explicit_binop_funcs_two_ways.items():
        for name in lrfv__iba:
            breje__grp = create_explicit_binary_op_overload(op)
            dicnb__zwxew = create_explicit_binary_reverse_op_overload(op)
            fxp__ydqb = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(breje__grp)
            overload_method(SeriesType, fxp__ydqb, no_unliteral=True)(
                dicnb__zwxew)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        breje__grp = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(breje__grp)
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
                vllt__vipd = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                rzgag__kftq = dt64_arr_sub(arr, vllt__vipd)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
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
                rzgag__kftq = np.empty(n, np.dtype('datetime64[ns]'))
                for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, vnff__zpr):
                        bodo.libs.array_kernels.setna(rzgag__kftq, vnff__zpr)
                        continue
                    ldb__vdnsm = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[vnff__zpr]))
                    nmqlu__uru = op(ldb__vdnsm, rhs)
                    rzgag__kftq[vnff__zpr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        nmqlu__uru.value)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
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
                    vllt__vipd = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    rzgag__kftq = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(vllt__vipd))
                    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vllt__vipd = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                rzgag__kftq = op(arr, vllt__vipd)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    axvqm__gflgh = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    rzgag__kftq = op(bodo.utils.conversion.
                        unbox_if_timestamp(axvqm__gflgh), arr)
                    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                axvqm__gflgh = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                rzgag__kftq = op(axvqm__gflgh, arr)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        breje__grp = create_binary_op_overload(op)
        overload(op)(breje__grp)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    owrux__ksog = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, owrux__ksog)
        for vnff__zpr in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, vnff__zpr
                ) or bodo.libs.array_kernels.isna(arg2, vnff__zpr):
                bodo.libs.array_kernels.setna(S, vnff__zpr)
                continue
            S[vnff__zpr
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                vnff__zpr]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[vnff__zpr]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                pcf__njbs = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, pcf__njbs)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        breje__grp = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(breje__grp)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                rzgag__kftq = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        breje__grp = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(breje__grp)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    rzgag__kftq = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
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
                    pcf__njbs = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    rzgag__kftq = ufunc(arr, pcf__njbs)
                    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    pcf__njbs = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    rzgag__kftq = ufunc(arr, pcf__njbs)
                    return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        breje__grp = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(breje__grp)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        tbm__ndzo = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        ycpac__dkuo = np.arange(n),
        bodo.libs.timsort.sort(tbm__ndzo, 0, n, ycpac__dkuo)
        return ycpac__dkuo[0]
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
        lnfcj__ppd = get_overload_const_str(downcast)
        if lnfcj__ppd in ('integer', 'signed'):
            out_dtype = types.int64
        elif lnfcj__ppd == 'unsigned':
            out_dtype = types.uint64
        else:
            assert lnfcj__ppd == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            wce__dzsoa = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            rzgag__kftq = pd.to_numeric(wce__dzsoa, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            thwc__iwqgq = np.empty(n, np.float64)
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, vnff__zpr):
                    bodo.libs.array_kernels.setna(thwc__iwqgq, vnff__zpr)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(thwc__iwqgq,
                        vnff__zpr, arg_a, vnff__zpr)
            return thwc__iwqgq
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            thwc__iwqgq = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for vnff__zpr in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, vnff__zpr):
                    bodo.libs.array_kernels.setna(thwc__iwqgq, vnff__zpr)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(thwc__iwqgq,
                        vnff__zpr, arg_a, vnff__zpr)
            return thwc__iwqgq
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        dnqnu__hbg = if_series_to_array_type(args[0])
        if isinstance(dnqnu__hbg, types.Array) and isinstance(dnqnu__hbg.
            dtype, types.Integer):
            dnqnu__hbg = types.Array(types.float64, 1, 'C')
        return dnqnu__hbg(*args)


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
    hlh__omm = bodo.utils.utils.is_array_typ(x, True)
    czdu__zosd = bodo.utils.utils.is_array_typ(y, True)
    uletk__mwfb = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        uletk__mwfb += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if hlh__omm and not bodo.utils.utils.is_array_typ(x, False):
        uletk__mwfb += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if czdu__zosd and not bodo.utils.utils.is_array_typ(y, False):
        uletk__mwfb += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    uletk__mwfb += '  n = len(condition)\n'
    wxwqg__ukt = x.dtype if hlh__omm else types.unliteral(x)
    hvct__hdbjr = y.dtype if czdu__zosd else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        wxwqg__ukt = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        hvct__hdbjr = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    mhki__pxk = get_data(x)
    qgx__ziox = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(ycpac__dkuo) for
        ycpac__dkuo in [mhki__pxk, qgx__ziox])
    if qgx__ziox == types.none:
        if isinstance(wxwqg__ukt, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif mhki__pxk == qgx__ziox and not is_nullable:
        out_dtype = dtype_to_array_type(wxwqg__ukt)
    elif wxwqg__ukt == string_type or hvct__hdbjr == string_type:
        out_dtype = bodo.string_array_type
    elif mhki__pxk == bytes_type or (hlh__omm and wxwqg__ukt == bytes_type
        ) and (qgx__ziox == bytes_type or czdu__zosd and hvct__hdbjr ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(wxwqg__ukt, bodo.PDCategoricalDtype):
        out_dtype = None
    elif wxwqg__ukt in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(wxwqg__ukt, 1, 'C')
    elif hvct__hdbjr in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(hvct__hdbjr, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(wxwqg__ukt), numba.np.numpy_support.
            as_dtype(hvct__hdbjr)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(wxwqg__ukt, bodo.PDCategoricalDtype):
        mxnob__xjkz = 'x'
    else:
        mxnob__xjkz = 'out_dtype'
    uletk__mwfb += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {mxnob__xjkz}, (-1,))\n')
    if isinstance(wxwqg__ukt, bodo.PDCategoricalDtype):
        uletk__mwfb += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        uletk__mwfb += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    uletk__mwfb += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    uletk__mwfb += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if hlh__omm:
        uletk__mwfb += '      if bodo.libs.array_kernels.isna(x, j):\n'
        uletk__mwfb += '        setna(out_arr, j)\n'
        uletk__mwfb += '        continue\n'
    if isinstance(wxwqg__ukt, bodo.PDCategoricalDtype):
        uletk__mwfb += '      out_codes[j] = x_codes[j]\n'
    else:
        uletk__mwfb += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if hlh__omm else 'x'))
    uletk__mwfb += '    else:\n'
    if czdu__zosd:
        uletk__mwfb += '      if bodo.libs.array_kernels.isna(y, j):\n'
        uletk__mwfb += '        setna(out_arr, j)\n'
        uletk__mwfb += '        continue\n'
    if qgx__ziox == types.none:
        if isinstance(wxwqg__ukt, bodo.PDCategoricalDtype):
            uletk__mwfb += '      out_codes[j] = -1\n'
        else:
            uletk__mwfb += '      setna(out_arr, j)\n'
    else:
        uletk__mwfb += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if czdu__zosd else 'y'))
    uletk__mwfb += '  return out_arr\n'
    pjg__uypv = {}
    exec(uletk__mwfb, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, pjg__uypv)
    lcz__pcy = pjg__uypv['_impl']
    return lcz__pcy


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
        lgaq__tvq = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(lgaq__tvq, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(lgaq__tvq):
            qzp__uhui = lgaq__tvq.data.dtype
        else:
            qzp__uhui = lgaq__tvq.dtype
        if isinstance(qzp__uhui, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        wrcpx__yyhhr = lgaq__tvq
    else:
        vpmh__kqbxp = []
        for lgaq__tvq in choicelist:
            if not bodo.utils.utils.is_array_typ(lgaq__tvq, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(lgaq__tvq):
                qzp__uhui = lgaq__tvq.data.dtype
            else:
                qzp__uhui = lgaq__tvq.dtype
            if isinstance(qzp__uhui, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            vpmh__kqbxp.append(qzp__uhui)
        if not is_common_scalar_dtype(vpmh__kqbxp):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        wrcpx__yyhhr = choicelist[0]
    if is_series_type(wrcpx__yyhhr):
        wrcpx__yyhhr = wrcpx__yyhhr.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, wrcpx__yyhhr.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(wrcpx__yyhhr, types.Array) or isinstance(
        wrcpx__yyhhr, BooleanArrayType) or isinstance(wrcpx__yyhhr,
        IntegerArrayType) or bodo.utils.utils.is_array_typ(wrcpx__yyhhr, 
        False) and wrcpx__yyhhr.dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {wrcpx__yyhhr} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    jrybw__kevt = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        cbbw__rij = choicelist.dtype
    else:
        yjnk__pvli = False
        vpmh__kqbxp = []
        for lgaq__tvq in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lgaq__tvq
                , 'numpy.select()')
            if is_nullable_type(lgaq__tvq):
                yjnk__pvli = True
            if is_series_type(lgaq__tvq):
                qzp__uhui = lgaq__tvq.data.dtype
            else:
                qzp__uhui = lgaq__tvq.dtype
            if isinstance(qzp__uhui, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            vpmh__kqbxp.append(qzp__uhui)
        qysn__dbcbs, rugxp__kvyut = get_common_scalar_dtype(vpmh__kqbxp)
        if not rugxp__kvyut:
            raise BodoError('Internal error in overload_np_select')
        gfk__zza = dtype_to_array_type(qysn__dbcbs)
        if yjnk__pvli:
            gfk__zza = to_nullable_type(gfk__zza)
        cbbw__rij = gfk__zza
    if isinstance(cbbw__rij, SeriesType):
        cbbw__rij = cbbw__rij.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        vpcv__aqre = True
    else:
        vpcv__aqre = False
    glxy__uke = False
    mvyw__ssu = False
    if vpcv__aqre:
        if isinstance(cbbw__rij.dtype, types.Number):
            pass
        elif cbbw__rij.dtype == types.bool_:
            mvyw__ssu = True
        else:
            glxy__uke = True
            cbbw__rij = to_nullable_type(cbbw__rij)
    elif default == types.none or is_overload_constant_nan(default):
        glxy__uke = True
        cbbw__rij = to_nullable_type(cbbw__rij)
    uletk__mwfb = 'def np_select_impl(condlist, choicelist, default=0):\n'
    uletk__mwfb += '  if len(condlist) != len(choicelist):\n'
    uletk__mwfb += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    uletk__mwfb += '  output_len = len(choicelist[0])\n'
    uletk__mwfb += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    uletk__mwfb += '  for i in range(output_len):\n'
    if glxy__uke:
        uletk__mwfb += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif mvyw__ssu:
        uletk__mwfb += '    out[i] = False\n'
    else:
        uletk__mwfb += '    out[i] = default\n'
    if jrybw__kevt:
        uletk__mwfb += '  for i in range(len(condlist) - 1, -1, -1):\n'
        uletk__mwfb += '    cond = condlist[i]\n'
        uletk__mwfb += '    choice = choicelist[i]\n'
        uletk__mwfb += '    out = np.where(cond, choice, out)\n'
    else:
        for vnff__zpr in range(len(choicelist) - 1, -1, -1):
            uletk__mwfb += f'  cond = condlist[{vnff__zpr}]\n'
            uletk__mwfb += f'  choice = choicelist[{vnff__zpr}]\n'
            uletk__mwfb += f'  out = np.where(cond, choice, out)\n'
    uletk__mwfb += '  return out'
    pjg__uypv = dict()
    exec(uletk__mwfb, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': cbbw__rij}, pjg__uypv)
    impl = pjg__uypv['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rzgag__kftq = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    huocx__fpfe = dict(subset=subset, keep=keep, inplace=inplace)
    xjsx__fyodi = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', huocx__fpfe,
        xjsx__fyodi, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        rcgsb__jqqjk = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (rcgsb__jqqjk,
            ), mnqbk__yyqvi = bodo.libs.array_kernels.drop_duplicates((
            rcgsb__jqqjk,), index, 1)
        index = bodo.utils.conversion.index_from_array(mnqbk__yyqvi)
        return bodo.hiframes.pd_series_ext.init_series(rcgsb__jqqjk, index,
            name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    dxn__oqn = element_type(S.data)
    if not is_common_scalar_dtype([dxn__oqn, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([dxn__oqn, right]):
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
        rzgag__kftq = np.empty(n, np.bool_)
        for vnff__zpr in numba.parfors.parfor.internal_prange(n):
            qfp__iffc = bodo.utils.conversion.box_if_dt64(arr[vnff__zpr])
            if inclusive == 'both':
                rzgag__kftq[vnff__zpr
                    ] = qfp__iffc <= right and qfp__iffc >= left
            else:
                rzgag__kftq[vnff__zpr] = qfp__iffc < right and qfp__iffc > left
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    huocx__fpfe = dict(axis=axis)
    xjsx__fyodi = dict(axis=None)
    check_unsupported_args('Series.repeat', huocx__fpfe, xjsx__fyodi,
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
            mnqbk__yyqvi = bodo.utils.conversion.index_to_array(index)
            rzgag__kftq = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            ogml__tuo = bodo.libs.array_kernels.repeat_kernel(mnqbk__yyqvi,
                repeats)
            pcqf__cip = bodo.utils.conversion.index_from_array(ogml__tuo)
            return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
                pcqf__cip, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mnqbk__yyqvi = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        rzgag__kftq = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        ogml__tuo = bodo.libs.array_kernels.repeat_kernel(mnqbk__yyqvi, repeats
            )
        pcqf__cip = bodo.utils.conversion.index_from_array(ogml__tuo)
        return bodo.hiframes.pd_series_ext.init_series(rzgag__kftq,
            pcqf__cip, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        ycpac__dkuo = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(ycpac__dkuo)
        obr__shs = {}
        for vnff__zpr in range(n):
            qfp__iffc = bodo.utils.conversion.box_if_dt64(ycpac__dkuo[
                vnff__zpr])
            obr__shs[index[vnff__zpr]] = qfp__iffc
        return obr__shs
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    dlyu__ebn = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            kmzl__frnzr = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(dlyu__ebn)
    elif is_literal_type(name):
        kmzl__frnzr = get_literal_value(name)
    else:
        raise_bodo_error(dlyu__ebn)
    kmzl__frnzr = 0 if kmzl__frnzr is None else kmzl__frnzr

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (kmzl__frnzr,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
