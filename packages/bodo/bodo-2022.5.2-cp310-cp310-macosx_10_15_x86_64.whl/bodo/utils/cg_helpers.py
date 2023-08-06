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
    fmocb__uzzph = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    jin__bsoh = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    kacju__xtyx = builder.gep(null_bitmap_ptr, [fmocb__uzzph], inbounds=True)
    uon__haqe = builder.load(kacju__xtyx)
    ayzdl__qln = lir.ArrayType(lir.IntType(8), 8)
    oebn__dtfxm = cgutils.alloca_once_value(builder, lir.Constant(
        ayzdl__qln, (1, 2, 4, 8, 16, 32, 64, 128)))
    koyk__djo = builder.load(builder.gep(oebn__dtfxm, [lir.Constant(lir.
        IntType(64), 0), jin__bsoh], inbounds=True))
    if val:
        builder.store(builder.or_(uon__haqe, koyk__djo), kacju__xtyx)
    else:
        koyk__djo = builder.xor(koyk__djo, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(uon__haqe, koyk__djo), kacju__xtyx)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    fmocb__uzzph = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    jin__bsoh = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    uon__haqe = builder.load(builder.gep(null_bitmap_ptr, [fmocb__uzzph],
        inbounds=True))
    ayzdl__qln = lir.ArrayType(lir.IntType(8), 8)
    oebn__dtfxm = cgutils.alloca_once_value(builder, lir.Constant(
        ayzdl__qln, (1, 2, 4, 8, 16, 32, 64, 128)))
    koyk__djo = builder.load(builder.gep(oebn__dtfxm, [lir.Constant(lir.
        IntType(64), 0), jin__bsoh], inbounds=True))
    return builder.and_(uon__haqe, koyk__djo)


