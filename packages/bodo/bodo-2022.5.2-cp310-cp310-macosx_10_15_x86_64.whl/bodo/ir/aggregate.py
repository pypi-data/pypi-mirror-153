"""IR node for the groupby, pivot and cross_tabulation"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, pivot_groupby_and_aggregate
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, decode_if_dict_array, get_literal_value, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array
from bodo.utils.utils import debug_prints, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign, sanitize_varname, unliteral_all
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        sig = func.signature
        if sig == types.none(types.voidptr):
            xyzxx__chxu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            mloh__dfv = cgutils.get_or_insert_function(builder.module,
                xyzxx__chxu, sym._literal_value)
            builder.call(mloh__dfv, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            xyzxx__chxu = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            mloh__dfv = cgutils.get_or_insert_function(builder.module,
                xyzxx__chxu, sym._literal_value)
            builder.call(mloh__dfv, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            xyzxx__chxu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            mloh__dfv = cgutils.get_or_insert_function(builder.module,
                xyzxx__chxu, sym._literal_value)
            builder.call(mloh__dfv, [context.get_constant_null(sig.args[0]),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'head', 'transform', 'size', 'shift', 'sum',
    'count', 'nunique', 'median', 'cumsum', 'cumprod', 'cummin', 'cummax',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'idxmin', 'idxmax',
    'var', 'std', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        nkffc__osr = True
        ryoa__blu = 1
        szozb__kzmr = -1
        if isinstance(rhs, ir.Expr):
            for gtpzd__hhji in rhs.kws:
                if func_name in list_cumulative:
                    if gtpzd__hhji[0] == 'skipna':
                        nkffc__osr = guard(find_const, func_ir, gtpzd__hhji[1])
                        if not isinstance(nkffc__osr, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if gtpzd__hhji[0] == 'dropna':
                        nkffc__osr = guard(find_const, func_ir, gtpzd__hhji[1])
                        if not isinstance(nkffc__osr, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            ryoa__blu = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', ryoa__blu)
            ryoa__blu = guard(find_const, func_ir, ryoa__blu)
        if func_name == 'head':
            szozb__kzmr = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(szozb__kzmr, int):
                szozb__kzmr = guard(find_const, func_ir, szozb__kzmr)
            if szozb__kzmr < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = nkffc__osr
        func.periods = ryoa__blu
        func.head_n = szozb__kzmr
        if func_name == 'transform':
            kws = dict(rhs.kws)
            fft__feg = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            zxk__akvu = typemap[fft__feg.name]
            qbk__ghi = None
            if isinstance(zxk__akvu, str):
                qbk__ghi = zxk__akvu
            elif is_overload_constant_str(zxk__akvu):
                qbk__ghi = get_overload_const_str(zxk__akvu)
            elif bodo.utils.typing.is_builtin_function(zxk__akvu):
                qbk__ghi = bodo.utils.typing.get_builtin_function_name(
                    zxk__akvu)
            if qbk__ghi not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {qbk__ghi}')
            func.transform_func = supported_agg_funcs.index(qbk__ghi)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    fft__feg = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if fft__feg == '':
        zxk__akvu = types.none
    else:
        zxk__akvu = typemap[fft__feg.name]
    if is_overload_constant_dict(zxk__akvu):
        mjd__pjoz = get_overload_constant_dict(zxk__akvu)
        bul__vyxhn = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in mjd__pjoz.values()]
        return bul__vyxhn
    if zxk__akvu == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(zxk__akvu, types.BaseTuple) or is_overload_constant_list(
        zxk__akvu):
        bul__vyxhn = []
        jlha__mkvii = 0
        if is_overload_constant_list(zxk__akvu):
            cqpen__zyj = get_overload_const_list(zxk__akvu)
        else:
            cqpen__zyj = zxk__akvu.types
        for t in cqpen__zyj:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                bul__vyxhn.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(cqpen__zyj) > 1:
                    func.fname = '<lambda_' + str(jlha__mkvii) + '>'
                    jlha__mkvii += 1
                bul__vyxhn.append(func)
        return [bul__vyxhn]
    if is_overload_constant_str(zxk__akvu):
        func_name = get_overload_const_str(zxk__akvu)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(zxk__akvu):
        func_name = bodo.utils.typing.get_builtin_function_name(zxk__akvu)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        jlha__mkvii = 0
        opvm__jzmju = []
        for pdb__ayg in f_val:
            func = get_agg_func_udf(func_ir, pdb__ayg, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{jlha__mkvii}>'
                jlha__mkvii += 1
            opvm__jzmju.append(func)
        return opvm__jzmju
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    qbk__ghi = code.co_name
    return qbk__ghi


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            nmzo__gun = types.DType(args[0])
            return signature(nmzo__gun, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    nnx__mwc = nobs_a + nobs_b
    reg__jqr = (nobs_a * mean_a + nobs_b * mean_b) / nnx__mwc
    zmqbo__wwu = mean_b - mean_a
    mvw__tprjq = (ssqdm_a + ssqdm_b + zmqbo__wwu * zmqbo__wwu * nobs_a *
        nobs_b / nnx__mwc)
    return mvw__tprjq, reg__jqr, nnx__mwc


def __special_combine(*args):
    return


@infer_global(__special_combine)
class SpecialCombineTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *unliteral_all(args))


@lower_builtin(__special_combine, types.VarArg(types.Any))
def lower_special_combine(context, builder, sig, args):
    return context.get_dummy_value()


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_key_vars, df_out_vars, df_in_vars, key_arrs, input_has_index,
        same_index, return_key, loc, func_name, dropna=True, pivot_arr=None,
        pivot_values=None, is_crosstab=False):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_key_vars = out_key_vars
        self.df_out_vars = df_out_vars
        self.df_in_vars = df_in_vars
        self.key_arrs = key_arrs
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self.pivot_arr = pivot_arr
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab

    def __repr__(self):
        eagpy__tne = ''
        for vvop__iea, ogrc__sbeil in self.df_out_vars.items():
            eagpy__tne += "'{}':{}, ".format(vvop__iea, ogrc__sbeil.name)
        rycau__jrozf = '{}{{{}}}'.format(self.df_out, eagpy__tne)
        ksigw__imhm = ''
        for vvop__iea, ogrc__sbeil in self.df_in_vars.items():
            ksigw__imhm += "'{}':{}, ".format(vvop__iea, ogrc__sbeil.name)
        rqcov__qrrru = '{}{{{}}}'.format(self.df_in, ksigw__imhm)
        zay__nfko = 'pivot {}:{}'.format(self.pivot_arr.name, self.pivot_values
            ) if self.pivot_arr is not None else ''
        key_names = ','.join([str(pqq__rwwpn) for pqq__rwwpn in self.key_names]
            )
        qoqhh__zaz = ','.join([ogrc__sbeil.name for ogrc__sbeil in self.
            key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(rycau__jrozf,
            rqcov__qrrru, key_names, qoqhh__zaz, zay__nfko)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        ghwr__caef, injtb__pmakj = self.gb_info_out.pop(out_col_name)
        if ghwr__caef is None and not self.is_crosstab:
            return
        vliv__qmd = self.gb_info_in[ghwr__caef]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for xkuzm__ijkx, (func, eagpy__tne) in enumerate(vliv__qmd):
                try:
                    eagpy__tne.remove(out_col_name)
                    if len(eagpy__tne) == 0:
                        vliv__qmd.pop(xkuzm__ijkx)
                        break
                except ValueError as kjf__fnozd:
                    continue
        else:
            for xkuzm__ijkx, (func, uwne__ssdt) in enumerate(vliv__qmd):
                if uwne__ssdt == out_col_name:
                    vliv__qmd.pop(xkuzm__ijkx)
                    break
        if len(vliv__qmd) == 0:
            self.gb_info_in.pop(ghwr__caef)
            self.df_in_vars.pop(ghwr__caef)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({ogrc__sbeil.name for ogrc__sbeil in aggregate_node.
        key_arrs})
    use_set.update({ogrc__sbeil.name for ogrc__sbeil in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({ogrc__sbeil.name for ogrc__sbeil in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({ogrc__sbeil.name for ogrc__sbeil in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    vutg__gbh = [nfnv__evzjo for nfnv__evzjo, rbet__esf in aggregate_node.
        df_out_vars.items() if rbet__esf.name not in lives]
    for yvht__hdi in vutg__gbh:
        aggregate_node.remove_out_col(yvht__hdi)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(ogrc__sbeil.name not in lives for
        ogrc__sbeil in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    egzqt__lqxj = set(ogrc__sbeil.name for ogrc__sbeil in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        egzqt__lqxj.update({ogrc__sbeil.name for ogrc__sbeil in
            aggregate_node.out_key_vars})
    return set(), egzqt__lqxj


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for xkuzm__ijkx in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[xkuzm__ijkx] = replace_vars_inner(
            aggregate_node.key_arrs[xkuzm__ijkx], var_dict)
    for nfnv__evzjo in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[nfnv__evzjo] = replace_vars_inner(
            aggregate_node.df_in_vars[nfnv__evzjo], var_dict)
    for nfnv__evzjo in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[nfnv__evzjo] = replace_vars_inner(
            aggregate_node.df_out_vars[nfnv__evzjo], var_dict)
    if aggregate_node.out_key_vars is not None:
        for xkuzm__ijkx in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[xkuzm__ijkx] = replace_vars_inner(
                aggregate_node.out_key_vars[xkuzm__ijkx], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for xkuzm__ijkx in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[xkuzm__ijkx] = visit_vars_inner(aggregate_node
            .key_arrs[xkuzm__ijkx], callback, cbdata)
    for nfnv__evzjo in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[nfnv__evzjo] = visit_vars_inner(
            aggregate_node.df_in_vars[nfnv__evzjo], callback, cbdata)
    for nfnv__evzjo in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[nfnv__evzjo] = visit_vars_inner(
            aggregate_node.df_out_vars[nfnv__evzjo], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for xkuzm__ijkx in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[xkuzm__ijkx] = visit_vars_inner(
                aggregate_node.out_key_vars[xkuzm__ijkx], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    cgj__yto = []
    for rssfq__qzqb in aggregate_node.key_arrs:
        nwf__fyfe = equiv_set.get_shape(rssfq__qzqb)
        if nwf__fyfe:
            cgj__yto.append(nwf__fyfe[0])
    if aggregate_node.pivot_arr is not None:
        nwf__fyfe = equiv_set.get_shape(aggregate_node.pivot_arr)
        if nwf__fyfe:
            cgj__yto.append(nwf__fyfe[0])
    for rbet__esf in aggregate_node.df_in_vars.values():
        nwf__fyfe = equiv_set.get_shape(rbet__esf)
        if nwf__fyfe:
            cgj__yto.append(nwf__fyfe[0])
    if len(cgj__yto) > 1:
        equiv_set.insert_equiv(*cgj__yto)
    muspb__kqo = []
    cgj__yto = []
    yam__ewhi = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        yam__ewhi.extend(aggregate_node.out_key_vars)
    for rbet__esf in yam__ewhi:
        wtlfu__zlr = typemap[rbet__esf.name]
        axsf__nwly = array_analysis._gen_shape_call(equiv_set, rbet__esf,
            wtlfu__zlr.ndim, None, muspb__kqo)
        equiv_set.insert_equiv(rbet__esf, axsf__nwly)
        cgj__yto.append(axsf__nwly[0])
        equiv_set.define(rbet__esf, set())
    if len(cgj__yto) > 1:
        equiv_set.insert_equiv(*cgj__yto)
    return [], muspb__kqo


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    xiomd__ixfmi = Distribution.OneD
    for rbet__esf in aggregate_node.df_in_vars.values():
        xiomd__ixfmi = Distribution(min(xiomd__ixfmi.value, array_dists[
            rbet__esf.name].value))
    for rssfq__qzqb in aggregate_node.key_arrs:
        xiomd__ixfmi = Distribution(min(xiomd__ixfmi.value, array_dists[
            rssfq__qzqb.name].value))
    if aggregate_node.pivot_arr is not None:
        xiomd__ixfmi = Distribution(min(xiomd__ixfmi.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = xiomd__ixfmi
    for rbet__esf in aggregate_node.df_in_vars.values():
        array_dists[rbet__esf.name] = xiomd__ixfmi
    for rssfq__qzqb in aggregate_node.key_arrs:
        array_dists[rssfq__qzqb.name] = xiomd__ixfmi
    dltk__oqak = Distribution.OneD_Var
    for rbet__esf in aggregate_node.df_out_vars.values():
        if rbet__esf.name in array_dists:
            dltk__oqak = Distribution(min(dltk__oqak.value, array_dists[
                rbet__esf.name].value))
    if aggregate_node.out_key_vars is not None:
        for rbet__esf in aggregate_node.out_key_vars:
            if rbet__esf.name in array_dists:
                dltk__oqak = Distribution(min(dltk__oqak.value, array_dists
                    [rbet__esf.name].value))
    dltk__oqak = Distribution(min(dltk__oqak.value, xiomd__ixfmi.value))
    for rbet__esf in aggregate_node.df_out_vars.values():
        array_dists[rbet__esf.name] = dltk__oqak
    if aggregate_node.out_key_vars is not None:
        for ojeqf__skywi in aggregate_node.out_key_vars:
            array_dists[ojeqf__skywi.name] = dltk__oqak
    if dltk__oqak != Distribution.OneD_Var:
        for rssfq__qzqb in aggregate_node.key_arrs:
            array_dists[rssfq__qzqb.name] = dltk__oqak
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = dltk__oqak
        for rbet__esf in aggregate_node.df_in_vars.values():
            array_dists[rbet__esf.name] = dltk__oqak


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for rbet__esf in agg_node.df_out_vars.values():
        definitions[rbet__esf.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for ojeqf__skywi in agg_node.out_key_vars:
            definitions[ojeqf__skywi.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for ogrc__sbeil in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[ogrc__sbeil.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                ogrc__sbeil.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    rcfm__dsk = tuple(typemap[ogrc__sbeil.name] for ogrc__sbeil in agg_node
        .key_arrs)
    mkrp__oohm = [ogrc__sbeil for hjmve__ain, ogrc__sbeil in agg_node.
        df_in_vars.items()]
    sms__pghw = [ogrc__sbeil for hjmve__ain, ogrc__sbeil in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    bul__vyxhn = []
    if agg_node.pivot_arr is not None:
        for ghwr__caef, vliv__qmd in agg_node.gb_info_in.items():
            for func, injtb__pmakj in vliv__qmd:
                if ghwr__caef is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        ghwr__caef].name])
                bul__vyxhn.append(func)
    else:
        for ghwr__caef, func in agg_node.gb_info_out.values():
            if ghwr__caef is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[ghwr__caef].
                    name])
            bul__vyxhn.append(func)
    out_col_typs = tuple(typemap[ogrc__sbeil.name] for ogrc__sbeil in sms__pghw
        )
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(rcfm__dsk + tuple(typemap[ogrc__sbeil.name] for
        ogrc__sbeil in mkrp__oohm) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    vzgp__ano = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for xkuzm__ijkx, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            vzgp__ano.update({f'in_cat_dtype_{xkuzm__ijkx}': in_col_typ})
    for xkuzm__ijkx, phmal__tkwlo in enumerate(out_col_typs):
        if isinstance(phmal__tkwlo, bodo.CategoricalArrayType):
            vzgp__ano.update({f'out_cat_dtype_{xkuzm__ijkx}': phmal__tkwlo})
    udf_func_struct = get_udf_func_struct(bul__vyxhn, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    jzs__zovit = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    vzgp__ano.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate,
        'pivot_groupby_and_aggregate': pivot_groupby_and_aggregate,
        'info_from_table': info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decode_if_dict_array': decode_if_dict_array, 'out_typs': out_col_typs}
        )
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            vzgp__ano.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            vzgp__ano.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    rre__jibdo = compile_to_numba_ir(jzs__zovit, vzgp__ano, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    lnoac__ssr = []
    if agg_node.pivot_arr is None:
        oxpm__hcpz = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        cve__mvul = ir.Var(oxpm__hcpz, mk_unique_var('dummy_none'), loc)
        typemap[cve__mvul.name] = types.none
        lnoac__ssr.append(ir.Assign(ir.Const(None, loc), cve__mvul, loc))
        mkrp__oohm.append(cve__mvul)
    else:
        mkrp__oohm.append(agg_node.pivot_arr)
    replace_arg_nodes(rre__jibdo, agg_node.key_arrs + mkrp__oohm)
    qpe__uohw = rre__jibdo.body[-3]
    assert is_assign(qpe__uohw) and isinstance(qpe__uohw.value, ir.Expr
        ) and qpe__uohw.value.op == 'build_tuple'
    lnoac__ssr += rre__jibdo.body[:-3]
    yam__ewhi = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        yam__ewhi += agg_node.out_key_vars
    for xkuzm__ijkx, sfl__stdi in enumerate(yam__ewhi):
        kuue__mjgmi = qpe__uohw.value.items[xkuzm__ijkx]
        lnoac__ssr.append(ir.Assign(kuue__mjgmi, sfl__stdi, sfl__stdi.loc))
    return lnoac__ssr


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        tqjt__nbch = args[0]
        dtype = types.Tuple([t.dtype for t in tqjt__nbch.types]) if isinstance(
            tqjt__nbch, types.BaseTuple) else tqjt__nbch.dtype
        if isinstance(tqjt__nbch, types.BaseTuple) and len(tqjt__nbch.types
            ) == 1:
            dtype = tqjt__nbch.types[0].dtype
        return signature(types.Set(dtype), *args)


@lower_builtin(get_numba_set, types.Any)
def lower_get_numba_set(context, builder, sig, args):
    return numba.cpython.setobj.set_empty_constructor(context, builder, sig,
        args)


@infer_global(bool)
class BoolNoneTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        zcmh__soi = args[0]
        if zcmh__soi == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    vllz__bbukm = context.compile_internal(builder, lambda a: False, sig, args)
    return vllz__bbukm


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        puu__avid = IntDtype(t.dtype).name
        assert puu__avid.endswith('Dtype()')
        puu__avid = puu__avid[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{puu__avid}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        ilgqt__gvo = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {ilgqt__gvo}_cat_dtype_{colnum})')
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    out_data_typs, do_combine, func_idx_to_in_col, label_suffix):
    wokm__twkrp = udf_func_struct.var_typs
    xvaa__qsmh = len(wokm__twkrp)
    xuh__moy = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    xuh__moy += '    if is_null_pointer(in_table):\n'
    xuh__moy += '        return\n'
    xuh__moy += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in wokm__twkrp]), 
        ',' if len(wokm__twkrp) == 1 else '')
    eho__bks = n_keys
    aacl__ahqc = []
    redvar_offsets = []
    vhkls__coxpm = []
    if do_combine:
        for xkuzm__ijkx, pdb__ayg in enumerate(allfuncs):
            if pdb__ayg.ftype != 'udf':
                eho__bks += pdb__ayg.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(eho__bks, eho__bks + pdb__ayg.
                    n_redvars))
                eho__bks += pdb__ayg.n_redvars
                vhkls__coxpm.append(data_in_typs_[func_idx_to_in_col[
                    xkuzm__ijkx]])
                aacl__ahqc.append(func_idx_to_in_col[xkuzm__ijkx] + n_keys)
    else:
        for xkuzm__ijkx, pdb__ayg in enumerate(allfuncs):
            if pdb__ayg.ftype != 'udf':
                eho__bks += pdb__ayg.ncols_post_shuffle
            else:
                redvar_offsets += list(range(eho__bks + 1, eho__bks + 1 +
                    pdb__ayg.n_redvars))
                eho__bks += pdb__ayg.n_redvars + 1
                vhkls__coxpm.append(data_in_typs_[func_idx_to_in_col[
                    xkuzm__ijkx]])
                aacl__ahqc.append(func_idx_to_in_col[xkuzm__ijkx] + n_keys)
    assert len(redvar_offsets) == xvaa__qsmh
    jija__juod = len(vhkls__coxpm)
    bjt__cjtx = []
    for xkuzm__ijkx, t in enumerate(vhkls__coxpm):
        bjt__cjtx.append(_gen_dummy_alloc(t, xkuzm__ijkx, True))
    xuh__moy += '    data_in_dummy = ({}{})\n'.format(','.join(bjt__cjtx), 
        ',' if len(vhkls__coxpm) == 1 else '')
    xuh__moy += """
    # initialize redvar cols
