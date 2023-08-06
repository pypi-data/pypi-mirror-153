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
        wcl__czbv = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, wcl__czbv)


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
        uigmt__zctbf, yimxp__tdsag = args
        jxoet__zuacu = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        jxoet__zuacu.left = uigmt__zctbf
        jxoet__zuacu.right = yimxp__tdsag
        context.nrt.incref(builder, signature.args[0], uigmt__zctbf)
        context.nrt.incref(builder, signature.args[1], yimxp__tdsag)
        return jxoet__zuacu._getvalue()
    ymjya__aks = IntervalArrayType(left)
    ltex__ppxs = ymjya__aks(left, right)
    return ltex__ppxs, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pxuhj__xxkrb = []
    for ywgov__bftie in args:
        vudg__wtass = equiv_set.get_shape(ywgov__bftie)
        if vudg__wtass is not None:
            pxuhj__xxkrb.append(vudg__wtass[0])
    if len(pxuhj__xxkrb) > 1:
        equiv_set.insert_equiv(*pxuhj__xxkrb)
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
    jxoet__zuacu = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, jxoet__zuacu.left)
    pwyc__ilr = c.pyapi.from_native_value(typ.arr_type, jxoet__zuacu.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, jxoet__zuacu.right)
    lotyw__dorr = c.pyapi.from_native_value(typ.arr_type, jxoet__zuacu.
        right, c.env_manager)
    qekqn__yoe = c.context.insert_const_string(c.builder.module, 'pandas')
    xst__xhqbm = c.pyapi.import_module_noblock(qekqn__yoe)
    mhjm__nll = c.pyapi.object_getattr_string(xst__xhqbm, 'arrays')
    bmg__aoox = c.pyapi.object_getattr_string(mhjm__nll, 'IntervalArray')
    guyyw__imdh = c.pyapi.call_method(bmg__aoox, 'from_arrays', (pwyc__ilr,
        lotyw__dorr))
    c.pyapi.decref(pwyc__ilr)
    c.pyapi.decref(lotyw__dorr)
    c.pyapi.decref(xst__xhqbm)
    c.pyapi.decref(mhjm__nll)
    c.pyapi.decref(bmg__aoox)
    c.context.nrt.decref(c.builder, typ, val)
    return guyyw__imdh


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    pwyc__ilr = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, pwyc__ilr).value
    c.pyapi.decref(pwyc__ilr)
    lotyw__dorr = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, lotyw__dorr).value
    c.pyapi.decref(lotyw__dorr)
    jxoet__zuacu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jxoet__zuacu.left = left
    jxoet__zuacu.right = right
    ztfjz__kib = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jxoet__zuacu._getvalue(), is_error=ztfjz__kib)


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
