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
            sxof__ttlvt = self.fs.open_input_file(path)
        except:
            sxof__ttlvt = self.fs.open_input_stream(path)
    elif mode == 'wb':
        sxof__ttlvt = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, sxof__ttlvt, path, mode, block_size, **kwargs)


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
    osre__ngj = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    uykpn__ucfl = False
    oubg__lkrf = get_proxy_uri_from_env_vars()
    if storage_options:
        uykpn__ucfl = storage_options.get('anon', False)
    return S3FileSystem(anonymous=uykpn__ucfl, region=region,
        endpoint_override=osre__ngj, proxy_options=oubg__lkrf)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    osre__ngj = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    uykpn__ucfl = False
    oubg__lkrf = get_proxy_uri_from_env_vars()
    if storage_options:
        uykpn__ucfl = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=osre__ngj, anonymous
        =uykpn__ucfl, proxy_options=oubg__lkrf)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    tzt__kkd = urlparse(path)
    if tzt__kkd.scheme in ('abfs', 'abfss'):
        ovag__yei = path
        if tzt__kkd.port is None:
            wkcc__nduy = 0
        else:
            wkcc__nduy = tzt__kkd.port
        sxf__xmxn = None
    else:
        ovag__yei = tzt__kkd.hostname
        wkcc__nduy = tzt__kkd.port
        sxf__xmxn = tzt__kkd.username
    try:
        fs = HdFS(host=ovag__yei, port=wkcc__nduy, user=sxf__xmxn)
    except Exception as qbceb__xlekt:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            qbceb__xlekt))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        aeq__ebye = fs.isdir(path)
    except gcsfs.utils.HttpError as qbceb__xlekt:
        raise BodoError(
            f'{qbceb__xlekt}. Make sure your google cloud credentials are set!'
            )
    return aeq__ebye


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [kvb__xghap.split('/')[-1] for kvb__xghap in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        tzt__kkd = urlparse(path)
        usldk__wqd = (tzt__kkd.netloc + tzt__kkd.path).rstrip('/')
        xkv__jajup = fs.get_file_info(usldk__wqd)
        if xkv__jajup.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not xkv__jajup.size and xkv__jajup.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as qbceb__xlekt:
        raise
    except BodoError as sisih__gloh:
        raise
    except Exception as qbceb__xlekt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(qbceb__xlekt).__name__}: {str(qbceb__xlekt)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    mnoob__tol = None
    try:
        if s3_is_directory(fs, path):
            tzt__kkd = urlparse(path)
            usldk__wqd = (tzt__kkd.netloc + tzt__kkd.path).rstrip('/')
            ksta__ueka = pa_fs.FileSelector(usldk__wqd, recursive=False)
            lko__zkcm = fs.get_file_info(ksta__ueka)
            if lko__zkcm and lko__zkcm[0].path in [usldk__wqd, f'{usldk__wqd}/'
                ] and int(lko__zkcm[0].size or 0) == 0:
                lko__zkcm = lko__zkcm[1:]
            mnoob__tol = [bii__hqe.base_name for bii__hqe in lko__zkcm]
    except BodoError as sisih__gloh:
        raise
    except Exception as qbceb__xlekt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(qbceb__xlekt).__name__}: {str(qbceb__xlekt)}
{bodo_error_msg}"""
            )
    return mnoob__tol


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    tzt__kkd = urlparse(path)
    rqb__zlrg = tzt__kkd.path
    try:
        ekwz__juj = HadoopFileSystem.from_uri(path)
    except Exception as qbceb__xlekt:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            qbceb__xlekt))
    avycg__tltj = ekwz__juj.get_file_info([rqb__zlrg])
    if avycg__tltj[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not avycg__tltj[0].size and avycg__tltj[0].type == FileType.Directory:
        return ekwz__juj, True
    return ekwz__juj, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    mnoob__tol = None
    ekwz__juj, aeq__ebye = hdfs_is_directory(path)
    if aeq__ebye:
        tzt__kkd = urlparse(path)
        rqb__zlrg = tzt__kkd.path
        ksta__ueka = FileSelector(rqb__zlrg, recursive=True)
        try:
            lko__zkcm = ekwz__juj.get_file_info(ksta__ueka)
        except Exception as qbceb__xlekt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(rqb__zlrg, qbceb__xlekt))
        mnoob__tol = [bii__hqe.base_name for bii__hqe in lko__zkcm]
    return ekwz__juj, mnoob__tol


def abfs_is_directory(path):
    ekwz__juj = get_hdfs_fs(path)
    try:
        avycg__tltj = ekwz__juj.info(path)
    except OSError as sisih__gloh:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if avycg__tltj['size'] == 0 and avycg__tltj['kind'].lower() == 'directory':
        return ekwz__juj, True
    return ekwz__juj, False


def abfs_list_dir_fnames(path):
    mnoob__tol = None
    ekwz__juj, aeq__ebye = abfs_is_directory(path)
    if aeq__ebye:
        tzt__kkd = urlparse(path)
        rqb__zlrg = tzt__kkd.path
        try:
            ipr__svg = ekwz__juj.ls(rqb__zlrg)
        except Exception as qbceb__xlekt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(rqb__zlrg, qbceb__xlekt))
        mnoob__tol = [fname[fname.rindex('/') + 1:] for fname in ipr__svg]
    return ekwz__juj, mnoob__tol


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    xkrca__tfar = urlparse(path)
    fname = path
    fs = None
    jvxq__mvw = 'read_json' if ftype == 'json' else 'read_csv'
    puuhi__olctg = (
        f'pd.{jvxq__mvw}(): there is no {ftype} file in directory: {fname}')
    eejj__bkzoo = directory_of_files_common_filter
    if xkrca__tfar.scheme == 's3':
        sbhjn__ufgwb = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        sqrz__gfjm = s3_list_dir_fnames(fs, path)
        usldk__wqd = (xkrca__tfar.netloc + xkrca__tfar.path).rstrip('/')
        fname = usldk__wqd
        if sqrz__gfjm:
            sqrz__gfjm = [(usldk__wqd + '/' + kvb__xghap) for kvb__xghap in
                sorted(filter(eejj__bkzoo, sqrz__gfjm))]
            bccp__wgu = [kvb__xghap for kvb__xghap in sqrz__gfjm if int(fs.
                get_file_info(kvb__xghap).size or 0) > 0]
            if len(bccp__wgu) == 0:
                raise BodoError(puuhi__olctg)
            fname = bccp__wgu[0]
        qev__rqlui = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        nfq__fed = fs._open(fname)
    elif xkrca__tfar.scheme == 'hdfs':
        sbhjn__ufgwb = True
        fs, sqrz__gfjm = hdfs_list_dir_fnames(path)
        qev__rqlui = fs.get_file_info([xkrca__tfar.path])[0].size
        if sqrz__gfjm:
            path = path.rstrip('/')
            sqrz__gfjm = [(path + '/' + kvb__xghap) for kvb__xghap in
                sorted(filter(eejj__bkzoo, sqrz__gfjm))]
            bccp__wgu = [kvb__xghap for kvb__xghap in sqrz__gfjm if fs.
                get_file_info([urlparse(kvb__xghap).path])[0].size > 0]
            if len(bccp__wgu) == 0:
                raise BodoError(puuhi__olctg)
            fname = bccp__wgu[0]
            fname = urlparse(fname).path
            qev__rqlui = fs.get_file_info([fname])[0].size
        nfq__fed = fs.open_input_file(fname)
    elif xkrca__tfar.scheme in ('abfs', 'abfss'):
        sbhjn__ufgwb = True
        fs, sqrz__gfjm = abfs_list_dir_fnames(path)
        qev__rqlui = fs.info(fname)['size']
        if sqrz__gfjm:
            path = path.rstrip('/')
            sqrz__gfjm = [(path + '/' + kvb__xghap) for kvb__xghap in
                sorted(filter(eejj__bkzoo, sqrz__gfjm))]
            bccp__wgu = [kvb__xghap for kvb__xghap in sqrz__gfjm if fs.info
                (kvb__xghap)['size'] > 0]
            if len(bccp__wgu) == 0:
                raise BodoError(puuhi__olctg)
            fname = bccp__wgu[0]
            qev__rqlui = fs.info(fname)['size']
            fname = urlparse(fname).path
        nfq__fed = fs.open(fname, 'rb')
    else:
        if xkrca__tfar.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {xkrca__tfar.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        sbhjn__ufgwb = False
        if os.path.isdir(path):
            ipr__svg = filter(eejj__bkzoo, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            bccp__wgu = [kvb__xghap for kvb__xghap in sorted(ipr__svg) if 
                os.path.getsize(kvb__xghap) > 0]
            if len(bccp__wgu) == 0:
                raise BodoError(puuhi__olctg)
            fname = bccp__wgu[0]
        qev__rqlui = os.path.getsize(fname)
        nfq__fed = fname
    return sbhjn__ufgwb, nfq__fed, qev__rqlui, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    epzv__escz = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            vks__vua, kzwo__qmrr = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = vks__vua.region
        except Exception as qbceb__xlekt:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{qbceb__xlekt}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = epzv__escz.bcast(bucket_loc)
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
        shgg__lyy = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        sinrf__qcliw, lvd__pki = unicode_to_utf8_and_len(D)
        yfm__xrzym = 0
        if is_parallel:
            yfm__xrzym = bodo.libs.distributed_api.dist_exscan(lvd__pki, np
                .int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), sinrf__qcliw, yfm__xrzym,
            lvd__pki, is_parallel, unicode_to_utf8(shgg__lyy))
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
    jnb__lfgv = get_overload_constant_dict(storage_options)
    gtw__ywi = 'def impl(storage_options):\n'
    gtw__ywi += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    gtw__ywi += f'    storage_options_py = {str(jnb__lfgv)}\n'
    gtw__ywi += '  return storage_options_py\n'
    jmb__tecq = {}
    exec(gtw__ywi, globals(), jmb__tecq)
    return jmb__tecq['impl']
