"""Array of tuple values, implemented by reusing array of structs implementation.
"""
import operator
import numba
import numpy as np
from numba.core import types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.struct_arr_ext import StructArrayType, box_struct_arr, unbox_struct_array


class TupleArrayType(types.ArrayCompatible):

    def __init__(self, data):
        self.data = data
        super(TupleArrayType, self).__init__(name='TupleArrayType({})'.
            format(data))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.BaseTuple.from_types(tuple(svnam__vmt.dtype for
            svnam__vmt in self.data))

    def copy(self):
        return TupleArrayType(self.data)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(TupleArrayType)
class TupleArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ndh__gtmw = [('data', StructArrayType(fe_type.data))]
        models.StructModel.__init__(self, dmm, fe_type, ndh__gtmw)


make_attribute_wrapper(TupleArrayType, 'data', '_data')


@intrinsic
def init_tuple_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, StructArrayType)
    ehktd__lcm = TupleArrayType(data_typ.data)

    def codegen(context, builder, sig, args):
        drpf__jpys, = args
        ijatl__spgi = context.make_helper(builder, ehktd__lcm)
        ijatl__spgi.data = drpf__jpys
        context.nrt.incref(builder, data_typ, drpf__jpys)
        return ijatl__spgi._getvalue()
    return ehktd__lcm(data_typ), codegen


@unbox(TupleArrayType)
def unbox_tuple_array(typ, val, c):
    data_typ = StructArrayType(typ.data)
    xxlv__gdg = unbox_struct_array(data_typ, val, c, is_tuple_array=True)
    drpf__jpys = xxlv__gdg.value
    ijatl__spgi = c.context.make_helper(c.builder, typ)
    ijatl__spgi.data = drpf__jpys
    ecc__qmlv = xxlv__gdg.is_error
    return NativeValue(ijatl__spgi._getvalue(), is_error=ecc__qmlv)


@box(TupleArrayType)
def box_tuple_arr(typ, val, c):
    data_typ = StructArrayType(typ.data)
    ijatl__spgi = c.context.make_helper(c.builder, typ, val)
    arr = box_struct_arr(data_typ, ijatl__spgi.data, c, is_tuple_array=True)
    return arr


@numba.njit
def pre_alloc_tuple_array(n, nested_counts, dtypes):
    return init_tuple_arr(bodo.libs.struct_arr_ext.pre_alloc_struct_array(n,
        nested_counts, dtypes, None))


def pre_alloc_tuple_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_tuple_arr_ext_pre_alloc_tuple_array
    ) = pre_alloc_tuple_array_equiv


@overload(operator.getitem, no_unliteral=True)
def tuple_arr_getitem(arr, ind):
    if not isinstance(arr, TupleArrayType):
        return
    if isinstance(ind, types.Integer):
        ewhmo__bzs = 'def impl(arr, ind):\n'
        fuv__dppn = ','.join(f'get_data(arr._data)[{ylq__iqmpo}][ind]' for
            ylq__iqmpo in range(len(arr.data)))
        ewhmo__bzs += f'  return ({fuv__dppn})\n'
        vxg__zdhu = {}
        exec(ewhmo__bzs, {'get_data': bodo.libs.struct_arr_ext.get_data},
            vxg__zdhu)
        zijng__tsd = vxg__zdhu['impl']
        return zijng__tsd

    def impl_arr(arr, ind):
        return init_tuple_arr(arr._data[ind])
    return impl_arr


@overload(operator.setitem, no_unliteral=True)
def tuple_arr_setitem(arr, ind, val):
    if not isinstance(arr, TupleArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        mnbhy__ydy = len(arr.data)
        ewhmo__bzs = 'def impl(arr, ind, val):\n'
        ewhmo__bzs += '  data = get_data(arr._data)\n'
        ewhmo__bzs += '  null_bitmap = get_null_bitmap(arr._data)\n'
        ewhmo__bzs += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for ylq__iqmpo in range(mnbhy__ydy):
            ewhmo__bzs += f'  data[{ylq__iqmpo}][ind] = val[{ylq__iqmpo}]\n'
        vxg__zdhu = {}
        exec(ewhmo__bzs, {'get_data': bodo.libs.struct_arr_ext.get_data,
            'get_null_bitmap': bodo.libs.struct_arr_ext.get_null_bitmap,
            'set_bit_to_arr': bodo.libs.int_arr_ext.set_bit_to_arr}, vxg__zdhu)
        zijng__tsd = vxg__zdhu['impl']
        return zijng__tsd

    def impl_arr(arr, ind, val):
        val = bodo.utils.conversion.coerce_to_array(val, use_nullable_array
            =True)
        arr._data[ind] = val._data
    return impl_arr


@overload(len, no_unliteral=True)
def overload_tuple_arr_len(A):
    if isinstance(A, TupleArrayType):
        return lambda A: len(A._data)


@overload_attribute(TupleArrayType, 'shape')
def overload_tuple_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(TupleArrayType, 'dtype')
def overload_tuple_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(TupleArrayType, 'ndim')
def overload_tuple_arr_ndim(A):
    return lambda A: 1


@overload_attribute(TupleArrayType, 'nbytes')
def overload_tuple_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(TupleArrayType, 'copy', no_unliteral=True)
def overload_tuple_arr_copy(A):

    def copy_impl(A):
        return init_tuple_arr(A._data.copy())
    return copy_impl
