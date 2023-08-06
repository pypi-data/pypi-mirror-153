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
        dpnrs__xkr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({dpnrs__xkr})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    tvi__nva = 'def impl(df):\n'
    if df.has_runtime_cols:
        tvi__nva += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        sztvp__bgdo = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        tvi__nva += f'  return {sztvp__bgdo}'
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo}, cwa__nvjj)
    impl = cwa__nvjj['impl']
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
    jngnb__yxdo = len(df.columns)
    vssjy__gdrmi = set(i for i in range(jngnb__yxdo) if isinstance(df.data[
        i], IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in vssjy__gdrmi else '') for i in
        range(jngnb__yxdo))
    tvi__nva = 'def f(df):\n'.format()
    tvi__nva += '    return np.stack(({},), 1)\n'.format(data_args)
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'np': np}, cwa__nvjj)
    gvoa__gxpud = cwa__nvjj['f']
    return gvoa__gxpud


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
    bvhxd__dzin = {'dtype': dtype, 'na_value': na_value}
    kiamp__jjcud = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', bvhxd__dzin, kiamp__jjcud,
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
            sacfv__hsmq = bodo.hiframes.table.compute_num_runtime_columns(t)
            return sacfv__hsmq * len(t)
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
            sacfv__hsmq = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), sacfv__hsmq
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    tvi__nva = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    eyqtl__uiujm = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    tvi__nva += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{eyqtl__uiujm}), {index}, None)
"""
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo}, cwa__nvjj)
    impl = cwa__nvjj['impl']
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
    bvhxd__dzin = {'copy': copy, 'errors': errors}
    kiamp__jjcud = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', bvhxd__dzin, kiamp__jjcud,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        omo__kvf = _bodo_object_typeref.instance_type
        assert isinstance(omo__kvf, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        ltu__jnozc = {}
        for i, name in enumerate(omo__kvf.columns):
            arr_typ = omo__kvf.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                mpl__sbb = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                mpl__sbb = boolean_dtype
            else:
                mpl__sbb = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = mpl__sbb
            ltu__jnozc[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {ltu__jnozc[pnkk__ivfi]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if pnkk__ivfi in ltu__jnozc else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, pnkk__ivfi in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        vys__xdj = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(vys__xdj[pnkk__ivfi])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if pnkk__ivfi in vys__xdj else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, pnkk__ivfi in enumerate(df.columns))
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
        foa__bbwd = types.none
        extra_globals = {'output_arr_typ': foa__bbwd}
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
        shsz__qao = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                shsz__qao.append(arr + '.copy()')
            elif is_overload_false(deep):
                shsz__qao.append(arr)
            else:
                shsz__qao.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(shsz__qao)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    bvhxd__dzin = {'index': index, 'level': level, 'errors': errors}
    kiamp__jjcud = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', bvhxd__dzin, kiamp__jjcud,
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
        aaym__osjl = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        aaym__osjl = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    vlmsq__igwo = tuple([aaym__osjl.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        out_df_type = df.copy(columns=vlmsq__igwo)
        foa__bbwd = types.none
        extra_globals = {'output_arr_typ': foa__bbwd}
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
        shsz__qao = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                shsz__qao.append(arr + '.copy()')
            elif is_overload_false(copy):
                shsz__qao.append(arr)
            else:
                shsz__qao.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(shsz__qao)
    return _gen_init_df(header, vlmsq__igwo, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    pqdu__cqog = not is_overload_none(items)
    tqtq__idvb = not is_overload_none(like)
    eax__hnv = not is_overload_none(regex)
    hbtmr__etnm = pqdu__cqog ^ tqtq__idvb ^ eax__hnv
    nevoh__wvql = not (pqdu__cqog or tqtq__idvb or eax__hnv)
    if nevoh__wvql:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not hbtmr__etnm:
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
        cdsg__nxt = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        cdsg__nxt = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert cdsg__nxt in {0, 1}
    tvi__nva = 'def impl(df, items=None, like=None, regex=None, axis=None):\n'
    if cdsg__nxt == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if cdsg__nxt == 1:
        bbxzk__utn = []
        anb__idow = []
        eobx__jubdc = []
        if pqdu__cqog:
            if is_overload_constant_list(items):
                emvny__ebay = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if tqtq__idvb:
            if is_overload_constant_str(like):
                zldfq__gvvxj = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if eax__hnv:
            if is_overload_constant_str(regex):
                dmyih__qwef = get_overload_const_str(regex)
                azj__nme = re.compile(dmyih__qwef)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, pnkk__ivfi in enumerate(df.columns):
            if not is_overload_none(items
                ) and pnkk__ivfi in emvny__ebay or not is_overload_none(like
                ) and zldfq__gvvxj in str(pnkk__ivfi) or not is_overload_none(
                regex) and azj__nme.search(str(pnkk__ivfi)):
                anb__idow.append(pnkk__ivfi)
                eobx__jubdc.append(i)
        for i in eobx__jubdc:
            var_name = f'data_{i}'
            bbxzk__utn.append(var_name)
            tvi__nva += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(bbxzk__utn)
        return _gen_init_df(tvi__nva, anb__idow, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        foa__bbwd = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([foa__bbwd] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': foa__bbwd}
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
    uymrr__yaia = is_overload_none(include)
    zsom__xpbv = is_overload_none(exclude)
    exq__vlx = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if uymrr__yaia and zsom__xpbv:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not uymrr__yaia:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            vyk__cngwy = [dtype_to_array_type(parse_dtype(elem, exq__vlx)) for
                elem in include]
        elif is_legal_input(include):
            vyk__cngwy = [dtype_to_array_type(parse_dtype(include, exq__vlx))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        vyk__cngwy = get_nullable_and_non_nullable_types(vyk__cngwy)
        lry__atcbt = tuple(pnkk__ivfi for i, pnkk__ivfi in enumerate(df.
            columns) if df.data[i] in vyk__cngwy)
    else:
        lry__atcbt = df.columns
    if not zsom__xpbv:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            bcr__brlj = [dtype_to_array_type(parse_dtype(elem, exq__vlx)) for
                elem in exclude]
        elif is_legal_input(exclude):
            bcr__brlj = [dtype_to_array_type(parse_dtype(exclude, exq__vlx))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        bcr__brlj = get_nullable_and_non_nullable_types(bcr__brlj)
        lry__atcbt = tuple(pnkk__ivfi for pnkk__ivfi in lry__atcbt if df.
            data[df.column_index[pnkk__ivfi]] not in bcr__brlj)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pnkk__ivfi]})'
         for pnkk__ivfi in lry__atcbt)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, lry__atcbt, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        foa__bbwd = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([foa__bbwd] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': foa__bbwd}
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
    fpou__lgoph = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in fpou__lgoph:
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
    fpou__lgoph = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in fpou__lgoph:
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
    tvi__nva = 'def impl(df, values):\n'
    sbitr__ovh = {}
    fxiwz__hslvi = False
    if isinstance(values, DataFrameType):
        fxiwz__hslvi = True
        for i, pnkk__ivfi in enumerate(df.columns):
            if pnkk__ivfi in values.column_index:
                ooprx__wzt = 'val{}'.format(i)
                tvi__nva += f"""  {ooprx__wzt} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[pnkk__ivfi]})
