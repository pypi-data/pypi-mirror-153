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
    axnzz__vxdyf = numba.core.bytecode.FunctionIdentity.from_function(func)
    rcdj__euy = numba.core.interpreter.Interpreter(axnzz__vxdyf)
    cuoal__sjam = numba.core.bytecode.ByteCode(func_id=axnzz__vxdyf)
    func_ir = rcdj__euy.interpret(cuoal__sjam)
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
        aavn__egi = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        aavn__egi.run()
    jbx__kfo = numba.core.postproc.PostProcessor(func_ir)
    jbx__kfo.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, sbh__cupzw in visit_vars_extensions.items():
        if isinstance(stmt, t):
            sbh__cupzw(stmt, callback, cbdata)
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
    zgamu__rij = ['ravel', 'transpose', 'reshape']
    for bua__iet in blocks.values():
        for hmw__wfp in bua__iet.body:
            if type(hmw__wfp) in alias_analysis_extensions:
                sbh__cupzw = alias_analysis_extensions[type(hmw__wfp)]
                sbh__cupzw(hmw__wfp, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(hmw__wfp, ir.Assign):
                dizmc__vdt = hmw__wfp.value
                kuar__ynat = hmw__wfp.target.name
                if is_immutable_type(kuar__ynat, typemap):
                    continue
                if isinstance(dizmc__vdt, ir.Var
                    ) and kuar__ynat != dizmc__vdt.name:
                    _add_alias(kuar__ynat, dizmc__vdt.name, alias_map,
                        arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr) and (dizmc__vdt.op ==
                    'cast' or dizmc__vdt.op in ['getitem', 'static_getitem']):
                    _add_alias(kuar__ynat, dizmc__vdt.value.name, alias_map,
                        arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr
                    ) and dizmc__vdt.op == 'inplace_binop':
                    _add_alias(kuar__ynat, dizmc__vdt.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr
                    ) and dizmc__vdt.op == 'getattr' and dizmc__vdt.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(kuar__ynat, dizmc__vdt.value.name, alias_map,
                        arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr
                    ) and dizmc__vdt.op == 'getattr' and dizmc__vdt.attr not in [
                    'shape'] and dizmc__vdt.value.name in arg_aliases:
                    _add_alias(kuar__ynat, dizmc__vdt.value.name, alias_map,
                        arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr
                    ) and dizmc__vdt.op == 'getattr' and dizmc__vdt.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(kuar__ynat, dizmc__vdt.value.name, alias_map,
                        arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr) and dizmc__vdt.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(kuar__ynat, typemap):
                    for jxges__nsf in dizmc__vdt.items:
                        _add_alias(kuar__ynat, jxges__nsf.name, alias_map,
                            arg_aliases)
                if isinstance(dizmc__vdt, ir.Expr) and dizmc__vdt.op == 'call':
                    rttq__qokym = guard(find_callname, func_ir, dizmc__vdt,
                        typemap)
                    if rttq__qokym is None:
                        continue
                    plnb__ofn, xbk__ovra = rttq__qokym
                    if rttq__qokym in alias_func_extensions:
                        pvpov__gpw = alias_func_extensions[rttq__qokym]
                        pvpov__gpw(kuar__ynat, dizmc__vdt.args, alias_map,
                            arg_aliases)
                    if xbk__ovra == 'numpy' and plnb__ofn in zgamu__rij:
                        _add_alias(kuar__ynat, dizmc__vdt.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(xbk__ovra, ir.Var
                        ) and plnb__ofn in zgamu__rij:
                        _add_alias(kuar__ynat, xbk__ovra.name, alias_map,
                            arg_aliases)
    jsi__qshwp = copy.deepcopy(alias_map)
    for jxges__nsf in jsi__qshwp:
        for uosqt__kzm in jsi__qshwp[jxges__nsf]:
            alias_map[jxges__nsf] |= alias_map[uosqt__kzm]
        for uosqt__kzm in jsi__qshwp[jxges__nsf]:
            alias_map[uosqt__kzm] = alias_map[jxges__nsf]
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
    nrk__wki = compute_cfg_from_blocks(func_ir.blocks)
    covk__pmmq = compute_use_defs(func_ir.blocks)
    mvzjx__ofs = compute_live_map(nrk__wki, func_ir.blocks, covk__pmmq.
        usemap, covk__pmmq.defmap)
    zzdzc__xjoy = True
    while zzdzc__xjoy:
        zzdzc__xjoy = False
        for bece__oln, block in func_ir.blocks.items():
            lives = {jxges__nsf.name for jxges__nsf in block.terminator.
                list_vars()}
            for oqo__nuf, nnyw__wqk in nrk__wki.successors(bece__oln):
                lives |= mvzjx__ofs[oqo__nuf]
            sog__rmfq = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    kuar__ynat = stmt.target
                    ylwj__xzpl = stmt.value
                    if kuar__ynat.name not in lives:
                        if isinstance(ylwj__xzpl, ir.Expr
                            ) and ylwj__xzpl.op == 'make_function':
                            continue
                        if isinstance(ylwj__xzpl, ir.Expr
                            ) and ylwj__xzpl.op == 'getattr':
                            continue
                        if isinstance(ylwj__xzpl, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(kuar__ynat,
                            None), types.Function):
                            continue
                        if isinstance(ylwj__xzpl, ir.Expr
                            ) and ylwj__xzpl.op == 'build_map':
                            continue
                        if isinstance(ylwj__xzpl, ir.Expr
                            ) and ylwj__xzpl.op == 'build_tuple':
                            continue
                    if isinstance(ylwj__xzpl, ir.Var
                        ) and kuar__ynat.name == ylwj__xzpl.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    ler__qgux = analysis.ir_extension_usedefs[type(stmt)]
                    puh__oxzj, fmoyv__ulqfo = ler__qgux(stmt)
                    lives -= fmoyv__ulqfo
                    lives |= puh__oxzj
                else:
                    lives |= {jxges__nsf.name for jxges__nsf in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(kuar__ynat.name)
                sog__rmfq.append(stmt)
            sog__rmfq.reverse()
            if len(block.body) != len(sog__rmfq):
                zzdzc__xjoy = True
            block.body = sog__rmfq


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    tvoz__tkm = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (tvoz__tkm,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    wzg__uvo = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), wzg__uvo)


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
            for mwcjn__ywtqh in fnty.templates:
                self._inline_overloads.update(mwcjn__ywtqh._inline_overloads)
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
    wzg__uvo = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), wzg__uvo)
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
    qaf__zji, ezwz__uyzq = self._get_impl(args, kws)
    if qaf__zji is None:
        return
    mjce__acvn = types.Dispatcher(qaf__zji)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        lhrbe__dwvk = qaf__zji._compiler
        flags = compiler.Flags()
        yucoz__qxd = lhrbe__dwvk.targetdescr.typing_context
        hqnw__odrvu = lhrbe__dwvk.targetdescr.target_context
        jidq__shcbv = lhrbe__dwvk.pipeline_class(yucoz__qxd, hqnw__odrvu,
            None, None, None, flags, None)
        pnll__cyvye = InlineWorker(yucoz__qxd, hqnw__odrvu, lhrbe__dwvk.
            locals, jidq__shcbv, flags, None)
        rgwsm__sis = mjce__acvn.dispatcher.get_call_template
        mwcjn__ywtqh, pqfqd__qtxa, hxk__zrbhj, kws = rgwsm__sis(ezwz__uyzq, kws
            )
        if hxk__zrbhj in self._inline_overloads:
            return self._inline_overloads[hxk__zrbhj]['iinfo'].signature
        ir = pnll__cyvye.run_untyped_passes(mjce__acvn.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, hqnw__odrvu, ir, hxk__zrbhj, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, hxk__zrbhj, None)
        self._inline_overloads[sig.args] = {'folded_args': hxk__zrbhj}
        goqa__hlx = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = goqa__hlx
        if not self._inline.is_always_inline:
            sig = mjce__acvn.get_call_type(self.context, ezwz__uyzq, kws)
            self._compiled_overloads[sig.args] = mjce__acvn.get_overload(sig)
        mapr__gei = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': hxk__zrbhj,
            'iinfo': mapr__gei}
    else:
        sig = mjce__acvn.get_call_type(self.context, ezwz__uyzq, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = mjce__acvn.get_overload(sig)
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
    cxe__lrn = [True, False]
    qrjs__alykk = [False, True]
    tppq__scaa = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    wuhoh__fre = get_local_target(context)
    bskj__arjz = utils.order_by_target_specificity(wuhoh__fre, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for slqeu__cyp in bskj__arjz:
        qjvvx__iqgf = slqeu__cyp(context)
        fwvzy__iakck = cxe__lrn if qjvvx__iqgf.prefer_literal else qrjs__alykk
        fwvzy__iakck = [True] if getattr(qjvvx__iqgf, '_no_unliteral', False
            ) else fwvzy__iakck
        for jifcw__pymb in fwvzy__iakck:
            try:
                if jifcw__pymb:
                    sig = qjvvx__iqgf.apply(args, kws)
                else:
                    hxgp__irzvv = tuple([_unlit_non_poison(a) for a in args])
                    rpqc__pssn = {zahc__psx: _unlit_non_poison(jxges__nsf) for
                        zahc__psx, jxges__nsf in kws.items()}
                    sig = qjvvx__iqgf.apply(hxgp__irzvv, rpqc__pssn)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    tppq__scaa.add_error(qjvvx__iqgf, False, e, jifcw__pymb)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = qjvvx__iqgf.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    wot__luz = getattr(qjvvx__iqgf, 'cases', None)
                    if wot__luz is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            wot__luz)
                    else:
                        msg = 'No match.'
                    tppq__scaa.add_error(qjvvx__iqgf, True, msg, jifcw__pymb)
    tppq__scaa.raise_error()


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
    mwcjn__ywtqh = self.template(context)
    cbydf__oqr = None
    zzc__nvriy = None
    uxl__ylkrn = None
    fwvzy__iakck = [True, False] if mwcjn__ywtqh.prefer_literal else [False,
        True]
    fwvzy__iakck = [True] if getattr(mwcjn__ywtqh, '_no_unliteral', False
        ) else fwvzy__iakck
    for jifcw__pymb in fwvzy__iakck:
        if jifcw__pymb:
            try:
                uxl__ylkrn = mwcjn__ywtqh.apply(args, kws)
            except Exception as zjdb__anor:
                if isinstance(zjdb__anor, errors.ForceLiteralArg):
                    raise zjdb__anor
                cbydf__oqr = zjdb__anor
                uxl__ylkrn = None
            else:
                break
        else:
            jogb__aizb = tuple([_unlit_non_poison(a) for a in args])
            kts__agekx = {zahc__psx: _unlit_non_poison(jxges__nsf) for 
                zahc__psx, jxges__nsf in kws.items()}
            csax__pbfxn = jogb__aizb == args and kws == kts__agekx
            if not csax__pbfxn and uxl__ylkrn is None:
                try:
                    uxl__ylkrn = mwcjn__ywtqh.apply(jogb__aizb, kts__agekx)
                except Exception as zjdb__anor:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        zjdb__anor, errors.NumbaError):
                        raise zjdb__anor
                    if isinstance(zjdb__anor, errors.ForceLiteralArg):
                        if mwcjn__ywtqh.prefer_literal:
                            raise zjdb__anor
                    zzc__nvriy = zjdb__anor
                else:
                    break
    if uxl__ylkrn is None and (zzc__nvriy is not None or cbydf__oqr is not None
        ):
        vefg__xgr = '- Resolution failure for {} arguments:\n{}\n'
        hxiz__yukbb = _termcolor.highlight(vefg__xgr)
        if numba.core.config.DEVELOPER_MODE:
            cndrh__htax = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    ylj__csns = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    ylj__csns = ['']
                wnpvq__yctot = '\n{}'.format(2 * cndrh__htax)
                ygw__sywoa = _termcolor.reset(wnpvq__yctot + wnpvq__yctot.
                    join(_bt_as_lines(ylj__csns)))
                return _termcolor.reset(ygw__sywoa)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            hukce__llbh = str(e)
            hukce__llbh = hukce__llbh if hukce__llbh else str(repr(e)
                ) + add_bt(e)
            yrqx__kui = errors.TypingError(textwrap.dedent(hukce__llbh))
            return hxiz__yukbb.format(literalness, str(yrqx__kui))
        import bodo
        if isinstance(cbydf__oqr, bodo.utils.typing.BodoError):
            raise cbydf__oqr
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', cbydf__oqr) +
                nested_msg('non-literal', zzc__nvriy))
        else:
            if 'missing a required argument' in cbydf__oqr.msg:
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
            raise errors.TypingError(msg, loc=cbydf__oqr.loc)
    return uxl__ylkrn


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
    plnb__ofn = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=plnb__ofn)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            ltxj__rclcm = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), ltxj__rclcm)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    ssged__ciert = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            ssged__ciert.append(types.Omitted(a.value))
        else:
            ssged__ciert.append(self.typeof_pyval(a))
    bqxqf__xwrs = None
    try:
        error = None
        bqxqf__xwrs = self.compile(tuple(ssged__ciert))
    except errors.ForceLiteralArg as e:
        fhnwf__hifh = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if fhnwf__hifh:
            vgmn__rvha = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            ohqc__lyutw = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(fhnwf__hifh))
            raise errors.CompilerError(vgmn__rvha.format(ohqc__lyutw))
        ezwz__uyzq = []
        try:
            for i, jxges__nsf in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        ezwz__uyzq.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        ezwz__uyzq.append(types.literal(args[i]))
                else:
                    ezwz__uyzq.append(args[i])
            args = ezwz__uyzq
        except (OSError, FileNotFoundError) as cnk__kcoya:
            error = FileNotFoundError(str(cnk__kcoya) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                bqxqf__xwrs = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        bzbv__pfjh = []
        for i, vtou__win in enumerate(args):
            val = vtou__win.value if isinstance(vtou__win, numba.core.
                dispatcher.OmittedArg) else vtou__win
            try:
                jcnnp__tqkk = typeof(val, Purpose.argument)
            except ValueError as cbgr__ljz:
                bzbv__pfjh.append((i, str(cbgr__ljz)))
            else:
                if jcnnp__tqkk is None:
                    bzbv__pfjh.append((i,
                        f'cannot determine Numba type of value {val}'))
        if bzbv__pfjh:
            qvj__apvmq = '\n'.join(f'- argument {i}: {gdbp__hxorz}' for i,
                gdbp__hxorz in bzbv__pfjh)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{qvj__apvmq}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                vik__dxeo = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                miv__smou = False
                for ifek__llrg in vik__dxeo:
                    if ifek__llrg in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        miv__smou = True
                        break
                if not miv__smou:
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
                ltxj__rclcm = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), ltxj__rclcm)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return bqxqf__xwrs


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
    for bviu__fielh in cres.library._codegen._engine._defined_symbols:
        if bviu__fielh.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in bviu__fielh and (
            'bodo_gb_udf_update_local' in bviu__fielh or 
            'bodo_gb_udf_combine' in bviu__fielh or 'bodo_gb_udf_eval' in
            bviu__fielh or 'bodo_gb_apply_general_udfs' in bviu__fielh):
            gb_agg_cfunc_addr[bviu__fielh
                ] = cres.library.get_pointer_to_function(bviu__fielh)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for bviu__fielh in cres.library._codegen._engine._defined_symbols:
        if bviu__fielh.startswith('cfunc') and ('get_join_cond_addr' not in
            bviu__fielh or 'bodo_join_gen_cond' in bviu__fielh):
            join_gen_cond_cfunc_addr[bviu__fielh
                ] = cres.library.get_pointer_to_function(bviu__fielh)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    qaf__zji = self._get_dispatcher_for_current_target()
    if qaf__zji is not self:
        return qaf__zji.compile(sig)
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
            bjqy__ohnkw = self.overloads.get(tuple(args))
            if bjqy__ohnkw is not None:
                return bjqy__ohnkw.entry_point
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
            bfit__rui = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=bfit__rui):
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
                ste__ivd = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in ste__ivd:
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
    cciv__cxids = self._final_module
    jwig__ayct = []
    nsrv__gxm = 0
    for fn in cciv__cxids.functions:
        nsrv__gxm += 1
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
            jwig__ayct.append(fn.name)
    if nsrv__gxm == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if jwig__ayct:
        cciv__cxids = cciv__cxids.clone()
        for name in jwig__ayct:
            cciv__cxids.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = cciv__cxids
    return cciv__cxids


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
    for vyrq__rso in self.constraints:
        loc = vyrq__rso.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                vyrq__rso(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                kfp__zyluo = numba.core.errors.TypingError(str(e), loc=
                    vyrq__rso.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(kfp__zyluo, e))
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
                    kfp__zyluo = numba.core.errors.TypingError(msg.format(
                        con=vyrq__rso, err=str(e)), loc=vyrq__rso.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(kfp__zyluo, e))
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
    for ftepk__vfu in self._failures.values():
        for nxco__itkx in ftepk__vfu:
            if isinstance(nxco__itkx.error, ForceLiteralArg):
                raise nxco__itkx.error
            if isinstance(nxco__itkx.error, bodo.utils.typing.BodoError):
                raise nxco__itkx.error
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
    selbm__aqu = False
    sog__rmfq = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        bee__qndtn = set()
        mkeg__iid = lives & alias_set
        for jxges__nsf in mkeg__iid:
            bee__qndtn |= alias_map[jxges__nsf]
        lives_n_aliases = lives | bee__qndtn | arg_aliases
        if type(stmt) in remove_dead_extensions:
            sbh__cupzw = remove_dead_extensions[type(stmt)]
            stmt = sbh__cupzw(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                selbm__aqu = True
                continue
        if isinstance(stmt, ir.Assign):
            kuar__ynat = stmt.target
            ylwj__xzpl = stmt.value
            if kuar__ynat.name not in lives and has_no_side_effect(ylwj__xzpl,
                lives_n_aliases, call_table):
                selbm__aqu = True
                continue
            if saved_array_analysis and kuar__ynat.name in lives and is_expr(
                ylwj__xzpl, 'getattr'
                ) and ylwj__xzpl.attr == 'shape' and is_array_typ(typemap[
                ylwj__xzpl.value.name]) and ylwj__xzpl.value.name not in lives:
                lazb__gbl = {jxges__nsf: zahc__psx for zahc__psx,
                    jxges__nsf in func_ir.blocks.items()}
                if block in lazb__gbl:
                    bece__oln = lazb__gbl[block]
                    vjm__muzz = saved_array_analysis.get_equiv_set(bece__oln)
                    kol__hror = vjm__muzz.get_equiv_set(ylwj__xzpl.value)
                    if kol__hror is not None:
                        for jxges__nsf in kol__hror:
                            if jxges__nsf.endswith('#0'):
                                jxges__nsf = jxges__nsf[:-2]
                            if jxges__nsf in typemap and is_array_typ(typemap
                                [jxges__nsf]) and jxges__nsf in lives:
                                ylwj__xzpl.value = ir.Var(ylwj__xzpl.value.
                                    scope, jxges__nsf, ylwj__xzpl.value.loc)
                                selbm__aqu = True
                                break
            if isinstance(ylwj__xzpl, ir.Var
                ) and kuar__ynat.name == ylwj__xzpl.name:
                selbm__aqu = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                selbm__aqu = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            ler__qgux = analysis.ir_extension_usedefs[type(stmt)]
            puh__oxzj, fmoyv__ulqfo = ler__qgux(stmt)
            lives -= fmoyv__ulqfo
            lives |= puh__oxzj
        else:
            lives |= {jxges__nsf.name for jxges__nsf in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                wdvtp__xtgrz = set()
                if isinstance(ylwj__xzpl, ir.Expr):
                    wdvtp__xtgrz = {jxges__nsf.name for jxges__nsf in
                        ylwj__xzpl.list_vars()}
                if kuar__ynat.name not in wdvtp__xtgrz:
                    lives.remove(kuar__ynat.name)
        sog__rmfq.append(stmt)
    sog__rmfq.reverse()
    block.body = sog__rmfq
    return selbm__aqu


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            tsg__ibo, = args
            if isinstance(tsg__ibo, types.IterableType):
                dtype = tsg__ibo.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), tsg__ibo)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    kcloq__serft = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (kcloq__serft, self.dtype)
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
        except LiteralTypingError as skt__sscao:
            return
    try:
        return literal(value)
    except LiteralTypingError as skt__sscao:
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
        zri__uph = py_func.__qualname__
    except AttributeError as skt__sscao:
        zri__uph = py_func.__name__
    xhw__ojrt = inspect.getfile(py_func)
    for cls in self._locator_classes:
        nyx__aah = cls.from_function(py_func, xhw__ojrt)
        if nyx__aah is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (zri__uph, xhw__ojrt))
    self._locator = nyx__aah
    vjt__sizj = inspect.getfile(py_func)
    racqr__uqm = os.path.splitext(os.path.basename(vjt__sizj))[0]
    if xhw__ojrt.startswith('<ipython-'):
        zdk__xip = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)', '\\1\\3',
            racqr__uqm, count=1)
        if zdk__xip == racqr__uqm:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        racqr__uqm = zdk__xip
    nta__wlc = '%s.%s' % (racqr__uqm, zri__uph)
    ftu__bwszv = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(nta__wlc, ftu__bwszv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    jijp__yps = list(filter(lambda a: self._istuple(a.name), args))
    if len(jijp__yps) == 2 and fn.__name__ == 'add':
        vdgc__jrj = self.typemap[jijp__yps[0].name]
        rgbfl__isj = self.typemap[jijp__yps[1].name]
        if vdgc__jrj.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                jijp__yps[1]))
        if rgbfl__isj.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                jijp__yps[0]))
        try:
            txmw__qav = [equiv_set.get_shape(x) for x in jijp__yps]
            if None in txmw__qav:
                return None
            aqgcx__xezw = sum(txmw__qav, ())
            return ArrayAnalysis.AnalyzeResult(shape=aqgcx__xezw)
        except GuardException as skt__sscao:
            return None
    fozc__ymp = list(filter(lambda a: self._isarray(a.name), args))
    require(len(fozc__ymp) > 0)
    jipry__iivk = [x.name for x in fozc__ymp]
    nkit__jru = [self.typemap[x.name].ndim for x in fozc__ymp]
    mjop__vjk = max(nkit__jru)
    require(mjop__vjk > 0)
    txmw__qav = [equiv_set.get_shape(x) for x in fozc__ymp]
    if any(a is None for a in txmw__qav):
        return ArrayAnalysis.AnalyzeResult(shape=fozc__ymp[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, fozc__ymp))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, txmw__qav,
        jipry__iivk)


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
    gxkp__oxv = code_obj.code
    zuhr__aov = len(gxkp__oxv.co_freevars)
    wtofy__vaxb = gxkp__oxv.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        mhui__clom, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        wtofy__vaxb = [jxges__nsf.name for jxges__nsf in mhui__clom]
    wldiu__mym = caller_ir.func_id.func.__globals__
    try:
        wldiu__mym = getattr(code_obj, 'globals', wldiu__mym)
    except KeyError as skt__sscao:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    ghv__jqfon = []
    for x in wtofy__vaxb:
        try:
            nyfyl__mqh = caller_ir.get_definition(x)
        except KeyError as skt__sscao:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(nyfyl__mqh, (ir.Const, ir.Global, ir.FreeVar)):
            val = nyfyl__mqh.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                tvoz__tkm = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                wldiu__mym[tvoz__tkm] = bodo.jit(distributed=False)(val)
                wldiu__mym[tvoz__tkm].is_nested_func = True
                val = tvoz__tkm
            if isinstance(val, CPUDispatcher):
                tvoz__tkm = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                wldiu__mym[tvoz__tkm] = val
                val = tvoz__tkm
            ghv__jqfon.append(val)
        elif isinstance(nyfyl__mqh, ir.Expr
            ) and nyfyl__mqh.op == 'make_function':
            oxam__bdm = convert_code_obj_to_function(nyfyl__mqh, caller_ir)
            tvoz__tkm = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            wldiu__mym[tvoz__tkm] = bodo.jit(distributed=False)(oxam__bdm)
            wldiu__mym[tvoz__tkm].is_nested_func = True
            ghv__jqfon.append(tvoz__tkm)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    rbzda__jlti = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate
        (ghv__jqfon)])
    hpqu__dvcvb = ','.join([('c_%d' % i) for i in range(zuhr__aov)])
    ydlym__kwyfc = list(gxkp__oxv.co_varnames)
    osja__qgqw = 0
    zrpl__uxhu = gxkp__oxv.co_argcount
    yjd__fdq = caller_ir.get_definition(code_obj.defaults)
    if yjd__fdq is not None:
        if isinstance(yjd__fdq, tuple):
            d = [caller_ir.get_definition(x).value for x in yjd__fdq]
            vgdx__mtn = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in yjd__fdq.items]
            vgdx__mtn = tuple(d)
        osja__qgqw = len(vgdx__mtn)
    eurz__plpnr = zrpl__uxhu - osja__qgqw
    ovl__vtf = ','.join([('%s' % ydlym__kwyfc[i]) for i in range(eurz__plpnr)])
    if osja__qgqw:
        lpgmu__fdvtc = [('%s = %s' % (ydlym__kwyfc[i + eurz__plpnr],
            vgdx__mtn[i])) for i in range(osja__qgqw)]
        ovl__vtf += ', '
        ovl__vtf += ', '.join(lpgmu__fdvtc)
    return _create_function_from_code_obj(gxkp__oxv, rbzda__jlti, ovl__vtf,
        hpqu__dvcvb, wldiu__mym)


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
    for npraj__jwpkm, (cdppq__iduv, ors__ausdx) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % ors__ausdx)
            acjhe__opaxu = _pass_registry.get(cdppq__iduv).pass_inst
            if isinstance(acjhe__opaxu, CompilerPass):
                self._runPass(npraj__jwpkm, acjhe__opaxu, state)
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
                    pipeline_name, ors__ausdx)
                zyyf__nfifq = self._patch_error(msg, e)
                raise zyyf__nfifq
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
    pfk__oiu = None
    fmoyv__ulqfo = {}

    def lookup(var, already_seen, varonly=True):
        val = fmoyv__ulqfo.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    llij__obris = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        kuar__ynat = stmt.target
        ylwj__xzpl = stmt.value
        fmoyv__ulqfo[kuar__ynat.name] = ylwj__xzpl
        if isinstance(ylwj__xzpl, ir.Var) and ylwj__xzpl.name in fmoyv__ulqfo:
            ylwj__xzpl = lookup(ylwj__xzpl, set())
        if isinstance(ylwj__xzpl, ir.Expr):
            fzrc__sdlvn = set(lookup(jxges__nsf, set(), True).name for
                jxges__nsf in ylwj__xzpl.list_vars())
            if name in fzrc__sdlvn:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ylwj__xzpl)]
                ntd__mfz = [x for x, hrlpg__qfxp in args if hrlpg__qfxp.
                    name != name]
                args = [(x, hrlpg__qfxp) for x, hrlpg__qfxp in args if x !=
                    hrlpg__qfxp.name]
                yavqs__kjqfl = dict(args)
                if len(ntd__mfz) == 1:
                    yavqs__kjqfl[ntd__mfz[0]] = ir.Var(kuar__ynat.scope, 
                        name + '#init', kuar__ynat.loc)
                replace_vars_inner(ylwj__xzpl, yavqs__kjqfl)
                pfk__oiu = nodes[i:]
                break
    return pfk__oiu


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
        weix__ffxfw = expand_aliases({jxges__nsf.name for jxges__nsf in
            stmt.list_vars()}, alias_map, arg_aliases)
        phwhd__cvq = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        rti__klry = expand_aliases({jxges__nsf.name for jxges__nsf in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        qjo__stg = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(phwhd__cvq & rti__klry | qjo__stg & weix__ffxfw) == 0:
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
    tgb__jxhy = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            tgb__jxhy.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                tgb__jxhy.update(get_parfor_writes(stmt, func_ir))
    return tgb__jxhy


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    tgb__jxhy = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        tgb__jxhy.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        tgb__jxhy = {jxges__nsf.name for jxges__nsf in stmt.df_out_vars.
            values()}
        if stmt.out_key_vars is not None:
            tgb__jxhy.update({jxges__nsf.name for jxges__nsf in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        tgb__jxhy = {jxges__nsf.name for jxges__nsf in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        tgb__jxhy = {jxges__nsf.name for jxges__nsf in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            tgb__jxhy.update({jxges__nsf.name for jxges__nsf in stmt.
                out_key_arrs})
            tgb__jxhy.update({jxges__nsf.name for jxges__nsf in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        rttq__qokym = guard(find_callname, func_ir, stmt.value)
        if rttq__qokym in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            tgb__jxhy.add(stmt.value.args[0].name)
        if rttq__qokym == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            tgb__jxhy.add(stmt.value.args[1].name)
    return tgb__jxhy


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
        sbh__cupzw = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        lnxfc__fkbmo = sbh__cupzw.format(self, msg)
        self.args = lnxfc__fkbmo,
    else:
        sbh__cupzw = _termcolor.errmsg('{0}')
        lnxfc__fkbmo = sbh__cupzw.format(self)
        self.args = lnxfc__fkbmo,
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
        for vcs__izu in options['distributed']:
            dist_spec[vcs__izu] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for vcs__izu in options['distributed_block']:
            dist_spec[vcs__izu] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    csjys__dqmsc = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, tcspu__oax in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(tcspu__oax)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    ottyb__srhch = {}
    for jzd__vbe in reversed(inspect.getmro(cls)):
        ottyb__srhch.update(jzd__vbe.__dict__)
    ztnta__jqf, fmvxa__eeraj, duw__lneq, bcqw__dmhaa = {}, {}, {}, {}
    for zahc__psx, jxges__nsf in ottyb__srhch.items():
        if isinstance(jxges__nsf, pytypes.FunctionType):
            ztnta__jqf[zahc__psx] = jxges__nsf
        elif isinstance(jxges__nsf, property):
            fmvxa__eeraj[zahc__psx] = jxges__nsf
        elif isinstance(jxges__nsf, staticmethod):
            duw__lneq[zahc__psx] = jxges__nsf
        else:
            bcqw__dmhaa[zahc__psx] = jxges__nsf
    ugl__dpjep = (set(ztnta__jqf) | set(fmvxa__eeraj) | set(duw__lneq)) & set(
        spec)
    if ugl__dpjep:
        raise NameError('name shadowing: {0}'.format(', '.join(ugl__dpjep)))
    bqv__gpozz = bcqw__dmhaa.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(bcqw__dmhaa)
    if bcqw__dmhaa:
        msg = 'class members are not yet supported: {0}'
        yusxg__xbmcx = ', '.join(bcqw__dmhaa.keys())
        raise TypeError(msg.format(yusxg__xbmcx))
    for zahc__psx, jxges__nsf in fmvxa__eeraj.items():
        if jxges__nsf.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(zahc__psx))
    jit_methods = {zahc__psx: bodo.jit(returns_maybe_distributed=
        csjys__dqmsc)(jxges__nsf) for zahc__psx, jxges__nsf in ztnta__jqf.
        items()}
    jit_props = {}
    for zahc__psx, jxges__nsf in fmvxa__eeraj.items():
        wzg__uvo = {}
        if jxges__nsf.fget:
            wzg__uvo['get'] = bodo.jit(jxges__nsf.fget)
        if jxges__nsf.fset:
            wzg__uvo['set'] = bodo.jit(jxges__nsf.fset)
        jit_props[zahc__psx] = wzg__uvo
    jit_static_methods = {zahc__psx: bodo.jit(jxges__nsf.__func__) for 
        zahc__psx, jxges__nsf in duw__lneq.items()}
    tomjp__epwn = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    nzjm__fthnv = dict(class_type=tomjp__epwn, __doc__=bqv__gpozz)
    nzjm__fthnv.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), nzjm__fthnv)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, tomjp__epwn)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(tomjp__epwn, typingctx, targetctx).register()
    as_numba_type.register(cls, tomjp__epwn.instance_type)
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
    hzfzm__tqt = ','.join('{0}:{1}'.format(zahc__psx, jxges__nsf) for 
        zahc__psx, jxges__nsf in struct.items())
    lkrvn__sue = ','.join('{0}:{1}'.format(zahc__psx, jxges__nsf) for 
        zahc__psx, jxges__nsf in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), hzfzm__tqt, lkrvn__sue)
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
    lkddt__hsx = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if lkddt__hsx is None:
        return
    amh__eplp, tvln__fjhp = lkddt__hsx
    for a in itertools.chain(amh__eplp, tvln__fjhp.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, amh__eplp, tvln__fjhp)
    except ForceLiteralArg as e:
        precw__tka = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(precw__tka, self.kws)
        tzda__ots = set()
        uvcw__cont = set()
        xiro__fgnpa = {}
        for npraj__jwpkm in e.requested_args:
            xms__xgy = typeinfer.func_ir.get_definition(folded[npraj__jwpkm])
            if isinstance(xms__xgy, ir.Arg):
                tzda__ots.add(xms__xgy.index)
                if xms__xgy.index in e.file_infos:
                    xiro__fgnpa[xms__xgy.index] = e.file_infos[xms__xgy.index]
            else:
                uvcw__cont.add(npraj__jwpkm)
        if uvcw__cont:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif tzda__ots:
            raise ForceLiteralArg(tzda__ots, loc=self.loc, file_infos=
                xiro__fgnpa)
    if sig is None:
        pabln__eyouh = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in amh__eplp]
        args += [('%s=%s' % (zahc__psx, jxges__nsf)) for zahc__psx,
            jxges__nsf in sorted(tvln__fjhp.items())]
        kaoay__mtw = pabln__eyouh.format(fnty, ', '.join(map(str, args)))
        clzlj__gbi = context.explain_function_type(fnty)
        msg = '\n'.join([kaoay__mtw, clzlj__gbi])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        vlbao__vzp = context.unify_pairs(sig.recvr, fnty.this)
        if vlbao__vzp is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if vlbao__vzp is not None and vlbao__vzp.is_precise():
            ywsy__rgqk = fnty.copy(this=vlbao__vzp)
            typeinfer.propagate_refined_type(self.func, ywsy__rgqk)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            neo__qckpc = target.getone()
            if context.unify_pairs(neo__qckpc, sig.return_type) == neo__qckpc:
                sig = sig.replace(return_type=neo__qckpc)
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
        vgmn__rvha = '*other* must be a {} but got a {} instead'
        raise TypeError(vgmn__rvha.format(ForceLiteralArg, type(other)))
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
    rlpe__lmov = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for zahc__psx, jxges__nsf in kwargs.items():
        gke__siasq = None
        try:
            fiw__pssy = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var(
                'dummy'), loc)
            func_ir._definitions[fiw__pssy.name] = [jxges__nsf]
            gke__siasq = get_const_value_inner(func_ir, fiw__pssy)
            func_ir._definitions.pop(fiw__pssy.name)
            if isinstance(gke__siasq, str):
                gke__siasq = sigutils._parse_signature_string(gke__siasq)
            if isinstance(gke__siasq, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {zahc__psx} is annotated as type class {gke__siasq}."""
                    )
            assert isinstance(gke__siasq, types.Type)
            if isinstance(gke__siasq, (types.List, types.Set)):
                gke__siasq = gke__siasq.copy(reflected=False)
            rlpe__lmov[zahc__psx] = gke__siasq
        except BodoError as skt__sscao:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(gke__siasq, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(jxges__nsf, ir.Global):
                    msg = f'Global {jxges__nsf.name!r} is not defined.'
                if isinstance(jxges__nsf, ir.FreeVar):
                    msg = f'Freevar {jxges__nsf.name!r} is not defined.'
            if isinstance(jxges__nsf, ir.Expr) and jxges__nsf.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=zahc__psx, msg=msg, loc=loc)
    for name, typ in rlpe__lmov.items():
        self._legalize_arg_type(name, typ, loc)
    return rlpe__lmov


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
    jcex__zuyom = inst.arg
    assert jcex__zuyom > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(jcex__zuyom)]))
    tmps = [state.make_temp() for _ in range(jcex__zuyom - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    imedq__fvnnt = ir.Global('format', format, loc=self.loc)
    self.store(value=imedq__fvnnt, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    ocjaj__gptfb = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=ocjaj__gptfb, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    jcex__zuyom = inst.arg
    assert jcex__zuyom > 0, 'invalid BUILD_STRING count'
    lypkk__grizs = self.get(strings[0])
    for other, spne__jwjp in zip(strings[1:], tmps):
        other = self.get(other)
        dizmc__vdt = ir.Expr.binop(operator.add, lhs=lypkk__grizs, rhs=
            other, loc=self.loc)
        self.store(dizmc__vdt, spne__jwjp)
        lypkk__grizs = self.get(spne__jwjp)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    jtaz__kmtog = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, jtaz__kmtog])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    mioqi__djlg = mk_unique_var(f'{var_name}')
    nigi__prh = mioqi__djlg.replace('<', '_').replace('>', '_')
    nigi__prh = nigi__prh.replace('.', '_').replace('$', '_v')
    return nigi__prh


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
                ctc__cjyzm = get_overload_const_str(val2)
                if ctc__cjyzm != 'ns':
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
        moh__oyf = states['defmap']
        if len(moh__oyf) == 0:
            vhwm__zuyu = assign.target
            numba.core.ssa._logger.debug('first assign: %s', vhwm__zuyu)
            if vhwm__zuyu.name not in scope.localvars:
                vhwm__zuyu = scope.define(assign.target.name, loc=assign.loc)
        else:
            vhwm__zuyu = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=vhwm__zuyu, value=assign.value, loc=
            assign.loc)
        moh__oyf[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    czr__qegdu = []
    for zahc__psx, jxges__nsf in typing.npydecl.registry.globals:
        if zahc__psx == func:
            czr__qegdu.append(jxges__nsf)
    for zahc__psx, jxges__nsf in typing.templates.builtin_registry.globals:
        if zahc__psx == func:
            czr__qegdu.append(jxges__nsf)
    if len(czr__qegdu) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return czr__qegdu


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    bthhg__mds = {}
    uan__vwk = find_topo_order(blocks)
    omhj__llyrx = {}
    for bece__oln in uan__vwk:
        block = blocks[bece__oln]
        sog__rmfq = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                kuar__ynat = stmt.target.name
                ylwj__xzpl = stmt.value
                if (ylwj__xzpl.op == 'getattr' and ylwj__xzpl.attr in
                    arr_math and isinstance(typemap[ylwj__xzpl.value.name],
                    types.npytypes.Array)):
                    ylwj__xzpl = stmt.value
                    char__sipoi = ylwj__xzpl.value
                    bthhg__mds[kuar__ynat] = char__sipoi
                    scope = char__sipoi.scope
                    loc = char__sipoi.loc
                    pkbt__sjbl = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[pkbt__sjbl.name] = types.misc.Module(numpy)
                    upj__dme = ir.Global('np', numpy, loc)
                    kzkr__kmq = ir.Assign(upj__dme, pkbt__sjbl, loc)
                    ylwj__xzpl.value = pkbt__sjbl
                    sog__rmfq.append(kzkr__kmq)
                    func_ir._definitions[pkbt__sjbl.name] = [upj__dme]
                    func = getattr(numpy, ylwj__xzpl.attr)
                    jaa__dcdsy = get_np_ufunc_typ_lst(func)
                    omhj__llyrx[kuar__ynat] = jaa__dcdsy
                if (ylwj__xzpl.op == 'call' and ylwj__xzpl.func.name in
                    bthhg__mds):
                    char__sipoi = bthhg__mds[ylwj__xzpl.func.name]
                    hoe__leut = calltypes.pop(ylwj__xzpl)
                    jog__ggi = hoe__leut.args[:len(ylwj__xzpl.args)]
                    zqvr__xkr = {name: typemap[jxges__nsf.name] for name,
                        jxges__nsf in ylwj__xzpl.kws}
                    pzm__lfi = omhj__llyrx[ylwj__xzpl.func.name]
                    ipd__sogz = None
                    for snp__dfjjj in pzm__lfi:
                        try:
                            ipd__sogz = snp__dfjjj.get_call_type(typingctx,
                                [typemap[char__sipoi.name]] + list(jog__ggi
                                ), zqvr__xkr)
                            typemap.pop(ylwj__xzpl.func.name)
                            typemap[ylwj__xzpl.func.name] = snp__dfjjj
                            calltypes[ylwj__xzpl] = ipd__sogz
                            break
                        except Exception as skt__sscao:
                            pass
                    if ipd__sogz is None:
                        raise TypeError(
                            f'No valid template found for {ylwj__xzpl.func.name}'
                            )
                    ylwj__xzpl.args = [char__sipoi] + ylwj__xzpl.args
            sog__rmfq.append(stmt)
        block.body = sog__rmfq


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    isfi__swk = ufunc.nin
    wwns__tupts = ufunc.nout
    eurz__plpnr = ufunc.nargs
    assert eurz__plpnr == isfi__swk + wwns__tupts
    if len(args) < isfi__swk:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), isfi__swk))
    if len(args) > eurz__plpnr:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            eurz__plpnr))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    oarn__szx = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    jni__hxngh = max(oarn__szx)
    mnpr__iabxo = args[isfi__swk:]
    if not all(d == jni__hxngh for d in oarn__szx[isfi__swk:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(kens__bgme, types.ArrayCompatible) and not
        isinstance(kens__bgme, types.Bytes) for kens__bgme in mnpr__iabxo):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(kens__bgme.mutable for kens__bgme in mnpr__iabxo):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    idyxi__tgzqn = [(x.dtype if isinstance(x, types.ArrayCompatible) and 
        not isinstance(x, types.Bytes) else x) for x in args]
    wsrrz__flj = None
    if jni__hxngh > 0 and len(mnpr__iabxo) < ufunc.nout:
        wsrrz__flj = 'C'
        apmwq__sxwwx = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in apmwq__sxwwx and 'F' in apmwq__sxwwx:
            wsrrz__flj = 'F'
    return idyxi__tgzqn, mnpr__iabxo, jni__hxngh, wsrrz__flj


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
        ljwqh__twtq = 'Dict.key_type cannot be of type {}'
        raise TypingError(ljwqh__twtq.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        ljwqh__twtq = 'Dict.value_type cannot be of type {}'
        raise TypingError(ljwqh__twtq.format(valty))
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
    qeus__zkmm = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[qeus__zkmm]
        return impl, args
    except KeyError as skt__sscao:
        pass
    impl, args = self._build_impl(qeus__zkmm, args, kws)
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
        uwf__ebbid = find_topo_order(parfor.loop_body)
    mlia__qwi = uwf__ebbid[0]
    gez__poimc = {}
    _update_parfor_get_setitems(parfor.loop_body[mlia__qwi].body, parfor.
        index_var, alias_map, gez__poimc, lives_n_aliases)
    wop__xcccv = set(gez__poimc.keys())
    for slivp__iodqp in uwf__ebbid:
        if slivp__iodqp == mlia__qwi:
            continue
        for stmt in parfor.loop_body[slivp__iodqp].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            lqgj__xxvfl = set(jxges__nsf.name for jxges__nsf in stmt.
                list_vars())
            psito__rgy = lqgj__xxvfl & wop__xcccv
            for a in psito__rgy:
                gez__poimc.pop(a, None)
    for slivp__iodqp in uwf__ebbid:
        if slivp__iodqp == mlia__qwi:
            continue
        block = parfor.loop_body[slivp__iodqp]
        pui__hjgr = gez__poimc.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            pui__hjgr, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    ktqqv__fccq = max(blocks.keys())
    kxed__sntg, vaw__fzus = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    wjgcp__uwbc = ir.Jump(kxed__sntg, ir.Loc('parfors_dummy', -1))
    blocks[ktqqv__fccq].body.append(wjgcp__uwbc)
    nrk__wki = compute_cfg_from_blocks(blocks)
    covk__pmmq = compute_use_defs(blocks)
    mvzjx__ofs = compute_live_map(nrk__wki, blocks, covk__pmmq.usemap,
        covk__pmmq.defmap)
    alias_set = set(alias_map.keys())
    for bece__oln, block in blocks.items():
        sog__rmfq = []
        oavlg__kbhp = {jxges__nsf.name for jxges__nsf in block.terminator.
            list_vars()}
        for oqo__nuf, nnyw__wqk in nrk__wki.successors(bece__oln):
            oavlg__kbhp |= mvzjx__ofs[oqo__nuf]
        for stmt in reversed(block.body):
            bee__qndtn = oavlg__kbhp & alias_set
            for jxges__nsf in bee__qndtn:
                oavlg__kbhp |= alias_map[jxges__nsf]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in oavlg__kbhp and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                rttq__qokym = guard(find_callname, func_ir, stmt.value)
                if rttq__qokym == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in oavlg__kbhp and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            oavlg__kbhp |= {jxges__nsf.name for jxges__nsf in stmt.list_vars()}
            sog__rmfq.append(stmt)
        sog__rmfq.reverse()
        block.body = sog__rmfq
    typemap.pop(vaw__fzus.name)
    blocks[ktqqv__fccq].body.pop()

    def trim_empty_parfor_branches(parfor):
        zzdzc__xjoy = False
        blocks = parfor.loop_body.copy()
        for bece__oln, block in blocks.items():
            if len(block.body):
                txvza__eldbe = block.body[-1]
                if isinstance(txvza__eldbe, ir.Branch):
                    if len(blocks[txvza__eldbe.truebr].body) == 1 and len(
                        blocks[txvza__eldbe.falsebr].body) == 1:
                        qhx__ftf = blocks[txvza__eldbe.truebr].body[0]
                        qxok__rjxt = blocks[txvza__eldbe.falsebr].body[0]
                        if isinstance(qhx__ftf, ir.Jump) and isinstance(
                            qxok__rjxt, ir.Jump
                            ) and qhx__ftf.target == qxok__rjxt.target:
                            parfor.loop_body[bece__oln].body[-1] = ir.Jump(
                                qhx__ftf.target, txvza__eldbe.loc)
                            zzdzc__xjoy = True
                    elif len(blocks[txvza__eldbe.truebr].body) == 1:
                        qhx__ftf = blocks[txvza__eldbe.truebr].body[0]
                        if isinstance(qhx__ftf, ir.Jump
                            ) and qhx__ftf.target == txvza__eldbe.falsebr:
                            parfor.loop_body[bece__oln].body[-1] = ir.Jump(
                                qhx__ftf.target, txvza__eldbe.loc)
                            zzdzc__xjoy = True
                    elif len(blocks[txvza__eldbe.falsebr].body) == 1:
                        qxok__rjxt = blocks[txvza__eldbe.falsebr].body[0]
                        if isinstance(qxok__rjxt, ir.Jump
                            ) and qxok__rjxt.target == txvza__eldbe.truebr:
                            parfor.loop_body[bece__oln].body[-1] = ir.Jump(
                                qxok__rjxt.target, txvza__eldbe.loc)
                            zzdzc__xjoy = True
        return zzdzc__xjoy
    zzdzc__xjoy = True
    while zzdzc__xjoy:
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
        zzdzc__xjoy = trim_empty_parfor_branches(parfor)
    hjn__hbu = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        hjn__hbu &= len(block.body) == 0
    if hjn__hbu:
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
    rvsm__otp = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                rvsm__otp += 1
                parfor = stmt
                ohq__yiq = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = ohq__yiq.scope
                loc = ir.Loc('parfors_dummy', -1)
                hdy__munz = ir.Var(scope, mk_unique_var('$const'), loc)
                ohq__yiq.body.append(ir.Assign(ir.Const(0, loc), hdy__munz,
                    loc))
                ohq__yiq.body.append(ir.Return(hdy__munz, loc))
                nrk__wki = compute_cfg_from_blocks(parfor.loop_body)
                for yaaf__byc in nrk__wki.dead_nodes():
                    del parfor.loop_body[yaaf__byc]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                ohq__yiq = parfor.loop_body[max(parfor.loop_body.keys())]
                ohq__yiq.body.pop()
                ohq__yiq.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return rvsm__otp


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
            bjqy__ohnkw = self.overloads.get(tuple(args))
            if bjqy__ohnkw is not None:
                return bjqy__ohnkw.entry_point
            self._pre_compile(args, return_type, flags)
            plbxv__sud = self.func_ir
            bfit__rui = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=bfit__rui):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=plbxv__sud, args=args,
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
        ymp__tcq = copy.deepcopy(flags)
        ymp__tcq.no_rewrites = True

        def compile_local(the_ir, the_flags):
            hcvxi__gvuw = pipeline_class(typingctx, targetctx, library,
                args, return_type, the_flags, locals)
            return hcvxi__gvuw.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        kzps__inq = compile_local(func_ir, ymp__tcq)
        ibqoj__vvrv = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    ibqoj__vvrv = compile_local(func_ir, flags)
                except Exception as skt__sscao:
                    pass
        if ibqoj__vvrv is not None:
            cres = ibqoj__vvrv
        else:
            cres = kzps__inq
        return cres
    else:
        hcvxi__gvuw = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return hcvxi__gvuw.compile_ir(func_ir=func_ir, lifted=lifted,
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
    alpe__hyadk = self.get_data_type(typ.dtype)
    exnga__oedi = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        exnga__oedi):
        qfea__snjtu = ary.ctypes.data
        wnmnh__abnua = self.add_dynamic_addr(builder, qfea__snjtu, info=str
            (type(qfea__snjtu)))
        kawb__pzyhu = self.add_dynamic_addr(builder, id(ary), info=str(type
            (ary)))
        self.global_arrays.append(ary)
    else:
        agprk__dtf = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            agprk__dtf = agprk__dtf.view('int64')
        val = bytearray(agprk__dtf.data)
        dvy__vgdo = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        wnmnh__abnua = cgutils.global_constant(builder, '.const.array.data',
            dvy__vgdo)
        wnmnh__abnua.align = self.get_abi_alignment(alpe__hyadk)
        kawb__pzyhu = None
    jqjt__valji = self.get_value_type(types.intp)
    tfd__fbz = [self.get_constant(types.intp, zrqgd__dhdir) for
        zrqgd__dhdir in ary.shape]
    shlsb__dcw = lir.Constant(lir.ArrayType(jqjt__valji, len(tfd__fbz)),
        tfd__fbz)
    wlpb__enhew = [self.get_constant(types.intp, zrqgd__dhdir) for
        zrqgd__dhdir in ary.strides]
    bvtkw__lug = lir.Constant(lir.ArrayType(jqjt__valji, len(wlpb__enhew)),
        wlpb__enhew)
    dgifk__veja = self.get_constant(types.intp, ary.dtype.itemsize)
    vmh__fkwhi = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        vmh__fkwhi, dgifk__veja, wnmnh__abnua.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), shlsb__dcw, bvtkw__lug])


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
    pkytj__xqmp = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    wysgx__alrlv = lir.Function(module, pkytj__xqmp, name='nrt_atomic_{0}'.
        format(op))
    [sbtkd__sxtxx] = wysgx__alrlv.args
    tti__ulsk = wysgx__alrlv.append_basic_block()
    builder = lir.IRBuilder(tti__ulsk)
    ras__wirgu = lir.Constant(_word_type, 1)
    if False:
        wrfq__tkpyf = builder.atomic_rmw(op, sbtkd__sxtxx, ras__wirgu,
            ordering=ordering)
        res = getattr(builder, op)(wrfq__tkpyf, ras__wirgu)
        builder.ret(res)
    else:
        wrfq__tkpyf = builder.load(sbtkd__sxtxx)
        ptu__wqmnt = getattr(builder, op)(wrfq__tkpyf, ras__wirgu)
        jqb__tqwka = builder.icmp_signed('!=', wrfq__tkpyf, lir.Constant(
            wrfq__tkpyf.type, -1))
        with cgutils.if_likely(builder, jqb__tqwka):
            builder.store(ptu__wqmnt, sbtkd__sxtxx)
        builder.ret(ptu__wqmnt)
    return wysgx__alrlv


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
        cyjs__bdtyt = state.targetctx.codegen()
        state.library = cyjs__bdtyt.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    rcdj__euy = state.func_ir
    typemap = state.typemap
    tqaac__gqt = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    bmtcj__npxvb = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            rcdj__euy, typemap, tqaac__gqt, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            nnii__vfem = lowering.Lower(targetctx, library, fndesc,
                rcdj__euy, metadata=metadata)
            nnii__vfem.lower()
            if not flags.no_cpython_wrapper:
                nnii__vfem.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(tqaac__gqt, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        nnii__vfem.create_cfunc_wrapper()
            env = nnii__vfem.env
            nmtv__bkpgx = nnii__vfem.call_helper
            del nnii__vfem
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, nmtv__bkpgx, cfunc=None, env=env
                )
        else:
            wiuwa__iutsk = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(wiuwa__iutsk, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, nmtv__bkpgx, cfunc=
                wiuwa__iutsk, env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        dsi__unu = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = dsi__unu - bmtcj__npxvb
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
        mowa__zus = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, mowa__zus),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            ispol__awed.do_break()
        miv__rta = c.builder.icmp_signed('!=', mowa__zus, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(miv__rta, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, mowa__zus)
                c.pyapi.decref(mowa__zus)
                ispol__awed.do_break()
        c.pyapi.decref(mowa__zus)
    wpe__gat, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(wpe__gat, likely=True) as (xvo__ujzlc, vsfl__iptu):
        with xvo__ujzlc:
            list.size = size
            kav__qoa = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                kav__qoa), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        kav__qoa))
                    with cgutils.for_range(c.builder, size) as ispol__awed:
                        itemobj = c.pyapi.list_getitem(obj, ispol__awed.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        jjl__znbr = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(jjl__znbr.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            ispol__awed.do_break()
                        list.setitem(ispol__awed.index, jjl__znbr.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with vsfl__iptu:
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
    mmo__fbjdz, iioat__qqg, qmp__qanl, yncye__ktd, bqgcs__xdoz = (
        compile_time_get_string_data(literal_string))
    cciv__cxids = builder.module
    gv = context.insert_const_bytes(cciv__cxids, mmo__fbjdz)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        iioat__qqg), context.get_constant(types.int32, qmp__qanl), context.
        get_constant(types.uint32, yncye__ktd), context.get_constant(
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
    cqph__lxo = None
    if isinstance(shape, types.Integer):
        cqph__lxo = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(zrqgd__dhdir, (types.Integer, types.IntEnumMember
            )) for zrqgd__dhdir in shape):
            cqph__lxo = len(shape)
    return cqph__lxo


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
            cqph__lxo = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if cqph__lxo == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(cqph__lxo))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            jipry__iivk = self._get_names(x)
            if len(jipry__iivk) != 0:
                return jipry__iivk[0]
            return jipry__iivk
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    jipry__iivk = self._get_names(obj)
    if len(jipry__iivk) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(jipry__iivk[0])


def get_equiv_set(self, obj):
    jipry__iivk = self._get_names(obj)
    if len(jipry__iivk) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(jipry__iivk[0])


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
    ndnb__diqwx = []
    for wywm__czjct in func_ir.arg_names:
        if wywm__czjct in typemap and isinstance(typemap[wywm__czjct],
            types.containers.UniTuple) and typemap[wywm__czjct].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(wywm__czjct))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for wrzw__ppkj in func_ir.blocks.values():
        for stmt in wrzw__ppkj.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    qnm__jxj = getattr(val, 'code', None)
                    if qnm__jxj is not None:
                        if getattr(val, 'closure', None) is not None:
                            njg__vzmr = '<creating a function from a closure>'
                            dizmc__vdt = ''
                        else:
                            njg__vzmr = qnm__jxj.co_name
                            dizmc__vdt = '(%s) ' % njg__vzmr
                    else:
                        njg__vzmr = '<could not ascertain use case>'
                        dizmc__vdt = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (njg__vzmr, dizmc__vdt))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                tknvy__nlrgs = False
                if isinstance(val, pytypes.FunctionType):
                    tknvy__nlrgs = val in {numba.gdb, numba.gdb_init}
                if not tknvy__nlrgs:
                    tknvy__nlrgs = getattr(val, '_name', '') == 'gdb_internal'
                if tknvy__nlrgs:
                    ndnb__diqwx.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    ukgfb__sjz = func_ir.get_definition(var)
                    ncqf__ett = guard(find_callname, func_ir, ukgfb__sjz)
                    if ncqf__ett and ncqf__ett[1] == 'numpy':
                        ty = getattr(numpy, ncqf__ett[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    hjn__ayvvb = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(hjn__ayvvb), loc=stmt.loc)
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
    if len(ndnb__diqwx) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        lvdbe__dbw = '\n'.join([x.strformat() for x in ndnb__diqwx])
        raise errors.UnsupportedError(msg % lvdbe__dbw)


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
    zahc__psx, jxges__nsf = next(iter(val.items()))
    pjpi__tguqh = typeof_impl(zahc__psx, c)
    owyb__ysqr = typeof_impl(jxges__nsf, c)
    if pjpi__tguqh is None or owyb__ysqr is None:
        raise ValueError(
            f'Cannot type dict element type {type(zahc__psx)}, {type(jxges__nsf)}'
            )
    return types.DictType(pjpi__tguqh, owyb__ysqr)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    afc__zvl = cgutils.alloca_once_value(c.builder, val)
    opwi__dbc = c.pyapi.object_hasattr_string(val, '_opaque')
    qdzt__uqxzs = c.builder.icmp_unsigned('==', opwi__dbc, lir.Constant(
        opwi__dbc.type, 0))
    jpm__xurgu = typ.key_type
    tuw__dbfle = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(jpm__xurgu, tuw__dbfle)

    def copy_dict(out_dict, in_dict):
        for zahc__psx, jxges__nsf in in_dict.items():
            out_dict[zahc__psx] = jxges__nsf
    with c.builder.if_then(qdzt__uqxzs):
        jdffq__aahhd = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        kxi__vnsu = c.pyapi.call_function_objargs(jdffq__aahhd, [])
        fcx__xzbd = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(fcx__xzbd, [kxi__vnsu, val])
        c.builder.store(kxi__vnsu, afc__zvl)
    val = c.builder.load(afc__zvl)
    hsvsu__ceae = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    eoi__trtz = c.pyapi.object_type(val)
    qiag__bshq = c.builder.icmp_unsigned('==', eoi__trtz, hsvsu__ceae)
    with c.builder.if_else(qiag__bshq) as (eglof__bgs, bif__ofz):
        with eglof__bgs:
            goaxg__ztayz = c.pyapi.object_getattr_string(val, '_opaque')
            gmpk__smof = types.MemInfoPointer(types.voidptr)
            jjl__znbr = c.unbox(gmpk__smof, goaxg__ztayz)
            mi = jjl__znbr.value
            ssged__ciert = gmpk__smof, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *ssged__ciert)
            knr__dtoph = context.get_constant_null(ssged__ciert[1])
            args = mi, knr__dtoph
            epjc__xywg, jps__qdi = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, jps__qdi)
            c.pyapi.decref(goaxg__ztayz)
            drvez__yod = c.builder.basic_block
        with bif__ofz:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", eoi__trtz, hsvsu__ceae)
            mnbj__wcl = c.builder.basic_block
    iyih__kthjk = c.builder.phi(jps__qdi.type)
    bts__websm = c.builder.phi(epjc__xywg.type)
    iyih__kthjk.add_incoming(jps__qdi, drvez__yod)
    iyih__kthjk.add_incoming(jps__qdi.type(None), mnbj__wcl)
    bts__websm.add_incoming(epjc__xywg, drvez__yod)
    bts__websm.add_incoming(cgutils.true_bit, mnbj__wcl)
    c.pyapi.decref(hsvsu__ceae)
    c.pyapi.decref(eoi__trtz)
    with c.builder.if_then(qdzt__uqxzs):
        c.pyapi.decref(val)
    return NativeValue(iyih__kthjk, is_error=bts__websm)


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
    jehde__qhgli = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=jehde__qhgli, name=updatevar)
    szuot__izya = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=szuot__izya, name=res)


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
        for zahc__psx, jxges__nsf in other.items():
            d[zahc__psx] = jxges__nsf
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
    dizmc__vdt = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(dizmc__vdt, res)


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
    mhybg__tqpd = PassManager(name)
    if state.func_ir is None:
        mhybg__tqpd.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            mhybg__tqpd.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        mhybg__tqpd.add_pass(FixupArgs, 'fix up args')
    mhybg__tqpd.add_pass(IRProcessing, 'processing IR')
    mhybg__tqpd.add_pass(WithLifting, 'Handle with contexts')
    mhybg__tqpd.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        mhybg__tqpd.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        mhybg__tqpd.add_pass(DeadBranchPrune, 'dead branch pruning')
        mhybg__tqpd.add_pass(GenericRewrites, 'nopython rewrites')
    mhybg__tqpd.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    mhybg__tqpd.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        mhybg__tqpd.add_pass(DeadBranchPrune, 'dead branch pruning')
    mhybg__tqpd.add_pass(FindLiterallyCalls, 'find literally calls')
    mhybg__tqpd.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        mhybg__tqpd.add_pass(ReconstructSSA, 'ssa')
    mhybg__tqpd.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    mhybg__tqpd.finalize()
    return mhybg__tqpd


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
    a, sftw__kukrt = args
    if isinstance(a, types.List) and isinstance(sftw__kukrt, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(sftw__kukrt, types.List):
        return signature(sftw__kukrt, types.intp, sftw__kukrt)


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
        wpele__saqpt, rpzsg__wbk = 0, 1
    else:
        wpele__saqpt, rpzsg__wbk = 1, 0
    iughu__byqmx = ListInstance(context, builder, sig.args[wpele__saqpt],
        args[wpele__saqpt])
    wwzt__qgz = iughu__byqmx.size
    bqq__hlr = args[rpzsg__wbk]
    kav__qoa = lir.Constant(bqq__hlr.type, 0)
    bqq__hlr = builder.select(cgutils.is_neg_int(builder, bqq__hlr),
        kav__qoa, bqq__hlr)
    vmh__fkwhi = builder.mul(bqq__hlr, wwzt__qgz)
    dii__mfy = ListInstance.allocate(context, builder, sig.return_type,
        vmh__fkwhi)
    dii__mfy.size = vmh__fkwhi
    with cgutils.for_range_slice(builder, kav__qoa, vmh__fkwhi, wwzt__qgz,
        inc=True) as (gdio__jyxiz, _):
        with cgutils.for_range(builder, wwzt__qgz) as ispol__awed:
            value = iughu__byqmx.getitem(ispol__awed.index)
            dii__mfy.setitem(builder.add(ispol__awed.index, gdio__jyxiz),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, dii__mfy.value)


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
    lhb__ipv = first.unify(self, second)
    if lhb__ipv is not None:
        return lhb__ipv
    lhb__ipv = second.unify(self, first)
    if lhb__ipv is not None:
        return lhb__ipv
    qlyu__dfmho = self.can_convert(fromty=first, toty=second)
    if qlyu__dfmho is not None and qlyu__dfmho <= Conversion.safe:
        return second
    qlyu__dfmho = self.can_convert(fromty=second, toty=first)
    if qlyu__dfmho is not None and qlyu__dfmho <= Conversion.safe:
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
    vmh__fkwhi = payload.used
    listobj = c.pyapi.list_new(vmh__fkwhi)
    wpe__gat = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(wpe__gat, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(vmh__fkwhi
            .type, 0))
        with payload._iterate() as ispol__awed:
            i = c.builder.load(index)
            item = ispol__awed.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return wpe__gat, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    qyng__tmdhw = h.type
    qwgvm__eegp = self.mask
    dtype = self._ty.dtype
    yucoz__qxd = context.typing_context
    fnty = yucoz__qxd.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(yucoz__qxd, (dtype, dtype), {})
    dlse__aedg = context.get_function(fnty, sig)
    kxw__rlkk = ir.Constant(qyng__tmdhw, 1)
    rwhis__xxd = ir.Constant(qyng__tmdhw, 5)
    bjezi__zqz = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, qwgvm__eegp))
    if for_insert:
        nns__bmbih = qwgvm__eegp.type(-1)
        zho__gmqjq = cgutils.alloca_once_value(builder, nns__bmbih)
    xcmsm__wbo = builder.append_basic_block('lookup.body')
    qogrf__otne = builder.append_basic_block('lookup.found')
    vqma__ecql = builder.append_basic_block('lookup.not_found')
    ndi__btq = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        olg__aobq = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, olg__aobq)):
            dfe__hrjr = dlse__aedg(builder, (item, entry.key))
            with builder.if_then(dfe__hrjr):
                builder.branch(qogrf__otne)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, olg__aobq)):
            builder.branch(vqma__ecql)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, olg__aobq)):
                lej__rpmd = builder.load(zho__gmqjq)
                lej__rpmd = builder.select(builder.icmp_unsigned('==',
                    lej__rpmd, nns__bmbih), i, lej__rpmd)
                builder.store(lej__rpmd, zho__gmqjq)
    with cgutils.for_range(builder, ir.Constant(qyng__tmdhw, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, kxw__rlkk)
        i = builder.and_(i, qwgvm__eegp)
        builder.store(i, index)
    builder.branch(xcmsm__wbo)
    with builder.goto_block(xcmsm__wbo):
        i = builder.load(index)
        check_entry(i)
        wjro__hhgz = builder.load(bjezi__zqz)
        wjro__hhgz = builder.lshr(wjro__hhgz, rwhis__xxd)
        i = builder.add(kxw__rlkk, builder.mul(i, rwhis__xxd))
        i = builder.and_(qwgvm__eegp, builder.add(i, wjro__hhgz))
        builder.store(i, index)
        builder.store(wjro__hhgz, bjezi__zqz)
        builder.branch(xcmsm__wbo)
    with builder.goto_block(vqma__ecql):
        if for_insert:
            i = builder.load(index)
            lej__rpmd = builder.load(zho__gmqjq)
            i = builder.select(builder.icmp_unsigned('==', lej__rpmd,
                nns__bmbih), i, lej__rpmd)
            builder.store(i, index)
        builder.branch(ndi__btq)
    with builder.goto_block(qogrf__otne):
        builder.branch(ndi__btq)
    builder.position_at_end(ndi__btq)
    tknvy__nlrgs = builder.phi(ir.IntType(1), 'found')
    tknvy__nlrgs.add_incoming(cgutils.true_bit, qogrf__otne)
    tknvy__nlrgs.add_incoming(cgutils.false_bit, vqma__ecql)
    return tknvy__nlrgs, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    wxqxv__avkyq = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    pwzu__zjau = payload.used
    kxw__rlkk = ir.Constant(pwzu__zjau.type, 1)
    pwzu__zjau = payload.used = builder.add(pwzu__zjau, kxw__rlkk)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, wxqxv__avkyq), likely=True):
        payload.fill = builder.add(payload.fill, kxw__rlkk)
    if do_resize:
        self.upsize(pwzu__zjau)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    tknvy__nlrgs, i = payload._lookup(item, h, for_insert=True)
    vlar__dvxun = builder.not_(tknvy__nlrgs)
    with builder.if_then(vlar__dvxun):
        entry = payload.get_entry(i)
        wxqxv__avkyq = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        pwzu__zjau = payload.used
        kxw__rlkk = ir.Constant(pwzu__zjau.type, 1)
        pwzu__zjau = payload.used = builder.add(pwzu__zjau, kxw__rlkk)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, wxqxv__avkyq), likely=True):
            payload.fill = builder.add(payload.fill, kxw__rlkk)
        if do_resize:
            self.upsize(pwzu__zjau)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    pwzu__zjau = payload.used
    kxw__rlkk = ir.Constant(pwzu__zjau.type, 1)
    pwzu__zjau = payload.used = self._builder.sub(pwzu__zjau, kxw__rlkk)
    if do_resize:
        self.downsize(pwzu__zjau)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    qyxuy__tcijm = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, qyxuy__tcijm)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    yfe__rfzu = payload
    wpe__gat = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(wpe__gat), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with yfe__rfzu._iterate() as ispol__awed:
        entry = ispol__awed.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(yfe__rfzu.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as ispol__awed:
        entry = ispol__awed.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    wpe__gat = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(wpe__gat), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    wpe__gat = cgutils.alloca_once_value(builder, cgutils.true_bit)
    qyng__tmdhw = context.get_value_type(types.intp)
    kav__qoa = ir.Constant(qyng__tmdhw, 0)
    kxw__rlkk = ir.Constant(qyng__tmdhw, 1)
    hkn__ikopq = context.get_data_type(types.SetPayload(self._ty))
    illi__bqdt = context.get_abi_sizeof(hkn__ikopq)
    qman__ooot = self._entrysize
    illi__bqdt -= qman__ooot
    xcv__gczol, ljrog__opg = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(qyng__tmdhw, qman__ooot), ir.Constant(qyng__tmdhw,
        illi__bqdt))
    with builder.if_then(ljrog__opg, likely=False):
        builder.store(cgutils.false_bit, wpe__gat)
    with builder.if_then(builder.load(wpe__gat), likely=True):
        if realloc:
            jbmww__olaqj = self._set.meminfo
            sbtkd__sxtxx = context.nrt.meminfo_varsize_alloc(builder,
                jbmww__olaqj, size=xcv__gczol)
            cgwia__aog = cgutils.is_null(builder, sbtkd__sxtxx)
        else:
            acjn__bgioq = _imp_dtor(context, builder.module, self._ty)
            jbmww__olaqj = context.nrt.meminfo_new_varsize_dtor(builder,
                xcv__gczol, builder.bitcast(acjn__bgioq, cgutils.voidptr_t))
            cgwia__aog = cgutils.is_null(builder, jbmww__olaqj)
        with builder.if_else(cgwia__aog, likely=False) as (ubqgi__lpv,
            xvo__ujzlc):
            with ubqgi__lpv:
                builder.store(cgutils.false_bit, wpe__gat)
            with xvo__ujzlc:
                if not realloc:
                    self._set.meminfo = jbmww__olaqj
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, xcv__gczol, 255)
                payload.used = kav__qoa
                payload.fill = kav__qoa
                payload.finger = kav__qoa
                veeq__vwd = builder.sub(nentries, kxw__rlkk)
                payload.mask = veeq__vwd
    return builder.load(wpe__gat)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    wpe__gat = cgutils.alloca_once_value(builder, cgutils.true_bit)
    qyng__tmdhw = context.get_value_type(types.intp)
    kav__qoa = ir.Constant(qyng__tmdhw, 0)
    kxw__rlkk = ir.Constant(qyng__tmdhw, 1)
    hkn__ikopq = context.get_data_type(types.SetPayload(self._ty))
    illi__bqdt = context.get_abi_sizeof(hkn__ikopq)
    qman__ooot = self._entrysize
    illi__bqdt -= qman__ooot
    qwgvm__eegp = src_payload.mask
    nentries = builder.add(kxw__rlkk, qwgvm__eegp)
    xcv__gczol = builder.add(ir.Constant(qyng__tmdhw, illi__bqdt), builder.
        mul(ir.Constant(qyng__tmdhw, qman__ooot), nentries))
    with builder.if_then(builder.load(wpe__gat), likely=True):
        acjn__bgioq = _imp_dtor(context, builder.module, self._ty)
        jbmww__olaqj = context.nrt.meminfo_new_varsize_dtor(builder,
            xcv__gczol, builder.bitcast(acjn__bgioq, cgutils.voidptr_t))
        cgwia__aog = cgutils.is_null(builder, jbmww__olaqj)
        with builder.if_else(cgwia__aog, likely=False) as (ubqgi__lpv,
            xvo__ujzlc):
            with ubqgi__lpv:
                builder.store(cgutils.false_bit, wpe__gat)
            with xvo__ujzlc:
                self._set.meminfo = jbmww__olaqj
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = kav__qoa
                payload.mask = qwgvm__eegp
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, qman__ooot)
                with src_payload._iterate() as ispol__awed:
                    context.nrt.incref(builder, self._ty.dtype, ispol__awed
                        .entry.key)
    return builder.load(wpe__gat)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    gptf__cvt = context.get_value_type(types.voidptr)
    rvvml__ydj = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [gptf__cvt, rvvml__ydj, gptf__cvt])
    plnb__ofn = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=plnb__ofn)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        pjcs__ahb = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, pjcs__ahb)
        with payload._iterate() as ispol__awed:
            entry = ispol__awed.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    mov__gri, = sig.args
    mhui__clom, = args
    zuc__lgcv = numba.core.imputils.call_len(context, builder, mov__gri,
        mhui__clom)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, zuc__lgcv)
    with numba.core.imputils.for_iter(context, builder, mov__gri, mhui__clom
        ) as ispol__awed:
        inst.add(ispol__awed.value)
        context.nrt.decref(builder, set_type.dtype, ispol__awed.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    mov__gri = sig.args[1]
    mhui__clom = args[1]
    zuc__lgcv = numba.core.imputils.call_len(context, builder, mov__gri,
        mhui__clom)
    if zuc__lgcv is not None:
        nho__anf = builder.add(inst.payload.used, zuc__lgcv)
        inst.upsize(nho__anf)
    with numba.core.imputils.for_iter(context, builder, mov__gri, mhui__clom
        ) as ispol__awed:
        zxsc__pan = context.cast(builder, ispol__awed.value, mov__gri.dtype,
            inst.dtype)
        inst.add(zxsc__pan)
        context.nrt.decref(builder, mov__gri.dtype, ispol__awed.value)
    if zuc__lgcv is not None:
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
    mhm__iwpk = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, mhm__iwpk, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    wiuwa__iutsk = target_context.get_executable(library, fndesc, env)
    qpvfz__thw = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=wiuwa__iutsk, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return qpvfz__thw


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
