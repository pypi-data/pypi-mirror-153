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
        ptef__ypvb = func.signature
        gku__ett = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        wcvju__azi = cgutils.get_or_insert_function(builder.module,
            gku__ett, sym._literal_value)
        builder.call(wcvju__azi, [context.get_constant_null(ptef__ypvb.args
            [0]), context.get_constant_null(ptef__ypvb.args[1]), context.
            get_constant_null(ptef__ypvb.args[2]), context.
            get_constant_null(ptef__ypvb.args[3]), context.
            get_constant_null(ptef__ypvb.args[4]), context.
            get_constant_null(ptef__ypvb.args[5]), context.get_constant(
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
        self.left_cond_cols = set(mrcch__flxb for mrcch__flxb in left_vars.
            keys() if f'(left.{mrcch__flxb})' in gen_cond_expr)
        self.right_cond_cols = set(mrcch__flxb for mrcch__flxb in
            right_vars.keys() if f'(right.{mrcch__flxb})' in gen_cond_expr)
        xbhlp__lmiwo = set(left_keys) & set(right_keys)
        pps__xme = set(left_vars.keys()) & set(right_vars.keys())
        yec__eeqr = pps__xme - xbhlp__lmiwo
        vect_same_key = []
        n_keys = len(left_keys)
        for duock__eijx in range(n_keys):
            eolo__rniey = left_keys[duock__eijx]
            wkw__rms = right_keys[duock__eijx]
            vect_same_key.append(eolo__rniey == wkw__rms)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(mrcch__flxb) + suffix_x if mrcch__flxb in
            yec__eeqr else mrcch__flxb): ('left', mrcch__flxb) for
            mrcch__flxb in left_vars.keys()}
        self.column_origins.update({(str(mrcch__flxb) + suffix_y if 
            mrcch__flxb in yec__eeqr else mrcch__flxb): ('right',
            mrcch__flxb) for mrcch__flxb in right_vars.keys()})
        if '$_bodo_index_' in yec__eeqr:
            yec__eeqr.remove('$_bodo_index_')
        self.add_suffix = yec__eeqr

    def __repr__(self):
        jpn__onz = ''
        for mrcch__flxb, iqcph__cxt in self.out_data_vars.items():
            jpn__onz += "'{}':{}, ".format(mrcch__flxb, iqcph__cxt.name)
        hsnve__sjt = '{}{{{}}}'.format(self.df_out, jpn__onz)
        mmuw__ebteo = ''
        for mrcch__flxb, iqcph__cxt in self.left_vars.items():
            mmuw__ebteo += "'{}':{}, ".format(mrcch__flxb, iqcph__cxt.name)
        brgct__zom = '{}{{{}}}'.format(self.left_df, mmuw__ebteo)
        mmuw__ebteo = ''
        for mrcch__flxb, iqcph__cxt in self.right_vars.items():
            mmuw__ebteo += "'{}':{}, ".format(mrcch__flxb, iqcph__cxt.name)
        nljck__otzb = '{}{{{}}}'.format(self.right_df, mmuw__ebteo)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, hsnve__sjt, brgct__zom, nljck__otzb)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    yphgj__euo = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    qxpve__wlpqi = []
    ypnj__iog = list(join_node.left_vars.values())
    for stxe__ucz in ypnj__iog:
        vaab__rvb = typemap[stxe__ucz.name]
        jswu__yfif = equiv_set.get_shape(stxe__ucz)
        if jswu__yfif:
            qxpve__wlpqi.append(jswu__yfif[0])
    if len(qxpve__wlpqi) > 1:
        equiv_set.insert_equiv(*qxpve__wlpqi)
    qxpve__wlpqi = []
    ypnj__iog = list(join_node.right_vars.values())
    for stxe__ucz in ypnj__iog:
        vaab__rvb = typemap[stxe__ucz.name]
        jswu__yfif = equiv_set.get_shape(stxe__ucz)
        if jswu__yfif:
            qxpve__wlpqi.append(jswu__yfif[0])
    if len(qxpve__wlpqi) > 1:
        equiv_set.insert_equiv(*qxpve__wlpqi)
    qxpve__wlpqi = []
    for stxe__ucz in join_node.out_data_vars.values():
        vaab__rvb = typemap[stxe__ucz.name]
        gdpc__pmvey = array_analysis._gen_shape_call(equiv_set, stxe__ucz,
            vaab__rvb.ndim, None, yphgj__euo)
        equiv_set.insert_equiv(stxe__ucz, gdpc__pmvey)
        qxpve__wlpqi.append(gdpc__pmvey[0])
        equiv_set.define(stxe__ucz, set())
    if len(qxpve__wlpqi) > 1:
        equiv_set.insert_equiv(*qxpve__wlpqi)
    return [], yphgj__euo


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    ecro__onoyp = Distribution.OneD
    umruo__scjwn = Distribution.OneD
    for stxe__ucz in join_node.left_vars.values():
        ecro__onoyp = Distribution(min(ecro__onoyp.value, array_dists[
            stxe__ucz.name].value))
    for stxe__ucz in join_node.right_vars.values():
        umruo__scjwn = Distribution(min(umruo__scjwn.value, array_dists[
            stxe__ucz.name].value))
    odqm__bhz = Distribution.OneD_Var
    for stxe__ucz in join_node.out_data_vars.values():
        if stxe__ucz.name in array_dists:
            odqm__bhz = Distribution(min(odqm__bhz.value, array_dists[
                stxe__ucz.name].value))
    fymu__jycv = Distribution(min(odqm__bhz.value, ecro__onoyp.value))
    gvg__gdst = Distribution(min(odqm__bhz.value, umruo__scjwn.value))
    odqm__bhz = Distribution(max(fymu__jycv.value, gvg__gdst.value))
    for stxe__ucz in join_node.out_data_vars.values():
        array_dists[stxe__ucz.name] = odqm__bhz
    if odqm__bhz != Distribution.OneD_Var:
        ecro__onoyp = odqm__bhz
        umruo__scjwn = odqm__bhz
    for stxe__ucz in join_node.left_vars.values():
        array_dists[stxe__ucz.name] = ecro__onoyp
    for stxe__ucz in join_node.right_vars.values():
        array_dists[stxe__ucz.name] = umruo__scjwn
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    xbhlp__lmiwo = set(join_node.left_keys) & set(join_node.right_keys)
    pps__xme = set(join_node.left_vars.keys()) & set(join_node.right_vars.
        keys())
    yec__eeqr = pps__xme - xbhlp__lmiwo
    for elr__qyo, dqmt__lxn in join_node.out_data_vars.items():
        if join_node.indicator and elr__qyo == '_merge':
            continue
        if not elr__qyo in join_node.column_origins:
            raise BodoError('join(): The variable ' + elr__qyo +
                ' is absent from the output')
        oiew__jqrh = join_node.column_origins[elr__qyo]
        if oiew__jqrh[0] == 'left':
            stxe__ucz = join_node.left_vars[oiew__jqrh[1]]
        else:
            stxe__ucz = join_node.right_vars[oiew__jqrh[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=dqmt__lxn.
            name, src=stxe__ucz.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for hlnuo__ctaqv in list(join_node.left_vars.keys()):
        join_node.left_vars[hlnuo__ctaqv] = visit_vars_inner(join_node.
            left_vars[hlnuo__ctaqv], callback, cbdata)
    for hlnuo__ctaqv in list(join_node.right_vars.keys()):
        join_node.right_vars[hlnuo__ctaqv] = visit_vars_inner(join_node.
            right_vars[hlnuo__ctaqv], callback, cbdata)
    for hlnuo__ctaqv in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[hlnuo__ctaqv] = visit_vars_inner(join_node.
            out_data_vars[hlnuo__ctaqv], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    bktm__tqn = []
    khcx__fze = True
    for hlnuo__ctaqv, stxe__ucz in join_node.out_data_vars.items():
        if stxe__ucz.name in lives:
            khcx__fze = False
            continue
        if hlnuo__ctaqv == '$_bodo_index_':
            continue
        if join_node.indicator and hlnuo__ctaqv == '_merge':
            bktm__tqn.append('_merge')
            join_node.indicator = False
            continue
        egiq__jedqx, oud__xckit = join_node.column_origins[hlnuo__ctaqv]
        if (egiq__jedqx == 'left' and oud__xckit not in join_node.left_keys and
            oud__xckit not in join_node.left_cond_cols):
            join_node.left_vars.pop(oud__xckit)
            bktm__tqn.append(hlnuo__ctaqv)
        if (egiq__jedqx == 'right' and oud__xckit not in join_node.
            right_keys and oud__xckit not in join_node.right_cond_cols):
            join_node.right_vars.pop(oud__xckit)
            bktm__tqn.append(hlnuo__ctaqv)
    for cname in bktm__tqn:
        join_node.out_data_vars.pop(cname)
    if khcx__fze:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({iqcph__cxt.name for iqcph__cxt in join_node.left_vars.
        values()})
    use_set.update({iqcph__cxt.name for iqcph__cxt in join_node.right_vars.
        values()})
    def_set.update({iqcph__cxt.name for iqcph__cxt in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    jsfzl__zsdp = set(iqcph__cxt.name for iqcph__cxt in join_node.
        out_data_vars.values())
    return set(), jsfzl__zsdp


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for hlnuo__ctaqv in list(join_node.left_vars.keys()):
        join_node.left_vars[hlnuo__ctaqv] = replace_vars_inner(join_node.
            left_vars[hlnuo__ctaqv], var_dict)
    for hlnuo__ctaqv in list(join_node.right_vars.keys()):
        join_node.right_vars[hlnuo__ctaqv] = replace_vars_inner(join_node.
            right_vars[hlnuo__ctaqv], var_dict)
    for hlnuo__ctaqv in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[hlnuo__ctaqv] = replace_vars_inner(join_node
            .out_data_vars[hlnuo__ctaqv], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for stxe__ucz in join_node.out_data_vars.values():
        definitions[stxe__ucz.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    otho__cwbwj = tuple(join_node.left_vars[mrcch__flxb] for mrcch__flxb in
        join_node.left_keys)
    sdkv__gord = tuple(join_node.right_vars[mrcch__flxb] for mrcch__flxb in
        join_node.right_keys)
    mvoj__xqsw = tuple(join_node.left_vars.keys())
    ryul__jemez = tuple(join_node.right_vars.keys())
    dzk__acgwo = ()
    syr__vmt = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        ixg__obl = join_node.right_keys[0]
        if ixg__obl in mvoj__xqsw:
            syr__vmt = ixg__obl,
            dzk__acgwo = join_node.right_vars[ixg__obl],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        ixg__obl = join_node.left_keys[0]
        if ixg__obl in ryul__jemez:
            syr__vmt = ixg__obl,
            dzk__acgwo = join_node.left_vars[ixg__obl],
            optional_column = True
    jjwb__lwoqs = tuple(join_node.out_data_vars[cname] for cname in syr__vmt)
    oska__umg = tuple(iqcph__cxt for txdj__gvn, iqcph__cxt in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if txdj__gvn
         not in join_node.left_keys)
    prtgi__duu = tuple(iqcph__cxt for txdj__gvn, iqcph__cxt in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if txdj__gvn
         not in join_node.right_keys)
    oohhq__mnmp = (dzk__acgwo + otho__cwbwj + sdkv__gord + oska__umg +
        prtgi__duu)
    yjpsb__xdog = tuple(typemap[iqcph__cxt.name] for iqcph__cxt in oohhq__mnmp)
    pebi__hzy = tuple('opti_c' + str(ztbxz__povs) for ztbxz__povs in range(
        len(dzk__acgwo)))
    left_other_names = tuple('t1_c' + str(ztbxz__povs) for ztbxz__povs in
        range(len(oska__umg)))
    right_other_names = tuple('t2_c' + str(ztbxz__povs) for ztbxz__povs in
        range(len(prtgi__duu)))
    left_other_types = tuple([typemap[mrcch__flxb.name] for mrcch__flxb in
        oska__umg])
    right_other_types = tuple([typemap[mrcch__flxb.name] for mrcch__flxb in
        prtgi__duu])
    left_key_names = tuple('t1_key' + str(ztbxz__povs) for ztbxz__povs in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(ztbxz__povs) for ztbxz__povs in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(pebi__hzy[0
        ]) if len(pebi__hzy) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[iqcph__cxt.name] for iqcph__cxt in
        otho__cwbwj)
    right_key_types = tuple(typemap[iqcph__cxt.name] for iqcph__cxt in
        sdkv__gord)
    for ztbxz__povs in range(n_keys):
        glbs[f'key_type_{ztbxz__povs}'] = _match_join_key_types(left_key_types
            [ztbxz__povs], right_key_types[ztbxz__povs], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[ztbxz__povs]}, key_type_{ztbxz__povs})'
         for ztbxz__povs in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[ztbxz__povs]}, key_type_{ztbxz__povs})'
         for ztbxz__povs in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    rxx__pkuc = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            flo__kzlan = str(cname) + join_node.suffix_x
        else:
            flo__kzlan = cname
        assert flo__kzlan in join_node.out_data_vars
        rxx__pkuc.append(join_node.out_data_vars[flo__kzlan])
    for ztbxz__povs, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[ztbxz__povs] and not join_node.is_join:
            if cname in join_node.add_suffix:
                flo__kzlan = str(cname) + join_node.suffix_y
            else:
                flo__kzlan = cname
            assert flo__kzlan in join_node.out_data_vars
            rxx__pkuc.append(join_node.out_data_vars[flo__kzlan])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                flo__kzlan = str(cname) + join_node.suffix_x
            else:
                flo__kzlan = str(cname) + join_node.suffix_y
        else:
            flo__kzlan = cname
        return join_node.out_data_vars[flo__kzlan]
    kpyl__ovvn = jjwb__lwoqs + tuple(rxx__pkuc)
    kpyl__ovvn += tuple(_get_out_col_var(txdj__gvn, True) for txdj__gvn,
        iqcph__cxt in sorted(join_node.left_vars.items(), key=lambda a: str
        (a[0])) if txdj__gvn not in join_node.left_keys)
    kpyl__ovvn += tuple(_get_out_col_var(txdj__gvn, False) for txdj__gvn,
        iqcph__cxt in sorted(join_node.right_vars.items(), key=lambda a:
        str(a[0])) if txdj__gvn not in join_node.right_keys)
    if join_node.indicator:
        kpyl__ovvn += _get_out_col_var('_merge', False),
    nhnr__wkxs = [('t3_c' + str(ztbxz__povs)) for ztbxz__povs in range(len(
        kpyl__ovvn))]
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
            right_parallel, glbs, [typemap[iqcph__cxt.name] for iqcph__cxt in
            kpyl__ovvn], join_node.loc, join_node.indicator, join_node.
            is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for ztbxz__povs in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(ztbxz__povs
                , ztbxz__povs)
        for ztbxz__povs in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                ztbxz__povs, ztbxz__povs)
        for ztbxz__povs in range(n_keys):
            func_text += (
                f'    t1_keys_{ztbxz__povs} = out_t1_keys[{ztbxz__povs}]\n')
        for ztbxz__povs in range(n_keys):
            func_text += (
                f'    t2_keys_{ztbxz__povs} = out_t2_keys[{ztbxz__povs}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {nhnr__wkxs[idx]} = opti_0\n'
        idx += 1
    for ztbxz__povs in range(n_keys):
        func_text += f'    {nhnr__wkxs[idx]} = t1_keys_{ztbxz__povs}\n'
        idx += 1
    for ztbxz__povs in range(n_keys):
        if not join_node.vect_same_key[ztbxz__povs] and not join_node.is_join:
            func_text += f'    {nhnr__wkxs[idx]} = t2_keys_{ztbxz__povs}\n'
            idx += 1
    for ztbxz__povs in range(len(left_other_names)):
        func_text += f'    {nhnr__wkxs[idx]} = left_{ztbxz__povs}\n'
        idx += 1
    for ztbxz__povs in range(len(right_other_names)):
        func_text += f'    {nhnr__wkxs[idx]} = right_{ztbxz__povs}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {nhnr__wkxs[idx]} = indicator_col\n'
        idx += 1
    wwf__otkbz = {}
    exec(func_text, {}, wwf__otkbz)
    qixv__yuua = wwf__otkbz['f']
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
    jzmba__othb = compile_to_numba_ir(qixv__yuua, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=yjpsb__xdog, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(jzmba__othb, oohhq__mnmp)
    mrumr__tuph = jzmba__othb.body[:-3]
    for ztbxz__povs in range(len(kpyl__ovvn)):
        mrumr__tuph[-len(kpyl__ovvn) + ztbxz__povs].target = kpyl__ovvn[
            ztbxz__povs]
    return mrumr__tuph


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    acnu__ftblc = next_label()
    mxjk__esbkb = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    qeynu__uxb = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{acnu__ftblc}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        mxjk__esbkb, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        qeynu__uxb, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    wwf__otkbz = {}
    exec(func_text, table_getitem_funcs, wwf__otkbz)
    uzgn__xxyvm = wwf__otkbz[f'bodo_join_gen_cond{acnu__ftblc}']
    dssd__mrmij = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    xcztg__fsy = numba.cfunc(dssd__mrmij, nopython=True)(uzgn__xxyvm)
    join_gen_cond_cfunc[xcztg__fsy.native_name] = xcztg__fsy
    join_gen_cond_cfunc_addr[xcztg__fsy.native_name] = xcztg__fsy.address
    return xcztg__fsy, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    spzb__pykqw = []
    for mrcch__flxb, oyp__hwpe in col_to_ind.items():
        cname = f'({table_name}.{mrcch__flxb})'
        if cname not in expr:
            continue
        etv__uvti = f'getitem_{table_name}_val_{oyp__hwpe}'
        opgj__yrxz = f'_bodo_{table_name}_val_{oyp__hwpe}'
        kyubw__vujh = typemap[col_vars[mrcch__flxb].name]
        if is_str_arr_type(kyubw__vujh):
            func_text += f"""  {opgj__yrxz}, {opgj__yrxz}_size = {etv__uvti}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {opgj__yrxz} = bodo.libs.str_arr_ext.decode_utf8({opgj__yrxz}, {opgj__yrxz}_size)
"""
        else:
            func_text += (
                f'  {opgj__yrxz} = {etv__uvti}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[etv__uvti
            ] = bodo.libs.array._gen_row_access_intrinsic(kyubw__vujh,
            oyp__hwpe)
        expr = expr.replace(cname, opgj__yrxz)
        vjrh__fwd = f'({na_check_name}.{table_name}.{mrcch__flxb})'
        if vjrh__fwd in expr:
            jkqq__kpr = f'nacheck_{table_name}_val_{oyp__hwpe}'
            fog__domap = f'_bodo_isna_{table_name}_val_{oyp__hwpe}'
            if (isinstance(kyubw__vujh, bodo.libs.int_arr_ext.
                IntegerArrayType) or kyubw__vujh == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(kyubw__vujh)):
                func_text += f"""  {fog__domap} = {jkqq__kpr}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {fog__domap} = {jkqq__kpr}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[jkqq__kpr
                ] = bodo.libs.array._gen_row_na_check_intrinsic(kyubw__vujh,
                oyp__hwpe)
            expr = expr.replace(vjrh__fwd, fog__domap)
        if oyp__hwpe >= n_keys:
            spzb__pykqw.append(oyp__hwpe)
    return expr, func_text, spzb__pykqw


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {mrcch__flxb: ztbxz__povs for ztbxz__povs, mrcch__flxb in
        enumerate(key_names)}
    ztbxz__povs = n_keys
    for mrcch__flxb in sorted(col_vars, key=lambda a: str(a)):
        if mrcch__flxb in col_to_ind:
            continue
        col_to_ind[mrcch__flxb] = ztbxz__povs
        ztbxz__povs += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as tbedr__iazmb:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    hvck__ndtvw = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[iqcph__cxt.name] in hvck__ndtvw for
        iqcph__cxt in join_node.left_vars.values())
    right_parallel = all(array_dists[iqcph__cxt.name] in hvck__ndtvw for
        iqcph__cxt in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[iqcph__cxt.name] in hvck__ndtvw for
            iqcph__cxt in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[iqcph__cxt.name] in hvck__ndtvw for
            iqcph__cxt in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[iqcph__cxt.name] in hvck__ndtvw for
            iqcph__cxt in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    gtjr__pztmo = []
    for ztbxz__povs in range(len(left_key_names)):
        kzb__yzwr = _match_join_key_types(left_key_types[ztbxz__povs],
            right_key_types[ztbxz__povs], loc)
        gtjr__pztmo.append(needs_typechange(kzb__yzwr, is_right,
            vect_same_key[ztbxz__povs]))
    for ztbxz__povs in range(len(left_other_names)):
        gtjr__pztmo.append(needs_typechange(left_other_types[ztbxz__povs],
            is_right, False))
    for ztbxz__povs in range(len(right_key_names)):
        if not vect_same_key[ztbxz__povs] and not is_join:
            kzb__yzwr = _match_join_key_types(left_key_types[ztbxz__povs],
                right_key_types[ztbxz__povs], loc)
            gtjr__pztmo.append(needs_typechange(kzb__yzwr, is_left, False))
    for ztbxz__povs in range(len(right_other_names)):
        gtjr__pztmo.append(needs_typechange(right_other_types[ztbxz__povs],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                kyvey__sgnlo = IntDtype(in_type.dtype).name
                assert kyvey__sgnlo.endswith('Dtype()')
                kyvey__sgnlo = kyvey__sgnlo[:-7]
                yyxky__czpp = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{kyvey__sgnlo}"))
"""
                uzmo__xia = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                yyxky__czpp = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                uzmo__xia = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            yyxky__czpp = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            uzmo__xia = f'typ_{idx}'
        else:
            yyxky__czpp = ''
            uzmo__xia = in_name
        return yyxky__czpp, uzmo__xia
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    sbu__xcli = []
    for ztbxz__povs in range(n_keys):
        sbu__xcli.append('t1_keys[{}]'.format(ztbxz__povs))
    for ztbxz__povs in range(len(left_other_names)):
        sbu__xcli.append('data_left[{}]'.format(ztbxz__povs))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in sbu__xcli))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    ojkq__bng = []
    for ztbxz__povs in range(n_keys):
        ojkq__bng.append('t2_keys[{}]'.format(ztbxz__povs))
    for ztbxz__povs in range(len(right_other_names)):
        ojkq__bng.append('data_right[{}]'.format(ztbxz__povs))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in ojkq__bng))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        ieppd__smenq else '0' for ieppd__smenq in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if ieppd__smenq else '0' for ieppd__smenq in gtjr__pztmo))
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
        pne__haf = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += pne__haf[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {pne__haf[1]})
