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
            snrlk__xae = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(snrlk__xae)
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
        bzo__qzpkr = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    nem__hmnz = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', hpx__dpg, idx_cpy_arg_defaults, fn_str=
        nem__hmnz, package_name='pandas', module_name='Index')
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
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ktwrz__zzju = c.pyapi.import_module_noblock(ufojv__fhqp)
    apuky__eiup = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, apuky__eiup.data)
    ugccd__nml = c.pyapi.from_native_value(typ.data, apuky__eiup.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, apuky__eiup.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, apuky__eiup.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([ugccd__nml])
    grqv__thki = c.pyapi.object_getattr_string(ktwrz__zzju, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', jjyoa__kjnee)])
    irsf__orxb = c.pyapi.call(grqv__thki, args, kws)
    c.pyapi.decref(ugccd__nml)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(ktwrz__zzju)
    c.pyapi.decref(grqv__thki)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return irsf__orxb


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        eum__wxt = c.pyapi.object_getattr_string(val, 'array')
    else:
        eum__wxt = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, eum__wxt).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    dtype = _dt_index_data_typ.dtype
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ahqug__bbzs.dict = nzzun__qhex
    c.pyapi.decref(eum__wxt)
    c.pyapi.decref(jjyoa__kjnee)
    return NativeValue(ahqug__bbzs._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        zfcqi__kuq, srk__evz = args
        apuky__eiup = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        apuky__eiup.data = zfcqi__kuq
        apuky__eiup.name = srk__evz
        context.nrt.incref(builder, signature.args[0], zfcqi__kuq)
        context.nrt.incref(builder, signature.args[1], srk__evz)
        dtype = _dt_index_data_typ.dtype
        apuky__eiup.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return apuky__eiup._getvalue()
    aif__uaus = DatetimeIndexType(name, data)
    sig = signature(aif__uaus, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    xvx__blgk = args[0]
    if equiv_set.has_shape(xvx__blgk):
        return ArrayAnalysis.AnalyzeResult(shape=xvx__blgk, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    alyze__jib = 'def impl(dti):\n'
    alyze__jib += '    numba.parfors.parfor.init_prange()\n'
    alyze__jib += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    alyze__jib += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    alyze__jib += '    n = len(A)\n'
    alyze__jib += '    S = np.empty(n, np.int64)\n'
    alyze__jib += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    alyze__jib += '        val = A[i]\n'
    alyze__jib += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        alyze__jib += '        S[i] = ts.' + field + '()\n'
    else:
        alyze__jib += '        S[i] = ts.' + field + '\n'
    alyze__jib += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    bfv__oyd = {}
    exec(alyze__jib, {'numba': numba, 'np': np, 'bodo': bodo}, bfv__oyd)
    impl = bfv__oyd['impl']
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
        sbr__vwdhg = len(A)
        S = np.empty(sbr__vwdhg, np.bool_)
        for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
            val = A[i]
            veuq__fwyw = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(veuq__fwyw.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        sbr__vwdhg = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            sbr__vwdhg)
        for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
            val = A[i]
            veuq__fwyw = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(veuq__fwyw.year, veuq__fwyw.month,
                veuq__fwyw.day)
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
    uph__vtx = dict(axis=axis, skipna=skipna)
    rivf__tcn = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        augyh__xes = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(augyh__xes)):
            if not bodo.libs.array_kernels.isna(augyh__xes, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(augyh__xes
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    uph__vtx = dict(axis=axis, skipna=skipna)
    rivf__tcn = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        augyh__xes = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(augyh__xes)):
            if not bodo.libs.array_kernels.isna(augyh__xes, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(augyh__xes
                    [i])
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
    uph__vtx = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    rivf__tcn = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        naaqi__jez = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(naaqi__jez)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        cyhb__onqje = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            augyh__xes = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            sbr__vwdhg = len(augyh__xes)
            S = np.empty(sbr__vwdhg, cyhb__onqje)
            gigkk__gkwsa = rhs.value
            for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    augyh__xes[i]) - gigkk__gkwsa)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        cyhb__onqje = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            augyh__xes = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            sbr__vwdhg = len(augyh__xes)
            S = np.empty(sbr__vwdhg, cyhb__onqje)
            gigkk__gkwsa = lhs.value
            for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    gigkk__gkwsa - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(augyh__xes[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    qzhv__fkvht = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    alyze__jib = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        alyze__jib += '  dt_index, _str = lhs, rhs\n'
        ams__ulwqq = 'arr[i] {} other'.format(qzhv__fkvht)
    else:
        alyze__jib += '  dt_index, _str = rhs, lhs\n'
        ams__ulwqq = 'other {} arr[i]'.format(qzhv__fkvht)
    alyze__jib += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    alyze__jib += '  l = len(arr)\n'
    alyze__jib += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    alyze__jib += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    alyze__jib += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    alyze__jib += '    S[i] = {}\n'.format(ams__ulwqq)
    alyze__jib += '  return S\n'
    bfv__oyd = {}
    exec(alyze__jib, {'bodo': bodo, 'numba': numba, 'np': np}, bfv__oyd)
    impl = bfv__oyd['impl']
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
    fhha__exw = getattr(data, 'dtype', None)
    if not is_overload_none(dtype):
        tuq__qljhc = parse_dtype(dtype, 'pandas.Index')
    else:
        tuq__qljhc = fhha__exw
    if isinstance(tuq__qljhc, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType) or tuq__qljhc == types.NPDatetime(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or tuq__qljhc == types.NPTimedelta('ns'):

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
        if isinstance(tuq__qljhc, (types.Integer, types.Float, types.Boolean)):

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                naaqi__jez = bodo.utils.conversion.coerce_to_array(data)
                cydzt__xmex = bodo.utils.conversion.fix_arr_dtype(naaqi__jez,
                    tuq__qljhc)
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    cydzt__xmex, name)
        elif tuq__qljhc in [types.string, bytes_type]:

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
                ydi__ojul = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = ydi__ojul[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                ydi__ojul = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                cqtm__bkg = ydi__ojul[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(cqtm__bkg
                    , name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            ybqar__zfm = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(ybqar__zfm[ind])
        return impl

    def impl(I, ind):
        ybqar__zfm = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        cqtm__bkg = ybqar__zfm[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(cqtm__bkg, name)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_categorical_index_getitem(I, ind):
    if not isinstance(I, CategoricalIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            hwew__kbgf = bodo.hiframes.pd_index_ext.get_index_data(I)
            val = hwew__kbgf[ind]
            return val
        return impl
    if isinstance(ind, types.SliceType):

        def impl(I, ind):
            hwew__kbgf = bodo.hiframes.pd_index_ext.get_index_data(I)
            name = bodo.hiframes.pd_index_ext.get_index_name(I)
            cqtm__bkg = hwew__kbgf[ind]
            return bodo.hiframes.pd_index_ext.init_categorical_index(cqtm__bkg,
                name)
        return impl
    raise BodoError(
        f'pd.CategoricalIndex.__getitem__: unsupported index type {ind}')


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    fmlv__vzs = False
    tsz__ycw = False
    if closed is None:
        fmlv__vzs = True
        tsz__ycw = True
    elif closed == 'left':
        fmlv__vzs = True
    elif closed == 'right':
        tsz__ycw = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return fmlv__vzs, tsz__ycw


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
    uph__vtx = dict(tz=tz, normalize=normalize, closed=closed)
    rivf__tcn = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    scgb__wkg = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        scgb__wkg = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    alyze__jib = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    alyze__jib += scgb__wkg
    if is_overload_none(start):
        alyze__jib += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        alyze__jib += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        alyze__jib += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        alyze__jib += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        alyze__jib += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            alyze__jib += '  b = start_t.value\n'
            alyze__jib += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            alyze__jib += '  b = start_t.value\n'
            alyze__jib += '  addend = np.int64(periods) * np.int64(stride)\n'
            alyze__jib += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            alyze__jib += '  e = end_t.value + stride\n'
            alyze__jib += '  addend = np.int64(periods) * np.int64(-stride)\n'
            alyze__jib += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        alyze__jib += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        alyze__jib += '  delta = end_t.value - start_t.value\n'
        alyze__jib += '  step = delta / (periods - 1)\n'
        alyze__jib += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        alyze__jib += '  arr1 *= step\n'
        alyze__jib += '  arr1 += start_t.value\n'
        alyze__jib += '  arr = arr1.astype(np.int64)\n'
        alyze__jib += '  arr[-1] = end_t.value\n'
    alyze__jib += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    alyze__jib += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    bfv__oyd = {}
    exec(alyze__jib, {'bodo': bodo, 'np': np, 'pd': pd}, bfv__oyd)
    f = bfv__oyd['f']
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
        nmar__bao = pd.Timedelta('1 day')
        if start is not None:
            nmar__bao = pd.Timedelta(start)
        jlugs__rejap = pd.Timedelta('1 day')
        if end is not None:
            jlugs__rejap = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        fmlv__vzs, tsz__ycw = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            clrs__teu = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = nmar__bao.value
                fst__gdhyv = b + (jlugs__rejap.value - b
                    ) // clrs__teu * clrs__teu + clrs__teu // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = nmar__bao.value
                ugkkv__uwd = np.int64(periods) * np.int64(clrs__teu)
                fst__gdhyv = np.int64(b) + ugkkv__uwd
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                fst__gdhyv = jlugs__rejap.value + clrs__teu
                ugkkv__uwd = np.int64(periods) * np.int64(-clrs__teu)
                b = np.int64(fst__gdhyv) + ugkkv__uwd
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            aedc__tjx = np.arange(b, fst__gdhyv, clrs__teu, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            zkrv__mznb = jlugs__rejap.value - nmar__bao.value
            step = zkrv__mznb / (periods - 1)
            ttiu__anw = np.arange(0, periods, 1, np.float64)
            ttiu__anw *= step
            ttiu__anw += nmar__bao.value
            aedc__tjx = ttiu__anw.astype(np.int64)
            aedc__tjx[-1] = jlugs__rejap.value
        if not fmlv__vzs and len(aedc__tjx) and aedc__tjx[0
            ] == nmar__bao.value:
            aedc__tjx = aedc__tjx[1:]
        if not tsz__ycw and len(aedc__tjx) and aedc__tjx[-1
            ] == jlugs__rejap.value:
            aedc__tjx = aedc__tjx[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(aedc__tjx)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        sbr__vwdhg = len(A)
        qvrdl__ttgyw = bodo.libs.int_arr_ext.alloc_int_array(sbr__vwdhg, np
            .uint32)
        qqlf__iang = bodo.libs.int_arr_ext.alloc_int_array(sbr__vwdhg, np.
            uint32)
        jrv__ngzu = bodo.libs.int_arr_ext.alloc_int_array(sbr__vwdhg, np.uint32
            )
        for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(qvrdl__ttgyw, i)
                bodo.libs.array_kernels.setna(qqlf__iang, i)
                bodo.libs.array_kernels.setna(jrv__ngzu, i)
                continue
            qvrdl__ttgyw[i], qqlf__iang[i], jrv__ngzu[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((qvrdl__ttgyw,
            qqlf__iang, jrv__ngzu), idx, ('year', 'week', 'day'))
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
        bzo__qzpkr = [('data', _timedelta_index_data_typ), ('name', fe_type
            .name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, bzo__qzpkr)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ktwrz__zzju = c.pyapi.import_module_noblock(ufojv__fhqp)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    ugccd__nml = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([ugccd__nml])
    kws = c.pyapi.dict_pack([('name', jjyoa__kjnee)])
    grqv__thki = c.pyapi.object_getattr_string(ktwrz__zzju, 'TimedeltaIndex')
    irsf__orxb = c.pyapi.call(grqv__thki, args, kws)
    c.pyapi.decref(ugccd__nml)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(ktwrz__zzju)
    c.pyapi.decref(grqv__thki)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return irsf__orxb


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    jnbpg__wzzj = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, jnbpg__wzzj
        ).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    c.pyapi.decref(jnbpg__wzzj)
    c.pyapi.decref(jjyoa__kjnee)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    dtype = _timedelta_index_data_typ.dtype
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ahqug__bbzs.dict = nzzun__qhex
    return NativeValue(ahqug__bbzs._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        zfcqi__kuq, srk__evz = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = zfcqi__kuq
        timedelta_index.name = srk__evz
        context.nrt.incref(builder, signature.args[0], zfcqi__kuq)
        context.nrt.incref(builder, signature.args[1], srk__evz)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    aif__uaus = TimedeltaIndexType(name)
    sig = signature(aif__uaus, data, name)
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
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    nem__hmnz = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()')
    check_unsupported_args('TimedeltaIndex.copy', hpx__dpg,
        idx_cpy_arg_defaults, fn_str=nem__hmnz, package_name='pandas',
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
    uph__vtx = dict(axis=axis, skipna=skipna)
    rivf__tcn = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        sbr__vwdhg = len(data)
        jac__nhtzn = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            jac__nhtzn = min(jac__nhtzn, val)
        bopdb__hwdr = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            jac__nhtzn)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(bopdb__hwdr, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    uph__vtx = dict(axis=axis, skipna=skipna)
    rivf__tcn = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        sbr__vwdhg = len(data)
        elgz__tko = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            elgz__tko = max(elgz__tko, val)
        bopdb__hwdr = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            elgz__tko)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(bopdb__hwdr, count)
    return impl


def gen_tdi_field_impl(field):
    alyze__jib = 'def impl(tdi):\n'
    alyze__jib += '    numba.parfors.parfor.init_prange()\n'
    alyze__jib += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    alyze__jib += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    alyze__jib += '    n = len(A)\n'
    alyze__jib += '    S = np.empty(n, np.int64)\n'
    alyze__jib += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    alyze__jib += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        alyze__jib += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        alyze__jib += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        alyze__jib += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        alyze__jib += (
            '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
    else:
        assert False, 'invalid timedelta field'
    alyze__jib += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    bfv__oyd = {}
    exec(alyze__jib, {'numba': numba, 'np': np, 'bodo': bodo}, bfv__oyd)
    impl = bfv__oyd['impl']
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
    uph__vtx = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    rivf__tcn = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        naaqi__jez = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(naaqi__jez)
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
        bzo__qzpkr = [('start', types.int64), ('stop', types.int64), (
            'step', types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    nem__hmnz = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', hpx__dpg,
        idx_cpy_arg_defaults, fn_str=nem__hmnz, package_name='pandas',
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
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    moi__muqv = c.pyapi.import_module_noblock(ufojv__fhqp)
    duw__ajk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    cci__zxiy = c.pyapi.from_native_value(types.int64, duw__ajk.start, c.
        env_manager)
    mlkzz__gkji = c.pyapi.from_native_value(types.int64, duw__ajk.stop, c.
        env_manager)
    vcm__znv = c.pyapi.from_native_value(types.int64, duw__ajk.step, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, duw__ajk.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, duw__ajk.name, c
        .env_manager)
    args = c.pyapi.tuple_pack([cci__zxiy, mlkzz__gkji, vcm__znv])
    kws = c.pyapi.dict_pack([('name', jjyoa__kjnee)])
    grqv__thki = c.pyapi.object_getattr_string(moi__muqv, 'RangeIndex')
    fisd__ayz = c.pyapi.call(grqv__thki, args, kws)
    c.pyapi.decref(cci__zxiy)
    c.pyapi.decref(mlkzz__gkji)
    c.pyapi.decref(vcm__znv)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(moi__muqv)
    c.pyapi.decref(grqv__thki)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return fisd__ayz


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name
    skzk__bqm = is_overload_constant_int(step) and get_overload_const_int(step
        ) == 0

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        if skzk__bqm:
            raise_bodo_error('Step must not be zero')
        pxozi__smo = cgutils.is_scalar_zero(builder, args[2])
        zyxrg__ite = context.get_python_api(builder)
        with builder.if_then(pxozi__smo):
            zyxrg__ite.err_format('PyExc_ValueError', 'Step must not be zero')
            val = context.get_constant(types.int32, -1)
            builder.ret(val)
        duw__ajk = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        duw__ajk.start = args[0]
        duw__ajk.stop = args[1]
        duw__ajk.step = args[2]
        duw__ajk.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return duw__ajk._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, awxlf__fli = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    cci__zxiy = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, cci__zxiy).value
    mlkzz__gkji = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, mlkzz__gkji).value
    vcm__znv = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, vcm__znv).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    c.pyapi.decref(cci__zxiy)
    c.pyapi.decref(mlkzz__gkji)
    c.pyapi.decref(vcm__znv)
    c.pyapi.decref(jjyoa__kjnee)
    duw__ajk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    duw__ajk.start = start
    duw__ajk.stop = stop
    duw__ajk.step = step
    duw__ajk.name = name
    return NativeValue(duw__ajk._getvalue())


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
        ttni__oydqy = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(ttni__oydqy.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        ttni__oydqy = 'RangeIndex(...) must be called with integers'
        raise BodoError(ttni__oydqy)
    ntce__xti = 'start'
    ahr__zdyuo = 'stop'
    nbw__gse = 'step'
    if is_overload_none(start):
        ntce__xti = '0'
    if is_overload_none(stop):
        ahr__zdyuo = 'start'
        ntce__xti = '0'
    if is_overload_none(step):
        nbw__gse = '1'
    alyze__jib = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    alyze__jib += '  return init_range_index({}, {}, {}, name)\n'.format(
        ntce__xti, ahr__zdyuo, nbw__gse)
    bfv__oyd = {}
    exec(alyze__jib, {'init_range_index': init_range_index}, bfv__oyd)
    ezfz__zca = bfv__oyd['_pd_range_index_imp']
    return ezfz__zca


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
                punc__cmlap = numba.cpython.unicode._normalize_slice(idx,
                    len(I))
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * punc__cmlap.start
                stop = I._start + I._step * punc__cmlap.stop
                step = I._step * punc__cmlap.step
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
        bzo__qzpkr = [('data', bodo.IntegerArrayType(types.int64)), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    nem__hmnz = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', hpx__dpg,
        idx_cpy_arg_defaults, fn_str=nem__hmnz, package_name='pandas',
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
        zfcqi__kuq, srk__evz, awxlf__fli = args
        eru__anxk = signature.return_type
        dfu__cbhl = cgutils.create_struct_proxy(eru__anxk)(context, builder)
        dfu__cbhl.data = zfcqi__kuq
        dfu__cbhl.name = srk__evz
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        dfu__cbhl.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return dfu__cbhl._getvalue()
    hlmcg__nrz = get_overload_const_str(freq)
    aif__uaus = PeriodIndexType(hlmcg__nrz, name)
    sig = signature(aif__uaus, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    moi__muqv = c.pyapi.import_module_noblock(ufojv__fhqp)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        ahqug__bbzs.data)
    eum__wxt = c.pyapi.from_native_value(bodo.IntegerArrayType(types.int64),
        ahqug__bbzs.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ahqug__bbzs.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, ahqug__bbzs.name,
        c.env_manager)
    sbcl__btdd = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', eum__wxt), ('name', jjyoa__kjnee),
        ('freq', sbcl__btdd)])
    grqv__thki = c.pyapi.object_getattr_string(moi__muqv, 'PeriodIndex')
    fisd__ayz = c.pyapi.call(grqv__thki, args, kws)
    c.pyapi.decref(eum__wxt)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(sbcl__btdd)
    c.pyapi.decref(moi__muqv)
    c.pyapi.decref(grqv__thki)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return fisd__ayz


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    inj__uacfm = c.pyapi.object_getattr_string(val, 'asi8')
    ehrje__prxs = c.pyapi.call_method(val, 'isna', ())
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ktwrz__zzju = c.pyapi.import_module_noblock(ufojv__fhqp)
    oaps__idjew = c.pyapi.object_getattr_string(ktwrz__zzju, 'arrays')
    eum__wxt = c.pyapi.call_method(oaps__idjew, 'IntegerArray', (inj__uacfm,
        ehrje__prxs))
    data = c.pyapi.to_native_value(arr_typ, eum__wxt).value
    c.pyapi.decref(inj__uacfm)
    c.pyapi.decref(ehrje__prxs)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(ktwrz__zzju)
    c.pyapi.decref(oaps__idjew)
    c.pyapi.decref(eum__wxt)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    ahqug__bbzs.dict = nzzun__qhex
    return NativeValue(ahqug__bbzs._getvalue())


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
        nsye__tok = get_categories_int_type(fe_type.data.dtype)
        bzo__qzpkr = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(nsye__tok, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type,
            bzo__qzpkr)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ktwrz__zzju = c.pyapi.import_module_noblock(ufojv__fhqp)
    lkrqu__divjx = numba.core.cgutils.create_struct_proxy(typ)(c.context, c
        .builder, val)
    c.context.nrt.incref(c.builder, typ.data, lkrqu__divjx.data)
    ugccd__nml = c.pyapi.from_native_value(typ.data, lkrqu__divjx.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, lkrqu__divjx.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, lkrqu__divjx.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([ugccd__nml])
    kws = c.pyapi.dict_pack([('name', jjyoa__kjnee)])
    grqv__thki = c.pyapi.object_getattr_string(ktwrz__zzju, 'CategoricalIndex')
    irsf__orxb = c.pyapi.call(grqv__thki, args, kws)
    c.pyapi.decref(ugccd__nml)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(ktwrz__zzju)
    c.pyapi.decref(grqv__thki)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return irsf__orxb


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    jnbpg__wzzj = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, jnbpg__wzzj).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    c.pyapi.decref(jnbpg__wzzj)
    c.pyapi.decref(jjyoa__kjnee)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ahqug__bbzs.dict = nzzun__qhex
    return NativeValue(ahqug__bbzs._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        zfcqi__kuq, srk__evz = args
        lkrqu__divjx = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        lkrqu__divjx.data = zfcqi__kuq
        lkrqu__divjx.name = srk__evz
        context.nrt.incref(builder, signature.args[0], zfcqi__kuq)
        context.nrt.incref(builder, signature.args[1], srk__evz)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        lkrqu__divjx.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return lkrqu__divjx._getvalue()
    aif__uaus = CategoricalIndexType(data, name)
    sig = signature(aif__uaus, data, name)
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
    nem__hmnz = idx_typ_to_format_str_map[CategoricalIndexType].format('copy()'
        )
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', hpx__dpg,
        idx_cpy_arg_defaults, fn_str=nem__hmnz, package_name='pandas',
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
        bzo__qzpkr = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, bzo__qzpkr)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ktwrz__zzju = c.pyapi.import_module_noblock(ufojv__fhqp)
    rfei__krw = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, rfei__krw.data)
    ugccd__nml = c.pyapi.from_native_value(typ.data, rfei__krw.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, rfei__krw.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, rfei__krw.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([ugccd__nml])
    kws = c.pyapi.dict_pack([('name', jjyoa__kjnee)])
    grqv__thki = c.pyapi.object_getattr_string(ktwrz__zzju, 'IntervalIndex')
    irsf__orxb = c.pyapi.call(grqv__thki, args, kws)
    c.pyapi.decref(ugccd__nml)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(ktwrz__zzju)
    c.pyapi.decref(grqv__thki)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return irsf__orxb


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    jnbpg__wzzj = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, jnbpg__wzzj).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    c.pyapi.decref(jnbpg__wzzj)
    c.pyapi.decref(jjyoa__kjnee)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ahqug__bbzs.dict = nzzun__qhex
    return NativeValue(ahqug__bbzs._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        zfcqi__kuq, srk__evz = args
        rfei__krw = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        rfei__krw.data = zfcqi__kuq
        rfei__krw.name = srk__evz
        context.nrt.incref(builder, signature.args[0], zfcqi__kuq)
        context.nrt.incref(builder, signature.args[1], srk__evz)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        rfei__krw.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return rfei__krw._getvalue()
    aif__uaus = IntervalIndexType(data, name)
    sig = signature(aif__uaus, data, name)
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
        bzo__qzpkr = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    nem__hmnz = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', hpx__dpg, idx_cpy_arg_defaults,
        fn_str=nem__hmnz, package_name='pandas', module_name='Index')
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
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    moi__muqv = c.pyapi.import_module_noblock(ufojv__fhqp)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, ahqug__bbzs.data)
    eum__wxt = c.pyapi.from_native_value(typ.data, ahqug__bbzs.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ahqug__bbzs.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, ahqug__bbzs.name,
        c.env_manager)
    acg__edzb = c.pyapi.make_none()
    nfew__slk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    fisd__ayz = c.pyapi.call_method(moi__muqv, 'Index', (eum__wxt,
        acg__edzb, nfew__slk, jjyoa__kjnee))
    c.pyapi.decref(eum__wxt)
    c.pyapi.decref(acg__edzb)
    c.pyapi.decref(nfew__slk)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(moi__muqv)
    c.context.nrt.decref(c.builder, typ, val)
    return fisd__ayz


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        eru__anxk = signature.return_type
        ahqug__bbzs = cgutils.create_struct_proxy(eru__anxk)(context, builder)
        ahqug__bbzs.data = args[0]
        ahqug__bbzs.name = args[1]
        context.nrt.incref(builder, eru__anxk.data, args[0])
        context.nrt.incref(builder, eru__anxk.name_typ, args[1])
        dtype = eru__anxk.dtype
        ahqug__bbzs.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return ahqug__bbzs._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    jnbpg__wzzj = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, jnbpg__wzzj).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    c.pyapi.decref(jnbpg__wzzj)
    c.pyapi.decref(jjyoa__kjnee)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    dtype = typ.dtype
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ahqug__bbzs.dict = nzzun__qhex
    return NativeValue(ahqug__bbzs._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        zyl__bltn = dict(dtype=dtype)
        vwlav__wwoov = dict(dtype=None)
        check_unsupported_args(func_str, zyl__bltn, vwlav__wwoov,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                naaqi__jez = bodo.utils.conversion.coerce_to_ndarray(data)
                gzn__qgqzw = bodo.utils.conversion.fix_arr_dtype(naaqi__jez,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(gzn__qgqzw
                    , name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                naaqi__jez = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    naaqi__jez = naaqi__jez.copy()
                gzn__qgqzw = bodo.utils.conversion.fix_arr_dtype(naaqi__jez,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(gzn__qgqzw
                    , name)
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
        bzo__qzpkr = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


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
        bzo__qzpkr = [('data', binary_array_type), ('name', fe_type.
            name_typ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    muz__bhlr = typ.data
    scalar_type = typ.data.dtype
    jnbpg__wzzj = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(muz__bhlr, jnbpg__wzzj).value
    jjyoa__kjnee = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jjyoa__kjnee).value
    c.pyapi.decref(jnbpg__wzzj)
    c.pyapi.decref(jjyoa__kjnee)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ahqug__bbzs.data = data
    ahqug__bbzs.name = name
    pjzf__nbe, nzzun__qhex = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    ahqug__bbzs.dict = nzzun__qhex
    return NativeValue(ahqug__bbzs._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    muz__bhlr = typ.data
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    moi__muqv = c.pyapi.import_module_noblock(ufojv__fhqp)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, muz__bhlr, ahqug__bbzs.data)
    eum__wxt = c.pyapi.from_native_value(muz__bhlr, ahqug__bbzs.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ahqug__bbzs.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, ahqug__bbzs.name,
        c.env_manager)
    acg__edzb = c.pyapi.make_none()
    nfew__slk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    fisd__ayz = c.pyapi.call_method(moi__muqv, 'Index', (eum__wxt,
        acg__edzb, nfew__slk, jjyoa__kjnee))
    c.pyapi.decref(eum__wxt)
    c.pyapi.decref(acg__edzb)
    c.pyapi.decref(nfew__slk)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(moi__muqv)
    c.context.nrt.decref(c.builder, typ, val)
    return fisd__ayz


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    lepv__gbhfd = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, lepv__gbhfd


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        ear__ctls = 'bytes_type'
    else:
        ear__ctls = 'string_type'
    alyze__jib = 'def impl(context, builder, signature, args):\n'
    alyze__jib += '    assert len(args) == 2\n'
    alyze__jib += '    index_typ = signature.return_type\n'
    alyze__jib += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    alyze__jib += '    index_val.data = args[0]\n'
    alyze__jib += '    index_val.name = args[1]\n'
    alyze__jib += '    # increase refcount of stored values\n'
    alyze__jib += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    alyze__jib += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    alyze__jib += '    # create empty dict for get_loc hashmap\n'
    alyze__jib += '    index_val.dict = context.compile_internal(\n'
    alyze__jib += '       builder,\n'
    alyze__jib += (
        f'       lambda: numba.typed.Dict.empty({ear__ctls}, types.int64),\n')
    alyze__jib += f'        types.DictType({ear__ctls}, types.int64)(), [],)\n'
    alyze__jib += '    return index_val._getvalue()\n'
    bfv__oyd = {}
    exec(alyze__jib, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, bfv__oyd)
    impl = bfv__oyd['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    nem__hmnz = idx_typ_to_format_str_map[typ].format('copy()')
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', hpx__dpg, idx_cpy_arg_defaults,
        fn_str=nem__hmnz, package_name='pandas', module_name='Index')
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
    uph__vtx = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    troaw__xtz = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', uph__vtx, troaw__xtz, package_name
        ='pandas', module_name='Index')
    return lambda I, indices: I[indices]


def _init_engine(I, ban_unique=True):
    pass


@overload(_init_engine)
def overload_init_engine(I, ban_unique=True):
    if isinstance(I, CategoricalIndexType):

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                aedc__tjx = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(aedc__tjx)):
                    if not bodo.libs.array_kernels.isna(aedc__tjx, i):
                        val = (bodo.hiframes.pd_categorical_ext.
                            get_code_for_value(aedc__tjx.dtype, aedc__tjx[i]))
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl
    else:

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                aedc__tjx = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(aedc__tjx)):
                    if not bodo.libs.array_kernels.isna(aedc__tjx, i):
                        val = aedc__tjx[i]
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
                aedc__tjx = bodo.utils.conversion.coerce_to_array(I)
                zjxvr__sqhnb = (bodo.hiframes.pd_categorical_ext.
                    get_code_for_value(aedc__tjx.dtype, key))
                return zjxvr__sqhnb in I._dict
            else:
                ttni__oydqy = (
                    'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                    )
                warnings.warn(ttni__oydqy)
                aedc__tjx = bodo.utils.conversion.coerce_to_array(I)
                ind = -1
                for i in range(len(aedc__tjx)):
                    if not bodo.libs.array_kernels.isna(aedc__tjx, i):
                        if aedc__tjx[i] == key:
                            ind = i
            return ind != -1
        return impl

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I, False)
            return key in I._dict
        else:
            ttni__oydqy = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(ttni__oydqy)
            aedc__tjx = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(aedc__tjx)):
                if not bodo.libs.array_kernels.isna(aedc__tjx, i):
                    if aedc__tjx[i] == key:
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
    uph__vtx = dict(method=method, tolerance=tolerance)
    rivf__tcn = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', uph__vtx, rivf__tcn,
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
            ttni__oydqy = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(ttni__oydqy)
            aedc__tjx = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(aedc__tjx)):
                if aedc__tjx[i] == key:
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
        jpuep__nlw = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                sbr__vwdhg = len(I)
                kma__iyyld = np.empty(sbr__vwdhg, np.bool_)
                for i in numba.parfors.parfor.internal_prange(sbr__vwdhg):
                    kma__iyyld[i] = not jpuep__nlw
                return kma__iyyld
            return impl
        alyze__jib = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if jpuep__nlw else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        bfv__oyd = {}
        exec(alyze__jib, {'bodo': bodo, 'np': np, 'numba': numba}, bfv__oyd)
        impl = bfv__oyd['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for efuob__yphir in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(efuob__yphir, overload_name, no_unliteral=True,
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
            aedc__tjx = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(aedc__tjx, 1)
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
            aedc__tjx = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(aedc__tjx, 2)
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
        aedc__tjx = bodo.hiframes.pd_index_ext.get_index_data(I)
        kma__iyyld = bodo.libs.array_kernels.duplicated((aedc__tjx,))
        return kma__iyyld
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
    uph__vtx = dict(keep=keep)
    rivf__tcn = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', uph__vtx, rivf__tcn,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    alyze__jib = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        alyze__jib += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        alyze__jib += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    bfv__oyd = {}
    exec(alyze__jib, {'bodo': bodo}, bfv__oyd)
    impl = bfv__oyd['impl']
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
    xvx__blgk = args[0]
    if isinstance(self.typemap[xvx__blgk.name], (HeterogeneousIndexType,
        MultiIndexType)):
        return None
    if equiv_set.has_shape(xvx__blgk):
        return ArrayAnalysis.AnalyzeResult(shape=xvx__blgk, pre=[])
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
    uph__vtx = dict(na_action=na_action)
    fxco__lstka = dict(na_action=None)
    check_unsupported_args('Index.map', uph__vtx, fxco__lstka, package_name
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
    ymhtk__llgoj = numba.core.registry.cpu_target.typing_context
    kyztd__skk = numba.core.registry.cpu_target.target_context
    try:
        bioj__vvw = get_const_func_output_type(mapper, (dtype,), {},
            ymhtk__llgoj, kyztd__skk)
    except Exception as fst__gdhyv:
        raise_bodo_error(get_udf_error_msg('Index.map()', fst__gdhyv))
    keysx__pcvwp = get_udf_out_arr_type(bioj__vvw)
    func = get_overload_const_func(mapper, None)
    alyze__jib = 'def f(I, mapper, na_action=None):\n'
    alyze__jib += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    alyze__jib += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    alyze__jib += '  numba.parfors.parfor.init_prange()\n'
    alyze__jib += '  n = len(A)\n'
    alyze__jib += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    alyze__jib += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    alyze__jib += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    alyze__jib += '    v = map_func(t2)\n'
    alyze__jib += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    alyze__jib += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    ppsm__qhla = bodo.compiler.udf_jit(func)
    bfv__oyd = {}
    exec(alyze__jib, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': ppsm__qhla, '_arr_typ': keysx__pcvwp,
        'init_nested_counts': bodo.utils.indexing.init_nested_counts,
        'add_nested_counts': bodo.utils.indexing.add_nested_counts,
        'data_arr_type': keysx__pcvwp.dtype}, bfv__oyd)
    f = bfv__oyd['f']
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
    wku__agcxn, fdawj__oyq = sig.args
    if wku__agcxn != fdawj__oyq:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    wku__agcxn, fdawj__oyq = sig.args
    if wku__agcxn != fdawj__oyq:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            alyze__jib = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(lhs)
"""
            if rhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                alyze__jib += """  dt = bodo.utils.conversion.unbox_if_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                alyze__jib += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            bfv__oyd = {}
            exec(alyze__jib, {'bodo': bodo, 'op': op}, bfv__oyd)
            impl = bfv__oyd['impl']
            return impl
        if is_index_type(rhs):
            alyze__jib = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(rhs)
"""
            if lhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                alyze__jib += """  dt = bodo.utils.conversion.unbox_if_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                alyze__jib += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            bfv__oyd = {}
            exec(alyze__jib, {'bodo': bodo, 'op': op}, bfv__oyd)
            impl = bfv__oyd['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    aedc__tjx = bodo.utils.conversion.coerce_to_array(data)
                    grc__lze = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    kma__iyyld = op(aedc__tjx, grc__lze)
                    return kma__iyyld
                return impl3
            count = len(lhs.data.types)
            alyze__jib = 'def f(lhs, rhs):\n'
            alyze__jib += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            bfv__oyd = {}
            exec(alyze__jib, {'op': op, 'np': np}, bfv__oyd)
            impl = bfv__oyd['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    aedc__tjx = bodo.utils.conversion.coerce_to_array(data)
                    grc__lze = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    kma__iyyld = op(grc__lze, aedc__tjx)
                    return kma__iyyld
                return impl4
            count = len(rhs.data.types)
            alyze__jib = 'def f(lhs, rhs):\n'
            alyze__jib += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            bfv__oyd = {}
            exec(alyze__jib, {'op': op, 'np': np}, bfv__oyd)
            impl = bfv__oyd['f']
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
        bzo__qzpkr = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, bzo__qzpkr)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    nem__hmnz = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    hpx__dpg = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', hpx__dpg, idx_cpy_arg_defaults,
        fn_str=nem__hmnz, package_name='pandas', module_name='Index')
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
    ufojv__fhqp = c.context.insert_const_string(c.builder.module, 'pandas')
    moi__muqv = c.pyapi.import_module_noblock(ufojv__fhqp)
    ahqug__bbzs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, ahqug__bbzs.data)
    eum__wxt = c.pyapi.from_native_value(typ.data, ahqug__bbzs.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ahqug__bbzs.name)
    jjyoa__kjnee = c.pyapi.from_native_value(typ.name_typ, ahqug__bbzs.name,
        c.env_manager)
    acg__edzb = c.pyapi.make_none()
    nfew__slk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    fisd__ayz = c.pyapi.call_method(moi__muqv, 'Index', (eum__wxt,
        acg__edzb, nfew__slk, jjyoa__kjnee))
    c.pyapi.decref(eum__wxt)
    c.pyapi.decref(acg__edzb)
    c.pyapi.decref(nfew__slk)
    c.pyapi.decref(jjyoa__kjnee)
    c.pyapi.decref(moi__muqv)
    c.context.nrt.decref(c.builder, typ, val)
    return fisd__ayz


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        eru__anxk = signature.return_type
        ahqug__bbzs = cgutils.create_struct_proxy(eru__anxk)(context, builder)
        ahqug__bbzs.data = args[0]
        ahqug__bbzs.name = args[1]
        context.nrt.incref(builder, eru__anxk.data, args[0])
        context.nrt.incref(builder, eru__anxk.name_typ, args[1])
        return ahqug__bbzs._getvalue()
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
    cyan__rsg = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in cyan__rsg:
        init_func = cyan__rsg[type(I)]
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
    hbc__nirvg = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index, RangeIndexType: bodo.
        hiframes.pd_index_ext.init_range_index}
    if type(I) in hbc__nirvg:
        return hbc__nirvg[type(I)]
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
    vevsz__gkptq = get_index_constructor(I)

    def impl(I):
        aedc__tjx = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        xlxp__sdtp = bodo.libs.array_kernels.unique(aedc__tjx)
        return vevsz__gkptq(xlxp__sdtp, name)
    return impl


@overload_method(RangeIndexType, 'unique', no_unliteral=True)
def overload_range_index_unique(I):

    def impl(I):
        return I.copy()
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
            dizek__izqyc = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_index_ext.get_index_data(I)
            sbr__vwdhg = len(A)
            kma__iyyld = np.empty(sbr__vwdhg, np.bool_)
            bodo.libs.array.array_isin(kma__iyyld, A, dizek__izqyc, False)
            return kma__iyyld
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        kma__iyyld = bodo.libs.array_ops.array_op_isin(A, values)
        return kma__iyyld
    return impl


@overload_method(RangeIndexType, 'isin', no_unliteral=True)
def overload_range_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            dizek__izqyc = bodo.utils.conversion.coerce_to_array(values)
            A = np.arange(I.start, I.stop, I.step)
            sbr__vwdhg = len(A)
            kma__iyyld = np.empty(sbr__vwdhg, np.bool_)
            bodo.libs.array.array_isin(kma__iyyld, A, dizek__izqyc, False)
            return kma__iyyld
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Index.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = np.arange(I.start, I.stop, I.step)
        kma__iyyld = bodo.libs.array_ops.array_op_isin(A, values)
        return kma__iyyld
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
    nxob__jpzjg = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, nxob__jpzjg])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    nxob__jpzjg = context.get_constant_null(types.DictType(types.int64,
        types.int64))
    return lir.Constant.literal_struct([data, name, nxob__jpzjg])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    nxob__jpzjg = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, nxob__jpzjg])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    muz__bhlr = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, muz__bhlr, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    nxob__jpzjg = context.get_constant_null(types.DictType(scalar_type,
        types.int64))
    return lir.Constant.literal_struct([data, name, nxob__jpzjg])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [sdel__orfhi] = sig.args
    [tun__src] = args
    uzylq__sotrk = context.make_helper(builder, sdel__orfhi, value=tun__src)
    epbe__xnij = context.make_helper(builder, sig.return_type)
    bqxwv__ubnn = cgutils.alloca_once_value(builder, uzylq__sotrk.start)
    otwwc__jmom = context.get_constant(types.intp, 0)
    vaad__hdcq = cgutils.alloca_once_value(builder, otwwc__jmom)
    epbe__xnij.iter = bqxwv__ubnn
    epbe__xnij.stop = uzylq__sotrk.stop
    epbe__xnij.step = uzylq__sotrk.step
    epbe__xnij.count = vaad__hdcq
    cgmk__ilex = builder.sub(uzylq__sotrk.stop, uzylq__sotrk.start)
    pgx__igzo = context.get_constant(types.intp, 1)
    ybo__swvn = builder.icmp_signed('>', cgmk__ilex, otwwc__jmom)
    ano__oyg = builder.icmp_signed('>', uzylq__sotrk.step, otwwc__jmom)
    kpu__cgats = builder.not_(builder.xor(ybo__swvn, ano__oyg))
    with builder.if_then(kpu__cgats):
        irex__kld = builder.srem(cgmk__ilex, uzylq__sotrk.step)
        irex__kld = builder.select(ybo__swvn, irex__kld, builder.neg(irex__kld)
            )
        pzqwp__xbmt = builder.icmp_signed('>', irex__kld, otwwc__jmom)
        sukuf__ztogh = builder.add(builder.sdiv(cgmk__ilex, uzylq__sotrk.
            step), builder.select(pzqwp__xbmt, pgx__igzo, otwwc__jmom))
        builder.store(sukuf__ztogh, vaad__hdcq)
    irsf__orxb = epbe__xnij._getvalue()
    xtniq__waly = impl_ret_new_ref(context, builder, sig.return_type,
        irsf__orxb)
    return xtniq__waly


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
    'is_type_compatible', 'item', 'join', 'memory_usage', 'nunique',
    'putmask', 'ravel', 'reindex', 'repeat', 'searchsorted', 'set_names',
    'set_value', 'shift', 'slice_indexer', 'slice_locs', 'sort',
    'sort_values', 'sortlevel', 'str', 'symmetric_difference',
    'to_flat_index', 'to_frame', 'to_list', 'to_native_types', 'to_numpy',
    'to_series', 'tolist', 'transpose', 'union', 'value_counts', 'view',
    'where']
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
    'isin']
multi_index_unsupported_atrs = ['levshape', 'levels', 'codes', 'dtypes',
    'values', 'shape', 'nbytes', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
multi_index_unsupported_methods = ['copy', 'set_levels', 'set_codes',
    'swaplevel', 'reorder_levels', 'remove_unused_levels', 'get_loc',
    'get_locs', 'get_loc_level', 'take', 'isna', 'isnull', 'map', 'isin',
    'unique']
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
string_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
binary_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
period_index_unsupported_methods = ['asfreq', 'strftime', 'to_timestamp',
    'isin', 'unique']
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
    for furo__xakv in index_unsupported_methods:
        for bkuws__hpl, typ in index_types:
            overload_method(typ, furo__xakv, no_unliteral=True)(
                create_unsupported_overload(bkuws__hpl.format(furo__xakv +
                '()')))
    for xmh__kegtd in index_unsupported_atrs:
        for bkuws__hpl, typ in index_types:
            overload_attribute(typ, xmh__kegtd, no_unliteral=True)(
                create_unsupported_overload(bkuws__hpl.format(xmh__kegtd)))
    punge__usz = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    higpj__vave = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods)]
    for typ, wwbyj__frwbo in higpj__vave:
        bkuws__hpl = idx_typ_to_format_str_map[typ]
        for zoide__rgf in wwbyj__frwbo:
            overload_method(typ, zoide__rgf, no_unliteral=True)(
                create_unsupported_overload(bkuws__hpl.format(zoide__rgf +
                '()')))
    for typ, nqb__tcooz in punge__usz:
        bkuws__hpl = idx_typ_to_format_str_map[typ]
        for xmh__kegtd in nqb__tcooz:
            overload_attribute(typ, xmh__kegtd, no_unliteral=True)(
                create_unsupported_overload(bkuws__hpl.format(xmh__kegtd)))
    for xiywt__hkm in [RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, MultiIndexType]:
        for zoide__rgf in ['max', 'min']:
            bkuws__hpl = idx_typ_to_format_str_map[xiywt__hkm]
            overload_method(xiywt__hkm, zoide__rgf, no_unliteral=True)(
                create_unsupported_overload(bkuws__hpl.format(zoide__rgf +
                '()')))


_install_index_unsupported()
