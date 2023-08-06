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
    vht__hyff = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(vht__hyff)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ijm__rqyz = _get_map_arr_data_type(fe_type)
        efqb__oul = [('data', ijm__rqyz)]
        models.StructModel.__init__(self, dmm, fe_type, efqb__oul)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    stk__nazu = all(isinstance(kfm__cpx, types.Array) and kfm__cpx.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        kfm__cpx in (typ.key_arr_type, typ.value_arr_type))
    if stk__nazu:
        srkt__zusl = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        vvi__uoyf = cgutils.get_or_insert_function(c.builder.module,
            srkt__zusl, name='count_total_elems_list_array')
        djir__uuy = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            vvi__uoyf, [val])])
    else:
        djir__uuy = get_array_elem_counts(c, c.builder, c.context, val, typ)
    ijm__rqyz = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, ijm__rqyz, djir__uuy, c
        )
    atixw__wfxi = _get_array_item_arr_payload(c.context, c.builder,
        ijm__rqyz, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, atixw__wfxi.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, atixw__wfxi.offsets).data
    sczt__xsgkp = _get_struct_arr_payload(c.context, c.builder, ijm__rqyz.
        dtype, atixw__wfxi.data)
    key_arr = c.builder.extract_value(sczt__xsgkp.data, 0)
    value_arr = c.builder.extract_value(sczt__xsgkp.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    rhp__evj, ucpw__lis = c.pyapi.call_jit_code(lambda A: A.fill(255), sig,
        [sczt__xsgkp.null_bitmap])
    if stk__nazu:
        poc__ihkro = c.context.make_array(ijm__rqyz.dtype.data[0])(c.
            context, c.builder, key_arr).data
        hdgq__ihu = c.context.make_array(ijm__rqyz.dtype.data[1])(c.context,
            c.builder, value_arr).data
        srkt__zusl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        peia__jral = cgutils.get_or_insert_function(c.builder.module,
            srkt__zusl, name='map_array_from_sequence')
        btzjr__oozl = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        phex__hwo = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(peia__jral, [val, c.builder.bitcast(poc__ihkro, lir.
            IntType(8).as_pointer()), c.builder.bitcast(hdgq__ihu, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), btzjr__oozl), lir.Constant(lir.
            IntType(32), phex__hwo)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    adbxd__trx = c.context.make_helper(c.builder, typ)
    adbxd__trx.data = data_arr
    ykeg__ujw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(adbxd__trx._getvalue(), is_error=ykeg__ujw)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    krlhm__azei = context.insert_const_string(builder.module, 'pandas')
    omw__zhzau = c.pyapi.import_module_noblock(krlhm__azei)
    bly__guvpu = c.pyapi.object_getattr_string(omw__zhzau, 'NA')
    wczd__avil = c.context.get_constant(offset_type, 0)
    builder.store(wczd__avil, offsets_ptr)
    bruia__erq = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as cxn__azge:
        jjf__khh = cxn__azge.index
        item_ind = builder.load(bruia__erq)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [jjf__khh]))
        unv__dsvm = seq_getitem(builder, context, val, jjf__khh)
        set_bitmap_bit(builder, null_bitmap_ptr, jjf__khh, 0)
        ovp__xkl = is_na_value(builder, context, unv__dsvm, bly__guvpu)
        ezd__grcw = builder.icmp_unsigned('!=', ovp__xkl, lir.Constant(
            ovp__xkl.type, 1))
        with builder.if_then(ezd__grcw):
            set_bitmap_bit(builder, null_bitmap_ptr, jjf__khh, 1)
            juhjm__nihai = dict_keys(builder, context, unv__dsvm)
            anxx__isv = dict_values(builder, context, unv__dsvm)
            n_items = bodo.utils.utils.object_length(c, juhjm__nihai)
            _unbox_array_item_array_copy_data(typ.key_arr_type,
                juhjm__nihai, c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, anxx__isv,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), bruia__erq)
            c.pyapi.decref(juhjm__nihai)
            c.pyapi.decref(anxx__isv)
        c.pyapi.decref(unv__dsvm)
    builder.store(builder.trunc(builder.load(bruia__erq), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(omw__zhzau)
    c.pyapi.decref(bly__guvpu)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    adbxd__trx = c.context.make_helper(c.builder, typ, val)
    data_arr = adbxd__trx.data
    ijm__rqyz = _get_map_arr_data_type(typ)
    atixw__wfxi = _get_array_item_arr_payload(c.context, c.builder,
        ijm__rqyz, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, atixw__wfxi.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, atixw__wfxi.offsets).data
    sczt__xsgkp = _get_struct_arr_payload(c.context, c.builder, ijm__rqyz.
        dtype, atixw__wfxi.data)
    key_arr = c.builder.extract_value(sczt__xsgkp.data, 0)
    value_arr = c.builder.extract_value(sczt__xsgkp.data, 1)
    if all(isinstance(kfm__cpx, types.Array) and kfm__cpx.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type) for kfm__cpx in
        (typ.key_arr_type, typ.value_arr_type)):
        poc__ihkro = c.context.make_array(ijm__rqyz.dtype.data[0])(c.
            context, c.builder, key_arr).data
        hdgq__ihu = c.context.make_array(ijm__rqyz.dtype.data[1])(c.context,
            c.builder, value_arr).data
        srkt__zusl = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        bzrdb__mawm = cgutils.get_or_insert_function(c.builder.module,
            srkt__zusl, name='np_array_from_map_array')
        btzjr__oozl = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        phex__hwo = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(bzrdb__mawm, [atixw__wfxi.n_arrays, c.builder.
            bitcast(poc__ihkro, lir.IntType(8).as_pointer()), c.builder.
            bitcast(hdgq__ihu, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), btzjr__oozl),
            lir.Constant(lir.IntType(32), phex__hwo)])
    else:
        arr = _box_map_array_generic(typ, c, atixw__wfxi.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    krlhm__azei = context.insert_const_string(builder.module, 'numpy')
    uil__uhgz = c.pyapi.import_module_noblock(krlhm__azei)
    dev__uvsfo = c.pyapi.object_getattr_string(uil__uhgz, 'object_')
    qtzqv__ydy = c.pyapi.long_from_longlong(n_maps)
    vojn__kpwkd = c.pyapi.call_method(uil__uhgz, 'ndarray', (qtzqv__ydy,
        dev__uvsfo))
    jdzrf__rjzf = c.pyapi.object_getattr_string(uil__uhgz, 'nan')
    aid__gnzue = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    bruia__erq = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as cxn__azge:
        mbpct__qkdck = cxn__azge.index
        pyarray_setitem(builder, context, vojn__kpwkd, mbpct__qkdck,
            jdzrf__rjzf)
        ojqy__gckid = get_bitmap_bit(builder, null_bitmap_ptr, mbpct__qkdck)
        hgqgo__mch = builder.icmp_unsigned('!=', ojqy__gckid, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(hgqgo__mch):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(mbpct__qkdck, lir.Constant(
                mbpct__qkdck.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [mbpct__qkdck]))), lir.IntType(64))
            item_ind = builder.load(bruia__erq)
            unv__dsvm = c.pyapi.dict_new()
            wtiq__mno = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            rhp__evj, xqk__awjhx = c.pyapi.call_jit_code(wtiq__mno, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            rhp__evj, oefxc__vwryf = c.pyapi.call_jit_code(wtiq__mno, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            rlmlj__kcjsi = c.pyapi.from_native_value(typ.key_arr_type,
                xqk__awjhx, c.env_manager)
            jdpa__lrjft = c.pyapi.from_native_value(typ.value_arr_type,
                oefxc__vwryf, c.env_manager)
            emhaw__kmrm = c.pyapi.call_function_objargs(aid__gnzue, (
                rlmlj__kcjsi, jdpa__lrjft))
            dict_merge_from_seq2(builder, context, unv__dsvm, emhaw__kmrm)
            builder.store(builder.add(item_ind, n_items), bruia__erq)
            pyarray_setitem(builder, context, vojn__kpwkd, mbpct__qkdck,
                unv__dsvm)
            c.pyapi.decref(emhaw__kmrm)
            c.pyapi.decref(rlmlj__kcjsi)
            c.pyapi.decref(jdpa__lrjft)
            c.pyapi.decref(unv__dsvm)
    c.pyapi.decref(aid__gnzue)
    c.pyapi.decref(uil__uhgz)
    c.pyapi.decref(dev__uvsfo)
    c.pyapi.decref(qtzqv__ydy)
    c.pyapi.decref(jdzrf__rjzf)
    return vojn__kpwkd


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    adbxd__trx = context.make_helper(builder, sig.return_type)
    adbxd__trx.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return adbxd__trx._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    jsi__zin = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return jsi__zin(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    fotq__lbtlh = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(fotq__lbtlh)


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
    dxjah__hcaqb = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            xjs__sux = val.keys()
            yemu__mhvgq = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), dxjah__hcaqb, ('key', 'value'))
            for otqu__ydhez, fthx__keq in enumerate(xjs__sux):
                yemu__mhvgq[otqu__ydhez
                    ] = bodo.libs.struct_arr_ext.init_struct((fthx__keq,
                    val[fthx__keq]), ('key', 'value'))
            arr._data[ind] = yemu__mhvgq
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
            arp__zcma = dict()
            eyd__lphu = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            yemu__mhvgq = bodo.libs.array_item_arr_ext.get_data(arr._data)
            oan__jzg, jivvb__uegak = bodo.libs.struct_arr_ext.get_data(
                yemu__mhvgq)
            vhk__oyma = eyd__lphu[ind]
            djomi__mep = eyd__lphu[ind + 1]
            for otqu__ydhez in range(vhk__oyma, djomi__mep):
                arp__zcma[oan__jzg[otqu__ydhez]] = jivvb__uegak[otqu__ydhez]
            return arp__zcma
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
