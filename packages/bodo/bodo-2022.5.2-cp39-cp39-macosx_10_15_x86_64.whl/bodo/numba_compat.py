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
    xgdg__odak = numba.core.bytecode.FunctionIdentity.from_function(func)
    qhknt__wtq = numba.core.interpreter.Interpreter(xgdg__odak)
    dfoqz__anru = numba.core.bytecode.ByteCode(func_id=xgdg__odak)
    func_ir = qhknt__wtq.interpret(dfoqz__anru)
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
        lic__pvbej = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        lic__pvbej.run()
    ysfm__ozlz = numba.core.postproc.PostProcessor(func_ir)
    ysfm__ozlz.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, sbib__yjt in visit_vars_extensions.items():
        if isinstance(stmt, t):
            sbib__yjt(stmt, callback, cbdata)
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
    xzexz__jkv = ['ravel', 'transpose', 'reshape']
    for veiej__yxyjf in blocks.values():
        for qzbu__lnzz in veiej__yxyjf.body:
            if type(qzbu__lnzz) in alias_analysis_extensions:
                sbib__yjt = alias_analysis_extensions[type(qzbu__lnzz)]
                sbib__yjt(qzbu__lnzz, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(qzbu__lnzz, ir.Assign):
                hzasu__cvzn = qzbu__lnzz.value
                zgvvf__aoyv = qzbu__lnzz.target.name
                if is_immutable_type(zgvvf__aoyv, typemap):
                    continue
                if isinstance(hzasu__cvzn, ir.Var
                    ) and zgvvf__aoyv != hzasu__cvzn.name:
                    _add_alias(zgvvf__aoyv, hzasu__cvzn.name, alias_map,
                        arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr) and (hzasu__cvzn.op ==
                    'cast' or hzasu__cvzn.op in ['getitem', 'static_getitem']):
                    _add_alias(zgvvf__aoyv, hzasu__cvzn.value.name,
                        alias_map, arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr
                    ) and hzasu__cvzn.op == 'inplace_binop':
                    _add_alias(zgvvf__aoyv, hzasu__cvzn.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr
                    ) and hzasu__cvzn.op == 'getattr' and hzasu__cvzn.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(zgvvf__aoyv, hzasu__cvzn.value.name,
                        alias_map, arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr
                    ) and hzasu__cvzn.op == 'getattr' and hzasu__cvzn.attr not in [
                    'shape'] and hzasu__cvzn.value.name in arg_aliases:
                    _add_alias(zgvvf__aoyv, hzasu__cvzn.value.name,
                        alias_map, arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr
                    ) and hzasu__cvzn.op == 'getattr' and hzasu__cvzn.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(zgvvf__aoyv, hzasu__cvzn.value.name,
                        alias_map, arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr) and hzasu__cvzn.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(zgvvf__aoyv, typemap):
                    for xreh__kuud in hzasu__cvzn.items:
                        _add_alias(zgvvf__aoyv, xreh__kuud.name, alias_map,
                            arg_aliases)
                if isinstance(hzasu__cvzn, ir.Expr
                    ) and hzasu__cvzn.op == 'call':
                    ylq__qijwe = guard(find_callname, func_ir, hzasu__cvzn,
                        typemap)
                    if ylq__qijwe is None:
                        continue
                    nwa__axhte, elvmk__elfn = ylq__qijwe
                    if ylq__qijwe in alias_func_extensions:
                        avdq__jeb = alias_func_extensions[ylq__qijwe]
                        avdq__jeb(zgvvf__aoyv, hzasu__cvzn.args, alias_map,
                            arg_aliases)
                    if elvmk__elfn == 'numpy' and nwa__axhte in xzexz__jkv:
                        _add_alias(zgvvf__aoyv, hzasu__cvzn.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(elvmk__elfn, ir.Var
                        ) and nwa__axhte in xzexz__jkv:
                        _add_alias(zgvvf__aoyv, elvmk__elfn.name, alias_map,
                            arg_aliases)
    vxq__hntwq = copy.deepcopy(alias_map)
    for xreh__kuud in vxq__hntwq:
        for mlu__zgncr in vxq__hntwq[xreh__kuud]:
            alias_map[xreh__kuud] |= alias_map[mlu__zgncr]
        for mlu__zgncr in vxq__hntwq[xreh__kuud]:
            alias_map[mlu__zgncr] = alias_map[xreh__kuud]
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
    vmtb__quljx = compute_cfg_from_blocks(func_ir.blocks)
    vwm__dxb = compute_use_defs(func_ir.blocks)
    ozsla__nnqq = compute_live_map(vmtb__quljx, func_ir.blocks, vwm__dxb.
        usemap, vwm__dxb.defmap)
    rjth__nwttk = True
    while rjth__nwttk:
        rjth__nwttk = False
        for kwutr__ropx, block in func_ir.blocks.items():
            lives = {xreh__kuud.name for xreh__kuud in block.terminator.
                list_vars()}
            for vpxz__qbtmm, viae__zxlk in vmtb__quljx.successors(kwutr__ropx):
                lives |= ozsla__nnqq[vpxz__qbtmm]
            iactv__nnw = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    zgvvf__aoyv = stmt.target
                    gzv__mfott = stmt.value
                    if zgvvf__aoyv.name not in lives:
                        if isinstance(gzv__mfott, ir.Expr
                            ) and gzv__mfott.op == 'make_function':
                            continue
                        if isinstance(gzv__mfott, ir.Expr
                            ) and gzv__mfott.op == 'getattr':
                            continue
                        if isinstance(gzv__mfott, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(zgvvf__aoyv,
                            None), types.Function):
                            continue
                        if isinstance(gzv__mfott, ir.Expr
                            ) and gzv__mfott.op == 'build_map':
                            continue
                        if isinstance(gzv__mfott, ir.Expr
                            ) and gzv__mfott.op == 'build_tuple':
                            continue
                    if isinstance(gzv__mfott, ir.Var
                        ) and zgvvf__aoyv.name == gzv__mfott.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    gsu__glqw = analysis.ir_extension_usedefs[type(stmt)]
                    ipj__kahkh, bggrz__xzqyt = gsu__glqw(stmt)
                    lives -= bggrz__xzqyt
                    lives |= ipj__kahkh
                else:
                    lives |= {xreh__kuud.name for xreh__kuud in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(zgvvf__aoyv.name)
                iactv__nnw.append(stmt)
            iactv__nnw.reverse()
            if len(block.body) != len(iactv__nnw):
                rjth__nwttk = True
            block.body = iactv__nnw


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    spdav__vmxx = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (spdav__vmxx,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    rwg__iijtp = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), rwg__iijtp)


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
            for eaac__zsbt in fnty.templates:
                self._inline_overloads.update(eaac__zsbt._inline_overloads)
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
    rwg__iijtp = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), rwg__iijtp)
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
    vbo__szdw, zpw__cyre = self._get_impl(args, kws)
    if vbo__szdw is None:
        return
    jsldu__kdb = types.Dispatcher(vbo__szdw)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        ecqls__ohge = vbo__szdw._compiler
        flags = compiler.Flags()
        rbjao__bka = ecqls__ohge.targetdescr.typing_context
        eagdy__xchws = ecqls__ohge.targetdescr.target_context
        nlu__ljtqw = ecqls__ohge.pipeline_class(rbjao__bka, eagdy__xchws,
            None, None, None, flags, None)
        svz__vpt = InlineWorker(rbjao__bka, eagdy__xchws, ecqls__ohge.
            locals, nlu__ljtqw, flags, None)
        knzjf__mcai = jsldu__kdb.dispatcher.get_call_template
        eaac__zsbt, kjdr__wmpa, uwf__fjy, kws = knzjf__mcai(zpw__cyre, kws)
        if uwf__fjy in self._inline_overloads:
            return self._inline_overloads[uwf__fjy]['iinfo'].signature
        ir = svz__vpt.run_untyped_passes(jsldu__kdb.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, eagdy__xchws, ir, uwf__fjy, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, uwf__fjy, None)
        self._inline_overloads[sig.args] = {'folded_args': uwf__fjy}
        rtnqv__lhjp = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = rtnqv__lhjp
        if not self._inline.is_always_inline:
            sig = jsldu__kdb.get_call_type(self.context, zpw__cyre, kws)
            self._compiled_overloads[sig.args] = jsldu__kdb.get_overload(sig)
        ayx__ilaaj = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': uwf__fjy,
            'iinfo': ayx__ilaaj}
    else:
        sig = jsldu__kdb.get_call_type(self.context, zpw__cyre, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = jsldu__kdb.get_overload(sig)
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
    bbyg__doelf = [True, False]
    fhd__ldj = [False, True]
    ecpff__kril = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    gfoy__ijkmd = get_local_target(context)
    ide__npqek = utils.order_by_target_specificity(gfoy__ijkmd, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for hszz__zblys in ide__npqek:
        qztq__dfpy = hszz__zblys(context)
        qrfr__iajg = bbyg__doelf if qztq__dfpy.prefer_literal else fhd__ldj
        qrfr__iajg = [True] if getattr(qztq__dfpy, '_no_unliteral', False
            ) else qrfr__iajg
        for bwbtn__nbyww in qrfr__iajg:
            try:
                if bwbtn__nbyww:
                    sig = qztq__dfpy.apply(args, kws)
                else:
                    pwh__utg = tuple([_unlit_non_poison(a) for a in args])
                    twvyi__skqb = {gipf__sfkqe: _unlit_non_poison(
                        xreh__kuud) for gipf__sfkqe, xreh__kuud in kws.items()}
                    sig = qztq__dfpy.apply(pwh__utg, twvyi__skqb)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    ecpff__kril.add_error(qztq__dfpy, False, e, bwbtn__nbyww)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = qztq__dfpy.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    grvhl__pfc = getattr(qztq__dfpy, 'cases', None)
                    if grvhl__pfc is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            grvhl__pfc)
                    else:
                        msg = 'No match.'
                    ecpff__kril.add_error(qztq__dfpy, True, msg, bwbtn__nbyww)
    ecpff__kril.raise_error()


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
    eaac__zsbt = self.template(context)
    oqyy__jkkx = None
    niarl__jhseb = None
    djmn__fxiy = None
    qrfr__iajg = [True, False] if eaac__zsbt.prefer_literal else [False, True]
    qrfr__iajg = [True] if getattr(eaac__zsbt, '_no_unliteral', False
        ) else qrfr__iajg
    for bwbtn__nbyww in qrfr__iajg:
        if bwbtn__nbyww:
            try:
                djmn__fxiy = eaac__zsbt.apply(args, kws)
            except Exception as ehm__tzhz:
                if isinstance(ehm__tzhz, errors.ForceLiteralArg):
                    raise ehm__tzhz
                oqyy__jkkx = ehm__tzhz
                djmn__fxiy = None
            else:
                break
        else:
            bda__xqjnz = tuple([_unlit_non_poison(a) for a in args])
            qvpyf__hrv = {gipf__sfkqe: _unlit_non_poison(xreh__kuud) for 
                gipf__sfkqe, xreh__kuud in kws.items()}
            pwqx__ouq = bda__xqjnz == args and kws == qvpyf__hrv
            if not pwqx__ouq and djmn__fxiy is None:
                try:
                    djmn__fxiy = eaac__zsbt.apply(bda__xqjnz, qvpyf__hrv)
                except Exception as ehm__tzhz:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        ehm__tzhz, errors.NumbaError):
                        raise ehm__tzhz
                    if isinstance(ehm__tzhz, errors.ForceLiteralArg):
                        if eaac__zsbt.prefer_literal:
                            raise ehm__tzhz
                    niarl__jhseb = ehm__tzhz
                else:
                    break
    if djmn__fxiy is None and (niarl__jhseb is not None or oqyy__jkkx is not
        None):
        mdsn__hflv = '- Resolution failure for {} arguments:\n{}\n'
        uguav__ojn = _termcolor.highlight(mdsn__hflv)
        if numba.core.config.DEVELOPER_MODE:
            soo__lepol = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    swaf__prf = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    swaf__prf = ['']
                urq__ooan = '\n{}'.format(2 * soo__lepol)
                iovfd__hwpg = _termcolor.reset(urq__ooan + urq__ooan.join(
                    _bt_as_lines(swaf__prf)))
                return _termcolor.reset(iovfd__hwpg)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            kdpyv__mpvg = str(e)
            kdpyv__mpvg = kdpyv__mpvg if kdpyv__mpvg else str(repr(e)
                ) + add_bt(e)
            bhrmr__hyzmq = errors.TypingError(textwrap.dedent(kdpyv__mpvg))
            return uguav__ojn.format(literalness, str(bhrmr__hyzmq))
        import bodo
        if isinstance(oqyy__jkkx, bodo.utils.typing.BodoError):
            raise oqyy__jkkx
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', oqyy__jkkx) +
                nested_msg('non-literal', niarl__jhseb))
        else:
            if 'missing a required argument' in oqyy__jkkx.msg:
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
            raise errors.TypingError(msg, loc=oqyy__jkkx.loc)
    return djmn__fxiy


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
    nwa__axhte = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=nwa__axhte)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            tjab__tfg = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), tjab__tfg)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    tuqg__sxm = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            tuqg__sxm.append(types.Omitted(a.value))
        else:
            tuqg__sxm.append(self.typeof_pyval(a))
    ses__jxzk = None
    try:
        error = None
        ses__jxzk = self.compile(tuple(tuqg__sxm))
    except errors.ForceLiteralArg as e:
        uucco__cqnql = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if uucco__cqnql:
            doos__bzhv = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            yyfy__ccbn = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(uucco__cqnql))
            raise errors.CompilerError(doos__bzhv.format(yyfy__ccbn))
        zpw__cyre = []
        try:
            for i, xreh__kuud in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        zpw__cyre.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        zpw__cyre.append(types.literal(args[i]))
                else:
                    zpw__cyre.append(args[i])
            args = zpw__cyre
        except (OSError, FileNotFoundError) as dqtu__bjdpj:
            error = FileNotFoundError(str(dqtu__bjdpj) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                ses__jxzk = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        ygjj__rgg = []
        for i, hvqk__xakq in enumerate(args):
            val = hvqk__xakq.value if isinstance(hvqk__xakq, numba.core.
                dispatcher.OmittedArg) else hvqk__xakq
            try:
                qkxho__uaqsi = typeof(val, Purpose.argument)
            except ValueError as zocdy__ysglh:
                ygjj__rgg.append((i, str(zocdy__ysglh)))
            else:
                if qkxho__uaqsi is None:
                    ygjj__rgg.append((i,
                        f'cannot determine Numba type of value {val}'))
        if ygjj__rgg:
            mhus__hddxj = '\n'.join(f'- argument {i}: {adog__ituc}' for i,
                adog__ituc in ygjj__rgg)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{mhus__hddxj}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                dhz__fqox = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                zehhq__enrwr = False
                for lyyu__wlwg in dhz__fqox:
                    if lyyu__wlwg in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        zehhq__enrwr = True
                        break
                if not zehhq__enrwr:
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
                tjab__tfg = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), tjab__tfg)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return ses__jxzk


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
    for pbdp__ilrh in cres.library._codegen._engine._defined_symbols:
        if pbdp__ilrh.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in pbdp__ilrh and (
            'bodo_gb_udf_update_local' in pbdp__ilrh or 
            'bodo_gb_udf_combine' in pbdp__ilrh or 'bodo_gb_udf_eval' in
            pbdp__ilrh or 'bodo_gb_apply_general_udfs' in pbdp__ilrh):
            gb_agg_cfunc_addr[pbdp__ilrh
                ] = cres.library.get_pointer_to_function(pbdp__ilrh)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for pbdp__ilrh in cres.library._codegen._engine._defined_symbols:
        if pbdp__ilrh.startswith('cfunc') and ('get_join_cond_addr' not in
            pbdp__ilrh or 'bodo_join_gen_cond' in pbdp__ilrh):
            join_gen_cond_cfunc_addr[pbdp__ilrh
                ] = cres.library.get_pointer_to_function(pbdp__ilrh)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    vbo__szdw = self._get_dispatcher_for_current_target()
    if vbo__szdw is not self:
        return vbo__szdw.compile(sig)
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
            iesl__vytr = self.overloads.get(tuple(args))
            if iesl__vytr is not None:
                return iesl__vytr.entry_point
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
            cxux__tss = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=cxux__tss):
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
                xes__vuz = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in xes__vuz:
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
    kdlkv__ivi = self._final_module
    edrty__ocwut = []
    wyov__iabl = 0
    for fn in kdlkv__ivi.functions:
        wyov__iabl += 1
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
            edrty__ocwut.append(fn.name)
    if wyov__iabl == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if edrty__ocwut:
        kdlkv__ivi = kdlkv__ivi.clone()
        for name in edrty__ocwut:
            kdlkv__ivi.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = kdlkv__ivi
    return kdlkv__ivi


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
    for hyc__bgfmu in self.constraints:
        loc = hyc__bgfmu.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                hyc__bgfmu(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                ofbk__ldovw = numba.core.errors.TypingError(str(e), loc=
                    hyc__bgfmu.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(ofbk__ldovw, e))
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
                    ofbk__ldovw = numba.core.errors.TypingError(msg.format(
                        con=hyc__bgfmu, err=str(e)), loc=hyc__bgfmu.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(ofbk__ldovw, e))
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
    for dxyml__wemn in self._failures.values():
        for fdbwh__xfeh in dxyml__wemn:
            if isinstance(fdbwh__xfeh.error, ForceLiteralArg):
                raise fdbwh__xfeh.error
            if isinstance(fdbwh__xfeh.error, bodo.utils.typing.BodoError):
                raise fdbwh__xfeh.error
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
    itvml__ijvx = False
    iactv__nnw = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        uld__qczb = set()
        ocli__lfz = lives & alias_set
        for xreh__kuud in ocli__lfz:
            uld__qczb |= alias_map[xreh__kuud]
        lives_n_aliases = lives | uld__qczb | arg_aliases
        if type(stmt) in remove_dead_extensions:
            sbib__yjt = remove_dead_extensions[type(stmt)]
            stmt = sbib__yjt(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                itvml__ijvx = True
                continue
        if isinstance(stmt, ir.Assign):
            zgvvf__aoyv = stmt.target
            gzv__mfott = stmt.value
            if zgvvf__aoyv.name not in lives and has_no_side_effect(gzv__mfott,
                lives_n_aliases, call_table):
                itvml__ijvx = True
                continue
            if saved_array_analysis and zgvvf__aoyv.name in lives and is_expr(
                gzv__mfott, 'getattr'
                ) and gzv__mfott.attr == 'shape' and is_array_typ(typemap[
                gzv__mfott.value.name]) and gzv__mfott.value.name not in lives:
                kec__fdsz = {xreh__kuud: gipf__sfkqe for gipf__sfkqe,
                    xreh__kuud in func_ir.blocks.items()}
                if block in kec__fdsz:
                    kwutr__ropx = kec__fdsz[block]
                    mijoo__itrnk = saved_array_analysis.get_equiv_set(
                        kwutr__ropx)
                    mzp__jdqhs = mijoo__itrnk.get_equiv_set(gzv__mfott.value)
                    if mzp__jdqhs is not None:
                        for xreh__kuud in mzp__jdqhs:
                            if xreh__kuud.endswith('#0'):
                                xreh__kuud = xreh__kuud[:-2]
                            if xreh__kuud in typemap and is_array_typ(typemap
                                [xreh__kuud]) and xreh__kuud in lives:
                                gzv__mfott.value = ir.Var(gzv__mfott.value.
                                    scope, xreh__kuud, gzv__mfott.value.loc)
                                itvml__ijvx = True
                                break
            if isinstance(gzv__mfott, ir.Var
                ) and zgvvf__aoyv.name == gzv__mfott.name:
                itvml__ijvx = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                itvml__ijvx = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            gsu__glqw = analysis.ir_extension_usedefs[type(stmt)]
            ipj__kahkh, bggrz__xzqyt = gsu__glqw(stmt)
            lives -= bggrz__xzqyt
            lives |= ipj__kahkh
        else:
            lives |= {xreh__kuud.name for xreh__kuud in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                lvcn__nxrrl = set()
                if isinstance(gzv__mfott, ir.Expr):
                    lvcn__nxrrl = {xreh__kuud.name for xreh__kuud in
                        gzv__mfott.list_vars()}
                if zgvvf__aoyv.name not in lvcn__nxrrl:
                    lives.remove(zgvvf__aoyv.name)
        iactv__nnw.append(stmt)
    iactv__nnw.reverse()
    block.body = iactv__nnw
    return itvml__ijvx


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            mhowe__qhv, = args
            if isinstance(mhowe__qhv, types.IterableType):
                dtype = mhowe__qhv.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), mhowe__qhv)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    ofe__lgna = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (ofe__lgna, self.dtype)
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
        except LiteralTypingError as jqd__mpu:
            return
    try:
        return literal(value)
    except LiteralTypingError as jqd__mpu:
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
        lqy__rnpmj = py_func.__qualname__
    except AttributeError as jqd__mpu:
        lqy__rnpmj = py_func.__name__
    rys__kihg = inspect.getfile(py_func)
    for cls in self._locator_classes:
        bew__ofreo = cls.from_function(py_func, rys__kihg)
        if bew__ofreo is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (lqy__rnpmj, rys__kihg))
    self._locator = bew__ofreo
    kosgx__axp = inspect.getfile(py_func)
    mxh__kao = os.path.splitext(os.path.basename(kosgx__axp))[0]
    if rys__kihg.startswith('<ipython-'):
        hsgt__dll = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', mxh__kao, count=1)
        if hsgt__dll == mxh__kao:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        mxh__kao = hsgt__dll
    ojzxu__psv = '%s.%s' % (mxh__kao, lqy__rnpmj)
    dpqxq__emxl = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(ojzxu__psv, dpqxq__emxl)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    qzw__mqjds = list(filter(lambda a: self._istuple(a.name), args))
    if len(qzw__mqjds) == 2 and fn.__name__ == 'add':
        yuqtf__skli = self.typemap[qzw__mqjds[0].name]
        tuzx__ylto = self.typemap[qzw__mqjds[1].name]
        if yuqtf__skli.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                qzw__mqjds[1]))
        if tuzx__ylto.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                qzw__mqjds[0]))
        try:
            rtvd__nrx = [equiv_set.get_shape(x) for x in qzw__mqjds]
            if None in rtvd__nrx:
                return None
            vwxeb__cein = sum(rtvd__nrx, ())
            return ArrayAnalysis.AnalyzeResult(shape=vwxeb__cein)
        except GuardException as jqd__mpu:
            return None
    qnbeh__riis = list(filter(lambda a: self._isarray(a.name), args))
    require(len(qnbeh__riis) > 0)
    bktir__qvzs = [x.name for x in qnbeh__riis]
    fggi__khtv = [self.typemap[x.name].ndim for x in qnbeh__riis]
    ghvd__seo = max(fggi__khtv)
    require(ghvd__seo > 0)
    rtvd__nrx = [equiv_set.get_shape(x) for x in qnbeh__riis]
    if any(a is None for a in rtvd__nrx):
        return ArrayAnalysis.AnalyzeResult(shape=qnbeh__riis[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, qnbeh__riis))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, rtvd__nrx,
        bktir__qvzs)


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
    cuiq__phjtg = code_obj.code
    erpet__xhlni = len(cuiq__phjtg.co_freevars)
    ojfy__viwy = cuiq__phjtg.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        ncqwp__hdcbi, op = ir_utils.find_build_sequence(caller_ir, code_obj
            .closure)
        assert op == 'build_tuple'
        ojfy__viwy = [xreh__kuud.name for xreh__kuud in ncqwp__hdcbi]
    qnry__trzf = caller_ir.func_id.func.__globals__
    try:
        qnry__trzf = getattr(code_obj, 'globals', qnry__trzf)
    except KeyError as jqd__mpu:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    gguo__fjix = []
    for x in ojfy__viwy:
        try:
            qxb__pih = caller_ir.get_definition(x)
        except KeyError as jqd__mpu:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(qxb__pih, (ir.Const, ir.Global, ir.FreeVar)):
            val = qxb__pih.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                spdav__vmxx = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                qnry__trzf[spdav__vmxx] = bodo.jit(distributed=False)(val)
                qnry__trzf[spdav__vmxx].is_nested_func = True
                val = spdav__vmxx
            if isinstance(val, CPUDispatcher):
                spdav__vmxx = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                qnry__trzf[spdav__vmxx] = val
                val = spdav__vmxx
            gguo__fjix.append(val)
        elif isinstance(qxb__pih, ir.Expr) and qxb__pih.op == 'make_function':
            eacs__gxsgx = convert_code_obj_to_function(qxb__pih, caller_ir)
            spdav__vmxx = ir_utils.mk_unique_var('nested_func').replace('.',
                '_')
            qnry__trzf[spdav__vmxx] = bodo.jit(distributed=False)(eacs__gxsgx)
            qnry__trzf[spdav__vmxx].is_nested_func = True
            gguo__fjix.append(spdav__vmxx)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    qvcob__gyboo = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in
        enumerate(gguo__fjix)])
    qxasf__hqccp = ','.join([('c_%d' % i) for i in range(erpet__xhlni)])
    ttuoi__ncaul = list(cuiq__phjtg.co_varnames)
    hcgm__easx = 0
    uobz__lrsy = cuiq__phjtg.co_argcount
    wlu__sgdgs = caller_ir.get_definition(code_obj.defaults)
    if wlu__sgdgs is not None:
        if isinstance(wlu__sgdgs, tuple):
            d = [caller_ir.get_definition(x).value for x in wlu__sgdgs]
            czq__jijy = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in wlu__sgdgs.items]
            czq__jijy = tuple(d)
        hcgm__easx = len(czq__jijy)
    rwie__wxa = uobz__lrsy - hcgm__easx
    bomb__pyke = ','.join([('%s' % ttuoi__ncaul[i]) for i in range(rwie__wxa)])
    if hcgm__easx:
        oaz__byos = [('%s = %s' % (ttuoi__ncaul[i + rwie__wxa], czq__jijy[i
            ])) for i in range(hcgm__easx)]
        bomb__pyke += ', '
        bomb__pyke += ', '.join(oaz__byos)
    return _create_function_from_code_obj(cuiq__phjtg, qvcob__gyboo,
        bomb__pyke, qxasf__hqccp, qnry__trzf)


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
    for gres__zxdmi, (lzc__ahj, zbp__ibo) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % zbp__ibo)
            gyzk__rmi = _pass_registry.get(lzc__ahj).pass_inst
            if isinstance(gyzk__rmi, CompilerPass):
                self._runPass(gres__zxdmi, gyzk__rmi, state)
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
                    pipeline_name, zbp__ibo)
                agle__lls = self._patch_error(msg, e)
                raise agle__lls
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
    ysk__pudru = None
    bggrz__xzqyt = {}

    def lookup(var, already_seen, varonly=True):
        val = bggrz__xzqyt.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    ghgni__are = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        zgvvf__aoyv = stmt.target
        gzv__mfott = stmt.value
        bggrz__xzqyt[zgvvf__aoyv.name] = gzv__mfott
        if isinstance(gzv__mfott, ir.Var) and gzv__mfott.name in bggrz__xzqyt:
            gzv__mfott = lookup(gzv__mfott, set())
        if isinstance(gzv__mfott, ir.Expr):
            fow__irx = set(lookup(xreh__kuud, set(), True).name for
                xreh__kuud in gzv__mfott.list_vars())
            if name in fow__irx:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(gzv__mfott)]
                xsvq__loxnl = [x for x, yuzs__lqjgc in args if yuzs__lqjgc.
                    name != name]
                args = [(x, yuzs__lqjgc) for x, yuzs__lqjgc in args if x !=
                    yuzs__lqjgc.name]
                bavdp__gdfkr = dict(args)
                if len(xsvq__loxnl) == 1:
                    bavdp__gdfkr[xsvq__loxnl[0]] = ir.Var(zgvvf__aoyv.scope,
                        name + '#init', zgvvf__aoyv.loc)
                replace_vars_inner(gzv__mfott, bavdp__gdfkr)
                ysk__pudru = nodes[i:]
                break
    return ysk__pudru


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
        hoth__zqa = expand_aliases({xreh__kuud.name for xreh__kuud in stmt.
            list_vars()}, alias_map, arg_aliases)
        mujv__hux = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        isjc__iln = expand_aliases({xreh__kuud.name for xreh__kuud in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        xywp__mic = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(mujv__hux & isjc__iln | xywp__mic & hoth__zqa) == 0:
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
    qxca__xtb = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            qxca__xtb.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                qxca__xtb.update(get_parfor_writes(stmt, func_ir))
    return qxca__xtb


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    qxca__xtb = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        qxca__xtb.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        qxca__xtb = {xreh__kuud.name for xreh__kuud in stmt.df_out_vars.
            values()}
        if stmt.out_key_vars is not None:
            qxca__xtb.update({xreh__kuud.name for xreh__kuud in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        qxca__xtb = {xreh__kuud.name for xreh__kuud in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        qxca__xtb = {xreh__kuud.name for xreh__kuud in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            qxca__xtb.update({xreh__kuud.name for xreh__kuud in stmt.
                out_key_arrs})
            qxca__xtb.update({xreh__kuud.name for xreh__kuud in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        ylq__qijwe = guard(find_callname, func_ir, stmt.value)
        if ylq__qijwe in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            qxca__xtb.add(stmt.value.args[0].name)
        if ylq__qijwe == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            qxca__xtb.add(stmt.value.args[1].name)
    return qxca__xtb


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
        sbib__yjt = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        yabr__nkfj = sbib__yjt.format(self, msg)
        self.args = yabr__nkfj,
    else:
        sbib__yjt = _termcolor.errmsg('{0}')
        yabr__nkfj = sbib__yjt.format(self)
        self.args = yabr__nkfj,
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
        for lvevk__dxl in options['distributed']:
            dist_spec[lvevk__dxl] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for lvevk__dxl in options['distributed_block']:
            dist_spec[lvevk__dxl] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    kxw__idytu = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, eqvu__laer in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(eqvu__laer)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    gcroz__kbi = {}
    for vcf__speq in reversed(inspect.getmro(cls)):
        gcroz__kbi.update(vcf__speq.__dict__)
    lfl__jbbz, zbaro__jae, qzfyb__zdgg, kjrai__zwrzs = {}, {}, {}, {}
    for gipf__sfkqe, xreh__kuud in gcroz__kbi.items():
        if isinstance(xreh__kuud, pytypes.FunctionType):
            lfl__jbbz[gipf__sfkqe] = xreh__kuud
        elif isinstance(xreh__kuud, property):
            zbaro__jae[gipf__sfkqe] = xreh__kuud
        elif isinstance(xreh__kuud, staticmethod):
            qzfyb__zdgg[gipf__sfkqe] = xreh__kuud
        else:
            kjrai__zwrzs[gipf__sfkqe] = xreh__kuud
    tgczy__xdcfw = (set(lfl__jbbz) | set(zbaro__jae) | set(qzfyb__zdgg)) & set(
        spec)
    if tgczy__xdcfw:
        raise NameError('name shadowing: {0}'.format(', '.join(tgczy__xdcfw)))
    lomho__uknw = kjrai__zwrzs.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(kjrai__zwrzs)
    if kjrai__zwrzs:
        msg = 'class members are not yet supported: {0}'
        swzwo__ijilr = ', '.join(kjrai__zwrzs.keys())
        raise TypeError(msg.format(swzwo__ijilr))
    for gipf__sfkqe, xreh__kuud in zbaro__jae.items():
        if xreh__kuud.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(gipf__sfkqe)
                )
    jit_methods = {gipf__sfkqe: bodo.jit(returns_maybe_distributed=
        kxw__idytu)(xreh__kuud) for gipf__sfkqe, xreh__kuud in lfl__jbbz.
        items()}
    jit_props = {}
    for gipf__sfkqe, xreh__kuud in zbaro__jae.items():
        rwg__iijtp = {}
        if xreh__kuud.fget:
            rwg__iijtp['get'] = bodo.jit(xreh__kuud.fget)
        if xreh__kuud.fset:
            rwg__iijtp['set'] = bodo.jit(xreh__kuud.fset)
        jit_props[gipf__sfkqe] = rwg__iijtp
    jit_static_methods = {gipf__sfkqe: bodo.jit(xreh__kuud.__func__) for 
        gipf__sfkqe, xreh__kuud in qzfyb__zdgg.items()}
    voqx__xddz = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    bbj__xbf = dict(class_type=voqx__xddz, __doc__=lomho__uknw)
    bbj__xbf.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), bbj__xbf)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, voqx__xddz)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(voqx__xddz, typingctx, targetctx).register()
    as_numba_type.register(cls, voqx__xddz.instance_type)
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
    qdac__mhjga = ','.join('{0}:{1}'.format(gipf__sfkqe, xreh__kuud) for 
        gipf__sfkqe, xreh__kuud in struct.items())
    vmd__csuc = ','.join('{0}:{1}'.format(gipf__sfkqe, xreh__kuud) for 
        gipf__sfkqe, xreh__kuud in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), qdac__mhjga, vmd__csuc)
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
    ayad__bsuuz = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if ayad__bsuuz is None:
        return
    xnsbf__ggxy, yzcd__eqew = ayad__bsuuz
    for a in itertools.chain(xnsbf__ggxy, yzcd__eqew.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, xnsbf__ggxy, yzcd__eqew)
    except ForceLiteralArg as e:
        fdo__bmqsf = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(fdo__bmqsf, self.kws)
        xdqp__pcut = set()
        fpdvi__odo = set()
        ozj__lehy = {}
        for gres__zxdmi in e.requested_args:
            ivd__bzg = typeinfer.func_ir.get_definition(folded[gres__zxdmi])
            if isinstance(ivd__bzg, ir.Arg):
                xdqp__pcut.add(ivd__bzg.index)
                if ivd__bzg.index in e.file_infos:
                    ozj__lehy[ivd__bzg.index] = e.file_infos[ivd__bzg.index]
            else:
                fpdvi__odo.add(gres__zxdmi)
        if fpdvi__odo:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif xdqp__pcut:
            raise ForceLiteralArg(xdqp__pcut, loc=self.loc, file_infos=
                ozj__lehy)
    if sig is None:
        ezo__voi = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in xnsbf__ggxy]
        args += [('%s=%s' % (gipf__sfkqe, xreh__kuud)) for gipf__sfkqe,
            xreh__kuud in sorted(yzcd__eqew.items())]
        gdtvt__obpew = ezo__voi.format(fnty, ', '.join(map(str, args)))
        swyya__dxqsy = context.explain_function_type(fnty)
        msg = '\n'.join([gdtvt__obpew, swyya__dxqsy])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        jkthu__soiz = context.unify_pairs(sig.recvr, fnty.this)
        if jkthu__soiz is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if jkthu__soiz is not None and jkthu__soiz.is_precise():
            couq__fkft = fnty.copy(this=jkthu__soiz)
            typeinfer.propagate_refined_type(self.func, couq__fkft)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            wyovb__uww = target.getone()
            if context.unify_pairs(wyovb__uww, sig.return_type) == wyovb__uww:
                sig = sig.replace(return_type=wyovb__uww)
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
        doos__bzhv = '*other* must be a {} but got a {} instead'
        raise TypeError(doos__bzhv.format(ForceLiteralArg, type(other)))
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
    bkke__dkzeb = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for gipf__sfkqe, xreh__kuud in kwargs.items():
        dede__ftan = None
        try:
            igs__rkk = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var(
                'dummy'), loc)
            func_ir._definitions[igs__rkk.name] = [xreh__kuud]
            dede__ftan = get_const_value_inner(func_ir, igs__rkk)
            func_ir._definitions.pop(igs__rkk.name)
            if isinstance(dede__ftan, str):
                dede__ftan = sigutils._parse_signature_string(dede__ftan)
            if isinstance(dede__ftan, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {gipf__sfkqe} is annotated as type class {dede__ftan}."""
                    )
            assert isinstance(dede__ftan, types.Type)
            if isinstance(dede__ftan, (types.List, types.Set)):
                dede__ftan = dede__ftan.copy(reflected=False)
            bkke__dkzeb[gipf__sfkqe] = dede__ftan
        except BodoError as jqd__mpu:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(dede__ftan, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(xreh__kuud, ir.Global):
                    msg = f'Global {xreh__kuud.name!r} is not defined.'
                if isinstance(xreh__kuud, ir.FreeVar):
                    msg = f'Freevar {xreh__kuud.name!r} is not defined.'
            if isinstance(xreh__kuud, ir.Expr) and xreh__kuud.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=gipf__sfkqe, msg=msg, loc=loc)
    for name, typ in bkke__dkzeb.items():
        self._legalize_arg_type(name, typ, loc)
    return bkke__dkzeb


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
    naxr__vob = inst.arg
    assert naxr__vob > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(naxr__vob)]))
    tmps = [state.make_temp() for _ in range(naxr__vob - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    cumyc__kupji = ir.Global('format', format, loc=self.loc)
    self.store(value=cumyc__kupji, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    lnqyr__ygwv = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=lnqyr__ygwv, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    naxr__vob = inst.arg
    assert naxr__vob > 0, 'invalid BUILD_STRING count'
    yrugh__ovyjy = self.get(strings[0])
    for other, sqfzn__bcop in zip(strings[1:], tmps):
        other = self.get(other)
        hzasu__cvzn = ir.Expr.binop(operator.add, lhs=yrugh__ovyjy, rhs=
            other, loc=self.loc)
        self.store(hzasu__cvzn, sqfzn__bcop)
        yrugh__ovyjy = self.get(sqfzn__bcop)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    mzi__mml = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, mzi__mml])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    jrlf__uvz = mk_unique_var(f'{var_name}')
    flgg__udvmc = jrlf__uvz.replace('<', '_').replace('>', '_')
    flgg__udvmc = flgg__udvmc.replace('.', '_').replace('$', '_v')
    return flgg__udvmc


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
                gkb__kis = get_overload_const_str(val2)
                if gkb__kis != 'ns':
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
        vov__kyrxl = states['defmap']
        if len(vov__kyrxl) == 0:
            xedq__tyx = assign.target
            numba.core.ssa._logger.debug('first assign: %s', xedq__tyx)
            if xedq__tyx.name not in scope.localvars:
                xedq__tyx = scope.define(assign.target.name, loc=assign.loc)
        else:
            xedq__tyx = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=xedq__tyx, value=assign.value, loc=assign.loc
            )
        vov__kyrxl[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    jyoqw__wtb = []
    for gipf__sfkqe, xreh__kuud in typing.npydecl.registry.globals:
        if gipf__sfkqe == func:
            jyoqw__wtb.append(xreh__kuud)
    for gipf__sfkqe, xreh__kuud in typing.templates.builtin_registry.globals:
        if gipf__sfkqe == func:
            jyoqw__wtb.append(xreh__kuud)
    if len(jyoqw__wtb) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return jyoqw__wtb


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    tzkbe__wepcw = {}
    oxca__knp = find_topo_order(blocks)
    lky__hbf = {}
    for kwutr__ropx in oxca__knp:
        block = blocks[kwutr__ropx]
        iactv__nnw = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                zgvvf__aoyv = stmt.target.name
                gzv__mfott = stmt.value
                if (gzv__mfott.op == 'getattr' and gzv__mfott.attr in
                    arr_math and isinstance(typemap[gzv__mfott.value.name],
                    types.npytypes.Array)):
                    gzv__mfott = stmt.value
                    elh__akpm = gzv__mfott.value
                    tzkbe__wepcw[zgvvf__aoyv] = elh__akpm
                    scope = elh__akpm.scope
                    loc = elh__akpm.loc
                    mcm__ouqhg = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[mcm__ouqhg.name] = types.misc.Module(numpy)
                    mzqzr__dnv = ir.Global('np', numpy, loc)
                    gmy__fpnmj = ir.Assign(mzqzr__dnv, mcm__ouqhg, loc)
                    gzv__mfott.value = mcm__ouqhg
                    iactv__nnw.append(gmy__fpnmj)
                    func_ir._definitions[mcm__ouqhg.name] = [mzqzr__dnv]
                    func = getattr(numpy, gzv__mfott.attr)
                    jato__udhhp = get_np_ufunc_typ_lst(func)
                    lky__hbf[zgvvf__aoyv] = jato__udhhp
                if (gzv__mfott.op == 'call' and gzv__mfott.func.name in
                    tzkbe__wepcw):
                    elh__akpm = tzkbe__wepcw[gzv__mfott.func.name]
                    kqh__put = calltypes.pop(gzv__mfott)
                    mmc__ysqvq = kqh__put.args[:len(gzv__mfott.args)]
                    clw__szkd = {name: typemap[xreh__kuud.name] for name,
                        xreh__kuud in gzv__mfott.kws}
                    gjzm__jip = lky__hbf[gzv__mfott.func.name]
                    suvmo__kbbh = None
                    for hxhs__gmn in gjzm__jip:
                        try:
                            suvmo__kbbh = hxhs__gmn.get_call_type(typingctx,
                                [typemap[elh__akpm.name]] + list(mmc__ysqvq
                                ), clw__szkd)
                            typemap.pop(gzv__mfott.func.name)
                            typemap[gzv__mfott.func.name] = hxhs__gmn
                            calltypes[gzv__mfott] = suvmo__kbbh
                            break
                        except Exception as jqd__mpu:
                            pass
                    if suvmo__kbbh is None:
                        raise TypeError(
                            f'No valid template found for {gzv__mfott.func.name}'
                            )
                    gzv__mfott.args = [elh__akpm] + gzv__mfott.args
            iactv__nnw.append(stmt)
        block.body = iactv__nnw


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    jlvne__abpyd = ufunc.nin
    zishi__usoe = ufunc.nout
    rwie__wxa = ufunc.nargs
    assert rwie__wxa == jlvne__abpyd + zishi__usoe
    if len(args) < jlvne__abpyd:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            jlvne__abpyd))
    if len(args) > rwie__wxa:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), rwie__wxa))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    keuhy__yyuid = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    bvbtb__nrst = max(keuhy__yyuid)
    pwtqv__zjoj = args[jlvne__abpyd:]
    if not all(d == bvbtb__nrst for d in keuhy__yyuid[jlvne__abpyd:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(vhr__wdhh, types.ArrayCompatible) and not
        isinstance(vhr__wdhh, types.Bytes) for vhr__wdhh in pwtqv__zjoj):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(vhr__wdhh.mutable for vhr__wdhh in pwtqv__zjoj):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    mbwh__oeb = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    bgwa__nyubv = None
    if bvbtb__nrst > 0 and len(pwtqv__zjoj) < ufunc.nout:
        bgwa__nyubv = 'C'
        ztthj__mgcrj = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in ztthj__mgcrj and 'F' in ztthj__mgcrj:
            bgwa__nyubv = 'F'
    return mbwh__oeb, pwtqv__zjoj, bvbtb__nrst, bgwa__nyubv


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
        ujoik__gkqj = 'Dict.key_type cannot be of type {}'
        raise TypingError(ujoik__gkqj.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        ujoik__gkqj = 'Dict.value_type cannot be of type {}'
        raise TypingError(ujoik__gkqj.format(valty))
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
    yila__nwj = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[yila__nwj]
        return impl, args
    except KeyError as jqd__mpu:
        pass
    impl, args = self._build_impl(yila__nwj, args, kws)
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
        xogr__ssyak = find_topo_order(parfor.loop_body)
    lem__tttwk = xogr__ssyak[0]
    phn__nama = {}
    _update_parfor_get_setitems(parfor.loop_body[lem__tttwk].body, parfor.
        index_var, alias_map, phn__nama, lives_n_aliases)
    ayt__tvryy = set(phn__nama.keys())
    for wtk__kik in xogr__ssyak:
        if wtk__kik == lem__tttwk:
            continue
        for stmt in parfor.loop_body[wtk__kik].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            fehtn__lygx = set(xreh__kuud.name for xreh__kuud in stmt.
                list_vars())
            anpog__vis = fehtn__lygx & ayt__tvryy
            for a in anpog__vis:
                phn__nama.pop(a, None)
    for wtk__kik in xogr__ssyak:
        if wtk__kik == lem__tttwk:
            continue
        block = parfor.loop_body[wtk__kik]
        eao__gizzc = phn__nama.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            eao__gizzc, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    kyk__slx = max(blocks.keys())
    wxmwo__wmnc, sqe__bhe = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    zzw__vuv = ir.Jump(wxmwo__wmnc, ir.Loc('parfors_dummy', -1))
    blocks[kyk__slx].body.append(zzw__vuv)
    vmtb__quljx = compute_cfg_from_blocks(blocks)
    vwm__dxb = compute_use_defs(blocks)
    ozsla__nnqq = compute_live_map(vmtb__quljx, blocks, vwm__dxb.usemap,
        vwm__dxb.defmap)
    alias_set = set(alias_map.keys())
    for kwutr__ropx, block in blocks.items():
        iactv__nnw = []
        spw__qomr = {xreh__kuud.name for xreh__kuud in block.terminator.
            list_vars()}
        for vpxz__qbtmm, viae__zxlk in vmtb__quljx.successors(kwutr__ropx):
            spw__qomr |= ozsla__nnqq[vpxz__qbtmm]
        for stmt in reversed(block.body):
            uld__qczb = spw__qomr & alias_set
            for xreh__kuud in uld__qczb:
                spw__qomr |= alias_map[xreh__kuud]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in spw__qomr and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                ylq__qijwe = guard(find_callname, func_ir, stmt.value)
                if ylq__qijwe == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in spw__qomr and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            spw__qomr |= {xreh__kuud.name for xreh__kuud in stmt.list_vars()}
            iactv__nnw.append(stmt)
        iactv__nnw.reverse()
        block.body = iactv__nnw
    typemap.pop(sqe__bhe.name)
    blocks[kyk__slx].body.pop()

    def trim_empty_parfor_branches(parfor):
        rjth__nwttk = False
        blocks = parfor.loop_body.copy()
        for kwutr__ropx, block in blocks.items():
            if len(block.body):
                eyijk__brkv = block.body[-1]
                if isinstance(eyijk__brkv, ir.Branch):
                    if len(blocks[eyijk__brkv.truebr].body) == 1 and len(blocks
                        [eyijk__brkv.falsebr].body) == 1:
                        dbl__pbii = blocks[eyijk__brkv.truebr].body[0]
                        qbi__eke = blocks[eyijk__brkv.falsebr].body[0]
                        if isinstance(dbl__pbii, ir.Jump) and isinstance(
                            qbi__eke, ir.Jump
                            ) and dbl__pbii.target == qbi__eke.target:
                            parfor.loop_body[kwutr__ropx].body[-1] = ir.Jump(
                                dbl__pbii.target, eyijk__brkv.loc)
                            rjth__nwttk = True
                    elif len(blocks[eyijk__brkv.truebr].body) == 1:
                        dbl__pbii = blocks[eyijk__brkv.truebr].body[0]
                        if isinstance(dbl__pbii, ir.Jump
                            ) and dbl__pbii.target == eyijk__brkv.falsebr:
                            parfor.loop_body[kwutr__ropx].body[-1] = ir.Jump(
                                dbl__pbii.target, eyijk__brkv.loc)
                            rjth__nwttk = True
                    elif len(blocks[eyijk__brkv.falsebr].body) == 1:
                        qbi__eke = blocks[eyijk__brkv.falsebr].body[0]
                        if isinstance(qbi__eke, ir.Jump
                            ) and qbi__eke.target == eyijk__brkv.truebr:
                            parfor.loop_body[kwutr__ropx].body[-1] = ir.Jump(
                                qbi__eke.target, eyijk__brkv.loc)
                            rjth__nwttk = True
        return rjth__nwttk
    rjth__nwttk = True
    while rjth__nwttk:
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
        rjth__nwttk = trim_empty_parfor_branches(parfor)
    kcrzq__fvwjl = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        kcrzq__fvwjl &= len(block.body) == 0
    if kcrzq__fvwjl:
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
    yac__nxehp = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                yac__nxehp += 1
                parfor = stmt
                goag__jrzuf = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = goag__jrzuf.scope
                loc = ir.Loc('parfors_dummy', -1)
                oyg__aybuq = ir.Var(scope, mk_unique_var('$const'), loc)
                goag__jrzuf.body.append(ir.Assign(ir.Const(0, loc),
                    oyg__aybuq, loc))
                goag__jrzuf.body.append(ir.Return(oyg__aybuq, loc))
                vmtb__quljx = compute_cfg_from_blocks(parfor.loop_body)
                for uia__olmuj in vmtb__quljx.dead_nodes():
                    del parfor.loop_body[uia__olmuj]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                goag__jrzuf = parfor.loop_body[max(parfor.loop_body.keys())]
                goag__jrzuf.body.pop()
                goag__jrzuf.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return yac__nxehp


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
            iesl__vytr = self.overloads.get(tuple(args))
            if iesl__vytr is not None:
                return iesl__vytr.entry_point
            self._pre_compile(args, return_type, flags)
            wmjk__ydnls = self.func_ir
            cxux__tss = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=cxux__tss):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=wmjk__ydnls, args=
                    args, return_type=return_type, flags=flags, locals=self
                    .locals, lifted=(), lifted_from=self.lifted_from,
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
        bpx__hld = copy.deepcopy(flags)
        bpx__hld.no_rewrites = True

        def compile_local(the_ir, the_flags):
            uapvz__qvs = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return uapvz__qvs.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        fuugt__jie = compile_local(func_ir, bpx__hld)
        llao__nep = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    llao__nep = compile_local(func_ir, flags)
                except Exception as jqd__mpu:
                    pass
        if llao__nep is not None:
            cres = llao__nep
        else:
            cres = fuugt__jie
        return cres
    else:
        uapvz__qvs = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return uapvz__qvs.compile_ir(func_ir=func_ir, lifted=lifted,
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
    pvx__oshb = self.get_data_type(typ.dtype)
    ocxf__unoy = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        ocxf__unoy):
        aqs__axxwv = ary.ctypes.data
        zdoh__dioug = self.add_dynamic_addr(builder, aqs__axxwv, info=str(
            type(aqs__axxwv)))
        aodvr__dflcg = self.add_dynamic_addr(builder, id(ary), info=str(
            type(ary)))
        self.global_arrays.append(ary)
    else:
        inkgy__notx = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            inkgy__notx = inkgy__notx.view('int64')
        val = bytearray(inkgy__notx.data)
        bcm__yspj = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        zdoh__dioug = cgutils.global_constant(builder, '.const.array.data',
            bcm__yspj)
        zdoh__dioug.align = self.get_abi_alignment(pvx__oshb)
        aodvr__dflcg = None
    hnza__cnuog = self.get_value_type(types.intp)
    xzqs__bih = [self.get_constant(types.intp, gelpa__rxo) for gelpa__rxo in
        ary.shape]
    krkm__ffgy = lir.Constant(lir.ArrayType(hnza__cnuog, len(xzqs__bih)),
        xzqs__bih)
    avdtg__gjdqz = [self.get_constant(types.intp, gelpa__rxo) for
        gelpa__rxo in ary.strides]
    gtd__rgkzg = lir.Constant(lir.ArrayType(hnza__cnuog, len(avdtg__gjdqz)),
        avdtg__gjdqz)
    submc__htvek = self.get_constant(types.intp, ary.dtype.itemsize)
    hprht__tlqc = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        hprht__tlqc, submc__htvek, zdoh__dioug.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), krkm__ffgy, gtd__rgkzg])


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
    wmqdh__mrf = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    bgj__fgzv = lir.Function(module, wmqdh__mrf, name='nrt_atomic_{0}'.
        format(op))
    [dzix__bic] = bgj__fgzv.args
    syhp__egb = bgj__fgzv.append_basic_block()
    builder = lir.IRBuilder(syhp__egb)
    pkxbb__giuk = lir.Constant(_word_type, 1)
    if False:
        kajnr__xypa = builder.atomic_rmw(op, dzix__bic, pkxbb__giuk,
            ordering=ordering)
        res = getattr(builder, op)(kajnr__xypa, pkxbb__giuk)
        builder.ret(res)
    else:
        kajnr__xypa = builder.load(dzix__bic)
        cqbb__zkf = getattr(builder, op)(kajnr__xypa, pkxbb__giuk)
        vnpo__ddl = builder.icmp_signed('!=', kajnr__xypa, lir.Constant(
            kajnr__xypa.type, -1))
        with cgutils.if_likely(builder, vnpo__ddl):
            builder.store(cqbb__zkf, dzix__bic)
        builder.ret(cqbb__zkf)
    return bgj__fgzv


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
        btow__lpb = state.targetctx.codegen()
        state.library = btow__lpb.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    qhknt__wtq = state.func_ir
    typemap = state.typemap
    ydqy__ltzg = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    zghgb__ojcrj = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            qhknt__wtq, typemap, ydqy__ltzg, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            diez__budtj = lowering.Lower(targetctx, library, fndesc,
                qhknt__wtq, metadata=metadata)
            diez__budtj.lower()
            if not flags.no_cpython_wrapper:
                diez__budtj.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(ydqy__ltzg, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        diez__budtj.create_cfunc_wrapper()
            env = diez__budtj.env
            nru__mvpom = diez__budtj.call_helper
            del diez__budtj
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, nru__mvpom, cfunc=None, env=env)
        else:
            pbdxd__wgz = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(pbdxd__wgz, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, nru__mvpom, cfunc=pbdxd__wgz,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        zle__bbn = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = zle__bbn - zghgb__ojcrj
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
        zdo__mddvr = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, zdo__mddvr),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            anzyk__xiw.do_break()
        mqt__nsll = c.builder.icmp_signed('!=', zdo__mddvr, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(mqt__nsll, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, zdo__mddvr)
                c.pyapi.decref(zdo__mddvr)
                anzyk__xiw.do_break()
        c.pyapi.decref(zdo__mddvr)
    tqtlw__maplg, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(tqtlw__maplg, likely=True) as (xtg__oot, udy__sasx):
        with xtg__oot:
            list.size = size
            ubrzx__upn = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                ubrzx__upn), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        ubrzx__upn))
                    with cgutils.for_range(c.builder, size) as anzyk__xiw:
                        itemobj = c.pyapi.list_getitem(obj, anzyk__xiw.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        jnh__txe = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(jnh__txe.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            anzyk__xiw.do_break()
                        list.setitem(anzyk__xiw.index, jnh__txe.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with udy__sasx:
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
    cnno__vdqpm, ewiuz__upi, vlcre__pnoa, tsxet__lvv, flv__zuzrp = (
        compile_time_get_string_data(literal_string))
    kdlkv__ivi = builder.module
    gv = context.insert_const_bytes(kdlkv__ivi, cnno__vdqpm)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        ewiuz__upi), context.get_constant(types.int32, vlcre__pnoa),
        context.get_constant(types.uint32, tsxet__lvv), context.
        get_constant(_Py_hash_t, -1), context.get_constant_null(types.
        MemInfoPointer(types.voidptr)), context.get_constant_null(types.
        pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    vecrq__kbup = None
    if isinstance(shape, types.Integer):
        vecrq__kbup = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(gelpa__rxo, (types.Integer, types.IntEnumMember)) for
            gelpa__rxo in shape):
            vecrq__kbup = len(shape)
    return vecrq__kbup


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
            vecrq__kbup = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if vecrq__kbup == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    vecrq__kbup))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            bktir__qvzs = self._get_names(x)
            if len(bktir__qvzs) != 0:
                return bktir__qvzs[0]
            return bktir__qvzs
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    bktir__qvzs = self._get_names(obj)
    if len(bktir__qvzs) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(bktir__qvzs[0])


def get_equiv_set(self, obj):
    bktir__qvzs = self._get_names(obj)
    if len(bktir__qvzs) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(bktir__qvzs[0])


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
    uczc__jekmp = []
    for fgyol__jabsr in func_ir.arg_names:
        if fgyol__jabsr in typemap and isinstance(typemap[fgyol__jabsr],
            types.containers.UniTuple) and typemap[fgyol__jabsr].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(fgyol__jabsr))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ioidu__cquem in func_ir.blocks.values():
        for stmt in ioidu__cquem.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    fgxh__fprma = getattr(val, 'code', None)
                    if fgxh__fprma is not None:
                        if getattr(val, 'closure', None) is not None:
                            naj__dsgmu = '<creating a function from a closure>'
                            hzasu__cvzn = ''
                        else:
                            naj__dsgmu = fgxh__fprma.co_name
                            hzasu__cvzn = '(%s) ' % naj__dsgmu
                    else:
                        naj__dsgmu = '<could not ascertain use case>'
                        hzasu__cvzn = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (naj__dsgmu, hzasu__cvzn))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                trwn__rfzyp = False
                if isinstance(val, pytypes.FunctionType):
                    trwn__rfzyp = val in {numba.gdb, numba.gdb_init}
                if not trwn__rfzyp:
                    trwn__rfzyp = getattr(val, '_name', '') == 'gdb_internal'
                if trwn__rfzyp:
                    uczc__jekmp.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    ftqih__htgbb = func_ir.get_definition(var)
                    msikt__wpra = guard(find_callname, func_ir, ftqih__htgbb)
                    if msikt__wpra and msikt__wpra[1] == 'numpy':
                        ty = getattr(numpy, msikt__wpra[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    laoe__izouk = '' if var.startswith('$'
                        ) else "'{}' ".format(var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(laoe__izouk), loc=stmt.loc)
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
    if len(uczc__jekmp) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        xwto__nxgg = '\n'.join([x.strformat() for x in uczc__jekmp])
        raise errors.UnsupportedError(msg % xwto__nxgg)


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
    gipf__sfkqe, xreh__kuud = next(iter(val.items()))
    uohh__kmdy = typeof_impl(gipf__sfkqe, c)
    nxz__udyj = typeof_impl(xreh__kuud, c)
    if uohh__kmdy is None or nxz__udyj is None:
        raise ValueError(
            f'Cannot type dict element type {type(gipf__sfkqe)}, {type(xreh__kuud)}'
            )
    return types.DictType(uohh__kmdy, nxz__udyj)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    koklp__rfta = cgutils.alloca_once_value(c.builder, val)
    twd__eyf = c.pyapi.object_hasattr_string(val, '_opaque')
    dcfmn__sau = c.builder.icmp_unsigned('==', twd__eyf, lir.Constant(
        twd__eyf.type, 0))
    vukvi__whoa = typ.key_type
    bwax__qmrtc = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(vukvi__whoa, bwax__qmrtc)

    def copy_dict(out_dict, in_dict):
        for gipf__sfkqe, xreh__kuud in in_dict.items():
            out_dict[gipf__sfkqe] = xreh__kuud
    with c.builder.if_then(dcfmn__sau):
        daooo__ktat = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        gzhu__stqs = c.pyapi.call_function_objargs(daooo__ktat, [])
        znl__jbgce = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(znl__jbgce, [gzhu__stqs, val])
        c.builder.store(gzhu__stqs, koklp__rfta)
    val = c.builder.load(koklp__rfta)
    ajc__ngtb = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    xwidy__brqkj = c.pyapi.object_type(val)
    ljvm__fwe = c.builder.icmp_unsigned('==', xwidy__brqkj, ajc__ngtb)
    with c.builder.if_else(ljvm__fwe) as (pntw__jvxw, qoj__lgfqn):
        with pntw__jvxw:
            tlb__dghy = c.pyapi.object_getattr_string(val, '_opaque')
            zgxss__gtvd = types.MemInfoPointer(types.voidptr)
            jnh__txe = c.unbox(zgxss__gtvd, tlb__dghy)
            mi = jnh__txe.value
            tuqg__sxm = zgxss__gtvd, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *tuqg__sxm)
            gyshf__spzoy = context.get_constant_null(tuqg__sxm[1])
            args = mi, gyshf__spzoy
            sdftz__hrrok, mmyb__mhyq = c.pyapi.call_jit_code(convert, sig, args
                )
            c.context.nrt.decref(c.builder, typ, mmyb__mhyq)
            c.pyapi.decref(tlb__dghy)
            ntwi__jdhvu = c.builder.basic_block
        with qoj__lgfqn:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", xwidy__brqkj, ajc__ngtb)
            gguv__mmam = c.builder.basic_block
    utcr__lpnvm = c.builder.phi(mmyb__mhyq.type)
    frswd__qwrcv = c.builder.phi(sdftz__hrrok.type)
    utcr__lpnvm.add_incoming(mmyb__mhyq, ntwi__jdhvu)
    utcr__lpnvm.add_incoming(mmyb__mhyq.type(None), gguv__mmam)
    frswd__qwrcv.add_incoming(sdftz__hrrok, ntwi__jdhvu)
    frswd__qwrcv.add_incoming(cgutils.true_bit, gguv__mmam)
    c.pyapi.decref(ajc__ngtb)
    c.pyapi.decref(xwidy__brqkj)
    with c.builder.if_then(dcfmn__sau):
        c.pyapi.decref(val)
    return NativeValue(utcr__lpnvm, is_error=frswd__qwrcv)


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
    sjau__iucl = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=sjau__iucl, name=updatevar)
    jdmz__fnje = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=jdmz__fnje, name=res)


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
        for gipf__sfkqe, xreh__kuud in other.items():
            d[gipf__sfkqe] = xreh__kuud
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
    hzasu__cvzn = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(hzasu__cvzn, res)


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
    hfnm__kcc = PassManager(name)
    if state.func_ir is None:
        hfnm__kcc.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            hfnm__kcc.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        hfnm__kcc.add_pass(FixupArgs, 'fix up args')
    hfnm__kcc.add_pass(IRProcessing, 'processing IR')
    hfnm__kcc.add_pass(WithLifting, 'Handle with contexts')
    hfnm__kcc.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        hfnm__kcc.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        hfnm__kcc.add_pass(DeadBranchPrune, 'dead branch pruning')
        hfnm__kcc.add_pass(GenericRewrites, 'nopython rewrites')
    hfnm__kcc.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    hfnm__kcc.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        hfnm__kcc.add_pass(DeadBranchPrune, 'dead branch pruning')
    hfnm__kcc.add_pass(FindLiterallyCalls, 'find literally calls')
    hfnm__kcc.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        hfnm__kcc.add_pass(ReconstructSSA, 'ssa')
    hfnm__kcc.add_pass(LiteralPropagationSubPipelinePass, 'Literal propagation'
        )
    hfnm__kcc.finalize()
    return hfnm__kcc


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
    a, kenc__vzkma = args
    if isinstance(a, types.List) and isinstance(kenc__vzkma, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(kenc__vzkma, types.List):
        return signature(kenc__vzkma, types.intp, kenc__vzkma)


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
        jieoh__rul, ydoci__iye = 0, 1
    else:
        jieoh__rul, ydoci__iye = 1, 0
    ubjet__qjid = ListInstance(context, builder, sig.args[jieoh__rul], args
        [jieoh__rul])
    uctj__ymttd = ubjet__qjid.size
    tzz__cgtt = args[ydoci__iye]
    ubrzx__upn = lir.Constant(tzz__cgtt.type, 0)
    tzz__cgtt = builder.select(cgutils.is_neg_int(builder, tzz__cgtt),
        ubrzx__upn, tzz__cgtt)
    hprht__tlqc = builder.mul(tzz__cgtt, uctj__ymttd)
    dhco__yfodz = ListInstance.allocate(context, builder, sig.return_type,
        hprht__tlqc)
    dhco__yfodz.size = hprht__tlqc
    with cgutils.for_range_slice(builder, ubrzx__upn, hprht__tlqc,
        uctj__ymttd, inc=True) as (dxdho__qbkvi, _):
        with cgutils.for_range(builder, uctj__ymttd) as anzyk__xiw:
            value = ubjet__qjid.getitem(anzyk__xiw.index)
            dhco__yfodz.setitem(builder.add(anzyk__xiw.index, dxdho__qbkvi),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, dhco__yfodz.
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
    cthhv__wjbq = first.unify(self, second)
    if cthhv__wjbq is not None:
        return cthhv__wjbq
    cthhv__wjbq = second.unify(self, first)
    if cthhv__wjbq is not None:
        return cthhv__wjbq
    vfrh__thfb = self.can_convert(fromty=first, toty=second)
    if vfrh__thfb is not None and vfrh__thfb <= Conversion.safe:
        return second
    vfrh__thfb = self.can_convert(fromty=second, toty=first)
    if vfrh__thfb is not None and vfrh__thfb <= Conversion.safe:
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
    hprht__tlqc = payload.used
    listobj = c.pyapi.list_new(hprht__tlqc)
    tqtlw__maplg = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(tqtlw__maplg, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(
            hprht__tlqc.type, 0))
        with payload._iterate() as anzyk__xiw:
            i = c.builder.load(index)
            item = anzyk__xiw.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return tqtlw__maplg, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    qvjj__whbm = h.type
    xpibn__xfvun = self.mask
    dtype = self._ty.dtype
    rbjao__bka = context.typing_context
    fnty = rbjao__bka.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(rbjao__bka, (dtype, dtype), {})
    bocax__snl = context.get_function(fnty, sig)
    aei__ptl = ir.Constant(qvjj__whbm, 1)
    eptkc__yjfc = ir.Constant(qvjj__whbm, 5)
    vrto__uqzy = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, xpibn__xfvun))
    if for_insert:
        anl__pjd = xpibn__xfvun.type(-1)
        wkh__dckb = cgutils.alloca_once_value(builder, anl__pjd)
    vth__dopkc = builder.append_basic_block('lookup.body')
    vhfd__lvb = builder.append_basic_block('lookup.found')
    qizz__pifi = builder.append_basic_block('lookup.not_found')
    pkfn__ypvnt = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        prnim__vxc = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, prnim__vxc)):
            xwalf__tjp = bocax__snl(builder, (item, entry.key))
            with builder.if_then(xwalf__tjp):
                builder.branch(vhfd__lvb)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, prnim__vxc)):
            builder.branch(qizz__pifi)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, prnim__vxc)):
                ajsh__xmpgx = builder.load(wkh__dckb)
                ajsh__xmpgx = builder.select(builder.icmp_unsigned('==',
                    ajsh__xmpgx, anl__pjd), i, ajsh__xmpgx)
                builder.store(ajsh__xmpgx, wkh__dckb)
    with cgutils.for_range(builder, ir.Constant(qvjj__whbm, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, aei__ptl)
        i = builder.and_(i, xpibn__xfvun)
        builder.store(i, index)
    builder.branch(vth__dopkc)
    with builder.goto_block(vth__dopkc):
        i = builder.load(index)
        check_entry(i)
        qxjya__xwdq = builder.load(vrto__uqzy)
        qxjya__xwdq = builder.lshr(qxjya__xwdq, eptkc__yjfc)
        i = builder.add(aei__ptl, builder.mul(i, eptkc__yjfc))
        i = builder.and_(xpibn__xfvun, builder.add(i, qxjya__xwdq))
        builder.store(i, index)
        builder.store(qxjya__xwdq, vrto__uqzy)
        builder.branch(vth__dopkc)
    with builder.goto_block(qizz__pifi):
        if for_insert:
            i = builder.load(index)
            ajsh__xmpgx = builder.load(wkh__dckb)
            i = builder.select(builder.icmp_unsigned('==', ajsh__xmpgx,
                anl__pjd), i, ajsh__xmpgx)
            builder.store(i, index)
        builder.branch(pkfn__ypvnt)
    with builder.goto_block(vhfd__lvb):
        builder.branch(pkfn__ypvnt)
    builder.position_at_end(pkfn__ypvnt)
    trwn__rfzyp = builder.phi(ir.IntType(1), 'found')
    trwn__rfzyp.add_incoming(cgutils.true_bit, vhfd__lvb)
    trwn__rfzyp.add_incoming(cgutils.false_bit, qizz__pifi)
    return trwn__rfzyp, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    mmnii__rdhwm = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    nsoe__baf = payload.used
    aei__ptl = ir.Constant(nsoe__baf.type, 1)
    nsoe__baf = payload.used = builder.add(nsoe__baf, aei__ptl)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, mmnii__rdhwm), likely=True):
        payload.fill = builder.add(payload.fill, aei__ptl)
    if do_resize:
        self.upsize(nsoe__baf)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    trwn__rfzyp, i = payload._lookup(item, h, for_insert=True)
    qdny__mcv = builder.not_(trwn__rfzyp)
    with builder.if_then(qdny__mcv):
        entry = payload.get_entry(i)
        mmnii__rdhwm = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        nsoe__baf = payload.used
        aei__ptl = ir.Constant(nsoe__baf.type, 1)
        nsoe__baf = payload.used = builder.add(nsoe__baf, aei__ptl)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, mmnii__rdhwm), likely=True):
            payload.fill = builder.add(payload.fill, aei__ptl)
        if do_resize:
            self.upsize(nsoe__baf)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    nsoe__baf = payload.used
    aei__ptl = ir.Constant(nsoe__baf.type, 1)
    nsoe__baf = payload.used = self._builder.sub(nsoe__baf, aei__ptl)
    if do_resize:
        self.downsize(nsoe__baf)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    ist__ircp = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, ist__ircp)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    vtk__zun = payload
    tqtlw__maplg = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(tqtlw__maplg), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with vtk__zun._iterate() as anzyk__xiw:
        entry = anzyk__xiw.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(vtk__zun.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as anzyk__xiw:
        entry = anzyk__xiw.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    tqtlw__maplg = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(tqtlw__maplg), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    tqtlw__maplg = cgutils.alloca_once_value(builder, cgutils.true_bit)
    qvjj__whbm = context.get_value_type(types.intp)
    ubrzx__upn = ir.Constant(qvjj__whbm, 0)
    aei__ptl = ir.Constant(qvjj__whbm, 1)
    mema__ldhzs = context.get_data_type(types.SetPayload(self._ty))
    jdagp__gsksu = context.get_abi_sizeof(mema__ldhzs)
    mlz__xkxr = self._entrysize
    jdagp__gsksu -= mlz__xkxr
    vgs__cfvcq, wvr__grw = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(qvjj__whbm, mlz__xkxr), ir.Constant(qvjj__whbm,
        jdagp__gsksu))
    with builder.if_then(wvr__grw, likely=False):
        builder.store(cgutils.false_bit, tqtlw__maplg)
    with builder.if_then(builder.load(tqtlw__maplg), likely=True):
        if realloc:
            sgg__thzl = self._set.meminfo
            dzix__bic = context.nrt.meminfo_varsize_alloc(builder,
                sgg__thzl, size=vgs__cfvcq)
            ijj__xgy = cgutils.is_null(builder, dzix__bic)
        else:
            wdg__pfc = _imp_dtor(context, builder.module, self._ty)
            sgg__thzl = context.nrt.meminfo_new_varsize_dtor(builder,
                vgs__cfvcq, builder.bitcast(wdg__pfc, cgutils.voidptr_t))
            ijj__xgy = cgutils.is_null(builder, sgg__thzl)
        with builder.if_else(ijj__xgy, likely=False) as (fuipp__yamm, xtg__oot
            ):
            with fuipp__yamm:
                builder.store(cgutils.false_bit, tqtlw__maplg)
            with xtg__oot:
                if not realloc:
                    self._set.meminfo = sgg__thzl
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, vgs__cfvcq, 255)
                payload.used = ubrzx__upn
                payload.fill = ubrzx__upn
                payload.finger = ubrzx__upn
                rjou__zzke = builder.sub(nentries, aei__ptl)
                payload.mask = rjou__zzke
    return builder.load(tqtlw__maplg)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    tqtlw__maplg = cgutils.alloca_once_value(builder, cgutils.true_bit)
    qvjj__whbm = context.get_value_type(types.intp)
    ubrzx__upn = ir.Constant(qvjj__whbm, 0)
    aei__ptl = ir.Constant(qvjj__whbm, 1)
    mema__ldhzs = context.get_data_type(types.SetPayload(self._ty))
    jdagp__gsksu = context.get_abi_sizeof(mema__ldhzs)
    mlz__xkxr = self._entrysize
    jdagp__gsksu -= mlz__xkxr
    xpibn__xfvun = src_payload.mask
    nentries = builder.add(aei__ptl, xpibn__xfvun)
    vgs__cfvcq = builder.add(ir.Constant(qvjj__whbm, jdagp__gsksu), builder
        .mul(ir.Constant(qvjj__whbm, mlz__xkxr), nentries))
    with builder.if_then(builder.load(tqtlw__maplg), likely=True):
        wdg__pfc = _imp_dtor(context, builder.module, self._ty)
        sgg__thzl = context.nrt.meminfo_new_varsize_dtor(builder,
            vgs__cfvcq, builder.bitcast(wdg__pfc, cgutils.voidptr_t))
        ijj__xgy = cgutils.is_null(builder, sgg__thzl)
        with builder.if_else(ijj__xgy, likely=False) as (fuipp__yamm, xtg__oot
            ):
            with fuipp__yamm:
                builder.store(cgutils.false_bit, tqtlw__maplg)
            with xtg__oot:
                self._set.meminfo = sgg__thzl
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = ubrzx__upn
                payload.mask = xpibn__xfvun
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, mlz__xkxr)
                with src_payload._iterate() as anzyk__xiw:
                    context.nrt.incref(builder, self._ty.dtype, anzyk__xiw.
                        entry.key)
    return builder.load(tqtlw__maplg)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    lxlt__zhuz = context.get_value_type(types.voidptr)
    hjzk__jqi = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [lxlt__zhuz, hjzk__jqi, lxlt__zhuz])
    nwa__axhte = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=nwa__axhte)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        hguh__gxrza = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, hguh__gxrza)
        with payload._iterate() as anzyk__xiw:
            entry = anzyk__xiw.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    oxpu__ccps, = sig.args
    ncqwp__hdcbi, = args
    pgp__pns = numba.core.imputils.call_len(context, builder, oxpu__ccps,
        ncqwp__hdcbi)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, pgp__pns)
    with numba.core.imputils.for_iter(context, builder, oxpu__ccps,
        ncqwp__hdcbi) as anzyk__xiw:
        inst.add(anzyk__xiw.value)
        context.nrt.decref(builder, set_type.dtype, anzyk__xiw.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    oxpu__ccps = sig.args[1]
    ncqwp__hdcbi = args[1]
    pgp__pns = numba.core.imputils.call_len(context, builder, oxpu__ccps,
        ncqwp__hdcbi)
    if pgp__pns is not None:
        xxxl__quf = builder.add(inst.payload.used, pgp__pns)
        inst.upsize(xxxl__quf)
    with numba.core.imputils.for_iter(context, builder, oxpu__ccps,
        ncqwp__hdcbi) as anzyk__xiw:
        dptvs__ukl = context.cast(builder, anzyk__xiw.value, oxpu__ccps.
            dtype, inst.dtype)
        inst.add(dptvs__ukl)
        context.nrt.decref(builder, oxpu__ccps.dtype, anzyk__xiw.value)
    if pgp__pns is not None:
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
    dei__mmbr = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, dei__mmbr, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    pbdxd__wgz = target_context.get_executable(library, fndesc, env)
    bpvpt__vzrqw = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=pbdxd__wgz, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return bpvpt__vzrqw


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
