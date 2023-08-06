"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    qwef__jelsl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    eyl__nofck = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    qfm__ukelj = builder.gep(null_bitmap_ptr, [qwef__jelsl], inbounds=True)
    bujj__ysw = builder.load(qfm__ukelj)
    jkcm__vub = lir.ArrayType(lir.IntType(8), 8)
    vyf__gri = cgutils.alloca_once_value(builder, lir.Constant(jkcm__vub, (
        1, 2, 4, 8, 16, 32, 64, 128)))
    qxs__ftbn = builder.load(builder.gep(vyf__gri, [lir.Constant(lir.
        IntType(64), 0), eyl__nofck], inbounds=True))
    if val:
        builder.store(builder.or_(bujj__ysw, qxs__ftbn), qfm__ukelj)
    else:
        qxs__ftbn = builder.xor(qxs__ftbn, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(bujj__ysw, qxs__ftbn), qfm__ukelj)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    qwef__jelsl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    eyl__nofck = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    bujj__ysw = builder.load(builder.gep(null_bitmap_ptr, [qwef__jelsl],
        inbounds=True))
    jkcm__vub = lir.ArrayType(lir.IntType(8), 8)
    vyf__gri = cgutils.alloca_once_value(builder, lir.Constant(jkcm__vub, (
        1, 2, 4, 8, 16, 32, 64, 128)))
    qxs__ftbn = builder.load(builder.gep(vyf__gri, [lir.Constant(lir.
        IntType(64), 0), eyl__nofck], inbounds=True))
    return builder.and_(bujj__ysw, qxs__ftbn)


