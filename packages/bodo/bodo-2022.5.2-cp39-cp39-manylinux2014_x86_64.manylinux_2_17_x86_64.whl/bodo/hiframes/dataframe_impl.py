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
        jty__asx = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({jty__asx})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    dmfgp__ravdg = 'def impl(df):\n'
    if df.has_runtime_cols:
        dmfgp__ravdg += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        vtq__qzx = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        dmfgp__ravdg += f'  return {vtq__qzx}'
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
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
    buym__fsqj = len(df.columns)
    xcftm__kidld = set(i for i in range(buym__fsqj) if isinstance(df.data[i
        ], IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in xcftm__kidld else '') for i in
        range(buym__fsqj))
    dmfgp__ravdg = 'def f(df):\n'.format()
    dmfgp__ravdg += '    return np.stack(({},), 1)\n'.format(data_args)
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'np': np}, fsfb__fbqpn)
    zzhun__wbv = fsfb__fbqpn['f']
    return zzhun__wbv


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
    gbfq__khjc = {'dtype': dtype, 'na_value': na_value}
    qkqbf__zvo = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', gbfq__khjc, qkqbf__zvo,
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
            wti__xxa = bodo.hiframes.table.compute_num_runtime_columns(t)
            return wti__xxa * len(t)
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
            wti__xxa = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), wti__xxa
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    dmfgp__ravdg = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    tcmzy__ecn = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    dmfgp__ravdg += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{tcmzy__ecn}), {index}, None)
"""
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
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
    gbfq__khjc = {'copy': copy, 'errors': errors}
    qkqbf__zvo = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', gbfq__khjc, qkqbf__zvo,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        jruhy__vrva = _bodo_object_typeref.instance_type
        assert isinstance(jruhy__vrva, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        wzk__lxgi = {}
        for i, name in enumerate(jruhy__vrva.columns):
            arr_typ = jruhy__vrva.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                unwtk__emhjp = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                unwtk__emhjp = boolean_dtype
            else:
                unwtk__emhjp = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = unwtk__emhjp
            wzk__lxgi[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {wzk__lxgi[fpfwa__qwkqo]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if fpfwa__qwkqo in wzk__lxgi else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, fpfwa__qwkqo in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        nrcwy__mjj = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(nrcwy__mjj[fpfwa__qwkqo])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if fpfwa__qwkqo in nrcwy__mjj else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, fpfwa__qwkqo in enumerate(df.columns))
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
        yjbw__grp = types.none
        extra_globals = {'output_arr_typ': yjbw__grp}
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
        aez__eixns = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                aez__eixns.append(arr + '.copy()')
            elif is_overload_false(deep):
                aez__eixns.append(arr)
            else:
                aez__eixns.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(aez__eixns)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    gbfq__khjc = {'index': index, 'level': level, 'errors': errors}
    qkqbf__zvo = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', gbfq__khjc, qkqbf__zvo,
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
        tgj__kgnwj = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        tgj__kgnwj = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    nfey__hai = tuple([tgj__kgnwj.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        out_df_type = df.copy(columns=nfey__hai)
        yjbw__grp = types.none
        extra_globals = {'output_arr_typ': yjbw__grp}
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
        aez__eixns = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                aez__eixns.append(arr + '.copy()')
            elif is_overload_false(copy):
                aez__eixns.append(arr)
            else:
                aez__eixns.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(aez__eixns)
    return _gen_init_df(header, nfey__hai, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    gnaq__sffej = not is_overload_none(items)
    cqa__zyx = not is_overload_none(like)
    vqorg__qmp = not is_overload_none(regex)
    goocj__iqk = gnaq__sffej ^ cqa__zyx ^ vqorg__qmp
    dvos__izhei = not (gnaq__sffej or cqa__zyx or vqorg__qmp)
    if dvos__izhei:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not goocj__iqk:
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
        crt__xmhq = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        crt__xmhq = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert crt__xmhq in {0, 1}
    dmfgp__ravdg = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if crt__xmhq == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if crt__xmhq == 1:
        ehm__oyqd = []
        niuiy__zdcsd = []
        evxxw__yey = []
        if gnaq__sffej:
            if is_overload_constant_list(items):
                bcwmh__cpib = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if cqa__zyx:
            if is_overload_constant_str(like):
                tbge__adud = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if vqorg__qmp:
            if is_overload_constant_str(regex):
                smvh__iwva = get_overload_const_str(regex)
                vsvn__hil = re.compile(smvh__iwva)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, fpfwa__qwkqo in enumerate(df.columns):
            if not is_overload_none(items
                ) and fpfwa__qwkqo in bcwmh__cpib or not is_overload_none(like
                ) and tbge__adud in str(fpfwa__qwkqo) or not is_overload_none(
                regex) and vsvn__hil.search(str(fpfwa__qwkqo)):
                niuiy__zdcsd.append(fpfwa__qwkqo)
                evxxw__yey.append(i)
        for i in evxxw__yey:
            var_name = f'data_{i}'
            ehm__oyqd.append(var_name)
            dmfgp__ravdg += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(ehm__oyqd)
        return _gen_init_df(dmfgp__ravdg, niuiy__zdcsd, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        yjbw__grp = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([yjbw__grp] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': yjbw__grp}
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
    eoxf__zire = is_overload_none(include)
    vviz__fheje = is_overload_none(exclude)
    fotpa__arat = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if eoxf__zire and vviz__fheje:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not eoxf__zire:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            ltw__haks = [dtype_to_array_type(parse_dtype(elem, fotpa__arat)
                ) for elem in include]
        elif is_legal_input(include):
            ltw__haks = [dtype_to_array_type(parse_dtype(include, fotpa__arat))
                ]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        ltw__haks = get_nullable_and_non_nullable_types(ltw__haks)
        lcy__knwwp = tuple(fpfwa__qwkqo for i, fpfwa__qwkqo in enumerate(df
            .columns) if df.data[i] in ltw__haks)
    else:
        lcy__knwwp = df.columns
    if not vviz__fheje:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            lpdj__hpykz = [dtype_to_array_type(parse_dtype(elem,
                fotpa__arat)) for elem in exclude]
        elif is_legal_input(exclude):
            lpdj__hpykz = [dtype_to_array_type(parse_dtype(exclude,
                fotpa__arat))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        lpdj__hpykz = get_nullable_and_non_nullable_types(lpdj__hpykz)
        lcy__knwwp = tuple(fpfwa__qwkqo for fpfwa__qwkqo in lcy__knwwp if 
            df.data[df.column_index[fpfwa__qwkqo]] not in lpdj__hpykz)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[fpfwa__qwkqo]})'
         for fpfwa__qwkqo in lcy__knwwp)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, lcy__knwwp, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        yjbw__grp = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([yjbw__grp] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': yjbw__grp}
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
    qor__mal = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in qor__mal:
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
    qor__mal = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in qor__mal:
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
    dmfgp__ravdg = 'def impl(df, values):\n'
    dbf__ftt = {}
    rzwam__xlw = False
    if isinstance(values, DataFrameType):
        rzwam__xlw = True
        for i, fpfwa__qwkqo in enumerate(df.columns):
            if fpfwa__qwkqo in values.column_index:
                bjtfk__kokka = 'val{}'.format(i)
                dmfgp__ravdg += f"""  {bjtfk__kokka} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[fpfwa__qwkqo]})
