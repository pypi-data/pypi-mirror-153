"""
Defines decorators of Bodo. Currently just @jit.
"""
import hashlib
import inspect
import warnings
import numba
from numba.core import cpu
from numba.core.options import _mapping
from numba.core.targetconfig import Option, TargetConfig
import bodo
from bodo import master_mode
numba.core.cpu.CPUTargetOptions.all_args_distributed_block = _mapping(
    'all_args_distributed_block')
numba.core.cpu.CPUTargetOptions.all_args_distributed_varlength = _mapping(
    'all_args_distributed_varlength')
numba.core.cpu.CPUTargetOptions.all_returns_distributed = _mapping(
    'all_returns_distributed')
numba.core.cpu.CPUTargetOptions.returns_maybe_distributed = _mapping(
    'returns_maybe_distributed')
numba.core.cpu.CPUTargetOptions.args_maybe_distributed = _mapping(
    'args_maybe_distributed')
numba.core.cpu.CPUTargetOptions.distributed = _mapping('distributed')
numba.core.cpu.CPUTargetOptions.distributed_block = _mapping(
    'distributed_block')
numba.core.cpu.CPUTargetOptions.replicated = _mapping('replicated')
numba.core.cpu.CPUTargetOptions.threaded = _mapping('threaded')
numba.core.cpu.CPUTargetOptions.pivots = _mapping('pivots')
numba.core.cpu.CPUTargetOptions.h5_types = _mapping('h5_types')


class Flags(TargetConfig):
    enable_looplift = Option(type=bool, default=False, doc=
        'Enable loop-lifting')
    enable_pyobject = Option(type=bool, default=False, doc=
        'Enable pyobject mode (in general)')
    enable_pyobject_looplift = Option(type=bool, default=False, doc=
        'Enable pyobject mode inside lifted loops')
    enable_ssa = Option(type=bool, default=True, doc='Enable SSA')
    force_pyobject = Option(type=bool, default=False, doc=
        'Force pyobject mode inside the whole function')
    release_gil = Option(type=bool, default=False, doc=
        'Release GIL inside the native function')
    no_compile = Option(type=bool, default=False, doc='TODO')
    debuginfo = Option(type=bool, default=False, doc='TODO')
    boundscheck = Option(type=bool, default=False, doc='TODO')
    forceinline = Option(type=bool, default=False, doc='TODO')
    no_cpython_wrapper = Option(type=bool, default=False, doc='TODO')
    no_cfunc_wrapper = Option(type=bool, default=False, doc='TODO')
    auto_parallel = Option(type=cpu.ParallelOptions, default=cpu.
        ParallelOptions(False), doc=
        """Enable automatic parallel optimization, can be fine-tuned by
taking a dictionary of sub-options instead of a boolean, see parfor.py for
detail"""
        )
    nrt = Option(type=bool, default=False, doc='TODO')
    no_rewrites = Option(type=bool, default=False, doc='TODO')
    error_model = Option(type=str, default='python', doc='TODO')
    fastmath = Option(type=cpu.FastMathOptions, default=cpu.FastMathOptions
        (False), doc='TODO')
    noalias = Option(type=bool, default=False, doc='TODO')
    inline = Option(type=cpu.InlineOptions, default=cpu.InlineOptions(
        'never'), doc='TODO')
    target_backend = Option(type=str, default='cpu', doc='backend')
    all_args_distributed_block = Option(type=bool, default=False, doc=
        'All args have 1D distribution')
    all_args_distributed_varlength = Option(type=bool, default=False, doc=
        'All args have 1D_Var distribution')
    all_returns_distributed = Option(type=bool, default=False, doc=
        'All returns are distributed')
    returns_maybe_distributed = Option(type=bool, default=True, doc=
        'Returns may be distributed')
    args_maybe_distributed = Option(type=bool, default=True, doc=
        'Arguments may be distributed')
    distributed = Option(type=set, default=set(), doc=
        'distributed arguments or returns')
    distributed_block = Option(type=set, default=set(), doc=
        'distributed 1D arguments or returns')
    replicated = Option(type=set, default=set(), doc=
        'replicated arguments or returns')
    threaded = Option(type=set, default=set(), doc=
        'Threaded arguments or returns')
    pivots = Option(type=dict, default=dict(), doc='pivot values')
    h5_types = Option(type=dict, default=dict(), doc='HDF5 read data types')


