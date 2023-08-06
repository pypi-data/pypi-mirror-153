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
        bzskd__owna = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, bzskd__owna)


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
        ioj__dbw = args[0]
        vxpi__vhvr = signature.return_type
        uthz__jpya = cgutils.create_struct_proxy(vxpi__vhvr)(context, builder)
        uthz__jpya.obj = ioj__dbw
        context.nrt.incref(builder, signature.args[0], ioj__dbw)
        return uthz__jpya._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for ocub__qxtom in keys:
        selection.remove(ocub__qxtom)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    vxpi__vhvr = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return vxpi__vhvr(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, vfww__jeg = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(vfww__jeg, (tuple, list)):
                if len(set(vfww__jeg).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(vfww__jeg).difference(set(grpby.df_type
                        .columns))))
                selection = vfww__jeg
            else:
                if vfww__jeg not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(vfww__jeg))
                selection = vfww__jeg,
                series_select = True
            ionkp__qmfhu = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(ionkp__qmfhu, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, vfww__jeg = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            vfww__jeg):
            ionkp__qmfhu = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(vfww__jeg)), {}).return_type
            return signature(ionkp__qmfhu, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    wgm__xai = arr_type == ArrayItemArrayType(string_array_type)
    gpop__iwqof = arr_type.dtype
    if isinstance(gpop__iwqof, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {gpop__iwqof} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(gpop__iwqof, (
        Decimal128Type, types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {gpop__iwqof} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(gpop__iwqof
        , (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(gpop__iwqof, (types.Integer, types.Float, types.Boolean)
        ):
        if wgm__xai or gpop__iwqof == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(gpop__iwqof, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not gpop__iwqof.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {gpop__iwqof} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(gpop__iwqof, types.Boolean) and func_name in {'cumsum',
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
    gpop__iwqof = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(gpop__iwqof, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(gpop__iwqof, types.Integer):
            return IntDtype(gpop__iwqof)
        return gpop__iwqof
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        zcdlm__mmlf = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{zcdlm__mmlf}'."
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
    for ocub__qxtom in grp.keys:
        if multi_level_names:
            abme__xstec = ocub__qxtom, ''
        else:
            abme__xstec = ocub__qxtom
        wcr__fsl = grp.df_type.columns.index(ocub__qxtom)
        data = to_str_arr_if_dict_array(grp.df_type.data[wcr__fsl])
        out_columns.append(abme__xstec)
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
        fdwle__ozw = tuple(grp.df_type.column_index[grp.keys[yuq__jsf]] for
            yuq__jsf in range(len(grp.keys)))
        fxkbj__wziu = tuple(grp.df_type.data[wcr__fsl] for wcr__fsl in
            fdwle__ozw)
        fxkbj__wziu = tuple(to_str_arr_if_dict_array(zlk__dcwe) for
            zlk__dcwe in fxkbj__wziu)
        index = MultiIndexType(fxkbj__wziu, tuple(types.StringLiteral(
            ocub__qxtom) for ocub__qxtom in grp.keys))
    else:
        wcr__fsl = grp.df_type.column_index[grp.keys[0]]
        ndyxx__zhwda = to_str_arr_if_dict_array(grp.df_type.data[wcr__fsl])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(ndyxx__zhwda,
            types.StringLiteral(grp.keys[0]))
    dazc__mjaj = {}
    mmwgd__fdrlu = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        dazc__mjaj[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for tmu__dzlsn in columns:
            wcr__fsl = grp.df_type.column_index[tmu__dzlsn]
            data = grp.df_type.data[wcr__fsl]
            data = to_str_arr_if_dict_array(data)
            riq__olyl = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                riq__olyl = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    lrrkk__yao = SeriesType(data.dtype, data, None, string_type
                        )
                    xxec__tnwn = get_const_func_output_type(func, (
                        lrrkk__yao,), {}, typing_context, target_context)
                    if xxec__tnwn != ArrayItemArrayType(string_array_type):
                        xxec__tnwn = dtype_to_array_type(xxec__tnwn)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=tmu__dzlsn, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    qjx__tafrl = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    tdltf__yumwn = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    hni__xquh = dict(numeric_only=qjx__tafrl, min_count=
                        tdltf__yumwn)
                    mkpur__bgv = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hni__xquh, mkpur__bgv, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    qjx__tafrl = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    tdltf__yumwn = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    hni__xquh = dict(numeric_only=qjx__tafrl, min_count=
                        tdltf__yumwn)
                    mkpur__bgv = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hni__xquh, mkpur__bgv, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    qjx__tafrl = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    hni__xquh = dict(numeric_only=qjx__tafrl)
                    mkpur__bgv = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hni__xquh, mkpur__bgv, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    yju__gttbv = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    chp__lykv = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    hni__xquh = dict(axis=yju__gttbv, skipna=chp__lykv)
                    mkpur__bgv = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hni__xquh, mkpur__bgv, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    xpx__jkesh = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    hni__xquh = dict(ddof=xpx__jkesh)
                    mkpur__bgv = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hni__xquh, mkpur__bgv, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                xxec__tnwn, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                pkbrh__ymlma = to_str_arr_if_dict_array(xxec__tnwn)
                out_data.append(pkbrh__ymlma)
                out_columns.append(tmu__dzlsn)
                if func_name == 'agg':
                    ximtx__ogg = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    dazc__mjaj[tmu__dzlsn, ximtx__ogg] = tmu__dzlsn
                else:
                    dazc__mjaj[tmu__dzlsn, func_name] = tmu__dzlsn
                out_column_type.append(riq__olyl)
            else:
                mmwgd__fdrlu.append(err_msg)
    if func_name == 'sum':
        tev__fvbi = any([(wuxd__mxcup == ColumnType.NumericalColumn.value) for
            wuxd__mxcup in out_column_type])
        if tev__fvbi:
            out_data = [wuxd__mxcup for wuxd__mxcup, afzb__lsxl in zip(
                out_data, out_column_type) if afzb__lsxl != ColumnType.
                NonNumericalColumn.value]
            out_columns = [wuxd__mxcup for wuxd__mxcup, afzb__lsxl in zip(
                out_columns, out_column_type) if afzb__lsxl != ColumnType.
                NonNumericalColumn.value]
            dazc__mjaj = {}
            for tmu__dzlsn in out_columns:
                if grp.as_index is False and tmu__dzlsn in grp.keys:
                    continue
                dazc__mjaj[tmu__dzlsn, func_name] = tmu__dzlsn
    dzouz__xgw = len(mmwgd__fdrlu)
    if len(out_data) == 0:
        if dzouz__xgw == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(dzouz__xgw, ' was' if dzouz__xgw == 1 else 's were',
                ','.join(mmwgd__fdrlu)))
    gyj__dnr = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            upthw__wza = IntDtype(out_data[0].dtype)
        else:
            upthw__wza = out_data[0].dtype
        ektw__xju = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        gyj__dnr = SeriesType(upthw__wza, index=index, name_typ=ektw__xju)
    return signature(gyj__dnr, *args), dazc__mjaj


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    mprpk__anjl = True
    if isinstance(f_val, str):
        mprpk__anjl = False
        rayku__gkl = f_val
    elif is_overload_constant_str(f_val):
        mprpk__anjl = False
        rayku__gkl = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        mprpk__anjl = False
        rayku__gkl = bodo.utils.typing.get_builtin_function_name(f_val)
    if not mprpk__anjl:
        if rayku__gkl not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {rayku__gkl}')
        ionkp__qmfhu = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(ionkp__qmfhu, (), rayku__gkl, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            weafo__xpxjq = types.functions.MakeFunctionLiteral(f_val)
        else:
            weafo__xpxjq = f_val
        validate_udf('agg', weafo__xpxjq)
        func = get_overload_const_func(weafo__xpxjq, None)
        juxi__oleul = func.code if hasattr(func, 'code') else func.__code__
        rayku__gkl = juxi__oleul.co_name
        ionkp__qmfhu = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(ionkp__qmfhu, (), 'agg', typing_context,
            target_context, weafo__xpxjq)[0].return_type
    return rayku__gkl, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    ife__dure = kws and all(isinstance(ulxtm__prqij, types.Tuple) and len(
        ulxtm__prqij) == 2 for ulxtm__prqij in kws.values())
    if is_overload_none(func) and not ife__dure:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not ife__dure:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    fibsj__bijkv = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if ife__dure or is_overload_constant_dict(func):
        if ife__dure:
            qxifa__xzt = [get_literal_value(nmsl__bgj) for nmsl__bgj,
                gexil__vni in kws.values()]
            ndpxf__tpmlf = [get_literal_value(fdk__lqh) for gexil__vni,
                fdk__lqh in kws.values()]
        else:
            nepwo__wzn = get_overload_constant_dict(func)
            qxifa__xzt = tuple(nepwo__wzn.keys())
            ndpxf__tpmlf = tuple(nepwo__wzn.values())
        if 'head' in ndpxf__tpmlf:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(tmu__dzlsn not in grp.selection and tmu__dzlsn not in grp.
            keys for tmu__dzlsn in qxifa__xzt):
            raise_bodo_error(
                f'Selected column names {qxifa__xzt} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            ndpxf__tpmlf)
        if ife__dure and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        dazc__mjaj = {}
        out_columns = []
        out_data = []
        out_column_type = []
        tiz__uimay = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for qsczw__mofbw, f_val in zip(qxifa__xzt, ndpxf__tpmlf):
            if isinstance(f_val, (tuple, list)):
                ekfb__znhc = 0
                for weafo__xpxjq in f_val:
                    rayku__gkl, out_tp = get_agg_funcname_and_outtyp(grp,
                        qsczw__mofbw, weafo__xpxjq, typing_context,
                        target_context)
                    fibsj__bijkv = rayku__gkl in list_cumulative
                    if rayku__gkl == '<lambda>' and len(f_val) > 1:
                        rayku__gkl = '<lambda_' + str(ekfb__znhc) + '>'
                        ekfb__znhc += 1
                    out_columns.append((qsczw__mofbw, rayku__gkl))
                    dazc__mjaj[qsczw__mofbw, rayku__gkl
                        ] = qsczw__mofbw, rayku__gkl
                    _append_out_type(grp, out_data, out_tp)
            else:
                rayku__gkl, out_tp = get_agg_funcname_and_outtyp(grp,
                    qsczw__mofbw, f_val, typing_context, target_context)
                fibsj__bijkv = rayku__gkl in list_cumulative
                if multi_level_names:
                    out_columns.append((qsczw__mofbw, rayku__gkl))
                    dazc__mjaj[qsczw__mofbw, rayku__gkl
                        ] = qsczw__mofbw, rayku__gkl
                elif not ife__dure:
                    out_columns.append(qsczw__mofbw)
                    dazc__mjaj[qsczw__mofbw, rayku__gkl] = qsczw__mofbw
                elif ife__dure:
                    tiz__uimay.append(rayku__gkl)
                _append_out_type(grp, out_data, out_tp)
        if ife__dure:
            for yuq__jsf, tcg__odi in enumerate(kws.keys()):
                out_columns.append(tcg__odi)
                dazc__mjaj[qxifa__xzt[yuq__jsf], tiz__uimay[yuq__jsf]
                    ] = tcg__odi
        if fibsj__bijkv:
            index = grp.df_type.index
        else:
            index = out_tp.index
        gyj__dnr = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(gyj__dnr, *args), dazc__mjaj
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            vzke__ynzs = get_overload_const_list(func)
        else:
            vzke__ynzs = func.types
        if len(vzke__ynzs) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        ekfb__znhc = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        dazc__mjaj = {}
        xvtru__dfke = grp.selection[0]
        for f_val in vzke__ynzs:
            rayku__gkl, out_tp = get_agg_funcname_and_outtyp(grp,
                xvtru__dfke, f_val, typing_context, target_context)
            fibsj__bijkv = rayku__gkl in list_cumulative
            if rayku__gkl == '<lambda>' and len(vzke__ynzs) > 1:
                rayku__gkl = '<lambda_' + str(ekfb__znhc) + '>'
                ekfb__znhc += 1
            out_columns.append(rayku__gkl)
            dazc__mjaj[xvtru__dfke, rayku__gkl] = rayku__gkl
            _append_out_type(grp, out_data, out_tp)
        if fibsj__bijkv:
            index = grp.df_type.index
        else:
            index = out_tp.index
        gyj__dnr = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(gyj__dnr, *args), dazc__mjaj
    rayku__gkl = ''
    if types.unliteral(func) == types.unicode_type:
        rayku__gkl = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        rayku__gkl = bodo.utils.typing.get_builtin_function_name(func)
    if rayku__gkl:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, rayku__gkl, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        yju__gttbv = args[0] if len(args) > 0 else kws.pop('axis', 0)
        qjx__tafrl = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        chp__lykv = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        hni__xquh = dict(axis=yju__gttbv, numeric_only=qjx__tafrl)
        mkpur__bgv = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', hni__xquh,
            mkpur__bgv, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        byvev__hqrl = args[0] if len(args) > 0 else kws.pop('periods', 1)
        shf__pgrn = args[1] if len(args) > 1 else kws.pop('freq', None)
        yju__gttbv = args[2] if len(args) > 2 else kws.pop('axis', 0)
        qfv__rhemp = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        hni__xquh = dict(freq=shf__pgrn, axis=yju__gttbv, fill_value=qfv__rhemp
            )
        mkpur__bgv = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', hni__xquh,
            mkpur__bgv, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        yhc__jndbu = args[0] if len(args) > 0 else kws.pop('func', None)
        nkek__icvfm = kws.pop('engine', None)
        krrt__mqtb = kws.pop('engine_kwargs', None)
        hni__xquh = dict(engine=nkek__icvfm, engine_kwargs=krrt__mqtb)
        mkpur__bgv = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', hni__xquh, mkpur__bgv,
            package_name='pandas', module_name='GroupBy')
    dazc__mjaj = {}
    for tmu__dzlsn in grp.selection:
        out_columns.append(tmu__dzlsn)
        dazc__mjaj[tmu__dzlsn, name_operation] = tmu__dzlsn
        wcr__fsl = grp.df_type.columns.index(tmu__dzlsn)
        data = grp.df_type.data[wcr__fsl]
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
            xxec__tnwn, err_msg = get_groupby_output_dtype(data,
                get_literal_value(yhc__jndbu), grp.df_type.index)
            if err_msg == 'ok':
                data = xxec__tnwn
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    gyj__dnr = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        gyj__dnr = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(gyj__dnr, *args), dazc__mjaj


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
        tni__nmmyh = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        sgfa__lvijo = isinstance(tni__nmmyh, (SeriesType,
            HeterogeneousSeriesType)
            ) and tni__nmmyh.const_info is not None or not isinstance(
            tni__nmmyh, (SeriesType, DataFrameType))
        if sgfa__lvijo:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                lno__vwnyw = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                fdwle__ozw = tuple(grp.df_type.columns.index(grp.keys[
                    yuq__jsf]) for yuq__jsf in range(len(grp.keys)))
                fxkbj__wziu = tuple(grp.df_type.data[wcr__fsl] for wcr__fsl in
                    fdwle__ozw)
                fxkbj__wziu = tuple(to_str_arr_if_dict_array(zlk__dcwe) for
                    zlk__dcwe in fxkbj__wziu)
                lno__vwnyw = MultiIndexType(fxkbj__wziu, tuple(types.
                    literal(ocub__qxtom) for ocub__qxtom in grp.keys))
            else:
                wcr__fsl = grp.df_type.columns.index(grp.keys[0])
                ndyxx__zhwda = grp.df_type.data[wcr__fsl]
                ndyxx__zhwda = to_str_arr_if_dict_array(ndyxx__zhwda)
                lno__vwnyw = bodo.hiframes.pd_index_ext.array_type_to_index(
                    ndyxx__zhwda, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            kxgm__nyu = tuple(grp.df_type.data[grp.df_type.columns.index(
                tmu__dzlsn)] for tmu__dzlsn in grp.keys)
            kxgm__nyu = tuple(to_str_arr_if_dict_array(zlk__dcwe) for
                zlk__dcwe in kxgm__nyu)
            ualh__bgabw = tuple(types.literal(ulxtm__prqij) for
                ulxtm__prqij in grp.keys) + get_index_name_types(tni__nmmyh
                .index)
            if not grp.as_index:
                kxgm__nyu = types.Array(types.int64, 1, 'C'),
                ualh__bgabw = (types.none,) + get_index_name_types(tni__nmmyh
                    .index)
            lno__vwnyw = MultiIndexType(kxgm__nyu +
                get_index_data_arr_types(tni__nmmyh.index), ualh__bgabw)
        if sgfa__lvijo:
            if isinstance(tni__nmmyh, HeterogeneousSeriesType):
                gexil__vni, gruv__wuum = tni__nmmyh.const_info
                if isinstance(tni__nmmyh.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    datu__edsrm = tni__nmmyh.data.tuple_typ.types
                elif isinstance(tni__nmmyh.data, types.Tuple):
                    datu__edsrm = tni__nmmyh.data.types
                salpe__evm = tuple(to_nullable_type(dtype_to_array_type(
                    zlk__dcwe)) for zlk__dcwe in datu__edsrm)
                gsgh__vyb = DataFrameType(out_data + salpe__evm, lno__vwnyw,
                    out_columns + gruv__wuum)
            elif isinstance(tni__nmmyh, SeriesType):
                hwfz__apkm, gruv__wuum = tni__nmmyh.const_info
                salpe__evm = tuple(to_nullable_type(dtype_to_array_type(
                    tni__nmmyh.dtype)) for gexil__vni in range(hwfz__apkm))
                gsgh__vyb = DataFrameType(out_data + salpe__evm, lno__vwnyw,
                    out_columns + gruv__wuum)
            else:
                uefpa__ejy = get_udf_out_arr_type(tni__nmmyh)
                if not grp.as_index:
                    gsgh__vyb = DataFrameType(out_data + (uefpa__ejy,),
                        lno__vwnyw, out_columns + ('',))
                else:
                    gsgh__vyb = SeriesType(uefpa__ejy.dtype, uefpa__ejy,
                        lno__vwnyw, None)
        elif isinstance(tni__nmmyh, SeriesType):
            gsgh__vyb = SeriesType(tni__nmmyh.dtype, tni__nmmyh.data,
                lno__vwnyw, tni__nmmyh.name_typ)
        else:
            gsgh__vyb = DataFrameType(tni__nmmyh.data, lno__vwnyw,
                tni__nmmyh.columns)
        qjg__cwnoz = gen_apply_pysig(len(f_args), kws.keys())
        srxl__yrryh = (func, *f_args) + tuple(kws.values())
        return signature(gsgh__vyb, *srxl__yrryh).replace(pysig=qjg__cwnoz)

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
    eopt__gah = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            qsczw__mofbw = grp.selection[0]
            uefpa__ejy = eopt__gah.data[eopt__gah.columns.index(qsczw__mofbw)]
            uefpa__ejy = to_str_arr_if_dict_array(uefpa__ejy)
            bdvm__fpcmk = SeriesType(uefpa__ejy.dtype, uefpa__ejy,
                eopt__gah.index, types.literal(qsczw__mofbw))
        else:
            qdegm__omfhx = tuple(eopt__gah.data[eopt__gah.columns.index(
                tmu__dzlsn)] for tmu__dzlsn in grp.selection)
            qdegm__omfhx = tuple(to_str_arr_if_dict_array(zlk__dcwe) for
                zlk__dcwe in qdegm__omfhx)
            bdvm__fpcmk = DataFrameType(qdegm__omfhx, eopt__gah.index,
                tuple(grp.selection))
    else:
        bdvm__fpcmk = eopt__gah
    pgdgu__tdpam = bdvm__fpcmk,
    pgdgu__tdpam += tuple(f_args)
    try:
        tni__nmmyh = get_const_func_output_type(func, pgdgu__tdpam, kws,
            typing_context, target_context)
    except Exception as yaasi__oawq:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', yaasi__oawq),
            getattr(yaasi__oawq, 'loc', None))
    return tni__nmmyh


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    pgdgu__tdpam = (grp,) + f_args
    try:
        tni__nmmyh = get_const_func_output_type(func, pgdgu__tdpam, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as yaasi__oawq:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()',
            yaasi__oawq), getattr(yaasi__oawq, 'loc', None))
    qjg__cwnoz = gen_apply_pysig(len(f_args), kws.keys())
    srxl__yrryh = (func, *f_args) + tuple(kws.values())
    return signature(tni__nmmyh, *srxl__yrryh).replace(pysig=qjg__cwnoz)


def gen_apply_pysig(n_args, kws):
    rytl__ejl = ', '.join(f'arg{yuq__jsf}' for yuq__jsf in range(n_args))
    rytl__ejl = rytl__ejl + ', ' if rytl__ejl else ''
    cov__xilzw = ', '.join(f"{xlpqz__mvv} = ''" for xlpqz__mvv in kws)
    ycixs__yfkg = f'def apply_stub(func, {rytl__ejl}{cov__xilzw}):\n'
    ycixs__yfkg += '    pass\n'
    jnbo__sxfyc = {}
    exec(ycixs__yfkg, {}, jnbo__sxfyc)
    svit__scthi = jnbo__sxfyc['apply_stub']
    return numba.core.utils.pysignature(svit__scthi)


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
        xxec__tnwn = get_pivot_output_dtype(data, aggfunc.literal_value)
        otqf__xthcc = dtype_to_array_type(xxec__tnwn)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/api_docs/pandas/dataframe/#pddataframepivot.'
                )
        cnwb__lcpk = _pivot_values.meta
        yrme__dzllm = len(cnwb__lcpk)
        wcr__fsl = df.columns.index(index)
        ndyxx__zhwda = df.data[wcr__fsl]
        ndyxx__zhwda = to_str_arr_if_dict_array(ndyxx__zhwda)
        ogtbn__razr = bodo.hiframes.pd_index_ext.array_type_to_index(
            ndyxx__zhwda, types.StringLiteral(index))
        dapf__wbjlq = DataFrameType((otqf__xthcc,) * yrme__dzllm,
            ogtbn__razr, tuple(cnwb__lcpk))
        return signature(dapf__wbjlq, *args)


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
        otqf__xthcc = types.Array(types.int64, 1, 'C')
        cnwb__lcpk = _pivot_values.meta
        yrme__dzllm = len(cnwb__lcpk)
        ogtbn__razr = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        dapf__wbjlq = DataFrameType((otqf__xthcc,) * yrme__dzllm,
            ogtbn__razr, tuple(cnwb__lcpk))
        return signature(dapf__wbjlq, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    ycixs__yfkg = 'def impl(keys, dropna, _is_parallel):\n'
    ycixs__yfkg += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    ycixs__yfkg += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{yuq__jsf}])' for yuq__jsf in range(len(keys.
        types))))
    ycixs__yfkg += '    table = arr_info_list_to_table(info_list)\n'
    ycixs__yfkg += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    ycixs__yfkg += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    ycixs__yfkg += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    ycixs__yfkg += '    delete_table_decref_arrays(table)\n'
    ycixs__yfkg += '    ev.finalize()\n'
    ycixs__yfkg += '    return sort_idx, group_labels, ngroups\n'
    jnbo__sxfyc = {}
    exec(ycixs__yfkg, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, jnbo__sxfyc)
    fxa__sbvm = jnbo__sxfyc['impl']
    return fxa__sbvm


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    dgtcj__osqru = len(labels)
    inxo__slqx = np.zeros(ngroups, dtype=np.int64)
    qinvw__ewuj = np.zeros(ngroups, dtype=np.int64)
    loii__cpt = 0
    rfi__hway = 0
    for yuq__jsf in range(dgtcj__osqru):
        qdshu__uusz = labels[yuq__jsf]
        if qdshu__uusz < 0:
            loii__cpt += 1
        else:
            rfi__hway += 1
            if yuq__jsf == dgtcj__osqru - 1 or qdshu__uusz != labels[
                yuq__jsf + 1]:
                inxo__slqx[qdshu__uusz] = loii__cpt
                qinvw__ewuj[qdshu__uusz] = loii__cpt + rfi__hway
                loii__cpt += rfi__hway
                rfi__hway = 0
    return inxo__slqx, qinvw__ewuj


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    fxa__sbvm, gexil__vni = gen_shuffle_dataframe(df, keys, _is_parallel)
    return fxa__sbvm


def gen_shuffle_dataframe(df, keys, _is_parallel):
    hwfz__apkm = len(df.columns)
    qyo__oicxi = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    ycixs__yfkg = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        ycixs__yfkg += '  return df, keys, get_null_shuffle_info()\n'
        jnbo__sxfyc = {}
        exec(ycixs__yfkg, {'get_null_shuffle_info': get_null_shuffle_info},
            jnbo__sxfyc)
        fxa__sbvm = jnbo__sxfyc['impl']
        return fxa__sbvm
    for yuq__jsf in range(hwfz__apkm):
        ycixs__yfkg += f"""  in_arr{yuq__jsf} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {yuq__jsf})
"""
    ycixs__yfkg += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    ycixs__yfkg += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{yuq__jsf}])' for yuq__jsf in range(qyo__oicxi
        )), ', '.join(f'array_to_info(in_arr{yuq__jsf})' for yuq__jsf in
        range(hwfz__apkm)), 'array_to_info(in_index_arr)')
    ycixs__yfkg += '  table = arr_info_list_to_table(info_list)\n'
    ycixs__yfkg += (
        f'  out_table = shuffle_table(table, {qyo__oicxi}, _is_parallel, 1)\n')
    for yuq__jsf in range(qyo__oicxi):
        ycixs__yfkg += f"""  out_key{yuq__jsf} = info_to_array(info_from_table(out_table, {yuq__jsf}), keys{yuq__jsf}_typ)
"""
    for yuq__jsf in range(hwfz__apkm):
        ycixs__yfkg += f"""  out_arr{yuq__jsf} = info_to_array(info_from_table(out_table, {yuq__jsf + qyo__oicxi}), in_arr{yuq__jsf}_typ)
"""
    ycixs__yfkg += f"""  out_arr_index = info_to_array(info_from_table(out_table, {qyo__oicxi + hwfz__apkm}), ind_arr_typ)
"""
    ycixs__yfkg += '  shuffle_info = get_shuffle_info(out_table)\n'
    ycixs__yfkg += '  delete_table(out_table)\n'
    ycixs__yfkg += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{yuq__jsf}' for yuq__jsf in range(hwfz__apkm)
        )
    ycixs__yfkg += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    ycixs__yfkg += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    ycixs__yfkg += '  return out_df, ({},), shuffle_info\n'.format(', '.
        join(f'out_key{yuq__jsf}' for yuq__jsf in range(qyo__oicxi)))
    kmr__roqx = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    kmr__roqx.update({f'keys{yuq__jsf}_typ': keys.types[yuq__jsf] for
        yuq__jsf in range(qyo__oicxi)})
    kmr__roqx.update({f'in_arr{yuq__jsf}_typ': df.data[yuq__jsf] for
        yuq__jsf in range(hwfz__apkm)})
    jnbo__sxfyc = {}
    exec(ycixs__yfkg, kmr__roqx, jnbo__sxfyc)
    fxa__sbvm = jnbo__sxfyc['impl']
    return fxa__sbvm, kmr__roqx


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        uusal__kkjof = len(data.array_types)
        ycixs__yfkg = 'def impl(data, shuffle_info):\n'
        ycixs__yfkg += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{yuq__jsf}])' for yuq__jsf in range(
            uusal__kkjof)))
        ycixs__yfkg += '  table = arr_info_list_to_table(info_list)\n'
        ycixs__yfkg += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for yuq__jsf in range(uusal__kkjof):
            ycixs__yfkg += f"""  out_arr{yuq__jsf} = info_to_array(info_from_table(out_table, {yuq__jsf}), data._data[{yuq__jsf}])
"""
        ycixs__yfkg += '  delete_table(out_table)\n'
        ycixs__yfkg += '  delete_table(table)\n'
        ycixs__yfkg += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{yuq__jsf}' for yuq__jsf in range(
            uusal__kkjof))))
        jnbo__sxfyc = {}
        exec(ycixs__yfkg, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, jnbo__sxfyc)
        fxa__sbvm = jnbo__sxfyc['impl']
        return fxa__sbvm
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            rysg__hkvou = bodo.utils.conversion.index_to_array(data)
            pkbrh__ymlma = reverse_shuffle(rysg__hkvou, shuffle_info)
            return bodo.utils.conversion.index_from_array(pkbrh__ymlma)
        return impl_index

    def impl_arr(data, shuffle_info):
        aef__dqw = [array_to_info(data)]
        ttdxa__wtpz = arr_info_list_to_table(aef__dqw)
        wzmcs__gzsep = reverse_shuffle_table(ttdxa__wtpz, shuffle_info)
        pkbrh__ymlma = info_to_array(info_from_table(wzmcs__gzsep, 0), data)
        delete_table(wzmcs__gzsep)
        delete_table(ttdxa__wtpz)
        return pkbrh__ymlma
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    hni__xquh = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    mkpur__bgv = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', hni__xquh, mkpur__bgv,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    cijjr__vqw = get_overload_const_bool(ascending)
    hnfe__epd = grp.selection[0]
    ycixs__yfkg = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    oam__ipxax = (
        f"lambda S: S.value_counts(ascending={cijjr__vqw}, _index_name='{hnfe__epd}')"
        )
    ycixs__yfkg += f'    return grp.apply({oam__ipxax})\n'
    jnbo__sxfyc = {}
    exec(ycixs__yfkg, {'bodo': bodo}, jnbo__sxfyc)
    fxa__sbvm = jnbo__sxfyc['impl']
    return fxa__sbvm


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
    for zxay__xdj in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, zxay__xdj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{zxay__xdj}'))
    for zxay__xdj in groupby_unsupported:
        overload_method(DataFrameGroupByType, zxay__xdj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{zxay__xdj}'))
    for zxay__xdj in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, zxay__xdj, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{zxay__xdj}'))
    for zxay__xdj in series_only_unsupported:
        overload_method(DataFrameGroupByType, zxay__xdj, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{zxay__xdj}'))
    for zxay__xdj in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, zxay__xdj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{zxay__xdj}'))


_install_groupby_unsupported()
