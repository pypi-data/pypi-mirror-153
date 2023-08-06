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
        jvwd__pwa = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, jvwd__pwa)


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
        wcqh__sqbz, onkdk__aowv = args
        okpe__pgaud = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        okpe__pgaud.left = wcqh__sqbz
        okpe__pgaud.right = onkdk__aowv
        context.nrt.incref(builder, signature.args[0], wcqh__sqbz)
        context.nrt.incref(builder, signature.args[1], onkdk__aowv)
        return okpe__pgaud._getvalue()
    jmqx__lxla = IntervalArrayType(left)
    qoof__sqogg = jmqx__lxla(left, right)
    return qoof__sqogg, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    jba__wmbdm = []
    for ltp__tyoz in args:
        nmi__yhpsd = equiv_set.get_shape(ltp__tyoz)
        if nmi__yhpsd is not None:
            jba__wmbdm.append(nmi__yhpsd[0])
    if len(jba__wmbdm) > 1:
        equiv_set.insert_equiv(*jba__wmbdm)
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
    okpe__pgaud = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, okpe__pgaud.left)
    ejcqy__sgzpb = c.pyapi.from_native_value(typ.arr_type, okpe__pgaud.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, okpe__pgaud.right)
    qdbbv__kgayn = c.pyapi.from_native_value(typ.arr_type, okpe__pgaud.
        right, c.env_manager)
    edyr__hbkd = c.context.insert_const_string(c.builder.module, 'pandas')
    ybc__jko = c.pyapi.import_module_noblock(edyr__hbkd)
    ltm__rwa = c.pyapi.object_getattr_string(ybc__jko, 'arrays')
    hml__eak = c.pyapi.object_getattr_string(ltm__rwa, 'IntervalArray')
    xroc__gcac = c.pyapi.call_method(hml__eak, 'from_arrays', (ejcqy__sgzpb,
        qdbbv__kgayn))
    c.pyapi.decref(ejcqy__sgzpb)
    c.pyapi.decref(qdbbv__kgayn)
    c.pyapi.decref(ybc__jko)
    c.pyapi.decref(ltm__rwa)
    c.pyapi.decref(hml__eak)
    c.context.nrt.decref(c.builder, typ, val)
    return xroc__gcac


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    ejcqy__sgzpb = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, ejcqy__sgzpb).value
    c.pyapi.decref(ejcqy__sgzpb)
    qdbbv__kgayn = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, qdbbv__kgayn).value
    c.pyapi.decref(qdbbv__kgayn)
    okpe__pgaud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    okpe__pgaud.left = left
    okpe__pgaud.right = right
    xrdfy__ycv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(okpe__pgaud._getvalue(), is_error=xrdfy__ycv)


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