def pyarray_check(builder, context, obj):
    imx__hysdc = context.get_argument_type(types.pyobject)
    lmk__zohgq = lir.FunctionType(lir.IntType(32), [imx__hysdc])
    kmy__rlwkw = cgutils.get_or_insert_function(builder.module, lmk__zohgq,
        name='is_np_array')
    return builder.call(kmy__rlwkw, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    imx__hysdc = context.get_argument_type(types.pyobject)
    dlroh__gdmwo = context.get_value_type(types.intp)
    inhqi__hnmd = lir.FunctionType(lir.IntType(8).as_pointer(), [imx__hysdc,
        dlroh__gdmwo])
    rpz__nsppi = cgutils.get_or_insert_function(builder.module, inhqi__hnmd,
        name='array_getptr1')
    gxw__bbud = lir.FunctionType(imx__hysdc, [imx__hysdc, lir.IntType(8).
        as_pointer()])
    naxch__azpaf = cgutils.get_or_insert_function(builder.module, gxw__bbud,
        name='array_getitem')
    stvn__nxgoi = builder.call(rpz__nsppi, [arr_obj, ind])
    return builder.call(naxch__azpaf, [arr_obj, stvn__nxgoi])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    imx__hysdc = context.get_argument_type(types.pyobject)
    dlroh__gdmwo = context.get_value_type(types.intp)
    inhqi__hnmd = lir.FunctionType(lir.IntType(8).as_pointer(), [imx__hysdc,
        dlroh__gdmwo])
    rpz__nsppi = cgutils.get_or_insert_function(builder.module, inhqi__hnmd,
        name='array_getptr1')
    ejfe__rojty = lir.FunctionType(lir.VoidType(), [imx__hysdc, lir.IntType
        (8).as_pointer(), imx__hysdc])
    byfjo__rcy = cgutils.get_or_insert_function(builder.module, ejfe__rojty,
        name='array_setitem')
    stvn__nxgoi = builder.call(rpz__nsppi, [arr_obj, ind])
    builder.call(byfjo__rcy, [arr_obj, stvn__nxgoi, val_obj])


def seq_getitem(builder, context, obj, ind):
    imx__hysdc = context.get_argument_type(types.pyobject)
    dlroh__gdmwo = context.get_value_type(types.intp)
    kbgew__otuu = lir.FunctionType(imx__hysdc, [imx__hysdc, dlroh__gdmwo])
    hfboy__coh = cgutils.get_or_insert_function(builder.module, kbgew__otuu,
        name='seq_getitem')
    return builder.call(hfboy__coh, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    imx__hysdc = context.get_argument_type(types.pyobject)
    nkfts__fqd = lir.FunctionType(lir.IntType(32), [imx__hysdc, imx__hysdc])
    ryhht__hllj = cgutils.get_or_insert_function(builder.module, nkfts__fqd,
        name='is_na_value')
    return builder.call(ryhht__hllj, [val, C_NA])


def list_check(builder, context, obj):
    imx__hysdc = context.get_argument_type(types.pyobject)
    heg__iwgy = context.get_value_type(types.int32)
    gxu__chrie = lir.FunctionType(heg__iwgy, [imx__hysdc])
    xns__dzva = cgutils.get_or_insert_function(builder.module, gxu__chrie,
        name='list_check')
    return builder.call(xns__dzva, [obj])


def dict_keys(builder, context, obj):
    imx__hysdc = context.get_argument_type(types.pyobject)
    gxu__chrie = lir.FunctionType(imx__hysdc, [imx__hysdc])
    xns__dzva = cgutils.get_or_insert_function(builder.module, gxu__chrie,
        name='dict_keys')
    return builder.call(xns__dzva, [obj])


def dict_values(builder, context, obj):
    imx__hysdc = context.get_argument_type(types.pyobject)
    gxu__chrie = lir.FunctionType(imx__hysdc, [imx__hysdc])
    xns__dzva = cgutils.get_or_insert_function(builder.module, gxu__chrie,
        name='dict_values')
    return builder.call(xns__dzva, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    imx__hysdc = context.get_argument_type(types.pyobject)
    gxu__chrie = lir.FunctionType(lir.VoidType(), [imx__hysdc, imx__hysdc])
    xns__dzva = cgutils.get_or_insert_function(builder.module, gxu__chrie,
        name='dict_merge_from_seq2')
    builder.call(xns__dzva, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    gyt__txxsj = cgutils.alloca_once_value(builder, val)
    pedcb__hnmou = list_check(builder, context, val)
    flkbc__ofn = builder.icmp_unsigned('!=', pedcb__hnmou, lir.Constant(
        pedcb__hnmou.type, 0))
    with builder.if_then(flkbc__ofn):
        krvg__fupsa = context.insert_const_string(builder.module, 'numpy')
        bbz__qsgll = c.pyapi.import_module_noblock(krvg__fupsa)
        ejimd__wvfad = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            ejimd__wvfad = str(typ.dtype)
        xme__zikqp = c.pyapi.object_getattr_string(bbz__qsgll, ejimd__wvfad)
        ykk__svu = builder.load(gyt__txxsj)
        vtmjj__wfchz = c.pyapi.call_method(bbz__qsgll, 'asarray', (ykk__svu,
            xme__zikqp))
        builder.store(vtmjj__wfchz, gyt__txxsj)
        c.pyapi.decref(bbz__qsgll)
        c.pyapi.decref(xme__zikqp)
    val = builder.load(gyt__txxsj)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        qvz__lqzew = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        kfij__krjkl, ombva__iwlj = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [qvz__lqzew])
        context.nrt.decref(builder, typ, qvz__lqzew)
        return cgutils.pack_array(builder, [ombva__iwlj])
    if isinstance(typ, (StructType, types.BaseTuple)):
        krvg__fupsa = context.insert_const_string(builder.module, 'pandas')
        gzcac__funsg = c.pyapi.import_module_noblock(krvg__fupsa)
        C_NA = c.pyapi.object_getattr_string(gzcac__funsg, 'NA')
        pryk__ajohr = bodo.utils.transform.get_type_alloc_counts(typ)
        rcvl__lnf = context.make_tuple(builder, types.Tuple(pryk__ajohr * [
            types.int64]), pryk__ajohr * [context.get_constant(types.int64, 0)]
            )
        iir__mxdz = cgutils.alloca_once_value(builder, rcvl__lnf)
        ijykj__tpbmv = 0
        xdsmc__faat = typ.data if isinstance(typ, StructType) else typ.types
        for qidy__pjj, t in enumerate(xdsmc__faat):
            wnpf__vuve = bodo.utils.transform.get_type_alloc_counts(t)
            if wnpf__vuve == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    qidy__pjj])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, qidy__pjj)
            jxe__gtd = is_na_value(builder, context, val_obj, C_NA)
            rtj__argm = builder.icmp_unsigned('!=', jxe__gtd, lir.Constant(
                jxe__gtd.type, 1))
            with builder.if_then(rtj__argm):
                rcvl__lnf = builder.load(iir__mxdz)
                jfxi__rob = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for qidy__pjj in range(wnpf__vuve):
                    oslyh__rabl = builder.extract_value(rcvl__lnf, 
                        ijykj__tpbmv + qidy__pjj)
                    wlst__eheq = builder.extract_value(jfxi__rob, qidy__pjj)
                    rcvl__lnf = builder.insert_value(rcvl__lnf, builder.add
                        (oslyh__rabl, wlst__eheq), ijykj__tpbmv + qidy__pjj)
                builder.store(rcvl__lnf, iir__mxdz)
            ijykj__tpbmv += wnpf__vuve
        c.pyapi.decref(gzcac__funsg)
        c.pyapi.decref(C_NA)
        return builder.load(iir__mxdz)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    krvg__fupsa = context.insert_const_string(builder.module, 'pandas')
    gzcac__funsg = c.pyapi.import_module_noblock(krvg__fupsa)
    C_NA = c.pyapi.object_getattr_string(gzcac__funsg, 'NA')
    pryk__ajohr = bodo.utils.transform.get_type_alloc_counts(typ)
    rcvl__lnf = context.make_tuple(builder, types.Tuple(pryk__ajohr * [
        types.int64]), [n] + (pryk__ajohr - 1) * [context.get_constant(
        types.int64, 0)])
    iir__mxdz = cgutils.alloca_once_value(builder, rcvl__lnf)
    with cgutils.for_range(builder, n) as eohp__yvt:
        ptn__jqn = eohp__yvt.index
        jrlrn__dwavk = seq_getitem(builder, context, arr_obj, ptn__jqn)
        jxe__gtd = is_na_value(builder, context, jrlrn__dwavk, C_NA)
        rtj__argm = builder.icmp_unsigned('!=', jxe__gtd, lir.Constant(
            jxe__gtd.type, 1))
        with builder.if_then(rtj__argm):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                rcvl__lnf = builder.load(iir__mxdz)
                jfxi__rob = get_array_elem_counts(c, builder, context,
                    jrlrn__dwavk, typ.dtype)
                for qidy__pjj in range(pryk__ajohr - 1):
                    oslyh__rabl = builder.extract_value(rcvl__lnf, 
                        qidy__pjj + 1)
                    wlst__eheq = builder.extract_value(jfxi__rob, qidy__pjj)
                    rcvl__lnf = builder.insert_value(rcvl__lnf, builder.add
                        (oslyh__rabl, wlst__eheq), qidy__pjj + 1)
                builder.store(rcvl__lnf, iir__mxdz)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                ijykj__tpbmv = 1
                for qidy__pjj, t in enumerate(typ.data):
                    wnpf__vuve = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if wnpf__vuve == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(jrlrn__dwavk, qidy__pjj
                            )
                    else:
                        val_obj = c.pyapi.dict_getitem_string(jrlrn__dwavk,
                            typ.names[qidy__pjj])
                    jxe__gtd = is_na_value(builder, context, val_obj, C_NA)
                    rtj__argm = builder.icmp_unsigned('!=', jxe__gtd, lir.
                        Constant(jxe__gtd.type, 1))
                    with builder.if_then(rtj__argm):
                        rcvl__lnf = builder.load(iir__mxdz)
                        jfxi__rob = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for qidy__pjj in range(wnpf__vuve):
                            oslyh__rabl = builder.extract_value(rcvl__lnf, 
                                ijykj__tpbmv + qidy__pjj)
                            wlst__eheq = builder.extract_value(jfxi__rob,
                                qidy__pjj)
                            rcvl__lnf = builder.insert_value(rcvl__lnf,
                                builder.add(oslyh__rabl, wlst__eheq), 
                                ijykj__tpbmv + qidy__pjj)
                        builder.store(rcvl__lnf, iir__mxdz)
                    ijykj__tpbmv += wnpf__vuve
            else:
                assert isinstance(typ, MapArrayType), typ
                rcvl__lnf = builder.load(iir__mxdz)
                tkkgt__gtyqv = dict_keys(builder, context, jrlrn__dwavk)
                veaw__mel = dict_values(builder, context, jrlrn__dwavk)
                sriqy__rqn = get_array_elem_counts(c, builder, context,
                    tkkgt__gtyqv, typ.key_arr_type)
                epjnl__rfm = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for qidy__pjj in range(1, epjnl__rfm + 1):
                    oslyh__rabl = builder.extract_value(rcvl__lnf, qidy__pjj)
                    wlst__eheq = builder.extract_value(sriqy__rqn, 
                        qidy__pjj - 1)
                    rcvl__lnf = builder.insert_value(rcvl__lnf, builder.add
                        (oslyh__rabl, wlst__eheq), qidy__pjj)
                pxqpj__ktqky = get_array_elem_counts(c, builder, context,
                    veaw__mel, typ.value_arr_type)
                for qidy__pjj in range(epjnl__rfm + 1, pryk__ajohr):
                    oslyh__rabl = builder.extract_value(rcvl__lnf, qidy__pjj)
                    wlst__eheq = builder.extract_value(pxqpj__ktqky, 
                        qidy__pjj - epjnl__rfm)
                    rcvl__lnf = builder.insert_value(rcvl__lnf, builder.add
                        (oslyh__rabl, wlst__eheq), qidy__pjj)
                builder.store(rcvl__lnf, iir__mxdz)
                c.pyapi.decref(tkkgt__gtyqv)
                c.pyapi.decref(veaw__mel)
        c.pyapi.decref(jrlrn__dwavk)
    c.pyapi.decref(gzcac__funsg)
    c.pyapi.decref(C_NA)
    return builder.load(iir__mxdz)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    hret__smt = n_elems.type.count
    assert hret__smt >= 1
    topuc__tynxh = builder.extract_value(n_elems, 0)
    if hret__smt != 1:
        kbc__mvamx = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, qidy__pjj) for qidy__pjj in range(1, hret__smt)])
        wlg__kthvb = types.Tuple([types.int64] * (hret__smt - 1))
    else:
        kbc__mvamx = context.get_dummy_value()
        wlg__kthvb = types.none
    jcqj__xqng = types.TypeRef(arr_type)
    qzub__wqtvh = arr_type(types.int64, jcqj__xqng, wlg__kthvb)
    args = [topuc__tynxh, context.get_dummy_value(), kbc__mvamx]
    pdh__uompa = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        kfij__krjkl, wneuk__fxn = c.pyapi.call_jit_code(pdh__uompa,
            qzub__wqtvh, args)
    else:
        wneuk__fxn = context.compile_internal(builder, pdh__uompa,
            qzub__wqtvh, args)
    return wneuk__fxn