"""
                sbitr__ovh[pnkk__ivfi] = ooprx__wzt
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        sbitr__ovh = {pnkk__ivfi: 'values' for pnkk__ivfi in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        ooprx__wzt = 'data{}'.format(i)
        tvi__nva += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(ooprx__wzt, i))
        data.append(ooprx__wzt)
    ebq__futuj = ['out{}'.format(i) for i in range(len(df.columns))]
    eja__xrp = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    zri__qar = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    nxv__wzbj = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, dolmt__kphx) in enumerate(zip(df.columns, data)):
        if cname in sbitr__ovh:
            mzzso__wlz = sbitr__ovh[cname]
            if fxiwz__hslvi:
                tvi__nva += eja__xrp.format(dolmt__kphx, mzzso__wlz,
                    ebq__futuj[i])
            else:
                tvi__nva += zri__qar.format(dolmt__kphx, mzzso__wlz,
                    ebq__futuj[i])
        else:
            tvi__nva += nxv__wzbj.format(ebq__futuj[i])
    return _gen_init_df(tvi__nva, df.columns, ','.join(ebq__futuj))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    jngnb__yxdo = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(jngnb__yxdo))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    fvj__nvqg = [pnkk__ivfi for pnkk__ivfi, mttr__tjst in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(mttr__tjst.
        dtype)]
    assert len(fvj__nvqg) != 0
    fgs__nvjag = ''
    if not any(mttr__tjst == types.float64 for mttr__tjst in df.data):
        fgs__nvjag = '.astype(np.float64)'
    kfec__fwyu = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[pnkk__ivfi], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[pnkk__ivfi]], IntegerArrayType) or
        df.data[df.column_index[pnkk__ivfi]] == boolean_array else '') for
        pnkk__ivfi in fvj__nvqg)
    gcb__sygu = 'np.stack(({},), 1){}'.format(kfec__fwyu, fgs__nvjag)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(fvj__nvqg)))
    index = f'{generate_col_to_index_func_text(fvj__nvqg)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(gcb__sygu)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, fvj__nvqg, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    zdf__eghnt = dict(ddof=ddof)
    lovy__xcvh = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    zgqtc__azdh = '1' if is_overload_none(min_periods) else 'min_periods'
    fvj__nvqg = [pnkk__ivfi for pnkk__ivfi, mttr__tjst in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(mttr__tjst.
        dtype)]
    if len(fvj__nvqg) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    fgs__nvjag = ''
    if not any(mttr__tjst == types.float64 for mttr__tjst in df.data):
        fgs__nvjag = '.astype(np.float64)'
    kfec__fwyu = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[pnkk__ivfi], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[pnkk__ivfi]], IntegerArrayType) or
        df.data[df.column_index[pnkk__ivfi]] == boolean_array else '') for
        pnkk__ivfi in fvj__nvqg)
    gcb__sygu = 'np.stack(({},), 1){}'.format(kfec__fwyu, fgs__nvjag)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(fvj__nvqg)))
    index = f'pd.Index({fvj__nvqg})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(gcb__sygu)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        zgqtc__azdh)
    return _gen_init_df(header, fvj__nvqg, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    zdf__eghnt = dict(axis=axis, level=level, numeric_only=numeric_only)
    lovy__xcvh = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    tvi__nva = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    tvi__nva += '  data = np.array([{}])\n'.format(data_args)
    sztvp__bgdo = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    tvi__nva += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {sztvp__bgdo})\n'
        )
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'np': np}, cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    zdf__eghnt = dict(axis=axis)
    lovy__xcvh = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    tvi__nva = 'def impl(df, axis=0, dropna=True):\n'
    tvi__nva += '  data = np.asarray(({},))\n'.format(data_args)
    sztvp__bgdo = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    tvi__nva += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {sztvp__bgdo})\n'
        )
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'np': np}, cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    zdf__eghnt = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    lovy__xcvh = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    zdf__eghnt = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    lovy__xcvh = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    zdf__eghnt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lovy__xcvh = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    zdf__eghnt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lovy__xcvh = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    zdf__eghnt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lovy__xcvh = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    zdf__eghnt = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    lovy__xcvh = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    zdf__eghnt = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    lovy__xcvh = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    zdf__eghnt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lovy__xcvh = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    zdf__eghnt = dict(numeric_only=numeric_only, interpolation=interpolation)
    lovy__xcvh = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    zdf__eghnt = dict(axis=axis, skipna=skipna)
    lovy__xcvh = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for jmus__fsw in df.data:
        if not (bodo.utils.utils.is_np_array_typ(jmus__fsw) and (jmus__fsw.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            jmus__fsw.dtype, (types.Number, types.Boolean))) or isinstance(
            jmus__fsw, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or
            jmus__fsw in [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {jmus__fsw} not supported.'
                )
        if isinstance(jmus__fsw, bodo.CategoricalArrayType
            ) and not jmus__fsw.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    zdf__eghnt = dict(axis=axis, skipna=skipna)
    lovy__xcvh = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for jmus__fsw in df.data:
        if not (bodo.utils.utils.is_np_array_typ(jmus__fsw) and (jmus__fsw.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            jmus__fsw.dtype, (types.Number, types.Boolean))) or isinstance(
            jmus__fsw, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or
            jmus__fsw in [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {jmus__fsw} not supported.'
                )
        if isinstance(jmus__fsw, bodo.CategoricalArrayType
            ) and not jmus__fsw.dtype.ordered:
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
        fvj__nvqg = tuple(pnkk__ivfi for pnkk__ivfi, mttr__tjst in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (mttr__tjst.dtype))
        out_colnames = fvj__nvqg
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            gaclg__dsq = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[pnkk__ivfi]].dtype) for pnkk__ivfi in out_colnames
                ]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(gaclg__dsq, []))
    except NotImplementedError as prl__nbx:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    zbbx__lbl = ''
    if func_name in ('sum', 'prod'):
        zbbx__lbl = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    tvi__nva = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, zbbx__lbl))
    if func_name == 'quantile':
        tvi__nva = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        tvi__nva = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        tvi__nva += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        tvi__nva += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    iox__qzeh = ''
    if func_name in ('min', 'max'):
        iox__qzeh = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        iox__qzeh = ', dtype=np.float32'
    jqafm__ziia = f'bodo.libs.array_ops.array_op_{func_name}'
    gwp__ytuw = ''
    if func_name in ['sum', 'prod']:
        gwp__ytuw = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        gwp__ytuw = 'index'
    elif func_name == 'quantile':
        gwp__ytuw = 'q'
    elif func_name in ['std', 'var']:
        gwp__ytuw = 'True, ddof'
    elif func_name == 'median':
        gwp__ytuw = 'True'
    data_args = ', '.join(
        f'{jqafm__ziia}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pnkk__ivfi]}), {gwp__ytuw})'
         for pnkk__ivfi in out_colnames)
    tvi__nva = ''
    if func_name in ('idxmax', 'idxmin'):
        tvi__nva += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        tvi__nva += ('  data = bodo.utils.conversion.coerce_to_array(({},))\n'
            .format(data_args))
    else:
        tvi__nva += '  data = np.asarray(({},){})\n'.format(data_args,
            iox__qzeh)
    tvi__nva += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return tvi__nva


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    fgg__fawh = [df_type.column_index[pnkk__ivfi] for pnkk__ivfi in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in fgg__fawh)
    twqb__pivs = '\n        '.join(f'row[{i}] = arr_{fgg__fawh[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    tqww__cyip = f'len(arr_{fgg__fawh[0]})'
    qbz__gfe = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in qbz__gfe:
        bypa__zyt = qbz__gfe[func_name]
        nmk__pkc = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        tvi__nva = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {tqww__cyip}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{nmk__pkc})
    for i in numba.parfors.parfor.internal_prange(n):
        {twqb__pivs}
        A[i] = {bypa__zyt}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return tvi__nva
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    zdf__eghnt = dict(fill_method=fill_method, limit=limit, freq=freq)
    lovy__xcvh = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', zdf__eghnt, lovy__xcvh,
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
    zdf__eghnt = dict(axis=axis, skipna=skipna)
    lovy__xcvh = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', zdf__eghnt, lovy__xcvh,
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
    zdf__eghnt = dict(skipna=skipna)
    lovy__xcvh = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', zdf__eghnt, lovy__xcvh,
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
    zdf__eghnt = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    lovy__xcvh = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    fvj__nvqg = [pnkk__ivfi for pnkk__ivfi, mttr__tjst in zip(df.columns,
        df.data) if _is_describe_type(mttr__tjst)]
    if len(fvj__nvqg) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    ntr__xorh = sum(df.data[df.column_index[pnkk__ivfi]].dtype == bodo.
        datetime64ns for pnkk__ivfi in fvj__nvqg)

    def _get_describe(col_ind):
        rscf__jwfzm = df.data[col_ind].dtype == bodo.datetime64ns
        if ntr__xorh and ntr__xorh != len(fvj__nvqg):
            if rscf__jwfzm:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for pnkk__ivfi in fvj__nvqg:
        col_ind = df.column_index[pnkk__ivfi]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[pnkk__ivfi]) for
        pnkk__ivfi in fvj__nvqg)
    hgjef__wfcoi = (
        "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']")
    if ntr__xorh == len(fvj__nvqg):
        hgjef__wfcoi = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif ntr__xorh:
        hgjef__wfcoi = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({hgjef__wfcoi})'
    return _gen_init_df(header, fvj__nvqg, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    zdf__eghnt = dict(axis=axis, convert=convert, is_copy=is_copy)
    lovy__xcvh = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', zdf__eghnt, lovy__xcvh,
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
    zdf__eghnt = dict(freq=freq, axis=axis, fill_value=fill_value)
    lovy__xcvh = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for cwd__cbpc in df.data:
        if not is_supported_shift_array_type(cwd__cbpc):
            raise BodoError(
                f'Dataframe.shift() column input type {cwd__cbpc.dtype} not supported yet.'
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
    zdf__eghnt = dict(axis=axis)
    lovy__xcvh = dict(axis=0)
    check_unsupported_args('DataFrame.diff', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for cwd__cbpc in df.data:
        if not (isinstance(cwd__cbpc, types.Array) and (isinstance(
            cwd__cbpc.dtype, types.Number) or cwd__cbpc.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {cwd__cbpc.dtype} not supported.'
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
    meonf__ygajc = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(meonf__ygajc)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        fxkux__ujri = get_overload_const_list(column)
    else:
        fxkux__ujri = [get_literal_value(column)]
    spf__fptkz = [df.column_index[pnkk__ivfi] for pnkk__ivfi in fxkux__ujri]
    for i in spf__fptkz:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{spf__fptkz[0]})\n'
        )
    for i in range(n):
        if i in spf__fptkz:
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
    bvhxd__dzin = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    kiamp__jjcud = {'inplace': False, 'append': False, 'verify_integrity': 
        False}
    check_unsupported_args('DataFrame.set_index', bvhxd__dzin, kiamp__jjcud,
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
    columns = tuple(pnkk__ivfi for pnkk__ivfi in df.columns if pnkk__ivfi !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    bvhxd__dzin = {'inplace': inplace}
    kiamp__jjcud = {'inplace': False}
    check_unsupported_args('query', bvhxd__dzin, kiamp__jjcud, package_name
        ='pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        hbokh__gfnct = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[hbokh__gfnct]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    bvhxd__dzin = {'subset': subset, 'keep': keep}
    kiamp__jjcud = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', bvhxd__dzin,
        kiamp__jjcud, package_name='pandas', module_name='DataFrame')
    jngnb__yxdo = len(df.columns)
    tvi__nva = "def impl(df, subset=None, keep='first'):\n"
    for i in range(jngnb__yxdo):
        tvi__nva += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    saaq__eju = ', '.join(f'data_{i}' for i in range(jngnb__yxdo))
    saaq__eju += ',' if jngnb__yxdo == 1 else ''
    tvi__nva += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({saaq__eju}))\n')
    tvi__nva += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    tvi__nva += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo}, cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    bvhxd__dzin = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    kiamp__jjcud = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    dkk__oqiv = []
    if is_overload_constant_list(subset):
        dkk__oqiv = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        dkk__oqiv = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        dkk__oqiv = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    owy__wchx = []
    for col_name in dkk__oqiv:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        owy__wchx.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', bvhxd__dzin,
        kiamp__jjcud, package_name='pandas', module_name='DataFrame')
    ukrl__rla = []
    if owy__wchx:
        for butnq__htthu in owy__wchx:
            if isinstance(df.data[butnq__htthu], bodo.MapArrayType):
                ukrl__rla.append(df.columns[butnq__htthu])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                ukrl__rla.append(col_name)
    if ukrl__rla:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {ukrl__rla} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    jngnb__yxdo = len(df.columns)
    boog__fjxy = ['data_{}'.format(i) for i in owy__wchx]
    ypbu__yng = ['data_{}'.format(i) for i in range(jngnb__yxdo) if i not in
        owy__wchx]
    if boog__fjxy:
        qdtjr__mxyta = len(boog__fjxy)
    else:
        qdtjr__mxyta = jngnb__yxdo
    krbr__hzz = ', '.join(boog__fjxy + ypbu__yng)
    data_args = ', '.join('data_{}'.format(i) for i in range(jngnb__yxdo))
    tvi__nva = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(jngnb__yxdo):
        tvi__nva += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    tvi__nva += (
        '  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})\n'
        .format(krbr__hzz, index, qdtjr__mxyta))
    tvi__nva += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return _gen_init_df(tvi__nva, df.columns, data_args, 'index')


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
            hbw__oel = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                hbw__oel = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                hbw__oel = lambda i: f'other[:,{i}]'
        jngnb__yxdo = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {hbw__oel(i)})'
             for i in range(jngnb__yxdo))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        fayak__rug = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(fayak__rug
            )


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    zdf__eghnt = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    lovy__xcvh = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', zdf__eghnt, lovy__xcvh,
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
    jngnb__yxdo = len(df.columns)
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
        for i in range(jngnb__yxdo):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other.column_index[df
                    .columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(jngnb__yxdo):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(jngnb__yxdo):
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
        getjx__aree = 'out_df_type'
    else:
        getjx__aree = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    tvi__nva = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {getjx__aree})
"""
    cwa__nvjj = {}
    ypm__mzlfp = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    ypm__mzlfp.update(extra_globals)
    exec(tvi__nva, ypm__mzlfp, cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        rtmxr__rmld = pd.Index(lhs.columns)
        zlcrf__rcsi = pd.Index(rhs.columns)
        joo__vmxt, zejp__hiopm, imh__muv = rtmxr__rmld.join(zlcrf__rcsi,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(joo__vmxt), zejp__hiopm, imh__muv
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        ssr__mhgo = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        albfe__htbdi = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, ssr__mhgo)
        check_runtime_cols_unsupported(rhs, ssr__mhgo)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                joo__vmxt, zejp__hiopm, imh__muv = _get_binop_columns(lhs, rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {egzq__tldfp}) {ssr__mhgo}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {fwxwy__kog})'
                     if egzq__tldfp != -1 and fwxwy__kog != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for egzq__tldfp, fwxwy__kog in zip(zejp__hiopm, imh__muv))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, joo__vmxt, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            vtxi__uge = []
            mnz__vfz = []
            if op in albfe__htbdi:
                for i, wzrmt__cvopi in enumerate(lhs.data):
                    if is_common_scalar_dtype([wzrmt__cvopi.dtype, rhs]):
                        vtxi__uge.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {ssr__mhgo} rhs'
                            )
                    else:
                        rtcmo__jea = f'arr{i}'
                        mnz__vfz.append(rtcmo__jea)
                        vtxi__uge.append(rtcmo__jea)
                data_args = ', '.join(vtxi__uge)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {ssr__mhgo} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(mnz__vfz) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {rtcmo__jea} = np.empty(n, dtype=np.bool_)\n' for
                    rtcmo__jea in mnz__vfz)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(rtcmo__jea, 
                    op == operator.ne) for rtcmo__jea in mnz__vfz)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            vtxi__uge = []
            mnz__vfz = []
            if op in albfe__htbdi:
                for i, wzrmt__cvopi in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, wzrmt__cvopi.dtype]):
                        vtxi__uge.append(
                            f'lhs {ssr__mhgo} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        rtcmo__jea = f'arr{i}'
                        mnz__vfz.append(rtcmo__jea)
                        vtxi__uge.append(rtcmo__jea)
                data_args = ', '.join(vtxi__uge)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, ssr__mhgo) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(mnz__vfz) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(rtcmo__jea) for rtcmo__jea in mnz__vfz)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(rtcmo__jea, 
                    op == operator.ne) for rtcmo__jea in mnz__vfz)
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
        fayak__rug = create_binary_op_overload(op)
        overload(op)(fayak__rug)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        ssr__mhgo = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, ssr__mhgo)
        check_runtime_cols_unsupported(right, ssr__mhgo)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                joo__vmxt, _, imh__muv = _get_binop_columns(left, right, True)
                tvi__nva = 'def impl(left, right):\n'
                for i, fwxwy__kog in enumerate(imh__muv):
                    if fwxwy__kog == -1:
                        tvi__nva += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    tvi__nva += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    tvi__nva += f"""  df_arr{i} {ssr__mhgo} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {fwxwy__kog})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    joo__vmxt)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(tvi__nva, joo__vmxt, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            tvi__nva = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                tvi__nva += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                tvi__nva += '  df_arr{0} {1} right\n'.format(i, ssr__mhgo)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(tvi__nva, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        fayak__rug = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(fayak__rug)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            ssr__mhgo = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, ssr__mhgo)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, ssr__mhgo) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        fayak__rug = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(fayak__rug)


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
            dlfzu__nfbh = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                dlfzu__nfbh[i] = bodo.libs.array_kernels.isna(obj, i)
            return dlfzu__nfbh
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
            dlfzu__nfbh = np.empty(n, np.bool_)
            for i in range(n):
                dlfzu__nfbh[i] = pd.isna(obj[i])
            return dlfzu__nfbh
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
    bvhxd__dzin = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    kiamp__jjcud = {'inplace': False, 'limit': None, 'regex': False,
        'method': 'pad'}
    check_unsupported_args('replace', bvhxd__dzin, kiamp__jjcud,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    xac__ugo = str(expr_node)
    return xac__ugo.startswith('left.') or xac__ugo.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    uthx__dob = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (uthx__dob,))
    iqnry__iobng = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        bcwpp__xboq = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        jlpnc__vyyrj = {('NOT_NA', iqnry__iobng(wzrmt__cvopi)):
            wzrmt__cvopi for wzrmt__cvopi in null_set}
        bjekw__lfyq, _, _ = _parse_query_expr(bcwpp__xboq, env, [], [],
            None, join_cleaned_cols=jlpnc__vyyrj)
        auibe__rjrn = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            qads__sqsn = pd.core.computation.ops.BinOp('&', bjekw__lfyq,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = auibe__rjrn
        return qads__sqsn

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                eyjqh__iwfd = set()
                dpmk__yksfs = set()
                aix__wrd = _insert_NA_cond_body(expr_node.lhs, eyjqh__iwfd)
                adfis__micno = _insert_NA_cond_body(expr_node.rhs, dpmk__yksfs)
                fmml__tzpsf = eyjqh__iwfd.intersection(dpmk__yksfs)
                eyjqh__iwfd.difference_update(fmml__tzpsf)
                dpmk__yksfs.difference_update(fmml__tzpsf)
                null_set.update(fmml__tzpsf)
                expr_node.lhs = append_null_checks(aix__wrd, eyjqh__iwfd)
                expr_node.rhs = append_null_checks(adfis__micno, dpmk__yksfs)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            jsnn__zqlbs = expr_node.name
            yxf__gkab, col_name = jsnn__zqlbs.split('.')
            if yxf__gkab == 'left':
                uafn__pqwg = left_columns
                data = left_data
            else:
                uafn__pqwg = right_columns
                data = right_data
            gabj__kiuqa = data[uafn__pqwg.index(col_name)]
            if bodo.utils.typing.is_nullable(gabj__kiuqa):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    emfo__xvz = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        miwq__hirs = str(expr_node.lhs)
        yhn__dhxi = str(expr_node.rhs)
        if miwq__hirs.startswith('left.') and yhn__dhxi.startswith('left.'
            ) or miwq__hirs.startswith('right.') and yhn__dhxi.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [miwq__hirs.split('.')[1]]
        right_on = [yhn__dhxi.split('.')[1]]
        if miwq__hirs.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        hxbu__hhr, skqn__qkkp, vynuq__wvq = _extract_equal_conds(expr_node.lhs)
        fcuaa__bhefq, afqku__pow, bll__vvdgj = _extract_equal_conds(expr_node
            .rhs)
        left_on = hxbu__hhr + fcuaa__bhefq
        right_on = skqn__qkkp + afqku__pow
        if vynuq__wvq is None:
            return left_on, right_on, bll__vvdgj
        if bll__vvdgj is None:
            return left_on, right_on, vynuq__wvq
        expr_node.lhs = vynuq__wvq
        expr_node.rhs = bll__vvdgj
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    uthx__dob = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (uthx__dob,))
    aaym__osjl = dict()
    iqnry__iobng = pd.core.computation.parsing.clean_column_name
    for name, uzfor__pwzui in (('left', left_columns), ('right', right_columns)
        ):
        for wzrmt__cvopi in uzfor__pwzui:
            rxri__kyu = iqnry__iobng(wzrmt__cvopi)
            wzwji__ddp = name, rxri__kyu
            if wzwji__ddp in aaym__osjl:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{wzrmt__cvopi}' and '{aaym__osjl[rxri__kyu]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            aaym__osjl[wzwji__ddp] = wzrmt__cvopi
    hkd__ewpmo, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=aaym__osjl)
    left_on, right_on, vicju__ohbgs = _extract_equal_conds(hkd__ewpmo.terms)
    return left_on, right_on, _insert_NA_cond(vicju__ohbgs, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    zdf__eghnt = dict(sort=sort, copy=copy, validate=validate)
    lovy__xcvh = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    iawky__hanni = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    mfsa__eafdh = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in iawky__hanni and ('left.' in on_str or 
                'right.' in on_str):
                left_on, right_on, vdvl__gvxk = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if vdvl__gvxk is None:
                    mfsa__eafdh = ''
                else:
                    mfsa__eafdh = str(vdvl__gvxk)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = iawky__hanni
        right_keys = iawky__hanni
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
    fjx__vxcyy = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        mijxp__xfi = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        mijxp__xfi = list(get_overload_const_list(suffixes))
    suffix_x = mijxp__xfi[0]
    suffix_y = mijxp__xfi[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    tvi__nva = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    tvi__nva += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    tvi__nva += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    tvi__nva += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, fjx__vxcyy, mfsa__eafdh))
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo}, cwa__nvjj)
    _impl = cwa__nvjj['_impl']
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
    xwk__wfspg = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    too__zmjv = {get_overload_const_str(hthpl__cxvl) for hthpl__cxvl in (
        left_on, right_on, on) if is_overload_constant_str(hthpl__cxvl)}
    for df in (left, right):
        for i, wzrmt__cvopi in enumerate(df.data):
            if not isinstance(wzrmt__cvopi, valid_dataframe_column_types
                ) and wzrmt__cvopi not in xwk__wfspg:
                raise BodoError(
                    f'{name_func}(): use of column with {type(wzrmt__cvopi)} in merge unsupported'
                    )
            if df.columns[i] in too__zmjv and isinstance(wzrmt__cvopi,
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
        mijxp__xfi = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        mijxp__xfi = list(get_overload_const_list(suffixes))
    if len(mijxp__xfi) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    iawky__hanni = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        crs__gbcjd = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            crs__gbcjd = on_str not in iawky__hanni and ('left.' in on_str or
                'right.' in on_str)
        if len(iawky__hanni) == 0 and not crs__gbcjd:
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
    nrq__npa = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            idc__tyjt = left.index
            tfp__tvia = isinstance(idc__tyjt, StringIndexType)
            zew__wpta = right.index
            yasi__ami = isinstance(zew__wpta, StringIndexType)
        elif is_overload_true(left_index):
            idc__tyjt = left.index
            tfp__tvia = isinstance(idc__tyjt, StringIndexType)
            zew__wpta = right.data[right.columns.index(right_keys[0])]
            yasi__ami = zew__wpta.dtype == string_type
        elif is_overload_true(right_index):
            idc__tyjt = left.data[left.columns.index(left_keys[0])]
            tfp__tvia = idc__tyjt.dtype == string_type
            zew__wpta = right.index
            yasi__ami = isinstance(zew__wpta, StringIndexType)
        if tfp__tvia and yasi__ami:
            return
        idc__tyjt = idc__tyjt.dtype
        zew__wpta = zew__wpta.dtype
        try:
            xqwnr__fsjj = nrq__npa.resolve_function_type(operator.eq, (
                idc__tyjt, zew__wpta), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=idc__tyjt, rk_dtype=zew__wpta))
    else:
        for qai__wczua, eacp__cuo in zip(left_keys, right_keys):
            idc__tyjt = left.data[left.columns.index(qai__wczua)].dtype
            jfjxh__fhtx = left.data[left.columns.index(qai__wczua)]
            zew__wpta = right.data[right.columns.index(eacp__cuo)].dtype
            aev__mpk = right.data[right.columns.index(eacp__cuo)]
            if jfjxh__fhtx == aev__mpk:
                continue
            wzj__gkupa = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=qai__wczua, lk_dtype=idc__tyjt, rk=eacp__cuo,
                rk_dtype=zew__wpta))
            nwd__dwkoy = idc__tyjt == string_type
            chl__pqrhy = zew__wpta == string_type
            if nwd__dwkoy ^ chl__pqrhy:
                raise_bodo_error(wzj__gkupa)
            try:
                xqwnr__fsjj = nrq__npa.resolve_function_type(operator.eq, (
                    idc__tyjt, zew__wpta), {})
            except:
                raise_bodo_error(wzj__gkupa)


def validate_keys(keys, df):
    rygh__xzrlo = set(keys).difference(set(df.columns))
    if len(rygh__xzrlo) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in rygh__xzrlo:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {rygh__xzrlo} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    zdf__eghnt = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    lovy__xcvh = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', zdf__eghnt, lovy__xcvh,
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
    tvi__nva = "def _impl(left, other, on=None, how='left',\n"
    tvi__nva += "    lsuffix='', rsuffix='', sort=False):\n"
    tvi__nva += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo}, cwa__nvjj)
    _impl = cwa__nvjj['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        gystg__atoxh = get_overload_const_list(on)
        validate_keys(gystg__atoxh, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    iawky__hanni = tuple(set(left.columns) & set(other.columns))
    if len(iawky__hanni) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=iawky__hanni))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    ekmf__mbho = set(left_keys) & set(right_keys)
    lbbw__ble = set(left_columns) & set(right_columns)
    swfi__kpn = lbbw__ble - ekmf__mbho
    pwng__kaagb = set(left_columns) - lbbw__ble
    knzj__cwjo = set(right_columns) - lbbw__ble
    pfpj__cjcf = {}

    def insertOutColumn(col_name):
        if col_name in pfpj__cjcf:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        pfpj__cjcf[col_name] = 0
    for gbqb__cng in ekmf__mbho:
        insertOutColumn(gbqb__cng)
    for gbqb__cng in swfi__kpn:
        atb__bojqz = str(gbqb__cng) + suffix_x
        pabl__wqs = str(gbqb__cng) + suffix_y
        insertOutColumn(atb__bojqz)
        insertOutColumn(pabl__wqs)
    for gbqb__cng in pwng__kaagb:
        insertOutColumn(gbqb__cng)
    for gbqb__cng in knzj__cwjo:
        insertOutColumn(gbqb__cng)
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
    iawky__hanni = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = iawky__hanni
        right_keys = iawky__hanni
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
        mijxp__xfi = suffixes
    if is_overload_constant_list(suffixes):
        mijxp__xfi = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        mijxp__xfi = suffixes.value
    suffix_x = mijxp__xfi[0]
    suffix_y = mijxp__xfi[1]
    tvi__nva = 'def _impl(left, right, on=None, left_on=None, right_on=None,\n'
    tvi__nva += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    tvi__nva += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    tvi__nva += "    allow_exact_matches=True, direction='backward'):\n"
    tvi__nva += '  suffix_x = suffixes[0]\n'
    tvi__nva += '  suffix_y = suffixes[1]\n'
    tvi__nva += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo}, cwa__nvjj)
    _impl = cwa__nvjj['_impl']
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
    zdf__eghnt = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    sbxa__saae = dict(sort=False, group_keys=True, squeeze=False, observed=True
        )
    check_unsupported_args('Dataframe.groupby', zdf__eghnt, sbxa__saae,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    qqohs__wrz = func_name == 'DataFrame.pivot_table'
    if qqohs__wrz:
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
    xlhxp__thp = get_literal_value(columns)
    if isinstance(xlhxp__thp, (list, tuple)):
        if len(xlhxp__thp) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {xlhxp__thp}"
                )
        xlhxp__thp = xlhxp__thp[0]
    if xlhxp__thp not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {xlhxp__thp} not found in DataFrame {df}."
            )
    irp__uphfr = df.column_index[xlhxp__thp]
    if is_overload_none(index):
        pcpt__rvi = []
        ufrq__kpcfe = []
    else:
        ufrq__kpcfe = get_literal_value(index)
        if not isinstance(ufrq__kpcfe, (list, tuple)):
            ufrq__kpcfe = [ufrq__kpcfe]
        pcpt__rvi = []
        for index in ufrq__kpcfe:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            pcpt__rvi.append(df.column_index[index])
    if not (all(isinstance(pnkk__ivfi, int) for pnkk__ivfi in ufrq__kpcfe) or
        all(isinstance(pnkk__ivfi, str) for pnkk__ivfi in ufrq__kpcfe)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        zvv__nnbf = []
        xtdhl__mrp = []
        eaqg__gerf = pcpt__rvi + [irp__uphfr]
        for i, pnkk__ivfi in enumerate(df.columns):
            if i not in eaqg__gerf:
                zvv__nnbf.append(i)
                xtdhl__mrp.append(pnkk__ivfi)
    else:
        xtdhl__mrp = get_literal_value(values)
        if not isinstance(xtdhl__mrp, (list, tuple)):
            xtdhl__mrp = [xtdhl__mrp]
        zvv__nnbf = []
        for val in xtdhl__mrp:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            zvv__nnbf.append(df.column_index[val])
    if all(isinstance(pnkk__ivfi, int) for pnkk__ivfi in xtdhl__mrp):
        xtdhl__mrp = np.array(xtdhl__mrp, 'int64')
    elif all(isinstance(pnkk__ivfi, str) for pnkk__ivfi in xtdhl__mrp):
        xtdhl__mrp = pd.array(xtdhl__mrp, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    yotd__uyjsn = set(zvv__nnbf) | set(pcpt__rvi) | {irp__uphfr}
    if len(yotd__uyjsn) != len(zvv__nnbf) + len(pcpt__rvi) + 1:
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
    if len(pcpt__rvi) == 0:
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
        for eij__lmn in pcpt__rvi:
            index_column = df.data[eij__lmn]
            check_valid_index_typ(index_column)
    awi__xbmpv = df.data[irp__uphfr]
    if isinstance(awi__xbmpv, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(awi__xbmpv, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for ghq__rai in zvv__nnbf:
        eizv__lyij = df.data[ghq__rai]
        if isinstance(eizv__lyij, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or eizv__lyij == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (ufrq__kpcfe, xlhxp__thp, xtdhl__mrp, pcpt__rvi, irp__uphfr,
        zvv__nnbf)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (ufrq__kpcfe, xlhxp__thp, xtdhl__mrp, eij__lmn, irp__uphfr, aany__lxypn
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(ufrq__kpcfe) == 0:
        if is_overload_none(data.index.name_typ):
            ufrq__kpcfe = [None]
        else:
            ufrq__kpcfe = [get_literal_value(data.index.name_typ)]
    if len(xtdhl__mrp) == 1:
        ezgj__cvfmy = None
    else:
        ezgj__cvfmy = xtdhl__mrp
    tvi__nva = 'def impl(data, index=None, columns=None, values=None):\n'
    tvi__nva += f'    pivot_values = data.iloc[:, {irp__uphfr}].unique()\n'
    tvi__nva += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(eij__lmn) == 0:
        tvi__nva += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        tvi__nva += '        (\n'
        for dfnyd__mxr in eij__lmn:
            tvi__nva += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {dfnyd__mxr}),
"""
        tvi__nva += '        ),\n'
    tvi__nva += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {irp__uphfr}),),
