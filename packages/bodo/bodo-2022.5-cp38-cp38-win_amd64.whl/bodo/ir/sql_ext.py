"""
Implementation of pd.read_sql in BODO.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.io.helpers import PyArrowTableSchemaType, is_nullable
from bodo.io.parquet_pio import ParquetPredicateType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request, connection, df_out, df_colnames,
        out_vars, out_types, converted_colnames, db_type, loc,
        unsupported_columns, unsupported_arrow_types, is_select_query,
        index_column_name, index_column_type, database_schema,
        pyarrow_table_schema=None):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.type_usecol_offset = list(range(len(df_colnames)))
        self.database_schema = database_schema
        self.pyarrow_table_schema = pyarrow_table_schema

    def __repr__(self):
        return (
            f'{self.df_out} = ReadSql(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, vars={self.out_vars}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, type_usecol_offset={self.type_usecol_offset}, database_schema={self.database_schema}, pyarrow_table_schema={self.pyarrow_table_schema})'
            )


def parse_dbtype(con_str):
    bgaxa__pln = urlparse(con_str)
    db_type = bgaxa__pln.scheme
    fne__shmp = bgaxa__pln.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', fne__shmp
    if db_type == 'mysql+pymysql':
        return 'mysql', fne__shmp
    return db_type, fne__shmp


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    pcmxy__glxg = sql_node.out_vars[0].name
    vjz__araob = sql_node.out_vars[1].name
    if pcmxy__glxg not in lives and vjz__araob not in lives:
        return None
    elif pcmxy__glxg not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif vjz__araob not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        fvqn__ami = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        jwf__mlknn = []
        flyk__skasj = []
        for vykst__avf in sql_node.type_usecol_offset:
            tvs__fdzek = sql_node.df_colnames[vykst__avf]
            jwf__mlknn.append(tvs__fdzek)
            if isinstance(sql_node.out_types[vykst__avf], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                flyk__skasj.append(tvs__fdzek)
        if sql_node.index_column_name:
            jwf__mlknn.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                flyk__skasj.append(sql_node.index_column_name)
        wybkz__jnawd = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', fvqn__ami,
            wybkz__jnawd, jwf__mlknn)
        if flyk__skasj:
            cvdx__iqp = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', cvdx__iqp,
                wybkz__jnawd, flyk__skasj)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        qwntc__nxfzx = set(sql_node.unsupported_columns)
        kcoiq__pad = set(sql_node.type_usecol_offset)
        qczw__ymv = kcoiq__pad & qwntc__nxfzx
        if qczw__ymv:
            oqenc__ekrk = sorted(qczw__ymv)
            dvyd__rkkj = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            kpef__wum = 0
            for qklzn__dmrr in oqenc__ekrk:
                while sql_node.unsupported_columns[kpef__wum] != qklzn__dmrr:
                    kpef__wum += 1
                dvyd__rkkj.append(
                    f"Column '{sql_node.original_df_colnames[qklzn__dmrr]}' with unsupported arrow type {sql_node.unsupported_arrow_types[kpef__wum]}"
                    )
                kpef__wum += 1
            qovje__ejdt = '\n'.join(dvyd__rkkj)
            raise BodoError(qovje__ejdt, loc=sql_node.loc)
    ijqer__vxatm, ume__uyuq = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    pua__dggi = ', '.join(ijqer__vxatm.values())
    pdik__hrsf = (
        f'def sql_impl(sql_request, conn, database_schema, {pua__dggi}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        hfr__azgg = []
        for xkfy__lim in sql_node.filters:
            jwom__hoihf = [' '.join(['(', laqcp__acy[0], laqcp__acy[1], '{' +
                ijqer__vxatm[laqcp__acy[2].name] + '}' if isinstance(
                laqcp__acy[2], ir.Var) else laqcp__acy[2], ')']) for
                laqcp__acy in xkfy__lim]
            hfr__azgg.append(' ( ' + ' AND '.join(jwom__hoihf) + ' ) ')
        xpmia__tbq = ' WHERE ' + ' OR '.join(hfr__azgg)
        for vykst__avf, jmw__vwd in enumerate(ijqer__vxatm.values()):
            pdik__hrsf += f'    {jmw__vwd} = get_sql_literal({jmw__vwd})\n'
        pdik__hrsf += f'    sql_request = f"{{sql_request}} {xpmia__tbq}"\n'
    lcmn__itj = ''
    if sql_node.db_type == 'iceberg':
        lcmn__itj = pua__dggi
    pdik__hrsf += f"""    (table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {lcmn__itj})
