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
    prc__rzr = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(prc__rzr)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uapq__nmn = _get_map_arr_data_type(fe_type)
        qzz__zql = [('data', uapq__nmn)]
        models.StructModel.__init__(self, dmm, fe_type, qzz__zql)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    clvt__fvopr = all(isinstance(xanrz__chgmx, types.Array) and 
        xanrz__chgmx.dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for xanrz__chgmx in (typ.key_arr_type, typ.
        value_arr_type))
    if clvt__fvopr:
        ceqsw__kqpl = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        hbr__ben = cgutils.get_or_insert_function(c.builder.module,
            ceqsw__kqpl, name='count_total_elems_list_array')
        ouq__miho = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            hbr__ben, [val])])
    else:
        ouq__miho = get_array_elem_counts(c, c.builder, c.context, val, typ)
    uapq__nmn = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, uapq__nmn, ouq__miho, c
        )
    jfsd__qaz = _get_array_item_arr_payload(c.context, c.builder, uapq__nmn,
        data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, jfsd__qaz.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, jfsd__qaz.offsets).data
    jfdr__bfysl = _get_struct_arr_payload(c.context, c.builder, uapq__nmn.
        dtype, jfsd__qaz.data)
    key_arr = c.builder.extract_value(jfdr__bfysl.data, 0)
    value_arr = c.builder.extract_value(jfdr__bfysl.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    pifru__maoin, vos__npu = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [jfdr__bfysl.null_bitmap])
    if clvt__fvopr:
        lmsc__ujljq = c.context.make_array(uapq__nmn.dtype.data[0])(c.
            context, c.builder, key_arr).data
        lfo__err = c.context.make_array(uapq__nmn.dtype.data[1])(c.context,
            c.builder, value_arr).data
        ceqsw__kqpl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        zitrz__jal = cgutils.get_or_insert_function(c.builder.module,
            ceqsw__kqpl, name='map_array_from_sequence')
        tcu__kajze = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        vzrtd__gdgdj = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.
            dtype)
        c.builder.call(zitrz__jal, [val, c.builder.bitcast(lmsc__ujljq, lir
            .IntType(8).as_pointer()), c.builder.bitcast(lfo__err, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), tcu__kajze), lir.Constant(lir.IntType
            (32), vzrtd__gdgdj)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    oeyn__tkx = c.context.make_helper(c.builder, typ)
    oeyn__tkx.data = data_arr
    bzhdn__fhrn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oeyn__tkx._getvalue(), is_error=bzhdn__fhrn)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    jcpgf__bqzs = context.insert_const_string(builder.module, 'pandas')
    tethh__egu = c.pyapi.import_module_noblock(jcpgf__bqzs)
    hhwh__rdvz = c.pyapi.object_getattr_string(tethh__egu, 'NA')
    fbgi__oozg = c.context.get_constant(offset_type, 0)
    builder.store(fbgi__oozg, offsets_ptr)
    iaqb__jkjj = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as ggmjt__iqi:
        ncga__uyttm = ggmjt__iqi.index
        item_ind = builder.load(iaqb__jkjj)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [ncga__uyttm]))
        vizh__zdbi = seq_getitem(builder, context, val, ncga__uyttm)
        set_bitmap_bit(builder, null_bitmap_ptr, ncga__uyttm, 0)
        zaep__getb = is_na_value(builder, context, vizh__zdbi, hhwh__rdvz)
        zdv__qwfid = builder.icmp_unsigned('!=', zaep__getb, lir.Constant(
            zaep__getb.type, 1))
        with builder.if_then(zdv__qwfid):
            set_bitmap_bit(builder, null_bitmap_ptr, ncga__uyttm, 1)
            edcz__higlo = dict_keys(builder, context, vizh__zdbi)
            ceukz__nzzr = dict_values(builder, context, vizh__zdbi)
            n_items = bodo.utils.utils.object_length(c, edcz__higlo)
            _unbox_array_item_array_copy_data(typ.key_arr_type, edcz__higlo,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                ceukz__nzzr, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), iaqb__jkjj)
            c.pyapi.decref(edcz__higlo)
            c.pyapi.decref(ceukz__nzzr)
        c.pyapi.decref(vizh__zdbi)
    builder.store(builder.trunc(builder.load(iaqb__jkjj), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(tethh__egu)
    c.pyapi.decref(hhwh__rdvz)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    oeyn__tkx = c.context.make_helper(c.builder, typ, val)
    data_arr = oeyn__tkx.data
    uapq__nmn = _get_map_arr_data_type(typ)
    jfsd__qaz = _get_array_item_arr_payload(c.context, c.builder, uapq__nmn,
        data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, jfsd__qaz.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, jfsd__qaz.offsets).data
    jfdr__bfysl = _get_struct_arr_payload(c.context, c.builder, uapq__nmn.
        dtype, jfsd__qaz.data)
    key_arr = c.builder.extract_value(jfdr__bfysl.data, 0)
    value_arr = c.builder.extract_value(jfdr__bfysl.data, 1)
    if all(isinstance(xanrz__chgmx, types.Array) and xanrz__chgmx.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        xanrz__chgmx in (typ.key_arr_type, typ.value_arr_type)):
        lmsc__ujljq = c.context.make_array(uapq__nmn.dtype.data[0])(c.
            context, c.builder, key_arr).data
        lfo__err = c.context.make_array(uapq__nmn.dtype.data[1])(c.context,
            c.builder, value_arr).data
        ceqsw__kqpl = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        pomku__bura = cgutils.get_or_insert_function(c.builder.module,
            ceqsw__kqpl, name='np_array_from_map_array')
        tcu__kajze = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        vzrtd__gdgdj = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.
            dtype)
        arr = c.builder.call(pomku__bura, [jfsd__qaz.n_arrays, c.builder.
            bitcast(lmsc__ujljq, lir.IntType(8).as_pointer()), c.builder.
            bitcast(lfo__err, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), tcu__kajze), lir
            .Constant(lir.IntType(32), vzrtd__gdgdj)])
    else:
        arr = _box_map_array_generic(typ, c, jfsd__qaz.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    jcpgf__bqzs = context.insert_const_string(builder.module, 'numpy')
    rezdx__tlln = c.pyapi.import_module_noblock(jcpgf__bqzs)
    zbvtt__fya = c.pyapi.object_getattr_string(rezdx__tlln, 'object_')
    ndv__zdz = c.pyapi.long_from_longlong(n_maps)
    kmkgm__qqeb = c.pyapi.call_method(rezdx__tlln, 'ndarray', (ndv__zdz,
        zbvtt__fya))
    dzgkh__gbnf = c.pyapi.object_getattr_string(rezdx__tlln, 'nan')
    tlg__ncp = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    iaqb__jkjj = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as ggmjt__iqi:
        leocj__rrr = ggmjt__iqi.index
        pyarray_setitem(builder, context, kmkgm__qqeb, leocj__rrr, dzgkh__gbnf)
        wyn__fhhdm = get_bitmap_bit(builder, null_bitmap_ptr, leocj__rrr)
        krqd__bqy = builder.icmp_unsigned('!=', wyn__fhhdm, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(krqd__bqy):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(leocj__rrr, lir.Constant(
                leocj__rrr.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [leocj__rrr]))), lir.IntType(64))
            item_ind = builder.load(iaqb__jkjj)
            vizh__zdbi = c.pyapi.dict_new()
            qez__lnjyq = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            pifru__maoin, vqq__ick = c.pyapi.call_jit_code(qez__lnjyq, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            pifru__maoin, usj__xilg = c.pyapi.call_jit_code(qez__lnjyq, typ
                .value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            blsg__xoip = c.pyapi.from_native_value(typ.key_arr_type,
                vqq__ick, c.env_manager)
            pcq__dgvd = c.pyapi.from_native_value(typ.value_arr_type,
                usj__xilg, c.env_manager)
            irj__ymvm = c.pyapi.call_function_objargs(tlg__ncp, (blsg__xoip,
                pcq__dgvd))
            dict_merge_from_seq2(builder, context, vizh__zdbi, irj__ymvm)
            builder.store(builder.add(item_ind, n_items), iaqb__jkjj)
            pyarray_setitem(builder, context, kmkgm__qqeb, leocj__rrr,
                vizh__zdbi)
            c.pyapi.decref(irj__ymvm)
            c.pyapi.decref(blsg__xoip)
            c.pyapi.decref(pcq__dgvd)
            c.pyapi.decref(vizh__zdbi)
    c.pyapi.decref(tlg__ncp)
    c.pyapi.decref(rezdx__tlln)
    c.pyapi.decref(zbvtt__fya)
    c.pyapi.decref(ndv__zdz)
    c.pyapi.decref(dzgkh__gbnf)
    return kmkgm__qqeb


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    oeyn__tkx = context.make_helper(builder, sig.return_type)
    oeyn__tkx.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return oeyn__tkx._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    bpq__njs = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return bpq__njs(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    wnor__unkbt = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(wnor__unkbt)


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
    djh__oti = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            uki__ufyxt = val.keys()
            owxlj__jastv = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), djh__oti, ('key', 'value'))
            for igras__gxho, pcmv__duws in enumerate(uki__ufyxt):
                owxlj__jastv[igras__gxho
                    ] = bodo.libs.struct_arr_ext.init_struct((pcmv__duws,
                    val[pcmv__duws]), ('key', 'value'))
            arr._data[ind] = owxlj__jastv
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
            cckk__keqv = dict()
            wffhd__adxvi = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            owxlj__jastv = bodo.libs.array_item_arr_ext.get_data(arr._data)
            bwq__pxauf, lnrot__uxqs = bodo.libs.struct_arr_ext.get_data(
                owxlj__jastv)
            drozy__bzkz = wffhd__adxvi[ind]
            jshqn__wbtfe = wffhd__adxvi[ind + 1]
            for igras__gxho in range(drozy__bzkz, jshqn__wbtfe):
                cckk__keqv[bwq__pxauf[igras__gxho]] = lnrot__uxqs[igras__gxho]
            return cckk__keqv
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
