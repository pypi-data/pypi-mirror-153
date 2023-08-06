import datetime
import operator
import warnings
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_constant
from numba.core.typing.templates import AttributeTemplate, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
import bodo.hiframes
import bodo.utils.conversion
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_func, get_overload_const_int, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, get_val_type_maybe_str_literal, is_const_func_type, is_heterogeneous_tuple_type, is_iterable_type, is_overload_constant_int, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
from bodo.utils.utils import is_null_value
_dt_index_data_typ = types.Array(types.NPDatetime('ns'), 1, 'C')
_timedelta_index_data_typ = types.Array(types.NPTimedelta('ns'), 1, 'C')
iNaT = pd._libs.tslibs.iNaT
NaT = types.NPDatetime('ns')('NaT')
idx_cpy_arg_defaults = dict(deep=False, dtype=None, names=None)
idx_typ_to_format_str_map = dict()


@typeof_impl.register(pd.Index)
def typeof_pd_index(val, c):
    if val.inferred_type == 'string' or pd._libs.lib.infer_dtype(val, True
        ) == 'string':
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'bytes' or pd._libs.lib.infer_dtype(val, True
        ) == 'bytes':
        return BinaryIndexType(get_val_type_maybe_str_literal(val.name))
    if val.equals(pd.Index([])):
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'date':
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'integer' or pd._libs.lib.infer_dtype(val, True
        ) == 'integer':
        if isinstance(val.dtype, pd.core.arrays.integer._IntegerDtype):
            wqgo__kqhhd = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(wqgo__kqhhd)
        else:
            dtype = types.int64
        return NumericIndexType(dtype, get_val_type_maybe_str_literal(val.
            name), IntegerArrayType(dtype))
    if val.inferred_type == 'boolean' or pd._libs.lib.infer_dtype(val, True
        ) == 'boolean':
        return NumericIndexType(types.bool_, get_val_type_maybe_str_literal
            (val.name), boolean_array)
    raise NotImplementedError(f'unsupported pd.Index type {val}')


class DatetimeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.datetime64ns, 1, 'C'
            ) if data is None else data
        super(DatetimeIndexType, self).__init__(name=
            f'DatetimeIndex({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def tzval(self):
        return self.data.tz if isinstance(self.data, bodo.DatetimeArrayType
            ) else None

    def copy(self):
        return DatetimeIndexType(self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return self.data.dtype.type_name

    @property
    def numpy_type_name(self):
        return str(self.data.dtype)


types.datetime_index = DatetimeIndexType()


@typeof_impl.register(pd.DatetimeIndex)
def typeof_datetime_index(val, c):
    if isinstance(val.dtype, pd.DatetimeTZDtype):
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name),
            DatetimeArrayType(val.tz))
    return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(DatetimeIndexType)
class DatetimeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    fhcn__sxtk = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', jneq__nhwyn, idx_cpy_arg_defaults,
        fn_str=fhcn__sxtk, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), A._name)
    return impl


@box(DatetimeIndexType)
def box_dt_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    ukv__dgqej = c.pyapi.import_module_noblock(ltzos__znxd)
    kyrj__jbjc = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, kyrj__jbjc.data)
    gxeax__ilq = c.pyapi.from_native_value(typ.data, kyrj__jbjc.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, kyrj__jbjc.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, kyrj__jbjc.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([gxeax__ilq])
    kuhr__kvobm = c.pyapi.object_getattr_string(ukv__dgqej, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', zvwf__qqeeu)])
    mzp__nxaw = c.pyapi.call(kuhr__kvobm, args, kws)
    c.pyapi.decref(gxeax__ilq)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(ukv__dgqej)
    c.pyapi.decref(kuhr__kvobm)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return mzp__nxaw


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        cixr__oftn = c.pyapi.object_getattr_string(val, 'array')
    else:
        cixr__oftn = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, cixr__oftn).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dtype = _dt_index_data_typ.dtype
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ffqk__lrnkp.dict = anbwa__kcl
    c.pyapi.decref(cixr__oftn)
    c.pyapi.decref(zvwf__qqeeu)
    return NativeValue(ffqk__lrnkp._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        gwx__nzzed, pxh__wxx = args
        kyrj__jbjc = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        kyrj__jbjc.data = gwx__nzzed
        kyrj__jbjc.name = pxh__wxx
        context.nrt.incref(builder, signature.args[0], gwx__nzzed)
        context.nrt.incref(builder, signature.args[1], pxh__wxx)
        dtype = _dt_index_data_typ.dtype
        kyrj__jbjc.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return kyrj__jbjc._getvalue()
    ojiy__mzz = DatetimeIndexType(name, data)
    sig = signature(ojiy__mzz, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    kyhwe__oomu = args[0]
    if equiv_set.has_shape(kyhwe__oomu):
        return ArrayAnalysis.AnalyzeResult(shape=kyhwe__oomu, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    wbuij__fhyx = 'def impl(dti):\n'
    wbuij__fhyx += '    numba.parfors.parfor.init_prange()\n'
    wbuij__fhyx += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    wbuij__fhyx += (
        '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n')
    wbuij__fhyx += '    n = len(A)\n'
    wbuij__fhyx += '    S = np.empty(n, np.int64)\n'
    wbuij__fhyx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    wbuij__fhyx += '        val = A[i]\n'
    wbuij__fhyx += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        wbuij__fhyx += '        S[i] = ts.' + field + '()\n'
    else:
        wbuij__fhyx += '        S[i] = ts.' + field + '\n'
    wbuij__fhyx += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'numba': numba, 'np': np, 'bodo': bodo}, oaywh__eyyff)
    impl = oaywh__eyyff['impl']
    return impl


def _install_dti_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        if field in ['is_leap_year']:
            continue
        impl = gen_dti_field_impl(field)
        overload_attribute(DatetimeIndexType, field)(lambda dti: impl)


_install_dti_date_fields()


@overload_attribute(DatetimeIndexType, 'is_leap_year')
def overload_datetime_index_is_leap_year(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        mbby__numqz = len(A)
        S = np.empty(mbby__numqz, np.bool_)
        for i in numba.parfors.parfor.internal_prange(mbby__numqz):
            val = A[i]
            eel__thn = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(eel__thn.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        mbby__numqz = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            mbby__numqz)
        for i in numba.parfors.parfor.internal_prange(mbby__numqz):
            val = A[i]
            eel__thn = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(eel__thn.year, eel__thn.month, eel__thn.day)
        return S
    return impl


@numba.njit(no_cpython_wrapper=True)
def _dti_val_finalize(s, count):
    if not count:
        s = iNaT
    return bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(s)


@numba.njit(no_cpython_wrapper=True)
def _tdi_val_finalize(s, count):
    return pd.Timedelta('nan') if not count else pd.Timedelta(s)


@overload_method(DatetimeIndexType, 'min', no_unliteral=True)
def overload_datetime_index_min(dti, axis=None, skipna=True):
    eeyru__wzx = dict(axis=axis, skipna=skipna)
    vbgry__awyk = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        pdmft__bysy = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(pdmft__bysy)):
            if not bodo.libs.array_kernels.isna(pdmft__bysy, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    pdmft__bysy[i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    eeyru__wzx = dict(axis=axis, skipna=skipna)
    vbgry__awyk = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        pdmft__bysy = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(pdmft__bysy)):
            if not bodo.libs.array_kernels.isna(pdmft__bysy, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    pdmft__bysy[i])
                s = max(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):

    def impl(A, tz):
        return init_datetime_index(A._data.tz_convert(tz), A._name)
    return impl


@infer_getattr
class DatetimeIndexAttribute(AttributeTemplate):
    key = DatetimeIndexType

    def resolve_values(self, ary):
        return _dt_index_data_typ


@overload(pd.DatetimeIndex, no_unliteral=True)
def pd_datetimeindex_overload(data=None, freq=None, tz=None, normalize=
    False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False,
    dtype=None, copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.DatetimeIndex() expected')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.DatetimeIndex()')
    eeyru__wzx = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    vbgry__awyk = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        ooj__ubz = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(ooj__ubz)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        htl__myj = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            pdmft__bysy = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            mbby__numqz = len(pdmft__bysy)
            S = np.empty(mbby__numqz, htl__myj)
            iiqxa__awy = rhs.value
            for i in numba.parfors.parfor.internal_prange(mbby__numqz):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    pdmft__bysy[i]) - iiqxa__awy)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        htl__myj = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            pdmft__bysy = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            mbby__numqz = len(pdmft__bysy)
            S = np.empty(mbby__numqz, htl__myj)
            iiqxa__awy = lhs.value
            for i in numba.parfors.parfor.internal_prange(mbby__numqz):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    iiqxa__awy - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(pdmft__bysy[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    tqhw__pkh = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    wbuij__fhyx = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        wbuij__fhyx += '  dt_index, _str = lhs, rhs\n'
        etsn__zzp = 'arr[i] {} other'.format(tqhw__pkh)
    else:
        wbuij__fhyx += '  dt_index, _str = rhs, lhs\n'
        etsn__zzp = 'other {} arr[i]'.format(tqhw__pkh)
    wbuij__fhyx += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    wbuij__fhyx += '  l = len(arr)\n'
    wbuij__fhyx += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    wbuij__fhyx += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    wbuij__fhyx += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    wbuij__fhyx += '    S[i] = {}\n'.format(etsn__zzp)
    wbuij__fhyx += '  return S\n'
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'bodo': bodo, 'numba': numba, 'np': np}, oaywh__eyyff)
    impl = oaywh__eyyff['impl']
    return impl


def overload_binop_dti_str(op):

    def overload_impl(lhs, rhs):
        if isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, True)
        if isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, False)
    return overload_impl


