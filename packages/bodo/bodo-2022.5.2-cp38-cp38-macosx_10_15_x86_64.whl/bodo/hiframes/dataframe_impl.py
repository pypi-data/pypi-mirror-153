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
        vetj__utcf = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({vetj__utcf})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    yli__chk = 'def impl(df):\n'
    if df.has_runtime_cols:
        yli__chk += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        exx__dikn = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        yli__chk += f'  return {exx__dikn}'
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo}, admw__egsmy)
    impl = admw__egsmy['impl']
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
    tingb__ehwb = len(df.columns)
    jptf__hsrxy = set(i for i in range(tingb__ehwb) if isinstance(df.data[i
        ], IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in jptf__hsrxy else '') for i in
        range(tingb__ehwb))
    yli__chk = 'def f(df):\n'.format()
    yli__chk += '    return np.stack(({},), 1)\n'.format(data_args)
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'np': np}, admw__egsmy)
    scrbo__iba = admw__egsmy['f']
    return scrbo__iba


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
    nhc__mhj = {'dtype': dtype, 'na_value': na_value}
    knxq__taxp = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', nhc__mhj, knxq__taxp,
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
            ppu__qsgr = bodo.hiframes.table.compute_num_runtime_columns(t)
            return ppu__qsgr * len(t)
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
            ppu__qsgr = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), ppu__qsgr
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    yli__chk = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    bpcb__qyek = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    yli__chk += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{bpcb__qyek}), {index}, None)
"""
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo}, admw__egsmy)
    impl = admw__egsmy['impl']
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
    nhc__mhj = {'copy': copy, 'errors': errors}
    knxq__taxp = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', nhc__mhj, knxq__taxp, package_name=
        'pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        cytix__jpyq = _bodo_object_typeref.instance_type
        assert isinstance(cytix__jpyq, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        pivds__npmaz = {}
        for i, name in enumerate(cytix__jpyq.columns):
            arr_typ = cytix__jpyq.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                oou__onsb = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                oou__onsb = boolean_dtype
            else:
                oou__onsb = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = oou__onsb
            pivds__npmaz[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {pivds__npmaz[vryey__lyp]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if vryey__lyp in pivds__npmaz else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, vryey__lyp in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        nak__baap = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(nak__baap[vryey__lyp])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if vryey__lyp in nak__baap else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, vryey__lyp in enumerate(df.columns))
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
        txgfx__oie = types.none
        extra_globals = {'output_arr_typ': txgfx__oie}
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
        uawxi__djslt = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                uawxi__djslt.append(arr + '.copy()')
            elif is_overload_false(deep):
                uawxi__djslt.append(arr)
            else:
                uawxi__djslt.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(uawxi__djslt)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    nhc__mhj = {'index': index, 'level': level, 'errors': errors}
    knxq__taxp = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', nhc__mhj, knxq__taxp,
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
        fhqj__eabl = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        fhqj__eabl = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    kci__sexai = tuple([fhqj__eabl.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        out_df_type = df.copy(columns=kci__sexai)
        txgfx__oie = types.none
        extra_globals = {'output_arr_typ': txgfx__oie}
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
        uawxi__djslt = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                uawxi__djslt.append(arr + '.copy()')
            elif is_overload_false(copy):
                uawxi__djslt.append(arr)
            else:
                uawxi__djslt.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(uawxi__djslt)
    return _gen_init_df(header, kci__sexai, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    sbf__wze = not is_overload_none(items)
    ktkf__mnf = not is_overload_none(like)
    mvkb__oea = not is_overload_none(regex)
    lotz__vzfh = sbf__wze ^ ktkf__mnf ^ mvkb__oea
    kwcgz__njp = not (sbf__wze or ktkf__mnf or mvkb__oea)
    if kwcgz__njp:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not lotz__vzfh:
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
        sicvu__nkyk = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        sicvu__nkyk = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert sicvu__nkyk in {0, 1}
    yli__chk = 'def impl(df, items=None, like=None, regex=None, axis=None):\n'
    if sicvu__nkyk == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if sicvu__nkyk == 1:
        wyn__cwjbv = []
        akok__yras = []
        oqchl__yve = []
        if sbf__wze:
            if is_overload_constant_list(items):
                mml__jbe = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if ktkf__mnf:
            if is_overload_constant_str(like):
                ywqc__nbtt = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if mvkb__oea:
            if is_overload_constant_str(regex):
                zub__mllti = get_overload_const_str(regex)
                egrh__nuys = re.compile(zub__mllti)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, vryey__lyp in enumerate(df.columns):
            if not is_overload_none(items
                ) and vryey__lyp in mml__jbe or not is_overload_none(like
                ) and ywqc__nbtt in str(vryey__lyp) or not is_overload_none(
                regex) and egrh__nuys.search(str(vryey__lyp)):
                akok__yras.append(vryey__lyp)
                oqchl__yve.append(i)
        for i in oqchl__yve:
            var_name = f'data_{i}'
            wyn__cwjbv.append(var_name)
            yli__chk += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(wyn__cwjbv)
        return _gen_init_df(yli__chk, akok__yras, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        txgfx__oie = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([txgfx__oie] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': txgfx__oie}
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
    knhp__hxx = is_overload_none(include)
    xlwlk__qveec = is_overload_none(exclude)
    hiod__vxzo = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if knhp__hxx and xlwlk__qveec:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not knhp__hxx:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            telww__tbwre = [dtype_to_array_type(parse_dtype(elem,
                hiod__vxzo)) for elem in include]
        elif is_legal_input(include):
            telww__tbwre = [dtype_to_array_type(parse_dtype(include,
                hiod__vxzo))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        telww__tbwre = get_nullable_and_non_nullable_types(telww__tbwre)
        wji__mmfjw = tuple(vryey__lyp for i, vryey__lyp in enumerate(df.
            columns) if df.data[i] in telww__tbwre)
    else:
        wji__mmfjw = df.columns
    if not xlwlk__qveec:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            qedn__jriwk = [dtype_to_array_type(parse_dtype(elem, hiod__vxzo
                )) for elem in exclude]
        elif is_legal_input(exclude):
            qedn__jriwk = [dtype_to_array_type(parse_dtype(exclude,
                hiod__vxzo))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        qedn__jriwk = get_nullable_and_non_nullable_types(qedn__jriwk)
        wji__mmfjw = tuple(vryey__lyp for vryey__lyp in wji__mmfjw if df.
            data[df.column_index[vryey__lyp]] not in qedn__jriwk)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[vryey__lyp]})'
         for vryey__lyp in wji__mmfjw)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, wji__mmfjw, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        txgfx__oie = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([txgfx__oie] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': txgfx__oie}
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
    hjdpi__fwuym = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in hjdpi__fwuym:
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
    hjdpi__fwuym = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in hjdpi__fwuym:
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
    yli__chk = 'def impl(df, values):\n'
    dnj__wztq = {}
    kdduz__uwq = False
    if isinstance(values, DataFrameType):
        kdduz__uwq = True
        for i, vryey__lyp in enumerate(df.columns):
            if vryey__lyp in values.column_index:
                had__hnrgj = 'val{}'.format(i)
                yli__chk += f"""  {had__hnrgj} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[vryey__lyp]})
