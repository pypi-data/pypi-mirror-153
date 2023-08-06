"""IR node for the join and merge"""
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic, overload
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
        tym__krk = func.signature
        mus__dpks = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        yde__qfaqa = cgutils.get_or_insert_function(builder.module,
            mus__dpks, sym._literal_value)
        builder.call(yde__qfaqa, [context.get_constant_null(tym__krk.args[0
            ]), context.get_constant_null(tym__krk.args[1]), context.
            get_constant_null(tym__krk.args[2]), context.get_constant_null(
            tym__krk.args[3]), context.get_constant_null(tym__krk.args[4]),
            context.get_constant_null(tym__krk.args[5]), context.
            get_constant(types.int64, 0), context.get_constant(types.int64, 0)]
            )
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


class Join(ir.Stmt):

    def __init__(self, df_out, left_df, right_df, left_keys, right_keys,
        out_data_vars, left_vars, right_vars, how, suffix_x, suffix_y, loc,
        is_left, is_right, is_join, left_index, right_index, indicator,
        is_na_equal, gen_cond_expr):
        self.df_out = df_out
        self.left_df = left_df
        self.right_df = right_df
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.suffix_x = suffix_x
        self.suffix_y = suffix_y
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator = indicator
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_cond_cols = set(zsnhu__onbwa for zsnhu__onbwa in
            left_vars.keys() if f'(left.{zsnhu__onbwa})' in gen_cond_expr)
        self.right_cond_cols = set(zsnhu__onbwa for zsnhu__onbwa in
            right_vars.keys() if f'(right.{zsnhu__onbwa})' in gen_cond_expr)
        mjj__wzbfg = set(left_keys) & set(right_keys)
        tzlis__ewzdv = set(left_vars.keys()) & set(right_vars.keys())
        qmq__nbd = tzlis__ewzdv - mjj__wzbfg
        vect_same_key = []
        n_keys = len(left_keys)
        for bwddp__vgbwx in range(n_keys):
            nkxtr__dxfjj = left_keys[bwddp__vgbwx]
            ejz__upbdb = right_keys[bwddp__vgbwx]
            vect_same_key.append(nkxtr__dxfjj == ejz__upbdb)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(zsnhu__onbwa) + suffix_x if 
            zsnhu__onbwa in qmq__nbd else zsnhu__onbwa): ('left',
            zsnhu__onbwa) for zsnhu__onbwa in left_vars.keys()}
        self.column_origins.update({(str(zsnhu__onbwa) + suffix_y if 
            zsnhu__onbwa in qmq__nbd else zsnhu__onbwa): ('right',
            zsnhu__onbwa) for zsnhu__onbwa in right_vars.keys()})
        if '$_bodo_index_' in qmq__nbd:
            qmq__nbd.remove('$_bodo_index_')
        self.add_suffix = qmq__nbd

    def __repr__(self):
        odxqp__wal = ''
        for zsnhu__onbwa, kuufp__igni in self.out_data_vars.items():
            odxqp__wal += "'{}':{}, ".format(zsnhu__onbwa, kuufp__igni.name)
        iamnc__ewlrm = '{}{{{}}}'.format(self.df_out, odxqp__wal)
        kfe__axqag = ''
        for zsnhu__onbwa, kuufp__igni in self.left_vars.items():
            kfe__axqag += "'{}':{}, ".format(zsnhu__onbwa, kuufp__igni.name)
        lvbn__datuw = '{}{{{}}}'.format(self.left_df, kfe__axqag)
        kfe__axqag = ''
        for zsnhu__onbwa, kuufp__igni in self.right_vars.items():
            kfe__axqag += "'{}':{}, ".format(zsnhu__onbwa, kuufp__igni.name)
        gotlb__tvxq = '{}{{{}}}'.format(self.right_df, kfe__axqag)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, iamnc__ewlrm, lvbn__datuw, gotlb__tvxq)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    bqqwf__yxggz = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    vgewa__ncugh = []
    sej__jdov = list(join_node.left_vars.values())
    for lzi__oou in sej__jdov:
        suh__blxwi = typemap[lzi__oou.name]
        jmq__ogumy = equiv_set.get_shape(lzi__oou)
        if jmq__ogumy:
            vgewa__ncugh.append(jmq__ogumy[0])
    if len(vgewa__ncugh) > 1:
        equiv_set.insert_equiv(*vgewa__ncugh)
    vgewa__ncugh = []
    sej__jdov = list(join_node.right_vars.values())
    for lzi__oou in sej__jdov:
        suh__blxwi = typemap[lzi__oou.name]
        jmq__ogumy = equiv_set.get_shape(lzi__oou)
        if jmq__ogumy:
            vgewa__ncugh.append(jmq__ogumy[0])
    if len(vgewa__ncugh) > 1:
        equiv_set.insert_equiv(*vgewa__ncugh)
    vgewa__ncugh = []
    for lzi__oou in join_node.out_data_vars.values():
        suh__blxwi = typemap[lzi__oou.name]
        wgvp__soa = array_analysis._gen_shape_call(equiv_set, lzi__oou,
            suh__blxwi.ndim, None, bqqwf__yxggz)
        equiv_set.insert_equiv(lzi__oou, wgvp__soa)
        vgewa__ncugh.append(wgvp__soa[0])
        equiv_set.define(lzi__oou, set())
    if len(vgewa__ncugh) > 1:
        equiv_set.insert_equiv(*vgewa__ncugh)
    return [], bqqwf__yxggz


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    biwoo__lhe = Distribution.OneD
    lyno__jukt = Distribution.OneD
    for lzi__oou in join_node.left_vars.values():
        biwoo__lhe = Distribution(min(biwoo__lhe.value, array_dists[
            lzi__oou.name].value))
    for lzi__oou in join_node.right_vars.values():
        lyno__jukt = Distribution(min(lyno__jukt.value, array_dists[
            lzi__oou.name].value))
    zdcs__ajth = Distribution.OneD_Var
    for lzi__oou in join_node.out_data_vars.values():
        if lzi__oou.name in array_dists:
            zdcs__ajth = Distribution(min(zdcs__ajth.value, array_dists[
                lzi__oou.name].value))
    elufm__kgtv = Distribution(min(zdcs__ajth.value, biwoo__lhe.value))
    ssx__yel = Distribution(min(zdcs__ajth.value, lyno__jukt.value))
    zdcs__ajth = Distribution(max(elufm__kgtv.value, ssx__yel.value))
    for lzi__oou in join_node.out_data_vars.values():
        array_dists[lzi__oou.name] = zdcs__ajth
    if zdcs__ajth != Distribution.OneD_Var:
        biwoo__lhe = zdcs__ajth
        lyno__jukt = zdcs__ajth
    for lzi__oou in join_node.left_vars.values():
        array_dists[lzi__oou.name] = biwoo__lhe
    for lzi__oou in join_node.right_vars.values():
        array_dists[lzi__oou.name] = lyno__jukt
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    mjj__wzbfg = set(join_node.left_keys) & set(join_node.right_keys)
    tzlis__ewzdv = set(join_node.left_vars.keys()) & set(join_node.
        right_vars.keys())
    qmq__nbd = tzlis__ewzdv - mjj__wzbfg
    for wlsut__yht, crqai__jbxl in join_node.out_data_vars.items():
        if join_node.indicator and wlsut__yht == '_merge':
            continue
        if not wlsut__yht in join_node.column_origins:
            raise BodoError('join(): The variable ' + wlsut__yht +
                ' is absent from the output')
        zlds__qmo = join_node.column_origins[wlsut__yht]
        if zlds__qmo[0] == 'left':
            lzi__oou = join_node.left_vars[zlds__qmo[1]]
        else:
            lzi__oou = join_node.right_vars[zlds__qmo[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=crqai__jbxl.
            name, src=lzi__oou.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for xhval__biaqr in list(join_node.left_vars.keys()):
        join_node.left_vars[xhval__biaqr] = visit_vars_inner(join_node.
            left_vars[xhval__biaqr], callback, cbdata)
    for xhval__biaqr in list(join_node.right_vars.keys()):
        join_node.right_vars[xhval__biaqr] = visit_vars_inner(join_node.
            right_vars[xhval__biaqr], callback, cbdata)
    for xhval__biaqr in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[xhval__biaqr] = visit_vars_inner(join_node.
            out_data_vars[xhval__biaqr], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    dquan__ess = []
    uvfu__huup = True
    for xhval__biaqr, lzi__oou in join_node.out_data_vars.items():
        if lzi__oou.name in lives:
            uvfu__huup = False
            continue
        if xhval__biaqr == '$_bodo_index_':
            continue
        if join_node.indicator and xhval__biaqr == '_merge':
            dquan__ess.append('_merge')
            join_node.indicator = False
            continue
        ijue__ytbm, abw__dad = join_node.column_origins[xhval__biaqr]
        if (ijue__ytbm == 'left' and abw__dad not in join_node.left_keys and
            abw__dad not in join_node.left_cond_cols):
            join_node.left_vars.pop(abw__dad)
            dquan__ess.append(xhval__biaqr)
        if (ijue__ytbm == 'right' and abw__dad not in join_node.right_keys and
            abw__dad not in join_node.right_cond_cols):
            join_node.right_vars.pop(abw__dad)
            dquan__ess.append(xhval__biaqr)
    for cname in dquan__ess:
        join_node.out_data_vars.pop(cname)
    if uvfu__huup:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({kuufp__igni.name for kuufp__igni in join_node.left_vars
        .values()})
    use_set.update({kuufp__igni.name for kuufp__igni in join_node.
        right_vars.values()})
    def_set.update({kuufp__igni.name for kuufp__igni in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    mkrcu__excx = set(kuufp__igni.name for kuufp__igni in join_node.
        out_data_vars.values())
    return set(), mkrcu__excx


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for xhval__biaqr in list(join_node.left_vars.keys()):
        join_node.left_vars[xhval__biaqr] = replace_vars_inner(join_node.
            left_vars[xhval__biaqr], var_dict)
    for xhval__biaqr in list(join_node.right_vars.keys()):
        join_node.right_vars[xhval__biaqr] = replace_vars_inner(join_node.
            right_vars[xhval__biaqr], var_dict)
    for xhval__biaqr in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[xhval__biaqr] = replace_vars_inner(join_node
            .out_data_vars[xhval__biaqr], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for lzi__oou in join_node.out_data_vars.values():
        definitions[lzi__oou.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    uuugi__wfor = tuple(join_node.left_vars[zsnhu__onbwa] for zsnhu__onbwa in
        join_node.left_keys)
    rfc__forpd = tuple(join_node.right_vars[zsnhu__onbwa] for zsnhu__onbwa in
        join_node.right_keys)
    hjw__wefa = tuple(join_node.left_vars.keys())
    mkp__bwh = tuple(join_node.right_vars.keys())
    yapts__lfrkr = ()
    nyisw__jepj = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        ypza__ehyvv = join_node.right_keys[0]
        if ypza__ehyvv in hjw__wefa:
            nyisw__jepj = ypza__ehyvv,
            yapts__lfrkr = join_node.right_vars[ypza__ehyvv],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        ypza__ehyvv = join_node.left_keys[0]
        if ypza__ehyvv in mkp__bwh:
            nyisw__jepj = ypza__ehyvv,
            yapts__lfrkr = join_node.left_vars[ypza__ehyvv],
            optional_column = True
    sjf__sov = tuple(join_node.out_data_vars[cname] for cname in nyisw__jepj)
    uvsyu__lzm = tuple(kuufp__igni for oyc__rsfzn, kuufp__igni in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if oyc__rsfzn
         not in join_node.left_keys)
    gjaze__qerd = tuple(kuufp__igni for oyc__rsfzn, kuufp__igni in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        oyc__rsfzn not in join_node.right_keys)
    yfqnn__ixis = (yapts__lfrkr + uuugi__wfor + rfc__forpd + uvsyu__lzm +
        gjaze__qerd)
    gnxcc__oytri = tuple(typemap[kuufp__igni.name] for kuufp__igni in
        yfqnn__ixis)
    zqx__rukla = tuple('opti_c' + str(uhx__nawn) for uhx__nawn in range(len
        (yapts__lfrkr)))
    left_other_names = tuple('t1_c' + str(uhx__nawn) for uhx__nawn in range
        (len(uvsyu__lzm)))
    right_other_names = tuple('t2_c' + str(uhx__nawn) for uhx__nawn in
        range(len(gjaze__qerd)))
    left_other_types = tuple([typemap[zsnhu__onbwa.name] for zsnhu__onbwa in
        uvsyu__lzm])
    right_other_types = tuple([typemap[zsnhu__onbwa.name] for zsnhu__onbwa in
        gjaze__qerd])
    left_key_names = tuple('t1_key' + str(uhx__nawn) for uhx__nawn in range
        (n_keys))
    right_key_names = tuple('t2_key' + str(uhx__nawn) for uhx__nawn in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(zqx__rukla[
        0]) if len(zqx__rukla) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[kuufp__igni.name] for kuufp__igni in
        uuugi__wfor)
    right_key_types = tuple(typemap[kuufp__igni.name] for kuufp__igni in
        rfc__forpd)
    for uhx__nawn in range(n_keys):
        glbs[f'key_type_{uhx__nawn}'] = _match_join_key_types(left_key_types
            [uhx__nawn], right_key_types[uhx__nawn], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[uhx__nawn]}, key_type_{uhx__nawn})'
         for uhx__nawn in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[uhx__nawn]}, key_type_{uhx__nawn})'
         for uhx__nawn in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    fyfwi__crnqb = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            sgk__tgnl = str(cname) + join_node.suffix_x
        else:
            sgk__tgnl = cname
        assert sgk__tgnl in join_node.out_data_vars
        fyfwi__crnqb.append(join_node.out_data_vars[sgk__tgnl])
    for uhx__nawn, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[uhx__nawn] and not join_node.is_join:
            if cname in join_node.add_suffix:
                sgk__tgnl = str(cname) + join_node.suffix_y
            else:
                sgk__tgnl = cname
            assert sgk__tgnl in join_node.out_data_vars
            fyfwi__crnqb.append(join_node.out_data_vars[sgk__tgnl])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                sgk__tgnl = str(cname) + join_node.suffix_x
            else:
                sgk__tgnl = str(cname) + join_node.suffix_y
        else:
            sgk__tgnl = cname
        return join_node.out_data_vars[sgk__tgnl]
    frpt__aomqa = sjf__sov + tuple(fyfwi__crnqb)
    frpt__aomqa += tuple(_get_out_col_var(oyc__rsfzn, True) for oyc__rsfzn,
        kuufp__igni in sorted(join_node.left_vars.items(), key=lambda a:
        str(a[0])) if oyc__rsfzn not in join_node.left_keys)
    frpt__aomqa += tuple(_get_out_col_var(oyc__rsfzn, False) for oyc__rsfzn,
        kuufp__igni in sorted(join_node.right_vars.items(), key=lambda a:
        str(a[0])) if oyc__rsfzn not in join_node.right_keys)
    if join_node.indicator:
        frpt__aomqa += _get_out_col_var('_merge', False),
    hkz__tgxdt = [('t3_c' + str(uhx__nawn)) for uhx__nawn in range(len(
        frpt__aomqa))]
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel
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
            right_parallel, glbs, [typemap[kuufp__igni.name] for
            kuufp__igni in frpt__aomqa], join_node.loc, join_node.indicator,
            join_node.is_na_equal, general_cond_cfunc, left_col_nums,
            right_col_nums)
    if join_node.how == 'asof':
        for uhx__nawn in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(uhx__nawn,
                uhx__nawn)
        for uhx__nawn in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(uhx__nawn
                , uhx__nawn)
        for uhx__nawn in range(n_keys):
            func_text += (
                f'    t1_keys_{uhx__nawn} = out_t1_keys[{uhx__nawn}]\n')
        for uhx__nawn in range(n_keys):
            func_text += (
                f'    t2_keys_{uhx__nawn} = out_t2_keys[{uhx__nawn}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {hkz__tgxdt[idx]} = opti_0\n'
        idx += 1
    for uhx__nawn in range(n_keys):
        func_text += f'    {hkz__tgxdt[idx]} = t1_keys_{uhx__nawn}\n'
        idx += 1
    for uhx__nawn in range(n_keys):
        if not join_node.vect_same_key[uhx__nawn] and not join_node.is_join:
            func_text += f'    {hkz__tgxdt[idx]} = t2_keys_{uhx__nawn}\n'
            idx += 1
    for uhx__nawn in range(len(left_other_names)):
        func_text += f'    {hkz__tgxdt[idx]} = left_{uhx__nawn}\n'
        idx += 1
    for uhx__nawn in range(len(right_other_names)):
        func_text += f'    {hkz__tgxdt[idx]} = right_{uhx__nawn}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {hkz__tgxdt[idx]} = indicator_col\n'
        idx += 1
    toql__aoyh = {}
    exec(func_text, {}, toql__aoyh)
    pwy__iym = toql__aoyh['f']
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
    oeudz__jfnf = compile_to_numba_ir(pwy__iym, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=gnxcc__oytri, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(oeudz__jfnf, yfqnn__ixis)
    ydvl__swuis = oeudz__jfnf.body[:-3]
    for uhx__nawn in range(len(frpt__aomqa)):
        ydvl__swuis[-len(frpt__aomqa) + uhx__nawn].target = frpt__aomqa[
            uhx__nawn]
    return ydvl__swuis


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    bjthj__nov = next_label()
    mmvnh__vbde = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    ijogf__erko = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{bjthj__nov}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        mmvnh__vbde, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        ijogf__erko, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    toql__aoyh = {}
    exec(func_text, table_getitem_funcs, toql__aoyh)
    iqsfl__pebdi = toql__aoyh[f'bodo_join_gen_cond{bjthj__nov}']
    idul__goa = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    vfjn__ayw = numba.cfunc(idul__goa, nopython=True)(iqsfl__pebdi)
    join_gen_cond_cfunc[vfjn__ayw.native_name] = vfjn__ayw
    join_gen_cond_cfunc_addr[vfjn__ayw.native_name] = vfjn__ayw.address
    return vfjn__ayw, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    gnd__ywp = []
    for zsnhu__onbwa, bipvo__dusbd in col_to_ind.items():
        cname = f'({table_name}.{zsnhu__onbwa})'
        if cname not in expr:
            continue
        pcrds__ejkrx = f'getitem_{table_name}_val_{bipvo__dusbd}'
        zpqx__ptzaz = f'_bodo_{table_name}_val_{bipvo__dusbd}'
        wdwas__mic = typemap[col_vars[zsnhu__onbwa].name]
        if is_str_arr_type(wdwas__mic):
            func_text += f"""  {zpqx__ptzaz}, {zpqx__ptzaz}_size = {pcrds__ejkrx}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {zpqx__ptzaz} = bodo.libs.str_arr_ext.decode_utf8({zpqx__ptzaz}, {zpqx__ptzaz}_size)
"""
        else:
            func_text += (
                f'  {zpqx__ptzaz} = {pcrds__ejkrx}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[pcrds__ejkrx
            ] = bodo.libs.array._gen_row_access_intrinsic(wdwas__mic,
            bipvo__dusbd)
        expr = expr.replace(cname, zpqx__ptzaz)
        wmug__ldmbz = f'({na_check_name}.{table_name}.{zsnhu__onbwa})'
        if wmug__ldmbz in expr:
            mpaf__vyei = f'nacheck_{table_name}_val_{bipvo__dusbd}'
            tywn__tjr = f'_bodo_isna_{table_name}_val_{bipvo__dusbd}'
            if (isinstance(wdwas__mic, bodo.libs.int_arr_ext.
                IntegerArrayType) or wdwas__mic == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(wdwas__mic)):
                func_text += f"""  {tywn__tjr} = {mpaf__vyei}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {tywn__tjr} = {mpaf__vyei}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[mpaf__vyei
                ] = bodo.libs.array._gen_row_na_check_intrinsic(wdwas__mic,
                bipvo__dusbd)
            expr = expr.replace(wmug__ldmbz, tywn__tjr)
        if bipvo__dusbd >= n_keys:
            gnd__ywp.append(bipvo__dusbd)
    return expr, func_text, gnd__ywp


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {zsnhu__onbwa: uhx__nawn for uhx__nawn, zsnhu__onbwa in
        enumerate(key_names)}
    uhx__nawn = n_keys
    for zsnhu__onbwa in sorted(col_vars, key=lambda a: str(a)):
        if zsnhu__onbwa in col_to_ind:
            continue
        col_to_ind[zsnhu__onbwa] = uhx__nawn
        uhx__nawn += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as fvizi__pcx:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    swap__stg = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[kuufp__igni.name] in swap__stg for
        kuufp__igni in join_node.left_vars.values())
    right_parallel = all(array_dists[kuufp__igni.name] in swap__stg for
        kuufp__igni in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[kuufp__igni.name] in swap__stg for
            kuufp__igni in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[kuufp__igni.name] in swap__stg for
            kuufp__igni in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[kuufp__igni.name] in swap__stg for
            kuufp__igni in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    wjqm__iddcq = []
    for uhx__nawn in range(len(left_key_names)):
        jnw__lstk = _match_join_key_types(left_key_types[uhx__nawn],
            right_key_types[uhx__nawn], loc)
        wjqm__iddcq.append(needs_typechange(jnw__lstk, is_right,
            vect_same_key[uhx__nawn]))
    for uhx__nawn in range(len(left_other_names)):
        wjqm__iddcq.append(needs_typechange(left_other_types[uhx__nawn],
            is_right, False))
    for uhx__nawn in range(len(right_key_names)):
        if not vect_same_key[uhx__nawn] and not is_join:
            jnw__lstk = _match_join_key_types(left_key_types[uhx__nawn],
                right_key_types[uhx__nawn], loc)
            wjqm__iddcq.append(needs_typechange(jnw__lstk, is_left, False))
    for uhx__nawn in range(len(right_other_names)):
        wjqm__iddcq.append(needs_typechange(right_other_types[uhx__nawn],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                xiznt__sfwx = IntDtype(in_type.dtype).name
                assert xiznt__sfwx.endswith('Dtype()')
                xiznt__sfwx = xiznt__sfwx[:-7]
                xwwnz__bqij = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{xiznt__sfwx}"))
"""
                kcusx__niac = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                xwwnz__bqij = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                kcusx__niac = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            xwwnz__bqij = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            kcusx__niac = f'typ_{idx}'
        else:
            xwwnz__bqij = ''
            kcusx__niac = in_name
        return xwwnz__bqij, kcusx__niac
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    gas__vqy = []
    for uhx__nawn in range(n_keys):
        gas__vqy.append('t1_keys[{}]'.format(uhx__nawn))
    for uhx__nawn in range(len(left_other_names)):
        gas__vqy.append('data_left[{}]'.format(uhx__nawn))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in gas__vqy))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    zwnw__oqohk = []
    for uhx__nawn in range(n_keys):
        zwnw__oqohk.append('t2_keys[{}]'.format(uhx__nawn))
    for uhx__nawn in range(len(right_other_names)):
        zwnw__oqohk.append('data_right[{}]'.format(uhx__nawn))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in zwnw__oqohk))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        ypc__lyu else '0' for ypc__lyu in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if ypc__lyu else '0' for ypc__lyu in wjqm__iddcq))
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
        nurvs__xacgr = get_out_type(idx, out_types[idx], 'opti_c0', False, 
            False)
        func_text += nurvs__xacgr[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {nurvs__xacgr[1]})
