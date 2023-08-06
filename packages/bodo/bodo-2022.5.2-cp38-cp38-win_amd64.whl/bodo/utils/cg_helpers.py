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
    udqtw__ywx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    ykm__qrxth = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    hoc__lqy = builder.gep(null_bitmap_ptr, [udqtw__ywx], inbounds=True)
    gwje__yzs = builder.load(hoc__lqy)
    kufmq__glkve = lir.ArrayType(lir.IntType(8), 8)
    estu__ozdgw = cgutils.alloca_once_value(builder, lir.Constant(
        kufmq__glkve, (1, 2, 4, 8, 16, 32, 64, 128)))
    dllo__ziq = builder.load(builder.gep(estu__ozdgw, [lir.Constant(lir.
        IntType(64), 0), ykm__qrxth], inbounds=True))
    if val:
        builder.store(builder.or_(gwje__yzs, dllo__ziq), hoc__lqy)
    else:
        dllo__ziq = builder.xor(dllo__ziq, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(gwje__yzs, dllo__ziq), hoc__lqy)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    udqtw__ywx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    ykm__qrxth = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    gwje__yzs = builder.load(builder.gep(null_bitmap_ptr, [udqtw__ywx],
        inbounds=True))
    kufmq__glkve = lir.ArrayType(lir.IntType(8), 8)
    estu__ozdgw = cgutils.alloca_once_value(builder, lir.Constant(
        kufmq__glkve, (1, 2, 4, 8, 16, 32, 64, 128)))
    dllo__ziq = builder.load(builder.gep(estu__ozdgw, [lir.Constant(lir.
        IntType(64), 0), ykm__qrxth], inbounds=True))
    return builder.and_(gwje__yzs, dllo__ziq)


