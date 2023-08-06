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
        bfop__mkja = int(np.log2(self.dtype.bitwidth // 8))
        hqkjc__ziaf = 0 if self.dtype.signed else 4
        idx = bfop__mkja + hqkjc__ziaf
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        plz__fncll = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, plz__fncll)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    gxbhi__pzpod = 8 * val.dtype.itemsize
    zik__titbj = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(zik__titbj, gxbhi__pzpod))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        rse__aah = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(rse__aah)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    sjdno__pio = c.context.insert_const_string(c.builder.module, 'pandas')
    udmd__dcsi = c.pyapi.import_module_noblock(sjdno__pio)
    cayco__ztcqs = c.pyapi.call_method(udmd__dcsi, str(typ)[:-2], ())
    c.pyapi.decref(udmd__dcsi)
    return cayco__ztcqs


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    gxbhi__pzpod = 8 * val.itemsize
    zik__titbj = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(zik__titbj, gxbhi__pzpod))
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
    yivo__gkqj = n + 7 >> 3
    sed__wfnd = np.empty(yivo__gkqj, np.uint8)
    for i in range(n):
        huban__fsfcf = i // 8
        sed__wfnd[huban__fsfcf] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            sed__wfnd[huban__fsfcf]) & kBitmask[i % 8]
    return sed__wfnd


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ecznd__aomz = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ecznd__aomz)
    c.pyapi.decref(ecznd__aomz)
    owtg__ccv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yivo__gkqj = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    avuw__gpdyx = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [yivo__gkqj])
    qmya__opzn = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    glm__psu = cgutils.get_or_insert_function(c.builder.module, qmya__opzn,
        name='is_pd_int_array')
    nhxed__boxr = c.builder.call(glm__psu, [obj])
    pbvpn__yuls = c.builder.icmp_unsigned('!=', nhxed__boxr, nhxed__boxr.
        type(0))
    with c.builder.if_else(pbvpn__yuls) as (dkgq__hqoj, oxn__cgjhf):
        with dkgq__hqoj:
            uvk__sbvs = c.pyapi.object_getattr_string(obj, '_data')
            owtg__ccv.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), uvk__sbvs).value
            pjbol__oaoxq = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), pjbol__oaoxq).value
            c.pyapi.decref(uvk__sbvs)
            c.pyapi.decref(pjbol__oaoxq)
            dmqhg__gpc = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            qmya__opzn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            glm__psu = cgutils.get_or_insert_function(c.builder.module,
                qmya__opzn, name='mask_arr_to_bitmap')
            c.builder.call(glm__psu, [avuw__gpdyx.data, dmqhg__gpc.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with oxn__cgjhf:
            iakka__qcbk = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            qmya__opzn = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            tokov__ehdwy = cgutils.get_or_insert_function(c.builder.module,
                qmya__opzn, name='int_array_from_sequence')
            c.builder.call(tokov__ehdwy, [obj, c.builder.bitcast(
                iakka__qcbk.data, lir.IntType(8).as_pointer()), avuw__gpdyx
                .data])
            owtg__ccv.data = iakka__qcbk._getvalue()
    owtg__ccv.null_bitmap = avuw__gpdyx._getvalue()
    vro__oxtg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(owtg__ccv._getvalue(), is_error=vro__oxtg)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    owtg__ccv = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        owtg__ccv.data, c.env_manager)
    moqq__igiqw = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, owtg__ccv.null_bitmap).data
    ecznd__aomz = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ecznd__aomz)
    sjdno__pio = c.context.insert_const_string(c.builder.module, 'numpy')
    uxru__gwk = c.pyapi.import_module_noblock(sjdno__pio)
    hhfa__yxiz = c.pyapi.object_getattr_string(uxru__gwk, 'bool_')
    mask_arr = c.pyapi.call_method(uxru__gwk, 'empty', (ecznd__aomz,
        hhfa__yxiz))
    frjx__gqsb = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    kgnp__gsi = c.pyapi.object_getattr_string(frjx__gqsb, 'data')
    lid__qywl = c.builder.inttoptr(c.pyapi.long_as_longlong(kgnp__gsi), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as ceped__kpln:
        i = ceped__kpln.index
        jwyu__puln = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        ddys__rggkq = c.builder.load(cgutils.gep(c.builder, moqq__igiqw,
            jwyu__puln))
        hmf__hqfe = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(ddys__rggkq, hmf__hqfe), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        xyum__afz = cgutils.gep(c.builder, lid__qywl, i)
        c.builder.store(val, xyum__afz)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        owtg__ccv.null_bitmap)
    sjdno__pio = c.context.insert_const_string(c.builder.module, 'pandas')
    udmd__dcsi = c.pyapi.import_module_noblock(sjdno__pio)
    yvt__tbro = c.pyapi.object_getattr_string(udmd__dcsi, 'arrays')
    cayco__ztcqs = c.pyapi.call_method(yvt__tbro, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(udmd__dcsi)
    c.pyapi.decref(ecznd__aomz)
    c.pyapi.decref(uxru__gwk)
    c.pyapi.decref(hhfa__yxiz)
    c.pyapi.decref(frjx__gqsb)
    c.pyapi.decref(kgnp__gsi)
    c.pyapi.decref(yvt__tbro)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return cayco__ztcqs


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        axfhv__swxi, bnb__drvyj = args
        owtg__ccv = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        owtg__ccv.data = axfhv__swxi
        owtg__ccv.null_bitmap = bnb__drvyj
        context.nrt.incref(builder, signature.args[0], axfhv__swxi)
        context.nrt.incref(builder, signature.args[1], bnb__drvyj)
        return owtg__ccv._getvalue()
    hfdp__xsu = IntegerArrayType(data.dtype)
    iivq__ivo = hfdp__xsu(data, null_bitmap)
    return iivq__ivo, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    pugyx__ncqtn = np.empty(n, pyval.dtype.type)
    stq__bup = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        ovlm__teugj = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(stq__bup, i, int(not ovlm__teugj))
        if not ovlm__teugj:
            pugyx__ncqtn[i] = s
    qxlr__nwvhq = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), pugyx__ncqtn)
    iqy__yvx = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), stq__bup)
    return lir.Constant.literal_struct([qxlr__nwvhq, iqy__yvx])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    sol__ibrq = args[0]
    if equiv_set.has_shape(sol__ibrq):
        return ArrayAnalysis.AnalyzeResult(shape=sol__ibrq, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    sol__ibrq = args[0]
    if equiv_set.has_shape(sol__ibrq):
        return ArrayAnalysis.AnalyzeResult(shape=sol__ibrq, pre=[])
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
    pugyx__ncqtn = np.empty(n, dtype)
    gdou__dkhsd = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(pugyx__ncqtn, gdou__dkhsd)


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
            pwvky__dzo, djle__hrkb = array_getitem_bool_index(A, ind)
            return init_integer_array(pwvky__dzo, djle__hrkb)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            pwvky__dzo, djle__hrkb = array_getitem_int_index(A, ind)
            return init_integer_array(pwvky__dzo, djle__hrkb)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            pwvky__dzo, djle__hrkb = array_getitem_slice_index(A, ind)
            return init_integer_array(pwvky__dzo, djle__hrkb)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    bwqum__fwc = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    chv__cvzp = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if chv__cvzp:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(bwqum__fwc)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or chv__cvzp):
        raise BodoError(bwqum__fwc)
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
            chbg__drirb = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                chbg__drirb[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    chbg__drirb[i] = np.nan
            return chbg__drirb
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
                qmon__pkbg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                fjlm__utlc = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                qgbx__zgx = qmon__pkbg & fjlm__utlc
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, qgbx__zgx)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        yivo__gkqj = n + 7 >> 3
        chbg__drirb = np.empty(yivo__gkqj, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            qmon__pkbg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            fjlm__utlc = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            qgbx__zgx = qmon__pkbg & fjlm__utlc
            bodo.libs.int_arr_ext.set_bit_to_arr(chbg__drirb, i, qgbx__zgx)
        return chbg__drirb
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
    for pcks__pauio in numba.np.ufunc_db.get_ufuncs():
        gvx__thf = create_op_overload(pcks__pauio, pcks__pauio.nin)
        overload(pcks__pauio, no_unliteral=True)(gvx__thf)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        gvx__thf = create_op_overload(op, 2)
        overload(op)(gvx__thf)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        gvx__thf = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(gvx__thf)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        gvx__thf = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(gvx__thf)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    lol__bsjn = len(arrs.types)
    eavh__bxoz = 'def f(arrs):\n'
    cayco__ztcqs = ', '.join('arrs[{}]._data'.format(i) for i in range(
        lol__bsjn))
    eavh__bxoz += '  return ({}{})\n'.format(cayco__ztcqs, ',' if lol__bsjn ==
        1 else '')
    eqfiu__jop = {}
    exec(eavh__bxoz, {}, eqfiu__jop)
    impl = eqfiu__jop['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    lol__bsjn = len(arrs.types)
    enif__xohip = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        lol__bsjn))
    eavh__bxoz = 'def f(arrs):\n'
    eavh__bxoz += '  n = {}\n'.format(enif__xohip)
    eavh__bxoz += '  n_bytes = (n + 7) >> 3\n'
    eavh__bxoz += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    eavh__bxoz += '  curr_bit = 0\n'
    for i in range(lol__bsjn):
        eavh__bxoz += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        eavh__bxoz += '  for j in range(len(arrs[{}])):\n'.format(i)
        eavh__bxoz += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        eavh__bxoz += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        eavh__bxoz += '    curr_bit += 1\n'
    eavh__bxoz += '  return new_mask\n'
    eqfiu__jop = {}
    exec(eavh__bxoz, {'np': np, 'bodo': bodo}, eqfiu__jop)
    impl = eqfiu__jop['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    xof__aqc = dict(skipna=skipna, min_count=min_count)
    ntu__wnzwg = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', xof__aqc, ntu__wnzwg)

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
        hmf__hqfe = []
        hkcwb__jltkc = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not hkcwb__jltkc:
                    data.append(dtype(1))
                    hmf__hqfe.append(False)
                    hkcwb__jltkc = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                hmf__hqfe.append(True)
        pwvky__dzo = np.array(data)
        n = len(pwvky__dzo)
        yivo__gkqj = n + 7 >> 3
        djle__hrkb = np.empty(yivo__gkqj, np.uint8)
        for oxbp__gcrju in range(n):
            set_bit_to_arr(djle__hrkb, oxbp__gcrju, hmf__hqfe[oxbp__gcrju])
        return init_integer_array(pwvky__dzo, djle__hrkb)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    wyno__mctpl = numba.core.registry.cpu_target.typing_context
    tedfu__zmhuw = wyno__mctpl.resolve_function_type(op, (types.Array(A.
        dtype, 1, 'C'),), {}).return_type
    tedfu__zmhuw = to_nullable_type(tedfu__zmhuw)

    def impl(A):
        n = len(A)
        xlq__vgnsl = bodo.utils.utils.alloc_type(n, tedfu__zmhuw, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(xlq__vgnsl, i)
                continue
            xlq__vgnsl[i] = op(A[i])
        return xlq__vgnsl
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    gswc__qik = isinstance(lhs, (types.Number, types.Boolean))
    itnq__fzt = isinstance(rhs, (types.Number, types.Boolean))
    svla__kdak = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    xjmfy__kbby = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    wyno__mctpl = numba.core.registry.cpu_target.typing_context
    tedfu__zmhuw = wyno__mctpl.resolve_function_type(op, (svla__kdak,
        xjmfy__kbby), {}).return_type
    tedfu__zmhuw = to_nullable_type(tedfu__zmhuw)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    unhyk__wqx = 'lhs' if gswc__qik else 'lhs[i]'
    umgr__kws = 'rhs' if itnq__fzt else 'rhs[i]'
    qloj__uzoft = ('False' if gswc__qik else
        'bodo.libs.array_kernels.isna(lhs, i)')
    taz__zhrok = ('False' if itnq__fzt else
        'bodo.libs.array_kernels.isna(rhs, i)')
    eavh__bxoz = 'def impl(lhs, rhs):\n'
    eavh__bxoz += '  n = len({})\n'.format('lhs' if not gswc__qik else 'rhs')
    if inplace:
        eavh__bxoz += '  out_arr = {}\n'.format('lhs' if not gswc__qik else
            'rhs')
    else:
        eavh__bxoz += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    eavh__bxoz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    eavh__bxoz += '    if ({}\n'.format(qloj__uzoft)
    eavh__bxoz += '        or {}):\n'.format(taz__zhrok)
    eavh__bxoz += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    eavh__bxoz += '      continue\n'
    eavh__bxoz += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(unhyk__wqx, umgr__kws))
    eavh__bxoz += '  return out_arr\n'
    eqfiu__jop = {}
    exec(eavh__bxoz, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        tedfu__zmhuw, 'op': op}, eqfiu__jop)
    impl = eqfiu__jop['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        gswc__qik = lhs in [pd_timedelta_type]
        itnq__fzt = rhs in [pd_timedelta_type]
        if gswc__qik:

            def impl(lhs, rhs):
                n = len(rhs)
                xlq__vgnsl = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(xlq__vgnsl, i)
                        continue
                    xlq__vgnsl[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return xlq__vgnsl
            return impl
        elif itnq__fzt:

            def impl(lhs, rhs):
                n = len(lhs)
                xlq__vgnsl = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(xlq__vgnsl, i)
                        continue
                    xlq__vgnsl[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return xlq__vgnsl
            return impl
    return impl
