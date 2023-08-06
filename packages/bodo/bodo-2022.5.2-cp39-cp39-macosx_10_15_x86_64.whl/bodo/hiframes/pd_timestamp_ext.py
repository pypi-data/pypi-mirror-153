"""Timestamp extension for Pandas Timestamp with timezone support."""
import calendar
import datetime
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import ConcreteTemplate, infer_global, signature
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo.libs.str_ext
import bodo.utils.utils
from bodo.hiframes.datetime_date_ext import DatetimeDateType, _ord2ymd, _ymd2ord, get_isocalendar
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, _no_input, datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdatetime_ext
from bodo.libs.pd_datetime_arr_ext import get_pytz_type_info
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import BodoError, check_unsupported_args, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_iterable_type, is_overload_constant_int, is_overload_constant_str, is_overload_none, raise_bodo_error
ll.add_symbol('extract_year_days', hdatetime_ext.extract_year_days)
ll.add_symbol('get_month_day', hdatetime_ext.get_month_day)
ll.add_symbol('npy_datetimestruct_to_datetime', hdatetime_ext.
    npy_datetimestruct_to_datetime)
npy_datetimestruct_to_datetime = types.ExternalFunction(
    'npy_datetimestruct_to_datetime', types.int64(types.int64, types.int32,
    types.int32, types.int32, types.int32, types.int32, types.int32))
date_fields = ['year', 'month', 'day', 'hour', 'minute', 'second',
    'microsecond', 'nanosecond', 'quarter', 'dayofyear', 'day_of_year',
    'dayofweek', 'day_of_week', 'daysinmonth', 'days_in_month',
    'is_leap_year', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end', 'week', 'weekofyear',
    'weekday']
date_methods = ['normalize', 'day_name', 'month_name']
timedelta_fields = ['days', 'seconds', 'microseconds', 'nanoseconds']
timedelta_methods = ['total_seconds', 'to_pytimedelta']
iNaT = pd._libs.tslibs.iNaT


class PandasTimestampType(types.Type):

    def __init__(self, tz_val=None):
        self.tz = tz_val
        if tz_val is None:
            xkjy__bfrx = 'PandasTimestampType()'
        else:
            xkjy__bfrx = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=xkjy__bfrx)


pd_timestamp_type = PandasTimestampType()


def check_tz_aware_unsupported(val, func_name):
    if isinstance(val, bodo.hiframes.series_dt_impl.
        SeriesDatetimePropertiesType):
        val = val.stype
    if isinstance(val, PandasTimestampType) and val.tz is not None:
        raise BodoError(
            f'{func_name} on Timezone-aware timestamp not yet supported. Please convert to timezone naive with ts.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware array not yet supported. Please convert to timezone naive with arr.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeIndexType) and isinstance(val.data,
        bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware index not yet supported. Please convert to timezone naive with index.tz_convert(None)'
            )
    elif isinstance(val, bodo.SeriesType) and isinstance(val.data, bodo.
        DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware series not yet supported. Please convert to timezone naive with series.dt.tz_convert(None)'
            )
    elif isinstance(val, bodo.DataFrameType):
        for dkgqa__xhbz in val.data:
            if isinstance(dkgqa__xhbz, bodo.DatetimeArrayType):
                raise BodoError(
                    f'{func_name} on Timezone-aware columns not yet supported. Please convert each column to timezone naive with series.dt.tz_convert(None)'
                    )


@typeof_impl.register(pd.Timestamp)
def typeof_pd_timestamp(val, c):
    return PandasTimestampType(get_pytz_type_info(val.tz) if val.tz else None)


ts_field_typ = types.int64


@register_model(PandasTimestampType)
class PandasTimestampModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        epjlc__hbo = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, epjlc__hbo)


make_attribute_wrapper(PandasTimestampType, 'year', 'year')
make_attribute_wrapper(PandasTimestampType, 'month', 'month')
make_attribute_wrapper(PandasTimestampType, 'day', 'day')
make_attribute_wrapper(PandasTimestampType, 'hour', 'hour')
make_attribute_wrapper(PandasTimestampType, 'minute', 'minute')
make_attribute_wrapper(PandasTimestampType, 'second', 'second')
make_attribute_wrapper(PandasTimestampType, 'microsecond', 'microsecond')
make_attribute_wrapper(PandasTimestampType, 'nanosecond', 'nanosecond')
make_attribute_wrapper(PandasTimestampType, 'value', 'value')