def pyarray_check(builder, context, obj):
    eieu__nvf = context.get_argument_type(types.pyobject)
    yrdu__iyce = lir.FunctionType(lir.IntType(32), [eieu__nvf])
    vodw__siqz = cgutils.get_or_insert_function(builder.module, yrdu__iyce,
        name='is_np_array')
    return builder.call(vodw__siqz, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    eieu__nvf = context.get_argument_type(types.pyobject)
    pmbpe__yvcln = context.get_value_type(types.intp)
    zumdl__huwy = lir.FunctionType(lir.IntType(8).as_pointer(), [eieu__nvf,
        pmbpe__yvcln])
    boro__gdxf = cgutils.get_or_insert_function(builder.module, zumdl__huwy,
        name='array_getptr1')
    omh__zdubc = lir.FunctionType(eieu__nvf, [eieu__nvf, lir.IntType(8).
        as_pointer()])
    gvcui__myjov = cgutils.get_or_insert_function(builder.module,
        omh__zdubc, name='array_getitem')
    gdlqd__yqne = builder.call(boro__gdxf, [arr_obj, ind])
    return builder.call(gvcui__myjov, [arr_obj, gdlqd__yqne])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    eieu__nvf = context.get_argument_type(types.pyobject)
    pmbpe__yvcln = context.get_value_type(types.intp)
    zumdl__huwy = lir.FunctionType(lir.IntType(8).as_pointer(), [eieu__nvf,
        pmbpe__yvcln])
    boro__gdxf = cgutils.get_or_insert_function(builder.module, zumdl__huwy,
        name='array_getptr1')
    qnrbm__sei = lir.FunctionType(lir.VoidType(), [eieu__nvf, lir.IntType(8
        ).as_pointer(), eieu__nvf])
    shd__ynvu = cgutils.get_or_insert_function(builder.module, qnrbm__sei,
        name='array_setitem')
    gdlqd__yqne = builder.call(boro__gdxf, [arr_obj, ind])
    builder.call(shd__ynvu, [arr_obj, gdlqd__yqne, val_obj])


def seq_getitem(builder, context, obj, ind):
    eieu__nvf = context.get_argument_type(types.pyobject)
    pmbpe__yvcln = context.get_value_type(types.intp)
    xkuv__dzo = lir.FunctionType(eieu__nvf, [eieu__nvf, pmbpe__yvcln])
    vybr__gcdnc = cgutils.get_or_insert_function(builder.module, xkuv__dzo,
        name='seq_getitem')
    return builder.call(vybr__gcdnc, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    eieu__nvf = context.get_argument_type(types.pyobject)
    fwcdi__bpwc = lir.FunctionType(lir.IntType(32), [eieu__nvf, eieu__nvf])
    wda__mjx = cgutils.get_or_insert_function(builder.module, fwcdi__bpwc,
        name='is_na_value')
    return builder.call(wda__mjx, [val, C_NA])


def list_check(builder, context, obj):
    eieu__nvf = context.get_argument_type(types.pyobject)
    xmft__lqssy = context.get_value_type(types.int32)
    koxnd__qkjp = lir.FunctionType(xmft__lqssy, [eieu__nvf])
    hikad__esi = cgutils.get_or_insert_function(builder.module, koxnd__qkjp,
        name='list_check')
    return builder.call(hikad__esi, [obj])


def dict_keys(builder, context, obj):
    eieu__nvf = context.get_argument_type(types.pyobject)
    koxnd__qkjp = lir.FunctionType(eieu__nvf, [eieu__nvf])
    hikad__esi = cgutils.get_or_insert_function(builder.module, koxnd__qkjp,
        name='dict_keys')
    return builder.call(hikad__esi, [obj])


def dict_values(builder, context, obj):
    eieu__nvf = context.get_argument_type(types.pyobject)
    koxnd__qkjp = lir.FunctionType(eieu__nvf, [eieu__nvf])
    hikad__esi = cgutils.get_or_insert_function(builder.module, koxnd__qkjp,
        name='dict_values')
    return builder.call(hikad__esi, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    eieu__nvf = context.get_argument_type(types.pyobject)
    koxnd__qkjp = lir.FunctionType(lir.VoidType(), [eieu__nvf, eieu__nvf])
    hikad__esi = cgutils.get_or_insert_function(builder.module, koxnd__qkjp,
        name='dict_merge_from_seq2')
    builder.call(hikad__esi, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    enf__tkh = cgutils.alloca_once_value(builder, val)
    yatr__nbj = list_check(builder, context, val)
    xuhpj__ywgyj = builder.icmp_unsigned('!=', yatr__nbj, lir.Constant(
        yatr__nbj.type, 0))
    with builder.if_then(xuhpj__ywgyj):
        vwqdv__mbxm = context.insert_const_string(builder.module, 'numpy')
        rpd__wvda = c.pyapi.import_module_noblock(vwqdv__mbxm)
        gqx__dsmt = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            gqx__dsmt = str(typ.dtype)
        vkc__saqip = c.pyapi.object_getattr_string(rpd__wvda, gqx__dsmt)
        vps__aab = builder.load(enf__tkh)
        cwvc__apvm = c.pyapi.call_method(rpd__wvda, 'asarray', (vps__aab,
            vkc__saqip))
        builder.store(cwvc__apvm, enf__tkh)
        c.pyapi.decref(rpd__wvda)
        c.pyapi.decref(vkc__saqip)
    val = builder.load(enf__tkh)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        sopvi__vdept = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        jmuul__era, voq__plgzn = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [sopvi__vdept])
        context.nrt.decref(builder, typ, sopvi__vdept)
        return cgutils.pack_array(builder, [voq__plgzn])
    if isinstance(typ, (StructType, types.BaseTuple)):
        vwqdv__mbxm = context.insert_const_string(builder.module, 'pandas')
        uvvev__agpjh = c.pyapi.import_module_noblock(vwqdv__mbxm)
        C_NA = c.pyapi.object_getattr_string(uvvev__agpjh, 'NA')
        nfgwf__wibvl = bodo.utils.transform.get_type_alloc_counts(typ)
        irh__cfcp = context.make_tuple(builder, types.Tuple(nfgwf__wibvl *
            [types.int64]), nfgwf__wibvl * [context.get_constant(types.
            int64, 0)])
        hat__npmw = cgutils.alloca_once_value(builder, irh__cfcp)
        ltc__inl = 0
        gvnv__sbeh = typ.data if isinstance(typ, StructType) else typ.types
        for pxkuk__zxtc, t in enumerate(gvnv__sbeh):
            gwo__qmt = bodo.utils.transform.get_type_alloc_counts(t)
            if gwo__qmt == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    pxkuk__zxtc])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, pxkuk__zxtc)
            kly__krz = is_na_value(builder, context, val_obj, C_NA)
            zgnk__uud = builder.icmp_unsigned('!=', kly__krz, lir.Constant(
                kly__krz.type, 1))
            with builder.if_then(zgnk__uud):
                irh__cfcp = builder.load(hat__npmw)
                atjv__oafnr = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for pxkuk__zxtc in range(gwo__qmt):
                    wkrz__jdakx = builder.extract_value(irh__cfcp, ltc__inl +
                        pxkuk__zxtc)
                    jlfr__kdcr = builder.extract_value(atjv__oafnr, pxkuk__zxtc
                        )
                    irh__cfcp = builder.insert_value(irh__cfcp, builder.add
                        (wkrz__jdakx, jlfr__kdcr), ltc__inl + pxkuk__zxtc)
                builder.store(irh__cfcp, hat__npmw)
            ltc__inl += gwo__qmt
        c.pyapi.decref(uvvev__agpjh)
        c.pyapi.decref(C_NA)
        return builder.load(hat__npmw)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    vwqdv__mbxm = context.insert_const_string(builder.module, 'pandas')
    uvvev__agpjh = c.pyapi.import_module_noblock(vwqdv__mbxm)
    C_NA = c.pyapi.object_getattr_string(uvvev__agpjh, 'NA')
    nfgwf__wibvl = bodo.utils.transform.get_type_alloc_counts(typ)
    irh__cfcp = context.make_tuple(builder, types.Tuple(nfgwf__wibvl * [
        types.int64]), [n] + (nfgwf__wibvl - 1) * [context.get_constant(
        types.int64, 0)])
    hat__npmw = cgutils.alloca_once_value(builder, irh__cfcp)
    with cgutils.for_range(builder, n) as vbqky__cztkb:
        urxq__jzgzg = vbqky__cztkb.index
        rti__fgz = seq_getitem(builder, context, arr_obj, urxq__jzgzg)
        kly__krz = is_na_value(builder, context, rti__fgz, C_NA)
        zgnk__uud = builder.icmp_unsigned('!=', kly__krz, lir.Constant(
            kly__krz.type, 1))
        with builder.if_then(zgnk__uud):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                irh__cfcp = builder.load(hat__npmw)
                atjv__oafnr = get_array_elem_counts(c, builder, context,
                    rti__fgz, typ.dtype)
                for pxkuk__zxtc in range(nfgwf__wibvl - 1):
                    wkrz__jdakx = builder.extract_value(irh__cfcp, 
                        pxkuk__zxtc + 1)
                    jlfr__kdcr = builder.extract_value(atjv__oafnr, pxkuk__zxtc
                        )
                    irh__cfcp = builder.insert_value(irh__cfcp, builder.add
                        (wkrz__jdakx, jlfr__kdcr), pxkuk__zxtc + 1)
                builder.store(irh__cfcp, hat__npmw)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                ltc__inl = 1
                for pxkuk__zxtc, t in enumerate(typ.data):
                    gwo__qmt = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if gwo__qmt == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(rti__fgz, pxkuk__zxtc)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(rti__fgz, typ
                            .names[pxkuk__zxtc])
                    kly__krz = is_na_value(builder, context, val_obj, C_NA)
                    zgnk__uud = builder.icmp_unsigned('!=', kly__krz, lir.
                        Constant(kly__krz.type, 1))
                    with builder.if_then(zgnk__uud):
                        irh__cfcp = builder.load(hat__npmw)
                        atjv__oafnr = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for pxkuk__zxtc in range(gwo__qmt):
                            wkrz__jdakx = builder.extract_value(irh__cfcp, 
                                ltc__inl + pxkuk__zxtc)
                            jlfr__kdcr = builder.extract_value(atjv__oafnr,
                                pxkuk__zxtc)
                            irh__cfcp = builder.insert_value(irh__cfcp,
                                builder.add(wkrz__jdakx, jlfr__kdcr), 
                                ltc__inl + pxkuk__zxtc)
                        builder.store(irh__cfcp, hat__npmw)
                    ltc__inl += gwo__qmt
            else:
                assert isinstance(typ, MapArrayType), typ
                irh__cfcp = builder.load(hat__npmw)
                jmpi__wxft = dict_keys(builder, context, rti__fgz)
                jyxjw__njd = dict_values(builder, context, rti__fgz)
                dovi__hrbgk = get_array_elem_counts(c, builder, context,
                    jmpi__wxft, typ.key_arr_type)
                hzsf__fxmk = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for pxkuk__zxtc in range(1, hzsf__fxmk + 1):
                    wkrz__jdakx = builder.extract_value(irh__cfcp, pxkuk__zxtc)
                    jlfr__kdcr = builder.extract_value(dovi__hrbgk, 
                        pxkuk__zxtc - 1)
                    irh__cfcp = builder.insert_value(irh__cfcp, builder.add
                        (wkrz__jdakx, jlfr__kdcr), pxkuk__zxtc)
                mtj__gvy = get_array_elem_counts(c, builder, context,
                    jyxjw__njd, typ.value_arr_type)
                for pxkuk__zxtc in range(hzsf__fxmk + 1, nfgwf__wibvl):
                    wkrz__jdakx = builder.extract_value(irh__cfcp, pxkuk__zxtc)
                    jlfr__kdcr = builder.extract_value(mtj__gvy, 
                        pxkuk__zxtc - hzsf__fxmk)
                    irh__cfcp = builder.insert_value(irh__cfcp, builder.add
                        (wkrz__jdakx, jlfr__kdcr), pxkuk__zxtc)
                builder.store(irh__cfcp, hat__npmw)
                c.pyapi.decref(jmpi__wxft)
                c.pyapi.decref(jyxjw__njd)
        c.pyapi.decref(rti__fgz)
    c.pyapi.decref(uvvev__agpjh)
    c.pyapi.decref(C_NA)
    return builder.load(hat__npmw)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    rznt__azcn = n_elems.type.count
    assert rznt__azcn >= 1
    cyov__zpxi = builder.extract_value(n_elems, 0)
    if rznt__azcn != 1:
        ugf__aidy = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, pxkuk__zxtc) for pxkuk__zxtc in range(1, rznt__azcn)])
        dmm__mzw = types.Tuple([types.int64] * (rznt__azcn - 1))
    else:
        ugf__aidy = context.get_dummy_value()
        dmm__mzw = types.none
    khqo__vamod = types.TypeRef(arr_type)
    vbl__gvxto = arr_type(types.int64, khqo__vamod, dmm__mzw)
    args = [cyov__zpxi, context.get_dummy_value(), ugf__aidy]
    tzb__ivee = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        jmuul__era, nwa__oda = c.pyapi.call_jit_code(tzb__ivee, vbl__gvxto,
            args)
    else:
        nwa__oda = context.compile_internal(builder, tzb__ivee, vbl__gvxto,
            args)
    return nwa__oda


