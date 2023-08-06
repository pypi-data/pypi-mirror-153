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
    hdzrv__tybp = urlparse(con_str)
    db_type = hdzrv__tybp.scheme
    kxj__apmf = hdzrv__tybp.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', kxj__apmf
    if db_type == 'mysql+pymysql':
        return 'mysql', kxj__apmf
    return db_type, kxj__apmf


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    zzdgn__pst = sql_node.out_vars[0].name
    tcefp__zje = sql_node.out_vars[1].name
    if zzdgn__pst not in lives and tcefp__zje not in lives:
        return None
    elif zzdgn__pst not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif tcefp__zje not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        ojyr__atzud = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        paxkr__vjkm = []
        smwz__ykz = []
        for pkfz__rydc in sql_node.type_usecol_offset:
            lumqd__ibfwe = sql_node.df_colnames[pkfz__rydc]
            paxkr__vjkm.append(lumqd__ibfwe)
            if isinstance(sql_node.out_types[pkfz__rydc], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                smwz__ykz.append(lumqd__ibfwe)
        if sql_node.index_column_name:
            paxkr__vjkm.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                smwz__ykz.append(sql_node.index_column_name)
        rmecc__mmf = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', ojyr__atzud,
            rmecc__mmf, paxkr__vjkm)
        if smwz__ykz:
            eep__qfzbg = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', eep__qfzbg,
                rmecc__mmf, smwz__ykz)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        plydh__pkzq = set(sql_node.unsupported_columns)
        pkpfh__wmsq = set(sql_node.type_usecol_offset)
        dhlcy__uhmb = pkpfh__wmsq & plydh__pkzq
        if dhlcy__uhmb:
            qsx__ihrsj = sorted(dhlcy__uhmb)
            etarf__mxwj = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            cthf__nre = 0
            for kmr__rgila in qsx__ihrsj:
                while sql_node.unsupported_columns[cthf__nre] != kmr__rgila:
                    cthf__nre += 1
                etarf__mxwj.append(
                    f"Column '{sql_node.original_df_colnames[kmr__rgila]}' with unsupported arrow type {sql_node.unsupported_arrow_types[cthf__nre]}"
                    )
                cthf__nre += 1
            xzy__vtjm = '\n'.join(etarf__mxwj)
            raise BodoError(xzy__vtjm, loc=sql_node.loc)
    voo__hoen, xvdp__adqm = bodo.ir.connector.generate_filter_map(sql_node.
        filters)
    zttj__rjh = ', '.join(voo__hoen.values())
    wfog__vhf = (
        f'def sql_impl(sql_request, conn, database_schema, {zttj__rjh}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        fmuup__hrwj = []
        for zrkju__drfoj in sql_node.filters:
            jcv__jzdun = [' '.join(['(', chvti__rqr[0], chvti__rqr[1], '{' +
                voo__hoen[chvti__rqr[2].name] + '}' if isinstance(
                chvti__rqr[2], ir.Var) else chvti__rqr[2], ')']) for
                chvti__rqr in zrkju__drfoj]
            fmuup__hrwj.append(' ( ' + ' AND '.join(jcv__jzdun) + ' ) ')
        nqu__jkf = ' WHERE ' + ' OR '.join(fmuup__hrwj)
        for pkfz__rydc, fje__yzr in enumerate(voo__hoen.values()):
            wfog__vhf += f'    {fje__yzr} = get_sql_literal({fje__yzr})\n'
        wfog__vhf += f'    sql_request = f"{{sql_request}} {nqu__jkf}"\n'
    idqia__jgvp = ''
    if sql_node.db_type == 'iceberg':
        idqia__jgvp = zttj__rjh
    wfog__vhf += f"""    (table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {idqia__jgvp})
"""
    doyd__isas = {}
    exec(wfog__vhf, {}, doyd__isas)
    rjtf__eaomg = doyd__isas['sql_impl']
    ibap__osvr = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, typemap, sql_node.filters, sql_node.
        pyarrow_table_schema)
    mqs__rnbr = types.none if sql_node.database_schema is None else string_type
    ttgs__zlg = compile_to_numba_ir(rjtf__eaomg, {'_sql_reader_py':
        ibap__osvr, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type, mqs__rnbr) +
        tuple(typemap[nti__tntt.name] for nti__tntt in xvdp__adqm), typemap
        =typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        qcw__zhmpx = [sql_node.df_colnames[pkfz__rydc] for pkfz__rydc in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            qcw__zhmpx.append(sql_node.index_column_name)
        coxwn__fsxoo = escape_column_names(qcw__zhmpx, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            izpdf__nnqg = ('SELECT ' + coxwn__fsxoo + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            izpdf__nnqg = ('SELECT ' + coxwn__fsxoo + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        izpdf__nnqg = sql_node.sql_request
    replace_arg_nodes(ttgs__zlg, [ir.Const(izpdf__nnqg, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + xvdp__adqm)
    rvggs__kqo = ttgs__zlg.body[:-3]
    rvggs__kqo[-2].target = sql_node.out_vars[0]
    rvggs__kqo[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        rvggs__kqo.pop(-1)
    elif not sql_node.type_usecol_offset:
        rvggs__kqo.pop(-2)
    return rvggs__kqo


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        qcw__zhmpx = [(bjn__napg.upper() if bjn__napg in converted_colnames
             else bjn__napg) for bjn__napg in col_names]
        coxwn__fsxoo = ', '.join([f'"{bjn__napg}"' for bjn__napg in qcw__zhmpx]
            )
    elif db_type == 'mysql':
        coxwn__fsxoo = ', '.join([f'`{bjn__napg}`' for bjn__napg in col_names])
    else:
        coxwn__fsxoo = ', '.join([f'"{bjn__napg}"' for bjn__napg in col_names])
    return coxwn__fsxoo


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    rpgrr__mogo = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rpgrr__mogo,
        'Filter pushdown')
    if rpgrr__mogo == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(rpgrr__mogo, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif rpgrr__mogo == bodo.pd_timestamp_type:

        def impl(filter_value):
            lvotv__frga = filter_value.nanosecond
            zdwk__mwutz = ''
            if lvotv__frga < 10:
                zdwk__mwutz = '00'
            elif lvotv__frga < 100:
                zdwk__mwutz = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{zdwk__mwutz}{lvotv__frga}'"
                )
        return impl
    elif rpgrr__mogo == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {rpgrr__mogo} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    kiy__owrw = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    rpgrr__mogo = types.unliteral(filter_value)
    if isinstance(rpgrr__mogo, types.List) and (isinstance(rpgrr__mogo.
        dtype, scalar_isinstance) or rpgrr__mogo.dtype in kiy__owrw):

        def impl(filter_value):
            ymhve__pvj = ', '.join([_get_snowflake_sql_literal_scalar(
                bjn__napg) for bjn__napg in filter_value])
            return f'({ymhve__pvj})'
        return impl
    elif isinstance(rpgrr__mogo, scalar_isinstance
        ) or rpgrr__mogo in kiy__owrw:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {rpgrr__mogo} used in filter pushdown.'
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
    except ImportError as sjkg__yiu:
        icamz__mebqr = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(icamz__mebqr)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as sjkg__yiu:
        icamz__mebqr = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(icamz__mebqr)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as sjkg__yiu:
        icamz__mebqr = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(icamz__mebqr)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as sjkg__yiu:
        icamz__mebqr = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(icamz__mebqr)


def req_limit(sql_request):
    import re
    znsa__uam = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    ldcb__gttib = znsa__uam.search(sql_request)
    if ldcb__gttib:
        return int(ldcb__gttib.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, typemap, filters, pyarrow_table_schema):
    kghy__jjh = next_label()
    qcw__zhmpx = [col_names[pkfz__rydc] for pkfz__rydc in type_usecol_offset]
    wqpa__xfff = [col_typs[pkfz__rydc] for pkfz__rydc in type_usecol_offset]
    if index_column_name:
        qcw__zhmpx.append(index_column_name)
        wqpa__xfff.append(index_column_type)
    vdp__mcs = None
    mhop__txgv = None
    ewj__xood = types.none
    ricyp__drqb = None
    if type_usecol_offset:
        ewj__xood = TableType(tuple(col_typs))
    idqia__jgvp = ''
    voo__hoen = {}
    xvdp__adqm = []
    if filters and db_type == 'iceberg':
        voo__hoen, xvdp__adqm = bodo.ir.connector.generate_filter_map(filters)
        idqia__jgvp = ', '.join(voo__hoen.values())
    wfog__vhf = (
        f'def sql_reader_py(sql_request, conn, database_schema, {idqia__jgvp}):\n'
        )
    if db_type == 'iceberg':
        mwbio__ity, ymf__cccrt = bodo.ir.connector.generate_arrow_filters(
            filters, voo__hoen, xvdp__adqm, col_names, col_names, col_typs,
            typemap, 'iceberg')
        mvtud__gofg = ',' if idqia__jgvp else ''
        wfog__vhf += (
            f"  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})\n")
        wfog__vhf += f"""  dnf_filters, expr_filters = get_filters_pyobject("{mwbio__ity}", "{ymf__cccrt}", ({idqia__jgvp}{mvtud__gofg}))
"""
        wfog__vhf += f'  out_table = iceberg_read(\n'
        wfog__vhf += (
            f'    unicode_to_utf8(conn), unicode_to_utf8(database_schema),\n')
        wfog__vhf += (
            f'    unicode_to_utf8(sql_request), {parallel}, dnf_filters,\n')
        wfog__vhf += (
            f'    expr_filters, selected_cols_arr_{kghy__jjh}.ctypes,\n')
        wfog__vhf += (
            f'    {len(col_names)}, nullable_cols_arr_{kghy__jjh}.ctypes,\n')
        wfog__vhf += f'    pyarrow_table_schema_{kghy__jjh},\n'
        wfog__vhf += f'  )\n'
        wfog__vhf += f'  check_and_propagate_cpp_exception()\n'
        uzogn__xiht = list(range(len(col_names)))
        igwae__gassn = {kwb__ijabw: pkfz__rydc for pkfz__rydc, kwb__ijabw in
            enumerate(uzogn__xiht)}
        lcso__snudc = [int(is_nullable(col_typs[pkfz__rydc])) for
            pkfz__rydc in type_usecol_offset]
        jwj__hotzi = not type_usecol_offset
        ewj__xood = TableType(tuple(col_typs))
        if jwj__hotzi:
            ewj__xood = types.none
        tcefp__zje = 'None'
        if index_column_name is not None:
            cpts__esm = len(type_usecol_offset) + 1 if not jwj__hotzi else 0
            tcefp__zje = (
                f'info_to_array(info_from_table(out_table, {cpts__esm}), index_col_typ)'
                )
        wfog__vhf += f'  index_var = {tcefp__zje}\n'
        vdp__mcs = None
        if not jwj__hotzi:
            vdp__mcs = []
            zcav__rnpvd = 0
            for pkfz__rydc, kmr__rgila in enumerate(uzogn__xiht):
                if zcav__rnpvd < len(type_usecol_offset
                    ) and pkfz__rydc == type_usecol_offset[zcav__rnpvd]:
                    vdp__mcs.append(igwae__gassn[kmr__rgila])
                    zcav__rnpvd += 1
                else:
                    vdp__mcs.append(-1)
            vdp__mcs = np.array(vdp__mcs, dtype=np.int64)
        if jwj__hotzi:
            wfog__vhf += '  table_var = None\n'
        else:
            wfog__vhf += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{kghy__jjh}, py_table_type_{kghy__jjh})
"""
        wfog__vhf += f'  delete_table(out_table)\n'
        wfog__vhf += f'  ev.finalize()\n'
    elif db_type == 'snowflake':
        wfog__vhf += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        lcso__snudc = [int(is_nullable(col_typs[pkfz__rydc])) for
            pkfz__rydc in type_usecol_offset]
        if index_column_name:
            lcso__snudc.append(int(is_nullable(index_column_type)))
        wfog__vhf += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(lcso__snudc)}, np.array({lcso__snudc}, dtype=np.int32).ctypes)
"""
        wfog__vhf += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            wfog__vhf += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            wfog__vhf += '  index_var = None\n'
        if type_usecol_offset:
            cthf__nre = []
            zcav__rnpvd = 0
            for pkfz__rydc in range(len(col_names)):
                if zcav__rnpvd < len(type_usecol_offset
                    ) and pkfz__rydc == type_usecol_offset[zcav__rnpvd]:
                    cthf__nre.append(zcav__rnpvd)
                    zcav__rnpvd += 1
                else:
                    cthf__nre.append(-1)
            vdp__mcs = np.array(cthf__nre, dtype=np.int64)
            wfog__vhf += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{kghy__jjh}, py_table_type_{kghy__jjh})
"""
        else:
            wfog__vhf += '  table_var = None\n'
        wfog__vhf += '  delete_table(out_table)\n'
        wfog__vhf += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            wfog__vhf += f"""  type_usecols_offsets_arr_{kghy__jjh}_2 = type_usecols_offsets_arr_{kghy__jjh}
"""
            mhop__txgv = np.array(type_usecol_offset, dtype=np.int64)
        wfog__vhf += '  df_typeref_2 = df_typeref\n'
        wfog__vhf += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            wfog__vhf += '  pymysql_check()\n'
        elif db_type == 'oracle':
            wfog__vhf += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            wfog__vhf += '  psycopg2_check()\n'
        if parallel:
            wfog__vhf += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                wfog__vhf += f'  nb_row = {limit}\n'
            else:
                wfog__vhf += '  with objmode(nb_row="int64"):\n'
                wfog__vhf += f'     if rank == {MPI_ROOT}:\n'
                wfog__vhf += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                wfog__vhf += '         frame = pd.read_sql(sql_cons, conn)\n'
                wfog__vhf += '         nb_row = frame.iat[0,0]\n'
                wfog__vhf += '     else:\n'
                wfog__vhf += '         nb_row = 0\n'
                wfog__vhf += '  nb_row = bcast_scalar(nb_row)\n'
            wfog__vhf += f"""  with objmode(table_var=py_table_type_{kghy__jjh}, index_var=index_col_typ):
"""
            wfog__vhf += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                wfog__vhf += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                wfog__vhf += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            wfog__vhf += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            wfog__vhf += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            wfog__vhf += f"""  with objmode(table_var=py_table_type_{kghy__jjh}, index_var=index_col_typ):
"""
            wfog__vhf += '    df_ret = pd.read_sql(sql_request, conn)\n'
            wfog__vhf += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            wfog__vhf += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            wfog__vhf += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            wfog__vhf += '    index_var = None\n'
        if type_usecol_offset:
            wfog__vhf += f'    arrs = []\n'
            wfog__vhf += f'    for i in range(df_ret.shape[1]):\n'
            wfog__vhf += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            wfog__vhf += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{kghy__jjh}_2, {len(col_names)})
"""
        else:
            wfog__vhf += '    table_var = None\n'
    wfog__vhf += '  return (table_var, index_var)\n'
    dtp__bznoz = globals()
    dtp__bznoz.update({'bodo': bodo, f'py_table_type_{kghy__jjh}':
        ewj__xood, 'index_col_typ': index_column_type, '_pq_reader_py':
        ricyp__drqb})
    if db_type in ('iceberg', 'snowflake'):
        dtp__bznoz.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{kghy__jjh}': vdp__mcs})
    if db_type == 'iceberg':
        dtp__bznoz.update({f'selected_cols_arr_{kghy__jjh}': np.array(
            uzogn__xiht, np.int32), f'nullable_cols_arr_{kghy__jjh}': np.
            array(lcso__snudc, np.int32), f'py_table_type_{kghy__jjh}':
            ewj__xood, f'pyarrow_table_schema_{kghy__jjh}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read})
    elif db_type == 'snowflake':
        dtp__bznoz.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        dtp__bznoz.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(wqpa__xfff), bodo.RangeIndexType(None),
            tuple(qcw__zhmpx)), 'Table': Table,
            f'type_usecols_offsets_arr_{kghy__jjh}': mhop__txgv})
    doyd__isas = {}
    exec(wfog__vhf, dtp__bznoz, doyd__isas)
    ibap__osvr = doyd__isas['sql_reader_py']
    rsajh__vsp = numba.njit(ibap__osvr)
    compiled_funcs.append(rsajh__vsp)
    return rsajh__vsp


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