@overload(pd.Index, inline='always', no_unliteral=True)
def pd_index_overload(data=None, dtype=None, copy=False, name=None,
    tupleize_cols=True):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.Index()')
    data = types.unliteral(data) if not isinstance(data, types.LiteralList
        ) else data
    if not is_overload_none(dtype):
        zifiw__jliq = parse_dtype(dtype, 'pandas.Index')
        uomj__eao = False
    else:
        zifiw__jliq = getattr(data, 'dtype', None)
        uomj__eao = True
    if isinstance(zifiw__jliq, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType
        ) or zifiw__jliq == types.NPDatetime('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or zifiw__jliq == types.NPTimedelta('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.TimedeltaIndex(data, name=name)
    elif is_heterogeneous_tuple_type(data):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return bodo.hiframes.pd_index_ext.init_heter_index(data, name)
        return impl
    elif bodo.utils.utils.is_array_typ(data, False) or isinstance(data, (
        SeriesType, types.List, types.UniTuple)):
        if isinstance(zifiw__jliq, (types.Integer, types.Float, types.Boolean)
            ):
            if uomj__eao:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    ooj__ubz = bodo.utils.conversion.coerce_to_array(data)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        ooj__ubz, name)
            else:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    ooj__ubz = bodo.utils.conversion.coerce_to_array(data)
                    wlndw__irmps = bodo.utils.conversion.fix_arr_dtype(ooj__ubz
                        , zifiw__jliq)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        wlndw__irmps, name)
        elif zifiw__jliq in [types.string, bytes_type]:

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                return bodo.hiframes.pd_index_ext.init_binary_str_index(bodo
                    .utils.conversion.coerce_to_array(data), name)
        else:
            raise BodoError(
                'pd.Index(): provided array is of unsupported type.')
    elif is_overload_none(data):
        raise BodoError(
            'data argument in pd.Index() is invalid: None or scalar is not acceptable'
            )
    else:
        raise BodoError(
            f'pd.Index(): the provided argument type {data} is not supported')
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_datetime_index_getitem(dti, ind):
    if isinstance(dti, DatetimeIndexType):
        if isinstance(ind, types.Integer):

            def impl(dti, ind):
                rggim__kwi = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = rggim__kwi[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                rggim__kwi = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                sakrv__gwcfi = rggim__kwi[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(
                    sakrv__gwcfi, name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            hicaj__ksw = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(hicaj__ksw[ind])
        return impl

    def impl(I, ind):
        hicaj__ksw = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        sakrv__gwcfi = hicaj__ksw[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(sakrv__gwcfi,
            name)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_categorical_index_getitem(I, ind):
    if not isinstance(I, CategoricalIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            zflvg__hrkv = bodo.hiframes.pd_index_ext.get_index_data(I)
            val = zflvg__hrkv[ind]
            return val
        return impl
    if isinstance(ind, types.SliceType):

        def impl(I, ind):
            zflvg__hrkv = bodo.hiframes.pd_index_ext.get_index_data(I)
            name = bodo.hiframes.pd_index_ext.get_index_name(I)
            sakrv__gwcfi = zflvg__hrkv[ind]
            return bodo.hiframes.pd_index_ext.init_categorical_index(
                sakrv__gwcfi, name)
        return impl
    raise BodoError(
        f'pd.CategoricalIndex.__getitem__: unsupported index type {ind}')


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    gztu__ertd = False
    khbd__ivm = False
    if closed is None:
        gztu__ertd = True
        khbd__ivm = True
    elif closed == 'left':
        gztu__ertd = True
    elif closed == 'right':
        khbd__ivm = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return gztu__ertd, khbd__ivm


@numba.njit(no_cpython_wrapper=True)
def to_offset_value(freq):
    if freq is None:
        return None
    with numba.objmode(r='int64'):
        r = pd.tseries.frequencies.to_offset(freq).nanos
    return r


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _dummy_convert_none_to_int(val):
    if is_overload_none(val):

        def impl(val):
            return 0
        return impl
    if isinstance(val, types.Optional):

        def impl(val):
            if val is None:
                return 0
            return bodo.utils.indexing.unoptional(val)
        return impl
    return lambda val: val


@overload(pd.date_range, inline='always')
def pd_date_range_overload(start=None, end=None, periods=None, freq=None,
    tz=None, normalize=False, name=None, closed=None):
    eeyru__wzx = dict(tz=tz, normalize=normalize, closed=closed)
    vbgry__awyk = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    vjix__ucsd = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        vjix__ucsd = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    wbuij__fhyx = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    wbuij__fhyx += vjix__ucsd
    if is_overload_none(start):
        wbuij__fhyx += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        wbuij__fhyx += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        wbuij__fhyx += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        wbuij__fhyx += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        wbuij__fhyx += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            wbuij__fhyx += '  b = start_t.value\n'
            wbuij__fhyx += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            wbuij__fhyx += '  b = start_t.value\n'
            wbuij__fhyx += '  addend = np.int64(periods) * np.int64(stride)\n'
            wbuij__fhyx += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            wbuij__fhyx += '  e = end_t.value + stride\n'
            wbuij__fhyx += '  addend = np.int64(periods) * np.int64(-stride)\n'
            wbuij__fhyx += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        wbuij__fhyx += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        wbuij__fhyx += '  delta = end_t.value - start_t.value\n'
        wbuij__fhyx += '  step = delta / (periods - 1)\n'
        wbuij__fhyx += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        wbuij__fhyx += '  arr1 *= step\n'
        wbuij__fhyx += '  arr1 += start_t.value\n'
        wbuij__fhyx += '  arr = arr1.astype(np.int64)\n'
        wbuij__fhyx += '  arr[-1] = end_t.value\n'
    wbuij__fhyx += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    wbuij__fhyx += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'bodo': bodo, 'np': np, 'pd': pd}, oaywh__eyyff)
    f = oaywh__eyyff['f']
    return f


@overload(pd.timedelta_range, no_unliteral=True)
def pd_timedelta_range_overload(start=None, end=None, periods=None, freq=
    None, name=None, closed=None):
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, name=None, closed=None
        ):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        vobf__pqh = pd.Timedelta('1 day')
        if start is not None:
            vobf__pqh = pd.Timedelta(start)
        xdw__osfhl = pd.Timedelta('1 day')
        if end is not None:
            xdw__osfhl = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        gztu__ertd, khbd__ivm = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            xpdh__zjjmg = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = vobf__pqh.value
                mqa__ffyo = b + (xdw__osfhl.value - b
                    ) // xpdh__zjjmg * xpdh__zjjmg + xpdh__zjjmg // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = vobf__pqh.value
                vxrhc__bpt = np.int64(periods) * np.int64(xpdh__zjjmg)
                mqa__ffyo = np.int64(b) + vxrhc__bpt
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                mqa__ffyo = xdw__osfhl.value + xpdh__zjjmg
                vxrhc__bpt = np.int64(periods) * np.int64(-xpdh__zjjmg)
                b = np.int64(mqa__ffyo) + vxrhc__bpt
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            bwyqp__nfh = np.arange(b, mqa__ffyo, xpdh__zjjmg, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            qru__ethi = xdw__osfhl.value - vobf__pqh.value
            step = qru__ethi / (periods - 1)
            agaa__rsd = np.arange(0, periods, 1, np.float64)
            agaa__rsd *= step
            agaa__rsd += vobf__pqh.value
            bwyqp__nfh = agaa__rsd.astype(np.int64)
            bwyqp__nfh[-1] = xdw__osfhl.value
        if not gztu__ertd and len(bwyqp__nfh) and bwyqp__nfh[0
            ] == vobf__pqh.value:
            bwyqp__nfh = bwyqp__nfh[1:]
        if not khbd__ivm and len(bwyqp__nfh) and bwyqp__nfh[-1
            ] == xdw__osfhl.value:
            bwyqp__nfh = bwyqp__nfh[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(bwyqp__nfh)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        mbby__numqz = len(A)
        nqfa__nsb = bodo.libs.int_arr_ext.alloc_int_array(mbby__numqz, np.
            uint32)
        jwv__xxeej = bodo.libs.int_arr_ext.alloc_int_array(mbby__numqz, np.
            uint32)
        cibls__cgpnh = bodo.libs.int_arr_ext.alloc_int_array(mbby__numqz,
            np.uint32)
        for i in numba.parfors.parfor.internal_prange(mbby__numqz):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(nqfa__nsb, i)
                bodo.libs.array_kernels.setna(jwv__xxeej, i)
                bodo.libs.array_kernels.setna(cibls__cgpnh, i)
                continue
            nqfa__nsb[i], jwv__xxeej[i], cibls__cgpnh[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((nqfa__nsb,
            jwv__xxeej, cibls__cgpnh), idx, ('year', 'week', 'day'))
    return impl


class TimedeltaIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.timedelta64ns, 1, 'C'
            ) if data is None else data
        super(TimedeltaIndexType, self).__init__(name=
            f'TimedeltaIndexType({name_typ}, {self.data})')
    ndim = 1

    def copy(self):
        return TimedeltaIndexType(self.name_typ)

    @property
    def dtype(self):
        return types.NPTimedelta('ns')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.name_typ, self.data

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return 'timedelta'

    @property
    def numpy_type_name(self):
        return 'timedelta64[ns]'


timedelta_index = TimedeltaIndexType()
types.timedelta_index = timedelta_index


@register_model(TimedeltaIndexType)
class TimedeltaIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', _timedelta_index_data_typ), ('name', fe_type
            .name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, wpt__uwhnk)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    ukv__dgqej = c.pyapi.import_module_noblock(ltzos__znxd)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    gxeax__ilq = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([gxeax__ilq])
    kws = c.pyapi.dict_pack([('name', zvwf__qqeeu)])
    kuhr__kvobm = c.pyapi.object_getattr_string(ukv__dgqej, 'TimedeltaIndex')
    mzp__nxaw = c.pyapi.call(kuhr__kvobm, args, kws)
    c.pyapi.decref(gxeax__ilq)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(ukv__dgqej)
    c.pyapi.decref(kuhr__kvobm)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return mzp__nxaw


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    kpbsz__sdg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, kpbsz__sdg).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    c.pyapi.decref(kpbsz__sdg)
    c.pyapi.decref(zvwf__qqeeu)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dtype = _timedelta_index_data_typ.dtype
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ffqk__lrnkp.dict = anbwa__kcl
    return NativeValue(ffqk__lrnkp._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        gwx__nzzed, pxh__wxx = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = gwx__nzzed
        timedelta_index.name = pxh__wxx
        context.nrt.incref(builder, signature.args[0], gwx__nzzed)
        context.nrt.incref(builder, signature.args[1], pxh__wxx)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    ojiy__mzz = TimedeltaIndexType(name)
    sig = signature(ojiy__mzz, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_timedelta_index
    ) = init_index_equiv


@infer_getattr
class TimedeltaIndexAttribute(AttributeTemplate):
    key = TimedeltaIndexType

    def resolve_values(self, ary):
        return _timedelta_index_data_typ


make_attribute_wrapper(TimedeltaIndexType, 'data', '_data')
make_attribute_wrapper(TimedeltaIndexType, 'name', '_name')
make_attribute_wrapper(TimedeltaIndexType, 'dict', '_dict')


@overload_method(TimedeltaIndexType, 'copy', no_unliteral=True)
def overload_timedelta_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    fhcn__sxtk = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()')
    check_unsupported_args('TimedeltaIndex.copy', jneq__nhwyn,
        idx_cpy_arg_defaults, fn_str=fhcn__sxtk, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), A._name)
    return impl


@overload_method(TimedeltaIndexType, 'min', inline='always', no_unliteral=True)
def overload_timedelta_index_min(tdi, axis=None, skipna=True):
    eeyru__wzx = dict(axis=axis, skipna=skipna)
    vbgry__awyk = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        mbby__numqz = len(data)
        ixk__zga = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(mbby__numqz):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            ixk__zga = min(ixk__zga, val)
        imi__xnnc = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            ixk__zga)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(imi__xnnc, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    eeyru__wzx = dict(axis=axis, skipna=skipna)
    vbgry__awyk = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        mbby__numqz = len(data)
        qeg__tjcs = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(mbby__numqz):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            qeg__tjcs = max(qeg__tjcs, val)
        imi__xnnc = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            qeg__tjcs)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(imi__xnnc, count)
    return impl


def gen_tdi_field_impl(field):
    wbuij__fhyx = 'def impl(tdi):\n'
    wbuij__fhyx += '    numba.parfors.parfor.init_prange()\n'
    wbuij__fhyx += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    wbuij__fhyx += (
        '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n')
    wbuij__fhyx += '    n = len(A)\n'
    wbuij__fhyx += '    S = np.empty(n, np.int64)\n'
    wbuij__fhyx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    wbuij__fhyx += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        wbuij__fhyx += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        wbuij__fhyx += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        wbuij__fhyx += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        wbuij__fhyx += (
            '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
    else:
        assert False, 'invalid timedelta field'
    wbuij__fhyx += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'numba': numba, 'np': np, 'bodo': bodo}, oaywh__eyyff)
    impl = oaywh__eyyff['impl']
    return impl


