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
    rbdx__bjqg = urlparse(conn_str)
    gomce__ljt = {}
    if rbdx__bjqg.username:
        gomce__ljt['user'] = rbdx__bjqg.username
    if rbdx__bjqg.password:
        gomce__ljt['password'] = rbdx__bjqg.password
    if rbdx__bjqg.hostname:
        gomce__ljt['account'] = rbdx__bjqg.hostname
    if rbdx__bjqg.port:
        gomce__ljt['port'] = rbdx__bjqg.port
    if rbdx__bjqg.path:
        irk__bhus = rbdx__bjqg.path
        if irk__bhus.startswith('/'):
            irk__bhus = irk__bhus[1:]
        ouqyy__hbsxv, schema = irk__bhus.split('/')
        gomce__ljt['database'] = ouqyy__hbsxv
        if schema:
            gomce__ljt['schema'] = schema
    if rbdx__bjqg.query:
        for ejvv__zczmn, pexo__yiey in parse_qsl(rbdx__bjqg.query):
            gomce__ljt[ejvv__zczmn] = pexo__yiey
            if ejvv__zczmn == 'session_parameters':
                gomce__ljt[ejvv__zczmn] = json.loads(pexo__yiey)
    gomce__ljt['application'] = 'bodo'
    return gomce__ljt


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for wisyk__oaq in batches:
            wisyk__oaq._bodo_num_rows = wisyk__oaq.rowcount
            self._bodo_total_rows += wisyk__oaq._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    sha__txbvr = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    zfob__ufv = MPI.COMM_WORLD
    ihy__owmb = tracing.Event('snowflake_connect', is_parallel=False)
    fmpcp__iqmdk = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**fmpcp__iqmdk)
    ihy__owmb.finalize()
    if bodo.get_rank() == 0:
        jdfqq__kze = conn.cursor()
        xwlr__dgsw = tracing.Event('get_schema', is_parallel=False)
        xjpu__qvl = f'select * from ({query}) x LIMIT {100}'
        pfccx__mipeg = jdfqq__kze.execute(xjpu__qvl).fetch_arrow_all()
        if pfccx__mipeg is None:
            yxn__emjg = jdfqq__kze.describe(query)
            dzi__uok = [pa.field(sgn__zlvc.name, FIELD_TYPE_TO_PA_TYPE[
                sgn__zlvc.type_code]) for sgn__zlvc in yxn__emjg]
            schema = pa.schema(dzi__uok)
        else:
            schema = pfccx__mipeg.schema
        xwlr__dgsw.finalize()
        enqh__rsls = tracing.Event('execute_query', is_parallel=False)
        jdfqq__kze.execute(query)
        enqh__rsls.finalize()
        batches = jdfqq__kze.get_result_batches()
        zfob__ufv.bcast((batches, schema))
    else:
        batches, schema = zfob__ufv.bcast(None)
    fra__jdsz = SnowflakeDataset(batches, schema, conn)
    sha__txbvr.finalize()
    return fra__jdsz
