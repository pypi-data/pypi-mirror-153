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
            sakom__qbal = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            tjyxc__wpf = cgutils.get_or_insert_function(builder.module,
                sakom__qbal, sym._literal_value)
            builder.call(tjyxc__wpf, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            sakom__qbal = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            tjyxc__wpf = cgutils.get_or_insert_function(builder.module,
                sakom__qbal, sym._literal_value)
            builder.call(tjyxc__wpf, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            sakom__qbal = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            tjyxc__wpf = cgutils.get_or_insert_function(builder.module,
                sakom__qbal, sym._literal_value)
            builder.call(tjyxc__wpf, [context.get_constant_null(sig.args[0]
                ), context.get_constant_null(sig.args[1]), context.
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
        fqz__edzlp = True
        qqty__clowd = 1
        lld__nki = -1
        if isinstance(rhs, ir.Expr):
            for qslqe__qbtd in rhs.kws:
                if func_name in list_cumulative:
                    if qslqe__qbtd[0] == 'skipna':
                        fqz__edzlp = guard(find_const, func_ir, qslqe__qbtd[1])
                        if not isinstance(fqz__edzlp, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if qslqe__qbtd[0] == 'dropna':
                        fqz__edzlp = guard(find_const, func_ir, qslqe__qbtd[1])
                        if not isinstance(fqz__edzlp, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            qqty__clowd = get_call_expr_arg('shift', rhs.args, dict(rhs.kws
                ), 0, 'periods', qqty__clowd)
            qqty__clowd = guard(find_const, func_ir, qqty__clowd)
        if func_name == 'head':
            lld__nki = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 0,
                'n', 5)
            if not isinstance(lld__nki, int):
                lld__nki = guard(find_const, func_ir, lld__nki)
            if lld__nki < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = fqz__edzlp
        func.periods = qqty__clowd
        func.head_n = lld__nki
        if func_name == 'transform':
            kws = dict(rhs.kws)
            sqrwl__fwq = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            mpekx__ryrk = typemap[sqrwl__fwq.name]
            lumt__pxp = None
            if isinstance(mpekx__ryrk, str):
                lumt__pxp = mpekx__ryrk
            elif is_overload_constant_str(mpekx__ryrk):
                lumt__pxp = get_overload_const_str(mpekx__ryrk)
            elif bodo.utils.typing.is_builtin_function(mpekx__ryrk):
                lumt__pxp = bodo.utils.typing.get_builtin_function_name(
                    mpekx__ryrk)
            if lumt__pxp not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {lumt__pxp}')
            func.transform_func = supported_agg_funcs.index(lumt__pxp)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    sqrwl__fwq = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if sqrwl__fwq == '':
        mpekx__ryrk = types.none
    else:
        mpekx__ryrk = typemap[sqrwl__fwq.name]
    if is_overload_constant_dict(mpekx__ryrk):
        wzk__qcfmy = get_overload_constant_dict(mpekx__ryrk)
        pwf__dej = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in wzk__qcfmy.values()]
        return pwf__dej
    if mpekx__ryrk == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(mpekx__ryrk, types.BaseTuple) or is_overload_constant_list(
        mpekx__ryrk):
        pwf__dej = []
        fxrzj__buwwg = 0
        if is_overload_constant_list(mpekx__ryrk):
            wec__ydvg = get_overload_const_list(mpekx__ryrk)
        else:
            wec__ydvg = mpekx__ryrk.types
        for t in wec__ydvg:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                pwf__dej.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(wec__ydvg) > 1:
                    func.fname = '<lambda_' + str(fxrzj__buwwg) + '>'
                    fxrzj__buwwg += 1
                pwf__dej.append(func)
        return [pwf__dej]
    if is_overload_constant_str(mpekx__ryrk):
        func_name = get_overload_const_str(mpekx__ryrk)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(mpekx__ryrk):
        func_name = bodo.utils.typing.get_builtin_function_name(mpekx__ryrk)
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
        fxrzj__buwwg = 0
        bjyz__jkl = []
        for yicj__pdur in f_val:
            func = get_agg_func_udf(func_ir, yicj__pdur, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{fxrzj__buwwg}>'
                fxrzj__buwwg += 1
            bjyz__jkl.append(func)
        return bjyz__jkl
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
    lumt__pxp = code.co_name
    return lumt__pxp


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
            ijs__xig = types.DType(args[0])
            return signature(ijs__xig, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    nlria__elw = nobs_a + nobs_b
    zurfa__kzg = (nobs_a * mean_a + nobs_b * mean_b) / nlria__elw
    uhaz__johyx = mean_b - mean_a
    qtbks__hcaa = (ssqdm_a + ssqdm_b + uhaz__johyx * uhaz__johyx * nobs_a *
        nobs_b / nlria__elw)
    return qtbks__hcaa, zurfa__kzg, nlria__elw


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
        cksr__erv = ''
        for oum__vik, gefl__jivqw in self.df_out_vars.items():
            cksr__erv += "'{}':{}, ".format(oum__vik, gefl__jivqw.name)
        emx__omin = '{}{{{}}}'.format(self.df_out, cksr__erv)
        aoy__llgn = ''
        for oum__vik, gefl__jivqw in self.df_in_vars.items():
            aoy__llgn += "'{}':{}, ".format(oum__vik, gefl__jivqw.name)
        deei__ivek = '{}{{{}}}'.format(self.df_in, aoy__llgn)
        jkgno__vgk = 'pivot {}:{}'.format(self.pivot_arr.name, self.
            pivot_values) if self.pivot_arr is not None else ''
        key_names = ','.join([str(kez__dpv) for kez__dpv in self.key_names])
        gypbj__bms = ','.join([gefl__jivqw.name for gefl__jivqw in self.
            key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(emx__omin,
            deei__ivek, key_names, gypbj__bms, jkgno__vgk)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        aaul__rrdc, exko__dnmz = self.gb_info_out.pop(out_col_name)
        if aaul__rrdc is None and not self.is_crosstab:
            return
        czjsl__gzif = self.gb_info_in[aaul__rrdc]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for wjgy__xew, (func, cksr__erv) in enumerate(czjsl__gzif):
                try:
                    cksr__erv.remove(out_col_name)
                    if len(cksr__erv) == 0:
                        czjsl__gzif.pop(wjgy__xew)
                        break
                except ValueError as aez__nwwgt:
                    continue
        else:
            for wjgy__xew, (func, egsek__ozyu) in enumerate(czjsl__gzif):
                if egsek__ozyu == out_col_name:
                    czjsl__gzif.pop(wjgy__xew)
                    break
        if len(czjsl__gzif) == 0:
            self.gb_info_in.pop(aaul__rrdc)
            self.df_in_vars.pop(aaul__rrdc)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({gefl__jivqw.name for gefl__jivqw in aggregate_node.
        key_arrs})
    use_set.update({gefl__jivqw.name for gefl__jivqw in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({gefl__jivqw.name for gefl__jivqw in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({gefl__jivqw.name for gefl__jivqw in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    bgoe__icta = [zmty__bjia for zmty__bjia, uoqb__bpz in aggregate_node.
        df_out_vars.items() if uoqb__bpz.name not in lives]
    for byyof__njyg in bgoe__icta:
        aggregate_node.remove_out_col(byyof__njyg)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(gefl__jivqw.name not in lives for
        gefl__jivqw in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    yopz__ewmck = set(gefl__jivqw.name for gefl__jivqw in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        yopz__ewmck.update({gefl__jivqw.name for gefl__jivqw in
            aggregate_node.out_key_vars})
    return set(), yopz__ewmck


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for wjgy__xew in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[wjgy__xew] = replace_vars_inner(aggregate_node
            .key_arrs[wjgy__xew], var_dict)
    for zmty__bjia in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[zmty__bjia] = replace_vars_inner(
            aggregate_node.df_in_vars[zmty__bjia], var_dict)
    for zmty__bjia in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[zmty__bjia] = replace_vars_inner(
            aggregate_node.df_out_vars[zmty__bjia], var_dict)
    if aggregate_node.out_key_vars is not None:
        for wjgy__xew in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[wjgy__xew] = replace_vars_inner(
                aggregate_node.out_key_vars[wjgy__xew], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for wjgy__xew in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[wjgy__xew] = visit_vars_inner(aggregate_node
            .key_arrs[wjgy__xew], callback, cbdata)
    for zmty__bjia in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[zmty__bjia] = visit_vars_inner(aggregate_node
            .df_in_vars[zmty__bjia], callback, cbdata)
    for zmty__bjia in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[zmty__bjia] = visit_vars_inner(
            aggregate_node.df_out_vars[zmty__bjia], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for wjgy__xew in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[wjgy__xew] = visit_vars_inner(
                aggregate_node.out_key_vars[wjgy__xew], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    elg__wod = []
    for dvnq__qkzgm in aggregate_node.key_arrs:
        fhbx__roa = equiv_set.get_shape(dvnq__qkzgm)
        if fhbx__roa:
            elg__wod.append(fhbx__roa[0])
    if aggregate_node.pivot_arr is not None:
        fhbx__roa = equiv_set.get_shape(aggregate_node.pivot_arr)
        if fhbx__roa:
            elg__wod.append(fhbx__roa[0])
    for uoqb__bpz in aggregate_node.df_in_vars.values():
        fhbx__roa = equiv_set.get_shape(uoqb__bpz)
        if fhbx__roa:
            elg__wod.append(fhbx__roa[0])
    if len(elg__wod) > 1:
        equiv_set.insert_equiv(*elg__wod)
    rjht__ieye = []
    elg__wod = []
    wdwg__hnfw = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        wdwg__hnfw.extend(aggregate_node.out_key_vars)
    for uoqb__bpz in wdwg__hnfw:
        gscr__tqa = typemap[uoqb__bpz.name]
        fpgmb__vrndg = array_analysis._gen_shape_call(equiv_set, uoqb__bpz,
            gscr__tqa.ndim, None, rjht__ieye)
        equiv_set.insert_equiv(uoqb__bpz, fpgmb__vrndg)
        elg__wod.append(fpgmb__vrndg[0])
        equiv_set.define(uoqb__bpz, set())
    if len(elg__wod) > 1:
        equiv_set.insert_equiv(*elg__wod)
    return [], rjht__ieye


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    fxybh__ttc = Distribution.OneD
    for uoqb__bpz in aggregate_node.df_in_vars.values():
        fxybh__ttc = Distribution(min(fxybh__ttc.value, array_dists[
            uoqb__bpz.name].value))
    for dvnq__qkzgm in aggregate_node.key_arrs:
        fxybh__ttc = Distribution(min(fxybh__ttc.value, array_dists[
            dvnq__qkzgm.name].value))
    if aggregate_node.pivot_arr is not None:
        fxybh__ttc = Distribution(min(fxybh__ttc.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = fxybh__ttc
    for uoqb__bpz in aggregate_node.df_in_vars.values():
        array_dists[uoqb__bpz.name] = fxybh__ttc
    for dvnq__qkzgm in aggregate_node.key_arrs:
        array_dists[dvnq__qkzgm.name] = fxybh__ttc
    ujndx__gequ = Distribution.OneD_Var
    for uoqb__bpz in aggregate_node.df_out_vars.values():
        if uoqb__bpz.name in array_dists:
            ujndx__gequ = Distribution(min(ujndx__gequ.value, array_dists[
                uoqb__bpz.name].value))
    if aggregate_node.out_key_vars is not None:
        for uoqb__bpz in aggregate_node.out_key_vars:
            if uoqb__bpz.name in array_dists:
                ujndx__gequ = Distribution(min(ujndx__gequ.value,
                    array_dists[uoqb__bpz.name].value))
    ujndx__gequ = Distribution(min(ujndx__gequ.value, fxybh__ttc.value))
    for uoqb__bpz in aggregate_node.df_out_vars.values():
        array_dists[uoqb__bpz.name] = ujndx__gequ
    if aggregate_node.out_key_vars is not None:
        for tkfgv__yynp in aggregate_node.out_key_vars:
            array_dists[tkfgv__yynp.name] = ujndx__gequ
    if ujndx__gequ != Distribution.OneD_Var:
        for dvnq__qkzgm in aggregate_node.key_arrs:
            array_dists[dvnq__qkzgm.name] = ujndx__gequ
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = ujndx__gequ
        for uoqb__bpz in aggregate_node.df_in_vars.values():
            array_dists[uoqb__bpz.name] = ujndx__gequ


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for uoqb__bpz in agg_node.df_out_vars.values():
        definitions[uoqb__bpz.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for tkfgv__yynp in agg_node.out_key_vars:
            definitions[tkfgv__yynp.name].append(agg_node)
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
        for gefl__jivqw in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[gefl__jivqw.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                gefl__jivqw.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    ifyap__lwxf = tuple(typemap[gefl__jivqw.name] for gefl__jivqw in
        agg_node.key_arrs)
    zsdc__vcri = [gefl__jivqw for chz__msxex, gefl__jivqw in agg_node.
        df_in_vars.items()]
    fho__zqc = [gefl__jivqw for chz__msxex, gefl__jivqw in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    pwf__dej = []
    if agg_node.pivot_arr is not None:
        for aaul__rrdc, czjsl__gzif in agg_node.gb_info_in.items():
            for func, exko__dnmz in czjsl__gzif:
                if aaul__rrdc is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        aaul__rrdc].name])
                pwf__dej.append(func)
    else:
        for aaul__rrdc, func in agg_node.gb_info_out.values():
            if aaul__rrdc is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[aaul__rrdc].
                    name])
            pwf__dej.append(func)
    out_col_typs = tuple(typemap[gefl__jivqw.name] for gefl__jivqw in fho__zqc)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(ifyap__lwxf + tuple(typemap[gefl__jivqw.name] for
        gefl__jivqw in zsdc__vcri) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    gazvi__afz = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for wjgy__xew, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            gazvi__afz.update({f'in_cat_dtype_{wjgy__xew}': in_col_typ})
    for wjgy__xew, tbhkp__ncec in enumerate(out_col_typs):
        if isinstance(tbhkp__ncec, bodo.CategoricalArrayType):
            gazvi__afz.update({f'out_cat_dtype_{wjgy__xew}': tbhkp__ncec})
    udf_func_struct = get_udf_func_struct(pwf__dej, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    ucbvu__obr = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    gazvi__afz.update({'pd': pd, 'pre_alloc_string_array':
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
            gazvi__afz.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            gazvi__afz.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    eub__rie = compile_to_numba_ir(ucbvu__obr, gazvi__afz, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    sco__ghwpv = []
    if agg_node.pivot_arr is None:
        cns__dxkeh = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        dex__okv = ir.Var(cns__dxkeh, mk_unique_var('dummy_none'), loc)
        typemap[dex__okv.name] = types.none
        sco__ghwpv.append(ir.Assign(ir.Const(None, loc), dex__okv, loc))
        zsdc__vcri.append(dex__okv)
    else:
        zsdc__vcri.append(agg_node.pivot_arr)
    replace_arg_nodes(eub__rie, agg_node.key_arrs + zsdc__vcri)
    auk__hnqd = eub__rie.body[-3]
    assert is_assign(auk__hnqd) and isinstance(auk__hnqd.value, ir.Expr
        ) and auk__hnqd.value.op == 'build_tuple'
    sco__ghwpv += eub__rie.body[:-3]
    wdwg__hnfw = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        wdwg__hnfw += agg_node.out_key_vars
    for wjgy__xew, oftim__beau in enumerate(wdwg__hnfw):
        ffshl__qrb = auk__hnqd.value.items[wjgy__xew]
        sco__ghwpv.append(ir.Assign(ffshl__qrb, oftim__beau, oftim__beau.loc))
    return sco__ghwpv


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        ebql__ioiyy = args[0]
        dtype = types.Tuple([t.dtype for t in ebql__ioiyy.types]
            ) if isinstance(ebql__ioiyy, types.BaseTuple
            ) else ebql__ioiyy.dtype
        if isinstance(ebql__ioiyy, types.BaseTuple) and len(ebql__ioiyy.types
            ) == 1:
            dtype = ebql__ioiyy.types[0].dtype
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
        irrhp__nhki = args[0]
        if irrhp__nhki == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    ksyl__tcin = context.compile_internal(builder, lambda a: False, sig, args)
    return ksyl__tcin


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        spe__jkvi = IntDtype(t.dtype).name
        assert spe__jkvi.endswith('Dtype()')
        spe__jkvi = spe__jkvi[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{spe__jkvi}'))"
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
        yoi__ztm = 'in' if is_input else 'out'
        return f'bodo.utils.utils.alloc_type(1, {yoi__ztm}_cat_dtype_{colnum})'
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
    wvs__rvjnw = udf_func_struct.var_typs
    xgwvu__nmbhk = len(wvs__rvjnw)
    gwlz__zrld = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    gwlz__zrld += '    if is_null_pointer(in_table):\n'
    gwlz__zrld += '        return\n'
    gwlz__zrld += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in wvs__rvjnw]), 
        ',' if len(wvs__rvjnw) == 1 else '')
    mgn__ozsc = n_keys
    ogfyq__hyb = []
    redvar_offsets = []
    uoe__msmpq = []
    if do_combine:
        for wjgy__xew, yicj__pdur in enumerate(allfuncs):
            if yicj__pdur.ftype != 'udf':
                mgn__ozsc += yicj__pdur.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(mgn__ozsc, mgn__ozsc +
                    yicj__pdur.n_redvars))
                mgn__ozsc += yicj__pdur.n_redvars
                uoe__msmpq.append(data_in_typs_[func_idx_to_in_col[wjgy__xew]])
                ogfyq__hyb.append(func_idx_to_in_col[wjgy__xew] + n_keys)
    else:
        for wjgy__xew, yicj__pdur in enumerate(allfuncs):
            if yicj__pdur.ftype != 'udf':
                mgn__ozsc += yicj__pdur.ncols_post_shuffle
            else:
                redvar_offsets += list(range(mgn__ozsc + 1, mgn__ozsc + 1 +
                    yicj__pdur.n_redvars))
                mgn__ozsc += yicj__pdur.n_redvars + 1
                uoe__msmpq.append(data_in_typs_[func_idx_to_in_col[wjgy__xew]])
                ogfyq__hyb.append(func_idx_to_in_col[wjgy__xew] + n_keys)
    assert len(redvar_offsets) == xgwvu__nmbhk
    fub__hvfe = len(uoe__msmpq)
    gtljg__bnk = []
    for wjgy__xew, t in enumerate(uoe__msmpq):
        gtljg__bnk.append(_gen_dummy_alloc(t, wjgy__xew, True))
    gwlz__zrld += '    data_in_dummy = ({}{})\n'.format(','.join(gtljg__bnk
        ), ',' if len(uoe__msmpq) == 1 else '')
    gwlz__zrld += """
    # initialize redvar cols
"""
    gwlz__zrld += '    init_vals = __init_func()\n'
    for wjgy__xew in range(xgwvu__nmbhk):
        gwlz__zrld += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(wjgy__xew, redvar_offsets[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(redvar_arr_{})\n'.format(wjgy__xew)
        gwlz__zrld += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            wjgy__xew, wjgy__xew)
    gwlz__zrld += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(wjgy__xew) for wjgy__xew in range(xgwvu__nmbhk)]), ',' if 
        xgwvu__nmbhk == 1 else '')
    gwlz__zrld += '\n'
    for wjgy__xew in range(fub__hvfe):
        gwlz__zrld += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(wjgy__xew, ogfyq__hyb[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(data_in_{})\n'.format(wjgy__xew)
    gwlz__zrld += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(wjgy__xew) for wjgy__xew in range(fub__hvfe)]), ',' if 
        fub__hvfe == 1 else '')
    gwlz__zrld += '\n'
    gwlz__zrld += '    for i in range(len(data_in_0)):\n'
    gwlz__zrld += '        w_ind = row_to_group[i]\n'
    gwlz__zrld += '        if w_ind != -1:\n'
    gwlz__zrld += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    qajgj__irv = {}
    exec(gwlz__zrld, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, qajgj__irv)
    return qajgj__irv['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    wvs__rvjnw = udf_func_struct.var_typs
    xgwvu__nmbhk = len(wvs__rvjnw)
    gwlz__zrld = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    gwlz__zrld += '    if is_null_pointer(in_table):\n'
    gwlz__zrld += '        return\n'
    gwlz__zrld += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in wvs__rvjnw]), 
        ',' if len(wvs__rvjnw) == 1 else '')
    bbrg__xfep = n_keys
    mshtu__gjztw = n_keys
    kfk__ldb = []
    luob__yygi = []
    for yicj__pdur in allfuncs:
        if yicj__pdur.ftype != 'udf':
            bbrg__xfep += yicj__pdur.ncols_pre_shuffle
            mshtu__gjztw += yicj__pdur.ncols_post_shuffle
        else:
            kfk__ldb += list(range(bbrg__xfep, bbrg__xfep + yicj__pdur.
                n_redvars))
            luob__yygi += list(range(mshtu__gjztw + 1, mshtu__gjztw + 1 +
                yicj__pdur.n_redvars))
            bbrg__xfep += yicj__pdur.n_redvars
            mshtu__gjztw += 1 + yicj__pdur.n_redvars
    assert len(kfk__ldb) == xgwvu__nmbhk
    gwlz__zrld += """
    # initialize redvar cols
"""
    gwlz__zrld += '    init_vals = __init_func()\n'
    for wjgy__xew in range(xgwvu__nmbhk):
        gwlz__zrld += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(wjgy__xew, luob__yygi[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(redvar_arr_{})\n'.format(wjgy__xew)
        gwlz__zrld += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            wjgy__xew, wjgy__xew)
    gwlz__zrld += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(wjgy__xew) for wjgy__xew in range(xgwvu__nmbhk)]), ',' if 
        xgwvu__nmbhk == 1 else '')
    gwlz__zrld += '\n'
    for wjgy__xew in range(xgwvu__nmbhk):
        gwlz__zrld += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(wjgy__xew, kfk__ldb[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(recv_redvar_arr_{})\n'.format(wjgy__xew)
    gwlz__zrld += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(wjgy__xew) for wjgy__xew in range(
        xgwvu__nmbhk)]), ',' if xgwvu__nmbhk == 1 else '')
    gwlz__zrld += '\n'
    if xgwvu__nmbhk:
        gwlz__zrld += '    for i in range(len(recv_redvar_arr_0)):\n'
        gwlz__zrld += '        w_ind = row_to_group[i]\n'
        gwlz__zrld += """        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)
"""
    qajgj__irv = {}
    exec(gwlz__zrld, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, qajgj__irv)
    return qajgj__irv['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    wvs__rvjnw = udf_func_struct.var_typs
    xgwvu__nmbhk = len(wvs__rvjnw)
    mgn__ozsc = n_keys
    redvar_offsets = []
    nind__wipl = []
    out_data_typs = []
    for wjgy__xew, yicj__pdur in enumerate(allfuncs):
        if yicj__pdur.ftype != 'udf':
            mgn__ozsc += yicj__pdur.ncols_post_shuffle
        else:
            nind__wipl.append(mgn__ozsc)
            redvar_offsets += list(range(mgn__ozsc + 1, mgn__ozsc + 1 +
                yicj__pdur.n_redvars))
            mgn__ozsc += 1 + yicj__pdur.n_redvars
            out_data_typs.append(out_data_typs_[wjgy__xew])
    assert len(redvar_offsets) == xgwvu__nmbhk
    fub__hvfe = len(out_data_typs)
    gwlz__zrld = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    gwlz__zrld += '    if is_null_pointer(table):\n'
    gwlz__zrld += '        return\n'
    gwlz__zrld += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in wvs__rvjnw]), 
        ',' if len(wvs__rvjnw) == 1 else '')
    gwlz__zrld += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for wjgy__xew in range(xgwvu__nmbhk):
        gwlz__zrld += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(wjgy__xew, redvar_offsets[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(redvar_arr_{})\n'.format(wjgy__xew)
    gwlz__zrld += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(wjgy__xew) for wjgy__xew in range(xgwvu__nmbhk)]), ',' if 
        xgwvu__nmbhk == 1 else '')
    gwlz__zrld += '\n'
    for wjgy__xew in range(fub__hvfe):
        gwlz__zrld += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(wjgy__xew, nind__wipl[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(data_out_{})\n'.format(wjgy__xew)
    gwlz__zrld += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(wjgy__xew) for wjgy__xew in range(fub__hvfe)]), ',' if 
        fub__hvfe == 1 else '')
    gwlz__zrld += '\n'
    gwlz__zrld += '    for i in range(len(data_out_0)):\n'
    gwlz__zrld += '        __eval_res(redvars, data_out, i)\n'
    qajgj__irv = {}
    exec(gwlz__zrld, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, qajgj__irv)
    return qajgj__irv['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    mgn__ozsc = n_keys
    xmls__qzuuv = []
    for wjgy__xew, yicj__pdur in enumerate(allfuncs):
        if yicj__pdur.ftype == 'gen_udf':
            xmls__qzuuv.append(mgn__ozsc)
            mgn__ozsc += 1
        elif yicj__pdur.ftype != 'udf':
            mgn__ozsc += yicj__pdur.ncols_post_shuffle
        else:
            mgn__ozsc += yicj__pdur.n_redvars + 1
    gwlz__zrld = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    gwlz__zrld += '    if num_groups == 0:\n'
    gwlz__zrld += '        return\n'
    for wjgy__xew, func in enumerate(udf_func_struct.general_udf_funcs):
        gwlz__zrld += '    # col {}\n'.format(wjgy__xew)
        gwlz__zrld += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(xmls__qzuuv[wjgy__xew], wjgy__xew))
        gwlz__zrld += '    incref(out_col)\n'
        gwlz__zrld += '    for j in range(num_groups):\n'
        gwlz__zrld += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(wjgy__xew, wjgy__xew))
        gwlz__zrld += '        incref(in_col)\n'
        gwlz__zrld += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(wjgy__xew))
    gazvi__afz = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    rqo__xiw = 0
    for wjgy__xew, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[rqo__xiw]
        gazvi__afz['func_{}'.format(rqo__xiw)] = func
        gazvi__afz['in_col_{}_typ'.format(rqo__xiw)] = in_col_typs[
            func_idx_to_in_col[wjgy__xew]]
        gazvi__afz['out_col_{}_typ'.format(rqo__xiw)] = out_col_typs[wjgy__xew]
        rqo__xiw += 1
    qajgj__irv = {}
    exec(gwlz__zrld, gazvi__afz, qajgj__irv)
    yicj__pdur = qajgj__irv['bodo_gb_apply_general_udfs{}'.format(label_suffix)
        ]
    tixjl__gvh = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(tixjl__gvh, nopython=True)(yicj__pdur)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    bjqp__urd = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        ekbo__cgbeu = 1
    else:
        ekbo__cgbeu = len(agg_node.pivot_values)
    vunb__iulw = tuple('key_' + sanitize_varname(oum__vik) for oum__vik in
        agg_node.key_names)
    kubtn__hcddi = {oum__vik: 'in_{}'.format(sanitize_varname(oum__vik)) for
        oum__vik in agg_node.gb_info_in.keys() if oum__vik is not None}
    qrtay__cra = {oum__vik: ('out_' + sanitize_varname(oum__vik)) for
        oum__vik in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    msnr__grld = ', '.join(vunb__iulw)
    vszuq__axk = ', '.join(kubtn__hcddi.values())
    if vszuq__axk != '':
        vszuq__axk = ', ' + vszuq__axk
    gwlz__zrld = 'def agg_top({}{}{}, pivot_arr):\n'.format(msnr__grld,
        vszuq__axk, ', index_arg' if agg_node.input_has_index else '')
    for a in (vunb__iulw + tuple(kubtn__hcddi.values())):
        gwlz__zrld += f'    {a} = decode_if_dict_array({a})\n'
    if bjqp__urd:
        gwlz__zrld += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        jvwl__afof = []
        for aaul__rrdc, czjsl__gzif in agg_node.gb_info_in.items():
            if aaul__rrdc is not None:
                for func, exko__dnmz in czjsl__gzif:
                    jvwl__afof.append(kubtn__hcddi[aaul__rrdc])
    else:
        jvwl__afof = tuple(kubtn__hcddi[aaul__rrdc] for aaul__rrdc,
            exko__dnmz in agg_node.gb_info_out.values() if aaul__rrdc is not
            None)
    crrb__ofhd = vunb__iulw + tuple(jvwl__afof)
    gwlz__zrld += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in crrb__ofhd), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    gwlz__zrld += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    cedpk__kgv = []
    func_idx_to_in_col = []
    ywk__mjxml = []
    fqz__edzlp = False
    uagqm__euv = 1
    lld__nki = -1
    ibun__xei = 0
    nvd__cwp = 0
    if not bjqp__urd:
        pwf__dej = [func for exko__dnmz, func in agg_node.gb_info_out.values()]
    else:
        pwf__dej = [func for func, exko__dnmz in czjsl__gzif for
            czjsl__gzif in agg_node.gb_info_in.values()]
    for hxjh__sdey, func in enumerate(pwf__dej):
        cedpk__kgv.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            ibun__xei += 1
        if hasattr(func, 'skipdropna'):
            fqz__edzlp = func.skipdropna
        if func.ftype == 'shift':
            uagqm__euv = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            nvd__cwp = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            lld__nki = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(hxjh__sdey)
        if func.ftype == 'udf':
            ywk__mjxml.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            ywk__mjxml.append(0)
            do_combine = False
    cedpk__kgv.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == ekbo__cgbeu, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * ekbo__cgbeu, 'invalid number of groupby outputs'
    if ibun__xei > 0:
        if ibun__xei != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for wjgy__xew, oum__vik in enumerate(agg_node.gb_info_out.keys()):
        dok__hwc = qrtay__cra[oum__vik] + '_dummy'
        tbhkp__ncec = out_col_typs[wjgy__xew]
        aaul__rrdc, func = agg_node.gb_info_out[oum__vik]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(tbhkp__ncec, bodo.
            CategoricalArrayType):
            gwlz__zrld += '    {} = {}\n'.format(dok__hwc, kubtn__hcddi[
                aaul__rrdc])
        elif udf_func_struct is not None:
            gwlz__zrld += '    {} = {}\n'.format(dok__hwc, _gen_dummy_alloc
                (tbhkp__ncec, wjgy__xew, False))
    if udf_func_struct is not None:
        iltxk__eis = next_label()
        if udf_func_struct.regular_udfs:
            tixjl__gvh = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            okg__zoqa = numba.cfunc(tixjl__gvh, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, iltxk__eis))
            fujbo__gbj = numba.cfunc(tixjl__gvh, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, iltxk__eis))
            fovl__hrc = numba.cfunc('void(voidptr)', nopython=True)(gen_eval_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, iltxk__eis))
            udf_func_struct.set_regular_cfuncs(okg__zoqa, fujbo__gbj, fovl__hrc
                )
            for dgx__uqydx in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[dgx__uqydx.native_name] = dgx__uqydx
                gb_agg_cfunc_addr[dgx__uqydx.native_name] = dgx__uqydx.address
        if udf_func_struct.general_udfs:
            xvqh__uemx = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                iltxk__eis)
            udf_func_struct.set_general_cfunc(xvqh__uemx)
        zsrej__kea = []
        qqkmy__gummh = 0
        wjgy__xew = 0
        for dok__hwc, yicj__pdur in zip(qrtay__cra.values(), allfuncs):
            if yicj__pdur.ftype in ('udf', 'gen_udf'):
                zsrej__kea.append(dok__hwc + '_dummy')
                for kzyzg__xpfa in range(qqkmy__gummh, qqkmy__gummh +
                    ywk__mjxml[wjgy__xew]):
                    zsrej__kea.append('data_redvar_dummy_' + str(kzyzg__xpfa))
                qqkmy__gummh += ywk__mjxml[wjgy__xew]
                wjgy__xew += 1
        if udf_func_struct.regular_udfs:
            wvs__rvjnw = udf_func_struct.var_typs
            for wjgy__xew, t in enumerate(wvs__rvjnw):
                gwlz__zrld += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(wjgy__xew, _get_np_dtype(t)))
        gwlz__zrld += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in zsrej__kea))
        gwlz__zrld += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            gwlz__zrld += ("    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".
                format(okg__zoqa.native_name))
            gwlz__zrld += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(fujbo__gbj.native_name))
            gwlz__zrld += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                fovl__hrc.native_name)
            gwlz__zrld += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(okg__zoqa.native_name))
            gwlz__zrld += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(fujbo__gbj.native_name))
            gwlz__zrld += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(fovl__hrc.native_name))
        else:
            gwlz__zrld += '    cpp_cb_update_addr = 0\n'
            gwlz__zrld += '    cpp_cb_combine_addr = 0\n'
            gwlz__zrld += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            dgx__uqydx = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[dgx__uqydx.native_name] = dgx__uqydx
            gb_agg_cfunc_addr[dgx__uqydx.native_name] = dgx__uqydx.address
            gwlz__zrld += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(dgx__uqydx.native_name))
            gwlz__zrld += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(dgx__uqydx.native_name))
        else:
            gwlz__zrld += '    cpp_cb_general_addr = 0\n'
    else:
        gwlz__zrld += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        gwlz__zrld += '    cpp_cb_update_addr = 0\n'
        gwlz__zrld += '    cpp_cb_combine_addr = 0\n'
        gwlz__zrld += '    cpp_cb_eval_addr = 0\n'
        gwlz__zrld += '    cpp_cb_general_addr = 0\n'
    gwlz__zrld += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(yicj__pdur.ftype)) for
        yicj__pdur in allfuncs] + ['0']))
    gwlz__zrld += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(
        str(cedpk__kgv))
    if len(ywk__mjxml) > 0:
        gwlz__zrld += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(ywk__mjxml))
    else:
        gwlz__zrld += '    udf_ncols = np.array([0], np.int32)\n'
    if bjqp__urd:
        gwlz__zrld += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        gwlz__zrld += '    arr_info = array_to_info(arr_type)\n'
        gwlz__zrld += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        gwlz__zrld += '    pivot_info = array_to_info(pivot_arr)\n'
        gwlz__zrld += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        gwlz__zrld += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, fqz__edzlp, agg_node.return_key, agg_node.same_index))
        gwlz__zrld += '    delete_info_decref_array(pivot_info)\n'
        gwlz__zrld += '    delete_info_decref_array(arr_info)\n'
    else:
        gwlz__zrld += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, fqz__edzlp,
            uagqm__euv, nvd__cwp, lld__nki, agg_node.return_key, agg_node.
            same_index, agg_node.dropna))
    havgd__lqa = 0
    if agg_node.return_key:
        for wjgy__xew, ltfo__iaq in enumerate(vunb__iulw):
            gwlz__zrld += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(ltfo__iaq, havgd__lqa, ltfo__iaq))
            havgd__lqa += 1
    for wjgy__xew, dok__hwc in enumerate(qrtay__cra.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(tbhkp__ncec, bodo.
            CategoricalArrayType):
            gwlz__zrld += f"""    {dok__hwc} = info_to_array(info_from_table(out_table, {havgd__lqa}), {dok__hwc + '_dummy'})
"""
        else:
            gwlz__zrld += f"""    {dok__hwc} = info_to_array(info_from_table(out_table, {havgd__lqa}), out_typs[{wjgy__xew}])
"""
        havgd__lqa += 1
    if agg_node.same_index:
        gwlz__zrld += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(havgd__lqa))
        havgd__lqa += 1
    gwlz__zrld += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    gwlz__zrld += '    delete_table_decref_arrays(table)\n'
    gwlz__zrld += '    delete_table_decref_arrays(udf_table_dummy)\n'
    gwlz__zrld += '    delete_table(out_table)\n'
    gwlz__zrld += f'    ev_clean.finalize()\n'
    exlt__qixy = tuple(qrtay__cra.values())
    if agg_node.return_key:
        exlt__qixy += tuple(vunb__iulw)
    gwlz__zrld += '    return ({},{})\n'.format(', '.join(exlt__qixy), 
        ' out_index_arg,' if agg_node.same_index else '')
    qajgj__irv = {}
    exec(gwlz__zrld, {'out_typs': out_col_typs}, qajgj__irv)
    cvi__anioi = qajgj__irv['agg_top']
    return cvi__anioi


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for akg__lqg in block.body:
            if is_call_assign(akg__lqg) and find_callname(f_ir, akg__lqg.value
                ) == ('len', 'builtins') and akg__lqg.value.args[0
                ].name == f_ir.arg_names[0]:
                eqlk__wzxu = get_definition(f_ir, akg__lqg.value.func)
                eqlk__wzxu.name = 'dummy_agg_count'
                eqlk__wzxu.value = dummy_agg_count
    rjxws__affe = get_name_var_table(f_ir.blocks)
    gxk__rzmzq = {}
    for name, exko__dnmz in rjxws__affe.items():
        gxk__rzmzq[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, gxk__rzmzq)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    azpe__qrhm = numba.core.compiler.Flags()
    azpe__qrhm.nrt = True
    vtjr__rvj = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, azpe__qrhm)
    vtjr__rvj.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, awo__gry, calltypes, exko__dnmz = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    rnpmu__hajs = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    bolee__wwfay = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    xjyj__quv = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    pju__dae = xjyj__quv(typemap, calltypes)
    pm = bolee__wwfay(typingctx, targetctx, None, f_ir, typemap, awo__gry,
        calltypes, pju__dae, {}, azpe__qrhm, None)
    idf__aspmb = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = bolee__wwfay(typingctx, targetctx, None, f_ir, typemap, awo__gry,
        calltypes, pju__dae, {}, azpe__qrhm, idf__aspmb)
    easc__mdhs = numba.core.typed_passes.InlineOverloads()
    easc__mdhs.run_pass(pm)
    wnwul__yry = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    wnwul__yry.run()
    for block in f_ir.blocks.values():
        for akg__lqg in block.body:
            if is_assign(akg__lqg) and isinstance(akg__lqg.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[akg__lqg.target.name],
                SeriesType):
                gscr__tqa = typemap.pop(akg__lqg.target.name)
                typemap[akg__lqg.target.name] = gscr__tqa.data
            if is_call_assign(akg__lqg) and find_callname(f_ir, akg__lqg.value
                ) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[akg__lqg.target.name].remove(akg__lqg.value)
                akg__lqg.value = akg__lqg.value.args[0]
                f_ir._definitions[akg__lqg.target.name].append(akg__lqg.value)
            if is_call_assign(akg__lqg) and find_callname(f_ir, akg__lqg.value
                ) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[akg__lqg.target.name].remove(akg__lqg.value)
                akg__lqg.value = ir.Const(False, akg__lqg.loc)
                f_ir._definitions[akg__lqg.target.name].append(akg__lqg.value)
            if is_call_assign(akg__lqg) and find_callname(f_ir, akg__lqg.value
                ) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[akg__lqg.target.name].remove(akg__lqg.value)
                akg__lqg.value = ir.Const(False, akg__lqg.loc)
                f_ir._definitions[akg__lqg.target.name].append(akg__lqg.value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    rrigt__cqzos = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, rnpmu__hajs)
    rrigt__cqzos.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    jhj__wqduf = numba.core.compiler.StateDict()
    jhj__wqduf.func_ir = f_ir
    jhj__wqduf.typemap = typemap
    jhj__wqduf.calltypes = calltypes
    jhj__wqduf.typingctx = typingctx
    jhj__wqduf.targetctx = targetctx
    jhj__wqduf.return_type = awo__gry
    numba.core.rewrites.rewrite_registry.apply('after-inference', jhj__wqduf)
    jyuua__ckg = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        awo__gry, typingctx, targetctx, rnpmu__hajs, azpe__qrhm, {})
    jyuua__ckg.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            pzf__hesp = ctypes.pythonapi.PyCell_Get
            pzf__hesp.restype = ctypes.py_object
            pzf__hesp.argtypes = ctypes.py_object,
            wzk__qcfmy = tuple(pzf__hesp(prucs__rixg) for prucs__rixg in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            wzk__qcfmy = closure.items
        assert len(code.co_freevars) == len(wzk__qcfmy)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, wzk__qcfmy
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
        pcx__psv = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (pcx__psv,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        cvbq__use, arr_var = _rm_arg_agg_block(block, pm.typemap)
        hfuwm__xkum = -1
        for wjgy__xew, akg__lqg in enumerate(cvbq__use):
            if isinstance(akg__lqg, numba.parfors.parfor.Parfor):
                assert hfuwm__xkum == -1, 'only one parfor for aggregation function'
                hfuwm__xkum = wjgy__xew
        parfor = None
        if hfuwm__xkum != -1:
            parfor = cvbq__use[hfuwm__xkum]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = cvbq__use[:hfuwm__xkum] + parfor.init_block.body
        eval_nodes = cvbq__use[hfuwm__xkum + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for akg__lqg in init_nodes:
            if is_assign(akg__lqg) and akg__lqg.target.name in redvars:
                ind = redvars.index(akg__lqg.target.name)
                reduce_vars[ind] = akg__lqg.target
        var_types = [pm.typemap[gefl__jivqw] for gefl__jivqw in redvars]
        kyjou__gwf = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        xcuso__guu = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        pmeo__qxrsf = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(pmeo__qxrsf)
        self.all_update_funcs.append(xcuso__guu)
        self.all_combine_funcs.append(kyjou__gwf)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        hll__suufp = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        dwqk__ygjnk = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        jdw__djqmg = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        wqba__bguf = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, hll__suufp, dwqk__ygjnk, jdw__djqmg,
            wqba__bguf)


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
    yes__cibqd = []
    for t, yicj__pdur in zip(in_col_types, agg_func):
        yes__cibqd.append((t, yicj__pdur))
    zol__adc = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    grp__amh = GeneralUDFGenerator()
    for in_col_typ, func in yes__cibqd:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            zol__adc.add_udf(in_col_typ, func)
        except:
            grp__amh.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = zol__adc.gen_all_func()
    general_udf_funcs = grp__amh.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    izky__fohvd = compute_use_defs(parfor.loop_body)
    awvz__bmte = set()
    for mth__euzh in izky__fohvd.usemap.values():
        awvz__bmte |= mth__euzh
    uqwr__qalr = set()
    for mth__euzh in izky__fohvd.defmap.values():
        uqwr__qalr |= mth__euzh
    xjwpd__snobv = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    xjwpd__snobv.body = eval_nodes
    jag__cqmh = compute_use_defs({(0): xjwpd__snobv})
    ojf__tgdfn = jag__cqmh.usemap[0]
    hua__mtvqb = set()
    gdb__zqnow = []
    hvp__jxske = []
    for akg__lqg in reversed(init_nodes):
        qbb__ayq = {gefl__jivqw.name for gefl__jivqw in akg__lqg.list_vars()}
        if is_assign(akg__lqg):
            gefl__jivqw = akg__lqg.target.name
            qbb__ayq.remove(gefl__jivqw)
            if (gefl__jivqw in awvz__bmte and gefl__jivqw not in hua__mtvqb and
                gefl__jivqw not in ojf__tgdfn and gefl__jivqw not in uqwr__qalr
                ):
                hvp__jxske.append(akg__lqg)
                awvz__bmte |= qbb__ayq
                uqwr__qalr.add(gefl__jivqw)
                continue
        hua__mtvqb |= qbb__ayq
        gdb__zqnow.append(akg__lqg)
    hvp__jxske.reverse()
    gdb__zqnow.reverse()
    jwxm__nmwil = min(parfor.loop_body.keys())
    qmuod__gxkda = parfor.loop_body[jwxm__nmwil]
    qmuod__gxkda.body = hvp__jxske + qmuod__gxkda.body
    return gdb__zqnow


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    khh__vmfmx = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    awusg__wab = set()
    rzhtz__fep = []
    for akg__lqg in init_nodes:
        if is_assign(akg__lqg) and isinstance(akg__lqg.value, ir.Global
            ) and isinstance(akg__lqg.value.value, pytypes.FunctionType
            ) and akg__lqg.value.value in khh__vmfmx:
            awusg__wab.add(akg__lqg.target.name)
        elif is_call_assign(akg__lqg
            ) and akg__lqg.value.func.name in awusg__wab:
            pass
        else:
            rzhtz__fep.append(akg__lqg)
    init_nodes = rzhtz__fep
    wfd__gbtt = types.Tuple(var_types)
    cmlsg__mqjh = lambda : None
    f_ir = compile_to_numba_ir(cmlsg__mqjh, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    yarx__gmemw = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    uugn__cqe = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        yarx__gmemw, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [uugn__cqe] + block.body
    block.body[-2].value.value = yarx__gmemw
    nxrum__xdr = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        wfd__gbtt, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    zwweb__gzhdx = numba.core.target_extension.dispatcher_registry[cpu_target](
        cmlsg__mqjh)
    zwweb__gzhdx.add_overload(nxrum__xdr)
    return zwweb__gzhdx


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    sixu__ssq = len(update_funcs)
    uau__key = len(in_col_types)
    if pivot_values is not None:
        assert uau__key == 1
    gwlz__zrld = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        nkdf__nme = redvar_offsets[uau__key]
        gwlz__zrld += '  pv = pivot_arr[i]\n'
        for kzyzg__xpfa, vvep__hmn in enumerate(pivot_values):
            yapza__ennnw = 'el' if kzyzg__xpfa != 0 else ''
            gwlz__zrld += "  {}if pv == '{}':\n".format(yapza__ennnw, vvep__hmn
                )
            iftij__oopbv = nkdf__nme * kzyzg__xpfa
            tbr__xbwrp = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                wjgy__xew) for wjgy__xew in range(iftij__oopbv +
                redvar_offsets[0], iftij__oopbv + redvar_offsets[1])])
            qioyx__uknvh = 'data_in[0][i]'
            if is_crosstab:
                qioyx__uknvh = '0'
            gwlz__zrld += '    {} = update_vars_0({}, {})\n'.format(tbr__xbwrp,
                tbr__xbwrp, qioyx__uknvh)
    else:
        for kzyzg__xpfa in range(sixu__ssq):
            tbr__xbwrp = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                wjgy__xew) for wjgy__xew in range(redvar_offsets[
                kzyzg__xpfa], redvar_offsets[kzyzg__xpfa + 1])])
            if tbr__xbwrp:
                gwlz__zrld += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(tbr__xbwrp, kzyzg__xpfa, tbr__xbwrp, 0 if 
                    uau__key == 1 else kzyzg__xpfa))
    gwlz__zrld += '  return\n'
    gazvi__afz = {}
    for wjgy__xew, yicj__pdur in enumerate(update_funcs):
        gazvi__afz['update_vars_{}'.format(wjgy__xew)] = yicj__pdur
    qajgj__irv = {}
    exec(gwlz__zrld, gazvi__afz, qajgj__irv)
    ykrmt__nlj = qajgj__irv['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(ykrmt__nlj)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    vphke__wgibw = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    arg_typs = vphke__wgibw, vphke__wgibw, types.intp, types.intp, pivot_typ
    hyqyl__yjpmx = len(redvar_offsets) - 1
    nkdf__nme = redvar_offsets[hyqyl__yjpmx]
    gwlz__zrld = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert hyqyl__yjpmx == 1
        for kez__dpv in range(len(pivot_values)):
            iftij__oopbv = nkdf__nme * kez__dpv
            tbr__xbwrp = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                wjgy__xew) for wjgy__xew in range(iftij__oopbv +
                redvar_offsets[0], iftij__oopbv + redvar_offsets[1])])
            wgnvm__ejmq = ', '.join(['recv_arrs[{}][i]'.format(wjgy__xew) for
                wjgy__xew in range(iftij__oopbv + redvar_offsets[0], 
                iftij__oopbv + redvar_offsets[1])])
            gwlz__zrld += '  {} = combine_vars_0({}, {})\n'.format(tbr__xbwrp,
                tbr__xbwrp, wgnvm__ejmq)
    else:
        for kzyzg__xpfa in range(hyqyl__yjpmx):
            tbr__xbwrp = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                wjgy__xew) for wjgy__xew in range(redvar_offsets[
                kzyzg__xpfa], redvar_offsets[kzyzg__xpfa + 1])])
            wgnvm__ejmq = ', '.join(['recv_arrs[{}][i]'.format(wjgy__xew) for
                wjgy__xew in range(redvar_offsets[kzyzg__xpfa],
                redvar_offsets[kzyzg__xpfa + 1])])
            if wgnvm__ejmq:
                gwlz__zrld += '  {} = combine_vars_{}({}, {})\n'.format(
                    tbr__xbwrp, kzyzg__xpfa, tbr__xbwrp, wgnvm__ejmq)
    gwlz__zrld += '  return\n'
    gazvi__afz = {}
    for wjgy__xew, yicj__pdur in enumerate(combine_funcs):
        gazvi__afz['combine_vars_{}'.format(wjgy__xew)] = yicj__pdur
    qajgj__irv = {}
    exec(gwlz__zrld, gazvi__afz, qajgj__irv)
    aob__bllpr = qajgj__irv['combine_all_f']
    f_ir = compile_to_numba_ir(aob__bllpr, gazvi__afz)
    jdw__djqmg = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    zwweb__gzhdx = numba.core.target_extension.dispatcher_registry[cpu_target](
        aob__bllpr)
    zwweb__gzhdx.add_overload(jdw__djqmg)
    return zwweb__gzhdx


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    vphke__wgibw = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    hyqyl__yjpmx = len(redvar_offsets) - 1
    nkdf__nme = redvar_offsets[hyqyl__yjpmx]
    gwlz__zrld = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert hyqyl__yjpmx == 1
        for kzyzg__xpfa in range(len(pivot_values)):
            iftij__oopbv = nkdf__nme * kzyzg__xpfa
            tbr__xbwrp = ', '.join(['redvar_arrs[{}][j]'.format(wjgy__xew) for
                wjgy__xew in range(iftij__oopbv + redvar_offsets[0], 
                iftij__oopbv + redvar_offsets[1])])
            gwlz__zrld += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                kzyzg__xpfa, tbr__xbwrp)
    else:
        for kzyzg__xpfa in range(hyqyl__yjpmx):
            tbr__xbwrp = ', '.join(['redvar_arrs[{}][j]'.format(wjgy__xew) for
                wjgy__xew in range(redvar_offsets[kzyzg__xpfa],
                redvar_offsets[kzyzg__xpfa + 1])])
            gwlz__zrld += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                kzyzg__xpfa, kzyzg__xpfa, tbr__xbwrp)
    gwlz__zrld += '  return\n'
    gazvi__afz = {}
    for wjgy__xew, yicj__pdur in enumerate(eval_funcs):
        gazvi__afz['eval_vars_{}'.format(wjgy__xew)] = yicj__pdur
    qajgj__irv = {}
    exec(gwlz__zrld, gazvi__afz, qajgj__irv)
    fnwfy__ryhee = qajgj__irv['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(fnwfy__ryhee)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    szyli__vlcwr = len(var_types)
    gmnyn__vads = [f'in{wjgy__xew}' for wjgy__xew in range(szyli__vlcwr)]
    wfd__gbtt = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    xdr__wcf = wfd__gbtt(0)
    gwlz__zrld = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        gmnyn__vads))
    qajgj__irv = {}
    exec(gwlz__zrld, {'_zero': xdr__wcf}, qajgj__irv)
    xaz__zdv = qajgj__irv['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(xaz__zdv, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': xdr__wcf}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    gwzwd__oxh = []
    for wjgy__xew, gefl__jivqw in enumerate(reduce_vars):
        gwzwd__oxh.append(ir.Assign(block.body[wjgy__xew].target,
            gefl__jivqw, gefl__jivqw.loc))
        for nmx__nbhf in gefl__jivqw.versioned_names:
            gwzwd__oxh.append(ir.Assign(gefl__jivqw, ir.Var(gefl__jivqw.
                scope, nmx__nbhf, gefl__jivqw.loc), gefl__jivqw.loc))
    block.body = block.body[:szyli__vlcwr] + gwzwd__oxh + eval_nodes
    pmeo__qxrsf = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        wfd__gbtt, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    zwweb__gzhdx = numba.core.target_extension.dispatcher_registry[cpu_target](
        xaz__zdv)
    zwweb__gzhdx.add_overload(pmeo__qxrsf)
    return zwweb__gzhdx


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    szyli__vlcwr = len(redvars)
    mfs__edt = [f'v{wjgy__xew}' for wjgy__xew in range(szyli__vlcwr)]
    gmnyn__vads = [f'in{wjgy__xew}' for wjgy__xew in range(szyli__vlcwr)]
    gwlz__zrld = 'def agg_combine({}):\n'.format(', '.join(mfs__edt +
        gmnyn__vads))
    fhq__debf = wrap_parfor_blocks(parfor)
    vjy__igmr = find_topo_order(fhq__debf)
    vjy__igmr = vjy__igmr[1:]
    unwrap_parfor_blocks(parfor)
    lryes__muscq = {}
    hbcnq__kxl = []
    for mmuj__tevs in vjy__igmr:
        vdwut__qiy = parfor.loop_body[mmuj__tevs]
        for akg__lqg in vdwut__qiy.body:
            if is_call_assign(akg__lqg) and guard(find_callname, f_ir,
                akg__lqg.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = akg__lqg.value.args
                dbn__pel = []
                vtrzv__zsfy = []
                for gefl__jivqw in args[:-1]:
                    ind = redvars.index(gefl__jivqw.name)
                    hbcnq__kxl.append(ind)
                    dbn__pel.append('v{}'.format(ind))
                    vtrzv__zsfy.append('in{}'.format(ind))
                qioml__cyxz = '__special_combine__{}'.format(len(lryes__muscq))
                gwlz__zrld += '    ({},) = {}({})\n'.format(', '.join(
                    dbn__pel), qioml__cyxz, ', '.join(dbn__pel + vtrzv__zsfy))
                dhcsl__vnd = ir.Expr.call(args[-1], [], (), vdwut__qiy.loc)
                iqou__iyb = guard(find_callname, f_ir, dhcsl__vnd)
                assert iqou__iyb == ('_var_combine', 'bodo.ir.aggregate')
                iqou__iyb = bodo.ir.aggregate._var_combine
                lryes__muscq[qioml__cyxz] = iqou__iyb
            if is_assign(akg__lqg) and akg__lqg.target.name in redvars:
                lzhn__khkm = akg__lqg.target.name
                ind = redvars.index(lzhn__khkm)
                if ind in hbcnq__kxl:
                    continue
                if len(f_ir._definitions[lzhn__khkm]) == 2:
                    var_def = f_ir._definitions[lzhn__khkm][0]
                    gwlz__zrld += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[lzhn__khkm][1]
                    gwlz__zrld += _match_reduce_def(var_def, f_ir, ind)
    gwlz__zrld += '    return {}'.format(', '.join(['v{}'.format(wjgy__xew) for
        wjgy__xew in range(szyli__vlcwr)]))
    qajgj__irv = {}
    exec(gwlz__zrld, {}, qajgj__irv)
    zkdal__xfyk = qajgj__irv['agg_combine']
    arg_typs = tuple(2 * var_types)
    gazvi__afz = {'numba': numba, 'bodo': bodo, 'np': np}
    gazvi__afz.update(lryes__muscq)
    f_ir = compile_to_numba_ir(zkdal__xfyk, gazvi__afz, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    wfd__gbtt = pm.typemap[block.body[-1].value.name]
    kyjou__gwf = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        wfd__gbtt, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    zwweb__gzhdx = numba.core.target_extension.dispatcher_registry[cpu_target](
        zkdal__xfyk)
    zwweb__gzhdx.add_overload(kyjou__gwf)
    return zwweb__gzhdx


def _match_reduce_def(var_def, f_ir, ind):
    gwlz__zrld = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        gwlz__zrld = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        xxh__vtdn = guard(find_callname, f_ir, var_def)
        if xxh__vtdn == ('min', 'builtins'):
            gwlz__zrld = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if xxh__vtdn == ('max', 'builtins'):
            gwlz__zrld = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return gwlz__zrld


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    szyli__vlcwr = len(redvars)
    vdkno__whzyu = 1
    hsr__igw = []
    for wjgy__xew in range(vdkno__whzyu):
        duu__uiwk = ir.Var(arr_var.scope, f'$input{wjgy__xew}', arr_var.loc)
        hsr__igw.append(duu__uiwk)
    ifbt__qbivz = parfor.loop_nests[0].index_variable
    olpsh__siatw = [0] * szyli__vlcwr
    for vdwut__qiy in parfor.loop_body.values():
        mpebg__bqs = []
        for akg__lqg in vdwut__qiy.body:
            if is_var_assign(akg__lqg
                ) and akg__lqg.value.name == ifbt__qbivz.name:
                continue
            if is_getitem(akg__lqg
                ) and akg__lqg.value.value.name == arr_var.name:
                akg__lqg.value = hsr__igw[0]
            if is_call_assign(akg__lqg) and guard(find_callname, pm.func_ir,
                akg__lqg.value) == ('isna', 'bodo.libs.array_kernels'
                ) and akg__lqg.value.args[0].name == arr_var.name:
                akg__lqg.value = ir.Const(False, akg__lqg.target.loc)
            if is_assign(akg__lqg) and akg__lqg.target.name in redvars:
                ind = redvars.index(akg__lqg.target.name)
                olpsh__siatw[ind] = akg__lqg.target
            mpebg__bqs.append(akg__lqg)
        vdwut__qiy.body = mpebg__bqs
    mfs__edt = ['v{}'.format(wjgy__xew) for wjgy__xew in range(szyli__vlcwr)]
    gmnyn__vads = ['in{}'.format(wjgy__xew) for wjgy__xew in range(
        vdkno__whzyu)]
    gwlz__zrld = 'def agg_update({}):\n'.format(', '.join(mfs__edt +
        gmnyn__vads))
    gwlz__zrld += '    __update_redvars()\n'
    gwlz__zrld += '    return {}'.format(', '.join(['v{}'.format(wjgy__xew) for
        wjgy__xew in range(szyli__vlcwr)]))
    qajgj__irv = {}
    exec(gwlz__zrld, {}, qajgj__irv)
    yli__kdqpb = qajgj__irv['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * vdkno__whzyu)
    f_ir = compile_to_numba_ir(yli__kdqpb, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    uvtp__vyze = f_ir.blocks.popitem()[1].body
    wfd__gbtt = pm.typemap[uvtp__vyze[-1].value.name]
    fhq__debf = wrap_parfor_blocks(parfor)
    vjy__igmr = find_topo_order(fhq__debf)
    vjy__igmr = vjy__igmr[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    qmuod__gxkda = f_ir.blocks[vjy__igmr[0]]
    rzemm__wegua = f_ir.blocks[vjy__igmr[-1]]
    epr__nho = uvtp__vyze[:szyli__vlcwr + vdkno__whzyu]
    if szyli__vlcwr > 1:
        wthau__yjzdi = uvtp__vyze[-3:]
        assert is_assign(wthau__yjzdi[0]) and isinstance(wthau__yjzdi[0].
            value, ir.Expr) and wthau__yjzdi[0].value.op == 'build_tuple'
    else:
        wthau__yjzdi = uvtp__vyze[-2:]
    for wjgy__xew in range(szyli__vlcwr):
        ockc__wct = uvtp__vyze[wjgy__xew].target
        fni__vfgif = ir.Assign(ockc__wct, olpsh__siatw[wjgy__xew],
            ockc__wct.loc)
        epr__nho.append(fni__vfgif)
    for wjgy__xew in range(szyli__vlcwr, szyli__vlcwr + vdkno__whzyu):
        ockc__wct = uvtp__vyze[wjgy__xew].target
        fni__vfgif = ir.Assign(ockc__wct, hsr__igw[wjgy__xew - szyli__vlcwr
            ], ockc__wct.loc)
        epr__nho.append(fni__vfgif)
    qmuod__gxkda.body = epr__nho + qmuod__gxkda.body
    tnl__pqw = []
    for wjgy__xew in range(szyli__vlcwr):
        ockc__wct = uvtp__vyze[wjgy__xew].target
        fni__vfgif = ir.Assign(olpsh__siatw[wjgy__xew], ockc__wct,
            ockc__wct.loc)
        tnl__pqw.append(fni__vfgif)
    rzemm__wegua.body += tnl__pqw + wthau__yjzdi
    tcn__nakna = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        wfd__gbtt, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    zwweb__gzhdx = numba.core.target_extension.dispatcher_registry[cpu_target](
        yli__kdqpb)
    zwweb__gzhdx.add_overload(tcn__nakna)
    return zwweb__gzhdx


def _rm_arg_agg_block(block, typemap):
    cvbq__use = []
    arr_var = None
    for wjgy__xew, akg__lqg in enumerate(block.body):
        if is_assign(akg__lqg) and isinstance(akg__lqg.value, ir.Arg):
            arr_var = akg__lqg.target
            uktwg__kwixc = typemap[arr_var.name]
            if not isinstance(uktwg__kwixc, types.ArrayCompatible):
                cvbq__use += block.body[wjgy__xew + 1:]
                break
            rmqr__mjlg = block.body[wjgy__xew + 1]
            assert is_assign(rmqr__mjlg) and isinstance(rmqr__mjlg.value,
                ir.Expr
                ) and rmqr__mjlg.value.op == 'getattr' and rmqr__mjlg.value.attr == 'shape' and rmqr__mjlg.value.value.name == arr_var.name
            nuwv__dure = rmqr__mjlg.target
            zjqdb__kmgdz = block.body[wjgy__xew + 2]
            assert is_assign(zjqdb__kmgdz) and isinstance(zjqdb__kmgdz.
                value, ir.Expr
                ) and zjqdb__kmgdz.value.op == 'static_getitem' and zjqdb__kmgdz.value.value.name == nuwv__dure.name
            cvbq__use += block.body[wjgy__xew + 3:]
            break
        cvbq__use.append(akg__lqg)
    return cvbq__use, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    fhq__debf = wrap_parfor_blocks(parfor)
    vjy__igmr = find_topo_order(fhq__debf)
    vjy__igmr = vjy__igmr[1:]
    unwrap_parfor_blocks(parfor)
    for mmuj__tevs in reversed(vjy__igmr):
        for akg__lqg in reversed(parfor.loop_body[mmuj__tevs].body):
            if isinstance(akg__lqg, ir.Assign) and (akg__lqg.target.name in
                parfor_params or akg__lqg.target.name in var_to_param):
                vyax__zfkjd = akg__lqg.target.name
                rhs = akg__lqg.value
                repvp__snd = (vyax__zfkjd if vyax__zfkjd in parfor_params else
                    var_to_param[vyax__zfkjd])
                blb__nnzsf = []
                if isinstance(rhs, ir.Var):
                    blb__nnzsf = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    blb__nnzsf = [gefl__jivqw.name for gefl__jivqw in
                        akg__lqg.value.list_vars()]
                param_uses[repvp__snd].extend(blb__nnzsf)
                for gefl__jivqw in blb__nnzsf:
                    var_to_param[gefl__jivqw] = repvp__snd
            if isinstance(akg__lqg, Parfor):
                get_parfor_reductions(akg__lqg, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for hwmma__dtat, blb__nnzsf in param_uses.items():
        if hwmma__dtat in blb__nnzsf and hwmma__dtat not in reduce_varnames:
            reduce_varnames.append(hwmma__dtat)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
