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
            qvs__ede = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(qvs__ede)
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
        scft__wdaj = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    iyxwm__rfxlo = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()'
        )
    check_unsupported_args('copy', zitic__jrol, idx_cpy_arg_defaults,
        fn_str=iyxwm__rfxlo, package_name='pandas', module_name='Index')
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
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    nifnr__dqc = c.pyapi.import_module_noblock(uoini__gxctr)
    nfz__uwlme = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, nfz__uwlme.data)
    thf__jsdml = c.pyapi.from_native_value(typ.data, nfz__uwlme.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, nfz__uwlme.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, nfz__uwlme.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([thf__jsdml])
    glmhq__qvs = c.pyapi.object_getattr_string(nifnr__dqc, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', eeath__hzscd)])
    ipt__alvhr = c.pyapi.call(glmhq__qvs, args, kws)
    c.pyapi.decref(thf__jsdml)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(nifnr__dqc)
    c.pyapi.decref(glmhq__qvs)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ipt__alvhr


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        nifeu__xen = c.pyapi.object_getattr_string(val, 'array')
    else:
        nifeu__xen = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, nifeu__xen).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    dtype = _dt_index_data_typ.dtype
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ipeir__oljvy.dict = qkb__hsixi
    c.pyapi.decref(nifeu__xen)
    c.pyapi.decref(eeath__hzscd)
    return NativeValue(ipeir__oljvy._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        xfems__ekec, nlkmc__nzq = args
        nfz__uwlme = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        nfz__uwlme.data = xfems__ekec
        nfz__uwlme.name = nlkmc__nzq
        context.nrt.incref(builder, signature.args[0], xfems__ekec)
        context.nrt.incref(builder, signature.args[1], nlkmc__nzq)
        dtype = _dt_index_data_typ.dtype
        nfz__uwlme.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return nfz__uwlme._getvalue()
    xjj__cbrva = DatetimeIndexType(name, data)
    sig = signature(xjj__cbrva, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    sdxaw__fha = args[0]
    if equiv_set.has_shape(sdxaw__fha):
        return ArrayAnalysis.AnalyzeResult(shape=sdxaw__fha, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    kvu__bxsmp = 'def impl(dti):\n'
    kvu__bxsmp += '    numba.parfors.parfor.init_prange()\n'
    kvu__bxsmp += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    kvu__bxsmp += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    kvu__bxsmp += '    n = len(A)\n'
    kvu__bxsmp += '    S = np.empty(n, np.int64)\n'
    kvu__bxsmp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    kvu__bxsmp += '        val = A[i]\n'
    kvu__bxsmp += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        kvu__bxsmp += '        S[i] = ts.' + field + '()\n'
    else:
        kvu__bxsmp += '        S[i] = ts.' + field + '\n'
    kvu__bxsmp += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    vvf__reiip = {}
    exec(kvu__bxsmp, {'numba': numba, 'np': np, 'bodo': bodo}, vvf__reiip)
    impl = vvf__reiip['impl']
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
        uqhku__xjnf = len(A)
        S = np.empty(uqhku__xjnf, np.bool_)
        for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
            val = A[i]
            cqbc__rnojo = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(cqbc__rnojo.year
                )
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        uqhku__xjnf = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            uqhku__xjnf)
        for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
            val = A[i]
            cqbc__rnojo = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(cqbc__rnojo.year, cqbc__rnojo.month,
                cqbc__rnojo.day)
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
    rzuf__vnll = dict(axis=axis, skipna=skipna)
    furwq__sgb = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        epc__vhzbv = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(epc__vhzbv)):
            if not bodo.libs.array_kernels.isna(epc__vhzbv, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(epc__vhzbv
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    rzuf__vnll = dict(axis=axis, skipna=skipna)
    furwq__sgb = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        epc__vhzbv = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(epc__vhzbv)):
            if not bodo.libs.array_kernels.isna(epc__vhzbv, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(epc__vhzbv
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
    rzuf__vnll = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    furwq__sgb = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        vtppp__ggf = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(vtppp__ggf)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        mwbf__kcwg = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            epc__vhzbv = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            uqhku__xjnf = len(epc__vhzbv)
            S = np.empty(uqhku__xjnf, mwbf__kcwg)
            bqqjd__kqq = rhs.value
            for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    epc__vhzbv[i]) - bqqjd__kqq)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        mwbf__kcwg = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            epc__vhzbv = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            uqhku__xjnf = len(epc__vhzbv)
            S = np.empty(uqhku__xjnf, mwbf__kcwg)
            bqqjd__kqq = lhs.value
            for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bqqjd__kqq - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(epc__vhzbv[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    jejoj__auv = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    kvu__bxsmp = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        kvu__bxsmp += '  dt_index, _str = lhs, rhs\n'
        hkmj__skimr = 'arr[i] {} other'.format(jejoj__auv)
    else:
        kvu__bxsmp += '  dt_index, _str = rhs, lhs\n'
        hkmj__skimr = 'other {} arr[i]'.format(jejoj__auv)
    kvu__bxsmp += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    kvu__bxsmp += '  l = len(arr)\n'
    kvu__bxsmp += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    kvu__bxsmp += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    kvu__bxsmp += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    kvu__bxsmp += '    S[i] = {}\n'.format(hkmj__skimr)
    kvu__bxsmp += '  return S\n'
    vvf__reiip = {}
    exec(kvu__bxsmp, {'bodo': bodo, 'numba': numba, 'np': np}, vvf__reiip)
    impl = vvf__reiip['impl']
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
        zjc__nbcxd = parse_dtype(dtype, 'pandas.Index')
        jqfjm__egin = False
    else:
        zjc__nbcxd = getattr(data, 'dtype', None)
        jqfjm__egin = True
    if isinstance(zjc__nbcxd, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType) or zjc__nbcxd == types.NPDatetime(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or zjc__nbcxd == types.NPTimedelta('ns'):

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
        if isinstance(zjc__nbcxd, (types.Integer, types.Float, types.Boolean)):
            if jqfjm__egin:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    vtppp__ggf = bodo.utils.conversion.coerce_to_array(data)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        vtppp__ggf, name)
            else:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    vtppp__ggf = bodo.utils.conversion.coerce_to_array(data)
                    ilrq__qhwun = bodo.utils.conversion.fix_arr_dtype(
                        vtppp__ggf, zjc__nbcxd)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        ilrq__qhwun, name)
        elif zjc__nbcxd in [types.string, bytes_type]:

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
                iwu__aruer = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = iwu__aruer[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                iwu__aruer = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                ngb__wcp = iwu__aruer[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(ngb__wcp,
                    name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            vgnhs__msh = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(vgnhs__msh[ind])
        return impl

    def impl(I, ind):
        vgnhs__msh = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        ngb__wcp = vgnhs__msh[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(ngb__wcp, name)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_categorical_index_getitem(I, ind):
    if not isinstance(I, CategoricalIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            kod__soe = bodo.hiframes.pd_index_ext.get_index_data(I)
            val = kod__soe[ind]
            return val
        return impl
    if isinstance(ind, types.SliceType):

        def impl(I, ind):
            kod__soe = bodo.hiframes.pd_index_ext.get_index_data(I)
            name = bodo.hiframes.pd_index_ext.get_index_name(I)
            ngb__wcp = kod__soe[ind]
            return bodo.hiframes.pd_index_ext.init_categorical_index(ngb__wcp,
                name)
        return impl
    raise BodoError(
        f'pd.CategoricalIndex.__getitem__: unsupported index type {ind}')


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    tkv__rotle = False
    bpahk__vtx = False
    if closed is None:
        tkv__rotle = True
        bpahk__vtx = True
    elif closed == 'left':
        tkv__rotle = True
    elif closed == 'right':
        bpahk__vtx = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return tkv__rotle, bpahk__vtx


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
    rzuf__vnll = dict(tz=tz, normalize=normalize, closed=closed)
    furwq__sgb = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    efq__nuc = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        efq__nuc = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    kvu__bxsmp = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    kvu__bxsmp += efq__nuc
    if is_overload_none(start):
        kvu__bxsmp += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        kvu__bxsmp += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        kvu__bxsmp += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        kvu__bxsmp += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        kvu__bxsmp += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            kvu__bxsmp += '  b = start_t.value\n'
            kvu__bxsmp += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            kvu__bxsmp += '  b = start_t.value\n'
            kvu__bxsmp += '  addend = np.int64(periods) * np.int64(stride)\n'
            kvu__bxsmp += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            kvu__bxsmp += '  e = end_t.value + stride\n'
            kvu__bxsmp += '  addend = np.int64(periods) * np.int64(-stride)\n'
            kvu__bxsmp += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        kvu__bxsmp += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        kvu__bxsmp += '  delta = end_t.value - start_t.value\n'
        kvu__bxsmp += '  step = delta / (periods - 1)\n'
        kvu__bxsmp += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        kvu__bxsmp += '  arr1 *= step\n'
        kvu__bxsmp += '  arr1 += start_t.value\n'
        kvu__bxsmp += '  arr = arr1.astype(np.int64)\n'
        kvu__bxsmp += '  arr[-1] = end_t.value\n'
    kvu__bxsmp += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    kvu__bxsmp += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    vvf__reiip = {}
    exec(kvu__bxsmp, {'bodo': bodo, 'np': np, 'pd': pd}, vvf__reiip)
    f = vvf__reiip['f']
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
        trf__clv = pd.Timedelta('1 day')
        if start is not None:
            trf__clv = pd.Timedelta(start)
        htwd__tcjlw = pd.Timedelta('1 day')
        if end is not None:
            htwd__tcjlw = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        tkv__rotle, bpahk__vtx = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            liuaz__jkxpa = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = trf__clv.value
                mvvc__wap = b + (htwd__tcjlw.value - b
                    ) // liuaz__jkxpa * liuaz__jkxpa + liuaz__jkxpa // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = trf__clv.value
                ojo__sjxw = np.int64(periods) * np.int64(liuaz__jkxpa)
                mvvc__wap = np.int64(b) + ojo__sjxw
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                mvvc__wap = htwd__tcjlw.value + liuaz__jkxpa
                ojo__sjxw = np.int64(periods) * np.int64(-liuaz__jkxpa)
                b = np.int64(mvvc__wap) + ojo__sjxw
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            qngf__jwi = np.arange(b, mvvc__wap, liuaz__jkxpa, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            basrl__nuzg = htwd__tcjlw.value - trf__clv.value
            step = basrl__nuzg / (periods - 1)
            azego__yfu = np.arange(0, periods, 1, np.float64)
            azego__yfu *= step
            azego__yfu += trf__clv.value
            qngf__jwi = azego__yfu.astype(np.int64)
            qngf__jwi[-1] = htwd__tcjlw.value
        if not tkv__rotle and len(qngf__jwi) and qngf__jwi[0
            ] == trf__clv.value:
            qngf__jwi = qngf__jwi[1:]
        if not bpahk__vtx and len(qngf__jwi) and qngf__jwi[-1
            ] == htwd__tcjlw.value:
            qngf__jwi = qngf__jwi[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(qngf__jwi)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        uqhku__xjnf = len(A)
        cvit__hjk = bodo.libs.int_arr_ext.alloc_int_array(uqhku__xjnf, np.
            uint32)
        wiac__spqyl = bodo.libs.int_arr_ext.alloc_int_array(uqhku__xjnf, np
            .uint32)
        zdt__ael = bodo.libs.int_arr_ext.alloc_int_array(uqhku__xjnf, np.uint32
            )
        for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(cvit__hjk, i)
                bodo.libs.array_kernels.setna(wiac__spqyl, i)
                bodo.libs.array_kernels.setna(zdt__ael, i)
                continue
            cvit__hjk[i], wiac__spqyl[i], zdt__ael[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((cvit__hjk,
            wiac__spqyl, zdt__ael), idx, ('year', 'week', 'day'))
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
        scft__wdaj = [('data', _timedelta_index_data_typ), ('name', fe_type
            .name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, scft__wdaj)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    nifnr__dqc = c.pyapi.import_module_noblock(uoini__gxctr)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    thf__jsdml = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([thf__jsdml])
    kws = c.pyapi.dict_pack([('name', eeath__hzscd)])
    glmhq__qvs = c.pyapi.object_getattr_string(nifnr__dqc, 'TimedeltaIndex')
    ipt__alvhr = c.pyapi.call(glmhq__qvs, args, kws)
    c.pyapi.decref(thf__jsdml)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(nifnr__dqc)
    c.pyapi.decref(glmhq__qvs)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ipt__alvhr


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    zcgc__byw = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, zcgc__byw).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    c.pyapi.decref(zcgc__byw)
    c.pyapi.decref(eeath__hzscd)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    dtype = _timedelta_index_data_typ.dtype
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ipeir__oljvy.dict = qkb__hsixi
    return NativeValue(ipeir__oljvy._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        xfems__ekec, nlkmc__nzq = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = xfems__ekec
        timedelta_index.name = nlkmc__nzq
        context.nrt.incref(builder, signature.args[0], xfems__ekec)
        context.nrt.incref(builder, signature.args[1], nlkmc__nzq)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    xjj__cbrva = TimedeltaIndexType(name)
    sig = signature(xjj__cbrva, data, name)
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
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    iyxwm__rfxlo = idx_typ_to_format_str_map[TimedeltaIndexType].format(
        'copy()')
    check_unsupported_args('TimedeltaIndex.copy', zitic__jrol,
        idx_cpy_arg_defaults, fn_str=iyxwm__rfxlo, package_name='pandas',
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
    rzuf__vnll = dict(axis=axis, skipna=skipna)
    furwq__sgb = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        uqhku__xjnf = len(data)
        zjl__oda = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            zjl__oda = min(zjl__oda, val)
        fzg__nxdm = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            zjl__oda)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(fzg__nxdm, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    rzuf__vnll = dict(axis=axis, skipna=skipna)
    furwq__sgb = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        uqhku__xjnf = len(data)
        gqdpk__psl = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            gqdpk__psl = max(gqdpk__psl, val)
        fzg__nxdm = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            gqdpk__psl)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(fzg__nxdm, count)
    return impl


def gen_tdi_field_impl(field):
    kvu__bxsmp = 'def impl(tdi):\n'
    kvu__bxsmp += '    numba.parfors.parfor.init_prange()\n'
    kvu__bxsmp += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    kvu__bxsmp += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    kvu__bxsmp += '    n = len(A)\n'
    kvu__bxsmp += '    S = np.empty(n, np.int64)\n'
    kvu__bxsmp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    kvu__bxsmp += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        kvu__bxsmp += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        kvu__bxsmp += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        kvu__bxsmp += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        kvu__bxsmp += (
            '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
    else:
        assert False, 'invalid timedelta field'
    kvu__bxsmp += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    vvf__reiip = {}
    exec(kvu__bxsmp, {'numba': numba, 'np': np, 'bodo': bodo}, vvf__reiip)
    impl = vvf__reiip['impl']
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
    rzuf__vnll = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    furwq__sgb = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        vtppp__ggf = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(vtppp__ggf)
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
        scft__wdaj = [('start', types.int64), ('stop', types.int64), (
            'step', types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    iyxwm__rfxlo = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', zitic__jrol,
        idx_cpy_arg_defaults, fn_str=iyxwm__rfxlo, package_name='pandas',
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
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    vajv__zttzs = c.pyapi.import_module_noblock(uoini__gxctr)
    jhghl__fbgzr = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    nris__nhl = c.pyapi.from_native_value(types.int64, jhghl__fbgzr.start,
        c.env_manager)
    edql__oyg = c.pyapi.from_native_value(types.int64, jhghl__fbgzr.stop, c
        .env_manager)
    csr__aice = c.pyapi.from_native_value(types.int64, jhghl__fbgzr.step, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, jhghl__fbgzr.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, jhghl__fbgzr.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([nris__nhl, edql__oyg, csr__aice])
    kws = c.pyapi.dict_pack([('name', eeath__hzscd)])
    glmhq__qvs = c.pyapi.object_getattr_string(vajv__zttzs, 'RangeIndex')
    ynjko__imaud = c.pyapi.call(glmhq__qvs, args, kws)
    c.pyapi.decref(nris__nhl)
    c.pyapi.decref(edql__oyg)
    c.pyapi.decref(csr__aice)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(vajv__zttzs)
    c.pyapi.decref(glmhq__qvs)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ynjko__imaud


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name
    kkgs__ccf = is_overload_constant_int(step) and get_overload_const_int(step
        ) == 0

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        if kkgs__ccf:
            raise_bodo_error('Step must not be zero')
        eoflc__xtmbe = cgutils.is_scalar_zero(builder, args[2])
        khu__bfbu = context.get_python_api(builder)
        with builder.if_then(eoflc__xtmbe):
            khu__bfbu.err_format('PyExc_ValueError', 'Step must not be zero')
            val = context.get_constant(types.int32, -1)
            builder.ret(val)
        jhghl__fbgzr = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        jhghl__fbgzr.start = args[0]
        jhghl__fbgzr.stop = args[1]
        jhghl__fbgzr.step = args[2]
        jhghl__fbgzr.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return jhghl__fbgzr._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, wlksz__ldq = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    nris__nhl = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, nris__nhl).value
    edql__oyg = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, edql__oyg).value
    csr__aice = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, csr__aice).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    c.pyapi.decref(nris__nhl)
    c.pyapi.decref(edql__oyg)
    c.pyapi.decref(csr__aice)
    c.pyapi.decref(eeath__hzscd)
    jhghl__fbgzr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jhghl__fbgzr.start = start
    jhghl__fbgzr.stop = stop
    jhghl__fbgzr.step = step
    jhghl__fbgzr.name = name
    return NativeValue(jhghl__fbgzr._getvalue())


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
        rxmwv__yusvw = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(rxmwv__yusvw.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        rxmwv__yusvw = 'RangeIndex(...) must be called with integers'
        raise BodoError(rxmwv__yusvw)
    msv__uhxz = 'start'
    ntdn__tdv = 'stop'
    tkoy__bsx = 'step'
    if is_overload_none(start):
        msv__uhxz = '0'
    if is_overload_none(stop):
        ntdn__tdv = 'start'
        msv__uhxz = '0'
    if is_overload_none(step):
        tkoy__bsx = '1'
    kvu__bxsmp = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    kvu__bxsmp += '  return init_range_index({}, {}, {}, name)\n'.format(
        msv__uhxz, ntdn__tdv, tkoy__bsx)
    vvf__reiip = {}
    exec(kvu__bxsmp, {'init_range_index': init_range_index}, vvf__reiip)
    oxq__nnv = vvf__reiip['_pd_range_index_imp']
    return oxq__nnv


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
                eozt__pkh = numba.cpython.unicode._normalize_slice(idx, len(I))
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * eozt__pkh.start
                stop = I._start + I._step * eozt__pkh.stop
                step = I._step * eozt__pkh.step
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
        scft__wdaj = [('data', bodo.IntegerArrayType(types.int64)), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    iyxwm__rfxlo = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', zitic__jrol,
        idx_cpy_arg_defaults, fn_str=iyxwm__rfxlo, package_name='pandas',
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
        xfems__ekec, nlkmc__nzq, wlksz__ldq = args
        bjaw__wfguv = signature.return_type
        fqc__wvnhr = cgutils.create_struct_proxy(bjaw__wfguv)(context, builder)
        fqc__wvnhr.data = xfems__ekec
        fqc__wvnhr.name = nlkmc__nzq
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        fqc__wvnhr.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return fqc__wvnhr._getvalue()
    eceud__gwc = get_overload_const_str(freq)
    xjj__cbrva = PeriodIndexType(eceud__gwc, name)
    sig = signature(xjj__cbrva, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    vajv__zttzs = c.pyapi.import_module_noblock(uoini__gxctr)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        ipeir__oljvy.data)
    nifeu__xen = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), ipeir__oljvy.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ipeir__oljvy.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, ipeir__oljvy.
        name, c.env_manager)
    ehsh__mcmq = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', nifeu__xen), ('name', eeath__hzscd
        ), ('freq', ehsh__mcmq)])
    glmhq__qvs = c.pyapi.object_getattr_string(vajv__zttzs, 'PeriodIndex')
    ynjko__imaud = c.pyapi.call(glmhq__qvs, args, kws)
    c.pyapi.decref(nifeu__xen)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(ehsh__mcmq)
    c.pyapi.decref(vajv__zttzs)
    c.pyapi.decref(glmhq__qvs)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ynjko__imaud


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    wdajm__uwzz = c.pyapi.object_getattr_string(val, 'asi8')
    uabqt__emzds = c.pyapi.call_method(val, 'isna', ())
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    nifnr__dqc = c.pyapi.import_module_noblock(uoini__gxctr)
    sdz__qhpej = c.pyapi.object_getattr_string(nifnr__dqc, 'arrays')
    nifeu__xen = c.pyapi.call_method(sdz__qhpej, 'IntegerArray', (
        wdajm__uwzz, uabqt__emzds))
    data = c.pyapi.to_native_value(arr_typ, nifeu__xen).value
    c.pyapi.decref(wdajm__uwzz)
    c.pyapi.decref(uabqt__emzds)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(nifnr__dqc)
    c.pyapi.decref(sdz__qhpej)
    c.pyapi.decref(nifeu__xen)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    ipeir__oljvy.dict = qkb__hsixi
    return NativeValue(ipeir__oljvy._getvalue())


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
        ruqrn__xid = get_categories_int_type(fe_type.data.dtype)
        scft__wdaj = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(ruqrn__xid, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type,
            scft__wdaj)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    nifnr__dqc = c.pyapi.import_module_noblock(uoini__gxctr)
    vqrp__emowq = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, vqrp__emowq.data)
    thf__jsdml = c.pyapi.from_native_value(typ.data, vqrp__emowq.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, vqrp__emowq.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, vqrp__emowq.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([thf__jsdml])
    kws = c.pyapi.dict_pack([('name', eeath__hzscd)])
    glmhq__qvs = c.pyapi.object_getattr_string(nifnr__dqc, 'CategoricalIndex')
    ipt__alvhr = c.pyapi.call(glmhq__qvs, args, kws)
    c.pyapi.decref(thf__jsdml)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(nifnr__dqc)
    c.pyapi.decref(glmhq__qvs)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ipt__alvhr


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    zcgc__byw = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, zcgc__byw).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    c.pyapi.decref(zcgc__byw)
    c.pyapi.decref(eeath__hzscd)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ipeir__oljvy.dict = qkb__hsixi
    return NativeValue(ipeir__oljvy._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        xfems__ekec, nlkmc__nzq = args
        vqrp__emowq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        vqrp__emowq.data = xfems__ekec
        vqrp__emowq.name = nlkmc__nzq
        context.nrt.incref(builder, signature.args[0], xfems__ekec)
        context.nrt.incref(builder, signature.args[1], nlkmc__nzq)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        vqrp__emowq.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return vqrp__emowq._getvalue()
    xjj__cbrva = CategoricalIndexType(data, name)
    sig = signature(xjj__cbrva, data, name)
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
    iyxwm__rfxlo = idx_typ_to_format_str_map[CategoricalIndexType].format(
        'copy()')
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', zitic__jrol,
        idx_cpy_arg_defaults, fn_str=iyxwm__rfxlo, package_name='pandas',
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
        scft__wdaj = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, scft__wdaj)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    nifnr__dqc = c.pyapi.import_module_noblock(uoini__gxctr)
    hqg__bduw = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, hqg__bduw.data)
    thf__jsdml = c.pyapi.from_native_value(typ.data, hqg__bduw.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, hqg__bduw.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, hqg__bduw.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([thf__jsdml])
    kws = c.pyapi.dict_pack([('name', eeath__hzscd)])
    glmhq__qvs = c.pyapi.object_getattr_string(nifnr__dqc, 'IntervalIndex')
    ipt__alvhr = c.pyapi.call(glmhq__qvs, args, kws)
    c.pyapi.decref(thf__jsdml)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(nifnr__dqc)
    c.pyapi.decref(glmhq__qvs)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ipt__alvhr


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    zcgc__byw = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, zcgc__byw).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    c.pyapi.decref(zcgc__byw)
    c.pyapi.decref(eeath__hzscd)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ipeir__oljvy.dict = qkb__hsixi
    return NativeValue(ipeir__oljvy._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        xfems__ekec, nlkmc__nzq = args
        hqg__bduw = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        hqg__bduw.data = xfems__ekec
        hqg__bduw.name = nlkmc__nzq
        context.nrt.incref(builder, signature.args[0], xfems__ekec)
        context.nrt.incref(builder, signature.args[1], nlkmc__nzq)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        hqg__bduw.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return hqg__bduw._getvalue()
    xjj__cbrva = IntervalIndexType(data, name)
    sig = signature(xjj__cbrva, data, name)
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
        scft__wdaj = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    iyxwm__rfxlo = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', zitic__jrol, idx_cpy_arg_defaults,
        fn_str=iyxwm__rfxlo, package_name='pandas', module_name='Index')
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
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    vajv__zttzs = c.pyapi.import_module_noblock(uoini__gxctr)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, ipeir__oljvy.data)
    nifeu__xen = c.pyapi.from_native_value(typ.data, ipeir__oljvy.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ipeir__oljvy.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, ipeir__oljvy.
        name, c.env_manager)
    hrs__iwn = c.pyapi.make_none()
    bpk__gyv = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    ynjko__imaud = c.pyapi.call_method(vajv__zttzs, 'Index', (nifeu__xen,
        hrs__iwn, bpk__gyv, eeath__hzscd))
    c.pyapi.decref(nifeu__xen)
    c.pyapi.decref(hrs__iwn)
    c.pyapi.decref(bpk__gyv)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(vajv__zttzs)
    c.context.nrt.decref(c.builder, typ, val)
    return ynjko__imaud


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        bjaw__wfguv = signature.return_type
        ipeir__oljvy = cgutils.create_struct_proxy(bjaw__wfguv)(context,
            builder)
        ipeir__oljvy.data = args[0]
        ipeir__oljvy.name = args[1]
        context.nrt.incref(builder, bjaw__wfguv.data, args[0])
        context.nrt.incref(builder, bjaw__wfguv.name_typ, args[1])
        dtype = bjaw__wfguv.dtype
        ipeir__oljvy.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return ipeir__oljvy._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    zcgc__byw = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, zcgc__byw).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    c.pyapi.decref(zcgc__byw)
    c.pyapi.decref(eeath__hzscd)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    dtype = typ.dtype
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    ipeir__oljvy.dict = qkb__hsixi
    return NativeValue(ipeir__oljvy._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        dhmtj__emlmd = dict(dtype=dtype)
        vku__enji = dict(dtype=None)
        check_unsupported_args(func_str, dhmtj__emlmd, vku__enji,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                vtppp__ggf = bodo.utils.conversion.coerce_to_ndarray(data)
                srrgl__mkf = bodo.utils.conversion.fix_arr_dtype(vtppp__ggf,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(srrgl__mkf
                    , name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                vtppp__ggf = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    vtppp__ggf = vtppp__ggf.copy()
                srrgl__mkf = bodo.utils.conversion.fix_arr_dtype(vtppp__ggf,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(srrgl__mkf
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
        scft__wdaj = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


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
        scft__wdaj = [('data', binary_array_type), ('name', fe_type.
            name_typ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    qitd__jauma = typ.data
    scalar_type = typ.data.dtype
    zcgc__byw = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(qitd__jauma, zcgc__byw).value
    eeath__hzscd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, eeath__hzscd).value
    c.pyapi.decref(zcgc__byw)
    c.pyapi.decref(eeath__hzscd)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipeir__oljvy.data = data
    ipeir__oljvy.name = name
    scu__quhlf, qkb__hsixi = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    ipeir__oljvy.dict = qkb__hsixi
    return NativeValue(ipeir__oljvy._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    qitd__jauma = typ.data
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    vajv__zttzs = c.pyapi.import_module_noblock(uoini__gxctr)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, qitd__jauma, ipeir__oljvy.data)
    nifeu__xen = c.pyapi.from_native_value(qitd__jauma, ipeir__oljvy.data,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ipeir__oljvy.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, ipeir__oljvy.
        name, c.env_manager)
    hrs__iwn = c.pyapi.make_none()
    bpk__gyv = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    ynjko__imaud = c.pyapi.call_method(vajv__zttzs, 'Index', (nifeu__xen,
        hrs__iwn, bpk__gyv, eeath__hzscd))
    c.pyapi.decref(nifeu__xen)
    c.pyapi.decref(hrs__iwn)
    c.pyapi.decref(bpk__gyv)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(vajv__zttzs)
    c.context.nrt.decref(c.builder, typ, val)
    return ynjko__imaud


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    zhwum__upfm = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, zhwum__upfm


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        mbxxx__efz = 'bytes_type'
    else:
        mbxxx__efz = 'string_type'
    kvu__bxsmp = 'def impl(context, builder, signature, args):\n'
    kvu__bxsmp += '    assert len(args) == 2\n'
    kvu__bxsmp += '    index_typ = signature.return_type\n'
    kvu__bxsmp += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    kvu__bxsmp += '    index_val.data = args[0]\n'
    kvu__bxsmp += '    index_val.name = args[1]\n'
    kvu__bxsmp += '    # increase refcount of stored values\n'
    kvu__bxsmp += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    kvu__bxsmp += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    kvu__bxsmp += '    # create empty dict for get_loc hashmap\n'
    kvu__bxsmp += '    index_val.dict = context.compile_internal(\n'
    kvu__bxsmp += '       builder,\n'
    kvu__bxsmp += (
        f'       lambda: numba.typed.Dict.empty({mbxxx__efz}, types.int64),\n')
    kvu__bxsmp += (
        f'        types.DictType({mbxxx__efz}, types.int64)(), [],)\n')
    kvu__bxsmp += '    return index_val._getvalue()\n'
    vvf__reiip = {}
    exec(kvu__bxsmp, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, vvf__reiip)
    impl = vvf__reiip['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    iyxwm__rfxlo = idx_typ_to_format_str_map[typ].format('copy()')
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', zitic__jrol, idx_cpy_arg_defaults,
        fn_str=iyxwm__rfxlo, package_name='pandas', module_name='Index')
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
    rzuf__vnll = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    usqw__sxtd = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', rzuf__vnll, usqw__sxtd,
        package_name='pandas', module_name='Index')
    return lambda I, indices: I[indices]


def _init_engine(I, ban_unique=True):
    pass


@overload(_init_engine)
def overload_init_engine(I, ban_unique=True):
    if isinstance(I, CategoricalIndexType):

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                qngf__jwi = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(qngf__jwi)):
                    if not bodo.libs.array_kernels.isna(qngf__jwi, i):
                        val = (bodo.hiframes.pd_categorical_ext.
                            get_code_for_value(qngf__jwi.dtype, qngf__jwi[i]))
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl
    else:

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                qngf__jwi = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(qngf__jwi)):
                    if not bodo.libs.array_kernels.isna(qngf__jwi, i):
                        val = qngf__jwi[i]
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
                qngf__jwi = bodo.utils.conversion.coerce_to_array(I)
                nyycn__xwq = (bodo.hiframes.pd_categorical_ext.
                    get_code_for_value(qngf__jwi.dtype, key))
                return nyycn__xwq in I._dict
            else:
                rxmwv__yusvw = (
                    'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                    )
                warnings.warn(rxmwv__yusvw)
                qngf__jwi = bodo.utils.conversion.coerce_to_array(I)
                ind = -1
                for i in range(len(qngf__jwi)):
                    if not bodo.libs.array_kernels.isna(qngf__jwi, i):
                        if qngf__jwi[i] == key:
                            ind = i
            return ind != -1
        return impl

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I, False)
            return key in I._dict
        else:
            rxmwv__yusvw = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(rxmwv__yusvw)
            qngf__jwi = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(qngf__jwi)):
                if not bodo.libs.array_kernels.isna(qngf__jwi, i):
                    if qngf__jwi[i] == key:
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
    rzuf__vnll = dict(method=method, tolerance=tolerance)
    furwq__sgb = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', rzuf__vnll, furwq__sgb,
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
            rxmwv__yusvw = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(rxmwv__yusvw)
            qngf__jwi = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(qngf__jwi)):
                if qngf__jwi[i] == key:
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
        cji__qtz = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                uqhku__xjnf = len(I)
                dkr__tkltg = np.empty(uqhku__xjnf, np.bool_)
                for i in numba.parfors.parfor.internal_prange(uqhku__xjnf):
                    dkr__tkltg[i] = not cji__qtz
                return dkr__tkltg
            return impl
        kvu__bxsmp = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if cji__qtz else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        vvf__reiip = {}
        exec(kvu__bxsmp, {'bodo': bodo, 'np': np, 'numba': numba}, vvf__reiip)
        impl = vvf__reiip['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for vri__whe in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(vri__whe, overload_name, no_unliteral=True,
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
            qngf__jwi = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(qngf__jwi, 1)
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
            qngf__jwi = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(qngf__jwi, 2)
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
        qngf__jwi = bodo.hiframes.pd_index_ext.get_index_data(I)
        dkr__tkltg = bodo.libs.array_kernels.duplicated((qngf__jwi,))
        return dkr__tkltg
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
    rzuf__vnll = dict(keep=keep)
    furwq__sgb = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', rzuf__vnll, furwq__sgb,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    kvu__bxsmp = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        kvu__bxsmp += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        kvu__bxsmp += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    vvf__reiip = {}
    exec(kvu__bxsmp, {'bodo': bodo}, vvf__reiip)
    impl = vvf__reiip['impl']
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
    sdxaw__fha = args[0]
    if isinstance(self.typemap[sdxaw__fha.name], (HeterogeneousIndexType,
        MultiIndexType)):
        return None
    if equiv_set.has_shape(sdxaw__fha):
        return ArrayAnalysis.AnalyzeResult(shape=sdxaw__fha, pre=[])
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
    rzuf__vnll = dict(na_action=na_action)
    puqdp__yjgou = dict(na_action=None)
    check_unsupported_args('Index.map', rzuf__vnll, puqdp__yjgou,
        package_name='pandas', module_name='Index')
    dtype = I.dtype
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.map')
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    gmknh__yfwn = numba.core.registry.cpu_target.typing_context
    qon__hala = numba.core.registry.cpu_target.target_context
    try:
        xsjfm__vqdfr = get_const_func_output_type(mapper, (dtype,), {},
            gmknh__yfwn, qon__hala)
    except Exception as mvvc__wap:
        raise_bodo_error(get_udf_error_msg('Index.map()', mvvc__wap))
    rlyi__xwd = get_udf_out_arr_type(xsjfm__vqdfr)
    func = get_overload_const_func(mapper, None)
    kvu__bxsmp = 'def f(I, mapper, na_action=None):\n'
    kvu__bxsmp += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    kvu__bxsmp += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    kvu__bxsmp += '  numba.parfors.parfor.init_prange()\n'
    kvu__bxsmp += '  n = len(A)\n'
    kvu__bxsmp += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    kvu__bxsmp += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    kvu__bxsmp += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    kvu__bxsmp += '    v = map_func(t2)\n'
    kvu__bxsmp += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    kvu__bxsmp += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    hbjt__ivix = bodo.compiler.udf_jit(func)
    vvf__reiip = {}
    exec(kvu__bxsmp, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': hbjt__ivix, '_arr_typ': rlyi__xwd, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'data_arr_type': rlyi__xwd.dtype},
        vvf__reiip)
    f = vvf__reiip['f']
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
    kbvv__dyafi, ghv__yaw = sig.args
    if kbvv__dyafi != ghv__yaw:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    kbvv__dyafi, ghv__yaw = sig.args
    if kbvv__dyafi != ghv__yaw:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            kvu__bxsmp = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(lhs)
"""
            if rhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                kvu__bxsmp += """  dt = bodo.utils.conversion.unbox_if_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                kvu__bxsmp += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            vvf__reiip = {}
            exec(kvu__bxsmp, {'bodo': bodo, 'op': op}, vvf__reiip)
            impl = vvf__reiip['impl']
            return impl
        if is_index_type(rhs):
            kvu__bxsmp = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(rhs)
"""
            if lhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                kvu__bxsmp += """  dt = bodo.utils.conversion.unbox_if_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                kvu__bxsmp += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            vvf__reiip = {}
            exec(kvu__bxsmp, {'bodo': bodo, 'op': op}, vvf__reiip)
            impl = vvf__reiip['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    qngf__jwi = bodo.utils.conversion.coerce_to_array(data)
                    wbp__vxndk = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    dkr__tkltg = op(qngf__jwi, wbp__vxndk)
                    return dkr__tkltg
                return impl3
            count = len(lhs.data.types)
            kvu__bxsmp = 'def f(lhs, rhs):\n'
            kvu__bxsmp += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            vvf__reiip = {}
            exec(kvu__bxsmp, {'op': op, 'np': np}, vvf__reiip)
            impl = vvf__reiip['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    qngf__jwi = bodo.utils.conversion.coerce_to_array(data)
                    wbp__vxndk = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    dkr__tkltg = op(wbp__vxndk, qngf__jwi)
                    return dkr__tkltg
                return impl4
            count = len(rhs.data.types)
            kvu__bxsmp = 'def f(lhs, rhs):\n'
            kvu__bxsmp += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            vvf__reiip = {}
            exec(kvu__bxsmp, {'op': op, 'np': np}, vvf__reiip)
            impl = vvf__reiip['f']
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
        scft__wdaj = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, scft__wdaj)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    iyxwm__rfxlo = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    zitic__jrol = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', zitic__jrol, idx_cpy_arg_defaults,
        fn_str=iyxwm__rfxlo, package_name='pandas', module_name='Index')
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
    uoini__gxctr = c.context.insert_const_string(c.builder.module, 'pandas')
    vajv__zttzs = c.pyapi.import_module_noblock(uoini__gxctr)
    ipeir__oljvy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, ipeir__oljvy.data)
    nifeu__xen = c.pyapi.from_native_value(typ.data, ipeir__oljvy.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ipeir__oljvy.name)
    eeath__hzscd = c.pyapi.from_native_value(typ.name_typ, ipeir__oljvy.
        name, c.env_manager)
    hrs__iwn = c.pyapi.make_none()
    bpk__gyv = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    ynjko__imaud = c.pyapi.call_method(vajv__zttzs, 'Index', (nifeu__xen,
        hrs__iwn, bpk__gyv, eeath__hzscd))
    c.pyapi.decref(nifeu__xen)
    c.pyapi.decref(hrs__iwn)
    c.pyapi.decref(bpk__gyv)
    c.pyapi.decref(eeath__hzscd)
    c.pyapi.decref(vajv__zttzs)
    c.context.nrt.decref(c.builder, typ, val)
    return ynjko__imaud


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        bjaw__wfguv = signature.return_type
        ipeir__oljvy = cgutils.create_struct_proxy(bjaw__wfguv)(context,
            builder)
        ipeir__oljvy.data = args[0]
        ipeir__oljvy.name = args[1]
        context.nrt.incref(builder, bjaw__wfguv.data, args[0])
        context.nrt.incref(builder, bjaw__wfguv.name_typ, args[1])
        return ipeir__oljvy._getvalue()
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
    zkvnu__sff = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in zkvnu__sff:
        init_func = zkvnu__sff[type(I)]
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
    sju__opy = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index, RangeIndexType: bodo.
        hiframes.pd_index_ext.init_range_index}
    if type(I) in sju__opy:
        return sju__opy[type(I)]
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
    jfrpe__coltw = get_index_constructor(I)

    def impl(I):
        qngf__jwi = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        zwscn__mcz = bodo.libs.array_kernels.unique(qngf__jwi)
        return jfrpe__coltw(zwscn__mcz, name)
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
        qngf__jwi = bodo.hiframes.pd_index_ext.get_index_data(I)
        uqhku__xjnf = bodo.libs.array_kernels.nunique(qngf__jwi, dropna)
        return uqhku__xjnf
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
            bbnq__oysz = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_index_ext.get_index_data(I)
            uqhku__xjnf = len(A)
            dkr__tkltg = np.empty(uqhku__xjnf, np.bool_)
            bodo.libs.array.array_isin(dkr__tkltg, A, bbnq__oysz, False)
            return dkr__tkltg
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        dkr__tkltg = bodo.libs.array_ops.array_op_isin(A, values)
        return dkr__tkltg
    return impl


@overload_method(RangeIndexType, 'isin', no_unliteral=True)
def overload_range_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            bbnq__oysz = bodo.utils.conversion.coerce_to_array(values)
            A = np.arange(I.start, I.stop, I.step)
            uqhku__xjnf = len(A)
            dkr__tkltg = np.empty(uqhku__xjnf, np.bool_)
            bodo.libs.array.array_isin(dkr__tkltg, A, bbnq__oysz, False)
            return dkr__tkltg
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Index.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = np.arange(I.start, I.stop, I.step)
        dkr__tkltg = bodo.libs.array_ops.array_op_isin(A, values)
        return dkr__tkltg
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
    mlb__gfwl = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, mlb__gfwl])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    mlb__gfwl = context.get_constant_null(types.DictType(types.int64, types
        .int64))
    return lir.Constant.literal_struct([data, name, mlb__gfwl])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    mlb__gfwl = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, mlb__gfwl])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    qitd__jauma = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, qitd__jauma, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    mlb__gfwl = context.get_constant_null(types.DictType(scalar_type, types
        .int64))
    return lir.Constant.literal_struct([data, name, mlb__gfwl])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [yyfo__lpzvp] = sig.args
    [ipz__mfano] = args
    zanr__wxb = context.make_helper(builder, yyfo__lpzvp, value=ipz__mfano)
    qjt__ssm = context.make_helper(builder, sig.return_type)
    hakda__zsdki = cgutils.alloca_once_value(builder, zanr__wxb.start)
    vsrgm__kejm = context.get_constant(types.intp, 0)
    jql__qbqgj = cgutils.alloca_once_value(builder, vsrgm__kejm)
    qjt__ssm.iter = hakda__zsdki
    qjt__ssm.stop = zanr__wxb.stop
    qjt__ssm.step = zanr__wxb.step
    qjt__ssm.count = jql__qbqgj
    chxwh__ngei = builder.sub(zanr__wxb.stop, zanr__wxb.start)
    kyzf__guqm = context.get_constant(types.intp, 1)
    jeqm__ndmym = builder.icmp_signed('>', chxwh__ngei, vsrgm__kejm)
    dtp__kmgq = builder.icmp_signed('>', zanr__wxb.step, vsrgm__kejm)
    gjic__sbi = builder.not_(builder.xor(jeqm__ndmym, dtp__kmgq))
    with builder.if_then(gjic__sbi):
        kmj__zzz = builder.srem(chxwh__ngei, zanr__wxb.step)
        kmj__zzz = builder.select(jeqm__ndmym, kmj__zzz, builder.neg(kmj__zzz))
        khk__rfwy = builder.icmp_signed('>', kmj__zzz, vsrgm__kejm)
        zxiu__olmi = builder.add(builder.sdiv(chxwh__ngei, zanr__wxb.step),
            builder.select(khk__rfwy, kyzf__guqm, vsrgm__kejm))
        builder.store(zxiu__olmi, jql__qbqgj)
    ipt__alvhr = qjt__ssm._getvalue()
    tywo__bgbip = impl_ret_new_ref(context, builder, sig.return_type,
        ipt__alvhr)
    return tywo__bgbip


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
    for mzcv__mohw in index_unsupported_methods:
        for ytg__eolus, typ in index_types:
            overload_method(typ, mzcv__mohw, no_unliteral=True)(
                create_unsupported_overload(ytg__eolus.format(mzcv__mohw +
                '()')))
    for eao__bdrkq in index_unsupported_atrs:
        for ytg__eolus, typ in index_types:
            overload_attribute(typ, eao__bdrkq, no_unliteral=True)(
                create_unsupported_overload(ytg__eolus.format(eao__bdrkq)))
    echwc__audo = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    aodpr__hidkv = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods)]
    for typ, rgv__rfy in aodpr__hidkv:
        ytg__eolus = idx_typ_to_format_str_map[typ]
        for obu__qcr in rgv__rfy:
            overload_method(typ, obu__qcr, no_unliteral=True)(
                create_unsupported_overload(ytg__eolus.format(obu__qcr + '()'))
                )
    for typ, qhpo__crw in echwc__audo:
        ytg__eolus = idx_typ_to_format_str_map[typ]
        for eao__bdrkq in qhpo__crw:
            overload_attribute(typ, eao__bdrkq, no_unliteral=True)(
                create_unsupported_overload(ytg__eolus.format(eao__bdrkq)))
    for csbxv__cwahe in [RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, MultiIndexType]:
        for obu__qcr in ['max', 'min']:
            ytg__eolus = idx_typ_to_format_str_map[csbxv__cwahe]
            overload_method(csbxv__cwahe, obu__qcr, no_unliteral=True)(
                create_unsupported_overload(ytg__eolus.format(obu__qcr + '()'))
                )


_install_index_unsupported()
