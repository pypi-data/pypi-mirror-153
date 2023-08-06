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
    irwub__pcgk = MPI.COMM_WORLD
    iype__crt = irwub__pcgk.Get_rank()
    ovnq__hvza = get_host_ranks()
    qthuv__yzk = get_nodes_first_ranks()
    if iype__crt in qthuv__yzk:
        try:
            jrpf__ztqbo = get_num_gpus(framework)
        except Exception as omyem__gbmub:
            jrpf__ztqbo = omyem__gbmub
        hlih__yzbu = create_subcomm_mpi4py(qthuv__yzk)
        xysd__jpt = hlih__yzbu.gather(jrpf__ztqbo)
        if iype__crt == 0:
            gpu_ranks = []
            gjgvm__kbpmu = None
            for dqpol__edc, iva__avqq in enumerate(ovnq__hvza.values()):
                dedlz__hsk = xysd__jpt[dqpol__edc]
                if isinstance(dedlz__hsk, Exception):
                    gjgvm__kbpmu = dedlz__hsk
                    break
                if dedlz__hsk == 0:
                    continue
                prmzr__irri = len(iva__avqq) // dedlz__hsk
                for wuzbn__cub, tjtx__kmphc in enumerate(iva__avqq):
                    if wuzbn__cub % prmzr__irri == 0:
                        wek__vyaya = wuzbn__cub / prmzr__irri
                        if wek__vyaya < dedlz__hsk:
                            gpu_ranks.append(tjtx__kmphc)
            if gjgvm__kbpmu:
                irwub__pcgk.bcast(gjgvm__kbpmu)
                raise gjgvm__kbpmu
            else:
                irwub__pcgk.bcast(gpu_ranks)
    if iype__crt != 0:
        gpu_ranks = irwub__pcgk.bcast(None)
        if isinstance(gpu_ranks, Exception):
            omyem__gbmub = gpu_ranks
            raise omyem__gbmub
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
    nuaf__sea = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        hlih__yzbu = MPI.COMM_WORLD.Split(color=0 if nuaf__sea in gpu_ranks
             else MPI.UNDEFINED, key=nuaf__sea)
        if hlih__yzbu != MPI.COMM_NULL:
            hvd.init(comm=hlih__yzbu)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                wtz__imm = tf.config.experimental.list_physical_devices('GPU')
                for cersf__nvj in wtz__imm:
                    tf.config.experimental.set_memory_growth(cersf__nvj, True)
                tf.config.experimental.set_visible_devices(wtz__imm[hvd.
                    local_rank()], 'GPU')
    else:
        if nuaf__sea == 0:
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
        kzf__wka = 17
        irwub__pcgk = MPI.COMM_WORLD
        ryik__gqzo = MPI.Get_processor_name()
        ebw__ijscv = get_host_ranks()[ryik__gqzo]
        assert_dl_initialized()
        if bodo.get_rank() == ebw__ijscv[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for iype__crt in ebw__ijscv[1:]:
                irwub__pcgk.isend(1, dest=iype__crt, tag=kzf__wka)
        else:
            while True:
                nirpa__iryd = MPI.Status()
                ghve__qjmmj = irwub__pcgk.Iprobe(MPI.ANY_SOURCE, MPI.
                    ANY_TAG, nirpa__iryd)
                if ghve__qjmmj:
                    assert nirpa__iryd.source == ebw__ijscv[0]
                    assert nirpa__iryd.tag == kzf__wka
                    irwub__pcgk.recv(source=0, tag=kzf__wka)
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
