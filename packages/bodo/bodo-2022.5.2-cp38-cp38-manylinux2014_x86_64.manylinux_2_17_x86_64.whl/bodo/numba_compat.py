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
    eiwz__uwjl = numba.core.bytecode.FunctionIdentity.from_function(func)
    htat__vgrpa = numba.core.interpreter.Interpreter(eiwz__uwjl)
    hcr__brx = numba.core.bytecode.ByteCode(func_id=eiwz__uwjl)
    func_ir = htat__vgrpa.interpret(hcr__brx)
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
        oiw__isere = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        oiw__isere.run()
    rbz__xodl = numba.core.postproc.PostProcessor(func_ir)
    rbz__xodl.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, tgsa__ayk in visit_vars_extensions.items():
        if isinstance(stmt, t):
            tgsa__ayk(stmt, callback, cbdata)
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
    tox__pta = ['ravel', 'transpose', 'reshape']
    for paae__ipdc in blocks.values():
        for bkub__ofiy in paae__ipdc.body:
            if type(bkub__ofiy) in alias_analysis_extensions:
                tgsa__ayk = alias_analysis_extensions[type(bkub__ofiy)]
                tgsa__ayk(bkub__ofiy, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(bkub__ofiy, ir.Assign):
                zjlkv__ldhq = bkub__ofiy.value
                qxip__hpcph = bkub__ofiy.target.name
                if is_immutable_type(qxip__hpcph, typemap):
                    continue
                if isinstance(zjlkv__ldhq, ir.Var
                    ) and qxip__hpcph != zjlkv__ldhq.name:
                    _add_alias(qxip__hpcph, zjlkv__ldhq.name, alias_map,
                        arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr) and (zjlkv__ldhq.op ==
                    'cast' or zjlkv__ldhq.op in ['getitem', 'static_getitem']):
                    _add_alias(qxip__hpcph, zjlkv__ldhq.value.name,
                        alias_map, arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr
                    ) and zjlkv__ldhq.op == 'inplace_binop':
                    _add_alias(qxip__hpcph, zjlkv__ldhq.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr
                    ) and zjlkv__ldhq.op == 'getattr' and zjlkv__ldhq.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(qxip__hpcph, zjlkv__ldhq.value.name,
                        alias_map, arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr
                    ) and zjlkv__ldhq.op == 'getattr' and zjlkv__ldhq.attr not in [
                    'shape'] and zjlkv__ldhq.value.name in arg_aliases:
                    _add_alias(qxip__hpcph, zjlkv__ldhq.value.name,
                        alias_map, arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr
                    ) and zjlkv__ldhq.op == 'getattr' and zjlkv__ldhq.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(qxip__hpcph, zjlkv__ldhq.value.name,
                        alias_map, arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr) and zjlkv__ldhq.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(qxip__hpcph, typemap):
                    for blb__xtsdl in zjlkv__ldhq.items:
                        _add_alias(qxip__hpcph, blb__xtsdl.name, alias_map,
                            arg_aliases)
                if isinstance(zjlkv__ldhq, ir.Expr
                    ) and zjlkv__ldhq.op == 'call':
                    rft__ongjy = guard(find_callname, func_ir, zjlkv__ldhq,
                        typemap)
                    if rft__ongjy is None:
                        continue
                    zpgm__nur, qgfsy__bnn = rft__ongjy
                    if rft__ongjy in alias_func_extensions:
                        rnelh__xpdab = alias_func_extensions[rft__ongjy]
                        rnelh__xpdab(qxip__hpcph, zjlkv__ldhq.args,
                            alias_map, arg_aliases)
                    if qgfsy__bnn == 'numpy' and zpgm__nur in tox__pta:
                        _add_alias(qxip__hpcph, zjlkv__ldhq.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(qgfsy__bnn, ir.Var
                        ) and zpgm__nur in tox__pta:
                        _add_alias(qxip__hpcph, qgfsy__bnn.name, alias_map,
                            arg_aliases)
    eml__def = copy.deepcopy(alias_map)
    for blb__xtsdl in eml__def:
        for whm__vrir in eml__def[blb__xtsdl]:
            alias_map[blb__xtsdl] |= alias_map[whm__vrir]
        for whm__vrir in eml__def[blb__xtsdl]:
            alias_map[whm__vrir] = alias_map[blb__xtsdl]
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
    hgivg__tun = compute_cfg_from_blocks(func_ir.blocks)
    qez__jfygy = compute_use_defs(func_ir.blocks)
    cgioc__lxih = compute_live_map(hgivg__tun, func_ir.blocks, qez__jfygy.
        usemap, qez__jfygy.defmap)
    wze__vfg = True
    while wze__vfg:
        wze__vfg = False
        for ymvls__gebgc, block in func_ir.blocks.items():
            lives = {blb__xtsdl.name for blb__xtsdl in block.terminator.
                list_vars()}
            for tax__xril, bhh__xjnhm in hgivg__tun.successors(ymvls__gebgc):
                lives |= cgioc__lxih[tax__xril]
            fiuhi__lym = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    qxip__hpcph = stmt.target
                    bjpbh__oyutl = stmt.value
                    if qxip__hpcph.name not in lives:
                        if isinstance(bjpbh__oyutl, ir.Expr
                            ) and bjpbh__oyutl.op == 'make_function':
                            continue
                        if isinstance(bjpbh__oyutl, ir.Expr
                            ) and bjpbh__oyutl.op == 'getattr':
                            continue
                        if isinstance(bjpbh__oyutl, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(qxip__hpcph,
                            None), types.Function):
                            continue
                        if isinstance(bjpbh__oyutl, ir.Expr
                            ) and bjpbh__oyutl.op == 'build_map':
                            continue
                        if isinstance(bjpbh__oyutl, ir.Expr
                            ) and bjpbh__oyutl.op == 'build_tuple':
                            continue
                    if isinstance(bjpbh__oyutl, ir.Var
                        ) and qxip__hpcph.name == bjpbh__oyutl.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    fer__qxiq = analysis.ir_extension_usedefs[type(stmt)]
                    itsbm__ubr, tpwm__ngf = fer__qxiq(stmt)
                    lives -= tpwm__ngf
                    lives |= itsbm__ubr
                else:
                    lives |= {blb__xtsdl.name for blb__xtsdl in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(qxip__hpcph.name)
                fiuhi__lym.append(stmt)
            fiuhi__lym.reverse()
            if len(block.body) != len(fiuhi__lym):
                wze__vfg = True
            block.body = fiuhi__lym


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    llza__idgy = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (llza__idgy,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    pml__zsw = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), pml__zsw)


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
            for xijo__xlzk in fnty.templates:
                self._inline_overloads.update(xijo__xlzk._inline_overloads)
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
    pml__zsw = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), pml__zsw)
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
    meb__zfolr, dvz__nbbt = self._get_impl(args, kws)
    if meb__zfolr is None:
        return
    zid__ksfdc = types.Dispatcher(meb__zfolr)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        vnpjr__bebhy = meb__zfolr._compiler
        flags = compiler.Flags()
        vvdy__frk = vnpjr__bebhy.targetdescr.typing_context
        yqum__wgszx = vnpjr__bebhy.targetdescr.target_context
        afviw__syh = vnpjr__bebhy.pipeline_class(vvdy__frk, yqum__wgszx,
            None, None, None, flags, None)
        cmwvw__cpp = InlineWorker(vvdy__frk, yqum__wgszx, vnpjr__bebhy.
            locals, afviw__syh, flags, None)
        gof__pvy = zid__ksfdc.dispatcher.get_call_template
        xijo__xlzk, uedik__abpsc, wnlq__bfa, kws = gof__pvy(dvz__nbbt, kws)
        if wnlq__bfa in self._inline_overloads:
            return self._inline_overloads[wnlq__bfa]['iinfo'].signature
        ir = cmwvw__cpp.run_untyped_passes(zid__ksfdc.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, yqum__wgszx, ir, wnlq__bfa, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, wnlq__bfa, None)
        self._inline_overloads[sig.args] = {'folded_args': wnlq__bfa}
        qgz__orty = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = qgz__orty
        if not self._inline.is_always_inline:
            sig = zid__ksfdc.get_call_type(self.context, dvz__nbbt, kws)
            self._compiled_overloads[sig.args] = zid__ksfdc.get_overload(sig)
        prmtj__qrjz = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': wnlq__bfa,
            'iinfo': prmtj__qrjz}
    else:
        sig = zid__ksfdc.get_call_type(self.context, dvz__nbbt, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = zid__ksfdc.get_overload(sig)
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
    hwzgn__kme = [True, False]
    auw__nrkg = [False, True]
    gshnj__egnsl = _ResolutionFailures(context, self, args, kws, depth=self
        ._depth)
    from numba.core.target_extension import get_local_target
    lupi__mmiyh = get_local_target(context)
    ftlcl__kbspr = utils.order_by_target_specificity(lupi__mmiyh, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for jrgy__zwu in ftlcl__kbspr:
        qteul__cjmri = jrgy__zwu(context)
        jdjok__riklt = hwzgn__kme if qteul__cjmri.prefer_literal else auw__nrkg
        jdjok__riklt = [True] if getattr(qteul__cjmri, '_no_unliteral', False
            ) else jdjok__riklt
        for hsdlw__ejvc in jdjok__riklt:
            try:
                if hsdlw__ejvc:
                    sig = qteul__cjmri.apply(args, kws)
                else:
                    qhq__xzhko = tuple([_unlit_non_poison(a) for a in args])
                    nix__zlw = {zgy__ltsm: _unlit_non_poison(blb__xtsdl) for
                        zgy__ltsm, blb__xtsdl in kws.items()}
                    sig = qteul__cjmri.apply(qhq__xzhko, nix__zlw)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    gshnj__egnsl.add_error(qteul__cjmri, False, e, hsdlw__ejvc)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = qteul__cjmri.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    rezum__pot = getattr(qteul__cjmri, 'cases', None)
                    if rezum__pot is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            rezum__pot)
                    else:
                        msg = 'No match.'
                    gshnj__egnsl.add_error(qteul__cjmri, True, msg, hsdlw__ejvc
                        )
    gshnj__egnsl.raise_error()


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
    xijo__xlzk = self.template(context)
    agf__lzx = None
    wui__cdjn = None
    lkua__akueu = None
    jdjok__riklt = [True, False] if xijo__xlzk.prefer_literal else [False, True
        ]
    jdjok__riklt = [True] if getattr(xijo__xlzk, '_no_unliteral', False
        ) else jdjok__riklt
    for hsdlw__ejvc in jdjok__riklt:
        if hsdlw__ejvc:
            try:
                lkua__akueu = xijo__xlzk.apply(args, kws)
            except Exception as xcqry__xfinp:
                if isinstance(xcqry__xfinp, errors.ForceLiteralArg):
                    raise xcqry__xfinp
                agf__lzx = xcqry__xfinp
                lkua__akueu = None
            else:
                break
        else:
            ygyj__krsra = tuple([_unlit_non_poison(a) for a in args])
            bgidw__bpj = {zgy__ltsm: _unlit_non_poison(blb__xtsdl) for 
                zgy__ltsm, blb__xtsdl in kws.items()}
            ync__btzfq = ygyj__krsra == args and kws == bgidw__bpj
            if not ync__btzfq and lkua__akueu is None:
                try:
                    lkua__akueu = xijo__xlzk.apply(ygyj__krsra, bgidw__bpj)
                except Exception as xcqry__xfinp:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        xcqry__xfinp, errors.NumbaError):
                        raise xcqry__xfinp
                    if isinstance(xcqry__xfinp, errors.ForceLiteralArg):
                        if xijo__xlzk.prefer_literal:
                            raise xcqry__xfinp
                    wui__cdjn = xcqry__xfinp
                else:
                    break
    if lkua__akueu is None and (wui__cdjn is not None or agf__lzx is not None):
        cdxx__bvl = '- Resolution failure for {} arguments:\n{}\n'
        dkj__cigyq = _termcolor.highlight(cdxx__bvl)
        if numba.core.config.DEVELOPER_MODE:
            jnvz__hik = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    fdii__neogh = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    fdii__neogh = ['']
                zmmy__gnuza = '\n{}'.format(2 * jnvz__hik)
                bmhk__kpyt = _termcolor.reset(zmmy__gnuza + zmmy__gnuza.
                    join(_bt_as_lines(fdii__neogh)))
                return _termcolor.reset(bmhk__kpyt)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            wvpv__qwsyu = str(e)
            wvpv__qwsyu = wvpv__qwsyu if wvpv__qwsyu else str(repr(e)
                ) + add_bt(e)
            rhx__ikn = errors.TypingError(textwrap.dedent(wvpv__qwsyu))
            return dkj__cigyq.format(literalness, str(rhx__ikn))
        import bodo
        if isinstance(agf__lzx, bodo.utils.typing.BodoError):
            raise agf__lzx
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', agf__lzx) +
                nested_msg('non-literal', wui__cdjn))
        else:
            if 'missing a required argument' in agf__lzx.msg:
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
            raise errors.TypingError(msg, loc=agf__lzx.loc)
    return lkua__akueu


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
    zpgm__nur = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=zpgm__nur)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            puvyz__tlov = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), puvyz__tlov)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    kibs__fch = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            kibs__fch.append(types.Omitted(a.value))
        else:
            kibs__fch.append(self.typeof_pyval(a))
    hhrgx__ittnu = None
    try:
        error = None
        hhrgx__ittnu = self.compile(tuple(kibs__fch))
    except errors.ForceLiteralArg as e:
        wiy__jmtu = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if wiy__jmtu:
            xgjxt__ultm = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            mrgjz__doem = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(wiy__jmtu))
            raise errors.CompilerError(xgjxt__ultm.format(mrgjz__doem))
        dvz__nbbt = []
        try:
            for i, blb__xtsdl in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        dvz__nbbt.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        dvz__nbbt.append(types.literal(args[i]))
                else:
                    dvz__nbbt.append(args[i])
            args = dvz__nbbt
        except (OSError, FileNotFoundError) as hnwq__ndvjv:
            error = FileNotFoundError(str(hnwq__ndvjv) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                hhrgx__ittnu = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        nykv__lylio = []
        for i, rxmq__figjo in enumerate(args):
            val = rxmq__figjo.value if isinstance(rxmq__figjo, numba.core.
                dispatcher.OmittedArg) else rxmq__figjo
            try:
                cgx__jdwt = typeof(val, Purpose.argument)
            except ValueError as lsn__bmfj:
                nykv__lylio.append((i, str(lsn__bmfj)))
            else:
                if cgx__jdwt is None:
                    nykv__lylio.append((i,
                        f'cannot determine Numba type of value {val}'))
        if nykv__lylio:
            jcon__mmzdw = '\n'.join(f'- argument {i}: {yll__oche}' for i,
                yll__oche in nykv__lylio)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{jcon__mmzdw}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                oyrng__dltoe = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                nfkuu__mqp = False
                for qnqb__nszf in oyrng__dltoe:
                    if qnqb__nszf in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        nfkuu__mqp = True
                        break
                if not nfkuu__mqp:
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
                puvyz__tlov = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), puvyz__tlov)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return hhrgx__ittnu


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
    for tsdf__zqml in cres.library._codegen._engine._defined_symbols:
        if tsdf__zqml.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in tsdf__zqml and (
            'bodo_gb_udf_update_local' in tsdf__zqml or 
            'bodo_gb_udf_combine' in tsdf__zqml or 'bodo_gb_udf_eval' in
            tsdf__zqml or 'bodo_gb_apply_general_udfs' in tsdf__zqml):
            gb_agg_cfunc_addr[tsdf__zqml
                ] = cres.library.get_pointer_to_function(tsdf__zqml)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for tsdf__zqml in cres.library._codegen._engine._defined_symbols:
        if tsdf__zqml.startswith('cfunc') and ('get_join_cond_addr' not in
            tsdf__zqml or 'bodo_join_gen_cond' in tsdf__zqml):
            join_gen_cond_cfunc_addr[tsdf__zqml
                ] = cres.library.get_pointer_to_function(tsdf__zqml)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    meb__zfolr = self._get_dispatcher_for_current_target()
    if meb__zfolr is not self:
        return meb__zfolr.compile(sig)
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
            eib__zsm = self.overloads.get(tuple(args))
            if eib__zsm is not None:
                return eib__zsm.entry_point
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
            lrtd__soejv = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=lrtd__soejv):
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
                hnjj__gim = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in hnjj__gim:
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
    vxg__bgrqc = self._final_module
    fmk__bawnk = []
    enqb__wyl = 0
    for fn in vxg__bgrqc.functions:
        enqb__wyl += 1
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
            fmk__bawnk.append(fn.name)
    if enqb__wyl == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if fmk__bawnk:
        vxg__bgrqc = vxg__bgrqc.clone()
        for name in fmk__bawnk:
            vxg__bgrqc.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = vxg__bgrqc
    return vxg__bgrqc


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
    for xenbx__ehw in self.constraints:
        loc = xenbx__ehw.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                xenbx__ehw(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                yybat__xznho = numba.core.errors.TypingError(str(e), loc=
                    xenbx__ehw.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(yybat__xznho, e)
                    )
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
                    yybat__xznho = numba.core.errors.TypingError(msg.format
                        (con=xenbx__ehw, err=str(e)), loc=xenbx__ehw.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(yybat__xznho, e))
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
    for uzytw__ablga in self._failures.values():
        for sfd__ttpt in uzytw__ablga:
            if isinstance(sfd__ttpt.error, ForceLiteralArg):
                raise sfd__ttpt.error
            if isinstance(sfd__ttpt.error, bodo.utils.typing.BodoError):
                raise sfd__ttpt.error
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
    hafs__alx = False
    fiuhi__lym = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        rnr__jozo = set()
        osh__yhxgw = lives & alias_set
        for blb__xtsdl in osh__yhxgw:
            rnr__jozo |= alias_map[blb__xtsdl]
        lives_n_aliases = lives | rnr__jozo | arg_aliases
        if type(stmt) in remove_dead_extensions:
            tgsa__ayk = remove_dead_extensions[type(stmt)]
            stmt = tgsa__ayk(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                hafs__alx = True
                continue
        if isinstance(stmt, ir.Assign):
            qxip__hpcph = stmt.target
            bjpbh__oyutl = stmt.value
            if qxip__hpcph.name not in lives and has_no_side_effect(
                bjpbh__oyutl, lives_n_aliases, call_table):
                hafs__alx = True
                continue
            if saved_array_analysis and qxip__hpcph.name in lives and is_expr(
                bjpbh__oyutl, 'getattr'
                ) and bjpbh__oyutl.attr == 'shape' and is_array_typ(typemap
                [bjpbh__oyutl.value.name]
                ) and bjpbh__oyutl.value.name not in lives:
                tpa__hxgk = {blb__xtsdl: zgy__ltsm for zgy__ltsm,
                    blb__xtsdl in func_ir.blocks.items()}
                if block in tpa__hxgk:
                    ymvls__gebgc = tpa__hxgk[block]
                    knz__ignac = saved_array_analysis.get_equiv_set(
                        ymvls__gebgc)
                    ooau__imc = knz__ignac.get_equiv_set(bjpbh__oyutl.value)
                    if ooau__imc is not None:
                        for blb__xtsdl in ooau__imc:
                            if blb__xtsdl.endswith('#0'):
                                blb__xtsdl = blb__xtsdl[:-2]
                            if blb__xtsdl in typemap and is_array_typ(typemap
                                [blb__xtsdl]) and blb__xtsdl in lives:
                                bjpbh__oyutl.value = ir.Var(bjpbh__oyutl.
                                    value.scope, blb__xtsdl, bjpbh__oyutl.
                                    value.loc)
                                hafs__alx = True
                                break
            if isinstance(bjpbh__oyutl, ir.Var
                ) and qxip__hpcph.name == bjpbh__oyutl.name:
                hafs__alx = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                hafs__alx = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            fer__qxiq = analysis.ir_extension_usedefs[type(stmt)]
            itsbm__ubr, tpwm__ngf = fer__qxiq(stmt)
            lives -= tpwm__ngf
            lives |= itsbm__ubr
        else:
            lives |= {blb__xtsdl.name for blb__xtsdl in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                bjaf__dqj = set()
                if isinstance(bjpbh__oyutl, ir.Expr):
                    bjaf__dqj = {blb__xtsdl.name for blb__xtsdl in
                        bjpbh__oyutl.list_vars()}
                if qxip__hpcph.name not in bjaf__dqj:
                    lives.remove(qxip__hpcph.name)
        fiuhi__lym.append(stmt)
    fiuhi__lym.reverse()
    block.body = fiuhi__lym
    return hafs__alx


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            zctbd__mahdj, = args
            if isinstance(zctbd__mahdj, types.IterableType):
                dtype = zctbd__mahdj.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), zctbd__mahdj)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    wmln__qyq = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (wmln__qyq, self.dtype)
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
        except LiteralTypingError as ymrfa__ohccg:
            return
    try:
        return literal(value)
    except LiteralTypingError as ymrfa__ohccg:
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
        uft__cxbz = py_func.__qualname__
    except AttributeError as ymrfa__ohccg:
        uft__cxbz = py_func.__name__
    pdqh__ghcqi = inspect.getfile(py_func)
    for cls in self._locator_classes:
        ifs__yna = cls.from_function(py_func, pdqh__ghcqi)
        if ifs__yna is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (uft__cxbz, pdqh__ghcqi))
    self._locator = ifs__yna
    yqfrp__peax = inspect.getfile(py_func)
    pmgrc__ihdi = os.path.splitext(os.path.basename(yqfrp__peax))[0]
    if pdqh__ghcqi.startswith('<ipython-'):
        lvyoe__aeci = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', pmgrc__ihdi, count=1)
        if lvyoe__aeci == pmgrc__ihdi:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        pmgrc__ihdi = lvyoe__aeci
    xxhy__bnnit = '%s.%s' % (pmgrc__ihdi, uft__cxbz)
    jmwe__zlkw = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(xxhy__bnnit, jmwe__zlkw)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    gwwje__jick = list(filter(lambda a: self._istuple(a.name), args))
    if len(gwwje__jick) == 2 and fn.__name__ == 'add':
        yalyk__ggkau = self.typemap[gwwje__jick[0].name]
        nvrsq__mdsl = self.typemap[gwwje__jick[1].name]
        if yalyk__ggkau.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                gwwje__jick[1]))
        if nvrsq__mdsl.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                gwwje__jick[0]))
        try:
            utvtk__wwrz = [equiv_set.get_shape(x) for x in gwwje__jick]
            if None in utvtk__wwrz:
                return None
            wiryk__ysd = sum(utvtk__wwrz, ())
            return ArrayAnalysis.AnalyzeResult(shape=wiryk__ysd)
        except GuardException as ymrfa__ohccg:
            return None
    ugct__xfi = list(filter(lambda a: self._isarray(a.name), args))
    require(len(ugct__xfi) > 0)
    opy__xog = [x.name for x in ugct__xfi]
    lmzt__ogdzh = [self.typemap[x.name].ndim for x in ugct__xfi]
    avx__xiaj = max(lmzt__ogdzh)
    require(avx__xiaj > 0)
    utvtk__wwrz = [equiv_set.get_shape(x) for x in ugct__xfi]
    if any(a is None for a in utvtk__wwrz):
        return ArrayAnalysis.AnalyzeResult(shape=ugct__xfi[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, ugct__xfi))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, utvtk__wwrz,
        opy__xog)


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
    rot__bvzam = code_obj.code
    gfti__jyg = len(rot__bvzam.co_freevars)
    goo__bul = rot__bvzam.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        aodvj__prk, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        goo__bul = [blb__xtsdl.name for blb__xtsdl in aodvj__prk]
    mgmz__hduzu = caller_ir.func_id.func.__globals__
    try:
        mgmz__hduzu = getattr(code_obj, 'globals', mgmz__hduzu)
    except KeyError as ymrfa__ohccg:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    vplu__cosp = []
    for x in goo__bul:
        try:
            vfq__bnb = caller_ir.get_definition(x)
        except KeyError as ymrfa__ohccg:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(vfq__bnb, (ir.Const, ir.Global, ir.FreeVar)):
            val = vfq__bnb.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                llza__idgy = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                mgmz__hduzu[llza__idgy] = bodo.jit(distributed=False)(val)
                mgmz__hduzu[llza__idgy].is_nested_func = True
                val = llza__idgy
            if isinstance(val, CPUDispatcher):
                llza__idgy = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                mgmz__hduzu[llza__idgy] = val
                val = llza__idgy
            vplu__cosp.append(val)
        elif isinstance(vfq__bnb, ir.Expr) and vfq__bnb.op == 'make_function':
            tkwf__mgkce = convert_code_obj_to_function(vfq__bnb, caller_ir)
            llza__idgy = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            mgmz__hduzu[llza__idgy] = bodo.jit(distributed=False)(tkwf__mgkce)
            mgmz__hduzu[llza__idgy].is_nested_func = True
            vplu__cosp.append(llza__idgy)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    bdgg__sqkm = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        vplu__cosp)])
    wccxy__bja = ','.join([('c_%d' % i) for i in range(gfti__jyg)])
    jsh__fkxhv = list(rot__bvzam.co_varnames)
    xjh__heer = 0
    wew__ifjyp = rot__bvzam.co_argcount
    zaryo__aim = caller_ir.get_definition(code_obj.defaults)
    if zaryo__aim is not None:
        if isinstance(zaryo__aim, tuple):
            d = [caller_ir.get_definition(x).value for x in zaryo__aim]
            gvlg__zuewe = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in zaryo__aim.items]
            gvlg__zuewe = tuple(d)
        xjh__heer = len(gvlg__zuewe)
    hlqqr__nhe = wew__ifjyp - xjh__heer
    ljbr__fisf = ','.join([('%s' % jsh__fkxhv[i]) for i in range(hlqqr__nhe)])
    if xjh__heer:
        gkfo__ietl = [('%s = %s' % (jsh__fkxhv[i + hlqqr__nhe], gvlg__zuewe
            [i])) for i in range(xjh__heer)]
        ljbr__fisf += ', '
        ljbr__fisf += ', '.join(gkfo__ietl)
    return _create_function_from_code_obj(rot__bvzam, bdgg__sqkm,
        ljbr__fisf, wccxy__bja, mgmz__hduzu)


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
    for jsmgc__mhu, (pnaqz__ovfy, nwfe__rlatg) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % nwfe__rlatg)
            gtri__xhg = _pass_registry.get(pnaqz__ovfy).pass_inst
            if isinstance(gtri__xhg, CompilerPass):
                self._runPass(jsmgc__mhu, gtri__xhg, state)
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
                    pipeline_name, nwfe__rlatg)
                ehq__cqj = self._patch_error(msg, e)
                raise ehq__cqj
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
    kefik__bofh = None
    tpwm__ngf = {}

    def lookup(var, already_seen, varonly=True):
        val = tpwm__ngf.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    mgi__iqmmb = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        qxip__hpcph = stmt.target
        bjpbh__oyutl = stmt.value
        tpwm__ngf[qxip__hpcph.name] = bjpbh__oyutl
        if isinstance(bjpbh__oyutl, ir.Var) and bjpbh__oyutl.name in tpwm__ngf:
            bjpbh__oyutl = lookup(bjpbh__oyutl, set())
        if isinstance(bjpbh__oyutl, ir.Expr):
            uig__lgznz = set(lookup(blb__xtsdl, set(), True).name for
                blb__xtsdl in bjpbh__oyutl.list_vars())
            if name in uig__lgznz:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(bjpbh__oyutl)]
                plmol__gvyf = [x for x, pyeha__xivct in args if 
                    pyeha__xivct.name != name]
                args = [(x, pyeha__xivct) for x, pyeha__xivct in args if x !=
                    pyeha__xivct.name]
                nbj__lciea = dict(args)
                if len(plmol__gvyf) == 1:
                    nbj__lciea[plmol__gvyf[0]] = ir.Var(qxip__hpcph.scope, 
                        name + '#init', qxip__hpcph.loc)
                replace_vars_inner(bjpbh__oyutl, nbj__lciea)
                kefik__bofh = nodes[i:]
                break
    return kefik__bofh


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
        gax__oni = expand_aliases({blb__xtsdl.name for blb__xtsdl in stmt.
            list_vars()}, alias_map, arg_aliases)
        ylfz__hflz = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        shi__wyb = expand_aliases({blb__xtsdl.name for blb__xtsdl in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        ztng__qbof = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(ylfz__hflz & shi__wyb | ztng__qbof & gax__oni) == 0:
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
    ymz__dvq = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            ymz__dvq.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                ymz__dvq.update(get_parfor_writes(stmt, func_ir))
    return ymz__dvq


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    ymz__dvq = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        ymz__dvq.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        ymz__dvq = {blb__xtsdl.name for blb__xtsdl in stmt.df_out_vars.values()
            }
        if stmt.out_key_vars is not None:
            ymz__dvq.update({blb__xtsdl.name for blb__xtsdl in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        ymz__dvq = {blb__xtsdl.name for blb__xtsdl in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        ymz__dvq = {blb__xtsdl.name for blb__xtsdl in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            ymz__dvq.update({blb__xtsdl.name for blb__xtsdl in stmt.
                out_key_arrs})
            ymz__dvq.update({blb__xtsdl.name for blb__xtsdl in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        rft__ongjy = guard(find_callname, func_ir, stmt.value)
        if rft__ongjy in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            ymz__dvq.add(stmt.value.args[0].name)
        if rft__ongjy == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            ymz__dvq.add(stmt.value.args[1].name)
    return ymz__dvq


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
        tgsa__ayk = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        trpzk__lgc = tgsa__ayk.format(self, msg)
        self.args = trpzk__lgc,
    else:
        tgsa__ayk = _termcolor.errmsg('{0}')
        trpzk__lgc = tgsa__ayk.format(self)
        self.args = trpzk__lgc,
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
        for kzqs__wsbmb in options['distributed']:
            dist_spec[kzqs__wsbmb] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for kzqs__wsbmb in options['distributed_block']:
            dist_spec[kzqs__wsbmb] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    kmny__ark = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, cdbrq__jjdyk in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(cdbrq__jjdyk)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    epxs__gkgi = {}
    for wdmxv__nqii in reversed(inspect.getmro(cls)):
        epxs__gkgi.update(wdmxv__nqii.__dict__)
    ujumj__ueem, uqrus__pxafz, beguu__gsg, rwigv__xgjau = {}, {}, {}, {}
    for zgy__ltsm, blb__xtsdl in epxs__gkgi.items():
        if isinstance(blb__xtsdl, pytypes.FunctionType):
            ujumj__ueem[zgy__ltsm] = blb__xtsdl
        elif isinstance(blb__xtsdl, property):
            uqrus__pxafz[zgy__ltsm] = blb__xtsdl
        elif isinstance(blb__xtsdl, staticmethod):
            beguu__gsg[zgy__ltsm] = blb__xtsdl
        else:
            rwigv__xgjau[zgy__ltsm] = blb__xtsdl
    apu__oavuo = (set(ujumj__ueem) | set(uqrus__pxafz) | set(beguu__gsg)
        ) & set(spec)
    if apu__oavuo:
        raise NameError('name shadowing: {0}'.format(', '.join(apu__oavuo)))
    qdzap__vyemf = rwigv__xgjau.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(rwigv__xgjau)
    if rwigv__xgjau:
        msg = 'class members are not yet supported: {0}'
        yvuo__nnrt = ', '.join(rwigv__xgjau.keys())
        raise TypeError(msg.format(yvuo__nnrt))
    for zgy__ltsm, blb__xtsdl in uqrus__pxafz.items():
        if blb__xtsdl.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(zgy__ltsm))
    jit_methods = {zgy__ltsm: bodo.jit(returns_maybe_distributed=kmny__ark)
        (blb__xtsdl) for zgy__ltsm, blb__xtsdl in ujumj__ueem.items()}
    jit_props = {}
    for zgy__ltsm, blb__xtsdl in uqrus__pxafz.items():
        pml__zsw = {}
        if blb__xtsdl.fget:
            pml__zsw['get'] = bodo.jit(blb__xtsdl.fget)
        if blb__xtsdl.fset:
            pml__zsw['set'] = bodo.jit(blb__xtsdl.fset)
        jit_props[zgy__ltsm] = pml__zsw
    jit_static_methods = {zgy__ltsm: bodo.jit(blb__xtsdl.__func__) for 
        zgy__ltsm, blb__xtsdl in beguu__gsg.items()}
    vmspj__zoe = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    zok__lhh = dict(class_type=vmspj__zoe, __doc__=qdzap__vyemf)
    zok__lhh.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), zok__lhh)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, vmspj__zoe)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(vmspj__zoe, typingctx, targetctx).register()
    as_numba_type.register(cls, vmspj__zoe.instance_type)
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
    qucz__zsc = ','.join('{0}:{1}'.format(zgy__ltsm, blb__xtsdl) for 
        zgy__ltsm, blb__xtsdl in struct.items())
    wuuk__qzd = ','.join('{0}:{1}'.format(zgy__ltsm, blb__xtsdl) for 
        zgy__ltsm, blb__xtsdl in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), qucz__zsc, wuuk__qzd)
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
    eko__bjo = numba.core.typeinfer.fold_arg_vars(typevars, self.args, self
        .vararg, self.kws)
    if eko__bjo is None:
        return
    oxlck__ryg, ltofh__mdbr = eko__bjo
    for a in itertools.chain(oxlck__ryg, ltofh__mdbr.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, oxlck__ryg, ltofh__mdbr)
    except ForceLiteralArg as e:
        caddb__whmj = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(caddb__whmj, self.kws)
        mgngv__wlsgd = set()
        yyxwm__rqrwz = set()
        rdoo__bzx = {}
        for jsmgc__mhu in e.requested_args:
            bjwyk__kpraf = typeinfer.func_ir.get_definition(folded[jsmgc__mhu])
            if isinstance(bjwyk__kpraf, ir.Arg):
                mgngv__wlsgd.add(bjwyk__kpraf.index)
                if bjwyk__kpraf.index in e.file_infos:
                    rdoo__bzx[bjwyk__kpraf.index] = e.file_infos[bjwyk__kpraf
                        .index]
            else:
                yyxwm__rqrwz.add(jsmgc__mhu)
        if yyxwm__rqrwz:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif mgngv__wlsgd:
            raise ForceLiteralArg(mgngv__wlsgd, loc=self.loc, file_infos=
                rdoo__bzx)
    if sig is None:
        ejd__qdsk = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in oxlck__ryg]
        args += [('%s=%s' % (zgy__ltsm, blb__xtsdl)) for zgy__ltsm,
            blb__xtsdl in sorted(ltofh__mdbr.items())]
        ifqm__ncqey = ejd__qdsk.format(fnty, ', '.join(map(str, args)))
        cixdy__jvo = context.explain_function_type(fnty)
        msg = '\n'.join([ifqm__ncqey, cixdy__jvo])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        wad__idncc = context.unify_pairs(sig.recvr, fnty.this)
        if wad__idncc is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if wad__idncc is not None and wad__idncc.is_precise():
            cliq__pdk = fnty.copy(this=wad__idncc)
            typeinfer.propagate_refined_type(self.func, cliq__pdk)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            gwn__lru = target.getone()
            if context.unify_pairs(gwn__lru, sig.return_type) == gwn__lru:
                sig = sig.replace(return_type=gwn__lru)
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
        xgjxt__ultm = '*other* must be a {} but got a {} instead'
        raise TypeError(xgjxt__ultm.format(ForceLiteralArg, type(other)))
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
    ncr__uowhz = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for zgy__ltsm, blb__xtsdl in kwargs.items():
        bla__aotrl = None
        try:
            yaq__fru = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var(
                'dummy'), loc)
            func_ir._definitions[yaq__fru.name] = [blb__xtsdl]
            bla__aotrl = get_const_value_inner(func_ir, yaq__fru)
            func_ir._definitions.pop(yaq__fru.name)
            if isinstance(bla__aotrl, str):
                bla__aotrl = sigutils._parse_signature_string(bla__aotrl)
            if isinstance(bla__aotrl, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {zgy__ltsm} is annotated as type class {bla__aotrl}."""
                    )
            assert isinstance(bla__aotrl, types.Type)
            if isinstance(bla__aotrl, (types.List, types.Set)):
                bla__aotrl = bla__aotrl.copy(reflected=False)
            ncr__uowhz[zgy__ltsm] = bla__aotrl
        except BodoError as ymrfa__ohccg:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(bla__aotrl, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(blb__xtsdl, ir.Global):
                    msg = f'Global {blb__xtsdl.name!r} is not defined.'
                if isinstance(blb__xtsdl, ir.FreeVar):
                    msg = f'Freevar {blb__xtsdl.name!r} is not defined.'
            if isinstance(blb__xtsdl, ir.Expr) and blb__xtsdl.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=zgy__ltsm, msg=msg, loc=loc)
    for name, typ in ncr__uowhz.items():
        self._legalize_arg_type(name, typ, loc)
    return ncr__uowhz


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
    drjh__zeg = inst.arg
    assert drjh__zeg > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(drjh__zeg)]))
    tmps = [state.make_temp() for _ in range(drjh__zeg - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    azowv__jloba = ir.Global('format', format, loc=self.loc)
    self.store(value=azowv__jloba, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    ozn__rzlyx = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=ozn__rzlyx, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    drjh__zeg = inst.arg
    assert drjh__zeg > 0, 'invalid BUILD_STRING count'
    akwwx__hydhh = self.get(strings[0])
    for other, vvoxh__vepqi in zip(strings[1:], tmps):
        other = self.get(other)
        zjlkv__ldhq = ir.Expr.binop(operator.add, lhs=akwwx__hydhh, rhs=
            other, loc=self.loc)
        self.store(zjlkv__ldhq, vvoxh__vepqi)
        akwwx__hydhh = self.get(vvoxh__vepqi)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    tdpzh__kngt = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, tdpzh__kngt])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    ssg__gja = mk_unique_var(f'{var_name}')
    zdwo__hxfg = ssg__gja.replace('<', '_').replace('>', '_')
    zdwo__hxfg = zdwo__hxfg.replace('.', '_').replace('$', '_v')
    return zdwo__hxfg


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
                nohvs__bubha = get_overload_const_str(val2)
                if nohvs__bubha != 'ns':
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
        kotr__csvxi = states['defmap']
        if len(kotr__csvxi) == 0:
            nzeh__cpra = assign.target
            numba.core.ssa._logger.debug('first assign: %s', nzeh__cpra)
            if nzeh__cpra.name not in scope.localvars:
                nzeh__cpra = scope.define(assign.target.name, loc=assign.loc)
        else:
            nzeh__cpra = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=nzeh__cpra, value=assign.value, loc=
            assign.loc)
        kotr__csvxi[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    mly__kenjt = []
    for zgy__ltsm, blb__xtsdl in typing.npydecl.registry.globals:
        if zgy__ltsm == func:
            mly__kenjt.append(blb__xtsdl)
    for zgy__ltsm, blb__xtsdl in typing.templates.builtin_registry.globals:
        if zgy__ltsm == func:
            mly__kenjt.append(blb__xtsdl)
    if len(mly__kenjt) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return mly__kenjt


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    qdtu__rsa = {}
    gkx__xawbk = find_topo_order(blocks)
    jkffh__zei = {}
    for ymvls__gebgc in gkx__xawbk:
        block = blocks[ymvls__gebgc]
        fiuhi__lym = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                qxip__hpcph = stmt.target.name
                bjpbh__oyutl = stmt.value
                if (bjpbh__oyutl.op == 'getattr' and bjpbh__oyutl.attr in
                    arr_math and isinstance(typemap[bjpbh__oyutl.value.name
                    ], types.npytypes.Array)):
                    bjpbh__oyutl = stmt.value
                    giapu__mdfc = bjpbh__oyutl.value
                    qdtu__rsa[qxip__hpcph] = giapu__mdfc
                    scope = giapu__mdfc.scope
                    loc = giapu__mdfc.loc
                    izslx__inaad = ir.Var(scope, mk_unique_var('$np_g_var'),
                        loc)
                    typemap[izslx__inaad.name] = types.misc.Module(numpy)
                    akajb__yzr = ir.Global('np', numpy, loc)
                    loas__njft = ir.Assign(akajb__yzr, izslx__inaad, loc)
                    bjpbh__oyutl.value = izslx__inaad
                    fiuhi__lym.append(loas__njft)
                    func_ir._definitions[izslx__inaad.name] = [akajb__yzr]
                    func = getattr(numpy, bjpbh__oyutl.attr)
                    zigdz__yhvvy = get_np_ufunc_typ_lst(func)
                    jkffh__zei[qxip__hpcph] = zigdz__yhvvy
                if (bjpbh__oyutl.op == 'call' and bjpbh__oyutl.func.name in
                    qdtu__rsa):
                    giapu__mdfc = qdtu__rsa[bjpbh__oyutl.func.name]
                    inrk__botgx = calltypes.pop(bjpbh__oyutl)
                    fmavv__shrv = inrk__botgx.args[:len(bjpbh__oyutl.args)]
                    ozzm__bfo = {name: typemap[blb__xtsdl.name] for name,
                        blb__xtsdl in bjpbh__oyutl.kws}
                    luoa__qrhfl = jkffh__zei[bjpbh__oyutl.func.name]
                    qqt__cca = None
                    for mms__jjpb in luoa__qrhfl:
                        try:
                            qqt__cca = mms__jjpb.get_call_type(typingctx, [
                                typemap[giapu__mdfc.name]] + list(
                                fmavv__shrv), ozzm__bfo)
                            typemap.pop(bjpbh__oyutl.func.name)
                            typemap[bjpbh__oyutl.func.name] = mms__jjpb
                            calltypes[bjpbh__oyutl] = qqt__cca
                            break
                        except Exception as ymrfa__ohccg:
                            pass
                    if qqt__cca is None:
                        raise TypeError(
                            f'No valid template found for {bjpbh__oyutl.func.name}'
                            )
                    bjpbh__oyutl.args = [giapu__mdfc] + bjpbh__oyutl.args
            fiuhi__lym.append(stmt)
        block.body = fiuhi__lym


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    hmcj__btjlz = ufunc.nin
    dfy__fxu = ufunc.nout
    hlqqr__nhe = ufunc.nargs
    assert hlqqr__nhe == hmcj__btjlz + dfy__fxu
    if len(args) < hmcj__btjlz:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            hmcj__btjlz))
    if len(args) > hlqqr__nhe:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), hlqqr__nhe)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    ebgj__obo = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    nmni__afux = max(ebgj__obo)
    lnlsl__fcu = args[hmcj__btjlz:]
    if not all(d == nmni__afux for d in ebgj__obo[hmcj__btjlz:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(ckwq__uefh, types.ArrayCompatible) and not
        isinstance(ckwq__uefh, types.Bytes) for ckwq__uefh in lnlsl__fcu):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(ckwq__uefh.mutable for ckwq__uefh in lnlsl__fcu):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    ytacp__aqzmo = [(x.dtype if isinstance(x, types.ArrayCompatible) and 
        not isinstance(x, types.Bytes) else x) for x in args]
    qnqp__snndn = None
    if nmni__afux > 0 and len(lnlsl__fcu) < ufunc.nout:
        qnqp__snndn = 'C'
        kyqsf__ptpzy = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in kyqsf__ptpzy and 'F' in kyqsf__ptpzy:
            qnqp__snndn = 'F'
    return ytacp__aqzmo, lnlsl__fcu, nmni__afux, qnqp__snndn


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
        ajbs__dqpw = 'Dict.key_type cannot be of type {}'
        raise TypingError(ajbs__dqpw.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        ajbs__dqpw = 'Dict.value_type cannot be of type {}'
        raise TypingError(ajbs__dqpw.format(valty))
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
    vzar__gbo = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[vzar__gbo]
        return impl, args
    except KeyError as ymrfa__ohccg:
        pass
    impl, args = self._build_impl(vzar__gbo, args, kws)
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
        lav__fksq = find_topo_order(parfor.loop_body)
    zzgu__xyjs = lav__fksq[0]
    noeb__uso = {}
    _update_parfor_get_setitems(parfor.loop_body[zzgu__xyjs].body, parfor.
        index_var, alias_map, noeb__uso, lives_n_aliases)
    fdvqs__dxsre = set(noeb__uso.keys())
    for axjrb__iyrpr in lav__fksq:
        if axjrb__iyrpr == zzgu__xyjs:
            continue
        for stmt in parfor.loop_body[axjrb__iyrpr].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            ciaq__wkxk = set(blb__xtsdl.name for blb__xtsdl in stmt.list_vars()
                )
            ylo__oql = ciaq__wkxk & fdvqs__dxsre
            for a in ylo__oql:
                noeb__uso.pop(a, None)
    for axjrb__iyrpr in lav__fksq:
        if axjrb__iyrpr == zzgu__xyjs:
            continue
        block = parfor.loop_body[axjrb__iyrpr]
        ftye__eckp = noeb__uso.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            ftye__eckp, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    ewo__fdi = max(blocks.keys())
    vbqf__nlbw, bro__pgzhu = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    vnzse__iyb = ir.Jump(vbqf__nlbw, ir.Loc('parfors_dummy', -1))
    blocks[ewo__fdi].body.append(vnzse__iyb)
    hgivg__tun = compute_cfg_from_blocks(blocks)
    qez__jfygy = compute_use_defs(blocks)
    cgioc__lxih = compute_live_map(hgivg__tun, blocks, qez__jfygy.usemap,
        qez__jfygy.defmap)
    alias_set = set(alias_map.keys())
    for ymvls__gebgc, block in blocks.items():
        fiuhi__lym = []
        tvsz__vkyg = {blb__xtsdl.name for blb__xtsdl in block.terminator.
            list_vars()}
        for tax__xril, bhh__xjnhm in hgivg__tun.successors(ymvls__gebgc):
            tvsz__vkyg |= cgioc__lxih[tax__xril]
        for stmt in reversed(block.body):
            rnr__jozo = tvsz__vkyg & alias_set
            for blb__xtsdl in rnr__jozo:
                tvsz__vkyg |= alias_map[blb__xtsdl]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in tvsz__vkyg and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                rft__ongjy = guard(find_callname, func_ir, stmt.value)
                if rft__ongjy == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in tvsz__vkyg and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            tvsz__vkyg |= {blb__xtsdl.name for blb__xtsdl in stmt.list_vars()}
            fiuhi__lym.append(stmt)
        fiuhi__lym.reverse()
        block.body = fiuhi__lym
    typemap.pop(bro__pgzhu.name)
    blocks[ewo__fdi].body.pop()

    def trim_empty_parfor_branches(parfor):
        wze__vfg = False
        blocks = parfor.loop_body.copy()
        for ymvls__gebgc, block in blocks.items():
            if len(block.body):
                llj__ato = block.body[-1]
                if isinstance(llj__ato, ir.Branch):
                    if len(blocks[llj__ato.truebr].body) == 1 and len(blocks
                        [llj__ato.falsebr].body) == 1:
                        rzrwz__rar = blocks[llj__ato.truebr].body[0]
                        lcmjj__xrw = blocks[llj__ato.falsebr].body[0]
                        if isinstance(rzrwz__rar, ir.Jump) and isinstance(
                            lcmjj__xrw, ir.Jump
                            ) and rzrwz__rar.target == lcmjj__xrw.target:
                            parfor.loop_body[ymvls__gebgc].body[-1] = ir.Jump(
                                rzrwz__rar.target, llj__ato.loc)
                            wze__vfg = True
                    elif len(blocks[llj__ato.truebr].body) == 1:
                        rzrwz__rar = blocks[llj__ato.truebr].body[0]
                        if isinstance(rzrwz__rar, ir.Jump
                            ) and rzrwz__rar.target == llj__ato.falsebr:
                            parfor.loop_body[ymvls__gebgc].body[-1] = ir.Jump(
                                rzrwz__rar.target, llj__ato.loc)
                            wze__vfg = True
                    elif len(blocks[llj__ato.falsebr].body) == 1:
                        lcmjj__xrw = blocks[llj__ato.falsebr].body[0]
                        if isinstance(lcmjj__xrw, ir.Jump
                            ) and lcmjj__xrw.target == llj__ato.truebr:
                            parfor.loop_body[ymvls__gebgc].body[-1] = ir.Jump(
                                lcmjj__xrw.target, llj__ato.loc)
                            wze__vfg = True
        return wze__vfg
    wze__vfg = True
    while wze__vfg:
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
        wze__vfg = trim_empty_parfor_branches(parfor)
    eeh__yfk = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        eeh__yfk &= len(block.body) == 0
    if eeh__yfk:
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
    pqi__xkeh = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                pqi__xkeh += 1
                parfor = stmt
                onqcc__uzsg = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = onqcc__uzsg.scope
                loc = ir.Loc('parfors_dummy', -1)
                xse__yga = ir.Var(scope, mk_unique_var('$const'), loc)
                onqcc__uzsg.body.append(ir.Assign(ir.Const(0, loc),
                    xse__yga, loc))
                onqcc__uzsg.body.append(ir.Return(xse__yga, loc))
                hgivg__tun = compute_cfg_from_blocks(parfor.loop_body)
                for pjbak__fbah in hgivg__tun.dead_nodes():
                    del parfor.loop_body[pjbak__fbah]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                onqcc__uzsg = parfor.loop_body[max(parfor.loop_body.keys())]
                onqcc__uzsg.body.pop()
                onqcc__uzsg.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return pqi__xkeh


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
            eib__zsm = self.overloads.get(tuple(args))
            if eib__zsm is not None:
                return eib__zsm.entry_point
            self._pre_compile(args, return_type, flags)
            bllc__ctka = self.func_ir
            lrtd__soejv = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=lrtd__soejv):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=bllc__ctka, args=args,
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
        omctu__iryh = copy.deepcopy(flags)
        omctu__iryh.no_rewrites = True

        def compile_local(the_ir, the_flags):
            dfhi__fbzt = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return dfhi__fbzt.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        uits__aqqb = compile_local(func_ir, omctu__iryh)
        joj__cczxl = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    joj__cczxl = compile_local(func_ir, flags)
                except Exception as ymrfa__ohccg:
                    pass
        if joj__cczxl is not None:
            cres = joj__cczxl
        else:
            cres = uits__aqqb
        return cres
    else:
        dfhi__fbzt = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return dfhi__fbzt.compile_ir(func_ir=func_ir, lifted=lifted,
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
    hijr__tyrls = self.get_data_type(typ.dtype)
    ocy__gig = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        ocy__gig):
        dqenz__dqup = ary.ctypes.data
        ewk__ipwwb = self.add_dynamic_addr(builder, dqenz__dqup, info=str(
            type(dqenz__dqup)))
        blqhr__etl = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        iyt__mzkz = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            iyt__mzkz = iyt__mzkz.view('int64')
        val = bytearray(iyt__mzkz.data)
        neek__crjq = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        ewk__ipwwb = cgutils.global_constant(builder, '.const.array.data',
            neek__crjq)
        ewk__ipwwb.align = self.get_abi_alignment(hijr__tyrls)
        blqhr__etl = None
    eymy__oxe = self.get_value_type(types.intp)
    ndwt__ydlk = [self.get_constant(types.intp, jpeao__ocu) for jpeao__ocu in
        ary.shape]
    kldj__fuvkk = lir.Constant(lir.ArrayType(eymy__oxe, len(ndwt__ydlk)),
        ndwt__ydlk)
    svg__eyv = [self.get_constant(types.intp, jpeao__ocu) for jpeao__ocu in
        ary.strides]
    oifwj__sxuz = lir.Constant(lir.ArrayType(eymy__oxe, len(svg__eyv)),
        svg__eyv)
    ihtqs__mlse = self.get_constant(types.intp, ary.dtype.itemsize)
    hoplc__hwfe = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        hoplc__hwfe, ihtqs__mlse, ewk__ipwwb.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), kldj__fuvkk, oifwj__sxuz])


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
    vniaz__dggyh = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    rmac__bqbl = lir.Function(module, vniaz__dggyh, name='nrt_atomic_{0}'.
        format(op))
    [htp__zvg] = rmac__bqbl.args
    afv__zjw = rmac__bqbl.append_basic_block()
    builder = lir.IRBuilder(afv__zjw)
    wdzrl__jgeod = lir.Constant(_word_type, 1)
    if False:
        lepy__omk = builder.atomic_rmw(op, htp__zvg, wdzrl__jgeod, ordering
            =ordering)
        res = getattr(builder, op)(lepy__omk, wdzrl__jgeod)
        builder.ret(res)
    else:
        lepy__omk = builder.load(htp__zvg)
        fqu__vlfjt = getattr(builder, op)(lepy__omk, wdzrl__jgeod)
        ykksc__wtas = builder.icmp_signed('!=', lepy__omk, lir.Constant(
            lepy__omk.type, -1))
        with cgutils.if_likely(builder, ykksc__wtas):
            builder.store(fqu__vlfjt, htp__zvg)
        builder.ret(fqu__vlfjt)
    return rmac__bqbl


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
        oefyi__bbc = state.targetctx.codegen()
        state.library = oefyi__bbc.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    htat__vgrpa = state.func_ir
    typemap = state.typemap
    muh__qgvq = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    siga__fhlpb = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            htat__vgrpa, typemap, muh__qgvq, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            qkifk__ujfz = lowering.Lower(targetctx, library, fndesc,
                htat__vgrpa, metadata=metadata)
            qkifk__ujfz.lower()
            if not flags.no_cpython_wrapper:
                qkifk__ujfz.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(muh__qgvq, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        qkifk__ujfz.create_cfunc_wrapper()
            env = qkifk__ujfz.env
            szag__lah = qkifk__ujfz.call_helper
            del qkifk__ujfz
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, szag__lah, cfunc=None, env=env)
        else:
            rcqsi__qwnlk = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(rcqsi__qwnlk, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, szag__lah, cfunc=
                rcqsi__qwnlk, env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        uucop__xyk = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = uucop__xyk - siga__fhlpb
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
        uqe__aru = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, uqe__aru), likely
            =False):
            c.builder.store(cgutils.true_bit, errorptr)
            eplfg__fte.do_break()
        brjlc__tvanr = c.builder.icmp_signed('!=', uqe__aru, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(brjlc__tvanr, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, uqe__aru)
                c.pyapi.decref(uqe__aru)
                eplfg__fte.do_break()
        c.pyapi.decref(uqe__aru)
    aao__nymmk, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(aao__nymmk, likely=True) as (hspui__qsplo,
        onbj__uwhd):
        with hspui__qsplo:
            list.size = size
            jpipl__hgila = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                jpipl__hgila), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        jpipl__hgila))
                    with cgutils.for_range(c.builder, size) as eplfg__fte:
                        itemobj = c.pyapi.list_getitem(obj, eplfg__fte.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        wrk__obi = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(wrk__obi.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            eplfg__fte.do_break()
                        list.setitem(eplfg__fte.index, wrk__obi.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with onbj__uwhd:
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
    nyj__cyf, zxmud__nwg, sbmg__bvwhu, vhbzq__njbt, trana__xdd = (
        compile_time_get_string_data(literal_string))
    vxg__bgrqc = builder.module
    gv = context.insert_const_bytes(vxg__bgrqc, nyj__cyf)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        zxmud__nwg), context.get_constant(types.int32, sbmg__bvwhu),
        context.get_constant(types.uint32, vhbzq__njbt), context.
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
    xhb__jbpp = None
    if isinstance(shape, types.Integer):
        xhb__jbpp = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(jpeao__ocu, (types.Integer, types.IntEnumMember)) for
            jpeao__ocu in shape):
            xhb__jbpp = len(shape)
    return xhb__jbpp


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
            xhb__jbpp = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if xhb__jbpp == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(xhb__jbpp))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            opy__xog = self._get_names(x)
            if len(opy__xog) != 0:
                return opy__xog[0]
            return opy__xog
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    opy__xog = self._get_names(obj)
    if len(opy__xog) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(opy__xog[0])


def get_equiv_set(self, obj):
    opy__xog = self._get_names(obj)
    if len(opy__xog) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(opy__xog[0])


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
    nsnd__lce = []
    for zfio__htwck in func_ir.arg_names:
        if zfio__htwck in typemap and isinstance(typemap[zfio__htwck],
            types.containers.UniTuple) and typemap[zfio__htwck].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(zfio__htwck))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for fewt__idfcx in func_ir.blocks.values():
        for stmt in fewt__idfcx.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    kksge__pwk = getattr(val, 'code', None)
                    if kksge__pwk is not None:
                        if getattr(val, 'closure', None) is not None:
                            lzqyd__lxk = '<creating a function from a closure>'
                            zjlkv__ldhq = ''
                        else:
                            lzqyd__lxk = kksge__pwk.co_name
                            zjlkv__ldhq = '(%s) ' % lzqyd__lxk
                    else:
                        lzqyd__lxk = '<could not ascertain use case>'
                        zjlkv__ldhq = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (lzqyd__lxk, zjlkv__ldhq))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                tgec__xrs = False
                if isinstance(val, pytypes.FunctionType):
                    tgec__xrs = val in {numba.gdb, numba.gdb_init}
                if not tgec__xrs:
                    tgec__xrs = getattr(val, '_name', '') == 'gdb_internal'
                if tgec__xrs:
                    nsnd__lce.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    rizl__ugkji = func_ir.get_definition(var)
                    rbp__oyxn = guard(find_callname, func_ir, rizl__ugkji)
                    if rbp__oyxn and rbp__oyxn[1] == 'numpy':
                        ty = getattr(numpy, rbp__oyxn[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    olmp__jsp = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(olmp__jsp), loc=stmt.loc)
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
    if len(nsnd__lce) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        iqxr__hjy = '\n'.join([x.strformat() for x in nsnd__lce])
        raise errors.UnsupportedError(msg % iqxr__hjy)


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
    zgy__ltsm, blb__xtsdl = next(iter(val.items()))
    ohk__roav = typeof_impl(zgy__ltsm, c)
    gwtx__fhzx = typeof_impl(blb__xtsdl, c)
    if ohk__roav is None or gwtx__fhzx is None:
        raise ValueError(
            f'Cannot type dict element type {type(zgy__ltsm)}, {type(blb__xtsdl)}'
            )
    return types.DictType(ohk__roav, gwtx__fhzx)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    joki__puwhe = cgutils.alloca_once_value(c.builder, val)
    jinf__hxmud = c.pyapi.object_hasattr_string(val, '_opaque')
    hptnp__vdqc = c.builder.icmp_unsigned('==', jinf__hxmud, lir.Constant(
        jinf__hxmud.type, 0))
    qkto__hqeua = typ.key_type
    mdor__vni = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(qkto__hqeua, mdor__vni)

    def copy_dict(out_dict, in_dict):
        for zgy__ltsm, blb__xtsdl in in_dict.items():
            out_dict[zgy__ltsm] = blb__xtsdl
    with c.builder.if_then(hptnp__vdqc):
        flwwx__alr = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        ufx__wpeo = c.pyapi.call_function_objargs(flwwx__alr, [])
        txvcl__aun = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(txvcl__aun, [ufx__wpeo, val])
        c.builder.store(ufx__wpeo, joki__puwhe)
    val = c.builder.load(joki__puwhe)
    pva__nos = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    bri__ocjtv = c.pyapi.object_type(val)
    afelr__eeop = c.builder.icmp_unsigned('==', bri__ocjtv, pva__nos)
    with c.builder.if_else(afelr__eeop) as (dzsir__wrqa, ikioh__oawwh):
        with dzsir__wrqa:
            hjet__vmkh = c.pyapi.object_getattr_string(val, '_opaque')
            vtul__uqtmf = types.MemInfoPointer(types.voidptr)
            wrk__obi = c.unbox(vtul__uqtmf, hjet__vmkh)
            mi = wrk__obi.value
            kibs__fch = vtul__uqtmf, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *kibs__fch)
            xbg__cyyqs = context.get_constant_null(kibs__fch[1])
            args = mi, xbg__cyyqs
            dotm__ojjfx, lipou__qxfwk = c.pyapi.call_jit_code(convert, sig,
                args)
            c.context.nrt.decref(c.builder, typ, lipou__qxfwk)
            c.pyapi.decref(hjet__vmkh)
            lnsvb__wdeal = c.builder.basic_block
        with ikioh__oawwh:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", bri__ocjtv, pva__nos)
            hhrkt__bowsq = c.builder.basic_block
    ksu__tou = c.builder.phi(lipou__qxfwk.type)
    rny__qqwk = c.builder.phi(dotm__ojjfx.type)
    ksu__tou.add_incoming(lipou__qxfwk, lnsvb__wdeal)
    ksu__tou.add_incoming(lipou__qxfwk.type(None), hhrkt__bowsq)
    rny__qqwk.add_incoming(dotm__ojjfx, lnsvb__wdeal)
    rny__qqwk.add_incoming(cgutils.true_bit, hhrkt__bowsq)
    c.pyapi.decref(pva__nos)
    c.pyapi.decref(bri__ocjtv)
    with c.builder.if_then(hptnp__vdqc):
        c.pyapi.decref(val)
    return NativeValue(ksu__tou, is_error=rny__qqwk)


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
    vuqij__zukbj = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=vuqij__zukbj, name=updatevar)
    iry__gkeai = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=iry__gkeai, name=res)


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
        for zgy__ltsm, blb__xtsdl in other.items():
            d[zgy__ltsm] = blb__xtsdl
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
    zjlkv__ldhq = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(zjlkv__ldhq, res)


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
    bmk__bhqxq = PassManager(name)
    if state.func_ir is None:
        bmk__bhqxq.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            bmk__bhqxq.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        bmk__bhqxq.add_pass(FixupArgs, 'fix up args')
    bmk__bhqxq.add_pass(IRProcessing, 'processing IR')
    bmk__bhqxq.add_pass(WithLifting, 'Handle with contexts')
    bmk__bhqxq.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        bmk__bhqxq.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        bmk__bhqxq.add_pass(DeadBranchPrune, 'dead branch pruning')
        bmk__bhqxq.add_pass(GenericRewrites, 'nopython rewrites')
    bmk__bhqxq.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    bmk__bhqxq.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        bmk__bhqxq.add_pass(DeadBranchPrune, 'dead branch pruning')
    bmk__bhqxq.add_pass(FindLiterallyCalls, 'find literally calls')
    bmk__bhqxq.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        bmk__bhqxq.add_pass(ReconstructSSA, 'ssa')
    bmk__bhqxq.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    bmk__bhqxq.finalize()
    return bmk__bhqxq


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
    a, hbxaj__hhuqy = args
    if isinstance(a, types.List) and isinstance(hbxaj__hhuqy, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(hbxaj__hhuqy, types.List):
        return signature(hbxaj__hhuqy, types.intp, hbxaj__hhuqy)


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
        cdzhs__fub, mchwh__crpkl = 0, 1
    else:
        cdzhs__fub, mchwh__crpkl = 1, 0
    gtzqa__pqfrr = ListInstance(context, builder, sig.args[cdzhs__fub],
        args[cdzhs__fub])
    ajjvq__rxci = gtzqa__pqfrr.size
    emyc__erj = args[mchwh__crpkl]
    jpipl__hgila = lir.Constant(emyc__erj.type, 0)
    emyc__erj = builder.select(cgutils.is_neg_int(builder, emyc__erj),
        jpipl__hgila, emyc__erj)
    hoplc__hwfe = builder.mul(emyc__erj, ajjvq__rxci)
    ydbh__zaxm = ListInstance.allocate(context, builder, sig.return_type,
        hoplc__hwfe)
    ydbh__zaxm.size = hoplc__hwfe
    with cgutils.for_range_slice(builder, jpipl__hgila, hoplc__hwfe,
        ajjvq__rxci, inc=True) as (slev__eayz, _):
        with cgutils.for_range(builder, ajjvq__rxci) as eplfg__fte:
            value = gtzqa__pqfrr.getitem(eplfg__fte.index)
            ydbh__zaxm.setitem(builder.add(eplfg__fte.index, slev__eayz),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, ydbh__zaxm.value
        )


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
    hhwjg__ime = first.unify(self, second)
    if hhwjg__ime is not None:
        return hhwjg__ime
    hhwjg__ime = second.unify(self, first)
    if hhwjg__ime is not None:
        return hhwjg__ime
    splvu__zmk = self.can_convert(fromty=first, toty=second)
    if splvu__zmk is not None and splvu__zmk <= Conversion.safe:
        return second
    splvu__zmk = self.can_convert(fromty=second, toty=first)
    if splvu__zmk is not None and splvu__zmk <= Conversion.safe:
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
    hoplc__hwfe = payload.used
    listobj = c.pyapi.list_new(hoplc__hwfe)
    aao__nymmk = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(aao__nymmk, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(
            hoplc__hwfe.type, 0))
        with payload._iterate() as eplfg__fte:
            i = c.builder.load(index)
            item = eplfg__fte.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return aao__nymmk, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    sre__uxp = h.type
    qcm__ajb = self.mask
    dtype = self._ty.dtype
    vvdy__frk = context.typing_context
    fnty = vvdy__frk.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(vvdy__frk, (dtype, dtype), {})
    eiv__wkau = context.get_function(fnty, sig)
    mymov__dju = ir.Constant(sre__uxp, 1)
    durea__ejdrb = ir.Constant(sre__uxp, 5)
    njx__izo = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, qcm__ajb))
    if for_insert:
        khsb__xdqb = qcm__ajb.type(-1)
        xxp__ngmut = cgutils.alloca_once_value(builder, khsb__xdqb)
    cguti__iby = builder.append_basic_block('lookup.body')
    mnftj__ewjrb = builder.append_basic_block('lookup.found')
    hgg__jidy = builder.append_basic_block('lookup.not_found')
    ebbxg__cfnd = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        yph__wqsnm = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, yph__wqsnm)):
            jmrpb__ozwiv = eiv__wkau(builder, (item, entry.key))
            with builder.if_then(jmrpb__ozwiv):
                builder.branch(mnftj__ewjrb)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, yph__wqsnm)):
            builder.branch(hgg__jidy)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, yph__wqsnm)):
                dgo__xqu = builder.load(xxp__ngmut)
                dgo__xqu = builder.select(builder.icmp_unsigned('==',
                    dgo__xqu, khsb__xdqb), i, dgo__xqu)
                builder.store(dgo__xqu, xxp__ngmut)
    with cgutils.for_range(builder, ir.Constant(sre__uxp, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, mymov__dju)
        i = builder.and_(i, qcm__ajb)
        builder.store(i, index)
    builder.branch(cguti__iby)
    with builder.goto_block(cguti__iby):
        i = builder.load(index)
        check_entry(i)
        zwqam__lug = builder.load(njx__izo)
        zwqam__lug = builder.lshr(zwqam__lug, durea__ejdrb)
        i = builder.add(mymov__dju, builder.mul(i, durea__ejdrb))
        i = builder.and_(qcm__ajb, builder.add(i, zwqam__lug))
        builder.store(i, index)
        builder.store(zwqam__lug, njx__izo)
        builder.branch(cguti__iby)
    with builder.goto_block(hgg__jidy):
        if for_insert:
            i = builder.load(index)
            dgo__xqu = builder.load(xxp__ngmut)
            i = builder.select(builder.icmp_unsigned('==', dgo__xqu,
                khsb__xdqb), i, dgo__xqu)
            builder.store(i, index)
        builder.branch(ebbxg__cfnd)
    with builder.goto_block(mnftj__ewjrb):
        builder.branch(ebbxg__cfnd)
    builder.position_at_end(ebbxg__cfnd)
    tgec__xrs = builder.phi(ir.IntType(1), 'found')
    tgec__xrs.add_incoming(cgutils.true_bit, mnftj__ewjrb)
    tgec__xrs.add_incoming(cgutils.false_bit, hgg__jidy)
    return tgec__xrs, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    yuwc__prpvn = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    mwh__moegv = payload.used
    mymov__dju = ir.Constant(mwh__moegv.type, 1)
    mwh__moegv = payload.used = builder.add(mwh__moegv, mymov__dju)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, yuwc__prpvn), likely=True):
        payload.fill = builder.add(payload.fill, mymov__dju)
    if do_resize:
        self.upsize(mwh__moegv)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    tgec__xrs, i = payload._lookup(item, h, for_insert=True)
    qaf__xtqv = builder.not_(tgec__xrs)
    with builder.if_then(qaf__xtqv):
        entry = payload.get_entry(i)
        yuwc__prpvn = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        mwh__moegv = payload.used
        mymov__dju = ir.Constant(mwh__moegv.type, 1)
        mwh__moegv = payload.used = builder.add(mwh__moegv, mymov__dju)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, yuwc__prpvn), likely=True):
            payload.fill = builder.add(payload.fill, mymov__dju)
        if do_resize:
            self.upsize(mwh__moegv)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    mwh__moegv = payload.used
    mymov__dju = ir.Constant(mwh__moegv.type, 1)
    mwh__moegv = payload.used = self._builder.sub(mwh__moegv, mymov__dju)
    if do_resize:
        self.downsize(mwh__moegv)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    vgl__ruik = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, vgl__ruik)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    ippsr__vmbjg = payload
    aao__nymmk = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(aao__nymmk), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with ippsr__vmbjg._iterate() as eplfg__fte:
        entry = eplfg__fte.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(ippsr__vmbjg.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as eplfg__fte:
        entry = eplfg__fte.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    aao__nymmk = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(aao__nymmk), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    aao__nymmk = cgutils.alloca_once_value(builder, cgutils.true_bit)
    sre__uxp = context.get_value_type(types.intp)
    jpipl__hgila = ir.Constant(sre__uxp, 0)
    mymov__dju = ir.Constant(sre__uxp, 1)
    hyb__uwwq = context.get_data_type(types.SetPayload(self._ty))
    lor__leh = context.get_abi_sizeof(hyb__uwwq)
    qxv__zin = self._entrysize
    lor__leh -= qxv__zin
    qsvaw__ofxrs, ketsw__mcg = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(sre__uxp, qxv__zin), ir.Constant(sre__uxp,
        lor__leh))
    with builder.if_then(ketsw__mcg, likely=False):
        builder.store(cgutils.false_bit, aao__nymmk)
    with builder.if_then(builder.load(aao__nymmk), likely=True):
        if realloc:
            ledx__psef = self._set.meminfo
            htp__zvg = context.nrt.meminfo_varsize_alloc(builder,
                ledx__psef, size=qsvaw__ofxrs)
            zgm__que = cgutils.is_null(builder, htp__zvg)
        else:
            jrix__kvxz = _imp_dtor(context, builder.module, self._ty)
            ledx__psef = context.nrt.meminfo_new_varsize_dtor(builder,
                qsvaw__ofxrs, builder.bitcast(jrix__kvxz, cgutils.voidptr_t))
            zgm__que = cgutils.is_null(builder, ledx__psef)
        with builder.if_else(zgm__que, likely=False) as (azo__okpkg,
            hspui__qsplo):
            with azo__okpkg:
                builder.store(cgutils.false_bit, aao__nymmk)
            with hspui__qsplo:
                if not realloc:
                    self._set.meminfo = ledx__psef
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, qsvaw__ofxrs, 255)
                payload.used = jpipl__hgila
                payload.fill = jpipl__hgila
                payload.finger = jpipl__hgila
                wmna__luz = builder.sub(nentries, mymov__dju)
                payload.mask = wmna__luz
    return builder.load(aao__nymmk)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    aao__nymmk = cgutils.alloca_once_value(builder, cgutils.true_bit)
    sre__uxp = context.get_value_type(types.intp)
    jpipl__hgila = ir.Constant(sre__uxp, 0)
    mymov__dju = ir.Constant(sre__uxp, 1)
    hyb__uwwq = context.get_data_type(types.SetPayload(self._ty))
    lor__leh = context.get_abi_sizeof(hyb__uwwq)
    qxv__zin = self._entrysize
    lor__leh -= qxv__zin
    qcm__ajb = src_payload.mask
    nentries = builder.add(mymov__dju, qcm__ajb)
    qsvaw__ofxrs = builder.add(ir.Constant(sre__uxp, lor__leh), builder.mul
        (ir.Constant(sre__uxp, qxv__zin), nentries))
    with builder.if_then(builder.load(aao__nymmk), likely=True):
        jrix__kvxz = _imp_dtor(context, builder.module, self._ty)
        ledx__psef = context.nrt.meminfo_new_varsize_dtor(builder,
            qsvaw__ofxrs, builder.bitcast(jrix__kvxz, cgutils.voidptr_t))
        zgm__que = cgutils.is_null(builder, ledx__psef)
        with builder.if_else(zgm__que, likely=False) as (azo__okpkg,
            hspui__qsplo):
            with azo__okpkg:
                builder.store(cgutils.false_bit, aao__nymmk)
            with hspui__qsplo:
                self._set.meminfo = ledx__psef
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = jpipl__hgila
                payload.mask = qcm__ajb
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, qxv__zin)
                with src_payload._iterate() as eplfg__fte:
                    context.nrt.incref(builder, self._ty.dtype, eplfg__fte.
                        entry.key)
    return builder.load(aao__nymmk)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    fji__aisxb = context.get_value_type(types.voidptr)
    qhh__viiy = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [fji__aisxb, qhh__viiy, fji__aisxb])
    zpgm__nur = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=zpgm__nur)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        qdkc__mhyhq = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, qdkc__mhyhq)
        with payload._iterate() as eplfg__fte:
            entry = eplfg__fte.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    fkm__hibij, = sig.args
    aodvj__prk, = args
    mgfet__qjzqm = numba.core.imputils.call_len(context, builder,
        fkm__hibij, aodvj__prk)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, mgfet__qjzqm)
    with numba.core.imputils.for_iter(context, builder, fkm__hibij, aodvj__prk
        ) as eplfg__fte:
        inst.add(eplfg__fte.value)
        context.nrt.decref(builder, set_type.dtype, eplfg__fte.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    fkm__hibij = sig.args[1]
    aodvj__prk = args[1]
    mgfet__qjzqm = numba.core.imputils.call_len(context, builder,
        fkm__hibij, aodvj__prk)
    if mgfet__qjzqm is not None:
        rphv__wzrq = builder.add(inst.payload.used, mgfet__qjzqm)
        inst.upsize(rphv__wzrq)
    with numba.core.imputils.for_iter(context, builder, fkm__hibij, aodvj__prk
        ) as eplfg__fte:
        wnzn__xbry = context.cast(builder, eplfg__fte.value, fkm__hibij.
            dtype, inst.dtype)
        inst.add(wnzn__xbry)
        context.nrt.decref(builder, fkm__hibij.dtype, eplfg__fte.value)
    if mgfet__qjzqm is not None:
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
    qhp__epniz = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, qhp__epniz, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    rcqsi__qwnlk = target_context.get_executable(library, fndesc, env)
    zib__vkcr = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=rcqsi__qwnlk, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return zib__vkcr


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
