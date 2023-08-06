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
        fzedt__uyo = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, fzedt__uyo)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        fzedt__uyo = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, fzedt__uyo)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    jbein__iyhlq = builder.module
    sbn__ibuf = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    zxs__tmeyh = cgutils.get_or_insert_function(jbein__iyhlq, sbn__ibuf,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not zxs__tmeyh.is_declaration:
        return zxs__tmeyh
    zxs__tmeyh.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(zxs__tmeyh.append_basic_block())
    iik__fims = zxs__tmeyh.args[0]
    qbp__wqe = context.get_value_type(payload_type).as_pointer()
    fctt__fpzp = builder.bitcast(iik__fims, qbp__wqe)
    cfpr__htr = context.make_helper(builder, payload_type, ref=fctt__fpzp)
    context.nrt.decref(builder, array_item_type.dtype, cfpr__htr.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), cfpr__htr
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), cfpr__htr
        .null_bitmap)
    builder.ret_void()
    return zxs__tmeyh


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    tntkx__wpgss = context.get_value_type(payload_type)
    tbdhj__uun = context.get_abi_sizeof(tntkx__wpgss)
    ify__wiph = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    nba__tpksa = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, tbdhj__uun), ify__wiph)
    aqnw__ogbj = context.nrt.meminfo_data(builder, nba__tpksa)
    mqdqt__wyekr = builder.bitcast(aqnw__ogbj, tntkx__wpgss.as_pointer())
    cfpr__htr = cgutils.create_struct_proxy(payload_type)(context, builder)
    cfpr__htr.n_arrays = n_arrays
    hqplu__pkfhf = n_elems.type.count
    eyht__ludea = builder.extract_value(n_elems, 0)
    aiei__gltp = cgutils.alloca_once_value(builder, eyht__ludea)
    ebse__avpp = builder.icmp_signed('==', eyht__ludea, lir.Constant(
        eyht__ludea.type, -1))
    with builder.if_then(ebse__avpp):
        builder.store(n_arrays, aiei__gltp)
    n_elems = cgutils.pack_array(builder, [builder.load(aiei__gltp)] + [
        builder.extract_value(n_elems, jlyi__gyoa) for jlyi__gyoa in range(
        1, hqplu__pkfhf)])
    cfpr__htr.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    ioyet__zyx = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    hbw__fln = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [ioyet__zyx])
    offsets_ptr = hbw__fln.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    cfpr__htr.offsets = hbw__fln._getvalue()
    buozk__plx = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    mbgrg__orll = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [buozk__plx])
    null_bitmap_ptr = mbgrg__orll.data
    cfpr__htr.null_bitmap = mbgrg__orll._getvalue()
    builder.store(cfpr__htr._getvalue(), mqdqt__wyekr)
    return nba__tpksa, cfpr__htr.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    pxc__rbj, cqll__ibsdb = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    kxlx__xzcv = context.insert_const_string(builder.module, 'pandas')
    czj__wou = c.pyapi.import_module_noblock(kxlx__xzcv)
    mvkso__scrr = c.pyapi.object_getattr_string(czj__wou, 'NA')
    wrm__nep = c.context.get_constant(offset_type, 0)
    builder.store(wrm__nep, offsets_ptr)
    hmsmo__gtt = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as ofid__tsj:
        fwsa__azd = ofid__tsj.index
        item_ind = builder.load(hmsmo__gtt)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [fwsa__azd]))
        arr_obj = seq_getitem(builder, context, val, fwsa__azd)
        set_bitmap_bit(builder, null_bitmap_ptr, fwsa__azd, 0)
        imxu__onyz = is_na_value(builder, context, arr_obj, mvkso__scrr)
        sph__fvt = builder.icmp_unsigned('!=', imxu__onyz, lir.Constant(
            imxu__onyz.type, 1))
        with builder.if_then(sph__fvt):
            set_bitmap_bit(builder, null_bitmap_ptr, fwsa__azd, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), hmsmo__gtt)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(hmsmo__gtt), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(czj__wou)
    c.pyapi.decref(mvkso__scrr)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    mdtol__zqt = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if mdtol__zqt:
        sbn__ibuf = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        dhji__cimxv = cgutils.get_or_insert_function(c.builder.module,
            sbn__ibuf, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(dhji__cimxv,
            [val])])
    else:
        ocyj__rsxau = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ocyj__rsxau, jlyi__gyoa) for jlyi__gyoa in range(1, ocyj__rsxau
            .type.count)])
    nba__tpksa, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if mdtol__zqt:
        acx__gdqun = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        azm__pds = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        sbn__ibuf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        zxs__tmeyh = cgutils.get_or_insert_function(c.builder.module,
            sbn__ibuf, name='array_item_array_from_sequence')
        c.builder.call(zxs__tmeyh, [val, c.builder.bitcast(azm__pds, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), acx__gdqun)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    ehcvj__cfc = c.context.make_helper(c.builder, typ)
    ehcvj__cfc.meminfo = nba__tpksa
    ivp__wyc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ehcvj__cfc._getvalue(), is_error=ivp__wyc)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    ehcvj__cfc = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    aqnw__ogbj = context.nrt.meminfo_data(builder, ehcvj__cfc.meminfo)
    mqdqt__wyekr = builder.bitcast(aqnw__ogbj, context.get_value_type(
        payload_type).as_pointer())
    cfpr__htr = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(mqdqt__wyekr))
    return cfpr__htr


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    kxlx__xzcv = context.insert_const_string(builder.module, 'numpy')
    bgklf__xyta = c.pyapi.import_module_noblock(kxlx__xzcv)
    tfhia__dqug = c.pyapi.object_getattr_string(bgklf__xyta, 'object_')
    wwhbb__dveh = c.pyapi.long_from_longlong(n_arrays)
    inoc__sjlzu = c.pyapi.call_method(bgklf__xyta, 'ndarray', (wwhbb__dveh,
        tfhia__dqug))
    biwvn__tfdk = c.pyapi.object_getattr_string(bgklf__xyta, 'nan')
    hmsmo__gtt = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as ofid__tsj:
        fwsa__azd = ofid__tsj.index
        pyarray_setitem(builder, context, inoc__sjlzu, fwsa__azd, biwvn__tfdk)
        bkfq__vyl = get_bitmap_bit(builder, null_bitmap_ptr, fwsa__azd)
        klegu__ecroi = builder.icmp_unsigned('!=', bkfq__vyl, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(klegu__ecroi):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(fwsa__azd, lir.Constant(fwsa__azd
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                fwsa__azd]))), lir.IntType(64))
            item_ind = builder.load(hmsmo__gtt)
            pxc__rbj, iltsu__rshk = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), hmsmo__gtt)
            arr_obj = c.pyapi.from_native_value(typ.dtype, iltsu__rshk, c.
                env_manager)
            pyarray_setitem(builder, context, inoc__sjlzu, fwsa__azd, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(bgklf__xyta)
    c.pyapi.decref(tfhia__dqug)
    c.pyapi.decref(wwhbb__dveh)
    c.pyapi.decref(biwvn__tfdk)
    return inoc__sjlzu


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    cfpr__htr = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = cfpr__htr.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), cfpr__htr.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), cfpr__htr.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        acx__gdqun = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        azm__pds = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        sbn__ibuf = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        cfnvi__ujntq = cgutils.get_or_insert_function(c.builder.module,
            sbn__ibuf, name='np_array_from_array_item_array')
        arr = c.builder.call(cfnvi__ujntq, [cfpr__htr.n_arrays, c.builder.
            bitcast(azm__pds, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), acx__gdqun)])
    else:
        arr = _box_array_item_array_generic(typ, c, cfpr__htr.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    qmm__befxd, peix__zlrx, akzu__mkw = args
    uwaqn__xugxe = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    hia__tvv = sig.args[1]
    if not isinstance(hia__tvv, types.UniTuple):
        peix__zlrx = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for akzu__mkw in range(uwaqn__xugxe)])
    elif hia__tvv.count < uwaqn__xugxe:
        peix__zlrx = cgutils.pack_array(builder, [builder.extract_value(
            peix__zlrx, jlyi__gyoa) for jlyi__gyoa in range(hia__tvv.count)
            ] + [lir.Constant(lir.IntType(64), -1) for akzu__mkw in range(
            uwaqn__xugxe - hia__tvv.count)])
    nba__tpksa, akzu__mkw, akzu__mkw, akzu__mkw = construct_array_item_array(
        context, builder, array_item_type, qmm__befxd, peix__zlrx)
    ehcvj__cfc = context.make_helper(builder, array_item_type)
    ehcvj__cfc.meminfo = nba__tpksa
    return ehcvj__cfc._getvalue()


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
    n_arrays, uokn__lvst, hbw__fln, mbgrg__orll = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    tntkx__wpgss = context.get_value_type(payload_type)
    tbdhj__uun = context.get_abi_sizeof(tntkx__wpgss)
    ify__wiph = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    nba__tpksa = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, tbdhj__uun), ify__wiph)
    aqnw__ogbj = context.nrt.meminfo_data(builder, nba__tpksa)
    mqdqt__wyekr = builder.bitcast(aqnw__ogbj, tntkx__wpgss.as_pointer())
    cfpr__htr = cgutils.create_struct_proxy(payload_type)(context, builder)
    cfpr__htr.n_arrays = n_arrays
    cfpr__htr.data = uokn__lvst
    cfpr__htr.offsets = hbw__fln
    cfpr__htr.null_bitmap = mbgrg__orll
    builder.store(cfpr__htr._getvalue(), mqdqt__wyekr)
    context.nrt.incref(builder, signature.args[1], uokn__lvst)
    context.nrt.incref(builder, signature.args[2], hbw__fln)
    context.nrt.incref(builder, signature.args[3], mbgrg__orll)
    ehcvj__cfc = context.make_helper(builder, array_item_type)
    ehcvj__cfc.meminfo = nba__tpksa
    return ehcvj__cfc._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    cfce__mjhft = ArrayItemArrayType(data_type)
    sig = cfce__mjhft(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        cfpr__htr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            cfpr__htr.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        cfpr__htr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        azm__pds = context.make_array(types.Array(offset_type, 1, 'C'))(context
            , builder, cfpr__htr.offsets).data
        hbw__fln = builder.bitcast(azm__pds, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(hbw__fln, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        cfpr__htr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            cfpr__htr.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        cfpr__htr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            cfpr__htr.null_bitmap)
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
        cfpr__htr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return cfpr__htr.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, yllrt__alu = args
        ehcvj__cfc = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        aqnw__ogbj = context.nrt.meminfo_data(builder, ehcvj__cfc.meminfo)
        mqdqt__wyekr = builder.bitcast(aqnw__ogbj, context.get_value_type(
            payload_type).as_pointer())
        cfpr__htr = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(mqdqt__wyekr))
        context.nrt.decref(builder, data_typ, cfpr__htr.data)
        cfpr__htr.data = yllrt__alu
        context.nrt.incref(builder, data_typ, yllrt__alu)
        builder.store(cfpr__htr._getvalue(), mqdqt__wyekr)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    uokn__lvst = get_data(arr)
    xzmh__zmfub = len(uokn__lvst)
    if xzmh__zmfub < new_size:
        pibf__xcox = max(2 * xzmh__zmfub, new_size)
        yllrt__alu = bodo.libs.array_kernels.resize_and_copy(uokn__lvst,
            old_size, pibf__xcox)
        replace_data_arr(arr, yllrt__alu)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    uokn__lvst = get_data(arr)
    hbw__fln = get_offsets(arr)
    gqjs__tgun = len(uokn__lvst)
    lke__idc = hbw__fln[-1]
    if gqjs__tgun != lke__idc:
        yllrt__alu = bodo.libs.array_kernels.resize_and_copy(uokn__lvst,
            lke__idc, lke__idc)
        replace_data_arr(arr, yllrt__alu)


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
            hbw__fln = get_offsets(arr)
            uokn__lvst = get_data(arr)
            iyau__gnwkd = hbw__fln[ind]
            irui__lgg = hbw__fln[ind + 1]
            return uokn__lvst[iyau__gnwkd:irui__lgg]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        qft__nuvs = arr.dtype

        def impl_bool(arr, ind):
            lnj__mgu = len(arr)
            if lnj__mgu != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            mbgrg__orll = get_null_bitmap(arr)
            n_arrays = 0
            sbs__wunvs = init_nested_counts(qft__nuvs)
            for jlyi__gyoa in range(lnj__mgu):
                if ind[jlyi__gyoa]:
                    n_arrays += 1
                    ckh__wkj = arr[jlyi__gyoa]
                    sbs__wunvs = add_nested_counts(sbs__wunvs, ckh__wkj)
            inoc__sjlzu = pre_alloc_array_item_array(n_arrays, sbs__wunvs,
                qft__nuvs)
            iyy__pbijk = get_null_bitmap(inoc__sjlzu)
            uun__bjlr = 0
            for hgt__tlqv in range(lnj__mgu):
                if ind[hgt__tlqv]:
                    inoc__sjlzu[uun__bjlr] = arr[hgt__tlqv]
                    avxy__syby = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        mbgrg__orll, hgt__tlqv)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iyy__pbijk,
                        uun__bjlr, avxy__syby)
                    uun__bjlr += 1
            return inoc__sjlzu
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        qft__nuvs = arr.dtype

        def impl_int(arr, ind):
            mbgrg__orll = get_null_bitmap(arr)
            lnj__mgu = len(ind)
            n_arrays = lnj__mgu
            sbs__wunvs = init_nested_counts(qft__nuvs)
            for bloeo__irpye in range(lnj__mgu):
                jlyi__gyoa = ind[bloeo__irpye]
                ckh__wkj = arr[jlyi__gyoa]
                sbs__wunvs = add_nested_counts(sbs__wunvs, ckh__wkj)
            inoc__sjlzu = pre_alloc_array_item_array(n_arrays, sbs__wunvs,
                qft__nuvs)
            iyy__pbijk = get_null_bitmap(inoc__sjlzu)
            for uhyx__ecjq in range(lnj__mgu):
                hgt__tlqv = ind[uhyx__ecjq]
                inoc__sjlzu[uhyx__ecjq] = arr[hgt__tlqv]
                avxy__syby = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    mbgrg__orll, hgt__tlqv)
                bodo.libs.int_arr_ext.set_bit_to_arr(iyy__pbijk, uhyx__ecjq,
                    avxy__syby)
            return inoc__sjlzu
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            lnj__mgu = len(arr)
            oygno__mtoru = numba.cpython.unicode._normalize_slice(ind, lnj__mgu
                )
            yxtq__zsrf = np.arange(oygno__mtoru.start, oygno__mtoru.stop,
                oygno__mtoru.step)
            return arr[yxtq__zsrf]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            hbw__fln = get_offsets(A)
            mbgrg__orll = get_null_bitmap(A)
            if idx == 0:
                hbw__fln[0] = 0
            n_items = len(val)
            srnrb__tkjro = hbw__fln[idx] + n_items
            ensure_data_capacity(A, hbw__fln[idx], srnrb__tkjro)
            uokn__lvst = get_data(A)
            hbw__fln[idx + 1] = hbw__fln[idx] + n_items
            uokn__lvst[hbw__fln[idx]:hbw__fln[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(mbgrg__orll, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            oygno__mtoru = numba.cpython.unicode._normalize_slice(idx, len(A))
            for jlyi__gyoa in range(oygno__mtoru.start, oygno__mtoru.stop,
                oygno__mtoru.step):
                A[jlyi__gyoa] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            hbw__fln = get_offsets(A)
            mbgrg__orll = get_null_bitmap(A)
            mzqet__cyg = get_offsets(val)
            bcb__otlke = get_data(val)
            hfkue__uxwx = get_null_bitmap(val)
            lnj__mgu = len(A)
            oygno__mtoru = numba.cpython.unicode._normalize_slice(idx, lnj__mgu
                )
            zpsb__ncvr, kmdz__qtcyr = oygno__mtoru.start, oygno__mtoru.stop
            assert oygno__mtoru.step == 1
            if zpsb__ncvr == 0:
                hbw__fln[zpsb__ncvr] = 0
            wats__hxhv = hbw__fln[zpsb__ncvr]
            srnrb__tkjro = wats__hxhv + len(bcb__otlke)
            ensure_data_capacity(A, wats__hxhv, srnrb__tkjro)
            uokn__lvst = get_data(A)
            uokn__lvst[wats__hxhv:wats__hxhv + len(bcb__otlke)] = bcb__otlke
            hbw__fln[zpsb__ncvr:kmdz__qtcyr + 1] = mzqet__cyg + wats__hxhv
            vhkj__ktxvk = 0
            for jlyi__gyoa in range(zpsb__ncvr, kmdz__qtcyr):
                avxy__syby = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    hfkue__uxwx, vhkj__ktxvk)
                bodo.libs.int_arr_ext.set_bit_to_arr(mbgrg__orll,
                    jlyi__gyoa, avxy__syby)
                vhkj__ktxvk += 1
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
