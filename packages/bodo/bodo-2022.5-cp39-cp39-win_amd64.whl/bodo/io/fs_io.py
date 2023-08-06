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
            mgvcm__tfg = self.fs.open_input_file(path)
        except:
            mgvcm__tfg = self.fs.open_input_stream(path)
    elif mode == 'wb':
        mgvcm__tfg = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, mgvcm__tfg, path, mode, block_size, **kwargs)


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
    gzjl__crkb = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    rjvpz__cafa = False
    yfpdo__tfwro = get_proxy_uri_from_env_vars()
    if storage_options:
        rjvpz__cafa = storage_options.get('anon', False)
    return S3FileSystem(anonymous=rjvpz__cafa, region=region,
        endpoint_override=gzjl__crkb, proxy_options=yfpdo__tfwro)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    gzjl__crkb = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    rjvpz__cafa = False
    yfpdo__tfwro = get_proxy_uri_from_env_vars()
    if storage_options:
        rjvpz__cafa = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=gzjl__crkb,
        anonymous=rjvpz__cafa, proxy_options=yfpdo__tfwro)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    mnivo__lnedq = urlparse(path)
    if mnivo__lnedq.scheme in ('abfs', 'abfss'):
        fdn__osnyi = path
        if mnivo__lnedq.port is None:
            ptd__oece = 0
        else:
            ptd__oece = mnivo__lnedq.port
        oddne__squcy = None
    else:
        fdn__osnyi = mnivo__lnedq.hostname
        ptd__oece = mnivo__lnedq.port
        oddne__squcy = mnivo__lnedq.username
    try:
        fs = HdFS(host=fdn__osnyi, port=ptd__oece, user=oddne__squcy)
    except Exception as wmwt__gqt:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            wmwt__gqt))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        yuz__cwyc = fs.isdir(path)
    except gcsfs.utils.HttpError as wmwt__gqt:
        raise BodoError(
            f'{wmwt__gqt}. Make sure your google cloud credentials are set!')
    return yuz__cwyc


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [copp__yvxpo.split('/')[-1] for copp__yvxpo in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        mnivo__lnedq = urlparse(path)
        rhp__xhdtf = (mnivo__lnedq.netloc + mnivo__lnedq.path).rstrip('/')
        dwj__cgcm = fs.get_file_info(rhp__xhdtf)
        if dwj__cgcm.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not dwj__cgcm.size and dwj__cgcm.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as wmwt__gqt:
        raise
    except BodoError as don__jltwy:
        raise
    except Exception as wmwt__gqt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(wmwt__gqt).__name__}: {str(wmwt__gqt)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    sebfh__rzvyn = None
    try:
        if s3_is_directory(fs, path):
            mnivo__lnedq = urlparse(path)
            rhp__xhdtf = (mnivo__lnedq.netloc + mnivo__lnedq.path).rstrip('/')
            hbozd__cmzm = pa_fs.FileSelector(rhp__xhdtf, recursive=False)
            iijhw__eukbw = fs.get_file_info(hbozd__cmzm)
            if iijhw__eukbw and iijhw__eukbw[0].path in [rhp__xhdtf,
                f'{rhp__xhdtf}/'] and int(iijhw__eukbw[0].size or 0) == 0:
                iijhw__eukbw = iijhw__eukbw[1:]
            sebfh__rzvyn = [jhfc__ontb.base_name for jhfc__ontb in iijhw__eukbw
                ]
    except BodoError as don__jltwy:
        raise
    except Exception as wmwt__gqt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(wmwt__gqt).__name__}: {str(wmwt__gqt)}
{bodo_error_msg}"""
            )
    return sebfh__rzvyn


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    mnivo__lnedq = urlparse(path)
    qnk__zsrlw = mnivo__lnedq.path
    try:
        ygo__ranms = HadoopFileSystem.from_uri(path)
    except Exception as wmwt__gqt:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            wmwt__gqt))
    hsrbl__ptxa = ygo__ranms.get_file_info([qnk__zsrlw])
    if hsrbl__ptxa[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not hsrbl__ptxa[0].size and hsrbl__ptxa[0].type == FileType.Directory:
        return ygo__ranms, True
    return ygo__ranms, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    sebfh__rzvyn = None
    ygo__ranms, yuz__cwyc = hdfs_is_directory(path)
    if yuz__cwyc:
        mnivo__lnedq = urlparse(path)
        qnk__zsrlw = mnivo__lnedq.path
        hbozd__cmzm = FileSelector(qnk__zsrlw, recursive=True)
        try:
            iijhw__eukbw = ygo__ranms.get_file_info(hbozd__cmzm)
        except Exception as wmwt__gqt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(qnk__zsrlw, wmwt__gqt))
        sebfh__rzvyn = [jhfc__ontb.base_name for jhfc__ontb in iijhw__eukbw]
    return ygo__ranms, sebfh__rzvyn


def abfs_is_directory(path):
    ygo__ranms = get_hdfs_fs(path)
    try:
        hsrbl__ptxa = ygo__ranms.info(path)
    except OSError as don__jltwy:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if hsrbl__ptxa['size'] == 0 and hsrbl__ptxa['kind'].lower() == 'directory':
        return ygo__ranms, True
    return ygo__ranms, False


def abfs_list_dir_fnames(path):
    sebfh__rzvyn = None
    ygo__ranms, yuz__cwyc = abfs_is_directory(path)
    if yuz__cwyc:
        mnivo__lnedq = urlparse(path)
        qnk__zsrlw = mnivo__lnedq.path
        try:
            gaez__qjt = ygo__ranms.ls(qnk__zsrlw)
        except Exception as wmwt__gqt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(qnk__zsrlw, wmwt__gqt))
        sebfh__rzvyn = [fname[fname.rindex('/') + 1:] for fname in gaez__qjt]
    return ygo__ranms, sebfh__rzvyn


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    scrpm__xkek = urlparse(path)
    fname = path
    fs = None
    ewf__jxiqo = 'read_json' if ftype == 'json' else 'read_csv'
    edigg__utv = (
        f'pd.{ewf__jxiqo}(): there is no {ftype} file in directory: {fname}')
    lft__prlhr = directory_of_files_common_filter
    if scrpm__xkek.scheme == 's3':
        socz__kia = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        rkwhu__vcx = s3_list_dir_fnames(fs, path)
        rhp__xhdtf = (scrpm__xkek.netloc + scrpm__xkek.path).rstrip('/')
        fname = rhp__xhdtf
        if rkwhu__vcx:
            rkwhu__vcx = [(rhp__xhdtf + '/' + copp__yvxpo) for copp__yvxpo in
                sorted(filter(lft__prlhr, rkwhu__vcx))]
            yvit__abce = [copp__yvxpo for copp__yvxpo in rkwhu__vcx if int(
                fs.get_file_info(copp__yvxpo).size or 0) > 0]
            if len(yvit__abce) == 0:
                raise BodoError(edigg__utv)
            fname = yvit__abce[0]
        fknl__swd = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        fudxc__xac = fs._open(fname)
    elif scrpm__xkek.scheme == 'hdfs':
        socz__kia = True
        fs, rkwhu__vcx = hdfs_list_dir_fnames(path)
        fknl__swd = fs.get_file_info([scrpm__xkek.path])[0].size
        if rkwhu__vcx:
            path = path.rstrip('/')
            rkwhu__vcx = [(path + '/' + copp__yvxpo) for copp__yvxpo in
                sorted(filter(lft__prlhr, rkwhu__vcx))]
            yvit__abce = [copp__yvxpo for copp__yvxpo in rkwhu__vcx if fs.
                get_file_info([urlparse(copp__yvxpo).path])[0].size > 0]
            if len(yvit__abce) == 0:
                raise BodoError(edigg__utv)
            fname = yvit__abce[0]
            fname = urlparse(fname).path
            fknl__swd = fs.get_file_info([fname])[0].size
        fudxc__xac = fs.open_input_file(fname)
    elif scrpm__xkek.scheme in ('abfs', 'abfss'):
        socz__kia = True
        fs, rkwhu__vcx = abfs_list_dir_fnames(path)
        fknl__swd = fs.info(fname)['size']
        if rkwhu__vcx:
            path = path.rstrip('/')
            rkwhu__vcx = [(path + '/' + copp__yvxpo) for copp__yvxpo in
                sorted(filter(lft__prlhr, rkwhu__vcx))]
            yvit__abce = [copp__yvxpo for copp__yvxpo in rkwhu__vcx if fs.
                info(copp__yvxpo)['size'] > 0]
            if len(yvit__abce) == 0:
                raise BodoError(edigg__utv)
            fname = yvit__abce[0]
            fknl__swd = fs.info(fname)['size']
            fname = urlparse(fname).path
        fudxc__xac = fs.open(fname, 'rb')
    else:
        if scrpm__xkek.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {scrpm__xkek.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        socz__kia = False
        if os.path.isdir(path):
            gaez__qjt = filter(lft__prlhr, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            yvit__abce = [copp__yvxpo for copp__yvxpo in sorted(gaez__qjt) if
                os.path.getsize(copp__yvxpo) > 0]
            if len(yvit__abce) == 0:
                raise BodoError(edigg__utv)
            fname = yvit__abce[0]
        fknl__swd = os.path.getsize(fname)
        fudxc__xac = fname
    return socz__kia, fudxc__xac, fknl__swd, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    dpqu__ahdfc = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            joptw__wtqi, qelcb__oxi = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = joptw__wtqi.region
        except Exception as wmwt__gqt:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{wmwt__gqt}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = dpqu__ahdfc.bcast(bucket_loc)
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
        hft__yfq = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel)
        qabd__unf, ncnvb__sccii = unicode_to_utf8_and_len(D)
        rpbd__wmdqp = 0
        if is_parallel:
            rpbd__wmdqp = bodo.libs.distributed_api.dist_exscan(ncnvb__sccii,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), qabd__unf, rpbd__wmdqp,
            ncnvb__sccii, is_parallel, unicode_to_utf8(hft__yfq))
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
    xwa__qcsly = get_overload_constant_dict(storage_options)
    ngxbr__dck = 'def impl(storage_options):\n'
    ngxbr__dck += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    ngxbr__dck += f'    storage_options_py = {str(xwa__qcsly)}\n'
    ngxbr__dck += '  return storage_options_py\n'
    iywwt__lhp = {}
    exec(ngxbr__dck, globals(), iywwt__lhp)
    return iywwt__lhp['impl']