"""
    tvi__nva += '        (\n'
    for ghq__rai in aany__lxypn:
        tvi__nva += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {ghq__rai}),
"""
    tvi__nva += '        ),\n'
    tvi__nva += '        pivot_values,\n'
    tvi__nva += '        index_lit_tup,\n'
    tvi__nva += '        columns_lit,\n'
    tvi__nva += '        values_name_const,\n'
    tvi__nva += '    )\n'
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'index_lit_tup': tuple(ufrq__kpcfe),
        'columns_lit': xlhxp__thp, 'values_name_const': ezgj__cvfmy}, cwa__nvjj
        )
    impl = cwa__nvjj['impl']
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
    zdf__eghnt = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    lovy__xcvh = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (ufrq__kpcfe, xlhxp__thp, xtdhl__mrp, eij__lmn, irp__uphfr, aany__lxypn
            ) = (pivot_error_checking(data, index, columns, values,
            'DataFrame.pivot_table'))
        if len(xtdhl__mrp) == 1:
            ezgj__cvfmy = None
        else:
            ezgj__cvfmy = xtdhl__mrp
        tvi__nva = 'def impl(\n'
        tvi__nva += '    data,\n'
        tvi__nva += '    values=None,\n'
        tvi__nva += '    index=None,\n'
        tvi__nva += '    columns=None,\n'
        tvi__nva += '    aggfunc="mean",\n'
        tvi__nva += '    fill_value=None,\n'
        tvi__nva += '    margins=False,\n'
        tvi__nva += '    dropna=True,\n'
        tvi__nva += '    margins_name="All",\n'
        tvi__nva += '    observed=False,\n'
        tvi__nva += '    sort=True,\n'
        tvi__nva += '    _pivot_values=None,\n'
        tvi__nva += '):\n'
        srhjf__egj = eij__lmn + [irp__uphfr] + aany__lxypn
        tvi__nva += f'    data = data.iloc[:, {srhjf__egj}]\n'
        qfrp__jhzuw = ufrq__kpcfe + [xlhxp__thp]
        tvi__nva += (
            f'    data = data.groupby({qfrp__jhzuw!r}, as_index=False).agg(aggfunc)\n'
            )
        tvi__nva += (
            f'    pivot_values = data.iloc[:, {len(eij__lmn)}].unique()\n')
        tvi__nva += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
        tvi__nva += '        (\n'
        for i in range(0, len(eij__lmn)):
            tvi__nva += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        tvi__nva += '        ),\n'
        tvi__nva += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(eij__lmn)}),),
