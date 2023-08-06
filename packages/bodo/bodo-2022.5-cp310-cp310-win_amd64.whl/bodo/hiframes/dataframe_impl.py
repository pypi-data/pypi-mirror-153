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
        afri__peg = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({afri__peg})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    guyvy__qzht = 'def impl(df):\n'
    if df.has_runtime_cols:
        guyvy__qzht += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        yut__sxet = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        guyvy__qzht += f'  return {yut__sxet}'
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo}, atun__ozaq)
    impl = atun__ozaq['impl']
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
    vyg__ikef = len(df.columns)
    eqwg__wpv = set(i for i in range(vyg__ikef) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in eqwg__wpv else '') for i in
        range(vyg__ikef))
    guyvy__qzht = 'def f(df):\n'.format()
    guyvy__qzht += '    return np.stack(({},), 1)\n'.format(data_args)
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'np': np}, atun__ozaq)
    daq__blpd = atun__ozaq['f']
    return daq__blpd


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
    jdvgy__ikglc = {'dtype': dtype, 'na_value': na_value}
    bgsse__pcc = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', jdvgy__ikglc, bgsse__pcc,
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
            awagh__wihm = bodo.hiframes.table.compute_num_runtime_columns(t)
            return awagh__wihm * len(t)
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
            awagh__wihm = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), awagh__wihm
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    guyvy__qzht = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    ppr__yqi = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    guyvy__qzht += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{ppr__yqi}), {index}, None)
"""
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo}, atun__ozaq)
    impl = atun__ozaq['impl']
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
    jdvgy__ikglc = {'copy': copy, 'errors': errors}
    bgsse__pcc = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', jdvgy__ikglc, bgsse__pcc,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        oqk__zgj = _bodo_object_typeref.instance_type
        assert isinstance(oqk__zgj, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        oxo__gzigs = {}
        for i, name in enumerate(oqk__zgj.columns):
            arr_typ = oqk__zgj.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                vkwqs__ssmq = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                vkwqs__ssmq = boolean_dtype
            else:
                vkwqs__ssmq = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = vkwqs__ssmq
            oxo__gzigs[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {oxo__gzigs[bha__lhf]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if bha__lhf in oxo__gzigs else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, bha__lhf in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        sqii__ahsh = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(sqii__ahsh[bha__lhf])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if bha__lhf in sqii__ahsh else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, bha__lhf in enumerate(df.columns))
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
        qcm__cxzg = types.none
        extra_globals = {'output_arr_typ': qcm__cxzg}
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
        dfmmk__qoaf = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                dfmmk__qoaf.append(arr + '.copy()')
            elif is_overload_false(deep):
                dfmmk__qoaf.append(arr)
            else:
                dfmmk__qoaf.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(dfmmk__qoaf)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    jdvgy__ikglc = {'index': index, 'level': level, 'errors': errors}
    bgsse__pcc = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', jdvgy__ikglc, bgsse__pcc,
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
        lokm__xwpn = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        lokm__xwpn = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    pjq__dejsx = tuple([lokm__xwpn.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        out_df_type = df.copy(columns=pjq__dejsx)
        qcm__cxzg = types.none
        extra_globals = {'output_arr_typ': qcm__cxzg}
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
        dfmmk__qoaf = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                dfmmk__qoaf.append(arr + '.copy()')
            elif is_overload_false(copy):
                dfmmk__qoaf.append(arr)
            else:
                dfmmk__qoaf.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(dfmmk__qoaf)
    return _gen_init_df(header, pjq__dejsx, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    ubcq__zqutu = not is_overload_none(items)
    tlpt__ksop = not is_overload_none(like)
    tugox__nhrv = not is_overload_none(regex)
    hrp__wzb = ubcq__zqutu ^ tlpt__ksop ^ tugox__nhrv
    esjex__xpac = not (ubcq__zqutu or tlpt__ksop or tugox__nhrv)
    if esjex__xpac:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not hrp__wzb:
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
        mzyil__knzbx = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        mzyil__knzbx = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert mzyil__knzbx in {0, 1}
    guyvy__qzht = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if mzyil__knzbx == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if mzyil__knzbx == 1:
        ysa__thfp = []
        rph__ykvm = []
        blfw__vray = []
        if ubcq__zqutu:
            if is_overload_constant_list(items):
                knapn__nsb = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if tlpt__ksop:
            if is_overload_constant_str(like):
                umifq__xzitf = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if tugox__nhrv:
            if is_overload_constant_str(regex):
                xtzvi__tobcg = get_overload_const_str(regex)
                gfnh__vaiwd = re.compile(xtzvi__tobcg)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, bha__lhf in enumerate(df.columns):
            if not is_overload_none(items
                ) and bha__lhf in knapn__nsb or not is_overload_none(like
                ) and umifq__xzitf in str(bha__lhf) or not is_overload_none(
                regex) and gfnh__vaiwd.search(str(bha__lhf)):
                rph__ykvm.append(bha__lhf)
                blfw__vray.append(i)
        for i in blfw__vray:
            var_name = f'data_{i}'
            ysa__thfp.append(var_name)
            guyvy__qzht += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(ysa__thfp)
        return _gen_init_df(guyvy__qzht, rph__ykvm, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        qcm__cxzg = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([qcm__cxzg] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': qcm__cxzg}
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
    dwyy__ygz = is_overload_none(include)
    uxwi__lkg = is_overload_none(exclude)
    tbvuz__bnzh = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if dwyy__ygz and uxwi__lkg:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not dwyy__ygz:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            bokk__gdxs = [dtype_to_array_type(parse_dtype(elem, tbvuz__bnzh
                )) for elem in include]
        elif is_legal_input(include):
            bokk__gdxs = [dtype_to_array_type(parse_dtype(include,
                tbvuz__bnzh))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        bokk__gdxs = get_nullable_and_non_nullable_types(bokk__gdxs)
        nahzt__nlm = tuple(bha__lhf for i, bha__lhf in enumerate(df.columns
            ) if df.data[i] in bokk__gdxs)
    else:
        nahzt__nlm = df.columns
    if not uxwi__lkg:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            furc__hmbn = [dtype_to_array_type(parse_dtype(elem, tbvuz__bnzh
                )) for elem in exclude]
        elif is_legal_input(exclude):
            furc__hmbn = [dtype_to_array_type(parse_dtype(exclude,
                tbvuz__bnzh))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        furc__hmbn = get_nullable_and_non_nullable_types(furc__hmbn)
        nahzt__nlm = tuple(bha__lhf for bha__lhf in nahzt__nlm if df.data[
            df.column_index[bha__lhf]] not in furc__hmbn)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bha__lhf]})'
         for bha__lhf in nahzt__nlm)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, nahzt__nlm, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        qcm__cxzg = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([qcm__cxzg] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': qcm__cxzg}
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
    tyyk__fkfi = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in tyyk__fkfi:
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
    tyyk__fkfi = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in tyyk__fkfi:
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
    guyvy__qzht = 'def impl(df, values):\n'
    lan__vwh = {}
    rkt__prb = False
    if isinstance(values, DataFrameType):
        rkt__prb = True
        for i, bha__lhf in enumerate(df.columns):
            if bha__lhf in values.column_index:
                ekf__hvofe = 'val{}'.format(i)
                guyvy__qzht += f"""  {ekf__hvofe} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[bha__lhf]})