"""
                dnj__wztq[vryey__lyp] = had__hnrgj
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        dnj__wztq = {vryey__lyp: 'values' for vryey__lyp in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        had__hnrgj = 'data{}'.format(i)
        yli__chk += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(had__hnrgj, i))
        data.append(had__hnrgj)
    ydrp__yec = ['out{}'.format(i) for i in range(len(df.columns))]
    wlzy__bbvxx = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    drc__coqo = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    wcm__bibo = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, tyha__nozvl) in enumerate(zip(df.columns, data)):
        if cname in dnj__wztq:
            tle__ubjhg = dnj__wztq[cname]
            if kdduz__uwq:
                yli__chk += wlzy__bbvxx.format(tyha__nozvl, tle__ubjhg,
                    ydrp__yec[i])
            else:
                yli__chk += drc__coqo.format(tyha__nozvl, tle__ubjhg,
                    ydrp__yec[i])
        else:
            yli__chk += wcm__bibo.format(ydrp__yec[i])
    return _gen_init_df(yli__chk, df.columns, ','.join(ydrp__yec))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    tingb__ehwb = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(tingb__ehwb))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    trpip__scdj = [vryey__lyp for vryey__lyp, movr__mha in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(movr__mha.dtype)
        ]
    assert len(trpip__scdj) != 0
    cdfw__wdqky = ''
    if not any(movr__mha == types.float64 for movr__mha in df.data):
        cdfw__wdqky = '.astype(np.float64)'
    oyta__bheq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[vryey__lyp], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[vryey__lyp]], IntegerArrayType) or
        df.data[df.column_index[vryey__lyp]] == boolean_array else '') for
        vryey__lyp in trpip__scdj)
    ulyy__pvc = 'np.stack(({},), 1){}'.format(oyta__bheq, cdfw__wdqky)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        trpip__scdj)))
    index = f'{generate_col_to_index_func_text(trpip__scdj)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(ulyy__pvc)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, trpip__scdj, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    bhzo__bll = dict(ddof=ddof)
    pxx__kaz = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    rmwd__zxqs = '1' if is_overload_none(min_periods) else 'min_periods'
    trpip__scdj = [vryey__lyp for vryey__lyp, movr__mha in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(movr__mha.dtype)
        ]
    if len(trpip__scdj) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    cdfw__wdqky = ''
    if not any(movr__mha == types.float64 for movr__mha in df.data):
        cdfw__wdqky = '.astype(np.float64)'
    oyta__bheq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[vryey__lyp], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[vryey__lyp]], IntegerArrayType) or
        df.data[df.column_index[vryey__lyp]] == boolean_array else '') for
        vryey__lyp in trpip__scdj)
    ulyy__pvc = 'np.stack(({},), 1){}'.format(oyta__bheq, cdfw__wdqky)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        trpip__scdj)))
    index = f'pd.Index({trpip__scdj})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(ulyy__pvc)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        rmwd__zxqs)
    return _gen_init_df(header, trpip__scdj, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    bhzo__bll = dict(axis=axis, level=level, numeric_only=numeric_only)
    pxx__kaz = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    yli__chk = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    yli__chk += '  data = np.array([{}])\n'.format(data_args)
    exx__dikn = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    yli__chk += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {exx__dikn})\n'
        )
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'np': np}, admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    bhzo__bll = dict(axis=axis)
    pxx__kaz = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    yli__chk = 'def impl(df, axis=0, dropna=True):\n'
    yli__chk += '  data = np.asarray(({},))\n'.format(data_args)
    exx__dikn = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    yli__chk += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {exx__dikn})\n'
        )
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'np': np}, admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    bhzo__bll = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    pxx__kaz = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    bhzo__bll = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    pxx__kaz = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    bhzo__bll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    pxx__kaz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    bhzo__bll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    pxx__kaz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    bhzo__bll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    pxx__kaz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    bhzo__bll = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    pxx__kaz = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    bhzo__bll = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    pxx__kaz = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    bhzo__bll = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    pxx__kaz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    bhzo__bll = dict(numeric_only=numeric_only, interpolation=interpolation)
    pxx__kaz = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    bhzo__bll = dict(axis=axis, skipna=skipna)
    pxx__kaz = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for lty__tdlo in df.data:
        if not (bodo.utils.utils.is_np_array_typ(lty__tdlo) and (lty__tdlo.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            lty__tdlo.dtype, (types.Number, types.Boolean))) or isinstance(
            lty__tdlo, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or
            lty__tdlo in [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {lty__tdlo} not supported.'
                )
        if isinstance(lty__tdlo, bodo.CategoricalArrayType
            ) and not lty__tdlo.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    bhzo__bll = dict(axis=axis, skipna=skipna)
    pxx__kaz = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for lty__tdlo in df.data:
        if not (bodo.utils.utils.is_np_array_typ(lty__tdlo) and (lty__tdlo.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            lty__tdlo.dtype, (types.Number, types.Boolean))) or isinstance(
            lty__tdlo, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or
            lty__tdlo in [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {lty__tdlo} not supported.'
                )
        if isinstance(lty__tdlo, bodo.CategoricalArrayType
            ) and not lty__tdlo.dtype.ordered:
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
        trpip__scdj = tuple(vryey__lyp for vryey__lyp, movr__mha in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (movr__mha.dtype))
        out_colnames = trpip__scdj
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            kiaak__mlf = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[vryey__lyp]].dtype) for vryey__lyp in out_colnames
                ]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(kiaak__mlf, []))
    except NotImplementedError as hedr__hpqa:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    tdqq__cftr = ''
    if func_name in ('sum', 'prod'):
        tdqq__cftr = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    yli__chk = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, tdqq__cftr))
    if func_name == 'quantile':
        yli__chk = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        yli__chk = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        yli__chk += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        yli__chk += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    ncnfw__tijq = ''
    if func_name in ('min', 'max'):
        ncnfw__tijq = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        ncnfw__tijq = ', dtype=np.float32'
    ivd__qarrm = f'bodo.libs.array_ops.array_op_{func_name}'
    qqn__bpyl = ''
    if func_name in ['sum', 'prod']:
        qqn__bpyl = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        qqn__bpyl = 'index'
    elif func_name == 'quantile':
        qqn__bpyl = 'q'
    elif func_name in ['std', 'var']:
        qqn__bpyl = 'True, ddof'
    elif func_name == 'median':
        qqn__bpyl = 'True'
    data_args = ', '.join(
        f'{ivd__qarrm}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[vryey__lyp]}), {qqn__bpyl})'
         for vryey__lyp in out_colnames)
    yli__chk = ''
    if func_name in ('idxmax', 'idxmin'):
        yli__chk += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        yli__chk += ('  data = bodo.utils.conversion.coerce_to_array(({},))\n'
            .format(data_args))
    else:
        yli__chk += '  data = np.asarray(({},){})\n'.format(data_args,
            ncnfw__tijq)
    yli__chk += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return yli__chk


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    lukww__mqii = [df_type.column_index[vryey__lyp] for vryey__lyp in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in lukww__mqii)
    fma__dqy = '\n        '.join(f'row[{i}] = arr_{lukww__mqii[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    xaxs__wqyvz = f'len(arr_{lukww__mqii[0]})'
    ypp__ktidc = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in ypp__ktidc:
        wexnq__aeli = ypp__ktidc[func_name]
        kry__anz = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        yli__chk = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {xaxs__wqyvz}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{kry__anz})
    for i in numba.parfors.parfor.internal_prange(n):
        {fma__dqy}
        A[i] = {wexnq__aeli}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return yli__chk
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    bhzo__bll = dict(fill_method=fill_method, limit=limit, freq=freq)
    pxx__kaz = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
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
    bhzo__bll = dict(axis=axis, skipna=skipna)
    pxx__kaz = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', bhzo__bll, pxx__kaz,
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
    bhzo__bll = dict(skipna=skipna)
    pxx__kaz = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', bhzo__bll, pxx__kaz,
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
    bhzo__bll = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    pxx__kaz = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    trpip__scdj = [vryey__lyp for vryey__lyp, movr__mha in zip(df.columns,
        df.data) if _is_describe_type(movr__mha)]
    if len(trpip__scdj) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    mvhh__foc = sum(df.data[df.column_index[vryey__lyp]].dtype == bodo.
        datetime64ns for vryey__lyp in trpip__scdj)

    def _get_describe(col_ind):
        awxbp__yzppq = df.data[col_ind].dtype == bodo.datetime64ns
        if mvhh__foc and mvhh__foc != len(trpip__scdj):
            if awxbp__yzppq:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for vryey__lyp in trpip__scdj:
        col_ind = df.column_index[vryey__lyp]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[vryey__lyp]) for
        vryey__lyp in trpip__scdj)
    ktk__enzzy = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if mvhh__foc == len(trpip__scdj):
        ktk__enzzy = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif mvhh__foc:
        ktk__enzzy = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({ktk__enzzy})'
    return _gen_init_df(header, trpip__scdj, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    bhzo__bll = dict(axis=axis, convert=convert, is_copy=is_copy)
    pxx__kaz = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', bhzo__bll, pxx__kaz,
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
    bhzo__bll = dict(freq=freq, axis=axis, fill_value=fill_value)
    pxx__kaz = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for bmpd__gcvtj in df.data:
        if not is_supported_shift_array_type(bmpd__gcvtj):
            raise BodoError(
                f'Dataframe.shift() column input type {bmpd__gcvtj.dtype} not supported yet.'
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
    bhzo__bll = dict(axis=axis)
    pxx__kaz = dict(axis=0)
    check_unsupported_args('DataFrame.diff', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for bmpd__gcvtj in df.data:
        if not (isinstance(bmpd__gcvtj, types.Array) and (isinstance(
            bmpd__gcvtj.dtype, types.Number) or bmpd__gcvtj.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {bmpd__gcvtj.dtype} not supported.'
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
    vipm__mmobk = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(vipm__mmobk)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        hajsw__gslnh = get_overload_const_list(column)
    else:
        hajsw__gslnh = [get_literal_value(column)]
    fvcl__dnn = [df.column_index[vryey__lyp] for vryey__lyp in hajsw__gslnh]
    for i in fvcl__dnn:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{fvcl__dnn[0]})\n'
        )
    for i in range(n):
        if i in fvcl__dnn:
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
    nhc__mhj = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    knxq__taxp = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', nhc__mhj, knxq__taxp,
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
    columns = tuple(vryey__lyp for vryey__lyp in df.columns if vryey__lyp !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    nhc__mhj = {'inplace': inplace}
    knxq__taxp = {'inplace': False}
    check_unsupported_args('query', nhc__mhj, knxq__taxp, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        zcjc__wctd = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[zcjc__wctd]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    nhc__mhj = {'subset': subset, 'keep': keep}
    knxq__taxp = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', nhc__mhj, knxq__taxp,
        package_name='pandas', module_name='DataFrame')
    tingb__ehwb = len(df.columns)
    yli__chk = "def impl(df, subset=None, keep='first'):\n"
    for i in range(tingb__ehwb):
        yli__chk += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    xso__zlxiv = ', '.join(f'data_{i}' for i in range(tingb__ehwb))
    xso__zlxiv += ',' if tingb__ehwb == 1 else ''
    yli__chk += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({xso__zlxiv}))\n')
    yli__chk += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    yli__chk += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo}, admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    nhc__mhj = {'keep': keep, 'inplace': inplace, 'ignore_index': ignore_index}
    knxq__taxp = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    rskpm__olb = []
    if is_overload_constant_list(subset):
        rskpm__olb = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        rskpm__olb = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        rskpm__olb = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    xdvy__teiby = []
    for col_name in rskpm__olb:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        xdvy__teiby.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', nhc__mhj,
        knxq__taxp, package_name='pandas', module_name='DataFrame')
    gauj__wdsx = []
    if xdvy__teiby:
        for bygsg__ccs in xdvy__teiby:
            if isinstance(df.data[bygsg__ccs], bodo.MapArrayType):
                gauj__wdsx.append(df.columns[bygsg__ccs])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                gauj__wdsx.append(col_name)
    if gauj__wdsx:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {gauj__wdsx} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    tingb__ehwb = len(df.columns)
    xxn__wuyp = ['data_{}'.format(i) for i in xdvy__teiby]
    fbba__fmy = ['data_{}'.format(i) for i in range(tingb__ehwb) if i not in
        xdvy__teiby]
    if xxn__wuyp:
        nwbfa__yotxm = len(xxn__wuyp)
    else:
        nwbfa__yotxm = tingb__ehwb
    wvmq__kjnz = ', '.join(xxn__wuyp + fbba__fmy)
    data_args = ', '.join('data_{}'.format(i) for i in range(tingb__ehwb))
    yli__chk = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(tingb__ehwb):
        yli__chk += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    yli__chk += (
        '  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})\n'
        .format(wvmq__kjnz, index, nwbfa__yotxm))
    yli__chk += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return _gen_init_df(yli__chk, df.columns, data_args, 'index')


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
            hjch__kbqil = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                hjch__kbqil = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                hjch__kbqil = lambda i: f'other[:,{i}]'
        tingb__ehwb = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {hjch__kbqil(i)})'
             for i in range(tingb__ehwb))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        xugq__xeu = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(xugq__xeu)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    bhzo__bll = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    pxx__kaz = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', bhzo__bll, pxx__kaz,
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
    tingb__ehwb = len(df.columns)
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
        for i in range(tingb__ehwb):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other.column_index[df
                    .columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(tingb__ehwb):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(tingb__ehwb):
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
        aixtx__wqak = 'out_df_type'
    else:
        aixtx__wqak = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    yli__chk = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {aixtx__wqak})
"""
    admw__egsmy = {}
    fdzh__horzz = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    fdzh__horzz.update(extra_globals)
    exec(yli__chk, fdzh__horzz, admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        onsxv__qhnmo = pd.Index(lhs.columns)
        kdzoc__aly = pd.Index(rhs.columns)
        tyl__lud, yll__tbz, kepxr__ybtja = onsxv__qhnmo.join(kdzoc__aly,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(tyl__lud), yll__tbz, kepxr__ybtja
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        iyjdk__gsan = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        jxlqp__cdoi = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, iyjdk__gsan)
        check_runtime_cols_unsupported(rhs, iyjdk__gsan)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                tyl__lud, yll__tbz, kepxr__ybtja = _get_binop_columns(lhs, rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {tagt__cgu}) {iyjdk__gsan}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {zecu__hpz})'
                     if tagt__cgu != -1 and zecu__hpz != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for tagt__cgu, zecu__hpz in zip(yll__tbz, kepxr__ybtja))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, tyl__lud, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            oto__jqw = []
            hjduo__rnrxp = []
            if op in jxlqp__cdoi:
                for i, iquyx__amwp in enumerate(lhs.data):
                    if is_common_scalar_dtype([iquyx__amwp.dtype, rhs]):
                        oto__jqw.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {iyjdk__gsan} rhs'
                            )
                    else:
                        cvfzo__xckg = f'arr{i}'
                        hjduo__rnrxp.append(cvfzo__xckg)
                        oto__jqw.append(cvfzo__xckg)
                data_args = ', '.join(oto__jqw)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {iyjdk__gsan} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(hjduo__rnrxp) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {cvfzo__xckg} = np.empty(n, dtype=np.bool_)\n' for
                    cvfzo__xckg in hjduo__rnrxp)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(cvfzo__xckg, 
                    op == operator.ne) for cvfzo__xckg in hjduo__rnrxp)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            oto__jqw = []
            hjduo__rnrxp = []
            if op in jxlqp__cdoi:
                for i, iquyx__amwp in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, iquyx__amwp.dtype]):
                        oto__jqw.append(
                            f'lhs {iyjdk__gsan} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        cvfzo__xckg = f'arr{i}'
                        hjduo__rnrxp.append(cvfzo__xckg)
                        oto__jqw.append(cvfzo__xckg)
                data_args = ', '.join(oto__jqw)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, iyjdk__gsan) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(hjduo__rnrxp) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(cvfzo__xckg) for cvfzo__xckg in hjduo__rnrxp)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(cvfzo__xckg, 
                    op == operator.ne) for cvfzo__xckg in hjduo__rnrxp)
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
        xugq__xeu = create_binary_op_overload(op)
        overload(op)(xugq__xeu)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        iyjdk__gsan = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, iyjdk__gsan)
        check_runtime_cols_unsupported(right, iyjdk__gsan)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                tyl__lud, _, kepxr__ybtja = _get_binop_columns(left, right,
                    True)
                yli__chk = 'def impl(left, right):\n'
                for i, zecu__hpz in enumerate(kepxr__ybtja):
                    if zecu__hpz == -1:
                        yli__chk += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    yli__chk += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    yli__chk += f"""  df_arr{i} {iyjdk__gsan} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {zecu__hpz})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    tyl__lud)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(yli__chk, tyl__lud, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            yli__chk = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                yli__chk += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                yli__chk += '  df_arr{0} {1} right\n'.format(i, iyjdk__gsan)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(yli__chk, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        xugq__xeu = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(xugq__xeu)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            iyjdk__gsan = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, iyjdk__gsan)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, iyjdk__gsan) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        xugq__xeu = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(xugq__xeu)


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
            yzir__rxrr = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                yzir__rxrr[i] = bodo.libs.array_kernels.isna(obj, i)
            return yzir__rxrr
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
            yzir__rxrr = np.empty(n, np.bool_)
            for i in range(n):
                yzir__rxrr[i] = pd.isna(obj[i])
            return yzir__rxrr
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
    nhc__mhj = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    knxq__taxp = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', nhc__mhj, knxq__taxp, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    gmzv__bhqtk = str(expr_node)
    return gmzv__bhqtk.startswith('left.') or gmzv__bhqtk.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    nncuo__kdaa = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (nncuo__kdaa,))
    uwp__fuk = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        gbcm__paj = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        ivcl__ktmq = {('NOT_NA', uwp__fuk(iquyx__amwp)): iquyx__amwp for
            iquyx__amwp in null_set}
        alt__ozif, _, _ = _parse_query_expr(gbcm__paj, env, [], [], None,
            join_cleaned_cols=ivcl__ktmq)
        ugnji__orem = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            wdjf__gdskk = pd.core.computation.ops.BinOp('&', alt__ozif,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = ugnji__orem
        return wdjf__gdskk

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                ggldx__imtzx = set()
                dzyl__spo = set()
                utdhy__nzbb = _insert_NA_cond_body(expr_node.lhs, ggldx__imtzx)
                dyvm__amlku = _insert_NA_cond_body(expr_node.rhs, dzyl__spo)
                tisda__ughx = ggldx__imtzx.intersection(dzyl__spo)
                ggldx__imtzx.difference_update(tisda__ughx)
                dzyl__spo.difference_update(tisda__ughx)
                null_set.update(tisda__ughx)
                expr_node.lhs = append_null_checks(utdhy__nzbb, ggldx__imtzx)
                expr_node.rhs = append_null_checks(dyvm__amlku, dzyl__spo)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            yxtb__lout = expr_node.name
            ubzol__mys, col_name = yxtb__lout.split('.')
            if ubzol__mys == 'left':
                hvqph__boixf = left_columns
                data = left_data
            else:
                hvqph__boixf = right_columns
                data = right_data
            ryofb__kkeb = data[hvqph__boixf.index(col_name)]
            if bodo.utils.typing.is_nullable(ryofb__kkeb):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    yofr__lsay = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        gpoj__mjqg = str(expr_node.lhs)
        gjpph__qlu = str(expr_node.rhs)
        if gpoj__mjqg.startswith('left.') and gjpph__qlu.startswith('left.'
            ) or gpoj__mjqg.startswith('right.') and gjpph__qlu.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [gpoj__mjqg.split('.')[1]]
        right_on = [gjpph__qlu.split('.')[1]]
        if gpoj__mjqg.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        ttpy__houd, uqz__blhc, uige__fjmif = _extract_equal_conds(expr_node.lhs
            )
        gughx__xtz, mxjaa__hbp, mhzr__zekgc = _extract_equal_conds(expr_node
            .rhs)
        left_on = ttpy__houd + gughx__xtz
        right_on = uqz__blhc + mxjaa__hbp
        if uige__fjmif is None:
            return left_on, right_on, mhzr__zekgc
        if mhzr__zekgc is None:
            return left_on, right_on, uige__fjmif
        expr_node.lhs = uige__fjmif
        expr_node.rhs = mhzr__zekgc
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    nncuo__kdaa = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (nncuo__kdaa,))
    fhqj__eabl = dict()
    uwp__fuk = pd.core.computation.parsing.clean_column_name
    for name, cpl__bxts in (('left', left_columns), ('right', right_columns)):
        for iquyx__amwp in cpl__bxts:
            jyav__agi = uwp__fuk(iquyx__amwp)
            ypim__vdgux = name, jyav__agi
            if ypim__vdgux in fhqj__eabl:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{iquyx__amwp}' and '{fhqj__eabl[jyav__agi]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            fhqj__eabl[ypim__vdgux] = iquyx__amwp
    uacg__zzsjd, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=fhqj__eabl)
    left_on, right_on, dagt__tdd = _extract_equal_conds(uacg__zzsjd.terms)
    return left_on, right_on, _insert_NA_cond(dagt__tdd, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    bhzo__bll = dict(sort=sort, copy=copy, validate=validate)
    pxx__kaz = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    aod__jna = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    ywru__gioyj = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in aod__jna and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, eqde__oljjz = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if eqde__oljjz is None:
                    ywru__gioyj = ''
                else:
                    ywru__gioyj = str(eqde__oljjz)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = aod__jna
        right_keys = aod__jna
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
    ppha__lag = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        nwvc__ahcs = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        nwvc__ahcs = list(get_overload_const_list(suffixes))
    suffix_x = nwvc__ahcs[0]
    suffix_y = nwvc__ahcs[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    yli__chk = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    yli__chk += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    yli__chk += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    yli__chk += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, ppha__lag, ywru__gioyj))
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo}, admw__egsmy)
    _impl = admw__egsmy['_impl']
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
    nxat__jfe = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    yllhw__gxk = {get_overload_const_str(inuru__zspr) for inuru__zspr in (
        left_on, right_on, on) if is_overload_constant_str(inuru__zspr)}
    for df in (left, right):
        for i, iquyx__amwp in enumerate(df.data):
            if not isinstance(iquyx__amwp, valid_dataframe_column_types
                ) and iquyx__amwp not in nxat__jfe:
                raise BodoError(
                    f'{name_func}(): use of column with {type(iquyx__amwp)} in merge unsupported'
                    )
            if df.columns[i] in yllhw__gxk and isinstance(iquyx__amwp,
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
        nwvc__ahcs = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        nwvc__ahcs = list(get_overload_const_list(suffixes))
    if len(nwvc__ahcs) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    aod__jna = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        ozm__fmo = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            ozm__fmo = on_str not in aod__jna and ('left.' in on_str or 
                'right.' in on_str)
        if len(aod__jna) == 0 and not ozm__fmo:
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
    ykk__xdzzl = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            jtxg__pwuz = left.index
            bhz__wnhh = isinstance(jtxg__pwuz, StringIndexType)
            vgxjy__wnvm = right.index
            vjrwi__svp = isinstance(vgxjy__wnvm, StringIndexType)
        elif is_overload_true(left_index):
            jtxg__pwuz = left.index
            bhz__wnhh = isinstance(jtxg__pwuz, StringIndexType)
            vgxjy__wnvm = right.data[right.columns.index(right_keys[0])]
            vjrwi__svp = vgxjy__wnvm.dtype == string_type
        elif is_overload_true(right_index):
            jtxg__pwuz = left.data[left.columns.index(left_keys[0])]
            bhz__wnhh = jtxg__pwuz.dtype == string_type
            vgxjy__wnvm = right.index
            vjrwi__svp = isinstance(vgxjy__wnvm, StringIndexType)
        if bhz__wnhh and vjrwi__svp:
            return
        jtxg__pwuz = jtxg__pwuz.dtype
        vgxjy__wnvm = vgxjy__wnvm.dtype
        try:
            ftf__pfyut = ykk__xdzzl.resolve_function_type(operator.eq, (
                jtxg__pwuz, vgxjy__wnvm), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=jtxg__pwuz, rk_dtype=vgxjy__wnvm))
    else:
        for hyhk__ubfi, rlyq__voh in zip(left_keys, right_keys):
            jtxg__pwuz = left.data[left.columns.index(hyhk__ubfi)].dtype
            ccla__pnw = left.data[left.columns.index(hyhk__ubfi)]
            vgxjy__wnvm = right.data[right.columns.index(rlyq__voh)].dtype
            ssrhx__kof = right.data[right.columns.index(rlyq__voh)]
            if ccla__pnw == ssrhx__kof:
                continue
            ymy__xex = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=hyhk__ubfi, lk_dtype=jtxg__pwuz, rk=rlyq__voh,
                rk_dtype=vgxjy__wnvm))
            zgwjc__vdnto = jtxg__pwuz == string_type
            npx__loea = vgxjy__wnvm == string_type
            if zgwjc__vdnto ^ npx__loea:
                raise_bodo_error(ymy__xex)
            try:
                ftf__pfyut = ykk__xdzzl.resolve_function_type(operator.eq,
                    (jtxg__pwuz, vgxjy__wnvm), {})
            except:
                raise_bodo_error(ymy__xex)


def validate_keys(keys, df):
    heq__evrq = set(keys).difference(set(df.columns))
    if len(heq__evrq) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in heq__evrq:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {heq__evrq} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    bhzo__bll = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    pxx__kaz = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', bhzo__bll, pxx__kaz,
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
    yli__chk = "def _impl(left, other, on=None, how='left',\n"
    yli__chk += "    lsuffix='', rsuffix='', sort=False):\n"
    yli__chk += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo}, admw__egsmy)
    _impl = admw__egsmy['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        oougp__ubc = get_overload_const_list(on)
        validate_keys(oougp__ubc, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    aod__jna = tuple(set(left.columns) & set(other.columns))
    if len(aod__jna) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=aod__jna))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    nps__nmd = set(left_keys) & set(right_keys)
    jzbax__knt = set(left_columns) & set(right_columns)
    xrfhx__weih = jzbax__knt - nps__nmd
    xomzb__tcww = set(left_columns) - jzbax__knt
    ynf__iidm = set(right_columns) - jzbax__knt
    lnvr__qcydn = {}

    def insertOutColumn(col_name):
        if col_name in lnvr__qcydn:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        lnvr__qcydn[col_name] = 0
    for qtvy__zxc in nps__nmd:
        insertOutColumn(qtvy__zxc)
    for qtvy__zxc in xrfhx__weih:
        liemt__smsq = str(qtvy__zxc) + suffix_x
        ouhf__tyaiq = str(qtvy__zxc) + suffix_y
        insertOutColumn(liemt__smsq)
        insertOutColumn(ouhf__tyaiq)
    for qtvy__zxc in xomzb__tcww:
        insertOutColumn(qtvy__zxc)
    for qtvy__zxc in ynf__iidm:
        insertOutColumn(qtvy__zxc)
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
    aod__jna = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = aod__jna
        right_keys = aod__jna
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
        nwvc__ahcs = suffixes
    if is_overload_constant_list(suffixes):
        nwvc__ahcs = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        nwvc__ahcs = suffixes.value
    suffix_x = nwvc__ahcs[0]
    suffix_y = nwvc__ahcs[1]
    yli__chk = 'def _impl(left, right, on=None, left_on=None, right_on=None,\n'
    yli__chk += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    yli__chk += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    yli__chk += "    allow_exact_matches=True, direction='backward'):\n"
    yli__chk += '  suffix_x = suffixes[0]\n'
    yli__chk += '  suffix_y = suffixes[1]\n'
    yli__chk += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo}, admw__egsmy)
    _impl = admw__egsmy['_impl']
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
    bhzo__bll = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    abxjv__wpnyj = dict(sort=False, group_keys=True, squeeze=False,
        observed=True)
    check_unsupported_args('Dataframe.groupby', bhzo__bll, abxjv__wpnyj,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    ouedp__wpuzg = func_name == 'DataFrame.pivot_table'
    if ouedp__wpuzg:
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
    bunpv__jgti = get_literal_value(columns)
    if isinstance(bunpv__jgti, (list, tuple)):
        if len(bunpv__jgti) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {bunpv__jgti}"
                )
        bunpv__jgti = bunpv__jgti[0]
    if bunpv__jgti not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {bunpv__jgti} not found in DataFrame {df}."
            )
    qgwqv__cjpwt = df.column_index[bunpv__jgti]
    if is_overload_none(index):
        uqczt__ucqt = []
        sho__rcdm = []
    else:
        sho__rcdm = get_literal_value(index)
        if not isinstance(sho__rcdm, (list, tuple)):
            sho__rcdm = [sho__rcdm]
        uqczt__ucqt = []
        for index in sho__rcdm:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            uqczt__ucqt.append(df.column_index[index])
    if not (all(isinstance(vryey__lyp, int) for vryey__lyp in sho__rcdm) or
        all(isinstance(vryey__lyp, str) for vryey__lyp in sho__rcdm)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        bidl__hyav = []
        ruwml__eylq = []
        qzhge__ygwha = uqczt__ucqt + [qgwqv__cjpwt]
        for i, vryey__lyp in enumerate(df.columns):
            if i not in qzhge__ygwha:
                bidl__hyav.append(i)
                ruwml__eylq.append(vryey__lyp)
    else:
        ruwml__eylq = get_literal_value(values)
        if not isinstance(ruwml__eylq, (list, tuple)):
            ruwml__eylq = [ruwml__eylq]
        bidl__hyav = []
        for val in ruwml__eylq:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            bidl__hyav.append(df.column_index[val])
    if all(isinstance(vryey__lyp, int) for vryey__lyp in ruwml__eylq):
        ruwml__eylq = np.array(ruwml__eylq, 'int64')
    elif all(isinstance(vryey__lyp, str) for vryey__lyp in ruwml__eylq):
        ruwml__eylq = pd.array(ruwml__eylq, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    qqiuj__mlrvl = set(bidl__hyav) | set(uqczt__ucqt) | {qgwqv__cjpwt}
    if len(qqiuj__mlrvl) != len(bidl__hyav) + len(uqczt__ucqt) + 1:
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
    if len(uqczt__ucqt) == 0:
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
        for ylok__kvus in uqczt__ucqt:
            index_column = df.data[ylok__kvus]
            check_valid_index_typ(index_column)
    gaa__cyg = df.data[qgwqv__cjpwt]
    if isinstance(gaa__cyg, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(gaa__cyg, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for nraz__rnr in bidl__hyav:
        ndo__vcs = df.data[nraz__rnr]
        if isinstance(ndo__vcs, (bodo.ArrayItemArrayType, bodo.MapArrayType,
            bodo.StructArrayType, bodo.TupleArrayType)
            ) or ndo__vcs == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (sho__rcdm, bunpv__jgti, ruwml__eylq, uqczt__ucqt, qgwqv__cjpwt,
        bidl__hyav)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (sho__rcdm, bunpv__jgti, ruwml__eylq, ylok__kvus, qgwqv__cjpwt, nrww__odi
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(sho__rcdm) == 0:
        if is_overload_none(data.index.name_typ):
            sho__rcdm = [None]
        else:
            sho__rcdm = [get_literal_value(data.index.name_typ)]
    if len(ruwml__eylq) == 1:
        ssygp__tko = None
    else:
        ssygp__tko = ruwml__eylq
    yli__chk = 'def impl(data, index=None, columns=None, values=None):\n'
    yli__chk += f'    pivot_values = data.iloc[:, {qgwqv__cjpwt}].unique()\n'
    yli__chk += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(ylok__kvus) == 0:
        yli__chk += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        yli__chk += '        (\n'
        for geq__eks in ylok__kvus:
            yli__chk += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {geq__eks}),
"""
        yli__chk += '        ),\n'
    yli__chk += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {qgwqv__cjpwt}),),
