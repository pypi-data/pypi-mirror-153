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
        mfj__qqv = ArrayItemArrayType(char_arr_type)
        djiyn__oya = [('data', mfj__qqv)]
        models.StructModel.__init__(self, dmm, fe_type, djiyn__oya)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        wkm__nbv, = args
        fso__zrg = context.make_helper(builder, string_array_type)
        fso__zrg.data = wkm__nbv
        context.nrt.incref(builder, data_typ, wkm__nbv)
        return fso__zrg._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    lqctz__ybvj = c.context.insert_const_string(c.builder.module, 'pandas')
    borp__qox = c.pyapi.import_module_noblock(lqctz__ybvj)
    kkz__ufqj = c.pyapi.call_method(borp__qox, 'StringDtype', ())
    c.pyapi.decref(borp__qox)
    return kkz__ufqj


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        gbh__nkv = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs)
        if gbh__nkv is not None:
            return gbh__nkv
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xwzbf__zko = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(xwzbf__zko)
                for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
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
                xwzbf__zko = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(xwzbf__zko)
                for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
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
                xwzbf__zko = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(xwzbf__zko)
                for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
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
    meq__adx = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    tvu__hoxl = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and tvu__hoxl or meq__adx and is_str_arr_type(rhs):

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
    dgwdu__ihtp = context.make_helper(builder, arr_typ, arr_value)
    mfj__qqv = ArrayItemArrayType(char_arr_type)
    iftal__pbeyg = _get_array_item_arr_payload(context, builder, mfj__qqv,
        dgwdu__ihtp.data)
    return iftal__pbeyg


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return iftal__pbeyg.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gyxc__wmfbg = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets).data
        return _get_num_total_chars(builder, gyxc__wmfbg, iftal__pbeyg.n_arrays
            )
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        dhjt__nyrg = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets)
        mka__pnnfd = context.make_helper(builder, offset_ctypes_type)
        mka__pnnfd.data = builder.bitcast(dhjt__nyrg.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        mka__pnnfd.meminfo = dhjt__nyrg.meminfo
        kkz__ufqj = mka__pnnfd._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            kkz__ufqj)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        wkm__nbv = context.make_helper(builder, char_arr_type, iftal__pbeyg
            .data)
        mka__pnnfd = context.make_helper(builder, data_ctypes_type)
        mka__pnnfd.data = wkm__nbv.data
        mka__pnnfd.meminfo = wkm__nbv.meminfo
        kkz__ufqj = mka__pnnfd._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kkz__ufqj)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        jmh__ewfdb, ind = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            jmh__ewfdb, sig.args[0])
        wkm__nbv = context.make_helper(builder, char_arr_type, iftal__pbeyg
            .data)
        mka__pnnfd = context.make_helper(builder, data_ctypes_type)
        mka__pnnfd.data = builder.gep(wkm__nbv.data, [ind])
        mka__pnnfd.meminfo = wkm__nbv.meminfo
        kkz__ufqj = mka__pnnfd._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kkz__ufqj)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        kpwmh__pgxac, lywd__ljlho, bkmm__mphf, avkg__obz = args
        lmb__lpusl = builder.bitcast(builder.gep(kpwmh__pgxac, [lywd__ljlho
            ]), lir.IntType(8).as_pointer())
        qcg__rdzcy = builder.bitcast(builder.gep(bkmm__mphf, [avkg__obz]),
            lir.IntType(8).as_pointer())
        bpx__ydxo = builder.load(qcg__rdzcy)
        builder.store(bpx__ydxo, lmb__lpusl)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        lwzzs__vjo = context.make_helper(builder, null_bitmap_arr_type,
            iftal__pbeyg.null_bitmap)
        mka__pnnfd = context.make_helper(builder, data_ctypes_type)
        mka__pnnfd.data = lwzzs__vjo.data
        mka__pnnfd.meminfo = lwzzs__vjo.meminfo
        kkz__ufqj = mka__pnnfd._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kkz__ufqj)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gyxc__wmfbg = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets).data
        return builder.load(builder.gep(gyxc__wmfbg, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        ily__jaon, ind = args
        if in_bitmap_typ == data_ctypes_type:
            mka__pnnfd = context.make_helper(builder, data_ctypes_type,
                ily__jaon)
            ily__jaon = mka__pnnfd.data
        return builder.load(builder.gep(ily__jaon, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        ily__jaon, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            mka__pnnfd = context.make_helper(builder, data_ctypes_type,
                ily__jaon)
            ily__jaon = mka__pnnfd.data
        builder.store(val, builder.gep(ily__jaon, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        miibj__npiv = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ntaob__jejl = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        dvyk__hbjer = context.make_helper(builder, offset_arr_type,
            miibj__npiv.offsets).data
        utbc__ehcez = context.make_helper(builder, offset_arr_type,
            ntaob__jejl.offsets).data
        advz__grli = context.make_helper(builder, char_arr_type,
            miibj__npiv.data).data
        iuhkj__rfqv = context.make_helper(builder, char_arr_type,
            ntaob__jejl.data).data
        oblvt__olvv = context.make_helper(builder, null_bitmap_arr_type,
            miibj__npiv.null_bitmap).data
        hfy__boxob = context.make_helper(builder, null_bitmap_arr_type,
            ntaob__jejl.null_bitmap).data
        zin__fww = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, utbc__ehcez, dvyk__hbjer, zin__fww)
        cgutils.memcpy(builder, iuhkj__rfqv, advz__grli, builder.load(
            builder.gep(dvyk__hbjer, [ind])))
        amb__ejj = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        zibpg__ipjag = builder.lshr(amb__ejj, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, hfy__boxob, oblvt__olvv, zibpg__ipjag)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        miibj__npiv = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ntaob__jejl = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        dvyk__hbjer = context.make_helper(builder, offset_arr_type,
            miibj__npiv.offsets).data
        advz__grli = context.make_helper(builder, char_arr_type,
            miibj__npiv.data).data
        iuhkj__rfqv = context.make_helper(builder, char_arr_type,
            ntaob__jejl.data).data
        num_total_chars = _get_num_total_chars(builder, dvyk__hbjer,
            miibj__npiv.n_arrays)
        cgutils.memcpy(builder, iuhkj__rfqv, advz__grli, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        miibj__npiv = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ntaob__jejl = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        dvyk__hbjer = context.make_helper(builder, offset_arr_type,
            miibj__npiv.offsets).data
        utbc__ehcez = context.make_helper(builder, offset_arr_type,
            ntaob__jejl.offsets).data
        oblvt__olvv = context.make_helper(builder, null_bitmap_arr_type,
            miibj__npiv.null_bitmap).data
        xwzbf__zko = miibj__npiv.n_arrays
        yvp__ptnga = context.get_constant(offset_type, 0)
        kxt__irxz = cgutils.alloca_once_value(builder, yvp__ptnga)
        with cgutils.for_range(builder, xwzbf__zko) as ype__vid:
            egd__hmpoz = lower_is_na(context, builder, oblvt__olvv,
                ype__vid.index)
            with cgutils.if_likely(builder, builder.not_(egd__hmpoz)):
                fbbm__lqs = builder.load(builder.gep(dvyk__hbjer, [ype__vid
                    .index]))
                xtnu__tveg = builder.load(kxt__irxz)
                builder.store(fbbm__lqs, builder.gep(utbc__ehcez, [xtnu__tveg])
                    )
                builder.store(builder.add(xtnu__tveg, lir.Constant(context.
                    get_value_type(offset_type), 1)), kxt__irxz)
        xtnu__tveg = builder.load(kxt__irxz)
        fbbm__lqs = builder.load(builder.gep(dvyk__hbjer, [xwzbf__zko]))
        builder.store(fbbm__lqs, builder.gep(utbc__ehcez, [xtnu__tveg]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        efgg__odgnz, ind, str, kncsa__tim = args
        efgg__odgnz = context.make_array(sig.args[0])(context, builder,
            efgg__odgnz)
        fuoby__zuf = builder.gep(efgg__odgnz.data, [ind])
        cgutils.raw_memcpy(builder, fuoby__zuf, str, kncsa__tim, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        fuoby__zuf, ind, huw__kzy, kncsa__tim = args
        fuoby__zuf = builder.gep(fuoby__zuf, [ind])
        cgutils.raw_memcpy(builder, fuoby__zuf, huw__kzy, kncsa__tim, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    fucl__hxw = np.int64(getitem_str_offset(A, i))
    phf__gikxs = np.int64(getitem_str_offset(A, i + 1))
    l = phf__gikxs - fucl__hxw
    ijvss__opgv = get_data_ptr_ind(A, fucl__hxw)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(ijvss__opgv, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    ilv__fkwk = getitem_str_offset(A, i)
    nes__gxtpy = getitem_str_offset(A, i + 1)
    iqdyo__syros = nes__gxtpy - ilv__fkwk
    auv__vywi = getitem_str_offset(B, j)
    vhip__evj = auv__vywi + iqdyo__syros
    setitem_str_offset(B, j + 1, vhip__evj)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if iqdyo__syros != 0:
        wkm__nbv = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(wkm__nbv, np.
            int64(auv__vywi), np.int64(vhip__evj))
        rgb__krrep = get_data_ptr(B).data
        zetja__cqnu = get_data_ptr(A).data
        memcpy_region(rgb__krrep, auv__vywi, zetja__cqnu, ilv__fkwk,
            iqdyo__syros, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    xwzbf__zko = len(str_arr)
    bfqrq__ikyy = np.empty(xwzbf__zko, np.bool_)
    for i in range(xwzbf__zko):
        bfqrq__ikyy[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return bfqrq__ikyy


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            xwzbf__zko = len(data)
            l = []
            for i in range(xwzbf__zko):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        ihvx__jlcs = data.count
        eyocf__bfqvt = ['to_list_if_immutable_arr(data[{}])'.format(i) for
            i in range(ihvx__jlcs)]
        if is_overload_true(str_null_bools):
            eyocf__bfqvt += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(ihvx__jlcs) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        vtk__cxv = 'def f(data, str_null_bools=None):\n'
        vtk__cxv += '  return ({}{})\n'.format(', '.join(eyocf__bfqvt), ',' if
            ihvx__jlcs == 1 else '')
        agjmy__whikk = {}
        exec(vtk__cxv, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, agjmy__whikk)
        pdyjx__bgvpm = agjmy__whikk['f']
        return pdyjx__bgvpm
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                xwzbf__zko = len(list_data)
                for i in range(xwzbf__zko):
                    huw__kzy = list_data[i]
                    str_arr[i] = huw__kzy
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                xwzbf__zko = len(list_data)
                for i in range(xwzbf__zko):
                    huw__kzy = list_data[i]
                    str_arr[i] = huw__kzy
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        ihvx__jlcs = str_arr.count
        pzck__vay = 0
        vtk__cxv = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(ihvx__jlcs):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                vtk__cxv += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, ihvx__jlcs + pzck__vay))
                pzck__vay += 1
            else:
                vtk__cxv += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        vtk__cxv += '  return\n'
        agjmy__whikk = {}
        exec(vtk__cxv, {'cp_str_list_to_array': cp_str_list_to_array},
            agjmy__whikk)
        apok__rrf = agjmy__whikk['f']
        return apok__rrf
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            xwzbf__zko = len(str_list)
            str_arr = pre_alloc_string_array(xwzbf__zko, -1)
            for i in range(xwzbf__zko):
                huw__kzy = str_list[i]
                str_arr[i] = huw__kzy
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            xwzbf__zko = len(A)
            xubsq__fojy = 0
            for i in range(xwzbf__zko):
                huw__kzy = A[i]
                xubsq__fojy += get_utf8_size(huw__kzy)
            return xubsq__fojy
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        xwzbf__zko = len(arr)
        n_chars = num_total_chars(arr)
        cwkyc__vtod = pre_alloc_string_array(xwzbf__zko, np.int64(n_chars))
        copy_str_arr_slice(cwkyc__vtod, arr, xwzbf__zko)
        return cwkyc__vtod
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
    vtk__cxv = 'def f(in_seq):\n'
    vtk__cxv += '    n_strs = len(in_seq)\n'
    vtk__cxv += '    A = pre_alloc_string_array(n_strs, -1)\n'
    vtk__cxv += '    return A\n'
    agjmy__whikk = {}
    exec(vtk__cxv, {'pre_alloc_string_array': pre_alloc_string_array},
        agjmy__whikk)
    tqg__rfni = agjmy__whikk['f']
    return tqg__rfni


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        ukcfa__theaz = 'pre_alloc_binary_array'
    else:
        ukcfa__theaz = 'pre_alloc_string_array'
    vtk__cxv = 'def f(in_seq):\n'
    vtk__cxv += '    n_strs = len(in_seq)\n'
    vtk__cxv += f'    A = {ukcfa__theaz}(n_strs, -1)\n'
    vtk__cxv += '    for i in range(n_strs):\n'
    vtk__cxv += '        A[i] = in_seq[i]\n'
    vtk__cxv += '    return A\n'
    agjmy__whikk = {}
    exec(vtk__cxv, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, agjmy__whikk)
    tqg__rfni = agjmy__whikk['f']
    return tqg__rfni


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        jcb__gywgw = builder.add(iftal__pbeyg.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        hov__spp = builder.lshr(lir.Constant(lir.IntType(64), offset_type.
            bitwidth), lir.Constant(lir.IntType(64), 3))
        zibpg__ipjag = builder.mul(jcb__gywgw, hov__spp)
        ojnzf__ssmn = context.make_array(offset_arr_type)(context, builder,
            iftal__pbeyg.offsets).data
        cgutils.memset(builder, ojnzf__ssmn, zibpg__ipjag, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        zaecw__akzv = iftal__pbeyg.n_arrays
        zibpg__ipjag = builder.lshr(builder.add(zaecw__akzv, lir.Constant(
            lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        fepf__bwg = context.make_array(null_bitmap_arr_type)(context,
            builder, iftal__pbeyg.null_bitmap).data
        cgutils.memset(builder, fepf__bwg, zibpg__ipjag, 0)
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
    emrvz__qpfxd = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        cqkhz__ujxbc = len(len_arr)
        for i in range(cqkhz__ujxbc):
            offsets[i] = emrvz__qpfxd
            emrvz__qpfxd += len_arr[i]
        offsets[cqkhz__ujxbc] = emrvz__qpfxd
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    xrqby__hon = i // 8
    zvteh__ujsd = getitem_str_bitmap(bits, xrqby__hon)
    zvteh__ujsd ^= np.uint8(-np.uint8(bit_is_set) ^ zvteh__ujsd) & kBitmask[
        i % 8]
    setitem_str_bitmap(bits, xrqby__hon, zvteh__ujsd)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    ulzr__vtnx = get_null_bitmap_ptr(out_str_arr)
    xpm__rwtv = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        fvuts__hmuoo = get_bit_bitmap(xpm__rwtv, j)
        set_bit_to(ulzr__vtnx, out_start + j, fvuts__hmuoo)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, jmh__ewfdb, yfn__lca, ifot__hmh = args
        miibj__npiv = _get_str_binary_arr_payload(context, builder,
            jmh__ewfdb, string_array_type)
        ntaob__jejl = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        dvyk__hbjer = context.make_helper(builder, offset_arr_type,
            miibj__npiv.offsets).data
        utbc__ehcez = context.make_helper(builder, offset_arr_type,
            ntaob__jejl.offsets).data
        advz__grli = context.make_helper(builder, char_arr_type,
            miibj__npiv.data).data
        iuhkj__rfqv = context.make_helper(builder, char_arr_type,
            ntaob__jejl.data).data
        num_total_chars = _get_num_total_chars(builder, dvyk__hbjer,
            miibj__npiv.n_arrays)
        dfqwe__ebc = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        gijt__jug = cgutils.get_or_insert_function(builder.module,
            dfqwe__ebc, name='set_string_array_range')
        builder.call(gijt__jug, [utbc__ehcez, iuhkj__rfqv, dvyk__hbjer,
            advz__grli, yfn__lca, ifot__hmh, miibj__npiv.n_arrays,
            num_total_chars])
        rixk__imkr = context.typing_context.resolve_value_type(copy_nulls_range
            )
        xkxv__ltwl = rixk__imkr.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        lxai__ekhiq = context.get_function(rixk__imkr, xkxv__ltwl)
        lxai__ekhiq(builder, (out_arr, jmh__ewfdb, yfn__lca))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    qfre__ujzf = c.context.make_helper(c.builder, typ, val)
    mfj__qqv = ArrayItemArrayType(char_arr_type)
    iftal__pbeyg = _get_array_item_arr_payload(c.context, c.builder,
        mfj__qqv, qfre__ujzf.data)
    lerg__wxw = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    zshyg__elgue = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        zshyg__elgue = 'pd_array_from_string_array'
    dfqwe__ebc = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    mrtkw__eyyvo = cgutils.get_or_insert_function(c.builder.module,
        dfqwe__ebc, name=zshyg__elgue)
    gyxc__wmfbg = c.context.make_array(offset_arr_type)(c.context, c.
        builder, iftal__pbeyg.offsets).data
    ijvss__opgv = c.context.make_array(char_arr_type)(c.context, c.builder,
        iftal__pbeyg.data).data
    fepf__bwg = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, iftal__pbeyg.null_bitmap).data
    arr = c.builder.call(mrtkw__eyyvo, [iftal__pbeyg.n_arrays, gyxc__wmfbg,
        ijvss__opgv, fepf__bwg, lerg__wxw])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        fepf__bwg = context.make_array(null_bitmap_arr_type)(context,
            builder, iftal__pbeyg.null_bitmap).data
        bym__quyl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        vkm__xacmi = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        zvteh__ujsd = builder.load(builder.gep(fepf__bwg, [bym__quyl],
            inbounds=True))
        xhq__kcqli = lir.ArrayType(lir.IntType(8), 8)
        clv__bkydh = cgutils.alloca_once_value(builder, lir.Constant(
            xhq__kcqli, (1, 2, 4, 8, 16, 32, 64, 128)))
        ity__qaqcn = builder.load(builder.gep(clv__bkydh, [lir.Constant(lir
            .IntType(64), 0), vkm__xacmi], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(zvteh__ujsd,
            ity__qaqcn), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        bym__quyl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        vkm__xacmi = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        fepf__bwg = context.make_array(null_bitmap_arr_type)(context,
            builder, iftal__pbeyg.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets).data
        tbmr__yada = builder.gep(fepf__bwg, [bym__quyl], inbounds=True)
        zvteh__ujsd = builder.load(tbmr__yada)
        xhq__kcqli = lir.ArrayType(lir.IntType(8), 8)
        clv__bkydh = cgutils.alloca_once_value(builder, lir.Constant(
            xhq__kcqli, (1, 2, 4, 8, 16, 32, 64, 128)))
        ity__qaqcn = builder.load(builder.gep(clv__bkydh, [lir.Constant(lir
            .IntType(64), 0), vkm__xacmi], inbounds=True))
        ity__qaqcn = builder.xor(ity__qaqcn, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(zvteh__ujsd, ity__qaqcn), tbmr__yada)
        if str_arr_typ == string_array_type:
            oqnu__avan = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            neunf__egjy = builder.icmp_unsigned('!=', oqnu__avan,
                iftal__pbeyg.n_arrays)
            with builder.if_then(neunf__egjy):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [oqnu__avan]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        bym__quyl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        vkm__xacmi = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        fepf__bwg = context.make_array(null_bitmap_arr_type)(context,
            builder, iftal__pbeyg.null_bitmap).data
        tbmr__yada = builder.gep(fepf__bwg, [bym__quyl], inbounds=True)
        zvteh__ujsd = builder.load(tbmr__yada)
        xhq__kcqli = lir.ArrayType(lir.IntType(8), 8)
        clv__bkydh = cgutils.alloca_once_value(builder, lir.Constant(
            xhq__kcqli, (1, 2, 4, 8, 16, 32, 64, 128)))
        ity__qaqcn = builder.load(builder.gep(clv__bkydh, [lir.Constant(lir
            .IntType(64), 0), vkm__xacmi], inbounds=True))
        builder.store(builder.or_(zvteh__ujsd, ity__qaqcn), tbmr__yada)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        zibpg__ipjag = builder.udiv(builder.add(iftal__pbeyg.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        fepf__bwg = context.make_array(null_bitmap_arr_type)(context,
            builder, iftal__pbeyg.null_bitmap).data
        cgutils.memset(builder, fepf__bwg, zibpg__ipjag, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    kvy__lytee = context.make_helper(builder, string_array_type, str_arr)
    mfj__qqv = ArrayItemArrayType(char_arr_type)
    ziqnp__ouo = context.make_helper(builder, mfj__qqv, kvy__lytee.data)
    gyzv__kcot = ArrayItemArrayPayloadType(mfj__qqv)
    vdnbj__lfr = context.nrt.meminfo_data(builder, ziqnp__ouo.meminfo)
    kxggx__brty = builder.bitcast(vdnbj__lfr, context.get_value_type(
        gyzv__kcot).as_pointer())
    return kxggx__brty


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        tgkeo__kwlel, mjk__psvmi = args
        eum__jflfx = _get_str_binary_arr_data_payload_ptr(context, builder,
            mjk__psvmi)
        vjkzs__ior = _get_str_binary_arr_data_payload_ptr(context, builder,
            tgkeo__kwlel)
        pzwxa__ndhgl = _get_str_binary_arr_payload(context, builder,
            mjk__psvmi, sig.args[1])
        zgmiq__iowwb = _get_str_binary_arr_payload(context, builder,
            tgkeo__kwlel, sig.args[0])
        context.nrt.incref(builder, char_arr_type, pzwxa__ndhgl.data)
        context.nrt.incref(builder, offset_arr_type, pzwxa__ndhgl.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, pzwxa__ndhgl.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, zgmiq__iowwb.data)
        context.nrt.decref(builder, offset_arr_type, zgmiq__iowwb.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, zgmiq__iowwb.
            null_bitmap)
        builder.store(builder.load(eum__jflfx), vjkzs__ior)
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
        xwzbf__zko = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return xwzbf__zko
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, fuoby__zuf, zcjp__mbqv = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder, arr,
            sig.args[0])
        offsets = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets).data
        data = context.make_helper(builder, char_arr_type, iftal__pbeyg.data
            ).data
        dfqwe__ebc = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        sftw__cvft = cgutils.get_or_insert_function(builder.module,
            dfqwe__ebc, name='setitem_string_array')
        olxtu__vfnc = context.get_constant(types.int32, -1)
        amif__lkdr = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets,
            iftal__pbeyg.n_arrays)
        builder.call(sftw__cvft, [offsets, data, num_total_chars, builder.
            extract_value(fuoby__zuf, 0), zcjp__mbqv, olxtu__vfnc,
            amif__lkdr, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    dfqwe__ebc = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    dacyh__jibs = cgutils.get_or_insert_function(builder.module, dfqwe__ebc,
        name='is_na')
    return builder.call(dacyh__jibs, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        lmb__lpusl, qcg__rdzcy, ihvx__jlcs, xjlgm__dye = args
        cgutils.raw_memcpy(builder, lmb__lpusl, qcg__rdzcy, ihvx__jlcs,
            xjlgm__dye)
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
        bhb__nssvz, nqq__nees = unicode_to_utf8_and_len(val)
        pbw__cjb = getitem_str_offset(A, ind)
        xyxk__walyq = getitem_str_offset(A, ind + 1)
        wol__otcj = xyxk__walyq - pbw__cjb
        if wol__otcj != nqq__nees:
            return False
        fuoby__zuf = get_data_ptr_ind(A, pbw__cjb)
        return memcmp(fuoby__zuf, bhb__nssvz, nqq__nees) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        pbw__cjb = getitem_str_offset(A, ind)
        wol__otcj = bodo.libs.str_ext.int_to_str_len(val)
        hvxd__uvej = pbw__cjb + wol__otcj
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data, pbw__cjb,
            hvxd__uvej)
        fuoby__zuf = get_data_ptr_ind(A, pbw__cjb)
        inplace_int64_to_str(fuoby__zuf, wol__otcj, val)
        setitem_str_offset(A, ind + 1, pbw__cjb + wol__otcj)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        fuoby__zuf, = args
        pec__krc = context.insert_const_string(builder.module, '<NA>')
        brz__npfdm = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, fuoby__zuf, pec__krc, brz__npfdm, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    vvsnh__meklg = len('<NA>')

    def impl(A, ind):
        pbw__cjb = getitem_str_offset(A, ind)
        hvxd__uvej = pbw__cjb + vvsnh__meklg
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data, pbw__cjb,
            hvxd__uvej)
        fuoby__zuf = get_data_ptr_ind(A, pbw__cjb)
        inplace_set_NA_str(fuoby__zuf)
        setitem_str_offset(A, ind + 1, pbw__cjb + vvsnh__meklg)
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
            pbw__cjb = getitem_str_offset(A, ind)
            xyxk__walyq = getitem_str_offset(A, ind + 1)
            zcjp__mbqv = xyxk__walyq - pbw__cjb
            fuoby__zuf = get_data_ptr_ind(A, pbw__cjb)
            yuerr__spif = decode_utf8(fuoby__zuf, zcjp__mbqv)
            return yuerr__spif
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            xwzbf__zko = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(xwzbf__zko):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            rgb__krrep = get_data_ptr(out_arr).data
            zetja__cqnu = get_data_ptr(A).data
            pzck__vay = 0
            xtnu__tveg = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(xwzbf__zko):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    bgmw__hlvpd = get_str_arr_item_length(A, i)
                    if bgmw__hlvpd == 1:
                        copy_single_char(rgb__krrep, xtnu__tveg,
                            zetja__cqnu, getitem_str_offset(A, i))
                    else:
                        memcpy_region(rgb__krrep, xtnu__tveg, zetja__cqnu,
                            getitem_str_offset(A, i), bgmw__hlvpd, 1)
                    xtnu__tveg += bgmw__hlvpd
                    setitem_str_offset(out_arr, pzck__vay + 1, xtnu__tveg)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, pzck__vay)
                    else:
                        str_arr_set_not_na(out_arr, pzck__vay)
                    pzck__vay += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            xwzbf__zko = len(ind)
            out_arr = pre_alloc_string_array(xwzbf__zko, -1)
            pzck__vay = 0
            for i in range(xwzbf__zko):
                huw__kzy = A[ind[i]]
                out_arr[pzck__vay] = huw__kzy
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, pzck__vay)
                pzck__vay += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            xwzbf__zko = len(A)
            rmdo__oftgj = numba.cpython.unicode._normalize_slice(ind,
                xwzbf__zko)
            phrq__fplbs = numba.cpython.unicode._slice_span(rmdo__oftgj)
            if rmdo__oftgj.step == 1:
                pbw__cjb = getitem_str_offset(A, rmdo__oftgj.start)
                xyxk__walyq = getitem_str_offset(A, rmdo__oftgj.stop)
                n_chars = xyxk__walyq - pbw__cjb
                cwkyc__vtod = pre_alloc_string_array(phrq__fplbs, np.int64(
                    n_chars))
                for i in range(phrq__fplbs):
                    cwkyc__vtod[i] = A[rmdo__oftgj.start + i]
                    if str_arr_is_na(A, rmdo__oftgj.start + i):
                        str_arr_set_na(cwkyc__vtod, i)
                return cwkyc__vtod
            else:
                cwkyc__vtod = pre_alloc_string_array(phrq__fplbs, -1)
                for i in range(phrq__fplbs):
                    cwkyc__vtod[i] = A[rmdo__oftgj.start + i * rmdo__oftgj.step
                        ]
                    if str_arr_is_na(A, rmdo__oftgj.start + i * rmdo__oftgj
                        .step):
                        str_arr_set_na(cwkyc__vtod, i)
                return cwkyc__vtod
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
    xlxxg__lgmbl = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(xlxxg__lgmbl)
        uip__zevc = 4

        def impl_scalar(A, idx, val):
            wji__ewev = (val._length if val._is_ascii else uip__zevc * val.
                _length)
            wkm__nbv = A._data
            pbw__cjb = np.int64(getitem_str_offset(A, idx))
            hvxd__uvej = pbw__cjb + wji__ewev
            bodo.libs.array_item_arr_ext.ensure_data_capacity(wkm__nbv,
                pbw__cjb, hvxd__uvej)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                hvxd__uvej, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                rmdo__oftgj = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                fucl__hxw = rmdo__oftgj.start
                wkm__nbv = A._data
                pbw__cjb = np.int64(getitem_str_offset(A, fucl__hxw))
                hvxd__uvej = pbw__cjb + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(wkm__nbv,
                    pbw__cjb, hvxd__uvej)
                set_string_array_range(A, val, fucl__hxw, pbw__cjb)
                ucyzm__ewads = 0
                for i in range(rmdo__oftgj.start, rmdo__oftgj.stop,
                    rmdo__oftgj.step):
                    if str_arr_is_na(val, ucyzm__ewads):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    ucyzm__ewads += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                wtb__jsin = str_list_to_array(val)
                A[idx] = wtb__jsin
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                rmdo__oftgj = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(rmdo__oftgj.start, rmdo__oftgj.stop,
                    rmdo__oftgj.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(xlxxg__lgmbl)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                xwzbf__zko = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(xwzbf__zko, -1)
                for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
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
                xwzbf__zko = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(xwzbf__zko, -1)
                jfqd__zbx = 0
                for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, jfqd__zbx):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, jfqd__zbx)
                        else:
                            out_arr[i] = str(val[jfqd__zbx])
                        jfqd__zbx += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(xlxxg__lgmbl)
    raise BodoError(xlxxg__lgmbl)


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
    hyx__mis = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(hyx__mis, (types.Float, types.Integer)
        ) and hyx__mis not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(hyx__mis, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            xwzbf__zko = len(A)
            B = np.empty(xwzbf__zko, hyx__mis)
            for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif hyx__mis == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            xwzbf__zko = len(A)
            B = np.empty(xwzbf__zko, hyx__mis)
            for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif hyx__mis == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            xwzbf__zko = len(A)
            B = np.empty(xwzbf__zko, hyx__mis)
            for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            xwzbf__zko = len(A)
            B = np.empty(xwzbf__zko, hyx__mis)
            for i in numba.parfors.parfor.internal_prange(xwzbf__zko):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        fuoby__zuf, zcjp__mbqv = args
        adlj__vugx = context.get_python_api(builder)
        srlhk__pgn = adlj__vugx.string_from_string_and_size(fuoby__zuf,
            zcjp__mbqv)
        okwt__jzxqd = adlj__vugx.to_native_value(string_type, srlhk__pgn).value
        pty__qygfo = cgutils.create_struct_proxy(string_type)(context,
            builder, okwt__jzxqd)
        pty__qygfo.hash = pty__qygfo.hash.type(-1)
        adlj__vugx.decref(srlhk__pgn)
        return pty__qygfo._getvalue()
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
        isebp__gxx, arr, ind, avqa__vltzq = args
        iftal__pbeyg = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type,
            iftal__pbeyg.offsets).data
        data = context.make_helper(builder, char_arr_type, iftal__pbeyg.data
            ).data
        dfqwe__ebc = lir.FunctionType(lir.IntType(32), [isebp__gxx.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        bmwtw__mydp = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            bmwtw__mydp = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        tcfqb__mvf = cgutils.get_or_insert_function(builder.module,
            dfqwe__ebc, bmwtw__mydp)
        return builder.call(tcfqb__mvf, [isebp__gxx, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    lerg__wxw = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    dfqwe__ebc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(32)])
    eptl__rkez = cgutils.get_or_insert_function(c.builder.module,
        dfqwe__ebc, name='string_array_from_sequence')
    koj__fbtcl = c.builder.call(eptl__rkez, [val, lerg__wxw])
    mfj__qqv = ArrayItemArrayType(char_arr_type)
    ziqnp__ouo = c.context.make_helper(c.builder, mfj__qqv)
    ziqnp__ouo.meminfo = koj__fbtcl
    kvy__lytee = c.context.make_helper(c.builder, typ)
    wkm__nbv = ziqnp__ouo._getvalue()
    kvy__lytee.data = wkm__nbv
    liner__rftdb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kvy__lytee._getvalue(), is_error=liner__rftdb)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    xwzbf__zko = len(pyval)
    xtnu__tveg = 0
    hdkvi__wbg = np.empty(xwzbf__zko + 1, np_offset_type)
    vik__kdd = []
    nuc__argl = np.empty(xwzbf__zko + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        hdkvi__wbg[i] = xtnu__tveg
        szi__zbnr = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(nuc__argl, i, int(not szi__zbnr))
        if szi__zbnr:
            continue
        sqtca__gxtu = list(s.encode()) if isinstance(s, str) else list(s)
        vik__kdd.extend(sqtca__gxtu)
        xtnu__tveg += len(sqtca__gxtu)
    hdkvi__wbg[xwzbf__zko] = xtnu__tveg
    yoydw__dvpcm = np.array(vik__kdd, np.uint8)
    diz__hja = context.get_constant(types.int64, xwzbf__zko)
    jkxbo__krj = context.get_constant_generic(builder, char_arr_type,
        yoydw__dvpcm)
    tjou__qmyfl = context.get_constant_generic(builder, offset_arr_type,
        hdkvi__wbg)
    cow__tuqn = context.get_constant_generic(builder, null_bitmap_arr_type,
        nuc__argl)
    iftal__pbeyg = lir.Constant.literal_struct([diz__hja, jkxbo__krj,
        tjou__qmyfl, cow__tuqn])
    iftal__pbeyg = cgutils.global_constant(builder, '.const.payload',
        iftal__pbeyg).bitcast(cgutils.voidptr_t)
    dhjzf__slr = context.get_constant(types.int64, -1)
    fost__ypq = context.get_constant_null(types.voidptr)
    jrzq__hcsd = lir.Constant.literal_struct([dhjzf__slr, fost__ypq,
        fost__ypq, iftal__pbeyg, dhjzf__slr])
    jrzq__hcsd = cgutils.global_constant(builder, '.const.meminfo', jrzq__hcsd
        ).bitcast(cgutils.voidptr_t)
    wkm__nbv = lir.Constant.literal_struct([jrzq__hcsd])
    kvy__lytee = lir.Constant.literal_struct([wkm__nbv])
    return kvy__lytee


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
