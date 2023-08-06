from urllib.parse import parse_qsl, urlparse
import pyarrow as pa
import snowflake.connector
import bodo
from bodo.utils import tracing
FIELD_TYPE_TO_PA_TYPE = [pa.int64(), pa.float64(), pa.string(), pa.date32(),
    pa.timestamp('ns'), pa.string(), pa.timestamp('ns'), pa.timestamp('ns'),
    pa.timestamp('ns'), pa.string(), pa.string(), pa.binary(), pa.time64(
    'ns'), pa.bool_()]


def get_connection_params(conn_str):
    import json
    dizxg__ikovn = urlparse(conn_str)
    hemg__xcb = {}
    if dizxg__ikovn.username:
        hemg__xcb['user'] = dizxg__ikovn.username
    if dizxg__ikovn.password:
        hemg__xcb['password'] = dizxg__ikovn.password
    if dizxg__ikovn.hostname:
        hemg__xcb['account'] = dizxg__ikovn.hostname
    if dizxg__ikovn.port:
        hemg__xcb['port'] = dizxg__ikovn.port
    if dizxg__ikovn.path:
        bub__kvx = dizxg__ikovn.path
        if bub__kvx.startswith('/'):
            bub__kvx = bub__kvx[1:]
        znej__hqpy, schema = bub__kvx.split('/')
        hemg__xcb['database'] = znej__hqpy
        if schema:
            hemg__xcb['schema'] = schema
    if dizxg__ikovn.query:
        for gqfs__xoc, nxmdg__jddu in parse_qsl(dizxg__ikovn.query):
            hemg__xcb[gqfs__xoc] = nxmdg__jddu
            if gqfs__xoc == 'session_parameters':
                hemg__xcb[gqfs__xoc] = json.loads(nxmdg__jddu)
    hemg__xcb['application'] = 'bodo'
    return hemg__xcb


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for zgmh__lfbko in batches:
            zgmh__lfbko._bodo_num_rows = zgmh__lfbko.rowcount
            self._bodo_total_rows += zgmh__lfbko._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    toa__qqix = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    ctw__ojgjg = MPI.COMM_WORLD
    blyna__hkg = tracing.Event('snowflake_connect', is_parallel=False)
    mcnp__esmlq = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**mcnp__esmlq)
    blyna__hkg.finalize()
    if bodo.get_rank() == 0:
        qnxs__wmnn = conn.cursor()
        irf__fuc = tracing.Event('get_schema', is_parallel=False)
        hbb__awmh = f'select * from ({query}) x LIMIT {100}'
        hiuk__sdfff = qnxs__wmnn.execute(hbb__awmh).fetch_arrow_all()
        if hiuk__sdfff is None:
            xhwy__lqyvx = qnxs__wmnn.describe(query)
            kmpp__gwxt = [pa.field(tdcog__qmol.name, FIELD_TYPE_TO_PA_TYPE[
                tdcog__qmol.type_code]) for tdcog__qmol in xhwy__lqyvx]
            schema = pa.schema(kmpp__gwxt)
        else:
            schema = hiuk__sdfff.schema
        irf__fuc.finalize()
        zoxi__jaki = tracing.Event('execute_query', is_parallel=False)
        qnxs__wmnn.execute(query)
        zoxi__jaki.finalize()
        batches = qnxs__wmnn.get_result_batches()
        ctw__ojgjg.bcast((batches, schema))
    else:
        batches, schema = ctw__ojgjg.bcast(None)
    shepn__fwj = SnowflakeDataset(batches, schema, conn)
    toa__qqix.finalize()
    return shepn__fwj