"""
        idx += 1
    for uhx__nawn, tqd__sds in enumerate(left_key_names):
        jnw__lstk = _match_join_key_types(left_key_types[uhx__nawn],
            right_key_types[uhx__nawn], loc)
        nurvs__xacgr = get_out_type(idx, jnw__lstk, f't1_keys[{uhx__nawn}]',
            is_right, vect_same_key[uhx__nawn])
        func_text += nurvs__xacgr[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if jnw__lstk != left_key_types[uhx__nawn] and left_key_types[uhx__nawn
            ] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{uhx__nawn} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {nurvs__xacgr[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{uhx__nawn} = info_to_array(info_from_table(out_table, {idx}), {nurvs__xacgr[1]})
"""
        idx += 1
    for uhx__nawn, tqd__sds in enumerate(left_other_names):
        nurvs__xacgr = get_out_type(idx, left_other_types[uhx__nawn],
            tqd__sds, is_right, False)
        func_text += nurvs__xacgr[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(uhx__nawn, idx, nurvs__xacgr[1]))
        idx += 1
    for uhx__nawn, tqd__sds in enumerate(right_key_names):
        if not vect_same_key[uhx__nawn] and not is_join:
            jnw__lstk = _match_join_key_types(left_key_types[uhx__nawn],
                right_key_types[uhx__nawn], loc)
            nurvs__xacgr = get_out_type(idx, jnw__lstk,
                f't2_keys[{uhx__nawn}]', is_left, False)
            func_text += nurvs__xacgr[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if jnw__lstk != right_key_types[uhx__nawn] and right_key_types[
                uhx__nawn] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{uhx__nawn} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {nurvs__xacgr[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{uhx__nawn} = info_to_array(info_from_table(out_table, {idx}), {nurvs__xacgr[1]})
"""
            idx += 1
    for uhx__nawn, tqd__sds in enumerate(right_other_names):
        nurvs__xacgr = get_out_type(idx, right_other_types[uhx__nawn],
            tqd__sds, is_left, False)
        func_text += nurvs__xacgr[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(uhx__nawn, idx, nurvs__xacgr[1]))
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
    ghfrf__hhu = bodo.libs.distributed_api.get_size()
    zhx__nqx = np.empty(ghfrf__hhu, left_key_arrs[0].dtype)
    xladl__snu = np.empty(ghfrf__hhu, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(zhx__nqx, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(xladl__snu, left_key_arrs[0][-1])
    hmwjk__jwrr = np.zeros(ghfrf__hhu, np.int32)
    llp__nyl = np.zeros(ghfrf__hhu, np.int32)
    mbc__mzz = np.zeros(ghfrf__hhu, np.int32)
    megie__dkraf = right_key_arrs[0][0]
    stjs__magl = right_key_arrs[0][-1]
    ucy__zegm = -1
    uhx__nawn = 0
    while uhx__nawn < ghfrf__hhu - 1 and xladl__snu[uhx__nawn] < megie__dkraf:
        uhx__nawn += 1
    while uhx__nawn < ghfrf__hhu and zhx__nqx[uhx__nawn] <= stjs__magl:
        ucy__zegm, fgd__vwzfx = _count_overlap(right_key_arrs[0], zhx__nqx[
            uhx__nawn], xladl__snu[uhx__nawn])
        if ucy__zegm != 0:
            ucy__zegm -= 1
            fgd__vwzfx += 1
        hmwjk__jwrr[uhx__nawn] = fgd__vwzfx
        llp__nyl[uhx__nawn] = ucy__zegm
        uhx__nawn += 1
    while uhx__nawn < ghfrf__hhu:
        hmwjk__jwrr[uhx__nawn] = 1
        llp__nyl[uhx__nawn] = len(right_key_arrs[0]) - 1
        uhx__nawn += 1
    bodo.libs.distributed_api.alltoall(hmwjk__jwrr, mbc__mzz, 1)
    pizfr__uxphv = mbc__mzz.sum()
    bzb__owfry = np.empty(pizfr__uxphv, right_key_arrs[0].dtype)
    tuak__iotc = alloc_arr_tup(pizfr__uxphv, right_data)
    zpr__vjot = bodo.ir.join.calc_disp(mbc__mzz)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], bzb__owfry,
        hmwjk__jwrr, mbc__mzz, llp__nyl, zpr__vjot)
    bodo.libs.distributed_api.alltoallv_tup(right_data, tuak__iotc,
        hmwjk__jwrr, mbc__mzz, llp__nyl, zpr__vjot)
    return (bzb__owfry,), tuak__iotc


@numba.njit
def _count_overlap(r_key_arr, start, end):
    fgd__vwzfx = 0
    ucy__zegm = 0
    cgxi__xdsxo = 0
    while cgxi__xdsxo < len(r_key_arr) and r_key_arr[cgxi__xdsxo] < start:
        ucy__zegm += 1
        cgxi__xdsxo += 1
    while cgxi__xdsxo < len(r_key_arr) and start <= r_key_arr[cgxi__xdsxo
        ] <= end:
        cgxi__xdsxo += 1
        fgd__vwzfx += 1
    return ucy__zegm, fgd__vwzfx


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    rtt__dmqqw = np.empty_like(arr)
    rtt__dmqqw[0] = 0
    for uhx__nawn in range(1, len(arr)):
        rtt__dmqqw[uhx__nawn] = rtt__dmqqw[uhx__nawn - 1] + arr[uhx__nawn - 1]
    return rtt__dmqqw


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    qsfa__slxkc = len(left_keys[0])
    znwk__hopts = len(right_keys[0])
    xecv__iru = alloc_arr_tup(qsfa__slxkc, left_keys)
    vlu__sapzv = alloc_arr_tup(qsfa__slxkc, right_keys)
    wcfh__vlr = alloc_arr_tup(qsfa__slxkc, data_left)
    oxnj__ypom = alloc_arr_tup(qsfa__slxkc, data_right)
    nho__jsj = 0
    muf__nfwbi = 0
    for nho__jsj in range(qsfa__slxkc):
        if muf__nfwbi < 0:
            muf__nfwbi = 0
        while muf__nfwbi < znwk__hopts and getitem_arr_tup(right_keys,
            muf__nfwbi) <= getitem_arr_tup(left_keys, nho__jsj):
            muf__nfwbi += 1
        muf__nfwbi -= 1
        setitem_arr_tup(xecv__iru, nho__jsj, getitem_arr_tup(left_keys,
            nho__jsj))
        setitem_arr_tup(wcfh__vlr, nho__jsj, getitem_arr_tup(data_left,
            nho__jsj))
        if muf__nfwbi >= 0:
            setitem_arr_tup(vlu__sapzv, nho__jsj, getitem_arr_tup(
                right_keys, muf__nfwbi))
            setitem_arr_tup(oxnj__ypom, nho__jsj, getitem_arr_tup(
                data_right, muf__nfwbi))
        else:
            bodo.libs.array_kernels.setna_tup(vlu__sapzv, nho__jsj)
            bodo.libs.array_kernels.setna_tup(oxnj__ypom, nho__jsj)
    return xecv__iru, vlu__sapzv, wcfh__vlr, oxnj__ypom


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    fgd__vwzfx = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(uhx__nawn) for uhx__nawn in range(fgd__vwzfx)))
    toql__aoyh = {}
    exec(func_text, {}, toql__aoyh)
    jroyy__gvri = toql__aoyh['f']
    return jroyy__gvri
