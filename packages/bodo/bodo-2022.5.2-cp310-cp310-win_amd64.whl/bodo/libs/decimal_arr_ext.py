"""Decimal array corresponding to Arrow Decimal128Array type.
It is similar to Spark's DecimalType. From Spark's docs:
'The DecimalType must have fixed precision (the maximum total number of digits) and
scale (the number of digits on the right of dot). For example, (5, 2) can support the
value from [-999.99 to 999.99].
The precision can be up to 38, the scale must be less or equal to precision.'
'When infer schema from decimal.Decimal objects, it will be DecimalType(38, 18).'
"""
import operator
from decimal import Decimal
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import decimal_ext
ll.add_symbol('box_decimal_array', decimal_ext.box_decimal_array)
ll.add_symbol('unbox_decimal', decimal_ext.unbox_decimal)
ll.add_symbol('unbox_decimal_array', decimal_ext.unbox_decimal_array)
ll.add_symbol('decimal_to_str', decimal_ext.decimal_to_str)
ll.add_symbol('str_to_decimal', decimal_ext.str_to_decimal)
ll.add_symbol('decimal_cmp_eq', decimal_ext.decimal_cmp_eq)
ll.add_symbol('decimal_cmp_ne', decimal_ext.decimal_cmp_ne)
ll.add_symbol('decimal_cmp_gt', decimal_ext.decimal_cmp_gt)
ll.add_symbol('decimal_cmp_ge', decimal_ext.decimal_cmp_ge)
ll.add_symbol('decimal_cmp_lt', decimal_ext.decimal_cmp_lt)
ll.add_symbol('decimal_cmp_le', decimal_ext.decimal_cmp_le)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
int128_type = types.Integer('int128', 128)


class Decimal128Type(types.Type):

    def __init__(self, precision, scale):
        assert isinstance(precision, int)
        assert isinstance(scale, int)
        super(Decimal128Type, self).__init__(name='Decimal128Type({}, {})'.
            format(precision, scale))
        self.precision = precision
        self.scale = scale
        self.bitwidth = 128


@typeof_impl.register(Decimal)
def typeof_decimal_value(val, c):
    return Decimal128Type(38, 18)


register_model(Decimal128Type)(models.IntegerModel)


@intrinsic
def int128_to_decimal128type(typingctx, val, precision_tp, scale_tp=None):
    assert val == int128_type
    assert is_overload_constant_int(precision_tp)
    assert is_overload_constant_int(scale_tp)

    def codegen(context, builder, signature, args):
        return args[0]
    precision = get_overload_const_int(precision_tp)
    scale = get_overload_const_int(scale_tp)
    return Decimal128Type(precision, scale)(int128_type, precision_tp, scale_tp
        ), codegen


@intrinsic
def decimal128type_to_int128(typingctx, val):
    assert isinstance(val, Decimal128Type)

    def codegen(context, builder, signature, args):
        return args[0]
    return int128_type(val), codegen


def decimal_to_str_codegen(context, builder, signature, args, scale):
    val, = args
    scale = context.get_constant(types.int32, scale)
    stvwt__jjcpe = cgutils.create_struct_proxy(types.unicode_type)(context,
        builder)
    jqa__nqt = lir.FunctionType(lir.VoidType(), [lir.IntType(128), lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64).as_pointer(),
        lir.IntType(32)])
    lprjx__ttrle = cgutils.get_or_insert_function(builder.module, jqa__nqt,
        name='decimal_to_str')
    builder.call(lprjx__ttrle, [val, stvwt__jjcpe._get_ptr_by_name(
        'meminfo'), stvwt__jjcpe._get_ptr_by_name('length'), scale])
    stvwt__jjcpe.kind = context.get_constant(types.int32, numba.cpython.
        unicode.PY_UNICODE_1BYTE_KIND)
    stvwt__jjcpe.is_ascii = context.get_constant(types.int32, 1)
    stvwt__jjcpe.hash = context.get_constant(numba.cpython.unicode.
        _Py_hash_t, -1)
    stvwt__jjcpe.data = context.nrt.meminfo_data(builder, stvwt__jjcpe.meminfo)
    stvwt__jjcpe.parent = cgutils.get_null_value(stvwt__jjcpe.parent.type)
    return stvwt__jjcpe._getvalue()


@intrinsic
def decimal_to_str(typingctx, val_t=None):
    assert isinstance(val_t, Decimal128Type)

    def codegen(context, builder, signature, args):
        return decimal_to_str_codegen(context, builder, signature, args,
            val_t.scale)
    return bodo.string_type(val_t), codegen


