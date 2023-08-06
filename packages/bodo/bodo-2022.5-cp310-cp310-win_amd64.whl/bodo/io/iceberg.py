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
        yiqcc__ybdry = bodo_iceberg_connector.get_bodo_connector_typing_schema(
            con, database_schema, table_name)
    except bodo_iceberg_connector.IcebergError as adm__ciqpx:
        if isinstance(adm__ciqpx, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{adm__ciqpx.message}:\n {adm__ciqpx.java_error.stacktrace()}'
                )
        else:
            raise BodoError(adm__ciqpx.message)
    return yiqcc__ybdry


def get_iceberg_file_list(table_name, conn, database_schema, filters):
    import bodo_iceberg_connector
    import numba.core
    try:
        bsu__wte = bodo_iceberg_connector.bodo_connector_get_parquet_file_list(
            conn, database_schema, table_name, filters)
    except bodo_iceberg_connector.IcebergError as adm__ciqpx:
        if isinstance(adm__ciqpx, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(
                f'{adm__ciqpx.message}:\n {adm__ciqpx.java_error.stacktrace()}'
                )
        else:
            raise BodoError(adm__ciqpx.message)
    return bsu__wte


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
    whhvg__egii = tracing.Event('get_iceberg_pq_dataset')
    from mpi4py import MPI
    gyjzv__gln = MPI.COMM_WORLD
    lshr__ipp = None
    if bodo.get_rank() == 0 or not is_parallel:
        zmatb__hwkev = tracing.Event('get_iceberg_file_list', is_parallel=False
            )
        try:
            lshr__ipp = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                zjh__qoy = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                zmatb__hwkev.add_attribute('num_files', len(lshr__ipp))
                zmatb__hwkev.add_attribute(f'first_{zjh__qoy}_files', ', '.
                    join(lshr__ipp[:zjh__qoy]))
        except Exception as adm__ciqpx:
            lshr__ipp = adm__ciqpx
        zmatb__hwkev.finalize()
    if is_parallel:
        lshr__ipp = gyjzv__gln.bcast(lshr__ipp)
    if isinstance(lshr__ipp, Exception):
        omw__xug = lshr__ipp
        raise BodoError(
            f'Error reading Iceberg Table: {type(omw__xug).__name__}: {str(omw__xug)}\n'
            )
    ufa__fzdqa = lshr__ipp
    if len(ufa__fzdqa) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(ufa__fzdqa,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema)
        except BodoError as adm__ciqpx:
            if re.search('Schema .* was different', str(adm__ciqpx), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{adm__ciqpx}"""
                    )
            else:
                raise
    uda__npy = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    whhvg__egii.finalize()
    return uda__npy
