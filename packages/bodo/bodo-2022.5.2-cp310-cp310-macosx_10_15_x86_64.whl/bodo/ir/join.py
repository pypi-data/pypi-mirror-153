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
        pxqo__sdqj = func.signature
        vjcox__edozd = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        xdrlo__bjsks = cgutils.get_or_insert_function(builder.module,
            vjcox__edozd, sym._literal_value)
        builder.call(xdrlo__bjsks, [context.get_constant_null(pxqo__sdqj.
            args[0]), context.get_constant_null(pxqo__sdqj.args[1]),
            context.get_constant_null(pxqo__sdqj.args[2]), context.
            get_constant_null(pxqo__sdqj.args[3]), context.
            get_constant_null(pxqo__sdqj.args[4]), context.
            get_constant_null(pxqo__sdqj.args[5]), context.get_constant(
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
            self.left_cond_cols = set(hfxvv__fuwb for hfxvv__fuwb in
                left_vars.keys() if f'(left.{hfxvv__fuwb})' in gen_cond_expr)
            self.right_cond_cols = set(hfxvv__fuwb for hfxvv__fuwb in
                right_vars.keys() if f'(right.{hfxvv__fuwb})' in gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        pdc__plyy = self.left_key_set & self.right_key_set
        huuoj__cdfyi = set(left_vars.keys()) & set(right_vars.keys())
        fod__ecko = huuoj__cdfyi - pdc__plyy
        vect_same_key = []
        n_keys = len(left_keys)
        for hgw__tcob in range(n_keys):
            dvwx__ztzz = left_keys[hgw__tcob]
            qtu__chx = right_keys[hgw__tcob]
            vect_same_key.append(dvwx__ztzz == qtu__chx)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(hfxvv__fuwb) + suffix_left if 
            hfxvv__fuwb in fod__ecko else hfxvv__fuwb): ('left',
            hfxvv__fuwb) for hfxvv__fuwb in left_vars.keys()}
        self.column_origins.update({(str(hfxvv__fuwb) + suffix_right if 
            hfxvv__fuwb in fod__ecko else hfxvv__fuwb): ('right',
            hfxvv__fuwb) for hfxvv__fuwb in right_vars.keys()})
        if '$_bodo_index_' in fod__ecko:
            fod__ecko.remove('$_bodo_index_')
        self.add_suffix = fod__ecko

    def __repr__(self):
        zydio__ppful = ''
        for hfxvv__fuwb, ees__ymla in self.out_data_vars.items():
            zydio__ppful += "'{}':{}, ".format(hfxvv__fuwb, ees__ymla.name)
        mupl__zyop = '{}{{{}}}'.format(self.df_out, zydio__ppful)
        pdoc__pbory = ''
        for hfxvv__fuwb, ees__ymla in self.left_vars.items():
            pdoc__pbory += "'{}':{}, ".format(hfxvv__fuwb, ees__ymla.name)
        rtpbt__jdvdy = '{}{{{}}}'.format(self.left_df, pdoc__pbory)
        pdoc__pbory = ''
        for hfxvv__fuwb, ees__ymla in self.right_vars.items():
            pdoc__pbory += "'{}':{}, ".format(hfxvv__fuwb, ees__ymla.name)
        twp__yjebm = '{}{{{}}}'.format(self.right_df, pdoc__pbory)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, mupl__zyop, rtpbt__jdvdy, twp__yjebm)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    avgi__dywk = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    neofe__gphan = []
    aqmqa__ntagk = list(join_node.left_vars.values())
    for akgtv__mcl in aqmqa__ntagk:
        nffb__yimq = typemap[akgtv__mcl.name]
        fymq__hizxp = equiv_set.get_shape(akgtv__mcl)
        if fymq__hizxp:
            neofe__gphan.append(fymq__hizxp[0])
    if len(neofe__gphan) > 1:
        equiv_set.insert_equiv(*neofe__gphan)
    neofe__gphan = []
    aqmqa__ntagk = list(join_node.right_vars.values())
    for akgtv__mcl in aqmqa__ntagk:
        nffb__yimq = typemap[akgtv__mcl.name]
        fymq__hizxp = equiv_set.get_shape(akgtv__mcl)
        if fymq__hizxp:
            neofe__gphan.append(fymq__hizxp[0])
    if len(neofe__gphan) > 1:
        equiv_set.insert_equiv(*neofe__gphan)
    neofe__gphan = []
    for akgtv__mcl in join_node.out_data_vars.values():
        nffb__yimq = typemap[akgtv__mcl.name]
        drqbw__ubhzb = array_analysis._gen_shape_call(equiv_set, akgtv__mcl,
            nffb__yimq.ndim, None, avgi__dywk)
        equiv_set.insert_equiv(akgtv__mcl, drqbw__ubhzb)
        neofe__gphan.append(drqbw__ubhzb[0])
        equiv_set.define(akgtv__mcl, set())
    if len(neofe__gphan) > 1:
        equiv_set.insert_equiv(*neofe__gphan)
    return [], avgi__dywk


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    ppq__jqyhq = Distribution.OneD
    hcxwv__qve = Distribution.OneD
    for akgtv__mcl in join_node.left_vars.values():
        ppq__jqyhq = Distribution(min(ppq__jqyhq.value, array_dists[
            akgtv__mcl.name].value))
    for akgtv__mcl in join_node.right_vars.values():
        hcxwv__qve = Distribution(min(hcxwv__qve.value, array_dists[
            akgtv__mcl.name].value))
    jdzpx__yznwp = Distribution.OneD_Var
    for akgtv__mcl in join_node.out_data_vars.values():
        if akgtv__mcl.name in array_dists:
            jdzpx__yznwp = Distribution(min(jdzpx__yznwp.value, array_dists
                [akgtv__mcl.name].value))
    mjeu__ponh = Distribution(min(jdzpx__yznwp.value, ppq__jqyhq.value))
    lchc__ndf = Distribution(min(jdzpx__yznwp.value, hcxwv__qve.value))
    jdzpx__yznwp = Distribution(max(mjeu__ponh.value, lchc__ndf.value))
    for akgtv__mcl in join_node.out_data_vars.values():
        array_dists[akgtv__mcl.name] = jdzpx__yznwp
    if jdzpx__yznwp != Distribution.OneD_Var:
        ppq__jqyhq = jdzpx__yznwp
        hcxwv__qve = jdzpx__yznwp
    for akgtv__mcl in join_node.left_vars.values():
        array_dists[akgtv__mcl.name] = ppq__jqyhq
    for akgtv__mcl in join_node.right_vars.values():
        array_dists[akgtv__mcl.name] = hcxwv__qve
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    for hdy__nqcg, cmpf__tek in join_node.out_data_vars.items():
        if join_node.indicator and hdy__nqcg == '_merge':
            continue
        if not hdy__nqcg in join_node.column_origins:
            raise BodoError('join(): The variable ' + hdy__nqcg +
                ' is absent from the output')
        mwpl__yct = join_node.column_origins[hdy__nqcg]
        if mwpl__yct[0] == 'left':
            akgtv__mcl = join_node.left_vars[mwpl__yct[1]]
        else:
            akgtv__mcl = join_node.right_vars[mwpl__yct[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=cmpf__tek.
            name, src=akgtv__mcl.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for hjtn__qsgjk in list(join_node.left_vars.keys()):
        join_node.left_vars[hjtn__qsgjk] = visit_vars_inner(join_node.
            left_vars[hjtn__qsgjk], callback, cbdata)
    for hjtn__qsgjk in list(join_node.right_vars.keys()):
        join_node.right_vars[hjtn__qsgjk] = visit_vars_inner(join_node.
            right_vars[hjtn__qsgjk], callback, cbdata)
    for hjtn__qsgjk in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[hjtn__qsgjk] = visit_vars_inner(join_node.
            out_data_vars[hjtn__qsgjk], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    sqlaw__qnh = []
    rztiu__pje = True
    for hjtn__qsgjk, akgtv__mcl in join_node.out_data_vars.items():
        if akgtv__mcl.name in lives:
            rztiu__pje = False
            continue
        if hjtn__qsgjk == '$_bodo_index_':
            continue
        if join_node.indicator and hjtn__qsgjk == '_merge':
            sqlaw__qnh.append('_merge')
            join_node.indicator = False
            continue
        xdy__gcdm, nkji__rbzky = join_node.column_origins[hjtn__qsgjk]
        if (xdy__gcdm == 'left' and nkji__rbzky not in join_node.
            left_key_set and nkji__rbzky not in join_node.left_cond_cols):
            join_node.left_vars.pop(nkji__rbzky)
            sqlaw__qnh.append(hjtn__qsgjk)
        if (xdy__gcdm == 'right' and nkji__rbzky not in join_node.
            right_key_set and nkji__rbzky not in join_node.right_cond_cols):
            join_node.right_vars.pop(nkji__rbzky)
            sqlaw__qnh.append(hjtn__qsgjk)
    for cname in sqlaw__qnh:
        join_node.out_data_vars.pop(cname)
    if rztiu__pje:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({ees__ymla.name for ees__ymla in join_node.left_vars.
        values()})
    use_set.update({ees__ymla.name for ees__ymla in join_node.right_vars.
        values()})
    def_set.update({ees__ymla.name for ees__ymla in join_node.out_data_vars
        .values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    gokyq__lnzi = set(ees__ymla.name for ees__ymla in join_node.
        out_data_vars.values())
    return set(), gokyq__lnzi


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for hjtn__qsgjk in list(join_node.left_vars.keys()):
        join_node.left_vars[hjtn__qsgjk] = replace_vars_inner(join_node.
            left_vars[hjtn__qsgjk], var_dict)
    for hjtn__qsgjk in list(join_node.right_vars.keys()):
        join_node.right_vars[hjtn__qsgjk] = replace_vars_inner(join_node.
            right_vars[hjtn__qsgjk], var_dict)
    for hjtn__qsgjk in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[hjtn__qsgjk] = replace_vars_inner(join_node
            .out_data_vars[hjtn__qsgjk], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for akgtv__mcl in join_node.out_data_vars.values():
        definitions[akgtv__mcl.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    yvep__title = tuple(join_node.left_vars[hfxvv__fuwb] for hfxvv__fuwb in
        join_node.left_keys)
    mcpy__wzgoo = tuple(join_node.right_vars[hfxvv__fuwb] for hfxvv__fuwb in
        join_node.right_keys)
    left_vars = join_node.left_vars
    right_vars = join_node.right_vars
    pwkg__zsrl = ()
    fckhz__oiyt = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        rols__cczr = join_node.right_keys[0]
        if rols__cczr in left_vars:
            fckhz__oiyt = rols__cczr,
            pwkg__zsrl = join_node.right_vars[rols__cczr],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        rols__cczr = join_node.left_keys[0]
        if rols__cczr in right_vars:
            fckhz__oiyt = rols__cczr,
            pwkg__zsrl = join_node.left_vars[rols__cczr],
            optional_column = True
    gneqt__vriqz = [join_node.out_data_vars[cname] for cname in fckhz__oiyt]
    iijr__vix = tuple(ees__ymla for vgj__zbuz, ees__ymla in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if vgj__zbuz
         not in join_node.left_key_set)
    qds__zekbg = tuple(ees__ymla for vgj__zbuz, ees__ymla in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if vgj__zbuz
         not in join_node.right_key_set)
    zjgm__gyxen = (pwkg__zsrl + yvep__title + mcpy__wzgoo + iijr__vix +
        qds__zekbg)
    ewi__ywu = tuple(typemap[ees__ymla.name] for ees__ymla in zjgm__gyxen)
    djw__cgp = tuple('opti_c' + str(kpkcf__kflp) for kpkcf__kflp in range(
        len(pwkg__zsrl)))
    left_other_names = tuple('t1_c' + str(kpkcf__kflp) for kpkcf__kflp in
        range(len(iijr__vix)))
    right_other_names = tuple('t2_c' + str(kpkcf__kflp) for kpkcf__kflp in
        range(len(qds__zekbg)))
    left_other_types = tuple([typemap[hfxvv__fuwb.name] for hfxvv__fuwb in
        iijr__vix])
    right_other_types = tuple([typemap[hfxvv__fuwb.name] for hfxvv__fuwb in
        qds__zekbg])
    left_key_names = tuple('t1_key' + str(kpkcf__kflp) for kpkcf__kflp in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(kpkcf__kflp) for kpkcf__kflp in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(djw__cgp[0]
        ) if len(djw__cgp) == 1 else '', ','.join(left_key_names), ','.join
        (right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[ees__ymla.name] for ees__ymla in yvep__title
        )
    right_key_types = tuple(typemap[ees__ymla.name] for ees__ymla in
        mcpy__wzgoo)
    for kpkcf__kflp in range(n_keys):
        glbs[f'key_type_{kpkcf__kflp}'] = _match_join_key_types(left_key_types
            [kpkcf__kflp], right_key_types[kpkcf__kflp], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[kpkcf__kflp]}, key_type_{kpkcf__kflp})'
         for kpkcf__kflp in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[kpkcf__kflp]}, key_type_{kpkcf__kflp})'
         for kpkcf__kflp in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            ksxd__jskrq = str(cname) + join_node.suffix_left
        else:
            ksxd__jskrq = cname
        assert ksxd__jskrq in join_node.out_data_vars
        gneqt__vriqz.append(join_node.out_data_vars[ksxd__jskrq])
    for kpkcf__kflp, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[kpkcf__kflp] and not join_node.is_join:
            if cname in join_node.add_suffix:
                ksxd__jskrq = str(cname) + join_node.suffix_right
            else:
                ksxd__jskrq = cname
            assert ksxd__jskrq in join_node.out_data_vars
            gneqt__vriqz.append(join_node.out_data_vars[ksxd__jskrq])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                ksxd__jskrq = str(cname) + join_node.suffix_left
            else:
                ksxd__jskrq = str(cname) + join_node.suffix_right
        else:
            ksxd__jskrq = cname
        return join_node.out_data_vars[ksxd__jskrq]
    for vgj__zbuz in sorted(join_node.left_vars.keys(), key=lambda a: str(a)):
        if vgj__zbuz not in join_node.left_key_set:
            gneqt__vriqz.append(_get_out_col_var(vgj__zbuz, True))
    for vgj__zbuz in sorted(join_node.right_vars.keys(), key=lambda a: str(a)):
        if vgj__zbuz not in join_node.right_key_set:
            gneqt__vriqz.append(_get_out_col_var(vgj__zbuz, False))
    if join_node.indicator:
        gneqt__vriqz.append(_get_out_col_var('_merge', False))
    viwni__hwe = [('t3_c' + str(kpkcf__kflp)) for kpkcf__kflp in range(len(
        gneqt__vriqz))]
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
            right_parallel, glbs, [typemap[ees__ymla.name] for ees__ymla in
            gneqt__vriqz], join_node.loc, join_node.indicator, join_node.
            is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for kpkcf__kflp in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(kpkcf__kflp
                , kpkcf__kflp)
        for kpkcf__kflp in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                kpkcf__kflp, kpkcf__kflp)
        for kpkcf__kflp in range(n_keys):
            func_text += (
                f'    t1_keys_{kpkcf__kflp} = out_t1_keys[{kpkcf__kflp}]\n')
        for kpkcf__kflp in range(n_keys):
            func_text += (
                f'    t2_keys_{kpkcf__kflp} = out_t2_keys[{kpkcf__kflp}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {viwni__hwe[idx]} = opti_0\n'
        idx += 1
    for kpkcf__kflp in range(n_keys):
        func_text += f'    {viwni__hwe[idx]} = t1_keys_{kpkcf__kflp}\n'
        idx += 1
    for kpkcf__kflp in range(n_keys):
        if not join_node.vect_same_key[kpkcf__kflp] and not join_node.is_join:
            func_text += f'    {viwni__hwe[idx]} = t2_keys_{kpkcf__kflp}\n'
            idx += 1
    for kpkcf__kflp in range(len(left_other_names)):
        func_text += f'    {viwni__hwe[idx]} = left_{kpkcf__kflp}\n'
        idx += 1
    for kpkcf__kflp in range(len(right_other_names)):
        func_text += f'    {viwni__hwe[idx]} = right_{kpkcf__kflp}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {viwni__hwe[idx]} = indicator_col\n'
        idx += 1
    vplf__mgp = {}
    exec(func_text, {}, vplf__mgp)
    fopb__kgcw = vplf__mgp['f']
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
    umcl__mbj = compile_to_numba_ir(fopb__kgcw, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=ewi__ywu, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(umcl__mbj, zjgm__gyxen)
    dldd__nak = umcl__mbj.body[:-3]
    for kpkcf__kflp in range(len(gneqt__vriqz)):
        dldd__nak[-len(gneqt__vriqz) + kpkcf__kflp].target = gneqt__vriqz[
            kpkcf__kflp]
    return dldd__nak


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    lee__jsfkm = next_label()
    dogfu__ylds = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    iwd__zndz = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{lee__jsfkm}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        dogfu__ylds, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        iwd__zndz, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    vplf__mgp = {}
    exec(func_text, table_getitem_funcs, vplf__mgp)
    isb__moa = vplf__mgp[f'bodo_join_gen_cond{lee__jsfkm}']
    fcc__scp = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    cvlc__xlgyv = numba.cfunc(fcc__scp, nopython=True)(isb__moa)
    join_gen_cond_cfunc[cvlc__xlgyv.native_name] = cvlc__xlgyv
    join_gen_cond_cfunc_addr[cvlc__xlgyv.native_name] = cvlc__xlgyv.address
    return cvlc__xlgyv, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    kuszu__ipok = []
    for hfxvv__fuwb, pwax__sukvy in col_to_ind.items():
        cname = f'({table_name}.{hfxvv__fuwb})'
        if cname not in expr:
            continue
        myur__ufr = f'getitem_{table_name}_val_{pwax__sukvy}'
        vdf__hdiy = f'_bodo_{table_name}_val_{pwax__sukvy}'
        bjyip__eyjl = typemap[col_vars[hfxvv__fuwb].name]
        if is_str_arr_type(bjyip__eyjl):
            func_text += f"""  {vdf__hdiy}, {vdf__hdiy}_size = {myur__ufr}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {vdf__hdiy} = bodo.libs.str_arr_ext.decode_utf8({vdf__hdiy}, {vdf__hdiy}_size)
"""
        else:
            func_text += (
                f'  {vdf__hdiy} = {myur__ufr}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[myur__ufr
            ] = bodo.libs.array._gen_row_access_intrinsic(bjyip__eyjl,
            pwax__sukvy)
        expr = expr.replace(cname, vdf__hdiy)
        ttgi__llyf = f'({na_check_name}.{table_name}.{hfxvv__fuwb})'
        if ttgi__llyf in expr:
            quv__mcwkr = f'nacheck_{table_name}_val_{pwax__sukvy}'
            quekj__jiacj = f'_bodo_isna_{table_name}_val_{pwax__sukvy}'
            if (isinstance(bjyip__eyjl, bodo.libs.int_arr_ext.
                IntegerArrayType) or bjyip__eyjl == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(bjyip__eyjl)):
                func_text += f"""  {quekj__jiacj} = {quv__mcwkr}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {quekj__jiacj} = {quv__mcwkr}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[quv__mcwkr
                ] = bodo.libs.array._gen_row_na_check_intrinsic(bjyip__eyjl,
                pwax__sukvy)
            expr = expr.replace(ttgi__llyf, quekj__jiacj)
        if pwax__sukvy >= n_keys:
            kuszu__ipok.append(pwax__sukvy)
    return expr, func_text, kuszu__ipok


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {hfxvv__fuwb: kpkcf__kflp for kpkcf__kflp, hfxvv__fuwb in
        enumerate(key_names)}
    kpkcf__kflp = n_keys
    for hfxvv__fuwb in sorted(col_vars, key=lambda a: str(a)):
        if hfxvv__fuwb in col_to_ind:
            continue
        col_to_ind[hfxvv__fuwb] = kpkcf__kflp
        kpkcf__kflp += 1
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
    except Exception as xgpp__wghv:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    kmln__mzze = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[ees__ymla.name] in kmln__mzze for
        ees__ymla in join_node.left_vars.values())
    right_parallel = all(array_dists[ees__ymla.name] in kmln__mzze for
        ees__ymla in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[ees__ymla.name] in kmln__mzze for
            ees__ymla in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[ees__ymla.name] in kmln__mzze for
            ees__ymla in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[ees__ymla.name] in kmln__mzze for ees__ymla in
            join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    kdh__hjs = []
    for kpkcf__kflp in range(len(left_key_names)):
        zyeo__rgfc = _match_join_key_types(left_key_types[kpkcf__kflp],
            right_key_types[kpkcf__kflp], loc)
        kdh__hjs.append(needs_typechange(zyeo__rgfc, is_right,
            vect_same_key[kpkcf__kflp]))
    for kpkcf__kflp in range(len(left_other_names)):
        kdh__hjs.append(needs_typechange(left_other_types[kpkcf__kflp],
            is_right, False))
    for kpkcf__kflp in range(len(right_key_names)):
        if not vect_same_key[kpkcf__kflp] and not is_join:
            zyeo__rgfc = _match_join_key_types(left_key_types[kpkcf__kflp],
                right_key_types[kpkcf__kflp], loc)
            kdh__hjs.append(needs_typechange(zyeo__rgfc, is_left, False))
    for kpkcf__kflp in range(len(right_other_names)):
        kdh__hjs.append(needs_typechange(right_other_types[kpkcf__kflp],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                ougo__xcn = IntDtype(in_type.dtype).name
                assert ougo__xcn.endswith('Dtype()')
                ougo__xcn = ougo__xcn[:-7]
                haohu__qfp = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{ougo__xcn}"))
"""
                vexd__vmbvl = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                haohu__qfp = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                vexd__vmbvl = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            haohu__qfp = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            vexd__vmbvl = f'typ_{idx}'
        else:
            haohu__qfp = ''
            vexd__vmbvl = in_name
        return haohu__qfp, vexd__vmbvl
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    vpgv__ffqb = []
    for kpkcf__kflp in range(n_keys):
        vpgv__ffqb.append('t1_keys[{}]'.format(kpkcf__kflp))
    for kpkcf__kflp in range(len(left_other_names)):
        vpgv__ffqb.append('data_left[{}]'.format(kpkcf__kflp))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in vpgv__ffqb))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    mcov__wae = []
    for kpkcf__kflp in range(n_keys):
        mcov__wae.append('t2_keys[{}]'.format(kpkcf__kflp))
    for kpkcf__kflp in range(len(right_other_names)):
        mcov__wae.append('data_right[{}]'.format(kpkcf__kflp))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in mcov__wae))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        imz__dtqsu else '0' for imz__dtqsu in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if imz__dtqsu else '0' for imz__dtqsu in kdh__hjs))
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
        sqf__zcez = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += sqf__zcez[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {sqf__zcez[1]})
"""
        idx += 1
    for kpkcf__kflp, guolt__tlq in enumerate(left_key_names):
        zyeo__rgfc = _match_join_key_types(left_key_types[kpkcf__kflp],
            right_key_types[kpkcf__kflp], loc)
        sqf__zcez = get_out_type(idx, zyeo__rgfc, f't1_keys[{kpkcf__kflp}]',
            is_right, vect_same_key[kpkcf__kflp])
        func_text += sqf__zcez[0]
        func_text += f"""    t1_keys_{kpkcf__kflp} = info_to_array(info_from_table(out_table, {idx}), {sqf__zcez[1]})
"""
        idx += 1
    for kpkcf__kflp, guolt__tlq in enumerate(left_other_names):
        sqf__zcez = get_out_type(idx, left_other_types[kpkcf__kflp],
            guolt__tlq, is_right, False)
        func_text += sqf__zcez[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(kpkcf__kflp, idx, sqf__zcez[1]))
        idx += 1
    for kpkcf__kflp, guolt__tlq in enumerate(right_key_names):
        if not vect_same_key[kpkcf__kflp] and not is_join:
            zyeo__rgfc = _match_join_key_types(left_key_types[kpkcf__kflp],
                right_key_types[kpkcf__kflp], loc)
            sqf__zcez = get_out_type(idx, zyeo__rgfc,
                f't2_keys[{kpkcf__kflp}]', is_left, False)
            func_text += sqf__zcez[0]
            func_text += f"""    t2_keys_{kpkcf__kflp} = info_to_array(info_from_table(out_table, {idx}), {sqf__zcez[1]})
"""
            idx += 1
    for kpkcf__kflp, guolt__tlq in enumerate(right_other_names):
        sqf__zcez = get_out_type(idx, right_other_types[kpkcf__kflp],
            guolt__tlq, is_left, False)
        func_text += sqf__zcez[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(kpkcf__kflp, idx, sqf__zcez[1]))
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
    jotxj__uwg = bodo.libs.distributed_api.get_size()
    nfqc__yvjlw = np.empty(jotxj__uwg, left_key_arrs[0].dtype)
    uymkj__ppa = np.empty(jotxj__uwg, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(nfqc__yvjlw, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(uymkj__ppa, left_key_arrs[0][-1])
    ujqt__jflif = np.zeros(jotxj__uwg, np.int32)
    hoq__atr = np.zeros(jotxj__uwg, np.int32)
    ytzu__cqne = np.zeros(jotxj__uwg, np.int32)
    fyp__luji = right_key_arrs[0][0]
    ggeqc__uvhb = right_key_arrs[0][-1]
    vhguc__gxu = -1
    kpkcf__kflp = 0
    while kpkcf__kflp < jotxj__uwg - 1 and uymkj__ppa[kpkcf__kflp] < fyp__luji:
        kpkcf__kflp += 1
    while kpkcf__kflp < jotxj__uwg and nfqc__yvjlw[kpkcf__kflp] <= ggeqc__uvhb:
        vhguc__gxu, ctx__wdtho = _count_overlap(right_key_arrs[0],
            nfqc__yvjlw[kpkcf__kflp], uymkj__ppa[kpkcf__kflp])
        if vhguc__gxu != 0:
            vhguc__gxu -= 1
            ctx__wdtho += 1
        ujqt__jflif[kpkcf__kflp] = ctx__wdtho
        hoq__atr[kpkcf__kflp] = vhguc__gxu
        kpkcf__kflp += 1
    while kpkcf__kflp < jotxj__uwg:
        ujqt__jflif[kpkcf__kflp] = 1
        hoq__atr[kpkcf__kflp] = len(right_key_arrs[0]) - 1
        kpkcf__kflp += 1
    bodo.libs.distributed_api.alltoall(ujqt__jflif, ytzu__cqne, 1)
    owmf__xyc = ytzu__cqne.sum()
    psp__xbid = np.empty(owmf__xyc, right_key_arrs[0].dtype)
    zinwg__yek = alloc_arr_tup(owmf__xyc, right_data)
    axrn__kfjn = bodo.ir.join.calc_disp(ytzu__cqne)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], psp__xbid,
        ujqt__jflif, ytzu__cqne, hoq__atr, axrn__kfjn)
    bodo.libs.distributed_api.alltoallv_tup(right_data, zinwg__yek,
        ujqt__jflif, ytzu__cqne, hoq__atr, axrn__kfjn)
    return (psp__xbid,), zinwg__yek


@numba.njit
def _count_overlap(r_key_arr, start, end):
    ctx__wdtho = 0
    vhguc__gxu = 0
    lbfrv__zfik = 0
    while lbfrv__zfik < len(r_key_arr) and r_key_arr[lbfrv__zfik] < start:
        vhguc__gxu += 1
        lbfrv__zfik += 1
    while lbfrv__zfik < len(r_key_arr) and start <= r_key_arr[lbfrv__zfik
        ] <= end:
        lbfrv__zfik += 1
        ctx__wdtho += 1
    return vhguc__gxu, ctx__wdtho


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    hyxn__pok = np.empty_like(arr)
    hyxn__pok[0] = 0
    for kpkcf__kflp in range(1, len(arr)):
        hyxn__pok[kpkcf__kflp] = hyxn__pok[kpkcf__kflp - 1] + arr[
            kpkcf__kflp - 1]
    return hyxn__pok


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    jib__jzpm = len(left_keys[0])
    ekrnn__cag = len(right_keys[0])
    wzejf__uibh = alloc_arr_tup(jib__jzpm, left_keys)
    fmlz__mwgfe = alloc_arr_tup(jib__jzpm, right_keys)
    nhfk__nverh = alloc_arr_tup(jib__jzpm, data_left)
    iho__vvv = alloc_arr_tup(jib__jzpm, data_right)
    sfy__pxs = 0
    lxmx__bhu = 0
    for sfy__pxs in range(jib__jzpm):
        if lxmx__bhu < 0:
            lxmx__bhu = 0
        while lxmx__bhu < ekrnn__cag and getitem_arr_tup(right_keys, lxmx__bhu
            ) <= getitem_arr_tup(left_keys, sfy__pxs):
            lxmx__bhu += 1
        lxmx__bhu -= 1
        setitem_arr_tup(wzejf__uibh, sfy__pxs, getitem_arr_tup(left_keys,
            sfy__pxs))
        setitem_arr_tup(nhfk__nverh, sfy__pxs, getitem_arr_tup(data_left,
            sfy__pxs))
        if lxmx__bhu >= 0:
            setitem_arr_tup(fmlz__mwgfe, sfy__pxs, getitem_arr_tup(
                right_keys, lxmx__bhu))
            setitem_arr_tup(iho__vvv, sfy__pxs, getitem_arr_tup(data_right,
                lxmx__bhu))
        else:
            bodo.libs.array_kernels.setna_tup(fmlz__mwgfe, sfy__pxs)
            bodo.libs.array_kernels.setna_tup(iho__vvv, sfy__pxs)
    return wzejf__uibh, fmlz__mwgfe, nhfk__nverh, iho__vvv
