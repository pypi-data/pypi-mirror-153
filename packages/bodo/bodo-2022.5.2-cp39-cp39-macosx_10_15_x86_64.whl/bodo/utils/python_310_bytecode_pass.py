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
    edu__xstng = keyword_expr.items.copy()
    fty__azei = keyword_expr.value_indexes
    for simgl__mcgyw, qbeh__jgwrw in fty__azei.items():
        edu__xstng[qbeh__jgwrw] = simgl__mcgyw, edu__xstng[qbeh__jgwrw][1]
    new_body[buildmap_idx] = None
    return edu__xstng


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    pya__xox = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    edu__xstng = []
    jstec__dsbpi = buildmap_idx + 1
    while jstec__dsbpi <= search_end:
        aujmm__zof = body[jstec__dsbpi]
        if not (isinstance(aujmm__zof, ir.Assign) and isinstance(aujmm__zof
            .value, ir.Const)):
            raise UnsupportedError(pya__xox)
        uxs__uln = aujmm__zof.target.name
        edw__pujss = aujmm__zof.value.value
        jstec__dsbpi += 1
        lgv__irhlb = True
        while jstec__dsbpi <= search_end and lgv__irhlb:
            tnzll__lkl = body[jstec__dsbpi]
            if (isinstance(tnzll__lkl, ir.Assign) and isinstance(tnzll__lkl
                .value, ir.Expr) and tnzll__lkl.value.op == 'getattr' and 
                tnzll__lkl.value.value.name == buildmap_name and tnzll__lkl
                .value.attr == '__setitem__'):
                lgv__irhlb = False
            else:
                jstec__dsbpi += 1
        if lgv__irhlb or jstec__dsbpi == search_end:
            raise UnsupportedError(pya__xox)
        lcd__pfv = body[jstec__dsbpi + 1]
        if not (isinstance(lcd__pfv, ir.Assign) and isinstance(lcd__pfv.
            value, ir.Expr) and lcd__pfv.value.op == 'call' and lcd__pfv.
            value.func.name == tnzll__lkl.target.name and len(lcd__pfv.
            value.args) == 2 and lcd__pfv.value.args[0].name == uxs__uln):
            raise UnsupportedError(pya__xox)
        wakt__nbz = lcd__pfv.value.args[1]
        edu__xstng.append((edw__pujss, wakt__nbz))
        new_body[jstec__dsbpi] = None
        new_body[jstec__dsbpi + 1] = None
        jstec__dsbpi += 2
    return edu__xstng


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    pya__xox = 'CALL_FUNCTION_EX with **kwargs not supported'
    jstec__dsbpi = 0
    wyxdl__btu = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        wpu__rbkr = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        wpu__rbkr = vararg_stmt.target.name
    gxrex__ibi = True
    while search_end >= jstec__dsbpi and gxrex__ibi:
        cbau__sbjt = body[search_end]
        if (isinstance(cbau__sbjt, ir.Assign) and cbau__sbjt.target.name ==
            wpu__rbkr and isinstance(cbau__sbjt.value, ir.Expr) and 
            cbau__sbjt.value.op == 'build_tuple' and not cbau__sbjt.value.items
            ):
            gxrex__ibi = False
            new_body[search_end] = None
        else:
            if search_end == jstec__dsbpi or not (isinstance(cbau__sbjt, ir
                .Assign) and cbau__sbjt.target.name == wpu__rbkr and
                isinstance(cbau__sbjt.value, ir.Expr) and cbau__sbjt.value.
                op == 'binop' and cbau__sbjt.value.fn == operator.add):
                raise UnsupportedError(pya__xox)
            bkn__pgsds = cbau__sbjt.value.lhs.name
            wca__dwtr = cbau__sbjt.value.rhs.name
            nwec__poncq = body[search_end - 1]
            if not (isinstance(nwec__poncq, ir.Assign) and isinstance(
                nwec__poncq.value, ir.Expr) and nwec__poncq.value.op ==
                'build_tuple' and len(nwec__poncq.value.items) == 1):
                raise UnsupportedError(pya__xox)
            if nwec__poncq.target.name == bkn__pgsds:
                wpu__rbkr = wca__dwtr
            elif nwec__poncq.target.name == wca__dwtr:
                wpu__rbkr = bkn__pgsds
            else:
                raise UnsupportedError(pya__xox)
            wyxdl__btu.append(nwec__poncq.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            xrzjx__zgq = True
            while search_end >= jstec__dsbpi and xrzjx__zgq:
                jpt__izwc = body[search_end]
                if isinstance(jpt__izwc, ir.Assign
                    ) and jpt__izwc.target.name == wpu__rbkr:
                    xrzjx__zgq = False
                else:
                    search_end -= 1
    if gxrex__ibi:
        raise UnsupportedError(pya__xox)
    return wyxdl__btu[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    pya__xox = 'CALL_FUNCTION_EX with **kwargs not supported'
    for qjjqo__ghml in func_ir.blocks.values():
        dbkj__qsmfw = False
        new_body = []
        for thzj__dxkqi, ivll__puzma in enumerate(qjjqo__ghml.body):
            if (isinstance(ivll__puzma, ir.Assign) and isinstance(
                ivll__puzma.value, ir.Expr) and ivll__puzma.value.op ==
                'call' and ivll__puzma.value.varkwarg is not None):
                dbkj__qsmfw = True
                vgw__jxmsh = ivll__puzma.value
                args = vgw__jxmsh.args
                edu__xstng = vgw__jxmsh.kws
                rydmp__gxp = vgw__jxmsh.vararg
                clgc__zar = vgw__jxmsh.varkwarg
                baxp__bbl = thzj__dxkqi - 1
                dtm__tuwu = baxp__bbl
                akbpf__jfrrx = None
                byuja__qlua = True
                while dtm__tuwu >= 0 and byuja__qlua:
                    akbpf__jfrrx = qjjqo__ghml.body[dtm__tuwu]
                    if isinstance(akbpf__jfrrx, ir.Assign
                        ) and akbpf__jfrrx.target.name == clgc__zar.name:
                        byuja__qlua = False
                    else:
                        dtm__tuwu -= 1
                if edu__xstng or byuja__qlua or not (isinstance(
                    akbpf__jfrrx.value, ir.Expr) and akbpf__jfrrx.value.op ==
                    'build_map'):
                    raise UnsupportedError(pya__xox)
                if akbpf__jfrrx.value.items:
                    edu__xstng = _call_function_ex_replace_kws_small(
                        akbpf__jfrrx.value, new_body, dtm__tuwu)
                else:
                    edu__xstng = _call_function_ex_replace_kws_large(
                        qjjqo__ghml.body, clgc__zar.name, dtm__tuwu, 
                        thzj__dxkqi - 1, new_body)
                baxp__bbl = dtm__tuwu
                if rydmp__gxp is not None:
                    if args:
                        raise UnsupportedError(pya__xox)
                    efhld__igxvf = baxp__bbl
                    zipo__twp = None
                    byuja__qlua = True
                    while efhld__igxvf >= 0 and byuja__qlua:
                        zipo__twp = qjjqo__ghml.body[efhld__igxvf]
                        if isinstance(zipo__twp, ir.Assign
                            ) and zipo__twp.target.name == rydmp__gxp.name:
                            byuja__qlua = False
                        else:
                            efhld__igxvf -= 1
                    if byuja__qlua:
                        raise UnsupportedError(pya__xox)
                    if isinstance(zipo__twp.value, ir.Expr
                        ) and zipo__twp.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(zipo__twp
                            .value, new_body, efhld__igxvf)
                    else:
                        args = _call_function_ex_replace_args_large(zipo__twp,
                            qjjqo__ghml.body, new_body, efhld__igxvf)
                qqnua__zqhut = ir.Expr.call(vgw__jxmsh.func, args,
                    edu__xstng, vgw__jxmsh.loc, target=vgw__jxmsh.target)
                if ivll__puzma.target.name in func_ir._definitions and len(
                    func_ir._definitions[ivll__puzma.target.name]) == 1:
                    func_ir._definitions[ivll__puzma.target.name].clear()
                func_ir._definitions[ivll__puzma.target.name].append(
                    qqnua__zqhut)
                ivll__puzma = ir.Assign(qqnua__zqhut, ivll__puzma.target,
                    ivll__puzma.loc)
            new_body.append(ivll__puzma)
        if dbkj__qsmfw:
            qjjqo__ghml.body = [mihaa__euuwi for mihaa__euuwi in new_body if
                mihaa__euuwi is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for qjjqo__ghml in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        dbkj__qsmfw = False
        for thzj__dxkqi, ivll__puzma in enumerate(qjjqo__ghml.body):
            fgx__azy = True
            btfhd__zloj = None
            if isinstance(ivll__puzma, ir.Assign) and isinstance(ivll__puzma
                .value, ir.Expr):
                if ivll__puzma.value.op == 'build_map':
                    btfhd__zloj = ivll__puzma.target.name
                    lit_old_idx[ivll__puzma.target.name] = thzj__dxkqi
                    lit_new_idx[ivll__puzma.target.name] = thzj__dxkqi
                    map_updates[ivll__puzma.target.name
                        ] = ivll__puzma.value.items.copy()
                    fgx__azy = False
                elif ivll__puzma.value.op == 'call' and thzj__dxkqi > 0:
                    dfa__ssq = ivll__puzma.value.func.name
                    tnzll__lkl = qjjqo__ghml.body[thzj__dxkqi - 1]
                    args = ivll__puzma.value.args
                    if (isinstance(tnzll__lkl, ir.Assign) and tnzll__lkl.
                        target.name == dfa__ssq and isinstance(tnzll__lkl.
                        value, ir.Expr) and tnzll__lkl.value.op ==
                        'getattr' and tnzll__lkl.value.value.name in
                        lit_old_idx):
                        lwfom__itzri = tnzll__lkl.value.value.name
                        akfqo__ezc = tnzll__lkl.value.attr
                        if akfqo__ezc == '__setitem__':
                            fgx__azy = False
                            map_updates[lwfom__itzri].append(args)
                            new_body[-1] = None
                        elif akfqo__ezc == 'update' and args[0
                            ].name in lit_old_idx:
                            fgx__azy = False
                            map_updates[lwfom__itzri].extend(map_updates[
                                args[0].name])
                            new_body[-1] = None
                        if not fgx__azy:
                            lit_new_idx[lwfom__itzri] = thzj__dxkqi
                            func_ir._definitions[tnzll__lkl.target.name
                                ].remove(tnzll__lkl.value)
            if not (isinstance(ivll__puzma, ir.Assign) and isinstance(
                ivll__puzma.value, ir.Expr) and ivll__puzma.value.op ==
                'getattr' and ivll__puzma.value.value.name in lit_old_idx and
                ivll__puzma.value.attr in ('__setitem__', 'update')):
                for kfrkj__qhgx in ivll__puzma.list_vars():
                    if (kfrkj__qhgx.name in lit_old_idx and kfrkj__qhgx.
                        name != btfhd__zloj):
                        _insert_build_map(func_ir, kfrkj__qhgx.name,
                            qjjqo__ghml.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if fgx__azy:
                new_body.append(ivll__puzma)
            else:
                func_ir._definitions[ivll__puzma.target.name].remove(
                    ivll__puzma.value)
                dbkj__qsmfw = True
                new_body.append(None)
        nqcj__bzpj = list(lit_old_idx.keys())
        for popv__xrhyb in nqcj__bzpj:
            _insert_build_map(func_ir, popv__xrhyb, qjjqo__ghml.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if dbkj__qsmfw:
            qjjqo__ghml.body = [mihaa__euuwi for mihaa__euuwi in new_body if
                mihaa__euuwi is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    err__pxeqk = lit_old_idx[name]
    yxi__vqeri = lit_new_idx[name]
    pjdt__gigry = map_updates[name]
    new_body[yxi__vqeri] = _build_new_build_map(func_ir, name, old_body,
        err__pxeqk, pjdt__gigry)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    uvdg__vrb = old_body[old_lineno]
    kpjb__wviz = uvdg__vrb.target
    wlg__agcvh = uvdg__vrb.value
    sczk__gmu = []
    kbrvw__fds = []
    for pkfui__roo in new_items:
        cha__ggibl, ztqx__trb = pkfui__roo
        bpm__ielnq = guard(get_definition, func_ir, cha__ggibl)
        if isinstance(bpm__ielnq, (ir.Const, ir.Global, ir.FreeVar)):
            sczk__gmu.append(bpm__ielnq.value)
        yghb__vht = guard(get_definition, func_ir, ztqx__trb)
        if isinstance(yghb__vht, (ir.Const, ir.Global, ir.FreeVar)):
            kbrvw__fds.append(yghb__vht.value)
        else:
            kbrvw__fds.append(numba.core.interpreter._UNKNOWN_VALUE(
                ztqx__trb.name))
    fty__azei = {}
    if len(sczk__gmu) == len(new_items):
        rufiu__ezqwr = {mihaa__euuwi: wfbtp__wil for mihaa__euuwi,
            wfbtp__wil in zip(sczk__gmu, kbrvw__fds)}
        for thzj__dxkqi, cha__ggibl in enumerate(sczk__gmu):
            fty__azei[cha__ggibl] = thzj__dxkqi
    else:
        rufiu__ezqwr = None
    ocx__fqrt = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=rufiu__ezqwr, value_indexes=fty__azei, loc=wlg__agcvh.loc
        )
    func_ir._definitions[name].append(ocx__fqrt)
    return ir.Assign(ocx__fqrt, ir.Var(kpjb__wviz.scope, name, kpjb__wviz.
        loc), ocx__fqrt.loc)
