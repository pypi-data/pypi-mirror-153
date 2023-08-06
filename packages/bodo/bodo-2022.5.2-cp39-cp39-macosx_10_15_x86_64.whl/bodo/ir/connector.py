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
    pxvpi__svbnm = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    izrdx__onqf = []
    for eifnh__iawzb in node.out_vars:
        typ = typemap[eifnh__iawzb.name]
        if typ == types.none:
            continue
        pflq__mgn = array_analysis._gen_shape_call(equiv_set, eifnh__iawzb,
            typ.ndim, None, pxvpi__svbnm)
        equiv_set.insert_equiv(eifnh__iawzb, pflq__mgn)
        izrdx__onqf.append(pflq__mgn[0])
        equiv_set.define(eifnh__iawzb, set())
    if len(izrdx__onqf) > 1:
        equiv_set.insert_equiv(*izrdx__onqf)
    return [], pxvpi__svbnm


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        kwi__cgqra = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        kwi__cgqra = Distribution.OneD_Var
    else:
        kwi__cgqra = Distribution.OneD
    for gfkkr__ifs in node.out_vars:
        if gfkkr__ifs.name in array_dists:
            kwi__cgqra = Distribution(min(kwi__cgqra.value, array_dists[
                gfkkr__ifs.name].value))
    for gfkkr__ifs in node.out_vars:
        array_dists[gfkkr__ifs.name] = kwi__cgqra


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
    for eifnh__iawzb, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(eifnh__iawzb.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    izla__tpmgx = []
    for eifnh__iawzb in node.out_vars:
        gwak__btojj = visit_vars_inner(eifnh__iawzb, callback, cbdata)
        izla__tpmgx.append(gwak__btojj)
    node.out_vars = izla__tpmgx
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for oxwjq__pykv in node.filters:
            for lle__sax in range(len(oxwjq__pykv)):
                val = oxwjq__pykv[lle__sax]
                oxwjq__pykv[lle__sax] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({gfkkr__ifs.name for gfkkr__ifs in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for fzvjv__vete in node.filters:
            for gfkkr__ifs in fzvjv__vete:
                if isinstance(gfkkr__ifs[2], ir.Var):
                    use_set.add(gfkkr__ifs[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    xzy__bjhe = set(gfkkr__ifs.name for gfkkr__ifs in node.out_vars)
    return set(), xzy__bjhe


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    izla__tpmgx = []
    for eifnh__iawzb in node.out_vars:
        gwak__btojj = replace_vars_inner(eifnh__iawzb, var_dict)
        izla__tpmgx.append(gwak__btojj)
    node.out_vars = izla__tpmgx
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for oxwjq__pykv in node.filters:
            for lle__sax in range(len(oxwjq__pykv)):
                val = oxwjq__pykv[lle__sax]
                oxwjq__pykv[lle__sax] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for eifnh__iawzb in node.out_vars:
        twui__qbq = definitions[eifnh__iawzb.name]
        if node not in twui__qbq:
            twui__qbq.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        ahfct__dbms = [gfkkr__ifs[2] for fzvjv__vete in filters for
            gfkkr__ifs in fzvjv__vete]
        syabs__opnnw = set()
        for bqro__qkyx in ahfct__dbms:
            if isinstance(bqro__qkyx, ir.Var):
                if bqro__qkyx.name not in syabs__opnnw:
                    filter_vars.append(bqro__qkyx)
                syabs__opnnw.add(bqro__qkyx.name)
        return {gfkkr__ifs.name: f'f{lle__sax}' for lle__sax, gfkkr__ifs in
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
    jvdw__jul = len(used_columns)
    for lle__sax in range(len(used_columns) - 1, -1, -1):
        if used_columns[lle__sax] < num_columns:
            break
        jvdw__jul = lle__sax
    return used_columns[:jvdw__jul]


def cast_float_to_nullable(df, df_type):
    import bodo
    nomdz__wgzw = {}
    for lle__sax, kzn__qkbfe in enumerate(df_type.data):
        if isinstance(kzn__qkbfe, bodo.IntegerArrayType):
            yqce__ngr = kzn__qkbfe.get_pandas_scalar_type_instance
            if yqce__ngr not in nomdz__wgzw:
                nomdz__wgzw[yqce__ngr] = []
            nomdz__wgzw[yqce__ngr].append(df.columns[lle__sax])
    for typ, ygnk__frkka in nomdz__wgzw.items():
        df[ygnk__frkka] = df[ygnk__frkka].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    zyres__uou = node.out_vars[0].name
    assert isinstance(typemap[zyres__uou], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, sbhw__gmwc = get_live_column_nums_block(column_live_map,
            equiv_vars, zyres__uou)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not sbhw__gmwc and not used_columns:
            used_columns = [0]
        if not sbhw__gmwc and len(used_columns) != len(node.type_usecol_offset
            ):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    spma__mlon = False
    if array_dists is not None:
        kkfzn__qrnd = node.out_vars[0].name
        spma__mlon = array_dists[kkfzn__qrnd] in (Distribution.OneD,
            Distribution.OneD_Var)
        csg__nfxji = node.out_vars[1].name
        assert typemap[csg__nfxji
            ] == types.none or not spma__mlon or array_dists[csg__nfxji] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return spma__mlon


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source):
    kjgjy__rgl = 'None'
    ozgyq__avp = 'None'
    if filters:
        mtln__nfmak = []
        iorkl__qfc = []
        vuo__ddai = False
        orig_colname_map = {c: lle__sax for lle__sax, c in enumerate(col_names)
            }
        for oxwjq__pykv in filters:
            dals__qtkom = []
            qzfxo__pibqi = []
            for gfkkr__ifs in oxwjq__pykv:
                if isinstance(gfkkr__ifs[2], ir.Var):
                    hpye__mbzm, uay__afsw = determine_filter_cast(
                        original_out_types, typemap, gfkkr__ifs,
                        orig_colname_map, partition_names, source)
                    if gfkkr__ifs[1] == 'in':
                        qzfxo__pibqi.append(
                            f"(ds.field('{gfkkr__ifs[0]}').isin({filter_map[gfkkr__ifs[2].name]}))"
                            )
                    else:
                        qzfxo__pibqi.append(
                            f"(ds.field('{gfkkr__ifs[0]}'){hpye__mbzm} {gfkkr__ifs[1]} ds.scalar({filter_map[gfkkr__ifs[2].name]}){uay__afsw})"
                            )
                else:
                    assert gfkkr__ifs[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if gfkkr__ifs[1] == 'is not':
                        vsn__avy = '~'
                    else:
                        vsn__avy = ''
                    qzfxo__pibqi.append(
                        f"({vsn__avy}ds.field('{gfkkr__ifs[0]}').is_null())")
                if not vuo__ddai:
                    if gfkkr__ifs[0] in partition_names and isinstance(
                        gfkkr__ifs[2], ir.Var):
                        acx__mndm = (
                            f"('{gfkkr__ifs[0]}', '{gfkkr__ifs[1]}', {filter_map[gfkkr__ifs[2].name]})"
                            )
                        dals__qtkom.append(acx__mndm)
                    elif gfkkr__ifs[0] in partition_names and not isinstance(
                        gfkkr__ifs[2], ir.Var) and source == 'iceberg':
                        acx__mndm = (
                            f"('{gfkkr__ifs[0]}', '{gfkkr__ifs[1]}', '{gfkkr__ifs[2]}')"
                            )
                        dals__qtkom.append(acx__mndm)
            xvpx__uzwbt = ''
            if dals__qtkom:
                xvpx__uzwbt = ', '.join(dals__qtkom)
            else:
                vuo__ddai = True
            zjtc__mula = ' & '.join(qzfxo__pibqi)
            if xvpx__uzwbt:
                mtln__nfmak.append(f'[{xvpx__uzwbt}]')
            iorkl__qfc.append(f'({zjtc__mula})')
        npmw__fqf = ', '.join(mtln__nfmak)
        evg__sechq = ' | '.join(iorkl__qfc)
        if npmw__fqf and not vuo__ddai:
            kjgjy__rgl = f'[{npmw__fqf}]'
        ozgyq__avp = f'({evg__sechq})'
    return kjgjy__rgl, ozgyq__avp


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    jsy__jmbc = filter_val[0]
    hsczv__rmos = col_types[orig_colname_map[jsy__jmbc]]
    crrhu__obp = bodo.utils.typing.element_type(hsczv__rmos)
    if source == 'parquet' and jsy__jmbc in partition_names:
        if crrhu__obp == types.unicode_type:
            yfwn__qkfpr = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(crrhu__obp, types.Integer):
            yfwn__qkfpr = f'.cast(pyarrow.{crrhu__obp.name}(), safe=False)'
        else:
            yfwn__qkfpr = ''
    else:
        yfwn__qkfpr = ''
    qsshl__mzwa = typemap[filter_val[2].name]
    if isinstance(qsshl__mzwa, (types.List, types.Set)):
        qcepd__wqx = qsshl__mzwa.dtype
    else:
        qcepd__wqx = qsshl__mzwa
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(crrhu__obp,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(qcepd__wqx,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([crrhu__obp, qcepd__wqx]):
        if not bodo.utils.typing.is_safe_arrow_cast(crrhu__obp, qcepd__wqx):
            raise BodoError(
                f'Unsupported Arrow cast from {crrhu__obp} to {qcepd__wqx} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if crrhu__obp == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif crrhu__obp in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(qsshl__mzwa, (types.List, types.Set)):
                vbl__jyhkq = 'list' if isinstance(qsshl__mzwa, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {vbl__jyhkq} values with isin filter pushdown.'
                    )
            return yfwn__qkfpr, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return yfwn__qkfpr, ''
