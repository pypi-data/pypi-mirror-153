import hashlib
import inspect
import warnings
import snowflake.sqlalchemy
import sqlalchemy.types as sqltypes
from sqlalchemy import exc as sa_exc
from sqlalchemy import util as sa_util
from sqlalchemy.sql import text
_check_snowflake_sqlalchemy_change = True


def _get_schema_columns(self, connection, schema, **kw):
    ltsc__oclst = {}
    xica__zfug, loxed__criw = self._current_database_schema(connection, **kw)
    laec__bhq = self._denormalize_quote_join(xica__zfug, schema)
    try:
        gmeit__zhjqc = self._get_schema_primary_keys(connection, laec__bhq,
            **kw)
        mdxa__zvtuc = connection.execute(text(
            """
        SELECT /* sqlalchemy:_get_schema_columns */
                ic.table_name,
                ic.column_name,
                ic.data_type,
                ic.character_maximum_length,
                ic.numeric_precision,
                ic.numeric_scale,
                ic.is_nullable,
                ic.column_default,
                ic.is_identity,
                ic.comment
            FROM information_schema.columns ic
            WHERE ic.table_schema=:table_schema
            ORDER BY ic.ordinal_position"""
            ), {'table_schema': self.denormalize_name(schema)})
    except sa_exc.ProgrammingError as bnmvi__xpyhj:
        if bnmvi__xpyhj.orig.errno == 90030:
            return None
        raise
    for table_name, oik__kvd, tkura__vyyne, egyu__guur, vfzf__quj, mzw__yyre, rwnxp__pph, syuks__lotav, cucyd__ajlg, toebl__mleo in mdxa__zvtuc:
        table_name = self.normalize_name(table_name)
        oik__kvd = self.normalize_name(oik__kvd)
        if table_name not in ltsc__oclst:
            ltsc__oclst[table_name] = list()
        if oik__kvd.startswith('sys_clustering_column'):
            continue
        sxk__azm = self.ischema_names.get(tkura__vyyne, None)
        jty__lsrx = {}
        if sxk__azm is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(tkura__vyyne, oik__kvd))
            sxk__azm = sqltypes.NULLTYPE
        elif issubclass(sxk__azm, sqltypes.FLOAT):
            jty__lsrx['precision'] = vfzf__quj
            jty__lsrx['decimal_return_scale'] = mzw__yyre
        elif issubclass(sxk__azm, sqltypes.Numeric):
            jty__lsrx['precision'] = vfzf__quj
            jty__lsrx['scale'] = mzw__yyre
        elif issubclass(sxk__azm, (sqltypes.String, sqltypes.BINARY)):
            jty__lsrx['length'] = egyu__guur
        jvqju__hocx = sxk__azm if isinstance(sxk__azm, sqltypes.NullType
            ) else sxk__azm(**jty__lsrx)
        cdq__vxqhl = gmeit__zhjqc.get(table_name)
        ltsc__oclst[table_name].append({'name': oik__kvd, 'type':
            jvqju__hocx, 'nullable': rwnxp__pph == 'YES', 'default':
            syuks__lotav, 'autoincrement': cucyd__ajlg == 'YES', 'comment':
            toebl__mleo, 'primary_key': oik__kvd in gmeit__zhjqc[table_name
            ]['constrained_columns'] if cdq__vxqhl else False})
    return ltsc__oclst


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_schema_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdf39af1ac165319d3b6074e8cf9296a090a21f0e2c05b644ff8ec0e56e2d769':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns = (
    _get_schema_columns)


def _get_table_columns(self, connection, table_name, schema=None, **kw):
    ltsc__oclst = []
    xica__zfug, loxed__criw = self._current_database_schema(connection, **kw)
    laec__bhq = self._denormalize_quote_join(xica__zfug, schema)
    gmeit__zhjqc = self._get_schema_primary_keys(connection, laec__bhq, **kw)
    mdxa__zvtuc = connection.execute(text(
        """
    SELECT /* sqlalchemy:get_table_columns */
            ic.table_name,
            ic.column_name,
            ic.data_type,
            ic.character_maximum_length,
            ic.numeric_precision,
            ic.numeric_scale,
            ic.is_nullable,
            ic.column_default,
            ic.is_identity,
            ic.comment
        FROM information_schema.columns ic
        WHERE ic.table_schema=:table_schema
        AND ic.table_name=:table_name
        ORDER BY ic.ordinal_position"""
        ), {'table_schema': self.denormalize_name(schema), 'table_name':
        self.denormalize_name(table_name)})
    for table_name, oik__kvd, tkura__vyyne, egyu__guur, vfzf__quj, mzw__yyre, rwnxp__pph, syuks__lotav, cucyd__ajlg, toebl__mleo in mdxa__zvtuc:
        table_name = self.normalize_name(table_name)
        oik__kvd = self.normalize_name(oik__kvd)
        if oik__kvd.startswith('sys_clustering_column'):
            continue
        sxk__azm = self.ischema_names.get(tkura__vyyne, None)
        jty__lsrx = {}
        if sxk__azm is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(tkura__vyyne, oik__kvd))
            sxk__azm = sqltypes.NULLTYPE
        elif issubclass(sxk__azm, sqltypes.FLOAT):
            jty__lsrx['precision'] = vfzf__quj
            jty__lsrx['decimal_return_scale'] = mzw__yyre
        elif issubclass(sxk__azm, sqltypes.Numeric):
            jty__lsrx['precision'] = vfzf__quj
            jty__lsrx['scale'] = mzw__yyre
        elif issubclass(sxk__azm, (sqltypes.String, sqltypes.BINARY)):
            jty__lsrx['length'] = egyu__guur
        jvqju__hocx = sxk__azm if isinstance(sxk__azm, sqltypes.NullType
            ) else sxk__azm(**jty__lsrx)
        cdq__vxqhl = gmeit__zhjqc.get(table_name)
        ltsc__oclst.append({'name': oik__kvd, 'type': jvqju__hocx,
            'nullable': rwnxp__pph == 'YES', 'default': syuks__lotav,
            'autoincrement': cucyd__ajlg == 'YES', 'comment': toebl__mleo if
            toebl__mleo != '' else None, 'primary_key': oik__kvd in
            gmeit__zhjqc[table_name]['constrained_columns'] if cdq__vxqhl else
            False})
    return ltsc__oclst


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_table_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9ecc8a2425c655836ade4008b1b98a8fd1819f3be43ba77b0fbbfc1f8740e2be':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns = (
    _get_table_columns)
