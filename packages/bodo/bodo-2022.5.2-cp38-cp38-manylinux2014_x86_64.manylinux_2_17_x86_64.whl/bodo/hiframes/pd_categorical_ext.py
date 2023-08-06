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
        xtwrs__ykzk = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=xtwrs__ykzk)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    twtlh__loli = tuple(val.categories.values)
    elem_type = None if len(twtlh__loli) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(twtlh__loli, elem_type, val.ordered, bodo.
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
        mscc__klp = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, mscc__klp)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    mms__uqe = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    nkkw__ofht = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, imsic__bmrkx, imsic__bmrkx = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    nmvhm__ghhdp = PDCategoricalDtype(nkkw__ofht, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, mms__uqe)
    return nmvhm__ghhdp(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    maq__mih = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, maq__mih).value
    c.pyapi.decref(maq__mih)
    joe__zpbr = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, joe__zpbr).value
    c.pyapi.decref(joe__zpbr)
    vid__gtbzd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=vid__gtbzd)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    maq__mih = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    xzdq__tqy = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c
        .env_manager)
    dnoz__buwj = c.context.insert_const_string(c.builder.module, 'pandas')
    mni__bjs = c.pyapi.import_module_noblock(dnoz__buwj)
    knje__tle = c.pyapi.call_method(mni__bjs, 'CategoricalDtype', (
        xzdq__tqy, maq__mih))
    c.pyapi.decref(maq__mih)
    c.pyapi.decref(xzdq__tqy)
    c.pyapi.decref(mni__bjs)
    c.context.nrt.decref(c.builder, typ, val)
    return knje__tle


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
        rxqr__bvr = get_categories_int_type(fe_type.dtype)
        mscc__klp = [('dtype', fe_type.dtype), ('codes', types.Array(
            rxqr__bvr, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, mscc__klp)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    boa__xnho = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), boa__xnho
        ).value
    c.pyapi.decref(boa__xnho)
    knje__tle = c.pyapi.object_getattr_string(val, 'dtype')
    ktmxs__gbv = c.pyapi.to_native_value(typ.dtype, knje__tle).value
    c.pyapi.decref(knje__tle)
    ufoc__qvbk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ufoc__qvbk.codes = codes
    ufoc__qvbk.dtype = ktmxs__gbv
    return NativeValue(ufoc__qvbk._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    dzne__rymtd = get_categories_int_type(typ.dtype)
    obmk__lafjf = context.get_constant_generic(builder, types.Array(
        dzne__rymtd, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, obmk__lafjf])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    fcbwt__uwfu = len(cat_dtype.categories)
    if fcbwt__uwfu < np.iinfo(np.int8).max:
        dtype = types.int8
    elif fcbwt__uwfu < np.iinfo(np.int16).max:
        dtype = types.int16
    elif fcbwt__uwfu < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    dnoz__buwj = c.context.insert_const_string(c.builder.module, 'pandas')
    mni__bjs = c.pyapi.import_module_noblock(dnoz__buwj)
    rxqr__bvr = get_categories_int_type(dtype)
    zfbi__uti = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    frgai__cxeza = types.Array(rxqr__bvr, 1, 'C')
    c.context.nrt.incref(c.builder, frgai__cxeza, zfbi__uti.codes)
    boa__xnho = c.pyapi.from_native_value(frgai__cxeza, zfbi__uti.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, zfbi__uti.dtype)
    knje__tle = c.pyapi.from_native_value(dtype, zfbi__uti.dtype, c.env_manager
        )
    nzvds__hgt = c.pyapi.borrow_none()
    irb__lel = c.pyapi.object_getattr_string(mni__bjs, 'Categorical')
    nkfe__vyj = c.pyapi.call_method(irb__lel, 'from_codes', (boa__xnho,
        nzvds__hgt, nzvds__hgt, knje__tle))
    c.pyapi.decref(irb__lel)
    c.pyapi.decref(boa__xnho)
    c.pyapi.decref(knje__tle)
    c.pyapi.decref(mni__bjs)
    c.context.nrt.decref(c.builder, typ, val)
    return nkfe__vyj


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
            vavyi__zufw = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                qevf__jhqnu = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), vavyi__zufw)
                return qevf__jhqnu
            return impl_lit

        def impl(A, other):
            vavyi__zufw = get_code_for_value(A.dtype, other)
            qevf__jhqnu = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), vavyi__zufw)
            return qevf__jhqnu
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        ocnk__kfenu = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(ocnk__kfenu)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    zfbi__uti = cat_dtype.categories
    n = len(zfbi__uti)
    for pqsy__czpym in range(n):
        if zfbi__uti[pqsy__czpym] == val:
            return pqsy__czpym
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    ksja__oinj = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if ksja__oinj != A.dtype.elem_type and ksja__oinj != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if ksja__oinj == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            qevf__jhqnu = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for pqsy__czpym in numba.parfors.parfor.internal_prange(n):
                jmao__ltgv = codes[pqsy__czpym]
                if jmao__ltgv == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            qevf__jhqnu, pqsy__czpym)
                    else:
                        bodo.libs.array_kernels.setna(qevf__jhqnu, pqsy__czpym)
                    continue
                qevf__jhqnu[pqsy__czpym] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[jmao__ltgv]))
            return qevf__jhqnu
        return impl
    frgai__cxeza = dtype_to_array_type(ksja__oinj)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        qevf__jhqnu = bodo.utils.utils.alloc_type(n, frgai__cxeza, (-1,))
        for pqsy__czpym in numba.parfors.parfor.internal_prange(n):
            jmao__ltgv = codes[pqsy__czpym]
            if jmao__ltgv == -1:
                bodo.libs.array_kernels.setna(qevf__jhqnu, pqsy__czpym)
                continue
            qevf__jhqnu[pqsy__czpym
                ] = bodo.utils.conversion.unbox_if_timestamp(categories[
                jmao__ltgv])
        return qevf__jhqnu
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        xldho__kqflb, ktmxs__gbv = args
        zfbi__uti = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        zfbi__uti.codes = xldho__kqflb
        zfbi__uti.dtype = ktmxs__gbv
        context.nrt.incref(builder, signature.args[0], xldho__kqflb)
        context.nrt.incref(builder, signature.args[1], ktmxs__gbv)
        return zfbi__uti._getvalue()
    mxvwu__eji = CategoricalArrayType(cat_dtype)
    sig = mxvwu__eji(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    eqfp__fhr = args[0]
    if equiv_set.has_shape(eqfp__fhr):
        return ArrayAnalysis.AnalyzeResult(shape=eqfp__fhr, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    rxqr__bvr = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, rxqr__bvr)
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
            oukn__kxtio = {}
            obmk__lafjf = np.empty(n + 1, np.int64)
            kja__apz = {}
            zau__rgj = []
            xdwmj__qzl = {}
            for pqsy__czpym in range(n):
                xdwmj__qzl[categories[pqsy__czpym]] = pqsy__czpym
            for dolv__cwq in to_replace:
                if dolv__cwq != value:
                    if dolv__cwq in xdwmj__qzl:
                        if value in xdwmj__qzl:
                            oukn__kxtio[dolv__cwq] = dolv__cwq
                            vghmk__eaey = xdwmj__qzl[dolv__cwq]
                            kja__apz[vghmk__eaey] = xdwmj__qzl[value]
                            zau__rgj.append(vghmk__eaey)
                        else:
                            oukn__kxtio[dolv__cwq] = value
                            xdwmj__qzl[value] = xdwmj__qzl[dolv__cwq]
            qbk__ysay = np.sort(np.array(zau__rgj))
            yww__ans = 0
            wqyv__acd = []
            for yjco__yntu in range(-1, n):
                while yww__ans < len(qbk__ysay) and yjco__yntu > qbk__ysay[
                    yww__ans]:
                    yww__ans += 1
                wqyv__acd.append(yww__ans)
            for giuny__rgh in range(-1, n):
                ownq__womam = giuny__rgh
                if giuny__rgh in kja__apz:
                    ownq__womam = kja__apz[giuny__rgh]
                obmk__lafjf[giuny__rgh + 1] = ownq__womam - wqyv__acd[
                    ownq__womam + 1]
            return oukn__kxtio, obmk__lafjf, len(qbk__ysay)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for pqsy__czpym in range(len(new_codes_arr)):
        new_codes_arr[pqsy__czpym] = codes_map_arr[old_codes_arr[
            pqsy__czpym] + 1]


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
    npmq__ohx = arr.dtype.ordered
    zpzte__lbf = arr.dtype.elem_type
    aozc__livl = get_overload_const(to_replace)
    dfgs__ndto = get_overload_const(value)
    if (arr.dtype.categories is not None and aozc__livl is not NOT_CONSTANT and
        dfgs__ndto is not NOT_CONSTANT):
        hid__kla, codes_map_arr, imsic__bmrkx = python_build_replace_dicts(
            aozc__livl, dfgs__ndto, arr.dtype.categories)
        if len(hid__kla) == 0:
            return lambda arr, to_replace, value: arr.copy()
        aynl__jut = []
        for gnizt__sdhm in arr.dtype.categories:
            if gnizt__sdhm in hid__kla:
                avgk__icpp = hid__kla[gnizt__sdhm]
                if avgk__icpp != gnizt__sdhm:
                    aynl__jut.append(avgk__icpp)
            else:
                aynl__jut.append(gnizt__sdhm)
        cbgwd__ozy = pd.CategoricalDtype(aynl__jut, npmq__ohx
            ).categories.values
        fyjs__gavnq = MetaType(tuple(cbgwd__ozy))

        def impl_dtype(arr, to_replace, value):
            jxpub__mrvpn = init_cat_dtype(bodo.utils.conversion.
                index_from_array(cbgwd__ozy), npmq__ohx, None, fyjs__gavnq)
            zfbi__uti = alloc_categorical_array(len(arr.codes), jxpub__mrvpn)
            reassign_codes(zfbi__uti.codes, arr.codes, codes_map_arr)
            return zfbi__uti
        return impl_dtype
    zpzte__lbf = arr.dtype.elem_type
    if zpzte__lbf == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            oukn__kxtio, codes_map_arr, tzy__oos = build_replace_dicts(
                to_replace, value, categories.values)
            if len(oukn__kxtio) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), npmq__ohx,
                    None, None))
            n = len(categories)
            cbgwd__ozy = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                tzy__oos, -1)
            dnno__cqju = 0
            for yjco__yntu in range(n):
                kxp__bkm = categories[yjco__yntu]
                if kxp__bkm in oukn__kxtio:
                    mpv__ajen = oukn__kxtio[kxp__bkm]
                    if mpv__ajen != kxp__bkm:
                        cbgwd__ozy[dnno__cqju] = mpv__ajen
                        dnno__cqju += 1
                else:
                    cbgwd__ozy[dnno__cqju] = kxp__bkm
                    dnno__cqju += 1
            zfbi__uti = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                cbgwd__ozy), npmq__ohx, None, None))
            reassign_codes(zfbi__uti.codes, arr.codes, codes_map_arr)
            return zfbi__uti
        return impl_str
    lflu__yoeug = dtype_to_array_type(zpzte__lbf)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        oukn__kxtio, codes_map_arr, tzy__oos = build_replace_dicts(to_replace,
            value, categories.values)
        if len(oukn__kxtio) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), npmq__ohx, None, None))
        n = len(categories)
        cbgwd__ozy = bodo.utils.utils.alloc_type(n - tzy__oos, lflu__yoeug,
            None)
        dnno__cqju = 0
        for pqsy__czpym in range(n):
            kxp__bkm = categories[pqsy__czpym]
            if kxp__bkm in oukn__kxtio:
                mpv__ajen = oukn__kxtio[kxp__bkm]
                if mpv__ajen != kxp__bkm:
                    cbgwd__ozy[dnno__cqju] = mpv__ajen
                    dnno__cqju += 1
            else:
                cbgwd__ozy[dnno__cqju] = kxp__bkm
                dnno__cqju += 1
        zfbi__uti = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(cbgwd__ozy), npmq__ohx,
            None, None))
        reassign_codes(zfbi__uti.codes, arr.codes, codes_map_arr)
        return zfbi__uti
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
    tfiza__ewsw = dict()
    ylt__plfq = 0
    for pqsy__czpym in range(len(vals)):
        val = vals[pqsy__czpym]
        if val in tfiza__ewsw:
            continue
        tfiza__ewsw[val] = ylt__plfq
        ylt__plfq += 1
    return tfiza__ewsw


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    tfiza__ewsw = dict()
    for pqsy__czpym in range(len(vals)):
        val = vals[pqsy__czpym]
        tfiza__ewsw[val] = pqsy__czpym
    return tfiza__ewsw


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    fcn__vpe = dict(fastpath=fastpath)
    iazl__pbrj = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', fcn__vpe, iazl__pbrj)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        ins__gic = get_overload_const(categories)
        if ins__gic is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                ywjy__voy = False
            else:
                ywjy__voy = get_overload_const_bool(ordered)
            mii__vuxv = pd.CategoricalDtype(ins__gic, ywjy__voy
                ).categories.values
            yjiah__ffj = MetaType(tuple(mii__vuxv))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                jxpub__mrvpn = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(mii__vuxv), ywjy__voy, None, yjiah__ffj)
                return bodo.utils.conversion.fix_arr_dtype(data, jxpub__mrvpn)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            twtlh__loli = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                twtlh__loli, ordered, None, None)
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
            qtv__xtk = arr.codes[ind]
            return arr.dtype.categories[max(qtv__xtk, 0)]
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
    for pqsy__czpym in range(len(arr1)):
        if arr1[pqsy__czpym] != arr2[pqsy__czpym]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    ufn__kqom = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    ahuw__kmb = not isinstance(val, CategoricalArrayType) and is_iterable_type(
        val) and is_common_scalar_dtype([val.dtype, arr.dtype.elem_type]
        ) and not (isinstance(arr.dtype.elem_type, types.Integer) and
        isinstance(val.dtype, types.Float))
    tfs__nzok = categorical_arrs_match(arr, val)
    skidc__qlyl = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    geq__dwb = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not ufn__kqom:
            raise BodoError(skidc__qlyl)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            qtv__xtk = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = qtv__xtk
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (ufn__kqom or ahuw__kmb or tfs__nzok !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(skidc__qlyl)
        if tfs__nzok == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(geq__dwb)
        if ufn__kqom:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dek__jsh = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for yjco__yntu in range(n):
                    arr.codes[ind[yjco__yntu]] = dek__jsh
            return impl_scalar
        if tfs__nzok == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for pqsy__czpym in range(n):
                    arr.codes[ind[pqsy__czpym]] = val.codes[pqsy__czpym]
            return impl_arr_ind_mask
        if tfs__nzok == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(geq__dwb)
                n = len(val.codes)
                for pqsy__czpym in range(n):
                    arr.codes[ind[pqsy__czpym]] = val.codes[pqsy__czpym]
            return impl_arr_ind_mask
        if ahuw__kmb:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for yjco__yntu in range(n):
                    leipq__cdhrl = bodo.utils.conversion.unbox_if_timestamp(val
                        [yjco__yntu])
                    if leipq__cdhrl not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    qtv__xtk = categories.get_loc(leipq__cdhrl)
                    arr.codes[ind[yjco__yntu]] = qtv__xtk
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (ufn__kqom or ahuw__kmb or tfs__nzok !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(skidc__qlyl)
        if tfs__nzok == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(geq__dwb)
        if ufn__kqom:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dek__jsh = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for yjco__yntu in range(n):
                    if ind[yjco__yntu]:
                        arr.codes[yjco__yntu] = dek__jsh
            return impl_scalar
        if tfs__nzok == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                evv__idon = 0
                for pqsy__czpym in range(n):
                    if ind[pqsy__czpym]:
                        arr.codes[pqsy__czpym] = val.codes[evv__idon]
                        evv__idon += 1
            return impl_bool_ind_mask
        if tfs__nzok == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(geq__dwb)
                n = len(ind)
                evv__idon = 0
                for pqsy__czpym in range(n):
                    if ind[pqsy__czpym]:
                        arr.codes[pqsy__czpym] = val.codes[evv__idon]
                        evv__idon += 1
            return impl_bool_ind_mask
        if ahuw__kmb:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                evv__idon = 0
                categories = arr.dtype.categories
                for yjco__yntu in range(n):
                    if ind[yjco__yntu]:
                        leipq__cdhrl = (bodo.utils.conversion.
                            unbox_if_timestamp(val[evv__idon]))
                        if leipq__cdhrl not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        qtv__xtk = categories.get_loc(leipq__cdhrl)
                        arr.codes[yjco__yntu] = qtv__xtk
                        evv__idon += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (ufn__kqom or ahuw__kmb or tfs__nzok !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(skidc__qlyl)
        if tfs__nzok == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(geq__dwb)
        if ufn__kqom:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dek__jsh = arr.dtype.categories.get_loc(val)
                webef__ohgoe = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for yjco__yntu in range(webef__ohgoe.start, webef__ohgoe.
                    stop, webef__ohgoe.step):
                    arr.codes[yjco__yntu] = dek__jsh
            return impl_scalar
        if tfs__nzok == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if tfs__nzok == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(geq__dwb)
                arr.codes[ind] = val.codes
            return impl_arr
        if ahuw__kmb:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                webef__ohgoe = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                evv__idon = 0
                for yjco__yntu in range(webef__ohgoe.start, webef__ohgoe.
                    stop, webef__ohgoe.step):
                    leipq__cdhrl = bodo.utils.conversion.unbox_if_timestamp(val
                        [evv__idon])
                    if leipq__cdhrl not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    qtv__xtk = categories.get_loc(leipq__cdhrl)
                    arr.codes[yjco__yntu] = qtv__xtk
                    evv__idon += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
