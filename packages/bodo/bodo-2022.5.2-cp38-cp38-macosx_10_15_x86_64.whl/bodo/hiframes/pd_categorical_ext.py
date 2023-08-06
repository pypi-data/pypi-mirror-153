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
        pjyd__tlh = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=pjyd__tlh)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    oet__ytp = tuple(val.categories.values)
    elem_type = None if len(oet__ytp) == 0 else bodo.typeof(val.categories.
        values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(oet__ytp, elem_type, val.ordered, bodo.typeof
        (val.categories), int_type)


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
        tsadn__dlfbo = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, tsadn__dlfbo)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    obgry__buxw = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    jsr__wmol = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, hbaf__xbaks, hbaf__xbaks = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    xcez__xiaeg = PDCategoricalDtype(jsr__wmol, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, obgry__buxw)
    return xcez__xiaeg(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nsfz__zaoee = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, nsfz__zaoee).value
    c.pyapi.decref(nsfz__zaoee)
    zaogc__kqz = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, zaogc__kqz).value
    c.pyapi.decref(zaogc__kqz)
    htyg__qow = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=htyg__qow)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    nsfz__zaoee = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    imag__cbvm = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    ouz__kzzkh = c.context.insert_const_string(c.builder.module, 'pandas')
    wnav__uam = c.pyapi.import_module_noblock(ouz__kzzkh)
    qyrf__cmrrs = c.pyapi.call_method(wnav__uam, 'CategoricalDtype', (
        imag__cbvm, nsfz__zaoee))
    c.pyapi.decref(nsfz__zaoee)
    c.pyapi.decref(imag__cbvm)
    c.pyapi.decref(wnav__uam)
    c.context.nrt.decref(c.builder, typ, val)
    return qyrf__cmrrs


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
        beo__efxqf = get_categories_int_type(fe_type.dtype)
        tsadn__dlfbo = [('dtype', fe_type.dtype), ('codes', types.Array(
            beo__efxqf, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, tsadn__dlfbo)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    alqrp__lnob = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), alqrp__lnob
        ).value
    c.pyapi.decref(alqrp__lnob)
    qyrf__cmrrs = c.pyapi.object_getattr_string(val, 'dtype')
    gath__spkd = c.pyapi.to_native_value(typ.dtype, qyrf__cmrrs).value
    c.pyapi.decref(qyrf__cmrrs)
    fod__sfqq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fod__sfqq.codes = codes
    fod__sfqq.dtype = gath__spkd
    return NativeValue(fod__sfqq._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    dtzm__uagj = get_categories_int_type(typ.dtype)
    tiuf__llwvz = context.get_constant_generic(builder, types.Array(
        dtzm__uagj, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, tiuf__llwvz])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    uecb__svzjy = len(cat_dtype.categories)
    if uecb__svzjy < np.iinfo(np.int8).max:
        dtype = types.int8
    elif uecb__svzjy < np.iinfo(np.int16).max:
        dtype = types.int16
    elif uecb__svzjy < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    ouz__kzzkh = c.context.insert_const_string(c.builder.module, 'pandas')
    wnav__uam = c.pyapi.import_module_noblock(ouz__kzzkh)
    beo__efxqf = get_categories_int_type(dtype)
    gzs__hujv = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ipp__ccek = types.Array(beo__efxqf, 1, 'C')
    c.context.nrt.incref(c.builder, ipp__ccek, gzs__hujv.codes)
    alqrp__lnob = c.pyapi.from_native_value(ipp__ccek, gzs__hujv.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, gzs__hujv.dtype)
    qyrf__cmrrs = c.pyapi.from_native_value(dtype, gzs__hujv.dtype, c.
        env_manager)
    sidb__dutwl = c.pyapi.borrow_none()
    rtdom__ayk = c.pyapi.object_getattr_string(wnav__uam, 'Categorical')
    wely__kmm = c.pyapi.call_method(rtdom__ayk, 'from_codes', (alqrp__lnob,
        sidb__dutwl, sidb__dutwl, qyrf__cmrrs))
    c.pyapi.decref(rtdom__ayk)
    c.pyapi.decref(alqrp__lnob)
    c.pyapi.decref(qyrf__cmrrs)
    c.pyapi.decref(wnav__uam)
    c.context.nrt.decref(c.builder, typ, val)
    return wely__kmm


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
            lgww__ore = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                eco__hpofh = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), lgww__ore)
                return eco__hpofh
            return impl_lit

        def impl(A, other):
            lgww__ore = get_code_for_value(A.dtype, other)
            eco__hpofh = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), lgww__ore)
            return eco__hpofh
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        gdr__bdi = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(gdr__bdi)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    gzs__hujv = cat_dtype.categories
    n = len(gzs__hujv)
    for zcov__tvgew in range(n):
        if gzs__hujv[zcov__tvgew] == val:
            return zcov__tvgew
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    cljkn__swx = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if cljkn__swx != A.dtype.elem_type and cljkn__swx != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if cljkn__swx == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            eco__hpofh = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for zcov__tvgew in numba.parfors.parfor.internal_prange(n):
                hxw__luc = codes[zcov__tvgew]
                if hxw__luc == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(eco__hpofh
                            , zcov__tvgew)
                    else:
                        bodo.libs.array_kernels.setna(eco__hpofh, zcov__tvgew)
                    continue
                eco__hpofh[zcov__tvgew] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[hxw__luc]))
            return eco__hpofh
        return impl
    ipp__ccek = dtype_to_array_type(cljkn__swx)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        eco__hpofh = bodo.utils.utils.alloc_type(n, ipp__ccek, (-1,))
        for zcov__tvgew in numba.parfors.parfor.internal_prange(n):
            hxw__luc = codes[zcov__tvgew]
            if hxw__luc == -1:
                bodo.libs.array_kernels.setna(eco__hpofh, zcov__tvgew)
                continue
            eco__hpofh[zcov__tvgew] = bodo.utils.conversion.unbox_if_timestamp(
                categories[hxw__luc])
        return eco__hpofh
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        owy__yor, gath__spkd = args
        gzs__hujv = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        gzs__hujv.codes = owy__yor
        gzs__hujv.dtype = gath__spkd
        context.nrt.incref(builder, signature.args[0], owy__yor)
        context.nrt.incref(builder, signature.args[1], gath__spkd)
        return gzs__hujv._getvalue()
    lzarj__ccmfv = CategoricalArrayType(cat_dtype)
    sig = lzarj__ccmfv(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ksc__dscfp = args[0]
    if equiv_set.has_shape(ksc__dscfp):
        return ArrayAnalysis.AnalyzeResult(shape=ksc__dscfp, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    beo__efxqf = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, beo__efxqf)
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
            zbgvq__anb = {}
            tiuf__llwvz = np.empty(n + 1, np.int64)
            cvp__dgx = {}
            jku__tarel = []
            hxymo__tacid = {}
            for zcov__tvgew in range(n):
                hxymo__tacid[categories[zcov__tvgew]] = zcov__tvgew
            for aajr__fkd in to_replace:
                if aajr__fkd != value:
                    if aajr__fkd in hxymo__tacid:
                        if value in hxymo__tacid:
                            zbgvq__anb[aajr__fkd] = aajr__fkd
                            mas__hasl = hxymo__tacid[aajr__fkd]
                            cvp__dgx[mas__hasl] = hxymo__tacid[value]
                            jku__tarel.append(mas__hasl)
                        else:
                            zbgvq__anb[aajr__fkd] = value
                            hxymo__tacid[value] = hxymo__tacid[aajr__fkd]
            rbf__lkh = np.sort(np.array(jku__tarel))
            yho__fkqu = 0
            lfk__ixom = []
            for mku__vyqye in range(-1, n):
                while yho__fkqu < len(rbf__lkh) and mku__vyqye > rbf__lkh[
                    yho__fkqu]:
                    yho__fkqu += 1
                lfk__ixom.append(yho__fkqu)
            for naxn__bhexy in range(-1, n):
                fac__zyrp = naxn__bhexy
                if naxn__bhexy in cvp__dgx:
                    fac__zyrp = cvp__dgx[naxn__bhexy]
                tiuf__llwvz[naxn__bhexy + 1] = fac__zyrp - lfk__ixom[
                    fac__zyrp + 1]
            return zbgvq__anb, tiuf__llwvz, len(rbf__lkh)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for zcov__tvgew in range(len(new_codes_arr)):
        new_codes_arr[zcov__tvgew] = codes_map_arr[old_codes_arr[
            zcov__tvgew] + 1]


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
    ycr__jxz = arr.dtype.ordered
    fozou__knnd = arr.dtype.elem_type
    eyo__stx = get_overload_const(to_replace)
    jmp__dnmlw = get_overload_const(value)
    if (arr.dtype.categories is not None and eyo__stx is not NOT_CONSTANT and
        jmp__dnmlw is not NOT_CONSTANT):
        artke__dcfso, codes_map_arr, hbaf__xbaks = python_build_replace_dicts(
            eyo__stx, jmp__dnmlw, arr.dtype.categories)
        if len(artke__dcfso) == 0:
            return lambda arr, to_replace, value: arr.copy()
        yimq__rpyua = []
        for amwcy__ouu in arr.dtype.categories:
            if amwcy__ouu in artke__dcfso:
                gdj__pkvr = artke__dcfso[amwcy__ouu]
                if gdj__pkvr != amwcy__ouu:
                    yimq__rpyua.append(gdj__pkvr)
            else:
                yimq__rpyua.append(amwcy__ouu)
        ekvin__yjcci = pd.CategoricalDtype(yimq__rpyua, ycr__jxz
            ).categories.values
        dgk__bykjm = MetaType(tuple(ekvin__yjcci))

        def impl_dtype(arr, to_replace, value):
            fygfy__alq = init_cat_dtype(bodo.utils.conversion.
                index_from_array(ekvin__yjcci), ycr__jxz, None, dgk__bykjm)
            gzs__hujv = alloc_categorical_array(len(arr.codes), fygfy__alq)
            reassign_codes(gzs__hujv.codes, arr.codes, codes_map_arr)
            return gzs__hujv
        return impl_dtype
    fozou__knnd = arr.dtype.elem_type
    if fozou__knnd == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            zbgvq__anb, codes_map_arr, ymyuw__yil = build_replace_dicts(
                to_replace, value, categories.values)
            if len(zbgvq__anb) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), ycr__jxz,
                    None, None))
            n = len(categories)
            ekvin__yjcci = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                ymyuw__yil, -1)
            vvlle__ptsey = 0
            for mku__vyqye in range(n):
                cydg__zkbr = categories[mku__vyqye]
                if cydg__zkbr in zbgvq__anb:
                    vzhg__tvf = zbgvq__anb[cydg__zkbr]
                    if vzhg__tvf != cydg__zkbr:
                        ekvin__yjcci[vvlle__ptsey] = vzhg__tvf
                        vvlle__ptsey += 1
                else:
                    ekvin__yjcci[vvlle__ptsey] = cydg__zkbr
                    vvlle__ptsey += 1
            gzs__hujv = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                ekvin__yjcci), ycr__jxz, None, None))
            reassign_codes(gzs__hujv.codes, arr.codes, codes_map_arr)
            return gzs__hujv
        return impl_str
    kumbk__sjx = dtype_to_array_type(fozou__knnd)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        zbgvq__anb, codes_map_arr, ymyuw__yil = build_replace_dicts(to_replace,
            value, categories.values)
        if len(zbgvq__anb) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), ycr__jxz, None, None))
        n = len(categories)
        ekvin__yjcci = bodo.utils.utils.alloc_type(n - ymyuw__yil,
            kumbk__sjx, None)
        vvlle__ptsey = 0
        for zcov__tvgew in range(n):
            cydg__zkbr = categories[zcov__tvgew]
            if cydg__zkbr in zbgvq__anb:
                vzhg__tvf = zbgvq__anb[cydg__zkbr]
                if vzhg__tvf != cydg__zkbr:
                    ekvin__yjcci[vvlle__ptsey] = vzhg__tvf
                    vvlle__ptsey += 1
            else:
                ekvin__yjcci[vvlle__ptsey] = cydg__zkbr
                vvlle__ptsey += 1
        gzs__hujv = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(ekvin__yjcci), ycr__jxz,
            None, None))
        reassign_codes(gzs__hujv.codes, arr.codes, codes_map_arr)
        return gzs__hujv
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
    lalmw__qtxp = dict()
    vqml__rpbl = 0
    for zcov__tvgew in range(len(vals)):
        val = vals[zcov__tvgew]
        if val in lalmw__qtxp:
            continue
        lalmw__qtxp[val] = vqml__rpbl
        vqml__rpbl += 1
    return lalmw__qtxp


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    lalmw__qtxp = dict()
    for zcov__tvgew in range(len(vals)):
        val = vals[zcov__tvgew]
        lalmw__qtxp[val] = zcov__tvgew
    return lalmw__qtxp


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    shc__ysv = dict(fastpath=fastpath)
    praug__mbh = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', shc__ysv, praug__mbh)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        qwn__abe = get_overload_const(categories)
        if qwn__abe is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                bxxx__qfiq = False
            else:
                bxxx__qfiq = get_overload_const_bool(ordered)
            qzzb__vwcsk = pd.CategoricalDtype(qwn__abe, bxxx__qfiq
                ).categories.values
            clq__rpua = MetaType(tuple(qzzb__vwcsk))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                fygfy__alq = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(qzzb__vwcsk), bxxx__qfiq, None, clq__rpua)
                return bodo.utils.conversion.fix_arr_dtype(data, fygfy__alq)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            oet__ytp = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                oet__ytp, ordered, None, None)
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
            dqxpi__kxugm = arr.codes[ind]
            return arr.dtype.categories[max(dqxpi__kxugm, 0)]
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
    for zcov__tvgew in range(len(arr1)):
        if arr1[zcov__tvgew] != arr2[zcov__tvgew]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    bch__suak = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    riwl__nbawr = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    rlo__ktnt = categorical_arrs_match(arr, val)
    xgusq__uqst = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    pjvi__mozq = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not bch__suak:
            raise BodoError(xgusq__uqst)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            dqxpi__kxugm = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = dqxpi__kxugm
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (bch__suak or riwl__nbawr or rlo__ktnt !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xgusq__uqst)
        if rlo__ktnt == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(pjvi__mozq)
        if bch__suak:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dxo__uvljr = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for mku__vyqye in range(n):
                    arr.codes[ind[mku__vyqye]] = dxo__uvljr
            return impl_scalar
        if rlo__ktnt == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for zcov__tvgew in range(n):
                    arr.codes[ind[zcov__tvgew]] = val.codes[zcov__tvgew]
            return impl_arr_ind_mask
        if rlo__ktnt == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(pjvi__mozq)
                n = len(val.codes)
                for zcov__tvgew in range(n):
                    arr.codes[ind[zcov__tvgew]] = val.codes[zcov__tvgew]
            return impl_arr_ind_mask
        if riwl__nbawr:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for mku__vyqye in range(n):
                    srrl__uzn = bodo.utils.conversion.unbox_if_timestamp(val
                        [mku__vyqye])
                    if srrl__uzn not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    dqxpi__kxugm = categories.get_loc(srrl__uzn)
                    arr.codes[ind[mku__vyqye]] = dqxpi__kxugm
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (bch__suak or riwl__nbawr or rlo__ktnt !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xgusq__uqst)
        if rlo__ktnt == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(pjvi__mozq)
        if bch__suak:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dxo__uvljr = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for mku__vyqye in range(n):
                    if ind[mku__vyqye]:
                        arr.codes[mku__vyqye] = dxo__uvljr
            return impl_scalar
        if rlo__ktnt == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                vac__pbgzs = 0
                for zcov__tvgew in range(n):
                    if ind[zcov__tvgew]:
                        arr.codes[zcov__tvgew] = val.codes[vac__pbgzs]
                        vac__pbgzs += 1
            return impl_bool_ind_mask
        if rlo__ktnt == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(pjvi__mozq)
                n = len(ind)
                vac__pbgzs = 0
                for zcov__tvgew in range(n):
                    if ind[zcov__tvgew]:
                        arr.codes[zcov__tvgew] = val.codes[vac__pbgzs]
                        vac__pbgzs += 1
            return impl_bool_ind_mask
        if riwl__nbawr:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                vac__pbgzs = 0
                categories = arr.dtype.categories
                for mku__vyqye in range(n):
                    if ind[mku__vyqye]:
                        srrl__uzn = bodo.utils.conversion.unbox_if_timestamp(
                            val[vac__pbgzs])
                        if srrl__uzn not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        dqxpi__kxugm = categories.get_loc(srrl__uzn)
                        arr.codes[mku__vyqye] = dqxpi__kxugm
                        vac__pbgzs += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (bch__suak or riwl__nbawr or rlo__ktnt !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xgusq__uqst)
        if rlo__ktnt == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(pjvi__mozq)
        if bch__suak:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dxo__uvljr = arr.dtype.categories.get_loc(val)
                yasi__rfj = numba.cpython.unicode._normalize_slice(ind, len
                    (arr))
                for mku__vyqye in range(yasi__rfj.start, yasi__rfj.stop,
                    yasi__rfj.step):
                    arr.codes[mku__vyqye] = dxo__uvljr
            return impl_scalar
        if rlo__ktnt == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if rlo__ktnt == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(pjvi__mozq)
                arr.codes[ind] = val.codes
            return impl_arr
        if riwl__nbawr:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                yasi__rfj = numba.cpython.unicode._normalize_slice(ind, len
                    (arr))
                vac__pbgzs = 0
                for mku__vyqye in range(yasi__rfj.start, yasi__rfj.stop,
                    yasi__rfj.step):
                    srrl__uzn = bodo.utils.conversion.unbox_if_timestamp(val
                        [vac__pbgzs])
                    if srrl__uzn not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    dqxpi__kxugm = categories.get_loc(srrl__uzn)
                    arr.codes[mku__vyqye] = dqxpi__kxugm
                    vac__pbgzs += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
