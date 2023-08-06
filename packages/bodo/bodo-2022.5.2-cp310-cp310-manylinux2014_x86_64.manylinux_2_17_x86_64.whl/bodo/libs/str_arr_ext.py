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
        reju__wlh = ArrayItemArrayType(char_arr_type)
        dyf__rfiv = [('data', reju__wlh)]
        models.StructModel.__init__(self, dmm, fe_type, dyf__rfiv)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        ubpkl__nwqv, = args
        nlfc__higp = context.make_helper(builder, string_array_type)
        nlfc__higp.data = ubpkl__nwqv
        context.nrt.incref(builder, data_typ, ubpkl__nwqv)
        return nlfc__higp._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    xggb__dogyb = c.context.insert_const_string(c.builder.module, 'pandas')
    sabj__lkey = c.pyapi.import_module_noblock(xggb__dogyb)
    bjuy__egk = c.pyapi.call_method(sabj__lkey, 'StringDtype', ())
    c.pyapi.decref(sabj__lkey)
    return bjuy__egk


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        codnq__cpfb = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs,
            rhs)
        if codnq__cpfb is not None:
            return codnq__cpfb
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lsxs__bwqnc = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(lsxs__bwqnc)
                for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
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
                lsxs__bwqnc = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(lsxs__bwqnc)
                for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
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
                lsxs__bwqnc = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(lsxs__bwqnc)
                for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
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
    rchgv__nzr = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    pyvd__gjtgh = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and pyvd__gjtgh or rchgv__nzr and is_str_arr_type(
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
    dkbnp__hxi = context.make_helper(builder, arr_typ, arr_value)
    reju__wlh = ArrayItemArrayType(char_arr_type)
    gupzd__isw = _get_array_item_arr_payload(context, builder, reju__wlh,
        dkbnp__hxi.data)
    return gupzd__isw


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return gupzd__isw.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        cizb__bnnh = context.make_helper(builder, offset_arr_type,
            gupzd__isw.offsets).data
        return _get_num_total_chars(builder, cizb__bnnh, gupzd__isw.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        iww__ioo = context.make_helper(builder, offset_arr_type, gupzd__isw
            .offsets)
        gtg__enxn = context.make_helper(builder, offset_ctypes_type)
        gtg__enxn.data = builder.bitcast(iww__ioo.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        gtg__enxn.meminfo = iww__ioo.meminfo
        bjuy__egk = gtg__enxn._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            bjuy__egk)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ubpkl__nwqv = context.make_helper(builder, char_arr_type,
            gupzd__isw.data)
        gtg__enxn = context.make_helper(builder, data_ctypes_type)
        gtg__enxn.data = ubpkl__nwqv.data
        gtg__enxn.meminfo = ubpkl__nwqv.meminfo
        bjuy__egk = gtg__enxn._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, bjuy__egk)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        fzw__ilk, ind = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder, fzw__ilk,
            sig.args[0])
        ubpkl__nwqv = context.make_helper(builder, char_arr_type,
            gupzd__isw.data)
        gtg__enxn = context.make_helper(builder, data_ctypes_type)
        gtg__enxn.data = builder.gep(ubpkl__nwqv.data, [ind])
        gtg__enxn.meminfo = ubpkl__nwqv.meminfo
        bjuy__egk = gtg__enxn._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, bjuy__egk)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        iodz__lita, nrrp__huhw, mob__qwu, zpjs__qhxww = args
        pvvcf__xsre = builder.bitcast(builder.gep(iodz__lita, [nrrp__huhw]),
            lir.IntType(8).as_pointer())
        mzy__ivle = builder.bitcast(builder.gep(mob__qwu, [zpjs__qhxww]),
            lir.IntType(8).as_pointer())
        gqm__usfjc = builder.load(mzy__ivle)
        builder.store(gqm__usfjc, pvvcf__xsre)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        npldx__ndaf = context.make_helper(builder, null_bitmap_arr_type,
            gupzd__isw.null_bitmap)
        gtg__enxn = context.make_helper(builder, data_ctypes_type)
        gtg__enxn.data = npldx__ndaf.data
        gtg__enxn.meminfo = npldx__ndaf.meminfo
        bjuy__egk = gtg__enxn._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, bjuy__egk)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        cizb__bnnh = context.make_helper(builder, offset_arr_type,
            gupzd__isw.offsets).data
        return builder.load(builder.gep(cizb__bnnh, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, gupzd__isw.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        kgaoh__qmheu, ind = args
        if in_bitmap_typ == data_ctypes_type:
            gtg__enxn = context.make_helper(builder, data_ctypes_type,
                kgaoh__qmheu)
            kgaoh__qmheu = gtg__enxn.data
        return builder.load(builder.gep(kgaoh__qmheu, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        kgaoh__qmheu, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            gtg__enxn = context.make_helper(builder, data_ctypes_type,
                kgaoh__qmheu)
            kgaoh__qmheu = gtg__enxn.data
        builder.store(val, builder.gep(kgaoh__qmheu, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        dohvz__byt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qax__lfg = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        ximv__tjnt = context.make_helper(builder, offset_arr_type,
            dohvz__byt.offsets).data
        cgr__ahvwn = context.make_helper(builder, offset_arr_type, qax__lfg
            .offsets).data
        gtj__zxt = context.make_helper(builder, char_arr_type, dohvz__byt.data
            ).data
        umi__lmqwi = context.make_helper(builder, char_arr_type, qax__lfg.data
            ).data
        ugsix__cyg = context.make_helper(builder, null_bitmap_arr_type,
            dohvz__byt.null_bitmap).data
        lnsb__pmlln = context.make_helper(builder, null_bitmap_arr_type,
            qax__lfg.null_bitmap).data
        zvrfd__hzph = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, cgr__ahvwn, ximv__tjnt, zvrfd__hzph)
        cgutils.memcpy(builder, umi__lmqwi, gtj__zxt, builder.load(builder.
            gep(ximv__tjnt, [ind])))
        iwyz__dxc = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        dxtxz__hixh = builder.lshr(iwyz__dxc, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, lnsb__pmlln, ugsix__cyg, dxtxz__hixh)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        dohvz__byt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qax__lfg = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        ximv__tjnt = context.make_helper(builder, offset_arr_type,
            dohvz__byt.offsets).data
        gtj__zxt = context.make_helper(builder, char_arr_type, dohvz__byt.data
            ).data
        umi__lmqwi = context.make_helper(builder, char_arr_type, qax__lfg.data
            ).data
        num_total_chars = _get_num_total_chars(builder, ximv__tjnt,
            dohvz__byt.n_arrays)
        cgutils.memcpy(builder, umi__lmqwi, gtj__zxt, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        dohvz__byt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qax__lfg = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        ximv__tjnt = context.make_helper(builder, offset_arr_type,
            dohvz__byt.offsets).data
        cgr__ahvwn = context.make_helper(builder, offset_arr_type, qax__lfg
            .offsets).data
        ugsix__cyg = context.make_helper(builder, null_bitmap_arr_type,
            dohvz__byt.null_bitmap).data
        lsxs__bwqnc = dohvz__byt.n_arrays
        ncso__htu = context.get_constant(offset_type, 0)
        jauqz__ybw = cgutils.alloca_once_value(builder, ncso__htu)
        with cgutils.for_range(builder, lsxs__bwqnc) as egyms__dttg:
            kgubu__ejsh = lower_is_na(context, builder, ugsix__cyg,
                egyms__dttg.index)
            with cgutils.if_likely(builder, builder.not_(kgubu__ejsh)):
                owqqw__hwml = builder.load(builder.gep(ximv__tjnt, [
                    egyms__dttg.index]))
                dza__kdm = builder.load(jauqz__ybw)
                builder.store(owqqw__hwml, builder.gep(cgr__ahvwn, [dza__kdm]))
                builder.store(builder.add(dza__kdm, lir.Constant(context.
                    get_value_type(offset_type), 1)), jauqz__ybw)
        dza__kdm = builder.load(jauqz__ybw)
        owqqw__hwml = builder.load(builder.gep(ximv__tjnt, [lsxs__bwqnc]))
        builder.store(owqqw__hwml, builder.gep(cgr__ahvwn, [dza__kdm]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ctng__edpm, ind, str, kbgtq__njhf = args
        ctng__edpm = context.make_array(sig.args[0])(context, builder,
            ctng__edpm)
        bfoam__jyiet = builder.gep(ctng__edpm.data, [ind])
        cgutils.raw_memcpy(builder, bfoam__jyiet, str, kbgtq__njhf, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        bfoam__jyiet, ind, yyid__jtc, kbgtq__njhf = args
        bfoam__jyiet = builder.gep(bfoam__jyiet, [ind])
        cgutils.raw_memcpy(builder, bfoam__jyiet, yyid__jtc, kbgtq__njhf, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    bha__jem = np.int64(getitem_str_offset(A, i))
    xqlyf__vkx = np.int64(getitem_str_offset(A, i + 1))
    l = xqlyf__vkx - bha__jem
    vzzoj__lqu = get_data_ptr_ind(A, bha__jem)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(vzzoj__lqu, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    mjz__rkszf = getitem_str_offset(A, i)
    zwy__qae = getitem_str_offset(A, i + 1)
    kwkyd__bkz = zwy__qae - mjz__rkszf
    glkil__rhwk = getitem_str_offset(B, j)
    sbuxe__swocm = glkil__rhwk + kwkyd__bkz
    setitem_str_offset(B, j + 1, sbuxe__swocm)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if kwkyd__bkz != 0:
        ubpkl__nwqv = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(ubpkl__nwqv, np.
            int64(glkil__rhwk), np.int64(sbuxe__swocm))
        hht__ovvmj = get_data_ptr(B).data
        obii__covn = get_data_ptr(A).data
        memcpy_region(hht__ovvmj, glkil__rhwk, obii__covn, mjz__rkszf,
            kwkyd__bkz, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    lsxs__bwqnc = len(str_arr)
    wbtr__bhdh = np.empty(lsxs__bwqnc, np.bool_)
    for i in range(lsxs__bwqnc):
        wbtr__bhdh[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return wbtr__bhdh


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            lsxs__bwqnc = len(data)
            l = []
            for i in range(lsxs__bwqnc):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        age__vvnp = data.count
        kqw__kitgv = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(age__vvnp)]
        if is_overload_true(str_null_bools):
            kqw__kitgv += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(age__vvnp) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        ypunv__xjjy = 'def f(data, str_null_bools=None):\n'
        ypunv__xjjy += '  return ({}{})\n'.format(', '.join(kqw__kitgv), 
            ',' if age__vvnp == 1 else '')
        rygou__fhqa = {}
        exec(ypunv__xjjy, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, rygou__fhqa)
        nkb__ngod = rygou__fhqa['f']
        return nkb__ngod
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                lsxs__bwqnc = len(list_data)
                for i in range(lsxs__bwqnc):
                    yyid__jtc = list_data[i]
                    str_arr[i] = yyid__jtc
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                lsxs__bwqnc = len(list_data)
                for i in range(lsxs__bwqnc):
                    yyid__jtc = list_data[i]
                    str_arr[i] = yyid__jtc
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        age__vvnp = str_arr.count
        kpvf__ueoxu = 0
        ypunv__xjjy = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(age__vvnp):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                ypunv__xjjy += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, age__vvnp + kpvf__ueoxu))
                kpvf__ueoxu += 1
            else:
                ypunv__xjjy += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        ypunv__xjjy += '  return\n'
        rygou__fhqa = {}
        exec(ypunv__xjjy, {'cp_str_list_to_array': cp_str_list_to_array},
            rygou__fhqa)
        octfw__cql = rygou__fhqa['f']
        return octfw__cql
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            lsxs__bwqnc = len(str_list)
            str_arr = pre_alloc_string_array(lsxs__bwqnc, -1)
            for i in range(lsxs__bwqnc):
                yyid__jtc = str_list[i]
                str_arr[i] = yyid__jtc
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            lsxs__bwqnc = len(A)
            qjklg__ylw = 0
            for i in range(lsxs__bwqnc):
                yyid__jtc = A[i]
                qjklg__ylw += get_utf8_size(yyid__jtc)
            return qjklg__ylw
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        lsxs__bwqnc = len(arr)
        n_chars = num_total_chars(arr)
        idddg__pnq = pre_alloc_string_array(lsxs__bwqnc, np.int64(n_chars))
        copy_str_arr_slice(idddg__pnq, arr, lsxs__bwqnc)
        return idddg__pnq
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
    ypunv__xjjy = 'def f(in_seq):\n'
    ypunv__xjjy += '    n_strs = len(in_seq)\n'
    ypunv__xjjy += '    A = pre_alloc_string_array(n_strs, -1)\n'
    ypunv__xjjy += '    return A\n'
    rygou__fhqa = {}
    exec(ypunv__xjjy, {'pre_alloc_string_array': pre_alloc_string_array},
        rygou__fhqa)
    wrurf__zwf = rygou__fhqa['f']
    return wrurf__zwf


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        ttsxu__vzce = 'pre_alloc_binary_array'
    else:
        ttsxu__vzce = 'pre_alloc_string_array'
    ypunv__xjjy = 'def f(in_seq):\n'
    ypunv__xjjy += '    n_strs = len(in_seq)\n'
    ypunv__xjjy += f'    A = {ttsxu__vzce}(n_strs, -1)\n'
    ypunv__xjjy += '    for i in range(n_strs):\n'
    ypunv__xjjy += '        A[i] = in_seq[i]\n'
    ypunv__xjjy += '    return A\n'
    rygou__fhqa = {}
    exec(ypunv__xjjy, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, rygou__fhqa)
    wrurf__zwf = rygou__fhqa['f']
    return wrurf__zwf


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        uiw__tgbs = builder.add(gupzd__isw.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        gszz__pzekl = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        dxtxz__hixh = builder.mul(uiw__tgbs, gszz__pzekl)
        gwro__brt = context.make_array(offset_arr_type)(context, builder,
            gupzd__isw.offsets).data
        cgutils.memset(builder, gwro__brt, dxtxz__hixh, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        lwt__ihitp = gupzd__isw.n_arrays
        dxtxz__hixh = builder.lshr(builder.add(lwt__ihitp, lir.Constant(lir
            .IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        jmeyq__fyyd = context.make_array(null_bitmap_arr_type)(context,
            builder, gupzd__isw.null_bitmap).data
        cgutils.memset(builder, jmeyq__fyyd, dxtxz__hixh, 0)
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
    icyo__xvq = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        cawl__bpgb = len(len_arr)
        for i in range(cawl__bpgb):
            offsets[i] = icyo__xvq
            icyo__xvq += len_arr[i]
        offsets[cawl__bpgb] = icyo__xvq
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    ltu__mcdjr = i // 8
    yayf__dcexk = getitem_str_bitmap(bits, ltu__mcdjr)
    yayf__dcexk ^= np.uint8(-np.uint8(bit_is_set) ^ yayf__dcexk) & kBitmask[
        i % 8]
    setitem_str_bitmap(bits, ltu__mcdjr, yayf__dcexk)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    nwc__eir = get_null_bitmap_ptr(out_str_arr)
    htu__fizuk = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        iyeik__gyape = get_bit_bitmap(htu__fizuk, j)
        set_bit_to(nwc__eir, out_start + j, iyeik__gyape)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, fzw__ilk, pbyc__ydmb, ffrji__bfa = args
        dohvz__byt = _get_str_binary_arr_payload(context, builder, fzw__ilk,
            string_array_type)
        qax__lfg = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        ximv__tjnt = context.make_helper(builder, offset_arr_type,
            dohvz__byt.offsets).data
        cgr__ahvwn = context.make_helper(builder, offset_arr_type, qax__lfg
            .offsets).data
        gtj__zxt = context.make_helper(builder, char_arr_type, dohvz__byt.data
            ).data
        umi__lmqwi = context.make_helper(builder, char_arr_type, qax__lfg.data
            ).data
        num_total_chars = _get_num_total_chars(builder, ximv__tjnt,
            dohvz__byt.n_arrays)
        udg__gcm = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        gopw__capnz = cgutils.get_or_insert_function(builder.module,
            udg__gcm, name='set_string_array_range')
        builder.call(gopw__capnz, [cgr__ahvwn, umi__lmqwi, ximv__tjnt,
            gtj__zxt, pbyc__ydmb, ffrji__bfa, dohvz__byt.n_arrays,
            num_total_chars])
        ckxwv__mjzo = context.typing_context.resolve_value_type(
            copy_nulls_range)
        ggczv__hymh = ckxwv__mjzo.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        rmbom__cdtc = context.get_function(ckxwv__mjzo, ggczv__hymh)
        rmbom__cdtc(builder, (out_arr, fzw__ilk, pbyc__ydmb))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    itqs__ptqzn = c.context.make_helper(c.builder, typ, val)
    reju__wlh = ArrayItemArrayType(char_arr_type)
    gupzd__isw = _get_array_item_arr_payload(c.context, c.builder,
        reju__wlh, itqs__ptqzn.data)
    zowk__srtym = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    ebt__gsqkc = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        ebt__gsqkc = 'pd_array_from_string_array'
    udg__gcm = lir.FunctionType(c.context.get_argument_type(types.pyobject),
        [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    tmn__jjy = cgutils.get_or_insert_function(c.builder.module, udg__gcm,
        name=ebt__gsqkc)
    cizb__bnnh = c.context.make_array(offset_arr_type)(c.context, c.builder,
        gupzd__isw.offsets).data
    vzzoj__lqu = c.context.make_array(char_arr_type)(c.context, c.builder,
        gupzd__isw.data).data
    jmeyq__fyyd = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, gupzd__isw.null_bitmap).data
    arr = c.builder.call(tmn__jjy, [gupzd__isw.n_arrays, cizb__bnnh,
        vzzoj__lqu, jmeyq__fyyd, zowk__srtym])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        jmeyq__fyyd = context.make_array(null_bitmap_arr_type)(context,
            builder, gupzd__isw.null_bitmap).data
        rdb__idt = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        cftko__joot = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        yayf__dcexk = builder.load(builder.gep(jmeyq__fyyd, [rdb__idt],
            inbounds=True))
        svjiw__rhif = lir.ArrayType(lir.IntType(8), 8)
        hxncc__ldmsq = cgutils.alloca_once_value(builder, lir.Constant(
            svjiw__rhif, (1, 2, 4, 8, 16, 32, 64, 128)))
        xur__pzy = builder.load(builder.gep(hxncc__ldmsq, [lir.Constant(lir
            .IntType(64), 0), cftko__joot], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(yayf__dcexk,
            xur__pzy), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        rdb__idt = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        cftko__joot = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        jmeyq__fyyd = context.make_array(null_bitmap_arr_type)(context,
            builder, gupzd__isw.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, gupzd__isw.
            offsets).data
        bzd__ldtc = builder.gep(jmeyq__fyyd, [rdb__idt], inbounds=True)
        yayf__dcexk = builder.load(bzd__ldtc)
        svjiw__rhif = lir.ArrayType(lir.IntType(8), 8)
        hxncc__ldmsq = cgutils.alloca_once_value(builder, lir.Constant(
            svjiw__rhif, (1, 2, 4, 8, 16, 32, 64, 128)))
        xur__pzy = builder.load(builder.gep(hxncc__ldmsq, [lir.Constant(lir
            .IntType(64), 0), cftko__joot], inbounds=True))
        xur__pzy = builder.xor(xur__pzy, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(yayf__dcexk, xur__pzy), bzd__ldtc)
        if str_arr_typ == string_array_type:
            dndpy__gmi = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            urat__bxl = builder.icmp_unsigned('!=', dndpy__gmi, gupzd__isw.
                n_arrays)
            with builder.if_then(urat__bxl):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [dndpy__gmi]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        rdb__idt = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        cftko__joot = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        jmeyq__fyyd = context.make_array(null_bitmap_arr_type)(context,
            builder, gupzd__isw.null_bitmap).data
        bzd__ldtc = builder.gep(jmeyq__fyyd, [rdb__idt], inbounds=True)
        yayf__dcexk = builder.load(bzd__ldtc)
        svjiw__rhif = lir.ArrayType(lir.IntType(8), 8)
        hxncc__ldmsq = cgutils.alloca_once_value(builder, lir.Constant(
            svjiw__rhif, (1, 2, 4, 8, 16, 32, 64, 128)))
        xur__pzy = builder.load(builder.gep(hxncc__ldmsq, [lir.Constant(lir
            .IntType(64), 0), cftko__joot], inbounds=True))
        builder.store(builder.or_(yayf__dcexk, xur__pzy), bzd__ldtc)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        dxtxz__hixh = builder.udiv(builder.add(gupzd__isw.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        jmeyq__fyyd = context.make_array(null_bitmap_arr_type)(context,
            builder, gupzd__isw.null_bitmap).data
        cgutils.memset(builder, jmeyq__fyyd, dxtxz__hixh, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    pkwn__parx = context.make_helper(builder, string_array_type, str_arr)
    reju__wlh = ArrayItemArrayType(char_arr_type)
    pthu__izhos = context.make_helper(builder, reju__wlh, pkwn__parx.data)
    ebyj__tflf = ArrayItemArrayPayloadType(reju__wlh)
    qfdw__nit = context.nrt.meminfo_data(builder, pthu__izhos.meminfo)
    azh__gof = builder.bitcast(qfdw__nit, context.get_value_type(ebyj__tflf
        ).as_pointer())
    return azh__gof


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        xkmn__lht, rocic__pzx = args
        xxng__ebx = _get_str_binary_arr_data_payload_ptr(context, builder,
            rocic__pzx)
        tffg__xbjxi = _get_str_binary_arr_data_payload_ptr(context, builder,
            xkmn__lht)
        jvblm__ixtz = _get_str_binary_arr_payload(context, builder,
            rocic__pzx, sig.args[1])
        jrngi__fxkh = _get_str_binary_arr_payload(context, builder,
            xkmn__lht, sig.args[0])
        context.nrt.incref(builder, char_arr_type, jvblm__ixtz.data)
        context.nrt.incref(builder, offset_arr_type, jvblm__ixtz.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, jvblm__ixtz.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, jrngi__fxkh.data)
        context.nrt.decref(builder, offset_arr_type, jrngi__fxkh.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, jrngi__fxkh.
            null_bitmap)
        builder.store(builder.load(xxng__ebx), tffg__xbjxi)
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
        lsxs__bwqnc = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return lsxs__bwqnc
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, bfoam__jyiet, nexz__nus = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder, arr, sig
            .args[0])
        offsets = context.make_helper(builder, offset_arr_type, gupzd__isw.
            offsets).data
        data = context.make_helper(builder, char_arr_type, gupzd__isw.data
            ).data
        udg__gcm = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        fvrs__tksk = cgutils.get_or_insert_function(builder.module,
            udg__gcm, name='setitem_string_array')
        xxtjo__acruo = context.get_constant(types.int32, -1)
        ndz__jmq = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, gupzd__isw
            .n_arrays)
        builder.call(fvrs__tksk, [offsets, data, num_total_chars, builder.
            extract_value(bfoam__jyiet, 0), nexz__nus, xxtjo__acruo,
            ndz__jmq, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    udg__gcm = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64)])
    anr__ilygv = cgutils.get_or_insert_function(builder.module, udg__gcm,
        name='is_na')
    return builder.call(anr__ilygv, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        pvvcf__xsre, mzy__ivle, age__vvnp, lgirc__hriz = args
        cgutils.raw_memcpy(builder, pvvcf__xsre, mzy__ivle, age__vvnp,
            lgirc__hriz)
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
        rtbnt__siex, wapb__jna = unicode_to_utf8_and_len(val)
        wgu__kdtx = getitem_str_offset(A, ind)
        iyz__gtm = getitem_str_offset(A, ind + 1)
        xsp__obxm = iyz__gtm - wgu__kdtx
        if xsp__obxm != wapb__jna:
            return False
        bfoam__jyiet = get_data_ptr_ind(A, wgu__kdtx)
        return memcmp(bfoam__jyiet, rtbnt__siex, wapb__jna) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        wgu__kdtx = getitem_str_offset(A, ind)
        xsp__obxm = bodo.libs.str_ext.int_to_str_len(val)
        hrvvy__uvy = wgu__kdtx + xsp__obxm
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            wgu__kdtx, hrvvy__uvy)
        bfoam__jyiet = get_data_ptr_ind(A, wgu__kdtx)
        inplace_int64_to_str(bfoam__jyiet, xsp__obxm, val)
        setitem_str_offset(A, ind + 1, wgu__kdtx + xsp__obxm)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        bfoam__jyiet, = args
        dzj__cmj = context.insert_const_string(builder.module, '<NA>')
        ddf__jpad = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, bfoam__jyiet, dzj__cmj, ddf__jpad, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    upqo__hydy = len('<NA>')

    def impl(A, ind):
        wgu__kdtx = getitem_str_offset(A, ind)
        hrvvy__uvy = wgu__kdtx + upqo__hydy
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            wgu__kdtx, hrvvy__uvy)
        bfoam__jyiet = get_data_ptr_ind(A, wgu__kdtx)
        inplace_set_NA_str(bfoam__jyiet)
        setitem_str_offset(A, ind + 1, wgu__kdtx + upqo__hydy)
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
            wgu__kdtx = getitem_str_offset(A, ind)
            iyz__gtm = getitem_str_offset(A, ind + 1)
            nexz__nus = iyz__gtm - wgu__kdtx
            bfoam__jyiet = get_data_ptr_ind(A, wgu__kdtx)
            plrll__hlhmv = decode_utf8(bfoam__jyiet, nexz__nus)
            return plrll__hlhmv
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            lsxs__bwqnc = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(lsxs__bwqnc):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            hht__ovvmj = get_data_ptr(out_arr).data
            obii__covn = get_data_ptr(A).data
            kpvf__ueoxu = 0
            dza__kdm = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(lsxs__bwqnc):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    fco__cem = get_str_arr_item_length(A, i)
                    if fco__cem == 1:
                        copy_single_char(hht__ovvmj, dza__kdm, obii__covn,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(hht__ovvmj, dza__kdm, obii__covn,
                            getitem_str_offset(A, i), fco__cem, 1)
                    dza__kdm += fco__cem
                    setitem_str_offset(out_arr, kpvf__ueoxu + 1, dza__kdm)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, kpvf__ueoxu)
                    else:
                        str_arr_set_not_na(out_arr, kpvf__ueoxu)
                    kpvf__ueoxu += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            lsxs__bwqnc = len(ind)
            out_arr = pre_alloc_string_array(lsxs__bwqnc, -1)
            kpvf__ueoxu = 0
            for i in range(lsxs__bwqnc):
                yyid__jtc = A[ind[i]]
                out_arr[kpvf__ueoxu] = yyid__jtc
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, kpvf__ueoxu)
                kpvf__ueoxu += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            lsxs__bwqnc = len(A)
            fagi__qcxug = numba.cpython.unicode._normalize_slice(ind,
                lsxs__bwqnc)
            hnzlx__tvvu = numba.cpython.unicode._slice_span(fagi__qcxug)
            if fagi__qcxug.step == 1:
                wgu__kdtx = getitem_str_offset(A, fagi__qcxug.start)
                iyz__gtm = getitem_str_offset(A, fagi__qcxug.stop)
                n_chars = iyz__gtm - wgu__kdtx
                idddg__pnq = pre_alloc_string_array(hnzlx__tvvu, np.int64(
                    n_chars))
                for i in range(hnzlx__tvvu):
                    idddg__pnq[i] = A[fagi__qcxug.start + i]
                    if str_arr_is_na(A, fagi__qcxug.start + i):
                        str_arr_set_na(idddg__pnq, i)
                return idddg__pnq
            else:
                idddg__pnq = pre_alloc_string_array(hnzlx__tvvu, -1)
                for i in range(hnzlx__tvvu):
                    idddg__pnq[i] = A[fagi__qcxug.start + i * fagi__qcxug.step]
                    if str_arr_is_na(A, fagi__qcxug.start + i * fagi__qcxug
                        .step):
                        str_arr_set_na(idddg__pnq, i)
                return idddg__pnq
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
    ikio__pzy = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(ikio__pzy)
        ziag__njkjt = 4

        def impl_scalar(A, idx, val):
            jze__qli = (val._length if val._is_ascii else ziag__njkjt * val
                ._length)
            ubpkl__nwqv = A._data
            wgu__kdtx = np.int64(getitem_str_offset(A, idx))
            hrvvy__uvy = wgu__kdtx + jze__qli
            bodo.libs.array_item_arr_ext.ensure_data_capacity(ubpkl__nwqv,
                wgu__kdtx, hrvvy__uvy)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                hrvvy__uvy, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                fagi__qcxug = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                bha__jem = fagi__qcxug.start
                ubpkl__nwqv = A._data
                wgu__kdtx = np.int64(getitem_str_offset(A, bha__jem))
                hrvvy__uvy = wgu__kdtx + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(ubpkl__nwqv,
                    wgu__kdtx, hrvvy__uvy)
                set_string_array_range(A, val, bha__jem, wgu__kdtx)
                zqy__xeg = 0
                for i in range(fagi__qcxug.start, fagi__qcxug.stop,
                    fagi__qcxug.step):
                    if str_arr_is_na(val, zqy__xeg):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    zqy__xeg += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                iknpi__fqmek = str_list_to_array(val)
                A[idx] = iknpi__fqmek
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                fagi__qcxug = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(fagi__qcxug.start, fagi__qcxug.stop,
                    fagi__qcxug.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(ikio__pzy)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                lsxs__bwqnc = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(lsxs__bwqnc, -1)
                for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
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
                lsxs__bwqnc = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(lsxs__bwqnc, -1)
                vfjn__wfxg = 0
                for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, vfjn__wfxg):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, vfjn__wfxg)
                        else:
                            out_arr[i] = str(val[vfjn__wfxg])
                        vfjn__wfxg += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(ikio__pzy)
    raise BodoError(ikio__pzy)


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
    fiu__ldafb = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(fiu__ldafb, (types.Float, types.Integer)
        ) and fiu__ldafb not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(fiu__ldafb, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            lsxs__bwqnc = len(A)
            B = np.empty(lsxs__bwqnc, fiu__ldafb)
            for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif fiu__ldafb == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            lsxs__bwqnc = len(A)
            B = np.empty(lsxs__bwqnc, fiu__ldafb)
            for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif fiu__ldafb == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            lsxs__bwqnc = len(A)
            B = np.empty(lsxs__bwqnc, fiu__ldafb)
            for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            lsxs__bwqnc = len(A)
            B = np.empty(lsxs__bwqnc, fiu__ldafb)
            for i in numba.parfors.parfor.internal_prange(lsxs__bwqnc):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        bfoam__jyiet, nexz__nus = args
        pgax__lhz = context.get_python_api(builder)
        asp__zkx = pgax__lhz.string_from_string_and_size(bfoam__jyiet,
            nexz__nus)
        jdh__mjb = pgax__lhz.to_native_value(string_type, asp__zkx).value
        fjc__kcb = cgutils.create_struct_proxy(string_type)(context,
            builder, jdh__mjb)
        fjc__kcb.hash = fjc__kcb.hash.type(-1)
        pgax__lhz.decref(asp__zkx)
        return fjc__kcb._getvalue()
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
        dbi__jakzs, arr, ind, uannu__hflgj = args
        gupzd__isw = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, gupzd__isw.
            offsets).data
        data = context.make_helper(builder, char_arr_type, gupzd__isw.data
            ).data
        udg__gcm = lir.FunctionType(lir.IntType(32), [dbi__jakzs.type, lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        opicw__kquti = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            opicw__kquti = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        xgs__ycgux = cgutils.get_or_insert_function(builder.module,
            udg__gcm, opicw__kquti)
        return builder.call(xgs__ycgux, [dbi__jakzs, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    zowk__srtym = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    udg__gcm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(32)])
    qzhsf__oso = cgutils.get_or_insert_function(c.builder.module, udg__gcm,
        name='string_array_from_sequence')
    ooy__bfkg = c.builder.call(qzhsf__oso, [val, zowk__srtym])
    reju__wlh = ArrayItemArrayType(char_arr_type)
    pthu__izhos = c.context.make_helper(c.builder, reju__wlh)
    pthu__izhos.meminfo = ooy__bfkg
    pkwn__parx = c.context.make_helper(c.builder, typ)
    ubpkl__nwqv = pthu__izhos._getvalue()
    pkwn__parx.data = ubpkl__nwqv
    bax__hmoaw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pkwn__parx._getvalue(), is_error=bax__hmoaw)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    lsxs__bwqnc = len(pyval)
    dza__kdm = 0
    jjtk__caqcj = np.empty(lsxs__bwqnc + 1, np_offset_type)
    qfgje__maeb = []
    znrzc__ctdnb = np.empty(lsxs__bwqnc + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        jjtk__caqcj[i] = dza__kdm
        zewk__wjog = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(znrzc__ctdnb, i, int(not
            zewk__wjog))
        if zewk__wjog:
            continue
        juoow__egdmv = list(s.encode()) if isinstance(s, str) else list(s)
        qfgje__maeb.extend(juoow__egdmv)
        dza__kdm += len(juoow__egdmv)
    jjtk__caqcj[lsxs__bwqnc] = dza__kdm
    mcnlt__dmger = np.array(qfgje__maeb, np.uint8)
    sdg__anmhd = context.get_constant(types.int64, lsxs__bwqnc)
    nge__zstlp = context.get_constant_generic(builder, char_arr_type,
        mcnlt__dmger)
    bbe__bgqci = context.get_constant_generic(builder, offset_arr_type,
        jjtk__caqcj)
    clus__fxlj = context.get_constant_generic(builder, null_bitmap_arr_type,
        znrzc__ctdnb)
    gupzd__isw = lir.Constant.literal_struct([sdg__anmhd, nge__zstlp,
        bbe__bgqci, clus__fxlj])
    gupzd__isw = cgutils.global_constant(builder, '.const.payload', gupzd__isw
        ).bitcast(cgutils.voidptr_t)
    fsi__zwoeo = context.get_constant(types.int64, -1)
    zhp__ygqb = context.get_constant_null(types.voidptr)
    ppxk__xqb = lir.Constant.literal_struct([fsi__zwoeo, zhp__ygqb,
        zhp__ygqb, gupzd__isw, fsi__zwoeo])
    ppxk__xqb = cgutils.global_constant(builder, '.const.meminfo', ppxk__xqb
        ).bitcast(cgutils.voidptr_t)
    ubpkl__nwqv = lir.Constant.literal_struct([ppxk__xqb])
    pkwn__parx = lir.Constant.literal_struct([ubpkl__nwqv])
    return pkwn__parx


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
