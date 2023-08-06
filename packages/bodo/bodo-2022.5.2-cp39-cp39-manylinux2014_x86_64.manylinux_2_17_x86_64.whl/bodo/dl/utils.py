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
    qfm__tjdnn = MPI.COMM_WORLD
    zocs__aic = qfm__tjdnn.Get_rank()
    kcnls__mcpn = get_host_ranks()
    tdn__xibzc = get_nodes_first_ranks()
    if zocs__aic in tdn__xibzc:
        try:
            xqn__coxbj = get_num_gpus(framework)
        except Exception as ark__wfcfq:
            xqn__coxbj = ark__wfcfq
        wqn__ohhp = create_subcomm_mpi4py(tdn__xibzc)
        nwb__qplre = wqn__ohhp.gather(xqn__coxbj)
        if zocs__aic == 0:
            gpu_ranks = []
            gakas__xobox = None
            for awvx__dch, cjck__vtyp in enumerate(kcnls__mcpn.values()):
                tchz__cakn = nwb__qplre[awvx__dch]
                if isinstance(tchz__cakn, Exception):
                    gakas__xobox = tchz__cakn
                    break
                if tchz__cakn == 0:
                    continue
                rqw__nqcio = len(cjck__vtyp) // tchz__cakn
                for obnrc__kxu, gesjw__mae in enumerate(cjck__vtyp):
                    if obnrc__kxu % rqw__nqcio == 0:
                        nibo__qlt = obnrc__kxu / rqw__nqcio
                        if nibo__qlt < tchz__cakn:
                            gpu_ranks.append(gesjw__mae)
            if gakas__xobox:
                qfm__tjdnn.bcast(gakas__xobox)
                raise gakas__xobox
            else:
                qfm__tjdnn.bcast(gpu_ranks)
    if zocs__aic != 0:
        gpu_ranks = qfm__tjdnn.bcast(None)
        if isinstance(gpu_ranks, Exception):
            ark__wfcfq = gpu_ranks
            raise ark__wfcfq
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
    mjh__utxwg = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        wqn__ohhp = MPI.COMM_WORLD.Split(color=0 if mjh__utxwg in gpu_ranks
             else MPI.UNDEFINED, key=mjh__utxwg)
        if wqn__ohhp != MPI.COMM_NULL:
            hvd.init(comm=wqn__ohhp)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                vqvua__mryj = tf.config.experimental.list_physical_devices(
                    'GPU')
                for dkf__bozw in vqvua__mryj:
                    tf.config.experimental.set_memory_growth(dkf__bozw, True)
                tf.config.experimental.set_visible_devices(vqvua__mryj[hvd.
                    local_rank()], 'GPU')
    else:
        if mjh__utxwg == 0:
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
        zry__njk = 17
        qfm__tjdnn = MPI.COMM_WORLD
        wwaq__xclvu = MPI.Get_processor_name()
        egos__bbe = get_host_ranks()[wwaq__xclvu]
        assert_dl_initialized()
        if bodo.get_rank() == egos__bbe[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for zocs__aic in egos__bbe[1:]:
                qfm__tjdnn.isend(1, dest=zocs__aic, tag=zry__njk)
        else:
            while True:
                pkpk__isdoy = MPI.Status()
                dii__ucc = qfm__tjdnn.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    pkpk__isdoy)
                if dii__ucc:
                    assert pkpk__isdoy.source == egos__bbe[0]
                    assert pkpk__isdoy.tag == zry__njk
                    qfm__tjdnn.recv(source=0, tag=zry__njk)
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
