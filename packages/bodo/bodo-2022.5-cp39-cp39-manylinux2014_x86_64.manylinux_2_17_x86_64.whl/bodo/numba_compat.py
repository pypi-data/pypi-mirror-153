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
    eku__qscs = numba.core.bytecode.FunctionIdentity.from_function(func)
    jufqs__fmcl = numba.core.interpreter.Interpreter(eku__qscs)
    yzzy__ecqkz = numba.core.bytecode.ByteCode(func_id=eku__qscs)
    func_ir = jufqs__fmcl.interpret(yzzy__ecqkz)
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
        dixzz__lmqz = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        dixzz__lmqz.run()
    wxjmi__ljpfs = numba.core.postproc.PostProcessor(func_ir)
    wxjmi__ljpfs.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, bkw__wtqcm in visit_vars_extensions.items():
        if isinstance(stmt, t):
            bkw__wtqcm(stmt, callback, cbdata)
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
    ndtqj__qun = ['ravel', 'transpose', 'reshape']
    for wgiha__uycxn in blocks.values():
        for nsdk__ocw in wgiha__uycxn.body:
            if type(nsdk__ocw) in alias_analysis_extensions:
                bkw__wtqcm = alias_analysis_extensions[type(nsdk__ocw)]
                bkw__wtqcm(nsdk__ocw, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(nsdk__ocw, ir.Assign):
                wkt__pelw = nsdk__ocw.value
                gbwza__cbs = nsdk__ocw.target.name
                if is_immutable_type(gbwza__cbs, typemap):
                    continue
                if isinstance(wkt__pelw, ir.Var
                    ) and gbwza__cbs != wkt__pelw.name:
                    _add_alias(gbwza__cbs, wkt__pelw.name, alias_map,
                        arg_aliases)
                if isinstance(wkt__pelw, ir.Expr) and (wkt__pelw.op ==
                    'cast' or wkt__pelw.op in ['getitem', 'static_getitem']):
                    _add_alias(gbwza__cbs, wkt__pelw.value.name, alias_map,
                        arg_aliases)
                if isinstance(wkt__pelw, ir.Expr
                    ) and wkt__pelw.op == 'inplace_binop':
                    _add_alias(gbwza__cbs, wkt__pelw.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(wkt__pelw, ir.Expr
                    ) and wkt__pelw.op == 'getattr' and wkt__pelw.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(gbwza__cbs, wkt__pelw.value.name, alias_map,
                        arg_aliases)
                if isinstance(wkt__pelw, ir.Expr
                    ) and wkt__pelw.op == 'getattr' and wkt__pelw.attr not in [
                    'shape'] and wkt__pelw.value.name in arg_aliases:
                    _add_alias(gbwza__cbs, wkt__pelw.value.name, alias_map,
                        arg_aliases)
                if isinstance(wkt__pelw, ir.Expr
                    ) and wkt__pelw.op == 'getattr' and wkt__pelw.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(gbwza__cbs, wkt__pelw.value.name, alias_map,
                        arg_aliases)
                if isinstance(wkt__pelw, ir.Expr) and wkt__pelw.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(gbwza__cbs, typemap):
                    for kmcq__vkeh in wkt__pelw.items:
                        _add_alias(gbwza__cbs, kmcq__vkeh.name, alias_map,
                            arg_aliases)
                if isinstance(wkt__pelw, ir.Expr) and wkt__pelw.op == 'call':
                    jarvb__fyoci = guard(find_callname, func_ir, wkt__pelw,
                        typemap)
                    if jarvb__fyoci is None:
                        continue
                    umt__wwyim, jjg__iiyd = jarvb__fyoci
                    if jarvb__fyoci in alias_func_extensions:
                        igupe__gvjs = alias_func_extensions[jarvb__fyoci]
                        igupe__gvjs(gbwza__cbs, wkt__pelw.args, alias_map,
                            arg_aliases)
                    if jjg__iiyd == 'numpy' and umt__wwyim in ndtqj__qun:
                        _add_alias(gbwza__cbs, wkt__pelw.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(jjg__iiyd, ir.Var
                        ) and umt__wwyim in ndtqj__qun:
                        _add_alias(gbwza__cbs, jjg__iiyd.name, alias_map,
                            arg_aliases)
    sql__sumqu = copy.deepcopy(alias_map)
    for kmcq__vkeh in sql__sumqu:
        for whc__qzt in sql__sumqu[kmcq__vkeh]:
            alias_map[kmcq__vkeh] |= alias_map[whc__qzt]
        for whc__qzt in sql__sumqu[kmcq__vkeh]:
            alias_map[whc__qzt] = alias_map[kmcq__vkeh]
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
    uhzu__khk = compute_cfg_from_blocks(func_ir.blocks)
    gnk__qnz = compute_use_defs(func_ir.blocks)
    pxd__fmbj = compute_live_map(uhzu__khk, func_ir.blocks, gnk__qnz.usemap,
        gnk__qnz.defmap)
    zch__zjco = True
    while zch__zjco:
        zch__zjco = False
        for akw__rez, block in func_ir.blocks.items():
            lives = {kmcq__vkeh.name for kmcq__vkeh in block.terminator.
                list_vars()}
            for uwdps__kkhng, drur__ammfi in uhzu__khk.successors(akw__rez):
                lives |= pxd__fmbj[uwdps__kkhng]
            wstt__pyojp = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    gbwza__cbs = stmt.target
                    ytvm__ilw = stmt.value
                    if gbwza__cbs.name not in lives:
                        if isinstance(ytvm__ilw, ir.Expr
                            ) and ytvm__ilw.op == 'make_function':
                            continue
                        if isinstance(ytvm__ilw, ir.Expr
                            ) and ytvm__ilw.op == 'getattr':
                            continue
                        if isinstance(ytvm__ilw, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(gbwza__cbs,
                            None), types.Function):
                            continue
                        if isinstance(ytvm__ilw, ir.Expr
                            ) and ytvm__ilw.op == 'build_map':
                            continue
                        if isinstance(ytvm__ilw, ir.Expr
                            ) and ytvm__ilw.op == 'build_tuple':
                            continue
                    if isinstance(ytvm__ilw, ir.Var
                        ) and gbwza__cbs.name == ytvm__ilw.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    euse__enewm = analysis.ir_extension_usedefs[type(stmt)]
                    xff__ipwmq, gkab__jgy = euse__enewm(stmt)
                    lives -= gkab__jgy
                    lives |= xff__ipwmq
                else:
                    lives |= {kmcq__vkeh.name for kmcq__vkeh in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(gbwza__cbs.name)
                wstt__pyojp.append(stmt)
            wstt__pyojp.reverse()
            if len(block.body) != len(wstt__pyojp):
                zch__zjco = True
            block.body = wstt__pyojp


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    qcp__lxllo = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (qcp__lxllo,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    sxrc__xigr = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), sxrc__xigr)


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
            for zmkux__xlw in fnty.templates:
                self._inline_overloads.update(zmkux__xlw._inline_overloads)
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
    sxrc__xigr = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), sxrc__xigr)
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
    yimd__kccl, srinh__jdxl = self._get_impl(args, kws)
    if yimd__kccl is None:
        return
    xcfh__cktw = types.Dispatcher(yimd__kccl)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        ffdyl__rylyk = yimd__kccl._compiler
        flags = compiler.Flags()
        xkzyv__faf = ffdyl__rylyk.targetdescr.typing_context
        ixwwj__kuv = ffdyl__rylyk.targetdescr.target_context
        iwoml__nmzj = ffdyl__rylyk.pipeline_class(xkzyv__faf, ixwwj__kuv,
            None, None, None, flags, None)
        yxml__igxxl = InlineWorker(xkzyv__faf, ixwwj__kuv, ffdyl__rylyk.
            locals, iwoml__nmzj, flags, None)
        djftz__gwbn = xcfh__cktw.dispatcher.get_call_template
        zmkux__xlw, pabys__qeqtq, eujyk__ysqan, kws = djftz__gwbn(srinh__jdxl,
            kws)
        if eujyk__ysqan in self._inline_overloads:
            return self._inline_overloads[eujyk__ysqan]['iinfo'].signature
        ir = yxml__igxxl.run_untyped_passes(xcfh__cktw.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, ixwwj__kuv, ir, eujyk__ysqan, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, eujyk__ysqan, None)
        self._inline_overloads[sig.args] = {'folded_args': eujyk__ysqan}
        oofhe__wbrk = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = oofhe__wbrk
        if not self._inline.is_always_inline:
            sig = xcfh__cktw.get_call_type(self.context, srinh__jdxl, kws)
            self._compiled_overloads[sig.args] = xcfh__cktw.get_overload(sig)
        dudz__yzdp = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': eujyk__ysqan,
            'iinfo': dudz__yzdp}
    else:
        sig = xcfh__cktw.get_call_type(self.context, srinh__jdxl, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = xcfh__cktw.get_overload(sig)
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
    kkfz__zyywg = [True, False]
    ffadq__qrxyd = [False, True]
    gjlb__shu = _ResolutionFailures(context, self, args, kws, depth=self._depth
        )
    from numba.core.target_extension import get_local_target
    rnrkp__ztroe = get_local_target(context)
    ryo__huuem = utils.order_by_target_specificity(rnrkp__ztroe, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for nql__wkwi in ryo__huuem:
        bdyzl__evnk = nql__wkwi(context)
        mknad__wkxuw = (kkfz__zyywg if bdyzl__evnk.prefer_literal else
            ffadq__qrxyd)
        mknad__wkxuw = [True] if getattr(bdyzl__evnk, '_no_unliteral', False
            ) else mknad__wkxuw
        for oswu__jxfo in mknad__wkxuw:
            try:
                if oswu__jxfo:
                    sig = bdyzl__evnk.apply(args, kws)
                else:
                    ixz__ule = tuple([_unlit_non_poison(a) for a in args])
                    lgal__ggd = {gqepb__jjs: _unlit_non_poison(kmcq__vkeh) for
                        gqepb__jjs, kmcq__vkeh in kws.items()}
                    sig = bdyzl__evnk.apply(ixz__ule, lgal__ggd)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    gjlb__shu.add_error(bdyzl__evnk, False, e, oswu__jxfo)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = bdyzl__evnk.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    flc__zxqdc = getattr(bdyzl__evnk, 'cases', None)
                    if flc__zxqdc is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            flc__zxqdc)
                    else:
                        msg = 'No match.'
                    gjlb__shu.add_error(bdyzl__evnk, True, msg, oswu__jxfo)
    gjlb__shu.raise_error()


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
    zmkux__xlw = self.template(context)
    mvt__fqzh = None
    dtclq__exhr = None
    xyuw__zlho = None
    mknad__wkxuw = [True, False] if zmkux__xlw.prefer_literal else [False, True
        ]
    mknad__wkxuw = [True] if getattr(zmkux__xlw, '_no_unliteral', False
        ) else mknad__wkxuw
    for oswu__jxfo in mknad__wkxuw:
        if oswu__jxfo:
            try:
                xyuw__zlho = zmkux__xlw.apply(args, kws)
            except Exception as swr__yderi:
                if isinstance(swr__yderi, errors.ForceLiteralArg):
                    raise swr__yderi
                mvt__fqzh = swr__yderi
                xyuw__zlho = None
            else:
                break
        else:
            jru__oll = tuple([_unlit_non_poison(a) for a in args])
            vsv__nha = {gqepb__jjs: _unlit_non_poison(kmcq__vkeh) for 
                gqepb__jjs, kmcq__vkeh in kws.items()}
            mwnx__ctzih = jru__oll == args and kws == vsv__nha
            if not mwnx__ctzih and xyuw__zlho is None:
                try:
                    xyuw__zlho = zmkux__xlw.apply(jru__oll, vsv__nha)
                except Exception as swr__yderi:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        swr__yderi, errors.NumbaError):
                        raise swr__yderi
                    if isinstance(swr__yderi, errors.ForceLiteralArg):
                        if zmkux__xlw.prefer_literal:
                            raise swr__yderi
                    dtclq__exhr = swr__yderi
                else:
                    break
    if xyuw__zlho is None and (dtclq__exhr is not None or mvt__fqzh is not None
        ):
        srxb__gqi = '- Resolution failure for {} arguments:\n{}\n'
        egqpi__wvnj = _termcolor.highlight(srxb__gqi)
        if numba.core.config.DEVELOPER_MODE:
            biql__qdhf = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    xfe__rauhu = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    xfe__rauhu = ['']
                mzie__azrt = '\n{}'.format(2 * biql__qdhf)
                hjeyp__eytge = _termcolor.reset(mzie__azrt + mzie__azrt.
                    join(_bt_as_lines(xfe__rauhu)))
                return _termcolor.reset(hjeyp__eytge)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            bqxoy__nrpye = str(e)
            bqxoy__nrpye = bqxoy__nrpye if bqxoy__nrpye else str(repr(e)
                ) + add_bt(e)
            ucml__tog = errors.TypingError(textwrap.dedent(bqxoy__nrpye))
            return egqpi__wvnj.format(literalness, str(ucml__tog))
        import bodo
        if isinstance(mvt__fqzh, bodo.utils.typing.BodoError):
            raise mvt__fqzh
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', mvt__fqzh) +
                nested_msg('non-literal', dtclq__exhr))
        else:
            if 'missing a required argument' in mvt__fqzh.msg:
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
            raise errors.TypingError(msg, loc=mvt__fqzh.loc)
    return xyuw__zlho


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
    umt__wwyim = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=umt__wwyim)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            sjb__enh = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), sjb__enh)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    umz__yspfk = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            umz__yspfk.append(types.Omitted(a.value))
        else:
            umz__yspfk.append(self.typeof_pyval(a))
    amzu__kxfta = None
    try:
        error = None
        amzu__kxfta = self.compile(tuple(umz__yspfk))
    except errors.ForceLiteralArg as e:
        bgytu__shfti = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if bgytu__shfti:
            twib__oepve = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            wsrab__giimu = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(bgytu__shfti))
            raise errors.CompilerError(twib__oepve.format(wsrab__giimu))
        srinh__jdxl = []
        try:
            for i, kmcq__vkeh in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        srinh__jdxl.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        srinh__jdxl.append(types.literal(args[i]))
                else:
                    srinh__jdxl.append(args[i])
            args = srinh__jdxl
        except (OSError, FileNotFoundError) as heg__pif:
            error = FileNotFoundError(str(heg__pif) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                amzu__kxfta = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        abt__rjo = []
        for i, jqku__qwscw in enumerate(args):
            val = jqku__qwscw.value if isinstance(jqku__qwscw, numba.core.
                dispatcher.OmittedArg) else jqku__qwscw
            try:
                ttvu__pukp = typeof(val, Purpose.argument)
            except ValueError as mcscv__qqabh:
                abt__rjo.append((i, str(mcscv__qqabh)))
            else:
                if ttvu__pukp is None:
                    abt__rjo.append((i,
                        f'cannot determine Numba type of value {val}'))
        if abt__rjo:
            fopu__bhqhe = '\n'.join(f'- argument {i}: {wslvq__pwjzn}' for i,
                wslvq__pwjzn in abt__rjo)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{fopu__bhqhe}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                rcnx__pqxam = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                bpbhe__hcmlk = False
                for vlex__bjp in rcnx__pqxam:
                    if vlex__bjp in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        bpbhe__hcmlk = True
                        break
                if not bpbhe__hcmlk:
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
                sjb__enh = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), sjb__enh)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return amzu__kxfta


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
    for chn__eqm in cres.library._codegen._engine._defined_symbols:
        if chn__eqm.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in chn__eqm and (
            'bodo_gb_udf_update_local' in chn__eqm or 'bodo_gb_udf_combine' in
            chn__eqm or 'bodo_gb_udf_eval' in chn__eqm or 
            'bodo_gb_apply_general_udfs' in chn__eqm):
            gb_agg_cfunc_addr[chn__eqm] = cres.library.get_pointer_to_function(
                chn__eqm)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for chn__eqm in cres.library._codegen._engine._defined_symbols:
        if chn__eqm.startswith('cfunc') and ('get_join_cond_addr' not in
            chn__eqm or 'bodo_join_gen_cond' in chn__eqm):
            join_gen_cond_cfunc_addr[chn__eqm
                ] = cres.library.get_pointer_to_function(chn__eqm)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    yimd__kccl = self._get_dispatcher_for_current_target()
    if yimd__kccl is not self:
        return yimd__kccl.compile(sig)
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
            djb__jlaq = self.overloads.get(tuple(args))
            if djb__jlaq is not None:
                return djb__jlaq.entry_point
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
            qinae__hnn = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=qinae__hnn):
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
                jsj__zdh = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in jsj__zdh:
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
    dis__enxp = self._final_module
    gtq__ikjhd = []
    jckd__ouee = 0
    for fn in dis__enxp.functions:
        jckd__ouee += 1
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
            gtq__ikjhd.append(fn.name)
    if jckd__ouee == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if gtq__ikjhd:
        dis__enxp = dis__enxp.clone()
        for name in gtq__ikjhd:
            dis__enxp.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = dis__enxp
    return dis__enxp


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
    for zbl__fyd in self.constraints:
        loc = zbl__fyd.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                zbl__fyd(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                dvlgo__jqr = numba.core.errors.TypingError(str(e), loc=
                    zbl__fyd.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(dvlgo__jqr, e))
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
                    dvlgo__jqr = numba.core.errors.TypingError(msg.format(
                        con=zbl__fyd, err=str(e)), loc=zbl__fyd.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(dvlgo__jqr, e))
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
    for ptqz__cyq in self._failures.values():
        for hajg__fpa in ptqz__cyq:
            if isinstance(hajg__fpa.error, ForceLiteralArg):
                raise hajg__fpa.error
            if isinstance(hajg__fpa.error, bodo.utils.typing.BodoError):
                raise hajg__fpa.error
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
    slpt__dotz = False
    wstt__pyojp = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        nnb__gkzym = set()
        lejdn__iyknq = lives & alias_set
        for kmcq__vkeh in lejdn__iyknq:
            nnb__gkzym |= alias_map[kmcq__vkeh]
        lives_n_aliases = lives | nnb__gkzym | arg_aliases
        if type(stmt) in remove_dead_extensions:
            bkw__wtqcm = remove_dead_extensions[type(stmt)]
            stmt = bkw__wtqcm(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                slpt__dotz = True
                continue
        if isinstance(stmt, ir.Assign):
            gbwza__cbs = stmt.target
            ytvm__ilw = stmt.value
            if gbwza__cbs.name not in lives and has_no_side_effect(ytvm__ilw,
                lives_n_aliases, call_table):
                slpt__dotz = True
                continue
            if saved_array_analysis and gbwza__cbs.name in lives and is_expr(
                ytvm__ilw, 'getattr'
                ) and ytvm__ilw.attr == 'shape' and is_array_typ(typemap[
                ytvm__ilw.value.name]) and ytvm__ilw.value.name not in lives:
                spiu__uoow = {kmcq__vkeh: gqepb__jjs for gqepb__jjs,
                    kmcq__vkeh in func_ir.blocks.items()}
                if block in spiu__uoow:
                    akw__rez = spiu__uoow[block]
                    syba__fab = saved_array_analysis.get_equiv_set(akw__rez)
                    atr__frsgp = syba__fab.get_equiv_set(ytvm__ilw.value)
                    if atr__frsgp is not None:
                        for kmcq__vkeh in atr__frsgp:
                            if kmcq__vkeh.endswith('#0'):
                                kmcq__vkeh = kmcq__vkeh[:-2]
                            if kmcq__vkeh in typemap and is_array_typ(typemap
                                [kmcq__vkeh]) and kmcq__vkeh in lives:
                                ytvm__ilw.value = ir.Var(ytvm__ilw.value.
                                    scope, kmcq__vkeh, ytvm__ilw.value.loc)
                                slpt__dotz = True
                                break
            if isinstance(ytvm__ilw, ir.Var
                ) and gbwza__cbs.name == ytvm__ilw.name:
                slpt__dotz = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                slpt__dotz = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            euse__enewm = analysis.ir_extension_usedefs[type(stmt)]
            xff__ipwmq, gkab__jgy = euse__enewm(stmt)
            lives -= gkab__jgy
            lives |= xff__ipwmq
        else:
            lives |= {kmcq__vkeh.name for kmcq__vkeh in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                zii__bcuxj = set()
                if isinstance(ytvm__ilw, ir.Expr):
                    zii__bcuxj = {kmcq__vkeh.name for kmcq__vkeh in
                        ytvm__ilw.list_vars()}
                if gbwza__cbs.name not in zii__bcuxj:
                    lives.remove(gbwza__cbs.name)
        wstt__pyojp.append(stmt)
    wstt__pyojp.reverse()
    block.body = wstt__pyojp
    return slpt__dotz


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            qfp__bbzhe, = args
            if isinstance(qfp__bbzhe, types.IterableType):
                dtype = qfp__bbzhe.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), qfp__bbzhe)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    rxh__keuxj = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (rxh__keuxj, self.dtype)
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
        except LiteralTypingError as ksfe__ods:
            return
    try:
        return literal(value)
    except LiteralTypingError as ksfe__ods:
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
        dja__mgzdn = py_func.__qualname__
    except AttributeError as ksfe__ods:
        dja__mgzdn = py_func.__name__
    qhv__phxl = inspect.getfile(py_func)
    for cls in self._locator_classes:
        zxtj__vlsf = cls.from_function(py_func, qhv__phxl)
        if zxtj__vlsf is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (dja__mgzdn, qhv__phxl))
    self._locator = zxtj__vlsf
    boskw__bhot = inspect.getfile(py_func)
    ajzp__tsfd = os.path.splitext(os.path.basename(boskw__bhot))[0]
    if qhv__phxl.startswith('<ipython-'):
        gtkpp__gawod = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', ajzp__tsfd, count=1)
        if gtkpp__gawod == ajzp__tsfd:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        ajzp__tsfd = gtkpp__gawod
    tlyk__swlcv = '%s.%s' % (ajzp__tsfd, dja__mgzdn)
    oxrlw__pzfst = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(tlyk__swlcv, oxrlw__pzfst)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    cibim__pnp = list(filter(lambda a: self._istuple(a.name), args))
    if len(cibim__pnp) == 2 and fn.__name__ == 'add':
        uct__jac = self.typemap[cibim__pnp[0].name]
        the__lgbp = self.typemap[cibim__pnp[1].name]
        if uct__jac.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                cibim__pnp[1]))
        if the__lgbp.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                cibim__pnp[0]))
        try:
            dete__eijls = [equiv_set.get_shape(x) for x in cibim__pnp]
            if None in dete__eijls:
                return None
            qyc__delg = sum(dete__eijls, ())
            return ArrayAnalysis.AnalyzeResult(shape=qyc__delg)
        except GuardException as ksfe__ods:
            return None
    mfkr__ggnni = list(filter(lambda a: self._isarray(a.name), args))
    require(len(mfkr__ggnni) > 0)
    vloa__rubus = [x.name for x in mfkr__ggnni]
    vja__efnwo = [self.typemap[x.name].ndim for x in mfkr__ggnni]
    rry__wkhuv = max(vja__efnwo)
    require(rry__wkhuv > 0)
    dete__eijls = [equiv_set.get_shape(x) for x in mfkr__ggnni]
    if any(a is None for a in dete__eijls):
        return ArrayAnalysis.AnalyzeResult(shape=mfkr__ggnni[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, mfkr__ggnni))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, dete__eijls,
        vloa__rubus)


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
    lcx__azngo = code_obj.code
    brkr__vgig = len(lcx__azngo.co_freevars)
    hyc__twle = lcx__azngo.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        gagf__qjolw, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        hyc__twle = [kmcq__vkeh.name for kmcq__vkeh in gagf__qjolw]
    fdyvh__kwdpp = caller_ir.func_id.func.__globals__
    try:
        fdyvh__kwdpp = getattr(code_obj, 'globals', fdyvh__kwdpp)
    except KeyError as ksfe__ods:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    gkv__tobih = []
    for x in hyc__twle:
        try:
            rgn__rzow = caller_ir.get_definition(x)
        except KeyError as ksfe__ods:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(rgn__rzow, (ir.Const, ir.Global, ir.FreeVar)):
            val = rgn__rzow.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                qcp__lxllo = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                fdyvh__kwdpp[qcp__lxllo] = bodo.jit(distributed=False)(val)
                fdyvh__kwdpp[qcp__lxllo].is_nested_func = True
                val = qcp__lxllo
            if isinstance(val, CPUDispatcher):
                qcp__lxllo = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                fdyvh__kwdpp[qcp__lxllo] = val
                val = qcp__lxllo
            gkv__tobih.append(val)
        elif isinstance(rgn__rzow, ir.Expr
            ) and rgn__rzow.op == 'make_function':
            twb__eqs = convert_code_obj_to_function(rgn__rzow, caller_ir)
            qcp__lxllo = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            fdyvh__kwdpp[qcp__lxllo] = bodo.jit(distributed=False)(twb__eqs)
            fdyvh__kwdpp[qcp__lxllo].is_nested_func = True
            gkv__tobih.append(qcp__lxllo)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    dokx__bidyi = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate
        (gkv__tobih)])
    ipu__djfy = ','.join([('c_%d' % i) for i in range(brkr__vgig)])
    qubth__vhfo = list(lcx__azngo.co_varnames)
    pndj__aoba = 0
    muke__auu = lcx__azngo.co_argcount
    yzbto__bkiv = caller_ir.get_definition(code_obj.defaults)
    if yzbto__bkiv is not None:
        if isinstance(yzbto__bkiv, tuple):
            d = [caller_ir.get_definition(x).value for x in yzbto__bkiv]
            jidmz__rribu = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in yzbto__bkiv.items]
            jidmz__rribu = tuple(d)
        pndj__aoba = len(jidmz__rribu)
    yvcr__zkt = muke__auu - pndj__aoba
    xeyj__ythy = ','.join([('%s' % qubth__vhfo[i]) for i in range(yvcr__zkt)])
    if pndj__aoba:
        tmph__qedkd = [('%s = %s' % (qubth__vhfo[i + yvcr__zkt],
            jidmz__rribu[i])) for i in range(pndj__aoba)]
        xeyj__ythy += ', '
        xeyj__ythy += ', '.join(tmph__qedkd)
    return _create_function_from_code_obj(lcx__azngo, dokx__bidyi,
        xeyj__ythy, ipu__djfy, fdyvh__kwdpp)


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
    for zrwa__jrwm, (qiwhj__nbbvc, okels__kqoyz) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % okels__kqoyz)
            nocqe__ecdqh = _pass_registry.get(qiwhj__nbbvc).pass_inst
            if isinstance(nocqe__ecdqh, CompilerPass):
                self._runPass(zrwa__jrwm, nocqe__ecdqh, state)
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
                    pipeline_name, okels__kqoyz)
                mas__njnk = self._patch_error(msg, e)
                raise mas__njnk
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
    csqkb__rarf = None
    gkab__jgy = {}

    def lookup(var, already_seen, varonly=True):
        val = gkab__jgy.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    bbm__qteqp = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        gbwza__cbs = stmt.target
        ytvm__ilw = stmt.value
        gkab__jgy[gbwza__cbs.name] = ytvm__ilw
        if isinstance(ytvm__ilw, ir.Var) and ytvm__ilw.name in gkab__jgy:
            ytvm__ilw = lookup(ytvm__ilw, set())
        if isinstance(ytvm__ilw, ir.Expr):
            zyirm__kiuhk = set(lookup(kmcq__vkeh, set(), True).name for
                kmcq__vkeh in ytvm__ilw.list_vars())
            if name in zyirm__kiuhk:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ytvm__ilw)]
                qrfws__qtycz = [x for x, jkuny__gnmtf in args if 
                    jkuny__gnmtf.name != name]
                args = [(x, jkuny__gnmtf) for x, jkuny__gnmtf in args if x !=
                    jkuny__gnmtf.name]
                igo__umd = dict(args)
                if len(qrfws__qtycz) == 1:
                    igo__umd[qrfws__qtycz[0]] = ir.Var(gbwza__cbs.scope, 
                        name + '#init', gbwza__cbs.loc)
                replace_vars_inner(ytvm__ilw, igo__umd)
                csqkb__rarf = nodes[i:]
                break
    return csqkb__rarf


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
        kdhd__zsg = expand_aliases({kmcq__vkeh.name for kmcq__vkeh in stmt.
            list_vars()}, alias_map, arg_aliases)
        dug__ksksk = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        lilqa__eza = expand_aliases({kmcq__vkeh.name for kmcq__vkeh in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        yko__hdih = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(dug__ksksk & lilqa__eza | yko__hdih & kdhd__zsg) == 0:
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
    pum__ryd = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            pum__ryd.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                pum__ryd.update(get_parfor_writes(stmt, func_ir))
    return pum__ryd


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    pum__ryd = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        pum__ryd.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        pum__ryd = {kmcq__vkeh.name for kmcq__vkeh in stmt.df_out_vars.values()
            }
        if stmt.out_key_vars is not None:
            pum__ryd.update({kmcq__vkeh.name for kmcq__vkeh in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        pum__ryd = {kmcq__vkeh.name for kmcq__vkeh in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        pum__ryd = {kmcq__vkeh.name for kmcq__vkeh in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            pum__ryd.update({kmcq__vkeh.name for kmcq__vkeh in stmt.
                out_key_arrs})
            pum__ryd.update({kmcq__vkeh.name for kmcq__vkeh in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        jarvb__fyoci = guard(find_callname, func_ir, stmt.value)
        if jarvb__fyoci in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'
            ), ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            pum__ryd.add(stmt.value.args[0].name)
        if jarvb__fyoci == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            pum__ryd.add(stmt.value.args[1].name)
    return pum__ryd


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
        bkw__wtqcm = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        qyow__wtpg = bkw__wtqcm.format(self, msg)
        self.args = qyow__wtpg,
    else:
        bkw__wtqcm = _termcolor.errmsg('{0}')
        qyow__wtpg = bkw__wtqcm.format(self)
        self.args = qyow__wtpg,
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
        for jmpd__nwbqd in options['distributed']:
            dist_spec[jmpd__nwbqd] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for jmpd__nwbqd in options['distributed_block']:
            dist_spec[jmpd__nwbqd] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    svi__nou = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, erf__vhklk in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(erf__vhklk)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    rtlch__enh = {}
    for jcm__rmvc in reversed(inspect.getmro(cls)):
        rtlch__enh.update(jcm__rmvc.__dict__)
    ukvb__rcmh, ehqk__cvyj, tzgkq__pvv, jyatk__eqtt = {}, {}, {}, {}
    for gqepb__jjs, kmcq__vkeh in rtlch__enh.items():
        if isinstance(kmcq__vkeh, pytypes.FunctionType):
            ukvb__rcmh[gqepb__jjs] = kmcq__vkeh
        elif isinstance(kmcq__vkeh, property):
            ehqk__cvyj[gqepb__jjs] = kmcq__vkeh
        elif isinstance(kmcq__vkeh, staticmethod):
            tzgkq__pvv[gqepb__jjs] = kmcq__vkeh
        else:
            jyatk__eqtt[gqepb__jjs] = kmcq__vkeh
    kwfzq__mpq = (set(ukvb__rcmh) | set(ehqk__cvyj) | set(tzgkq__pvv)) & set(
        spec)
    if kwfzq__mpq:
        raise NameError('name shadowing: {0}'.format(', '.join(kwfzq__mpq)))
    umbre__mdfxx = jyatk__eqtt.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(jyatk__eqtt)
    if jyatk__eqtt:
        msg = 'class members are not yet supported: {0}'
        uijm__ymtz = ', '.join(jyatk__eqtt.keys())
        raise TypeError(msg.format(uijm__ymtz))
    for gqepb__jjs, kmcq__vkeh in ehqk__cvyj.items():
        if kmcq__vkeh.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(gqepb__jjs))
    jit_methods = {gqepb__jjs: bodo.jit(returns_maybe_distributed=svi__nou)
        (kmcq__vkeh) for gqepb__jjs, kmcq__vkeh in ukvb__rcmh.items()}
    jit_props = {}
    for gqepb__jjs, kmcq__vkeh in ehqk__cvyj.items():
        sxrc__xigr = {}
        if kmcq__vkeh.fget:
            sxrc__xigr['get'] = bodo.jit(kmcq__vkeh.fget)
        if kmcq__vkeh.fset:
            sxrc__xigr['set'] = bodo.jit(kmcq__vkeh.fset)
        jit_props[gqepb__jjs] = sxrc__xigr
    jit_static_methods = {gqepb__jjs: bodo.jit(kmcq__vkeh.__func__) for 
        gqepb__jjs, kmcq__vkeh in tzgkq__pvv.items()}
    hfxzf__knrdm = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    tjd__klvig = dict(class_type=hfxzf__knrdm, __doc__=umbre__mdfxx)
    tjd__klvig.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), tjd__klvig)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, hfxzf__knrdm)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(hfxzf__knrdm, typingctx, targetctx).register()
    as_numba_type.register(cls, hfxzf__knrdm.instance_type)
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
    kcs__hzmx = ','.join('{0}:{1}'.format(gqepb__jjs, kmcq__vkeh) for 
        gqepb__jjs, kmcq__vkeh in struct.items())
    ijv__elvy = ','.join('{0}:{1}'.format(gqepb__jjs, kmcq__vkeh) for 
        gqepb__jjs, kmcq__vkeh in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), kcs__hzmx, ijv__elvy)
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
    lec__bzmc = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if lec__bzmc is None:
        return
    srv__iqa, dqm__pfxro = lec__bzmc
    for a in itertools.chain(srv__iqa, dqm__pfxro.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, srv__iqa, dqm__pfxro)
    except ForceLiteralArg as e:
        urfn__nlin = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(urfn__nlin, self.kws)
        hsunp__nrt = set()
        lsbmc__hmmt = set()
        rpp__fioa = {}
        for zrwa__jrwm in e.requested_args:
            ujmp__xwuyf = typeinfer.func_ir.get_definition(folded[zrwa__jrwm])
            if isinstance(ujmp__xwuyf, ir.Arg):
                hsunp__nrt.add(ujmp__xwuyf.index)
                if ujmp__xwuyf.index in e.file_infos:
                    rpp__fioa[ujmp__xwuyf.index] = e.file_infos[ujmp__xwuyf
                        .index]
            else:
                lsbmc__hmmt.add(zrwa__jrwm)
        if lsbmc__hmmt:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif hsunp__nrt:
            raise ForceLiteralArg(hsunp__nrt, loc=self.loc, file_infos=
                rpp__fioa)
    if sig is None:
        fmb__zpzl = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in srv__iqa]
        args += [('%s=%s' % (gqepb__jjs, kmcq__vkeh)) for gqepb__jjs,
            kmcq__vkeh in sorted(dqm__pfxro.items())]
        lhlli__lkgx = fmb__zpzl.format(fnty, ', '.join(map(str, args)))
        aes__xypy = context.explain_function_type(fnty)
        msg = '\n'.join([lhlli__lkgx, aes__xypy])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        xad__ehl = context.unify_pairs(sig.recvr, fnty.this)
        if xad__ehl is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if xad__ehl is not None and xad__ehl.is_precise():
            sogjh__sud = fnty.copy(this=xad__ehl)
            typeinfer.propagate_refined_type(self.func, sogjh__sud)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            vqla__hzw = target.getone()
            if context.unify_pairs(vqla__hzw, sig.return_type) == vqla__hzw:
                sig = sig.replace(return_type=vqla__hzw)
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
        twib__oepve = '*other* must be a {} but got a {} instead'
        raise TypeError(twib__oepve.format(ForceLiteralArg, type(other)))
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
    qwbu__duomq = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for gqepb__jjs, kmcq__vkeh in kwargs.items():
        lsd__jcxqz = None
        try:
            nms__zsjnj = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var
                ('dummy'), loc)
            func_ir._definitions[nms__zsjnj.name] = [kmcq__vkeh]
            lsd__jcxqz = get_const_value_inner(func_ir, nms__zsjnj)
            func_ir._definitions.pop(nms__zsjnj.name)
            if isinstance(lsd__jcxqz, str):
                lsd__jcxqz = sigutils._parse_signature_string(lsd__jcxqz)
            if isinstance(lsd__jcxqz, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {gqepb__jjs} is annotated as type class {lsd__jcxqz}."""
                    )
            assert isinstance(lsd__jcxqz, types.Type)
            if isinstance(lsd__jcxqz, (types.List, types.Set)):
                lsd__jcxqz = lsd__jcxqz.copy(reflected=False)
            qwbu__duomq[gqepb__jjs] = lsd__jcxqz
        except BodoError as ksfe__ods:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(lsd__jcxqz, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(kmcq__vkeh, ir.Global):
                    msg = f'Global {kmcq__vkeh.name!r} is not defined.'
                if isinstance(kmcq__vkeh, ir.FreeVar):
                    msg = f'Freevar {kmcq__vkeh.name!r} is not defined.'
            if isinstance(kmcq__vkeh, ir.Expr) and kmcq__vkeh.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=gqepb__jjs, msg=msg, loc=loc)
    for name, typ in qwbu__duomq.items():
        self._legalize_arg_type(name, typ, loc)
    return qwbu__duomq


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
    kzd__zdbyc = inst.arg
    assert kzd__zdbyc > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(kzd__zdbyc)]))
    tmps = [state.make_temp() for _ in range(kzd__zdbyc - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    lgdry__iyxf = ir.Global('format', format, loc=self.loc)
    self.store(value=lgdry__iyxf, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    zhn__yexq = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=zhn__yexq, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    kzd__zdbyc = inst.arg
    assert kzd__zdbyc > 0, 'invalid BUILD_STRING count'
    yjf__pnlk = self.get(strings[0])
    for other, roxn__aht in zip(strings[1:], tmps):
        other = self.get(other)
        wkt__pelw = ir.Expr.binop(operator.add, lhs=yjf__pnlk, rhs=other,
            loc=self.loc)
        self.store(wkt__pelw, roxn__aht)
        yjf__pnlk = self.get(roxn__aht)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    adyi__lkn = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, adyi__lkn])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    rlfbf__fyeg = mk_unique_var(f'{var_name}')
    suy__yjpwi = rlfbf__fyeg.replace('<', '_').replace('>', '_')
    suy__yjpwi = suy__yjpwi.replace('.', '_').replace('$', '_v')
    return suy__yjpwi


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
                olwj__dxt = get_overload_const_str(val2)
                if olwj__dxt != 'ns':
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
        xjq__tvmay = states['defmap']
        if len(xjq__tvmay) == 0:
            yub__pljhr = assign.target
            numba.core.ssa._logger.debug('first assign: %s', yub__pljhr)
            if yub__pljhr.name not in scope.localvars:
                yub__pljhr = scope.define(assign.target.name, loc=assign.loc)
        else:
            yub__pljhr = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=yub__pljhr, value=assign.value, loc=
            assign.loc)
        xjq__tvmay[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    mxbyr__nput = []
    for gqepb__jjs, kmcq__vkeh in typing.npydecl.registry.globals:
        if gqepb__jjs == func:
            mxbyr__nput.append(kmcq__vkeh)
    for gqepb__jjs, kmcq__vkeh in typing.templates.builtin_registry.globals:
        if gqepb__jjs == func:
            mxbyr__nput.append(kmcq__vkeh)
    if len(mxbyr__nput) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return mxbyr__nput


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    ravla__whtq = {}
    vvov__qhc = find_topo_order(blocks)
    unq__sgd = {}
    for akw__rez in vvov__qhc:
        block = blocks[akw__rez]
        wstt__pyojp = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                gbwza__cbs = stmt.target.name
                ytvm__ilw = stmt.value
                if (ytvm__ilw.op == 'getattr' and ytvm__ilw.attr in
                    arr_math and isinstance(typemap[ytvm__ilw.value.name],
                    types.npytypes.Array)):
                    ytvm__ilw = stmt.value
                    idoyy__ntkz = ytvm__ilw.value
                    ravla__whtq[gbwza__cbs] = idoyy__ntkz
                    scope = idoyy__ntkz.scope
                    loc = idoyy__ntkz.loc
                    ooc__lgnp = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[ooc__lgnp.name] = types.misc.Module(numpy)
                    jvq__tow = ir.Global('np', numpy, loc)
                    walne__zss = ir.Assign(jvq__tow, ooc__lgnp, loc)
                    ytvm__ilw.value = ooc__lgnp
                    wstt__pyojp.append(walne__zss)
                    func_ir._definitions[ooc__lgnp.name] = [jvq__tow]
                    func = getattr(numpy, ytvm__ilw.attr)
                    phdcm__wqhs = get_np_ufunc_typ_lst(func)
                    unq__sgd[gbwza__cbs] = phdcm__wqhs
                if (ytvm__ilw.op == 'call' and ytvm__ilw.func.name in
                    ravla__whtq):
                    idoyy__ntkz = ravla__whtq[ytvm__ilw.func.name]
                    hlt__zubqt = calltypes.pop(ytvm__ilw)
                    fiz__kyrxa = hlt__zubqt.args[:len(ytvm__ilw.args)]
                    altqd__mtcu = {name: typemap[kmcq__vkeh.name] for name,
                        kmcq__vkeh in ytvm__ilw.kws}
                    pqh__iaju = unq__sgd[ytvm__ilw.func.name]
                    kvwgk__ogzgy = None
                    for kctrh__dsou in pqh__iaju:
                        try:
                            kvwgk__ogzgy = kctrh__dsou.get_call_type(typingctx,
                                [typemap[idoyy__ntkz.name]] + list(
                                fiz__kyrxa), altqd__mtcu)
                            typemap.pop(ytvm__ilw.func.name)
                            typemap[ytvm__ilw.func.name] = kctrh__dsou
                            calltypes[ytvm__ilw] = kvwgk__ogzgy
                            break
                        except Exception as ksfe__ods:
                            pass
                    if kvwgk__ogzgy is None:
                        raise TypeError(
                            f'No valid template found for {ytvm__ilw.func.name}'
                            )
                    ytvm__ilw.args = [idoyy__ntkz] + ytvm__ilw.args
            wstt__pyojp.append(stmt)
        block.body = wstt__pyojp


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    yaief__kkw = ufunc.nin
    mznu__shnv = ufunc.nout
    yvcr__zkt = ufunc.nargs
    assert yvcr__zkt == yaief__kkw + mznu__shnv
    if len(args) < yaief__kkw:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), yaief__kkw)
            )
    if len(args) > yvcr__zkt:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), yvcr__zkt))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    hvweo__gdjev = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    lvmmu__rlw = max(hvweo__gdjev)
    mdq__kxwpq = args[yaief__kkw:]
    if not all(d == lvmmu__rlw for d in hvweo__gdjev[yaief__kkw:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(vyz__vrfl, types.ArrayCompatible) and not
        isinstance(vyz__vrfl, types.Bytes) for vyz__vrfl in mdq__kxwpq):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(vyz__vrfl.mutable for vyz__vrfl in mdq__kxwpq):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    trbh__tuvrq = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    agjml__dsoqk = None
    if lvmmu__rlw > 0 and len(mdq__kxwpq) < ufunc.nout:
        agjml__dsoqk = 'C'
        zvdka__zmua = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in zvdka__zmua and 'F' in zvdka__zmua:
            agjml__dsoqk = 'F'
    return trbh__tuvrq, mdq__kxwpq, lvmmu__rlw, agjml__dsoqk


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
        txobi__umel = 'Dict.key_type cannot be of type {}'
        raise TypingError(txobi__umel.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        txobi__umel = 'Dict.value_type cannot be of type {}'
        raise TypingError(txobi__umel.format(valty))
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
    tank__fdkxh = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[tank__fdkxh]
        return impl, args
    except KeyError as ksfe__ods:
        pass
    impl, args = self._build_impl(tank__fdkxh, args, kws)
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
        tkars__jzy = find_topo_order(parfor.loop_body)
    alf__kqe = tkars__jzy[0]
    kvykf__non = {}
    _update_parfor_get_setitems(parfor.loop_body[alf__kqe].body, parfor.
        index_var, alias_map, kvykf__non, lives_n_aliases)
    orh__quvme = set(kvykf__non.keys())
    for ujfmw__xqwn in tkars__jzy:
        if ujfmw__xqwn == alf__kqe:
            continue
        for stmt in parfor.loop_body[ujfmw__xqwn].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            hoo__uwe = set(kmcq__vkeh.name for kmcq__vkeh in stmt.list_vars())
            zoslr__uptk = hoo__uwe & orh__quvme
            for a in zoslr__uptk:
                kvykf__non.pop(a, None)
    for ujfmw__xqwn in tkars__jzy:
        if ujfmw__xqwn == alf__kqe:
            continue
        block = parfor.loop_body[ujfmw__xqwn]
        cyjd__yhltr = kvykf__non.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            cyjd__yhltr, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    mpdkt__jcwc = max(blocks.keys())
    raqyf__jyr, dfrak__fnbh = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    buicb__qmhq = ir.Jump(raqyf__jyr, ir.Loc('parfors_dummy', -1))
    blocks[mpdkt__jcwc].body.append(buicb__qmhq)
    uhzu__khk = compute_cfg_from_blocks(blocks)
    gnk__qnz = compute_use_defs(blocks)
    pxd__fmbj = compute_live_map(uhzu__khk, blocks, gnk__qnz.usemap,
        gnk__qnz.defmap)
    alias_set = set(alias_map.keys())
    for akw__rez, block in blocks.items():
        wstt__pyojp = []
        dhqrk__jykk = {kmcq__vkeh.name for kmcq__vkeh in block.terminator.
            list_vars()}
        for uwdps__kkhng, drur__ammfi in uhzu__khk.successors(akw__rez):
            dhqrk__jykk |= pxd__fmbj[uwdps__kkhng]
        for stmt in reversed(block.body):
            nnb__gkzym = dhqrk__jykk & alias_set
            for kmcq__vkeh in nnb__gkzym:
                dhqrk__jykk |= alias_map[kmcq__vkeh]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in dhqrk__jykk and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                jarvb__fyoci = guard(find_callname, func_ir, stmt.value)
                if jarvb__fyoci == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in dhqrk__jykk and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            dhqrk__jykk |= {kmcq__vkeh.name for kmcq__vkeh in stmt.list_vars()}
            wstt__pyojp.append(stmt)
        wstt__pyojp.reverse()
        block.body = wstt__pyojp
    typemap.pop(dfrak__fnbh.name)
    blocks[mpdkt__jcwc].body.pop()

    def trim_empty_parfor_branches(parfor):
        zch__zjco = False
        blocks = parfor.loop_body.copy()
        for akw__rez, block in blocks.items():
            if len(block.body):
                mdgvn__tjbpo = block.body[-1]
                if isinstance(mdgvn__tjbpo, ir.Branch):
                    if len(blocks[mdgvn__tjbpo.truebr].body) == 1 and len(
                        blocks[mdgvn__tjbpo.falsebr].body) == 1:
                        ugzvz__eoj = blocks[mdgvn__tjbpo.truebr].body[0]
                        mtyoy__uhtek = blocks[mdgvn__tjbpo.falsebr].body[0]
                        if isinstance(ugzvz__eoj, ir.Jump) and isinstance(
                            mtyoy__uhtek, ir.Jump
                            ) and ugzvz__eoj.target == mtyoy__uhtek.target:
                            parfor.loop_body[akw__rez].body[-1] = ir.Jump(
                                ugzvz__eoj.target, mdgvn__tjbpo.loc)
                            zch__zjco = True
                    elif len(blocks[mdgvn__tjbpo.truebr].body) == 1:
                        ugzvz__eoj = blocks[mdgvn__tjbpo.truebr].body[0]
                        if isinstance(ugzvz__eoj, ir.Jump
                            ) and ugzvz__eoj.target == mdgvn__tjbpo.falsebr:
                            parfor.loop_body[akw__rez].body[-1] = ir.Jump(
                                ugzvz__eoj.target, mdgvn__tjbpo.loc)
                            zch__zjco = True
                    elif len(blocks[mdgvn__tjbpo.falsebr].body) == 1:
                        mtyoy__uhtek = blocks[mdgvn__tjbpo.falsebr].body[0]
                        if isinstance(mtyoy__uhtek, ir.Jump
                            ) and mtyoy__uhtek.target == mdgvn__tjbpo.truebr:
                            parfor.loop_body[akw__rez].body[-1] = ir.Jump(
                                mtyoy__uhtek.target, mdgvn__tjbpo.loc)
                            zch__zjco = True
        return zch__zjco
    zch__zjco = True
    while zch__zjco:
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
        zch__zjco = trim_empty_parfor_branches(parfor)
    ilhev__aygqf = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        ilhev__aygqf &= len(block.body) == 0
    if ilhev__aygqf:
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
    yvx__qorwy = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                yvx__qorwy += 1
                parfor = stmt
                aazl__jae = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = aazl__jae.scope
                loc = ir.Loc('parfors_dummy', -1)
                aphg__xohop = ir.Var(scope, mk_unique_var('$const'), loc)
                aazl__jae.body.append(ir.Assign(ir.Const(0, loc),
                    aphg__xohop, loc))
                aazl__jae.body.append(ir.Return(aphg__xohop, loc))
                uhzu__khk = compute_cfg_from_blocks(parfor.loop_body)
                for ckw__zblyo in uhzu__khk.dead_nodes():
                    del parfor.loop_body[ckw__zblyo]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                aazl__jae = parfor.loop_body[max(parfor.loop_body.keys())]
                aazl__jae.body.pop()
                aazl__jae.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return yvx__qorwy


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
            djb__jlaq = self.overloads.get(tuple(args))
            if djb__jlaq is not None:
                return djb__jlaq.entry_point
            self._pre_compile(args, return_type, flags)
            ide__euigd = self.func_ir
            qinae__hnn = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=qinae__hnn):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=ide__euigd, args=args,
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
        gnqrs__cmswq = copy.deepcopy(flags)
        gnqrs__cmswq.no_rewrites = True

        def compile_local(the_ir, the_flags):
            uyc__rizk = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return uyc__rizk.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        ajmi__kywxy = compile_local(func_ir, gnqrs__cmswq)
        len__uijfy = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    len__uijfy = compile_local(func_ir, flags)
                except Exception as ksfe__ods:
                    pass
        if len__uijfy is not None:
            cres = len__uijfy
        else:
            cres = ajmi__kywxy
        return cres
    else:
        uyc__rizk = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return uyc__rizk.compile_ir(func_ir=func_ir, lifted=lifted,
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
    wth__tzs = self.get_data_type(typ.dtype)
    gesx__vej = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        gesx__vej):
        kbo__eei = ary.ctypes.data
        urjat__kfvzj = self.add_dynamic_addr(builder, kbo__eei, info=str(
            type(kbo__eei)))
        ybipj__alio = self.add_dynamic_addr(builder, id(ary), info=str(type
            (ary)))
        self.global_arrays.append(ary)
    else:
        jrrv__vot = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            jrrv__vot = jrrv__vot.view('int64')
        val = bytearray(jrrv__vot.data)
        aviwm__amp = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        urjat__kfvzj = cgutils.global_constant(builder, '.const.array.data',
            aviwm__amp)
        urjat__kfvzj.align = self.get_abi_alignment(wth__tzs)
        ybipj__alio = None
    fbon__zyphe = self.get_value_type(types.intp)
    fgnq__bzds = [self.get_constant(types.intp, gzn__cqq) for gzn__cqq in
        ary.shape]
    wtr__ezvvd = lir.Constant(lir.ArrayType(fbon__zyphe, len(fgnq__bzds)),
        fgnq__bzds)
    ugqj__xceex = [self.get_constant(types.intp, gzn__cqq) for gzn__cqq in
        ary.strides]
    bkd__ukyjz = lir.Constant(lir.ArrayType(fbon__zyphe, len(ugqj__xceex)),
        ugqj__xceex)
    mwa__egmqs = self.get_constant(types.intp, ary.dtype.itemsize)
    ynts__iva = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        ynts__iva, mwa__egmqs, urjat__kfvzj.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), wtr__ezvvd, bkd__ukyjz])


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
    rut__semy = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    yif__llfce = lir.Function(module, rut__semy, name='nrt_atomic_{0}'.
        format(op))
    [ypgf__zdy] = yif__llfce.args
    qyyjh__dsu = yif__llfce.append_basic_block()
    builder = lir.IRBuilder(qyyjh__dsu)
    idcx__bmbw = lir.Constant(_word_type, 1)
    if False:
        tnn__jlfst = builder.atomic_rmw(op, ypgf__zdy, idcx__bmbw, ordering
            =ordering)
        res = getattr(builder, op)(tnn__jlfst, idcx__bmbw)
        builder.ret(res)
    else:
        tnn__jlfst = builder.load(ypgf__zdy)
        lnxpj__xmf = getattr(builder, op)(tnn__jlfst, idcx__bmbw)
        sfh__uwztz = builder.icmp_signed('!=', tnn__jlfst, lir.Constant(
            tnn__jlfst.type, -1))
        with cgutils.if_likely(builder, sfh__uwztz):
            builder.store(lnxpj__xmf, ypgf__zdy)
        builder.ret(lnxpj__xmf)
    return yif__llfce


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
        wikis__tewe = state.targetctx.codegen()
        state.library = wikis__tewe.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    jufqs__fmcl = state.func_ir
    typemap = state.typemap
    ekenm__zsuhb = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    wesdx__felmq = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            jufqs__fmcl, typemap, ekenm__zsuhb, calltypes, mangler=
            targetctx.mangler, inline=flags.forceinline, noalias=flags.
            noalias, abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            tezp__ivux = lowering.Lower(targetctx, library, fndesc,
                jufqs__fmcl, metadata=metadata)
            tezp__ivux.lower()
            if not flags.no_cpython_wrapper:
                tezp__ivux.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(ekenm__zsuhb, (types.Optional, types.
                        Generator)):
                        pass
                    else:
                        tezp__ivux.create_cfunc_wrapper()
            env = tezp__ivux.env
            omm__xkpa = tezp__ivux.call_helper
            del tezp__ivux
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, omm__xkpa, cfunc=None, env=env)
        else:
            nzv__dnb = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(nzv__dnb, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, omm__xkpa, cfunc=nzv__dnb,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        inyc__sokqz = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = inyc__sokqz - wesdx__felmq
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
        cpxwy__diyfc = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, cpxwy__diyfc),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            yaff__boti.do_break()
        ebt__ungcn = c.builder.icmp_signed('!=', cpxwy__diyfc, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(ebt__ungcn, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, cpxwy__diyfc)
                c.pyapi.decref(cpxwy__diyfc)
                yaff__boti.do_break()
        c.pyapi.decref(cpxwy__diyfc)
    bbhq__uwjk, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(bbhq__uwjk, likely=True) as (mvgw__wtrc, ifu__oebw):
        with mvgw__wtrc:
            list.size = size
            cakyb__gzt = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                cakyb__gzt), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        cakyb__gzt))
                    with cgutils.for_range(c.builder, size) as yaff__boti:
                        itemobj = c.pyapi.list_getitem(obj, yaff__boti.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        collt__vkkd = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(collt__vkkd.is_error, likely
                            =False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            yaff__boti.do_break()
                        list.setitem(yaff__boti.index, collt__vkkd.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with ifu__oebw:
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
    glfv__fpkw, lhdu__hey, pjhy__difm, hkmsm__hclx, emfrg__eqyc = (
        compile_time_get_string_data(literal_string))
    dis__enxp = builder.module
    gv = context.insert_const_bytes(dis__enxp, glfv__fpkw)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        lhdu__hey), context.get_constant(types.int32, pjhy__difm), context.
        get_constant(types.uint32, hkmsm__hclx), context.get_constant(
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
    apkj__dzxzz = None
    if isinstance(shape, types.Integer):
        apkj__dzxzz = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(gzn__cqq, (types.Integer, types.IntEnumMember)) for
            gzn__cqq in shape):
            apkj__dzxzz = len(shape)
    return apkj__dzxzz


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
            apkj__dzxzz = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if apkj__dzxzz == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    apkj__dzxzz))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            vloa__rubus = self._get_names(x)
            if len(vloa__rubus) != 0:
                return vloa__rubus[0]
            return vloa__rubus
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    vloa__rubus = self._get_names(obj)
    if len(vloa__rubus) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(vloa__rubus[0])


def get_equiv_set(self, obj):
    vloa__rubus = self._get_names(obj)
    if len(vloa__rubus) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(vloa__rubus[0])


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
    aaipw__cnoj = []
    for xddzi__ilt in func_ir.arg_names:
        if xddzi__ilt in typemap and isinstance(typemap[xddzi__ilt], types.
            containers.UniTuple) and typemap[xddzi__ilt].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(xddzi__ilt))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for msjw__qjaua in func_ir.blocks.values():
        for stmt in msjw__qjaua.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    nby__cyyt = getattr(val, 'code', None)
                    if nby__cyyt is not None:
                        if getattr(val, 'closure', None) is not None:
                            rqvdt__dzvqj = (
                                '<creating a function from a closure>')
                            wkt__pelw = ''
                        else:
                            rqvdt__dzvqj = nby__cyyt.co_name
                            wkt__pelw = '(%s) ' % rqvdt__dzvqj
                    else:
                        rqvdt__dzvqj = '<could not ascertain use case>'
                        wkt__pelw = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (rqvdt__dzvqj, wkt__pelw))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                bgbu__lif = False
                if isinstance(val, pytypes.FunctionType):
                    bgbu__lif = val in {numba.gdb, numba.gdb_init}
                if not bgbu__lif:
                    bgbu__lif = getattr(val, '_name', '') == 'gdb_internal'
                if bgbu__lif:
                    aaipw__cnoj.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    tglvi__kqzy = func_ir.get_definition(var)
                    ovb__zajd = guard(find_callname, func_ir, tglvi__kqzy)
                    if ovb__zajd and ovb__zajd[1] == 'numpy':
                        ty = getattr(numpy, ovb__zajd[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    nyf__gum = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(nyf__gum), loc=stmt.loc)
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
    if len(aaipw__cnoj) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        jienv__qyzej = '\n'.join([x.strformat() for x in aaipw__cnoj])
        raise errors.UnsupportedError(msg % jienv__qyzej)


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
    gqepb__jjs, kmcq__vkeh = next(iter(val.items()))
    drorm__ind = typeof_impl(gqepb__jjs, c)
    vjbo__mgr = typeof_impl(kmcq__vkeh, c)
    if drorm__ind is None or vjbo__mgr is None:
        raise ValueError(
            f'Cannot type dict element type {type(gqepb__jjs)}, {type(kmcq__vkeh)}'
            )
    return types.DictType(drorm__ind, vjbo__mgr)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    vaufp__hcobp = cgutils.alloca_once_value(c.builder, val)
    yztzt__depn = c.pyapi.object_hasattr_string(val, '_opaque')
    obrgx__yzc = c.builder.icmp_unsigned('==', yztzt__depn, lir.Constant(
        yztzt__depn.type, 0))
    vrs__xvgpe = typ.key_type
    iifv__rfjl = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(vrs__xvgpe, iifv__rfjl)

    def copy_dict(out_dict, in_dict):
        for gqepb__jjs, kmcq__vkeh in in_dict.items():
            out_dict[gqepb__jjs] = kmcq__vkeh
    with c.builder.if_then(obrgx__yzc):
        zpbh__bjwg = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        uycuc__rnn = c.pyapi.call_function_objargs(zpbh__bjwg, [])
        pkms__soyou = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(pkms__soyou, [uycuc__rnn, val])
        c.builder.store(uycuc__rnn, vaufp__hcobp)
    val = c.builder.load(vaufp__hcobp)
    modeb__uiwxi = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    jcol__jwijt = c.pyapi.object_type(val)
    nflfe__rgth = c.builder.icmp_unsigned('==', jcol__jwijt, modeb__uiwxi)
    with c.builder.if_else(nflfe__rgth) as (cui__mjfue, bqu__agflw):
        with cui__mjfue:
            zpwgo__eio = c.pyapi.object_getattr_string(val, '_opaque')
            zsr__ifbr = types.MemInfoPointer(types.voidptr)
            collt__vkkd = c.unbox(zsr__ifbr, zpwgo__eio)
            mi = collt__vkkd.value
            umz__yspfk = zsr__ifbr, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *umz__yspfk)
            rjdnr__oqday = context.get_constant_null(umz__yspfk[1])
            args = mi, rjdnr__oqday
            lboaq__raz, mvet__vpav = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, mvet__vpav)
            c.pyapi.decref(zpwgo__eio)
            bmck__nth = c.builder.basic_block
        with bqu__agflw:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", jcol__jwijt, modeb__uiwxi)
            olgit__fjqvq = c.builder.basic_block
    nkasg__sewy = c.builder.phi(mvet__vpav.type)
    hmhvn__kqima = c.builder.phi(lboaq__raz.type)
    nkasg__sewy.add_incoming(mvet__vpav, bmck__nth)
    nkasg__sewy.add_incoming(mvet__vpav.type(None), olgit__fjqvq)
    hmhvn__kqima.add_incoming(lboaq__raz, bmck__nth)
    hmhvn__kqima.add_incoming(cgutils.true_bit, olgit__fjqvq)
    c.pyapi.decref(modeb__uiwxi)
    c.pyapi.decref(jcol__jwijt)
    with c.builder.if_then(obrgx__yzc):
        c.pyapi.decref(val)
    return NativeValue(nkasg__sewy, is_error=hmhvn__kqima)


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
    mlypb__zfxpi = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=mlypb__zfxpi, name=updatevar)
    ufc__fly = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=ufc__fly, name=res)


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
        for gqepb__jjs, kmcq__vkeh in other.items():
            d[gqepb__jjs] = kmcq__vkeh
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
    wkt__pelw = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(wkt__pelw, res)


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
    ndruc__vipt = PassManager(name)
    if state.func_ir is None:
        ndruc__vipt.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            ndruc__vipt.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        ndruc__vipt.add_pass(FixupArgs, 'fix up args')
    ndruc__vipt.add_pass(IRProcessing, 'processing IR')
    ndruc__vipt.add_pass(WithLifting, 'Handle with contexts')
    ndruc__vipt.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        ndruc__vipt.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        ndruc__vipt.add_pass(DeadBranchPrune, 'dead branch pruning')
        ndruc__vipt.add_pass(GenericRewrites, 'nopython rewrites')
    ndruc__vipt.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    ndruc__vipt.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        ndruc__vipt.add_pass(DeadBranchPrune, 'dead branch pruning')
    ndruc__vipt.add_pass(FindLiterallyCalls, 'find literally calls')
    ndruc__vipt.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        ndruc__vipt.add_pass(ReconstructSSA, 'ssa')
    ndruc__vipt.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    ndruc__vipt.finalize()
    return ndruc__vipt


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
    a, ktpcd__ikfbi = args
    if isinstance(a, types.List) and isinstance(ktpcd__ikfbi, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(ktpcd__ikfbi, types.List):
        return signature(ktpcd__ikfbi, types.intp, ktpcd__ikfbi)


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
        mwmsy__kns, qpvr__ghq = 0, 1
    else:
        mwmsy__kns, qpvr__ghq = 1, 0
    olp__xvkco = ListInstance(context, builder, sig.args[mwmsy__kns], args[
        mwmsy__kns])
    voftg__ikwe = olp__xvkco.size
    qml__hcne = args[qpvr__ghq]
    cakyb__gzt = lir.Constant(qml__hcne.type, 0)
    qml__hcne = builder.select(cgutils.is_neg_int(builder, qml__hcne),
        cakyb__gzt, qml__hcne)
    ynts__iva = builder.mul(qml__hcne, voftg__ikwe)
    kgssl__aprx = ListInstance.allocate(context, builder, sig.return_type,
        ynts__iva)
    kgssl__aprx.size = ynts__iva
    with cgutils.for_range_slice(builder, cakyb__gzt, ynts__iva,
        voftg__ikwe, inc=True) as (xne__ige, _):
        with cgutils.for_range(builder, voftg__ikwe) as yaff__boti:
            value = olp__xvkco.getitem(yaff__boti.index)
            kgssl__aprx.setitem(builder.add(yaff__boti.index, xne__ige),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, kgssl__aprx.
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
    uwp__asngb = first.unify(self, second)
    if uwp__asngb is not None:
        return uwp__asngb
    uwp__asngb = second.unify(self, first)
    if uwp__asngb is not None:
        return uwp__asngb
    bvz__phghd = self.can_convert(fromty=first, toty=second)
    if bvz__phghd is not None and bvz__phghd <= Conversion.safe:
        return second
    bvz__phghd = self.can_convert(fromty=second, toty=first)
    if bvz__phghd is not None and bvz__phghd <= Conversion.safe:
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
    ynts__iva = payload.used
    listobj = c.pyapi.list_new(ynts__iva)
    bbhq__uwjk = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(bbhq__uwjk, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(ynts__iva.
            type, 0))
        with payload._iterate() as yaff__boti:
            i = c.builder.load(index)
            item = yaff__boti.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return bbhq__uwjk, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    hou__lydyi = h.type
    oxh__fvspl = self.mask
    dtype = self._ty.dtype
    xkzyv__faf = context.typing_context
    fnty = xkzyv__faf.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(xkzyv__faf, (dtype, dtype), {})
    ffmp__adhfa = context.get_function(fnty, sig)
    gaqfe__olkj = ir.Constant(hou__lydyi, 1)
    wbjs__wdx = ir.Constant(hou__lydyi, 5)
    mdqs__ntcoh = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, oxh__fvspl))
    if for_insert:
        uusdd__qeq = oxh__fvspl.type(-1)
        oijjy__jff = cgutils.alloca_once_value(builder, uusdd__qeq)
    mtp__pzliy = builder.append_basic_block('lookup.body')
    twxs__kvwf = builder.append_basic_block('lookup.found')
    oze__satod = builder.append_basic_block('lookup.not_found')
    fqatm__bpxlp = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        wtxll__boy = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, wtxll__boy)):
            oqkl__aupq = ffmp__adhfa(builder, (item, entry.key))
            with builder.if_then(oqkl__aupq):
                builder.branch(twxs__kvwf)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, wtxll__boy)):
            builder.branch(oze__satod)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, wtxll__boy)):
                hspp__qfae = builder.load(oijjy__jff)
                hspp__qfae = builder.select(builder.icmp_unsigned('==',
                    hspp__qfae, uusdd__qeq), i, hspp__qfae)
                builder.store(hspp__qfae, oijjy__jff)
    with cgutils.for_range(builder, ir.Constant(hou__lydyi, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, gaqfe__olkj)
        i = builder.and_(i, oxh__fvspl)
        builder.store(i, index)
    builder.branch(mtp__pzliy)
    with builder.goto_block(mtp__pzliy):
        i = builder.load(index)
        check_entry(i)
        wtsfu__une = builder.load(mdqs__ntcoh)
        wtsfu__une = builder.lshr(wtsfu__une, wbjs__wdx)
        i = builder.add(gaqfe__olkj, builder.mul(i, wbjs__wdx))
        i = builder.and_(oxh__fvspl, builder.add(i, wtsfu__une))
        builder.store(i, index)
        builder.store(wtsfu__une, mdqs__ntcoh)
        builder.branch(mtp__pzliy)
    with builder.goto_block(oze__satod):
        if for_insert:
            i = builder.load(index)
            hspp__qfae = builder.load(oijjy__jff)
            i = builder.select(builder.icmp_unsigned('==', hspp__qfae,
                uusdd__qeq), i, hspp__qfae)
            builder.store(i, index)
        builder.branch(fqatm__bpxlp)
    with builder.goto_block(twxs__kvwf):
        builder.branch(fqatm__bpxlp)
    builder.position_at_end(fqatm__bpxlp)
    bgbu__lif = builder.phi(ir.IntType(1), 'found')
    bgbu__lif.add_incoming(cgutils.true_bit, twxs__kvwf)
    bgbu__lif.add_incoming(cgutils.false_bit, oze__satod)
    return bgbu__lif, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    ggjrh__acnn = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    ngn__vhp = payload.used
    gaqfe__olkj = ir.Constant(ngn__vhp.type, 1)
    ngn__vhp = payload.used = builder.add(ngn__vhp, gaqfe__olkj)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, ggjrh__acnn), likely=True):
        payload.fill = builder.add(payload.fill, gaqfe__olkj)
    if do_resize:
        self.upsize(ngn__vhp)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    bgbu__lif, i = payload._lookup(item, h, for_insert=True)
    sdg__cnlgy = builder.not_(bgbu__lif)
    with builder.if_then(sdg__cnlgy):
        entry = payload.get_entry(i)
        ggjrh__acnn = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        ngn__vhp = payload.used
        gaqfe__olkj = ir.Constant(ngn__vhp.type, 1)
        ngn__vhp = payload.used = builder.add(ngn__vhp, gaqfe__olkj)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, ggjrh__acnn), likely=True):
            payload.fill = builder.add(payload.fill, gaqfe__olkj)
        if do_resize:
            self.upsize(ngn__vhp)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    ngn__vhp = payload.used
    gaqfe__olkj = ir.Constant(ngn__vhp.type, 1)
    ngn__vhp = payload.used = self._builder.sub(ngn__vhp, gaqfe__olkj)
    if do_resize:
        self.downsize(ngn__vhp)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    jzkc__awl = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, jzkc__awl)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    xpodf__ebwt = payload
    bbhq__uwjk = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(bbhq__uwjk), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with xpodf__ebwt._iterate() as yaff__boti:
        entry = yaff__boti.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(xpodf__ebwt.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as yaff__boti:
        entry = yaff__boti.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    bbhq__uwjk = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(bbhq__uwjk), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    bbhq__uwjk = cgutils.alloca_once_value(builder, cgutils.true_bit)
    hou__lydyi = context.get_value_type(types.intp)
    cakyb__gzt = ir.Constant(hou__lydyi, 0)
    gaqfe__olkj = ir.Constant(hou__lydyi, 1)
    gjo__gzig = context.get_data_type(types.SetPayload(self._ty))
    vkxfp__osrpf = context.get_abi_sizeof(gjo__gzig)
    mru__hptu = self._entrysize
    vkxfp__osrpf -= mru__hptu
    ozni__ogu, lak__eqgml = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(hou__lydyi, mru__hptu), ir.Constant(hou__lydyi,
        vkxfp__osrpf))
    with builder.if_then(lak__eqgml, likely=False):
        builder.store(cgutils.false_bit, bbhq__uwjk)
    with builder.if_then(builder.load(bbhq__uwjk), likely=True):
        if realloc:
            vtfbx__rmfx = self._set.meminfo
            ypgf__zdy = context.nrt.meminfo_varsize_alloc(builder,
                vtfbx__rmfx, size=ozni__ogu)
            cqxo__fxs = cgutils.is_null(builder, ypgf__zdy)
        else:
            lya__eulyl = _imp_dtor(context, builder.module, self._ty)
            vtfbx__rmfx = context.nrt.meminfo_new_varsize_dtor(builder,
                ozni__ogu, builder.bitcast(lya__eulyl, cgutils.voidptr_t))
            cqxo__fxs = cgutils.is_null(builder, vtfbx__rmfx)
        with builder.if_else(cqxo__fxs, likely=False) as (mhtzw__oix,
            mvgw__wtrc):
            with mhtzw__oix:
                builder.store(cgutils.false_bit, bbhq__uwjk)
            with mvgw__wtrc:
                if not realloc:
                    self._set.meminfo = vtfbx__rmfx
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, ozni__ogu, 255)
                payload.used = cakyb__gzt
                payload.fill = cakyb__gzt
                payload.finger = cakyb__gzt
                hegf__ayttx = builder.sub(nentries, gaqfe__olkj)
                payload.mask = hegf__ayttx
    return builder.load(bbhq__uwjk)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    bbhq__uwjk = cgutils.alloca_once_value(builder, cgutils.true_bit)
    hou__lydyi = context.get_value_type(types.intp)
    cakyb__gzt = ir.Constant(hou__lydyi, 0)
    gaqfe__olkj = ir.Constant(hou__lydyi, 1)
    gjo__gzig = context.get_data_type(types.SetPayload(self._ty))
    vkxfp__osrpf = context.get_abi_sizeof(gjo__gzig)
    mru__hptu = self._entrysize
    vkxfp__osrpf -= mru__hptu
    oxh__fvspl = src_payload.mask
    nentries = builder.add(gaqfe__olkj, oxh__fvspl)
    ozni__ogu = builder.add(ir.Constant(hou__lydyi, vkxfp__osrpf), builder.
        mul(ir.Constant(hou__lydyi, mru__hptu), nentries))
    with builder.if_then(builder.load(bbhq__uwjk), likely=True):
        lya__eulyl = _imp_dtor(context, builder.module, self._ty)
        vtfbx__rmfx = context.nrt.meminfo_new_varsize_dtor(builder,
            ozni__ogu, builder.bitcast(lya__eulyl, cgutils.voidptr_t))
        cqxo__fxs = cgutils.is_null(builder, vtfbx__rmfx)
        with builder.if_else(cqxo__fxs, likely=False) as (mhtzw__oix,
            mvgw__wtrc):
            with mhtzw__oix:
                builder.store(cgutils.false_bit, bbhq__uwjk)
            with mvgw__wtrc:
                self._set.meminfo = vtfbx__rmfx
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = cakyb__gzt
                payload.mask = oxh__fvspl
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, mru__hptu)
                with src_payload._iterate() as yaff__boti:
                    context.nrt.incref(builder, self._ty.dtype, yaff__boti.
                        entry.key)
    return builder.load(bbhq__uwjk)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    tbkr__nzn = context.get_value_type(types.voidptr)
    kicod__ohovc = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [tbkr__nzn, kicod__ohovc, tbkr__nzn])
    umt__wwyim = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=umt__wwyim)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        ksyu__lkaui = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, ksyu__lkaui)
        with payload._iterate() as yaff__boti:
            entry = yaff__boti.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    zvqz__hunrr, = sig.args
    gagf__qjolw, = args
    htdc__slvqe = numba.core.imputils.call_len(context, builder,
        zvqz__hunrr, gagf__qjolw)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, htdc__slvqe)
    with numba.core.imputils.for_iter(context, builder, zvqz__hunrr,
        gagf__qjolw) as yaff__boti:
        inst.add(yaff__boti.value)
        context.nrt.decref(builder, set_type.dtype, yaff__boti.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    zvqz__hunrr = sig.args[1]
    gagf__qjolw = args[1]
    htdc__slvqe = numba.core.imputils.call_len(context, builder,
        zvqz__hunrr, gagf__qjolw)
    if htdc__slvqe is not None:
        mji__ubkzf = builder.add(inst.payload.used, htdc__slvqe)
        inst.upsize(mji__ubkzf)
    with numba.core.imputils.for_iter(context, builder, zvqz__hunrr,
        gagf__qjolw) as yaff__boti:
        aae__jdahz = context.cast(builder, yaff__boti.value, zvqz__hunrr.
            dtype, inst.dtype)
        inst.add(aae__jdahz)
        context.nrt.decref(builder, zvqz__hunrr.dtype, yaff__boti.value)
    if htdc__slvqe is not None:
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
    iblo__ezo = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, iblo__ezo, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    nzv__dnb = target_context.get_executable(library, fndesc, env)
    xfjb__szcm = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=nzv__dnb, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return xfjb__szcm


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
