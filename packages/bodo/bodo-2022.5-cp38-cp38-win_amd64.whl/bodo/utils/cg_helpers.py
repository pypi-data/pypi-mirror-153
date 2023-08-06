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
    hbmib__pblyn = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    ykvaq__dsf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    qqbx__pbhf = builder.gep(null_bitmap_ptr, [hbmib__pblyn], inbounds=True)
    dotuk__cpw = builder.load(qqbx__pbhf)
    vmnkv__vpsw = lir.ArrayType(lir.IntType(8), 8)
    kpn__njw = cgutils.alloca_once_value(builder, lir.Constant(vmnkv__vpsw,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    iea__skult = builder.load(builder.gep(kpn__njw, [lir.Constant(lir.
        IntType(64), 0), ykvaq__dsf], inbounds=True))
    if val:
        builder.store(builder.or_(dotuk__cpw, iea__skult), qqbx__pbhf)
    else:
        iea__skult = builder.xor(iea__skult, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(dotuk__cpw, iea__skult), qqbx__pbhf)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    hbmib__pblyn = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    ykvaq__dsf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    dotuk__cpw = builder.load(builder.gep(null_bitmap_ptr, [hbmib__pblyn],
        inbounds=True))
    vmnkv__vpsw = lir.ArrayType(lir.IntType(8), 8)
    kpn__njw = cgutils.alloca_once_value(builder, lir.Constant(vmnkv__vpsw,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    iea__skult = builder.load(builder.gep(kpn__njw, [lir.Constant(lir.
        IntType(64), 0), ykvaq__dsf], inbounds=True))
    return builder.and_(dotuk__cpw, iea__skult)


def pyarray_check(builder, context, obj):
    qddpm__rve = context.get_argument_type(types.pyobject)
    nfd__qit = lir.FunctionType(lir.IntType(32), [qddpm__rve])
    den__muoyj = cgutils.get_or_insert_function(builder.module, nfd__qit,
        name='is_np_array')
    return builder.call(den__muoyj, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    qddpm__rve = context.get_argument_type(types.pyobject)
    kin__yrts = context.get_value_type(types.intp)
    hyrp__avi = lir.FunctionType(lir.IntType(8).as_pointer(), [qddpm__rve,
        kin__yrts])
    gkl__xqfqc = cgutils.get_or_insert_function(builder.module, hyrp__avi,
        name='array_getptr1')
    ljj__kbm = lir.FunctionType(qddpm__rve, [qddpm__rve, lir.IntType(8).
        as_pointer()])
    kezzv__ynlo = cgutils.get_or_insert_function(builder.module, ljj__kbm,
        name='array_getitem')
    lpr__tiwq = builder.call(gkl__xqfqc, [arr_obj, ind])
    return builder.call(kezzv__ynlo, [arr_obj, lpr__tiwq])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    qddpm__rve = context.get_argument_type(types.pyobject)
    kin__yrts = context.get_value_type(types.intp)
    hyrp__avi = lir.FunctionType(lir.IntType(8).as_pointer(), [qddpm__rve,
        kin__yrts])
    gkl__xqfqc = cgutils.get_or_insert_function(builder.module, hyrp__avi,
        name='array_getptr1')
    iaas__ypapg = lir.FunctionType(lir.VoidType(), [qddpm__rve, lir.IntType
        (8).as_pointer(), qddpm__rve])
    sblel__wsu = cgutils.get_or_insert_function(builder.module, iaas__ypapg,
        name='array_setitem')
    lpr__tiwq = builder.call(gkl__xqfqc, [arr_obj, ind])
    builder.call(sblel__wsu, [arr_obj, lpr__tiwq, val_obj])


def seq_getitem(builder, context, obj, ind):
    qddpm__rve = context.get_argument_type(types.pyobject)
    kin__yrts = context.get_value_type(types.intp)
    fsyb__nqbb = lir.FunctionType(qddpm__rve, [qddpm__rve, kin__yrts])
    mzz__pqots = cgutils.get_or_insert_function(builder.module, fsyb__nqbb,
        name='seq_getitem')
    return builder.call(mzz__pqots, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    qddpm__rve = context.get_argument_type(types.pyobject)
    sxcbv__blu = lir.FunctionType(lir.IntType(32), [qddpm__rve, qddpm__rve])
    xvt__sydk = cgutils.get_or_insert_function(builder.module, sxcbv__blu,
        name='is_na_value')
    return builder.call(xvt__sydk, [val, C_NA])


def list_check(builder, context, obj):
    qddpm__rve = context.get_argument_type(types.pyobject)
    ohqza__ejyo = context.get_value_type(types.int32)
    vevmz__ihxy = lir.FunctionType(ohqza__ejyo, [qddpm__rve])
    grx__eden = cgutils.get_or_insert_function(builder.module, vevmz__ihxy,
        name='list_check')
    return builder.call(grx__eden, [obj])


def dict_keys(builder, context, obj):
    qddpm__rve = context.get_argument_type(types.pyobject)
    vevmz__ihxy = lir.FunctionType(qddpm__rve, [qddpm__rve])
    grx__eden = cgutils.get_or_insert_function(builder.module, vevmz__ihxy,
        name='dict_keys')
    return builder.call(grx__eden, [obj])


def dict_values(builder, context, obj):
    qddpm__rve = context.get_argument_type(types.pyobject)
    vevmz__ihxy = lir.FunctionType(qddpm__rve, [qddpm__rve])
    grx__eden = cgutils.get_or_insert_function(builder.module, vevmz__ihxy,
        name='dict_values')
    return builder.call(grx__eden, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    qddpm__rve = context.get_argument_type(types.pyobject)
    vevmz__ihxy = lir.FunctionType(lir.VoidType(), [qddpm__rve, qddpm__rve])
    grx__eden = cgutils.get_or_insert_function(builder.module, vevmz__ihxy,
        name='dict_merge_from_seq2')
    builder.call(grx__eden, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    pao__nryfe = cgutils.alloca_once_value(builder, val)
    tgg__ifinj = list_check(builder, context, val)
    ahfk__weq = builder.icmp_unsigned('!=', tgg__ifinj, lir.Constant(
        tgg__ifinj.type, 0))
    with builder.if_then(ahfk__weq):
        rkvy__tjpe = context.insert_const_string(builder.module, 'numpy')
        ogo__ndda = c.pyapi.import_module_noblock(rkvy__tjpe)
        elf__ljig = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            elf__ljig = str(typ.dtype)
        gnk__vxfn = c.pyapi.object_getattr_string(ogo__ndda, elf__ljig)
        rus__nvxmc = builder.load(pao__nryfe)
        pnv__eagc = c.pyapi.call_method(ogo__ndda, 'asarray', (rus__nvxmc,
            gnk__vxfn))
        builder.store(pnv__eagc, pao__nryfe)
        c.pyapi.decref(ogo__ndda)
        c.pyapi.decref(gnk__vxfn)
    val = builder.load(pao__nryfe)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        xiddm__sovzb = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        dnyy__yoz, bfpl__haz = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [xiddm__sovzb])
        context.nrt.decref(builder, typ, xiddm__sovzb)
        return cgutils.pack_array(builder, [bfpl__haz])
    if isinstance(typ, (StructType, types.BaseTuple)):
        rkvy__tjpe = context.insert_const_string(builder.module, 'pandas')
        xyuix__fqxh = c.pyapi.import_module_noblock(rkvy__tjpe)
        C_NA = c.pyapi.object_getattr_string(xyuix__fqxh, 'NA')
        cqnz__lbsqb = bodo.utils.transform.get_type_alloc_counts(typ)
        yzt__oik = context.make_tuple(builder, types.Tuple(cqnz__lbsqb * [
            types.int64]), cqnz__lbsqb * [context.get_constant(types.int64, 0)]
            )
        rhwd__hdt = cgutils.alloca_once_value(builder, yzt__oik)
        lku__oha = 0
        eaxao__xopp = typ.data if isinstance(typ, StructType) else typ.types
        for vseax__pbct, t in enumerate(eaxao__xopp):
            gsuwn__jhj = bodo.utils.transform.get_type_alloc_counts(t)
            if gsuwn__jhj == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    vseax__pbct])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, vseax__pbct)
            xsx__ubjbk = is_na_value(builder, context, val_obj, C_NA)
            txti__kdsyv = builder.icmp_unsigned('!=', xsx__ubjbk, lir.
                Constant(xsx__ubjbk.type, 1))
            with builder.if_then(txti__kdsyv):
                yzt__oik = builder.load(rhwd__hdt)
                jvn__jet = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for vseax__pbct in range(gsuwn__jhj):
                    yyr__vikgv = builder.extract_value(yzt__oik, lku__oha +
                        vseax__pbct)
                    ctkl__fwaal = builder.extract_value(jvn__jet, vseax__pbct)
                    yzt__oik = builder.insert_value(yzt__oik, builder.add(
                        yyr__vikgv, ctkl__fwaal), lku__oha + vseax__pbct)
                builder.store(yzt__oik, rhwd__hdt)
            lku__oha += gsuwn__jhj
        c.pyapi.decref(xyuix__fqxh)
        c.pyapi.decref(C_NA)
        return builder.load(rhwd__hdt)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    rkvy__tjpe = context.insert_const_string(builder.module, 'pandas')
    xyuix__fqxh = c.pyapi.import_module_noblock(rkvy__tjpe)
    C_NA = c.pyapi.object_getattr_string(xyuix__fqxh, 'NA')
    cqnz__lbsqb = bodo.utils.transform.get_type_alloc_counts(typ)
    yzt__oik = context.make_tuple(builder, types.Tuple(cqnz__lbsqb * [types
        .int64]), [n] + (cqnz__lbsqb - 1) * [context.get_constant(types.
        int64, 0)])
    rhwd__hdt = cgutils.alloca_once_value(builder, yzt__oik)
    with cgutils.for_range(builder, n) as mvge__xplee:
        amds__jazwq = mvge__xplee.index
        rfn__dzmw = seq_getitem(builder, context, arr_obj, amds__jazwq)
        xsx__ubjbk = is_na_value(builder, context, rfn__dzmw, C_NA)
        txti__kdsyv = builder.icmp_unsigned('!=', xsx__ubjbk, lir.Constant(
            xsx__ubjbk.type, 1))
        with builder.if_then(txti__kdsyv):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                yzt__oik = builder.load(rhwd__hdt)
                jvn__jet = get_array_elem_counts(c, builder, context,
                    rfn__dzmw, typ.dtype)
                for vseax__pbct in range(cqnz__lbsqb - 1):
                    yyr__vikgv = builder.extract_value(yzt__oik, 
                        vseax__pbct + 1)
                    ctkl__fwaal = builder.extract_value(jvn__jet, vseax__pbct)
                    yzt__oik = builder.insert_value(yzt__oik, builder.add(
                        yyr__vikgv, ctkl__fwaal), vseax__pbct + 1)
                builder.store(yzt__oik, rhwd__hdt)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                lku__oha = 1
                for vseax__pbct, t in enumerate(typ.data):
                    gsuwn__jhj = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if gsuwn__jhj == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(rfn__dzmw, vseax__pbct)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(rfn__dzmw,
                            typ.names[vseax__pbct])
                    xsx__ubjbk = is_na_value(builder, context, val_obj, C_NA)
                    txti__kdsyv = builder.icmp_unsigned('!=', xsx__ubjbk,
                        lir.Constant(xsx__ubjbk.type, 1))
                    with builder.if_then(txti__kdsyv):
                        yzt__oik = builder.load(rhwd__hdt)
                        jvn__jet = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for vseax__pbct in range(gsuwn__jhj):
                            yyr__vikgv = builder.extract_value(yzt__oik, 
                                lku__oha + vseax__pbct)
                            ctkl__fwaal = builder.extract_value(jvn__jet,
                                vseax__pbct)
                            yzt__oik = builder.insert_value(yzt__oik,
                                builder.add(yyr__vikgv, ctkl__fwaal), 
                                lku__oha + vseax__pbct)
                        builder.store(yzt__oik, rhwd__hdt)
                    lku__oha += gsuwn__jhj
            else:
                assert isinstance(typ, MapArrayType), typ
                yzt__oik = builder.load(rhwd__hdt)
                kjx__ifsk = dict_keys(builder, context, rfn__dzmw)
                qgxcu__gkic = dict_values(builder, context, rfn__dzmw)
                knnh__lszdq = get_array_elem_counts(c, builder, context,
                    kjx__ifsk, typ.key_arr_type)
                vziu__psw = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for vseax__pbct in range(1, vziu__psw + 1):
                    yyr__vikgv = builder.extract_value(yzt__oik, vseax__pbct)
                    ctkl__fwaal = builder.extract_value(knnh__lszdq, 
                        vseax__pbct - 1)
                    yzt__oik = builder.insert_value(yzt__oik, builder.add(
                        yyr__vikgv, ctkl__fwaal), vseax__pbct)
                mkp__vyhu = get_array_elem_counts(c, builder, context,
                    qgxcu__gkic, typ.value_arr_type)
                for vseax__pbct in range(vziu__psw + 1, cqnz__lbsqb):
                    yyr__vikgv = builder.extract_value(yzt__oik, vseax__pbct)
                    ctkl__fwaal = builder.extract_value(mkp__vyhu, 
                        vseax__pbct - vziu__psw)
                    yzt__oik = builder.insert_value(yzt__oik, builder.add(
                        yyr__vikgv, ctkl__fwaal), vseax__pbct)
                builder.store(yzt__oik, rhwd__hdt)
                c.pyapi.decref(kjx__ifsk)
                c.pyapi.decref(qgxcu__gkic)
        c.pyapi.decref(rfn__dzmw)
    c.pyapi.decref(xyuix__fqxh)
    c.pyapi.decref(C_NA)
    return builder.load(rhwd__hdt)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    cfxn__cjkvx = n_elems.type.count
    assert cfxn__cjkvx >= 1
    hzazs__wwi = builder.extract_value(n_elems, 0)
    if cfxn__cjkvx != 1:
        wfb__dfck = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, vseax__pbct) for vseax__pbct in range(1, cfxn__cjkvx)])
        apv__ilm = types.Tuple([types.int64] * (cfxn__cjkvx - 1))
    else:
        wfb__dfck = context.get_dummy_value()
        apv__ilm = types.none
    ehatb__iue = types.TypeRef(arr_type)
    eztv__ilbe = arr_type(types.int64, ehatb__iue, apv__ilm)
    args = [hzazs__wwi, context.get_dummy_value(), wfb__dfck]
    lcgx__usjz = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        dnyy__yoz, ytqaf__xja = c.pyapi.call_jit_code(lcgx__usjz,
            eztv__ilbe, args)
    else:
        ytqaf__xja = context.compile_internal(builder, lcgx__usjz,
            eztv__ilbe, args)
    return ytqaf__xja


def is_ll_eq(builder, val1, val2):
    znd__rotgu = val1.type.pointee
    xmvi__smkyy = val2.type.pointee
    assert znd__rotgu == xmvi__smkyy, 'invalid llvm value comparison'
    if isinstance(znd__rotgu, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(znd__rotgu.elements) if isinstance(znd__rotgu, lir.
            BaseStructType) else znd__rotgu.count
        mkwgz__imtl = lir.Constant(lir.IntType(1), 1)
        for vseax__pbct in range(n_elems):
            btaq__dyycs = lir.IntType(32)(0)
            xwxqw__csqoe = lir.IntType(32)(vseax__pbct)
            fty__ypk = builder.gep(val1, [btaq__dyycs, xwxqw__csqoe],
                inbounds=True)
            uxm__arew = builder.gep(val2, [btaq__dyycs, xwxqw__csqoe],
                inbounds=True)
            mkwgz__imtl = builder.and_(mkwgz__imtl, is_ll_eq(builder,
                fty__ypk, uxm__arew))
        return mkwgz__imtl
    qpnh__kyz = builder.load(val1)
    gle__krw = builder.load(val2)
    if qpnh__kyz.type in (lir.FloatType(), lir.DoubleType()):
        lddac__xio = 32 if qpnh__kyz.type == lir.FloatType() else 64
        qpnh__kyz = builder.bitcast(qpnh__kyz, lir.IntType(lddac__xio))
        gle__krw = builder.bitcast(gle__krw, lir.IntType(lddac__xio))
    return builder.icmp_unsigned('==', qpnh__kyz, gle__krw)