"""
                dbf__ftt[fpfwa__qwkqo] = bjtfk__kokka
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        dbf__ftt = {fpfwa__qwkqo: 'values' for fpfwa__qwkqo in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        bjtfk__kokka = 'data{}'.format(i)
        dmfgp__ravdg += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(bjtfk__kokka, i))
        data.append(bjtfk__kokka)
    lyoj__vkfkb = ['out{}'.format(i) for i in range(len(df.columns))]
    zbpo__cipy = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    sbvsj__qpri = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    eouc__ydnzz = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, bmh__eqw) in enumerate(zip(df.columns, data)):
        if cname in dbf__ftt:
            qmsb__gro = dbf__ftt[cname]
            if rzwam__xlw:
                dmfgp__ravdg += zbpo__cipy.format(bmh__eqw, qmsb__gro,
                    lyoj__vkfkb[i])
            else:
                dmfgp__ravdg += sbvsj__qpri.format(bmh__eqw, qmsb__gro,
                    lyoj__vkfkb[i])
        else:
            dmfgp__ravdg += eouc__ydnzz.format(lyoj__vkfkb[i])
    return _gen_init_df(dmfgp__ravdg, df.columns, ','.join(lyoj__vkfkb))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    buym__fsqj = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(buym__fsqj))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    ijrt__cet = [fpfwa__qwkqo for fpfwa__qwkqo, dmin__hljms in zip(df.
        columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype(
        dmin__hljms.dtype)]
    assert len(ijrt__cet) != 0
    sxtw__otg = ''
    if not any(dmin__hljms == types.float64 for dmin__hljms in df.data):
        sxtw__otg = '.astype(np.float64)'
    etdn__wjiho = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[fpfwa__qwkqo], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[fpfwa__qwkqo]], IntegerArrayType
        ) or df.data[df.column_index[fpfwa__qwkqo]] == boolean_array else
        '') for fpfwa__qwkqo in ijrt__cet)
    xphiu__vdxhb = 'np.stack(({},), 1){}'.format(etdn__wjiho, sxtw__otg)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(ijrt__cet)))
    index = f'{generate_col_to_index_func_text(ijrt__cet)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(xphiu__vdxhb)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, ijrt__cet, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    bxjt__ntmka = dict(ddof=ddof)
    vvy__rqgxw = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    qfi__czbss = '1' if is_overload_none(min_periods) else 'min_periods'
    ijrt__cet = [fpfwa__qwkqo for fpfwa__qwkqo, dmin__hljms in zip(df.
        columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype(
        dmin__hljms.dtype)]
    if len(ijrt__cet) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    sxtw__otg = ''
    if not any(dmin__hljms == types.float64 for dmin__hljms in df.data):
        sxtw__otg = '.astype(np.float64)'
    etdn__wjiho = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[fpfwa__qwkqo], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[fpfwa__qwkqo]], IntegerArrayType
        ) or df.data[df.column_index[fpfwa__qwkqo]] == boolean_array else
        '') for fpfwa__qwkqo in ijrt__cet)
    xphiu__vdxhb = 'np.stack(({},), 1){}'.format(etdn__wjiho, sxtw__otg)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(ijrt__cet)))
    index = f'pd.Index({ijrt__cet})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(xphiu__vdxhb)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        qfi__czbss)
    return _gen_init_df(header, ijrt__cet, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    bxjt__ntmka = dict(axis=axis, level=level, numeric_only=numeric_only)
    vvy__rqgxw = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    dmfgp__ravdg = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    dmfgp__ravdg += '  data = np.array([{}])\n'.format(data_args)
    vtq__qzx = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    dmfgp__ravdg += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {vtq__qzx})\n'
        )
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'np': np}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    bxjt__ntmka = dict(axis=axis)
    vvy__rqgxw = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    dmfgp__ravdg = 'def impl(df, axis=0, dropna=True):\n'
    dmfgp__ravdg += '  data = np.asarray(({},))\n'.format(data_args)
    vtq__qzx = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    dmfgp__ravdg += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {vtq__qzx})\n'
        )
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'np': np}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    bxjt__ntmka = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    vvy__rqgxw = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    bxjt__ntmka = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    vvy__rqgxw = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    bxjt__ntmka = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vvy__rqgxw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    bxjt__ntmka = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vvy__rqgxw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    bxjt__ntmka = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vvy__rqgxw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    bxjt__ntmka = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    vvy__rqgxw = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    bxjt__ntmka = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    vvy__rqgxw = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    bxjt__ntmka = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vvy__rqgxw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    bxjt__ntmka = dict(numeric_only=numeric_only, interpolation=interpolation)
    vvy__rqgxw = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    bxjt__ntmka = dict(axis=axis, skipna=skipna)
    vvy__rqgxw = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for yktl__ppsw in df.data:
        if not (bodo.utils.utils.is_np_array_typ(yktl__ppsw) and (
            yktl__ppsw.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(yktl__ppsw.dtype, (types.Number, types.Boolean))) or
            isinstance(yktl__ppsw, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or yktl__ppsw in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {yktl__ppsw} not supported.'
                )
        if isinstance(yktl__ppsw, bodo.CategoricalArrayType
            ) and not yktl__ppsw.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    bxjt__ntmka = dict(axis=axis, skipna=skipna)
    vvy__rqgxw = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for yktl__ppsw in df.data:
        if not (bodo.utils.utils.is_np_array_typ(yktl__ppsw) and (
            yktl__ppsw.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(yktl__ppsw.dtype, (types.Number, types.Boolean))) or
            isinstance(yktl__ppsw, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or yktl__ppsw in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {yktl__ppsw} not supported.'
                )
        if isinstance(yktl__ppsw, bodo.CategoricalArrayType
            ) and not yktl__ppsw.dtype.ordered:
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
        ijrt__cet = tuple(fpfwa__qwkqo for fpfwa__qwkqo, dmin__hljms in zip
            (df.columns, df.data) if bodo.utils.typing.
            _is_pandas_numeric_dtype(dmin__hljms.dtype))
        out_colnames = ijrt__cet
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            ivpx__lfimd = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[fpfwa__qwkqo]].dtype) for fpfwa__qwkqo in
                out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(ivpx__lfimd, []))
    except NotImplementedError as wxq__qwdgt:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    ucfvh__vwzj = ''
    if func_name in ('sum', 'prod'):
        ucfvh__vwzj = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    dmfgp__ravdg = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, ucfvh__vwzj))
    if func_name == 'quantile':
        dmfgp__ravdg = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        dmfgp__ravdg = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        dmfgp__ravdg += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        dmfgp__ravdg += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    hds__bywoj = ''
    if func_name in ('min', 'max'):
        hds__bywoj = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        hds__bywoj = ', dtype=np.float32'
    wpvv__zzwxh = f'bodo.libs.array_ops.array_op_{func_name}'
    kky__hww = ''
    if func_name in ['sum', 'prod']:
        kky__hww = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        kky__hww = 'index'
    elif func_name == 'quantile':
        kky__hww = 'q'
    elif func_name in ['std', 'var']:
        kky__hww = 'True, ddof'
    elif func_name == 'median':
        kky__hww = 'True'
    data_args = ', '.join(
        f'{wpvv__zzwxh}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[fpfwa__qwkqo]}), {kky__hww})'
         for fpfwa__qwkqo in out_colnames)
    dmfgp__ravdg = ''
    if func_name in ('idxmax', 'idxmin'):
        dmfgp__ravdg += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        dmfgp__ravdg += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        dmfgp__ravdg += '  data = np.asarray(({},){})\n'.format(data_args,
            hds__bywoj)
    dmfgp__ravdg += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return dmfgp__ravdg


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    hhiy__yum = [df_type.column_index[fpfwa__qwkqo] for fpfwa__qwkqo in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in hhiy__yum)
    bagt__lwmr = '\n        '.join(f'row[{i}] = arr_{hhiy__yum[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    oastf__rnrd = f'len(arr_{hhiy__yum[0]})'
    tqjrz__wlbqg = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in tqjrz__wlbqg:
        jqxq__voiky = tqjrz__wlbqg[func_name]
        labf__krk = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        dmfgp__ravdg = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {oastf__rnrd}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{labf__krk})
    for i in numba.parfors.parfor.internal_prange(n):
        {bagt__lwmr}
        A[i] = {jqxq__voiky}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return dmfgp__ravdg
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    bxjt__ntmka = dict(fill_method=fill_method, limit=limit, freq=freq)
    vvy__rqgxw = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', bxjt__ntmka, vvy__rqgxw,
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
    bxjt__ntmka = dict(axis=axis, skipna=skipna)
    vvy__rqgxw = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', bxjt__ntmka, vvy__rqgxw,
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
    bxjt__ntmka = dict(skipna=skipna)
    vvy__rqgxw = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', bxjt__ntmka, vvy__rqgxw,
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
    bxjt__ntmka = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    vvy__rqgxw = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    ijrt__cet = [fpfwa__qwkqo for fpfwa__qwkqo, dmin__hljms in zip(df.
        columns, df.data) if _is_describe_type(dmin__hljms)]
    if len(ijrt__cet) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    fcbo__otvs = sum(df.data[df.column_index[fpfwa__qwkqo]].dtype == bodo.
        datetime64ns for fpfwa__qwkqo in ijrt__cet)

    def _get_describe(col_ind):
        dkxe__xsdp = df.data[col_ind].dtype == bodo.datetime64ns
        if fcbo__otvs and fcbo__otvs != len(ijrt__cet):
            if dkxe__xsdp:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for fpfwa__qwkqo in ijrt__cet:
        col_ind = df.column_index[fpfwa__qwkqo]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[fpfwa__qwkqo]) for
        fpfwa__qwkqo in ijrt__cet)
    mwh__qmnlo = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if fcbo__otvs == len(ijrt__cet):
        mwh__qmnlo = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif fcbo__otvs:
        mwh__qmnlo = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({mwh__qmnlo})'
    return _gen_init_df(header, ijrt__cet, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    bxjt__ntmka = dict(axis=axis, convert=convert, is_copy=is_copy)
    vvy__rqgxw = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', bxjt__ntmka, vvy__rqgxw,
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
    bxjt__ntmka = dict(freq=freq, axis=axis, fill_value=fill_value)
    vvy__rqgxw = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for wru__ctas in df.data:
        if not is_supported_shift_array_type(wru__ctas):
            raise BodoError(
                f'Dataframe.shift() column input type {wru__ctas.dtype} not supported yet.'
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
    bxjt__ntmka = dict(axis=axis)
    vvy__rqgxw = dict(axis=0)
    check_unsupported_args('DataFrame.diff', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for wru__ctas in df.data:
        if not (isinstance(wru__ctas, types.Array) and (isinstance(
            wru__ctas.dtype, types.Number) or wru__ctas.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {wru__ctas.dtype} not supported.'
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
    rejd__fcyf = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(rejd__fcyf)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        steg__bqkmz = get_overload_const_list(column)
    else:
        steg__bqkmz = [get_literal_value(column)]
    gvcie__tjyoz = [df.column_index[fpfwa__qwkqo] for fpfwa__qwkqo in
        steg__bqkmz]
    for i in gvcie__tjyoz:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{gvcie__tjyoz[0]})\n'
        )
    for i in range(n):
        if i in gvcie__tjyoz:
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
    gbfq__khjc = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    qkqbf__zvo = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', gbfq__khjc, qkqbf__zvo,
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
    columns = tuple(fpfwa__qwkqo for fpfwa__qwkqo in df.columns if 
        fpfwa__qwkqo != col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    gbfq__khjc = {'inplace': inplace}
    qkqbf__zvo = {'inplace': False}
    check_unsupported_args('query', gbfq__khjc, qkqbf__zvo, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        lcg__tcb = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[lcg__tcb]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    gbfq__khjc = {'subset': subset, 'keep': keep}
    qkqbf__zvo = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', gbfq__khjc, qkqbf__zvo,
        package_name='pandas', module_name='DataFrame')
    buym__fsqj = len(df.columns)
    dmfgp__ravdg = "def impl(df, subset=None, keep='first'):\n"
    for i in range(buym__fsqj):
        dmfgp__ravdg += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    yrbmb__fym = ', '.join(f'data_{i}' for i in range(buym__fsqj))
    yrbmb__fym += ',' if buym__fsqj == 1 else ''
    dmfgp__ravdg += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({yrbmb__fym}))\n')
    dmfgp__ravdg += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    dmfgp__ravdg += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    gbfq__khjc = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    qkqbf__zvo = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    cseu__oex = []
    if is_overload_constant_list(subset):
        cseu__oex = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        cseu__oex = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        cseu__oex = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    vgkde__dkztn = []
    for col_name in cseu__oex:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        vgkde__dkztn.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', gbfq__khjc,
        qkqbf__zvo, package_name='pandas', module_name='DataFrame')
    zvvks__jlyn = []
    if vgkde__dkztn:
        for wlvq__hdfy in vgkde__dkztn:
            if isinstance(df.data[wlvq__hdfy], bodo.MapArrayType):
                zvvks__jlyn.append(df.columns[wlvq__hdfy])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                zvvks__jlyn.append(col_name)
    if zvvks__jlyn:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {zvvks__jlyn} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    buym__fsqj = len(df.columns)
    tlzxw__deai = ['data_{}'.format(i) for i in vgkde__dkztn]
    amxj__xzd = ['data_{}'.format(i) for i in range(buym__fsqj) if i not in
        vgkde__dkztn]
    if tlzxw__deai:
        hyama__vrup = len(tlzxw__deai)
    else:
        hyama__vrup = buym__fsqj
    kooi__uerv = ', '.join(tlzxw__deai + amxj__xzd)
    data_args = ', '.join('data_{}'.format(i) for i in range(buym__fsqj))
    dmfgp__ravdg = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(buym__fsqj):
        dmfgp__ravdg += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    dmfgp__ravdg += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(kooi__uerv, index, hyama__vrup))
    dmfgp__ravdg += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(dmfgp__ravdg, df.columns, data_args, 'index')


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
            rrhdg__evmvx = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                rrhdg__evmvx = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                rrhdg__evmvx = lambda i: f'other[:,{i}]'
        buym__fsqj = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {rrhdg__evmvx(i)})'
             for i in range(buym__fsqj))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        ngl__rphb = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(ngl__rphb)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    bxjt__ntmka = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    vvy__rqgxw = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', bxjt__ntmka, vvy__rqgxw,
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
    buym__fsqj = len(df.columns)
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
        for i in range(buym__fsqj):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other.column_index[df
                    .columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(buym__fsqj):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(buym__fsqj):
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
        jwx__gnu = 'out_df_type'
    else:
        jwx__gnu = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    dmfgp__ravdg = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {jwx__gnu})
"""
    fsfb__fbqpn = {}
    ktd__dkyeh = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    ktd__dkyeh.update(extra_globals)
    exec(dmfgp__ravdg, ktd__dkyeh, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        gxnnd__cgvp = pd.Index(lhs.columns)
        yrzrj__aanf = pd.Index(rhs.columns)
        wvdq__nyxpg, zyo__tke, bwmun__talfs = gxnnd__cgvp.join(yrzrj__aanf,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(wvdq__nyxpg), zyo__tke, bwmun__talfs
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        nztx__llu = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        rad__qiml = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, nztx__llu)
        check_runtime_cols_unsupported(rhs, nztx__llu)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                wvdq__nyxpg, zyo__tke, bwmun__talfs = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {pginh__way}) {nztx__llu}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {zgnbu__zyxy})'
                     if pginh__way != -1 and zgnbu__zyxy != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for pginh__way, zgnbu__zyxy in zip(zyo__tke, bwmun__talfs)
                    )
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, wvdq__nyxpg, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            dckm__bbvqh = []
            tkas__yvju = []
            if op in rad__qiml:
                for i, mest__htlmh in enumerate(lhs.data):
                    if is_common_scalar_dtype([mest__htlmh.dtype, rhs]):
                        dckm__bbvqh.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {nztx__llu} rhs'
                            )
                    else:
                        csbaj__lpgrd = f'arr{i}'
                        tkas__yvju.append(csbaj__lpgrd)
                        dckm__bbvqh.append(csbaj__lpgrd)
                data_args = ', '.join(dckm__bbvqh)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {nztx__llu} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(tkas__yvju) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {csbaj__lpgrd} = np.empty(n, dtype=np.bool_)\n' for
                    csbaj__lpgrd in tkas__yvju)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(csbaj__lpgrd,
                    op == operator.ne) for csbaj__lpgrd in tkas__yvju)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            dckm__bbvqh = []
            tkas__yvju = []
            if op in rad__qiml:
                for i, mest__htlmh in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, mest__htlmh.dtype]):
                        dckm__bbvqh.append(
                            f'lhs {nztx__llu} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        csbaj__lpgrd = f'arr{i}'
                        tkas__yvju.append(csbaj__lpgrd)
                        dckm__bbvqh.append(csbaj__lpgrd)
                data_args = ', '.join(dckm__bbvqh)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, nztx__llu) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(tkas__yvju) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(csbaj__lpgrd) for csbaj__lpgrd in tkas__yvju)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(csbaj__lpgrd,
                    op == operator.ne) for csbaj__lpgrd in tkas__yvju)
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
        ngl__rphb = create_binary_op_overload(op)
        overload(op)(ngl__rphb)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        nztx__llu = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, nztx__llu)
        check_runtime_cols_unsupported(right, nztx__llu)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                wvdq__nyxpg, _, bwmun__talfs = _get_binop_columns(left,
                    right, True)
                dmfgp__ravdg = 'def impl(left, right):\n'
                for i, zgnbu__zyxy in enumerate(bwmun__talfs):
                    if zgnbu__zyxy == -1:
                        dmfgp__ravdg += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    dmfgp__ravdg += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    dmfgp__ravdg += f"""  df_arr{i} {nztx__llu} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {zgnbu__zyxy})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    wvdq__nyxpg)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(dmfgp__ravdg, wvdq__nyxpg, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            dmfgp__ravdg = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                dmfgp__ravdg += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                dmfgp__ravdg += '  df_arr{0} {1} right\n'.format(i, nztx__llu)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(dmfgp__ravdg, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        ngl__rphb = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(ngl__rphb)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            nztx__llu = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, nztx__llu)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, nztx__llu) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        ngl__rphb = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(ngl__rphb)


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
            twgya__yej = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                twgya__yej[i] = bodo.libs.array_kernels.isna(obj, i)
            return twgya__yej
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
            twgya__yej = np.empty(n, np.bool_)
            for i in range(n):
                twgya__yej[i] = pd.isna(obj[i])
            return twgya__yej
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
    gbfq__khjc = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    qkqbf__zvo = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', gbfq__khjc, qkqbf__zvo, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    xnnxr__jcgmr = str(expr_node)
    return xnnxr__jcgmr.startswith('left.') or xnnxr__jcgmr.startswith('right.'
        )


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    itnru__sixl = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (itnru__sixl,))
    msmqc__dsfow = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        bvl__gpsnp = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        clg__eleqp = {('NOT_NA', msmqc__dsfow(mest__htlmh)): mest__htlmh for
            mest__htlmh in null_set}
        uha__flk, _, _ = _parse_query_expr(bvl__gpsnp, env, [], [], None,
            join_cleaned_cols=clg__eleqp)
        evvxz__ridlg = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            payn__lnhno = pd.core.computation.ops.BinOp('&', uha__flk,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = evvxz__ridlg
        return payn__lnhno

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                uef__qqm = set()
                dujn__gzall = set()
                ziux__tkej = _insert_NA_cond_body(expr_node.lhs, uef__qqm)
                fmwuk__uhva = _insert_NA_cond_body(expr_node.rhs, dujn__gzall)
                lxwp__zyqpp = uef__qqm.intersection(dujn__gzall)
                uef__qqm.difference_update(lxwp__zyqpp)
                dujn__gzall.difference_update(lxwp__zyqpp)
                null_set.update(lxwp__zyqpp)
                expr_node.lhs = append_null_checks(ziux__tkej, uef__qqm)
                expr_node.rhs = append_null_checks(fmwuk__uhva, dujn__gzall)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            qthdy__nkso = expr_node.name
            rdzk__fdgrs, col_name = qthdy__nkso.split('.')
            if rdzk__fdgrs == 'left':
                iyts__eckw = left_columns
                data = left_data
            else:
                iyts__eckw = right_columns
                data = right_data
            fgxhe__cpw = data[iyts__eckw.index(col_name)]
            if bodo.utils.typing.is_nullable(fgxhe__cpw):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    nqgpt__wjrp = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        ghnx__dtdvb = str(expr_node.lhs)
        gxgvy__zzv = str(expr_node.rhs)
        if ghnx__dtdvb.startswith('left.') and gxgvy__zzv.startswith('left.'
            ) or ghnx__dtdvb.startswith('right.') and gxgvy__zzv.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [ghnx__dtdvb.split('.')[1]]
        right_on = [gxgvy__zzv.split('.')[1]]
        if ghnx__dtdvb.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        awoao__feft, soo__gvk, fdfi__jlk = _extract_equal_conds(expr_node.lhs)
        thjj__bvs, rok__vkh, qsuur__qugki = _extract_equal_conds(expr_node.rhs)
        left_on = awoao__feft + thjj__bvs
        right_on = soo__gvk + rok__vkh
        if fdfi__jlk is None:
            return left_on, right_on, qsuur__qugki
        if qsuur__qugki is None:
            return left_on, right_on, fdfi__jlk
        expr_node.lhs = fdfi__jlk
        expr_node.rhs = qsuur__qugki
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    itnru__sixl = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (itnru__sixl,))
    tgj__kgnwj = dict()
    msmqc__dsfow = pd.core.computation.parsing.clean_column_name
    for name, cenba__ofxql in (('left', left_columns), ('right', right_columns)
        ):
        for mest__htlmh in cenba__ofxql:
            oaq__uqiux = msmqc__dsfow(mest__htlmh)
            quxom__quwu = name, oaq__uqiux
            if quxom__quwu in tgj__kgnwj:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{mest__htlmh}' and '{tgj__kgnwj[oaq__uqiux]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            tgj__kgnwj[quxom__quwu] = mest__htlmh
    wyrl__ohh, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=tgj__kgnwj)
    left_on, right_on, wgfdu__suelc = _extract_equal_conds(wyrl__ohh.terms)
    return left_on, right_on, _insert_NA_cond(wgfdu__suelc, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    bxjt__ntmka = dict(sort=sort, copy=copy, validate=validate)
    vvy__rqgxw = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    sryl__adqx = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    efuv__vxs = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in sryl__adqx and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, gbiy__yiwjr = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if gbiy__yiwjr is None:
                    efuv__vxs = ''
                else:
                    efuv__vxs = str(gbiy__yiwjr)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = sryl__adqx
        right_keys = sryl__adqx
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
    myp__feg = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        clawv__mhjsm = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        clawv__mhjsm = list(get_overload_const_list(suffixes))
    suffix_x = clawv__mhjsm[0]
    suffix_y = clawv__mhjsm[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    dmfgp__ravdg = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    dmfgp__ravdg += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    dmfgp__ravdg += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    dmfgp__ravdg += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, myp__feg, efuv__vxs))
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo}, fsfb__fbqpn)
    _impl = fsfb__fbqpn['_impl']
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
    ryhpd__jnpg = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    rtdam__aigs = {get_overload_const_str(rlxu__epgy) for rlxu__epgy in (
        left_on, right_on, on) if is_overload_constant_str(rlxu__epgy)}
    for df in (left, right):
        for i, mest__htlmh in enumerate(df.data):
            if not isinstance(mest__htlmh, valid_dataframe_column_types
                ) and mest__htlmh not in ryhpd__jnpg:
                raise BodoError(
                    f'{name_func}(): use of column with {type(mest__htlmh)} in merge unsupported'
                    )
            if df.columns[i] in rtdam__aigs and isinstance(mest__htlmh,
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
        clawv__mhjsm = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        clawv__mhjsm = list(get_overload_const_list(suffixes))
    if len(clawv__mhjsm) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    sryl__adqx = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        uie__apc = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            uie__apc = on_str not in sryl__adqx and ('left.' in on_str or 
                'right.' in on_str)
        if len(sryl__adqx) == 0 and not uie__apc:
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
    kfl__nwpd = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            iucq__dzx = left.index
            kwp__gcl = isinstance(iucq__dzx, StringIndexType)
            yvbyp__hsl = right.index
            sqme__zbi = isinstance(yvbyp__hsl, StringIndexType)
        elif is_overload_true(left_index):
            iucq__dzx = left.index
            kwp__gcl = isinstance(iucq__dzx, StringIndexType)
            yvbyp__hsl = right.data[right.columns.index(right_keys[0])]
            sqme__zbi = yvbyp__hsl.dtype == string_type
        elif is_overload_true(right_index):
            iucq__dzx = left.data[left.columns.index(left_keys[0])]
            kwp__gcl = iucq__dzx.dtype == string_type
            yvbyp__hsl = right.index
            sqme__zbi = isinstance(yvbyp__hsl, StringIndexType)
        if kwp__gcl and sqme__zbi:
            return
        iucq__dzx = iucq__dzx.dtype
        yvbyp__hsl = yvbyp__hsl.dtype
        try:
            hqgw__xfkr = kfl__nwpd.resolve_function_type(operator.eq, (
                iucq__dzx, yvbyp__hsl), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=iucq__dzx, rk_dtype=yvbyp__hsl))
    else:
        for jyhym__uijuo, srlc__utuxq in zip(left_keys, right_keys):
            iucq__dzx = left.data[left.columns.index(jyhym__uijuo)].dtype
            ptoqh__zrfr = left.data[left.columns.index(jyhym__uijuo)]
            yvbyp__hsl = right.data[right.columns.index(srlc__utuxq)].dtype
            btsq__mpkbc = right.data[right.columns.index(srlc__utuxq)]
            if ptoqh__zrfr == btsq__mpkbc:
                continue
            jyigw__yhmyi = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=jyhym__uijuo, lk_dtype=iucq__dzx, rk=srlc__utuxq,
                rk_dtype=yvbyp__hsl))
            jrk__clysl = iucq__dzx == string_type
            cuu__ckst = yvbyp__hsl == string_type
            if jrk__clysl ^ cuu__ckst:
                raise_bodo_error(jyigw__yhmyi)
            try:
                hqgw__xfkr = kfl__nwpd.resolve_function_type(operator.eq, (
                    iucq__dzx, yvbyp__hsl), {})
            except:
                raise_bodo_error(jyigw__yhmyi)


def validate_keys(keys, df):
    neg__iqfm = set(keys).difference(set(df.columns))
    if len(neg__iqfm) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in neg__iqfm:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {neg__iqfm} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    bxjt__ntmka = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    vvy__rqgxw = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', bxjt__ntmka, vvy__rqgxw,
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
    dmfgp__ravdg = "def _impl(left, other, on=None, how='left',\n"
    dmfgp__ravdg += "    lsuffix='', rsuffix='', sort=False):\n"
    dmfgp__ravdg += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo}, fsfb__fbqpn)
    _impl = fsfb__fbqpn['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        dojo__phuk = get_overload_const_list(on)
        validate_keys(dojo__phuk, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    sryl__adqx = tuple(set(left.columns) & set(other.columns))
    if len(sryl__adqx) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=sryl__adqx))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    nmn__jjpqb = set(left_keys) & set(right_keys)
    uogqj__mrmw = set(left_columns) & set(right_columns)
    jxsvw__ewbx = uogqj__mrmw - nmn__jjpqb
    zzqoj__htpl = set(left_columns) - uogqj__mrmw
    apy__kjkan = set(right_columns) - uogqj__mrmw
    munw__jeolp = {}

    def insertOutColumn(col_name):
        if col_name in munw__jeolp:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        munw__jeolp[col_name] = 0
    for mzzi__tmv in nmn__jjpqb:
        insertOutColumn(mzzi__tmv)
    for mzzi__tmv in jxsvw__ewbx:
        wsp__zwhx = str(mzzi__tmv) + suffix_x
        bvcyw__rhu = str(mzzi__tmv) + suffix_y
        insertOutColumn(wsp__zwhx)
        insertOutColumn(bvcyw__rhu)
    for mzzi__tmv in zzqoj__htpl:
        insertOutColumn(mzzi__tmv)
    for mzzi__tmv in apy__kjkan:
        insertOutColumn(mzzi__tmv)
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
    sryl__adqx = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = sryl__adqx
        right_keys = sryl__adqx
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
        clawv__mhjsm = suffixes
    if is_overload_constant_list(suffixes):
        clawv__mhjsm = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        clawv__mhjsm = suffixes.value
    suffix_x = clawv__mhjsm[0]
    suffix_y = clawv__mhjsm[1]
    dmfgp__ravdg = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    dmfgp__ravdg += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    dmfgp__ravdg += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    dmfgp__ravdg += "    allow_exact_matches=True, direction='backward'):\n"
    dmfgp__ravdg += '  suffix_x = suffixes[0]\n'
    dmfgp__ravdg += '  suffix_y = suffixes[1]\n'
    dmfgp__ravdg += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo}, fsfb__fbqpn)
    _impl = fsfb__fbqpn['_impl']
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
    bxjt__ntmka = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    iiwhi__nmk = dict(sort=False, group_keys=True, squeeze=False, observed=True
        )
    check_unsupported_args('Dataframe.groupby', bxjt__ntmka, iiwhi__nmk,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    fboru__thj = func_name == 'DataFrame.pivot_table'
    if fboru__thj:
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
    qiog__jen = get_literal_value(columns)
    if isinstance(qiog__jen, (list, tuple)):
        if len(qiog__jen) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {qiog__jen}"
                )
        qiog__jen = qiog__jen[0]
    if qiog__jen not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {qiog__jen} not found in DataFrame {df}."
            )
    lek__ypftw = df.column_index[qiog__jen]
    if is_overload_none(index):
        vbq__nzxpr = []
        wkffd__cse = []
    else:
        wkffd__cse = get_literal_value(index)
        if not isinstance(wkffd__cse, (list, tuple)):
            wkffd__cse = [wkffd__cse]
        vbq__nzxpr = []
        for index in wkffd__cse:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            vbq__nzxpr.append(df.column_index[index])
    if not (all(isinstance(fpfwa__qwkqo, int) for fpfwa__qwkqo in
        wkffd__cse) or all(isinstance(fpfwa__qwkqo, str) for fpfwa__qwkqo in
        wkffd__cse)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        ppg__fha = []
        vugzh__bjrel = []
        guwj__pbuh = vbq__nzxpr + [lek__ypftw]
        for i, fpfwa__qwkqo in enumerate(df.columns):
            if i not in guwj__pbuh:
                ppg__fha.append(i)
                vugzh__bjrel.append(fpfwa__qwkqo)
    else:
        vugzh__bjrel = get_literal_value(values)
        if not isinstance(vugzh__bjrel, (list, tuple)):
            vugzh__bjrel = [vugzh__bjrel]
        ppg__fha = []
        for val in vugzh__bjrel:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            ppg__fha.append(df.column_index[val])
    if all(isinstance(fpfwa__qwkqo, int) for fpfwa__qwkqo in vugzh__bjrel):
        vugzh__bjrel = np.array(vugzh__bjrel, 'int64')
    elif all(isinstance(fpfwa__qwkqo, str) for fpfwa__qwkqo in vugzh__bjrel):
        vugzh__bjrel = pd.array(vugzh__bjrel, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    vmot__oen = set(ppg__fha) | set(vbq__nzxpr) | {lek__ypftw}
    if len(vmot__oen) != len(ppg__fha) + len(vbq__nzxpr) + 1:
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
    if len(vbq__nzxpr) == 0:
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
        for yaq__qdpg in vbq__nzxpr:
            index_column = df.data[yaq__qdpg]
            check_valid_index_typ(index_column)
    kwh__mdw = df.data[lek__ypftw]
    if isinstance(kwh__mdw, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(kwh__mdw, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for ecuuc__zlwr in ppg__fha:
        pqw__xmlxm = df.data[ecuuc__zlwr]
        if isinstance(pqw__xmlxm, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or pqw__xmlxm == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (wkffd__cse, qiog__jen, vugzh__bjrel, vbq__nzxpr, lek__ypftw,
        ppg__fha)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (wkffd__cse, qiog__jen, vugzh__bjrel, yaq__qdpg, lek__ypftw, xeskx__ikrcd
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(wkffd__cse) == 0:
        if is_overload_none(data.index.name_typ):
            wkffd__cse = [None]
        else:
            wkffd__cse = [get_literal_value(data.index.name_typ)]
    if len(vugzh__bjrel) == 1:
        kss__tni = None
    else:
        kss__tni = vugzh__bjrel
    dmfgp__ravdg = 'def impl(data, index=None, columns=None, values=None):\n'
    dmfgp__ravdg += f'    pivot_values = data.iloc[:, {lek__ypftw}].unique()\n'
    dmfgp__ravdg += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(yaq__qdpg) == 0:
        dmfgp__ravdg += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        dmfgp__ravdg += '        (\n'
        for phzr__mdl in yaq__qdpg:
            dmfgp__ravdg += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {phzr__mdl}),
"""
        dmfgp__ravdg += '        ),\n'
    dmfgp__ravdg += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {lek__ypftw}),),
