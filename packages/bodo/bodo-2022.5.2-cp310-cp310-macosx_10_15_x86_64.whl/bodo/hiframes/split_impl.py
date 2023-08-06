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
        wzk__sajr = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, wzk__sajr)


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
    jsdo__qbx = context.get_value_type(str_arr_split_view_payload_type)
    dut__ghn = context.get_abi_sizeof(jsdo__qbx)
    aamii__pxul = context.get_value_type(types.voidptr)
    doi__nhxdy = context.get_value_type(types.uintp)
    bjkx__snz = lir.FunctionType(lir.VoidType(), [aamii__pxul, doi__nhxdy,
        aamii__pxul])
    jvspj__wmdkn = cgutils.get_or_insert_function(builder.module, bjkx__snz,
        name='dtor_str_arr_split_view')
    yzys__gsqev = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, dut__ghn), jvspj__wmdkn)
    tzzd__ehvt = context.nrt.meminfo_data(builder, yzys__gsqev)
    prmpz__zwrdd = builder.bitcast(tzzd__ehvt, jsdo__qbx.as_pointer())
    return yzys__gsqev, prmpz__zwrdd


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        vszmq__omft, rnusy__shj = args
        yzys__gsqev, prmpz__zwrdd = construct_str_arr_split_view(context,
            builder)
        hqfy__jinlz = _get_str_binary_arr_payload(context, builder,
            vszmq__omft, string_array_type)
        cggsg__fuct = lir.FunctionType(lir.VoidType(), [prmpz__zwrdd.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        pdpn__zme = cgutils.get_or_insert_function(builder.module,
            cggsg__fuct, name='str_arr_split_view_impl')
        khryh__tkzvj = context.make_helper(builder, offset_arr_type,
            hqfy__jinlz.offsets).data
        teogw__skq = context.make_helper(builder, char_arr_type,
            hqfy__jinlz.data).data
        ukyr__qtm = context.make_helper(builder, null_bitmap_arr_type,
            hqfy__jinlz.null_bitmap).data
        qebj__nsdsj = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(pdpn__zme, [prmpz__zwrdd, hqfy__jinlz.n_arrays,
            khryh__tkzvj, teogw__skq, ukyr__qtm, qebj__nsdsj])
        wvlaz__jbkc = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(prmpz__zwrdd))
        kjhw__cfiq = context.make_helper(builder, string_array_split_view_type)
        kjhw__cfiq.num_items = hqfy__jinlz.n_arrays
        kjhw__cfiq.index_offsets = wvlaz__jbkc.index_offsets
        kjhw__cfiq.data_offsets = wvlaz__jbkc.data_offsets
        kjhw__cfiq.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [vszmq__omft]
            )
        kjhw__cfiq.null_bitmap = wvlaz__jbkc.null_bitmap
        kjhw__cfiq.meminfo = yzys__gsqev
        ixavg__yuqqy = kjhw__cfiq._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, ixavg__yuqqy)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    ioc__tkpv = context.make_helper(builder, string_array_split_view_type, val)
    hfa__wok = context.insert_const_string(builder.module, 'numpy')
    tfpz__mnelk = c.pyapi.import_module_noblock(hfa__wok)
    dtype = c.pyapi.object_getattr_string(tfpz__mnelk, 'object_')
    qqt__inl = builder.sext(ioc__tkpv.num_items, c.pyapi.longlong)
    sst__juqub = c.pyapi.long_from_longlong(qqt__inl)
    notyg__sjpy = c.pyapi.call_method(tfpz__mnelk, 'ndarray', (sst__juqub,
        dtype))
    bhndv__btmz = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    twet__ysjcz = c.pyapi._get_function(bhndv__btmz, name='array_getptr1')
    lttz__snqge = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    nblr__kaela = c.pyapi._get_function(lttz__snqge, name='array_setitem')
    wee__okx = c.pyapi.object_getattr_string(tfpz__mnelk, 'nan')
    with cgutils.for_range(builder, ioc__tkpv.num_items) as vzhgh__cznel:
        str_ind = vzhgh__cznel.index
        bpkrt__uood = builder.sext(builder.load(builder.gep(ioc__tkpv.
            index_offsets, [str_ind])), lir.IntType(64))
        iqvdf__ovxum = builder.sext(builder.load(builder.gep(ioc__tkpv.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        qzoa__ggxol = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        atgj__gvrv = builder.gep(ioc__tkpv.null_bitmap, [qzoa__ggxol])
        cyj__ljl = builder.load(atgj__gvrv)
        hqk__ggcw = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(cyj__ljl, hqk__ggcw), lir.Constant(
            lir.IntType(8), 1))
        nix__miumw = builder.sub(iqvdf__ovxum, bpkrt__uood)
        nix__miumw = builder.sub(nix__miumw, nix__miumw.type(1))
        qrsi__xdmg = builder.call(twet__ysjcz, [notyg__sjpy, str_ind])
        hlv__wuptu = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(hlv__wuptu) as (pnhe__valao, rgj__xal):
            with pnhe__valao:
                eqwvz__inb = c.pyapi.list_new(nix__miumw)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    eqwvz__inb), likely=True):
                    with cgutils.for_range(c.builder, nix__miumw
                        ) as vzhgh__cznel:
                        uji__tsqei = builder.add(bpkrt__uood, vzhgh__cznel.
                            index)
                        data_start = builder.load(builder.gep(ioc__tkpv.
                            data_offsets, [uji__tsqei]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        gytqs__mmsrr = builder.load(builder.gep(ioc__tkpv.
                            data_offsets, [builder.add(uji__tsqei,
                            uji__tsqei.type(1))]))
                        stbio__rcbb = builder.gep(builder.extract_value(
                            ioc__tkpv.data, 0), [data_start])
                        ipc__yirzq = builder.sext(builder.sub(gytqs__mmsrr,
                            data_start), lir.IntType(64))
                        eegx__kofz = c.pyapi.string_from_string_and_size(
                            stbio__rcbb, ipc__yirzq)
                        c.pyapi.list_setitem(eqwvz__inb, vzhgh__cznel.index,
                            eegx__kofz)
                builder.call(nblr__kaela, [notyg__sjpy, qrsi__xdmg, eqwvz__inb]
                    )
            with rgj__xal:
                builder.call(nblr__kaela, [notyg__sjpy, qrsi__xdmg, wee__okx])
    c.pyapi.decref(tfpz__mnelk)
    c.pyapi.decref(dtype)
    c.pyapi.decref(wee__okx)
    return notyg__sjpy


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        plyw__rcsgi, zzjl__yumxx, stbio__rcbb = args
        yzys__gsqev, prmpz__zwrdd = construct_str_arr_split_view(context,
            builder)
        cggsg__fuct = lir.FunctionType(lir.VoidType(), [prmpz__zwrdd.type,
            lir.IntType(64), lir.IntType(64)])
        pdpn__zme = cgutils.get_or_insert_function(builder.module,
            cggsg__fuct, name='str_arr_split_view_alloc')
        builder.call(pdpn__zme, [prmpz__zwrdd, plyw__rcsgi, zzjl__yumxx])
        wvlaz__jbkc = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(prmpz__zwrdd))
        kjhw__cfiq = context.make_helper(builder, string_array_split_view_type)
        kjhw__cfiq.num_items = plyw__rcsgi
        kjhw__cfiq.index_offsets = wvlaz__jbkc.index_offsets
        kjhw__cfiq.data_offsets = wvlaz__jbkc.data_offsets
        kjhw__cfiq.data = stbio__rcbb
        kjhw__cfiq.null_bitmap = wvlaz__jbkc.null_bitmap
        context.nrt.incref(builder, data_t, stbio__rcbb)
        kjhw__cfiq.meminfo = yzys__gsqev
        ixavg__yuqqy = kjhw__cfiq._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, ixavg__yuqqy)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        krfi__gbaw, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            krfi__gbaw = builder.extract_value(krfi__gbaw, 0)
        return builder.bitcast(builder.gep(krfi__gbaw, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        krfi__gbaw, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            krfi__gbaw = builder.extract_value(krfi__gbaw, 0)
        return builder.load(builder.gep(krfi__gbaw, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        krfi__gbaw, ind, zmzx__mnwt = args
        eld__azqf = builder.gep(krfi__gbaw, [ind])
        builder.store(zmzx__mnwt, eld__azqf)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        lvrcn__aoff, ind = args
        dotn__lplzv = context.make_helper(builder, arr_ctypes_t, lvrcn__aoff)
        uxdlv__phcqc = context.make_helper(builder, arr_ctypes_t)
        uxdlv__phcqc.data = builder.gep(dotn__lplzv.data, [ind])
        uxdlv__phcqc.meminfo = dotn__lplzv.meminfo
        tgtw__qnw = uxdlv__phcqc._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, tgtw__qnw)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    ltmy__ensh = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not ltmy__ensh:
        return 0, 0, 0
    uji__tsqei = getitem_c_arr(arr._index_offsets, item_ind)
    ebn__azh = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    ymbeo__gvh = ebn__azh - uji__tsqei
    if str_ind >= ymbeo__gvh:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, uji__tsqei + str_ind)
    data_start += 1
    if uji__tsqei + str_ind == 0:
        data_start = 0
    gytqs__mmsrr = getitem_c_arr(arr._data_offsets, uji__tsqei + str_ind + 1)
    hmbpm__qhhg = gytqs__mmsrr - data_start
    return 1, data_start, hmbpm__qhhg


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
        azaa__bujov = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            uji__tsqei = getitem_c_arr(A._index_offsets, ind)
            ebn__azh = getitem_c_arr(A._index_offsets, ind + 1)
            blblu__afyql = ebn__azh - uji__tsqei - 1
            vszmq__omft = bodo.libs.str_arr_ext.pre_alloc_string_array(
                blblu__afyql, -1)
            for uri__apca in range(blblu__afyql):
                data_start = getitem_c_arr(A._data_offsets, uji__tsqei +
                    uri__apca)
                data_start += 1
                if uji__tsqei + uri__apca == 0:
                    data_start = 0
                gytqs__mmsrr = getitem_c_arr(A._data_offsets, uji__tsqei +
                    uri__apca + 1)
                hmbpm__qhhg = gytqs__mmsrr - data_start
                eld__azqf = get_array_ctypes_ptr(A._data, data_start)
                bhnfu__qwr = bodo.libs.str_arr_ext.decode_utf8(eld__azqf,
                    hmbpm__qhhg)
                vszmq__omft[uri__apca] = bhnfu__qwr
            return vszmq__omft
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        pni__eypho = offset_type.bitwidth // 8

        def _impl(A, ind):
            blblu__afyql = len(A)
            if blblu__afyql != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            plyw__rcsgi = 0
            zzjl__yumxx = 0
            for uri__apca in range(blblu__afyql):
                if ind[uri__apca]:
                    plyw__rcsgi += 1
                    uji__tsqei = getitem_c_arr(A._index_offsets, uri__apca)
                    ebn__azh = getitem_c_arr(A._index_offsets, uri__apca + 1)
                    zzjl__yumxx += ebn__azh - uji__tsqei
            notyg__sjpy = pre_alloc_str_arr_view(plyw__rcsgi, zzjl__yumxx,
                A._data)
            item_ind = 0
            jgo__cqh = 0
            for uri__apca in range(blblu__afyql):
                if ind[uri__apca]:
                    uji__tsqei = getitem_c_arr(A._index_offsets, uri__apca)
                    ebn__azh = getitem_c_arr(A._index_offsets, uri__apca + 1)
                    goyyz__ugzqk = ebn__azh - uji__tsqei
                    setitem_c_arr(notyg__sjpy._index_offsets, item_ind,
                        jgo__cqh)
                    eld__azqf = get_c_arr_ptr(A._data_offsets, uji__tsqei)
                    mpdr__rqlqo = get_c_arr_ptr(notyg__sjpy._data_offsets,
                        jgo__cqh)
                    _memcpy(mpdr__rqlqo, eld__azqf, goyyz__ugzqk, pni__eypho)
                    ltmy__ensh = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, uri__apca)
                    bodo.libs.int_arr_ext.set_bit_to_arr(notyg__sjpy.
                        _null_bitmap, item_ind, ltmy__ensh)
                    item_ind += 1
                    jgo__cqh += goyyz__ugzqk
            setitem_c_arr(notyg__sjpy._index_offsets, item_ind, jgo__cqh)
            return notyg__sjpy
        return _impl
