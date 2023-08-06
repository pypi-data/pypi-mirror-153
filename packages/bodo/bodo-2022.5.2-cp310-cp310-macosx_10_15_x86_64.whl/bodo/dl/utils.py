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
    dcn__ubryv = MPI.COMM_WORLD
    krkf__nerh = dcn__ubryv.Get_rank()
    cwth__htl = get_host_ranks()
    ztyo__vnfpt = get_nodes_first_ranks()
    if krkf__nerh in ztyo__vnfpt:
        try:
            ewh__lqrgq = get_num_gpus(framework)
        except Exception as zjpy__dbywd:
            ewh__lqrgq = zjpy__dbywd
        yeds__tiwlb = create_subcomm_mpi4py(ztyo__vnfpt)
        hyl__pfgp = yeds__tiwlb.gather(ewh__lqrgq)
        if krkf__nerh == 0:
            gpu_ranks = []
            ixi__qbmwk = None
            for fpa__cdja, rzeh__csa in enumerate(cwth__htl.values()):
                ajj__eumo = hyl__pfgp[fpa__cdja]
                if isinstance(ajj__eumo, Exception):
                    ixi__qbmwk = ajj__eumo
                    break
                if ajj__eumo == 0:
                    continue
                dtowy__rpz = len(rzeh__csa) // ajj__eumo
                for maf__qdoze, cemas__oaxj in enumerate(rzeh__csa):
                    if maf__qdoze % dtowy__rpz == 0:
                        ato__vntbo = maf__qdoze / dtowy__rpz
                        if ato__vntbo < ajj__eumo:
                            gpu_ranks.append(cemas__oaxj)
            if ixi__qbmwk:
                dcn__ubryv.bcast(ixi__qbmwk)
                raise ixi__qbmwk
            else:
                dcn__ubryv.bcast(gpu_ranks)
    if krkf__nerh != 0:
        gpu_ranks = dcn__ubryv.bcast(None)
        if isinstance(gpu_ranks, Exception):
            zjpy__dbywd = gpu_ranks
            raise zjpy__dbywd
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
    euch__ldrz = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        yeds__tiwlb = MPI.COMM_WORLD.Split(color=0 if euch__ldrz in
            gpu_ranks else MPI.UNDEFINED, key=euch__ldrz)
        if yeds__tiwlb != MPI.COMM_NULL:
            hvd.init(comm=yeds__tiwlb)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                hyt__ynj = tf.config.experimental.list_physical_devices('GPU')
                for lajs__vfmxh in hyt__ynj:
                    tf.config.experimental.set_memory_growth(lajs__vfmxh, True)
                tf.config.experimental.set_visible_devices(hyt__ynj[hvd.
                    local_rank()], 'GPU')
    else:
        if euch__ldrz == 0:
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
        prcao__wjm = 17
        dcn__ubryv = MPI.COMM_WORLD
        fwzfu__okyw = MPI.Get_processor_name()
        vxbp__joqzv = get_host_ranks()[fwzfu__okyw]
        assert_dl_initialized()
        if bodo.get_rank() == vxbp__joqzv[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for krkf__nerh in vxbp__joqzv[1:]:
                dcn__ubryv.isend(1, dest=krkf__nerh, tag=prcao__wjm)
        else:
            while True:
                kxc__toqfi = MPI.Status()
                qld__nrrq = dcn__ubryv.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    kxc__toqfi)
                if qld__nrrq:
                    assert kxc__toqfi.source == vxbp__joqzv[0]
                    assert kxc__toqfi.tag == prcao__wjm
                    dcn__ubryv.recv(source=0, tag=prcao__wjm)
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
