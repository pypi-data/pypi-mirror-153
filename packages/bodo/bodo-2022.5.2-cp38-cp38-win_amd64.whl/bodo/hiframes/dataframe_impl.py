"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array, boolean_dtype
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        jsen__qrnd = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({jsen__qrnd})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    rqw__ecpp = 'def impl(df):\n'
    if df.has_runtime_cols:
        rqw__ecpp += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        ivekj__uhh = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        rqw__ecpp += f'  return {ivekj__uhh}'
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    omeqh__snl = len(df.columns)
    lwu__nde = set(i for i in range(omeqh__snl) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in lwu__nde else '') for i in range
        (omeqh__snl))
    rqw__ecpp = 'def f(df):\n'.format()
    rqw__ecpp += '    return np.stack(({},), 1)\n'.format(data_args)
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'np': np}, mxq__gvh)
    cgcb__scv = mxq__gvh['f']
    return cgcb__scv


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    exzj__gkdr = {'dtype': dtype, 'na_value': na_value}
    sap__zvwdo = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', exzj__gkdr, sap__zvwdo,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            czsqs__ovof = bodo.hiframes.table.compute_num_runtime_columns(t)
            return czsqs__ovof * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            czsqs__ovof = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), czsqs__ovof
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    rqw__ecpp = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    cynia__zfj = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    rqw__ecpp += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{cynia__zfj}), {index}, None)
"""
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.astype()')
    exzj__gkdr = {'copy': copy, 'errors': errors}
    sap__zvwdo = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', exzj__gkdr, sap__zvwdo,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        bmotp__vajrs = _bodo_object_typeref.instance_type
        assert isinstance(bmotp__vajrs, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        qsob__eteh = {}
        for i, name in enumerate(bmotp__vajrs.columns):
            arr_typ = bmotp__vajrs.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                nglmy__cdr = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                nglmy__cdr = boolean_dtype
            else:
                nglmy__cdr = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = nglmy__cdr
            qsob__eteh[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {qsob__eteh[zxa__pxxj]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if zxa__pxxj in qsob__eteh else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, zxa__pxxj in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        ruep__rbm = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(ruep__rbm[zxa__pxxj])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if zxa__pxxj in ruep__rbm else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, zxa__pxxj in enumerate(df.columns))
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    header = 'def impl(df, deep=True):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        out_df_type = df
        ngr__mayk = types.none
        extra_globals = {'output_arr_typ': ngr__mayk}
        if is_overload_false(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if deep else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        encp__dhtgi = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                encp__dhtgi.append(arr + '.copy()')
            elif is_overload_false(deep):
                encp__dhtgi.append(arr)
            else:
                encp__dhtgi.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(encp__dhtgi)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    exzj__gkdr = {'index': index, 'level': level, 'errors': errors}
    sap__zvwdo = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', exzj__gkdr, sap__zvwdo,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        nmq__siubp = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        nmq__siubp = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    ern__cjb = tuple([nmq__siubp.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        out_df_type = df.copy(columns=ern__cjb)
        ngr__mayk = types.none
        extra_globals = {'output_arr_typ': ngr__mayk}
        if is_overload_false(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if copy else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        encp__dhtgi = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                encp__dhtgi.append(arr + '.copy()')
            elif is_overload_false(copy):
                encp__dhtgi.append(arr)
            else:
                encp__dhtgi.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(encp__dhtgi)
    return _gen_init_df(header, ern__cjb, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    myrx__oqbd = not is_overload_none(items)
    gyhhm__gzi = not is_overload_none(like)
    lec__grq = not is_overload_none(regex)
    fvx__pkq = myrx__oqbd ^ gyhhm__gzi ^ lec__grq
    nnc__nvl = not (myrx__oqbd or gyhhm__gzi or lec__grq)
    if nnc__nvl:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not fvx__pkq:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        sesu__vkz = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        sesu__vkz = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert sesu__vkz in {0, 1}
    rqw__ecpp = 'def impl(df, items=None, like=None, regex=None, axis=None):\n'
    if sesu__vkz == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if sesu__vkz == 1:
        wsw__gqnu = []
        fogyb__uyyqw = []
        lntak__ila = []
        if myrx__oqbd:
            if is_overload_constant_list(items):
                are__btnn = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if gyhhm__gzi:
            if is_overload_constant_str(like):
                jfm__due = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if lec__grq:
            if is_overload_constant_str(regex):
                pcs__ozbie = get_overload_const_str(regex)
                ddgk__xfp = re.compile(pcs__ozbie)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, zxa__pxxj in enumerate(df.columns):
            if not is_overload_none(items
                ) and zxa__pxxj in are__btnn or not is_overload_none(like
                ) and jfm__due in str(zxa__pxxj) or not is_overload_none(regex
                ) and ddgk__xfp.search(str(zxa__pxxj)):
                fogyb__uyyqw.append(zxa__pxxj)
                lntak__ila.append(i)
        for i in lntak__ila:
            var_name = f'data_{i}'
            wsw__gqnu.append(var_name)
            rqw__ecpp += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(wsw__gqnu)
        return _gen_init_df(rqw__ecpp, fogyb__uyyqw, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        ngr__mayk = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([ngr__mayk] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ngr__mayk}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    rode__owykw = is_overload_none(include)
    wtjt__kvc = is_overload_none(exclude)
    gsszx__cdxv = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if rode__owykw and wtjt__kvc:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not rode__owykw:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            mcnl__kgy = [dtype_to_array_type(parse_dtype(elem, gsszx__cdxv)
                ) for elem in include]
        elif is_legal_input(include):
            mcnl__kgy = [dtype_to_array_type(parse_dtype(include, gsszx__cdxv))
                ]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        mcnl__kgy = get_nullable_and_non_nullable_types(mcnl__kgy)
        bsw__fdj = tuple(zxa__pxxj for i, zxa__pxxj in enumerate(df.columns
            ) if df.data[i] in mcnl__kgy)
    else:
        bsw__fdj = df.columns
    if not wtjt__kvc:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            hibem__dbasb = [dtype_to_array_type(parse_dtype(elem,
                gsszx__cdxv)) for elem in exclude]
        elif is_legal_input(exclude):
            hibem__dbasb = [dtype_to_array_type(parse_dtype(exclude,
                gsszx__cdxv))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        hibem__dbasb = get_nullable_and_non_nullable_types(hibem__dbasb)
        bsw__fdj = tuple(zxa__pxxj for zxa__pxxj in bsw__fdj if df.data[df.
            column_index[zxa__pxxj]] not in hibem__dbasb)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[zxa__pxxj]})'
         for zxa__pxxj in bsw__fdj)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, bsw__fdj, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        ngr__mayk = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([ngr__mayk] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ngr__mayk}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


def overload_dataframe_head(df, n=5):
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    xjoe__oey = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in xjoe__oey:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    xjoe__oey = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in xjoe__oey:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    rqw__ecpp = 'def impl(df, values):\n'
    nqdbh__bsyhm = {}
    xyvjk__nyqhg = False
    if isinstance(values, DataFrameType):
        xyvjk__nyqhg = True
        for i, zxa__pxxj in enumerate(df.columns):
            if zxa__pxxj in values.column_index:
                vea__pglhb = 'val{}'.format(i)
                rqw__ecpp += f"""  {vea__pglhb} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[zxa__pxxj]})