def str_to_decimal_codegen(context, builder, signature, args):
    val, sevvq__qwet, sevvq__qwet = args
    val = bodo.libs.str_ext.gen_unicode_to_std_str(context, builder, val)
    jqa__nqt = lir.FunctionType(lir.IntType(128), [lir.IntType(8).as_pointer()]
        )
    lprjx__ttrle = cgutils.get_or_insert_function(builder.module, jqa__nqt,
        name='str_to_decimal')
    rhrv__rvv = builder.call(lprjx__ttrle, [val])
    return rhrv__rvv


@intrinsic
def str_to_decimal(typingctx, val, precision_tp, scale_tp=None):
    assert val == bodo.string_type or is_overload_constant_str(val)
    assert is_overload_constant_int(precision_tp)
    assert is_overload_constant_int(scale_tp)

    def codegen(context, builder, signature, args):
        return str_to_decimal_codegen(context, builder, signature, args)
    precision = get_overload_const_int(precision_tp)
    scale = get_overload_const_int(scale_tp)
    return Decimal128Type(precision, scale)(val, precision_tp, scale_tp
        ), codegen


@overload(str, no_unliteral=True)
def overload_str_decimal(val):
    if isinstance(val, Decimal128Type):

        def impl(val):
            return decimal_to_str(val)
        return impl


@intrinsic
def decimal128type_to_int64_tuple(typingctx, val):
    assert isinstance(val, Decimal128Type)

    def codegen(context, builder, signature, args):
        lvas__mdqz = cgutils.alloca_once(builder, lir.ArrayType(lir.IntType
            (64), 2))
        builder.store(args[0], builder.bitcast(lvas__mdqz, lir.IntType(128)
            .as_pointer()))
        return builder.load(lvas__mdqz)
    return types.UniTuple(types.int64, 2)(val), codegen


@intrinsic
def decimal128type_cmp(typingctx, val1, scale1, val2, scale2, func_name):
    assert is_overload_constant_str(func_name)
    uqh__faoh = get_overload_const_str(func_name)

    def codegen(context, builder, signature, args):
        val1, scale1, val2, scale2, sevvq__qwet = args
        jqa__nqt = lir.FunctionType(lir.IntType(1), [lir.IntType(128), lir.
            IntType(64), lir.IntType(128), lir.IntType(64)])
        lprjx__ttrle = cgutils.get_or_insert_function(builder.module,
            jqa__nqt, name=uqh__faoh)
        return builder.call(lprjx__ttrle, (val1, scale1, val2, scale2))
    return types.boolean(val1, scale1, val2, scale2, func_name), codegen


def decimal_create_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            uqh__faoh = 'decimal_cmp_' + op.__name__
            scale1 = lhs.scale
            scale2 = rhs.scale

            def impl(lhs, rhs):
                return decimal128type_cmp(lhs, scale1, rhs, scale2, uqh__faoh)
            return impl
    return overload_cmp


@lower_constant(Decimal128Type)
def lower_constant_decimal(context, builder, ty, pyval):
    pjtvs__loar = numba.njit(lambda v: decimal128type_to_int64_tuple(v))(pyval)
    gmeva__cdgd = [context.get_constant_generic(builder, types.int64, v) for
        v in pjtvs__loar]
    mpiot__ejjf = cgutils.pack_array(builder, gmeva__cdgd)
    lvas__mdqz = cgutils.alloca_once(builder, lir.IntType(128))
    builder.store(mpiot__ejjf, builder.bitcast(lvas__mdqz, lir.ArrayType(
        lir.IntType(64), 2).as_pointer()))
    return builder.load(lvas__mdqz)


@overload(Decimal, no_unliteral=True)
def decimal_constructor_overload(value='0', context=None):
    if not is_overload_none(context):
        raise BodoError('decimal.Decimal() context argument not supported yet')
    if isinstance(value, (types.Integer,)) or is_overload_constant_str(value
        ) or value == bodo.string_type:

        def impl(value='0', context=None):
            return str_to_decimal(str(value), 38, 18)
        return impl
    else:
        raise BodoError(
            'decimal.Decimal() value type must be an integer or string')


@overload(bool, no_unliteral=True)
def decimal_to_bool(dec):
    if not isinstance(dec, Decimal128Type):
        return

    def impl(dec):
        return bool(decimal128type_to_int128(dec))
    return impl


@unbox(Decimal128Type)
def unbox_decimal(typ, val, c):
    jqa__nqt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer(
        ), lir.IntType(128).as_pointer()])
    lprjx__ttrle = cgutils.get_or_insert_function(c.builder.module,
        jqa__nqt, name='unbox_decimal')
    lvas__mdqz = cgutils.alloca_once(c.builder, c.context.get_value_type(
        int128_type))
    c.builder.call(lprjx__ttrle, [val, lvas__mdqz])
    kzf__jgsty = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    qoccb__iske = c.builder.load(lvas__mdqz)
    return NativeValue(qoccb__iske, is_error=kzf__jgsty)