"""
    yli__chk += '        (\n'
    for nraz__rnr in nrww__odi:
        yli__chk += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {nraz__rnr}),
"""
    yli__chk += '        ),\n'
    yli__chk += '        pivot_values,\n'
    yli__chk += '        index_lit_tup,\n'
    yli__chk += '        columns_lit,\n'
    yli__chk += '        values_name_const,\n'
    yli__chk += '    )\n'
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'index_lit_tup': tuple(sho__rcdm),
        'columns_lit': bunpv__jgti, 'values_name_const': ssygp__tko},
        admw__egsmy)
    impl = admw__egsmy['impl']
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
    bhzo__bll = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    pxx__kaz = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (sho__rcdm, bunpv__jgti, ruwml__eylq, ylok__kvus, qgwqv__cjpwt,
            nrww__odi) = (pivot_error_checking(data, index, columns, values,
            'DataFrame.pivot_table'))
        if len(ruwml__eylq) == 1:
            ssygp__tko = None
        else:
            ssygp__tko = ruwml__eylq
        yli__chk = 'def impl(\n'
        yli__chk += '    data,\n'
        yli__chk += '    values=None,\n'
        yli__chk += '    index=None,\n'
        yli__chk += '    columns=None,\n'
        yli__chk += '    aggfunc="mean",\n'
        yli__chk += '    fill_value=None,\n'
        yli__chk += '    margins=False,\n'
        yli__chk += '    dropna=True,\n'
        yli__chk += '    margins_name="All",\n'
        yli__chk += '    observed=False,\n'
        yli__chk += '    sort=True,\n'
        yli__chk += '    _pivot_values=None,\n'
        yli__chk += '):\n'
        ovgnp__irbn = ylok__kvus + [qgwqv__cjpwt] + nrww__odi
        yli__chk += f'    data = data.iloc[:, {ovgnp__irbn}]\n'
        aux__goqcz = sho__rcdm + [bunpv__jgti]
        yli__chk += (
            f'    data = data.groupby({aux__goqcz!r}, as_index=False).agg(aggfunc)\n'
            )
        yli__chk += (
            f'    pivot_values = data.iloc[:, {len(ylok__kvus)}].unique()\n')
        yli__chk += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
        yli__chk += '        (\n'
        for i in range(0, len(ylok__kvus)):
            yli__chk += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        yli__chk += '        ),\n'
        yli__chk += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(ylok__kvus)}),),
