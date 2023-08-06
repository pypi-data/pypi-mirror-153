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
        nvale__sfao = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, nvale__sfao)


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
        jmf__fzekd = args[0]
        ygqa__dqd = signature.return_type
        noa__arcjt = cgutils.create_struct_proxy(ygqa__dqd)(context, builder)
        noa__arcjt.obj = jmf__fzekd
        context.nrt.incref(builder, signature.args[0], jmf__fzekd)
        return noa__arcjt._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for voo__ylrtl in keys:
        selection.remove(voo__ylrtl)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    ygqa__dqd = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return ygqa__dqd(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, vcqb__agk = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(vcqb__agk, (tuple, list)):
                if len(set(vcqb__agk).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(vcqb__agk).difference(set(grpby.df_type
                        .columns))))
                selection = vcqb__agk
            else:
                if vcqb__agk not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(vcqb__agk))
                selection = vcqb__agk,
                series_select = True
            rapfs__ycw = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(rapfs__ycw, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, vcqb__agk = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            vcqb__agk):
            rapfs__ycw = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(vcqb__agk)), {}).return_type
            return signature(rapfs__ycw, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    oar__vdb = arr_type == ArrayItemArrayType(string_array_type)
    nvrj__tyxt = arr_type.dtype
    if isinstance(nvrj__tyxt, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {nvrj__tyxt} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(nvrj__tyxt, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {nvrj__tyxt} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(nvrj__tyxt,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(nvrj__tyxt, (types.Integer, types.Float, types.Boolean)):
        if oar__vdb or nvrj__tyxt == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(nvrj__tyxt, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not nvrj__tyxt.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {nvrj__tyxt} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(nvrj__tyxt, types.Boolean) and func_name in {'cumsum',
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
    nvrj__tyxt = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(nvrj__tyxt, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(nvrj__tyxt, types.Integer):
            return IntDtype(nvrj__tyxt)
        return nvrj__tyxt
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        doxh__ygjim = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{doxh__ygjim}'."
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
    for voo__ylrtl in grp.keys:
        if multi_level_names:
            vktpk__qaa = voo__ylrtl, ''
        else:
            vktpk__qaa = voo__ylrtl
        dud__vfrwh = grp.df_type.columns.index(voo__ylrtl)
        data = to_str_arr_if_dict_array(grp.df_type.data[dud__vfrwh])
        out_columns.append(vktpk__qaa)
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
        gvdzl__oqaa = tuple(grp.df_type.column_index[grp.keys[bswi__gaeoh]] for
            bswi__gaeoh in range(len(grp.keys)))
        tar__rxa = tuple(grp.df_type.data[dud__vfrwh] for dud__vfrwh in
            gvdzl__oqaa)
        tar__rxa = tuple(to_str_arr_if_dict_array(vtkv__gknfb) for
            vtkv__gknfb in tar__rxa)
        index = MultiIndexType(tar__rxa, tuple(types.StringLiteral(
            voo__ylrtl) for voo__ylrtl in grp.keys))
    else:
        dud__vfrwh = grp.df_type.column_index[grp.keys[0]]
        hxgvg__thmb = to_str_arr_if_dict_array(grp.df_type.data[dud__vfrwh])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(hxgvg__thmb,
            types.StringLiteral(grp.keys[0]))
    eonaj__tydap = {}
    zmqpc__iveua = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        eonaj__tydap[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for vprks__ztuu in columns:
            dud__vfrwh = grp.df_type.column_index[vprks__ztuu]
            data = grp.df_type.data[dud__vfrwh]
            data = to_str_arr_if_dict_array(data)
            fbe__vfw = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                fbe__vfw = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    skv__nlw = SeriesType(data.dtype, data, None, string_type)
                    dgn__apphw = get_const_func_output_type(func, (skv__nlw
                        ,), {}, typing_context, target_context)
                    if dgn__apphw != ArrayItemArrayType(string_array_type):
                        dgn__apphw = dtype_to_array_type(dgn__apphw)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=vprks__ztuu, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    idcuf__iamk = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    zpu__jlt = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    npwjf__rhs = dict(numeric_only=idcuf__iamk, min_count=
                        zpu__jlt)
                    sbaho__regq = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        npwjf__rhs, sbaho__regq, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    idcuf__iamk = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    zpu__jlt = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    npwjf__rhs = dict(numeric_only=idcuf__iamk, min_count=
                        zpu__jlt)
                    sbaho__regq = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        npwjf__rhs, sbaho__regq, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    idcuf__iamk = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    npwjf__rhs = dict(numeric_only=idcuf__iamk)
                    sbaho__regq = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        npwjf__rhs, sbaho__regq, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    jlf__etzlx = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    mwdt__xtw = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    npwjf__rhs = dict(axis=jlf__etzlx, skipna=mwdt__xtw)
                    sbaho__regq = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        npwjf__rhs, sbaho__regq, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    uzl__onjt = args[0] if len(args) > 0 else kws.pop('ddof', 1
                        )
                    npwjf__rhs = dict(ddof=uzl__onjt)
                    sbaho__regq = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        npwjf__rhs, sbaho__regq, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                dgn__apphw, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                sxw__bqp = to_str_arr_if_dict_array(dgn__apphw)
                out_data.append(sxw__bqp)
                out_columns.append(vprks__ztuu)
                if func_name == 'agg':
                    loprt__vdg = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    eonaj__tydap[vprks__ztuu, loprt__vdg] = vprks__ztuu
                else:
                    eonaj__tydap[vprks__ztuu, func_name] = vprks__ztuu
                out_column_type.append(fbe__vfw)
            else:
                zmqpc__iveua.append(err_msg)
    if func_name == 'sum':
        xia__udti = any([(hufl__npmpm == ColumnType.NumericalColumn.value) for
            hufl__npmpm in out_column_type])
        if xia__udti:
            out_data = [hufl__npmpm for hufl__npmpm, bmhn__wll in zip(
                out_data, out_column_type) if bmhn__wll != ColumnType.
                NonNumericalColumn.value]
            out_columns = [hufl__npmpm for hufl__npmpm, bmhn__wll in zip(
                out_columns, out_column_type) if bmhn__wll != ColumnType.
                NonNumericalColumn.value]
            eonaj__tydap = {}
            for vprks__ztuu in out_columns:
                if grp.as_index is False and vprks__ztuu in grp.keys:
                    continue
                eonaj__tydap[vprks__ztuu, func_name] = vprks__ztuu
    cjur__cqzn = len(zmqpc__iveua)
    if len(out_data) == 0:
        if cjur__cqzn == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(cjur__cqzn, ' was' if cjur__cqzn == 1 else 's were',
                ','.join(zmqpc__iveua)))
    dqab__magi = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            eub__luwl = IntDtype(out_data[0].dtype)
        else:
            eub__luwl = out_data[0].dtype
        vnf__trs = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        dqab__magi = SeriesType(eub__luwl, index=index, name_typ=vnf__trs)
    return signature(dqab__magi, *args), eonaj__tydap


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    xabgi__gsf = True
    if isinstance(f_val, str):
        xabgi__gsf = False
        ohv__unae = f_val
    elif is_overload_constant_str(f_val):
        xabgi__gsf = False
        ohv__unae = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        xabgi__gsf = False
        ohv__unae = bodo.utils.typing.get_builtin_function_name(f_val)
    if not xabgi__gsf:
        if ohv__unae not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {ohv__unae}')
        rapfs__ycw = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(rapfs__ycw, (), ohv__unae, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            lcft__fla = types.functions.MakeFunctionLiteral(f_val)
        else:
            lcft__fla = f_val
        validate_udf('agg', lcft__fla)
        func = get_overload_const_func(lcft__fla, None)
        raz__mhb = func.code if hasattr(func, 'code') else func.__code__
        ohv__unae = raz__mhb.co_name
        rapfs__ycw = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(rapfs__ycw, (), 'agg', typing_context,
            target_context, lcft__fla)[0].return_type
    return ohv__unae, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    kqgu__rszt = kws and all(isinstance(lfc__knqvt, types.Tuple) and len(
        lfc__knqvt) == 2 for lfc__knqvt in kws.values())
    if is_overload_none(func) and not kqgu__rszt:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not kqgu__rszt:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    jzbc__kxh = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if kqgu__rszt or is_overload_constant_dict(func):
        if kqgu__rszt:
            ngwps__molju = [get_literal_value(bowz__afub) for bowz__afub,
                rgpig__uofef in kws.values()]
            gpma__jico = [get_literal_value(gfcbd__hqk) for rgpig__uofef,
                gfcbd__hqk in kws.values()]
        else:
            kkjdc__robox = get_overload_constant_dict(func)
            ngwps__molju = tuple(kkjdc__robox.keys())
            gpma__jico = tuple(kkjdc__robox.values())
        if 'head' in gpma__jico:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(vprks__ztuu not in grp.selection and vprks__ztuu not in grp.
            keys for vprks__ztuu in ngwps__molju):
            raise_bodo_error(
                f'Selected column names {ngwps__molju} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            gpma__jico)
        if kqgu__rszt and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        eonaj__tydap = {}
        out_columns = []
        out_data = []
        out_column_type = []
        kphz__xsbe = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for gbfee__dck, f_val in zip(ngwps__molju, gpma__jico):
            if isinstance(f_val, (tuple, list)):
                oxy__uou = 0
                for lcft__fla in f_val:
                    ohv__unae, out_tp = get_agg_funcname_and_outtyp(grp,
                        gbfee__dck, lcft__fla, typing_context, target_context)
                    jzbc__kxh = ohv__unae in list_cumulative
                    if ohv__unae == '<lambda>' and len(f_val) > 1:
                        ohv__unae = '<lambda_' + str(oxy__uou) + '>'
                        oxy__uou += 1
                    out_columns.append((gbfee__dck, ohv__unae))
                    eonaj__tydap[gbfee__dck, ohv__unae] = gbfee__dck, ohv__unae
                    _append_out_type(grp, out_data, out_tp)
            else:
                ohv__unae, out_tp = get_agg_funcname_and_outtyp(grp,
                    gbfee__dck, f_val, typing_context, target_context)
                jzbc__kxh = ohv__unae in list_cumulative
                if multi_level_names:
                    out_columns.append((gbfee__dck, ohv__unae))
                    eonaj__tydap[gbfee__dck, ohv__unae] = gbfee__dck, ohv__unae
                elif not kqgu__rszt:
                    out_columns.append(gbfee__dck)
                    eonaj__tydap[gbfee__dck, ohv__unae] = gbfee__dck
                elif kqgu__rszt:
                    kphz__xsbe.append(ohv__unae)
                _append_out_type(grp, out_data, out_tp)
        if kqgu__rszt:
            for bswi__gaeoh, ijgw__drbyq in enumerate(kws.keys()):
                out_columns.append(ijgw__drbyq)
                eonaj__tydap[ngwps__molju[bswi__gaeoh], kphz__xsbe[bswi__gaeoh]
                    ] = ijgw__drbyq
        if jzbc__kxh:
            index = grp.df_type.index
        else:
            index = out_tp.index
        dqab__magi = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(dqab__magi, *args), eonaj__tydap
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            rvaqu__pdyo = get_overload_const_list(func)
        else:
            rvaqu__pdyo = func.types
        if len(rvaqu__pdyo) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        oxy__uou = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        eonaj__tydap = {}
        qjj__eeryp = grp.selection[0]
        for f_val in rvaqu__pdyo:
            ohv__unae, out_tp = get_agg_funcname_and_outtyp(grp, qjj__eeryp,
                f_val, typing_context, target_context)
            jzbc__kxh = ohv__unae in list_cumulative
            if ohv__unae == '<lambda>' and len(rvaqu__pdyo) > 1:
                ohv__unae = '<lambda_' + str(oxy__uou) + '>'
                oxy__uou += 1
            out_columns.append(ohv__unae)
            eonaj__tydap[qjj__eeryp, ohv__unae] = ohv__unae
            _append_out_type(grp, out_data, out_tp)
        if jzbc__kxh:
            index = grp.df_type.index
        else:
            index = out_tp.index
        dqab__magi = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(dqab__magi, *args), eonaj__tydap
    ohv__unae = ''
    if types.unliteral(func) == types.unicode_type:
        ohv__unae = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        ohv__unae = bodo.utils.typing.get_builtin_function_name(func)
    if ohv__unae:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, ohv__unae, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        jlf__etzlx = args[0] if len(args) > 0 else kws.pop('axis', 0)
        idcuf__iamk = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        mwdt__xtw = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        npwjf__rhs = dict(axis=jlf__etzlx, numeric_only=idcuf__iamk)
        sbaho__regq = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', npwjf__rhs,
            sbaho__regq, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        sbxxp__dnf = args[0] if len(args) > 0 else kws.pop('periods', 1)
        hleb__ivwd = args[1] if len(args) > 1 else kws.pop('freq', None)
        jlf__etzlx = args[2] if len(args) > 2 else kws.pop('axis', 0)
        oyi__pjx = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        npwjf__rhs = dict(freq=hleb__ivwd, axis=jlf__etzlx, fill_value=oyi__pjx
            )
        sbaho__regq = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', npwjf__rhs,
            sbaho__regq, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        nanju__rmdes = args[0] if len(args) > 0 else kws.pop('func', None)
        tkmba__pnea = kws.pop('engine', None)
        tshxw__mpqk = kws.pop('engine_kwargs', None)
        npwjf__rhs = dict(engine=tkmba__pnea, engine_kwargs=tshxw__mpqk)
        sbaho__regq = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', npwjf__rhs,
            sbaho__regq, package_name='pandas', module_name='GroupBy')
    eonaj__tydap = {}
    for vprks__ztuu in grp.selection:
        out_columns.append(vprks__ztuu)
        eonaj__tydap[vprks__ztuu, name_operation] = vprks__ztuu
        dud__vfrwh = grp.df_type.columns.index(vprks__ztuu)
        data = grp.df_type.data[dud__vfrwh]
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
            dgn__apphw, err_msg = get_groupby_output_dtype(data,
                get_literal_value(nanju__rmdes), grp.df_type.index)
            if err_msg == 'ok':
                data = dgn__apphw
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    dqab__magi = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        dqab__magi = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(dqab__magi, *args), eonaj__tydap


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
        jnhok__yeey = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        yxvbw__eey = isinstance(jnhok__yeey, (SeriesType,
            HeterogeneousSeriesType)
            ) and jnhok__yeey.const_info is not None or not isinstance(
            jnhok__yeey, (SeriesType, DataFrameType))
        if yxvbw__eey:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                rfp__bkhsu = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                gvdzl__oqaa = tuple(grp.df_type.columns.index(grp.keys[
                    bswi__gaeoh]) for bswi__gaeoh in range(len(grp.keys)))
                tar__rxa = tuple(grp.df_type.data[dud__vfrwh] for
                    dud__vfrwh in gvdzl__oqaa)
                tar__rxa = tuple(to_str_arr_if_dict_array(vtkv__gknfb) for
                    vtkv__gknfb in tar__rxa)
                rfp__bkhsu = MultiIndexType(tar__rxa, tuple(types.literal(
                    voo__ylrtl) for voo__ylrtl in grp.keys))
            else:
                dud__vfrwh = grp.df_type.columns.index(grp.keys[0])
                hxgvg__thmb = grp.df_type.data[dud__vfrwh]
                hxgvg__thmb = to_str_arr_if_dict_array(hxgvg__thmb)
                rfp__bkhsu = bodo.hiframes.pd_index_ext.array_type_to_index(
                    hxgvg__thmb, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            tte__uwf = tuple(grp.df_type.data[grp.df_type.columns.index(
                vprks__ztuu)] for vprks__ztuu in grp.keys)
            tte__uwf = tuple(to_str_arr_if_dict_array(vtkv__gknfb) for
                vtkv__gknfb in tte__uwf)
            ovkzx__itafb = tuple(types.literal(lfc__knqvt) for lfc__knqvt in
                grp.keys) + get_index_name_types(jnhok__yeey.index)
            if not grp.as_index:
                tte__uwf = types.Array(types.int64, 1, 'C'),
                ovkzx__itafb = (types.none,) + get_index_name_types(jnhok__yeey
                    .index)
            rfp__bkhsu = MultiIndexType(tte__uwf + get_index_data_arr_types
                (jnhok__yeey.index), ovkzx__itafb)
        if yxvbw__eey:
            if isinstance(jnhok__yeey, HeterogeneousSeriesType):
                rgpig__uofef, pgl__sxt = jnhok__yeey.const_info
                if isinstance(jnhok__yeey.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    alccv__tky = jnhok__yeey.data.tuple_typ.types
                elif isinstance(jnhok__yeey.data, types.Tuple):
                    alccv__tky = jnhok__yeey.data.types
                bai__uke = tuple(to_nullable_type(dtype_to_array_type(
                    vtkv__gknfb)) for vtkv__gknfb in alccv__tky)
                ogzcm__bric = DataFrameType(out_data + bai__uke, rfp__bkhsu,
                    out_columns + pgl__sxt)
            elif isinstance(jnhok__yeey, SeriesType):
                qry__zuv, pgl__sxt = jnhok__yeey.const_info
                bai__uke = tuple(to_nullable_type(dtype_to_array_type(
                    jnhok__yeey.dtype)) for rgpig__uofef in range(qry__zuv))
                ogzcm__bric = DataFrameType(out_data + bai__uke, rfp__bkhsu,
                    out_columns + pgl__sxt)
            else:
                hmw__uax = get_udf_out_arr_type(jnhok__yeey)
                if not grp.as_index:
                    ogzcm__bric = DataFrameType(out_data + (hmw__uax,),
                        rfp__bkhsu, out_columns + ('',))
                else:
                    ogzcm__bric = SeriesType(hmw__uax.dtype, hmw__uax,
                        rfp__bkhsu, None)
        elif isinstance(jnhok__yeey, SeriesType):
            ogzcm__bric = SeriesType(jnhok__yeey.dtype, jnhok__yeey.data,
                rfp__bkhsu, jnhok__yeey.name_typ)
        else:
            ogzcm__bric = DataFrameType(jnhok__yeey.data, rfp__bkhsu,
                jnhok__yeey.columns)
        pcu__nhesr = gen_apply_pysig(len(f_args), kws.keys())
        obmvo__oqm = (func, *f_args) + tuple(kws.values())
        return signature(ogzcm__bric, *obmvo__oqm).replace(pysig=pcu__nhesr)

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
    jgb__uzvez = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            gbfee__dck = grp.selection[0]
            hmw__uax = jgb__uzvez.data[jgb__uzvez.columns.index(gbfee__dck)]
            hmw__uax = to_str_arr_if_dict_array(hmw__uax)
            nea__xtj = SeriesType(hmw__uax.dtype, hmw__uax, jgb__uzvez.
                index, types.literal(gbfee__dck))
        else:
            fuzaq__agsme = tuple(jgb__uzvez.data[jgb__uzvez.columns.index(
                vprks__ztuu)] for vprks__ztuu in grp.selection)
            fuzaq__agsme = tuple(to_str_arr_if_dict_array(vtkv__gknfb) for
                vtkv__gknfb in fuzaq__agsme)
            nea__xtj = DataFrameType(fuzaq__agsme, jgb__uzvez.index, tuple(
                grp.selection))
    else:
        nea__xtj = jgb__uzvez
    ewzmi__icnk = nea__xtj,
    ewzmi__icnk += tuple(f_args)
    try:
        jnhok__yeey = get_const_func_output_type(func, ewzmi__icnk, kws,
            typing_context, target_context)
    except Exception as mgud__ggqb:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', mgud__ggqb),
            getattr(mgud__ggqb, 'loc', None))
    return jnhok__yeey


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    ewzmi__icnk = (grp,) + f_args
    try:
        jnhok__yeey = get_const_func_output_type(func, ewzmi__icnk, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as mgud__ggqb:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', mgud__ggqb
            ), getattr(mgud__ggqb, 'loc', None))
    pcu__nhesr = gen_apply_pysig(len(f_args), kws.keys())
    obmvo__oqm = (func, *f_args) + tuple(kws.values())
    return signature(jnhok__yeey, *obmvo__oqm).replace(pysig=pcu__nhesr)


def gen_apply_pysig(n_args, kws):
    iktrs__okjw = ', '.join(f'arg{bswi__gaeoh}' for bswi__gaeoh in range(
        n_args))
    iktrs__okjw = iktrs__okjw + ', ' if iktrs__okjw else ''
    ujp__dntc = ', '.join(f"{gqa__jaf} = ''" for gqa__jaf in kws)
    bfqq__ephe = f'def apply_stub(func, {iktrs__okjw}{ujp__dntc}):\n'
    bfqq__ephe += '    pass\n'
    pqk__mih = {}
    exec(bfqq__ephe, {}, pqk__mih)
    sfj__kle = pqk__mih['apply_stub']
    return numba.core.utils.pysignature(sfj__kle)


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
        dgn__apphw = get_pivot_output_dtype(data, aggfunc.literal_value)
        iflff__mza = dtype_to_array_type(dgn__apphw)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/api_docs/pandas/dataframe/#pddataframepivot.'
                )
        nwtm__ldehj = _pivot_values.meta
        dmok__ooqoc = len(nwtm__ldehj)
        dud__vfrwh = df.columns.index(index)
        hxgvg__thmb = df.data[dud__vfrwh]
        hxgvg__thmb = to_str_arr_if_dict_array(hxgvg__thmb)
        tcc__wtrz = bodo.hiframes.pd_index_ext.array_type_to_index(hxgvg__thmb,
            types.StringLiteral(index))
        awib__wox = DataFrameType((iflff__mza,) * dmok__ooqoc, tcc__wtrz,
            tuple(nwtm__ldehj))
        return signature(awib__wox, *args)


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
        iflff__mza = types.Array(types.int64, 1, 'C')
        nwtm__ldehj = _pivot_values.meta
        dmok__ooqoc = len(nwtm__ldehj)
        tcc__wtrz = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        awib__wox = DataFrameType((iflff__mza,) * dmok__ooqoc, tcc__wtrz,
            tuple(nwtm__ldehj))
        return signature(awib__wox, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    bfqq__ephe = 'def impl(keys, dropna, _is_parallel):\n'
    bfqq__ephe += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    bfqq__ephe += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{bswi__gaeoh}])' for bswi__gaeoh in range(len(
        keys.types))))
    bfqq__ephe += '    table = arr_info_list_to_table(info_list)\n'
    bfqq__ephe += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    bfqq__ephe += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    bfqq__ephe += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    bfqq__ephe += '    delete_table_decref_arrays(table)\n'
    bfqq__ephe += '    ev.finalize()\n'
    bfqq__ephe += '    return sort_idx, group_labels, ngroups\n'
    pqk__mih = {}
    exec(bfqq__ephe, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, pqk__mih)
    ccy__ukv = pqk__mih['impl']
    return ccy__ukv


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    ggp__vkkgo = len(labels)
    tooyk__zngjc = np.zeros(ngroups, dtype=np.int64)
    xuhl__iepan = np.zeros(ngroups, dtype=np.int64)
    dab__uzqzd = 0
    kouw__sre = 0
    for bswi__gaeoh in range(ggp__vkkgo):
        nnpg__hoix = labels[bswi__gaeoh]
        if nnpg__hoix < 0:
            dab__uzqzd += 1
        else:
            kouw__sre += 1
            if bswi__gaeoh == ggp__vkkgo - 1 or nnpg__hoix != labels[
                bswi__gaeoh + 1]:
                tooyk__zngjc[nnpg__hoix] = dab__uzqzd
                xuhl__iepan[nnpg__hoix] = dab__uzqzd + kouw__sre
                dab__uzqzd += kouw__sre
                kouw__sre = 0
    return tooyk__zngjc, xuhl__iepan


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ccy__ukv, rgpig__uofef = gen_shuffle_dataframe(df, keys, _is_parallel)
    return ccy__ukv


def gen_shuffle_dataframe(df, keys, _is_parallel):
    qry__zuv = len(df.columns)
    cab__wzen = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    bfqq__ephe = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        bfqq__ephe += '  return df, keys, get_null_shuffle_info()\n'
        pqk__mih = {}
        exec(bfqq__ephe, {'get_null_shuffle_info': get_null_shuffle_info},
            pqk__mih)
        ccy__ukv = pqk__mih['impl']
        return ccy__ukv
    for bswi__gaeoh in range(qry__zuv):
        bfqq__ephe += f"""  in_arr{bswi__gaeoh} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bswi__gaeoh})
"""
    bfqq__ephe += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    bfqq__ephe += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{bswi__gaeoh}])' for bswi__gaeoh in range(
        cab__wzen)), ', '.join(f'array_to_info(in_arr{bswi__gaeoh})' for
        bswi__gaeoh in range(qry__zuv)), 'array_to_info(in_index_arr)')
    bfqq__ephe += '  table = arr_info_list_to_table(info_list)\n'
    bfqq__ephe += (
        f'  out_table = shuffle_table(table, {cab__wzen}, _is_parallel, 1)\n')
    for bswi__gaeoh in range(cab__wzen):
        bfqq__ephe += f"""  out_key{bswi__gaeoh} = info_to_array(info_from_table(out_table, {bswi__gaeoh}), keys{bswi__gaeoh}_typ)
"""
    for bswi__gaeoh in range(qry__zuv):
        bfqq__ephe += f"""  out_arr{bswi__gaeoh} = info_to_array(info_from_table(out_table, {bswi__gaeoh + cab__wzen}), in_arr{bswi__gaeoh}_typ)
"""
    bfqq__ephe += f"""  out_arr_index = info_to_array(info_from_table(out_table, {cab__wzen + qry__zuv}), ind_arr_typ)
"""
    bfqq__ephe += '  shuffle_info = get_shuffle_info(out_table)\n'
    bfqq__ephe += '  delete_table(out_table)\n'
    bfqq__ephe += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{bswi__gaeoh}' for bswi__gaeoh in range(
        qry__zuv))
    bfqq__ephe += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    bfqq__ephe += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    bfqq__ephe += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{bswi__gaeoh}' for bswi__gaeoh in range(cab__wzen)))
    uxm__lth = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    uxm__lth.update({f'keys{bswi__gaeoh}_typ': keys.types[bswi__gaeoh] for
        bswi__gaeoh in range(cab__wzen)})
    uxm__lth.update({f'in_arr{bswi__gaeoh}_typ': df.data[bswi__gaeoh] for
        bswi__gaeoh in range(qry__zuv)})
    pqk__mih = {}
    exec(bfqq__ephe, uxm__lth, pqk__mih)
    ccy__ukv = pqk__mih['impl']
    return ccy__ukv, uxm__lth


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        nyj__wbyvs = len(data.array_types)
        bfqq__ephe = 'def impl(data, shuffle_info):\n'
        bfqq__ephe += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{bswi__gaeoh}])' for bswi__gaeoh in
            range(nyj__wbyvs)))
        bfqq__ephe += '  table = arr_info_list_to_table(info_list)\n'
        bfqq__ephe += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for bswi__gaeoh in range(nyj__wbyvs):
            bfqq__ephe += f"""  out_arr{bswi__gaeoh} = info_to_array(info_from_table(out_table, {bswi__gaeoh}), data._data[{bswi__gaeoh}])
"""
        bfqq__ephe += '  delete_table(out_table)\n'
        bfqq__ephe += '  delete_table(table)\n'
        bfqq__ephe += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{bswi__gaeoh}' for bswi__gaeoh in
            range(nyj__wbyvs))))
        pqk__mih = {}
        exec(bfqq__ephe, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, pqk__mih)
        ccy__ukv = pqk__mih['impl']
        return ccy__ukv
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            uwrm__tutob = bodo.utils.conversion.index_to_array(data)
            sxw__bqp = reverse_shuffle(uwrm__tutob, shuffle_info)
            return bodo.utils.conversion.index_from_array(sxw__bqp)
        return impl_index

    def impl_arr(data, shuffle_info):
        ypsx__inm = [array_to_info(data)]
        pqnbb__jjdvm = arr_info_list_to_table(ypsx__inm)
        crbb__sqjmz = reverse_shuffle_table(pqnbb__jjdvm, shuffle_info)
        sxw__bqp = info_to_array(info_from_table(crbb__sqjmz, 0), data)
        delete_table(crbb__sqjmz)
        delete_table(pqnbb__jjdvm)
        return sxw__bqp
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    npwjf__rhs = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    sbaho__regq = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', npwjf__rhs, sbaho__regq,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    vcr__prh = get_overload_const_bool(ascending)
    ear__iagz = grp.selection[0]
    bfqq__ephe = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    jpqmj__sns = (
        f"lambda S: S.value_counts(ascending={vcr__prh}, _index_name='{ear__iagz}')"
        )
    bfqq__ephe += f'    return grp.apply({jpqmj__sns})\n'
    pqk__mih = {}
    exec(bfqq__ephe, {'bodo': bodo}, pqk__mih)
    ccy__ukv = pqk__mih['impl']
    return ccy__ukv


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
    for rlt__zkf in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, rlt__zkf, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{rlt__zkf}'))
    for rlt__zkf in groupby_unsupported:
        overload_method(DataFrameGroupByType, rlt__zkf, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{rlt__zkf}'))
    for rlt__zkf in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, rlt__zkf, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{rlt__zkf}'))
    for rlt__zkf in series_only_unsupported:
        overload_method(DataFrameGroupByType, rlt__zkf, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{rlt__zkf}'))
    for rlt__zkf in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, rlt__zkf, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{rlt__zkf}'))


_install_groupby_unsupported()
