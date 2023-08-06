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
        sko__txx = ArrayItemArrayType(char_arr_type)
        nntx__rblgl = [('data', sko__txx)]
        models.StructModel.__init__(self, dmm, fe_type, nntx__rblgl)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        cqo__lrwv, = args
        nzr__ljox = context.make_helper(builder, string_array_type)
        nzr__ljox.data = cqo__lrwv
        context.nrt.incref(builder, data_typ, cqo__lrwv)
        return nzr__ljox._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    ismec__lyrz = c.context.insert_const_string(c.builder.module, 'pandas')
    nxy__aonp = c.pyapi.import_module_noblock(ismec__lyrz)
    hold__pedey = c.pyapi.call_method(nxy__aonp, 'StringDtype', ())
    c.pyapi.decref(nxy__aonp)
    return hold__pedey


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        cmd__ftwmo = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs
            )
        if cmd__ftwmo is not None:
            return cmd__ftwmo
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                irlwi__pdah = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(irlwi__pdah)
                for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
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
                irlwi__pdah = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(irlwi__pdah)
                for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
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
                irlwi__pdah = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(irlwi__pdah)
                for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
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
    bkipw__nqe = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    wbj__sdmxb = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and wbj__sdmxb or bkipw__nqe and is_str_arr_type(
        rhs):

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
    skc__yqp = context.make_helper(builder, arr_typ, arr_value)
    sko__txx = ArrayItemArrayType(char_arr_type)
    ljq__ncs = _get_array_item_arr_payload(context, builder, sko__txx,
        skc__yqp.data)
    return ljq__ncs


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return ljq__ncs.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        mrnjh__dolln = context.make_helper(builder, offset_arr_type,
            ljq__ncs.offsets).data
        return _get_num_total_chars(builder, mrnjh__dolln, ljq__ncs.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        indmj__aqiqt = context.make_helper(builder, offset_arr_type,
            ljq__ncs.offsets)
        vxxp__tkls = context.make_helper(builder, offset_ctypes_type)
        vxxp__tkls.data = builder.bitcast(indmj__aqiqt.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        vxxp__tkls.meminfo = indmj__aqiqt.meminfo
        hold__pedey = vxxp__tkls._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            hold__pedey)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        cqo__lrwv = context.make_helper(builder, char_arr_type, ljq__ncs.data)
        vxxp__tkls = context.make_helper(builder, data_ctypes_type)
        vxxp__tkls.data = cqo__lrwv.data
        vxxp__tkls.meminfo = cqo__lrwv.meminfo
        hold__pedey = vxxp__tkls._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            hold__pedey)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        gngsr__yoxg, ind = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder,
            gngsr__yoxg, sig.args[0])
        cqo__lrwv = context.make_helper(builder, char_arr_type, ljq__ncs.data)
        vxxp__tkls = context.make_helper(builder, data_ctypes_type)
        vxxp__tkls.data = builder.gep(cqo__lrwv.data, [ind])
        vxxp__tkls.meminfo = cqo__lrwv.meminfo
        hold__pedey = vxxp__tkls._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            hold__pedey)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        rdfbc__hzsgc, uusg__cctqu, rlxw__xqpgz, wpvy__iseq = args
        qtw__wjgh = builder.bitcast(builder.gep(rdfbc__hzsgc, [uusg__cctqu]
            ), lir.IntType(8).as_pointer())
        duik__nydaa = builder.bitcast(builder.gep(rlxw__xqpgz, [wpvy__iseq]
            ), lir.IntType(8).as_pointer())
        vdok__hztc = builder.load(duik__nydaa)
        builder.store(vdok__hztc, qtw__wjgh)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        dqo__bfec = context.make_helper(builder, null_bitmap_arr_type,
            ljq__ncs.null_bitmap)
        vxxp__tkls = context.make_helper(builder, data_ctypes_type)
        vxxp__tkls.data = dqo__bfec.data
        vxxp__tkls.meminfo = dqo__bfec.meminfo
        hold__pedey = vxxp__tkls._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            hold__pedey)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        mrnjh__dolln = context.make_helper(builder, offset_arr_type,
            ljq__ncs.offsets).data
        return builder.load(builder.gep(mrnjh__dolln, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, ljq__ncs.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        xut__syrsk, ind = args
        if in_bitmap_typ == data_ctypes_type:
            vxxp__tkls = context.make_helper(builder, data_ctypes_type,
                xut__syrsk)
            xut__syrsk = vxxp__tkls.data
        return builder.load(builder.gep(xut__syrsk, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        xut__syrsk, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            vxxp__tkls = context.make_helper(builder, data_ctypes_type,
                xut__syrsk)
            xut__syrsk = vxxp__tkls.data
        builder.store(val, builder.gep(xut__syrsk, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        equm__utfxl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ynqd__yghfr = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        skch__gabj = context.make_helper(builder, offset_arr_type,
            equm__utfxl.offsets).data
        xxtmd__eded = context.make_helper(builder, offset_arr_type,
            ynqd__yghfr.offsets).data
        jqfyh__zuct = context.make_helper(builder, char_arr_type,
            equm__utfxl.data).data
        anje__vjr = context.make_helper(builder, char_arr_type, ynqd__yghfr
            .data).data
        zmnj__abq = context.make_helper(builder, null_bitmap_arr_type,
            equm__utfxl.null_bitmap).data
        qvzsq__lzwmg = context.make_helper(builder, null_bitmap_arr_type,
            ynqd__yghfr.null_bitmap).data
        bynie__bisi = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, xxtmd__eded, skch__gabj, bynie__bisi)
        cgutils.memcpy(builder, anje__vjr, jqfyh__zuct, builder.load(
            builder.gep(skch__gabj, [ind])))
        elnw__alkno = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        zkpex__wiydc = builder.lshr(elnw__alkno, lir.Constant(lir.IntType(
            64), 3))
        cgutils.memcpy(builder, qvzsq__lzwmg, zmnj__abq, zkpex__wiydc)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        equm__utfxl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ynqd__yghfr = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        skch__gabj = context.make_helper(builder, offset_arr_type,
            equm__utfxl.offsets).data
        jqfyh__zuct = context.make_helper(builder, char_arr_type,
            equm__utfxl.data).data
        anje__vjr = context.make_helper(builder, char_arr_type, ynqd__yghfr
            .data).data
        num_total_chars = _get_num_total_chars(builder, skch__gabj,
            equm__utfxl.n_arrays)
        cgutils.memcpy(builder, anje__vjr, jqfyh__zuct, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        equm__utfxl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ynqd__yghfr = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        skch__gabj = context.make_helper(builder, offset_arr_type,
            equm__utfxl.offsets).data
        xxtmd__eded = context.make_helper(builder, offset_arr_type,
            ynqd__yghfr.offsets).data
        zmnj__abq = context.make_helper(builder, null_bitmap_arr_type,
            equm__utfxl.null_bitmap).data
        irlwi__pdah = equm__utfxl.n_arrays
        ptg__zyzhs = context.get_constant(offset_type, 0)
        lee__tsoft = cgutils.alloca_once_value(builder, ptg__zyzhs)
        with cgutils.for_range(builder, irlwi__pdah) as mesw__ffze:
            iyi__ogivy = lower_is_na(context, builder, zmnj__abq,
                mesw__ffze.index)
            with cgutils.if_likely(builder, builder.not_(iyi__ogivy)):
                csvl__ymhu = builder.load(builder.gep(skch__gabj, [
                    mesw__ffze.index]))
                vwr__irnu = builder.load(lee__tsoft)
                builder.store(csvl__ymhu, builder.gep(xxtmd__eded, [vwr__irnu])
                    )
                builder.store(builder.add(vwr__irnu, lir.Constant(context.
                    get_value_type(offset_type), 1)), lee__tsoft)
        vwr__irnu = builder.load(lee__tsoft)
        csvl__ymhu = builder.load(builder.gep(skch__gabj, [irlwi__pdah]))
        builder.store(csvl__ymhu, builder.gep(xxtmd__eded, [vwr__irnu]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        xiin__swszv, ind, str, xltn__nge = args
        xiin__swszv = context.make_array(sig.args[0])(context, builder,
            xiin__swszv)
        hyajj__yghtp = builder.gep(xiin__swszv.data, [ind])
        cgutils.raw_memcpy(builder, hyajj__yghtp, str, xltn__nge, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        hyajj__yghtp, ind, qgo__earpw, xltn__nge = args
        hyajj__yghtp = builder.gep(hyajj__yghtp, [ind])
        cgutils.raw_memcpy(builder, hyajj__yghtp, qgo__earpw, xltn__nge, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    tevfh__mbrkg = np.int64(getitem_str_offset(A, i))
    uzx__yclij = np.int64(getitem_str_offset(A, i + 1))
    l = uzx__yclij - tevfh__mbrkg
    qzh__xenn = get_data_ptr_ind(A, tevfh__mbrkg)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(qzh__xenn, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    zyaqg__rkcz = getitem_str_offset(A, i)
    ujbsk__uysuk = getitem_str_offset(A, i + 1)
    ovp__vqm = ujbsk__uysuk - zyaqg__rkcz
    laev__ezq = getitem_str_offset(B, j)
    ikt__otilj = laev__ezq + ovp__vqm
    setitem_str_offset(B, j + 1, ikt__otilj)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if ovp__vqm != 0:
        cqo__lrwv = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(cqo__lrwv, np.
            int64(laev__ezq), np.int64(ikt__otilj))
        hvnp__lkax = get_data_ptr(B).data
        wqquw__yzeo = get_data_ptr(A).data
        memcpy_region(hvnp__lkax, laev__ezq, wqquw__yzeo, zyaqg__rkcz,
            ovp__vqm, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    irlwi__pdah = len(str_arr)
    tai__djyy = np.empty(irlwi__pdah, np.bool_)
    for i in range(irlwi__pdah):
        tai__djyy[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return tai__djyy


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            irlwi__pdah = len(data)
            l = []
            for i in range(irlwi__pdah):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        tev__xjtx = data.count
        nqfim__sqryt = ['to_list_if_immutable_arr(data[{}])'.format(i) for
            i in range(tev__xjtx)]
        if is_overload_true(str_null_bools):
            nqfim__sqryt += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(tev__xjtx) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        eprp__ksy = 'def f(data, str_null_bools=None):\n'
        eprp__ksy += '  return ({}{})\n'.format(', '.join(nqfim__sqryt), 
            ',' if tev__xjtx == 1 else '')
        kmui__ehqt = {}
        exec(eprp__ksy, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, kmui__ehqt)
        uvv__rhl = kmui__ehqt['f']
        return uvv__rhl
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                irlwi__pdah = len(list_data)
                for i in range(irlwi__pdah):
                    qgo__earpw = list_data[i]
                    str_arr[i] = qgo__earpw
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                irlwi__pdah = len(list_data)
                for i in range(irlwi__pdah):
                    qgo__earpw = list_data[i]
                    str_arr[i] = qgo__earpw
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        tev__xjtx = str_arr.count
        onpma__mumop = 0
        eprp__ksy = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(tev__xjtx):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                eprp__ksy += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, tev__xjtx + onpma__mumop))
                onpma__mumop += 1
            else:
                eprp__ksy += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        eprp__ksy += '  return\n'
        kmui__ehqt = {}
        exec(eprp__ksy, {'cp_str_list_to_array': cp_str_list_to_array},
            kmui__ehqt)
        qpa__npeij = kmui__ehqt['f']
        return qpa__npeij
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            irlwi__pdah = len(str_list)
            str_arr = pre_alloc_string_array(irlwi__pdah, -1)
            for i in range(irlwi__pdah):
                qgo__earpw = str_list[i]
                str_arr[i] = qgo__earpw
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            irlwi__pdah = len(A)
            pyj__uxs = 0
            for i in range(irlwi__pdah):
                qgo__earpw = A[i]
                pyj__uxs += get_utf8_size(qgo__earpw)
            return pyj__uxs
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        irlwi__pdah = len(arr)
        n_chars = num_total_chars(arr)
        inbm__mdvcb = pre_alloc_string_array(irlwi__pdah, np.int64(n_chars))
        copy_str_arr_slice(inbm__mdvcb, arr, irlwi__pdah)
        return inbm__mdvcb
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
    eprp__ksy = 'def f(in_seq):\n'
    eprp__ksy += '    n_strs = len(in_seq)\n'
    eprp__ksy += '    A = pre_alloc_string_array(n_strs, -1)\n'
    eprp__ksy += '    return A\n'
    kmui__ehqt = {}
    exec(eprp__ksy, {'pre_alloc_string_array': pre_alloc_string_array},
        kmui__ehqt)
    hjgf__wxt = kmui__ehqt['f']
    return hjgf__wxt


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        mhji__oatf = 'pre_alloc_binary_array'
    else:
        mhji__oatf = 'pre_alloc_string_array'
    eprp__ksy = 'def f(in_seq):\n'
    eprp__ksy += '    n_strs = len(in_seq)\n'
    eprp__ksy += f'    A = {mhji__oatf}(n_strs, -1)\n'
    eprp__ksy += '    for i in range(n_strs):\n'
    eprp__ksy += '        A[i] = in_seq[i]\n'
    eprp__ksy += '    return A\n'
    kmui__ehqt = {}
    exec(eprp__ksy, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, kmui__ehqt)
    hjgf__wxt = kmui__ehqt['f']
    return hjgf__wxt


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        yskxm__nlc = builder.add(ljq__ncs.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        tkpl__dflk = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        zkpex__wiydc = builder.mul(yskxm__nlc, tkpl__dflk)
        bgvjs__zlro = context.make_array(offset_arr_type)(context, builder,
            ljq__ncs.offsets).data
        cgutils.memset(builder, bgvjs__zlro, zkpex__wiydc, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        hdnsj__taib = ljq__ncs.n_arrays
        zkpex__wiydc = builder.lshr(builder.add(hdnsj__taib, lir.Constant(
            lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        pdnip__foiox = context.make_array(null_bitmap_arr_type)(context,
            builder, ljq__ncs.null_bitmap).data
        cgutils.memset(builder, pdnip__foiox, zkpex__wiydc, 0)
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
    icdnr__rnzu = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        dkd__xcy = len(len_arr)
        for i in range(dkd__xcy):
            offsets[i] = icdnr__rnzu
            icdnr__rnzu += len_arr[i]
        offsets[dkd__xcy] = icdnr__rnzu
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    chp__dha = i // 8
    rmblf__chi = getitem_str_bitmap(bits, chp__dha)
    rmblf__chi ^= np.uint8(-np.uint8(bit_is_set) ^ rmblf__chi) & kBitmask[i % 8
        ]
    setitem_str_bitmap(bits, chp__dha, rmblf__chi)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    zowye__muf = get_null_bitmap_ptr(out_str_arr)
    xmd__juf = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        uxt__zhkyz = get_bit_bitmap(xmd__juf, j)
        set_bit_to(zowye__muf, out_start + j, uxt__zhkyz)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, gngsr__yoxg, jdp__bgl, kpow__sokuj = args
        equm__utfxl = _get_str_binary_arr_payload(context, builder,
            gngsr__yoxg, string_array_type)
        ynqd__yghfr = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        skch__gabj = context.make_helper(builder, offset_arr_type,
            equm__utfxl.offsets).data
        xxtmd__eded = context.make_helper(builder, offset_arr_type,
            ynqd__yghfr.offsets).data
        jqfyh__zuct = context.make_helper(builder, char_arr_type,
            equm__utfxl.data).data
        anje__vjr = context.make_helper(builder, char_arr_type, ynqd__yghfr
            .data).data
        num_total_chars = _get_num_total_chars(builder, skch__gabj,
            equm__utfxl.n_arrays)
        uwhrq__wjgx = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        jylw__lxfl = cgutils.get_or_insert_function(builder.module,
            uwhrq__wjgx, name='set_string_array_range')
        builder.call(jylw__lxfl, [xxtmd__eded, anje__vjr, skch__gabj,
            jqfyh__zuct, jdp__bgl, kpow__sokuj, equm__utfxl.n_arrays,
            num_total_chars])
        bxer__edov = context.typing_context.resolve_value_type(copy_nulls_range
            )
        wtma__fyuku = bxer__edov.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        vgo__qatc = context.get_function(bxer__edov, wtma__fyuku)
        vgo__qatc(builder, (out_arr, gngsr__yoxg, jdp__bgl))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    uxp__uta = c.context.make_helper(c.builder, typ, val)
    sko__txx = ArrayItemArrayType(char_arr_type)
    ljq__ncs = _get_array_item_arr_payload(c.context, c.builder, sko__txx,
        uxp__uta.data)
    vcik__ivcy = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    ffj__dbmcy = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        ffj__dbmcy = 'pd_array_from_string_array'
    uwhrq__wjgx = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    ypl__cwyvx = cgutils.get_or_insert_function(c.builder.module,
        uwhrq__wjgx, name=ffj__dbmcy)
    mrnjh__dolln = c.context.make_array(offset_arr_type)(c.context, c.
        builder, ljq__ncs.offsets).data
    qzh__xenn = c.context.make_array(char_arr_type)(c.context, c.builder,
        ljq__ncs.data).data
    pdnip__foiox = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, ljq__ncs.null_bitmap).data
    arr = c.builder.call(ypl__cwyvx, [ljq__ncs.n_arrays, mrnjh__dolln,
        qzh__xenn, pdnip__foiox, vcik__ivcy])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        pdnip__foiox = context.make_array(null_bitmap_arr_type)(context,
            builder, ljq__ncs.null_bitmap).data
        qsf__xckp = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        jgxn__cite = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        rmblf__chi = builder.load(builder.gep(pdnip__foiox, [qsf__xckp],
            inbounds=True))
        gxj__cbn = lir.ArrayType(lir.IntType(8), 8)
        gczc__xlh = cgutils.alloca_once_value(builder, lir.Constant(
            gxj__cbn, (1, 2, 4, 8, 16, 32, 64, 128)))
        cwgfa__mzd = builder.load(builder.gep(gczc__xlh, [lir.Constant(lir.
            IntType(64), 0), jgxn__cite], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(rmblf__chi,
            cwgfa__mzd), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        qsf__xckp = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        jgxn__cite = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        pdnip__foiox = context.make_array(null_bitmap_arr_type)(context,
            builder, ljq__ncs.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, ljq__ncs.
            offsets).data
        odd__rzdpo = builder.gep(pdnip__foiox, [qsf__xckp], inbounds=True)
        rmblf__chi = builder.load(odd__rzdpo)
        gxj__cbn = lir.ArrayType(lir.IntType(8), 8)
        gczc__xlh = cgutils.alloca_once_value(builder, lir.Constant(
            gxj__cbn, (1, 2, 4, 8, 16, 32, 64, 128)))
        cwgfa__mzd = builder.load(builder.gep(gczc__xlh, [lir.Constant(lir.
            IntType(64), 0), jgxn__cite], inbounds=True))
        cwgfa__mzd = builder.xor(cwgfa__mzd, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(rmblf__chi, cwgfa__mzd), odd__rzdpo)
        if str_arr_typ == string_array_type:
            jmiih__bksl = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            xher__uje = builder.icmp_unsigned('!=', jmiih__bksl, ljq__ncs.
                n_arrays)
            with builder.if_then(xher__uje):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [jmiih__bksl]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        qsf__xckp = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        jgxn__cite = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        pdnip__foiox = context.make_array(null_bitmap_arr_type)(context,
            builder, ljq__ncs.null_bitmap).data
        odd__rzdpo = builder.gep(pdnip__foiox, [qsf__xckp], inbounds=True)
        rmblf__chi = builder.load(odd__rzdpo)
        gxj__cbn = lir.ArrayType(lir.IntType(8), 8)
        gczc__xlh = cgutils.alloca_once_value(builder, lir.Constant(
            gxj__cbn, (1, 2, 4, 8, 16, 32, 64, 128)))
        cwgfa__mzd = builder.load(builder.gep(gczc__xlh, [lir.Constant(lir.
            IntType(64), 0), jgxn__cite], inbounds=True))
        builder.store(builder.or_(rmblf__chi, cwgfa__mzd), odd__rzdpo)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        zkpex__wiydc = builder.udiv(builder.add(ljq__ncs.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        pdnip__foiox = context.make_array(null_bitmap_arr_type)(context,
            builder, ljq__ncs.null_bitmap).data
        cgutils.memset(builder, pdnip__foiox, zkpex__wiydc, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    mbq__ybl = context.make_helper(builder, string_array_type, str_arr)
    sko__txx = ArrayItemArrayType(char_arr_type)
    gxqrg__zllqz = context.make_helper(builder, sko__txx, mbq__ybl.data)
    yia__uuruf = ArrayItemArrayPayloadType(sko__txx)
    cxn__ofw = context.nrt.meminfo_data(builder, gxqrg__zllqz.meminfo)
    jqn__geai = builder.bitcast(cxn__ofw, context.get_value_type(yia__uuruf
        ).as_pointer())
    return jqn__geai


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        edgkl__yid, iouu__uac = args
        rmm__qpmd = _get_str_binary_arr_data_payload_ptr(context, builder,
            iouu__uac)
        lhvgi__cjbms = _get_str_binary_arr_data_payload_ptr(context,
            builder, edgkl__yid)
        lcdrm__ohx = _get_str_binary_arr_payload(context, builder,
            iouu__uac, sig.args[1])
        gddk__ikjs = _get_str_binary_arr_payload(context, builder,
            edgkl__yid, sig.args[0])
        context.nrt.incref(builder, char_arr_type, lcdrm__ohx.data)
        context.nrt.incref(builder, offset_arr_type, lcdrm__ohx.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, lcdrm__ohx.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, gddk__ikjs.data)
        context.nrt.decref(builder, offset_arr_type, gddk__ikjs.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, gddk__ikjs.
            null_bitmap)
        builder.store(builder.load(rmm__qpmd), lhvgi__cjbms)
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
        irlwi__pdah = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return irlwi__pdah
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, hyajj__yghtp, ewd__axkvw = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, ljq__ncs.
            offsets).data
        data = context.make_helper(builder, char_arr_type, ljq__ncs.data).data
        uwhrq__wjgx = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        bgjzz__cha = cgutils.get_or_insert_function(builder.module,
            uwhrq__wjgx, name='setitem_string_array')
        oheq__ywcau = context.get_constant(types.int32, -1)
        hypc__yteq = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, ljq__ncs.
            n_arrays)
        builder.call(bgjzz__cha, [offsets, data, num_total_chars, builder.
            extract_value(hyajj__yghtp, 0), ewd__axkvw, oheq__ywcau,
            hypc__yteq, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    uwhrq__wjgx = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    vihdm__iulf = cgutils.get_or_insert_function(builder.module,
        uwhrq__wjgx, name='is_na')
    return builder.call(vihdm__iulf, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        qtw__wjgh, duik__nydaa, tev__xjtx, dgk__exh = args
        cgutils.raw_memcpy(builder, qtw__wjgh, duik__nydaa, tev__xjtx, dgk__exh
            )
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
        rrrf__yenwe, oge__cmhi = unicode_to_utf8_and_len(val)
        npy__nerg = getitem_str_offset(A, ind)
        ghd__vhg = getitem_str_offset(A, ind + 1)
        hvavl__hjwr = ghd__vhg - npy__nerg
        if hvavl__hjwr != oge__cmhi:
            return False
        hyajj__yghtp = get_data_ptr_ind(A, npy__nerg)
        return memcmp(hyajj__yghtp, rrrf__yenwe, oge__cmhi) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        npy__nerg = getitem_str_offset(A, ind)
        hvavl__hjwr = bodo.libs.str_ext.int_to_str_len(val)
        eogf__onnh = npy__nerg + hvavl__hjwr
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            npy__nerg, eogf__onnh)
        hyajj__yghtp = get_data_ptr_ind(A, npy__nerg)
        inplace_int64_to_str(hyajj__yghtp, hvavl__hjwr, val)
        setitem_str_offset(A, ind + 1, npy__nerg + hvavl__hjwr)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        hyajj__yghtp, = args
        tren__kxv = context.insert_const_string(builder.module, '<NA>')
        swgm__opl = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, hyajj__yghtp, tren__kxv, swgm__opl, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    rkgbp__wqiz = len('<NA>')

    def impl(A, ind):
        npy__nerg = getitem_str_offset(A, ind)
        eogf__onnh = npy__nerg + rkgbp__wqiz
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            npy__nerg, eogf__onnh)
        hyajj__yghtp = get_data_ptr_ind(A, npy__nerg)
        inplace_set_NA_str(hyajj__yghtp)
        setitem_str_offset(A, ind + 1, npy__nerg + rkgbp__wqiz)
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
            npy__nerg = getitem_str_offset(A, ind)
            ghd__vhg = getitem_str_offset(A, ind + 1)
            ewd__axkvw = ghd__vhg - npy__nerg
            hyajj__yghtp = get_data_ptr_ind(A, npy__nerg)
            xge__wtru = decode_utf8(hyajj__yghtp, ewd__axkvw)
            return xge__wtru
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            irlwi__pdah = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(irlwi__pdah):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            hvnp__lkax = get_data_ptr(out_arr).data
            wqquw__yzeo = get_data_ptr(A).data
            onpma__mumop = 0
            vwr__irnu = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(irlwi__pdah):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    ffumd__krwu = get_str_arr_item_length(A, i)
                    if ffumd__krwu == 1:
                        copy_single_char(hvnp__lkax, vwr__irnu, wqquw__yzeo,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(hvnp__lkax, vwr__irnu, wqquw__yzeo,
                            getitem_str_offset(A, i), ffumd__krwu, 1)
                    vwr__irnu += ffumd__krwu
                    setitem_str_offset(out_arr, onpma__mumop + 1, vwr__irnu)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, onpma__mumop)
                    else:
                        str_arr_set_not_na(out_arr, onpma__mumop)
                    onpma__mumop += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            irlwi__pdah = len(ind)
            out_arr = pre_alloc_string_array(irlwi__pdah, -1)
            onpma__mumop = 0
            for i in range(irlwi__pdah):
                qgo__earpw = A[ind[i]]
                out_arr[onpma__mumop] = qgo__earpw
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, onpma__mumop)
                onpma__mumop += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            irlwi__pdah = len(A)
            widt__ayf = numba.cpython.unicode._normalize_slice(ind, irlwi__pdah
                )
            ntteu__jzgw = numba.cpython.unicode._slice_span(widt__ayf)
            if widt__ayf.step == 1:
                npy__nerg = getitem_str_offset(A, widt__ayf.start)
                ghd__vhg = getitem_str_offset(A, widt__ayf.stop)
                n_chars = ghd__vhg - npy__nerg
                inbm__mdvcb = pre_alloc_string_array(ntteu__jzgw, np.int64(
                    n_chars))
                for i in range(ntteu__jzgw):
                    inbm__mdvcb[i] = A[widt__ayf.start + i]
                    if str_arr_is_na(A, widt__ayf.start + i):
                        str_arr_set_na(inbm__mdvcb, i)
                return inbm__mdvcb
            else:
                inbm__mdvcb = pre_alloc_string_array(ntteu__jzgw, -1)
                for i in range(ntteu__jzgw):
                    inbm__mdvcb[i] = A[widt__ayf.start + i * widt__ayf.step]
                    if str_arr_is_na(A, widt__ayf.start + i * widt__ayf.step):
                        str_arr_set_na(inbm__mdvcb, i)
                return inbm__mdvcb
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
    cht__tqaq = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(cht__tqaq)
        ntqe__huti = 4

        def impl_scalar(A, idx, val):
            tloo__qdq = (val._length if val._is_ascii else ntqe__huti * val
                ._length)
            cqo__lrwv = A._data
            npy__nerg = np.int64(getitem_str_offset(A, idx))
            eogf__onnh = npy__nerg + tloo__qdq
            bodo.libs.array_item_arr_ext.ensure_data_capacity(cqo__lrwv,
                npy__nerg, eogf__onnh)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                eogf__onnh, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                widt__ayf = numba.cpython.unicode._normalize_slice(idx, len(A))
                tevfh__mbrkg = widt__ayf.start
                cqo__lrwv = A._data
                npy__nerg = np.int64(getitem_str_offset(A, tevfh__mbrkg))
                eogf__onnh = npy__nerg + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(cqo__lrwv,
                    npy__nerg, eogf__onnh)
                set_string_array_range(A, val, tevfh__mbrkg, npy__nerg)
                dyc__tcdc = 0
                for i in range(widt__ayf.start, widt__ayf.stop, widt__ayf.step
                    ):
                    if str_arr_is_na(val, dyc__tcdc):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    dyc__tcdc += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                ixta__dqt = str_list_to_array(val)
                A[idx] = ixta__dqt
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                widt__ayf = numba.cpython.unicode._normalize_slice(idx, len(A))
                for i in range(widt__ayf.start, widt__ayf.stop, widt__ayf.step
                    ):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(cht__tqaq)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                irlwi__pdah = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(irlwi__pdah, -1)
                for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
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
                irlwi__pdah = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(irlwi__pdah, -1)
                dqp__oep = 0
                for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, dqp__oep):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, dqp__oep)
                        else:
                            out_arr[i] = str(val[dqp__oep])
                        dqp__oep += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(cht__tqaq)
    raise BodoError(cht__tqaq)


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
    dfeqd__jjtf = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(dfeqd__jjtf, (types.Float, types.Integer)
        ) and dfeqd__jjtf not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(dfeqd__jjtf, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            irlwi__pdah = len(A)
            B = np.empty(irlwi__pdah, dfeqd__jjtf)
            for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif dfeqd__jjtf == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            irlwi__pdah = len(A)
            B = np.empty(irlwi__pdah, dfeqd__jjtf)
            for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif dfeqd__jjtf == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            irlwi__pdah = len(A)
            B = np.empty(irlwi__pdah, dfeqd__jjtf)
            for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            irlwi__pdah = len(A)
            B = np.empty(irlwi__pdah, dfeqd__jjtf)
            for i in numba.parfors.parfor.internal_prange(irlwi__pdah):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        hyajj__yghtp, ewd__axkvw = args
        osyvn__dhjdz = context.get_python_api(builder)
        ysrfj__kld = osyvn__dhjdz.string_from_string_and_size(hyajj__yghtp,
            ewd__axkvw)
        fupss__xiy = osyvn__dhjdz.to_native_value(string_type, ysrfj__kld
            ).value
        wyd__zjgyq = cgutils.create_struct_proxy(string_type)(context,
            builder, fupss__xiy)
        wyd__zjgyq.hash = wyd__zjgyq.hash.type(-1)
        osyvn__dhjdz.decref(ysrfj__kld)
        return wyd__zjgyq._getvalue()
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
        pln__lzlq, arr, ind, ftr__yljr = args
        ljq__ncs = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, ljq__ncs.
            offsets).data
        data = context.make_helper(builder, char_arr_type, ljq__ncs.data).data
        uwhrq__wjgx = lir.FunctionType(lir.IntType(32), [pln__lzlq.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        gwd__zmvom = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            gwd__zmvom = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        kbb__kvnzw = cgutils.get_or_insert_function(builder.module,
            uwhrq__wjgx, gwd__zmvom)
        return builder.call(kbb__kvnzw, [pln__lzlq, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    vcik__ivcy = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    uwhrq__wjgx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    ojs__ixlv = cgutils.get_or_insert_function(c.builder.module,
        uwhrq__wjgx, name='string_array_from_sequence')
    djb__soc = c.builder.call(ojs__ixlv, [val, vcik__ivcy])
    sko__txx = ArrayItemArrayType(char_arr_type)
    gxqrg__zllqz = c.context.make_helper(c.builder, sko__txx)
    gxqrg__zllqz.meminfo = djb__soc
    mbq__ybl = c.context.make_helper(c.builder, typ)
    cqo__lrwv = gxqrg__zllqz._getvalue()
    mbq__ybl.data = cqo__lrwv
    hshxx__xyoii = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mbq__ybl._getvalue(), is_error=hshxx__xyoii)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    irlwi__pdah = len(pyval)
    vwr__irnu = 0
    iqf__nyhyf = np.empty(irlwi__pdah + 1, np_offset_type)
    lhys__axret = []
    kyb__ovo = np.empty(irlwi__pdah + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        iqf__nyhyf[i] = vwr__irnu
        lxwr__ryzy = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(kyb__ovo, i, int(not lxwr__ryzy))
        if lxwr__ryzy:
            continue
        jtx__fdr = list(s.encode()) if isinstance(s, str) else list(s)
        lhys__axret.extend(jtx__fdr)
        vwr__irnu += len(jtx__fdr)
    iqf__nyhyf[irlwi__pdah] = vwr__irnu
    bul__euqz = np.array(lhys__axret, np.uint8)
    dzbls__wgz = context.get_constant(types.int64, irlwi__pdah)
    bksnb__fjpit = context.get_constant_generic(builder, char_arr_type,
        bul__euqz)
    oqpyx__mif = context.get_constant_generic(builder, offset_arr_type,
        iqf__nyhyf)
    lpcqs__jcjxp = context.get_constant_generic(builder,
        null_bitmap_arr_type, kyb__ovo)
    ljq__ncs = lir.Constant.literal_struct([dzbls__wgz, bksnb__fjpit,
        oqpyx__mif, lpcqs__jcjxp])
    ljq__ncs = cgutils.global_constant(builder, '.const.payload', ljq__ncs
        ).bitcast(cgutils.voidptr_t)
    gwk__ewzy = context.get_constant(types.int64, -1)
    yimql__jbnq = context.get_constant_null(types.voidptr)
    jmusi__zzahb = lir.Constant.literal_struct([gwk__ewzy, yimql__jbnq,
        yimql__jbnq, ljq__ncs, gwk__ewzy])
    jmusi__zzahb = cgutils.global_constant(builder, '.const.meminfo',
        jmusi__zzahb).bitcast(cgutils.voidptr_t)
    cqo__lrwv = lir.Constant.literal_struct([jmusi__zzahb])
    mbq__ybl = lir.Constant.literal_struct([cqo__lrwv])
    return mbq__ybl


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
