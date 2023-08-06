"""IR node for the join and merge"""
from collections import defaultdict
from typing import List, Literal, Union
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, hash_join_table, info_from_table, info_to_array
from bodo.libs.int_arr_ext import IntDtype
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.typing import BodoError, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, debug_prints, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        vbmp__fwjru = func.signature
        oqu__vqs = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        tgy__uuz = cgutils.get_or_insert_function(builder.module, oqu__vqs,
            sym._literal_value)
        builder.call(tgy__uuz, [context.get_constant_null(vbmp__fwjru.args[
            0]), context.get_constant_null(vbmp__fwjru.args[1]), context.
            get_constant_null(vbmp__fwjru.args[2]), context.
            get_constant_null(vbmp__fwjru.args[3]), context.
            get_constant_null(vbmp__fwjru.args[4]), context.
            get_constant_null(vbmp__fwjru.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


HOW_OPTIONS = Literal['inner', 'left', 'right', 'outer', 'asof']


class Join(ir.Stmt):

    def __init__(self, df_out: str, left_df: str, right_df: str, left_keys:
        Union[List[str], str], right_keys: Union[List[str], str],
        out_data_vars: List[ir.Var], left_vars: List[ir.Var], right_vars:
        List[ir.Var], how: HOW_OPTIONS, suffix_left: str, suffix_right: str,
        loc: ir.Loc, is_left: bool, is_right: bool, is_join: bool,
        left_index: bool, right_index: bool, indicator: bool, is_na_equal:
        bool, gen_cond_expr: str):
        self.df_out = df_out
        self.left_df = left_df
        self.right_df = right_df
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.left_key_set = set(left_keys)
        self.right_key_set = set(right_keys)
        self.out_data_vars = out_data_vars
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.suffix_left = suffix_left
        self.suffix_right = suffix_right
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator = indicator
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        if gen_cond_expr:
            self.left_cond_cols = set(yip__ppr for yip__ppr in left_vars.
                keys() if f'(left.{yip__ppr})' in gen_cond_expr)
            self.right_cond_cols = set(yip__ppr for yip__ppr in right_vars.
                keys() if f'(right.{yip__ppr})' in gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        vxw__dwd = self.left_key_set & self.right_key_set
        lswi__ezk = set(left_vars.keys()) & set(right_vars.keys())
        duq__mysv = lswi__ezk - vxw__dwd
        vect_same_key = []
        n_keys = len(left_keys)
        for dfenf__gbtg in range(n_keys):
            natz__sev = left_keys[dfenf__gbtg]
            qyh__tckn = right_keys[dfenf__gbtg]
            vect_same_key.append(natz__sev == qyh__tckn)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(yip__ppr) + suffix_left if yip__ppr in
            duq__mysv else yip__ppr): ('left', yip__ppr) for yip__ppr in
            left_vars.keys()}
        self.column_origins.update({(str(yip__ppr) + suffix_right if 
            yip__ppr in duq__mysv else yip__ppr): ('right', yip__ppr) for
            yip__ppr in right_vars.keys()})
        if '$_bodo_index_' in duq__mysv:
            duq__mysv.remove('$_bodo_index_')
        self.add_suffix = duq__mysv

    def __repr__(self):
        xwmy__lpyj = ''
        for yip__ppr, lcdcr__nvwy in self.out_data_vars.items():
            xwmy__lpyj += "'{}':{}, ".format(yip__ppr, lcdcr__nvwy.name)
        bcnpb__jbb = '{}{{{}}}'.format(self.df_out, xwmy__lpyj)
        asuj__lywst = ''
        for yip__ppr, lcdcr__nvwy in self.left_vars.items():
            asuj__lywst += "'{}':{}, ".format(yip__ppr, lcdcr__nvwy.name)
        qkqv__ojvov = '{}{{{}}}'.format(self.left_df, asuj__lywst)
        asuj__lywst = ''
        for yip__ppr, lcdcr__nvwy in self.right_vars.items():
            asuj__lywst += "'{}':{}, ".format(yip__ppr, lcdcr__nvwy.name)
        ywzi__yqyz = '{}{{{}}}'.format(self.right_df, asuj__lywst)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, bcnpb__jbb, qkqv__ojvov, ywzi__yqyz)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    aviic__vwvnp = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    jtake__ghefa = []
    khx__hhlb = list(join_node.left_vars.values())
    for glyz__xeq in khx__hhlb:
        lwado__rxc = typemap[glyz__xeq.name]
        lopud__xajv = equiv_set.get_shape(glyz__xeq)
        if lopud__xajv:
            jtake__ghefa.append(lopud__xajv[0])
    if len(jtake__ghefa) > 1:
        equiv_set.insert_equiv(*jtake__ghefa)
    jtake__ghefa = []
    khx__hhlb = list(join_node.right_vars.values())
    for glyz__xeq in khx__hhlb:
        lwado__rxc = typemap[glyz__xeq.name]
        lopud__xajv = equiv_set.get_shape(glyz__xeq)
        if lopud__xajv:
            jtake__ghefa.append(lopud__xajv[0])
    if len(jtake__ghefa) > 1:
        equiv_set.insert_equiv(*jtake__ghefa)
    jtake__ghefa = []
    for glyz__xeq in join_node.out_data_vars.values():
        lwado__rxc = typemap[glyz__xeq.name]
        tqqvk__qqgfe = array_analysis._gen_shape_call(equiv_set, glyz__xeq,
            lwado__rxc.ndim, None, aviic__vwvnp)
        equiv_set.insert_equiv(glyz__xeq, tqqvk__qqgfe)
        jtake__ghefa.append(tqqvk__qqgfe[0])
        equiv_set.define(glyz__xeq, set())
    if len(jtake__ghefa) > 1:
        equiv_set.insert_equiv(*jtake__ghefa)
    return [], aviic__vwvnp


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    ezzzx__aix = Distribution.OneD
    vya__xxjz = Distribution.OneD
    for glyz__xeq in join_node.left_vars.values():
        ezzzx__aix = Distribution(min(ezzzx__aix.value, array_dists[
            glyz__xeq.name].value))
    for glyz__xeq in join_node.right_vars.values():
        vya__xxjz = Distribution(min(vya__xxjz.value, array_dists[glyz__xeq
            .name].value))
    bqq__bwa = Distribution.OneD_Var
    for glyz__xeq in join_node.out_data_vars.values():
        if glyz__xeq.name in array_dists:
            bqq__bwa = Distribution(min(bqq__bwa.value, array_dists[
                glyz__xeq.name].value))
    ipk__mte = Distribution(min(bqq__bwa.value, ezzzx__aix.value))
    okvus__kcjkx = Distribution(min(bqq__bwa.value, vya__xxjz.value))
    bqq__bwa = Distribution(max(ipk__mte.value, okvus__kcjkx.value))
    for glyz__xeq in join_node.out_data_vars.values():
        array_dists[glyz__xeq.name] = bqq__bwa
    if bqq__bwa != Distribution.OneD_Var:
        ezzzx__aix = bqq__bwa
        vya__xxjz = bqq__bwa
    for glyz__xeq in join_node.left_vars.values():
        array_dists[glyz__xeq.name] = ezzzx__aix
    for glyz__xeq in join_node.right_vars.values():
        array_dists[glyz__xeq.name] = vya__xxjz
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    for ykkti__azaeo, fho__eze in join_node.out_data_vars.items():
        if join_node.indicator and ykkti__azaeo == '_merge':
            continue
        if not ykkti__azaeo in join_node.column_origins:
            raise BodoError('join(): The variable ' + ykkti__azaeo +
                ' is absent from the output')
        ishh__nupru = join_node.column_origins[ykkti__azaeo]
        if ishh__nupru[0] == 'left':
            glyz__xeq = join_node.left_vars[ishh__nupru[1]]
        else:
            glyz__xeq = join_node.right_vars[ishh__nupru[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=fho__eze.
            name, src=glyz__xeq.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for smtq__yblm in list(join_node.left_vars.keys()):
        join_node.left_vars[smtq__yblm] = visit_vars_inner(join_node.
            left_vars[smtq__yblm], callback, cbdata)
    for smtq__yblm in list(join_node.right_vars.keys()):
        join_node.right_vars[smtq__yblm] = visit_vars_inner(join_node.
            right_vars[smtq__yblm], callback, cbdata)
    for smtq__yblm in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[smtq__yblm] = visit_vars_inner(join_node.
            out_data_vars[smtq__yblm], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    keklc__ammz = []
    lyvah__hbkb = True
    for smtq__yblm, glyz__xeq in join_node.out_data_vars.items():
        if glyz__xeq.name in lives:
            lyvah__hbkb = False
            continue
        if smtq__yblm == '$_bodo_index_':
            continue
        if join_node.indicator and smtq__yblm == '_merge':
            keklc__ammz.append('_merge')
            join_node.indicator = False
            continue
        vnt__cbvei, tqsh__ntg = join_node.column_origins[smtq__yblm]
        if (vnt__cbvei == 'left' and tqsh__ntg not in join_node.
            left_key_set and tqsh__ntg not in join_node.left_cond_cols):
            join_node.left_vars.pop(tqsh__ntg)
            keklc__ammz.append(smtq__yblm)
        if (vnt__cbvei == 'right' and tqsh__ntg not in join_node.
            right_key_set and tqsh__ntg not in join_node.right_cond_cols):
            join_node.right_vars.pop(tqsh__ntg)
            keklc__ammz.append(smtq__yblm)
    for cname in keklc__ammz:
        join_node.out_data_vars.pop(cname)
    if lyvah__hbkb:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({lcdcr__nvwy.name for lcdcr__nvwy in join_node.left_vars
        .values()})
    use_set.update({lcdcr__nvwy.name for lcdcr__nvwy in join_node.
        right_vars.values()})
    def_set.update({lcdcr__nvwy.name for lcdcr__nvwy in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    epc__hzzo = set(lcdcr__nvwy.name for lcdcr__nvwy in join_node.
        out_data_vars.values())
    return set(), epc__hzzo


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for smtq__yblm in list(join_node.left_vars.keys()):
        join_node.left_vars[smtq__yblm] = replace_vars_inner(join_node.
            left_vars[smtq__yblm], var_dict)
    for smtq__yblm in list(join_node.right_vars.keys()):
        join_node.right_vars[smtq__yblm] = replace_vars_inner(join_node.
            right_vars[smtq__yblm], var_dict)
    for smtq__yblm in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[smtq__yblm] = replace_vars_inner(join_node.
            out_data_vars[smtq__yblm], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for glyz__xeq in join_node.out_data_vars.values():
        definitions[glyz__xeq.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    tovsp__mgxqw = tuple(join_node.left_vars[yip__ppr] for yip__ppr in
        join_node.left_keys)
    hxgm__zqvmf = tuple(join_node.right_vars[yip__ppr] for yip__ppr in
        join_node.right_keys)
    left_vars = join_node.left_vars
    right_vars = join_node.right_vars
    ympj__xjfv = ()
    mzfen__wdtpw = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        jjz__bsb = join_node.right_keys[0]
        if jjz__bsb in left_vars:
            mzfen__wdtpw = jjz__bsb,
            ympj__xjfv = join_node.right_vars[jjz__bsb],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        jjz__bsb = join_node.left_keys[0]
        if jjz__bsb in right_vars:
            mzfen__wdtpw = jjz__bsb,
            ympj__xjfv = join_node.left_vars[jjz__bsb],
            optional_column = True
    wgqq__gzbls = [join_node.out_data_vars[cname] for cname in mzfen__wdtpw]
    okj__suh = tuple(lcdcr__nvwy for dgww__wwh, lcdcr__nvwy in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if dgww__wwh
         not in join_node.left_key_set)
    mli__xmmgp = tuple(lcdcr__nvwy for dgww__wwh, lcdcr__nvwy in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if dgww__wwh
         not in join_node.right_key_set)
    kfgh__ixyp = (ympj__xjfv + tovsp__mgxqw + hxgm__zqvmf + okj__suh +
        mli__xmmgp)
    flrqh__iafhs = tuple(typemap[lcdcr__nvwy.name] for lcdcr__nvwy in
        kfgh__ixyp)
    udpu__jey = tuple('opti_c' + str(ddyx__istz) for ddyx__istz in range(
        len(ympj__xjfv)))
    left_other_names = tuple('t1_c' + str(ddyx__istz) for ddyx__istz in
        range(len(okj__suh)))
    right_other_names = tuple('t2_c' + str(ddyx__istz) for ddyx__istz in
        range(len(mli__xmmgp)))
    left_other_types = tuple([typemap[yip__ppr.name] for yip__ppr in okj__suh])
    right_other_types = tuple([typemap[yip__ppr.name] for yip__ppr in
        mli__xmmgp])
    left_key_names = tuple('t1_key' + str(ddyx__istz) for ddyx__istz in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(ddyx__istz) for ddyx__istz in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(udpu__jey[0
        ]) if len(udpu__jey) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[lcdcr__nvwy.name] for lcdcr__nvwy in
        tovsp__mgxqw)
    right_key_types = tuple(typemap[lcdcr__nvwy.name] for lcdcr__nvwy in
        hxgm__zqvmf)
    for ddyx__istz in range(n_keys):
        glbs[f'key_type_{ddyx__istz}'] = _match_join_key_types(left_key_types
            [ddyx__istz], right_key_types[ddyx__istz], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[ddyx__istz]}, key_type_{ddyx__istz})'
         for ddyx__istz in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[ddyx__istz]}, key_type_{ddyx__istz})'
         for ddyx__istz in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            zxrri__vpcim = str(cname) + join_node.suffix_left
        else:
            zxrri__vpcim = cname
        assert zxrri__vpcim in join_node.out_data_vars
        wgqq__gzbls.append(join_node.out_data_vars[zxrri__vpcim])
    for ddyx__istz, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[ddyx__istz] and not join_node.is_join:
            if cname in join_node.add_suffix:
                zxrri__vpcim = str(cname) + join_node.suffix_right
            else:
                zxrri__vpcim = cname
            assert zxrri__vpcim in join_node.out_data_vars
            wgqq__gzbls.append(join_node.out_data_vars[zxrri__vpcim])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                zxrri__vpcim = str(cname) + join_node.suffix_left
            else:
                zxrri__vpcim = str(cname) + join_node.suffix_right
        else:
            zxrri__vpcim = cname
        return join_node.out_data_vars[zxrri__vpcim]
    for dgww__wwh in sorted(join_node.left_vars.keys(), key=lambda a: str(a)):
        if dgww__wwh not in join_node.left_key_set:
            wgqq__gzbls.append(_get_out_col_var(dgww__wwh, True))
    for dgww__wwh in sorted(join_node.right_vars.keys(), key=lambda a: str(a)):
        if dgww__wwh not in join_node.right_key_set:
            wgqq__gzbls.append(_get_out_col_var(dgww__wwh, False))
    if join_node.indicator:
        wgqq__gzbls.append(_get_out_col_var('_merge', False))
    bfsw__vwt = [('t3_c' + str(ddyx__istz)) for ddyx__istz in range(len(
        wgqq__gzbls))]
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel, 'pd.merge_asof requires both left and right to be replicated or distributed'
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_local_hash_join(optional_column, left_key_names,
            right_key_names, left_key_types, right_key_types,
            left_other_names, right_other_names, left_other_types,
            right_other_types, join_node.vect_same_key, join_node.is_left,
            join_node.is_right, join_node.is_join, left_parallel,
            right_parallel, glbs, [typemap[lcdcr__nvwy.name] for
            lcdcr__nvwy in wgqq__gzbls], join_node.loc, join_node.indicator,
            join_node.is_na_equal, general_cond_cfunc, left_col_nums,
            right_col_nums)
    if join_node.how == 'asof':
        for ddyx__istz in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(ddyx__istz,
                ddyx__istz)
        for ddyx__istz in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                ddyx__istz, ddyx__istz)
        for ddyx__istz in range(n_keys):
            func_text += (
                f'    t1_keys_{ddyx__istz} = out_t1_keys[{ddyx__istz}]\n')
        for ddyx__istz in range(n_keys):
            func_text += (
                f'    t2_keys_{ddyx__istz} = out_t2_keys[{ddyx__istz}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {bfsw__vwt[idx]} = opti_0\n'
        idx += 1
    for ddyx__istz in range(n_keys):
        func_text += f'    {bfsw__vwt[idx]} = t1_keys_{ddyx__istz}\n'
        idx += 1
    for ddyx__istz in range(n_keys):
        if not join_node.vect_same_key[ddyx__istz] and not join_node.is_join:
            func_text += f'    {bfsw__vwt[idx]} = t2_keys_{ddyx__istz}\n'
            idx += 1
    for ddyx__istz in range(len(left_other_names)):
        func_text += f'    {bfsw__vwt[idx]} = left_{ddyx__istz}\n'
        idx += 1
    for ddyx__istz in range(len(right_other_names)):
        func_text += f'    {bfsw__vwt[idx]} = right_{ddyx__istz}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {bfsw__vwt[idx]} = indicator_col\n'
        idx += 1
    irpsk__ifs = {}
    exec(func_text, {}, irpsk__ifs)
    eedjk__ner = irpsk__ifs['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'hash_join_table':
        hash_join_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    ydwh__bjmn = compile_to_numba_ir(eedjk__ner, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=flrqh__iafhs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ydwh__bjmn, kfgh__ixyp)
    ekc__dfp = ydwh__bjmn.body[:-3]
    for ddyx__istz in range(len(wgqq__gzbls)):
        ekc__dfp[-len(wgqq__gzbls) + ddyx__istz].target = wgqq__gzbls[
            ddyx__istz]
    return ekc__dfp


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    kfib__apj = next_label()
    wxlt__qcd = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    vxon__epb = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{kfib__apj}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        wxlt__qcd, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        vxon__epb, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    irpsk__ifs = {}
    exec(func_text, table_getitem_funcs, irpsk__ifs)
    eeey__wbr = irpsk__ifs[f'bodo_join_gen_cond{kfib__apj}']
    kulh__adzow = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    djtmk__megl = numba.cfunc(kulh__adzow, nopython=True)(eeey__wbr)
    join_gen_cond_cfunc[djtmk__megl.native_name] = djtmk__megl
    join_gen_cond_cfunc_addr[djtmk__megl.native_name] = djtmk__megl.address
    return djtmk__megl, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    lsnx__roos = []
    for yip__ppr, igg__bahk in col_to_ind.items():
        cname = f'({table_name}.{yip__ppr})'
        if cname not in expr:
            continue
        evz__jqo = f'getitem_{table_name}_val_{igg__bahk}'
        zkb__ivv = f'_bodo_{table_name}_val_{igg__bahk}'
        hkz__jxwl = typemap[col_vars[yip__ppr].name]
        if is_str_arr_type(hkz__jxwl):
            func_text += f"""  {zkb__ivv}, {zkb__ivv}_size = {evz__jqo}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {zkb__ivv} = bodo.libs.str_arr_ext.decode_utf8({zkb__ivv}, {zkb__ivv}_size)
"""
        else:
            func_text += (
                f'  {zkb__ivv} = {evz__jqo}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[evz__jqo
            ] = bodo.libs.array._gen_row_access_intrinsic(hkz__jxwl, igg__bahk)
        expr = expr.replace(cname, zkb__ivv)
        zmrp__idukz = f'({na_check_name}.{table_name}.{yip__ppr})'
        if zmrp__idukz in expr:
            hlnr__mkyrd = f'nacheck_{table_name}_val_{igg__bahk}'
            ozf__mtx = f'_bodo_isna_{table_name}_val_{igg__bahk}'
            if (isinstance(hkz__jxwl, bodo.libs.int_arr_ext.
                IntegerArrayType) or hkz__jxwl == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(hkz__jxwl)):
                func_text += f"""  {ozf__mtx} = {hlnr__mkyrd}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {ozf__mtx} = {hlnr__mkyrd}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[hlnr__mkyrd
                ] = bodo.libs.array._gen_row_na_check_intrinsic(hkz__jxwl,
                igg__bahk)
            expr = expr.replace(zmrp__idukz, ozf__mtx)
        if igg__bahk >= n_keys:
            lsnx__roos.append(igg__bahk)
    return expr, func_text, lsnx__roos


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {yip__ppr: ddyx__istz for ddyx__istz, yip__ppr in
        enumerate(key_names)}
    ddyx__istz = n_keys
    for yip__ppr in sorted(col_vars, key=lambda a: str(a)):
        if yip__ppr in col_to_ind:
            continue
        col_to_ind[yip__ppr] = ddyx__istz
        ddyx__istz += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as ihi__zadd:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    mdwt__bphrj = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[lcdcr__nvwy.name] in mdwt__bphrj for
        lcdcr__nvwy in join_node.left_vars.values())
    right_parallel = all(array_dists[lcdcr__nvwy.name] in mdwt__bphrj for
        lcdcr__nvwy in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[lcdcr__nvwy.name] in mdwt__bphrj for
            lcdcr__nvwy in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[lcdcr__nvwy.name] in mdwt__bphrj for
            lcdcr__nvwy in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[lcdcr__nvwy.name] in mdwt__bphrj for
            lcdcr__nvwy in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    clte__fkhp = []
    for ddyx__istz in range(len(left_key_names)):
        xhf__dhe = _match_join_key_types(left_key_types[ddyx__istz],
            right_key_types[ddyx__istz], loc)
        clte__fkhp.append(needs_typechange(xhf__dhe, is_right,
            vect_same_key[ddyx__istz]))
    for ddyx__istz in range(len(left_other_names)):
        clte__fkhp.append(needs_typechange(left_other_types[ddyx__istz],
            is_right, False))
    for ddyx__istz in range(len(right_key_names)):
        if not vect_same_key[ddyx__istz] and not is_join:
            xhf__dhe = _match_join_key_types(left_key_types[ddyx__istz],
                right_key_types[ddyx__istz], loc)
            clte__fkhp.append(needs_typechange(xhf__dhe, is_left, False))
    for ddyx__istz in range(len(right_other_names)):
        clte__fkhp.append(needs_typechange(right_other_types[ddyx__istz],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                vzp__gstv = IntDtype(in_type.dtype).name
                assert vzp__gstv.endswith('Dtype()')
                vzp__gstv = vzp__gstv[:-7]
                usm__hfo = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{vzp__gstv}"))
"""
                prww__qur = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                usm__hfo = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                prww__qur = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            usm__hfo = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            prww__qur = f'typ_{idx}'
        else:
            usm__hfo = ''
            prww__qur = in_name
        return usm__hfo, prww__qur
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    bfi__fbid = []
    for ddyx__istz in range(n_keys):
        bfi__fbid.append('t1_keys[{}]'.format(ddyx__istz))
    for ddyx__istz in range(len(left_other_names)):
        bfi__fbid.append('data_left[{}]'.format(ddyx__istz))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in bfi__fbid))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    neep__jhe = []
    for ddyx__istz in range(n_keys):
        neep__jhe.append('t2_keys[{}]'.format(ddyx__istz))
    for ddyx__istz in range(len(right_other_names)):
        neep__jhe.append('data_right[{}]'.format(ddyx__istz))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in neep__jhe))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        rvtz__irp else '0' for rvtz__irp in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if rvtz__irp else '0' for rvtz__irp in clte__fkhp))
    func_text += f"""    left_table_cond_columns = np.array({left_col_nums if len(left_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    func_text += f"""    right_table_cond_columns = np.array({right_col_nums if len(right_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += (
        """    out_table = hash_join_table(table_left, table_right, {}, {}, {}, {}, {}, vect_same_key.ctypes, vect_need_typechange.ctypes, {}, {}, {}, {}, {}, {}, cfunc_cond, left_table_cond_columns.ctypes, {}, right_table_cond_columns.ctypes, {})
"""
        .format(left_parallel, right_parallel, n_keys, len(left_other_names
        ), len(right_other_names), is_left, is_right, is_join,
        optional_column, indicator, is_na_equal, len(left_col_nums), len(
        right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    idx = 0
    if optional_column:
        lsagr__wvd = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += lsagr__wvd[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {lsagr__wvd[1]})
"""
        idx += 1
    for ddyx__istz, hshxq__ytlyy in enumerate(left_key_names):
        xhf__dhe = _match_join_key_types(left_key_types[ddyx__istz],
            right_key_types[ddyx__istz], loc)
        lsagr__wvd = get_out_type(idx, xhf__dhe, f't1_keys[{ddyx__istz}]',
            is_right, vect_same_key[ddyx__istz])
        func_text += lsagr__wvd[0]
        func_text += f"""    t1_keys_{ddyx__istz} = info_to_array(info_from_table(out_table, {idx}), {lsagr__wvd[1]})
"""
        idx += 1
    for ddyx__istz, hshxq__ytlyy in enumerate(left_other_names):
        lsagr__wvd = get_out_type(idx, left_other_types[ddyx__istz],
            hshxq__ytlyy, is_right, False)
        func_text += lsagr__wvd[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(ddyx__istz, idx, lsagr__wvd[1]))
        idx += 1
    for ddyx__istz, hshxq__ytlyy in enumerate(right_key_names):
        if not vect_same_key[ddyx__istz] and not is_join:
            xhf__dhe = _match_join_key_types(left_key_types[ddyx__istz],
                right_key_types[ddyx__istz], loc)
            lsagr__wvd = get_out_type(idx, xhf__dhe,
                f't2_keys[{ddyx__istz}]', is_left, False)
            func_text += lsagr__wvd[0]
            func_text += f"""    t2_keys_{ddyx__istz} = info_to_array(info_from_table(out_table, {idx}), {lsagr__wvd[1]})
"""
            idx += 1
    for ddyx__istz, hshxq__ytlyy in enumerate(right_other_names):
        lsagr__wvd = get_out_type(idx, right_other_types[ddyx__istz],
            hshxq__ytlyy, is_left, False)
        func_text += lsagr__wvd[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(ddyx__istz, idx, lsagr__wvd[1]))
        idx += 1
    if indicator:
        func_text += f"""    typ_{idx} = pd.Categorical(values=['both'], categories=('left_only', 'right_only', 'both'))
"""
        func_text += f"""    indicator_col = info_to_array(info_from_table(out_table, {idx}), typ_{idx})
"""
        idx += 1
    func_text += '    delete_table(out_table)\n'
    return func_text


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    hkh__zmxn = bodo.libs.distributed_api.get_size()
    magy__wub = np.empty(hkh__zmxn, left_key_arrs[0].dtype)
    rfh__iaz = np.empty(hkh__zmxn, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(magy__wub, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(rfh__iaz, left_key_arrs[0][-1])
    pwktz__dtf = np.zeros(hkh__zmxn, np.int32)
    zlzna__cnb = np.zeros(hkh__zmxn, np.int32)
    vizr__pji = np.zeros(hkh__zmxn, np.int32)
    iydxz__aofff = right_key_arrs[0][0]
    auquu__nqpbf = right_key_arrs[0][-1]
    rgn__kqr = -1
    ddyx__istz = 0
    while ddyx__istz < hkh__zmxn - 1 and rfh__iaz[ddyx__istz] < iydxz__aofff:
        ddyx__istz += 1
    while ddyx__istz < hkh__zmxn and magy__wub[ddyx__istz] <= auquu__nqpbf:
        rgn__kqr, borb__tth = _count_overlap(right_key_arrs[0], magy__wub[
            ddyx__istz], rfh__iaz[ddyx__istz])
        if rgn__kqr != 0:
            rgn__kqr -= 1
            borb__tth += 1
        pwktz__dtf[ddyx__istz] = borb__tth
        zlzna__cnb[ddyx__istz] = rgn__kqr
        ddyx__istz += 1
    while ddyx__istz < hkh__zmxn:
        pwktz__dtf[ddyx__istz] = 1
        zlzna__cnb[ddyx__istz] = len(right_key_arrs[0]) - 1
        ddyx__istz += 1
    bodo.libs.distributed_api.alltoall(pwktz__dtf, vizr__pji, 1)
    wclv__pqjb = vizr__pji.sum()
    jawi__eip = np.empty(wclv__pqjb, right_key_arrs[0].dtype)
    fuwyl__nusek = alloc_arr_tup(wclv__pqjb, right_data)
    tjgp__ylt = bodo.ir.join.calc_disp(vizr__pji)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], jawi__eip,
        pwktz__dtf, vizr__pji, zlzna__cnb, tjgp__ylt)
    bodo.libs.distributed_api.alltoallv_tup(right_data, fuwyl__nusek,
        pwktz__dtf, vizr__pji, zlzna__cnb, tjgp__ylt)
    return (jawi__eip,), fuwyl__nusek


@numba.njit
def _count_overlap(r_key_arr, start, end):
    borb__tth = 0
    rgn__kqr = 0
    xpag__wrjoh = 0
    while xpag__wrjoh < len(r_key_arr) and r_key_arr[xpag__wrjoh] < start:
        rgn__kqr += 1
        xpag__wrjoh += 1
    while xpag__wrjoh < len(r_key_arr) and start <= r_key_arr[xpag__wrjoh
        ] <= end:
        xpag__wrjoh += 1
        borb__tth += 1
    return rgn__kqr, borb__tth


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    jiha__yifqs = np.empty_like(arr)
    jiha__yifqs[0] = 0
    for ddyx__istz in range(1, len(arr)):
        jiha__yifqs[ddyx__istz] = jiha__yifqs[ddyx__istz - 1] + arr[
            ddyx__istz - 1]
    return jiha__yifqs


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    prw__iux = len(left_keys[0])
    jhn__ofhz = len(right_keys[0])
    uxz__awze = alloc_arr_tup(prw__iux, left_keys)
    hhmtg__hje = alloc_arr_tup(prw__iux, right_keys)
    gtf__gpxlq = alloc_arr_tup(prw__iux, data_left)
    idp__gfp = alloc_arr_tup(prw__iux, data_right)
    rcnod__mhrgm = 0
    aqrj__pccb = 0
    for rcnod__mhrgm in range(prw__iux):
        if aqrj__pccb < 0:
            aqrj__pccb = 0
        while aqrj__pccb < jhn__ofhz and getitem_arr_tup(right_keys, aqrj__pccb
            ) <= getitem_arr_tup(left_keys, rcnod__mhrgm):
            aqrj__pccb += 1
        aqrj__pccb -= 1
        setitem_arr_tup(uxz__awze, rcnod__mhrgm, getitem_arr_tup(left_keys,
            rcnod__mhrgm))
        setitem_arr_tup(gtf__gpxlq, rcnod__mhrgm, getitem_arr_tup(data_left,
            rcnod__mhrgm))
        if aqrj__pccb >= 0:
            setitem_arr_tup(hhmtg__hje, rcnod__mhrgm, getitem_arr_tup(
                right_keys, aqrj__pccb))
            setitem_arr_tup(idp__gfp, rcnod__mhrgm, getitem_arr_tup(
                data_right, aqrj__pccb))
        else:
            bodo.libs.array_kernels.setna_tup(hhmtg__hje, rcnod__mhrgm)
            bodo.libs.array_kernels.setna_tup(idp__gfp, rcnod__mhrgm)
    return uxz__awze, hhmtg__hje, gtf__gpxlq, idp__gfp
