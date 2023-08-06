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
        kjhv__ymmde = bodo_iceberg_connector.get_bodo_connector_typing_schema(
            con, database_schema, table_name)
    except bodo_iceberg_connector.IcebergError as hnvo__jedsa:
        if isinstance(hnvo__jedsa, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{hnvo__jedsa.message}:\n {hnvo__jedsa.java_error.stacktrace()}'
                )
        else:
            raise BodoError(hnvo__jedsa.message)
    return kjhv__ymmde


def get_iceberg_file_list(table_name, conn, database_schema, filters):
    import bodo_iceberg_connector
    import numba.core
    try:
        ghzf__lvhj = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as hnvo__jedsa:
        if isinstance(hnvo__jedsa, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{hnvo__jedsa.message}:\n {hnvo__jedsa.java_error.stacktrace()}'
                )
        else:
            raise BodoError(hnvo__jedsa.message)
    return ghzf__lvhj


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
    tlkte__dcqd = tracing.Event('get_iceberg_pq_dataset')
    from mpi4py import MPI
    yuvgi__xtg = MPI.COMM_WORLD
    kashf__uvs = None
    if bodo.get_rank() == 0 or not is_parallel:
        likd__hehc = tracing.Event('get_iceberg_file_list', is_parallel=False)
        try:
            kashf__uvs = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                skz__izraw = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                likd__hehc.add_attribute('num_files', len(kashf__uvs))
                likd__hehc.add_attribute(f'first_{skz__izraw}_files', ', '.
                    join(kashf__uvs[:skz__izraw]))
        except Exception as hnvo__jedsa:
            kashf__uvs = hnvo__jedsa
        likd__hehc.finalize()
    if is_parallel:
        kashf__uvs = yuvgi__xtg.bcast(kashf__uvs)
    if isinstance(kashf__uvs, Exception):
        rciry__lrh = kashf__uvs
        raise BodoError(
            f"""Error reading Iceberg Table: {type(rciry__lrh).__name__}: {str(rciry__lrh)}
"""
            )
    fzwl__olxr = kashf__uvs
    if len(fzwl__olxr) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(fzwl__olxr,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema)
        except BodoError as hnvo__jedsa:
            if re.search('Schema .* was different', str(hnvo__jedsa), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{hnvo__jedsa}"""
                    )
            else:
                raise
    oqcyr__mwgbi = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    tlkte__dcqd.finalize()
    return oqcyr__mwgbi
