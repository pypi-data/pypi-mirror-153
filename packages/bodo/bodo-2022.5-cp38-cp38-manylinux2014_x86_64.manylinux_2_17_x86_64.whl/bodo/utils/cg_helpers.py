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
    phlbc__zxbq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    dac__qlg = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    qeu__lsyo = builder.gep(null_bitmap_ptr, [phlbc__zxbq], inbounds=True)
    zqp__uttmf = builder.load(qeu__lsyo)
    uis__vda = lir.ArrayType(lir.IntType(8), 8)
    jwpx__pkz = cgutils.alloca_once_value(builder, lir.Constant(uis__vda, (
        1, 2, 4, 8, 16, 32, 64, 128)))
    zub__vpv = builder.load(builder.gep(jwpx__pkz, [lir.Constant(lir.
        IntType(64), 0), dac__qlg], inbounds=True))
    if val:
        builder.store(builder.or_(zqp__uttmf, zub__vpv), qeu__lsyo)
    else:
        zub__vpv = builder.xor(zub__vpv, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(zqp__uttmf, zub__vpv), qeu__lsyo)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    phlbc__zxbq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    dac__qlg = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    zqp__uttmf = builder.load(builder.gep(null_bitmap_ptr, [phlbc__zxbq],
        inbounds=True))
    uis__vda = lir.ArrayType(lir.IntType(8), 8)
    jwpx__pkz = cgutils.alloca_once_value(builder, lir.Constant(uis__vda, (
        1, 2, 4, 8, 16, 32, 64, 128)))
    zub__vpv = builder.load(builder.gep(jwpx__pkz, [lir.Constant(lir.
        IntType(64), 0), dac__qlg], inbounds=True))
    return builder.and_(zqp__uttmf, zub__vpv)