def is_ll_eq(builder, val1, val2):
    egyq__dnk = val1.type.pointee
    pzzr__jck = val2.type.pointee
    assert egyq__dnk == pzzr__jck, 'invalid llvm value comparison'
    if isinstance(egyq__dnk, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(egyq__dnk.elements) if isinstance(egyq__dnk, lir.
            BaseStructType) else egyq__dnk.count
        wsl__xcuas = lir.Constant(lir.IntType(1), 1)
        for pxkuk__zxtc in range(n_elems):
            oohi__iqcal = lir.IntType(32)(0)
            rxq__jye = lir.IntType(32)(pxkuk__zxtc)
            eddmh__ukmp = builder.gep(val1, [oohi__iqcal, rxq__jye],
                inbounds=True)
            llh__pdx = builder.gep(val2, [oohi__iqcal, rxq__jye], inbounds=True
                )
            wsl__xcuas = builder.and_(wsl__xcuas, is_ll_eq(builder,
                eddmh__ukmp, llh__pdx))
        return wsl__xcuas
    clgfh__zld = builder.load(val1)
    zqfar__mjy = builder.load(val2)
    if clgfh__zld.type in (lir.FloatType(), lir.DoubleType()):
        vfaid__pynmy = 32 if clgfh__zld.type == lir.FloatType() else 64
        clgfh__zld = builder.bitcast(clgfh__zld, lir.IntType(vfaid__pynmy))
        zqfar__mjy = builder.bitcast(zqfar__mjy, lir.IntType(vfaid__pynmy))
    return builder.icmp_unsigned('==', clgfh__zld, zqfar__mjy)