"""
    xuh__moy += '    init_vals = __init_func()\n'
    for xkuzm__ijkx in range(xvaa__qsmh):
        xuh__moy += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(xkuzm__ijkx, redvar_offsets[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(redvar_arr_{})\n'.format(xkuzm__ijkx)
        xuh__moy += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            xkuzm__ijkx, xkuzm__ijkx)
    xuh__moy += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(xkuzm__ijkx) for xkuzm__ijkx in range(xvaa__qsmh)]), ',' if 
        xvaa__qsmh == 1 else '')
    xuh__moy += '\n'
    for xkuzm__ijkx in range(jija__juod):
        xuh__moy += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(xkuzm__ijkx, aacl__ahqc[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(data_in_{})\n'.format(xkuzm__ijkx)
    xuh__moy += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(xkuzm__ijkx) for xkuzm__ijkx in range(jija__juod)]), ',' if 
        jija__juod == 1 else '')
    xuh__moy += '\n'
    xuh__moy += '    for i in range(len(data_in_0)):\n'
    xuh__moy += '        w_ind = row_to_group[i]\n'
    xuh__moy += '        if w_ind != -1:\n'
    xuh__moy += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    eyz__eaki = {}
    exec(xuh__moy, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, eyz__eaki)
    return eyz__eaki['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    wokm__twkrp = udf_func_struct.var_typs
    xvaa__qsmh = len(wokm__twkrp)
    xuh__moy = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    xuh__moy += '    if is_null_pointer(in_table):\n'
    xuh__moy += '        return\n'
    xuh__moy += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in wokm__twkrp]), 
        ',' if len(wokm__twkrp) == 1 else '')
    tcz__repzz = n_keys
    ubo__ioir = n_keys
    dili__enr = []
    mnk__saj = []
    for pdb__ayg in allfuncs:
        if pdb__ayg.ftype != 'udf':
            tcz__repzz += pdb__ayg.ncols_pre_shuffle
            ubo__ioir += pdb__ayg.ncols_post_shuffle
        else:
            dili__enr += list(range(tcz__repzz, tcz__repzz + pdb__ayg.
                n_redvars))
            mnk__saj += list(range(ubo__ioir + 1, ubo__ioir + 1 + pdb__ayg.
                n_redvars))
            tcz__repzz += pdb__ayg.n_redvars
            ubo__ioir += 1 + pdb__ayg.n_redvars
    assert len(dili__enr) == xvaa__qsmh
    xuh__moy += """
    # initialize redvar cols