"""
                nqdbh__bsyhm[zxa__pxxj] = vea__pglhb
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        nqdbh__bsyhm = {zxa__pxxj: 'values' for zxa__pxxj in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        vea__pglhb = 'data{}'.format(i)
        rqw__ecpp += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(vea__pglhb, i))
        data.append(vea__pglhb)
    cqdnu__uxkm = ['out{}'.format(i) for i in range(len(df.columns))]
    hex__vzvks = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    uafby__uuo = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    nskle__oind = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, nhab__iiuyf) in enumerate(zip(df.columns, data)):
        if cname in nqdbh__bsyhm:
            qodpe__efkj = nqdbh__bsyhm[cname]
            if xyvjk__nyqhg:
                rqw__ecpp += hex__vzvks.format(nhab__iiuyf, qodpe__efkj,
                    cqdnu__uxkm[i])
            else:
                rqw__ecpp += uafby__uuo.format(nhab__iiuyf, qodpe__efkj,
                    cqdnu__uxkm[i])
        else:
            rqw__ecpp += nskle__oind.format(cqdnu__uxkm[i])
    return _gen_init_df(rqw__ecpp, df.columns, ','.join(cqdnu__uxkm))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    omeqh__snl = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(omeqh__snl))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    xhgu__afs = [zxa__pxxj for zxa__pxxj, alk__otpml in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(alk__otpml.dtype)]
    assert len(xhgu__afs) != 0
    tbjjo__eyl = ''
    if not any(alk__otpml == types.float64 for alk__otpml in df.data):
        tbjjo__eyl = '.astype(np.float64)'
    zic__lpe = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[zxa__pxxj], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[zxa__pxxj]], IntegerArrayType) or
        df.data[df.column_index[zxa__pxxj]] == boolean_array else '') for
        zxa__pxxj in xhgu__afs)
    jeny__hhr = 'np.stack(({},), 1){}'.format(zic__lpe, tbjjo__eyl)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(xhgu__afs)))
    index = f'{generate_col_to_index_func_text(xhgu__afs)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(jeny__hhr)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, xhgu__afs, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    jsbfw__hzoll = dict(ddof=ddof)
    rhzam__bztnu = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    cpfur__eggf = '1' if is_overload_none(min_periods) else 'min_periods'
    xhgu__afs = [zxa__pxxj for zxa__pxxj, alk__otpml in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(alk__otpml.dtype)]
    if len(xhgu__afs) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    tbjjo__eyl = ''
    if not any(alk__otpml == types.float64 for alk__otpml in df.data):
        tbjjo__eyl = '.astype(np.float64)'
    zic__lpe = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[zxa__pxxj], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[zxa__pxxj]], IntegerArrayType) or
        df.data[df.column_index[zxa__pxxj]] == boolean_array else '') for
        zxa__pxxj in xhgu__afs)
    jeny__hhr = 'np.stack(({},), 1){}'.format(zic__lpe, tbjjo__eyl)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(xhgu__afs)))
    index = f'pd.Index({xhgu__afs})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(jeny__hhr)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        cpfur__eggf)
    return _gen_init_df(header, xhgu__afs, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    jsbfw__hzoll = dict(axis=axis, level=level, numeric_only=numeric_only)
    rhzam__bztnu = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    rqw__ecpp = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    rqw__ecpp += '  data = np.array([{}])\n'.format(data_args)
    ivekj__uhh = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    rqw__ecpp += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {ivekj__uhh})\n'
        )
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'np': np}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    jsbfw__hzoll = dict(axis=axis)
    rhzam__bztnu = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    rqw__ecpp = 'def impl(df, axis=0, dropna=True):\n'
    rqw__ecpp += '  data = np.asarray(({},))\n'.format(data_args)
    ivekj__uhh = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    rqw__ecpp += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {ivekj__uhh})\n'
        )
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'np': np}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    rhzam__bztnu = dict(skipna=None, level=None, numeric_only=None, min_count=0
        )
    check_unsupported_args('DataFrame.prod', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    rhzam__bztnu = dict(skipna=None, level=None, numeric_only=None, min_count=0
        )
    check_unsupported_args('DataFrame.sum', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rhzam__bztnu = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rhzam__bztnu = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rhzam__bztnu = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, ddof=ddof, numeric_only
        =numeric_only)
    rhzam__bztnu = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, ddof=ddof, numeric_only
        =numeric_only)
    rhzam__bztnu = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    jsbfw__hzoll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rhzam__bztnu = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    jsbfw__hzoll = dict(numeric_only=numeric_only, interpolation=interpolation)
    rhzam__bztnu = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    jsbfw__hzoll = dict(axis=axis, skipna=skipna)
    rhzam__bztnu = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for gglgj__ngvd in df.data:
        if not (bodo.utils.utils.is_np_array_typ(gglgj__ngvd) and (
            gglgj__ngvd.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(gglgj__ngvd.dtype, (types.Number, types.Boolean))) or
            isinstance(gglgj__ngvd, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or gglgj__ngvd in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {gglgj__ngvd} not supported.'
                )
        if isinstance(gglgj__ngvd, bodo.CategoricalArrayType
            ) and not gglgj__ngvd.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    jsbfw__hzoll = dict(axis=axis, skipna=skipna)
    rhzam__bztnu = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for gglgj__ngvd in df.data:
        if not (bodo.utils.utils.is_np_array_typ(gglgj__ngvd) and (
            gglgj__ngvd.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(gglgj__ngvd.dtype, (types.Number, types.Boolean))) or
            isinstance(gglgj__ngvd, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or gglgj__ngvd in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {gglgj__ngvd} not supported.'
                )
        if isinstance(gglgj__ngvd, bodo.CategoricalArrayType
            ) and not gglgj__ngvd.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        xhgu__afs = tuple(zxa__pxxj for zxa__pxxj, alk__otpml in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (alk__otpml.dtype))
        out_colnames = xhgu__afs
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            pep__nby = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[zxa__pxxj]].dtype) for zxa__pxxj in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(pep__nby, []))
    except NotImplementedError as iiix__plkkh:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    xtlpo__jdvs = ''
    if func_name in ('sum', 'prod'):
        xtlpo__jdvs = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    rqw__ecpp = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, xtlpo__jdvs))
    if func_name == 'quantile':
        rqw__ecpp = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        rqw__ecpp = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        rqw__ecpp += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        rqw__ecpp += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    gfhfx__jgaqj = ''
    if func_name in ('min', 'max'):
        gfhfx__jgaqj = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        gfhfx__jgaqj = ', dtype=np.float32'
    axd__vzd = f'bodo.libs.array_ops.array_op_{func_name}'
    grjbv__zcw = ''
    if func_name in ['sum', 'prod']:
        grjbv__zcw = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        grjbv__zcw = 'index'
    elif func_name == 'quantile':
        grjbv__zcw = 'q'
    elif func_name in ['std', 'var']:
        grjbv__zcw = 'True, ddof'
    elif func_name == 'median':
        grjbv__zcw = 'True'
    data_args = ', '.join(
        f'{axd__vzd}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[zxa__pxxj]}), {grjbv__zcw})'
         for zxa__pxxj in out_colnames)
    rqw__ecpp = ''
    if func_name in ('idxmax', 'idxmin'):
        rqw__ecpp += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        rqw__ecpp += ('  data = bodo.utils.conversion.coerce_to_array(({},))\n'
            .format(data_args))
    else:
        rqw__ecpp += '  data = np.asarray(({},){})\n'.format(data_args,
            gfhfx__jgaqj)
    rqw__ecpp += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return rqw__ecpp


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    xsuo__qehp = [df_type.column_index[zxa__pxxj] for zxa__pxxj in out_colnames
        ]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in xsuo__qehp)
    jalka__vogzi = '\n        '.join(f'row[{i}] = arr_{xsuo__qehp[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    mwz__okv = f'len(arr_{xsuo__qehp[0]})'
    zmwy__lfvr = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in zmwy__lfvr:
        lqww__mjt = zmwy__lfvr[func_name]
        ipv__heo = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        rqw__ecpp = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {mwz__okv}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{ipv__heo})
    for i in numba.parfors.parfor.internal_prange(n):
        {jalka__vogzi}
        A[i] = {lqww__mjt}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return rqw__ecpp
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    jsbfw__hzoll = dict(fill_method=fill_method, limit=limit, freq=freq)
    rhzam__bztnu = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', jsbfw__hzoll,
        rhzam__bztnu, package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    jsbfw__hzoll = dict(axis=axis, skipna=skipna)
    rhzam__bztnu = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    jsbfw__hzoll = dict(skipna=skipna)
    rhzam__bztnu = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    jsbfw__hzoll = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    rhzam__bztnu = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    xhgu__afs = [zxa__pxxj for zxa__pxxj, alk__otpml in zip(df.columns, df.
        data) if _is_describe_type(alk__otpml)]
    if len(xhgu__afs) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    dgtb__ghte = sum(df.data[df.column_index[zxa__pxxj]].dtype == bodo.
        datetime64ns for zxa__pxxj in xhgu__afs)

    def _get_describe(col_ind):
        zhfah__lpbb = df.data[col_ind].dtype == bodo.datetime64ns
        if dgtb__ghte and dgtb__ghte != len(xhgu__afs):
            if zhfah__lpbb:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for zxa__pxxj in xhgu__afs:
        col_ind = df.column_index[zxa__pxxj]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[zxa__pxxj]) for
        zxa__pxxj in xhgu__afs)
    egkxq__sran = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if dgtb__ghte == len(xhgu__afs):
        egkxq__sran = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif dgtb__ghte:
        egkxq__sran = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({egkxq__sran})'
    return _gen_init_df(header, xhgu__afs, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    jsbfw__hzoll = dict(axis=axis, convert=convert, is_copy=is_copy)
    rhzam__bztnu = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    jsbfw__hzoll = dict(freq=freq, axis=axis, fill_value=fill_value)
    rhzam__bztnu = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for onx__ysarh in df.data:
        if not is_supported_shift_array_type(onx__ysarh):
            raise BodoError(
                f'Dataframe.shift() column input type {onx__ysarh.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    jsbfw__hzoll = dict(axis=axis)
    rhzam__bztnu = dict(axis=0)
    check_unsupported_args('DataFrame.diff', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for onx__ysarh in df.data:
        if not (isinstance(onx__ysarh, types.Array) and (isinstance(
            onx__ysarh.dtype, types.Number) or onx__ysarh.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {onx__ysarh.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    xyajf__ogsok = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(xyajf__ogsok)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        siwug__evg = get_overload_const_list(column)
    else:
        siwug__evg = [get_literal_value(column)]
    upia__aollj = [df.column_index[zxa__pxxj] for zxa__pxxj in siwug__evg]
    for i in upia__aollj:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{upia__aollj[0]})\n'
        )
    for i in range(n):
        if i in upia__aollj:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    exzj__gkdr = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    sap__zvwdo = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', exzj__gkdr, sap__zvwdo,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(zxa__pxxj for zxa__pxxj in df.columns if zxa__pxxj !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    exzj__gkdr = {'inplace': inplace}
    sap__zvwdo = {'inplace': False}
    check_unsupported_args('query', exzj__gkdr, sap__zvwdo, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        vajs__rbgcj = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[vajs__rbgcj]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    exzj__gkdr = {'subset': subset, 'keep': keep}
    sap__zvwdo = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', exzj__gkdr, sap__zvwdo,
        package_name='pandas', module_name='DataFrame')
    omeqh__snl = len(df.columns)
    rqw__ecpp = "def impl(df, subset=None, keep='first'):\n"
    for i in range(omeqh__snl):
        rqw__ecpp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    nqg__bww = ', '.join(f'data_{i}' for i in range(omeqh__snl))
    nqg__bww += ',' if omeqh__snl == 1 else ''
    rqw__ecpp += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({nqg__bww}))\n')
    rqw__ecpp += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    rqw__ecpp += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    exzj__gkdr = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    sap__zvwdo = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    zpr__zieyq = []
    if is_overload_constant_list(subset):
        zpr__zieyq = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        zpr__zieyq = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        zpr__zieyq = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    sjns__bxpy = []
    for col_name in zpr__zieyq:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        sjns__bxpy.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', exzj__gkdr,
        sap__zvwdo, package_name='pandas', module_name='DataFrame')
    bygj__tkf = []
    if sjns__bxpy:
        for exkkg__mfyi in sjns__bxpy:
            if isinstance(df.data[exkkg__mfyi], bodo.MapArrayType):
                bygj__tkf.append(df.columns[exkkg__mfyi])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                bygj__tkf.append(col_name)
    if bygj__tkf:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {bygj__tkf} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    omeqh__snl = len(df.columns)
    zgq__dcdts = ['data_{}'.format(i) for i in sjns__bxpy]
    ffn__defgy = ['data_{}'.format(i) for i in range(omeqh__snl) if i not in
        sjns__bxpy]
    if zgq__dcdts:
        ocbn__isr = len(zgq__dcdts)
    else:
        ocbn__isr = omeqh__snl
    pkjpx__tmmad = ', '.join(zgq__dcdts + ffn__defgy)
    data_args = ', '.join('data_{}'.format(i) for i in range(omeqh__snl))
    rqw__ecpp = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(omeqh__snl):
        rqw__ecpp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    rqw__ecpp += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(pkjpx__tmmad, index, ocbn__isr))
    rqw__ecpp += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(rqw__ecpp, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):

                def cond_str(i, gen_all_false):
                    if df.columns[i] in cond.column_index:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {cond.column_index[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            zwf__fft = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                zwf__fft = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                zwf__fft = lambda i: f'other[:,{i}]'
        omeqh__snl = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {zwf__fft(i)})'
             for i in range(omeqh__snl))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        tvr__rvu = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(tvr__rvu)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    jsbfw__hzoll = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    rhzam__bztnu = dict(inplace=False, level=None, errors='raise', try_cast
        =False)
    check_unsupported_args(f'{func_name}', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    omeqh__snl = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        for i in range(omeqh__snl):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other.column_index[df
                    .columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(omeqh__snl):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(omeqh__snl):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None,
    out_df_type=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    if out_df_type is not None:
        extra_globals['out_df_type'] = out_df_type
        zdrwz__eqk = 'out_df_type'
    else:
        zdrwz__eqk = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    rqw__ecpp = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {zdrwz__eqk})
"""
    mxq__gvh = {}
    bmtat__mbev = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    bmtat__mbev.update(extra_globals)
    exec(rqw__ecpp, bmtat__mbev, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        vjs__wpn = pd.Index(lhs.columns)
        yahdq__xmb = pd.Index(rhs.columns)
        cczg__amlk, ybuwj__zqc, sir__ymmam = vjs__wpn.join(yahdq__xmb, how=
            'left' if is_inplace else 'outer', level=None, return_indexers=True
            )
        return tuple(cczg__amlk), ybuwj__zqc, sir__ymmam
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        szqok__pxf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        vug__ozwi = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, szqok__pxf)
        check_runtime_cols_unsupported(rhs, szqok__pxf)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                cczg__amlk, ybuwj__zqc, sir__ymmam = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {ocwx__efcto}) {szqok__pxf}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {rie__gtd})'
                     if ocwx__efcto != -1 and rie__gtd != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for ocwx__efcto, rie__gtd in zip(ybuwj__zqc, sir__ymmam))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, cczg__amlk, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            ouwd__dgkpv = []
            xxk__vcvq = []
            if op in vug__ozwi:
                for i, zewo__xygi in enumerate(lhs.data):
                    if is_common_scalar_dtype([zewo__xygi.dtype, rhs]):
                        ouwd__dgkpv.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {szqok__pxf} rhs'
                            )
                    else:
                        ltxa__zlen = f'arr{i}'
                        xxk__vcvq.append(ltxa__zlen)
                        ouwd__dgkpv.append(ltxa__zlen)
                data_args = ', '.join(ouwd__dgkpv)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {szqok__pxf} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(xxk__vcvq) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {ltxa__zlen} = np.empty(n, dtype=np.bool_)\n' for
                    ltxa__zlen in xxk__vcvq)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(ltxa__zlen, 
                    op == operator.ne) for ltxa__zlen in xxk__vcvq)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            ouwd__dgkpv = []
            xxk__vcvq = []
            if op in vug__ozwi:
                for i, zewo__xygi in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, zewo__xygi.dtype]):
                        ouwd__dgkpv.append(
                            f'lhs {szqok__pxf} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        ltxa__zlen = f'arr{i}'
                        xxk__vcvq.append(ltxa__zlen)
                        ouwd__dgkpv.append(ltxa__zlen)
                data_args = ', '.join(ouwd__dgkpv)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, szqok__pxf) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(xxk__vcvq) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(ltxa__zlen) for ltxa__zlen in xxk__vcvq)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(ltxa__zlen, 
                    op == operator.ne) for ltxa__zlen in xxk__vcvq)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        tvr__rvu = create_binary_op_overload(op)
        overload(op)(tvr__rvu)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        szqok__pxf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, szqok__pxf)
        check_runtime_cols_unsupported(right, szqok__pxf)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                cczg__amlk, _, sir__ymmam = _get_binop_columns(left, right,
                    True)
                rqw__ecpp = 'def impl(left, right):\n'
                for i, rie__gtd in enumerate(sir__ymmam):
                    if rie__gtd == -1:
                        rqw__ecpp += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    rqw__ecpp += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    rqw__ecpp += f"""  df_arr{i} {szqok__pxf} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {rie__gtd})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    cczg__amlk)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(rqw__ecpp, cczg__amlk, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            rqw__ecpp = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                rqw__ecpp += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                rqw__ecpp += '  df_arr{0} {1} right\n'.format(i, szqok__pxf)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(rqw__ecpp, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        tvr__rvu = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(tvr__rvu)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            szqok__pxf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, szqok__pxf)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, szqok__pxf) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        tvr__rvu = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(tvr__rvu)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            mjk__odz = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                mjk__odz[i] = bodo.libs.array_kernels.isna(obj, i)
            return mjk__odz
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            mjk__odz = np.empty(n, np.bool_)
            for i in range(n):
                mjk__odz[i] = pd.isna(obj[i])
            return mjk__odz
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    exzj__gkdr = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    sap__zvwdo = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', exzj__gkdr, sap__zvwdo, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    dfjrf__rzsyz = str(expr_node)
    return dfjrf__rzsyz.startswith('left.') or dfjrf__rzsyz.startswith('right.'
        )


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    dtu__hwqt = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (dtu__hwqt,))
    kgcs__alq = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        ovlx__ouuvu = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        wwbik__whtkg = {('NOT_NA', kgcs__alq(zewo__xygi)): zewo__xygi for
            zewo__xygi in null_set}
        aou__tdkl, _, _ = _parse_query_expr(ovlx__ouuvu, env, [], [], None,
            join_cleaned_cols=wwbik__whtkg)
        ipj__fviqg = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            rhako__ppeph = pd.core.computation.ops.BinOp('&', aou__tdkl,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = ipj__fviqg
        return rhako__ppeph

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                vew__dbxfv = set()
                qszf__ugm = set()
                pbqt__agfun = _insert_NA_cond_body(expr_node.lhs, vew__dbxfv)
                vqry__acwq = _insert_NA_cond_body(expr_node.rhs, qszf__ugm)
                lcfk__xntdq = vew__dbxfv.intersection(qszf__ugm)
                vew__dbxfv.difference_update(lcfk__xntdq)
                qszf__ugm.difference_update(lcfk__xntdq)
                null_set.update(lcfk__xntdq)
                expr_node.lhs = append_null_checks(pbqt__agfun, vew__dbxfv)
                expr_node.rhs = append_null_checks(vqry__acwq, qszf__ugm)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            xvsq__ywmn = expr_node.name
            shw__dvd, col_name = xvsq__ywmn.split('.')
            if shw__dvd == 'left':
                bvptu__kyd = left_columns
                data = left_data
            else:
                bvptu__kyd = right_columns
                data = right_data
            dkhth__hgsln = data[bvptu__kyd.index(col_name)]
            if bodo.utils.typing.is_nullable(dkhth__hgsln):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    ricsh__kem = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        xpsag__dllc = str(expr_node.lhs)
        ovwzf__yrbay = str(expr_node.rhs)
        if xpsag__dllc.startswith('left.') and ovwzf__yrbay.startswith('left.'
            ) or xpsag__dllc.startswith('right.') and ovwzf__yrbay.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [xpsag__dllc.split('.')[1]]
        right_on = [ovwzf__yrbay.split('.')[1]]
        if xpsag__dllc.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        vqt__wqixt, bbq__vxf, mpc__lkc = _extract_equal_conds(expr_node.lhs)
        yorkk__weawj, tjkx__foi, jai__cmyf = _extract_equal_conds(expr_node.rhs
            )
        left_on = vqt__wqixt + yorkk__weawj
        right_on = bbq__vxf + tjkx__foi
        if mpc__lkc is None:
            return left_on, right_on, jai__cmyf
        if jai__cmyf is None:
            return left_on, right_on, mpc__lkc
        expr_node.lhs = mpc__lkc
        expr_node.rhs = jai__cmyf
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    dtu__hwqt = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (dtu__hwqt,))
    nmq__siubp = dict()
    kgcs__alq = pd.core.computation.parsing.clean_column_name
    for name, qvzxy__wdw in (('left', left_columns), ('right', right_columns)):
        for zewo__xygi in qvzxy__wdw:
            uuhao__ecaf = kgcs__alq(zewo__xygi)
            vai__kua = name, uuhao__ecaf
            if vai__kua in nmq__siubp:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{zewo__xygi}' and '{nmq__siubp[uuhao__ecaf]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            nmq__siubp[vai__kua] = zewo__xygi
    prf__fnij, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=nmq__siubp)
    left_on, right_on, krrlv__xtl = _extract_equal_conds(prf__fnij.terms)
    return left_on, right_on, _insert_NA_cond(krrlv__xtl, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    jsbfw__hzoll = dict(sort=sort, copy=copy, validate=validate)
    rhzam__bztnu = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    odl__qqme = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    rjj__imd = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in odl__qqme and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, muj__uer = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if muj__uer is None:
                    rjj__imd = ''
                else:
                    rjj__imd = str(muj__uer)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = odl__qqme
        right_keys = odl__qqme
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    hitp__enof = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        lrkuw__vbn = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        lrkuw__vbn = list(get_overload_const_list(suffixes))
    suffix_x = lrkuw__vbn[0]
    suffix_y = lrkuw__vbn[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    rqw__ecpp = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    rqw__ecpp += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    rqw__ecpp += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    rqw__ecpp += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, hitp__enof, rjj__imd))
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo}, mxq__gvh)
    _impl = mxq__gvh['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, DecimalArrayType, IntervalArrayType, bodo.
        DatetimeArrayType)
    xavn__bwryg = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    xvgfn__aby = {get_overload_const_str(isnmw__fjdut) for isnmw__fjdut in
        (left_on, right_on, on) if is_overload_constant_str(isnmw__fjdut)}
    for df in (left, right):
        for i, zewo__xygi in enumerate(df.data):
            if not isinstance(zewo__xygi, valid_dataframe_column_types
                ) and zewo__xygi not in xavn__bwryg:
                raise BodoError(
                    f'{name_func}(): use of column with {type(zewo__xygi)} in merge unsupported'
                    )
            if df.columns[i] in xvgfn__aby and isinstance(zewo__xygi,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        lrkuw__vbn = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        lrkuw__vbn = list(get_overload_const_list(suffixes))
    if len(lrkuw__vbn) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    odl__qqme = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        bfyyq__zfe = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            bfyyq__zfe = on_str not in odl__qqme and ('left.' in on_str or 
                'right.' in on_str)
        if len(odl__qqme) == 0 and not bfyyq__zfe:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    iakjw__get = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            wlub__ihse = left.index
            rmxi__pdjt = isinstance(wlub__ihse, StringIndexType)
            tjyb__eyknv = right.index
            ixr__ihp = isinstance(tjyb__eyknv, StringIndexType)
        elif is_overload_true(left_index):
            wlub__ihse = left.index
            rmxi__pdjt = isinstance(wlub__ihse, StringIndexType)
            tjyb__eyknv = right.data[right.columns.index(right_keys[0])]
            ixr__ihp = tjyb__eyknv.dtype == string_type
        elif is_overload_true(right_index):
            wlub__ihse = left.data[left.columns.index(left_keys[0])]
            rmxi__pdjt = wlub__ihse.dtype == string_type
            tjyb__eyknv = right.index
            ixr__ihp = isinstance(tjyb__eyknv, StringIndexType)
        if rmxi__pdjt and ixr__ihp:
            return
        wlub__ihse = wlub__ihse.dtype
        tjyb__eyknv = tjyb__eyknv.dtype
        try:
            jrh__qhfm = iakjw__get.resolve_function_type(operator.eq, (
                wlub__ihse, tjyb__eyknv), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=wlub__ihse, rk_dtype=tjyb__eyknv))
    else:
        for pgxm__ceep, gdad__ikzng in zip(left_keys, right_keys):
            wlub__ihse = left.data[left.columns.index(pgxm__ceep)].dtype
            jfjm__gayfk = left.data[left.columns.index(pgxm__ceep)]
            tjyb__eyknv = right.data[right.columns.index(gdad__ikzng)].dtype
            rnttb__ctbb = right.data[right.columns.index(gdad__ikzng)]
            if jfjm__gayfk == rnttb__ctbb:
                continue
            czp__uouh = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=pgxm__ceep, lk_dtype=wlub__ihse, rk=gdad__ikzng,
                rk_dtype=tjyb__eyknv))
            jpmth__ehum = wlub__ihse == string_type
            yycdc__iqw = tjyb__eyknv == string_type
            if jpmth__ehum ^ yycdc__iqw:
                raise_bodo_error(czp__uouh)
            try:
                jrh__qhfm = iakjw__get.resolve_function_type(operator.eq, (
                    wlub__ihse, tjyb__eyknv), {})
            except:
                raise_bodo_error(czp__uouh)


def validate_keys(keys, df):
    brn__gfdf = set(keys).difference(set(df.columns))
    if len(brn__gfdf) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in brn__gfdf:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {brn__gfdf} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    jsbfw__hzoll = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    rhzam__bztnu = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    rqw__ecpp = "def _impl(left, other, on=None, how='left',\n"
    rqw__ecpp += "    lsuffix='', rsuffix='', sort=False):\n"
    rqw__ecpp += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo}, mxq__gvh)
    _impl = mxq__gvh['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        kqt__pkhnq = get_overload_const_list(on)
        validate_keys(kqt__pkhnq, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    odl__qqme = tuple(set(left.columns) & set(other.columns))
    if len(odl__qqme) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=odl__qqme))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    vlrn__bvn = set(left_keys) & set(right_keys)
    serf__woez = set(left_columns) & set(right_columns)
    xsn__ywfqw = serf__woez - vlrn__bvn
    winre__oalk = set(left_columns) - serf__woez
    mbilp__pab = set(right_columns) - serf__woez
    jhz__gzu = {}

    def insertOutColumn(col_name):
        if col_name in jhz__gzu:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        jhz__gzu[col_name] = 0
    for yjc__lwiku in vlrn__bvn:
        insertOutColumn(yjc__lwiku)
    for yjc__lwiku in xsn__ywfqw:
        bhj__qwlq = str(yjc__lwiku) + suffix_x
        uqhnr__vyzv = str(yjc__lwiku) + suffix_y
        insertOutColumn(bhj__qwlq)
        insertOutColumn(uqhnr__vyzv)
    for yjc__lwiku in winre__oalk:
        insertOutColumn(yjc__lwiku)
    for yjc__lwiku in mbilp__pab:
        insertOutColumn(yjc__lwiku)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    odl__qqme = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = odl__qqme
        right_keys = odl__qqme
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        lrkuw__vbn = suffixes
    if is_overload_constant_list(suffixes):
        lrkuw__vbn = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        lrkuw__vbn = suffixes.value
    suffix_x = lrkuw__vbn[0]
    suffix_y = lrkuw__vbn[1]
    rqw__ecpp = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    rqw__ecpp += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    rqw__ecpp += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    rqw__ecpp += "    allow_exact_matches=True, direction='backward'):\n"
    rqw__ecpp += '  suffix_x = suffixes[0]\n'
    rqw__ecpp += '  suffix_y = suffixes[1]\n'
    rqw__ecpp += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo}, mxq__gvh)
    _impl = mxq__gvh['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    jsbfw__hzoll = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    mvx__ekl = dict(sort=False, group_keys=True, squeeze=False, observed=True)
    check_unsupported_args('Dataframe.groupby', jsbfw__hzoll, mvx__ekl,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    xtxxn__aqwc = func_name == 'DataFrame.pivot_table'
    if xtxxn__aqwc:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    tnkzu__vvb = get_literal_value(columns)
    if isinstance(tnkzu__vvb, (list, tuple)):
        if len(tnkzu__vvb) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {tnkzu__vvb}"
                )
        tnkzu__vvb = tnkzu__vvb[0]
    if tnkzu__vvb not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {tnkzu__vvb} not found in DataFrame {df}."
            )
    acn__kepx = df.column_index[tnkzu__vvb]
    if is_overload_none(index):
        fdtb__arcn = []
        jtf__btf = []
    else:
        jtf__btf = get_literal_value(index)
        if not isinstance(jtf__btf, (list, tuple)):
            jtf__btf = [jtf__btf]
        fdtb__arcn = []
        for index in jtf__btf:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            fdtb__arcn.append(df.column_index[index])
    if not (all(isinstance(zxa__pxxj, int) for zxa__pxxj in jtf__btf) or
        all(isinstance(zxa__pxxj, str) for zxa__pxxj in jtf__btf)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        uwp__swb = []
        aazkv__hxydi = []
        mnv__omgki = fdtb__arcn + [acn__kepx]
        for i, zxa__pxxj in enumerate(df.columns):
            if i not in mnv__omgki:
                uwp__swb.append(i)
                aazkv__hxydi.append(zxa__pxxj)
    else:
        aazkv__hxydi = get_literal_value(values)
        if not isinstance(aazkv__hxydi, (list, tuple)):
            aazkv__hxydi = [aazkv__hxydi]
        uwp__swb = []
        for val in aazkv__hxydi:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            uwp__swb.append(df.column_index[val])
    if all(isinstance(zxa__pxxj, int) for zxa__pxxj in aazkv__hxydi):
        aazkv__hxydi = np.array(aazkv__hxydi, 'int64')
    elif all(isinstance(zxa__pxxj, str) for zxa__pxxj in aazkv__hxydi):
        aazkv__hxydi = pd.array(aazkv__hxydi, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    dft__lcpqp = set(uwp__swb) | set(fdtb__arcn) | {acn__kepx}
    if len(dft__lcpqp) != len(uwp__swb) + len(fdtb__arcn) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(fdtb__arcn) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for jvbu__dxu in fdtb__arcn:
            index_column = df.data[jvbu__dxu]
            check_valid_index_typ(index_column)
    aftis__txcrd = df.data[acn__kepx]
    if isinstance(aftis__txcrd, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(aftis__txcrd, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for ank__jqqjd in uwp__swb:
        ubvho__tbcyj = df.data[ank__jqqjd]
        if isinstance(ubvho__tbcyj, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or ubvho__tbcyj == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return jtf__btf, tnkzu__vvb, aazkv__hxydi, fdtb__arcn, acn__kepx, uwp__swb


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (jtf__btf, tnkzu__vvb, aazkv__hxydi, jvbu__dxu, acn__kepx, djlk__mviey) = (
        pivot_error_checking(data, index, columns, values, 'DataFrame.pivot'))
    if len(jtf__btf) == 0:
        if is_overload_none(data.index.name_typ):
            jtf__btf = [None]
        else:
            jtf__btf = [get_literal_value(data.index.name_typ)]
    if len(aazkv__hxydi) == 1:
        wjcof__wuniw = None
    else:
        wjcof__wuniw = aazkv__hxydi
    rqw__ecpp = 'def impl(data, index=None, columns=None, values=None):\n'
    rqw__ecpp += f'    pivot_values = data.iloc[:, {acn__kepx}].unique()\n'
    rqw__ecpp += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(jvbu__dxu) == 0:
        rqw__ecpp += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        rqw__ecpp += '        (\n'
        for tmwe__odgxx in jvbu__dxu:
            rqw__ecpp += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {tmwe__odgxx}),
"""
        rqw__ecpp += '        ),\n'
    rqw__ecpp += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {acn__kepx}),),
