"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lwna__gdmnp = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, lwna__gdmnp)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        lwna__gdmnp = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, lwna__gdmnp)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    neq__yhnt = builder.module
    bsje__xjz = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    rijve__bstlw = cgutils.get_or_insert_function(neq__yhnt, bsje__xjz,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not rijve__bstlw.is_declaration:
        return rijve__bstlw
    rijve__bstlw.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(rijve__bstlw.append_basic_block())
    hjd__cyewy = rijve__bstlw.args[0]
    lif__yqv = context.get_value_type(payload_type).as_pointer()
    vaup__yea = builder.bitcast(hjd__cyewy, lif__yqv)
    wean__xjipr = context.make_helper(builder, payload_type, ref=vaup__yea)
    context.nrt.decref(builder, array_item_type.dtype, wean__xjipr.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        wean__xjipr.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        wean__xjipr.null_bitmap)
    builder.ret_void()
    return rijve__bstlw


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    rck__eva = context.get_value_type(payload_type)
    flnx__vzyvi = context.get_abi_sizeof(rck__eva)
    lmfc__onh = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    onwxm__nrv = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, flnx__vzyvi), lmfc__onh)
    edba__jzuk = context.nrt.meminfo_data(builder, onwxm__nrv)
    qqnan__oihjc = builder.bitcast(edba__jzuk, rck__eva.as_pointer())
    wean__xjipr = cgutils.create_struct_proxy(payload_type)(context, builder)
    wean__xjipr.n_arrays = n_arrays
    htd__lemq = n_elems.type.count
    vqrfe__upi = builder.extract_value(n_elems, 0)
    hnn__bou = cgutils.alloca_once_value(builder, vqrfe__upi)
    cczan__sdqtt = builder.icmp_signed('==', vqrfe__upi, lir.Constant(
        vqrfe__upi.type, -1))
    with builder.if_then(cczan__sdqtt):
        builder.store(n_arrays, hnn__bou)
    n_elems = cgutils.pack_array(builder, [builder.load(hnn__bou)] + [
        builder.extract_value(n_elems, cwv__gkx) for cwv__gkx in range(1,
        htd__lemq)])
    wean__xjipr.data = gen_allocate_array(context, builder, array_item_type
        .dtype, n_elems, c)
    xfuzb__vpdxy = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    ybt__cjcu = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xfuzb__vpdxy])
    offsets_ptr = ybt__cjcu.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    wean__xjipr.offsets = ybt__cjcu._getvalue()
    alm__qdop = builder.udiv(builder.add(n_arrays, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    weuv__mmmyy = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [alm__qdop])
    null_bitmap_ptr = weuv__mmmyy.data
    wean__xjipr.null_bitmap = weuv__mmmyy._getvalue()
    builder.store(wean__xjipr._getvalue(), qqnan__oihjc)
    return onwxm__nrv, wean__xjipr.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    kupr__jxij, wlyq__slpbx = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    ugr__pfvc = context.insert_const_string(builder.module, 'pandas')
    bqgp__qhnn = c.pyapi.import_module_noblock(ugr__pfvc)
    wqcqx__tth = c.pyapi.object_getattr_string(bqgp__qhnn, 'NA')
    awh__ugp = c.context.get_constant(offset_type, 0)
    builder.store(awh__ugp, offsets_ptr)
    jjo__zvlef = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as yjzq__bglxx:
        chnps__lcivk = yjzq__bglxx.index
        item_ind = builder.load(jjo__zvlef)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [chnps__lcivk]))
        arr_obj = seq_getitem(builder, context, val, chnps__lcivk)
        set_bitmap_bit(builder, null_bitmap_ptr, chnps__lcivk, 0)
        phhdi__ynka = is_na_value(builder, context, arr_obj, wqcqx__tth)
        bto__ghte = builder.icmp_unsigned('!=', phhdi__ynka, lir.Constant(
            phhdi__ynka.type, 1))
        with builder.if_then(bto__ghte):
            set_bitmap_bit(builder, null_bitmap_ptr, chnps__lcivk, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), jjo__zvlef)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(jjo__zvlef), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(bqgp__qhnn)
    c.pyapi.decref(wqcqx__tth)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    pqg__zkqih = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if pqg__zkqih:
        bsje__xjz = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        omzeu__oazk = cgutils.get_or_insert_function(c.builder.module,
            bsje__xjz, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(omzeu__oazk,
            [val])])
    else:
        zuvv__namj = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            zuvv__namj, cwv__gkx) for cwv__gkx in range(1, zuvv__namj.type.
            count)])
    onwxm__nrv, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if pqg__zkqih:
        eyy__xluqu = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        fgi__nehue = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        bsje__xjz = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        rijve__bstlw = cgutils.get_or_insert_function(c.builder.module,
            bsje__xjz, name='array_item_array_from_sequence')
        c.builder.call(rijve__bstlw, [val, c.builder.bitcast(fgi__nehue,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), eyy__xluqu)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    sjge__mimbf = c.context.make_helper(c.builder, typ)
    sjge__mimbf.meminfo = onwxm__nrv
    astj__arxd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sjge__mimbf._getvalue(), is_error=astj__arxd)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    sjge__mimbf = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    edba__jzuk = context.nrt.meminfo_data(builder, sjge__mimbf.meminfo)
    qqnan__oihjc = builder.bitcast(edba__jzuk, context.get_value_type(
        payload_type).as_pointer())
    wean__xjipr = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(qqnan__oihjc))
    return wean__xjipr


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    ugr__pfvc = context.insert_const_string(builder.module, 'numpy')
    dxjiz__fru = c.pyapi.import_module_noblock(ugr__pfvc)
    eodyj__xah = c.pyapi.object_getattr_string(dxjiz__fru, 'object_')
    udlw__yiyo = c.pyapi.long_from_longlong(n_arrays)
    qzox__zwcuk = c.pyapi.call_method(dxjiz__fru, 'ndarray', (udlw__yiyo,
        eodyj__xah))
    gbp__chtp = c.pyapi.object_getattr_string(dxjiz__fru, 'nan')
    jjo__zvlef = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as yjzq__bglxx:
        chnps__lcivk = yjzq__bglxx.index
        pyarray_setitem(builder, context, qzox__zwcuk, chnps__lcivk, gbp__chtp)
        fdin__fvpie = get_bitmap_bit(builder, null_bitmap_ptr, chnps__lcivk)
        kqrg__svkhr = builder.icmp_unsigned('!=', fdin__fvpie, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(kqrg__svkhr):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(chnps__lcivk, lir.Constant(
                chnps__lcivk.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [chnps__lcivk]))), lir.IntType(64))
            item_ind = builder.load(jjo__zvlef)
            kupr__jxij, tvfu__jke = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), jjo__zvlef)
            arr_obj = c.pyapi.from_native_value(typ.dtype, tvfu__jke, c.
                env_manager)
            pyarray_setitem(builder, context, qzox__zwcuk, chnps__lcivk,
                arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(dxjiz__fru)
    c.pyapi.decref(eodyj__xah)
    c.pyapi.decref(udlw__yiyo)
    c.pyapi.decref(gbp__chtp)
    return qzox__zwcuk


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    wean__xjipr = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = wean__xjipr.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), wean__xjipr.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), wean__xjipr.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        eyy__xluqu = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        fgi__nehue = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        bsje__xjz = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        wqm__jprsj = cgutils.get_or_insert_function(c.builder.module,
            bsje__xjz, name='np_array_from_array_item_array')
        arr = c.builder.call(wqm__jprsj, [wean__xjipr.n_arrays, c.builder.
            bitcast(fgi__nehue, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), eyy__xluqu)])
    else:
        arr = _box_array_item_array_generic(typ, c, wean__xjipr.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    rzxa__gfbo, diajm__otky, hnbh__mxr = args
    amgc__qsk = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    cxuas__bysh = sig.args[1]
    if not isinstance(cxuas__bysh, types.UniTuple):
        diajm__otky = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), -1) for hnbh__mxr in range(amgc__qsk)])
    elif cxuas__bysh.count < amgc__qsk:
        diajm__otky = cgutils.pack_array(builder, [builder.extract_value(
            diajm__otky, cwv__gkx) for cwv__gkx in range(cxuas__bysh.count)
            ] + [lir.Constant(lir.IntType(64), -1) for hnbh__mxr in range(
            amgc__qsk - cxuas__bysh.count)])
    onwxm__nrv, hnbh__mxr, hnbh__mxr, hnbh__mxr = construct_array_item_array(
        context, builder, array_item_type, rzxa__gfbo, diajm__otky)
    sjge__mimbf = context.make_helper(builder, array_item_type)
    sjge__mimbf.meminfo = onwxm__nrv
    return sjge__mimbf._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, hgkw__llsp, ybt__cjcu, weuv__mmmyy = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    rck__eva = context.get_value_type(payload_type)
    flnx__vzyvi = context.get_abi_sizeof(rck__eva)
    lmfc__onh = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    onwxm__nrv = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, flnx__vzyvi), lmfc__onh)
    edba__jzuk = context.nrt.meminfo_data(builder, onwxm__nrv)
    qqnan__oihjc = builder.bitcast(edba__jzuk, rck__eva.as_pointer())
    wean__xjipr = cgutils.create_struct_proxy(payload_type)(context, builder)
    wean__xjipr.n_arrays = n_arrays
    wean__xjipr.data = hgkw__llsp
    wean__xjipr.offsets = ybt__cjcu
    wean__xjipr.null_bitmap = weuv__mmmyy
    builder.store(wean__xjipr._getvalue(), qqnan__oihjc)
    context.nrt.incref(builder, signature.args[1], hgkw__llsp)
    context.nrt.incref(builder, signature.args[2], ybt__cjcu)
    context.nrt.incref(builder, signature.args[3], weuv__mmmyy)
    sjge__mimbf = context.make_helper(builder, array_item_type)
    sjge__mimbf.meminfo = onwxm__nrv
    return sjge__mimbf._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    cjlw__zofb = ArrayItemArrayType(data_type)
    sig = cjlw__zofb(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        wean__xjipr = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            wean__xjipr.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        wean__xjipr = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        fgi__nehue = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, wean__xjipr.offsets).data
        ybt__cjcu = builder.bitcast(fgi__nehue, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(ybt__cjcu, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        wean__xjipr = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            wean__xjipr.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        wean__xjipr = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            wean__xjipr.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        wean__xjipr = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return wean__xjipr.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, fhwa__vbm = args
        sjge__mimbf = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        edba__jzuk = context.nrt.meminfo_data(builder, sjge__mimbf.meminfo)
        qqnan__oihjc = builder.bitcast(edba__jzuk, context.get_value_type(
            payload_type).as_pointer())
        wean__xjipr = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(qqnan__oihjc))
        context.nrt.decref(builder, data_typ, wean__xjipr.data)
        wean__xjipr.data = fhwa__vbm
        context.nrt.incref(builder, data_typ, fhwa__vbm)
        builder.store(wean__xjipr._getvalue(), qqnan__oihjc)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    hgkw__llsp = get_data(arr)
    lkaob__vpbo = len(hgkw__llsp)
    if lkaob__vpbo < new_size:
        esj__jod = max(2 * lkaob__vpbo, new_size)
        fhwa__vbm = bodo.libs.array_kernels.resize_and_copy(hgkw__llsp,
            old_size, esj__jod)
        replace_data_arr(arr, fhwa__vbm)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    hgkw__llsp = get_data(arr)
    ybt__cjcu = get_offsets(arr)
    rki__rnslu = len(hgkw__llsp)
    qmj__lfx = ybt__cjcu[-1]
    if rki__rnslu != qmj__lfx:
        fhwa__vbm = bodo.libs.array_kernels.resize_and_copy(hgkw__llsp,
            qmj__lfx, qmj__lfx)
        replace_data_arr(arr, fhwa__vbm)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ybt__cjcu = get_offsets(arr)
            hgkw__llsp = get_data(arr)
            ojo__fahn = ybt__cjcu[ind]
            bluen__drdu = ybt__cjcu[ind + 1]
            return hgkw__llsp[ojo__fahn:bluen__drdu]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        qtba__syad = arr.dtype

        def impl_bool(arr, ind):
            dut__vjapb = len(arr)
            if dut__vjapb != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            weuv__mmmyy = get_null_bitmap(arr)
            n_arrays = 0
            yxat__qtnju = init_nested_counts(qtba__syad)
            for cwv__gkx in range(dut__vjapb):
                if ind[cwv__gkx]:
                    n_arrays += 1
                    vpj__pljs = arr[cwv__gkx]
                    yxat__qtnju = add_nested_counts(yxat__qtnju, vpj__pljs)
            qzox__zwcuk = pre_alloc_array_item_array(n_arrays, yxat__qtnju,
                qtba__syad)
            ewi__lgk = get_null_bitmap(qzox__zwcuk)
            hoddq__mlciz = 0
            for duca__rflpb in range(dut__vjapb):
                if ind[duca__rflpb]:
                    qzox__zwcuk[hoddq__mlciz] = arr[duca__rflpb]
                    aiad__okx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        weuv__mmmyy, duca__rflpb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ewi__lgk,
                        hoddq__mlciz, aiad__okx)
                    hoddq__mlciz += 1
            return qzox__zwcuk
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        qtba__syad = arr.dtype

        def impl_int(arr, ind):
            weuv__mmmyy = get_null_bitmap(arr)
            dut__vjapb = len(ind)
            n_arrays = dut__vjapb
            yxat__qtnju = init_nested_counts(qtba__syad)
            for qxck__tef in range(dut__vjapb):
                cwv__gkx = ind[qxck__tef]
                vpj__pljs = arr[cwv__gkx]
                yxat__qtnju = add_nested_counts(yxat__qtnju, vpj__pljs)
            qzox__zwcuk = pre_alloc_array_item_array(n_arrays, yxat__qtnju,
                qtba__syad)
            ewi__lgk = get_null_bitmap(qzox__zwcuk)
            for gexs__dspap in range(dut__vjapb):
                duca__rflpb = ind[gexs__dspap]
                qzox__zwcuk[gexs__dspap] = arr[duca__rflpb]
                aiad__okx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    weuv__mmmyy, duca__rflpb)
                bodo.libs.int_arr_ext.set_bit_to_arr(ewi__lgk, gexs__dspap,
                    aiad__okx)
            return qzox__zwcuk
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            dut__vjapb = len(arr)
            yhfu__bhkgx = numba.cpython.unicode._normalize_slice(ind,
                dut__vjapb)
            rtc__hsb = np.arange(yhfu__bhkgx.start, yhfu__bhkgx.stop,
                yhfu__bhkgx.step)
            return arr[rtc__hsb]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            ybt__cjcu = get_offsets(A)
            weuv__mmmyy = get_null_bitmap(A)
            if idx == 0:
                ybt__cjcu[0] = 0
            n_items = len(val)
            qcm__aafx = ybt__cjcu[idx] + n_items
            ensure_data_capacity(A, ybt__cjcu[idx], qcm__aafx)
            hgkw__llsp = get_data(A)
            ybt__cjcu[idx + 1] = ybt__cjcu[idx] + n_items
            hgkw__llsp[ybt__cjcu[idx]:ybt__cjcu[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(weuv__mmmyy, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            yhfu__bhkgx = numba.cpython.unicode._normalize_slice(idx, len(A))
            for cwv__gkx in range(yhfu__bhkgx.start, yhfu__bhkgx.stop,
                yhfu__bhkgx.step):
                A[cwv__gkx] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            ybt__cjcu = get_offsets(A)
            weuv__mmmyy = get_null_bitmap(A)
            icfry__kfth = get_offsets(val)
            wcm__uqu = get_data(val)
            vmmu__rig = get_null_bitmap(val)
            dut__vjapb = len(A)
            yhfu__bhkgx = numba.cpython.unicode._normalize_slice(idx,
                dut__vjapb)
            fgndv__ztl, qzid__sdy = yhfu__bhkgx.start, yhfu__bhkgx.stop
            assert yhfu__bhkgx.step == 1
            if fgndv__ztl == 0:
                ybt__cjcu[fgndv__ztl] = 0
            rxxwv__rvgv = ybt__cjcu[fgndv__ztl]
            qcm__aafx = rxxwv__rvgv + len(wcm__uqu)
            ensure_data_capacity(A, rxxwv__rvgv, qcm__aafx)
            hgkw__llsp = get_data(A)
            hgkw__llsp[rxxwv__rvgv:rxxwv__rvgv + len(wcm__uqu)] = wcm__uqu
            ybt__cjcu[fgndv__ztl:qzid__sdy + 1] = icfry__kfth + rxxwv__rvgv
            tjdrj__udk = 0
            for cwv__gkx in range(fgndv__ztl, qzid__sdy):
                aiad__okx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(vmmu__rig,
                    tjdrj__udk)
                bodo.libs.int_arr_ext.set_bit_to_arr(weuv__mmmyy, cwv__gkx,
                    aiad__okx)
                tjdrj__udk += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
