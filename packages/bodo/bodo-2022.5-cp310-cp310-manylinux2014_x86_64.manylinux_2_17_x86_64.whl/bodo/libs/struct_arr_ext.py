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
            .utils.is_array_typ(xpjq__bfe, False) for xpjq__bfe in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(xpjq__bfe,
                str) for xpjq__bfe in names) and len(names) == len(data)
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
        return StructType(tuple(egcz__rfmh.dtype for egcz__rfmh in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(xpjq__bfe) for xpjq__bfe in d.keys())
        data = tuple(dtype_to_array_type(egcz__rfmh) for egcz__rfmh in d.
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
            is_array_typ(xpjq__bfe, False) for xpjq__bfe in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ynjsb__axba = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ynjsb__axba)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        ynjsb__axba = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ynjsb__axba)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    shyxn__lum = builder.module
    oru__tqpc = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ankb__lwqt = cgutils.get_or_insert_function(shyxn__lum, oru__tqpc, name
        ='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not ankb__lwqt.is_declaration:
        return ankb__lwqt
    ankb__lwqt.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ankb__lwqt.append_basic_block())
    kol__eaosw = ankb__lwqt.args[0]
    auf__fnxuy = context.get_value_type(payload_type).as_pointer()
    vmjck__zhfm = builder.bitcast(kol__eaosw, auf__fnxuy)
    vgym__hcobk = context.make_helper(builder, payload_type, ref=vmjck__zhfm)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), vgym__hcobk.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        vgym__hcobk.null_bitmap)
    builder.ret_void()
    return ankb__lwqt


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    ebl__zpea = context.get_value_type(payload_type)
    jrsmv__fymqj = context.get_abi_sizeof(ebl__zpea)
    wofhq__laj = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    ghy__alhj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jrsmv__fymqj), wofhq__laj)
    qxhhk__wllt = context.nrt.meminfo_data(builder, ghy__alhj)
    xfqk__ttlrh = builder.bitcast(qxhhk__wllt, ebl__zpea.as_pointer())
    vgym__hcobk = cgutils.create_struct_proxy(payload_type)(context, builder)
    lmmp__tbgai = []
    bjeb__vzmx = 0
    for arr_typ in struct_arr_type.data:
        jfrap__mmoke = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype
            )
        eryx__kibcv = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(bjeb__vzmx, bjeb__vzmx +
            jfrap__mmoke)])
        arr = gen_allocate_array(context, builder, arr_typ, eryx__kibcv, c)
        lmmp__tbgai.append(arr)
        bjeb__vzmx += jfrap__mmoke
    vgym__hcobk.data = cgutils.pack_array(builder, lmmp__tbgai
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, lmmp__tbgai)
    bpda__ulij = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    zpcnp__hija = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [bpda__ulij])
    null_bitmap_ptr = zpcnp__hija.data
    vgym__hcobk.null_bitmap = zpcnp__hija._getvalue()
    builder.store(vgym__hcobk._getvalue(), xfqk__ttlrh)
    return ghy__alhj, vgym__hcobk.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    bzp__oauw = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        ghm__scza = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            ghm__scza)
        bzp__oauw.append(arr.data)
    lzjca__ggl = cgutils.pack_array(c.builder, bzp__oauw
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, bzp__oauw)
    klvv__hggro = cgutils.alloca_once_value(c.builder, lzjca__ggl)
    qvo__xfck = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(xpjq__bfe.dtype)) for xpjq__bfe in data_typ]
    qxc__mhqj = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, qvo__xfck))
    qrlri__awob = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, xpjq__bfe) for xpjq__bfe in
        names])
    ngwc__rce = cgutils.alloca_once_value(c.builder, qrlri__awob)
    return klvv__hggro, qxc__mhqj, ngwc__rce


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    uzsh__lre = all(isinstance(egcz__rfmh, types.Array) and egcz__rfmh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for egcz__rfmh in typ.data)
    if uzsh__lre:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        hrvoe__tgif = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            hrvoe__tgif, i) for i in range(1, hrvoe__tgif.type.count)], lir
            .IntType(64))
    ghy__alhj, data_tup, null_bitmap_ptr = construct_struct_array(c.context,
        c.builder, typ, n_structs, n_elems, c)
    if uzsh__lre:
        klvv__hggro, qxc__mhqj, ngwc__rce = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        oru__tqpc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        ankb__lwqt = cgutils.get_or_insert_function(c.builder.module,
            oru__tqpc, name='struct_array_from_sequence')
        c.builder.call(ankb__lwqt, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(klvv__hggro, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(qxc__mhqj,
            lir.IntType(8).as_pointer()), c.builder.bitcast(ngwc__rce, lir.
            IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    oogrp__xvco = c.context.make_helper(c.builder, typ)
    oogrp__xvco.meminfo = ghy__alhj
    jvn__ausi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oogrp__xvco._getvalue(), is_error=jvn__ausi)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    pfir__fghw = context.insert_const_string(builder.module, 'pandas')
    iora__xhva = c.pyapi.import_module_noblock(pfir__fghw)
    iuwou__zfgqy = c.pyapi.object_getattr_string(iora__xhva, 'NA')
    with cgutils.for_range(builder, n_structs) as zvsm__xsz:
        img__bvmol = zvsm__xsz.index
        hoztv__kwwx = seq_getitem(builder, context, val, img__bvmol)
        set_bitmap_bit(builder, null_bitmap_ptr, img__bvmol, 0)
        for ppp__fkxga in range(len(typ.data)):
            arr_typ = typ.data[ppp__fkxga]
            data_arr = builder.extract_value(data_tup, ppp__fkxga)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            ipxs__ackhd, lxxfh__hkrvx = c.pyapi.call_jit_code(set_na, sig,
                [data_arr, img__bvmol])
        ytiu__tgt = is_na_value(builder, context, hoztv__kwwx, iuwou__zfgqy)
        jocfs__gnfkd = builder.icmp_unsigned('!=', ytiu__tgt, lir.Constant(
            ytiu__tgt.type, 1))
        with builder.if_then(jocfs__gnfkd):
            set_bitmap_bit(builder, null_bitmap_ptr, img__bvmol, 1)
            for ppp__fkxga in range(len(typ.data)):
                arr_typ = typ.data[ppp__fkxga]
                if is_tuple_array:
                    itex__hoqyk = c.pyapi.tuple_getitem(hoztv__kwwx, ppp__fkxga
                        )
                else:
                    itex__hoqyk = c.pyapi.dict_getitem_string(hoztv__kwwx,
                        typ.names[ppp__fkxga])
                ytiu__tgt = is_na_value(builder, context, itex__hoqyk,
                    iuwou__zfgqy)
                jocfs__gnfkd = builder.icmp_unsigned('!=', ytiu__tgt, lir.
                    Constant(ytiu__tgt.type, 1))
                with builder.if_then(jocfs__gnfkd):
                    itex__hoqyk = to_arr_obj_if_list_obj(c, context,
                        builder, itex__hoqyk, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        itex__hoqyk).value
                    data_arr = builder.extract_value(data_tup, ppp__fkxga)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    ipxs__ackhd, lxxfh__hkrvx = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, img__bvmol, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(hoztv__kwwx)
    c.pyapi.decref(iora__xhva)
    c.pyapi.decref(iuwou__zfgqy)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    oogrp__xvco = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    qxhhk__wllt = context.nrt.meminfo_data(builder, oogrp__xvco.meminfo)
    xfqk__ttlrh = builder.bitcast(qxhhk__wllt, context.get_value_type(
        payload_type).as_pointer())
    vgym__hcobk = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(xfqk__ttlrh))
    return vgym__hcobk


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    vgym__hcobk = _get_struct_arr_payload(c.context, c.builder, typ, val)
    ipxs__ackhd, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), vgym__hcobk.null_bitmap).data
    uzsh__lre = all(isinstance(egcz__rfmh, types.Array) and egcz__rfmh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for egcz__rfmh in typ.data)
    if uzsh__lre:
        klvv__hggro, qxc__mhqj, ngwc__rce = _get_C_API_ptrs(c, vgym__hcobk.
            data, typ.data, typ.names)
        oru__tqpc = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        gomd__fib = cgutils.get_or_insert_function(c.builder.module,
            oru__tqpc, name='np_array_from_struct_array')
        arr = c.builder.call(gomd__fib, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(klvv__hggro, lir
            .IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            qxc__mhqj, lir.IntType(8).as_pointer()), c.builder.bitcast(
            ngwc__rce, lir.IntType(8).as_pointer()), c.context.get_constant
            (types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, vgym__hcobk.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    pfir__fghw = context.insert_const_string(builder.module, 'numpy')
    gpil__bjq = c.pyapi.import_module_noblock(pfir__fghw)
    msw__ssew = c.pyapi.object_getattr_string(gpil__bjq, 'object_')
    gzr__wzaq = c.pyapi.long_from_longlong(length)
    fmv__odctd = c.pyapi.call_method(gpil__bjq, 'ndarray', (gzr__wzaq,
        msw__ssew))
    mai__qogh = c.pyapi.object_getattr_string(gpil__bjq, 'nan')
    with cgutils.for_range(builder, length) as zvsm__xsz:
        img__bvmol = zvsm__xsz.index
        pyarray_setitem(builder, context, fmv__odctd, img__bvmol, mai__qogh)
        bgk__gquxi = get_bitmap_bit(builder, null_bitmap_ptr, img__bvmol)
        ouflc__aaj = builder.icmp_unsigned('!=', bgk__gquxi, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(ouflc__aaj):
            if is_tuple_array:
                hoztv__kwwx = c.pyapi.tuple_new(len(typ.data))
            else:
                hoztv__kwwx = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(mai__qogh)
                    c.pyapi.tuple_setitem(hoztv__kwwx, i, mai__qogh)
                else:
                    c.pyapi.dict_setitem_string(hoztv__kwwx, typ.names[i],
                        mai__qogh)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                ipxs__ackhd, qwll__kgip = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, img__bvmol])
                with builder.if_then(qwll__kgip):
                    ipxs__ackhd, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, img__bvmol])
                    msoq__nly = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(hoztv__kwwx, i, msoq__nly)
                    else:
                        c.pyapi.dict_setitem_string(hoztv__kwwx, typ.names[
                            i], msoq__nly)
                        c.pyapi.decref(msoq__nly)
            pyarray_setitem(builder, context, fmv__odctd, img__bvmol,
                hoztv__kwwx)
            c.pyapi.decref(hoztv__kwwx)
    c.pyapi.decref(gpil__bjq)
    c.pyapi.decref(msw__ssew)
    c.pyapi.decref(gzr__wzaq)
    c.pyapi.decref(mai__qogh)
    return fmv__odctd


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    forgr__cqcjy = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if forgr__cqcjy == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for cwayx__hpef in range(forgr__cqcjy)])
    elif nested_counts_type.count < forgr__cqcjy:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for cwayx__hpef in range(
            forgr__cqcjy - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(egcz__rfmh) for egcz__rfmh in
            names_typ.types)
    fss__mmnp = tuple(egcz__rfmh.instance_type for egcz__rfmh in dtypes_typ
        .types)
    struct_arr_type = StructArrayType(fss__mmnp, names)

    def codegen(context, builder, sig, args):
        xzxb__hsy, nested_counts, cwayx__hpef, cwayx__hpef = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        ghy__alhj, cwayx__hpef, cwayx__hpef = construct_struct_array(context,
            builder, struct_arr_type, xzxb__hsy, nested_counts)
        oogrp__xvco = context.make_helper(builder, struct_arr_type)
        oogrp__xvco.meminfo = ghy__alhj
        return oogrp__xvco._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(xpjq__bfe, str) for
            xpjq__bfe in names) and len(names) == len(data)
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
        ynjsb__axba = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, ynjsb__axba)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        ynjsb__axba = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ynjsb__axba)


