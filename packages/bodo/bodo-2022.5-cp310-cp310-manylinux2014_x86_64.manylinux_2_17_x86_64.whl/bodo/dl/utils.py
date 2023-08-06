"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    ddeek__itk = MPI.COMM_WORLD
    coo__mzpmm = ddeek__itk.Get_rank()
    ftb__gnub = get_host_ranks()
    abeb__eengw = get_nodes_first_ranks()
    if coo__mzpmm in abeb__eengw:
        try:
            vad__zso = get_num_gpus(framework)
        except Exception as adaaw__zozay:
            vad__zso = adaaw__zozay
        ztfv__yxf = create_subcomm_mpi4py(abeb__eengw)
        oelhf__vlhne = ztfv__yxf.gather(vad__zso)
        if coo__mzpmm == 0:
            gpu_ranks = []
            mslkz__tov = None
            for mpxj__ygsqa, zlq__hvth in enumerate(ftb__gnub.values()):
                kmyzp__xmvw = oelhf__vlhne[mpxj__ygsqa]
                if isinstance(kmyzp__xmvw, Exception):
                    mslkz__tov = kmyzp__xmvw
                    break
                if kmyzp__xmvw == 0:
                    continue
                wpg__sdzw = len(zlq__hvth) // kmyzp__xmvw
                for bwds__syhhm, pzec__zdns in enumerate(zlq__hvth):
                    if bwds__syhhm % wpg__sdzw == 0:
                        gpj__hoxit = bwds__syhhm / wpg__sdzw
                        if gpj__hoxit < kmyzp__xmvw:
                            gpu_ranks.append(pzec__zdns)
            if mslkz__tov:
                ddeek__itk.bcast(mslkz__tov)
                raise mslkz__tov
            else:
                ddeek__itk.bcast(gpu_ranks)
    if coo__mzpmm != 0:
        gpu_ranks = ddeek__itk.bcast(None)
        if isinstance(gpu_ranks, Exception):
            adaaw__zozay = gpu_ranks
            raise adaaw__zozay
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    igs__misrm = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        ztfv__yxf = MPI.COMM_WORLD.Split(color=0 if igs__misrm in gpu_ranks
             else MPI.UNDEFINED, key=igs__misrm)
        if ztfv__yxf != MPI.COMM_NULL:
            hvd.init(comm=ztfv__yxf)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                oscd__ykuxh = tf.config.experimental.list_physical_devices(
                    'GPU')
                for nhck__wxw in oscd__ykuxh:
                    tf.config.experimental.set_memory_growth(nhck__wxw, True)
                tf.config.experimental.set_visible_devices(oscd__ykuxh[hvd.
                    local_rank()], 'GPU')
    else:
        if igs__misrm == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        puby__kwngt = 17
        ddeek__itk = MPI.COMM_WORLD
        nxfzv__qjsri = MPI.Get_processor_name()
        cgqtx__gzgzs = get_host_ranks()[nxfzv__qjsri]
        assert_dl_initialized()
        if bodo.get_rank() == cgqtx__gzgzs[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for coo__mzpmm in cgqtx__gzgzs[1:]:
                ddeek__itk.isend(1, dest=coo__mzpmm, tag=puby__kwngt)
        else:
            while True:
                txthl__cih = MPI.Status()
                ggw__dwy = ddeek__itk.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    txthl__cih)
                if ggw__dwy:
                    assert txthl__cih.source == cgqtx__gzgzs[0]
                    assert txthl__cih.tag == puby__kwngt
                    ddeek__itk.recv(source=0, tag=puby__kwngt)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
