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
        cgx__vulkt = 'bodo' if distributed else 'bodo_seq'
        cgx__vulkt = (cgx__vulkt + '_inline' if inline_calls_pass else
            cgx__vulkt)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, cgx__vulkt
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
    for oytmv__fkp, (lua__rken, yvogz__qsnt) in enumerate(pm.passes):
        if lua__rken == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(oytmv__fkp, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for oytmv__fkp, (lua__rken, yvogz__qsnt) in enumerate(pm.passes):
        if lua__rken == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[oytmv__fkp] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for oytmv__fkp, (lua__rken, yvogz__qsnt) in enumerate(pm.passes):
        if lua__rken == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(oytmv__fkp)
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
    gftn__gfxo = guard(get_definition, func_ir, rhs.func)
    if isinstance(gftn__gfxo, (ir.Global, ir.FreeVar, ir.Const)):
        erf__bttpn = gftn__gfxo.value
    else:
        cvz__jmi = guard(find_callname, func_ir, rhs)
        if not (cvz__jmi and isinstance(cvz__jmi[0], str) and isinstance(
            cvz__jmi[1], str)):
            return
        func_name, func_mod = cvz__jmi
        try:
            import importlib
            oft__szcth = importlib.import_module(func_mod)
            erf__bttpn = getattr(oft__szcth, func_name)
        except:
            return
    if isinstance(erf__bttpn, CPUDispatcher) and issubclass(erf__bttpn.
        _compiler.pipeline_class, BodoCompiler
        ) and erf__bttpn._compiler.pipeline_class != BodoCompilerUDF:
        erf__bttpn._compiler.pipeline_class = BodoCompilerUDF
        erf__bttpn.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for uvbp__myr in block.body:
                if is_call_assign(uvbp__myr):
                    _convert_bodo_dispatcher_to_udf(uvbp__myr.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        wbfsk__skftg = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        wbfsk__skftg.run()
        return True


def _update_definitions(func_ir, node_list):
    fzh__xrvlx = ir.Loc('', 0)
    onp__hdjb = ir.Block(ir.Scope(None, fzh__xrvlx), fzh__xrvlx)
    onp__hdjb.body = node_list
    build_definitions({(0): onp__hdjb}, func_ir._definitions)


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
        agqpc__bvrs = 'overload_series_' + rhs.attr
        ohkhz__xut = getattr(bodo.hiframes.series_impl, agqpc__bvrs)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        agqpc__bvrs = 'overload_dataframe_' + rhs.attr
        ohkhz__xut = getattr(bodo.hiframes.dataframe_impl, agqpc__bvrs)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    qpub__rmwy = ohkhz__xut(rhs_type)
    xrk__mrg = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    cjs__hnczp = compile_func_single_block(qpub__rmwy, (rhs.value,), stmt.
        target, xrk__mrg)
    _update_definitions(func_ir, cjs__hnczp)
    new_body += cjs__hnczp
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
        suyef__okd = tuple(typemap[dbmp__dtil.name] for dbmp__dtil in rhs.args)
        wsg__ical = {cgx__vulkt: typemap[dbmp__dtil.name] for cgx__vulkt,
            dbmp__dtil in dict(rhs.kws).items()}
        qpub__rmwy = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*suyef__okd, **wsg__ical)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        suyef__okd = tuple(typemap[dbmp__dtil.name] for dbmp__dtil in rhs.args)
        wsg__ical = {cgx__vulkt: typemap[dbmp__dtil.name] for cgx__vulkt,
            dbmp__dtil in dict(rhs.kws).items()}
        qpub__rmwy = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*suyef__okd, **wsg__ical)
    else:
        return False
    cojt__vjk = replace_func(pass_info, qpub__rmwy, rhs.args, pysig=numba.
        core.utils.pysignature(qpub__rmwy), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    jhcyc__cedwc, yvogz__qsnt = inline_closure_call(func_ir, cojt__vjk.
        glbls, block, len(new_body), cojt__vjk.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=cojt__vjk.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for uotob__ppc in jhcyc__cedwc.values():
        uotob__ppc.loc = rhs.loc
        update_locs(uotob__ppc.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    qoexn__lvof = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = qoexn__lvof(func_ir, typemap)
    fqwzu__eer = func_ir.blocks
    work_list = list((gbv__zalr, fqwzu__eer[gbv__zalr]) for gbv__zalr in
        reversed(fqwzu__eer.keys()))
    while work_list:
        zzvt__vywdq, block = work_list.pop()
        new_body = []
        xcn__hkxio = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                cvz__jmi = guard(find_callname, func_ir, rhs, typemap)
                if cvz__jmi is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = cvz__jmi
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    xcn__hkxio = True
                    break
            new_body.append(stmt)
        if not xcn__hkxio:
            fqwzu__eer[zzvt__vywdq].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        wlov__hpr = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = wlov__hpr.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        akv__zhb = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        luku__pzm = akv__zhb.run()
        klmn__aqzxr = luku__pzm
        if klmn__aqzxr:
            klmn__aqzxr = akv__zhb.run()
        if klmn__aqzxr:
            akv__zhb.run()
        return luku__pzm


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        cexm__jdwe = 0
        urg__cjuyz = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            cexm__jdwe = int(os.environ[urg__cjuyz])
        except:
            pass
        if cexm__jdwe > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(cexm__jdwe,
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
        xrk__mrg = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, xrk__mrg)
        for block in state.func_ir.blocks.values():
            new_body = []
            for uvbp__myr in block.body:
                if type(uvbp__myr) in distributed_run_extensions:
                    zvh__tkpl = distributed_run_extensions[type(uvbp__myr)]
                    tpfcb__sxtud = zvh__tkpl(uvbp__myr, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += tpfcb__sxtud
                elif is_call_assign(uvbp__myr):
                    rhs = uvbp__myr.value
                    cvz__jmi = guard(find_callname, state.func_ir, rhs)
                    if cvz__jmi == ('gatherv', 'bodo') or cvz__jmi == (
                        'allgatherv', 'bodo'):
                        deui__tcm = state.typemap[uvbp__myr.target.name]
                        qwvag__keks = state.typemap[rhs.args[0].name]
                        if isinstance(qwvag__keks, types.Array) and isinstance(
                            deui__tcm, types.Array):
                            dmwa__frsw = qwvag__keks.copy(readonly=False)
                            gye__buh = deui__tcm.copy(readonly=False)
                            if dmwa__frsw == gye__buh:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), uvbp__myr.target, xrk__mrg)
                                continue
                        if (deui__tcm != qwvag__keks and 
                            to_str_arr_if_dict_array(deui__tcm) ==
                            to_str_arr_if_dict_array(qwvag__keks)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), uvbp__myr.target, xrk__mrg,
                                extra_globals={'decode_if_dict_array':
                                decode_if_dict_array})
                            continue
                        else:
                            uvbp__myr.value = rhs.args[0]
                    new_body.append(uvbp__myr)
                else:
                    new_body.append(uvbp__myr)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        gcjs__wwa = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return gcjs__wwa.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    uhm__tartr = set()
    while work_list:
        zzvt__vywdq, block = work_list.pop()
        uhm__tartr.add(zzvt__vywdq)
        for i, uag__uuoj in enumerate(block.body):
            if isinstance(uag__uuoj, ir.Assign):
                wllyo__ypm = uag__uuoj.value
                if isinstance(wllyo__ypm, ir.Expr) and wllyo__ypm.op == 'call':
                    gftn__gfxo = guard(get_definition, func_ir, wllyo__ypm.func
                        )
                    if isinstance(gftn__gfxo, (ir.Global, ir.FreeVar)
                        ) and isinstance(gftn__gfxo.value, CPUDispatcher
                        ) and issubclass(gftn__gfxo.value._compiler.
                        pipeline_class, BodoCompiler):
                        rorxn__vytnt = gftn__gfxo.value.py_func
                        arg_types = None
                        if typingctx:
                            bmhbm__xnrvp = dict(wllyo__ypm.kws)
                            ygb__aqum = tuple(typemap[dbmp__dtil.name] for
                                dbmp__dtil in wllyo__ypm.args)
                            cos__eowx = {wyy__mjqc: typemap[dbmp__dtil.name
                                ] for wyy__mjqc, dbmp__dtil in bmhbm__xnrvp
                                .items()}
                            yvogz__qsnt, arg_types = (gftn__gfxo.value.
                                fold_argument_types(ygb__aqum, cos__eowx))
                        yvogz__qsnt, vlc__zxcf = inline_closure_call(func_ir,
                            rorxn__vytnt.__globals__, block, i,
                            rorxn__vytnt, typingctx=typingctx, targetctx=
                            targetctx, arg_typs=arg_types, typemap=typemap,
                            calltypes=calltypes, work_list=work_list)
                        _locals.update((vlc__zxcf[wyy__mjqc].name,
                            dbmp__dtil) for wyy__mjqc, dbmp__dtil in
                            gftn__gfxo.value.locals.items() if wyy__mjqc in
                            vlc__zxcf)
                        break
    return uhm__tartr


def udf_jit(signature_or_function=None, **options):
    euvr__mfdhc = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=euvr__mfdhc,
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
    for oytmv__fkp, (lua__rken, yvogz__qsnt) in enumerate(pm.passes):
        if lua__rken == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:oytmv__fkp + 1]
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
    glvn__aakwk = None
    odfus__bxmmy = None
    _locals = {}
    khg__mef = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(khg__mef, arg_types,
        kw_types)
    ykqw__hba = numba.core.compiler.Flags()
    czymc__ypcbv = {'comprehension': True, 'setitem': False,
        'inplace_binop': False, 'reduction': True, 'numpy': True, 'stencil':
        False, 'fusion': True}
    pxoi__rzxe = {'nopython': True, 'boundscheck': False, 'parallel':
        czymc__ypcbv}
    numba.core.registry.cpu_target.options.parse_as_flags(ykqw__hba, pxoi__rzxe
        )
    urkj__mre = TyperCompiler(typingctx, targetctx, glvn__aakwk, args,
        odfus__bxmmy, ykqw__hba, _locals)
    return urkj__mre.compile_extra(func)
