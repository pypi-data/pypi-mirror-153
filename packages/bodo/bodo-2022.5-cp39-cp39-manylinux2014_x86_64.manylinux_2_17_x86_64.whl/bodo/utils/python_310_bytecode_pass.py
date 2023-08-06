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
    izi__zzda = keyword_expr.items.copy()
    mowam__hcgig = keyword_expr.value_indexes
    for iae__dvo, opshq__nzaqt in mowam__hcgig.items():
        izi__zzda[opshq__nzaqt] = iae__dvo, izi__zzda[opshq__nzaqt][1]
    new_body[buildmap_idx] = None
    return izi__zzda


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    gbx__qdpj = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    izi__zzda = []
    xdp__otx = buildmap_idx + 1
    while xdp__otx <= search_end:
        nrl__lwjqs = body[xdp__otx]
        if not (isinstance(nrl__lwjqs, ir.Assign) and isinstance(nrl__lwjqs
            .value, ir.Const)):
            raise UnsupportedError(gbx__qdpj)
        vji__wqh = nrl__lwjqs.target.name
        juz__abch = nrl__lwjqs.value.value
        xdp__otx += 1
        vpw__wiy = True
        while xdp__otx <= search_end and vpw__wiy:
            dqfdq__hlag = body[xdp__otx]
            if (isinstance(dqfdq__hlag, ir.Assign) and isinstance(
                dqfdq__hlag.value, ir.Expr) and dqfdq__hlag.value.op ==
                'getattr' and dqfdq__hlag.value.value.name == buildmap_name and
                dqfdq__hlag.value.attr == '__setitem__'):
                vpw__wiy = False
            else:
                xdp__otx += 1
        if vpw__wiy or xdp__otx == search_end:
            raise UnsupportedError(gbx__qdpj)
        zqrt__vgit = body[xdp__otx + 1]
        if not (isinstance(zqrt__vgit, ir.Assign) and isinstance(zqrt__vgit
            .value, ir.Expr) and zqrt__vgit.value.op == 'call' and 
            zqrt__vgit.value.func.name == dqfdq__hlag.target.name and len(
            zqrt__vgit.value.args) == 2 and zqrt__vgit.value.args[0].name ==
            vji__wqh):
            raise UnsupportedError(gbx__qdpj)
        lwqu__hhf = zqrt__vgit.value.args[1]
        izi__zzda.append((juz__abch, lwqu__hhf))
        new_body[xdp__otx] = None
        new_body[xdp__otx + 1] = None
        xdp__otx += 2
    return izi__zzda


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    gbx__qdpj = 'CALL_FUNCTION_EX with **kwargs not supported'
    xdp__otx = 0
    tvdv__fjpbz = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        gzhao__ojw = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        gzhao__ojw = vararg_stmt.target.name
    dba__rzxi = True
    while search_end >= xdp__otx and dba__rzxi:
        oyl__flrz = body[search_end]
        if (isinstance(oyl__flrz, ir.Assign) and oyl__flrz.target.name ==
            gzhao__ojw and isinstance(oyl__flrz.value, ir.Expr) and 
            oyl__flrz.value.op == 'build_tuple' and not oyl__flrz.value.items):
            dba__rzxi = False
            new_body[search_end] = None
        else:
            if search_end == xdp__otx or not (isinstance(oyl__flrz, ir.
                Assign) and oyl__flrz.target.name == gzhao__ojw and
                isinstance(oyl__flrz.value, ir.Expr) and oyl__flrz.value.op ==
                'binop' and oyl__flrz.value.fn == operator.add):
                raise UnsupportedError(gbx__qdpj)
            fjp__lwtk = oyl__flrz.value.lhs.name
            sxao__ynm = oyl__flrz.value.rhs.name
            neyu__mkdd = body[search_end - 1]
            if not (isinstance(neyu__mkdd, ir.Assign) and isinstance(
                neyu__mkdd.value, ir.Expr) and neyu__mkdd.value.op ==
                'build_tuple' and len(neyu__mkdd.value.items) == 1):
                raise UnsupportedError(gbx__qdpj)
            if neyu__mkdd.target.name == fjp__lwtk:
                gzhao__ojw = sxao__ynm
            elif neyu__mkdd.target.name == sxao__ynm:
                gzhao__ojw = fjp__lwtk
            else:
                raise UnsupportedError(gbx__qdpj)
            tvdv__fjpbz.append(neyu__mkdd.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            vwy__qrvk = True
            while search_end >= xdp__otx and vwy__qrvk:
                xjvxt__hkbe = body[search_end]
                if isinstance(xjvxt__hkbe, ir.Assign
                    ) and xjvxt__hkbe.target.name == gzhao__ojw:
                    vwy__qrvk = False
                else:
                    search_end -= 1
    if dba__rzxi:
        raise UnsupportedError(gbx__qdpj)
    return tvdv__fjpbz[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    gbx__qdpj = 'CALL_FUNCTION_EX with **kwargs not supported'
    for tnurf__lhfa in func_ir.blocks.values():
        stznu__agdck = False
        new_body = []
        for rch__mkxij, lzr__ezmw in enumerate(tnurf__lhfa.body):
            if (isinstance(lzr__ezmw, ir.Assign) and isinstance(lzr__ezmw.
                value, ir.Expr) and lzr__ezmw.value.op == 'call' and 
                lzr__ezmw.value.varkwarg is not None):
                stznu__agdck = True
                xsil__usr = lzr__ezmw.value
                args = xsil__usr.args
                izi__zzda = xsil__usr.kws
                lwzzp__frv = xsil__usr.vararg
                dedn__gbi = xsil__usr.varkwarg
                zyjnv__qqfw = rch__mkxij - 1
                zhh__serrz = zyjnv__qqfw
                zcgt__mdwhg = None
                eeqg__qnin = True
                while zhh__serrz >= 0 and eeqg__qnin:
                    zcgt__mdwhg = tnurf__lhfa.body[zhh__serrz]
                    if isinstance(zcgt__mdwhg, ir.Assign
                        ) and zcgt__mdwhg.target.name == dedn__gbi.name:
                        eeqg__qnin = False
                    else:
                        zhh__serrz -= 1
                if izi__zzda or eeqg__qnin or not (isinstance(zcgt__mdwhg.
                    value, ir.Expr) and zcgt__mdwhg.value.op == 'build_map'):
                    raise UnsupportedError(gbx__qdpj)
                if zcgt__mdwhg.value.items:
                    izi__zzda = _call_function_ex_replace_kws_small(zcgt__mdwhg
                        .value, new_body, zhh__serrz)
                else:
                    izi__zzda = _call_function_ex_replace_kws_large(tnurf__lhfa
                        .body, dedn__gbi.name, zhh__serrz, rch__mkxij - 1,
                        new_body)
                zyjnv__qqfw = zhh__serrz
                if lwzzp__frv is not None:
                    if args:
                        raise UnsupportedError(gbx__qdpj)
                    zxe__ygr = zyjnv__qqfw
                    mnbiy__imyil = None
                    eeqg__qnin = True
                    while zxe__ygr >= 0 and eeqg__qnin:
                        mnbiy__imyil = tnurf__lhfa.body[zxe__ygr]
                        if isinstance(mnbiy__imyil, ir.Assign
                            ) and mnbiy__imyil.target.name == lwzzp__frv.name:
                            eeqg__qnin = False
                        else:
                            zxe__ygr -= 1
                    if eeqg__qnin:
                        raise UnsupportedError(gbx__qdpj)
                    if isinstance(mnbiy__imyil.value, ir.Expr
                        ) and mnbiy__imyil.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(
                            mnbiy__imyil.value, new_body, zxe__ygr)
                    else:
                        args = _call_function_ex_replace_args_large(
                            mnbiy__imyil, tnurf__lhfa.body, new_body, zxe__ygr)
                idj__wnncs = ir.Expr.call(xsil__usr.func, args, izi__zzda,
                    xsil__usr.loc, target=xsil__usr.target)
                if lzr__ezmw.target.name in func_ir._definitions and len(
                    func_ir._definitions[lzr__ezmw.target.name]) == 1:
                    func_ir._definitions[lzr__ezmw.target.name].clear()
                func_ir._definitions[lzr__ezmw.target.name].append(idj__wnncs)
                lzr__ezmw = ir.Assign(idj__wnncs, lzr__ezmw.target,
                    lzr__ezmw.loc)
            new_body.append(lzr__ezmw)
        if stznu__agdck:
            tnurf__lhfa.body = [cqujf__uuoyt for cqujf__uuoyt in new_body if
                cqujf__uuoyt is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for tnurf__lhfa in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        stznu__agdck = False
        for rch__mkxij, lzr__ezmw in enumerate(tnurf__lhfa.body):
            nqlvg__chzr = True
            ong__kcby = None
            if isinstance(lzr__ezmw, ir.Assign) and isinstance(lzr__ezmw.
                value, ir.Expr):
                if lzr__ezmw.value.op == 'build_map':
                    ong__kcby = lzr__ezmw.target.name
                    lit_old_idx[lzr__ezmw.target.name] = rch__mkxij
                    lit_new_idx[lzr__ezmw.target.name] = rch__mkxij
                    map_updates[lzr__ezmw.target.name
                        ] = lzr__ezmw.value.items.copy()
                    nqlvg__chzr = False
                elif lzr__ezmw.value.op == 'call' and rch__mkxij > 0:
                    ogw__qlv = lzr__ezmw.value.func.name
                    dqfdq__hlag = tnurf__lhfa.body[rch__mkxij - 1]
                    args = lzr__ezmw.value.args
                    if (isinstance(dqfdq__hlag, ir.Assign) and dqfdq__hlag.
                        target.name == ogw__qlv and isinstance(dqfdq__hlag.
                        value, ir.Expr) and dqfdq__hlag.value.op ==
                        'getattr' and dqfdq__hlag.value.value.name in
                        lit_old_idx):
                        mrzm__wyym = dqfdq__hlag.value.value.name
                        nnctl__brsso = dqfdq__hlag.value.attr
                        if nnctl__brsso == '__setitem__':
                            nqlvg__chzr = False
                            map_updates[mrzm__wyym].append(args)
                            new_body[-1] = None
                        elif nnctl__brsso == 'update' and args[0
                            ].name in lit_old_idx:
                            nqlvg__chzr = False
                            map_updates[mrzm__wyym].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not nqlvg__chzr:
                            lit_new_idx[mrzm__wyym] = rch__mkxij
                            func_ir._definitions[dqfdq__hlag.target.name
                                ].remove(dqfdq__hlag.value)
            if not (isinstance(lzr__ezmw, ir.Assign) and isinstance(
                lzr__ezmw.value, ir.Expr) and lzr__ezmw.value.op ==
                'getattr' and lzr__ezmw.value.value.name in lit_old_idx and
                lzr__ezmw.value.attr in ('__setitem__', 'update')):
                for lqny__lrn in lzr__ezmw.list_vars():
                    if (lqny__lrn.name in lit_old_idx and lqny__lrn.name !=
                        ong__kcby):
                        _insert_build_map(func_ir, lqny__lrn.name,
                            tnurf__lhfa.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if nqlvg__chzr:
                new_body.append(lzr__ezmw)
            else:
                func_ir._definitions[lzr__ezmw.target.name].remove(lzr__ezmw
                    .value)
                stznu__agdck = True
                new_body.append(None)
        yyja__invgd = list(lit_old_idx.keys())
        for hdgg__kvqoa in yyja__invgd:
            _insert_build_map(func_ir, hdgg__kvqoa, tnurf__lhfa.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if stznu__agdck:
            tnurf__lhfa.body = [cqujf__uuoyt for cqujf__uuoyt in new_body if
                cqujf__uuoyt is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    nkhe__evt = lit_old_idx[name]
    wucbh__hsrpe = lit_new_idx[name]
    eurvp__cty = map_updates[name]
    new_body[wucbh__hsrpe] = _build_new_build_map(func_ir, name, old_body,
        nkhe__evt, eurvp__cty)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    gajkq__uxx = old_body[old_lineno]
    gxj__ccuje = gajkq__uxx.target
    qqhed__iiqkd = gajkq__uxx.value
    xmtiz__cad = []
    pzih__dcllx = []
    for vvvhi__vhun in new_items:
        ljg__ahdbt, chfl__jgw = vvvhi__vhun
        nyzvz__khdxm = guard(get_definition, func_ir, ljg__ahdbt)
        if isinstance(nyzvz__khdxm, (ir.Const, ir.Global, ir.FreeVar)):
            xmtiz__cad.append(nyzvz__khdxm.value)
        euy__wvxcc = guard(get_definition, func_ir, chfl__jgw)
        if isinstance(euy__wvxcc, (ir.Const, ir.Global, ir.FreeVar)):
            pzih__dcllx.append(euy__wvxcc.value)
        else:
            pzih__dcllx.append(numba.core.interpreter._UNKNOWN_VALUE(
                chfl__jgw.name))
    mowam__hcgig = {}
    if len(xmtiz__cad) == len(new_items):
        wtukg__vfqoo = {cqujf__uuoyt: rkxmd__zafn for cqujf__uuoyt,
            rkxmd__zafn in zip(xmtiz__cad, pzih__dcllx)}
        for rch__mkxij, ljg__ahdbt in enumerate(xmtiz__cad):
            mowam__hcgig[ljg__ahdbt] = rch__mkxij
    else:
        wtukg__vfqoo = None
    tutd__rdwas = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=wtukg__vfqoo, value_indexes=mowam__hcgig, loc=
        qqhed__iiqkd.loc)
    func_ir._definitions[name].append(tutd__rdwas)
    return ir.Assign(tutd__rdwas, ir.Var(gxj__ccuje.scope, name, gxj__ccuje
        .loc), tutd__rdwas.loc)
