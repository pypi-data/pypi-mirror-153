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
            afjot__aqth = 'PandasTimestampType()'
        else:
            afjot__aqth = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=afjot__aqth)


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
        for dnzcr__sxz in val.data:
            if isinstance(dnzcr__sxz, bodo.DatetimeArrayType):
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
        obns__ilxxs = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, obns__ilxxs)


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
    zjtm__bsi = c.pyapi.object_getattr_string(val, 'year')
    hxx__irk = c.pyapi.object_getattr_string(val, 'month')
    tgf__tevya = c.pyapi.object_getattr_string(val, 'day')
    zchzx__syek = c.pyapi.object_getattr_string(val, 'hour')
    colgc__foiil = c.pyapi.object_getattr_string(val, 'minute')
    spqkr__cebl = c.pyapi.object_getattr_string(val, 'second')
    ocot__afuii = c.pyapi.object_getattr_string(val, 'microsecond')
    aux__kspd = c.pyapi.object_getattr_string(val, 'nanosecond')
    qso__vxxt = c.pyapi.object_getattr_string(val, 'value')
    hwyo__cxbp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hwyo__cxbp.year = c.pyapi.long_as_longlong(zjtm__bsi)
    hwyo__cxbp.month = c.pyapi.long_as_longlong(hxx__irk)
    hwyo__cxbp.day = c.pyapi.long_as_longlong(tgf__tevya)
    hwyo__cxbp.hour = c.pyapi.long_as_longlong(zchzx__syek)
    hwyo__cxbp.minute = c.pyapi.long_as_longlong(colgc__foiil)
    hwyo__cxbp.second = c.pyapi.long_as_longlong(spqkr__cebl)
    hwyo__cxbp.microsecond = c.pyapi.long_as_longlong(ocot__afuii)
    hwyo__cxbp.nanosecond = c.pyapi.long_as_longlong(aux__kspd)
    hwyo__cxbp.value = c.pyapi.long_as_longlong(qso__vxxt)
    c.pyapi.decref(zjtm__bsi)
    c.pyapi.decref(hxx__irk)
    c.pyapi.decref(tgf__tevya)
    c.pyapi.decref(zchzx__syek)
    c.pyapi.decref(colgc__foiil)
    c.pyapi.decref(spqkr__cebl)
    c.pyapi.decref(ocot__afuii)
    c.pyapi.decref(aux__kspd)
    c.pyapi.decref(qso__vxxt)
    svn__ucq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hwyo__cxbp._getvalue(), is_error=svn__ucq)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    lrzg__peu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zjtm__bsi = c.pyapi.long_from_longlong(lrzg__peu.year)
    hxx__irk = c.pyapi.long_from_longlong(lrzg__peu.month)
    tgf__tevya = c.pyapi.long_from_longlong(lrzg__peu.day)
    zchzx__syek = c.pyapi.long_from_longlong(lrzg__peu.hour)
    colgc__foiil = c.pyapi.long_from_longlong(lrzg__peu.minute)
    spqkr__cebl = c.pyapi.long_from_longlong(lrzg__peu.second)
    hsdw__dzfo = c.pyapi.long_from_longlong(lrzg__peu.microsecond)
    uuv__xccr = c.pyapi.long_from_longlong(lrzg__peu.nanosecond)
    qbbto__afr = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(qbbto__afr, (zjtm__bsi,
            hxx__irk, tgf__tevya, zchzx__syek, colgc__foiil, spqkr__cebl,
            hsdw__dzfo, uuv__xccr))
    else:
        if isinstance(typ.tz, int):
            xians__dqf = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            nvnt__huvoc = c.context.insert_const_string(c.builder.module,
                str(typ.tz))
            xians__dqf = c.pyapi.string_from_string(nvnt__huvoc)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', zjtm__bsi), ('month', hxx__irk
            ), ('day', tgf__tevya), ('hour', zchzx__syek), ('minute',
            colgc__foiil), ('second', spqkr__cebl), ('microsecond',
            hsdw__dzfo), ('nanosecond', uuv__xccr), ('tz', xians__dqf)])
        res = c.pyapi.call(qbbto__afr, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(xians__dqf)
    c.pyapi.decref(zjtm__bsi)
    c.pyapi.decref(hxx__irk)
    c.pyapi.decref(tgf__tevya)
    c.pyapi.decref(zchzx__syek)
    c.pyapi.decref(colgc__foiil)
    c.pyapi.decref(spqkr__cebl)
    c.pyapi.decref(hsdw__dzfo)
    c.pyapi.decref(uuv__xccr)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, ptq__ccrsp, vktwd__uflas,
            value, ulr__ixu) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = ptq__ccrsp
        ts.nanosecond = vktwd__uflas
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
        xauk__lqpnh, precision = (pd._libs.tslibs.conversion.
            precision_from_unit(unit))
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * xauk__lqpnh
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            weaiz__exsg = np.int64(ts_input)
            hjcw__tdrg = ts_input - weaiz__exsg
            if precision:
                hjcw__tdrg = np.round(hjcw__tdrg, precision)
            value = weaiz__exsg * xauk__lqpnh + np.int64(hjcw__tdrg *
                xauk__lqpnh)
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
        xauk__lqpnh, precision = (pd._libs.tslibs.conversion.
            precision_from_unit(ts_input.unit))

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * xauk__lqpnh
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
        ulr__ixu, plic__rza, ulr__ixu = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return plic__rza
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
        year, plic__rza, wsvp__yamht = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, plic__rza, wsvp__yamht
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            zhrbc__sqx = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + zhrbc__sqx
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            zhrbc__sqx = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + zhrbc__sqx
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    azwzu__ixqqu = dict(locale=locale)
    gsj__agyh = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', azwzu__ixqqu, gsj__agyh,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        uepfa__ajy = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
        ulr__ixu, ulr__ixu, uekn__yhox = ptt.isocalendar()
        return uepfa__ajy[uekn__yhox - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    azwzu__ixqqu = dict(locale=locale)
    gsj__agyh = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', azwzu__ixqqu, gsj__agyh,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        flpj__cok = ('January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December')
        return flpj__cok[ptt.month - 1]
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
    azwzu__ixqqu = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    gkg__gbh = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', azwzu__ixqqu, gkg__gbh,
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
        rdhee__hly = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], rdhee__hly)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        dkyvy__utwjq = cgutils.alloca_once(builder, lir.IntType(64))
        clv__yvlxn = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        bcg__ytt = cgutils.get_or_insert_function(builder.module,
            clv__yvlxn, name='extract_year_days')
        builder.call(bcg__ytt, [rdhee__hly, year, dkyvy__utwjq])
        return cgutils.pack_array(builder, [builder.load(rdhee__hly),
            builder.load(year), builder.load(dkyvy__utwjq)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        clv__yvlxn = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        bcg__ytt = cgutils.get_or_insert_function(builder.module,
            clv__yvlxn, name='get_month_day')
        builder.call(bcg__ytt, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    kgct__opnse = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 
        365, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    sem__ekazy = is_leap_year(year)
    spxx__hrt = kgct__opnse[sem__ekazy * 13 + month - 1]
    krh__phqm = spxx__hrt + day
    return krh__phqm


@register_jitable
def get_day_of_week(y, m, d):
    cxt__kwope = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + cxt__kwope[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    tfu__awj = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 31,
        30, 31, 30, 31, 31, 30, 31, 30, 31]
    return tfu__awj[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    sww__ffkj = xgtkv__idfn = np.array([])
    vpofh__nlmhs = '0'
    if is_overload_constant_str(tz):
        nvnt__huvoc = get_overload_const_str(tz)
        xians__dqf = pytz.timezone(nvnt__huvoc)
        if isinstance(xians__dqf, pytz.tzinfo.DstTzInfo):
            sww__ffkj = np.array(xians__dqf._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            xgtkv__idfn = np.array(xians__dqf._transition_info)[:, 0]
            xgtkv__idfn = (pd.Series(xgtkv__idfn).dt.total_seconds() * 
                1000000000).astype(np.int64).values
            vpofh__nlmhs = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            xgtkv__idfn = np.int64(xians__dqf._utcoffset.total_seconds() * 
                1000000000)
            vpofh__nlmhs = 'deltas'
    elif is_overload_constant_int(tz):
        vfhl__ybjkf = get_overload_const_int(tz)
        vpofh__nlmhs = str(vfhl__ybjkf)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        cqnxq__upirw = 'tz_ts_input'
        dlozm__zqz = 'ts_input'
    else:
        cqnxq__upirw = 'ts_input'
        dlozm__zqz = 'tz_ts_input'
    huqy__pbr = 'def impl(ts_input, tz=None, is_convert=True):\n'
    huqy__pbr += f'  tz_ts_input = ts_input + {vpofh__nlmhs}\n'
    huqy__pbr += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({cqnxq__upirw}))\n'
        )
    huqy__pbr += '  month, day = get_month_day(year, days)\n'
    huqy__pbr += '  return init_timestamp(\n'
    huqy__pbr += '    year=year,\n'
    huqy__pbr += '    month=month,\n'
    huqy__pbr += '    day=day,\n'
    huqy__pbr += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    huqy__pbr += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    huqy__pbr += '    second=(dt // 1_000_000_000) % 60,\n'
    huqy__pbr += '    microsecond=(dt // 1000) % 1_000_000,\n'
    huqy__pbr += '    nanosecond=dt % 1000,\n'
    huqy__pbr += f'    value={dlozm__zqz},\n'
    huqy__pbr += '    tz=tz,\n'
    huqy__pbr += '  )\n'
    jxmhn__mbkcw = {}
    exec(huqy__pbr, {'np': np, 'pd': pd, 'trans': sww__ffkj, 'deltas':
        xgtkv__idfn, 'integer_to_dt64': integer_to_dt64,
        'extract_year_days': extract_year_days, 'get_month_day':
        get_month_day, 'init_timestamp': init_timestamp, 'zero_if_none':
        zero_if_none}, jxmhn__mbkcw)
    impl = jxmhn__mbkcw['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    rdhee__hly, year, dkyvy__utwjq = extract_year_days(dt64)
    month, day = get_month_day(year, dkyvy__utwjq)
    return init_timestamp(year=year, month=month, day=day, hour=rdhee__hly //
        (60 * 60 * 1000000000), minute=rdhee__hly // (60 * 1000000000) % 60,
        second=rdhee__hly // 1000000000 % 60, microsecond=rdhee__hly // 
        1000 % 1000000, nanosecond=rdhee__hly % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    bffrg__owt = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    mdq__ktt = bffrg__owt // (86400 * 1000000000)
    zzh__ohz = bffrg__owt - mdq__ktt * 86400 * 1000000000
    qlcgd__nmov = zzh__ohz // 1000000000
    fqxio__edvo = zzh__ohz - qlcgd__nmov * 1000000000
    rvj__gdsew = fqxio__edvo // 1000
    return datetime.timedelta(mdq__ktt, qlcgd__nmov, rvj__gdsew)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    bffrg__owt = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(bffrg__owt)


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
    yaau__knhz = len(arr)
    lcmn__dgl = np.empty(yaau__knhz, 'datetime64[ns]')
    uvc__eqn = arr._indices
    pgkza__ppaou = pandas_string_array_to_datetime(arr._data, errors,
        dayfirst, yearfirst, utc, format, exact, unit,
        infer_datetime_format, origin, cache).values
    for oen__pnm in range(yaau__knhz):
        if bodo.libs.array_kernels.isna(uvc__eqn, oen__pnm):
            bodo.libs.array_kernels.setna(lcmn__dgl, oen__pnm)
            continue
        lcmn__dgl[oen__pnm] = pgkza__ppaou[uvc__eqn[oen__pnm]]
    return lcmn__dgl


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
            polxg__pkw = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            afjot__aqth = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            aia__hzf = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(aia__hzf,
                polxg__pkw, afjot__aqth)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        xrnpe__yiwe = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            yaau__knhz = len(arg_a)
            lcmn__dgl = np.empty(yaau__knhz, xrnpe__yiwe)
            for oen__pnm in numba.parfors.parfor.internal_prange(yaau__knhz):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, oen__pnm):
                    data = arg_a[oen__pnm]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                lcmn__dgl[oen__pnm
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(lcmn__dgl,
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
        xrnpe__yiwe = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            yaau__knhz = len(arg_a)
            lcmn__dgl = np.empty(yaau__knhz, xrnpe__yiwe)
            for oen__pnm in numba.parfors.parfor.internal_prange(yaau__knhz):
                data = arg_a[oen__pnm]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                lcmn__dgl[oen__pnm
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(lcmn__dgl,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        xrnpe__yiwe = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            yaau__knhz = len(arg_a)
            lcmn__dgl = np.empty(yaau__knhz, xrnpe__yiwe)
            ftf__fnjfo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            pgkza__ppaou = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for oen__pnm in numba.parfors.parfor.internal_prange(yaau__knhz):
                c = ftf__fnjfo[oen__pnm]
                if c == -1:
                    bodo.libs.array_kernels.setna(lcmn__dgl, oen__pnm)
                    continue
                lcmn__dgl[oen__pnm] = pgkza__ppaou[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(lcmn__dgl,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            lcmn__dgl = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(lcmn__dgl,
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
            polxg__pkw = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            afjot__aqth = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            aia__hzf = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(aia__hzf,
                polxg__pkw, afjot__aqth)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, afb__wre = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, afb__wre, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, ulr__ixu = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, afb__wre = pd._libs.tslibs.conversion.precision_from_unit(unit)
        gzs__qdhe = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                yaau__knhz = len(arg_a)
                lcmn__dgl = np.empty(yaau__knhz, gzs__qdhe)
                for oen__pnm in numba.parfors.parfor.internal_prange(yaau__knhz
                    ):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, oen__pnm):
                        val = float_to_timedelta_val(arg_a[oen__pnm],
                            afb__wre, m)
                    lcmn__dgl[oen__pnm
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    lcmn__dgl, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                yaau__knhz = len(arg_a)
                lcmn__dgl = np.empty(yaau__knhz, gzs__qdhe)
                for oen__pnm in numba.parfors.parfor.internal_prange(yaau__knhz
                    ):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, oen__pnm):
                        val = arg_a[oen__pnm] * m
                    lcmn__dgl[oen__pnm
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    lcmn__dgl, None)
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
                yaau__knhz = len(arg_a)
                lcmn__dgl = np.empty(yaau__knhz, gzs__qdhe)
                for oen__pnm in numba.parfors.parfor.internal_prange(yaau__knhz
                    ):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, oen__pnm):
                        lnawb__gqhyc = arg_a[oen__pnm]
                        val = (lnawb__gqhyc.microseconds + 1000 * 1000 * (
                            lnawb__gqhyc.seconds + 24 * 60 * 60 *
                            lnawb__gqhyc.days)) * 1000
                    lcmn__dgl[oen__pnm
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    lcmn__dgl, None)
            return impl_datetime_timedelta
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    weaiz__exsg = np.int64(data)
    hjcw__tdrg = data - weaiz__exsg
    if precision:
        hjcw__tdrg = np.round(hjcw__tdrg, precision)
    return weaiz__exsg * multiplier + np.int64(hjcw__tdrg * multiplier)


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
        azwzu__ixqqu = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        iuf__slq = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', azwzu__ixqqu,
            iuf__slq, package_name='pandas', module_name='Timestamp')
        mead__qmi = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        sxjsl__qwzq = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 
            1000, 60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        huqy__pbr = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for oen__pnm, vrsip__pjmzt in enumerate(mead__qmi):
            dlgvq__pena = 'if' if oen__pnm == 0 else 'elif'
            huqy__pbr += '    {} {}:\n'.format(dlgvq__pena, vrsip__pjmzt)
            huqy__pbr += '        unit_value = {}\n'.format(sxjsl__qwzq[
                oen__pnm])
        huqy__pbr += '    else:\n'
        huqy__pbr += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            huqy__pbr += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        elif td == pd_timestamp_type:
            if method == 'ceil':
                huqy__pbr += (
                    '    value = td.value + np.remainder(-td.value, unit_value)\n'
                    )
            if method == 'floor':
                huqy__pbr += (
                    '    value = td.value - np.remainder(td.value, unit_value)\n'
                    )
            if method == 'round':
                huqy__pbr += '    if unit_value == 1:\n'
                huqy__pbr += '        value = td.value\n'
                huqy__pbr += '    else:\n'
                huqy__pbr += (
                    '        quotient, remainder = np.divmod(td.value, unit_value)\n'
                    )
                huqy__pbr += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                huqy__pbr += '        if mask:\n'
                huqy__pbr += '            quotient = quotient + 1\n'
                huqy__pbr += '        value = quotient * unit_value\n'
            huqy__pbr += '    return pd.Timestamp(value)\n'
        jxmhn__mbkcw = {}
        exec(huqy__pbr, {'np': np, 'pd': pd}, jxmhn__mbkcw)
        impl = jxmhn__mbkcw['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    ejqrj__yowxb = ['ceil', 'floor', 'round']
    for method in ejqrj__yowxb:
        yppmh__hyg = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(yppmh__hyg)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            yppmh__hyg)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    srdtw__vcmsb = totmicrosec // 1000000
    second = srdtw__vcmsb % 60
    pha__dfdq = srdtw__vcmsb // 60
    minute = pha__dfdq % 60
    deq__edmf = pha__dfdq // 60
    hour = deq__edmf % 24
    quw__tiw = deq__edmf // 24
    year, month, day = _ord2ymd(quw__tiw)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ncua__nohoa = lhs.toordinal()
            fbu__cmefz = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            zsllj__naah = lhs.microsecond
            nanosecond = lhs.nanosecond
            ols__jtoi = rhs.days
            getfj__ane = rhs.seconds
            mfvoi__mgt = rhs.microseconds
            lwokk__bxti = ncua__nohoa - ols__jtoi
            icpja__kknc = fbu__cmefz - getfj__ane
            ekwa__qkmx = zsllj__naah - mfvoi__mgt
            totmicrosec = 1000000 * (lwokk__bxti * 86400 + icpja__kknc
                ) + ekwa__qkmx
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
            ncua__nohoa = lhs.toordinal()
            fbu__cmefz = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            zsllj__naah = lhs.microsecond
            nanosecond = lhs.nanosecond
            ols__jtoi = rhs.days
            getfj__ane = rhs.seconds
            mfvoi__mgt = rhs.microseconds
            lwokk__bxti = ncua__nohoa + ols__jtoi
            icpja__kknc = fbu__cmefz + getfj__ane
            ekwa__qkmx = zsllj__naah + mfvoi__mgt
            totmicrosec = 1000000 * (lwokk__bxti * 86400 + icpja__kknc
                ) + ekwa__qkmx
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ncua__nohoa = lhs.toordinal()
            fbu__cmefz = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            zsllj__naah = lhs.microsecond
            nnyku__qgy = lhs.nanosecond
            mfvoi__mgt = rhs.value // 1000
            eogpd__kzze = rhs.nanoseconds
            ekwa__qkmx = zsllj__naah + mfvoi__mgt
            totmicrosec = 1000000 * (ncua__nohoa * 86400 + fbu__cmefz
                ) + ekwa__qkmx
            zuktw__hsz = nnyku__qgy + eogpd__kzze
            return compute_pd_timestamp(totmicrosec, zuktw__hsz)
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
        nggt__krr = 'datetime.date'
    else:
        nggt__krr = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{nggt__krr}.strftime(): 'strftime' argument must be a string")

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
    return types.Tuple([types.StringLiteral(zokzs__nntaf) for zokzs__nntaf in
        val])


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
    for fsw__qimbb in timestamp_unsupported_attrs:
        rei__zvl = 'pandas.Timestamp.' + fsw__qimbb
        overload_attribute(PandasTimestampType, fsw__qimbb)(
            create_unsupported_overload(rei__zvl))
    for xglrc__hfv in timestamp_unsupported_methods:
        rei__zvl = 'pandas.Timestamp.' + xglrc__hfv
        overload_method(PandasTimestampType, xglrc__hfv)(
            create_unsupported_overload(rei__zvl + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass, pd_timestamp_type,
    types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