"""
    xuh__moy += '    init_vals = __init_func()\n'
    for xkuzm__ijkx in range(xvaa__qsmh):
        xuh__moy += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(xkuzm__ijkx, mnk__saj[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(redvar_arr_{})\n'.format(xkuzm__ijkx)
        xuh__moy += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            xkuzm__ijkx, xkuzm__ijkx)
    xuh__moy += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(xkuzm__ijkx) for xkuzm__ijkx in range(xvaa__qsmh)]), ',' if 
        xvaa__qsmh == 1 else '')
    xuh__moy += '\n'
    for xkuzm__ijkx in range(xvaa__qsmh):
        xuh__moy += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(xkuzm__ijkx, dili__enr[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(recv_redvar_arr_{})\n'.format(xkuzm__ijkx)
    xuh__moy += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(xkuzm__ijkx) for xkuzm__ijkx in range(
        xvaa__qsmh)]), ',' if xvaa__qsmh == 1 else '')
    xuh__moy += '\n'
    if xvaa__qsmh:
        xuh__moy += '    for i in range(len(recv_redvar_arr_0)):\n'
        xuh__moy += '        w_ind = row_to_group[i]\n'
        xuh__moy += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)\n'
            )
    eyz__eaki = {}
    exec(xuh__moy, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, eyz__eaki)
    return eyz__eaki['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    wokm__twkrp = udf_func_struct.var_typs
    xvaa__qsmh = len(wokm__twkrp)
    eho__bks = n_keys
    redvar_offsets = []
    qca__dguiq = []
    out_data_typs = []
    for xkuzm__ijkx, pdb__ayg in enumerate(allfuncs):
        if pdb__ayg.ftype != 'udf':
            eho__bks += pdb__ayg.ncols_post_shuffle
        else:
            qca__dguiq.append(eho__bks)
            redvar_offsets += list(range(eho__bks + 1, eho__bks + 1 +
                pdb__ayg.n_redvars))
            eho__bks += 1 + pdb__ayg.n_redvars
            out_data_typs.append(out_data_typs_[xkuzm__ijkx])
    assert len(redvar_offsets) == xvaa__qsmh
    jija__juod = len(out_data_typs)
    xuh__moy = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    xuh__moy += '    if is_null_pointer(table):\n'
    xuh__moy += '        return\n'
    xuh__moy += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in wokm__twkrp]), 
        ',' if len(wokm__twkrp) == 1 else '')
    xuh__moy += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for xkuzm__ijkx in range(xvaa__qsmh):
        xuh__moy += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(xkuzm__ijkx, redvar_offsets[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(redvar_arr_{})\n'.format(xkuzm__ijkx)
    xuh__moy += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(xkuzm__ijkx) for xkuzm__ijkx in range(xvaa__qsmh)]), ',' if 
        xvaa__qsmh == 1 else '')
    xuh__moy += '\n'
    for xkuzm__ijkx in range(jija__juod):
        xuh__moy += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(xkuzm__ijkx, qca__dguiq[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(data_out_{})\n'.format(xkuzm__ijkx)
    xuh__moy += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(xkuzm__ijkx) for xkuzm__ijkx in range(jija__juod)]), ',' if 
        jija__juod == 1 else '')
    xuh__moy += '\n'
    xuh__moy += '    for i in range(len(data_out_0)):\n'
    xuh__moy += '        __eval_res(redvars, data_out, i)\n'
    eyz__eaki = {}
    exec(xuh__moy, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, eyz__eaki)
    return eyz__eaki['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    eho__bks = n_keys
    xiyx__zjxjz = []
    for xkuzm__ijkx, pdb__ayg in enumerate(allfuncs):
        if pdb__ayg.ftype == 'gen_udf':
            xiyx__zjxjz.append(eho__bks)
            eho__bks += 1
        elif pdb__ayg.ftype != 'udf':
            eho__bks += pdb__ayg.ncols_post_shuffle
        else:
            eho__bks += pdb__ayg.n_redvars + 1
    xuh__moy = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    xuh__moy += '    if num_groups == 0:\n'
    xuh__moy += '        return\n'
    for xkuzm__ijkx, func in enumerate(udf_func_struct.general_udf_funcs):
        xuh__moy += '    # col {}\n'.format(xkuzm__ijkx)
        xuh__moy += (
            '    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)\n'
            .format(xiyx__zjxjz[xkuzm__ijkx], xkuzm__ijkx))
        xuh__moy += '    incref(out_col)\n'
        xuh__moy += '    for j in range(num_groups):\n'
        xuh__moy += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(xkuzm__ijkx, xkuzm__ijkx))
        xuh__moy += '        incref(in_col)\n'
        xuh__moy += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(xkuzm__ijkx))
    vzgp__ano = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    hspzw__yqrxr = 0
    for xkuzm__ijkx, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[hspzw__yqrxr]
        vzgp__ano['func_{}'.format(hspzw__yqrxr)] = func
        vzgp__ano['in_col_{}_typ'.format(hspzw__yqrxr)] = in_col_typs[
            func_idx_to_in_col[xkuzm__ijkx]]
        vzgp__ano['out_col_{}_typ'.format(hspzw__yqrxr)] = out_col_typs[
            xkuzm__ijkx]
        hspzw__yqrxr += 1
    eyz__eaki = {}
    exec(xuh__moy, vzgp__ano, eyz__eaki)
    pdb__ayg = eyz__eaki['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    tgra__eupvc = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(tgra__eupvc, nopython=True)(pdb__ayg)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    oiey__nhcwc = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        swt__npln = 1
    else:
        swt__npln = len(agg_node.pivot_values)
    uqluq__wlz = tuple('key_' + sanitize_varname(vvop__iea) for vvop__iea in
        agg_node.key_names)
    jnlw__ppkh = {vvop__iea: 'in_{}'.format(sanitize_varname(vvop__iea)) for
        vvop__iea in agg_node.gb_info_in.keys() if vvop__iea is not None}
    csq__cqa = {vvop__iea: ('out_' + sanitize_varname(vvop__iea)) for
        vvop__iea in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    rqqni__aoij = ', '.join(uqluq__wlz)
    nbnh__tezm = ', '.join(jnlw__ppkh.values())
    if nbnh__tezm != '':
        nbnh__tezm = ', ' + nbnh__tezm
    xuh__moy = 'def agg_top({}{}{}, pivot_arr):\n'.format(rqqni__aoij,
        nbnh__tezm, ', index_arg' if agg_node.input_has_index else '')
    for a in (uqluq__wlz + tuple(jnlw__ppkh.values())):
        xuh__moy += f'    {a} = decode_if_dict_array({a})\n'
    if oiey__nhcwc:
        xuh__moy += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        kpq__hdn = []
        for ghwr__caef, vliv__qmd in agg_node.gb_info_in.items():
            if ghwr__caef is not None:
                for func, injtb__pmakj in vliv__qmd:
                    kpq__hdn.append(jnlw__ppkh[ghwr__caef])
    else:
        kpq__hdn = tuple(jnlw__ppkh[ghwr__caef] for ghwr__caef,
            injtb__pmakj in agg_node.gb_info_out.values() if ghwr__caef is not
            None)
    dbzg__fyo = uqluq__wlz + tuple(kpq__hdn)
    xuh__moy += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in dbzg__fyo), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    xuh__moy += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    bla__aomj = []
    func_idx_to_in_col = []
    see__slsjz = []
    nkffc__osr = False
    iiud__hqct = 1
    szozb__kzmr = -1
    dzao__gflmp = 0
    yhelp__dajxk = 0
    if not oiey__nhcwc:
        bul__vyxhn = [func for injtb__pmakj, func in agg_node.gb_info_out.
            values()]
    else:
        bul__vyxhn = [func for func, injtb__pmakj in vliv__qmd for
            vliv__qmd in agg_node.gb_info_in.values()]
    for mdlnf__nbdqu, func in enumerate(bul__vyxhn):
        bla__aomj.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            dzao__gflmp += 1
        if hasattr(func, 'skipdropna'):
            nkffc__osr = func.skipdropna
        if func.ftype == 'shift':
            iiud__hqct = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            yhelp__dajxk = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            szozb__kzmr = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(mdlnf__nbdqu)
        if func.ftype == 'udf':
            see__slsjz.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            see__slsjz.append(0)
            do_combine = False
    bla__aomj.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == swt__npln, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * swt__npln, 'invalid number of groupby outputs'
    if dzao__gflmp > 0:
        if dzao__gflmp != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for xkuzm__ijkx, vvop__iea in enumerate(agg_node.gb_info_out.keys()):
        dtl__ssvb = csq__cqa[vvop__iea] + '_dummy'
        phmal__tkwlo = out_col_typs[xkuzm__ijkx]
        ghwr__caef, func = agg_node.gb_info_out[vvop__iea]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(phmal__tkwlo, bodo.
            CategoricalArrayType):
            xuh__moy += '    {} = {}\n'.format(dtl__ssvb, jnlw__ppkh[
                ghwr__caef])
        elif udf_func_struct is not None:
            xuh__moy += '    {} = {}\n'.format(dtl__ssvb, _gen_dummy_alloc(
                phmal__tkwlo, xkuzm__ijkx, False))
    if udf_func_struct is not None:
        rtoqb__ltt = next_label()
        if udf_func_struct.regular_udfs:
            tgra__eupvc = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            aae__cbazy = numba.cfunc(tgra__eupvc, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, rtoqb__ltt))
            qil__ciy = numba.cfunc(tgra__eupvc, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, rtoqb__ltt))
            ouecd__sqp = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                rtoqb__ltt))
            udf_func_struct.set_regular_cfuncs(aae__cbazy, qil__ciy, ouecd__sqp
                )
            for pyqaf__mzqc in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[pyqaf__mzqc.native_name] = pyqaf__mzqc
                gb_agg_cfunc_addr[pyqaf__mzqc.native_name
                    ] = pyqaf__mzqc.address
        if udf_func_struct.general_udfs:
            lrod__jjxp = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                rtoqb__ltt)
            udf_func_struct.set_general_cfunc(lrod__jjxp)
        tipgt__khcmi = []
        mds__ppgid = 0
        xkuzm__ijkx = 0
        for dtl__ssvb, pdb__ayg in zip(csq__cqa.values(), allfuncs):
            if pdb__ayg.ftype in ('udf', 'gen_udf'):
                tipgt__khcmi.append(dtl__ssvb + '_dummy')
                for ylmzr__aynhc in range(mds__ppgid, mds__ppgid +
                    see__slsjz[xkuzm__ijkx]):
                    tipgt__khcmi.append('data_redvar_dummy_' + str(
                        ylmzr__aynhc))
                mds__ppgid += see__slsjz[xkuzm__ijkx]
                xkuzm__ijkx += 1
        if udf_func_struct.regular_udfs:
            wokm__twkrp = udf_func_struct.var_typs
            for xkuzm__ijkx, t in enumerate(wokm__twkrp):
                xuh__moy += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(xkuzm__ijkx, _get_np_dtype(t)))
        xuh__moy += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in tipgt__khcmi))
        xuh__moy += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            xuh__moy += "    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".format(
                aae__cbazy.native_name)
            xuh__moy += "    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".format(
                qil__ciy.native_name)
            xuh__moy += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                ouecd__sqp.native_name)
            xuh__moy += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(aae__cbazy.native_name))
            xuh__moy += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(qil__ciy.native_name))
            xuh__moy += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n".
                format(ouecd__sqp.native_name))
        else:
            xuh__moy += '    cpp_cb_update_addr = 0\n'
            xuh__moy += '    cpp_cb_combine_addr = 0\n'
            xuh__moy += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            pyqaf__mzqc = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[pyqaf__mzqc.native_name] = pyqaf__mzqc
            gb_agg_cfunc_addr[pyqaf__mzqc.native_name] = pyqaf__mzqc.address
            xuh__moy += "    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".format(
                pyqaf__mzqc.native_name)
            xuh__moy += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(pyqaf__mzqc.native_name))
        else:
            xuh__moy += '    cpp_cb_general_addr = 0\n'
    else:
        xuh__moy += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        xuh__moy += '    cpp_cb_update_addr = 0\n'
        xuh__moy += '    cpp_cb_combine_addr = 0\n'
        xuh__moy += '    cpp_cb_eval_addr = 0\n'
        xuh__moy += '    cpp_cb_general_addr = 0\n'
    xuh__moy += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(pdb__ayg.ftype)) for pdb__ayg in
        allfuncs] + ['0']))
    xuh__moy += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(str
        (bla__aomj))
    if len(see__slsjz) > 0:
        xuh__moy += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(str
            (see__slsjz))
    else:
        xuh__moy += '    udf_ncols = np.array([0], np.int32)\n'
    if oiey__nhcwc:
        xuh__moy += '    arr_type = coerce_to_array({})\n'.format(agg_node.
            pivot_values)
        xuh__moy += '    arr_info = array_to_info(arr_type)\n'
        xuh__moy += '    dispatch_table = arr_info_list_to_table([arr_info])\n'
        xuh__moy += '    pivot_info = array_to_info(pivot_arr)\n'
        xuh__moy += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        xuh__moy += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, nkffc__osr, agg_node.return_key, agg_node.same_index))
        xuh__moy += '    delete_info_decref_array(pivot_info)\n'
        xuh__moy += '    delete_info_decref_array(arr_info)\n'
    else:
        xuh__moy += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, nkffc__osr,
            iiud__hqct, yhelp__dajxk, szozb__kzmr, agg_node.return_key,
            agg_node.same_index, agg_node.dropna))
    fzk__qxsnp = 0
    if agg_node.return_key:
        for xkuzm__ijkx, maker__xqr in enumerate(uqluq__wlz):
            xuh__moy += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(maker__xqr, fzk__qxsnp, maker__xqr))
            fzk__qxsnp += 1
    for xkuzm__ijkx, dtl__ssvb in enumerate(csq__cqa.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(phmal__tkwlo, bodo.
            CategoricalArrayType):
            xuh__moy += f"""    {dtl__ssvb} = info_to_array(info_from_table(out_table, {fzk__qxsnp}), {dtl__ssvb + '_dummy'})
