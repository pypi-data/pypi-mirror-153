"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(tktxk__zzh, False) for tktxk__zzh in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(tktxk__zzh,
                str) for tktxk__zzh in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(jsab__uzq.dtype for jsab__uzq in self.data),
            self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(tktxk__zzh) for tktxk__zzh in d.keys())
        data = tuple(dtype_to_array_type(jsab__uzq) for jsab__uzq in d.values()
            )
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(tktxk__zzh, False) for tktxk__zzh in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hfv__nuq = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, hfv__nuq)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        hfv__nuq = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, hfv__nuq)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    kql__ctxf = builder.module
    drcul__npmfh = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    izs__lsptc = cgutils.get_or_insert_function(kql__ctxf, drcul__npmfh,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not izs__lsptc.is_declaration:
        return izs__lsptc
    izs__lsptc.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(izs__lsptc.append_basic_block())
    eusf__ogtl = izs__lsptc.args[0]
    wvanh__yve = context.get_value_type(payload_type).as_pointer()
    telj__iyoc = builder.bitcast(eusf__ogtl, wvanh__yve)
    tpwai__tksg = context.make_helper(builder, payload_type, ref=telj__iyoc)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), tpwai__tksg.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        tpwai__tksg.null_bitmap)
    builder.ret_void()
    return izs__lsptc


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    iipwo__yaf = context.get_value_type(payload_type)
    coy__pnxuq = context.get_abi_sizeof(iipwo__yaf)
    fbvx__iijy = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    bbynn__haux = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, coy__pnxuq), fbvx__iijy)
    tvs__cro = context.nrt.meminfo_data(builder, bbynn__haux)
    mzojn__scm = builder.bitcast(tvs__cro, iipwo__yaf.as_pointer())
    tpwai__tksg = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    viqfx__wvku = 0
    for arr_typ in struct_arr_type.data:
        djzk__bub = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        oosap__epq = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(viqfx__wvku, 
            viqfx__wvku + djzk__bub)])
        arr = gen_allocate_array(context, builder, arr_typ, oosap__epq, c)
        arrs.append(arr)
        viqfx__wvku += djzk__bub
    tpwai__tksg.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    wsaby__bsh = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    lzvr__ithu = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [wsaby__bsh])
    null_bitmap_ptr = lzvr__ithu.data
    tpwai__tksg.null_bitmap = lzvr__ithu._getvalue()
    builder.store(tpwai__tksg._getvalue(), mzojn__scm)
    return bbynn__haux, tpwai__tksg.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    quxg__mjf = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        mqrjd__namy = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            mqrjd__namy)
        quxg__mjf.append(arr.data)
    zmk__mnaji = cgutils.pack_array(c.builder, quxg__mjf
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, quxg__mjf)
    htow__idts = cgutils.alloca_once_value(c.builder, zmk__mnaji)
    hhhv__sew = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(tktxk__zzh.dtype)) for tktxk__zzh in data_typ]
    whr__azyp = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, hhhv__sew))
    yuk__hfkz = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, tktxk__zzh) for tktxk__zzh in
        names])
    ecdcr__uerx = cgutils.alloca_once_value(c.builder, yuk__hfkz)
    return htow__idts, whr__azyp, ecdcr__uerx


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    kna__htxe = all(isinstance(jsab__uzq, types.Array) and jsab__uzq.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        jsab__uzq in typ.data)
    if kna__htxe:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        nbnd__unq = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            nbnd__unq, i) for i in range(1, nbnd__unq.type.count)], lir.
            IntType(64))
    bbynn__haux, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if kna__htxe:
        htow__idts, whr__azyp, ecdcr__uerx = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        drcul__npmfh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        izs__lsptc = cgutils.get_or_insert_function(c.builder.module,
            drcul__npmfh, name='struct_array_from_sequence')
        c.builder.call(izs__lsptc, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(htow__idts, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(whr__azyp,
            lir.IntType(8).as_pointer()), c.builder.bitcast(ecdcr__uerx,
            lir.IntType(8).as_pointer()), c.context.get_constant(types.
            bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    plq__uya = c.context.make_helper(c.builder, typ)
    plq__uya.meminfo = bbynn__haux
    ury__pkyi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(plq__uya._getvalue(), is_error=ury__pkyi)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    wix__sytxc = context.insert_const_string(builder.module, 'pandas')
    higw__lcxq = c.pyapi.import_module_noblock(wix__sytxc)
    ljhcs__wkv = c.pyapi.object_getattr_string(higw__lcxq, 'NA')
    with cgutils.for_range(builder, n_structs) as bjxmk__firm:
        wzpon__lxfzi = bjxmk__firm.index
        jiqce__piepr = seq_getitem(builder, context, val, wzpon__lxfzi)
        set_bitmap_bit(builder, null_bitmap_ptr, wzpon__lxfzi, 0)
        for tcbu__fixi in range(len(typ.data)):
            arr_typ = typ.data[tcbu__fixi]
            data_arr = builder.extract_value(data_tup, tcbu__fixi)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            pfzje__wjaz, fyx__xdg = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, wzpon__lxfzi])
        abqi__grs = is_na_value(builder, context, jiqce__piepr, ljhcs__wkv)
        ishfq__unbk = builder.icmp_unsigned('!=', abqi__grs, lir.Constant(
            abqi__grs.type, 1))
        with builder.if_then(ishfq__unbk):
            set_bitmap_bit(builder, null_bitmap_ptr, wzpon__lxfzi, 1)
            for tcbu__fixi in range(len(typ.data)):
                arr_typ = typ.data[tcbu__fixi]
                if is_tuple_array:
                    dkqv__clzsp = c.pyapi.tuple_getitem(jiqce__piepr,
                        tcbu__fixi)
                else:
                    dkqv__clzsp = c.pyapi.dict_getitem_string(jiqce__piepr,
                        typ.names[tcbu__fixi])
                abqi__grs = is_na_value(builder, context, dkqv__clzsp,
                    ljhcs__wkv)
                ishfq__unbk = builder.icmp_unsigned('!=', abqi__grs, lir.
                    Constant(abqi__grs.type, 1))
                with builder.if_then(ishfq__unbk):
                    dkqv__clzsp = to_arr_obj_if_list_obj(c, context,
                        builder, dkqv__clzsp, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        dkqv__clzsp).value
                    data_arr = builder.extract_value(data_tup, tcbu__fixi)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    pfzje__wjaz, fyx__xdg = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, wzpon__lxfzi, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(jiqce__piepr)
    c.pyapi.decref(higw__lcxq)
    c.pyapi.decref(ljhcs__wkv)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    plq__uya = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    tvs__cro = context.nrt.meminfo_data(builder, plq__uya.meminfo)
    mzojn__scm = builder.bitcast(tvs__cro, context.get_value_type(
        payload_type).as_pointer())
    tpwai__tksg = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(mzojn__scm))
    return tpwai__tksg


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    tpwai__tksg = _get_struct_arr_payload(c.context, c.builder, typ, val)
    pfzje__wjaz, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), tpwai__tksg.null_bitmap).data
    kna__htxe = all(isinstance(jsab__uzq, types.Array) and jsab__uzq.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        jsab__uzq in typ.data)
    if kna__htxe:
        htow__idts, whr__azyp, ecdcr__uerx = _get_C_API_ptrs(c, tpwai__tksg
            .data, typ.data, typ.names)
        drcul__npmfh = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        kaui__bdsaq = cgutils.get_or_insert_function(c.builder.module,
            drcul__npmfh, name='np_array_from_struct_array')
        arr = c.builder.call(kaui__bdsaq, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(htow__idts, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            whr__azyp, lir.IntType(8).as_pointer()), c.builder.bitcast(
            ecdcr__uerx, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, tpwai__tksg.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    wix__sytxc = context.insert_const_string(builder.module, 'numpy')
    omh__igi = c.pyapi.import_module_noblock(wix__sytxc)
    taj__aatry = c.pyapi.object_getattr_string(omh__igi, 'object_')
    acnl__ilajj = c.pyapi.long_from_longlong(length)
    jrrjw__yamuw = c.pyapi.call_method(omh__igi, 'ndarray', (acnl__ilajj,
        taj__aatry))
    bbvne__tvyui = c.pyapi.object_getattr_string(omh__igi, 'nan')
    with cgutils.for_range(builder, length) as bjxmk__firm:
        wzpon__lxfzi = bjxmk__firm.index
        pyarray_setitem(builder, context, jrrjw__yamuw, wzpon__lxfzi,
            bbvne__tvyui)
        chsqt__jaj = get_bitmap_bit(builder, null_bitmap_ptr, wzpon__lxfzi)
        yllb__hmyx = builder.icmp_unsigned('!=', chsqt__jaj, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(yllb__hmyx):
            if is_tuple_array:
                jiqce__piepr = c.pyapi.tuple_new(len(typ.data))
            else:
                jiqce__piepr = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(bbvne__tvyui)
                    c.pyapi.tuple_setitem(jiqce__piepr, i, bbvne__tvyui)
                else:
                    c.pyapi.dict_setitem_string(jiqce__piepr, typ.names[i],
                        bbvne__tvyui)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                pfzje__wjaz, xledj__flnsw = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, wzpon__lxfzi])
                with builder.if_then(xledj__flnsw):
                    pfzje__wjaz, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, wzpon__lxfzi])
                    nrco__etdel = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(jiqce__piepr, i, nrco__etdel)
                    else:
                        c.pyapi.dict_setitem_string(jiqce__piepr, typ.names
                            [i], nrco__etdel)
                        c.pyapi.decref(nrco__etdel)
            pyarray_setitem(builder, context, jrrjw__yamuw, wzpon__lxfzi,
                jiqce__piepr)
            c.pyapi.decref(jiqce__piepr)
    c.pyapi.decref(omh__igi)
    c.pyapi.decref(taj__aatry)
    c.pyapi.decref(acnl__ilajj)
    c.pyapi.decref(bbvne__tvyui)
    return jrrjw__yamuw


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    axqu__tnue = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if axqu__tnue == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for tntl__clj in range(axqu__tnue)])
    elif nested_counts_type.count < axqu__tnue:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for tntl__clj in range(
            axqu__tnue - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(jsab__uzq) for jsab__uzq in
            names_typ.types)
    iggn__pmd = tuple(jsab__uzq.instance_type for jsab__uzq in dtypes_typ.types
        )
    struct_arr_type = StructArrayType(iggn__pmd, names)

    def codegen(context, builder, sig, args):
        umie__kcyb, nested_counts, tntl__clj, tntl__clj = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        bbynn__haux, tntl__clj, tntl__clj = construct_struct_array(context,
            builder, struct_arr_type, umie__kcyb, nested_counts)
        plq__uya = context.make_helper(builder, struct_arr_type)
        plq__uya.meminfo = bbynn__haux
        return plq__uya._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(tktxk__zzh, str) for
            tktxk__zzh in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hfv__nuq = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, hfv__nuq)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        hfv__nuq = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, hfv__nuq)