def _install_tdi_time_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        impl = gen_tdi_field_impl(field)
        overload_attribute(TimedeltaIndexType, field)(lambda tdi: impl)


_install_tdi_time_fields()


@overload(pd.TimedeltaIndex, no_unliteral=True)
def pd_timedelta_index_overload(data=None, unit=None, freq=None, dtype=None,
    copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.TimedeltaIndex() expected')
    eeyru__wzx = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    vbgry__awyk = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        ooj__ubz = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(ooj__ubz)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return impl


class RangeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        if name_typ is None:
            name_typ = types.none
        self.name_typ = name_typ
        super(RangeIndexType, self).__init__(name='RangeIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return RangeIndexType(self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.RangeIteratorType(types.int64)

    @property
    def dtype(self):
        return types.int64

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)

    def unify(self, typingctx, other):
        if isinstance(other, NumericIndexType):
            name_typ = self.name_typ.unify(typingctx, other.name_typ)
            if name_typ is None:
                name_typ = types.none
            return NumericIndexType(types.int64, name_typ)


@typeof_impl.register(pd.RangeIndex)
def typeof_pd_range_index(val, c):
    return RangeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(RangeIndexType)
class RangeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('start', types.int64), ('stop', types.int64), (
            'step', types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    fhcn__sxtk = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', jneq__nhwyn,
        idx_cpy_arg_defaults, fn_str=fhcn__sxtk, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, A._name)
    return impl


@box(RangeIndexType)
def box_range_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    jocn__reed = c.pyapi.import_module_noblock(ltzos__znxd)
    yddg__uvb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    upubt__ysdcg = c.pyapi.from_native_value(types.int64, yddg__uvb.start,
        c.env_manager)
    fttge__jmqd = c.pyapi.from_native_value(types.int64, yddg__uvb.stop, c.
        env_manager)
    yhwgh__xoje = c.pyapi.from_native_value(types.int64, yddg__uvb.step, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, yddg__uvb.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, yddg__uvb.name, c
        .env_manager)
    args = c.pyapi.tuple_pack([upubt__ysdcg, fttge__jmqd, yhwgh__xoje])
    kws = c.pyapi.dict_pack([('name', zvwf__qqeeu)])
    kuhr__kvobm = c.pyapi.object_getattr_string(jocn__reed, 'RangeIndex')
    tvrl__ozzux = c.pyapi.call(kuhr__kvobm, args, kws)
    c.pyapi.decref(upubt__ysdcg)
    c.pyapi.decref(fttge__jmqd)
    c.pyapi.decref(yhwgh__xoje)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(jocn__reed)
    c.pyapi.decref(kuhr__kvobm)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return tvrl__ozzux


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name
    pmrly__feyy = is_overload_constant_int(step) and get_overload_const_int(
        step) == 0

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        if pmrly__feyy:
            raise_bodo_error('Step must not be zero')
        cjc__txxtk = cgutils.is_scalar_zero(builder, args[2])
        uuvfh__nzig = context.get_python_api(builder)
        with builder.if_then(cjc__txxtk):
            uuvfh__nzig.err_format('PyExc_ValueError', 'Step must not be zero')
            val = context.get_constant(types.int32, -1)
            builder.ret(val)
        yddg__uvb = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        yddg__uvb.start = args[0]
        yddg__uvb.stop = args[1]
        yddg__uvb.step = args[2]
        yddg__uvb.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return yddg__uvb._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, pfqf__pzf = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    upubt__ysdcg = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, upubt__ysdcg).value
    fttge__jmqd = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, fttge__jmqd).value
    yhwgh__xoje = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, yhwgh__xoje).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    c.pyapi.decref(upubt__ysdcg)
    c.pyapi.decref(fttge__jmqd)
    c.pyapi.decref(yhwgh__xoje)
    c.pyapi.decref(zvwf__qqeeu)
    yddg__uvb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yddg__uvb.start = start
    yddg__uvb.stop = stop
    yddg__uvb.step = step
    yddg__uvb.name = name
    return NativeValue(yddg__uvb._getvalue())


@lower_constant(RangeIndexType)
def lower_constant_range_index(context, builder, ty, pyval):
    start = context.get_constant(types.int64, pyval.start)
    stop = context.get_constant(types.int64, pyval.stop)
    step = context.get_constant(types.int64, pyval.step)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    return lir.Constant.literal_struct([start, stop, step, name])


@overload(pd.RangeIndex, no_unliteral=True, inline='always')
def range_index_overload(start=None, stop=None, step=None, dtype=None, copy
    =False, name=None):

    def _ensure_int_or_none(value, field):
        ixjmf__sna = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(ixjmf__sna.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        ixjmf__sna = 'RangeIndex(...) must be called with integers'
        raise BodoError(ixjmf__sna)
    qkjc__ifd = 'start'
    dzt__tzx = 'stop'
    pjw__cht = 'step'
    if is_overload_none(start):
        qkjc__ifd = '0'
    if is_overload_none(stop):
        dzt__tzx = 'start'
        qkjc__ifd = '0'
    if is_overload_none(step):
        pjw__cht = '1'
    wbuij__fhyx = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    wbuij__fhyx += '  return init_range_index({}, {}, {}, name)\n'.format(
        qkjc__ifd, dzt__tzx, pjw__cht)
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'init_range_index': init_range_index}, oaywh__eyyff)
    kwg__pdr = oaywh__eyyff['_pd_range_index_imp']
    return kwg__pdr


@overload(pd.CategoricalIndex, no_unliteral=True, inline='always')
def categorical_index_overload(data=None, categories=None, ordered=None,
    dtype=None, copy=False, name=None):
    raise BodoError('pd.CategoricalIndex() initializer not yet supported.')


@overload_attribute(RangeIndexType, 'start')
def rangeIndex_get_start(ri):

    def impl(ri):
        return ri._start
    return impl


@overload_attribute(RangeIndexType, 'stop')
def rangeIndex_get_stop(ri):

    def impl(ri):
        return ri._stop
    return impl


@overload_attribute(RangeIndexType, 'step')
def rangeIndex_get_step(ri):

    def impl(ri):
        return ri._step
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_range_index_getitem(I, idx):
    if isinstance(I, RangeIndexType):
        if isinstance(types.unliteral(idx), types.Integer):
            return lambda I, idx: idx * I._step + I._start
        if isinstance(idx, types.SliceType):

            def impl(I, idx):
                owdbl__halk = numba.cpython.unicode._normalize_slice(idx,
                    len(I))
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * owdbl__halk.start
                stop = I._start + I._step * owdbl__halk.stop
                step = I._step * owdbl__halk.step
                return bodo.hiframes.pd_index_ext.init_range_index(start,
                    stop, step, name)
            return impl
        return lambda I, idx: bodo.hiframes.pd_index_ext.init_numeric_index(np
            .arange(I._start, I._stop, I._step, np.int64)[idx], bodo.
            hiframes.pd_index_ext.get_index_name(I))


