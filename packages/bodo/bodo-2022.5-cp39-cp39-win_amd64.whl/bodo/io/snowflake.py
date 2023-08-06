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
    qdxv__vpq = urlparse(conn_str)
    ckida__vnr = {}
    if qdxv__vpq.username:
        ckida__vnr['user'] = qdxv__vpq.username
    if qdxv__vpq.password:
        ckida__vnr['password'] = qdxv__vpq.password
    if qdxv__vpq.hostname:
        ckida__vnr['account'] = qdxv__vpq.hostname
    if qdxv__vpq.port:
        ckida__vnr['port'] = qdxv__vpq.port
    if qdxv__vpq.path:
        gra__iyf = qdxv__vpq.path
        if gra__iyf.startswith('/'):
            gra__iyf = gra__iyf[1:]
        roahq__odao, schema = gra__iyf.split('/')
        ckida__vnr['database'] = roahq__odao
        if schema:
            ckida__vnr['schema'] = schema
    if qdxv__vpq.query:
        for sep__zuewz, orlt__uiko in parse_qsl(qdxv__vpq.query):
            ckida__vnr[sep__zuewz] = orlt__uiko
            if sep__zuewz == 'session_parameters':
                ckida__vnr[sep__zuewz] = json.loads(orlt__uiko)
    ckida__vnr['application'] = 'bodo'
    return ckida__vnr


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for xjlv__yes in batches:
            xjlv__yes._bodo_num_rows = xjlv__yes.rowcount
            self._bodo_total_rows += xjlv__yes._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    ocvv__lqly = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    mnk__bagdm = MPI.COMM_WORLD
    ahgox__aitpq = tracing.Event('snowflake_connect', is_parallel=False)
    hoc__xzou = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**hoc__xzou)
    ahgox__aitpq.finalize()
    if bodo.get_rank() == 0:
        zuaac__xzisb = conn.cursor()
        ixql__rtvzq = tracing.Event('get_schema', is_parallel=False)
        eiym__izu = f'select * from ({query}) x LIMIT {100}'
        ptmu__rsg = zuaac__xzisb.execute(eiym__izu).fetch_arrow_all()
        if ptmu__rsg is None:
            iuq__asmwc = zuaac__xzisb.describe(query)
            tdte__qwm = [pa.field(rbi__fpj.name, FIELD_TYPE_TO_PA_TYPE[
                rbi__fpj.type_code]) for rbi__fpj in iuq__asmwc]
            schema = pa.schema(tdte__qwm)
        else:
            schema = ptmu__rsg.schema
        ixql__rtvzq.finalize()
        juc__ilud = tracing.Event('execute_query', is_parallel=False)
        zuaac__xzisb.execute(query)
        juc__ilud.finalize()
        batches = zuaac__xzisb.get_result_batches()
        mnk__bagdm.bcast((batches, schema))
    else:
        batches, schema = mnk__bagdm.bcast(None)
    hxpw__tylgt = SnowflakeDataset(batches, schema, conn)
    ocvv__lqly.finalize()
    return hxpw__tylgt