"""
        yli__chk += '        (\n'
        for i in range(len(ylok__kvus) + 1, len(nrww__odi) + len(ylok__kvus
            ) + 1):
            yli__chk += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        yli__chk += '        ),\n'
        yli__chk += '        pivot_values,\n'
        yli__chk += '        index_lit_tup,\n'
        yli__chk += '        columns_lit,\n'
        yli__chk += '        values_name_const,\n'
        yli__chk += '        check_duplicates=False,\n'
        yli__chk += '    )\n'
        admw__egsmy = {}
        exec(yli__chk, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(sho__rcdm), 'columns_lit': bunpv__jgti,
            'values_name_const': ssygp__tko}, admw__egsmy)
        impl = admw__egsmy['impl']
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
    bhzo__bll = dict(col_level=col_level, ignore_index=ignore_index)
    pxx__kaz = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', bhzo__bll, pxx__kaz,
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
    tsknx__kghnj = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(tsknx__kghnj, (list, tuple)):
        tsknx__kghnj = [tsknx__kghnj]
    for vryey__lyp in tsknx__kghnj:
        if vryey__lyp not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {vryey__lyp} not found in {frame}."
                )
    uiymh__hbxw = [frame.column_index[i] for i in tsknx__kghnj]
    if is_overload_none(value_vars):
        ltbhi__bguq = []
        prq__gscm = []
        for i, vryey__lyp in enumerate(frame.columns):
            if i not in uiymh__hbxw:
                ltbhi__bguq.append(i)
                prq__gscm.append(vryey__lyp)
    else:
        prq__gscm = get_literal_value(value_vars)
        if not isinstance(prq__gscm, (list, tuple)):
            prq__gscm = [prq__gscm]
        prq__gscm = [v for v in prq__gscm if v not in tsknx__kghnj]
        if not prq__gscm:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        ltbhi__bguq = []
        for val in prq__gscm:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            ltbhi__bguq.append(frame.column_index[val])
    for vryey__lyp in prq__gscm:
        if vryey__lyp not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {vryey__lyp} not found in {frame}."
                )
    if not (all(isinstance(vryey__lyp, int) for vryey__lyp in prq__gscm) or
        all(isinstance(vryey__lyp, str) for vryey__lyp in prq__gscm)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    oty__ezclu = frame.data[ltbhi__bguq[0]]
    nkcu__dhhhc = [frame.data[i].dtype for i in ltbhi__bguq]
    ltbhi__bguq = np.array(ltbhi__bguq, dtype=np.int64)
    uiymh__hbxw = np.array(uiymh__hbxw, dtype=np.int64)
    _, iuhw__juhn = bodo.utils.typing.get_common_scalar_dtype(nkcu__dhhhc)
    if not iuhw__juhn:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': prq__gscm, 'val_type': oty__ezclu}
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
    if frame.is_table_format and all(v == oty__ezclu.dtype for v in nkcu__dhhhc
        ):
        extra_globals['value_idxs'] = ltbhi__bguq
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(prq__gscm) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {ltbhi__bguq[0]})
"""
    else:
        uxoup__tnq = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in ltbhi__bguq)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({uxoup__tnq},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in uiymh__hbxw:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(prq__gscm)})\n'
            )
    cmf__dykx = ', '.join(f'out_id{i}' for i in uiymh__hbxw) + (', ' if len
        (uiymh__hbxw) > 0 else '')
    data_args = cmf__dykx + 'var_col, val_col'
    columns = tuple(tsknx__kghnj + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(prq__gscm)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    bhzo__bll = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    pxx__kaz = dict(values=None, rownames=None, colnames=None, aggfunc=None,
        margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', bhzo__bll, pxx__kaz,
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
    bhzo__bll = dict(ignore_index=ignore_index, key=key)
    pxx__kaz = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
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
    qxqus__liwwt = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        qxqus__liwwt.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        gasl__scf = [get_overload_const_tuple(by)]
    else:
        gasl__scf = get_overload_const_list(by)
    gasl__scf = set((k, '') if (k, '') in qxqus__liwwt else k for k in
        gasl__scf)
    if len(gasl__scf.difference(qxqus__liwwt)) > 0:
        buxj__qwxen = list(set(get_overload_const_list(by)).difference(
            qxqus__liwwt))
        raise_bodo_error(f'sort_values(): invalid keys {buxj__qwxen} for by.')
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
        qibf__yyd = get_overload_const_list(na_position)
        for na_position in qibf__yyd:
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
    bhzo__bll = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    pxx__kaz = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
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
    bhzo__bll = dict(limit=limit, downcast=downcast)
    pxx__kaz = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    kgm__kjq = not is_overload_none(value)
    vop__uhkq = not is_overload_none(method)
    if kgm__kjq and vop__uhkq:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not kgm__kjq and not vop__uhkq:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if kgm__kjq:
        iym__cbuuv = 'value=value'
    else:
        iym__cbuuv = 'method=method'
    data_args = [(
        f"df['{vryey__lyp}'].fillna({iym__cbuuv}, inplace=inplace)" if
        isinstance(vryey__lyp, str) else
        f'df[{vryey__lyp}].fillna({iym__cbuuv}, inplace=inplace)') for
        vryey__lyp in df.columns]
    yli__chk = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        yli__chk += '  ' + '  \n'.join(data_args) + '\n'
        admw__egsmy = {}
        exec(yli__chk, {}, admw__egsmy)
        impl = admw__egsmy['impl']
        return impl
    else:
        return _gen_init_df(yli__chk, df.columns, ', '.join(movr__mha +
            '.values' for movr__mha in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    bhzo__bll = dict(col_level=col_level, col_fill=col_fill)
    pxx__kaz = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', bhzo__bll, pxx__kaz,
        package_name='pandas', module_name='DataFrame')
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
    yli__chk = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    yli__chk += (
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
        akh__lhx = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            akh__lhx)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            yli__chk += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            sere__igall = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = sere__igall + data_args
        else:
            jcpt__zxux = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [jcpt__zxux] + data_args
    return _gen_init_df(yli__chk, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    bleo__zraak = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and bleo__zraak == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(bleo__zraak))


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
        yjev__bohn = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        feq__rgeiq = get_overload_const_list(subset)
        yjev__bohn = []
        for rpfp__drms in feq__rgeiq:
            if rpfp__drms not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{rpfp__drms}' not in data frame columns {df}"
                    )
            yjev__bohn.append(df.column_index[rpfp__drms])
    tingb__ehwb = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(tingb__ehwb))
    yli__chk = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(tingb__ehwb):
        yli__chk += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    yli__chk += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in yjev__bohn)))
    yli__chk += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return _gen_init_df(yli__chk, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    bhzo__bll = dict(index=index, level=level, errors=errors)
    pxx__kaz = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', bhzo__bll, pxx__kaz,
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
            oul__qjy = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            oul__qjy = get_overload_const_list(labels)
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
            oul__qjy = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            oul__qjy = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for vryey__lyp in oul__qjy:
        if vryey__lyp not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(vryey__lyp, df.columns))
    if len(set(oul__qjy)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    kci__sexai = tuple(vryey__lyp for vryey__lyp in df.columns if 
        vryey__lyp not in oul__qjy)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[vryey__lyp], '.copy()' if not inplace else
        '') for vryey__lyp in kci__sexai)
    yli__chk = 'def impl(df, labels=None, axis=0, index=None, columns=None,\n'
    yli__chk += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(yli__chk, kci__sexai, data_args, index)


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
    bhzo__bll = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    gjeyj__bve = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', bhzo__bll, gjeyj__bve,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    tingb__ehwb = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(tingb__ehwb))
    fqqu__lmo = ', '.join('rhs_data_{}'.format(i) for i in range(tingb__ehwb))
    yli__chk = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    yli__chk += '  if (frac == 1 or n == len(df)) and not replace:\n'
    yli__chk += '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n'
    for i in range(tingb__ehwb):
        yli__chk += (
            '  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    yli__chk += '  if frac is None:\n'
    yli__chk += '    frac_d = -1.0\n'
    yli__chk += '  else:\n'
    yli__chk += '    frac_d = frac\n'
    yli__chk += '  if n is None:\n'
    yli__chk += '    n_i = 0\n'
    yli__chk += '  else:\n'
    yli__chk += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    yli__chk += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({fqqu__lmo},), {index}, n_i, frac_d, replace)
