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
        qlak__zynsj = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, qlak__zynsj)


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
    xchh__jzawe = context.get_value_type(str_arr_split_view_payload_type)
    wcev__krqbg = context.get_abi_sizeof(xchh__jzawe)
    jwz__qwfyq = context.get_value_type(types.voidptr)
    eytwh__cxa = context.get_value_type(types.uintp)
    pxjj__ahah = lir.FunctionType(lir.VoidType(), [jwz__qwfyq, eytwh__cxa,
        jwz__qwfyq])
    ppq__faec = cgutils.get_or_insert_function(builder.module, pxjj__ahah,
        name='dtor_str_arr_split_view')
    ywuz__zhg = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, wcev__krqbg), ppq__faec)
    szpw__ntkl = context.nrt.meminfo_data(builder, ywuz__zhg)
    fbo__gwmw = builder.bitcast(szpw__ntkl, xchh__jzawe.as_pointer())
    return ywuz__zhg, fbo__gwmw


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        tirn__gczp, ijiqy__tajv = args
        ywuz__zhg, fbo__gwmw = construct_str_arr_split_view(context, builder)
        uhuc__trcpq = _get_str_binary_arr_payload(context, builder,
            tirn__gczp, string_array_type)
        ahmg__uicv = lir.FunctionType(lir.VoidType(), [fbo__gwmw.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        vkhou__anul = cgutils.get_or_insert_function(builder.module,
            ahmg__uicv, name='str_arr_split_view_impl')
        hhi__eulf = context.make_helper(builder, offset_arr_type,
            uhuc__trcpq.offsets).data
        tpxq__cjuch = context.make_helper(builder, char_arr_type,
            uhuc__trcpq.data).data
        olyb__ldgi = context.make_helper(builder, null_bitmap_arr_type,
            uhuc__trcpq.null_bitmap).data
        aiywt__xzt = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(vkhou__anul, [fbo__gwmw, uhuc__trcpq.n_arrays,
            hhi__eulf, tpxq__cjuch, olyb__ldgi, aiywt__xzt])
        zndoo__vosix = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(fbo__gwmw))
        ujv__nfwzs = context.make_helper(builder, string_array_split_view_type)
        ujv__nfwzs.num_items = uhuc__trcpq.n_arrays
        ujv__nfwzs.index_offsets = zndoo__vosix.index_offsets
        ujv__nfwzs.data_offsets = zndoo__vosix.data_offsets
        ujv__nfwzs.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [tirn__gczp])
        ujv__nfwzs.null_bitmap = zndoo__vosix.null_bitmap
        ujv__nfwzs.meminfo = ywuz__zhg
        zlk__ysf = ujv__nfwzs._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, zlk__ysf)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    msqmw__szv = context.make_helper(builder, string_array_split_view_type, val
        )
    blou__qah = context.insert_const_string(builder.module, 'numpy')
    lcht__bucm = c.pyapi.import_module_noblock(blou__qah)
    dtype = c.pyapi.object_getattr_string(lcht__bucm, 'object_')
    byduc__rvj = builder.sext(msqmw__szv.num_items, c.pyapi.longlong)
    umzer__ljjyf = c.pyapi.long_from_longlong(byduc__rvj)
    spqja__lke = c.pyapi.call_method(lcht__bucm, 'ndarray', (umzer__ljjyf,
        dtype))
    ent__bftao = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    xxddh__ixhe = c.pyapi._get_function(ent__bftao, name='array_getptr1')
    mthr__weq = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    biq__sbfbk = c.pyapi._get_function(mthr__weq, name='array_setitem')
    bma__cfa = c.pyapi.object_getattr_string(lcht__bucm, 'nan')
    with cgutils.for_range(builder, msqmw__szv.num_items) as bwr__uhob:
        str_ind = bwr__uhob.index
        lwkz__ozx = builder.sext(builder.load(builder.gep(msqmw__szv.
            index_offsets, [str_ind])), lir.IntType(64))
        onptl__mlbt = builder.sext(builder.load(builder.gep(msqmw__szv.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        mkquy__bsh = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        bpkcj__fao = builder.gep(msqmw__szv.null_bitmap, [mkquy__bsh])
        rxs__btbj = builder.load(bpkcj__fao)
        alsql__vwzp = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(rxs__btbj, alsql__vwzp), lir.
            Constant(lir.IntType(8), 1))
        zftbu__pjyq = builder.sub(onptl__mlbt, lwkz__ozx)
        zftbu__pjyq = builder.sub(zftbu__pjyq, zftbu__pjyq.type(1))
        ozjtr__efk = builder.call(xxddh__ixhe, [spqja__lke, str_ind])
        cxfe__mbo = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(cxfe__mbo) as (krf__lstld, olja__nbeyx):
            with krf__lstld:
                trpfn__ztp = c.pyapi.list_new(zftbu__pjyq)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    trpfn__ztp), likely=True):
                    with cgutils.for_range(c.builder, zftbu__pjyq
                        ) as bwr__uhob:
                        wpkr__jqkg = builder.add(lwkz__ozx, bwr__uhob.index)
                        data_start = builder.load(builder.gep(msqmw__szv.
                            data_offsets, [wpkr__jqkg]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        jag__lep = builder.load(builder.gep(msqmw__szv.
                            data_offsets, [builder.add(wpkr__jqkg,
                            wpkr__jqkg.type(1))]))
                        lnaq__cby = builder.gep(builder.extract_value(
                            msqmw__szv.data, 0), [data_start])
                        oam__ybt = builder.sext(builder.sub(jag__lep,
                            data_start), lir.IntType(64))
                        ikm__drdg = c.pyapi.string_from_string_and_size(
                            lnaq__cby, oam__ybt)
                        c.pyapi.list_setitem(trpfn__ztp, bwr__uhob.index,
                            ikm__drdg)
                builder.call(biq__sbfbk, [spqja__lke, ozjtr__efk, trpfn__ztp])
            with olja__nbeyx:
                builder.call(biq__sbfbk, [spqja__lke, ozjtr__efk, bma__cfa])
    c.pyapi.decref(lcht__bucm)
    c.pyapi.decref(dtype)
    c.pyapi.decref(bma__cfa)
    return spqja__lke


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        ter__ssevo, zlrs__gkot, lnaq__cby = args
        ywuz__zhg, fbo__gwmw = construct_str_arr_split_view(context, builder)
        ahmg__uicv = lir.FunctionType(lir.VoidType(), [fbo__gwmw.type, lir.
            IntType(64), lir.IntType(64)])
        vkhou__anul = cgutils.get_or_insert_function(builder.module,
            ahmg__uicv, name='str_arr_split_view_alloc')
        builder.call(vkhou__anul, [fbo__gwmw, ter__ssevo, zlrs__gkot])
        zndoo__vosix = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(fbo__gwmw))
        ujv__nfwzs = context.make_helper(builder, string_array_split_view_type)
        ujv__nfwzs.num_items = ter__ssevo
        ujv__nfwzs.index_offsets = zndoo__vosix.index_offsets
        ujv__nfwzs.data_offsets = zndoo__vosix.data_offsets
        ujv__nfwzs.data = lnaq__cby
        ujv__nfwzs.null_bitmap = zndoo__vosix.null_bitmap
        context.nrt.incref(builder, data_t, lnaq__cby)
        ujv__nfwzs.meminfo = ywuz__zhg
        zlk__ysf = ujv__nfwzs._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, zlk__ysf)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        bhgwk__uowh, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            bhgwk__uowh = builder.extract_value(bhgwk__uowh, 0)
        return builder.bitcast(builder.gep(bhgwk__uowh, [ind]), lir.IntType
            (8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        bhgwk__uowh, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            bhgwk__uowh = builder.extract_value(bhgwk__uowh, 0)
        return builder.load(builder.gep(bhgwk__uowh, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        bhgwk__uowh, ind, fqz__bgojc = args
        cvq__fhopd = builder.gep(bhgwk__uowh, [ind])
        builder.store(fqz__bgojc, cvq__fhopd)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        skdjp__plcqe, ind = args
        sgex__ivkd = context.make_helper(builder, arr_ctypes_t, skdjp__plcqe)
        yulny__zijrl = context.make_helper(builder, arr_ctypes_t)
        yulny__zijrl.data = builder.gep(sgex__ivkd.data, [ind])
        yulny__zijrl.meminfo = sgex__ivkd.meminfo
        vduy__rdgd = yulny__zijrl._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, vduy__rdgd)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    imhk__nbsf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not imhk__nbsf:
        return 0, 0, 0
    wpkr__jqkg = getitem_c_arr(arr._index_offsets, item_ind)
    mry__nravk = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    lgeo__nbd = mry__nravk - wpkr__jqkg
    if str_ind >= lgeo__nbd:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, wpkr__jqkg + str_ind)
    data_start += 1
    if wpkr__jqkg + str_ind == 0:
        data_start = 0
    jag__lep = getitem_c_arr(arr._data_offsets, wpkr__jqkg + str_ind + 1)
    tez__nbzbe = jag__lep - data_start
    return 1, data_start, tez__nbzbe


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
        zhkzw__rgpl = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            wpkr__jqkg = getitem_c_arr(A._index_offsets, ind)
            mry__nravk = getitem_c_arr(A._index_offsets, ind + 1)
            nyjxc__dtyhs = mry__nravk - wpkr__jqkg - 1
            tirn__gczp = bodo.libs.str_arr_ext.pre_alloc_string_array(
                nyjxc__dtyhs, -1)
            for dhj__nkbvq in range(nyjxc__dtyhs):
                data_start = getitem_c_arr(A._data_offsets, wpkr__jqkg +
                    dhj__nkbvq)
                data_start += 1
                if wpkr__jqkg + dhj__nkbvq == 0:
                    data_start = 0
                jag__lep = getitem_c_arr(A._data_offsets, wpkr__jqkg +
                    dhj__nkbvq + 1)
                tez__nbzbe = jag__lep - data_start
                cvq__fhopd = get_array_ctypes_ptr(A._data, data_start)
                jybe__gztv = bodo.libs.str_arr_ext.decode_utf8(cvq__fhopd,
                    tez__nbzbe)
                tirn__gczp[dhj__nkbvq] = jybe__gztv
            return tirn__gczp
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        ucn__jef = offset_type.bitwidth // 8

        def _impl(A, ind):
            nyjxc__dtyhs = len(A)
            if nyjxc__dtyhs != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            ter__ssevo = 0
            zlrs__gkot = 0
            for dhj__nkbvq in range(nyjxc__dtyhs):
                if ind[dhj__nkbvq]:
                    ter__ssevo += 1
                    wpkr__jqkg = getitem_c_arr(A._index_offsets, dhj__nkbvq)
                    mry__nravk = getitem_c_arr(A._index_offsets, dhj__nkbvq + 1
                        )
                    zlrs__gkot += mry__nravk - wpkr__jqkg
            spqja__lke = pre_alloc_str_arr_view(ter__ssevo, zlrs__gkot, A._data
                )
            item_ind = 0
            qlm__sevd = 0
            for dhj__nkbvq in range(nyjxc__dtyhs):
                if ind[dhj__nkbvq]:
                    wpkr__jqkg = getitem_c_arr(A._index_offsets, dhj__nkbvq)
                    mry__nravk = getitem_c_arr(A._index_offsets, dhj__nkbvq + 1
                        )
                    jkgmu__nec = mry__nravk - wpkr__jqkg
                    setitem_c_arr(spqja__lke._index_offsets, item_ind,
                        qlm__sevd)
                    cvq__fhopd = get_c_arr_ptr(A._data_offsets, wpkr__jqkg)
                    uvf__vsni = get_c_arr_ptr(spqja__lke._data_offsets,
                        qlm__sevd)
                    _memcpy(uvf__vsni, cvq__fhopd, jkgmu__nec, ucn__jef)
                    imhk__nbsf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, dhj__nkbvq)
                    bodo.libs.int_arr_ext.set_bit_to_arr(spqja__lke.
                        _null_bitmap, item_ind, imhk__nbsf)
                    item_ind += 1
                    qlm__sevd += jkgmu__nec
            setitem_c_arr(spqja__lke._index_offsets, item_ind, qlm__sevd)
            return spqja__lke
        return _impl