"""
                lan__vwh[bha__lhf] = ekf__hvofe
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        lan__vwh = {bha__lhf: 'values' for bha__lhf in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        ekf__hvofe = 'data{}'.format(i)
        guyvy__qzht += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(ekf__hvofe, i))
        data.append(ekf__hvofe)
    aeb__uubw = ['out{}'.format(i) for i in range(len(df.columns))]
    ayeip__znk = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    fbpfh__wxo = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    xzlza__asymu = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, jynw__semye) in enumerate(zip(df.columns, data)):
        if cname in lan__vwh:
            oiyd__xrkk = lan__vwh[cname]
            if rkt__prb:
                guyvy__qzht += ayeip__znk.format(jynw__semye, oiyd__xrkk,
                    aeb__uubw[i])
            else:
                guyvy__qzht += fbpfh__wxo.format(jynw__semye, oiyd__xrkk,
                    aeb__uubw[i])
        else:
            guyvy__qzht += xzlza__asymu.format(aeb__uubw[i])
    return _gen_init_df(guyvy__qzht, df.columns, ','.join(aeb__uubw))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    vyg__ikef = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(vyg__ikef))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    yhnk__uwg = [bha__lhf for bha__lhf, zum__ypiin in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(zum__ypiin.dtype)]
    assert len(yhnk__uwg) != 0
    kfh__vjg = ''
    if not any(zum__ypiin == types.float64 for zum__ypiin in df.data):
        kfh__vjg = '.astype(np.float64)'
    fle__kqpp = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[bha__lhf], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[bha__lhf]], IntegerArrayType) or
        df.data[df.column_index[bha__lhf]] == boolean_array else '') for
        bha__lhf in yhnk__uwg)
    yxak__lcdz = 'np.stack(({},), 1){}'.format(fle__kqpp, kfh__vjg)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(yhnk__uwg)))
    index = f'{generate_col_to_index_func_text(yhnk__uwg)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(yxak__lcdz)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, yhnk__uwg, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    brjx__hym = dict(ddof=ddof)
    dgoy__xcv = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    ciem__mzq = '1' if is_overload_none(min_periods) else 'min_periods'
    yhnk__uwg = [bha__lhf for bha__lhf, zum__ypiin in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(zum__ypiin.dtype)]
    if len(yhnk__uwg) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    kfh__vjg = ''
    if not any(zum__ypiin == types.float64 for zum__ypiin in df.data):
        kfh__vjg = '.astype(np.float64)'
    fle__kqpp = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[bha__lhf], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[bha__lhf]], IntegerArrayType) or
        df.data[df.column_index[bha__lhf]] == boolean_array else '') for
        bha__lhf in yhnk__uwg)
    yxak__lcdz = 'np.stack(({},), 1){}'.format(fle__kqpp, kfh__vjg)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(yhnk__uwg)))
    index = f'pd.Index({yhnk__uwg})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(yxak__lcdz)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        ciem__mzq)
    return _gen_init_df(header, yhnk__uwg, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    brjx__hym = dict(axis=axis, level=level, numeric_only=numeric_only)
    dgoy__xcv = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    guyvy__qzht = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    guyvy__qzht += '  data = np.array([{}])\n'.format(data_args)
    yut__sxet = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    guyvy__qzht += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {yut__sxet})\n'
        )
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'np': np}, atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    brjx__hym = dict(axis=axis)
    dgoy__xcv = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    guyvy__qzht = 'def impl(df, axis=0, dropna=True):\n'
    guyvy__qzht += '  data = np.asarray(({},))\n'.format(data_args)
    yut__sxet = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    guyvy__qzht += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {yut__sxet})\n'
        )
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'np': np}, atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    brjx__hym = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    dgoy__xcv = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    brjx__hym = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    dgoy__xcv = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    brjx__hym = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dgoy__xcv = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    brjx__hym = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dgoy__xcv = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    brjx__hym = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dgoy__xcv = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    brjx__hym = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    dgoy__xcv = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    brjx__hym = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    dgoy__xcv = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    brjx__hym = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dgoy__xcv = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    brjx__hym = dict(numeric_only=numeric_only, interpolation=interpolation)
    dgoy__xcv = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    brjx__hym = dict(axis=axis, skipna=skipna)
    dgoy__xcv = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for ehndb__nfl in df.data:
        if not (bodo.utils.utils.is_np_array_typ(ehndb__nfl) and (
            ehndb__nfl.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(ehndb__nfl.dtype, (types.Number, types.Boolean))) or
            isinstance(ehndb__nfl, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or ehndb__nfl in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {ehndb__nfl} not supported.'
                )
        if isinstance(ehndb__nfl, bodo.CategoricalArrayType
            ) and not ehndb__nfl.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    brjx__hym = dict(axis=axis, skipna=skipna)
    dgoy__xcv = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for ehndb__nfl in df.data:
        if not (bodo.utils.utils.is_np_array_typ(ehndb__nfl) and (
            ehndb__nfl.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(ehndb__nfl.dtype, (types.Number, types.Boolean))) or
            isinstance(ehndb__nfl, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or ehndb__nfl in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {ehndb__nfl} not supported.'
                )
        if isinstance(ehndb__nfl, bodo.CategoricalArrayType
            ) and not ehndb__nfl.dtype.ordered:
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
        yhnk__uwg = tuple(bha__lhf for bha__lhf, zum__ypiin in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (zum__ypiin.dtype))
        out_colnames = yhnk__uwg
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            ucw__dxlqt = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[bha__lhf]].dtype) for bha__lhf in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(ucw__dxlqt, []))
    except NotImplementedError as yfvfk__bdcwj:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    nftc__jsph = ''
    if func_name in ('sum', 'prod'):
        nftc__jsph = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    guyvy__qzht = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, nftc__jsph))
    if func_name == 'quantile':
        guyvy__qzht = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        guyvy__qzht = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        guyvy__qzht += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        guyvy__qzht += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    yuca__qkuic = ''
    if func_name in ('min', 'max'):
        yuca__qkuic = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        yuca__qkuic = ', dtype=np.float32'
    jfyq__jec = f'bodo.libs.array_ops.array_op_{func_name}'
    vmg__ykztu = ''
    if func_name in ['sum', 'prod']:
        vmg__ykztu = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        vmg__ykztu = 'index'
    elif func_name == 'quantile':
        vmg__ykztu = 'q'
    elif func_name in ['std', 'var']:
        vmg__ykztu = 'True, ddof'
    elif func_name == 'median':
        vmg__ykztu = 'True'
    data_args = ', '.join(
        f'{jfyq__jec}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bha__lhf]}), {vmg__ykztu})'
         for bha__lhf in out_colnames)
    guyvy__qzht = ''
    if func_name in ('idxmax', 'idxmin'):
        guyvy__qzht += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        guyvy__qzht += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        guyvy__qzht += '  data = np.asarray(({},){})\n'.format(data_args,
            yuca__qkuic)
    guyvy__qzht += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return guyvy__qzht


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    xugz__mkg = [df_type.column_index[bha__lhf] for bha__lhf in out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in xugz__mkg)
    tdgbx__oqmg = '\n        '.join(f'row[{i}] = arr_{xugz__mkg[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    ehs__hsns = f'len(arr_{xugz__mkg[0]})'
    qqw__pkug = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in qqw__pkug:
        aqpij__khn = qqw__pkug[func_name]
        ziupb__odr = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        guyvy__qzht = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {ehs__hsns}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{ziupb__odr})
    for i in numba.parfors.parfor.internal_prange(n):
        {tdgbx__oqmg}
        A[i] = {aqpij__khn}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return guyvy__qzht
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    brjx__hym = dict(fill_method=fill_method, limit=limit, freq=freq)
    dgoy__xcv = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', brjx__hym, dgoy__xcv,
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
    brjx__hym = dict(axis=axis, skipna=skipna)
    dgoy__xcv = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', brjx__hym, dgoy__xcv,
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
    brjx__hym = dict(skipna=skipna)
    dgoy__xcv = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', brjx__hym, dgoy__xcv,
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
    brjx__hym = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    dgoy__xcv = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    yhnk__uwg = [bha__lhf for bha__lhf, zum__ypiin in zip(df.columns, df.
        data) if _is_describe_type(zum__ypiin)]
    if len(yhnk__uwg) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    zmd__frn = sum(df.data[df.column_index[bha__lhf]].dtype == bodo.
        datetime64ns for bha__lhf in yhnk__uwg)

    def _get_describe(col_ind):
        layps__yfbo = df.data[col_ind].dtype == bodo.datetime64ns
        if zmd__frn and zmd__frn != len(yhnk__uwg):
            if layps__yfbo:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for bha__lhf in yhnk__uwg:
        col_ind = df.column_index[bha__lhf]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[bha__lhf]) for
        bha__lhf in yhnk__uwg)
    uqce__daono = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if zmd__frn == len(yhnk__uwg):
        uqce__daono = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif zmd__frn:
        uqce__daono = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({uqce__daono})'
    return _gen_init_df(header, yhnk__uwg, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    brjx__hym = dict(axis=axis, convert=convert, is_copy=is_copy)
    dgoy__xcv = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', brjx__hym, dgoy__xcv,
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
    brjx__hym = dict(freq=freq, axis=axis, fill_value=fill_value)
    dgoy__xcv = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for wef__jmbr in df.data:
        if not is_supported_shift_array_type(wef__jmbr):
            raise BodoError(
                f'Dataframe.shift() column input type {wef__jmbr.dtype} not supported yet.'
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
    brjx__hym = dict(axis=axis)
    dgoy__xcv = dict(axis=0)
    check_unsupported_args('DataFrame.diff', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for wef__jmbr in df.data:
        if not (isinstance(wef__jmbr, types.Array) and (isinstance(
            wef__jmbr.dtype, types.Number) or wef__jmbr.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {wef__jmbr.dtype} not supported.'
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
    tul__wlj = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(tul__wlj)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        vprju__pnps = get_overload_const_list(column)
    else:
        vprju__pnps = [get_literal_value(column)]
    ubt__cpym = [df.column_index[bha__lhf] for bha__lhf in vprju__pnps]
    for i in ubt__cpym:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{ubt__cpym[0]})\n'
        )
    for i in range(n):
        if i in ubt__cpym:
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
    jdvgy__ikglc = {'inplace': inplace, 'append': append,
        'verify_integrity': verify_integrity}
    bgsse__pcc = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', jdvgy__ikglc, bgsse__pcc,
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
    columns = tuple(bha__lhf for bha__lhf in df.columns if bha__lhf != col_name
        )
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    jdvgy__ikglc = {'inplace': inplace}
    bgsse__pcc = {'inplace': False}
    check_unsupported_args('query', jdvgy__ikglc, bgsse__pcc, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        brm__qzj = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[brm__qzj]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    jdvgy__ikglc = {'subset': subset, 'keep': keep}
    bgsse__pcc = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', jdvgy__ikglc, bgsse__pcc,
        package_name='pandas', module_name='DataFrame')
    vyg__ikef = len(df.columns)
    guyvy__qzht = "def impl(df, subset=None, keep='first'):\n"
    for i in range(vyg__ikef):
        guyvy__qzht += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    xvoh__fjg = ', '.join(f'data_{i}' for i in range(vyg__ikef))
    xvoh__fjg += ',' if vyg__ikef == 1 else ''
    guyvy__qzht += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({xvoh__fjg}))\n')
    guyvy__qzht += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    guyvy__qzht += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo}, atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    jdvgy__ikglc = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    bgsse__pcc = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    eec__trv = []
    if is_overload_constant_list(subset):
        eec__trv = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        eec__trv = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        eec__trv = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    oqrg__ywci = []
    for col_name in eec__trv:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        oqrg__ywci.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', jdvgy__ikglc,
        bgsse__pcc, package_name='pandas', module_name='DataFrame')
    ulajr__gubv = []
    if oqrg__ywci:
        for stwu__ondk in oqrg__ywci:
            if isinstance(df.data[stwu__ondk], bodo.MapArrayType):
                ulajr__gubv.append(df.columns[stwu__ondk])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                ulajr__gubv.append(col_name)
    if ulajr__gubv:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {ulajr__gubv} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    vyg__ikef = len(df.columns)
    siy__qaen = ['data_{}'.format(i) for i in oqrg__ywci]
    bxf__tebdh = ['data_{}'.format(i) for i in range(vyg__ikef) if i not in
        oqrg__ywci]
    if siy__qaen:
        honzg__bjy = len(siy__qaen)
    else:
        honzg__bjy = vyg__ikef
    hre__lhhbi = ', '.join(siy__qaen + bxf__tebdh)
    data_args = ', '.join('data_{}'.format(i) for i in range(vyg__ikef))
    guyvy__qzht = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(vyg__ikef):
        guyvy__qzht += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    guyvy__qzht += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(hre__lhhbi, index, honzg__bjy))
    guyvy__qzht += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(guyvy__qzht, df.columns, data_args, 'index')


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
            wecm__iyl = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                wecm__iyl = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                wecm__iyl = lambda i: f'other[:,{i}]'
        vyg__ikef = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {wecm__iyl(i)})'
             for i in range(vyg__ikef))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        pbhzl__mfvec = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(
            pbhzl__mfvec)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    brjx__hym = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    dgoy__xcv = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', brjx__hym, dgoy__xcv,
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
    vyg__ikef = len(df.columns)
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
        for i in range(vyg__ikef):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other.column_index[df
                    .columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(vyg__ikef):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(vyg__ikef):
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
        dne__zybi = 'out_df_type'
    else:
        dne__zybi = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    guyvy__qzht = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {dne__zybi})
"""
    atun__ozaq = {}
    oilto__upjg = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    oilto__upjg.update(extra_globals)
    exec(guyvy__qzht, oilto__upjg, atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        wwu__xuc = pd.Index(lhs.columns)
        uipfi__vplt = pd.Index(rhs.columns)
        yxkiv__jbse, ugvmz__szzl, ifx__xxk = wwu__xuc.join(uipfi__vplt, how
            ='left' if is_inplace else 'outer', level=None, return_indexers
            =True)
        return tuple(yxkiv__jbse), ugvmz__szzl, ifx__xxk
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        vke__bkg = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        zef__xes = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, vke__bkg)
        check_runtime_cols_unsupported(rhs, vke__bkg)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                yxkiv__jbse, ugvmz__szzl, ifx__xxk = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {uhkvf__ooa}) {vke__bkg}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {infe__edqy})'
                     if uhkvf__ooa != -1 and infe__edqy != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for uhkvf__ooa, infe__edqy in zip(ugvmz__szzl, ifx__xxk))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, yxkiv__jbse, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            zjva__dyai = []
            puzq__ndk = []
            if op in zef__xes:
                for i, dpn__hmi in enumerate(lhs.data):
                    if is_common_scalar_dtype([dpn__hmi.dtype, rhs]):
                        zjva__dyai.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {vke__bkg} rhs'
                            )
                    else:
                        nranr__bqhz = f'arr{i}'
                        puzq__ndk.append(nranr__bqhz)
                        zjva__dyai.append(nranr__bqhz)
                data_args = ', '.join(zjva__dyai)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {vke__bkg} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(puzq__ndk) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {nranr__bqhz} = np.empty(n, dtype=np.bool_)\n' for
                    nranr__bqhz in puzq__ndk)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(nranr__bqhz, 
                    op == operator.ne) for nranr__bqhz in puzq__ndk)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            zjva__dyai = []
            puzq__ndk = []
            if op in zef__xes:
                for i, dpn__hmi in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, dpn__hmi.dtype]):
                        zjva__dyai.append(
                            f'lhs {vke__bkg} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        nranr__bqhz = f'arr{i}'
                        puzq__ndk.append(nranr__bqhz)
                        zjva__dyai.append(nranr__bqhz)
                data_args = ', '.join(zjva__dyai)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, vke__bkg) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(puzq__ndk) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(nranr__bqhz) for nranr__bqhz in puzq__ndk)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(nranr__bqhz, 
                    op == operator.ne) for nranr__bqhz in puzq__ndk)
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
        pbhzl__mfvec = create_binary_op_overload(op)
        overload(op)(pbhzl__mfvec)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        vke__bkg = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, vke__bkg)
        check_runtime_cols_unsupported(right, vke__bkg)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                yxkiv__jbse, _, ifx__xxk = _get_binop_columns(left, right, True
                    )
                guyvy__qzht = 'def impl(left, right):\n'
                for i, infe__edqy in enumerate(ifx__xxk):
                    if infe__edqy == -1:
                        guyvy__qzht += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    guyvy__qzht += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    guyvy__qzht += f"""  df_arr{i} {vke__bkg} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {infe__edqy})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    yxkiv__jbse)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(guyvy__qzht, yxkiv__jbse, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            guyvy__qzht = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                guyvy__qzht += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                guyvy__qzht += '  df_arr{0} {1} right\n'.format(i, vke__bkg)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(guyvy__qzht, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        pbhzl__mfvec = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(pbhzl__mfvec)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            vke__bkg = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, vke__bkg)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, vke__bkg) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        pbhzl__mfvec = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(pbhzl__mfvec)


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
            zmqfu__ygyc = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                zmqfu__ygyc[i] = bodo.libs.array_kernels.isna(obj, i)
            return zmqfu__ygyc
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
            zmqfu__ygyc = np.empty(n, np.bool_)
            for i in range(n):
                zmqfu__ygyc[i] = pd.isna(obj[i])
            return zmqfu__ygyc
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
    jdvgy__ikglc = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    bgsse__pcc = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', jdvgy__ikglc, bgsse__pcc,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    szh__kyb = str(expr_node)
    return szh__kyb.startswith('left.') or szh__kyb.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    mqiq__vbu = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (mqiq__vbu,))
    bwzr__slzgw = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        gbvu__zygk = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        iccd__evioj = {('NOT_NA', bwzr__slzgw(dpn__hmi)): dpn__hmi for
            dpn__hmi in null_set}
        eunhf__stdz, _, _ = _parse_query_expr(gbvu__zygk, env, [], [], None,
            join_cleaned_cols=iccd__evioj)
        dbf__itue = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            kovia__kap = pd.core.computation.ops.BinOp('&', eunhf__stdz,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = dbf__itue
        return kovia__kap

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                yycjh__nno = set()
                rqbxs__memw = set()
                quumm__sjtt = _insert_NA_cond_body(expr_node.lhs, yycjh__nno)
                vjrrl__lnjgj = _insert_NA_cond_body(expr_node.rhs, rqbxs__memw)
                alf__ddtk = yycjh__nno.intersection(rqbxs__memw)
                yycjh__nno.difference_update(alf__ddtk)
                rqbxs__memw.difference_update(alf__ddtk)
                null_set.update(alf__ddtk)
                expr_node.lhs = append_null_checks(quumm__sjtt, yycjh__nno)
                expr_node.rhs = append_null_checks(vjrrl__lnjgj, rqbxs__memw)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            ytjj__exmzi = expr_node.name
            lzxv__omod, col_name = ytjj__exmzi.split('.')
            if lzxv__omod == 'left':
                utqb__jbyv = left_columns
                data = left_data
            else:
                utqb__jbyv = right_columns
                data = right_data
            gsgvy__rqfbd = data[utqb__jbyv.index(col_name)]
            if bodo.utils.typing.is_nullable(gsgvy__rqfbd):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    yfoxh__ggs = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        pasng__zlt = str(expr_node.lhs)
        srd__lhbdz = str(expr_node.rhs)
        if pasng__zlt.startswith('left.') and srd__lhbdz.startswith('left.'
            ) or pasng__zlt.startswith('right.') and srd__lhbdz.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [pasng__zlt.split('.')[1]]
        right_on = [srd__lhbdz.split('.')[1]]
        if pasng__zlt.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        czv__elwu, ecyp__hyu, yac__qqo = _extract_equal_conds(expr_node.lhs)
        mckuu__loke, qxavc__qhwd, jyscj__xnga = _extract_equal_conds(expr_node
            .rhs)
        left_on = czv__elwu + mckuu__loke
        right_on = ecyp__hyu + qxavc__qhwd
        if yac__qqo is None:
            return left_on, right_on, jyscj__xnga
        if jyscj__xnga is None:
            return left_on, right_on, yac__qqo
        expr_node.lhs = yac__qqo
        expr_node.rhs = jyscj__xnga
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    mqiq__vbu = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (mqiq__vbu,))
    lokm__xwpn = dict()
    bwzr__slzgw = pd.core.computation.parsing.clean_column_name
    for name, fsmv__kwjm in (('left', left_columns), ('right', right_columns)):
        for dpn__hmi in fsmv__kwjm:
            mwu__lmzr = bwzr__slzgw(dpn__hmi)
            sat__hisij = name, mwu__lmzr
            if sat__hisij in lokm__xwpn:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{dpn__hmi}' and '{lokm__xwpn[mwu__lmzr]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            lokm__xwpn[sat__hisij] = dpn__hmi
    bitii__rrtin, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=lokm__xwpn)
    left_on, right_on, whjc__xfck = _extract_equal_conds(bitii__rrtin.terms)
    return left_on, right_on, _insert_NA_cond(whjc__xfck, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    brjx__hym = dict(sort=sort, copy=copy, validate=validate)
    dgoy__xcv = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    bnzi__pcp = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    rhtt__dnsd = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in bnzi__pcp and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, rcywz__hgv = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if rcywz__hgv is None:
                    rhtt__dnsd = ''
                else:
                    rhtt__dnsd = str(rcywz__hgv)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = bnzi__pcp
        right_keys = bnzi__pcp
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
    jmf__aky = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        swrht__dtwrf = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        swrht__dtwrf = list(get_overload_const_list(suffixes))
    suffix_x = swrht__dtwrf[0]
    suffix_y = swrht__dtwrf[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    guyvy__qzht = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    guyvy__qzht += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    guyvy__qzht += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    guyvy__qzht += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, jmf__aky, rhtt__dnsd))
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo}, atun__ozaq)
    _impl = atun__ozaq['_impl']
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
    spxt__mqfix = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    bat__pvd = {get_overload_const_str(mvs__ggu) for mvs__ggu in (left_on,
        right_on, on) if is_overload_constant_str(mvs__ggu)}
    for df in (left, right):
        for i, dpn__hmi in enumerate(df.data):
            if not isinstance(dpn__hmi, valid_dataframe_column_types
                ) and dpn__hmi not in spxt__mqfix:
                raise BodoError(
                    f'{name_func}(): use of column with {type(dpn__hmi)} in merge unsupported'
                    )
            if df.columns[i] in bat__pvd and isinstance(dpn__hmi, MapArrayType
                ):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        swrht__dtwrf = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        swrht__dtwrf = list(get_overload_const_list(suffixes))
    if len(swrht__dtwrf) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    bnzi__pcp = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        rgk__hrgax = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            rgk__hrgax = on_str not in bnzi__pcp and ('left.' in on_str or 
                'right.' in on_str)
        if len(bnzi__pcp) == 0 and not rgk__hrgax:
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
    pzik__dcbx = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            hjvbs__ixep = left.index
            kgn__imvhq = isinstance(hjvbs__ixep, StringIndexType)
            peal__nmjjf = right.index
            ucqtk__medsk = isinstance(peal__nmjjf, StringIndexType)
        elif is_overload_true(left_index):
            hjvbs__ixep = left.index
            kgn__imvhq = isinstance(hjvbs__ixep, StringIndexType)
            peal__nmjjf = right.data[right.columns.index(right_keys[0])]
            ucqtk__medsk = peal__nmjjf.dtype == string_type
        elif is_overload_true(right_index):
            hjvbs__ixep = left.data[left.columns.index(left_keys[0])]
            kgn__imvhq = hjvbs__ixep.dtype == string_type
            peal__nmjjf = right.index
            ucqtk__medsk = isinstance(peal__nmjjf, StringIndexType)
        if kgn__imvhq and ucqtk__medsk:
            return
        hjvbs__ixep = hjvbs__ixep.dtype
        peal__nmjjf = peal__nmjjf.dtype
        try:
            wqr__wmli = pzik__dcbx.resolve_function_type(operator.eq, (
                hjvbs__ixep, peal__nmjjf), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=hjvbs__ixep, rk_dtype=peal__nmjjf))
    else:
        for joabr__tcseq, zdbm__sgk in zip(left_keys, right_keys):
            hjvbs__ixep = left.data[left.columns.index(joabr__tcseq)].dtype
            rskuy__rch = left.data[left.columns.index(joabr__tcseq)]
            peal__nmjjf = right.data[right.columns.index(zdbm__sgk)].dtype
            uxs__bjut = right.data[right.columns.index(zdbm__sgk)]
            if rskuy__rch == uxs__bjut:
                continue
            vbn__bus = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=joabr__tcseq, lk_dtype=hjvbs__ixep, rk=zdbm__sgk,
                rk_dtype=peal__nmjjf))
            sdi__zzpj = hjvbs__ixep == string_type
            dpyj__frft = peal__nmjjf == string_type
            if sdi__zzpj ^ dpyj__frft:
                raise_bodo_error(vbn__bus)
            try:
                wqr__wmli = pzik__dcbx.resolve_function_type(operator.eq, (
                    hjvbs__ixep, peal__nmjjf), {})
            except:
                raise_bodo_error(vbn__bus)


def validate_keys(keys, df):
    qmw__ztu = set(keys).difference(set(df.columns))
    if len(qmw__ztu) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in qmw__ztu:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {qmw__ztu} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    brjx__hym = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    dgoy__xcv = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', brjx__hym, dgoy__xcv,
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
    guyvy__qzht = "def _impl(left, other, on=None, how='left',\n"
    guyvy__qzht += "    lsuffix='', rsuffix='', sort=False):\n"
    guyvy__qzht += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo}, atun__ozaq)
    _impl = atun__ozaq['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        jyyc__lne = get_overload_const_list(on)
        validate_keys(jyyc__lne, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    bnzi__pcp = tuple(set(left.columns) & set(other.columns))
    if len(bnzi__pcp) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=bnzi__pcp))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    wzm__grxpg = set(left_keys) & set(right_keys)
    hoi__cajmv = set(left_columns) & set(right_columns)
    chghy__lahwc = hoi__cajmv - wzm__grxpg
    smh__apg = set(left_columns) - hoi__cajmv
    sfnhl__chz = set(right_columns) - hoi__cajmv
    hppd__ykz = {}

    def insertOutColumn(col_name):
        if col_name in hppd__ykz:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        hppd__ykz[col_name] = 0
    for fnnu__zzer in wzm__grxpg:
        insertOutColumn(fnnu__zzer)
    for fnnu__zzer in chghy__lahwc:
        urtlx__btqgw = str(fnnu__zzer) + suffix_x
        ryvmf__wuhya = str(fnnu__zzer) + suffix_y
        insertOutColumn(urtlx__btqgw)
        insertOutColumn(ryvmf__wuhya)
    for fnnu__zzer in smh__apg:
        insertOutColumn(fnnu__zzer)
    for fnnu__zzer in sfnhl__chz:
        insertOutColumn(fnnu__zzer)
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
    bnzi__pcp = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = bnzi__pcp
        right_keys = bnzi__pcp
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
        swrht__dtwrf = suffixes
    if is_overload_constant_list(suffixes):
        swrht__dtwrf = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        swrht__dtwrf = suffixes.value
    suffix_x = swrht__dtwrf[0]
    suffix_y = swrht__dtwrf[1]
    guyvy__qzht = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    guyvy__qzht += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    guyvy__qzht += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    guyvy__qzht += "    allow_exact_matches=True, direction='backward'):\n"
    guyvy__qzht += '  suffix_x = suffixes[0]\n'
    guyvy__qzht += '  suffix_y = suffixes[1]\n'
    guyvy__qzht += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo}, atun__ozaq)
    _impl = atun__ozaq['_impl']
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
    brjx__hym = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    gwu__zyll = dict(sort=False, group_keys=True, squeeze=False, observed=True)
    check_unsupported_args('Dataframe.groupby', brjx__hym, gwu__zyll,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    vovs__zxflh = func_name == 'DataFrame.pivot_table'
    if vovs__zxflh:
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
    lgcdg__eedvp = get_literal_value(columns)
    if isinstance(lgcdg__eedvp, (list, tuple)):
        if len(lgcdg__eedvp) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {lgcdg__eedvp}"
                )
        lgcdg__eedvp = lgcdg__eedvp[0]
    if lgcdg__eedvp not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {lgcdg__eedvp} not found in DataFrame {df}."
            )
    nweix__nsch = df.column_index[lgcdg__eedvp]
    if is_overload_none(index):
        sqeor__hemwk = []
        ynujx__reimx = []
    else:
        ynujx__reimx = get_literal_value(index)
        if not isinstance(ynujx__reimx, (list, tuple)):
            ynujx__reimx = [ynujx__reimx]
        sqeor__hemwk = []
        for index in ynujx__reimx:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            sqeor__hemwk.append(df.column_index[index])
    if not (all(isinstance(bha__lhf, int) for bha__lhf in ynujx__reimx) or
        all(isinstance(bha__lhf, str) for bha__lhf in ynujx__reimx)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        fik__dvqe = []
        kqd__aan = []
        elzz__pfuq = sqeor__hemwk + [nweix__nsch]
        for i, bha__lhf in enumerate(df.columns):
            if i not in elzz__pfuq:
                fik__dvqe.append(i)
                kqd__aan.append(bha__lhf)
    else:
        kqd__aan = get_literal_value(values)
        if not isinstance(kqd__aan, (list, tuple)):
            kqd__aan = [kqd__aan]
        fik__dvqe = []
        for val in kqd__aan:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            fik__dvqe.append(df.column_index[val])
    if all(isinstance(bha__lhf, int) for bha__lhf in kqd__aan):
        kqd__aan = np.array(kqd__aan, 'int64')
    elif all(isinstance(bha__lhf, str) for bha__lhf in kqd__aan):
        kqd__aan = pd.array(kqd__aan, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    ytwl__xrm = set(fik__dvqe) | set(sqeor__hemwk) | {nweix__nsch}
    if len(ytwl__xrm) != len(fik__dvqe) + len(sqeor__hemwk) + 1:
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
    if len(sqeor__hemwk) == 0:
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
        for neyq__nvkag in sqeor__hemwk:
            index_column = df.data[neyq__nvkag]
            check_valid_index_typ(index_column)
    hqwp__dfq = df.data[nweix__nsch]
    if isinstance(hqwp__dfq, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(hqwp__dfq, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for rjeam__uoma in fik__dvqe:
        mwny__wkluq = df.data[rjeam__uoma]
        if isinstance(mwny__wkluq, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or mwny__wkluq == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (ynujx__reimx, lgcdg__eedvp, kqd__aan, sqeor__hemwk, nweix__nsch,
        fik__dvqe)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (ynujx__reimx, lgcdg__eedvp, kqd__aan, neyq__nvkag, nweix__nsch, jws__lhvn
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(ynujx__reimx) == 0:
        if is_overload_none(data.index.name_typ):
            ynujx__reimx = [None]
        else:
            ynujx__reimx = [get_literal_value(data.index.name_typ)]
    if len(kqd__aan) == 1:
        cdbom__uei = None
    else:
        cdbom__uei = kqd__aan
    guyvy__qzht = 'def impl(data, index=None, columns=None, values=None):\n'
    guyvy__qzht += f'    pivot_values = data.iloc[:, {nweix__nsch}].unique()\n'
    guyvy__qzht += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(neyq__nvkag) == 0:
        guyvy__qzht += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        guyvy__qzht += '        (\n'
        for quxao__qbxan in neyq__nvkag:
            guyvy__qzht += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {quxao__qbxan}),
"""
        guyvy__qzht += '        ),\n'
    guyvy__qzht += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {nweix__nsch}),),
