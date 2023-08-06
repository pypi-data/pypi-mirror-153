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
        efy__swcv = bodo_iceberg_connector.get_bodo_connector_typing_schema(con
            , database_schema, table_name)
    except bodo_iceberg_connector.IcebergError as sty__gypu:
        if isinstance(sty__gypu, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{sty__gypu.message}:\n {sty__gypu.java_error.stacktrace()}')
        else:
            raise BodoError(sty__gypu.message)
    return efy__swcv


def get_iceberg_file_list(table_name, conn, database_schema, filters):
    import bodo_iceberg_connector
    import numba.core
    try:
        cbsrp__xowpd = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as sty__gypu:
        if isinstance(sty__gypu, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{sty__gypu.message}:\n {sty__gypu.java_error.stacktrace()}')
        else:
            raise BodoError(sty__gypu.message)
    return cbsrp__xowpd


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
    ewj__azn = tracing.Event('get_iceberg_pq_dataset')
    from mpi4py import MPI
    ypcug__hps = MPI.COMM_WORLD
    sdiv__ziajk = None
    if bodo.get_rank() == 0 or not is_parallel:
        tfcue__ekef = tracing.Event('get_iceberg_file_list', is_parallel=False)
        try:
            sdiv__ziajk = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                lrsb__ouocg = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                tfcue__ekef.add_attribute('num_files', len(sdiv__ziajk))
                tfcue__ekef.add_attribute(f'first_{lrsb__ouocg}_files',
                    ', '.join(sdiv__ziajk[:lrsb__ouocg]))
        except Exception as sty__gypu:
            sdiv__ziajk = sty__gypu
        tfcue__ekef.finalize()
    if is_parallel:
        sdiv__ziajk = ypcug__hps.bcast(sdiv__ziajk)
    if isinstance(sdiv__ziajk, Exception):
        nzg__qvjqz = sdiv__ziajk
        raise BodoError(
            f"""Error reading Iceberg Table: {type(nzg__qvjqz).__name__}: {str(nzg__qvjqz)}
"""
            )
    zvkoe__lrkv = sdiv__ziajk
    if len(zvkoe__lrkv) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(zvkoe__lrkv,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema)
        except BodoError as sty__gypu:
            if re.search('Schema .* was different', str(sty__gypu), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{sty__gypu}"""
                    )
            else:
                raise
    gfnic__rwqq = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    ewj__azn.finalize()
    return gfnic__rwqq
