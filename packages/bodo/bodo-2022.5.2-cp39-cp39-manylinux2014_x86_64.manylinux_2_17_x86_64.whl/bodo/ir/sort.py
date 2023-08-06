"""IR node for the data sorting"""
from collections import defaultdict
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
import bodo.libs.timsort
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, sort_values_table
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints, gen_getitem
MIN_SAMPLES = 1000000
samplePointsPerPartitionHint = 20
MPI_ROOT = 0


class Sort(ir.Stmt):

    def __init__(self, df_in, df_out, key_arrs, out_key_arrs, df_in_vars,
        df_out_vars, inplace, loc, ascending_list=True, na_position='last'):
        self.df_in = df_in
        self.df_out = df_out
        self.key_arrs = key_arrs
        self.out_key_arrs = out_key_arrs
        self.df_in_vars = df_in_vars
        self.df_out_vars = df_out_vars
        self.inplace = inplace
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_arrs)
            else:
                self.na_position_b = (False,) * len(key_arrs)
        else:
            self.na_position_b = tuple([(True if qxn__ogysu == 'last' else 
                False) for qxn__ogysu in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        cktiy__hqfzv = ''
        for vce__bjexj, jnlqk__koya in self.df_in_vars.items():
            cktiy__hqfzv += "'{}':{}, ".format(vce__bjexj, jnlqk__koya.name)
        fse__obga = '{}{{{}}}'.format(self.df_in, cktiy__hqfzv)
        slh__hwxay = ''
        for vce__bjexj, jnlqk__koya in self.df_out_vars.items():
            slh__hwxay += "'{}':{}, ".format(vce__bjexj, jnlqk__koya.name)
        sgoqy__nim = '{}{{{}}}'.format(self.df_out, slh__hwxay)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            jnlqk__koya.name for jnlqk__koya in self.key_arrs), fse__obga,
            ', '.join(jnlqk__koya.name for jnlqk__koya in self.out_key_arrs
            ), sgoqy__nim)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    nex__wdh = []
    uoqzl__vci = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for xrzk__vcuq in uoqzl__vci:
        ephl__fnfo = equiv_set.get_shape(xrzk__vcuq)
        if ephl__fnfo is not None:
            nex__wdh.append(ephl__fnfo[0])
    if len(nex__wdh) > 1:
        equiv_set.insert_equiv(*nex__wdh)
    olorc__jbsdn = []
    nex__wdh = []
    aqy__rgnyx = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for xrzk__vcuq in aqy__rgnyx:
        eovj__bjtkh = typemap[xrzk__vcuq.name]
        anzr__nhpj = array_analysis._gen_shape_call(equiv_set, xrzk__vcuq,
            eovj__bjtkh.ndim, None, olorc__jbsdn)
        equiv_set.insert_equiv(xrzk__vcuq, anzr__nhpj)
        nex__wdh.append(anzr__nhpj[0])
        equiv_set.define(xrzk__vcuq, set())
    if len(nex__wdh) > 1:
        equiv_set.insert_equiv(*nex__wdh)
    return [], olorc__jbsdn


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    uoqzl__vci = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    gjgj__cyhr = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    jsp__pibo = Distribution.OneD
    for xrzk__vcuq in uoqzl__vci:
        jsp__pibo = Distribution(min(jsp__pibo.value, array_dists[
            xrzk__vcuq.name].value))
    ykfy__vhzb = Distribution(min(jsp__pibo.value, Distribution.OneD_Var.value)
        )
    for xrzk__vcuq in gjgj__cyhr:
        if xrzk__vcuq.name in array_dists:
            ykfy__vhzb = Distribution(min(ykfy__vhzb.value, array_dists[
                xrzk__vcuq.name].value))
    if ykfy__vhzb != Distribution.OneD_Var:
        jsp__pibo = ykfy__vhzb
    for xrzk__vcuq in uoqzl__vci:
        array_dists[xrzk__vcuq.name] = jsp__pibo
    for xrzk__vcuq in gjgj__cyhr:
        array_dists[xrzk__vcuq.name] = ykfy__vhzb
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for hvpzz__rvao, powqc__cwg in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=powqc__cwg.
            name, src=hvpzz__rvao.name, loc=sort_node.loc))
    for oexv__sino, xrzk__vcuq in sort_node.df_in_vars.items():
        qgu__luzjp = sort_node.df_out_vars[oexv__sino]
        typeinferer.constraints.append(typeinfer.Propagate(dst=qgu__luzjp.
            name, src=xrzk__vcuq.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for xrzk__vcuq in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[xrzk__vcuq.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for xge__vkfy in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[xge__vkfy] = visit_vars_inner(sort_node.key_arrs
            [xge__vkfy], callback, cbdata)
        sort_node.out_key_arrs[xge__vkfy] = visit_vars_inner(sort_node.
            out_key_arrs[xge__vkfy], callback, cbdata)
    for oexv__sino in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[oexv__sino] = visit_vars_inner(sort_node.
            df_in_vars[oexv__sino], callback, cbdata)
    for oexv__sino in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[oexv__sino] = visit_vars_inner(sort_node.
            df_out_vars[oexv__sino], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    cemds__zuu = []
    for oexv__sino, xrzk__vcuq in sort_node.df_out_vars.items():
        if xrzk__vcuq.name not in lives:
            cemds__zuu.append(oexv__sino)
    for kkfos__uwixx in cemds__zuu:
        sort_node.df_in_vars.pop(kkfos__uwixx)
        sort_node.df_out_vars.pop(kkfos__uwixx)
    if len(sort_node.df_out_vars) == 0 and all(jnlqk__koya.name not in
        lives for jnlqk__koya in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({jnlqk__koya.name for jnlqk__koya in sort_node.key_arrs})
    use_set.update({jnlqk__koya.name for jnlqk__koya in sort_node.
        df_in_vars.values()})
    if not sort_node.inplace:
        def_set.update({jnlqk__koya.name for jnlqk__koya in sort_node.
            out_key_arrs})
        def_set.update({jnlqk__koya.name for jnlqk__koya in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    jec__qjl = set()
    if not sort_node.inplace:
        jec__qjl = set(jnlqk__koya.name for jnlqk__koya in sort_node.
            df_out_vars.values())
        jec__qjl.update({jnlqk__koya.name for jnlqk__koya in sort_node.
            out_key_arrs})
    return set(), jec__qjl


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for xge__vkfy in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[xge__vkfy] = replace_vars_inner(sort_node.
            key_arrs[xge__vkfy], var_dict)
        sort_node.out_key_arrs[xge__vkfy] = replace_vars_inner(sort_node.
            out_key_arrs[xge__vkfy], var_dict)
    for oexv__sino in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[oexv__sino] = replace_vars_inner(sort_node.
            df_in_vars[oexv__sino], var_dict)
    for oexv__sino in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[oexv__sino] = replace_vars_inner(sort_node.
            df_out_vars[oexv__sino], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    vqwd__vevq = False
    norat__uwhb = list(sort_node.df_in_vars.values())
    aqy__rgnyx = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        vqwd__vevq = True
        for jnlqk__koya in (sort_node.key_arrs + sort_node.out_key_arrs +
            norat__uwhb + aqy__rgnyx):
            if array_dists[jnlqk__koya.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                jnlqk__koya.name] != distributed_pass.Distribution.OneD_Var:
                vqwd__vevq = False
    loc = sort_node.loc
    ynx__ougld = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        yqvw__qkfl = []
        for jnlqk__koya in key_arrs:
            vqv__rgnkx = _copy_array_nodes(jnlqk__koya, nodes, typingctx,
                targetctx, typemap, calltypes)
            yqvw__qkfl.append(vqv__rgnkx)
        key_arrs = yqvw__qkfl
        aacuj__bgxfm = []
        for jnlqk__koya in norat__uwhb:
            teaer__cbv = _copy_array_nodes(jnlqk__koya, nodes, typingctx,
                targetctx, typemap, calltypes)
            aacuj__bgxfm.append(teaer__cbv)
        norat__uwhb = aacuj__bgxfm
    key_name_args = [f'key{xge__vkfy}' for xge__vkfy in range(len(key_arrs))]
    lnk__hgw = ', '.join(key_name_args)
    col_name_args = [f'c{xge__vkfy}' for xge__vkfy in range(len(norat__uwhb))]
    ukjc__ixt = ', '.join(col_name_args)
    ahm__ghjd = 'def f({}, {}):\n'.format(lnk__hgw, ukjc__ixt)
    ahm__ghjd += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, vqwd__vevq)
    ahm__ghjd += '  return key_arrs, data\n'
    mogf__ayxkh = {}
    exec(ahm__ghjd, {}, mogf__ayxkh)
    wlwy__faho = mogf__ayxkh['f']
    cvtc__nub = types.Tuple([typemap[jnlqk__koya.name] for jnlqk__koya in
        key_arrs])
    ouv__lnp = types.Tuple([typemap[jnlqk__koya.name] for jnlqk__koya in
        norat__uwhb])
    fbtyn__dcz = compile_to_numba_ir(wlwy__faho, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(cvtc__nub.types) + list(ouv__lnp.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(fbtyn__dcz, key_arrs + norat__uwhb)
    nodes += fbtyn__dcz.body[:-2]
    gfmmf__pqu = nodes[-1].target
    fybwu__onmu = ir.Var(ynx__ougld, mk_unique_var('key_data'), loc)
    typemap[fybwu__onmu.name] = cvtc__nub
    gen_getitem(fybwu__onmu, gfmmf__pqu, 0, calltypes, nodes)
    juca__ajlh = ir.Var(ynx__ougld, mk_unique_var('sort_data'), loc)
    typemap[juca__ajlh.name] = ouv__lnp
    gen_getitem(juca__ajlh, gfmmf__pqu, 1, calltypes, nodes)
    for xge__vkfy, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, fybwu__onmu, xge__vkfy, calltypes, nodes)
    for xge__vkfy, var in enumerate(aqy__rgnyx):
        gen_getitem(var, juca__ajlh, xge__vkfy, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    fbtyn__dcz = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(fbtyn__dcz, [var])
    nodes += fbtyn__dcz.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    ahm__ghjd = ''
    gdnl__jgg = len(key_name_args)
    qyxjk__pcfl = ['array_to_info({})'.format(lqj__btrsr) for lqj__btrsr in
        key_name_args] + ['array_to_info({})'.format(lqj__btrsr) for
        lqj__btrsr in col_name_args]
    ahm__ghjd += '  info_list_total = [{}]\n'.format(','.join(qyxjk__pcfl))
    ahm__ghjd += '  table_total = arr_info_list_to_table(info_list_total)\n'
    ahm__ghjd += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        cqc__gux else '0' for cqc__gux in ascending_list))
    ahm__ghjd += '  na_position = np.array([{}])\n'.format(','.join('1' if
        cqc__gux else '0' for cqc__gux in na_position_b))
    ahm__ghjd += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(gdnl__jgg, parallel_b))
    ydq__jflt = 0
    qqjr__cfceb = []
    for lqj__btrsr in key_name_args:
        qqjr__cfceb.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(ydq__jflt, lqj__btrsr))
        ydq__jflt += 1
    ahm__ghjd += '  key_arrs = ({},)\n'.format(','.join(qqjr__cfceb))
    umphu__kklzw = []
    for lqj__btrsr in col_name_args:
        umphu__kklzw.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(ydq__jflt, lqj__btrsr))
        ydq__jflt += 1
    if len(umphu__kklzw) > 0:
        ahm__ghjd += '  data = ({},)\n'.format(','.join(umphu__kklzw))
    else:
        ahm__ghjd += '  data = ()\n'
    ahm__ghjd += '  delete_table(out_table)\n'
    ahm__ghjd += '  delete_table(table_total)\n'
    return ahm__ghjd