"""
    rqw__ecpp += '        (\n'
    for ank__jqqjd in djlk__mviey:
        rqw__ecpp += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {ank__jqqjd}),
"""
    rqw__ecpp += '        ),\n'
    rqw__ecpp += '        pivot_values,\n'
    rqw__ecpp += '        index_lit_tup,\n'
    rqw__ecpp += '        columns_lit,\n'
    rqw__ecpp += '        values_name_const,\n'
    rqw__ecpp += '    )\n'
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'index_lit_tup': tuple(jtf__btf),
        'columns_lit': tnkzu__vvb, 'values_name_const': wjcof__wuniw}, mxq__gvh
        )
    impl = mxq__gvh['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    jsbfw__hzoll = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed, sort=sort)
    rhzam__bztnu = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', jsbfw__hzoll,
        rhzam__bztnu, package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (jtf__btf, tnkzu__vvb, aazkv__hxydi, jvbu__dxu, acn__kepx, djlk__mviey
            ) = (pivot_error_checking(data, index, columns, values,
            'DataFrame.pivot_table'))
        if len(aazkv__hxydi) == 1:
            wjcof__wuniw = None
        else:
            wjcof__wuniw = aazkv__hxydi
        rqw__ecpp = 'def impl(\n'
        rqw__ecpp += '    data,\n'
        rqw__ecpp += '    values=None,\n'
        rqw__ecpp += '    index=None,\n'
        rqw__ecpp += '    columns=None,\n'
        rqw__ecpp += '    aggfunc="mean",\n'
        rqw__ecpp += '    fill_value=None,\n'
        rqw__ecpp += '    margins=False,\n'
        rqw__ecpp += '    dropna=True,\n'
        rqw__ecpp += '    margins_name="All",\n'
        rqw__ecpp += '    observed=False,\n'
        rqw__ecpp += '    sort=True,\n'
        rqw__ecpp += '    _pivot_values=None,\n'
        rqw__ecpp += '):\n'
        emb__ziu = jvbu__dxu + [acn__kepx] + djlk__mviey
        rqw__ecpp += f'    data = data.iloc[:, {emb__ziu}]\n'
        jagyn__dvr = jtf__btf + [tnkzu__vvb]
        rqw__ecpp += (
            f'    data = data.groupby({jagyn__dvr!r}, as_index=False).agg(aggfunc)\n'
            )
        rqw__ecpp += (
            f'    pivot_values = data.iloc[:, {len(jvbu__dxu)}].unique()\n')
        rqw__ecpp += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
        rqw__ecpp += '        (\n'
        for i in range(0, len(jvbu__dxu)):
            rqw__ecpp += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        rqw__ecpp += '        ),\n'
        rqw__ecpp += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(jvbu__dxu)}),),
