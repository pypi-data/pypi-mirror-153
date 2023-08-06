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
        kdjv__ovwb = ArrayItemArrayType(char_arr_type)
        mmzq__dutm = [('data', kdjv__ovwb)]
        models.StructModel.__init__(self, dmm, fe_type, mmzq__dutm)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        rrax__qkmgv, = args
        fjjj__qfit = context.make_helper(builder, string_array_type)
        fjjj__qfit.data = rrax__qkmgv
        context.nrt.incref(builder, data_typ, rrax__qkmgv)
        return fjjj__qfit._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    lvau__sbf = c.context.insert_const_string(c.builder.module, 'pandas')
    ftt__cylzo = c.pyapi.import_module_noblock(lvau__sbf)
    qgf__gyclx = c.pyapi.call_method(ftt__cylzo, 'StringDtype', ())
    c.pyapi.decref(ftt__cylzo)
    return qgf__gyclx


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        ioplv__vhg = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs
            )
        if ioplv__vhg is not None:
            return ioplv__vhg
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                nor__sccts = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(nor__sccts)
                for i in numba.parfors.parfor.internal_prange(nor__sccts):
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
                nor__sccts = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(nor__sccts)
                for i in numba.parfors.parfor.internal_prange(nor__sccts):
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
                nor__sccts = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(nor__sccts)
                for i in numba.parfors.parfor.internal_prange(nor__sccts):
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
    lgs__nenzo = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    pzkkg__gpk = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and pzkkg__gpk or lgs__nenzo and is_str_arr_type(
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
    uafiu__imibf = context.make_helper(builder, arr_typ, arr_value)
    kdjv__ovwb = ArrayItemArrayType(char_arr_type)
    dlm__idk = _get_array_item_arr_payload(context, builder, kdjv__ovwb,
        uafiu__imibf.data)
    return dlm__idk


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return dlm__idk.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        cgfdu__upicn = context.make_helper(builder, offset_arr_type,
            dlm__idk.offsets).data
        return _get_num_total_chars(builder, cgfdu__upicn, dlm__idk.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        vvxtx__madd = context.make_helper(builder, offset_arr_type,
            dlm__idk.offsets)
        ter__pxrv = context.make_helper(builder, offset_ctypes_type)
        ter__pxrv.data = builder.bitcast(vvxtx__madd.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        ter__pxrv.meminfo = vvxtx__madd.meminfo
        qgf__gyclx = ter__pxrv._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            qgf__gyclx)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        rrax__qkmgv = context.make_helper(builder, char_arr_type, dlm__idk.data
            )
        ter__pxrv = context.make_helper(builder, data_ctypes_type)
        ter__pxrv.data = rrax__qkmgv.data
        ter__pxrv.meminfo = rrax__qkmgv.meminfo
        qgf__gyclx = ter__pxrv._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, qgf__gyclx
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        pspbk__slwe, ind = args
        dlm__idk = _get_str_binary_arr_payload(context, builder,
            pspbk__slwe, sig.args[0])
        rrax__qkmgv = context.make_helper(builder, char_arr_type, dlm__idk.data
            )
        ter__pxrv = context.make_helper(builder, data_ctypes_type)
        ter__pxrv.data = builder.gep(rrax__qkmgv.data, [ind])
        ter__pxrv.meminfo = rrax__qkmgv.meminfo
        qgf__gyclx = ter__pxrv._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, qgf__gyclx
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        krgwe__agsnv, bucpl__evigb, irmj__bvpm, qawn__uffo = args
        nkt__dppo = builder.bitcast(builder.gep(krgwe__agsnv, [bucpl__evigb
            ]), lir.IntType(8).as_pointer())
        ybm__tkm = builder.bitcast(builder.gep(irmj__bvpm, [qawn__uffo]),
            lir.IntType(8).as_pointer())
        sxm__hpbd = builder.load(ybm__tkm)
        builder.store(sxm__hpbd, nkt__dppo)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        rglfx__evdp = context.make_helper(builder, null_bitmap_arr_type,
            dlm__idk.null_bitmap)
        ter__pxrv = context.make_helper(builder, data_ctypes_type)
        ter__pxrv.data = rglfx__evdp.data
        ter__pxrv.meminfo = rglfx__evdp.meminfo
        qgf__gyclx = ter__pxrv._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, qgf__gyclx
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        cgfdu__upicn = context.make_helper(builder, offset_arr_type,
            dlm__idk.offsets).data
        return builder.load(builder.gep(cgfdu__upicn, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, dlm__idk.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        dttsm__hjvx, ind = args
        if in_bitmap_typ == data_ctypes_type:
            ter__pxrv = context.make_helper(builder, data_ctypes_type,
                dttsm__hjvx)
            dttsm__hjvx = ter__pxrv.data
        return builder.load(builder.gep(dttsm__hjvx, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        dttsm__hjvx, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            ter__pxrv = context.make_helper(builder, data_ctypes_type,
                dttsm__hjvx)
            dttsm__hjvx = ter__pxrv.data
        builder.store(val, builder.gep(dttsm__hjvx, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        zdez__yigo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qvd__hvu = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        zaeko__aja = context.make_helper(builder, offset_arr_type,
            zdez__yigo.offsets).data
        yeg__zho = context.make_helper(builder, offset_arr_type, qvd__hvu.
            offsets).data
        oroa__nbt = context.make_helper(builder, char_arr_type, zdez__yigo.data
            ).data
        lte__yaff = context.make_helper(builder, char_arr_type, qvd__hvu.data
            ).data
        qsil__iwke = context.make_helper(builder, null_bitmap_arr_type,
            zdez__yigo.null_bitmap).data
        zog__bjsw = context.make_helper(builder, null_bitmap_arr_type,
            qvd__hvu.null_bitmap).data
        xrh__skvfr = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, yeg__zho, zaeko__aja, xrh__skvfr)
        cgutils.memcpy(builder, lte__yaff, oroa__nbt, builder.load(builder.
            gep(zaeko__aja, [ind])))
        ler__kbgq = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        pjbiz__tjm = builder.lshr(ler__kbgq, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, zog__bjsw, qsil__iwke, pjbiz__tjm)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        zdez__yigo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qvd__hvu = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        zaeko__aja = context.make_helper(builder, offset_arr_type,
            zdez__yigo.offsets).data
        oroa__nbt = context.make_helper(builder, char_arr_type, zdez__yigo.data
            ).data
        lte__yaff = context.make_helper(builder, char_arr_type, qvd__hvu.data
            ).data
        num_total_chars = _get_num_total_chars(builder, zaeko__aja,
            zdez__yigo.n_arrays)
        cgutils.memcpy(builder, lte__yaff, oroa__nbt, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        zdez__yigo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qvd__hvu = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        zaeko__aja = context.make_helper(builder, offset_arr_type,
            zdez__yigo.offsets).data
        yeg__zho = context.make_helper(builder, offset_arr_type, qvd__hvu.
            offsets).data
        qsil__iwke = context.make_helper(builder, null_bitmap_arr_type,
            zdez__yigo.null_bitmap).data
        nor__sccts = zdez__yigo.n_arrays
        vjld__xpowr = context.get_constant(offset_type, 0)
        vasux__xoav = cgutils.alloca_once_value(builder, vjld__xpowr)
        with cgutils.for_range(builder, nor__sccts) as aroch__fnyh:
            vksd__pikza = lower_is_na(context, builder, qsil__iwke,
                aroch__fnyh.index)
            with cgutils.if_likely(builder, builder.not_(vksd__pikza)):
                opkr__aoayz = builder.load(builder.gep(zaeko__aja, [
                    aroch__fnyh.index]))
                uuao__zvxdi = builder.load(vasux__xoav)
                builder.store(opkr__aoayz, builder.gep(yeg__zho, [uuao__zvxdi])
                    )
                builder.store(builder.add(uuao__zvxdi, lir.Constant(context
                    .get_value_type(offset_type), 1)), vasux__xoav)
        uuao__zvxdi = builder.load(vasux__xoav)
        opkr__aoayz = builder.load(builder.gep(zaeko__aja, [nor__sccts]))
        builder.store(opkr__aoayz, builder.gep(yeg__zho, [uuao__zvxdi]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        nbsfh__urqbh, ind, str, uxqtv__sjf = args
        nbsfh__urqbh = context.make_array(sig.args[0])(context, builder,
            nbsfh__urqbh)
        doni__wur = builder.gep(nbsfh__urqbh.data, [ind])
        cgutils.raw_memcpy(builder, doni__wur, str, uxqtv__sjf, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        doni__wur, ind, izq__canm, uxqtv__sjf = args
        doni__wur = builder.gep(doni__wur, [ind])
        cgutils.raw_memcpy(builder, doni__wur, izq__canm, uxqtv__sjf, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    pkdw__uebtb = np.int64(getitem_str_offset(A, i))
    gzi__hgp = np.int64(getitem_str_offset(A, i + 1))
    l = gzi__hgp - pkdw__uebtb
    fjry__zwju = get_data_ptr_ind(A, pkdw__uebtb)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(fjry__zwju, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    mwk__tlgrx = getitem_str_offset(A, i)
    qsqa__xgeyd = getitem_str_offset(A, i + 1)
    nqoi__jtj = qsqa__xgeyd - mwk__tlgrx
    fvb__znx = getitem_str_offset(B, j)
    zarjz__tlxhh = fvb__znx + nqoi__jtj
    setitem_str_offset(B, j + 1, zarjz__tlxhh)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if nqoi__jtj != 0:
        rrax__qkmgv = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(rrax__qkmgv, np.
            int64(fvb__znx), np.int64(zarjz__tlxhh))
        tvipd__wea = get_data_ptr(B).data
        pwms__bhbt = get_data_ptr(A).data
        memcpy_region(tvipd__wea, fvb__znx, pwms__bhbt, mwk__tlgrx,
            nqoi__jtj, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    nor__sccts = len(str_arr)
    ywljw__meh = np.empty(nor__sccts, np.bool_)
    for i in range(nor__sccts):
        ywljw__meh[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return ywljw__meh


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            nor__sccts = len(data)
            l = []
            for i in range(nor__sccts):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        clkhk__ukhky = data.count
        pwkcq__ooanf = ['to_list_if_immutable_arr(data[{}])'.format(i) for
            i in range(clkhk__ukhky)]
        if is_overload_true(str_null_bools):
            pwkcq__ooanf += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(clkhk__ukhky) if is_str_arr_type(data.types[i]) or 
                data.types[i] == binary_array_type]
        cpat__uguxp = 'def f(data, str_null_bools=None):\n'
        cpat__uguxp += '  return ({}{})\n'.format(', '.join(pwkcq__ooanf), 
            ',' if clkhk__ukhky == 1 else '')
        ugt__umrqa = {}
        exec(cpat__uguxp, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, ugt__umrqa)
        xmdg__emvxe = ugt__umrqa['f']
        return xmdg__emvxe
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                nor__sccts = len(list_data)
                for i in range(nor__sccts):
                    izq__canm = list_data[i]
                    str_arr[i] = izq__canm
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                nor__sccts = len(list_data)
                for i in range(nor__sccts):
                    izq__canm = list_data[i]
                    str_arr[i] = izq__canm
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        clkhk__ukhky = str_arr.count
        hcqt__uafiq = 0
        cpat__uguxp = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(clkhk__ukhky):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                cpat__uguxp += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, clkhk__ukhky + hcqt__uafiq))
                hcqt__uafiq += 1
            else:
                cpat__uguxp += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        cpat__uguxp += '  return\n'
        ugt__umrqa = {}
        exec(cpat__uguxp, {'cp_str_list_to_array': cp_str_list_to_array},
            ugt__umrqa)
        mkvy__irziy = ugt__umrqa['f']
        return mkvy__irziy
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            nor__sccts = len(str_list)
            str_arr = pre_alloc_string_array(nor__sccts, -1)
            for i in range(nor__sccts):
                izq__canm = str_list[i]
                str_arr[i] = izq__canm
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            nor__sccts = len(A)
            beskw__vjlhy = 0
            for i in range(nor__sccts):
                izq__canm = A[i]
                beskw__vjlhy += get_utf8_size(izq__canm)
            return beskw__vjlhy
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        nor__sccts = len(arr)
        n_chars = num_total_chars(arr)
        hpe__jmex = pre_alloc_string_array(nor__sccts, np.int64(n_chars))
        copy_str_arr_slice(hpe__jmex, arr, nor__sccts)
        return hpe__jmex
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
    cpat__uguxp = 'def f(in_seq):\n'
    cpat__uguxp += '    n_strs = len(in_seq)\n'
    cpat__uguxp += '    A = pre_alloc_string_array(n_strs, -1)\n'
    cpat__uguxp += '    return A\n'
    ugt__umrqa = {}
    exec(cpat__uguxp, {'pre_alloc_string_array': pre_alloc_string_array},
        ugt__umrqa)
    pjo__wmqg = ugt__umrqa['f']
    return pjo__wmqg


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        lpxh__kid = 'pre_alloc_binary_array'
    else:
        lpxh__kid = 'pre_alloc_string_array'
    cpat__uguxp = 'def f(in_seq):\n'
    cpat__uguxp += '    n_strs = len(in_seq)\n'
    cpat__uguxp += f'    A = {lpxh__kid}(n_strs, -1)\n'
    cpat__uguxp += '    for i in range(n_strs):\n'
    cpat__uguxp += '        A[i] = in_seq[i]\n'
    cpat__uguxp += '    return A\n'
    ugt__umrqa = {}
    exec(cpat__uguxp, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, ugt__umrqa)
    pjo__wmqg = ugt__umrqa['f']
    return pjo__wmqg


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        sunau__pws = builder.add(dlm__idk.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        wbz__skurf = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        pjbiz__tjm = builder.mul(sunau__pws, wbz__skurf)
        jpzf__hpt = context.make_array(offset_arr_type)(context, builder,
            dlm__idk.offsets).data
        cgutils.memset(builder, jpzf__hpt, pjbiz__tjm, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        hhql__xeo = dlm__idk.n_arrays
        pjbiz__tjm = builder.lshr(builder.add(hhql__xeo, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        nepkz__zzya = context.make_array(null_bitmap_arr_type)(context,
            builder, dlm__idk.null_bitmap).data
        cgutils.memset(builder, nepkz__zzya, pjbiz__tjm, 0)
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
    tkzw__pyu = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        ouukc__gurpa = len(len_arr)
        for i in range(ouukc__gurpa):
            offsets[i] = tkzw__pyu
            tkzw__pyu += len_arr[i]
        offsets[ouukc__gurpa] = tkzw__pyu
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    tgoit__nwrhy = i // 8
    ghqx__qjds = getitem_str_bitmap(bits, tgoit__nwrhy)
    ghqx__qjds ^= np.uint8(-np.uint8(bit_is_set) ^ ghqx__qjds) & kBitmask[i % 8
        ]
    setitem_str_bitmap(bits, tgoit__nwrhy, ghqx__qjds)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    eqri__gql = get_null_bitmap_ptr(out_str_arr)
    ppdmm__lua = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        qhgns__ndd = get_bit_bitmap(ppdmm__lua, j)
        set_bit_to(eqri__gql, out_start + j, qhgns__ndd)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, pspbk__slwe, apr__lcmh, dwe__rwikx = args
        zdez__yigo = _get_str_binary_arr_payload(context, builder,
            pspbk__slwe, string_array_type)
        qvd__hvu = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        zaeko__aja = context.make_helper(builder, offset_arr_type,
            zdez__yigo.offsets).data
        yeg__zho = context.make_helper(builder, offset_arr_type, qvd__hvu.
            offsets).data
        oroa__nbt = context.make_helper(builder, char_arr_type, zdez__yigo.data
            ).data
        lte__yaff = context.make_helper(builder, char_arr_type, qvd__hvu.data
            ).data
        num_total_chars = _get_num_total_chars(builder, zaeko__aja,
            zdez__yigo.n_arrays)
        nnfz__jcwey = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        eyijj__onatx = cgutils.get_or_insert_function(builder.module,
            nnfz__jcwey, name='set_string_array_range')
        builder.call(eyijj__onatx, [yeg__zho, lte__yaff, zaeko__aja,
            oroa__nbt, apr__lcmh, dwe__rwikx, zdez__yigo.n_arrays,
            num_total_chars])
        vnsx__ewozd = context.typing_context.resolve_value_type(
            copy_nulls_range)
        hsoj__bwz = vnsx__ewozd.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        huijn__rxos = context.get_function(vnsx__ewozd, hsoj__bwz)
        huijn__rxos(builder, (out_arr, pspbk__slwe, apr__lcmh))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    sub__lbzh = c.context.make_helper(c.builder, typ, val)
    kdjv__ovwb = ArrayItemArrayType(char_arr_type)
    dlm__idk = _get_array_item_arr_payload(c.context, c.builder, kdjv__ovwb,
        sub__lbzh.data)
    cztws__xhzig = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    olbmr__gpr = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        olbmr__gpr = 'pd_array_from_string_array'
    nnfz__jcwey = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    mvcd__qqobs = cgutils.get_or_insert_function(c.builder.module,
        nnfz__jcwey, name=olbmr__gpr)
    cgfdu__upicn = c.context.make_array(offset_arr_type)(c.context, c.
        builder, dlm__idk.offsets).data
    fjry__zwju = c.context.make_array(char_arr_type)(c.context, c.builder,
        dlm__idk.data).data
    nepkz__zzya = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, dlm__idk.null_bitmap).data
    arr = c.builder.call(mvcd__qqobs, [dlm__idk.n_arrays, cgfdu__upicn,
        fjry__zwju, nepkz__zzya, cztws__xhzig])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        nepkz__zzya = context.make_array(null_bitmap_arr_type)(context,
            builder, dlm__idk.null_bitmap).data
        fzpl__kkc = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        abe__xbu = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        ghqx__qjds = builder.load(builder.gep(nepkz__zzya, [fzpl__kkc],
            inbounds=True))
        ixdqr__pgeix = lir.ArrayType(lir.IntType(8), 8)
        xkhw__xkgz = cgutils.alloca_once_value(builder, lir.Constant(
            ixdqr__pgeix, (1, 2, 4, 8, 16, 32, 64, 128)))
        kks__nqvie = builder.load(builder.gep(xkhw__xkgz, [lir.Constant(lir
            .IntType(64), 0), abe__xbu], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(ghqx__qjds,
            kks__nqvie), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        fzpl__kkc = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        abe__xbu = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        nepkz__zzya = context.make_array(null_bitmap_arr_type)(context,
            builder, dlm__idk.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, dlm__idk.
            offsets).data
        oftfw__uoy = builder.gep(nepkz__zzya, [fzpl__kkc], inbounds=True)
        ghqx__qjds = builder.load(oftfw__uoy)
        ixdqr__pgeix = lir.ArrayType(lir.IntType(8), 8)
        xkhw__xkgz = cgutils.alloca_once_value(builder, lir.Constant(
            ixdqr__pgeix, (1, 2, 4, 8, 16, 32, 64, 128)))
        kks__nqvie = builder.load(builder.gep(xkhw__xkgz, [lir.Constant(lir
            .IntType(64), 0), abe__xbu], inbounds=True))
        kks__nqvie = builder.xor(kks__nqvie, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(ghqx__qjds, kks__nqvie), oftfw__uoy)
        if str_arr_typ == string_array_type:
            cgehz__zza = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            qddlp__zhwge = builder.icmp_unsigned('!=', cgehz__zza, dlm__idk
                .n_arrays)
            with builder.if_then(qddlp__zhwge):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [cgehz__zza]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        fzpl__kkc = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        abe__xbu = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        nepkz__zzya = context.make_array(null_bitmap_arr_type)(context,
            builder, dlm__idk.null_bitmap).data
        oftfw__uoy = builder.gep(nepkz__zzya, [fzpl__kkc], inbounds=True)
        ghqx__qjds = builder.load(oftfw__uoy)
        ixdqr__pgeix = lir.ArrayType(lir.IntType(8), 8)
        xkhw__xkgz = cgutils.alloca_once_value(builder, lir.Constant(
            ixdqr__pgeix, (1, 2, 4, 8, 16, 32, 64, 128)))
        kks__nqvie = builder.load(builder.gep(xkhw__xkgz, [lir.Constant(lir
            .IntType(64), 0), abe__xbu], inbounds=True))
        builder.store(builder.or_(ghqx__qjds, kks__nqvie), oftfw__uoy)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        pjbiz__tjm = builder.udiv(builder.add(dlm__idk.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        nepkz__zzya = context.make_array(null_bitmap_arr_type)(context,
            builder, dlm__idk.null_bitmap).data
        cgutils.memset(builder, nepkz__zzya, pjbiz__tjm, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    zogo__vmo = context.make_helper(builder, string_array_type, str_arr)
    kdjv__ovwb = ArrayItemArrayType(char_arr_type)
    yres__vypfd = context.make_helper(builder, kdjv__ovwb, zogo__vmo.data)
    xxhh__ntzbx = ArrayItemArrayPayloadType(kdjv__ovwb)
    hmwib__hin = context.nrt.meminfo_data(builder, yres__vypfd.meminfo)
    mba__mgf = builder.bitcast(hmwib__hin, context.get_value_type(
        xxhh__ntzbx).as_pointer())
    return mba__mgf


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        onvd__mtgk, uud__hqmvw = args
        qvp__jtdq = _get_str_binary_arr_data_payload_ptr(context, builder,
            uud__hqmvw)
        ond__zam = _get_str_binary_arr_data_payload_ptr(context, builder,
            onvd__mtgk)
        efyi__vjp = _get_str_binary_arr_payload(context, builder,
            uud__hqmvw, sig.args[1])
        nodmu__ixjqh = _get_str_binary_arr_payload(context, builder,
            onvd__mtgk, sig.args[0])
        context.nrt.incref(builder, char_arr_type, efyi__vjp.data)
        context.nrt.incref(builder, offset_arr_type, efyi__vjp.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, efyi__vjp.null_bitmap
            )
        context.nrt.decref(builder, char_arr_type, nodmu__ixjqh.data)
        context.nrt.decref(builder, offset_arr_type, nodmu__ixjqh.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, nodmu__ixjqh.
            null_bitmap)
        builder.store(builder.load(qvp__jtdq), ond__zam)
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
        nor__sccts = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return nor__sccts
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, doni__wur, mbtm__yusk = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, dlm__idk.
            offsets).data
        data = context.make_helper(builder, char_arr_type, dlm__idk.data).data
        nnfz__jcwey = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        qznqr__zcc = cgutils.get_or_insert_function(builder.module,
            nnfz__jcwey, name='setitem_string_array')
        snrsv__edgbi = context.get_constant(types.int32, -1)
        gshr__gydf = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, dlm__idk.
            n_arrays)
        builder.call(qznqr__zcc, [offsets, data, num_total_chars, builder.
            extract_value(doni__wur, 0), mbtm__yusk, snrsv__edgbi,
            gshr__gydf, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    nnfz__jcwey = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    wctrj__xgurc = cgutils.get_or_insert_function(builder.module,
        nnfz__jcwey, name='is_na')
    return builder.call(wctrj__xgurc, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        nkt__dppo, ybm__tkm, clkhk__ukhky, lgnva__oiqsn = args
        cgutils.raw_memcpy(builder, nkt__dppo, ybm__tkm, clkhk__ukhky,
            lgnva__oiqsn)
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
        vlrtm__mcga, ovng__ocauv = unicode_to_utf8_and_len(val)
        yxk__wov = getitem_str_offset(A, ind)
        fezgz__spmn = getitem_str_offset(A, ind + 1)
        dfg__jpb = fezgz__spmn - yxk__wov
        if dfg__jpb != ovng__ocauv:
            return False
        doni__wur = get_data_ptr_ind(A, yxk__wov)
        return memcmp(doni__wur, vlrtm__mcga, ovng__ocauv) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        yxk__wov = getitem_str_offset(A, ind)
        dfg__jpb = bodo.libs.str_ext.int_to_str_len(val)
        wpc__tzpj = yxk__wov + dfg__jpb
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data, yxk__wov,
            wpc__tzpj)
        doni__wur = get_data_ptr_ind(A, yxk__wov)
        inplace_int64_to_str(doni__wur, dfg__jpb, val)
        setitem_str_offset(A, ind + 1, yxk__wov + dfg__jpb)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        doni__wur, = args
        cko__heqih = context.insert_const_string(builder.module, '<NA>')
        nsxuu__ctt = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, doni__wur, cko__heqih, nsxuu__ctt, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    bdvwr__gaiho = len('<NA>')

    def impl(A, ind):
        yxk__wov = getitem_str_offset(A, ind)
        wpc__tzpj = yxk__wov + bdvwr__gaiho
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data, yxk__wov,
            wpc__tzpj)
        doni__wur = get_data_ptr_ind(A, yxk__wov)
        inplace_set_NA_str(doni__wur)
        setitem_str_offset(A, ind + 1, yxk__wov + bdvwr__gaiho)
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
            yxk__wov = getitem_str_offset(A, ind)
            fezgz__spmn = getitem_str_offset(A, ind + 1)
            mbtm__yusk = fezgz__spmn - yxk__wov
            doni__wur = get_data_ptr_ind(A, yxk__wov)
            fooyb__vfdj = decode_utf8(doni__wur, mbtm__yusk)
            return fooyb__vfdj
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            nor__sccts = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(nor__sccts):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            tvipd__wea = get_data_ptr(out_arr).data
            pwms__bhbt = get_data_ptr(A).data
            hcqt__uafiq = 0
            uuao__zvxdi = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(nor__sccts):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    tvsg__yxxg = get_str_arr_item_length(A, i)
                    if tvsg__yxxg == 1:
                        copy_single_char(tvipd__wea, uuao__zvxdi,
                            pwms__bhbt, getitem_str_offset(A, i))
                    else:
                        memcpy_region(tvipd__wea, uuao__zvxdi, pwms__bhbt,
                            getitem_str_offset(A, i), tvsg__yxxg, 1)
                    uuao__zvxdi += tvsg__yxxg
                    setitem_str_offset(out_arr, hcqt__uafiq + 1, uuao__zvxdi)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, hcqt__uafiq)
                    else:
                        str_arr_set_not_na(out_arr, hcqt__uafiq)
                    hcqt__uafiq += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            nor__sccts = len(ind)
            out_arr = pre_alloc_string_array(nor__sccts, -1)
            hcqt__uafiq = 0
            for i in range(nor__sccts):
                izq__canm = A[ind[i]]
                out_arr[hcqt__uafiq] = izq__canm
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, hcqt__uafiq)
                hcqt__uafiq += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            nor__sccts = len(A)
            pzmg__txsd = numba.cpython.unicode._normalize_slice(ind, nor__sccts
                )
            coe__zsh = numba.cpython.unicode._slice_span(pzmg__txsd)
            if pzmg__txsd.step == 1:
                yxk__wov = getitem_str_offset(A, pzmg__txsd.start)
                fezgz__spmn = getitem_str_offset(A, pzmg__txsd.stop)
                n_chars = fezgz__spmn - yxk__wov
                hpe__jmex = pre_alloc_string_array(coe__zsh, np.int64(n_chars))
                for i in range(coe__zsh):
                    hpe__jmex[i] = A[pzmg__txsd.start + i]
                    if str_arr_is_na(A, pzmg__txsd.start + i):
                        str_arr_set_na(hpe__jmex, i)
                return hpe__jmex
            else:
                hpe__jmex = pre_alloc_string_array(coe__zsh, -1)
                for i in range(coe__zsh):
                    hpe__jmex[i] = A[pzmg__txsd.start + i * pzmg__txsd.step]
                    if str_arr_is_na(A, pzmg__txsd.start + i * pzmg__txsd.step
                        ):
                        str_arr_set_na(hpe__jmex, i)
                return hpe__jmex
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
    kwkza__mvehj = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(kwkza__mvehj)
        vmmiz__bbw = 4

        def impl_scalar(A, idx, val):
            quw__zuwr = (val._length if val._is_ascii else vmmiz__bbw * val
                ._length)
            rrax__qkmgv = A._data
            yxk__wov = np.int64(getitem_str_offset(A, idx))
            wpc__tzpj = yxk__wov + quw__zuwr
            bodo.libs.array_item_arr_ext.ensure_data_capacity(rrax__qkmgv,
                yxk__wov, wpc__tzpj)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                wpc__tzpj, val._data, val._length, val._kind, val._is_ascii,
                idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                pzmg__txsd = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                pkdw__uebtb = pzmg__txsd.start
                rrax__qkmgv = A._data
                yxk__wov = np.int64(getitem_str_offset(A, pkdw__uebtb))
                wpc__tzpj = yxk__wov + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(rrax__qkmgv,
                    yxk__wov, wpc__tzpj)
                set_string_array_range(A, val, pkdw__uebtb, yxk__wov)
                hjfs__surnf = 0
                for i in range(pzmg__txsd.start, pzmg__txsd.stop,
                    pzmg__txsd.step):
                    if str_arr_is_na(val, hjfs__surnf):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    hjfs__surnf += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                eopvg__lutk = str_list_to_array(val)
                A[idx] = eopvg__lutk
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                pzmg__txsd = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                for i in range(pzmg__txsd.start, pzmg__txsd.stop,
                    pzmg__txsd.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(kwkza__mvehj)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                nor__sccts = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(nor__sccts, -1)
                for i in numba.parfors.parfor.internal_prange(nor__sccts):
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
                nor__sccts = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(nor__sccts, -1)
                zybfi__lnj = 0
                for i in numba.parfors.parfor.internal_prange(nor__sccts):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, zybfi__lnj):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, zybfi__lnj)
                        else:
                            out_arr[i] = str(val[zybfi__lnj])
                        zybfi__lnj += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(kwkza__mvehj)
    raise BodoError(kwkza__mvehj)


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
    cayb__pbydi = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(cayb__pbydi, (types.Float, types.Integer)
        ) and cayb__pbydi not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(cayb__pbydi, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            nor__sccts = len(A)
            B = np.empty(nor__sccts, cayb__pbydi)
            for i in numba.parfors.parfor.internal_prange(nor__sccts):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif cayb__pbydi == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            nor__sccts = len(A)
            B = np.empty(nor__sccts, cayb__pbydi)
            for i in numba.parfors.parfor.internal_prange(nor__sccts):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif cayb__pbydi == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            nor__sccts = len(A)
            B = np.empty(nor__sccts, cayb__pbydi)
            for i in numba.parfors.parfor.internal_prange(nor__sccts):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            nor__sccts = len(A)
            B = np.empty(nor__sccts, cayb__pbydi)
            for i in numba.parfors.parfor.internal_prange(nor__sccts):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        doni__wur, mbtm__yusk = args
        mlqif__lyasd = context.get_python_api(builder)
        guou__fyvo = mlqif__lyasd.string_from_string_and_size(doni__wur,
            mbtm__yusk)
        wmlux__zpkl = mlqif__lyasd.to_native_value(string_type, guou__fyvo
            ).value
        bzy__pzeq = cgutils.create_struct_proxy(string_type)(context,
            builder, wmlux__zpkl)
        bzy__pzeq.hash = bzy__pzeq.hash.type(-1)
        mlqif__lyasd.decref(guou__fyvo)
        return bzy__pzeq._getvalue()
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
        czcf__grcbo, arr, ind, ufha__nmnw = args
        dlm__idk = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, dlm__idk.
            offsets).data
        data = context.make_helper(builder, char_arr_type, dlm__idk.data).data
        nnfz__jcwey = lir.FunctionType(lir.IntType(32), [czcf__grcbo.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        ifix__scude = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            ifix__scude = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        pszqn__vuf = cgutils.get_or_insert_function(builder.module,
            nnfz__jcwey, ifix__scude)
        return builder.call(pszqn__vuf, [czcf__grcbo, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    cztws__xhzig = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    nnfz__jcwey = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    vnsh__kpsa = cgutils.get_or_insert_function(c.builder.module,
        nnfz__jcwey, name='string_array_from_sequence')
    rsllx__dcdzv = c.builder.call(vnsh__kpsa, [val, cztws__xhzig])
    kdjv__ovwb = ArrayItemArrayType(char_arr_type)
    yres__vypfd = c.context.make_helper(c.builder, kdjv__ovwb)
    yres__vypfd.meminfo = rsllx__dcdzv
    zogo__vmo = c.context.make_helper(c.builder, typ)
    rrax__qkmgv = yres__vypfd._getvalue()
    zogo__vmo.data = rrax__qkmgv
    gpkwx__rbg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zogo__vmo._getvalue(), is_error=gpkwx__rbg)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    nor__sccts = len(pyval)
    uuao__zvxdi = 0
    tczkr__swyzr = np.empty(nor__sccts + 1, np_offset_type)
    yhkp__dpy = []
    gkxn__gjtbr = np.empty(nor__sccts + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        tczkr__swyzr[i] = uuao__zvxdi
        yktu__kun = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(gkxn__gjtbr, i, int(not yktu__kun)
            )
        if yktu__kun:
            continue
        asjgo__jvwix = list(s.encode()) if isinstance(s, str) else list(s)
        yhkp__dpy.extend(asjgo__jvwix)
        uuao__zvxdi += len(asjgo__jvwix)
    tczkr__swyzr[nor__sccts] = uuao__zvxdi
    vlc__kgpm = np.array(yhkp__dpy, np.uint8)
    aakhw__onu = context.get_constant(types.int64, nor__sccts)
    sub__hxd = context.get_constant_generic(builder, char_arr_type, vlc__kgpm)
    zazou__yxfil = context.get_constant_generic(builder, offset_arr_type,
        tczkr__swyzr)
    rbmi__cdla = context.get_constant_generic(builder, null_bitmap_arr_type,
        gkxn__gjtbr)
    dlm__idk = lir.Constant.literal_struct([aakhw__onu, sub__hxd,
        zazou__yxfil, rbmi__cdla])
    dlm__idk = cgutils.global_constant(builder, '.const.payload', dlm__idk
        ).bitcast(cgutils.voidptr_t)
    fvsk__xcs = context.get_constant(types.int64, -1)
    ctdkb__mzz = context.get_constant_null(types.voidptr)
    jdz__tffp = lir.Constant.literal_struct([fvsk__xcs, ctdkb__mzz,
        ctdkb__mzz, dlm__idk, fvsk__xcs])
    jdz__tffp = cgutils.global_constant(builder, '.const.meminfo', jdz__tffp
        ).bitcast(cgutils.voidptr_t)
    rrax__qkmgv = lir.Constant.literal_struct([jdz__tffp])
    zogo__vmo = lir.Constant.literal_struct([rrax__qkmgv])
    return zogo__vmo


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
