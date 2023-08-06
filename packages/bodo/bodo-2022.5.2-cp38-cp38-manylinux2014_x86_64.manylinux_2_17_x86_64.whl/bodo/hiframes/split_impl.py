import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rftd__dap = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, rftd__dap)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    xcpgi__tesac = context.get_value_type(str_arr_split_view_payload_type)
    rwng__ejb = context.get_abi_sizeof(xcpgi__tesac)
    fdfo__sako = context.get_value_type(types.voidptr)
    jtb__arghf = context.get_value_type(types.uintp)
    soz__xhjkx = lir.FunctionType(lir.VoidType(), [fdfo__sako, jtb__arghf,
        fdfo__sako])
    ejm__myzlq = cgutils.get_or_insert_function(builder.module, soz__xhjkx,
        name='dtor_str_arr_split_view')
    wtrmg__vwqjs = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rwng__ejb), ejm__myzlq)
    ygxg__nidhs = context.nrt.meminfo_data(builder, wtrmg__vwqjs)
    zyax__pes = builder.bitcast(ygxg__nidhs, xcpgi__tesac.as_pointer())
    return wtrmg__vwqjs, zyax__pes


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        ljxh__tsnv, bod__eov = args
        wtrmg__vwqjs, zyax__pes = construct_str_arr_split_view(context, builder
            )
        grlc__veplz = _get_str_binary_arr_payload(context, builder,
            ljxh__tsnv, string_array_type)
        rrn__ywugk = lir.FunctionType(lir.VoidType(), [zyax__pes.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        twsgg__qec = cgutils.get_or_insert_function(builder.module,
            rrn__ywugk, name='str_arr_split_view_impl')
        marg__alvu = context.make_helper(builder, offset_arr_type,
            grlc__veplz.offsets).data
        atk__fyu = context.make_helper(builder, char_arr_type, grlc__veplz.data
            ).data
        flq__wop = context.make_helper(builder, null_bitmap_arr_type,
            grlc__veplz.null_bitmap).data
        kgqai__mad = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(twsgg__qec, [zyax__pes, grlc__veplz.n_arrays,
            marg__alvu, atk__fyu, flq__wop, kgqai__mad])
        kznj__gayz = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(zyax__pes))
        kyhe__sdjt = context.make_helper(builder, string_array_split_view_type)
        kyhe__sdjt.num_items = grlc__veplz.n_arrays
        kyhe__sdjt.index_offsets = kznj__gayz.index_offsets
        kyhe__sdjt.data_offsets = kznj__gayz.data_offsets
        kyhe__sdjt.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [ljxh__tsnv])
        kyhe__sdjt.null_bitmap = kznj__gayz.null_bitmap
        kyhe__sdjt.meminfo = wtrmg__vwqjs
        foqb__tid = kyhe__sdjt._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, foqb__tid)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    cvroj__corb = context.make_helper(builder, string_array_split_view_type,
        val)
    zxqdr__ibds = context.insert_const_string(builder.module, 'numpy')
    dsdva__iqid = c.pyapi.import_module_noblock(zxqdr__ibds)
    dtype = c.pyapi.object_getattr_string(dsdva__iqid, 'object_')
    lup__kbygp = builder.sext(cvroj__corb.num_items, c.pyapi.longlong)
    lms__rngvg = c.pyapi.long_from_longlong(lup__kbygp)
    utb__jidc = c.pyapi.call_method(dsdva__iqid, 'ndarray', (lms__rngvg, dtype)
        )
    jpp__nat = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.pyobj,
        c.pyapi.py_ssize_t])
    ldrsn__hhao = c.pyapi._get_function(jpp__nat, name='array_getptr1')
    eprx__gwdt = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    turd__wbdnp = c.pyapi._get_function(eprx__gwdt, name='array_setitem')
    sdc__cfpg = c.pyapi.object_getattr_string(dsdva__iqid, 'nan')
    with cgutils.for_range(builder, cvroj__corb.num_items) as zpt__njbz:
        str_ind = zpt__njbz.index
        xsvj__kql = builder.sext(builder.load(builder.gep(cvroj__corb.
            index_offsets, [str_ind])), lir.IntType(64))
        yqhw__zpmom = builder.sext(builder.load(builder.gep(cvroj__corb.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        zis__lpuyy = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        qhas__ykif = builder.gep(cvroj__corb.null_bitmap, [zis__lpuyy])
        wmof__pwwxq = builder.load(qhas__ykif)
        ihkt__pwb = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(wmof__pwwxq, ihkt__pwb), lir.
            Constant(lir.IntType(8), 1))
        yuzv__uru = builder.sub(yqhw__zpmom, xsvj__kql)
        yuzv__uru = builder.sub(yuzv__uru, yuzv__uru.type(1))
        khbv__vhy = builder.call(ldrsn__hhao, [utb__jidc, str_ind])
        smcr__uqbq = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(smcr__uqbq) as (uxqq__pyu, twro__tkax):
            with uxqq__pyu:
                bfwya__ugf = c.pyapi.list_new(yuzv__uru)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    bfwya__ugf), likely=True):
                    with cgutils.for_range(c.builder, yuzv__uru) as zpt__njbz:
                        khb__hsb = builder.add(xsvj__kql, zpt__njbz.index)
                        data_start = builder.load(builder.gep(cvroj__corb.
                            data_offsets, [khb__hsb]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        wufmt__nvwyv = builder.load(builder.gep(cvroj__corb
                            .data_offsets, [builder.add(khb__hsb, khb__hsb.
                            type(1))]))
                        uvooz__ngm = builder.gep(builder.extract_value(
                            cvroj__corb.data, 0), [data_start])
                        znzdc__mllqk = builder.sext(builder.sub(
                            wufmt__nvwyv, data_start), lir.IntType(64))
                        ldx__tjlum = c.pyapi.string_from_string_and_size(
                            uvooz__ngm, znzdc__mllqk)
                        c.pyapi.list_setitem(bfwya__ugf, zpt__njbz.index,
                            ldx__tjlum)
                builder.call(turd__wbdnp, [utb__jidc, khbv__vhy, bfwya__ugf])
            with twro__tkax:
                builder.call(turd__wbdnp, [utb__jidc, khbv__vhy, sdc__cfpg])
    c.pyapi.decref(dsdva__iqid)
    c.pyapi.decref(dtype)
    c.pyapi.decref(sdc__cfpg)
    return utb__jidc


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        hqm__wuz, oid__vkao, uvooz__ngm = args
        wtrmg__vwqjs, zyax__pes = construct_str_arr_split_view(context, builder
            )
        rrn__ywugk = lir.FunctionType(lir.VoidType(), [zyax__pes.type, lir.
            IntType(64), lir.IntType(64)])
        twsgg__qec = cgutils.get_or_insert_function(builder.module,
            rrn__ywugk, name='str_arr_split_view_alloc')
        builder.call(twsgg__qec, [zyax__pes, hqm__wuz, oid__vkao])
        kznj__gayz = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(zyax__pes))
        kyhe__sdjt = context.make_helper(builder, string_array_split_view_type)
        kyhe__sdjt.num_items = hqm__wuz
        kyhe__sdjt.index_offsets = kznj__gayz.index_offsets
        kyhe__sdjt.data_offsets = kznj__gayz.data_offsets
        kyhe__sdjt.data = uvooz__ngm
        kyhe__sdjt.null_bitmap = kznj__gayz.null_bitmap
        context.nrt.incref(builder, data_t, uvooz__ngm)
        kyhe__sdjt.meminfo = wtrmg__vwqjs
        foqb__tid = kyhe__sdjt._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, foqb__tid)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        eziza__tsz, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            eziza__tsz = builder.extract_value(eziza__tsz, 0)
        return builder.bitcast(builder.gep(eziza__tsz, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        eziza__tsz, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            eziza__tsz = builder.extract_value(eziza__tsz, 0)
        return builder.load(builder.gep(eziza__tsz, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        eziza__tsz, ind, ljwef__uug = args
        vhmri__bxwzk = builder.gep(eziza__tsz, [ind])
        builder.store(ljwef__uug, vhmri__bxwzk)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        smpje__whw, ind = args
        jxvew__rvt = context.make_helper(builder, arr_ctypes_t, smpje__whw)
        qbjh__dml = context.make_helper(builder, arr_ctypes_t)
        qbjh__dml.data = builder.gep(jxvew__rvt.data, [ind])
        qbjh__dml.meminfo = jxvew__rvt.meminfo
        xcxfv__gmz = qbjh__dml._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, xcxfv__gmz)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    orv__xlhmw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not orv__xlhmw:
        return 0, 0, 0
    khb__hsb = getitem_c_arr(arr._index_offsets, item_ind)
    fgby__fhh = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    dehpt__pilwf = fgby__fhh - khb__hsb
    if str_ind >= dehpt__pilwf:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, khb__hsb + str_ind)
    data_start += 1
    if khb__hsb + str_ind == 0:
        data_start = 0
    wufmt__nvwyv = getitem_c_arr(arr._data_offsets, khb__hsb + str_ind + 1)
    lzv__zjnzs = wufmt__nvwyv - data_start
    return 1, data_start, lzv__zjnzs


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        pnw__qpkzo = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            khb__hsb = getitem_c_arr(A._index_offsets, ind)
            fgby__fhh = getitem_c_arr(A._index_offsets, ind + 1)
            eyu__mthl = fgby__fhh - khb__hsb - 1
            ljxh__tsnv = bodo.libs.str_arr_ext.pre_alloc_string_array(eyu__mthl
                , -1)
            for rtt__jadz in range(eyu__mthl):
                data_start = getitem_c_arr(A._data_offsets, khb__hsb +
                    rtt__jadz)
                data_start += 1
                if khb__hsb + rtt__jadz == 0:
                    data_start = 0
                wufmt__nvwyv = getitem_c_arr(A._data_offsets, khb__hsb +
                    rtt__jadz + 1)
                lzv__zjnzs = wufmt__nvwyv - data_start
                vhmri__bxwzk = get_array_ctypes_ptr(A._data, data_start)
                zsz__vpt = bodo.libs.str_arr_ext.decode_utf8(vhmri__bxwzk,
                    lzv__zjnzs)
                ljxh__tsnv[rtt__jadz] = zsz__vpt
            return ljxh__tsnv
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        tdylq__zvinf = offset_type.bitwidth // 8

        def _impl(A, ind):
            eyu__mthl = len(A)
            if eyu__mthl != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            hqm__wuz = 0
            oid__vkao = 0
            for rtt__jadz in range(eyu__mthl):
                if ind[rtt__jadz]:
                    hqm__wuz += 1
                    khb__hsb = getitem_c_arr(A._index_offsets, rtt__jadz)
                    fgby__fhh = getitem_c_arr(A._index_offsets, rtt__jadz + 1)
                    oid__vkao += fgby__fhh - khb__hsb
            utb__jidc = pre_alloc_str_arr_view(hqm__wuz, oid__vkao, A._data)
            item_ind = 0
            kgegk__dtl = 0
            for rtt__jadz in range(eyu__mthl):
                if ind[rtt__jadz]:
                    khb__hsb = getitem_c_arr(A._index_offsets, rtt__jadz)
                    fgby__fhh = getitem_c_arr(A._index_offsets, rtt__jadz + 1)
                    otc__txqom = fgby__fhh - khb__hsb
                    setitem_c_arr(utb__jidc._index_offsets, item_ind,
                        kgegk__dtl)
                    vhmri__bxwzk = get_c_arr_ptr(A._data_offsets, khb__hsb)
                    zln__cks = get_c_arr_ptr(utb__jidc._data_offsets,
                        kgegk__dtl)
                    _memcpy(zln__cks, vhmri__bxwzk, otc__txqom, tdylq__zvinf)
                    orv__xlhmw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, rtt__jadz)
                    bodo.libs.int_arr_ext.set_bit_to_arr(utb__jidc.
                        _null_bitmap, item_ind, orv__xlhmw)
                    item_ind += 1
                    kgegk__dtl += otc__txqom
            setitem_c_arr(utb__jidc._index_offsets, item_ind, kgegk__dtl)
            return utb__jidc
        return _impl
