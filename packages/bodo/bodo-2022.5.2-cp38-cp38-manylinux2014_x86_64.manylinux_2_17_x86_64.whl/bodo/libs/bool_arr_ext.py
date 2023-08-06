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
        edqdi__awgga = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, edqdi__awgga)


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
    iajl__kjqtp = c.context.insert_const_string(c.builder.module, 'pandas')
    uzr__hmdrf = c.pyapi.import_module_noblock(iajl__kjqtp)
    xzzwk__kiq = c.pyapi.call_method(uzr__hmdrf, 'BooleanDtype', ())
    c.pyapi.decref(uzr__hmdrf)
    return xzzwk__kiq


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    epe__ufta = n + 7 >> 3
    return np.full(epe__ufta, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    imgeb__dpsse = c.context.typing_context.resolve_value_type(func)
    wgtpb__aul = imgeb__dpsse.get_call_type(c.context.typing_context,
        arg_typs, {})
    mdwtb__lih = c.context.get_function(imgeb__dpsse, wgtpb__aul)
    gyn__tnwa = c.context.call_conv.get_function_type(wgtpb__aul.
        return_type, wgtpb__aul.args)
    mcpi__doyrk = c.builder.module
    ncyc__swvjw = lir.Function(mcpi__doyrk, gyn__tnwa, name=mcpi__doyrk.
        get_unique_name('.func_conv'))
    ncyc__swvjw.linkage = 'internal'
    yyney__tpmrg = lir.IRBuilder(ncyc__swvjw.append_basic_block())
    hpn__wazyj = c.context.call_conv.decode_arguments(yyney__tpmrg,
        wgtpb__aul.args, ncyc__swvjw)
    geh__ucyib = mdwtb__lih(yyney__tpmrg, hpn__wazyj)
    c.context.call_conv.return_value(yyney__tpmrg, geh__ucyib)
    dpc__vnpwq, aesau__absr = c.context.call_conv.call_function(c.builder,
        ncyc__swvjw, wgtpb__aul.return_type, wgtpb__aul.args, args)
    return aesau__absr


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    spe__mcy = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(spe__mcy)
    c.pyapi.decref(spe__mcy)
    gyn__tnwa = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    nqp__vcodn = cgutils.get_or_insert_function(c.builder.module, gyn__tnwa,
        name='is_bool_array')
    gyn__tnwa = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    ncyc__swvjw = cgutils.get_or_insert_function(c.builder.module,
        gyn__tnwa, name='is_pd_boolean_array')
    wjqas__vipej = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gsa__zyt = c.builder.call(ncyc__swvjw, [obj])
    efy__eizzo = c.builder.icmp_unsigned('!=', gsa__zyt, gsa__zyt.type(0))
    with c.builder.if_else(efy__eizzo) as (nrz__bxrky, cknx__hkow):
        with nrz__bxrky:
            frxx__jll = c.pyapi.object_getattr_string(obj, '_data')
            wjqas__vipej.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), frxx__jll).value
            quzif__aeigv = c.pyapi.object_getattr_string(obj, '_mask')
            dsg__ycc = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), quzif__aeigv).value
            epe__ufta = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            yqtso__gmo = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, dsg__ycc)
            jyzy__uotl = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [epe__ufta])
            gyn__tnwa = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            ncyc__swvjw = cgutils.get_or_insert_function(c.builder.module,
                gyn__tnwa, name='mask_arr_to_bitmap')
            c.builder.call(ncyc__swvjw, [jyzy__uotl.data, yqtso__gmo.data, n])
            wjqas__vipej.null_bitmap = jyzy__uotl._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), dsg__ycc)
            c.pyapi.decref(frxx__jll)
            c.pyapi.decref(quzif__aeigv)
        with cknx__hkow:
            brhrh__djqn = c.builder.call(nqp__vcodn, [obj])
            qpv__xnu = c.builder.icmp_unsigned('!=', brhrh__djqn,
                brhrh__djqn.type(0))
            with c.builder.if_else(qpv__xnu) as (uwxm__xbph, jkm__ofjus):
                with uwxm__xbph:
                    wjqas__vipej.data = c.pyapi.to_native_value(types.Array
                        (types.bool_, 1, 'C'), obj).value
                    wjqas__vipej.null_bitmap = call_func_in_unbox(
                        gen_full_bitmap, (n,), (types.int64,), c)
                with jkm__ofjus:
                    wjqas__vipej.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    epe__ufta = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    wjqas__vipej.null_bitmap = bodo.utils.utils._empty_nd_impl(
                        c.context, c.builder, types.Array(types.uint8, 1,
                        'C'), [epe__ufta])._getvalue()
                    nyowg__fagc = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, wjqas__vipej.data
                        ).data
                    bcgsk__zni = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, wjqas__vipej.
                        null_bitmap).data
                    gyn__tnwa = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    ncyc__swvjw = cgutils.get_or_insert_function(c.builder.
                        module, gyn__tnwa, name='unbox_bool_array_obj')
                    c.builder.call(ncyc__swvjw, [obj, nyowg__fagc,
                        bcgsk__zni, n])
    return NativeValue(wjqas__vipej._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    wjqas__vipej = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        wjqas__vipej.data, c.env_manager)
    gce__ntbw = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, wjqas__vipej.null_bitmap).data
    spe__mcy = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(spe__mcy)
    iajl__kjqtp = c.context.insert_const_string(c.builder.module, 'numpy')
    fxr__lzp = c.pyapi.import_module_noblock(iajl__kjqtp)
    skgv__vks = c.pyapi.object_getattr_string(fxr__lzp, 'bool_')
    dsg__ycc = c.pyapi.call_method(fxr__lzp, 'empty', (spe__mcy, skgv__vks))
    jvy__apjcg = c.pyapi.object_getattr_string(dsg__ycc, 'ctypes')
    enzzi__huty = c.pyapi.object_getattr_string(jvy__apjcg, 'data')
    movgq__jeij = c.builder.inttoptr(c.pyapi.long_as_longlong(enzzi__huty),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as uxhr__pepop:
        ggr__vyl = uxhr__pepop.index
        cyjb__dbcji = c.builder.lshr(ggr__vyl, lir.Constant(lir.IntType(64), 3)
            )
        ycec__osr = c.builder.load(cgutils.gep(c.builder, gce__ntbw,
            cyjb__dbcji))
        nwkk__gvip = c.builder.trunc(c.builder.and_(ggr__vyl, lir.Constant(
            lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(ycec__osr, nwkk__gvip), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        dxmn__sjz = cgutils.gep(c.builder, movgq__jeij, ggr__vyl)
        c.builder.store(val, dxmn__sjz)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        wjqas__vipej.null_bitmap)
    iajl__kjqtp = c.context.insert_const_string(c.builder.module, 'pandas')
    uzr__hmdrf = c.pyapi.import_module_noblock(iajl__kjqtp)
    uvicu__otkau = c.pyapi.object_getattr_string(uzr__hmdrf, 'arrays')
    xzzwk__kiq = c.pyapi.call_method(uvicu__otkau, 'BooleanArray', (data,
        dsg__ycc))
    c.pyapi.decref(uzr__hmdrf)
    c.pyapi.decref(spe__mcy)
    c.pyapi.decref(fxr__lzp)
    c.pyapi.decref(skgv__vks)
    c.pyapi.decref(jvy__apjcg)
    c.pyapi.decref(enzzi__huty)
    c.pyapi.decref(uvicu__otkau)
    c.pyapi.decref(data)
    c.pyapi.decref(dsg__ycc)
    return xzzwk__kiq


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    bgvki__mjr = np.empty(n, np.bool_)
    essal__ijuhf = np.empty(n + 7 >> 3, np.uint8)
    for ggr__vyl, s in enumerate(pyval):
        nvsh__ssd = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(essal__ijuhf, ggr__vyl, int(
            not nvsh__ssd))
        if not nvsh__ssd:
            bgvki__mjr[ggr__vyl] = s
    guwk__mhke = context.get_constant_generic(builder, data_type, bgvki__mjr)
    isqf__olda = context.get_constant_generic(builder, nulls_type, essal__ijuhf
        )
    return lir.Constant.literal_struct([guwk__mhke, isqf__olda])


def lower_init_bool_array(context, builder, signature, args):
    cnzzj__eob, exi__ewgwt = args
    wjqas__vipej = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    wjqas__vipej.data = cnzzj__eob
    wjqas__vipej.null_bitmap = exi__ewgwt
    context.nrt.incref(builder, signature.args[0], cnzzj__eob)
    context.nrt.incref(builder, signature.args[1], exi__ewgwt)
    return wjqas__vipej._getvalue()


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
    qlxzc__bdoti = args[0]
    if equiv_set.has_shape(qlxzc__bdoti):
        return ArrayAnalysis.AnalyzeResult(shape=qlxzc__bdoti, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    qlxzc__bdoti = args[0]
    if equiv_set.has_shape(qlxzc__bdoti):
        return ArrayAnalysis.AnalyzeResult(shape=qlxzc__bdoti, pre=[])
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
    bgvki__mjr = np.empty(n, dtype=np.bool_)
    onbo__guot = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(bgvki__mjr, onbo__guot)


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
            zkgh__ebwzw, opp__jaikj = array_getitem_bool_index(A, ind)
            return init_bool_array(zkgh__ebwzw, opp__jaikj)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            zkgh__ebwzw, opp__jaikj = array_getitem_int_index(A, ind)
            return init_bool_array(zkgh__ebwzw, opp__jaikj)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            zkgh__ebwzw, opp__jaikj = array_getitem_slice_index(A, ind)
            return init_bool_array(zkgh__ebwzw, opp__jaikj)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    wre__emw = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(wre__emw)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(wre__emw)
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
        for ggr__vyl in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, ggr__vyl):
                val = A[ggr__vyl]
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
            vom__xkero = np.empty(n, nb_dtype)
            for ggr__vyl in numba.parfors.parfor.internal_prange(n):
                vom__xkero[ggr__vyl] = data[ggr__vyl]
                if bodo.libs.array_kernels.isna(A, ggr__vyl):
                    vom__xkero[ggr__vyl] = np.nan
            return vom__xkero
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
    zald__gbsmj = op.__name__
    zald__gbsmj = ufunc_aliases.get(zald__gbsmj, zald__gbsmj)
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
    for sext__cnm in numba.np.ufunc_db.get_ufuncs():
        cou__qqu = create_op_overload(sext__cnm, sext__cnm.nin)
        overload(sext__cnm, no_unliteral=True)(cou__qqu)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        cou__qqu = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(cou__qqu)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        cou__qqu = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(cou__qqu)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        cou__qqu = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(cou__qqu)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        nwkk__gvip = []
        mdd__pzwga = False
        iug__auxi = False
        mjw__qdmr = False
        for ggr__vyl in range(len(A)):
            if bodo.libs.array_kernels.isna(A, ggr__vyl):
                if not mdd__pzwga:
                    data.append(False)
                    nwkk__gvip.append(False)
                    mdd__pzwga = True
                continue
            val = A[ggr__vyl]
            if val and not iug__auxi:
                data.append(True)
                nwkk__gvip.append(True)
                iug__auxi = True
            if not val and not mjw__qdmr:
                data.append(False)
                nwkk__gvip.append(True)
                mjw__qdmr = True
            if mdd__pzwga and iug__auxi and mjw__qdmr:
                break
        zkgh__ebwzw = np.array(data)
        n = len(zkgh__ebwzw)
        epe__ufta = 1
        opp__jaikj = np.empty(epe__ufta, np.uint8)
        for ega__udmd in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(opp__jaikj, ega__udmd,
                nwkk__gvip[ega__udmd])
        return init_bool_array(zkgh__ebwzw, opp__jaikj)
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
    xzzwk__kiq = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, xzzwk__kiq)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    gnef__aax = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        bdsqk__utbs = bodo.utils.utils.is_array_typ(val1, False)
        rsi__vbcel = bodo.utils.utils.is_array_typ(val2, False)
        hqwn__egkzr = 'val1' if bdsqk__utbs else 'val2'
        znbb__mqm = 'def impl(val1, val2):\n'
        znbb__mqm += f'  n = len({hqwn__egkzr})\n'
        znbb__mqm += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        znbb__mqm += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if bdsqk__utbs:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            vbza__uocy = 'val1[i]'
        else:
            null1 = 'False\n'
            vbza__uocy = 'val1'
        if rsi__vbcel:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            bbcdx__pwen = 'val2[i]'
        else:
            null2 = 'False\n'
            bbcdx__pwen = 'val2'
        if gnef__aax:
            znbb__mqm += f"""    result, isna_val = compute_or_body({null1}, {null2}, {vbza__uocy}, {bbcdx__pwen})
"""
        else:
            znbb__mqm += f"""    result, isna_val = compute_and_body({null1}, {null2}, {vbza__uocy}, {bbcdx__pwen})
"""
        znbb__mqm += '    out_arr[i] = result\n'
        znbb__mqm += '    if isna_val:\n'
        znbb__mqm += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        znbb__mqm += '      continue\n'
        znbb__mqm += '  return out_arr\n'
        ocsfn__bxu = {}
        exec(znbb__mqm, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, ocsfn__bxu)
        impl = ocsfn__bxu['impl']
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
        kekd__lump = boolean_array
        return kekd__lump(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    myx__gajhl = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return myx__gajhl


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        qtrgr__spjlz = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(qtrgr__spjlz)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(qtrgr__spjlz)


_install_nullable_logical_lowering()