@box(Decimal128Type)
def box_decimal(typ, val, c):
    cyui__yrixl = decimal_to_str_codegen(c.context, c.builder, bodo.
        string_type(typ), (val,), typ.scale)
    ujigr__zkuae = c.pyapi.from_native_value(bodo.string_type, cyui__yrixl,
        c.env_manager)
    zstx__xyrde = c.context.insert_const_string(c.builder.module, 'decimal')
    knk__oed = c.pyapi.import_module_noblock(zstx__xyrde)
    lvas__mdqz = c.pyapi.call_method(knk__oed, 'Decimal', (ujigr__zkuae,))
    c.pyapi.decref(ujigr__zkuae)
    c.pyapi.decref(knk__oed)
    return lvas__mdqz


@overload_method(Decimal128Type, '__hash__', no_unliteral=True)
def decimal_hash(val):

    def impl(val):
        return hash(decimal_to_str(val))
    return impl


class DecimalArrayType(types.ArrayCompatible):

    def __init__(self, precision, scale):
        self.precision = precision
        self.scale = scale
        super(DecimalArrayType, self).__init__(name=
            'DecimalArrayType({}, {})'.format(precision, scale))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return DecimalArrayType(self.precision, self.scale)

    @property
    def dtype(self):
        return Decimal128Type(self.precision, self.scale)


data_type = types.Array(int128_type, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DecimalArrayType)
class DecimalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ntec__boe = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ntec__boe)


make_attribute_wrapper(DecimalArrayType, 'data', '_data')
make_attribute_wrapper(DecimalArrayType, 'null_bitmap', '_null_bitmap')


@intrinsic
def init_decimal_array(typingctx, data, null_bitmap, precision_tp, scale_tp
    =None):
    assert data == types.Array(int128_type, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    assert is_overload_constant_int(precision_tp)
    assert is_overload_constant_int(scale_tp)

    def codegen(context, builder, signature, args):
        esdtn__wux, wvo__uvhv, sevvq__qwet, sevvq__qwet = args
        jljpb__fdu = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        jljpb__fdu.data = esdtn__wux
        jljpb__fdu.null_bitmap = wvo__uvhv
        context.nrt.incref(builder, signature.args[0], esdtn__wux)
        context.nrt.incref(builder, signature.args[1], wvo__uvhv)
        return jljpb__fdu._getvalue()
    precision = get_overload_const_int(precision_tp)
    scale = get_overload_const_int(scale_tp)
    ytf__eptcz = DecimalArrayType(precision, scale)
    nwt__cwlje = ytf__eptcz(data, null_bitmap, precision_tp, scale_tp)
    return nwt__cwlje, codegen


@lower_constant(DecimalArrayType)
def lower_constant_decimal_arr(context, builder, typ, pyval):
    n = len(pyval)
    ajc__xkpwn = context.get_constant(types.int64, n)
    oka__mxtzc = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(int128_type, 1, 'C'), [ajc__xkpwn])
    pdxut__yoip = np.empty(n + 7 >> 3, np.uint8)

    def f(arr, idx, val):
        arr[idx] = decimal128type_to_int128(val)
    for yadmh__ktzw, pwman__jrg in enumerate(pyval):
        wvub__nufk = pd.isna(pwman__jrg)
        bodo.libs.int_arr_ext.set_bit_to_arr(pdxut__yoip, yadmh__ktzw, int(
            not wvub__nufk))
        if not wvub__nufk:
            context.compile_internal(builder, f, types.void(types.Array(
                int128_type, 1, 'C'), types.int64, Decimal128Type(typ.
                precision, typ.scale)), [oka__mxtzc._getvalue(), context.
                get_constant(types.int64, yadmh__ktzw), context.
                get_constant_generic(builder, Decimal128Type(typ.precision,
                typ.scale), pwman__jrg)])
    ontk__pwn = context.get_constant_generic(builder, nulls_type, pdxut__yoip)
    jljpb__fdu = context.make_helper(builder, typ)
    jljpb__fdu.data = oka__mxtzc._getvalue()
    jljpb__fdu.null_bitmap = ontk__pwn
    return jljpb__fdu._getvalue()


@numba.njit(no_cpython_wrapper=True)
def alloc_decimal_array(n, precision, scale):
    qwy__qkvc = np.empty(n, dtype=int128_type)
    hvzl__kpvad = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_decimal_array(qwy__qkvc, hvzl__kpvad, precision, scale)


def alloc_decimal_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_decimal_arr_ext_alloc_decimal_array
    ) = alloc_decimal_array_equiv


