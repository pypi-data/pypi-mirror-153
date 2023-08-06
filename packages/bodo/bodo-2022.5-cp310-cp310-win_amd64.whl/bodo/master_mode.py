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
        ehovh__ohln = state
        rwoa__ydvk = inspect.getsourcelines(ehovh__ohln)[0][0]
        assert rwoa__ydvk.startswith('@bodo.jit') or rwoa__ydvk.startswith(
            '@jit')
        ebh__xuav = eval(rwoa__ydvk[1:])
        self.dispatcher = ebh__xuav(ehovh__ohln)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    ruy__sqx = MPI.COMM_WORLD
    while True:
        wxnt__uypov = ruy__sqx.bcast(None, root=MASTER_RANK)
        if wxnt__uypov[0] == 'exec':
            ehovh__ohln = pickle.loads(wxnt__uypov[1])
            for gewic__mtwyp, nbfjh__yff in list(ehovh__ohln.__globals__.
                items()):
                if isinstance(nbfjh__yff, MasterModeDispatcher):
                    ehovh__ohln.__globals__[gewic__mtwyp
                        ] = nbfjh__yff.dispatcher
            if ehovh__ohln.__module__ not in sys.modules:
                sys.modules[ehovh__ohln.__module__] = pytypes.ModuleType(
                    ehovh__ohln.__module__)
            rwoa__ydvk = inspect.getsourcelines(ehovh__ohln)[0][0]
            assert rwoa__ydvk.startswith('@bodo.jit') or rwoa__ydvk.startswith(
                '@jit')
            ebh__xuav = eval(rwoa__ydvk[1:])
            func = ebh__xuav(ehovh__ohln)
            res__ibez = wxnt__uypov[2]
            vctr__kmhrj = wxnt__uypov[3]
            witc__fary = []
            for gdwzt__rdww in res__ibez:
                if gdwzt__rdww == 'scatter':
                    witc__fary.append(bodo.scatterv(None))
                elif gdwzt__rdww == 'bcast':
                    witc__fary.append(ruy__sqx.bcast(None, root=MASTER_RANK))
            yunhq__yybv = {}
            for argname, gdwzt__rdww in vctr__kmhrj.items():
                if gdwzt__rdww == 'scatter':
                    yunhq__yybv[argname] = bodo.scatterv(None)
                elif gdwzt__rdww == 'bcast':
                    yunhq__yybv[argname] = ruy__sqx.bcast(None, root=
                        MASTER_RANK)
            wsb__veom = func(*witc__fary, **yunhq__yybv)
            if wsb__veom is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(wsb__veom)
            del (wxnt__uypov, ehovh__ohln, func, ebh__xuav, res__ibez,
                vctr__kmhrj, witc__fary, yunhq__yybv, wsb__veom)
            gc.collect()
        elif wxnt__uypov[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    ruy__sqx = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        res__ibez = ['scatter' for mbygk__wtl in range(len(args))]
        vctr__kmhrj = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        eiah__wwp = func.py_func.__code__.co_varnames
        wtq__pgank = func.targetoptions

        def get_distribution(argname):
            if argname in wtq__pgank.get('distributed', []
                ) or argname in wtq__pgank.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        res__ibez = [get_distribution(argname) for argname in eiah__wwp[:
            len(args)]]
        vctr__kmhrj = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    qvypb__zfyht = pickle.dumps(func.py_func)
    ruy__sqx.bcast(['exec', qvypb__zfyht, res__ibez, vctr__kmhrj])
    witc__fary = []
    for bqkz__sqxt, gdwzt__rdww in zip(args, res__ibez):
        if gdwzt__rdww == 'scatter':
            witc__fary.append(bodo.scatterv(bqkz__sqxt))
        elif gdwzt__rdww == 'bcast':
            ruy__sqx.bcast(bqkz__sqxt)
            witc__fary.append(bqkz__sqxt)
    yunhq__yybv = {}
    for argname, bqkz__sqxt in kwargs.items():
        gdwzt__rdww = vctr__kmhrj[argname]
        if gdwzt__rdww == 'scatter':
            yunhq__yybv[argname] = bodo.scatterv(bqkz__sqxt)
        elif gdwzt__rdww == 'bcast':
            ruy__sqx.bcast(bqkz__sqxt)
            yunhq__yybv[argname] = bqkz__sqxt
    peiu__niwf = []
    for gewic__mtwyp, nbfjh__yff in list(func.py_func.__globals__.items()):
        if isinstance(nbfjh__yff, MasterModeDispatcher):
            peiu__niwf.append((func.py_func.__globals__, gewic__mtwyp, func
                .py_func.__globals__[gewic__mtwyp]))
            func.py_func.__globals__[gewic__mtwyp] = nbfjh__yff.dispatcher
    wsb__veom = func(*witc__fary, **yunhq__yybv)
    for isc__kqh, gewic__mtwyp, nbfjh__yff in peiu__niwf:
        isc__kqh[gewic__mtwyp] = nbfjh__yff
    if wsb__veom is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        wsb__veom = bodo.gatherv(wsb__veom)
    return wsb__veom


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
