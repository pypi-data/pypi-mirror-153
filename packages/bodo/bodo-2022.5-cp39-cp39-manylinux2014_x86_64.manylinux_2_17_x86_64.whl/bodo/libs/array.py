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
        dqg__gcv = context.make_helper(builder, arr_type, in_arr)
        in_arr = dqg__gcv.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        cydn__xnx = context.make_helper(builder, arr_type, in_arr)
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='list_string_array_to_info')
        return builder.call(cajls__ilasm, [cydn__xnx.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                ytt__ucc = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for xkdr__wwv in arr_typ.data:
                    ytt__ucc += get_types(xkdr__wwv)
                return ytt__ucc
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
            cxp__jwavb = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                jdeke__pgh = context.make_helper(builder, arr_typ, value=arr)
                ivk__uuzi = get_lengths(_get_map_arr_data_type(arr_typ),
                    jdeke__pgh.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                fiw__nrfzr = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ivk__uuzi = get_lengths(arr_typ.dtype, fiw__nrfzr.data)
                ivk__uuzi = cgutils.pack_array(builder, [fiw__nrfzr.
                    n_arrays] + [builder.extract_value(ivk__uuzi,
                    njpof__wuae) for njpof__wuae in range(ivk__uuzi.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                fiw__nrfzr = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ivk__uuzi = []
                for njpof__wuae, xkdr__wwv in enumerate(arr_typ.data):
                    fiy__zgmu = get_lengths(xkdr__wwv, builder.
                        extract_value(fiw__nrfzr.data, njpof__wuae))
                    ivk__uuzi += [builder.extract_value(fiy__zgmu,
                        osfwa__zvoep) for osfwa__zvoep in range(fiy__zgmu.
                        type.count)]
                ivk__uuzi = cgutils.pack_array(builder, [cxp__jwavb,
                    context.get_constant(types.int64, -1)] + ivk__uuzi)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                ivk__uuzi = cgutils.pack_array(builder, [cxp__jwavb])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return ivk__uuzi

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                jdeke__pgh = context.make_helper(builder, arr_typ, value=arr)
                xzyuq__inkn = get_buffers(_get_map_arr_data_type(arr_typ),
                    jdeke__pgh.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                fiw__nrfzr = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ipxhw__xocy = get_buffers(arr_typ.dtype, fiw__nrfzr.data)
                jwrw__crjyd = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, fiw__nrfzr.offsets)
                vhxa__wgd = builder.bitcast(jwrw__crjyd.data, lir.IntType(8
                    ).as_pointer())
                kwppg__ebhru = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, fiw__nrfzr.null_bitmap)
                xyrn__oev = builder.bitcast(kwppg__ebhru.data, lir.IntType(
                    8).as_pointer())
                xzyuq__inkn = cgutils.pack_array(builder, [vhxa__wgd,
                    xyrn__oev] + [builder.extract_value(ipxhw__xocy,
                    njpof__wuae) for njpof__wuae in range(ipxhw__xocy.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                fiw__nrfzr = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ipxhw__xocy = []
                for njpof__wuae, xkdr__wwv in enumerate(arr_typ.data):
                    yuc__cbqjh = get_buffers(xkdr__wwv, builder.
                        extract_value(fiw__nrfzr.data, njpof__wuae))
                    ipxhw__xocy += [builder.extract_value(yuc__cbqjh,
                        osfwa__zvoep) for osfwa__zvoep in range(yuc__cbqjh.
                        type.count)]
                kwppg__ebhru = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, fiw__nrfzr.null_bitmap)
                xyrn__oev = builder.bitcast(kwppg__ebhru.data, lir.IntType(
                    8).as_pointer())
                xzyuq__inkn = cgutils.pack_array(builder, [xyrn__oev] +
                    ipxhw__xocy)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                vbsqx__cddkw = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    vbsqx__cddkw = int128_type
                elif arr_typ == datetime_date_array_type:
                    vbsqx__cddkw = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                jcm__tqt = context.make_array(types.Array(vbsqx__cddkw, 1, 'C')
                    )(context, builder, arr.data)
                kwppg__ebhru = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, arr.null_bitmap)
                arp__tytz = builder.bitcast(jcm__tqt.data, lir.IntType(8).
                    as_pointer())
                xyrn__oev = builder.bitcast(kwppg__ebhru.data, lir.IntType(
                    8).as_pointer())
                xzyuq__inkn = cgutils.pack_array(builder, [xyrn__oev,
                    arp__tytz])
            elif arr_typ in (string_array_type, binary_array_type):
                fiw__nrfzr = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                rtrn__dwnq = context.make_helper(builder, offset_arr_type,
                    fiw__nrfzr.offsets).data
                pqh__vki = context.make_helper(builder, char_arr_type,
                    fiw__nrfzr.data).data
                ajdey__svi = context.make_helper(builder,
                    null_bitmap_arr_type, fiw__nrfzr.null_bitmap).data
                xzyuq__inkn = cgutils.pack_array(builder, [builder.bitcast(
                    rtrn__dwnq, lir.IntType(8).as_pointer()), builder.
                    bitcast(ajdey__svi, lir.IntType(8).as_pointer()),
                    builder.bitcast(pqh__vki, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                arp__tytz = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                dqkc__ejckl = lir.Constant(lir.IntType(8).as_pointer(), None)
                xzyuq__inkn = cgutils.pack_array(builder, [dqkc__ejckl,
                    arp__tytz])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return xzyuq__inkn

        def get_field_names(arr_typ):
            jqczy__cay = []
            if isinstance(arr_typ, StructArrayType):
                for qost__qfsnw, enpvm__mbst in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    jqczy__cay.append(qost__qfsnw)
                    jqczy__cay += get_field_names(enpvm__mbst)
            elif isinstance(arr_typ, ArrayItemArrayType):
                jqczy__cay += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                jqczy__cay += get_field_names(_get_map_arr_data_type(arr_typ))
            return jqczy__cay
        ytt__ucc = get_types(arr_type)
        lgi__elhc = cgutils.pack_array(builder, [context.get_constant(types
            .int32, t) for t in ytt__ucc])
        mbf__tamx = cgutils.alloca_once_value(builder, lgi__elhc)
        ivk__uuzi = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, ivk__uuzi)
        xzyuq__inkn = get_buffers(arr_type, in_arr)
        pxolc__wwwk = cgutils.alloca_once_value(builder, xzyuq__inkn)
        jqczy__cay = get_field_names(arr_type)
        if len(jqczy__cay) == 0:
            jqczy__cay = ['irrelevant']
        ttdw__fpdn = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in jqczy__cay])
        cgr__ppj = cgutils.alloca_once_value(builder, ttdw__fpdn)
        if isinstance(arr_type, MapArrayType):
            eiot__rwdwi = _get_map_arr_data_type(arr_type)
            nwv__mosf = context.make_helper(builder, arr_type, value=in_arr)
            mquw__bvgg = nwv__mosf.data
        else:
            eiot__rwdwi = arr_type
            mquw__bvgg = in_arr
        bry__fomk = context.make_helper(builder, eiot__rwdwi, mquw__bvgg)
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='nested_array_to_info')
        svniu__qls = builder.call(cajls__ilasm, [builder.bitcast(mbf__tamx,
            lir.IntType(32).as_pointer()), builder.bitcast(pxolc__wwwk, lir
            .IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            cgr__ppj, lir.IntType(8).as_pointer()), bry__fomk.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
    if arr_type in (string_array_type, binary_array_type):
        kguhq__ktsui = context.make_helper(builder, arr_type, in_arr)
        jrqrx__klkl = ArrayItemArrayType(char_arr_type)
        cydn__xnx = context.make_helper(builder, jrqrx__klkl, kguhq__ktsui.data
            )
        fiw__nrfzr = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        rtrn__dwnq = context.make_helper(builder, offset_arr_type,
            fiw__nrfzr.offsets).data
        pqh__vki = context.make_helper(builder, char_arr_type, fiw__nrfzr.data
            ).data
        ajdey__svi = context.make_helper(builder, null_bitmap_arr_type,
            fiw__nrfzr.null_bitmap).data
        mqi__jnd = builder.zext(builder.load(builder.gep(rtrn__dwnq, [
            fiw__nrfzr.n_arrays])), lir.IntType(64))
        wem__ctrg = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='string_array_to_info')
        return builder.call(cajls__ilasm, [fiw__nrfzr.n_arrays, mqi__jnd,
            pqh__vki, rtrn__dwnq, ajdey__svi, cydn__xnx.meminfo, wem__ctrg])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        yqazk__ocwow = arr.data
        bigua__svnrd = arr.indices
        sig = array_info_type(arr_type.data)
        beych__adthz = array_to_info_codegen(context, builder, sig, (
            yqazk__ocwow,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        ecr__wubj = array_to_info_codegen(context, builder, sig, (
            bigua__svnrd,), False)
        pejy__bhuw = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, bigua__svnrd)
        xyrn__oev = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, pejy__bhuw.null_bitmap).data
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='dict_str_array_to_info')
        igvx__drzjl = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(cajls__ilasm, [beych__adthz, ecr__wubj, builder
            .bitcast(xyrn__oev, lir.IntType(8).as_pointer()), igvx__drzjl])
    psfp__qbqi = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        gvmha__yxgm = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        hla__drd = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(hla__drd, 1, 'C')
        psfp__qbqi = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if psfp__qbqi:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        cxp__jwavb = builder.extract_value(arr.shape, 0)
        pcowj__tlp = arr_type.dtype
        efpo__fqcbl = numba_to_c_type(pcowj__tlp)
        zdbuk__vqq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efpo__fqcbl))
        if psfp__qbqi:
            zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            cajls__ilasm = cgutils.get_or_insert_function(builder.module,
                zto__qzwcv, name='categorical_array_to_info')
            return builder.call(cajls__ilasm, [cxp__jwavb, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                zdbuk__vqq), gvmha__yxgm, arr.meminfo])
        else:
            zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            cajls__ilasm = cgutils.get_or_insert_function(builder.module,
                zto__qzwcv, name='numpy_array_to_info')
            return builder.call(cajls__ilasm, [cxp__jwavb, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                zdbuk__vqq), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        pcowj__tlp = arr_type.dtype
        vbsqx__cddkw = pcowj__tlp
        if isinstance(arr_type, DecimalArrayType):
            vbsqx__cddkw = int128_type
        if arr_type == datetime_date_array_type:
            vbsqx__cddkw = types.int64
        jcm__tqt = context.make_array(types.Array(vbsqx__cddkw, 1, 'C'))(
            context, builder, arr.data)
        cxp__jwavb = builder.extract_value(jcm__tqt.shape, 0)
        dmxdd__oxon = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        efpo__fqcbl = numba_to_c_type(pcowj__tlp)
        zdbuk__vqq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efpo__fqcbl))
        if isinstance(arr_type, DecimalArrayType):
            zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            cajls__ilasm = cgutils.get_or_insert_function(builder.module,
                zto__qzwcv, name='decimal_array_to_info')
            return builder.call(cajls__ilasm, [cxp__jwavb, builder.bitcast(
                jcm__tqt.data, lir.IntType(8).as_pointer()), builder.load(
                zdbuk__vqq), builder.bitcast(dmxdd__oxon.data, lir.IntType(
                8).as_pointer()), jcm__tqt.meminfo, dmxdd__oxon.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        else:
            zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            cajls__ilasm = cgutils.get_or_insert_function(builder.module,
                zto__qzwcv, name='nullable_array_to_info')
            return builder.call(cajls__ilasm, [cxp__jwavb, builder.bitcast(
                jcm__tqt.data, lir.IntType(8).as_pointer()), builder.load(
                zdbuk__vqq), builder.bitcast(dmxdd__oxon.data, lir.IntType(
                8).as_pointer()), jcm__tqt.meminfo, dmxdd__oxon.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        nzfp__dhe = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        esm__udovw = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        cxp__jwavb = builder.extract_value(nzfp__dhe.shape, 0)
        efpo__fqcbl = numba_to_c_type(arr_type.arr_type.dtype)
        zdbuk__vqq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efpo__fqcbl))
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='interval_array_to_info')
        return builder.call(cajls__ilasm, [cxp__jwavb, builder.bitcast(
            nzfp__dhe.data, lir.IntType(8).as_pointer()), builder.bitcast(
            esm__udovw.data, lir.IntType(8).as_pointer()), builder.load(
            zdbuk__vqq), nzfp__dhe.meminfo, esm__udovw.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    loc__fdxc = cgutils.alloca_once(builder, lir.IntType(64))
    arp__tytz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    vpz__wyg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    cajls__ilasm = cgutils.get_or_insert_function(builder.module,
        zto__qzwcv, name='info_to_numpy_array')
    builder.call(cajls__ilasm, [in_info, loc__fdxc, arp__tytz, vpz__wyg])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    aqsp__tvstb = context.get_value_type(types.intp)
    bqv__hevf = cgutils.pack_array(builder, [builder.load(loc__fdxc)], ty=
        aqsp__tvstb)
    jfyk__qbyq = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    tvoms__lprhn = cgutils.pack_array(builder, [jfyk__qbyq], ty=aqsp__tvstb)
    pqh__vki = builder.bitcast(builder.load(arp__tytz), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=pqh__vki, shape=bqv__hevf,
        strides=tvoms__lprhn, itemsize=jfyk__qbyq, meminfo=builder.load(
        vpz__wyg))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    hnio__ecdc = context.make_helper(builder, arr_type)
    zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    cajls__ilasm = cgutils.get_or_insert_function(builder.module,
        zto__qzwcv, name='info_to_list_string_array')
    builder.call(cajls__ilasm, [in_info, hnio__ecdc._get_ptr_by_name(
        'meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return hnio__ecdc._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    ubb__zlg = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        cdsm__gjfn = lengths_pos
        iimxz__sjozn = infos_pos
        tszb__odo, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        itd__esik = ArrayItemArrayPayloadType(arr_typ)
        zumjd__lbgdf = context.get_data_type(itd__esik)
        tynhu__llko = context.get_abi_sizeof(zumjd__lbgdf)
        vnzsd__criw = define_array_item_dtor(context, builder, arr_typ,
            itd__esik)
        wxwjf__cyf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tynhu__llko), vnzsd__criw)
        uwzri__irxa = context.nrt.meminfo_data(builder, wxwjf__cyf)
        epxeu__gjb = builder.bitcast(uwzri__irxa, zumjd__lbgdf.as_pointer())
        fiw__nrfzr = cgutils.create_struct_proxy(itd__esik)(context, builder)
        fiw__nrfzr.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), cdsm__gjfn)
        fiw__nrfzr.data = tszb__odo
        cwde__fusos = builder.load(array_infos_ptr)
        qmkw__ukxzs = builder.bitcast(builder.extract_value(cwde__fusos,
            iimxz__sjozn), ubb__zlg)
        fiw__nrfzr.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, qmkw__ukxzs)
        hmuql__roecs = builder.bitcast(builder.extract_value(cwde__fusos, 
            iimxz__sjozn + 1), ubb__zlg)
        fiw__nrfzr.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, hmuql__roecs)
        builder.store(fiw__nrfzr._getvalue(), epxeu__gjb)
        cydn__xnx = context.make_helper(builder, arr_typ)
        cydn__xnx.meminfo = wxwjf__cyf
        return cydn__xnx._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        lapsk__qkcf = []
        iimxz__sjozn = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for zctg__saeag in arr_typ.data:
            tszb__odo, lengths_pos, infos_pos = nested_to_array(context,
                builder, zctg__saeag, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            lapsk__qkcf.append(tszb__odo)
        itd__esik = StructArrayPayloadType(arr_typ.data)
        zumjd__lbgdf = context.get_value_type(itd__esik)
        tynhu__llko = context.get_abi_sizeof(zumjd__lbgdf)
        vnzsd__criw = define_struct_arr_dtor(context, builder, arr_typ,
            itd__esik)
        wxwjf__cyf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tynhu__llko), vnzsd__criw)
        uwzri__irxa = context.nrt.meminfo_data(builder, wxwjf__cyf)
        epxeu__gjb = builder.bitcast(uwzri__irxa, zumjd__lbgdf.as_pointer())
        fiw__nrfzr = cgutils.create_struct_proxy(itd__esik)(context, builder)
        fiw__nrfzr.data = cgutils.pack_array(builder, lapsk__qkcf
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, lapsk__qkcf)
        cwde__fusos = builder.load(array_infos_ptr)
        hmuql__roecs = builder.bitcast(builder.extract_value(cwde__fusos,
            iimxz__sjozn), ubb__zlg)
        fiw__nrfzr.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, hmuql__roecs)
        builder.store(fiw__nrfzr._getvalue(), epxeu__gjb)
        sbwf__rwzo = context.make_helper(builder, arr_typ)
        sbwf__rwzo.meminfo = wxwjf__cyf
        return sbwf__rwzo._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        cwde__fusos = builder.load(array_infos_ptr)
        ywjpq__fia = builder.bitcast(builder.extract_value(cwde__fusos,
            infos_pos), ubb__zlg)
        kguhq__ktsui = context.make_helper(builder, arr_typ)
        jrqrx__klkl = ArrayItemArrayType(char_arr_type)
        cydn__xnx = context.make_helper(builder, jrqrx__klkl)
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_to_string_array')
        builder.call(cajls__ilasm, [ywjpq__fia, cydn__xnx._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        kguhq__ktsui.data = cydn__xnx._getvalue()
        return kguhq__ktsui._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        cwde__fusos = builder.load(array_infos_ptr)
        hnzkn__orq = builder.bitcast(builder.extract_value(cwde__fusos, 
            infos_pos + 1), ubb__zlg)
        return _lower_info_to_array_numpy(arr_typ, context, builder, hnzkn__orq
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        vbsqx__cddkw = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            vbsqx__cddkw = int128_type
        elif arr_typ == datetime_date_array_type:
            vbsqx__cddkw = types.int64
        cwde__fusos = builder.load(array_infos_ptr)
        hmuql__roecs = builder.bitcast(builder.extract_value(cwde__fusos,
            infos_pos), ubb__zlg)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, hmuql__roecs)
        hnzkn__orq = builder.bitcast(builder.extract_value(cwde__fusos, 
            infos_pos + 1), ubb__zlg)
        arr.data = _lower_info_to_array_numpy(types.Array(vbsqx__cddkw, 1,
            'C'), context, builder, hnzkn__orq)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, tdtak__ange = args
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
                return 1 + sum([get_num_arrays(zctg__saeag) for zctg__saeag in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(zctg__saeag) for zctg__saeag in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            erowl__rtpp = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            erowl__rtpp = _get_map_arr_data_type(arr_type)
        else:
            erowl__rtpp = arr_type
        bqq__ghy = get_num_arrays(erowl__rtpp)
        ivk__uuzi = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for tdtak__ange in range(bqq__ghy)])
        lengths_ptr = cgutils.alloca_once_value(builder, ivk__uuzi)
        dqkc__ejckl = lir.Constant(lir.IntType(8).as_pointer(), None)
        beesy__gqdbq = cgutils.pack_array(builder, [dqkc__ejckl for
            tdtak__ange in range(get_num_infos(erowl__rtpp))])
        array_infos_ptr = cgutils.alloca_once_value(builder, beesy__gqdbq)
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_to_nested_array')
        builder.call(cajls__ilasm, [in_info, builder.bitcast(lengths_ptr,
            lir.IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, tdtak__ange, tdtak__ange = nested_to_array(context, builder,
            erowl__rtpp, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            dqg__gcv = context.make_helper(builder, arr_type)
            dqg__gcv.data = arr
            context.nrt.incref(builder, erowl__rtpp, arr)
            arr = dqg__gcv._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, erowl__rtpp)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        kguhq__ktsui = context.make_helper(builder, arr_type)
        jrqrx__klkl = ArrayItemArrayType(char_arr_type)
        cydn__xnx = context.make_helper(builder, jrqrx__klkl)
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_to_string_array')
        builder.call(cajls__ilasm, [in_info, cydn__xnx._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        kguhq__ktsui.data = cydn__xnx._getvalue()
        return kguhq__ktsui._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='get_nested_info')
        beych__adthz = builder.call(cajls__ilasm, [in_info, lir.Constant(
            lir.IntType(32), 1)])
        ecr__wubj = builder.call(cajls__ilasm, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        twhx__jol = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        twhx__jol.data = info_to_array_codegen(context, builder, sig, (
            beych__adthz, context.get_constant_null(arr_type.data)))
        rro__yph = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = rro__yph(array_info_type, rro__yph)
        twhx__jol.indices = info_to_array_codegen(context, builder, sig, (
            ecr__wubj, context.get_constant_null(rro__yph)))
        zto__qzwcv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='get_has_global_dictionary')
        igvx__drzjl = builder.call(cajls__ilasm, [in_info])
        twhx__jol.has_global_dictionary = builder.trunc(igvx__drzjl,
            cgutils.bool_t)
        return twhx__jol._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        hla__drd = get_categories_int_type(arr_type.dtype)
        tjday__srl = types.Array(hla__drd, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(tjday__srl, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            jpb__nvm = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(jpb__nvm))
            int_type = arr_type.dtype.int_type
            hor__cbsw = bodo.typeof(jpb__nvm)
            you__yzg = context.get_constant_generic(builder, hor__cbsw,
                jpb__nvm)
            pcowj__tlp = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(hor__cbsw), [you__yzg])
        else:
            pcowj__tlp = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, pcowj__tlp)
        out_arr.dtype = pcowj__tlp
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        pqh__vki = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = pqh__vki
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        vbsqx__cddkw = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            vbsqx__cddkw = int128_type
        elif arr_type == datetime_date_array_type:
            vbsqx__cddkw = types.int64
        yhoss__pinh = types.Array(vbsqx__cddkw, 1, 'C')
        jcm__tqt = context.make_array(yhoss__pinh)(context, builder)
        vxv__mnj = types.Array(types.uint8, 1, 'C')
        wznc__qdbt = context.make_array(vxv__mnj)(context, builder)
        loc__fdxc = cgutils.alloca_once(builder, lir.IntType(64))
        csy__lahb = cgutils.alloca_once(builder, lir.IntType(64))
        arp__tytz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        odcv__ikycr = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        vpz__wyg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wfg__zloat = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_to_nullable_array')
        builder.call(cajls__ilasm, [in_info, loc__fdxc, csy__lahb,
            arp__tytz, odcv__ikycr, vpz__wyg, wfg__zloat])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        aqsp__tvstb = context.get_value_type(types.intp)
        bqv__hevf = cgutils.pack_array(builder, [builder.load(loc__fdxc)],
            ty=aqsp__tvstb)
        jfyk__qbyq = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(vbsqx__cddkw)))
        tvoms__lprhn = cgutils.pack_array(builder, [jfyk__qbyq], ty=aqsp__tvstb
            )
        pqh__vki = builder.bitcast(builder.load(arp__tytz), context.
            get_data_type(vbsqx__cddkw).as_pointer())
        numba.np.arrayobj.populate_array(jcm__tqt, data=pqh__vki, shape=
            bqv__hevf, strides=tvoms__lprhn, itemsize=jfyk__qbyq, meminfo=
            builder.load(vpz__wyg))
        arr.data = jcm__tqt._getvalue()
        bqv__hevf = cgutils.pack_array(builder, [builder.load(csy__lahb)],
            ty=aqsp__tvstb)
        jfyk__qbyq = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        tvoms__lprhn = cgutils.pack_array(builder, [jfyk__qbyq], ty=aqsp__tvstb
            )
        pqh__vki = builder.bitcast(builder.load(odcv__ikycr), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(wznc__qdbt, data=pqh__vki, shape=
            bqv__hevf, strides=tvoms__lprhn, itemsize=jfyk__qbyq, meminfo=
            builder.load(wfg__zloat))
        arr.null_bitmap = wznc__qdbt._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        nzfp__dhe = context.make_array(arr_type.arr_type)(context, builder)
        esm__udovw = context.make_array(arr_type.arr_type)(context, builder)
        loc__fdxc = cgutils.alloca_once(builder, lir.IntType(64))
        fprsy__zqkb = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dgwo__sgha = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ojxc__krltx = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        puat__ulvu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_to_interval_array')
        builder.call(cajls__ilasm, [in_info, loc__fdxc, fprsy__zqkb,
            dgwo__sgha, ojxc__krltx, puat__ulvu])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        aqsp__tvstb = context.get_value_type(types.intp)
        bqv__hevf = cgutils.pack_array(builder, [builder.load(loc__fdxc)],
            ty=aqsp__tvstb)
        jfyk__qbyq = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        tvoms__lprhn = cgutils.pack_array(builder, [jfyk__qbyq], ty=aqsp__tvstb
            )
        mml__itc = builder.bitcast(builder.load(fprsy__zqkb), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(nzfp__dhe, data=mml__itc, shape=
            bqv__hevf, strides=tvoms__lprhn, itemsize=jfyk__qbyq, meminfo=
            builder.load(ojxc__krltx))
        arr.left = nzfp__dhe._getvalue()
        vphoy__iqpmn = builder.bitcast(builder.load(dgwo__sgha), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(esm__udovw, data=vphoy__iqpmn,
            shape=bqv__hevf, strides=tvoms__lprhn, itemsize=jfyk__qbyq,
            meminfo=builder.load(puat__ulvu))
        arr.right = esm__udovw._getvalue()
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
        cxp__jwavb, tdtak__ange = args
        efpo__fqcbl = numba_to_c_type(array_type.dtype)
        zdbuk__vqq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efpo__fqcbl))
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='alloc_numpy')
        return builder.call(cajls__ilasm, [cxp__jwavb, builder.load(
            zdbuk__vqq)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        cxp__jwavb, jtdtz__irf = args
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='alloc_string_array')
        return builder.call(cajls__ilasm, [cxp__jwavb, jtdtz__irf])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    pit__slks, = args
    bmyws__magx = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], pit__slks)
    zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer().as_pointer(), lir.IntType(64)])
    cajls__ilasm = cgutils.get_or_insert_function(builder.module,
        zto__qzwcv, name='arr_info_list_to_table')
    return builder.call(cajls__ilasm, [bmyws__magx.data, bmyws__magx.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_from_table')
        return builder.call(cajls__ilasm, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    eydxf__ryo = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        taat__ggav, wdzp__bprcj, tdtak__ange = args
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='info_from_table')
        otsz__cvtv = cgutils.create_struct_proxy(eydxf__ryo)(context, builder)
        otsz__cvtv.parent = cgutils.get_null_value(otsz__cvtv.parent.type)
        lnjff__ijigj = context.make_array(table_idx_arr_t)(context, builder,
            wdzp__bprcj)
        bbq__nge = context.get_constant(types.int64, -1)
        kok__ppzn = context.get_constant(types.int64, 0)
        tospv__icqpw = cgutils.alloca_once_value(builder, kok__ppzn)
        for t, tha__ljpn in eydxf__ryo.type_to_blk.items():
            zlof__rzdc = context.get_constant(types.int64, len(eydxf__ryo.
                block_to_arr_ind[tha__ljpn]))
            tdtak__ange, vpt__vmo = ListInstance.allocate_ex(context,
                builder, types.List(t), zlof__rzdc)
            vpt__vmo.size = zlof__rzdc
            olbw__fjhit = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(eydxf__ryo.block_to_arr_ind[
                tha__ljpn], dtype=np.int64))
            trlr__rovd = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, olbw__fjhit)
            with cgutils.for_range(builder, zlof__rzdc) as vqpny__kouqu:
                njpof__wuae = vqpny__kouqu.index
                coo__vkbia = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    trlr__rovd, njpof__wuae)
                ujp__wcjpn = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, lnjff__ijigj, coo__vkbia)
                uxask__anf = builder.icmp_unsigned('!=', ujp__wcjpn, bbq__nge)
                with builder.if_else(uxask__anf) as (kpq__hepz, cqopu__arx):
                    with kpq__hepz:
                        bdggw__sbl = builder.call(cajls__ilasm, [taat__ggav,
                            ujp__wcjpn])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            bdggw__sbl])
                        vpt__vmo.inititem(njpof__wuae, arr, incref=False)
                        cxp__jwavb = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(cxp__jwavb, tospv__icqpw)
                    with cqopu__arx:
                        kpnom__yxq = context.get_constant_null(t)
                        vpt__vmo.inititem(njpof__wuae, kpnom__yxq, incref=False
                            )
            setattr(otsz__cvtv, f'block_{tha__ljpn}', vpt__vmo.value)
        otsz__cvtv.len = builder.load(tospv__icqpw)
        return otsz__cvtv._getvalue()
    return eydxf__ryo(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    eydxf__ryo = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        imqhw__fdpe, tdtak__ange = args
        vune__jgb = cgutils.create_struct_proxy(eydxf__ryo)(context,
            builder, imqhw__fdpe)
        if eydxf__ryo.has_runtime_cols:
            akn__fir = lir.Constant(lir.IntType(64), 0)
            for tha__ljpn, t in enumerate(eydxf__ryo.arr_types):
                nmobf__vcxqs = getattr(vune__jgb, f'block_{tha__ljpn}')
                yyzvr__djqu = ListInstance(context, builder, types.List(t),
                    nmobf__vcxqs)
                akn__fir = builder.add(akn__fir, yyzvr__djqu.size)
        else:
            akn__fir = lir.Constant(lir.IntType(64), len(eydxf__ryo.arr_types))
        tdtak__ange, qpimp__uus = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), akn__fir)
        qpimp__uus.size = akn__fir
        if eydxf__ryo.has_runtime_cols:
            zelml__uph = lir.Constant(lir.IntType(64), 0)
            for tha__ljpn, t in enumerate(eydxf__ryo.arr_types):
                nmobf__vcxqs = getattr(vune__jgb, f'block_{tha__ljpn}')
                yyzvr__djqu = ListInstance(context, builder, types.List(t),
                    nmobf__vcxqs)
                zlof__rzdc = yyzvr__djqu.size
                with cgutils.for_range(builder, zlof__rzdc) as vqpny__kouqu:
                    njpof__wuae = vqpny__kouqu.index
                    arr = yyzvr__djqu.getitem(njpof__wuae)
                    mdp__bludl = signature(array_info_type, t)
                    dqofl__wyb = arr,
                    phgj__klt = array_to_info_codegen(context, builder,
                        mdp__bludl, dqofl__wyb)
                    qpimp__uus.inititem(builder.add(zelml__uph, njpof__wuae
                        ), phgj__klt, incref=False)
                zelml__uph = builder.add(zelml__uph, zlof__rzdc)
        else:
            for t, tha__ljpn in eydxf__ryo.type_to_blk.items():
                zlof__rzdc = context.get_constant(types.int64, len(
                    eydxf__ryo.block_to_arr_ind[tha__ljpn]))
                nmobf__vcxqs = getattr(vune__jgb, f'block_{tha__ljpn}')
                yyzvr__djqu = ListInstance(context, builder, types.List(t),
                    nmobf__vcxqs)
                olbw__fjhit = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(eydxf__ryo.
                    block_to_arr_ind[tha__ljpn], dtype=np.int64))
                trlr__rovd = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, olbw__fjhit)
                with cgutils.for_range(builder, zlof__rzdc) as vqpny__kouqu:
                    njpof__wuae = vqpny__kouqu.index
                    coo__vkbia = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        trlr__rovd, njpof__wuae)
                    qth__iadk = signature(types.none, eydxf__ryo, types.
                        List(t), types.int64, types.int64)
                    ocur__tzbzx = (imqhw__fdpe, nmobf__vcxqs, njpof__wuae,
                        coo__vkbia)
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, qth__iadk, ocur__tzbzx)
                    arr = yyzvr__djqu.getitem(njpof__wuae)
                    mdp__bludl = signature(array_info_type, t)
                    dqofl__wyb = arr,
                    phgj__klt = array_to_info_codegen(context, builder,
                        mdp__bludl, dqofl__wyb)
                    qpimp__uus.inititem(coo__vkbia, phgj__klt, incref=False)
        gqz__dvnd = qpimp__uus.value
        bhdo__wuff = signature(table_type, types.List(array_info_type))
        yrul__hau = gqz__dvnd,
        taat__ggav = arr_info_list_to_table_codegen(context, builder,
            bhdo__wuff, yrul__hau)
        context.nrt.decref(builder, types.List(array_info_type), gqz__dvnd)
        return taat__ggav
    return table_type(eydxf__ryo, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='delete_table')
        builder.call(cajls__ilasm, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='shuffle_table')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
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
        zto__qzwcv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='delete_shuffle_info')
        return builder.call(cajls__ilasm, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='reverse_shuffle_table')
        return builder.call(cajls__ilasm, args)
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
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='hash_join_table')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
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
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='sort_values_table')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='sample_table')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='shuffle_renormalization')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='shuffle_renormalization_group')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='drop_duplicates_table')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
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
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='pivot_groupby_and_aggregate')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
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
        zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        cajls__ilasm = cgutils.get_or_insert_function(builder.module,
            zto__qzwcv, name='groupby_and_aggregate')
        svniu__qls = builder.call(cajls__ilasm, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return svniu__qls
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
    sajgp__ojmxm = array_to_info(in_arr)
    vey__rranf = array_to_info(in_values)
    yvljf__oefqw = array_to_info(out_arr)
    efk__ptc = arr_info_list_to_table([sajgp__ojmxm, vey__rranf, yvljf__oefqw])
    _array_isin(yvljf__oefqw, sajgp__ojmxm, vey__rranf, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(efk__ptc)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    sajgp__ojmxm = array_to_info(in_arr)
    yvljf__oefqw = array_to_info(out_arr)
    _get_search_regex(sajgp__ojmxm, case, pat, yvljf__oefqw)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    ypa__iaou = col_array_typ.dtype
    if isinstance(ypa__iaou, types.Number) or ypa__iaou in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                otsz__cvtv, zfc__teei = args
                otsz__cvtv = builder.bitcast(otsz__cvtv, lir.IntType(8).
                    as_pointer().as_pointer())
                saerj__mct = lir.Constant(lir.IntType(64), c_ind)
                dhrk__bkn = builder.load(builder.gep(otsz__cvtv, [saerj__mct]))
                dhrk__bkn = builder.bitcast(dhrk__bkn, context.
                    get_data_type(ypa__iaou).as_pointer())
                return builder.load(builder.gep(dhrk__bkn, [zfc__teei]))
            return ypa__iaou(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                otsz__cvtv, zfc__teei = args
                otsz__cvtv = builder.bitcast(otsz__cvtv, lir.IntType(8).
                    as_pointer().as_pointer())
                saerj__mct = lir.Constant(lir.IntType(64), c_ind)
                dhrk__bkn = builder.load(builder.gep(otsz__cvtv, [saerj__mct]))
                zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                zfuwm__rrvv = cgutils.get_or_insert_function(builder.module,
                    zto__qzwcv, name='array_info_getitem')
                bzh__rud = cgutils.alloca_once(builder, lir.IntType(64))
                args = dhrk__bkn, zfc__teei, bzh__rud
                arp__tytz = builder.call(zfuwm__rrvv, args)
                return context.make_tuple(builder, sig.return_type, [
                    arp__tytz, builder.load(bzh__rud)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                gqvp__vyiq = lir.Constant(lir.IntType(64), 1)
                ucvi__telqt = lir.Constant(lir.IntType(64), 2)
                otsz__cvtv, zfc__teei = args
                otsz__cvtv = builder.bitcast(otsz__cvtv, lir.IntType(8).
                    as_pointer().as_pointer())
                saerj__mct = lir.Constant(lir.IntType(64), c_ind)
                dhrk__bkn = builder.load(builder.gep(otsz__cvtv, [saerj__mct]))
                zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                qlx__hcwt = cgutils.get_or_insert_function(builder.module,
                    zto__qzwcv, name='get_nested_info')
                args = dhrk__bkn, ucvi__telqt
                uyhix__opz = builder.call(qlx__hcwt, args)
                zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                wxn__pfj = cgutils.get_or_insert_function(builder.module,
                    zto__qzwcv, name='array_info_getdata1')
                args = uyhix__opz,
                hpxt__joj = builder.call(wxn__pfj, args)
                hpxt__joj = builder.bitcast(hpxt__joj, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                vshfg__ufh = builder.sext(builder.load(builder.gep(
                    hpxt__joj, [zfc__teei])), lir.IntType(64))
                args = dhrk__bkn, gqvp__vyiq
                hhhf__gze = builder.call(qlx__hcwt, args)
                zto__qzwcv = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                zfuwm__rrvv = cgutils.get_or_insert_function(builder.module,
                    zto__qzwcv, name='array_info_getitem')
                bzh__rud = cgutils.alloca_once(builder, lir.IntType(64))
                args = hhhf__gze, vshfg__ufh, bzh__rud
                arp__tytz = builder.call(zfuwm__rrvv, args)
                return context.make_tuple(builder, sig.return_type, [
                    arp__tytz, builder.load(bzh__rud)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{ypa__iaou}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                zlyg__hddi, zfc__teei = args
                zlyg__hddi = builder.bitcast(zlyg__hddi, lir.IntType(8).
                    as_pointer().as_pointer())
                saerj__mct = lir.Constant(lir.IntType(64), c_ind)
                dhrk__bkn = builder.load(builder.gep(zlyg__hddi, [saerj__mct]))
                ajdey__svi = builder.bitcast(dhrk__bkn, context.
                    get_data_type(types.bool_).as_pointer())
                zww__mdz = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ajdey__svi, zfc__teei)
                wgc__cdgt = builder.icmp_unsigned('!=', zww__mdz, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(wgc__cdgt, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        ypa__iaou = col_array_dtype.dtype
        if ypa__iaou in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    otsz__cvtv, zfc__teei = args
                    otsz__cvtv = builder.bitcast(otsz__cvtv, lir.IntType(8)
                        .as_pointer().as_pointer())
                    saerj__mct = lir.Constant(lir.IntType(64), c_ind)
                    dhrk__bkn = builder.load(builder.gep(otsz__cvtv, [
                        saerj__mct]))
                    dhrk__bkn = builder.bitcast(dhrk__bkn, context.
                        get_data_type(ypa__iaou).as_pointer())
                    uwngy__nlung = builder.load(builder.gep(dhrk__bkn, [
                        zfc__teei]))
                    wgc__cdgt = builder.icmp_unsigned('!=', uwngy__nlung,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(wgc__cdgt, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(ypa__iaou, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    otsz__cvtv, zfc__teei = args
                    otsz__cvtv = builder.bitcast(otsz__cvtv, lir.IntType(8)
                        .as_pointer().as_pointer())
                    saerj__mct = lir.Constant(lir.IntType(64), c_ind)
                    dhrk__bkn = builder.load(builder.gep(otsz__cvtv, [
                        saerj__mct]))
                    dhrk__bkn = builder.bitcast(dhrk__bkn, context.
                        get_data_type(ypa__iaou).as_pointer())
                    uwngy__nlung = builder.load(builder.gep(dhrk__bkn, [
                        zfc__teei]))
                    rwxs__rboo = signature(types.bool_, ypa__iaou)
                    zww__mdz = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, rwxs__rboo, (uwngy__nlung,))
                    return builder.not_(builder.sext(zww__mdz, lir.IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
