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
        imk__mev = 'bodo' if distributed else 'bodo_seq'
        imk__mev = imk__mev + '_inline' if inline_calls_pass else imk__mev
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, imk__mev)
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
    for esu__sfhft, (hnbj__ttcn, oqfi__awed) in enumerate(pm.passes):
        if hnbj__ttcn == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(esu__sfhft, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for esu__sfhft, (hnbj__ttcn, oqfi__awed) in enumerate(pm.passes):
        if hnbj__ttcn == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[esu__sfhft] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for esu__sfhft, (hnbj__ttcn, oqfi__awed) in enumerate(pm.passes):
        if hnbj__ttcn == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(esu__sfhft)
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
    xrau__out = guard(get_definition, func_ir, rhs.func)
    if isinstance(xrau__out, (ir.Global, ir.FreeVar, ir.Const)):
        xtu__xcfs = xrau__out.value
    else:
        ljaxq__dda = guard(find_callname, func_ir, rhs)
        if not (ljaxq__dda and isinstance(ljaxq__dda[0], str) and
            isinstance(ljaxq__dda[1], str)):
            return
        func_name, func_mod = ljaxq__dda
        try:
            import importlib
            vtxae__lys = importlib.import_module(func_mod)
            xtu__xcfs = getattr(vtxae__lys, func_name)
        except:
            return
    if isinstance(xtu__xcfs, CPUDispatcher) and issubclass(xtu__xcfs.
        _compiler.pipeline_class, BodoCompiler
        ) and xtu__xcfs._compiler.pipeline_class != BodoCompilerUDF:
        xtu__xcfs._compiler.pipeline_class = BodoCompilerUDF
        xtu__xcfs.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for kuy__zosb in block.body:
                if is_call_assign(kuy__zosb):
                    _convert_bodo_dispatcher_to_udf(kuy__zosb.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        uxpou__plpbr = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        uxpou__plpbr.run()
        return True


def _update_definitions(func_ir, node_list):
    jsos__wez = ir.Loc('', 0)
    syxtw__autq = ir.Block(ir.Scope(None, jsos__wez), jsos__wez)
    syxtw__autq.body = node_list
    build_definitions({(0): syxtw__autq}, func_ir._definitions)


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
        har__rmuc = 'overload_series_' + rhs.attr
        aknzy__rhepf = getattr(bodo.hiframes.series_impl, har__rmuc)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        har__rmuc = 'overload_dataframe_' + rhs.attr
        aknzy__rhepf = getattr(bodo.hiframes.dataframe_impl, har__rmuc)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    ymod__fltov = aknzy__rhepf(rhs_type)
    beowp__cwx = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    rng__ehh = compile_func_single_block(ymod__fltov, (rhs.value,), stmt.
        target, beowp__cwx)
    _update_definitions(func_ir, rng__ehh)
    new_body += rng__ehh
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
        mghm__khwey = tuple(typemap[emht__medzv.name] for emht__medzv in
            rhs.args)
        xgjvd__nhau = {imk__mev: typemap[emht__medzv.name] for imk__mev,
            emht__medzv in dict(rhs.kws).items()}
        ymod__fltov = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*mghm__khwey, **xgjvd__nhau)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        mghm__khwey = tuple(typemap[emht__medzv.name] for emht__medzv in
            rhs.args)
        xgjvd__nhau = {imk__mev: typemap[emht__medzv.name] for imk__mev,
            emht__medzv in dict(rhs.kws).items()}
        ymod__fltov = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*mghm__khwey, **xgjvd__nhau)
    else:
        return False
    folw__rhj = replace_func(pass_info, ymod__fltov, rhs.args, pysig=numba.
        core.utils.pysignature(ymod__fltov), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    fuhlz__wlbwc, oqfi__awed = inline_closure_call(func_ir, folw__rhj.glbls,
        block, len(new_body), folw__rhj.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=folw__rhj.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for poa__guscg in fuhlz__wlbwc.values():
        poa__guscg.loc = rhs.loc
        update_locs(poa__guscg.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    becn__spn = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = becn__spn(func_ir, typemap)
    bhet__ccx = func_ir.blocks
    work_list = list((jcskr__skd, bhet__ccx[jcskr__skd]) for jcskr__skd in
        reversed(bhet__ccx.keys()))
    while work_list:
        oilse__qrshu, block = work_list.pop()
        new_body = []
        zosc__nwya = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                ljaxq__dda = guard(find_callname, func_ir, rhs, typemap)
                if ljaxq__dda is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = ljaxq__dda
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    zosc__nwya = True
                    break
            new_body.append(stmt)
        if not zosc__nwya:
            bhet__ccx[oilse__qrshu].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        nmous__mgd = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = nmous__mgd.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        nnnia__lerus = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        eyuh__qdg = nnnia__lerus.run()
        eslih__kiyff = eyuh__qdg
        if eslih__kiyff:
            eslih__kiyff = nnnia__lerus.run()
        if eslih__kiyff:
            nnnia__lerus.run()
        return eyuh__qdg


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        acrf__lifl = 0
        axzug__negg = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            acrf__lifl = int(os.environ[axzug__negg])
        except:
            pass
        if acrf__lifl > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(acrf__lifl,
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
        beowp__cwx = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, beowp__cwx)
        for block in state.func_ir.blocks.values():
            new_body = []
            for kuy__zosb in block.body:
                if type(kuy__zosb) in distributed_run_extensions:
                    rszq__zuge = distributed_run_extensions[type(kuy__zosb)]
                    flx__cvxa = rszq__zuge(kuy__zosb, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += flx__cvxa
                elif is_call_assign(kuy__zosb):
                    rhs = kuy__zosb.value
                    ljaxq__dda = guard(find_callname, state.func_ir, rhs)
                    if ljaxq__dda == ('gatherv', 'bodo') or ljaxq__dda == (
                        'allgatherv', 'bodo'):
                        sso__tzhsx = state.typemap[kuy__zosb.target.name]
                        pilly__egep = state.typemap[rhs.args[0].name]
                        if isinstance(pilly__egep, types.Array) and isinstance(
                            sso__tzhsx, types.Array):
                            nyb__htohl = pilly__egep.copy(readonly=False)
                            luewe__iqyv = sso__tzhsx.copy(readonly=False)
                            if nyb__htohl == luewe__iqyv:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), kuy__zosb.target, beowp__cwx)
                                continue
                        if (sso__tzhsx != pilly__egep and 
                            to_str_arr_if_dict_array(sso__tzhsx) ==
                            to_str_arr_if_dict_array(pilly__egep)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), kuy__zosb.target,
                                beowp__cwx, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            kuy__zosb.value = rhs.args[0]
                    new_body.append(kuy__zosb)
                else:
                    new_body.append(kuy__zosb)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        vfhd__lahx = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return vfhd__lahx.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    ckn__rcsx = set()
    while work_list:
        oilse__qrshu, block = work_list.pop()
        ckn__rcsx.add(oilse__qrshu)
        for i, wbdlm__kdby in enumerate(block.body):
            if isinstance(wbdlm__kdby, ir.Assign):
                ejibm__cjf = wbdlm__kdby.value
                if isinstance(ejibm__cjf, ir.Expr) and ejibm__cjf.op == 'call':
                    xrau__out = guard(get_definition, func_ir, ejibm__cjf.func)
                    if isinstance(xrau__out, (ir.Global, ir.FreeVar)
                        ) and isinstance(xrau__out.value, CPUDispatcher
                        ) and issubclass(xrau__out.value._compiler.
                        pipeline_class, BodoCompiler):
                        zybo__iilf = xrau__out.value.py_func
                        arg_types = None
                        if typingctx:
                            zfu__wqvao = dict(ejibm__cjf.kws)
                            vjp__xdv = tuple(typemap[emht__medzv.name] for
                                emht__medzv in ejibm__cjf.args)
                            yxhs__sqz = {zdo__hgvbr: typemap[emht__medzv.
                                name] for zdo__hgvbr, emht__medzv in
                                zfu__wqvao.items()}
                            oqfi__awed, arg_types = (xrau__out.value.
                                fold_argument_types(vjp__xdv, yxhs__sqz))
                        oqfi__awed, cix__xma = inline_closure_call(func_ir,
                            zybo__iilf.__globals__, block, i, zybo__iilf,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((cix__xma[zdo__hgvbr].name,
                            emht__medzv) for zdo__hgvbr, emht__medzv in
                            xrau__out.value.locals.items() if zdo__hgvbr in
                            cix__xma)
                        break
    return ckn__rcsx


def udf_jit(signature_or_function=None, **options):
    tma__ehkx = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=tma__ehkx,
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
    for esu__sfhft, (hnbj__ttcn, oqfi__awed) in enumerate(pm.passes):
        if hnbj__ttcn == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:esu__sfhft + 1]
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
    ybyvv__rwnn = None
    azoxf__vbkp = None
    _locals = {}
    pwh__iqc = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(pwh__iqc, arg_types,
        kw_types)
    dne__lsq = numba.core.compiler.Flags()
    jxuge__gmx = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    ztmjf__jfc = {'nopython': True, 'boundscheck': False, 'parallel':
        jxuge__gmx}
    numba.core.registry.cpu_target.options.parse_as_flags(dne__lsq, ztmjf__jfc)
    zhop__iss = TyperCompiler(typingctx, targetctx, ybyvv__rwnn, args,
        azoxf__vbkp, dne__lsq, _locals)
    return zhop__iss.compile_extra(func)