def is_ll_eq(builder, val1, val2):
    ukwd__mrmvc = val1.type.pointee
    flqvd__iuz = val2.type.pointee
    assert ukwd__mrmvc == flqvd__iuz, 'invalid llvm value comparison'
    if isinstance(ukwd__mrmvc, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(ukwd__mrmvc.elements) if isinstance(ukwd__mrmvc, lir.
            BaseStructType) else ukwd__mrmvc.count
        bhks__pbwqm = lir.Constant(lir.IntType(1), 1)
        for qidy__pjj in range(n_elems):
            rcfa__hdd = lir.IntType(32)(0)
            hwi__tvcx = lir.IntType(32)(qidy__pjj)
            pul__tch = builder.gep(val1, [rcfa__hdd, hwi__tvcx], inbounds=True)
            czbn__zrur = builder.gep(val2, [rcfa__hdd, hwi__tvcx], inbounds
                =True)
            bhks__pbwqm = builder.and_(bhks__pbwqm, is_ll_eq(builder,
                pul__tch, czbn__zrur))
        return bhks__pbwqm
    iedu__hvzok = builder.load(val1)
    kmi__lis = builder.load(val2)
    if iedu__hvzok.type in (lir.FloatType(), lir.DoubleType()):
        mqdn__bkhcb = 32 if iedu__hvzok.type == lir.FloatType() else 64
        iedu__hvzok = builder.bitcast(iedu__hvzok, lir.IntType(mqdn__bkhcb))
        kmi__lis = builder.bitcast(kmi__lis, lir.IntType(mqdn__bkhcb))
    return builder.icmp_unsigned('==', iedu__hvzok, kmi__lis)