"""
    guyvy__qzht += '        (\n'
    for rjeam__uoma in jws__lhvn:
        guyvy__qzht += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {rjeam__uoma}),
"""
    guyvy__qzht += '        ),\n'
    guyvy__qzht += '        pivot_values,\n'
    guyvy__qzht += '        index_lit_tup,\n'
    guyvy__qzht += '        columns_lit,\n'
    guyvy__qzht += '        values_name_const,\n'
    guyvy__qzht += '    )\n'
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'index_lit_tup': tuple(ynujx__reimx),
        'columns_lit': lgcdg__eedvp, 'values_name_const': cdbom__uei},
        atun__ozaq)
    impl = atun__ozaq['impl']
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
    brjx__hym = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    dgoy__xcv = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (ynujx__reimx, lgcdg__eedvp, kqd__aan, neyq__nvkag, nweix__nsch,
            jws__lhvn) = (pivot_error_checking(data, index, columns, values,
            'DataFrame.pivot_table'))
        if len(kqd__aan) == 1:
            cdbom__uei = None
        else:
            cdbom__uei = kqd__aan
        guyvy__qzht = 'def impl(\n'
        guyvy__qzht += '    data,\n'
        guyvy__qzht += '    values=None,\n'
        guyvy__qzht += '    index=None,\n'
        guyvy__qzht += '    columns=None,\n'
        guyvy__qzht += '    aggfunc="mean",\n'
        guyvy__qzht += '    fill_value=None,\n'
        guyvy__qzht += '    margins=False,\n'
        guyvy__qzht += '    dropna=True,\n'
        guyvy__qzht += '    margins_name="All",\n'
        guyvy__qzht += '    observed=False,\n'
        guyvy__qzht += '    sort=True,\n'
        guyvy__qzht += '    _pivot_values=None,\n'
        guyvy__qzht += '):\n'
        vfbqr__kvnz = neyq__nvkag + [nweix__nsch] + jws__lhvn
        guyvy__qzht += f'    data = data.iloc[:, {vfbqr__kvnz}]\n'
        qdbr__lehg = ynujx__reimx + [lgcdg__eedvp]
        guyvy__qzht += (
            f'    data = data.groupby({qdbr__lehg!r}, as_index=False).agg(aggfunc)\n'
            )
        guyvy__qzht += (
            f'    pivot_values = data.iloc[:, {len(neyq__nvkag)}].unique()\n')
        guyvy__qzht += (
            '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n')
        guyvy__qzht += '        (\n'
        for i in range(0, len(neyq__nvkag)):
            guyvy__qzht += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        guyvy__qzht += '        ),\n'
        guyvy__qzht += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(neyq__nvkag)}),),
