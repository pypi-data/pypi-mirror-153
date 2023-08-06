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
            .utils.is_array_typ(wxx__ism, False) for wxx__ism in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(wxx__ism,
                str) for wxx__ism in names) and len(names) == len(data)
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
        return StructType(tuple(dplom__cfxui.dtype for dplom__cfxui in self
            .data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(wxx__ism) for wxx__ism in d.keys())
        data = tuple(dtype_to_array_type(dplom__cfxui) for dplom__cfxui in
            d.values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(wxx__ism, False) for wxx__ism in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zeon__ssd = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, zeon__ssd)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        zeon__ssd = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, zeon__ssd)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    yka__bqc = builder.module
    qru__dkyry = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    tpz__vnvcz = cgutils.get_or_insert_function(yka__bqc, qru__dkyry, name=
        '.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not tpz__vnvcz.is_declaration:
        return tpz__vnvcz
    tpz__vnvcz.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(tpz__vnvcz.append_basic_block())
    xnfr__eitrk = tpz__vnvcz.args[0]
    rky__zkcuq = context.get_value_type(payload_type).as_pointer()
    wbjho__tcgde = builder.bitcast(xnfr__eitrk, rky__zkcuq)
    ntr__nxdeg = context.make_helper(builder, payload_type, ref=wbjho__tcgde)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), ntr__nxdeg.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        ntr__nxdeg.null_bitmap)
    builder.ret_void()
    return tpz__vnvcz


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    mgk__pflen = context.get_value_type(payload_type)
    jlsok__mgc = context.get_abi_sizeof(mgk__pflen)
    ekf__olqi = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    tuaim__iydp = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jlsok__mgc), ekf__olqi)
    arjra__iygiz = context.nrt.meminfo_data(builder, tuaim__iydp)
    ycdkw__mfcf = builder.bitcast(arjra__iygiz, mgk__pflen.as_pointer())
    ntr__nxdeg = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    yubx__wcvq = 0
    for arr_typ in struct_arr_type.data:
        ktbt__cie = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        trgj__nqxw = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(yubx__wcvq, yubx__wcvq +
            ktbt__cie)])
        arr = gen_allocate_array(context, builder, arr_typ, trgj__nqxw, c)
        arrs.append(arr)
        yubx__wcvq += ktbt__cie
    ntr__nxdeg.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    gwxzd__xzyr = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    tsadz__juaa = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [gwxzd__xzyr])
    null_bitmap_ptr = tsadz__juaa.data
    ntr__nxdeg.null_bitmap = tsadz__juaa._getvalue()
    builder.store(ntr__nxdeg._getvalue(), ycdkw__mfcf)
    return tuaim__iydp, ntr__nxdeg.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    idd__kcttf = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        njtd__ais = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            njtd__ais)
        idd__kcttf.append(arr.data)
    rauj__chqb = cgutils.pack_array(c.builder, idd__kcttf
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, idd__kcttf)
    ujhsn__mgc = cgutils.alloca_once_value(c.builder, rauj__chqb)
    vlpzj__wss = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(wxx__ism.dtype)) for wxx__ism in data_typ]
    ftg__cgzhq = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, vlpzj__wss))
    blbjx__erjk = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, wxx__ism) for wxx__ism in names])
    uos__fjx = cgutils.alloca_once_value(c.builder, blbjx__erjk)
    return ujhsn__mgc, ftg__cgzhq, uos__fjx


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    dhaqc__vlaye = all(isinstance(dplom__cfxui, types.Array) and 
        dplom__cfxui.dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for dplom__cfxui in typ.data)
    if dhaqc__vlaye:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        mgy__vhexo = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            mgy__vhexo, i) for i in range(1, mgy__vhexo.type.count)], lir.
            IntType(64))
    tuaim__iydp, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if dhaqc__vlaye:
        ujhsn__mgc, ftg__cgzhq, uos__fjx = _get_C_API_ptrs(c, data_tup, typ
            .data, typ.names)
        qru__dkyry = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        tpz__vnvcz = cgutils.get_or_insert_function(c.builder.module,
            qru__dkyry, name='struct_array_from_sequence')
        c.builder.call(tpz__vnvcz, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(ujhsn__mgc, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(ftg__cgzhq,
            lir.IntType(8).as_pointer()), c.builder.bitcast(uos__fjx, lir.
            IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    oixb__xuit = c.context.make_helper(c.builder, typ)
    oixb__xuit.meminfo = tuaim__iydp
    lagyj__cwun = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oixb__xuit._getvalue(), is_error=lagyj__cwun)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    bdibe__kxyf = context.insert_const_string(builder.module, 'pandas')
    usq__ufzg = c.pyapi.import_module_noblock(bdibe__kxyf)
    efrrc__hphaw = c.pyapi.object_getattr_string(usq__ufzg, 'NA')
    with cgutils.for_range(builder, n_structs) as dyhcx__iquoj:
        wsvu__cykiw = dyhcx__iquoj.index
        mllix__bwt = seq_getitem(builder, context, val, wsvu__cykiw)
        set_bitmap_bit(builder, null_bitmap_ptr, wsvu__cykiw, 0)
        for uezv__fnn in range(len(typ.data)):
            arr_typ = typ.data[uezv__fnn]
            data_arr = builder.extract_value(data_tup, uezv__fnn)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            bpqz__riru, mvmpn__qzc = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, wsvu__cykiw])
        sjc__koruw = is_na_value(builder, context, mllix__bwt, efrrc__hphaw)
        thai__pli = builder.icmp_unsigned('!=', sjc__koruw, lir.Constant(
            sjc__koruw.type, 1))
        with builder.if_then(thai__pli):
            set_bitmap_bit(builder, null_bitmap_ptr, wsvu__cykiw, 1)
            for uezv__fnn in range(len(typ.data)):
                arr_typ = typ.data[uezv__fnn]
                if is_tuple_array:
                    qyw__uoruz = c.pyapi.tuple_getitem(mllix__bwt, uezv__fnn)
                else:
                    qyw__uoruz = c.pyapi.dict_getitem_string(mllix__bwt,
                        typ.names[uezv__fnn])
                sjc__koruw = is_na_value(builder, context, qyw__uoruz,
                    efrrc__hphaw)
                thai__pli = builder.icmp_unsigned('!=', sjc__koruw, lir.
                    Constant(sjc__koruw.type, 1))
                with builder.if_then(thai__pli):
                    qyw__uoruz = to_arr_obj_if_list_obj(c, context, builder,
                        qyw__uoruz, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        qyw__uoruz).value
                    data_arr = builder.extract_value(data_tup, uezv__fnn)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    bpqz__riru, mvmpn__qzc = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, wsvu__cykiw, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(mllix__bwt)
    c.pyapi.decref(usq__ufzg)
    c.pyapi.decref(efrrc__hphaw)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    oixb__xuit = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    arjra__iygiz = context.nrt.meminfo_data(builder, oixb__xuit.meminfo)
    ycdkw__mfcf = builder.bitcast(arjra__iygiz, context.get_value_type(
        payload_type).as_pointer())
    ntr__nxdeg = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ycdkw__mfcf))
    return ntr__nxdeg


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    ntr__nxdeg = _get_struct_arr_payload(c.context, c.builder, typ, val)
    bpqz__riru, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), ntr__nxdeg.null_bitmap).data
    dhaqc__vlaye = all(isinstance(dplom__cfxui, types.Array) and 
        dplom__cfxui.dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for dplom__cfxui in typ.data)
    if dhaqc__vlaye:
        ujhsn__mgc, ftg__cgzhq, uos__fjx = _get_C_API_ptrs(c, ntr__nxdeg.
            data, typ.data, typ.names)
        qru__dkyry = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        xtwy__yanu = cgutils.get_or_insert_function(c.builder.module,
            qru__dkyry, name='np_array_from_struct_array')
        arr = c.builder.call(xtwy__yanu, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(ujhsn__mgc, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            ftg__cgzhq, lir.IntType(8).as_pointer()), c.builder.bitcast(
            uos__fjx, lir.IntType(8).as_pointer()), c.context.get_constant(
            types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, ntr__nxdeg.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    bdibe__kxyf = context.insert_const_string(builder.module, 'numpy')
    ghl__iwt = c.pyapi.import_module_noblock(bdibe__kxyf)
    vjkvs__qylr = c.pyapi.object_getattr_string(ghl__iwt, 'object_')
    umfju__ppub = c.pyapi.long_from_longlong(length)
    anw__mtkfh = c.pyapi.call_method(ghl__iwt, 'ndarray', (umfju__ppub,
        vjkvs__qylr))
    vyb__byzst = c.pyapi.object_getattr_string(ghl__iwt, 'nan')
    with cgutils.for_range(builder, length) as dyhcx__iquoj:
        wsvu__cykiw = dyhcx__iquoj.index
        pyarray_setitem(builder, context, anw__mtkfh, wsvu__cykiw, vyb__byzst)
        cnumj__dhh = get_bitmap_bit(builder, null_bitmap_ptr, wsvu__cykiw)
        kvbh__oouye = builder.icmp_unsigned('!=', cnumj__dhh, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(kvbh__oouye):
            if is_tuple_array:
                mllix__bwt = c.pyapi.tuple_new(len(typ.data))
            else:
                mllix__bwt = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(vyb__byzst)
                    c.pyapi.tuple_setitem(mllix__bwt, i, vyb__byzst)
                else:
                    c.pyapi.dict_setitem_string(mllix__bwt, typ.names[i],
                        vyb__byzst)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                bpqz__riru, hoch__lpdg = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, wsvu__cykiw])
                with builder.if_then(hoch__lpdg):
                    bpqz__riru, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, wsvu__cykiw])
                    sgzkt__ngq = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(mllix__bwt, i, sgzkt__ngq)
                    else:
                        c.pyapi.dict_setitem_string(mllix__bwt, typ.names[i
                            ], sgzkt__ngq)
                        c.pyapi.decref(sgzkt__ngq)
            pyarray_setitem(builder, context, anw__mtkfh, wsvu__cykiw,
                mllix__bwt)
            c.pyapi.decref(mllix__bwt)
    c.pyapi.decref(ghl__iwt)
    c.pyapi.decref(vjkvs__qylr)
    c.pyapi.decref(umfju__ppub)
    c.pyapi.decref(vyb__byzst)
    return anw__mtkfh


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    wfv__ueh = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if wfv__ueh == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for vmga__xsfx in range(wfv__ueh)])
    elif nested_counts_type.count < wfv__ueh:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for vmga__xsfx in range(
            wfv__ueh - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(dplom__cfxui) for dplom__cfxui in
            names_typ.types)
    fjl__olzfe = tuple(dplom__cfxui.instance_type for dplom__cfxui in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(fjl__olzfe, names)

    def codegen(context, builder, sig, args):
        yvf__osfsa, nested_counts, vmga__xsfx, vmga__xsfx = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        tuaim__iydp, vmga__xsfx, vmga__xsfx = construct_struct_array(context,
            builder, struct_arr_type, yvf__osfsa, nested_counts)
        oixb__xuit = context.make_helper(builder, struct_arr_type)
        oixb__xuit.meminfo = tuaim__iydp
        return oixb__xuit._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(wxx__ism, str) for
            wxx__ism in names) and len(names) == len(data)
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
        zeon__ssd = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, zeon__ssd)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        zeon__ssd = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, zeon__ssd)


