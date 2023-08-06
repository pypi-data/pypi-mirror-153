"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        djwh__hhfl = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, djwh__hhfl)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        juaqv__muew, ajth__xllu = args
        lofsb__awbt = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        lofsb__awbt.left = juaqv__muew
        lofsb__awbt.right = ajth__xllu
        context.nrt.incref(builder, signature.args[0], juaqv__muew)
        context.nrt.incref(builder, signature.args[1], ajth__xllu)
        return lofsb__awbt._getvalue()
    uxl__rru = IntervalArrayType(left)
    wibg__jbsf = uxl__rru(left, right)
    return wibg__jbsf, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    fbb__oaw = []
    for dex__gqqkk in args:
        cxm__mod = equiv_set.get_shape(dex__gqqkk)
        if cxm__mod is not None:
            fbb__oaw.append(cxm__mod[0])
    if len(fbb__oaw) > 1:
        equiv_set.insert_equiv(*fbb__oaw)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    lofsb__awbt = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, lofsb__awbt.left)
    hnn__uhl = c.pyapi.from_native_value(typ.arr_type, lofsb__awbt.left, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, lofsb__awbt.right)
    zze__qey = c.pyapi.from_native_value(typ.arr_type, lofsb__awbt.right, c
        .env_manager)
    catbs__xgvrs = c.context.insert_const_string(c.builder.module, 'pandas')
    vmq__ktne = c.pyapi.import_module_noblock(catbs__xgvrs)
    luxl__uvr = c.pyapi.object_getattr_string(vmq__ktne, 'arrays')
    ovo__kgenz = c.pyapi.object_getattr_string(luxl__uvr, 'IntervalArray')
    kor__mtmsm = c.pyapi.call_method(ovo__kgenz, 'from_arrays', (hnn__uhl,
        zze__qey))
    c.pyapi.decref(hnn__uhl)
    c.pyapi.decref(zze__qey)
    c.pyapi.decref(vmq__ktne)
    c.pyapi.decref(luxl__uvr)
    c.pyapi.decref(ovo__kgenz)
    c.context.nrt.decref(c.builder, typ, val)
    return kor__mtmsm


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    hnn__uhl = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, hnn__uhl).value
    c.pyapi.decref(hnn__uhl)
    zze__qey = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, zze__qey).value
    c.pyapi.decref(zze__qey)
    lofsb__awbt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lofsb__awbt.left = left
    lofsb__awbt.right = right
    tbz__syg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lofsb__awbt._getvalue(), is_error=tbz__syg)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
