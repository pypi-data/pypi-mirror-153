"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
from collections import defaultdict
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from numba.extending import box, models, register_model
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.typing import BodoError
from bodo.utils.utils import debug_prints


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    pept__smkd = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    yyad__fwcc = []
    for gqu__yvxp in node.out_vars:
        typ = typemap[gqu__yvxp.name]
        if typ == types.none:
            continue
        xus__ektwa = array_analysis._gen_shape_call(equiv_set, gqu__yvxp,
            typ.ndim, None, pept__smkd)
        equiv_set.insert_equiv(gqu__yvxp, xus__ektwa)
        yyad__fwcc.append(xus__ektwa[0])
        equiv_set.define(gqu__yvxp, set())
    if len(yyad__fwcc) > 1:
        equiv_set.insert_equiv(*yyad__fwcc)
    return [], pept__smkd


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        cepl__ktfl = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        cepl__ktfl = Distribution.OneD_Var
    else:
        cepl__ktfl = Distribution.OneD
    for tner__kia in node.out_vars:
        if tner__kia.name in array_dists:
            cepl__ktfl = Distribution(min(cepl__ktfl.value, array_dists[
                tner__kia.name].value))
    for tner__kia in node.out_vars:
        array_dists[tner__kia.name] = cepl__ktfl


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        return
    for gqu__yvxp, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(gqu__yvxp.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    wxj__npn = []
    for gqu__yvxp in node.out_vars:
        vwhl__etd = visit_vars_inner(gqu__yvxp, callback, cbdata)
        wxj__npn.append(vwhl__etd)
    node.out_vars = wxj__npn
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for djwoy__qiw in node.filters:
            for qwvtd__lhz in range(len(djwoy__qiw)):
                val = djwoy__qiw[qwvtd__lhz]
                djwoy__qiw[qwvtd__lhz] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({tner__kia.name for tner__kia in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for mzg__ftv in node.filters:
            for tner__kia in mzg__ftv:
                if isinstance(tner__kia[2], ir.Var):
                    use_set.add(tner__kia[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    ygnhz__ikafh = set(tner__kia.name for tner__kia in node.out_vars)
    return set(), ygnhz__ikafh


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    wxj__npn = []
    for gqu__yvxp in node.out_vars:
        vwhl__etd = replace_vars_inner(gqu__yvxp, var_dict)
        wxj__npn.append(vwhl__etd)
    node.out_vars = wxj__npn
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for djwoy__qiw in node.filters:
            for qwvtd__lhz in range(len(djwoy__qiw)):
                val = djwoy__qiw[qwvtd__lhz]
                djwoy__qiw[qwvtd__lhz] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for gqu__yvxp in node.out_vars:
        kfw__bojyq = definitions[gqu__yvxp.name]
        if node not in kfw__bojyq:
            kfw__bojyq.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        rcoc__sqmwf = [tner__kia[2] for mzg__ftv in filters for tner__kia in
            mzg__ftv]
        zkxn__dxw = set()
        for xtcc__nhhuw in rcoc__sqmwf:
            if isinstance(xtcc__nhhuw, ir.Var):
                if xtcc__nhhuw.name not in zkxn__dxw:
                    filter_vars.append(xtcc__nhhuw)
                zkxn__dxw.add(xtcc__nhhuw.name)
        return {tner__kia.name: f'f{qwvtd__lhz}' for qwvtd__lhz, tner__kia in
            enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


class StreamReaderType(types.Opaque):

    def __init__(self):
        super(StreamReaderType, self).__init__(name='StreamReaderType')


stream_reader_type = StreamReaderType()
register_model(StreamReaderType)(models.OpaqueModel)


@box(StreamReaderType)
def box_stream_reader(typ, val, c):
    c.pyapi.incref(val)
    return val


def trim_extra_used_columns(used_columns, num_columns):
    tjv__lmwyk = len(used_columns)
    for qwvtd__lhz in range(len(used_columns) - 1, -1, -1):
        if used_columns[qwvtd__lhz] < num_columns:
            break
        tjv__lmwyk = qwvtd__lhz
    return used_columns[:tjv__lmwyk]


def cast_float_to_nullable(df, df_type):
    import bodo
    ahwjk__vcmie = {}
    for qwvtd__lhz, zenx__ubva in enumerate(df_type.data):
        if isinstance(zenx__ubva, bodo.IntegerArrayType):
            wkbcg__oddny = zenx__ubva.get_pandas_scalar_type_instance
            if wkbcg__oddny not in ahwjk__vcmie:
                ahwjk__vcmie[wkbcg__oddny] = []
            ahwjk__vcmie[wkbcg__oddny].append(df.columns[qwvtd__lhz])
    for typ, ovyle__wlivk in ahwjk__vcmie.items():
        df[ovyle__wlivk] = df[ovyle__wlivk].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    znmi__kfo = node.out_vars[0].name
    assert isinstance(typemap[znmi__kfo], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, uema__myt = get_live_column_nums_block(column_live_map,
            equiv_vars, znmi__kfo)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not uema__myt and not used_columns:
            used_columns = [0]
        if not uema__myt and len(used_columns) != len(node.type_usecol_offset):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    zln__gafq = False
    if array_dists is not None:
        nhe__tjzh = node.out_vars[0].name
        zln__gafq = array_dists[nhe__tjzh] in (Distribution.OneD,
            Distribution.OneD_Var)
        qlq__ccx = node.out_vars[1].name
        assert typemap[qlq__ccx] == types.none or not zln__gafq or array_dists[
            qlq__ccx] in (Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return zln__gafq


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source):
    shtqh__fncnf = 'None'
    vmjv__xwdgw = 'None'
    if filters:
        cemts__mxpcm = []
        lmv__mferb = []
        yoqht__cctah = False
        orig_colname_map = {c: qwvtd__lhz for qwvtd__lhz, c in enumerate(
            col_names)}
        for djwoy__qiw in filters:
            sfi__kceg = []
            gaj__laoj = []
            for tner__kia in djwoy__qiw:
                if isinstance(tner__kia[2], ir.Var):
                    jikd__ratgo, lxoej__obl = determine_filter_cast(
                        original_out_types, typemap, tner__kia,
                        orig_colname_map, partition_names, source)
                    if tner__kia[1] == 'in':
                        gaj__laoj.append(
                            f"(ds.field('{tner__kia[0]}').isin({filter_map[tner__kia[2].name]}))"
                            )
                    else:
                        gaj__laoj.append(
                            f"(ds.field('{tner__kia[0]}'){jikd__ratgo} {tner__kia[1]} ds.scalar({filter_map[tner__kia[2].name]}){lxoej__obl})"
                            )
                else:
                    assert tner__kia[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if tner__kia[1] == 'is not':
                        als__ebhi = '~'
                    else:
                        als__ebhi = ''
                    gaj__laoj.append(
                        f"({als__ebhi}ds.field('{tner__kia[0]}').is_null())")
                if not yoqht__cctah:
                    if tner__kia[0] in partition_names and isinstance(tner__kia
                        [2], ir.Var):
                        kcga__bxp = (
                            f"('{tner__kia[0]}', '{tner__kia[1]}', {filter_map[tner__kia[2].name]})"
                            )
                        sfi__kceg.append(kcga__bxp)
                    elif tner__kia[0] in partition_names and not isinstance(
                        tner__kia[2], ir.Var) and source == 'iceberg':
                        kcga__bxp = (
                            f"('{tner__kia[0]}', '{tner__kia[1]}', '{tner__kia[2]}')"
                            )
                        sfi__kceg.append(kcga__bxp)
            xuqzo__izthc = ''
            if sfi__kceg:
                xuqzo__izthc = ', '.join(sfi__kceg)
            else:
                yoqht__cctah = True
            mkznz__ionq = ' & '.join(gaj__laoj)
            if xuqzo__izthc:
                cemts__mxpcm.append(f'[{xuqzo__izthc}]')
            lmv__mferb.append(f'({mkznz__ionq})')
        tbfwh__eme = ', '.join(cemts__mxpcm)
        axzfo__etpka = ' | '.join(lmv__mferb)
        if tbfwh__eme and not yoqht__cctah:
            shtqh__fncnf = f'[{tbfwh__eme}]'
        vmjv__xwdgw = f'({axzfo__etpka})'
    return shtqh__fncnf, vmjv__xwdgw


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    zfxis__wgs = filter_val[0]
    bpde__umgt = col_types[orig_colname_map[zfxis__wgs]]
    sge__sklbh = bodo.utils.typing.element_type(bpde__umgt)
    if source == 'parquet' and zfxis__wgs in partition_names:
        if sge__sklbh == types.unicode_type:
            fyxa__bejrd = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(sge__sklbh, types.Integer):
            fyxa__bejrd = f'.cast(pyarrow.{sge__sklbh.name}(), safe=False)'
        else:
            fyxa__bejrd = ''
    else:
        fyxa__bejrd = ''
    tws__nupla = typemap[filter_val[2].name]
    if isinstance(tws__nupla, (types.List, types.Set)):
        hky__iepon = tws__nupla.dtype
    else:
        hky__iepon = tws__nupla
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(sge__sklbh,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(hky__iepon,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([sge__sklbh, hky__iepon]):
        if not bodo.utils.typing.is_safe_arrow_cast(sge__sklbh, hky__iepon):
            raise BodoError(
                f'Unsupported Arrow cast from {sge__sklbh} to {hky__iepon} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if sge__sklbh == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif sge__sklbh in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(tws__nupla, (types.List, types.Set)):
                slk__phflz = 'list' if isinstance(tws__nupla, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {slk__phflz} values with isin filter pushdown.'
                    )
            return fyxa__bejrd, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return fyxa__bejrd, ''
