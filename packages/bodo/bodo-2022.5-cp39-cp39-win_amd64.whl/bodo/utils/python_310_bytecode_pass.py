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
    jxagk__juthq = keyword_expr.items.copy()
    gvw__zgl = keyword_expr.value_indexes
    for mvnzy__yuvfj, xugl__smai in gvw__zgl.items():
        jxagk__juthq[xugl__smai] = mvnzy__yuvfj, jxagk__juthq[xugl__smai][1]
    new_body[buildmap_idx] = None
    return jxagk__juthq


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    lcnh__kxc = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    jxagk__juthq = []
    neq__exhrj = buildmap_idx + 1
    while neq__exhrj <= search_end:
        rqnau__wda = body[neq__exhrj]
        if not (isinstance(rqnau__wda, ir.Assign) and isinstance(rqnau__wda
            .value, ir.Const)):
            raise UnsupportedError(lcnh__kxc)
        shvip__pvsuy = rqnau__wda.target.name
        naw__cblgt = rqnau__wda.value.value
        neq__exhrj += 1
        ndn__vgk = True
        while neq__exhrj <= search_end and ndn__vgk:
            ozd__nqy = body[neq__exhrj]
            if (isinstance(ozd__nqy, ir.Assign) and isinstance(ozd__nqy.
                value, ir.Expr) and ozd__nqy.value.op == 'getattr' and 
                ozd__nqy.value.value.name == buildmap_name and ozd__nqy.
                value.attr == '__setitem__'):
                ndn__vgk = False
            else:
                neq__exhrj += 1
        if ndn__vgk or neq__exhrj == search_end:
            raise UnsupportedError(lcnh__kxc)
        dec__snagm = body[neq__exhrj + 1]
        if not (isinstance(dec__snagm, ir.Assign) and isinstance(dec__snagm
            .value, ir.Expr) and dec__snagm.value.op == 'call' and 
            dec__snagm.value.func.name == ozd__nqy.target.name and len(
            dec__snagm.value.args) == 2 and dec__snagm.value.args[0].name ==
            shvip__pvsuy):
            raise UnsupportedError(lcnh__kxc)
        sbfuv__ivdnw = dec__snagm.value.args[1]
        jxagk__juthq.append((naw__cblgt, sbfuv__ivdnw))
        new_body[neq__exhrj] = None
        new_body[neq__exhrj + 1] = None
        neq__exhrj += 2
    return jxagk__juthq


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    lcnh__kxc = 'CALL_FUNCTION_EX with **kwargs not supported'
    neq__exhrj = 0
    hheln__obwee = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        ulyoq__mbhzp = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        ulyoq__mbhzp = vararg_stmt.target.name
    pmnl__nbpo = True
    while search_end >= neq__exhrj and pmnl__nbpo:
        prfty__doxe = body[search_end]
        if (isinstance(prfty__doxe, ir.Assign) and prfty__doxe.target.name ==
            ulyoq__mbhzp and isinstance(prfty__doxe.value, ir.Expr) and 
            prfty__doxe.value.op == 'build_tuple' and not prfty__doxe.value
            .items):
            pmnl__nbpo = False
            new_body[search_end] = None
        else:
            if search_end == neq__exhrj or not (isinstance(prfty__doxe, ir.
                Assign) and prfty__doxe.target.name == ulyoq__mbhzp and
                isinstance(prfty__doxe.value, ir.Expr) and prfty__doxe.
                value.op == 'binop' and prfty__doxe.value.fn == operator.add):
                raise UnsupportedError(lcnh__kxc)
            okgi__zbwv = prfty__doxe.value.lhs.name
            qwrhy__eloeu = prfty__doxe.value.rhs.name
            ecevy__arox = body[search_end - 1]
            if not (isinstance(ecevy__arox, ir.Assign) and isinstance(
                ecevy__arox.value, ir.Expr) and ecevy__arox.value.op ==
                'build_tuple' and len(ecevy__arox.value.items) == 1):
                raise UnsupportedError(lcnh__kxc)
            if ecevy__arox.target.name == okgi__zbwv:
                ulyoq__mbhzp = qwrhy__eloeu
            elif ecevy__arox.target.name == qwrhy__eloeu:
                ulyoq__mbhzp = okgi__zbwv
            else:
                raise UnsupportedError(lcnh__kxc)
            hheln__obwee.append(ecevy__arox.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            nbfo__wdqc = True
            while search_end >= neq__exhrj and nbfo__wdqc:
                jhyfh__qnoh = body[search_end]
                if isinstance(jhyfh__qnoh, ir.Assign
                    ) and jhyfh__qnoh.target.name == ulyoq__mbhzp:
                    nbfo__wdqc = False
                else:
                    search_end -= 1
    if pmnl__nbpo:
        raise UnsupportedError(lcnh__kxc)
    return hheln__obwee[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    lcnh__kxc = 'CALL_FUNCTION_EX with **kwargs not supported'
    for gljyq__yjbrk in func_ir.blocks.values():
        xfujo__qfkew = False
        new_body = []
        for vnno__lrfmv, capb__hcei in enumerate(gljyq__yjbrk.body):
            if (isinstance(capb__hcei, ir.Assign) and isinstance(capb__hcei
                .value, ir.Expr) and capb__hcei.value.op == 'call' and 
                capb__hcei.value.varkwarg is not None):
                xfujo__qfkew = True
                oix__odfg = capb__hcei.value
                args = oix__odfg.args
                jxagk__juthq = oix__odfg.kws
                ykcgu__dzu = oix__odfg.vararg
                akg__gchd = oix__odfg.varkwarg
                svyjq__ptkvs = vnno__lrfmv - 1
                hbrk__dspxp = svyjq__ptkvs
                arrr__kmlk = None
                qecuu__rpj = True
                while hbrk__dspxp >= 0 and qecuu__rpj:
                    arrr__kmlk = gljyq__yjbrk.body[hbrk__dspxp]
                    if isinstance(arrr__kmlk, ir.Assign
                        ) and arrr__kmlk.target.name == akg__gchd.name:
                        qecuu__rpj = False
                    else:
                        hbrk__dspxp -= 1
                if jxagk__juthq or qecuu__rpj or not (isinstance(arrr__kmlk
                    .value, ir.Expr) and arrr__kmlk.value.op == 'build_map'):
                    raise UnsupportedError(lcnh__kxc)
                if arrr__kmlk.value.items:
                    jxagk__juthq = _call_function_ex_replace_kws_small(
                        arrr__kmlk.value, new_body, hbrk__dspxp)
                else:
                    jxagk__juthq = _call_function_ex_replace_kws_large(
                        gljyq__yjbrk.body, akg__gchd.name, hbrk__dspxp, 
                        vnno__lrfmv - 1, new_body)
                svyjq__ptkvs = hbrk__dspxp
                if ykcgu__dzu is not None:
                    if args:
                        raise UnsupportedError(lcnh__kxc)
                    fvvo__iawv = svyjq__ptkvs
                    cpzrd__hrpv = None
                    qecuu__rpj = True
                    while fvvo__iawv >= 0 and qecuu__rpj:
                        cpzrd__hrpv = gljyq__yjbrk.body[fvvo__iawv]
                        if isinstance(cpzrd__hrpv, ir.Assign
                            ) and cpzrd__hrpv.target.name == ykcgu__dzu.name:
                            qecuu__rpj = False
                        else:
                            fvvo__iawv -= 1
                    if qecuu__rpj:
                        raise UnsupportedError(lcnh__kxc)
                    if isinstance(cpzrd__hrpv.value, ir.Expr
                        ) and cpzrd__hrpv.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(cpzrd__hrpv
                            .value, new_body, fvvo__iawv)
                    else:
                        args = _call_function_ex_replace_args_large(cpzrd__hrpv
                            , gljyq__yjbrk.body, new_body, fvvo__iawv)
                guwb__dfw = ir.Expr.call(oix__odfg.func, args, jxagk__juthq,
                    oix__odfg.loc, target=oix__odfg.target)
                if capb__hcei.target.name in func_ir._definitions and len(
                    func_ir._definitions[capb__hcei.target.name]) == 1:
                    func_ir._definitions[capb__hcei.target.name].clear()
                func_ir._definitions[capb__hcei.target.name].append(guwb__dfw)
                capb__hcei = ir.Assign(guwb__dfw, capb__hcei.target,
                    capb__hcei.loc)
            new_body.append(capb__hcei)
        if xfujo__qfkew:
            gljyq__yjbrk.body = [rcasb__jmvy for rcasb__jmvy in new_body if
                rcasb__jmvy is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for gljyq__yjbrk in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        xfujo__qfkew = False
        for vnno__lrfmv, capb__hcei in enumerate(gljyq__yjbrk.body):
            cut__pnjy = True
            tlzs__nzh = None
            if isinstance(capb__hcei, ir.Assign) and isinstance(capb__hcei.
                value, ir.Expr):
                if capb__hcei.value.op == 'build_map':
                    tlzs__nzh = capb__hcei.target.name
                    lit_old_idx[capb__hcei.target.name] = vnno__lrfmv
                    lit_new_idx[capb__hcei.target.name] = vnno__lrfmv
                    map_updates[capb__hcei.target.name
                        ] = capb__hcei.value.items.copy()
                    cut__pnjy = False
                elif capb__hcei.value.op == 'call' and vnno__lrfmv > 0:
                    kqp__sco = capb__hcei.value.func.name
                    ozd__nqy = gljyq__yjbrk.body[vnno__lrfmv - 1]
                    args = capb__hcei.value.args
                    if (isinstance(ozd__nqy, ir.Assign) and ozd__nqy.target
                        .name == kqp__sco and isinstance(ozd__nqy.value, ir
                        .Expr) and ozd__nqy.value.op == 'getattr' and 
                        ozd__nqy.value.value.name in lit_old_idx):
                        wxc__ein = ozd__nqy.value.value.name
                        duu__japwr = ozd__nqy.value.attr
                        if duu__japwr == '__setitem__':
                            cut__pnjy = False
                            map_updates[wxc__ein].append(args)
                            new_body[-1] = None
                        elif duu__japwr == 'update' and args[0
                            ].name in lit_old_idx:
                            cut__pnjy = False
                            map_updates[wxc__ein].extend(map_updates[args[0
                                ].name])
                            new_body[-1] = None
                        if not cut__pnjy:
                            lit_new_idx[wxc__ein] = vnno__lrfmv
                            func_ir._definitions[ozd__nqy.target.name].remove(
                                ozd__nqy.value)
            if not (isinstance(capb__hcei, ir.Assign) and isinstance(
                capb__hcei.value, ir.Expr) and capb__hcei.value.op ==
                'getattr' and capb__hcei.value.value.name in lit_old_idx and
                capb__hcei.value.attr in ('__setitem__', 'update')):
                for yeety__ymms in capb__hcei.list_vars():
                    if (yeety__ymms.name in lit_old_idx and yeety__ymms.
                        name != tlzs__nzh):
                        _insert_build_map(func_ir, yeety__ymms.name,
                            gljyq__yjbrk.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if cut__pnjy:
                new_body.append(capb__hcei)
            else:
                func_ir._definitions[capb__hcei.target.name].remove(capb__hcei
                    .value)
                xfujo__qfkew = True
                new_body.append(None)
        tkcnr__mhoce = list(lit_old_idx.keys())
        for vmw__zsw in tkcnr__mhoce:
            _insert_build_map(func_ir, vmw__zsw, gljyq__yjbrk.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if xfujo__qfkew:
            gljyq__yjbrk.body = [rcasb__jmvy for rcasb__jmvy in new_body if
                rcasb__jmvy is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    hhipu__ysdg = lit_old_idx[name]
    zcdt__unlf = lit_new_idx[name]
    gbj__jobno = map_updates[name]
    new_body[zcdt__unlf] = _build_new_build_map(func_ir, name, old_body,
        hhipu__ysdg, gbj__jobno)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    bjpv__aurf = old_body[old_lineno]
    dmi__ytu = bjpv__aurf.target
    qtxrz__rufk = bjpv__aurf.value
    fhhr__ldnh = []
    mah__zpanq = []
    for tlo__aiza in new_items:
        fgfzo__vzwyu, rxek__hbx = tlo__aiza
        nazak__vcl = guard(get_definition, func_ir, fgfzo__vzwyu)
        if isinstance(nazak__vcl, (ir.Const, ir.Global, ir.FreeVar)):
            fhhr__ldnh.append(nazak__vcl.value)
        anov__wiczc = guard(get_definition, func_ir, rxek__hbx)
        if isinstance(anov__wiczc, (ir.Const, ir.Global, ir.FreeVar)):
            mah__zpanq.append(anov__wiczc.value)
        else:
            mah__zpanq.append(numba.core.interpreter._UNKNOWN_VALUE(
                rxek__hbx.name))
    gvw__zgl = {}
    if len(fhhr__ldnh) == len(new_items):
        binaw__qimx = {rcasb__jmvy: npf__wrbu for rcasb__jmvy, npf__wrbu in
            zip(fhhr__ldnh, mah__zpanq)}
        for vnno__lrfmv, fgfzo__vzwyu in enumerate(fhhr__ldnh):
            gvw__zgl[fgfzo__vzwyu] = vnno__lrfmv
    else:
        binaw__qimx = None
    zfqk__tmsn = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=binaw__qimx, value_indexes=gvw__zgl, loc=qtxrz__rufk.loc)
    func_ir._definitions[name].append(zfqk__tmsn)
    return ir.Assign(zfqk__tmsn, ir.Var(dmi__ytu.scope, name, dmi__ytu.loc),
        zfqk__tmsn.loc)
