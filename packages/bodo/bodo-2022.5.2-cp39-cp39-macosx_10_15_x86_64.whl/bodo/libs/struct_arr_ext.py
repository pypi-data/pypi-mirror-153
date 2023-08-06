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
            .utils.is_array_typ(wpk__jbetm, False) for wpk__jbetm in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(wpk__jbetm,
                str) for wpk__jbetm in names) and len(names) == len(data)
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
        return StructType(tuple(pxqc__sxofh.dtype for pxqc__sxofh in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(wpk__jbetm) for wpk__jbetm in d.keys())
        data = tuple(dtype_to_array_type(pxqc__sxofh) for pxqc__sxofh in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(wpk__jbetm, False) for wpk__jbetm in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vgesi__pkvp = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, vgesi__pkvp)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        vgesi__pkvp = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, vgesi__pkvp)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    lio__eggcy = builder.module
    zbfw__acy = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    gnr__nzwa = cgutils.get_or_insert_function(lio__eggcy, zbfw__acy, name=
        '.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not gnr__nzwa.is_declaration:
        return gnr__nzwa
    gnr__nzwa.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(gnr__nzwa.append_basic_block())
    abl__zqpl = gnr__nzwa.args[0]
    kez__hnu = context.get_value_type(payload_type).as_pointer()
    ntvtb__rjoy = builder.bitcast(abl__zqpl, kez__hnu)
    uoshr__krgpd = context.make_helper(builder, payload_type, ref=ntvtb__rjoy)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), uoshr__krgpd.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        uoshr__krgpd.null_bitmap)
    builder.ret_void()
    return gnr__nzwa


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    imm__bmum = context.get_value_type(payload_type)
    wjc__txq = context.get_abi_sizeof(imm__bmum)
    eifuw__yupfs = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    favu__hxvqt = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, wjc__txq), eifuw__yupfs)
    vlc__ntkt = context.nrt.meminfo_data(builder, favu__hxvqt)
    poal__jipr = builder.bitcast(vlc__ntkt, imm__bmum.as_pointer())
    uoshr__krgpd = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    vfda__eltl = 0
    for arr_typ in struct_arr_type.data:
        aafs__zwrl = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        ejtx__bok = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(vfda__eltl, vfda__eltl +
            aafs__zwrl)])
        arr = gen_allocate_array(context, builder, arr_typ, ejtx__bok, c)
        arrs.append(arr)
        vfda__eltl += aafs__zwrl
    uoshr__krgpd.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    airni__jfyk = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    grz__qen = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [airni__jfyk])
    null_bitmap_ptr = grz__qen.data
    uoshr__krgpd.null_bitmap = grz__qen._getvalue()
    builder.store(uoshr__krgpd._getvalue(), poal__jipr)
    return favu__hxvqt, uoshr__krgpd.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    kyzbs__qdf = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        sela__eomwl = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            sela__eomwl)
        kyzbs__qdf.append(arr.data)
    nvovl__agtd = cgutils.pack_array(c.builder, kyzbs__qdf
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, kyzbs__qdf)
    jct__mgji = cgutils.alloca_once_value(c.builder, nvovl__agtd)
    thhli__uxuk = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(wpk__jbetm.dtype)) for wpk__jbetm in data_typ]
    joz__hctby = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, thhli__uxuk))
    lobl__ajulh = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, wpk__jbetm) for wpk__jbetm in
        names])
    hvr__snkb = cgutils.alloca_once_value(c.builder, lobl__ajulh)
    return jct__mgji, joz__hctby, hvr__snkb


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    hqxj__uzof = all(isinstance(pxqc__sxofh, types.Array) and pxqc__sxofh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for pxqc__sxofh in typ.data)
    if hqxj__uzof:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        huapp__hpa = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            huapp__hpa, i) for i in range(1, huapp__hpa.type.count)], lir.
            IntType(64))
    favu__hxvqt, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if hqxj__uzof:
        jct__mgji, joz__hctby, hvr__snkb = _get_C_API_ptrs(c, data_tup, typ
            .data, typ.names)
        zbfw__acy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        gnr__nzwa = cgutils.get_or_insert_function(c.builder.module,
            zbfw__acy, name='struct_array_from_sequence')
        c.builder.call(gnr__nzwa, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(jct__mgji, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(joz__hctby,
            lir.IntType(8).as_pointer()), c.builder.bitcast(hvr__snkb, lir.
            IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    ihuf__ibucs = c.context.make_helper(c.builder, typ)
    ihuf__ibucs.meminfo = favu__hxvqt
    peu__qkzb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ihuf__ibucs._getvalue(), is_error=peu__qkzb)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    cgocj__vxqvq = context.insert_const_string(builder.module, 'pandas')
    goup__tntok = c.pyapi.import_module_noblock(cgocj__vxqvq)
    skch__yci = c.pyapi.object_getattr_string(goup__tntok, 'NA')
    with cgutils.for_range(builder, n_structs) as awl__rqc:
        tuatb__hnn = awl__rqc.index
        qrw__uweq = seq_getitem(builder, context, val, tuatb__hnn)
        set_bitmap_bit(builder, null_bitmap_ptr, tuatb__hnn, 0)
        for uaou__hnfd in range(len(typ.data)):
            arr_typ = typ.data[uaou__hnfd]
            data_arr = builder.extract_value(data_tup, uaou__hnfd)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            fcjn__kzxxo, gim__bwgd = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, tuatb__hnn])
        tif__dcu = is_na_value(builder, context, qrw__uweq, skch__yci)
        gths__jumb = builder.icmp_unsigned('!=', tif__dcu, lir.Constant(
            tif__dcu.type, 1))
        with builder.if_then(gths__jumb):
            set_bitmap_bit(builder, null_bitmap_ptr, tuatb__hnn, 1)
            for uaou__hnfd in range(len(typ.data)):
                arr_typ = typ.data[uaou__hnfd]
                if is_tuple_array:
                    ody__ckutv = c.pyapi.tuple_getitem(qrw__uweq, uaou__hnfd)
                else:
                    ody__ckutv = c.pyapi.dict_getitem_string(qrw__uweq, typ
                        .names[uaou__hnfd])
                tif__dcu = is_na_value(builder, context, ody__ckutv, skch__yci)
                gths__jumb = builder.icmp_unsigned('!=', tif__dcu, lir.
                    Constant(tif__dcu.type, 1))
                with builder.if_then(gths__jumb):
                    ody__ckutv = to_arr_obj_if_list_obj(c, context, builder,
                        ody__ckutv, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        ody__ckutv).value
                    data_arr = builder.extract_value(data_tup, uaou__hnfd)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    fcjn__kzxxo, gim__bwgd = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, tuatb__hnn, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(qrw__uweq)
    c.pyapi.decref(goup__tntok)
    c.pyapi.decref(skch__yci)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    ihuf__ibucs = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    vlc__ntkt = context.nrt.meminfo_data(builder, ihuf__ibucs.meminfo)
    poal__jipr = builder.bitcast(vlc__ntkt, context.get_value_type(
        payload_type).as_pointer())
    uoshr__krgpd = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(poal__jipr))
    return uoshr__krgpd


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    uoshr__krgpd = _get_struct_arr_payload(c.context, c.builder, typ, val)
    fcjn__kzxxo, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), uoshr__krgpd.null_bitmap).data
    hqxj__uzof = all(isinstance(pxqc__sxofh, types.Array) and pxqc__sxofh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for pxqc__sxofh in typ.data)
    if hqxj__uzof:
        jct__mgji, joz__hctby, hvr__snkb = _get_C_API_ptrs(c, uoshr__krgpd.
            data, typ.data, typ.names)
        zbfw__acy = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        kllj__kbnor = cgutils.get_or_insert_function(c.builder.module,
            zbfw__acy, name='np_array_from_struct_array')
        arr = c.builder.call(kllj__kbnor, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(jct__mgji, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            joz__hctby, lir.IntType(8).as_pointer()), c.builder.bitcast(
            hvr__snkb, lir.IntType(8).as_pointer()), c.context.get_constant
            (types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, uoshr__krgpd.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    cgocj__vxqvq = context.insert_const_string(builder.module, 'numpy')
    nreip__wbgdh = c.pyapi.import_module_noblock(cgocj__vxqvq)
    mrme__douoe = c.pyapi.object_getattr_string(nreip__wbgdh, 'object_')
    fvj__atbfd = c.pyapi.long_from_longlong(length)
    bfi__srah = c.pyapi.call_method(nreip__wbgdh, 'ndarray', (fvj__atbfd,
        mrme__douoe))
    dyziu__vtq = c.pyapi.object_getattr_string(nreip__wbgdh, 'nan')
    with cgutils.for_range(builder, length) as awl__rqc:
        tuatb__hnn = awl__rqc.index
        pyarray_setitem(builder, context, bfi__srah, tuatb__hnn, dyziu__vtq)
        czc__tia = get_bitmap_bit(builder, null_bitmap_ptr, tuatb__hnn)
        ffajo__toqq = builder.icmp_unsigned('!=', czc__tia, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(ffajo__toqq):
            if is_tuple_array:
                qrw__uweq = c.pyapi.tuple_new(len(typ.data))
            else:
                qrw__uweq = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(dyziu__vtq)
                    c.pyapi.tuple_setitem(qrw__uweq, i, dyziu__vtq)
                else:
                    c.pyapi.dict_setitem_string(qrw__uweq, typ.names[i],
                        dyziu__vtq)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                fcjn__kzxxo, wfjxo__nxc = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, tuatb__hnn])
                with builder.if_then(wfjxo__nxc):
                    fcjn__kzxxo, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, tuatb__hnn])
                    ljh__suskl = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(qrw__uweq, i, ljh__suskl)
                    else:
                        c.pyapi.dict_setitem_string(qrw__uweq, typ.names[i],
                            ljh__suskl)
                        c.pyapi.decref(ljh__suskl)
            pyarray_setitem(builder, context, bfi__srah, tuatb__hnn, qrw__uweq)
            c.pyapi.decref(qrw__uweq)
    c.pyapi.decref(nreip__wbgdh)
    c.pyapi.decref(mrme__douoe)
    c.pyapi.decref(fvj__atbfd)
    c.pyapi.decref(dyziu__vtq)
    return bfi__srah


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    swgz__qog = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if swgz__qog == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for ytndo__cooy in range(swgz__qog)])
    elif nested_counts_type.count < swgz__qog:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for ytndo__cooy in range(
            swgz__qog - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(pxqc__sxofh) for pxqc__sxofh in
            names_typ.types)
    xty__qxpfm = tuple(pxqc__sxofh.instance_type for pxqc__sxofh in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(xty__qxpfm, names)

    def codegen(context, builder, sig, args):
        drcqt__woim, nested_counts, ytndo__cooy, ytndo__cooy = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        favu__hxvqt, ytndo__cooy, ytndo__cooy = construct_struct_array(context,
            builder, struct_arr_type, drcqt__woim, nested_counts)
        ihuf__ibucs = context.make_helper(builder, struct_arr_type)
        ihuf__ibucs.meminfo = favu__hxvqt
        return ihuf__ibucs._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(wpk__jbetm, str) for
            wpk__jbetm in names) and len(names) == len(data)
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
        vgesi__pkvp = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, vgesi__pkvp)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        vgesi__pkvp = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, vgesi__pkvp)