"""
        guyvy__qzht += '        (\n'
        for i in range(len(neyq__nvkag) + 1, len(jws__lhvn) + len(
            neyq__nvkag) + 1):
            guyvy__qzht += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        guyvy__qzht += '        ),\n'
        guyvy__qzht += '        pivot_values,\n'
        guyvy__qzht += '        index_lit_tup,\n'
        guyvy__qzht += '        columns_lit,\n'
        guyvy__qzht += '        values_name_const,\n'
        guyvy__qzht += '        check_duplicates=False,\n'
        guyvy__qzht += '    )\n'
        atun__ozaq = {}
        exec(guyvy__qzht, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(ynujx__reimx), 'columns_lit': lgcdg__eedvp,
            'values_name_const': cdbom__uei}, atun__ozaq)
        impl = atun__ozaq['impl']
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
    brjx__hym = dict(col_level=col_level, ignore_index=ignore_index)
    dgoy__xcv = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', brjx__hym, dgoy__xcv,
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
    pxkxp__ngfdb = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(pxkxp__ngfdb, (list, tuple)):
        pxkxp__ngfdb = [pxkxp__ngfdb]
    for bha__lhf in pxkxp__ngfdb:
        if bha__lhf not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {bha__lhf} not found in {frame}."
                )
    oqyiv__fhry = [frame.column_index[i] for i in pxkxp__ngfdb]
    if is_overload_none(value_vars):
        jkeyp__zmkm = []
        ktuqy__vxoto = []
        for i, bha__lhf in enumerate(frame.columns):
            if i not in oqyiv__fhry:
                jkeyp__zmkm.append(i)
                ktuqy__vxoto.append(bha__lhf)
    else:
        ktuqy__vxoto = get_literal_value(value_vars)
        if not isinstance(ktuqy__vxoto, (list, tuple)):
            ktuqy__vxoto = [ktuqy__vxoto]
        ktuqy__vxoto = [v for v in ktuqy__vxoto if v not in pxkxp__ngfdb]
        if not ktuqy__vxoto:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        jkeyp__zmkm = []
        for val in ktuqy__vxoto:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            jkeyp__zmkm.append(frame.column_index[val])
    for bha__lhf in ktuqy__vxoto:
        if bha__lhf not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {bha__lhf} not found in {frame}."
                )
    if not (all(isinstance(bha__lhf, int) for bha__lhf in ktuqy__vxoto) or
        all(isinstance(bha__lhf, str) for bha__lhf in ktuqy__vxoto)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    sxkg__sxyhc = frame.data[jkeyp__zmkm[0]]
    otrq__kjnuh = [frame.data[i].dtype for i in jkeyp__zmkm]
    jkeyp__zmkm = np.array(jkeyp__zmkm, dtype=np.int64)
    oqyiv__fhry = np.array(oqyiv__fhry, dtype=np.int64)
    _, mps__qte = bodo.utils.typing.get_common_scalar_dtype(otrq__kjnuh)
    if not mps__qte:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': ktuqy__vxoto, 'val_type':
        sxkg__sxyhc}
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
    if frame.is_table_format and all(v == sxkg__sxyhc.dtype for v in
        otrq__kjnuh):
        extra_globals['value_idxs'] = jkeyp__zmkm
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(ktuqy__vxoto) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {jkeyp__zmkm[0]})
"""
    else:
        smre__uzkp = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in jkeyp__zmkm)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({smre__uzkp},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in oqyiv__fhry:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(ktuqy__vxoto)})\n'
            )
    mmyye__uvl = ', '.join(f'out_id{i}' for i in oqyiv__fhry) + (', ' if 
        len(oqyiv__fhry) > 0 else '')
    data_args = mmyye__uvl + 'var_col, val_col'
    columns = tuple(pxkxp__ngfdb + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(ktuqy__vxoto)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    brjx__hym = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    dgoy__xcv = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', brjx__hym, dgoy__xcv,
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
    brjx__hym = dict(ignore_index=ignore_index, key=key)
    dgoy__xcv = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', brjx__hym, dgoy__xcv,
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
    rkuw__pqfzq = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        rkuw__pqfzq.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        loivm__vpv = [get_overload_const_tuple(by)]
    else:
        loivm__vpv = get_overload_const_list(by)
    loivm__vpv = set((k, '') if (k, '') in rkuw__pqfzq else k for k in
        loivm__vpv)
    if len(loivm__vpv.difference(rkuw__pqfzq)) > 0:
        xtve__fcdb = list(set(get_overload_const_list(by)).difference(
            rkuw__pqfzq))
        raise_bodo_error(f'sort_values(): invalid keys {xtve__fcdb} for by.')
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
        avi__ucjg = get_overload_const_list(na_position)
        for na_position in avi__ucjg:
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
    brjx__hym = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    dgoy__xcv = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', brjx__hym, dgoy__xcv,
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
    brjx__hym = dict(limit=limit, downcast=downcast)
    dgoy__xcv = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', brjx__hym, dgoy__xcv,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    fin__ixq = not is_overload_none(value)
    ukfj__kcwo = not is_overload_none(method)
    if fin__ixq and ukfj__kcwo:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not fin__ixq and not ukfj__kcwo:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if fin__ixq:
        xfe__fdfow = 'value=value'
    else:
        xfe__fdfow = 'method=method'
    data_args = [(f"df['{bha__lhf}'].fillna({xfe__fdfow}, inplace=inplace)" if
        isinstance(bha__lhf, str) else
        f'df[{bha__lhf}].fillna({xfe__fdfow}, inplace=inplace)') for
        bha__lhf in df.columns]
    guyvy__qzht = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        guyvy__qzht += '  ' + '  \n'.join(data_args) + '\n'
        atun__ozaq = {}
        exec(guyvy__qzht, {}, atun__ozaq)
        impl = atun__ozaq['impl']
        return impl
    else:
        return _gen_init_df(guyvy__qzht, df.columns, ', '.join(zum__ypiin +
            '.values' for zum__ypiin in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    brjx__hym = dict(col_level=col_level, col_fill=col_fill)
    dgoy__xcv = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', brjx__hym, dgoy__xcv,
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
    guyvy__qzht = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    guyvy__qzht += (
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
        zcvx__tbzcd = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            zcvx__tbzcd)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            guyvy__qzht += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            pvyre__slsa = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = pvyre__slsa + data_args
        else:
            bkrrh__xtr = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [bkrrh__xtr] + data_args
    return _gen_init_df(guyvy__qzht, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    qve__adp = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and qve__adp == 1 or is_overload_constant_list(level) and list(
        get_overload_const_list(level)) == list(range(qve__adp))


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
        wra__okis = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        sbzr__qjnqh = get_overload_const_list(subset)
        wra__okis = []
        for gqiob__vytsw in sbzr__qjnqh:
            if gqiob__vytsw not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{gqiob__vytsw}' not in data frame columns {df}"
                    )
            wra__okis.append(df.column_index[gqiob__vytsw])
    vyg__ikef = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(vyg__ikef))
    guyvy__qzht = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(vyg__ikef):
        guyvy__qzht += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    guyvy__qzht += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in wra__okis)))
    guyvy__qzht += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(guyvy__qzht, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    brjx__hym = dict(index=index, level=level, errors=errors)
    dgoy__xcv = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', brjx__hym, dgoy__xcv,
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
            puhm__owkbf = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            puhm__owkbf = get_overload_const_list(labels)
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
            puhm__owkbf = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            puhm__owkbf = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for bha__lhf in puhm__owkbf:
        if bha__lhf not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(bha__lhf, df.columns))
    if len(set(puhm__owkbf)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    pjq__dejsx = tuple(bha__lhf for bha__lhf in df.columns if bha__lhf not in
        puhm__owkbf)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[bha__lhf], '.copy()' if not inplace else '') for
        bha__lhf in pjq__dejsx)
    guyvy__qzht = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    guyvy__qzht += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(guyvy__qzht, pjq__dejsx, data_args, index)


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
    brjx__hym = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    xhjz__tokp = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', brjx__hym, xhjz__tokp,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    vyg__ikef = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(vyg__ikef))
    img__xigys = ', '.join('rhs_data_{}'.format(i) for i in range(vyg__ikef))
    guyvy__qzht = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    guyvy__qzht += '  if (frac == 1 or n == len(df)) and not replace:\n'
    guyvy__qzht += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(vyg__ikef):
        guyvy__qzht += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    guyvy__qzht += '  if frac is None:\n'
    guyvy__qzht += '    frac_d = -1.0\n'
    guyvy__qzht += '  else:\n'
    guyvy__qzht += '    frac_d = frac\n'
    guyvy__qzht += '  if n is None:\n'
    guyvy__qzht += '    n_i = 0\n'
    guyvy__qzht += '  else:\n'
    guyvy__qzht += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    guyvy__qzht += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({img__xigys},), {index}, n_i, frac_d, replace)
