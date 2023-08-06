"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('pivot_groupby_and_aggregate', array_ext.
    pivot_groupby_and_aggregate)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        rvsdo__uxxpd = context.make_helper(builder, arr_type, in_arr)
        in_arr = rvsdo__uxxpd.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        bbmh__nvq = context.make_helper(builder, arr_type, in_arr)
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='list_string_array_to_info')
        return builder.call(idi__ythj, [bbmh__nvq.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                mtrq__dytm = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for fpfx__okmt in arr_typ.data:
                    mtrq__dytm += get_types(fpfx__okmt)
                return mtrq__dytm
            elif isinstance(arr_typ, (types.Array, IntegerArrayType)
                ) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            phwhj__kbbf = context.compile_internal(builder, lambda a: len(a
                ), types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                posco__ubb = context.make_helper(builder, arr_typ, value=arr)
                atq__fxt = get_lengths(_get_map_arr_data_type(arr_typ),
                    posco__ubb.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                kko__xnw = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                atq__fxt = get_lengths(arr_typ.dtype, kko__xnw.data)
                atq__fxt = cgutils.pack_array(builder, [kko__xnw.n_arrays] +
                    [builder.extract_value(atq__fxt, dtkz__vytut) for
                    dtkz__vytut in range(atq__fxt.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                kko__xnw = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                atq__fxt = []
                for dtkz__vytut, fpfx__okmt in enumerate(arr_typ.data):
                    gmpxi__orn = get_lengths(fpfx__okmt, builder.
                        extract_value(kko__xnw.data, dtkz__vytut))
                    atq__fxt += [builder.extract_value(gmpxi__orn,
                        odiw__psxi) for odiw__psxi in range(gmpxi__orn.type
                        .count)]
                atq__fxt = cgutils.pack_array(builder, [phwhj__kbbf,
                    context.get_constant(types.int64, -1)] + atq__fxt)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                atq__fxt = cgutils.pack_array(builder, [phwhj__kbbf])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return atq__fxt

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                posco__ubb = context.make_helper(builder, arr_typ, value=arr)
                wpqcn__mxeey = get_buffers(_get_map_arr_data_type(arr_typ),
                    posco__ubb.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                kko__xnw = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                xjza__dsrj = get_buffers(arr_typ.dtype, kko__xnw.data)
                dtahv__ukn = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, kko__xnw.offsets)
                jail__fpzr = builder.bitcast(dtahv__ukn.data, lir.IntType(8
                    ).as_pointer())
                nlon__vplq = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, kko__xnw.null_bitmap)
                hnbh__xvb = builder.bitcast(nlon__vplq.data, lir.IntType(8)
                    .as_pointer())
                wpqcn__mxeey = cgutils.pack_array(builder, [jail__fpzr,
                    hnbh__xvb] + [builder.extract_value(xjza__dsrj,
                    dtkz__vytut) for dtkz__vytut in range(xjza__dsrj.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                kko__xnw = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                xjza__dsrj = []
                for dtkz__vytut, fpfx__okmt in enumerate(arr_typ.data):
                    vorv__bvr = get_buffers(fpfx__okmt, builder.
                        extract_value(kko__xnw.data, dtkz__vytut))
                    xjza__dsrj += [builder.extract_value(vorv__bvr,
                        odiw__psxi) for odiw__psxi in range(vorv__bvr.type.
                        count)]
                nlon__vplq = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, kko__xnw.null_bitmap)
                hnbh__xvb = builder.bitcast(nlon__vplq.data, lir.IntType(8)
                    .as_pointer())
                wpqcn__mxeey = cgutils.pack_array(builder, [hnbh__xvb] +
                    xjza__dsrj)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                rvbj__okev = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    rvbj__okev = int128_type
                elif arr_typ == datetime_date_array_type:
                    rvbj__okev = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                veiu__tvtt = context.make_array(types.Array(rvbj__okev, 1, 'C')
                    )(context, builder, arr.data)
                nlon__vplq = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                qxzfy__ximhg = builder.bitcast(veiu__tvtt.data, lir.IntType
                    (8).as_pointer())
                hnbh__xvb = builder.bitcast(nlon__vplq.data, lir.IntType(8)
                    .as_pointer())
                wpqcn__mxeey = cgutils.pack_array(builder, [hnbh__xvb,
                    qxzfy__ximhg])
            elif arr_typ in (string_array_type, binary_array_type):
                kko__xnw = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                zti__avvwe = context.make_helper(builder, offset_arr_type,
                    kko__xnw.offsets).data
                otjlw__zzim = context.make_helper(builder, char_arr_type,
                    kko__xnw.data).data
                myy__qiu = context.make_helper(builder,
                    null_bitmap_arr_type, kko__xnw.null_bitmap).data
                wpqcn__mxeey = cgutils.pack_array(builder, [builder.bitcast
                    (zti__avvwe, lir.IntType(8).as_pointer()), builder.
                    bitcast(myy__qiu, lir.IntType(8).as_pointer()), builder
                    .bitcast(otjlw__zzim, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                qxzfy__ximhg = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                mvun__oyt = lir.Constant(lir.IntType(8).as_pointer(), None)
                wpqcn__mxeey = cgutils.pack_array(builder, [mvun__oyt,
                    qxzfy__ximhg])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return wpqcn__mxeey

        def get_field_names(arr_typ):
            ovpow__ard = []
            if isinstance(arr_typ, StructArrayType):
                for qtzma__vdhzo, hgbbs__syz in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    ovpow__ard.append(qtzma__vdhzo)
                    ovpow__ard += get_field_names(hgbbs__syz)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ovpow__ard += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                ovpow__ard += get_field_names(_get_map_arr_data_type(arr_typ))
            return ovpow__ard
        mtrq__dytm = get_types(arr_type)
        jlkap__aqup = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in mtrq__dytm])
        opocn__wtqy = cgutils.alloca_once_value(builder, jlkap__aqup)
        atq__fxt = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, atq__fxt)
        wpqcn__mxeey = get_buffers(arr_type, in_arr)
        mkzr__opc = cgutils.alloca_once_value(builder, wpqcn__mxeey)
        ovpow__ard = get_field_names(arr_type)
        if len(ovpow__ard) == 0:
            ovpow__ard = ['irrelevant']
        tas__yyo = cgutils.pack_array(builder, [context.insert_const_string
            (builder.module, a) for a in ovpow__ard])
        tvetr__rrhv = cgutils.alloca_once_value(builder, tas__yyo)
        if isinstance(arr_type, MapArrayType):
            rnqy__dvbdg = _get_map_arr_data_type(arr_type)
            bzvpb__xwgo = context.make_helper(builder, arr_type, value=in_arr)
            wdm__irhsk = bzvpb__xwgo.data
        else:
            rnqy__dvbdg = arr_type
            wdm__irhsk = in_arr
        jygkk__ofjd = context.make_helper(builder, rnqy__dvbdg, wdm__irhsk)
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='nested_array_to_info')
        amrq__glsgh = builder.call(idi__ythj, [builder.bitcast(opocn__wtqy,
            lir.IntType(32).as_pointer()), builder.bitcast(mkzr__opc, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            tvetr__rrhv, lir.IntType(8).as_pointer()), jygkk__ofjd.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    if arr_type in (string_array_type, binary_array_type):
        fzac__qob = context.make_helper(builder, arr_type, in_arr)
        zmb__mrkh = ArrayItemArrayType(char_arr_type)
        bbmh__nvq = context.make_helper(builder, zmb__mrkh, fzac__qob.data)
        kko__xnw = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        zti__avvwe = context.make_helper(builder, offset_arr_type, kko__xnw
            .offsets).data
        otjlw__zzim = context.make_helper(builder, char_arr_type, kko__xnw.data
            ).data
        myy__qiu = context.make_helper(builder, null_bitmap_arr_type,
            kko__xnw.null_bitmap).data
        adh__wtx = builder.zext(builder.load(builder.gep(zti__avvwe, [
            kko__xnw.n_arrays])), lir.IntType(64))
        mgmj__urtv = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='string_array_to_info')
        return builder.call(idi__ythj, [kko__xnw.n_arrays, adh__wtx,
            otjlw__zzim, zti__avvwe, myy__qiu, bbmh__nvq.meminfo, mgmj__urtv])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        odl__xhufu = arr.data
        aix__wdj = arr.indices
        sig = array_info_type(arr_type.data)
        txiag__mzb = array_to_info_codegen(context, builder, sig, (
            odl__xhufu,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        vru__rylyf = array_to_info_codegen(context, builder, sig, (aix__wdj
            ,), False)
        aec__ccjeu = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, aix__wdj)
        hnbh__xvb = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, aec__ccjeu.null_bitmap).data
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='dict_str_array_to_info')
        wyz__dfk = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(idi__ythj, [txiag__mzb, vru__rylyf, builder.
            bitcast(hnbh__xvb, lir.IntType(8).as_pointer()), wyz__dfk])
    zlf__sqew = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        rmmw__vzk = context.compile_internal(builder, lambda a: len(a.dtype
            .categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        kjp__ztjh = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(kjp__ztjh, 1, 'C')
        zlf__sqew = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if zlf__sqew:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        phwhj__kbbf = builder.extract_value(arr.shape, 0)
        jqnk__xpv = arr_type.dtype
        bryk__wxr = numba_to_c_type(jqnk__xpv)
        hfaxf__yvez = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), bryk__wxr))
        if zlf__sqew:
            zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            idi__ythj = cgutils.get_or_insert_function(builder.module,
                zlpj__qjecv, name='categorical_array_to_info')
            return builder.call(idi__ythj, [phwhj__kbbf, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                hfaxf__yvez), rmmw__vzk, arr.meminfo])
        else:
            zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            idi__ythj = cgutils.get_or_insert_function(builder.module,
                zlpj__qjecv, name='numpy_array_to_info')
            return builder.call(idi__ythj, [phwhj__kbbf, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                hfaxf__yvez), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        jqnk__xpv = arr_type.dtype
        rvbj__okev = jqnk__xpv
        if isinstance(arr_type, DecimalArrayType):
            rvbj__okev = int128_type
        if arr_type == datetime_date_array_type:
            rvbj__okev = types.int64
        veiu__tvtt = context.make_array(types.Array(rvbj__okev, 1, 'C'))(
            context, builder, arr.data)
        phwhj__kbbf = builder.extract_value(veiu__tvtt.shape, 0)
        cemmi__lwgyc = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        bryk__wxr = numba_to_c_type(jqnk__xpv)
        hfaxf__yvez = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), bryk__wxr))
        if isinstance(arr_type, DecimalArrayType):
            zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            idi__ythj = cgutils.get_or_insert_function(builder.module,
                zlpj__qjecv, name='decimal_array_to_info')
            return builder.call(idi__ythj, [phwhj__kbbf, builder.bitcast(
                veiu__tvtt.data, lir.IntType(8).as_pointer()), builder.load
                (hfaxf__yvez), builder.bitcast(cemmi__lwgyc.data, lir.
                IntType(8).as_pointer()), veiu__tvtt.meminfo, cemmi__lwgyc.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        else:
            zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            idi__ythj = cgutils.get_or_insert_function(builder.module,
                zlpj__qjecv, name='nullable_array_to_info')
            return builder.call(idi__ythj, [phwhj__kbbf, builder.bitcast(
                veiu__tvtt.data, lir.IntType(8).as_pointer()), builder.load
                (hfaxf__yvez), builder.bitcast(cemmi__lwgyc.data, lir.
                IntType(8).as_pointer()), veiu__tvtt.meminfo, cemmi__lwgyc.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        zvhxy__sozb = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        salih__isi = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        phwhj__kbbf = builder.extract_value(zvhxy__sozb.shape, 0)
        bryk__wxr = numba_to_c_type(arr_type.arr_type.dtype)
        hfaxf__yvez = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), bryk__wxr))
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='interval_array_to_info')
        return builder.call(idi__ythj, [phwhj__kbbf, builder.bitcast(
            zvhxy__sozb.data, lir.IntType(8).as_pointer()), builder.bitcast
            (salih__isi.data, lir.IntType(8).as_pointer()), builder.load(
            hfaxf__yvez), zvhxy__sozb.meminfo, salih__isi.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    madcf__ortba = cgutils.alloca_once(builder, lir.IntType(64))
    qxzfy__ximhg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    qgsq__kotz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    idi__ythj = cgutils.get_or_insert_function(builder.module, zlpj__qjecv,
        name='info_to_numpy_array')
    builder.call(idi__ythj, [in_info, madcf__ortba, qxzfy__ximhg, qgsq__kotz])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    tch__lmv = context.get_value_type(types.intp)
    lpeju__psvj = cgutils.pack_array(builder, [builder.load(madcf__ortba)],
        ty=tch__lmv)
    efd__vhbr = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    kpf__ptt = cgutils.pack_array(builder, [efd__vhbr], ty=tch__lmv)
    otjlw__zzim = builder.bitcast(builder.load(qxzfy__ximhg), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=otjlw__zzim, shape=
        lpeju__psvj, strides=kpf__ptt, itemsize=efd__vhbr, meminfo=builder.
        load(qgsq__kotz))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    iyr__rriqh = context.make_helper(builder, arr_type)
    zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    idi__ythj = cgutils.get_or_insert_function(builder.module, zlpj__qjecv,
        name='info_to_list_string_array')
    builder.call(idi__ythj, [in_info, iyr__rriqh._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return iyr__rriqh._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    yrnd__phpdi = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        tmua__wcc = lengths_pos
        eez__tazrg = infos_pos
        rlud__dzh, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        tzk__cxy = ArrayItemArrayPayloadType(arr_typ)
        aphk__ncr = context.get_data_type(tzk__cxy)
        rdykm__qdt = context.get_abi_sizeof(aphk__ncr)
        qgfo__bgt = define_array_item_dtor(context, builder, arr_typ, tzk__cxy)
        ucyii__xjzho = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, rdykm__qdt), qgfo__bgt)
        beco__megt = context.nrt.meminfo_data(builder, ucyii__xjzho)
        hgkeu__nhw = builder.bitcast(beco__megt, aphk__ncr.as_pointer())
        kko__xnw = cgutils.create_struct_proxy(tzk__cxy)(context, builder)
        kko__xnw.n_arrays = builder.extract_value(builder.load(lengths_ptr),
            tmua__wcc)
        kko__xnw.data = rlud__dzh
        diiij__wpk = builder.load(array_infos_ptr)
        tjq__mjb = builder.bitcast(builder.extract_value(diiij__wpk,
            eez__tazrg), yrnd__phpdi)
        kko__xnw.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, tjq__mjb)
        ovjtt__wkzu = builder.bitcast(builder.extract_value(diiij__wpk, 
            eez__tazrg + 1), yrnd__phpdi)
        kko__xnw.null_bitmap = _lower_info_to_array_numpy(types.Array(types
            .uint8, 1, 'C'), context, builder, ovjtt__wkzu)
        builder.store(kko__xnw._getvalue(), hgkeu__nhw)
        bbmh__nvq = context.make_helper(builder, arr_typ)
        bbmh__nvq.meminfo = ucyii__xjzho
        return bbmh__nvq._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        akcn__ueijg = []
        eez__tazrg = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for hpcb__try in arr_typ.data:
            rlud__dzh, lengths_pos, infos_pos = nested_to_array(context,
                builder, hpcb__try, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            akcn__ueijg.append(rlud__dzh)
        tzk__cxy = StructArrayPayloadType(arr_typ.data)
        aphk__ncr = context.get_value_type(tzk__cxy)
        rdykm__qdt = context.get_abi_sizeof(aphk__ncr)
        qgfo__bgt = define_struct_arr_dtor(context, builder, arr_typ, tzk__cxy)
        ucyii__xjzho = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, rdykm__qdt), qgfo__bgt)
        beco__megt = context.nrt.meminfo_data(builder, ucyii__xjzho)
        hgkeu__nhw = builder.bitcast(beco__megt, aphk__ncr.as_pointer())
        kko__xnw = cgutils.create_struct_proxy(tzk__cxy)(context, builder)
        kko__xnw.data = cgutils.pack_array(builder, akcn__ueijg
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, akcn__ueijg)
        diiij__wpk = builder.load(array_infos_ptr)
        ovjtt__wkzu = builder.bitcast(builder.extract_value(diiij__wpk,
            eez__tazrg), yrnd__phpdi)
        kko__xnw.null_bitmap = _lower_info_to_array_numpy(types.Array(types
            .uint8, 1, 'C'), context, builder, ovjtt__wkzu)
        builder.store(kko__xnw._getvalue(), hgkeu__nhw)
        xyozg__bow = context.make_helper(builder, arr_typ)
        xyozg__bow.meminfo = ucyii__xjzho
        return xyozg__bow._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        diiij__wpk = builder.load(array_infos_ptr)
        salyj__xcn = builder.bitcast(builder.extract_value(diiij__wpk,
            infos_pos), yrnd__phpdi)
        fzac__qob = context.make_helper(builder, arr_typ)
        zmb__mrkh = ArrayItemArrayType(char_arr_type)
        bbmh__nvq = context.make_helper(builder, zmb__mrkh)
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_to_string_array')
        builder.call(idi__ythj, [salyj__xcn, bbmh__nvq._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        fzac__qob.data = bbmh__nvq._getvalue()
        return fzac__qob._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        diiij__wpk = builder.load(array_infos_ptr)
        pap__mqb = builder.bitcast(builder.extract_value(diiij__wpk, 
            infos_pos + 1), yrnd__phpdi)
        return _lower_info_to_array_numpy(arr_typ, context, builder, pap__mqb
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        rvbj__okev = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            rvbj__okev = int128_type
        elif arr_typ == datetime_date_array_type:
            rvbj__okev = types.int64
        diiij__wpk = builder.load(array_infos_ptr)
        ovjtt__wkzu = builder.bitcast(builder.extract_value(diiij__wpk,
            infos_pos), yrnd__phpdi)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, ovjtt__wkzu)
        pap__mqb = builder.bitcast(builder.extract_value(diiij__wpk, 
            infos_pos + 1), yrnd__phpdi)
        arr.data = _lower_info_to_array_numpy(types.Array(rvbj__okev, 1,
            'C'), context, builder, pap__mqb)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, agg__ocv = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(hpcb__try) for hpcb__try in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(hpcb__try) for hpcb__try in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            rgi__nlfqc = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            rgi__nlfqc = _get_map_arr_data_type(arr_type)
        else:
            rgi__nlfqc = arr_type
        rghl__vub = get_num_arrays(rgi__nlfqc)
        atq__fxt = cgutils.pack_array(builder, [lir.Constant(lir.IntType(64
            ), 0) for agg__ocv in range(rghl__vub)])
        lengths_ptr = cgutils.alloca_once_value(builder, atq__fxt)
        mvun__oyt = lir.Constant(lir.IntType(8).as_pointer(), None)
        liuk__cugt = cgutils.pack_array(builder, [mvun__oyt for agg__ocv in
            range(get_num_infos(rgi__nlfqc))])
        array_infos_ptr = cgutils.alloca_once_value(builder, liuk__cugt)
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_to_nested_array')
        builder.call(idi__ythj, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, agg__ocv, agg__ocv = nested_to_array(context, builder,
            rgi__nlfqc, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            rvsdo__uxxpd = context.make_helper(builder, arr_type)
            rvsdo__uxxpd.data = arr
            context.nrt.incref(builder, rgi__nlfqc, arr)
            arr = rvsdo__uxxpd._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, rgi__nlfqc)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        fzac__qob = context.make_helper(builder, arr_type)
        zmb__mrkh = ArrayItemArrayType(char_arr_type)
        bbmh__nvq = context.make_helper(builder, zmb__mrkh)
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_to_string_array')
        builder.call(idi__ythj, [in_info, bbmh__nvq._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        fzac__qob.data = bbmh__nvq._getvalue()
        return fzac__qob._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='get_nested_info')
        txiag__mzb = builder.call(idi__ythj, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        vru__rylyf = builder.call(idi__ythj, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        ynnzk__pmpt = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        ynnzk__pmpt.data = info_to_array_codegen(context, builder, sig, (
            txiag__mzb, context.get_constant_null(arr_type.data)))
        fyro__yuy = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = fyro__yuy(array_info_type, fyro__yuy)
        ynnzk__pmpt.indices = info_to_array_codegen(context, builder, sig,
            (vru__rylyf, context.get_constant_null(fyro__yuy)))
        zlpj__qjecv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='get_has_global_dictionary')
        wyz__dfk = builder.call(idi__ythj, [in_info])
        ynnzk__pmpt.has_global_dictionary = builder.trunc(wyz__dfk, cgutils
            .bool_t)
        return ynnzk__pmpt._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        kjp__ztjh = get_categories_int_type(arr_type.dtype)
        uqvm__tlx = types.Array(kjp__ztjh, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(uqvm__tlx, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            vne__ggju = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(vne__ggju))
            int_type = arr_type.dtype.int_type
            awvln__uqqx = bodo.typeof(vne__ggju)
            vbhs__udu = context.get_constant_generic(builder, awvln__uqqx,
                vne__ggju)
            jqnk__xpv = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(awvln__uqqx), [vbhs__udu])
        else:
            jqnk__xpv = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, jqnk__xpv)
        out_arr.dtype = jqnk__xpv
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        otjlw__zzim = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = otjlw__zzim
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        rvbj__okev = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            rvbj__okev = int128_type
        elif arr_type == datetime_date_array_type:
            rvbj__okev = types.int64
        zwcq__rju = types.Array(rvbj__okev, 1, 'C')
        veiu__tvtt = context.make_array(zwcq__rju)(context, builder)
        cigmr__lceez = types.Array(types.uint8, 1, 'C')
        srh__orkm = context.make_array(cigmr__lceez)(context, builder)
        madcf__ortba = cgutils.alloca_once(builder, lir.IntType(64))
        qdir__uhbv = cgutils.alloca_once(builder, lir.IntType(64))
        qxzfy__ximhg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        rtcen__bcor = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        qgsq__kotz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        owfb__simn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_to_nullable_array')
        builder.call(idi__ythj, [in_info, madcf__ortba, qdir__uhbv,
            qxzfy__ximhg, rtcen__bcor, qgsq__kotz, owfb__simn])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        tch__lmv = context.get_value_type(types.intp)
        lpeju__psvj = cgutils.pack_array(builder, [builder.load(
            madcf__ortba)], ty=tch__lmv)
        efd__vhbr = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(rvbj__okev)))
        kpf__ptt = cgutils.pack_array(builder, [efd__vhbr], ty=tch__lmv)
        otjlw__zzim = builder.bitcast(builder.load(qxzfy__ximhg), context.
            get_data_type(rvbj__okev).as_pointer())
        numba.np.arrayobj.populate_array(veiu__tvtt, data=otjlw__zzim,
            shape=lpeju__psvj, strides=kpf__ptt, itemsize=efd__vhbr,
            meminfo=builder.load(qgsq__kotz))
        arr.data = veiu__tvtt._getvalue()
        lpeju__psvj = cgutils.pack_array(builder, [builder.load(qdir__uhbv)
            ], ty=tch__lmv)
        efd__vhbr = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(types.uint8)))
        kpf__ptt = cgutils.pack_array(builder, [efd__vhbr], ty=tch__lmv)
        otjlw__zzim = builder.bitcast(builder.load(rtcen__bcor), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(srh__orkm, data=otjlw__zzim, shape
            =lpeju__psvj, strides=kpf__ptt, itemsize=efd__vhbr, meminfo=
            builder.load(owfb__simn))
        arr.null_bitmap = srh__orkm._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        zvhxy__sozb = context.make_array(arr_type.arr_type)(context, builder)
        salih__isi = context.make_array(arr_type.arr_type)(context, builder)
        madcf__ortba = cgutils.alloca_once(builder, lir.IntType(64))
        xfwg__mfx = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wyzr__uxqa = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        pkxln__tev = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wxa__bcdma = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_to_interval_array')
        builder.call(idi__ythj, [in_info, madcf__ortba, xfwg__mfx,
            wyzr__uxqa, pkxln__tev, wxa__bcdma])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        tch__lmv = context.get_value_type(types.intp)
        lpeju__psvj = cgutils.pack_array(builder, [builder.load(
            madcf__ortba)], ty=tch__lmv)
        efd__vhbr = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(arr_type.arr_type.dtype)))
        kpf__ptt = cgutils.pack_array(builder, [efd__vhbr], ty=tch__lmv)
        opnxc__ukys = builder.bitcast(builder.load(xfwg__mfx), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(zvhxy__sozb, data=opnxc__ukys,
            shape=lpeju__psvj, strides=kpf__ptt, itemsize=efd__vhbr,
            meminfo=builder.load(pkxln__tev))
        arr.left = zvhxy__sozb._getvalue()
        ftcrh__rumkm = builder.bitcast(builder.load(wyzr__uxqa), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(salih__isi, data=ftcrh__rumkm,
            shape=lpeju__psvj, strides=kpf__ptt, itemsize=efd__vhbr,
            meminfo=builder.load(wxa__bcdma))
        arr.right = salih__isi._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        phwhj__kbbf, agg__ocv = args
        bryk__wxr = numba_to_c_type(array_type.dtype)
        hfaxf__yvez = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), bryk__wxr))
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='alloc_numpy')
        return builder.call(idi__ythj, [phwhj__kbbf, builder.load(hfaxf__yvez)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        phwhj__kbbf, eht__mca = args
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='alloc_string_array')
        return builder.call(idi__ythj, [phwhj__kbbf, eht__mca])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    dtds__zvrmq, = args
    mga__tuazs = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], dtds__zvrmq)
    zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    idi__ythj = cgutils.get_or_insert_function(builder.module, zlpj__qjecv,
        name='arr_info_list_to_table')
    return builder.call(idi__ythj, [mga__tuazs.data, mga__tuazs.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_from_table')
        return builder.call(idi__ythj, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    bfur__brayb = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        uwai__yov, kqfj__ynio, agg__ocv = args
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='info_from_table')
        atc__xypul = cgutils.create_struct_proxy(bfur__brayb)(context, builder)
        atc__xypul.parent = cgutils.get_null_value(atc__xypul.parent.type)
        oen__njvqx = context.make_array(table_idx_arr_t)(context, builder,
            kqfj__ynio)
        kvzy__yeh = context.get_constant(types.int64, -1)
        zfv__kyr = context.get_constant(types.int64, 0)
        cqobf__wszyt = cgutils.alloca_once_value(builder, zfv__kyr)
        for t, vibr__radj in bfur__brayb.type_to_blk.items():
            ipvi__thop = context.get_constant(types.int64, len(bfur__brayb.
                block_to_arr_ind[vibr__radj]))
            agg__ocv, ukow__puih = ListInstance.allocate_ex(context,
                builder, types.List(t), ipvi__thop)
            ukow__puih.size = ipvi__thop
            venbg__pmnq = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(bfur__brayb.block_to_arr_ind
                [vibr__radj], dtype=np.int64))
            eocj__xrz = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, venbg__pmnq)
            with cgutils.for_range(builder, ipvi__thop) as wxff__slxd:
                dtkz__vytut = wxff__slxd.index
                ajvx__xko = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    eocj__xrz, dtkz__vytut)
                vty__uqcr = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, oen__njvqx, ajvx__xko)
                gvkz__dwusa = builder.icmp_unsigned('!=', vty__uqcr, kvzy__yeh)
                with builder.if_else(gvkz__dwusa) as (tzl__lwu, ygir__krdkp):
                    with tzl__lwu:
                        czwqo__nfsq = builder.call(idi__ythj, [uwai__yov,
                            vty__uqcr])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            czwqo__nfsq])
                        ukow__puih.inititem(dtkz__vytut, arr, incref=False)
                        phwhj__kbbf = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(phwhj__kbbf, cqobf__wszyt)
                    with ygir__krdkp:
                        hpqo__rxgvj = context.get_constant_null(t)
                        ukow__puih.inititem(dtkz__vytut, hpqo__rxgvj,
                            incref=False)
            setattr(atc__xypul, f'block_{vibr__radj}', ukow__puih.value)
        atc__xypul.len = builder.load(cqobf__wszyt)
        return atc__xypul._getvalue()
    return bfur__brayb(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    bfur__brayb = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        pgo__hji, agg__ocv = args
        uqam__quf = cgutils.create_struct_proxy(bfur__brayb)(context,
            builder, pgo__hji)
        if bfur__brayb.has_runtime_cols:
            amdou__cmatl = lir.Constant(lir.IntType(64), 0)
            for vibr__radj, t in enumerate(bfur__brayb.arr_types):
                aooo__odfsz = getattr(uqam__quf, f'block_{vibr__radj}')
                hlqgd__feccp = ListInstance(context, builder, types.List(t),
                    aooo__odfsz)
                amdou__cmatl = builder.add(amdou__cmatl, hlqgd__feccp.size)
        else:
            amdou__cmatl = lir.Constant(lir.IntType(64), len(bfur__brayb.
                arr_types))
        agg__ocv, pib__owyq = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), amdou__cmatl)
        pib__owyq.size = amdou__cmatl
        if bfur__brayb.has_runtime_cols:
            sxxg__agdyd = lir.Constant(lir.IntType(64), 0)
            for vibr__radj, t in enumerate(bfur__brayb.arr_types):
                aooo__odfsz = getattr(uqam__quf, f'block_{vibr__radj}')
                hlqgd__feccp = ListInstance(context, builder, types.List(t),
                    aooo__odfsz)
                ipvi__thop = hlqgd__feccp.size
                with cgutils.for_range(builder, ipvi__thop) as wxff__slxd:
                    dtkz__vytut = wxff__slxd.index
                    arr = hlqgd__feccp.getitem(dtkz__vytut)
                    esu__nzso = signature(array_info_type, t)
                    rfep__givz = arr,
                    qelse__ybocg = array_to_info_codegen(context, builder,
                        esu__nzso, rfep__givz)
                    pib__owyq.inititem(builder.add(sxxg__agdyd, dtkz__vytut
                        ), qelse__ybocg, incref=False)
                sxxg__agdyd = builder.add(sxxg__agdyd, ipvi__thop)
        else:
            for t, vibr__radj in bfur__brayb.type_to_blk.items():
                ipvi__thop = context.get_constant(types.int64, len(
                    bfur__brayb.block_to_arr_ind[vibr__radj]))
                aooo__odfsz = getattr(uqam__quf, f'block_{vibr__radj}')
                hlqgd__feccp = ListInstance(context, builder, types.List(t),
                    aooo__odfsz)
                venbg__pmnq = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(bfur__brayb.
                    block_to_arr_ind[vibr__radj], dtype=np.int64))
                eocj__xrz = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, venbg__pmnq)
                with cgutils.for_range(builder, ipvi__thop) as wxff__slxd:
                    dtkz__vytut = wxff__slxd.index
                    ajvx__xko = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        eocj__xrz, dtkz__vytut)
                    wjjh__yik = signature(types.none, bfur__brayb, types.
                        List(t), types.int64, types.int64)
                    zwxjl__nvita = (pgo__hji, aooo__odfsz, dtkz__vytut,
                        ajvx__xko)
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, wjjh__yik, zwxjl__nvita)
                    arr = hlqgd__feccp.getitem(dtkz__vytut)
                    esu__nzso = signature(array_info_type, t)
                    rfep__givz = arr,
                    qelse__ybocg = array_to_info_codegen(context, builder,
                        esu__nzso, rfep__givz)
                    pib__owyq.inititem(ajvx__xko, qelse__ybocg, incref=False)
        mhal__tuj = pib__owyq.value
        fhck__rcsh = signature(table_type, types.List(array_info_type))
        ncf__vmmnm = mhal__tuj,
        uwai__yov = arr_info_list_to_table_codegen(context, builder,
            fhck__rcsh, ncf__vmmnm)
        context.nrt.decref(builder, types.List(array_info_type), mhal__tuj)
        return uwai__yov
    return table_type(bfur__brayb, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='delete_table')
        builder.call(idi__ythj, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='shuffle_table')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        zlpj__qjecv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='delete_shuffle_info')
        return builder.call(idi__ythj, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='reverse_shuffle_table')
        return builder.call(idi__ythj, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    optional_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='hash_join_table')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.boolean, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.int64), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='sort_values_table')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='sample_table')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='shuffle_renormalization')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='shuffle_renormalization_group')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='drop_duplicates_table')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def pivot_groupby_and_aggregate(typingctx, table_t, n_keys_t,
    dispatch_table_t, dispatch_info_t, input_has_index, ftypes,
    func_offsets, udf_n_redvars, is_parallel, is_crosstab, skipdropna_t,
    return_keys, return_index, update_cb, combine_cb, eval_cb,
    udf_table_dummy_t):
    assert table_t == table_type
    assert dispatch_table_t == table_type
    assert dispatch_info_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='pivot_groupby_and_aggregate')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int64, table_t, table_t, types.boolean,
        types.voidptr, types.voidptr, types.voidptr, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, table_t), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb, udf_table_dummy_t
    ):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        idi__ythj = cgutils.get_or_insert_function(builder.module,
            zlpj__qjecv, name='groupby_and_aggregate')
        amrq__glsgh = builder.call(idi__ythj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return amrq__glsgh
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t), codegen


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    kqfb__tso = array_to_info(in_arr)
    roe__ewcyy = array_to_info(in_values)
    lcz__aik = array_to_info(out_arr)
    mvjop__djdd = arr_info_list_to_table([kqfb__tso, roe__ewcyy, lcz__aik])
    _array_isin(lcz__aik, kqfb__tso, roe__ewcyy, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(mvjop__djdd)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    kqfb__tso = array_to_info(in_arr)
    lcz__aik = array_to_info(out_arr)
    _get_search_regex(kqfb__tso, case, pat, lcz__aik)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    advw__qtsv = col_array_typ.dtype
    if isinstance(advw__qtsv, types.Number) or advw__qtsv in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                atc__xypul, lijgw__leasd = args
                atc__xypul = builder.bitcast(atc__xypul, lir.IntType(8).
                    as_pointer().as_pointer())
                fphp__fflbz = lir.Constant(lir.IntType(64), c_ind)
                ike__ljmk = builder.load(builder.gep(atc__xypul, [fphp__fflbz])
                    )
                ike__ljmk = builder.bitcast(ike__ljmk, context.
                    get_data_type(advw__qtsv).as_pointer())
                return builder.load(builder.gep(ike__ljmk, [lijgw__leasd]))
            return advw__qtsv(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                atc__xypul, lijgw__leasd = args
                atc__xypul = builder.bitcast(atc__xypul, lir.IntType(8).
                    as_pointer().as_pointer())
                fphp__fflbz = lir.Constant(lir.IntType(64), c_ind)
                ike__ljmk = builder.load(builder.gep(atc__xypul, [fphp__fflbz])
                    )
                zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                loosa__zun = cgutils.get_or_insert_function(builder.module,
                    zlpj__qjecv, name='array_info_getitem')
                npnhu__eol = cgutils.alloca_once(builder, lir.IntType(64))
                args = ike__ljmk, lijgw__leasd, npnhu__eol
                qxzfy__ximhg = builder.call(loosa__zun, args)
                return context.make_tuple(builder, sig.return_type, [
                    qxzfy__ximhg, builder.load(npnhu__eol)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                wubm__xpi = lir.Constant(lir.IntType(64), 1)
                tqnuk__dtc = lir.Constant(lir.IntType(64), 2)
                atc__xypul, lijgw__leasd = args
                atc__xypul = builder.bitcast(atc__xypul, lir.IntType(8).
                    as_pointer().as_pointer())
                fphp__fflbz = lir.Constant(lir.IntType(64), c_ind)
                ike__ljmk = builder.load(builder.gep(atc__xypul, [fphp__fflbz])
                    )
                zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                thmzf__tosbh = cgutils.get_or_insert_function(builder.
                    module, zlpj__qjecv, name='get_nested_info')
                args = ike__ljmk, tqnuk__dtc
                gskcv__mpg = builder.call(thmzf__tosbh, args)
                zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                zrpo__uqoy = cgutils.get_or_insert_function(builder.module,
                    zlpj__qjecv, name='array_info_getdata1')
                args = gskcv__mpg,
                tusy__dtqfu = builder.call(zrpo__uqoy, args)
                tusy__dtqfu = builder.bitcast(tusy__dtqfu, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                qjgr__tdz = builder.sext(builder.load(builder.gep(
                    tusy__dtqfu, [lijgw__leasd])), lir.IntType(64))
                args = ike__ljmk, wubm__xpi
                wnk__rocsq = builder.call(thmzf__tosbh, args)
                zlpj__qjecv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                loosa__zun = cgutils.get_or_insert_function(builder.module,
                    zlpj__qjecv, name='array_info_getitem')
                npnhu__eol = cgutils.alloca_once(builder, lir.IntType(64))
                args = wnk__rocsq, qjgr__tdz, npnhu__eol
                qxzfy__ximhg = builder.call(loosa__zun, args)
                return context.make_tuple(builder, sig.return_type, [
                    qxzfy__ximhg, builder.load(npnhu__eol)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{advw__qtsv}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                qnwum__gxafv, lijgw__leasd = args
                qnwum__gxafv = builder.bitcast(qnwum__gxafv, lir.IntType(8)
                    .as_pointer().as_pointer())
                fphp__fflbz = lir.Constant(lir.IntType(64), c_ind)
                ike__ljmk = builder.load(builder.gep(qnwum__gxafv, [
                    fphp__fflbz]))
                myy__qiu = builder.bitcast(ike__ljmk, context.get_data_type
                    (types.bool_).as_pointer())
                xrt__ujcog = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    myy__qiu, lijgw__leasd)
                qyj__bba = builder.icmp_unsigned('!=', xrt__ujcog, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(qyj__bba, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        advw__qtsv = col_array_dtype.dtype
        if advw__qtsv in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    atc__xypul, lijgw__leasd = args
                    atc__xypul = builder.bitcast(atc__xypul, lir.IntType(8)
                        .as_pointer().as_pointer())
                    fphp__fflbz = lir.Constant(lir.IntType(64), c_ind)
                    ike__ljmk = builder.load(builder.gep(atc__xypul, [
                        fphp__fflbz]))
                    ike__ljmk = builder.bitcast(ike__ljmk, context.
                        get_data_type(advw__qtsv).as_pointer())
                    dgu__iedi = builder.load(builder.gep(ike__ljmk, [
                        lijgw__leasd]))
                    qyj__bba = builder.icmp_unsigned('!=', dgu__iedi, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(qyj__bba, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(advw__qtsv, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    atc__xypul, lijgw__leasd = args
                    atc__xypul = builder.bitcast(atc__xypul, lir.IntType(8)
                        .as_pointer().as_pointer())
                    fphp__fflbz = lir.Constant(lir.IntType(64), c_ind)
                    ike__ljmk = builder.load(builder.gep(atc__xypul, [
                        fphp__fflbz]))
                    ike__ljmk = builder.bitcast(ike__ljmk, context.
                        get_data_type(advw__qtsv).as_pointer())
                    dgu__iedi = builder.load(builder.gep(ike__ljmk, [
                        lijgw__leasd]))
                    zbzd__zqxob = signature(types.bool_, advw__qtsv)
                    xrt__ujcog = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, zbzd__zqxob, (dgu__iedi,))
                    return builder.not_(builder.sext(xrt__ujcog, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
