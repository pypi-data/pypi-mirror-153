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
        ler__dskgy = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, ler__dskgy)


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
        kjq__smr, nsq__rgzcs = args
        ozaje__useks = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ozaje__useks.left = kjq__smr
        ozaje__useks.right = nsq__rgzcs
        context.nrt.incref(builder, signature.args[0], kjq__smr)
        context.nrt.incref(builder, signature.args[1], nsq__rgzcs)
        return ozaje__useks._getvalue()
    edcs__usy = IntervalArrayType(left)
    kizf__sazp = edcs__usy(left, right)
    return kizf__sazp, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    vkep__scc = []
    for wfbfv__cqwgb in args:
        ruys__vpmlj = equiv_set.get_shape(wfbfv__cqwgb)
        if ruys__vpmlj is not None:
            vkep__scc.append(ruys__vpmlj[0])
    if len(vkep__scc) > 1:
        equiv_set.insert_equiv(*vkep__scc)
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
    ozaje__useks = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, ozaje__useks.left)
    cygr__owgi = c.pyapi.from_native_value(typ.arr_type, ozaje__useks.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, ozaje__useks.right)
    kuvp__peir = c.pyapi.from_native_value(typ.arr_type, ozaje__useks.right,
        c.env_manager)
    hpx__bot = c.context.insert_const_string(c.builder.module, 'pandas')
    fql__ppxet = c.pyapi.import_module_noblock(hpx__bot)
    cmwv__wnkdg = c.pyapi.object_getattr_string(fql__ppxet, 'arrays')
    ifci__ipout = c.pyapi.object_getattr_string(cmwv__wnkdg, 'IntervalArray')
    etr__dtqj = c.pyapi.call_method(ifci__ipout, 'from_arrays', (cygr__owgi,
        kuvp__peir))
    c.pyapi.decref(cygr__owgi)
    c.pyapi.decref(kuvp__peir)
    c.pyapi.decref(fql__ppxet)
    c.pyapi.decref(cmwv__wnkdg)
    c.pyapi.decref(ifci__ipout)
    c.context.nrt.decref(c.builder, typ, val)
    return etr__dtqj


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    cygr__owgi = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, cygr__owgi).value
    c.pyapi.decref(cygr__owgi)
    kuvp__peir = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, kuvp__peir).value
    c.pyapi.decref(kuvp__peir)
    ozaje__useks = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ozaje__useks.left = left
    ozaje__useks.right = right
    qytjo__pqvg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ozaje__useks._getvalue(), is_error=qytjo__pqvg)


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
