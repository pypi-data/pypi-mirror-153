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
    hcgrp__uqb = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    oljl__xfux = []
    for bmpgn__kdc in node.out_vars:
        typ = typemap[bmpgn__kdc.name]
        if typ == types.none:
            continue
        kmtz__icwc = array_analysis._gen_shape_call(equiv_set, bmpgn__kdc,
            typ.ndim, None, hcgrp__uqb)
        equiv_set.insert_equiv(bmpgn__kdc, kmtz__icwc)
        oljl__xfux.append(kmtz__icwc[0])
        equiv_set.define(bmpgn__kdc, set())
    if len(oljl__xfux) > 1:
        equiv_set.insert_equiv(*oljl__xfux)
    return [], hcgrp__uqb


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        ztr__yemkm = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        ztr__yemkm = Distribution.OneD_Var
    else:
        ztr__yemkm = Distribution.OneD
    for nmbi__aub in node.out_vars:
        if nmbi__aub.name in array_dists:
            ztr__yemkm = Distribution(min(ztr__yemkm.value, array_dists[
                nmbi__aub.name].value))
    for nmbi__aub in node.out_vars:
        array_dists[nmbi__aub.name] = ztr__yemkm


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
    for bmpgn__kdc, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(bmpgn__kdc.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    fwr__lje = []
    for bmpgn__kdc in node.out_vars:
        cxhq__qfra = visit_vars_inner(bmpgn__kdc, callback, cbdata)
        fwr__lje.append(cxhq__qfra)
    node.out_vars = fwr__lje
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for nasnn__prsjq in node.filters:
            for hvrpi__vwvo in range(len(nasnn__prsjq)):
                val = nasnn__prsjq[hvrpi__vwvo]
                nasnn__prsjq[hvrpi__vwvo] = val[0], val[1], visit_vars_inner(
                    val[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({nmbi__aub.name for nmbi__aub in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for mymq__jhm in node.filters:
            for nmbi__aub in mymq__jhm:
                if isinstance(nmbi__aub[2], ir.Var):
                    use_set.add(nmbi__aub[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    zesv__qyuy = set(nmbi__aub.name for nmbi__aub in node.out_vars)
    return set(), zesv__qyuy


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    fwr__lje = []
    for bmpgn__kdc in node.out_vars:
        cxhq__qfra = replace_vars_inner(bmpgn__kdc, var_dict)
        fwr__lje.append(cxhq__qfra)
    node.out_vars = fwr__lje
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for nasnn__prsjq in node.filters:
            for hvrpi__vwvo in range(len(nasnn__prsjq)):
                val = nasnn__prsjq[hvrpi__vwvo]
                nasnn__prsjq[hvrpi__vwvo] = val[0], val[1], replace_vars_inner(
                    val[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for bmpgn__kdc in node.out_vars:
        nhdv__vuli = definitions[bmpgn__kdc.name]
        if node not in nhdv__vuli:
            nhdv__vuli.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        ogjzn__vvprg = [nmbi__aub[2] for mymq__jhm in filters for nmbi__aub in
            mymq__jhm]
        zfa__qxk = set()
        for kru__vpq in ogjzn__vvprg:
            if isinstance(kru__vpq, ir.Var):
                if kru__vpq.name not in zfa__qxk:
                    filter_vars.append(kru__vpq)
                zfa__qxk.add(kru__vpq.name)
        return {nmbi__aub.name: f'f{hvrpi__vwvo}' for hvrpi__vwvo,
            nmbi__aub in enumerate(filter_vars)}, filter_vars
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
    gotel__iwa = len(used_columns)
    for hvrpi__vwvo in range(len(used_columns) - 1, -1, -1):
        if used_columns[hvrpi__vwvo] < num_columns:
            break
        gotel__iwa = hvrpi__vwvo
    return used_columns[:gotel__iwa]


def cast_float_to_nullable(df, df_type):
    import bodo
    zifrl__uggp = {}
    for hvrpi__vwvo, wqbn__szoqm in enumerate(df_type.data):
        if isinstance(wqbn__szoqm, bodo.IntegerArrayType):
            iaq__zdfbk = wqbn__szoqm.get_pandas_scalar_type_instance
            if iaq__zdfbk not in zifrl__uggp:
                zifrl__uggp[iaq__zdfbk] = []
            zifrl__uggp[iaq__zdfbk].append(df.columns[hvrpi__vwvo])
    for typ, ewd__vbb in zifrl__uggp.items():
        df[ewd__vbb] = df[ewd__vbb].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    ipci__mkvav = node.out_vars[0].name
    assert isinstance(typemap[ipci__mkvav], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, bnxdt__vjde = get_live_column_nums_block(column_live_map,
            equiv_vars, ipci__mkvav)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not bnxdt__vjde and not used_columns:
            used_columns = [0]
        if not bnxdt__vjde and len(used_columns) != len(node.type_usecol_offset
            ):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    iayk__jrvvy = False
    if array_dists is not None:
        djmx__cncid = node.out_vars[0].name
        iayk__jrvvy = array_dists[djmx__cncid] in (Distribution.OneD,
            Distribution.OneD_Var)
        toj__nmxz = node.out_vars[1].name
        assert typemap[toj__nmxz
            ] == types.none or not iayk__jrvvy or array_dists[toj__nmxz] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return iayk__jrvvy


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source):
    sjlsb__gvt = 'None'
    ttjt__edpu = 'None'
    if filters:
        xzwpt__dhoaf = []
        xubdc__ooxx = []
        ujbv__vhhz = False
        orig_colname_map = {c: hvrpi__vwvo for hvrpi__vwvo, c in enumerate(
            col_names)}
        for nasnn__prsjq in filters:
            bqmxy__tszod = []
            lsqxg__vlf = []
            for nmbi__aub in nasnn__prsjq:
                if isinstance(nmbi__aub[2], ir.Var):
                    eimw__rsvlw, hhtn__eiy = determine_filter_cast(
                        original_out_types, typemap, nmbi__aub,
                        orig_colname_map, partition_names, source)
                    if nmbi__aub[1] == 'in':
                        lsqxg__vlf.append(
                            f"(ds.field('{nmbi__aub[0]}').isin({filter_map[nmbi__aub[2].name]}))"
                            )
                    else:
                        lsqxg__vlf.append(
                            f"(ds.field('{nmbi__aub[0]}'){eimw__rsvlw} {nmbi__aub[1]} ds.scalar({filter_map[nmbi__aub[2].name]}){hhtn__eiy})"
                            )
                else:
                    assert nmbi__aub[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if nmbi__aub[1] == 'is not':
                        ndu__ehx = '~'
                    else:
                        ndu__ehx = ''
                    lsqxg__vlf.append(
                        f"({ndu__ehx}ds.field('{nmbi__aub[0]}').is_null())")
                if not ujbv__vhhz:
                    if nmbi__aub[0] in partition_names and isinstance(nmbi__aub
                        [2], ir.Var):
                        nlxv__jjdom = (
                            f"('{nmbi__aub[0]}', '{nmbi__aub[1]}', {filter_map[nmbi__aub[2].name]})"
                            )
                        bqmxy__tszod.append(nlxv__jjdom)
                    elif nmbi__aub[0] in partition_names and not isinstance(
                        nmbi__aub[2], ir.Var) and source == 'iceberg':
                        nlxv__jjdom = (
                            f"('{nmbi__aub[0]}', '{nmbi__aub[1]}', '{nmbi__aub[2]}')"
                            )
                        bqmxy__tszod.append(nlxv__jjdom)
            grc__fnlzg = ''
            if bqmxy__tszod:
                grc__fnlzg = ', '.join(bqmxy__tszod)
            else:
                ujbv__vhhz = True
            nuw__vsr = ' & '.join(lsqxg__vlf)
            if grc__fnlzg:
                xzwpt__dhoaf.append(f'[{grc__fnlzg}]')
            xubdc__ooxx.append(f'({nuw__vsr})')
        edep__itg = ', '.join(xzwpt__dhoaf)
        grae__ukw = ' | '.join(xubdc__ooxx)
        if edep__itg and not ujbv__vhhz:
            sjlsb__gvt = f'[{edep__itg}]'
        ttjt__edpu = f'({grae__ukw})'
    return sjlsb__gvt, ttjt__edpu


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    qkqi__xlws = filter_val[0]
    wqiy__rlw = col_types[orig_colname_map[qkqi__xlws]]
    oauim__kcqa = bodo.utils.typing.element_type(wqiy__rlw)
    if source == 'parquet' and qkqi__xlws in partition_names:
        if oauim__kcqa == types.unicode_type:
            wdbw__nxewu = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(oauim__kcqa, types.Integer):
            wdbw__nxewu = f'.cast(pyarrow.{oauim__kcqa.name}(), safe=False)'
        else:
            wdbw__nxewu = ''
    else:
        wdbw__nxewu = ''
    nkj__fpo = typemap[filter_val[2].name]
    if isinstance(nkj__fpo, (types.List, types.Set)):
        orn__bbfqe = nkj__fpo.dtype
    else:
        orn__bbfqe = nkj__fpo
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(oauim__kcqa,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(orn__bbfqe,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([oauim__kcqa, orn__bbfqe]):
        if not bodo.utils.typing.is_safe_arrow_cast(oauim__kcqa, orn__bbfqe):
            raise BodoError(
                f'Unsupported Arrow cast from {oauim__kcqa} to {orn__bbfqe} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if oauim__kcqa == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif oauim__kcqa in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(nkj__fpo, (types.List, types.Set)):
                eljd__ozkqw = 'list' if isinstance(nkj__fpo, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {eljd__ozkqw} values with isin filter pushdown.'
                    )
            return wdbw__nxewu, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return wdbw__nxewu, ''
