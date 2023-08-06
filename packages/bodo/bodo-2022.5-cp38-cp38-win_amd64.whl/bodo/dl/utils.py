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
    kqknk__ypnsw = MPI.COMM_WORLD
    cktgr__wqhvl = kqknk__ypnsw.Get_rank()
    nvypx__vao = get_host_ranks()
    ekx__qffd = get_nodes_first_ranks()
    if cktgr__wqhvl in ekx__qffd:
        try:
            fwle__ccey = get_num_gpus(framework)
        except Exception as cjyfv__pjt:
            fwle__ccey = cjyfv__pjt
        uyuta__lkzzg = create_subcomm_mpi4py(ekx__qffd)
        mbg__tus = uyuta__lkzzg.gather(fwle__ccey)
        if cktgr__wqhvl == 0:
            gpu_ranks = []
            zbays__ijog = None
            for ojn__qfh, wll__lie in enumerate(nvypx__vao.values()):
                kzmlz__jdr = mbg__tus[ojn__qfh]
                if isinstance(kzmlz__jdr, Exception):
                    zbays__ijog = kzmlz__jdr
                    break
                if kzmlz__jdr == 0:
                    continue
                leml__kwu = len(wll__lie) // kzmlz__jdr
                for ulqs__znnck, xpk__kuya in enumerate(wll__lie):
                    if ulqs__znnck % leml__kwu == 0:
                        gyy__wsbf = ulqs__znnck / leml__kwu
                        if gyy__wsbf < kzmlz__jdr:
                            gpu_ranks.append(xpk__kuya)
            if zbays__ijog:
                kqknk__ypnsw.bcast(zbays__ijog)
                raise zbays__ijog
            else:
                kqknk__ypnsw.bcast(gpu_ranks)
    if cktgr__wqhvl != 0:
        gpu_ranks = kqknk__ypnsw.bcast(None)
        if isinstance(gpu_ranks, Exception):
            cjyfv__pjt = gpu_ranks
            raise cjyfv__pjt
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
    dorjf__asp = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        uyuta__lkzzg = MPI.COMM_WORLD.Split(color=0 if dorjf__asp in
            gpu_ranks else MPI.UNDEFINED, key=dorjf__asp)
        if uyuta__lkzzg != MPI.COMM_NULL:
            hvd.init(comm=uyuta__lkzzg)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                ajyk__oomwk = tf.config.experimental.list_physical_devices(
                    'GPU')
                for oaudz__relsn in ajyk__oomwk:
                    tf.config.experimental.set_memory_growth(oaudz__relsn, True
                        )
                tf.config.experimental.set_visible_devices(ajyk__oomwk[hvd.
                    local_rank()], 'GPU')
    else:
        if dorjf__asp == 0:
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
        dpo__qrkll = 17
        kqknk__ypnsw = MPI.COMM_WORLD
        ide__tbyvi = MPI.Get_processor_name()
        hor__rqr = get_host_ranks()[ide__tbyvi]
        assert_dl_initialized()
        if bodo.get_rank() == hor__rqr[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for cktgr__wqhvl in hor__rqr[1:]:
                kqknk__ypnsw.isend(1, dest=cktgr__wqhvl, tag=dpo__qrkll)
        else:
            while True:
                wxd__nnyv = MPI.Status()
                eknm__maz = kqknk__ypnsw.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    wxd__nnyv)
                if eknm__maz:
                    assert wxd__nnyv.source == hor__rqr[0]
                    assert wxd__nnyv.tag == dpo__qrkll
                    kqknk__ypnsw.recv(source=0, tag=dpo__qrkll)
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