def pyarray_check(builder, context, obj):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    zqcwn__qnrsd = lir.FunctionType(lir.IntType(32), [rrdyr__ltmgn])
    poabc__qgj = cgutils.get_or_insert_function(builder.module,
        zqcwn__qnrsd, name='is_np_array')
    return builder.call(poabc__qgj, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    qloal__qjvte = context.get_value_type(types.intp)
    zrph__chd = lir.FunctionType(lir.IntType(8).as_pointer(), [rrdyr__ltmgn,
        qloal__qjvte])
    ptv__fxzxk = cgutils.get_or_insert_function(builder.module, zrph__chd,
        name='array_getptr1')
    vzms__qchj = lir.FunctionType(rrdyr__ltmgn, [rrdyr__ltmgn, lir.IntType(
        8).as_pointer()])
    hnpu__btub = cgutils.get_or_insert_function(builder.module, vzms__qchj,
        name='array_getitem')
    ire__uichy = builder.call(ptv__fxzxk, [arr_obj, ind])
    return builder.call(hnpu__btub, [arr_obj, ire__uichy])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    qloal__qjvte = context.get_value_type(types.intp)
    zrph__chd = lir.FunctionType(lir.IntType(8).as_pointer(), [rrdyr__ltmgn,
        qloal__qjvte])
    ptv__fxzxk = cgutils.get_or_insert_function(builder.module, zrph__chd,
        name='array_getptr1')
    qxgv__vekq = lir.FunctionType(lir.VoidType(), [rrdyr__ltmgn, lir.
        IntType(8).as_pointer(), rrdyr__ltmgn])
    per__wvj = cgutils.get_or_insert_function(builder.module, qxgv__vekq,
        name='array_setitem')
    ire__uichy = builder.call(ptv__fxzxk, [arr_obj, ind])
    builder.call(per__wvj, [arr_obj, ire__uichy, val_obj])


def seq_getitem(builder, context, obj, ind):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    qloal__qjvte = context.get_value_type(types.intp)
    pdh__agae = lir.FunctionType(rrdyr__ltmgn, [rrdyr__ltmgn, qloal__qjvte])
    dwhjd__ewts = cgutils.get_or_insert_function(builder.module, pdh__agae,
        name='seq_getitem')
    return builder.call(dwhjd__ewts, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    wvzt__zixt = lir.FunctionType(lir.IntType(32), [rrdyr__ltmgn, rrdyr__ltmgn]
        )
    rrgme__kfb = cgutils.get_or_insert_function(builder.module, wvzt__zixt,
        name='is_na_value')
    return builder.call(rrgme__kfb, [val, C_NA])


def list_check(builder, context, obj):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    wskur__hfo = context.get_value_type(types.int32)
    kad__kndl = lir.FunctionType(wskur__hfo, [rrdyr__ltmgn])
    vyop__gri = cgutils.get_or_insert_function(builder.module, kad__kndl,
        name='list_check')
    return builder.call(vyop__gri, [obj])


def dict_keys(builder, context, obj):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    kad__kndl = lir.FunctionType(rrdyr__ltmgn, [rrdyr__ltmgn])
    vyop__gri = cgutils.get_or_insert_function(builder.module, kad__kndl,
        name='dict_keys')
    return builder.call(vyop__gri, [obj])


def dict_values(builder, context, obj):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    kad__kndl = lir.FunctionType(rrdyr__ltmgn, [rrdyr__ltmgn])
    vyop__gri = cgutils.get_or_insert_function(builder.module, kad__kndl,
        name='dict_values')
    return builder.call(vyop__gri, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    rrdyr__ltmgn = context.get_argument_type(types.pyobject)
    kad__kndl = lir.FunctionType(lir.VoidType(), [rrdyr__ltmgn, rrdyr__ltmgn])
    vyop__gri = cgutils.get_or_insert_function(builder.module, kad__kndl,
        name='dict_merge_from_seq2')
    builder.call(vyop__gri, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    xsoqo__bpo = cgutils.alloca_once_value(builder, val)
    pgltg__vfhv = list_check(builder, context, val)
    owwh__cyo = builder.icmp_unsigned('!=', pgltg__vfhv, lir.Constant(
        pgltg__vfhv.type, 0))
    with builder.if_then(owwh__cyo):
        heug__qhtx = context.insert_const_string(builder.module, 'numpy')
        wlql__wcu = c.pyapi.import_module_noblock(heug__qhtx)
        sls__qdp = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            sls__qdp = str(typ.dtype)
        fdchf__woc = c.pyapi.object_getattr_string(wlql__wcu, sls__qdp)
        rfk__ocdp = builder.load(xsoqo__bpo)
        mfh__quina = c.pyapi.call_method(wlql__wcu, 'asarray', (rfk__ocdp,
            fdchf__woc))
        builder.store(mfh__quina, xsoqo__bpo)
        c.pyapi.decref(wlql__wcu)
        c.pyapi.decref(fdchf__woc)
    val = builder.load(xsoqo__bpo)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        ipubu__tumss = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        bvfkt__qbcsb, wdxgj__qsp = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [ipubu__tumss])
        context.nrt.decref(builder, typ, ipubu__tumss)
        return cgutils.pack_array(builder, [wdxgj__qsp])
    if isinstance(typ, (StructType, types.BaseTuple)):
        heug__qhtx = context.insert_const_string(builder.module, 'pandas')
        wxp__httek = c.pyapi.import_module_noblock(heug__qhtx)
        C_NA = c.pyapi.object_getattr_string(wxp__httek, 'NA')
        lzdw__qpazn = bodo.utils.transform.get_type_alloc_counts(typ)
        bcw__qcy = context.make_tuple(builder, types.Tuple(lzdw__qpazn * [
            types.int64]), lzdw__qpazn * [context.get_constant(types.int64, 0)]
            )
        wsmmi__gvmi = cgutils.alloca_once_value(builder, bcw__qcy)
        nfvr__mao = 0
        rqm__vue = typ.data if isinstance(typ, StructType) else typ.types
        for axdl__ybwx, t in enumerate(rqm__vue):
            dnq__lrk = bodo.utils.transform.get_type_alloc_counts(t)
            if dnq__lrk == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    axdl__ybwx])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, axdl__ybwx)
            qat__lvrmd = is_na_value(builder, context, val_obj, C_NA)
            eukte__nmivg = builder.icmp_unsigned('!=', qat__lvrmd, lir.
                Constant(qat__lvrmd.type, 1))
            with builder.if_then(eukte__nmivg):
                bcw__qcy = builder.load(wsmmi__gvmi)
                hqesf__fhvj = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for axdl__ybwx in range(dnq__lrk):
                    hsbpz__ews = builder.extract_value(bcw__qcy, nfvr__mao +
                        axdl__ybwx)
                    uhk__muu = builder.extract_value(hqesf__fhvj, axdl__ybwx)
                    bcw__qcy = builder.insert_value(bcw__qcy, builder.add(
                        hsbpz__ews, uhk__muu), nfvr__mao + axdl__ybwx)
                builder.store(bcw__qcy, wsmmi__gvmi)
            nfvr__mao += dnq__lrk
        c.pyapi.decref(wxp__httek)
        c.pyapi.decref(C_NA)
        return builder.load(wsmmi__gvmi)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    heug__qhtx = context.insert_const_string(builder.module, 'pandas')
    wxp__httek = c.pyapi.import_module_noblock(heug__qhtx)
    C_NA = c.pyapi.object_getattr_string(wxp__httek, 'NA')
    lzdw__qpazn = bodo.utils.transform.get_type_alloc_counts(typ)
    bcw__qcy = context.make_tuple(builder, types.Tuple(lzdw__qpazn * [types
        .int64]), [n] + (lzdw__qpazn - 1) * [context.get_constant(types.
        int64, 0)])
    wsmmi__gvmi = cgutils.alloca_once_value(builder, bcw__qcy)
    with cgutils.for_range(builder, n) as jadpl__wuw:
        gwcng__uzxpa = jadpl__wuw.index
        ssv__airn = seq_getitem(builder, context, arr_obj, gwcng__uzxpa)
        qat__lvrmd = is_na_value(builder, context, ssv__airn, C_NA)
        eukte__nmivg = builder.icmp_unsigned('!=', qat__lvrmd, lir.Constant
            (qat__lvrmd.type, 1))
        with builder.if_then(eukte__nmivg):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                bcw__qcy = builder.load(wsmmi__gvmi)
                hqesf__fhvj = get_array_elem_counts(c, builder, context,
                    ssv__airn, typ.dtype)
                for axdl__ybwx in range(lzdw__qpazn - 1):
                    hsbpz__ews = builder.extract_value(bcw__qcy, axdl__ybwx + 1
                        )
                    uhk__muu = builder.extract_value(hqesf__fhvj, axdl__ybwx)
                    bcw__qcy = builder.insert_value(bcw__qcy, builder.add(
                        hsbpz__ews, uhk__muu), axdl__ybwx + 1)
                builder.store(bcw__qcy, wsmmi__gvmi)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                nfvr__mao = 1
                for axdl__ybwx, t in enumerate(typ.data):
                    dnq__lrk = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if dnq__lrk == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(ssv__airn, axdl__ybwx)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(ssv__airn,
                            typ.names[axdl__ybwx])
                    qat__lvrmd = is_na_value(builder, context, val_obj, C_NA)
                    eukte__nmivg = builder.icmp_unsigned('!=', qat__lvrmd,
                        lir.Constant(qat__lvrmd.type, 1))
                    with builder.if_then(eukte__nmivg):
                        bcw__qcy = builder.load(wsmmi__gvmi)
                        hqesf__fhvj = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for axdl__ybwx in range(dnq__lrk):
                            hsbpz__ews = builder.extract_value(bcw__qcy, 
                                nfvr__mao + axdl__ybwx)
                            uhk__muu = builder.extract_value(hqesf__fhvj,
                                axdl__ybwx)
                            bcw__qcy = builder.insert_value(bcw__qcy,
                                builder.add(hsbpz__ews, uhk__muu), 
                                nfvr__mao + axdl__ybwx)
                        builder.store(bcw__qcy, wsmmi__gvmi)
                    nfvr__mao += dnq__lrk
            else:
                assert isinstance(typ, MapArrayType), typ
                bcw__qcy = builder.load(wsmmi__gvmi)
                qzonz__pims = dict_keys(builder, context, ssv__airn)
                iebp__pcp = dict_values(builder, context, ssv__airn)
                sknlz__eweb = get_array_elem_counts(c, builder, context,
                    qzonz__pims, typ.key_arr_type)
                ytc__wnx = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for axdl__ybwx in range(1, ytc__wnx + 1):
                    hsbpz__ews = builder.extract_value(bcw__qcy, axdl__ybwx)
                    uhk__muu = builder.extract_value(sknlz__eweb, 
                        axdl__ybwx - 1)
                    bcw__qcy = builder.insert_value(bcw__qcy, builder.add(
                        hsbpz__ews, uhk__muu), axdl__ybwx)
                wzfq__tge = get_array_elem_counts(c, builder, context,
                    iebp__pcp, typ.value_arr_type)
                for axdl__ybwx in range(ytc__wnx + 1, lzdw__qpazn):
                    hsbpz__ews = builder.extract_value(bcw__qcy, axdl__ybwx)
                    uhk__muu = builder.extract_value(wzfq__tge, axdl__ybwx -
                        ytc__wnx)
                    bcw__qcy = builder.insert_value(bcw__qcy, builder.add(
                        hsbpz__ews, uhk__muu), axdl__ybwx)
                builder.store(bcw__qcy, wsmmi__gvmi)
                c.pyapi.decref(qzonz__pims)
                c.pyapi.decref(iebp__pcp)
        c.pyapi.decref(ssv__airn)
    c.pyapi.decref(wxp__httek)
    c.pyapi.decref(C_NA)
    return builder.load(wsmmi__gvmi)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    npaap__ign = n_elems.type.count
    assert npaap__ign >= 1
    hkwx__chf = builder.extract_value(n_elems, 0)
    if npaap__ign != 1:
        atvd__onjd = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, axdl__ybwx) for axdl__ybwx in range(1, npaap__ign)])
        mguzf__yoo = types.Tuple([types.int64] * (npaap__ign - 1))
    else:
        atvd__onjd = context.get_dummy_value()
        mguzf__yoo = types.none
    qaoef__qxuu = types.TypeRef(arr_type)
    ltom__hxcgd = arr_type(types.int64, qaoef__qxuu, mguzf__yoo)
    args = [hkwx__chf, context.get_dummy_value(), atvd__onjd]
    beq__udau = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        bvfkt__qbcsb, rtxl__vsds = c.pyapi.call_jit_code(beq__udau,
            ltom__hxcgd, args)
    else:
        rtxl__vsds = context.compile_internal(builder, beq__udau,
            ltom__hxcgd, args)
    return rtxl__vsds


