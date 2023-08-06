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
    urspc__vsnq = urlparse(con_str)
    db_type = urspc__vsnq.scheme
    fjpj__kiw = urspc__vsnq.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', fjpj__kiw
    if db_type == 'mysql+pymysql':
        return 'mysql', fjpj__kiw
    return db_type, fjpj__kiw


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    mrzxt__wkcz = sql_node.out_vars[0].name
    mpw__vyvu = sql_node.out_vars[1].name
    if mrzxt__wkcz not in lives and mpw__vyvu not in lives:
        return None
    elif mrzxt__wkcz not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif mpw__vyvu not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        vymeq__mrvgo = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        koyko__reum = []
        cyo__dxw = []
        for etew__gjbk in sql_node.type_usecol_offset:
            rhit__wgjcf = sql_node.df_colnames[etew__gjbk]
            koyko__reum.append(rhit__wgjcf)
            if isinstance(sql_node.out_types[etew__gjbk], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                cyo__dxw.append(rhit__wgjcf)
        if sql_node.index_column_name:
            koyko__reum.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                cyo__dxw.append(sql_node.index_column_name)
        jfwp__wzsfk = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', vymeq__mrvgo,
            jfwp__wzsfk, koyko__reum)
        if cyo__dxw:
            zltu__hyp = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', zltu__hyp,
                jfwp__wzsfk, cyo__dxw)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        qobtb__dou = set(sql_node.unsupported_columns)
        bbj__hwjgk = set(sql_node.type_usecol_offset)
        ntxek__ibte = bbj__hwjgk & qobtb__dou
        if ntxek__ibte:
            jnrvu__puvuf = sorted(ntxek__ibte)
            puqfk__tzj = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            dxr__vbg = 0
            for vfe__wxdil in jnrvu__puvuf:
                while sql_node.unsupported_columns[dxr__vbg] != vfe__wxdil:
                    dxr__vbg += 1
                puqfk__tzj.append(
                    f"Column '{sql_node.original_df_colnames[vfe__wxdil]}' with unsupported arrow type {sql_node.unsupported_arrow_types[dxr__vbg]}"
                    )
                dxr__vbg += 1
            uic__hzp = '\n'.join(puqfk__tzj)
            raise BodoError(uic__hzp, loc=sql_node.loc)
    umzun__naer, ldppj__bmq = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    skc__szy = ', '.join(umzun__naer.values())
    mnz__kozut = (
        f'def sql_impl(sql_request, conn, database_schema, {skc__szy}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        qwzo__qmevv = []
        for tjt__oejd in sql_node.filters:
            vob__wskpa = [' '.join(['(', kzy__ukfdy[0], kzy__ukfdy[1], '{' +
                umzun__naer[kzy__ukfdy[2].name] + '}' if isinstance(
                kzy__ukfdy[2], ir.Var) else kzy__ukfdy[2], ')']) for
                kzy__ukfdy in tjt__oejd]
            qwzo__qmevv.append(' ( ' + ' AND '.join(vob__wskpa) + ' ) ')
        jiep__lxxjf = ' WHERE ' + ' OR '.join(qwzo__qmevv)
        for etew__gjbk, fon__mip in enumerate(umzun__naer.values()):
            mnz__kozut += f'    {fon__mip} = get_sql_literal({fon__mip})\n'
        mnz__kozut += f'    sql_request = f"{{sql_request}} {jiep__lxxjf}"\n'
    tnqb__oldb = ''
    if sql_node.db_type == 'iceberg':
        tnqb__oldb = skc__szy
    mnz__kozut += f"""    (table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {tnqb__oldb})
"""
    xiwz__kpq = {}
    exec(mnz__kozut, {}, xiwz__kpq)
    vwmbd__ktpuj = xiwz__kpq['sql_impl']
    mhp__ltdin = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, typemap, sql_node.filters, sql_node.
        pyarrow_table_schema)
    npse__kpsyu = (types.none if sql_node.database_schema is None else
        string_type)
    npltw__umznh = compile_to_numba_ir(vwmbd__ktpuj, {'_sql_reader_py':
        mhp__ltdin, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type,
        npse__kpsyu) + tuple(typemap[iqg__tbnj.name] for iqg__tbnj in
        ldppj__bmq), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        bpj__zsn = [sql_node.df_colnames[etew__gjbk] for etew__gjbk in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            bpj__zsn.append(sql_node.index_column_name)
        ypmu__zzc = escape_column_names(bpj__zsn, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            onngy__ezph = ('SELECT ' + ypmu__zzc + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            onngy__ezph = ('SELECT ' + ypmu__zzc + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        onngy__ezph = sql_node.sql_request
    replace_arg_nodes(npltw__umznh, [ir.Const(onngy__ezph, sql_node.loc),
        ir.Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + ldppj__bmq)
    eol__syru = npltw__umznh.body[:-3]
    eol__syru[-2].target = sql_node.out_vars[0]
    eol__syru[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        eol__syru.pop(-1)
    elif not sql_node.type_usecol_offset:
        eol__syru.pop(-2)
    return eol__syru


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        bpj__zsn = [(mtgtn__wht.upper() if mtgtn__wht in converted_colnames
             else mtgtn__wht) for mtgtn__wht in col_names]
        ypmu__zzc = ', '.join([f'"{mtgtn__wht}"' for mtgtn__wht in bpj__zsn])
    elif db_type == 'mysql':
        ypmu__zzc = ', '.join([f'`{mtgtn__wht}`' for mtgtn__wht in col_names])
    else:
        ypmu__zzc = ', '.join([f'"{mtgtn__wht}"' for mtgtn__wht in col_names])
    return ypmu__zzc


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    docbr__ljuy = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(docbr__ljuy,
        'Filter pushdown')
    if docbr__ljuy == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(docbr__ljuy, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif docbr__ljuy == bodo.pd_timestamp_type:

        def impl(filter_value):
            ynzz__qiicn = filter_value.nanosecond
            dxvq__htr = ''
            if ynzz__qiicn < 10:
                dxvq__htr = '00'
            elif ynzz__qiicn < 100:
                dxvq__htr = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{dxvq__htr}{ynzz__qiicn}'"
                )
        return impl
    elif docbr__ljuy == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {docbr__ljuy} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    byy__cgvn = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    docbr__ljuy = types.unliteral(filter_value)
    if isinstance(docbr__ljuy, types.List) and (isinstance(docbr__ljuy.
        dtype, scalar_isinstance) or docbr__ljuy.dtype in byy__cgvn):

        def impl(filter_value):
            dhl__jnhs = ', '.join([_get_snowflake_sql_literal_scalar(
                mtgtn__wht) for mtgtn__wht in filter_value])
            return f'({dhl__jnhs})'
        return impl
    elif isinstance(docbr__ljuy, scalar_isinstance
        ) or docbr__ljuy in byy__cgvn:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {docbr__ljuy} used in filter pushdown.'
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
    except ImportError as ctn__xuboi:
        dwfk__feowu = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(dwfk__feowu)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as ctn__xuboi:
        dwfk__feowu = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(dwfk__feowu)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as ctn__xuboi:
        dwfk__feowu = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(dwfk__feowu)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as ctn__xuboi:
        dwfk__feowu = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(dwfk__feowu)


def req_limit(sql_request):
    import re
    ellbv__abqk = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    fqp__catwk = ellbv__abqk.search(sql_request)
    if fqp__catwk:
        return int(fqp__catwk.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, typemap, filters, pyarrow_table_schema):
    ihgtt__bribs = next_label()
    bpj__zsn = [col_names[etew__gjbk] for etew__gjbk in type_usecol_offset]
    pjqt__inqfw = [col_typs[etew__gjbk] for etew__gjbk in type_usecol_offset]
    if index_column_name:
        bpj__zsn.append(index_column_name)
        pjqt__inqfw.append(index_column_type)
    sbbw__awu = None
    fhf__bsj = None
    ldhhd__bje = types.none
    jlkhk__ahhr = None
    if type_usecol_offset:
        ldhhd__bje = TableType(tuple(col_typs))
    tnqb__oldb = ''
    umzun__naer = {}
    ldppj__bmq = []
    if filters and db_type == 'iceberg':
        umzun__naer, ldppj__bmq = bodo.ir.connector.generate_filter_map(filters
            )
        tnqb__oldb = ', '.join(umzun__naer.values())
    mnz__kozut = (
        f'def sql_reader_py(sql_request, conn, database_schema, {tnqb__oldb}):\n'
        )
    if db_type == 'iceberg':
        mkg__aaxpn, uuz__zsz = bodo.ir.connector.generate_arrow_filters(filters
            , umzun__naer, ldppj__bmq, col_names, col_names, col_typs,
            typemap, 'iceberg')
        nzjre__kpyys = ',' if tnqb__oldb else ''
        mnz__kozut += (
            f"  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})\n")
        mnz__kozut += f"""  dnf_filters, expr_filters = get_filters_pyobject("{mkg__aaxpn}", "{uuz__zsz}", ({tnqb__oldb}{nzjre__kpyys}))
"""
        mnz__kozut += f'  out_table = iceberg_read(\n'
        mnz__kozut += (
            f'    unicode_to_utf8(conn), unicode_to_utf8(database_schema),\n')
        mnz__kozut += (
            f'    unicode_to_utf8(sql_request), {parallel}, dnf_filters,\n')
        mnz__kozut += (
            f'    expr_filters, selected_cols_arr_{ihgtt__bribs}.ctypes,\n')
        mnz__kozut += (
            f'    {len(col_names)}, nullable_cols_arr_{ihgtt__bribs}.ctypes,\n'
            )
        mnz__kozut += f'    pyarrow_table_schema_{ihgtt__bribs},\n'
        mnz__kozut += f'  )\n'
        mnz__kozut += f'  check_and_propagate_cpp_exception()\n'
        hzq__nndjb = list(range(len(col_names)))
        ijjw__eyb = {qtrxq__laoxm: etew__gjbk for etew__gjbk, qtrxq__laoxm in
            enumerate(hzq__nndjb)}
        buil__abho = [int(is_nullable(col_typs[etew__gjbk])) for etew__gjbk in
            type_usecol_offset]
        fpe__cnry = not type_usecol_offset
        ldhhd__bje = TableType(tuple(col_typs))
        if fpe__cnry:
            ldhhd__bje = types.none
        mpw__vyvu = 'None'
        if index_column_name is not None:
            nsulu__fzo = len(type_usecol_offset) + 1 if not fpe__cnry else 0
            mpw__vyvu = (
                f'info_to_array(info_from_table(out_table, {nsulu__fzo}), index_col_typ)'
                )
        mnz__kozut += f'  index_var = {mpw__vyvu}\n'
        sbbw__awu = None
        if not fpe__cnry:
            sbbw__awu = []
            yurm__ryvtf = 0
            for etew__gjbk, vfe__wxdil in enumerate(hzq__nndjb):
                if yurm__ryvtf < len(type_usecol_offset
                    ) and etew__gjbk == type_usecol_offset[yurm__ryvtf]:
                    sbbw__awu.append(ijjw__eyb[vfe__wxdil])
                    yurm__ryvtf += 1
                else:
                    sbbw__awu.append(-1)
            sbbw__awu = np.array(sbbw__awu, dtype=np.int64)
        if fpe__cnry:
            mnz__kozut += '  table_var = None\n'
        else:
            mnz__kozut += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{ihgtt__bribs}, py_table_type_{ihgtt__bribs})
"""
        mnz__kozut += f'  delete_table(out_table)\n'
        mnz__kozut += f'  ev.finalize()\n'
    elif db_type == 'snowflake':
        mnz__kozut += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        buil__abho = [int(is_nullable(col_typs[etew__gjbk])) for etew__gjbk in
            type_usecol_offset]
        if index_column_name:
            buil__abho.append(int(is_nullable(index_column_type)))
        mnz__kozut += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(buil__abho)}, np.array({buil__abho}, dtype=np.int32).ctypes)
"""
        mnz__kozut += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            mnz__kozut += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            mnz__kozut += '  index_var = None\n'
        if type_usecol_offset:
            dxr__vbg = []
            yurm__ryvtf = 0
            for etew__gjbk in range(len(col_names)):
                if yurm__ryvtf < len(type_usecol_offset
                    ) and etew__gjbk == type_usecol_offset[yurm__ryvtf]:
                    dxr__vbg.append(yurm__ryvtf)
                    yurm__ryvtf += 1
                else:
                    dxr__vbg.append(-1)
            sbbw__awu = np.array(dxr__vbg, dtype=np.int64)
            mnz__kozut += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{ihgtt__bribs}, py_table_type_{ihgtt__bribs})
"""
        else:
            mnz__kozut += '  table_var = None\n'
        mnz__kozut += '  delete_table(out_table)\n'
        mnz__kozut += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            mnz__kozut += f"""  type_usecols_offsets_arr_{ihgtt__bribs}_2 = type_usecols_offsets_arr_{ihgtt__bribs}
"""
            fhf__bsj = np.array(type_usecol_offset, dtype=np.int64)
        mnz__kozut += '  df_typeref_2 = df_typeref\n'
        mnz__kozut += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            mnz__kozut += '  pymysql_check()\n'
        elif db_type == 'oracle':
            mnz__kozut += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            mnz__kozut += '  psycopg2_check()\n'
        if parallel:
            mnz__kozut += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                mnz__kozut += f'  nb_row = {limit}\n'
            else:
                mnz__kozut += '  with objmode(nb_row="int64"):\n'
                mnz__kozut += f'     if rank == {MPI_ROOT}:\n'
                mnz__kozut += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                mnz__kozut += '         frame = pd.read_sql(sql_cons, conn)\n'
                mnz__kozut += '         nb_row = frame.iat[0,0]\n'
                mnz__kozut += '     else:\n'
                mnz__kozut += '         nb_row = 0\n'
                mnz__kozut += '  nb_row = bcast_scalar(nb_row)\n'
            mnz__kozut += f"""  with objmode(table_var=py_table_type_{ihgtt__bribs}, index_var=index_col_typ):
"""
            mnz__kozut += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                mnz__kozut += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                mnz__kozut += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            mnz__kozut += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            mnz__kozut += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            mnz__kozut += f"""  with objmode(table_var=py_table_type_{ihgtt__bribs}, index_var=index_col_typ):
"""
            mnz__kozut += '    df_ret = pd.read_sql(sql_request, conn)\n'
            mnz__kozut += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            mnz__kozut += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            mnz__kozut += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            mnz__kozut += '    index_var = None\n'
        if type_usecol_offset:
            mnz__kozut += f'    arrs = []\n'
            mnz__kozut += f'    for i in range(df_ret.shape[1]):\n'
            mnz__kozut += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            mnz__kozut += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{ihgtt__bribs}_2, {len(col_names)})
"""
        else:
            mnz__kozut += '    table_var = None\n'
    mnz__kozut += '  return (table_var, index_var)\n'
    bqsb__ifd = globals()
    bqsb__ifd.update({'bodo': bodo, f'py_table_type_{ihgtt__bribs}':
        ldhhd__bje, 'index_col_typ': index_column_type, '_pq_reader_py':
        jlkhk__ahhr})
    if db_type in ('iceberg', 'snowflake'):
        bqsb__ifd.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{ihgtt__bribs}': sbbw__awu})
    if db_type == 'iceberg':
        bqsb__ifd.update({f'selected_cols_arr_{ihgtt__bribs}': np.array(
            hzq__nndjb, np.int32), f'nullable_cols_arr_{ihgtt__bribs}': np.
            array(buil__abho, np.int32), f'py_table_type_{ihgtt__bribs}':
            ldhhd__bje, f'pyarrow_table_schema_{ihgtt__bribs}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read})
    elif db_type == 'snowflake':
        bqsb__ifd.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        bqsb__ifd.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(pjqt__inqfw), bodo.RangeIndexType(None
            ), tuple(bpj__zsn)), 'Table': Table,
            f'type_usecols_offsets_arr_{ihgtt__bribs}': fhf__bsj})
    xiwz__kpq = {}
    exec(mnz__kozut, bqsb__ifd, xiwz__kpq)
    mhp__ltdin = xiwz__kpq['sql_reader_py']
    ntm__nyjyc = numba.njit(mhp__ltdin)
    compiled_funcs.append(ntm__nyjyc)
    return ntm__nyjyc


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