"""
    dmfgp__ravdg += '        (\n'
    for ecuuc__zlwr in xeskx__ikrcd:
        dmfgp__ravdg += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {ecuuc__zlwr}),
"""
    dmfgp__ravdg += '        ),\n'
    dmfgp__ravdg += '        pivot_values,\n'
    dmfgp__ravdg += '        index_lit_tup,\n'
    dmfgp__ravdg += '        columns_lit,\n'
    dmfgp__ravdg += '        values_name_const,\n'
    dmfgp__ravdg += '    )\n'
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'index_lit_tup': tuple(wkffd__cse),
        'columns_lit': qiog__jen, 'values_name_const': kss__tni}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
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
    bxjt__ntmka = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed, sort=sort)
    vvy__rqgxw = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (wkffd__cse, qiog__jen, vugzh__bjrel, yaq__qdpg, lek__ypftw,
            xeskx__ikrcd) = (pivot_error_checking(data, index, columns,
            values, 'DataFrame.pivot_table'))
        if len(vugzh__bjrel) == 1:
            kss__tni = None
        else:
            kss__tni = vugzh__bjrel
        dmfgp__ravdg = 'def impl(\n'
        dmfgp__ravdg += '    data,\n'
        dmfgp__ravdg += '    values=None,\n'
        dmfgp__ravdg += '    index=None,\n'
        dmfgp__ravdg += '    columns=None,\n'
        dmfgp__ravdg += '    aggfunc="mean",\n'
        dmfgp__ravdg += '    fill_value=None,\n'
        dmfgp__ravdg += '    margins=False,\n'
        dmfgp__ravdg += '    dropna=True,\n'
        dmfgp__ravdg += '    margins_name="All",\n'
        dmfgp__ravdg += '    observed=False,\n'
        dmfgp__ravdg += '    sort=True,\n'
        dmfgp__ravdg += '    _pivot_values=None,\n'
        dmfgp__ravdg += '):\n'
        vlhol__rvlz = yaq__qdpg + [lek__ypftw] + xeskx__ikrcd
        dmfgp__ravdg += f'    data = data.iloc[:, {vlhol__rvlz}]\n'
        nvgzc__csseh = wkffd__cse + [qiog__jen]
        dmfgp__ravdg += (
            f'    data = data.groupby({nvgzc__csseh!r}, as_index=False).agg(aggfunc)\n'
            )
        dmfgp__ravdg += (
            f'    pivot_values = data.iloc[:, {len(yaq__qdpg)}].unique()\n')
        dmfgp__ravdg += (
            '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n')
        dmfgp__ravdg += '        (\n'
        for i in range(0, len(yaq__qdpg)):
            dmfgp__ravdg += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        dmfgp__ravdg += '        ),\n'
        dmfgp__ravdg += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(yaq__qdpg)}),),