@overload(len, no_unliteral=True)
def overload_range_len(r):
    if isinstance(r, RangeIndexType):
        return lambda r: max(0, -(-(r._stop - r._start) // r._step))


class PeriodIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, freq, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.freq = freq
        self.name_typ = name_typ
        super(PeriodIndexType, self).__init__(name=
            'PeriodIndexType({}, {})'.format(freq, name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return PeriodIndexType(self.freq, self.name_typ)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'period[{self.freq}]'


@typeof_impl.register(pd.PeriodIndex)
def typeof_pd_period_index(val, c):
    return PeriodIndexType(val.freqstr, get_val_type_maybe_str_literal(val.
        name))


@register_model(PeriodIndexType)
class PeriodIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', bodo.IntegerArrayType(types.int64)), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    fhcn__sxtk = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', jneq__nhwyn,
        idx_cpy_arg_defaults, fn_str=fhcn__sxtk, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), name, freq)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), A._name, freq)
    return impl


@intrinsic
def init_period_index(typingctx, data, name, freq):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        gwx__nzzed, pxh__wxx, pfqf__pzf = args
        qdjg__gmai = signature.return_type
        huldr__mwh = cgutils.create_struct_proxy(qdjg__gmai)(context, builder)
        huldr__mwh.data = gwx__nzzed
        huldr__mwh.name = pxh__wxx
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        huldr__mwh.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return huldr__mwh._getvalue()
    tfkcs__chs = get_overload_const_str(freq)
    ojiy__mzz = PeriodIndexType(tfkcs__chs, name)
    sig = signature(ojiy__mzz, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    jocn__reed = c.pyapi.import_module_noblock(ltzos__znxd)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        ffqk__lrnkp.data)
    cixr__oftn = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), ffqk__lrnkp.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ffqk__lrnkp.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, ffqk__lrnkp.name,
        c.env_manager)
    gejke__kkehx = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', cixr__oftn), ('name', zvwf__qqeeu),
        ('freq', gejke__kkehx)])
    kuhr__kvobm = c.pyapi.object_getattr_string(jocn__reed, 'PeriodIndex')
    tvrl__ozzux = c.pyapi.call(kuhr__kvobm, args, kws)
    c.pyapi.decref(cixr__oftn)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(gejke__kkehx)
    c.pyapi.decref(jocn__reed)
    c.pyapi.decref(kuhr__kvobm)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return tvrl__ozzux


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    zbh__unddo = c.pyapi.object_getattr_string(val, 'asi8')
    oypmi__suq = c.pyapi.call_method(val, 'isna', ())
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    ukv__dgqej = c.pyapi.import_module_noblock(ltzos__znxd)
    wleut__bttil = c.pyapi.object_getattr_string(ukv__dgqej, 'arrays')
    cixr__oftn = c.pyapi.call_method(wleut__bttil, 'IntegerArray', (
        zbh__unddo, oypmi__suq))
    data = c.pyapi.to_native_value(arr_typ, cixr__oftn).value
    c.pyapi.decref(zbh__unddo)
    c.pyapi.decref(oypmi__suq)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(ukv__dgqej)
    c.pyapi.decref(wleut__bttil)
    c.pyapi.decref(cixr__oftn)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    ffqk__lrnkp.dict = anbwa__kcl
    return NativeValue(ffqk__lrnkp._getvalue())


class CategoricalIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
        assert isinstance(data, CategoricalArrayType
            ), 'CategoricalIndexType expects CategoricalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(CategoricalIndexType, self).__init__(name=
            f'CategoricalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return CategoricalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'categorical'

    @property
    def numpy_type_name(self):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        return str(get_categories_int_type(self.dtype))

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, self.dtype.elem_type)


@register_model(CategoricalIndexType)
class CategoricalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        oqrg__mtz = get_categories_int_type(fe_type.data.dtype)
        wpt__uwhnk = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(oqrg__mtz, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type,
            wpt__uwhnk)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    ukv__dgqej = c.pyapi.import_module_noblock(ltzos__znxd)
    feqrh__zxudi = numba.core.cgutils.create_struct_proxy(typ)(c.context, c
        .builder, val)
    c.context.nrt.incref(c.builder, typ.data, feqrh__zxudi.data)
    gxeax__ilq = c.pyapi.from_native_value(typ.data, feqrh__zxudi.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, feqrh__zxudi.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, feqrh__zxudi.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([gxeax__ilq])
    kws = c.pyapi.dict_pack([('name', zvwf__qqeeu)])
    kuhr__kvobm = c.pyapi.object_getattr_string(ukv__dgqej, 'CategoricalIndex')
    mzp__nxaw = c.pyapi.call(kuhr__kvobm, args, kws)
    c.pyapi.decref(gxeax__ilq)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(ukv__dgqej)
    c.pyapi.decref(kuhr__kvobm)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return mzp__nxaw


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    kpbsz__sdg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, kpbsz__sdg).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    c.pyapi.decref(kpbsz__sdg)
    c.pyapi.decref(zvwf__qqeeu)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ffqk__lrnkp.dict = anbwa__kcl
    return NativeValue(ffqk__lrnkp._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        gwx__nzzed, pxh__wxx = args
        feqrh__zxudi = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        feqrh__zxudi.data = gwx__nzzed
        feqrh__zxudi.name = pxh__wxx
        context.nrt.incref(builder, signature.args[0], gwx__nzzed)
        context.nrt.incref(builder, signature.args[1], pxh__wxx)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        feqrh__zxudi.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return feqrh__zxudi._getvalue()
    ojiy__mzz = CategoricalIndexType(data, name)
    sig = signature(ojiy__mzz, data, name)
    return sig, codegen


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_categorical_index
    ) = init_index_equiv
make_attribute_wrapper(CategoricalIndexType, 'data', '_data')
make_attribute_wrapper(CategoricalIndexType, 'name', '_name')
make_attribute_wrapper(CategoricalIndexType, 'dict', '_dict')


@overload_method(CategoricalIndexType, 'copy', no_unliteral=True)
def overload_categorical_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    fhcn__sxtk = idx_typ_to_format_str_map[CategoricalIndexType].format(
        'copy()')
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', jneq__nhwyn,
        idx_cpy_arg_defaults, fn_str=fhcn__sxtk, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), A._name)
    return impl


class IntervalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.libs.interval_arr_ext import IntervalArrayType
        assert isinstance(data, IntervalArrayType
            ), 'IntervalIndexType expects IntervalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(IntervalIndexType, self).__init__(name=
            f'IntervalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return IntervalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'interval[{self.data.arr_type.dtype}, right]'


