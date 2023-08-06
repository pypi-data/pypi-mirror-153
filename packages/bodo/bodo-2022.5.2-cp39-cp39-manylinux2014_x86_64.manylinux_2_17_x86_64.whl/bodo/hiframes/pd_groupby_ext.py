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
        xaq__tlok = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, xaq__tlok)


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
        wrhv__tsre = args[0]
        fumm__cfq = signature.return_type
        nnug__hsttj = cgutils.create_struct_proxy(fumm__cfq)(context, builder)
        nnug__hsttj.obj = wrhv__tsre
        context.nrt.incref(builder, signature.args[0], wrhv__tsre)
        return nnug__hsttj._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for qbky__seqg in keys:
        selection.remove(qbky__seqg)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    fumm__cfq = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return fumm__cfq(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, okrf__gpwt = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(okrf__gpwt, (tuple, list)):
                if len(set(okrf__gpwt).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(okrf__gpwt).difference(set(grpby.
                        df_type.columns))))
                selection = okrf__gpwt
            else:
                if okrf__gpwt not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(okrf__gpwt))
                selection = okrf__gpwt,
                series_select = True
            zrmp__hsme = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(zrmp__hsme, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, okrf__gpwt = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            okrf__gpwt):
            zrmp__hsme = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(okrf__gpwt)), {}).return_type
            return signature(zrmp__hsme, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    nicte__avx = arr_type == ArrayItemArrayType(string_array_type)
    ubf__mrmj = arr_type.dtype
    if isinstance(ubf__mrmj, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {ubf__mrmj} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(ubf__mrmj, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {ubf__mrmj} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(ubf__mrmj,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(ubf__mrmj, (types.Integer, types.Float, types.Boolean)):
        if nicte__avx or ubf__mrmj == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(ubf__mrmj, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not ubf__mrmj.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {ubf__mrmj} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(ubf__mrmj, types.Boolean) and func_name in {'cumsum',
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
    ubf__mrmj = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(ubf__mrmj, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(ubf__mrmj, types.Integer):
            return IntDtype(ubf__mrmj)
        return ubf__mrmj
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        npsp__quoe = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{npsp__quoe}'."
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
    for qbky__seqg in grp.keys:
        if multi_level_names:
            adfff__jxwbk = qbky__seqg, ''
        else:
            adfff__jxwbk = qbky__seqg
        mpnze__ypiv = grp.df_type.columns.index(qbky__seqg)
        data = to_str_arr_if_dict_array(grp.df_type.data[mpnze__ypiv])
        out_columns.append(adfff__jxwbk)
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
        ukma__psev = tuple(grp.df_type.column_index[grp.keys[nbcaz__xtj]] for
            nbcaz__xtj in range(len(grp.keys)))
        acy__rkn = tuple(grp.df_type.data[mpnze__ypiv] for mpnze__ypiv in
            ukma__psev)
        acy__rkn = tuple(to_str_arr_if_dict_array(ulncy__pax) for
            ulncy__pax in acy__rkn)
        index = MultiIndexType(acy__rkn, tuple(types.StringLiteral(
            qbky__seqg) for qbky__seqg in grp.keys))
    else:
        mpnze__ypiv = grp.df_type.column_index[grp.keys[0]]
        btfpa__fos = to_str_arr_if_dict_array(grp.df_type.data[mpnze__ypiv])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(btfpa__fos,
            types.StringLiteral(grp.keys[0]))
    crs__rpjni = {}
    hbcq__ezyi = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        crs__rpjni[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for wtj__vnov in columns:
            mpnze__ypiv = grp.df_type.column_index[wtj__vnov]
            data = grp.df_type.data[mpnze__ypiv]
            data = to_str_arr_if_dict_array(data)
            gth__snfyu = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                gth__snfyu = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    lzp__dret = SeriesType(data.dtype, data, None, string_type)
                    eabm__oju = get_const_func_output_type(func, (lzp__dret
                        ,), {}, typing_context, target_context)
                    if eabm__oju != ArrayItemArrayType(string_array_type):
                        eabm__oju = dtype_to_array_type(eabm__oju)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=wtj__vnov, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    tte__jffy = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    wcqf__noi = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    yicbj__mlmpi = dict(numeric_only=tte__jffy, min_count=
                        wcqf__noi)
                    urn__mka = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        yicbj__mlmpi, urn__mka, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    tte__jffy = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    wcqf__noi = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    yicbj__mlmpi = dict(numeric_only=tte__jffy, min_count=
                        wcqf__noi)
                    urn__mka = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        yicbj__mlmpi, urn__mka, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    tte__jffy = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    yicbj__mlmpi = dict(numeric_only=tte__jffy)
                    urn__mka = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        yicbj__mlmpi, urn__mka, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    lfes__aak = args[0] if len(args) > 0 else kws.pop('axis', 0
                        )
                    awem__buh = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    yicbj__mlmpi = dict(axis=lfes__aak, skipna=awem__buh)
                    urn__mka = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        yicbj__mlmpi, urn__mka, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    wowa__olru = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    yicbj__mlmpi = dict(ddof=wowa__olru)
                    urn__mka = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        yicbj__mlmpi, urn__mka, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                eabm__oju, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                ufa__ljht = to_str_arr_if_dict_array(eabm__oju)
                out_data.append(ufa__ljht)
                out_columns.append(wtj__vnov)
                if func_name == 'agg':
                    nwb__ewvi = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    crs__rpjni[wtj__vnov, nwb__ewvi] = wtj__vnov
                else:
                    crs__rpjni[wtj__vnov, func_name] = wtj__vnov
                out_column_type.append(gth__snfyu)
            else:
                hbcq__ezyi.append(err_msg)
    if func_name == 'sum':
        tbid__nycka = any([(oxq__jhbzj == ColumnType.NumericalColumn.value) for
            oxq__jhbzj in out_column_type])
        if tbid__nycka:
            out_data = [oxq__jhbzj for oxq__jhbzj, tssew__hfqfv in zip(
                out_data, out_column_type) if tssew__hfqfv != ColumnType.
                NonNumericalColumn.value]
            out_columns = [oxq__jhbzj for oxq__jhbzj, tssew__hfqfv in zip(
                out_columns, out_column_type) if tssew__hfqfv != ColumnType
                .NonNumericalColumn.value]
            crs__rpjni = {}
            for wtj__vnov in out_columns:
                if grp.as_index is False and wtj__vnov in grp.keys:
                    continue
                crs__rpjni[wtj__vnov, func_name] = wtj__vnov
    klqlp__nrptk = len(hbcq__ezyi)
    if len(out_data) == 0:
        if klqlp__nrptk == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(klqlp__nrptk, ' was' if klqlp__nrptk == 1 else
                's were', ','.join(hbcq__ezyi)))
    wjoir__wsj = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            dzyft__tfmxh = IntDtype(out_data[0].dtype)
        else:
            dzyft__tfmxh = out_data[0].dtype
        zqeh__fif = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        wjoir__wsj = SeriesType(dzyft__tfmxh, index=index, name_typ=zqeh__fif)
    return signature(wjoir__wsj, *args), crs__rpjni


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    swi__guukd = True
    if isinstance(f_val, str):
        swi__guukd = False
        ffig__gkih = f_val
    elif is_overload_constant_str(f_val):
        swi__guukd = False
        ffig__gkih = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        swi__guukd = False
        ffig__gkih = bodo.utils.typing.get_builtin_function_name(f_val)
    if not swi__guukd:
        if ffig__gkih not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {ffig__gkih}')
        zrmp__hsme = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(zrmp__hsme, (), ffig__gkih, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            noaqm__oixy = types.functions.MakeFunctionLiteral(f_val)
        else:
            noaqm__oixy = f_val
        validate_udf('agg', noaqm__oixy)
        func = get_overload_const_func(noaqm__oixy, None)
        nfnef__gmbz = func.code if hasattr(func, 'code') else func.__code__
        ffig__gkih = nfnef__gmbz.co_name
        zrmp__hsme = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(zrmp__hsme, (), 'agg', typing_context,
            target_context, noaqm__oixy)[0].return_type
    return ffig__gkih, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    wnyed__ttw = kws and all(isinstance(kqwmt__htf, types.Tuple) and len(
        kqwmt__htf) == 2 for kqwmt__htf in kws.values())
    if is_overload_none(func) and not wnyed__ttw:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not wnyed__ttw:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    gdmp__vrc = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if wnyed__ttw or is_overload_constant_dict(func):
        if wnyed__ttw:
            qhwmg__fygn = [get_literal_value(vil__bssfv) for vil__bssfv,
                pbjxc__agkf in kws.values()]
            bca__lkj = [get_literal_value(qtp__mrtdq) for pbjxc__agkf,
                qtp__mrtdq in kws.values()]
        else:
            wlnk__doe = get_overload_constant_dict(func)
            qhwmg__fygn = tuple(wlnk__doe.keys())
            bca__lkj = tuple(wlnk__doe.values())
        if 'head' in bca__lkj:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(wtj__vnov not in grp.selection and wtj__vnov not in grp.keys for
            wtj__vnov in qhwmg__fygn):
            raise_bodo_error(
                f'Selected column names {qhwmg__fygn} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            bca__lkj)
        if wnyed__ttw and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        crs__rpjni = {}
        out_columns = []
        out_data = []
        out_column_type = []
        dxl__dioku = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for hmwsp__yneqd, f_val in zip(qhwmg__fygn, bca__lkj):
            if isinstance(f_val, (tuple, list)):
                wqi__lgap = 0
                for noaqm__oixy in f_val:
                    ffig__gkih, out_tp = get_agg_funcname_and_outtyp(grp,
                        hmwsp__yneqd, noaqm__oixy, typing_context,
                        target_context)
                    gdmp__vrc = ffig__gkih in list_cumulative
                    if ffig__gkih == '<lambda>' and len(f_val) > 1:
                        ffig__gkih = '<lambda_' + str(wqi__lgap) + '>'
                        wqi__lgap += 1
                    out_columns.append((hmwsp__yneqd, ffig__gkih))
                    crs__rpjni[hmwsp__yneqd, ffig__gkih
                        ] = hmwsp__yneqd, ffig__gkih
                    _append_out_type(grp, out_data, out_tp)
            else:
                ffig__gkih, out_tp = get_agg_funcname_and_outtyp(grp,
                    hmwsp__yneqd, f_val, typing_context, target_context)
                gdmp__vrc = ffig__gkih in list_cumulative
                if multi_level_names:
                    out_columns.append((hmwsp__yneqd, ffig__gkih))
                    crs__rpjni[hmwsp__yneqd, ffig__gkih
                        ] = hmwsp__yneqd, ffig__gkih
                elif not wnyed__ttw:
                    out_columns.append(hmwsp__yneqd)
                    crs__rpjni[hmwsp__yneqd, ffig__gkih] = hmwsp__yneqd
                elif wnyed__ttw:
                    dxl__dioku.append(ffig__gkih)
                _append_out_type(grp, out_data, out_tp)
        if wnyed__ttw:
            for nbcaz__xtj, tnbki__jaau in enumerate(kws.keys()):
                out_columns.append(tnbki__jaau)
                crs__rpjni[qhwmg__fygn[nbcaz__xtj], dxl__dioku[nbcaz__xtj]
                    ] = tnbki__jaau
        if gdmp__vrc:
            index = grp.df_type.index
        else:
            index = out_tp.index
        wjoir__wsj = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(wjoir__wsj, *args), crs__rpjni
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            end__hcypj = get_overload_const_list(func)
        else:
            end__hcypj = func.types
        if len(end__hcypj) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        wqi__lgap = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        crs__rpjni = {}
        ild__tqj = grp.selection[0]
        for f_val in end__hcypj:
            ffig__gkih, out_tp = get_agg_funcname_and_outtyp(grp, ild__tqj,
                f_val, typing_context, target_context)
            gdmp__vrc = ffig__gkih in list_cumulative
            if ffig__gkih == '<lambda>' and len(end__hcypj) > 1:
                ffig__gkih = '<lambda_' + str(wqi__lgap) + '>'
                wqi__lgap += 1
            out_columns.append(ffig__gkih)
            crs__rpjni[ild__tqj, ffig__gkih] = ffig__gkih
            _append_out_type(grp, out_data, out_tp)
        if gdmp__vrc:
            index = grp.df_type.index
        else:
            index = out_tp.index
        wjoir__wsj = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(wjoir__wsj, *args), crs__rpjni
    ffig__gkih = ''
    if types.unliteral(func) == types.unicode_type:
        ffig__gkih = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        ffig__gkih = bodo.utils.typing.get_builtin_function_name(func)
    if ffig__gkih:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, ffig__gkih, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        lfes__aak = args[0] if len(args) > 0 else kws.pop('axis', 0)
        tte__jffy = args[1] if len(args) > 1 else kws.pop('numeric_only', False
            )
        awem__buh = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        yicbj__mlmpi = dict(axis=lfes__aak, numeric_only=tte__jffy)
        urn__mka = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', yicbj__mlmpi,
            urn__mka, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        irt__xzyls = args[0] if len(args) > 0 else kws.pop('periods', 1)
        pdfrk__fjka = args[1] if len(args) > 1 else kws.pop('freq', None)
        lfes__aak = args[2] if len(args) > 2 else kws.pop('axis', 0)
        abb__ebojd = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        yicbj__mlmpi = dict(freq=pdfrk__fjka, axis=lfes__aak, fill_value=
            abb__ebojd)
        urn__mka = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', yicbj__mlmpi,
            urn__mka, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        eax__cyg = args[0] if len(args) > 0 else kws.pop('func', None)
        gdzo__slv = kws.pop('engine', None)
        ahiid__ixgu = kws.pop('engine_kwargs', None)
        yicbj__mlmpi = dict(engine=gdzo__slv, engine_kwargs=ahiid__ixgu)
        urn__mka = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', yicbj__mlmpi, urn__mka,
            package_name='pandas', module_name='GroupBy')
    crs__rpjni = {}
    for wtj__vnov in grp.selection:
        out_columns.append(wtj__vnov)
        crs__rpjni[wtj__vnov, name_operation] = wtj__vnov
        mpnze__ypiv = grp.df_type.columns.index(wtj__vnov)
        data = grp.df_type.data[mpnze__ypiv]
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
            eabm__oju, err_msg = get_groupby_output_dtype(data,
                get_literal_value(eax__cyg), grp.df_type.index)
            if err_msg == 'ok':
                data = eabm__oju
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    wjoir__wsj = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        wjoir__wsj = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(wjoir__wsj, *args), crs__rpjni


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
        php__rmr = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        ywase__wlrio = isinstance(php__rmr, (SeriesType,
            HeterogeneousSeriesType)
            ) and php__rmr.const_info is not None or not isinstance(php__rmr,
            (SeriesType, DataFrameType))
        if ywase__wlrio:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                nlffm__niau = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                ukma__psev = tuple(grp.df_type.columns.index(grp.keys[
                    nbcaz__xtj]) for nbcaz__xtj in range(len(grp.keys)))
                acy__rkn = tuple(grp.df_type.data[mpnze__ypiv] for
                    mpnze__ypiv in ukma__psev)
                acy__rkn = tuple(to_str_arr_if_dict_array(ulncy__pax) for
                    ulncy__pax in acy__rkn)
                nlffm__niau = MultiIndexType(acy__rkn, tuple(types.literal(
                    qbky__seqg) for qbky__seqg in grp.keys))
            else:
                mpnze__ypiv = grp.df_type.columns.index(grp.keys[0])
                btfpa__fos = grp.df_type.data[mpnze__ypiv]
                btfpa__fos = to_str_arr_if_dict_array(btfpa__fos)
                nlffm__niau = bodo.hiframes.pd_index_ext.array_type_to_index(
                    btfpa__fos, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            mhjct__xmg = tuple(grp.df_type.data[grp.df_type.columns.index(
                wtj__vnov)] for wtj__vnov in grp.keys)
            mhjct__xmg = tuple(to_str_arr_if_dict_array(ulncy__pax) for
                ulncy__pax in mhjct__xmg)
            lggbw__jpjo = tuple(types.literal(kqwmt__htf) for kqwmt__htf in
                grp.keys) + get_index_name_types(php__rmr.index)
            if not grp.as_index:
                mhjct__xmg = types.Array(types.int64, 1, 'C'),
                lggbw__jpjo = (types.none,) + get_index_name_types(php__rmr
                    .index)
            nlffm__niau = MultiIndexType(mhjct__xmg +
                get_index_data_arr_types(php__rmr.index), lggbw__jpjo)
        if ywase__wlrio:
            if isinstance(php__rmr, HeterogeneousSeriesType):
                pbjxc__agkf, qkur__gjht = php__rmr.const_info
                if isinstance(php__rmr.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    bkuk__nrvu = php__rmr.data.tuple_typ.types
                elif isinstance(php__rmr.data, types.Tuple):
                    bkuk__nrvu = php__rmr.data.types
                ubnn__izei = tuple(to_nullable_type(dtype_to_array_type(
                    ulncy__pax)) for ulncy__pax in bkuk__nrvu)
                brt__lig = DataFrameType(out_data + ubnn__izei, nlffm__niau,
                    out_columns + qkur__gjht)
            elif isinstance(php__rmr, SeriesType):
                zzt__pbo, qkur__gjht = php__rmr.const_info
                ubnn__izei = tuple(to_nullable_type(dtype_to_array_type(
                    php__rmr.dtype)) for pbjxc__agkf in range(zzt__pbo))
                brt__lig = DataFrameType(out_data + ubnn__izei, nlffm__niau,
                    out_columns + qkur__gjht)
            else:
                cvd__wgq = get_udf_out_arr_type(php__rmr)
                if not grp.as_index:
                    brt__lig = DataFrameType(out_data + (cvd__wgq,),
                        nlffm__niau, out_columns + ('',))
                else:
                    brt__lig = SeriesType(cvd__wgq.dtype, cvd__wgq,
                        nlffm__niau, None)
        elif isinstance(php__rmr, SeriesType):
            brt__lig = SeriesType(php__rmr.dtype, php__rmr.data,
                nlffm__niau, php__rmr.name_typ)
        else:
            brt__lig = DataFrameType(php__rmr.data, nlffm__niau, php__rmr.
                columns)
        idg__sxpaa = gen_apply_pysig(len(f_args), kws.keys())
        scnfy__fqo = (func, *f_args) + tuple(kws.values())
        return signature(brt__lig, *scnfy__fqo).replace(pysig=idg__sxpaa)

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
    rtub__orr = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            hmwsp__yneqd = grp.selection[0]
            cvd__wgq = rtub__orr.data[rtub__orr.columns.index(hmwsp__yneqd)]
            cvd__wgq = to_str_arr_if_dict_array(cvd__wgq)
            emqn__iiuux = SeriesType(cvd__wgq.dtype, cvd__wgq, rtub__orr.
                index, types.literal(hmwsp__yneqd))
        else:
            bol__oss = tuple(rtub__orr.data[rtub__orr.columns.index(
                wtj__vnov)] for wtj__vnov in grp.selection)
            bol__oss = tuple(to_str_arr_if_dict_array(ulncy__pax) for
                ulncy__pax in bol__oss)
            emqn__iiuux = DataFrameType(bol__oss, rtub__orr.index, tuple(
                grp.selection))
    else:
        emqn__iiuux = rtub__orr
    htjn__kcjj = emqn__iiuux,
    htjn__kcjj += tuple(f_args)
    try:
        php__rmr = get_const_func_output_type(func, htjn__kcjj, kws,
            typing_context, target_context)
    except Exception as dqcdo__pwd:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', dqcdo__pwd),
            getattr(dqcdo__pwd, 'loc', None))
    return php__rmr


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    htjn__kcjj = (grp,) + f_args
    try:
        php__rmr = get_const_func_output_type(func, htjn__kcjj, kws, self.
            context, numba.core.registry.cpu_target.target_context, False)
    except Exception as dqcdo__pwd:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', dqcdo__pwd
            ), getattr(dqcdo__pwd, 'loc', None))
    idg__sxpaa = gen_apply_pysig(len(f_args), kws.keys())
    scnfy__fqo = (func, *f_args) + tuple(kws.values())
    return signature(php__rmr, *scnfy__fqo).replace(pysig=idg__sxpaa)


def gen_apply_pysig(n_args, kws):
    zcpas__bbx = ', '.join(f'arg{nbcaz__xtj}' for nbcaz__xtj in range(n_args))
    zcpas__bbx = zcpas__bbx + ', ' if zcpas__bbx else ''
    dvlf__lnz = ', '.join(f"{fke__rnqzg} = ''" for fke__rnqzg in kws)
    suc__opy = f'def apply_stub(func, {zcpas__bbx}{dvlf__lnz}):\n'
    suc__opy += '    pass\n'
    icf__nwpih = {}
    exec(suc__opy, {}, icf__nwpih)
    bzbcx__ilnh = icf__nwpih['apply_stub']
    return numba.core.utils.pysignature(bzbcx__ilnh)


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
        eabm__oju = get_pivot_output_dtype(data, aggfunc.literal_value)
        cpqsf__mmy = dtype_to_array_type(eabm__oju)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/api_docs/pandas/dataframe/#pddataframepivot.'
                )
        ktjwm__rbika = _pivot_values.meta
        fxod__tta = len(ktjwm__rbika)
        mpnze__ypiv = df.columns.index(index)
        btfpa__fos = df.data[mpnze__ypiv]
        btfpa__fos = to_str_arr_if_dict_array(btfpa__fos)
        lnpg__yhs = bodo.hiframes.pd_index_ext.array_type_to_index(btfpa__fos,
            types.StringLiteral(index))
        muipa__mlcda = DataFrameType((cpqsf__mmy,) * fxod__tta, lnpg__yhs,
            tuple(ktjwm__rbika))
        return signature(muipa__mlcda, *args)


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
        cpqsf__mmy = types.Array(types.int64, 1, 'C')
        ktjwm__rbika = _pivot_values.meta
        fxod__tta = len(ktjwm__rbika)
        lnpg__yhs = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        muipa__mlcda = DataFrameType((cpqsf__mmy,) * fxod__tta, lnpg__yhs,
            tuple(ktjwm__rbika))
        return signature(muipa__mlcda, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    suc__opy = 'def impl(keys, dropna, _is_parallel):\n'
    suc__opy += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    suc__opy += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{nbcaz__xtj}])' for nbcaz__xtj in range(len(
        keys.types))))
    suc__opy += '    table = arr_info_list_to_table(info_list)\n'
    suc__opy += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    suc__opy += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    suc__opy += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    suc__opy += '    delete_table_decref_arrays(table)\n'
    suc__opy += '    ev.finalize()\n'
    suc__opy += '    return sort_idx, group_labels, ngroups\n'
    icf__nwpih = {}
    exec(suc__opy, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, icf__nwpih)
    gdys__pks = icf__nwpih['impl']
    return gdys__pks


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    xtpx__zag = len(labels)
    lqpdq__kfjix = np.zeros(ngroups, dtype=np.int64)
    ukkk__wau = np.zeros(ngroups, dtype=np.int64)
    gbj__okpws = 0
    nqjf__xnlu = 0
    for nbcaz__xtj in range(xtpx__zag):
        fqiif__dits = labels[nbcaz__xtj]
        if fqiif__dits < 0:
            gbj__okpws += 1
        else:
            nqjf__xnlu += 1
            if nbcaz__xtj == xtpx__zag - 1 or fqiif__dits != labels[
                nbcaz__xtj + 1]:
                lqpdq__kfjix[fqiif__dits] = gbj__okpws
                ukkk__wau[fqiif__dits] = gbj__okpws + nqjf__xnlu
                gbj__okpws += nqjf__xnlu
                nqjf__xnlu = 0
    return lqpdq__kfjix, ukkk__wau


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    gdys__pks, pbjxc__agkf = gen_shuffle_dataframe(df, keys, _is_parallel)
    return gdys__pks


def gen_shuffle_dataframe(df, keys, _is_parallel):
    zzt__pbo = len(df.columns)
    inpqg__vimmw = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    suc__opy = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        suc__opy += '  return df, keys, get_null_shuffle_info()\n'
        icf__nwpih = {}
        exec(suc__opy, {'get_null_shuffle_info': get_null_shuffle_info},
            icf__nwpih)
        gdys__pks = icf__nwpih['impl']
        return gdys__pks
    for nbcaz__xtj in range(zzt__pbo):
        suc__opy += f"""  in_arr{nbcaz__xtj} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {nbcaz__xtj})
"""
    suc__opy += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    suc__opy += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{nbcaz__xtj}])' for nbcaz__xtj in range(
        inpqg__vimmw)), ', '.join(f'array_to_info(in_arr{nbcaz__xtj})' for
        nbcaz__xtj in range(zzt__pbo)), 'array_to_info(in_index_arr)')
    suc__opy += '  table = arr_info_list_to_table(info_list)\n'
    suc__opy += (
        f'  out_table = shuffle_table(table, {inpqg__vimmw}, _is_parallel, 1)\n'
        )
    for nbcaz__xtj in range(inpqg__vimmw):
        suc__opy += f"""  out_key{nbcaz__xtj} = info_to_array(info_from_table(out_table, {nbcaz__xtj}), keys{nbcaz__xtj}_typ)
"""
    for nbcaz__xtj in range(zzt__pbo):
        suc__opy += f"""  out_arr{nbcaz__xtj} = info_to_array(info_from_table(out_table, {nbcaz__xtj + inpqg__vimmw}), in_arr{nbcaz__xtj}_typ)
"""
    suc__opy += f"""  out_arr_index = info_to_array(info_from_table(out_table, {inpqg__vimmw + zzt__pbo}), ind_arr_typ)
"""
    suc__opy += '  shuffle_info = get_shuffle_info(out_table)\n'
    suc__opy += '  delete_table(out_table)\n'
    suc__opy += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{nbcaz__xtj}' for nbcaz__xtj in range(
        zzt__pbo))
    suc__opy += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    suc__opy += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    suc__opy += '  return out_df, ({},), shuffle_info\n'.format(', '.join(
        f'out_key{nbcaz__xtj}' for nbcaz__xtj in range(inpqg__vimmw)))
    lxhq__yij = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    lxhq__yij.update({f'keys{nbcaz__xtj}_typ': keys.types[nbcaz__xtj] for
        nbcaz__xtj in range(inpqg__vimmw)})
    lxhq__yij.update({f'in_arr{nbcaz__xtj}_typ': df.data[nbcaz__xtj] for
        nbcaz__xtj in range(zzt__pbo)})
    icf__nwpih = {}
    exec(suc__opy, lxhq__yij, icf__nwpih)
    gdys__pks = icf__nwpih['impl']
    return gdys__pks, lxhq__yij


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        mho__pgot = len(data.array_types)
        suc__opy = 'def impl(data, shuffle_info):\n'
        suc__opy += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{nbcaz__xtj}])' for nbcaz__xtj in
            range(mho__pgot)))
        suc__opy += '  table = arr_info_list_to_table(info_list)\n'
        suc__opy += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for nbcaz__xtj in range(mho__pgot):
            suc__opy += f"""  out_arr{nbcaz__xtj} = info_to_array(info_from_table(out_table, {nbcaz__xtj}), data._data[{nbcaz__xtj}])
"""
        suc__opy += '  delete_table(out_table)\n'
        suc__opy += '  delete_table(table)\n'
        suc__opy += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{nbcaz__xtj}' for nbcaz__xtj in range
            (mho__pgot))))
        icf__nwpih = {}
        exec(suc__opy, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, icf__nwpih)
        gdys__pks = icf__nwpih['impl']
        return gdys__pks
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            adlpg__ttaa = bodo.utils.conversion.index_to_array(data)
            ufa__ljht = reverse_shuffle(adlpg__ttaa, shuffle_info)
            return bodo.utils.conversion.index_from_array(ufa__ljht)
        return impl_index

    def impl_arr(data, shuffle_info):
        wyx__zvq = [array_to_info(data)]
        mqwv__yngus = arr_info_list_to_table(wyx__zvq)
        yoxnw__nzm = reverse_shuffle_table(mqwv__yngus, shuffle_info)
        ufa__ljht = info_to_array(info_from_table(yoxnw__nzm, 0), data)
        delete_table(yoxnw__nzm)
        delete_table(mqwv__yngus)
        return ufa__ljht
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    yicbj__mlmpi = dict(normalize=normalize, sort=sort, bins=bins, dropna=
        dropna)
    urn__mka = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', yicbj__mlmpi, urn__mka,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    gpdzp__rkyet = get_overload_const_bool(ascending)
    wzyhe__lhyf = grp.selection[0]
    suc__opy = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    lpdk__vbyit = (
        f"lambda S: S.value_counts(ascending={gpdzp__rkyet}, _index_name='{wzyhe__lhyf}')"
        )
    suc__opy += f'    return grp.apply({lpdk__vbyit})\n'
    icf__nwpih = {}
    exec(suc__opy, {'bodo': bodo}, icf__nwpih)
    gdys__pks = icf__nwpih['impl']
    return gdys__pks


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
    for jjue__lqas in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, jjue__lqas, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{jjue__lqas}'))
    for jjue__lqas in groupby_unsupported:
        overload_method(DataFrameGroupByType, jjue__lqas, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{jjue__lqas}'))
    for jjue__lqas in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, jjue__lqas, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{jjue__lqas}'))
    for jjue__lqas in series_only_unsupported:
        overload_method(DataFrameGroupByType, jjue__lqas, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{jjue__lqas}'))
    for jjue__lqas in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, jjue__lqas, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{jjue__lqas}'))


_install_groupby_unsupported()