def define_struct_dtor(context, builder, struct_type, payload_type):
    lio__eggcy = builder.module
    zbfw__acy = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    gnr__nzwa = cgutils.get_or_insert_function(lio__eggcy, zbfw__acy, name=
        '.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not gnr__nzwa.is_declaration:
        return gnr__nzwa
    gnr__nzwa.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(gnr__nzwa.append_basic_block())
    abl__zqpl = gnr__nzwa.args[0]
    kez__hnu = context.get_value_type(payload_type).as_pointer()
    ntvtb__rjoy = builder.bitcast(abl__zqpl, kez__hnu)
    uoshr__krgpd = context.make_helper(builder, payload_type, ref=ntvtb__rjoy)
    for i in range(len(struct_type.data)):
        gstjw__qcq = builder.extract_value(uoshr__krgpd.null_bitmap, i)
        ffajo__toqq = builder.icmp_unsigned('==', gstjw__qcq, lir.Constant(
            gstjw__qcq.type, 1))
        with builder.if_then(ffajo__toqq):
            val = builder.extract_value(uoshr__krgpd.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return gnr__nzwa


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    vlc__ntkt = context.nrt.meminfo_data(builder, struct.meminfo)
    poal__jipr = builder.bitcast(vlc__ntkt, context.get_value_type(
        payload_type).as_pointer())
    uoshr__krgpd = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(poal__jipr))
    return uoshr__krgpd, poal__jipr


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    cgocj__vxqvq = context.insert_const_string(builder.module, 'pandas')
    goup__tntok = c.pyapi.import_module_noblock(cgocj__vxqvq)
    skch__yci = c.pyapi.object_getattr_string(goup__tntok, 'NA')
    kab__okgxw = []
    nulls = []
    for i, pxqc__sxofh in enumerate(typ.data):
        ljh__suskl = c.pyapi.dict_getitem_string(val, typ.names[i])
        fbnzc__ibu = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        dyoz__dvo = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(pxqc__sxofh)))
        tif__dcu = is_na_value(builder, context, ljh__suskl, skch__yci)
        ffajo__toqq = builder.icmp_unsigned('!=', tif__dcu, lir.Constant(
            tif__dcu.type, 1))
        with builder.if_then(ffajo__toqq):
            builder.store(context.get_constant(types.uint8, 1), fbnzc__ibu)
            field_val = c.pyapi.to_native_value(pxqc__sxofh, ljh__suskl).value
            builder.store(field_val, dyoz__dvo)
        kab__okgxw.append(builder.load(dyoz__dvo))
        nulls.append(builder.load(fbnzc__ibu))
    c.pyapi.decref(goup__tntok)
    c.pyapi.decref(skch__yci)
    favu__hxvqt = construct_struct(context, builder, typ, kab__okgxw, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = favu__hxvqt
    peu__qkzb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=peu__qkzb)