"""
    feg__imaa = {}
    exec(pdik__hrsf, {}, feg__imaa)
    yutn__rgvdp = feg__imaa['sql_impl']
    cgh__gqkvw = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, typemap, sql_node.filters, sql_node.
        pyarrow_table_schema)
    edntc__ewnrw = (types.none if sql_node.database_schema is None else
        string_type)
    meuhw__jepiq = compile_to_numba_ir(yutn__rgvdp, {'_sql_reader_py':
        cgh__gqkvw, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type,
        edntc__ewnrw) + tuple(typemap[llzjb__xlre.name] for llzjb__xlre in
        ume__uyuq), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        naa__tcyat = [sql_node.df_colnames[vykst__avf] for vykst__avf in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            naa__tcyat.append(sql_node.index_column_name)
        glzat__cvzt = escape_column_names(naa__tcyat, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            skueo__wlso = ('SELECT ' + glzat__cvzt + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            skueo__wlso = ('SELECT ' + glzat__cvzt + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        skueo__wlso = sql_node.sql_request
    replace_arg_nodes(meuhw__jepiq, [ir.Const(skueo__wlso, sql_node.loc),
        ir.Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + ume__uyuq)
    portt__dtqbv = meuhw__jepiq.body[:-3]
    portt__dtqbv[-2].target = sql_node.out_vars[0]
    portt__dtqbv[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        portt__dtqbv.pop(-1)
    elif not sql_node.type_usecol_offset:
        portt__dtqbv.pop(-2)
    return portt__dtqbv


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        naa__tcyat = [(dvdux__tyk.upper() if dvdux__tyk in
            converted_colnames else dvdux__tyk) for dvdux__tyk in col_names]
        glzat__cvzt = ', '.join([f'"{dvdux__tyk}"' for dvdux__tyk in
            naa__tcyat])
    elif db_type == 'mysql':
        glzat__cvzt = ', '.join([f'`{dvdux__tyk}`' for dvdux__tyk in col_names]
            )
    else:
        glzat__cvzt = ', '.join([f'"{dvdux__tyk}"' for dvdux__tyk in col_names]
            )
    return glzat__cvzt


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    zzyz__gycg = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(zzyz__gycg,
        'Filter pushdown')
    if zzyz__gycg == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(zzyz__gycg, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif zzyz__gycg == bodo.pd_timestamp_type:

        def impl(filter_value):
            dejh__jbnkb = filter_value.nanosecond
            pip__pwz = ''
            if dejh__jbnkb < 10:
                pip__pwz = '00'
            elif dejh__jbnkb < 100:
                pip__pwz = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{pip__pwz}{dejh__jbnkb}'"
                )
        return impl
    elif zzyz__gycg == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {zzyz__gycg} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    cyo__gbfwr = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    zzyz__gycg = types.unliteral(filter_value)
    if isinstance(zzyz__gycg, types.List) and (isinstance(zzyz__gycg.dtype,
        scalar_isinstance) or zzyz__gycg.dtype in cyo__gbfwr):

        def impl(filter_value):
            xth__dam = ', '.join([_get_snowflake_sql_literal_scalar(
                dvdux__tyk) for dvdux__tyk in filter_value])
            return f'({xth__dam})'
        return impl
    elif isinstance(zzyz__gycg, scalar_isinstance) or zzyz__gycg in cyo__gbfwr:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {zzyz__gycg} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.df_colnames
        )


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as wfrl__lypl:
        kfm__outs = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(kfm__outs)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as wfrl__lypl:
        kfm__outs = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(kfm__outs)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as wfrl__lypl:
        kfm__outs = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(kfm__outs)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as wfrl__lypl:
        kfm__outs = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(kfm__outs)


def req_limit(sql_request):
    import re
    czrbo__apefd = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    avuq__pco = czrbo__apefd.search(sql_request)
    if avuq__pco:
        return int(avuq__pco.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, typemap, filters, pyarrow_table_schema):
    ngpg__nhxj = next_label()
    naa__tcyat = [col_names[vykst__avf] for vykst__avf in type_usecol_offset]
    mbgar__aczv = [col_typs[vykst__avf] for vykst__avf in type_usecol_offset]
    if index_column_name:
        naa__tcyat.append(index_column_name)
        mbgar__aczv.append(index_column_type)
    lzevq__srixb = None
    etag__owhc = None
    ovgxe__agme = types.none
    qvokp__qjpz = None
    if type_usecol_offset:
        ovgxe__agme = TableType(tuple(col_typs))
    lcmn__itj = ''
    ijqer__vxatm = {}
    ume__uyuq = []
    if filters and db_type == 'iceberg':
        ijqer__vxatm, ume__uyuq = bodo.ir.connector.generate_filter_map(filters
            )
        lcmn__itj = ', '.join(ijqer__vxatm.values())
    pdik__hrsf = (
        f'def sql_reader_py(sql_request, conn, database_schema, {lcmn__itj}):\n'
        )
    if db_type == 'iceberg':
        vzlda__fxrg, krtoc__qjs = bodo.ir.connector.generate_arrow_filters(
            filters, ijqer__vxatm, ume__uyuq, col_names, col_names,
            col_typs, typemap, 'iceberg')
        slflh__lwwaj = ',' if lcmn__itj else ''
        pdik__hrsf += (
            f"  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})\n")
        pdik__hrsf += f"""  dnf_filters, expr_filters = get_filters_pyobject("{vzlda__fxrg}", "{krtoc__qjs}", ({lcmn__itj}{slflh__lwwaj}))
