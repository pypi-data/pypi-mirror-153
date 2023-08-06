"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contingous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, decode_if_dict_array, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bwp__rauan = ArrayItemArrayType(char_arr_type)
        fxk__sjrjg = [('data', bwp__rauan)]
        models.StructModel.__init__(self, dmm, fe_type, fxk__sjrjg)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        vvls__tgatf, = args
        odo__qzmtg = context.make_helper(builder, string_array_type)
        odo__qzmtg.data = vvls__tgatf
        context.nrt.incref(builder, data_typ, vvls__tgatf)
        return odo__qzmtg._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    hsdev__lbfhj = c.context.insert_const_string(c.builder.module, 'pandas')
    sytnl__tvkgl = c.pyapi.import_module_noblock(hsdev__lbfhj)
    rqsl__hce = c.pyapi.call_method(sytnl__tvkgl, 'StringDtype', ())
    c.pyapi.decref(sytnl__tvkgl)
    return rqsl__hce


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        igjy__rkvu = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs
            )
        if igjy__rkvu is not None:
            return igjy__rkvu
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ikdax__jjcng = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ikdax__jjcng)
                for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ikdax__jjcng = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ikdax__jjcng)
                for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ikdax__jjcng = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ikdax__jjcng)
                for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    pgr__mlb = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    cde__vxmvx = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and cde__vxmvx or pgr__mlb and is_str_arr_type(rhs
        ):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    bnmb__yzh = context.make_helper(builder, arr_typ, arr_value)
    bwp__rauan = ArrayItemArrayType(char_arr_type)
    nlj__qhs = _get_array_item_arr_payload(context, builder, bwp__rauan,
        bnmb__yzh.data)
    return nlj__qhs


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return nlj__qhs.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        byude__qnlvk = context.make_helper(builder, offset_arr_type,
            nlj__qhs.offsets).data
        return _get_num_total_chars(builder, byude__qnlvk, nlj__qhs.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        uemyq__gmn = context.make_helper(builder, offset_arr_type, nlj__qhs
            .offsets)
        oeyt__bsnfq = context.make_helper(builder, offset_ctypes_type)
        oeyt__bsnfq.data = builder.bitcast(uemyq__gmn.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        oeyt__bsnfq.meminfo = uemyq__gmn.meminfo
        rqsl__hce = oeyt__bsnfq._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            rqsl__hce)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        vvls__tgatf = context.make_helper(builder, char_arr_type, nlj__qhs.data
            )
        oeyt__bsnfq = context.make_helper(builder, data_ctypes_type)
        oeyt__bsnfq.data = vvls__tgatf.data
        oeyt__bsnfq.meminfo = vvls__tgatf.meminfo
        rqsl__hce = oeyt__bsnfq._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, rqsl__hce)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        cun__ayrv, ind = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, cun__ayrv,
            sig.args[0])
        vvls__tgatf = context.make_helper(builder, char_arr_type, nlj__qhs.data
            )
        oeyt__bsnfq = context.make_helper(builder, data_ctypes_type)
        oeyt__bsnfq.data = builder.gep(vvls__tgatf.data, [ind])
        oeyt__bsnfq.meminfo = vvls__tgatf.meminfo
        rqsl__hce = oeyt__bsnfq._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, rqsl__hce)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        nvug__yqt, jvcg__btcae, kxsx__gui, dptkz__uygm = args
        qdtyk__fkibw = builder.bitcast(builder.gep(nvug__yqt, [jvcg__btcae]
            ), lir.IntType(8).as_pointer())
        ouwms__akyjk = builder.bitcast(builder.gep(kxsx__gui, [dptkz__uygm]
            ), lir.IntType(8).as_pointer())
        jdkf__talvg = builder.load(ouwms__akyjk)
        builder.store(jdkf__talvg, qdtyk__fkibw)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ownj__syx = context.make_helper(builder, null_bitmap_arr_type,
            nlj__qhs.null_bitmap)
        oeyt__bsnfq = context.make_helper(builder, data_ctypes_type)
        oeyt__bsnfq.data = ownj__syx.data
        oeyt__bsnfq.meminfo = ownj__syx.meminfo
        rqsl__hce = oeyt__bsnfq._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, rqsl__hce)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        byude__qnlvk = context.make_helper(builder, offset_arr_type,
            nlj__qhs.offsets).data
        return builder.load(builder.gep(byude__qnlvk, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, nlj__qhs.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        dnxxh__uleih, ind = args
        if in_bitmap_typ == data_ctypes_type:
            oeyt__bsnfq = context.make_helper(builder, data_ctypes_type,
                dnxxh__uleih)
            dnxxh__uleih = oeyt__bsnfq.data
        return builder.load(builder.gep(dnxxh__uleih, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        dnxxh__uleih, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            oeyt__bsnfq = context.make_helper(builder, data_ctypes_type,
                dnxxh__uleih)
            dnxxh__uleih = oeyt__bsnfq.data
        builder.store(val, builder.gep(dnxxh__uleih, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        gbt__rhnxe = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        xjt__enfoe = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        crm__eyi = context.make_helper(builder, offset_arr_type, gbt__rhnxe
            .offsets).data
        yuksv__cjdq = context.make_helper(builder, offset_arr_type,
            xjt__enfoe.offsets).data
        rjxk__qriqa = context.make_helper(builder, char_arr_type,
            gbt__rhnxe.data).data
        shany__flat = context.make_helper(builder, char_arr_type,
            xjt__enfoe.data).data
        exa__fbqp = context.make_helper(builder, null_bitmap_arr_type,
            gbt__rhnxe.null_bitmap).data
        iuct__yrc = context.make_helper(builder, null_bitmap_arr_type,
            xjt__enfoe.null_bitmap).data
        ayd__dge = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, yuksv__cjdq, crm__eyi, ayd__dge)
        cgutils.memcpy(builder, shany__flat, rjxk__qriqa, builder.load(
            builder.gep(crm__eyi, [ind])))
        szy__zwul = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        fmjc__gkkhu = builder.lshr(szy__zwul, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, iuct__yrc, exa__fbqp, fmjc__gkkhu)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        gbt__rhnxe = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        xjt__enfoe = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        crm__eyi = context.make_helper(builder, offset_arr_type, gbt__rhnxe
            .offsets).data
        rjxk__qriqa = context.make_helper(builder, char_arr_type,
            gbt__rhnxe.data).data
        shany__flat = context.make_helper(builder, char_arr_type,
            xjt__enfoe.data).data
        num_total_chars = _get_num_total_chars(builder, crm__eyi,
            gbt__rhnxe.n_arrays)
        cgutils.memcpy(builder, shany__flat, rjxk__qriqa, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        gbt__rhnxe = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        xjt__enfoe = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        crm__eyi = context.make_helper(builder, offset_arr_type, gbt__rhnxe
            .offsets).data
        yuksv__cjdq = context.make_helper(builder, offset_arr_type,
            xjt__enfoe.offsets).data
        exa__fbqp = context.make_helper(builder, null_bitmap_arr_type,
            gbt__rhnxe.null_bitmap).data
        ikdax__jjcng = gbt__rhnxe.n_arrays
        puoyg__phoa = context.get_constant(offset_type, 0)
        rcept__krq = cgutils.alloca_once_value(builder, puoyg__phoa)
        with cgutils.for_range(builder, ikdax__jjcng) as rorbc__mnrc:
            hfone__zmy = lower_is_na(context, builder, exa__fbqp,
                rorbc__mnrc.index)
            with cgutils.if_likely(builder, builder.not_(hfone__zmy)):
                bhw__mllmz = builder.load(builder.gep(crm__eyi, [
                    rorbc__mnrc.index]))
                hew__zaju = builder.load(rcept__krq)
                builder.store(bhw__mllmz, builder.gep(yuksv__cjdq, [hew__zaju])
                    )
                builder.store(builder.add(hew__zaju, lir.Constant(context.
                    get_value_type(offset_type), 1)), rcept__krq)
        hew__zaju = builder.load(rcept__krq)
        bhw__mllmz = builder.load(builder.gep(crm__eyi, [ikdax__jjcng]))
        builder.store(bhw__mllmz, builder.gep(yuksv__cjdq, [hew__zaju]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        cap__mpzcz, ind, str, shn__vonfy = args
        cap__mpzcz = context.make_array(sig.args[0])(context, builder,
            cap__mpzcz)
        pls__dkt = builder.gep(cap__mpzcz.data, [ind])
        cgutils.raw_memcpy(builder, pls__dkt, str, shn__vonfy, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        pls__dkt, ind, wnov__swq, shn__vonfy = args
        pls__dkt = builder.gep(pls__dkt, [ind])
        cgutils.raw_memcpy(builder, pls__dkt, wnov__swq, shn__vonfy, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    ksdu__fokde = np.int64(getitem_str_offset(A, i))
    rhsyr__nlf = np.int64(getitem_str_offset(A, i + 1))
    l = rhsyr__nlf - ksdu__fokde
    kfz__qgv = get_data_ptr_ind(A, ksdu__fokde)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(kfz__qgv, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    mjvx__llizb = getitem_str_offset(A, i)
    xwsvy__mluvt = getitem_str_offset(A, i + 1)
    zxi__sph = xwsvy__mluvt - mjvx__llizb
    ccf__jutx = getitem_str_offset(B, j)
    zvuz__loxzz = ccf__jutx + zxi__sph
    setitem_str_offset(B, j + 1, zvuz__loxzz)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if zxi__sph != 0:
        vvls__tgatf = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(vvls__tgatf, np.
            int64(ccf__jutx), np.int64(zvuz__loxzz))
        qvg__qjzhl = get_data_ptr(B).data
        rfh__dtf = get_data_ptr(A).data
        memcpy_region(qvg__qjzhl, ccf__jutx, rfh__dtf, mjvx__llizb, zxi__sph, 1
            )


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    ikdax__jjcng = len(str_arr)
    lfxo__pfvo = np.empty(ikdax__jjcng, np.bool_)
    for i in range(ikdax__jjcng):
        lfxo__pfvo[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return lfxo__pfvo


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            ikdax__jjcng = len(data)
            l = []
            for i in range(ikdax__jjcng):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        pqjb__efid = data.count
        qqgi__puysz = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(pqjb__efid)]
        if is_overload_true(str_null_bools):
            qqgi__puysz += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(pqjb__efid) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        tuacl__wugq = 'def f(data, str_null_bools=None):\n'
        tuacl__wugq += '  return ({}{})\n'.format(', '.join(qqgi__puysz), 
            ',' if pqjb__efid == 1 else '')
        snyqs__sklii = {}
        exec(tuacl__wugq, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, snyqs__sklii)
        nnc__wurxl = snyqs__sklii['f']
        return nnc__wurxl
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                ikdax__jjcng = len(list_data)
                for i in range(ikdax__jjcng):
                    wnov__swq = list_data[i]
                    str_arr[i] = wnov__swq
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                ikdax__jjcng = len(list_data)
                for i in range(ikdax__jjcng):
                    wnov__swq = list_data[i]
                    str_arr[i] = wnov__swq
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        pqjb__efid = str_arr.count
        vmz__vdhmn = 0
        tuacl__wugq = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(pqjb__efid):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                tuacl__wugq += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, pqjb__efid + vmz__vdhmn))
                vmz__vdhmn += 1
            else:
                tuacl__wugq += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        tuacl__wugq += '  return\n'
        snyqs__sklii = {}
        exec(tuacl__wugq, {'cp_str_list_to_array': cp_str_list_to_array},
            snyqs__sklii)
        uyi__lsouf = snyqs__sklii['f']
        return uyi__lsouf
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            ikdax__jjcng = len(str_list)
            str_arr = pre_alloc_string_array(ikdax__jjcng, -1)
            for i in range(ikdax__jjcng):
                wnov__swq = str_list[i]
                str_arr[i] = wnov__swq
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            ikdax__jjcng = len(A)
            cxk__qum = 0
            for i in range(ikdax__jjcng):
                wnov__swq = A[i]
                cxk__qum += get_utf8_size(wnov__swq)
            return cxk__qum
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        ikdax__jjcng = len(arr)
        n_chars = num_total_chars(arr)
        iyeu__vfep = pre_alloc_string_array(ikdax__jjcng, np.int64(n_chars))
        copy_str_arr_slice(iyeu__vfep, arr, ikdax__jjcng)
        return iyeu__vfep
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    tuacl__wugq = 'def f(in_seq):\n'
    tuacl__wugq += '    n_strs = len(in_seq)\n'
    tuacl__wugq += '    A = pre_alloc_string_array(n_strs, -1)\n'
    tuacl__wugq += '    return A\n'
    snyqs__sklii = {}
    exec(tuacl__wugq, {'pre_alloc_string_array': pre_alloc_string_array},
        snyqs__sklii)
    uzkys__olsu = snyqs__sklii['f']
    return uzkys__olsu


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        jpv__jer = 'pre_alloc_binary_array'
    else:
        jpv__jer = 'pre_alloc_string_array'
    tuacl__wugq = 'def f(in_seq):\n'
    tuacl__wugq += '    n_strs = len(in_seq)\n'
    tuacl__wugq += f'    A = {jpv__jer}(n_strs, -1)\n'
    tuacl__wugq += '    for i in range(n_strs):\n'
    tuacl__wugq += '        A[i] = in_seq[i]\n'
    tuacl__wugq += '    return A\n'
    snyqs__sklii = {}
    exec(tuacl__wugq, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, snyqs__sklii)
    uzkys__olsu = snyqs__sklii['f']
    return uzkys__olsu


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        wxxw__lvotl = builder.add(nlj__qhs.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        yfvy__kkn = builder.lshr(lir.Constant(lir.IntType(64), offset_type.
            bitwidth), lir.Constant(lir.IntType(64), 3))
        fmjc__gkkhu = builder.mul(wxxw__lvotl, yfvy__kkn)
        ayiuj__ddha = context.make_array(offset_arr_type)(context, builder,
            nlj__qhs.offsets).data
        cgutils.memset(builder, ayiuj__ddha, fmjc__gkkhu, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        zmhhp__qizbr = nlj__qhs.n_arrays
        fmjc__gkkhu = builder.lshr(builder.add(zmhhp__qizbr, lir.Constant(
            lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        pbfgo__csj = context.make_array(null_bitmap_arr_type)(context,
            builder, nlj__qhs.null_bitmap).data
        cgutils.memset(builder, pbfgo__csj, fmjc__gkkhu, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    imiv__czi = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        mql__urz = len(len_arr)
        for i in range(mql__urz):
            offsets[i] = imiv__czi
            imiv__czi += len_arr[i]
        offsets[mql__urz] = imiv__czi
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    undn__aucl = i // 8
    yjb__bjbdz = getitem_str_bitmap(bits, undn__aucl)
    yjb__bjbdz ^= np.uint8(-np.uint8(bit_is_set) ^ yjb__bjbdz) & kBitmask[i % 8
        ]
    setitem_str_bitmap(bits, undn__aucl, yjb__bjbdz)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    nql__mzj = get_null_bitmap_ptr(out_str_arr)
    ywiyq__pzowy = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        awwf__wlj = get_bit_bitmap(ywiyq__pzowy, j)
        set_bit_to(nql__mzj, out_start + j, awwf__wlj)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, cun__ayrv, sxhwy__eenm, rio__osv = args
        gbt__rhnxe = _get_str_binary_arr_payload(context, builder,
            cun__ayrv, string_array_type)
        xjt__enfoe = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        crm__eyi = context.make_helper(builder, offset_arr_type, gbt__rhnxe
            .offsets).data
        yuksv__cjdq = context.make_helper(builder, offset_arr_type,
            xjt__enfoe.offsets).data
        rjxk__qriqa = context.make_helper(builder, char_arr_type,
            gbt__rhnxe.data).data
        shany__flat = context.make_helper(builder, char_arr_type,
            xjt__enfoe.data).data
        num_total_chars = _get_num_total_chars(builder, crm__eyi,
            gbt__rhnxe.n_arrays)
        rmpo__ohon = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        llc__uyrgi = cgutils.get_or_insert_function(builder.module,
            rmpo__ohon, name='set_string_array_range')
        builder.call(llc__uyrgi, [yuksv__cjdq, shany__flat, crm__eyi,
            rjxk__qriqa, sxhwy__eenm, rio__osv, gbt__rhnxe.n_arrays,
            num_total_chars])
        kpk__amw = context.typing_context.resolve_value_type(copy_nulls_range)
        reoh__esdt = kpk__amw.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        xcw__muu = context.get_function(kpk__amw, reoh__esdt)
        xcw__muu(builder, (out_arr, cun__ayrv, sxhwy__eenm))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    nnv__cbof = c.context.make_helper(c.builder, typ, val)
    bwp__rauan = ArrayItemArrayType(char_arr_type)
    nlj__qhs = _get_array_item_arr_payload(c.context, c.builder, bwp__rauan,
        nnv__cbof.data)
    zeh__ufn = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    jcthv__uqs = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        jcthv__uqs = 'pd_array_from_string_array'
    rmpo__ohon = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    ziqt__libq = cgutils.get_or_insert_function(c.builder.module,
        rmpo__ohon, name=jcthv__uqs)
    byude__qnlvk = c.context.make_array(offset_arr_type)(c.context, c.
        builder, nlj__qhs.offsets).data
    kfz__qgv = c.context.make_array(char_arr_type)(c.context, c.builder,
        nlj__qhs.data).data
    pbfgo__csj = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, nlj__qhs.null_bitmap).data
    arr = c.builder.call(ziqt__libq, [nlj__qhs.n_arrays, byude__qnlvk,
        kfz__qgv, pbfgo__csj, zeh__ufn])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        pbfgo__csj = context.make_array(null_bitmap_arr_type)(context,
            builder, nlj__qhs.null_bitmap).data
        aial__oyngq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        zwifk__fcaex = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        yjb__bjbdz = builder.load(builder.gep(pbfgo__csj, [aial__oyngq],
            inbounds=True))
        plt__pstpu = lir.ArrayType(lir.IntType(8), 8)
        qfbw__mxr = cgutils.alloca_once_value(builder, lir.Constant(
            plt__pstpu, (1, 2, 4, 8, 16, 32, 64, 128)))
        pjejm__pci = builder.load(builder.gep(qfbw__mxr, [lir.Constant(lir.
            IntType(64), 0), zwifk__fcaex], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(yjb__bjbdz,
            pjejm__pci), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        aial__oyngq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        zwifk__fcaex = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        pbfgo__csj = context.make_array(null_bitmap_arr_type)(context,
            builder, nlj__qhs.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, nlj__qhs.
            offsets).data
        adu__kihz = builder.gep(pbfgo__csj, [aial__oyngq], inbounds=True)
        yjb__bjbdz = builder.load(adu__kihz)
        plt__pstpu = lir.ArrayType(lir.IntType(8), 8)
        qfbw__mxr = cgutils.alloca_once_value(builder, lir.Constant(
            plt__pstpu, (1, 2, 4, 8, 16, 32, 64, 128)))
        pjejm__pci = builder.load(builder.gep(qfbw__mxr, [lir.Constant(lir.
            IntType(64), 0), zwifk__fcaex], inbounds=True))
        pjejm__pci = builder.xor(pjejm__pci, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(yjb__bjbdz, pjejm__pci), adu__kihz)
        if str_arr_typ == string_array_type:
            bfx__cht = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            zpot__fhy = builder.icmp_unsigned('!=', bfx__cht, nlj__qhs.n_arrays
                )
            with builder.if_then(zpot__fhy):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [bfx__cht]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        aial__oyngq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        zwifk__fcaex = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        pbfgo__csj = context.make_array(null_bitmap_arr_type)(context,
            builder, nlj__qhs.null_bitmap).data
        adu__kihz = builder.gep(pbfgo__csj, [aial__oyngq], inbounds=True)
        yjb__bjbdz = builder.load(adu__kihz)
        plt__pstpu = lir.ArrayType(lir.IntType(8), 8)
        qfbw__mxr = cgutils.alloca_once_value(builder, lir.Constant(
            plt__pstpu, (1, 2, 4, 8, 16, 32, 64, 128)))
        pjejm__pci = builder.load(builder.gep(qfbw__mxr, [lir.Constant(lir.
            IntType(64), 0), zwifk__fcaex], inbounds=True))
        builder.store(builder.or_(yjb__bjbdz, pjejm__pci), adu__kihz)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        fmjc__gkkhu = builder.udiv(builder.add(nlj__qhs.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        pbfgo__csj = context.make_array(null_bitmap_arr_type)(context,
            builder, nlj__qhs.null_bitmap).data
        cgutils.memset(builder, pbfgo__csj, fmjc__gkkhu, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    yio__jfal = context.make_helper(builder, string_array_type, str_arr)
    bwp__rauan = ArrayItemArrayType(char_arr_type)
    srls__lzew = context.make_helper(builder, bwp__rauan, yio__jfal.data)
    ffx__poxf = ArrayItemArrayPayloadType(bwp__rauan)
    lovwv__tsfs = context.nrt.meminfo_data(builder, srls__lzew.meminfo)
    sfkv__xktav = builder.bitcast(lovwv__tsfs, context.get_value_type(
        ffx__poxf).as_pointer())
    return sfkv__xktav


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        pmc__ldj, qwnb__uag = args
        omp__aylo = _get_str_binary_arr_data_payload_ptr(context, builder,
            qwnb__uag)
        etay__zaaj = _get_str_binary_arr_data_payload_ptr(context, builder,
            pmc__ldj)
        nwkb__kwht = _get_str_binary_arr_payload(context, builder,
            qwnb__uag, sig.args[1])
        kpn__xgjau = _get_str_binary_arr_payload(context, builder, pmc__ldj,
            sig.args[0])
        context.nrt.incref(builder, char_arr_type, nwkb__kwht.data)
        context.nrt.incref(builder, offset_arr_type, nwkb__kwht.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, nwkb__kwht.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, kpn__xgjau.data)
        context.nrt.decref(builder, offset_arr_type, kpn__xgjau.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, kpn__xgjau.
            null_bitmap)
        builder.store(builder.load(omp__aylo), etay__zaaj)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        ikdax__jjcng = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return ikdax__jjcng
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, pls__dkt, whd__kwj = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, nlj__qhs.
            offsets).data
        data = context.make_helper(builder, char_arr_type, nlj__qhs.data).data
        rmpo__ohon = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        ixkd__ihvx = cgutils.get_or_insert_function(builder.module,
            rmpo__ohon, name='setitem_string_array')
        kva__iidgl = context.get_constant(types.int32, -1)
        hwq__bjqy = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, nlj__qhs.
            n_arrays)
        builder.call(ixkd__ihvx, [offsets, data, num_total_chars, builder.
            extract_value(pls__dkt, 0), whd__kwj, kva__iidgl, hwq__bjqy, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    rmpo__ohon = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    dumdy__cvmg = cgutils.get_or_insert_function(builder.module, rmpo__ohon,
        name='is_na')
    return builder.call(dumdy__cvmg, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        qdtyk__fkibw, ouwms__akyjk, pqjb__efid, taky__wwegw = args
        cgutils.raw_memcpy(builder, qdtyk__fkibw, ouwms__akyjk, pqjb__efid,
            taky__wwegw)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        siuux__uhm, yyyc__peyt = unicode_to_utf8_and_len(val)
        vsskg__lsqd = getitem_str_offset(A, ind)
        pphgw__cfr = getitem_str_offset(A, ind + 1)
        rtmmc__cxztj = pphgw__cfr - vsskg__lsqd
        if rtmmc__cxztj != yyyc__peyt:
            return False
        pls__dkt = get_data_ptr_ind(A, vsskg__lsqd)
        return memcmp(pls__dkt, siuux__uhm, yyyc__peyt) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        vsskg__lsqd = getitem_str_offset(A, ind)
        rtmmc__cxztj = bodo.libs.str_ext.int_to_str_len(val)
        nxim__nxune = vsskg__lsqd + rtmmc__cxztj
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            vsskg__lsqd, nxim__nxune)
        pls__dkt = get_data_ptr_ind(A, vsskg__lsqd)
        inplace_int64_to_str(pls__dkt, rtmmc__cxztj, val)
        setitem_str_offset(A, ind + 1, vsskg__lsqd + rtmmc__cxztj)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        pls__dkt, = args
        ygjgb__ubjdz = context.insert_const_string(builder.module, '<NA>')
        eym__gblw = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, pls__dkt, ygjgb__ubjdz, eym__gblw, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    zsza__rts = len('<NA>')

    def impl(A, ind):
        vsskg__lsqd = getitem_str_offset(A, ind)
        nxim__nxune = vsskg__lsqd + zsza__rts
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            vsskg__lsqd, nxim__nxune)
        pls__dkt = get_data_ptr_ind(A, vsskg__lsqd)
        inplace_set_NA_str(pls__dkt)
        setitem_str_offset(A, ind + 1, vsskg__lsqd + zsza__rts)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            vsskg__lsqd = getitem_str_offset(A, ind)
            pphgw__cfr = getitem_str_offset(A, ind + 1)
            whd__kwj = pphgw__cfr - vsskg__lsqd
            pls__dkt = get_data_ptr_ind(A, vsskg__lsqd)
            njyag__wvk = decode_utf8(pls__dkt, whd__kwj)
            return njyag__wvk
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            ikdax__jjcng = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(ikdax__jjcng):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            qvg__qjzhl = get_data_ptr(out_arr).data
            rfh__dtf = get_data_ptr(A).data
            vmz__vdhmn = 0
            hew__zaju = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(ikdax__jjcng):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    xcnr__yec = get_str_arr_item_length(A, i)
                    if xcnr__yec == 1:
                        copy_single_char(qvg__qjzhl, hew__zaju, rfh__dtf,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(qvg__qjzhl, hew__zaju, rfh__dtf,
                            getitem_str_offset(A, i), xcnr__yec, 1)
                    hew__zaju += xcnr__yec
                    setitem_str_offset(out_arr, vmz__vdhmn + 1, hew__zaju)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, vmz__vdhmn)
                    else:
                        str_arr_set_not_na(out_arr, vmz__vdhmn)
                    vmz__vdhmn += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ikdax__jjcng = len(ind)
            out_arr = pre_alloc_string_array(ikdax__jjcng, -1)
            vmz__vdhmn = 0
            for i in range(ikdax__jjcng):
                wnov__swq = A[ind[i]]
                out_arr[vmz__vdhmn] = wnov__swq
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, vmz__vdhmn)
                vmz__vdhmn += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            ikdax__jjcng = len(A)
            nnbfj__xwid = numba.cpython.unicode._normalize_slice(ind,
                ikdax__jjcng)
            tmuq__cccik = numba.cpython.unicode._slice_span(nnbfj__xwid)
            if nnbfj__xwid.step == 1:
                vsskg__lsqd = getitem_str_offset(A, nnbfj__xwid.start)
                pphgw__cfr = getitem_str_offset(A, nnbfj__xwid.stop)
                n_chars = pphgw__cfr - vsskg__lsqd
                iyeu__vfep = pre_alloc_string_array(tmuq__cccik, np.int64(
                    n_chars))
                for i in range(tmuq__cccik):
                    iyeu__vfep[i] = A[nnbfj__xwid.start + i]
                    if str_arr_is_na(A, nnbfj__xwid.start + i):
                        str_arr_set_na(iyeu__vfep, i)
                return iyeu__vfep
            else:
                iyeu__vfep = pre_alloc_string_array(tmuq__cccik, -1)
                for i in range(tmuq__cccik):
                    iyeu__vfep[i] = A[nnbfj__xwid.start + i * nnbfj__xwid.step]
                    if str_arr_is_na(A, nnbfj__xwid.start + i * nnbfj__xwid
                        .step):
                        str_arr_set_na(iyeu__vfep, i)
                return iyeu__vfep
        return str_arr_slice_impl
    raise BodoError(
        f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    qdjv__nngw = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(qdjv__nngw)
        kzcf__qzj = 4

        def impl_scalar(A, idx, val):
            jxzy__tsh = (val._length if val._is_ascii else kzcf__qzj * val.
                _length)
            vvls__tgatf = A._data
            vsskg__lsqd = np.int64(getitem_str_offset(A, idx))
            nxim__nxune = vsskg__lsqd + jxzy__tsh
            bodo.libs.array_item_arr_ext.ensure_data_capacity(vvls__tgatf,
                vsskg__lsqd, nxim__nxune)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                nxim__nxune, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                nnbfj__xwid = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                ksdu__fokde = nnbfj__xwid.start
                vvls__tgatf = A._data
                vsskg__lsqd = np.int64(getitem_str_offset(A, ksdu__fokde))
                nxim__nxune = vsskg__lsqd + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(vvls__tgatf,
                    vsskg__lsqd, nxim__nxune)
                set_string_array_range(A, val, ksdu__fokde, vsskg__lsqd)
                qhnh__dpf = 0
                for i in range(nnbfj__xwid.start, nnbfj__xwid.stop,
                    nnbfj__xwid.step):
                    if str_arr_is_na(val, qhnh__dpf):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    qhnh__dpf += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                dkmj__ssy = str_list_to_array(val)
                A[idx] = dkmj__ssy
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                nnbfj__xwid = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(nnbfj__xwid.start, nnbfj__xwid.stop,
                    nnbfj__xwid.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(qdjv__nngw)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                ikdax__jjcng = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(ikdax__jjcng, -1)
                for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                ikdax__jjcng = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(ikdax__jjcng, -1)
                eqr__ion = 0
                for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, eqr__ion):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, eqr__ion)
                        else:
                            out_arr[i] = str(val[eqr__ion])
                        eqr__ion += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(qdjv__nngw)
    raise BodoError(qdjv__nngw)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    ynyg__cmskm = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(ynyg__cmskm, (types.Float, types.Integer)
        ) and ynyg__cmskm not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(ynyg__cmskm, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ikdax__jjcng = len(A)
            B = np.empty(ikdax__jjcng, ynyg__cmskm)
            for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif ynyg__cmskm == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ikdax__jjcng = len(A)
            B = np.empty(ikdax__jjcng, ynyg__cmskm)
            for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif ynyg__cmskm == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ikdax__jjcng = len(A)
            B = np.empty(ikdax__jjcng, ynyg__cmskm)
            for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ikdax__jjcng = len(A)
            B = np.empty(ikdax__jjcng, ynyg__cmskm)
            for i in numba.parfors.parfor.internal_prange(ikdax__jjcng):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        pls__dkt, whd__kwj = args
        asn__utoj = context.get_python_api(builder)
        sbixq__pdv = asn__utoj.string_from_string_and_size(pls__dkt, whd__kwj)
        ewnb__fvry = asn__utoj.to_native_value(string_type, sbixq__pdv).value
        zup__bxml = cgutils.create_struct_proxy(string_type)(context,
            builder, ewnb__fvry)
        zup__bxml.hash = zup__bxml.hash.type(-1)
        asn__utoj.decref(sbixq__pdv)
        return zup__bxml._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    str_arr = decode_if_dict_array(str_arr)
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        pylm__abee, arr, ind, hesj__bsf = args
        nlj__qhs = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, nlj__qhs.
            offsets).data
        data = context.make_helper(builder, char_arr_type, nlj__qhs.data).data
        rmpo__ohon = lir.FunctionType(lir.IntType(32), [pylm__abee.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        bwc__ytcs = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            bwc__ytcs = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        wgcu__cduol = cgutils.get_or_insert_function(builder.module,
            rmpo__ohon, bwc__ytcs)
        return builder.call(wgcu__cduol, [pylm__abee, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    zeh__ufn = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    rmpo__ohon = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(32)])
    zykgp__ajcq = cgutils.get_or_insert_function(c.builder.module,
        rmpo__ohon, name='string_array_from_sequence')
    tqwnx__wuz = c.builder.call(zykgp__ajcq, [val, zeh__ufn])
    bwp__rauan = ArrayItemArrayType(char_arr_type)
    srls__lzew = c.context.make_helper(c.builder, bwp__rauan)
    srls__lzew.meminfo = tqwnx__wuz
    yio__jfal = c.context.make_helper(c.builder, typ)
    vvls__tgatf = srls__lzew._getvalue()
    yio__jfal.data = vvls__tgatf
    esg__zhc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yio__jfal._getvalue(), is_error=esg__zhc)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    ikdax__jjcng = len(pyval)
    hew__zaju = 0
    updkh__onhh = np.empty(ikdax__jjcng + 1, np_offset_type)
    bvn__sce = []
    tie__wys = np.empty(ikdax__jjcng + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        updkh__onhh[i] = hew__zaju
        olx__xjbl = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(tie__wys, i, int(not olx__xjbl))
        if olx__xjbl:
            continue
        eqrc__wqbd = list(s.encode()) if isinstance(s, str) else list(s)
        bvn__sce.extend(eqrc__wqbd)
        hew__zaju += len(eqrc__wqbd)
    updkh__onhh[ikdax__jjcng] = hew__zaju
    cfhpq__clco = np.array(bvn__sce, np.uint8)
    wvf__wnxw = context.get_constant(types.int64, ikdax__jjcng)
    nid__pfddh = context.get_constant_generic(builder, char_arr_type,
        cfhpq__clco)
    qcp__jkr = context.get_constant_generic(builder, offset_arr_type,
        updkh__onhh)
    jluv__cnfg = context.get_constant_generic(builder, null_bitmap_arr_type,
        tie__wys)
    nlj__qhs = lir.Constant.literal_struct([wvf__wnxw, nid__pfddh, qcp__jkr,
        jluv__cnfg])
    nlj__qhs = cgutils.global_constant(builder, '.const.payload', nlj__qhs
        ).bitcast(cgutils.voidptr_t)
    ifuqk__edf = context.get_constant(types.int64, -1)
    pxp__pxd = context.get_constant_null(types.voidptr)
    pntdl__gjoh = lir.Constant.literal_struct([ifuqk__edf, pxp__pxd,
        pxp__pxd, nlj__qhs, ifuqk__edf])
    pntdl__gjoh = cgutils.global_constant(builder, '.const.meminfo',
        pntdl__gjoh).bitcast(cgutils.voidptr_t)
    vvls__tgatf = lir.Constant.literal_struct([pntdl__gjoh])
    yio__jfal = lir.Constant.literal_struct([vvls__tgatf])
    return yio__jfal


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
