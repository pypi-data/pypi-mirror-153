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
        xrrj__ulr = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, xrrj__ulr)


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
    nnou__jtu = c.context.insert_const_string(c.builder.module, 'pandas')
    eef__ztrbp = c.pyapi.import_module_noblock(nnou__jtu)
    rrt__eed = c.pyapi.call_method(eef__ztrbp, 'BooleanDtype', ())
    c.pyapi.decref(eef__ztrbp)
    return rrt__eed


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    kleaf__zvgih = n + 7 >> 3
    return np.full(kleaf__zvgih, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    sba__jfubu = c.context.typing_context.resolve_value_type(func)
    sice__rppt = sba__jfubu.get_call_type(c.context.typing_context,
        arg_typs, {})
    fvdse__riban = c.context.get_function(sba__jfubu, sice__rppt)
    rlqky__eyred = c.context.call_conv.get_function_type(sice__rppt.
        return_type, sice__rppt.args)
    wytct__vseu = c.builder.module
    bavm__rky = lir.Function(wytct__vseu, rlqky__eyred, name=wytct__vseu.
        get_unique_name('.func_conv'))
    bavm__rky.linkage = 'internal'
    mhfx__kpq = lir.IRBuilder(bavm__rky.append_basic_block())
    jio__voxjs = c.context.call_conv.decode_arguments(mhfx__kpq, sice__rppt
        .args, bavm__rky)
    uqugx__xjvl = fvdse__riban(mhfx__kpq, jio__voxjs)
    c.context.call_conv.return_value(mhfx__kpq, uqugx__xjvl)
    csh__syj, vguw__cdw = c.context.call_conv.call_function(c.builder,
        bavm__rky, sice__rppt.return_type, sice__rppt.args, args)
    return vguw__cdw


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    thfph__kjs = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(thfph__kjs)
    c.pyapi.decref(thfph__kjs)
    rlqky__eyred = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    yze__twl = cgutils.get_or_insert_function(c.builder.module,
        rlqky__eyred, name='is_bool_array')
    rlqky__eyred = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    bavm__rky = cgutils.get_or_insert_function(c.builder.module,
        rlqky__eyred, name='is_pd_boolean_array')
    gsd__qmc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qyleu__onbi = c.builder.call(bavm__rky, [obj])
    yqi__iixr = c.builder.icmp_unsigned('!=', qyleu__onbi, qyleu__onbi.type(0))
    with c.builder.if_else(yqi__iixr) as (pukq__iktep, jszf__xpk):
        with pukq__iktep:
            aqycn__rchby = c.pyapi.object_getattr_string(obj, '_data')
            gsd__qmc.data = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), aqycn__rchby).value
            simu__bre = c.pyapi.object_getattr_string(obj, '_mask')
            feqi__bzkvi = c.pyapi.to_native_value(types.Array(types.bool_, 
                1, 'C'), simu__bre).value
            kleaf__zvgih = c.builder.udiv(c.builder.add(n, lir.Constant(lir
                .IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            gan__fro = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, feqi__bzkvi)
            kelwp__uigzf = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [kleaf__zvgih])
            rlqky__eyred = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            bavm__rky = cgutils.get_or_insert_function(c.builder.module,
                rlqky__eyred, name='mask_arr_to_bitmap')
            c.builder.call(bavm__rky, [kelwp__uigzf.data, gan__fro.data, n])
            gsd__qmc.null_bitmap = kelwp__uigzf._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), feqi__bzkvi)
            c.pyapi.decref(aqycn__rchby)
            c.pyapi.decref(simu__bre)
        with jszf__xpk:
            swn__yucw = c.builder.call(yze__twl, [obj])
            bbjew__gtqf = c.builder.icmp_unsigned('!=', swn__yucw,
                swn__yucw.type(0))
            with c.builder.if_else(bbjew__gtqf) as (tni__mexz, shdp__qpg):
                with tni__mexz:
                    gsd__qmc.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    gsd__qmc.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with shdp__qpg:
                    gsd__qmc.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    kleaf__zvgih = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    gsd__qmc.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [kleaf__zvgih])._getvalue()
                    xtlj__ycym = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, gsd__qmc.data
                        ).data
                    pkf__ezlky = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, gsd__qmc.
                        null_bitmap).data
                    rlqky__eyred = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    bavm__rky = cgutils.get_or_insert_function(c.builder.
                        module, rlqky__eyred, name='unbox_bool_array_obj')
                    c.builder.call(bavm__rky, [obj, xtlj__ycym, pkf__ezlky, n])
    return NativeValue(gsd__qmc._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    gsd__qmc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        gsd__qmc.data, c.env_manager)
    ggwjq__biuyb = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, gsd__qmc.null_bitmap).data
    thfph__kjs = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(thfph__kjs)
    nnou__jtu = c.context.insert_const_string(c.builder.module, 'numpy')
    stle__oylcz = c.pyapi.import_module_noblock(nnou__jtu)
    nelp__dsmy = c.pyapi.object_getattr_string(stle__oylcz, 'bool_')
    feqi__bzkvi = c.pyapi.call_method(stle__oylcz, 'empty', (thfph__kjs,
        nelp__dsmy))
    vgo__awudk = c.pyapi.object_getattr_string(feqi__bzkvi, 'ctypes')
    oyrx__jmfrn = c.pyapi.object_getattr_string(vgo__awudk, 'data')
    let__nls = c.builder.inttoptr(c.pyapi.long_as_longlong(oyrx__jmfrn),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as rsnzx__wjmnq:
        hxbu__sdsr = rsnzx__wjmnq.index
        plqlt__vldvr = c.builder.lshr(hxbu__sdsr, lir.Constant(lir.IntType(
            64), 3))
        ljl__lsly = c.builder.load(cgutils.gep(c.builder, ggwjq__biuyb,
            plqlt__vldvr))
        tez__lbmbr = c.builder.trunc(c.builder.and_(hxbu__sdsr, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(ljl__lsly, tez__lbmbr), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        schkb__gfs = cgutils.gep(c.builder, let__nls, hxbu__sdsr)
        c.builder.store(val, schkb__gfs)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        gsd__qmc.null_bitmap)
    nnou__jtu = c.context.insert_const_string(c.builder.module, 'pandas')
    eef__ztrbp = c.pyapi.import_module_noblock(nnou__jtu)
    ykk__mlpwt = c.pyapi.object_getattr_string(eef__ztrbp, 'arrays')
    rrt__eed = c.pyapi.call_method(ykk__mlpwt, 'BooleanArray', (data,
        feqi__bzkvi))
    c.pyapi.decref(eef__ztrbp)
    c.pyapi.decref(thfph__kjs)
    c.pyapi.decref(stle__oylcz)
    c.pyapi.decref(nelp__dsmy)
    c.pyapi.decref(vgo__awudk)
    c.pyapi.decref(oyrx__jmfrn)
    c.pyapi.decref(ykk__mlpwt)
    c.pyapi.decref(data)
    c.pyapi.decref(feqi__bzkvi)
    return rrt__eed


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    dwl__rad = np.empty(n, np.bool_)
    qbr__htzw = np.empty(n + 7 >> 3, np.uint8)
    for hxbu__sdsr, s in enumerate(pyval):
        oreqe__jglxr = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(qbr__htzw, hxbu__sdsr, int(not
            oreqe__jglxr))
        if not oreqe__jglxr:
            dwl__rad[hxbu__sdsr] = s
    uplt__inkg = context.get_constant_generic(builder, data_type, dwl__rad)
    fuky__axwjo = context.get_constant_generic(builder, nulls_type, qbr__htzw)
    return lir.Constant.literal_struct([uplt__inkg, fuky__axwjo])


def lower_init_bool_array(context, builder, signature, args):
    jhrx__gpq, ttaz__dag = args
    gsd__qmc = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    gsd__qmc.data = jhrx__gpq
    gsd__qmc.null_bitmap = ttaz__dag
    context.nrt.incref(builder, signature.args[0], jhrx__gpq)
    context.nrt.incref(builder, signature.args[1], ttaz__dag)
    return gsd__qmc._getvalue()


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
    rtn__hnfgl = args[0]
    if equiv_set.has_shape(rtn__hnfgl):
        return ArrayAnalysis.AnalyzeResult(shape=rtn__hnfgl, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    rtn__hnfgl = args[0]
    if equiv_set.has_shape(rtn__hnfgl):
        return ArrayAnalysis.AnalyzeResult(shape=rtn__hnfgl, pre=[])
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
    dwl__rad = np.empty(n, dtype=np.bool_)
    neyl__zozn = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(dwl__rad, neyl__zozn)


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
            uqbag__qij, huya__tuwa = array_getitem_bool_index(A, ind)
            return init_bool_array(uqbag__qij, huya__tuwa)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            uqbag__qij, huya__tuwa = array_getitem_int_index(A, ind)
            return init_bool_array(uqbag__qij, huya__tuwa)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            uqbag__qij, huya__tuwa = array_getitem_slice_index(A, ind)
            return init_bool_array(uqbag__qij, huya__tuwa)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    xmfs__mbehw = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(xmfs__mbehw)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(xmfs__mbehw)
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
        for hxbu__sdsr in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, hxbu__sdsr):
                val = A[hxbu__sdsr]
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
            wkhic__sgxnh = np.empty(n, nb_dtype)
            for hxbu__sdsr in numba.parfors.parfor.internal_prange(n):
                wkhic__sgxnh[hxbu__sdsr] = data[hxbu__sdsr]
                if bodo.libs.array_kernels.isna(A, hxbu__sdsr):
                    wkhic__sgxnh[hxbu__sdsr] = np.nan
            return wkhic__sgxnh
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
    dma__xgdx = op.__name__
    dma__xgdx = ufunc_aliases.get(dma__xgdx, dma__xgdx)
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
    for mfl__cnazp in numba.np.ufunc_db.get_ufuncs():
        sahy__bqncn = create_op_overload(mfl__cnazp, mfl__cnazp.nin)
        overload(mfl__cnazp, no_unliteral=True)(sahy__bqncn)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        sahy__bqncn = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(sahy__bqncn)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        sahy__bqncn = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(sahy__bqncn)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        sahy__bqncn = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(sahy__bqncn)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        tez__lbmbr = []
        mgrit__gvg = False
        udv__vwz = False
        rmur__zmx = False
        for hxbu__sdsr in range(len(A)):
            if bodo.libs.array_kernels.isna(A, hxbu__sdsr):
                if not mgrit__gvg:
                    data.append(False)
                    tez__lbmbr.append(False)
                    mgrit__gvg = True
                continue
            val = A[hxbu__sdsr]
            if val and not udv__vwz:
                data.append(True)
                tez__lbmbr.append(True)
                udv__vwz = True
            if not val and not rmur__zmx:
                data.append(False)
                tez__lbmbr.append(True)
                rmur__zmx = True
            if mgrit__gvg and udv__vwz and rmur__zmx:
                break
        uqbag__qij = np.array(data)
        n = len(uqbag__qij)
        kleaf__zvgih = 1
        huya__tuwa = np.empty(kleaf__zvgih, np.uint8)
        for vrsxz__ntpdk in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(huya__tuwa, vrsxz__ntpdk,
                tez__lbmbr[vrsxz__ntpdk])
        return init_bool_array(uqbag__qij, huya__tuwa)
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
    rrt__eed = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, rrt__eed)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    jln__fwqzo = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        hxeoi__cjjwe = bodo.utils.utils.is_array_typ(val1, False)
        ecwj__lihjl = bodo.utils.utils.is_array_typ(val2, False)
        yhx__ckl = 'val1' if hxeoi__cjjwe else 'val2'
        des__pplc = 'def impl(val1, val2):\n'
        des__pplc += f'  n = len({yhx__ckl})\n'
        des__pplc += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        des__pplc += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if hxeoi__cjjwe:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            wtd__cqjhm = 'val1[i]'
        else:
            null1 = 'False\n'
            wtd__cqjhm = 'val1'
        if ecwj__lihjl:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            vfwih__rnd = 'val2[i]'
        else:
            null2 = 'False\n'
            vfwih__rnd = 'val2'
        if jln__fwqzo:
            des__pplc += f"""    result, isna_val = compute_or_body({null1}, {null2}, {wtd__cqjhm}, {vfwih__rnd})
"""
        else:
            des__pplc += f"""    result, isna_val = compute_and_body({null1}, {null2}, {wtd__cqjhm}, {vfwih__rnd})
"""
        des__pplc += '    out_arr[i] = result\n'
        des__pplc += '    if isna_val:\n'
        des__pplc += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        des__pplc += '      continue\n'
        des__pplc += '  return out_arr\n'
        fdzn__tdph = {}
        exec(des__pplc, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, fdzn__tdph)
        impl = fdzn__tdph['impl']
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
        aeasp__serqh = boolean_array
        return aeasp__serqh(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    bgl__kiwe = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return bgl__kiwe


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        vcj__utdgn = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(vcj__utdgn)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(vcj__utdgn)


_install_nullable_logical_lowering()
