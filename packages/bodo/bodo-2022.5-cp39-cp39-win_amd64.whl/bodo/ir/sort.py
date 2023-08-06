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
            self.na_position_b = tuple([(True if iwpsb__ggew == 'last' else
                False) for iwpsb__ggew in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        vim__jubka = ''
        for ijzb__zya, cfg__dgsdh in self.df_in_vars.items():
            vim__jubka += "'{}':{}, ".format(ijzb__zya, cfg__dgsdh.name)
        qms__eeef = '{}{{{}}}'.format(self.df_in, vim__jubka)
        ommv__hiyon = ''
        for ijzb__zya, cfg__dgsdh in self.df_out_vars.items():
            ommv__hiyon += "'{}':{}, ".format(ijzb__zya, cfg__dgsdh.name)
        ycyz__glwg = '{}{{{}}}'.format(self.df_out, ommv__hiyon)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            cfg__dgsdh.name for cfg__dgsdh in self.key_arrs), qms__eeef,
            ', '.join(cfg__dgsdh.name for cfg__dgsdh in self.out_key_arrs),
            ycyz__glwg)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    iomz__powg = []
    oeugz__fjnq = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for oen__hplp in oeugz__fjnq:
        dhb__jokb = equiv_set.get_shape(oen__hplp)
        if dhb__jokb is not None:
            iomz__powg.append(dhb__jokb[0])
    if len(iomz__powg) > 1:
        equiv_set.insert_equiv(*iomz__powg)
    duf__okx = []
    iomz__powg = []
    wcsh__smr = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for oen__hplp in wcsh__smr:
        mwidx__qmxon = typemap[oen__hplp.name]
        npdab__sxm = array_analysis._gen_shape_call(equiv_set, oen__hplp,
            mwidx__qmxon.ndim, None, duf__okx)
        equiv_set.insert_equiv(oen__hplp, npdab__sxm)
        iomz__powg.append(npdab__sxm[0])
        equiv_set.define(oen__hplp, set())
    if len(iomz__powg) > 1:
        equiv_set.insert_equiv(*iomz__powg)
    return [], duf__okx


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    oeugz__fjnq = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    jufbh__poqqk = sort_node.out_key_arrs + list(sort_node.df_out_vars.values()
        )
    haimo__rvgu = Distribution.OneD
    for oen__hplp in oeugz__fjnq:
        haimo__rvgu = Distribution(min(haimo__rvgu.value, array_dists[
            oen__hplp.name].value))
    pozz__qoqn = Distribution(min(haimo__rvgu.value, Distribution.OneD_Var.
        value))
    for oen__hplp in jufbh__poqqk:
        if oen__hplp.name in array_dists:
            pozz__qoqn = Distribution(min(pozz__qoqn.value, array_dists[
                oen__hplp.name].value))
    if pozz__qoqn != Distribution.OneD_Var:
        haimo__rvgu = pozz__qoqn
    for oen__hplp in oeugz__fjnq:
        array_dists[oen__hplp.name] = haimo__rvgu
    for oen__hplp in jufbh__poqqk:
        array_dists[oen__hplp.name] = pozz__qoqn
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for npp__silw, uujuf__ggmvl in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=uujuf__ggmvl
            .name, src=npp__silw.name, loc=sort_node.loc))
    for ttv__lkp, oen__hplp in sort_node.df_in_vars.items():
        nisn__wmp = sort_node.df_out_vars[ttv__lkp]
        typeinferer.constraints.append(typeinfer.Propagate(dst=nisn__wmp.
            name, src=oen__hplp.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for oen__hplp in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[oen__hplp.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for dghu__kyoe in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[dghu__kyoe] = visit_vars_inner(sort_node.
            key_arrs[dghu__kyoe], callback, cbdata)
        sort_node.out_key_arrs[dghu__kyoe] = visit_vars_inner(sort_node.
            out_key_arrs[dghu__kyoe], callback, cbdata)
    for ttv__lkp in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[ttv__lkp] = visit_vars_inner(sort_node.
            df_in_vars[ttv__lkp], callback, cbdata)
    for ttv__lkp in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[ttv__lkp] = visit_vars_inner(sort_node.
            df_out_vars[ttv__lkp], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    lej__uxku = []
    for ttv__lkp, oen__hplp in sort_node.df_out_vars.items():
        if oen__hplp.name not in lives:
            lej__uxku.append(ttv__lkp)
    for thme__bruqj in lej__uxku:
        sort_node.df_in_vars.pop(thme__bruqj)
        sort_node.df_out_vars.pop(thme__bruqj)
    if len(sort_node.df_out_vars) == 0 and all(cfg__dgsdh.name not in lives for
        cfg__dgsdh in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({cfg__dgsdh.name for cfg__dgsdh in sort_node.key_arrs})
    use_set.update({cfg__dgsdh.name for cfg__dgsdh in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({cfg__dgsdh.name for cfg__dgsdh in sort_node.
            out_key_arrs})
        def_set.update({cfg__dgsdh.name for cfg__dgsdh in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    buooz__stmii = set()
    if not sort_node.inplace:
        buooz__stmii = set(cfg__dgsdh.name for cfg__dgsdh in sort_node.
            df_out_vars.values())
        buooz__stmii.update({cfg__dgsdh.name for cfg__dgsdh in sort_node.
            out_key_arrs})
    return set(), buooz__stmii


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for dghu__kyoe in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[dghu__kyoe] = replace_vars_inner(sort_node.
            key_arrs[dghu__kyoe], var_dict)
        sort_node.out_key_arrs[dghu__kyoe] = replace_vars_inner(sort_node.
            out_key_arrs[dghu__kyoe], var_dict)
    for ttv__lkp in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[ttv__lkp] = replace_vars_inner(sort_node.
            df_in_vars[ttv__lkp], var_dict)
    for ttv__lkp in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[ttv__lkp] = replace_vars_inner(sort_node.
            df_out_vars[ttv__lkp], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    qqp__tgjph = False
    bmt__wqubc = list(sort_node.df_in_vars.values())
    wcsh__smr = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        qqp__tgjph = True
        for cfg__dgsdh in (sort_node.key_arrs + sort_node.out_key_arrs +
            bmt__wqubc + wcsh__smr):
            if array_dists[cfg__dgsdh.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                cfg__dgsdh.name] != distributed_pass.Distribution.OneD_Var:
                qqp__tgjph = False
    loc = sort_node.loc
    chek__ixdj = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        oqf__wdt = []
        for cfg__dgsdh in key_arrs:
            xsnmz__menvh = _copy_array_nodes(cfg__dgsdh, nodes, typingctx,
                targetctx, typemap, calltypes)
            oqf__wdt.append(xsnmz__menvh)
        key_arrs = oqf__wdt
        aoqa__vqhyi = []
        for cfg__dgsdh in bmt__wqubc:
            enu__oeweg = _copy_array_nodes(cfg__dgsdh, nodes, typingctx,
                targetctx, typemap, calltypes)
            aoqa__vqhyi.append(enu__oeweg)
        bmt__wqubc = aoqa__vqhyi
    key_name_args = [f'key{dghu__kyoe}' for dghu__kyoe in range(len(key_arrs))]
    skvps__hhusa = ', '.join(key_name_args)
    col_name_args = [f'c{dghu__kyoe}' for dghu__kyoe in range(len(bmt__wqubc))]
    szdq__yalgd = ', '.join(col_name_args)
    wqxi__tygh = 'def f({}, {}):\n'.format(skvps__hhusa, szdq__yalgd)
    wqxi__tygh += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, qqp__tgjph)
    wqxi__tygh += '  return key_arrs, data\n'
    talt__jggd = {}
    exec(wqxi__tygh, {}, talt__jggd)
    ugco__ztw = talt__jggd['f']
    gayce__pck = types.Tuple([typemap[cfg__dgsdh.name] for cfg__dgsdh in
        key_arrs])
    kqy__tgl = types.Tuple([typemap[cfg__dgsdh.name] for cfg__dgsdh in
        bmt__wqubc])
    nev__yzmo = compile_to_numba_ir(ugco__ztw, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(gayce__pck.types) + list(kqy__tgl.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(nev__yzmo, key_arrs + bmt__wqubc)
    nodes += nev__yzmo.body[:-2]
    akq__sfjgk = nodes[-1].target
    wstx__xrpu = ir.Var(chek__ixdj, mk_unique_var('key_data'), loc)
    typemap[wstx__xrpu.name] = gayce__pck
    gen_getitem(wstx__xrpu, akq__sfjgk, 0, calltypes, nodes)
    jmoa__npiu = ir.Var(chek__ixdj, mk_unique_var('sort_data'), loc)
    typemap[jmoa__npiu.name] = kqy__tgl
    gen_getitem(jmoa__npiu, akq__sfjgk, 1, calltypes, nodes)
    for dghu__kyoe, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, wstx__xrpu, dghu__kyoe, calltypes, nodes)
    for dghu__kyoe, var in enumerate(wcsh__smr):
        gen_getitem(var, jmoa__npiu, dghu__kyoe, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    nev__yzmo = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(nev__yzmo, [var])
    nodes += nev__yzmo.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    wqxi__tygh = ''
    nxqn__rbir = len(key_name_args)
    fcdm__bttus = ['array_to_info({})'.format(blhue__hdr) for blhue__hdr in
        key_name_args] + ['array_to_info({})'.format(blhue__hdr) for
        blhue__hdr in col_name_args]
    wqxi__tygh += '  info_list_total = [{}]\n'.format(','.join(fcdm__bttus))
    wqxi__tygh += '  table_total = arr_info_list_to_table(info_list_total)\n'
    wqxi__tygh += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        apr__omjb else '0' for apr__omjb in ascending_list))
    wqxi__tygh += '  na_position = np.array([{}])\n'.format(','.join('1' if
        apr__omjb else '0' for apr__omjb in na_position_b))
    wqxi__tygh += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(nxqn__rbir, parallel_b))
    hwpft__ewhi = 0
    lggvv__genlc = []
    for blhue__hdr in key_name_args:
        lggvv__genlc.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(hwpft__ewhi, blhue__hdr))
        hwpft__ewhi += 1
    wqxi__tygh += '  key_arrs = ({},)\n'.format(','.join(lggvv__genlc))
    losm__zocc = []
    for blhue__hdr in col_name_args:
        losm__zocc.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(hwpft__ewhi, blhue__hdr))
        hwpft__ewhi += 1
    if len(losm__zocc) > 0:
        wqxi__tygh += '  data = ({},)\n'.format(','.join(losm__zocc))
    else:
        wqxi__tygh += '  data = ()\n'
    wqxi__tygh += '  delete_table(out_table)\n'
    wqxi__tygh += '  delete_table(table_total)\n'
    return wqxi__tygh
