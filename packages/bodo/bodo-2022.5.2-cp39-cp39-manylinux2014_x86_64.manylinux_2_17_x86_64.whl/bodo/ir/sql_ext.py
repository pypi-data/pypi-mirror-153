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
    ntsk__umrtw = urlparse(con_str)
    db_type = ntsk__umrtw.scheme
    bxos__yegmm = ntsk__umrtw.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', bxos__yegmm
    if db_type == 'mysql+pymysql':
        return 'mysql', bxos__yegmm
    return db_type, bxos__yegmm


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    efkkb__lmv = sql_node.out_vars[0].name
    bzk__qaz = sql_node.out_vars[1].name
    if efkkb__lmv not in lives and bzk__qaz not in lives:
        return None
    elif efkkb__lmv not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif bzk__qaz not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        cbili__uha = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        kwdyy__lxwz = []
        kun__bfl = []
        for xwv__agv in sql_node.type_usecol_offset:
            qfir__sdk = sql_node.df_colnames[xwv__agv]
            kwdyy__lxwz.append(qfir__sdk)
            if isinstance(sql_node.out_types[xwv__agv], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                kun__bfl.append(qfir__sdk)
        if sql_node.index_column_name:
            kwdyy__lxwz.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                kun__bfl.append(sql_node.index_column_name)
        fhxj__jjz = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', cbili__uha,
            fhxj__jjz, kwdyy__lxwz)
        if kun__bfl:
            fdyxz__cdae = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                fdyxz__cdae, fhxj__jjz, kun__bfl)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        xrk__fov = set(sql_node.unsupported_columns)
        llina__gok = set(sql_node.type_usecol_offset)
        acamd__yxyw = llina__gok & xrk__fov
        if acamd__yxyw:
            tpsfl__jtw = sorted(acamd__yxyw)
            zly__nfgns = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            spn__zlm = 0
            for cfvm__hlc in tpsfl__jtw:
                while sql_node.unsupported_columns[spn__zlm] != cfvm__hlc:
                    spn__zlm += 1
                zly__nfgns.append(
                    f"Column '{sql_node.original_df_colnames[cfvm__hlc]}' with unsupported arrow type {sql_node.unsupported_arrow_types[spn__zlm]}"
                    )
                spn__zlm += 1
            evs__wnhn = '\n'.join(zly__nfgns)
            raise BodoError(evs__wnhn, loc=sql_node.loc)
    rvpr__epf, kfnw__kxinx = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    ewk__xhfam = ', '.join(rvpr__epf.values())
    yjdkx__vjyri = (
        f'def sql_impl(sql_request, conn, database_schema, {ewk__xhfam}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        freku__mjpu = []
        for ecjlb__juwnt in sql_node.filters:
            hslv__lqte = [' '.join(['(', kmnif__uvn[0], kmnif__uvn[1], '{' +
                rvpr__epf[kmnif__uvn[2].name] + '}' if isinstance(
                kmnif__uvn[2], ir.Var) else kmnif__uvn[2], ')']) for
                kmnif__uvn in ecjlb__juwnt]
            freku__mjpu.append(' ( ' + ' AND '.join(hslv__lqte) + ' ) ')
        hkyl__xotj = ' WHERE ' + ' OR '.join(freku__mjpu)
        for xwv__agv, mfiqm__ksuk in enumerate(rvpr__epf.values()):
            yjdkx__vjyri += (
                f'    {mfiqm__ksuk} = get_sql_literal({mfiqm__ksuk})\n')
        yjdkx__vjyri += f'    sql_request = f"{{sql_request}} {hkyl__xotj}"\n'
    zkl__gxbgk = ''
    if sql_node.db_type == 'iceberg':
        zkl__gxbgk = ewk__xhfam
    yjdkx__vjyri += f"""    (table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {zkl__gxbgk})
"""
    bem__ppmhw = {}
    exec(yjdkx__vjyri, {}, bem__ppmhw)
    fenk__jlgqh = bem__ppmhw['sql_impl']
    rospc__kzc = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, typemap, sql_node.filters, sql_node.
        pyarrow_table_schema)
    cxtw__vyyo = (types.none if sql_node.database_schema is None else
        string_type)
    talk__hnphs = compile_to_numba_ir(fenk__jlgqh, {'_sql_reader_py':
        rospc__kzc, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type, cxtw__vyyo
        ) + tuple(typemap[zzutk__anb.name] for zzutk__anb in kfnw__kxinx),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        upi__hae = [sql_node.df_colnames[xwv__agv] for xwv__agv in sql_node
            .type_usecol_offset]
        if sql_node.index_column_name:
            upi__hae.append(sql_node.index_column_name)
        ydxcn__gqq = escape_column_names(upi__hae, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            scu__fgekd = ('SELECT ' + ydxcn__gqq + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            scu__fgekd = ('SELECT ' + ydxcn__gqq + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        scu__fgekd = sql_node.sql_request
    replace_arg_nodes(talk__hnphs, [ir.Const(scu__fgekd, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + kfnw__kxinx)
    kvzc__foct = talk__hnphs.body[:-3]
    kvzc__foct[-2].target = sql_node.out_vars[0]
    kvzc__foct[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        kvzc__foct.pop(-1)
    elif not sql_node.type_usecol_offset:
        kvzc__foct.pop(-2)
    return kvzc__foct


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        upi__hae = [(wroj__gky.upper() if wroj__gky in converted_colnames else
            wroj__gky) for wroj__gky in col_names]
        ydxcn__gqq = ', '.join([f'"{wroj__gky}"' for wroj__gky in upi__hae])
    elif db_type == 'mysql':
        ydxcn__gqq = ', '.join([f'`{wroj__gky}`' for wroj__gky in col_names])
    else:
        ydxcn__gqq = ', '.join([f'"{wroj__gky}"' for wroj__gky in col_names])
    return ydxcn__gqq


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    nqrkr__qot = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(nqrkr__qot,
        'Filter pushdown')
    if nqrkr__qot == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(nqrkr__qot, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif nqrkr__qot == bodo.pd_timestamp_type:

        def impl(filter_value):
            iliee__kzo = filter_value.nanosecond
            sirh__zagho = ''
            if iliee__kzo < 10:
                sirh__zagho = '00'
            elif iliee__kzo < 100:
                sirh__zagho = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{sirh__zagho}{iliee__kzo}'"
                )
        return impl
    elif nqrkr__qot == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {nqrkr__qot} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    ssaxp__zpbf = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    nqrkr__qot = types.unliteral(filter_value)
    if isinstance(nqrkr__qot, types.List) and (isinstance(nqrkr__qot.dtype,
        scalar_isinstance) or nqrkr__qot.dtype in ssaxp__zpbf):

        def impl(filter_value):
            ebzf__virfz = ', '.join([_get_snowflake_sql_literal_scalar(
                wroj__gky) for wroj__gky in filter_value])
            return f'({ebzf__virfz})'
        return impl
    elif isinstance(nqrkr__qot, scalar_isinstance
        ) or nqrkr__qot in ssaxp__zpbf:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {nqrkr__qot} used in filter pushdown.'
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
    except ImportError as jigwg__atk:
        cuqxn__orii = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(cuqxn__orii)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as jigwg__atk:
        cuqxn__orii = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(cuqxn__orii)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as jigwg__atk:
        cuqxn__orii = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(cuqxn__orii)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as jigwg__atk:
        cuqxn__orii = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(cuqxn__orii)


def req_limit(sql_request):
    import re
    gcfs__amq = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    hzkbf__lktd = gcfs__amq.search(sql_request)
    if hzkbf__lktd:
        return int(hzkbf__lktd.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, typemap, filters, pyarrow_table_schema):
    txk__eyh = next_label()
    upi__hae = [col_names[xwv__agv] for xwv__agv in type_usecol_offset]
    bqgfv__ptp = [col_typs[xwv__agv] for xwv__agv in type_usecol_offset]
    if index_column_name:
        upi__hae.append(index_column_name)
        bqgfv__ptp.append(index_column_type)
    yfiyb__ytl = None
    wczz__cqwfw = None
    hkn__tddba = types.none
    rvz__atnw = None
    if type_usecol_offset:
        hkn__tddba = TableType(tuple(col_typs))
    zkl__gxbgk = ''
    rvpr__epf = {}
    kfnw__kxinx = []
    if filters and db_type == 'iceberg':
        rvpr__epf, kfnw__kxinx = bodo.ir.connector.generate_filter_map(filters)
        zkl__gxbgk = ', '.join(rvpr__epf.values())
    yjdkx__vjyri = (
        f'def sql_reader_py(sql_request, conn, database_schema, {zkl__gxbgk}):\n'
        )
    if db_type == 'iceberg':
        mmnvo__spe, exyb__jviio = bodo.ir.connector.generate_arrow_filters(
            filters, rvpr__epf, kfnw__kxinx, col_names, col_names, col_typs,
            typemap, 'iceberg')
        jaob__pxvne = ',' if zkl__gxbgk else ''
        yjdkx__vjyri += (
            f"  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})\n")
        yjdkx__vjyri += f"""  dnf_filters, expr_filters = get_filters_pyobject("{mmnvo__spe}", "{exyb__jviio}", ({zkl__gxbgk}{jaob__pxvne}))
"""
        yjdkx__vjyri += f'  out_table = iceberg_read(\n'
        yjdkx__vjyri += (
            f'    unicode_to_utf8(conn), unicode_to_utf8(database_schema),\n')
        yjdkx__vjyri += (
            f'    unicode_to_utf8(sql_request), {parallel}, dnf_filters,\n')
        yjdkx__vjyri += (
            f'    expr_filters, selected_cols_arr_{txk__eyh}.ctypes,\n')
        yjdkx__vjyri += (
            f'    {len(col_names)}, nullable_cols_arr_{txk__eyh}.ctypes,\n')
        yjdkx__vjyri += f'    pyarrow_table_schema_{txk__eyh},\n'
        yjdkx__vjyri += f'  )\n'
        yjdkx__vjyri += f'  check_and_propagate_cpp_exception()\n'
        tle__knwb = list(range(len(col_names)))
        nzhfn__uwxu = {uibcu__twbz: xwv__agv for xwv__agv, uibcu__twbz in
            enumerate(tle__knwb)}
        wcifj__lput = [int(is_nullable(col_typs[xwv__agv])) for xwv__agv in
            type_usecol_offset]
        mylaj__ojjjd = not type_usecol_offset
        hkn__tddba = TableType(tuple(col_typs))
        if mylaj__ojjjd:
            hkn__tddba = types.none
        bzk__qaz = 'None'
        if index_column_name is not None:
            wifs__iarmh = len(type_usecol_offset
                ) + 1 if not mylaj__ojjjd else 0
            bzk__qaz = (
                f'info_to_array(info_from_table(out_table, {wifs__iarmh}), index_col_typ)'
                )
        yjdkx__vjyri += f'  index_var = {bzk__qaz}\n'
        yfiyb__ytl = None
        if not mylaj__ojjjd:
            yfiyb__ytl = []
            ksz__meys = 0
            for xwv__agv, cfvm__hlc in enumerate(tle__knwb):
                if ksz__meys < len(type_usecol_offset
                    ) and xwv__agv == type_usecol_offset[ksz__meys]:
                    yfiyb__ytl.append(nzhfn__uwxu[cfvm__hlc])
                    ksz__meys += 1
                else:
                    yfiyb__ytl.append(-1)
            yfiyb__ytl = np.array(yfiyb__ytl, dtype=np.int64)
        if mylaj__ojjjd:
            yjdkx__vjyri += '  table_var = None\n'
        else:
            yjdkx__vjyri += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{txk__eyh}, py_table_type_{txk__eyh})
"""
        yjdkx__vjyri += f'  delete_table(out_table)\n'
        yjdkx__vjyri += f'  ev.finalize()\n'
    elif db_type == 'snowflake':
        yjdkx__vjyri += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        wcifj__lput = [int(is_nullable(col_typs[xwv__agv])) for xwv__agv in
            type_usecol_offset]
        if index_column_name:
            wcifj__lput.append(int(is_nullable(index_column_type)))
        yjdkx__vjyri += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(wcifj__lput)}, np.array({wcifj__lput}, dtype=np.int32).ctypes)
"""
        yjdkx__vjyri += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            yjdkx__vjyri += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            yjdkx__vjyri += '  index_var = None\n'
        if type_usecol_offset:
            spn__zlm = []
            ksz__meys = 0
            for xwv__agv in range(len(col_names)):
                if ksz__meys < len(type_usecol_offset
                    ) and xwv__agv == type_usecol_offset[ksz__meys]:
                    spn__zlm.append(ksz__meys)
                    ksz__meys += 1
                else:
                    spn__zlm.append(-1)
            yfiyb__ytl = np.array(spn__zlm, dtype=np.int64)
            yjdkx__vjyri += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{txk__eyh}, py_table_type_{txk__eyh})
"""
        else:
            yjdkx__vjyri += '  table_var = None\n'
        yjdkx__vjyri += '  delete_table(out_table)\n'
        yjdkx__vjyri += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            yjdkx__vjyri += f"""  type_usecols_offsets_arr_{txk__eyh}_2 = type_usecols_offsets_arr_{txk__eyh}
"""
            wczz__cqwfw = np.array(type_usecol_offset, dtype=np.int64)
        yjdkx__vjyri += '  df_typeref_2 = df_typeref\n'
        yjdkx__vjyri += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            yjdkx__vjyri += '  pymysql_check()\n'
        elif db_type == 'oracle':
            yjdkx__vjyri += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            yjdkx__vjyri += '  psycopg2_check()\n'
        if parallel:
            yjdkx__vjyri += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                yjdkx__vjyri += f'  nb_row = {limit}\n'
            else:
                yjdkx__vjyri += '  with objmode(nb_row="int64"):\n'
                yjdkx__vjyri += f'     if rank == {MPI_ROOT}:\n'
                yjdkx__vjyri += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                yjdkx__vjyri += (
                    '         frame = pd.read_sql(sql_cons, conn)\n')
                yjdkx__vjyri += '         nb_row = frame.iat[0,0]\n'
                yjdkx__vjyri += '     else:\n'
                yjdkx__vjyri += '         nb_row = 0\n'
                yjdkx__vjyri += '  nb_row = bcast_scalar(nb_row)\n'
            yjdkx__vjyri += f"""  with objmode(table_var=py_table_type_{txk__eyh}, index_var=index_col_typ):
"""
            yjdkx__vjyri += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
            if db_type == 'oracle':
                yjdkx__vjyri += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                yjdkx__vjyri += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            yjdkx__vjyri += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            yjdkx__vjyri += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            yjdkx__vjyri += f"""  with objmode(table_var=py_table_type_{txk__eyh}, index_var=index_col_typ):
"""
            yjdkx__vjyri += '    df_ret = pd.read_sql(sql_request, conn)\n'
            yjdkx__vjyri += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            yjdkx__vjyri += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            yjdkx__vjyri += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            yjdkx__vjyri += '    index_var = None\n'
        if type_usecol_offset:
            yjdkx__vjyri += f'    arrs = []\n'
            yjdkx__vjyri += f'    for i in range(df_ret.shape[1]):\n'
            yjdkx__vjyri += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            yjdkx__vjyri += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{txk__eyh}_2, {len(col_names)})
"""
        else:
            yjdkx__vjyri += '    table_var = None\n'
    yjdkx__vjyri += '  return (table_var, index_var)\n'
    kaiio__iocv = globals()
    kaiio__iocv.update({'bodo': bodo, f'py_table_type_{txk__eyh}':
        hkn__tddba, 'index_col_typ': index_column_type, '_pq_reader_py':
        rvz__atnw})
    if db_type in ('iceberg', 'snowflake'):
        kaiio__iocv.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{txk__eyh}': yfiyb__ytl})
    if db_type == 'iceberg':
        kaiio__iocv.update({f'selected_cols_arr_{txk__eyh}': np.array(
            tle__knwb, np.int32), f'nullable_cols_arr_{txk__eyh}': np.array
            (wcifj__lput, np.int32), f'py_table_type_{txk__eyh}':
            hkn__tddba, f'pyarrow_table_schema_{txk__eyh}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read})
    elif db_type == 'snowflake':
        kaiio__iocv.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        kaiio__iocv.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(bqgfv__ptp), bodo.RangeIndexType(None),
            tuple(upi__hae)), 'Table': Table,
            f'type_usecols_offsets_arr_{txk__eyh}': wczz__cqwfw})
    bem__ppmhw = {}
    exec(yjdkx__vjyri, kaiio__iocv, bem__ppmhw)
    rospc__kzc = bem__ppmhw['sql_reader_py']
    abbj__ljddb = numba.njit(rospc__kzc)
    compiled_funcs.append(abbj__ljddb)
    return abbj__ljddb


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
