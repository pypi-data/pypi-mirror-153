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
    eebbv__qmf = keyword_expr.items.copy()
    aip__onq = keyword_expr.value_indexes
    for pwz__ajvzw, fof__elioy in aip__onq.items():
        eebbv__qmf[fof__elioy] = pwz__ajvzw, eebbv__qmf[fof__elioy][1]
    new_body[buildmap_idx] = None
    return eebbv__qmf


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    hnzpj__btitd = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    eebbv__qmf = []
    rho__rkcdz = buildmap_idx + 1
    while rho__rkcdz <= search_end:
        dxhy__nia = body[rho__rkcdz]
        if not (isinstance(dxhy__nia, ir.Assign) and isinstance(dxhy__nia.
            value, ir.Const)):
            raise UnsupportedError(hnzpj__btitd)
        yrcp__msp = dxhy__nia.target.name
        ixzc__zjazy = dxhy__nia.value.value
        rho__rkcdz += 1
        qbokf__wzmtn = True
        while rho__rkcdz <= search_end and qbokf__wzmtn:
            pknl__nxb = body[rho__rkcdz]
            if (isinstance(pknl__nxb, ir.Assign) and isinstance(pknl__nxb.
                value, ir.Expr) and pknl__nxb.value.op == 'getattr' and 
                pknl__nxb.value.value.name == buildmap_name and pknl__nxb.
                value.attr == '__setitem__'):
                qbokf__wzmtn = False
            else:
                rho__rkcdz += 1
        if qbokf__wzmtn or rho__rkcdz == search_end:
            raise UnsupportedError(hnzpj__btitd)
        bwbh__dslvz = body[rho__rkcdz + 1]
        if not (isinstance(bwbh__dslvz, ir.Assign) and isinstance(
            bwbh__dslvz.value, ir.Expr) and bwbh__dslvz.value.op == 'call' and
            bwbh__dslvz.value.func.name == pknl__nxb.target.name and len(
            bwbh__dslvz.value.args) == 2 and bwbh__dslvz.value.args[0].name ==
            yrcp__msp):
            raise UnsupportedError(hnzpj__btitd)
        rcoc__inedb = bwbh__dslvz.value.args[1]
        eebbv__qmf.append((ixzc__zjazy, rcoc__inedb))
        new_body[rho__rkcdz] = None
        new_body[rho__rkcdz + 1] = None
        rho__rkcdz += 2
    return eebbv__qmf


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    hnzpj__btitd = 'CALL_FUNCTION_EX with **kwargs not supported'
    rho__rkcdz = 0
    ivqer__fcjk = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        jwni__oljy = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        jwni__oljy = vararg_stmt.target.name
    jkcpz__kzk = True
    while search_end >= rho__rkcdz and jkcpz__kzk:
        ocm__olbvh = body[search_end]
        if (isinstance(ocm__olbvh, ir.Assign) and ocm__olbvh.target.name ==
            jwni__oljy and isinstance(ocm__olbvh.value, ir.Expr) and 
            ocm__olbvh.value.op == 'build_tuple' and not ocm__olbvh.value.items
            ):
            jkcpz__kzk = False
            new_body[search_end] = None
        else:
            if search_end == rho__rkcdz or not (isinstance(ocm__olbvh, ir.
                Assign) and ocm__olbvh.target.name == jwni__oljy and
                isinstance(ocm__olbvh.value, ir.Expr) and ocm__olbvh.value.
                op == 'binop' and ocm__olbvh.value.fn == operator.add):
                raise UnsupportedError(hnzpj__btitd)
            fnyji__qoj = ocm__olbvh.value.lhs.name
            rqajm__rkyu = ocm__olbvh.value.rhs.name
            ofi__uic = body[search_end - 1]
            if not (isinstance(ofi__uic, ir.Assign) and isinstance(ofi__uic
                .value, ir.Expr) and ofi__uic.value.op == 'build_tuple' and
                len(ofi__uic.value.items) == 1):
                raise UnsupportedError(hnzpj__btitd)
            if ofi__uic.target.name == fnyji__qoj:
                jwni__oljy = rqajm__rkyu
            elif ofi__uic.target.name == rqajm__rkyu:
                jwni__oljy = fnyji__qoj
            else:
                raise UnsupportedError(hnzpj__btitd)
            ivqer__fcjk.append(ofi__uic.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            ori__xmj = True
            while search_end >= rho__rkcdz and ori__xmj:
                zye__glruv = body[search_end]
                if isinstance(zye__glruv, ir.Assign
                    ) and zye__glruv.target.name == jwni__oljy:
                    ori__xmj = False
                else:
                    search_end -= 1
    if jkcpz__kzk:
        raise UnsupportedError(hnzpj__btitd)
    return ivqer__fcjk[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    hnzpj__btitd = 'CALL_FUNCTION_EX with **kwargs not supported'
    for ssqk__kerz in func_ir.blocks.values():
        yrpoi__vtfkl = False
        new_body = []
        for eilz__hybhl, ylqqf__qzly in enumerate(ssqk__kerz.body):
            if (isinstance(ylqqf__qzly, ir.Assign) and isinstance(
                ylqqf__qzly.value, ir.Expr) and ylqqf__qzly.value.op ==
                'call' and ylqqf__qzly.value.varkwarg is not None):
                yrpoi__vtfkl = True
                jokf__ine = ylqqf__qzly.value
                args = jokf__ine.args
                eebbv__qmf = jokf__ine.kws
                awne__hpja = jokf__ine.vararg
                luid__qxkn = jokf__ine.varkwarg
                dwhq__jvgfq = eilz__hybhl - 1
                bltzi__wqstq = dwhq__jvgfq
                gqodk__qtxq = None
                mlun__vgu = True
                while bltzi__wqstq >= 0 and mlun__vgu:
                    gqodk__qtxq = ssqk__kerz.body[bltzi__wqstq]
                    if isinstance(gqodk__qtxq, ir.Assign
                        ) and gqodk__qtxq.target.name == luid__qxkn.name:
                        mlun__vgu = False
                    else:
                        bltzi__wqstq -= 1
                if eebbv__qmf or mlun__vgu or not (isinstance(gqodk__qtxq.
                    value, ir.Expr) and gqodk__qtxq.value.op == 'build_map'):
                    raise UnsupportedError(hnzpj__btitd)
                if gqodk__qtxq.value.items:
                    eebbv__qmf = _call_function_ex_replace_kws_small(
                        gqodk__qtxq.value, new_body, bltzi__wqstq)
                else:
                    eebbv__qmf = _call_function_ex_replace_kws_large(ssqk__kerz
                        .body, luid__qxkn.name, bltzi__wqstq, eilz__hybhl -
                        1, new_body)
                dwhq__jvgfq = bltzi__wqstq
                if awne__hpja is not None:
                    if args:
                        raise UnsupportedError(hnzpj__btitd)
                    crqfw__lyxhg = dwhq__jvgfq
                    vfkpg__qydt = None
                    mlun__vgu = True
                    while crqfw__lyxhg >= 0 and mlun__vgu:
                        vfkpg__qydt = ssqk__kerz.body[crqfw__lyxhg]
                        if isinstance(vfkpg__qydt, ir.Assign
                            ) and vfkpg__qydt.target.name == awne__hpja.name:
                            mlun__vgu = False
                        else:
                            crqfw__lyxhg -= 1
                    if mlun__vgu:
                        raise UnsupportedError(hnzpj__btitd)
                    if isinstance(vfkpg__qydt.value, ir.Expr
                        ) and vfkpg__qydt.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(vfkpg__qydt
                            .value, new_body, crqfw__lyxhg)
                    else:
                        args = _call_function_ex_replace_args_large(vfkpg__qydt
                            , ssqk__kerz.body, new_body, crqfw__lyxhg)
                xswl__ateu = ir.Expr.call(jokf__ine.func, args, eebbv__qmf,
                    jokf__ine.loc, target=jokf__ine.target)
                if ylqqf__qzly.target.name in func_ir._definitions and len(
                    func_ir._definitions[ylqqf__qzly.target.name]) == 1:
                    func_ir._definitions[ylqqf__qzly.target.name].clear()
                func_ir._definitions[ylqqf__qzly.target.name].append(xswl__ateu
                    )
                ylqqf__qzly = ir.Assign(xswl__ateu, ylqqf__qzly.target,
                    ylqqf__qzly.loc)
            new_body.append(ylqqf__qzly)
        if yrpoi__vtfkl:
            ssqk__kerz.body = [xma__kyn for xma__kyn in new_body if 
                xma__kyn is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for ssqk__kerz in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        yrpoi__vtfkl = False
        for eilz__hybhl, ylqqf__qzly in enumerate(ssqk__kerz.body):
            cdl__gzr = True
            snyll__xnm = None
            if isinstance(ylqqf__qzly, ir.Assign) and isinstance(ylqqf__qzly
                .value, ir.Expr):
                if ylqqf__qzly.value.op == 'build_map':
                    snyll__xnm = ylqqf__qzly.target.name
                    lit_old_idx[ylqqf__qzly.target.name] = eilz__hybhl
                    lit_new_idx[ylqqf__qzly.target.name] = eilz__hybhl
                    map_updates[ylqqf__qzly.target.name
                        ] = ylqqf__qzly.value.items.copy()
                    cdl__gzr = False
                elif ylqqf__qzly.value.op == 'call' and eilz__hybhl > 0:
                    qtvbu__rkqz = ylqqf__qzly.value.func.name
                    pknl__nxb = ssqk__kerz.body[eilz__hybhl - 1]
                    args = ylqqf__qzly.value.args
                    if (isinstance(pknl__nxb, ir.Assign) and pknl__nxb.
                        target.name == qtvbu__rkqz and isinstance(pknl__nxb
                        .value, ir.Expr) and pknl__nxb.value.op ==
                        'getattr' and pknl__nxb.value.value.name in lit_old_idx
                        ):
                        xjgs__whm = pknl__nxb.value.value.name
                        xzo__bpmg = pknl__nxb.value.attr
                        if xzo__bpmg == '__setitem__':
                            cdl__gzr = False
                            map_updates[xjgs__whm].append(args)
                            new_body[-1] = None
                        elif xzo__bpmg == 'update' and args[0
                            ].name in lit_old_idx:
                            cdl__gzr = False
                            map_updates[xjgs__whm].extend(map_updates[args[
                                0].name])
                            new_body[-1] = None
                        if not cdl__gzr:
                            lit_new_idx[xjgs__whm] = eilz__hybhl
                            func_ir._definitions[pknl__nxb.target.name].remove(
                                pknl__nxb.value)
            if not (isinstance(ylqqf__qzly, ir.Assign) and isinstance(
                ylqqf__qzly.value, ir.Expr) and ylqqf__qzly.value.op ==
                'getattr' and ylqqf__qzly.value.value.name in lit_old_idx and
                ylqqf__qzly.value.attr in ('__setitem__', 'update')):
                for hqn__mjkf in ylqqf__qzly.list_vars():
                    if (hqn__mjkf.name in lit_old_idx and hqn__mjkf.name !=
                        snyll__xnm):
                        _insert_build_map(func_ir, hqn__mjkf.name,
                            ssqk__kerz.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if cdl__gzr:
                new_body.append(ylqqf__qzly)
            else:
                func_ir._definitions[ylqqf__qzly.target.name].remove(
                    ylqqf__qzly.value)
                yrpoi__vtfkl = True
                new_body.append(None)
        zuhp__qibr = list(lit_old_idx.keys())
        for juqow__tag in zuhp__qibr:
            _insert_build_map(func_ir, juqow__tag, ssqk__kerz.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if yrpoi__vtfkl:
            ssqk__kerz.body = [xma__kyn for xma__kyn in new_body if 
                xma__kyn is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    yfa__uxbh = lit_old_idx[name]
    iuuh__fbwe = lit_new_idx[name]
    fny__ahqpd = map_updates[name]
    new_body[iuuh__fbwe] = _build_new_build_map(func_ir, name, old_body,
        yfa__uxbh, fny__ahqpd)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    nlmpf__bmvm = old_body[old_lineno]
    ojfr__alc = nlmpf__bmvm.target
    tchp__bvqjc = nlmpf__bmvm.value
    mlddi__guvze = []
    eni__dzqv = []
    for ifkvh__riga in new_items:
        attx__pqr, bbqtk__egqm = ifkvh__riga
        jkew__lurni = guard(get_definition, func_ir, attx__pqr)
        if isinstance(jkew__lurni, (ir.Const, ir.Global, ir.FreeVar)):
            mlddi__guvze.append(jkew__lurni.value)
        quha__zzsv = guard(get_definition, func_ir, bbqtk__egqm)
        if isinstance(quha__zzsv, (ir.Const, ir.Global, ir.FreeVar)):
            eni__dzqv.append(quha__zzsv.value)
        else:
            eni__dzqv.append(numba.core.interpreter._UNKNOWN_VALUE(
                bbqtk__egqm.name))
    aip__onq = {}
    if len(mlddi__guvze) == len(new_items):
        zhn__ttzy = {xma__kyn: xhfbt__sjt for xma__kyn, xhfbt__sjt in zip(
            mlddi__guvze, eni__dzqv)}
        for eilz__hybhl, attx__pqr in enumerate(mlddi__guvze):
            aip__onq[attx__pqr] = eilz__hybhl
    else:
        zhn__ttzy = None
    loe__aqf = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=zhn__ttzy, value_indexes=aip__onq, loc=tchp__bvqjc.loc)
    func_ir._definitions[name].append(loe__aqf)
    return ir.Assign(loe__aqf, ir.Var(ojfr__alc.scope, name, ojfr__alc.loc),
        loe__aqf.loc)