"""
        pdik__hrsf += f'  out_table = iceberg_read(\n'
        pdik__hrsf += (
            f'    unicode_to_utf8(conn), unicode_to_utf8(database_schema),\n')
        pdik__hrsf += (
            f'    unicode_to_utf8(sql_request), {parallel}, dnf_filters,\n')
        pdik__hrsf += (
            f'    expr_filters, selected_cols_arr_{ngpg__nhxj}.ctypes,\n')
        pdik__hrsf += (
            f'    {len(col_names)}, nullable_cols_arr_{ngpg__nhxj}.ctypes,\n')
        pdik__hrsf += f'    pyarrow_table_schema_{ngpg__nhxj},\n'
        pdik__hrsf += f'  )\n'
        pdik__hrsf += f'  check_and_propagate_cpp_exception()\n'
        fixm__lvrun = list(range(len(col_names)))
        gayrz__srsqu = {ror__xol: vykst__avf for vykst__avf, ror__xol in
            enumerate(fixm__lvrun)}
        wbctu__atqxo = [int(is_nullable(col_typs[vykst__avf])) for
            vykst__avf in type_usecol_offset]
        xdfz__qmvb = not type_usecol_offset
        ovgxe__agme = TableType(tuple(col_typs))
        if xdfz__qmvb:
            ovgxe__agme = types.none
        vjz__araob = 'None'
        if index_column_name is not None:
            hnk__jkp = len(type_usecol_offset) + 1 if not xdfz__qmvb else 0
            vjz__araob = (
                f'info_to_array(info_from_table(out_table, {hnk__jkp}), index_col_typ)'
                )
        pdik__hrsf += f'  index_var = {vjz__araob}\n'
        lzevq__srixb = None
        if not xdfz__qmvb:
            lzevq__srixb = []
            zwa__xnv = 0
            for vykst__avf, qklzn__dmrr in enumerate(fixm__lvrun):
                if zwa__xnv < len(type_usecol_offset
                    ) and vykst__avf == type_usecol_offset[zwa__xnv]:
                    lzevq__srixb.append(gayrz__srsqu[qklzn__dmrr])
                    zwa__xnv += 1
                else:
                    lzevq__srixb.append(-1)
            lzevq__srixb = np.array(lzevq__srixb, dtype=np.int64)
        if xdfz__qmvb:
            pdik__hrsf += '  table_var = None\n'
        else:
            pdik__hrsf += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{ngpg__nhxj}, py_table_type_{ngpg__nhxj})
"""
        pdik__hrsf += f'  delete_table(out_table)\n'
        pdik__hrsf += f'  ev.finalize()\n'
    elif db_type == 'snowflake':
        pdik__hrsf += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        wbctu__atqxo = [int(is_nullable(col_typs[vykst__avf])) for
            vykst__avf in type_usecol_offset]
        if index_column_name:
            wbctu__atqxo.append(int(is_nullable(index_column_type)))
        pdik__hrsf += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(wbctu__atqxo)}, np.array({wbctu__atqxo}, dtype=np.int32).ctypes)