@unbox(PandasTimestampType)
def unbox_pandas_timestamp(typ, val, c):
    jchd__qmpyo = c.pyapi.object_getattr_string(val, 'year')
    hghoh__qaq = c.pyapi.object_getattr_string(val, 'month')
    kjom__amdo = c.pyapi.object_getattr_string(val, 'day')
    fso__bpqh = c.pyapi.object_getattr_string(val, 'hour')
    sbwk__ynlhy = c.pyapi.object_getattr_string(val, 'minute')
    qddpe__oub = c.pyapi.object_getattr_string(val, 'second')
    calqe__qvv = c.pyapi.object_getattr_string(val, 'microsecond')
    zots__bhmvl = c.pyapi.object_getattr_string(val, 'nanosecond')
    axkdb__vni = c.pyapi.object_getattr_string(val, 'value')
    eepp__kuz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    eepp__kuz.year = c.pyapi.long_as_longlong(jchd__qmpyo)
    eepp__kuz.month = c.pyapi.long_as_longlong(hghoh__qaq)
    eepp__kuz.day = c.pyapi.long_as_longlong(kjom__amdo)
    eepp__kuz.hour = c.pyapi.long_as_longlong(fso__bpqh)
    eepp__kuz.minute = c.pyapi.long_as_longlong(sbwk__ynlhy)
    eepp__kuz.second = c.pyapi.long_as_longlong(qddpe__oub)
    eepp__kuz.microsecond = c.pyapi.long_as_longlong(calqe__qvv)
    eepp__kuz.nanosecond = c.pyapi.long_as_longlong(zots__bhmvl)
    eepp__kuz.value = c.pyapi.long_as_longlong(axkdb__vni)
    c.pyapi.decref(jchd__qmpyo)
    c.pyapi.decref(hghoh__qaq)
    c.pyapi.decref(kjom__amdo)
    c.pyapi.decref(fso__bpqh)
    c.pyapi.decref(sbwk__ynlhy)
    c.pyapi.decref(qddpe__oub)
    c.pyapi.decref(calqe__qvv)
    c.pyapi.decref(zots__bhmvl)
    c.pyapi.decref(axkdb__vni)
    mxhdq__feyb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(eepp__kuz._getvalue(), is_error=mxhdq__feyb)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    zpa__atidh = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jchd__qmpyo = c.pyapi.long_from_longlong(zpa__atidh.year)
    hghoh__qaq = c.pyapi.long_from_longlong(zpa__atidh.month)
    kjom__amdo = c.pyapi.long_from_longlong(zpa__atidh.day)
    fso__bpqh = c.pyapi.long_from_longlong(zpa__atidh.hour)
    sbwk__ynlhy = c.pyapi.long_from_longlong(zpa__atidh.minute)
    qddpe__oub = c.pyapi.long_from_longlong(zpa__atidh.second)
    ver__zgun = c.pyapi.long_from_longlong(zpa__atidh.microsecond)
    eyf__sfrdi = c.pyapi.long_from_longlong(zpa__atidh.nanosecond)
    pgqpa__eqw = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(pgqpa__eqw, (jchd__qmpyo,
            hghoh__qaq, kjom__amdo, fso__bpqh, sbwk__ynlhy, qddpe__oub,
            ver__zgun, eyf__sfrdi))
    else:
        if isinstance(typ.tz, int):
            kkbx__ofzmj = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            muki__vdsj = c.context.insert_const_string(c.builder.module,
                str(typ.tz))
            kkbx__ofzmj = c.pyapi.string_from_string(muki__vdsj)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', jchd__qmpyo), ('month',
            hghoh__qaq), ('day', kjom__amdo), ('hour', fso__bpqh), (
            'minute', sbwk__ynlhy), ('second', qddpe__oub), ('microsecond',
            ver__zgun), ('nanosecond', eyf__sfrdi), ('tz', kkbx__ofzmj)])
        res = c.pyapi.call(pgqpa__eqw, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(kkbx__ofzmj)
    c.pyapi.decref(jchd__qmpyo)
    c.pyapi.decref(hghoh__qaq)
    c.pyapi.decref(kjom__amdo)
    c.pyapi.decref(fso__bpqh)
    c.pyapi.decref(sbwk__ynlhy)
    c.pyapi.decref(qddpe__oub)
    c.pyapi.decref(ver__zgun)
    c.pyapi.decref(eyf__sfrdi)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, amudd__tga, iuz__ebsqi,
            value, wfqi__lwlh) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = amudd__tga
        ts.nanosecond = iuz__ebsqi
        ts.value = value
        return ts._getvalue()
    if is_overload_none(tz):
        typ = pd_timestamp_type
    elif is_overload_constant_str(tz):
        typ = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        typ = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error('tz must be a constant string, int, or None')
    return typ(types.int64, types.int64, types.int64, types.int64, types.
        int64, types.int64, types.int64, types.int64, types.int64, tz), codegen


@numba.generated_jit
def zero_if_none(value):
    if value == types.none:
        return lambda value: 0
    return lambda value: value


