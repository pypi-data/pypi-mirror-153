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
        hpbd__kgb = bodo_iceberg_connector.get_bodo_connector_typing_schema(con
            , database_schema, table_name)
    except bodo_iceberg_connector.IcebergError as wcji__ewcyb:
        if isinstance(wcji__ewcyb, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{wcji__ewcyb.message}:\n {wcji__ewcyb.java_error.stacktrace()}'
                )
        else:
            raise BodoError(wcji__ewcyb.message)
    return hpbd__kgb


def get_iceberg_file_list(table_name, conn, database_schema, filters):
    import bodo_iceberg_connector
    import numba.core
    try:
        lzp__kuhok = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as wcji__ewcyb:
        if isinstance(wcji__ewcyb, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{wcji__ewcyb.message}:\n {wcji__ewcyb.java_error.stacktrace()}'
                )
        else:
            raise BodoError(wcji__ewcyb.message)
    return lzp__kuhok


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
    idzeb__ufwp = tracing.Event('get_iceberg_pq_dataset')
    from mpi4py import MPI
    qnos__btw = MPI.COMM_WORLD
    opaf__mvk = None
    if bodo.get_rank() == 0 or not is_parallel:
        zart__buv = tracing.Event('get_iceberg_file_list', is_parallel=False)
        try:
            opaf__mvk = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                vwqz__gube = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                zart__buv.add_attribute('num_files', len(opaf__mvk))
                zart__buv.add_attribute(f'first_{vwqz__gube}_files', ', '.
                    join(opaf__mvk[:vwqz__gube]))
        except Exception as wcji__ewcyb:
            opaf__mvk = wcji__ewcyb
        zart__buv.finalize()
    if is_parallel:
        opaf__mvk = qnos__btw.bcast(opaf__mvk)
    if isinstance(opaf__mvk, Exception):
        cpwna__wfsen = opaf__mvk
        raise BodoError(
            f"""Error reading Iceberg Table: {type(cpwna__wfsen).__name__}: {str(cpwna__wfsen)}
"""
            )
    eqicj__vnbpc = opaf__mvk
    if len(eqicj__vnbpc) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(eqicj__vnbpc,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema)
        except BodoError as wcji__ewcyb:
            if re.search('Schema .* was different', str(wcji__ewcyb), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{wcji__ewcyb}"""
                    )
            else:
                raise
    org__fktn = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    idzeb__ufwp.finalize()
    return org__fktn
