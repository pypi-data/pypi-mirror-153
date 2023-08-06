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
        jqet__efr = int(np.log2(self.dtype.bitwidth // 8))
        weke__gefv = 0 if self.dtype.signed else 4
        idx = jqet__efr + weke__gefv
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pfnrg__rva = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, pfnrg__rva)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    apcnh__fftyl = 8 * val.dtype.itemsize
    ctax__sbsoc = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ctax__sbsoc, apcnh__fftyl))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        ofq__wuatg = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(ofq__wuatg)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    jwav__desh = c.context.insert_const_string(c.builder.module, 'pandas')
    iptzo__ljex = c.pyapi.import_module_noblock(jwav__desh)
    lppfj__mcoc = c.pyapi.call_method(iptzo__ljex, str(typ)[:-2], ())
    c.pyapi.decref(iptzo__ljex)
    return lppfj__mcoc


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    apcnh__fftyl = 8 * val.itemsize
    ctax__sbsoc = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ctax__sbsoc, apcnh__fftyl))
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
    zjppx__bkfyy = n + 7 >> 3
    sank__wfdo = np.empty(zjppx__bkfyy, np.uint8)
    for i in range(n):
        kkq__prdw = i // 8
        sank__wfdo[kkq__prdw] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            sank__wfdo[kkq__prdw]) & kBitmask[i % 8]
    return sank__wfdo


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    hpe__vfqu = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(hpe__vfqu)
    c.pyapi.decref(hpe__vfqu)
    bhro__ltg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zjppx__bkfyy = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    oxgn__nnv = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [zjppx__bkfyy])
    ytb__wmxx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    xruia__eoot = cgutils.get_or_insert_function(c.builder.module,
        ytb__wmxx, name='is_pd_int_array')
    pjwbp__hwxy = c.builder.call(xruia__eoot, [obj])
    tbwen__jamk = c.builder.icmp_unsigned('!=', pjwbp__hwxy, pjwbp__hwxy.
        type(0))
    with c.builder.if_else(tbwen__jamk) as (eqb__niid, wcyek__nir):
        with eqb__niid:
            ilnn__jncu = c.pyapi.object_getattr_string(obj, '_data')
            bhro__ltg.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), ilnn__jncu).value
            vbdii__lkeic = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), vbdii__lkeic).value
            c.pyapi.decref(ilnn__jncu)
            c.pyapi.decref(vbdii__lkeic)
            femae__dnmyw = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, mask_arr)
            ytb__wmxx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            xruia__eoot = cgutils.get_or_insert_function(c.builder.module,
                ytb__wmxx, name='mask_arr_to_bitmap')
            c.builder.call(xruia__eoot, [oxgn__nnv.data, femae__dnmyw.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with wcyek__nir:
            izep__yzjt = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            ytb__wmxx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            ckcl__qzlvh = cgutils.get_or_insert_function(c.builder.module,
                ytb__wmxx, name='int_array_from_sequence')
            c.builder.call(ckcl__qzlvh, [obj, c.builder.bitcast(izep__yzjt.
                data, lir.IntType(8).as_pointer()), oxgn__nnv.data])
            bhro__ltg.data = izep__yzjt._getvalue()
    bhro__ltg.null_bitmap = oxgn__nnv._getvalue()
    odaug__zwfg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bhro__ltg._getvalue(), is_error=odaug__zwfg)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    bhro__ltg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        bhro__ltg.data, c.env_manager)
    ides__pkxd = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, bhro__ltg.null_bitmap).data
    hpe__vfqu = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(hpe__vfqu)
    jwav__desh = c.context.insert_const_string(c.builder.module, 'numpy')
    swdl__pehm = c.pyapi.import_module_noblock(jwav__desh)
    farqr__sql = c.pyapi.object_getattr_string(swdl__pehm, 'bool_')
    mask_arr = c.pyapi.call_method(swdl__pehm, 'empty', (hpe__vfqu, farqr__sql)
        )
    rnbw__phew = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    sypj__gwjr = c.pyapi.object_getattr_string(rnbw__phew, 'data')
    wjmwq__jqs = c.builder.inttoptr(c.pyapi.long_as_longlong(sypj__gwjr),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as hzest__gva:
        i = hzest__gva.index
        weu__dhdxg = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        hgi__ksexp = c.builder.load(cgutils.gep(c.builder, ides__pkxd,
            weu__dhdxg))
        zdzr__hyx = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(hgi__ksexp, zdzr__hyx), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        ikhoc__awdvh = cgutils.gep(c.builder, wjmwq__jqs, i)
        c.builder.store(val, ikhoc__awdvh)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        bhro__ltg.null_bitmap)
    jwav__desh = c.context.insert_const_string(c.builder.module, 'pandas')
    iptzo__ljex = c.pyapi.import_module_noblock(jwav__desh)
    myo__vxsh = c.pyapi.object_getattr_string(iptzo__ljex, 'arrays')
    lppfj__mcoc = c.pyapi.call_method(myo__vxsh, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(iptzo__ljex)
    c.pyapi.decref(hpe__vfqu)
    c.pyapi.decref(swdl__pehm)
    c.pyapi.decref(farqr__sql)
    c.pyapi.decref(rnbw__phew)
    c.pyapi.decref(sypj__gwjr)
    c.pyapi.decref(myo__vxsh)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return lppfj__mcoc


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        yce__gof, vmqu__xaxf = args
        bhro__ltg = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        bhro__ltg.data = yce__gof
        bhro__ltg.null_bitmap = vmqu__xaxf
        context.nrt.incref(builder, signature.args[0], yce__gof)
        context.nrt.incref(builder, signature.args[1], vmqu__xaxf)
        return bhro__ltg._getvalue()
    vuoq__hnm = IntegerArrayType(data.dtype)
    orh__aywqe = vuoq__hnm(data, null_bitmap)
    return orh__aywqe, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    otnl__otip = np.empty(n, pyval.dtype.type)
    kig__dwxqd = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        bkmux__ngqr = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(kig__dwxqd, i, int(not
            bkmux__ngqr))
        if not bkmux__ngqr:
            otnl__otip[i] = s
    tylg__slps = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), otnl__otip)
    xnrwx__zth = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), kig__dwxqd)
    return lir.Constant.literal_struct([tylg__slps, xnrwx__zth])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    sxy__cvu = args[0]
    if equiv_set.has_shape(sxy__cvu):
        return ArrayAnalysis.AnalyzeResult(shape=sxy__cvu, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    sxy__cvu = args[0]
    if equiv_set.has_shape(sxy__cvu):
        return ArrayAnalysis.AnalyzeResult(shape=sxy__cvu, pre=[])
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
    otnl__otip = np.empty(n, dtype)
    rdvt__rzw = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(otnl__otip, rdvt__rzw)


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
            dzyi__ddb, pwyru__lmfx = array_getitem_bool_index(A, ind)
            return init_integer_array(dzyi__ddb, pwyru__lmfx)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            dzyi__ddb, pwyru__lmfx = array_getitem_int_index(A, ind)
            return init_integer_array(dzyi__ddb, pwyru__lmfx)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            dzyi__ddb, pwyru__lmfx = array_getitem_slice_index(A, ind)
            return init_integer_array(dzyi__ddb, pwyru__lmfx)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dcqf__xqzkx = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    odx__msfz = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if odx__msfz:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(dcqf__xqzkx)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or odx__msfz):
        raise BodoError(dcqf__xqzkx)
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
            vbvnu__tllsy = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                vbvnu__tllsy[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    vbvnu__tllsy[i] = np.nan
            return vbvnu__tllsy
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
                zqwz__anmvt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                pkpa__elxt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                nme__fpayz = zqwz__anmvt & pkpa__elxt
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, nme__fpayz)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        zjppx__bkfyy = n + 7 >> 3
        vbvnu__tllsy = np.empty(zjppx__bkfyy, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            zqwz__anmvt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            pkpa__elxt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            nme__fpayz = zqwz__anmvt & pkpa__elxt
            bodo.libs.int_arr_ext.set_bit_to_arr(vbvnu__tllsy, i, nme__fpayz)
        return vbvnu__tllsy
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
    for spfgi__gsnqv in numba.np.ufunc_db.get_ufuncs():
        drwjb__vdaw = create_op_overload(spfgi__gsnqv, spfgi__gsnqv.nin)
        overload(spfgi__gsnqv, no_unliteral=True)(drwjb__vdaw)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        drwjb__vdaw = create_op_overload(op, 2)
        overload(op)(drwjb__vdaw)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        drwjb__vdaw = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(drwjb__vdaw)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        drwjb__vdaw = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(drwjb__vdaw)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    lwag__rldsy = len(arrs.types)
    oaux__gaxrm = 'def f(arrs):\n'
    lppfj__mcoc = ', '.join('arrs[{}]._data'.format(i) for i in range(
        lwag__rldsy))
    oaux__gaxrm += '  return ({}{})\n'.format(lppfj__mcoc, ',' if 
        lwag__rldsy == 1 else '')
    dazt__tsz = {}
    exec(oaux__gaxrm, {}, dazt__tsz)
    impl = dazt__tsz['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    lwag__rldsy = len(arrs.types)
    esj__pefo = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        lwag__rldsy))
    oaux__gaxrm = 'def f(arrs):\n'
    oaux__gaxrm += '  n = {}\n'.format(esj__pefo)
    oaux__gaxrm += '  n_bytes = (n + 7) >> 3\n'
    oaux__gaxrm += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    oaux__gaxrm += '  curr_bit = 0\n'
    for i in range(lwag__rldsy):
        oaux__gaxrm += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        oaux__gaxrm += '  for j in range(len(arrs[{}])):\n'.format(i)
        oaux__gaxrm += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        oaux__gaxrm += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        oaux__gaxrm += '    curr_bit += 1\n'
    oaux__gaxrm += '  return new_mask\n'
    dazt__tsz = {}
    exec(oaux__gaxrm, {'np': np, 'bodo': bodo}, dazt__tsz)
    impl = dazt__tsz['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    jkjl__lhbz = dict(skipna=skipna, min_count=min_count)
    taawp__ydit = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', jkjl__lhbz, taawp__ydit)

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
        zdzr__hyx = []
        nnft__mlwro = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not nnft__mlwro:
                    data.append(dtype(1))
                    zdzr__hyx.append(False)
                    nnft__mlwro = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                zdzr__hyx.append(True)
        dzyi__ddb = np.array(data)
        n = len(dzyi__ddb)
        zjppx__bkfyy = n + 7 >> 3
        pwyru__lmfx = np.empty(zjppx__bkfyy, np.uint8)
        for wxzd__zby in range(n):
            set_bit_to_arr(pwyru__lmfx, wxzd__zby, zdzr__hyx[wxzd__zby])
        return init_integer_array(dzyi__ddb, pwyru__lmfx)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    ojti__covp = numba.core.registry.cpu_target.typing_context
    qih__mfw = ojti__covp.resolve_function_type(op, (types.Array(A.dtype, 1,
        'C'),), {}).return_type
    qih__mfw = to_nullable_type(qih__mfw)

    def impl(A):
        n = len(A)
        lze__olxf = bodo.utils.utils.alloc_type(n, qih__mfw, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(lze__olxf, i)
                continue
            lze__olxf[i] = op(A[i])
        return lze__olxf
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    jgmn__cktac = isinstance(lhs, (types.Number, types.Boolean))
    wpj__rvz = isinstance(rhs, (types.Number, types.Boolean))
    qpg__ymax = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    qomfl__quznf = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    ojti__covp = numba.core.registry.cpu_target.typing_context
    qih__mfw = ojti__covp.resolve_function_type(op, (qpg__ymax,
        qomfl__quznf), {}).return_type
    qih__mfw = to_nullable_type(qih__mfw)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    bygp__kpbmf = 'lhs' if jgmn__cktac else 'lhs[i]'
    fwb__ezdq = 'rhs' if wpj__rvz else 'rhs[i]'
    qetz__nzgjb = ('False' if jgmn__cktac else
        'bodo.libs.array_kernels.isna(lhs, i)')
    stmt__jjd = 'False' if wpj__rvz else 'bodo.libs.array_kernels.isna(rhs, i)'
    oaux__gaxrm = 'def impl(lhs, rhs):\n'
    oaux__gaxrm += '  n = len({})\n'.format('lhs' if not jgmn__cktac else 'rhs'
        )
    if inplace:
        oaux__gaxrm += '  out_arr = {}\n'.format('lhs' if not jgmn__cktac else
            'rhs')
    else:
        oaux__gaxrm += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    oaux__gaxrm += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    oaux__gaxrm += '    if ({}\n'.format(qetz__nzgjb)
    oaux__gaxrm += '        or {}):\n'.format(stmt__jjd)
    oaux__gaxrm += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    oaux__gaxrm += '      continue\n'
    oaux__gaxrm += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(bygp__kpbmf, fwb__ezdq))
    oaux__gaxrm += '  return out_arr\n'
    dazt__tsz = {}
    exec(oaux__gaxrm, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        qih__mfw, 'op': op}, dazt__tsz)
    impl = dazt__tsz['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        jgmn__cktac = lhs in [pd_timedelta_type]
        wpj__rvz = rhs in [pd_timedelta_type]
        if jgmn__cktac:

            def impl(lhs, rhs):
                n = len(rhs)
                lze__olxf = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(lze__olxf, i)
                        continue
                    lze__olxf[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return lze__olxf
            return impl
        elif wpj__rvz:

            def impl(lhs, rhs):
                n = len(lhs)
                lze__olxf = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(lze__olxf, i)
                        continue
                    lze__olxf[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return lze__olxf
            return impl
    return impl
