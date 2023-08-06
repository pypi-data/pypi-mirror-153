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
            gsn__wsrw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            paekg__hosyb = cgutils.get_or_insert_function(builder.module,
                gsn__wsrw, sym._literal_value)
            builder.call(paekg__hosyb, [context.get_constant_null(sig.args[0])]
                )
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            gsn__wsrw = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            paekg__hosyb = cgutils.get_or_insert_function(builder.module,
                gsn__wsrw, sym._literal_value)
            builder.call(paekg__hosyb, [context.get_constant(types.int64, 0
                ), context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            gsn__wsrw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            paekg__hosyb = cgutils.get_or_insert_function(builder.module,
                gsn__wsrw, sym._literal_value)
            builder.call(paekg__hosyb, [context.get_constant_null(sig.args[
                0]), context.get_constant_null(sig.args[1]), context.
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
        oowld__zuiu = True
        www__ripg = 1
        zcce__hmaya = -1
        if isinstance(rhs, ir.Expr):
            for kdeai__vpio in rhs.kws:
                if func_name in list_cumulative:
                    if kdeai__vpio[0] == 'skipna':
                        oowld__zuiu = guard(find_const, func_ir, kdeai__vpio[1]
                            )
                        if not isinstance(oowld__zuiu, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if kdeai__vpio[0] == 'dropna':
                        oowld__zuiu = guard(find_const, func_ir, kdeai__vpio[1]
                            )
                        if not isinstance(oowld__zuiu, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            www__ripg = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', www__ripg)
            www__ripg = guard(find_const, func_ir, www__ripg)
        if func_name == 'head':
            zcce__hmaya = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(zcce__hmaya, int):
                zcce__hmaya = guard(find_const, func_ir, zcce__hmaya)
            if zcce__hmaya < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = oowld__zuiu
        func.periods = www__ripg
        func.head_n = zcce__hmaya
        if func_name == 'transform':
            kws = dict(rhs.kws)
            rhto__goxa = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            jrui__wee = typemap[rhto__goxa.name]
            ogbc__dkuwz = None
            if isinstance(jrui__wee, str):
                ogbc__dkuwz = jrui__wee
            elif is_overload_constant_str(jrui__wee):
                ogbc__dkuwz = get_overload_const_str(jrui__wee)
            elif bodo.utils.typing.is_builtin_function(jrui__wee):
                ogbc__dkuwz = bodo.utils.typing.get_builtin_function_name(
                    jrui__wee)
            if ogbc__dkuwz not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {ogbc__dkuwz}'
                    )
            func.transform_func = supported_agg_funcs.index(ogbc__dkuwz)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    rhto__goxa = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if rhto__goxa == '':
        jrui__wee = types.none
    else:
        jrui__wee = typemap[rhto__goxa.name]
    if is_overload_constant_dict(jrui__wee):
        qlvb__hdpx = get_overload_constant_dict(jrui__wee)
        dsruj__nntnt = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in qlvb__hdpx.values()]
        return dsruj__nntnt
    if jrui__wee == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(jrui__wee, types.BaseTuple) or is_overload_constant_list(
        jrui__wee):
        dsruj__nntnt = []
        mfm__gakos = 0
        if is_overload_constant_list(jrui__wee):
            wkuy__dbgq = get_overload_const_list(jrui__wee)
        else:
            wkuy__dbgq = jrui__wee.types
        for t in wkuy__dbgq:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                dsruj__nntnt.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(wkuy__dbgq) > 1:
                    func.fname = '<lambda_' + str(mfm__gakos) + '>'
                    mfm__gakos += 1
                dsruj__nntnt.append(func)
        return [dsruj__nntnt]
    if is_overload_constant_str(jrui__wee):
        func_name = get_overload_const_str(jrui__wee)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(jrui__wee):
        func_name = bodo.utils.typing.get_builtin_function_name(jrui__wee)
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
        mfm__gakos = 0
        wjlt__zavtv = []
        for mdgmo__emk in f_val:
            func = get_agg_func_udf(func_ir, mdgmo__emk, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{mfm__gakos}>'
                mfm__gakos += 1
            wjlt__zavtv.append(func)
        return wjlt__zavtv
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
    ogbc__dkuwz = code.co_name
    return ogbc__dkuwz


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
            obym__maxhs = types.DType(args[0])
            return signature(obym__maxhs, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    dhutf__pcxmz = nobs_a + nobs_b
    mheg__gxf = (nobs_a * mean_a + nobs_b * mean_b) / dhutf__pcxmz
    betfv__scato = mean_b - mean_a
    xfxrg__lzy = (ssqdm_a + ssqdm_b + betfv__scato * betfv__scato * nobs_a *
        nobs_b / dhutf__pcxmz)
    return xfxrg__lzy, mheg__gxf, dhutf__pcxmz


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
        elpi__emae = ''
        for kje__bao, ddgx__valf in self.df_out_vars.items():
            elpi__emae += "'{}':{}, ".format(kje__bao, ddgx__valf.name)
        qlf__hoin = '{}{{{}}}'.format(self.df_out, elpi__emae)
        swdqv__acmtx = ''
        for kje__bao, ddgx__valf in self.df_in_vars.items():
            swdqv__acmtx += "'{}':{}, ".format(kje__bao, ddgx__valf.name)
        tmfn__sbi = '{}{{{}}}'.format(self.df_in, swdqv__acmtx)
        wqpuo__yjwkv = 'pivot {}:{}'.format(self.pivot_arr.name, self.
            pivot_values) if self.pivot_arr is not None else ''
        key_names = ','.join([str(aap__mvdq) for aap__mvdq in self.key_names])
        crqef__dha = ','.join([ddgx__valf.name for ddgx__valf in self.key_arrs]
            )
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(qlf__hoin,
            tmfn__sbi, key_names, crqef__dha, wqpuo__yjwkv)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        cjy__zyei, avady__ogjqd = self.gb_info_out.pop(out_col_name)
        if cjy__zyei is None and not self.is_crosstab:
            return
        lsvb__kchm = self.gb_info_in[cjy__zyei]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for jjfn__cgr, (func, elpi__emae) in enumerate(lsvb__kchm):
                try:
                    elpi__emae.remove(out_col_name)
                    if len(elpi__emae) == 0:
                        lsvb__kchm.pop(jjfn__cgr)
                        break
                except ValueError as agh__suj:
                    continue
        else:
            for jjfn__cgr, (func, dhi__sfsei) in enumerate(lsvb__kchm):
                if dhi__sfsei == out_col_name:
                    lsvb__kchm.pop(jjfn__cgr)
                    break
        if len(lsvb__kchm) == 0:
            self.gb_info_in.pop(cjy__zyei)
            self.df_in_vars.pop(cjy__zyei)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({ddgx__valf.name for ddgx__valf in aggregate_node.key_arrs})
    use_set.update({ddgx__valf.name for ddgx__valf in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({ddgx__valf.name for ddgx__valf in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({ddgx__valf.name for ddgx__valf in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    ydyh__oyjvk = [hjp__mxo for hjp__mxo, uty__awb in aggregate_node.
        df_out_vars.items() if uty__awb.name not in lives]
    for zizf__xrfe in ydyh__oyjvk:
        aggregate_node.remove_out_col(zizf__xrfe)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(ddgx__valf.name not in lives for
        ddgx__valf in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    aevr__cgj = set(ddgx__valf.name for ddgx__valf in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        aevr__cgj.update({ddgx__valf.name for ddgx__valf in aggregate_node.
            out_key_vars})
    return set(), aevr__cgj


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for jjfn__cgr in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[jjfn__cgr] = replace_vars_inner(aggregate_node
            .key_arrs[jjfn__cgr], var_dict)
    for hjp__mxo in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[hjp__mxo] = replace_vars_inner(aggregate_node
            .df_in_vars[hjp__mxo], var_dict)
    for hjp__mxo in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[hjp__mxo] = replace_vars_inner(
            aggregate_node.df_out_vars[hjp__mxo], var_dict)
    if aggregate_node.out_key_vars is not None:
        for jjfn__cgr in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[jjfn__cgr] = replace_vars_inner(
                aggregate_node.out_key_vars[jjfn__cgr], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for jjfn__cgr in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[jjfn__cgr] = visit_vars_inner(aggregate_node
            .key_arrs[jjfn__cgr], callback, cbdata)
    for hjp__mxo in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[hjp__mxo] = visit_vars_inner(aggregate_node
            .df_in_vars[hjp__mxo], callback, cbdata)
    for hjp__mxo in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[hjp__mxo] = visit_vars_inner(aggregate_node
            .df_out_vars[hjp__mxo], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for jjfn__cgr in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[jjfn__cgr] = visit_vars_inner(
                aggregate_node.out_key_vars[jjfn__cgr], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    bnxeh__jns = []
    for qxo__xmlho in aggregate_node.key_arrs:
        hfx__nnynx = equiv_set.get_shape(qxo__xmlho)
        if hfx__nnynx:
            bnxeh__jns.append(hfx__nnynx[0])
    if aggregate_node.pivot_arr is not None:
        hfx__nnynx = equiv_set.get_shape(aggregate_node.pivot_arr)
        if hfx__nnynx:
            bnxeh__jns.append(hfx__nnynx[0])
    for uty__awb in aggregate_node.df_in_vars.values():
        hfx__nnynx = equiv_set.get_shape(uty__awb)
        if hfx__nnynx:
            bnxeh__jns.append(hfx__nnynx[0])
    if len(bnxeh__jns) > 1:
        equiv_set.insert_equiv(*bnxeh__jns)
    vobsv__hxub = []
    bnxeh__jns = []
    cktj__fcldr = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        cktj__fcldr.extend(aggregate_node.out_key_vars)
    for uty__awb in cktj__fcldr:
        djtau__ztbf = typemap[uty__awb.name]
        qgvo__rcix = array_analysis._gen_shape_call(equiv_set, uty__awb,
            djtau__ztbf.ndim, None, vobsv__hxub)
        equiv_set.insert_equiv(uty__awb, qgvo__rcix)
        bnxeh__jns.append(qgvo__rcix[0])
        equiv_set.define(uty__awb, set())
    if len(bnxeh__jns) > 1:
        equiv_set.insert_equiv(*bnxeh__jns)
    return [], vobsv__hxub


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    ljyd__vhdnx = Distribution.OneD
    for uty__awb in aggregate_node.df_in_vars.values():
        ljyd__vhdnx = Distribution(min(ljyd__vhdnx.value, array_dists[
            uty__awb.name].value))
    for qxo__xmlho in aggregate_node.key_arrs:
        ljyd__vhdnx = Distribution(min(ljyd__vhdnx.value, array_dists[
            qxo__xmlho.name].value))
    if aggregate_node.pivot_arr is not None:
        ljyd__vhdnx = Distribution(min(ljyd__vhdnx.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = ljyd__vhdnx
    for uty__awb in aggregate_node.df_in_vars.values():
        array_dists[uty__awb.name] = ljyd__vhdnx
    for qxo__xmlho in aggregate_node.key_arrs:
        array_dists[qxo__xmlho.name] = ljyd__vhdnx
    osziy__min = Distribution.OneD_Var
    for uty__awb in aggregate_node.df_out_vars.values():
        if uty__awb.name in array_dists:
            osziy__min = Distribution(min(osziy__min.value, array_dists[
                uty__awb.name].value))
    if aggregate_node.out_key_vars is not None:
        for uty__awb in aggregate_node.out_key_vars:
            if uty__awb.name in array_dists:
                osziy__min = Distribution(min(osziy__min.value, array_dists
                    [uty__awb.name].value))
    osziy__min = Distribution(min(osziy__min.value, ljyd__vhdnx.value))
    for uty__awb in aggregate_node.df_out_vars.values():
        array_dists[uty__awb.name] = osziy__min
    if aggregate_node.out_key_vars is not None:
        for ksq__kczni in aggregate_node.out_key_vars:
            array_dists[ksq__kczni.name] = osziy__min
    if osziy__min != Distribution.OneD_Var:
        for qxo__xmlho in aggregate_node.key_arrs:
            array_dists[qxo__xmlho.name] = osziy__min
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = osziy__min
        for uty__awb in aggregate_node.df_in_vars.values():
            array_dists[uty__awb.name] = osziy__min


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for uty__awb in agg_node.df_out_vars.values():
        definitions[uty__awb.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for ksq__kczni in agg_node.out_key_vars:
            definitions[ksq__kczni.name].append(agg_node)
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
        for ddgx__valf in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[ddgx__valf.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                ddgx__valf.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    stn__dvx = tuple(typemap[ddgx__valf.name] for ddgx__valf in agg_node.
        key_arrs)
    oxkg__rotfx = [ddgx__valf for erhks__hnj, ddgx__valf in agg_node.
        df_in_vars.items()]
    lazdb__njsy = [ddgx__valf for erhks__hnj, ddgx__valf in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    dsruj__nntnt = []
    if agg_node.pivot_arr is not None:
        for cjy__zyei, lsvb__kchm in agg_node.gb_info_in.items():
            for func, avady__ogjqd in lsvb__kchm:
                if cjy__zyei is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        cjy__zyei].name])
                dsruj__nntnt.append(func)
    else:
        for cjy__zyei, func in agg_node.gb_info_out.values():
            if cjy__zyei is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[cjy__zyei].name]
                    )
            dsruj__nntnt.append(func)
    out_col_typs = tuple(typemap[ddgx__valf.name] for ddgx__valf in lazdb__njsy
        )
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(stn__dvx + tuple(typemap[ddgx__valf.name] for
        ddgx__valf in oxkg__rotfx) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    gihel__xgssz = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for jjfn__cgr, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            gihel__xgssz.update({f'in_cat_dtype_{jjfn__cgr}': in_col_typ})
    for jjfn__cgr, tcs__pnowi in enumerate(out_col_typs):
        if isinstance(tcs__pnowi, bodo.CategoricalArrayType):
            gihel__xgssz.update({f'out_cat_dtype_{jjfn__cgr}': tcs__pnowi})
    udf_func_struct = get_udf_func_struct(dsruj__nntnt, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    zjtz__hmm = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    gihel__xgssz.update({'pd': pd, 'pre_alloc_string_array':
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
            gihel__xgssz.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            gihel__xgssz.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    noyi__xli = compile_to_numba_ir(zjtz__hmm, gihel__xgssz, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    ejkuy__oyv = []
    if agg_node.pivot_arr is None:
        jbglv__pzw = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        fwagc__opogy = ir.Var(jbglv__pzw, mk_unique_var('dummy_none'), loc)
        typemap[fwagc__opogy.name] = types.none
        ejkuy__oyv.append(ir.Assign(ir.Const(None, loc), fwagc__opogy, loc))
        oxkg__rotfx.append(fwagc__opogy)
    else:
        oxkg__rotfx.append(agg_node.pivot_arr)
    replace_arg_nodes(noyi__xli, agg_node.key_arrs + oxkg__rotfx)
    cqwuw__izepb = noyi__xli.body[-3]
    assert is_assign(cqwuw__izepb) and isinstance(cqwuw__izepb.value, ir.Expr
        ) and cqwuw__izepb.value.op == 'build_tuple'
    ejkuy__oyv += noyi__xli.body[:-3]
    cktj__fcldr = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        cktj__fcldr += agg_node.out_key_vars
    for jjfn__cgr, cxz__sost in enumerate(cktj__fcldr):
        svw__ivv = cqwuw__izepb.value.items[jjfn__cgr]
        ejkuy__oyv.append(ir.Assign(svw__ivv, cxz__sost, cxz__sost.loc))
    return ejkuy__oyv


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        hotuy__dbik = args[0]
        dtype = types.Tuple([t.dtype for t in hotuy__dbik.types]
            ) if isinstance(hotuy__dbik, types.BaseTuple
            ) else hotuy__dbik.dtype
        if isinstance(hotuy__dbik, types.BaseTuple) and len(hotuy__dbik.types
            ) == 1:
            dtype = hotuy__dbik.types[0].dtype
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
        ibo__gwqmc = args[0]
        if ibo__gwqmc == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    cgbo__kgxcq = context.compile_internal(builder, lambda a: False, sig, args)
    return cgbo__kgxcq


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        bco__cvssf = IntDtype(t.dtype).name
        assert bco__cvssf.endswith('Dtype()')
        bco__cvssf = bco__cvssf[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{bco__cvssf}'))"
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
        fox__rea = 'in' if is_input else 'out'
        return f'bodo.utils.utils.alloc_type(1, {fox__rea}_cat_dtype_{colnum})'
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
    smj__mtm = udf_func_struct.var_typs
    gnztx__fjec = len(smj__mtm)
    vrty__weald = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    vrty__weald += '    if is_null_pointer(in_table):\n'
    vrty__weald += '        return\n'
    vrty__weald += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in smj__mtm]), ',' if
        len(smj__mtm) == 1 else '')
    hjp__wka = n_keys
    bfoz__rhof = []
    redvar_offsets = []
    zbgs__ipcq = []
    if do_combine:
        for jjfn__cgr, mdgmo__emk in enumerate(allfuncs):
            if mdgmo__emk.ftype != 'udf':
                hjp__wka += mdgmo__emk.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(hjp__wka, hjp__wka +
                    mdgmo__emk.n_redvars))
                hjp__wka += mdgmo__emk.n_redvars
                zbgs__ipcq.append(data_in_typs_[func_idx_to_in_col[jjfn__cgr]])
                bfoz__rhof.append(func_idx_to_in_col[jjfn__cgr] + n_keys)
    else:
        for jjfn__cgr, mdgmo__emk in enumerate(allfuncs):
            if mdgmo__emk.ftype != 'udf':
                hjp__wka += mdgmo__emk.ncols_post_shuffle
            else:
                redvar_offsets += list(range(hjp__wka + 1, hjp__wka + 1 +
                    mdgmo__emk.n_redvars))
                hjp__wka += mdgmo__emk.n_redvars + 1
                zbgs__ipcq.append(data_in_typs_[func_idx_to_in_col[jjfn__cgr]])
                bfoz__rhof.append(func_idx_to_in_col[jjfn__cgr] + n_keys)
    assert len(redvar_offsets) == gnztx__fjec
    ddwzf__ethx = len(zbgs__ipcq)
    igcd__bpd = []
    for jjfn__cgr, t in enumerate(zbgs__ipcq):
        igcd__bpd.append(_gen_dummy_alloc(t, jjfn__cgr, True))
    vrty__weald += '    data_in_dummy = ({}{})\n'.format(','.join(igcd__bpd
        ), ',' if len(zbgs__ipcq) == 1 else '')
    vrty__weald += """
    # initialize redvar cols
"""
    vrty__weald += '    init_vals = __init_func()\n'
    for jjfn__cgr in range(gnztx__fjec):
        vrty__weald += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(jjfn__cgr, redvar_offsets[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(redvar_arr_{})\n'.format(jjfn__cgr)
        vrty__weald += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            jjfn__cgr, jjfn__cgr)
    vrty__weald += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(jjfn__cgr) for jjfn__cgr in range(
        gnztx__fjec)]), ',' if gnztx__fjec == 1 else '')
    vrty__weald += '\n'
    for jjfn__cgr in range(ddwzf__ethx):
        vrty__weald += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(jjfn__cgr, bfoz__rhof[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(data_in_{})\n'.format(jjfn__cgr)
    vrty__weald += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(jjfn__cgr) for jjfn__cgr in range(ddwzf__ethx)]), ',' if 
        ddwzf__ethx == 1 else '')
    vrty__weald += '\n'
    vrty__weald += '    for i in range(len(data_in_0)):\n'
    vrty__weald += '        w_ind = row_to_group[i]\n'
    vrty__weald += '        if w_ind != -1:\n'
    vrty__weald += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    yxl__acyd = {}
    exec(vrty__weald, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yxl__acyd)
    return yxl__acyd['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    smj__mtm = udf_func_struct.var_typs
    gnztx__fjec = len(smj__mtm)
    vrty__weald = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    vrty__weald += '    if is_null_pointer(in_table):\n'
    vrty__weald += '        return\n'
    vrty__weald += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in smj__mtm]), ',' if
        len(smj__mtm) == 1 else '')
    kiqdl__bih = n_keys
    dfl__rrpc = n_keys
    gwpp__ugwb = []
    clo__ifg = []
    for mdgmo__emk in allfuncs:
        if mdgmo__emk.ftype != 'udf':
            kiqdl__bih += mdgmo__emk.ncols_pre_shuffle
            dfl__rrpc += mdgmo__emk.ncols_post_shuffle
        else:
            gwpp__ugwb += list(range(kiqdl__bih, kiqdl__bih + mdgmo__emk.
                n_redvars))
            clo__ifg += list(range(dfl__rrpc + 1, dfl__rrpc + 1 +
                mdgmo__emk.n_redvars))
            kiqdl__bih += mdgmo__emk.n_redvars
            dfl__rrpc += 1 + mdgmo__emk.n_redvars
    assert len(gwpp__ugwb) == gnztx__fjec
    vrty__weald += """
    # initialize redvar cols
"""
    vrty__weald += '    init_vals = __init_func()\n'
    for jjfn__cgr in range(gnztx__fjec):
        vrty__weald += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(jjfn__cgr, clo__ifg[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(redvar_arr_{})\n'.format(jjfn__cgr)
        vrty__weald += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            jjfn__cgr, jjfn__cgr)
    vrty__weald += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(jjfn__cgr) for jjfn__cgr in range(
        gnztx__fjec)]), ',' if gnztx__fjec == 1 else '')
    vrty__weald += '\n'
    for jjfn__cgr in range(gnztx__fjec):
        vrty__weald += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(jjfn__cgr, gwpp__ugwb[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(recv_redvar_arr_{})\n'.format(jjfn__cgr)
    vrty__weald += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(jjfn__cgr) for jjfn__cgr in range(
        gnztx__fjec)]), ',' if gnztx__fjec == 1 else '')
    vrty__weald += '\n'
    if gnztx__fjec:
        vrty__weald += '    for i in range(len(recv_redvar_arr_0)):\n'
        vrty__weald += '        w_ind = row_to_group[i]\n'
        vrty__weald += """        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)
"""
    yxl__acyd = {}
    exec(vrty__weald, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yxl__acyd)
    return yxl__acyd['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    smj__mtm = udf_func_struct.var_typs
    gnztx__fjec = len(smj__mtm)
    hjp__wka = n_keys
    redvar_offsets = []
    riht__hgtq = []
    out_data_typs = []
    for jjfn__cgr, mdgmo__emk in enumerate(allfuncs):
        if mdgmo__emk.ftype != 'udf':
            hjp__wka += mdgmo__emk.ncols_post_shuffle
        else:
            riht__hgtq.append(hjp__wka)
            redvar_offsets += list(range(hjp__wka + 1, hjp__wka + 1 +
                mdgmo__emk.n_redvars))
            hjp__wka += 1 + mdgmo__emk.n_redvars
            out_data_typs.append(out_data_typs_[jjfn__cgr])
    assert len(redvar_offsets) == gnztx__fjec
    ddwzf__ethx = len(out_data_typs)
    vrty__weald = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    vrty__weald += '    if is_null_pointer(table):\n'
    vrty__weald += '        return\n'
    vrty__weald += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in smj__mtm]), ',' if
        len(smj__mtm) == 1 else '')
    vrty__weald += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for jjfn__cgr in range(gnztx__fjec):
        vrty__weald += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(jjfn__cgr, redvar_offsets[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(redvar_arr_{})\n'.format(jjfn__cgr)
    vrty__weald += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(jjfn__cgr) for jjfn__cgr in range(
        gnztx__fjec)]), ',' if gnztx__fjec == 1 else '')
    vrty__weald += '\n'
    for jjfn__cgr in range(ddwzf__ethx):
        vrty__weald += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(jjfn__cgr, riht__hgtq[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(data_out_{})\n'.format(jjfn__cgr)
    vrty__weald += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'
        .format(jjfn__cgr) for jjfn__cgr in range(ddwzf__ethx)]), ',' if 
        ddwzf__ethx == 1 else '')
    vrty__weald += '\n'
    vrty__weald += '    for i in range(len(data_out_0)):\n'
    vrty__weald += '        __eval_res(redvars, data_out, i)\n'
    yxl__acyd = {}
    exec(vrty__weald, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yxl__acyd)
    return yxl__acyd['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    hjp__wka = n_keys
    yackz__qseh = []
    for jjfn__cgr, mdgmo__emk in enumerate(allfuncs):
        if mdgmo__emk.ftype == 'gen_udf':
            yackz__qseh.append(hjp__wka)
            hjp__wka += 1
        elif mdgmo__emk.ftype != 'udf':
            hjp__wka += mdgmo__emk.ncols_post_shuffle
        else:
            hjp__wka += mdgmo__emk.n_redvars + 1
    vrty__weald = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    vrty__weald += '    if num_groups == 0:\n'
    vrty__weald += '        return\n'
    for jjfn__cgr, func in enumerate(udf_func_struct.general_udf_funcs):
        vrty__weald += '    # col {}\n'.format(jjfn__cgr)
        vrty__weald += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(yackz__qseh[jjfn__cgr], jjfn__cgr))
        vrty__weald += '    incref(out_col)\n'
        vrty__weald += '    for j in range(num_groups):\n'
        vrty__weald += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(jjfn__cgr, jjfn__cgr))
        vrty__weald += '        incref(in_col)\n'
        vrty__weald += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(jjfn__cgr))
    gihel__xgssz = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    zfql__opcq = 0
    for jjfn__cgr, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[zfql__opcq]
        gihel__xgssz['func_{}'.format(zfql__opcq)] = func
        gihel__xgssz['in_col_{}_typ'.format(zfql__opcq)] = in_col_typs[
            func_idx_to_in_col[jjfn__cgr]]
        gihel__xgssz['out_col_{}_typ'.format(zfql__opcq)] = out_col_typs[
            jjfn__cgr]
        zfql__opcq += 1
    yxl__acyd = {}
    exec(vrty__weald, gihel__xgssz, yxl__acyd)
    mdgmo__emk = yxl__acyd['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    kfrym__sdu = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(kfrym__sdu, nopython=True)(mdgmo__emk)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    kmemy__wsxuy = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        iexvc__riec = 1
    else:
        iexvc__riec = len(agg_node.pivot_values)
    eajm__lul = tuple('key_' + sanitize_varname(kje__bao) for kje__bao in
        agg_node.key_names)
    caya__uko = {kje__bao: 'in_{}'.format(sanitize_varname(kje__bao)) for
        kje__bao in agg_node.gb_info_in.keys() if kje__bao is not None}
    zgnr__xly = {kje__bao: ('out_' + sanitize_varname(kje__bao)) for
        kje__bao in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    bosx__jpkds = ', '.join(eajm__lul)
    jys__lgrll = ', '.join(caya__uko.values())
    if jys__lgrll != '':
        jys__lgrll = ', ' + jys__lgrll
    vrty__weald = 'def agg_top({}{}{}, pivot_arr):\n'.format(bosx__jpkds,
        jys__lgrll, ', index_arg' if agg_node.input_has_index else '')
    for a in (eajm__lul + tuple(caya__uko.values())):
        vrty__weald += f'    {a} = decode_if_dict_array({a})\n'
    if kmemy__wsxuy:
        vrty__weald += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        zjj__ystg = []
        for cjy__zyei, lsvb__kchm in agg_node.gb_info_in.items():
            if cjy__zyei is not None:
                for func, avady__ogjqd in lsvb__kchm:
                    zjj__ystg.append(caya__uko[cjy__zyei])
    else:
        zjj__ystg = tuple(caya__uko[cjy__zyei] for cjy__zyei, avady__ogjqd in
            agg_node.gb_info_out.values() if cjy__zyei is not None)
    dyi__jkwyi = eajm__lul + tuple(zjj__ystg)
    vrty__weald += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in dyi__jkwyi), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    vrty__weald += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    glvj__jqp = []
    func_idx_to_in_col = []
    avbu__cyf = []
    oowld__zuiu = False
    zfeuf__hpict = 1
    zcce__hmaya = -1
    qrggj__cbaz = 0
    tehed__zcsac = 0
    if not kmemy__wsxuy:
        dsruj__nntnt = [func for avady__ogjqd, func in agg_node.gb_info_out
            .values()]
    else:
        dsruj__nntnt = [func for func, avady__ogjqd in lsvb__kchm for
            lsvb__kchm in agg_node.gb_info_in.values()]
    for yjskl__eam, func in enumerate(dsruj__nntnt):
        glvj__jqp.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            qrggj__cbaz += 1
        if hasattr(func, 'skipdropna'):
            oowld__zuiu = func.skipdropna
        if func.ftype == 'shift':
            zfeuf__hpict = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            tehed__zcsac = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            zcce__hmaya = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(yjskl__eam)
        if func.ftype == 'udf':
            avbu__cyf.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            avbu__cyf.append(0)
            do_combine = False
    glvj__jqp.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == iexvc__riec, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * iexvc__riec, 'invalid number of groupby outputs'
    if qrggj__cbaz > 0:
        if qrggj__cbaz != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for jjfn__cgr, kje__bao in enumerate(agg_node.gb_info_out.keys()):
        pzx__htpb = zgnr__xly[kje__bao] + '_dummy'
        tcs__pnowi = out_col_typs[jjfn__cgr]
        cjy__zyei, func = agg_node.gb_info_out[kje__bao]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(tcs__pnowi, bodo.
            CategoricalArrayType):
            vrty__weald += '    {} = {}\n'.format(pzx__htpb, caya__uko[
                cjy__zyei])
        elif udf_func_struct is not None:
            vrty__weald += '    {} = {}\n'.format(pzx__htpb,
                _gen_dummy_alloc(tcs__pnowi, jjfn__cgr, False))
    if udf_func_struct is not None:
        ztou__ggq = next_label()
        if udf_func_struct.regular_udfs:
            kfrym__sdu = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            vkk__xsmo = numba.cfunc(kfrym__sdu, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, ztou__ggq))
            paym__wei = numba.cfunc(kfrym__sdu, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, ztou__ggq))
            eeye__odcp = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                ztou__ggq))
            udf_func_struct.set_regular_cfuncs(vkk__xsmo, paym__wei, eeye__odcp
                )
            for wen__wtc in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[wen__wtc.native_name] = wen__wtc
                gb_agg_cfunc_addr[wen__wtc.native_name] = wen__wtc.address
        if udf_func_struct.general_udfs:
            nsak__itr = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                ztou__ggq)
            udf_func_struct.set_general_cfunc(nsak__itr)
        jfmje__edm = []
        ujue__sgqk = 0
        jjfn__cgr = 0
        for pzx__htpb, mdgmo__emk in zip(zgnr__xly.values(), allfuncs):
            if mdgmo__emk.ftype in ('udf', 'gen_udf'):
                jfmje__edm.append(pzx__htpb + '_dummy')
                for uhiog__qmz in range(ujue__sgqk, ujue__sgqk + avbu__cyf[
                    jjfn__cgr]):
                    jfmje__edm.append('data_redvar_dummy_' + str(uhiog__qmz))
                ujue__sgqk += avbu__cyf[jjfn__cgr]
                jjfn__cgr += 1
        if udf_func_struct.regular_udfs:
            smj__mtm = udf_func_struct.var_typs
            for jjfn__cgr, t in enumerate(smj__mtm):
                vrty__weald += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(jjfn__cgr, _get_np_dtype(t)))
        vrty__weald += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in jfmje__edm))
        vrty__weald += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            vrty__weald += ("    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".
                format(vkk__xsmo.native_name))
            vrty__weald += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n"
                .format(paym__wei.native_name))
            vrty__weald += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                eeye__odcp.native_name)
            vrty__weald += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(vkk__xsmo.native_name))
            vrty__weald += (
                "    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n".format
                (paym__wei.native_name))
            vrty__weald += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(eeye__odcp.native_name))
        else:
            vrty__weald += '    cpp_cb_update_addr = 0\n'
            vrty__weald += '    cpp_cb_combine_addr = 0\n'
            vrty__weald += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            wen__wtc = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[wen__wtc.native_name] = wen__wtc
            gb_agg_cfunc_addr[wen__wtc.native_name] = wen__wtc.address
            vrty__weald += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n"
                .format(wen__wtc.native_name))
            vrty__weald += (
                "    cpp_cb_general_addr = get_agg_udf_addr('{}')\n".format
                (wen__wtc.native_name))
        else:
            vrty__weald += '    cpp_cb_general_addr = 0\n'
    else:
        vrty__weald += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        vrty__weald += '    cpp_cb_update_addr = 0\n'
        vrty__weald += '    cpp_cb_combine_addr = 0\n'
        vrty__weald += '    cpp_cb_eval_addr = 0\n'
        vrty__weald += '    cpp_cb_general_addr = 0\n'
    vrty__weald += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(mdgmo__emk.ftype)) for
        mdgmo__emk in allfuncs] + ['0']))
    vrty__weald += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(
        str(glvj__jqp))
    if len(avbu__cyf) > 0:
        vrty__weald += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(avbu__cyf))
    else:
        vrty__weald += '    udf_ncols = np.array([0], np.int32)\n'
    if kmemy__wsxuy:
        vrty__weald += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        vrty__weald += '    arr_info = array_to_info(arr_type)\n'
        vrty__weald += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        vrty__weald += '    pivot_info = array_to_info(pivot_arr)\n'
        vrty__weald += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        vrty__weald += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, oowld__zuiu, agg_node.return_key, agg_node.same_index)
            )
        vrty__weald += '    delete_info_decref_array(pivot_info)\n'
        vrty__weald += '    delete_info_decref_array(arr_info)\n'
    else:
        vrty__weald += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, oowld__zuiu,
            zfeuf__hpict, tehed__zcsac, zcce__hmaya, agg_node.return_key,
            agg_node.same_index, agg_node.dropna))
    thsbw__hahjn = 0
    if agg_node.return_key:
        for jjfn__cgr, tzygk__oycq in enumerate(eajm__lul):
            vrty__weald += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(tzygk__oycq, thsbw__hahjn, tzygk__oycq))
            thsbw__hahjn += 1
    for jjfn__cgr, pzx__htpb in enumerate(zgnr__xly.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(tcs__pnowi, bodo.
            CategoricalArrayType):
            vrty__weald += f"""    {pzx__htpb} = info_to_array(info_from_table(out_table, {thsbw__hahjn}), {pzx__htpb + '_dummy'})
"""
        else:
            vrty__weald += f"""    {pzx__htpb} = info_to_array(info_from_table(out_table, {thsbw__hahjn}), out_typs[{jjfn__cgr}])
"""
        thsbw__hahjn += 1
    if agg_node.same_index:
        vrty__weald += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(thsbw__hahjn))
        thsbw__hahjn += 1
    vrty__weald += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    vrty__weald += '    delete_table_decref_arrays(table)\n'
    vrty__weald += '    delete_table_decref_arrays(udf_table_dummy)\n'
    vrty__weald += '    delete_table(out_table)\n'
    vrty__weald += f'    ev_clean.finalize()\n'
    jceny__zmvo = tuple(zgnr__xly.values())
    if agg_node.return_key:
        jceny__zmvo += tuple(eajm__lul)
    vrty__weald += '    return ({},{})\n'.format(', '.join(jceny__zmvo), 
        ' out_index_arg,' if agg_node.same_index else '')
    yxl__acyd = {}
    exec(vrty__weald, {'out_typs': out_col_typs}, yxl__acyd)
    oiud__qlckt = yxl__acyd['agg_top']
    return oiud__qlckt


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for vgxd__wcr in block.body:
            if is_call_assign(vgxd__wcr) and find_callname(f_ir, vgxd__wcr.
                value) == ('len', 'builtins') and vgxd__wcr.value.args[0
                ].name == f_ir.arg_names[0]:
                lozpa__kidd = get_definition(f_ir, vgxd__wcr.value.func)
                lozpa__kidd.name = 'dummy_agg_count'
                lozpa__kidd.value = dummy_agg_count
    unah__xip = get_name_var_table(f_ir.blocks)
    xvdv__kgsz = {}
    for name, avady__ogjqd in unah__xip.items():
        xvdv__kgsz[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, xvdv__kgsz)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    eqt__uilc = numba.core.compiler.Flags()
    eqt__uilc.nrt = True
    nzmdx__ooxmz = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, eqt__uilc)
    nzmdx__ooxmz.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, kkxg__qkzk, calltypes, avady__ogjqd = (numba.core.typed_passes
        .type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    jnrn__aieir = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    jnmi__esejz = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    tzv__uyuw = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    ofmn__giwe = tzv__uyuw(typemap, calltypes)
    pm = jnmi__esejz(typingctx, targetctx, None, f_ir, typemap, kkxg__qkzk,
        calltypes, ofmn__giwe, {}, eqt__uilc, None)
    qjks__vzjv = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = jnmi__esejz(typingctx, targetctx, None, f_ir, typemap, kkxg__qkzk,
        calltypes, ofmn__giwe, {}, eqt__uilc, qjks__vzjv)
    dqh__qxxl = numba.core.typed_passes.InlineOverloads()
    dqh__qxxl.run_pass(pm)
    ysw__uwl = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    ysw__uwl.run()
    for block in f_ir.blocks.values():
        for vgxd__wcr in block.body:
            if is_assign(vgxd__wcr) and isinstance(vgxd__wcr.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[vgxd__wcr.target.name],
                SeriesType):
                djtau__ztbf = typemap.pop(vgxd__wcr.target.name)
                typemap[vgxd__wcr.target.name] = djtau__ztbf.data
            if is_call_assign(vgxd__wcr) and find_callname(f_ir, vgxd__wcr.
                value) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[vgxd__wcr.target.name].remove(vgxd__wcr.value
                    )
                vgxd__wcr.value = vgxd__wcr.value.args[0]
                f_ir._definitions[vgxd__wcr.target.name].append(vgxd__wcr.value
                    )
            if is_call_assign(vgxd__wcr) and find_callname(f_ir, vgxd__wcr.
                value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[vgxd__wcr.target.name].remove(vgxd__wcr.value
                    )
                vgxd__wcr.value = ir.Const(False, vgxd__wcr.loc)
                f_ir._definitions[vgxd__wcr.target.name].append(vgxd__wcr.value
                    )
            if is_call_assign(vgxd__wcr) and find_callname(f_ir, vgxd__wcr.
                value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[vgxd__wcr.target.name].remove(vgxd__wcr.value
                    )
                vgxd__wcr.value = ir.Const(False, vgxd__wcr.loc)
                f_ir._definitions[vgxd__wcr.target.name].append(vgxd__wcr.value
                    )
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    ozc__lbrm = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, jnrn__aieir)
    ozc__lbrm.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    ccsx__jwwk = numba.core.compiler.StateDict()
    ccsx__jwwk.func_ir = f_ir
    ccsx__jwwk.typemap = typemap
    ccsx__jwwk.calltypes = calltypes
    ccsx__jwwk.typingctx = typingctx
    ccsx__jwwk.targetctx = targetctx
    ccsx__jwwk.return_type = kkxg__qkzk
    numba.core.rewrites.rewrite_registry.apply('after-inference', ccsx__jwwk)
    qulm__gkg = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        kkxg__qkzk, typingctx, targetctx, jnrn__aieir, eqt__uilc, {})
    qulm__gkg.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            yxdgw__fbz = ctypes.pythonapi.PyCell_Get
            yxdgw__fbz.restype = ctypes.py_object
            yxdgw__fbz.argtypes = ctypes.py_object,
            qlvb__hdpx = tuple(yxdgw__fbz(yfmwq__jxew) for yfmwq__jxew in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            qlvb__hdpx = closure.items
        assert len(code.co_freevars) == len(qlvb__hdpx)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, qlvb__hdpx
            )


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
        cuini__xwyb = SeriesType(in_col_typ.dtype, in_col_typ, None,
            string_type)
        f_ir, pm = compile_to_optimized_ir(func, (cuini__xwyb,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        ewfy__kqsq, arr_var = _rm_arg_agg_block(block, pm.typemap)
        lwqz__gwd = -1
        for jjfn__cgr, vgxd__wcr in enumerate(ewfy__kqsq):
            if isinstance(vgxd__wcr, numba.parfors.parfor.Parfor):
                assert lwqz__gwd == -1, 'only one parfor for aggregation function'
                lwqz__gwd = jjfn__cgr
        parfor = None
        if lwqz__gwd != -1:
            parfor = ewfy__kqsq[lwqz__gwd]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = ewfy__kqsq[:lwqz__gwd] + parfor.init_block.body
        eval_nodes = ewfy__kqsq[lwqz__gwd + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for vgxd__wcr in init_nodes:
            if is_assign(vgxd__wcr) and vgxd__wcr.target.name in redvars:
                ind = redvars.index(vgxd__wcr.target.name)
                reduce_vars[ind] = vgxd__wcr.target
        var_types = [pm.typemap[ddgx__valf] for ddgx__valf in redvars]
        nbxzk__hgj = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        sqer__efsl = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        dqwp__fkofl = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(dqwp__fkofl)
        self.all_update_funcs.append(sqer__efsl)
        self.all_combine_funcs.append(nbxzk__hgj)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        ouasj__irjo = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        tmawi__glsqn = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        wznhp__lfqty = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        ztmum__mnfpb = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, ouasj__irjo, tmawi__glsqn, wznhp__lfqty,
            ztmum__mnfpb)


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
    uvtba__anx = []
    for t, mdgmo__emk in zip(in_col_types, agg_func):
        uvtba__anx.append((t, mdgmo__emk))
    nwvib__ouji = RegularUDFGenerator(in_col_types, out_col_types,
        pivot_typ, pivot_values, is_crosstab, typingctx, targetctx)
    hht__gshnj = GeneralUDFGenerator()
    for in_col_typ, func in uvtba__anx:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            nwvib__ouji.add_udf(in_col_typ, func)
        except:
            hht__gshnj.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = nwvib__ouji.gen_all_func()
    general_udf_funcs = hht__gshnj.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    put__fazk = compute_use_defs(parfor.loop_body)
    dmvf__pkoc = set()
    for ewau__ihdf in put__fazk.usemap.values():
        dmvf__pkoc |= ewau__ihdf
    tqxt__ldgfu = set()
    for ewau__ihdf in put__fazk.defmap.values():
        tqxt__ldgfu |= ewau__ihdf
    iukr__dzzwu = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    iukr__dzzwu.body = eval_nodes
    tny__wurxv = compute_use_defs({(0): iukr__dzzwu})
    titdw__tnuye = tny__wurxv.usemap[0]
    fouz__qpsau = set()
    begy__utsp = []
    sgha__xnyxo = []
    for vgxd__wcr in reversed(init_nodes):
        wrlqm__jude = {ddgx__valf.name for ddgx__valf in vgxd__wcr.list_vars()}
        if is_assign(vgxd__wcr):
            ddgx__valf = vgxd__wcr.target.name
            wrlqm__jude.remove(ddgx__valf)
            if (ddgx__valf in dmvf__pkoc and ddgx__valf not in fouz__qpsau and
                ddgx__valf not in titdw__tnuye and ddgx__valf not in
                tqxt__ldgfu):
                sgha__xnyxo.append(vgxd__wcr)
                dmvf__pkoc |= wrlqm__jude
                tqxt__ldgfu.add(ddgx__valf)
                continue
        fouz__qpsau |= wrlqm__jude
        begy__utsp.append(vgxd__wcr)
    sgha__xnyxo.reverse()
    begy__utsp.reverse()
    zebk__gdhcw = min(parfor.loop_body.keys())
    grlpo__asdzf = parfor.loop_body[zebk__gdhcw]
    grlpo__asdzf.body = sgha__xnyxo + grlpo__asdzf.body
    return begy__utsp


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    tps__zrfb = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    biiz__eiu = set()
    yixa__ehji = []
    for vgxd__wcr in init_nodes:
        if is_assign(vgxd__wcr) and isinstance(vgxd__wcr.value, ir.Global
            ) and isinstance(vgxd__wcr.value.value, pytypes.FunctionType
            ) and vgxd__wcr.value.value in tps__zrfb:
            biiz__eiu.add(vgxd__wcr.target.name)
        elif is_call_assign(vgxd__wcr
            ) and vgxd__wcr.value.func.name in biiz__eiu:
            pass
        else:
            yixa__ehji.append(vgxd__wcr)
    init_nodes = yixa__ehji
    ixh__odg = types.Tuple(var_types)
    hpv__kdlfu = lambda : None
    f_ir = compile_to_numba_ir(hpv__kdlfu, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    racsu__jtt = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    mfyz__vykkr = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        racsu__jtt, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [mfyz__vykkr] + block.body
    block.body[-2].value.value = racsu__jtt
    tzbag__mhauk = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        ixh__odg, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rxdvh__ppbnj = numba.core.target_extension.dispatcher_registry[cpu_target](
        hpv__kdlfu)
    rxdvh__ppbnj.add_overload(tzbag__mhauk)
    return rxdvh__ppbnj


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    hsns__rndm = len(update_funcs)
    dtu__ebb = len(in_col_types)
    if pivot_values is not None:
        assert dtu__ebb == 1
    vrty__weald = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        zmbdc__hfcza = redvar_offsets[dtu__ebb]
        vrty__weald += '  pv = pivot_arr[i]\n'
        for uhiog__qmz, prjca__bvf in enumerate(pivot_values):
            pped__rgtz = 'el' if uhiog__qmz != 0 else ''
            vrty__weald += "  {}if pv == '{}':\n".format(pped__rgtz, prjca__bvf
                )
            aikj__hukxg = zmbdc__hfcza * uhiog__qmz
            kpvn__blw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                jjfn__cgr) for jjfn__cgr in range(aikj__hukxg +
                redvar_offsets[0], aikj__hukxg + redvar_offsets[1])])
            abkz__mvany = 'data_in[0][i]'
            if is_crosstab:
                abkz__mvany = '0'
            vrty__weald += '    {} = update_vars_0({}, {})\n'.format(kpvn__blw,
                kpvn__blw, abkz__mvany)
    else:
        for uhiog__qmz in range(hsns__rndm):
            kpvn__blw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                jjfn__cgr) for jjfn__cgr in range(redvar_offsets[uhiog__qmz
                ], redvar_offsets[uhiog__qmz + 1])])
            if kpvn__blw:
                vrty__weald += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(kpvn__blw, uhiog__qmz, kpvn__blw, 0 if dtu__ebb ==
                    1 else uhiog__qmz))
    vrty__weald += '  return\n'
    gihel__xgssz = {}
    for jjfn__cgr, mdgmo__emk in enumerate(update_funcs):
        gihel__xgssz['update_vars_{}'.format(jjfn__cgr)] = mdgmo__emk
    yxl__acyd = {}
    exec(vrty__weald, gihel__xgssz, yxl__acyd)
    drapk__zyo = yxl__acyd['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(drapk__zyo)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    tmci__twkd = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = tmci__twkd, tmci__twkd, types.intp, types.intp, pivot_typ
    rli__mazd = len(redvar_offsets) - 1
    zmbdc__hfcza = redvar_offsets[rli__mazd]
    vrty__weald = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert rli__mazd == 1
        for aap__mvdq in range(len(pivot_values)):
            aikj__hukxg = zmbdc__hfcza * aap__mvdq
            kpvn__blw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                jjfn__cgr) for jjfn__cgr in range(aikj__hukxg +
                redvar_offsets[0], aikj__hukxg + redvar_offsets[1])])
            fsptz__tun = ', '.join(['recv_arrs[{}][i]'.format(jjfn__cgr) for
                jjfn__cgr in range(aikj__hukxg + redvar_offsets[0], 
                aikj__hukxg + redvar_offsets[1])])
            vrty__weald += '  {} = combine_vars_0({}, {})\n'.format(kpvn__blw,
                kpvn__blw, fsptz__tun)
    else:
        for uhiog__qmz in range(rli__mazd):
            kpvn__blw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                jjfn__cgr) for jjfn__cgr in range(redvar_offsets[uhiog__qmz
                ], redvar_offsets[uhiog__qmz + 1])])
            fsptz__tun = ', '.join(['recv_arrs[{}][i]'.format(jjfn__cgr) for
                jjfn__cgr in range(redvar_offsets[uhiog__qmz],
                redvar_offsets[uhiog__qmz + 1])])
            if fsptz__tun:
                vrty__weald += '  {} = combine_vars_{}({}, {})\n'.format(
                    kpvn__blw, uhiog__qmz, kpvn__blw, fsptz__tun)
    vrty__weald += '  return\n'
    gihel__xgssz = {}
    for jjfn__cgr, mdgmo__emk in enumerate(combine_funcs):
        gihel__xgssz['combine_vars_{}'.format(jjfn__cgr)] = mdgmo__emk
    yxl__acyd = {}
    exec(vrty__weald, gihel__xgssz, yxl__acyd)
    sxu__daklg = yxl__acyd['combine_all_f']
    f_ir = compile_to_numba_ir(sxu__daklg, gihel__xgssz)
    wznhp__lfqty = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rxdvh__ppbnj = numba.core.target_extension.dispatcher_registry[cpu_target](
        sxu__daklg)
    rxdvh__ppbnj.add_overload(wznhp__lfqty)
    return rxdvh__ppbnj


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    tmci__twkd = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    out_col_typs = types.Tuple(out_col_typs)
    rli__mazd = len(redvar_offsets) - 1
    zmbdc__hfcza = redvar_offsets[rli__mazd]
    vrty__weald = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert rli__mazd == 1
        for uhiog__qmz in range(len(pivot_values)):
            aikj__hukxg = zmbdc__hfcza * uhiog__qmz
            kpvn__blw = ', '.join(['redvar_arrs[{}][j]'.format(jjfn__cgr) for
                jjfn__cgr in range(aikj__hukxg + redvar_offsets[0], 
                aikj__hukxg + redvar_offsets[1])])
            vrty__weald += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                uhiog__qmz, kpvn__blw)
    else:
        for uhiog__qmz in range(rli__mazd):
            kpvn__blw = ', '.join(['redvar_arrs[{}][j]'.format(jjfn__cgr) for
                jjfn__cgr in range(redvar_offsets[uhiog__qmz],
                redvar_offsets[uhiog__qmz + 1])])
            vrty__weald += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                uhiog__qmz, uhiog__qmz, kpvn__blw)
    vrty__weald += '  return\n'
    gihel__xgssz = {}
    for jjfn__cgr, mdgmo__emk in enumerate(eval_funcs):
        gihel__xgssz['eval_vars_{}'.format(jjfn__cgr)] = mdgmo__emk
    yxl__acyd = {}
    exec(vrty__weald, gihel__xgssz, yxl__acyd)
    dxfp__jzfhu = yxl__acyd['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(dxfp__jzfhu)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    tdbm__dyau = len(var_types)
    jlz__qamq = [f'in{jjfn__cgr}' for jjfn__cgr in range(tdbm__dyau)]
    ixh__odg = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    ccwdn__pvu = ixh__odg(0)
    vrty__weald = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        jlz__qamq))
    yxl__acyd = {}
    exec(vrty__weald, {'_zero': ccwdn__pvu}, yxl__acyd)
    fhukm__psfa = yxl__acyd['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(fhukm__psfa, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': ccwdn__pvu}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    sva__yac = []
    for jjfn__cgr, ddgx__valf in enumerate(reduce_vars):
        sva__yac.append(ir.Assign(block.body[jjfn__cgr].target, ddgx__valf,
            ddgx__valf.loc))
        for iwxot__ucr in ddgx__valf.versioned_names:
            sva__yac.append(ir.Assign(ddgx__valf, ir.Var(ddgx__valf.scope,
                iwxot__ucr, ddgx__valf.loc), ddgx__valf.loc))
    block.body = block.body[:tdbm__dyau] + sva__yac + eval_nodes
    dqwp__fkofl = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ixh__odg, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rxdvh__ppbnj = numba.core.target_extension.dispatcher_registry[cpu_target](
        fhukm__psfa)
    rxdvh__ppbnj.add_overload(dqwp__fkofl)
    return rxdvh__ppbnj


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    tdbm__dyau = len(redvars)
    oim__tcc = [f'v{jjfn__cgr}' for jjfn__cgr in range(tdbm__dyau)]
    jlz__qamq = [f'in{jjfn__cgr}' for jjfn__cgr in range(tdbm__dyau)]
    vrty__weald = 'def agg_combine({}):\n'.format(', '.join(oim__tcc +
        jlz__qamq))
    jvy__upyut = wrap_parfor_blocks(parfor)
    zjcap__btk = find_topo_order(jvy__upyut)
    zjcap__btk = zjcap__btk[1:]
    unwrap_parfor_blocks(parfor)
    lcsoi__zbum = {}
    kob__kpqm = []
    for here__lxios in zjcap__btk:
        fsl__pgr = parfor.loop_body[here__lxios]
        for vgxd__wcr in fsl__pgr.body:
            if is_call_assign(vgxd__wcr) and guard(find_callname, f_ir,
                vgxd__wcr.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = vgxd__wcr.value.args
                ipfvg__mnfx = []
                zgr__mykfs = []
                for ddgx__valf in args[:-1]:
                    ind = redvars.index(ddgx__valf.name)
                    kob__kpqm.append(ind)
                    ipfvg__mnfx.append('v{}'.format(ind))
                    zgr__mykfs.append('in{}'.format(ind))
                dfi__bfc = '__special_combine__{}'.format(len(lcsoi__zbum))
                vrty__weald += '    ({},) = {}({})\n'.format(', '.join(
                    ipfvg__mnfx), dfi__bfc, ', '.join(ipfvg__mnfx + zgr__mykfs)
                    )
                tti__asr = ir.Expr.call(args[-1], [], (), fsl__pgr.loc)
                abpj__tkxx = guard(find_callname, f_ir, tti__asr)
                assert abpj__tkxx == ('_var_combine', 'bodo.ir.aggregate')
                abpj__tkxx = bodo.ir.aggregate._var_combine
                lcsoi__zbum[dfi__bfc] = abpj__tkxx
            if is_assign(vgxd__wcr) and vgxd__wcr.target.name in redvars:
                wlcxr__gtn = vgxd__wcr.target.name
                ind = redvars.index(wlcxr__gtn)
                if ind in kob__kpqm:
                    continue
                if len(f_ir._definitions[wlcxr__gtn]) == 2:
                    var_def = f_ir._definitions[wlcxr__gtn][0]
                    vrty__weald += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[wlcxr__gtn][1]
                    vrty__weald += _match_reduce_def(var_def, f_ir, ind)
    vrty__weald += '    return {}'.format(', '.join(['v{}'.format(jjfn__cgr
        ) for jjfn__cgr in range(tdbm__dyau)]))
    yxl__acyd = {}
    exec(vrty__weald, {}, yxl__acyd)
    bmcqg__uyxt = yxl__acyd['agg_combine']
    arg_typs = tuple(2 * var_types)
    gihel__xgssz = {'numba': numba, 'bodo': bodo, 'np': np}
    gihel__xgssz.update(lcsoi__zbum)
    f_ir = compile_to_numba_ir(bmcqg__uyxt, gihel__xgssz, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=pm.
        typemap, calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    ixh__odg = pm.typemap[block.body[-1].value.name]
    nbxzk__hgj = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ixh__odg, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rxdvh__ppbnj = numba.core.target_extension.dispatcher_registry[cpu_target](
        bmcqg__uyxt)
    rxdvh__ppbnj.add_overload(nbxzk__hgj)
    return rxdvh__ppbnj


def _match_reduce_def(var_def, f_ir, ind):
    vrty__weald = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        vrty__weald = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        cuewm__mkng = guard(find_callname, f_ir, var_def)
        if cuewm__mkng == ('min', 'builtins'):
            vrty__weald = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if cuewm__mkng == ('max', 'builtins'):
            vrty__weald = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return vrty__weald


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    tdbm__dyau = len(redvars)
    dhwyc__uby = 1
    mzcj__lfuyr = []
    for jjfn__cgr in range(dhwyc__uby):
        guh__hpv = ir.Var(arr_var.scope, f'$input{jjfn__cgr}', arr_var.loc)
        mzcj__lfuyr.append(guh__hpv)
    nnk__dwyx = parfor.loop_nests[0].index_variable
    isybj__kexmr = [0] * tdbm__dyau
    for fsl__pgr in parfor.loop_body.values():
        tvwtq__ech = []
        for vgxd__wcr in fsl__pgr.body:
            if is_var_assign(vgxd__wcr
                ) and vgxd__wcr.value.name == nnk__dwyx.name:
                continue
            if is_getitem(vgxd__wcr
                ) and vgxd__wcr.value.value.name == arr_var.name:
                vgxd__wcr.value = mzcj__lfuyr[0]
            if is_call_assign(vgxd__wcr) and guard(find_callname, pm.
                func_ir, vgxd__wcr.value) == ('isna', 'bodo.libs.array_kernels'
                ) and vgxd__wcr.value.args[0].name == arr_var.name:
                vgxd__wcr.value = ir.Const(False, vgxd__wcr.target.loc)
            if is_assign(vgxd__wcr) and vgxd__wcr.target.name in redvars:
                ind = redvars.index(vgxd__wcr.target.name)
                isybj__kexmr[ind] = vgxd__wcr.target
            tvwtq__ech.append(vgxd__wcr)
        fsl__pgr.body = tvwtq__ech
    oim__tcc = ['v{}'.format(jjfn__cgr) for jjfn__cgr in range(tdbm__dyau)]
    jlz__qamq = ['in{}'.format(jjfn__cgr) for jjfn__cgr in range(dhwyc__uby)]
    vrty__weald = 'def agg_update({}):\n'.format(', '.join(oim__tcc +
        jlz__qamq))
    vrty__weald += '    __update_redvars()\n'
    vrty__weald += '    return {}'.format(', '.join(['v{}'.format(jjfn__cgr
        ) for jjfn__cgr in range(tdbm__dyau)]))
    yxl__acyd = {}
    exec(vrty__weald, {}, yxl__acyd)
    vrsy__ahh = yxl__acyd['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * dhwyc__uby)
    f_ir = compile_to_numba_ir(vrsy__ahh, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    jcuz__znoxv = f_ir.blocks.popitem()[1].body
    ixh__odg = pm.typemap[jcuz__znoxv[-1].value.name]
    jvy__upyut = wrap_parfor_blocks(parfor)
    zjcap__btk = find_topo_order(jvy__upyut)
    zjcap__btk = zjcap__btk[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    grlpo__asdzf = f_ir.blocks[zjcap__btk[0]]
    okd__jfdwk = f_ir.blocks[zjcap__btk[-1]]
    ntejw__ldew = jcuz__znoxv[:tdbm__dyau + dhwyc__uby]
    if tdbm__dyau > 1:
        lud__wvli = jcuz__znoxv[-3:]
        assert is_assign(lud__wvli[0]) and isinstance(lud__wvli[0].value,
            ir.Expr) and lud__wvli[0].value.op == 'build_tuple'
    else:
        lud__wvli = jcuz__znoxv[-2:]
    for jjfn__cgr in range(tdbm__dyau):
        rszs__lsp = jcuz__znoxv[jjfn__cgr].target
        yzalw__xdisi = ir.Assign(rszs__lsp, isybj__kexmr[jjfn__cgr],
            rszs__lsp.loc)
        ntejw__ldew.append(yzalw__xdisi)
    for jjfn__cgr in range(tdbm__dyau, tdbm__dyau + dhwyc__uby):
        rszs__lsp = jcuz__znoxv[jjfn__cgr].target
        yzalw__xdisi = ir.Assign(rszs__lsp, mzcj__lfuyr[jjfn__cgr -
            tdbm__dyau], rszs__lsp.loc)
        ntejw__ldew.append(yzalw__xdisi)
    grlpo__asdzf.body = ntejw__ldew + grlpo__asdzf.body
    zaxz__ibpaf = []
    for jjfn__cgr in range(tdbm__dyau):
        rszs__lsp = jcuz__znoxv[jjfn__cgr].target
        yzalw__xdisi = ir.Assign(isybj__kexmr[jjfn__cgr], rszs__lsp,
            rszs__lsp.loc)
        zaxz__ibpaf.append(yzalw__xdisi)
    okd__jfdwk.body += zaxz__ibpaf + lud__wvli
    cfvbu__hanj = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ixh__odg, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rxdvh__ppbnj = numba.core.target_extension.dispatcher_registry[cpu_target](
        vrsy__ahh)
    rxdvh__ppbnj.add_overload(cfvbu__hanj)
    return rxdvh__ppbnj


def _rm_arg_agg_block(block, typemap):
    ewfy__kqsq = []
    arr_var = None
    for jjfn__cgr, vgxd__wcr in enumerate(block.body):
        if is_assign(vgxd__wcr) and isinstance(vgxd__wcr.value, ir.Arg):
            arr_var = vgxd__wcr.target
            gqw__lcp = typemap[arr_var.name]
            if not isinstance(gqw__lcp, types.ArrayCompatible):
                ewfy__kqsq += block.body[jjfn__cgr + 1:]
                break
            leqjh__gfczj = block.body[jjfn__cgr + 1]
            assert is_assign(leqjh__gfczj) and isinstance(leqjh__gfczj.
                value, ir.Expr
                ) and leqjh__gfczj.value.op == 'getattr' and leqjh__gfczj.value.attr == 'shape' and leqjh__gfczj.value.value.name == arr_var.name
            otwbh__kyek = leqjh__gfczj.target
            xne__eltk = block.body[jjfn__cgr + 2]
            assert is_assign(xne__eltk) and isinstance(xne__eltk.value, ir.Expr
                ) and xne__eltk.value.op == 'static_getitem' and xne__eltk.value.value.name == otwbh__kyek.name
            ewfy__kqsq += block.body[jjfn__cgr + 3:]
            break
        ewfy__kqsq.append(vgxd__wcr)
    return ewfy__kqsq, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    jvy__upyut = wrap_parfor_blocks(parfor)
    zjcap__btk = find_topo_order(jvy__upyut)
    zjcap__btk = zjcap__btk[1:]
    unwrap_parfor_blocks(parfor)
    for here__lxios in reversed(zjcap__btk):
        for vgxd__wcr in reversed(parfor.loop_body[here__lxios].body):
            if isinstance(vgxd__wcr, ir.Assign) and (vgxd__wcr.target.name in
                parfor_params or vgxd__wcr.target.name in var_to_param):
                btlz__bwzs = vgxd__wcr.target.name
                rhs = vgxd__wcr.value
                mlvjn__jkasg = (btlz__bwzs if btlz__bwzs in parfor_params else
                    var_to_param[btlz__bwzs])
                xirwz__yfpw = []
                if isinstance(rhs, ir.Var):
                    xirwz__yfpw = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    xirwz__yfpw = [ddgx__valf.name for ddgx__valf in
                        vgxd__wcr.value.list_vars()]
                param_uses[mlvjn__jkasg].extend(xirwz__yfpw)
                for ddgx__valf in xirwz__yfpw:
                    var_to_param[ddgx__valf] = mlvjn__jkasg
            if isinstance(vgxd__wcr, Parfor):
                get_parfor_reductions(vgxd__wcr, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for qyv__clyr, xirwz__yfpw in param_uses.items():
        if qyv__clyr in xirwz__yfpw and qyv__clyr not in reduce_varnames:
            reduce_varnames.append(qyv__clyr)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
