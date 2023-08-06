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
        tepc__xvlle = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, tepc__xvlle)


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
    wil__iawqg = context.get_value_type(str_arr_split_view_payload_type)
    xirz__fbrxw = context.get_abi_sizeof(wil__iawqg)
    luocz__fon = context.get_value_type(types.voidptr)
    mwix__tkfdy = context.get_value_type(types.uintp)
    gii__lhn = lir.FunctionType(lir.VoidType(), [luocz__fon, mwix__tkfdy,
        luocz__fon])
    jre__vgjtn = cgutils.get_or_insert_function(builder.module, gii__lhn,
        name='dtor_str_arr_split_view')
    xgwqz__miyv = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, xirz__fbrxw), jre__vgjtn)
    pirhc__pjw = context.nrt.meminfo_data(builder, xgwqz__miyv)
    snot__obvz = builder.bitcast(pirhc__pjw, wil__iawqg.as_pointer())
    return xgwqz__miyv, snot__obvz


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        koe__cyda, qbcy__hhdjf = args
        xgwqz__miyv, snot__obvz = construct_str_arr_split_view(context, builder
            )
        qgs__mgg = _get_str_binary_arr_payload(context, builder, koe__cyda,
            string_array_type)
        kor__dxl = lir.FunctionType(lir.VoidType(), [snot__obvz.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        zonhi__bcrzm = cgutils.get_or_insert_function(builder.module,
            kor__dxl, name='str_arr_split_view_impl')
        ihzwt__jwtw = context.make_helper(builder, offset_arr_type,
            qgs__mgg.offsets).data
        ytktr__lylhk = context.make_helper(builder, char_arr_type, qgs__mgg
            .data).data
        cbcbj__tczfd = context.make_helper(builder, null_bitmap_arr_type,
            qgs__mgg.null_bitmap).data
        gam__gkl = context.get_constant(types.int8, ord(sep_typ.literal_value))
        builder.call(zonhi__bcrzm, [snot__obvz, qgs__mgg.n_arrays,
            ihzwt__jwtw, ytktr__lylhk, cbcbj__tczfd, gam__gkl])
        okpd__yrows = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(snot__obvz))
        yzmqf__bepu = context.make_helper(builder, string_array_split_view_type
            )
        yzmqf__bepu.num_items = qgs__mgg.n_arrays
        yzmqf__bepu.index_offsets = okpd__yrows.index_offsets
        yzmqf__bepu.data_offsets = okpd__yrows.data_offsets
        yzmqf__bepu.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [koe__cyda])
        yzmqf__bepu.null_bitmap = okpd__yrows.null_bitmap
        yzmqf__bepu.meminfo = xgwqz__miyv
        klts__uqlwl = yzmqf__bepu._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, klts__uqlwl)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    jlw__oph = context.make_helper(builder, string_array_split_view_type, val)
    yto__gyym = context.insert_const_string(builder.module, 'numpy')
    ofgl__rildz = c.pyapi.import_module_noblock(yto__gyym)
    dtype = c.pyapi.object_getattr_string(ofgl__rildz, 'object_')
    wdvy__njxie = builder.sext(jlw__oph.num_items, c.pyapi.longlong)
    gks__cun = c.pyapi.long_from_longlong(wdvy__njxie)
    nrxvk__zfuto = c.pyapi.call_method(ofgl__rildz, 'ndarray', (gks__cun,
        dtype))
    ppgnz__zll = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    twwj__smj = c.pyapi._get_function(ppgnz__zll, name='array_getptr1')
    lkfwh__ftda = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    eqgwv__ksak = c.pyapi._get_function(lkfwh__ftda, name='array_setitem')
    kmgv__yjzx = c.pyapi.object_getattr_string(ofgl__rildz, 'nan')
    with cgutils.for_range(builder, jlw__oph.num_items) as srrn__yht:
        str_ind = srrn__yht.index
        lhh__qorgo = builder.sext(builder.load(builder.gep(jlw__oph.
            index_offsets, [str_ind])), lir.IntType(64))
        tfl__uhiq = builder.sext(builder.load(builder.gep(jlw__oph.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        ruwdb__sfp = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        ynrud__gom = builder.gep(jlw__oph.null_bitmap, [ruwdb__sfp])
        crgan__codux = builder.load(ynrud__gom)
        pau__nouki = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(crgan__codux, pau__nouki), lir.
            Constant(lir.IntType(8), 1))
        kdwbg__qqj = builder.sub(tfl__uhiq, lhh__qorgo)
        kdwbg__qqj = builder.sub(kdwbg__qqj, kdwbg__qqj.type(1))
        pogf__vlsn = builder.call(twwj__smj, [nrxvk__zfuto, str_ind])
        kbww__dkr = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(kbww__dkr) as (qxyzr__sskyh, erlq__xpwv):
            with qxyzr__sskyh:
                ydx__nje = c.pyapi.list_new(kdwbg__qqj)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    ydx__nje), likely=True):
                    with cgutils.for_range(c.builder, kdwbg__qqj) as srrn__yht:
                        otzm__oushb = builder.add(lhh__qorgo, srrn__yht.index)
                        data_start = builder.load(builder.gep(jlw__oph.
                            data_offsets, [otzm__oushb]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        ttj__slrv = builder.load(builder.gep(jlw__oph.
                            data_offsets, [builder.add(otzm__oushb,
                            otzm__oushb.type(1))]))
                        cinvt__ukpv = builder.gep(builder.extract_value(
                            jlw__oph.data, 0), [data_start])
                        gxxdo__kduvk = builder.sext(builder.sub(ttj__slrv,
                            data_start), lir.IntType(64))
                        hklut__zbdu = c.pyapi.string_from_string_and_size(
                            cinvt__ukpv, gxxdo__kduvk)
                        c.pyapi.list_setitem(ydx__nje, srrn__yht.index,
                            hklut__zbdu)
                builder.call(eqgwv__ksak, [nrxvk__zfuto, pogf__vlsn, ydx__nje])
            with erlq__xpwv:
                builder.call(eqgwv__ksak, [nrxvk__zfuto, pogf__vlsn,
                    kmgv__yjzx])
    c.pyapi.decref(ofgl__rildz)
    c.pyapi.decref(dtype)
    c.pyapi.decref(kmgv__yjzx)
    return nrxvk__zfuto


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        ktsa__ican, iwpm__ybixq, cinvt__ukpv = args
        xgwqz__miyv, snot__obvz = construct_str_arr_split_view(context, builder
            )
        kor__dxl = lir.FunctionType(lir.VoidType(), [snot__obvz.type, lir.
            IntType(64), lir.IntType(64)])
        zonhi__bcrzm = cgutils.get_or_insert_function(builder.module,
            kor__dxl, name='str_arr_split_view_alloc')
        builder.call(zonhi__bcrzm, [snot__obvz, ktsa__ican, iwpm__ybixq])
        okpd__yrows = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(snot__obvz))
        yzmqf__bepu = context.make_helper(builder, string_array_split_view_type
            )
        yzmqf__bepu.num_items = ktsa__ican
        yzmqf__bepu.index_offsets = okpd__yrows.index_offsets
        yzmqf__bepu.data_offsets = okpd__yrows.data_offsets
        yzmqf__bepu.data = cinvt__ukpv
        yzmqf__bepu.null_bitmap = okpd__yrows.null_bitmap
        context.nrt.incref(builder, data_t, cinvt__ukpv)
        yzmqf__bepu.meminfo = xgwqz__miyv
        klts__uqlwl = yzmqf__bepu._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, klts__uqlwl)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        mga__cugy, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mga__cugy = builder.extract_value(mga__cugy, 0)
        return builder.bitcast(builder.gep(mga__cugy, [ind]), lir.IntType(8
            ).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        mga__cugy, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mga__cugy = builder.extract_value(mga__cugy, 0)
        return builder.load(builder.gep(mga__cugy, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        mga__cugy, ind, rpc__rthj = args
        gtven__guzp = builder.gep(mga__cugy, [ind])
        builder.store(rpc__rthj, gtven__guzp)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        ias__wvxuq, ind = args
        iaiyx__vcbf = context.make_helper(builder, arr_ctypes_t, ias__wvxuq)
        zugo__zgge = context.make_helper(builder, arr_ctypes_t)
        zugo__zgge.data = builder.gep(iaiyx__vcbf.data, [ind])
        zugo__zgge.meminfo = iaiyx__vcbf.meminfo
        wawdu__oqi = zugo__zgge._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, wawdu__oqi)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    onsuk__oul = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not onsuk__oul:
        return 0, 0, 0
    otzm__oushb = getitem_c_arr(arr._index_offsets, item_ind)
    egrtx__hkwd = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    sljrq__fsp = egrtx__hkwd - otzm__oushb
    if str_ind >= sljrq__fsp:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, otzm__oushb + str_ind)
    data_start += 1
    if otzm__oushb + str_ind == 0:
        data_start = 0
    ttj__slrv = getitem_c_arr(arr._data_offsets, otzm__oushb + str_ind + 1)
    vef__lrrpt = ttj__slrv - data_start
    return 1, data_start, vef__lrrpt


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
        sassh__ghzp = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            otzm__oushb = getitem_c_arr(A._index_offsets, ind)
            egrtx__hkwd = getitem_c_arr(A._index_offsets, ind + 1)
            pbnbf__yfoq = egrtx__hkwd - otzm__oushb - 1
            koe__cyda = bodo.libs.str_arr_ext.pre_alloc_string_array(
                pbnbf__yfoq, -1)
            for qrsw__ehwgl in range(pbnbf__yfoq):
                data_start = getitem_c_arr(A._data_offsets, otzm__oushb +
                    qrsw__ehwgl)
                data_start += 1
                if otzm__oushb + qrsw__ehwgl == 0:
                    data_start = 0
                ttj__slrv = getitem_c_arr(A._data_offsets, otzm__oushb +
                    qrsw__ehwgl + 1)
                vef__lrrpt = ttj__slrv - data_start
                gtven__guzp = get_array_ctypes_ptr(A._data, data_start)
                ayd__tuq = bodo.libs.str_arr_ext.decode_utf8(gtven__guzp,
                    vef__lrrpt)
                koe__cyda[qrsw__ehwgl] = ayd__tuq
            return koe__cyda
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        ttab__mdbty = offset_type.bitwidth // 8

        def _impl(A, ind):
            pbnbf__yfoq = len(A)
            if pbnbf__yfoq != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            ktsa__ican = 0
            iwpm__ybixq = 0
            for qrsw__ehwgl in range(pbnbf__yfoq):
                if ind[qrsw__ehwgl]:
                    ktsa__ican += 1
                    otzm__oushb = getitem_c_arr(A._index_offsets, qrsw__ehwgl)
                    egrtx__hkwd = getitem_c_arr(A._index_offsets, 
                        qrsw__ehwgl + 1)
                    iwpm__ybixq += egrtx__hkwd - otzm__oushb
            nrxvk__zfuto = pre_alloc_str_arr_view(ktsa__ican, iwpm__ybixq,
                A._data)
            item_ind = 0
            amabz__oqfxs = 0
            for qrsw__ehwgl in range(pbnbf__yfoq):
                if ind[qrsw__ehwgl]:
                    otzm__oushb = getitem_c_arr(A._index_offsets, qrsw__ehwgl)
                    egrtx__hkwd = getitem_c_arr(A._index_offsets, 
                        qrsw__ehwgl + 1)
                    gsje__aostx = egrtx__hkwd - otzm__oushb
                    setitem_c_arr(nrxvk__zfuto._index_offsets, item_ind,
                        amabz__oqfxs)
                    gtven__guzp = get_c_arr_ptr(A._data_offsets, otzm__oushb)
                    qua__ljg = get_c_arr_ptr(nrxvk__zfuto._data_offsets,
                        amabz__oqfxs)
                    _memcpy(qua__ljg, gtven__guzp, gsje__aostx, ttab__mdbty)
                    onsuk__oul = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, qrsw__ehwgl)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nrxvk__zfuto.
                        _null_bitmap, item_ind, onsuk__oul)
                    item_ind += 1
                    amabz__oqfxs += gsje__aostx
            setitem_c_arr(nrxvk__zfuto._index_offsets, item_ind, amabz__oqfxs)
            return nrxvk__zfuto
        return _impl
