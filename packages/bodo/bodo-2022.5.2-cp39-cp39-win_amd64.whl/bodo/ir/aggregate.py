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
            edee__lod = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            caky__rcu = cgutils.get_or_insert_function(builder.module,
                edee__lod, sym._literal_value)
            builder.call(caky__rcu, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            edee__lod = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            caky__rcu = cgutils.get_or_insert_function(builder.module,
                edee__lod, sym._literal_value)
            builder.call(caky__rcu, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            edee__lod = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            caky__rcu = cgutils.get_or_insert_function(builder.module,
                edee__lod, sym._literal_value)
            builder.call(caky__rcu, [context.get_constant_null(sig.args[0]),
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
        mhv__hrw = True
        wjo__lpct = 1
        kfwp__xuyf = -1
        if isinstance(rhs, ir.Expr):
            for dsqtw__wtl in rhs.kws:
                if func_name in list_cumulative:
                    if dsqtw__wtl[0] == 'skipna':
                        mhv__hrw = guard(find_const, func_ir, dsqtw__wtl[1])
                        if not isinstance(mhv__hrw, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if dsqtw__wtl[0] == 'dropna':
                        mhv__hrw = guard(find_const, func_ir, dsqtw__wtl[1])
                        if not isinstance(mhv__hrw, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            wjo__lpct = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', wjo__lpct)
            wjo__lpct = guard(find_const, func_ir, wjo__lpct)
        if func_name == 'head':
            kfwp__xuyf = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(kfwp__xuyf, int):
                kfwp__xuyf = guard(find_const, func_ir, kfwp__xuyf)
            if kfwp__xuyf < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = mhv__hrw
        func.periods = wjo__lpct
        func.head_n = kfwp__xuyf
        if func_name == 'transform':
            kws = dict(rhs.kws)
            nbsoz__aqg = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            xekub__sqyqp = typemap[nbsoz__aqg.name]
            gov__usoh = None
            if isinstance(xekub__sqyqp, str):
                gov__usoh = xekub__sqyqp
            elif is_overload_constant_str(xekub__sqyqp):
                gov__usoh = get_overload_const_str(xekub__sqyqp)
            elif bodo.utils.typing.is_builtin_function(xekub__sqyqp):
                gov__usoh = bodo.utils.typing.get_builtin_function_name(
                    xekub__sqyqp)
            if gov__usoh not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {gov__usoh}')
            func.transform_func = supported_agg_funcs.index(gov__usoh)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    nbsoz__aqg = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if nbsoz__aqg == '':
        xekub__sqyqp = types.none
    else:
        xekub__sqyqp = typemap[nbsoz__aqg.name]
    if is_overload_constant_dict(xekub__sqyqp):
        bqn__zxd = get_overload_constant_dict(xekub__sqyqp)
        svmum__srtta = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in bqn__zxd.values()]
        return svmum__srtta
    if xekub__sqyqp == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(xekub__sqyqp, types.BaseTuple) or is_overload_constant_list(
        xekub__sqyqp):
        svmum__srtta = []
        xgra__lceja = 0
        if is_overload_constant_list(xekub__sqyqp):
            bxwr__cml = get_overload_const_list(xekub__sqyqp)
        else:
            bxwr__cml = xekub__sqyqp.types
        for t in bxwr__cml:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                svmum__srtta.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(bxwr__cml) > 1:
                    func.fname = '<lambda_' + str(xgra__lceja) + '>'
                    xgra__lceja += 1
                svmum__srtta.append(func)
        return [svmum__srtta]
    if is_overload_constant_str(xekub__sqyqp):
        func_name = get_overload_const_str(xekub__sqyqp)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(xekub__sqyqp):
        func_name = bodo.utils.typing.get_builtin_function_name(xekub__sqyqp)
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
        xgra__lceja = 0
        rdog__gyees = []
        for szr__zui in f_val:
            func = get_agg_func_udf(func_ir, szr__zui, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{xgra__lceja}>'
                xgra__lceja += 1
            rdog__gyees.append(func)
        return rdog__gyees
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
    gov__usoh = code.co_name
    return gov__usoh


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
            frpa__vke = types.DType(args[0])
            return signature(frpa__vke, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    mgy__wxjw = nobs_a + nobs_b
    vbyrn__aiqur = (nobs_a * mean_a + nobs_b * mean_b) / mgy__wxjw
    ikus__msbu = mean_b - mean_a
    jac__ygdd = (ssqdm_a + ssqdm_b + ikus__msbu * ikus__msbu * nobs_a *
        nobs_b / mgy__wxjw)
    return jac__ygdd, vbyrn__aiqur, mgy__wxjw


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
        sly__pwcb = ''
        for wwbs__pcjum, sxa__xorac in self.df_out_vars.items():
            sly__pwcb += "'{}':{}, ".format(wwbs__pcjum, sxa__xorac.name)
        mddy__bcrwz = '{}{{{}}}'.format(self.df_out, sly__pwcb)
        mpvy__vlf = ''
        for wwbs__pcjum, sxa__xorac in self.df_in_vars.items():
            mpvy__vlf += "'{}':{}, ".format(wwbs__pcjum, sxa__xorac.name)
        ohs__auz = '{}{{{}}}'.format(self.df_in, mpvy__vlf)
        cjhjf__vwnj = 'pivot {}:{}'.format(self.pivot_arr.name, self.
            pivot_values) if self.pivot_arr is not None else ''
        key_names = ','.join([str(qpv__jlmu) for qpv__jlmu in self.key_names])
        ath__nyf = ','.join([sxa__xorac.name for sxa__xorac in self.key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(mddy__bcrwz,
            ohs__auz, key_names, ath__nyf, cjhjf__vwnj)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        jhtk__aeglx, jelue__oiba = self.gb_info_out.pop(out_col_name)
        if jhtk__aeglx is None and not self.is_crosstab:
            return
        oiblf__eelu = self.gb_info_in[jhtk__aeglx]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for beryn__pjuoh, (func, sly__pwcb) in enumerate(oiblf__eelu):
                try:
                    sly__pwcb.remove(out_col_name)
                    if len(sly__pwcb) == 0:
                        oiblf__eelu.pop(beryn__pjuoh)
                        break
                except ValueError as jwgx__xcym:
                    continue
        else:
            for beryn__pjuoh, (func, cin__slqqu) in enumerate(oiblf__eelu):
                if cin__slqqu == out_col_name:
                    oiblf__eelu.pop(beryn__pjuoh)
                    break
        if len(oiblf__eelu) == 0:
            self.gb_info_in.pop(jhtk__aeglx)
            self.df_in_vars.pop(jhtk__aeglx)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({sxa__xorac.name for sxa__xorac in aggregate_node.key_arrs})
    use_set.update({sxa__xorac.name for sxa__xorac in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({sxa__xorac.name for sxa__xorac in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({sxa__xorac.name for sxa__xorac in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    luegf__gmocy = [oyoz__qpjn for oyoz__qpjn, oxg__tzbc in aggregate_node.
        df_out_vars.items() if oxg__tzbc.name not in lives]
    for fei__qjqx in luegf__gmocy:
        aggregate_node.remove_out_col(fei__qjqx)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(sxa__xorac.name not in lives for
        sxa__xorac in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    eocql__ezfzh = set(sxa__xorac.name for sxa__xorac in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        eocql__ezfzh.update({sxa__xorac.name for sxa__xorac in
            aggregate_node.out_key_vars})
    return set(), eocql__ezfzh


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for beryn__pjuoh in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[beryn__pjuoh] = replace_vars_inner(
            aggregate_node.key_arrs[beryn__pjuoh], var_dict)
    for oyoz__qpjn in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[oyoz__qpjn] = replace_vars_inner(
            aggregate_node.df_in_vars[oyoz__qpjn], var_dict)
    for oyoz__qpjn in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[oyoz__qpjn] = replace_vars_inner(
            aggregate_node.df_out_vars[oyoz__qpjn], var_dict)
    if aggregate_node.out_key_vars is not None:
        for beryn__pjuoh in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[beryn__pjuoh] = replace_vars_inner(
                aggregate_node.out_key_vars[beryn__pjuoh], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for beryn__pjuoh in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[beryn__pjuoh] = visit_vars_inner(aggregate_node
            .key_arrs[beryn__pjuoh], callback, cbdata)
    for oyoz__qpjn in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[oyoz__qpjn] = visit_vars_inner(aggregate_node
            .df_in_vars[oyoz__qpjn], callback, cbdata)
    for oyoz__qpjn in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[oyoz__qpjn] = visit_vars_inner(
            aggregate_node.df_out_vars[oyoz__qpjn], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for beryn__pjuoh in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[beryn__pjuoh] = visit_vars_inner(
                aggregate_node.out_key_vars[beryn__pjuoh], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    mqcha__chzq = []
    for kta__zfuo in aggregate_node.key_arrs:
        crlk__slziy = equiv_set.get_shape(kta__zfuo)
        if crlk__slziy:
            mqcha__chzq.append(crlk__slziy[0])
    if aggregate_node.pivot_arr is not None:
        crlk__slziy = equiv_set.get_shape(aggregate_node.pivot_arr)
        if crlk__slziy:
            mqcha__chzq.append(crlk__slziy[0])
    for oxg__tzbc in aggregate_node.df_in_vars.values():
        crlk__slziy = equiv_set.get_shape(oxg__tzbc)
        if crlk__slziy:
            mqcha__chzq.append(crlk__slziy[0])
    if len(mqcha__chzq) > 1:
        equiv_set.insert_equiv(*mqcha__chzq)
    dzqly__phto = []
    mqcha__chzq = []
    muhqs__fbhh = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        muhqs__fbhh.extend(aggregate_node.out_key_vars)
    for oxg__tzbc in muhqs__fbhh:
        sgq__yxvot = typemap[oxg__tzbc.name]
        bvku__omwr = array_analysis._gen_shape_call(equiv_set, oxg__tzbc,
            sgq__yxvot.ndim, None, dzqly__phto)
        equiv_set.insert_equiv(oxg__tzbc, bvku__omwr)
        mqcha__chzq.append(bvku__omwr[0])
        equiv_set.define(oxg__tzbc, set())
    if len(mqcha__chzq) > 1:
        equiv_set.insert_equiv(*mqcha__chzq)
    return [], dzqly__phto


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    kbtlk__wmo = Distribution.OneD
    for oxg__tzbc in aggregate_node.df_in_vars.values():
        kbtlk__wmo = Distribution(min(kbtlk__wmo.value, array_dists[
            oxg__tzbc.name].value))
    for kta__zfuo in aggregate_node.key_arrs:
        kbtlk__wmo = Distribution(min(kbtlk__wmo.value, array_dists[
            kta__zfuo.name].value))
    if aggregate_node.pivot_arr is not None:
        kbtlk__wmo = Distribution(min(kbtlk__wmo.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = kbtlk__wmo
    for oxg__tzbc in aggregate_node.df_in_vars.values():
        array_dists[oxg__tzbc.name] = kbtlk__wmo
    for kta__zfuo in aggregate_node.key_arrs:
        array_dists[kta__zfuo.name] = kbtlk__wmo
    xwni__qvz = Distribution.OneD_Var
    for oxg__tzbc in aggregate_node.df_out_vars.values():
        if oxg__tzbc.name in array_dists:
            xwni__qvz = Distribution(min(xwni__qvz.value, array_dists[
                oxg__tzbc.name].value))
    if aggregate_node.out_key_vars is not None:
        for oxg__tzbc in aggregate_node.out_key_vars:
            if oxg__tzbc.name in array_dists:
                xwni__qvz = Distribution(min(xwni__qvz.value, array_dists[
                    oxg__tzbc.name].value))
    xwni__qvz = Distribution(min(xwni__qvz.value, kbtlk__wmo.value))
    for oxg__tzbc in aggregate_node.df_out_vars.values():
        array_dists[oxg__tzbc.name] = xwni__qvz
    if aggregate_node.out_key_vars is not None:
        for ptz__zbimk in aggregate_node.out_key_vars:
            array_dists[ptz__zbimk.name] = xwni__qvz
    if xwni__qvz != Distribution.OneD_Var:
        for kta__zfuo in aggregate_node.key_arrs:
            array_dists[kta__zfuo.name] = xwni__qvz
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = xwni__qvz
        for oxg__tzbc in aggregate_node.df_in_vars.values():
            array_dists[oxg__tzbc.name] = xwni__qvz


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for oxg__tzbc in agg_node.df_out_vars.values():
        definitions[oxg__tzbc.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for ptz__zbimk in agg_node.out_key_vars:
            definitions[ptz__zbimk.name].append(agg_node)
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
        for sxa__xorac in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[sxa__xorac.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                sxa__xorac.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    pxctu__commp = tuple(typemap[sxa__xorac.name] for sxa__xorac in
        agg_node.key_arrs)
    hyve__odirp = [sxa__xorac for pdlz__mntg, sxa__xorac in agg_node.
        df_in_vars.items()]
    zpyr__swwx = [sxa__xorac for pdlz__mntg, sxa__xorac in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    svmum__srtta = []
    if agg_node.pivot_arr is not None:
        for jhtk__aeglx, oiblf__eelu in agg_node.gb_info_in.items():
            for func, jelue__oiba in oiblf__eelu:
                if jhtk__aeglx is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        jhtk__aeglx].name])
                svmum__srtta.append(func)
    else:
        for jhtk__aeglx, func in agg_node.gb_info_out.values():
            if jhtk__aeglx is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[jhtk__aeglx]
                    .name])
            svmum__srtta.append(func)
    out_col_typs = tuple(typemap[sxa__xorac.name] for sxa__xorac in zpyr__swwx)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(pxctu__commp + tuple(typemap[sxa__xorac.name] for
        sxa__xorac in hyve__odirp) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    fphh__ccd = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for beryn__pjuoh, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            fphh__ccd.update({f'in_cat_dtype_{beryn__pjuoh}': in_col_typ})
    for beryn__pjuoh, eullq__nzt in enumerate(out_col_typs):
        if isinstance(eullq__nzt, bodo.CategoricalArrayType):
            fphh__ccd.update({f'out_cat_dtype_{beryn__pjuoh}': eullq__nzt})
    udf_func_struct = get_udf_func_struct(svmum__srtta, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    dcefl__jks = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    fphh__ccd.update({'pd': pd, 'pre_alloc_string_array':
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
            fphh__ccd.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            fphh__ccd.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    wyomu__vdsm = compile_to_numba_ir(dcefl__jks, fphh__ccd, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    oww__qpsta = []
    if agg_node.pivot_arr is None:
        hpl__yahvg = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        csfzx__uhrkb = ir.Var(hpl__yahvg, mk_unique_var('dummy_none'), loc)
        typemap[csfzx__uhrkb.name] = types.none
        oww__qpsta.append(ir.Assign(ir.Const(None, loc), csfzx__uhrkb, loc))
        hyve__odirp.append(csfzx__uhrkb)
    else:
        hyve__odirp.append(agg_node.pivot_arr)
    replace_arg_nodes(wyomu__vdsm, agg_node.key_arrs + hyve__odirp)
    giz__ieck = wyomu__vdsm.body[-3]
    assert is_assign(giz__ieck) and isinstance(giz__ieck.value, ir.Expr
        ) and giz__ieck.value.op == 'build_tuple'
    oww__qpsta += wyomu__vdsm.body[:-3]
    muhqs__fbhh = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        muhqs__fbhh += agg_node.out_key_vars
    for beryn__pjuoh, clzg__mma in enumerate(muhqs__fbhh):
        jtswt__xbo = giz__ieck.value.items[beryn__pjuoh]
        oww__qpsta.append(ir.Assign(jtswt__xbo, clzg__mma, clzg__mma.loc))
    return oww__qpsta


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        lctr__rrjcg = args[0]
        dtype = types.Tuple([t.dtype for t in lctr__rrjcg.types]
            ) if isinstance(lctr__rrjcg, types.BaseTuple
            ) else lctr__rrjcg.dtype
        if isinstance(lctr__rrjcg, types.BaseTuple) and len(lctr__rrjcg.types
            ) == 1:
            dtype = lctr__rrjcg.types[0].dtype
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
        nxd__oos = args[0]
        if nxd__oos == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    sdn__ffssn = context.compile_internal(builder, lambda a: False, sig, args)
    return sdn__ffssn


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        qcro__rpco = IntDtype(t.dtype).name
        assert qcro__rpco.endswith('Dtype()')
        qcro__rpco = qcro__rpco[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{qcro__rpco}'))"
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
        ssjg__buwrh = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {ssjg__buwrh}_cat_dtype_{colnum})'
            )
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
    miuh__kfi = udf_func_struct.var_typs
    jvlh__yvxqb = len(miuh__kfi)
    qreo__bik = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    qreo__bik += '    if is_null_pointer(in_table):\n'
    qreo__bik += '        return\n'
    qreo__bik += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in miuh__kfi]), 
        ',' if len(miuh__kfi) == 1 else '')
    dglc__eys = n_keys
    nuqtj__dkn = []
    redvar_offsets = []
    fgm__rfq = []
    if do_combine:
        for beryn__pjuoh, szr__zui in enumerate(allfuncs):
            if szr__zui.ftype != 'udf':
                dglc__eys += szr__zui.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(dglc__eys, dglc__eys +
                    szr__zui.n_redvars))
                dglc__eys += szr__zui.n_redvars
                fgm__rfq.append(data_in_typs_[func_idx_to_in_col[beryn__pjuoh]]
                    )
                nuqtj__dkn.append(func_idx_to_in_col[beryn__pjuoh] + n_keys)
    else:
        for beryn__pjuoh, szr__zui in enumerate(allfuncs):
            if szr__zui.ftype != 'udf':
                dglc__eys += szr__zui.ncols_post_shuffle
            else:
                redvar_offsets += list(range(dglc__eys + 1, dglc__eys + 1 +
                    szr__zui.n_redvars))
                dglc__eys += szr__zui.n_redvars + 1
                fgm__rfq.append(data_in_typs_[func_idx_to_in_col[beryn__pjuoh]]
                    )
                nuqtj__dkn.append(func_idx_to_in_col[beryn__pjuoh] + n_keys)
    assert len(redvar_offsets) == jvlh__yvxqb
    tvxz__lrpzy = len(fgm__rfq)
    qsoc__guu = []
    for beryn__pjuoh, t in enumerate(fgm__rfq):
        qsoc__guu.append(_gen_dummy_alloc(t, beryn__pjuoh, True))
    qreo__bik += '    data_in_dummy = ({}{})\n'.format(','.join(qsoc__guu),
        ',' if len(fgm__rfq) == 1 else '')
    qreo__bik += """
    # initialize redvar cols
"""
    qreo__bik += '    init_vals = __init_func()\n'
    for beryn__pjuoh in range(jvlh__yvxqb):
        qreo__bik += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(beryn__pjuoh, redvar_offsets[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(redvar_arr_{})\n'.format(beryn__pjuoh)
        qreo__bik += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            beryn__pjuoh, beryn__pjuoh)
    qreo__bik += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(beryn__pjuoh) for beryn__pjuoh in range(jvlh__yvxqb)]), ',' if
        jvlh__yvxqb == 1 else '')
    qreo__bik += '\n'
    for beryn__pjuoh in range(tvxz__lrpzy):
        qreo__bik += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(beryn__pjuoh, nuqtj__dkn[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(data_in_{})\n'.format(beryn__pjuoh)
    qreo__bik += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(beryn__pjuoh) for beryn__pjuoh in range(tvxz__lrpzy)]), ',' if
        tvxz__lrpzy == 1 else '')
    qreo__bik += '\n'
    qreo__bik += '    for i in range(len(data_in_0)):\n'
    qreo__bik += '        w_ind = row_to_group[i]\n'
    qreo__bik += '        if w_ind != -1:\n'
    qreo__bik += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    huiub__kxju = {}
    exec(qreo__bik, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, huiub__kxju)
    return huiub__kxju['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    miuh__kfi = udf_func_struct.var_typs
    jvlh__yvxqb = len(miuh__kfi)
    qreo__bik = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    qreo__bik += '    if is_null_pointer(in_table):\n'
    qreo__bik += '        return\n'
    qreo__bik += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in miuh__kfi]), 
        ',' if len(miuh__kfi) == 1 else '')
    ycq__wwl = n_keys
    xzn__nqg = n_keys
    rzi__vsfca = []
    mxk__awd = []
    for szr__zui in allfuncs:
        if szr__zui.ftype != 'udf':
            ycq__wwl += szr__zui.ncols_pre_shuffle
            xzn__nqg += szr__zui.ncols_post_shuffle
        else:
            rzi__vsfca += list(range(ycq__wwl, ycq__wwl + szr__zui.n_redvars))
            mxk__awd += list(range(xzn__nqg + 1, xzn__nqg + 1 + szr__zui.
                n_redvars))
            ycq__wwl += szr__zui.n_redvars
            xzn__nqg += 1 + szr__zui.n_redvars
    assert len(rzi__vsfca) == jvlh__yvxqb
    qreo__bik += """
    # initialize redvar cols
"""
    qreo__bik += '    init_vals = __init_func()\n'
    for beryn__pjuoh in range(jvlh__yvxqb):
        qreo__bik += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(beryn__pjuoh, mxk__awd[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(redvar_arr_{})\n'.format(beryn__pjuoh)
        qreo__bik += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            beryn__pjuoh, beryn__pjuoh)
    qreo__bik += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(beryn__pjuoh) for beryn__pjuoh in range(jvlh__yvxqb)]), ',' if
        jvlh__yvxqb == 1 else '')
    qreo__bik += '\n'
    for beryn__pjuoh in range(jvlh__yvxqb):
        qreo__bik += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(beryn__pjuoh, rzi__vsfca[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(recv_redvar_arr_{})\n'.format(beryn__pjuoh)
    qreo__bik += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(beryn__pjuoh) for beryn__pjuoh in range
        (jvlh__yvxqb)]), ',' if jvlh__yvxqb == 1 else '')
    qreo__bik += '\n'
    if jvlh__yvxqb:
        qreo__bik += '    for i in range(len(recv_redvar_arr_0)):\n'
        qreo__bik += '        w_ind = row_to_group[i]\n'
        qreo__bik += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)\n'
            )
    huiub__kxju = {}
    exec(qreo__bik, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, huiub__kxju)
    return huiub__kxju['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    miuh__kfi = udf_func_struct.var_typs
    jvlh__yvxqb = len(miuh__kfi)
    dglc__eys = n_keys
    redvar_offsets = []
    dfnpf__kmrqa = []
    out_data_typs = []
    for beryn__pjuoh, szr__zui in enumerate(allfuncs):
        if szr__zui.ftype != 'udf':
            dglc__eys += szr__zui.ncols_post_shuffle
        else:
            dfnpf__kmrqa.append(dglc__eys)
            redvar_offsets += list(range(dglc__eys + 1, dglc__eys + 1 +
                szr__zui.n_redvars))
            dglc__eys += 1 + szr__zui.n_redvars
            out_data_typs.append(out_data_typs_[beryn__pjuoh])
    assert len(redvar_offsets) == jvlh__yvxqb
    tvxz__lrpzy = len(out_data_typs)
    qreo__bik = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    qreo__bik += '    if is_null_pointer(table):\n'
    qreo__bik += '        return\n'
    qreo__bik += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in miuh__kfi]), 
        ',' if len(miuh__kfi) == 1 else '')
    qreo__bik += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for beryn__pjuoh in range(jvlh__yvxqb):
        qreo__bik += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(beryn__pjuoh, redvar_offsets[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(redvar_arr_{})\n'.format(beryn__pjuoh)
    qreo__bik += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(beryn__pjuoh) for beryn__pjuoh in range(jvlh__yvxqb)]), ',' if
        jvlh__yvxqb == 1 else '')
    qreo__bik += '\n'
    for beryn__pjuoh in range(tvxz__lrpzy):
        qreo__bik += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(beryn__pjuoh, dfnpf__kmrqa[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(data_out_{})\n'.format(beryn__pjuoh)
    qreo__bik += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(beryn__pjuoh) for beryn__pjuoh in range(tvxz__lrpzy)]), ',' if
        tvxz__lrpzy == 1 else '')
    qreo__bik += '\n'
    qreo__bik += '    for i in range(len(data_out_0)):\n'
    qreo__bik += '        __eval_res(redvars, data_out, i)\n'
    huiub__kxju = {}
    exec(qreo__bik, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, huiub__kxju)
    return huiub__kxju['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    dglc__eys = n_keys
    ria__edu = []
    for beryn__pjuoh, szr__zui in enumerate(allfuncs):
        if szr__zui.ftype == 'gen_udf':
            ria__edu.append(dglc__eys)
            dglc__eys += 1
        elif szr__zui.ftype != 'udf':
            dglc__eys += szr__zui.ncols_post_shuffle
        else:
            dglc__eys += szr__zui.n_redvars + 1
    qreo__bik = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    qreo__bik += '    if num_groups == 0:\n'
    qreo__bik += '        return\n'
    for beryn__pjuoh, func in enumerate(udf_func_struct.general_udf_funcs):
        qreo__bik += '    # col {}\n'.format(beryn__pjuoh)
        qreo__bik += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(ria__edu[beryn__pjuoh], beryn__pjuoh))
        qreo__bik += '    incref(out_col)\n'
        qreo__bik += '    for j in range(num_groups):\n'
        qreo__bik += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(beryn__pjuoh, beryn__pjuoh))
        qreo__bik += '        incref(in_col)\n'
        qreo__bik += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(beryn__pjuoh))
    fphh__ccd = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    mlnb__dcawy = 0
    for beryn__pjuoh, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[mlnb__dcawy]
        fphh__ccd['func_{}'.format(mlnb__dcawy)] = func
        fphh__ccd['in_col_{}_typ'.format(mlnb__dcawy)] = in_col_typs[
            func_idx_to_in_col[beryn__pjuoh]]
        fphh__ccd['out_col_{}_typ'.format(mlnb__dcawy)] = out_col_typs[
            beryn__pjuoh]
        mlnb__dcawy += 1
    huiub__kxju = {}
    exec(qreo__bik, fphh__ccd, huiub__kxju)
    szr__zui = huiub__kxju['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    rnria__chswh = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(rnria__chswh, nopython=True)(szr__zui)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    utjb__miom = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        fsgo__dyh = 1
    else:
        fsgo__dyh = len(agg_node.pivot_values)
    pjxo__ymu = tuple('key_' + sanitize_varname(wwbs__pcjum) for
        wwbs__pcjum in agg_node.key_names)
    zajyn__wyuc = {wwbs__pcjum: 'in_{}'.format(sanitize_varname(wwbs__pcjum
        )) for wwbs__pcjum in agg_node.gb_info_in.keys() if wwbs__pcjum is not
        None}
    ktb__fpc = {wwbs__pcjum: ('out_' + sanitize_varname(wwbs__pcjum)) for
        wwbs__pcjum in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    cyd__rten = ', '.join(pjxo__ymu)
    ujrwi__dnqht = ', '.join(zajyn__wyuc.values())
    if ujrwi__dnqht != '':
        ujrwi__dnqht = ', ' + ujrwi__dnqht
    qreo__bik = 'def agg_top({}{}{}, pivot_arr):\n'.format(cyd__rten,
        ujrwi__dnqht, ', index_arg' if agg_node.input_has_index else '')
    for a in (pjxo__ymu + tuple(zajyn__wyuc.values())):
        qreo__bik += f'    {a} = decode_if_dict_array({a})\n'
    if utjb__miom:
        qreo__bik += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        vavf__kzstf = []
        for jhtk__aeglx, oiblf__eelu in agg_node.gb_info_in.items():
            if jhtk__aeglx is not None:
                for func, jelue__oiba in oiblf__eelu:
                    vavf__kzstf.append(zajyn__wyuc[jhtk__aeglx])
    else:
        vavf__kzstf = tuple(zajyn__wyuc[jhtk__aeglx] for jhtk__aeglx,
            jelue__oiba in agg_node.gb_info_out.values() if jhtk__aeglx is not
            None)
    zoolh__ymepf = pjxo__ymu + tuple(vavf__kzstf)
    qreo__bik += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in zoolh__ymepf), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    qreo__bik += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    qoeht__ctrew = []
    func_idx_to_in_col = []
    xqlyl__tbv = []
    mhv__hrw = False
    ltf__rss = 1
    kfwp__xuyf = -1
    bqis__eor = 0
    rlzq__kni = 0
    if not utjb__miom:
        svmum__srtta = [func for jelue__oiba, func in agg_node.gb_info_out.
            values()]
    else:
        svmum__srtta = [func for func, jelue__oiba in oiblf__eelu for
            oiblf__eelu in agg_node.gb_info_in.values()]
    for pnkpv__eooy, func in enumerate(svmum__srtta):
        qoeht__ctrew.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            bqis__eor += 1
        if hasattr(func, 'skipdropna'):
            mhv__hrw = func.skipdropna
        if func.ftype == 'shift':
            ltf__rss = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            rlzq__kni = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            kfwp__xuyf = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(pnkpv__eooy)
        if func.ftype == 'udf':
            xqlyl__tbv.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            xqlyl__tbv.append(0)
            do_combine = False
    qoeht__ctrew.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == fsgo__dyh, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * fsgo__dyh, 'invalid number of groupby outputs'
    if bqis__eor > 0:
        if bqis__eor != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for beryn__pjuoh, wwbs__pcjum in enumerate(agg_node.gb_info_out.keys()):
        key__dji = ktb__fpc[wwbs__pcjum] + '_dummy'
        eullq__nzt = out_col_typs[beryn__pjuoh]
        jhtk__aeglx, func = agg_node.gb_info_out[wwbs__pcjum]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(eullq__nzt, bodo.
            CategoricalArrayType):
            qreo__bik += '    {} = {}\n'.format(key__dji, zajyn__wyuc[
                jhtk__aeglx])
        elif udf_func_struct is not None:
            qreo__bik += '    {} = {}\n'.format(key__dji, _gen_dummy_alloc(
                eullq__nzt, beryn__pjuoh, False))
    if udf_func_struct is not None:
        grmlo__kpnq = next_label()
        if udf_func_struct.regular_udfs:
            rnria__chswh = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            pjcq__ldui = numba.cfunc(rnria__chswh, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, grmlo__kpnq))
            amf__jzwx = numba.cfunc(rnria__chswh, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, grmlo__kpnq))
            tqlk__hynh = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                grmlo__kpnq))
            udf_func_struct.set_regular_cfuncs(pjcq__ldui, amf__jzwx,
                tqlk__hynh)
            for qjcl__unyh in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[qjcl__unyh.native_name] = qjcl__unyh
                gb_agg_cfunc_addr[qjcl__unyh.native_name] = qjcl__unyh.address
        if udf_func_struct.general_udfs:
            tnjs__ios = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                grmlo__kpnq)
            udf_func_struct.set_general_cfunc(tnjs__ios)
        gumqf__yso = []
        wked__wzds = 0
        beryn__pjuoh = 0
        for key__dji, szr__zui in zip(ktb__fpc.values(), allfuncs):
            if szr__zui.ftype in ('udf', 'gen_udf'):
                gumqf__yso.append(key__dji + '_dummy')
                for ggb__xfkez in range(wked__wzds, wked__wzds + xqlyl__tbv
                    [beryn__pjuoh]):
                    gumqf__yso.append('data_redvar_dummy_' + str(ggb__xfkez))
                wked__wzds += xqlyl__tbv[beryn__pjuoh]
                beryn__pjuoh += 1
        if udf_func_struct.regular_udfs:
            miuh__kfi = udf_func_struct.var_typs
            for beryn__pjuoh, t in enumerate(miuh__kfi):
                qreo__bik += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(beryn__pjuoh, _get_np_dtype(t)))
        qreo__bik += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in gumqf__yso))
        qreo__bik += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            qreo__bik += "    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".format(
                pjcq__ldui.native_name)
            qreo__bik += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(amf__jzwx.native_name))
            qreo__bik += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                tqlk__hynh.native_name)
            qreo__bik += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(pjcq__ldui.native_name))
            qreo__bik += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(amf__jzwx.native_name))
            qreo__bik += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(tqlk__hynh.native_name))
        else:
            qreo__bik += '    cpp_cb_update_addr = 0\n'
            qreo__bik += '    cpp_cb_combine_addr = 0\n'
            qreo__bik += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            qjcl__unyh = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[qjcl__unyh.native_name] = qjcl__unyh
            gb_agg_cfunc_addr[qjcl__unyh.native_name] = qjcl__unyh.address
            qreo__bik += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(qjcl__unyh.native_name))
            qreo__bik += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(qjcl__unyh.native_name))
        else:
            qreo__bik += '    cpp_cb_general_addr = 0\n'
    else:
        qreo__bik += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        qreo__bik += '    cpp_cb_update_addr = 0\n'
        qreo__bik += '    cpp_cb_combine_addr = 0\n'
        qreo__bik += '    cpp_cb_eval_addr = 0\n'
        qreo__bik += '    cpp_cb_general_addr = 0\n'
    qreo__bik += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(szr__zui.ftype)) for szr__zui in
        allfuncs] + ['0']))
    qreo__bik += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(str
        (qoeht__ctrew))
    if len(xqlyl__tbv) > 0:
        qreo__bik += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(xqlyl__tbv))
    else:
        qreo__bik += '    udf_ncols = np.array([0], np.int32)\n'
    if utjb__miom:
        qreo__bik += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        qreo__bik += '    arr_info = array_to_info(arr_type)\n'
        qreo__bik += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        qreo__bik += '    pivot_info = array_to_info(pivot_arr)\n'
        qreo__bik += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        qreo__bik += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, mhv__hrw, agg_node.return_key, agg_node.same_index))
        qreo__bik += '    delete_info_decref_array(pivot_info)\n'
        qreo__bik += '    delete_info_decref_array(arr_info)\n'
    else:
        qreo__bik += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, mhv__hrw,
            ltf__rss, rlzq__kni, kfwp__xuyf, agg_node.return_key, agg_node.
            same_index, agg_node.dropna))
    shwz__wbleq = 0
    if agg_node.return_key:
        for beryn__pjuoh, bcmi__wew in enumerate(pjxo__ymu):
            qreo__bik += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(bcmi__wew, shwz__wbleq, bcmi__wew))
            shwz__wbleq += 1
    for beryn__pjuoh, key__dji in enumerate(ktb__fpc.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(eullq__nzt, bodo.
            CategoricalArrayType):
            qreo__bik += f"""    {key__dji} = info_to_array(info_from_table(out_table, {shwz__wbleq}), {key__dji + '_dummy'})
"""
        else:
            qreo__bik += f"""    {key__dji} = info_to_array(info_from_table(out_table, {shwz__wbleq}), out_typs[{beryn__pjuoh}])
"""
        shwz__wbleq += 1
    if agg_node.same_index:
        qreo__bik += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(shwz__wbleq))
        shwz__wbleq += 1
    qreo__bik += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    qreo__bik += '    delete_table_decref_arrays(table)\n'
    qreo__bik += '    delete_table_decref_arrays(udf_table_dummy)\n'
    qreo__bik += '    delete_table(out_table)\n'
    qreo__bik += f'    ev_clean.finalize()\n'
    egnob__okax = tuple(ktb__fpc.values())
    if agg_node.return_key:
        egnob__okax += tuple(pjxo__ymu)
    qreo__bik += '    return ({},{})\n'.format(', '.join(egnob__okax), 
        ' out_index_arg,' if agg_node.same_index else '')
    huiub__kxju = {}
    exec(qreo__bik, {'out_typs': out_col_typs}, huiub__kxju)
    dxuql__hqe = huiub__kxju['agg_top']
    return dxuql__hqe


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for yhdqn__jwp in block.body:
            if is_call_assign(yhdqn__jwp) and find_callname(f_ir,
                yhdqn__jwp.value) == ('len', 'builtins'
                ) and yhdqn__jwp.value.args[0].name == f_ir.arg_names[0]:
                rclk__bgu = get_definition(f_ir, yhdqn__jwp.value.func)
                rclk__bgu.name = 'dummy_agg_count'
                rclk__bgu.value = dummy_agg_count
    jhgb__oyth = get_name_var_table(f_ir.blocks)
    whgqe__vdg = {}
    for name, jelue__oiba in jhgb__oyth.items():
        whgqe__vdg[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, whgqe__vdg)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    hulo__mfxw = numba.core.compiler.Flags()
    hulo__mfxw.nrt = True
    enbrb__rypty = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, hulo__mfxw)
    enbrb__rypty.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, nbstg__scpps, calltypes, jelue__oiba = (numba.core.
        typed_passes.type_inference_stage(typingctx, targetctx, f_ir,
        arg_typs, None))
    ssq__gbb = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    hsca__mdiiu = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    bjf__rupm = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    ntam__sylh = bjf__rupm(typemap, calltypes)
    pm = hsca__mdiiu(typingctx, targetctx, None, f_ir, typemap,
        nbstg__scpps, calltypes, ntam__sylh, {}, hulo__mfxw, None)
    wgvi__qrzh = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = hsca__mdiiu(typingctx, targetctx, None, f_ir, typemap,
        nbstg__scpps, calltypes, ntam__sylh, {}, hulo__mfxw, wgvi__qrzh)
    suwhp__vga = numba.core.typed_passes.InlineOverloads()
    suwhp__vga.run_pass(pm)
    dxung__qly = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    dxung__qly.run()
    for block in f_ir.blocks.values():
        for yhdqn__jwp in block.body:
            if is_assign(yhdqn__jwp) and isinstance(yhdqn__jwp.value, (ir.
                Arg, ir.Var)) and isinstance(typemap[yhdqn__jwp.target.name
                ], SeriesType):
                sgq__yxvot = typemap.pop(yhdqn__jwp.target.name)
                typemap[yhdqn__jwp.target.name] = sgq__yxvot.data
            if is_call_assign(yhdqn__jwp) and find_callname(f_ir,
                yhdqn__jwp.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[yhdqn__jwp.target.name].remove(yhdqn__jwp
                    .value)
                yhdqn__jwp.value = yhdqn__jwp.value.args[0]
                f_ir._definitions[yhdqn__jwp.target.name].append(yhdqn__jwp
                    .value)
            if is_call_assign(yhdqn__jwp) and find_callname(f_ir,
                yhdqn__jwp.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[yhdqn__jwp.target.name].remove(yhdqn__jwp
                    .value)
                yhdqn__jwp.value = ir.Const(False, yhdqn__jwp.loc)
                f_ir._definitions[yhdqn__jwp.target.name].append(yhdqn__jwp
                    .value)
            if is_call_assign(yhdqn__jwp) and find_callname(f_ir,
                yhdqn__jwp.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[yhdqn__jwp.target.name].remove(yhdqn__jwp
                    .value)
                yhdqn__jwp.value = ir.Const(False, yhdqn__jwp.loc)
                f_ir._definitions[yhdqn__jwp.target.name].append(yhdqn__jwp
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    djt__oaq = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, ssq__gbb)
    djt__oaq.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    cey__ubocl = numba.core.compiler.StateDict()
    cey__ubocl.func_ir = f_ir
    cey__ubocl.typemap = typemap
    cey__ubocl.calltypes = calltypes
    cey__ubocl.typingctx = typingctx
    cey__ubocl.targetctx = targetctx
    cey__ubocl.return_type = nbstg__scpps
    numba.core.rewrites.rewrite_registry.apply('after-inference', cey__ubocl)
    yxjig__dkg = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        nbstg__scpps, typingctx, targetctx, ssq__gbb, hulo__mfxw, {})
    yxjig__dkg.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            tlqks__zyk = ctypes.pythonapi.PyCell_Get
            tlqks__zyk.restype = ctypes.py_object
            tlqks__zyk.argtypes = ctypes.py_object,
            bqn__zxd = tuple(tlqks__zyk(nqwhs__lgs) for nqwhs__lgs in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            bqn__zxd = closure.items
        assert len(code.co_freevars) == len(bqn__zxd)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, bqn__zxd)


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
        vbhx__opo = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (vbhx__opo,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        bemaw__zrv, arr_var = _rm_arg_agg_block(block, pm.typemap)
        pzof__qyym = -1
        for beryn__pjuoh, yhdqn__jwp in enumerate(bemaw__zrv):
            if isinstance(yhdqn__jwp, numba.parfors.parfor.Parfor):
                assert pzof__qyym == -1, 'only one parfor for aggregation function'
                pzof__qyym = beryn__pjuoh
        parfor = None
        if pzof__qyym != -1:
            parfor = bemaw__zrv[pzof__qyym]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = bemaw__zrv[:pzof__qyym] + parfor.init_block.body
        eval_nodes = bemaw__zrv[pzof__qyym + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for yhdqn__jwp in init_nodes:
            if is_assign(yhdqn__jwp) and yhdqn__jwp.target.name in redvars:
                ind = redvars.index(yhdqn__jwp.target.name)
                reduce_vars[ind] = yhdqn__jwp.target
        var_types = [pm.typemap[sxa__xorac] for sxa__xorac in redvars]
        xaxji__rzxe = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        swrx__nis = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        vavg__bzmq = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(vavg__bzmq)
        self.all_update_funcs.append(swrx__nis)
        self.all_combine_funcs.append(xaxji__rzxe)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        yxxby__bvny = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        qsds__qxaio = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        zesa__qhsqd = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        cvgf__joyuy = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, yxxby__bvny, qsds__qxaio, zesa__qhsqd,
            cvgf__joyuy)


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
    zznaq__psrwb = []
    for t, szr__zui in zip(in_col_types, agg_func):
        zznaq__psrwb.append((t, szr__zui))
    aadz__gvn = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    tdwie__xijp = GeneralUDFGenerator()
    for in_col_typ, func in zznaq__psrwb:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            aadz__gvn.add_udf(in_col_typ, func)
        except:
            tdwie__xijp.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = aadz__gvn.gen_all_func()
    general_udf_funcs = tdwie__xijp.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    kwv__sswr = compute_use_defs(parfor.loop_body)
    lcigi__vatr = set()
    for vbry__dtf in kwv__sswr.usemap.values():
        lcigi__vatr |= vbry__dtf
    oxfa__lir = set()
    for vbry__dtf in kwv__sswr.defmap.values():
        oxfa__lir |= vbry__dtf
    vqw__jxp = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    vqw__jxp.body = eval_nodes
    vyriy__jeg = compute_use_defs({(0): vqw__jxp})
    hmj__xgtwg = vyriy__jeg.usemap[0]
    quqt__fckl = set()
    ngxfw__lxn = []
    tcead__pmhcz = []
    for yhdqn__jwp in reversed(init_nodes):
        zjcax__clois = {sxa__xorac.name for sxa__xorac in yhdqn__jwp.
            list_vars()}
        if is_assign(yhdqn__jwp):
            sxa__xorac = yhdqn__jwp.target.name
            zjcax__clois.remove(sxa__xorac)
            if (sxa__xorac in lcigi__vatr and sxa__xorac not in quqt__fckl and
                sxa__xorac not in hmj__xgtwg and sxa__xorac not in oxfa__lir):
                tcead__pmhcz.append(yhdqn__jwp)
                lcigi__vatr |= zjcax__clois
                oxfa__lir.add(sxa__xorac)
                continue
        quqt__fckl |= zjcax__clois
        ngxfw__lxn.append(yhdqn__jwp)
    tcead__pmhcz.reverse()
    ngxfw__lxn.reverse()
    ghm__phr = min(parfor.loop_body.keys())
    zfy__eqic = parfor.loop_body[ghm__phr]
    zfy__eqic.body = tcead__pmhcz + zfy__eqic.body
    return ngxfw__lxn


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    hfgle__wmthm = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    rkzbj__yuzvi = set()
    aisn__yqfi = []
    for yhdqn__jwp in init_nodes:
        if is_assign(yhdqn__jwp) and isinstance(yhdqn__jwp.value, ir.Global
            ) and isinstance(yhdqn__jwp.value.value, pytypes.FunctionType
            ) and yhdqn__jwp.value.value in hfgle__wmthm:
            rkzbj__yuzvi.add(yhdqn__jwp.target.name)
        elif is_call_assign(yhdqn__jwp
            ) and yhdqn__jwp.value.func.name in rkzbj__yuzvi:
            pass
        else:
            aisn__yqfi.append(yhdqn__jwp)
    init_nodes = aisn__yqfi
    pyucv__uko = types.Tuple(var_types)
    acgmz__hie = lambda : None
    f_ir = compile_to_numba_ir(acgmz__hie, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    okweh__jvec = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    jmlad__qftq = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        okweh__jvec, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [jmlad__qftq] + block.body
    block.body[-2].value.value = okweh__jvec
    xqdzg__xjloy = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        pyucv__uko, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jbsl__awfr = numba.core.target_extension.dispatcher_registry[cpu_target](
        acgmz__hie)
    jbsl__awfr.add_overload(xqdzg__xjloy)
    return jbsl__awfr


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    dgamh__yzmoi = len(update_funcs)
    qkgf__prphg = len(in_col_types)
    if pivot_values is not None:
        assert qkgf__prphg == 1
    qreo__bik = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        myqr__cdak = redvar_offsets[qkgf__prphg]
        qreo__bik += '  pv = pivot_arr[i]\n'
        for ggb__xfkez, spvz__led in enumerate(pivot_values):
            tugp__tkn = 'el' if ggb__xfkez != 0 else ''
            qreo__bik += "  {}if pv == '{}':\n".format(tugp__tkn, spvz__led)
            eul__kapqg = myqr__cdak * ggb__xfkez
            dck__ciol = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                beryn__pjuoh) for beryn__pjuoh in range(eul__kapqg +
                redvar_offsets[0], eul__kapqg + redvar_offsets[1])])
            xtk__qyzi = 'data_in[0][i]'
            if is_crosstab:
                xtk__qyzi = '0'
            qreo__bik += '    {} = update_vars_0({}, {})\n'.format(dck__ciol,
                dck__ciol, xtk__qyzi)
    else:
        for ggb__xfkez in range(dgamh__yzmoi):
            dck__ciol = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                beryn__pjuoh) for beryn__pjuoh in range(redvar_offsets[
                ggb__xfkez], redvar_offsets[ggb__xfkez + 1])])
            if dck__ciol:
                qreo__bik += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(dck__ciol, ggb__xfkez, dck__ciol, 0 if 
                    qkgf__prphg == 1 else ggb__xfkez))
    qreo__bik += '  return\n'
    fphh__ccd = {}
    for beryn__pjuoh, szr__zui in enumerate(update_funcs):
        fphh__ccd['update_vars_{}'.format(beryn__pjuoh)] = szr__zui
    huiub__kxju = {}
    exec(qreo__bik, fphh__ccd, huiub__kxju)
    jxjd__rjxm = huiub__kxju['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(jxjd__rjxm)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    qurdd__snd = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = qurdd__snd, qurdd__snd, types.intp, types.intp, pivot_typ
    igep__mzdus = len(redvar_offsets) - 1
    myqr__cdak = redvar_offsets[igep__mzdus]
    qreo__bik = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert igep__mzdus == 1
        for qpv__jlmu in range(len(pivot_values)):
            eul__kapqg = myqr__cdak * qpv__jlmu
            dck__ciol = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                beryn__pjuoh) for beryn__pjuoh in range(eul__kapqg +
                redvar_offsets[0], eul__kapqg + redvar_offsets[1])])
            kelka__yqseq = ', '.join(['recv_arrs[{}][i]'.format(
                beryn__pjuoh) for beryn__pjuoh in range(eul__kapqg +
                redvar_offsets[0], eul__kapqg + redvar_offsets[1])])
            qreo__bik += '  {} = combine_vars_0({}, {})\n'.format(dck__ciol,
                dck__ciol, kelka__yqseq)
    else:
        for ggb__xfkez in range(igep__mzdus):
            dck__ciol = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                beryn__pjuoh) for beryn__pjuoh in range(redvar_offsets[
                ggb__xfkez], redvar_offsets[ggb__xfkez + 1])])
            kelka__yqseq = ', '.join(['recv_arrs[{}][i]'.format(
                beryn__pjuoh) for beryn__pjuoh in range(redvar_offsets[
                ggb__xfkez], redvar_offsets[ggb__xfkez + 1])])
            if kelka__yqseq:
                qreo__bik += '  {} = combine_vars_{}({}, {})\n'.format(
                    dck__ciol, ggb__xfkez, dck__ciol, kelka__yqseq)
    qreo__bik += '  return\n'
    fphh__ccd = {}
    for beryn__pjuoh, szr__zui in enumerate(combine_funcs):
        fphh__ccd['combine_vars_{}'.format(beryn__pjuoh)] = szr__zui
    huiub__kxju = {}
    exec(qreo__bik, fphh__ccd, huiub__kxju)
    fnlym__sjdqs = huiub__kxju['combine_all_f']
    f_ir = compile_to_numba_ir(fnlym__sjdqs, fphh__ccd)
    zesa__qhsqd = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jbsl__awfr = numba.core.target_extension.dispatcher_registry[cpu_target](
        fnlym__sjdqs)
    jbsl__awfr.add_overload(zesa__qhsqd)
    return jbsl__awfr


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    qurdd__snd = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    out_col_typs = types.Tuple(out_col_typs)
    igep__mzdus = len(redvar_offsets) - 1
    myqr__cdak = redvar_offsets[igep__mzdus]
    qreo__bik = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert igep__mzdus == 1
        for ggb__xfkez in range(len(pivot_values)):
            eul__kapqg = myqr__cdak * ggb__xfkez
            dck__ciol = ', '.join(['redvar_arrs[{}][j]'.format(beryn__pjuoh
                ) for beryn__pjuoh in range(eul__kapqg + redvar_offsets[0],
                eul__kapqg + redvar_offsets[1])])
            qreo__bik += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                ggb__xfkez, dck__ciol)
    else:
        for ggb__xfkez in range(igep__mzdus):
            dck__ciol = ', '.join(['redvar_arrs[{}][j]'.format(beryn__pjuoh
                ) for beryn__pjuoh in range(redvar_offsets[ggb__xfkez],
                redvar_offsets[ggb__xfkez + 1])])
            qreo__bik += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                ggb__xfkez, ggb__xfkez, dck__ciol)
    qreo__bik += '  return\n'
    fphh__ccd = {}
    for beryn__pjuoh, szr__zui in enumerate(eval_funcs):
        fphh__ccd['eval_vars_{}'.format(beryn__pjuoh)] = szr__zui
    huiub__kxju = {}
    exec(qreo__bik, fphh__ccd, huiub__kxju)
    lttoc__fauo = huiub__kxju['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(lttoc__fauo)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    zcb__scl = len(var_types)
    zvl__dhvr = [f'in{beryn__pjuoh}' for beryn__pjuoh in range(zcb__scl)]
    pyucv__uko = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    geh__kofg = pyucv__uko(0)
    qreo__bik = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        zvl__dhvr))
    huiub__kxju = {}
    exec(qreo__bik, {'_zero': geh__kofg}, huiub__kxju)
    fhze__noi = huiub__kxju['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(fhze__noi, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': geh__kofg}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    vdsg__aumfp = []
    for beryn__pjuoh, sxa__xorac in enumerate(reduce_vars):
        vdsg__aumfp.append(ir.Assign(block.body[beryn__pjuoh].target,
            sxa__xorac, sxa__xorac.loc))
        for sniwn__zlkce in sxa__xorac.versioned_names:
            vdsg__aumfp.append(ir.Assign(sxa__xorac, ir.Var(sxa__xorac.
                scope, sniwn__zlkce, sxa__xorac.loc), sxa__xorac.loc))
    block.body = block.body[:zcb__scl] + vdsg__aumfp + eval_nodes
    vavg__bzmq = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        pyucv__uko, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jbsl__awfr = numba.core.target_extension.dispatcher_registry[cpu_target](
        fhze__noi)
    jbsl__awfr.add_overload(vavg__bzmq)
    return jbsl__awfr


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    zcb__scl = len(redvars)
    lrorb__mzqsm = [f'v{beryn__pjuoh}' for beryn__pjuoh in range(zcb__scl)]
    zvl__dhvr = [f'in{beryn__pjuoh}' for beryn__pjuoh in range(zcb__scl)]
    qreo__bik = 'def agg_combine({}):\n'.format(', '.join(lrorb__mzqsm +
        zvl__dhvr))
    vizp__nznsw = wrap_parfor_blocks(parfor)
    kqetm__slsvz = find_topo_order(vizp__nznsw)
    kqetm__slsvz = kqetm__slsvz[1:]
    unwrap_parfor_blocks(parfor)
    lnjj__rsvgo = {}
    xhit__amv = []
    for xuc__cfa in kqetm__slsvz:
        knbti__qdi = parfor.loop_body[xuc__cfa]
        for yhdqn__jwp in knbti__qdi.body:
            if is_call_assign(yhdqn__jwp) and guard(find_callname, f_ir,
                yhdqn__jwp.value) == ('__special_combine', 'bodo.ir.aggregate'
                ):
                args = yhdqn__jwp.value.args
                imy__ubsy = []
                cerru__zgb = []
                for sxa__xorac in args[:-1]:
                    ind = redvars.index(sxa__xorac.name)
                    xhit__amv.append(ind)
                    imy__ubsy.append('v{}'.format(ind))
                    cerru__zgb.append('in{}'.format(ind))
                vqg__efgs = '__special_combine__{}'.format(len(lnjj__rsvgo))
                qreo__bik += '    ({},) = {}({})\n'.format(', '.join(
                    imy__ubsy), vqg__efgs, ', '.join(imy__ubsy + cerru__zgb))
                qkra__mmlnd = ir.Expr.call(args[-1], [], (), knbti__qdi.loc)
                tjpi__pkpbd = guard(find_callname, f_ir, qkra__mmlnd)
                assert tjpi__pkpbd == ('_var_combine', 'bodo.ir.aggregate')
                tjpi__pkpbd = bodo.ir.aggregate._var_combine
                lnjj__rsvgo[vqg__efgs] = tjpi__pkpbd
            if is_assign(yhdqn__jwp) and yhdqn__jwp.target.name in redvars:
                dbko__krtdi = yhdqn__jwp.target.name
                ind = redvars.index(dbko__krtdi)
                if ind in xhit__amv:
                    continue
                if len(f_ir._definitions[dbko__krtdi]) == 2:
                    var_def = f_ir._definitions[dbko__krtdi][0]
                    qreo__bik += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[dbko__krtdi][1]
                    qreo__bik += _match_reduce_def(var_def, f_ir, ind)
    qreo__bik += '    return {}'.format(', '.join(['v{}'.format(
        beryn__pjuoh) for beryn__pjuoh in range(zcb__scl)]))
    huiub__kxju = {}
    exec(qreo__bik, {}, huiub__kxju)
    semz__biem = huiub__kxju['agg_combine']
    arg_typs = tuple(2 * var_types)
    fphh__ccd = {'numba': numba, 'bodo': bodo, 'np': np}
    fphh__ccd.update(lnjj__rsvgo)
    f_ir = compile_to_numba_ir(semz__biem, fphh__ccd, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    pyucv__uko = pm.typemap[block.body[-1].value.name]
    xaxji__rzxe = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        pyucv__uko, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jbsl__awfr = numba.core.target_extension.dispatcher_registry[cpu_target](
        semz__biem)
    jbsl__awfr.add_overload(xaxji__rzxe)
    return jbsl__awfr


def _match_reduce_def(var_def, f_ir, ind):
    qreo__bik = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        qreo__bik = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        xetxd__cdxo = guard(find_callname, f_ir, var_def)
        if xetxd__cdxo == ('min', 'builtins'):
            qreo__bik = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if xetxd__cdxo == ('max', 'builtins'):
            qreo__bik = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return qreo__bik


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    zcb__scl = len(redvars)
    lzbhg__dsiq = 1
    ntoof__lqij = []
    for beryn__pjuoh in range(lzbhg__dsiq):
        tof__vdtrk = ir.Var(arr_var.scope, f'$input{beryn__pjuoh}', arr_var.loc
            )
        ntoof__lqij.append(tof__vdtrk)
    miov__dob = parfor.loop_nests[0].index_variable
    hgk__fjqaj = [0] * zcb__scl
    for knbti__qdi in parfor.loop_body.values():
        kflm__whiuz = []
        for yhdqn__jwp in knbti__qdi.body:
            if is_var_assign(yhdqn__jwp
                ) and yhdqn__jwp.value.name == miov__dob.name:
                continue
            if is_getitem(yhdqn__jwp
                ) and yhdqn__jwp.value.value.name == arr_var.name:
                yhdqn__jwp.value = ntoof__lqij[0]
            if is_call_assign(yhdqn__jwp) and guard(find_callname, pm.
                func_ir, yhdqn__jwp.value) == ('isna',
                'bodo.libs.array_kernels') and yhdqn__jwp.value.args[0
                ].name == arr_var.name:
                yhdqn__jwp.value = ir.Const(False, yhdqn__jwp.target.loc)
            if is_assign(yhdqn__jwp) and yhdqn__jwp.target.name in redvars:
                ind = redvars.index(yhdqn__jwp.target.name)
                hgk__fjqaj[ind] = yhdqn__jwp.target
            kflm__whiuz.append(yhdqn__jwp)
        knbti__qdi.body = kflm__whiuz
    lrorb__mzqsm = ['v{}'.format(beryn__pjuoh) for beryn__pjuoh in range(
        zcb__scl)]
    zvl__dhvr = ['in{}'.format(beryn__pjuoh) for beryn__pjuoh in range(
        lzbhg__dsiq)]
    qreo__bik = 'def agg_update({}):\n'.format(', '.join(lrorb__mzqsm +
        zvl__dhvr))
    qreo__bik += '    __update_redvars()\n'
    qreo__bik += '    return {}'.format(', '.join(['v{}'.format(
        beryn__pjuoh) for beryn__pjuoh in range(zcb__scl)]))
    huiub__kxju = {}
    exec(qreo__bik, {}, huiub__kxju)
    wvzo__fbbwl = huiub__kxju['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * lzbhg__dsiq)
    f_ir = compile_to_numba_ir(wvzo__fbbwl, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    rew__uns = f_ir.blocks.popitem()[1].body
    pyucv__uko = pm.typemap[rew__uns[-1].value.name]
    vizp__nznsw = wrap_parfor_blocks(parfor)
    kqetm__slsvz = find_topo_order(vizp__nznsw)
    kqetm__slsvz = kqetm__slsvz[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    zfy__eqic = f_ir.blocks[kqetm__slsvz[0]]
    yqe__bwpw = f_ir.blocks[kqetm__slsvz[-1]]
    nxcy__qms = rew__uns[:zcb__scl + lzbhg__dsiq]
    if zcb__scl > 1:
        xozzn__lhglx = rew__uns[-3:]
        assert is_assign(xozzn__lhglx[0]) and isinstance(xozzn__lhglx[0].
            value, ir.Expr) and xozzn__lhglx[0].value.op == 'build_tuple'
    else:
        xozzn__lhglx = rew__uns[-2:]
    for beryn__pjuoh in range(zcb__scl):
        pnooe__cdhop = rew__uns[beryn__pjuoh].target
        kgb__fzy = ir.Assign(pnooe__cdhop, hgk__fjqaj[beryn__pjuoh],
            pnooe__cdhop.loc)
        nxcy__qms.append(kgb__fzy)
    for beryn__pjuoh in range(zcb__scl, zcb__scl + lzbhg__dsiq):
        pnooe__cdhop = rew__uns[beryn__pjuoh].target
        kgb__fzy = ir.Assign(pnooe__cdhop, ntoof__lqij[beryn__pjuoh -
            zcb__scl], pnooe__cdhop.loc)
        nxcy__qms.append(kgb__fzy)
    zfy__eqic.body = nxcy__qms + zfy__eqic.body
    fvnk__lkmo = []
    for beryn__pjuoh in range(zcb__scl):
        pnooe__cdhop = rew__uns[beryn__pjuoh].target
        kgb__fzy = ir.Assign(hgk__fjqaj[beryn__pjuoh], pnooe__cdhop,
            pnooe__cdhop.loc)
        fvnk__lkmo.append(kgb__fzy)
    yqe__bwpw.body += fvnk__lkmo + xozzn__lhglx
    ucwmk__gupr = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        pyucv__uko, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jbsl__awfr = numba.core.target_extension.dispatcher_registry[cpu_target](
        wvzo__fbbwl)
    jbsl__awfr.add_overload(ucwmk__gupr)
    return jbsl__awfr


def _rm_arg_agg_block(block, typemap):
    bemaw__zrv = []
    arr_var = None
    for beryn__pjuoh, yhdqn__jwp in enumerate(block.body):
        if is_assign(yhdqn__jwp) and isinstance(yhdqn__jwp.value, ir.Arg):
            arr_var = yhdqn__jwp.target
            dmxe__uha = typemap[arr_var.name]
            if not isinstance(dmxe__uha, types.ArrayCompatible):
                bemaw__zrv += block.body[beryn__pjuoh + 1:]
                break
            vbd__yxr = block.body[beryn__pjuoh + 1]
            assert is_assign(vbd__yxr) and isinstance(vbd__yxr.value, ir.Expr
                ) and vbd__yxr.value.op == 'getattr' and vbd__yxr.value.attr == 'shape' and vbd__yxr.value.value.name == arr_var.name
            xllln__ble = vbd__yxr.target
            ybmap__xsxe = block.body[beryn__pjuoh + 2]
            assert is_assign(ybmap__xsxe) and isinstance(ybmap__xsxe.value,
                ir.Expr
                ) and ybmap__xsxe.value.op == 'static_getitem' and ybmap__xsxe.value.value.name == xllln__ble.name
            bemaw__zrv += block.body[beryn__pjuoh + 3:]
            break
        bemaw__zrv.append(yhdqn__jwp)
    return bemaw__zrv, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    vizp__nznsw = wrap_parfor_blocks(parfor)
    kqetm__slsvz = find_topo_order(vizp__nznsw)
    kqetm__slsvz = kqetm__slsvz[1:]
    unwrap_parfor_blocks(parfor)
    for xuc__cfa in reversed(kqetm__slsvz):
        for yhdqn__jwp in reversed(parfor.loop_body[xuc__cfa].body):
            if isinstance(yhdqn__jwp, ir.Assign) and (yhdqn__jwp.target.
                name in parfor_params or yhdqn__jwp.target.name in var_to_param
                ):
                hlrq__zwmy = yhdqn__jwp.target.name
                rhs = yhdqn__jwp.value
                nppz__rjirj = (hlrq__zwmy if hlrq__zwmy in parfor_params else
                    var_to_param[hlrq__zwmy])
                cuco__jvx = []
                if isinstance(rhs, ir.Var):
                    cuco__jvx = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    cuco__jvx = [sxa__xorac.name for sxa__xorac in
                        yhdqn__jwp.value.list_vars()]
                param_uses[nppz__rjirj].extend(cuco__jvx)
                for sxa__xorac in cuco__jvx:
                    var_to_param[sxa__xorac] = nppz__rjirj
            if isinstance(yhdqn__jwp, Parfor):
                get_parfor_reductions(yhdqn__jwp, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for rdkf__ismm, cuco__jvx in param_uses.items():
        if rdkf__ismm in cuco__jvx and rdkf__ismm not in reduce_varnames:
            reduce_varnames.append(rdkf__ismm)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