def pyarray_check(builder, context, obj):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    tayu__ksedu = lir.FunctionType(lir.IntType(32), [nlxca__ckg])
    kqvqu__ncrs = cgutils.get_or_insert_function(builder.module,
        tayu__ksedu, name='is_np_array')
    return builder.call(kqvqu__ncrs, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    amcj__etzr = context.get_value_type(types.intp)
    yvx__sxwp = lir.FunctionType(lir.IntType(8).as_pointer(), [nlxca__ckg,
        amcj__etzr])
    vcnqu__mbm = cgutils.get_or_insert_function(builder.module, yvx__sxwp,
        name='array_getptr1')
    tcbf__lwe = lir.FunctionType(nlxca__ckg, [nlxca__ckg, lir.IntType(8).
        as_pointer()])
    krs__txvew = cgutils.get_or_insert_function(builder.module, tcbf__lwe,
        name='array_getitem')
    cvph__mbyy = builder.call(vcnqu__mbm, [arr_obj, ind])
    return builder.call(krs__txvew, [arr_obj, cvph__mbyy])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    amcj__etzr = context.get_value_type(types.intp)
    yvx__sxwp = lir.FunctionType(lir.IntType(8).as_pointer(), [nlxca__ckg,
        amcj__etzr])
    vcnqu__mbm = cgutils.get_or_insert_function(builder.module, yvx__sxwp,
        name='array_getptr1')
    xurb__rsvs = lir.FunctionType(lir.VoidType(), [nlxca__ckg, lir.IntType(
        8).as_pointer(), nlxca__ckg])
    rgo__kkuzx = cgutils.get_or_insert_function(builder.module, xurb__rsvs,
        name='array_setitem')
    cvph__mbyy = builder.call(vcnqu__mbm, [arr_obj, ind])
    builder.call(rgo__kkuzx, [arr_obj, cvph__mbyy, val_obj])


def seq_getitem(builder, context, obj, ind):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    amcj__etzr = context.get_value_type(types.intp)
    wfg__tlezu = lir.FunctionType(nlxca__ckg, [nlxca__ckg, amcj__etzr])
    hygdd__ayjqy = cgutils.get_or_insert_function(builder.module,
        wfg__tlezu, name='seq_getitem')
    return builder.call(hygdd__ayjqy, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    qqpd__cdbj = lir.FunctionType(lir.IntType(32), [nlxca__ckg, nlxca__ckg])
    ylsuh__tjkx = cgutils.get_or_insert_function(builder.module, qqpd__cdbj,
        name='is_na_value')
    return builder.call(ylsuh__tjkx, [val, C_NA])


def list_check(builder, context, obj):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    ghacz__gnrvt = context.get_value_type(types.int32)
    geqi__fvdt = lir.FunctionType(ghacz__gnrvt, [nlxca__ckg])
    mjg__mthk = cgutils.get_or_insert_function(builder.module, geqi__fvdt,
        name='list_check')
    return builder.call(mjg__mthk, [obj])


def dict_keys(builder, context, obj):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    geqi__fvdt = lir.FunctionType(nlxca__ckg, [nlxca__ckg])
    mjg__mthk = cgutils.get_or_insert_function(builder.module, geqi__fvdt,
        name='dict_keys')
    return builder.call(mjg__mthk, [obj])


def dict_values(builder, context, obj):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    geqi__fvdt = lir.FunctionType(nlxca__ckg, [nlxca__ckg])
    mjg__mthk = cgutils.get_or_insert_function(builder.module, geqi__fvdt,
        name='dict_values')
    return builder.call(mjg__mthk, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    nlxca__ckg = context.get_argument_type(types.pyobject)
    geqi__fvdt = lir.FunctionType(lir.VoidType(), [nlxca__ckg, nlxca__ckg])
    mjg__mthk = cgutils.get_or_insert_function(builder.module, geqi__fvdt,
        name='dict_merge_from_seq2')
    builder.call(mjg__mthk, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    yia__zofak = cgutils.alloca_once_value(builder, val)
    ycdj__avacj = list_check(builder, context, val)
    wcci__rzp = builder.icmp_unsigned('!=', ycdj__avacj, lir.Constant(
        ycdj__avacj.type, 0))
    with builder.if_then(wcci__rzp):
        mgf__zteis = context.insert_const_string(builder.module, 'numpy')
        ulqqc__dtn = c.pyapi.import_module_noblock(mgf__zteis)
        mgkc__bpkm = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            mgkc__bpkm = str(typ.dtype)
        jgyk__fhi = c.pyapi.object_getattr_string(ulqqc__dtn, mgkc__bpkm)
        ztz__ivbzx = builder.load(yia__zofak)
        gkzh__fkzk = c.pyapi.call_method(ulqqc__dtn, 'asarray', (ztz__ivbzx,
            jgyk__fhi))
        builder.store(gkzh__fkzk, yia__zofak)
        c.pyapi.decref(ulqqc__dtn)
        c.pyapi.decref(jgyk__fhi)
    val = builder.load(yia__zofak)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        rjpw__cvzz = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        jkpzc__xan, sgge__swlt = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [rjpw__cvzz])
        context.nrt.decref(builder, typ, rjpw__cvzz)
        return cgutils.pack_array(builder, [sgge__swlt])
    if isinstance(typ, (StructType, types.BaseTuple)):
        mgf__zteis = context.insert_const_string(builder.module, 'pandas')
        myztp__scyho = c.pyapi.import_module_noblock(mgf__zteis)
        C_NA = c.pyapi.object_getattr_string(myztp__scyho, 'NA')
        hdfsd__yzxbh = bodo.utils.transform.get_type_alloc_counts(typ)
        ymv__dehf = context.make_tuple(builder, types.Tuple(hdfsd__yzxbh *
            [types.int64]), hdfsd__yzxbh * [context.get_constant(types.
            int64, 0)])
        njjl__rlnf = cgutils.alloca_once_value(builder, ymv__dehf)
        dfh__rljnf = 0
        wmfwi__nvn = typ.data if isinstance(typ, StructType) else typ.types
        for pxwga__npr, t in enumerate(wmfwi__nvn):
            det__gsypg = bodo.utils.transform.get_type_alloc_counts(t)
            if det__gsypg == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    pxwga__npr])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, pxwga__npr)
            kfd__rph = is_na_value(builder, context, val_obj, C_NA)
            onv__whl = builder.icmp_unsigned('!=', kfd__rph, lir.Constant(
                kfd__rph.type, 1))
            with builder.if_then(onv__whl):
                ymv__dehf = builder.load(njjl__rlnf)
                qfs__qmh = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for pxwga__npr in range(det__gsypg):
                    yvr__qgb = builder.extract_value(ymv__dehf, dfh__rljnf +
                        pxwga__npr)
                    tdg__bfiv = builder.extract_value(qfs__qmh, pxwga__npr)
                    ymv__dehf = builder.insert_value(ymv__dehf, builder.add
                        (yvr__qgb, tdg__bfiv), dfh__rljnf + pxwga__npr)
                builder.store(ymv__dehf, njjl__rlnf)
            dfh__rljnf += det__gsypg
        c.pyapi.decref(myztp__scyho)
        c.pyapi.decref(C_NA)
        return builder.load(njjl__rlnf)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    mgf__zteis = context.insert_const_string(builder.module, 'pandas')
    myztp__scyho = c.pyapi.import_module_noblock(mgf__zteis)
    C_NA = c.pyapi.object_getattr_string(myztp__scyho, 'NA')
    hdfsd__yzxbh = bodo.utils.transform.get_type_alloc_counts(typ)
    ymv__dehf = context.make_tuple(builder, types.Tuple(hdfsd__yzxbh * [
        types.int64]), [n] + (hdfsd__yzxbh - 1) * [context.get_constant(
        types.int64, 0)])
    njjl__rlnf = cgutils.alloca_once_value(builder, ymv__dehf)
    with cgutils.for_range(builder, n) as gfpy__msab:
        wctct__iai = gfpy__msab.index
        cjg__evkxb = seq_getitem(builder, context, arr_obj, wctct__iai)
        kfd__rph = is_na_value(builder, context, cjg__evkxb, C_NA)
        onv__whl = builder.icmp_unsigned('!=', kfd__rph, lir.Constant(
            kfd__rph.type, 1))
        with builder.if_then(onv__whl):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                ymv__dehf = builder.load(njjl__rlnf)
                qfs__qmh = get_array_elem_counts(c, builder, context,
                    cjg__evkxb, typ.dtype)
                for pxwga__npr in range(hdfsd__yzxbh - 1):
                    yvr__qgb = builder.extract_value(ymv__dehf, pxwga__npr + 1)
                    tdg__bfiv = builder.extract_value(qfs__qmh, pxwga__npr)
                    ymv__dehf = builder.insert_value(ymv__dehf, builder.add
                        (yvr__qgb, tdg__bfiv), pxwga__npr + 1)
                builder.store(ymv__dehf, njjl__rlnf)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                dfh__rljnf = 1
                for pxwga__npr, t in enumerate(typ.data):
                    det__gsypg = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if det__gsypg == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(cjg__evkxb, pxwga__npr)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(cjg__evkxb,
                            typ.names[pxwga__npr])
                    kfd__rph = is_na_value(builder, context, val_obj, C_NA)
                    onv__whl = builder.icmp_unsigned('!=', kfd__rph, lir.
                        Constant(kfd__rph.type, 1))
                    with builder.if_then(onv__whl):
                        ymv__dehf = builder.load(njjl__rlnf)
                        qfs__qmh = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for pxwga__npr in range(det__gsypg):
                            yvr__qgb = builder.extract_value(ymv__dehf, 
                                dfh__rljnf + pxwga__npr)
                            tdg__bfiv = builder.extract_value(qfs__qmh,
                                pxwga__npr)
                            ymv__dehf = builder.insert_value(ymv__dehf,
                                builder.add(yvr__qgb, tdg__bfiv), 
                                dfh__rljnf + pxwga__npr)
                        builder.store(ymv__dehf, njjl__rlnf)
                    dfh__rljnf += det__gsypg
            else:
                assert isinstance(typ, MapArrayType), typ
                ymv__dehf = builder.load(njjl__rlnf)
                spg__ygew = dict_keys(builder, context, cjg__evkxb)
                hfe__sehl = dict_values(builder, context, cjg__evkxb)
                wro__smtqm = get_array_elem_counts(c, builder, context,
                    spg__ygew, typ.key_arr_type)
                bwsvt__dazaf = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for pxwga__npr in range(1, bwsvt__dazaf + 1):
                    yvr__qgb = builder.extract_value(ymv__dehf, pxwga__npr)
                    tdg__bfiv = builder.extract_value(wro__smtqm, 
                        pxwga__npr - 1)
                    ymv__dehf = builder.insert_value(ymv__dehf, builder.add
                        (yvr__qgb, tdg__bfiv), pxwga__npr)
                pufkk__pudm = get_array_elem_counts(c, builder, context,
                    hfe__sehl, typ.value_arr_type)
                for pxwga__npr in range(bwsvt__dazaf + 1, hdfsd__yzxbh):
                    yvr__qgb = builder.extract_value(ymv__dehf, pxwga__npr)
                    tdg__bfiv = builder.extract_value(pufkk__pudm, 
                        pxwga__npr - bwsvt__dazaf)
                    ymv__dehf = builder.insert_value(ymv__dehf, builder.add
                        (yvr__qgb, tdg__bfiv), pxwga__npr)
                builder.store(ymv__dehf, njjl__rlnf)
                c.pyapi.decref(spg__ygew)
                c.pyapi.decref(hfe__sehl)
        c.pyapi.decref(cjg__evkxb)
    c.pyapi.decref(myztp__scyho)
    c.pyapi.decref(C_NA)
    return builder.load(njjl__rlnf)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    uiomq__afyxe = n_elems.type.count
    assert uiomq__afyxe >= 1
    nnebf__lgyk = builder.extract_value(n_elems, 0)
    if uiomq__afyxe != 1:
        vwl__zialn = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, pxwga__npr) for pxwga__npr in range(1, uiomq__afyxe)])
        twe__nqj = types.Tuple([types.int64] * (uiomq__afyxe - 1))
    else:
        vwl__zialn = context.get_dummy_value()
        twe__nqj = types.none
    uwp__iwxdg = types.TypeRef(arr_type)
    irflu__aspn = arr_type(types.int64, uwp__iwxdg, twe__nqj)
    args = [nnebf__lgyk, context.get_dummy_value(), vwl__zialn]
    fprxt__keku = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        jkpzc__xan, zgo__bayz = c.pyapi.call_jit_code(fprxt__keku,
            irflu__aspn, args)
    else:
        zgo__bayz = context.compile_internal(builder, fprxt__keku,
            irflu__aspn, args)
    return zgo__bayz


