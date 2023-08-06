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
    vlg__tql = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(vlg__tql)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pafgg__nef = _get_map_arr_data_type(fe_type)
        fsods__rga = [('data', pafgg__nef)]
        models.StructModel.__init__(self, dmm, fe_type, fsods__rga)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    elzy__phvd = all(isinstance(lokwg__hgiby, types.Array) and lokwg__hgiby
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for lokwg__hgiby in (typ.key_arr_type, typ.
        value_arr_type))
    if elzy__phvd:
        gihp__hwcx = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        aqc__msjei = cgutils.get_or_insert_function(c.builder.module,
            gihp__hwcx, name='count_total_elems_list_array')
        uis__wwpi = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            aqc__msjei, [val])])
    else:
        uis__wwpi = get_array_elem_counts(c, c.builder, c.context, val, typ)
    pafgg__nef = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, pafgg__nef,
        uis__wwpi, c)
    qar__sgabu = _get_array_item_arr_payload(c.context, c.builder,
        pafgg__nef, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, qar__sgabu.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, qar__sgabu.offsets).data
    psrk__dyrco = _get_struct_arr_payload(c.context, c.builder, pafgg__nef.
        dtype, qar__sgabu.data)
    key_arr = c.builder.extract_value(psrk__dyrco.data, 0)
    value_arr = c.builder.extract_value(psrk__dyrco.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    exhn__kfmlo, yxn__ijon = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [psrk__dyrco.null_bitmap])
    if elzy__phvd:
        hzf__ssgob = c.context.make_array(pafgg__nef.dtype.data[0])(c.
            context, c.builder, key_arr).data
        gflf__icws = c.context.make_array(pafgg__nef.dtype.data[1])(c.
            context, c.builder, value_arr).data
        gihp__hwcx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        nxnxe__ywrwr = cgutils.get_or_insert_function(c.builder.module,
            gihp__hwcx, name='map_array_from_sequence')
        dmj__cwlqi = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        myl__hfh = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(nxnxe__ywrwr, [val, c.builder.bitcast(hzf__ssgob,
            lir.IntType(8).as_pointer()), c.builder.bitcast(gflf__icws, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), dmj__cwlqi), lir.Constant(lir.IntType
            (32), myl__hfh)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    vrrmm__ahokv = c.context.make_helper(c.builder, typ)
    vrrmm__ahokv.data = data_arr
    wmed__kncj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vrrmm__ahokv._getvalue(), is_error=wmed__kncj)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    dnz__dwch = context.insert_const_string(builder.module, 'pandas')
    ayp__hbax = c.pyapi.import_module_noblock(dnz__dwch)
    emyr__mbnm = c.pyapi.object_getattr_string(ayp__hbax, 'NA')
    fouw__urfc = c.context.get_constant(offset_type, 0)
    builder.store(fouw__urfc, offsets_ptr)
    iob__pkxyj = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as eeloa__wol:
        gmtha__nga = eeloa__wol.index
        item_ind = builder.load(iob__pkxyj)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [gmtha__nga]))
        sgco__rnafi = seq_getitem(builder, context, val, gmtha__nga)
        set_bitmap_bit(builder, null_bitmap_ptr, gmtha__nga, 0)
        asgc__nhwm = is_na_value(builder, context, sgco__rnafi, emyr__mbnm)
        zbwa__rwo = builder.icmp_unsigned('!=', asgc__nhwm, lir.Constant(
            asgc__nhwm.type, 1))
        with builder.if_then(zbwa__rwo):
            set_bitmap_bit(builder, null_bitmap_ptr, gmtha__nga, 1)
            cvmi__pgv = dict_keys(builder, context, sgco__rnafi)
            ycsoq__inbb = dict_values(builder, context, sgco__rnafi)
            n_items = bodo.utils.utils.object_length(c, cvmi__pgv)
            _unbox_array_item_array_copy_data(typ.key_arr_type, cvmi__pgv,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                ycsoq__inbb, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), iob__pkxyj)
            c.pyapi.decref(cvmi__pgv)
            c.pyapi.decref(ycsoq__inbb)
        c.pyapi.decref(sgco__rnafi)
    builder.store(builder.trunc(builder.load(iob__pkxyj), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(ayp__hbax)
    c.pyapi.decref(emyr__mbnm)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    vrrmm__ahokv = c.context.make_helper(c.builder, typ, val)
    data_arr = vrrmm__ahokv.data
    pafgg__nef = _get_map_arr_data_type(typ)
    qar__sgabu = _get_array_item_arr_payload(c.context, c.builder,
        pafgg__nef, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, qar__sgabu.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, qar__sgabu.offsets).data
    psrk__dyrco = _get_struct_arr_payload(c.context, c.builder, pafgg__nef.
        dtype, qar__sgabu.data)
    key_arr = c.builder.extract_value(psrk__dyrco.data, 0)
    value_arr = c.builder.extract_value(psrk__dyrco.data, 1)
    if all(isinstance(lokwg__hgiby, types.Array) and lokwg__hgiby.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        lokwg__hgiby in (typ.key_arr_type, typ.value_arr_type)):
        hzf__ssgob = c.context.make_array(pafgg__nef.dtype.data[0])(c.
            context, c.builder, key_arr).data
        gflf__icws = c.context.make_array(pafgg__nef.dtype.data[1])(c.
            context, c.builder, value_arr).data
        gihp__hwcx = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        dme__wxurm = cgutils.get_or_insert_function(c.builder.module,
            gihp__hwcx, name='np_array_from_map_array')
        dmj__cwlqi = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        myl__hfh = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(dme__wxurm, [qar__sgabu.n_arrays, c.builder.
            bitcast(hzf__ssgob, lir.IntType(8).as_pointer()), c.builder.
            bitcast(gflf__icws, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), dmj__cwlqi), lir
            .Constant(lir.IntType(32), myl__hfh)])
    else:
        arr = _box_map_array_generic(typ, c, qar__sgabu.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    dnz__dwch = context.insert_const_string(builder.module, 'numpy')
    ekvt__hnwf = c.pyapi.import_module_noblock(dnz__dwch)
    mgnul__jvua = c.pyapi.object_getattr_string(ekvt__hnwf, 'object_')
    vqfzd__ijzu = c.pyapi.long_from_longlong(n_maps)
    vywqh__tpbly = c.pyapi.call_method(ekvt__hnwf, 'ndarray', (vqfzd__ijzu,
        mgnul__jvua))
    yttn__suj = c.pyapi.object_getattr_string(ekvt__hnwf, 'nan')
    hjf__yhb = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    iob__pkxyj = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as eeloa__wol:
        tmw__swkh = eeloa__wol.index
        pyarray_setitem(builder, context, vywqh__tpbly, tmw__swkh, yttn__suj)
        iodxr__uwhsx = get_bitmap_bit(builder, null_bitmap_ptr, tmw__swkh)
        awz__mtcc = builder.icmp_unsigned('!=', iodxr__uwhsx, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(awz__mtcc):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(tmw__swkh, lir.Constant(tmw__swkh
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                tmw__swkh]))), lir.IntType(64))
            item_ind = builder.load(iob__pkxyj)
            sgco__rnafi = c.pyapi.dict_new()
            ogi__eecfk = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            exhn__kfmlo, zis__dlr = c.pyapi.call_jit_code(ogi__eecfk, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            exhn__kfmlo, xuuds__jevx = c.pyapi.call_jit_code(ogi__eecfk,
                typ.value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            ntsgg__bqj = c.pyapi.from_native_value(typ.key_arr_type,
                zis__dlr, c.env_manager)
            tcqm__lbno = c.pyapi.from_native_value(typ.value_arr_type,
                xuuds__jevx, c.env_manager)
            isqnz__cpg = c.pyapi.call_function_objargs(hjf__yhb, (
                ntsgg__bqj, tcqm__lbno))
            dict_merge_from_seq2(builder, context, sgco__rnafi, isqnz__cpg)
            builder.store(builder.add(item_ind, n_items), iob__pkxyj)
            pyarray_setitem(builder, context, vywqh__tpbly, tmw__swkh,
                sgco__rnafi)
            c.pyapi.decref(isqnz__cpg)
            c.pyapi.decref(ntsgg__bqj)
            c.pyapi.decref(tcqm__lbno)
            c.pyapi.decref(sgco__rnafi)
    c.pyapi.decref(hjf__yhb)
    c.pyapi.decref(ekvt__hnwf)
    c.pyapi.decref(mgnul__jvua)
    c.pyapi.decref(vqfzd__ijzu)
    c.pyapi.decref(yttn__suj)
    return vywqh__tpbly


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    vrrmm__ahokv = context.make_helper(builder, sig.return_type)
    vrrmm__ahokv.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return vrrmm__ahokv._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    jytx__hbru = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return jytx__hbru(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    mwgiz__igc = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(mwgiz__igc)


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
    evls__zruu = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            exit__gasjm = val.keys()
            fhvo__axo = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), evls__zruu, ('key', 'value'))
            for nqexx__qzzg, zdjbf__wqcrk in enumerate(exit__gasjm):
                fhvo__axo[nqexx__qzzg] = bodo.libs.struct_arr_ext.init_struct((
                    zdjbf__wqcrk, val[zdjbf__wqcrk]), ('key', 'value'))
            arr._data[ind] = fhvo__axo
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
            abnp__jdfsr = dict()
            lmkqb__wvmm = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            fhvo__axo = bodo.libs.array_item_arr_ext.get_data(arr._data)
            syjig__wobhl, noevi__txx = bodo.libs.struct_arr_ext.get_data(
                fhvo__axo)
            cns__ors = lmkqb__wvmm[ind]
            mlf__xgrhv = lmkqb__wvmm[ind + 1]
            for nqexx__qzzg in range(cns__ors, mlf__xgrhv):
                abnp__jdfsr[syjig__wobhl[nqexx__qzzg]] = noevi__txx[nqexx__qzzg
                    ]
            return abnp__jdfsr
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