def define_struct_dtor(context, builder, struct_type, payload_type):
    yka__bqc = builder.module
    qru__dkyry = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    tpz__vnvcz = cgutils.get_or_insert_function(yka__bqc, qru__dkyry, name=
        '.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not tpz__vnvcz.is_declaration:
        return tpz__vnvcz
    tpz__vnvcz.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(tpz__vnvcz.append_basic_block())
    xnfr__eitrk = tpz__vnvcz.args[0]
    rky__zkcuq = context.get_value_type(payload_type).as_pointer()
    wbjho__tcgde = builder.bitcast(xnfr__eitrk, rky__zkcuq)
    ntr__nxdeg = context.make_helper(builder, payload_type, ref=wbjho__tcgde)
    for i in range(len(struct_type.data)):
        qry__ccrpl = builder.extract_value(ntr__nxdeg.null_bitmap, i)
        kvbh__oouye = builder.icmp_unsigned('==', qry__ccrpl, lir.Constant(
            qry__ccrpl.type, 1))
        with builder.if_then(kvbh__oouye):
            val = builder.extract_value(ntr__nxdeg.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return tpz__vnvcz


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    arjra__iygiz = context.nrt.meminfo_data(builder, struct.meminfo)
    ycdkw__mfcf = builder.bitcast(arjra__iygiz, context.get_value_type(
        payload_type).as_pointer())
    ntr__nxdeg = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ycdkw__mfcf))
    return ntr__nxdeg, ycdkw__mfcf


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    bdibe__kxyf = context.insert_const_string(builder.module, 'pandas')
    usq__ufzg = c.pyapi.import_module_noblock(bdibe__kxyf)
    efrrc__hphaw = c.pyapi.object_getattr_string(usq__ufzg, 'NA')
    ntz__qkap = []
    nulls = []
    for i, dplom__cfxui in enumerate(typ.data):
        sgzkt__ngq = c.pyapi.dict_getitem_string(val, typ.names[i])
        tcpcu__zhsje = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        ejdus__jog = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(dplom__cfxui)))
        sjc__koruw = is_na_value(builder, context, sgzkt__ngq, efrrc__hphaw)
        kvbh__oouye = builder.icmp_unsigned('!=', sjc__koruw, lir.Constant(
            sjc__koruw.type, 1))
        with builder.if_then(kvbh__oouye):
            builder.store(context.get_constant(types.uint8, 1), tcpcu__zhsje)
            field_val = c.pyapi.to_native_value(dplom__cfxui, sgzkt__ngq).value
            builder.store(field_val, ejdus__jog)
        ntz__qkap.append(builder.load(ejdus__jog))
        nulls.append(builder.load(tcpcu__zhsje))
    c.pyapi.decref(usq__ufzg)
    c.pyapi.decref(efrrc__hphaw)
    tuaim__iydp = construct_struct(context, builder, typ, ntz__qkap, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = tuaim__iydp
    lagyj__cwun = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=lagyj__cwun)


