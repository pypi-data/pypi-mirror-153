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
        fsyy__ftlgq = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, fsyy__ftlgq)


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
    xrb__avht = c.context.insert_const_string(c.builder.module, 'pandas')
    mupj__erd = c.pyapi.import_module_noblock(xrb__avht)
    gabbn__qcnt = c.pyapi.call_method(mupj__erd, 'BooleanDtype', ())
    c.pyapi.decref(mupj__erd)
    return gabbn__qcnt


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    zuumj__msz = n + 7 >> 3
    return np.full(zuumj__msz, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    xpw__jtd = c.context.typing_context.resolve_value_type(func)
    khkpx__lugr = xpw__jtd.get_call_type(c.context.typing_context, arg_typs, {}
        )
    cbo__pvc = c.context.get_function(xpw__jtd, khkpx__lugr)
    few__wwnz = c.context.call_conv.get_function_type(khkpx__lugr.
        return_type, khkpx__lugr.args)
    jarkj__wgsh = c.builder.module
    mody__cqh = lir.Function(jarkj__wgsh, few__wwnz, name=jarkj__wgsh.
        get_unique_name('.func_conv'))
    mody__cqh.linkage = 'internal'
    ktn__iad = lir.IRBuilder(mody__cqh.append_basic_block())
    tfppq__agzvd = c.context.call_conv.decode_arguments(ktn__iad,
        khkpx__lugr.args, mody__cqh)
    dqoc__jyh = cbo__pvc(ktn__iad, tfppq__agzvd)
    c.context.call_conv.return_value(ktn__iad, dqoc__jyh)
    oqbt__fjtzo, mokjr__zra = c.context.call_conv.call_function(c.builder,
        mody__cqh, khkpx__lugr.return_type, khkpx__lugr.args, args)
    return mokjr__zra


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    ytvak__verv = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ytvak__verv)
    c.pyapi.decref(ytvak__verv)
    few__wwnz = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    vdo__eut = cgutils.get_or_insert_function(c.builder.module, few__wwnz,
        name='is_bool_array')
    few__wwnz = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    mody__cqh = cgutils.get_or_insert_function(c.builder.module, few__wwnz,
        name='is_pd_boolean_array')
    gtlt__lnpt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fjhzh__nnw = c.builder.call(mody__cqh, [obj])
    vmywk__qqs = c.builder.icmp_unsigned('!=', fjhzh__nnw, fjhzh__nnw.type(0))
    with c.builder.if_else(vmywk__qqs) as (twl__cjiuy, lshv__xde):
        with twl__cjiuy:
            ddgpg__afrqs = c.pyapi.object_getattr_string(obj, '_data')
            gtlt__lnpt.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), ddgpg__afrqs).value
            jatdr__eby = c.pyapi.object_getattr_string(obj, '_mask')
            glgcu__edt = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), jatdr__eby).value
            zuumj__msz = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            ami__lbw = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, glgcu__edt)
            qeal__ateyr = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [zuumj__msz])
            few__wwnz = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            mody__cqh = cgutils.get_or_insert_function(c.builder.module,
                few__wwnz, name='mask_arr_to_bitmap')
            c.builder.call(mody__cqh, [qeal__ateyr.data, ami__lbw.data, n])
            gtlt__lnpt.null_bitmap = qeal__ateyr._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), glgcu__edt)
            c.pyapi.decref(ddgpg__afrqs)
            c.pyapi.decref(jatdr__eby)
        with lshv__xde:
            jfyg__ykgfz = c.builder.call(vdo__eut, [obj])
            qax__gdvm = c.builder.icmp_unsigned('!=', jfyg__ykgfz,
                jfyg__ykgfz.type(0))
            with c.builder.if_else(qax__gdvm) as (wmgmr__dpjr, evz__hqto):
                with wmgmr__dpjr:
                    gtlt__lnpt.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    gtlt__lnpt.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with evz__hqto:
                    gtlt__lnpt.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    zuumj__msz = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    gtlt__lnpt.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [zuumj__msz])._getvalue()
                    utqx__egn = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, gtlt__lnpt.data
                        ).data
                    ufy__yzjg = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, gtlt__lnpt.
                        null_bitmap).data
                    few__wwnz = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    mody__cqh = cgutils.get_or_insert_function(c.builder.
                        module, few__wwnz, name='unbox_bool_array_obj')
                    c.builder.call(mody__cqh, [obj, utqx__egn, ufy__yzjg, n])
    return NativeValue(gtlt__lnpt._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    gtlt__lnpt = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        gtlt__lnpt.data, c.env_manager)
    ymfcx__nag = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, gtlt__lnpt.null_bitmap).data
    ytvak__verv = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ytvak__verv)
    xrb__avht = c.context.insert_const_string(c.builder.module, 'numpy')
    sqap__zylcp = c.pyapi.import_module_noblock(xrb__avht)
    xdtyo__xdh = c.pyapi.object_getattr_string(sqap__zylcp, 'bool_')
    glgcu__edt = c.pyapi.call_method(sqap__zylcp, 'empty', (ytvak__verv,
        xdtyo__xdh))
    kzx__tan = c.pyapi.object_getattr_string(glgcu__edt, 'ctypes')
    dqkcx__bhw = c.pyapi.object_getattr_string(kzx__tan, 'data')
    cjcoa__jgeb = c.builder.inttoptr(c.pyapi.long_as_longlong(dqkcx__bhw),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as fjh__gcd:
        hvq__skzc = fjh__gcd.index
        fbt__lbuge = c.builder.lshr(hvq__skzc, lir.Constant(lir.IntType(64), 3)
            )
        svm__yid = c.builder.load(cgutils.gep(c.builder, ymfcx__nag,
            fbt__lbuge))
        ipjxm__juohk = c.builder.trunc(c.builder.and_(hvq__skzc, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(svm__yid, ipjxm__juohk), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        cif__wfjd = cgutils.gep(c.builder, cjcoa__jgeb, hvq__skzc)
        c.builder.store(val, cif__wfjd)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        gtlt__lnpt.null_bitmap)
    xrb__avht = c.context.insert_const_string(c.builder.module, 'pandas')
    mupj__erd = c.pyapi.import_module_noblock(xrb__avht)
    wavob__vwu = c.pyapi.object_getattr_string(mupj__erd, 'arrays')
    gabbn__qcnt = c.pyapi.call_method(wavob__vwu, 'BooleanArray', (data,
        glgcu__edt))
    c.pyapi.decref(mupj__erd)
    c.pyapi.decref(ytvak__verv)
    c.pyapi.decref(sqap__zylcp)
    c.pyapi.decref(xdtyo__xdh)
    c.pyapi.decref(kzx__tan)
    c.pyapi.decref(dqkcx__bhw)
    c.pyapi.decref(wavob__vwu)
    c.pyapi.decref(data)
    c.pyapi.decref(glgcu__edt)
    return gabbn__qcnt


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    pcc__jgdcs = np.empty(n, np.bool_)
    fyo__fxqr = np.empty(n + 7 >> 3, np.uint8)
    for hvq__skzc, s in enumerate(pyval):
        euc__jqkg = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(fyo__fxqr, hvq__skzc, int(not
            euc__jqkg))
        if not euc__jqkg:
            pcc__jgdcs[hvq__skzc] = s
    wtoey__mwsj = context.get_constant_generic(builder, data_type, pcc__jgdcs)
    kpvv__swsbm = context.get_constant_generic(builder, nulls_type, fyo__fxqr)
    return lir.Constant.literal_struct([wtoey__mwsj, kpvv__swsbm])


def lower_init_bool_array(context, builder, signature, args):
    gakj__adbd, hinvi__njtp = args
    gtlt__lnpt = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    gtlt__lnpt.data = gakj__adbd
    gtlt__lnpt.null_bitmap = hinvi__njtp
    context.nrt.incref(builder, signature.args[0], gakj__adbd)
    context.nrt.incref(builder, signature.args[1], hinvi__njtp)
    return gtlt__lnpt._getvalue()


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
    omdgp__lznx = args[0]
    if equiv_set.has_shape(omdgp__lznx):
        return ArrayAnalysis.AnalyzeResult(shape=omdgp__lznx, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    omdgp__lznx = args[0]
    if equiv_set.has_shape(omdgp__lznx):
        return ArrayAnalysis.AnalyzeResult(shape=omdgp__lznx, pre=[])
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
    pcc__jgdcs = np.empty(n, dtype=np.bool_)
    ldmar__duma = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(pcc__jgdcs, ldmar__duma)


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
            hviv__ygxu, esvxl__dmla = array_getitem_bool_index(A, ind)
            return init_bool_array(hviv__ygxu, esvxl__dmla)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            hviv__ygxu, esvxl__dmla = array_getitem_int_index(A, ind)
            return init_bool_array(hviv__ygxu, esvxl__dmla)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            hviv__ygxu, esvxl__dmla = array_getitem_slice_index(A, ind)
            return init_bool_array(hviv__ygxu, esvxl__dmla)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    usfi__yidkb = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(usfi__yidkb)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(usfi__yidkb)
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
        for hvq__skzc in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, hvq__skzc):
                val = A[hvq__skzc]
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
            bem__upaq = np.empty(n, nb_dtype)
            for hvq__skzc in numba.parfors.parfor.internal_prange(n):
                bem__upaq[hvq__skzc] = data[hvq__skzc]
                if bodo.libs.array_kernels.isna(A, hvq__skzc):
                    bem__upaq[hvq__skzc] = np.nan
            return bem__upaq
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
    jjpd__oxj = op.__name__
    jjpd__oxj = ufunc_aliases.get(jjpd__oxj, jjpd__oxj)
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
    for asap__ivml in numba.np.ufunc_db.get_ufuncs():
        tfeu__uyb = create_op_overload(asap__ivml, asap__ivml.nin)
        overload(asap__ivml, no_unliteral=True)(tfeu__uyb)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        tfeu__uyb = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(tfeu__uyb)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        tfeu__uyb = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(tfeu__uyb)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        tfeu__uyb = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(tfeu__uyb)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        ipjxm__juohk = []
        cmo__kba = False
        vflj__unom = False
        sgow__sju = False
        for hvq__skzc in range(len(A)):
            if bodo.libs.array_kernels.isna(A, hvq__skzc):
                if not cmo__kba:
                    data.append(False)
                    ipjxm__juohk.append(False)
                    cmo__kba = True
                continue
            val = A[hvq__skzc]
            if val and not vflj__unom:
                data.append(True)
                ipjxm__juohk.append(True)
                vflj__unom = True
            if not val and not sgow__sju:
                data.append(False)
                ipjxm__juohk.append(True)
                sgow__sju = True
            if cmo__kba and vflj__unom and sgow__sju:
                break
        hviv__ygxu = np.array(data)
        n = len(hviv__ygxu)
        zuumj__msz = 1
        esvxl__dmla = np.empty(zuumj__msz, np.uint8)
        for whch__zwoj in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(esvxl__dmla, whch__zwoj,
                ipjxm__juohk[whch__zwoj])
        return init_bool_array(hviv__ygxu, esvxl__dmla)
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
    gabbn__qcnt = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, gabbn__qcnt)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    cea__qez = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        rvoiq__nwf = bodo.utils.utils.is_array_typ(val1, False)
        licad__eplc = bodo.utils.utils.is_array_typ(val2, False)
        dnlmy__njwe = 'val1' if rvoiq__nwf else 'val2'
        oufxd__aaqu = 'def impl(val1, val2):\n'
        oufxd__aaqu += f'  n = len({dnlmy__njwe})\n'
        oufxd__aaqu += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        oufxd__aaqu += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if rvoiq__nwf:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            mvwn__awp = 'val1[i]'
        else:
            null1 = 'False\n'
            mvwn__awp = 'val1'
        if licad__eplc:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            ryzs__boxip = 'val2[i]'
        else:
            null2 = 'False\n'
            ryzs__boxip = 'val2'
        if cea__qez:
            oufxd__aaqu += f"""    result, isna_val = compute_or_body({null1}, {null2}, {mvwn__awp}, {ryzs__boxip})
"""
        else:
            oufxd__aaqu += f"""    result, isna_val = compute_and_body({null1}, {null2}, {mvwn__awp}, {ryzs__boxip})
"""
        oufxd__aaqu += '    out_arr[i] = result\n'
        oufxd__aaqu += '    if isna_val:\n'
        oufxd__aaqu += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        oufxd__aaqu += '      continue\n'
        oufxd__aaqu += '  return out_arr\n'
        herl__nmmm = {}
        exec(oufxd__aaqu, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, herl__nmmm)
        impl = herl__nmmm['impl']
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
        obfy__hout = boolean_array
        return obfy__hout(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    zosq__wxq = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return zosq__wxq


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        rsslv__aahtn = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(rsslv__aahtn)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(rsslv__aahtn)


_install_nullable_logical_lowering()