"""
        rqw__ecpp += '        (\n'
        for i in range(len(jvbu__dxu) + 1, len(djlk__mviey) + len(jvbu__dxu
            ) + 1):
            rqw__ecpp += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        rqw__ecpp += '        ),\n'
        rqw__ecpp += '        pivot_values,\n'
        rqw__ecpp += '        index_lit_tup,\n'
        rqw__ecpp += '        columns_lit,\n'
        rqw__ecpp += '        values_name_const,\n'
        rqw__ecpp += '        check_duplicates=False,\n'
        rqw__ecpp += '    )\n'
        mxq__gvh = {}
        exec(rqw__ecpp, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(jtf__btf), 'columns_lit': tnkzu__vvb, 'values_name_const':
            wjcof__wuniw}, mxq__gvh)
        impl = mxq__gvh['impl']
        return impl
    if aggfunc == 'mean':

        def _impl(data, values=None, index=None, columns=None, aggfunc=
            'mean', fill_value=None, margins=False, dropna=True,
            margins_name='All', observed=False, sort=True, _pivot_values=None):
            return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data,
                values, index, columns, 'mean', _pivot_values)
        return _impl

    def _impl(data, values=None, index=None, columns=None, aggfunc='mean',
        fill_value=None, margins=False, dropna=True, margins_name='All',
        observed=False, sort=True, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data, values,
            index, columns, aggfunc, _pivot_values)
    return _impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    jsbfw__hzoll = dict(col_level=col_level, ignore_index=ignore_index)
    rhzam__bztnu = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame.")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal.")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal.")
    if not is_overload_none(var_name) and not (is_literal_type(var_name) and
        (is_scalar_type(var_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'var_name', if specified, must be a literal.")
    if value_name != 'value' and not (is_literal_type(value_name) and (
        is_scalar_type(value_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'value_name', if specified, must be a literal.")
    var_name = get_literal_value(var_name) if not is_overload_none(var_name
        ) else 'variable'
    value_name = get_literal_value(value_name
        ) if value_name != 'value' else 'value'
    tvf__kao = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(tvf__kao, (list, tuple)):
        tvf__kao = [tvf__kao]
    for zxa__pxxj in tvf__kao:
        if zxa__pxxj not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {zxa__pxxj} not found in {frame}."
                )
    kudm__yhd = [frame.column_index[i] for i in tvf__kao]
    if is_overload_none(value_vars):
        vmqxi__ypekp = []
        bjo__fdbxb = []
        for i, zxa__pxxj in enumerate(frame.columns):
            if i not in kudm__yhd:
                vmqxi__ypekp.append(i)
                bjo__fdbxb.append(zxa__pxxj)
    else:
        bjo__fdbxb = get_literal_value(value_vars)
        if not isinstance(bjo__fdbxb, (list, tuple)):
            bjo__fdbxb = [bjo__fdbxb]
        bjo__fdbxb = [v for v in bjo__fdbxb if v not in tvf__kao]
        if not bjo__fdbxb:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        vmqxi__ypekp = []
        for val in bjo__fdbxb:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            vmqxi__ypekp.append(frame.column_index[val])
    for zxa__pxxj in bjo__fdbxb:
        if zxa__pxxj not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {zxa__pxxj} not found in {frame}."
                )
    if not (all(isinstance(zxa__pxxj, int) for zxa__pxxj in bjo__fdbxb) or
        all(isinstance(zxa__pxxj, str) for zxa__pxxj in bjo__fdbxb)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    sxl__upkak = frame.data[vmqxi__ypekp[0]]
    ffn__lse = [frame.data[i].dtype for i in vmqxi__ypekp]
    vmqxi__ypekp = np.array(vmqxi__ypekp, dtype=np.int64)
    kudm__yhd = np.array(kudm__yhd, dtype=np.int64)
    _, qwofx__uvwb = bodo.utils.typing.get_common_scalar_dtype(ffn__lse)
    if not qwofx__uvwb:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': bjo__fdbxb, 'val_type': sxl__upkak}
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == sxl__upkak.dtype for v in ffn__lse):
        extra_globals['value_idxs'] = vmqxi__ypekp
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(bjo__fdbxb) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {vmqxi__ypekp[0]})
"""
    else:
        fjkmk__vpzsw = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in vmqxi__ypekp)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({fjkmk__vpzsw},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in kudm__yhd:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(bjo__fdbxb)})\n'
            )
    yrkv__kxr = ', '.join(f'out_id{i}' for i in kudm__yhd) + (', ' if len(
        kudm__yhd) > 0 else '')
    data_args = yrkv__kxr + 'var_col, val_col'
    columns = tuple(tvf__kao + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(bjo__fdbxb)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    jsbfw__hzoll = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    rhzam__bztnu = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    jsbfw__hzoll = dict(ignore_index=ignore_index, key=key)
    rhzam__bztnu = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', jsbfw__hzoll,
        rhzam__bztnu, package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    mpv__bcj = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        mpv__bcj.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        utqxv__siu = [get_overload_const_tuple(by)]
    else:
        utqxv__siu = get_overload_const_list(by)
    utqxv__siu = set((k, '') if (k, '') in mpv__bcj else k for k in utqxv__siu)
    if len(utqxv__siu.difference(mpv__bcj)) > 0:
        hlah__yom = list(set(get_overload_const_list(by)).difference(mpv__bcj))
        raise_bodo_error(f'sort_values(): invalid keys {hlah__yom} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        pevrt__shlee = get_overload_const_list(na_position)
        for na_position in pevrt__shlee:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    jsbfw__hzoll = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    rhzam__bztnu = dict(axis=0, level=None, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', jsbfw__hzoll,
        rhzam__bztnu, package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    jsbfw__hzoll = dict(limit=limit, downcast=downcast)
    rhzam__bztnu = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    zibv__hvqsw = not is_overload_none(value)
    wohad__vzpag = not is_overload_none(method)
    if zibv__hvqsw and wohad__vzpag:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not zibv__hvqsw and not wohad__vzpag:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if zibv__hvqsw:
        bumz__pjnx = 'value=value'
    else:
        bumz__pjnx = 'method=method'
    data_args = [(
        f"df['{zxa__pxxj}'].fillna({bumz__pjnx}, inplace=inplace)" if
        isinstance(zxa__pxxj, str) else
        f'df[{zxa__pxxj}].fillna({bumz__pjnx}, inplace=inplace)') for
        zxa__pxxj in df.columns]
    rqw__ecpp = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        rqw__ecpp += '  ' + '  \n'.join(data_args) + '\n'
        mxq__gvh = {}
        exec(rqw__ecpp, {}, mxq__gvh)
        impl = mxq__gvh['impl']
        return impl
    else:
        return _gen_init_df(rqw__ecpp, df.columns, ', '.join(alk__otpml +
            '.values' for alk__otpml in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    jsbfw__hzoll = dict(col_level=col_level, col_fill=col_fill)
    rhzam__bztnu = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', jsbfw__hzoll,
        rhzam__bztnu, package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    rqw__ecpp = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    rqw__ecpp += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        kbq__kvo = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            kbq__kvo)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            rqw__ecpp += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            pvd__cfncn = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = pvd__cfncn + data_args
        else:
            tgktg__gkkaq = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [tgktg__gkkaq] + data_args
    return _gen_init_df(rqw__ecpp, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    tqhwm__chvh = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and tqhwm__chvh == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(tqhwm__chvh))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        kxkv__eduou = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        toog__hay = get_overload_const_list(subset)
        kxkv__eduou = []
        for jly__kqp in toog__hay:
            if jly__kqp not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{jly__kqp}' not in data frame columns {df}"
                    )
            kxkv__eduou.append(df.column_index[jly__kqp])
    omeqh__snl = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(omeqh__snl))
    rqw__ecpp = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(omeqh__snl):
        rqw__ecpp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    rqw__ecpp += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in kxkv__eduou)))
    rqw__ecpp += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(rqw__ecpp, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    jsbfw__hzoll = dict(index=index, level=level, errors=errors)
    rhzam__bztnu = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', jsbfw__hzoll, rhzam__bztnu,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            sdfqc__vva = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            sdfqc__vva = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            sdfqc__vva = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            sdfqc__vva = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for zxa__pxxj in sdfqc__vva:
        if zxa__pxxj not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(zxa__pxxj, df.columns))
    if len(set(sdfqc__vva)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    ern__cjb = tuple(zxa__pxxj for zxa__pxxj in df.columns if zxa__pxxj not in
        sdfqc__vva)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[zxa__pxxj], '.copy()' if not inplace else ''
        ) for zxa__pxxj in ern__cjb)
    rqw__ecpp = 'def impl(df, labels=None, axis=0, index=None, columns=None,\n'
    rqw__ecpp += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(rqw__ecpp, ern__cjb, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    jsbfw__hzoll = dict(random_state=random_state, weights=weights, axis=
        axis, ignore_index=ignore_index)
    lotnx__odtaf = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', jsbfw__hzoll, lotnx__odtaf,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    omeqh__snl = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(omeqh__snl))
    rwzo__wrn = ', '.join('rhs_data_{}'.format(i) for i in range(omeqh__snl))
    rqw__ecpp = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    rqw__ecpp += '  if (frac == 1 or n == len(df)) and not replace:\n'
    rqw__ecpp += '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n'
    for i in range(omeqh__snl):
        rqw__ecpp += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    rqw__ecpp += '  if frac is None:\n'
    rqw__ecpp += '    frac_d = -1.0\n'
    rqw__ecpp += '  else:\n'
    rqw__ecpp += '    frac_d = frac\n'
    rqw__ecpp += '  if n is None:\n'
    rqw__ecpp += '    n_i = 0\n'
    rqw__ecpp += '  else:\n'
    rqw__ecpp += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    rqw__ecpp += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({rwzo__wrn},), {index}, n_i, frac_d, replace)