def define_struct_dtor(context, builder, struct_type, payload_type):
    shyxn__lum = builder.module
    oru__tqpc = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ankb__lwqt = cgutils.get_or_insert_function(shyxn__lum, oru__tqpc, name
        ='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not ankb__lwqt.is_declaration:
        return ankb__lwqt
    ankb__lwqt.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ankb__lwqt.append_basic_block())
    kol__eaosw = ankb__lwqt.args[0]
    auf__fnxuy = context.get_value_type(payload_type).as_pointer()
    vmjck__zhfm = builder.bitcast(kol__eaosw, auf__fnxuy)
    vgym__hcobk = context.make_helper(builder, payload_type, ref=vmjck__zhfm)
    for i in range(len(struct_type.data)):
        tuuwv__iqp = builder.extract_value(vgym__hcobk.null_bitmap, i)
        ouflc__aaj = builder.icmp_unsigned('==', tuuwv__iqp, lir.Constant(
            tuuwv__iqp.type, 1))
        with builder.if_then(ouflc__aaj):
            val = builder.extract_value(vgym__hcobk.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return ankb__lwqt


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    qxhhk__wllt = context.nrt.meminfo_data(builder, struct.meminfo)
    xfqk__ttlrh = builder.bitcast(qxhhk__wllt, context.get_value_type(
        payload_type).as_pointer())
    vgym__hcobk = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(xfqk__ttlrh))
    return vgym__hcobk, xfqk__ttlrh


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    pfir__fghw = context.insert_const_string(builder.module, 'pandas')
    iora__xhva = c.pyapi.import_module_noblock(pfir__fghw)
    iuwou__zfgqy = c.pyapi.object_getattr_string(iora__xhva, 'NA')
    vmc__fygh = []
    nulls = []
    for i, egcz__rfmh in enumerate(typ.data):
        msoq__nly = c.pyapi.dict_getitem_string(val, typ.names[i])
        kzd__gqqar = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        wjlrw__bsoji = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(egcz__rfmh)))
        ytiu__tgt = is_na_value(builder, context, msoq__nly, iuwou__zfgqy)
        ouflc__aaj = builder.icmp_unsigned('!=', ytiu__tgt, lir.Constant(
            ytiu__tgt.type, 1))
        with builder.if_then(ouflc__aaj):
            builder.store(context.get_constant(types.uint8, 1), kzd__gqqar)
            field_val = c.pyapi.to_native_value(egcz__rfmh, msoq__nly).value
            builder.store(field_val, wjlrw__bsoji)
        vmc__fygh.append(builder.load(wjlrw__bsoji))
        nulls.append(builder.load(kzd__gqqar))
    c.pyapi.decref(iora__xhva)
    c.pyapi.decref(iuwou__zfgqy)
    ghy__alhj = construct_struct(context, builder, typ, vmc__fygh, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = ghy__alhj
    jvn__ausi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=jvn__ausi)


