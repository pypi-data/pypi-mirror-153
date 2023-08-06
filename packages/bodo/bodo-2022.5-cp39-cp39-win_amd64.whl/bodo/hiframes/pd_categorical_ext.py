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
        pnle__yjqu = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=pnle__yjqu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    xrj__wplyg = tuple(val.categories.values)
    elem_type = None if len(xrj__wplyg) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(xrj__wplyg, elem_type, val.ordered, bodo.
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
        rmma__lcq = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, rmma__lcq)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    wxb__zjg = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    jvxc__uxys = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, tqi__lkywg, tqi__lkywg = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    stmk__jtds = PDCategoricalDtype(jvxc__uxys, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, wxb__zjg)
    return stmk__jtds(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jbmy__qhhiy = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, jbmy__qhhiy).value
    c.pyapi.decref(jbmy__qhhiy)
    cmugh__ltwh = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, cmugh__ltwh).value
    c.pyapi.decref(cmugh__ltwh)
    gbvw__puadn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=gbvw__puadn)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    jbmy__qhhiy = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    blxl__hdr = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c
        .env_manager)
    eylh__kqarp = c.context.insert_const_string(c.builder.module, 'pandas')
    acjp__twv = c.pyapi.import_module_noblock(eylh__kqarp)
    xbl__ose = c.pyapi.call_method(acjp__twv, 'CategoricalDtype', (
        blxl__hdr, jbmy__qhhiy))
    c.pyapi.decref(jbmy__qhhiy)
    c.pyapi.decref(blxl__hdr)
    c.pyapi.decref(acjp__twv)
    c.context.nrt.decref(c.builder, typ, val)
    return xbl__ose


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
        dlmc__ydnh = get_categories_int_type(fe_type.dtype)
        rmma__lcq = [('dtype', fe_type.dtype), ('codes', types.Array(
            dlmc__ydnh, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, rmma__lcq)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    mgrj__txlj = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), mgrj__txlj
        ).value
    c.pyapi.decref(mgrj__txlj)
    xbl__ose = c.pyapi.object_getattr_string(val, 'dtype')
    csa__fwagq = c.pyapi.to_native_value(typ.dtype, xbl__ose).value
    c.pyapi.decref(xbl__ose)
    hgihn__kwdoq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hgihn__kwdoq.codes = codes
    hgihn__kwdoq.dtype = csa__fwagq
    return NativeValue(hgihn__kwdoq._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    zljws__kgaln = get_categories_int_type(typ.dtype)
    zuy__uaqg = context.get_constant_generic(builder, types.Array(
        zljws__kgaln, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, zuy__uaqg])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    lahwz__zjq = len(cat_dtype.categories)
    if lahwz__zjq < np.iinfo(np.int8).max:
        dtype = types.int8
    elif lahwz__zjq < np.iinfo(np.int16).max:
        dtype = types.int16
    elif lahwz__zjq < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    eylh__kqarp = c.context.insert_const_string(c.builder.module, 'pandas')
    acjp__twv = c.pyapi.import_module_noblock(eylh__kqarp)
    dlmc__ydnh = get_categories_int_type(dtype)
    gzt__zzbys = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    wbmgz__lmxtu = types.Array(dlmc__ydnh, 1, 'C')
    c.context.nrt.incref(c.builder, wbmgz__lmxtu, gzt__zzbys.codes)
    mgrj__txlj = c.pyapi.from_native_value(wbmgz__lmxtu, gzt__zzbys.codes,
        c.env_manager)
    c.context.nrt.incref(c.builder, dtype, gzt__zzbys.dtype)
    xbl__ose = c.pyapi.from_native_value(dtype, gzt__zzbys.dtype, c.env_manager
        )
    aaaa__mzir = c.pyapi.borrow_none()
    lsmqx__kiln = c.pyapi.object_getattr_string(acjp__twv, 'Categorical')
    iwm__ymky = c.pyapi.call_method(lsmqx__kiln, 'from_codes', (mgrj__txlj,
        aaaa__mzir, aaaa__mzir, xbl__ose))
    c.pyapi.decref(lsmqx__kiln)
    c.pyapi.decref(mgrj__txlj)
    c.pyapi.decref(xbl__ose)
    c.pyapi.decref(acjp__twv)
    c.context.nrt.decref(c.builder, typ, val)
    return iwm__ymky


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
            zjbwv__deaz = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                pvaeh__plhli = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), zjbwv__deaz)
                return pvaeh__plhli
            return impl_lit

        def impl(A, other):
            zjbwv__deaz = get_code_for_value(A.dtype, other)
            pvaeh__plhli = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), zjbwv__deaz)
            return pvaeh__plhli
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        ykmo__jtqp = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(ykmo__jtqp)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    gzt__zzbys = cat_dtype.categories
    n = len(gzt__zzbys)
    for czh__aofst in range(n):
        if gzt__zzbys[czh__aofst] == val:
            return czh__aofst
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    wpgnf__sdj = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if wpgnf__sdj != A.dtype.elem_type and wpgnf__sdj != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if wpgnf__sdj == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            pvaeh__plhli = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for czh__aofst in numba.parfors.parfor.internal_prange(n):
                tyndf__okc = codes[czh__aofst]
                if tyndf__okc == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            pvaeh__plhli, czh__aofst)
                    else:
                        bodo.libs.array_kernels.setna(pvaeh__plhli, czh__aofst)
                    continue
                pvaeh__plhli[czh__aofst] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[tyndf__okc]))
            return pvaeh__plhli
        return impl
    wbmgz__lmxtu = dtype_to_array_type(wpgnf__sdj)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        pvaeh__plhli = bodo.utils.utils.alloc_type(n, wbmgz__lmxtu, (-1,))
        for czh__aofst in numba.parfors.parfor.internal_prange(n):
            tyndf__okc = codes[czh__aofst]
            if tyndf__okc == -1:
                bodo.libs.array_kernels.setna(pvaeh__plhli, czh__aofst)
                continue
            pvaeh__plhli[czh__aofst
                ] = bodo.utils.conversion.unbox_if_timestamp(categories[
                tyndf__okc])
        return pvaeh__plhli
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        zneww__nmfut, csa__fwagq = args
        gzt__zzbys = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        gzt__zzbys.codes = zneww__nmfut
        gzt__zzbys.dtype = csa__fwagq
        context.nrt.incref(builder, signature.args[0], zneww__nmfut)
        context.nrt.incref(builder, signature.args[1], csa__fwagq)
        return gzt__zzbys._getvalue()
    kngfr__bruo = CategoricalArrayType(cat_dtype)
    sig = kngfr__bruo(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    vrn__mvz = args[0]
    if equiv_set.has_shape(vrn__mvz):
        return ArrayAnalysis.AnalyzeResult(shape=vrn__mvz, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    dlmc__ydnh = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, dlmc__ydnh)
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
            brkog__kcfti = {}
            zuy__uaqg = np.empty(n + 1, np.int64)
            njxi__pre = {}
            unog__jnj = []
            lhql__ncvc = {}
            for czh__aofst in range(n):
                lhql__ncvc[categories[czh__aofst]] = czh__aofst
            for hcv__qxa in to_replace:
                if hcv__qxa != value:
                    if hcv__qxa in lhql__ncvc:
                        if value in lhql__ncvc:
                            brkog__kcfti[hcv__qxa] = hcv__qxa
                            zdt__ifc = lhql__ncvc[hcv__qxa]
                            njxi__pre[zdt__ifc] = lhql__ncvc[value]
                            unog__jnj.append(zdt__ifc)
                        else:
                            brkog__kcfti[hcv__qxa] = value
                            lhql__ncvc[value] = lhql__ncvc[hcv__qxa]
            huuwf__sdam = np.sort(np.array(unog__jnj))
            lblrh__jex = 0
            cpgi__xgejw = []
            for qih__jiei in range(-1, n):
                while lblrh__jex < len(huuwf__sdam
                    ) and qih__jiei > huuwf__sdam[lblrh__jex]:
                    lblrh__jex += 1
                cpgi__xgejw.append(lblrh__jex)
            for zqere__hrtqn in range(-1, n):
                ujh__dam = zqere__hrtqn
                if zqere__hrtqn in njxi__pre:
                    ujh__dam = njxi__pre[zqere__hrtqn]
                zuy__uaqg[zqere__hrtqn + 1] = ujh__dam - cpgi__xgejw[
                    ujh__dam + 1]
            return brkog__kcfti, zuy__uaqg, len(huuwf__sdam)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for czh__aofst in range(len(new_codes_arr)):
        new_codes_arr[czh__aofst] = codes_map_arr[old_codes_arr[czh__aofst] + 1
            ]


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
    acpgo__czh = arr.dtype.ordered
    pethz__aerc = arr.dtype.elem_type
    vlhu__cjynz = get_overload_const(to_replace)
    swkqa__rri = get_overload_const(value)
    if (arr.dtype.categories is not None and vlhu__cjynz is not
        NOT_CONSTANT and swkqa__rri is not NOT_CONSTANT):
        uici__upfur, codes_map_arr, tqi__lkywg = python_build_replace_dicts(
            vlhu__cjynz, swkqa__rri, arr.dtype.categories)
        if len(uici__upfur) == 0:
            return lambda arr, to_replace, value: arr.copy()
        hxzdf__zuzzt = []
        for cjnmp__yypix in arr.dtype.categories:
            if cjnmp__yypix in uici__upfur:
                lwbzc__dkdmg = uici__upfur[cjnmp__yypix]
                if lwbzc__dkdmg != cjnmp__yypix:
                    hxzdf__zuzzt.append(lwbzc__dkdmg)
            else:
                hxzdf__zuzzt.append(cjnmp__yypix)
        rxsy__unvo = pd.CategoricalDtype(hxzdf__zuzzt, acpgo__czh
            ).categories.values
        akey__dulnc = MetaType(tuple(rxsy__unvo))

        def impl_dtype(arr, to_replace, value):
            euthb__eaal = init_cat_dtype(bodo.utils.conversion.
                index_from_array(rxsy__unvo), acpgo__czh, None, akey__dulnc)
            gzt__zzbys = alloc_categorical_array(len(arr.codes), euthb__eaal)
            reassign_codes(gzt__zzbys.codes, arr.codes, codes_map_arr)
            return gzt__zzbys
        return impl_dtype
    pethz__aerc = arr.dtype.elem_type
    if pethz__aerc == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            brkog__kcfti, codes_map_arr, cof__ujh = build_replace_dicts(
                to_replace, value, categories.values)
            if len(brkog__kcfti) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), acpgo__czh,
                    None, None))
            n = len(categories)
            rxsy__unvo = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                cof__ujh, -1)
            mkws__vwh = 0
            for qih__jiei in range(n):
                pqeuf__cdbpp = categories[qih__jiei]
                if pqeuf__cdbpp in brkog__kcfti:
                    cefr__dpc = brkog__kcfti[pqeuf__cdbpp]
                    if cefr__dpc != pqeuf__cdbpp:
                        rxsy__unvo[mkws__vwh] = cefr__dpc
                        mkws__vwh += 1
                else:
                    rxsy__unvo[mkws__vwh] = pqeuf__cdbpp
                    mkws__vwh += 1
            gzt__zzbys = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                rxsy__unvo), acpgo__czh, None, None))
            reassign_codes(gzt__zzbys.codes, arr.codes, codes_map_arr)
            return gzt__zzbys
        return impl_str
    wei__hfqxb = dtype_to_array_type(pethz__aerc)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        brkog__kcfti, codes_map_arr, cof__ujh = build_replace_dicts(to_replace,
            value, categories.values)
        if len(brkog__kcfti) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), acpgo__czh, None, None))
        n = len(categories)
        rxsy__unvo = bodo.utils.utils.alloc_type(n - cof__ujh, wei__hfqxb, None
            )
        mkws__vwh = 0
        for czh__aofst in range(n):
            pqeuf__cdbpp = categories[czh__aofst]
            if pqeuf__cdbpp in brkog__kcfti:
                cefr__dpc = brkog__kcfti[pqeuf__cdbpp]
                if cefr__dpc != pqeuf__cdbpp:
                    rxsy__unvo[mkws__vwh] = cefr__dpc
                    mkws__vwh += 1
            else:
                rxsy__unvo[mkws__vwh] = pqeuf__cdbpp
                mkws__vwh += 1
        gzt__zzbys = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(rxsy__unvo), acpgo__czh,
            None, None))
        reassign_codes(gzt__zzbys.codes, arr.codes, codes_map_arr)
        return gzt__zzbys
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
    cdime__szxh = dict()
    hamet__qvi = 0
    for czh__aofst in range(len(vals)):
        val = vals[czh__aofst]
        if val in cdime__szxh:
            continue
        cdime__szxh[val] = hamet__qvi
        hamet__qvi += 1
    return cdime__szxh


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    cdime__szxh = dict()
    for czh__aofst in range(len(vals)):
        val = vals[czh__aofst]
        cdime__szxh[val] = czh__aofst
    return cdime__szxh


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    iut__gbll = dict(fastpath=fastpath)
    iyes__qctew = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', iut__gbll, iyes__qctew)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        cdou__teimo = get_overload_const(categories)
        if cdou__teimo is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                vpox__enhjf = False
            else:
                vpox__enhjf = get_overload_const_bool(ordered)
            suqr__skgww = pd.CategoricalDtype(cdou__teimo, vpox__enhjf
                ).categories.values
            zvxa__zva = MetaType(tuple(suqr__skgww))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                euthb__eaal = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(suqr__skgww), vpox__enhjf, None, zvxa__zva
                    )
                return bodo.utils.conversion.fix_arr_dtype(data, euthb__eaal)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            xrj__wplyg = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                xrj__wplyg, ordered, None, None)
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
            nnb__lud = arr.codes[ind]
            return arr.dtype.categories[max(nnb__lud, 0)]
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
    for czh__aofst in range(len(arr1)):
        if arr1[czh__aofst] != arr2[czh__aofst]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    mmyoi__wxa = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    jgjsg__zie = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    ffey__zxkxo = categorical_arrs_match(arr, val)
    ppex__dujst = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    fcm__vfs = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not mmyoi__wxa:
            raise BodoError(ppex__dujst)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            nnb__lud = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = nnb__lud
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (mmyoi__wxa or jgjsg__zie or ffey__zxkxo !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ppex__dujst)
        if ffey__zxkxo == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(fcm__vfs)
        if mmyoi__wxa:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                gwpkf__whrk = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for qih__jiei in range(n):
                    arr.codes[ind[qih__jiei]] = gwpkf__whrk
            return impl_scalar
        if ffey__zxkxo == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for czh__aofst in range(n):
                    arr.codes[ind[czh__aofst]] = val.codes[czh__aofst]
            return impl_arr_ind_mask
        if ffey__zxkxo == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(fcm__vfs)
                n = len(val.codes)
                for czh__aofst in range(n):
                    arr.codes[ind[czh__aofst]] = val.codes[czh__aofst]
            return impl_arr_ind_mask
        if jgjsg__zie:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for qih__jiei in range(n):
                    jqs__mksmk = bodo.utils.conversion.unbox_if_timestamp(val
                        [qih__jiei])
                    if jqs__mksmk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    nnb__lud = categories.get_loc(jqs__mksmk)
                    arr.codes[ind[qih__jiei]] = nnb__lud
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (mmyoi__wxa or jgjsg__zie or ffey__zxkxo !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ppex__dujst)
        if ffey__zxkxo == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(fcm__vfs)
        if mmyoi__wxa:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                gwpkf__whrk = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for qih__jiei in range(n):
                    if ind[qih__jiei]:
                        arr.codes[qih__jiei] = gwpkf__whrk
            return impl_scalar
        if ffey__zxkxo == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                ddkgi__bufub = 0
                for czh__aofst in range(n):
                    if ind[czh__aofst]:
                        arr.codes[czh__aofst] = val.codes[ddkgi__bufub]
                        ddkgi__bufub += 1
            return impl_bool_ind_mask
        if ffey__zxkxo == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(fcm__vfs)
                n = len(ind)
                ddkgi__bufub = 0
                for czh__aofst in range(n):
                    if ind[czh__aofst]:
                        arr.codes[czh__aofst] = val.codes[ddkgi__bufub]
                        ddkgi__bufub += 1
            return impl_bool_ind_mask
        if jgjsg__zie:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                ddkgi__bufub = 0
                categories = arr.dtype.categories
                for qih__jiei in range(n):
                    if ind[qih__jiei]:
                        jqs__mksmk = bodo.utils.conversion.unbox_if_timestamp(
                            val[ddkgi__bufub])
                        if jqs__mksmk not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        nnb__lud = categories.get_loc(jqs__mksmk)
                        arr.codes[qih__jiei] = nnb__lud
                        ddkgi__bufub += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (mmyoi__wxa or jgjsg__zie or ffey__zxkxo !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ppex__dujst)
        if ffey__zxkxo == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(fcm__vfs)
        if mmyoi__wxa:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                gwpkf__whrk = arr.dtype.categories.get_loc(val)
                wght__pduil = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for qih__jiei in range(wght__pduil.start, wght__pduil.stop,
                    wght__pduil.step):
                    arr.codes[qih__jiei] = gwpkf__whrk
            return impl_scalar
        if ffey__zxkxo == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if ffey__zxkxo == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(fcm__vfs)
                arr.codes[ind] = val.codes
            return impl_arr
        if jgjsg__zie:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                wght__pduil = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                ddkgi__bufub = 0
                for qih__jiei in range(wght__pduil.start, wght__pduil.stop,
                    wght__pduil.step):
                    jqs__mksmk = bodo.utils.conversion.unbox_if_timestamp(val
                        [ddkgi__bufub])
                    if jqs__mksmk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    nnb__lud = categories.get_loc(jqs__mksmk)
                    arr.codes[qih__jiei] = nnb__lud
                    ddkgi__bufub += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
