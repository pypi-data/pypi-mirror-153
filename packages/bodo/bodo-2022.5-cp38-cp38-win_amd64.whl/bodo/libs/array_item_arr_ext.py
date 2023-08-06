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
        iyz__rjiq = [('n_arrays', types.int64), ('data', fe_type.array_type
            .dtype), ('offsets', types.Array(offset_type, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, iyz__rjiq)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        iyz__rjiq = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, iyz__rjiq)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    lbll__agq = builder.module
    vaa__kbdat = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    kdfp__elab = cgutils.get_or_insert_function(lbll__agq, vaa__kbdat, name
        ='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not kdfp__elab.is_declaration:
        return kdfp__elab
    kdfp__elab.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(kdfp__elab.append_basic_block())
    wtq__cdnt = kdfp__elab.args[0]
    cfnkv__myeen = context.get_value_type(payload_type).as_pointer()
    goban__xftv = builder.bitcast(wtq__cdnt, cfnkv__myeen)
    gflg__axle = context.make_helper(builder, payload_type, ref=goban__xftv)
    context.nrt.decref(builder, array_item_type.dtype, gflg__axle.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        gflg__axle.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        gflg__axle.null_bitmap)
    builder.ret_void()
    return kdfp__elab


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    nroi__hfkg = context.get_value_type(payload_type)
    hnsuq__essff = context.get_abi_sizeof(nroi__hfkg)
    kiosn__wbuj = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    oiaw__kzzsj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, hnsuq__essff), kiosn__wbuj)
    bjgwd__wij = context.nrt.meminfo_data(builder, oiaw__kzzsj)
    eeg__pdgof = builder.bitcast(bjgwd__wij, nroi__hfkg.as_pointer())
    gflg__axle = cgutils.create_struct_proxy(payload_type)(context, builder)
    gflg__axle.n_arrays = n_arrays
    exr__bizy = n_elems.type.count
    hnno__ajj = builder.extract_value(n_elems, 0)
    qfla__whmr = cgutils.alloca_once_value(builder, hnno__ajj)
    zdeyn__uufmt = builder.icmp_signed('==', hnno__ajj, lir.Constant(
        hnno__ajj.type, -1))
    with builder.if_then(zdeyn__uufmt):
        builder.store(n_arrays, qfla__whmr)
    n_elems = cgutils.pack_array(builder, [builder.load(qfla__whmr)] + [
        builder.extract_value(n_elems, fdadt__ovkd) for fdadt__ovkd in
        range(1, exr__bizy)])
    gflg__axle.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    nepqc__wvexl = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    dblgg__nfdt = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [nepqc__wvexl])
    offsets_ptr = dblgg__nfdt.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    gflg__axle.offsets = dblgg__nfdt._getvalue()
    zoz__pkwlu = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    pncz__dajnt = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [zoz__pkwlu])
    null_bitmap_ptr = pncz__dajnt.data
    gflg__axle.null_bitmap = pncz__dajnt._getvalue()
    builder.store(gflg__axle._getvalue(), eeg__pdgof)
    return oiaw__kzzsj, gflg__axle.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    exr__xrbhq, woe__hee = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    vpi__dav = context.insert_const_string(builder.module, 'pandas')
    nyej__ekuc = c.pyapi.import_module_noblock(vpi__dav)
    wly__fjo = c.pyapi.object_getattr_string(nyej__ekuc, 'NA')
    sdllq__jyzb = c.context.get_constant(offset_type, 0)
    builder.store(sdllq__jyzb, offsets_ptr)
    mwrn__hozk = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as ucfie__smu:
        yvhjr__hgi = ucfie__smu.index
        item_ind = builder.load(mwrn__hozk)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [yvhjr__hgi]))
        arr_obj = seq_getitem(builder, context, val, yvhjr__hgi)
        set_bitmap_bit(builder, null_bitmap_ptr, yvhjr__hgi, 0)
        mqp__vkq = is_na_value(builder, context, arr_obj, wly__fjo)
        bfbh__ozpzp = builder.icmp_unsigned('!=', mqp__vkq, lir.Constant(
            mqp__vkq.type, 1))
        with builder.if_then(bfbh__ozpzp):
            set_bitmap_bit(builder, null_bitmap_ptr, yvhjr__hgi, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), mwrn__hozk)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(mwrn__hozk), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(nyej__ekuc)
    c.pyapi.decref(wly__fjo)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    yatuj__zyuat = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if yatuj__zyuat:
        vaa__kbdat = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        txaak__cimh = cgutils.get_or_insert_function(c.builder.module,
            vaa__kbdat, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(txaak__cimh,
            [val])])
    else:
        pfcch__dpdt = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            pfcch__dpdt, fdadt__ovkd) for fdadt__ovkd in range(1,
            pfcch__dpdt.type.count)])
    oiaw__kzzsj, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if yatuj__zyuat:
        ptj__vrp = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        coxgw__qlxcv = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        vaa__kbdat = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        kdfp__elab = cgutils.get_or_insert_function(c.builder.module,
            vaa__kbdat, name='array_item_array_from_sequence')
        c.builder.call(kdfp__elab, [val, c.builder.bitcast(coxgw__qlxcv,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), ptj__vrp)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    zeea__xpys = c.context.make_helper(c.builder, typ)
    zeea__xpys.meminfo = oiaw__kzzsj
    bljkx__nxctj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zeea__xpys._getvalue(), is_error=bljkx__nxctj)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    zeea__xpys = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    bjgwd__wij = context.nrt.meminfo_data(builder, zeea__xpys.meminfo)
    eeg__pdgof = builder.bitcast(bjgwd__wij, context.get_value_type(
        payload_type).as_pointer())
    gflg__axle = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(eeg__pdgof))
    return gflg__axle


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    vpi__dav = context.insert_const_string(builder.module, 'numpy')
    ric__pyb = c.pyapi.import_module_noblock(vpi__dav)
    hbav__olm = c.pyapi.object_getattr_string(ric__pyb, 'object_')
    upow__vdae = c.pyapi.long_from_longlong(n_arrays)
    vmnq__cpxo = c.pyapi.call_method(ric__pyb, 'ndarray', (upow__vdae,
        hbav__olm))
    ywaum__pxopm = c.pyapi.object_getattr_string(ric__pyb, 'nan')
    mwrn__hozk = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as ucfie__smu:
        yvhjr__hgi = ucfie__smu.index
        pyarray_setitem(builder, context, vmnq__cpxo, yvhjr__hgi, ywaum__pxopm)
        ahxpd__ywo = get_bitmap_bit(builder, null_bitmap_ptr, yvhjr__hgi)
        hzgu__cfd = builder.icmp_unsigned('!=', ahxpd__ywo, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(hzgu__cfd):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(yvhjr__hgi, lir.Constant(
                yvhjr__hgi.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [yvhjr__hgi]))), lir.IntType(64))
            item_ind = builder.load(mwrn__hozk)
            exr__xrbhq, xzb__abbgi = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), mwrn__hozk)
            arr_obj = c.pyapi.from_native_value(typ.dtype, xzb__abbgi, c.
                env_manager)
            pyarray_setitem(builder, context, vmnq__cpxo, yvhjr__hgi, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(ric__pyb)
    c.pyapi.decref(hbav__olm)
    c.pyapi.decref(upow__vdae)
    c.pyapi.decref(ywaum__pxopm)
    return vmnq__cpxo


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    gflg__axle = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = gflg__axle.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), gflg__axle.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), gflg__axle.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        ptj__vrp = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        coxgw__qlxcv = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        vaa__kbdat = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        cgy__zoh = cgutils.get_or_insert_function(c.builder.module,
            vaa__kbdat, name='np_array_from_array_item_array')
        arr = c.builder.call(cgy__zoh, [gflg__axle.n_arrays, c.builder.
            bitcast(coxgw__qlxcv, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), ptj__vrp)])
    else:
        arr = _box_array_item_array_generic(typ, c, gflg__axle.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    ededj__xzevg, sfq__lhoow, nvxq__cfipm = args
    nipv__cnv = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    qdmjh__nzv = sig.args[1]
    if not isinstance(qdmjh__nzv, types.UniTuple):
        sfq__lhoow = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for nvxq__cfipm in range(nipv__cnv)])
    elif qdmjh__nzv.count < nipv__cnv:
        sfq__lhoow = cgutils.pack_array(builder, [builder.extract_value(
            sfq__lhoow, fdadt__ovkd) for fdadt__ovkd in range(qdmjh__nzv.
            count)] + [lir.Constant(lir.IntType(64), -1) for nvxq__cfipm in
            range(nipv__cnv - qdmjh__nzv.count)])
    oiaw__kzzsj, nvxq__cfipm, nvxq__cfipm, nvxq__cfipm = (
        construct_array_item_array(context, builder, array_item_type,
        ededj__xzevg, sfq__lhoow))
    zeea__xpys = context.make_helper(builder, array_item_type)
    zeea__xpys.meminfo = oiaw__kzzsj
    return zeea__xpys._getvalue()


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
    n_arrays, yef__itpr, dblgg__nfdt, pncz__dajnt = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    nroi__hfkg = context.get_value_type(payload_type)
    hnsuq__essff = context.get_abi_sizeof(nroi__hfkg)
    kiosn__wbuj = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    oiaw__kzzsj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, hnsuq__essff), kiosn__wbuj)
    bjgwd__wij = context.nrt.meminfo_data(builder, oiaw__kzzsj)
    eeg__pdgof = builder.bitcast(bjgwd__wij, nroi__hfkg.as_pointer())
    gflg__axle = cgutils.create_struct_proxy(payload_type)(context, builder)
    gflg__axle.n_arrays = n_arrays
    gflg__axle.data = yef__itpr
    gflg__axle.offsets = dblgg__nfdt
    gflg__axle.null_bitmap = pncz__dajnt
    builder.store(gflg__axle._getvalue(), eeg__pdgof)
    context.nrt.incref(builder, signature.args[1], yef__itpr)
    context.nrt.incref(builder, signature.args[2], dblgg__nfdt)
    context.nrt.incref(builder, signature.args[3], pncz__dajnt)
    zeea__xpys = context.make_helper(builder, array_item_type)
    zeea__xpys.meminfo = oiaw__kzzsj
    return zeea__xpys._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    kjx__gtog = ArrayItemArrayType(data_type)
    sig = kjx__gtog(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gflg__axle = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            gflg__axle.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        gflg__axle = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        coxgw__qlxcv = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, gflg__axle.offsets).data
        dblgg__nfdt = builder.bitcast(coxgw__qlxcv, lir.IntType(offset_type
            .bitwidth).as_pointer())
        return builder.load(builder.gep(dblgg__nfdt, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gflg__axle = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            gflg__axle.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gflg__axle = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            gflg__axle.null_bitmap)
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
        gflg__axle = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return gflg__axle.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, rziro__zwv = args
        zeea__xpys = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        bjgwd__wij = context.nrt.meminfo_data(builder, zeea__xpys.meminfo)
        eeg__pdgof = builder.bitcast(bjgwd__wij, context.get_value_type(
            payload_type).as_pointer())
        gflg__axle = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(eeg__pdgof))
        context.nrt.decref(builder, data_typ, gflg__axle.data)
        gflg__axle.data = rziro__zwv
        context.nrt.incref(builder, data_typ, rziro__zwv)
        builder.store(gflg__axle._getvalue(), eeg__pdgof)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    yef__itpr = get_data(arr)
    yagt__nlxk = len(yef__itpr)
    if yagt__nlxk < new_size:
        vijgj__dlu = max(2 * yagt__nlxk, new_size)
        rziro__zwv = bodo.libs.array_kernels.resize_and_copy(yef__itpr,
            old_size, vijgj__dlu)
        replace_data_arr(arr, rziro__zwv)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    yef__itpr = get_data(arr)
    dblgg__nfdt = get_offsets(arr)
    nxea__ska = len(yef__itpr)
    ffcm__hai = dblgg__nfdt[-1]
    if nxea__ska != ffcm__hai:
        rziro__zwv = bodo.libs.array_kernels.resize_and_copy(yef__itpr,
            ffcm__hai, ffcm__hai)
        replace_data_arr(arr, rziro__zwv)


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
            dblgg__nfdt = get_offsets(arr)
            yef__itpr = get_data(arr)
            dhr__eobg = dblgg__nfdt[ind]
            vcynq__zwsb = dblgg__nfdt[ind + 1]
            return yef__itpr[dhr__eobg:vcynq__zwsb]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        hvtre__vmf = arr.dtype

        def impl_bool(arr, ind):
            vrihw__ybt = len(arr)
            if vrihw__ybt != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            pncz__dajnt = get_null_bitmap(arr)
            n_arrays = 0
            qvc__qxra = init_nested_counts(hvtre__vmf)
            for fdadt__ovkd in range(vrihw__ybt):
                if ind[fdadt__ovkd]:
                    n_arrays += 1
                    pkqp__mvlvd = arr[fdadt__ovkd]
                    qvc__qxra = add_nested_counts(qvc__qxra, pkqp__mvlvd)
            vmnq__cpxo = pre_alloc_array_item_array(n_arrays, qvc__qxra,
                hvtre__vmf)
            hwxsv__uttj = get_null_bitmap(vmnq__cpxo)
            qwyn__emb = 0
            for uow__oloqb in range(vrihw__ybt):
                if ind[uow__oloqb]:
                    vmnq__cpxo[qwyn__emb] = arr[uow__oloqb]
                    rogry__nbao = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        pncz__dajnt, uow__oloqb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hwxsv__uttj,
                        qwyn__emb, rogry__nbao)
                    qwyn__emb += 1
            return vmnq__cpxo
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        hvtre__vmf = arr.dtype

        def impl_int(arr, ind):
            pncz__dajnt = get_null_bitmap(arr)
            vrihw__ybt = len(ind)
            n_arrays = vrihw__ybt
            qvc__qxra = init_nested_counts(hvtre__vmf)
            for ipm__gjdm in range(vrihw__ybt):
                fdadt__ovkd = ind[ipm__gjdm]
                pkqp__mvlvd = arr[fdadt__ovkd]
                qvc__qxra = add_nested_counts(qvc__qxra, pkqp__mvlvd)
            vmnq__cpxo = pre_alloc_array_item_array(n_arrays, qvc__qxra,
                hvtre__vmf)
            hwxsv__uttj = get_null_bitmap(vmnq__cpxo)
            for pgyub__wmbi in range(vrihw__ybt):
                uow__oloqb = ind[pgyub__wmbi]
                vmnq__cpxo[pgyub__wmbi] = arr[uow__oloqb]
                rogry__nbao = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    pncz__dajnt, uow__oloqb)
                bodo.libs.int_arr_ext.set_bit_to_arr(hwxsv__uttj,
                    pgyub__wmbi, rogry__nbao)
            return vmnq__cpxo
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            vrihw__ybt = len(arr)
            nbxzn__lcdt = numba.cpython.unicode._normalize_slice(ind,
                vrihw__ybt)
            gku__acd = np.arange(nbxzn__lcdt.start, nbxzn__lcdt.stop,
                nbxzn__lcdt.step)
            return arr[gku__acd]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            dblgg__nfdt = get_offsets(A)
            pncz__dajnt = get_null_bitmap(A)
            if idx == 0:
                dblgg__nfdt[0] = 0
            n_items = len(val)
            hdp__dmfn = dblgg__nfdt[idx] + n_items
            ensure_data_capacity(A, dblgg__nfdt[idx], hdp__dmfn)
            yef__itpr = get_data(A)
            dblgg__nfdt[idx + 1] = dblgg__nfdt[idx] + n_items
            yef__itpr[dblgg__nfdt[idx]:dblgg__nfdt[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(pncz__dajnt, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            nbxzn__lcdt = numba.cpython.unicode._normalize_slice(idx, len(A))
            for fdadt__ovkd in range(nbxzn__lcdt.start, nbxzn__lcdt.stop,
                nbxzn__lcdt.step):
                A[fdadt__ovkd] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            dblgg__nfdt = get_offsets(A)
            pncz__dajnt = get_null_bitmap(A)
            tbc__vkay = get_offsets(val)
            kwqph__oub = get_data(val)
            ertml__bfhpo = get_null_bitmap(val)
            vrihw__ybt = len(A)
            nbxzn__lcdt = numba.cpython.unicode._normalize_slice(idx,
                vrihw__ybt)
            wxnfb__gytl, cqi__qew = nbxzn__lcdt.start, nbxzn__lcdt.stop
            assert nbxzn__lcdt.step == 1
            if wxnfb__gytl == 0:
                dblgg__nfdt[wxnfb__gytl] = 0
            ivzap__etgcw = dblgg__nfdt[wxnfb__gytl]
            hdp__dmfn = ivzap__etgcw + len(kwqph__oub)
            ensure_data_capacity(A, ivzap__etgcw, hdp__dmfn)
            yef__itpr = get_data(A)
            yef__itpr[ivzap__etgcw:ivzap__etgcw + len(kwqph__oub)] = kwqph__oub
            dblgg__nfdt[wxnfb__gytl:cqi__qew + 1] = tbc__vkay + ivzap__etgcw
            msyn__uzkwe = 0
            for fdadt__ovkd in range(wxnfb__gytl, cqi__qew):
                rogry__nbao = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    ertml__bfhpo, msyn__uzkwe)
                bodo.libs.int_arr_ext.set_bit_to_arr(pncz__dajnt,
                    fdadt__ovkd, rogry__nbao)
                msyn__uzkwe += 1
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