def define_struct_dtor(context, builder, struct_type, payload_type):
    kql__ctxf = builder.module
    drcul__npmfh = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    izs__lsptc = cgutils.get_or_insert_function(kql__ctxf, drcul__npmfh,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not izs__lsptc.is_declaration:
        return izs__lsptc
    izs__lsptc.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(izs__lsptc.append_basic_block())
    eusf__ogtl = izs__lsptc.args[0]
    wvanh__yve = context.get_value_type(payload_type).as_pointer()
    telj__iyoc = builder.bitcast(eusf__ogtl, wvanh__yve)
    tpwai__tksg = context.make_helper(builder, payload_type, ref=telj__iyoc)
    for i in range(len(struct_type.data)):
        xving__xzgx = builder.extract_value(tpwai__tksg.null_bitmap, i)
        yllb__hmyx = builder.icmp_unsigned('==', xving__xzgx, lir.Constant(
            xving__xzgx.type, 1))
        with builder.if_then(yllb__hmyx):
            val = builder.extract_value(tpwai__tksg.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return izs__lsptc


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    tvs__cro = context.nrt.meminfo_data(builder, struct.meminfo)
    mzojn__scm = builder.bitcast(tvs__cro, context.get_value_type(
        payload_type).as_pointer())
    tpwai__tksg = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(mzojn__scm))
    return tpwai__tksg, mzojn__scm


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    wix__sytxc = context.insert_const_string(builder.module, 'pandas')
    higw__lcxq = c.pyapi.import_module_noblock(wix__sytxc)
    ljhcs__wkv = c.pyapi.object_getattr_string(higw__lcxq, 'NA')
    nyhzu__camky = []
    nulls = []
    for i, jsab__uzq in enumerate(typ.data):
        nrco__etdel = c.pyapi.dict_getitem_string(val, typ.names[i])
        lpv__kxm = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        kyu__jbk = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(jsab__uzq)))
        abqi__grs = is_na_value(builder, context, nrco__etdel, ljhcs__wkv)
        yllb__hmyx = builder.icmp_unsigned('!=', abqi__grs, lir.Constant(
            abqi__grs.type, 1))
        with builder.if_then(yllb__hmyx):
            builder.store(context.get_constant(types.uint8, 1), lpv__kxm)
            field_val = c.pyapi.to_native_value(jsab__uzq, nrco__etdel).value
            builder.store(field_val, kyu__jbk)
        nyhzu__camky.append(builder.load(kyu__jbk))
        nulls.append(builder.load(lpv__kxm))
    c.pyapi.decref(higw__lcxq)
    c.pyapi.decref(ljhcs__wkv)
    bbynn__haux = construct_struct(context, builder, typ, nyhzu__camky, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = bbynn__haux
    ury__pkyi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=ury__pkyi)


