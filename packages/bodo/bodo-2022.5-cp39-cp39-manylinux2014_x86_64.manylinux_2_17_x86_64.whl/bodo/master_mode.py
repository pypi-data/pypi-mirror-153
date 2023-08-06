import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        pyk__rpyel = state
        vus__mjav = inspect.getsourcelines(pyk__rpyel)[0][0]
        assert vus__mjav.startswith('@bodo.jit') or vus__mjav.startswith('@jit'
            )
        cnhg__rauq = eval(vus__mjav[1:])
        self.dispatcher = cnhg__rauq(pyk__rpyel)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    dhzda__firaa = MPI.COMM_WORLD
    while True:
        jff__ywwd = dhzda__firaa.bcast(None, root=MASTER_RANK)
        if jff__ywwd[0] == 'exec':
            pyk__rpyel = pickle.loads(jff__ywwd[1])
            for lpel__wgkkp, xpuz__gck in list(pyk__rpyel.__globals__.items()):
                if isinstance(xpuz__gck, MasterModeDispatcher):
                    pyk__rpyel.__globals__[lpel__wgkkp] = xpuz__gck.dispatcher
            if pyk__rpyel.__module__ not in sys.modules:
                sys.modules[pyk__rpyel.__module__] = pytypes.ModuleType(
                    pyk__rpyel.__module__)
            vus__mjav = inspect.getsourcelines(pyk__rpyel)[0][0]
            assert vus__mjav.startswith('@bodo.jit') or vus__mjav.startswith(
                '@jit')
            cnhg__rauq = eval(vus__mjav[1:])
            func = cnhg__rauq(pyk__rpyel)
            rpo__ohit = jff__ywwd[2]
            gse__fao = jff__ywwd[3]
            bit__hdh = []
            for thfh__dscm in rpo__ohit:
                if thfh__dscm == 'scatter':
                    bit__hdh.append(bodo.scatterv(None))
                elif thfh__dscm == 'bcast':
                    bit__hdh.append(dhzda__firaa.bcast(None, root=MASTER_RANK))
            bltu__vqh = {}
            for argname, thfh__dscm in gse__fao.items():
                if thfh__dscm == 'scatter':
                    bltu__vqh[argname] = bodo.scatterv(None)
                elif thfh__dscm == 'bcast':
                    bltu__vqh[argname] = dhzda__firaa.bcast(None, root=
                        MASTER_RANK)
            ggekc__uabue = func(*bit__hdh, **bltu__vqh)
            if ggekc__uabue is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(ggekc__uabue)
            del (jff__ywwd, pyk__rpyel, func, cnhg__rauq, rpo__ohit,
                gse__fao, bit__hdh, bltu__vqh, ggekc__uabue)
            gc.collect()
        elif jff__ywwd[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    dhzda__firaa = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        rpo__ohit = ['scatter' for kwtm__kekw in range(len(args))]
        gse__fao = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        qat__qtsre = func.py_func.__code__.co_varnames
        yncur__xhiuw = func.targetoptions

        def get_distribution(argname):
            if argname in yncur__xhiuw.get('distributed', []
                ) or argname in yncur__xhiuw.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        rpo__ohit = [get_distribution(argname) for argname in qat__qtsre[:
            len(args)]]
        gse__fao = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    vem__vllhe = pickle.dumps(func.py_func)
    dhzda__firaa.bcast(['exec', vem__vllhe, rpo__ohit, gse__fao])
    bit__hdh = []
    for fqua__qyvjn, thfh__dscm in zip(args, rpo__ohit):
        if thfh__dscm == 'scatter':
            bit__hdh.append(bodo.scatterv(fqua__qyvjn))
        elif thfh__dscm == 'bcast':
            dhzda__firaa.bcast(fqua__qyvjn)
            bit__hdh.append(fqua__qyvjn)
    bltu__vqh = {}
    for argname, fqua__qyvjn in kwargs.items():
        thfh__dscm = gse__fao[argname]
        if thfh__dscm == 'scatter':
            bltu__vqh[argname] = bodo.scatterv(fqua__qyvjn)
        elif thfh__dscm == 'bcast':
            dhzda__firaa.bcast(fqua__qyvjn)
            bltu__vqh[argname] = fqua__qyvjn
    sln__ija = []
    for lpel__wgkkp, xpuz__gck in list(func.py_func.__globals__.items()):
        if isinstance(xpuz__gck, MasterModeDispatcher):
            sln__ija.append((func.py_func.__globals__, lpel__wgkkp, func.
                py_func.__globals__[lpel__wgkkp]))
            func.py_func.__globals__[lpel__wgkkp] = xpuz__gck.dispatcher
    ggekc__uabue = func(*bit__hdh, **bltu__vqh)
    for fbde__csss, lpel__wgkkp, xpuz__gck in sln__ija:
        fbde__csss[lpel__wgkkp] = xpuz__gck
    if ggekc__uabue is not None and func.overloads[func.signatures[0]
        ].metadata['is_return_distributed']:
        ggekc__uabue = bodo.gatherv(ggekc__uabue)
    return ggekc__uabue


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
