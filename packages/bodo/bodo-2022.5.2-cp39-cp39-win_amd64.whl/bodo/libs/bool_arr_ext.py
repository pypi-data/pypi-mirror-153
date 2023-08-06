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
        myaae__rce = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, myaae__rce)


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
    dmbm__geg = c.context.insert_const_string(c.builder.module, 'pandas')
    aapn__ybvm = c.pyapi.import_module_noblock(dmbm__geg)
    yjz__ioyb = c.pyapi.call_method(aapn__ybvm, 'BooleanDtype', ())
    c.pyapi.decref(aapn__ybvm)
    return yjz__ioyb


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    kvp__eql = n + 7 >> 3
    return np.full(kvp__eql, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    nwqqi__hxdho = c.context.typing_context.resolve_value_type(func)
    lnbvc__bmk = nwqqi__hxdho.get_call_type(c.context.typing_context,
        arg_typs, {})
    wkwvw__hcqx = c.context.get_function(nwqqi__hxdho, lnbvc__bmk)
    qbkvu__huh = c.context.call_conv.get_function_type(lnbvc__bmk.
        return_type, lnbvc__bmk.args)
    llbt__gfl = c.builder.module
    sfru__hsjsh = lir.Function(llbt__gfl, qbkvu__huh, name=llbt__gfl.
        get_unique_name('.func_conv'))
    sfru__hsjsh.linkage = 'internal'
    wks__lhn = lir.IRBuilder(sfru__hsjsh.append_basic_block())
    cod__iui = c.context.call_conv.decode_arguments(wks__lhn, lnbvc__bmk.
        args, sfru__hsjsh)
    uot__aqk = wkwvw__hcqx(wks__lhn, cod__iui)
    c.context.call_conv.return_value(wks__lhn, uot__aqk)
    jmp__fgd, jva__igx = c.context.call_conv.call_function(c.builder,
        sfru__hsjsh, lnbvc__bmk.return_type, lnbvc__bmk.args, args)
    return jva__igx


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    oyap__xlw = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(oyap__xlw)
    c.pyapi.decref(oyap__xlw)
    qbkvu__huh = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    xiu__nzlm = cgutils.get_or_insert_function(c.builder.module, qbkvu__huh,
        name='is_bool_array')
    qbkvu__huh = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    sfru__hsjsh = cgutils.get_or_insert_function(c.builder.module,
        qbkvu__huh, name='is_pd_boolean_array')
    hxxni__bqvk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    iur__pkgo = c.builder.call(sfru__hsjsh, [obj])
    gpq__xyre = c.builder.icmp_unsigned('!=', iur__pkgo, iur__pkgo.type(0))
    with c.builder.if_else(gpq__xyre) as (ieh__qljs, pqc__xazw):
        with ieh__qljs:
            hwf__hznnb = c.pyapi.object_getattr_string(obj, '_data')
            hxxni__bqvk.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), hwf__hznnb).value
            ubqct__pslbe = c.pyapi.object_getattr_string(obj, '_mask')
            koy__wtzm = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), ubqct__pslbe).value
            kvp__eql = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            pwjkd__ufu = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, koy__wtzm)
            utfpr__mmbnc = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [kvp__eql])
            qbkvu__huh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            sfru__hsjsh = cgutils.get_or_insert_function(c.builder.module,
                qbkvu__huh, name='mask_arr_to_bitmap')
            c.builder.call(sfru__hsjsh, [utfpr__mmbnc.data, pwjkd__ufu.data, n]
                )
            hxxni__bqvk.null_bitmap = utfpr__mmbnc._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), koy__wtzm)
            c.pyapi.decref(hwf__hznnb)
            c.pyapi.decref(ubqct__pslbe)
        with pqc__xazw:
            uezs__lhnee = c.builder.call(xiu__nzlm, [obj])
            chxk__hgmc = c.builder.icmp_unsigned('!=', uezs__lhnee,
                uezs__lhnee.type(0))
            with c.builder.if_else(chxk__hgmc) as (gsci__bjirw, bilk__xktw):
                with gsci__bjirw:
                    hxxni__bqvk.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    hxxni__bqvk.null_bitmap = call_func_in_unbox(
                        gen_full_bitmap, (n,), (types.int64,), c)
                with bilk__xktw:
                    hxxni__bqvk.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    kvp__eql = c.builder.udiv(c.builder.add(n, lir.Constant
                        (lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8)
                        )
                    hxxni__bqvk.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [kvp__eql])._getvalue()
                    avrce__fjow = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, hxxni__bqvk.data
                        ).data
                    giyh__bku = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, hxxni__bqvk.
                        null_bitmap).data
                    qbkvu__huh = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    sfru__hsjsh = cgutils.get_or_insert_function(c.builder.
                        module, qbkvu__huh, name='unbox_bool_array_obj')
                    c.builder.call(sfru__hsjsh, [obj, avrce__fjow,
                        giyh__bku, n])
    return NativeValue(hxxni__bqvk._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    hxxni__bqvk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        hxxni__bqvk.data, c.env_manager)
    vmhby__odr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, hxxni__bqvk.null_bitmap).data
    oyap__xlw = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(oyap__xlw)
    dmbm__geg = c.context.insert_const_string(c.builder.module, 'numpy')
    qosv__mvtt = c.pyapi.import_module_noblock(dmbm__geg)
    fgbx__ribwr = c.pyapi.object_getattr_string(qosv__mvtt, 'bool_')
    koy__wtzm = c.pyapi.call_method(qosv__mvtt, 'empty', (oyap__xlw,
        fgbx__ribwr))
    elif__gwock = c.pyapi.object_getattr_string(koy__wtzm, 'ctypes')
    kenq__wjyx = c.pyapi.object_getattr_string(elif__gwock, 'data')
    bpmp__tckgm = c.builder.inttoptr(c.pyapi.long_as_longlong(kenq__wjyx),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as nljzj__yyv:
        igs__abh = nljzj__yyv.index
        ynv__hwrd = c.builder.lshr(igs__abh, lir.Constant(lir.IntType(64), 3))
        qku__qnbsv = c.builder.load(cgutils.gep(c.builder, vmhby__odr,
            ynv__hwrd))
        shf__oakr = c.builder.trunc(c.builder.and_(igs__abh, lir.Constant(
            lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(qku__qnbsv, shf__oakr), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        wzxh__obn = cgutils.gep(c.builder, bpmp__tckgm, igs__abh)
        c.builder.store(val, wzxh__obn)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        hxxni__bqvk.null_bitmap)
    dmbm__geg = c.context.insert_const_string(c.builder.module, 'pandas')
    aapn__ybvm = c.pyapi.import_module_noblock(dmbm__geg)
    ikc__zmbuh = c.pyapi.object_getattr_string(aapn__ybvm, 'arrays')
    yjz__ioyb = c.pyapi.call_method(ikc__zmbuh, 'BooleanArray', (data,
        koy__wtzm))
    c.pyapi.decref(aapn__ybvm)
    c.pyapi.decref(oyap__xlw)
    c.pyapi.decref(qosv__mvtt)
    c.pyapi.decref(fgbx__ribwr)
    c.pyapi.decref(elif__gwock)
    c.pyapi.decref(kenq__wjyx)
    c.pyapi.decref(ikc__zmbuh)
    c.pyapi.decref(data)
    c.pyapi.decref(koy__wtzm)
    return yjz__ioyb


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    djq__dpshw = np.empty(n, np.bool_)
    yajoc__fxccm = np.empty(n + 7 >> 3, np.uint8)
    for igs__abh, s in enumerate(pyval):
        avqji__rampx = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(yajoc__fxccm, igs__abh, int(
            not avqji__rampx))
        if not avqji__rampx:
            djq__dpshw[igs__abh] = s
    sds__edoa = context.get_constant_generic(builder, data_type, djq__dpshw)
    iiy__cfc = context.get_constant_generic(builder, nulls_type, yajoc__fxccm)
    return lir.Constant.literal_struct([sds__edoa, iiy__cfc])


def lower_init_bool_array(context, builder, signature, args):
    oszi__pgg, dbvvu__cdqo = args
    hxxni__bqvk = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    hxxni__bqvk.data = oszi__pgg
    hxxni__bqvk.null_bitmap = dbvvu__cdqo
    context.nrt.incref(builder, signature.args[0], oszi__pgg)
    context.nrt.incref(builder, signature.args[1], dbvvu__cdqo)
    return hxxni__bqvk._getvalue()


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
    tztn__ddbh = args[0]
    if equiv_set.has_shape(tztn__ddbh):
        return ArrayAnalysis.AnalyzeResult(shape=tztn__ddbh, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    tztn__ddbh = args[0]
    if equiv_set.has_shape(tztn__ddbh):
        return ArrayAnalysis.AnalyzeResult(shape=tztn__ddbh, pre=[])
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
    djq__dpshw = np.empty(n, dtype=np.bool_)
    fge__etrcl = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(djq__dpshw, fge__etrcl)


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
            uhztw__yrn, jxh__juz = array_getitem_bool_index(A, ind)
            return init_bool_array(uhztw__yrn, jxh__juz)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            uhztw__yrn, jxh__juz = array_getitem_int_index(A, ind)
            return init_bool_array(uhztw__yrn, jxh__juz)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            uhztw__yrn, jxh__juz = array_getitem_slice_index(A, ind)
            return init_bool_array(uhztw__yrn, jxh__juz)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    acvbp__iut = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(acvbp__iut)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(acvbp__iut)
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
        for igs__abh in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, igs__abh):
                val = A[igs__abh]
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
            pkqnw__pyvdn = np.empty(n, nb_dtype)
            for igs__abh in numba.parfors.parfor.internal_prange(n):
                pkqnw__pyvdn[igs__abh] = data[igs__abh]
                if bodo.libs.array_kernels.isna(A, igs__abh):
                    pkqnw__pyvdn[igs__abh] = np.nan
            return pkqnw__pyvdn
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
    qazcg__ofql = op.__name__
    qazcg__ofql = ufunc_aliases.get(qazcg__ofql, qazcg__ofql)
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
    for haphp__nln in numba.np.ufunc_db.get_ufuncs():
        qsil__eufj = create_op_overload(haphp__nln, haphp__nln.nin)
        overload(haphp__nln, no_unliteral=True)(qsil__eufj)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        qsil__eufj = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qsil__eufj)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        qsil__eufj = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qsil__eufj)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        qsil__eufj = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(qsil__eufj)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        shf__oakr = []
        vxqzi__nwi = False
        rng__kzjp = False
        zoc__hhy = False
        for igs__abh in range(len(A)):
            if bodo.libs.array_kernels.isna(A, igs__abh):
                if not vxqzi__nwi:
                    data.append(False)
                    shf__oakr.append(False)
                    vxqzi__nwi = True
                continue
            val = A[igs__abh]
            if val and not rng__kzjp:
                data.append(True)
                shf__oakr.append(True)
                rng__kzjp = True
            if not val and not zoc__hhy:
                data.append(False)
                shf__oakr.append(True)
                zoc__hhy = True
            if vxqzi__nwi and rng__kzjp and zoc__hhy:
                break
        uhztw__yrn = np.array(data)
        n = len(uhztw__yrn)
        kvp__eql = 1
        jxh__juz = np.empty(kvp__eql, np.uint8)
        for tect__arso in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(jxh__juz, tect__arso,
                shf__oakr[tect__arso])
        return init_bool_array(uhztw__yrn, jxh__juz)
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
    yjz__ioyb = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, yjz__ioyb)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    bhwlv__rhvsa = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        dmnsq__lrvr = bodo.utils.utils.is_array_typ(val1, False)
        dau__msvn = bodo.utils.utils.is_array_typ(val2, False)
        ruhj__hbpe = 'val1' if dmnsq__lrvr else 'val2'
        hdap__zgi = 'def impl(val1, val2):\n'
        hdap__zgi += f'  n = len({ruhj__hbpe})\n'
        hdap__zgi += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        hdap__zgi += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if dmnsq__lrvr:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            xqep__mobb = 'val1[i]'
        else:
            null1 = 'False\n'
            xqep__mobb = 'val1'
        if dau__msvn:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            kgve__hxau = 'val2[i]'
        else:
            null2 = 'False\n'
            kgve__hxau = 'val2'
        if bhwlv__rhvsa:
            hdap__zgi += f"""    result, isna_val = compute_or_body({null1}, {null2}, {xqep__mobb}, {kgve__hxau})
"""
        else:
            hdap__zgi += f"""    result, isna_val = compute_and_body({null1}, {null2}, {xqep__mobb}, {kgve__hxau})
"""
        hdap__zgi += '    out_arr[i] = result\n'
        hdap__zgi += '    if isna_val:\n'
        hdap__zgi += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        hdap__zgi += '      continue\n'
        hdap__zgi += '  return out_arr\n'
        huu__gyns = {}
        exec(hdap__zgi, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, huu__gyns)
        impl = huu__gyns['impl']
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
        ryiyn__fri = boolean_array
        return ryiyn__fri(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    wzij__xawu = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return wzij__xawu


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        mqphb__yylho = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(mqphb__yylho)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(mqphb__yylho)


_install_nullable_logical_lowering()
