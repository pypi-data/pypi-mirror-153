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
    flcp__pevm = urlparse(conn_str)
    nzcqw__qbyfw = {}
    if flcp__pevm.username:
        nzcqw__qbyfw['user'] = flcp__pevm.username
    if flcp__pevm.password:
        nzcqw__qbyfw['password'] = flcp__pevm.password
    if flcp__pevm.hostname:
        nzcqw__qbyfw['account'] = flcp__pevm.hostname
    if flcp__pevm.port:
        nzcqw__qbyfw['port'] = flcp__pevm.port
    if flcp__pevm.path:
        wfk__rjsm = flcp__pevm.path
        if wfk__rjsm.startswith('/'):
            wfk__rjsm = wfk__rjsm[1:]
        dhsm__lumpo, schema = wfk__rjsm.split('/')
        nzcqw__qbyfw['database'] = dhsm__lumpo
        if schema:
            nzcqw__qbyfw['schema'] = schema
    if flcp__pevm.query:
        for bgsmr__jyu, cnpv__liul in parse_qsl(flcp__pevm.query):
            nzcqw__qbyfw[bgsmr__jyu] = cnpv__liul
            if bgsmr__jyu == 'session_parameters':
                nzcqw__qbyfw[bgsmr__jyu] = json.loads(cnpv__liul)
    nzcqw__qbyfw['application'] = 'bodo'
    return nzcqw__qbyfw


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for oeha__rfvy in batches:
            oeha__rfvy._bodo_num_rows = oeha__rfvy.rowcount
            self._bodo_total_rows += oeha__rfvy._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    fthdy__ttu = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    uiwbq__esvv = MPI.COMM_WORLD
    ihabn__dcf = tracing.Event('snowflake_connect', is_parallel=False)
    xueoz__qbnz = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**xueoz__qbnz)
    ihabn__dcf.finalize()
    if bodo.get_rank() == 0:
        qwwn__mzc = conn.cursor()
        wrg__vei = tracing.Event('get_schema', is_parallel=False)
        wla__txcpp = f'select * from ({query}) x LIMIT {100}'
        zbj__rfr = qwwn__mzc.execute(wla__txcpp).fetch_arrow_all()
        if zbj__rfr is None:
            steu__gghwv = qwwn__mzc.describe(query)
            euvd__obtfr = [pa.field(unyr__str.name, FIELD_TYPE_TO_PA_TYPE[
                unyr__str.type_code]) for unyr__str in steu__gghwv]
            schema = pa.schema(euvd__obtfr)
        else:
            schema = zbj__rfr.schema
        wrg__vei.finalize()
        tiqnm__myydv = tracing.Event('execute_query', is_parallel=False)
        qwwn__mzc.execute(query)
        tiqnm__myydv.finalize()
        batches = qwwn__mzc.get_result_batches()
        uiwbq__esvv.bcast((batches, schema))
    else:
        batches, schema = uiwbq__esvv.bcast(None)
    vhrz__ste = SnowflakeDataset(batches, schema, conn)
    fthdy__ttu.finalize()
    return vhrz__ste
