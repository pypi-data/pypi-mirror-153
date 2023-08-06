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
        sczt__risz = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, sczt__risz)


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
        gnzlj__qku = args[0]
        inhjw__slzas = signature.return_type
        qnytb__uexs = cgutils.create_struct_proxy(inhjw__slzas)(context,
            builder)
        qnytb__uexs.obj = gnzlj__qku
        context.nrt.incref(builder, signature.args[0], gnzlj__qku)
        return qnytb__uexs._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for ypdhn__iez in keys:
        selection.remove(ypdhn__iez)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    inhjw__slzas = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return inhjw__slzas(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, xby__alb = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(xby__alb, (tuple, list)):
                if len(set(xby__alb).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(xby__alb).difference(set(grpby.df_type.
                        columns))))
                selection = xby__alb
            else:
                if xby__alb not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(xby__alb))
                selection = xby__alb,
                series_select = True
            fcjz__ocitn = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(fcjz__ocitn, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, xby__alb = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(xby__alb
            ):
            fcjz__ocitn = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(xby__alb)), {}).return_type
            return signature(fcjz__ocitn, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    txuml__nzten = arr_type == ArrayItemArrayType(string_array_type)
    iaywc__krp = arr_type.dtype
    if isinstance(iaywc__krp, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {iaywc__krp} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(iaywc__krp, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {iaywc__krp} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(iaywc__krp,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(iaywc__krp, (types.Integer, types.Float, types.Boolean)):
        if txuml__nzten or iaywc__krp == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(iaywc__krp, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not iaywc__krp.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {iaywc__krp} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(iaywc__krp, types.Boolean) and func_name in {'cumsum',
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
    iaywc__krp = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(iaywc__krp, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(iaywc__krp, types.Integer):
            return IntDtype(iaywc__krp)
        return iaywc__krp
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        yktmk__ilma = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{yktmk__ilma}'."
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
    for ypdhn__iez in grp.keys:
        if multi_level_names:
            jjbc__ute = ypdhn__iez, ''
        else:
            jjbc__ute = ypdhn__iez
        skudu__yux = grp.df_type.columns.index(ypdhn__iez)
        data = to_str_arr_if_dict_array(grp.df_type.data[skudu__yux])
        out_columns.append(jjbc__ute)
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
        wpqmy__sut = tuple(grp.df_type.column_index[grp.keys[xehsx__lvc]] for
            xehsx__lvc in range(len(grp.keys)))
        odlhw__vlip = tuple(grp.df_type.data[skudu__yux] for skudu__yux in
            wpqmy__sut)
        odlhw__vlip = tuple(to_str_arr_if_dict_array(xscui__deqy) for
            xscui__deqy in odlhw__vlip)
        index = MultiIndexType(odlhw__vlip, tuple(types.StringLiteral(
            ypdhn__iez) for ypdhn__iez in grp.keys))
    else:
        skudu__yux = grp.df_type.column_index[grp.keys[0]]
        mvrc__xaje = to_str_arr_if_dict_array(grp.df_type.data[skudu__yux])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(mvrc__xaje,
            types.StringLiteral(grp.keys[0]))
    vkv__akvrp = {}
    grx__nkh = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        vkv__akvrp[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for kzkq__ykmv in columns:
            skudu__yux = grp.df_type.column_index[kzkq__ykmv]
            data = grp.df_type.data[skudu__yux]
            data = to_str_arr_if_dict_array(data)
            mgzqa__yhhra = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                mgzqa__yhhra = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    hiih__ydsb = SeriesType(data.dtype, data, None, string_type
                        )
                    hmz__prac = get_const_func_output_type(func, (
                        hiih__ydsb,), {}, typing_context, target_context)
                    if hmz__prac != ArrayItemArrayType(string_array_type):
                        hmz__prac = dtype_to_array_type(hmz__prac)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=kzkq__ykmv, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    dochp__lrew = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    ayda__gfmw = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    hfswj__wng = dict(numeric_only=dochp__lrew, min_count=
                        ayda__gfmw)
                    mjya__ipfn = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hfswj__wng, mjya__ipfn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    dochp__lrew = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    ayda__gfmw = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    hfswj__wng = dict(numeric_only=dochp__lrew, min_count=
                        ayda__gfmw)
                    mjya__ipfn = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hfswj__wng, mjya__ipfn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    dochp__lrew = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    hfswj__wng = dict(numeric_only=dochp__lrew)
                    mjya__ipfn = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hfswj__wng, mjya__ipfn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    dii__qwxwn = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    jzzqt__dirh = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    hfswj__wng = dict(axis=dii__qwxwn, skipna=jzzqt__dirh)
                    mjya__ipfn = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hfswj__wng, mjya__ipfn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    mgywc__ezj = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    hfswj__wng = dict(ddof=mgywc__ezj)
                    mjya__ipfn = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hfswj__wng, mjya__ipfn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                hmz__prac, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                mycuw__pvrdg = to_str_arr_if_dict_array(hmz__prac)
                out_data.append(mycuw__pvrdg)
                out_columns.append(kzkq__ykmv)
                if func_name == 'agg':
                    hxmih__vka = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    vkv__akvrp[kzkq__ykmv, hxmih__vka] = kzkq__ykmv
                else:
                    vkv__akvrp[kzkq__ykmv, func_name] = kzkq__ykmv
                out_column_type.append(mgzqa__yhhra)
            else:
                grx__nkh.append(err_msg)
    if func_name == 'sum':
        pes__eevxg = any([(iauj__thx == ColumnType.NumericalColumn.value) for
            iauj__thx in out_column_type])
        if pes__eevxg:
            out_data = [iauj__thx for iauj__thx, mqji__botu in zip(out_data,
                out_column_type) if mqji__botu != ColumnType.
                NonNumericalColumn.value]
            out_columns = [iauj__thx for iauj__thx, mqji__botu in zip(
                out_columns, out_column_type) if mqji__botu != ColumnType.
                NonNumericalColumn.value]
            vkv__akvrp = {}
            for kzkq__ykmv in out_columns:
                if grp.as_index is False and kzkq__ykmv in grp.keys:
                    continue
                vkv__akvrp[kzkq__ykmv, func_name] = kzkq__ykmv
    gwk__jzn = len(grx__nkh)
    if len(out_data) == 0:
        if gwk__jzn == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(gwk__jzn, ' was' if gwk__jzn == 1 else 's were',
                ','.join(grx__nkh)))
    rwsnr__olagf = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            deh__imj = IntDtype(out_data[0].dtype)
        else:
            deh__imj = out_data[0].dtype
        huy__rrb = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        rwsnr__olagf = SeriesType(deh__imj, index=index, name_typ=huy__rrb)
    return signature(rwsnr__olagf, *args), vkv__akvrp


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    ppgq__pis = True
    if isinstance(f_val, str):
        ppgq__pis = False
        uwz__xqvnz = f_val
    elif is_overload_constant_str(f_val):
        ppgq__pis = False
        uwz__xqvnz = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        ppgq__pis = False
        uwz__xqvnz = bodo.utils.typing.get_builtin_function_name(f_val)
    if not ppgq__pis:
        if uwz__xqvnz not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {uwz__xqvnz}')
        fcjz__ocitn = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(fcjz__ocitn, (), uwz__xqvnz, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            oimet__odcjt = types.functions.MakeFunctionLiteral(f_val)
        else:
            oimet__odcjt = f_val
        validate_udf('agg', oimet__odcjt)
        func = get_overload_const_func(oimet__odcjt, None)
        ixfw__hvgz = func.code if hasattr(func, 'code') else func.__code__
        uwz__xqvnz = ixfw__hvgz.co_name
        fcjz__ocitn = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(fcjz__ocitn, (), 'agg', typing_context,
            target_context, oimet__odcjt)[0].return_type
    return uwz__xqvnz, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    hfh__hfx = kws and all(isinstance(ies__pkm, types.Tuple) and len(
        ies__pkm) == 2 for ies__pkm in kws.values())
    if is_overload_none(func) and not hfh__hfx:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not hfh__hfx:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    nxmkd__gblq = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if hfh__hfx or is_overload_constant_dict(func):
        if hfh__hfx:
            qpf__jcqv = [get_literal_value(ynyn__phxx) for ynyn__phxx,
                bgid__rshn in kws.values()]
            hinv__nebhy = [get_literal_value(ilpy__xwh) for bgid__rshn,
                ilpy__xwh in kws.values()]
        else:
            ruprp__dfqu = get_overload_constant_dict(func)
            qpf__jcqv = tuple(ruprp__dfqu.keys())
            hinv__nebhy = tuple(ruprp__dfqu.values())
        if 'head' in hinv__nebhy:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(kzkq__ykmv not in grp.selection and kzkq__ykmv not in grp.
            keys for kzkq__ykmv in qpf__jcqv):
            raise_bodo_error(
                f'Selected column names {qpf__jcqv} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            hinv__nebhy)
        if hfh__hfx and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        vkv__akvrp = {}
        out_columns = []
        out_data = []
        out_column_type = []
        qrj__qayrm = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for sfbxh__yjtl, f_val in zip(qpf__jcqv, hinv__nebhy):
            if isinstance(f_val, (tuple, list)):
                tuz__strc = 0
                for oimet__odcjt in f_val:
                    uwz__xqvnz, out_tp = get_agg_funcname_and_outtyp(grp,
                        sfbxh__yjtl, oimet__odcjt, typing_context,
                        target_context)
                    nxmkd__gblq = uwz__xqvnz in list_cumulative
                    if uwz__xqvnz == '<lambda>' and len(f_val) > 1:
                        uwz__xqvnz = '<lambda_' + str(tuz__strc) + '>'
                        tuz__strc += 1
                    out_columns.append((sfbxh__yjtl, uwz__xqvnz))
                    vkv__akvrp[sfbxh__yjtl, uwz__xqvnz
                        ] = sfbxh__yjtl, uwz__xqvnz
                    _append_out_type(grp, out_data, out_tp)
            else:
                uwz__xqvnz, out_tp = get_agg_funcname_and_outtyp(grp,
                    sfbxh__yjtl, f_val, typing_context, target_context)
                nxmkd__gblq = uwz__xqvnz in list_cumulative
                if multi_level_names:
                    out_columns.append((sfbxh__yjtl, uwz__xqvnz))
                    vkv__akvrp[sfbxh__yjtl, uwz__xqvnz
                        ] = sfbxh__yjtl, uwz__xqvnz
                elif not hfh__hfx:
                    out_columns.append(sfbxh__yjtl)
                    vkv__akvrp[sfbxh__yjtl, uwz__xqvnz] = sfbxh__yjtl
                elif hfh__hfx:
                    qrj__qayrm.append(uwz__xqvnz)
                _append_out_type(grp, out_data, out_tp)
        if hfh__hfx:
            for xehsx__lvc, hkwlr__pbuj in enumerate(kws.keys()):
                out_columns.append(hkwlr__pbuj)
                vkv__akvrp[qpf__jcqv[xehsx__lvc], qrj__qayrm[xehsx__lvc]
                    ] = hkwlr__pbuj
        if nxmkd__gblq:
            index = grp.df_type.index
        else:
            index = out_tp.index
        rwsnr__olagf = DataFrameType(tuple(out_data), index, tuple(out_columns)
            )
        return signature(rwsnr__olagf, *args), vkv__akvrp
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            cakw__hdf = get_overload_const_list(func)
        else:
            cakw__hdf = func.types
        if len(cakw__hdf) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        tuz__strc = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        vkv__akvrp = {}
        ysr__kmdw = grp.selection[0]
        for f_val in cakw__hdf:
            uwz__xqvnz, out_tp = get_agg_funcname_and_outtyp(grp, ysr__kmdw,
                f_val, typing_context, target_context)
            nxmkd__gblq = uwz__xqvnz in list_cumulative
            if uwz__xqvnz == '<lambda>' and len(cakw__hdf) > 1:
                uwz__xqvnz = '<lambda_' + str(tuz__strc) + '>'
                tuz__strc += 1
            out_columns.append(uwz__xqvnz)
            vkv__akvrp[ysr__kmdw, uwz__xqvnz] = uwz__xqvnz
            _append_out_type(grp, out_data, out_tp)
        if nxmkd__gblq:
            index = grp.df_type.index
        else:
            index = out_tp.index
        rwsnr__olagf = DataFrameType(tuple(out_data), index, tuple(out_columns)
            )
        return signature(rwsnr__olagf, *args), vkv__akvrp
    uwz__xqvnz = ''
    if types.unliteral(func) == types.unicode_type:
        uwz__xqvnz = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        uwz__xqvnz = bodo.utils.typing.get_builtin_function_name(func)
    if uwz__xqvnz:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, uwz__xqvnz, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        dii__qwxwn = args[0] if len(args) > 0 else kws.pop('axis', 0)
        dochp__lrew = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        jzzqt__dirh = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        hfswj__wng = dict(axis=dii__qwxwn, numeric_only=dochp__lrew)
        mjya__ipfn = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', hfswj__wng,
            mjya__ipfn, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        wcyk__gyrtm = args[0] if len(args) > 0 else kws.pop('periods', 1)
        fgekh__pdsno = args[1] if len(args) > 1 else kws.pop('freq', None)
        dii__qwxwn = args[2] if len(args) > 2 else kws.pop('axis', 0)
        vkalx__vavtm = args[3] if len(args) > 3 else kws.pop('fill_value', None
            )
        hfswj__wng = dict(freq=fgekh__pdsno, axis=dii__qwxwn, fill_value=
            vkalx__vavtm)
        mjya__ipfn = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', hfswj__wng,
            mjya__ipfn, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        hhwxa__ywu = args[0] if len(args) > 0 else kws.pop('func', None)
        gtnj__hlvf = kws.pop('engine', None)
        tvxpy__djc = kws.pop('engine_kwargs', None)
        hfswj__wng = dict(engine=gtnj__hlvf, engine_kwargs=tvxpy__djc)
        mjya__ipfn = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', hfswj__wng, mjya__ipfn,
            package_name='pandas', module_name='GroupBy')
    vkv__akvrp = {}
    for kzkq__ykmv in grp.selection:
        out_columns.append(kzkq__ykmv)
        vkv__akvrp[kzkq__ykmv, name_operation] = kzkq__ykmv
        skudu__yux = grp.df_type.columns.index(kzkq__ykmv)
        data = grp.df_type.data[skudu__yux]
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
            hmz__prac, err_msg = get_groupby_output_dtype(data,
                get_literal_value(hhwxa__ywu), grp.df_type.index)
            if err_msg == 'ok':
                data = hmz__prac
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    rwsnr__olagf = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        rwsnr__olagf = SeriesType(out_data[0].dtype, data=out_data[0],
            index=index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(rwsnr__olagf, *args), vkv__akvrp


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
        xca__aptwa = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        uyahf__ecg = isinstance(xca__aptwa, (SeriesType,
            HeterogeneousSeriesType)
            ) and xca__aptwa.const_info is not None or not isinstance(
            xca__aptwa, (SeriesType, DataFrameType))
        if uyahf__ecg:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                gyc__xdadz = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                wpqmy__sut = tuple(grp.df_type.columns.index(grp.keys[
                    xehsx__lvc]) for xehsx__lvc in range(len(grp.keys)))
                odlhw__vlip = tuple(grp.df_type.data[skudu__yux] for
                    skudu__yux in wpqmy__sut)
                odlhw__vlip = tuple(to_str_arr_if_dict_array(xscui__deqy) for
                    xscui__deqy in odlhw__vlip)
                gyc__xdadz = MultiIndexType(odlhw__vlip, tuple(types.
                    literal(ypdhn__iez) for ypdhn__iez in grp.keys))
            else:
                skudu__yux = grp.df_type.columns.index(grp.keys[0])
                mvrc__xaje = grp.df_type.data[skudu__yux]
                mvrc__xaje = to_str_arr_if_dict_array(mvrc__xaje)
                gyc__xdadz = bodo.hiframes.pd_index_ext.array_type_to_index(
                    mvrc__xaje, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            ytz__mspv = tuple(grp.df_type.data[grp.df_type.columns.index(
                kzkq__ykmv)] for kzkq__ykmv in grp.keys)
            ytz__mspv = tuple(to_str_arr_if_dict_array(xscui__deqy) for
                xscui__deqy in ytz__mspv)
            deww__jdt = tuple(types.literal(ies__pkm) for ies__pkm in grp.keys
                ) + get_index_name_types(xca__aptwa.index)
            if not grp.as_index:
                ytz__mspv = types.Array(types.int64, 1, 'C'),
                deww__jdt = (types.none,) + get_index_name_types(xca__aptwa
                    .index)
            gyc__xdadz = MultiIndexType(ytz__mspv +
                get_index_data_arr_types(xca__aptwa.index), deww__jdt)
        if uyahf__ecg:
            if isinstance(xca__aptwa, HeterogeneousSeriesType):
                bgid__rshn, blnk__lhjm = xca__aptwa.const_info
                if isinstance(xca__aptwa.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    asii__wnos = xca__aptwa.data.tuple_typ.types
                elif isinstance(xca__aptwa.data, types.Tuple):
                    asii__wnos = xca__aptwa.data.types
                cyzd__igti = tuple(to_nullable_type(dtype_to_array_type(
                    xscui__deqy)) for xscui__deqy in asii__wnos)
                mtxmj__suew = DataFrameType(out_data + cyzd__igti,
                    gyc__xdadz, out_columns + blnk__lhjm)
            elif isinstance(xca__aptwa, SeriesType):
                axmqh__gjbs, blnk__lhjm = xca__aptwa.const_info
                cyzd__igti = tuple(to_nullable_type(dtype_to_array_type(
                    xca__aptwa.dtype)) for bgid__rshn in range(axmqh__gjbs))
                mtxmj__suew = DataFrameType(out_data + cyzd__igti,
                    gyc__xdadz, out_columns + blnk__lhjm)
            else:
                ebe__kvtec = get_udf_out_arr_type(xca__aptwa)
                if not grp.as_index:
                    mtxmj__suew = DataFrameType(out_data + (ebe__kvtec,),
                        gyc__xdadz, out_columns + ('',))
                else:
                    mtxmj__suew = SeriesType(ebe__kvtec.dtype, ebe__kvtec,
                        gyc__xdadz, None)
        elif isinstance(xca__aptwa, SeriesType):
            mtxmj__suew = SeriesType(xca__aptwa.dtype, xca__aptwa.data,
                gyc__xdadz, xca__aptwa.name_typ)
        else:
            mtxmj__suew = DataFrameType(xca__aptwa.data, gyc__xdadz,
                xca__aptwa.columns)
        sgxjz__bouln = gen_apply_pysig(len(f_args), kws.keys())
        hykjl__cwoj = (func, *f_args) + tuple(kws.values())
        return signature(mtxmj__suew, *hykjl__cwoj).replace(pysig=sgxjz__bouln)

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
    rnv__zgk = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            sfbxh__yjtl = grp.selection[0]
            ebe__kvtec = rnv__zgk.data[rnv__zgk.columns.index(sfbxh__yjtl)]
            ebe__kvtec = to_str_arr_if_dict_array(ebe__kvtec)
            nnr__dgz = SeriesType(ebe__kvtec.dtype, ebe__kvtec, rnv__zgk.
                index, types.literal(sfbxh__yjtl))
        else:
            mbztp__daqi = tuple(rnv__zgk.data[rnv__zgk.columns.index(
                kzkq__ykmv)] for kzkq__ykmv in grp.selection)
            mbztp__daqi = tuple(to_str_arr_if_dict_array(xscui__deqy) for
                xscui__deqy in mbztp__daqi)
            nnr__dgz = DataFrameType(mbztp__daqi, rnv__zgk.index, tuple(grp
                .selection))
    else:
        nnr__dgz = rnv__zgk
    sbhxi__nwuos = nnr__dgz,
    sbhxi__nwuos += tuple(f_args)
    try:
        xca__aptwa = get_const_func_output_type(func, sbhxi__nwuos, kws,
            typing_context, target_context)
    except Exception as gcs__peeak:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', gcs__peeak),
            getattr(gcs__peeak, 'loc', None))
    return xca__aptwa


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    sbhxi__nwuos = (grp,) + f_args
    try:
        xca__aptwa = get_const_func_output_type(func, sbhxi__nwuos, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as gcs__peeak:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', gcs__peeak
            ), getattr(gcs__peeak, 'loc', None))
    sgxjz__bouln = gen_apply_pysig(len(f_args), kws.keys())
    hykjl__cwoj = (func, *f_args) + tuple(kws.values())
    return signature(xca__aptwa, *hykjl__cwoj).replace(pysig=sgxjz__bouln)


def gen_apply_pysig(n_args, kws):
    vobk__ijdj = ', '.join(f'arg{xehsx__lvc}' for xehsx__lvc in range(n_args))
    vobk__ijdj = vobk__ijdj + ', ' if vobk__ijdj else ''
    ksxk__kkn = ', '.join(f"{sjtu__zpo} = ''" for sjtu__zpo in kws)
    pjhl__uxzn = f'def apply_stub(func, {vobk__ijdj}{ksxk__kkn}):\n'
    pjhl__uxzn += '    pass\n'
    whswf__nkuf = {}
    exec(pjhl__uxzn, {}, whswf__nkuf)
    hbmb__ylql = whswf__nkuf['apply_stub']
    return numba.core.utils.pysignature(hbmb__ylql)


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
        hmz__prac = get_pivot_output_dtype(data, aggfunc.literal_value)
        rudp__meptm = dtype_to_array_type(hmz__prac)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/api_docs/pandas/dataframe/#pddataframepivot.'
                )
        muimy__lpq = _pivot_values.meta
        wejvc__nini = len(muimy__lpq)
        skudu__yux = df.columns.index(index)
        mvrc__xaje = df.data[skudu__yux]
        mvrc__xaje = to_str_arr_if_dict_array(mvrc__xaje)
        bkgwu__bczz = bodo.hiframes.pd_index_ext.array_type_to_index(mvrc__xaje
            , types.StringLiteral(index))
        zrsq__exaan = DataFrameType((rudp__meptm,) * wejvc__nini,
            bkgwu__bczz, tuple(muimy__lpq))
        return signature(zrsq__exaan, *args)


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
        rudp__meptm = types.Array(types.int64, 1, 'C')
        muimy__lpq = _pivot_values.meta
        wejvc__nini = len(muimy__lpq)
        bkgwu__bczz = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        zrsq__exaan = DataFrameType((rudp__meptm,) * wejvc__nini,
            bkgwu__bczz, tuple(muimy__lpq))
        return signature(zrsq__exaan, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    pjhl__uxzn = 'def impl(keys, dropna, _is_parallel):\n'
    pjhl__uxzn += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    pjhl__uxzn += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{xehsx__lvc}])' for xehsx__lvc in range(len(
        keys.types))))
    pjhl__uxzn += '    table = arr_info_list_to_table(info_list)\n'
    pjhl__uxzn += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    pjhl__uxzn += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    pjhl__uxzn += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    pjhl__uxzn += '    delete_table_decref_arrays(table)\n'
    pjhl__uxzn += '    ev.finalize()\n'
    pjhl__uxzn += '    return sort_idx, group_labels, ngroups\n'
    whswf__nkuf = {}
    exec(pjhl__uxzn, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, whswf__nkuf)
    algpq__fuq = whswf__nkuf['impl']
    return algpq__fuq


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    znc__ilgq = len(labels)
    pfrd__focqk = np.zeros(ngroups, dtype=np.int64)
    kyd__jbra = np.zeros(ngroups, dtype=np.int64)
    mpf__gbq = 0
    mvr__osgry = 0
    for xehsx__lvc in range(znc__ilgq):
        tte__pcomy = labels[xehsx__lvc]
        if tte__pcomy < 0:
            mpf__gbq += 1
        else:
            mvr__osgry += 1
            if xehsx__lvc == znc__ilgq - 1 or tte__pcomy != labels[
                xehsx__lvc + 1]:
                pfrd__focqk[tte__pcomy] = mpf__gbq
                kyd__jbra[tte__pcomy] = mpf__gbq + mvr__osgry
                mpf__gbq += mvr__osgry
                mvr__osgry = 0
    return pfrd__focqk, kyd__jbra


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    algpq__fuq, bgid__rshn = gen_shuffle_dataframe(df, keys, _is_parallel)
    return algpq__fuq


def gen_shuffle_dataframe(df, keys, _is_parallel):
    axmqh__gjbs = len(df.columns)
    yxnoh__ssby = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    pjhl__uxzn = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        pjhl__uxzn += '  return df, keys, get_null_shuffle_info()\n'
        whswf__nkuf = {}
        exec(pjhl__uxzn, {'get_null_shuffle_info': get_null_shuffle_info},
            whswf__nkuf)
        algpq__fuq = whswf__nkuf['impl']
        return algpq__fuq
    for xehsx__lvc in range(axmqh__gjbs):
        pjhl__uxzn += f"""  in_arr{xehsx__lvc} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {xehsx__lvc})
"""
    pjhl__uxzn += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    pjhl__uxzn += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{xehsx__lvc}])' for xehsx__lvc in range(
        yxnoh__ssby)), ', '.join(f'array_to_info(in_arr{xehsx__lvc})' for
        xehsx__lvc in range(axmqh__gjbs)), 'array_to_info(in_index_arr)')
    pjhl__uxzn += '  table = arr_info_list_to_table(info_list)\n'
    pjhl__uxzn += (
        f'  out_table = shuffle_table(table, {yxnoh__ssby}, _is_parallel, 1)\n'
        )
    for xehsx__lvc in range(yxnoh__ssby):
        pjhl__uxzn += f"""  out_key{xehsx__lvc} = info_to_array(info_from_table(out_table, {xehsx__lvc}), keys{xehsx__lvc}_typ)
"""
    for xehsx__lvc in range(axmqh__gjbs):
        pjhl__uxzn += f"""  out_arr{xehsx__lvc} = info_to_array(info_from_table(out_table, {xehsx__lvc + yxnoh__ssby}), in_arr{xehsx__lvc}_typ)
"""
    pjhl__uxzn += f"""  out_arr_index = info_to_array(info_from_table(out_table, {yxnoh__ssby + axmqh__gjbs}), ind_arr_typ)
"""
    pjhl__uxzn += '  shuffle_info = get_shuffle_info(out_table)\n'
    pjhl__uxzn += '  delete_table(out_table)\n'
    pjhl__uxzn += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{xehsx__lvc}' for xehsx__lvc in range(
        axmqh__gjbs))
    pjhl__uxzn += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    pjhl__uxzn += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    pjhl__uxzn += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{xehsx__lvc}' for xehsx__lvc in range(yxnoh__ssby)))
    rjin__piz = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    rjin__piz.update({f'keys{xehsx__lvc}_typ': keys.types[xehsx__lvc] for
        xehsx__lvc in range(yxnoh__ssby)})
    rjin__piz.update({f'in_arr{xehsx__lvc}_typ': df.data[xehsx__lvc] for
        xehsx__lvc in range(axmqh__gjbs)})
    whswf__nkuf = {}
    exec(pjhl__uxzn, rjin__piz, whswf__nkuf)
    algpq__fuq = whswf__nkuf['impl']
    return algpq__fuq, rjin__piz


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        xhmn__qdzy = len(data.array_types)
        pjhl__uxzn = 'def impl(data, shuffle_info):\n'
        pjhl__uxzn += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{xehsx__lvc}])' for xehsx__lvc in
            range(xhmn__qdzy)))
        pjhl__uxzn += '  table = arr_info_list_to_table(info_list)\n'
        pjhl__uxzn += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for xehsx__lvc in range(xhmn__qdzy):
            pjhl__uxzn += f"""  out_arr{xehsx__lvc} = info_to_array(info_from_table(out_table, {xehsx__lvc}), data._data[{xehsx__lvc}])
"""
        pjhl__uxzn += '  delete_table(out_table)\n'
        pjhl__uxzn += '  delete_table(table)\n'
        pjhl__uxzn += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{xehsx__lvc}' for xehsx__lvc in range
            (xhmn__qdzy))))
        whswf__nkuf = {}
        exec(pjhl__uxzn, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, whswf__nkuf)
        algpq__fuq = whswf__nkuf['impl']
        return algpq__fuq
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ujb__wfx = bodo.utils.conversion.index_to_array(data)
            mycuw__pvrdg = reverse_shuffle(ujb__wfx, shuffle_info)
            return bodo.utils.conversion.index_from_array(mycuw__pvrdg)
        return impl_index

    def impl_arr(data, shuffle_info):
        inmz__kcwt = [array_to_info(data)]
        bwoks__uuf = arr_info_list_to_table(inmz__kcwt)
        rdmo__wgl = reverse_shuffle_table(bwoks__uuf, shuffle_info)
        mycuw__pvrdg = info_to_array(info_from_table(rdmo__wgl, 0), data)
        delete_table(rdmo__wgl)
        delete_table(bwoks__uuf)
        return mycuw__pvrdg
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    hfswj__wng = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    mjya__ipfn = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', hfswj__wng, mjya__ipfn,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    vzn__wqyp = get_overload_const_bool(ascending)
    umxph__dzjyi = grp.selection[0]
    pjhl__uxzn = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    gta__tekzf = (
        f"lambda S: S.value_counts(ascending={vzn__wqyp}, _index_name='{umxph__dzjyi}')"
        )
    pjhl__uxzn += f'    return grp.apply({gta__tekzf})\n'
    whswf__nkuf = {}
    exec(pjhl__uxzn, {'bodo': bodo}, whswf__nkuf)
    algpq__fuq = whswf__nkuf['impl']
    return algpq__fuq


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
    for oqr__sbfjl in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, oqr__sbfjl, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{oqr__sbfjl}'))
    for oqr__sbfjl in groupby_unsupported:
        overload_method(DataFrameGroupByType, oqr__sbfjl, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{oqr__sbfjl}'))
    for oqr__sbfjl in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, oqr__sbfjl, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{oqr__sbfjl}'))
    for oqr__sbfjl in series_only_unsupported:
        overload_method(DataFrameGroupByType, oqr__sbfjl, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{oqr__sbfjl}'))
    for oqr__sbfjl in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, oqr__sbfjl, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{oqr__sbfjl}'))


_install_groupby_unsupported()