@lower_constant(PandasTimestampType)
def constant_timestamp(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    nanosecond = context.get_constant(types.int64, pyval.nanosecond)
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct((year, month, day, hour, minute,
        second, microsecond, nanosecond, value))


@overload(pd.Timestamp, no_unliteral=True)
def overload_pd_timestamp(ts_input=_no_input, freq=None, tz=None, unit=None,
    year=None, month=None, day=None, hour=None, minute=None, second=None,
    microsecond=None, nanosecond=None, tzinfo=None):
    if not is_overload_none(tz) and is_overload_constant_str(tz
        ) and get_overload_const_str(tz) not in pytz.all_timezones_set:
        raise BodoError(
            "pandas.Timestamp(): 'tz', if provided, must be constant string found in pytz.all_timezones"
            )
    if ts_input == _no_input or getattr(ts_input, 'value', None) == _no_input:

        def impl_kw(ts_input=_no_input, freq=None, tz=None, unit=None, year
            =None, month=None, day=None, hour=None, minute=None, second=
            None, microsecond=None, nanosecond=None, tzinfo=None):
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, tz)
        return impl_kw
    if isinstance(types.unliteral(freq), types.Integer):

        def impl_pos(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = npy_datetimestruct_to_datetime(ts_input, freq, tz,
                zero_if_none(unit), zero_if_none(year), zero_if_none(month),
                zero_if_none(day))
            value += zero_if_none(hour)
            return init_timestamp(ts_input, freq, tz, zero_if_none(unit),
                zero_if_none(year), zero_if_none(month), zero_if_none(day),
                zero_if_none(hour), value, None)
        return impl_pos
    if isinstance(ts_input, types.Number):
        if is_overload_none(unit):
            unit = 'ns'
        if not is_overload_constant_str(unit):
            raise BodoError(
                'pandas.Timedelta(): unit argument must be a constant str')
        unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
            get_overload_const_str(unit))
        xxhd__kaxy, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * xxhd__kaxy
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            cyusi__sis = np.int64(ts_input)
            zov__phq = ts_input - cyusi__sis
            if precision:
                zov__phq = np.round(zov__phq, precision)
            value = cyusi__sis * xxhd__kaxy + np.int64(zov__phq * xxhd__kaxy)
            return convert_val_to_timestamp(value, tz)
        return impl_float
    if ts_input == bodo.string_type or is_overload_constant_str(ts_input):
        types.pd_timestamp_type = pd_timestamp_type
        if is_overload_none(tz):
            tz_val = None
        elif is_overload_constant_str(tz):
            tz_val = get_overload_const_str(tz)
        else:
            raise_bodo_error(
                'pandas.Timestamp(): tz argument must be a constant string or None'
                )
        typ = PandasTimestampType(tz_val)

        def impl_str(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            with numba.objmode(res=typ):
                res = pd.Timestamp(ts_input, tz=tz)
            return res
        return impl_str
    if ts_input == pd_timestamp_type:
        return (lambda ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None: ts_input)
    if ts_input == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:

        def impl_datetime(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            hour = ts_input.hour
            minute = ts_input.minute
            second = ts_input.second
            microsecond = ts_input.microsecond
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, tz)
        return impl_datetime
    if ts_input == bodo.hiframes.datetime_date_ext.datetime_date_type:

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, None)
        return impl_date
    if isinstance(ts_input, numba.core.types.scalars.NPDatetime):
        xxhd__kaxy, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * xxhd__kaxy
            return convert_datetime64_to_timestamp(integer_to_dt64(value))
        return impl_date


@overload_attribute(PandasTimestampType, 'dayofyear')
@overload_attribute(PandasTimestampType, 'day_of_year')
def overload_pd_dayofyear(ptt):

    def pd_dayofyear(ptt):
        return get_day_of_year(ptt.year, ptt.month, ptt.day)
    return pd_dayofyear


@overload_method(PandasTimestampType, 'weekday')
@overload_attribute(PandasTimestampType, 'dayofweek')
@overload_attribute(PandasTimestampType, 'day_of_week')
def overload_pd_dayofweek(ptt):

    def pd_dayofweek(ptt):
        return get_day_of_week(ptt.year, ptt.month, ptt.day)
    return pd_dayofweek


@overload_attribute(PandasTimestampType, 'week')
@overload_attribute(PandasTimestampType, 'weekofyear')
def overload_week_number(ptt):

    def pd_week_number(ptt):
        wfqi__lwlh, vjx__zqd, wfqi__lwlh = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return vjx__zqd
    return pd_week_number


