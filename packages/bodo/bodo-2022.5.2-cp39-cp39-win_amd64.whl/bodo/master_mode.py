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
        ovcb__wbsky = state
        axn__iatp = inspect.getsourcelines(ovcb__wbsky)[0][0]
        assert axn__iatp.startswith('@bodo.jit') or axn__iatp.startswith('@jit'
            )
        egu__zxn = eval(axn__iatp[1:])
        self.dispatcher = egu__zxn(ovcb__wbsky)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    tlk__wxvnx = MPI.COMM_WORLD
    while True:
        yur__jokwi = tlk__wxvnx.bcast(None, root=MASTER_RANK)
        if yur__jokwi[0] == 'exec':
            ovcb__wbsky = pickle.loads(yur__jokwi[1])
            for dvtmg__ona, gfmcy__xji in list(ovcb__wbsky.__globals__.items()
                ):
                if isinstance(gfmcy__xji, MasterModeDispatcher):
                    ovcb__wbsky.__globals__[dvtmg__ona] = gfmcy__xji.dispatcher
            if ovcb__wbsky.__module__ not in sys.modules:
                sys.modules[ovcb__wbsky.__module__] = pytypes.ModuleType(
                    ovcb__wbsky.__module__)
            axn__iatp = inspect.getsourcelines(ovcb__wbsky)[0][0]
            assert axn__iatp.startswith('@bodo.jit') or axn__iatp.startswith(
                '@jit')
            egu__zxn = eval(axn__iatp[1:])
            func = egu__zxn(ovcb__wbsky)
            vib__dem = yur__jokwi[2]
            jdo__emwh = yur__jokwi[3]
            cgw__wnijc = []
            for vqzm__obtss in vib__dem:
                if vqzm__obtss == 'scatter':
                    cgw__wnijc.append(bodo.scatterv(None))
                elif vqzm__obtss == 'bcast':
                    cgw__wnijc.append(tlk__wxvnx.bcast(None, root=MASTER_RANK))
            vbpl__sucz = {}
            for argname, vqzm__obtss in jdo__emwh.items():
                if vqzm__obtss == 'scatter':
                    vbpl__sucz[argname] = bodo.scatterv(None)
                elif vqzm__obtss == 'bcast':
                    vbpl__sucz[argname] = tlk__wxvnx.bcast(None, root=
                        MASTER_RANK)
            pmet__purr = func(*cgw__wnijc, **vbpl__sucz)
            if pmet__purr is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(pmet__purr)
            del (yur__jokwi, ovcb__wbsky, func, egu__zxn, vib__dem,
                jdo__emwh, cgw__wnijc, vbpl__sucz, pmet__purr)
            gc.collect()
        elif yur__jokwi[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    tlk__wxvnx = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        vib__dem = ['scatter' for mqb__vlu in range(len(args))]
        jdo__emwh = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        moo__okdus = func.py_func.__code__.co_varnames
        korof__jit = func.targetoptions

        def get_distribution(argname):
            if argname in korof__jit.get('distributed', []
                ) or argname in korof__jit.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        vib__dem = [get_distribution(argname) for argname in moo__okdus[:
            len(args)]]
        jdo__emwh = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    jqqo__buec = pickle.dumps(func.py_func)
    tlk__wxvnx.bcast(['exec', jqqo__buec, vib__dem, jdo__emwh])
    cgw__wnijc = []
    for ajuq__exw, vqzm__obtss in zip(args, vib__dem):
        if vqzm__obtss == 'scatter':
            cgw__wnijc.append(bodo.scatterv(ajuq__exw))
        elif vqzm__obtss == 'bcast':
            tlk__wxvnx.bcast(ajuq__exw)
            cgw__wnijc.append(ajuq__exw)
    vbpl__sucz = {}
    for argname, ajuq__exw in kwargs.items():
        vqzm__obtss = jdo__emwh[argname]
        if vqzm__obtss == 'scatter':
            vbpl__sucz[argname] = bodo.scatterv(ajuq__exw)
        elif vqzm__obtss == 'bcast':
            tlk__wxvnx.bcast(ajuq__exw)
            vbpl__sucz[argname] = ajuq__exw
    avngf__zvpy = []
    for dvtmg__ona, gfmcy__xji in list(func.py_func.__globals__.items()):
        if isinstance(gfmcy__xji, MasterModeDispatcher):
            avngf__zvpy.append((func.py_func.__globals__, dvtmg__ona, func.
                py_func.__globals__[dvtmg__ona]))
            func.py_func.__globals__[dvtmg__ona] = gfmcy__xji.dispatcher
    pmet__purr = func(*cgw__wnijc, **vbpl__sucz)
    for esuir__qbac, dvtmg__ona, gfmcy__xji in avngf__zvpy:
        esuir__qbac[dvtmg__ona] = gfmcy__xji
    if pmet__purr is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        pmet__purr = bodo.gatherv(pmet__purr)
    return pmet__purr


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