"""
        pdik__hrsf += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            pdik__hrsf += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            pdik__hrsf += '  index_var = None\n'
        if type_usecol_offset:
            kpef__wum = []
            zwa__xnv = 0
            for vykst__avf in range(len(col_names)):
                if zwa__xnv < len(type_usecol_offset
                    ) and vykst__avf == type_usecol_offset[zwa__xnv]:
                    kpef__wum.append(zwa__xnv)
                    zwa__xnv += 1
                else:
                    kpef__wum.append(-1)
            lzevq__srixb = np.array(kpef__wum, dtype=np.int64)
            pdik__hrsf += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{ngpg__nhxj}, py_table_type_{ngpg__nhxj})
"""
        else:
            pdik__hrsf += '  table_var = None\n'
        pdik__hrsf += '  delete_table(out_table)\n'
        pdik__hrsf += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            pdik__hrsf += f"""  type_usecols_offsets_arr_{ngpg__nhxj}_2 = type_usecols_offsets_arr_{ngpg__nhxj}
"""
            etag__owhc = np.array(type_usecol_offset, dtype=np.int64)
        pdik__hrsf += '  df_typeref_2 = df_typeref\n'
        pdik__hrsf += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            pdik__hrsf += '  pymysql_check()\n'
        elif db_type == 'oracle':
            pdik__hrsf += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            pdik__hrsf += '  psycopg2_check()\n'
        if parallel:
            pdik__hrsf += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                pdik__hrsf += f'  nb_row = {limit}\n'
            else:
                pdik__hrsf += '  with objmode(nb_row="int64"):\n'
                pdik__hrsf += f'     if rank == {MPI_ROOT}:\n'
                pdik__hrsf += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                pdik__hrsf += '         frame = pd.read_sql(sql_cons, conn)\n'
                pdik__hrsf += '         nb_row = frame.iat[0,0]\n'
                pdik__hrsf += '     else:\n'
                pdik__hrsf += '         nb_row = 0\n'
                pdik__hrsf += '  nb_row = bcast_scalar(nb_row)\n'
            pdik__hrsf += f"""  with objmode(table_var=py_table_type_{ngpg__nhxj}, index_var=index_col_typ):
"""
            pdik__hrsf += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                pdik__hrsf += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                pdik__hrsf += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            pdik__hrsf += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            pdik__hrsf += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            pdik__hrsf += f"""  with objmode(table_var=py_table_type_{ngpg__nhxj}, index_var=index_col_typ):
"""
            pdik__hrsf += '    df_ret = pd.read_sql(sql_request, conn)\n'
            pdik__hrsf += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            pdik__hrsf += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            pdik__hrsf += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            pdik__hrsf += '    index_var = None\n'
        if type_usecol_offset:
            pdik__hrsf += f'    arrs = []\n'
            pdik__hrsf += f'    for i in range(df_ret.shape[1]):\n'
            pdik__hrsf += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            pdik__hrsf += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{ngpg__nhxj}_2, {len(col_names)})
"""
        else:
            pdik__hrsf += '    table_var = None\n'
    pdik__hrsf += '  return (table_var, index_var)\n'
    tzhff__qjsqa = globals()
    tzhff__qjsqa.update({'bodo': bodo, f'py_table_type_{ngpg__nhxj}':
        ovgxe__agme, 'index_col_typ': index_column_type, '_pq_reader_py':
        qvokp__qjpz})
    if db_type in ('iceberg', 'snowflake'):
        tzhff__qjsqa.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{ngpg__nhxj}': lzevq__srixb})
    if db_type == 'iceberg':
        tzhff__qjsqa.update({f'selected_cols_arr_{ngpg__nhxj}': np.array(
            fixm__lvrun, np.int32), f'nullable_cols_arr_{ngpg__nhxj}': np.
            array(wbctu__atqxo, np.int32), f'py_table_type_{ngpg__nhxj}':
            ovgxe__agme, f'pyarrow_table_schema_{ngpg__nhxj}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read})
    elif db_type == 'snowflake':
        tzhff__qjsqa.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        tzhff__qjsqa.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(mbgar__aczv), bodo.RangeIndexType(None
            ), tuple(naa__tcyat)), 'Table': Table,
            f'type_usecols_offsets_arr_{ngpg__nhxj}': etag__owhc})
    feg__imaa = {}
    exec(pdik__hrsf, tzhff__qjsqa, feg__imaa)
    cgh__gqkvw = feg__imaa['sql_reader_py']
    vjfl__djlzm = numba.njit(cgh__gqkvw)
    compiled_funcs.append(vjfl__djlzm)
    return vjfl__djlzm


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
parquet_predicate_type = ParquetPredicateType()
pyarrow_table_schema_type = PyArrowTableSchemaType()
_iceberg_read = types.ExternalFunction('iceberg_pq_read', table_type(types.
    voidptr, types.voidptr, types.voidptr, types.boolean,
    parquet_predicate_type, parquet_predicate_type, types.voidptr, types.
    int32, types.voidptr, pyarrow_table_schema_type))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
ll.add_symbol('iceberg_pq_read', arrow_cpp.iceberg_pq_read)
