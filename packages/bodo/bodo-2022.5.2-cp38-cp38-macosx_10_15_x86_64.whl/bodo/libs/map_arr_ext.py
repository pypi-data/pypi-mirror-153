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
    jfgjm__szqna = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(jfgjm__szqna)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oxfw__apdjm = _get_map_arr_data_type(fe_type)
        rmx__pmoa = [('data', oxfw__apdjm)]
        models.StructModel.__init__(self, dmm, fe_type, rmx__pmoa)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    rxy__ooclk = all(isinstance(maqoq__vsu, types.Array) and maqoq__vsu.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for maqoq__vsu in (typ.key_arr_type, typ.
        value_arr_type))
    if rxy__ooclk:
        ctbne__xsnna = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        cmgu__wgsou = cgutils.get_or_insert_function(c.builder.module,
            ctbne__xsnna, name='count_total_elems_list_array')
        ffj__qqn = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            cmgu__wgsou, [val])])
    else:
        ffj__qqn = get_array_elem_counts(c, c.builder, c.context, val, typ)
    oxfw__apdjm = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, oxfw__apdjm,
        ffj__qqn, c)
    rte__kqi = _get_array_item_arr_payload(c.context, c.builder,
        oxfw__apdjm, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, rte__kqi.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, rte__kqi.offsets).data
    uik__qqgxq = _get_struct_arr_payload(c.context, c.builder, oxfw__apdjm.
        dtype, rte__kqi.data)
    key_arr = c.builder.extract_value(uik__qqgxq.data, 0)
    value_arr = c.builder.extract_value(uik__qqgxq.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    jdk__ohstu, jnljo__haaz = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [uik__qqgxq.null_bitmap])
    if rxy__ooclk:
        rwt__fhe = c.context.make_array(oxfw__apdjm.dtype.data[0])(c.
            context, c.builder, key_arr).data
        dxq__jmtr = c.context.make_array(oxfw__apdjm.dtype.data[1])(c.
            context, c.builder, value_arr).data
        ctbne__xsnna = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        ufrp__oykx = cgutils.get_or_insert_function(c.builder.module,
            ctbne__xsnna, name='map_array_from_sequence')
        qvry__rhcd = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        wrcvf__rmvos = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.
            dtype)
        c.builder.call(ufrp__oykx, [val, c.builder.bitcast(rwt__fhe, lir.
            IntType(8).as_pointer()), c.builder.bitcast(dxq__jmtr, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), qvry__rhcd), lir.Constant(lir.IntType
            (32), wrcvf__rmvos)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    ffpsn__rbys = c.context.make_helper(c.builder, typ)
    ffpsn__rbys.data = data_arr
    mhk__tghr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ffpsn__rbys._getvalue(), is_error=mhk__tghr)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    dby__gyrb = context.insert_const_string(builder.module, 'pandas')
    wtba__aux = c.pyapi.import_module_noblock(dby__gyrb)
    xtyz__gvk = c.pyapi.object_getattr_string(wtba__aux, 'NA')
    eka__rjqi = c.context.get_constant(offset_type, 0)
    builder.store(eka__rjqi, offsets_ptr)
    gei__tnh = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as otpvj__vyrq:
        zqrc__wzj = otpvj__vyrq.index
        item_ind = builder.load(gei__tnh)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [zqrc__wzj]))
        xnh__djg = seq_getitem(builder, context, val, zqrc__wzj)
        set_bitmap_bit(builder, null_bitmap_ptr, zqrc__wzj, 0)
        miu__kgz = is_na_value(builder, context, xnh__djg, xtyz__gvk)
        drowk__nfwg = builder.icmp_unsigned('!=', miu__kgz, lir.Constant(
            miu__kgz.type, 1))
        with builder.if_then(drowk__nfwg):
            set_bitmap_bit(builder, null_bitmap_ptr, zqrc__wzj, 1)
            yvf__wwxjh = dict_keys(builder, context, xnh__djg)
            mnpnr__dquxy = dict_values(builder, context, xnh__djg)
            n_items = bodo.utils.utils.object_length(c, yvf__wwxjh)
            _unbox_array_item_array_copy_data(typ.key_arr_type, yvf__wwxjh,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                mnpnr__dquxy, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), gei__tnh)
            c.pyapi.decref(yvf__wwxjh)
            c.pyapi.decref(mnpnr__dquxy)
        c.pyapi.decref(xnh__djg)
    builder.store(builder.trunc(builder.load(gei__tnh), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(wtba__aux)
    c.pyapi.decref(xtyz__gvk)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    ffpsn__rbys = c.context.make_helper(c.builder, typ, val)
    data_arr = ffpsn__rbys.data
    oxfw__apdjm = _get_map_arr_data_type(typ)
    rte__kqi = _get_array_item_arr_payload(c.context, c.builder,
        oxfw__apdjm, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, rte__kqi.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, rte__kqi.offsets).data
    uik__qqgxq = _get_struct_arr_payload(c.context, c.builder, oxfw__apdjm.
        dtype, rte__kqi.data)
    key_arr = c.builder.extract_value(uik__qqgxq.data, 0)
    value_arr = c.builder.extract_value(uik__qqgxq.data, 1)
    if all(isinstance(maqoq__vsu, types.Array) and maqoq__vsu.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        maqoq__vsu in (typ.key_arr_type, typ.value_arr_type)):
        rwt__fhe = c.context.make_array(oxfw__apdjm.dtype.data[0])(c.
            context, c.builder, key_arr).data
        dxq__jmtr = c.context.make_array(oxfw__apdjm.dtype.data[1])(c.
            context, c.builder, value_arr).data
        ctbne__xsnna = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        bxzeh__xyyim = cgutils.get_or_insert_function(c.builder.module,
            ctbne__xsnna, name='np_array_from_map_array')
        qvry__rhcd = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        wrcvf__rmvos = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.
            dtype)
        arr = c.builder.call(bxzeh__xyyim, [rte__kqi.n_arrays, c.builder.
            bitcast(rwt__fhe, lir.IntType(8).as_pointer()), c.builder.
            bitcast(dxq__jmtr, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), qvry__rhcd), lir
            .Constant(lir.IntType(32), wrcvf__rmvos)])
    else:
        arr = _box_map_array_generic(typ, c, rte__kqi.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    dby__gyrb = context.insert_const_string(builder.module, 'numpy')
    lflbe__nosm = c.pyapi.import_module_noblock(dby__gyrb)
    xnd__xkkf = c.pyapi.object_getattr_string(lflbe__nosm, 'object_')
    nqv__vtbu = c.pyapi.long_from_longlong(n_maps)
    guvzx__lakg = c.pyapi.call_method(lflbe__nosm, 'ndarray', (nqv__vtbu,
        xnd__xkkf))
    syj__yhexl = c.pyapi.object_getattr_string(lflbe__nosm, 'nan')
    twj__dbkv = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    gei__tnh = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        64), 0))
    with cgutils.for_range(builder, n_maps) as otpvj__vyrq:
        yqr__sxytl = otpvj__vyrq.index
        pyarray_setitem(builder, context, guvzx__lakg, yqr__sxytl, syj__yhexl)
        phrxr__mmoih = get_bitmap_bit(builder, null_bitmap_ptr, yqr__sxytl)
        die__mzjnk = builder.icmp_unsigned('!=', phrxr__mmoih, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(die__mzjnk):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(yqr__sxytl, lir.Constant(
                yqr__sxytl.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [yqr__sxytl]))), lir.IntType(64))
            item_ind = builder.load(gei__tnh)
            xnh__djg = c.pyapi.dict_new()
            zis__biu = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            jdk__ohstu, xcbed__zru = c.pyapi.call_jit_code(zis__biu, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            jdk__ohstu, gnub__eii = c.pyapi.call_jit_code(zis__biu, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            hmm__uihb = c.pyapi.from_native_value(typ.key_arr_type,
                xcbed__zru, c.env_manager)
            yevbw__vevu = c.pyapi.from_native_value(typ.value_arr_type,
                gnub__eii, c.env_manager)
            zmgp__xyudo = c.pyapi.call_function_objargs(twj__dbkv, (
                hmm__uihb, yevbw__vevu))
            dict_merge_from_seq2(builder, context, xnh__djg, zmgp__xyudo)
            builder.store(builder.add(item_ind, n_items), gei__tnh)
            pyarray_setitem(builder, context, guvzx__lakg, yqr__sxytl, xnh__djg
                )
            c.pyapi.decref(zmgp__xyudo)
            c.pyapi.decref(hmm__uihb)
            c.pyapi.decref(yevbw__vevu)
            c.pyapi.decref(xnh__djg)
    c.pyapi.decref(twj__dbkv)
    c.pyapi.decref(lflbe__nosm)
    c.pyapi.decref(xnd__xkkf)
    c.pyapi.decref(nqv__vtbu)
    c.pyapi.decref(syj__yhexl)
    return guvzx__lakg


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    ffpsn__rbys = context.make_helper(builder, sig.return_type)
    ffpsn__rbys.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return ffpsn__rbys._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    auk__jcv = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return auk__jcv(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    zztzf__hvnfh = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(zztzf__hvnfh)


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
    ppr__chvhi = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            nmib__vfgl = val.keys()
            wyu__ghnvy = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), ppr__chvhi, ('key', 'value'))
            for mxws__nuwik, wqcx__arr in enumerate(nmib__vfgl):
                wyu__ghnvy[mxws__nuwik] = bodo.libs.struct_arr_ext.init_struct(
                    (wqcx__arr, val[wqcx__arr]), ('key', 'value'))
            arr._data[ind] = wyu__ghnvy
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
            fwp__uzzd = dict()
            vgzjt__fiqq = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            wyu__ghnvy = bodo.libs.array_item_arr_ext.get_data(arr._data)
            augr__wqbbd, aec__pbz = bodo.libs.struct_arr_ext.get_data(
                wyu__ghnvy)
            vxxys__tnguz = vgzjt__fiqq[ind]
            kbav__zyq = vgzjt__fiqq[ind + 1]
            for mxws__nuwik in range(vxxys__tnguz, kbav__zyq):
                fwp__uzzd[augr__wqbbd[mxws__nuwik]] = aec__pbz[mxws__nuwik]
            return fwp__uzzd
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