"""
        tvi__nva += '        (\n'
        for i in range(len(eij__lmn) + 1, len(aany__lxypn) + len(eij__lmn) + 1
            ):
            tvi__nva += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        tvi__nva += '        ),\n'
        tvi__nva += '        pivot_values,\n'
        tvi__nva += '        index_lit_tup,\n'
        tvi__nva += '        columns_lit,\n'
        tvi__nva += '        values_name_const,\n'
        tvi__nva += '        check_duplicates=False,\n'
        tvi__nva += '    )\n'
        cwa__nvjj = {}
        exec(tvi__nva, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(ufrq__kpcfe), 'columns_lit': xlhxp__thp,
            'values_name_const': ezgj__cvfmy}, cwa__nvjj)
        impl = cwa__nvjj['impl']
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
    zdf__eghnt = dict(col_level=col_level, ignore_index=ignore_index)
    lovy__xcvh = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', zdf__eghnt, lovy__xcvh,
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
    gbuj__hmqx = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(gbuj__hmqx, (list, tuple)):
        gbuj__hmqx = [gbuj__hmqx]
    for pnkk__ivfi in gbuj__hmqx:
        if pnkk__ivfi not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {pnkk__ivfi} not found in {frame}."
                )
    asx__pku = [frame.column_index[i] for i in gbuj__hmqx]
    if is_overload_none(value_vars):
        unl__apmk = []
        dbrf__dwvk = []
        for i, pnkk__ivfi in enumerate(frame.columns):
            if i not in asx__pku:
                unl__apmk.append(i)
                dbrf__dwvk.append(pnkk__ivfi)
    else:
        dbrf__dwvk = get_literal_value(value_vars)
        if not isinstance(dbrf__dwvk, (list, tuple)):
            dbrf__dwvk = [dbrf__dwvk]
        dbrf__dwvk = [v for v in dbrf__dwvk if v not in gbuj__hmqx]
        if not dbrf__dwvk:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        unl__apmk = []
        for val in dbrf__dwvk:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            unl__apmk.append(frame.column_index[val])
    for pnkk__ivfi in dbrf__dwvk:
        if pnkk__ivfi not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {pnkk__ivfi} not found in {frame}."
                )
    if not (all(isinstance(pnkk__ivfi, int) for pnkk__ivfi in dbrf__dwvk) or
        all(isinstance(pnkk__ivfi, str) for pnkk__ivfi in dbrf__dwvk)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    gtmuz__pgfrn = frame.data[unl__apmk[0]]
    lkgux__zsgav = [frame.data[i].dtype for i in unl__apmk]
    unl__apmk = np.array(unl__apmk, dtype=np.int64)
    asx__pku = np.array(asx__pku, dtype=np.int64)
    _, xsrar__gnv = bodo.utils.typing.get_common_scalar_dtype(lkgux__zsgav)
    if not xsrar__gnv:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': dbrf__dwvk, 'val_type':
        gtmuz__pgfrn}
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
    if frame.is_table_format and all(v == gtmuz__pgfrn.dtype for v in
        lkgux__zsgav):
        extra_globals['value_idxs'] = unl__apmk
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(dbrf__dwvk) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {unl__apmk[0]})
"""
    else:
        azxq__wfazh = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in unl__apmk)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({azxq__wfazh},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in asx__pku:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(dbrf__dwvk)})\n'
            )
    wcqbz__vuyrq = ', '.join(f'out_id{i}' for i in asx__pku) + (', ' if len
        (asx__pku) > 0 else '')
    data_args = wcqbz__vuyrq + 'var_col, val_col'
    columns = tuple(gbuj__hmqx + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(dbrf__dwvk)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    zdf__eghnt = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    lovy__xcvh = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', zdf__eghnt, lovy__xcvh,
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
    zdf__eghnt = dict(ignore_index=ignore_index, key=key)
    lovy__xcvh = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', zdf__eghnt, lovy__xcvh,
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
    sddrt__hykml = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        sddrt__hykml.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        ocs__fwobv = [get_overload_const_tuple(by)]
    else:
        ocs__fwobv = get_overload_const_list(by)
    ocs__fwobv = set((k, '') if (k, '') in sddrt__hykml else k for k in
        ocs__fwobv)
    if len(ocs__fwobv.difference(sddrt__hykml)) > 0:
        wpjjo__kamf = list(set(get_overload_const_list(by)).difference(
            sddrt__hykml))
        raise_bodo_error(f'sort_values(): invalid keys {wpjjo__kamf} for by.')
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
        kpksh__ymr = get_overload_const_list(na_position)
        for na_position in kpksh__ymr:
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
    zdf__eghnt = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    lovy__xcvh = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', zdf__eghnt, lovy__xcvh,
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
    zdf__eghnt = dict(limit=limit, downcast=downcast)
    lovy__xcvh = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', zdf__eghnt, lovy__xcvh,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    srvv__cwazr = not is_overload_none(value)
    srhwn__boug = not is_overload_none(method)
    if srvv__cwazr and srhwn__boug:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not srvv__cwazr and not srhwn__boug:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if srvv__cwazr:
        wssku__izmeh = 'value=value'
    else:
        wssku__izmeh = 'method=method'
    data_args = [(
        f"df['{pnkk__ivfi}'].fillna({wssku__izmeh}, inplace=inplace)" if
        isinstance(pnkk__ivfi, str) else
        f'df[{pnkk__ivfi}].fillna({wssku__izmeh}, inplace=inplace)') for
        pnkk__ivfi in df.columns]
    tvi__nva = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        tvi__nva += '  ' + '  \n'.join(data_args) + '\n'
        cwa__nvjj = {}
        exec(tvi__nva, {}, cwa__nvjj)
        impl = cwa__nvjj['impl']
        return impl
    else:
        return _gen_init_df(tvi__nva, df.columns, ', '.join(mttr__tjst +
            '.values' for mttr__tjst in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    zdf__eghnt = dict(col_level=col_level, col_fill=col_fill)
    lovy__xcvh = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', zdf__eghnt, lovy__xcvh,
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
    tvi__nva = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    tvi__nva += (
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
        tysn__zpidy = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            tysn__zpidy)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            tvi__nva += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            wumok__tint = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = wumok__tint + data_args
        else:
            iax__vnn = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [iax__vnn] + data_args
    return _gen_init_df(tvi__nva, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    pltof__aptn = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and pltof__aptn == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(pltof__aptn))


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
        ypdf__akcgb = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        ursbj__heuiw = get_overload_const_list(subset)
        ypdf__akcgb = []
        for bqk__kcp in ursbj__heuiw:
            if bqk__kcp not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{bqk__kcp}' not in data frame columns {df}"
                    )
            ypdf__akcgb.append(df.column_index[bqk__kcp])
    jngnb__yxdo = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(jngnb__yxdo))
    tvi__nva = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(jngnb__yxdo):
        tvi__nva += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    tvi__nva += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in ypdf__akcgb)))
    tvi__nva += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return _gen_init_df(tvi__nva, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    zdf__eghnt = dict(index=index, level=level, errors=errors)
    lovy__xcvh = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', zdf__eghnt, lovy__xcvh,
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
            fdork__rajoi = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            fdork__rajoi = get_overload_const_list(labels)
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
            fdork__rajoi = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            fdork__rajoi = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for pnkk__ivfi in fdork__rajoi:
        if pnkk__ivfi not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(pnkk__ivfi, df.columns))
    if len(set(fdork__rajoi)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    vlmsq__igwo = tuple(pnkk__ivfi for pnkk__ivfi in df.columns if 
        pnkk__ivfi not in fdork__rajoi)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[pnkk__ivfi], '.copy()' if not inplace else
        '') for pnkk__ivfi in vlmsq__igwo)
    tvi__nva = 'def impl(df, labels=None, axis=0, index=None, columns=None,\n'
    tvi__nva += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(tvi__nva, vlmsq__igwo, data_args, index)


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
    zdf__eghnt = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    holf__cpnms = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', zdf__eghnt, holf__cpnms,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    jngnb__yxdo = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(jngnb__yxdo))
    hvmp__jmn = ', '.join('rhs_data_{}'.format(i) for i in range(jngnb__yxdo))
    tvi__nva = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    tvi__nva += '  if (frac == 1 or n == len(df)) and not replace:\n'
    tvi__nva += '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n'
    for i in range(jngnb__yxdo):
        tvi__nva += (
            '  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    tvi__nva += '  if frac is None:\n'
    tvi__nva += '    frac_d = -1.0\n'
    tvi__nva += '  else:\n'
    tvi__nva += '    frac_d = frac\n'
    tvi__nva += '  if n is None:\n'
    tvi__nva += '    n_i = 0\n'
    tvi__nva += '  else:\n'
    tvi__nva += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    tvi__nva += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({hvmp__jmn},), {index}, n_i, frac_d, replace)
