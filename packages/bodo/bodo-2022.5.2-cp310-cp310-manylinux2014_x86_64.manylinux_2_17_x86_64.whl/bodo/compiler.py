"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
numba.core.config.DISABLE_PERFORMANCE_WARNINGS = 1
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        kgsy__roux = 'bodo' if distributed else 'bodo_seq'
        kgsy__roux = (kgsy__roux + '_inline' if inline_calls_pass else
            kgsy__roux)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, kgsy__roux
            )
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for pllzj__nwws, (rcak__upzh, nbe__ytrr) in enumerate(pm.passes):
        if rcak__upzh == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(pllzj__nwws, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for pllzj__nwws, (rcak__upzh, nbe__ytrr) in enumerate(pm.passes):
        if rcak__upzh == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[pllzj__nwws] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for pllzj__nwws, (rcak__upzh, nbe__ytrr) in enumerate(pm.passes):
        if rcak__upzh == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(pllzj__nwws)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    ggw__hnjiw = guard(get_definition, func_ir, rhs.func)
    if isinstance(ggw__hnjiw, (ir.Global, ir.FreeVar, ir.Const)):
        vbb__xxbzr = ggw__hnjiw.value
    else:
        euv__kdbg = guard(find_callname, func_ir, rhs)
        if not (euv__kdbg and isinstance(euv__kdbg[0], str) and isinstance(
            euv__kdbg[1], str)):
            return
        func_name, func_mod = euv__kdbg
        try:
            import importlib
            klh__thwjp = importlib.import_module(func_mod)
            vbb__xxbzr = getattr(klh__thwjp, func_name)
        except:
            return
    if isinstance(vbb__xxbzr, CPUDispatcher) and issubclass(vbb__xxbzr.
        _compiler.pipeline_class, BodoCompiler
        ) and vbb__xxbzr._compiler.pipeline_class != BodoCompilerUDF:
        vbb__xxbzr._compiler.pipeline_class = BodoCompilerUDF
        vbb__xxbzr.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for mxin__pleok in block.body:
                if is_call_assign(mxin__pleok):
                    _convert_bodo_dispatcher_to_udf(mxin__pleok.value,
                        state.func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        cvqth__vxet = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        cvqth__vxet.run()
        return True


def _update_definitions(func_ir, node_list):
    epk__cmzh = ir.Loc('', 0)
    sze__sbq = ir.Block(ir.Scope(None, epk__cmzh), epk__cmzh)
    sze__sbq.body = node_list
    build_definitions({(0): sze__sbq}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        kqtm__fuy = 'overload_series_' + rhs.attr
        laf__qbk = getattr(bodo.hiframes.series_impl, kqtm__fuy)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        kqtm__fuy = 'overload_dataframe_' + rhs.attr
        laf__qbk = getattr(bodo.hiframes.dataframe_impl, kqtm__fuy)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    jvskx__vpcwq = laf__qbk(rhs_type)
    iuvl__jeoo = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    pvu__yag = compile_func_single_block(jvskx__vpcwq, (rhs.value,), stmt.
        target, iuvl__jeoo)
    _update_definitions(func_ir, pvu__yag)
    new_body += pvu__yag
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        erhd__ytibd = tuple(typemap[oeb__atg.name] for oeb__atg in rhs.args)
        zcpyo__fhl = {kgsy__roux: typemap[oeb__atg.name] for kgsy__roux,
            oeb__atg in dict(rhs.kws).items()}
        jvskx__vpcwq = getattr(bodo.hiframes.series_impl, 
            'overload_series_' + func_name)(*erhd__ytibd, **zcpyo__fhl)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        erhd__ytibd = tuple(typemap[oeb__atg.name] for oeb__atg in rhs.args)
        zcpyo__fhl = {kgsy__roux: typemap[oeb__atg.name] for kgsy__roux,
            oeb__atg in dict(rhs.kws).items()}
        jvskx__vpcwq = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*erhd__ytibd, **zcpyo__fhl)
    else:
        return False
    tfr__wpsk = replace_func(pass_info, jvskx__vpcwq, rhs.args, pysig=numba
        .core.utils.pysignature(jvskx__vpcwq), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    kibo__spqa, nbe__ytrr = inline_closure_call(func_ir, tfr__wpsk.glbls,
        block, len(new_body), tfr__wpsk.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=tfr__wpsk.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for nowu__asnca in kibo__spqa.values():
        nowu__asnca.loc = rhs.loc
        update_locs(nowu__asnca.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    vgz__antnu = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = vgz__antnu(func_ir, typemap)
    wod__ssxk = func_ir.blocks
    work_list = list((vdheo__kgv, wod__ssxk[vdheo__kgv]) for vdheo__kgv in
        reversed(wod__ssxk.keys()))
    while work_list:
        ago__pjbvm, block = work_list.pop()
        new_body = []
        ydwo__tgj = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                euv__kdbg = guard(find_callname, func_ir, rhs, typemap)
                if euv__kdbg is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = euv__kdbg
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    ydwo__tgj = True
                    break
            new_body.append(stmt)
        if not ydwo__tgj:
            wod__ssxk[ago__pjbvm].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        rdu__zhda = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = rdu__zhda.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        kaqy__cqmc = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        iuqf__tosp = kaqy__cqmc.run()
        uhnq__iatkf = iuqf__tosp
        if uhnq__iatkf:
            uhnq__iatkf = kaqy__cqmc.run()
        if uhnq__iatkf:
            kaqy__cqmc.run()
        return iuqf__tosp


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        qhw__dokn = 0
        uvyr__fkapp = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            qhw__dokn = int(os.environ[uvyr__fkapp])
        except:
            pass
        if qhw__dokn > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(qhw__dokn, state
                .metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        iuvl__jeoo = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, iuvl__jeoo)
        for block in state.func_ir.blocks.values():
            new_body = []
            for mxin__pleok in block.body:
                if type(mxin__pleok) in distributed_run_extensions:
                    tkdkf__puh = distributed_run_extensions[type(mxin__pleok)]
                    xkttx__vie = tkdkf__puh(mxin__pleok, None, state.
                        typemap, state.calltypes, state.typingctx, state.
                        targetctx)
                    new_body += xkttx__vie
                elif is_call_assign(mxin__pleok):
                    rhs = mxin__pleok.value
                    euv__kdbg = guard(find_callname, state.func_ir, rhs)
                    if euv__kdbg == ('gatherv', 'bodo') or euv__kdbg == (
                        'allgatherv', 'bodo'):
                        isr__wvh = state.typemap[mxin__pleok.target.name]
                        nyx__tuwlv = state.typemap[rhs.args[0].name]
                        if isinstance(nyx__tuwlv, types.Array) and isinstance(
                            isr__wvh, types.Array):
                            ppvxz__brlet = nyx__tuwlv.copy(readonly=False)
                            woq__roxun = isr__wvh.copy(readonly=False)
                            if ppvxz__brlet == woq__roxun:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), mxin__pleok.target, iuvl__jeoo)
                                continue
                        if isr__wvh != nyx__tuwlv and to_str_arr_if_dict_array(
                            isr__wvh) == to_str_arr_if_dict_array(nyx__tuwlv):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), mxin__pleok.target,
                                iuvl__jeoo, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            mxin__pleok.value = rhs.args[0]
                    new_body.append(mxin__pleok)
                else:
                    new_body.append(mxin__pleok)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        olqw__jrw = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return olqw__jrw.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    tob__waxb = set()
    while work_list:
        ago__pjbvm, block = work_list.pop()
        tob__waxb.add(ago__pjbvm)
        for i, woxvs__zkh in enumerate(block.body):
            if isinstance(woxvs__zkh, ir.Assign):
                zdjoy__ern = woxvs__zkh.value
                if isinstance(zdjoy__ern, ir.Expr) and zdjoy__ern.op == 'call':
                    ggw__hnjiw = guard(get_definition, func_ir, zdjoy__ern.func
                        )
                    if isinstance(ggw__hnjiw, (ir.Global, ir.FreeVar)
                        ) and isinstance(ggw__hnjiw.value, CPUDispatcher
                        ) and issubclass(ggw__hnjiw.value._compiler.
                        pipeline_class, BodoCompiler):
                        krq__bixn = ggw__hnjiw.value.py_func
                        arg_types = None
                        if typingctx:
                            gpug__apxnj = dict(zdjoy__ern.kws)
                            dcbd__ohl = tuple(typemap[oeb__atg.name] for
                                oeb__atg in zdjoy__ern.args)
                            zjoh__ynpr = {gvb__gxd: typemap[oeb__atg.name] for
                                gvb__gxd, oeb__atg in gpug__apxnj.items()}
                            nbe__ytrr, arg_types = (ggw__hnjiw.value.
                                fold_argument_types(dcbd__ohl, zjoh__ynpr))
                        nbe__ytrr, lbpji__mkr = inline_closure_call(func_ir,
                            krq__bixn.__globals__, block, i, krq__bixn,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((lbpji__mkr[gvb__gxd].name, oeb__atg
                            ) for gvb__gxd, oeb__atg in ggw__hnjiw.value.
                            locals.items() if gvb__gxd in lbpji__mkr)
                        break
    return tob__waxb


def udf_jit(signature_or_function=None, **options):
    bko__adt = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=bko__adt,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for pllzj__nwws, (rcak__upzh, nbe__ytrr) in enumerate(pm.passes):
        if rcak__upzh == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:pllzj__nwws + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    wve__lal = None
    tkuii__lknpb = None
    _locals = {}
    gocpq__kro = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(gocpq__kro, arg_types,
        kw_types)
    qgk__oxyh = numba.core.compiler.Flags()
    vpfe__rck = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    rih__fsgut = {'nopython': True, 'boundscheck': False, 'parallel': vpfe__rck
        }
    numba.core.registry.cpu_target.options.parse_as_flags(qgk__oxyh, rih__fsgut
        )
    tzluf__wowm = TyperCompiler(typingctx, targetctx, wve__lal, args,
        tkuii__lknpb, qgk__oxyh, _locals)
    return tzluf__wowm.compile_extra(func)