@box(DecimalArrayType)
def box_decimal_arr(typ, val, c):
    eojg__vgb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    qwy__qkvc = c.context.make_array(types.Array(int128_type, 1, 'C'))(c.
        context, c.builder, eojg__vgb.data)
    qma__ywz = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, eojg__vgb.null_bitmap).data
    n = c.builder.extract_value(qwy__qkvc.shape, 0)
    scale = c.context.get_constant(types.int32, typ.scale)
    jqa__nqt = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(128).as_pointer(), lir.IntType(8).as_pointer(), lir.IntType
        (32)])
    vqu__kktn = cgutils.get_or_insert_function(c.builder.module, jqa__nqt,
        name='box_decimal_array')
    bqekt__mbj = c.builder.call(vqu__kktn, [n, qwy__qkvc.data, qma__ywz, scale]
        )
    c.context.nrt.decref(c.builder, typ, val)
    return bqekt__mbj


@unbox(DecimalArrayType)
def unbox_decimal_arr(typ, val, c):
    jljpb__fdu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qnd__oyse = c.pyapi.call_method(val, '__len__', ())
    n = c.pyapi.long_as_longlong(qnd__oyse)
    c.pyapi.decref(qnd__oyse)
    jywr__ekv = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    oka__mxtzc = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(int128_type, 1, 'C'), [n])
    gkjew__ymzsh = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [jywr__ekv])
    jqa__nqt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer(
        ), lir.IntType(64), lir.IntType(128).as_pointer(), lir.IntType(8).
        as_pointer()])
    lprjx__ttrle = cgutils.get_or_insert_function(c.builder.module,
        jqa__nqt, name='unbox_decimal_array')
    c.builder.call(lprjx__ttrle, [val, n, oka__mxtzc.data, gkjew__ymzsh.data])
    jljpb__fdu.null_bitmap = gkjew__ymzsh._getvalue()
    jljpb__fdu.data = oka__mxtzc._getvalue()
    kzf__jgsty = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jljpb__fdu._getvalue(), is_error=kzf__jgsty)


@overload_method(DecimalArrayType, 'copy', no_unliteral=True)
def overload_decimal_arr_copy(A):
    precision = A.precision
    scale = A.scale
    return lambda A: bodo.libs.decimal_arr_ext.init_decimal_array(A._data.
        copy(), A._null_bitmap.copy(), precision, scale)


@overload(len, no_unliteral=True)
def overload_decimal_arr_len(A):
    if isinstance(A, DecimalArrayType):
        return lambda A: len(A._data)


@overload_attribute(DecimalArrayType, 'shape')
def overload_decimal_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DecimalArrayType, 'dtype')
def overload_decimal_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(DecimalArrayType, 'ndim')
def overload_decimal_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DecimalArrayType, 'nbytes')
def decimal_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload(operator.setitem, no_unliteral=True)
def decimal_arr_setitem(A, idx, val):
    if not isinstance(A, DecimalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    bak__bvgq = (
        f"setitem for DecimalArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if isinstance(val, Decimal128Type):

            def impl_scalar(A, idx, val):
                A._data[idx] = decimal128type_to_int128(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(bak__bvgq)
    if not (is_iterable_type(val) and isinstance(val.dtype, bodo.
        Decimal128Type) or isinstance(val, Decimal128Type)):
        raise BodoError(bak__bvgq)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if isinstance(val, Decimal128Type):
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                decimal128type_to_int128(val))

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if isinstance(val, Decimal128Type):
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                decimal128type_to_int128(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if isinstance(val, Decimal128Type):
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                decimal128type_to_int128(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for DecimalArray with indexing type {idx} not supported.')


@overload(operator.getitem, no_unliteral=True)
def decimal_arr_getitem(A, ind):
    if not isinstance(A, DecimalArrayType):
        return
    if isinstance(ind, types.Integer):
        precision = A.precision
        scale = A.scale
        return lambda A, ind: int128_to_decimal128type(A._data[ind],
            precision, scale)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        precision = A.precision
        scale = A.scale

        def impl(A, ind):
            xpblm__pnksz, fpboa__rex = array_getitem_bool_index(A, ind)
            return init_decimal_array(xpblm__pnksz, fpboa__rex, precision,
                scale)
        return impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        precision = A.precision
        scale = A.scale

        def impl(A, ind):
            xpblm__pnksz, fpboa__rex = array_getitem_int_index(A, ind)
            return init_decimal_array(xpblm__pnksz, fpboa__rex, precision,
                scale)
        return impl
    if isinstance(ind, types.SliceType):
        precision = A.precision
        scale = A.scale

        def impl_slice(A, ind):
            xpblm__pnksz, fpboa__rex = array_getitem_slice_index(A, ind)
            return init_decimal_array(xpblm__pnksz, fpboa__rex, precision,
                scale)
        return impl_slice
    raise BodoError(
        f'getitem for DecimalArray with indexing type {ind} not supported.')
