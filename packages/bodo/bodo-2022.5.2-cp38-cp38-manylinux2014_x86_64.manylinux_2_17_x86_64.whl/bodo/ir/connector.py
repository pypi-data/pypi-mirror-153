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
    qnbfa__spkc = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    eco__kfi = []
    for bth__tbee in node.out_vars:
        typ = typemap[bth__tbee.name]
        if typ == types.none:
            continue
        aubx__wanh = array_analysis._gen_shape_call(equiv_set, bth__tbee,
            typ.ndim, None, qnbfa__spkc)
        equiv_set.insert_equiv(bth__tbee, aubx__wanh)
        eco__kfi.append(aubx__wanh[0])
        equiv_set.define(bth__tbee, set())
    if len(eco__kfi) > 1:
        equiv_set.insert_equiv(*eco__kfi)
    return [], qnbfa__spkc


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        twza__dijvy = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        twza__dijvy = Distribution.OneD_Var
    else:
        twza__dijvy = Distribution.OneD
    for ggbev__ytl in node.out_vars:
        if ggbev__ytl.name in array_dists:
            twza__dijvy = Distribution(min(twza__dijvy.value, array_dists[
                ggbev__ytl.name].value))
    for ggbev__ytl in node.out_vars:
        array_dists[ggbev__ytl.name] = twza__dijvy


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
    for bth__tbee, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(bth__tbee.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    fxeq__qzwta = []
    for bth__tbee in node.out_vars:
        xweg__kgwag = visit_vars_inner(bth__tbee, callback, cbdata)
        fxeq__qzwta.append(xweg__kgwag)
    node.out_vars = fxeq__qzwta
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for pwmo__kpfm in node.filters:
            for rqoey__qyjc in range(len(pwmo__kpfm)):
                val = pwmo__kpfm[rqoey__qyjc]
                pwmo__kpfm[rqoey__qyjc] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({ggbev__ytl.name for ggbev__ytl in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for mjpfi__dql in node.filters:
            for ggbev__ytl in mjpfi__dql:
                if isinstance(ggbev__ytl[2], ir.Var):
                    use_set.add(ggbev__ytl[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    klk__hjh = set(ggbev__ytl.name for ggbev__ytl in node.out_vars)
    return set(), klk__hjh


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    fxeq__qzwta = []
    for bth__tbee in node.out_vars:
        xweg__kgwag = replace_vars_inner(bth__tbee, var_dict)
        fxeq__qzwta.append(xweg__kgwag)
    node.out_vars = fxeq__qzwta
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for pwmo__kpfm in node.filters:
            for rqoey__qyjc in range(len(pwmo__kpfm)):
                val = pwmo__kpfm[rqoey__qyjc]
                pwmo__kpfm[rqoey__qyjc] = val[0], val[1], replace_vars_inner(
                    val[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for bth__tbee in node.out_vars:
        ifwm__hnk = definitions[bth__tbee.name]
        if node not in ifwm__hnk:
            ifwm__hnk.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        aqa__tugr = [ggbev__ytl[2] for mjpfi__dql in filters for ggbev__ytl in
            mjpfi__dql]
        ssm__yzm = set()
        for rtaew__mqd in aqa__tugr:
            if isinstance(rtaew__mqd, ir.Var):
                if rtaew__mqd.name not in ssm__yzm:
                    filter_vars.append(rtaew__mqd)
                ssm__yzm.add(rtaew__mqd.name)
        return {ggbev__ytl.name: f'f{rqoey__qyjc}' for rqoey__qyjc,
            ggbev__ytl in enumerate(filter_vars)}, filter_vars
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
    vbo__awx = len(used_columns)
    for rqoey__qyjc in range(len(used_columns) - 1, -1, -1):
        if used_columns[rqoey__qyjc] < num_columns:
            break
        vbo__awx = rqoey__qyjc
    return used_columns[:vbo__awx]


def cast_float_to_nullable(df, df_type):
    import bodo
    tvb__bwmy = {}
    for rqoey__qyjc, lqdt__iddo in enumerate(df_type.data):
        if isinstance(lqdt__iddo, bodo.IntegerArrayType):
            rywsv__aiug = lqdt__iddo.get_pandas_scalar_type_instance
            if rywsv__aiug not in tvb__bwmy:
                tvb__bwmy[rywsv__aiug] = []
            tvb__bwmy[rywsv__aiug].append(df.columns[rqoey__qyjc])
    for typ, zsy__xce in tvb__bwmy.items():
        df[zsy__xce] = df[zsy__xce].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    wyodu__lcr = node.out_vars[0].name
    assert isinstance(typemap[wyodu__lcr], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, nltr__gko = get_live_column_nums_block(column_live_map,
            equiv_vars, wyodu__lcr)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not nltr__gko and not used_columns:
            used_columns = [0]
        if not nltr__gko and len(used_columns) != len(node.type_usecol_offset):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    nup__bvs = False
    if array_dists is not None:
        ytba__cbg = node.out_vars[0].name
        nup__bvs = array_dists[ytba__cbg] in (Distribution.OneD,
            Distribution.OneD_Var)
        txfw__byz = node.out_vars[1].name
        assert typemap[txfw__byz] == types.none or not nup__bvs or array_dists[
            txfw__byz] in (Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return nup__bvs


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source):
    litls__gvd = 'None'
    ryfj__zlaw = 'None'
    if filters:
        tql__vwq = []
        lfqs__ocx = []
        begn__kmf = False
        orig_colname_map = {c: rqoey__qyjc for rqoey__qyjc, c in enumerate(
            col_names)}
        for pwmo__kpfm in filters:
            wuzb__pzma = []
            nwri__wpe = []
            for ggbev__ytl in pwmo__kpfm:
                if isinstance(ggbev__ytl[2], ir.Var):
                    uez__bjz, splt__bybot = determine_filter_cast(
                        original_out_types, typemap, ggbev__ytl,
                        orig_colname_map, partition_names, source)
                    if ggbev__ytl[1] == 'in':
                        nwri__wpe.append(
                            f"(ds.field('{ggbev__ytl[0]}').isin({filter_map[ggbev__ytl[2].name]}))"
                            )
                    else:
                        nwri__wpe.append(
                            f"(ds.field('{ggbev__ytl[0]}'){uez__bjz} {ggbev__ytl[1]} ds.scalar({filter_map[ggbev__ytl[2].name]}){splt__bybot})"
                            )
                else:
                    assert ggbev__ytl[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if ggbev__ytl[1] == 'is not':
                        ppb__dftyy = '~'
                    else:
                        ppb__dftyy = ''
                    nwri__wpe.append(
                        f"({ppb__dftyy}ds.field('{ggbev__ytl[0]}').is_null())")
                if not begn__kmf:
                    if ggbev__ytl[0] in partition_names and isinstance(
                        ggbev__ytl[2], ir.Var):
                        gtk__uxyo = (
                            f"('{ggbev__ytl[0]}', '{ggbev__ytl[1]}', {filter_map[ggbev__ytl[2].name]})"
                            )
                        wuzb__pzma.append(gtk__uxyo)
                    elif ggbev__ytl[0] in partition_names and not isinstance(
                        ggbev__ytl[2], ir.Var) and source == 'iceberg':
                        gtk__uxyo = (
                            f"('{ggbev__ytl[0]}', '{ggbev__ytl[1]}', '{ggbev__ytl[2]}')"
                            )
                        wuzb__pzma.append(gtk__uxyo)
            arfql__vtowt = ''
            if wuzb__pzma:
                arfql__vtowt = ', '.join(wuzb__pzma)
            else:
                begn__kmf = True
            zpshk__cyv = ' & '.join(nwri__wpe)
            if arfql__vtowt:
                tql__vwq.append(f'[{arfql__vtowt}]')
            lfqs__ocx.append(f'({zpshk__cyv})')
        ueyda__ffym = ', '.join(tql__vwq)
        ccy__zof = ' | '.join(lfqs__ocx)
        if ueyda__ffym and not begn__kmf:
            litls__gvd = f'[{ueyda__ffym}]'
        ryfj__zlaw = f'({ccy__zof})'
    return litls__gvd, ryfj__zlaw


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    wocrl__uqor = filter_val[0]
    lvmgg__mky = col_types[orig_colname_map[wocrl__uqor]]
    lizjw__hfq = bodo.utils.typing.element_type(lvmgg__mky)
    if source == 'parquet' and wocrl__uqor in partition_names:
        if lizjw__hfq == types.unicode_type:
            vsq__niwcf = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(lizjw__hfq, types.Integer):
            vsq__niwcf = f'.cast(pyarrow.{lizjw__hfq.name}(), safe=False)'
        else:
            vsq__niwcf = ''
    else:
        vsq__niwcf = ''
    wutua__hailt = typemap[filter_val[2].name]
    if isinstance(wutua__hailt, (types.List, types.Set)):
        ppcyi__cbu = wutua__hailt.dtype
    else:
        ppcyi__cbu = wutua__hailt
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lizjw__hfq,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ppcyi__cbu,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([lizjw__hfq, ppcyi__cbu]):
        if not bodo.utils.typing.is_safe_arrow_cast(lizjw__hfq, ppcyi__cbu):
            raise BodoError(
                f'Unsupported Arrow cast from {lizjw__hfq} to {ppcyi__cbu} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if lizjw__hfq == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif lizjw__hfq in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(wutua__hailt, (types.List, types.Set)):
                miwjk__otlid = 'list' if isinstance(wutua__hailt, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {miwjk__otlid} values with isin filter pushdown.'
                    )
            return vsq__niwcf, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return vsq__niwcf, ''