@box(StructType)
def box_struct(typ, val, c):
    uak__wcnop = c.pyapi.dict_new(len(typ.data))
    tpwai__tksg, tntl__clj = _get_struct_payload(c.context, c.builder, typ, val
        )
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(uak__wcnop, typ.names[i], c.pyapi.
            borrow_none())
        xving__xzgx = c.builder.extract_value(tpwai__tksg.null_bitmap, i)
        yllb__hmyx = c.builder.icmp_unsigned('==', xving__xzgx, lir.
            Constant(xving__xzgx.type, 1))
        with c.builder.if_then(yllb__hmyx):
            jmqeb__rlzyz = c.builder.extract_value(tpwai__tksg.data, i)
            c.context.nrt.incref(c.builder, val_typ, jmqeb__rlzyz)
            dkqv__clzsp = c.pyapi.from_native_value(val_typ, jmqeb__rlzyz,
                c.env_manager)
            c.pyapi.dict_setitem_string(uak__wcnop, typ.names[i], dkqv__clzsp)
            c.pyapi.decref(dkqv__clzsp)
    c.context.nrt.decref(c.builder, typ, val)
    return uak__wcnop


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(jsab__uzq) for jsab__uzq in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, kge__szf = args
        payload_type = StructPayloadType(struct_type.data)
        iipwo__yaf = context.get_value_type(payload_type)
        coy__pnxuq = context.get_abi_sizeof(iipwo__yaf)
        fbvx__iijy = define_struct_dtor(context, builder, struct_type,
            payload_type)
        bbynn__haux = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, coy__pnxuq), fbvx__iijy)
        tvs__cro = context.nrt.meminfo_data(builder, bbynn__haux)
        mzojn__scm = builder.bitcast(tvs__cro, iipwo__yaf.as_pointer())
        tpwai__tksg = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        tpwai__tksg.data = data
        tpwai__tksg.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for tntl__clj in range(len(
            data_typ.types))])
        builder.store(tpwai__tksg._getvalue(), mzojn__scm)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = bbynn__haux
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        tpwai__tksg, tntl__clj = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tpwai__tksg.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        tpwai__tksg, tntl__clj = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tpwai__tksg.null_bitmap)
    idrvr__vdkuy = types.UniTuple(types.int8, len(struct_typ.data))
    return idrvr__vdkuy(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, tntl__clj, val = args
        tpwai__tksg, mzojn__scm = _get_struct_payload(context, builder,
            struct_typ, struct)
        lry__lahnm = tpwai__tksg.data
        tzf__walty = builder.insert_value(lry__lahnm, val, field_ind)
        shw__rfgyw = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, shw__rfgyw, lry__lahnm)
        context.nrt.incref(builder, shw__rfgyw, tzf__walty)
        tpwai__tksg.data = tzf__walty
        builder.store(tpwai__tksg._getvalue(), mzojn__scm)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    pbr__imw = get_overload_const_str(ind)
    if pbr__imw not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            pbr__imw, struct))
    return struct.names.index(pbr__imw)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    iipwo__yaf = context.get_value_type(payload_type)
    coy__pnxuq = context.get_abi_sizeof(iipwo__yaf)
    fbvx__iijy = define_struct_dtor(context, builder, struct_type, payload_type
        )
    bbynn__haux = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, coy__pnxuq), fbvx__iijy)
    tvs__cro = context.nrt.meminfo_data(builder, bbynn__haux)
    mzojn__scm = builder.bitcast(tvs__cro, iipwo__yaf.as_pointer())
    tpwai__tksg = cgutils.create_struct_proxy(payload_type)(context, builder)
    tpwai__tksg.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    tpwai__tksg.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(tpwai__tksg._getvalue(), mzojn__scm)
    return bbynn__haux


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    emx__kauqi = tuple(d.dtype for d in struct_arr_typ.data)
    oclfq__mqoi = StructType(emx__kauqi, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        jkk__rih, ind = args
        tpwai__tksg = _get_struct_arr_payload(context, builder,
            struct_arr_typ, jkk__rih)
        nyhzu__camky = []
        ezpjc__tmux = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            mqrjd__namy = builder.extract_value(tpwai__tksg.data, i)
            jdsto__iok = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                mqrjd__namy, ind])
            ezpjc__tmux.append(jdsto__iok)
            qmv__ohb = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            yllb__hmyx = builder.icmp_unsigned('==', jdsto__iok, lir.
                Constant(jdsto__iok.type, 1))
            with builder.if_then(yllb__hmyx):
                ech__mgxo = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    mqrjd__namy, ind])
                builder.store(ech__mgxo, qmv__ohb)
            nyhzu__camky.append(builder.load(qmv__ohb))
        if isinstance(oclfq__mqoi, types.DictType):
            cvk__cbrfc = [context.insert_const_string(builder.module,
                mwxyl__fwdw) for mwxyl__fwdw in struct_arr_typ.names]
            nulxy__ofwx = cgutils.pack_array(builder, nyhzu__camky)
            yvpnw__zzhm = cgutils.pack_array(builder, cvk__cbrfc)

            def impl(names, vals):
                d = {}
                for i, mwxyl__fwdw in enumerate(names):
                    d[mwxyl__fwdw] = vals[i]
                return d
            gcr__mis = context.compile_internal(builder, impl, oclfq__mqoi(
                types.Tuple(tuple(types.StringLiteral(mwxyl__fwdw) for
                mwxyl__fwdw in struct_arr_typ.names)), types.Tuple(
                emx__kauqi)), [yvpnw__zzhm, nulxy__ofwx])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                emx__kauqi), nulxy__ofwx)
            return gcr__mis
        bbynn__haux = construct_struct(context, builder, oclfq__mqoi,
            nyhzu__camky, ezpjc__tmux)
        struct = context.make_helper(builder, oclfq__mqoi)
        struct.meminfo = bbynn__haux
        return struct._getvalue()
    return oclfq__mqoi(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tpwai__tksg = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tpwai__tksg.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tpwai__tksg = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tpwai__tksg.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(jsab__uzq) for jsab__uzq in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, lzvr__ithu, kge__szf = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        iipwo__yaf = context.get_value_type(payload_type)
        coy__pnxuq = context.get_abi_sizeof(iipwo__yaf)
        fbvx__iijy = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        bbynn__haux = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, coy__pnxuq), fbvx__iijy)
        tvs__cro = context.nrt.meminfo_data(builder, bbynn__haux)
        mzojn__scm = builder.bitcast(tvs__cro, iipwo__yaf.as_pointer())
        tpwai__tksg = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        tpwai__tksg.data = data
        tpwai__tksg.null_bitmap = lzvr__ithu
        builder.store(tpwai__tksg._getvalue(), mzojn__scm)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, lzvr__ithu)
        plq__uya = context.make_helper(builder, struct_arr_type)
        plq__uya.meminfo = bbynn__haux
        return plq__uya._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    knyom__bynl = len(arr.data)
    tsc__qsgcl = 'def impl(arr, ind):\n'
    tsc__qsgcl += '  data = get_data(arr)\n'
    tsc__qsgcl += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        tsc__qsgcl += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        tsc__qsgcl += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        tsc__qsgcl += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    tsc__qsgcl += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(knyom__bynl)), ', '.join("'{}'".format(mwxyl__fwdw) for
        mwxyl__fwdw in arr.names)))
    kxshf__cpc = {}
    exec(tsc__qsgcl, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, kxshf__cpc)
    impl = kxshf__cpc['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        knyom__bynl = len(arr.data)
        tsc__qsgcl = 'def impl(arr, ind, val):\n'
        tsc__qsgcl += '  data = get_data(arr)\n'
        tsc__qsgcl += '  null_bitmap = get_null_bitmap(arr)\n'
        tsc__qsgcl += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(knyom__bynl):
            if isinstance(val, StructType):
                tsc__qsgcl += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                tsc__qsgcl += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                tsc__qsgcl += '  else:\n'
                tsc__qsgcl += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                tsc__qsgcl += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        kxshf__cpc = {}
        exec(tsc__qsgcl, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, kxshf__cpc)
        impl = kxshf__cpc['impl']
        return impl
    if isinstance(ind, types.SliceType):
        knyom__bynl = len(arr.data)
        tsc__qsgcl = 'def impl(arr, ind, val):\n'
        tsc__qsgcl += '  data = get_data(arr)\n'
        tsc__qsgcl += '  null_bitmap = get_null_bitmap(arr)\n'
        tsc__qsgcl += '  val_data = get_data(val)\n'
        tsc__qsgcl += '  val_null_bitmap = get_null_bitmap(val)\n'
        tsc__qsgcl += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(knyom__bynl):
            tsc__qsgcl += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        kxshf__cpc = {}
        exec(tsc__qsgcl, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, kxshf__cpc)
        impl = kxshf__cpc['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    tsc__qsgcl = 'def impl(A):\n'
    tsc__qsgcl += '  total_nbytes = 0\n'
    tsc__qsgcl += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        tsc__qsgcl += f'  total_nbytes += data[{i}].nbytes\n'
    tsc__qsgcl += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    tsc__qsgcl += '  return total_nbytes\n'
    kxshf__cpc = {}
    exec(tsc__qsgcl, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, kxshf__cpc)
    impl = kxshf__cpc['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        lzvr__ithu = get_null_bitmap(A)
        mln__hkpjs = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        jcsb__ogqc = lzvr__ithu.copy()
        return init_struct_arr(mln__hkpjs, jcsb__ogqc, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(tktxk__zzh.copy() for tktxk__zzh in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    tsxmk__slcia = arrs.count
    tsc__qsgcl = 'def f(arrs):\n'
    tsc__qsgcl += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(tsxmk__slcia)))
    kxshf__cpc = {}
    exec(tsc__qsgcl, {}, kxshf__cpc)
    impl = kxshf__cpc['f']
    return impl