"""
        dmfgp__ravdg += '        (\n'
        for i in range(len(yaq__qdpg) + 1, len(xeskx__ikrcd) + len(
            yaq__qdpg) + 1):
            dmfgp__ravdg += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        dmfgp__ravdg += '        ),\n'
        dmfgp__ravdg += '        pivot_values,\n'
        dmfgp__ravdg += '        index_lit_tup,\n'
        dmfgp__ravdg += '        columns_lit,\n'
        dmfgp__ravdg += '        values_name_const,\n'
        dmfgp__ravdg += '        check_duplicates=False,\n'
        dmfgp__ravdg += '    )\n'
        fsfb__fbqpn = {}
        exec(dmfgp__ravdg, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(wkffd__cse), 'columns_lit': qiog__jen,
            'values_name_const': kss__tni}, fsfb__fbqpn)
        impl = fsfb__fbqpn['impl']
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
    bxjt__ntmka = dict(col_level=col_level, ignore_index=ignore_index)
    vvy__rqgxw = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', bxjt__ntmka, vvy__rqgxw,
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
    giz__tiay = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(giz__tiay, (list, tuple)):
        giz__tiay = [giz__tiay]
    for fpfwa__qwkqo in giz__tiay:
        if fpfwa__qwkqo not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {fpfwa__qwkqo} not found in {frame}."
                )
    wywvz__eqwvj = [frame.column_index[i] for i in giz__tiay]
    if is_overload_none(value_vars):
        rjkzo__nchby = []
        zsftr__mfu = []
        for i, fpfwa__qwkqo in enumerate(frame.columns):
            if i not in wywvz__eqwvj:
                rjkzo__nchby.append(i)
                zsftr__mfu.append(fpfwa__qwkqo)
    else:
        zsftr__mfu = get_literal_value(value_vars)
        if not isinstance(zsftr__mfu, (list, tuple)):
            zsftr__mfu = [zsftr__mfu]
        zsftr__mfu = [v for v in zsftr__mfu if v not in giz__tiay]
        if not zsftr__mfu:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        rjkzo__nchby = []
        for val in zsftr__mfu:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            rjkzo__nchby.append(frame.column_index[val])
    for fpfwa__qwkqo in zsftr__mfu:
        if fpfwa__qwkqo not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {fpfwa__qwkqo} not found in {frame}."
                )
    if not (all(isinstance(fpfwa__qwkqo, int) for fpfwa__qwkqo in
        zsftr__mfu) or all(isinstance(fpfwa__qwkqo, str) for fpfwa__qwkqo in
        zsftr__mfu)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    cvn__oipil = frame.data[rjkzo__nchby[0]]
    ohhpl__wbgwo = [frame.data[i].dtype for i in rjkzo__nchby]
    rjkzo__nchby = np.array(rjkzo__nchby, dtype=np.int64)
    wywvz__eqwvj = np.array(wywvz__eqwvj, dtype=np.int64)
    _, zepsw__ceuh = bodo.utils.typing.get_common_scalar_dtype(ohhpl__wbgwo)
    if not zepsw__ceuh:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': zsftr__mfu, 'val_type': cvn__oipil}
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
    if frame.is_table_format and all(v == cvn__oipil.dtype for v in
        ohhpl__wbgwo):
        extra_globals['value_idxs'] = rjkzo__nchby
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(zsftr__mfu) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {rjkzo__nchby[0]})
"""
    else:
        wruix__loq = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in rjkzo__nchby)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({wruix__loq},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in wywvz__eqwvj:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(zsftr__mfu)})\n'
            )
    yjik__bkaug = ', '.join(f'out_id{i}' for i in wywvz__eqwvj) + (', ' if 
        len(wywvz__eqwvj) > 0 else '')
    data_args = yjik__bkaug + 'var_col, val_col'
    columns = tuple(giz__tiay + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(zsftr__mfu)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    bxjt__ntmka = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    vvy__rqgxw = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', bxjt__ntmka, vvy__rqgxw,
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
    bxjt__ntmka = dict(ignore_index=ignore_index, key=key)
    vvy__rqgxw = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', bxjt__ntmka, vvy__rqgxw,
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
    fnu__bwabj = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        fnu__bwabj.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        lex__cfh = [get_overload_const_tuple(by)]
    else:
        lex__cfh = get_overload_const_list(by)
    lex__cfh = set((k, '') if (k, '') in fnu__bwabj else k for k in lex__cfh)
    if len(lex__cfh.difference(fnu__bwabj)) > 0:
        kip__vjme = list(set(get_overload_const_list(by)).difference(
            fnu__bwabj))
        raise_bodo_error(f'sort_values(): invalid keys {kip__vjme} for by.')
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
        pkgdf__diac = get_overload_const_list(na_position)
        for na_position in pkgdf__diac:
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
    bxjt__ntmka = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    vvy__rqgxw = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', bxjt__ntmka, vvy__rqgxw,
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
    bxjt__ntmka = dict(limit=limit, downcast=downcast)
    vvy__rqgxw = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', bxjt__ntmka, vvy__rqgxw,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    jpcn__mdip = not is_overload_none(value)
    aipxk__uwght = not is_overload_none(method)
    if jpcn__mdip and aipxk__uwght:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not jpcn__mdip and not aipxk__uwght:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if jpcn__mdip:
        ivuq__aos = 'value=value'
    else:
        ivuq__aos = 'method=method'
    data_args = [(
        f"df['{fpfwa__qwkqo}'].fillna({ivuq__aos}, inplace=inplace)" if
        isinstance(fpfwa__qwkqo, str) else
        f'df[{fpfwa__qwkqo}].fillna({ivuq__aos}, inplace=inplace)') for
        fpfwa__qwkqo in df.columns]
    dmfgp__ravdg = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        dmfgp__ravdg += '  ' + '  \n'.join(data_args) + '\n'
        fsfb__fbqpn = {}
        exec(dmfgp__ravdg, {}, fsfb__fbqpn)
        impl = fsfb__fbqpn['impl']
        return impl
    else:
        return _gen_init_df(dmfgp__ravdg, df.columns, ', '.join(dmin__hljms +
            '.values' for dmin__hljms in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    bxjt__ntmka = dict(col_level=col_level, col_fill=col_fill)
    vvy__rqgxw = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', bxjt__ntmka, vvy__rqgxw,
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
    dmfgp__ravdg = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    dmfgp__ravdg += (
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
        dpqxt__rubp = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            dpqxt__rubp)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            dmfgp__ravdg += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            tjxfg__wwe = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = tjxfg__wwe + data_args
        else:
            qpi__ntt = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [qpi__ntt] + data_args
    return _gen_init_df(dmfgp__ravdg, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    mjs__vspq = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and mjs__vspq == 1 or is_overload_constant_list(level) and list(
        get_overload_const_list(level)) == list(range(mjs__vspq))


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
        mtzcx__zfndc = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        vxf__zgsvs = get_overload_const_list(subset)
        mtzcx__zfndc = []
        for ggjxw__sfbu in vxf__zgsvs:
            if ggjxw__sfbu not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{ggjxw__sfbu}' not in data frame columns {df}"
                    )
            mtzcx__zfndc.append(df.column_index[ggjxw__sfbu])
    buym__fsqj = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(buym__fsqj))
    dmfgp__ravdg = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(buym__fsqj):
        dmfgp__ravdg += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    dmfgp__ravdg += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in mtzcx__zfndc)))
    dmfgp__ravdg += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(dmfgp__ravdg, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    bxjt__ntmka = dict(index=index, level=level, errors=errors)
    vvy__rqgxw = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', bxjt__ntmka, vvy__rqgxw,
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
            txdv__zox = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            txdv__zox = get_overload_const_list(labels)
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
            txdv__zox = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            txdv__zox = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for fpfwa__qwkqo in txdv__zox:
        if fpfwa__qwkqo not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(fpfwa__qwkqo, df.columns))
    if len(set(txdv__zox)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    nfey__hai = tuple(fpfwa__qwkqo for fpfwa__qwkqo in df.columns if 
        fpfwa__qwkqo not in txdv__zox)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[fpfwa__qwkqo], '.copy()' if not inplace else
        '') for fpfwa__qwkqo in nfey__hai)
    dmfgp__ravdg = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    dmfgp__ravdg += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(dmfgp__ravdg, nfey__hai, data_args, index)


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
    bxjt__ntmka = dict(random_state=random_state, weights=weights, axis=
        axis, ignore_index=ignore_index)
    xolpj__ilxzy = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', bxjt__ntmka, xolpj__ilxzy,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    buym__fsqj = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(buym__fsqj))
    pdv__tyey = ', '.join('rhs_data_{}'.format(i) for i in range(buym__fsqj))
    dmfgp__ravdg = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    dmfgp__ravdg += '  if (frac == 1 or n == len(df)) and not replace:\n'
    dmfgp__ravdg += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(buym__fsqj):
        dmfgp__ravdg += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    dmfgp__ravdg += '  if frac is None:\n'
    dmfgp__ravdg += '    frac_d = -1.0\n'
    dmfgp__ravdg += '  else:\n'
    dmfgp__ravdg += '    frac_d = frac\n'
    dmfgp__ravdg += '  if n is None:\n'
    dmfgp__ravdg += '    n_i = 0\n'
    dmfgp__ravdg += '  else:\n'
    dmfgp__ravdg += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    dmfgp__ravdg += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({pdv__tyey},), {index}, n_i, frac_d, replace)
