"""
File that contains the main functionality for the Iceberg
integration within the Bodo repo. This does not contain the
main IR transformation.
"""
import os
import re
import bodo
from bodo.utils import tracing
from bodo.utils.typing import BodoError


def get_iceberg_type_info(table_name: str, con: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    try:
        simv__pabvh = bodo_iceberg_connector.get_bodo_connector_typing_schema(
            con, database_schema, table_name)
    except bodo_iceberg_connector.IcebergError as zete__ebkar:
        if isinstance(zete__ebkar, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{zete__ebkar.message}:\n {zete__ebkar.java_error.stacktrace()}'
                )
        else:
            raise BodoError(zete__ebkar.message)
    return simv__pabvh


def get_iceberg_file_list(table_name, conn, database_schema, filters):
    import bodo_iceberg_connector
    import numba.core
    try:
        ncbym__jga = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as zete__ebkar:
        if isinstance(zete__ebkar, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{zete__ebkar.message}:\n {zete__ebkar.java_error.stacktrace()}'
                )
        else:
            raise BodoError(zete__ebkar.message)
    return ncbym__jga


class IcebergParquetDataset(object):

    def __init__(self, conn, database_schema, table_name, pa_table_schema,
        pq_dataset=None):
        self.pq_dataset = pq_dataset
        self.conn = conn
        self.database_schema = database_schema
        self.table_name = table_name
        self.schema = pa_table_schema
        self.pieces = []
        self._bodo_total_rows = 0
        self._prefix = ''
        if pq_dataset is not None:
            self.pieces = pq_dataset.pieces
            self._bodo_total_rows = pq_dataset._bodo_total_rows
            self._prefix = pq_dataset._prefix


def get_iceberg_pq_dataset(conn, database_schema, table_name,
    typing_pa_table_schema, dnf_filters=None, expr_filters=None,
    is_parallel=False):
    uhpq__ndusk = tracing.Event('get_iceberg_pq_dataset')
    from mpi4py import MPI
    jkvi__rfz = MPI.COMM_WORLD
    dnah__efq = None
    if bodo.get_rank() == 0 or not is_parallel:
        siko__jpuv = tracing.Event('get_iceberg_file_list', is_parallel=False)
        try:
            dnah__efq = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                tvx__yeaa = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                siko__jpuv.add_attribute('num_files', len(dnah__efq))
                siko__jpuv.add_attribute(f'first_{tvx__yeaa}_files', ', '.
                    join(dnah__efq[:tvx__yeaa]))
        except Exception as zete__ebkar:
            dnah__efq = zete__ebkar
        siko__jpuv.finalize()
    if is_parallel:
        dnah__efq = jkvi__rfz.bcast(dnah__efq)
    if isinstance(dnah__efq, Exception):
        rrqtj__koady = dnah__efq
        raise BodoError(
            f"""Error reading Iceberg Table: {type(rrqtj__koady).__name__}: {str(rrqtj__koady)}
"""
            )
    nbqvj__hpjb = dnah__efq
    if len(nbqvj__hpjb) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(nbqvj__hpjb,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema)
        except BodoError as zete__ebkar:
            if re.search('Schema .* was different', str(zete__ebkar), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{zete__ebkar}"""
                    )
            else:
                raise
    zyum__wrb = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    uhpq__ndusk.finalize()
    return zyum__wrb
