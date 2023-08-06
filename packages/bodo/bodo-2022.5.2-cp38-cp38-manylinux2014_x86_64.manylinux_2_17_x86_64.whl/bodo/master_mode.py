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
        gny__qipc = state
        sfxly__unqyz = inspect.getsourcelines(gny__qipc)[0][0]
        assert sfxly__unqyz.startswith('@bodo.jit') or sfxly__unqyz.startswith(
            '@jit')
        bszns__vel = eval(sfxly__unqyz[1:])
        self.dispatcher = bszns__vel(gny__qipc)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    isn__pjv = MPI.COMM_WORLD
    while True:
        giq__wfy = isn__pjv.bcast(None, root=MASTER_RANK)
        if giq__wfy[0] == 'exec':
            gny__qipc = pickle.loads(giq__wfy[1])
            for noh__unkw, bvnb__fgagg in list(gny__qipc.__globals__.items()):
                if isinstance(bvnb__fgagg, MasterModeDispatcher):
                    gny__qipc.__globals__[noh__unkw] = bvnb__fgagg.dispatcher
            if gny__qipc.__module__ not in sys.modules:
                sys.modules[gny__qipc.__module__] = pytypes.ModuleType(
                    gny__qipc.__module__)
            sfxly__unqyz = inspect.getsourcelines(gny__qipc)[0][0]
            assert sfxly__unqyz.startswith('@bodo.jit'
                ) or sfxly__unqyz.startswith('@jit')
            bszns__vel = eval(sfxly__unqyz[1:])
            func = bszns__vel(gny__qipc)
            mgote__npd = giq__wfy[2]
            fwbt__uwbn = giq__wfy[3]
            olxov__bluk = []
            for soin__gksb in mgote__npd:
                if soin__gksb == 'scatter':
                    olxov__bluk.append(bodo.scatterv(None))
                elif soin__gksb == 'bcast':
                    olxov__bluk.append(isn__pjv.bcast(None, root=MASTER_RANK))
            ewwpg__fszog = {}
            for argname, soin__gksb in fwbt__uwbn.items():
                if soin__gksb == 'scatter':
                    ewwpg__fszog[argname] = bodo.scatterv(None)
                elif soin__gksb == 'bcast':
                    ewwpg__fszog[argname] = isn__pjv.bcast(None, root=
                        MASTER_RANK)
            dwuz__ktrji = func(*olxov__bluk, **ewwpg__fszog)
            if dwuz__ktrji is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(dwuz__ktrji)
            del (giq__wfy, gny__qipc, func, bszns__vel, mgote__npd,
                fwbt__uwbn, olxov__bluk, ewwpg__fszog, dwuz__ktrji)
            gc.collect()
        elif giq__wfy[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    isn__pjv = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        mgote__npd = ['scatter' for mgfqa__cqvh in range(len(args))]
        fwbt__uwbn = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        try__yrki = func.py_func.__code__.co_varnames
        qwo__nkh = func.targetoptions

        def get_distribution(argname):
            if argname in qwo__nkh.get('distributed', []
                ) or argname in qwo__nkh.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        mgote__npd = [get_distribution(argname) for argname in try__yrki[:
            len(args)]]
        fwbt__uwbn = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    bwm__snciw = pickle.dumps(func.py_func)
    isn__pjv.bcast(['exec', bwm__snciw, mgote__npd, fwbt__uwbn])
    olxov__bluk = []
    for dqlyv__ltjzl, soin__gksb in zip(args, mgote__npd):
        if soin__gksb == 'scatter':
            olxov__bluk.append(bodo.scatterv(dqlyv__ltjzl))
        elif soin__gksb == 'bcast':
            isn__pjv.bcast(dqlyv__ltjzl)
            olxov__bluk.append(dqlyv__ltjzl)
    ewwpg__fszog = {}
    for argname, dqlyv__ltjzl in kwargs.items():
        soin__gksb = fwbt__uwbn[argname]
        if soin__gksb == 'scatter':
            ewwpg__fszog[argname] = bodo.scatterv(dqlyv__ltjzl)
        elif soin__gksb == 'bcast':
            isn__pjv.bcast(dqlyv__ltjzl)
            ewwpg__fszog[argname] = dqlyv__ltjzl
    wsci__ooiyg = []
    for noh__unkw, bvnb__fgagg in list(func.py_func.__globals__.items()):
        if isinstance(bvnb__fgagg, MasterModeDispatcher):
            wsci__ooiyg.append((func.py_func.__globals__, noh__unkw, func.
                py_func.__globals__[noh__unkw]))
            func.py_func.__globals__[noh__unkw] = bvnb__fgagg.dispatcher
    dwuz__ktrji = func(*olxov__bluk, **ewwpg__fszog)
    for akk__asp, noh__unkw, bvnb__fgagg in wsci__ooiyg:
        akk__asp[noh__unkw] = bvnb__fgagg
    if dwuz__ktrji is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        dwuz__ktrji = bodo.gatherv(dwuz__ktrji)
    return dwuz__ktrji


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