DEFAULT_FLAGS = Flags()
DEFAULT_FLAGS.nrt = True
if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.core.compiler.Flags)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9d5f7a93545fe783c20a9d7579c73e04d91d6b2841fb5972b391a67fff03b9c3':
        warnings.warn('numba.core.compiler.Flags has changed')
numba.core.compiler.Flags = Flags
numba.core.compiler.DEFAULT_FLAGS = DEFAULT_FLAGS


def distributed_diagnostics(self, signature=None, level=1):
    if signature is None and len(self.signatures) == 0:
        raise bodo.utils.typing.BodoError(
            'Distributed diagnostics not available for a function that is not compiled yet'
            )
    if bodo.get_rank() != 0:
        return

    def dump(sig):
        nsqlh__eqjtx = self.overloads[sig]
        qjuf__gizfb = nsqlh__eqjtx.metadata.get('distributed_diagnostics', None
            )
        if qjuf__gizfb is None:
            mmx__rxwr = 'No distributed diagnostic available'
            raise bodo.utils.typing.BodoError(mmx__rxwr)
        qjuf__gizfb.dump(level, self.get_metadata(sig))
    if signature is not None:
        dump(signature)
    else:
        [dump(sig) for sig in self.signatures]


numba.core.dispatcher.Dispatcher.distributed_diagnostics = (
    distributed_diagnostics)


def master_mode_wrapper(numba_jit_wrapper):

    def _wrapper(pyfunc):
        vauub__sbtz = numba_jit_wrapper(pyfunc)
        return master_mode.MasterModeDispatcher(vauub__sbtz)
    return _wrapper


def is_jit_execution():
    return False


@numba.extending.overload(is_jit_execution)
def is_jit_execution_overload():
    return lambda : True


def jit(signature_or_function=None, pipeline_class=None, **options):
    _init_extensions()
    if 'nopython' not in options:
        options['nopython'] = True
    options['parallel'] = {'comprehension': True, 'setitem': False,
        'inplace_binop': False, 'reduction': True, 'numpy': True, 'stencil':
        False, 'fusion': True}
    pipeline_class = (bodo.compiler.BodoCompiler if pipeline_class is None else
        pipeline_class)
    if 'distributed' in options and isinstance(options['distributed'], bool):
        hkno__vwqf = options.pop('distributed')
        pipeline_class = (pipeline_class if hkno__vwqf else bodo.compiler.
            BodoCompilerSeq)
    if 'replicated' in options and isinstance(options['replicated'], bool):
        khyrq__vfjzp = options.pop('replicated')
        pipeline_class = (bodo.compiler.BodoCompilerSeq if khyrq__vfjzp else
            pipeline_class)
    txnr__bjh = numba.jit(signature_or_function, pipeline_class=
        pipeline_class, **options)
    if master_mode.master_mode_on and bodo.get_rank(
        ) == master_mode.MASTER_RANK:
        if isinstance(txnr__bjh, numba.dispatcher._DispatcherBase):
            return master_mode.MasterModeDispatcher(txnr__bjh)
        else:
            return master_mode_wrapper(txnr__bjh)
    else:
        return txnr__bjh


def _init_extensions():
    import sys
    laa__ijrm = False
    if 'sklearn' in sys.modules and 'bodo.libs.sklearn_ext' not in sys.modules:
        import bodo.libs.sklearn_ext
        laa__ijrm = True
    if ('matplotlib' in sys.modules and 'bodo.libs.matplotlib_ext' not in
        sys.modules):
        import bodo.libs.matplotlib_ext
        laa__ijrm = True
    if 'xgboost' in sys.modules and 'bodo.libs.xgb_ext' not in sys.modules:
        import bodo.libs.xgb_ext
        laa__ijrm = True
    if 'h5py' in sys.modules and 'bodo.io.h5_api' not in sys.modules:
        import bodo.io.h5_api
        if bodo.utils.utils.has_supported_h5py():
            from bodo.io import h5
        laa__ijrm = True
    if 'pyspark' in sys.modules and 'bodo.libs.pyspark_ext' not in sys.modules:
        import pyspark.sql.functions
        import bodo.libs.pyspark_ext
        bodo.utils.transform.no_side_effect_call_tuples.update({('col',
            pyspark.sql.functions), (pyspark.sql.functions.col,), ('sum',
            pyspark.sql.functions), (pyspark.sql.functions.sum,)})
        laa__ijrm = True
    if laa__ijrm:
        numba.core.registry.cpu_target.target_context.refresh()
