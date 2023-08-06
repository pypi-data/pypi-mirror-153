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
            self.na_position_b = tuple([(True if clc__vdfz == 'last' else 
                False) for clc__vdfz in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        ack__akwdw = ''
        for qalu__zujkl, dctl__bfyp in self.df_in_vars.items():
            ack__akwdw += "'{}':{}, ".format(qalu__zujkl, dctl__bfyp.name)
        ptnor__bce = '{}{{{}}}'.format(self.df_in, ack__akwdw)
        mbodm__hsvll = ''
        for qalu__zujkl, dctl__bfyp in self.df_out_vars.items():
            mbodm__hsvll += "'{}':{}, ".format(qalu__zujkl, dctl__bfyp.name)
        xce__zchh = '{}{{{}}}'.format(self.df_out, mbodm__hsvll)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            dctl__bfyp.name for dctl__bfyp in self.key_arrs), ptnor__bce,
            ', '.join(dctl__bfyp.name for dctl__bfyp in self.out_key_arrs),
            xce__zchh)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    wkorg__qtz = []
    dvt__ylt = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for kswh__bwwye in dvt__ylt:
        aal__brrgn = equiv_set.get_shape(kswh__bwwye)
        if aal__brrgn is not None:
            wkorg__qtz.append(aal__brrgn[0])
    if len(wkorg__qtz) > 1:
        equiv_set.insert_equiv(*wkorg__qtz)
    gqh__hcabe = []
    wkorg__qtz = []
    woww__ucjr = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for kswh__bwwye in woww__ucjr:
        fwcxg__yhwaw = typemap[kswh__bwwye.name]
        ddxz__opcfu = array_analysis._gen_shape_call(equiv_set, kswh__bwwye,
            fwcxg__yhwaw.ndim, None, gqh__hcabe)
        equiv_set.insert_equiv(kswh__bwwye, ddxz__opcfu)
        wkorg__qtz.append(ddxz__opcfu[0])
        equiv_set.define(kswh__bwwye, set())
    if len(wkorg__qtz) > 1:
        equiv_set.insert_equiv(*wkorg__qtz)
    return [], gqh__hcabe


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    dvt__ylt = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    awu__qffd = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    jsiqd__rjk = Distribution.OneD
    for kswh__bwwye in dvt__ylt:
        jsiqd__rjk = Distribution(min(jsiqd__rjk.value, array_dists[
            kswh__bwwye.name].value))
    awyj__siado = Distribution(min(jsiqd__rjk.value, Distribution.OneD_Var.
        value))
    for kswh__bwwye in awu__qffd:
        if kswh__bwwye.name in array_dists:
            awyj__siado = Distribution(min(awyj__siado.value, array_dists[
                kswh__bwwye.name].value))
    if awyj__siado != Distribution.OneD_Var:
        jsiqd__rjk = awyj__siado
    for kswh__bwwye in dvt__ylt:
        array_dists[kswh__bwwye.name] = jsiqd__rjk
    for kswh__bwwye in awu__qffd:
        array_dists[kswh__bwwye.name] = awyj__siado
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for hjyth__bnnki, hykee__iqry in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=hykee__iqry.
            name, src=hjyth__bnnki.name, loc=sort_node.loc))
    for rfoh__sbotk, kswh__bwwye in sort_node.df_in_vars.items():
        dxerg__pnzec = sort_node.df_out_vars[rfoh__sbotk]
        typeinferer.constraints.append(typeinfer.Propagate(dst=dxerg__pnzec
            .name, src=kswh__bwwye.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for kswh__bwwye in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[kswh__bwwye.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for ajuow__bgm in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[ajuow__bgm] = visit_vars_inner(sort_node.
            key_arrs[ajuow__bgm], callback, cbdata)
        sort_node.out_key_arrs[ajuow__bgm] = visit_vars_inner(sort_node.
            out_key_arrs[ajuow__bgm], callback, cbdata)
    for rfoh__sbotk in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[rfoh__sbotk] = visit_vars_inner(sort_node.
            df_in_vars[rfoh__sbotk], callback, cbdata)
    for rfoh__sbotk in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[rfoh__sbotk] = visit_vars_inner(sort_node.
            df_out_vars[rfoh__sbotk], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    tgglb__spd = []
    for rfoh__sbotk, kswh__bwwye in sort_node.df_out_vars.items():
        if kswh__bwwye.name not in lives:
            tgglb__spd.append(rfoh__sbotk)
    for xhi__mbhd in tgglb__spd:
        sort_node.df_in_vars.pop(xhi__mbhd)
        sort_node.df_out_vars.pop(xhi__mbhd)
    if len(sort_node.df_out_vars) == 0 and all(dctl__bfyp.name not in lives for
        dctl__bfyp in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({dctl__bfyp.name for dctl__bfyp in sort_node.key_arrs})
    use_set.update({dctl__bfyp.name for dctl__bfyp in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({dctl__bfyp.name for dctl__bfyp in sort_node.
            out_key_arrs})
        def_set.update({dctl__bfyp.name for dctl__bfyp in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    cjor__biwdk = set()
    if not sort_node.inplace:
        cjor__biwdk = set(dctl__bfyp.name for dctl__bfyp in sort_node.
            df_out_vars.values())
        cjor__biwdk.update({dctl__bfyp.name for dctl__bfyp in sort_node.
            out_key_arrs})
    return set(), cjor__biwdk


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for ajuow__bgm in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[ajuow__bgm] = replace_vars_inner(sort_node.
            key_arrs[ajuow__bgm], var_dict)
        sort_node.out_key_arrs[ajuow__bgm] = replace_vars_inner(sort_node.
            out_key_arrs[ajuow__bgm], var_dict)
    for rfoh__sbotk in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[rfoh__sbotk] = replace_vars_inner(sort_node.
            df_in_vars[rfoh__sbotk], var_dict)
    for rfoh__sbotk in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[rfoh__sbotk] = replace_vars_inner(sort_node.
            df_out_vars[rfoh__sbotk], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    xyki__hnxmo = False
    cil__chnc = list(sort_node.df_in_vars.values())
    woww__ucjr = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        xyki__hnxmo = True
        for dctl__bfyp in (sort_node.key_arrs + sort_node.out_key_arrs +
            cil__chnc + woww__ucjr):
            if array_dists[dctl__bfyp.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                dctl__bfyp.name] != distributed_pass.Distribution.OneD_Var:
                xyki__hnxmo = False
    loc = sort_node.loc
    iuey__ksz = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        pifw__jwr = []
        for dctl__bfyp in key_arrs:
            ccvfn__tmmk = _copy_array_nodes(dctl__bfyp, nodes, typingctx,
                targetctx, typemap, calltypes)
            pifw__jwr.append(ccvfn__tmmk)
        key_arrs = pifw__jwr
        lmy__phr = []
        for dctl__bfyp in cil__chnc:
            kfri__djo = _copy_array_nodes(dctl__bfyp, nodes, typingctx,
                targetctx, typemap, calltypes)
            lmy__phr.append(kfri__djo)
        cil__chnc = lmy__phr
    key_name_args = [f'key{ajuow__bgm}' for ajuow__bgm in range(len(key_arrs))]
    thza__ewjad = ', '.join(key_name_args)
    col_name_args = [f'c{ajuow__bgm}' for ajuow__bgm in range(len(cil__chnc))]
    cfrnm__evfpi = ', '.join(col_name_args)
    kwybg__zpg = 'def f({}, {}):\n'.format(thza__ewjad, cfrnm__evfpi)
    kwybg__zpg += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, xyki__hnxmo)
    kwybg__zpg += '  return key_arrs, data\n'
    sqi__qger = {}
    exec(kwybg__zpg, {}, sqi__qger)
    idb__mqccg = sqi__qger['f']
    hus__erp = types.Tuple([typemap[dctl__bfyp.name] for dctl__bfyp in
        key_arrs])
    ijn__hkzq = types.Tuple([typemap[dctl__bfyp.name] for dctl__bfyp in
        cil__chnc])
    vcye__jgevr = compile_to_numba_ir(idb__mqccg, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(hus__erp.types) + list(ijn__hkzq.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(vcye__jgevr, key_arrs + cil__chnc)
    nodes += vcye__jgevr.body[:-2]
    eslam__zdg = nodes[-1].target
    ibjsa__dyu = ir.Var(iuey__ksz, mk_unique_var('key_data'), loc)
    typemap[ibjsa__dyu.name] = hus__erp
    gen_getitem(ibjsa__dyu, eslam__zdg, 0, calltypes, nodes)
    goy__ibjc = ir.Var(iuey__ksz, mk_unique_var('sort_data'), loc)
    typemap[goy__ibjc.name] = ijn__hkzq
    gen_getitem(goy__ibjc, eslam__zdg, 1, calltypes, nodes)
    for ajuow__bgm, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, ibjsa__dyu, ajuow__bgm, calltypes, nodes)
    for ajuow__bgm, var in enumerate(woww__ucjr):
        gen_getitem(var, goy__ibjc, ajuow__bgm, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    vcye__jgevr = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(vcye__jgevr, [var])
    nodes += vcye__jgevr.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    kwybg__zpg = ''
    gzoi__gcgt = len(key_name_args)
    vrtuw__btna = ['array_to_info({})'.format(spi__bfj) for spi__bfj in
        key_name_args] + ['array_to_info({})'.format(spi__bfj) for spi__bfj in
        col_name_args]
    kwybg__zpg += '  info_list_total = [{}]\n'.format(','.join(vrtuw__btna))
    kwybg__zpg += '  table_total = arr_info_list_to_table(info_list_total)\n'
    kwybg__zpg += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        gedj__qgee else '0' for gedj__qgee in ascending_list))
    kwybg__zpg += '  na_position = np.array([{}])\n'.format(','.join('1' if
        gedj__qgee else '0' for gedj__qgee in na_position_b))
    kwybg__zpg += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(gzoi__gcgt, parallel_b))
    tmkfv__irj = 0
    spgt__nasu = []
    for spi__bfj in key_name_args:
        spgt__nasu.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(tmkfv__irj, spi__bfj))
        tmkfv__irj += 1
    kwybg__zpg += '  key_arrs = ({},)\n'.format(','.join(spgt__nasu))
    jnn__gkb = []
    for spi__bfj in col_name_args:
        jnn__gkb.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(tmkfv__irj, spi__bfj))
        tmkfv__irj += 1
    if len(jnn__gkb) > 0:
        kwybg__zpg += '  data = ({},)\n'.format(','.join(jnn__gkb))
    else:
        kwybg__zpg += '  data = ()\n'
    kwybg__zpg += '  delete_table(out_table)\n'
    kwybg__zpg += '  delete_table(table_total)\n'
    return kwybg__zpg
