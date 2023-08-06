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
    jpwb__htlab = {}
    mznc__gsixp, xgsr__rle = self._current_database_schema(connection, **kw)
    bxxnh__mum = self._denormalize_quote_join(mznc__gsixp, schema)
    try:
        zxsnp__fab = self._get_schema_primary_keys(connection, bxxnh__mum, **kw
            )
        lsbt__uiy = connection.execute(text(
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
    except sa_exc.ProgrammingError as rzam__rzv:
        if rzam__rzv.orig.errno == 90030:
            return None
        raise
    for table_name, yldh__rlw, dhg__yoe, aznf__dymad, rrx__mtfvj, vym__pfpy, ult__nugvt, wsb__rrvcm, antdj__lsdnz, fdhae__fss in lsbt__uiy:
        table_name = self.normalize_name(table_name)
        yldh__rlw = self.normalize_name(yldh__rlw)
        if table_name not in jpwb__htlab:
            jpwb__htlab[table_name] = list()
        if yldh__rlw.startswith('sys_clustering_column'):
            continue
        pprl__edn = self.ischema_names.get(dhg__yoe, None)
        ywq__csgp = {}
        if pprl__edn is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(dhg__yoe, yldh__rlw))
            pprl__edn = sqltypes.NULLTYPE
        elif issubclass(pprl__edn, sqltypes.FLOAT):
            ywq__csgp['precision'] = rrx__mtfvj
            ywq__csgp['decimal_return_scale'] = vym__pfpy
        elif issubclass(pprl__edn, sqltypes.Numeric):
            ywq__csgp['precision'] = rrx__mtfvj
            ywq__csgp['scale'] = vym__pfpy
        elif issubclass(pprl__edn, (sqltypes.String, sqltypes.BINARY)):
            ywq__csgp['length'] = aznf__dymad
        agz__faah = pprl__edn if isinstance(pprl__edn, sqltypes.NullType
            ) else pprl__edn(**ywq__csgp)
        bjcg__dxoo = zxsnp__fab.get(table_name)
        jpwb__htlab[table_name].append({'name': yldh__rlw, 'type':
            agz__faah, 'nullable': ult__nugvt == 'YES', 'default':
            wsb__rrvcm, 'autoincrement': antdj__lsdnz == 'YES', 'comment':
            fdhae__fss, 'primary_key': yldh__rlw in zxsnp__fab[table_name][
            'constrained_columns'] if bjcg__dxoo else False})
    return jpwb__htlab


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
    jpwb__htlab = []
    mznc__gsixp, xgsr__rle = self._current_database_schema(connection, **kw)
    bxxnh__mum = self._denormalize_quote_join(mznc__gsixp, schema)
    zxsnp__fab = self._get_schema_primary_keys(connection, bxxnh__mum, **kw)
    lsbt__uiy = connection.execute(text(
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
    for table_name, yldh__rlw, dhg__yoe, aznf__dymad, rrx__mtfvj, vym__pfpy, ult__nugvt, wsb__rrvcm, antdj__lsdnz, fdhae__fss in lsbt__uiy:
        table_name = self.normalize_name(table_name)
        yldh__rlw = self.normalize_name(yldh__rlw)
        if yldh__rlw.startswith('sys_clustering_column'):
            continue
        pprl__edn = self.ischema_names.get(dhg__yoe, None)
        ywq__csgp = {}
        if pprl__edn is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(dhg__yoe, yldh__rlw))
            pprl__edn = sqltypes.NULLTYPE
        elif issubclass(pprl__edn, sqltypes.FLOAT):
            ywq__csgp['precision'] = rrx__mtfvj
            ywq__csgp['decimal_return_scale'] = vym__pfpy
        elif issubclass(pprl__edn, sqltypes.Numeric):
            ywq__csgp['precision'] = rrx__mtfvj
            ywq__csgp['scale'] = vym__pfpy
        elif issubclass(pprl__edn, (sqltypes.String, sqltypes.BINARY)):
            ywq__csgp['length'] = aznf__dymad
        agz__faah = pprl__edn if isinstance(pprl__edn, sqltypes.NullType
            ) else pprl__edn(**ywq__csgp)
        bjcg__dxoo = zxsnp__fab.get(table_name)
        jpwb__htlab.append({'name': yldh__rlw, 'type': agz__faah,
            'nullable': ult__nugvt == 'YES', 'default': wsb__rrvcm,
            'autoincrement': antdj__lsdnz == 'YES', 'comment': fdhae__fss if
            fdhae__fss != '' else None, 'primary_key': yldh__rlw in
            zxsnp__fab[table_name]['constrained_columns'] if bjcg__dxoo else
            False})
    return jpwb__htlab


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