"""
    rqw__ecpp += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(rqw__ecpp, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    exzj__gkdr = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    sap__zvwdo = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', exzj__gkdr, sap__zvwdo,
        package_name='pandas', module_name='DataFrame')
    aihp__siap = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            impc__gfgog = aihp__siap + '\n'
            impc__gfgog += 'Index: 0 entries\n'
            impc__gfgog += 'Empty DataFrame'
            print(impc__gfgog)
        return _info_impl
    else:
        rqw__ecpp = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        rqw__ecpp += '    ncols = df.shape[1]\n'
        rqw__ecpp += f'    lines = "{aihp__siap}\\n"\n'
        rqw__ecpp += f'    lines += "{df.index}: "\n'
        rqw__ecpp += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            rqw__ecpp += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            rqw__ecpp += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            rqw__ecpp += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        rqw__ecpp += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        rqw__ecpp += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        rqw__ecpp += '    column_width = max(space, 7)\n'
        rqw__ecpp += '    column= "Column"\n'
        rqw__ecpp += '    underl= "------"\n'
        rqw__ecpp += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        rqw__ecpp += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        rqw__ecpp += '    mem_size = 0\n'
        rqw__ecpp += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        rqw__ecpp += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        rqw__ecpp += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        iczf__auorl = dict()
        for i in range(len(df.columns)):
            rqw__ecpp += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            cgly__iznoy = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                cgly__iznoy = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                gcn__hza = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                cgly__iznoy = f'{gcn__hza[:-7]}'
            rqw__ecpp += f'    col_dtype[{i}] = "{cgly__iznoy}"\n'
            if cgly__iznoy in iczf__auorl:
                iczf__auorl[cgly__iznoy] += 1
            else:
                iczf__auorl[cgly__iznoy] = 1
            rqw__ecpp += f'    col_name[{i}] = "{df.columns[i]}"\n'
            rqw__ecpp += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        rqw__ecpp += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        rqw__ecpp += '    for i in column_info:\n'
        rqw__ecpp += "        lines += f'{i}\\n'\n"
        gfwmr__hwufh = ', '.join(f'{k}({iczf__auorl[k]})' for k in sorted(
            iczf__auorl))
        rqw__ecpp += f"    lines += 'dtypes: {gfwmr__hwufh}\\n'\n"
        rqw__ecpp += '    mem_size += df.index.nbytes\n'
        rqw__ecpp += '    total_size = _sizeof_fmt(mem_size)\n'
        rqw__ecpp += "    lines += f'memory usage: {total_size}'\n"
        rqw__ecpp += '    print(lines)\n'
        mxq__gvh = {}
        exec(rqw__ecpp, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo': bodo,
            'np': np}, mxq__gvh)
        _info_impl = mxq__gvh['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    rqw__ecpp = 'def impl(df, index=True, deep=False):\n'
    kprsy__knzt = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    iaj__xrxfp = is_overload_true(index)
    columns = df.columns
    if iaj__xrxfp:
        columns = ('Index',) + columns
    if len(columns) == 0:
        ycphm__eguf = ()
    elif all(isinstance(zxa__pxxj, int) for zxa__pxxj in columns):
        ycphm__eguf = np.array(columns, 'int64')
    elif all(isinstance(zxa__pxxj, str) for zxa__pxxj in columns):
        ycphm__eguf = pd.array(columns, 'string')
    else:
        ycphm__eguf = columns
    if df.is_table_format:
        mgicr__rri = int(iaj__xrxfp)
        czsqs__ovof = len(columns)
        rqw__ecpp += f'  nbytes_arr = np.empty({czsqs__ovof}, np.int64)\n'
        rqw__ecpp += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        rqw__ecpp += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {mgicr__rri})
"""
        if iaj__xrxfp:
            rqw__ecpp += f'  nbytes_arr[0] = {kprsy__knzt}\n'
        rqw__ecpp += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if iaj__xrxfp:
            data = f'{kprsy__knzt},{data}'
        else:
            cynia__zfj = ',' if len(columns) == 1 else ''
            data = f'{data}{cynia__zfj}'
        rqw__ecpp += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        ycphm__eguf}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    xvwe__xrkq = 'read_excel_df{}'.format(next_label())
    setattr(types, xvwe__xrkq, df_type)
    eto__mol = False
    if is_overload_constant_list(parse_dates):
        eto__mol = get_overload_const_list(parse_dates)
    brlu__ufqq = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    rqw__ecpp = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{xvwe__xrkq}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{brlu__ufqq}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={eto__mol},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    mxq__gvh = {}
    exec(rqw__ecpp, globals(), mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as iiix__plkkh:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    rqw__ecpp = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    rqw__ecpp += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    rqw__ecpp += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        rqw__ecpp += '   fig, ax = plt.subplots()\n'
    else:
        rqw__ecpp += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        rqw__ecpp += '   fig.set_figwidth(figsize[0])\n'
        rqw__ecpp += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        rqw__ecpp += '   xlabel = x\n'
    rqw__ecpp += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        rqw__ecpp += '   ylabel = y\n'
    else:
        rqw__ecpp += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        rqw__ecpp += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        rqw__ecpp += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    rqw__ecpp += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            rqw__ecpp += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            eryjf__jukq = get_overload_const_str(x)
            ekgic__wrgd = df.columns.index(eryjf__jukq)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if ekgic__wrgd != i:
                        rqw__ecpp += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            rqw__ecpp += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        rqw__ecpp += '   ax.scatter(df[x], df[y], s=20)\n'
        rqw__ecpp += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        rqw__ecpp += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        rqw__ecpp += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        rqw__ecpp += '   ax.legend()\n'
    rqw__ecpp += '   return ax\n'
    mxq__gvh = {}
    exec(rqw__ecpp, {'bodo': bodo, 'plt': plt}, mxq__gvh)
    impl = mxq__gvh['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for ldpvl__wvvs in df_typ.data:
        if not (isinstance(ldpvl__wvvs, IntegerArrayType) or isinstance(
            ldpvl__wvvs.dtype, types.Number) or ldpvl__wvvs.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        eovv__lbxc = args[0]
        wrqvr__rozq = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        ibnkt__buq = eovv__lbxc
        check_runtime_cols_unsupported(eovv__lbxc, 'set_df_col()')
        if isinstance(eovv__lbxc, DataFrameType):
            index = eovv__lbxc.index
            if len(eovv__lbxc.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(eovv__lbxc.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if wrqvr__rozq in eovv__lbxc.columns:
                ern__cjb = eovv__lbxc.columns
                jqwpu__eimyr = eovv__lbxc.columns.index(wrqvr__rozq)
                fkhan__odqjx = list(eovv__lbxc.data)
                fkhan__odqjx[jqwpu__eimyr] = val
                fkhan__odqjx = tuple(fkhan__odqjx)
            else:
                ern__cjb = eovv__lbxc.columns + (wrqvr__rozq,)
                fkhan__odqjx = eovv__lbxc.data + (val,)
            ibnkt__buq = DataFrameType(fkhan__odqjx, index, ern__cjb,
                eovv__lbxc.dist, eovv__lbxc.is_table_format)
        return ibnkt__buq(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    psq__uqeu = {}

    def _rewrite_membership_op(self, node, left, right):
        zit__swori = node.op
        op = self.visit(zit__swori)
        return op, zit__swori, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    zjcz__gpg = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in zjcz__gpg:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in zjcz__gpg:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        ngdgr__idp = node.attr
        value = node.value
        avsq__ywpv = pd.core.computation.ops.LOCAL_TAG
        if ngdgr__idp in ('str', 'dt'):
            try:
                ewcbq__dve = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as cbsqa__xtgn:
                col_name = cbsqa__xtgn.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            ewcbq__dve = str(self.visit(value))
        vai__kua = ewcbq__dve, ngdgr__idp
        if vai__kua in join_cleaned_cols:
            ngdgr__idp = join_cleaned_cols[vai__kua]
        name = ewcbq__dve + '.' + ngdgr__idp
        if name.startswith(avsq__ywpv):
            name = name[len(avsq__ywpv):]
        if ngdgr__idp in ('str', 'dt'):
            kxqr__vwqp = columns[cleaned_columns.index(ewcbq__dve)]
            psq__uqeu[kxqr__vwqp] = ewcbq__dve
            self.env.scope[name] = 0
            return self.term_type(avsq__ywpv + name, self.env)
        zjcz__gpg.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in zjcz__gpg:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        xgb__eqrtm = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        wrqvr__rozq = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(xgb__eqrtm), wrqvr__rozq))

    def op__str__(self):
        lnazz__oatga = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            trk__enkh)) for trk__enkh in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(lnazz__oatga)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(lnazz__oatga)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(lnazz__oatga))
    btewo__yepwd = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    kvcwb__zaenr = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_evaluate_binop)
    nfh__mkumb = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    gmrlw__euigb = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    lilt__vopur = pd.core.computation.ops.Term.__str__
    wrwa__smjpu = pd.core.computation.ops.MathCall.__str__
    ahgc__rojy = pd.core.computation.ops.Op.__str__
    ipj__fviqg = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        prf__fnij = pd.core.computation.expr.Expr(expr, env=env)
        bej__ilmnt = str(prf__fnij)
    except pd.core.computation.ops.UndefinedVariableError as cbsqa__xtgn:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == cbsqa__xtgn.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {cbsqa__xtgn}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            btewo__yepwd)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            kvcwb__zaenr)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = nfh__mkumb
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = gmrlw__euigb
        pd.core.computation.ops.Term.__str__ = lilt__vopur
        pd.core.computation.ops.MathCall.__str__ = wrwa__smjpu
        pd.core.computation.ops.Op.__str__ = ahgc__rojy
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            ipj__fviqg)
    zknt__eclr = pd.core.computation.parsing.clean_column_name
    psq__uqeu.update({zxa__pxxj: zknt__eclr(zxa__pxxj) for zxa__pxxj in
        columns if zknt__eclr(zxa__pxxj) in prf__fnij.names})
    return prf__fnij, bej__ilmnt, psq__uqeu


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        fvppy__alarl = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(fvppy__alarl))
        bnzx__phhz = namedtuple('Pandas', col_names)
        ruz__oroej = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], bnzx__phhz)
        super(DataFrameTupleIterator, self).__init__(name, ruz__oroej)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        yboeg__ssjrr = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        yboeg__ssjrr = [types.Array(types.int64, 1, 'C')] + yboeg__ssjrr
        tzlxn__nhbyw = DataFrameTupleIterator(col_names, yboeg__ssjrr)
        return tzlxn__nhbyw(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ovvm__jsvz = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            ovvm__jsvz)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    olwvd__nmtb = args[len(args) // 2:]
    xdnvq__sbme = sig.args[len(sig.args) // 2:]
    hrj__clrde = context.make_helper(builder, sig.return_type)
    doav__pngk = context.get_constant(types.intp, 0)
    rbivw__yfh = cgutils.alloca_once_value(builder, doav__pngk)
    hrj__clrde.index = rbivw__yfh
    for i, arr in enumerate(olwvd__nmtb):
        setattr(hrj__clrde, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(olwvd__nmtb, xdnvq__sbme):
        context.nrt.incref(builder, arr_typ, arr)
    res = hrj__clrde._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    xdifd__pcxr, = sig.args
    phd__jypf, = args
    hrj__clrde = context.make_helper(builder, xdifd__pcxr, value=phd__jypf)
    ncyxg__vcet = signature(types.intp, xdifd__pcxr.array_types[1])
    nbcq__dduxb = context.compile_internal(builder, lambda a: len(a),
        ncyxg__vcet, [hrj__clrde.array0])
    index = builder.load(hrj__clrde.index)
    pnps__hjbyi = builder.icmp_signed('<', index, nbcq__dduxb)
    result.set_valid(pnps__hjbyi)
    with builder.if_then(pnps__hjbyi):
        values = [index]
        for i, arr_typ in enumerate(xdifd__pcxr.array_types[1:]):
            gamn__nowqb = getattr(hrj__clrde, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                fooy__xnof = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    fooy__xnof, [gamn__nowqb, index])
            else:
                fooy__xnof = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    fooy__xnof, [gamn__nowqb, index])
            values.append(val)
        value = context.make_tuple(builder, xdifd__pcxr.yield_type, values)
        result.yield_(value)
        gbltg__fvixg = cgutils.increment_index(builder, index)
        builder.store(gbltg__fvixg, hrj__clrde.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    zhm__oue = ir.Assign(rhs, lhs, expr.loc)
    gru__egyjq = lhs
    ogfwy__apbos = []
    tio__hkxea = []
    bjna__bwr = typ.count
    for i in range(bjna__bwr):
        wmep__sxlgu = ir.Var(gru__egyjq.scope, mk_unique_var('{}_size{}'.
            format(gru__egyjq.name, i)), gru__egyjq.loc)
        thdx__yxnp = ir.Expr.static_getitem(lhs, i, None, gru__egyjq.loc)
        self.calltypes[thdx__yxnp] = None
        ogfwy__apbos.append(ir.Assign(thdx__yxnp, wmep__sxlgu, gru__egyjq.loc))
        self._define(equiv_set, wmep__sxlgu, types.intp, thdx__yxnp)
        tio__hkxea.append(wmep__sxlgu)
    ois__fdd = tuple(tio__hkxea)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        ois__fdd, pre=[zhm__oue] + ogfwy__apbos)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