"""
        idx += 1
    for ztbxz__povs, cpzz__iza in enumerate(left_key_names):
        kzb__yzwr = _match_join_key_types(left_key_types[ztbxz__povs],
            right_key_types[ztbxz__povs], loc)
        pne__haf = get_out_type(idx, kzb__yzwr, f't1_keys[{ztbxz__povs}]',
            is_right, vect_same_key[ztbxz__povs])
        func_text += pne__haf[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if kzb__yzwr != left_key_types[ztbxz__povs] and left_key_types[
            ztbxz__povs] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{ztbxz__povs} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {pne__haf[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{ztbxz__povs} = info_to_array(info_from_table(out_table, {idx}), {pne__haf[1]})
"""
        idx += 1
    for ztbxz__povs, cpzz__iza in enumerate(left_other_names):
        pne__haf = get_out_type(idx, left_other_types[ztbxz__povs],
            cpzz__iza, is_right, False)
        func_text += pne__haf[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(ztbxz__povs, idx, pne__haf[1]))
        idx += 1
    for ztbxz__povs, cpzz__iza in enumerate(right_key_names):
        if not vect_same_key[ztbxz__povs] and not is_join:
            kzb__yzwr = _match_join_key_types(left_key_types[ztbxz__povs],
                right_key_types[ztbxz__povs], loc)
            pne__haf = get_out_type(idx, kzb__yzwr,
                f't2_keys[{ztbxz__povs}]', is_left, False)
            func_text += pne__haf[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if kzb__yzwr != right_key_types[ztbxz__povs] and right_key_types[
                ztbxz__povs] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{ztbxz__povs} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {pne__haf[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{ztbxz__povs} = info_to_array(info_from_table(out_table, {idx}), {pne__haf[1]})
"""
            idx += 1
    for ztbxz__povs, cpzz__iza in enumerate(right_other_names):
        pne__haf = get_out_type(idx, right_other_types[ztbxz__povs],
            cpzz__iza, is_left, False)
        func_text += pne__haf[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(ztbxz__povs, idx, pne__haf[1]))
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
    stot__lkrrq = bodo.libs.distributed_api.get_size()
    chawz__zoa = np.empty(stot__lkrrq, left_key_arrs[0].dtype)
    ovfif__mxu = np.empty(stot__lkrrq, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(chawz__zoa, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(ovfif__mxu, left_key_arrs[0][-1])
    vzqd__kbov = np.zeros(stot__lkrrq, np.int32)
    ggn__pkij = np.zeros(stot__lkrrq, np.int32)
    iaiz__sdqs = np.zeros(stot__lkrrq, np.int32)
    mmtdh__uvn = right_key_arrs[0][0]
    itxs__peic = right_key_arrs[0][-1]
    ixtz__yui = -1
    ztbxz__povs = 0
    while ztbxz__povs < stot__lkrrq - 1 and ovfif__mxu[ztbxz__povs
        ] < mmtdh__uvn:
        ztbxz__povs += 1
    while ztbxz__povs < stot__lkrrq and chawz__zoa[ztbxz__povs] <= itxs__peic:
        ixtz__yui, djlko__zdch = _count_overlap(right_key_arrs[0],
            chawz__zoa[ztbxz__povs], ovfif__mxu[ztbxz__povs])
        if ixtz__yui != 0:
            ixtz__yui -= 1
            djlko__zdch += 1
        vzqd__kbov[ztbxz__povs] = djlko__zdch
        ggn__pkij[ztbxz__povs] = ixtz__yui
        ztbxz__povs += 1
    while ztbxz__povs < stot__lkrrq:
        vzqd__kbov[ztbxz__povs] = 1
        ggn__pkij[ztbxz__povs] = len(right_key_arrs[0]) - 1
        ztbxz__povs += 1
    bodo.libs.distributed_api.alltoall(vzqd__kbov, iaiz__sdqs, 1)
    blk__jno = iaiz__sdqs.sum()
    dflgn__hulb = np.empty(blk__jno, right_key_arrs[0].dtype)
    pmjp__hfhs = alloc_arr_tup(blk__jno, right_data)
    pyjek__oily = bodo.ir.join.calc_disp(iaiz__sdqs)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], dflgn__hulb,
        vzqd__kbov, iaiz__sdqs, ggn__pkij, pyjek__oily)
    bodo.libs.distributed_api.alltoallv_tup(right_data, pmjp__hfhs,
        vzqd__kbov, iaiz__sdqs, ggn__pkij, pyjek__oily)
    return (dflgn__hulb,), pmjp__hfhs


@numba.njit
def _count_overlap(r_key_arr, start, end):
    djlko__zdch = 0
    ixtz__yui = 0
    ijauz__wzk = 0
    while ijauz__wzk < len(r_key_arr) and r_key_arr[ijauz__wzk] < start:
        ixtz__yui += 1
        ijauz__wzk += 1
    while ijauz__wzk < len(r_key_arr) and start <= r_key_arr[ijauz__wzk
        ] <= end:
        ijauz__wzk += 1
        djlko__zdch += 1
    return ixtz__yui, djlko__zdch


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    pnbb__mhtv = np.empty_like(arr)
    pnbb__mhtv[0] = 0
    for ztbxz__povs in range(1, len(arr)):
        pnbb__mhtv[ztbxz__povs] = pnbb__mhtv[ztbxz__povs - 1] + arr[
            ztbxz__povs - 1]
    return pnbb__mhtv


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    dsqc__kkp = len(left_keys[0])
    bgp__oiyuk = len(right_keys[0])
    xwqcu__lqj = alloc_arr_tup(dsqc__kkp, left_keys)
    hta__jzmlj = alloc_arr_tup(dsqc__kkp, right_keys)
    swrl__zfi = alloc_arr_tup(dsqc__kkp, data_left)
    vrrf__mjkbp = alloc_arr_tup(dsqc__kkp, data_right)
    ieaqq__jmor = 0
    vwj__ffhi = 0
    for ieaqq__jmor in range(dsqc__kkp):
        if vwj__ffhi < 0:
            vwj__ffhi = 0
        while vwj__ffhi < bgp__oiyuk and getitem_arr_tup(right_keys, vwj__ffhi
            ) <= getitem_arr_tup(left_keys, ieaqq__jmor):
            vwj__ffhi += 1
        vwj__ffhi -= 1
        setitem_arr_tup(xwqcu__lqj, ieaqq__jmor, getitem_arr_tup(left_keys,
            ieaqq__jmor))
        setitem_arr_tup(swrl__zfi, ieaqq__jmor, getitem_arr_tup(data_left,
            ieaqq__jmor))
        if vwj__ffhi >= 0:
            setitem_arr_tup(hta__jzmlj, ieaqq__jmor, getitem_arr_tup(
                right_keys, vwj__ffhi))
            setitem_arr_tup(vrrf__mjkbp, ieaqq__jmor, getitem_arr_tup(
                data_right, vwj__ffhi))
        else:
            bodo.libs.array_kernels.setna_tup(hta__jzmlj, ieaqq__jmor)
            bodo.libs.array_kernels.setna_tup(vrrf__mjkbp, ieaqq__jmor)
    return xwqcu__lqj, hta__jzmlj, swrl__zfi, vrrf__mjkbp


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    djlko__zdch = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(ztbxz__povs) for ztbxz__povs in range(djlko__zdch)))
    wwf__otkbz = {}
    exec(func_text, {}, wwf__otkbz)
    vtxb__bxnsl = wwf__otkbz['f']
    return vtxb__bxnsl
