"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df_type,
            'pandas.groupby()')
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kwmk__gwka = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, kwmk__gwka)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type=None,
    dropna_type=None):

    def codegen(context, builder, signature, args):
        wbk__pnu = args[0]
        knbkt__kuc = signature.return_type
        djg__kszuw = cgutils.create_struct_proxy(knbkt__kuc)(context, builder)
        djg__kszuw.obj = wbk__pnu
        context.nrt.incref(builder, signature.args[0], wbk__pnu)
        return djg__kszuw._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for xmt__mei in keys:
        selection.remove(xmt__mei)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    knbkt__kuc = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return knbkt__kuc(obj_type, by_type, as_index_type, dropna_type), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, ixdu__spx = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(ixdu__spx, (tuple, list)):
                if len(set(ixdu__spx).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(ixdu__spx).difference(set(grpby.df_type
                        .columns))))
                selection = ixdu__spx
            else:
                if ixdu__spx not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(ixdu__spx))
                selection = ixdu__spx,
                series_select = True
            dua__gtzm = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(dua__gtzm, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, ixdu__spx = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            ixdu__spx):
            dua__gtzm = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(ixdu__spx)), {}).return_type
            return signature(dua__gtzm, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    tiqet__cqo = arr_type == ArrayItemArrayType(string_array_type)
    jlmbf__jxwr = arr_type.dtype
    if isinstance(jlmbf__jxwr, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {jlmbf__jxwr} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(jlmbf__jxwr, (
        Decimal128Type, types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {jlmbf__jxwr} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(jlmbf__jxwr
        , (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(jlmbf__jxwr, (types.Integer, types.Float, types.Boolean)
        ):
        if tiqet__cqo or jlmbf__jxwr == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(jlmbf__jxwr, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not jlmbf__jxwr.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {jlmbf__jxwr} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(jlmbf__jxwr, types.Boolean) and func_name in {'cumsum',
        'sum', 'mean', 'std', 'var'}:
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    if func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    if func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    jlmbf__jxwr = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(jlmbf__jxwr, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(jlmbf__jxwr, types.Integer):
            return IntDtype(jlmbf__jxwr)
        return jlmbf__jxwr
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        ngza__fliec = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{ngza__fliec}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for xmt__mei in grp.keys:
        if multi_level_names:
            bzvv__ausw = xmt__mei, ''
        else:
            bzvv__ausw = xmt__mei
        phn__impe = grp.df_type.columns.index(xmt__mei)
        data = to_str_arr_if_dict_array(grp.df_type.data[phn__impe])
        out_columns.append(bzvv__ausw)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name == 'head':
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name == 'head':
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        sxzvt__ajh = tuple(grp.df_type.column_index[grp.keys[xos__iyr]] for
            xos__iyr in range(len(grp.keys)))
        grhhl__vrz = tuple(grp.df_type.data[phn__impe] for phn__impe in
            sxzvt__ajh)
        grhhl__vrz = tuple(to_str_arr_if_dict_array(apxqx__rpl) for
            apxqx__rpl in grhhl__vrz)
        index = MultiIndexType(grhhl__vrz, tuple(types.StringLiteral(
            xmt__mei) for xmt__mei in grp.keys))
    else:
        phn__impe = grp.df_type.column_index[grp.keys[0]]
        hkxri__ycgcp = to_str_arr_if_dict_array(grp.df_type.data[phn__impe])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(hkxri__ycgcp,
            types.StringLiteral(grp.keys[0]))
    phsj__qbt = {}
    iosk__chj = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        phsj__qbt[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for byr__nzne in columns:
            phn__impe = grp.df_type.column_index[byr__nzne]
            data = grp.df_type.data[phn__impe]
            data = to_str_arr_if_dict_array(data)
            csdc__opef = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                csdc__opef = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    nssuo__jjc = SeriesType(data.dtype, data, None, string_type
                        )
                    ael__wpk = get_const_func_output_type(func, (nssuo__jjc
                        ,), {}, typing_context, target_context)
                    if ael__wpk != ArrayItemArrayType(string_array_type):
                        ael__wpk = dtype_to_array_type(ael__wpk)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=byr__nzne, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    ogluy__pxnvn = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    refx__abq = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    ydra__zpy = dict(numeric_only=ogluy__pxnvn, min_count=
                        refx__abq)
                    tphp__rvi = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        ydra__zpy, tphp__rvi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    ogluy__pxnvn = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    refx__abq = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    ydra__zpy = dict(numeric_only=ogluy__pxnvn, min_count=
                        refx__abq)
                    tphp__rvi = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        ydra__zpy, tphp__rvi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    ogluy__pxnvn = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    ydra__zpy = dict(numeric_only=ogluy__pxnvn)
                    tphp__rvi = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        ydra__zpy, tphp__rvi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    oqv__xxb = args[0] if len(args) > 0 else kws.pop('axis', 0)
                    dcnf__ikje = args[1] if len(args) > 1 else kws.pop('skipna'
                        , True)
                    ydra__zpy = dict(axis=oqv__xxb, skipna=dcnf__ikje)
                    tphp__rvi = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        ydra__zpy, tphp__rvi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    afuzw__bxo = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    ydra__zpy = dict(ddof=afuzw__bxo)
                    tphp__rvi = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        ydra__zpy, tphp__rvi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                ael__wpk, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                ahcb__bvhpx = to_str_arr_if_dict_array(ael__wpk)
                out_data.append(ahcb__bvhpx)
                out_columns.append(byr__nzne)
                if func_name == 'agg':
                    rheia__kjmao = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    phsj__qbt[byr__nzne, rheia__kjmao] = byr__nzne
                else:
                    phsj__qbt[byr__nzne, func_name] = byr__nzne
                out_column_type.append(csdc__opef)
            else:
                iosk__chj.append(err_msg)
    if func_name == 'sum':
        zah__ztg = any([(yuwax__kwkkp == ColumnType.NumericalColumn.value) for
            yuwax__kwkkp in out_column_type])
        if zah__ztg:
            out_data = [yuwax__kwkkp for yuwax__kwkkp, tmcqz__ccwni in zip(
                out_data, out_column_type) if tmcqz__ccwni != ColumnType.
                NonNumericalColumn.value]
            out_columns = [yuwax__kwkkp for yuwax__kwkkp, tmcqz__ccwni in
                zip(out_columns, out_column_type) if tmcqz__ccwni !=
                ColumnType.NonNumericalColumn.value]
            phsj__qbt = {}
            for byr__nzne in out_columns:
                if grp.as_index is False and byr__nzne in grp.keys:
                    continue
                phsj__qbt[byr__nzne, func_name] = byr__nzne
    bmywt__oxzmo = len(iosk__chj)
    if len(out_data) == 0:
        if bmywt__oxzmo == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(bmywt__oxzmo, ' was' if bmywt__oxzmo == 1 else
                's were', ','.join(iosk__chj)))
    xnrf__esmn = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            pwh__ulah = IntDtype(out_data[0].dtype)
        else:
            pwh__ulah = out_data[0].dtype
        wbzmz__uls = (types.none if func_name == 'size' else types.
            StringLiteral(grp.selection[0]))
        xnrf__esmn = SeriesType(pwh__ulah, index=index, name_typ=wbzmz__uls)
    return signature(xnrf__esmn, *args), phsj__qbt


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    utdo__mmde = True
    if isinstance(f_val, str):
        utdo__mmde = False
        gxryj__ddb = f_val
    elif is_overload_constant_str(f_val):
        utdo__mmde = False
        gxryj__ddb = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        utdo__mmde = False
        gxryj__ddb = bodo.utils.typing.get_builtin_function_name(f_val)
    if not utdo__mmde:
        if gxryj__ddb not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {gxryj__ddb}')
        dua__gtzm = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(dua__gtzm, (), gxryj__ddb, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            dqwd__dzum = types.functions.MakeFunctionLiteral(f_val)
        else:
            dqwd__dzum = f_val
        validate_udf('agg', dqwd__dzum)
        func = get_overload_const_func(dqwd__dzum, None)
        jldpp__iard = func.code if hasattr(func, 'code') else func.__code__
        gxryj__ddb = jldpp__iard.co_name
        dua__gtzm = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(dua__gtzm, (), 'agg', typing_context,
            target_context, dqwd__dzum)[0].return_type
    return gxryj__ddb, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    iilde__zewe = kws and all(isinstance(uvs__ydj, types.Tuple) and len(
        uvs__ydj) == 2 for uvs__ydj in kws.values())
    if is_overload_none(func) and not iilde__zewe:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not iilde__zewe:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    iyb__aaik = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if iilde__zewe or is_overload_constant_dict(func):
        if iilde__zewe:
            pgan__bmpaa = [get_literal_value(icggy__cjjw) for icggy__cjjw,
                twec__gzhu in kws.values()]
            lye__xakj = [get_literal_value(aimj__mqw) for twec__gzhu,
                aimj__mqw in kws.values()]
        else:
            yuc__ruokv = get_overload_constant_dict(func)
            pgan__bmpaa = tuple(yuc__ruokv.keys())
            lye__xakj = tuple(yuc__ruokv.values())
        if 'head' in lye__xakj:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(byr__nzne not in grp.selection and byr__nzne not in grp.keys for
            byr__nzne in pgan__bmpaa):
            raise_bodo_error(
                f'Selected column names {pgan__bmpaa} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            lye__xakj)
        if iilde__zewe and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        phsj__qbt = {}
        out_columns = []
        out_data = []
        out_column_type = []
        opmss__erbyk = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for edg__ghq, f_val in zip(pgan__bmpaa, lye__xakj):
            if isinstance(f_val, (tuple, list)):
                cdhgg__sjjw = 0
                for dqwd__dzum in f_val:
                    gxryj__ddb, out_tp = get_agg_funcname_and_outtyp(grp,
                        edg__ghq, dqwd__dzum, typing_context, target_context)
                    iyb__aaik = gxryj__ddb in list_cumulative
                    if gxryj__ddb == '<lambda>' and len(f_val) > 1:
                        gxryj__ddb = '<lambda_' + str(cdhgg__sjjw) + '>'
                        cdhgg__sjjw += 1
                    out_columns.append((edg__ghq, gxryj__ddb))
                    phsj__qbt[edg__ghq, gxryj__ddb] = edg__ghq, gxryj__ddb
                    _append_out_type(grp, out_data, out_tp)
            else:
                gxryj__ddb, out_tp = get_agg_funcname_and_outtyp(grp,
                    edg__ghq, f_val, typing_context, target_context)
                iyb__aaik = gxryj__ddb in list_cumulative
                if multi_level_names:
                    out_columns.append((edg__ghq, gxryj__ddb))
                    phsj__qbt[edg__ghq, gxryj__ddb] = edg__ghq, gxryj__ddb
                elif not iilde__zewe:
                    out_columns.append(edg__ghq)
                    phsj__qbt[edg__ghq, gxryj__ddb] = edg__ghq
                elif iilde__zewe:
                    opmss__erbyk.append(gxryj__ddb)
                _append_out_type(grp, out_data, out_tp)
        if iilde__zewe:
            for xos__iyr, smzko__bin in enumerate(kws.keys()):
                out_columns.append(smzko__bin)
                phsj__qbt[pgan__bmpaa[xos__iyr], opmss__erbyk[xos__iyr]
                    ] = smzko__bin
        if iyb__aaik:
            index = grp.df_type.index
        else:
            index = out_tp.index
        xnrf__esmn = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(xnrf__esmn, *args), phsj__qbt
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            azax__otfm = get_overload_const_list(func)
        else:
            azax__otfm = func.types
        if len(azax__otfm) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        cdhgg__sjjw = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        phsj__qbt = {}
        ualxk__qsry = grp.selection[0]
        for f_val in azax__otfm:
            gxryj__ddb, out_tp = get_agg_funcname_and_outtyp(grp,
                ualxk__qsry, f_val, typing_context, target_context)
            iyb__aaik = gxryj__ddb in list_cumulative
            if gxryj__ddb == '<lambda>' and len(azax__otfm) > 1:
                gxryj__ddb = '<lambda_' + str(cdhgg__sjjw) + '>'
                cdhgg__sjjw += 1
            out_columns.append(gxryj__ddb)
            phsj__qbt[ualxk__qsry, gxryj__ddb] = gxryj__ddb
            _append_out_type(grp, out_data, out_tp)
        if iyb__aaik:
            index = grp.df_type.index
        else:
            index = out_tp.index
        xnrf__esmn = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(xnrf__esmn, *args), phsj__qbt
    gxryj__ddb = ''
    if types.unliteral(func) == types.unicode_type:
        gxryj__ddb = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        gxryj__ddb = bodo.utils.typing.get_builtin_function_name(func)
    if gxryj__ddb:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, gxryj__ddb, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        oqv__xxb = args[0] if len(args) > 0 else kws.pop('axis', 0)
        ogluy__pxnvn = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        dcnf__ikje = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        ydra__zpy = dict(axis=oqv__xxb, numeric_only=ogluy__pxnvn)
        tphp__rvi = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', ydra__zpy,
            tphp__rvi, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        qok__sutpd = args[0] if len(args) > 0 else kws.pop('periods', 1)
        xtwdb__bnrnf = args[1] if len(args) > 1 else kws.pop('freq', None)
        oqv__xxb = args[2] if len(args) > 2 else kws.pop('axis', 0)
        rekrl__fce = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        ydra__zpy = dict(freq=xtwdb__bnrnf, axis=oqv__xxb, fill_value=
            rekrl__fce)
        tphp__rvi = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', ydra__zpy,
            tphp__rvi, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        vgbp__mrsz = args[0] if len(args) > 0 else kws.pop('func', None)
        wyhz__szyn = kws.pop('engine', None)
        kfau__ubaow = kws.pop('engine_kwargs', None)
        ydra__zpy = dict(engine=wyhz__szyn, engine_kwargs=kfau__ubaow)
        tphp__rvi = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', ydra__zpy, tphp__rvi,
            package_name='pandas', module_name='GroupBy')
    phsj__qbt = {}
    for byr__nzne in grp.selection:
        out_columns.append(byr__nzne)
        phsj__qbt[byr__nzne, name_operation] = byr__nzne
        phn__impe = grp.df_type.columns.index(byr__nzne)
        data = grp.df_type.data[phn__impe]
        data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            ael__wpk, err_msg = get_groupby_output_dtype(data,
                get_literal_value(vgbp__mrsz), grp.df_type.index)
            if err_msg == 'ok':
                data = ael__wpk
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    xnrf__esmn = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        xnrf__esmn = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(xnrf__esmn, *args), phsj__qbt


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        hnox__ckmr = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        icm__ril = isinstance(hnox__ckmr, (SeriesType, HeterogeneousSeriesType)
            ) and hnox__ckmr.const_info is not None or not isinstance(
            hnox__ckmr, (SeriesType, DataFrameType))
        if icm__ril:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                arv__pdydw = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                sxzvt__ajh = tuple(grp.df_type.columns.index(grp.keys[
                    xos__iyr]) for xos__iyr in range(len(grp.keys)))
                grhhl__vrz = tuple(grp.df_type.data[phn__impe] for
                    phn__impe in sxzvt__ajh)
                grhhl__vrz = tuple(to_str_arr_if_dict_array(apxqx__rpl) for
                    apxqx__rpl in grhhl__vrz)
                arv__pdydw = MultiIndexType(grhhl__vrz, tuple(types.literal
                    (xmt__mei) for xmt__mei in grp.keys))
            else:
                phn__impe = grp.df_type.columns.index(grp.keys[0])
                hkxri__ycgcp = grp.df_type.data[phn__impe]
                hkxri__ycgcp = to_str_arr_if_dict_array(hkxri__ycgcp)
                arv__pdydw = bodo.hiframes.pd_index_ext.array_type_to_index(
                    hkxri__ycgcp, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            sbx__zmy = tuple(grp.df_type.data[grp.df_type.columns.index(
                byr__nzne)] for byr__nzne in grp.keys)
            sbx__zmy = tuple(to_str_arr_if_dict_array(apxqx__rpl) for
                apxqx__rpl in sbx__zmy)
            eqphq__sqai = tuple(types.literal(uvs__ydj) for uvs__ydj in grp
                .keys) + get_index_name_types(hnox__ckmr.index)
            if not grp.as_index:
                sbx__zmy = types.Array(types.int64, 1, 'C'),
                eqphq__sqai = (types.none,) + get_index_name_types(hnox__ckmr
                    .index)
            arv__pdydw = MultiIndexType(sbx__zmy + get_index_data_arr_types
                (hnox__ckmr.index), eqphq__sqai)
        if icm__ril:
            if isinstance(hnox__ckmr, HeterogeneousSeriesType):
                twec__gzhu, hvdn__atq = hnox__ckmr.const_info
                if isinstance(hnox__ckmr.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    jrkp__hastf = hnox__ckmr.data.tuple_typ.types
                elif isinstance(hnox__ckmr.data, types.Tuple):
                    jrkp__hastf = hnox__ckmr.data.types
                hns__ucrhc = tuple(to_nullable_type(dtype_to_array_type(
                    apxqx__rpl)) for apxqx__rpl in jrkp__hastf)
                zmsez__lyxv = DataFrameType(out_data + hns__ucrhc,
                    arv__pdydw, out_columns + hvdn__atq)
            elif isinstance(hnox__ckmr, SeriesType):
                snnq__wcroh, hvdn__atq = hnox__ckmr.const_info
                hns__ucrhc = tuple(to_nullable_type(dtype_to_array_type(
                    hnox__ckmr.dtype)) for twec__gzhu in range(snnq__wcroh))
                zmsez__lyxv = DataFrameType(out_data + hns__ucrhc,
                    arv__pdydw, out_columns + hvdn__atq)
            else:
                qjs__jqg = get_udf_out_arr_type(hnox__ckmr)
                if not grp.as_index:
                    zmsez__lyxv = DataFrameType(out_data + (qjs__jqg,),
                        arv__pdydw, out_columns + ('',))
                else:
                    zmsez__lyxv = SeriesType(qjs__jqg.dtype, qjs__jqg,
                        arv__pdydw, None)
        elif isinstance(hnox__ckmr, SeriesType):
            zmsez__lyxv = SeriesType(hnox__ckmr.dtype, hnox__ckmr.data,
                arv__pdydw, hnox__ckmr.name_typ)
        else:
            zmsez__lyxv = DataFrameType(hnox__ckmr.data, arv__pdydw,
                hnox__ckmr.columns)
        dngm__emxnn = gen_apply_pysig(len(f_args), kws.keys())
        yxsda__eeiew = (func, *f_args) + tuple(kws.values())
        return signature(zmsez__lyxv, *yxsda__eeiew).replace(pysig=dngm__emxnn)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    tpfzr__xoh = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            edg__ghq = grp.selection[0]
            qjs__jqg = tpfzr__xoh.data[tpfzr__xoh.columns.index(edg__ghq)]
            qjs__jqg = to_str_arr_if_dict_array(qjs__jqg)
            dxga__kht = SeriesType(qjs__jqg.dtype, qjs__jqg, tpfzr__xoh.
                index, types.literal(edg__ghq))
        else:
            nwt__rdq = tuple(tpfzr__xoh.data[tpfzr__xoh.columns.index(
                byr__nzne)] for byr__nzne in grp.selection)
            nwt__rdq = tuple(to_str_arr_if_dict_array(apxqx__rpl) for
                apxqx__rpl in nwt__rdq)
            dxga__kht = DataFrameType(nwt__rdq, tpfzr__xoh.index, tuple(grp
                .selection))
    else:
        dxga__kht = tpfzr__xoh
    dsu__wousw = dxga__kht,
    dsu__wousw += tuple(f_args)
    try:
        hnox__ckmr = get_const_func_output_type(func, dsu__wousw, kws,
            typing_context, target_context)
    except Exception as cmu__tzic:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', cmu__tzic),
            getattr(cmu__tzic, 'loc', None))
    return hnox__ckmr


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    dsu__wousw = (grp,) + f_args
    try:
        hnox__ckmr = get_const_func_output_type(func, dsu__wousw, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as cmu__tzic:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', cmu__tzic),
            getattr(cmu__tzic, 'loc', None))
    dngm__emxnn = gen_apply_pysig(len(f_args), kws.keys())
    yxsda__eeiew = (func, *f_args) + tuple(kws.values())
    return signature(hnox__ckmr, *yxsda__eeiew).replace(pysig=dngm__emxnn)


def gen_apply_pysig(n_args, kws):
    qtv__rkq = ', '.join(f'arg{xos__iyr}' for xos__iyr in range(n_args))
    qtv__rkq = qtv__rkq + ', ' if qtv__rkq else ''
    lsxr__zqdh = ', '.join(f"{ile__eqkrj} = ''" for ile__eqkrj in kws)
    exmh__cdzu = f'def apply_stub(func, {qtv__rkq}{lsxr__zqdh}):\n'
    exmh__cdzu += '    pass\n'
    efuss__mihzf = {}
    exec(exmh__cdzu, {}, efuss__mihzf)
    aof__jlqub = efuss__mihzf['apply_stub']
    return numba.core.utils.pysignature(aof__jlqub)


def pivot_table_dummy(df, values, index, columns, aggfunc, _pivot_values):
    return 0


@infer_global(pivot_table_dummy)
class PivotTableTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, values, index, columns, aggfunc, _pivot_values = args
        if not (is_overload_constant_str(values) and
            is_overload_constant_str(index) and is_overload_constant_str(
            columns)):
            raise BodoError(
                "pivot_table() only support string constants for 'values', 'index' and 'columns' arguments"
                )
        values = values.literal_value
        index = index.literal_value
        columns = columns.literal_value
        data = df.data[df.columns.index(values)]
        data = to_str_arr_if_dict_array(data)
        ael__wpk = get_pivot_output_dtype(data, aggfunc.literal_value)
        hpng__vnfew = dtype_to_array_type(ael__wpk)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/api_docs/pandas/dataframe/#pddataframepivot.'
                )
        nwm__acej = _pivot_values.meta
        yqjgl__vcg = len(nwm__acej)
        phn__impe = df.columns.index(index)
        hkxri__ycgcp = df.data[phn__impe]
        hkxri__ycgcp = to_str_arr_if_dict_array(hkxri__ycgcp)
        jgz__xwjun = bodo.hiframes.pd_index_ext.array_type_to_index(
            hkxri__ycgcp, types.StringLiteral(index))
        amu__jfez = DataFrameType((hpng__vnfew,) * yqjgl__vcg, jgz__xwjun,
            tuple(nwm__acej))
        return signature(amu__jfez, *args)


PivotTableTyper._no_unliteral = True


@lower_builtin(pivot_table_dummy, types.VarArg(types.Any))
def lower_pivot_table_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        hpng__vnfew = types.Array(types.int64, 1, 'C')
        nwm__acej = _pivot_values.meta
        yqjgl__vcg = len(nwm__acej)
        jgz__xwjun = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        amu__jfez = DataFrameType((hpng__vnfew,) * yqjgl__vcg, jgz__xwjun,
            tuple(nwm__acej))
        return signature(amu__jfez, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    exmh__cdzu = 'def impl(keys, dropna, _is_parallel):\n'
    exmh__cdzu += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    exmh__cdzu += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{xos__iyr}])' for xos__iyr in range(len(keys.
        types))))
    exmh__cdzu += '    table = arr_info_list_to_table(info_list)\n'
    exmh__cdzu += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    exmh__cdzu += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    exmh__cdzu += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    exmh__cdzu += '    delete_table_decref_arrays(table)\n'
    exmh__cdzu += '    ev.finalize()\n'
    exmh__cdzu += '    return sort_idx, group_labels, ngroups\n'
    efuss__mihzf = {}
    exec(exmh__cdzu, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, efuss__mihzf
        )
    ciflw__xctum = efuss__mihzf['impl']
    return ciflw__xctum


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    kasf__hnqkq = len(labels)
    skrri__bzqel = np.zeros(ngroups, dtype=np.int64)
    oaoif__umx = np.zeros(ngroups, dtype=np.int64)
    tekk__jonz = 0
    fzdrn__ole = 0
    for xos__iyr in range(kasf__hnqkq):
        mwycq__vzgu = labels[xos__iyr]
        if mwycq__vzgu < 0:
            tekk__jonz += 1
        else:
            fzdrn__ole += 1
            if xos__iyr == kasf__hnqkq - 1 or mwycq__vzgu != labels[
                xos__iyr + 1]:
                skrri__bzqel[mwycq__vzgu] = tekk__jonz
                oaoif__umx[mwycq__vzgu] = tekk__jonz + fzdrn__ole
                tekk__jonz += fzdrn__ole
                fzdrn__ole = 0
    return skrri__bzqel, oaoif__umx


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ciflw__xctum, twec__gzhu = gen_shuffle_dataframe(df, keys, _is_parallel)
    return ciflw__xctum


def gen_shuffle_dataframe(df, keys, _is_parallel):
    snnq__wcroh = len(df.columns)
    xlg__ikfz = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    exmh__cdzu = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        exmh__cdzu += '  return df, keys, get_null_shuffle_info()\n'
        efuss__mihzf = {}
        exec(exmh__cdzu, {'get_null_shuffle_info': get_null_shuffle_info},
            efuss__mihzf)
        ciflw__xctum = efuss__mihzf['impl']
        return ciflw__xctum
    for xos__iyr in range(snnq__wcroh):
        exmh__cdzu += f"""  in_arr{xos__iyr} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {xos__iyr})
"""
    exmh__cdzu += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    exmh__cdzu += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{xos__iyr}])' for xos__iyr in range(xlg__ikfz)
        ), ', '.join(f'array_to_info(in_arr{xos__iyr})' for xos__iyr in
        range(snnq__wcroh)), 'array_to_info(in_index_arr)')
    exmh__cdzu += '  table = arr_info_list_to_table(info_list)\n'
    exmh__cdzu += (
        f'  out_table = shuffle_table(table, {xlg__ikfz}, _is_parallel, 1)\n')
    for xos__iyr in range(xlg__ikfz):
        exmh__cdzu += f"""  out_key{xos__iyr} = info_to_array(info_from_table(out_table, {xos__iyr}), keys{xos__iyr}_typ)
"""
    for xos__iyr in range(snnq__wcroh):
        exmh__cdzu += f"""  out_arr{xos__iyr} = info_to_array(info_from_table(out_table, {xos__iyr + xlg__ikfz}), in_arr{xos__iyr}_typ)
"""
    exmh__cdzu += f"""  out_arr_index = info_to_array(info_from_table(out_table, {xlg__ikfz + snnq__wcroh}), ind_arr_typ)
"""
    exmh__cdzu += '  shuffle_info = get_shuffle_info(out_table)\n'
    exmh__cdzu += '  delete_table(out_table)\n'
    exmh__cdzu += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{xos__iyr}' for xos__iyr in range(
        snnq__wcroh))
    exmh__cdzu += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    exmh__cdzu += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    exmh__cdzu += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{xos__iyr}' for xos__iyr in range(xlg__ikfz)))
    jqt__eho = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    jqt__eho.update({f'keys{xos__iyr}_typ': keys.types[xos__iyr] for
        xos__iyr in range(xlg__ikfz)})
    jqt__eho.update({f'in_arr{xos__iyr}_typ': df.data[xos__iyr] for
        xos__iyr in range(snnq__wcroh)})
    efuss__mihzf = {}
    exec(exmh__cdzu, jqt__eho, efuss__mihzf)
    ciflw__xctum = efuss__mihzf['impl']
    return ciflw__xctum, jqt__eho


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        qgvl__dwyro = len(data.array_types)
        exmh__cdzu = 'def impl(data, shuffle_info):\n'
        exmh__cdzu += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{xos__iyr}])' for xos__iyr in range(
            qgvl__dwyro)))
        exmh__cdzu += '  table = arr_info_list_to_table(info_list)\n'
        exmh__cdzu += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for xos__iyr in range(qgvl__dwyro):
            exmh__cdzu += f"""  out_arr{xos__iyr} = info_to_array(info_from_table(out_table, {xos__iyr}), data._data[{xos__iyr}])
"""
        exmh__cdzu += '  delete_table(out_table)\n'
        exmh__cdzu += '  delete_table(table)\n'
        exmh__cdzu += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{xos__iyr}' for xos__iyr in range(
            qgvl__dwyro))))
        efuss__mihzf = {}
        exec(exmh__cdzu, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, efuss__mihzf)
        ciflw__xctum = efuss__mihzf['impl']
        return ciflw__xctum
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ihf__lkopv = bodo.utils.conversion.index_to_array(data)
            ahcb__bvhpx = reverse_shuffle(ihf__lkopv, shuffle_info)
            return bodo.utils.conversion.index_from_array(ahcb__bvhpx)
        return impl_index

    def impl_arr(data, shuffle_info):
        qag__gsw = [array_to_info(data)]
        swj__tzjq = arr_info_list_to_table(qag__gsw)
        qfxkh__qtrid = reverse_shuffle_table(swj__tzjq, shuffle_info)
        ahcb__bvhpx = info_to_array(info_from_table(qfxkh__qtrid, 0), data)
        delete_table(qfxkh__qtrid)
        delete_table(swj__tzjq)
        return ahcb__bvhpx
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    ydra__zpy = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    tphp__rvi = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', ydra__zpy, tphp__rvi,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    kjs__dwfgs = get_overload_const_bool(ascending)
    sgu__nwsbb = grp.selection[0]
    exmh__cdzu = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    kvx__uwx = (
        f"lambda S: S.value_counts(ascending={kjs__dwfgs}, _index_name='{sgu__nwsbb}')"
        )
    exmh__cdzu += f'    return grp.apply({kvx__uwx})\n'
    efuss__mihzf = {}
    exec(exmh__cdzu, {'bodo': bodo}, efuss__mihzf)
    ciflw__xctum = efuss__mihzf['impl']
    return ciflw__xctum


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill',
    'ngroup', 'nth', 'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail',
    'corr', 'cov', 'describe', 'diff', 'fillna', 'filter', 'hist', 'mad',
    'plot', 'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for ojbgv__jzb in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, ojbgv__jzb, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{ojbgv__jzb}'))
    for ojbgv__jzb in groupby_unsupported:
        overload_method(DataFrameGroupByType, ojbgv__jzb, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{ojbgv__jzb}'))
    for ojbgv__jzb in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, ojbgv__jzb, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{ojbgv__jzb}'))
    for ojbgv__jzb in series_only_unsupported:
        overload_method(DataFrameGroupByType, ojbgv__jzb, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{ojbgv__jzb}'))
    for ojbgv__jzb in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, ojbgv__jzb, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{ojbgv__jzb}'))


_install_groupby_unsupported()
