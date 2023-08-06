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
        mfn__kncoo = context.make_helper(builder, arr_type, in_arr)
        in_arr = mfn__kncoo.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        mrd__ibm = context.make_helper(builder, arr_type, in_arr)
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='list_string_array_to_info')
        return builder.call(tidqg__yiaeh, [mrd__ibm.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                grjch__ygmp = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for ejnq__hci in arr_typ.data:
                    grjch__ygmp += get_types(ejnq__hci)
                return grjch__ygmp
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
            yfqxa__irlo = context.compile_internal(builder, lambda a: len(a
                ), types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                pyrxx__egq = context.make_helper(builder, arr_typ, value=arr)
                yqv__npbx = get_lengths(_get_map_arr_data_type(arr_typ),
                    pyrxx__egq.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                sgczw__nrngj = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                yqv__npbx = get_lengths(arr_typ.dtype, sgczw__nrngj.data)
                yqv__npbx = cgutils.pack_array(builder, [sgczw__nrngj.
                    n_arrays] + [builder.extract_value(yqv__npbx,
                    prdb__osjt) for prdb__osjt in range(yqv__npbx.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                sgczw__nrngj = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                yqv__npbx = []
                for prdb__osjt, ejnq__hci in enumerate(arr_typ.data):
                    hmkv__vxxm = get_lengths(ejnq__hci, builder.
                        extract_value(sgczw__nrngj.data, prdb__osjt))
                    yqv__npbx += [builder.extract_value(hmkv__vxxm,
                        cflfs__eax) for cflfs__eax in range(hmkv__vxxm.type
                        .count)]
                yqv__npbx = cgutils.pack_array(builder, [yfqxa__irlo,
                    context.get_constant(types.int64, -1)] + yqv__npbx)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                yqv__npbx = cgutils.pack_array(builder, [yfqxa__irlo])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return yqv__npbx

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                pyrxx__egq = context.make_helper(builder, arr_typ, value=arr)
                kekq__fsc = get_buffers(_get_map_arr_data_type(arr_typ),
                    pyrxx__egq.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                sgczw__nrngj = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                zfx__ozf = get_buffers(arr_typ.dtype, sgczw__nrngj.data)
                agwr__zvcd = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, sgczw__nrngj.offsets)
                kdxnh__huf = builder.bitcast(agwr__zvcd.data, lir.IntType(8
                    ).as_pointer())
                yvch__ylnr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, sgczw__nrngj.null_bitmap)
                msujg__anzai = builder.bitcast(yvch__ylnr.data, lir.IntType
                    (8).as_pointer())
                kekq__fsc = cgutils.pack_array(builder, [kdxnh__huf,
                    msujg__anzai] + [builder.extract_value(zfx__ozf,
                    prdb__osjt) for prdb__osjt in range(zfx__ozf.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                sgczw__nrngj = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                zfx__ozf = []
                for prdb__osjt, ejnq__hci in enumerate(arr_typ.data):
                    wkw__gsgob = get_buffers(ejnq__hci, builder.
                        extract_value(sgczw__nrngj.data, prdb__osjt))
                    zfx__ozf += [builder.extract_value(wkw__gsgob,
                        cflfs__eax) for cflfs__eax in range(wkw__gsgob.type
                        .count)]
                yvch__ylnr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, sgczw__nrngj.null_bitmap)
                msujg__anzai = builder.bitcast(yvch__ylnr.data, lir.IntType
                    (8).as_pointer())
                kekq__fsc = cgutils.pack_array(builder, [msujg__anzai] +
                    zfx__ozf)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                ymc__igzgr = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    ymc__igzgr = int128_type
                elif arr_typ == datetime_date_array_type:
                    ymc__igzgr = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                azkdb__kpxsc = context.make_array(types.Array(ymc__igzgr, 1,
                    'C'))(context, builder, arr.data)
                yvch__ylnr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                aqe__tah = builder.bitcast(azkdb__kpxsc.data, lir.IntType(8
                    ).as_pointer())
                msujg__anzai = builder.bitcast(yvch__ylnr.data, lir.IntType
                    (8).as_pointer())
                kekq__fsc = cgutils.pack_array(builder, [msujg__anzai,
                    aqe__tah])
            elif arr_typ in (string_array_type, binary_array_type):
                sgczw__nrngj = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                pbchd__yohd = context.make_helper(builder, offset_arr_type,
                    sgczw__nrngj.offsets).data
                aur__bzoqb = context.make_helper(builder, char_arr_type,
                    sgczw__nrngj.data).data
                rhj__cksth = context.make_helper(builder,
                    null_bitmap_arr_type, sgczw__nrngj.null_bitmap).data
                kekq__fsc = cgutils.pack_array(builder, [builder.bitcast(
                    pbchd__yohd, lir.IntType(8).as_pointer()), builder.
                    bitcast(rhj__cksth, lir.IntType(8).as_pointer()),
                    builder.bitcast(aur__bzoqb, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                aqe__tah = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                vtxf__htji = lir.Constant(lir.IntType(8).as_pointer(), None)
                kekq__fsc = cgutils.pack_array(builder, [vtxf__htji, aqe__tah])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return kekq__fsc

        def get_field_names(arr_typ):
            blov__rxsc = []
            if isinstance(arr_typ, StructArrayType):
                for zoe__owsf, ues__hql in zip(arr_typ.dtype.names, arr_typ
                    .data):
                    blov__rxsc.append(zoe__owsf)
                    blov__rxsc += get_field_names(ues__hql)
            elif isinstance(arr_typ, ArrayItemArrayType):
                blov__rxsc += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                blov__rxsc += get_field_names(_get_map_arr_data_type(arr_typ))
            return blov__rxsc
        grjch__ygmp = get_types(arr_type)
        bqtfx__yrua = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in grjch__ygmp])
        ckk__kfzs = cgutils.alloca_once_value(builder, bqtfx__yrua)
        yqv__npbx = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, yqv__npbx)
        kekq__fsc = get_buffers(arr_type, in_arr)
        lml__cqnoc = cgutils.alloca_once_value(builder, kekq__fsc)
        blov__rxsc = get_field_names(arr_type)
        if len(blov__rxsc) == 0:
            blov__rxsc = ['irrelevant']
        dpg__pre = cgutils.pack_array(builder, [context.insert_const_string
            (builder.module, a) for a in blov__rxsc])
        ava__wsbft = cgutils.alloca_once_value(builder, dpg__pre)
        if isinstance(arr_type, MapArrayType):
            qrp__koq = _get_map_arr_data_type(arr_type)
            olykb__mrqeg = context.make_helper(builder, arr_type, value=in_arr)
            nui__lhofl = olykb__mrqeg.data
        else:
            qrp__koq = arr_type
            nui__lhofl = in_arr
        gsdaj__idojf = context.make_helper(builder, qrp__koq, nui__lhofl)
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='nested_array_to_info')
        xrvgh__kde = builder.call(tidqg__yiaeh, [builder.bitcast(ckk__kfzs,
            lir.IntType(32).as_pointer()), builder.bitcast(lml__cqnoc, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            ava__wsbft, lir.IntType(8).as_pointer()), gsdaj__idojf.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
    if arr_type in (string_array_type, binary_array_type):
        bou__oqvde = context.make_helper(builder, arr_type, in_arr)
        yttk__hbfp = ArrayItemArrayType(char_arr_type)
        mrd__ibm = context.make_helper(builder, yttk__hbfp, bou__oqvde.data)
        sgczw__nrngj = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        pbchd__yohd = context.make_helper(builder, offset_arr_type,
            sgczw__nrngj.offsets).data
        aur__bzoqb = context.make_helper(builder, char_arr_type,
            sgczw__nrngj.data).data
        rhj__cksth = context.make_helper(builder, null_bitmap_arr_type,
            sgczw__nrngj.null_bitmap).data
        ugpx__xysm = builder.zext(builder.load(builder.gep(pbchd__yohd, [
            sgczw__nrngj.n_arrays])), lir.IntType(64))
        hmhe__hfeyx = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='string_array_to_info')
        return builder.call(tidqg__yiaeh, [sgczw__nrngj.n_arrays,
            ugpx__xysm, aur__bzoqb, pbchd__yohd, rhj__cksth, mrd__ibm.
            meminfo, hmhe__hfeyx])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        nabn__ocbac = arr.data
        khkl__dayl = arr.indices
        sig = array_info_type(arr_type.data)
        narcg__wxy = array_to_info_codegen(context, builder, sig, (
            nabn__ocbac,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        ngwk__hebdx = array_to_info_codegen(context, builder, sig, (
            khkl__dayl,), False)
        iccy__mszk = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, khkl__dayl)
        msujg__anzai = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, iccy__mszk.null_bitmap).data
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='dict_str_array_to_info')
        kwc__sqs = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(tidqg__yiaeh, [narcg__wxy, ngwk__hebdx, builder
            .bitcast(msujg__anzai, lir.IntType(8).as_pointer()), kwc__sqs])
    ucjgt__djvv = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        lhibm__qkvxi = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        rtk__hcyp = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(rtk__hcyp, 1, 'C')
        ucjgt__djvv = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if ucjgt__djvv:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        yfqxa__irlo = builder.extract_value(arr.shape, 0)
        uil__gmxk = arr_type.dtype
        euekt__fkpk = numba_to_c_type(uil__gmxk)
        ipt__bnzu = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), euekt__fkpk))
        if ucjgt__djvv:
            dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
                dkaw__gebyl, name='categorical_array_to_info')
            return builder.call(tidqg__yiaeh, [yfqxa__irlo, builder.bitcast
                (arr.data, lir.IntType(8).as_pointer()), builder.load(
                ipt__bnzu), lhibm__qkvxi, arr.meminfo])
        else:
            dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
                dkaw__gebyl, name='numpy_array_to_info')
            return builder.call(tidqg__yiaeh, [yfqxa__irlo, builder.bitcast
                (arr.data, lir.IntType(8).as_pointer()), builder.load(
                ipt__bnzu), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        uil__gmxk = arr_type.dtype
        ymc__igzgr = uil__gmxk
        if isinstance(arr_type, DecimalArrayType):
            ymc__igzgr = int128_type
        if arr_type == datetime_date_array_type:
            ymc__igzgr = types.int64
        azkdb__kpxsc = context.make_array(types.Array(ymc__igzgr, 1, 'C'))(
            context, builder, arr.data)
        yfqxa__irlo = builder.extract_value(azkdb__kpxsc.shape, 0)
        geh__awqu = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        euekt__fkpk = numba_to_c_type(uil__gmxk)
        ipt__bnzu = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), euekt__fkpk))
        if isinstance(arr_type, DecimalArrayType):
            dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
                dkaw__gebyl, name='decimal_array_to_info')
            return builder.call(tidqg__yiaeh, [yfqxa__irlo, builder.bitcast
                (azkdb__kpxsc.data, lir.IntType(8).as_pointer()), builder.
                load(ipt__bnzu), builder.bitcast(geh__awqu.data, lir.
                IntType(8).as_pointer()), azkdb__kpxsc.meminfo, geh__awqu.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        else:
            dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
                dkaw__gebyl, name='nullable_array_to_info')
            return builder.call(tidqg__yiaeh, [yfqxa__irlo, builder.bitcast
                (azkdb__kpxsc.data, lir.IntType(8).as_pointer()), builder.
                load(ipt__bnzu), builder.bitcast(geh__awqu.data, lir.
                IntType(8).as_pointer()), azkdb__kpxsc.meminfo, geh__awqu.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        xnkgp__ltk = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        idcnl__upx = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        yfqxa__irlo = builder.extract_value(xnkgp__ltk.shape, 0)
        euekt__fkpk = numba_to_c_type(arr_type.arr_type.dtype)
        ipt__bnzu = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), euekt__fkpk))
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='interval_array_to_info')
        return builder.call(tidqg__yiaeh, [yfqxa__irlo, builder.bitcast(
            xnkgp__ltk.data, lir.IntType(8).as_pointer()), builder.bitcast(
            idcnl__upx.data, lir.IntType(8).as_pointer()), builder.load(
            ipt__bnzu), xnkgp__ltk.meminfo, idcnl__upx.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    mbjkx__psdc = cgutils.alloca_once(builder, lir.IntType(64))
    aqe__tah = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    pqcq__guxgx = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
        dkaw__gebyl, name='info_to_numpy_array')
    builder.call(tidqg__yiaeh, [in_info, mbjkx__psdc, aqe__tah, pqcq__guxgx])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    dsjad__vhgr = context.get_value_type(types.intp)
    owpez__yjkso = cgutils.pack_array(builder, [builder.load(mbjkx__psdc)],
        ty=dsjad__vhgr)
    cgfsn__jypy = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    lwjf__dwi = cgutils.pack_array(builder, [cgfsn__jypy], ty=dsjad__vhgr)
    aur__bzoqb = builder.bitcast(builder.load(aqe__tah), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=aur__bzoqb, shape=
        owpez__yjkso, strides=lwjf__dwi, itemsize=cgfsn__jypy, meminfo=
        builder.load(pqcq__guxgx))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    fcfo__kaj = context.make_helper(builder, arr_type)
    dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
        dkaw__gebyl, name='info_to_list_string_array')
    builder.call(tidqg__yiaeh, [in_info, fcfo__kaj._get_ptr_by_name('meminfo')]
        )
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return fcfo__kaj._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    zxjph__evx = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        gomc__nrgo = lengths_pos
        bqkl__cuu = infos_pos
        fqib__bzkr, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        hidzu__pfqej = ArrayItemArrayPayloadType(arr_typ)
        vgf__whfb = context.get_data_type(hidzu__pfqej)
        okduj__fzew = context.get_abi_sizeof(vgf__whfb)
        gphv__qpz = define_array_item_dtor(context, builder, arr_typ,
            hidzu__pfqej)
        rem__krsx = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, okduj__fzew), gphv__qpz)
        tvfjq__inl = context.nrt.meminfo_data(builder, rem__krsx)
        zvq__gdkf = builder.bitcast(tvfjq__inl, vgf__whfb.as_pointer())
        sgczw__nrngj = cgutils.create_struct_proxy(hidzu__pfqej)(context,
            builder)
        sgczw__nrngj.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), gomc__nrgo)
        sgczw__nrngj.data = fqib__bzkr
        abez__ihpgh = builder.load(array_infos_ptr)
        sqwt__gfbz = builder.bitcast(builder.extract_value(abez__ihpgh,
            bqkl__cuu), zxjph__evx)
        sgczw__nrngj.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, sqwt__gfbz)
        slyq__alico = builder.bitcast(builder.extract_value(abez__ihpgh, 
            bqkl__cuu + 1), zxjph__evx)
        sgczw__nrngj.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, slyq__alico)
        builder.store(sgczw__nrngj._getvalue(), zvq__gdkf)
        mrd__ibm = context.make_helper(builder, arr_typ)
        mrd__ibm.meminfo = rem__krsx
        return mrd__ibm._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        erxql__opkvy = []
        bqkl__cuu = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for nrmxv__uyq in arr_typ.data:
            fqib__bzkr, lengths_pos, infos_pos = nested_to_array(context,
                builder, nrmxv__uyq, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            erxql__opkvy.append(fqib__bzkr)
        hidzu__pfqej = StructArrayPayloadType(arr_typ.data)
        vgf__whfb = context.get_value_type(hidzu__pfqej)
        okduj__fzew = context.get_abi_sizeof(vgf__whfb)
        gphv__qpz = define_struct_arr_dtor(context, builder, arr_typ,
            hidzu__pfqej)
        rem__krsx = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, okduj__fzew), gphv__qpz)
        tvfjq__inl = context.nrt.meminfo_data(builder, rem__krsx)
        zvq__gdkf = builder.bitcast(tvfjq__inl, vgf__whfb.as_pointer())
        sgczw__nrngj = cgutils.create_struct_proxy(hidzu__pfqej)(context,
            builder)
        sgczw__nrngj.data = cgutils.pack_array(builder, erxql__opkvy
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, erxql__opkvy)
        abez__ihpgh = builder.load(array_infos_ptr)
        slyq__alico = builder.bitcast(builder.extract_value(abez__ihpgh,
            bqkl__cuu), zxjph__evx)
        sgczw__nrngj.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, slyq__alico)
        builder.store(sgczw__nrngj._getvalue(), zvq__gdkf)
        qphsf__ldtzy = context.make_helper(builder, arr_typ)
        qphsf__ldtzy.meminfo = rem__krsx
        return qphsf__ldtzy._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        abez__ihpgh = builder.load(array_infos_ptr)
        tml__bra = builder.bitcast(builder.extract_value(abez__ihpgh,
            infos_pos), zxjph__evx)
        bou__oqvde = context.make_helper(builder, arr_typ)
        yttk__hbfp = ArrayItemArrayType(char_arr_type)
        mrd__ibm = context.make_helper(builder, yttk__hbfp)
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_to_string_array')
        builder.call(tidqg__yiaeh, [tml__bra, mrd__ibm._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        bou__oqvde.data = mrd__ibm._getvalue()
        return bou__oqvde._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        abez__ihpgh = builder.load(array_infos_ptr)
        mpr__pzkkh = builder.bitcast(builder.extract_value(abez__ihpgh, 
            infos_pos + 1), zxjph__evx)
        return _lower_info_to_array_numpy(arr_typ, context, builder, mpr__pzkkh
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        ymc__igzgr = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            ymc__igzgr = int128_type
        elif arr_typ == datetime_date_array_type:
            ymc__igzgr = types.int64
        abez__ihpgh = builder.load(array_infos_ptr)
        slyq__alico = builder.bitcast(builder.extract_value(abez__ihpgh,
            infos_pos), zxjph__evx)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, slyq__alico)
        mpr__pzkkh = builder.bitcast(builder.extract_value(abez__ihpgh, 
            infos_pos + 1), zxjph__evx)
        arr.data = _lower_info_to_array_numpy(types.Array(ymc__igzgr, 1,
            'C'), context, builder, mpr__pzkkh)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, sjpf__uqu = args
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
                return 1 + sum([get_num_arrays(nrmxv__uyq) for nrmxv__uyq in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(nrmxv__uyq) for nrmxv__uyq in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            fyib__tyol = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            fyib__tyol = _get_map_arr_data_type(arr_type)
        else:
            fyib__tyol = arr_type
        mrelc__kedew = get_num_arrays(fyib__tyol)
        yqv__npbx = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for sjpf__uqu in range(mrelc__kedew)])
        lengths_ptr = cgutils.alloca_once_value(builder, yqv__npbx)
        vtxf__htji = lir.Constant(lir.IntType(8).as_pointer(), None)
        jpgd__keo = cgutils.pack_array(builder, [vtxf__htji for sjpf__uqu in
            range(get_num_infos(fyib__tyol))])
        array_infos_ptr = cgutils.alloca_once_value(builder, jpgd__keo)
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_to_nested_array')
        builder.call(tidqg__yiaeh, [in_info, builder.bitcast(lengths_ptr,
            lir.IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, sjpf__uqu, sjpf__uqu = nested_to_array(context, builder,
            fyib__tyol, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            mfn__kncoo = context.make_helper(builder, arr_type)
            mfn__kncoo.data = arr
            context.nrt.incref(builder, fyib__tyol, arr)
            arr = mfn__kncoo._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, fyib__tyol)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        bou__oqvde = context.make_helper(builder, arr_type)
        yttk__hbfp = ArrayItemArrayType(char_arr_type)
        mrd__ibm = context.make_helper(builder, yttk__hbfp)
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_to_string_array')
        builder.call(tidqg__yiaeh, [in_info, mrd__ibm._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        bou__oqvde.data = mrd__ibm._getvalue()
        return bou__oqvde._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='get_nested_info')
        narcg__wxy = builder.call(tidqg__yiaeh, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        ngwk__hebdx = builder.call(tidqg__yiaeh, [in_info, lir.Constant(lir
            .IntType(32), 2)])
        ixxr__qnep = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        ixxr__qnep.data = info_to_array_codegen(context, builder, sig, (
            narcg__wxy, context.get_constant_null(arr_type.data)))
        djuc__iwk = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = djuc__iwk(array_info_type, djuc__iwk)
        ixxr__qnep.indices = info_to_array_codegen(context, builder, sig, (
            ngwk__hebdx, context.get_constant_null(djuc__iwk)))
        dkaw__gebyl = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='get_has_global_dictionary')
        kwc__sqs = builder.call(tidqg__yiaeh, [in_info])
        ixxr__qnep.has_global_dictionary = builder.trunc(kwc__sqs, cgutils.
            bool_t)
        return ixxr__qnep._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        rtk__hcyp = get_categories_int_type(arr_type.dtype)
        dyg__fgkr = types.Array(rtk__hcyp, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(dyg__fgkr, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            byk__uloi = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(byk__uloi))
            int_type = arr_type.dtype.int_type
            krrv__jxh = bodo.typeof(byk__uloi)
            ioyl__ifdbx = context.get_constant_generic(builder, krrv__jxh,
                byk__uloi)
            uil__gmxk = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(krrv__jxh), [ioyl__ifdbx])
        else:
            uil__gmxk = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, uil__gmxk)
        out_arr.dtype = uil__gmxk
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        aur__bzoqb = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = aur__bzoqb
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        ymc__igzgr = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            ymc__igzgr = int128_type
        elif arr_type == datetime_date_array_type:
            ymc__igzgr = types.int64
        fgmv__amfo = types.Array(ymc__igzgr, 1, 'C')
        azkdb__kpxsc = context.make_array(fgmv__amfo)(context, builder)
        gva__psa = types.Array(types.uint8, 1, 'C')
        klhwf__buc = context.make_array(gva__psa)(context, builder)
        mbjkx__psdc = cgutils.alloca_once(builder, lir.IntType(64))
        xzy__iui = cgutils.alloca_once(builder, lir.IntType(64))
        aqe__tah = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        rpy__lqjpj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        pqcq__guxgx = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        cwmf__yjunl = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_to_nullable_array')
        builder.call(tidqg__yiaeh, [in_info, mbjkx__psdc, xzy__iui,
            aqe__tah, rpy__lqjpj, pqcq__guxgx, cwmf__yjunl])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        dsjad__vhgr = context.get_value_type(types.intp)
        owpez__yjkso = cgutils.pack_array(builder, [builder.load(
            mbjkx__psdc)], ty=dsjad__vhgr)
        cgfsn__jypy = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(ymc__igzgr)))
        lwjf__dwi = cgutils.pack_array(builder, [cgfsn__jypy], ty=dsjad__vhgr)
        aur__bzoqb = builder.bitcast(builder.load(aqe__tah), context.
            get_data_type(ymc__igzgr).as_pointer())
        numba.np.arrayobj.populate_array(azkdb__kpxsc, data=aur__bzoqb,
            shape=owpez__yjkso, strides=lwjf__dwi, itemsize=cgfsn__jypy,
            meminfo=builder.load(pqcq__guxgx))
        arr.data = azkdb__kpxsc._getvalue()
        owpez__yjkso = cgutils.pack_array(builder, [builder.load(xzy__iui)],
            ty=dsjad__vhgr)
        cgfsn__jypy = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        lwjf__dwi = cgutils.pack_array(builder, [cgfsn__jypy], ty=dsjad__vhgr)
        aur__bzoqb = builder.bitcast(builder.load(rpy__lqjpj), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(klhwf__buc, data=aur__bzoqb, shape
            =owpez__yjkso, strides=lwjf__dwi, itemsize=cgfsn__jypy, meminfo
            =builder.load(cwmf__yjunl))
        arr.null_bitmap = klhwf__buc._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        xnkgp__ltk = context.make_array(arr_type.arr_type)(context, builder)
        idcnl__upx = context.make_array(arr_type.arr_type)(context, builder)
        mbjkx__psdc = cgutils.alloca_once(builder, lir.IntType(64))
        ifwq__syn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        mwvu__cxcml = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ozjmd__jop = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        mmqq__aekq = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_to_interval_array')
        builder.call(tidqg__yiaeh, [in_info, mbjkx__psdc, ifwq__syn,
            mwvu__cxcml, ozjmd__jop, mmqq__aekq])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        dsjad__vhgr = context.get_value_type(types.intp)
        owpez__yjkso = cgutils.pack_array(builder, [builder.load(
            mbjkx__psdc)], ty=dsjad__vhgr)
        cgfsn__jypy = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        lwjf__dwi = cgutils.pack_array(builder, [cgfsn__jypy], ty=dsjad__vhgr)
        mmfzw__tgtpt = builder.bitcast(builder.load(ifwq__syn), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(xnkgp__ltk, data=mmfzw__tgtpt,
            shape=owpez__yjkso, strides=lwjf__dwi, itemsize=cgfsn__jypy,
            meminfo=builder.load(ozjmd__jop))
        arr.left = xnkgp__ltk._getvalue()
        tyipi__mvfm = builder.bitcast(builder.load(mwvu__cxcml), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(idcnl__upx, data=tyipi__mvfm,
            shape=owpez__yjkso, strides=lwjf__dwi, itemsize=cgfsn__jypy,
            meminfo=builder.load(mmqq__aekq))
        arr.right = idcnl__upx._getvalue()
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
        yfqxa__irlo, sjpf__uqu = args
        euekt__fkpk = numba_to_c_type(array_type.dtype)
        ipt__bnzu = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), euekt__fkpk))
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='alloc_numpy')
        return builder.call(tidqg__yiaeh, [yfqxa__irlo, builder.load(
            ipt__bnzu)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        yfqxa__irlo, jnb__rexq = args
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='alloc_string_array')
        return builder.call(tidqg__yiaeh, [yfqxa__irlo, jnb__rexq])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    dka__xjlht, = args
    vwb__jmd = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], dka__xjlht)
    dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
        dkaw__gebyl, name='arr_info_list_to_table')
    return builder.call(tidqg__yiaeh, [vwb__jmd.data, vwb__jmd.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_from_table')
        return builder.call(tidqg__yiaeh, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    eft__jxhc = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        tibz__dppc, pcxv__ecsrs, sjpf__uqu = args
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='info_from_table')
        atx__xucd = cgutils.create_struct_proxy(eft__jxhc)(context, builder)
        atx__xucd.parent = cgutils.get_null_value(atx__xucd.parent.type)
        ccnbs__iaub = context.make_array(table_idx_arr_t)(context, builder,
            pcxv__ecsrs)
        tfyjx__nqjrb = context.get_constant(types.int64, -1)
        icvi__jkdh = context.get_constant(types.int64, 0)
        fudi__oev = cgutils.alloca_once_value(builder, icvi__jkdh)
        for t, nilve__zim in eft__jxhc.type_to_blk.items():
            fomh__ebdoa = context.get_constant(types.int64, len(eft__jxhc.
                block_to_arr_ind[nilve__zim]))
            sjpf__uqu, bblf__zvgxf = ListInstance.allocate_ex(context,
                builder, types.List(t), fomh__ebdoa)
            bblf__zvgxf.size = fomh__ebdoa
            mczrt__ehncc = context.make_constant_array(builder, types.Array
                (types.int64, 1, 'C'), np.array(eft__jxhc.block_to_arr_ind[
                nilve__zim], dtype=np.int64))
            xeau__ybl = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, mczrt__ehncc)
            with cgutils.for_range(builder, fomh__ebdoa) as uifw__ete:
                prdb__osjt = uifw__ete.index
                yjwhb__wqd = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    xeau__ybl, prdb__osjt)
                kejsx__fkjef = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, ccnbs__iaub, yjwhb__wqd)
                dnufq__rze = builder.icmp_unsigned('!=', kejsx__fkjef,
                    tfyjx__nqjrb)
                with builder.if_else(dnufq__rze) as (iigk__hefrd, lzis__xsdu):
                    with iigk__hefrd:
                        bld__pfu = builder.call(tidqg__yiaeh, [tibz__dppc,
                            kejsx__fkjef])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            bld__pfu])
                        bblf__zvgxf.inititem(prdb__osjt, arr, incref=False)
                        yfqxa__irlo = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(yfqxa__irlo, fudi__oev)
                    with lzis__xsdu:
                        pnsw__hqin = context.get_constant_null(t)
                        bblf__zvgxf.inititem(prdb__osjt, pnsw__hqin, incref
                            =False)
            setattr(atx__xucd, f'block_{nilve__zim}', bblf__zvgxf.value)
        atx__xucd.len = builder.load(fudi__oev)
        return atx__xucd._getvalue()
    return eft__jxhc(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    eft__jxhc = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        tjt__cuq, sjpf__uqu = args
        pcu__gvkfy = cgutils.create_struct_proxy(eft__jxhc)(context,
            builder, tjt__cuq)
        if eft__jxhc.has_runtime_cols:
            pdefj__phaf = lir.Constant(lir.IntType(64), 0)
            for nilve__zim, t in enumerate(eft__jxhc.arr_types):
                rknzv__albw = getattr(pcu__gvkfy, f'block_{nilve__zim}')
                vyrbi__uwxy = ListInstance(context, builder, types.List(t),
                    rknzv__albw)
                pdefj__phaf = builder.add(pdefj__phaf, vyrbi__uwxy.size)
        else:
            pdefj__phaf = lir.Constant(lir.IntType(64), len(eft__jxhc.
                arr_types))
        sjpf__uqu, pvcy__byucg = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), pdefj__phaf)
        pvcy__byucg.size = pdefj__phaf
        if eft__jxhc.has_runtime_cols:
            kdqqv__ymnb = lir.Constant(lir.IntType(64), 0)
            for nilve__zim, t in enumerate(eft__jxhc.arr_types):
                rknzv__albw = getattr(pcu__gvkfy, f'block_{nilve__zim}')
                vyrbi__uwxy = ListInstance(context, builder, types.List(t),
                    rknzv__albw)
                fomh__ebdoa = vyrbi__uwxy.size
                with cgutils.for_range(builder, fomh__ebdoa) as uifw__ete:
                    prdb__osjt = uifw__ete.index
                    arr = vyrbi__uwxy.getitem(prdb__osjt)
                    ozjax__vsrga = signature(array_info_type, t)
                    nvxop__aql = arr,
                    lsis__pdd = array_to_info_codegen(context, builder,
                        ozjax__vsrga, nvxop__aql)
                    pvcy__byucg.inititem(builder.add(kdqqv__ymnb,
                        prdb__osjt), lsis__pdd, incref=False)
                kdqqv__ymnb = builder.add(kdqqv__ymnb, fomh__ebdoa)
        else:
            for t, nilve__zim in eft__jxhc.type_to_blk.items():
                fomh__ebdoa = context.get_constant(types.int64, len(
                    eft__jxhc.block_to_arr_ind[nilve__zim]))
                rknzv__albw = getattr(pcu__gvkfy, f'block_{nilve__zim}')
                vyrbi__uwxy = ListInstance(context, builder, types.List(t),
                    rknzv__albw)
                mczrt__ehncc = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(eft__jxhc.
                    block_to_arr_ind[nilve__zim], dtype=np.int64))
                xeau__ybl = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, mczrt__ehncc)
                with cgutils.for_range(builder, fomh__ebdoa) as uifw__ete:
                    prdb__osjt = uifw__ete.index
                    yjwhb__wqd = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        xeau__ybl, prdb__osjt)
                    atebl__afhrq = signature(types.none, eft__jxhc, types.
                        List(t), types.int64, types.int64)
                    luao__hcg = tjt__cuq, rknzv__albw, prdb__osjt, yjwhb__wqd
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, atebl__afhrq, luao__hcg)
                    arr = vyrbi__uwxy.getitem(prdb__osjt)
                    ozjax__vsrga = signature(array_info_type, t)
                    nvxop__aql = arr,
                    lsis__pdd = array_to_info_codegen(context, builder,
                        ozjax__vsrga, nvxop__aql)
                    pvcy__byucg.inititem(yjwhb__wqd, lsis__pdd, incref=False)
        xsl__ttn = pvcy__byucg.value
        kugj__nwe = signature(table_type, types.List(array_info_type))
        njg__owg = xsl__ttn,
        tibz__dppc = arr_info_list_to_table_codegen(context, builder,
            kugj__nwe, njg__owg)
        context.nrt.decref(builder, types.List(array_info_type), xsl__ttn)
        return tibz__dppc
    return table_type(eft__jxhc, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='delete_table')
        builder.call(tidqg__yiaeh, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='shuffle_table')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
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
        dkaw__gebyl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='delete_shuffle_info')
        return builder.call(tidqg__yiaeh, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='reverse_shuffle_table')
        return builder.call(tidqg__yiaeh, args)
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
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='hash_join_table')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
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
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='sort_values_table')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='sample_table')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='shuffle_renormalization')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='shuffle_renormalization_group')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='drop_duplicates_table')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
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
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='pivot_groupby_and_aggregate')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
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
        dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        tidqg__yiaeh = cgutils.get_or_insert_function(builder.module,
            dkaw__gebyl, name='groupby_and_aggregate')
        xrvgh__kde = builder.call(tidqg__yiaeh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xrvgh__kde
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
    mktra__fqp = array_to_info(in_arr)
    tkcd__yaxy = array_to_info(in_values)
    jcyu__lhhf = array_to_info(out_arr)
    vxrp__aqix = arr_info_list_to_table([mktra__fqp, tkcd__yaxy, jcyu__lhhf])
    _array_isin(jcyu__lhhf, mktra__fqp, tkcd__yaxy, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(vxrp__aqix)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    mktra__fqp = array_to_info(in_arr)
    jcyu__lhhf = array_to_info(out_arr)
    _get_search_regex(mktra__fqp, case, pat, jcyu__lhhf)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    rnqp__jjox = col_array_typ.dtype
    if isinstance(rnqp__jjox, types.Number) or rnqp__jjox in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                atx__xucd, zfmoz__txxza = args
                atx__xucd = builder.bitcast(atx__xucd, lir.IntType(8).
                    as_pointer().as_pointer())
                yzpn__lva = lir.Constant(lir.IntType(64), c_ind)
                cke__elq = builder.load(builder.gep(atx__xucd, [yzpn__lva]))
                cke__elq = builder.bitcast(cke__elq, context.get_data_type(
                    rnqp__jjox).as_pointer())
                return builder.load(builder.gep(cke__elq, [zfmoz__txxza]))
            return rnqp__jjox(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                atx__xucd, zfmoz__txxza = args
                atx__xucd = builder.bitcast(atx__xucd, lir.IntType(8).
                    as_pointer().as_pointer())
                yzpn__lva = lir.Constant(lir.IntType(64), c_ind)
                cke__elq = builder.load(builder.gep(atx__xucd, [yzpn__lva]))
                dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                yna__jgus = cgutils.get_or_insert_function(builder.module,
                    dkaw__gebyl, name='array_info_getitem')
                vshr__hasc = cgutils.alloca_once(builder, lir.IntType(64))
                args = cke__elq, zfmoz__txxza, vshr__hasc
                aqe__tah = builder.call(yna__jgus, args)
                return context.make_tuple(builder, sig.return_type, [
                    aqe__tah, builder.load(vshr__hasc)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ghu__ugyyf = lir.Constant(lir.IntType(64), 1)
                okxr__mhr = lir.Constant(lir.IntType(64), 2)
                atx__xucd, zfmoz__txxza = args
                atx__xucd = builder.bitcast(atx__xucd, lir.IntType(8).
                    as_pointer().as_pointer())
                yzpn__lva = lir.Constant(lir.IntType(64), c_ind)
                cke__elq = builder.load(builder.gep(atx__xucd, [yzpn__lva]))
                dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                bqhs__hzsnx = cgutils.get_or_insert_function(builder.module,
                    dkaw__gebyl, name='get_nested_info')
                args = cke__elq, okxr__mhr
                vowfr__voob = builder.call(bqhs__hzsnx, args)
                dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                lge__xvzy = cgutils.get_or_insert_function(builder.module,
                    dkaw__gebyl, name='array_info_getdata1')
                args = vowfr__voob,
                eud__kswoj = builder.call(lge__xvzy, args)
                eud__kswoj = builder.bitcast(eud__kswoj, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                ttsmz__nbo = builder.sext(builder.load(builder.gep(
                    eud__kswoj, [zfmoz__txxza])), lir.IntType(64))
                args = cke__elq, ghu__ugyyf
                fou__ozjv = builder.call(bqhs__hzsnx, args)
                dkaw__gebyl = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                yna__jgus = cgutils.get_or_insert_function(builder.module,
                    dkaw__gebyl, name='array_info_getitem')
                vshr__hasc = cgutils.alloca_once(builder, lir.IntType(64))
                args = fou__ozjv, ttsmz__nbo, vshr__hasc
                aqe__tah = builder.call(yna__jgus, args)
                return context.make_tuple(builder, sig.return_type, [
                    aqe__tah, builder.load(vshr__hasc)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{rnqp__jjox}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                gkm__gyucn, zfmoz__txxza = args
                gkm__gyucn = builder.bitcast(gkm__gyucn, lir.IntType(8).
                    as_pointer().as_pointer())
                yzpn__lva = lir.Constant(lir.IntType(64), c_ind)
                cke__elq = builder.load(builder.gep(gkm__gyucn, [yzpn__lva]))
                rhj__cksth = builder.bitcast(cke__elq, context.
                    get_data_type(types.bool_).as_pointer())
                ikq__ppa = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    rhj__cksth, zfmoz__txxza)
                kgp__hfeik = builder.icmp_unsigned('!=', ikq__ppa, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(kgp__hfeik, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        rnqp__jjox = col_array_dtype.dtype
        if rnqp__jjox in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    atx__xucd, zfmoz__txxza = args
                    atx__xucd = builder.bitcast(atx__xucd, lir.IntType(8).
                        as_pointer().as_pointer())
                    yzpn__lva = lir.Constant(lir.IntType(64), c_ind)
                    cke__elq = builder.load(builder.gep(atx__xucd, [yzpn__lva])
                        )
                    cke__elq = builder.bitcast(cke__elq, context.
                        get_data_type(rnqp__jjox).as_pointer())
                    vwm__dqb = builder.load(builder.gep(cke__elq, [
                        zfmoz__txxza]))
                    kgp__hfeik = builder.icmp_unsigned('!=', vwm__dqb, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(kgp__hfeik, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(rnqp__jjox, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    atx__xucd, zfmoz__txxza = args
                    atx__xucd = builder.bitcast(atx__xucd, lir.IntType(8).
                        as_pointer().as_pointer())
                    yzpn__lva = lir.Constant(lir.IntType(64), c_ind)
                    cke__elq = builder.load(builder.gep(atx__xucd, [yzpn__lva])
                        )
                    cke__elq = builder.bitcast(cke__elq, context.
                        get_data_type(rnqp__jjox).as_pointer())
                    vwm__dqb = builder.load(builder.gep(cke__elq, [
                        zfmoz__txxza]))
                    ygs__gwg = signature(types.bool_, rnqp__jjox)
                    ikq__ppa = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, ygs__gwg, (vwm__dqb,))
                    return builder.not_(builder.sext(ikq__ppa, lir.IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