"""
    yli__chk += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(yli__chk, df.columns,
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
    nhc__mhj = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    knxq__taxp = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', nhc__mhj, knxq__taxp,
        package_name='pandas', module_name='DataFrame')
    kfyo__zfygi = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            see__spno = kfyo__zfygi + '\n'
            see__spno += 'Index: 0 entries\n'
            see__spno += 'Empty DataFrame'
            print(see__spno)
        return _info_impl
    else:
        yli__chk = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        yli__chk += '    ncols = df.shape[1]\n'
        yli__chk += f'    lines = "{kfyo__zfygi}\\n"\n'
        yli__chk += f'    lines += "{df.index}: "\n'
        yli__chk += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            yli__chk += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            yli__chk += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            yli__chk += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        yli__chk += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        yli__chk += f'    space = {max(len(str(k)) for k in df.columns) + 1}\n'
        yli__chk += '    column_width = max(space, 7)\n'
        yli__chk += '    column= "Column"\n'
        yli__chk += '    underl= "------"\n'
        yli__chk += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        yli__chk += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        yli__chk += '    mem_size = 0\n'
        yli__chk += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        yli__chk += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        yli__chk += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        lkhwc__klmm = dict()
        for i in range(len(df.columns)):
            yli__chk += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            zavb__lbhm = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                zavb__lbhm = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                swt__hmj = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                zavb__lbhm = f'{swt__hmj[:-7]}'
            yli__chk += f'    col_dtype[{i}] = "{zavb__lbhm}"\n'
            if zavb__lbhm in lkhwc__klmm:
                lkhwc__klmm[zavb__lbhm] += 1
            else:
                lkhwc__klmm[zavb__lbhm] = 1
            yli__chk += f'    col_name[{i}] = "{df.columns[i]}"\n'
            yli__chk += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        yli__chk += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        yli__chk += '    for i in column_info:\n'
        yli__chk += "        lines += f'{i}\\n'\n"
        cjm__zlgrq = ', '.join(f'{k}({lkhwc__klmm[k]})' for k in sorted(
            lkhwc__klmm))
        yli__chk += f"    lines += 'dtypes: {cjm__zlgrq}\\n'\n"
        yli__chk += '    mem_size += df.index.nbytes\n'
        yli__chk += '    total_size = _sizeof_fmt(mem_size)\n'
        yli__chk += "    lines += f'memory usage: {total_size}'\n"
        yli__chk += '    print(lines)\n'
        admw__egsmy = {}
        exec(yli__chk, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo': bodo,
            'np': np}, admw__egsmy)
        _info_impl = admw__egsmy['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    yli__chk = 'def impl(df, index=True, deep=False):\n'
    vkyu__gnz = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes'
    wte__njug = is_overload_true(index)
    columns = df.columns
    if wte__njug:
        columns = ('Index',) + columns
    if len(columns) == 0:
        dbc__cina = ()
    elif all(isinstance(vryey__lyp, int) for vryey__lyp in columns):
        dbc__cina = np.array(columns, 'int64')
    elif all(isinstance(vryey__lyp, str) for vryey__lyp in columns):
        dbc__cina = pd.array(columns, 'string')
    else:
        dbc__cina = columns
    if df.is_table_format:
        tvaf__gxyx = int(wte__njug)
        ppu__qsgr = len(columns)
        yli__chk += f'  nbytes_arr = np.empty({ppu__qsgr}, np.int64)\n'
        yli__chk += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        yli__chk += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {tvaf__gxyx})
"""
        if wte__njug:
            yli__chk += f'  nbytes_arr[0] = {vkyu__gnz}\n'
        yli__chk += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if wte__njug:
            data = f'{vkyu__gnz},{data}'
        else:
            bpcb__qyek = ',' if len(columns) == 1 else ''
            data = f'{data}{bpcb__qyek}'
        yli__chk += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        dbc__cina}, admw__egsmy)
    impl = admw__egsmy['impl']
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
    rdla__hmt = 'read_excel_df{}'.format(next_label())
    setattr(types, rdla__hmt, df_type)
    jvrc__hee = False
    if is_overload_constant_list(parse_dates):
        jvrc__hee = get_overload_const_list(parse_dates)
    sccoh__dsru = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    yli__chk = f"""
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
    with numba.objmode(df="{rdla__hmt}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{sccoh__dsru}}},
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
            parse_dates={jvrc__hee},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    admw__egsmy = {}
    exec(yli__chk, globals(), admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as hedr__hpqa:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    yli__chk = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    yli__chk += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    yli__chk += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        yli__chk += '   fig, ax = plt.subplots()\n'
    else:
        yli__chk += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        yli__chk += '   fig.set_figwidth(figsize[0])\n'
        yli__chk += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        yli__chk += '   xlabel = x\n'
    yli__chk += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        yli__chk += '   ylabel = y\n'
    else:
        yli__chk += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        yli__chk += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        yli__chk += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    yli__chk += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            yli__chk += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            aznjf__fqcx = get_overload_const_str(x)
            ffj__zjw = df.columns.index(aznjf__fqcx)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if ffj__zjw != i:
                        yli__chk += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            yli__chk += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        yli__chk += '   ax.scatter(df[x], df[y], s=20)\n'
        yli__chk += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        yli__chk += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        yli__chk += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        yli__chk += '   ax.legend()\n'
    yli__chk += '   return ax\n'
    admw__egsmy = {}
    exec(yli__chk, {'bodo': bodo, 'plt': plt}, admw__egsmy)
    impl = admw__egsmy['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for fbuna__yvc in df_typ.data:
        if not (isinstance(fbuna__yvc, IntegerArrayType) or isinstance(
            fbuna__yvc.dtype, types.Number) or fbuna__yvc.dtype in (bodo.
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
        hjp__svfse = args[0]
        kxix__qeok = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        uuqt__ifuf = hjp__svfse
        check_runtime_cols_unsupported(hjp__svfse, 'set_df_col()')
        if isinstance(hjp__svfse, DataFrameType):
            index = hjp__svfse.index
            if len(hjp__svfse.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(hjp__svfse.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if kxix__qeok in hjp__svfse.columns:
                kci__sexai = hjp__svfse.columns
                kfilg__qlzf = hjp__svfse.columns.index(kxix__qeok)
                bgyh__xqob = list(hjp__svfse.data)
                bgyh__xqob[kfilg__qlzf] = val
                bgyh__xqob = tuple(bgyh__xqob)
            else:
                kci__sexai = hjp__svfse.columns + (kxix__qeok,)
                bgyh__xqob = hjp__svfse.data + (val,)
            uuqt__ifuf = DataFrameType(bgyh__xqob, index, kci__sexai,
                hjp__svfse.dist, hjp__svfse.is_table_format)
        return uuqt__ifuf(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    mhrl__vdo = {}

    def _rewrite_membership_op(self, node, left, right):
        cssme__kxhwo = node.op
        op = self.visit(cssme__kxhwo)
        return op, cssme__kxhwo, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    lwn__lvu = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in lwn__lvu:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in lwn__lvu:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        qrrmu__wuwpu = node.attr
        value = node.value
        uxd__wbzro = pd.core.computation.ops.LOCAL_TAG
        if qrrmu__wuwpu in ('str', 'dt'):
            try:
                nvrqp__zmwt = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as slse__mkpqu:
                col_name = slse__mkpqu.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            nvrqp__zmwt = str(self.visit(value))
        ypim__vdgux = nvrqp__zmwt, qrrmu__wuwpu
        if ypim__vdgux in join_cleaned_cols:
            qrrmu__wuwpu = join_cleaned_cols[ypim__vdgux]
        name = nvrqp__zmwt + '.' + qrrmu__wuwpu
        if name.startswith(uxd__wbzro):
            name = name[len(uxd__wbzro):]
        if qrrmu__wuwpu in ('str', 'dt'):
            rnaw__lfwv = columns[cleaned_columns.index(nvrqp__zmwt)]
            mhrl__vdo[rnaw__lfwv] = nvrqp__zmwt
            self.env.scope[name] = 0
            return self.term_type(uxd__wbzro + name, self.env)
        lwn__lvu.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in lwn__lvu:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        ehyt__wbmgm = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        kxix__qeok = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(ehyt__wbmgm), kxix__qeok))

    def op__str__(self):
        cznwp__uoba = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            oftyf__gmpyg)) for oftyf__gmpyg in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(cznwp__uoba)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(cznwp__uoba)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(cznwp__uoba))
    upf__rnrh = pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op
    qyie__mxz = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    cvxet__hea = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    iaba__tcsbu = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    xsioe__iws = pd.core.computation.ops.Term.__str__
    zsc__ynyx = pd.core.computation.ops.MathCall.__str__
    ypkk__okp = pd.core.computation.ops.Op.__str__
    ugnji__orem = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        uacg__zzsjd = pd.core.computation.expr.Expr(expr, env=env)
        ddm__zndp = str(uacg__zzsjd)
    except pd.core.computation.ops.UndefinedVariableError as slse__mkpqu:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == slse__mkpqu.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {slse__mkpqu}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            upf__rnrh)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            qyie__mxz)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = cvxet__hea
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = iaba__tcsbu
        pd.core.computation.ops.Term.__str__ = xsioe__iws
        pd.core.computation.ops.MathCall.__str__ = zsc__ynyx
        pd.core.computation.ops.Op.__str__ = ypkk__okp
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            ugnji__orem)
    pyajs__miunt = pd.core.computation.parsing.clean_column_name
    mhrl__vdo.update({vryey__lyp: pyajs__miunt(vryey__lyp) for vryey__lyp in
        columns if pyajs__miunt(vryey__lyp) in uacg__zzsjd.names})
    return uacg__zzsjd, ddm__zndp, mhrl__vdo


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        nmce__apal = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(nmce__apal))
        omeet__viqj = namedtuple('Pandas', col_names)
        yteqj__zklo = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], omeet__viqj)
        super(DataFrameTupleIterator, self).__init__(name, yteqj__zklo)

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
        ekz__zts = [if_series_to_array_type(a) for a in args[len(args) // 2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        ekz__zts = [types.Array(types.int64, 1, 'C')] + ekz__zts
        xog__sgi = DataFrameTupleIterator(col_names, ekz__zts)
        return xog__sgi(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wnl__hkod = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            wnl__hkod)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    hxu__gjzj = args[len(args) // 2:]
    azlnw__dghax = sig.args[len(sig.args) // 2:]
    aponb__ztyok = context.make_helper(builder, sig.return_type)
    nkaw__hnn = context.get_constant(types.intp, 0)
    hssbc__opgm = cgutils.alloca_once_value(builder, nkaw__hnn)
    aponb__ztyok.index = hssbc__opgm
    for i, arr in enumerate(hxu__gjzj):
        setattr(aponb__ztyok, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(hxu__gjzj, azlnw__dghax):
        context.nrt.incref(builder, arr_typ, arr)
    res = aponb__ztyok._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    pgd__cxhpe, = sig.args
    lbdwv__wvwe, = args
    aponb__ztyok = context.make_helper(builder, pgd__cxhpe, value=lbdwv__wvwe)
    cve__oyro = signature(types.intp, pgd__cxhpe.array_types[1])
    gkj__fugti = context.compile_internal(builder, lambda a: len(a),
        cve__oyro, [aponb__ztyok.array0])
    index = builder.load(aponb__ztyok.index)
    whnso__jdm = builder.icmp_signed('<', index, gkj__fugti)
    result.set_valid(whnso__jdm)
    with builder.if_then(whnso__jdm):
        values = [index]
        for i, arr_typ in enumerate(pgd__cxhpe.array_types[1:]):
            xnjmm__zyej = getattr(aponb__ztyok, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                hcdlv__fwed = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    hcdlv__fwed, [xnjmm__zyej, index])
            else:
                hcdlv__fwed = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    hcdlv__fwed, [xnjmm__zyej, index])
            values.append(val)
        value = context.make_tuple(builder, pgd__cxhpe.yield_type, values)
        result.yield_(value)
        vad__hfsk = cgutils.increment_index(builder, index)
        builder.store(vad__hfsk, aponb__ztyok.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    dpeuv__bwxqb = ir.Assign(rhs, lhs, expr.loc)
    zrvok__nob = lhs
    puo__rqx = []
    vke__esdhb = []
    jzhp__ulk = typ.count
    for i in range(jzhp__ulk):
        zwtol__ioy = ir.Var(zrvok__nob.scope, mk_unique_var('{}_size{}'.
            format(zrvok__nob.name, i)), zrvok__nob.loc)
        hmzj__npet = ir.Expr.static_getitem(lhs, i, None, zrvok__nob.loc)
        self.calltypes[hmzj__npet] = None
        puo__rqx.append(ir.Assign(hmzj__npet, zwtol__ioy, zrvok__nob.loc))
        self._define(equiv_set, zwtol__ioy, types.intp, hmzj__npet)
        vke__esdhb.append(zwtol__ioy)
    trqzq__zbrwf = tuple(vke__esdhb)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        trqzq__zbrwf, pre=[dpeuv__bwxqb] + puo__rqx)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
