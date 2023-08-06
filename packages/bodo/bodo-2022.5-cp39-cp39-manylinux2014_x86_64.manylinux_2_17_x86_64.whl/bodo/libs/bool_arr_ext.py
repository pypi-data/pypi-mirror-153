"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kcra__tqo = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, kcra__tqo)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    dlx__nmbu = c.context.insert_const_string(c.builder.module, 'pandas')
    hmzy__oftpx = c.pyapi.import_module_noblock(dlx__nmbu)
    qkanq__afznx = c.pyapi.call_method(hmzy__oftpx, 'BooleanDtype', ())
    c.pyapi.decref(hmzy__oftpx)
    return qkanq__afznx


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    lcmkd__lmbf = n + 7 >> 3
    return np.full(lcmkd__lmbf, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    lsl__zfpm = c.context.typing_context.resolve_value_type(func)
    irama__qezh = lsl__zfpm.get_call_type(c.context.typing_context,
        arg_typs, {})
    dekdv__fif = c.context.get_function(lsl__zfpm, irama__qezh)
    zkvd__muob = c.context.call_conv.get_function_type(irama__qezh.
        return_type, irama__qezh.args)
    awhe__cxvua = c.builder.module
    qtxf__fmntq = lir.Function(awhe__cxvua, zkvd__muob, name=awhe__cxvua.
        get_unique_name('.func_conv'))
    qtxf__fmntq.linkage = 'internal'
    kxhxe__jqvd = lir.IRBuilder(qtxf__fmntq.append_basic_block())
    dxjw__jmj = c.context.call_conv.decode_arguments(kxhxe__jqvd,
        irama__qezh.args, qtxf__fmntq)
    qcr__ykz = dekdv__fif(kxhxe__jqvd, dxjw__jmj)
    c.context.call_conv.return_value(kxhxe__jqvd, qcr__ykz)
    oyvj__zsmu, jyf__yzwhm = c.context.call_conv.call_function(c.builder,
        qtxf__fmntq, irama__qezh.return_type, irama__qezh.args, args)
    return jyf__yzwhm


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    maeq__mdo = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(maeq__mdo)
    c.pyapi.decref(maeq__mdo)
    zkvd__muob = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    gltf__ppi = cgutils.get_or_insert_function(c.builder.module, zkvd__muob,
        name='is_bool_array')
    zkvd__muob = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    qtxf__fmntq = cgutils.get_or_insert_function(c.builder.module,
        zkvd__muob, name='is_pd_boolean_array')
    rtif__dxp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tfsxq__esgpm = c.builder.call(qtxf__fmntq, [obj])
    qyjyi__zqfj = c.builder.icmp_unsigned('!=', tfsxq__esgpm, tfsxq__esgpm.
        type(0))
    with c.builder.if_else(qyjyi__zqfj) as (gljg__spxay, hawjx__wfg):
        with gljg__spxay:
            umbq__pjiu = c.pyapi.object_getattr_string(obj, '_data')
            rtif__dxp.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), umbq__pjiu).value
            ylf__vyvd = c.pyapi.object_getattr_string(obj, '_mask')
            kdxw__ljgl = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), ylf__vyvd).value
            lcmkd__lmbf = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            pnvez__ajtbt = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, kdxw__ljgl)
            ieva__xwz = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [lcmkd__lmbf])
            zkvd__muob = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            qtxf__fmntq = cgutils.get_or_insert_function(c.builder.module,
                zkvd__muob, name='mask_arr_to_bitmap')
            c.builder.call(qtxf__fmntq, [ieva__xwz.data, pnvez__ajtbt.data, n])
            rtif__dxp.null_bitmap = ieva__xwz._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), kdxw__ljgl)
            c.pyapi.decref(umbq__pjiu)
            c.pyapi.decref(ylf__vyvd)
        with hawjx__wfg:
            ywbyw__rbowi = c.builder.call(gltf__ppi, [obj])
            ntm__uok = c.builder.icmp_unsigned('!=', ywbyw__rbowi,
                ywbyw__rbowi.type(0))
            with c.builder.if_else(ntm__uok) as (sctjv__ohmxn, ojsh__ultf):
                with sctjv__ohmxn:
                    rtif__dxp.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    rtif__dxp.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with ojsh__ultf:
                    rtif__dxp.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    lcmkd__lmbf = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    rtif__dxp.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [lcmkd__lmbf])._getvalue()
                    kpksr__txdan = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, rtif__dxp.data
                        ).data
                    lry__umuru = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, rtif__dxp.
                        null_bitmap).data
                    zkvd__muob = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    qtxf__fmntq = cgutils.get_or_insert_function(c.builder.
                        module, zkvd__muob, name='unbox_bool_array_obj')
                    c.builder.call(qtxf__fmntq, [obj, kpksr__txdan,
                        lry__umuru, n])
    return NativeValue(rtif__dxp._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    rtif__dxp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        rtif__dxp.data, c.env_manager)
    ldnev__ukjxy = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, rtif__dxp.null_bitmap).data
    maeq__mdo = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(maeq__mdo)
    dlx__nmbu = c.context.insert_const_string(c.builder.module, 'numpy')
    ofg__ynonc = c.pyapi.import_module_noblock(dlx__nmbu)
    sfsly__ufuk = c.pyapi.object_getattr_string(ofg__ynonc, 'bool_')
    kdxw__ljgl = c.pyapi.call_method(ofg__ynonc, 'empty', (maeq__mdo,
        sfsly__ufuk))
    vifa__vdukb = c.pyapi.object_getattr_string(kdxw__ljgl, 'ctypes')
    hwfsg__zaihs = c.pyapi.object_getattr_string(vifa__vdukb, 'data')
    cpyw__kjd = c.builder.inttoptr(c.pyapi.long_as_longlong(hwfsg__zaihs),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as tfftq__ofaxx:
        puz__wgt = tfftq__ofaxx.index
        xvqi__gsr = c.builder.lshr(puz__wgt, lir.Constant(lir.IntType(64), 3))
        kzbbp__hwe = c.builder.load(cgutils.gep(c.builder, ldnev__ukjxy,
            xvqi__gsr))
        kasft__nype = c.builder.trunc(c.builder.and_(puz__wgt, lir.Constant
            (lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(kzbbp__hwe, kasft__nype), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        pjhfh__swjrq = cgutils.gep(c.builder, cpyw__kjd, puz__wgt)
        c.builder.store(val, pjhfh__swjrq)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        rtif__dxp.null_bitmap)
    dlx__nmbu = c.context.insert_const_string(c.builder.module, 'pandas')
    hmzy__oftpx = c.pyapi.import_module_noblock(dlx__nmbu)
    urs__xbom = c.pyapi.object_getattr_string(hmzy__oftpx, 'arrays')
    qkanq__afznx = c.pyapi.call_method(urs__xbom, 'BooleanArray', (data,
        kdxw__ljgl))
    c.pyapi.decref(hmzy__oftpx)
    c.pyapi.decref(maeq__mdo)
    c.pyapi.decref(ofg__ynonc)
    c.pyapi.decref(sfsly__ufuk)
    c.pyapi.decref(vifa__vdukb)
    c.pyapi.decref(hwfsg__zaihs)
    c.pyapi.decref(urs__xbom)
    c.pyapi.decref(data)
    c.pyapi.decref(kdxw__ljgl)
    return qkanq__afznx


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    ffp__aew = np.empty(n, np.bool_)
    kcbfq__gvtou = np.empty(n + 7 >> 3, np.uint8)
    for puz__wgt, s in enumerate(pyval):
        cqx__zvb = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(kcbfq__gvtou, puz__wgt, int(
            not cqx__zvb))
        if not cqx__zvb:
            ffp__aew[puz__wgt] = s
    rxy__rlt = context.get_constant_generic(builder, data_type, ffp__aew)
    vfj__jro = context.get_constant_generic(builder, nulls_type, kcbfq__gvtou)
    return lir.Constant.literal_struct([rxy__rlt, vfj__jro])


def lower_init_bool_array(context, builder, signature, args):
    kggy__uvpyn, qmz__jabi = args
    rtif__dxp = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    rtif__dxp.data = kggy__uvpyn
    rtif__dxp.null_bitmap = qmz__jabi
    context.nrt.incref(builder, signature.args[0], kggy__uvpyn)
    context.nrt.incref(builder, signature.args[1], qmz__jabi)
    return rtif__dxp._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    krif__cfymk = args[0]
    if equiv_set.has_shape(krif__cfymk):
        return ArrayAnalysis.AnalyzeResult(shape=krif__cfymk, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    krif__cfymk = args[0]
    if equiv_set.has_shape(krif__cfymk):
        return ArrayAnalysis.AnalyzeResult(shape=krif__cfymk, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    ffp__aew = np.empty(n, dtype=np.bool_)
    fpt__qoaxf = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(ffp__aew, fpt__qoaxf)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ivti__ahcv, uvox__kto = array_getitem_bool_index(A, ind)
            return init_bool_array(ivti__ahcv, uvox__kto)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ivti__ahcv, uvox__kto = array_getitem_int_index(A, ind)
            return init_bool_array(ivti__ahcv, uvox__kto)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ivti__ahcv, uvox__kto = array_getitem_slice_index(A, ind)
            return init_bool_array(ivti__ahcv, uvox__kto)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    afjc__pac = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(afjc__pac)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(afjc__pac)
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
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for puz__wgt in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, puz__wgt):
                val = A[puz__wgt]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
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
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            lrto__qmlcy = np.empty(n, nb_dtype)
            for puz__wgt in numba.parfors.parfor.internal_prange(n):
                lrto__qmlcy[puz__wgt] = data[puz__wgt]
                if bodo.libs.array_kernels.isna(A, puz__wgt):
                    lrto__qmlcy[puz__wgt] = np.nan
            return lrto__qmlcy
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    ncqgl__uzfq = op.__name__
    ncqgl__uzfq = ufunc_aliases.get(ncqgl__uzfq, ncqgl__uzfq)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for fqr__kwcb in numba.np.ufunc_db.get_ufuncs():
        ecy__tgxs = create_op_overload(fqr__kwcb, fqr__kwcb.nin)
        overload(fqr__kwcb, no_unliteral=True)(ecy__tgxs)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        ecy__tgxs = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(ecy__tgxs)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        ecy__tgxs = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(ecy__tgxs)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        ecy__tgxs = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(ecy__tgxs)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        kasft__nype = []
        eavbk__hjtwn = False
        ojeks__lypbc = False
        thyc__onpip = False
        for puz__wgt in range(len(A)):
            if bodo.libs.array_kernels.isna(A, puz__wgt):
                if not eavbk__hjtwn:
                    data.append(False)
                    kasft__nype.append(False)
                    eavbk__hjtwn = True
                continue
            val = A[puz__wgt]
            if val and not ojeks__lypbc:
                data.append(True)
                kasft__nype.append(True)
                ojeks__lypbc = True
            if not val and not thyc__onpip:
                data.append(False)
                kasft__nype.append(True)
                thyc__onpip = True
            if eavbk__hjtwn and ojeks__lypbc and thyc__onpip:
                break
        ivti__ahcv = np.array(data)
        n = len(ivti__ahcv)
        lcmkd__lmbf = 1
        uvox__kto = np.empty(lcmkd__lmbf, np.uint8)
        for vvkue__qid in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(uvox__kto, vvkue__qid,
                kasft__nype[vvkue__qid])
        return init_bool_array(ivti__ahcv, uvox__kto)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType)) or isinstance(A, bodo.libs.
        struct_arr_ext.StructArrayType) or isinstance(A, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType) or isinstance(A, bodo.libs.
        map_arr_ext.MapArrayType) or A in (string_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type, boolean_array)):
        return lambda A, ind: A[ind._data]


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    qkanq__afznx = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, qkanq__afznx)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    xpztj__uixy = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        ivd__lwvca = bodo.utils.utils.is_array_typ(val1, False)
        zif__gqnah = bodo.utils.utils.is_array_typ(val2, False)
        exlb__rufd = 'val1' if ivd__lwvca else 'val2'
        buu__kwd = 'def impl(val1, val2):\n'
        buu__kwd += f'  n = len({exlb__rufd})\n'
        buu__kwd += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        buu__kwd += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if ivd__lwvca:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            zmydh__whxbq = 'val1[i]'
        else:
            null1 = 'False\n'
            zmydh__whxbq = 'val1'
        if zif__gqnah:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            oyoty__dasok = 'val2[i]'
        else:
            null2 = 'False\n'
            oyoty__dasok = 'val2'
        if xpztj__uixy:
            buu__kwd += f"""    result, isna_val = compute_or_body({null1}, {null2}, {zmydh__whxbq}, {oyoty__dasok})
"""
        else:
            buu__kwd += f"""    result, isna_val = compute_and_body({null1}, {null2}, {zmydh__whxbq}, {oyoty__dasok})
"""
        buu__kwd += '    out_arr[i] = result\n'
        buu__kwd += '    if isna_val:\n'
        buu__kwd += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        buu__kwd += '      continue\n'
        buu__kwd += '  return out_arr\n'
        emxxq__qmwiq = {}
        exec(buu__kwd, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, emxxq__qmwiq
            )
        impl = emxxq__qmwiq['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        bnsm__pyu = boolean_array
        return bnsm__pyu(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    whd__dvo = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array) and (
        bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype == types.
        bool_ or typ1 == types.bool_) and (bodo.utils.utils.is_array_typ(
        typ2, False) and typ2.dtype == types.bool_ or typ2 == types.bool_)
    return whd__dvo


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        udlo__pjt = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(udlo__pjt)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(udlo__pjt)


_install_nullable_logical_lowering()