@register_model(IntervalIndexType)
class IntervalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, wpt__uwhnk)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    ukv__dgqej = c.pyapi.import_module_noblock(ltzos__znxd)
    wkh__vabsj = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, wkh__vabsj.data)
    gxeax__ilq = c.pyapi.from_native_value(typ.data, wkh__vabsj.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, wkh__vabsj.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, wkh__vabsj.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([gxeax__ilq])
    kws = c.pyapi.dict_pack([('name', zvwf__qqeeu)])
    kuhr__kvobm = c.pyapi.object_getattr_string(ukv__dgqej, 'IntervalIndex')
    mzp__nxaw = c.pyapi.call(kuhr__kvobm, args, kws)
    c.pyapi.decref(gxeax__ilq)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(ukv__dgqej)
    c.pyapi.decref(kuhr__kvobm)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return mzp__nxaw


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    kpbsz__sdg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, kpbsz__sdg).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    c.pyapi.decref(kpbsz__sdg)
    c.pyapi.decref(zvwf__qqeeu)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ffqk__lrnkp.dict = anbwa__kcl
    return NativeValue(ffqk__lrnkp._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        gwx__nzzed, pxh__wxx = args
        wkh__vabsj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        wkh__vabsj.data = gwx__nzzed
        wkh__vabsj.name = pxh__wxx
        context.nrt.incref(builder, signature.args[0], gwx__nzzed)
        context.nrt.incref(builder, signature.args[1], pxh__wxx)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        wkh__vabsj.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return wkh__vabsj._getvalue()
    ojiy__mzz = IntervalIndexType(data, name)
    sig = signature(ojiy__mzz, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_interval_index
    ) = init_index_equiv
make_attribute_wrapper(IntervalIndexType, 'data', '_data')
make_attribute_wrapper(IntervalIndexType, 'name', '_name')
make_attribute_wrapper(IntervalIndexType, 'dict', '_dict')


class NumericIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, dtype, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.dtype = dtype
        self.name_typ = name_typ
        data = dtype_to_array_type(dtype) if data is None else data
        self.data = data
        super(NumericIndexType, self).__init__(name=
            f'NumericIndexType({dtype}, {name_typ}, {data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return NumericIndexType(self.dtype, self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    Int64Index = pd.Int64Index
    UInt64Index = pd.UInt64Index
    Float64Index = pd.Float64Index


@typeof_impl.register(Int64Index)
def typeof_pd_int64_index(val, c):
    return NumericIndexType(types.int64, get_val_type_maybe_str_literal(val
        .name))


@typeof_impl.register(UInt64Index)
def typeof_pd_uint64_index(val, c):
    return NumericIndexType(types.uint64, get_val_type_maybe_str_literal(
        val.name))


@typeof_impl.register(Float64Index)
def typeof_pd_float64_index(val, c):
    return NumericIndexType(types.float64, get_val_type_maybe_str_literal(
        val.name))


@register_model(NumericIndexType)
class NumericIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    fhcn__sxtk = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', jneq__nhwyn, idx_cpy_arg_defaults,
        fn_str=fhcn__sxtk, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(NumericIndexType)
def box_numeric_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    jocn__reed = c.pyapi.import_module_noblock(ltzos__znxd)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, ffqk__lrnkp.data)
    cixr__oftn = c.pyapi.from_native_value(typ.data, ffqk__lrnkp.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ffqk__lrnkp.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, ffqk__lrnkp.name,
        c.env_manager)
    dug__aodbt = c.pyapi.make_none()
    clbb__vbu = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    tvrl__ozzux = c.pyapi.call_method(jocn__reed, 'Index', (cixr__oftn,
        dug__aodbt, clbb__vbu, zvwf__qqeeu))
    c.pyapi.decref(cixr__oftn)
    c.pyapi.decref(dug__aodbt)
    c.pyapi.decref(clbb__vbu)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(jocn__reed)
    c.context.nrt.decref(c.builder, typ, val)
    return tvrl__ozzux


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        qdjg__gmai = signature.return_type
        ffqk__lrnkp = cgutils.create_struct_proxy(qdjg__gmai)(context, builder)
        ffqk__lrnkp.data = args[0]
        ffqk__lrnkp.name = args[1]
        context.nrt.incref(builder, qdjg__gmai.data, args[0])
        context.nrt.incref(builder, qdjg__gmai.name_typ, args[1])
        dtype = qdjg__gmai.dtype
        ffqk__lrnkp.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return ffqk__lrnkp._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    kpbsz__sdg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, kpbsz__sdg).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    c.pyapi.decref(kpbsz__sdg)
    c.pyapi.decref(zvwf__qqeeu)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dtype = typ.dtype
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ffqk__lrnkp.dict = anbwa__kcl
    return NativeValue(ffqk__lrnkp._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        nsph__zveb = dict(dtype=dtype)
        imx__drizj = dict(dtype=None)
        check_unsupported_args(func_str, nsph__zveb, imx__drizj,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                ooj__ubz = bodo.utils.conversion.coerce_to_ndarray(data)
                ney__mfx = bodo.utils.conversion.fix_arr_dtype(ooj__ubz, np
                    .dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(ney__mfx,
                    name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                ooj__ubz = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    ooj__ubz = ooj__ubz.copy()
                ney__mfx = bodo.utils.conversion.fix_arr_dtype(ooj__ubz, np
                    .dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(ney__mfx,
                    name)
        return impl
    return overload_impl


def _install_numeric_constructors():
    for func, func_str, default_dtype in ((Int64Index, 'pandas.Int64Index',
        np.int64), (UInt64Index, 'pandas.UInt64Index', np.uint64), (
        Float64Index, 'pandas.Float64Index', np.float64)):
        overload_impl = create_numeric_constructor(func, func_str,
            default_dtype)
        overload(func, no_unliteral=True)(overload_impl)


_install_numeric_constructors()


class StringIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = string_array_type if data_typ is None else data_typ
        super(StringIndexType, self).__init__(name=
            f'StringIndexType({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return StringIndexType(self.name_typ, self.data)

    @property
    def dtype(self):
        return string_type

    @property
    def pandas_type_name(self):
        return 'unicode'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(StringIndexType)
class StringIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(StringIndexType, 'data', '_data')
make_attribute_wrapper(StringIndexType, 'name', '_name')
make_attribute_wrapper(StringIndexType, 'dict', '_dict')


class BinaryIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        assert data_typ is None or data_typ == binary_array_type, 'data_typ must be binary_array_type'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = binary_array_type
        super(BinaryIndexType, self).__init__(name='BinaryIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return BinaryIndexType(self.name_typ)

    @property
    def dtype(self):
        return bytes_type

    @property
    def pandas_type_name(self):
        return 'bytes'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(BinaryIndexType)
class BinaryIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', binary_array_type), ('name', fe_type.
            name_typ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    mejk__qec = typ.data
    scalar_type = typ.data.dtype
    kpbsz__sdg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(mejk__qec, kpbsz__sdg).value
    zvwf__qqeeu = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zvwf__qqeeu).value
    c.pyapi.decref(kpbsz__sdg)
    c.pyapi.decref(zvwf__qqeeu)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffqk__lrnkp.data = data
    ffqk__lrnkp.name = name
    dldej__apstr, anbwa__kcl = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    ffqk__lrnkp.dict = anbwa__kcl
    return NativeValue(ffqk__lrnkp._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    mejk__qec = typ.data
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    jocn__reed = c.pyapi.import_module_noblock(ltzos__znxd)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, mejk__qec, ffqk__lrnkp.data)
    cixr__oftn = c.pyapi.from_native_value(mejk__qec, ffqk__lrnkp.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ffqk__lrnkp.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, ffqk__lrnkp.name,
        c.env_manager)
    dug__aodbt = c.pyapi.make_none()
    clbb__vbu = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    tvrl__ozzux = c.pyapi.call_method(jocn__reed, 'Index', (cixr__oftn,
        dug__aodbt, clbb__vbu, zvwf__qqeeu))
    c.pyapi.decref(cixr__oftn)
    c.pyapi.decref(dug__aodbt)
    c.pyapi.decref(clbb__vbu)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(jocn__reed)
    c.context.nrt.decref(c.builder, typ, val)
    return tvrl__ozzux


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    zeml__mjpc = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, zeml__mjpc


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        kfbaf__ektm = 'bytes_type'
    else:
        kfbaf__ektm = 'string_type'
    wbuij__fhyx = 'def impl(context, builder, signature, args):\n'
    wbuij__fhyx += '    assert len(args) == 2\n'
    wbuij__fhyx += '    index_typ = signature.return_type\n'
    wbuij__fhyx += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    wbuij__fhyx += '    index_val.data = args[0]\n'
    wbuij__fhyx += '    index_val.name = args[1]\n'
    wbuij__fhyx += '    # increase refcount of stored values\n'
    wbuij__fhyx += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    wbuij__fhyx += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    wbuij__fhyx += '    # create empty dict for get_loc hashmap\n'
    wbuij__fhyx += '    index_val.dict = context.compile_internal(\n'
    wbuij__fhyx += '       builder,\n'
    wbuij__fhyx += (
        f'       lambda: numba.typed.Dict.empty({kfbaf__ektm}, types.int64),\n'
        )
    wbuij__fhyx += (
        f'        types.DictType({kfbaf__ektm}, types.int64)(), [],)\n')
    wbuij__fhyx += '    return index_val._getvalue()\n'
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, oaywh__eyyff)
    impl = oaywh__eyyff['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    fhcn__sxtk = idx_typ_to_format_str_map[typ].format('copy()')
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', jneq__nhwyn, idx_cpy_arg_defaults,
        fn_str=fhcn__sxtk, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), A._name)
    return impl


@overload_attribute(BinaryIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
@overload_attribute(DatetimeIndexType, 'name')
@overload_attribute(TimedeltaIndexType, 'name')
@overload_attribute(RangeIndexType, 'name')
@overload_attribute(PeriodIndexType, 'name')
@overload_attribute(NumericIndexType, 'name')
@overload_attribute(IntervalIndexType, 'name')
@overload_attribute(CategoricalIndexType, 'name')
@overload_attribute(MultiIndexType, 'name')
def Index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_index_getitem(I, ind):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType)
        ) and isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, NumericIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_numeric_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))
    if isinstance(I, (StringIndexType, BinaryIndexType)):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_binary_str_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))


def array_type_to_index(arr_typ, name_typ=None):
    if is_str_arr_type(arr_typ):
        return StringIndexType(name_typ, arr_typ)
    if arr_typ == bodo.binary_array_type:
        return BinaryIndexType(name_typ)
    assert isinstance(arr_typ, (types.Array, IntegerArrayType, bodo.
        CategoricalArrayType)) or arr_typ in (bodo.datetime_date_array_type,
        bodo.boolean_array
        ), f'Converting array type {arr_typ} to index not supported'
    if (arr_typ == bodo.datetime_date_array_type or arr_typ.dtype == types.
        NPDatetime('ns')):
        return DatetimeIndexType(name_typ)
    if isinstance(arr_typ, bodo.DatetimeArrayType):
        return DatetimeIndexType(name_typ, arr_typ)
    if isinstance(arr_typ, bodo.CategoricalArrayType):
        return CategoricalIndexType(arr_typ, name_typ)
    if arr_typ.dtype == types.NPTimedelta('ns'):
        return TimedeltaIndexType(name_typ)
    if isinstance(arr_typ.dtype, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(arr_typ.dtype, name_typ, arr_typ)
    raise BodoError(f'invalid index type {arr_typ}')


def is_pd_index_type(t):
    return isinstance(t, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, StringIndexType, BinaryIndexType, RangeIndexType,
        HeterogeneousIndexType))


@overload_method(RangeIndexType, 'take', no_unliteral=True)
@overload_method(NumericIndexType, 'take', no_unliteral=True)
@overload_method(StringIndexType, 'take', no_unliteral=True)
@overload_method(BinaryIndexType, 'take', no_unliteral=True)
@overload_method(CategoricalIndexType, 'take', no_unliteral=True)
@overload_method(PeriodIndexType, 'take', no_unliteral=True)
@overload_method(DatetimeIndexType, 'take', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'take', no_unliteral=True)
def overload_index_take(I, indices, axis=0, allow_fill=True, fill_value=None):
    eeyru__wzx = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    uch__pkcj = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', eeyru__wzx, uch__pkcj,
        package_name='pandas', module_name='Index')
    return lambda I, indices: I[indices]


def _init_engine(I, ban_unique=True):
    pass


@overload(_init_engine)
def overload_init_engine(I, ban_unique=True):
    if isinstance(I, CategoricalIndexType):

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                bwyqp__nfh = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(bwyqp__nfh)):
                    if not bodo.libs.array_kernels.isna(bwyqp__nfh, i):
                        val = (bodo.hiframes.pd_categorical_ext.
                            get_code_for_value(bwyqp__nfh.dtype, bwyqp__nfh[i])
                            )
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl
    else:

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                bwyqp__nfh = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(bwyqp__nfh)):
                    if not bodo.libs.array_kernels.isna(bwyqp__nfh, i):
                        val = bwyqp__nfh[i]
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl


@overload(operator.contains, no_unliteral=True)
def index_contains(I, val):
    if not is_index_type(I):
        return
    if isinstance(I, RangeIndexType):
        return lambda I, val: range_contains(I.start, I.stop, I.step, val)
    if isinstance(I, CategoricalIndexType):

        def impl(I, val):
            key = bodo.utils.conversion.unbox_if_timestamp(val)
            if not is_null_value(I._dict):
                _init_engine(I, False)
                bwyqp__nfh = bodo.utils.conversion.coerce_to_array(I)
                xpgg__bfyn = (bodo.hiframes.pd_categorical_ext.
                    get_code_for_value(bwyqp__nfh.dtype, key))
                return xpgg__bfyn in I._dict
            else:
                ixjmf__sna = (
                    'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                    )
                warnings.warn(ixjmf__sna)
                bwyqp__nfh = bodo.utils.conversion.coerce_to_array(I)
                ind = -1
                for i in range(len(bwyqp__nfh)):
                    if not bodo.libs.array_kernels.isna(bwyqp__nfh, i):
                        if bwyqp__nfh[i] == key:
                            ind = i
            return ind != -1
        return impl

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I, False)
            return key in I._dict
        else:
            ixjmf__sna = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(ixjmf__sna)
            bwyqp__nfh = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(bwyqp__nfh)):
                if not bodo.libs.array_kernels.isna(bwyqp__nfh, i):
                    if bwyqp__nfh[i] == key:
                        ind = i
        return ind != -1
    return impl