@overload_method(PandasTimestampType, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(val.value)


@overload_attribute(PandasTimestampType, 'days_in_month')
@overload_attribute(PandasTimestampType, 'daysinmonth')
def overload_pd_daysinmonth(ptt):

    def pd_daysinmonth(ptt):
        return get_days_in_month(ptt.year, ptt.month)
    return pd_daysinmonth


@overload_attribute(PandasTimestampType, 'is_leap_year')
def overload_pd_is_leap_year(ptt):

    def pd_is_leap_year(ptt):
        return is_leap_year(ptt.year)
    return pd_is_leap_year


@overload_attribute(PandasTimestampType, 'is_month_start')
def overload_pd_is_month_start(ptt):

    def pd_is_month_start(ptt):
        return ptt.day == 1
    return pd_is_month_start


@overload_attribute(PandasTimestampType, 'is_month_end')
def overload_pd_is_month_end(ptt):

    def pd_is_month_end(ptt):
        return ptt.day == get_days_in_month(ptt.year, ptt.month)
    return pd_is_month_end


@overload_attribute(PandasTimestampType, 'is_quarter_start')
def overload_pd_is_quarter_start(ptt):

    def pd_is_quarter_start(ptt):
        return ptt.day == 1 and ptt.month % 3 == 1
    return pd_is_quarter_start


@overload_attribute(PandasTimestampType, 'is_quarter_end')
def overload_pd_is_quarter_end(ptt):

    def pd_is_quarter_end(ptt):
        return ptt.month % 3 == 0 and ptt.day == get_days_in_month(ptt.year,
            ptt.month)
    return pd_is_quarter_end


@overload_attribute(PandasTimestampType, 'is_year_start')
def overload_pd_is_year_start(ptt):

    def pd_is_year_start(ptt):
        return ptt.day == 1 and ptt.month == 1
    return pd_is_year_start


@overload_attribute(PandasTimestampType, 'is_year_end')
def overload_pd_is_year_end(ptt):

    def pd_is_year_end(ptt):
        return ptt.day == 31 and ptt.month == 12
    return pd_is_year_end


@overload_attribute(PandasTimestampType, 'quarter')
def overload_quarter(ptt):

    def quarter(ptt):
        return (ptt.month - 1) // 3 + 1
    return quarter


@overload_method(PandasTimestampType, 'date', no_unliteral=True)
def overload_pd_timestamp_date(ptt):

    def pd_timestamp_date_impl(ptt):
        return datetime.date(ptt.year, ptt.month, ptt.day)
    return pd_timestamp_date_impl


@overload_method(PandasTimestampType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(ptt):

    def impl(ptt):
        year, vjx__zqd, uzl__knvg = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, vjx__zqd, uzl__knvg
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            gcb__ortij = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + gcb__ortij
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            gcb__ortij = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + gcb__ortij
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    puf__bqzy = dict(locale=locale)
    tqx__vnoe = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', puf__bqzy, tqx__vnoe,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        ygoz__nxbqg = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
        wfqi__lwlh, wfqi__lwlh, qbwsh__dpvf = ptt.isocalendar()
        return ygoz__nxbqg[qbwsh__dpvf - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    puf__bqzy = dict(locale=locale)
    tqx__vnoe = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', puf__bqzy, tqx__vnoe,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        lwam__pbnb = ('January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November',
            'December')
        return lwam__pbnb[ptt.month - 1]
    return impl


@overload_method(PandasTimestampType, 'tz_convert', no_unliteral=True)
def overload_pd_timestamp_tz_convert(ptt, tz):
    if ptt.tz is None:
        raise BodoError(
            'Cannot convert tz-naive Timestamp, use tz_localize to localize')
    if is_overload_none(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value)
    elif is_overload_constant_str(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value, tz=tz)


@overload_method(PandasTimestampType, 'tz_localize', no_unliteral=True)
def overload_pd_timestamp_tz_localize(ptt, tz, ambiguous='raise',
    nonexistent='raise'):
    if ptt.tz is not None and not is_overload_none(tz):
        raise BodoError(
            'Cannot localize tz-aware Timestamp, use tz_convert for conversions'
            )
    puf__bqzy = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    dks__byluc = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', puf__bqzy, dks__byluc,
        package_name='pandas', module_name='Timestamp')
    if is_overload_none(tz):
        return (lambda ptt, tz, ambiguous='raise', nonexistent='raise':
            convert_val_to_timestamp(ptt.value, is_convert=False))
    elif is_overload_constant_str(tz):
        return (lambda ptt, tz, ambiguous='raise', nonexistent='raise':
            convert_val_to_timestamp(ptt.value, tz=tz, is_convert=False))


@numba.njit
def str_2d(a):
    res = str(a)
    if len(res) == 1:
        return '0' + res
    return res


@overload(str, no_unliteral=True)
def ts_str_overload(a):
    if a == pd_timestamp_type:
        return lambda a: a.isoformat(' ')


@intrinsic
def extract_year_days(typingctx, dt64_t=None):
    assert dt64_t in (types.int64, types.NPDatetime('ns'))

    def codegen(context, builder, sig, args):
        hstxl__tzge = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], hstxl__tzge)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        adw__sjmdj = cgutils.alloca_once(builder, lir.IntType(64))
        smg__yentd = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        ulg__jys = cgutils.get_or_insert_function(builder.module,
            smg__yentd, name='extract_year_days')
        builder.call(ulg__jys, [hstxl__tzge, year, adw__sjmdj])
        return cgutils.pack_array(builder, [builder.load(hstxl__tzge),
            builder.load(year), builder.load(adw__sjmdj)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        smg__yentd = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        ulg__jys = cgutils.get_or_insert_function(builder.module,
            smg__yentd, name='get_month_day')
        builder.call(ulg__jys, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    dise__ouno = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 
        365, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    uum__qqmy = is_leap_year(year)
    dwsg__cfkp = dise__ouno[uum__qqmy * 13 + month - 1]
    fxlw__ndcdv = dwsg__cfkp + day
    return fxlw__ndcdv


@register_jitable
def get_day_of_week(y, m, d):
    mowxg__gctac = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + mowxg__gctac[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    eznt__rgk = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 31,
        30, 31, 30, 31, 31, 30, 31, 30, 31]
    return eznt__rgk[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    mur__ggisz = xaon__yjgz = np.array([])
    fqfd__bgd = '0'
    if is_overload_constant_str(tz):
        muki__vdsj = get_overload_const_str(tz)
        kkbx__ofzmj = pytz.timezone(muki__vdsj)
        if isinstance(kkbx__ofzmj, pytz.tzinfo.DstTzInfo):
            mur__ggisz = np.array(kkbx__ofzmj._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            xaon__yjgz = np.array(kkbx__ofzmj._transition_info)[:, 0]
            xaon__yjgz = (pd.Series(xaon__yjgz).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            fqfd__bgd = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            xaon__yjgz = np.int64(kkbx__ofzmj._utcoffset.total_seconds() * 
                1000000000)
            fqfd__bgd = 'deltas'
    elif is_overload_constant_int(tz):
        voxj__jfq = get_overload_const_int(tz)
        fqfd__bgd = str(voxj__jfq)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        orc__hlxh = 'tz_ts_input'
        dkasd__nwm = 'ts_input'
    else:
        orc__hlxh = 'ts_input'
        dkasd__nwm = 'tz_ts_input'
    qukzi__pdw = 'def impl(ts_input, tz=None, is_convert=True):\n'
    qukzi__pdw += f'  tz_ts_input = ts_input + {fqfd__bgd}\n'
    qukzi__pdw += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({orc__hlxh}))\n'
        )
    qukzi__pdw += '  month, day = get_month_day(year, days)\n'
    qukzi__pdw += '  return init_timestamp(\n'
    qukzi__pdw += '    year=year,\n'
    qukzi__pdw += '    month=month,\n'
    qukzi__pdw += '    day=day,\n'
    qukzi__pdw += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    qukzi__pdw += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    qukzi__pdw += '    second=(dt // 1_000_000_000) % 60,\n'
    qukzi__pdw += '    microsecond=(dt // 1000) % 1_000_000,\n'
    qukzi__pdw += '    nanosecond=dt % 1000,\n'
    qukzi__pdw += f'    value={dkasd__nwm},\n'
    qukzi__pdw += '    tz=tz,\n'
    qukzi__pdw += '  )\n'
    cfibz__vlm = {}
    exec(qukzi__pdw, {'np': np, 'pd': pd, 'trans': mur__ggisz, 'deltas':
        xaon__yjgz, 'integer_to_dt64': integer_to_dt64, 'extract_year_days':
        extract_year_days, 'get_month_day': get_month_day, 'init_timestamp':
        init_timestamp, 'zero_if_none': zero_if_none}, cfibz__vlm)
    impl = cfibz__vlm['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    hstxl__tzge, year, adw__sjmdj = extract_year_days(dt64)
    month, day = get_month_day(year, adw__sjmdj)
    return init_timestamp(year=year, month=month, day=day, hour=hstxl__tzge //
        (60 * 60 * 1000000000), minute=hstxl__tzge // (60 * 1000000000) % 
        60, second=hstxl__tzge // 1000000000 % 60, microsecond=hstxl__tzge //
        1000 % 1000000, nanosecond=hstxl__tzge % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    qpos__tsl = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    btqad__nik = qpos__tsl // (86400 * 1000000000)
    rkk__pww = qpos__tsl - btqad__nik * 86400 * 1000000000
    pzgh__qfpjv = rkk__pww // 1000000000
    qhl__wqu = rkk__pww - pzgh__qfpjv * 1000000000
    ksb__osju = qhl__wqu // 1000
    return datetime.timedelta(btqad__nik, pzgh__qfpjv, ksb__osju)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    qpos__tsl = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(qpos__tsl)


@intrinsic
def integer_to_timedelta64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPTimedelta('ns')(val), codegen


@intrinsic
def integer_to_dt64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPDatetime('ns')(val), codegen


@intrinsic
def dt64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(types.NPDatetime('ns'), types.int64)
def cast_dt64_to_integer(context, builder, fromty, toty, val):
    return val


@overload_method(types.NPDatetime, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@overload_method(types.NPTimedelta, '__hash__', no_unliteral=True)
def td64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@intrinsic
def timedelta64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(bodo.timedelta64ns, types.int64)
def cast_td64_to_integer(context, builder, fromty, toty, val):
    return val


@numba.njit
def parse_datetime_str(val):
    with numba.objmode(res='int64'):
        res = pd.Timestamp(val).value
    return integer_to_dt64(res)


@numba.njit
def datetime_timedelta_to_timedelta64(val):
    with numba.objmode(res='NPTimedelta("ns")'):
        res = pd.to_timedelta(val)
        res = res.to_timedelta64()
    return res


@numba.njit
def series_str_dt64_astype(data):
    with numba.objmode(res="NPDatetime('ns')[::1]"):
        res = pd.Series(data).astype('datetime64[ns]').values
    return res


@numba.njit
def series_str_td64_astype(data):
    with numba.objmode(res="NPTimedelta('ns')[::1]"):
        res = data.astype('timedelta64[ns]')
    return res


@numba.njit
def datetime_datetime_to_dt64(val):
    with numba.objmode(res='NPDatetime("ns")'):
        res = np.datetime64(val).astype('datetime64[ns]')
    return res


@register_jitable
def datetime_date_arr_to_dt64_arr(arr):
    with numba.objmode(res='NPDatetime("ns")[::1]'):
        res = np.array(arr, dtype='datetime64[ns]')
    return res


types.pd_timestamp_type = pd_timestamp_type


@register_jitable
def to_datetime_scalar(a, errors='raise', dayfirst=False, yearfirst=False,
    utc=None, format=None, exact=True, unit=None, infer_datetime_format=
    False, origin='unix', cache=True):
    with numba.objmode(t='pd_timestamp_type'):
        t = pd.to_datetime(a, errors=errors, dayfirst=dayfirst, yearfirst=
            yearfirst, utc=utc, format=format, exact=exact, unit=unit,
            infer_datetime_format=infer_datetime_format, origin=origin,
            cache=cache)
    return t


@numba.njit
def pandas_string_array_to_datetime(arr, errors, dayfirst, yearfirst, utc,
    format, exact, unit, infer_datetime_format, origin, cache):
    with numba.objmode(result='datetime_index'):
        result = pd.to_datetime(arr, errors=errors, dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
    return result


@numba.njit
def pandas_dict_string_array_to_datetime(arr, errors, dayfirst, yearfirst,
    utc, format, exact, unit, infer_datetime_format, origin, cache):
    lcwlk__wcqdf = len(arr)
    pid__dkei = np.empty(lcwlk__wcqdf, 'datetime64[ns]')
    zkz__znq = arr._indices
    ogcf__munsm = pandas_string_array_to_datetime(arr._data, errors,
        dayfirst, yearfirst, utc, format, exact, unit,
        infer_datetime_format, origin, cache).values
    for ehw__sbtk in range(lcwlk__wcqdf):
        if bodo.libs.array_kernels.isna(zkz__znq, ehw__sbtk):
            bodo.libs.array_kernels.setna(pid__dkei, ehw__sbtk)
            continue
        pid__dkei[ehw__sbtk] = ogcf__munsm[zkz__znq[ehw__sbtk]]
    return pid__dkei


@overload(pd.to_datetime, inline='always', no_unliteral=True)
def overload_to_datetime(arg_a, errors='raise', dayfirst=False, yearfirst=
    False, utc=None, format=None, exact=True, unit=None,
    infer_datetime_format=False, origin='unix', cache=True):
    if arg_a == bodo.string_type or is_overload_constant_str(arg_a
        ) or is_overload_constant_int(arg_a) or isinstance(arg_a, types.Integer
        ):

        def pd_to_datetime_impl(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return to_datetime_scalar(arg_a, errors=errors, dayfirst=
                dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                exact=exact, unit=unit, infer_datetime_format=
                infer_datetime_format, origin=origin, cache=cache)
        return pd_to_datetime_impl
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            smzu__nvrpq = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            xkjy__bfrx = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ivsr__zwxxy = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(ivsr__zwxxy,
                smzu__nvrpq, xkjy__bfrx)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        ptzk__kzyop = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            lcwlk__wcqdf = len(arg_a)
            pid__dkei = np.empty(lcwlk__wcqdf, ptzk__kzyop)
            for ehw__sbtk in numba.parfors.parfor.internal_prange(lcwlk__wcqdf
                ):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, ehw__sbtk):
                    data = arg_a[ehw__sbtk]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                pid__dkei[ehw__sbtk
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(pid__dkei,
                None)
        return impl_date_arr
    if arg_a == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return (lambda arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True: bodo.
            hiframes.pd_index_ext.init_datetime_index(arg_a, None))
    if arg_a == string_array_type:

        def impl_string_array(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pandas_string_array_to_datetime(arg_a, errors, dayfirst,
                yearfirst, utc, format, exact, unit, infer_datetime_format,
                origin, cache)
        return impl_string_array
    if isinstance(arg_a, types.Array) and isinstance(arg_a.dtype, types.Integer
        ):
        ptzk__kzyop = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            lcwlk__wcqdf = len(arg_a)
            pid__dkei = np.empty(lcwlk__wcqdf, ptzk__kzyop)
            for ehw__sbtk in numba.parfors.parfor.internal_prange(lcwlk__wcqdf
                ):
                data = arg_a[ehw__sbtk]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                pid__dkei[ehw__sbtk
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(pid__dkei,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        ptzk__kzyop = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            lcwlk__wcqdf = len(arg_a)
            pid__dkei = np.empty(lcwlk__wcqdf, ptzk__kzyop)
            ybuw__mgz = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            ogcf__munsm = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for ehw__sbtk in numba.parfors.parfor.internal_prange(lcwlk__wcqdf
                ):
                c = ybuw__mgz[ehw__sbtk]
                if c == -1:
                    bodo.libs.array_kernels.setna(pid__dkei, ehw__sbtk)
                    continue
                pid__dkei[ehw__sbtk] = ogcf__munsm[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(pid__dkei,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            pid__dkei = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(pid__dkei,
                None)
        return impl_dict_str_arr
    if isinstance(arg_a, PandasTimestampType):

        def impl_timestamp(arg_a, errors='raise', dayfirst=False, yearfirst
            =False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return arg_a
        return impl_timestamp
    raise_bodo_error(f'pd.to_datetime(): cannot convert date type {arg_a}')


@overload(pd.to_timedelta, inline='always', no_unliteral=True)
def overload_to_timedelta(arg_a, unit='ns', errors='raise'):
    if not is_overload_constant_str(unit):
        raise BodoError(
            'pandas.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, unit='ns', errors='raise'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            smzu__nvrpq = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            xkjy__bfrx = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ivsr__zwxxy = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(ivsr__zwxxy,
                smzu__nvrpq, xkjy__bfrx)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, worz__cwfwj = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, worz__cwfwj, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, wfqi__lwlh = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, worz__cwfwj = pd._libs.tslibs.conversion.precision_from_unit(unit)
        upc__pcpmw = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                lcwlk__wcqdf = len(arg_a)
                pid__dkei = np.empty(lcwlk__wcqdf, upc__pcpmw)
                for ehw__sbtk in numba.parfors.parfor.internal_prange(
                    lcwlk__wcqdf):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, ehw__sbtk):
                        val = float_to_timedelta_val(arg_a[ehw__sbtk],
                            worz__cwfwj, m)
                    pid__dkei[ehw__sbtk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    pid__dkei, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                lcwlk__wcqdf = len(arg_a)
                pid__dkei = np.empty(lcwlk__wcqdf, upc__pcpmw)
                for ehw__sbtk in numba.parfors.parfor.internal_prange(
                    lcwlk__wcqdf):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, ehw__sbtk):
                        val = arg_a[ehw__sbtk] * m
                    pid__dkei[ehw__sbtk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    pid__dkei, None)
            return impl_int
        if arg_a.dtype == bodo.timedelta64ns:

            def impl_td64(arg_a, unit='ns', errors='raise'):
                arr = bodo.utils.conversion.coerce_to_ndarray(arg_a)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(arr,
                    None)
            return impl_td64
        if arg_a.dtype == bodo.string_type or isinstance(arg_a.dtype, types
            .UnicodeCharSeq):

            def impl_str(arg_a, unit='ns', errors='raise'):
                return pandas_string_array_to_timedelta(arg_a, unit, errors)
            return impl_str
        if arg_a.dtype == datetime_timedelta_type:

            def impl_datetime_timedelta(arg_a, unit='ns', errors='raise'):
                lcwlk__wcqdf = len(arg_a)
                pid__dkei = np.empty(lcwlk__wcqdf, upc__pcpmw)
                for ehw__sbtk in numba.parfors.parfor.internal_prange(
                    lcwlk__wcqdf):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, ehw__sbtk):
                        ipbp__qpzk = arg_a[ehw__sbtk]
                        val = (ipbp__qpzk.microseconds + 1000 * 1000 * (
                            ipbp__qpzk.seconds + 24 * 60 * 60 * ipbp__qpzk.
                            days)) * 1000
                    pid__dkei[ehw__sbtk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    pid__dkei, None)
            return impl_datetime_timedelta
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    cyusi__sis = np.int64(data)
    zov__phq = data - cyusi__sis
    if precision:
        zov__phq = np.round(zov__phq, precision)
    return cyusi__sis * multiplier + np.int64(zov__phq * multiplier)


@numba.njit
def pandas_string_array_to_timedelta(arg_a, unit='ns', errors='raise'):
    with numba.objmode(result='timedelta_index'):
        result = pd.to_timedelta(arg_a, errors=errors)
    return result


def create_timestamp_cmp_op_overload(op):

    def overload_date_timestamp_cmp(lhs, rhs):
        if (lhs == pd_timestamp_type and rhs == bodo.hiframes.
            datetime_date_ext.datetime_date_type):
            return lambda lhs, rhs: op(lhs.value, bodo.hiframes.
                pd_timestamp_ext.npy_datetimestruct_to_datetime(rhs.year,
                rhs.month, rhs.day, 0, 0, 0, 0))
        if (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and 
            rhs == pd_timestamp_type):
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                npy_datetimestruct_to_datetime(lhs.year, lhs.month, lhs.day,
                0, 0, 0, 0), rhs.value)
        if lhs == pd_timestamp_type and rhs == pd_timestamp_type:
            return lambda lhs, rhs: op(lhs.value, rhs.value)
        if lhs == pd_timestamp_type and rhs == bodo.datetime64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(lhs.value), rhs)
        if lhs == bodo.datetime64ns and rhs == pd_timestamp_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(rhs.value))
    return overload_date_timestamp_cmp


@overload_method(PandasTimestampType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


def overload_freq_methods(method):

    def freq_overload(td, freq, ambiguous='raise', nonexistent='raise'):
        check_tz_aware_unsupported(td, f'Timestamp.{method}()')
        puf__bqzy = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        ledee__qtngw = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', puf__bqzy,
            ledee__qtngw, package_name='pandas', module_name='Timestamp')
        nkipb__apwyl = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        lhw__hus = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 1000,
            60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        qukzi__pdw = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for ehw__sbtk, hqqbt__hbi in enumerate(nkipb__apwyl):
            vmw__iawlz = 'if' if ehw__sbtk == 0 else 'elif'
            qukzi__pdw += '    {} {}:\n'.format(vmw__iawlz, hqqbt__hbi)
            qukzi__pdw += '        unit_value = {}\n'.format(lhw__hus[
                ehw__sbtk])
        qukzi__pdw += '    else:\n'
        qukzi__pdw += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            qukzi__pdw += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        elif td == pd_timestamp_type:
            if method == 'ceil':
                qukzi__pdw += (
                    '    value = td.value + np.remainder(-td.value, unit_value)\n'
                    )
            if method == 'floor':
                qukzi__pdw += (
                    '    value = td.value - np.remainder(td.value, unit_value)\n'
                    )
            if method == 'round':
                qukzi__pdw += '    if unit_value == 1:\n'
                qukzi__pdw += '        value = td.value\n'
                qukzi__pdw += '    else:\n'
                qukzi__pdw += (
                    '        quotient, remainder = np.divmod(td.value, unit_value)\n'
                    )
                qukzi__pdw += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                qukzi__pdw += '        if mask:\n'
                qukzi__pdw += '            quotient = quotient + 1\n'
                qukzi__pdw += '        value = quotient * unit_value\n'
            qukzi__pdw += '    return pd.Timestamp(value)\n'
        cfibz__vlm = {}
        exec(qukzi__pdw, {'np': np, 'pd': pd}, cfibz__vlm)
        impl = cfibz__vlm['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    tvfhr__qlc = ['ceil', 'floor', 'round']
    for method in tvfhr__qlc:
        xxp__kesb = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(xxp__kesb)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            xxp__kesb)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    jhpr__hzv = totmicrosec // 1000000
    second = jhpr__hzv % 60
    jjq__yfv = jhpr__hzv // 60
    minute = jjq__yfv % 60
    olpeu__sqj = jjq__yfv // 60
    hour = olpeu__sqj % 24
    bygh__lrs = olpeu__sqj // 24
    year, month, day = _ord2ymd(bygh__lrs)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            qem__ddsut = lhs.toordinal()
            mhiol__dadxs = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            jpe__rajqz = lhs.microsecond
            nanosecond = lhs.nanosecond
            syulj__fcd = rhs.days
            qbs__xlzg = rhs.seconds
            okdmm__sbq = rhs.microseconds
            rkp__nty = qem__ddsut - syulj__fcd
            pxz__uicq = mhiol__dadxs - qbs__xlzg
            hvzc__zoh = jpe__rajqz - okdmm__sbq
            totmicrosec = 1000000 * (rkp__nty * 86400 + pxz__uicq) + hvzc__zoh
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl_timestamp(lhs, rhs):
            return convert_numpy_timedelta64_to_pd_timedelta(lhs.value -
                rhs.value)
        return impl_timestamp
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


def overload_add_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            qem__ddsut = lhs.toordinal()
            mhiol__dadxs = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            jpe__rajqz = lhs.microsecond
            nanosecond = lhs.nanosecond
            syulj__fcd = rhs.days
            qbs__xlzg = rhs.seconds
            okdmm__sbq = rhs.microseconds
            rkp__nty = qem__ddsut + syulj__fcd
            pxz__uicq = mhiol__dadxs + qbs__xlzg
            hvzc__zoh = jpe__rajqz + okdmm__sbq
            totmicrosec = 1000000 * (rkp__nty * 86400 + pxz__uicq) + hvzc__zoh
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            qem__ddsut = lhs.toordinal()
            mhiol__dadxs = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            jpe__rajqz = lhs.microsecond
            citt__pxzy = lhs.nanosecond
            okdmm__sbq = rhs.value // 1000
            pejz__cln = rhs.nanoseconds
            hvzc__zoh = jpe__rajqz + okdmm__sbq
            totmicrosec = 1000000 * (qem__ddsut * 86400 + mhiol__dadxs
                ) + hvzc__zoh
            snjk__ngd = citt__pxzy + pejz__cln
            return compute_pd_timestamp(totmicrosec, snjk__ngd)
        return impl
    if (lhs == pd_timedelta_type and rhs == pd_timestamp_type or lhs ==
        datetime_timedelta_type and rhs == pd_timestamp_type):

        def impl(lhs, rhs):
            return rhs + lhs
        return impl


@overload(min, no_unliteral=True)
def timestamp_min(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.min()')
    check_tz_aware_unsupported(rhs, f'Timestamp.min()')
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def timestamp_max(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.max()')
    check_tz_aware_unsupported(rhs, f'Timestamp.max()')
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, 'strftime')
@overload_method(PandasTimestampType, 'strftime')
def strftime(ts, format):
    if isinstance(ts, DatetimeDateType):
        azre__axum = 'datetime.date'
    else:
        azre__axum = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{azre__axum}.strftime(): 'strftime' argument must be a string")

    def impl(ts, format):
        with numba.objmode(res='unicode_type'):
            res = ts.strftime(format)
        return res
    return impl


@overload_method(PandasTimestampType, 'to_datetime64')
def to_datetime64(ts):

    def impl(ts):
        return integer_to_dt64(ts.value)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='pd_timestamp_type'):
        d = pd.Timestamp.now()
    return d


class CompDT64(ConcreteTemplate):
    cases = [signature(types.boolean, types.NPDatetime('ns'), types.
        NPDatetime('ns'))]


@infer_global(operator.lt)
class CmpOpLt(CompDT64):
    key = operator.lt


@infer_global(operator.le)
class CmpOpLe(CompDT64):
    key = operator.le


@infer_global(operator.gt)
class CmpOpGt(CompDT64):
    key = operator.gt


@infer_global(operator.ge)
class CmpOpGe(CompDT64):
    key = operator.ge


@infer_global(operator.eq)
class CmpOpEq(CompDT64):
    key = operator.eq


@infer_global(operator.ne)
class CmpOpNe(CompDT64):
    key = operator.ne


@typeof_impl.register(calendar._localized_month)
def typeof_python_calendar(val, c):
    return types.Tuple([types.StringLiteral(bev__jxfj) for bev__jxfj in val])


@overload(str)
def overload_datetime64_str(val):
    if val == bodo.datetime64ns:

        def impl(val):
            return (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(val).isoformat('T'))
        return impl


timestamp_unsupported_attrs = ['asm8', 'components', 'freqstr', 'tz',
    'fold', 'tzinfo', 'freq']
timestamp_unsupported_methods = ['astimezone', 'ctime', 'dst', 'isoweekday',
    'replace', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz',
    'to_julian_date', 'to_numpy', 'to_period', 'to_pydatetime', 'tzname',
    'utcoffset', 'utctimetuple']


def _install_pd_timestamp_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for bxxtu__hzgdy in timestamp_unsupported_attrs:
        btoas__gvlgv = 'pandas.Timestamp.' + bxxtu__hzgdy
        overload_attribute(PandasTimestampType, bxxtu__hzgdy)(
            create_unsupported_overload(btoas__gvlgv))
    for ppad__bggep in timestamp_unsupported_methods:
        btoas__gvlgv = 'pandas.Timestamp.' + ppad__bggep
        overload_method(PandasTimestampType, ppad__bggep)(
            create_unsupported_overload(btoas__gvlgv + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass, pd_timestamp_type,
    types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
