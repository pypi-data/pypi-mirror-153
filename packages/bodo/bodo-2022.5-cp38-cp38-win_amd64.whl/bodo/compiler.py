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
        clwd__hcvll = 'bodo' if distributed else 'bodo_seq'
        clwd__hcvll = (clwd__hcvll + '_inline' if inline_calls_pass else
            clwd__hcvll)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            clwd__hcvll)
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
    for hyi__knwcw, (lbkg__otujj, kar__ulvm) in enumerate(pm.passes):
        if lbkg__otujj == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(hyi__knwcw, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for hyi__knwcw, (lbkg__otujj, kar__ulvm) in enumerate(pm.passes):
        if lbkg__otujj == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[hyi__knwcw] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for hyi__knwcw, (lbkg__otujj, kar__ulvm) in enumerate(pm.passes):
        if lbkg__otujj == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(hyi__knwcw)
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
    oipq__dqe = guard(get_definition, func_ir, rhs.func)
    if isinstance(oipq__dqe, (ir.Global, ir.FreeVar, ir.Const)):
        hiw__fnmdm = oipq__dqe.value
    else:
        lplf__wvq = guard(find_callname, func_ir, rhs)
        if not (lplf__wvq and isinstance(lplf__wvq[0], str) and isinstance(
            lplf__wvq[1], str)):
            return
        func_name, func_mod = lplf__wvq
        try:
            import importlib
            iet__pixnv = importlib.import_module(func_mod)
            hiw__fnmdm = getattr(iet__pixnv, func_name)
        except:
            return
    if isinstance(hiw__fnmdm, CPUDispatcher) and issubclass(hiw__fnmdm.
        _compiler.pipeline_class, BodoCompiler
        ) and hiw__fnmdm._compiler.pipeline_class != BodoCompilerUDF:
        hiw__fnmdm._compiler.pipeline_class = BodoCompilerUDF
        hiw__fnmdm.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for lupgf__srs in block.body:
                if is_call_assign(lupgf__srs):
                    _convert_bodo_dispatcher_to_udf(lupgf__srs.value, state
                        .func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        fug__ydi = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        fug__ydi.run()
        return True


def _update_definitions(func_ir, node_list):
    ocxdo__apco = ir.Loc('', 0)
    lbxfv__vsyq = ir.Block(ir.Scope(None, ocxdo__apco), ocxdo__apco)
    lbxfv__vsyq.body = node_list
    build_definitions({(0): lbxfv__vsyq}, func_ir._definitions)


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
        ppof__cmees = 'overload_series_' + rhs.attr
        mogd__xrlou = getattr(bodo.hiframes.series_impl, ppof__cmees)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        ppof__cmees = 'overload_dataframe_' + rhs.attr
        mogd__xrlou = getattr(bodo.hiframes.dataframe_impl, ppof__cmees)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    emrr__nhy = mogd__xrlou(rhs_type)
    dxbel__imfs = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc
        )
    jvcss__jurpn = compile_func_single_block(emrr__nhy, (rhs.value,), stmt.
        target, dxbel__imfs)
    _update_definitions(func_ir, jvcss__jurpn)
    new_body += jvcss__jurpn
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
        bfssc__bsypx = tuple(typemap[jqul__iqufb.name] for jqul__iqufb in
            rhs.args)
        sdoo__ami = {clwd__hcvll: typemap[jqul__iqufb.name] for clwd__hcvll,
            jqul__iqufb in dict(rhs.kws).items()}
        emrr__nhy = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*bfssc__bsypx, **sdoo__ami)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        bfssc__bsypx = tuple(typemap[jqul__iqufb.name] for jqul__iqufb in
            rhs.args)
        sdoo__ami = {clwd__hcvll: typemap[jqul__iqufb.name] for clwd__hcvll,
            jqul__iqufb in dict(rhs.kws).items()}
        emrr__nhy = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*bfssc__bsypx, **sdoo__ami)
    else:
        return False
    tyuve__jypoy = replace_func(pass_info, emrr__nhy, rhs.args, pysig=numba
        .core.utils.pysignature(emrr__nhy), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    bzoc__ajoab, kar__ulvm = inline_closure_call(func_ir, tyuve__jypoy.
        glbls, block, len(new_body), tyuve__jypoy.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=tyuve__jypoy.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for xoh__gzlj in bzoc__ajoab.values():
        xoh__gzlj.loc = rhs.loc
        update_locs(xoh__gzlj.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    unpav__ptnrk = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = unpav__ptnrk(func_ir, typemap)
    fmguz__bcz = func_ir.blocks
    work_list = list((sjhcj__cop, fmguz__bcz[sjhcj__cop]) for sjhcj__cop in
        reversed(fmguz__bcz.keys()))
    while work_list:
        xfi__ohv, block = work_list.pop()
        new_body = []
        larrm__iwch = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                lplf__wvq = guard(find_callname, func_ir, rhs, typemap)
                if lplf__wvq is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = lplf__wvq
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    larrm__iwch = True
                    break
            new_body.append(stmt)
        if not larrm__iwch:
            fmguz__bcz[xfi__ohv].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        ffly__xbgy = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = ffly__xbgy.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        wchi__fzukm = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        cjz__wmg = wchi__fzukm.run()
        jmm__keaqq = cjz__wmg
        if jmm__keaqq:
            jmm__keaqq = wchi__fzukm.run()
        if jmm__keaqq:
            wchi__fzukm.run()
        return cjz__wmg


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        ronhq__qwoh = 0
        fcgqc__gxj = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            ronhq__qwoh = int(os.environ[fcgqc__gxj])
        except:
            pass
        if ronhq__qwoh > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(ronhq__qwoh,
                state.metadata)
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
        dxbel__imfs = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, dxbel__imfs)
        for block in state.func_ir.blocks.values():
            new_body = []
            for lupgf__srs in block.body:
                if type(lupgf__srs) in distributed_run_extensions:
                    jklmq__fmrda = distributed_run_extensions[type(lupgf__srs)]
                    ixg__hsuj = jklmq__fmrda(lupgf__srs, None, state.
                        typemap, state.calltypes, state.typingctx, state.
                        targetctx)
                    new_body += ixg__hsuj
                elif is_call_assign(lupgf__srs):
                    rhs = lupgf__srs.value
                    lplf__wvq = guard(find_callname, state.func_ir, rhs)
                    if lplf__wvq == ('gatherv', 'bodo') or lplf__wvq == (
                        'allgatherv', 'bodo'):
                        cyv__lmbqn = state.typemap[lupgf__srs.target.name]
                        djy__rmlcm = state.typemap[rhs.args[0].name]
                        if isinstance(djy__rmlcm, types.Array) and isinstance(
                            cyv__lmbqn, types.Array):
                            usfob__qagy = djy__rmlcm.copy(readonly=False)
                            fihl__bnz = cyv__lmbqn.copy(readonly=False)
                            if usfob__qagy == fihl__bnz:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), lupgf__srs.target, dxbel__imfs)
                                continue
                        if (cyv__lmbqn != djy__rmlcm and 
                            to_str_arr_if_dict_array(cyv__lmbqn) ==
                            to_str_arr_if_dict_array(djy__rmlcm)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), lupgf__srs.target,
                                dxbel__imfs, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            lupgf__srs.value = rhs.args[0]
                    new_body.append(lupgf__srs)
                else:
                    new_body.append(lupgf__srs)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        dsde__avo = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return dsde__avo.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    mxzs__ldgtn = set()
    while work_list:
        xfi__ohv, block = work_list.pop()
        mxzs__ldgtn.add(xfi__ohv)
        for i, mdy__jrroq in enumerate(block.body):
            if isinstance(mdy__jrroq, ir.Assign):
                mev__dttjm = mdy__jrroq.value
                if isinstance(mev__dttjm, ir.Expr) and mev__dttjm.op == 'call':
                    oipq__dqe = guard(get_definition, func_ir, mev__dttjm.func)
                    if isinstance(oipq__dqe, (ir.Global, ir.FreeVar)
                        ) and isinstance(oipq__dqe.value, CPUDispatcher
                        ) and issubclass(oipq__dqe.value._compiler.
                        pipeline_class, BodoCompiler):
                        iqn__ikr = oipq__dqe.value.py_func
                        arg_types = None
                        if typingctx:
                            bshi__ivvy = dict(mev__dttjm.kws)
                            vaxj__den = tuple(typemap[jqul__iqufb.name] for
                                jqul__iqufb in mev__dttjm.args)
                            wnn__hmbnb = {olu__vnbp: typemap[jqul__iqufb.
                                name] for olu__vnbp, jqul__iqufb in
                                bshi__ivvy.items()}
                            kar__ulvm, arg_types = (oipq__dqe.value.
                                fold_argument_types(vaxj__den, wnn__hmbnb))
                        kar__ulvm, jkh__ivan = inline_closure_call(func_ir,
                            iqn__ikr.__globals__, block, i, iqn__ikr,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((jkh__ivan[olu__vnbp].name,
                            jqul__iqufb) for olu__vnbp, jqul__iqufb in
                            oipq__dqe.value.locals.items() if olu__vnbp in
                            jkh__ivan)
                        break
    return mxzs__ldgtn


def udf_jit(signature_or_function=None, **options):
    jddj__myyl = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=jddj__myyl,
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
    for hyi__knwcw, (lbkg__otujj, kar__ulvm) in enumerate(pm.passes):
        if lbkg__otujj == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:hyi__knwcw + 1]
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
    mlp__hrb = None
    zhl__qbzy = None
    _locals = {}
    yll__jtxf = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(yll__jtxf, arg_types,
        kw_types)
    jxui__pcdrj = numba.core.compiler.Flags()
    qxbsh__rnza = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    vazf__wnh = {'nopython': True, 'boundscheck': False, 'parallel':
        qxbsh__rnza}
    numba.core.registry.cpu_target.options.parse_as_flags(jxui__pcdrj,
        vazf__wnh)
    oaqho__cgl = TyperCompiler(typingctx, targetctx, mlp__hrb, args,
        zhl__qbzy, jxui__pcdrj, _locals)
    return oaqho__cgl.compile_extra(func)
