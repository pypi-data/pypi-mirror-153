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
            self.na_position_b = tuple([(True if iirri__cqjrk == 'last' else
                False) for iirri__cqjrk in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        exfkx__tkvkj = ''
        for pfu__ziwe, yjkt__osrzf in self.df_in_vars.items():
            exfkx__tkvkj += "'{}':{}, ".format(pfu__ziwe, yjkt__osrzf.name)
        dfk__bal = '{}{{{}}}'.format(self.df_in, exfkx__tkvkj)
        gfg__emm = ''
        for pfu__ziwe, yjkt__osrzf in self.df_out_vars.items():
            gfg__emm += "'{}':{}, ".format(pfu__ziwe, yjkt__osrzf.name)
        iut__izhml = '{}{{{}}}'.format(self.df_out, gfg__emm)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            yjkt__osrzf.name for yjkt__osrzf in self.key_arrs), dfk__bal,
            ', '.join(yjkt__osrzf.name for yjkt__osrzf in self.out_key_arrs
            ), iut__izhml)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    wto__yxl = []
    sdvhg__ivu = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for unzmb__uqg in sdvhg__ivu:
        kyuj__gmot = equiv_set.get_shape(unzmb__uqg)
        if kyuj__gmot is not None:
            wto__yxl.append(kyuj__gmot[0])
    if len(wto__yxl) > 1:
        equiv_set.insert_equiv(*wto__yxl)
    aqmxf__geb = []
    wto__yxl = []
    lfze__qgkht = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for unzmb__uqg in lfze__qgkht:
        egnb__dhw = typemap[unzmb__uqg.name]
        fslf__yvsa = array_analysis._gen_shape_call(equiv_set, unzmb__uqg,
            egnb__dhw.ndim, None, aqmxf__geb)
        equiv_set.insert_equiv(unzmb__uqg, fslf__yvsa)
        wto__yxl.append(fslf__yvsa[0])
        equiv_set.define(unzmb__uqg, set())
    if len(wto__yxl) > 1:
        equiv_set.insert_equiv(*wto__yxl)
    return [], aqmxf__geb


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    sdvhg__ivu = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    tvwyb__hvrlv = sort_node.out_key_arrs + list(sort_node.df_out_vars.values()
        )
    dmglt__elybl = Distribution.OneD
    for unzmb__uqg in sdvhg__ivu:
        dmglt__elybl = Distribution(min(dmglt__elybl.value, array_dists[
            unzmb__uqg.name].value))
    yktyc__xfbx = Distribution(min(dmglt__elybl.value, Distribution.
        OneD_Var.value))
    for unzmb__uqg in tvwyb__hvrlv:
        if unzmb__uqg.name in array_dists:
            yktyc__xfbx = Distribution(min(yktyc__xfbx.value, array_dists[
                unzmb__uqg.name].value))
    if yktyc__xfbx != Distribution.OneD_Var:
        dmglt__elybl = yktyc__xfbx
    for unzmb__uqg in sdvhg__ivu:
        array_dists[unzmb__uqg.name] = dmglt__elybl
    for unzmb__uqg in tvwyb__hvrlv:
        array_dists[unzmb__uqg.name] = yktyc__xfbx
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for tul__xkv, ftsg__rxm in zip(sort_node.key_arrs, sort_node.out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=ftsg__rxm.
            name, src=tul__xkv.name, loc=sort_node.loc))
    for fir__uyxzh, unzmb__uqg in sort_node.df_in_vars.items():
        ajpnp__afn = sort_node.df_out_vars[fir__uyxzh]
        typeinferer.constraints.append(typeinfer.Propagate(dst=ajpnp__afn.
            name, src=unzmb__uqg.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for unzmb__uqg in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[unzmb__uqg.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for iumex__yqqs in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[iumex__yqqs] = visit_vars_inner(sort_node.
            key_arrs[iumex__yqqs], callback, cbdata)
        sort_node.out_key_arrs[iumex__yqqs] = visit_vars_inner(sort_node.
            out_key_arrs[iumex__yqqs], callback, cbdata)
    for fir__uyxzh in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[fir__uyxzh] = visit_vars_inner(sort_node.
            df_in_vars[fir__uyxzh], callback, cbdata)
    for fir__uyxzh in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[fir__uyxzh] = visit_vars_inner(sort_node.
            df_out_vars[fir__uyxzh], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    kbxtk__yjcrk = []
    for fir__uyxzh, unzmb__uqg in sort_node.df_out_vars.items():
        if unzmb__uqg.name not in lives:
            kbxtk__yjcrk.append(fir__uyxzh)
    for ooeo__ykkoh in kbxtk__yjcrk:
        sort_node.df_in_vars.pop(ooeo__ykkoh)
        sort_node.df_out_vars.pop(ooeo__ykkoh)
    if len(sort_node.df_out_vars) == 0 and all(yjkt__osrzf.name not in
        lives for yjkt__osrzf in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({yjkt__osrzf.name for yjkt__osrzf in sort_node.key_arrs})
    use_set.update({yjkt__osrzf.name for yjkt__osrzf in sort_node.
        df_in_vars.values()})
    if not sort_node.inplace:
        def_set.update({yjkt__osrzf.name for yjkt__osrzf in sort_node.
            out_key_arrs})
        def_set.update({yjkt__osrzf.name for yjkt__osrzf in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    bwvvj__okjm = set()
    if not sort_node.inplace:
        bwvvj__okjm = set(yjkt__osrzf.name for yjkt__osrzf in sort_node.
            df_out_vars.values())
        bwvvj__okjm.update({yjkt__osrzf.name for yjkt__osrzf in sort_node.
            out_key_arrs})
    return set(), bwvvj__okjm


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for iumex__yqqs in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[iumex__yqqs] = replace_vars_inner(sort_node.
            key_arrs[iumex__yqqs], var_dict)
        sort_node.out_key_arrs[iumex__yqqs] = replace_vars_inner(sort_node.
            out_key_arrs[iumex__yqqs], var_dict)
    for fir__uyxzh in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[fir__uyxzh] = replace_vars_inner(sort_node.
            df_in_vars[fir__uyxzh], var_dict)
    for fir__uyxzh in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[fir__uyxzh] = replace_vars_inner(sort_node.
            df_out_vars[fir__uyxzh], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    jszj__umh = False
    txoe__fgfx = list(sort_node.df_in_vars.values())
    lfze__qgkht = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        jszj__umh = True
        for yjkt__osrzf in (sort_node.key_arrs + sort_node.out_key_arrs +
            txoe__fgfx + lfze__qgkht):
            if array_dists[yjkt__osrzf.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                yjkt__osrzf.name] != distributed_pass.Distribution.OneD_Var:
                jszj__umh = False
    loc = sort_node.loc
    gyj__vrtvf = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        enyjj__yhysa = []
        for yjkt__osrzf in key_arrs:
            frn__xpyof = _copy_array_nodes(yjkt__osrzf, nodes, typingctx,
                targetctx, typemap, calltypes)
            enyjj__yhysa.append(frn__xpyof)
        key_arrs = enyjj__yhysa
        hik__eeikk = []
        for yjkt__osrzf in txoe__fgfx:
            lnt__kxxen = _copy_array_nodes(yjkt__osrzf, nodes, typingctx,
                targetctx, typemap, calltypes)
            hik__eeikk.append(lnt__kxxen)
        txoe__fgfx = hik__eeikk
    key_name_args = [f'key{iumex__yqqs}' for iumex__yqqs in range(len(
        key_arrs))]
    nnwt__befh = ', '.join(key_name_args)
    col_name_args = [f'c{iumex__yqqs}' for iumex__yqqs in range(len(
        txoe__fgfx))]
    pfmcj__fgd = ', '.join(col_name_args)
    wio__fpgdk = 'def f({}, {}):\n'.format(nnwt__befh, pfmcj__fgd)
    wio__fpgdk += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, jszj__umh)
    wio__fpgdk += '  return key_arrs, data\n'
    zgu__gtj = {}
    exec(wio__fpgdk, {}, zgu__gtj)
    pvizk__bigrw = zgu__gtj['f']
    bsul__bkoct = types.Tuple([typemap[yjkt__osrzf.name] for yjkt__osrzf in
        key_arrs])
    ucn__henej = types.Tuple([typemap[yjkt__osrzf.name] for yjkt__osrzf in
        txoe__fgfx])
    ncvsg__bmoxm = compile_to_numba_ir(pvizk__bigrw, {'bodo': bodo, 'np':
        np, 'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(bsul__bkoct.types) + list(ucn__henej
        .types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ncvsg__bmoxm, key_arrs + txoe__fgfx)
    nodes += ncvsg__bmoxm.body[:-2]
    vsnxr__xczw = nodes[-1].target
    bvh__bre = ir.Var(gyj__vrtvf, mk_unique_var('key_data'), loc)
    typemap[bvh__bre.name] = bsul__bkoct
    gen_getitem(bvh__bre, vsnxr__xczw, 0, calltypes, nodes)
    ibuj__ezv = ir.Var(gyj__vrtvf, mk_unique_var('sort_data'), loc)
    typemap[ibuj__ezv.name] = ucn__henej
    gen_getitem(ibuj__ezv, vsnxr__xczw, 1, calltypes, nodes)
    for iumex__yqqs, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, bvh__bre, iumex__yqqs, calltypes, nodes)
    for iumex__yqqs, var in enumerate(lfze__qgkht):
        gen_getitem(var, ibuj__ezv, iumex__yqqs, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    ncvsg__bmoxm = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ncvsg__bmoxm, [var])
    nodes += ncvsg__bmoxm.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    wio__fpgdk = ''
    qwar__oxx = len(key_name_args)
    yopdr__tjt = ['array_to_info({})'.format(txzg__rxqjp) for txzg__rxqjp in
        key_name_args] + ['array_to_info({})'.format(txzg__rxqjp) for
        txzg__rxqjp in col_name_args]
    wio__fpgdk += '  info_list_total = [{}]\n'.format(','.join(yopdr__tjt))
    wio__fpgdk += '  table_total = arr_info_list_to_table(info_list_total)\n'
    wio__fpgdk += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        mngll__wumf else '0' for mngll__wumf in ascending_list))
    wio__fpgdk += '  na_position = np.array([{}])\n'.format(','.join('1' if
        mngll__wumf else '0' for mngll__wumf in na_position_b))
    wio__fpgdk += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(qwar__oxx, parallel_b))
    avc__vpp = 0
    tsjk__lywu = []
    for txzg__rxqjp in key_name_args:
        tsjk__lywu.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(avc__vpp, txzg__rxqjp))
        avc__vpp += 1
    wio__fpgdk += '  key_arrs = ({},)\n'.format(','.join(tsjk__lywu))
    bqrol__jef = []
    for txzg__rxqjp in col_name_args:
        bqrol__jef.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(avc__vpp, txzg__rxqjp))
        avc__vpp += 1
    if len(bqrol__jef) > 0:
        wio__fpgdk += '  data = ({},)\n'.format(','.join(bqrol__jef))
    else:
        wio__fpgdk += '  data = ()\n'
    wio__fpgdk += '  delete_table(out_table)\n'
    wio__fpgdk += '  delete_table(table_total)\n'
    return wio__fpgdk
