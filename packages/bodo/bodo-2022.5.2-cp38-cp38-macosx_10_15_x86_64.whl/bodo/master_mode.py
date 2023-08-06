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
        uum__akgx = state
        qpza__ybvn = inspect.getsourcelines(uum__akgx)[0][0]
        assert qpza__ybvn.startswith('@bodo.jit') or qpza__ybvn.startswith(
            '@jit')
        yqjx__stkc = eval(qpza__ybvn[1:])
        self.dispatcher = yqjx__stkc(uum__akgx)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    nnya__eoqk = MPI.COMM_WORLD
    while True:
        obcvm__yhk = nnya__eoqk.bcast(None, root=MASTER_RANK)
        if obcvm__yhk[0] == 'exec':
            uum__akgx = pickle.loads(obcvm__yhk[1])
            for zmo__rwq, mljlg__jrz in list(uum__akgx.__globals__.items()):
                if isinstance(mljlg__jrz, MasterModeDispatcher):
                    uum__akgx.__globals__[zmo__rwq] = mljlg__jrz.dispatcher
            if uum__akgx.__module__ not in sys.modules:
                sys.modules[uum__akgx.__module__] = pytypes.ModuleType(
                    uum__akgx.__module__)
            qpza__ybvn = inspect.getsourcelines(uum__akgx)[0][0]
            assert qpza__ybvn.startswith('@bodo.jit') or qpza__ybvn.startswith(
                '@jit')
            yqjx__stkc = eval(qpza__ybvn[1:])
            func = yqjx__stkc(uum__akgx)
            fish__tytzd = obcvm__yhk[2]
            dudbj__dfz = obcvm__yhk[3]
            gkqx__unlq = []
            for favj__itzmo in fish__tytzd:
                if favj__itzmo == 'scatter':
                    gkqx__unlq.append(bodo.scatterv(None))
                elif favj__itzmo == 'bcast':
                    gkqx__unlq.append(nnya__eoqk.bcast(None, root=MASTER_RANK))
            ogd__jjiz = {}
            for argname, favj__itzmo in dudbj__dfz.items():
                if favj__itzmo == 'scatter':
                    ogd__jjiz[argname] = bodo.scatterv(None)
                elif favj__itzmo == 'bcast':
                    ogd__jjiz[argname] = nnya__eoqk.bcast(None, root=
                        MASTER_RANK)
            tqcp__tgnau = func(*gkqx__unlq, **ogd__jjiz)
            if tqcp__tgnau is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(tqcp__tgnau)
            del (obcvm__yhk, uum__akgx, func, yqjx__stkc, fish__tytzd,
                dudbj__dfz, gkqx__unlq, ogd__jjiz, tqcp__tgnau)
            gc.collect()
        elif obcvm__yhk[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    nnya__eoqk = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        fish__tytzd = ['scatter' for csk__kna in range(len(args))]
        dudbj__dfz = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        lfnw__ihi = func.py_func.__code__.co_varnames
        qvsow__ytmyk = func.targetoptions

        def get_distribution(argname):
            if argname in qvsow__ytmyk.get('distributed', []
                ) or argname in qvsow__ytmyk.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        fish__tytzd = [get_distribution(argname) for argname in lfnw__ihi[:
            len(args)]]
        dudbj__dfz = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    fplda__ykp = pickle.dumps(func.py_func)
    nnya__eoqk.bcast(['exec', fplda__ykp, fish__tytzd, dudbj__dfz])
    gkqx__unlq = []
    for xfj__dup, favj__itzmo in zip(args, fish__tytzd):
        if favj__itzmo == 'scatter':
            gkqx__unlq.append(bodo.scatterv(xfj__dup))
        elif favj__itzmo == 'bcast':
            nnya__eoqk.bcast(xfj__dup)
            gkqx__unlq.append(xfj__dup)
    ogd__jjiz = {}
    for argname, xfj__dup in kwargs.items():
        favj__itzmo = dudbj__dfz[argname]
        if favj__itzmo == 'scatter':
            ogd__jjiz[argname] = bodo.scatterv(xfj__dup)
        elif favj__itzmo == 'bcast':
            nnya__eoqk.bcast(xfj__dup)
            ogd__jjiz[argname] = xfj__dup
    elgz__msxsf = []
    for zmo__rwq, mljlg__jrz in list(func.py_func.__globals__.items()):
        if isinstance(mljlg__jrz, MasterModeDispatcher):
            elgz__msxsf.append((func.py_func.__globals__, zmo__rwq, func.
                py_func.__globals__[zmo__rwq]))
            func.py_func.__globals__[zmo__rwq] = mljlg__jrz.dispatcher
    tqcp__tgnau = func(*gkqx__unlq, **ogd__jjiz)
    for eusi__krii, zmo__rwq, mljlg__jrz in elgz__msxsf:
        eusi__krii[zmo__rwq] = mljlg__jrz
    if tqcp__tgnau is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        tqcp__tgnau = bodo.gatherv(tqcp__tgnau)
    return tqcp__tgnau


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
