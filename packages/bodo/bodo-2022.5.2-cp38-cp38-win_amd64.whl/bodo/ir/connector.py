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
    enr__fanox = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    qnt__duxt = []
    for hkk__eooa in node.out_vars:
        typ = typemap[hkk__eooa.name]
        if typ == types.none:
            continue
        aht__ozb = array_analysis._gen_shape_call(equiv_set, hkk__eooa, typ
            .ndim, None, enr__fanox)
        equiv_set.insert_equiv(hkk__eooa, aht__ozb)
        qnt__duxt.append(aht__ozb[0])
        equiv_set.define(hkk__eooa, set())
    if len(qnt__duxt) > 1:
        equiv_set.insert_equiv(*qnt__duxt)
    return [], enr__fanox


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        idt__gduu = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        idt__gduu = Distribution.OneD_Var
    else:
        idt__gduu = Distribution.OneD
    for duc__jvm in node.out_vars:
        if duc__jvm.name in array_dists:
            idt__gduu = Distribution(min(idt__gduu.value, array_dists[
                duc__jvm.name].value))
    for duc__jvm in node.out_vars:
        array_dists[duc__jvm.name] = idt__gduu


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
    for hkk__eooa, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(hkk__eooa.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    loc__kks = []
    for hkk__eooa in node.out_vars:
        mtu__azpe = visit_vars_inner(hkk__eooa, callback, cbdata)
        loc__kks.append(mtu__azpe)
    node.out_vars = loc__kks
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for pcv__pmay in node.filters:
            for ezqf__zyr in range(len(pcv__pmay)):
                val = pcv__pmay[ezqf__zyr]
                pcv__pmay[ezqf__zyr] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({duc__jvm.name for duc__jvm in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for iejc__toi in node.filters:
            for duc__jvm in iejc__toi:
                if isinstance(duc__jvm[2], ir.Var):
                    use_set.add(duc__jvm[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    bfw__abkt = set(duc__jvm.name for duc__jvm in node.out_vars)
    return set(), bfw__abkt


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    loc__kks = []
    for hkk__eooa in node.out_vars:
        mtu__azpe = replace_vars_inner(hkk__eooa, var_dict)
        loc__kks.append(mtu__azpe)
    node.out_vars = loc__kks
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for pcv__pmay in node.filters:
            for ezqf__zyr in range(len(pcv__pmay)):
                val = pcv__pmay[ezqf__zyr]
                pcv__pmay[ezqf__zyr] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for hkk__eooa in node.out_vars:
        zcf__mop = definitions[hkk__eooa.name]
        if node not in zcf__mop:
            zcf__mop.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        vfu__gwc = [duc__jvm[2] for iejc__toi in filters for duc__jvm in
            iejc__toi]
        imojn__pnmxt = set()
        for lsit__xxtqz in vfu__gwc:
            if isinstance(lsit__xxtqz, ir.Var):
                if lsit__xxtqz.name not in imojn__pnmxt:
                    filter_vars.append(lsit__xxtqz)
                imojn__pnmxt.add(lsit__xxtqz.name)
        return {duc__jvm.name: f'f{ezqf__zyr}' for ezqf__zyr, duc__jvm in
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
    zhyz__stfa = len(used_columns)
    for ezqf__zyr in range(len(used_columns) - 1, -1, -1):
        if used_columns[ezqf__zyr] < num_columns:
            break
        zhyz__stfa = ezqf__zyr
    return used_columns[:zhyz__stfa]


def cast_float_to_nullable(df, df_type):
    import bodo
    raphg__cum = {}
    for ezqf__zyr, inpd__flvd in enumerate(df_type.data):
        if isinstance(inpd__flvd, bodo.IntegerArrayType):
            fvruk__prr = inpd__flvd.get_pandas_scalar_type_instance
            if fvruk__prr not in raphg__cum:
                raphg__cum[fvruk__prr] = []
            raphg__cum[fvruk__prr].append(df.columns[ezqf__zyr])
    for typ, zlxlt__xqry in raphg__cum.items():
        df[zlxlt__xqry] = df[zlxlt__xqry].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    qqxqm__eaxif = node.out_vars[0].name
    assert isinstance(typemap[qqxqm__eaxif], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, elacc__hrqun = get_live_column_nums_block(column_live_map
            , equiv_vars, qqxqm__eaxif)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not elacc__hrqun and not used_columns:
            used_columns = [0]
        if not elacc__hrqun and len(used_columns) != len(node.
            type_usecol_offset):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    bpgs__whhd = False
    if array_dists is not None:
        nix__mvua = node.out_vars[0].name
        bpgs__whhd = array_dists[nix__mvua] in (Distribution.OneD,
            Distribution.OneD_Var)
        hdloa__ilo = node.out_vars[1].name
        assert typemap[hdloa__ilo
            ] == types.none or not bpgs__whhd or array_dists[hdloa__ilo] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return bpgs__whhd


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source):
    kigf__sdzm = 'None'
    lqsp__flkj = 'None'
    if filters:
        ydt__dmt = []
        rlgnr__klv = []
        yohi__qwnth = False
        orig_colname_map = {c: ezqf__zyr for ezqf__zyr, c in enumerate(
            col_names)}
        for pcv__pmay in filters:
            chye__oykq = []
            qfa__kam = []
            for duc__jvm in pcv__pmay:
                if isinstance(duc__jvm[2], ir.Var):
                    jatdx__fluh, sckvy__nqtch = determine_filter_cast(
                        original_out_types, typemap, duc__jvm,
                        orig_colname_map, partition_names, source)
                    if duc__jvm[1] == 'in':
                        qfa__kam.append(
                            f"(ds.field('{duc__jvm[0]}').isin({filter_map[duc__jvm[2].name]}))"
                            )
                    else:
                        qfa__kam.append(
                            f"(ds.field('{duc__jvm[0]}'){jatdx__fluh} {duc__jvm[1]} ds.scalar({filter_map[duc__jvm[2].name]}){sckvy__nqtch})"
                            )
                else:
                    assert duc__jvm[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if duc__jvm[1] == 'is not':
                        jhtr__zvg = '~'
                    else:
                        jhtr__zvg = ''
                    qfa__kam.append(
                        f"({jhtr__zvg}ds.field('{duc__jvm[0]}').is_null())")
                if not yohi__qwnth:
                    if duc__jvm[0] in partition_names and isinstance(duc__jvm
                        [2], ir.Var):
                        hdxo__iumaq = (
                            f"('{duc__jvm[0]}', '{duc__jvm[1]}', {filter_map[duc__jvm[2].name]})"
                            )
                        chye__oykq.append(hdxo__iumaq)
                    elif duc__jvm[0] in partition_names and not isinstance(
                        duc__jvm[2], ir.Var) and source == 'iceberg':
                        hdxo__iumaq = (
                            f"('{duc__jvm[0]}', '{duc__jvm[1]}', '{duc__jvm[2]}')"
                            )
                        chye__oykq.append(hdxo__iumaq)
            rgap__xic = ''
            if chye__oykq:
                rgap__xic = ', '.join(chye__oykq)
            else:
                yohi__qwnth = True
            onay__xff = ' & '.join(qfa__kam)
            if rgap__xic:
                ydt__dmt.append(f'[{rgap__xic}]')
            rlgnr__klv.append(f'({onay__xff})')
        qqt__fjxb = ', '.join(ydt__dmt)
        ycq__wwfrj = ' | '.join(rlgnr__klv)
        if qqt__fjxb and not yohi__qwnth:
            kigf__sdzm = f'[{qqt__fjxb}]'
        lqsp__flkj = f'({ycq__wwfrj})'
    return kigf__sdzm, lqsp__flkj


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    vqmj__txda = filter_val[0]
    wcd__wks = col_types[orig_colname_map[vqmj__txda]]
    zsgx__ekrv = bodo.utils.typing.element_type(wcd__wks)
    if source == 'parquet' and vqmj__txda in partition_names:
        if zsgx__ekrv == types.unicode_type:
            alxh__egdj = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(zsgx__ekrv, types.Integer):
            alxh__egdj = f'.cast(pyarrow.{zsgx__ekrv.name}(), safe=False)'
        else:
            alxh__egdj = ''
    else:
        alxh__egdj = ''
    gxwok__tzkd = typemap[filter_val[2].name]
    if isinstance(gxwok__tzkd, (types.List, types.Set)):
        vbm__zbf = gxwok__tzkd.dtype
    else:
        vbm__zbf = gxwok__tzkd
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(zsgx__ekrv,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(vbm__zbf,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([zsgx__ekrv, vbm__zbf]):
        if not bodo.utils.typing.is_safe_arrow_cast(zsgx__ekrv, vbm__zbf):
            raise BodoError(
                f'Unsupported Arrow cast from {zsgx__ekrv} to {vbm__zbf} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if zsgx__ekrv == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif zsgx__ekrv in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(gxwok__tzkd, (types.List, types.Set)):
                jlt__ktcq = 'list' if isinstance(gxwok__tzkd, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {jlt__ktcq} values with isin filter pushdown.'
                    )
            return alxh__egdj, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return alxh__egdj, ''
