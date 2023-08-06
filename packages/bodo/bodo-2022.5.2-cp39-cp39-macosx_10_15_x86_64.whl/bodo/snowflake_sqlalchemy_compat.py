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
    uxg__ckah = {}
    dnyfg__xxlbm, lhpj__dnnol = self._current_database_schema(connection, **kw)
    fzu__hqlr = self._denormalize_quote_join(dnyfg__xxlbm, schema)
    try:
        cqxy__mbagb = self._get_schema_primary_keys(connection, fzu__hqlr, **kw
            )
        hkhx__rojpy = connection.execute(text(
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
    except sa_exc.ProgrammingError as xjer__dkizj:
        if xjer__dkizj.orig.errno == 90030:
            return None
        raise
    for table_name, lty__zuymz, wtypr__ocws, cnjdh__adpht, knno__pft, rwjq__wuri, lccoc__dig, etfe__gql, iac__bdu, qgq__blupa in hkhx__rojpy:
        table_name = self.normalize_name(table_name)
        lty__zuymz = self.normalize_name(lty__zuymz)
        if table_name not in uxg__ckah:
            uxg__ckah[table_name] = list()
        if lty__zuymz.startswith('sys_clustering_column'):
            continue
        iroiq__kmk = self.ischema_names.get(wtypr__ocws, None)
        zdez__ert = {}
        if iroiq__kmk is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(wtypr__ocws, lty__zuymz))
            iroiq__kmk = sqltypes.NULLTYPE
        elif issubclass(iroiq__kmk, sqltypes.FLOAT):
            zdez__ert['precision'] = knno__pft
            zdez__ert['decimal_return_scale'] = rwjq__wuri
        elif issubclass(iroiq__kmk, sqltypes.Numeric):
            zdez__ert['precision'] = knno__pft
            zdez__ert['scale'] = rwjq__wuri
        elif issubclass(iroiq__kmk, (sqltypes.String, sqltypes.BINARY)):
            zdez__ert['length'] = cnjdh__adpht
        lkwf__hmhez = iroiq__kmk if isinstance(iroiq__kmk, sqltypes.NullType
            ) else iroiq__kmk(**zdez__ert)
        ksm__mgv = cqxy__mbagb.get(table_name)
        uxg__ckah[table_name].append({'name': lty__zuymz, 'type':
            lkwf__hmhez, 'nullable': lccoc__dig == 'YES', 'default':
            etfe__gql, 'autoincrement': iac__bdu == 'YES', 'comment':
            qgq__blupa, 'primary_key': lty__zuymz in cqxy__mbagb[table_name
            ]['constrained_columns'] if ksm__mgv else False})
    return uxg__ckah


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
    uxg__ckah = []
    dnyfg__xxlbm, lhpj__dnnol = self._current_database_schema(connection, **kw)
    fzu__hqlr = self._denormalize_quote_join(dnyfg__xxlbm, schema)
    cqxy__mbagb = self._get_schema_primary_keys(connection, fzu__hqlr, **kw)
    hkhx__rojpy = connection.execute(text(
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
    for table_name, lty__zuymz, wtypr__ocws, cnjdh__adpht, knno__pft, rwjq__wuri, lccoc__dig, etfe__gql, iac__bdu, qgq__blupa in hkhx__rojpy:
        table_name = self.normalize_name(table_name)
        lty__zuymz = self.normalize_name(lty__zuymz)
        if lty__zuymz.startswith('sys_clustering_column'):
            continue
        iroiq__kmk = self.ischema_names.get(wtypr__ocws, None)
        zdez__ert = {}
        if iroiq__kmk is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(wtypr__ocws, lty__zuymz))
            iroiq__kmk = sqltypes.NULLTYPE
        elif issubclass(iroiq__kmk, sqltypes.FLOAT):
            zdez__ert['precision'] = knno__pft
            zdez__ert['decimal_return_scale'] = rwjq__wuri
        elif issubclass(iroiq__kmk, sqltypes.Numeric):
            zdez__ert['precision'] = knno__pft
            zdez__ert['scale'] = rwjq__wuri
        elif issubclass(iroiq__kmk, (sqltypes.String, sqltypes.BINARY)):
            zdez__ert['length'] = cnjdh__adpht
        lkwf__hmhez = iroiq__kmk if isinstance(iroiq__kmk, sqltypes.NullType
            ) else iroiq__kmk(**zdez__ert)
        ksm__mgv = cqxy__mbagb.get(table_name)
        uxg__ckah.append({'name': lty__zuymz, 'type': lkwf__hmhez,
            'nullable': lccoc__dig == 'YES', 'default': etfe__gql,
            'autoincrement': iac__bdu == 'YES', 'comment': qgq__blupa if 
            qgq__blupa != '' else None, 'primary_key': lty__zuymz in
            cqxy__mbagb[table_name]['constrained_columns'] if ksm__mgv else
            False})
    return uxg__ckah


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
