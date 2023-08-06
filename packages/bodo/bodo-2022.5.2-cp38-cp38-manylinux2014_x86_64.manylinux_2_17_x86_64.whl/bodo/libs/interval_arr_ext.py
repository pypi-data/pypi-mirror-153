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
        hifi__pebw = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, hifi__pebw)


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
        jdrwm__zlj, dcsgp__rdglw = args
        eob__ajfzr = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        eob__ajfzr.left = jdrwm__zlj
        eob__ajfzr.right = dcsgp__rdglw
        context.nrt.incref(builder, signature.args[0], jdrwm__zlj)
        context.nrt.incref(builder, signature.args[1], dcsgp__rdglw)
        return eob__ajfzr._getvalue()
    gvdsd__fbwhk = IntervalArrayType(left)
    suqw__wcbjx = gvdsd__fbwhk(left, right)
    return suqw__wcbjx, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    holq__gdrd = []
    for nscys__rho in args:
        dbf__ycin = equiv_set.get_shape(nscys__rho)
        if dbf__ycin is not None:
            holq__gdrd.append(dbf__ycin[0])
    if len(holq__gdrd) > 1:
        equiv_set.insert_equiv(*holq__gdrd)
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
    eob__ajfzr = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, eob__ajfzr.left)
    gwpq__ukpv = c.pyapi.from_native_value(typ.arr_type, eob__ajfzr.left, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, eob__ajfzr.right)
    hmfrb__gurgg = c.pyapi.from_native_value(typ.arr_type, eob__ajfzr.right,
        c.env_manager)
    rymcv__hibj = c.context.insert_const_string(c.builder.module, 'pandas')
    tni__mnkg = c.pyapi.import_module_noblock(rymcv__hibj)
    rldjp__cjw = c.pyapi.object_getattr_string(tni__mnkg, 'arrays')
    jlok__wfuqz = c.pyapi.object_getattr_string(rldjp__cjw, 'IntervalArray')
    gho__zwie = c.pyapi.call_method(jlok__wfuqz, 'from_arrays', (gwpq__ukpv,
        hmfrb__gurgg))
    c.pyapi.decref(gwpq__ukpv)
    c.pyapi.decref(hmfrb__gurgg)
    c.pyapi.decref(tni__mnkg)
    c.pyapi.decref(rldjp__cjw)
    c.pyapi.decref(jlok__wfuqz)
    c.context.nrt.decref(c.builder, typ, val)
    return gho__zwie


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    gwpq__ukpv = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, gwpq__ukpv).value
    c.pyapi.decref(gwpq__ukpv)
    hmfrb__gurgg = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, hmfrb__gurgg).value
    c.pyapi.decref(hmfrb__gurgg)
    eob__ajfzr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    eob__ajfzr.left = left
    eob__ajfzr.right = right
    emjo__uhjkj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(eob__ajfzr._getvalue(), is_error=emjo__uhjkj)


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
