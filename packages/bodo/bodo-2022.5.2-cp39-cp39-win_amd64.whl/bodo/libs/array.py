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
        yci__yxz = context.make_helper(builder, arr_type, in_arr)
        in_arr = yci__yxz.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        fews__ozoo = context.make_helper(builder, arr_type, in_arr)
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='list_string_array_to_info')
        return builder.call(hoqb__mtyog, [fews__ozoo.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                wvng__tya = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for fnjwc__dee in arr_typ.data:
                    wvng__tya += get_types(fnjwc__dee)
                return wvng__tya
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
            klijk__ycuz = context.compile_internal(builder, lambda a: len(a
                ), types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                maqs__ldgy = context.make_helper(builder, arr_typ, value=arr)
                jlghn__aagz = get_lengths(_get_map_arr_data_type(arr_typ),
                    maqs__ldgy.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                dxjsd__zrqeh = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                jlghn__aagz = get_lengths(arr_typ.dtype, dxjsd__zrqeh.data)
                jlghn__aagz = cgutils.pack_array(builder, [dxjsd__zrqeh.
                    n_arrays] + [builder.extract_value(jlghn__aagz,
                    aps__kbs) for aps__kbs in range(jlghn__aagz.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                dxjsd__zrqeh = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                jlghn__aagz = []
                for aps__kbs, fnjwc__dee in enumerate(arr_typ.data):
                    qah__sgj = get_lengths(fnjwc__dee, builder.
                        extract_value(dxjsd__zrqeh.data, aps__kbs))
                    jlghn__aagz += [builder.extract_value(qah__sgj,
                        lgjys__dmk) for lgjys__dmk in range(qah__sgj.type.
                        count)]
                jlghn__aagz = cgutils.pack_array(builder, [klijk__ycuz,
                    context.get_constant(types.int64, -1)] + jlghn__aagz)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                jlghn__aagz = cgutils.pack_array(builder, [klijk__ycuz])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return jlghn__aagz

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                maqs__ldgy = context.make_helper(builder, arr_typ, value=arr)
                msjlf__nww = get_buffers(_get_map_arr_data_type(arr_typ),
                    maqs__ldgy.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                dxjsd__zrqeh = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                jhcj__jayxv = get_buffers(arr_typ.dtype, dxjsd__zrqeh.data)
                ung__ancr = context.make_array(types.Array(offset_type, 1, 'C')
                    )(context, builder, dxjsd__zrqeh.offsets)
                yue__asfyt = builder.bitcast(ung__ancr.data, lir.IntType(8)
                    .as_pointer())
                imaji__gav = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, dxjsd__zrqeh.null_bitmap)
                lqvq__jgu = builder.bitcast(imaji__gav.data, lir.IntType(8)
                    .as_pointer())
                msjlf__nww = cgutils.pack_array(builder, [yue__asfyt,
                    lqvq__jgu] + [builder.extract_value(jhcj__jayxv,
                    aps__kbs) for aps__kbs in range(jhcj__jayxv.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                dxjsd__zrqeh = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                jhcj__jayxv = []
                for aps__kbs, fnjwc__dee in enumerate(arr_typ.data):
                    ckbaa__yhhkz = get_buffers(fnjwc__dee, builder.
                        extract_value(dxjsd__zrqeh.data, aps__kbs))
                    jhcj__jayxv += [builder.extract_value(ckbaa__yhhkz,
                        lgjys__dmk) for lgjys__dmk in range(ckbaa__yhhkz.
                        type.count)]
                imaji__gav = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, dxjsd__zrqeh.null_bitmap)
                lqvq__jgu = builder.bitcast(imaji__gav.data, lir.IntType(8)
                    .as_pointer())
                msjlf__nww = cgutils.pack_array(builder, [lqvq__jgu] +
                    jhcj__jayxv)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                pjeu__yovyq = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    pjeu__yovyq = int128_type
                elif arr_typ == datetime_date_array_type:
                    pjeu__yovyq = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                pvzk__pnv = context.make_array(types.Array(pjeu__yovyq, 1, 'C')
                    )(context, builder, arr.data)
                imaji__gav = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                xxe__vimv = builder.bitcast(pvzk__pnv.data, lir.IntType(8).
                    as_pointer())
                lqvq__jgu = builder.bitcast(imaji__gav.data, lir.IntType(8)
                    .as_pointer())
                msjlf__nww = cgutils.pack_array(builder, [lqvq__jgu, xxe__vimv]
                    )
            elif arr_typ in (string_array_type, binary_array_type):
                dxjsd__zrqeh = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                uert__rqhfd = context.make_helper(builder, offset_arr_type,
                    dxjsd__zrqeh.offsets).data
                llul__oqazv = context.make_helper(builder, char_arr_type,
                    dxjsd__zrqeh.data).data
                ijgae__jxd = context.make_helper(builder,
                    null_bitmap_arr_type, dxjsd__zrqeh.null_bitmap).data
                msjlf__nww = cgutils.pack_array(builder, [builder.bitcast(
                    uert__rqhfd, lir.IntType(8).as_pointer()), builder.
                    bitcast(ijgae__jxd, lir.IntType(8).as_pointer()),
                    builder.bitcast(llul__oqazv, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                xxe__vimv = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                ywszu__wmp = lir.Constant(lir.IntType(8).as_pointer(), None)
                msjlf__nww = cgutils.pack_array(builder, [ywszu__wmp,
                    xxe__vimv])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return msjlf__nww

        def get_field_names(arr_typ):
            ppzkn__obdqk = []
            if isinstance(arr_typ, StructArrayType):
                for rkt__ttqeb, ihkw__qtbr in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    ppzkn__obdqk.append(rkt__ttqeb)
                    ppzkn__obdqk += get_field_names(ihkw__qtbr)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ppzkn__obdqk += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                ppzkn__obdqk += get_field_names(_get_map_arr_data_type(arr_typ)
                    )
            return ppzkn__obdqk
        wvng__tya = get_types(arr_type)
        pqnfg__cks = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in wvng__tya])
        kas__npqad = cgutils.alloca_once_value(builder, pqnfg__cks)
        jlghn__aagz = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, jlghn__aagz)
        msjlf__nww = get_buffers(arr_type, in_arr)
        hqwin__mgulo = cgutils.alloca_once_value(builder, msjlf__nww)
        ppzkn__obdqk = get_field_names(arr_type)
        if len(ppzkn__obdqk) == 0:
            ppzkn__obdqk = ['irrelevant']
        noe__wnwvb = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in ppzkn__obdqk])
        kktok__qhu = cgutils.alloca_once_value(builder, noe__wnwvb)
        if isinstance(arr_type, MapArrayType):
            edtbo__zie = _get_map_arr_data_type(arr_type)
            tsbdy__gneb = context.make_helper(builder, arr_type, value=in_arr)
            xdc__ntnkd = tsbdy__gneb.data
        else:
            edtbo__zie = arr_type
            xdc__ntnkd = in_arr
        symx__yaje = context.make_helper(builder, edtbo__zie, xdc__ntnkd)
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='nested_array_to_info')
        jeohm__qjimo = builder.call(hoqb__mtyog, [builder.bitcast(
            kas__npqad, lir.IntType(32).as_pointer()), builder.bitcast(
            hqwin__mgulo, lir.IntType(8).as_pointer().as_pointer()),
            builder.bitcast(lengths_ptr, lir.IntType(64).as_pointer()),
            builder.bitcast(kktok__qhu, lir.IntType(8).as_pointer()),
            symx__yaje.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
    if arr_type in (string_array_type, binary_array_type):
        qeg__vyngo = context.make_helper(builder, arr_type, in_arr)
        cmxtk__hpkgi = ArrayItemArrayType(char_arr_type)
        fews__ozoo = context.make_helper(builder, cmxtk__hpkgi, qeg__vyngo.data
            )
        dxjsd__zrqeh = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        uert__rqhfd = context.make_helper(builder, offset_arr_type,
            dxjsd__zrqeh.offsets).data
        llul__oqazv = context.make_helper(builder, char_arr_type,
            dxjsd__zrqeh.data).data
        ijgae__jxd = context.make_helper(builder, null_bitmap_arr_type,
            dxjsd__zrqeh.null_bitmap).data
        abt__vlflg = builder.zext(builder.load(builder.gep(uert__rqhfd, [
            dxjsd__zrqeh.n_arrays])), lir.IntType(64))
        swa__ryczh = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='string_array_to_info')
        return builder.call(hoqb__mtyog, [dxjsd__zrqeh.n_arrays, abt__vlflg,
            llul__oqazv, uert__rqhfd, ijgae__jxd, fews__ozoo.meminfo,
            swa__ryczh])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        fpp__waoj = arr.data
        nrm__yuatt = arr.indices
        sig = array_info_type(arr_type.data)
        xwr__oytyr = array_to_info_codegen(context, builder, sig, (
            fpp__waoj,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        ikbmn__fez = array_to_info_codegen(context, builder, sig, (
            nrm__yuatt,), False)
        ppgh__qyl = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, nrm__yuatt)
        lqvq__jgu = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, ppgh__qyl.null_bitmap).data
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='dict_str_array_to_info')
        zsyt__arth = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(hoqb__mtyog, [xwr__oytyr, ikbmn__fez, builder.
            bitcast(lqvq__jgu, lir.IntType(8).as_pointer()), zsyt__arth])
    ohtkg__ndx = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        qeq__afshm = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        swtfy__xrllo = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(swtfy__xrllo, 1, 'C')
        ohtkg__ndx = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if ohtkg__ndx:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        klijk__ycuz = builder.extract_value(arr.shape, 0)
        dgkrv__nbl = arr_type.dtype
        xsdf__zil = numba_to_c_type(dgkrv__nbl)
        lxp__iozq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), xsdf__zil))
        if ohtkg__ndx:
            bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
                bwe__bkahb, name='categorical_array_to_info')
            return builder.call(hoqb__mtyog, [klijk__ycuz, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                lxp__iozq), qeq__afshm, arr.meminfo])
        else:
            bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
                bwe__bkahb, name='numpy_array_to_info')
            return builder.call(hoqb__mtyog, [klijk__ycuz, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                lxp__iozq), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        dgkrv__nbl = arr_type.dtype
        pjeu__yovyq = dgkrv__nbl
        if isinstance(arr_type, DecimalArrayType):
            pjeu__yovyq = int128_type
        if arr_type == datetime_date_array_type:
            pjeu__yovyq = types.int64
        pvzk__pnv = context.make_array(types.Array(pjeu__yovyq, 1, 'C'))(
            context, builder, arr.data)
        klijk__ycuz = builder.extract_value(pvzk__pnv.shape, 0)
        fdtt__fro = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        xsdf__zil = numba_to_c_type(dgkrv__nbl)
        lxp__iozq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), xsdf__zil))
        if isinstance(arr_type, DecimalArrayType):
            bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
                bwe__bkahb, name='decimal_array_to_info')
            return builder.call(hoqb__mtyog, [klijk__ycuz, builder.bitcast(
                pvzk__pnv.data, lir.IntType(8).as_pointer()), builder.load(
                lxp__iozq), builder.bitcast(fdtt__fro.data, lir.IntType(8).
                as_pointer()), pvzk__pnv.meminfo, fdtt__fro.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        else:
            bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
                bwe__bkahb, name='nullable_array_to_info')
            return builder.call(hoqb__mtyog, [klijk__ycuz, builder.bitcast(
                pvzk__pnv.data, lir.IntType(8).as_pointer()), builder.load(
                lxp__iozq), builder.bitcast(fdtt__fro.data, lir.IntType(8).
                as_pointer()), pvzk__pnv.meminfo, fdtt__fro.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        bgo__ghl = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        xwn__njlwl = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        klijk__ycuz = builder.extract_value(bgo__ghl.shape, 0)
        xsdf__zil = numba_to_c_type(arr_type.arr_type.dtype)
        lxp__iozq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), xsdf__zil))
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='interval_array_to_info')
        return builder.call(hoqb__mtyog, [klijk__ycuz, builder.bitcast(
            bgo__ghl.data, lir.IntType(8).as_pointer()), builder.bitcast(
            xwn__njlwl.data, lir.IntType(8).as_pointer()), builder.load(
            lxp__iozq), bgo__ghl.meminfo, xwn__njlwl.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    wmayl__yyk = cgutils.alloca_once(builder, lir.IntType(64))
    xxe__vimv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    axds__swbd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    hoqb__mtyog = cgutils.get_or_insert_function(builder.module, bwe__bkahb,
        name='info_to_numpy_array')
    builder.call(hoqb__mtyog, [in_info, wmayl__yyk, xxe__vimv, axds__swbd])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    ovha__ykjrp = context.get_value_type(types.intp)
    dpeus__ukzup = cgutils.pack_array(builder, [builder.load(wmayl__yyk)],
        ty=ovha__ykjrp)
    qfsq__khlt = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    pxnou__cjvuo = cgutils.pack_array(builder, [qfsq__khlt], ty=ovha__ykjrp)
    llul__oqazv = builder.bitcast(builder.load(xxe__vimv), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=llul__oqazv, shape=
        dpeus__ukzup, strides=pxnou__cjvuo, itemsize=qfsq__khlt, meminfo=
        builder.load(axds__swbd))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    lndii__sjo = context.make_helper(builder, arr_type)
    bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    hoqb__mtyog = cgutils.get_or_insert_function(builder.module, bwe__bkahb,
        name='info_to_list_string_array')
    builder.call(hoqb__mtyog, [in_info, lndii__sjo._get_ptr_by_name('meminfo')]
        )
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return lndii__sjo._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    vtuhz__qkf = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        pez__fybbb = lengths_pos
        typjk__crg = infos_pos
        azk__amidm, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        yiczp__smcp = ArrayItemArrayPayloadType(arr_typ)
        krrp__vxjtk = context.get_data_type(yiczp__smcp)
        jmrmo__kpvhm = context.get_abi_sizeof(krrp__vxjtk)
        rvv__lbhv = define_array_item_dtor(context, builder, arr_typ,
            yiczp__smcp)
        dvk__fmvo = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jmrmo__kpvhm), rvv__lbhv)
        rwnir__zlyrv = context.nrt.meminfo_data(builder, dvk__fmvo)
        szg__trcfk = builder.bitcast(rwnir__zlyrv, krrp__vxjtk.as_pointer())
        dxjsd__zrqeh = cgutils.create_struct_proxy(yiczp__smcp)(context,
            builder)
        dxjsd__zrqeh.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), pez__fybbb)
        dxjsd__zrqeh.data = azk__amidm
        fmmvg__zfy = builder.load(array_infos_ptr)
        cym__lkzk = builder.bitcast(builder.extract_value(fmmvg__zfy,
            typjk__crg), vtuhz__qkf)
        dxjsd__zrqeh.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, cym__lkzk)
        llth__ymp = builder.bitcast(builder.extract_value(fmmvg__zfy, 
            typjk__crg + 1), vtuhz__qkf)
        dxjsd__zrqeh.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, llth__ymp)
        builder.store(dxjsd__zrqeh._getvalue(), szg__trcfk)
        fews__ozoo = context.make_helper(builder, arr_typ)
        fews__ozoo.meminfo = dvk__fmvo
        return fews__ozoo._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        yrnw__ugl = []
        typjk__crg = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for ydrc__bkf in arr_typ.data:
            azk__amidm, lengths_pos, infos_pos = nested_to_array(context,
                builder, ydrc__bkf, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            yrnw__ugl.append(azk__amidm)
        yiczp__smcp = StructArrayPayloadType(arr_typ.data)
        krrp__vxjtk = context.get_value_type(yiczp__smcp)
        jmrmo__kpvhm = context.get_abi_sizeof(krrp__vxjtk)
        rvv__lbhv = define_struct_arr_dtor(context, builder, arr_typ,
            yiczp__smcp)
        dvk__fmvo = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jmrmo__kpvhm), rvv__lbhv)
        rwnir__zlyrv = context.nrt.meminfo_data(builder, dvk__fmvo)
        szg__trcfk = builder.bitcast(rwnir__zlyrv, krrp__vxjtk.as_pointer())
        dxjsd__zrqeh = cgutils.create_struct_proxy(yiczp__smcp)(context,
            builder)
        dxjsd__zrqeh.data = cgutils.pack_array(builder, yrnw__ugl
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, yrnw__ugl)
        fmmvg__zfy = builder.load(array_infos_ptr)
        llth__ymp = builder.bitcast(builder.extract_value(fmmvg__zfy,
            typjk__crg), vtuhz__qkf)
        dxjsd__zrqeh.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, llth__ymp)
        builder.store(dxjsd__zrqeh._getvalue(), szg__trcfk)
        hbwv__ynzta = context.make_helper(builder, arr_typ)
        hbwv__ynzta.meminfo = dvk__fmvo
        return hbwv__ynzta._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        fmmvg__zfy = builder.load(array_infos_ptr)
        awf__jpyrd = builder.bitcast(builder.extract_value(fmmvg__zfy,
            infos_pos), vtuhz__qkf)
        qeg__vyngo = context.make_helper(builder, arr_typ)
        cmxtk__hpkgi = ArrayItemArrayType(char_arr_type)
        fews__ozoo = context.make_helper(builder, cmxtk__hpkgi)
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_to_string_array')
        builder.call(hoqb__mtyog, [awf__jpyrd, fews__ozoo._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qeg__vyngo.data = fews__ozoo._getvalue()
        return qeg__vyngo._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        fmmvg__zfy = builder.load(array_infos_ptr)
        oatsf__vhf = builder.bitcast(builder.extract_value(fmmvg__zfy, 
            infos_pos + 1), vtuhz__qkf)
        return _lower_info_to_array_numpy(arr_typ, context, builder, oatsf__vhf
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        pjeu__yovyq = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            pjeu__yovyq = int128_type
        elif arr_typ == datetime_date_array_type:
            pjeu__yovyq = types.int64
        fmmvg__zfy = builder.load(array_infos_ptr)
        llth__ymp = builder.bitcast(builder.extract_value(fmmvg__zfy,
            infos_pos), vtuhz__qkf)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, llth__ymp)
        oatsf__vhf = builder.bitcast(builder.extract_value(fmmvg__zfy, 
            infos_pos + 1), vtuhz__qkf)
        arr.data = _lower_info_to_array_numpy(types.Array(pjeu__yovyq, 1,
            'C'), context, builder, oatsf__vhf)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, nai__mlzop = args
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
                return 1 + sum([get_num_arrays(ydrc__bkf) for ydrc__bkf in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(ydrc__bkf) for ydrc__bkf in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            xucc__ztse = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            xucc__ztse = _get_map_arr_data_type(arr_type)
        else:
            xucc__ztse = arr_type
        xidv__hkkmt = get_num_arrays(xucc__ztse)
        jlghn__aagz = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), 0) for nai__mlzop in range(xidv__hkkmt)])
        lengths_ptr = cgutils.alloca_once_value(builder, jlghn__aagz)
        ywszu__wmp = lir.Constant(lir.IntType(8).as_pointer(), None)
        hllj__oyp = cgutils.pack_array(builder, [ywszu__wmp for nai__mlzop in
            range(get_num_infos(xucc__ztse))])
        array_infos_ptr = cgutils.alloca_once_value(builder, hllj__oyp)
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_to_nested_array')
        builder.call(hoqb__mtyog, [in_info, builder.bitcast(lengths_ptr,
            lir.IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, nai__mlzop, nai__mlzop = nested_to_array(context, builder,
            xucc__ztse, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            yci__yxz = context.make_helper(builder, arr_type)
            yci__yxz.data = arr
            context.nrt.incref(builder, xucc__ztse, arr)
            arr = yci__yxz._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, xucc__ztse)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        qeg__vyngo = context.make_helper(builder, arr_type)
        cmxtk__hpkgi = ArrayItemArrayType(char_arr_type)
        fews__ozoo = context.make_helper(builder, cmxtk__hpkgi)
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_to_string_array')
        builder.call(hoqb__mtyog, [in_info, fews__ozoo._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qeg__vyngo.data = fews__ozoo._getvalue()
        return qeg__vyngo._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='get_nested_info')
        xwr__oytyr = builder.call(hoqb__mtyog, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        ikbmn__fez = builder.call(hoqb__mtyog, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        ntid__vmo = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        ntid__vmo.data = info_to_array_codegen(context, builder, sig, (
            xwr__oytyr, context.get_constant_null(arr_type.data)))
        rbrof__zmkzd = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = rbrof__zmkzd(array_info_type, rbrof__zmkzd)
        ntid__vmo.indices = info_to_array_codegen(context, builder, sig, (
            ikbmn__fez, context.get_constant_null(rbrof__zmkzd)))
        bwe__bkahb = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='get_has_global_dictionary')
        zsyt__arth = builder.call(hoqb__mtyog, [in_info])
        ntid__vmo.has_global_dictionary = builder.trunc(zsyt__arth, cgutils
            .bool_t)
        return ntid__vmo._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        swtfy__xrllo = get_categories_int_type(arr_type.dtype)
        szkf__vftu = types.Array(swtfy__xrllo, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(szkf__vftu, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            hmr__uen = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(hmr__uen))
            int_type = arr_type.dtype.int_type
            dxfvk__rqx = bodo.typeof(hmr__uen)
            cmpt__dcpq = context.get_constant_generic(builder, dxfvk__rqx,
                hmr__uen)
            dgkrv__nbl = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(dxfvk__rqx), [cmpt__dcpq])
        else:
            dgkrv__nbl = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, dgkrv__nbl)
        out_arr.dtype = dgkrv__nbl
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        llul__oqazv = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = llul__oqazv
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        pjeu__yovyq = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            pjeu__yovyq = int128_type
        elif arr_type == datetime_date_array_type:
            pjeu__yovyq = types.int64
        qeit__tivq = types.Array(pjeu__yovyq, 1, 'C')
        pvzk__pnv = context.make_array(qeit__tivq)(context, builder)
        agbvd__fghrg = types.Array(types.uint8, 1, 'C')
        gsfi__alz = context.make_array(agbvd__fghrg)(context, builder)
        wmayl__yyk = cgutils.alloca_once(builder, lir.IntType(64))
        rgjyj__wpt = cgutils.alloca_once(builder, lir.IntType(64))
        xxe__vimv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        gwylp__frcq = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        axds__swbd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        kgwwn__lfkb = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_to_nullable_array')
        builder.call(hoqb__mtyog, [in_info, wmayl__yyk, rgjyj__wpt,
            xxe__vimv, gwylp__frcq, axds__swbd, kgwwn__lfkb])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ovha__ykjrp = context.get_value_type(types.intp)
        dpeus__ukzup = cgutils.pack_array(builder, [builder.load(wmayl__yyk
            )], ty=ovha__ykjrp)
        qfsq__khlt = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(pjeu__yovyq)))
        pxnou__cjvuo = cgutils.pack_array(builder, [qfsq__khlt], ty=ovha__ykjrp
            )
        llul__oqazv = builder.bitcast(builder.load(xxe__vimv), context.
            get_data_type(pjeu__yovyq).as_pointer())
        numba.np.arrayobj.populate_array(pvzk__pnv, data=llul__oqazv, shape
            =dpeus__ukzup, strides=pxnou__cjvuo, itemsize=qfsq__khlt,
            meminfo=builder.load(axds__swbd))
        arr.data = pvzk__pnv._getvalue()
        dpeus__ukzup = cgutils.pack_array(builder, [builder.load(rgjyj__wpt
            )], ty=ovha__ykjrp)
        qfsq__khlt = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        pxnou__cjvuo = cgutils.pack_array(builder, [qfsq__khlt], ty=ovha__ykjrp
            )
        llul__oqazv = builder.bitcast(builder.load(gwylp__frcq), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(gsfi__alz, data=llul__oqazv, shape
            =dpeus__ukzup, strides=pxnou__cjvuo, itemsize=qfsq__khlt,
            meminfo=builder.load(kgwwn__lfkb))
        arr.null_bitmap = gsfi__alz._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        bgo__ghl = context.make_array(arr_type.arr_type)(context, builder)
        xwn__njlwl = context.make_array(arr_type.arr_type)(context, builder)
        wmayl__yyk = cgutils.alloca_once(builder, lir.IntType(64))
        fyyd__xxze = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        glfny__rbksx = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        tqq__pcnyw = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        uwdod__zouz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_to_interval_array')
        builder.call(hoqb__mtyog, [in_info, wmayl__yyk, fyyd__xxze,
            glfny__rbksx, tqq__pcnyw, uwdod__zouz])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ovha__ykjrp = context.get_value_type(types.intp)
        dpeus__ukzup = cgutils.pack_array(builder, [builder.load(wmayl__yyk
            )], ty=ovha__ykjrp)
        qfsq__khlt = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        pxnou__cjvuo = cgutils.pack_array(builder, [qfsq__khlt], ty=ovha__ykjrp
            )
        qpx__ofbvd = builder.bitcast(builder.load(fyyd__xxze), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(bgo__ghl, data=qpx__ofbvd, shape=
            dpeus__ukzup, strides=pxnou__cjvuo, itemsize=qfsq__khlt,
            meminfo=builder.load(tqq__pcnyw))
        arr.left = bgo__ghl._getvalue()
        buif__pfu = builder.bitcast(builder.load(glfny__rbksx), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(xwn__njlwl, data=buif__pfu, shape=
            dpeus__ukzup, strides=pxnou__cjvuo, itemsize=qfsq__khlt,
            meminfo=builder.load(uwdod__zouz))
        arr.right = xwn__njlwl._getvalue()
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
        klijk__ycuz, nai__mlzop = args
        xsdf__zil = numba_to_c_type(array_type.dtype)
        lxp__iozq = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), xsdf__zil))
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='alloc_numpy')
        return builder.call(hoqb__mtyog, [klijk__ycuz, builder.load(lxp__iozq)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        klijk__ycuz, aiypn__kom = args
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='alloc_string_array')
        return builder.call(hoqb__mtyog, [klijk__ycuz, aiypn__kom])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    qxyu__dumao, = args
    jmjju__cumxu = numba.cpython.listobj.ListInstance(context, builder, sig
        .args[0], qxyu__dumao)
    bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer().as_pointer(), lir.IntType(64)])
    hoqb__mtyog = cgutils.get_or_insert_function(builder.module, bwe__bkahb,
        name='arr_info_list_to_table')
    return builder.call(hoqb__mtyog, [jmjju__cumxu.data, jmjju__cumxu.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_from_table')
        return builder.call(hoqb__mtyog, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    qbnl__xag = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        canw__yzw, agvk__hjq, nai__mlzop = args
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='info_from_table')
        atrhc__jqf = cgutils.create_struct_proxy(qbnl__xag)(context, builder)
        atrhc__jqf.parent = cgutils.get_null_value(atrhc__jqf.parent.type)
        umfmx__aba = context.make_array(table_idx_arr_t)(context, builder,
            agvk__hjq)
        bhax__azxf = context.get_constant(types.int64, -1)
        vaan__abjwz = context.get_constant(types.int64, 0)
        wbwlm__zgauh = cgutils.alloca_once_value(builder, vaan__abjwz)
        for t, gjin__youds in qbnl__xag.type_to_blk.items():
            mfcte__nlws = context.get_constant(types.int64, len(qbnl__xag.
                block_to_arr_ind[gjin__youds]))
            nai__mlzop, bgtuj__gvzcx = ListInstance.allocate_ex(context,
                builder, types.List(t), mfcte__nlws)
            bgtuj__gvzcx.size = mfcte__nlws
            oct__qcknj = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(qbnl__xag.block_to_arr_ind[
                gjin__youds], dtype=np.int64))
            fmx__uokgg = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, oct__qcknj)
            with cgutils.for_range(builder, mfcte__nlws) as agon__qemoq:
                aps__kbs = agon__qemoq.index
                zxtmu__jbr = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    fmx__uokgg, aps__kbs)
                sjw__qpka = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, umfmx__aba, zxtmu__jbr)
                cdn__rwcfo = builder.icmp_unsigned('!=', sjw__qpka, bhax__azxf)
                with builder.if_else(cdn__rwcfo) as (sva__blen, eqrcp__tmnqz):
                    with sva__blen:
                        xihed__dixmx = builder.call(hoqb__mtyog, [canw__yzw,
                            sjw__qpka])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            xihed__dixmx])
                        bgtuj__gvzcx.inititem(aps__kbs, arr, incref=False)
                        klijk__ycuz = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(klijk__ycuz, wbwlm__zgauh)
                    with eqrcp__tmnqz:
                        nbuoo__zpeao = context.get_constant_null(t)
                        bgtuj__gvzcx.inititem(aps__kbs, nbuoo__zpeao,
                            incref=False)
            setattr(atrhc__jqf, f'block_{gjin__youds}', bgtuj__gvzcx.value)
        atrhc__jqf.len = builder.load(wbwlm__zgauh)
        return atrhc__jqf._getvalue()
    return qbnl__xag(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    qbnl__xag = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        mzhf__mun, nai__mlzop = args
        getl__uglim = cgutils.create_struct_proxy(qbnl__xag)(context,
            builder, mzhf__mun)
        if qbnl__xag.has_runtime_cols:
            lou__igzze = lir.Constant(lir.IntType(64), 0)
            for gjin__youds, t in enumerate(qbnl__xag.arr_types):
                dpz__pmud = getattr(getl__uglim, f'block_{gjin__youds}')
                jar__heyk = ListInstance(context, builder, types.List(t),
                    dpz__pmud)
                lou__igzze = builder.add(lou__igzze, jar__heyk.size)
        else:
            lou__igzze = lir.Constant(lir.IntType(64), len(qbnl__xag.arr_types)
                )
        nai__mlzop, evqyc__guof = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), lou__igzze)
        evqyc__guof.size = lou__igzze
        if qbnl__xag.has_runtime_cols:
            njgc__dbbeh = lir.Constant(lir.IntType(64), 0)
            for gjin__youds, t in enumerate(qbnl__xag.arr_types):
                dpz__pmud = getattr(getl__uglim, f'block_{gjin__youds}')
                jar__heyk = ListInstance(context, builder, types.List(t),
                    dpz__pmud)
                mfcte__nlws = jar__heyk.size
                with cgutils.for_range(builder, mfcte__nlws) as agon__qemoq:
                    aps__kbs = agon__qemoq.index
                    arr = jar__heyk.getitem(aps__kbs)
                    iitjf__rzuk = signature(array_info_type, t)
                    aoksw__epwa = arr,
                    zzqwt__usn = array_to_info_codegen(context, builder,
                        iitjf__rzuk, aoksw__epwa)
                    evqyc__guof.inititem(builder.add(njgc__dbbeh, aps__kbs),
                        zzqwt__usn, incref=False)
                njgc__dbbeh = builder.add(njgc__dbbeh, mfcte__nlws)
        else:
            for t, gjin__youds in qbnl__xag.type_to_blk.items():
                mfcte__nlws = context.get_constant(types.int64, len(
                    qbnl__xag.block_to_arr_ind[gjin__youds]))
                dpz__pmud = getattr(getl__uglim, f'block_{gjin__youds}')
                jar__heyk = ListInstance(context, builder, types.List(t),
                    dpz__pmud)
                oct__qcknj = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(qbnl__xag.
                    block_to_arr_ind[gjin__youds], dtype=np.int64))
                fmx__uokgg = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, oct__qcknj)
                with cgutils.for_range(builder, mfcte__nlws) as agon__qemoq:
                    aps__kbs = agon__qemoq.index
                    zxtmu__jbr = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        fmx__uokgg, aps__kbs)
                    wtymz__sgvzr = signature(types.none, qbnl__xag, types.
                        List(t), types.int64, types.int64)
                    cdiso__jyeai = mzhf__mun, dpz__pmud, aps__kbs, zxtmu__jbr
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, wtymz__sgvzr, cdiso__jyeai)
                    arr = jar__heyk.getitem(aps__kbs)
                    iitjf__rzuk = signature(array_info_type, t)
                    aoksw__epwa = arr,
                    zzqwt__usn = array_to_info_codegen(context, builder,
                        iitjf__rzuk, aoksw__epwa)
                    evqyc__guof.inititem(zxtmu__jbr, zzqwt__usn, incref=False)
        xdeq__tvm = evqyc__guof.value
        uwya__gxo = signature(table_type, types.List(array_info_type))
        piic__ubx = xdeq__tvm,
        canw__yzw = arr_info_list_to_table_codegen(context, builder,
            uwya__gxo, piic__ubx)
        context.nrt.decref(builder, types.List(array_info_type), xdeq__tvm)
        return canw__yzw
    return table_type(qbnl__xag, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='delete_table')
        builder.call(hoqb__mtyog, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='shuffle_table')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
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
        bwe__bkahb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='delete_shuffle_info')
        return builder.call(hoqb__mtyog, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='reverse_shuffle_table')
        return builder.call(hoqb__mtyog, args)
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
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='hash_join_table')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
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
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='sort_values_table')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='sample_table')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='shuffle_renormalization')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='shuffle_renormalization_group')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='drop_duplicates_table')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
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
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='pivot_groupby_and_aggregate')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
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
        bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        hoqb__mtyog = cgutils.get_or_insert_function(builder.module,
            bwe__bkahb, name='groupby_and_aggregate')
        jeohm__qjimo = builder.call(hoqb__mtyog, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return jeohm__qjimo
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
    wcosg__ffxr = array_to_info(in_arr)
    wogm__cmx = array_to_info(in_values)
    zlfg__fet = array_to_info(out_arr)
    xhkiu__azbs = arr_info_list_to_table([wcosg__ffxr, wogm__cmx, zlfg__fet])
    _array_isin(zlfg__fet, wcosg__ffxr, wogm__cmx, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(xhkiu__azbs)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    wcosg__ffxr = array_to_info(in_arr)
    zlfg__fet = array_to_info(out_arr)
    _get_search_regex(wcosg__ffxr, case, pat, zlfg__fet)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    slka__uwr = col_array_typ.dtype
    if isinstance(slka__uwr, types.Number) or slka__uwr in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                atrhc__jqf, wcj__mev = args
                atrhc__jqf = builder.bitcast(atrhc__jqf, lir.IntType(8).
                    as_pointer().as_pointer())
                brpqx__pupw = lir.Constant(lir.IntType(64), c_ind)
                dnyia__zqoy = builder.load(builder.gep(atrhc__jqf, [
                    brpqx__pupw]))
                dnyia__zqoy = builder.bitcast(dnyia__zqoy, context.
                    get_data_type(slka__uwr).as_pointer())
                return builder.load(builder.gep(dnyia__zqoy, [wcj__mev]))
            return slka__uwr(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                atrhc__jqf, wcj__mev = args
                atrhc__jqf = builder.bitcast(atrhc__jqf, lir.IntType(8).
                    as_pointer().as_pointer())
                brpqx__pupw = lir.Constant(lir.IntType(64), c_ind)
                dnyia__zqoy = builder.load(builder.gep(atrhc__jqf, [
                    brpqx__pupw]))
                bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                qbnfd__qity = cgutils.get_or_insert_function(builder.module,
                    bwe__bkahb, name='array_info_getitem')
                fdtlr__quqg = cgutils.alloca_once(builder, lir.IntType(64))
                args = dnyia__zqoy, wcj__mev, fdtlr__quqg
                xxe__vimv = builder.call(qbnfd__qity, args)
                return context.make_tuple(builder, sig.return_type, [
                    xxe__vimv, builder.load(fdtlr__quqg)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                wvdv__xzy = lir.Constant(lir.IntType(64), 1)
                ulfvt__tic = lir.Constant(lir.IntType(64), 2)
                atrhc__jqf, wcj__mev = args
                atrhc__jqf = builder.bitcast(atrhc__jqf, lir.IntType(8).
                    as_pointer().as_pointer())
                brpqx__pupw = lir.Constant(lir.IntType(64), c_ind)
                dnyia__zqoy = builder.load(builder.gep(atrhc__jqf, [
                    brpqx__pupw]))
                bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                tlyji__nek = cgutils.get_or_insert_function(builder.module,
                    bwe__bkahb, name='get_nested_info')
                args = dnyia__zqoy, ulfvt__tic
                lpp__qxfd = builder.call(tlyji__nek, args)
                bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                oph__kzrc = cgutils.get_or_insert_function(builder.module,
                    bwe__bkahb, name='array_info_getdata1')
                args = lpp__qxfd,
                xkct__rusmk = builder.call(oph__kzrc, args)
                xkct__rusmk = builder.bitcast(xkct__rusmk, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                ncjw__oprb = builder.sext(builder.load(builder.gep(
                    xkct__rusmk, [wcj__mev])), lir.IntType(64))
                args = dnyia__zqoy, wvdv__xzy
                dcfv__vyi = builder.call(tlyji__nek, args)
                bwe__bkahb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                qbnfd__qity = cgutils.get_or_insert_function(builder.module,
                    bwe__bkahb, name='array_info_getitem')
                fdtlr__quqg = cgutils.alloca_once(builder, lir.IntType(64))
                args = dcfv__vyi, ncjw__oprb, fdtlr__quqg
                xxe__vimv = builder.call(qbnfd__qity, args)
                return context.make_tuple(builder, sig.return_type, [
                    xxe__vimv, builder.load(fdtlr__quqg)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{slka__uwr}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                iwv__vhrz, wcj__mev = args
                iwv__vhrz = builder.bitcast(iwv__vhrz, lir.IntType(8).
                    as_pointer().as_pointer())
                brpqx__pupw = lir.Constant(lir.IntType(64), c_ind)
                dnyia__zqoy = builder.load(builder.gep(iwv__vhrz, [
                    brpqx__pupw]))
                ijgae__jxd = builder.bitcast(dnyia__zqoy, context.
                    get_data_type(types.bool_).as_pointer())
                oqnvu__noc = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ijgae__jxd, wcj__mev)
                jcxyr__meg = builder.icmp_unsigned('!=', oqnvu__noc, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(jcxyr__meg, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        slka__uwr = col_array_dtype.dtype
        if slka__uwr in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    atrhc__jqf, wcj__mev = args
                    atrhc__jqf = builder.bitcast(atrhc__jqf, lir.IntType(8)
                        .as_pointer().as_pointer())
                    brpqx__pupw = lir.Constant(lir.IntType(64), c_ind)
                    dnyia__zqoy = builder.load(builder.gep(atrhc__jqf, [
                        brpqx__pupw]))
                    dnyia__zqoy = builder.bitcast(dnyia__zqoy, context.
                        get_data_type(slka__uwr).as_pointer())
                    wgxk__xfmqj = builder.load(builder.gep(dnyia__zqoy, [
                        wcj__mev]))
                    jcxyr__meg = builder.icmp_unsigned('!=', wgxk__xfmqj,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(jcxyr__meg, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(slka__uwr, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    atrhc__jqf, wcj__mev = args
                    atrhc__jqf = builder.bitcast(atrhc__jqf, lir.IntType(8)
                        .as_pointer().as_pointer())
                    brpqx__pupw = lir.Constant(lir.IntType(64), c_ind)
                    dnyia__zqoy = builder.load(builder.gep(atrhc__jqf, [
                        brpqx__pupw]))
                    dnyia__zqoy = builder.bitcast(dnyia__zqoy, context.
                        get_data_type(slka__uwr).as_pointer())
                    wgxk__xfmqj = builder.load(builder.gep(dnyia__zqoy, [
                        wcj__mev]))
                    lnjbv__axjp = signature(types.bool_, slka__uwr)
                    oqnvu__noc = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, lnjbv__axjp, (wgxk__xfmqj,))
                    return builder.not_(builder.sext(oqnvu__noc, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
