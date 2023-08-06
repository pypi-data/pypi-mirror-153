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
            xahqq__lmew = self.fs.open_input_file(path)
        except:
            xahqq__lmew = self.fs.open_input_stream(path)
    elif mode == 'wb':
        xahqq__lmew = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, xahqq__lmew, path, mode, block_size, **kwargs)


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
    lwhc__ldf = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    jbp__yoq = False
    jhh__jstpg = get_proxy_uri_from_env_vars()
    if storage_options:
        jbp__yoq = storage_options.get('anon', False)
    return S3FileSystem(anonymous=jbp__yoq, region=region,
        endpoint_override=lwhc__ldf, proxy_options=jhh__jstpg)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    lwhc__ldf = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    jbp__yoq = False
    jhh__jstpg = get_proxy_uri_from_env_vars()
    if storage_options:
        jbp__yoq = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=lwhc__ldf, anonymous
        =jbp__yoq, proxy_options=jhh__jstpg)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    zvrl__zimkl = urlparse(path)
    if zvrl__zimkl.scheme in ('abfs', 'abfss'):
        qfyjo__xbip = path
        if zvrl__zimkl.port is None:
            rrc__lka = 0
        else:
            rrc__lka = zvrl__zimkl.port
        yija__enemf = None
    else:
        qfyjo__xbip = zvrl__zimkl.hostname
        rrc__lka = zvrl__zimkl.port
        yija__enemf = zvrl__zimkl.username
    try:
        fs = HdFS(host=qfyjo__xbip, port=rrc__lka, user=yija__enemf)
    except Exception as yvd__dhaks:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            yvd__dhaks))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        awbk__cfa = fs.isdir(path)
    except gcsfs.utils.HttpError as yvd__dhaks:
        raise BodoError(
            f'{yvd__dhaks}. Make sure your google cloud credentials are set!')
    return awbk__cfa


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [ovqk__ahrvq.split('/')[-1] for ovqk__ahrvq in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        zvrl__zimkl = urlparse(path)
        fht__icvu = (zvrl__zimkl.netloc + zvrl__zimkl.path).rstrip('/')
        mnd__txwdf = fs.get_file_info(fht__icvu)
        if mnd__txwdf.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not mnd__txwdf.size and mnd__txwdf.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as yvd__dhaks:
        raise
    except BodoError as mep__mpp:
        raise
    except Exception as yvd__dhaks:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(yvd__dhaks).__name__}: {str(yvd__dhaks)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    blw__tdatv = None
    try:
        if s3_is_directory(fs, path):
            zvrl__zimkl = urlparse(path)
            fht__icvu = (zvrl__zimkl.netloc + zvrl__zimkl.path).rstrip('/')
            yddyw__tto = pa_fs.FileSelector(fht__icvu, recursive=False)
            wqqxs__wrzit = fs.get_file_info(yddyw__tto)
            if wqqxs__wrzit and wqqxs__wrzit[0].path in [fht__icvu,
                f'{fht__icvu}/'] and int(wqqxs__wrzit[0].size or 0) == 0:
                wqqxs__wrzit = wqqxs__wrzit[1:]
            blw__tdatv = [yau__lfif.base_name for yau__lfif in wqqxs__wrzit]
    except BodoError as mep__mpp:
        raise
    except Exception as yvd__dhaks:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(yvd__dhaks).__name__}: {str(yvd__dhaks)}
{bodo_error_msg}"""
            )
    return blw__tdatv


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    zvrl__zimkl = urlparse(path)
    ndr__uugjv = zvrl__zimkl.path
    try:
        cfou__zom = HadoopFileSystem.from_uri(path)
    except Exception as yvd__dhaks:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            yvd__dhaks))
    tohko__bzqh = cfou__zom.get_file_info([ndr__uugjv])
    if tohko__bzqh[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not tohko__bzqh[0].size and tohko__bzqh[0].type == FileType.Directory:
        return cfou__zom, True
    return cfou__zom, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    blw__tdatv = None
    cfou__zom, awbk__cfa = hdfs_is_directory(path)
    if awbk__cfa:
        zvrl__zimkl = urlparse(path)
        ndr__uugjv = zvrl__zimkl.path
        yddyw__tto = FileSelector(ndr__uugjv, recursive=True)
        try:
            wqqxs__wrzit = cfou__zom.get_file_info(yddyw__tto)
        except Exception as yvd__dhaks:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(ndr__uugjv, yvd__dhaks))
        blw__tdatv = [yau__lfif.base_name for yau__lfif in wqqxs__wrzit]
    return cfou__zom, blw__tdatv


def abfs_is_directory(path):
    cfou__zom = get_hdfs_fs(path)
    try:
        tohko__bzqh = cfou__zom.info(path)
    except OSError as mep__mpp:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if tohko__bzqh['size'] == 0 and tohko__bzqh['kind'].lower() == 'directory':
        return cfou__zom, True
    return cfou__zom, False


def abfs_list_dir_fnames(path):
    blw__tdatv = None
    cfou__zom, awbk__cfa = abfs_is_directory(path)
    if awbk__cfa:
        zvrl__zimkl = urlparse(path)
        ndr__uugjv = zvrl__zimkl.path
        try:
            wuh__ixadc = cfou__zom.ls(ndr__uugjv)
        except Exception as yvd__dhaks:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(ndr__uugjv, yvd__dhaks))
        blw__tdatv = [fname[fname.rindex('/') + 1:] for fname in wuh__ixadc]
    return cfou__zom, blw__tdatv


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    duxr__vgjrd = urlparse(path)
    fname = path
    fs = None
    weppx__jfogg = 'read_json' if ftype == 'json' else 'read_csv'
    lfjr__djfsx = (
        f'pd.{weppx__jfogg}(): there is no {ftype} file in directory: {fname}')
    eli__war = directory_of_files_common_filter
    if duxr__vgjrd.scheme == 's3':
        rrjh__kcpkl = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        xkvkw__hamy = s3_list_dir_fnames(fs, path)
        fht__icvu = (duxr__vgjrd.netloc + duxr__vgjrd.path).rstrip('/')
        fname = fht__icvu
        if xkvkw__hamy:
            xkvkw__hamy = [(fht__icvu + '/' + ovqk__ahrvq) for ovqk__ahrvq in
                sorted(filter(eli__war, xkvkw__hamy))]
            dmesq__dko = [ovqk__ahrvq for ovqk__ahrvq in xkvkw__hamy if int
                (fs.get_file_info(ovqk__ahrvq).size or 0) > 0]
            if len(dmesq__dko) == 0:
                raise BodoError(lfjr__djfsx)
            fname = dmesq__dko[0]
        zli__rvaj = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        oxx__kavk = fs._open(fname)
    elif duxr__vgjrd.scheme == 'hdfs':
        rrjh__kcpkl = True
        fs, xkvkw__hamy = hdfs_list_dir_fnames(path)
        zli__rvaj = fs.get_file_info([duxr__vgjrd.path])[0].size
        if xkvkw__hamy:
            path = path.rstrip('/')
            xkvkw__hamy = [(path + '/' + ovqk__ahrvq) for ovqk__ahrvq in
                sorted(filter(eli__war, xkvkw__hamy))]
            dmesq__dko = [ovqk__ahrvq for ovqk__ahrvq in xkvkw__hamy if fs.
                get_file_info([urlparse(ovqk__ahrvq).path])[0].size > 0]
            if len(dmesq__dko) == 0:
                raise BodoError(lfjr__djfsx)
            fname = dmesq__dko[0]
            fname = urlparse(fname).path
            zli__rvaj = fs.get_file_info([fname])[0].size
        oxx__kavk = fs.open_input_file(fname)
    elif duxr__vgjrd.scheme in ('abfs', 'abfss'):
        rrjh__kcpkl = True
        fs, xkvkw__hamy = abfs_list_dir_fnames(path)
        zli__rvaj = fs.info(fname)['size']
        if xkvkw__hamy:
            path = path.rstrip('/')
            xkvkw__hamy = [(path + '/' + ovqk__ahrvq) for ovqk__ahrvq in
                sorted(filter(eli__war, xkvkw__hamy))]
            dmesq__dko = [ovqk__ahrvq for ovqk__ahrvq in xkvkw__hamy if fs.
                info(ovqk__ahrvq)['size'] > 0]
            if len(dmesq__dko) == 0:
                raise BodoError(lfjr__djfsx)
            fname = dmesq__dko[0]
            zli__rvaj = fs.info(fname)['size']
            fname = urlparse(fname).path
        oxx__kavk = fs.open(fname, 'rb')
    else:
        if duxr__vgjrd.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {duxr__vgjrd.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        rrjh__kcpkl = False
        if os.path.isdir(path):
            wuh__ixadc = filter(eli__war, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            dmesq__dko = [ovqk__ahrvq for ovqk__ahrvq in sorted(wuh__ixadc) if
                os.path.getsize(ovqk__ahrvq) > 0]
            if len(dmesq__dko) == 0:
                raise BodoError(lfjr__djfsx)
            fname = dmesq__dko[0]
        zli__rvaj = os.path.getsize(fname)
        oxx__kavk = fname
    return rrjh__kcpkl, oxx__kavk, zli__rvaj, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    fuuad__irn = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            gate__anac, mzd__iab = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = gate__anac.region
        except Exception as yvd__dhaks:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{yvd__dhaks}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = fuuad__irn.bcast(bucket_loc)
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
        xou__vcmle = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        gnu__mrqy, xcy__habn = unicode_to_utf8_and_len(D)
        ejgo__gycr = 0
        if is_parallel:
            ejgo__gycr = bodo.libs.distributed_api.dist_exscan(xcy__habn,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), gnu__mrqy, ejgo__gycr,
            xcy__habn, is_parallel, unicode_to_utf8(xou__vcmle))
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
    zocvx__cqbgi = get_overload_constant_dict(storage_options)
    hnslk__pmbdx = 'def impl(storage_options):\n'
    hnslk__pmbdx += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    hnslk__pmbdx += f'    storage_options_py = {str(zocvx__cqbgi)}\n'
    hnslk__pmbdx += '  return storage_options_py\n'
    xxv__neemo = {}
    exec(hnslk__pmbdx, globals(), xxv__neemo)
    return xxv__neemo['impl']
