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
    qdd__hedep = urlparse(conn_str)
    tjebb__zlz = {}
    if qdd__hedep.username:
        tjebb__zlz['user'] = qdd__hedep.username
    if qdd__hedep.password:
        tjebb__zlz['password'] = qdd__hedep.password
    if qdd__hedep.hostname:
        tjebb__zlz['account'] = qdd__hedep.hostname
    if qdd__hedep.port:
        tjebb__zlz['port'] = qdd__hedep.port
    if qdd__hedep.path:
        yxw__lobq = qdd__hedep.path
        if yxw__lobq.startswith('/'):
            yxw__lobq = yxw__lobq[1:]
        ivm__cxfjw, schema = yxw__lobq.split('/')
        tjebb__zlz['database'] = ivm__cxfjw
        if schema:
            tjebb__zlz['schema'] = schema
    if qdd__hedep.query:
        for ppeke__eqcz, ubm__rvhb in parse_qsl(qdd__hedep.query):
            tjebb__zlz[ppeke__eqcz] = ubm__rvhb
            if ppeke__eqcz == 'session_parameters':
                tjebb__zlz[ppeke__eqcz] = json.loads(ubm__rvhb)
    tjebb__zlz['application'] = 'bodo'
    return tjebb__zlz


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for xep__alw in batches:
            xep__alw._bodo_num_rows = xep__alw.rowcount
            self._bodo_total_rows += xep__alw._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    wpvsm__mnw = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    lgthd__trfbj = MPI.COMM_WORLD
    qupod__mpgbl = tracing.Event('snowflake_connect', is_parallel=False)
    jxa__jms = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**jxa__jms)
    qupod__mpgbl.finalize()
    if bodo.get_rank() == 0:
        dlza__njih = conn.cursor()
        gtwp__nuam = tracing.Event('get_schema', is_parallel=False)
        wwhg__djjah = f'select * from ({query}) x LIMIT {100}'
        ilx__jrlw = dlza__njih.execute(wwhg__djjah).fetch_arrow_all()
        if ilx__jrlw is None:
            mtdtq__mmum = dlza__njih.describe(query)
            wpfod__xmz = [pa.field(xgf__jgkm.name, FIELD_TYPE_TO_PA_TYPE[
                xgf__jgkm.type_code]) for xgf__jgkm in mtdtq__mmum]
            schema = pa.schema(wpfod__xmz)
        else:
            schema = ilx__jrlw.schema
        gtwp__nuam.finalize()
        lmjv__mht = tracing.Event('execute_query', is_parallel=False)
        dlza__njih.execute(query)
        lmjv__mht.finalize()
        batches = dlza__njih.get_result_batches()
        lgthd__trfbj.bcast((batches, schema))
    else:
        batches, schema = lgthd__trfbj.bcast(None)
    xjwd__ugdxo = SnowflakeDataset(batches, schema, conn)
    wpvsm__mnw.finalize()
    return xjwd__ugdxo
