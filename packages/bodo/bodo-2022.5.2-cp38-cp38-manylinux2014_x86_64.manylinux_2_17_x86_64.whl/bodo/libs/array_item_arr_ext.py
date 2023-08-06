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
        ybn__blkjo = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ybn__blkjo)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        ybn__blkjo = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ybn__blkjo)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    qztmo__mgyab = builder.module
    apx__qpsxb = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    eqlu__rhpba = cgutils.get_or_insert_function(qztmo__mgyab, apx__qpsxb,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not eqlu__rhpba.is_declaration:
        return eqlu__rhpba
    eqlu__rhpba.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(eqlu__rhpba.append_basic_block())
    kdah__svsip = eqlu__rhpba.args[0]
    tvksw__djvyk = context.get_value_type(payload_type).as_pointer()
    nnd__owier = builder.bitcast(kdah__svsip, tvksw__djvyk)
    dpay__pzz = context.make_helper(builder, payload_type, ref=nnd__owier)
    context.nrt.decref(builder, array_item_type.dtype, dpay__pzz.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), dpay__pzz
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), dpay__pzz
        .null_bitmap)
    builder.ret_void()
    return eqlu__rhpba


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    voktx__rsfgu = context.get_value_type(payload_type)
    uwy__ciymr = context.get_abi_sizeof(voktx__rsfgu)
    mvn__pxze = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    ydesd__tfnqj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, uwy__ciymr), mvn__pxze)
    vnoqz__gbn = context.nrt.meminfo_data(builder, ydesd__tfnqj)
    caatq__mfojz = builder.bitcast(vnoqz__gbn, voktx__rsfgu.as_pointer())
    dpay__pzz = cgutils.create_struct_proxy(payload_type)(context, builder)
    dpay__pzz.n_arrays = n_arrays
    zwrx__pni = n_elems.type.count
    ywoc__cwonf = builder.extract_value(n_elems, 0)
    myvfi__dxpa = cgutils.alloca_once_value(builder, ywoc__cwonf)
    nrf__fop = builder.icmp_signed('==', ywoc__cwonf, lir.Constant(
        ywoc__cwonf.type, -1))
    with builder.if_then(nrf__fop):
        builder.store(n_arrays, myvfi__dxpa)
    n_elems = cgutils.pack_array(builder, [builder.load(myvfi__dxpa)] + [
        builder.extract_value(n_elems, ogbve__lmd) for ogbve__lmd in range(
        1, zwrx__pni)])
    dpay__pzz.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    unv__tlrd = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    dvfmg__cwjij = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [unv__tlrd])
    offsets_ptr = dvfmg__cwjij.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    dpay__pzz.offsets = dvfmg__cwjij._getvalue()
    yhmc__sbt = builder.udiv(builder.add(n_arrays, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    bkoac__lfq = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [yhmc__sbt])
    null_bitmap_ptr = bkoac__lfq.data
    dpay__pzz.null_bitmap = bkoac__lfq._getvalue()
    builder.store(dpay__pzz._getvalue(), caatq__mfojz)
    return ydesd__tfnqj, dpay__pzz.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    hlp__vas, symq__ajkh = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    obgef__xmzlg = context.insert_const_string(builder.module, 'pandas')
    tks__tap = c.pyapi.import_module_noblock(obgef__xmzlg)
    welp__rqto = c.pyapi.object_getattr_string(tks__tap, 'NA')
    nhmh__bez = c.context.get_constant(offset_type, 0)
    builder.store(nhmh__bez, offsets_ptr)
    xrgb__ezf = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as hob__tka:
        ygzlp__eifwc = hob__tka.index
        item_ind = builder.load(xrgb__ezf)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [ygzlp__eifwc]))
        arr_obj = seq_getitem(builder, context, val, ygzlp__eifwc)
        set_bitmap_bit(builder, null_bitmap_ptr, ygzlp__eifwc, 0)
        zyno__baekz = is_na_value(builder, context, arr_obj, welp__rqto)
        hwwny__ijp = builder.icmp_unsigned('!=', zyno__baekz, lir.Constant(
            zyno__baekz.type, 1))
        with builder.if_then(hwwny__ijp):
            set_bitmap_bit(builder, null_bitmap_ptr, ygzlp__eifwc, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), xrgb__ezf)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(xrgb__ezf), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(tks__tap)
    c.pyapi.decref(welp__rqto)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    xesap__glwp = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if xesap__glwp:
        apx__qpsxb = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        tadac__msvs = cgutils.get_or_insert_function(c.builder.module,
            apx__qpsxb, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(tadac__msvs,
            [val])])
    else:
        ywwjo__okzug = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ywwjo__okzug, ogbve__lmd) for ogbve__lmd in range(1,
            ywwjo__okzug.type.count)])
    ydesd__tfnqj, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if xesap__glwp:
        kdm__tnvh = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        uxut__usp = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        apx__qpsxb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        eqlu__rhpba = cgutils.get_or_insert_function(c.builder.module,
            apx__qpsxb, name='array_item_array_from_sequence')
        c.builder.call(eqlu__rhpba, [val, c.builder.bitcast(uxut__usp, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), kdm__tnvh)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    iqsn__fyjns = c.context.make_helper(c.builder, typ)
    iqsn__fyjns.meminfo = ydesd__tfnqj
    xkbc__ptp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(iqsn__fyjns._getvalue(), is_error=xkbc__ptp)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    iqsn__fyjns = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    vnoqz__gbn = context.nrt.meminfo_data(builder, iqsn__fyjns.meminfo)
    caatq__mfojz = builder.bitcast(vnoqz__gbn, context.get_value_type(
        payload_type).as_pointer())
    dpay__pzz = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(caatq__mfojz))
    return dpay__pzz


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    obgef__xmzlg = context.insert_const_string(builder.module, 'numpy')
    xlip__xpwun = c.pyapi.import_module_noblock(obgef__xmzlg)
    cvhcd__ygjv = c.pyapi.object_getattr_string(xlip__xpwun, 'object_')
    bgum__vvw = c.pyapi.long_from_longlong(n_arrays)
    zaxf__bxnoh = c.pyapi.call_method(xlip__xpwun, 'ndarray', (bgum__vvw,
        cvhcd__ygjv))
    yvk__tps = c.pyapi.object_getattr_string(xlip__xpwun, 'nan')
    xrgb__ezf = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_arrays) as hob__tka:
        ygzlp__eifwc = hob__tka.index
        pyarray_setitem(builder, context, zaxf__bxnoh, ygzlp__eifwc, yvk__tps)
        qonye__gsub = get_bitmap_bit(builder, null_bitmap_ptr, ygzlp__eifwc)
        gvkmj__kywb = builder.icmp_unsigned('!=', qonye__gsub, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(gvkmj__kywb):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(ygzlp__eifwc, lir.Constant(
                ygzlp__eifwc.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [ygzlp__eifwc]))), lir.IntType(64))
            item_ind = builder.load(xrgb__ezf)
            hlp__vas, cyzzj__gulr = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), xrgb__ezf)
            arr_obj = c.pyapi.from_native_value(typ.dtype, cyzzj__gulr, c.
                env_manager)
            pyarray_setitem(builder, context, zaxf__bxnoh, ygzlp__eifwc,
                arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(xlip__xpwun)
    c.pyapi.decref(cvhcd__ygjv)
    c.pyapi.decref(bgum__vvw)
    c.pyapi.decref(yvk__tps)
    return zaxf__bxnoh


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    dpay__pzz = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = dpay__pzz.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), dpay__pzz.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), dpay__pzz.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        kdm__tnvh = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        uxut__usp = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        apx__qpsxb = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        rrsfb__epb = cgutils.get_or_insert_function(c.builder.module,
            apx__qpsxb, name='np_array_from_array_item_array')
        arr = c.builder.call(rrsfb__epb, [dpay__pzz.n_arrays, c.builder.
            bitcast(uxut__usp, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), kdm__tnvh)])
    else:
        arr = _box_array_item_array_generic(typ, c, dpay__pzz.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    lwi__xxs, gzigj__kmvg, ngeo__gnuy = args
    nyg__jme = bodo.utils.transform.get_type_alloc_counts(array_item_type.dtype
        )
    lsk__haq = sig.args[1]
    if not isinstance(lsk__haq, types.UniTuple):
        gzigj__kmvg = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), -1) for ngeo__gnuy in range(nyg__jme)])
    elif lsk__haq.count < nyg__jme:
        gzigj__kmvg = cgutils.pack_array(builder, [builder.extract_value(
            gzigj__kmvg, ogbve__lmd) for ogbve__lmd in range(lsk__haq.count
            )] + [lir.Constant(lir.IntType(64), -1) for ngeo__gnuy in range
            (nyg__jme - lsk__haq.count)])
    ydesd__tfnqj, ngeo__gnuy, ngeo__gnuy, ngeo__gnuy = (
        construct_array_item_array(context, builder, array_item_type,
        lwi__xxs, gzigj__kmvg))
    iqsn__fyjns = context.make_helper(builder, array_item_type)
    iqsn__fyjns.meminfo = ydesd__tfnqj
    return iqsn__fyjns._getvalue()


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
    n_arrays, gfwq__wvcvc, dvfmg__cwjij, bkoac__lfq = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    voktx__rsfgu = context.get_value_type(payload_type)
    uwy__ciymr = context.get_abi_sizeof(voktx__rsfgu)
    mvn__pxze = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    ydesd__tfnqj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, uwy__ciymr), mvn__pxze)
    vnoqz__gbn = context.nrt.meminfo_data(builder, ydesd__tfnqj)
    caatq__mfojz = builder.bitcast(vnoqz__gbn, voktx__rsfgu.as_pointer())
    dpay__pzz = cgutils.create_struct_proxy(payload_type)(context, builder)
    dpay__pzz.n_arrays = n_arrays
    dpay__pzz.data = gfwq__wvcvc
    dpay__pzz.offsets = dvfmg__cwjij
    dpay__pzz.null_bitmap = bkoac__lfq
    builder.store(dpay__pzz._getvalue(), caatq__mfojz)
    context.nrt.incref(builder, signature.args[1], gfwq__wvcvc)
    context.nrt.incref(builder, signature.args[2], dvfmg__cwjij)
    context.nrt.incref(builder, signature.args[3], bkoac__lfq)
    iqsn__fyjns = context.make_helper(builder, array_item_type)
    iqsn__fyjns.meminfo = ydesd__tfnqj
    return iqsn__fyjns._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    xrec__rvijq = ArrayItemArrayType(data_type)
    sig = xrec__rvijq(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dpay__pzz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            dpay__pzz.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        dpay__pzz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        uxut__usp = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, dpay__pzz.offsets).data
        dvfmg__cwjij = builder.bitcast(uxut__usp, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(dvfmg__cwjij, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dpay__pzz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            dpay__pzz.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dpay__pzz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            dpay__pzz.null_bitmap)
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
        dpay__pzz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return dpay__pzz.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, ocu__jnx = args
        iqsn__fyjns = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        vnoqz__gbn = context.nrt.meminfo_data(builder, iqsn__fyjns.meminfo)
        caatq__mfojz = builder.bitcast(vnoqz__gbn, context.get_value_type(
            payload_type).as_pointer())
        dpay__pzz = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(caatq__mfojz))
        context.nrt.decref(builder, data_typ, dpay__pzz.data)
        dpay__pzz.data = ocu__jnx
        context.nrt.incref(builder, data_typ, ocu__jnx)
        builder.store(dpay__pzz._getvalue(), caatq__mfojz)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    gfwq__wvcvc = get_data(arr)
    rczhz__olmz = len(gfwq__wvcvc)
    if rczhz__olmz < new_size:
        hdra__ijfl = max(2 * rczhz__olmz, new_size)
        ocu__jnx = bodo.libs.array_kernels.resize_and_copy(gfwq__wvcvc,
            old_size, hdra__ijfl)
        replace_data_arr(arr, ocu__jnx)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    gfwq__wvcvc = get_data(arr)
    dvfmg__cwjij = get_offsets(arr)
    igci__wmas = len(gfwq__wvcvc)
    hdh__rto = dvfmg__cwjij[-1]
    if igci__wmas != hdh__rto:
        ocu__jnx = bodo.libs.array_kernels.resize_and_copy(gfwq__wvcvc,
            hdh__rto, hdh__rto)
        replace_data_arr(arr, ocu__jnx)


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
            dvfmg__cwjij = get_offsets(arr)
            gfwq__wvcvc = get_data(arr)
            qmbie__ldjh = dvfmg__cwjij[ind]
            ant__fcea = dvfmg__cwjij[ind + 1]
            return gfwq__wvcvc[qmbie__ldjh:ant__fcea]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        gugg__sdy = arr.dtype

        def impl_bool(arr, ind):
            wuku__jcxj = len(arr)
            if wuku__jcxj != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            bkoac__lfq = get_null_bitmap(arr)
            n_arrays = 0
            tegfc__oty = init_nested_counts(gugg__sdy)
            for ogbve__lmd in range(wuku__jcxj):
                if ind[ogbve__lmd]:
                    n_arrays += 1
                    apy__hhq = arr[ogbve__lmd]
                    tegfc__oty = add_nested_counts(tegfc__oty, apy__hhq)
            zaxf__bxnoh = pre_alloc_array_item_array(n_arrays, tegfc__oty,
                gugg__sdy)
            iamuj__fcwh = get_null_bitmap(zaxf__bxnoh)
            sqk__itjo = 0
            for sep__qqs in range(wuku__jcxj):
                if ind[sep__qqs]:
                    zaxf__bxnoh[sqk__itjo] = arr[sep__qqs]
                    qkm__ybu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        bkoac__lfq, sep__qqs)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iamuj__fcwh,
                        sqk__itjo, qkm__ybu)
                    sqk__itjo += 1
            return zaxf__bxnoh
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        gugg__sdy = arr.dtype

        def impl_int(arr, ind):
            bkoac__lfq = get_null_bitmap(arr)
            wuku__jcxj = len(ind)
            n_arrays = wuku__jcxj
            tegfc__oty = init_nested_counts(gugg__sdy)
            for ecpbp__bdda in range(wuku__jcxj):
                ogbve__lmd = ind[ecpbp__bdda]
                apy__hhq = arr[ogbve__lmd]
                tegfc__oty = add_nested_counts(tegfc__oty, apy__hhq)
            zaxf__bxnoh = pre_alloc_array_item_array(n_arrays, tegfc__oty,
                gugg__sdy)
            iamuj__fcwh = get_null_bitmap(zaxf__bxnoh)
            for xzvc__pmv in range(wuku__jcxj):
                sep__qqs = ind[xzvc__pmv]
                zaxf__bxnoh[xzvc__pmv] = arr[sep__qqs]
                qkm__ybu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(bkoac__lfq,
                    sep__qqs)
                bodo.libs.int_arr_ext.set_bit_to_arr(iamuj__fcwh, xzvc__pmv,
                    qkm__ybu)
            return zaxf__bxnoh
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            wuku__jcxj = len(arr)
            vtti__vue = numba.cpython.unicode._normalize_slice(ind, wuku__jcxj)
            empx__uqs = np.arange(vtti__vue.start, vtti__vue.stop,
                vtti__vue.step)
            return arr[empx__uqs]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            dvfmg__cwjij = get_offsets(A)
            bkoac__lfq = get_null_bitmap(A)
            if idx == 0:
                dvfmg__cwjij[0] = 0
            n_items = len(val)
            djtah__omq = dvfmg__cwjij[idx] + n_items
            ensure_data_capacity(A, dvfmg__cwjij[idx], djtah__omq)
            gfwq__wvcvc = get_data(A)
            dvfmg__cwjij[idx + 1] = dvfmg__cwjij[idx] + n_items
            gfwq__wvcvc[dvfmg__cwjij[idx]:dvfmg__cwjij[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(bkoac__lfq, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            vtti__vue = numba.cpython.unicode._normalize_slice(idx, len(A))
            for ogbve__lmd in range(vtti__vue.start, vtti__vue.stop,
                vtti__vue.step):
                A[ogbve__lmd] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            dvfmg__cwjij = get_offsets(A)
            bkoac__lfq = get_null_bitmap(A)
            tlrw__aurgt = get_offsets(val)
            zlkx__oxe = get_data(val)
            tws__ztp = get_null_bitmap(val)
            wuku__jcxj = len(A)
            vtti__vue = numba.cpython.unicode._normalize_slice(idx, wuku__jcxj)
            pnwzk__srl, hblp__nqb = vtti__vue.start, vtti__vue.stop
            assert vtti__vue.step == 1
            if pnwzk__srl == 0:
                dvfmg__cwjij[pnwzk__srl] = 0
            lhy__llnz = dvfmg__cwjij[pnwzk__srl]
            djtah__omq = lhy__llnz + len(zlkx__oxe)
            ensure_data_capacity(A, lhy__llnz, djtah__omq)
            gfwq__wvcvc = get_data(A)
            gfwq__wvcvc[lhy__llnz:lhy__llnz + len(zlkx__oxe)] = zlkx__oxe
            dvfmg__cwjij[pnwzk__srl:hblp__nqb + 1] = tlrw__aurgt + lhy__llnz
            unpz__epns = 0
            for ogbve__lmd in range(pnwzk__srl, hblp__nqb):
                qkm__ybu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(tws__ztp,
                    unpz__epns)
                bodo.libs.int_arr_ext.set_bit_to_arr(bkoac__lfq, ogbve__lmd,
                    qkm__ybu)
                unpz__epns += 1
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
