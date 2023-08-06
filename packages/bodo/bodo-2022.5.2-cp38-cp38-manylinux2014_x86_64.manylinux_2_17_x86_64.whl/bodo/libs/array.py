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
        nty__jkgs = context.make_helper(builder, arr_type, in_arr)
        in_arr = nty__jkgs.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        fht__pcxl = context.make_helper(builder, arr_type, in_arr)
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='list_string_array_to_info')
        return builder.call(fhi__wwlj, [fht__pcxl.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                mfqlz__ivlaa = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for hza__cartd in arr_typ.data:
                    mfqlz__ivlaa += get_types(hza__cartd)
                return mfqlz__ivlaa
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
            qbddg__exs = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                ipus__gme = context.make_helper(builder, arr_typ, value=arr)
                ztth__max = get_lengths(_get_map_arr_data_type(arr_typ),
                    ipus__gme.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                gerje__opc = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ztth__max = get_lengths(arr_typ.dtype, gerje__opc.data)
                ztth__max = cgutils.pack_array(builder, [gerje__opc.
                    n_arrays] + [builder.extract_value(ztth__max, hbz__qyx) for
                    hbz__qyx in range(ztth__max.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                gerje__opc = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ztth__max = []
                for hbz__qyx, hza__cartd in enumerate(arr_typ.data):
                    ffd__crvqd = get_lengths(hza__cartd, builder.
                        extract_value(gerje__opc.data, hbz__qyx))
                    ztth__max += [builder.extract_value(ffd__crvqd,
                        pxlpc__lcq) for pxlpc__lcq in range(ffd__crvqd.type
                        .count)]
                ztth__max = cgutils.pack_array(builder, [qbddg__exs,
                    context.get_constant(types.int64, -1)] + ztth__max)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                ztth__max = cgutils.pack_array(builder, [qbddg__exs])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return ztth__max

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                ipus__gme = context.make_helper(builder, arr_typ, value=arr)
                dww__kdg = get_buffers(_get_map_arr_data_type(arr_typ),
                    ipus__gme.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                gerje__opc = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                mft__nwpq = get_buffers(arr_typ.dtype, gerje__opc.data)
                eed__pxfq = context.make_array(types.Array(offset_type, 1, 'C')
                    )(context, builder, gerje__opc.offsets)
                drbm__gnfv = builder.bitcast(eed__pxfq.data, lir.IntType(8)
                    .as_pointer())
                exsjg__pul = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, gerje__opc.null_bitmap)
                uuh__tsn = builder.bitcast(exsjg__pul.data, lir.IntType(8).
                    as_pointer())
                dww__kdg = cgutils.pack_array(builder, [drbm__gnfv,
                    uuh__tsn] + [builder.extract_value(mft__nwpq, hbz__qyx) for
                    hbz__qyx in range(mft__nwpq.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                gerje__opc = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                mft__nwpq = []
                for hbz__qyx, hza__cartd in enumerate(arr_typ.data):
                    skn__btmky = get_buffers(hza__cartd, builder.
                        extract_value(gerje__opc.data, hbz__qyx))
                    mft__nwpq += [builder.extract_value(skn__btmky,
                        pxlpc__lcq) for pxlpc__lcq in range(skn__btmky.type
                        .count)]
                exsjg__pul = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, gerje__opc.null_bitmap)
                uuh__tsn = builder.bitcast(exsjg__pul.data, lir.IntType(8).
                    as_pointer())
                dww__kdg = cgutils.pack_array(builder, [uuh__tsn] + mft__nwpq)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                fjco__nvxtd = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    fjco__nvxtd = int128_type
                elif arr_typ == datetime_date_array_type:
                    fjco__nvxtd = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                qir__poftz = context.make_array(types.Array(fjco__nvxtd, 1,
                    'C'))(context, builder, arr.data)
                exsjg__pul = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                turxj__kdsi = builder.bitcast(qir__poftz.data, lir.IntType(
                    8).as_pointer())
                uuh__tsn = builder.bitcast(exsjg__pul.data, lir.IntType(8).
                    as_pointer())
                dww__kdg = cgutils.pack_array(builder, [uuh__tsn, turxj__kdsi])
            elif arr_typ in (string_array_type, binary_array_type):
                gerje__opc = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                jvqj__sjr = context.make_helper(builder, offset_arr_type,
                    gerje__opc.offsets).data
                ncw__ajvx = context.make_helper(builder, char_arr_type,
                    gerje__opc.data).data
                ducba__lclie = context.make_helper(builder,
                    null_bitmap_arr_type, gerje__opc.null_bitmap).data
                dww__kdg = cgutils.pack_array(builder, [builder.bitcast(
                    jvqj__sjr, lir.IntType(8).as_pointer()), builder.
                    bitcast(ducba__lclie, lir.IntType(8).as_pointer()),
                    builder.bitcast(ncw__ajvx, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                turxj__kdsi = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                gfoxl__nfs = lir.Constant(lir.IntType(8).as_pointer(), None)
                dww__kdg = cgutils.pack_array(builder, [gfoxl__nfs,
                    turxj__kdsi])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return dww__kdg

        def get_field_names(arr_typ):
            ogx__bkpp = []
            if isinstance(arr_typ, StructArrayType):
                for blu__mrla, kjo__hnrmt in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    ogx__bkpp.append(blu__mrla)
                    ogx__bkpp += get_field_names(kjo__hnrmt)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ogx__bkpp += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                ogx__bkpp += get_field_names(_get_map_arr_data_type(arr_typ))
            return ogx__bkpp
        mfqlz__ivlaa = get_types(arr_type)
        enopb__qxix = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in mfqlz__ivlaa])
        ukl__xoz = cgutils.alloca_once_value(builder, enopb__qxix)
        ztth__max = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, ztth__max)
        dww__kdg = get_buffers(arr_type, in_arr)
        ggocr__wwur = cgutils.alloca_once_value(builder, dww__kdg)
        ogx__bkpp = get_field_names(arr_type)
        if len(ogx__bkpp) == 0:
            ogx__bkpp = ['irrelevant']
        osz__rpdu = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in ogx__bkpp])
        ydn__wqn = cgutils.alloca_once_value(builder, osz__rpdu)
        if isinstance(arr_type, MapArrayType):
            eimco__kckon = _get_map_arr_data_type(arr_type)
            zicne__zialx = context.make_helper(builder, arr_type, value=in_arr)
            tjn__gbs = zicne__zialx.data
        else:
            eimco__kckon = arr_type
            tjn__gbs = in_arr
        xjfdt__ebkr = context.make_helper(builder, eimco__kckon, tjn__gbs)
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='nested_array_to_info')
        uvbl__bfce = builder.call(fhi__wwlj, [builder.bitcast(ukl__xoz, lir
            .IntType(32).as_pointer()), builder.bitcast(ggocr__wwur, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            ydn__wqn, lir.IntType(8).as_pointer()), xjfdt__ebkr.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
    if arr_type in (string_array_type, binary_array_type):
        qspcf__hxy = context.make_helper(builder, arr_type, in_arr)
        rxibq__axkq = ArrayItemArrayType(char_arr_type)
        fht__pcxl = context.make_helper(builder, rxibq__axkq, qspcf__hxy.data)
        gerje__opc = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        jvqj__sjr = context.make_helper(builder, offset_arr_type,
            gerje__opc.offsets).data
        ncw__ajvx = context.make_helper(builder, char_arr_type, gerje__opc.data
            ).data
        ducba__lclie = context.make_helper(builder, null_bitmap_arr_type,
            gerje__opc.null_bitmap).data
        zoc__coc = builder.zext(builder.load(builder.gep(jvqj__sjr, [
            gerje__opc.n_arrays])), lir.IntType(64))
        cgg__ljb = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='string_array_to_info')
        return builder.call(fhi__wwlj, [gerje__opc.n_arrays, zoc__coc,
            ncw__ajvx, jvqj__sjr, ducba__lclie, fht__pcxl.meminfo, cgg__ljb])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        rnk__tyy = arr.data
        zjef__jlo = arr.indices
        sig = array_info_type(arr_type.data)
        kvc__hgqr = array_to_info_codegen(context, builder, sig, (rnk__tyy,
            ), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        ktqjv__hsd = array_to_info_codegen(context, builder, sig, (
            zjef__jlo,), False)
        ffc__bvh = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, zjef__jlo)
        uuh__tsn = context.make_array(types.Array(types.uint8, 1, 'C'))(context
            , builder, ffc__bvh.null_bitmap).data
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='dict_str_array_to_info')
        jrbsu__zzu = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(fhi__wwlj, [kvc__hgqr, ktqjv__hsd, builder.
            bitcast(uuh__tsn, lir.IntType(8).as_pointer()), jrbsu__zzu])
    mrqrc__elb = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        njqw__yjw = context.compile_internal(builder, lambda a: len(a.dtype
            .categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        fgnrb__rbrxc = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(fgnrb__rbrxc, 1, 'C')
        mrqrc__elb = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if mrqrc__elb:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        qbddg__exs = builder.extract_value(arr.shape, 0)
        pizk__svyxk = arr_type.dtype
        kyhw__kswq = numba_to_c_type(pizk__svyxk)
        fjcgs__okfkb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kyhw__kswq))
        if mrqrc__elb:
            gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            fhi__wwlj = cgutils.get_or_insert_function(builder.module,
                gzmh__rpepn, name='categorical_array_to_info')
            return builder.call(fhi__wwlj, [qbddg__exs, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(
                fjcgs__okfkb), njqw__yjw, arr.meminfo])
        else:
            gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            fhi__wwlj = cgutils.get_or_insert_function(builder.module,
                gzmh__rpepn, name='numpy_array_to_info')
            return builder.call(fhi__wwlj, [qbddg__exs, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(
                fjcgs__okfkb), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        pizk__svyxk = arr_type.dtype
        fjco__nvxtd = pizk__svyxk
        if isinstance(arr_type, DecimalArrayType):
            fjco__nvxtd = int128_type
        if arr_type == datetime_date_array_type:
            fjco__nvxtd = types.int64
        qir__poftz = context.make_array(types.Array(fjco__nvxtd, 1, 'C'))(
            context, builder, arr.data)
        qbddg__exs = builder.extract_value(qir__poftz.shape, 0)
        atp__ojgx = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        kyhw__kswq = numba_to_c_type(pizk__svyxk)
        fjcgs__okfkb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kyhw__kswq))
        if isinstance(arr_type, DecimalArrayType):
            gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            fhi__wwlj = cgutils.get_or_insert_function(builder.module,
                gzmh__rpepn, name='decimal_array_to_info')
            return builder.call(fhi__wwlj, [qbddg__exs, builder.bitcast(
                qir__poftz.data, lir.IntType(8).as_pointer()), builder.load
                (fjcgs__okfkb), builder.bitcast(atp__ojgx.data, lir.IntType
                (8).as_pointer()), qir__poftz.meminfo, atp__ojgx.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        else:
            gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            fhi__wwlj = cgutils.get_or_insert_function(builder.module,
                gzmh__rpepn, name='nullable_array_to_info')
            return builder.call(fhi__wwlj, [qbddg__exs, builder.bitcast(
                qir__poftz.data, lir.IntType(8).as_pointer()), builder.load
                (fjcgs__okfkb), builder.bitcast(atp__ojgx.data, lir.IntType
                (8).as_pointer()), qir__poftz.meminfo, atp__ojgx.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        airl__cue = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        rnc__gnueb = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        qbddg__exs = builder.extract_value(airl__cue.shape, 0)
        kyhw__kswq = numba_to_c_type(arr_type.arr_type.dtype)
        fjcgs__okfkb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kyhw__kswq))
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='interval_array_to_info')
        return builder.call(fhi__wwlj, [qbddg__exs, builder.bitcast(
            airl__cue.data, lir.IntType(8).as_pointer()), builder.bitcast(
            rnc__gnueb.data, lir.IntType(8).as_pointer()), builder.load(
            fjcgs__okfkb), airl__cue.meminfo, rnc__gnueb.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    mciwk__ybdrc = cgutils.alloca_once(builder, lir.IntType(64))
    turxj__kdsi = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    yhcxm__dcd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    fhi__wwlj = cgutils.get_or_insert_function(builder.module, gzmh__rpepn,
        name='info_to_numpy_array')
    builder.call(fhi__wwlj, [in_info, mciwk__ybdrc, turxj__kdsi, yhcxm__dcd])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    fbigk__aema = context.get_value_type(types.intp)
    xyz__idrqj = cgutils.pack_array(builder, [builder.load(mciwk__ybdrc)],
        ty=fbigk__aema)
    pplv__tbxyc = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    xzqbj__ubl = cgutils.pack_array(builder, [pplv__tbxyc], ty=fbigk__aema)
    ncw__ajvx = builder.bitcast(builder.load(turxj__kdsi), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=ncw__ajvx, shape=xyz__idrqj,
        strides=xzqbj__ubl, itemsize=pplv__tbxyc, meminfo=builder.load(
        yhcxm__dcd))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    bxsbt__nei = context.make_helper(builder, arr_type)
    gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    fhi__wwlj = cgutils.get_or_insert_function(builder.module, gzmh__rpepn,
        name='info_to_list_string_array')
    builder.call(fhi__wwlj, [in_info, bxsbt__nei._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return bxsbt__nei._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    mzzc__obzy = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        vfm__mca = lengths_pos
        xacwp__bieyu = infos_pos
        qwra__naky, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        xvbi__ryww = ArrayItemArrayPayloadType(arr_typ)
        wvdvi__zmu = context.get_data_type(xvbi__ryww)
        xac__hep = context.get_abi_sizeof(wvdvi__zmu)
        njy__vovf = define_array_item_dtor(context, builder, arr_typ,
            xvbi__ryww)
        tanc__rml = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, xac__hep), njy__vovf)
        lbor__vudm = context.nrt.meminfo_data(builder, tanc__rml)
        bmzr__usuyc = builder.bitcast(lbor__vudm, wvdvi__zmu.as_pointer())
        gerje__opc = cgutils.create_struct_proxy(xvbi__ryww)(context, builder)
        gerje__opc.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), vfm__mca)
        gerje__opc.data = qwra__naky
        iqqel__tggp = builder.load(array_infos_ptr)
        efx__owzpc = builder.bitcast(builder.extract_value(iqqel__tggp,
            xacwp__bieyu), mzzc__obzy)
        gerje__opc.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, efx__owzpc)
        rnoee__ybz = builder.bitcast(builder.extract_value(iqqel__tggp, 
            xacwp__bieyu + 1), mzzc__obzy)
        gerje__opc.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, rnoee__ybz)
        builder.store(gerje__opc._getvalue(), bmzr__usuyc)
        fht__pcxl = context.make_helper(builder, arr_typ)
        fht__pcxl.meminfo = tanc__rml
        return fht__pcxl._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        xiy__wzozg = []
        xacwp__bieyu = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for rllv__szr in arr_typ.data:
            qwra__naky, lengths_pos, infos_pos = nested_to_array(context,
                builder, rllv__szr, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            xiy__wzozg.append(qwra__naky)
        xvbi__ryww = StructArrayPayloadType(arr_typ.data)
        wvdvi__zmu = context.get_value_type(xvbi__ryww)
        xac__hep = context.get_abi_sizeof(wvdvi__zmu)
        njy__vovf = define_struct_arr_dtor(context, builder, arr_typ,
            xvbi__ryww)
        tanc__rml = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, xac__hep), njy__vovf)
        lbor__vudm = context.nrt.meminfo_data(builder, tanc__rml)
        bmzr__usuyc = builder.bitcast(lbor__vudm, wvdvi__zmu.as_pointer())
        gerje__opc = cgutils.create_struct_proxy(xvbi__ryww)(context, builder)
        gerje__opc.data = cgutils.pack_array(builder, xiy__wzozg
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, xiy__wzozg)
        iqqel__tggp = builder.load(array_infos_ptr)
        rnoee__ybz = builder.bitcast(builder.extract_value(iqqel__tggp,
            xacwp__bieyu), mzzc__obzy)
        gerje__opc.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, rnoee__ybz)
        builder.store(gerje__opc._getvalue(), bmzr__usuyc)
        zoe__qsxai = context.make_helper(builder, arr_typ)
        zoe__qsxai.meminfo = tanc__rml
        return zoe__qsxai._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        iqqel__tggp = builder.load(array_infos_ptr)
        tsxhh__dpkx = builder.bitcast(builder.extract_value(iqqel__tggp,
            infos_pos), mzzc__obzy)
        qspcf__hxy = context.make_helper(builder, arr_typ)
        rxibq__axkq = ArrayItemArrayType(char_arr_type)
        fht__pcxl = context.make_helper(builder, rxibq__axkq)
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_to_string_array')
        builder.call(fhi__wwlj, [tsxhh__dpkx, fht__pcxl._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qspcf__hxy.data = fht__pcxl._getvalue()
        return qspcf__hxy._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        iqqel__tggp = builder.load(array_infos_ptr)
        ideq__slk = builder.bitcast(builder.extract_value(iqqel__tggp, 
            infos_pos + 1), mzzc__obzy)
        return _lower_info_to_array_numpy(arr_typ, context, builder, ideq__slk
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        fjco__nvxtd = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            fjco__nvxtd = int128_type
        elif arr_typ == datetime_date_array_type:
            fjco__nvxtd = types.int64
        iqqel__tggp = builder.load(array_infos_ptr)
        rnoee__ybz = builder.bitcast(builder.extract_value(iqqel__tggp,
            infos_pos), mzzc__obzy)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, rnoee__ybz)
        ideq__slk = builder.bitcast(builder.extract_value(iqqel__tggp, 
            infos_pos + 1), mzzc__obzy)
        arr.data = _lower_info_to_array_numpy(types.Array(fjco__nvxtd, 1,
            'C'), context, builder, ideq__slk)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, nmxq__sigz = args
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
                return 1 + sum([get_num_arrays(rllv__szr) for rllv__szr in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(rllv__szr) for rllv__szr in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            ckuhe__msvc = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            ckuhe__msvc = _get_map_arr_data_type(arr_type)
        else:
            ckuhe__msvc = arr_type
        mggok__khbds = get_num_arrays(ckuhe__msvc)
        ztth__max = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for nmxq__sigz in range(mggok__khbds)])
        lengths_ptr = cgutils.alloca_once_value(builder, ztth__max)
        gfoxl__nfs = lir.Constant(lir.IntType(8).as_pointer(), None)
        zshtb__nzj = cgutils.pack_array(builder, [gfoxl__nfs for nmxq__sigz in
            range(get_num_infos(ckuhe__msvc))])
        array_infos_ptr = cgutils.alloca_once_value(builder, zshtb__nzj)
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_to_nested_array')
        builder.call(fhi__wwlj, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, nmxq__sigz, nmxq__sigz = nested_to_array(context, builder,
            ckuhe__msvc, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            nty__jkgs = context.make_helper(builder, arr_type)
            nty__jkgs.data = arr
            context.nrt.incref(builder, ckuhe__msvc, arr)
            arr = nty__jkgs._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, ckuhe__msvc)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        qspcf__hxy = context.make_helper(builder, arr_type)
        rxibq__axkq = ArrayItemArrayType(char_arr_type)
        fht__pcxl = context.make_helper(builder, rxibq__axkq)
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_to_string_array')
        builder.call(fhi__wwlj, [in_info, fht__pcxl._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qspcf__hxy.data = fht__pcxl._getvalue()
        return qspcf__hxy._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='get_nested_info')
        kvc__hgqr = builder.call(fhi__wwlj, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        ktqjv__hsd = builder.call(fhi__wwlj, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        jtrpr__dbcdp = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        jtrpr__dbcdp.data = info_to_array_codegen(context, builder, sig, (
            kvc__hgqr, context.get_constant_null(arr_type.data)))
        dlzix__iyhxy = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = dlzix__iyhxy(array_info_type, dlzix__iyhxy)
        jtrpr__dbcdp.indices = info_to_array_codegen(context, builder, sig,
            (ktqjv__hsd, context.get_constant_null(dlzix__iyhxy)))
        gzmh__rpepn = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='get_has_global_dictionary')
        jrbsu__zzu = builder.call(fhi__wwlj, [in_info])
        jtrpr__dbcdp.has_global_dictionary = builder.trunc(jrbsu__zzu,
            cgutils.bool_t)
        return jtrpr__dbcdp._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        fgnrb__rbrxc = get_categories_int_type(arr_type.dtype)
        slci__mhxoj = types.Array(fgnrb__rbrxc, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(slci__mhxoj, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            zjpb__imcis = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(zjpb__imcis))
            int_type = arr_type.dtype.int_type
            pril__bduuy = bodo.typeof(zjpb__imcis)
            monnz__mjneq = context.get_constant_generic(builder,
                pril__bduuy, zjpb__imcis)
            pizk__svyxk = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(pril__bduuy), [monnz__mjneq])
        else:
            pizk__svyxk = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, pizk__svyxk)
        out_arr.dtype = pizk__svyxk
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        ncw__ajvx = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = ncw__ajvx
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        fjco__nvxtd = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            fjco__nvxtd = int128_type
        elif arr_type == datetime_date_array_type:
            fjco__nvxtd = types.int64
        pxwul__flpn = types.Array(fjco__nvxtd, 1, 'C')
        qir__poftz = context.make_array(pxwul__flpn)(context, builder)
        xbvv__kwlmh = types.Array(types.uint8, 1, 'C')
        ewa__qobti = context.make_array(xbvv__kwlmh)(context, builder)
        mciwk__ybdrc = cgutils.alloca_once(builder, lir.IntType(64))
        jte__lvmj = cgutils.alloca_once(builder, lir.IntType(64))
        turxj__kdsi = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        czhs__mph = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        yhcxm__dcd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        pisku__ilf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_to_nullable_array')
        builder.call(fhi__wwlj, [in_info, mciwk__ybdrc, jte__lvmj,
            turxj__kdsi, czhs__mph, yhcxm__dcd, pisku__ilf])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        fbigk__aema = context.get_value_type(types.intp)
        xyz__idrqj = cgutils.pack_array(builder, [builder.load(mciwk__ybdrc
            )], ty=fbigk__aema)
        pplv__tbxyc = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(fjco__nvxtd)))
        xzqbj__ubl = cgutils.pack_array(builder, [pplv__tbxyc], ty=fbigk__aema)
        ncw__ajvx = builder.bitcast(builder.load(turxj__kdsi), context.
            get_data_type(fjco__nvxtd).as_pointer())
        numba.np.arrayobj.populate_array(qir__poftz, data=ncw__ajvx, shape=
            xyz__idrqj, strides=xzqbj__ubl, itemsize=pplv__tbxyc, meminfo=
            builder.load(yhcxm__dcd))
        arr.data = qir__poftz._getvalue()
        xyz__idrqj = cgutils.pack_array(builder, [builder.load(jte__lvmj)],
            ty=fbigk__aema)
        pplv__tbxyc = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        xzqbj__ubl = cgutils.pack_array(builder, [pplv__tbxyc], ty=fbigk__aema)
        ncw__ajvx = builder.bitcast(builder.load(czhs__mph), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(ewa__qobti, data=ncw__ajvx, shape=
            xyz__idrqj, strides=xzqbj__ubl, itemsize=pplv__tbxyc, meminfo=
            builder.load(pisku__ilf))
        arr.null_bitmap = ewa__qobti._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        airl__cue = context.make_array(arr_type.arr_type)(context, builder)
        rnc__gnueb = context.make_array(arr_type.arr_type)(context, builder)
        mciwk__ybdrc = cgutils.alloca_once(builder, lir.IntType(64))
        kgs__nazp = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zmpn__xodpf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        jzwp__vwvvy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zfv__lxg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_to_interval_array')
        builder.call(fhi__wwlj, [in_info, mciwk__ybdrc, kgs__nazp,
            zmpn__xodpf, jzwp__vwvvy, zfv__lxg])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        fbigk__aema = context.get_value_type(types.intp)
        xyz__idrqj = cgutils.pack_array(builder, [builder.load(mciwk__ybdrc
            )], ty=fbigk__aema)
        pplv__tbxyc = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        xzqbj__ubl = cgutils.pack_array(builder, [pplv__tbxyc], ty=fbigk__aema)
        cbwe__bijme = builder.bitcast(builder.load(kgs__nazp), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(airl__cue, data=cbwe__bijme, shape
            =xyz__idrqj, strides=xzqbj__ubl, itemsize=pplv__tbxyc, meminfo=
            builder.load(jzwp__vwvvy))
        arr.left = airl__cue._getvalue()
        gmay__zadre = builder.bitcast(builder.load(zmpn__xodpf), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(rnc__gnueb, data=gmay__zadre,
            shape=xyz__idrqj, strides=xzqbj__ubl, itemsize=pplv__tbxyc,
            meminfo=builder.load(zfv__lxg))
        arr.right = rnc__gnueb._getvalue()
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
        qbddg__exs, nmxq__sigz = args
        kyhw__kswq = numba_to_c_type(array_type.dtype)
        fjcgs__okfkb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kyhw__kswq))
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='alloc_numpy')
        return builder.call(fhi__wwlj, [qbddg__exs, builder.load(fjcgs__okfkb)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        qbddg__exs, vokdq__wnb = args
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='alloc_string_array')
        return builder.call(fhi__wwlj, [qbddg__exs, vokdq__wnb])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    vauqh__sicu, = args
    whgi__svu = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], vauqh__sicu)
    gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    fhi__wwlj = cgutils.get_or_insert_function(builder.module, gzmh__rpepn,
        name='arr_info_list_to_table')
    return builder.call(fhi__wwlj, [whgi__svu.data, whgi__svu.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_from_table')
        return builder.call(fhi__wwlj, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    dyxbw__zns = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        mgl__meqnk, jrvew__begyv, nmxq__sigz = args
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='info_from_table')
        bbu__vjr = cgutils.create_struct_proxy(dyxbw__zns)(context, builder)
        bbu__vjr.parent = cgutils.get_null_value(bbu__vjr.parent.type)
        jjxr__jijah = context.make_array(table_idx_arr_t)(context, builder,
            jrvew__begyv)
        gyc__zaqp = context.get_constant(types.int64, -1)
        aatye__mazvt = context.get_constant(types.int64, 0)
        tcdxx__lwmu = cgutils.alloca_once_value(builder, aatye__mazvt)
        for t, umlef__ceww in dyxbw__zns.type_to_blk.items():
            bhfxn__ligen = context.get_constant(types.int64, len(dyxbw__zns
                .block_to_arr_ind[umlef__ceww]))
            nmxq__sigz, tht__gqc = ListInstance.allocate_ex(context,
                builder, types.List(t), bhfxn__ligen)
            tht__gqc.size = bhfxn__ligen
            uaptm__fzaam = context.make_constant_array(builder, types.Array
                (types.int64, 1, 'C'), np.array(dyxbw__zns.block_to_arr_ind
                [umlef__ceww], dtype=np.int64))
            ikg__ymzg = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, uaptm__fzaam)
            with cgutils.for_range(builder, bhfxn__ligen) as lvybl__fmyxh:
                hbz__qyx = lvybl__fmyxh.index
                lscj__rysh = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    ikg__ymzg, hbz__qyx)
                fjbc__wncs = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, jjxr__jijah, lscj__rysh)
                dtg__mqerw = builder.icmp_unsigned('!=', fjbc__wncs, gyc__zaqp)
                with builder.if_else(dtg__mqerw) as (paw__vqm, oaujv__aglg):
                    with paw__vqm:
                        qusml__bfte = builder.call(fhi__wwlj, [mgl__meqnk,
                            fjbc__wncs])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            qusml__bfte])
                        tht__gqc.inititem(hbz__qyx, arr, incref=False)
                        qbddg__exs = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(qbddg__exs, tcdxx__lwmu)
                    with oaujv__aglg:
                        aanr__bijs = context.get_constant_null(t)
                        tht__gqc.inititem(hbz__qyx, aanr__bijs, incref=False)
            setattr(bbu__vjr, f'block_{umlef__ceww}', tht__gqc.value)
        bbu__vjr.len = builder.load(tcdxx__lwmu)
        return bbu__vjr._getvalue()
    return dyxbw__zns(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    dyxbw__zns = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        xypj__clbf, nmxq__sigz = args
        xau__dzawg = cgutils.create_struct_proxy(dyxbw__zns)(context,
            builder, xypj__clbf)
        if dyxbw__zns.has_runtime_cols:
            lcik__rnhsa = lir.Constant(lir.IntType(64), 0)
            for umlef__ceww, t in enumerate(dyxbw__zns.arr_types):
                jwqxf__oqzdt = getattr(xau__dzawg, f'block_{umlef__ceww}')
                hmgd__vfb = ListInstance(context, builder, types.List(t),
                    jwqxf__oqzdt)
                lcik__rnhsa = builder.add(lcik__rnhsa, hmgd__vfb.size)
        else:
            lcik__rnhsa = lir.Constant(lir.IntType(64), len(dyxbw__zns.
                arr_types))
        nmxq__sigz, kmayr__srfnz = ListInstance.allocate_ex(context,
            builder, types.List(array_info_type), lcik__rnhsa)
        kmayr__srfnz.size = lcik__rnhsa
        if dyxbw__zns.has_runtime_cols:
            cdpoo__rij = lir.Constant(lir.IntType(64), 0)
            for umlef__ceww, t in enumerate(dyxbw__zns.arr_types):
                jwqxf__oqzdt = getattr(xau__dzawg, f'block_{umlef__ceww}')
                hmgd__vfb = ListInstance(context, builder, types.List(t),
                    jwqxf__oqzdt)
                bhfxn__ligen = hmgd__vfb.size
                with cgutils.for_range(builder, bhfxn__ligen) as lvybl__fmyxh:
                    hbz__qyx = lvybl__fmyxh.index
                    arr = hmgd__vfb.getitem(hbz__qyx)
                    hjtl__ddedf = signature(array_info_type, t)
                    ftpqa__ztu = arr,
                    njx__kkax = array_to_info_codegen(context, builder,
                        hjtl__ddedf, ftpqa__ztu)
                    kmayr__srfnz.inititem(builder.add(cdpoo__rij, hbz__qyx),
                        njx__kkax, incref=False)
                cdpoo__rij = builder.add(cdpoo__rij, bhfxn__ligen)
        else:
            for t, umlef__ceww in dyxbw__zns.type_to_blk.items():
                bhfxn__ligen = context.get_constant(types.int64, len(
                    dyxbw__zns.block_to_arr_ind[umlef__ceww]))
                jwqxf__oqzdt = getattr(xau__dzawg, f'block_{umlef__ceww}')
                hmgd__vfb = ListInstance(context, builder, types.List(t),
                    jwqxf__oqzdt)
                uaptm__fzaam = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(dyxbw__zns.
                    block_to_arr_ind[umlef__ceww], dtype=np.int64))
                ikg__ymzg = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, uaptm__fzaam)
                with cgutils.for_range(builder, bhfxn__ligen) as lvybl__fmyxh:
                    hbz__qyx = lvybl__fmyxh.index
                    lscj__rysh = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        ikg__ymzg, hbz__qyx)
                    qvo__wjgll = signature(types.none, dyxbw__zns, types.
                        List(t), types.int64, types.int64)
                    yldmz__dvm = xypj__clbf, jwqxf__oqzdt, hbz__qyx, lscj__rysh
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, qvo__wjgll, yldmz__dvm)
                    arr = hmgd__vfb.getitem(hbz__qyx)
                    hjtl__ddedf = signature(array_info_type, t)
                    ftpqa__ztu = arr,
                    njx__kkax = array_to_info_codegen(context, builder,
                        hjtl__ddedf, ftpqa__ztu)
                    kmayr__srfnz.inititem(lscj__rysh, njx__kkax, incref=False)
        lroy__gbkbi = kmayr__srfnz.value
        fxe__dicjo = signature(table_type, types.List(array_info_type))
        hem__mfhlb = lroy__gbkbi,
        mgl__meqnk = arr_info_list_to_table_codegen(context, builder,
            fxe__dicjo, hem__mfhlb)
        context.nrt.decref(builder, types.List(array_info_type), lroy__gbkbi)
        return mgl__meqnk
    return table_type(dyxbw__zns, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='delete_table')
        builder.call(fhi__wwlj, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='shuffle_table')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
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
        gzmh__rpepn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='delete_shuffle_info')
        return builder.call(fhi__wwlj, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='reverse_shuffle_table')
        return builder.call(fhi__wwlj, args)
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
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='hash_join_table')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
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
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='sort_values_table')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='sample_table')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='shuffle_renormalization')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='shuffle_renormalization_group')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='drop_duplicates_table')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
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
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='pivot_groupby_and_aggregate')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
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
        gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        fhi__wwlj = cgutils.get_or_insert_function(builder.module,
            gzmh__rpepn, name='groupby_and_aggregate')
        uvbl__bfce = builder.call(fhi__wwlj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return uvbl__bfce
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
    igex__htm = array_to_info(in_arr)
    dufdq__znof = array_to_info(in_values)
    gyip__rrfai = array_to_info(out_arr)
    kdtv__ekdg = arr_info_list_to_table([igex__htm, dufdq__znof, gyip__rrfai])
    _array_isin(gyip__rrfai, igex__htm, dufdq__znof, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(kdtv__ekdg)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    igex__htm = array_to_info(in_arr)
    gyip__rrfai = array_to_info(out_arr)
    _get_search_regex(igex__htm, case, pat, gyip__rrfai)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    hdb__twh = col_array_typ.dtype
    if isinstance(hdb__twh, types.Number) or hdb__twh in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bbu__vjr, kxuvg__ccgjo = args
                bbu__vjr = builder.bitcast(bbu__vjr, lir.IntType(8).
                    as_pointer().as_pointer())
                zkpvz__bvg = lir.Constant(lir.IntType(64), c_ind)
                bdps__bkqx = builder.load(builder.gep(bbu__vjr, [zkpvz__bvg]))
                bdps__bkqx = builder.bitcast(bdps__bkqx, context.
                    get_data_type(hdb__twh).as_pointer())
                return builder.load(builder.gep(bdps__bkqx, [kxuvg__ccgjo]))
            return hdb__twh(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bbu__vjr, kxuvg__ccgjo = args
                bbu__vjr = builder.bitcast(bbu__vjr, lir.IntType(8).
                    as_pointer().as_pointer())
                zkpvz__bvg = lir.Constant(lir.IntType(64), c_ind)
                bdps__bkqx = builder.load(builder.gep(bbu__vjr, [zkpvz__bvg]))
                gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                opw__sfb = cgutils.get_or_insert_function(builder.module,
                    gzmh__rpepn, name='array_info_getitem')
                qxwd__vssf = cgutils.alloca_once(builder, lir.IntType(64))
                args = bdps__bkqx, kxuvg__ccgjo, qxwd__vssf
                turxj__kdsi = builder.call(opw__sfb, args)
                return context.make_tuple(builder, sig.return_type, [
                    turxj__kdsi, builder.load(qxwd__vssf)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bhbt__hwv = lir.Constant(lir.IntType(64), 1)
                vqev__qfmba = lir.Constant(lir.IntType(64), 2)
                bbu__vjr, kxuvg__ccgjo = args
                bbu__vjr = builder.bitcast(bbu__vjr, lir.IntType(8).
                    as_pointer().as_pointer())
                zkpvz__bvg = lir.Constant(lir.IntType(64), c_ind)
                bdps__bkqx = builder.load(builder.gep(bbu__vjr, [zkpvz__bvg]))
                gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                tnht__buqoj = cgutils.get_or_insert_function(builder.module,
                    gzmh__rpepn, name='get_nested_info')
                args = bdps__bkqx, vqev__qfmba
                xcil__hbxcj = builder.call(tnht__buqoj, args)
                gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                iak__gnlm = cgutils.get_or_insert_function(builder.module,
                    gzmh__rpepn, name='array_info_getdata1')
                args = xcil__hbxcj,
                xujoz__twrns = builder.call(iak__gnlm, args)
                xujoz__twrns = builder.bitcast(xujoz__twrns, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                avh__vqkbw = builder.sext(builder.load(builder.gep(
                    xujoz__twrns, [kxuvg__ccgjo])), lir.IntType(64))
                args = bdps__bkqx, bhbt__hwv
                jmfhn__otju = builder.call(tnht__buqoj, args)
                gzmh__rpepn = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                opw__sfb = cgutils.get_or_insert_function(builder.module,
                    gzmh__rpepn, name='array_info_getitem')
                qxwd__vssf = cgutils.alloca_once(builder, lir.IntType(64))
                args = jmfhn__otju, avh__vqkbw, qxwd__vssf
                turxj__kdsi = builder.call(opw__sfb, args)
                return context.make_tuple(builder, sig.return_type, [
                    turxj__kdsi, builder.load(qxwd__vssf)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{hdb__twh}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                szgcf__admv, kxuvg__ccgjo = args
                szgcf__admv = builder.bitcast(szgcf__admv, lir.IntType(8).
                    as_pointer().as_pointer())
                zkpvz__bvg = lir.Constant(lir.IntType(64), c_ind)
                bdps__bkqx = builder.load(builder.gep(szgcf__admv, [
                    zkpvz__bvg]))
                ducba__lclie = builder.bitcast(bdps__bkqx, context.
                    get_data_type(types.bool_).as_pointer())
                mfd__osu = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ducba__lclie, kxuvg__ccgjo)
                dexk__vwa = builder.icmp_unsigned('!=', mfd__osu, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(dexk__vwa, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        hdb__twh = col_array_dtype.dtype
        if hdb__twh in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    bbu__vjr, kxuvg__ccgjo = args
                    bbu__vjr = builder.bitcast(bbu__vjr, lir.IntType(8).
                        as_pointer().as_pointer())
                    zkpvz__bvg = lir.Constant(lir.IntType(64), c_ind)
                    bdps__bkqx = builder.load(builder.gep(bbu__vjr, [
                        zkpvz__bvg]))
                    bdps__bkqx = builder.bitcast(bdps__bkqx, context.
                        get_data_type(hdb__twh).as_pointer())
                    fufc__mgq = builder.load(builder.gep(bdps__bkqx, [
                        kxuvg__ccgjo]))
                    dexk__vwa = builder.icmp_unsigned('!=', fufc__mgq, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(dexk__vwa, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(hdb__twh, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    bbu__vjr, kxuvg__ccgjo = args
                    bbu__vjr = builder.bitcast(bbu__vjr, lir.IntType(8).
                        as_pointer().as_pointer())
                    zkpvz__bvg = lir.Constant(lir.IntType(64), c_ind)
                    bdps__bkqx = builder.load(builder.gep(bbu__vjr, [
                        zkpvz__bvg]))
                    bdps__bkqx = builder.bitcast(bdps__bkqx, context.
                        get_data_type(hdb__twh).as_pointer())
                    fufc__mgq = builder.load(builder.gep(bdps__bkqx, [
                        kxuvg__ccgjo]))
                    wdkuu__rfv = signature(types.bool_, hdb__twh)
                    mfd__osu = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, wdkuu__rfv, (fufc__mgq,))
                    return builder.not_(builder.sext(mfd__osu, lir.IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