"""
    tvi__nva += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(tvi__nva, df.columns,
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
    bvhxd__dzin = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    kiamp__jjcud = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', bvhxd__dzin, kiamp__jjcud,
        package_name='pandas', module_name='DataFrame')
    qjfyq__quu = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            vacw__yimj = qjfyq__quu + '\n'
            vacw__yimj += 'Index: 0 entries\n'
            vacw__yimj += 'Empty DataFrame'
            print(vacw__yimj)
        return _info_impl
    else:
        tvi__nva = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        tvi__nva += '    ncols = df.shape[1]\n'
        tvi__nva += f'    lines = "{qjfyq__quu}\\n"\n'
        tvi__nva += f'    lines += "{df.index}: "\n'
        tvi__nva += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            tvi__nva += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            tvi__nva += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            tvi__nva += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        tvi__nva += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        tvi__nva += f'    space = {max(len(str(k)) for k in df.columns) + 1}\n'
        tvi__nva += '    column_width = max(space, 7)\n'
        tvi__nva += '    column= "Column"\n'
        tvi__nva += '    underl= "------"\n'
        tvi__nva += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        tvi__nva += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        tvi__nva += '    mem_size = 0\n'
        tvi__nva += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        tvi__nva += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        tvi__nva += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        cxo__picd = dict()
        for i in range(len(df.columns)):
            tvi__nva += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            qfi__jbh = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                qfi__jbh = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                rfb__kxfcl = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                qfi__jbh = f'{rfb__kxfcl[:-7]}'
            tvi__nva += f'    col_dtype[{i}] = "{qfi__jbh}"\n'
            if qfi__jbh in cxo__picd:
                cxo__picd[qfi__jbh] += 1
            else:
                cxo__picd[qfi__jbh] = 1
            tvi__nva += f'    col_name[{i}] = "{df.columns[i]}"\n'
            tvi__nva += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        tvi__nva += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        tvi__nva += '    for i in column_info:\n'
        tvi__nva += "        lines += f'{i}\\n'\n"
        yvxs__yte = ', '.join(f'{k}({cxo__picd[k]})' for k in sorted(cxo__picd)
            )
        tvi__nva += f"    lines += 'dtypes: {yvxs__yte}\\n'\n"
        tvi__nva += '    mem_size += df.index.nbytes\n'
        tvi__nva += '    total_size = _sizeof_fmt(mem_size)\n'
        tvi__nva += "    lines += f'memory usage: {total_size}'\n"
        tvi__nva += '    print(lines)\n'
        cwa__nvjj = {}
        exec(tvi__nva, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo': bodo,
            'np': np}, cwa__nvjj)
        _info_impl = cwa__nvjj['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    tvi__nva = 'def impl(df, index=True, deep=False):\n'
    zee__tytj = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes'
    zqjej__gqo = is_overload_true(index)
    columns = df.columns
    if zqjej__gqo:
        columns = ('Index',) + columns
    if len(columns) == 0:
        etglo__czajs = ()
    elif all(isinstance(pnkk__ivfi, int) for pnkk__ivfi in columns):
        etglo__czajs = np.array(columns, 'int64')
    elif all(isinstance(pnkk__ivfi, str) for pnkk__ivfi in columns):
        etglo__czajs = pd.array(columns, 'string')
    else:
        etglo__czajs = columns
    if df.is_table_format:
        wyr__yxp = int(zqjej__gqo)
        sacfv__hsmq = len(columns)
        tvi__nva += f'  nbytes_arr = np.empty({sacfv__hsmq}, np.int64)\n'
        tvi__nva += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        tvi__nva += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {wyr__yxp})
"""
        if zqjej__gqo:
            tvi__nva += f'  nbytes_arr[0] = {zee__tytj}\n'
        tvi__nva += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if zqjej__gqo:
            data = f'{zee__tytj},{data}'
        else:
            eyqtl__uiujm = ',' if len(columns) == 1 else ''
            data = f'{data}{eyqtl__uiujm}'
        tvi__nva += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        etglo__czajs}, cwa__nvjj)
    impl = cwa__nvjj['impl']
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
    ucal__xmv = 'read_excel_df{}'.format(next_label())
    setattr(types, ucal__xmv, df_type)
    hmwta__zdmno = False
    if is_overload_constant_list(parse_dates):
        hmwta__zdmno = get_overload_const_list(parse_dates)
    ycaj__yodna = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    tvi__nva = f"""
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
    with numba.objmode(df="{ucal__xmv}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{ycaj__yodna}}},
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
            parse_dates={hmwta__zdmno},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    cwa__nvjj = {}
    exec(tvi__nva, globals(), cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as prl__nbx:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    tvi__nva = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    tvi__nva += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    tvi__nva += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        tvi__nva += '   fig, ax = plt.subplots()\n'
    else:
        tvi__nva += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        tvi__nva += '   fig.set_figwidth(figsize[0])\n'
        tvi__nva += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        tvi__nva += '   xlabel = x\n'
    tvi__nva += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        tvi__nva += '   ylabel = y\n'
    else:
        tvi__nva += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        tvi__nva += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        tvi__nva += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    tvi__nva += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            tvi__nva += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            hywqs__avc = get_overload_const_str(x)
            zrd__lemt = df.columns.index(hywqs__avc)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if zrd__lemt != i:
                        tvi__nva += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            tvi__nva += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        tvi__nva += '   ax.scatter(df[x], df[y], s=20)\n'
        tvi__nva += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        tvi__nva += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        tvi__nva += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        tvi__nva += '   ax.legend()\n'
    tvi__nva += '   return ax\n'
    cwa__nvjj = {}
    exec(tvi__nva, {'bodo': bodo, 'plt': plt}, cwa__nvjj)
    impl = cwa__nvjj['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for gvtao__bmpm in df_typ.data:
        if not (isinstance(gvtao__bmpm, IntegerArrayType) or isinstance(
            gvtao__bmpm.dtype, types.Number) or gvtao__bmpm.dtype in (bodo.
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
        baqta__qcp = args[0]
        mcg__lkao = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        jacc__crzcn = baqta__qcp
        check_runtime_cols_unsupported(baqta__qcp, 'set_df_col()')
        if isinstance(baqta__qcp, DataFrameType):
            index = baqta__qcp.index
            if len(baqta__qcp.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(baqta__qcp.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if mcg__lkao in baqta__qcp.columns:
                vlmsq__igwo = baqta__qcp.columns
                kxgg__peucs = baqta__qcp.columns.index(mcg__lkao)
                ccupa__ehi = list(baqta__qcp.data)
                ccupa__ehi[kxgg__peucs] = val
                ccupa__ehi = tuple(ccupa__ehi)
            else:
                vlmsq__igwo = baqta__qcp.columns + (mcg__lkao,)
                ccupa__ehi = baqta__qcp.data + (val,)
            jacc__crzcn = DataFrameType(ccupa__ehi, index, vlmsq__igwo,
                baqta__qcp.dist, baqta__qcp.is_table_format)
        return jacc__crzcn(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    tor__ffa = {}

    def _rewrite_membership_op(self, node, left, right):
        kew__ygq = node.op
        op = self.visit(kew__ygq)
        return op, kew__ygq, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    siqis__ddnxm = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in siqis__ddnxm:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in siqis__ddnxm:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        ckeg__prrny = node.attr
        value = node.value
        vcboh__oga = pd.core.computation.ops.LOCAL_TAG
        if ckeg__prrny in ('str', 'dt'):
            try:
                fouu__fixqh = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as mszaw__uke:
                col_name = mszaw__uke.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            fouu__fixqh = str(self.visit(value))
        wzwji__ddp = fouu__fixqh, ckeg__prrny
        if wzwji__ddp in join_cleaned_cols:
            ckeg__prrny = join_cleaned_cols[wzwji__ddp]
        name = fouu__fixqh + '.' + ckeg__prrny
        if name.startswith(vcboh__oga):
            name = name[len(vcboh__oga):]
        if ckeg__prrny in ('str', 'dt'):
            jsnz__fxr = columns[cleaned_columns.index(fouu__fixqh)]
            tor__ffa[jsnz__fxr] = fouu__fixqh
            self.env.scope[name] = 0
            return self.term_type(vcboh__oga + name, self.env)
        siqis__ddnxm.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in siqis__ddnxm:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        pjcg__rfmrj = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        mcg__lkao = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(pjcg__rfmrj), mcg__lkao))

    def op__str__(self):
        woxq__elud = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            rqexa__nwxeo)) for rqexa__nwxeo in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(woxq__elud)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(woxq__elud)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(woxq__elud))
    ziitx__yelkp = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    boq__lqhzy = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    gvcr__fqcjz = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    tnj__gbwl = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    wuv__kor = pd.core.computation.ops.Term.__str__
    hvu__ifigv = pd.core.computation.ops.MathCall.__str__
    vzkiy__eewiz = pd.core.computation.ops.Op.__str__
    auibe__rjrn = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        hkd__ewpmo = pd.core.computation.expr.Expr(expr, env=env)
        xgqg__mxq = str(hkd__ewpmo)
    except pd.core.computation.ops.UndefinedVariableError as mszaw__uke:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == mszaw__uke.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {mszaw__uke}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            ziitx__yelkp)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            boq__lqhzy)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = gvcr__fqcjz
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = tnj__gbwl
        pd.core.computation.ops.Term.__str__ = wuv__kor
        pd.core.computation.ops.MathCall.__str__ = hvu__ifigv
        pd.core.computation.ops.Op.__str__ = vzkiy__eewiz
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            auibe__rjrn)
    jva__dcy = pd.core.computation.parsing.clean_column_name
    tor__ffa.update({pnkk__ivfi: jva__dcy(pnkk__ivfi) for pnkk__ivfi in
        columns if jva__dcy(pnkk__ivfi) in hkd__ewpmo.names})
    return hkd__ewpmo, xgqg__mxq, tor__ffa


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        ykkcp__wvth = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(ykkcp__wvth))
        bohkr__gvube = namedtuple('Pandas', col_names)
        qky__tgbkk = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], bohkr__gvube)
        super(DataFrameTupleIterator, self).__init__(name, qky__tgbkk)

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
        bixhu__ebkia = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        bixhu__ebkia = [types.Array(types.int64, 1, 'C')] + bixhu__ebkia
        rwy__hoh = DataFrameTupleIterator(col_names, bixhu__ebkia)
        return rwy__hoh(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yuqx__vkl = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            yuqx__vkl)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    hjd__nbn = args[len(args) // 2:]
    meil__ptgm = sig.args[len(sig.args) // 2:]
    muxfh__hfzg = context.make_helper(builder, sig.return_type)
    xact__tsu = context.get_constant(types.intp, 0)
    qjlqj__jkfj = cgutils.alloca_once_value(builder, xact__tsu)
    muxfh__hfzg.index = qjlqj__jkfj
    for i, arr in enumerate(hjd__nbn):
        setattr(muxfh__hfzg, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(hjd__nbn, meil__ptgm):
        context.nrt.incref(builder, arr_typ, arr)
    res = muxfh__hfzg._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    tjgvi__bzq, = sig.args
    olabs__vyk, = args
    muxfh__hfzg = context.make_helper(builder, tjgvi__bzq, value=olabs__vyk)
    wrji__lsf = signature(types.intp, tjgvi__bzq.array_types[1])
    qcy__tfkoz = context.compile_internal(builder, lambda a: len(a),
        wrji__lsf, [muxfh__hfzg.array0])
    index = builder.load(muxfh__hfzg.index)
    ugtp__cbnw = builder.icmp_signed('<', index, qcy__tfkoz)
    result.set_valid(ugtp__cbnw)
    with builder.if_then(ugtp__cbnw):
        values = [index]
        for i, arr_typ in enumerate(tjgvi__bzq.array_types[1:]):
            agf__gaij = getattr(muxfh__hfzg, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                goopt__vknl = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    goopt__vknl, [agf__gaij, index])
            else:
                goopt__vknl = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    goopt__vknl, [agf__gaij, index])
            values.append(val)
        value = context.make_tuple(builder, tjgvi__bzq.yield_type, values)
        result.yield_(value)
        zhuag__wnf = cgutils.increment_index(builder, index)
        builder.store(zhuag__wnf, muxfh__hfzg.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    lgt__inqty = ir.Assign(rhs, lhs, expr.loc)
    wgx__rkyow = lhs
    dfe__ylb = []
    dtjh__lad = []
    gwl__jjarm = typ.count
    for i in range(gwl__jjarm):
        tfcph__okir = ir.Var(wgx__rkyow.scope, mk_unique_var('{}_size{}'.
            format(wgx__rkyow.name, i)), wgx__rkyow.loc)
        xrfn__cvboo = ir.Expr.static_getitem(lhs, i, None, wgx__rkyow.loc)
        self.calltypes[xrfn__cvboo] = None
        dfe__ylb.append(ir.Assign(xrfn__cvboo, tfcph__okir, wgx__rkyow.loc))
        self._define(equiv_set, tfcph__okir, types.intp, xrfn__cvboo)
        dtjh__lad.append(tfcph__okir)
    uly__qrnqi = tuple(dtjh__lad)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        uly__qrnqi, pre=[lgt__inqty] + dfe__ylb)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
