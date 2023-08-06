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
        cmzvo__fans = int(np.log2(self.dtype.bitwidth // 8))
        eyzia__qjie = 0 if self.dtype.signed else 4
        idx = cmzvo__fans + eyzia__qjie
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pnkp__qxn = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, pnkp__qxn)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    wvuc__uiu = 8 * val.dtype.itemsize
    kprrd__pjfds = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(kprrd__pjfds, wvuc__uiu))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        wbsi__cqbbm = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(wbsi__cqbbm)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    mhqj__wftfa = c.context.insert_const_string(c.builder.module, 'pandas')
    ile__vjs = c.pyapi.import_module_noblock(mhqj__wftfa)
    ymk__diw = c.pyapi.call_method(ile__vjs, str(typ)[:-2], ())
    c.pyapi.decref(ile__vjs)
    return ymk__diw


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    wvuc__uiu = 8 * val.itemsize
    kprrd__pjfds = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(kprrd__pjfds, wvuc__uiu))
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
    mbcm__xofs = n + 7 >> 3
    wgh__ztk = np.empty(mbcm__xofs, np.uint8)
    for i in range(n):
        huw__hxd = i // 8
        wgh__ztk[huw__hxd] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            wgh__ztk[huw__hxd]) & kBitmask[i % 8]
    return wgh__ztk


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ngw__ysb = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ngw__ysb)
    c.pyapi.decref(ngw__ysb)
    lli__fze = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mbcm__xofs = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    qkld__ugtbx = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [mbcm__xofs])
    edkbi__ktif = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    fmge__jlnsx = cgutils.get_or_insert_function(c.builder.module,
        edkbi__ktif, name='is_pd_int_array')
    cnaq__clen = c.builder.call(fmge__jlnsx, [obj])
    ivloy__ois = c.builder.icmp_unsigned('!=', cnaq__clen, cnaq__clen.type(0))
    with c.builder.if_else(ivloy__ois) as (cwalu__hxa, lffkz__szv):
        with cwalu__hxa:
            netc__ytr = c.pyapi.object_getattr_string(obj, '_data')
            lli__fze.data = c.pyapi.to_native_value(types.Array(typ.dtype, 
                1, 'C'), netc__ytr).value
            lnnlq__nnyzr = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), lnnlq__nnyzr).value
            c.pyapi.decref(netc__ytr)
            c.pyapi.decref(lnnlq__nnyzr)
            ihs__xvr = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, mask_arr)
            edkbi__ktif = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            fmge__jlnsx = cgutils.get_or_insert_function(c.builder.module,
                edkbi__ktif, name='mask_arr_to_bitmap')
            c.builder.call(fmge__jlnsx, [qkld__ugtbx.data, ihs__xvr.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with lffkz__szv:
            vkfaf__fhaf = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            edkbi__ktif = lir.FunctionType(lir.IntType(32), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            rlq__iyyom = cgutils.get_or_insert_function(c.builder.module,
                edkbi__ktif, name='int_array_from_sequence')
            c.builder.call(rlq__iyyom, [obj, c.builder.bitcast(vkfaf__fhaf.
                data, lir.IntType(8).as_pointer()), qkld__ugtbx.data])
            lli__fze.data = vkfaf__fhaf._getvalue()
    lli__fze.null_bitmap = qkld__ugtbx._getvalue()
    qcm__jyxdm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lli__fze._getvalue(), is_error=qcm__jyxdm)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    lli__fze = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        lli__fze.data, c.env_manager)
    bqgl__mab = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, lli__fze.null_bitmap).data
    ngw__ysb = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ngw__ysb)
    mhqj__wftfa = c.context.insert_const_string(c.builder.module, 'numpy')
    zctn__hvj = c.pyapi.import_module_noblock(mhqj__wftfa)
    bqrg__zyry = c.pyapi.object_getattr_string(zctn__hvj, 'bool_')
    mask_arr = c.pyapi.call_method(zctn__hvj, 'empty', (ngw__ysb, bqrg__zyry))
    xqgol__osxfx = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    nkr__grv = c.pyapi.object_getattr_string(xqgol__osxfx, 'data')
    lrh__ixf = c.builder.inttoptr(c.pyapi.long_as_longlong(nkr__grv), lir.
        IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as vzx__uom:
        i = vzx__uom.index
        sca__szz = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        zdo__ywj = c.builder.load(cgutils.gep(c.builder, bqgl__mab, sca__szz))
        xak__tmqik = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(zdo__ywj, xak__tmqik), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        eft__wsgn = cgutils.gep(c.builder, lrh__ixf, i)
        c.builder.store(val, eft__wsgn)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        lli__fze.null_bitmap)
    mhqj__wftfa = c.context.insert_const_string(c.builder.module, 'pandas')
    ile__vjs = c.pyapi.import_module_noblock(mhqj__wftfa)
    vjz__kqgc = c.pyapi.object_getattr_string(ile__vjs, 'arrays')
    ymk__diw = c.pyapi.call_method(vjz__kqgc, 'IntegerArray', (data, mask_arr))
    c.pyapi.decref(ile__vjs)
    c.pyapi.decref(ngw__ysb)
    c.pyapi.decref(zctn__hvj)
    c.pyapi.decref(bqrg__zyry)
    c.pyapi.decref(xqgol__osxfx)
    c.pyapi.decref(nkr__grv)
    c.pyapi.decref(vjz__kqgc)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return ymk__diw


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        dxwhi__piew, uwm__xpnjx = args
        lli__fze = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        lli__fze.data = dxwhi__piew
        lli__fze.null_bitmap = uwm__xpnjx
        context.nrt.incref(builder, signature.args[0], dxwhi__piew)
        context.nrt.incref(builder, signature.args[1], uwm__xpnjx)
        return lli__fze._getvalue()
    vddg__qizu = IntegerArrayType(data.dtype)
    wnpm__vinlj = vddg__qizu(data, null_bitmap)
    return wnpm__vinlj, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    zgut__zbvtp = np.empty(n, pyval.dtype.type)
    tvcju__kvq = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        sxrwq__nmwww = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(tvcju__kvq, i, int(not
            sxrwq__nmwww))
        if not sxrwq__nmwww:
            zgut__zbvtp[i] = s
    aadw__maw = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), zgut__zbvtp)
    mfmuo__hgcus = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), tvcju__kvq)
    return lir.Constant.literal_struct([aadw__maw, mfmuo__hgcus])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zmq__kmldp = args[0]
    if equiv_set.has_shape(zmq__kmldp):
        return ArrayAnalysis.AnalyzeResult(shape=zmq__kmldp, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zmq__kmldp = args[0]
    if equiv_set.has_shape(zmq__kmldp):
        return ArrayAnalysis.AnalyzeResult(shape=zmq__kmldp, pre=[])
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
    zgut__zbvtp = np.empty(n, dtype)
    rwcw__ison = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(zgut__zbvtp, rwcw__ison)


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
            nyur__fhwe, kcp__ccnj = array_getitem_bool_index(A, ind)
            return init_integer_array(nyur__fhwe, kcp__ccnj)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            nyur__fhwe, kcp__ccnj = array_getitem_int_index(A, ind)
            return init_integer_array(nyur__fhwe, kcp__ccnj)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            nyur__fhwe, kcp__ccnj = array_getitem_slice_index(A, ind)
            return init_integer_array(nyur__fhwe, kcp__ccnj)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    zmkuy__vwjea = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    tpl__szv = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if tpl__szv:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(zmkuy__vwjea)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or tpl__szv):
        raise BodoError(zmkuy__vwjea)
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
            cpwzx__osuch = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                cpwzx__osuch[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    cpwzx__osuch[i] = np.nan
            return cpwzx__osuch
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
                lkkpg__ffjk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                nhv__ucnsd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                kqklc__mvzl = lkkpg__ffjk & nhv__ucnsd
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, kqklc__mvzl)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        mbcm__xofs = n + 7 >> 3
        cpwzx__osuch = np.empty(mbcm__xofs, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            lkkpg__ffjk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            nhv__ucnsd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            kqklc__mvzl = lkkpg__ffjk & nhv__ucnsd
            bodo.libs.int_arr_ext.set_bit_to_arr(cpwzx__osuch, i, kqklc__mvzl)
        return cpwzx__osuch
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
    for mncfh__snk in numba.np.ufunc_db.get_ufuncs():
        qnr__uezf = create_op_overload(mncfh__snk, mncfh__snk.nin)
        overload(mncfh__snk, no_unliteral=True)(qnr__uezf)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        qnr__uezf = create_op_overload(op, 2)
        overload(op)(qnr__uezf)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        qnr__uezf = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qnr__uezf)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        qnr__uezf = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(qnr__uezf)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    wcz__irl = len(arrs.types)
    dpxrj__pzfw = 'def f(arrs):\n'
    ymk__diw = ', '.join('arrs[{}]._data'.format(i) for i in range(wcz__irl))
    dpxrj__pzfw += '  return ({}{})\n'.format(ymk__diw, ',' if wcz__irl == 
        1 else '')
    vhi__mke = {}
    exec(dpxrj__pzfw, {}, vhi__mke)
    impl = vhi__mke['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    wcz__irl = len(arrs.types)
    iwri__spaqs = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        wcz__irl))
    dpxrj__pzfw = 'def f(arrs):\n'
    dpxrj__pzfw += '  n = {}\n'.format(iwri__spaqs)
    dpxrj__pzfw += '  n_bytes = (n + 7) >> 3\n'
    dpxrj__pzfw += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    dpxrj__pzfw += '  curr_bit = 0\n'
    for i in range(wcz__irl):
        dpxrj__pzfw += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        dpxrj__pzfw += '  for j in range(len(arrs[{}])):\n'.format(i)
        dpxrj__pzfw += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        dpxrj__pzfw += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        dpxrj__pzfw += '    curr_bit += 1\n'
    dpxrj__pzfw += '  return new_mask\n'
    vhi__mke = {}
    exec(dpxrj__pzfw, {'np': np, 'bodo': bodo}, vhi__mke)
    impl = vhi__mke['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    gkib__fcpes = dict(skipna=skipna, min_count=min_count)
    koi__duauu = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', gkib__fcpes, koi__duauu)

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
        xak__tmqik = []
        jjx__cekw = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not jjx__cekw:
                    data.append(dtype(1))
                    xak__tmqik.append(False)
                    jjx__cekw = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                xak__tmqik.append(True)
        nyur__fhwe = np.array(data)
        n = len(nyur__fhwe)
        mbcm__xofs = n + 7 >> 3
        kcp__ccnj = np.empty(mbcm__xofs, np.uint8)
        for bkgn__aji in range(n):
            set_bit_to_arr(kcp__ccnj, bkgn__aji, xak__tmqik[bkgn__aji])
        return init_integer_array(nyur__fhwe, kcp__ccnj)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    dwrbt__kupu = numba.core.registry.cpu_target.typing_context
    hnwdv__hozto = dwrbt__kupu.resolve_function_type(op, (types.Array(A.
        dtype, 1, 'C'),), {}).return_type
    hnwdv__hozto = to_nullable_type(hnwdv__hozto)

    def impl(A):
        n = len(A)
        jbn__ruyn = bodo.utils.utils.alloc_type(n, hnwdv__hozto, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(jbn__ruyn, i)
                continue
            jbn__ruyn[i] = op(A[i])
        return jbn__ruyn
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    rjmr__htkmr = isinstance(lhs, (types.Number, types.Boolean))
    ejq__ubi = isinstance(rhs, (types.Number, types.Boolean))
    gicle__vkzvh = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    rnx__afli = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    dwrbt__kupu = numba.core.registry.cpu_target.typing_context
    hnwdv__hozto = dwrbt__kupu.resolve_function_type(op, (gicle__vkzvh,
        rnx__afli), {}).return_type
    hnwdv__hozto = to_nullable_type(hnwdv__hozto)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    nntto__qrh = 'lhs' if rjmr__htkmr else 'lhs[i]'
    vngwl__klv = 'rhs' if ejq__ubi else 'rhs[i]'
    hru__hiw = ('False' if rjmr__htkmr else
        'bodo.libs.array_kernels.isna(lhs, i)')
    qfluu__vlg = ('False' if ejq__ubi else
        'bodo.libs.array_kernels.isna(rhs, i)')
    dpxrj__pzfw = 'def impl(lhs, rhs):\n'
    dpxrj__pzfw += '  n = len({})\n'.format('lhs' if not rjmr__htkmr else 'rhs'
        )
    if inplace:
        dpxrj__pzfw += '  out_arr = {}\n'.format('lhs' if not rjmr__htkmr else
            'rhs')
    else:
        dpxrj__pzfw += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    dpxrj__pzfw += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    dpxrj__pzfw += '    if ({}\n'.format(hru__hiw)
    dpxrj__pzfw += '        or {}):\n'.format(qfluu__vlg)
    dpxrj__pzfw += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    dpxrj__pzfw += '      continue\n'
    dpxrj__pzfw += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(nntto__qrh, vngwl__klv))
    dpxrj__pzfw += '  return out_arr\n'
    vhi__mke = {}
    exec(dpxrj__pzfw, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        hnwdv__hozto, 'op': op}, vhi__mke)
    impl = vhi__mke['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        rjmr__htkmr = lhs in [pd_timedelta_type]
        ejq__ubi = rhs in [pd_timedelta_type]
        if rjmr__htkmr:

            def impl(lhs, rhs):
                n = len(rhs)
                jbn__ruyn = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(jbn__ruyn, i)
                        continue
                    jbn__ruyn[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return jbn__ruyn
            return impl
        elif ejq__ubi:

            def impl(lhs, rhs):
                n = len(lhs)
                jbn__ruyn = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(jbn__ruyn, i)
                        continue
                    jbn__ruyn[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return jbn__ruyn
            return impl
    return impl
