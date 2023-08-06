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
            .utils.is_array_typ(fqrj__pjma, False) for fqrj__pjma in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(fqrj__pjma,
                str) for fqrj__pjma in names) and len(names) == len(data)
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
        return StructType(tuple(lhjbh__qzdm.dtype for lhjbh__qzdm in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(fqrj__pjma) for fqrj__pjma in d.keys())
        data = tuple(dtype_to_array_type(lhjbh__qzdm) for lhjbh__qzdm in d.
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
            is_array_typ(fqrj__pjma, False) for fqrj__pjma in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lvoz__jfyap = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, lvoz__jfyap)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        lvoz__jfyap = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, lvoz__jfyap)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    dzcut__enoow = builder.module
    cuo__zvab = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    qkpvs__hpejj = cgutils.get_or_insert_function(dzcut__enoow, cuo__zvab,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not qkpvs__hpejj.is_declaration:
        return qkpvs__hpejj
    qkpvs__hpejj.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(qkpvs__hpejj.append_basic_block())
    csad__wwfs = qkpvs__hpejj.args[0]
    qpbwm__tuyvh = context.get_value_type(payload_type).as_pointer()
    xwmjm__mni = builder.bitcast(csad__wwfs, qpbwm__tuyvh)
    tgh__mkqfr = context.make_helper(builder, payload_type, ref=xwmjm__mni)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), tgh__mkqfr.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        tgh__mkqfr.null_bitmap)
    builder.ret_void()
    return qkpvs__hpejj


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    yquui__aiv = context.get_value_type(payload_type)
    iropi__cvwzz = context.get_abi_sizeof(yquui__aiv)
    okrm__pjlc = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    rjwrd__wxci = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, iropi__cvwzz), okrm__pjlc)
    mdnf__rocgc = context.nrt.meminfo_data(builder, rjwrd__wxci)
    ygbl__alth = builder.bitcast(mdnf__rocgc, yquui__aiv.as_pointer())
    tgh__mkqfr = cgutils.create_struct_proxy(payload_type)(context, builder)
    xpwde__omcis = []
    jgemc__klgp = 0
    for arr_typ in struct_arr_type.data:
        pefxy__cdm = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        jlxb__lhms = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(jgemc__klgp, 
            jgemc__klgp + pefxy__cdm)])
        arr = gen_allocate_array(context, builder, arr_typ, jlxb__lhms, c)
        xpwde__omcis.append(arr)
        jgemc__klgp += pefxy__cdm
    tgh__mkqfr.data = cgutils.pack_array(builder, xpwde__omcis
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, xpwde__omcis)
    kmv__xval = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    mfo__jktwv = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [kmv__xval])
    null_bitmap_ptr = mfo__jktwv.data
    tgh__mkqfr.null_bitmap = mfo__jktwv._getvalue()
    builder.store(tgh__mkqfr._getvalue(), ygbl__alth)
    return rjwrd__wxci, tgh__mkqfr.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    lifzn__wwxwm = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        jjd__etqh = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            jjd__etqh)
        lifzn__wwxwm.append(arr.data)
    mop__xyn = cgutils.pack_array(c.builder, lifzn__wwxwm
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, lifzn__wwxwm)
    xcmw__faj = cgutils.alloca_once_value(c.builder, mop__xyn)
    ymdy__uvsz = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(fqrj__pjma.dtype)) for fqrj__pjma in data_typ]
    fgaex__yyr = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, ymdy__uvsz))
    zogh__slj = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, fqrj__pjma) for fqrj__pjma in
        names])
    jpkwe__rktqz = cgutils.alloca_once_value(c.builder, zogh__slj)
    return xcmw__faj, fgaex__yyr, jpkwe__rktqz


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    gccbe__jtwa = all(isinstance(lhjbh__qzdm, types.Array) and lhjbh__qzdm.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for lhjbh__qzdm in typ.data)
    if gccbe__jtwa:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        ghopd__uylx = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ghopd__uylx, i) for i in range(1, ghopd__uylx.type.count)], lir
            .IntType(64))
    rjwrd__wxci, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if gccbe__jtwa:
        xcmw__faj, fgaex__yyr, jpkwe__rktqz = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        cuo__zvab = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        qkpvs__hpejj = cgutils.get_or_insert_function(c.builder.module,
            cuo__zvab, name='struct_array_from_sequence')
        c.builder.call(qkpvs__hpejj, [val, c.context.get_constant(types.
            int32, len(typ.data)), c.builder.bitcast(xcmw__faj, lir.IntType
            (8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            fgaex__yyr, lir.IntType(8).as_pointer()), c.builder.bitcast(
            jpkwe__rktqz, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    wgwi__yyxrb = c.context.make_helper(c.builder, typ)
    wgwi__yyxrb.meminfo = rjwrd__wxci
    lzgo__gjgr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wgwi__yyxrb._getvalue(), is_error=lzgo__gjgr)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    ebcm__llesu = context.insert_const_string(builder.module, 'pandas')
    gepd__yqxpl = c.pyapi.import_module_noblock(ebcm__llesu)
    ybb__ptpk = c.pyapi.object_getattr_string(gepd__yqxpl, 'NA')
    with cgutils.for_range(builder, n_structs) as aoh__jovv:
        xgzy__mjuf = aoh__jovv.index
        xme__rrkv = seq_getitem(builder, context, val, xgzy__mjuf)
        set_bitmap_bit(builder, null_bitmap_ptr, xgzy__mjuf, 0)
        for buzm__udz in range(len(typ.data)):
            arr_typ = typ.data[buzm__udz]
            data_arr = builder.extract_value(data_tup, buzm__udz)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            xyfg__hhx, wkvg__ogkfr = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, xgzy__mjuf])
        tav__irdb = is_na_value(builder, context, xme__rrkv, ybb__ptpk)
        qxemy__hxr = builder.icmp_unsigned('!=', tav__irdb, lir.Constant(
            tav__irdb.type, 1))
        with builder.if_then(qxemy__hxr):
            set_bitmap_bit(builder, null_bitmap_ptr, xgzy__mjuf, 1)
            for buzm__udz in range(len(typ.data)):
                arr_typ = typ.data[buzm__udz]
                if is_tuple_array:
                    tefi__hqpih = c.pyapi.tuple_getitem(xme__rrkv, buzm__udz)
                else:
                    tefi__hqpih = c.pyapi.dict_getitem_string(xme__rrkv,
                        typ.names[buzm__udz])
                tav__irdb = is_na_value(builder, context, tefi__hqpih,
                    ybb__ptpk)
                qxemy__hxr = builder.icmp_unsigned('!=', tav__irdb, lir.
                    Constant(tav__irdb.type, 1))
                with builder.if_then(qxemy__hxr):
                    tefi__hqpih = to_arr_obj_if_list_obj(c, context,
                        builder, tefi__hqpih, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        tefi__hqpih).value
                    data_arr = builder.extract_value(data_tup, buzm__udz)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    xyfg__hhx, wkvg__ogkfr = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, xgzy__mjuf, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(xme__rrkv)
    c.pyapi.decref(gepd__yqxpl)
    c.pyapi.decref(ybb__ptpk)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    wgwi__yyxrb = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    mdnf__rocgc = context.nrt.meminfo_data(builder, wgwi__yyxrb.meminfo)
    ygbl__alth = builder.bitcast(mdnf__rocgc, context.get_value_type(
        payload_type).as_pointer())
    tgh__mkqfr = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ygbl__alth))
    return tgh__mkqfr


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    tgh__mkqfr = _get_struct_arr_payload(c.context, c.builder, typ, val)
    xyfg__hhx, length = c.pyapi.call_jit_code(lambda A: len(A), types.int64
        (typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), tgh__mkqfr.null_bitmap).data
    gccbe__jtwa = all(isinstance(lhjbh__qzdm, types.Array) and lhjbh__qzdm.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for lhjbh__qzdm in typ.data)
    if gccbe__jtwa:
        xcmw__faj, fgaex__yyr, jpkwe__rktqz = _get_C_API_ptrs(c, tgh__mkqfr
            .data, typ.data, typ.names)
        cuo__zvab = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        cxtft__bga = cgutils.get_or_insert_function(c.builder.module,
            cuo__zvab, name='np_array_from_struct_array')
        arr = c.builder.call(cxtft__bga, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(xcmw__faj, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            fgaex__yyr, lir.IntType(8).as_pointer()), c.builder.bitcast(
            jpkwe__rktqz, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, tgh__mkqfr.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    ebcm__llesu = context.insert_const_string(builder.module, 'numpy')
    wqwz__kabo = c.pyapi.import_module_noblock(ebcm__llesu)
    wgbk__ytnqw = c.pyapi.object_getattr_string(wqwz__kabo, 'object_')
    gltn__btq = c.pyapi.long_from_longlong(length)
    aro__ttjpo = c.pyapi.call_method(wqwz__kabo, 'ndarray', (gltn__btq,
        wgbk__ytnqw))
    mynrd__grpv = c.pyapi.object_getattr_string(wqwz__kabo, 'nan')
    with cgutils.for_range(builder, length) as aoh__jovv:
        xgzy__mjuf = aoh__jovv.index
        pyarray_setitem(builder, context, aro__ttjpo, xgzy__mjuf, mynrd__grpv)
        cen__hfkf = get_bitmap_bit(builder, null_bitmap_ptr, xgzy__mjuf)
        hhvtf__ygdv = builder.icmp_unsigned('!=', cen__hfkf, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(hhvtf__ygdv):
            if is_tuple_array:
                xme__rrkv = c.pyapi.tuple_new(len(typ.data))
            else:
                xme__rrkv = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(mynrd__grpv)
                    c.pyapi.tuple_setitem(xme__rrkv, i, mynrd__grpv)
                else:
                    c.pyapi.dict_setitem_string(xme__rrkv, typ.names[i],
                        mynrd__grpv)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                xyfg__hhx, xuf__izdp = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, xgzy__mjuf])
                with builder.if_then(xuf__izdp):
                    xyfg__hhx, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, xgzy__mjuf])
                    vzxdd__ecsb = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(xme__rrkv, i, vzxdd__ecsb)
                    else:
                        c.pyapi.dict_setitem_string(xme__rrkv, typ.names[i],
                            vzxdd__ecsb)
                        c.pyapi.decref(vzxdd__ecsb)
            pyarray_setitem(builder, context, aro__ttjpo, xgzy__mjuf, xme__rrkv
                )
            c.pyapi.decref(xme__rrkv)
    c.pyapi.decref(wqwz__kabo)
    c.pyapi.decref(wgbk__ytnqw)
    c.pyapi.decref(gltn__btq)
    c.pyapi.decref(mynrd__grpv)
    return aro__ttjpo


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    lywf__tpu = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if lywf__tpu == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for mxd__tmdwg in range(lywf__tpu)])
    elif nested_counts_type.count < lywf__tpu:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for mxd__tmdwg in range(
            lywf__tpu - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(lhjbh__qzdm) for lhjbh__qzdm in
            names_typ.types)
    jlvxl__tnuw = tuple(lhjbh__qzdm.instance_type for lhjbh__qzdm in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(jlvxl__tnuw, names)

    def codegen(context, builder, sig, args):
        zvh__rsze, nested_counts, mxd__tmdwg, mxd__tmdwg = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        rjwrd__wxci, mxd__tmdwg, mxd__tmdwg = construct_struct_array(context,
            builder, struct_arr_type, zvh__rsze, nested_counts)
        wgwi__yyxrb = context.make_helper(builder, struct_arr_type)
        wgwi__yyxrb.meminfo = rjwrd__wxci
        return wgwi__yyxrb._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(fqrj__pjma, str) for
            fqrj__pjma in names) and len(names) == len(data)
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
        lvoz__jfyap = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, lvoz__jfyap)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        lvoz__jfyap = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, lvoz__jfyap)