def is_ll_eq(builder, val1, val2):
    pcmcp__bsi = val1.type.pointee
    ucr__djber = val2.type.pointee
    assert pcmcp__bsi == ucr__djber, 'invalid llvm value comparison'
    if isinstance(pcmcp__bsi, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(pcmcp__bsi.elements) if isinstance(pcmcp__bsi, lir.
            BaseStructType) else pcmcp__bsi.count
        ulj__mfy = lir.Constant(lir.IntType(1), 1)
        for axdl__ybwx in range(n_elems):
            xpp__lsrto = lir.IntType(32)(0)
            mivnl__limen = lir.IntType(32)(axdl__ybwx)
            retm__qjelz = builder.gep(val1, [xpp__lsrto, mivnl__limen],
                inbounds=True)
            glq__haj = builder.gep(val2, [xpp__lsrto, mivnl__limen],
                inbounds=True)
            ulj__mfy = builder.and_(ulj__mfy, is_ll_eq(builder, retm__qjelz,
                glq__haj))
        return ulj__mfy
    vwoi__rlz = builder.load(val1)
    gyija__dmrcc = builder.load(val2)
    if vwoi__rlz.type in (lir.FloatType(), lir.DoubleType()):
        kecic__ojclq = 32 if vwoi__rlz.type == lir.FloatType() else 64
        vwoi__rlz = builder.bitcast(vwoi__rlz, lir.IntType(kecic__ojclq))
        gyija__dmrcc = builder.bitcast(gyija__dmrcc, lir.IntType(kecic__ojclq))
    return builder.icmp_unsigned('==', vwoi__rlz, gyija__dmrcc)