@box(StructType)
def box_struct(typ, val, c):
    cir__cegc = c.pyapi.dict_new(len(typ.data))
    uoshr__krgpd, ytndo__cooy = _get_struct_payload(c.context, c.builder,
        typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(cir__cegc, typ.names[i], c.pyapi.
            borrow_none())
        gstjw__qcq = c.builder.extract_value(uoshr__krgpd.null_bitmap, i)
        ffajo__toqq = c.builder.icmp_unsigned('==', gstjw__qcq, lir.
            Constant(gstjw__qcq.type, 1))
        with c.builder.if_then(ffajo__toqq):
            pathf__kygyy = c.builder.extract_value(uoshr__krgpd.data, i)
            c.context.nrt.incref(c.builder, val_typ, pathf__kygyy)
            ody__ckutv = c.pyapi.from_native_value(val_typ, pathf__kygyy, c
                .env_manager)
            c.pyapi.dict_setitem_string(cir__cegc, typ.names[i], ody__ckutv)
            c.pyapi.decref(ody__ckutv)
    c.context.nrt.decref(c.builder, typ, val)
    return cir__cegc


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(pxqc__sxofh) for pxqc__sxofh in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, rvy__nji = args
        payload_type = StructPayloadType(struct_type.data)
        imm__bmum = context.get_value_type(payload_type)
        wjc__txq = context.get_abi_sizeof(imm__bmum)
        eifuw__yupfs = define_struct_dtor(context, builder, struct_type,
            payload_type)
        favu__hxvqt = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, wjc__txq), eifuw__yupfs)
        vlc__ntkt = context.nrt.meminfo_data(builder, favu__hxvqt)
        poal__jipr = builder.bitcast(vlc__ntkt, imm__bmum.as_pointer())
        uoshr__krgpd = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        uoshr__krgpd.data = data
        uoshr__krgpd.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for ytndo__cooy in range(len(
            data_typ.types))])
        builder.store(uoshr__krgpd._getvalue(), poal__jipr)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = favu__hxvqt
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        uoshr__krgpd, ytndo__cooy = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            uoshr__krgpd.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        uoshr__krgpd, ytndo__cooy = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            uoshr__krgpd.null_bitmap)
    wxdpt__kahyj = types.UniTuple(types.int8, len(struct_typ.data))
    return wxdpt__kahyj(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, ytndo__cooy, val = args
        uoshr__krgpd, poal__jipr = _get_struct_payload(context, builder,
            struct_typ, struct)
        lizp__tegd = uoshr__krgpd.data
        ectjy__qnsw = builder.insert_value(lizp__tegd, val, field_ind)
        wmtt__rml = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, wmtt__rml, lizp__tegd)
        context.nrt.incref(builder, wmtt__rml, ectjy__qnsw)
        uoshr__krgpd.data = ectjy__qnsw
        builder.store(uoshr__krgpd._getvalue(), poal__jipr)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    yydl__fdqb = get_overload_const_str(ind)
    if yydl__fdqb not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            yydl__fdqb, struct))
    return struct.names.index(yydl__fdqb)


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
    imm__bmum = context.get_value_type(payload_type)
    wjc__txq = context.get_abi_sizeof(imm__bmum)
    eifuw__yupfs = define_struct_dtor(context, builder, struct_type,
        payload_type)
    favu__hxvqt = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, wjc__txq), eifuw__yupfs)
    vlc__ntkt = context.nrt.meminfo_data(builder, favu__hxvqt)
    poal__jipr = builder.bitcast(vlc__ntkt, imm__bmum.as_pointer())
    uoshr__krgpd = cgutils.create_struct_proxy(payload_type)(context, builder)
    uoshr__krgpd.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    uoshr__krgpd.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(uoshr__krgpd._getvalue(), poal__jipr)
    return favu__hxvqt


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    wktlg__jsu = tuple(d.dtype for d in struct_arr_typ.data)
    fuvo__wqzxl = StructType(wktlg__jsu, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        qhjt__dayy, ind = args
        uoshr__krgpd = _get_struct_arr_payload(context, builder,
            struct_arr_typ, qhjt__dayy)
        kab__okgxw = []
        iim__jrzej = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            sela__eomwl = builder.extract_value(uoshr__krgpd.data, i)
            icurz__vxz = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                sela__eomwl, ind])
            iim__jrzej.append(icurz__vxz)
            evfu__nxcdk = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            ffajo__toqq = builder.icmp_unsigned('==', icurz__vxz, lir.
                Constant(icurz__vxz.type, 1))
            with builder.if_then(ffajo__toqq):
                twkdm__bbxxx = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    sela__eomwl, ind])
                builder.store(twkdm__bbxxx, evfu__nxcdk)
            kab__okgxw.append(builder.load(evfu__nxcdk))
        if isinstance(fuvo__wqzxl, types.DictType):
            zaf__ebbah = [context.insert_const_string(builder.module,
                gkj__yhji) for gkj__yhji in struct_arr_typ.names]
            cyx__mjiwc = cgutils.pack_array(builder, kab__okgxw)
            bhmuq__tnth = cgutils.pack_array(builder, zaf__ebbah)

            def impl(names, vals):
                d = {}
                for i, gkj__yhji in enumerate(names):
                    d[gkj__yhji] = vals[i]
                return d
            zrhuf__hbvn = context.compile_internal(builder, impl,
                fuvo__wqzxl(types.Tuple(tuple(types.StringLiteral(gkj__yhji
                ) for gkj__yhji in struct_arr_typ.names)), types.Tuple(
                wktlg__jsu)), [bhmuq__tnth, cyx__mjiwc])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                wktlg__jsu), cyx__mjiwc)
            return zrhuf__hbvn
        favu__hxvqt = construct_struct(context, builder, fuvo__wqzxl,
            kab__okgxw, iim__jrzej)
        struct = context.make_helper(builder, fuvo__wqzxl)
        struct.meminfo = favu__hxvqt
        return struct._getvalue()
    return fuvo__wqzxl(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        uoshr__krgpd = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            uoshr__krgpd.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        uoshr__krgpd = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            uoshr__krgpd.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(pxqc__sxofh) for pxqc__sxofh in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, grz__qen, rvy__nji = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        imm__bmum = context.get_value_type(payload_type)
        wjc__txq = context.get_abi_sizeof(imm__bmum)
        eifuw__yupfs = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        favu__hxvqt = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, wjc__txq), eifuw__yupfs)
        vlc__ntkt = context.nrt.meminfo_data(builder, favu__hxvqt)
        poal__jipr = builder.bitcast(vlc__ntkt, imm__bmum.as_pointer())
        uoshr__krgpd = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        uoshr__krgpd.data = data
        uoshr__krgpd.null_bitmap = grz__qen
        builder.store(uoshr__krgpd._getvalue(), poal__jipr)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, grz__qen)
        ihuf__ibucs = context.make_helper(builder, struct_arr_type)
        ihuf__ibucs.meminfo = favu__hxvqt
        return ihuf__ibucs._getvalue()
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
    ytn__efmk = len(arr.data)
    oecti__wlk = 'def impl(arr, ind):\n'
    oecti__wlk += '  data = get_data(arr)\n'
    oecti__wlk += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        oecti__wlk += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        oecti__wlk += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        oecti__wlk += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    oecti__wlk += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(ytn__efmk)), ', '.join("'{}'".format(gkj__yhji) for
        gkj__yhji in arr.names)))
    fyzk__daxly = {}
    exec(oecti__wlk, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, fyzk__daxly)
    impl = fyzk__daxly['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        ytn__efmk = len(arr.data)
        oecti__wlk = 'def impl(arr, ind, val):\n'
        oecti__wlk += '  data = get_data(arr)\n'
        oecti__wlk += '  null_bitmap = get_null_bitmap(arr)\n'
        oecti__wlk += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(ytn__efmk):
            if isinstance(val, StructType):
                oecti__wlk += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                oecti__wlk += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                oecti__wlk += '  else:\n'
                oecti__wlk += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                oecti__wlk += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        fyzk__daxly = {}
        exec(oecti__wlk, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, fyzk__daxly)
        impl = fyzk__daxly['impl']
        return impl
    if isinstance(ind, types.SliceType):
        ytn__efmk = len(arr.data)
        oecti__wlk = 'def impl(arr, ind, val):\n'
        oecti__wlk += '  data = get_data(arr)\n'
        oecti__wlk += '  null_bitmap = get_null_bitmap(arr)\n'
        oecti__wlk += '  val_data = get_data(val)\n'
        oecti__wlk += '  val_null_bitmap = get_null_bitmap(val)\n'
        oecti__wlk += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(ytn__efmk):
            oecti__wlk += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        fyzk__daxly = {}
        exec(oecti__wlk, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, fyzk__daxly)
        impl = fyzk__daxly['impl']
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
    oecti__wlk = 'def impl(A):\n'
    oecti__wlk += '  total_nbytes = 0\n'
    oecti__wlk += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        oecti__wlk += f'  total_nbytes += data[{i}].nbytes\n'
    oecti__wlk += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    oecti__wlk += '  return total_nbytes\n'
    fyzk__daxly = {}
    exec(oecti__wlk, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, fyzk__daxly)
    impl = fyzk__daxly['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        grz__qen = get_null_bitmap(A)
        llgdn__okyn = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        gec__wwb = grz__qen.copy()
        return init_struct_arr(llgdn__okyn, gec__wwb, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(wpk__jbetm.copy() for wpk__jbetm in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    egnu__avhq = arrs.count
    oecti__wlk = 'def f(arrs):\n'
    oecti__wlk += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(egnu__avhq)))
    fyzk__daxly = {}
    exec(oecti__wlk, {}, fyzk__daxly)
    impl = fyzk__daxly['f']
    return impl
