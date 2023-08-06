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
        wtg__nna = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, wtg__nna)


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
    pkeja__gjgy = context.get_value_type(str_arr_split_view_payload_type)
    eqbn__inmv = context.get_abi_sizeof(pkeja__gjgy)
    rryuf__htzt = context.get_value_type(types.voidptr)
    xdpkh__qapy = context.get_value_type(types.uintp)
    esqc__cgo = lir.FunctionType(lir.VoidType(), [rryuf__htzt, xdpkh__qapy,
        rryuf__htzt])
    dviv__syn = cgutils.get_or_insert_function(builder.module, esqc__cgo,
        name='dtor_str_arr_split_view')
    uau__psfg = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, eqbn__inmv), dviv__syn)
    wsabi__wbsvo = context.nrt.meminfo_data(builder, uau__psfg)
    futw__xwqyz = builder.bitcast(wsabi__wbsvo, pkeja__gjgy.as_pointer())
    return uau__psfg, futw__xwqyz


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        ykvl__yow, jufkt__owx = args
        uau__psfg, futw__xwqyz = construct_str_arr_split_view(context, builder)
        cbroo__axy = _get_str_binary_arr_payload(context, builder,
            ykvl__yow, string_array_type)
        auwe__alt = lir.FunctionType(lir.VoidType(), [futw__xwqyz.type, lir
            .IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        smx__holpy = cgutils.get_or_insert_function(builder.module,
            auwe__alt, name='str_arr_split_view_impl')
        byyyw__wdr = context.make_helper(builder, offset_arr_type,
            cbroo__axy.offsets).data
        esby__ffc = context.make_helper(builder, char_arr_type, cbroo__axy.data
            ).data
        whaub__nly = context.make_helper(builder, null_bitmap_arr_type,
            cbroo__axy.null_bitmap).data
        dpnx__qzkno = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(smx__holpy, [futw__xwqyz, cbroo__axy.n_arrays,
            byyyw__wdr, esby__ffc, whaub__nly, dpnx__qzkno])
        lyw__qdxcc = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(futw__xwqyz))
        zyy__jehvt = context.make_helper(builder, string_array_split_view_type)
        zyy__jehvt.num_items = cbroo__axy.n_arrays
        zyy__jehvt.index_offsets = lyw__qdxcc.index_offsets
        zyy__jehvt.data_offsets = lyw__qdxcc.data_offsets
        zyy__jehvt.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [ykvl__yow])
        zyy__jehvt.null_bitmap = lyw__qdxcc.null_bitmap
        zyy__jehvt.meminfo = uau__psfg
        gqk__obtjw = zyy__jehvt._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, gqk__obtjw)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    guy__yimjr = context.make_helper(builder, string_array_split_view_type, val
        )
    zfui__mriab = context.insert_const_string(builder.module, 'numpy')
    ttx__eol = c.pyapi.import_module_noblock(zfui__mriab)
    dtype = c.pyapi.object_getattr_string(ttx__eol, 'object_')
    wrcw__klhk = builder.sext(guy__yimjr.num_items, c.pyapi.longlong)
    diy__vtavh = c.pyapi.long_from_longlong(wrcw__klhk)
    wwklo__irrev = c.pyapi.call_method(ttx__eol, 'ndarray', (diy__vtavh, dtype)
        )
    ytku__bgcsc = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    ghi__rcayz = c.pyapi._get_function(ytku__bgcsc, name='array_getptr1')
    skvn__opv = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    narn__sls = c.pyapi._get_function(skvn__opv, name='array_setitem')
    zmnhq__rwomp = c.pyapi.object_getattr_string(ttx__eol, 'nan')
    with cgutils.for_range(builder, guy__yimjr.num_items) as sno__ezvy:
        str_ind = sno__ezvy.index
        dvg__rtvd = builder.sext(builder.load(builder.gep(guy__yimjr.
            index_offsets, [str_ind])), lir.IntType(64))
        ltl__ksyod = builder.sext(builder.load(builder.gep(guy__yimjr.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        teuiu__vyag = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        cdmk__trbbw = builder.gep(guy__yimjr.null_bitmap, [teuiu__vyag])
        qhb__ditda = builder.load(cdmk__trbbw)
        cnvfz__shonb = builder.trunc(builder.and_(str_ind, lir.Constant(lir
            .IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(qhb__ditda, cnvfz__shonb), lir.
            Constant(lir.IntType(8), 1))
        pmxzr__khyc = builder.sub(ltl__ksyod, dvg__rtvd)
        pmxzr__khyc = builder.sub(pmxzr__khyc, pmxzr__khyc.type(1))
        ieaci__baa = builder.call(ghi__rcayz, [wwklo__irrev, str_ind])
        isuyt__hujrj = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(isuyt__hujrj) as (kpifz__uerd, zapl__elbsa):
            with kpifz__uerd:
                vtdu__vtb = c.pyapi.list_new(pmxzr__khyc)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    vtdu__vtb), likely=True):
                    with cgutils.for_range(c.builder, pmxzr__khyc
                        ) as sno__ezvy:
                        sry__gejqe = builder.add(dvg__rtvd, sno__ezvy.index)
                        data_start = builder.load(builder.gep(guy__yimjr.
                            data_offsets, [sry__gejqe]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        dvyu__ekr = builder.load(builder.gep(guy__yimjr.
                            data_offsets, [builder.add(sry__gejqe,
                            sry__gejqe.type(1))]))
                        bms__zxe = builder.gep(builder.extract_value(
                            guy__yimjr.data, 0), [data_start])
                        ocx__jxy = builder.sext(builder.sub(dvyu__ekr,
                            data_start), lir.IntType(64))
                        jygn__irlgj = c.pyapi.string_from_string_and_size(
                            bms__zxe, ocx__jxy)
                        c.pyapi.list_setitem(vtdu__vtb, sno__ezvy.index,
                            jygn__irlgj)
                builder.call(narn__sls, [wwklo__irrev, ieaci__baa, vtdu__vtb])
            with zapl__elbsa:
                builder.call(narn__sls, [wwklo__irrev, ieaci__baa,
                    zmnhq__rwomp])
    c.pyapi.decref(ttx__eol)
    c.pyapi.decref(dtype)
    c.pyapi.decref(zmnhq__rwomp)
    return wwklo__irrev


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        jkl__lnxkx, jqdpz__nvi, bms__zxe = args
        uau__psfg, futw__xwqyz = construct_str_arr_split_view(context, builder)
        auwe__alt = lir.FunctionType(lir.VoidType(), [futw__xwqyz.type, lir
            .IntType(64), lir.IntType(64)])
        smx__holpy = cgutils.get_or_insert_function(builder.module,
            auwe__alt, name='str_arr_split_view_alloc')
        builder.call(smx__holpy, [futw__xwqyz, jkl__lnxkx, jqdpz__nvi])
        lyw__qdxcc = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(futw__xwqyz))
        zyy__jehvt = context.make_helper(builder, string_array_split_view_type)
        zyy__jehvt.num_items = jkl__lnxkx
        zyy__jehvt.index_offsets = lyw__qdxcc.index_offsets
        zyy__jehvt.data_offsets = lyw__qdxcc.data_offsets
        zyy__jehvt.data = bms__zxe
        zyy__jehvt.null_bitmap = lyw__qdxcc.null_bitmap
        context.nrt.incref(builder, data_t, bms__zxe)
        zyy__jehvt.meminfo = uau__psfg
        gqk__obtjw = zyy__jehvt._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, gqk__obtjw)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        jvyr__chp, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            jvyr__chp = builder.extract_value(jvyr__chp, 0)
        return builder.bitcast(builder.gep(jvyr__chp, [ind]), lir.IntType(8
            ).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        jvyr__chp, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            jvyr__chp = builder.extract_value(jvyr__chp, 0)
        return builder.load(builder.gep(jvyr__chp, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        jvyr__chp, ind, snzxc__wiieq = args
        aht__svbi = builder.gep(jvyr__chp, [ind])
        builder.store(snzxc__wiieq, aht__svbi)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        omskc__swfa, ind = args
        eulg__tjbgh = context.make_helper(builder, arr_ctypes_t, omskc__swfa)
        rednh__wwgh = context.make_helper(builder, arr_ctypes_t)
        rednh__wwgh.data = builder.gep(eulg__tjbgh.data, [ind])
        rednh__wwgh.meminfo = eulg__tjbgh.meminfo
        lrvgu__oly = rednh__wwgh._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, lrvgu__oly)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    saxk__ikoo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not saxk__ikoo:
        return 0, 0, 0
    sry__gejqe = getitem_c_arr(arr._index_offsets, item_ind)
    gkiq__medb = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    hlsd__pxh = gkiq__medb - sry__gejqe
    if str_ind >= hlsd__pxh:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, sry__gejqe + str_ind)
    data_start += 1
    if sry__gejqe + str_ind == 0:
        data_start = 0
    dvyu__ekr = getitem_c_arr(arr._data_offsets, sry__gejqe + str_ind + 1)
    snpr__uxgf = dvyu__ekr - data_start
    return 1, data_start, snpr__uxgf


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
        qfur__kqhb = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            sry__gejqe = getitem_c_arr(A._index_offsets, ind)
            gkiq__medb = getitem_c_arr(A._index_offsets, ind + 1)
            tjgwi__uigd = gkiq__medb - sry__gejqe - 1
            ykvl__yow = bodo.libs.str_arr_ext.pre_alloc_string_array(
                tjgwi__uigd, -1)
            for cqg__knshz in range(tjgwi__uigd):
                data_start = getitem_c_arr(A._data_offsets, sry__gejqe +
                    cqg__knshz)
                data_start += 1
                if sry__gejqe + cqg__knshz == 0:
                    data_start = 0
                dvyu__ekr = getitem_c_arr(A._data_offsets, sry__gejqe +
                    cqg__knshz + 1)
                snpr__uxgf = dvyu__ekr - data_start
                aht__svbi = get_array_ctypes_ptr(A._data, data_start)
                upxf__aqf = bodo.libs.str_arr_ext.decode_utf8(aht__svbi,
                    snpr__uxgf)
                ykvl__yow[cqg__knshz] = upxf__aqf
            return ykvl__yow
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        xwgl__ykeg = offset_type.bitwidth // 8

        def _impl(A, ind):
            tjgwi__uigd = len(A)
            if tjgwi__uigd != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            jkl__lnxkx = 0
            jqdpz__nvi = 0
            for cqg__knshz in range(tjgwi__uigd):
                if ind[cqg__knshz]:
                    jkl__lnxkx += 1
                    sry__gejqe = getitem_c_arr(A._index_offsets, cqg__knshz)
                    gkiq__medb = getitem_c_arr(A._index_offsets, cqg__knshz + 1
                        )
                    jqdpz__nvi += gkiq__medb - sry__gejqe
            wwklo__irrev = pre_alloc_str_arr_view(jkl__lnxkx, jqdpz__nvi, A
                ._data)
            item_ind = 0
            sbmyz__tvtza = 0
            for cqg__knshz in range(tjgwi__uigd):
                if ind[cqg__knshz]:
                    sry__gejqe = getitem_c_arr(A._index_offsets, cqg__knshz)
                    gkiq__medb = getitem_c_arr(A._index_offsets, cqg__knshz + 1
                        )
                    jlwgz__mly = gkiq__medb - sry__gejqe
                    setitem_c_arr(wwklo__irrev._index_offsets, item_ind,
                        sbmyz__tvtza)
                    aht__svbi = get_c_arr_ptr(A._data_offsets, sry__gejqe)
                    yji__vclz = get_c_arr_ptr(wwklo__irrev._data_offsets,
                        sbmyz__tvtza)
                    _memcpy(yji__vclz, aht__svbi, jlwgz__mly, xwgl__ykeg)
                    saxk__ikoo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, cqg__knshz)
                    bodo.libs.int_arr_ext.set_bit_to_arr(wwklo__irrev.
                        _null_bitmap, item_ind, saxk__ikoo)
                    item_ind += 1
                    sbmyz__tvtza += jlwgz__mly
            setitem_c_arr(wwklo__irrev._index_offsets, item_ind, sbmyz__tvtza)
            return wwklo__irrev
        return _impl
