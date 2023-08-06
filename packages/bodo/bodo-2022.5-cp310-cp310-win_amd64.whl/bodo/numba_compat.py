"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    pont__olvxj = numba.core.bytecode.FunctionIdentity.from_function(func)
    acon__ljyhd = numba.core.interpreter.Interpreter(pont__olvxj)
    nncq__pswgo = numba.core.bytecode.ByteCode(func_id=pont__olvxj)
    func_ir = acon__ljyhd.interpret(nncq__pswgo)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        vesjg__ton = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        vesjg__ton.run()
    eqa__tsc = numba.core.postproc.PostProcessor(func_ir)
    eqa__tsc.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, eqf__bwnia in visit_vars_extensions.items():
        if isinstance(stmt, t):
            eqf__bwnia(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    rlga__ujcq = ['ravel', 'transpose', 'reshape']
    for wauhh__quye in blocks.values():
        for esyd__czq in wauhh__quye.body:
            if type(esyd__czq) in alias_analysis_extensions:
                eqf__bwnia = alias_analysis_extensions[type(esyd__czq)]
                eqf__bwnia(esyd__czq, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(esyd__czq, ir.Assign):
                uzni__iupby = esyd__czq.value
                kapl__mth = esyd__czq.target.name
                if is_immutable_type(kapl__mth, typemap):
                    continue
                if isinstance(uzni__iupby, ir.Var
                    ) and kapl__mth != uzni__iupby.name:
                    _add_alias(kapl__mth, uzni__iupby.name, alias_map,
                        arg_aliases)
                if isinstance(uzni__iupby, ir.Expr) and (uzni__iupby.op ==
                    'cast' or uzni__iupby.op in ['getitem', 'static_getitem']):
                    _add_alias(kapl__mth, uzni__iupby.value.name, alias_map,
                        arg_aliases)
                if isinstance(uzni__iupby, ir.Expr
                    ) and uzni__iupby.op == 'inplace_binop':
                    _add_alias(kapl__mth, uzni__iupby.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(uzni__iupby, ir.Expr
                    ) and uzni__iupby.op == 'getattr' and uzni__iupby.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(kapl__mth, uzni__iupby.value.name, alias_map,
                        arg_aliases)
                if isinstance(uzni__iupby, ir.Expr
                    ) and uzni__iupby.op == 'getattr' and uzni__iupby.attr not in [
                    'shape'] and uzni__iupby.value.name in arg_aliases:
                    _add_alias(kapl__mth, uzni__iupby.value.name, alias_map,
                        arg_aliases)
                if isinstance(uzni__iupby, ir.Expr
                    ) and uzni__iupby.op == 'getattr' and uzni__iupby.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(kapl__mth, uzni__iupby.value.name, alias_map,
                        arg_aliases)
                if isinstance(uzni__iupby, ir.Expr) and uzni__iupby.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(kapl__mth, typemap):
                    for glyq__hikd in uzni__iupby.items:
                        _add_alias(kapl__mth, glyq__hikd.name, alias_map,
                            arg_aliases)
                if isinstance(uzni__iupby, ir.Expr
                    ) and uzni__iupby.op == 'call':
                    njh__zorjw = guard(find_callname, func_ir, uzni__iupby,
                        typemap)
                    if njh__zorjw is None:
                        continue
                    fclot__kvgn, bamd__odpc = njh__zorjw
                    if njh__zorjw in alias_func_extensions:
                        pver__xnw = alias_func_extensions[njh__zorjw]
                        pver__xnw(kapl__mth, uzni__iupby.args, alias_map,
                            arg_aliases)
                    if bamd__odpc == 'numpy' and fclot__kvgn in rlga__ujcq:
                        _add_alias(kapl__mth, uzni__iupby.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(bamd__odpc, ir.Var
                        ) and fclot__kvgn in rlga__ujcq:
                        _add_alias(kapl__mth, bamd__odpc.name, alias_map,
                            arg_aliases)
    uehle__vihe = copy.deepcopy(alias_map)
    for glyq__hikd in uehle__vihe:
        for jnyw__mzaxe in uehle__vihe[glyq__hikd]:
            alias_map[glyq__hikd] |= alias_map[jnyw__mzaxe]
        for jnyw__mzaxe in uehle__vihe[glyq__hikd]:
            alias_map[jnyw__mzaxe] = alias_map[glyq__hikd]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    cxdr__doh = compute_cfg_from_blocks(func_ir.blocks)
    eqx__nbu = compute_use_defs(func_ir.blocks)
    mvmr__vnht = compute_live_map(cxdr__doh, func_ir.blocks, eqx__nbu.
        usemap, eqx__nbu.defmap)
    lbmo__ghgys = True
    while lbmo__ghgys:
        lbmo__ghgys = False
        for wkskp__zftj, block in func_ir.blocks.items():
            lives = {glyq__hikd.name for glyq__hikd in block.terminator.
                list_vars()}
            for mvqr__pfs, ypur__blm in cxdr__doh.successors(wkskp__zftj):
                lives |= mvmr__vnht[mvqr__pfs]
            jtcr__xyyy = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    kapl__mth = stmt.target
                    ryul__and = stmt.value
                    if kapl__mth.name not in lives:
                        if isinstance(ryul__and, ir.Expr
                            ) and ryul__and.op == 'make_function':
                            continue
                        if isinstance(ryul__and, ir.Expr
                            ) and ryul__and.op == 'getattr':
                            continue
                        if isinstance(ryul__and, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(kapl__mth,
                            None), types.Function):
                            continue
                        if isinstance(ryul__and, ir.Expr
                            ) and ryul__and.op == 'build_map':
                            continue
                        if isinstance(ryul__and, ir.Expr
                            ) and ryul__and.op == 'build_tuple':
                            continue
                    if isinstance(ryul__and, ir.Var
                        ) and kapl__mth.name == ryul__and.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    ufzv__garkv = analysis.ir_extension_usedefs[type(stmt)]
                    pnymi__ngd, goou__dwd = ufzv__garkv(stmt)
                    lives -= goou__dwd
                    lives |= pnymi__ngd
                else:
                    lives |= {glyq__hikd.name for glyq__hikd in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(kapl__mth.name)
                jtcr__xyyy.append(stmt)
            jtcr__xyyy.reverse()
            if len(block.body) != len(jtcr__xyyy):
                lbmo__ghgys = True
            block.body = jtcr__xyyy


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    nctn__creaz = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (nctn__creaz,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    ldir__gzkkn = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), ldir__gzkkn)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for bqoca__xgptm in fnty.templates:
                self._inline_overloads.update(bqoca__xgptm._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    ldir__gzkkn = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), ldir__gzkkn)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    xpxpz__pispn, meh__bxlf = self._get_impl(args, kws)
    if xpxpz__pispn is None:
        return
    vko__unm = types.Dispatcher(xpxpz__pispn)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        oenbs__osz = xpxpz__pispn._compiler
        flags = compiler.Flags()
        etbuq__urfb = oenbs__osz.targetdescr.typing_context
        cngsl__vzzyl = oenbs__osz.targetdescr.target_context
        knzt__fetsg = oenbs__osz.pipeline_class(etbuq__urfb, cngsl__vzzyl,
            None, None, None, flags, None)
        lkrq__mokre = InlineWorker(etbuq__urfb, cngsl__vzzyl, oenbs__osz.
            locals, knzt__fetsg, flags, None)
        cvoyz__zvtuf = vko__unm.dispatcher.get_call_template
        bqoca__xgptm, wlry__qihtt, gaako__qbry, kws = cvoyz__zvtuf(meh__bxlf,
            kws)
        if gaako__qbry in self._inline_overloads:
            return self._inline_overloads[gaako__qbry]['iinfo'].signature
        ir = lkrq__mokre.run_untyped_passes(vko__unm.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, cngsl__vzzyl, ir, gaako__qbry, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, gaako__qbry, None)
        self._inline_overloads[sig.args] = {'folded_args': gaako__qbry}
        ujb__msw = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = ujb__msw
        if not self._inline.is_always_inline:
            sig = vko__unm.get_call_type(self.context, meh__bxlf, kws)
            self._compiled_overloads[sig.args] = vko__unm.get_overload(sig)
        lwk__ffby = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': gaako__qbry,
            'iinfo': lwk__ffby}
    else:
        sig = vko__unm.get_call_type(self.context, meh__bxlf, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = vko__unm.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    wujiv__dau = [True, False]
    nxl__fmxds = [False, True]
    ydra__odvp = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    rjbpa__zqp = get_local_target(context)
    zpq__efdsj = utils.order_by_target_specificity(rjbpa__zqp, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for zchj__bubgn in zpq__efdsj:
        tshy__shbt = zchj__bubgn(context)
        dcw__weih = wujiv__dau if tshy__shbt.prefer_literal else nxl__fmxds
        dcw__weih = [True] if getattr(tshy__shbt, '_no_unliteral', False
            ) else dcw__weih
        for vok__lucet in dcw__weih:
            try:
                if vok__lucet:
                    sig = tshy__shbt.apply(args, kws)
                else:
                    ddd__vai = tuple([_unlit_non_poison(a) for a in args])
                    pfw__pxxzd = {flmm__odmnq: _unlit_non_poison(glyq__hikd
                        ) for flmm__odmnq, glyq__hikd in kws.items()}
                    sig = tshy__shbt.apply(ddd__vai, pfw__pxxzd)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    ydra__odvp.add_error(tshy__shbt, False, e, vok__lucet)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = tshy__shbt.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    edwt__ombwo = getattr(tshy__shbt, 'cases', None)
                    if edwt__ombwo is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            edwt__ombwo)
                    else:
                        msg = 'No match.'
                    ydra__odvp.add_error(tshy__shbt, True, msg, vok__lucet)
    ydra__odvp.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    bqoca__xgptm = self.template(context)
    sepbp__aqcye = None
    snp__mcgqm = None
    umz__nbv = None
    dcw__weih = [True, False] if bqoca__xgptm.prefer_literal else [False, True]
    dcw__weih = [True] if getattr(bqoca__xgptm, '_no_unliteral', False
        ) else dcw__weih
    for vok__lucet in dcw__weih:
        if vok__lucet:
            try:
                umz__nbv = bqoca__xgptm.apply(args, kws)
            except Exception as dvo__jkhyl:
                if isinstance(dvo__jkhyl, errors.ForceLiteralArg):
                    raise dvo__jkhyl
                sepbp__aqcye = dvo__jkhyl
                umz__nbv = None
            else:
                break
        else:
            emafj__tyf = tuple([_unlit_non_poison(a) for a in args])
            amc__qlmg = {flmm__odmnq: _unlit_non_poison(glyq__hikd) for 
                flmm__odmnq, glyq__hikd in kws.items()}
            qnqvq__shuj = emafj__tyf == args and kws == amc__qlmg
            if not qnqvq__shuj and umz__nbv is None:
                try:
                    umz__nbv = bqoca__xgptm.apply(emafj__tyf, amc__qlmg)
                except Exception as dvo__jkhyl:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        dvo__jkhyl, errors.NumbaError):
                        raise dvo__jkhyl
                    if isinstance(dvo__jkhyl, errors.ForceLiteralArg):
                        if bqoca__xgptm.prefer_literal:
                            raise dvo__jkhyl
                    snp__mcgqm = dvo__jkhyl
                else:
                    break
    if umz__nbv is None and (snp__mcgqm is not None or sepbp__aqcye is not None
        ):
        rggm__wzezp = '- Resolution failure for {} arguments:\n{}\n'
        amw__nko = _termcolor.highlight(rggm__wzezp)
        if numba.core.config.DEVELOPER_MODE:
            bbc__wny = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    bjg__nyjs = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    bjg__nyjs = ['']
                cdibc__nowan = '\n{}'.format(2 * bbc__wny)
                xkb__bguls = _termcolor.reset(cdibc__nowan + cdibc__nowan.
                    join(_bt_as_lines(bjg__nyjs)))
                return _termcolor.reset(xkb__bguls)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            klupv__mtsmy = str(e)
            klupv__mtsmy = klupv__mtsmy if klupv__mtsmy else str(repr(e)
                ) + add_bt(e)
            usp__pqgb = errors.TypingError(textwrap.dedent(klupv__mtsmy))
            return amw__nko.format(literalness, str(usp__pqgb))
        import bodo
        if isinstance(sepbp__aqcye, bodo.utils.typing.BodoError):
            raise sepbp__aqcye
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', sepbp__aqcye) +
                nested_msg('non-literal', snp__mcgqm))
        else:
            if 'missing a required argument' in sepbp__aqcye.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=sepbp__aqcye.loc)
    return umz__nbv


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    fclot__kvgn = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=fclot__kvgn)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            pmzi__mrih = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), pmzi__mrih)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    vqd__okgf = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            vqd__okgf.append(types.Omitted(a.value))
        else:
            vqd__okgf.append(self.typeof_pyval(a))
    nxj__roy = None
    try:
        error = None
        nxj__roy = self.compile(tuple(vqd__okgf))
    except errors.ForceLiteralArg as e:
        kpks__eejy = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if kpks__eejy:
            lvpjw__glki = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            mfvx__prk = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(kpks__eejy))
            raise errors.CompilerError(lvpjw__glki.format(mfvx__prk))
        meh__bxlf = []
        try:
            for i, glyq__hikd in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        meh__bxlf.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        meh__bxlf.append(types.literal(args[i]))
                else:
                    meh__bxlf.append(args[i])
            args = meh__bxlf
        except (OSError, FileNotFoundError) as lev__kehlw:
            error = FileNotFoundError(str(lev__kehlw) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                nxj__roy = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        dbw__haj = []
        for i, vrw__kwn in enumerate(args):
            val = vrw__kwn.value if isinstance(vrw__kwn, numba.core.
                dispatcher.OmittedArg) else vrw__kwn
            try:
                pox__wvl = typeof(val, Purpose.argument)
            except ValueError as vsej__sithr:
                dbw__haj.append((i, str(vsej__sithr)))
            else:
                if pox__wvl is None:
                    dbw__haj.append((i,
                        f'cannot determine Numba type of value {val}'))
        if dbw__haj:
            afx__rqli = '\n'.join(f'- argument {i}: {evbgi__xbx}' for i,
                evbgi__xbx in dbw__haj)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{afx__rqli}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                fwi__uxfxy = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                phzvt__vmb = False
                for xyjm__aura in fwi__uxfxy:
                    if xyjm__aura in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        phzvt__vmb = True
                        break
                if not phzvt__vmb:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                pmzi__mrih = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), pmzi__mrih)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return nxj__roy


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for kuy__ecpi in cres.library._codegen._engine._defined_symbols:
        if kuy__ecpi.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in kuy__ecpi and (
            'bodo_gb_udf_update_local' in kuy__ecpi or 
            'bodo_gb_udf_combine' in kuy__ecpi or 'bodo_gb_udf_eval' in
            kuy__ecpi or 'bodo_gb_apply_general_udfs' in kuy__ecpi):
            gb_agg_cfunc_addr[kuy__ecpi
                ] = cres.library.get_pointer_to_function(kuy__ecpi)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for kuy__ecpi in cres.library._codegen._engine._defined_symbols:
        if kuy__ecpi.startswith('cfunc') and ('get_join_cond_addr' not in
            kuy__ecpi or 'bodo_join_gen_cond' in kuy__ecpi):
            join_gen_cond_cfunc_addr[kuy__ecpi
                ] = cres.library.get_pointer_to_function(kuy__ecpi)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    xpxpz__pispn = self._get_dispatcher_for_current_target()
    if xpxpz__pispn is not self:
        return xpxpz__pispn.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            eyec__ccpb = self.overloads.get(tuple(args))
            if eyec__ccpb is not None:
                return eyec__ccpb.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            gfqa__rot = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=gfqa__rot):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
                if bodo.get_rank() == 0:
                    self._cache.save_overload(sig, cres)
            else:
                gjley__xmp = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in gjley__xmp:
                    self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    dje__dsfa = self._final_module
    zhg__gwt = []
    bwxfh__fiquo = 0
    for fn in dje__dsfa.functions:
        bwxfh__fiquo += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            zhg__gwt.append(fn.name)
    if bwxfh__fiquo == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if zhg__gwt:
        dje__dsfa = dje__dsfa.clone()
        for name in zhg__gwt:
            dje__dsfa.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = dje__dsfa
    return dje__dsfa


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for qauk__dxx in self.constraints:
        loc = qauk__dxx.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                qauk__dxx(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                hgo__rdqpj = numba.core.errors.TypingError(str(e), loc=
                    qauk__dxx.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(hgo__rdqpj, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    hgo__rdqpj = numba.core.errors.TypingError(msg.format(
                        con=qauk__dxx, err=str(e)), loc=qauk__dxx.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(hgo__rdqpj, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for lxg__jbsb in self._failures.values():
        for roirc__bji in lxg__jbsb:
            if isinstance(roirc__bji.error, ForceLiteralArg):
                raise roirc__bji.error
            if isinstance(roirc__bji.error, bodo.utils.typing.BodoError):
                raise roirc__bji.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    nbkp__gdd = False
    jtcr__xyyy = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        brbq__cea = set()
        clfw__asf = lives & alias_set
        for glyq__hikd in clfw__asf:
            brbq__cea |= alias_map[glyq__hikd]
        lives_n_aliases = lives | brbq__cea | arg_aliases
        if type(stmt) in remove_dead_extensions:
            eqf__bwnia = remove_dead_extensions[type(stmt)]
            stmt = eqf__bwnia(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                nbkp__gdd = True
                continue
        if isinstance(stmt, ir.Assign):
            kapl__mth = stmt.target
            ryul__and = stmt.value
            if kapl__mth.name not in lives and has_no_side_effect(ryul__and,
                lives_n_aliases, call_table):
                nbkp__gdd = True
                continue
            if saved_array_analysis and kapl__mth.name in lives and is_expr(
                ryul__and, 'getattr'
                ) and ryul__and.attr == 'shape' and is_array_typ(typemap[
                ryul__and.value.name]) and ryul__and.value.name not in lives:
                efwa__rnv = {glyq__hikd: flmm__odmnq for flmm__odmnq,
                    glyq__hikd in func_ir.blocks.items()}
                if block in efwa__rnv:
                    wkskp__zftj = efwa__rnv[block]
                    caz__vlw = saved_array_analysis.get_equiv_set(wkskp__zftj)
                    uxso__isbaf = caz__vlw.get_equiv_set(ryul__and.value)
                    if uxso__isbaf is not None:
                        for glyq__hikd in uxso__isbaf:
                            if glyq__hikd.endswith('#0'):
                                glyq__hikd = glyq__hikd[:-2]
                            if glyq__hikd in typemap and is_array_typ(typemap
                                [glyq__hikd]) and glyq__hikd in lives:
                                ryul__and.value = ir.Var(ryul__and.value.
                                    scope, glyq__hikd, ryul__and.value.loc)
                                nbkp__gdd = True
                                break
            if isinstance(ryul__and, ir.Var
                ) and kapl__mth.name == ryul__and.name:
                nbkp__gdd = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                nbkp__gdd = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            ufzv__garkv = analysis.ir_extension_usedefs[type(stmt)]
            pnymi__ngd, goou__dwd = ufzv__garkv(stmt)
            lives -= goou__dwd
            lives |= pnymi__ngd
        else:
            lives |= {glyq__hikd.name for glyq__hikd in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                xfcdc__wxr = set()
                if isinstance(ryul__and, ir.Expr):
                    xfcdc__wxr = {glyq__hikd.name for glyq__hikd in
                        ryul__and.list_vars()}
                if kapl__mth.name not in xfcdc__wxr:
                    lives.remove(kapl__mth.name)
        jtcr__xyyy.append(stmt)
    jtcr__xyyy.reverse()
    block.body = jtcr__xyyy
    return nbkp__gdd


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            jogc__orcjc, = args
            if isinstance(jogc__orcjc, types.IterableType):
                dtype = jogc__orcjc.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), jogc__orcjc)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    roy__xur = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (roy__xur, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as ctcwe__bpswq:
            return
    try:
        return literal(value)
    except LiteralTypingError as ctcwe__bpswq:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        nofpq__nhosw = py_func.__qualname__
    except AttributeError as ctcwe__bpswq:
        nofpq__nhosw = py_func.__name__
    jpy__mwjbi = inspect.getfile(py_func)
    for cls in self._locator_classes:
        czv__sthve = cls.from_function(py_func, jpy__mwjbi)
        if czv__sthve is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (nofpq__nhosw, jpy__mwjbi))
    self._locator = czv__sthve
    irfp__xnbmo = inspect.getfile(py_func)
    bviwi__snnc = os.path.splitext(os.path.basename(irfp__xnbmo))[0]
    if jpy__mwjbi.startswith('<ipython-'):
        ygxax__zxbgd = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', bviwi__snnc, count=1)
        if ygxax__zxbgd == bviwi__snnc:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        bviwi__snnc = ygxax__zxbgd
    pog__ncdz = '%s.%s' % (bviwi__snnc, nofpq__nhosw)
    nbikt__plio = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(pog__ncdz, nbikt__plio)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    xvwxh__euguk = list(filter(lambda a: self._istuple(a.name), args))
    if len(xvwxh__euguk) == 2 and fn.__name__ == 'add':
        rzluc__cqqju = self.typemap[xvwxh__euguk[0].name]
        tdyk__bmlzy = self.typemap[xvwxh__euguk[1].name]
        if rzluc__cqqju.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                xvwxh__euguk[1]))
        if tdyk__bmlzy.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                xvwxh__euguk[0]))
        try:
            loat__lzanc = [equiv_set.get_shape(x) for x in xvwxh__euguk]
            if None in loat__lzanc:
                return None
            nja__swv = sum(loat__lzanc, ())
            return ArrayAnalysis.AnalyzeResult(shape=nja__swv)
        except GuardException as ctcwe__bpswq:
            return None
    vsib__qtxuo = list(filter(lambda a: self._isarray(a.name), args))
    require(len(vsib__qtxuo) > 0)
    wslw__chlq = [x.name for x in vsib__qtxuo]
    whh__uxkxq = [self.typemap[x.name].ndim for x in vsib__qtxuo]
    kufe__mcr = max(whh__uxkxq)
    require(kufe__mcr > 0)
    loat__lzanc = [equiv_set.get_shape(x) for x in vsib__qtxuo]
    if any(a is None for a in loat__lzanc):
        return ArrayAnalysis.AnalyzeResult(shape=vsib__qtxuo[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, vsib__qtxuo))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, loat__lzanc,
        wslw__chlq)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    sdgu__yca = code_obj.code
    bxwcw__gxwnh = len(sdgu__yca.co_freevars)
    xeq__atli = sdgu__yca.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        uurqt__weicy, op = ir_utils.find_build_sequence(caller_ir, code_obj
            .closure)
        assert op == 'build_tuple'
        xeq__atli = [glyq__hikd.name for glyq__hikd in uurqt__weicy]
    xif__yuec = caller_ir.func_id.func.__globals__
    try:
        xif__yuec = getattr(code_obj, 'globals', xif__yuec)
    except KeyError as ctcwe__bpswq:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    slyet__bkwix = []
    for x in xeq__atli:
        try:
            sbah__bcnwi = caller_ir.get_definition(x)
        except KeyError as ctcwe__bpswq:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(sbah__bcnwi, (ir.Const, ir.Global, ir.FreeVar)):
            val = sbah__bcnwi.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                nctn__creaz = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                xif__yuec[nctn__creaz] = bodo.jit(distributed=False)(val)
                xif__yuec[nctn__creaz].is_nested_func = True
                val = nctn__creaz
            if isinstance(val, CPUDispatcher):
                nctn__creaz = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                xif__yuec[nctn__creaz] = val
                val = nctn__creaz
            slyet__bkwix.append(val)
        elif isinstance(sbah__bcnwi, ir.Expr
            ) and sbah__bcnwi.op == 'make_function':
            vtad__sfok = convert_code_obj_to_function(sbah__bcnwi, caller_ir)
            nctn__creaz = ir_utils.mk_unique_var('nested_func').replace('.',
                '_')
            xif__yuec[nctn__creaz] = bodo.jit(distributed=False)(vtad__sfok)
            xif__yuec[nctn__creaz].is_nested_func = True
            slyet__bkwix.append(nctn__creaz)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    cxk__uxft = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        slyet__bkwix)])
    drbtj__gaoe = ','.join([('c_%d' % i) for i in range(bxwcw__gxwnh)])
    zmqan__mpc = list(sdgu__yca.co_varnames)
    ufvaq__qbof = 0
    eve__cbir = sdgu__yca.co_argcount
    flgxv__ihzs = caller_ir.get_definition(code_obj.defaults)
    if flgxv__ihzs is not None:
        if isinstance(flgxv__ihzs, tuple):
            d = [caller_ir.get_definition(x).value for x in flgxv__ihzs]
            pjf__slb = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in flgxv__ihzs.items]
            pjf__slb = tuple(d)
        ufvaq__qbof = len(pjf__slb)
    oxk__pabqy = eve__cbir - ufvaq__qbof
    ovb__rwhbk = ','.join([('%s' % zmqan__mpc[i]) for i in range(oxk__pabqy)])
    if ufvaq__qbof:
        jtru__mpcxr = [('%s = %s' % (zmqan__mpc[i + oxk__pabqy], pjf__slb[i
            ])) for i in range(ufvaq__qbof)]
        ovb__rwhbk += ', '
        ovb__rwhbk += ', '.join(jtru__mpcxr)
    return _create_function_from_code_obj(sdgu__yca, cxk__uxft, ovb__rwhbk,
        drbtj__gaoe, xif__yuec)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for znsx__jxf, (lghr__aepb, fng__hyv) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % fng__hyv)
            bmq__osm = _pass_registry.get(lghr__aepb).pass_inst
            if isinstance(bmq__osm, CompilerPass):
                self._runPass(znsx__jxf, bmq__osm, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, fng__hyv)
                shjdw__eck = self._patch_error(msg, e)
                raise shjdw__eck
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    sxrn__vmoru = None
    goou__dwd = {}

    def lookup(var, already_seen, varonly=True):
        val = goou__dwd.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    vqy__qnnb = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        kapl__mth = stmt.target
        ryul__and = stmt.value
        goou__dwd[kapl__mth.name] = ryul__and
        if isinstance(ryul__and, ir.Var) and ryul__and.name in goou__dwd:
            ryul__and = lookup(ryul__and, set())
        if isinstance(ryul__and, ir.Expr):
            wedim__hpub = set(lookup(glyq__hikd, set(), True).name for
                glyq__hikd in ryul__and.list_vars())
            if name in wedim__hpub:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ryul__and)]
                ibt__egp = [x for x, myrh__fvbss in args if myrh__fvbss.
                    name != name]
                args = [(x, myrh__fvbss) for x, myrh__fvbss in args if x !=
                    myrh__fvbss.name]
                hkl__fca = dict(args)
                if len(ibt__egp) == 1:
                    hkl__fca[ibt__egp[0]] = ir.Var(kapl__mth.scope, name +
                        '#init', kapl__mth.loc)
                replace_vars_inner(ryul__and, hkl__fca)
                sxrn__vmoru = nodes[i:]
                break
    return sxrn__vmoru


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        bzd__grnq = expand_aliases({glyq__hikd.name for glyq__hikd in stmt.
            list_vars()}, alias_map, arg_aliases)
        jkswg__qia = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        rcn__lni = expand_aliases({glyq__hikd.name for glyq__hikd in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        wdwtx__oxhz = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(jkswg__qia & rcn__lni | wdwtx__oxhz & bzd__grnq) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    acu__hutl = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            acu__hutl.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                acu__hutl.update(get_parfor_writes(stmt, func_ir))
    return acu__hutl


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    acu__hutl = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        acu__hutl.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        acu__hutl = {glyq__hikd.name for glyq__hikd in stmt.df_out_vars.
            values()}
        if stmt.out_key_vars is not None:
            acu__hutl.update({glyq__hikd.name for glyq__hikd in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        acu__hutl = {glyq__hikd.name for glyq__hikd in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        acu__hutl = {glyq__hikd.name for glyq__hikd in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            acu__hutl.update({glyq__hikd.name for glyq__hikd in stmt.
                out_key_arrs})
            acu__hutl.update({glyq__hikd.name for glyq__hikd in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        njh__zorjw = guard(find_callname, func_ir, stmt.value)
        if njh__zorjw in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            acu__hutl.add(stmt.value.args[0].name)
        if njh__zorjw == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            acu__hutl.add(stmt.value.args[1].name)
    return acu__hutl


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        eqf__bwnia = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        ann__hnqtn = eqf__bwnia.format(self, msg)
        self.args = ann__hnqtn,
    else:
        eqf__bwnia = _termcolor.errmsg('{0}')
        ann__hnqtn = eqf__bwnia.format(self)
        self.args = ann__hnqtn,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for jlo__uqv in options['distributed']:
            dist_spec[jlo__uqv] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for jlo__uqv in options['distributed_block']:
            dist_spec[jlo__uqv] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    lro__icl = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, qvywk__aefk in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(qvywk__aefk)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    dhjmq__xsk = {}
    for vvocl__ucfl in reversed(inspect.getmro(cls)):
        dhjmq__xsk.update(vvocl__ucfl.__dict__)
    midh__onmev, zbu__faoeq, adc__pczhj, xxs__ine = {}, {}, {}, {}
    for flmm__odmnq, glyq__hikd in dhjmq__xsk.items():
        if isinstance(glyq__hikd, pytypes.FunctionType):
            midh__onmev[flmm__odmnq] = glyq__hikd
        elif isinstance(glyq__hikd, property):
            zbu__faoeq[flmm__odmnq] = glyq__hikd
        elif isinstance(glyq__hikd, staticmethod):
            adc__pczhj[flmm__odmnq] = glyq__hikd
        else:
            xxs__ine[flmm__odmnq] = glyq__hikd
    wbfv__jykpu = (set(midh__onmev) | set(zbu__faoeq) | set(adc__pczhj)) & set(
        spec)
    if wbfv__jykpu:
        raise NameError('name shadowing: {0}'.format(', '.join(wbfv__jykpu)))
    xknb__dfgms = xxs__ine.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(xxs__ine)
    if xxs__ine:
        msg = 'class members are not yet supported: {0}'
        mxy__bfpim = ', '.join(xxs__ine.keys())
        raise TypeError(msg.format(mxy__bfpim))
    for flmm__odmnq, glyq__hikd in zbu__faoeq.items():
        if glyq__hikd.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(flmm__odmnq)
                )
    jit_methods = {flmm__odmnq: bodo.jit(returns_maybe_distributed=lro__icl
        )(glyq__hikd) for flmm__odmnq, glyq__hikd in midh__onmev.items()}
    jit_props = {}
    for flmm__odmnq, glyq__hikd in zbu__faoeq.items():
        ldir__gzkkn = {}
        if glyq__hikd.fget:
            ldir__gzkkn['get'] = bodo.jit(glyq__hikd.fget)
        if glyq__hikd.fset:
            ldir__gzkkn['set'] = bodo.jit(glyq__hikd.fset)
        jit_props[flmm__odmnq] = ldir__gzkkn
    jit_static_methods = {flmm__odmnq: bodo.jit(glyq__hikd.__func__) for 
        flmm__odmnq, glyq__hikd in adc__pczhj.items()}
    fwg__ulnf = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    tqz__oykv = dict(class_type=fwg__ulnf, __doc__=xknb__dfgms)
    tqz__oykv.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), tqz__oykv)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, fwg__ulnf)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(fwg__ulnf, typingctx, targetctx).register()
    as_numba_type.register(cls, fwg__ulnf.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    hiwr__ofw = ','.join('{0}:{1}'.format(flmm__odmnq, glyq__hikd) for 
        flmm__odmnq, glyq__hikd in struct.items())
    xkypr__tuj = ','.join('{0}:{1}'.format(flmm__odmnq, glyq__hikd) for 
        flmm__odmnq, glyq__hikd in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), hiwr__ofw, xkypr__tuj)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    tpw__hhve = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if tpw__hhve is None:
        return
    mecy__lnw, nco__pcot = tpw__hhve
    for a in itertools.chain(mecy__lnw, nco__pcot.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, mecy__lnw, nco__pcot)
    except ForceLiteralArg as e:
        mjl__zegxb = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(mjl__zegxb, self.kws)
        zmew__eotjc = set()
        cosuo__ibs = set()
        hwk__ynh = {}
        for znsx__jxf in e.requested_args:
            qiu__ixzdw = typeinfer.func_ir.get_definition(folded[znsx__jxf])
            if isinstance(qiu__ixzdw, ir.Arg):
                zmew__eotjc.add(qiu__ixzdw.index)
                if qiu__ixzdw.index in e.file_infos:
                    hwk__ynh[qiu__ixzdw.index] = e.file_infos[qiu__ixzdw.index]
            else:
                cosuo__ibs.add(znsx__jxf)
        if cosuo__ibs:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif zmew__eotjc:
            raise ForceLiteralArg(zmew__eotjc, loc=self.loc, file_infos=
                hwk__ynh)
    if sig is None:
        pnce__syott = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in mecy__lnw]
        args += [('%s=%s' % (flmm__odmnq, glyq__hikd)) for flmm__odmnq,
            glyq__hikd in sorted(nco__pcot.items())]
        oud__qeg = pnce__syott.format(fnty, ', '.join(map(str, args)))
        nnl__nvob = context.explain_function_type(fnty)
        msg = '\n'.join([oud__qeg, nnl__nvob])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        rbiqe__eetgf = context.unify_pairs(sig.recvr, fnty.this)
        if rbiqe__eetgf is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if rbiqe__eetgf is not None and rbiqe__eetgf.is_precise():
            ini__pwes = fnty.copy(this=rbiqe__eetgf)
            typeinfer.propagate_refined_type(self.func, ini__pwes)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            mjbqo__uqemy = target.getone()
            if context.unify_pairs(mjbqo__uqemy, sig.return_type
                ) == mjbqo__uqemy:
                sig = sig.replace(return_type=mjbqo__uqemy)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        lvpjw__glki = '*other* must be a {} but got a {} instead'
        raise TypeError(lvpjw__glki.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    oubw__nrq = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for flmm__odmnq, glyq__hikd in kwargs.items():
        olwgq__ypwrt = None
        try:
            jjd__xgpoi = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var
                ('dummy'), loc)
            func_ir._definitions[jjd__xgpoi.name] = [glyq__hikd]
            olwgq__ypwrt = get_const_value_inner(func_ir, jjd__xgpoi)
            func_ir._definitions.pop(jjd__xgpoi.name)
            if isinstance(olwgq__ypwrt, str):
                olwgq__ypwrt = sigutils._parse_signature_string(olwgq__ypwrt)
            if isinstance(olwgq__ypwrt, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {flmm__odmnq} is annotated as type class {olwgq__ypwrt}."""
                    )
            assert isinstance(olwgq__ypwrt, types.Type)
            if isinstance(olwgq__ypwrt, (types.List, types.Set)):
                olwgq__ypwrt = olwgq__ypwrt.copy(reflected=False)
            oubw__nrq[flmm__odmnq] = olwgq__ypwrt
        except BodoError as ctcwe__bpswq:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(olwgq__ypwrt, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(glyq__hikd, ir.Global):
                    msg = f'Global {glyq__hikd.name!r} is not defined.'
                if isinstance(glyq__hikd, ir.FreeVar):
                    msg = f'Freevar {glyq__hikd.name!r} is not defined.'
            if isinstance(glyq__hikd, ir.Expr) and glyq__hikd.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=flmm__odmnq, msg=msg, loc=loc)
    for name, typ in oubw__nrq.items():
        self._legalize_arg_type(name, typ, loc)
    return oubw__nrq


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    beoge__xme = inst.arg
    assert beoge__xme > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(beoge__xme)]))
    tmps = [state.make_temp() for _ in range(beoge__xme - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    skjbz__pare = ir.Global('format', format, loc=self.loc)
    self.store(value=skjbz__pare, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    aie__alj = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=aie__alj, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    beoge__xme = inst.arg
    assert beoge__xme > 0, 'invalid BUILD_STRING count'
    jvtc__khkk = self.get(strings[0])
    for other, stmmx__jxxu in zip(strings[1:], tmps):
        other = self.get(other)
        uzni__iupby = ir.Expr.binop(operator.add, lhs=jvtc__khkk, rhs=other,
            loc=self.loc)
        self.store(uzni__iupby, stmmx__jxxu)
        jvtc__khkk = self.get(stmmx__jxxu)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    qqjls__krmpn = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, qqjls__krmpn])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    cskan__ikcsz = mk_unique_var(f'{var_name}')
    byk__gvkf = cskan__ikcsz.replace('<', '_').replace('>', '_')
    byk__gvkf = byk__gvkf.replace('.', '_').replace('$', '_v')
    return byk__gvkf


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if val1 == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                wxsbj__irhup = get_overload_const_str(val2)
                if wxsbj__irhup != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        bmd__pyx = states['defmap']
        if len(bmd__pyx) == 0:
            efisg__qcrp = assign.target
            numba.core.ssa._logger.debug('first assign: %s', efisg__qcrp)
            if efisg__qcrp.name not in scope.localvars:
                efisg__qcrp = scope.define(assign.target.name, loc=assign.loc)
        else:
            efisg__qcrp = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=efisg__qcrp, value=assign.value, loc=
            assign.loc)
        bmd__pyx[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    edx__gylwu = []
    for flmm__odmnq, glyq__hikd in typing.npydecl.registry.globals:
        if flmm__odmnq == func:
            edx__gylwu.append(glyq__hikd)
    for flmm__odmnq, glyq__hikd in typing.templates.builtin_registry.globals:
        if flmm__odmnq == func:
            edx__gylwu.append(glyq__hikd)
    if len(edx__gylwu) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return edx__gylwu


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    rfuwp__vegew = {}
    ojt__whne = find_topo_order(blocks)
    nkmx__eablk = {}
    for wkskp__zftj in ojt__whne:
        block = blocks[wkskp__zftj]
        jtcr__xyyy = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                kapl__mth = stmt.target.name
                ryul__and = stmt.value
                if (ryul__and.op == 'getattr' and ryul__and.attr in
                    arr_math and isinstance(typemap[ryul__and.value.name],
                    types.npytypes.Array)):
                    ryul__and = stmt.value
                    zyp__vdvz = ryul__and.value
                    rfuwp__vegew[kapl__mth] = zyp__vdvz
                    scope = zyp__vdvz.scope
                    loc = zyp__vdvz.loc
                    neznx__molk = ir.Var(scope, mk_unique_var('$np_g_var'), loc
                        )
                    typemap[neznx__molk.name] = types.misc.Module(numpy)
                    uata__xjtq = ir.Global('np', numpy, loc)
                    hsdax__iylxn = ir.Assign(uata__xjtq, neznx__molk, loc)
                    ryul__and.value = neznx__molk
                    jtcr__xyyy.append(hsdax__iylxn)
                    func_ir._definitions[neznx__molk.name] = [uata__xjtq]
                    func = getattr(numpy, ryul__and.attr)
                    igmoy__wuba = get_np_ufunc_typ_lst(func)
                    nkmx__eablk[kapl__mth] = igmoy__wuba
                if (ryul__and.op == 'call' and ryul__and.func.name in
                    rfuwp__vegew):
                    zyp__vdvz = rfuwp__vegew[ryul__and.func.name]
                    wmjd__qla = calltypes.pop(ryul__and)
                    gpn__pkz = wmjd__qla.args[:len(ryul__and.args)]
                    ujodt__gdni = {name: typemap[glyq__hikd.name] for name,
                        glyq__hikd in ryul__and.kws}
                    hmofq__yie = nkmx__eablk[ryul__and.func.name]
                    bun__nwb = None
                    for mgks__gjrzz in hmofq__yie:
                        try:
                            bun__nwb = mgks__gjrzz.get_call_type(typingctx,
                                [typemap[zyp__vdvz.name]] + list(gpn__pkz),
                                ujodt__gdni)
                            typemap.pop(ryul__and.func.name)
                            typemap[ryul__and.func.name] = mgks__gjrzz
                            calltypes[ryul__and] = bun__nwb
                            break
                        except Exception as ctcwe__bpswq:
                            pass
                    if bun__nwb is None:
                        raise TypeError(
                            f'No valid template found for {ryul__and.func.name}'
                            )
                    ryul__and.args = [zyp__vdvz] + ryul__and.args
            jtcr__xyyy.append(stmt)
        block.body = jtcr__xyyy


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    offsa__bchps = ufunc.nin
    ixkcw__ntwbi = ufunc.nout
    oxk__pabqy = ufunc.nargs
    assert oxk__pabqy == offsa__bchps + ixkcw__ntwbi
    if len(args) < offsa__bchps:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            offsa__bchps))
    if len(args) > oxk__pabqy:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), oxk__pabqy)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    kumoo__gwtuo = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    ffkx__typcz = max(kumoo__gwtuo)
    vgy__uodp = args[offsa__bchps:]
    if not all(d == ffkx__typcz for d in kumoo__gwtuo[offsa__bchps:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(ymjvf__licih, types.ArrayCompatible) and not
        isinstance(ymjvf__licih, types.Bytes) for ymjvf__licih in vgy__uodp):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(ymjvf__licih.mutable for ymjvf__licih in vgy__uodp):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    ayd__ifthr = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    rkqqy__mhp = None
    if ffkx__typcz > 0 and len(vgy__uodp) < ufunc.nout:
        rkqqy__mhp = 'C'
        oafy__dorpm = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in oafy__dorpm and 'F' in oafy__dorpm:
            rkqqy__mhp = 'F'
    return ayd__ifthr, vgy__uodp, ffkx__typcz, rkqqy__mhp


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        okhp__gurw = 'Dict.key_type cannot be of type {}'
        raise TypingError(okhp__gurw.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        okhp__gurw = 'Dict.value_type cannot be of type {}'
        raise TypingError(okhp__gurw.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    mgeou__nqxfy = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[mgeou__nqxfy]
        return impl, args
    except KeyError as ctcwe__bpswq:
        pass
    impl, args = self._build_impl(mgeou__nqxfy, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        qxsc__czdg = find_topo_order(parfor.loop_body)
    sbfer__dkn = qxsc__czdg[0]
    tned__zfirn = {}
    _update_parfor_get_setitems(parfor.loop_body[sbfer__dkn].body, parfor.
        index_var, alias_map, tned__zfirn, lives_n_aliases)
    beml__ojnr = set(tned__zfirn.keys())
    for ibvfa__akl in qxsc__czdg:
        if ibvfa__akl == sbfer__dkn:
            continue
        for stmt in parfor.loop_body[ibvfa__akl].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            ophdr__lfy = set(glyq__hikd.name for glyq__hikd in stmt.list_vars()
                )
            hpk__noig = ophdr__lfy & beml__ojnr
            for a in hpk__noig:
                tned__zfirn.pop(a, None)
    for ibvfa__akl in qxsc__czdg:
        if ibvfa__akl == sbfer__dkn:
            continue
        block = parfor.loop_body[ibvfa__akl]
        vtq__onp = tned__zfirn.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            vtq__onp, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    saks__eefx = max(blocks.keys())
    ego__feej, okmxi__yketl = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    jux__zwoh = ir.Jump(ego__feej, ir.Loc('parfors_dummy', -1))
    blocks[saks__eefx].body.append(jux__zwoh)
    cxdr__doh = compute_cfg_from_blocks(blocks)
    eqx__nbu = compute_use_defs(blocks)
    mvmr__vnht = compute_live_map(cxdr__doh, blocks, eqx__nbu.usemap,
        eqx__nbu.defmap)
    alias_set = set(alias_map.keys())
    for wkskp__zftj, block in blocks.items():
        jtcr__xyyy = []
        wbwfj__icwi = {glyq__hikd.name for glyq__hikd in block.terminator.
            list_vars()}
        for mvqr__pfs, ypur__blm in cxdr__doh.successors(wkskp__zftj):
            wbwfj__icwi |= mvmr__vnht[mvqr__pfs]
        for stmt in reversed(block.body):
            brbq__cea = wbwfj__icwi & alias_set
            for glyq__hikd in brbq__cea:
                wbwfj__icwi |= alias_map[glyq__hikd]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in wbwfj__icwi and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                njh__zorjw = guard(find_callname, func_ir, stmt.value)
                if njh__zorjw == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in wbwfj__icwi and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            wbwfj__icwi |= {glyq__hikd.name for glyq__hikd in stmt.list_vars()}
            jtcr__xyyy.append(stmt)
        jtcr__xyyy.reverse()
        block.body = jtcr__xyyy
    typemap.pop(okmxi__yketl.name)
    blocks[saks__eefx].body.pop()

    def trim_empty_parfor_branches(parfor):
        lbmo__ghgys = False
        blocks = parfor.loop_body.copy()
        for wkskp__zftj, block in blocks.items():
            if len(block.body):
                kcpf__zidgy = block.body[-1]
                if isinstance(kcpf__zidgy, ir.Branch):
                    if len(blocks[kcpf__zidgy.truebr].body) == 1 and len(blocks
                        [kcpf__zidgy.falsebr].body) == 1:
                        kaa__yoac = blocks[kcpf__zidgy.truebr].body[0]
                        xbd__kuqxz = blocks[kcpf__zidgy.falsebr].body[0]
                        if isinstance(kaa__yoac, ir.Jump) and isinstance(
                            xbd__kuqxz, ir.Jump
                            ) and kaa__yoac.target == xbd__kuqxz.target:
                            parfor.loop_body[wkskp__zftj].body[-1] = ir.Jump(
                                kaa__yoac.target, kcpf__zidgy.loc)
                            lbmo__ghgys = True
                    elif len(blocks[kcpf__zidgy.truebr].body) == 1:
                        kaa__yoac = blocks[kcpf__zidgy.truebr].body[0]
                        if isinstance(kaa__yoac, ir.Jump
                            ) and kaa__yoac.target == kcpf__zidgy.falsebr:
                            parfor.loop_body[wkskp__zftj].body[-1] = ir.Jump(
                                kaa__yoac.target, kcpf__zidgy.loc)
                            lbmo__ghgys = True
                    elif len(blocks[kcpf__zidgy.falsebr].body) == 1:
                        xbd__kuqxz = blocks[kcpf__zidgy.falsebr].body[0]
                        if isinstance(xbd__kuqxz, ir.Jump
                            ) and xbd__kuqxz.target == kcpf__zidgy.truebr:
                            parfor.loop_body[wkskp__zftj].body[-1] = ir.Jump(
                                xbd__kuqxz.target, kcpf__zidgy.loc)
                            lbmo__ghgys = True
        return lbmo__ghgys
    lbmo__ghgys = True
    while lbmo__ghgys:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        lbmo__ghgys = trim_empty_parfor_branches(parfor)
    xonk__ipom = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        xonk__ipom &= len(block.body) == 0
    if xonk__ipom:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import simplify_CFG
    from numba.parfors.parfor import Parfor
    xkor__bga = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                xkor__bga += 1
                parfor = stmt
                lcqdw__cwvan = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = lcqdw__cwvan.scope
                loc = ir.Loc('parfors_dummy', -1)
                axm__tqi = ir.Var(scope, mk_unique_var('$const'), loc)
                lcqdw__cwvan.body.append(ir.Assign(ir.Const(0, loc),
                    axm__tqi, loc))
                lcqdw__cwvan.body.append(ir.Return(axm__tqi, loc))
                cxdr__doh = compute_cfg_from_blocks(parfor.loop_body)
                for izsz__yurfs in cxdr__doh.dead_nodes():
                    del parfor.loop_body[izsz__yurfs]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                lcqdw__cwvan = parfor.loop_body[max(parfor.loop_body.keys())]
                lcqdw__cwvan.body.pop()
                lcqdw__cwvan.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return xkor__bga


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            eyec__ccpb = self.overloads.get(tuple(args))
            if eyec__ccpb is not None:
                return eyec__ccpb.entry_point
            self._pre_compile(args, return_type, flags)
            ive__uirgl = self.func_ir
            gfqa__rot = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=gfqa__rot):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=ive__uirgl, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        cgqp__cjl = copy.deepcopy(flags)
        cgqp__cjl.no_rewrites = True

        def compile_local(the_ir, the_flags):
            fpk__wyce = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return fpk__wyce.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        rpq__zjc = compile_local(func_ir, cgqp__cjl)
        gjed__kuwb = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    gjed__kuwb = compile_local(func_ir, flags)
                except Exception as ctcwe__bpswq:
                    pass
        if gjed__kuwb is not None:
            cres = gjed__kuwb
        else:
            cres = rpq__zjc
        return cres
    else:
        fpk__wyce = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return fpk__wyce.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    hjvs__gaf = self.get_data_type(typ.dtype)
    hcqt__qtakx = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        hcqt__qtakx):
        sxy__jzha = ary.ctypes.data
        xgt__ypfdw = self.add_dynamic_addr(builder, sxy__jzha, info=str(
            type(sxy__jzha)))
        vwvw__cva = self.add_dynamic_addr(builder, id(ary), info=str(type(ary))
            )
        self.global_arrays.append(ary)
    else:
        smy__win = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            smy__win = smy__win.view('int64')
        val = bytearray(smy__win.data)
        xtd__uxmto = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        xgt__ypfdw = cgutils.global_constant(builder, '.const.array.data',
            xtd__uxmto)
        xgt__ypfdw.align = self.get_abi_alignment(hjvs__gaf)
        vwvw__cva = None
    zht__dxz = self.get_value_type(types.intp)
    cdry__wokf = [self.get_constant(types.intp, zfluj__rqbpo) for
        zfluj__rqbpo in ary.shape]
    vuuvb__ghbmc = lir.Constant(lir.ArrayType(zht__dxz, len(cdry__wokf)),
        cdry__wokf)
    naedk__bbsrx = [self.get_constant(types.intp, zfluj__rqbpo) for
        zfluj__rqbpo in ary.strides]
    jksbn__ugyqu = lir.Constant(lir.ArrayType(zht__dxz, len(naedk__bbsrx)),
        naedk__bbsrx)
    vcj__qubzj = self.get_constant(types.intp, ary.dtype.itemsize)
    oywk__xvvm = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        oywk__xvvm, vcj__qubzj, xgt__ypfdw.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), vuuvb__ghbmc, jksbn__ugyqu])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    xzyo__fxzfb = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    oijg__mszo = lir.Function(module, xzyo__fxzfb, name='nrt_atomic_{0}'.
        format(op))
    [lcnyv__hph] = oijg__mszo.args
    zfjcc__krfgr = oijg__mszo.append_basic_block()
    builder = lir.IRBuilder(zfjcc__krfgr)
    ofjr__sdnx = lir.Constant(_word_type, 1)
    if False:
        dqrxx__zykaq = builder.atomic_rmw(op, lcnyv__hph, ofjr__sdnx,
            ordering=ordering)
        res = getattr(builder, op)(dqrxx__zykaq, ofjr__sdnx)
        builder.ret(res)
    else:
        dqrxx__zykaq = builder.load(lcnyv__hph)
        woqvf__sje = getattr(builder, op)(dqrxx__zykaq, ofjr__sdnx)
        jrktc__zheb = builder.icmp_signed('!=', dqrxx__zykaq, lir.Constant(
            dqrxx__zykaq.type, -1))
        with cgutils.if_likely(builder, jrktc__zheb):
            builder.store(woqvf__sje, lcnyv__hph)
        builder.ret(woqvf__sje)
    return oijg__mszo


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        fmvh__zphgo = state.targetctx.codegen()
        state.library = fmvh__zphgo.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    acon__ljyhd = state.func_ir
    typemap = state.typemap
    xzaky__iezi = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    nzrm__gung = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            acon__ljyhd, typemap, xzaky__iezi, calltypes, mangler=targetctx
            .mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            stvwz__bou = lowering.Lower(targetctx, library, fndesc,
                acon__ljyhd, metadata=metadata)
            stvwz__bou.lower()
            if not flags.no_cpython_wrapper:
                stvwz__bou.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(xzaky__iezi, (types.Optional, types.
                        Generator)):
                        pass
                    else:
                        stvwz__bou.create_cfunc_wrapper()
            env = stvwz__bou.env
            zmpt__ghsvx = stvwz__bou.call_helper
            del stvwz__bou
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, zmpt__ghsvx, cfunc=None, env=env
                )
        else:
            hww__ycw = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(hww__ycw, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, zmpt__ghsvx, cfunc=hww__ycw,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        gbbs__hfuzr = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = gbbs__hfuzr - nzrm__gung
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        jroxp__xvnqd = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, jroxp__xvnqd),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            tlf__cumwf.do_break()
        fmxq__eqg = c.builder.icmp_signed('!=', jroxp__xvnqd, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(fmxq__eqg, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, jroxp__xvnqd)
                c.pyapi.decref(jroxp__xvnqd)
                tlf__cumwf.do_break()
        c.pyapi.decref(jroxp__xvnqd)
    fty__eosh, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(fty__eosh, likely=True) as (rjw__xrv, vhh__narrn):
        with rjw__xrv:
            list.size = size
            rbu__nga = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                rbu__nga), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        rbu__nga))
                    with cgutils.for_range(c.builder, size) as tlf__cumwf:
                        itemobj = c.pyapi.list_getitem(obj, tlf__cumwf.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        mletq__sem = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(mletq__sem.is_error, likely=
                            False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            tlf__cumwf.do_break()
                        list.setitem(tlf__cumwf.index, mletq__sem.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with vhh__narrn:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    tnf__njqcl, qfr__pntuc, znm__mrjk, dvys__xtvm, nggs__maikk = (
        compile_time_get_string_data(literal_string))
    dje__dsfa = builder.module
    gv = context.insert_const_bytes(dje__dsfa, tnf__njqcl)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        qfr__pntuc), context.get_constant(types.int32, znm__mrjk), context.
        get_constant(types.uint32, dvys__xtvm), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    yvitt__jijv = None
    if isinstance(shape, types.Integer):
        yvitt__jijv = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(zfluj__rqbpo, (types.Integer, types.IntEnumMember
            )) for zfluj__rqbpo in shape):
            yvitt__jijv = len(shape)
    return yvitt__jijv


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            yvitt__jijv = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if yvitt__jijv == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    yvitt__jijv))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            wslw__chlq = self._get_names(x)
            if len(wslw__chlq) != 0:
                return wslw__chlq[0]
            return wslw__chlq
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    wslw__chlq = self._get_names(obj)
    if len(wslw__chlq) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(wslw__chlq[0])


def get_equiv_set(self, obj):
    wslw__chlq = self._get_names(obj)
    if len(wslw__chlq) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(wslw__chlq[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    ltdre__ekknc = []
    for qvb__xpp in func_ir.arg_names:
        if qvb__xpp in typemap and isinstance(typemap[qvb__xpp], types.
            containers.UniTuple) and typemap[qvb__xpp].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(qvb__xpp))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for wjrd__ifx in func_ir.blocks.values():
        for stmt in wjrd__ifx.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    qps__fcmat = getattr(val, 'code', None)
                    if qps__fcmat is not None:
                        if getattr(val, 'closure', None) is not None:
                            xuhsw__fvch = (
                                '<creating a function from a closure>')
                            uzni__iupby = ''
                        else:
                            xuhsw__fvch = qps__fcmat.co_name
                            uzni__iupby = '(%s) ' % xuhsw__fvch
                    else:
                        xuhsw__fvch = '<could not ascertain use case>'
                        uzni__iupby = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (xuhsw__fvch, uzni__iupby))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                ptxf__kwfx = False
                if isinstance(val, pytypes.FunctionType):
                    ptxf__kwfx = val in {numba.gdb, numba.gdb_init}
                if not ptxf__kwfx:
                    ptxf__kwfx = getattr(val, '_name', '') == 'gdb_internal'
                if ptxf__kwfx:
                    ltdre__ekknc.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    qsjyz__pjt = func_ir.get_definition(var)
                    bzfi__aemu = guard(find_callname, func_ir, qsjyz__pjt)
                    if bzfi__aemu and bzfi__aemu[1] == 'numpy':
                        ty = getattr(numpy, bzfi__aemu[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    maf__drx = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(maf__drx), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(ltdre__ekknc) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        cdnf__cijkl = '\n'.join([x.strformat() for x in ltdre__ekknc])
        raise errors.UnsupportedError(msg % cdnf__cijkl)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    flmm__odmnq, glyq__hikd = next(iter(val.items()))
    kfww__oswje = typeof_impl(flmm__odmnq, c)
    yicw__vkd = typeof_impl(glyq__hikd, c)
    if kfww__oswje is None or yicw__vkd is None:
        raise ValueError(
            f'Cannot type dict element type {type(flmm__odmnq)}, {type(glyq__hikd)}'
            )
    return types.DictType(kfww__oswje, yicw__vkd)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    kqbv__tmy = cgutils.alloca_once_value(c.builder, val)
    aah__hixj = c.pyapi.object_hasattr_string(val, '_opaque')
    ouf__uwau = c.builder.icmp_unsigned('==', aah__hixj, lir.Constant(
        aah__hixj.type, 0))
    xzvib__vgnfu = typ.key_type
    ctxuq__ecqa = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(xzvib__vgnfu, ctxuq__ecqa)

    def copy_dict(out_dict, in_dict):
        for flmm__odmnq, glyq__hikd in in_dict.items():
            out_dict[flmm__odmnq] = glyq__hikd
    with c.builder.if_then(ouf__uwau):
        cwpxx__qbw = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        cdd__mcsbq = c.pyapi.call_function_objargs(cwpxx__qbw, [])
        qob__yrkli = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(qob__yrkli, [cdd__mcsbq, val])
        c.builder.store(cdd__mcsbq, kqbv__tmy)
    val = c.builder.load(kqbv__tmy)
    tmn__gih = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    eda__rfdzq = c.pyapi.object_type(val)
    lva__idutm = c.builder.icmp_unsigned('==', eda__rfdzq, tmn__gih)
    with c.builder.if_else(lva__idutm) as (ocee__daibi, gkscy__aba):
        with ocee__daibi:
            xiwka__xcbtw = c.pyapi.object_getattr_string(val, '_opaque')
            ygzia__gnj = types.MemInfoPointer(types.voidptr)
            mletq__sem = c.unbox(ygzia__gnj, xiwka__xcbtw)
            mi = mletq__sem.value
            vqd__okgf = ygzia__gnj, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *vqd__okgf)
            fuju__ukuwv = context.get_constant_null(vqd__okgf[1])
            args = mi, fuju__ukuwv
            zmukj__tzr, aky__hnj = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, aky__hnj)
            c.pyapi.decref(xiwka__xcbtw)
            efip__bfb = c.builder.basic_block
        with gkscy__aba:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", eda__rfdzq, tmn__gih)
            unz__pvpet = c.builder.basic_block
    dtkbs__rhzpa = c.builder.phi(aky__hnj.type)
    xuns__zhm = c.builder.phi(zmukj__tzr.type)
    dtkbs__rhzpa.add_incoming(aky__hnj, efip__bfb)
    dtkbs__rhzpa.add_incoming(aky__hnj.type(None), unz__pvpet)
    xuns__zhm.add_incoming(zmukj__tzr, efip__bfb)
    xuns__zhm.add_incoming(cgutils.true_bit, unz__pvpet)
    c.pyapi.decref(tmn__gih)
    c.pyapi.decref(eda__rfdzq)
    with c.builder.if_then(ouf__uwau):
        c.pyapi.decref(val)
    return NativeValue(dtkbs__rhzpa, is_error=xuns__zhm)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    ugo__vjc = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=ugo__vjc, name=updatevar)
    otoj__nlhl = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=otoj__nlhl, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for flmm__odmnq, glyq__hikd in other.items():
            d[flmm__odmnq] = glyq__hikd
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    uzni__iupby = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(uzni__iupby, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    mbaip__cxf = PassManager(name)
    if state.func_ir is None:
        mbaip__cxf.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            mbaip__cxf.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        mbaip__cxf.add_pass(FixupArgs, 'fix up args')
    mbaip__cxf.add_pass(IRProcessing, 'processing IR')
    mbaip__cxf.add_pass(WithLifting, 'Handle with contexts')
    mbaip__cxf.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        mbaip__cxf.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        mbaip__cxf.add_pass(DeadBranchPrune, 'dead branch pruning')
        mbaip__cxf.add_pass(GenericRewrites, 'nopython rewrites')
    mbaip__cxf.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    mbaip__cxf.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        mbaip__cxf.add_pass(DeadBranchPrune, 'dead branch pruning')
    mbaip__cxf.add_pass(FindLiterallyCalls, 'find literally calls')
    mbaip__cxf.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        mbaip__cxf.add_pass(ReconstructSSA, 'ssa')
    mbaip__cxf.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    mbaip__cxf.finalize()
    return mbaip__cxf


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, fcc__motul = args
    if isinstance(a, types.List) and isinstance(fcc__motul, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(fcc__motul, types.List):
        return signature(fcc__motul, types.intp, fcc__motul)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        qrw__gctez, cmdo__czowy = 0, 1
    else:
        qrw__gctez, cmdo__czowy = 1, 0
    ama__ibg = ListInstance(context, builder, sig.args[qrw__gctez], args[
        qrw__gctez])
    sln__fdv = ama__ibg.size
    wekw__comfn = args[cmdo__czowy]
    rbu__nga = lir.Constant(wekw__comfn.type, 0)
    wekw__comfn = builder.select(cgutils.is_neg_int(builder, wekw__comfn),
        rbu__nga, wekw__comfn)
    oywk__xvvm = builder.mul(wekw__comfn, sln__fdv)
    blocb__rwww = ListInstance.allocate(context, builder, sig.return_type,
        oywk__xvvm)
    blocb__rwww.size = oywk__xvvm
    with cgutils.for_range_slice(builder, rbu__nga, oywk__xvvm, sln__fdv,
        inc=True) as (smeuc__qwptd, _):
        with cgutils.for_range(builder, sln__fdv) as tlf__cumwf:
            value = ama__ibg.getitem(tlf__cumwf.index)
            blocb__rwww.setitem(builder.add(tlf__cumwf.index, smeuc__qwptd),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, blocb__rwww.
        value)


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    eoug__kcp = first.unify(self, second)
    if eoug__kcp is not None:
        return eoug__kcp
    eoug__kcp = second.unify(self, first)
    if eoug__kcp is not None:
        return eoug__kcp
    ruie__gyfu = self.can_convert(fromty=first, toty=second)
    if ruie__gyfu is not None and ruie__gyfu <= Conversion.safe:
        return second
    ruie__gyfu = self.can_convert(fromty=second, toty=first)
    if ruie__gyfu is not None and ruie__gyfu <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    oywk__xvvm = payload.used
    listobj = c.pyapi.list_new(oywk__xvvm)
    fty__eosh = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(fty__eosh, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(oywk__xvvm
            .type, 0))
        with payload._iterate() as tlf__cumwf:
            i = c.builder.load(index)
            item = tlf__cumwf.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return fty__eosh, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    xqs__qijt = h.type
    fgmgy__rwcfx = self.mask
    dtype = self._ty.dtype
    etbuq__urfb = context.typing_context
    fnty = etbuq__urfb.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(etbuq__urfb, (dtype, dtype), {})
    irxe__uxhec = context.get_function(fnty, sig)
    uvuk__xmlq = ir.Constant(xqs__qijt, 1)
    fnbn__fza = ir.Constant(xqs__qijt, 5)
    gusr__fwt = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, fgmgy__rwcfx))
    if for_insert:
        msa__abdst = fgmgy__rwcfx.type(-1)
        hwi__vsrn = cgutils.alloca_once_value(builder, msa__abdst)
    nnu__mkee = builder.append_basic_block('lookup.body')
    sgpwd__hmc = builder.append_basic_block('lookup.found')
    xbr__lzrlq = builder.append_basic_block('lookup.not_found')
    jypll__uwe = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        nve__hcr = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, nve__hcr)):
            hie__ait = irxe__uxhec(builder, (item, entry.key))
            with builder.if_then(hie__ait):
                builder.branch(sgpwd__hmc)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, nve__hcr)):
            builder.branch(xbr__lzrlq)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, nve__hcr)):
                nwhiz__benme = builder.load(hwi__vsrn)
                nwhiz__benme = builder.select(builder.icmp_unsigned('==',
                    nwhiz__benme, msa__abdst), i, nwhiz__benme)
                builder.store(nwhiz__benme, hwi__vsrn)
    with cgutils.for_range(builder, ir.Constant(xqs__qijt, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, uvuk__xmlq)
        i = builder.and_(i, fgmgy__rwcfx)
        builder.store(i, index)
    builder.branch(nnu__mkee)
    with builder.goto_block(nnu__mkee):
        i = builder.load(index)
        check_entry(i)
        spy__xuoas = builder.load(gusr__fwt)
        spy__xuoas = builder.lshr(spy__xuoas, fnbn__fza)
        i = builder.add(uvuk__xmlq, builder.mul(i, fnbn__fza))
        i = builder.and_(fgmgy__rwcfx, builder.add(i, spy__xuoas))
        builder.store(i, index)
        builder.store(spy__xuoas, gusr__fwt)
        builder.branch(nnu__mkee)
    with builder.goto_block(xbr__lzrlq):
        if for_insert:
            i = builder.load(index)
            nwhiz__benme = builder.load(hwi__vsrn)
            i = builder.select(builder.icmp_unsigned('==', nwhiz__benme,
                msa__abdst), i, nwhiz__benme)
            builder.store(i, index)
        builder.branch(jypll__uwe)
    with builder.goto_block(sgpwd__hmc):
        builder.branch(jypll__uwe)
    builder.position_at_end(jypll__uwe)
    ptxf__kwfx = builder.phi(ir.IntType(1), 'found')
    ptxf__kwfx.add_incoming(cgutils.true_bit, sgpwd__hmc)
    ptxf__kwfx.add_incoming(cgutils.false_bit, xbr__lzrlq)
    return ptxf__kwfx, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    vlqd__sebhy = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    gky__ifatd = payload.used
    uvuk__xmlq = ir.Constant(gky__ifatd.type, 1)
    gky__ifatd = payload.used = builder.add(gky__ifatd, uvuk__xmlq)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, vlqd__sebhy), likely=True):
        payload.fill = builder.add(payload.fill, uvuk__xmlq)
    if do_resize:
        self.upsize(gky__ifatd)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    ptxf__kwfx, i = payload._lookup(item, h, for_insert=True)
    uno__diqv = builder.not_(ptxf__kwfx)
    with builder.if_then(uno__diqv):
        entry = payload.get_entry(i)
        vlqd__sebhy = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        gky__ifatd = payload.used
        uvuk__xmlq = ir.Constant(gky__ifatd.type, 1)
        gky__ifatd = payload.used = builder.add(gky__ifatd, uvuk__xmlq)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, vlqd__sebhy), likely=True):
            payload.fill = builder.add(payload.fill, uvuk__xmlq)
        if do_resize:
            self.upsize(gky__ifatd)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    gky__ifatd = payload.used
    uvuk__xmlq = ir.Constant(gky__ifatd.type, 1)
    gky__ifatd = payload.used = self._builder.sub(gky__ifatd, uvuk__xmlq)
    if do_resize:
        self.downsize(gky__ifatd)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    kzs__mmx = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, kzs__mmx)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    iki__ozc = payload
    fty__eosh = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(fty__eosh), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with iki__ozc._iterate() as tlf__cumwf:
        entry = tlf__cumwf.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(iki__ozc.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as tlf__cumwf:
        entry = tlf__cumwf.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    fty__eosh = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(fty__eosh), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    fty__eosh = cgutils.alloca_once_value(builder, cgutils.true_bit)
    xqs__qijt = context.get_value_type(types.intp)
    rbu__nga = ir.Constant(xqs__qijt, 0)
    uvuk__xmlq = ir.Constant(xqs__qijt, 1)
    fnvxd__pjtij = context.get_data_type(types.SetPayload(self._ty))
    erc__tsf = context.get_abi_sizeof(fnvxd__pjtij)
    mfyq__qomhj = self._entrysize
    erc__tsf -= mfyq__qomhj
    ooif__mlrly, tezap__iynjv = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(xqs__qijt, mfyq__qomhj), ir.Constant(
        xqs__qijt, erc__tsf))
    with builder.if_then(tezap__iynjv, likely=False):
        builder.store(cgutils.false_bit, fty__eosh)
    with builder.if_then(builder.load(fty__eosh), likely=True):
        if realloc:
            joev__tqa = self._set.meminfo
            lcnyv__hph = context.nrt.meminfo_varsize_alloc(builder,
                joev__tqa, size=ooif__mlrly)
            bxjyy__esvuk = cgutils.is_null(builder, lcnyv__hph)
        else:
            sdpke__ijykl = _imp_dtor(context, builder.module, self._ty)
            joev__tqa = context.nrt.meminfo_new_varsize_dtor(builder,
                ooif__mlrly, builder.bitcast(sdpke__ijykl, cgutils.voidptr_t))
            bxjyy__esvuk = cgutils.is_null(builder, joev__tqa)
        with builder.if_else(bxjyy__esvuk, likely=False) as (cxx__ttdcj,
            rjw__xrv):
            with cxx__ttdcj:
                builder.store(cgutils.false_bit, fty__eosh)
            with rjw__xrv:
                if not realloc:
                    self._set.meminfo = joev__tqa
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, ooif__mlrly, 255)
                payload.used = rbu__nga
                payload.fill = rbu__nga
                payload.finger = rbu__nga
                zrf__iqln = builder.sub(nentries, uvuk__xmlq)
                payload.mask = zrf__iqln
    return builder.load(fty__eosh)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    fty__eosh = cgutils.alloca_once_value(builder, cgutils.true_bit)
    xqs__qijt = context.get_value_type(types.intp)
    rbu__nga = ir.Constant(xqs__qijt, 0)
    uvuk__xmlq = ir.Constant(xqs__qijt, 1)
    fnvxd__pjtij = context.get_data_type(types.SetPayload(self._ty))
    erc__tsf = context.get_abi_sizeof(fnvxd__pjtij)
    mfyq__qomhj = self._entrysize
    erc__tsf -= mfyq__qomhj
    fgmgy__rwcfx = src_payload.mask
    nentries = builder.add(uvuk__xmlq, fgmgy__rwcfx)
    ooif__mlrly = builder.add(ir.Constant(xqs__qijt, erc__tsf), builder.mul
        (ir.Constant(xqs__qijt, mfyq__qomhj), nentries))
    with builder.if_then(builder.load(fty__eosh), likely=True):
        sdpke__ijykl = _imp_dtor(context, builder.module, self._ty)
        joev__tqa = context.nrt.meminfo_new_varsize_dtor(builder,
            ooif__mlrly, builder.bitcast(sdpke__ijykl, cgutils.voidptr_t))
        bxjyy__esvuk = cgutils.is_null(builder, joev__tqa)
        with builder.if_else(bxjyy__esvuk, likely=False) as (cxx__ttdcj,
            rjw__xrv):
            with cxx__ttdcj:
                builder.store(cgutils.false_bit, fty__eosh)
            with rjw__xrv:
                self._set.meminfo = joev__tqa
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = rbu__nga
                payload.mask = fgmgy__rwcfx
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, mfyq__qomhj)
                with src_payload._iterate() as tlf__cumwf:
                    context.nrt.incref(builder, self._ty.dtype, tlf__cumwf.
                        entry.key)
    return builder.load(fty__eosh)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    vek__oqla = context.get_value_type(types.voidptr)
    jvjux__pecbt = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [vek__oqla, jvjux__pecbt, vek__oqla])
    fclot__kvgn = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=fclot__kvgn)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        jwb__yrpb = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, jwb__yrpb)
        with payload._iterate() as tlf__cumwf:
            entry = tlf__cumwf.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    nvfux__mvdx, = sig.args
    uurqt__weicy, = args
    dkf__fbvqv = numba.core.imputils.call_len(context, builder, nvfux__mvdx,
        uurqt__weicy)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, dkf__fbvqv)
    with numba.core.imputils.for_iter(context, builder, nvfux__mvdx,
        uurqt__weicy) as tlf__cumwf:
        inst.add(tlf__cumwf.value)
        context.nrt.decref(builder, set_type.dtype, tlf__cumwf.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    nvfux__mvdx = sig.args[1]
    uurqt__weicy = args[1]
    dkf__fbvqv = numba.core.imputils.call_len(context, builder, nvfux__mvdx,
        uurqt__weicy)
    if dkf__fbvqv is not None:
        pvjeu__kjfnw = builder.add(inst.payload.used, dkf__fbvqv)
        inst.upsize(pvjeu__kjfnw)
    with numba.core.imputils.for_iter(context, builder, nvfux__mvdx,
        uurqt__weicy) as tlf__cumwf:
        naiuf__ddyo = context.cast(builder, tlf__cumwf.value, nvfux__mvdx.
            dtype, inst.dtype)
        inst.add(naiuf__ddyo)
        context.nrt.decref(builder, nvfux__mvdx.dtype, tlf__cumwf.value)
    if dkf__fbvqv is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    gkbvu__cwro = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, gkbvu__cwro, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    hww__ycw = target_context.get_executable(library, fndesc, env)
    blifm__aiig = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=hww__ycw, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return blifm__aiig


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild


def _get_cache_path(self):
    return numba.config.CACHE_DIR


if _check_numba_change:
    if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
        numba.core.caching._IPythonCacheLocator.get_cache_path = (
            _get_cache_path)
