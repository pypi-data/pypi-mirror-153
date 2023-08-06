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
            self.na_position_b = tuple([(True if wxbw__ipq == 'last' else 
                False) for wxbw__ipq in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        duw__noh = ''
        for quxb__uxh, dgu__lwus in self.df_in_vars.items():
            duw__noh += "'{}':{}, ".format(quxb__uxh, dgu__lwus.name)
        cot__oweak = '{}{{{}}}'.format(self.df_in, duw__noh)
        tusvt__uvfe = ''
        for quxb__uxh, dgu__lwus in self.df_out_vars.items():
            tusvt__uvfe += "'{}':{}, ".format(quxb__uxh, dgu__lwus.name)
        tch__lrtwc = '{}{{{}}}'.format(self.df_out, tusvt__uvfe)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(dgu__lwus
            .name for dgu__lwus in self.key_arrs), cot__oweak, ', '.join(
            dgu__lwus.name for dgu__lwus in self.out_key_arrs), tch__lrtwc)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    tfa__tttz = []
    evc__jvew = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for uprle__teba in evc__jvew:
        jjlb__xkwl = equiv_set.get_shape(uprle__teba)
        if jjlb__xkwl is not None:
            tfa__tttz.append(jjlb__xkwl[0])
    if len(tfa__tttz) > 1:
        equiv_set.insert_equiv(*tfa__tttz)
    bsm__rhyl = []
    tfa__tttz = []
    fmv__flybj = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for uprle__teba in fmv__flybj:
        vkth__nnzsv = typemap[uprle__teba.name]
        tpyu__lwutv = array_analysis._gen_shape_call(equiv_set, uprle__teba,
            vkth__nnzsv.ndim, None, bsm__rhyl)
        equiv_set.insert_equiv(uprle__teba, tpyu__lwutv)
        tfa__tttz.append(tpyu__lwutv[0])
        equiv_set.define(uprle__teba, set())
    if len(tfa__tttz) > 1:
        equiv_set.insert_equiv(*tfa__tttz)
    return [], bsm__rhyl


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    evc__jvew = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    etnf__mhpwv = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    adx__gmlq = Distribution.OneD
    for uprle__teba in evc__jvew:
        adx__gmlq = Distribution(min(adx__gmlq.value, array_dists[
            uprle__teba.name].value))
    gnbwz__ajoai = Distribution(min(adx__gmlq.value, Distribution.OneD_Var.
        value))
    for uprle__teba in etnf__mhpwv:
        if uprle__teba.name in array_dists:
            gnbwz__ajoai = Distribution(min(gnbwz__ajoai.value, array_dists
                [uprle__teba.name].value))
    if gnbwz__ajoai != Distribution.OneD_Var:
        adx__gmlq = gnbwz__ajoai
    for uprle__teba in evc__jvew:
        array_dists[uprle__teba.name] = adx__gmlq
    for uprle__teba in etnf__mhpwv:
        array_dists[uprle__teba.name] = gnbwz__ajoai
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for rfxg__lwlg, cnp__arwxl in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=cnp__arwxl.
            name, src=rfxg__lwlg.name, loc=sort_node.loc))
    for hlaoo__ebx, uprle__teba in sort_node.df_in_vars.items():
        hnc__emlcz = sort_node.df_out_vars[hlaoo__ebx]
        typeinferer.constraints.append(typeinfer.Propagate(dst=hnc__emlcz.
            name, src=uprle__teba.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for uprle__teba in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[uprle__teba.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for wpdaj__rmih in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[wpdaj__rmih] = visit_vars_inner(sort_node.
            key_arrs[wpdaj__rmih], callback, cbdata)
        sort_node.out_key_arrs[wpdaj__rmih] = visit_vars_inner(sort_node.
            out_key_arrs[wpdaj__rmih], callback, cbdata)
    for hlaoo__ebx in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[hlaoo__ebx] = visit_vars_inner(sort_node.
            df_in_vars[hlaoo__ebx], callback, cbdata)
    for hlaoo__ebx in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[hlaoo__ebx] = visit_vars_inner(sort_node.
            df_out_vars[hlaoo__ebx], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    cjs__cudar = []
    for hlaoo__ebx, uprle__teba in sort_node.df_out_vars.items():
        if uprle__teba.name not in lives:
            cjs__cudar.append(hlaoo__ebx)
    for uie__zjfs in cjs__cudar:
        sort_node.df_in_vars.pop(uie__zjfs)
        sort_node.df_out_vars.pop(uie__zjfs)
    if len(sort_node.df_out_vars) == 0 and all(dgu__lwus.name not in lives for
        dgu__lwus in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({dgu__lwus.name for dgu__lwus in sort_node.key_arrs})
    use_set.update({dgu__lwus.name for dgu__lwus in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({dgu__lwus.name for dgu__lwus in sort_node.out_key_arrs}
            )
        def_set.update({dgu__lwus.name for dgu__lwus in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    dgt__xgm = set()
    if not sort_node.inplace:
        dgt__xgm = set(dgu__lwus.name for dgu__lwus in sort_node.
            df_out_vars.values())
        dgt__xgm.update({dgu__lwus.name for dgu__lwus in sort_node.
            out_key_arrs})
    return set(), dgt__xgm


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for wpdaj__rmih in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[wpdaj__rmih] = replace_vars_inner(sort_node.
            key_arrs[wpdaj__rmih], var_dict)
        sort_node.out_key_arrs[wpdaj__rmih] = replace_vars_inner(sort_node.
            out_key_arrs[wpdaj__rmih], var_dict)
    for hlaoo__ebx in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[hlaoo__ebx] = replace_vars_inner(sort_node.
            df_in_vars[hlaoo__ebx], var_dict)
    for hlaoo__ebx in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[hlaoo__ebx] = replace_vars_inner(sort_node.
            df_out_vars[hlaoo__ebx], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    wzmpa__omc = False
    mzsu__fantr = list(sort_node.df_in_vars.values())
    fmv__flybj = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        wzmpa__omc = True
        for dgu__lwus in (sort_node.key_arrs + sort_node.out_key_arrs +
            mzsu__fantr + fmv__flybj):
            if array_dists[dgu__lwus.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                dgu__lwus.name] != distributed_pass.Distribution.OneD_Var:
                wzmpa__omc = False
    loc = sort_node.loc
    uvn__dvins = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        ygapy__rztn = []
        for dgu__lwus in key_arrs:
            mvbf__ysna = _copy_array_nodes(dgu__lwus, nodes, typingctx,
                targetctx, typemap, calltypes)
            ygapy__rztn.append(mvbf__ysna)
        key_arrs = ygapy__rztn
        xqbie__wtvu = []
        for dgu__lwus in mzsu__fantr:
            lrhp__hhw = _copy_array_nodes(dgu__lwus, nodes, typingctx,
                targetctx, typemap, calltypes)
            xqbie__wtvu.append(lrhp__hhw)
        mzsu__fantr = xqbie__wtvu
    key_name_args = [f'key{wpdaj__rmih}' for wpdaj__rmih in range(len(
        key_arrs))]
    pcj__lkx = ', '.join(key_name_args)
    col_name_args = [f'c{wpdaj__rmih}' for wpdaj__rmih in range(len(
        mzsu__fantr))]
    ccvsa__auhgx = ', '.join(col_name_args)
    zzrbq__icuf = 'def f({}, {}):\n'.format(pcj__lkx, ccvsa__auhgx)
    zzrbq__icuf += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, wzmpa__omc)
    zzrbq__icuf += '  return key_arrs, data\n'
    ogx__mzywc = {}
    exec(zzrbq__icuf, {}, ogx__mzywc)
    aasj__lutqt = ogx__mzywc['f']
    yavao__maln = types.Tuple([typemap[dgu__lwus.name] for dgu__lwus in
        key_arrs])
    hgfzj__davxj = types.Tuple([typemap[dgu__lwus.name] for dgu__lwus in
        mzsu__fantr])
    znbw__fqewe = compile_to_numba_ir(aasj__lutqt, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(yavao__maln.types) + list(
        hgfzj__davxj.types)), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(znbw__fqewe, key_arrs + mzsu__fantr)
    nodes += znbw__fqewe.body[:-2]
    ibp__cfif = nodes[-1].target
    ktf__sfgyz = ir.Var(uvn__dvins, mk_unique_var('key_data'), loc)
    typemap[ktf__sfgyz.name] = yavao__maln
    gen_getitem(ktf__sfgyz, ibp__cfif, 0, calltypes, nodes)
    ecjd__cztnx = ir.Var(uvn__dvins, mk_unique_var('sort_data'), loc)
    typemap[ecjd__cztnx.name] = hgfzj__davxj
    gen_getitem(ecjd__cztnx, ibp__cfif, 1, calltypes, nodes)
    for wpdaj__rmih, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, ktf__sfgyz, wpdaj__rmih, calltypes, nodes)
    for wpdaj__rmih, var in enumerate(fmv__flybj):
        gen_getitem(var, ecjd__cztnx, wpdaj__rmih, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    znbw__fqewe = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(znbw__fqewe, [var])
    nodes += znbw__fqewe.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    zzrbq__icuf = ''
    uair__elj = len(key_name_args)
    kveg__mrw = ['array_to_info({})'.format(drz__hygpy) for drz__hygpy in
        key_name_args] + ['array_to_info({})'.format(drz__hygpy) for
        drz__hygpy in col_name_args]
    zzrbq__icuf += '  info_list_total = [{}]\n'.format(','.join(kveg__mrw))
    zzrbq__icuf += '  table_total = arr_info_list_to_table(info_list_total)\n'
    zzrbq__icuf += '  vect_ascending = np.array([{}])\n'.format(','.join(
        '1' if fkj__hdcz else '0' for fkj__hdcz in ascending_list))
    zzrbq__icuf += '  na_position = np.array([{}])\n'.format(','.join('1' if
        fkj__hdcz else '0' for fkj__hdcz in na_position_b))
    zzrbq__icuf += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(uair__elj, parallel_b))
    hektd__dgudj = 0
    eqqp__ttea = []
    for drz__hygpy in key_name_args:
        eqqp__ttea.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(hektd__dgudj, drz__hygpy))
        hektd__dgudj += 1
    zzrbq__icuf += '  key_arrs = ({},)\n'.format(','.join(eqqp__ttea))
    svoa__vhsol = []
    for drz__hygpy in col_name_args:
        svoa__vhsol.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(hektd__dgudj, drz__hygpy))
        hektd__dgudj += 1
    if len(svoa__vhsol) > 0:
        zzrbq__icuf += '  data = ({},)\n'.format(','.join(svoa__vhsol))
    else:
        zzrbq__icuf += '  data = ()\n'
    zzrbq__icuf += '  delete_table(out_table)\n'
    zzrbq__icuf += '  delete_table(table_total)\n'
    return zzrbq__icuf
