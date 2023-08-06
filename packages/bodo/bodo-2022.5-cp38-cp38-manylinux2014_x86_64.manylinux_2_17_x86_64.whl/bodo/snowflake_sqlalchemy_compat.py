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
    zxi__sszju = {}
    aciu__kwl, vxgq__iqx = self._current_database_schema(connection, **kw)
    uspk__agfo = self._denormalize_quote_join(aciu__kwl, schema)
    try:
        cboo__ekkh = self._get_schema_primary_keys(connection, uspk__agfo, **kw
            )
        ford__wcfh = connection.execute(text(
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
    except sa_exc.ProgrammingError as cjl__foq:
        if cjl__foq.orig.errno == 90030:
            return None
        raise
    for table_name, pkv__bxl, ateaa__pmkub, oph__nrqns, irju__unwuj, lbla__nwlp, pjxag__euufn, qnu__frx, deong__iss, cgf__yydyr in ford__wcfh:
        table_name = self.normalize_name(table_name)
        pkv__bxl = self.normalize_name(pkv__bxl)
        if table_name not in zxi__sszju:
            zxi__sszju[table_name] = list()
        if pkv__bxl.startswith('sys_clustering_column'):
            continue
        skrg__kybno = self.ischema_names.get(ateaa__pmkub, None)
        stnk__jgkn = {}
        if skrg__kybno is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(ateaa__pmkub, pkv__bxl))
            skrg__kybno = sqltypes.NULLTYPE
        elif issubclass(skrg__kybno, sqltypes.FLOAT):
            stnk__jgkn['precision'] = irju__unwuj
            stnk__jgkn['decimal_return_scale'] = lbla__nwlp
        elif issubclass(skrg__kybno, sqltypes.Numeric):
            stnk__jgkn['precision'] = irju__unwuj
            stnk__jgkn['scale'] = lbla__nwlp
        elif issubclass(skrg__kybno, (sqltypes.String, sqltypes.BINARY)):
            stnk__jgkn['length'] = oph__nrqns
        rzwzr__qwnlx = skrg__kybno if isinstance(skrg__kybno, sqltypes.NullType
            ) else skrg__kybno(**stnk__jgkn)
        ojpbu__kqfox = cboo__ekkh.get(table_name)
        zxi__sszju[table_name].append({'name': pkv__bxl, 'type':
            rzwzr__qwnlx, 'nullable': pjxag__euufn == 'YES', 'default':
            qnu__frx, 'autoincrement': deong__iss == 'YES', 'comment':
            cgf__yydyr, 'primary_key': pkv__bxl in cboo__ekkh[table_name][
            'constrained_columns'] if ojpbu__kqfox else False})
    return zxi__sszju


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
    zxi__sszju = []
    aciu__kwl, vxgq__iqx = self._current_database_schema(connection, **kw)
    uspk__agfo = self._denormalize_quote_join(aciu__kwl, schema)
    cboo__ekkh = self._get_schema_primary_keys(connection, uspk__agfo, **kw)
    ford__wcfh = connection.execute(text(
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
    for table_name, pkv__bxl, ateaa__pmkub, oph__nrqns, irju__unwuj, lbla__nwlp, pjxag__euufn, qnu__frx, deong__iss, cgf__yydyr in ford__wcfh:
        table_name = self.normalize_name(table_name)
        pkv__bxl = self.normalize_name(pkv__bxl)
        if pkv__bxl.startswith('sys_clustering_column'):
            continue
        skrg__kybno = self.ischema_names.get(ateaa__pmkub, None)
        stnk__jgkn = {}
        if skrg__kybno is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(ateaa__pmkub, pkv__bxl))
            skrg__kybno = sqltypes.NULLTYPE
        elif issubclass(skrg__kybno, sqltypes.FLOAT):
            stnk__jgkn['precision'] = irju__unwuj
            stnk__jgkn['decimal_return_scale'] = lbla__nwlp
        elif issubclass(skrg__kybno, sqltypes.Numeric):
            stnk__jgkn['precision'] = irju__unwuj
            stnk__jgkn['scale'] = lbla__nwlp
        elif issubclass(skrg__kybno, (sqltypes.String, sqltypes.BINARY)):
            stnk__jgkn['length'] = oph__nrqns
        rzwzr__qwnlx = skrg__kybno if isinstance(skrg__kybno, sqltypes.NullType
            ) else skrg__kybno(**stnk__jgkn)
        ojpbu__kqfox = cboo__ekkh.get(table_name)
        zxi__sszju.append({'name': pkv__bxl, 'type': rzwzr__qwnlx,
            'nullable': pjxag__euufn == 'YES', 'default': qnu__frx,
            'autoincrement': deong__iss == 'YES', 'comment': cgf__yydyr if 
            cgf__yydyr != '' else None, 'primary_key': pkv__bxl in
            cboo__ekkh[table_name]['constrained_columns'] if ojpbu__kqfox else
            False})
    return zxi__sszju


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
