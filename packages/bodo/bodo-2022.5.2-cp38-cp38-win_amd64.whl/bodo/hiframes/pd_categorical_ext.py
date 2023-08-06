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
        tcsxc__phks = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=tcsxc__phks)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    mbiq__rsytb = tuple(val.categories.values)
    elem_type = None if len(mbiq__rsytb) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(mbiq__rsytb, elem_type, val.ordered, bodo.
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
        ezedw__pwm = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ezedw__pwm)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    uutyd__jdq = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    aciva__shusg = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, bfuxx__yoyn, bfuxx__yoyn = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    wryof__agfpp = PDCategoricalDtype(aciva__shusg, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, uutyd__jdq)
    return wryof__agfpp(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oeri__tirz = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, oeri__tirz).value
    c.pyapi.decref(oeri__tirz)
    qzvia__ymh = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, qzvia__ymh).value
    c.pyapi.decref(qzvia__ymh)
    amw__wiq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=amw__wiq)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    oeri__tirz = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    usx__tgs = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c.
        env_manager)
    ghih__jmr = c.context.insert_const_string(c.builder.module, 'pandas')
    npimk__mbutq = c.pyapi.import_module_noblock(ghih__jmr)
    bfd__efhtj = c.pyapi.call_method(npimk__mbutq, 'CategoricalDtype', (
        usx__tgs, oeri__tirz))
    c.pyapi.decref(oeri__tirz)
    c.pyapi.decref(usx__tgs)
    c.pyapi.decref(npimk__mbutq)
    c.context.nrt.decref(c.builder, typ, val)
    return bfd__efhtj


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
        wsd__roswc = get_categories_int_type(fe_type.dtype)
        ezedw__pwm = [('dtype', fe_type.dtype), ('codes', types.Array(
            wsd__roswc, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, ezedw__pwm)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    obp__gvhpu = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), obp__gvhpu
        ).value
    c.pyapi.decref(obp__gvhpu)
    bfd__efhtj = c.pyapi.object_getattr_string(val, 'dtype')
    ktm__iov = c.pyapi.to_native_value(typ.dtype, bfd__efhtj).value
    c.pyapi.decref(bfd__efhtj)
    qemg__mablw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qemg__mablw.codes = codes
    qemg__mablw.dtype = ktm__iov
    return NativeValue(qemg__mablw._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    juv__xjn = get_categories_int_type(typ.dtype)
    oppr__hrmih = context.get_constant_generic(builder, types.Array(
        juv__xjn, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, oppr__hrmih])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    cvpz__gpry = len(cat_dtype.categories)
    if cvpz__gpry < np.iinfo(np.int8).max:
        dtype = types.int8
    elif cvpz__gpry < np.iinfo(np.int16).max:
        dtype = types.int16
    elif cvpz__gpry < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    ghih__jmr = c.context.insert_const_string(c.builder.module, 'pandas')
    npimk__mbutq = c.pyapi.import_module_noblock(ghih__jmr)
    wsd__roswc = get_categories_int_type(dtype)
    mjfi__fhsfm = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    mmv__atlnk = types.Array(wsd__roswc, 1, 'C')
    c.context.nrt.incref(c.builder, mmv__atlnk, mjfi__fhsfm.codes)
    obp__gvhpu = c.pyapi.from_native_value(mmv__atlnk, mjfi__fhsfm.codes, c
        .env_manager)
    c.context.nrt.incref(c.builder, dtype, mjfi__fhsfm.dtype)
    bfd__efhtj = c.pyapi.from_native_value(dtype, mjfi__fhsfm.dtype, c.
        env_manager)
    sqb__fzp = c.pyapi.borrow_none()
    mmsuf__sqlj = c.pyapi.object_getattr_string(npimk__mbutq, 'Categorical')
    vgc__inc = c.pyapi.call_method(mmsuf__sqlj, 'from_codes', (obp__gvhpu,
        sqb__fzp, sqb__fzp, bfd__efhtj))
    c.pyapi.decref(mmsuf__sqlj)
    c.pyapi.decref(obp__gvhpu)
    c.pyapi.decref(bfd__efhtj)
    c.pyapi.decref(npimk__mbutq)
    c.context.nrt.decref(c.builder, typ, val)
    return vgc__inc


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
            rpuf__zhrro = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                uuao__slxcl = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), rpuf__zhrro)
                return uuao__slxcl
            return impl_lit

        def impl(A, other):
            rpuf__zhrro = get_code_for_value(A.dtype, other)
            uuao__slxcl = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), rpuf__zhrro)
            return uuao__slxcl
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        fivgi__gljm = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(fivgi__gljm)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    mjfi__fhsfm = cat_dtype.categories
    n = len(mjfi__fhsfm)
    for kkdz__hqi in range(n):
        if mjfi__fhsfm[kkdz__hqi] == val:
            return kkdz__hqi
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    bkhk__crppj = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if bkhk__crppj != A.dtype.elem_type and bkhk__crppj != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if bkhk__crppj == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            uuao__slxcl = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for kkdz__hqi in numba.parfors.parfor.internal_prange(n):
                sersz__krr = codes[kkdz__hqi]
                if sersz__krr == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            uuao__slxcl, kkdz__hqi)
                    else:
                        bodo.libs.array_kernels.setna(uuao__slxcl, kkdz__hqi)
                    continue
                uuao__slxcl[kkdz__hqi] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[sersz__krr]))
            return uuao__slxcl
        return impl
    mmv__atlnk = dtype_to_array_type(bkhk__crppj)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        uuao__slxcl = bodo.utils.utils.alloc_type(n, mmv__atlnk, (-1,))
        for kkdz__hqi in numba.parfors.parfor.internal_prange(n):
            sersz__krr = codes[kkdz__hqi]
            if sersz__krr == -1:
                bodo.libs.array_kernels.setna(uuao__slxcl, kkdz__hqi)
                continue
            uuao__slxcl[kkdz__hqi] = bodo.utils.conversion.unbox_if_timestamp(
                categories[sersz__krr])
        return uuao__slxcl
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        gcj__szl, ktm__iov = args
        mjfi__fhsfm = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        mjfi__fhsfm.codes = gcj__szl
        mjfi__fhsfm.dtype = ktm__iov
        context.nrt.incref(builder, signature.args[0], gcj__szl)
        context.nrt.incref(builder, signature.args[1], ktm__iov)
        return mjfi__fhsfm._getvalue()
    uopcy__kfseb = CategoricalArrayType(cat_dtype)
    sig = uopcy__kfseb(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    nrkp__pczs = args[0]
    if equiv_set.has_shape(nrkp__pczs):
        return ArrayAnalysis.AnalyzeResult(shape=nrkp__pczs, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    wsd__roswc = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, wsd__roswc)
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
            lybii__qebro = {}
            oppr__hrmih = np.empty(n + 1, np.int64)
            ggl__bmc = {}
            iem__fzsne = []
            fbccj__siv = {}
            for kkdz__hqi in range(n):
                fbccj__siv[categories[kkdz__hqi]] = kkdz__hqi
            for yghx__vkkcq in to_replace:
                if yghx__vkkcq != value:
                    if yghx__vkkcq in fbccj__siv:
                        if value in fbccj__siv:
                            lybii__qebro[yghx__vkkcq] = yghx__vkkcq
                            lbt__idu = fbccj__siv[yghx__vkkcq]
                            ggl__bmc[lbt__idu] = fbccj__siv[value]
                            iem__fzsne.append(lbt__idu)
                        else:
                            lybii__qebro[yghx__vkkcq] = value
                            fbccj__siv[value] = fbccj__siv[yghx__vkkcq]
            ogvmd__rpy = np.sort(np.array(iem__fzsne))
            kxj__tbuvi = 0
            tzx__qcm = []
            for ledb__nkad in range(-1, n):
                while kxj__tbuvi < len(ogvmd__rpy) and ledb__nkad > ogvmd__rpy[
                    kxj__tbuvi]:
                    kxj__tbuvi += 1
                tzx__qcm.append(kxj__tbuvi)
            for god__zvn in range(-1, n):
                vlzgy__cqjnr = god__zvn
                if god__zvn in ggl__bmc:
                    vlzgy__cqjnr = ggl__bmc[god__zvn]
                oppr__hrmih[god__zvn + 1] = vlzgy__cqjnr - tzx__qcm[
                    vlzgy__cqjnr + 1]
            return lybii__qebro, oppr__hrmih, len(ogvmd__rpy)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for kkdz__hqi in range(len(new_codes_arr)):
        new_codes_arr[kkdz__hqi] = codes_map_arr[old_codes_arr[kkdz__hqi] + 1]


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
    iedzc__zhy = arr.dtype.ordered
    ofa__jhi = arr.dtype.elem_type
    asq__jcao = get_overload_const(to_replace)
    ldpek__jac = get_overload_const(value)
    if (arr.dtype.categories is not None and asq__jcao is not NOT_CONSTANT and
        ldpek__jac is not NOT_CONSTANT):
        roumo__curci, codes_map_arr, bfuxx__yoyn = python_build_replace_dicts(
            asq__jcao, ldpek__jac, arr.dtype.categories)
        if len(roumo__curci) == 0:
            return lambda arr, to_replace, value: arr.copy()
        swk__pguhq = []
        for mbsjs__izpq in arr.dtype.categories:
            if mbsjs__izpq in roumo__curci:
                jav__evkwb = roumo__curci[mbsjs__izpq]
                if jav__evkwb != mbsjs__izpq:
                    swk__pguhq.append(jav__evkwb)
            else:
                swk__pguhq.append(mbsjs__izpq)
        esz__tihr = pd.CategoricalDtype(swk__pguhq, iedzc__zhy
            ).categories.values
        vgzm__tseu = MetaType(tuple(esz__tihr))

        def impl_dtype(arr, to_replace, value):
            ker__fvj = init_cat_dtype(bodo.utils.conversion.
                index_from_array(esz__tihr), iedzc__zhy, None, vgzm__tseu)
            mjfi__fhsfm = alloc_categorical_array(len(arr.codes), ker__fvj)
            reassign_codes(mjfi__fhsfm.codes, arr.codes, codes_map_arr)
            return mjfi__fhsfm
        return impl_dtype
    ofa__jhi = arr.dtype.elem_type
    if ofa__jhi == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            lybii__qebro, codes_map_arr, zcjbq__ppvv = build_replace_dicts(
                to_replace, value, categories.values)
            if len(lybii__qebro) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), iedzc__zhy,
                    None, None))
            n = len(categories)
            esz__tihr = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                zcjbq__ppvv, -1)
            jrla__qod = 0
            for ledb__nkad in range(n):
                etf__hgwf = categories[ledb__nkad]
                if etf__hgwf in lybii__qebro:
                    teg__kpg = lybii__qebro[etf__hgwf]
                    if teg__kpg != etf__hgwf:
                        esz__tihr[jrla__qod] = teg__kpg
                        jrla__qod += 1
                else:
                    esz__tihr[jrla__qod] = etf__hgwf
                    jrla__qod += 1
            mjfi__fhsfm = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                esz__tihr), iedzc__zhy, None, None))
            reassign_codes(mjfi__fhsfm.codes, arr.codes, codes_map_arr)
            return mjfi__fhsfm
        return impl_str
    uixtt__dba = dtype_to_array_type(ofa__jhi)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        lybii__qebro, codes_map_arr, zcjbq__ppvv = build_replace_dicts(
            to_replace, value, categories.values)
        if len(lybii__qebro) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), iedzc__zhy, None, None))
        n = len(categories)
        esz__tihr = bodo.utils.utils.alloc_type(n - zcjbq__ppvv, uixtt__dba,
            None)
        jrla__qod = 0
        for kkdz__hqi in range(n):
            etf__hgwf = categories[kkdz__hqi]
            if etf__hgwf in lybii__qebro:
                teg__kpg = lybii__qebro[etf__hgwf]
                if teg__kpg != etf__hgwf:
                    esz__tihr[jrla__qod] = teg__kpg
                    jrla__qod += 1
            else:
                esz__tihr[jrla__qod] = etf__hgwf
                jrla__qod += 1
        mjfi__fhsfm = alloc_categorical_array(len(arr.codes),
            init_cat_dtype(bodo.utils.conversion.index_from_array(esz__tihr
            ), iedzc__zhy, None, None))
        reassign_codes(mjfi__fhsfm.codes, arr.codes, codes_map_arr)
        return mjfi__fhsfm
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
    inkz__ybz = dict()
    opi__lxp = 0
    for kkdz__hqi in range(len(vals)):
        val = vals[kkdz__hqi]
        if val in inkz__ybz:
            continue
        inkz__ybz[val] = opi__lxp
        opi__lxp += 1
    return inkz__ybz


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    inkz__ybz = dict()
    for kkdz__hqi in range(len(vals)):
        val = vals[kkdz__hqi]
        inkz__ybz[val] = kkdz__hqi
    return inkz__ybz


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    ebze__vvz = dict(fastpath=fastpath)
    dhwm__kpwg = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', ebze__vvz, dhwm__kpwg)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        wcv__cdgym = get_overload_const(categories)
        if wcv__cdgym is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                xlbpx__tbrkq = False
            else:
                xlbpx__tbrkq = get_overload_const_bool(ordered)
            djyn__lbac = pd.CategoricalDtype(wcv__cdgym, xlbpx__tbrkq
                ).categories.values
            dpwf__fpdni = MetaType(tuple(djyn__lbac))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                ker__fvj = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(djyn__lbac), xlbpx__tbrkq, None,
                    dpwf__fpdni)
                return bodo.utils.conversion.fix_arr_dtype(data, ker__fvj)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            mbiq__rsytb = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                mbiq__rsytb, ordered, None, None)
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
            alfup__paap = arr.codes[ind]
            return arr.dtype.categories[max(alfup__paap, 0)]
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
    for kkdz__hqi in range(len(arr1)):
        if arr1[kkdz__hqi] != arr2[kkdz__hqi]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    cjxyw__eytp = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    qvyt__rby = not isinstance(val, CategoricalArrayType) and is_iterable_type(
        val) and is_common_scalar_dtype([val.dtype, arr.dtype.elem_type]
        ) and not (isinstance(arr.dtype.elem_type, types.Integer) and
        isinstance(val.dtype, types.Float))
    hzhd__skz = categorical_arrs_match(arr, val)
    cop__souxk = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    qhfx__fcpa = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not cjxyw__eytp:
            raise BodoError(cop__souxk)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            alfup__paap = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = alfup__paap
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (cjxyw__eytp or qvyt__rby or hzhd__skz !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(cop__souxk)
        if hzhd__skz == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(qhfx__fcpa)
        if cjxyw__eytp:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                ttyn__vgpj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for ledb__nkad in range(n):
                    arr.codes[ind[ledb__nkad]] = ttyn__vgpj
            return impl_scalar
        if hzhd__skz == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for kkdz__hqi in range(n):
                    arr.codes[ind[kkdz__hqi]] = val.codes[kkdz__hqi]
            return impl_arr_ind_mask
        if hzhd__skz == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(qhfx__fcpa)
                n = len(val.codes)
                for kkdz__hqi in range(n):
                    arr.codes[ind[kkdz__hqi]] = val.codes[kkdz__hqi]
            return impl_arr_ind_mask
        if qvyt__rby:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for ledb__nkad in range(n):
                    qae__szz = bodo.utils.conversion.unbox_if_timestamp(val
                        [ledb__nkad])
                    if qae__szz not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    alfup__paap = categories.get_loc(qae__szz)
                    arr.codes[ind[ledb__nkad]] = alfup__paap
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (cjxyw__eytp or qvyt__rby or hzhd__skz !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(cop__souxk)
        if hzhd__skz == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(qhfx__fcpa)
        if cjxyw__eytp:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                ttyn__vgpj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for ledb__nkad in range(n):
                    if ind[ledb__nkad]:
                        arr.codes[ledb__nkad] = ttyn__vgpj
            return impl_scalar
        if hzhd__skz == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                sigj__wgmx = 0
                for kkdz__hqi in range(n):
                    if ind[kkdz__hqi]:
                        arr.codes[kkdz__hqi] = val.codes[sigj__wgmx]
                        sigj__wgmx += 1
            return impl_bool_ind_mask
        if hzhd__skz == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(qhfx__fcpa)
                n = len(ind)
                sigj__wgmx = 0
                for kkdz__hqi in range(n):
                    if ind[kkdz__hqi]:
                        arr.codes[kkdz__hqi] = val.codes[sigj__wgmx]
                        sigj__wgmx += 1
            return impl_bool_ind_mask
        if qvyt__rby:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                sigj__wgmx = 0
                categories = arr.dtype.categories
                for ledb__nkad in range(n):
                    if ind[ledb__nkad]:
                        qae__szz = bodo.utils.conversion.unbox_if_timestamp(val
                            [sigj__wgmx])
                        if qae__szz not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        alfup__paap = categories.get_loc(qae__szz)
                        arr.codes[ledb__nkad] = alfup__paap
                        sigj__wgmx += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (cjxyw__eytp or qvyt__rby or hzhd__skz !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(cop__souxk)
        if hzhd__skz == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(qhfx__fcpa)
        if cjxyw__eytp:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                ttyn__vgpj = arr.dtype.categories.get_loc(val)
                vfzmd__jeylq = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for ledb__nkad in range(vfzmd__jeylq.start, vfzmd__jeylq.
                    stop, vfzmd__jeylq.step):
                    arr.codes[ledb__nkad] = ttyn__vgpj
            return impl_scalar
        if hzhd__skz == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if hzhd__skz == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(qhfx__fcpa)
                arr.codes[ind] = val.codes
            return impl_arr
        if qvyt__rby:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                vfzmd__jeylq = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                sigj__wgmx = 0
                for ledb__nkad in range(vfzmd__jeylq.start, vfzmd__jeylq.
                    stop, vfzmd__jeylq.step):
                    qae__szz = bodo.utils.conversion.unbox_if_timestamp(val
                        [sigj__wgmx])
                    if qae__szz not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    alfup__paap = categories.get_loc(qae__szz)
                    arr.codes[ledb__nkad] = alfup__paap
                    sigj__wgmx += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
