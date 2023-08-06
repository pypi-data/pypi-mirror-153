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
        xdei__wyf = int(np.log2(self.dtype.bitwidth // 8))
        jwb__ykqj = 0 if self.dtype.signed else 4
        idx = xdei__wyf + jwb__ykqj
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        skz__twn = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, skz__twn)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    vafg__lux = 8 * val.dtype.itemsize
    ilo__lmb = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ilo__lmb, vafg__lux))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        qstg__ocozz = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(qstg__ocozz)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    zdt__qgha = c.context.insert_const_string(c.builder.module, 'pandas')
    xyj__byzx = c.pyapi.import_module_noblock(zdt__qgha)
    ofpnk__dpmpk = c.pyapi.call_method(xyj__byzx, str(typ)[:-2], ())
    c.pyapi.decref(xyj__byzx)
    return ofpnk__dpmpk


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    vafg__lux = 8 * val.itemsize
    ilo__lmb = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ilo__lmb, vafg__lux))
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
    npb__zue = n + 7 >> 3
    bicmt__iebjv = np.empty(npb__zue, np.uint8)
    for i in range(n):
        zcupn__tyhm = i // 8
        bicmt__iebjv[zcupn__tyhm] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            bicmt__iebjv[zcupn__tyhm]) & kBitmask[i % 8]
    return bicmt__iebjv


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    mgb__nqk = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(mgb__nqk)
    c.pyapi.decref(mgb__nqk)
    wrfym__bkzt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    npb__zue = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    vcsjx__nfpo = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [npb__zue])
    zdn__ooka = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    lqds__hsdt = cgutils.get_or_insert_function(c.builder.module, zdn__ooka,
        name='is_pd_int_array')
    knlp__mop = c.builder.call(lqds__hsdt, [obj])
    ozu__sbomo = c.builder.icmp_unsigned('!=', knlp__mop, knlp__mop.type(0))
    with c.builder.if_else(ozu__sbomo) as (ickfh__rmbq, wasnr__ucidf):
        with ickfh__rmbq:
            zoz__saep = c.pyapi.object_getattr_string(obj, '_data')
            wrfym__bkzt.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), zoz__saep).value
            tohz__gmcr = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), tohz__gmcr).value
            c.pyapi.decref(zoz__saep)
            c.pyapi.decref(tohz__gmcr)
            trgp__qyn = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, mask_arr)
            zdn__ooka = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            lqds__hsdt = cgutils.get_or_insert_function(c.builder.module,
                zdn__ooka, name='mask_arr_to_bitmap')
            c.builder.call(lqds__hsdt, [vcsjx__nfpo.data, trgp__qyn.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with wasnr__ucidf:
            rsyi__szeg = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            zdn__ooka = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            xgl__silyj = cgutils.get_or_insert_function(c.builder.module,
                zdn__ooka, name='int_array_from_sequence')
            c.builder.call(xgl__silyj, [obj, c.builder.bitcast(rsyi__szeg.
                data, lir.IntType(8).as_pointer()), vcsjx__nfpo.data])
            wrfym__bkzt.data = rsyi__szeg._getvalue()
    wrfym__bkzt.null_bitmap = vcsjx__nfpo._getvalue()
    ljgjk__die = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wrfym__bkzt._getvalue(), is_error=ljgjk__die)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    wrfym__bkzt = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        wrfym__bkzt.data, c.env_manager)
    vkwom__dow = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, wrfym__bkzt.null_bitmap).data
    mgb__nqk = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(mgb__nqk)
    zdt__qgha = c.context.insert_const_string(c.builder.module, 'numpy')
    byg__uprjd = c.pyapi.import_module_noblock(zdt__qgha)
    lhm__fmof = c.pyapi.object_getattr_string(byg__uprjd, 'bool_')
    mask_arr = c.pyapi.call_method(byg__uprjd, 'empty', (mgb__nqk, lhm__fmof))
    zmv__mltjh = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    rlx__emj = c.pyapi.object_getattr_string(zmv__mltjh, 'data')
    vpn__tvg = c.builder.inttoptr(c.pyapi.long_as_longlong(rlx__emj), lir.
        IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as bljp__icg:
        i = bljp__icg.index
        ktfp__ixyh = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        hrzq__kndc = c.builder.load(cgutils.gep(c.builder, vkwom__dow,
            ktfp__ixyh))
        cvn__niqie = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(hrzq__kndc, cvn__niqie), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        frvjz__zuth = cgutils.gep(c.builder, vpn__tvg, i)
        c.builder.store(val, frvjz__zuth)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        wrfym__bkzt.null_bitmap)
    zdt__qgha = c.context.insert_const_string(c.builder.module, 'pandas')
    xyj__byzx = c.pyapi.import_module_noblock(zdt__qgha)
    ojcmo__met = c.pyapi.object_getattr_string(xyj__byzx, 'arrays')
    ofpnk__dpmpk = c.pyapi.call_method(ojcmo__met, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(xyj__byzx)
    c.pyapi.decref(mgb__nqk)
    c.pyapi.decref(byg__uprjd)
    c.pyapi.decref(lhm__fmof)
    c.pyapi.decref(zmv__mltjh)
    c.pyapi.decref(rlx__emj)
    c.pyapi.decref(ojcmo__met)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return ofpnk__dpmpk


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        ttl__vznsx, zzz__phd = args
        wrfym__bkzt = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        wrfym__bkzt.data = ttl__vznsx
        wrfym__bkzt.null_bitmap = zzz__phd
        context.nrt.incref(builder, signature.args[0], ttl__vznsx)
        context.nrt.incref(builder, signature.args[1], zzz__phd)
        return wrfym__bkzt._getvalue()
    qffd__tqei = IntegerArrayType(data.dtype)
    vxnb__hbuyj = qffd__tqei(data, null_bitmap)
    return vxnb__hbuyj, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    ebm__rjevh = np.empty(n, pyval.dtype.type)
    jni__yim = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        gpppc__rvh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(jni__yim, i, int(not gpppc__rvh))
        if not gpppc__rvh:
            ebm__rjevh[i] = s
    aetnn__qryc = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), ebm__rjevh)
    jplm__saa = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), jni__yim)
    return lir.Constant.literal_struct([aetnn__qryc, jplm__saa])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pdz__sdtqy = args[0]
    if equiv_set.has_shape(pdz__sdtqy):
        return ArrayAnalysis.AnalyzeResult(shape=pdz__sdtqy, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pdz__sdtqy = args[0]
    if equiv_set.has_shape(pdz__sdtqy):
        return ArrayAnalysis.AnalyzeResult(shape=pdz__sdtqy, pre=[])
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
    ebm__rjevh = np.empty(n, dtype)
    riaw__qqa = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(ebm__rjevh, riaw__qqa)


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
            vzqy__kfnzr, kflgn__pimrv = array_getitem_bool_index(A, ind)
            return init_integer_array(vzqy__kfnzr, kflgn__pimrv)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            vzqy__kfnzr, kflgn__pimrv = array_getitem_int_index(A, ind)
            return init_integer_array(vzqy__kfnzr, kflgn__pimrv)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            vzqy__kfnzr, kflgn__pimrv = array_getitem_slice_index(A, ind)
            return init_integer_array(vzqy__kfnzr, kflgn__pimrv)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    urpdi__fzb = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    fhay__yvo = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if fhay__yvo:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(urpdi__fzb)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or fhay__yvo):
        raise BodoError(urpdi__fzb)
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
            xzc__phde = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                xzc__phde[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    xzc__phde[i] = np.nan
            return xzc__phde
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
                otzdb__ilfh = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                oexoa__buwo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                vfvy__thqiy = otzdb__ilfh & oexoa__buwo
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, vfvy__thqiy)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        npb__zue = n + 7 >> 3
        xzc__phde = np.empty(npb__zue, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            otzdb__ilfh = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            oexoa__buwo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            vfvy__thqiy = otzdb__ilfh & oexoa__buwo
            bodo.libs.int_arr_ext.set_bit_to_arr(xzc__phde, i, vfvy__thqiy)
        return xzc__phde
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
    for jdyp__wpu in numba.np.ufunc_db.get_ufuncs():
        olh__xsst = create_op_overload(jdyp__wpu, jdyp__wpu.nin)
        overload(jdyp__wpu, no_unliteral=True)(olh__xsst)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        olh__xsst = create_op_overload(op, 2)
        overload(op)(olh__xsst)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        olh__xsst = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(olh__xsst)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        olh__xsst = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(olh__xsst)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    rovzd__xcnbw = len(arrs.types)
    zje__uoigf = 'def f(arrs):\n'
    ofpnk__dpmpk = ', '.join('arrs[{}]._data'.format(i) for i in range(
        rovzd__xcnbw))
    zje__uoigf += '  return ({}{})\n'.format(ofpnk__dpmpk, ',' if 
        rovzd__xcnbw == 1 else '')
    aiij__elwzm = {}
    exec(zje__uoigf, {}, aiij__elwzm)
    impl = aiij__elwzm['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    rovzd__xcnbw = len(arrs.types)
    mtv__kvxy = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        rovzd__xcnbw))
    zje__uoigf = 'def f(arrs):\n'
    zje__uoigf += '  n = {}\n'.format(mtv__kvxy)
    zje__uoigf += '  n_bytes = (n + 7) >> 3\n'
    zje__uoigf += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    zje__uoigf += '  curr_bit = 0\n'
    for i in range(rovzd__xcnbw):
        zje__uoigf += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        zje__uoigf += '  for j in range(len(arrs[{}])):\n'.format(i)
        zje__uoigf += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        zje__uoigf += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        zje__uoigf += '    curr_bit += 1\n'
    zje__uoigf += '  return new_mask\n'
    aiij__elwzm = {}
    exec(zje__uoigf, {'np': np, 'bodo': bodo}, aiij__elwzm)
    impl = aiij__elwzm['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    rpzf__uycz = dict(skipna=skipna, min_count=min_count)
    ynu__fqiv = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', rpzf__uycz, ynu__fqiv)

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
        cvn__niqie = []
        ajj__rlnp = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not ajj__rlnp:
                    data.append(dtype(1))
                    cvn__niqie.append(False)
                    ajj__rlnp = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                cvn__niqie.append(True)
        vzqy__kfnzr = np.array(data)
        n = len(vzqy__kfnzr)
        npb__zue = n + 7 >> 3
        kflgn__pimrv = np.empty(npb__zue, np.uint8)
        for epm__xmd in range(n):
            set_bit_to_arr(kflgn__pimrv, epm__xmd, cvn__niqie[epm__xmd])
        return init_integer_array(vzqy__kfnzr, kflgn__pimrv)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    lllmb__ffs = numba.core.registry.cpu_target.typing_context
    ghj__fgzj = lllmb__ffs.resolve_function_type(op, (types.Array(A.dtype, 
        1, 'C'),), {}).return_type
    ghj__fgzj = to_nullable_type(ghj__fgzj)

    def impl(A):
        n = len(A)
        uwnxf__tkwcb = bodo.utils.utils.alloc_type(n, ghj__fgzj, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(uwnxf__tkwcb, i)
                continue
            uwnxf__tkwcb[i] = op(A[i])
        return uwnxf__tkwcb
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    ghz__pmp = isinstance(lhs, (types.Number, types.Boolean))
    yroi__pkahv = isinstance(rhs, (types.Number, types.Boolean))
    ttr__bvnmi = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    vxhk__xqm = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    lllmb__ffs = numba.core.registry.cpu_target.typing_context
    ghj__fgzj = lllmb__ffs.resolve_function_type(op, (ttr__bvnmi, vxhk__xqm
        ), {}).return_type
    ghj__fgzj = to_nullable_type(ghj__fgzj)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    msx__fhm = 'lhs' if ghz__pmp else 'lhs[i]'
    iehb__ziizx = 'rhs' if yroi__pkahv else 'rhs[i]'
    wupc__onh = 'False' if ghz__pmp else 'bodo.libs.array_kernels.isna(lhs, i)'
    jhu__arrlv = ('False' if yroi__pkahv else
        'bodo.libs.array_kernels.isna(rhs, i)')
    zje__uoigf = 'def impl(lhs, rhs):\n'
    zje__uoigf += '  n = len({})\n'.format('lhs' if not ghz__pmp else 'rhs')
    if inplace:
        zje__uoigf += '  out_arr = {}\n'.format('lhs' if not ghz__pmp else
            'rhs')
    else:
        zje__uoigf += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    zje__uoigf += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    zje__uoigf += '    if ({}\n'.format(wupc__onh)
    zje__uoigf += '        or {}):\n'.format(jhu__arrlv)
    zje__uoigf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    zje__uoigf += '      continue\n'
    zje__uoigf += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(msx__fhm, iehb__ziizx))
    zje__uoigf += '  return out_arr\n'
    aiij__elwzm = {}
    exec(zje__uoigf, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        ghj__fgzj, 'op': op}, aiij__elwzm)
    impl = aiij__elwzm['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        ghz__pmp = lhs in [pd_timedelta_type]
        yroi__pkahv = rhs in [pd_timedelta_type]
        if ghz__pmp:

            def impl(lhs, rhs):
                n = len(rhs)
                uwnxf__tkwcb = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(uwnxf__tkwcb, i)
                        continue
                    uwnxf__tkwcb[i] = bodo.utils.conversion.unbox_if_timestamp(
                        op(lhs, rhs[i]))
                return uwnxf__tkwcb
            return impl
        elif yroi__pkahv:

            def impl(lhs, rhs):
                n = len(lhs)
                uwnxf__tkwcb = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(uwnxf__tkwcb, i)
                        continue
                    uwnxf__tkwcb[i] = bodo.utils.conversion.unbox_if_timestamp(
                        op(lhs[i], rhs))
                return uwnxf__tkwcb
            return impl
    return impl
