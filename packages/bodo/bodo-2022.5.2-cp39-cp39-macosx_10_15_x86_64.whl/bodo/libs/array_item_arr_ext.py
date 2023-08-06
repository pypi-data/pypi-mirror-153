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
        ltkz__ulnr = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ltkz__ulnr)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        ltkz__ulnr = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ltkz__ulnr)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    src__spdk = builder.module
    gxdgp__vnrn = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    jiynd__hbt = cgutils.get_or_insert_function(src__spdk, gxdgp__vnrn,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not jiynd__hbt.is_declaration:
        return jiynd__hbt
    jiynd__hbt.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(jiynd__hbt.append_basic_block())
    nre__goj = jiynd__hbt.args[0]
    bjhz__xkjo = context.get_value_type(payload_type).as_pointer()
    kef__jdyh = builder.bitcast(nre__goj, bjhz__xkjo)
    liwu__epuf = context.make_helper(builder, payload_type, ref=kef__jdyh)
    context.nrt.decref(builder, array_item_type.dtype, liwu__epuf.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        liwu__epuf.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        liwu__epuf.null_bitmap)
    builder.ret_void()
    return jiynd__hbt


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    fjxz__mng = context.get_value_type(payload_type)
    quln__rpv = context.get_abi_sizeof(fjxz__mng)
    jqzx__jjeow = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    bcm__qynbf = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, quln__rpv), jqzx__jjeow)
    hrme__obpyh = context.nrt.meminfo_data(builder, bcm__qynbf)
    jfvq__lunu = builder.bitcast(hrme__obpyh, fjxz__mng.as_pointer())
    liwu__epuf = cgutils.create_struct_proxy(payload_type)(context, builder)
    liwu__epuf.n_arrays = n_arrays
    htzaa__syxm = n_elems.type.count
    wpveu__jmcjp = builder.extract_value(n_elems, 0)
    pclpu__wnupx = cgutils.alloca_once_value(builder, wpveu__jmcjp)
    faamf__pcj = builder.icmp_signed('==', wpveu__jmcjp, lir.Constant(
        wpveu__jmcjp.type, -1))
    with builder.if_then(faamf__pcj):
        builder.store(n_arrays, pclpu__wnupx)
    n_elems = cgutils.pack_array(builder, [builder.load(pclpu__wnupx)] + [
        builder.extract_value(n_elems, tkn__riuk) for tkn__riuk in range(1,
        htzaa__syxm)])
    liwu__epuf.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    isd__cmcbo = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    mmbnr__dev = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [isd__cmcbo])
    offsets_ptr = mmbnr__dev.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    liwu__epuf.offsets = mmbnr__dev._getvalue()
    eacsi__rdlv = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    xuop__gifim = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [eacsi__rdlv])
    null_bitmap_ptr = xuop__gifim.data
    liwu__epuf.null_bitmap = xuop__gifim._getvalue()
    builder.store(liwu__epuf._getvalue(), jfvq__lunu)
    return bcm__qynbf, liwu__epuf.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    uyjak__fao, dndzm__tycng = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    zjpgk__yvcx = context.insert_const_string(builder.module, 'pandas')
    nuah__bvzhe = c.pyapi.import_module_noblock(zjpgk__yvcx)
    kay__nih = c.pyapi.object_getattr_string(nuah__bvzhe, 'NA')
    dlgli__yirb = c.context.get_constant(offset_type, 0)
    builder.store(dlgli__yirb, offsets_ptr)
    dymwg__fry = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as fqo__thash:
        erg__dixy = fqo__thash.index
        item_ind = builder.load(dymwg__fry)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [erg__dixy]))
        arr_obj = seq_getitem(builder, context, val, erg__dixy)
        set_bitmap_bit(builder, null_bitmap_ptr, erg__dixy, 0)
        bxae__bvwrl = is_na_value(builder, context, arr_obj, kay__nih)
        pveq__vzzlu = builder.icmp_unsigned('!=', bxae__bvwrl, lir.Constant
            (bxae__bvwrl.type, 1))
        with builder.if_then(pveq__vzzlu):
            set_bitmap_bit(builder, null_bitmap_ptr, erg__dixy, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), dymwg__fry)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(dymwg__fry), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(nuah__bvzhe)
    c.pyapi.decref(kay__nih)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    czdqv__gojsk = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if czdqv__gojsk:
        gxdgp__vnrn = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        ydr__emp = cgutils.get_or_insert_function(c.builder.module,
            gxdgp__vnrn, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(ydr__emp, [
            val])])
    else:
        jln__zrp = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            jln__zrp, tkn__riuk) for tkn__riuk in range(1, jln__zrp.type.
            count)])
    bcm__qynbf, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if czdqv__gojsk:
        rhled__nuhld = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        fmplo__qpkpr = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        gxdgp__vnrn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        jiynd__hbt = cgutils.get_or_insert_function(c.builder.module,
            gxdgp__vnrn, name='array_item_array_from_sequence')
        c.builder.call(jiynd__hbt, [val, c.builder.bitcast(fmplo__qpkpr,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), rhled__nuhld)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    pwnr__ghr = c.context.make_helper(c.builder, typ)
    pwnr__ghr.meminfo = bcm__qynbf
    kahek__hepcd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pwnr__ghr._getvalue(), is_error=kahek__hepcd)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    pwnr__ghr = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    hrme__obpyh = context.nrt.meminfo_data(builder, pwnr__ghr.meminfo)
    jfvq__lunu = builder.bitcast(hrme__obpyh, context.get_value_type(
        payload_type).as_pointer())
    liwu__epuf = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(jfvq__lunu))
    return liwu__epuf


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    zjpgk__yvcx = context.insert_const_string(builder.module, 'numpy')
    jnct__ihnsk = c.pyapi.import_module_noblock(zjpgk__yvcx)
    pil__wrmj = c.pyapi.object_getattr_string(jnct__ihnsk, 'object_')
    pxoq__ttkng = c.pyapi.long_from_longlong(n_arrays)
    zjfao__jzu = c.pyapi.call_method(jnct__ihnsk, 'ndarray', (pxoq__ttkng,
        pil__wrmj))
    nuiv__guojm = c.pyapi.object_getattr_string(jnct__ihnsk, 'nan')
    dymwg__fry = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as fqo__thash:
        erg__dixy = fqo__thash.index
        pyarray_setitem(builder, context, zjfao__jzu, erg__dixy, nuiv__guojm)
        rysix__riqu = get_bitmap_bit(builder, null_bitmap_ptr, erg__dixy)
        ckmh__ghoq = builder.icmp_unsigned('!=', rysix__riqu, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(ckmh__ghoq):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(erg__dixy, lir.Constant(erg__dixy
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                erg__dixy]))), lir.IntType(64))
            item_ind = builder.load(dymwg__fry)
            uyjak__fao, mle__vxrva = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), dymwg__fry)
            arr_obj = c.pyapi.from_native_value(typ.dtype, mle__vxrva, c.
                env_manager)
            pyarray_setitem(builder, context, zjfao__jzu, erg__dixy, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(jnct__ihnsk)
    c.pyapi.decref(pil__wrmj)
    c.pyapi.decref(pxoq__ttkng)
    c.pyapi.decref(nuiv__guojm)
    return zjfao__jzu


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    liwu__epuf = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = liwu__epuf.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), liwu__epuf.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), liwu__epuf.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        rhled__nuhld = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        fmplo__qpkpr = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        gxdgp__vnrn = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        wsx__ibcpz = cgutils.get_or_insert_function(c.builder.module,
            gxdgp__vnrn, name='np_array_from_array_item_array')
        arr = c.builder.call(wsx__ibcpz, [liwu__epuf.n_arrays, c.builder.
            bitcast(fmplo__qpkpr, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), rhled__nuhld)])
    else:
        arr = _box_array_item_array_generic(typ, c, liwu__epuf.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    kvvyq__xprdo, qcps__jhm, flk__rftr = args
    qnpbo__bbr = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    qypyw__tvysz = sig.args[1]
    if not isinstance(qypyw__tvysz, types.UniTuple):
        qcps__jhm = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for flk__rftr in range(qnpbo__bbr)])
    elif qypyw__tvysz.count < qnpbo__bbr:
        qcps__jhm = cgutils.pack_array(builder, [builder.extract_value(
            qcps__jhm, tkn__riuk) for tkn__riuk in range(qypyw__tvysz.count
            )] + [lir.Constant(lir.IntType(64), -1) for flk__rftr in range(
            qnpbo__bbr - qypyw__tvysz.count)])
    bcm__qynbf, flk__rftr, flk__rftr, flk__rftr = construct_array_item_array(
        context, builder, array_item_type, kvvyq__xprdo, qcps__jhm)
    pwnr__ghr = context.make_helper(builder, array_item_type)
    pwnr__ghr.meminfo = bcm__qynbf
    return pwnr__ghr._getvalue()


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
    n_arrays, gbg__recdu, mmbnr__dev, xuop__gifim = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    fjxz__mng = context.get_value_type(payload_type)
    quln__rpv = context.get_abi_sizeof(fjxz__mng)
    jqzx__jjeow = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    bcm__qynbf = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, quln__rpv), jqzx__jjeow)
    hrme__obpyh = context.nrt.meminfo_data(builder, bcm__qynbf)
    jfvq__lunu = builder.bitcast(hrme__obpyh, fjxz__mng.as_pointer())
    liwu__epuf = cgutils.create_struct_proxy(payload_type)(context, builder)
    liwu__epuf.n_arrays = n_arrays
    liwu__epuf.data = gbg__recdu
    liwu__epuf.offsets = mmbnr__dev
    liwu__epuf.null_bitmap = xuop__gifim
    builder.store(liwu__epuf._getvalue(), jfvq__lunu)
    context.nrt.incref(builder, signature.args[1], gbg__recdu)
    context.nrt.incref(builder, signature.args[2], mmbnr__dev)
    context.nrt.incref(builder, signature.args[3], xuop__gifim)
    pwnr__ghr = context.make_helper(builder, array_item_type)
    pwnr__ghr.meminfo = bcm__qynbf
    return pwnr__ghr._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    mbg__gljc = ArrayItemArrayType(data_type)
    sig = mbg__gljc(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        liwu__epuf = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            liwu__epuf.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        liwu__epuf = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        fmplo__qpkpr = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, liwu__epuf.offsets).data
        mmbnr__dev = builder.bitcast(fmplo__qpkpr, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(mmbnr__dev, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        liwu__epuf = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            liwu__epuf.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        liwu__epuf = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            liwu__epuf.null_bitmap)
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
        liwu__epuf = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return liwu__epuf.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, ixj__shfs = args
        pwnr__ghr = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        hrme__obpyh = context.nrt.meminfo_data(builder, pwnr__ghr.meminfo)
        jfvq__lunu = builder.bitcast(hrme__obpyh, context.get_value_type(
            payload_type).as_pointer())
        liwu__epuf = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(jfvq__lunu))
        context.nrt.decref(builder, data_typ, liwu__epuf.data)
        liwu__epuf.data = ixj__shfs
        context.nrt.incref(builder, data_typ, ixj__shfs)
        builder.store(liwu__epuf._getvalue(), jfvq__lunu)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    gbg__recdu = get_data(arr)
    yuq__vwqpo = len(gbg__recdu)
    if yuq__vwqpo < new_size:
        itmuf__mhq = max(2 * yuq__vwqpo, new_size)
        ixj__shfs = bodo.libs.array_kernels.resize_and_copy(gbg__recdu,
            old_size, itmuf__mhq)
        replace_data_arr(arr, ixj__shfs)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    gbg__recdu = get_data(arr)
    mmbnr__dev = get_offsets(arr)
    mbq__xdvl = len(gbg__recdu)
    uoqjf__vxys = mmbnr__dev[-1]
    if mbq__xdvl != uoqjf__vxys:
        ixj__shfs = bodo.libs.array_kernels.resize_and_copy(gbg__recdu,
            uoqjf__vxys, uoqjf__vxys)
        replace_data_arr(arr, ixj__shfs)


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
            mmbnr__dev = get_offsets(arr)
            gbg__recdu = get_data(arr)
            nad__wzjr = mmbnr__dev[ind]
            tufui__lru = mmbnr__dev[ind + 1]
            return gbg__recdu[nad__wzjr:tufui__lru]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        gwzl__cbyc = arr.dtype

        def impl_bool(arr, ind):
            oxkkf__lolti = len(arr)
            if oxkkf__lolti != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            xuop__gifim = get_null_bitmap(arr)
            n_arrays = 0
            gukoh__hirmk = init_nested_counts(gwzl__cbyc)
            for tkn__riuk in range(oxkkf__lolti):
                if ind[tkn__riuk]:
                    n_arrays += 1
                    vfkma__fjp = arr[tkn__riuk]
                    gukoh__hirmk = add_nested_counts(gukoh__hirmk, vfkma__fjp)
            zjfao__jzu = pre_alloc_array_item_array(n_arrays, gukoh__hirmk,
                gwzl__cbyc)
            cehlr__zlysv = get_null_bitmap(zjfao__jzu)
            gmf__myc = 0
            for cgh__lcjye in range(oxkkf__lolti):
                if ind[cgh__lcjye]:
                    zjfao__jzu[gmf__myc] = arr[cgh__lcjye]
                    phs__cokmq = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        xuop__gifim, cgh__lcjye)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cehlr__zlysv,
                        gmf__myc, phs__cokmq)
                    gmf__myc += 1
            return zjfao__jzu
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        gwzl__cbyc = arr.dtype

        def impl_int(arr, ind):
            xuop__gifim = get_null_bitmap(arr)
            oxkkf__lolti = len(ind)
            n_arrays = oxkkf__lolti
            gukoh__hirmk = init_nested_counts(gwzl__cbyc)
            for jlmb__sijb in range(oxkkf__lolti):
                tkn__riuk = ind[jlmb__sijb]
                vfkma__fjp = arr[tkn__riuk]
                gukoh__hirmk = add_nested_counts(gukoh__hirmk, vfkma__fjp)
            zjfao__jzu = pre_alloc_array_item_array(n_arrays, gukoh__hirmk,
                gwzl__cbyc)
            cehlr__zlysv = get_null_bitmap(zjfao__jzu)
            for cnpy__qlvma in range(oxkkf__lolti):
                cgh__lcjye = ind[cnpy__qlvma]
                zjfao__jzu[cnpy__qlvma] = arr[cgh__lcjye]
                phs__cokmq = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    xuop__gifim, cgh__lcjye)
                bodo.libs.int_arr_ext.set_bit_to_arr(cehlr__zlysv,
                    cnpy__qlvma, phs__cokmq)
            return zjfao__jzu
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            oxkkf__lolti = len(arr)
            zpmml__gyrx = numba.cpython.unicode._normalize_slice(ind,
                oxkkf__lolti)
            zpfg__jlq = np.arange(zpmml__gyrx.start, zpmml__gyrx.stop,
                zpmml__gyrx.step)
            return arr[zpfg__jlq]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            mmbnr__dev = get_offsets(A)
            xuop__gifim = get_null_bitmap(A)
            if idx == 0:
                mmbnr__dev[0] = 0
            n_items = len(val)
            pjthm__kxg = mmbnr__dev[idx] + n_items
            ensure_data_capacity(A, mmbnr__dev[idx], pjthm__kxg)
            gbg__recdu = get_data(A)
            mmbnr__dev[idx + 1] = mmbnr__dev[idx] + n_items
            gbg__recdu[mmbnr__dev[idx]:mmbnr__dev[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(xuop__gifim, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            zpmml__gyrx = numba.cpython.unicode._normalize_slice(idx, len(A))
            for tkn__riuk in range(zpmml__gyrx.start, zpmml__gyrx.stop,
                zpmml__gyrx.step):
                A[tkn__riuk] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            mmbnr__dev = get_offsets(A)
            xuop__gifim = get_null_bitmap(A)
            eziuz__bszeq = get_offsets(val)
            uetx__skplk = get_data(val)
            qfrk__zulk = get_null_bitmap(val)
            oxkkf__lolti = len(A)
            zpmml__gyrx = numba.cpython.unicode._normalize_slice(idx,
                oxkkf__lolti)
            ads__ljwj, wof__jto = zpmml__gyrx.start, zpmml__gyrx.stop
            assert zpmml__gyrx.step == 1
            if ads__ljwj == 0:
                mmbnr__dev[ads__ljwj] = 0
            ejhz__yko = mmbnr__dev[ads__ljwj]
            pjthm__kxg = ejhz__yko + len(uetx__skplk)
            ensure_data_capacity(A, ejhz__yko, pjthm__kxg)
            gbg__recdu = get_data(A)
            gbg__recdu[ejhz__yko:ejhz__yko + len(uetx__skplk)] = uetx__skplk
            mmbnr__dev[ads__ljwj:wof__jto + 1] = eziuz__bszeq + ejhz__yko
            uzg__alil = 0
            for tkn__riuk in range(ads__ljwj, wof__jto):
                phs__cokmq = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    qfrk__zulk, uzg__alil)
                bodo.libs.int_arr_ext.set_bit_to_arr(xuop__gifim, tkn__riuk,
                    phs__cokmq)
                uzg__alil += 1
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