@box(StructType)
def box_struct(typ, val, c):
    gom__huqss = c.pyapi.dict_new(len(typ.data))
    vgym__hcobk, cwayx__hpef = _get_struct_payload(c.context, c.builder,
        typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(gom__huqss, typ.names[i], c.pyapi.
            borrow_none())
        tuuwv__iqp = c.builder.extract_value(vgym__hcobk.null_bitmap, i)
        ouflc__aaj = c.builder.icmp_unsigned('==', tuuwv__iqp, lir.Constant
            (tuuwv__iqp.type, 1))
        with c.builder.if_then(ouflc__aaj):
            zqlp__apdel = c.builder.extract_value(vgym__hcobk.data, i)
            c.context.nrt.incref(c.builder, val_typ, zqlp__apdel)
            itex__hoqyk = c.pyapi.from_native_value(val_typ, zqlp__apdel, c
                .env_manager)
            c.pyapi.dict_setitem_string(gom__huqss, typ.names[i], itex__hoqyk)
            c.pyapi.decref(itex__hoqyk)
    c.context.nrt.decref(c.builder, typ, val)
    return gom__huqss


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(egcz__rfmh) for egcz__rfmh in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, vldo__oiqi = args
        payload_type = StructPayloadType(struct_type.data)
        ebl__zpea = context.get_value_type(payload_type)
        jrsmv__fymqj = context.get_abi_sizeof(ebl__zpea)
        wofhq__laj = define_struct_dtor(context, builder, struct_type,
            payload_type)
        ghy__alhj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jrsmv__fymqj), wofhq__laj)
        qxhhk__wllt = context.nrt.meminfo_data(builder, ghy__alhj)
        xfqk__ttlrh = builder.bitcast(qxhhk__wllt, ebl__zpea.as_pointer())
        vgym__hcobk = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        vgym__hcobk.data = data
        vgym__hcobk.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for cwayx__hpef in range(len(
            data_typ.types))])
        builder.store(vgym__hcobk._getvalue(), xfqk__ttlrh)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = ghy__alhj
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        vgym__hcobk, cwayx__hpef = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vgym__hcobk.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        vgym__hcobk, cwayx__hpef = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vgym__hcobk.null_bitmap)
    gav__hul = types.UniTuple(types.int8, len(struct_typ.data))
    return gav__hul(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, cwayx__hpef, val = args
        vgym__hcobk, xfqk__ttlrh = _get_struct_payload(context, builder,
            struct_typ, struct)
        gmjqx__pywss = vgym__hcobk.data
        ngv__jfdd = builder.insert_value(gmjqx__pywss, val, field_ind)
        jbkv__ylub = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, jbkv__ylub, gmjqx__pywss)
        context.nrt.incref(builder, jbkv__ylub, ngv__jfdd)
        vgym__hcobk.data = ngv__jfdd
        builder.store(vgym__hcobk._getvalue(), xfqk__ttlrh)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    dcnok__rfw = get_overload_const_str(ind)
    if dcnok__rfw not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            dcnok__rfw, struct))
    return struct.names.index(dcnok__rfw)


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
    ebl__zpea = context.get_value_type(payload_type)
    jrsmv__fymqj = context.get_abi_sizeof(ebl__zpea)
    wofhq__laj = define_struct_dtor(context, builder, struct_type, payload_type
        )
    ghy__alhj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jrsmv__fymqj), wofhq__laj)
    qxhhk__wllt = context.nrt.meminfo_data(builder, ghy__alhj)
    xfqk__ttlrh = builder.bitcast(qxhhk__wllt, ebl__zpea.as_pointer())
    vgym__hcobk = cgutils.create_struct_proxy(payload_type)(context, builder)
    vgym__hcobk.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    vgym__hcobk.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(vgym__hcobk._getvalue(), xfqk__ttlrh)
    return ghy__alhj


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    cbn__dgtq = tuple(d.dtype for d in struct_arr_typ.data)
    hwt__glzi = StructType(cbn__dgtq, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        nacw__iaifm, ind = args
        vgym__hcobk = _get_struct_arr_payload(context, builder,
            struct_arr_typ, nacw__iaifm)
        vmc__fygh = []
        sttpp__dvp = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            ghm__scza = builder.extract_value(vgym__hcobk.data, i)
            wpf__jobhd = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [ghm__scza,
                ind])
            sttpp__dvp.append(wpf__jobhd)
            trr__tiw = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            ouflc__aaj = builder.icmp_unsigned('==', wpf__jobhd, lir.
                Constant(wpf__jobhd.type, 1))
            with builder.if_then(ouflc__aaj):
                ecqn__bblm = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    ghm__scza, ind])
                builder.store(ecqn__bblm, trr__tiw)
            vmc__fygh.append(builder.load(trr__tiw))
        if isinstance(hwt__glzi, types.DictType):
            mcg__kjlbi = [context.insert_const_string(builder.module,
                juy__idgqk) for juy__idgqk in struct_arr_typ.names]
            zjc__lsnps = cgutils.pack_array(builder, vmc__fygh)
            kegui__ydf = cgutils.pack_array(builder, mcg__kjlbi)

            def impl(names, vals):
                d = {}
                for i, juy__idgqk in enumerate(names):
                    d[juy__idgqk] = vals[i]
                return d
            xlzfy__mwoik = context.compile_internal(builder, impl,
                hwt__glzi(types.Tuple(tuple(types.StringLiteral(juy__idgqk) for
                juy__idgqk in struct_arr_typ.names)), types.Tuple(cbn__dgtq
                )), [kegui__ydf, zjc__lsnps])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                cbn__dgtq), zjc__lsnps)
            return xlzfy__mwoik
        ghy__alhj = construct_struct(context, builder, hwt__glzi, vmc__fygh,
            sttpp__dvp)
        struct = context.make_helper(builder, hwt__glzi)
        struct.meminfo = ghy__alhj
        return struct._getvalue()
    return hwt__glzi(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        vgym__hcobk = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vgym__hcobk.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        vgym__hcobk = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vgym__hcobk.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(egcz__rfmh) for egcz__rfmh in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, zpcnp__hija, vldo__oiqi = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        ebl__zpea = context.get_value_type(payload_type)
        jrsmv__fymqj = context.get_abi_sizeof(ebl__zpea)
        wofhq__laj = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        ghy__alhj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jrsmv__fymqj), wofhq__laj)
        qxhhk__wllt = context.nrt.meminfo_data(builder, ghy__alhj)
        xfqk__ttlrh = builder.bitcast(qxhhk__wllt, ebl__zpea.as_pointer())
        vgym__hcobk = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        vgym__hcobk.data = data
        vgym__hcobk.null_bitmap = zpcnp__hija
        builder.store(vgym__hcobk._getvalue(), xfqk__ttlrh)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, zpcnp__hija)
        oogrp__xvco = context.make_helper(builder, struct_arr_type)
        oogrp__xvco.meminfo = ghy__alhj
        return oogrp__xvco._getvalue()
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
    abu__aqacg = len(arr.data)
    bmz__rre = 'def impl(arr, ind):\n'
    bmz__rre += '  data = get_data(arr)\n'
    bmz__rre += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        bmz__rre += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        bmz__rre += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        bmz__rre += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    bmz__rre += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(abu__aqacg)), ', '.join("'{}'".format(juy__idgqk) for
        juy__idgqk in arr.names)))
    ogkes__srkgx = {}
    exec(bmz__rre, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, ogkes__srkgx)
    impl = ogkes__srkgx['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        abu__aqacg = len(arr.data)
        bmz__rre = 'def impl(arr, ind, val):\n'
        bmz__rre += '  data = get_data(arr)\n'
        bmz__rre += '  null_bitmap = get_null_bitmap(arr)\n'
        bmz__rre += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(abu__aqacg):
            if isinstance(val, StructType):
                bmz__rre += "  if is_field_value_null(val, '{}'):\n".format(arr
                    .names[i])
                bmz__rre += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                bmz__rre += '  else:\n'
                bmz__rre += "    data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
            else:
                bmz__rre += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        ogkes__srkgx = {}
        exec(bmz__rre, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, ogkes__srkgx)
        impl = ogkes__srkgx['impl']
        return impl
    if isinstance(ind, types.SliceType):
        abu__aqacg = len(arr.data)
        bmz__rre = 'def impl(arr, ind, val):\n'
        bmz__rre += '  data = get_data(arr)\n'
        bmz__rre += '  null_bitmap = get_null_bitmap(arr)\n'
        bmz__rre += '  val_data = get_data(val)\n'
        bmz__rre += '  val_null_bitmap = get_null_bitmap(val)\n'
        bmz__rre += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(abu__aqacg):
            bmz__rre += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        ogkes__srkgx = {}
        exec(bmz__rre, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, ogkes__srkgx)
        impl = ogkes__srkgx['impl']
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
    bmz__rre = 'def impl(A):\n'
    bmz__rre += '  total_nbytes = 0\n'
    bmz__rre += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        bmz__rre += f'  total_nbytes += data[{i}].nbytes\n'
    bmz__rre += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    bmz__rre += '  return total_nbytes\n'
    ogkes__srkgx = {}
    exec(bmz__rre, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, ogkes__srkgx)
    impl = ogkes__srkgx['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        zpcnp__hija = get_null_bitmap(A)
        jmik__guas = bodo.ir.join.copy_arr_tup(data)
        rspz__inlej = zpcnp__hija.copy()
        return init_struct_arr(jmik__guas, rspz__inlej, names)
    return copy_impl
