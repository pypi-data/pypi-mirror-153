"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        return True


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    depq__azqca = keyword_expr.items.copy()
    exi__xitj = keyword_expr.value_indexes
    for tqvrg__npvko, vttw__frg in exi__xitj.items():
        depq__azqca[vttw__frg] = tqvrg__npvko, depq__azqca[vttw__frg][1]
    new_body[buildmap_idx] = None
    return depq__azqca


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    bpazo__ojhij = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    depq__azqca = []
    ubkmo__cxe = buildmap_idx + 1
    while ubkmo__cxe <= search_end:
        tnrob__rsb = body[ubkmo__cxe]
        if not (isinstance(tnrob__rsb, ir.Assign) and isinstance(tnrob__rsb
            .value, ir.Const)):
            raise UnsupportedError(bpazo__ojhij)
        ulcy__xss = tnrob__rsb.target.name
        lrn__wtdo = tnrob__rsb.value.value
        ubkmo__cxe += 1
        fdef__raf = True
        while ubkmo__cxe <= search_end and fdef__raf:
            wcoxm__cgag = body[ubkmo__cxe]
            if (isinstance(wcoxm__cgag, ir.Assign) and isinstance(
                wcoxm__cgag.value, ir.Expr) and wcoxm__cgag.value.op ==
                'getattr' and wcoxm__cgag.value.value.name == buildmap_name and
                wcoxm__cgag.value.attr == '__setitem__'):
                fdef__raf = False
            else:
                ubkmo__cxe += 1
        if fdef__raf or ubkmo__cxe == search_end:
            raise UnsupportedError(bpazo__ojhij)
        pxql__tsmsr = body[ubkmo__cxe + 1]
        if not (isinstance(pxql__tsmsr, ir.Assign) and isinstance(
            pxql__tsmsr.value, ir.Expr) and pxql__tsmsr.value.op == 'call' and
            pxql__tsmsr.value.func.name == wcoxm__cgag.target.name and len(
            pxql__tsmsr.value.args) == 2 and pxql__tsmsr.value.args[0].name ==
            ulcy__xss):
            raise UnsupportedError(bpazo__ojhij)
        pigcg__ary = pxql__tsmsr.value.args[1]
        depq__azqca.append((lrn__wtdo, pigcg__ary))
        new_body[ubkmo__cxe] = None
        new_body[ubkmo__cxe + 1] = None
        ubkmo__cxe += 2
    return depq__azqca


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    bpazo__ojhij = 'CALL_FUNCTION_EX with **kwargs not supported'
    ubkmo__cxe = 0
    lvw__hgxi = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        yfyhi__gzn = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        yfyhi__gzn = vararg_stmt.target.name
    qyaps__dfo = True
    while search_end >= ubkmo__cxe and qyaps__dfo:
        rzloa__vrl = body[search_end]
        if (isinstance(rzloa__vrl, ir.Assign) and rzloa__vrl.target.name ==
            yfyhi__gzn and isinstance(rzloa__vrl.value, ir.Expr) and 
            rzloa__vrl.value.op == 'build_tuple' and not rzloa__vrl.value.items
            ):
            qyaps__dfo = False
            new_body[search_end] = None
        else:
            if search_end == ubkmo__cxe or not (isinstance(rzloa__vrl, ir.
                Assign) and rzloa__vrl.target.name == yfyhi__gzn and
                isinstance(rzloa__vrl.value, ir.Expr) and rzloa__vrl.value.
                op == 'binop' and rzloa__vrl.value.fn == operator.add):
                raise UnsupportedError(bpazo__ojhij)
            abxrz__ncxgn = rzloa__vrl.value.lhs.name
            vkrco__onnc = rzloa__vrl.value.rhs.name
            xvhuc__amzdz = body[search_end - 1]
            if not (isinstance(xvhuc__amzdz, ir.Assign) and isinstance(
                xvhuc__amzdz.value, ir.Expr) and xvhuc__amzdz.value.op ==
                'build_tuple' and len(xvhuc__amzdz.value.items) == 1):
                raise UnsupportedError(bpazo__ojhij)
            if xvhuc__amzdz.target.name == abxrz__ncxgn:
                yfyhi__gzn = vkrco__onnc
            elif xvhuc__amzdz.target.name == vkrco__onnc:
                yfyhi__gzn = abxrz__ncxgn
            else:
                raise UnsupportedError(bpazo__ojhij)
            lvw__hgxi.append(xvhuc__amzdz.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            pmd__lwoi = True
            while search_end >= ubkmo__cxe and pmd__lwoi:
                owih__ptw = body[search_end]
                if isinstance(owih__ptw, ir.Assign
                    ) and owih__ptw.target.name == yfyhi__gzn:
                    pmd__lwoi = False
                else:
                    search_end -= 1
    if qyaps__dfo:
        raise UnsupportedError(bpazo__ojhij)
    return lvw__hgxi[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    bpazo__ojhij = 'CALL_FUNCTION_EX with **kwargs not supported'
    for qfvih__cshwf in func_ir.blocks.values():
        fbw__frdlm = False
        new_body = []
        for irfi__iupb, dexw__zhs in enumerate(qfvih__cshwf.body):
            if (isinstance(dexw__zhs, ir.Assign) and isinstance(dexw__zhs.
                value, ir.Expr) and dexw__zhs.value.op == 'call' and 
                dexw__zhs.value.varkwarg is not None):
                fbw__frdlm = True
                vmw__cts = dexw__zhs.value
                args = vmw__cts.args
                depq__azqca = vmw__cts.kws
                sdthh__zzbw = vmw__cts.vararg
                zrhw__loccz = vmw__cts.varkwarg
                dan__eiba = irfi__iupb - 1
                noc__lovon = dan__eiba
                ztj__phx = None
                oarsi__fjgdd = True
                while noc__lovon >= 0 and oarsi__fjgdd:
                    ztj__phx = qfvih__cshwf.body[noc__lovon]
                    if isinstance(ztj__phx, ir.Assign
                        ) and ztj__phx.target.name == zrhw__loccz.name:
                        oarsi__fjgdd = False
                    else:
                        noc__lovon -= 1
                if depq__azqca or oarsi__fjgdd or not (isinstance(ztj__phx.
                    value, ir.Expr) and ztj__phx.value.op == 'build_map'):
                    raise UnsupportedError(bpazo__ojhij)
                if ztj__phx.value.items:
                    depq__azqca = _call_function_ex_replace_kws_small(ztj__phx
                        .value, new_body, noc__lovon)
                else:
                    depq__azqca = _call_function_ex_replace_kws_large(
                        qfvih__cshwf.body, zrhw__loccz.name, noc__lovon, 
                        irfi__iupb - 1, new_body)
                dan__eiba = noc__lovon
                if sdthh__zzbw is not None:
                    if args:
                        raise UnsupportedError(bpazo__ojhij)
                    xnh__inci = dan__eiba
                    hbisx__sajgx = None
                    oarsi__fjgdd = True
                    while xnh__inci >= 0 and oarsi__fjgdd:
                        hbisx__sajgx = qfvih__cshwf.body[xnh__inci]
                        if isinstance(hbisx__sajgx, ir.Assign
                            ) and hbisx__sajgx.target.name == sdthh__zzbw.name:
                            oarsi__fjgdd = False
                        else:
                            xnh__inci -= 1
                    if oarsi__fjgdd:
                        raise UnsupportedError(bpazo__ojhij)
                    if isinstance(hbisx__sajgx.value, ir.Expr
                        ) and hbisx__sajgx.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(
                            hbisx__sajgx.value, new_body, xnh__inci)
                    else:
                        args = _call_function_ex_replace_args_large(
                            hbisx__sajgx, qfvih__cshwf.body, new_body,
                            xnh__inci)
                uhcv__tmtlv = ir.Expr.call(vmw__cts.func, args, depq__azqca,
                    vmw__cts.loc, target=vmw__cts.target)
                if dexw__zhs.target.name in func_ir._definitions and len(
                    func_ir._definitions[dexw__zhs.target.name]) == 1:
                    func_ir._definitions[dexw__zhs.target.name].clear()
                func_ir._definitions[dexw__zhs.target.name].append(uhcv__tmtlv)
                dexw__zhs = ir.Assign(uhcv__tmtlv, dexw__zhs.target,
                    dexw__zhs.loc)
            new_body.append(dexw__zhs)
        if fbw__frdlm:
            qfvih__cshwf.body = [wcstn__rfx for wcstn__rfx in new_body if 
                wcstn__rfx is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for qfvih__cshwf in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        fbw__frdlm = False
        for irfi__iupb, dexw__zhs in enumerate(qfvih__cshwf.body):
            tdm__espeo = True
            kum__rxt = None
            if isinstance(dexw__zhs, ir.Assign) and isinstance(dexw__zhs.
                value, ir.Expr):
                if dexw__zhs.value.op == 'build_map':
                    kum__rxt = dexw__zhs.target.name
                    lit_old_idx[dexw__zhs.target.name] = irfi__iupb
                    lit_new_idx[dexw__zhs.target.name] = irfi__iupb
                    map_updates[dexw__zhs.target.name
                        ] = dexw__zhs.value.items.copy()
                    tdm__espeo = False
                elif dexw__zhs.value.op == 'call' and irfi__iupb > 0:
                    bqdc__hxx = dexw__zhs.value.func.name
                    wcoxm__cgag = qfvih__cshwf.body[irfi__iupb - 1]
                    args = dexw__zhs.value.args
                    if (isinstance(wcoxm__cgag, ir.Assign) and wcoxm__cgag.
                        target.name == bqdc__hxx and isinstance(wcoxm__cgag
                        .value, ir.Expr) and wcoxm__cgag.value.op ==
                        'getattr' and wcoxm__cgag.value.value.name in
                        lit_old_idx):
                        ygg__erwsh = wcoxm__cgag.value.value.name
                        xfv__sjol = wcoxm__cgag.value.attr
                        if xfv__sjol == '__setitem__':
                            tdm__espeo = False
                            map_updates[ygg__erwsh].append(args)
                            new_body[-1] = None
                        elif xfv__sjol == 'update' and args[0
                            ].name in lit_old_idx:
                            tdm__espeo = False
                            map_updates[ygg__erwsh].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not tdm__espeo:
                            lit_new_idx[ygg__erwsh] = irfi__iupb
                            func_ir._definitions[wcoxm__cgag.target.name
                                ].remove(wcoxm__cgag.value)
            if not (isinstance(dexw__zhs, ir.Assign) and isinstance(
                dexw__zhs.value, ir.Expr) and dexw__zhs.value.op ==
                'getattr' and dexw__zhs.value.value.name in lit_old_idx and
                dexw__zhs.value.attr in ('__setitem__', 'update')):
                for qejey__nnber in dexw__zhs.list_vars():
                    if (qejey__nnber.name in lit_old_idx and qejey__nnber.
                        name != kum__rxt):
                        _insert_build_map(func_ir, qejey__nnber.name,
                            qfvih__cshwf.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if tdm__espeo:
                new_body.append(dexw__zhs)
            else:
                func_ir._definitions[dexw__zhs.target.name].remove(dexw__zhs
                    .value)
                fbw__frdlm = True
                new_body.append(None)
        ymbcr__zyje = list(lit_old_idx.keys())
        for cae__gxon in ymbcr__zyje:
            _insert_build_map(func_ir, cae__gxon, qfvih__cshwf.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if fbw__frdlm:
            qfvih__cshwf.body = [wcstn__rfx for wcstn__rfx in new_body if 
                wcstn__rfx is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    hpwqk__ttf = lit_old_idx[name]
    lhg__qrfqp = lit_new_idx[name]
    opsz__jfu = map_updates[name]
    new_body[lhg__qrfqp] = _build_new_build_map(func_ir, name, old_body,
        hpwqk__ttf, opsz__jfu)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    bkngu__xsf = old_body[old_lineno]
    leiwf__con = bkngu__xsf.target
    zljr__bsclu = bkngu__xsf.value
    irvvf__woyir = []
    atdk__vidx = []
    for oaktb__rfv in new_items:
        bgw__tcsl, mzsn__wujb = oaktb__rfv
        ymo__xpoy = guard(get_definition, func_ir, bgw__tcsl)
        if isinstance(ymo__xpoy, (ir.Const, ir.Global, ir.FreeVar)):
            irvvf__woyir.append(ymo__xpoy.value)
        oysd__ulw = guard(get_definition, func_ir, mzsn__wujb)
        if isinstance(oysd__ulw, (ir.Const, ir.Global, ir.FreeVar)):
            atdk__vidx.append(oysd__ulw.value)
        else:
            atdk__vidx.append(numba.core.interpreter._UNKNOWN_VALUE(
                mzsn__wujb.name))
    exi__xitj = {}
    if len(irvvf__woyir) == len(new_items):
        fgbn__zpypy = {wcstn__rfx: rknho__xff for wcstn__rfx, rknho__xff in
            zip(irvvf__woyir, atdk__vidx)}
        for irfi__iupb, bgw__tcsl in enumerate(irvvf__woyir):
            exi__xitj[bgw__tcsl] = irfi__iupb
    else:
        fgbn__zpypy = None
    eotjp__rzypb = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=fgbn__zpypy, value_indexes=exi__xitj, loc=zljr__bsclu.loc
        )
    func_ir._definitions[name].append(eotjp__rzypb)
    return ir.Assign(eotjp__rzypb, ir.Var(leiwf__con.scope, name,
        leiwf__con.loc), eotjp__rzypb.loc)
