"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        yatm__mct = int(np.log2(self.dtype.bitwidth // 8))
        rxeva__cvgr = 0 if self.dtype.signed else 4
        idx = yatm__mct + rxeva__cvgr
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        non__kbz = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, non__kbz)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    ntseu__sixkg = 8 * val.dtype.itemsize
    txiqf__djet = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(txiqf__djet, ntseu__sixkg))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        rix__mpix = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(rix__mpix)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    hioc__kdo = c.context.insert_const_string(c.builder.module, 'pandas')
    qmjeb__cdh = c.pyapi.import_module_noblock(hioc__kdo)
    vaqqh__ducf = c.pyapi.call_method(qmjeb__cdh, str(typ)[:-2], ())
    c.pyapi.decref(qmjeb__cdh)
    return vaqqh__ducf


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    ntseu__sixkg = 8 * val.itemsize
    txiqf__djet = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(txiqf__djet, ntseu__sixkg))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    wtmu__qzgx = n + 7 >> 3
    gfon__xvct = np.empty(wtmu__qzgx, np.uint8)
    for i in range(n):
        bbtv__dldq = i // 8
        gfon__xvct[bbtv__dldq] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            gfon__xvct[bbtv__dldq]) & kBitmask[i % 8]
    return gfon__xvct


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    tdftc__gcdxl = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(tdftc__gcdxl)
    c.pyapi.decref(tdftc__gcdxl)
    mpqoz__roonj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wtmu__qzgx = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    tmf__lnyg = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [wtmu__qzgx])
    fak__azuw = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    gqbz__idkoh = cgutils.get_or_insert_function(c.builder.module,
        fak__azuw, name='is_pd_int_array')
    cgw__qhj = c.builder.call(gqbz__idkoh, [obj])
    qij__tgwx = c.builder.icmp_unsigned('!=', cgw__qhj, cgw__qhj.type(0))
    with c.builder.if_else(qij__tgwx) as (hqnp__xdxur, cpxi__toa):
        with hqnp__xdxur:
            gava__lgj = c.pyapi.object_getattr_string(obj, '_data')
            mpqoz__roonj.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), gava__lgj).value
            wbzja__jktu = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), wbzja__jktu).value
            c.pyapi.decref(gava__lgj)
            c.pyapi.decref(wbzja__jktu)
            vtl__xlgb = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, mask_arr)
            fak__azuw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            gqbz__idkoh = cgutils.get_or_insert_function(c.builder.module,
                fak__azuw, name='mask_arr_to_bitmap')
            c.builder.call(gqbz__idkoh, [tmf__lnyg.data, vtl__xlgb.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with cpxi__toa:
            sng__lvpu = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            fak__azuw = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            glkis__zvt = cgutils.get_or_insert_function(c.builder.module,
                fak__azuw, name='int_array_from_sequence')
            c.builder.call(glkis__zvt, [obj, c.builder.bitcast(sng__lvpu.
                data, lir.IntType(8).as_pointer()), tmf__lnyg.data])
            mpqoz__roonj.data = sng__lvpu._getvalue()
    mpqoz__roonj.null_bitmap = tmf__lnyg._getvalue()
    qzysy__fiz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mpqoz__roonj._getvalue(), is_error=qzysy__fiz)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    mpqoz__roonj = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        mpqoz__roonj.data, c.env_manager)
    vigs__rjwai = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, mpqoz__roonj.null_bitmap).data
    tdftc__gcdxl = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(tdftc__gcdxl)
    hioc__kdo = c.context.insert_const_string(c.builder.module, 'numpy')
    nkr__kqbze = c.pyapi.import_module_noblock(hioc__kdo)
    rhrj__nmr = c.pyapi.object_getattr_string(nkr__kqbze, 'bool_')
    mask_arr = c.pyapi.call_method(nkr__kqbze, 'empty', (tdftc__gcdxl,
        rhrj__nmr))
    kep__lpngx = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    xix__zfaj = c.pyapi.object_getattr_string(kep__lpngx, 'data')
    xspow__slpoa = c.builder.inttoptr(c.pyapi.long_as_longlong(xix__zfaj),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as qib__qfil:
        i = qib__qfil.index
        ipbfp__cevk = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        kybok__tucn = c.builder.load(cgutils.gep(c.builder, vigs__rjwai,
            ipbfp__cevk))
        yhtd__vqk = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(kybok__tucn, yhtd__vqk), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        zgwsr__vspqq = cgutils.gep(c.builder, xspow__slpoa, i)
        c.builder.store(val, zgwsr__vspqq)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        mpqoz__roonj.null_bitmap)
    hioc__kdo = c.context.insert_const_string(c.builder.module, 'pandas')
    qmjeb__cdh = c.pyapi.import_module_noblock(hioc__kdo)
    ewd__zobnr = c.pyapi.object_getattr_string(qmjeb__cdh, 'arrays')
    vaqqh__ducf = c.pyapi.call_method(ewd__zobnr, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(qmjeb__cdh)
    c.pyapi.decref(tdftc__gcdxl)
    c.pyapi.decref(nkr__kqbze)
    c.pyapi.decref(rhrj__nmr)
    c.pyapi.decref(kep__lpngx)
    c.pyapi.decref(xix__zfaj)
    c.pyapi.decref(ewd__zobnr)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return vaqqh__ducf


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        miaim__cqj, euzjn__war = args
        mpqoz__roonj = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        mpqoz__roonj.data = miaim__cqj
        mpqoz__roonj.null_bitmap = euzjn__war
        context.nrt.incref(builder, signature.args[0], miaim__cqj)
        context.nrt.incref(builder, signature.args[1], euzjn__war)
        return mpqoz__roonj._getvalue()
    tlaar__ipvpr = IntegerArrayType(data.dtype)
    bwk__xhk = tlaar__ipvpr(data, null_bitmap)
    return bwk__xhk, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    jpc__gse = np.empty(n, pyval.dtype.type)
    ggjn__vobz = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        lof__zdqd = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ggjn__vobz, i, int(not lof__zdqd))
        if not lof__zdqd:
            jpc__gse[i] = s
    yzt__kxs = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), jpc__gse)
    znliw__lvimy = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ggjn__vobz)
    return lir.Constant.literal_struct([yzt__kxs, znliw__lvimy])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zqc__knlbx = args[0]
    if equiv_set.has_shape(zqc__knlbx):
        return ArrayAnalysis.AnalyzeResult(shape=zqc__knlbx, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zqc__knlbx = args[0]
    if equiv_set.has_shape(zqc__knlbx):
        return ArrayAnalysis.AnalyzeResult(shape=zqc__knlbx, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    jpc__gse = np.empty(n, dtype)
    syod__kawb = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(jpc__gse, syod__kawb)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            bzt__jcq, uqcs__kuta = array_getitem_bool_index(A, ind)
            return init_integer_array(bzt__jcq, uqcs__kuta)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            bzt__jcq, uqcs__kuta = array_getitem_int_index(A, ind)
            return init_integer_array(bzt__jcq, uqcs__kuta)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            bzt__jcq, uqcs__kuta = array_getitem_slice_index(A, ind)
            return init_integer_array(bzt__jcq, uqcs__kuta)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    kvnzt__tiue = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    koxv__yzre = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if koxv__yzre:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(kvnzt__tiue)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or koxv__yzre):
        raise BodoError(kvnzt__tiue)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            hjxx__hrio = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                hjxx__hrio[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    hjxx__hrio[i] = np.nan
            return hjxx__hrio
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def apply_null_mask(arr, bitmap, mask_fill, inplace):
    assert isinstance(arr, types.Array)
    if isinstance(arr.dtype, types.Integer):
        if is_overload_none(inplace):
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap.copy()))
        else:
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap))
    if isinstance(arr.dtype, types.Float):

        def impl(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = np.nan
            return arr
        return impl
    if arr.dtype == types.bool_:

        def impl_bool(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = mask_fill
            return arr
        return impl_bool
    return lambda arr, bitmap, mask_fill, inplace: arr


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def merge_bitmaps(B1, B2, n, inplace):
    assert B1 == types.Array(types.uint8, 1, 'C')
    assert B2 == types.Array(types.uint8, 1, 'C')
    if not is_overload_none(inplace):

        def impl_inplace(B1, B2, n, inplace):
            for i in numba.parfors.parfor.internal_prange(n):
                tkfaf__hyw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                odhfy__lberg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                mmg__aaqsk = tkfaf__hyw & odhfy__lberg
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, mmg__aaqsk)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        wtmu__qzgx = n + 7 >> 3
        hjxx__hrio = np.empty(wtmu__qzgx, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            tkfaf__hyw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            odhfy__lberg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            mmg__aaqsk = tkfaf__hyw & odhfy__lberg
            bodo.libs.int_arr_ext.set_bit_to_arr(hjxx__hrio, i, mmg__aaqsk)
        return hjxx__hrio
    return impl


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for mqs__gymn in numba.np.ufunc_db.get_ufuncs():
        klhx__dyvp = create_op_overload(mqs__gymn, mqs__gymn.nin)
        overload(mqs__gymn, no_unliteral=True)(klhx__dyvp)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        klhx__dyvp = create_op_overload(op, 2)
        overload(op)(klhx__dyvp)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        klhx__dyvp = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(klhx__dyvp)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        klhx__dyvp = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(klhx__dyvp)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    kcgh__hxvwo = len(arrs.types)
    aher__incgd = 'def f(arrs):\n'
    vaqqh__ducf = ', '.join('arrs[{}]._data'.format(i) for i in range(
        kcgh__hxvwo))
    aher__incgd += '  return ({}{})\n'.format(vaqqh__ducf, ',' if 
        kcgh__hxvwo == 1 else '')
    aqhil__ead = {}
    exec(aher__incgd, {}, aqhil__ead)
    impl = aqhil__ead['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    kcgh__hxvwo = len(arrs.types)
    otuja__phvcr = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        kcgh__hxvwo))
    aher__incgd = 'def f(arrs):\n'
    aher__incgd += '  n = {}\n'.format(otuja__phvcr)
    aher__incgd += '  n_bytes = (n + 7) >> 3\n'
    aher__incgd += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    aher__incgd += '  curr_bit = 0\n'
    for i in range(kcgh__hxvwo):
        aher__incgd += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        aher__incgd += '  for j in range(len(arrs[{}])):\n'.format(i)
        aher__incgd += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        aher__incgd += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        aher__incgd += '    curr_bit += 1\n'
    aher__incgd += '  return new_mask\n'
    aqhil__ead = {}
    exec(aher__incgd, {'np': np, 'bodo': bodo}, aqhil__ead)
    impl = aqhil__ead['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    onpjt__vfum = dict(skipna=skipna, min_count=min_count)
    lgs__thl = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', onpjt__vfum, lgs__thl)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        yhtd__vqk = []
        ttalj__qws = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not ttalj__qws:
                    data.append(dtype(1))
                    yhtd__vqk.append(False)
                    ttalj__qws = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                yhtd__vqk.append(True)
        bzt__jcq = np.array(data)
        n = len(bzt__jcq)
        wtmu__qzgx = n + 7 >> 3
        uqcs__kuta = np.empty(wtmu__qzgx, np.uint8)
        for lytzx__sqvw in range(n):
            set_bit_to_arr(uqcs__kuta, lytzx__sqvw, yhtd__vqk[lytzx__sqvw])
        return init_integer_array(bzt__jcq, uqcs__kuta)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    njsez__yukas = numba.core.registry.cpu_target.typing_context
    xwt__ypiq = njsez__yukas.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    xwt__ypiq = to_nullable_type(xwt__ypiq)

    def impl(A):
        n = len(A)
        jll__xto = bodo.utils.utils.alloc_type(n, xwt__ypiq, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(jll__xto, i)
                continue
            jll__xto[i] = op(A[i])
        return jll__xto
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    oqpam__jxonp = isinstance(lhs, (types.Number, types.Boolean))
    nynh__jyt = isinstance(rhs, (types.Number, types.Boolean))
    whwz__nhw = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    xumip__tcam = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    njsez__yukas = numba.core.registry.cpu_target.typing_context
    xwt__ypiq = njsez__yukas.resolve_function_type(op, (whwz__nhw,
        xumip__tcam), {}).return_type
    xwt__ypiq = to_nullable_type(xwt__ypiq)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    nvo__hypc = 'lhs' if oqpam__jxonp else 'lhs[i]'
    kopf__ecph = 'rhs' if nynh__jyt else 'rhs[i]'
    rxh__oujab = ('False' if oqpam__jxonp else
        'bodo.libs.array_kernels.isna(lhs, i)')
    tuih__ygns = ('False' if nynh__jyt else
        'bodo.libs.array_kernels.isna(rhs, i)')
    aher__incgd = 'def impl(lhs, rhs):\n'
    aher__incgd += '  n = len({})\n'.format('lhs' if not oqpam__jxonp else
        'rhs')
    if inplace:
        aher__incgd += '  out_arr = {}\n'.format('lhs' if not oqpam__jxonp else
            'rhs')
    else:
        aher__incgd += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    aher__incgd += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    aher__incgd += '    if ({}\n'.format(rxh__oujab)
    aher__incgd += '        or {}):\n'.format(tuih__ygns)
    aher__incgd += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    aher__incgd += '      continue\n'
    aher__incgd += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(nvo__hypc, kopf__ecph))
    aher__incgd += '  return out_arr\n'
    aqhil__ead = {}
    exec(aher__incgd, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        xwt__ypiq, 'op': op}, aqhil__ead)
    impl = aqhil__ead['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        oqpam__jxonp = lhs in [pd_timedelta_type]
        nynh__jyt = rhs in [pd_timedelta_type]
        if oqpam__jxonp:

            def impl(lhs, rhs):
                n = len(rhs)
                jll__xto = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(jll__xto, i)
                        continue
                    jll__xto[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return jll__xto
            return impl
        elif nynh__jyt:

            def impl(lhs, rhs):
                n = len(lhs)
                jll__xto = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(jll__xto, i)
                        continue
                    jll__xto[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return jll__xto
            return impl
    return impl