def define_struct_dtor(context, builder, struct_type, payload_type):
    dzcut__enoow = builder.module
    cuo__zvab = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    qkpvs__hpejj = cgutils.get_or_insert_function(dzcut__enoow, cuo__zvab,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not qkpvs__hpejj.is_declaration:
        return qkpvs__hpejj
    qkpvs__hpejj.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(qkpvs__hpejj.append_basic_block())
    csad__wwfs = qkpvs__hpejj.args[0]
    qpbwm__tuyvh = context.get_value_type(payload_type).as_pointer()
    xwmjm__mni = builder.bitcast(csad__wwfs, qpbwm__tuyvh)
    tgh__mkqfr = context.make_helper(builder, payload_type, ref=xwmjm__mni)
    for i in range(len(struct_type.data)):
        iro__gwazw = builder.extract_value(tgh__mkqfr.null_bitmap, i)
        hhvtf__ygdv = builder.icmp_unsigned('==', iro__gwazw, lir.Constant(
            iro__gwazw.type, 1))
        with builder.if_then(hhvtf__ygdv):
            val = builder.extract_value(tgh__mkqfr.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return qkpvs__hpejj


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    mdnf__rocgc = context.nrt.meminfo_data(builder, struct.meminfo)
    ygbl__alth = builder.bitcast(mdnf__rocgc, context.get_value_type(
        payload_type).as_pointer())
    tgh__mkqfr = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ygbl__alth))
    return tgh__mkqfr, ygbl__alth


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    ebcm__llesu = context.insert_const_string(builder.module, 'pandas')
    gepd__yqxpl = c.pyapi.import_module_noblock(ebcm__llesu)
    ybb__ptpk = c.pyapi.object_getattr_string(gepd__yqxpl, 'NA')
    lsyzx__xbnoa = []
    nulls = []
    for i, lhjbh__qzdm in enumerate(typ.data):
        vzxdd__ecsb = c.pyapi.dict_getitem_string(val, typ.names[i])
        ikm__ucki = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        cwy__yxmrf = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(lhjbh__qzdm)))
        tav__irdb = is_na_value(builder, context, vzxdd__ecsb, ybb__ptpk)
        hhvtf__ygdv = builder.icmp_unsigned('!=', tav__irdb, lir.Constant(
            tav__irdb.type, 1))
        with builder.if_then(hhvtf__ygdv):
            builder.store(context.get_constant(types.uint8, 1), ikm__ucki)
            field_val = c.pyapi.to_native_value(lhjbh__qzdm, vzxdd__ecsb).value
            builder.store(field_val, cwy__yxmrf)
        lsyzx__xbnoa.append(builder.load(cwy__yxmrf))
        nulls.append(builder.load(ikm__ucki))
    c.pyapi.decref(gepd__yqxpl)
    c.pyapi.decref(ybb__ptpk)
    rjwrd__wxci = construct_struct(context, builder, typ, lsyzx__xbnoa, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = rjwrd__wxci
    lzgo__gjgr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=lzgo__gjgr)


