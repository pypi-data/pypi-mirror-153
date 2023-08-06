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
        dcprb__jdd = func.signature
        sjn__ezjk = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        edh__ovui = cgutils.get_or_insert_function(builder.module,
            sjn__ezjk, sym._literal_value)
        builder.call(edh__ovui, [context.get_constant_null(dcprb__jdd.args[
            0]), context.get_constant_null(dcprb__jdd.args[1]), context.
            get_constant_null(dcprb__jdd.args[2]), context.
            get_constant_null(dcprb__jdd.args[3]), context.
            get_constant_null(dcprb__jdd.args[4]), context.
            get_constant_null(dcprb__jdd.args[5]), context.get_constant(
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
            self.left_cond_cols = set(wgct__daou for wgct__daou in
                left_vars.keys() if f'(left.{wgct__daou})' in gen_cond_expr)
            self.right_cond_cols = set(wgct__daou for wgct__daou in
                right_vars.keys() if f'(right.{wgct__daou})' in gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        qwuzr__vmh = self.left_key_set & self.right_key_set
        duo__jil = set(left_vars.keys()) & set(right_vars.keys())
        pre__ydzu = duo__jil - qwuzr__vmh
        vect_same_key = []
        n_keys = len(left_keys)
        for yyt__ebl in range(n_keys):
            uoc__nqmjj = left_keys[yyt__ebl]
            kcy__lwtzj = right_keys[yyt__ebl]
            vect_same_key.append(uoc__nqmjj == kcy__lwtzj)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(wgct__daou) + suffix_left if wgct__daou in
            pre__ydzu else wgct__daou): ('left', wgct__daou) for wgct__daou in
            left_vars.keys()}
        self.column_origins.update({(str(wgct__daou) + suffix_right if 
            wgct__daou in pre__ydzu else wgct__daou): ('right', wgct__daou) for
            wgct__daou in right_vars.keys()})
        if '$_bodo_index_' in pre__ydzu:
            pre__ydzu.remove('$_bodo_index_')
        self.add_suffix = pre__ydzu

    def __repr__(self):
        gcn__zmj = ''
        for wgct__daou, ycxqh__byfet in self.out_data_vars.items():
            gcn__zmj += "'{}':{}, ".format(wgct__daou, ycxqh__byfet.name)
        isk__wvx = '{}{{{}}}'.format(self.df_out, gcn__zmj)
        gaq__crpru = ''
        for wgct__daou, ycxqh__byfet in self.left_vars.items():
            gaq__crpru += "'{}':{}, ".format(wgct__daou, ycxqh__byfet.name)
        cuunu__yqke = '{}{{{}}}'.format(self.left_df, gaq__crpru)
        gaq__crpru = ''
        for wgct__daou, ycxqh__byfet in self.right_vars.items():
            gaq__crpru += "'{}':{}, ".format(wgct__daou, ycxqh__byfet.name)
        nbvu__dsq = '{}{{{}}}'.format(self.right_df, gaq__crpru)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, isk__wvx, cuunu__yqke, nbvu__dsq)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    gpkdg__rzenj = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    njdnk__qju = []
    puph__gia = list(join_node.left_vars.values())
    for ckjt__stkfn in puph__gia:
        aexkk__bqer = typemap[ckjt__stkfn.name]
        ivc__rte = equiv_set.get_shape(ckjt__stkfn)
        if ivc__rte:
            njdnk__qju.append(ivc__rte[0])
    if len(njdnk__qju) > 1:
        equiv_set.insert_equiv(*njdnk__qju)
    njdnk__qju = []
    puph__gia = list(join_node.right_vars.values())
    for ckjt__stkfn in puph__gia:
        aexkk__bqer = typemap[ckjt__stkfn.name]
        ivc__rte = equiv_set.get_shape(ckjt__stkfn)
        if ivc__rte:
            njdnk__qju.append(ivc__rte[0])
    if len(njdnk__qju) > 1:
        equiv_set.insert_equiv(*njdnk__qju)
    njdnk__qju = []
    for ckjt__stkfn in join_node.out_data_vars.values():
        aexkk__bqer = typemap[ckjt__stkfn.name]
        teafj__glpyn = array_analysis._gen_shape_call(equiv_set,
            ckjt__stkfn, aexkk__bqer.ndim, None, gpkdg__rzenj)
        equiv_set.insert_equiv(ckjt__stkfn, teafj__glpyn)
        njdnk__qju.append(teafj__glpyn[0])
        equiv_set.define(ckjt__stkfn, set())
    if len(njdnk__qju) > 1:
        equiv_set.insert_equiv(*njdnk__qju)
    return [], gpkdg__rzenj


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    qell__ciev = Distribution.OneD
    lnfy__wnyge = Distribution.OneD
    for ckjt__stkfn in join_node.left_vars.values():
        qell__ciev = Distribution(min(qell__ciev.value, array_dists[
            ckjt__stkfn.name].value))
    for ckjt__stkfn in join_node.right_vars.values():
        lnfy__wnyge = Distribution(min(lnfy__wnyge.value, array_dists[
            ckjt__stkfn.name].value))
    ywrmb__wnb = Distribution.OneD_Var
    for ckjt__stkfn in join_node.out_data_vars.values():
        if ckjt__stkfn.name in array_dists:
            ywrmb__wnb = Distribution(min(ywrmb__wnb.value, array_dists[
                ckjt__stkfn.name].value))
    ekzxl__oyia = Distribution(min(ywrmb__wnb.value, qell__ciev.value))
    nnq__gmcoj = Distribution(min(ywrmb__wnb.value, lnfy__wnyge.value))
    ywrmb__wnb = Distribution(max(ekzxl__oyia.value, nnq__gmcoj.value))
    for ckjt__stkfn in join_node.out_data_vars.values():
        array_dists[ckjt__stkfn.name] = ywrmb__wnb
    if ywrmb__wnb != Distribution.OneD_Var:
        qell__ciev = ywrmb__wnb
        lnfy__wnyge = ywrmb__wnb
    for ckjt__stkfn in join_node.left_vars.values():
        array_dists[ckjt__stkfn.name] = qell__ciev
    for ckjt__stkfn in join_node.right_vars.values():
        array_dists[ckjt__stkfn.name] = lnfy__wnyge
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    for kzg__yji, ksus__drkt in join_node.out_data_vars.items():
        if join_node.indicator and kzg__yji == '_merge':
            continue
        if not kzg__yji in join_node.column_origins:
            raise BodoError('join(): The variable ' + kzg__yji +
                ' is absent from the output')
        lic__yxqy = join_node.column_origins[kzg__yji]
        if lic__yxqy[0] == 'left':
            ckjt__stkfn = join_node.left_vars[lic__yxqy[1]]
        else:
            ckjt__stkfn = join_node.right_vars[lic__yxqy[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=ksus__drkt.
            name, src=ckjt__stkfn.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for hvoaa__kbyp in list(join_node.left_vars.keys()):
        join_node.left_vars[hvoaa__kbyp] = visit_vars_inner(join_node.
            left_vars[hvoaa__kbyp], callback, cbdata)
    for hvoaa__kbyp in list(join_node.right_vars.keys()):
        join_node.right_vars[hvoaa__kbyp] = visit_vars_inner(join_node.
            right_vars[hvoaa__kbyp], callback, cbdata)
    for hvoaa__kbyp in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[hvoaa__kbyp] = visit_vars_inner(join_node.
            out_data_vars[hvoaa__kbyp], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    bkxr__iyskc = []
    ydk__cwn = True
    for hvoaa__kbyp, ckjt__stkfn in join_node.out_data_vars.items():
        if ckjt__stkfn.name in lives:
            ydk__cwn = False
            continue
        if hvoaa__kbyp == '$_bodo_index_':
            continue
        if join_node.indicator and hvoaa__kbyp == '_merge':
            bkxr__iyskc.append('_merge')
            join_node.indicator = False
            continue
        nsg__kmvd, jmra__ivfiz = join_node.column_origins[hvoaa__kbyp]
        if (nsg__kmvd == 'left' and jmra__ivfiz not in join_node.
            left_key_set and jmra__ivfiz not in join_node.left_cond_cols):
            join_node.left_vars.pop(jmra__ivfiz)
            bkxr__iyskc.append(hvoaa__kbyp)
        if (nsg__kmvd == 'right' and jmra__ivfiz not in join_node.
            right_key_set and jmra__ivfiz not in join_node.right_cond_cols):
            join_node.right_vars.pop(jmra__ivfiz)
            bkxr__iyskc.append(hvoaa__kbyp)
    for cname in bkxr__iyskc:
        join_node.out_data_vars.pop(cname)
    if ydk__cwn:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({ycxqh__byfet.name for ycxqh__byfet in join_node.
        left_vars.values()})
    use_set.update({ycxqh__byfet.name for ycxqh__byfet in join_node.
        right_vars.values()})
    def_set.update({ycxqh__byfet.name for ycxqh__byfet in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    hyj__wdigi = set(ycxqh__byfet.name for ycxqh__byfet in join_node.
        out_data_vars.values())
    return set(), hyj__wdigi


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for hvoaa__kbyp in list(join_node.left_vars.keys()):
        join_node.left_vars[hvoaa__kbyp] = replace_vars_inner(join_node.
            left_vars[hvoaa__kbyp], var_dict)
    for hvoaa__kbyp in list(join_node.right_vars.keys()):
        join_node.right_vars[hvoaa__kbyp] = replace_vars_inner(join_node.
            right_vars[hvoaa__kbyp], var_dict)
    for hvoaa__kbyp in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[hvoaa__kbyp] = replace_vars_inner(join_node
            .out_data_vars[hvoaa__kbyp], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ckjt__stkfn in join_node.out_data_vars.values():
        definitions[ckjt__stkfn.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    xiex__cuhbt = tuple(join_node.left_vars[wgct__daou] for wgct__daou in
        join_node.left_keys)
    iwgzl__dsxx = tuple(join_node.right_vars[wgct__daou] for wgct__daou in
        join_node.right_keys)
    left_vars = join_node.left_vars
    right_vars = join_node.right_vars
    pibl__vkx = ()
    dcyns__mii = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        kzm__qba = join_node.right_keys[0]
        if kzm__qba in left_vars:
            dcyns__mii = kzm__qba,
            pibl__vkx = join_node.right_vars[kzm__qba],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        kzm__qba = join_node.left_keys[0]
        if kzm__qba in right_vars:
            dcyns__mii = kzm__qba,
            pibl__vkx = join_node.left_vars[kzm__qba],
            optional_column = True
    iiqbd__hxyl = [join_node.out_data_vars[cname] for cname in dcyns__mii]
    fnfvs__omu = tuple(ycxqh__byfet for jjox__uuuq, ycxqh__byfet in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if jjox__uuuq
         not in join_node.left_key_set)
    rmea__kcpcu = tuple(ycxqh__byfet for jjox__uuuq, ycxqh__byfet in sorted
        (join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        jjox__uuuq not in join_node.right_key_set)
    zpwv__lbome = (pibl__vkx + xiex__cuhbt + iwgzl__dsxx + fnfvs__omu +
        rmea__kcpcu)
    bmpio__opuse = tuple(typemap[ycxqh__byfet.name] for ycxqh__byfet in
        zpwv__lbome)
    qfawh__qwc = tuple('opti_c' + str(bywp__jorvh) for bywp__jorvh in range
        (len(pibl__vkx)))
    left_other_names = tuple('t1_c' + str(bywp__jorvh) for bywp__jorvh in
        range(len(fnfvs__omu)))
    right_other_names = tuple('t2_c' + str(bywp__jorvh) for bywp__jorvh in
        range(len(rmea__kcpcu)))
    left_other_types = tuple([typemap[wgct__daou.name] for wgct__daou in
        fnfvs__omu])
    right_other_types = tuple([typemap[wgct__daou.name] for wgct__daou in
        rmea__kcpcu])
    left_key_names = tuple('t1_key' + str(bywp__jorvh) for bywp__jorvh in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(bywp__jorvh) for bywp__jorvh in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(qfawh__qwc[
        0]) if len(qfawh__qwc) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[ycxqh__byfet.name] for ycxqh__byfet in
        xiex__cuhbt)
    right_key_types = tuple(typemap[ycxqh__byfet.name] for ycxqh__byfet in
        iwgzl__dsxx)
    for bywp__jorvh in range(n_keys):
        glbs[f'key_type_{bywp__jorvh}'] = _match_join_key_types(left_key_types
            [bywp__jorvh], right_key_types[bywp__jorvh], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[bywp__jorvh]}, key_type_{bywp__jorvh})'
         for bywp__jorvh in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[bywp__jorvh]}, key_type_{bywp__jorvh})'
         for bywp__jorvh in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            jtwj__uumm = str(cname) + join_node.suffix_left
        else:
            jtwj__uumm = cname
        assert jtwj__uumm in join_node.out_data_vars
        iiqbd__hxyl.append(join_node.out_data_vars[jtwj__uumm])
    for bywp__jorvh, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[bywp__jorvh] and not join_node.is_join:
            if cname in join_node.add_suffix:
                jtwj__uumm = str(cname) + join_node.suffix_right
            else:
                jtwj__uumm = cname
            assert jtwj__uumm in join_node.out_data_vars
            iiqbd__hxyl.append(join_node.out_data_vars[jtwj__uumm])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                jtwj__uumm = str(cname) + join_node.suffix_left
            else:
                jtwj__uumm = str(cname) + join_node.suffix_right
        else:
            jtwj__uumm = cname
        return join_node.out_data_vars[jtwj__uumm]
    for jjox__uuuq in sorted(join_node.left_vars.keys(), key=lambda a: str(a)):
        if jjox__uuuq not in join_node.left_key_set:
            iiqbd__hxyl.append(_get_out_col_var(jjox__uuuq, True))
    for jjox__uuuq in sorted(join_node.right_vars.keys(), key=lambda a: str(a)
        ):
        if jjox__uuuq not in join_node.right_key_set:
            iiqbd__hxyl.append(_get_out_col_var(jjox__uuuq, False))
    if join_node.indicator:
        iiqbd__hxyl.append(_get_out_col_var('_merge', False))
    lyv__pqp = [('t3_c' + str(bywp__jorvh)) for bywp__jorvh in range(len(
        iiqbd__hxyl))]
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
            right_parallel, glbs, [typemap[ycxqh__byfet.name] for
            ycxqh__byfet in iiqbd__hxyl], join_node.loc, join_node.
            indicator, join_node.is_na_equal, general_cond_cfunc,
            left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for bywp__jorvh in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(bywp__jorvh
                , bywp__jorvh)
        for bywp__jorvh in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                bywp__jorvh, bywp__jorvh)
        for bywp__jorvh in range(n_keys):
            func_text += (
                f'    t1_keys_{bywp__jorvh} = out_t1_keys[{bywp__jorvh}]\n')
        for bywp__jorvh in range(n_keys):
            func_text += (
                f'    t2_keys_{bywp__jorvh} = out_t2_keys[{bywp__jorvh}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {lyv__pqp[idx]} = opti_0\n'
        idx += 1
    for bywp__jorvh in range(n_keys):
        func_text += f'    {lyv__pqp[idx]} = t1_keys_{bywp__jorvh}\n'
        idx += 1
    for bywp__jorvh in range(n_keys):
        if not join_node.vect_same_key[bywp__jorvh] and not join_node.is_join:
            func_text += f'    {lyv__pqp[idx]} = t2_keys_{bywp__jorvh}\n'
            idx += 1
    for bywp__jorvh in range(len(left_other_names)):
        func_text += f'    {lyv__pqp[idx]} = left_{bywp__jorvh}\n'
        idx += 1
    for bywp__jorvh in range(len(right_other_names)):
        func_text += f'    {lyv__pqp[idx]} = right_{bywp__jorvh}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {lyv__pqp[idx]} = indicator_col\n'
        idx += 1
    qzq__ecb = {}
    exec(func_text, {}, qzq__ecb)
    wohb__dfr = qzq__ecb['f']
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
    wlio__pska = compile_to_numba_ir(wohb__dfr, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=bmpio__opuse, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(wlio__pska, zpwv__lbome)
    dzfxh__gcf = wlio__pska.body[:-3]
    for bywp__jorvh in range(len(iiqbd__hxyl)):
        dzfxh__gcf[-len(iiqbd__hxyl) + bywp__jorvh].target = iiqbd__hxyl[
            bywp__jorvh]
    return dzfxh__gcf


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    igeyj__sza = next_label()
    edy__bcc = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    qzis__gwoc = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{igeyj__sza}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        edy__bcc, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        qzis__gwoc, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    qzq__ecb = {}
    exec(func_text, table_getitem_funcs, qzq__ecb)
    kbyb__kjtzf = qzq__ecb[f'bodo_join_gen_cond{igeyj__sza}']
    uyod__rli = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    kfy__tei = numba.cfunc(uyod__rli, nopython=True)(kbyb__kjtzf)
    join_gen_cond_cfunc[kfy__tei.native_name] = kfy__tei
    join_gen_cond_cfunc_addr[kfy__tei.native_name] = kfy__tei.address
    return kfy__tei, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    imxpe__rim = []
    for wgct__daou, kuv__lkklp in col_to_ind.items():
        cname = f'({table_name}.{wgct__daou})'
        if cname not in expr:
            continue
        aet__ssqv = f'getitem_{table_name}_val_{kuv__lkklp}'
        egqt__luv = f'_bodo_{table_name}_val_{kuv__lkklp}'
        qqes__rpjd = typemap[col_vars[wgct__daou].name]
        if is_str_arr_type(qqes__rpjd):
            func_text += f"""  {egqt__luv}, {egqt__luv}_size = {aet__ssqv}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {egqt__luv} = bodo.libs.str_arr_ext.decode_utf8({egqt__luv}, {egqt__luv}_size)
"""
        else:
            func_text += (
                f'  {egqt__luv} = {aet__ssqv}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[aet__ssqv
            ] = bodo.libs.array._gen_row_access_intrinsic(qqes__rpjd,
            kuv__lkklp)
        expr = expr.replace(cname, egqt__luv)
        gfftq__ksr = f'({na_check_name}.{table_name}.{wgct__daou})'
        if gfftq__ksr in expr:
            ftj__hzeq = f'nacheck_{table_name}_val_{kuv__lkklp}'
            doij__qghi = f'_bodo_isna_{table_name}_val_{kuv__lkklp}'
            if (isinstance(qqes__rpjd, bodo.libs.int_arr_ext.
                IntegerArrayType) or qqes__rpjd == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(qqes__rpjd)):
                func_text += f"""  {doij__qghi} = {ftj__hzeq}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {doij__qghi} = {ftj__hzeq}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[ftj__hzeq
                ] = bodo.libs.array._gen_row_na_check_intrinsic(qqes__rpjd,
                kuv__lkklp)
            expr = expr.replace(gfftq__ksr, doij__qghi)
        if kuv__lkklp >= n_keys:
            imxpe__rim.append(kuv__lkklp)
    return expr, func_text, imxpe__rim


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {wgct__daou: bywp__jorvh for bywp__jorvh, wgct__daou in
        enumerate(key_names)}
    bywp__jorvh = n_keys
    for wgct__daou in sorted(col_vars, key=lambda a: str(a)):
        if wgct__daou in col_to_ind:
            continue
        col_to_ind[wgct__daou] = bywp__jorvh
        bywp__jorvh += 1
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
    except Exception as tye__cyq:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    knwm__cvq = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[ycxqh__byfet.name] in knwm__cvq for
        ycxqh__byfet in join_node.left_vars.values())
    right_parallel = all(array_dists[ycxqh__byfet.name] in knwm__cvq for
        ycxqh__byfet in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[ycxqh__byfet.name] in knwm__cvq for
            ycxqh__byfet in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[ycxqh__byfet.name] in knwm__cvq for
            ycxqh__byfet in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[ycxqh__byfet.name] in knwm__cvq for
            ycxqh__byfet in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    tvoi__dexdr = []
    for bywp__jorvh in range(len(left_key_names)):
        tjqkm__qav = _match_join_key_types(left_key_types[bywp__jorvh],
            right_key_types[bywp__jorvh], loc)
        tvoi__dexdr.append(needs_typechange(tjqkm__qav, is_right,
            vect_same_key[bywp__jorvh]))
    for bywp__jorvh in range(len(left_other_names)):
        tvoi__dexdr.append(needs_typechange(left_other_types[bywp__jorvh],
            is_right, False))
    for bywp__jorvh in range(len(right_key_names)):
        if not vect_same_key[bywp__jorvh] and not is_join:
            tjqkm__qav = _match_join_key_types(left_key_types[bywp__jorvh],
                right_key_types[bywp__jorvh], loc)
            tvoi__dexdr.append(needs_typechange(tjqkm__qav, is_left, False))
    for bywp__jorvh in range(len(right_other_names)):
        tvoi__dexdr.append(needs_typechange(right_other_types[bywp__jorvh],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                bwjhg__wkl = IntDtype(in_type.dtype).name
                assert bwjhg__wkl.endswith('Dtype()')
                bwjhg__wkl = bwjhg__wkl[:-7]
                yca__wnnv = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{bwjhg__wkl}"))
"""
                ipip__soxr = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                yca__wnnv = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                ipip__soxr = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            yca__wnnv = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            ipip__soxr = f'typ_{idx}'
        else:
            yca__wnnv = ''
            ipip__soxr = in_name
        return yca__wnnv, ipip__soxr
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    wdiv__yox = []
    for bywp__jorvh in range(n_keys):
        wdiv__yox.append('t1_keys[{}]'.format(bywp__jorvh))
    for bywp__jorvh in range(len(left_other_names)):
        wdiv__yox.append('data_left[{}]'.format(bywp__jorvh))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in wdiv__yox))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    dfd__bgyd = []
    for bywp__jorvh in range(n_keys):
        dfd__bgyd.append('t2_keys[{}]'.format(bywp__jorvh))
    for bywp__jorvh in range(len(right_other_names)):
        dfd__bgyd.append('data_right[{}]'.format(bywp__jorvh))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in dfd__bgyd))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        ych__tfmdg else '0' for ych__tfmdg in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if ych__tfmdg else '0' for ych__tfmdg in tvoi__dexdr))
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
        rrh__vcn = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += rrh__vcn[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {rrh__vcn[1]})
"""
        idx += 1
    for bywp__jorvh, eydy__kvw in enumerate(left_key_names):
        tjqkm__qav = _match_join_key_types(left_key_types[bywp__jorvh],
            right_key_types[bywp__jorvh], loc)
        rrh__vcn = get_out_type(idx, tjqkm__qav, f't1_keys[{bywp__jorvh}]',
            is_right, vect_same_key[bywp__jorvh])
        func_text += rrh__vcn[0]
        func_text += f"""    t1_keys_{bywp__jorvh} = info_to_array(info_from_table(out_table, {idx}), {rrh__vcn[1]})
"""
        idx += 1
    for bywp__jorvh, eydy__kvw in enumerate(left_other_names):
        rrh__vcn = get_out_type(idx, left_other_types[bywp__jorvh],
            eydy__kvw, is_right, False)
        func_text += rrh__vcn[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(bywp__jorvh, idx, rrh__vcn[1]))
        idx += 1
    for bywp__jorvh, eydy__kvw in enumerate(right_key_names):
        if not vect_same_key[bywp__jorvh] and not is_join:
            tjqkm__qav = _match_join_key_types(left_key_types[bywp__jorvh],
                right_key_types[bywp__jorvh], loc)
            rrh__vcn = get_out_type(idx, tjqkm__qav,
                f't2_keys[{bywp__jorvh}]', is_left, False)
            func_text += rrh__vcn[0]
            func_text += f"""    t2_keys_{bywp__jorvh} = info_to_array(info_from_table(out_table, {idx}), {rrh__vcn[1]})
"""
            idx += 1
    for bywp__jorvh, eydy__kvw in enumerate(right_other_names):
        rrh__vcn = get_out_type(idx, right_other_types[bywp__jorvh],
            eydy__kvw, is_left, False)
        func_text += rrh__vcn[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(bywp__jorvh, idx, rrh__vcn[1]))
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
    wxpo__rnkf = bodo.libs.distributed_api.get_size()
    wkm__mlkse = np.empty(wxpo__rnkf, left_key_arrs[0].dtype)
    fby__twwu = np.empty(wxpo__rnkf, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(wkm__mlkse, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(fby__twwu, left_key_arrs[0][-1])
    nrg__zrkr = np.zeros(wxpo__rnkf, np.int32)
    uwl__qvdal = np.zeros(wxpo__rnkf, np.int32)
    zxg__rdgmr = np.zeros(wxpo__rnkf, np.int32)
    low__ump = right_key_arrs[0][0]
    ykg__mqo = right_key_arrs[0][-1]
    unyhq__lihsx = -1
    bywp__jorvh = 0
    while bywp__jorvh < wxpo__rnkf - 1 and fby__twwu[bywp__jorvh] < low__ump:
        bywp__jorvh += 1
    while bywp__jorvh < wxpo__rnkf and wkm__mlkse[bywp__jorvh] <= ykg__mqo:
        unyhq__lihsx, vnl__stkd = _count_overlap(right_key_arrs[0],
            wkm__mlkse[bywp__jorvh], fby__twwu[bywp__jorvh])
        if unyhq__lihsx != 0:
            unyhq__lihsx -= 1
            vnl__stkd += 1
        nrg__zrkr[bywp__jorvh] = vnl__stkd
        uwl__qvdal[bywp__jorvh] = unyhq__lihsx
        bywp__jorvh += 1
    while bywp__jorvh < wxpo__rnkf:
        nrg__zrkr[bywp__jorvh] = 1
        uwl__qvdal[bywp__jorvh] = len(right_key_arrs[0]) - 1
        bywp__jorvh += 1
    bodo.libs.distributed_api.alltoall(nrg__zrkr, zxg__rdgmr, 1)
    xys__rpe = zxg__rdgmr.sum()
    eeym__oupf = np.empty(xys__rpe, right_key_arrs[0].dtype)
    plf__eemp = alloc_arr_tup(xys__rpe, right_data)
    qizxf__sdxk = bodo.ir.join.calc_disp(zxg__rdgmr)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], eeym__oupf,
        nrg__zrkr, zxg__rdgmr, uwl__qvdal, qizxf__sdxk)
    bodo.libs.distributed_api.alltoallv_tup(right_data, plf__eemp,
        nrg__zrkr, zxg__rdgmr, uwl__qvdal, qizxf__sdxk)
    return (eeym__oupf,), plf__eemp


@numba.njit
def _count_overlap(r_key_arr, start, end):
    vnl__stkd = 0
    unyhq__lihsx = 0
    btko__niwbz = 0
    while btko__niwbz < len(r_key_arr) and r_key_arr[btko__niwbz] < start:
        unyhq__lihsx += 1
        btko__niwbz += 1
    while btko__niwbz < len(r_key_arr) and start <= r_key_arr[btko__niwbz
        ] <= end:
        btko__niwbz += 1
        vnl__stkd += 1
    return unyhq__lihsx, vnl__stkd


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    drs__rvhpy = np.empty_like(arr)
    drs__rvhpy[0] = 0
    for bywp__jorvh in range(1, len(arr)):
        drs__rvhpy[bywp__jorvh] = drs__rvhpy[bywp__jorvh - 1] + arr[
            bywp__jorvh - 1]
    return drs__rvhpy


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    ooib__ebup = len(left_keys[0])
    klsl__mmvyo = len(right_keys[0])
    mpnnf__aly = alloc_arr_tup(ooib__ebup, left_keys)
    tpyma__qzilr = alloc_arr_tup(ooib__ebup, right_keys)
    dip__awflq = alloc_arr_tup(ooib__ebup, data_left)
    dwrz__kugm = alloc_arr_tup(ooib__ebup, data_right)
    bery__fshnp = 0
    hbvri__hqqc = 0
    for bery__fshnp in range(ooib__ebup):
        if hbvri__hqqc < 0:
            hbvri__hqqc = 0
        while hbvri__hqqc < klsl__mmvyo and getitem_arr_tup(right_keys,
            hbvri__hqqc) <= getitem_arr_tup(left_keys, bery__fshnp):
            hbvri__hqqc += 1
        hbvri__hqqc -= 1
        setitem_arr_tup(mpnnf__aly, bery__fshnp, getitem_arr_tup(left_keys,
            bery__fshnp))
        setitem_arr_tup(dip__awflq, bery__fshnp, getitem_arr_tup(data_left,
            bery__fshnp))
        if hbvri__hqqc >= 0:
            setitem_arr_tup(tpyma__qzilr, bery__fshnp, getitem_arr_tup(
                right_keys, hbvri__hqqc))
            setitem_arr_tup(dwrz__kugm, bery__fshnp, getitem_arr_tup(
                data_right, hbvri__hqqc))
        else:
            bodo.libs.array_kernels.setna_tup(tpyma__qzilr, bery__fshnp)
            bodo.libs.array_kernels.setna_tup(dwrz__kugm, bery__fshnp)
    return mpnnf__aly, tpyma__qzilr, dip__awflq, dwrz__kugm
