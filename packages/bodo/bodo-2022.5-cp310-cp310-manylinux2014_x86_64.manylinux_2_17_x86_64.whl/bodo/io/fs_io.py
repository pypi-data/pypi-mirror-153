"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            rwusl__xphz = self.fs.open_input_file(path)
        except:
            rwusl__xphz = self.fs.open_input_stream(path)
    elif mode == 'wb':
        rwusl__xphz = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, rwusl__xphz, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    qyld__jgtnk = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    qvfui__lmu = False
    eil__aadwa = get_proxy_uri_from_env_vars()
    if storage_options:
        qvfui__lmu = storage_options.get('anon', False)
    return S3FileSystem(anonymous=qvfui__lmu, region=region,
        endpoint_override=qyld__jgtnk, proxy_options=eil__aadwa)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    qyld__jgtnk = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    qvfui__lmu = False
    eil__aadwa = get_proxy_uri_from_env_vars()
    if storage_options:
        qvfui__lmu = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=qyld__jgtnk,
        anonymous=qvfui__lmu, proxy_options=eil__aadwa)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    lcx__plkfq = urlparse(path)
    if lcx__plkfq.scheme in ('abfs', 'abfss'):
        zzdwh__bglaa = path
        if lcx__plkfq.port is None:
            kae__erhjy = 0
        else:
            kae__erhjy = lcx__plkfq.port
        qpv__nkk = None
    else:
        zzdwh__bglaa = lcx__plkfq.hostname
        kae__erhjy = lcx__plkfq.port
        qpv__nkk = lcx__plkfq.username
    try:
        fs = HdFS(host=zzdwh__bglaa, port=kae__erhjy, user=qpv__nkk)
    except Exception as fcfzk__bjhb:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            fcfzk__bjhb))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        jzenc__tsc = fs.isdir(path)
    except gcsfs.utils.HttpError as fcfzk__bjhb:
        raise BodoError(
            f'{fcfzk__bjhb}. Make sure your google cloud credentials are set!')
    return jzenc__tsc


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [nayx__ywizn.split('/')[-1] for nayx__ywizn in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        lcx__plkfq = urlparse(path)
        ibim__lvv = (lcx__plkfq.netloc + lcx__plkfq.path).rstrip('/')
        zro__cqqyj = fs.get_file_info(ibim__lvv)
        if zro__cqqyj.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not zro__cqqyj.size and zro__cqqyj.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as fcfzk__bjhb:
        raise
    except BodoError as trtew__qcge:
        raise
    except Exception as fcfzk__bjhb:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(fcfzk__bjhb).__name__}: {str(fcfzk__bjhb)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    stqdk__ygd = None
    try:
        if s3_is_directory(fs, path):
            lcx__plkfq = urlparse(path)
            ibim__lvv = (lcx__plkfq.netloc + lcx__plkfq.path).rstrip('/')
            fobw__uwtm = pa_fs.FileSelector(ibim__lvv, recursive=False)
            dfcc__nsto = fs.get_file_info(fobw__uwtm)
            if dfcc__nsto and dfcc__nsto[0].path in [ibim__lvv, f'{ibim__lvv}/'
                ] and int(dfcc__nsto[0].size or 0) == 0:
                dfcc__nsto = dfcc__nsto[1:]
            stqdk__ygd = [hpln__iewib.base_name for hpln__iewib in dfcc__nsto]
    except BodoError as trtew__qcge:
        raise
    except Exception as fcfzk__bjhb:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(fcfzk__bjhb).__name__}: {str(fcfzk__bjhb)}
{bodo_error_msg}"""
            )
    return stqdk__ygd


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    lcx__plkfq = urlparse(path)
    bxtkv__mbwy = lcx__plkfq.path
    try:
        owret__aav = HadoopFileSystem.from_uri(path)
    except Exception as fcfzk__bjhb:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            fcfzk__bjhb))
    ajh__uxr = owret__aav.get_file_info([bxtkv__mbwy])
    if ajh__uxr[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not ajh__uxr[0].size and ajh__uxr[0].type == FileType.Directory:
        return owret__aav, True
    return owret__aav, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    stqdk__ygd = None
    owret__aav, jzenc__tsc = hdfs_is_directory(path)
    if jzenc__tsc:
        lcx__plkfq = urlparse(path)
        bxtkv__mbwy = lcx__plkfq.path
        fobw__uwtm = FileSelector(bxtkv__mbwy, recursive=True)
        try:
            dfcc__nsto = owret__aav.get_file_info(fobw__uwtm)
        except Exception as fcfzk__bjhb:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(bxtkv__mbwy, fcfzk__bjhb))
        stqdk__ygd = [hpln__iewib.base_name for hpln__iewib in dfcc__nsto]
    return owret__aav, stqdk__ygd


def abfs_is_directory(path):
    owret__aav = get_hdfs_fs(path)
    try:
        ajh__uxr = owret__aav.info(path)
    except OSError as trtew__qcge:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if ajh__uxr['size'] == 0 and ajh__uxr['kind'].lower() == 'directory':
        return owret__aav, True
    return owret__aav, False


def abfs_list_dir_fnames(path):
    stqdk__ygd = None
    owret__aav, jzenc__tsc = abfs_is_directory(path)
    if jzenc__tsc:
        lcx__plkfq = urlparse(path)
        bxtkv__mbwy = lcx__plkfq.path
        try:
            iucqr__ugtu = owret__aav.ls(bxtkv__mbwy)
        except Exception as fcfzk__bjhb:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(bxtkv__mbwy, fcfzk__bjhb))
        stqdk__ygd = [fname[fname.rindex('/') + 1:] for fname in iucqr__ugtu]
    return owret__aav, stqdk__ygd


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    hbnwk__qdxg = urlparse(path)
    fname = path
    fs = None
    uoho__bwnn = 'read_json' if ftype == 'json' else 'read_csv'
    xyye__askj = (
        f'pd.{uoho__bwnn}(): there is no {ftype} file in directory: {fname}')
    jqj__jfcq = directory_of_files_common_filter
    if hbnwk__qdxg.scheme == 's3':
        ewrkk__yfl = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        jorr__qxwu = s3_list_dir_fnames(fs, path)
        ibim__lvv = (hbnwk__qdxg.netloc + hbnwk__qdxg.path).rstrip('/')
        fname = ibim__lvv
        if jorr__qxwu:
            jorr__qxwu = [(ibim__lvv + '/' + nayx__ywizn) for nayx__ywizn in
                sorted(filter(jqj__jfcq, jorr__qxwu))]
            agi__xcjr = [nayx__ywizn for nayx__ywizn in jorr__qxwu if int(
                fs.get_file_info(nayx__ywizn).size or 0) > 0]
            if len(agi__xcjr) == 0:
                raise BodoError(xyye__askj)
            fname = agi__xcjr[0]
        mkb__mwkr = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        plaiu__lwbz = fs._open(fname)
    elif hbnwk__qdxg.scheme == 'hdfs':
        ewrkk__yfl = True
        fs, jorr__qxwu = hdfs_list_dir_fnames(path)
        mkb__mwkr = fs.get_file_info([hbnwk__qdxg.path])[0].size
        if jorr__qxwu:
            path = path.rstrip('/')
            jorr__qxwu = [(path + '/' + nayx__ywizn) for nayx__ywizn in
                sorted(filter(jqj__jfcq, jorr__qxwu))]
            agi__xcjr = [nayx__ywizn for nayx__ywizn in jorr__qxwu if fs.
                get_file_info([urlparse(nayx__ywizn).path])[0].size > 0]
            if len(agi__xcjr) == 0:
                raise BodoError(xyye__askj)
            fname = agi__xcjr[0]
            fname = urlparse(fname).path
            mkb__mwkr = fs.get_file_info([fname])[0].size
        plaiu__lwbz = fs.open_input_file(fname)
    elif hbnwk__qdxg.scheme in ('abfs', 'abfss'):
        ewrkk__yfl = True
        fs, jorr__qxwu = abfs_list_dir_fnames(path)
        mkb__mwkr = fs.info(fname)['size']
        if jorr__qxwu:
            path = path.rstrip('/')
            jorr__qxwu = [(path + '/' + nayx__ywizn) for nayx__ywizn in
                sorted(filter(jqj__jfcq, jorr__qxwu))]
            agi__xcjr = [nayx__ywizn for nayx__ywizn in jorr__qxwu if fs.
                info(nayx__ywizn)['size'] > 0]
            if len(agi__xcjr) == 0:
                raise BodoError(xyye__askj)
            fname = agi__xcjr[0]
            mkb__mwkr = fs.info(fname)['size']
            fname = urlparse(fname).path
        plaiu__lwbz = fs.open(fname, 'rb')
    else:
        if hbnwk__qdxg.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {hbnwk__qdxg.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        ewrkk__yfl = False
        if os.path.isdir(path):
            iucqr__ugtu = filter(jqj__jfcq, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            agi__xcjr = [nayx__ywizn for nayx__ywizn in sorted(iucqr__ugtu) if
                os.path.getsize(nayx__ywizn) > 0]
            if len(agi__xcjr) == 0:
                raise BodoError(xyye__askj)
            fname = agi__xcjr[0]
        mkb__mwkr = os.path.getsize(fname)
        plaiu__lwbz = fname
    return ewrkk__yfl, plaiu__lwbz, mkb__mwkr, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    yyf__tsmr = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            dii__qmxic, zeea__dwgmz = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = dii__qmxic.region
        except Exception as fcfzk__bjhb:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{fcfzk__bjhb}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = yyf__tsmr.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, is_parallel=False):

    def impl(path_or_buf, D, is_parallel=False):
        ace__yvf = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel)
        jeln__fhgt, iashg__tkoz = unicode_to_utf8_and_len(D)
        dam__mnyqf = 0
        if is_parallel:
            dam__mnyqf = bodo.libs.distributed_api.dist_exscan(iashg__tkoz,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), jeln__fhgt, dam__mnyqf,
            iashg__tkoz, is_parallel, unicode_to_utf8(ace__yvf))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    ooo__enplq = get_overload_constant_dict(storage_options)
    zlbpb__gvet = 'def impl(storage_options):\n'
    zlbpb__gvet += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    zlbpb__gvet += f'    storage_options_py = {str(ooo__enplq)}\n'
    zlbpb__gvet += '  return storage_options_py\n'
    fduf__hvjmw = {}
    exec(zlbpb__gvet, globals(), fduf__hvjmw)
    return fduf__hvjmw['impl']