@box(StructType)
def box_struct(typ, val, c):
    zgsh__brio = c.pyapi.dict_new(len(typ.data))
    ntr__nxdeg, vmga__xsfx = _get_struct_payload(c.context, c.builder, typ, val
        )
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(zgsh__brio, typ.names[i], c.pyapi.
            borrow_none())
        qry__ccrpl = c.builder.extract_value(ntr__nxdeg.null_bitmap, i)
        kvbh__oouye = c.builder.icmp_unsigned('==', qry__ccrpl, lir.
            Constant(qry__ccrpl.type, 1))
        with c.builder.if_then(kvbh__oouye):
            ffrsp__hexe = c.builder.extract_value(ntr__nxdeg.data, i)
            c.context.nrt.incref(c.builder, val_typ, ffrsp__hexe)
            qyw__uoruz = c.pyapi.from_native_value(val_typ, ffrsp__hexe, c.
                env_manager)
            c.pyapi.dict_setitem_string(zgsh__brio, typ.names[i], qyw__uoruz)
            c.pyapi.decref(qyw__uoruz)
    c.context.nrt.decref(c.builder, typ, val)
    return zgsh__brio


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(dplom__cfxui) for dplom__cfxui in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, ulku__rdqgt = args
        payload_type = StructPayloadType(struct_type.data)
        mgk__pflen = context.get_value_type(payload_type)
        jlsok__mgc = context.get_abi_sizeof(mgk__pflen)
        ekf__olqi = define_struct_dtor(context, builder, struct_type,
            payload_type)
        tuaim__iydp = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jlsok__mgc), ekf__olqi)
        arjra__iygiz = context.nrt.meminfo_data(builder, tuaim__iydp)
        ycdkw__mfcf = builder.bitcast(arjra__iygiz, mgk__pflen.as_pointer())
        ntr__nxdeg = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        ntr__nxdeg.data = data
        ntr__nxdeg.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for vmga__xsfx in range(len(
            data_typ.types))])
        builder.store(ntr__nxdeg._getvalue(), ycdkw__mfcf)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = tuaim__iydp
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        ntr__nxdeg, vmga__xsfx = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ntr__nxdeg.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        ntr__nxdeg, vmga__xsfx = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ntr__nxdeg.null_bitmap)
    ypr__esxch = types.UniTuple(types.int8, len(struct_typ.data))
    return ypr__esxch(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, vmga__xsfx, val = args
        ntr__nxdeg, ycdkw__mfcf = _get_struct_payload(context, builder,
            struct_typ, struct)
        vqaa__jdtfy = ntr__nxdeg.data
        rwft__iirco = builder.insert_value(vqaa__jdtfy, val, field_ind)
        bvbdw__frw = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, bvbdw__frw, vqaa__jdtfy)
        context.nrt.incref(builder, bvbdw__frw, rwft__iirco)
        ntr__nxdeg.data = rwft__iirco
        builder.store(ntr__nxdeg._getvalue(), ycdkw__mfcf)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    yqm__xeidk = get_overload_const_str(ind)
    if yqm__xeidk not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            yqm__xeidk, struct))
    return struct.names.index(yqm__xeidk)


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
    mgk__pflen = context.get_value_type(payload_type)
    jlsok__mgc = context.get_abi_sizeof(mgk__pflen)
    ekf__olqi = define_struct_dtor(context, builder, struct_type, payload_type)
    tuaim__iydp = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jlsok__mgc), ekf__olqi)
    arjra__iygiz = context.nrt.meminfo_data(builder, tuaim__iydp)
    ycdkw__mfcf = builder.bitcast(arjra__iygiz, mgk__pflen.as_pointer())
    ntr__nxdeg = cgutils.create_struct_proxy(payload_type)(context, builder)
    ntr__nxdeg.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    ntr__nxdeg.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(ntr__nxdeg._getvalue(), ycdkw__mfcf)
    return tuaim__iydp


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    hwj__hjl = tuple(d.dtype for d in struct_arr_typ.data)
    kjuwk__ank = StructType(hwj__hjl, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        fqj__hbzxi, ind = args
        ntr__nxdeg = _get_struct_arr_payload(context, builder,
            struct_arr_typ, fqj__hbzxi)
        ntz__qkap = []
        mpql__uyvzu = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            njtd__ais = builder.extract_value(ntr__nxdeg.data, i)
            wsbt__iybxd = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [njtd__ais,
                ind])
            mpql__uyvzu.append(wsbt__iybxd)
            res__jay = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            kvbh__oouye = builder.icmp_unsigned('==', wsbt__iybxd, lir.
                Constant(wsbt__iybxd.type, 1))
            with builder.if_then(kvbh__oouye):
                tyl__oqbrz = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    njtd__ais, ind])
                builder.store(tyl__oqbrz, res__jay)
            ntz__qkap.append(builder.load(res__jay))
        if isinstance(kjuwk__ank, types.DictType):
            pli__fkjaq = [context.insert_const_string(builder.module,
                nmo__rokl) for nmo__rokl in struct_arr_typ.names]
            gjib__shlhy = cgutils.pack_array(builder, ntz__qkap)
            qzpn__ytody = cgutils.pack_array(builder, pli__fkjaq)

            def impl(names, vals):
                d = {}
                for i, nmo__rokl in enumerate(names):
                    d[nmo__rokl] = vals[i]
                return d
            xevr__yszul = context.compile_internal(builder, impl,
                kjuwk__ank(types.Tuple(tuple(types.StringLiteral(nmo__rokl) for
                nmo__rokl in struct_arr_typ.names)), types.Tuple(hwj__hjl)),
                [qzpn__ytody, gjib__shlhy])
            context.nrt.decref(builder, types.BaseTuple.from_types(hwj__hjl
                ), gjib__shlhy)
            return xevr__yszul
        tuaim__iydp = construct_struct(context, builder, kjuwk__ank,
            ntz__qkap, mpql__uyvzu)
        struct = context.make_helper(builder, kjuwk__ank)
        struct.meminfo = tuaim__iydp
        return struct._getvalue()
    return kjuwk__ank(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ntr__nxdeg = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ntr__nxdeg.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ntr__nxdeg = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ntr__nxdeg.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(dplom__cfxui) for dplom__cfxui in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, tsadz__juaa, ulku__rdqgt = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        mgk__pflen = context.get_value_type(payload_type)
        jlsok__mgc = context.get_abi_sizeof(mgk__pflen)
        ekf__olqi = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        tuaim__iydp = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jlsok__mgc), ekf__olqi)
        arjra__iygiz = context.nrt.meminfo_data(builder, tuaim__iydp)
        ycdkw__mfcf = builder.bitcast(arjra__iygiz, mgk__pflen.as_pointer())
        ntr__nxdeg = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        ntr__nxdeg.data = data
        ntr__nxdeg.null_bitmap = tsadz__juaa
        builder.store(ntr__nxdeg._getvalue(), ycdkw__mfcf)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, tsadz__juaa)
        oixb__xuit = context.make_helper(builder, struct_arr_type)
        oixb__xuit.meminfo = tuaim__iydp
        return oixb__xuit._getvalue()
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
    hfp__cskt = len(arr.data)
    ezifu__carvi = 'def impl(arr, ind):\n'
    ezifu__carvi += '  data = get_data(arr)\n'
    ezifu__carvi += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        ezifu__carvi += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        ezifu__carvi += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        ezifu__carvi += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    ezifu__carvi += (
        '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.format(
        ', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for i in
        range(hfp__cskt)), ', '.join("'{}'".format(nmo__rokl) for nmo__rokl in
        arr.names)))
    gbau__hnl = {}
    exec(ezifu__carvi, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, gbau__hnl)
    impl = gbau__hnl['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        hfp__cskt = len(arr.data)
        ezifu__carvi = 'def impl(arr, ind, val):\n'
        ezifu__carvi += '  data = get_data(arr)\n'
        ezifu__carvi += '  null_bitmap = get_null_bitmap(arr)\n'
        ezifu__carvi += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(hfp__cskt):
            if isinstance(val, StructType):
                ezifu__carvi += ("  if is_field_value_null(val, '{}'):\n".
                    format(arr.names[i]))
                ezifu__carvi += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                ezifu__carvi += '  else:\n'
                ezifu__carvi += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                ezifu__carvi += "  data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
        gbau__hnl = {}
        exec(ezifu__carvi, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, gbau__hnl)
        impl = gbau__hnl['impl']
        return impl
    if isinstance(ind, types.SliceType):
        hfp__cskt = len(arr.data)
        ezifu__carvi = 'def impl(arr, ind, val):\n'
        ezifu__carvi += '  data = get_data(arr)\n'
        ezifu__carvi += '  null_bitmap = get_null_bitmap(arr)\n'
        ezifu__carvi += '  val_data = get_data(val)\n'
        ezifu__carvi += '  val_null_bitmap = get_null_bitmap(val)\n'
        ezifu__carvi += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(hfp__cskt):
            ezifu__carvi += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        gbau__hnl = {}
        exec(ezifu__carvi, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, gbau__hnl)
        impl = gbau__hnl['impl']
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
    ezifu__carvi = 'def impl(A):\n'
    ezifu__carvi += '  total_nbytes = 0\n'
    ezifu__carvi += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        ezifu__carvi += f'  total_nbytes += data[{i}].nbytes\n'
    ezifu__carvi += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    ezifu__carvi += '  return total_nbytes\n'
    gbau__hnl = {}
    exec(ezifu__carvi, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, gbau__hnl)
    impl = gbau__hnl['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        tsadz__juaa = get_null_bitmap(A)
        xyl__ptc = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        sgol__vxxtl = tsadz__juaa.copy()
        return init_struct_arr(xyl__ptc, sgol__vxxtl, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(wxx__ism.copy() for wxx__ism in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    tfg__hnvlt = arrs.count
    ezifu__carvi = 'def f(arrs):\n'
    ezifu__carvi += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(tfg__hnvlt)))
    gbau__hnl = {}
    exec(ezifu__carvi, {}, gbau__hnl)
    impl = gbau__hnl['f']
    return impl
