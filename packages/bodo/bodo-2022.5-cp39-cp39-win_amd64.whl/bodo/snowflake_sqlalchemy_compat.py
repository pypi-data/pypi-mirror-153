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
    ykpz__lsb = {}
    jbcb__qtv, dzriu__xodqd = self._current_database_schema(connection, **kw)
    qimk__iwks = self._denormalize_quote_join(jbcb__qtv, schema)
    try:
        uaoq__owcc = self._get_schema_primary_keys(connection, qimk__iwks, **kw
            )
        fzh__zpc = connection.execute(text(
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
    except sa_exc.ProgrammingError as ggakh__dtv:
        if ggakh__dtv.orig.errno == 90030:
            return None
        raise
    for table_name, hgg__nnpnf, dhzyk__ijt, tvym__tgdlx, xsul__dueek, gzt__cpy, cerd__lycpl, pjkrx__dkot, tvqr__bbari, gwvyg__ncip in fzh__zpc:
        table_name = self.normalize_name(table_name)
        hgg__nnpnf = self.normalize_name(hgg__nnpnf)
        if table_name not in ykpz__lsb:
            ykpz__lsb[table_name] = list()
        if hgg__nnpnf.startswith('sys_clustering_column'):
            continue
        kuna__ljz = self.ischema_names.get(dhzyk__ijt, None)
        pmdkv__kru = {}
        if kuna__ljz is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(dhzyk__ijt, hgg__nnpnf))
            kuna__ljz = sqltypes.NULLTYPE
        elif issubclass(kuna__ljz, sqltypes.FLOAT):
            pmdkv__kru['precision'] = xsul__dueek
            pmdkv__kru['decimal_return_scale'] = gzt__cpy
        elif issubclass(kuna__ljz, sqltypes.Numeric):
            pmdkv__kru['precision'] = xsul__dueek
            pmdkv__kru['scale'] = gzt__cpy
        elif issubclass(kuna__ljz, (sqltypes.String, sqltypes.BINARY)):
            pmdkv__kru['length'] = tvym__tgdlx
        bce__cvw = kuna__ljz if isinstance(kuna__ljz, sqltypes.NullType
            ) else kuna__ljz(**pmdkv__kru)
        kec__nvlr = uaoq__owcc.get(table_name)
        ykpz__lsb[table_name].append({'name': hgg__nnpnf, 'type': bce__cvw,
            'nullable': cerd__lycpl == 'YES', 'default': pjkrx__dkot,
            'autoincrement': tvqr__bbari == 'YES', 'comment': gwvyg__ncip,
            'primary_key': hgg__nnpnf in uaoq__owcc[table_name][
            'constrained_columns'] if kec__nvlr else False})
    return ykpz__lsb


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
    ykpz__lsb = []
    jbcb__qtv, dzriu__xodqd = self._current_database_schema(connection, **kw)
    qimk__iwks = self._denormalize_quote_join(jbcb__qtv, schema)
    uaoq__owcc = self._get_schema_primary_keys(connection, qimk__iwks, **kw)
    fzh__zpc = connection.execute(text(
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
    for table_name, hgg__nnpnf, dhzyk__ijt, tvym__tgdlx, xsul__dueek, gzt__cpy, cerd__lycpl, pjkrx__dkot, tvqr__bbari, gwvyg__ncip in fzh__zpc:
        table_name = self.normalize_name(table_name)
        hgg__nnpnf = self.normalize_name(hgg__nnpnf)
        if hgg__nnpnf.startswith('sys_clustering_column'):
            continue
        kuna__ljz = self.ischema_names.get(dhzyk__ijt, None)
        pmdkv__kru = {}
        if kuna__ljz is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(dhzyk__ijt, hgg__nnpnf))
            kuna__ljz = sqltypes.NULLTYPE
        elif issubclass(kuna__ljz, sqltypes.FLOAT):
            pmdkv__kru['precision'] = xsul__dueek
            pmdkv__kru['decimal_return_scale'] = gzt__cpy
        elif issubclass(kuna__ljz, sqltypes.Numeric):
            pmdkv__kru['precision'] = xsul__dueek
            pmdkv__kru['scale'] = gzt__cpy
        elif issubclass(kuna__ljz, (sqltypes.String, sqltypes.BINARY)):
            pmdkv__kru['length'] = tvym__tgdlx
        bce__cvw = kuna__ljz if isinstance(kuna__ljz, sqltypes.NullType
            ) else kuna__ljz(**pmdkv__kru)
        kec__nvlr = uaoq__owcc.get(table_name)
        ykpz__lsb.append({'name': hgg__nnpnf, 'type': bce__cvw, 'nullable':
            cerd__lycpl == 'YES', 'default': pjkrx__dkot, 'autoincrement': 
            tvqr__bbari == 'YES', 'comment': gwvyg__ncip if gwvyg__ncip !=
            '' else None, 'primary_key': hgg__nnpnf in uaoq__owcc[
            table_name]['constrained_columns'] if kec__nvlr else False})
    return ykpz__lsb


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
