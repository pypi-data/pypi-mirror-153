import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        tkq__iolle = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=tkq__iolle)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    bwxg__hsoxb = tuple(val.categories.values)
    elem_type = None if len(bwxg__hsoxb) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(bwxg__hsoxb, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bitsg__fnnwo = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, bitsg__fnnwo)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    ntf__tvrf = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    hil__hmvp = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, hcqga__tdm, hcqga__tdm = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    myewg__hbhy = PDCategoricalDtype(hil__hmvp, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, ntf__tvrf)
    return myewg__hbhy(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    aqpa__uui = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, aqpa__uui).value
    c.pyapi.decref(aqpa__uui)
    zatb__rlb = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, zatb__rlb).value
    c.pyapi.decref(zatb__rlb)
    fkmhi__swlu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=fkmhi__swlu)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    aqpa__uui = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    nsazk__lknv = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    vvwn__zuw = c.context.insert_const_string(c.builder.module, 'pandas')
    cop__jnx = c.pyapi.import_module_noblock(vvwn__zuw)
    wyybj__iuw = c.pyapi.call_method(cop__jnx, 'CategoricalDtype', (
        nsazk__lknv, aqpa__uui))
    c.pyapi.decref(aqpa__uui)
    c.pyapi.decref(nsazk__lknv)
    c.pyapi.decref(cop__jnx)
    c.context.nrt.decref(c.builder, typ, val)
    return wyybj__iuw


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zvnnd__bszce = get_categories_int_type(fe_type.dtype)
        bitsg__fnnwo = [('dtype', fe_type.dtype), ('codes', types.Array(
            zvnnd__bszce, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, bitsg__fnnwo)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    owzwq__nqjmb = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), owzwq__nqjmb
        ).value
    c.pyapi.decref(owzwq__nqjmb)
    wyybj__iuw = c.pyapi.object_getattr_string(val, 'dtype')
    qwgn__ssyji = c.pyapi.to_native_value(typ.dtype, wyybj__iuw).value
    c.pyapi.decref(wyybj__iuw)
    xqov__iqivx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xqov__iqivx.codes = codes
    xqov__iqivx.dtype = qwgn__ssyji
    return NativeValue(xqov__iqivx._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    mbt__xiupc = get_categories_int_type(typ.dtype)
    jztih__qpv = context.get_constant_generic(builder, types.Array(
        mbt__xiupc, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, jztih__qpv])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    swm__ctty = len(cat_dtype.categories)
    if swm__ctty < np.iinfo(np.int8).max:
        dtype = types.int8
    elif swm__ctty < np.iinfo(np.int16).max:
        dtype = types.int16
    elif swm__ctty < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    vvwn__zuw = c.context.insert_const_string(c.builder.module, 'pandas')
    cop__jnx = c.pyapi.import_module_noblock(vvwn__zuw)
    zvnnd__bszce = get_categories_int_type(dtype)
    muf__amwdz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    jgg__quqva = types.Array(zvnnd__bszce, 1, 'C')
    c.context.nrt.incref(c.builder, jgg__quqva, muf__amwdz.codes)
    owzwq__nqjmb = c.pyapi.from_native_value(jgg__quqva, muf__amwdz.codes,
        c.env_manager)
    c.context.nrt.incref(c.builder, dtype, muf__amwdz.dtype)
    wyybj__iuw = c.pyapi.from_native_value(dtype, muf__amwdz.dtype, c.
        env_manager)
    pcp__dejdi = c.pyapi.borrow_none()
    eaom__bcg = c.pyapi.object_getattr_string(cop__jnx, 'Categorical')
    kjmpn__yma = c.pyapi.call_method(eaom__bcg, 'from_codes', (owzwq__nqjmb,
        pcp__dejdi, pcp__dejdi, wyybj__iuw))
    c.pyapi.decref(eaom__bcg)
    c.pyapi.decref(owzwq__nqjmb)
    c.pyapi.decref(wyybj__iuw)
    c.pyapi.decref(cop__jnx)
    c.context.nrt.decref(c.builder, typ, val)
    return kjmpn__yma


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            iucf__qoe = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                acjke__dgi = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), iucf__qoe)
                return acjke__dgi
            return impl_lit

        def impl(A, other):
            iucf__qoe = get_code_for_value(A.dtype, other)
            acjke__dgi = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), iucf__qoe)
            return acjke__dgi
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        dxcco__gtum = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(dxcco__gtum)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    muf__amwdz = cat_dtype.categories
    n = len(muf__amwdz)
    for ifpn__jym in range(n):
        if muf__amwdz[ifpn__jym] == val:
            return ifpn__jym
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    natji__sbfev = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if (natji__sbfev != A.dtype.elem_type and natji__sbfev != types.
        unicode_type):
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if natji__sbfev == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            acjke__dgi = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for ifpn__jym in numba.parfors.parfor.internal_prange(n):
                rstz__fah = codes[ifpn__jym]
                if rstz__fah == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(acjke__dgi
                            , ifpn__jym)
                    else:
                        bodo.libs.array_kernels.setna(acjke__dgi, ifpn__jym)
                    continue
                acjke__dgi[ifpn__jym] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[rstz__fah]))
            return acjke__dgi
        return impl
    jgg__quqva = dtype_to_array_type(natji__sbfev)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        acjke__dgi = bodo.utils.utils.alloc_type(n, jgg__quqva, (-1,))
        for ifpn__jym in numba.parfors.parfor.internal_prange(n):
            rstz__fah = codes[ifpn__jym]
            if rstz__fah == -1:
                bodo.libs.array_kernels.setna(acjke__dgi, ifpn__jym)
                continue
            acjke__dgi[ifpn__jym] = bodo.utils.conversion.unbox_if_timestamp(
                categories[rstz__fah])
        return acjke__dgi
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        kkjtt__jnard, qwgn__ssyji = args
        muf__amwdz = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        muf__amwdz.codes = kkjtt__jnard
        muf__amwdz.dtype = qwgn__ssyji
        context.nrt.incref(builder, signature.args[0], kkjtt__jnard)
        context.nrt.incref(builder, signature.args[1], qwgn__ssyji)
        return muf__amwdz._getvalue()
    des__jfbvm = CategoricalArrayType(cat_dtype)
    sig = des__jfbvm(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    vilbf__idsnp = args[0]
    if equiv_set.has_shape(vilbf__idsnp):
        return ArrayAnalysis.AnalyzeResult(shape=vilbf__idsnp, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    zvnnd__bszce = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, zvnnd__bszce)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            ehd__rao = {}
            jztih__qpv = np.empty(n + 1, np.int64)
            qsnak__gkl = {}
            vkd__mtqi = []
            mwg__ymwpn = {}
            for ifpn__jym in range(n):
                mwg__ymwpn[categories[ifpn__jym]] = ifpn__jym
            for wvh__jzzfk in to_replace:
                if wvh__jzzfk != value:
                    if wvh__jzzfk in mwg__ymwpn:
                        if value in mwg__ymwpn:
                            ehd__rao[wvh__jzzfk] = wvh__jzzfk
                            kadk__oyv = mwg__ymwpn[wvh__jzzfk]
                            qsnak__gkl[kadk__oyv] = mwg__ymwpn[value]
                            vkd__mtqi.append(kadk__oyv)
                        else:
                            ehd__rao[wvh__jzzfk] = value
                            mwg__ymwpn[value] = mwg__ymwpn[wvh__jzzfk]
            vrr__agy = np.sort(np.array(vkd__mtqi))
            ersua__ljt = 0
            noe__tkal = []
            for ugbg__gskwa in range(-1, n):
                while ersua__ljt < len(vrr__agy) and ugbg__gskwa > vrr__agy[
                    ersua__ljt]:
                    ersua__ljt += 1
                noe__tkal.append(ersua__ljt)
            for bwkbd__zwrto in range(-1, n):
                susqn__vayd = bwkbd__zwrto
                if bwkbd__zwrto in qsnak__gkl:
                    susqn__vayd = qsnak__gkl[bwkbd__zwrto]
                jztih__qpv[bwkbd__zwrto + 1] = susqn__vayd - noe__tkal[
                    susqn__vayd + 1]
            return ehd__rao, jztih__qpv, len(vrr__agy)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for ifpn__jym in range(len(new_codes_arr)):
        new_codes_arr[ifpn__jym] = codes_map_arr[old_codes_arr[ifpn__jym] + 1]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    chwq__kck = arr.dtype.ordered
    ipv__evphk = arr.dtype.elem_type
    mqwfl__wamx = get_overload_const(to_replace)
    oblo__mhrm = get_overload_const(value)
    if (arr.dtype.categories is not None and mqwfl__wamx is not
        NOT_CONSTANT and oblo__mhrm is not NOT_CONSTANT):
        paqwm__jmi, codes_map_arr, hcqga__tdm = python_build_replace_dicts(
            mqwfl__wamx, oblo__mhrm, arr.dtype.categories)
        if len(paqwm__jmi) == 0:
            return lambda arr, to_replace, value: arr.copy()
        qknuo__lct = []
        for fwcpb__vvqkj in arr.dtype.categories:
            if fwcpb__vvqkj in paqwm__jmi:
                yop__qjezm = paqwm__jmi[fwcpb__vvqkj]
                if yop__qjezm != fwcpb__vvqkj:
                    qknuo__lct.append(yop__qjezm)
            else:
                qknuo__lct.append(fwcpb__vvqkj)
        cdjm__drff = pd.CategoricalDtype(qknuo__lct, chwq__kck
            ).categories.values
        xbiyi__xsg = MetaType(tuple(cdjm__drff))

        def impl_dtype(arr, to_replace, value):
            xoksx__tva = init_cat_dtype(bodo.utils.conversion.
                index_from_array(cdjm__drff), chwq__kck, None, xbiyi__xsg)
            muf__amwdz = alloc_categorical_array(len(arr.codes), xoksx__tva)
            reassign_codes(muf__amwdz.codes, arr.codes, codes_map_arr)
            return muf__amwdz
        return impl_dtype
    ipv__evphk = arr.dtype.elem_type
    if ipv__evphk == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            ehd__rao, codes_map_arr, jad__uhkx = build_replace_dicts(to_replace
                , value, categories.values)
            if len(ehd__rao) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), chwq__kck,
                    None, None))
            n = len(categories)
            cdjm__drff = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                jad__uhkx, -1)
            dkumj__shka = 0
            for ugbg__gskwa in range(n):
                ily__xugo = categories[ugbg__gskwa]
                if ily__xugo in ehd__rao:
                    qewjs__xpej = ehd__rao[ily__xugo]
                    if qewjs__xpej != ily__xugo:
                        cdjm__drff[dkumj__shka] = qewjs__xpej
                        dkumj__shka += 1
                else:
                    cdjm__drff[dkumj__shka] = ily__xugo
                    dkumj__shka += 1
            muf__amwdz = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                cdjm__drff), chwq__kck, None, None))
            reassign_codes(muf__amwdz.codes, arr.codes, codes_map_arr)
            return muf__amwdz
        return impl_str
    xqu__fins = dtype_to_array_type(ipv__evphk)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        ehd__rao, codes_map_arr, jad__uhkx = build_replace_dicts(to_replace,
            value, categories.values)
        if len(ehd__rao) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), chwq__kck, None, None))
        n = len(categories)
        cdjm__drff = bodo.utils.utils.alloc_type(n - jad__uhkx, xqu__fins, None
            )
        dkumj__shka = 0
        for ifpn__jym in range(n):
            ily__xugo = categories[ifpn__jym]
            if ily__xugo in ehd__rao:
                qewjs__xpej = ehd__rao[ily__xugo]
                if qewjs__xpej != ily__xugo:
                    cdjm__drff[dkumj__shka] = qewjs__xpej
                    dkumj__shka += 1
            else:
                cdjm__drff[dkumj__shka] = ily__xugo
                dkumj__shka += 1
        muf__amwdz = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(cdjm__drff), chwq__kck,
            None, None))
        reassign_codes(muf__amwdz.codes, arr.codes, codes_map_arr)
        return muf__amwdz
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    weai__ibhld = dict()
    qtqln__ibwbb = 0
    for ifpn__jym in range(len(vals)):
        val = vals[ifpn__jym]
        if val in weai__ibhld:
            continue
        weai__ibhld[val] = qtqln__ibwbb
        qtqln__ibwbb += 1
    return weai__ibhld


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    weai__ibhld = dict()
    for ifpn__jym in range(len(vals)):
        val = vals[ifpn__jym]
        weai__ibhld[val] = ifpn__jym
    return weai__ibhld


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    gxefo__egoj = dict(fastpath=fastpath)
    dpsj__mbj = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', gxefo__egoj, dpsj__mbj)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        foyl__exirf = get_overload_const(categories)
        if foyl__exirf is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                vaft__qwja = False
            else:
                vaft__qwja = get_overload_const_bool(ordered)
            raspt__dwx = pd.CategoricalDtype(foyl__exirf, vaft__qwja
                ).categories.values
            wkn__etik = MetaType(tuple(raspt__dwx))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                xoksx__tva = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(raspt__dwx), vaft__qwja, None, wkn__etik)
                return bodo.utils.conversion.fix_arr_dtype(data, xoksx__tva)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            bwxg__hsoxb = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                bwxg__hsoxb, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            okup__zxdt = arr.codes[ind]
            return arr.dtype.categories[max(okup__zxdt, 0)]
        return categorical_getitem_impl
    if is_list_like_index_type(ind) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    raise BodoError(
        f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
        )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for ifpn__jym in range(len(arr1)):
        if arr1[ifpn__jym] != arr2[ifpn__jym]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    bvje__kuqv = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    yiso__uen = not isinstance(val, CategoricalArrayType) and is_iterable_type(
        val) and is_common_scalar_dtype([val.dtype, arr.dtype.elem_type]
        ) and not (isinstance(arr.dtype.elem_type, types.Integer) and
        isinstance(val.dtype, types.Float))
    rqiqi__xtts = categorical_arrs_match(arr, val)
    cje__jmeky = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    uhnce__niam = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not bvje__kuqv:
            raise BodoError(cje__jmeky)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            okup__zxdt = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = okup__zxdt
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (bvje__kuqv or yiso__uen or rqiqi__xtts !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(cje__jmeky)
        if rqiqi__xtts == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(uhnce__niam)
        if bvje__kuqv:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                hbk__ynokg = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for ugbg__gskwa in range(n):
                    arr.codes[ind[ugbg__gskwa]] = hbk__ynokg
            return impl_scalar
        if rqiqi__xtts == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for ifpn__jym in range(n):
                    arr.codes[ind[ifpn__jym]] = val.codes[ifpn__jym]
            return impl_arr_ind_mask
        if rqiqi__xtts == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(uhnce__niam)
                n = len(val.codes)
                for ifpn__jym in range(n):
                    arr.codes[ind[ifpn__jym]] = val.codes[ifpn__jym]
            return impl_arr_ind_mask
        if yiso__uen:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for ugbg__gskwa in range(n):
                    six__uvvtu = bodo.utils.conversion.unbox_if_timestamp(val
                        [ugbg__gskwa])
                    if six__uvvtu not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    okup__zxdt = categories.get_loc(six__uvvtu)
                    arr.codes[ind[ugbg__gskwa]] = okup__zxdt
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (bvje__kuqv or yiso__uen or rqiqi__xtts !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(cje__jmeky)
        if rqiqi__xtts == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(uhnce__niam)
        if bvje__kuqv:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                hbk__ynokg = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for ugbg__gskwa in range(n):
                    if ind[ugbg__gskwa]:
                        arr.codes[ugbg__gskwa] = hbk__ynokg
            return impl_scalar
        if rqiqi__xtts == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                pigcy__xvc = 0
                for ifpn__jym in range(n):
                    if ind[ifpn__jym]:
                        arr.codes[ifpn__jym] = val.codes[pigcy__xvc]
                        pigcy__xvc += 1
            return impl_bool_ind_mask
        if rqiqi__xtts == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(uhnce__niam)
                n = len(ind)
                pigcy__xvc = 0
                for ifpn__jym in range(n):
                    if ind[ifpn__jym]:
                        arr.codes[ifpn__jym] = val.codes[pigcy__xvc]
                        pigcy__xvc += 1
            return impl_bool_ind_mask
        if yiso__uen:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                pigcy__xvc = 0
                categories = arr.dtype.categories
                for ugbg__gskwa in range(n):
                    if ind[ugbg__gskwa]:
                        six__uvvtu = bodo.utils.conversion.unbox_if_timestamp(
                            val[pigcy__xvc])
                        if six__uvvtu not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        okup__zxdt = categories.get_loc(six__uvvtu)
                        arr.codes[ugbg__gskwa] = okup__zxdt
                        pigcy__xvc += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (bvje__kuqv or yiso__uen or rqiqi__xtts !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(cje__jmeky)
        if rqiqi__xtts == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(uhnce__niam)
        if bvje__kuqv:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                hbk__ynokg = arr.dtype.categories.get_loc(val)
                dthx__iptxs = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for ugbg__gskwa in range(dthx__iptxs.start, dthx__iptxs.
                    stop, dthx__iptxs.step):
                    arr.codes[ugbg__gskwa] = hbk__ynokg
            return impl_scalar
        if rqiqi__xtts == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if rqiqi__xtts == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(uhnce__niam)
                arr.codes[ind] = val.codes
            return impl_arr
        if yiso__uen:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                dthx__iptxs = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                pigcy__xvc = 0
                for ugbg__gskwa in range(dthx__iptxs.start, dthx__iptxs.
                    stop, dthx__iptxs.step):
                    six__uvvtu = bodo.utils.conversion.unbox_if_timestamp(val
                        [pigcy__xvc])
                    if six__uvvtu not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    okup__zxdt = categories.get_loc(six__uvvtu)
                    arr.codes[ugbg__gskwa] = okup__zxdt
                    pigcy__xvc += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
