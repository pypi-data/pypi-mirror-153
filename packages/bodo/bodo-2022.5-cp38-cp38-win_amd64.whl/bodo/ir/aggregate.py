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
            fvjbz__jaxay = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer()])
            qmafp__inb = cgutils.get_or_insert_function(builder.module,
                fvjbz__jaxay, sym._literal_value)
            builder.call(qmafp__inb, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            fvjbz__jaxay = lir.FunctionType(lir.VoidType(), [lir.IntType(64
                ), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            qmafp__inb = cgutils.get_or_insert_function(builder.module,
                fvjbz__jaxay, sym._literal_value)
            builder.call(qmafp__inb, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            fvjbz__jaxay = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)
                .as_pointer()])
            qmafp__inb = cgutils.get_or_insert_function(builder.module,
                fvjbz__jaxay, sym._literal_value)
            builder.call(qmafp__inb, [context.get_constant_null(sig.args[0]
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
        zuwir__epza = True
        hale__xjnvx = 1
        jlvt__gwwi = -1
        if isinstance(rhs, ir.Expr):
            for opt__hyx in rhs.kws:
                if func_name in list_cumulative:
                    if opt__hyx[0] == 'skipna':
                        zuwir__epza = guard(find_const, func_ir, opt__hyx[1])
                        if not isinstance(zuwir__epza, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if opt__hyx[0] == 'dropna':
                        zuwir__epza = guard(find_const, func_ir, opt__hyx[1])
                        if not isinstance(zuwir__epza, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            hale__xjnvx = get_call_expr_arg('shift', rhs.args, dict(rhs.kws
                ), 0, 'periods', hale__xjnvx)
            hale__xjnvx = guard(find_const, func_ir, hale__xjnvx)
        if func_name == 'head':
            jlvt__gwwi = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(jlvt__gwwi, int):
                jlvt__gwwi = guard(find_const, func_ir, jlvt__gwwi)
            if jlvt__gwwi < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = zuwir__epza
        func.periods = hale__xjnvx
        func.head_n = jlvt__gwwi
        if func_name == 'transform':
            kws = dict(rhs.kws)
            ojp__bcwx = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            fxf__mbav = typemap[ojp__bcwx.name]
            vyjj__fay = None
            if isinstance(fxf__mbav, str):
                vyjj__fay = fxf__mbav
            elif is_overload_constant_str(fxf__mbav):
                vyjj__fay = get_overload_const_str(fxf__mbav)
            elif bodo.utils.typing.is_builtin_function(fxf__mbav):
                vyjj__fay = bodo.utils.typing.get_builtin_function_name(
                    fxf__mbav)
            if vyjj__fay not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {vyjj__fay}')
            func.transform_func = supported_agg_funcs.index(vyjj__fay)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    ojp__bcwx = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if ojp__bcwx == '':
        fxf__mbav = types.none
    else:
        fxf__mbav = typemap[ojp__bcwx.name]
    if is_overload_constant_dict(fxf__mbav):
        ewil__oyq = get_overload_constant_dict(fxf__mbav)
        fspd__vmer = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in ewil__oyq.values()]
        return fspd__vmer
    if fxf__mbav == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(fxf__mbav, types.BaseTuple) or is_overload_constant_list(
        fxf__mbav):
        fspd__vmer = []
        ghg__jnbf = 0
        if is_overload_constant_list(fxf__mbav):
            mvp__ipk = get_overload_const_list(fxf__mbav)
        else:
            mvp__ipk = fxf__mbav.types
        for t in mvp__ipk:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                fspd__vmer.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(mvp__ipk) > 1:
                    func.fname = '<lambda_' + str(ghg__jnbf) + '>'
                    ghg__jnbf += 1
                fspd__vmer.append(func)
        return [fspd__vmer]
    if is_overload_constant_str(fxf__mbav):
        func_name = get_overload_const_str(fxf__mbav)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(fxf__mbav):
        func_name = bodo.utils.typing.get_builtin_function_name(fxf__mbav)
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
        ghg__jnbf = 0
        uiuh__xludq = []
        for ogt__ykgo in f_val:
            func = get_agg_func_udf(func_ir, ogt__ykgo, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{ghg__jnbf}>'
                ghg__jnbf += 1
            uiuh__xludq.append(func)
        return uiuh__xludq
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
    vyjj__fay = code.co_name
    return vyjj__fay


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
            ziiq__cotn = types.DType(args[0])
            return signature(ziiq__cotn, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    mpdwt__zck = nobs_a + nobs_b
    cxerc__uvtsg = (nobs_a * mean_a + nobs_b * mean_b) / mpdwt__zck
    bgmul__jzib = mean_b - mean_a
    isu__hzzye = (ssqdm_a + ssqdm_b + bgmul__jzib * bgmul__jzib * nobs_a *
        nobs_b / mpdwt__zck)
    return isu__hzzye, cxerc__uvtsg, mpdwt__zck


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
        ohs__rzfl = ''
        for mqj__ddit, uko__ydos in self.df_out_vars.items():
            ohs__rzfl += "'{}':{}, ".format(mqj__ddit, uko__ydos.name)
        dxa__ggkdz = '{}{{{}}}'.format(self.df_out, ohs__rzfl)
        ngst__zmr = ''
        for mqj__ddit, uko__ydos in self.df_in_vars.items():
            ngst__zmr += "'{}':{}, ".format(mqj__ddit, uko__ydos.name)
        warai__fmh = '{}{{{}}}'.format(self.df_in, ngst__zmr)
        tas__czun = 'pivot {}:{}'.format(self.pivot_arr.name, self.pivot_values
            ) if self.pivot_arr is not None else ''
        key_names = ','.join([str(zgp__azjo) for zgp__azjo in self.key_names])
        whxjo__fzt = ','.join([uko__ydos.name for uko__ydos in self.key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(dxa__ggkdz,
            warai__fmh, key_names, whxjo__fzt, tas__czun)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        uxc__jhj, kxh__ukssb = self.gb_info_out.pop(out_col_name)
        if uxc__jhj is None and not self.is_crosstab:
            return
        atne__euzw = self.gb_info_in[uxc__jhj]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for qaga__vnkh, (func, ohs__rzfl) in enumerate(atne__euzw):
                try:
                    ohs__rzfl.remove(out_col_name)
                    if len(ohs__rzfl) == 0:
                        atne__euzw.pop(qaga__vnkh)
                        break
                except ValueError as lbfe__fjxrh:
                    continue
        else:
            for qaga__vnkh, (func, ufg__amd) in enumerate(atne__euzw):
                if ufg__amd == out_col_name:
                    atne__euzw.pop(qaga__vnkh)
                    break
        if len(atne__euzw) == 0:
            self.gb_info_in.pop(uxc__jhj)
            self.df_in_vars.pop(uxc__jhj)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({uko__ydos.name for uko__ydos in aggregate_node.key_arrs})
    use_set.update({uko__ydos.name for uko__ydos in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({uko__ydos.name for uko__ydos in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({uko__ydos.name for uko__ydos in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    meu__oaxm = [mgmrj__bym for mgmrj__bym, dkdng__pvwp in aggregate_node.
        df_out_vars.items() if dkdng__pvwp.name not in lives]
    for pyjs__lfk in meu__oaxm:
        aggregate_node.remove_out_col(pyjs__lfk)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(uko__ydos.name not in lives for
        uko__ydos in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    edj__lib = set(uko__ydos.name for uko__ydos in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        edj__lib.update({uko__ydos.name for uko__ydos in aggregate_node.
            out_key_vars})
    return set(), edj__lib


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for qaga__vnkh in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[qaga__vnkh] = replace_vars_inner(aggregate_node
            .key_arrs[qaga__vnkh], var_dict)
    for mgmrj__bym in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[mgmrj__bym] = replace_vars_inner(
            aggregate_node.df_in_vars[mgmrj__bym], var_dict)
    for mgmrj__bym in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[mgmrj__bym] = replace_vars_inner(
            aggregate_node.df_out_vars[mgmrj__bym], var_dict)
    if aggregate_node.out_key_vars is not None:
        for qaga__vnkh in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[qaga__vnkh] = replace_vars_inner(
                aggregate_node.out_key_vars[qaga__vnkh], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for qaga__vnkh in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[qaga__vnkh] = visit_vars_inner(aggregate_node
            .key_arrs[qaga__vnkh], callback, cbdata)
    for mgmrj__bym in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[mgmrj__bym] = visit_vars_inner(aggregate_node
            .df_in_vars[mgmrj__bym], callback, cbdata)
    for mgmrj__bym in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[mgmrj__bym] = visit_vars_inner(
            aggregate_node.df_out_vars[mgmrj__bym], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for qaga__vnkh in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[qaga__vnkh] = visit_vars_inner(
                aggregate_node.out_key_vars[qaga__vnkh], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    gwgx__gvsu = []
    for dojia__itrp in aggregate_node.key_arrs:
        sdn__hcavv = equiv_set.get_shape(dojia__itrp)
        if sdn__hcavv:
            gwgx__gvsu.append(sdn__hcavv[0])
    if aggregate_node.pivot_arr is not None:
        sdn__hcavv = equiv_set.get_shape(aggregate_node.pivot_arr)
        if sdn__hcavv:
            gwgx__gvsu.append(sdn__hcavv[0])
    for dkdng__pvwp in aggregate_node.df_in_vars.values():
        sdn__hcavv = equiv_set.get_shape(dkdng__pvwp)
        if sdn__hcavv:
            gwgx__gvsu.append(sdn__hcavv[0])
    if len(gwgx__gvsu) > 1:
        equiv_set.insert_equiv(*gwgx__gvsu)
    oaoiu__eud = []
    gwgx__gvsu = []
    omt__kjam = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        omt__kjam.extend(aggregate_node.out_key_vars)
    for dkdng__pvwp in omt__kjam:
        hhk__mou = typemap[dkdng__pvwp.name]
        sdcyt__idcvv = array_analysis._gen_shape_call(equiv_set,
            dkdng__pvwp, hhk__mou.ndim, None, oaoiu__eud)
        equiv_set.insert_equiv(dkdng__pvwp, sdcyt__idcvv)
        gwgx__gvsu.append(sdcyt__idcvv[0])
        equiv_set.define(dkdng__pvwp, set())
    if len(gwgx__gvsu) > 1:
        equiv_set.insert_equiv(*gwgx__gvsu)
    return [], oaoiu__eud


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    jhw__iqqu = Distribution.OneD
    for dkdng__pvwp in aggregate_node.df_in_vars.values():
        jhw__iqqu = Distribution(min(jhw__iqqu.value, array_dists[
            dkdng__pvwp.name].value))
    for dojia__itrp in aggregate_node.key_arrs:
        jhw__iqqu = Distribution(min(jhw__iqqu.value, array_dists[
            dojia__itrp.name].value))
    if aggregate_node.pivot_arr is not None:
        jhw__iqqu = Distribution(min(jhw__iqqu.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = jhw__iqqu
    for dkdng__pvwp in aggregate_node.df_in_vars.values():
        array_dists[dkdng__pvwp.name] = jhw__iqqu
    for dojia__itrp in aggregate_node.key_arrs:
        array_dists[dojia__itrp.name] = jhw__iqqu
    xhgok__bmf = Distribution.OneD_Var
    for dkdng__pvwp in aggregate_node.df_out_vars.values():
        if dkdng__pvwp.name in array_dists:
            xhgok__bmf = Distribution(min(xhgok__bmf.value, array_dists[
                dkdng__pvwp.name].value))
    if aggregate_node.out_key_vars is not None:
        for dkdng__pvwp in aggregate_node.out_key_vars:
            if dkdng__pvwp.name in array_dists:
                xhgok__bmf = Distribution(min(xhgok__bmf.value, array_dists
                    [dkdng__pvwp.name].value))
    xhgok__bmf = Distribution(min(xhgok__bmf.value, jhw__iqqu.value))
    for dkdng__pvwp in aggregate_node.df_out_vars.values():
        array_dists[dkdng__pvwp.name] = xhgok__bmf
    if aggregate_node.out_key_vars is not None:
        for ndxub__gaba in aggregate_node.out_key_vars:
            array_dists[ndxub__gaba.name] = xhgok__bmf
    if xhgok__bmf != Distribution.OneD_Var:
        for dojia__itrp in aggregate_node.key_arrs:
            array_dists[dojia__itrp.name] = xhgok__bmf
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = xhgok__bmf
        for dkdng__pvwp in aggregate_node.df_in_vars.values():
            array_dists[dkdng__pvwp.name] = xhgok__bmf


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for dkdng__pvwp in agg_node.df_out_vars.values():
        definitions[dkdng__pvwp.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for ndxub__gaba in agg_node.out_key_vars:
            definitions[ndxub__gaba.name].append(agg_node)
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
        for uko__ydos in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[uko__ydos.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                uko__ydos.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    fqnh__efs = tuple(typemap[uko__ydos.name] for uko__ydos in agg_node.
        key_arrs)
    pqv__rtmzv = [uko__ydos for fgo__tyxjr, uko__ydos in agg_node.
        df_in_vars.items()]
    gvw__mmj = [uko__ydos for fgo__tyxjr, uko__ydos in agg_node.df_out_vars
        .items()]
    in_col_typs = []
    fspd__vmer = []
    if agg_node.pivot_arr is not None:
        for uxc__jhj, atne__euzw in agg_node.gb_info_in.items():
            for func, kxh__ukssb in atne__euzw:
                if uxc__jhj is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[uxc__jhj
                        ].name])
                fspd__vmer.append(func)
    else:
        for uxc__jhj, func in agg_node.gb_info_out.values():
            if uxc__jhj is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[uxc__jhj].name])
            fspd__vmer.append(func)
    out_col_typs = tuple(typemap[uko__ydos.name] for uko__ydos in gvw__mmj)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(fqnh__efs + tuple(typemap[uko__ydos.name] for
        uko__ydos in pqv__rtmzv) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    tyqx__gfp = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for qaga__vnkh, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            tyqx__gfp.update({f'in_cat_dtype_{qaga__vnkh}': in_col_typ})
    for qaga__vnkh, ldko__dktoi in enumerate(out_col_typs):
        if isinstance(ldko__dktoi, bodo.CategoricalArrayType):
            tyqx__gfp.update({f'out_cat_dtype_{qaga__vnkh}': ldko__dktoi})
    udf_func_struct = get_udf_func_struct(fspd__vmer, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    ehhlb__esk = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    tyqx__gfp.update({'pd': pd, 'pre_alloc_string_array':
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
            tyqx__gfp.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            tyqx__gfp.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    ljcx__qxk = compile_to_numba_ir(ehhlb__esk, tyqx__gfp, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    fol__knkpb = []
    if agg_node.pivot_arr is None:
        rqkk__jnwky = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        xhhbv__dxee = ir.Var(rqkk__jnwky, mk_unique_var('dummy_none'), loc)
        typemap[xhhbv__dxee.name] = types.none
        fol__knkpb.append(ir.Assign(ir.Const(None, loc), xhhbv__dxee, loc))
        pqv__rtmzv.append(xhhbv__dxee)
    else:
        pqv__rtmzv.append(agg_node.pivot_arr)
    replace_arg_nodes(ljcx__qxk, agg_node.key_arrs + pqv__rtmzv)
    xps__orjix = ljcx__qxk.body[-3]
    assert is_assign(xps__orjix) and isinstance(xps__orjix.value, ir.Expr
        ) and xps__orjix.value.op == 'build_tuple'
    fol__knkpb += ljcx__qxk.body[:-3]
    omt__kjam = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        omt__kjam += agg_node.out_key_vars
    for qaga__vnkh, bcwt__gyh in enumerate(omt__kjam):
        jhjdz__uyi = xps__orjix.value.items[qaga__vnkh]
        fol__knkpb.append(ir.Assign(jhjdz__uyi, bcwt__gyh, bcwt__gyh.loc))
    return fol__knkpb


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        lntm__imp = args[0]
        dtype = types.Tuple([t.dtype for t in lntm__imp.types]) if isinstance(
            lntm__imp, types.BaseTuple) else lntm__imp.dtype
        if isinstance(lntm__imp, types.BaseTuple) and len(lntm__imp.types
            ) == 1:
            dtype = lntm__imp.types[0].dtype
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
        sdcw__vssq = args[0]
        if sdcw__vssq == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    duu__cmabo = context.compile_internal(builder, lambda a: False, sig, args)
    return duu__cmabo


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        qveqi__oqa = IntDtype(t.dtype).name
        assert qveqi__oqa.endswith('Dtype()')
        qveqi__oqa = qveqi__oqa[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{qveqi__oqa}'))"
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
        nrjd__iitcn = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {nrjd__iitcn}_cat_dtype_{colnum})'
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
    teet__bug = udf_func_struct.var_typs
    hfpr__rtx = len(teet__bug)
    mhj__ffgrf = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    mhj__ffgrf += '    if is_null_pointer(in_table):\n'
    mhj__ffgrf += '        return\n'
    mhj__ffgrf += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in teet__bug]), 
        ',' if len(teet__bug) == 1 else '')
    tdpl__ujjr = n_keys
    wbhiz__muj = []
    redvar_offsets = []
    mrpbo__eocjr = []
    if do_combine:
        for qaga__vnkh, ogt__ykgo in enumerate(allfuncs):
            if ogt__ykgo.ftype != 'udf':
                tdpl__ujjr += ogt__ykgo.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(tdpl__ujjr, tdpl__ujjr +
                    ogt__ykgo.n_redvars))
                tdpl__ujjr += ogt__ykgo.n_redvars
                mrpbo__eocjr.append(data_in_typs_[func_idx_to_in_col[
                    qaga__vnkh]])
                wbhiz__muj.append(func_idx_to_in_col[qaga__vnkh] + n_keys)
    else:
        for qaga__vnkh, ogt__ykgo in enumerate(allfuncs):
            if ogt__ykgo.ftype != 'udf':
                tdpl__ujjr += ogt__ykgo.ncols_post_shuffle
            else:
                redvar_offsets += list(range(tdpl__ujjr + 1, tdpl__ujjr + 1 +
                    ogt__ykgo.n_redvars))
                tdpl__ujjr += ogt__ykgo.n_redvars + 1
                mrpbo__eocjr.append(data_in_typs_[func_idx_to_in_col[
                    qaga__vnkh]])
                wbhiz__muj.append(func_idx_to_in_col[qaga__vnkh] + n_keys)
    assert len(redvar_offsets) == hfpr__rtx
    ugn__kwn = len(mrpbo__eocjr)
    mbok__ovg = []
    for qaga__vnkh, t in enumerate(mrpbo__eocjr):
        mbok__ovg.append(_gen_dummy_alloc(t, qaga__vnkh, True))
    mhj__ffgrf += '    data_in_dummy = ({}{})\n'.format(','.join(mbok__ovg),
        ',' if len(mrpbo__eocjr) == 1 else '')
    mhj__ffgrf += """
    # initialize redvar cols
"""
    mhj__ffgrf += '    init_vals = __init_func()\n'
    for qaga__vnkh in range(hfpr__rtx):
        mhj__ffgrf += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(qaga__vnkh, redvar_offsets[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(redvar_arr_{})\n'.format(qaga__vnkh)
        mhj__ffgrf += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            qaga__vnkh, qaga__vnkh)
    mhj__ffgrf += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(qaga__vnkh) for qaga__vnkh in range(hfpr__rtx)]), ',' if 
        hfpr__rtx == 1 else '')
    mhj__ffgrf += '\n'
    for qaga__vnkh in range(ugn__kwn):
        mhj__ffgrf += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(qaga__vnkh, wbhiz__muj[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(data_in_{})\n'.format(qaga__vnkh)
    mhj__ffgrf += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(qaga__vnkh) for qaga__vnkh in range(ugn__kwn)]), ',' if 
        ugn__kwn == 1 else '')
    mhj__ffgrf += '\n'
    mhj__ffgrf += '    for i in range(len(data_in_0)):\n'
    mhj__ffgrf += '        w_ind = row_to_group[i]\n'
    mhj__ffgrf += '        if w_ind != -1:\n'
    mhj__ffgrf += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, bdkc__oxlla)
    return bdkc__oxlla['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    teet__bug = udf_func_struct.var_typs
    hfpr__rtx = len(teet__bug)
    mhj__ffgrf = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    mhj__ffgrf += '    if is_null_pointer(in_table):\n'
    mhj__ffgrf += '        return\n'
    mhj__ffgrf += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in teet__bug]), 
        ',' if len(teet__bug) == 1 else '')
    njei__jrl = n_keys
    jed__eeyo = n_keys
    mkk__wry = []
    dwvoy__jrb = []
    for ogt__ykgo in allfuncs:
        if ogt__ykgo.ftype != 'udf':
            njei__jrl += ogt__ykgo.ncols_pre_shuffle
            jed__eeyo += ogt__ykgo.ncols_post_shuffle
        else:
            mkk__wry += list(range(njei__jrl, njei__jrl + ogt__ykgo.n_redvars))
            dwvoy__jrb += list(range(jed__eeyo + 1, jed__eeyo + 1 +
                ogt__ykgo.n_redvars))
            njei__jrl += ogt__ykgo.n_redvars
            jed__eeyo += 1 + ogt__ykgo.n_redvars
    assert len(mkk__wry) == hfpr__rtx
    mhj__ffgrf += """
    # initialize redvar cols
"""
    mhj__ffgrf += '    init_vals = __init_func()\n'
    for qaga__vnkh in range(hfpr__rtx):
        mhj__ffgrf += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(qaga__vnkh, dwvoy__jrb[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(redvar_arr_{})\n'.format(qaga__vnkh)
        mhj__ffgrf += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            qaga__vnkh, qaga__vnkh)
    mhj__ffgrf += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(qaga__vnkh) for qaga__vnkh in range(hfpr__rtx)]), ',' if 
        hfpr__rtx == 1 else '')
    mhj__ffgrf += '\n'
    for qaga__vnkh in range(hfpr__rtx):
        mhj__ffgrf += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(qaga__vnkh, mkk__wry[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(recv_redvar_arr_{})\n'.format(qaga__vnkh)
    mhj__ffgrf += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(qaga__vnkh) for qaga__vnkh in range(
        hfpr__rtx)]), ',' if hfpr__rtx == 1 else '')
    mhj__ffgrf += '\n'
    if hfpr__rtx:
        mhj__ffgrf += '    for i in range(len(recv_redvar_arr_0)):\n'
        mhj__ffgrf += '        w_ind = row_to_group[i]\n'
        mhj__ffgrf += """        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)
"""
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, bdkc__oxlla)
    return bdkc__oxlla['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    teet__bug = udf_func_struct.var_typs
    hfpr__rtx = len(teet__bug)
    tdpl__ujjr = n_keys
    redvar_offsets = []
    hpek__mkzws = []
    out_data_typs = []
    for qaga__vnkh, ogt__ykgo in enumerate(allfuncs):
        if ogt__ykgo.ftype != 'udf':
            tdpl__ujjr += ogt__ykgo.ncols_post_shuffle
        else:
            hpek__mkzws.append(tdpl__ujjr)
            redvar_offsets += list(range(tdpl__ujjr + 1, tdpl__ujjr + 1 +
                ogt__ykgo.n_redvars))
            tdpl__ujjr += 1 + ogt__ykgo.n_redvars
            out_data_typs.append(out_data_typs_[qaga__vnkh])
    assert len(redvar_offsets) == hfpr__rtx
    ugn__kwn = len(out_data_typs)
    mhj__ffgrf = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    mhj__ffgrf += '    if is_null_pointer(table):\n'
    mhj__ffgrf += '        return\n'
    mhj__ffgrf += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in teet__bug]), 
        ',' if len(teet__bug) == 1 else '')
    mhj__ffgrf += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for qaga__vnkh in range(hfpr__rtx):
        mhj__ffgrf += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(qaga__vnkh, redvar_offsets[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(redvar_arr_{})\n'.format(qaga__vnkh)
    mhj__ffgrf += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(qaga__vnkh) for qaga__vnkh in range(hfpr__rtx)]), ',' if 
        hfpr__rtx == 1 else '')
    mhj__ffgrf += '\n'
    for qaga__vnkh in range(ugn__kwn):
        mhj__ffgrf += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(qaga__vnkh, hpek__mkzws[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(data_out_{})\n'.format(qaga__vnkh)
    mhj__ffgrf += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(qaga__vnkh) for qaga__vnkh in range(ugn__kwn)]), ',' if 
        ugn__kwn == 1 else '')
    mhj__ffgrf += '\n'
    mhj__ffgrf += '    for i in range(len(data_out_0)):\n'
    mhj__ffgrf += '        __eval_res(redvars, data_out, i)\n'
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, bdkc__oxlla)
    return bdkc__oxlla['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    tdpl__ujjr = n_keys
    hpdjm__znv = []
    for qaga__vnkh, ogt__ykgo in enumerate(allfuncs):
        if ogt__ykgo.ftype == 'gen_udf':
            hpdjm__znv.append(tdpl__ujjr)
            tdpl__ujjr += 1
        elif ogt__ykgo.ftype != 'udf':
            tdpl__ujjr += ogt__ykgo.ncols_post_shuffle
        else:
            tdpl__ujjr += ogt__ykgo.n_redvars + 1
    mhj__ffgrf = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    mhj__ffgrf += '    if num_groups == 0:\n'
    mhj__ffgrf += '        return\n'
    for qaga__vnkh, func in enumerate(udf_func_struct.general_udf_funcs):
        mhj__ffgrf += '    # col {}\n'.format(qaga__vnkh)
        mhj__ffgrf += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(hpdjm__znv[qaga__vnkh], qaga__vnkh))
        mhj__ffgrf += '    incref(out_col)\n'
        mhj__ffgrf += '    for j in range(num_groups):\n'
        mhj__ffgrf += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(qaga__vnkh, qaga__vnkh))
        mhj__ffgrf += '        incref(in_col)\n'
        mhj__ffgrf += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(qaga__vnkh))
    tyqx__gfp = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    qykwb__czp = 0
    for qaga__vnkh, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[qykwb__czp]
        tyqx__gfp['func_{}'.format(qykwb__czp)] = func
        tyqx__gfp['in_col_{}_typ'.format(qykwb__czp)] = in_col_typs[
            func_idx_to_in_col[qaga__vnkh]]
        tyqx__gfp['out_col_{}_typ'.format(qykwb__czp)] = out_col_typs[
            qaga__vnkh]
        qykwb__czp += 1
    bdkc__oxlla = {}
    exec(mhj__ffgrf, tyqx__gfp, bdkc__oxlla)
    ogt__ykgo = bdkc__oxlla['bodo_gb_apply_general_udfs{}'.format(label_suffix)
        ]
    xbl__xoj = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(xbl__xoj, nopython=True)(ogt__ykgo)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    wsj__rcyw = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        owcp__tqg = 1
    else:
        owcp__tqg = len(agg_node.pivot_values)
    lawef__jwx = tuple('key_' + sanitize_varname(mqj__ddit) for mqj__ddit in
        agg_node.key_names)
    fph__ayea = {mqj__ddit: 'in_{}'.format(sanitize_varname(mqj__ddit)) for
        mqj__ddit in agg_node.gb_info_in.keys() if mqj__ddit is not None}
    bcbl__pwwi = {mqj__ddit: ('out_' + sanitize_varname(mqj__ddit)) for
        mqj__ddit in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    zkan__wqnc = ', '.join(lawef__jwx)
    dgzyv__msty = ', '.join(fph__ayea.values())
    if dgzyv__msty != '':
        dgzyv__msty = ', ' + dgzyv__msty
    mhj__ffgrf = 'def agg_top({}{}{}, pivot_arr):\n'.format(zkan__wqnc,
        dgzyv__msty, ', index_arg' if agg_node.input_has_index else '')
    for a in (lawef__jwx + tuple(fph__ayea.values())):
        mhj__ffgrf += f'    {a} = decode_if_dict_array({a})\n'
    if wsj__rcyw:
        mhj__ffgrf += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        nqlq__rzsts = []
        for uxc__jhj, atne__euzw in agg_node.gb_info_in.items():
            if uxc__jhj is not None:
                for func, kxh__ukssb in atne__euzw:
                    nqlq__rzsts.append(fph__ayea[uxc__jhj])
    else:
        nqlq__rzsts = tuple(fph__ayea[uxc__jhj] for uxc__jhj, kxh__ukssb in
            agg_node.gb_info_out.values() if uxc__jhj is not None)
    yvbly__zyg = lawef__jwx + tuple(nqlq__rzsts)
    mhj__ffgrf += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in yvbly__zyg), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    mhj__ffgrf += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    pguoz__pett = []
    func_idx_to_in_col = []
    zsfp__qxz = []
    zuwir__epza = False
    srm__zxk = 1
    jlvt__gwwi = -1
    uwd__pkwq = 0
    esfzy__kges = 0
    if not wsj__rcyw:
        fspd__vmer = [func for kxh__ukssb, func in agg_node.gb_info_out.
            values()]
    else:
        fspd__vmer = [func for func, kxh__ukssb in atne__euzw for
            atne__euzw in agg_node.gb_info_in.values()]
    for oij__kznw, func in enumerate(fspd__vmer):
        pguoz__pett.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            uwd__pkwq += 1
        if hasattr(func, 'skipdropna'):
            zuwir__epza = func.skipdropna
        if func.ftype == 'shift':
            srm__zxk = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            esfzy__kges = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            jlvt__gwwi = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(oij__kznw)
        if func.ftype == 'udf':
            zsfp__qxz.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            zsfp__qxz.append(0)
            do_combine = False
    pguoz__pett.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == owcp__tqg, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * owcp__tqg, 'invalid number of groupby outputs'
    if uwd__pkwq > 0:
        if uwd__pkwq != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for qaga__vnkh, mqj__ddit in enumerate(agg_node.gb_info_out.keys()):
        ltjv__xibg = bcbl__pwwi[mqj__ddit] + '_dummy'
        ldko__dktoi = out_col_typs[qaga__vnkh]
        uxc__jhj, func = agg_node.gb_info_out[mqj__ddit]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(ldko__dktoi, bodo.
            CategoricalArrayType):
            mhj__ffgrf += '    {} = {}\n'.format(ltjv__xibg, fph__ayea[
                uxc__jhj])
        elif udf_func_struct is not None:
            mhj__ffgrf += '    {} = {}\n'.format(ltjv__xibg,
                _gen_dummy_alloc(ldko__dktoi, qaga__vnkh, False))
    if udf_func_struct is not None:
        hmy__yng = next_label()
        if udf_func_struct.regular_udfs:
            xbl__xoj = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            vez__uxu = numba.cfunc(xbl__xoj, nopython=True)(gen_update_cb(
                udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, hmy__yng))
            uic__hqsuw = numba.cfunc(xbl__xoj, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, hmy__yng))
            hieyt__bspb = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                hmy__yng))
            udf_func_struct.set_regular_cfuncs(vez__uxu, uic__hqsuw,
                hieyt__bspb)
            for omt__epat in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[omt__epat.native_name] = omt__epat
                gb_agg_cfunc_addr[omt__epat.native_name] = omt__epat.address
        if udf_func_struct.general_udfs:
            vqhw__duxo = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col, hmy__yng
                )
            udf_func_struct.set_general_cfunc(vqhw__duxo)
        hui__dtpr = []
        dsh__ygsf = 0
        qaga__vnkh = 0
        for ltjv__xibg, ogt__ykgo in zip(bcbl__pwwi.values(), allfuncs):
            if ogt__ykgo.ftype in ('udf', 'gen_udf'):
                hui__dtpr.append(ltjv__xibg + '_dummy')
                for hbg__mlbz in range(dsh__ygsf, dsh__ygsf + zsfp__qxz[
                    qaga__vnkh]):
                    hui__dtpr.append('data_redvar_dummy_' + str(hbg__mlbz))
                dsh__ygsf += zsfp__qxz[qaga__vnkh]
                qaga__vnkh += 1
        if udf_func_struct.regular_udfs:
            teet__bug = udf_func_struct.var_typs
            for qaga__vnkh, t in enumerate(teet__bug):
                mhj__ffgrf += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(qaga__vnkh, _get_np_dtype(t)))
        mhj__ffgrf += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in hui__dtpr))
        mhj__ffgrf += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            mhj__ffgrf += ("    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".
                format(vez__uxu.native_name))
            mhj__ffgrf += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(uic__hqsuw.native_name))
            mhj__ffgrf += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                hieyt__bspb.native_name)
            mhj__ffgrf += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(vez__uxu.native_name))
            mhj__ffgrf += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(uic__hqsuw.native_name))
            mhj__ffgrf += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(hieyt__bspb.native_name))
        else:
            mhj__ffgrf += '    cpp_cb_update_addr = 0\n'
            mhj__ffgrf += '    cpp_cb_combine_addr = 0\n'
            mhj__ffgrf += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            omt__epat = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[omt__epat.native_name] = omt__epat
            gb_agg_cfunc_addr[omt__epat.native_name] = omt__epat.address
            mhj__ffgrf += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(omt__epat.native_name))
            mhj__ffgrf += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(omt__epat.native_name))
        else:
            mhj__ffgrf += '    cpp_cb_general_addr = 0\n'
    else:
        mhj__ffgrf += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        mhj__ffgrf += '    cpp_cb_update_addr = 0\n'
        mhj__ffgrf += '    cpp_cb_combine_addr = 0\n'
        mhj__ffgrf += '    cpp_cb_eval_addr = 0\n'
        mhj__ffgrf += '    cpp_cb_general_addr = 0\n'
    mhj__ffgrf += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(ogt__ykgo.ftype)) for
        ogt__ykgo in allfuncs] + ['0']))
    mhj__ffgrf += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(
        str(pguoz__pett))
    if len(zsfp__qxz) > 0:
        mhj__ffgrf += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(zsfp__qxz))
    else:
        mhj__ffgrf += '    udf_ncols = np.array([0], np.int32)\n'
    if wsj__rcyw:
        mhj__ffgrf += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        mhj__ffgrf += '    arr_info = array_to_info(arr_type)\n'
        mhj__ffgrf += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        mhj__ffgrf += '    pivot_info = array_to_info(pivot_arr)\n'
        mhj__ffgrf += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        mhj__ffgrf += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, zuwir__epza, agg_node.return_key, agg_node.same_index)
            )
        mhj__ffgrf += '    delete_info_decref_array(pivot_info)\n'
        mhj__ffgrf += '    delete_info_decref_array(arr_info)\n'
    else:
        mhj__ffgrf += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, zuwir__epza,
            srm__zxk, esfzy__kges, jlvt__gwwi, agg_node.return_key,
            agg_node.same_index, agg_node.dropna))
    ajzyk__tui = 0
    if agg_node.return_key:
        for qaga__vnkh, umgyy__kyec in enumerate(lawef__jwx):
            mhj__ffgrf += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(umgyy__kyec, ajzyk__tui, umgyy__kyec))
            ajzyk__tui += 1
    for qaga__vnkh, ltjv__xibg in enumerate(bcbl__pwwi.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(ldko__dktoi, bodo.
            CategoricalArrayType):
            mhj__ffgrf += f"""    {ltjv__xibg} = info_to_array(info_from_table(out_table, {ajzyk__tui}), {ltjv__xibg + '_dummy'})
"""
        else:
            mhj__ffgrf += f"""    {ltjv__xibg} = info_to_array(info_from_table(out_table, {ajzyk__tui}), out_typs[{qaga__vnkh}])
"""
        ajzyk__tui += 1
    if agg_node.same_index:
        mhj__ffgrf += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(ajzyk__tui))
        ajzyk__tui += 1
    mhj__ffgrf += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    mhj__ffgrf += '    delete_table_decref_arrays(table)\n'
    mhj__ffgrf += '    delete_table_decref_arrays(udf_table_dummy)\n'
    mhj__ffgrf += '    delete_table(out_table)\n'
    mhj__ffgrf += f'    ev_clean.finalize()\n'
    flcey__jbxqg = tuple(bcbl__pwwi.values())
    if agg_node.return_key:
        flcey__jbxqg += tuple(lawef__jwx)
    mhj__ffgrf += '    return ({},{})\n'.format(', '.join(flcey__jbxqg), 
        ' out_index_arg,' if agg_node.same_index else '')
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {'out_typs': out_col_typs}, bdkc__oxlla)
    quqz__wpkh = bdkc__oxlla['agg_top']
    return quqz__wpkh


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for rauh__rxk in block.body:
            if is_call_assign(rauh__rxk) and find_callname(f_ir, rauh__rxk.
                value) == ('len', 'builtins') and rauh__rxk.value.args[0
                ].name == f_ir.arg_names[0]:
                ibnyh__monvk = get_definition(f_ir, rauh__rxk.value.func)
                ibnyh__monvk.name = 'dummy_agg_count'
                ibnyh__monvk.value = dummy_agg_count
    nkf__cyfs = get_name_var_table(f_ir.blocks)
    sqfb__xgxg = {}
    for name, kxh__ukssb in nkf__cyfs.items():
        sqfb__xgxg[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, sqfb__xgxg)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    djzw__avg = numba.core.compiler.Flags()
    djzw__avg.nrt = True
    bxa__hbhtr = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, djzw__avg)
    bxa__hbhtr.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, onps__uwhpn, calltypes, kxh__ukssb = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    botr__jefzk = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    zcbe__elnp = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    edov__bkfl = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    ymsjx__xitev = edov__bkfl(typemap, calltypes)
    pm = zcbe__elnp(typingctx, targetctx, None, f_ir, typemap, onps__uwhpn,
        calltypes, ymsjx__xitev, {}, djzw__avg, None)
    fhqn__oeh = numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline(
        pm)
    pm = zcbe__elnp(typingctx, targetctx, None, f_ir, typemap, onps__uwhpn,
        calltypes, ymsjx__xitev, {}, djzw__avg, fhqn__oeh)
    swrfn__exg = numba.core.typed_passes.InlineOverloads()
    swrfn__exg.run_pass(pm)
    getq__fyy = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    getq__fyy.run()
    for block in f_ir.blocks.values():
        for rauh__rxk in block.body:
            if is_assign(rauh__rxk) and isinstance(rauh__rxk.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[rauh__rxk.target.name],
                SeriesType):
                hhk__mou = typemap.pop(rauh__rxk.target.name)
                typemap[rauh__rxk.target.name] = hhk__mou.data
            if is_call_assign(rauh__rxk) and find_callname(f_ir, rauh__rxk.
                value) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[rauh__rxk.target.name].remove(rauh__rxk.value
                    )
                rauh__rxk.value = rauh__rxk.value.args[0]
                f_ir._definitions[rauh__rxk.target.name].append(rauh__rxk.value
                    )
            if is_call_assign(rauh__rxk) and find_callname(f_ir, rauh__rxk.
                value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[rauh__rxk.target.name].remove(rauh__rxk.value
                    )
                rauh__rxk.value = ir.Const(False, rauh__rxk.loc)
                f_ir._definitions[rauh__rxk.target.name].append(rauh__rxk.value
                    )
            if is_call_assign(rauh__rxk) and find_callname(f_ir, rauh__rxk.
                value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[rauh__rxk.target.name].remove(rauh__rxk.value
                    )
                rauh__rxk.value = ir.Const(False, rauh__rxk.loc)
                f_ir._definitions[rauh__rxk.target.name].append(rauh__rxk.value
                    )
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    ukpij__oagj = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, botr__jefzk)
    ukpij__oagj.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    gkljr__ynjs = numba.core.compiler.StateDict()
    gkljr__ynjs.func_ir = f_ir
    gkljr__ynjs.typemap = typemap
    gkljr__ynjs.calltypes = calltypes
    gkljr__ynjs.typingctx = typingctx
    gkljr__ynjs.targetctx = targetctx
    gkljr__ynjs.return_type = onps__uwhpn
    numba.core.rewrites.rewrite_registry.apply('after-inference', gkljr__ynjs)
    xey__nzgj = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        onps__uwhpn, typingctx, targetctx, botr__jefzk, djzw__avg, {})
    xey__nzgj.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            gwcm__bpoin = ctypes.pythonapi.PyCell_Get
            gwcm__bpoin.restype = ctypes.py_object
            gwcm__bpoin.argtypes = ctypes.py_object,
            ewil__oyq = tuple(gwcm__bpoin(ijc__izzov) for ijc__izzov in closure
                )
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            ewil__oyq = closure.items
        assert len(code.co_freevars) == len(ewil__oyq)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, ewil__oyq)


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
        wyh__izvft = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type
            )
        f_ir, pm = compile_to_optimized_ir(func, (wyh__izvft,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        wljq__zcp, arr_var = _rm_arg_agg_block(block, pm.typemap)
        yfk__qibpu = -1
        for qaga__vnkh, rauh__rxk in enumerate(wljq__zcp):
            if isinstance(rauh__rxk, numba.parfors.parfor.Parfor):
                assert yfk__qibpu == -1, 'only one parfor for aggregation function'
                yfk__qibpu = qaga__vnkh
        parfor = None
        if yfk__qibpu != -1:
            parfor = wljq__zcp[yfk__qibpu]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = wljq__zcp[:yfk__qibpu] + parfor.init_block.body
        eval_nodes = wljq__zcp[yfk__qibpu + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for rauh__rxk in init_nodes:
            if is_assign(rauh__rxk) and rauh__rxk.target.name in redvars:
                ind = redvars.index(rauh__rxk.target.name)
                reduce_vars[ind] = rauh__rxk.target
        var_types = [pm.typemap[uko__ydos] for uko__ydos in redvars]
        dxbld__uzlfh = gen_combine_func(f_ir, parfor, redvars,
            var_to_redvar, var_types, arr_var, pm, self.typingctx, self.
            targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        ssec__jgx = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        kxis__tfzir = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(kxis__tfzir)
        self.all_update_funcs.append(ssec__jgx)
        self.all_combine_funcs.append(dxbld__uzlfh)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        pwjbh__tijug = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        ppfhr__boe = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        ehhb__pnh = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        wwr__iexjl = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, pwjbh__tijug, ppfhr__boe, ehhb__pnh,
            wwr__iexjl)


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
    wts__xudiy = []
    for t, ogt__ykgo in zip(in_col_types, agg_func):
        wts__xudiy.append((t, ogt__ykgo))
    xfaq__jvw = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    kgm__obq = GeneralUDFGenerator()
    for in_col_typ, func in wts__xudiy:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            xfaq__jvw.add_udf(in_col_typ, func)
        except:
            kgm__obq.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = xfaq__jvw.gen_all_func()
    general_udf_funcs = kgm__obq.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    xhbj__dwx = compute_use_defs(parfor.loop_body)
    abdh__jbdeg = set()
    for iboyg__gzt in xhbj__dwx.usemap.values():
        abdh__jbdeg |= iboyg__gzt
    yku__cjz = set()
    for iboyg__gzt in xhbj__dwx.defmap.values():
        yku__cjz |= iboyg__gzt
    rlr__xne = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    rlr__xne.body = eval_nodes
    ozofx__zav = compute_use_defs({(0): rlr__xne})
    zuv__oly = ozofx__zav.usemap[0]
    atf__lysq = set()
    dzql__ywfb = []
    jwds__ovu = []
    for rauh__rxk in reversed(init_nodes):
        vidab__tnvxb = {uko__ydos.name for uko__ydos in rauh__rxk.list_vars()}
        if is_assign(rauh__rxk):
            uko__ydos = rauh__rxk.target.name
            vidab__tnvxb.remove(uko__ydos)
            if (uko__ydos in abdh__jbdeg and uko__ydos not in atf__lysq and
                uko__ydos not in zuv__oly and uko__ydos not in yku__cjz):
                jwds__ovu.append(rauh__rxk)
                abdh__jbdeg |= vidab__tnvxb
                yku__cjz.add(uko__ydos)
                continue
        atf__lysq |= vidab__tnvxb
        dzql__ywfb.append(rauh__rxk)
    jwds__ovu.reverse()
    dzql__ywfb.reverse()
    pynl__goaiz = min(parfor.loop_body.keys())
    dyfd__uif = parfor.loop_body[pynl__goaiz]
    dyfd__uif.body = jwds__ovu + dyfd__uif.body
    return dzql__ywfb


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    qgohe__udmdj = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ihyt__cvvkm = set()
    rbl__kvlj = []
    for rauh__rxk in init_nodes:
        if is_assign(rauh__rxk) and isinstance(rauh__rxk.value, ir.Global
            ) and isinstance(rauh__rxk.value.value, pytypes.FunctionType
            ) and rauh__rxk.value.value in qgohe__udmdj:
            ihyt__cvvkm.add(rauh__rxk.target.name)
        elif is_call_assign(rauh__rxk
            ) and rauh__rxk.value.func.name in ihyt__cvvkm:
            pass
        else:
            rbl__kvlj.append(rauh__rxk)
    init_nodes = rbl__kvlj
    ilr__tolq = types.Tuple(var_types)
    lrj__fxzr = lambda : None
    f_ir = compile_to_numba_ir(lrj__fxzr, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    fdi__jlqvn = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    rpykb__yzba = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        fdi__jlqvn, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [rpykb__yzba] + block.body
    block.body[-2].value.value = fdi__jlqvn
    tvt__zagv = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        ilr__tolq, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    whygy__pjq = numba.core.target_extension.dispatcher_registry[cpu_target](
        lrj__fxzr)
    whygy__pjq.add_overload(tvt__zagv)
    return whygy__pjq


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    rrx__mafq = len(update_funcs)
    nbyhv__odemp = len(in_col_types)
    if pivot_values is not None:
        assert nbyhv__odemp == 1
    mhj__ffgrf = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        gxg__uxvc = redvar_offsets[nbyhv__odemp]
        mhj__ffgrf += '  pv = pivot_arr[i]\n'
        for hbg__mlbz, pogpj__meva in enumerate(pivot_values):
            eml__fct = 'el' if hbg__mlbz != 0 else ''
            mhj__ffgrf += "  {}if pv == '{}':\n".format(eml__fct, pogpj__meva)
            ofx__vznoy = gxg__uxvc * hbg__mlbz
            auxm__fnbc = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                qaga__vnkh) for qaga__vnkh in range(ofx__vznoy +
                redvar_offsets[0], ofx__vznoy + redvar_offsets[1])])
            zwtrx__drn = 'data_in[0][i]'
            if is_crosstab:
                zwtrx__drn = '0'
            mhj__ffgrf += '    {} = update_vars_0({}, {})\n'.format(auxm__fnbc,
                auxm__fnbc, zwtrx__drn)
    else:
        for hbg__mlbz in range(rrx__mafq):
            auxm__fnbc = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                qaga__vnkh) for qaga__vnkh in range(redvar_offsets[
                hbg__mlbz], redvar_offsets[hbg__mlbz + 1])])
            if auxm__fnbc:
                mhj__ffgrf += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(auxm__fnbc, hbg__mlbz, auxm__fnbc, 0 if 
                    nbyhv__odemp == 1 else hbg__mlbz))
    mhj__ffgrf += '  return\n'
    tyqx__gfp = {}
    for qaga__vnkh, ogt__ykgo in enumerate(update_funcs):
        tyqx__gfp['update_vars_{}'.format(qaga__vnkh)] = ogt__ykgo
    bdkc__oxlla = {}
    exec(mhj__ffgrf, tyqx__gfp, bdkc__oxlla)
    xexzs__wep = bdkc__oxlla['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(xexzs__wep)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    albnf__lesdu = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    arg_typs = albnf__lesdu, albnf__lesdu, types.intp, types.intp, pivot_typ
    behw__pykll = len(redvar_offsets) - 1
    gxg__uxvc = redvar_offsets[behw__pykll]
    mhj__ffgrf = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert behw__pykll == 1
        for zgp__azjo in range(len(pivot_values)):
            ofx__vznoy = gxg__uxvc * zgp__azjo
            auxm__fnbc = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                qaga__vnkh) for qaga__vnkh in range(ofx__vznoy +
                redvar_offsets[0], ofx__vznoy + redvar_offsets[1])])
            zqpyb__oap = ', '.join(['recv_arrs[{}][i]'.format(qaga__vnkh) for
                qaga__vnkh in range(ofx__vznoy + redvar_offsets[0], 
                ofx__vznoy + redvar_offsets[1])])
            mhj__ffgrf += '  {} = combine_vars_0({}, {})\n'.format(auxm__fnbc,
                auxm__fnbc, zqpyb__oap)
    else:
        for hbg__mlbz in range(behw__pykll):
            auxm__fnbc = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                qaga__vnkh) for qaga__vnkh in range(redvar_offsets[
                hbg__mlbz], redvar_offsets[hbg__mlbz + 1])])
            zqpyb__oap = ', '.join(['recv_arrs[{}][i]'.format(qaga__vnkh) for
                qaga__vnkh in range(redvar_offsets[hbg__mlbz],
                redvar_offsets[hbg__mlbz + 1])])
            if zqpyb__oap:
                mhj__ffgrf += '  {} = combine_vars_{}({}, {})\n'.format(
                    auxm__fnbc, hbg__mlbz, auxm__fnbc, zqpyb__oap)
    mhj__ffgrf += '  return\n'
    tyqx__gfp = {}
    for qaga__vnkh, ogt__ykgo in enumerate(combine_funcs):
        tyqx__gfp['combine_vars_{}'.format(qaga__vnkh)] = ogt__ykgo
    bdkc__oxlla = {}
    exec(mhj__ffgrf, tyqx__gfp, bdkc__oxlla)
    kilb__xhwr = bdkc__oxlla['combine_all_f']
    f_ir = compile_to_numba_ir(kilb__xhwr, tyqx__gfp)
    ehhb__pnh = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    whygy__pjq = numba.core.target_extension.dispatcher_registry[cpu_target](
        kilb__xhwr)
    whygy__pjq.add_overload(ehhb__pnh)
    return whygy__pjq


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    albnf__lesdu = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    behw__pykll = len(redvar_offsets) - 1
    gxg__uxvc = redvar_offsets[behw__pykll]
    mhj__ffgrf = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert behw__pykll == 1
        for hbg__mlbz in range(len(pivot_values)):
            ofx__vznoy = gxg__uxvc * hbg__mlbz
            auxm__fnbc = ', '.join(['redvar_arrs[{}][j]'.format(qaga__vnkh) for
                qaga__vnkh in range(ofx__vznoy + redvar_offsets[0], 
                ofx__vznoy + redvar_offsets[1])])
            mhj__ffgrf += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                hbg__mlbz, auxm__fnbc)
    else:
        for hbg__mlbz in range(behw__pykll):
            auxm__fnbc = ', '.join(['redvar_arrs[{}][j]'.format(qaga__vnkh) for
                qaga__vnkh in range(redvar_offsets[hbg__mlbz],
                redvar_offsets[hbg__mlbz + 1])])
            mhj__ffgrf += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                hbg__mlbz, hbg__mlbz, auxm__fnbc)
    mhj__ffgrf += '  return\n'
    tyqx__gfp = {}
    for qaga__vnkh, ogt__ykgo in enumerate(eval_funcs):
        tyqx__gfp['eval_vars_{}'.format(qaga__vnkh)] = ogt__ykgo
    bdkc__oxlla = {}
    exec(mhj__ffgrf, tyqx__gfp, bdkc__oxlla)
    royav__acsl = bdkc__oxlla['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(royav__acsl)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    btimf__lnqrz = len(var_types)
    mpve__fjvb = [f'in{qaga__vnkh}' for qaga__vnkh in range(btimf__lnqrz)]
    ilr__tolq = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    zil__lmcx = ilr__tolq(0)
    mhj__ffgrf = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        mpve__fjvb))
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {'_zero': zil__lmcx}, bdkc__oxlla)
    ilbc__aog = bdkc__oxlla['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(ilbc__aog, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': zil__lmcx}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    yai__gev = []
    for qaga__vnkh, uko__ydos in enumerate(reduce_vars):
        yai__gev.append(ir.Assign(block.body[qaga__vnkh].target, uko__ydos,
            uko__ydos.loc))
        for knf__jdfm in uko__ydos.versioned_names:
            yai__gev.append(ir.Assign(uko__ydos, ir.Var(uko__ydos.scope,
                knf__jdfm, uko__ydos.loc), uko__ydos.loc))
    block.body = block.body[:btimf__lnqrz] + yai__gev + eval_nodes
    kxis__tfzir = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ilr__tolq, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    whygy__pjq = numba.core.target_extension.dispatcher_registry[cpu_target](
        ilbc__aog)
    whygy__pjq.add_overload(kxis__tfzir)
    return whygy__pjq


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    btimf__lnqrz = len(redvars)
    glvm__qawhw = [f'v{qaga__vnkh}' for qaga__vnkh in range(btimf__lnqrz)]
    mpve__fjvb = [f'in{qaga__vnkh}' for qaga__vnkh in range(btimf__lnqrz)]
    mhj__ffgrf = 'def agg_combine({}):\n'.format(', '.join(glvm__qawhw +
        mpve__fjvb))
    lcyc__wrea = wrap_parfor_blocks(parfor)
    gwhli__ynwi = find_topo_order(lcyc__wrea)
    gwhli__ynwi = gwhli__ynwi[1:]
    unwrap_parfor_blocks(parfor)
    far__xohq = {}
    vbqo__ybtt = []
    for xypcy__fqwo in gwhli__ynwi:
        qmsz__sjxkn = parfor.loop_body[xypcy__fqwo]
        for rauh__rxk in qmsz__sjxkn.body:
            if is_call_assign(rauh__rxk) and guard(find_callname, f_ir,
                rauh__rxk.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = rauh__rxk.value.args
                onmtt__ocoil = []
                pqrxs__vyv = []
                for uko__ydos in args[:-1]:
                    ind = redvars.index(uko__ydos.name)
                    vbqo__ybtt.append(ind)
                    onmtt__ocoil.append('v{}'.format(ind))
                    pqrxs__vyv.append('in{}'.format(ind))
                yud__ygmv = '__special_combine__{}'.format(len(far__xohq))
                mhj__ffgrf += '    ({},) = {}({})\n'.format(', '.join(
                    onmtt__ocoil), yud__ygmv, ', '.join(onmtt__ocoil +
                    pqrxs__vyv))
                zxbvw__lqzn = ir.Expr.call(args[-1], [], (), qmsz__sjxkn.loc)
                wjcfg__kbi = guard(find_callname, f_ir, zxbvw__lqzn)
                assert wjcfg__kbi == ('_var_combine', 'bodo.ir.aggregate')
                wjcfg__kbi = bodo.ir.aggregate._var_combine
                far__xohq[yud__ygmv] = wjcfg__kbi
            if is_assign(rauh__rxk) and rauh__rxk.target.name in redvars:
                prq__fou = rauh__rxk.target.name
                ind = redvars.index(prq__fou)
                if ind in vbqo__ybtt:
                    continue
                if len(f_ir._definitions[prq__fou]) == 2:
                    var_def = f_ir._definitions[prq__fou][0]
                    mhj__ffgrf += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[prq__fou][1]
                    mhj__ffgrf += _match_reduce_def(var_def, f_ir, ind)
    mhj__ffgrf += '    return {}'.format(', '.join(['v{}'.format(qaga__vnkh
        ) for qaga__vnkh in range(btimf__lnqrz)]))
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {}, bdkc__oxlla)
    ujrum__hps = bdkc__oxlla['agg_combine']
    arg_typs = tuple(2 * var_types)
    tyqx__gfp = {'numba': numba, 'bodo': bodo, 'np': np}
    tyqx__gfp.update(far__xohq)
    f_ir = compile_to_numba_ir(ujrum__hps, tyqx__gfp, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    ilr__tolq = pm.typemap[block.body[-1].value.name]
    dxbld__uzlfh = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ilr__tolq, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    whygy__pjq = numba.core.target_extension.dispatcher_registry[cpu_target](
        ujrum__hps)
    whygy__pjq.add_overload(dxbld__uzlfh)
    return whygy__pjq


def _match_reduce_def(var_def, f_ir, ind):
    mhj__ffgrf = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        mhj__ffgrf = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        wrs__wxnt = guard(find_callname, f_ir, var_def)
        if wrs__wxnt == ('min', 'builtins'):
            mhj__ffgrf = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if wrs__wxnt == ('max', 'builtins'):
            mhj__ffgrf = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return mhj__ffgrf


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    btimf__lnqrz = len(redvars)
    vqk__qahg = 1
    lmih__iaa = []
    for qaga__vnkh in range(vqk__qahg):
        xxhup__obtk = ir.Var(arr_var.scope, f'$input{qaga__vnkh}', arr_var.loc)
        lmih__iaa.append(xxhup__obtk)
    rajc__wgay = parfor.loop_nests[0].index_variable
    ebt__mgv = [0] * btimf__lnqrz
    for qmsz__sjxkn in parfor.loop_body.values():
        fqhe__wdite = []
        for rauh__rxk in qmsz__sjxkn.body:
            if is_var_assign(rauh__rxk
                ) and rauh__rxk.value.name == rajc__wgay.name:
                continue
            if is_getitem(rauh__rxk
                ) and rauh__rxk.value.value.name == arr_var.name:
                rauh__rxk.value = lmih__iaa[0]
            if is_call_assign(rauh__rxk) and guard(find_callname, pm.
                func_ir, rauh__rxk.value) == ('isna', 'bodo.libs.array_kernels'
                ) and rauh__rxk.value.args[0].name == arr_var.name:
                rauh__rxk.value = ir.Const(False, rauh__rxk.target.loc)
            if is_assign(rauh__rxk) and rauh__rxk.target.name in redvars:
                ind = redvars.index(rauh__rxk.target.name)
                ebt__mgv[ind] = rauh__rxk.target
            fqhe__wdite.append(rauh__rxk)
        qmsz__sjxkn.body = fqhe__wdite
    glvm__qawhw = ['v{}'.format(qaga__vnkh) for qaga__vnkh in range(
        btimf__lnqrz)]
    mpve__fjvb = ['in{}'.format(qaga__vnkh) for qaga__vnkh in range(vqk__qahg)]
    mhj__ffgrf = 'def agg_update({}):\n'.format(', '.join(glvm__qawhw +
        mpve__fjvb))
    mhj__ffgrf += '    __update_redvars()\n'
    mhj__ffgrf += '    return {}'.format(', '.join(['v{}'.format(qaga__vnkh
        ) for qaga__vnkh in range(btimf__lnqrz)]))
    bdkc__oxlla = {}
    exec(mhj__ffgrf, {}, bdkc__oxlla)
    yzu__htst = bdkc__oxlla['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * vqk__qahg)
    f_ir = compile_to_numba_ir(yzu__htst, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    imhyh__gfgxx = f_ir.blocks.popitem()[1].body
    ilr__tolq = pm.typemap[imhyh__gfgxx[-1].value.name]
    lcyc__wrea = wrap_parfor_blocks(parfor)
    gwhli__ynwi = find_topo_order(lcyc__wrea)
    gwhli__ynwi = gwhli__ynwi[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    dyfd__uif = f_ir.blocks[gwhli__ynwi[0]]
    rzde__uax = f_ir.blocks[gwhli__ynwi[-1]]
    lqt__fupv = imhyh__gfgxx[:btimf__lnqrz + vqk__qahg]
    if btimf__lnqrz > 1:
        htve__fiup = imhyh__gfgxx[-3:]
        assert is_assign(htve__fiup[0]) and isinstance(htve__fiup[0].value,
            ir.Expr) and htve__fiup[0].value.op == 'build_tuple'
    else:
        htve__fiup = imhyh__gfgxx[-2:]
    for qaga__vnkh in range(btimf__lnqrz):
        ytd__gdfr = imhyh__gfgxx[qaga__vnkh].target
        dxe__pkjeq = ir.Assign(ytd__gdfr, ebt__mgv[qaga__vnkh], ytd__gdfr.loc)
        lqt__fupv.append(dxe__pkjeq)
    for qaga__vnkh in range(btimf__lnqrz, btimf__lnqrz + vqk__qahg):
        ytd__gdfr = imhyh__gfgxx[qaga__vnkh].target
        dxe__pkjeq = ir.Assign(ytd__gdfr, lmih__iaa[qaga__vnkh -
            btimf__lnqrz], ytd__gdfr.loc)
        lqt__fupv.append(dxe__pkjeq)
    dyfd__uif.body = lqt__fupv + dyfd__uif.body
    omkmd__syvu = []
    for qaga__vnkh in range(btimf__lnqrz):
        ytd__gdfr = imhyh__gfgxx[qaga__vnkh].target
        dxe__pkjeq = ir.Assign(ebt__mgv[qaga__vnkh], ytd__gdfr, ytd__gdfr.loc)
        omkmd__syvu.append(dxe__pkjeq)
    rzde__uax.body += omkmd__syvu + htve__fiup
    sqzb__ikz = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ilr__tolq, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    whygy__pjq = numba.core.target_extension.dispatcher_registry[cpu_target](
        yzu__htst)
    whygy__pjq.add_overload(sqzb__ikz)
    return whygy__pjq


def _rm_arg_agg_block(block, typemap):
    wljq__zcp = []
    arr_var = None
    for qaga__vnkh, rauh__rxk in enumerate(block.body):
        if is_assign(rauh__rxk) and isinstance(rauh__rxk.value, ir.Arg):
            arr_var = rauh__rxk.target
            xyvss__qsufx = typemap[arr_var.name]
            if not isinstance(xyvss__qsufx, types.ArrayCompatible):
                wljq__zcp += block.body[qaga__vnkh + 1:]
                break
            ctu__xzwpn = block.body[qaga__vnkh + 1]
            assert is_assign(ctu__xzwpn) and isinstance(ctu__xzwpn.value,
                ir.Expr
                ) and ctu__xzwpn.value.op == 'getattr' and ctu__xzwpn.value.attr == 'shape' and ctu__xzwpn.value.value.name == arr_var.name
            zmb__qwmv = ctu__xzwpn.target
            gxf__yop = block.body[qaga__vnkh + 2]
            assert is_assign(gxf__yop) and isinstance(gxf__yop.value, ir.Expr
                ) and gxf__yop.value.op == 'static_getitem' and gxf__yop.value.value.name == zmb__qwmv.name
            wljq__zcp += block.body[qaga__vnkh + 3:]
            break
        wljq__zcp.append(rauh__rxk)
    return wljq__zcp, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    lcyc__wrea = wrap_parfor_blocks(parfor)
    gwhli__ynwi = find_topo_order(lcyc__wrea)
    gwhli__ynwi = gwhli__ynwi[1:]
    unwrap_parfor_blocks(parfor)
    for xypcy__fqwo in reversed(gwhli__ynwi):
        for rauh__rxk in reversed(parfor.loop_body[xypcy__fqwo].body):
            if isinstance(rauh__rxk, ir.Assign) and (rauh__rxk.target.name in
                parfor_params or rauh__rxk.target.name in var_to_param):
                blp__tmusw = rauh__rxk.target.name
                rhs = rauh__rxk.value
                cqk__zweox = (blp__tmusw if blp__tmusw in parfor_params else
                    var_to_param[blp__tmusw])
                ecb__oswp = []
                if isinstance(rhs, ir.Var):
                    ecb__oswp = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    ecb__oswp = [uko__ydos.name for uko__ydos in rauh__rxk.
                        value.list_vars()]
                param_uses[cqk__zweox].extend(ecb__oswp)
                for uko__ydos in ecb__oswp:
                    var_to_param[uko__ydos] = cqk__zweox
            if isinstance(rauh__rxk, Parfor):
                get_parfor_reductions(rauh__rxk, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for lufwz__hgclq, ecb__oswp in param_uses.items():
        if lufwz__hgclq in ecb__oswp and lufwz__hgclq not in reduce_varnames:
            reduce_varnames.append(lufwz__hgclq)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