@box(StructType)
def box_struct(typ, val, c):
    ndeh__szg = c.pyapi.dict_new(len(typ.data))
    tgh__mkqfr, mxd__tmdwg = _get_struct_payload(c.context, c.builder, typ, val
        )
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(ndeh__szg, typ.names[i], c.pyapi.
            borrow_none())
        iro__gwazw = c.builder.extract_value(tgh__mkqfr.null_bitmap, i)
        hhvtf__ygdv = c.builder.icmp_unsigned('==', iro__gwazw, lir.
            Constant(iro__gwazw.type, 1))
        with c.builder.if_then(hhvtf__ygdv):
            hgn__prpat = c.builder.extract_value(tgh__mkqfr.data, i)
            c.context.nrt.incref(c.builder, val_typ, hgn__prpat)
            tefi__hqpih = c.pyapi.from_native_value(val_typ, hgn__prpat, c.
                env_manager)
            c.pyapi.dict_setitem_string(ndeh__szg, typ.names[i], tefi__hqpih)
            c.pyapi.decref(tefi__hqpih)
    c.context.nrt.decref(c.builder, typ, val)
    return ndeh__szg


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(lhjbh__qzdm) for lhjbh__qzdm in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, avcq__tobui = args
        payload_type = StructPayloadType(struct_type.data)
        yquui__aiv = context.get_value_type(payload_type)
        iropi__cvwzz = context.get_abi_sizeof(yquui__aiv)
        okrm__pjlc = define_struct_dtor(context, builder, struct_type,
            payload_type)
        rjwrd__wxci = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, iropi__cvwzz), okrm__pjlc)
        mdnf__rocgc = context.nrt.meminfo_data(builder, rjwrd__wxci)
        ygbl__alth = builder.bitcast(mdnf__rocgc, yquui__aiv.as_pointer())
        tgh__mkqfr = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        tgh__mkqfr.data = data
        tgh__mkqfr.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for mxd__tmdwg in range(len(
            data_typ.types))])
        builder.store(tgh__mkqfr._getvalue(), ygbl__alth)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = rjwrd__wxci
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        tgh__mkqfr, mxd__tmdwg = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tgh__mkqfr.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        tgh__mkqfr, mxd__tmdwg = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tgh__mkqfr.null_bitmap)
    llw__wyywd = types.UniTuple(types.int8, len(struct_typ.data))
    return llw__wyywd(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, mxd__tmdwg, val = args
        tgh__mkqfr, ygbl__alth = _get_struct_payload(context, builder,
            struct_typ, struct)
        txh__ech = tgh__mkqfr.data
        hmpg__nqh = builder.insert_value(txh__ech, val, field_ind)
        jpai__ydc = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, jpai__ydc, txh__ech)
        context.nrt.incref(builder, jpai__ydc, hmpg__nqh)
        tgh__mkqfr.data = hmpg__nqh
        builder.store(tgh__mkqfr._getvalue(), ygbl__alth)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    nlx__cmx = get_overload_const_str(ind)
    if nlx__cmx not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            nlx__cmx, struct))
    return struct.names.index(nlx__cmx)


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
    yquui__aiv = context.get_value_type(payload_type)
    iropi__cvwzz = context.get_abi_sizeof(yquui__aiv)
    okrm__pjlc = define_struct_dtor(context, builder, struct_type, payload_type
        )
    rjwrd__wxci = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, iropi__cvwzz), okrm__pjlc)
    mdnf__rocgc = context.nrt.meminfo_data(builder, rjwrd__wxci)
    ygbl__alth = builder.bitcast(mdnf__rocgc, yquui__aiv.as_pointer())
    tgh__mkqfr = cgutils.create_struct_proxy(payload_type)(context, builder)
    tgh__mkqfr.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    tgh__mkqfr.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(tgh__mkqfr._getvalue(), ygbl__alth)
    return rjwrd__wxci


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    jglc__vvad = tuple(d.dtype for d in struct_arr_typ.data)
    zqc__qkmx = StructType(jglc__vvad, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        hyyg__wjs, ind = args
        tgh__mkqfr = _get_struct_arr_payload(context, builder,
            struct_arr_typ, hyyg__wjs)
        lsyzx__xbnoa = []
        nehy__whmxx = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            jjd__etqh = builder.extract_value(tgh__mkqfr.data, i)
            ersm__auha = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [jjd__etqh,
                ind])
            nehy__whmxx.append(ersm__auha)
            gac__zfqhe = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            hhvtf__ygdv = builder.icmp_unsigned('==', ersm__auha, lir.
                Constant(ersm__auha.type, 1))
            with builder.if_then(hhvtf__ygdv):
                vmkhv__zlvw = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    jjd__etqh, ind])
                builder.store(vmkhv__zlvw, gac__zfqhe)
            lsyzx__xbnoa.append(builder.load(gac__zfqhe))
        if isinstance(zqc__qkmx, types.DictType):
            dgihk__nbea = [context.insert_const_string(builder.module,
                uvtvc__voqfi) for uvtvc__voqfi in struct_arr_typ.names]
            azc__qtvf = cgutils.pack_array(builder, lsyzx__xbnoa)
            exg__cgnws = cgutils.pack_array(builder, dgihk__nbea)

            def impl(names, vals):
                d = {}
                for i, uvtvc__voqfi in enumerate(names):
                    d[uvtvc__voqfi] = vals[i]
                return d
            htyi__jzz = context.compile_internal(builder, impl, zqc__qkmx(
                types.Tuple(tuple(types.StringLiteral(uvtvc__voqfi) for
                uvtvc__voqfi in struct_arr_typ.names)), types.Tuple(
                jglc__vvad)), [exg__cgnws, azc__qtvf])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                jglc__vvad), azc__qtvf)
            return htyi__jzz
        rjwrd__wxci = construct_struct(context, builder, zqc__qkmx,
            lsyzx__xbnoa, nehy__whmxx)
        struct = context.make_helper(builder, zqc__qkmx)
        struct.meminfo = rjwrd__wxci
        return struct._getvalue()
    return zqc__qkmx(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tgh__mkqfr = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tgh__mkqfr.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tgh__mkqfr = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tgh__mkqfr.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(lhjbh__qzdm) for lhjbh__qzdm in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, mfo__jktwv, avcq__tobui = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        yquui__aiv = context.get_value_type(payload_type)
        iropi__cvwzz = context.get_abi_sizeof(yquui__aiv)
        okrm__pjlc = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        rjwrd__wxci = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, iropi__cvwzz), okrm__pjlc)
        mdnf__rocgc = context.nrt.meminfo_data(builder, rjwrd__wxci)
        ygbl__alth = builder.bitcast(mdnf__rocgc, yquui__aiv.as_pointer())
        tgh__mkqfr = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        tgh__mkqfr.data = data
        tgh__mkqfr.null_bitmap = mfo__jktwv
        builder.store(tgh__mkqfr._getvalue(), ygbl__alth)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, mfo__jktwv)
        wgwi__yyxrb = context.make_helper(builder, struct_arr_type)
        wgwi__yyxrb.meminfo = rjwrd__wxci
        return wgwi__yyxrb._getvalue()
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
    ahhio__cwm = len(arr.data)
    asc__qsg = 'def impl(arr, ind):\n'
    asc__qsg += '  data = get_data(arr)\n'
    asc__qsg += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        asc__qsg += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        asc__qsg += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        asc__qsg += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    asc__qsg += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(ahhio__cwm)), ', '.join("'{}'".format(uvtvc__voqfi) for
        uvtvc__voqfi in arr.names)))
    etcm__tiy = {}
    exec(asc__qsg, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, etcm__tiy)
    impl = etcm__tiy['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        ahhio__cwm = len(arr.data)
        asc__qsg = 'def impl(arr, ind, val):\n'
        asc__qsg += '  data = get_data(arr)\n'
        asc__qsg += '  null_bitmap = get_null_bitmap(arr)\n'
        asc__qsg += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(ahhio__cwm):
            if isinstance(val, StructType):
                asc__qsg += "  if is_field_value_null(val, '{}'):\n".format(arr
                    .names[i])
                asc__qsg += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                asc__qsg += '  else:\n'
                asc__qsg += "    data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
            else:
                asc__qsg += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        etcm__tiy = {}
        exec(asc__qsg, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, etcm__tiy)
        impl = etcm__tiy['impl']
        return impl
    if isinstance(ind, types.SliceType):
        ahhio__cwm = len(arr.data)
        asc__qsg = 'def impl(arr, ind, val):\n'
        asc__qsg += '  data = get_data(arr)\n'
        asc__qsg += '  null_bitmap = get_null_bitmap(arr)\n'
        asc__qsg += '  val_data = get_data(val)\n'
        asc__qsg += '  val_null_bitmap = get_null_bitmap(val)\n'
        asc__qsg += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(ahhio__cwm):
            asc__qsg += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        etcm__tiy = {}
        exec(asc__qsg, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, etcm__tiy)
        impl = etcm__tiy['impl']
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
    asc__qsg = 'def impl(A):\n'
    asc__qsg += '  total_nbytes = 0\n'
    asc__qsg += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        asc__qsg += f'  total_nbytes += data[{i}].nbytes\n'
    asc__qsg += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    asc__qsg += '  return total_nbytes\n'
    etcm__tiy = {}
    exec(asc__qsg, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, etcm__tiy)
    impl = etcm__tiy['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        mfo__jktwv = get_null_bitmap(A)
        zlp__agqz = bodo.ir.join.copy_arr_tup(data)
        rqkv__abnj = mfo__jktwv.copy()
        return init_struct_arr(zlp__agqz, rqkv__abnj, names)
    return copy_impl