"""
    guyvy__qzht += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(guyvy__qzht, df.
        columns, data_args, 'index')


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
    jdvgy__ikglc = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    bgsse__pcc = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', jdvgy__ikglc, bgsse__pcc,
        package_name='pandas', module_name='DataFrame')
    ddc__oqy = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            mrg__cdg = ddc__oqy + '\n'
            mrg__cdg += 'Index: 0 entries\n'
            mrg__cdg += 'Empty DataFrame'
            print(mrg__cdg)
        return _info_impl
    else:
        guyvy__qzht = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        guyvy__qzht += '    ncols = df.shape[1]\n'
        guyvy__qzht += f'    lines = "{ddc__oqy}\\n"\n'
        guyvy__qzht += f'    lines += "{df.index}: "\n'
        guyvy__qzht += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            guyvy__qzht += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            guyvy__qzht += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            guyvy__qzht += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        guyvy__qzht += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        guyvy__qzht += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        guyvy__qzht += '    column_width = max(space, 7)\n'
        guyvy__qzht += '    column= "Column"\n'
        guyvy__qzht += '    underl= "------"\n'
        guyvy__qzht += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        guyvy__qzht += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        guyvy__qzht += '    mem_size = 0\n'
        guyvy__qzht += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        guyvy__qzht += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        guyvy__qzht += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        adp__ytqw = dict()
        for i in range(len(df.columns)):
            guyvy__qzht += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            almg__ykw = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                almg__ykw = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                gdle__wrwp = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                almg__ykw = f'{gdle__wrwp[:-7]}'
            guyvy__qzht += f'    col_dtype[{i}] = "{almg__ykw}"\n'
            if almg__ykw in adp__ytqw:
                adp__ytqw[almg__ykw] += 1
            else:
                adp__ytqw[almg__ykw] = 1
            guyvy__qzht += f'    col_name[{i}] = "{df.columns[i]}"\n'
            guyvy__qzht += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        guyvy__qzht += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        guyvy__qzht += '    for i in column_info:\n'
        guyvy__qzht += "        lines += f'{i}\\n'\n"
        yrxxe__ncsb = ', '.join(f'{k}({adp__ytqw[k]})' for k in sorted(
            adp__ytqw))
        guyvy__qzht += f"    lines += 'dtypes: {yrxxe__ncsb}\\n'\n"
        guyvy__qzht += '    mem_size += df.index.nbytes\n'
        guyvy__qzht += '    total_size = _sizeof_fmt(mem_size)\n'
        guyvy__qzht += "    lines += f'memory usage: {total_size}'\n"
        guyvy__qzht += '    print(lines)\n'
        atun__ozaq = {}
        exec(guyvy__qzht, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, atun__ozaq)
        _info_impl = atun__ozaq['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    guyvy__qzht = 'def impl(df, index=True, deep=False):\n'
    koye__cwne = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    hqv__tvum = is_overload_true(index)
    columns = df.columns
    if hqv__tvum:
        columns = ('Index',) + columns
    if len(columns) == 0:
        ixyhc__jyq = ()
    elif all(isinstance(bha__lhf, int) for bha__lhf in columns):
        ixyhc__jyq = np.array(columns, 'int64')
    elif all(isinstance(bha__lhf, str) for bha__lhf in columns):
        ixyhc__jyq = pd.array(columns, 'string')
    else:
        ixyhc__jyq = columns
    if df.is_table_format:
        nva__pfrbd = int(hqv__tvum)
        awagh__wihm = len(columns)
        guyvy__qzht += f'  nbytes_arr = np.empty({awagh__wihm}, np.int64)\n'
        guyvy__qzht += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        guyvy__qzht += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {nva__pfrbd})
"""
        if hqv__tvum:
            guyvy__qzht += f'  nbytes_arr[0] = {koye__cwne}\n'
        guyvy__qzht += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if hqv__tvum:
            data = f'{koye__cwne},{data}'
        else:
            ppr__yqi = ',' if len(columns) == 1 else ''
            data = f'{data}{ppr__yqi}'
        guyvy__qzht += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        ixyhc__jyq}, atun__ozaq)
    impl = atun__ozaq['impl']
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
    mycna__mjoa = 'read_excel_df{}'.format(next_label())
    setattr(types, mycna__mjoa, df_type)
    dnr__mafk = False
    if is_overload_constant_list(parse_dates):
        dnr__mafk = get_overload_const_list(parse_dates)
    fomv__apm = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    guyvy__qzht = f"""
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
    with numba.objmode(df="{mycna__mjoa}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{fomv__apm}}},
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
            parse_dates={dnr__mafk},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    atun__ozaq = {}
    exec(guyvy__qzht, globals(), atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as yfvfk__bdcwj:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    guyvy__qzht = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    guyvy__qzht += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    guyvy__qzht += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        guyvy__qzht += '   fig, ax = plt.subplots()\n'
    else:
        guyvy__qzht += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        guyvy__qzht += '   fig.set_figwidth(figsize[0])\n'
        guyvy__qzht += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        guyvy__qzht += '   xlabel = x\n'
    guyvy__qzht += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        guyvy__qzht += '   ylabel = y\n'
    else:
        guyvy__qzht += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        guyvy__qzht += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        guyvy__qzht += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    guyvy__qzht += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            guyvy__qzht += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            vdfu__vbjak = get_overload_const_str(x)
            tpbpi__bhst = df.columns.index(vdfu__vbjak)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if tpbpi__bhst != i:
                        guyvy__qzht += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            guyvy__qzht += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        guyvy__qzht += '   ax.scatter(df[x], df[y], s=20)\n'
        guyvy__qzht += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        guyvy__qzht += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        guyvy__qzht += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        guyvy__qzht += '   ax.legend()\n'
    guyvy__qzht += '   return ax\n'
    atun__ozaq = {}
    exec(guyvy__qzht, {'bodo': bodo, 'plt': plt}, atun__ozaq)
    impl = atun__ozaq['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for vwap__tolbf in df_typ.data:
        if not (isinstance(vwap__tolbf, IntegerArrayType) or isinstance(
            vwap__tolbf.dtype, types.Number) or vwap__tolbf.dtype in (bodo.
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
        ldr__dnpzz = args[0]
        pwzoa__xcxt = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        xkzi__cizgk = ldr__dnpzz
        check_runtime_cols_unsupported(ldr__dnpzz, 'set_df_col()')
        if isinstance(ldr__dnpzz, DataFrameType):
            index = ldr__dnpzz.index
            if len(ldr__dnpzz.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(ldr__dnpzz.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if pwzoa__xcxt in ldr__dnpzz.columns:
                pjq__dejsx = ldr__dnpzz.columns
                ljp__vori = ldr__dnpzz.columns.index(pwzoa__xcxt)
                gtcvh__htgxp = list(ldr__dnpzz.data)
                gtcvh__htgxp[ljp__vori] = val
                gtcvh__htgxp = tuple(gtcvh__htgxp)
            else:
                pjq__dejsx = ldr__dnpzz.columns + (pwzoa__xcxt,)
                gtcvh__htgxp = ldr__dnpzz.data + (val,)
            xkzi__cizgk = DataFrameType(gtcvh__htgxp, index, pjq__dejsx,
                ldr__dnpzz.dist, ldr__dnpzz.is_table_format)
        return xkzi__cizgk(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    mmte__roaj = {}

    def _rewrite_membership_op(self, node, left, right):
        ekvpm__zjat = node.op
        op = self.visit(ekvpm__zjat)
        return op, ekvpm__zjat, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    gncsj__nqyoz = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in gncsj__nqyoz:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in gncsj__nqyoz:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        eikxx__prfq = node.attr
        value = node.value
        yfh__ikwe = pd.core.computation.ops.LOCAL_TAG
        if eikxx__prfq in ('str', 'dt'):
            try:
                urjl__rndov = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as cedvn__xqnu:
                col_name = cedvn__xqnu.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            urjl__rndov = str(self.visit(value))
        sat__hisij = urjl__rndov, eikxx__prfq
        if sat__hisij in join_cleaned_cols:
            eikxx__prfq = join_cleaned_cols[sat__hisij]
        name = urjl__rndov + '.' + eikxx__prfq
        if name.startswith(yfh__ikwe):
            name = name[len(yfh__ikwe):]
        if eikxx__prfq in ('str', 'dt'):
            yrw__rohfa = columns[cleaned_columns.index(urjl__rndov)]
            mmte__roaj[yrw__rohfa] = urjl__rndov
            self.env.scope[name] = 0
            return self.term_type(yfh__ikwe + name, self.env)
        gncsj__nqyoz.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in gncsj__nqyoz:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        uhm__mayl = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        pwzoa__xcxt = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(uhm__mayl), pwzoa__xcxt))

    def op__str__(self):
        pch__kon = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            efiyb__zsg)) for efiyb__zsg in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(pch__kon)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(pch__kon)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(pch__kon))
    ahdcw__yffvr = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    ayx__vqvog = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    hcd__odrqg = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    evcw__qlc = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    wcq__vkct = pd.core.computation.ops.Term.__str__
    ayaai__mxug = pd.core.computation.ops.MathCall.__str__
    jyj__zjxf = pd.core.computation.ops.Op.__str__
    dbf__itue = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        bitii__rrtin = pd.core.computation.expr.Expr(expr, env=env)
        fyu__zbkrd = str(bitii__rrtin)
    except pd.core.computation.ops.UndefinedVariableError as cedvn__xqnu:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == cedvn__xqnu.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {cedvn__xqnu}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            ahdcw__yffvr)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            ayx__vqvog)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = hcd__odrqg
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = evcw__qlc
        pd.core.computation.ops.Term.__str__ = wcq__vkct
        pd.core.computation.ops.MathCall.__str__ = ayaai__mxug
        pd.core.computation.ops.Op.__str__ = jyj__zjxf
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            dbf__itue)
    pmq__bvka = pd.core.computation.parsing.clean_column_name
    mmte__roaj.update({bha__lhf: pmq__bvka(bha__lhf) for bha__lhf in
        columns if pmq__bvka(bha__lhf) in bitii__rrtin.names})
    return bitii__rrtin, fyu__zbkrd, mmte__roaj


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        gce__veup = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(gce__veup))
        qoa__bcsf = namedtuple('Pandas', col_names)
        tqqs__ezbe = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], qoa__bcsf)
        super(DataFrameTupleIterator, self).__init__(name, tqqs__ezbe)

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
        txuy__hhlie = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        txuy__hhlie = [types.Array(types.int64, 1, 'C')] + txuy__hhlie
        riu__jtocc = DataFrameTupleIterator(col_names, txuy__hhlie)
        return riu__jtocc(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jywwy__nkga = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            jywwy__nkga)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    krx__elnvt = args[len(args) // 2:]
    ypj__wsh = sig.args[len(sig.args) // 2:]
    zoddp__icrj = context.make_helper(builder, sig.return_type)
    cbliv__ioj = context.get_constant(types.intp, 0)
    gul__qiae = cgutils.alloca_once_value(builder, cbliv__ioj)
    zoddp__icrj.index = gul__qiae
    for i, arr in enumerate(krx__elnvt):
        setattr(zoddp__icrj, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(krx__elnvt, ypj__wsh):
        context.nrt.incref(builder, arr_typ, arr)
    res = zoddp__icrj._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    cbmlb__qnei, = sig.args
    grj__wfpwl, = args
    zoddp__icrj = context.make_helper(builder, cbmlb__qnei, value=grj__wfpwl)
    hig__tokem = signature(types.intp, cbmlb__qnei.array_types[1])
    dhzr__kcnqz = context.compile_internal(builder, lambda a: len(a),
        hig__tokem, [zoddp__icrj.array0])
    index = builder.load(zoddp__icrj.index)
    vixgy__ymlxs = builder.icmp_signed('<', index, dhzr__kcnqz)
    result.set_valid(vixgy__ymlxs)
    with builder.if_then(vixgy__ymlxs):
        values = [index]
        for i, arr_typ in enumerate(cbmlb__qnei.array_types[1:]):
            latgl__klwoq = getattr(zoddp__icrj, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                iyiix__aeo = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    iyiix__aeo, [latgl__klwoq, index])
            else:
                iyiix__aeo = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    iyiix__aeo, [latgl__klwoq, index])
            values.append(val)
        value = context.make_tuple(builder, cbmlb__qnei.yield_type, values)
        result.yield_(value)
        kke__lbxsh = cgutils.increment_index(builder, index)
        builder.store(kke__lbxsh, zoddp__icrj.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    ncjf__alkci = ir.Assign(rhs, lhs, expr.loc)
    aqf__yytf = lhs
    wzcud__adggf = []
    rupy__jcz = []
    obhg__pqti = typ.count
    for i in range(obhg__pqti):
        sui__ajhyf = ir.Var(aqf__yytf.scope, mk_unique_var('{}_size{}'.
            format(aqf__yytf.name, i)), aqf__yytf.loc)
        zqiex__zycha = ir.Expr.static_getitem(lhs, i, None, aqf__yytf.loc)
        self.calltypes[zqiex__zycha] = None
        wzcud__adggf.append(ir.Assign(zqiex__zycha, sui__ajhyf, aqf__yytf.loc))
        self._define(equiv_set, sui__ajhyf, types.intp, zqiex__zycha)
        rupy__jcz.append(sui__ajhyf)
    qqlk__wog = tuple(rupy__jcz)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        qqlk__wog, pre=[ncjf__alkci] + wzcud__adggf)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