"""
        else:
            xuh__moy += f"""    {dtl__ssvb} = info_to_array(info_from_table(out_table, {fzk__qxsnp}), out_typs[{xkuzm__ijkx}])
"""
        fzk__qxsnp += 1
    if agg_node.same_index:
        xuh__moy += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(fzk__qxsnp))
        fzk__qxsnp += 1
    xuh__moy += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    xuh__moy += '    delete_table_decref_arrays(table)\n'
    xuh__moy += '    delete_table_decref_arrays(udf_table_dummy)\n'
    xuh__moy += '    delete_table(out_table)\n'
    xuh__moy += f'    ev_clean.finalize()\n'
    kgkf__czbmd = tuple(csq__cqa.values())
    if agg_node.return_key:
        kgkf__czbmd += tuple(uqluq__wlz)
    xuh__moy += '    return ({},{})\n'.format(', '.join(kgkf__czbmd), 
        ' out_index_arg,' if agg_node.same_index else '')
    eyz__eaki = {}
    exec(xuh__moy, {'out_typs': out_col_typs}, eyz__eaki)
    xaurj__lqjuu = eyz__eaki['agg_top']
    return xaurj__lqjuu


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for akgn__hpavo in block.body:
            if is_call_assign(akgn__hpavo) and find_callname(f_ir,
                akgn__hpavo.value) == ('len', 'builtins'
                ) and akgn__hpavo.value.args[0].name == f_ir.arg_names[0]:
                mpxp__ggk = get_definition(f_ir, akgn__hpavo.value.func)
                mpxp__ggk.name = 'dummy_agg_count'
                mpxp__ggk.value = dummy_agg_count
    ysq__edca = get_name_var_table(f_ir.blocks)
    xnmsc__wkqk = {}
    for name, injtb__pmakj in ysq__edca.items():
        xnmsc__wkqk[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, xnmsc__wkqk)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    eoafo__qel = numba.core.compiler.Flags()
    eoafo__qel.nrt = True
    fhro__muknm = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, eoafo__qel)
    fhro__muknm.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, wpsyd__qdcvv, calltypes, injtb__pmakj = (numba.core.
        typed_passes.type_inference_stage(typingctx, targetctx, f_ir,
        arg_typs, None))
    phft__qfhm = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    zrb__lsl = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    omfhz__neoz = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    xokd__iyr = omfhz__neoz(typemap, calltypes)
    pm = zrb__lsl(typingctx, targetctx, None, f_ir, typemap, wpsyd__qdcvv,
        calltypes, xokd__iyr, {}, eoafo__qel, None)
    lroxl__iywy = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = zrb__lsl(typingctx, targetctx, None, f_ir, typemap, wpsyd__qdcvv,
        calltypes, xokd__iyr, {}, eoafo__qel, lroxl__iywy)
    sgrzo__bwhw = numba.core.typed_passes.InlineOverloads()
    sgrzo__bwhw.run_pass(pm)
    azx__kipxq = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    azx__kipxq.run()
    for block in f_ir.blocks.values():
        for akgn__hpavo in block.body:
            if is_assign(akgn__hpavo) and isinstance(akgn__hpavo.value, (ir
                .Arg, ir.Var)) and isinstance(typemap[akgn__hpavo.target.
                name], SeriesType):
                wtlfu__zlr = typemap.pop(akgn__hpavo.target.name)
                typemap[akgn__hpavo.target.name] = wtlfu__zlr.data
            if is_call_assign(akgn__hpavo) and find_callname(f_ir,
                akgn__hpavo.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[akgn__hpavo.target.name].remove(akgn__hpavo
                    .value)
                akgn__hpavo.value = akgn__hpavo.value.args[0]
                f_ir._definitions[akgn__hpavo.target.name].append(akgn__hpavo
                    .value)
            if is_call_assign(akgn__hpavo) and find_callname(f_ir,
                akgn__hpavo.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[akgn__hpavo.target.name].remove(akgn__hpavo
                    .value)
                akgn__hpavo.value = ir.Const(False, akgn__hpavo.loc)
                f_ir._definitions[akgn__hpavo.target.name].append(akgn__hpavo
                    .value)
            if is_call_assign(akgn__hpavo) and find_callname(f_ir,
                akgn__hpavo.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[akgn__hpavo.target.name].remove(akgn__hpavo
                    .value)
                akgn__hpavo.value = ir.Const(False, akgn__hpavo.loc)
                f_ir._definitions[akgn__hpavo.target.name].append(akgn__hpavo
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    wxa__younp = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, phft__qfhm)
    wxa__younp.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    kssk__jqqcd = numba.core.compiler.StateDict()
    kssk__jqqcd.func_ir = f_ir
    kssk__jqqcd.typemap = typemap
    kssk__jqqcd.calltypes = calltypes
    kssk__jqqcd.typingctx = typingctx
    kssk__jqqcd.targetctx = targetctx
    kssk__jqqcd.return_type = wpsyd__qdcvv
    numba.core.rewrites.rewrite_registry.apply('after-inference', kssk__jqqcd)
    fptqi__ygkoi = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        wpsyd__qdcvv, typingctx, targetctx, phft__qfhm, eoafo__qel, {})
    fptqi__ygkoi.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            ani__htw = ctypes.pythonapi.PyCell_Get
            ani__htw.restype = ctypes.py_object
            ani__htw.argtypes = ctypes.py_object,
            mjd__pjoz = tuple(ani__htw(qqd__rvt) for qqd__rvt in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            mjd__pjoz = closure.items
        assert len(code.co_freevars) == len(mjd__pjoz)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, mjd__pjoz)


class RegularUDFGenerator(object):

    def __init__(self, in_col_types, out_col_types, pivot_typ, pivot_values,
        is_crosstab, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.out_col_types = out_col_types
        self.pivot_typ = pivot_typ
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        vhxp__kuw = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (vhxp__kuw,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        jhw__qljh, arr_var = _rm_arg_agg_block(block, pm.typemap)
        ypo__qwcpi = -1
        for xkuzm__ijkx, akgn__hpavo in enumerate(jhw__qljh):
            if isinstance(akgn__hpavo, numba.parfors.parfor.Parfor):
                assert ypo__qwcpi == -1, 'only one parfor for aggregation function'
                ypo__qwcpi = xkuzm__ijkx
        parfor = None
        if ypo__qwcpi != -1:
            parfor = jhw__qljh[ypo__qwcpi]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = jhw__qljh[:ypo__qwcpi] + parfor.init_block.body
        eval_nodes = jhw__qljh[ypo__qwcpi + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for akgn__hpavo in init_nodes:
            if is_assign(akgn__hpavo) and akgn__hpavo.target.name in redvars:
                ind = redvars.index(akgn__hpavo.target.name)
                reduce_vars[ind] = akgn__hpavo.target
        var_types = [pm.typemap[ogrc__sbeil] for ogrc__sbeil in redvars]
        yyw__dombg = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        hpvx__cgtah = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        qqkli__gko = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(qqkli__gko)
        self.all_update_funcs.append(hpvx__cgtah)
        self.all_combine_funcs.append(yyw__dombg)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        epa__ewbv = gen_init_func(self.all_init_nodes, self.all_reduce_vars,
            self.all_vartypes, self.typingctx, self.targetctx)
        hllf__oqi = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        apbaz__yth = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        oom__oji = gen_all_eval_func(self.all_eval_funcs, self.all_vartypes,
            self.redvar_offsets, self.out_col_types, self.typingctx, self.
            targetctx, self.pivot_values)
        return self.all_vartypes, epa__ewbv, hllf__oqi, apbaz__yth, oom__oji


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, input_has_index, in_col_types,
    out_col_types, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab):
    if is_crosstab and len(in_col_types) == 0:
        in_col_types = [types.Array(types.intp, 1, 'C')]
    xxjr__htri = []
    for t, pdb__ayg in zip(in_col_types, agg_func):
        xxjr__htri.append((t, pdb__ayg))
    lcdyk__lfrnn = RegularUDFGenerator(in_col_types, out_col_types,
        pivot_typ, pivot_values, is_crosstab, typingctx, targetctx)
    ocy__qvwq = GeneralUDFGenerator()
    for in_col_typ, func in xxjr__htri:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            lcdyk__lfrnn.add_udf(in_col_typ, func)
        except:
            ocy__qvwq.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = lcdyk__lfrnn.gen_all_func()
    general_udf_funcs = ocy__qvwq.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    bpa__qni = compute_use_defs(parfor.loop_body)
    lensr__hzlq = set()
    for lzt__ujyf in bpa__qni.usemap.values():
        lensr__hzlq |= lzt__ujyf
    coje__atq = set()
    for lzt__ujyf in bpa__qni.defmap.values():
        coje__atq |= lzt__ujyf
    ezrv__sba = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    ezrv__sba.body = eval_nodes
    fnpsu__nhxup = compute_use_defs({(0): ezrv__sba})
    pnl__uzpyj = fnpsu__nhxup.usemap[0]
    ibqwf__xsn = set()
    mfnj__dfv = []
    cjkj__mnn = []
    for akgn__hpavo in reversed(init_nodes):
        pkmok__pid = {ogrc__sbeil.name for ogrc__sbeil in akgn__hpavo.
            list_vars()}
        if is_assign(akgn__hpavo):
            ogrc__sbeil = akgn__hpavo.target.name
            pkmok__pid.remove(ogrc__sbeil)
            if (ogrc__sbeil in lensr__hzlq and ogrc__sbeil not in
                ibqwf__xsn and ogrc__sbeil not in pnl__uzpyj and 
                ogrc__sbeil not in coje__atq):
                cjkj__mnn.append(akgn__hpavo)
                lensr__hzlq |= pkmok__pid
                coje__atq.add(ogrc__sbeil)
                continue
        ibqwf__xsn |= pkmok__pid
        mfnj__dfv.append(akgn__hpavo)
    cjkj__mnn.reverse()
    mfnj__dfv.reverse()
    rstm__oyzc = min(parfor.loop_body.keys())
    tdx__gsy = parfor.loop_body[rstm__oyzc]
    tdx__gsy.body = cjkj__mnn + tdx__gsy.body
    return mfnj__dfv


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    kev__gzwf = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ngx__pvcg = set()
    uwo__pom = []
    for akgn__hpavo in init_nodes:
        if is_assign(akgn__hpavo) and isinstance(akgn__hpavo.value, ir.Global
            ) and isinstance(akgn__hpavo.value.value, pytypes.FunctionType
            ) and akgn__hpavo.value.value in kev__gzwf:
            ngx__pvcg.add(akgn__hpavo.target.name)
        elif is_call_assign(akgn__hpavo
            ) and akgn__hpavo.value.func.name in ngx__pvcg:
            pass
        else:
            uwo__pom.append(akgn__hpavo)
    init_nodes = uwo__pom
    nmuk__bqoa = types.Tuple(var_types)
    hgtdf__dnhgu = lambda : None
    f_ir = compile_to_numba_ir(hgtdf__dnhgu, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    ooh__dly = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    xnsz__jjxng = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), ooh__dly,
        loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [xnsz__jjxng] + block.body
    block.body[-2].value.value = ooh__dly
    ghhn__cbvgx = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        nmuk__bqoa, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wuylz__feu = numba.core.target_extension.dispatcher_registry[cpu_target](
        hgtdf__dnhgu)
    wuylz__feu.add_overload(ghhn__cbvgx)
    return wuylz__feu


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    nppce__bjjoj = len(update_funcs)
    hutes__dxfz = len(in_col_types)
    if pivot_values is not None:
        assert hutes__dxfz == 1
    xuh__moy = 'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n'
    if pivot_values is not None:
        bfjb__lhrg = redvar_offsets[hutes__dxfz]
        xuh__moy += '  pv = pivot_arr[i]\n'
        for ylmzr__aynhc, ecunk__gbw in enumerate(pivot_values):
            kfgg__xewc = 'el' if ylmzr__aynhc != 0 else ''
            xuh__moy += "  {}if pv == '{}':\n".format(kfgg__xewc, ecunk__gbw)
            lonoq__ugf = bfjb__lhrg * ylmzr__aynhc
            qqed__cbkvs = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                xkuzm__ijkx) for xkuzm__ijkx in range(lonoq__ugf +
                redvar_offsets[0], lonoq__ugf + redvar_offsets[1])])
            zkgru__tkkd = 'data_in[0][i]'
            if is_crosstab:
                zkgru__tkkd = '0'
            xuh__moy += '    {} = update_vars_0({}, {})\n'.format(qqed__cbkvs,
                qqed__cbkvs, zkgru__tkkd)
    else:
        for ylmzr__aynhc in range(nppce__bjjoj):
            qqed__cbkvs = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                xkuzm__ijkx) for xkuzm__ijkx in range(redvar_offsets[
                ylmzr__aynhc], redvar_offsets[ylmzr__aynhc + 1])])
            if qqed__cbkvs:
                xuh__moy += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(qqed__cbkvs, ylmzr__aynhc, qqed__cbkvs, 0 if 
                    hutes__dxfz == 1 else ylmzr__aynhc))
    xuh__moy += '  return\n'
    vzgp__ano = {}
    for xkuzm__ijkx, pdb__ayg in enumerate(update_funcs):
        vzgp__ano['update_vars_{}'.format(xkuzm__ijkx)] = pdb__ayg
    eyz__eaki = {}
    exec(xuh__moy, vzgp__ano, eyz__eaki)
    fmfgu__hdqgo = eyz__eaki['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(fmfgu__hdqgo)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    aiaaq__jqfmt = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    arg_typs = aiaaq__jqfmt, aiaaq__jqfmt, types.intp, types.intp, pivot_typ
    jled__iiwai = len(redvar_offsets) - 1
    bfjb__lhrg = redvar_offsets[jled__iiwai]
    xuh__moy = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert jled__iiwai == 1
        for pqq__rwwpn in range(len(pivot_values)):
            lonoq__ugf = bfjb__lhrg * pqq__rwwpn
            qqed__cbkvs = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                xkuzm__ijkx) for xkuzm__ijkx in range(lonoq__ugf +
                redvar_offsets[0], lonoq__ugf + redvar_offsets[1])])
            emaj__fjasp = ', '.join(['recv_arrs[{}][i]'.format(xkuzm__ijkx) for
                xkuzm__ijkx in range(lonoq__ugf + redvar_offsets[0], 
                lonoq__ugf + redvar_offsets[1])])
            xuh__moy += '  {} = combine_vars_0({}, {})\n'.format(qqed__cbkvs,
                qqed__cbkvs, emaj__fjasp)
    else:
        for ylmzr__aynhc in range(jled__iiwai):
            qqed__cbkvs = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                xkuzm__ijkx) for xkuzm__ijkx in range(redvar_offsets[
                ylmzr__aynhc], redvar_offsets[ylmzr__aynhc + 1])])
            emaj__fjasp = ', '.join(['recv_arrs[{}][i]'.format(xkuzm__ijkx) for
                xkuzm__ijkx in range(redvar_offsets[ylmzr__aynhc],
                redvar_offsets[ylmzr__aynhc + 1])])
            if emaj__fjasp:
                xuh__moy += '  {} = combine_vars_{}({}, {})\n'.format(
                    qqed__cbkvs, ylmzr__aynhc, qqed__cbkvs, emaj__fjasp)
    xuh__moy += '  return\n'
    vzgp__ano = {}
    for xkuzm__ijkx, pdb__ayg in enumerate(combine_funcs):
        vzgp__ano['combine_vars_{}'.format(xkuzm__ijkx)] = pdb__ayg
    eyz__eaki = {}
    exec(xuh__moy, vzgp__ano, eyz__eaki)
    ilvlg__rbq = eyz__eaki['combine_all_f']
    f_ir = compile_to_numba_ir(ilvlg__rbq, vzgp__ano)
    apbaz__yth = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wuylz__feu = numba.core.target_extension.dispatcher_registry[cpu_target](
        ilvlg__rbq)
    wuylz__feu.add_overload(apbaz__yth)
    return wuylz__feu


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    aiaaq__jqfmt = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    jled__iiwai = len(redvar_offsets) - 1
    bfjb__lhrg = redvar_offsets[jled__iiwai]
    xuh__moy = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert jled__iiwai == 1
        for ylmzr__aynhc in range(len(pivot_values)):
            lonoq__ugf = bfjb__lhrg * ylmzr__aynhc
            qqed__cbkvs = ', '.join(['redvar_arrs[{}][j]'.format(
                xkuzm__ijkx) for xkuzm__ijkx in range(lonoq__ugf +
                redvar_offsets[0], lonoq__ugf + redvar_offsets[1])])
            xuh__moy += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                ylmzr__aynhc, qqed__cbkvs)
    else:
        for ylmzr__aynhc in range(jled__iiwai):
            qqed__cbkvs = ', '.join(['redvar_arrs[{}][j]'.format(
                xkuzm__ijkx) for xkuzm__ijkx in range(redvar_offsets[
                ylmzr__aynhc], redvar_offsets[ylmzr__aynhc + 1])])
            xuh__moy += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                ylmzr__aynhc, ylmzr__aynhc, qqed__cbkvs)
    xuh__moy += '  return\n'
    vzgp__ano = {}
    for xkuzm__ijkx, pdb__ayg in enumerate(eval_funcs):
        vzgp__ano['eval_vars_{}'.format(xkuzm__ijkx)] = pdb__ayg
    eyz__eaki = {}
    exec(xuh__moy, vzgp__ano, eyz__eaki)
    ogf__gbc = eyz__eaki['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(ogf__gbc)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    pzuc__utz = len(var_types)
    menxv__yoq = [f'in{xkuzm__ijkx}' for xkuzm__ijkx in range(pzuc__utz)]
    nmuk__bqoa = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    yem__tjxh = nmuk__bqoa(0)
    xuh__moy = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        menxv__yoq))
    eyz__eaki = {}
    exec(xuh__moy, {'_zero': yem__tjxh}, eyz__eaki)
    nnep__ege = eyz__eaki['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(nnep__ege, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': yem__tjxh}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    old__vdwi = []
    for xkuzm__ijkx, ogrc__sbeil in enumerate(reduce_vars):
        old__vdwi.append(ir.Assign(block.body[xkuzm__ijkx].target,
            ogrc__sbeil, ogrc__sbeil.loc))
        for fpq__psngx in ogrc__sbeil.versioned_names:
            old__vdwi.append(ir.Assign(ogrc__sbeil, ir.Var(ogrc__sbeil.
                scope, fpq__psngx, ogrc__sbeil.loc), ogrc__sbeil.loc))
    block.body = block.body[:pzuc__utz] + old__vdwi + eval_nodes
    qqkli__gko = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nmuk__bqoa, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wuylz__feu = numba.core.target_extension.dispatcher_registry[cpu_target](
        nnep__ege)
    wuylz__feu.add_overload(qqkli__gko)
    return wuylz__feu


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    pzuc__utz = len(redvars)
    fkbpr__budv = [f'v{xkuzm__ijkx}' for xkuzm__ijkx in range(pzuc__utz)]
    menxv__yoq = [f'in{xkuzm__ijkx}' for xkuzm__ijkx in range(pzuc__utz)]
    xuh__moy = 'def agg_combine({}):\n'.format(', '.join(fkbpr__budv +
        menxv__yoq))
    gzlzk__wcxd = wrap_parfor_blocks(parfor)
    ehmh__geokv = find_topo_order(gzlzk__wcxd)
    ehmh__geokv = ehmh__geokv[1:]
    unwrap_parfor_blocks(parfor)
    ish__cuo = {}
    lla__vngfh = []
    for kev__uhm in ehmh__geokv:
        cxjsp__btx = parfor.loop_body[kev__uhm]
        for akgn__hpavo in cxjsp__btx.body:
            if is_call_assign(akgn__hpavo) and guard(find_callname, f_ir,
                akgn__hpavo.value) == ('__special_combine', 'bodo.ir.aggregate'
                ):
                args = akgn__hpavo.value.args
                qtor__gcxd = []
                ozinj__oxc = []
                for ogrc__sbeil in args[:-1]:
                    ind = redvars.index(ogrc__sbeil.name)
                    lla__vngfh.append(ind)
                    qtor__gcxd.append('v{}'.format(ind))
                    ozinj__oxc.append('in{}'.format(ind))
                rlrb__tsd = '__special_combine__{}'.format(len(ish__cuo))
                xuh__moy += '    ({},) = {}({})\n'.format(', '.join(
                    qtor__gcxd), rlrb__tsd, ', '.join(qtor__gcxd + ozinj__oxc))
                admdt__xrgg = ir.Expr.call(args[-1], [], (), cxjsp__btx.loc)
                buw__jeibq = guard(find_callname, f_ir, admdt__xrgg)
                assert buw__jeibq == ('_var_combine', 'bodo.ir.aggregate')
                buw__jeibq = bodo.ir.aggregate._var_combine
                ish__cuo[rlrb__tsd] = buw__jeibq
            if is_assign(akgn__hpavo) and akgn__hpavo.target.name in redvars:
                kfcwa__lti = akgn__hpavo.target.name
                ind = redvars.index(kfcwa__lti)
                if ind in lla__vngfh:
                    continue
                if len(f_ir._definitions[kfcwa__lti]) == 2:
                    var_def = f_ir._definitions[kfcwa__lti][0]
                    xuh__moy += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[kfcwa__lti][1]
                    xuh__moy += _match_reduce_def(var_def, f_ir, ind)
    xuh__moy += '    return {}'.format(', '.join(['v{}'.format(xkuzm__ijkx) for
        xkuzm__ijkx in range(pzuc__utz)]))
    eyz__eaki = {}
    exec(xuh__moy, {}, eyz__eaki)
    gduke__drgp = eyz__eaki['agg_combine']
    arg_typs = tuple(2 * var_types)
    vzgp__ano = {'numba': numba, 'bodo': bodo, 'np': np}
    vzgp__ano.update(ish__cuo)
    f_ir = compile_to_numba_ir(gduke__drgp, vzgp__ano, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    nmuk__bqoa = pm.typemap[block.body[-1].value.name]
    yyw__dombg = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nmuk__bqoa, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wuylz__feu = numba.core.target_extension.dispatcher_registry[cpu_target](
        gduke__drgp)
    wuylz__feu.add_overload(yyw__dombg)
    return wuylz__feu


def _match_reduce_def(var_def, f_ir, ind):
    xuh__moy = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        xuh__moy = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        pyte__jfck = guard(find_callname, f_ir, var_def)
        if pyte__jfck == ('min', 'builtins'):
            xuh__moy = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if pyte__jfck == ('max', 'builtins'):
            xuh__moy = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return xuh__moy


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    pzuc__utz = len(redvars)
    pdgun__atuwx = 1
    oedb__hadre = []
    for xkuzm__ijkx in range(pdgun__atuwx):
        zpj__esn = ir.Var(arr_var.scope, f'$input{xkuzm__ijkx}', arr_var.loc)
        oedb__hadre.append(zpj__esn)
    wbxl__uuv = parfor.loop_nests[0].index_variable
    xrt__pxflf = [0] * pzuc__utz
    for cxjsp__btx in parfor.loop_body.values():
        dczif__nmlru = []
        for akgn__hpavo in cxjsp__btx.body:
            if is_var_assign(akgn__hpavo
                ) and akgn__hpavo.value.name == wbxl__uuv.name:
                continue
            if is_getitem(akgn__hpavo
                ) and akgn__hpavo.value.value.name == arr_var.name:
                akgn__hpavo.value = oedb__hadre[0]
            if is_call_assign(akgn__hpavo) and guard(find_callname, pm.
                func_ir, akgn__hpavo.value) == ('isna',
                'bodo.libs.array_kernels') and akgn__hpavo.value.args[0
                ].name == arr_var.name:
                akgn__hpavo.value = ir.Const(False, akgn__hpavo.target.loc)
            if is_assign(akgn__hpavo) and akgn__hpavo.target.name in redvars:
                ind = redvars.index(akgn__hpavo.target.name)
                xrt__pxflf[ind] = akgn__hpavo.target
            dczif__nmlru.append(akgn__hpavo)
        cxjsp__btx.body = dczif__nmlru
    fkbpr__budv = ['v{}'.format(xkuzm__ijkx) for xkuzm__ijkx in range(
        pzuc__utz)]
    menxv__yoq = ['in{}'.format(xkuzm__ijkx) for xkuzm__ijkx in range(
        pdgun__atuwx)]
    xuh__moy = 'def agg_update({}):\n'.format(', '.join(fkbpr__budv +
        menxv__yoq))
    xuh__moy += '    __update_redvars()\n'
    xuh__moy += '    return {}'.format(', '.join(['v{}'.format(xkuzm__ijkx) for
        xkuzm__ijkx in range(pzuc__utz)]))
    eyz__eaki = {}
    exec(xuh__moy, {}, eyz__eaki)
    zro__diq = eyz__eaki['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * pdgun__atuwx)
    f_ir = compile_to_numba_ir(zro__diq, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    vbnh__ycu = f_ir.blocks.popitem()[1].body
    nmuk__bqoa = pm.typemap[vbnh__ycu[-1].value.name]
    gzlzk__wcxd = wrap_parfor_blocks(parfor)
    ehmh__geokv = find_topo_order(gzlzk__wcxd)
    ehmh__geokv = ehmh__geokv[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    tdx__gsy = f_ir.blocks[ehmh__geokv[0]]
    teot__limw = f_ir.blocks[ehmh__geokv[-1]]
    dpgvn__bmptu = vbnh__ycu[:pzuc__utz + pdgun__atuwx]
    if pzuc__utz > 1:
        tdb__fihu = vbnh__ycu[-3:]
        assert is_assign(tdb__fihu[0]) and isinstance(tdb__fihu[0].value,
            ir.Expr) and tdb__fihu[0].value.op == 'build_tuple'
    else:
        tdb__fihu = vbnh__ycu[-2:]
    for xkuzm__ijkx in range(pzuc__utz):
        alkwx__kys = vbnh__ycu[xkuzm__ijkx].target
        hapyo__uwi = ir.Assign(alkwx__kys, xrt__pxflf[xkuzm__ijkx],
            alkwx__kys.loc)
        dpgvn__bmptu.append(hapyo__uwi)
    for xkuzm__ijkx in range(pzuc__utz, pzuc__utz + pdgun__atuwx):
        alkwx__kys = vbnh__ycu[xkuzm__ijkx].target
        hapyo__uwi = ir.Assign(alkwx__kys, oedb__hadre[xkuzm__ijkx -
            pzuc__utz], alkwx__kys.loc)
        dpgvn__bmptu.append(hapyo__uwi)
    tdx__gsy.body = dpgvn__bmptu + tdx__gsy.body
    aqbzj__wioza = []
    for xkuzm__ijkx in range(pzuc__utz):
        alkwx__kys = vbnh__ycu[xkuzm__ijkx].target
        hapyo__uwi = ir.Assign(xrt__pxflf[xkuzm__ijkx], alkwx__kys,
            alkwx__kys.loc)
        aqbzj__wioza.append(hapyo__uwi)
    teot__limw.body += aqbzj__wioza + tdb__fihu
    wsu__ubi = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nmuk__bqoa, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wuylz__feu = numba.core.target_extension.dispatcher_registry[cpu_target](
        zro__diq)
    wuylz__feu.add_overload(wsu__ubi)
    return wuylz__feu


def _rm_arg_agg_block(block, typemap):
    jhw__qljh = []
    arr_var = None
    for xkuzm__ijkx, akgn__hpavo in enumerate(block.body):
        if is_assign(akgn__hpavo) and isinstance(akgn__hpavo.value, ir.Arg):
            arr_var = akgn__hpavo.target
            ipr__uzc = typemap[arr_var.name]
            if not isinstance(ipr__uzc, types.ArrayCompatible):
                jhw__qljh += block.body[xkuzm__ijkx + 1:]
                break
            hhrg__tlxk = block.body[xkuzm__ijkx + 1]
            assert is_assign(hhrg__tlxk) and isinstance(hhrg__tlxk.value,
                ir.Expr
                ) and hhrg__tlxk.value.op == 'getattr' and hhrg__tlxk.value.attr == 'shape' and hhrg__tlxk.value.value.name == arr_var.name
            ayps__pqkw = hhrg__tlxk.target
            afp__dqsgv = block.body[xkuzm__ijkx + 2]
            assert is_assign(afp__dqsgv) and isinstance(afp__dqsgv.value,
                ir.Expr
                ) and afp__dqsgv.value.op == 'static_getitem' and afp__dqsgv.value.value.name == ayps__pqkw.name
            jhw__qljh += block.body[xkuzm__ijkx + 3:]
            break
        jhw__qljh.append(akgn__hpavo)
    return jhw__qljh, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    gzlzk__wcxd = wrap_parfor_blocks(parfor)
    ehmh__geokv = find_topo_order(gzlzk__wcxd)
    ehmh__geokv = ehmh__geokv[1:]
    unwrap_parfor_blocks(parfor)
    for kev__uhm in reversed(ehmh__geokv):
        for akgn__hpavo in reversed(parfor.loop_body[kev__uhm].body):
            if isinstance(akgn__hpavo, ir.Assign) and (akgn__hpavo.target.
                name in parfor_params or akgn__hpavo.target.name in
                var_to_param):
                lmv__slfxu = akgn__hpavo.target.name
                rhs = akgn__hpavo.value
                svt__isc = (lmv__slfxu if lmv__slfxu in parfor_params else
                    var_to_param[lmv__slfxu])
                bmlcj__krn = []
                if isinstance(rhs, ir.Var):
                    bmlcj__krn = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    bmlcj__krn = [ogrc__sbeil.name for ogrc__sbeil in
                        akgn__hpavo.value.list_vars()]
                param_uses[svt__isc].extend(bmlcj__krn)
                for ogrc__sbeil in bmlcj__krn:
                    var_to_param[ogrc__sbeil] = svt__isc
            if isinstance(akgn__hpavo, Parfor):
                get_parfor_reductions(akgn__hpavo, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for tsrc__wmfw, bmlcj__krn in param_uses.items():
        if tsrc__wmfw in bmlcj__krn and tsrc__wmfw not in reduce_varnames:
            reduce_varnames.append(tsrc__wmfw)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
