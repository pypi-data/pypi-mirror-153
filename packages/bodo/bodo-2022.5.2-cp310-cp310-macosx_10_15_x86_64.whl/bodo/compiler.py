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
        ndtjn__qeis = 'bodo' if distributed else 'bodo_seq'
        ndtjn__qeis = (ndtjn__qeis + '_inline' if inline_calls_pass else
            ndtjn__qeis)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            ndtjn__qeis)
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
    for qtrnu__ssor, (bhybt__cgx, kcl__thtmz) in enumerate(pm.passes):
        if bhybt__cgx == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(qtrnu__ssor, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for qtrnu__ssor, (bhybt__cgx, kcl__thtmz) in enumerate(pm.passes):
        if bhybt__cgx == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[qtrnu__ssor] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for qtrnu__ssor, (bhybt__cgx, kcl__thtmz) in enumerate(pm.passes):
        if bhybt__cgx == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(qtrnu__ssor)
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
    qyv__uvceg = guard(get_definition, func_ir, rhs.func)
    if isinstance(qyv__uvceg, (ir.Global, ir.FreeVar, ir.Const)):
        dxnnq__ywslz = qyv__uvceg.value
    else:
        xusf__xbv = guard(find_callname, func_ir, rhs)
        if not (xusf__xbv and isinstance(xusf__xbv[0], str) and isinstance(
            xusf__xbv[1], str)):
            return
        func_name, func_mod = xusf__xbv
        try:
            import importlib
            yrb__mmkc = importlib.import_module(func_mod)
            dxnnq__ywslz = getattr(yrb__mmkc, func_name)
        except:
            return
    if isinstance(dxnnq__ywslz, CPUDispatcher) and issubclass(dxnnq__ywslz.
        _compiler.pipeline_class, BodoCompiler
        ) and dxnnq__ywslz._compiler.pipeline_class != BodoCompilerUDF:
        dxnnq__ywslz._compiler.pipeline_class = BodoCompilerUDF
        dxnnq__ywslz.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for qll__norc in block.body:
                if is_call_assign(qll__norc):
                    _convert_bodo_dispatcher_to_udf(qll__norc.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        wytya__seuuw = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        wytya__seuuw.run()
        return True


def _update_definitions(func_ir, node_list):
    rzd__hihj = ir.Loc('', 0)
    lsiff__wuvs = ir.Block(ir.Scope(None, rzd__hihj), rzd__hihj)
    lsiff__wuvs.body = node_list
    build_definitions({(0): lsiff__wuvs}, func_ir._definitions)


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
        pej__kcaaj = 'overload_series_' + rhs.attr
        ehxtj__vcca = getattr(bodo.hiframes.series_impl, pej__kcaaj)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        pej__kcaaj = 'overload_dataframe_' + rhs.attr
        ehxtj__vcca = getattr(bodo.hiframes.dataframe_impl, pej__kcaaj)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    rkthu__csagg = ehxtj__vcca(rhs_type)
    olew__fhhb = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    hrab__axmt = compile_func_single_block(rkthu__csagg, (rhs.value,), stmt
        .target, olew__fhhb)
    _update_definitions(func_ir, hrab__axmt)
    new_body += hrab__axmt
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
        ste__bvzl = tuple(typemap[hxku__ctrlb.name] for hxku__ctrlb in rhs.args
            )
        rjtu__uero = {ndtjn__qeis: typemap[hxku__ctrlb.name] for 
            ndtjn__qeis, hxku__ctrlb in dict(rhs.kws).items()}
        rkthu__csagg = getattr(bodo.hiframes.series_impl, 
            'overload_series_' + func_name)(*ste__bvzl, **rjtu__uero)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        ste__bvzl = tuple(typemap[hxku__ctrlb.name] for hxku__ctrlb in rhs.args
            )
        rjtu__uero = {ndtjn__qeis: typemap[hxku__ctrlb.name] for 
            ndtjn__qeis, hxku__ctrlb in dict(rhs.kws).items()}
        rkthu__csagg = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*ste__bvzl, **rjtu__uero)
    else:
        return False
    xyhp__uggyv = replace_func(pass_info, rkthu__csagg, rhs.args, pysig=
        numba.core.utils.pysignature(rkthu__csagg), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    sujw__phjop, kcl__thtmz = inline_closure_call(func_ir, xyhp__uggyv.
        glbls, block, len(new_body), xyhp__uggyv.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=xyhp__uggyv.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for nbjq__ehk in sujw__phjop.values():
        nbjq__ehk.loc = rhs.loc
        update_locs(nbjq__ehk.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    blkpw__hfde = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = blkpw__hfde(func_ir, typemap)
    qkgvr__csxl = func_ir.blocks
    work_list = list((uen__lqcvl, qkgvr__csxl[uen__lqcvl]) for uen__lqcvl in
        reversed(qkgvr__csxl.keys()))
    while work_list:
        naof__jgc, block = work_list.pop()
        new_body = []
        dowu__wwmvf = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                xusf__xbv = guard(find_callname, func_ir, rhs, typemap)
                if xusf__xbv is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = xusf__xbv
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    dowu__wwmvf = True
                    break
            new_body.append(stmt)
        if not dowu__wwmvf:
            qkgvr__csxl[naof__jgc].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        szbzh__berq = DistributedPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = szbzh__berq.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        poi__xidji = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        mfye__ahiiz = poi__xidji.run()
        ylru__izmr = mfye__ahiiz
        if ylru__izmr:
            ylru__izmr = poi__xidji.run()
        if ylru__izmr:
            poi__xidji.run()
        return mfye__ahiiz


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        knbc__dbiy = 0
        ioew__xttu = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            knbc__dbiy = int(os.environ[ioew__xttu])
        except:
            pass
        if knbc__dbiy > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(knbc__dbiy,
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
        olew__fhhb = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, olew__fhhb)
        for block in state.func_ir.blocks.values():
            new_body = []
            for qll__norc in block.body:
                if type(qll__norc) in distributed_run_extensions:
                    rkkf__xzk = distributed_run_extensions[type(qll__norc)]
                    zisc__qgp = rkkf__xzk(qll__norc, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += zisc__qgp
                elif is_call_assign(qll__norc):
                    rhs = qll__norc.value
                    xusf__xbv = guard(find_callname, state.func_ir, rhs)
                    if xusf__xbv == ('gatherv', 'bodo') or xusf__xbv == (
                        'allgatherv', 'bodo'):
                        uajmc__dai = state.typemap[qll__norc.target.name]
                        ogk__uhir = state.typemap[rhs.args[0].name]
                        if isinstance(ogk__uhir, types.Array) and isinstance(
                            uajmc__dai, types.Array):
                            xgnqe__tdfst = ogk__uhir.copy(readonly=False)
                            bsyg__eyoq = uajmc__dai.copy(readonly=False)
                            if xgnqe__tdfst == bsyg__eyoq:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), qll__norc.target, olew__fhhb)
                                continue
                        if (uajmc__dai != ogk__uhir and 
                            to_str_arr_if_dict_array(uajmc__dai) ==
                            to_str_arr_if_dict_array(ogk__uhir)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), qll__norc.target,
                                olew__fhhb, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            qll__norc.value = rhs.args[0]
                    new_body.append(qll__norc)
                else:
                    new_body.append(qll__norc)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        hoy__qjl = TableColumnDelPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes)
        return hoy__qjl.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    kwmvg__vjf = set()
    while work_list:
        naof__jgc, block = work_list.pop()
        kwmvg__vjf.add(naof__jgc)
        for i, gjzqs__zabz in enumerate(block.body):
            if isinstance(gjzqs__zabz, ir.Assign):
                xgbt__msp = gjzqs__zabz.value
                if isinstance(xgbt__msp, ir.Expr) and xgbt__msp.op == 'call':
                    qyv__uvceg = guard(get_definition, func_ir, xgbt__msp.func)
                    if isinstance(qyv__uvceg, (ir.Global, ir.FreeVar)
                        ) and isinstance(qyv__uvceg.value, CPUDispatcher
                        ) and issubclass(qyv__uvceg.value._compiler.
                        pipeline_class, BodoCompiler):
                        qplmm__vkwxg = qyv__uvceg.value.py_func
                        arg_types = None
                        if typingctx:
                            mdii__iwth = dict(xgbt__msp.kws)
                            dceqg__kfih = tuple(typemap[hxku__ctrlb.name] for
                                hxku__ctrlb in xgbt__msp.args)
                            jzmv__zvdyh = {ecpxn__xasb: typemap[hxku__ctrlb
                                .name] for ecpxn__xasb, hxku__ctrlb in
                                mdii__iwth.items()}
                            kcl__thtmz, arg_types = (qyv__uvceg.value.
                                fold_argument_types(dceqg__kfih, jzmv__zvdyh))
                        kcl__thtmz, ufs__nagj = inline_closure_call(func_ir,
                            qplmm__vkwxg.__globals__, block, i,
                            qplmm__vkwxg, typingctx=typingctx, targetctx=
                            targetctx, arg_typs=arg_types, typemap=typemap,
                            calltypes=calltypes, work_list=work_list)
                        _locals.update((ufs__nagj[ecpxn__xasb].name,
                            hxku__ctrlb) for ecpxn__xasb, hxku__ctrlb in
                            qyv__uvceg.value.locals.items() if ecpxn__xasb in
                            ufs__nagj)
                        break
    return kwmvg__vjf


def udf_jit(signature_or_function=None, **options):
    dmp__xctb = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=dmp__xctb,
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
    for qtrnu__ssor, (bhybt__cgx, kcl__thtmz) in enumerate(pm.passes):
        if bhybt__cgx == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:qtrnu__ssor + 1]
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
    zsfeo__awhd = None
    hgxcp__ubp = None
    _locals = {}
    jnnpm__zrvly = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(jnnpm__zrvly, arg_types,
        kw_types)
    gvwlw__mrutp = numba.core.compiler.Flags()
    qogs__kon = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    pyvdi__dsp = {'nopython': True, 'boundscheck': False, 'parallel': qogs__kon
        }
    numba.core.registry.cpu_target.options.parse_as_flags(gvwlw__mrutp,
        pyvdi__dsp)
    kjfjg__hpzn = TyperCompiler(typingctx, targetctx, zsfeo__awhd, args,
        hgxcp__ubp, gvwlw__mrutp, _locals)
    return kjfjg__hpzn.compile_extra(func)