@register_jitable
def range_contains(start, stop, step, val):
    if step > 0 and not start <= val < stop:
        return False
    if step < 0 and not stop <= val < start:
        return False
    return (val - start) % step == 0


@overload_method(RangeIndexType, 'get_loc', no_unliteral=True)
@overload_method(NumericIndexType, 'get_loc', no_unliteral=True)
@overload_method(StringIndexType, 'get_loc', no_unliteral=True)
@overload_method(BinaryIndexType, 'get_loc', no_unliteral=True)
@overload_method(PeriodIndexType, 'get_loc', no_unliteral=True)
@overload_method(DatetimeIndexType, 'get_loc', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'get_loc', no_unliteral=True)
def overload_index_get_loc(I, key, method=None, tolerance=None):
    eeyru__wzx = dict(method=method, tolerance=tolerance)
    vbgry__awyk = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')
    key = types.unliteral(key)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.get_loc')
    if key == pd_timestamp_type:
        key = bodo.datetime64ns
    if key == pd_timedelta_type:
        key = bodo.timedelta64ns
    if key != I.dtype:
        raise_bodo_error(
            'Index.get_loc(): invalid label type in Index.get_loc()')
    if isinstance(I, RangeIndexType):

        def impl_range(I, key, method=None, tolerance=None):
            if not range_contains(I.start, I.stop, I.step, key):
                raise KeyError('Index.get_loc(): key not found')
            return key - I.start if I.step == 1 else (key - I.start) // I.step
        return impl_range

    def impl(I, key, method=None, tolerance=None):
        key = bodo.utils.conversion.unbox_if_timestamp(key)
        if not is_null_value(I._dict):
            _init_engine(I)
            ind = I._dict.get(key, -1)
        else:
            ixjmf__sna = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(ixjmf__sna)
            bwyqp__nfh = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(bwyqp__nfh)):
                if bwyqp__nfh[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        if ind == -1:
            raise KeyError('Index.get_loc(): key not found')
        return ind
    return impl


def create_isna_specific_method(overload_name):

    def overload_index_isna_specific_method(I):
        nqrz__hbpa = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                mbby__numqz = len(I)
                edh__ubdv = np.empty(mbby__numqz, np.bool_)
                for i in numba.parfors.parfor.internal_prange(mbby__numqz):
                    edh__ubdv[i] = not nqrz__hbpa
                return edh__ubdv
            return impl
        wbuij__fhyx = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if nqrz__hbpa else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        oaywh__eyyff = {}
        exec(wbuij__fhyx, {'bodo': bodo, 'np': np, 'numba': numba},
            oaywh__eyyff)
        impl = oaywh__eyyff['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for jrmy__osdz in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(jrmy__osdz, overload_name, no_unliteral=True,
                inline='always')(overload_impl)


_install_isna_specific_methods()


@overload_attribute(RangeIndexType, 'values')
@overload_attribute(NumericIndexType, 'values')
@overload_attribute(StringIndexType, 'values')
@overload_attribute(BinaryIndexType, 'values')
@overload_attribute(CategoricalIndexType, 'values')
@overload_attribute(PeriodIndexType, 'values')
@overload_attribute(DatetimeIndexType, 'values')
@overload_attribute(TimedeltaIndexType, 'values')
def overload_values(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I, 'Index.values'
        )
    return lambda I: bodo.utils.conversion.coerce_to_array(I)


@overload(len, no_unliteral=True)
def overload_index_len(I):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType,
        PeriodIndexType, IntervalIndexType, CategoricalIndexType,
        DatetimeIndexType, TimedeltaIndexType, HeterogeneousIndexType)):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I))


@overload_attribute(DatetimeIndexType, 'shape')
@overload_attribute(NumericIndexType, 'shape')
@overload_attribute(StringIndexType, 'shape')
@overload_attribute(BinaryIndexType, 'shape')
@overload_attribute(PeriodIndexType, 'shape')
@overload_attribute(TimedeltaIndexType, 'shape')
@overload_attribute(IntervalIndexType, 'shape')
@overload_attribute(CategoricalIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)),)


@overload_attribute(RangeIndexType, 'shape')
def overload_range_index_shape(s):
    return lambda s: (len(s),)