"""
    dmfgp__ravdg += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(dmfgp__ravdg, df.
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
    gbfq__khjc = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    qkqbf__zvo = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', gbfq__khjc, qkqbf__zvo,
        package_name='pandas', module_name='DataFrame')
    uwgjm__ukb = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            sel__jpm = uwgjm__ukb + '\n'
            sel__jpm += 'Index: 0 entries\n'
            sel__jpm += 'Empty DataFrame'
            print(sel__jpm)
        return _info_impl
    else:
        dmfgp__ravdg = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        dmfgp__ravdg += '    ncols = df.shape[1]\n'
        dmfgp__ravdg += f'    lines = "{uwgjm__ukb}\\n"\n'
        dmfgp__ravdg += f'    lines += "{df.index}: "\n'
        dmfgp__ravdg += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            dmfgp__ravdg += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            dmfgp__ravdg += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            dmfgp__ravdg += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        dmfgp__ravdg += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        dmfgp__ravdg += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        dmfgp__ravdg += '    column_width = max(space, 7)\n'
        dmfgp__ravdg += '    column= "Column"\n'
        dmfgp__ravdg += '    underl= "------"\n'
        dmfgp__ravdg += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        dmfgp__ravdg += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        dmfgp__ravdg += '    mem_size = 0\n'
        dmfgp__ravdg += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        dmfgp__ravdg += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        dmfgp__ravdg += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        zpb__byh = dict()
        for i in range(len(df.columns)):
            dmfgp__ravdg += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            xlpqm__ytygg = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                xlpqm__ytygg = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                jkvhj__qonh = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                xlpqm__ytygg = f'{jkvhj__qonh[:-7]}'
            dmfgp__ravdg += f'    col_dtype[{i}] = "{xlpqm__ytygg}"\n'
            if xlpqm__ytygg in zpb__byh:
                zpb__byh[xlpqm__ytygg] += 1
            else:
                zpb__byh[xlpqm__ytygg] = 1
            dmfgp__ravdg += f'    col_name[{i}] = "{df.columns[i]}"\n'
            dmfgp__ravdg += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        dmfgp__ravdg += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        dmfgp__ravdg += '    for i in column_info:\n'
        dmfgp__ravdg += "        lines += f'{i}\\n'\n"
        nxtt__jkp = ', '.join(f'{k}({zpb__byh[k]})' for k in sorted(zpb__byh))
        dmfgp__ravdg += f"    lines += 'dtypes: {nxtt__jkp}\\n'\n"
        dmfgp__ravdg += '    mem_size += df.index.nbytes\n'
        dmfgp__ravdg += '    total_size = _sizeof_fmt(mem_size)\n'
        dmfgp__ravdg += "    lines += f'memory usage: {total_size}'\n"
        dmfgp__ravdg += '    print(lines)\n'
        fsfb__fbqpn = {}
        exec(dmfgp__ravdg, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, fsfb__fbqpn)
        _info_impl = fsfb__fbqpn['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    dmfgp__ravdg = 'def impl(df, index=True, deep=False):\n'
    evln__cev = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes'
    utotp__qag = is_overload_true(index)
    columns = df.columns
    if utotp__qag:
        columns = ('Index',) + columns
    if len(columns) == 0:
        cxlmh__khe = ()
    elif all(isinstance(fpfwa__qwkqo, int) for fpfwa__qwkqo in columns):
        cxlmh__khe = np.array(columns, 'int64')
    elif all(isinstance(fpfwa__qwkqo, str) for fpfwa__qwkqo in columns):
        cxlmh__khe = pd.array(columns, 'string')
    else:
        cxlmh__khe = columns
    if df.is_table_format:
        qvai__zoog = int(utotp__qag)
        wti__xxa = len(columns)
        dmfgp__ravdg += f'  nbytes_arr = np.empty({wti__xxa}, np.int64)\n'
        dmfgp__ravdg += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        dmfgp__ravdg += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {qvai__zoog})
"""
        if utotp__qag:
            dmfgp__ravdg += f'  nbytes_arr[0] = {evln__cev}\n'
        dmfgp__ravdg += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if utotp__qag:
            data = f'{evln__cev},{data}'
        else:
            tcmzy__ecn = ',' if len(columns) == 1 else ''
            data = f'{data}{tcmzy__ecn}'
        dmfgp__ravdg += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        cxlmh__khe}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
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
    fhbt__lqxyh = 'read_excel_df{}'.format(next_label())
    setattr(types, fhbt__lqxyh, df_type)
    vilhu__nucf = False
    if is_overload_constant_list(parse_dates):
        vilhu__nucf = get_overload_const_list(parse_dates)
    njowb__dya = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    dmfgp__ravdg = f"""
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
    with numba.objmode(df="{fhbt__lqxyh}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{njowb__dya}}},
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
            parse_dates={vilhu__nucf},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, globals(), fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as wxq__qwdgt:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    dmfgp__ravdg = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    dmfgp__ravdg += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    dmfgp__ravdg += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        dmfgp__ravdg += '   fig, ax = plt.subplots()\n'
    else:
        dmfgp__ravdg += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        dmfgp__ravdg += '   fig.set_figwidth(figsize[0])\n'
        dmfgp__ravdg += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        dmfgp__ravdg += '   xlabel = x\n'
    dmfgp__ravdg += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        dmfgp__ravdg += '   ylabel = y\n'
    else:
        dmfgp__ravdg += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        dmfgp__ravdg += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        dmfgp__ravdg += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    dmfgp__ravdg += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            dmfgp__ravdg += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            fic__aghtr = get_overload_const_str(x)
            gddav__crx = df.columns.index(fic__aghtr)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if gddav__crx != i:
                        dmfgp__ravdg += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            dmfgp__ravdg += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        dmfgp__ravdg += '   ax.scatter(df[x], df[y], s=20)\n'
        dmfgp__ravdg += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        dmfgp__ravdg += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        dmfgp__ravdg += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        dmfgp__ravdg += '   ax.legend()\n'
    dmfgp__ravdg += '   return ax\n'
    fsfb__fbqpn = {}
    exec(dmfgp__ravdg, {'bodo': bodo, 'plt': plt}, fsfb__fbqpn)
    impl = fsfb__fbqpn['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for ixk__uegox in df_typ.data:
        if not (isinstance(ixk__uegox, IntegerArrayType) or isinstance(
            ixk__uegox.dtype, types.Number) or ixk__uegox.dtype in (bodo.
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
        lss__sddfc = args[0]
        miuwv__ght = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        tijte__bgn = lss__sddfc
        check_runtime_cols_unsupported(lss__sddfc, 'set_df_col()')
        if isinstance(lss__sddfc, DataFrameType):
            index = lss__sddfc.index
            if len(lss__sddfc.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(lss__sddfc.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if miuwv__ght in lss__sddfc.columns:
                nfey__hai = lss__sddfc.columns
                cbia__mdsor = lss__sddfc.columns.index(miuwv__ght)
                kynpf__pana = list(lss__sddfc.data)
                kynpf__pana[cbia__mdsor] = val
                kynpf__pana = tuple(kynpf__pana)
            else:
                nfey__hai = lss__sddfc.columns + (miuwv__ght,)
                kynpf__pana = lss__sddfc.data + (val,)
            tijte__bgn = DataFrameType(kynpf__pana, index, nfey__hai,
                lss__sddfc.dist, lss__sddfc.is_table_format)
        return tijte__bgn(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    gyv__mxb = {}

    def _rewrite_membership_op(self, node, left, right):
        xcps__tkuo = node.op
        op = self.visit(xcps__tkuo)
        return op, xcps__tkuo, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    fmk__wmb = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in fmk__wmb:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in fmk__wmb:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        crjsk__dyw = node.attr
        value = node.value
        ycnp__moj = pd.core.computation.ops.LOCAL_TAG
        if crjsk__dyw in ('str', 'dt'):
            try:
                kbzm__vrkjy = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as grk__akk:
                col_name = grk__akk.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            kbzm__vrkjy = str(self.visit(value))
        quxom__quwu = kbzm__vrkjy, crjsk__dyw
        if quxom__quwu in join_cleaned_cols:
            crjsk__dyw = join_cleaned_cols[quxom__quwu]
        name = kbzm__vrkjy + '.' + crjsk__dyw
        if name.startswith(ycnp__moj):
            name = name[len(ycnp__moj):]
        if crjsk__dyw in ('str', 'dt'):
            bnzgl__yked = columns[cleaned_columns.index(kbzm__vrkjy)]
            gyv__mxb[bnzgl__yked] = kbzm__vrkjy
            self.env.scope[name] = 0
            return self.term_type(ycnp__moj + name, self.env)
        fmk__wmb.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in fmk__wmb:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        ihuso__spo = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        miuwv__ght = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(ihuso__spo), miuwv__ght))

    def op__str__(self):
        qjjy__rkl = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            nzc__xqhlm)) for nzc__xqhlm in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(qjjy__rkl)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(qjjy__rkl)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(qjjy__rkl))
    bin__ipqya = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    vfw__ezi = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    gwg__hzhs = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    orsre__pae = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    tkb__jftzz = pd.core.computation.ops.Term.__str__
    uku__onnqo = pd.core.computation.ops.MathCall.__str__
    bbmhu__pbxd = pd.core.computation.ops.Op.__str__
    evvxz__ridlg = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        wyrl__ohh = pd.core.computation.expr.Expr(expr, env=env)
        tbsv__xqm = str(wyrl__ohh)
    except pd.core.computation.ops.UndefinedVariableError as grk__akk:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == grk__akk.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {grk__akk}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            bin__ipqya)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            vfw__ezi)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = gwg__hzhs
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = orsre__pae
        pd.core.computation.ops.Term.__str__ = tkb__jftzz
        pd.core.computation.ops.MathCall.__str__ = uku__onnqo
        pd.core.computation.ops.Op.__str__ = bbmhu__pbxd
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            evvxz__ridlg)
    uvfu__mtcx = pd.core.computation.parsing.clean_column_name
    gyv__mxb.update({fpfwa__qwkqo: uvfu__mtcx(fpfwa__qwkqo) for
        fpfwa__qwkqo in columns if uvfu__mtcx(fpfwa__qwkqo) in wyrl__ohh.names}
        )
    return wyrl__ohh, tbsv__xqm, gyv__mxb


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        rmrr__mgr = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(rmrr__mgr))
        mlefv__ifv = namedtuple('Pandas', col_names)
        bmy__nravw = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], mlefv__ifv)
        super(DataFrameTupleIterator, self).__init__(name, bmy__nravw)

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
        hwcjp__eynv = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        hwcjp__eynv = [types.Array(types.int64, 1, 'C')] + hwcjp__eynv
        mrj__mebc = DataFrameTupleIterator(col_names, hwcjp__eynv)
        return mrj__mebc(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        icgpp__xtcu = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            icgpp__xtcu)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    zhj__ajnfc = args[len(args) // 2:]
    axob__pigh = sig.args[len(sig.args) // 2:]
    kje__xyqqx = context.make_helper(builder, sig.return_type)
    hkaka__cxu = context.get_constant(types.intp, 0)
    moh__dazwi = cgutils.alloca_once_value(builder, hkaka__cxu)
    kje__xyqqx.index = moh__dazwi
    for i, arr in enumerate(zhj__ajnfc):
        setattr(kje__xyqqx, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(zhj__ajnfc, axob__pigh):
        context.nrt.incref(builder, arr_typ, arr)
    res = kje__xyqqx._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    kcdh__excm, = sig.args
    aeui__ksfy, = args
    kje__xyqqx = context.make_helper(builder, kcdh__excm, value=aeui__ksfy)
    wxvoy__zyjav = signature(types.intp, kcdh__excm.array_types[1])
    uzr__nkok = context.compile_internal(builder, lambda a: len(a),
        wxvoy__zyjav, [kje__xyqqx.array0])
    index = builder.load(kje__xyqqx.index)
    chvie__mgvo = builder.icmp_signed('<', index, uzr__nkok)
    result.set_valid(chvie__mgvo)
    with builder.if_then(chvie__mgvo):
        values = [index]
        for i, arr_typ in enumerate(kcdh__excm.array_types[1:]):
            yonc__mgu = getattr(kje__xyqqx, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                xvxjv__gvjq = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    xvxjv__gvjq, [yonc__mgu, index])
            else:
                xvxjv__gvjq = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    xvxjv__gvjq, [yonc__mgu, index])
            values.append(val)
        value = context.make_tuple(builder, kcdh__excm.yield_type, values)
        result.yield_(value)
        pecsj__xymc = cgutils.increment_index(builder, index)
        builder.store(pecsj__xymc, kje__xyqqx.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    dvcf__dqoyv = ir.Assign(rhs, lhs, expr.loc)
    ekxru__njxy = lhs
    vazwb__uge = []
    enyg__eul = []
    usyvw__dsafq = typ.count
    for i in range(usyvw__dsafq):
        cflol__fac = ir.Var(ekxru__njxy.scope, mk_unique_var('{}_size{}'.
            format(ekxru__njxy.name, i)), ekxru__njxy.loc)
        wxk__gbqot = ir.Expr.static_getitem(lhs, i, None, ekxru__njxy.loc)
        self.calltypes[wxk__gbqot] = None
        vazwb__uge.append(ir.Assign(wxk__gbqot, cflol__fac, ekxru__njxy.loc))
        self._define(equiv_set, cflol__fac, types.intp, wxk__gbqot)
        enyg__eul.append(cflol__fac)
    aqvwi__onmdz = tuple(enyg__eul)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        aqvwi__onmdz, pre=[dvcf__dqoyv] + vazwb__uge)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
