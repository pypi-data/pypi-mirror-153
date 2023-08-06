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
    efvr__trsis = urlparse(con_str)
    db_type = efvr__trsis.scheme
    gzr__qmux = efvr__trsis.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', gzr__qmux
    if db_type == 'mysql+pymysql':
        return 'mysql', gzr__qmux
    return db_type, gzr__qmux


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    zjc__vfr = sql_node.out_vars[0].name
    uvdas__ofo = sql_node.out_vars[1].name
    if zjc__vfr not in lives and uvdas__ofo not in lives:
        return None
    elif zjc__vfr not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif uvdas__ofo not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        dxf__xgxv = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        zwo__cqj = []
        licy__csqi = []
        for yjmsz__csfud in sql_node.type_usecol_offset:
            asu__fcjyk = sql_node.df_colnames[yjmsz__csfud]
            zwo__cqj.append(asu__fcjyk)
            if isinstance(sql_node.out_types[yjmsz__csfud], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                licy__csqi.append(asu__fcjyk)
        if sql_node.index_column_name:
            zwo__cqj.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                licy__csqi.append(sql_node.index_column_name)
        aizc__wqkf = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', dxf__xgxv,
            aizc__wqkf, zwo__cqj)
        if licy__csqi:
            zezjz__uivhn = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                zezjz__uivhn, aizc__wqkf, licy__csqi)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        eqb__bkiut = set(sql_node.unsupported_columns)
        unqg__yxx = set(sql_node.type_usecol_offset)
        cwqe__tqet = unqg__yxx & eqb__bkiut
        if cwqe__tqet:
            edjxx__zbu = sorted(cwqe__tqet)
            lwhvr__dzw = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            chxr__ugshn = 0
            for bss__jvhq in edjxx__zbu:
                while sql_node.unsupported_columns[chxr__ugshn] != bss__jvhq:
                    chxr__ugshn += 1
                lwhvr__dzw.append(
                    f"Column '{sql_node.original_df_colnames[bss__jvhq]}' with unsupported arrow type {sql_node.unsupported_arrow_types[chxr__ugshn]}"
                    )
                chxr__ugshn += 1
            pkbwb__heiy = '\n'.join(lwhvr__dzw)
            raise BodoError(pkbwb__heiy, loc=sql_node.loc)
    hcpkf__wmjxk, fqke__njs = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    osrz__aak = ', '.join(hcpkf__wmjxk.values())
    dry__icovl = (
        f'def sql_impl(sql_request, conn, database_schema, {osrz__aak}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        jsuqv__aaj = []
        for gkvqf__ziie in sql_node.filters:
            eujvh__yyb = [' '.join(['(', gkbri__vvgbx[0], gkbri__vvgbx[1], 
                '{' + hcpkf__wmjxk[gkbri__vvgbx[2].name] + '}' if
                isinstance(gkbri__vvgbx[2], ir.Var) else gkbri__vvgbx[2],
                ')']) for gkbri__vvgbx in gkvqf__ziie]
            jsuqv__aaj.append(' ( ' + ' AND '.join(eujvh__yyb) + ' ) ')
        derer__qkbtj = ' WHERE ' + ' OR '.join(jsuqv__aaj)
        for yjmsz__csfud, xtkag__rcs in enumerate(hcpkf__wmjxk.values()):
            dry__icovl += f'    {xtkag__rcs} = get_sql_literal({xtkag__rcs})\n'
        dry__icovl += f'    sql_request = f"{{sql_request}} {derer__qkbtj}"\n'
    gqz__vzg = ''
    if sql_node.db_type == 'iceberg':
        gqz__vzg = osrz__aak
    dry__icovl += f"""    (table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {gqz__vzg})
"""
    pjlra__bnl = {}
    exec(dry__icovl, {}, pjlra__bnl)
    mols__ipyh = pjlra__bnl['sql_impl']
    agl__pvuc = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, typemap, sql_node.filters, sql_node.
        pyarrow_table_schema)
    qomr__ssa = types.none if sql_node.database_schema is None else string_type
    pucq__ngb = compile_to_numba_ir(mols__ipyh, {'_sql_reader_py':
        agl__pvuc, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type, qomr__ssa) +
        tuple(typemap[aiy__nclx.name] for aiy__nclx in fqke__njs), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        ctnyn__kkvjb = [sql_node.df_colnames[yjmsz__csfud] for yjmsz__csfud in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            ctnyn__kkvjb.append(sql_node.index_column_name)
        fcndq__prnkl = escape_column_names(ctnyn__kkvjb, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            tqa__zuisw = ('SELECT ' + fcndq__prnkl + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            tqa__zuisw = ('SELECT ' + fcndq__prnkl + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        tqa__zuisw = sql_node.sql_request
    replace_arg_nodes(pucq__ngb, [ir.Const(tqa__zuisw, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + fqke__njs)
    nazz__rxv = pucq__ngb.body[:-3]
    nazz__rxv[-2].target = sql_node.out_vars[0]
    nazz__rxv[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        nazz__rxv.pop(-1)
    elif not sql_node.type_usecol_offset:
        nazz__rxv.pop(-2)
    return nazz__rxv


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        ctnyn__kkvjb = [(smkdd__jrd.upper() if smkdd__jrd in
            converted_colnames else smkdd__jrd) for smkdd__jrd in col_names]
        fcndq__prnkl = ', '.join([f'"{smkdd__jrd}"' for smkdd__jrd in
            ctnyn__kkvjb])
    elif db_type == 'mysql':
        fcndq__prnkl = ', '.join([f'`{smkdd__jrd}`' for smkdd__jrd in
            col_names])
    else:
        fcndq__prnkl = ', '.join([f'"{smkdd__jrd}"' for smkdd__jrd in
            col_names])
    return fcndq__prnkl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    uzxkm__rjb = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(uzxkm__rjb,
        'Filter pushdown')
    if uzxkm__rjb == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(uzxkm__rjb, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif uzxkm__rjb == bodo.pd_timestamp_type:

        def impl(filter_value):
            cdqk__znir = filter_value.nanosecond
            xlqp__cop = ''
            if cdqk__znir < 10:
                xlqp__cop = '00'
            elif cdqk__znir < 100:
                xlqp__cop = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{xlqp__cop}{cdqk__znir}'"
                )
        return impl
    elif uzxkm__rjb == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {uzxkm__rjb} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    hoafo__jng = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    uzxkm__rjb = types.unliteral(filter_value)
    if isinstance(uzxkm__rjb, types.List) and (isinstance(uzxkm__rjb.dtype,
        scalar_isinstance) or uzxkm__rjb.dtype in hoafo__jng):

        def impl(filter_value):
            vodg__cow = ', '.join([_get_snowflake_sql_literal_scalar(
                smkdd__jrd) for smkdd__jrd in filter_value])
            return f'({vodg__cow})'
        return impl
    elif isinstance(uzxkm__rjb, scalar_isinstance) or uzxkm__rjb in hoafo__jng:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {uzxkm__rjb} used in filter pushdown.'
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
    except ImportError as tdii__gzq:
        djw__annxa = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(djw__annxa)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as tdii__gzq:
        djw__annxa = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(djw__annxa)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as tdii__gzq:
        djw__annxa = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(djw__annxa)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as tdii__gzq:
        djw__annxa = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(djw__annxa)


def req_limit(sql_request):
    import re
    hyh__yvf = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    usin__xgcb = hyh__yvf.search(sql_request)
    if usin__xgcb:
        return int(usin__xgcb.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, typemap, filters, pyarrow_table_schema):
    jxhxk__ttj = next_label()
    ctnyn__kkvjb = [col_names[yjmsz__csfud] for yjmsz__csfud in
        type_usecol_offset]
    kkhkd__excz = [col_typs[yjmsz__csfud] for yjmsz__csfud in
        type_usecol_offset]
    if index_column_name:
        ctnyn__kkvjb.append(index_column_name)
        kkhkd__excz.append(index_column_type)
    wkvjp__jqppq = None
    zcbf__yss = None
    xege__ctl = types.none
    lfwe__hpiy = None
    if type_usecol_offset:
        xege__ctl = TableType(tuple(col_typs))
    gqz__vzg = ''
    hcpkf__wmjxk = {}
    fqke__njs = []
    if filters and db_type == 'iceberg':
        hcpkf__wmjxk, fqke__njs = bodo.ir.connector.generate_filter_map(filters
            )
        gqz__vzg = ', '.join(hcpkf__wmjxk.values())
    dry__icovl = (
        f'def sql_reader_py(sql_request, conn, database_schema, {gqz__vzg}):\n'
        )
    if db_type == 'iceberg':
        lltj__tnzx, gkr__nuy = bodo.ir.connector.generate_arrow_filters(filters
            , hcpkf__wmjxk, fqke__njs, col_names, col_names, col_typs,
            typemap, 'iceberg')
        dpvci__mqf = ',' if gqz__vzg else ''
        dry__icovl += (
            f"  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})\n")
        dry__icovl += f"""  dnf_filters, expr_filters = get_filters_pyobject("{lltj__tnzx}", "{gkr__nuy}", ({gqz__vzg}{dpvci__mqf}))
"""
        dry__icovl += f'  out_table = iceberg_read(\n'
        dry__icovl += (
            f'    unicode_to_utf8(conn), unicode_to_utf8(database_schema),\n')
        dry__icovl += (
            f'    unicode_to_utf8(sql_request), {parallel}, dnf_filters,\n')
        dry__icovl += (
            f'    expr_filters, selected_cols_arr_{jxhxk__ttj}.ctypes,\n')
        dry__icovl += (
            f'    {len(col_names)}, nullable_cols_arr_{jxhxk__ttj}.ctypes,\n')
        dry__icovl += f'    pyarrow_table_schema_{jxhxk__ttj},\n'
        dry__icovl += f'  )\n'
        dry__icovl += f'  check_and_propagate_cpp_exception()\n'
        ymr__aen = list(range(len(col_names)))
        ttad__szh = {xwgu__ukurb: yjmsz__csfud for yjmsz__csfud,
            xwgu__ukurb in enumerate(ymr__aen)}
        obqt__mlocs = [int(is_nullable(col_typs[yjmsz__csfud])) for
            yjmsz__csfud in type_usecol_offset]
        czdc__kzsn = not type_usecol_offset
        xege__ctl = TableType(tuple(col_typs))
        if czdc__kzsn:
            xege__ctl = types.none
        uvdas__ofo = 'None'
        if index_column_name is not None:
            kouur__buub = len(type_usecol_offset) + 1 if not czdc__kzsn else 0
            uvdas__ofo = (
                f'info_to_array(info_from_table(out_table, {kouur__buub}), index_col_typ)'
                )
        dry__icovl += f'  index_var = {uvdas__ofo}\n'
        wkvjp__jqppq = None
        if not czdc__kzsn:
            wkvjp__jqppq = []
            goynu__afn = 0
            for yjmsz__csfud, bss__jvhq in enumerate(ymr__aen):
                if goynu__afn < len(type_usecol_offset
                    ) and yjmsz__csfud == type_usecol_offset[goynu__afn]:
                    wkvjp__jqppq.append(ttad__szh[bss__jvhq])
                    goynu__afn += 1
                else:
                    wkvjp__jqppq.append(-1)
            wkvjp__jqppq = np.array(wkvjp__jqppq, dtype=np.int64)
        if czdc__kzsn:
            dry__icovl += '  table_var = None\n'
        else:
            dry__icovl += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{jxhxk__ttj}, py_table_type_{jxhxk__ttj})
"""
        dry__icovl += f'  delete_table(out_table)\n'
        dry__icovl += f'  ev.finalize()\n'
    elif db_type == 'snowflake':
        dry__icovl += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        obqt__mlocs = [int(is_nullable(col_typs[yjmsz__csfud])) for
            yjmsz__csfud in type_usecol_offset]
        if index_column_name:
            obqt__mlocs.append(int(is_nullable(index_column_type)))
        dry__icovl += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(obqt__mlocs)}, np.array({obqt__mlocs}, dtype=np.int32).ctypes)
"""
        dry__icovl += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            dry__icovl += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            dry__icovl += '  index_var = None\n'
        if type_usecol_offset:
            chxr__ugshn = []
            goynu__afn = 0
            for yjmsz__csfud in range(len(col_names)):
                if goynu__afn < len(type_usecol_offset
                    ) and yjmsz__csfud == type_usecol_offset[goynu__afn]:
                    chxr__ugshn.append(goynu__afn)
                    goynu__afn += 1
                else:
                    chxr__ugshn.append(-1)
            wkvjp__jqppq = np.array(chxr__ugshn, dtype=np.int64)
            dry__icovl += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{jxhxk__ttj}, py_table_type_{jxhxk__ttj})
"""
        else:
            dry__icovl += '  table_var = None\n'
        dry__icovl += '  delete_table(out_table)\n'
        dry__icovl += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            dry__icovl += f"""  type_usecols_offsets_arr_{jxhxk__ttj}_2 = type_usecols_offsets_arr_{jxhxk__ttj}
"""
            zcbf__yss = np.array(type_usecol_offset, dtype=np.int64)
        dry__icovl += '  df_typeref_2 = df_typeref\n'
        dry__icovl += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            dry__icovl += '  pymysql_check()\n'
        elif db_type == 'oracle':
            dry__icovl += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            dry__icovl += '  psycopg2_check()\n'
        if parallel:
            dry__icovl += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                dry__icovl += f'  nb_row = {limit}\n'
            else:
                dry__icovl += '  with objmode(nb_row="int64"):\n'
                dry__icovl += f'     if rank == {MPI_ROOT}:\n'
                dry__icovl += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                dry__icovl += '         frame = pd.read_sql(sql_cons, conn)\n'
                dry__icovl += '         nb_row = frame.iat[0,0]\n'
                dry__icovl += '     else:\n'
                dry__icovl += '         nb_row = 0\n'
                dry__icovl += '  nb_row = bcast_scalar(nb_row)\n'
            dry__icovl += f"""  with objmode(table_var=py_table_type_{jxhxk__ttj}, index_var=index_col_typ):
"""
            dry__icovl += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                dry__icovl += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                dry__icovl += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            dry__icovl += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            dry__icovl += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            dry__icovl += f"""  with objmode(table_var=py_table_type_{jxhxk__ttj}, index_var=index_col_typ):
"""
            dry__icovl += '    df_ret = pd.read_sql(sql_request, conn)\n'
            dry__icovl += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            dry__icovl += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            dry__icovl += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            dry__icovl += '    index_var = None\n'
        if type_usecol_offset:
            dry__icovl += f'    arrs = []\n'
            dry__icovl += f'    for i in range(df_ret.shape[1]):\n'
            dry__icovl += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            dry__icovl += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{jxhxk__ttj}_2, {len(col_names)})
"""
        else:
            dry__icovl += '    table_var = None\n'
    dry__icovl += '  return (table_var, index_var)\n'
    ivvch__dvoo = globals()
    ivvch__dvoo.update({'bodo': bodo, f'py_table_type_{jxhxk__ttj}':
        xege__ctl, 'index_col_typ': index_column_type, '_pq_reader_py':
        lfwe__hpiy})
    if db_type in ('iceberg', 'snowflake'):
        ivvch__dvoo.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{jxhxk__ttj}': wkvjp__jqppq})
    if db_type == 'iceberg':
        ivvch__dvoo.update({f'selected_cols_arr_{jxhxk__ttj}': np.array(
            ymr__aen, np.int32), f'nullable_cols_arr_{jxhxk__ttj}': np.
            array(obqt__mlocs, np.int32), f'py_table_type_{jxhxk__ttj}':
            xege__ctl, f'pyarrow_table_schema_{jxhxk__ttj}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read})
    elif db_type == 'snowflake':
        ivvch__dvoo.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        ivvch__dvoo.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(kkhkd__excz), bodo.RangeIndexType(None
            ), tuple(ctnyn__kkvjb)), 'Table': Table,
            f'type_usecols_offsets_arr_{jxhxk__ttj}': zcbf__yss})
    pjlra__bnl = {}
    exec(dry__icovl, ivvch__dvoo, pjlra__bnl)
    agl__pvuc = pjlra__bnl['sql_reader_py']
    iyzh__qzwsz = numba.njit(agl__pvuc)
    compiled_funcs.append(iyzh__qzwsz)
    return iyzh__qzwsz


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