@overload_attribute(NumericIndexType, 'is_monotonic', inline='always')
@overload_attribute(RangeIndexType, 'is_monotonic', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic', inline='always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic', inline='always')
@overload_attribute(NumericIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_increasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_increasing', inline=
    'always')
def overload_index_is_montonic(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_increasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            bwyqp__nfh = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(bwyqp__nfh, 1)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step > 0 or len(I) <= 1
        return impl


@overload_attribute(NumericIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_decreasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_decreasing', inline=
    'always')
def overload_index_is_montonic_decreasing(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_decreasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            bwyqp__nfh = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(bwyqp__nfh, 2)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step < 0 or len(I) <= 1
        return impl


@overload_method(NumericIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(DatetimeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(TimedeltaIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(StringIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(PeriodIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(CategoricalIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(BinaryIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(RangeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
def overload_index_duplicated(I, keep='first'):
    if isinstance(I, RangeIndexType):

        def impl(I, keep='first'):
            return np.zeros(len(I), np.bool_)
        return impl

    def impl(I, keep='first'):
        bwyqp__nfh = bodo.hiframes.pd_index_ext.get_index_data(I)
        edh__ubdv = bodo.libs.array_kernels.duplicated((bwyqp__nfh,))
        return edh__ubdv
    return impl


@overload_method(RangeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(NumericIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(StringIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(BinaryIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(CategoricalIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(PeriodIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
def overload_index_drop_duplicates(I, keep='first'):
    eeyru__wzx = dict(keep=keep)
    vbgry__awyk = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', eeyru__wzx, vbgry__awyk,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    wbuij__fhyx = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        wbuij__fhyx += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        wbuij__fhyx += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'bodo': bodo}, oaywh__eyyff)
    impl = oaywh__eyyff['impl']
    return impl


@numba.generated_jit(nopython=True)
def get_index_data(S):
    return lambda S: S._data


@numba.generated_jit(nopython=True)
def get_index_name(S):
    return lambda S: S._name


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_index_data',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_datetime_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_timedelta_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_numeric_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_binary_str_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_categorical_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func


def get_index_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    kyhwe__oomu = args[0]
    if isinstance(self.typemap[kyhwe__oomu.name], (HeterogeneousIndexType,
        MultiIndexType)):
        return None
    if equiv_set.has_shape(kyhwe__oomu):
        return ArrayAnalysis.AnalyzeResult(shape=kyhwe__oomu, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_get_index_data
    ) = get_index_data_equiv


@overload_method(RangeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(NumericIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(StringIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(BinaryIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(CategoricalIndexType, 'map', inline='always', no_unliteral
    =True)
@overload_method(PeriodIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(DatetimeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'map', inline='always', no_unliteral=True)
def overload_index_map(I, mapper, na_action=None):
    if not is_const_func_type(mapper):
        raise BodoError("Index.map(): 'mapper' should be a function")
    eeyru__wzx = dict(na_action=na_action)
    ynj__dpob = dict(na_action=None)
    check_unsupported_args('Index.map', eeyru__wzx, ynj__dpob, package_name
        ='pandas', module_name='Index')
    dtype = I.dtype
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.map')
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    kby__mdnsw = numba.core.registry.cpu_target.typing_context
    vao__wpm = numba.core.registry.cpu_target.target_context
    try:
        okdi__ewh = get_const_func_output_type(mapper, (dtype,), {},
            kby__mdnsw, vao__wpm)
    except Exception as mqa__ffyo:
        raise_bodo_error(get_udf_error_msg('Index.map()', mqa__ffyo))
    efw__lloc = get_udf_out_arr_type(okdi__ewh)
    func = get_overload_const_func(mapper, None)
    wbuij__fhyx = 'def f(I, mapper, na_action=None):\n'
    wbuij__fhyx += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    wbuij__fhyx += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    wbuij__fhyx += '  numba.parfors.parfor.init_prange()\n'
    wbuij__fhyx += '  n = len(A)\n'
    wbuij__fhyx += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    wbuij__fhyx += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    wbuij__fhyx += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    wbuij__fhyx += '    v = map_func(t2)\n'
    wbuij__fhyx += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    wbuij__fhyx += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    azkp__arng = bodo.compiler.udf_jit(func)
    oaywh__eyyff = {}
    exec(wbuij__fhyx, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': azkp__arng, '_arr_typ': efw__lloc, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'data_arr_type': efw__lloc.dtype},
        oaywh__eyyff)
    f = oaywh__eyyff['f']
    return f


@lower_builtin(operator.is_, NumericIndexType, NumericIndexType)
@lower_builtin(operator.is_, StringIndexType, StringIndexType)
@lower_builtin(operator.is_, BinaryIndexType, BinaryIndexType)
@lower_builtin(operator.is_, PeriodIndexType, PeriodIndexType)
@lower_builtin(operator.is_, DatetimeIndexType, DatetimeIndexType)
@lower_builtin(operator.is_, TimedeltaIndexType, TimedeltaIndexType)
@lower_builtin(operator.is_, IntervalIndexType, IntervalIndexType)
@lower_builtin(operator.is_, CategoricalIndexType, CategoricalIndexType)
def index_is(context, builder, sig, args):
    tsumk__wumtr, gdbl__luhv = sig.args
    if tsumk__wumtr != gdbl__luhv:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    tsumk__wumtr, gdbl__luhv = sig.args
    if tsumk__wumtr != gdbl__luhv:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            wbuij__fhyx = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(lhs)
"""
            if rhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                wbuij__fhyx += """  dt = bodo.utils.conversion.unbox_if_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                wbuij__fhyx += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            oaywh__eyyff = {}
            exec(wbuij__fhyx, {'bodo': bodo, 'op': op}, oaywh__eyyff)
            impl = oaywh__eyyff['impl']
            return impl
        if is_index_type(rhs):
            wbuij__fhyx = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(rhs)
"""
            if lhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                wbuij__fhyx += """  dt = bodo.utils.conversion.unbox_if_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                wbuij__fhyx += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            oaywh__eyyff = {}
            exec(wbuij__fhyx, {'bodo': bodo, 'op': op}, oaywh__eyyff)
            impl = oaywh__eyyff['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    bwyqp__nfh = bodo.utils.conversion.coerce_to_array(data)
                    zctkq__ebo = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    edh__ubdv = op(bwyqp__nfh, zctkq__ebo)
                    return edh__ubdv
                return impl3
            count = len(lhs.data.types)
            wbuij__fhyx = 'def f(lhs, rhs):\n'
            wbuij__fhyx += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            oaywh__eyyff = {}
            exec(wbuij__fhyx, {'op': op, 'np': np}, oaywh__eyyff)
            impl = oaywh__eyyff['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    bwyqp__nfh = bodo.utils.conversion.coerce_to_array(data)
                    zctkq__ebo = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    edh__ubdv = op(zctkq__ebo, bwyqp__nfh)
                    return edh__ubdv
                return impl4
            count = len(rhs.data.types)
            wbuij__fhyx = 'def f(lhs, rhs):\n'
            wbuij__fhyx += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            oaywh__eyyff = {}
            exec(wbuij__fhyx, {'op': op, 'np': np}, oaywh__eyyff)
            impl = oaywh__eyyff['f']
            return impl
    return overload_index_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        overload_impl = create_binary_op_overload(op)
        overload(op, inline='always')(overload_impl)


_install_binary_ops()


def is_index_type(t):
    return isinstance(t, (RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, PeriodIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType))


@lower_cast(RangeIndexType, NumericIndexType)
def cast_range_index_to_int_index(context, builder, fromty, toty, val):
    f = lambda I: init_numeric_index(np.arange(I._start, I._stop, I._step),
        bodo.hiframes.pd_index_ext.get_index_name(I))
    return context.compile_internal(builder, f, toty(fromty), [val])


class HeterogeneousIndexType(types.Type):
    ndim = 1

    def __init__(self, data=None, name_typ=None):
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        super(HeterogeneousIndexType, self).__init__(name=
            f'heter_index({data}, {name_typ})')

    def copy(self):
        return HeterogeneousIndexType(self.data, self.name_typ)

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return 'object'


@register_model(HeterogeneousIndexType)
class HeterogeneousIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpt__uwhnk = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, wpt__uwhnk)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    fhcn__sxtk = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    jneq__nhwyn = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', jneq__nhwyn, idx_cpy_arg_defaults,
        fn_str=fhcn__sxtk, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(HeterogeneousIndexType)
def box_heter_index(typ, val, c):
    ltzos__znxd = c.context.insert_const_string(c.builder.module, 'pandas')
    jocn__reed = c.pyapi.import_module_noblock(ltzos__znxd)
    ffqk__lrnkp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, ffqk__lrnkp.data)
    cixr__oftn = c.pyapi.from_native_value(typ.data, ffqk__lrnkp.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ffqk__lrnkp.name)
    zvwf__qqeeu = c.pyapi.from_native_value(typ.name_typ, ffqk__lrnkp.name,
        c.env_manager)
    dug__aodbt = c.pyapi.make_none()
    clbb__vbu = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    tvrl__ozzux = c.pyapi.call_method(jocn__reed, 'Index', (cixr__oftn,
        dug__aodbt, clbb__vbu, zvwf__qqeeu))
    c.pyapi.decref(cixr__oftn)
    c.pyapi.decref(dug__aodbt)
    c.pyapi.decref(clbb__vbu)
    c.pyapi.decref(zvwf__qqeeu)
    c.pyapi.decref(jocn__reed)
    c.context.nrt.decref(c.builder, typ, val)
    return tvrl__ozzux


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        qdjg__gmai = signature.return_type
        ffqk__lrnkp = cgutils.create_struct_proxy(qdjg__gmai)(context, builder)
        ffqk__lrnkp.data = args[0]
        ffqk__lrnkp.name = args[1]
        context.nrt.incref(builder, qdjg__gmai.data, args[0])
        context.nrt.incref(builder, qdjg__gmai.name_typ, args[1])
        return ffqk__lrnkp._getvalue()
    return HeterogeneousIndexType(data, name)(data, name), codegen


@overload_attribute(HeterogeneousIndexType, 'name')
def heter_index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload_attribute(NumericIndexType, 'nbytes')
@overload_attribute(DatetimeIndexType, 'nbytes')
@overload_attribute(TimedeltaIndexType, 'nbytes')
@overload_attribute(RangeIndexType, 'nbytes')
@overload_attribute(StringIndexType, 'nbytes')
@overload_attribute(BinaryIndexType, 'nbytes')
@overload_attribute(CategoricalIndexType, 'nbytes')
@overload_attribute(PeriodIndexType, 'nbytes')
def overload_nbytes(I):
    if isinstance(I, RangeIndexType):

        def _impl_nbytes(I):
            return bodo.io.np_io.get_dtype_size(type(I._start)
                ) + bodo.io.np_io.get_dtype_size(type(I._step)
                ) + bodo.io.np_io.get_dtype_size(type(I._stop))
        return _impl_nbytes
    else:

        def _impl_nbytes(I):
            return I._data.nbytes
        return _impl_nbytes


@overload_method(NumericIndexType, 'rename', inline='always')
@overload_method(DatetimeIndexType, 'rename', inline='always')
@overload_method(TimedeltaIndexType, 'rename', inline='always')
@overload_method(RangeIndexType, 'rename', inline='always')
@overload_method(StringIndexType, 'rename', inline='always')
@overload_method(BinaryIndexType, 'rename', inline='always')
@overload_method(CategoricalIndexType, 'rename', inline='always')
@overload_method(PeriodIndexType, 'rename', inline='always')
@overload_method(IntervalIndexType, 'rename', inline='always')
@overload_method(HeterogeneousIndexType, 'rename', inline='always')
def overload_rename(I, name, inplace=False):
    if is_overload_true(inplace):
        raise BodoError('Index.rename(): inplace index renaming unsupported')
    return init_index_from_index(I, name)


def init_index_from_index(I, name):
    obst__kpga = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in obst__kpga:
        init_func = obst__kpga[type(I)]
        return lambda I, name, inplace=False: init_func(bodo.hiframes.
            pd_index_ext.get_index_data(I).copy(), name)
    if isinstance(I, RangeIndexType):
        return lambda I, name, inplace=False: I.copy(name=name)
    if isinstance(I, PeriodIndexType):
        freq = I.freq
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_period_index(bodo.hiframes.pd_index_ext.get_index_data(I).
            copy(), name, freq))
    if isinstance(I, HeterogeneousIndexType):
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_heter_index(bodo.hiframes.pd_index_ext.get_index_data(I),
            name))
    raise_bodo_error(f'init_index(): Unknown type {type(I)}')


def get_index_constructor(I):
    ciku__zdjw = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index, RangeIndexType: bodo.
        hiframes.pd_index_ext.init_range_index}
    if type(I) in ciku__zdjw:
        return ciku__zdjw[type(I)]
    raise BodoError(
        f'Unsupported type for standard Index constructor: {type(I)}')


@overload_method(NumericIndexType, 'unique', no_unliteral=True, inline='always'
    )
@overload_method(BinaryIndexType, 'unique', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'unique', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(IntervalIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(DatetimeIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'unique', no_unliteral=True, inline=
    'always')
def overload_index_unique(I):
    lsq__czc = get_index_constructor(I)

    def impl(I):
        bwyqp__nfh = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        yzyj__cukep = bodo.libs.array_kernels.unique(bwyqp__nfh)
        return lsq__czc(yzyj__cukep, name)
    return impl


@overload_method(RangeIndexType, 'unique', no_unliteral=True)
def overload_range_index_unique(I):

    def impl(I):
        return I.copy()
    return impl


@overload_method(NumericIndexType, 'nunique', inline='always')
@overload_method(BinaryIndexType, 'nunique', inline='always')
@overload_method(StringIndexType, 'nunique', inline='always')
@overload_method(CategoricalIndexType, 'nunique', inline='always')
@overload_method(DatetimeIndexType, 'nunique', inline='always')
@overload_method(TimedeltaIndexType, 'nunique', inline='always')
@overload_method(PeriodIndexType, 'nunique', inline='always')
def overload_index_nunique(I, dropna=True):

    def impl(I, dropna=True):
        bwyqp__nfh = bodo.hiframes.pd_index_ext.get_index_data(I)
        mbby__numqz = bodo.libs.array_kernels.nunique(bwyqp__nfh, dropna)
        return mbby__numqz
    return impl


@overload_method(RangeIndexType, 'nunique', inline='always')
def overload_range_index_nunique(I, dropna=True):

    def impl(I, dropna=True):
        start = I._start
        stop = I._stop
        step = I._step
        return max(0, -(-(stop - start) // step))
    return impl


@overload_method(NumericIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(TimedeltaIndexType, 'isin', no_unliteral=True, inline='always'
    )
def overload_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            cnn__wjuw = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_index_ext.get_index_data(I)
            mbby__numqz = len(A)
            edh__ubdv = np.empty(mbby__numqz, np.bool_)
            bodo.libs.array.array_isin(edh__ubdv, A, cnn__wjuw, False)
            return edh__ubdv
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        edh__ubdv = bodo.libs.array_ops.array_op_isin(A, values)
        return edh__ubdv
    return impl


@overload_method(RangeIndexType, 'isin', no_unliteral=True)
def overload_range_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            cnn__wjuw = bodo.utils.conversion.coerce_to_array(values)
            A = np.arange(I.start, I.stop, I.step)
            mbby__numqz = len(A)
            edh__ubdv = np.empty(mbby__numqz, np.bool_)
            bodo.libs.array.array_isin(edh__ubdv, A, cnn__wjuw, False)
            return edh__ubdv
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Index.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = np.arange(I.start, I.stop, I.step)
        edh__ubdv = bodo.libs.array_ops.array_op_isin(A, values)
        return edh__ubdv
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_heter_index_getitem(I, ind):
    if not isinstance(I, HeterogeneousIndexType):
        return
    if isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, HeterogeneousIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_heter_index(bodo
            .hiframes.pd_index_ext.get_index_data(I)[ind], bodo.hiframes.
            pd_index_ext.get_index_name(I))


@lower_constant(DatetimeIndexType)
@lower_constant(TimedeltaIndexType)
def lower_constant_time_index(context, builder, ty, pyval):
    if isinstance(ty.data, bodo.DatetimeArrayType):
        data = context.get_constant_generic(builder, ty.data, pyval.array)
    else:
        data = context.get_constant_generic(builder, types.Array(types.
            int64, 1, 'C'), pyval.values.view(np.int64))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    azbu__redo = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, azbu__redo])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    azbu__redo = context.get_constant_null(types.DictType(types.int64,
        types.int64))
    return lir.Constant.literal_struct([data, name, azbu__redo])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    azbu__redo = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, azbu__redo])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    mejk__qec = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, mejk__qec, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    azbu__redo = context.get_constant_null(types.DictType(scalar_type,
        types.int64))
    return lir.Constant.literal_struct([data, name, azbu__redo])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [qmcvm__dlcb] = sig.args
    [hyft__ohaq] = args
    ozp__gqz = context.make_helper(builder, qmcvm__dlcb, value=hyft__ohaq)
    vmyp__dgt = context.make_helper(builder, sig.return_type)
    dlxid__cosbp = cgutils.alloca_once_value(builder, ozp__gqz.start)
    vzbo__htknr = context.get_constant(types.intp, 0)
    erc__hmiv = cgutils.alloca_once_value(builder, vzbo__htknr)
    vmyp__dgt.iter = dlxid__cosbp
    vmyp__dgt.stop = ozp__gqz.stop
    vmyp__dgt.step = ozp__gqz.step
    vmyp__dgt.count = erc__hmiv
    wljk__hpo = builder.sub(ozp__gqz.stop, ozp__gqz.start)
    opn__ohl = context.get_constant(types.intp, 1)
    npns__keapv = builder.icmp_signed('>', wljk__hpo, vzbo__htknr)
    bcjmy__plxuw = builder.icmp_signed('>', ozp__gqz.step, vzbo__htknr)
    yskop__zwa = builder.not_(builder.xor(npns__keapv, bcjmy__plxuw))
    with builder.if_then(yskop__zwa):
        apuah__cdnf = builder.srem(wljk__hpo, ozp__gqz.step)
        apuah__cdnf = builder.select(npns__keapv, apuah__cdnf, builder.neg(
            apuah__cdnf))
        ipge__xjatt = builder.icmp_signed('>', apuah__cdnf, vzbo__htknr)
        ylmu__ocd = builder.add(builder.sdiv(wljk__hpo, ozp__gqz.step),
            builder.select(ipge__xjatt, opn__ohl, vzbo__htknr))
        builder.store(ylmu__ocd, erc__hmiv)
    mzp__nxaw = vmyp__dgt._getvalue()
    qiai__zifnu = impl_ret_new_ref(context, builder, sig.return_type, mzp__nxaw
        )
    return qiai__zifnu


def _install_index_getiter():
    index_types = [NumericIndexType, StringIndexType, BinaryIndexType,
        CategoricalIndexType, TimedeltaIndexType, DatetimeIndexType]
    for typ in index_types:
        lower_builtin('getiter', typ)(numba.np.arrayobj.getiter_array)


_install_index_getiter()
index_unsupported_methods = ['all', 'any', 'append', 'argmax', 'argmin',
    'argsort', 'asof', 'asof_locs', 'astype', 'delete', 'difference',
    'drop', 'droplevel', 'dropna', 'equals', 'factorize', 'fillna',
    'format', 'get_indexer', 'get_indexer_for', 'get_indexer_non_unique',
    'get_level_values', 'get_slice_bound', 'get_value', 'groupby',
    'holds_integer', 'identical', 'insert', 'intersection', 'is_',
    'is_boolean', 'is_categorical', 'is_floating', 'is_integer',
    'is_interval', 'is_mixed', 'is_numeric', 'is_object',
    'is_type_compatible', 'item', 'join', 'memory_usage', 'putmask',
    'ravel', 'reindex', 'repeat', 'searchsorted', 'set_names', 'set_value',
    'shift', 'slice_indexer', 'slice_locs', 'sort', 'sort_values',
    'sortlevel', 'str', 'symmetric_difference', 'to_flat_index', 'to_frame',
    'to_list', 'to_native_types', 'to_numpy', 'to_series', 'tolist',
    'transpose', 'union', 'value_counts', 'view', 'where']
index_unsupported_atrs = ['T', 'array', 'asi8', 'dtype', 'has_duplicates',
    'hasnans', 'inferred_type', 'is_all_dates', 'is_unique', 'ndim',
    'nlevels', 'size', 'names', 'empty']
cat_idx_unsupported_atrs = ['codes', 'categories', 'ordered',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing']
cat_idx_unsupported_methods = ['rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered', 'get_loc', 'isin']
interval_idx_unsupported_atrs = ['closed', 'is_empty',
    'is_non_overlapping_monotonic', 'is_overlapping', 'left', 'right',
    'mid', 'length', 'values', 'shape', 'nbytes', 'is_monotonic',
    'is_monotonic_increasing', 'is_monotonic_decreasing']
interval_idx_unsupported_methods = ['contains', 'copy', 'overlaps',
    'set_closed', 'to_tuples', 'take', 'get_loc', 'isna', 'isnull', 'map',
    'isin', 'nunique']
multi_index_unsupported_atrs = ['levshape', 'levels', 'codes', 'dtypes',
    'values', 'shape', 'nbytes', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
multi_index_unsupported_methods = ['copy', 'set_levels', 'set_codes',
    'swaplevel', 'reorder_levels', 'remove_unused_levels', 'get_loc',
    'get_locs', 'get_loc_level', 'take', 'isna', 'isnull', 'map', 'isin',
    'unique', 'nunique']
dt_index_unsupported_atrs = ['time', 'timez', 'tz', 'freq', 'freqstr',
    'inferred_freq']
dt_index_unsupported_methods = ['normalize', 'strftime', 'snap',
    'tz_localize', 'round', 'floor', 'ceil', 'to_period', 'to_perioddelta',
    'to_pydatetime', 'month_name', 'day_name', 'mean', 'indexer_at_time',
    'indexer_between', 'indexer_between_time']
td_index_unsupported_atrs = ['components', 'inferred_freq']
td_index_unsupported_methods = ['to_pydatetime', 'round', 'floor', 'ceil',
    'mean']
period_index_unsupported_atrs = ['day', 'dayofweek', 'day_of_week',
    'dayofyear', 'day_of_year', 'days_in_month', 'daysinmonth', 'freq',
    'freqstr', 'hour', 'is_leap_year', 'minute', 'month', 'quarter',
    'second', 'week', 'weekday', 'weekofyear', 'year', 'end_time', 'qyear',
    'start_time', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
period_index_unsupported_methods = ['asfreq', 'strftime', 'to_timestamp',
    'isin', 'unique']
string_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
binary_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
index_types = [('pandas.RangeIndex.{}', RangeIndexType), (
    'pandas.Index.{} with numeric data', NumericIndexType), (
    'pandas.Index.{} with string data', StringIndexType), (
    'pandas.Index.{} with binary data', BinaryIndexType), (
    'pandas.TimedeltaIndex.{}', TimedeltaIndexType), (
    'pandas.IntervalIndex.{}', IntervalIndexType), (
    'pandas.CategoricalIndex.{}', CategoricalIndexType), (
    'pandas.PeriodIndex.{}', PeriodIndexType), ('pandas.DatetimeIndex.{}',
    DatetimeIndexType), ('pandas.MultiIndex.{}', MultiIndexType)]
for name, typ in index_types:
    idx_typ_to_format_str_map[typ] = name


def _install_index_unsupported():
    for euxdd__mfyb in index_unsupported_methods:
        for lqs__bpz, typ in index_types:
            overload_method(typ, euxdd__mfyb, no_unliteral=True)(
                create_unsupported_overload(lqs__bpz.format(euxdd__mfyb +
                '()')))
    for jlo__ybg in index_unsupported_atrs:
        for lqs__bpz, typ in index_types:
            overload_attribute(typ, jlo__ybg, no_unliteral=True)(
                create_unsupported_overload(lqs__bpz.format(jlo__ybg)))
    efs__jqzwu = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    lkccw__pyux = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods)]
    for typ, wpj__ucq in lkccw__pyux:
        lqs__bpz = idx_typ_to_format_str_map[typ]
        for rdyvx__xatn in wpj__ucq:
            overload_method(typ, rdyvx__xatn, no_unliteral=True)(
                create_unsupported_overload(lqs__bpz.format(rdyvx__xatn +
                '()')))
    for typ, agene__rcc in efs__jqzwu:
        lqs__bpz = idx_typ_to_format_str_map[typ]
        for jlo__ybg in agene__rcc:
            overload_attribute(typ, jlo__ybg, no_unliteral=True)(
                create_unsupported_overload(lqs__bpz.format(jlo__ybg)))
    for txq__aoke in [RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, MultiIndexType]:
        for rdyvx__xatn in ['max', 'min']:
            lqs__bpz = idx_typ_to_format_str_map[txq__aoke]
            overload_method(txq__aoke, rdyvx__xatn, no_unliteral=True)(
                create_unsupported_overload(lqs__bpz.format(rdyvx__xatn +
                '()')))


_install_index_unsupported()