def is_ll_eq(builder, val1, val2):
    ifhz__gngeb = val1.type.pointee
    asskg__gwgvn = val2.type.pointee
    assert ifhz__gngeb == asskg__gwgvn, 'invalid llvm value comparison'
    if isinstance(ifhz__gngeb, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(ifhz__gngeb.elements) if isinstance(ifhz__gngeb, lir.
            BaseStructType) else ifhz__gngeb.count
        rrc__fsx = lir.Constant(lir.IntType(1), 1)
        for pxwga__npr in range(n_elems):
            zjxs__blhwl = lir.IntType(32)(0)
            kehw__spe = lir.IntType(32)(pxwga__npr)
            jjmm__duc = builder.gep(val1, [zjxs__blhwl, kehw__spe],
                inbounds=True)
            mye__nnowl = builder.gep(val2, [zjxs__blhwl, kehw__spe],
                inbounds=True)
            rrc__fsx = builder.and_(rrc__fsx, is_ll_eq(builder, jjmm__duc,
                mye__nnowl))
        return rrc__fsx
    hdgjh__azn = builder.load(val1)
    rpuu__qmqi = builder.load(val2)
    if hdgjh__azn.type in (lir.FloatType(), lir.DoubleType()):
        tts__osa = 32 if hdgjh__azn.type == lir.FloatType() else 64
        hdgjh__azn = builder.bitcast(hdgjh__azn, lir.IntType(tts__osa))
        rpuu__qmqi = builder.bitcast(rpuu__qmqi, lir.IntType(tts__osa))
    return builder.icmp_unsigned('==', hdgjh__azn, rpuu__qmqi)
