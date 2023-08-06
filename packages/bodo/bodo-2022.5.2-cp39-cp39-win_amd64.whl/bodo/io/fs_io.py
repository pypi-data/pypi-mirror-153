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
            ieqyc__qhyei = self.fs.open_input_file(path)
        except:
            ieqyc__qhyei = self.fs.open_input_stream(path)
    elif mode == 'wb':
        ieqyc__qhyei = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, ieqyc__qhyei, path, mode, block_size, **kwargs)


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
    tae__ytefy = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    srk__hlwtw = False
    tdr__czbq = get_proxy_uri_from_env_vars()
    if storage_options:
        srk__hlwtw = storage_options.get('anon', False)
    return S3FileSystem(anonymous=srk__hlwtw, region=region,
        endpoint_override=tae__ytefy, proxy_options=tdr__czbq)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    tae__ytefy = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    srk__hlwtw = False
    tdr__czbq = get_proxy_uri_from_env_vars()
    if storage_options:
        srk__hlwtw = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=tae__ytefy,
        anonymous=srk__hlwtw, proxy_options=tdr__czbq)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    nloj__oigx = urlparse(path)
    if nloj__oigx.scheme in ('abfs', 'abfss'):
        pjhtt__lile = path
        if nloj__oigx.port is None:
            atll__uwydp = 0
        else:
            atll__uwydp = nloj__oigx.port
        lyj__iqddl = None
    else:
        pjhtt__lile = nloj__oigx.hostname
        atll__uwydp = nloj__oigx.port
        lyj__iqddl = nloj__oigx.username
    try:
        fs = HdFS(host=pjhtt__lile, port=atll__uwydp, user=lyj__iqddl)
    except Exception as gycb__gar:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            gycb__gar))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        vfs__aixf = fs.isdir(path)
    except gcsfs.utils.HttpError as gycb__gar:
        raise BodoError(
            f'{gycb__gar}. Make sure your google cloud credentials are set!')
    return vfs__aixf


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [yoe__hse.split('/')[-1] for yoe__hse in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        nloj__oigx = urlparse(path)
        axtul__rpnmq = (nloj__oigx.netloc + nloj__oigx.path).rstrip('/')
        dsbus__edswm = fs.get_file_info(axtul__rpnmq)
        if dsbus__edswm.type in (pa_fs.FileType.NotFound, pa_fs.FileType.
            Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not dsbus__edswm.size and dsbus__edswm.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as gycb__gar:
        raise
    except BodoError as hzpx__dyht:
        raise
    except Exception as gycb__gar:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(gycb__gar).__name__}: {str(gycb__gar)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    jzd__aibm = None
    try:
        if s3_is_directory(fs, path):
            nloj__oigx = urlparse(path)
            axtul__rpnmq = (nloj__oigx.netloc + nloj__oigx.path).rstrip('/')
            mlve__lgqz = pa_fs.FileSelector(axtul__rpnmq, recursive=False)
            kphla__wmpg = fs.get_file_info(mlve__lgqz)
            if kphla__wmpg and kphla__wmpg[0].path in [axtul__rpnmq,
                f'{axtul__rpnmq}/'] and int(kphla__wmpg[0].size or 0) == 0:
                kphla__wmpg = kphla__wmpg[1:]
            jzd__aibm = [ctkw__uvrzb.base_name for ctkw__uvrzb in kphla__wmpg]
    except BodoError as hzpx__dyht:
        raise
    except Exception as gycb__gar:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(gycb__gar).__name__}: {str(gycb__gar)}
{bodo_error_msg}"""
            )
    return jzd__aibm


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    nloj__oigx = urlparse(path)
    rwlz__xorx = nloj__oigx.path
    try:
        fdu__szv = HadoopFileSystem.from_uri(path)
    except Exception as gycb__gar:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            gycb__gar))
    doz__vqpiy = fdu__szv.get_file_info([rwlz__xorx])
    if doz__vqpiy[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not doz__vqpiy[0].size and doz__vqpiy[0].type == FileType.Directory:
        return fdu__szv, True
    return fdu__szv, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    jzd__aibm = None
    fdu__szv, vfs__aixf = hdfs_is_directory(path)
    if vfs__aixf:
        nloj__oigx = urlparse(path)
        rwlz__xorx = nloj__oigx.path
        mlve__lgqz = FileSelector(rwlz__xorx, recursive=True)
        try:
            kphla__wmpg = fdu__szv.get_file_info(mlve__lgqz)
        except Exception as gycb__gar:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(rwlz__xorx, gycb__gar))
        jzd__aibm = [ctkw__uvrzb.base_name for ctkw__uvrzb in kphla__wmpg]
    return fdu__szv, jzd__aibm


def abfs_is_directory(path):
    fdu__szv = get_hdfs_fs(path)
    try:
        doz__vqpiy = fdu__szv.info(path)
    except OSError as hzpx__dyht:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if doz__vqpiy['size'] == 0 and doz__vqpiy['kind'].lower() == 'directory':
        return fdu__szv, True
    return fdu__szv, False


def abfs_list_dir_fnames(path):
    jzd__aibm = None
    fdu__szv, vfs__aixf = abfs_is_directory(path)
    if vfs__aixf:
        nloj__oigx = urlparse(path)
        rwlz__xorx = nloj__oigx.path
        try:
            jtjqk__zpg = fdu__szv.ls(rwlz__xorx)
        except Exception as gycb__gar:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(rwlz__xorx, gycb__gar))
        jzd__aibm = [fname[fname.rindex('/') + 1:] for fname in jtjqk__zpg]
    return fdu__szv, jzd__aibm


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    ddcb__upkzy = urlparse(path)
    fname = path
    fs = None
    gwhf__trg = 'read_json' if ftype == 'json' else 'read_csv'
    goq__gaef = (
        f'pd.{gwhf__trg}(): there is no {ftype} file in directory: {fname}')
    rjh__nws = directory_of_files_common_filter
    if ddcb__upkzy.scheme == 's3':
        ingob__rmipf = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        wog__ddxw = s3_list_dir_fnames(fs, path)
        axtul__rpnmq = (ddcb__upkzy.netloc + ddcb__upkzy.path).rstrip('/')
        fname = axtul__rpnmq
        if wog__ddxw:
            wog__ddxw = [(axtul__rpnmq + '/' + yoe__hse) for yoe__hse in
                sorted(filter(rjh__nws, wog__ddxw))]
            sbvs__xip = [yoe__hse for yoe__hse in wog__ddxw if int(fs.
                get_file_info(yoe__hse).size or 0) > 0]
            if len(sbvs__xip) == 0:
                raise BodoError(goq__gaef)
            fname = sbvs__xip[0]
        ooh__fps = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        qdn__zycu = fs._open(fname)
    elif ddcb__upkzy.scheme == 'hdfs':
        ingob__rmipf = True
        fs, wog__ddxw = hdfs_list_dir_fnames(path)
        ooh__fps = fs.get_file_info([ddcb__upkzy.path])[0].size
        if wog__ddxw:
            path = path.rstrip('/')
            wog__ddxw = [(path + '/' + yoe__hse) for yoe__hse in sorted(
                filter(rjh__nws, wog__ddxw))]
            sbvs__xip = [yoe__hse for yoe__hse in wog__ddxw if fs.
                get_file_info([urlparse(yoe__hse).path])[0].size > 0]
            if len(sbvs__xip) == 0:
                raise BodoError(goq__gaef)
            fname = sbvs__xip[0]
            fname = urlparse(fname).path
            ooh__fps = fs.get_file_info([fname])[0].size
        qdn__zycu = fs.open_input_file(fname)
    elif ddcb__upkzy.scheme in ('abfs', 'abfss'):
        ingob__rmipf = True
        fs, wog__ddxw = abfs_list_dir_fnames(path)
        ooh__fps = fs.info(fname)['size']
        if wog__ddxw:
            path = path.rstrip('/')
            wog__ddxw = [(path + '/' + yoe__hse) for yoe__hse in sorted(
                filter(rjh__nws, wog__ddxw))]
            sbvs__xip = [yoe__hse for yoe__hse in wog__ddxw if fs.info(
                yoe__hse)['size'] > 0]
            if len(sbvs__xip) == 0:
                raise BodoError(goq__gaef)
            fname = sbvs__xip[0]
            ooh__fps = fs.info(fname)['size']
            fname = urlparse(fname).path
        qdn__zycu = fs.open(fname, 'rb')
    else:
        if ddcb__upkzy.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {ddcb__upkzy.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        ingob__rmipf = False
        if os.path.isdir(path):
            jtjqk__zpg = filter(rjh__nws, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            sbvs__xip = [yoe__hse for yoe__hse in sorted(jtjqk__zpg) if os.
                path.getsize(yoe__hse) > 0]
            if len(sbvs__xip) == 0:
                raise BodoError(goq__gaef)
            fname = sbvs__xip[0]
        ooh__fps = os.path.getsize(fname)
        qdn__zycu = fname
    return ingob__rmipf, qdn__zycu, ooh__fps, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    skvxo__jekjh = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            wqkq__kulz, klgc__dokfw = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = wqkq__kulz.region
        except Exception as gycb__gar:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{gycb__gar}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = skvxo__jekjh.bcast(bucket_loc)
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
        ookn__teyp = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        ullcc__xqe, wmbb__nwlco = unicode_to_utf8_and_len(D)
        xutnk__yihe = 0
        if is_parallel:
            xutnk__yihe = bodo.libs.distributed_api.dist_exscan(wmbb__nwlco,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), ullcc__xqe, xutnk__yihe,
            wmbb__nwlco, is_parallel, unicode_to_utf8(ookn__teyp))
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
    flcf__bqki = get_overload_constant_dict(storage_options)
    ruap__zfkh = 'def impl(storage_options):\n'
    ruap__zfkh += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    ruap__zfkh += f'    storage_options_py = {str(flcf__bqki)}\n'
    ruap__zfkh += '  return storage_options_py\n'
    tmp__mwlx = {}
    exec(ruap__zfkh, globals(), tmp__mwlx)
    return tmp__mwlx['impl']
