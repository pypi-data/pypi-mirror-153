"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    wmter__ifyu = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(wmter__ifyu)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ddf__qft = _get_map_arr_data_type(fe_type)
        brx__hkg = [('data', ddf__qft)]
        models.StructModel.__init__(self, dmm, fe_type, brx__hkg)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    ibs__djnay = all(isinstance(lqy__jji, types.Array) and lqy__jji.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        lqy__jji in (typ.key_arr_type, typ.value_arr_type))
    if ibs__djnay:
        qbud__rilrc = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        adl__ndfrg = cgutils.get_or_insert_function(c.builder.module,
            qbud__rilrc, name='count_total_elems_list_array')
        zrfek__elr = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            adl__ndfrg, [val])])
    else:
        zrfek__elr = get_array_elem_counts(c, c.builder, c.context, val, typ)
    ddf__qft = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, ddf__qft, zrfek__elr, c
        )
    lzwy__rsyht = _get_array_item_arr_payload(c.context, c.builder,
        ddf__qft, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, lzwy__rsyht.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, lzwy__rsyht.offsets).data
    pkndo__uxuwh = _get_struct_arr_payload(c.context, c.builder, ddf__qft.
        dtype, lzwy__rsyht.data)
    key_arr = c.builder.extract_value(pkndo__uxuwh.data, 0)
    value_arr = c.builder.extract_value(pkndo__uxuwh.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    dop__amz, ohti__swtoc = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [pkndo__uxuwh.null_bitmap])
    if ibs__djnay:
        reklj__vji = c.context.make_array(ddf__qft.dtype.data[0])(c.context,
            c.builder, key_arr).data
        bbxmd__eyq = c.context.make_array(ddf__qft.dtype.data[1])(c.context,
            c.builder, value_arr).data
        qbud__rilrc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        frhde__xfxs = cgutils.get_or_insert_function(c.builder.module,
            qbud__rilrc, name='map_array_from_sequence')
        fdj__oxmtc = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        cioa__ftudo = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        c.builder.call(frhde__xfxs, [val, c.builder.bitcast(reklj__vji, lir
            .IntType(8).as_pointer()), c.builder.bitcast(bbxmd__eyq, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), fdj__oxmtc), lir.Constant(lir.IntType
            (32), cioa__ftudo)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    gdfmu__xhs = c.context.make_helper(c.builder, typ)
    gdfmu__xhs.data = data_arr
    mlvtz__flsc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gdfmu__xhs._getvalue(), is_error=mlvtz__flsc)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    abymn__gysw = context.insert_const_string(builder.module, 'pandas')
    sqwn__toil = c.pyapi.import_module_noblock(abymn__gysw)
    htc__hylss = c.pyapi.object_getattr_string(sqwn__toil, 'NA')
    hfndi__xcnoe = c.context.get_constant(offset_type, 0)
    builder.store(hfndi__xcnoe, offsets_ptr)
    hsl__fsut = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as pjl__wept:
        wiy__mab = pjl__wept.index
        item_ind = builder.load(hsl__fsut)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [wiy__mab]))
        gcv__vchpy = seq_getitem(builder, context, val, wiy__mab)
        set_bitmap_bit(builder, null_bitmap_ptr, wiy__mab, 0)
        hrx__uafgg = is_na_value(builder, context, gcv__vchpy, htc__hylss)
        ngkje__bcms = builder.icmp_unsigned('!=', hrx__uafgg, lir.Constant(
            hrx__uafgg.type, 1))
        with builder.if_then(ngkje__bcms):
            set_bitmap_bit(builder, null_bitmap_ptr, wiy__mab, 1)
            lttn__aqii = dict_keys(builder, context, gcv__vchpy)
            cpzu__yox = dict_values(builder, context, gcv__vchpy)
            n_items = bodo.utils.utils.object_length(c, lttn__aqii)
            _unbox_array_item_array_copy_data(typ.key_arr_type, lttn__aqii,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, cpzu__yox,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), hsl__fsut)
            c.pyapi.decref(lttn__aqii)
            c.pyapi.decref(cpzu__yox)
        c.pyapi.decref(gcv__vchpy)
    builder.store(builder.trunc(builder.load(hsl__fsut), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(sqwn__toil)
    c.pyapi.decref(htc__hylss)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    gdfmu__xhs = c.context.make_helper(c.builder, typ, val)
    data_arr = gdfmu__xhs.data
    ddf__qft = _get_map_arr_data_type(typ)
    lzwy__rsyht = _get_array_item_arr_payload(c.context, c.builder,
        ddf__qft, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, lzwy__rsyht.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, lzwy__rsyht.offsets).data
    pkndo__uxuwh = _get_struct_arr_payload(c.context, c.builder, ddf__qft.
        dtype, lzwy__rsyht.data)
    key_arr = c.builder.extract_value(pkndo__uxuwh.data, 0)
    value_arr = c.builder.extract_value(pkndo__uxuwh.data, 1)
    if all(isinstance(lqy__jji, types.Array) and lqy__jji.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type) for lqy__jji in
        (typ.key_arr_type, typ.value_arr_type)):
        reklj__vji = c.context.make_array(ddf__qft.dtype.data[0])(c.context,
            c.builder, key_arr).data
        bbxmd__eyq = c.context.make_array(ddf__qft.dtype.data[1])(c.context,
            c.builder, value_arr).data
        qbud__rilrc = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        mdpf__stwv = cgutils.get_or_insert_function(c.builder.module,
            qbud__rilrc, name='np_array_from_map_array')
        fdj__oxmtc = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        cioa__ftudo = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        arr = c.builder.call(mdpf__stwv, [lzwy__rsyht.n_arrays, c.builder.
            bitcast(reklj__vji, lir.IntType(8).as_pointer()), c.builder.
            bitcast(bbxmd__eyq, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), fdj__oxmtc), lir
            .Constant(lir.IntType(32), cioa__ftudo)])
    else:
        arr = _box_map_array_generic(typ, c, lzwy__rsyht.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    abymn__gysw = context.insert_const_string(builder.module, 'numpy')
    awnp__mupmu = c.pyapi.import_module_noblock(abymn__gysw)
    csvnc__bcmvo = c.pyapi.object_getattr_string(awnp__mupmu, 'object_')
    qznl__xqd = c.pyapi.long_from_longlong(n_maps)
    nimyi__nexvm = c.pyapi.call_method(awnp__mupmu, 'ndarray', (qznl__xqd,
        csvnc__bcmvo))
    sphig__cusml = c.pyapi.object_getattr_string(awnp__mupmu, 'nan')
    ama__kqk = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    hsl__fsut = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_maps) as pjl__wept:
        tolx__bvcne = pjl__wept.index
        pyarray_setitem(builder, context, nimyi__nexvm, tolx__bvcne,
            sphig__cusml)
        sepn__iednx = get_bitmap_bit(builder, null_bitmap_ptr, tolx__bvcne)
        njbh__fhy = builder.icmp_unsigned('!=', sepn__iednx, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(njbh__fhy):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(tolx__bvcne, lir.Constant(
                tolx__bvcne.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [tolx__bvcne]))), lir.IntType(64))
            item_ind = builder.load(hsl__fsut)
            gcv__vchpy = c.pyapi.dict_new()
            pmeb__esyw = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            dop__amz, ept__dlny = c.pyapi.call_jit_code(pmeb__esyw, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            dop__amz, pykam__rgzxq = c.pyapi.call_jit_code(pmeb__esyw, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            ersr__ttvmk = c.pyapi.from_native_value(typ.key_arr_type,
                ept__dlny, c.env_manager)
            obwnb__kem = c.pyapi.from_native_value(typ.value_arr_type,
                pykam__rgzxq, c.env_manager)
            aeo__lmw = c.pyapi.call_function_objargs(ama__kqk, (ersr__ttvmk,
                obwnb__kem))
            dict_merge_from_seq2(builder, context, gcv__vchpy, aeo__lmw)
            builder.store(builder.add(item_ind, n_items), hsl__fsut)
            pyarray_setitem(builder, context, nimyi__nexvm, tolx__bvcne,
                gcv__vchpy)
            c.pyapi.decref(aeo__lmw)
            c.pyapi.decref(ersr__ttvmk)
            c.pyapi.decref(obwnb__kem)
            c.pyapi.decref(gcv__vchpy)
    c.pyapi.decref(ama__kqk)
    c.pyapi.decref(awnp__mupmu)
    c.pyapi.decref(csvnc__bcmvo)
    c.pyapi.decref(qznl__xqd)
    c.pyapi.decref(sphig__cusml)
    return nimyi__nexvm


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    gdfmu__xhs = context.make_helper(builder, sig.return_type)
    gdfmu__xhs.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return gdfmu__xhs._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    bxcg__qgnqw = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return bxcg__qgnqw(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    ewznz__eneg = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(ewznz__eneg)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    txdf__qar = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            texs__bfozy = val.keys()
            ksmi__clyv = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), txdf__qar, ('key', 'value'))
            for piw__zmiy, jsypl__pkvn in enumerate(texs__bfozy):
                ksmi__clyv[piw__zmiy] = bodo.libs.struct_arr_ext.init_struct((
                    jsypl__pkvn, val[jsypl__pkvn]), ('key', 'value'))
            arr._data[ind] = ksmi__clyv
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            jwbev__lpmkl = dict()
            tgag__nndw = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            ksmi__clyv = bodo.libs.array_item_arr_ext.get_data(arr._data)
            kfq__wvhp, ujwp__cwfh = bodo.libs.struct_arr_ext.get_data(
                ksmi__clyv)
            ohlqn__ltur = tgag__nndw[ind]
            eug__zpa = tgag__nndw[ind + 1]
            for piw__zmiy in range(ohlqn__ltur, eug__zpa):
                jwbev__lpmkl[kfq__wvhp[piw__zmiy]] = ujwp__cwfh[piw__zmiy]
            return jwbev__lpmkl
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
