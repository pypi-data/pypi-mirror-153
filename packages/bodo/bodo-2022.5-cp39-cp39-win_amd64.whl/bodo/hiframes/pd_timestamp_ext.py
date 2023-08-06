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
            ttbyj__jymed = 'PandasTimestampType()'
        else:
            ttbyj__jymed = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=ttbyj__jymed)


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
        for cuke__fgyda in val.data:
            if isinstance(cuke__fgyda, bodo.DatetimeArrayType):
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
        fkx__htfec = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, fkx__htfec)


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
    mzs__edxcw = c.pyapi.object_getattr_string(val, 'year')
    xfhhr__qdwhh = c.pyapi.object_getattr_string(val, 'month')
    uklzv__gxfic = c.pyapi.object_getattr_string(val, 'day')
    qar__thul = c.pyapi.object_getattr_string(val, 'hour')
    mvdso__opq = c.pyapi.object_getattr_string(val, 'minute')
    vdd__daxl = c.pyapi.object_getattr_string(val, 'second')
    fvq__quh = c.pyapi.object_getattr_string(val, 'microsecond')
    yxbtb__yxlo = c.pyapi.object_getattr_string(val, 'nanosecond')
    nhev__vrje = c.pyapi.object_getattr_string(val, 'value')
    rgw__klay = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rgw__klay.year = c.pyapi.long_as_longlong(mzs__edxcw)
    rgw__klay.month = c.pyapi.long_as_longlong(xfhhr__qdwhh)
    rgw__klay.day = c.pyapi.long_as_longlong(uklzv__gxfic)
    rgw__klay.hour = c.pyapi.long_as_longlong(qar__thul)
    rgw__klay.minute = c.pyapi.long_as_longlong(mvdso__opq)
    rgw__klay.second = c.pyapi.long_as_longlong(vdd__daxl)
    rgw__klay.microsecond = c.pyapi.long_as_longlong(fvq__quh)
    rgw__klay.nanosecond = c.pyapi.long_as_longlong(yxbtb__yxlo)
    rgw__klay.value = c.pyapi.long_as_longlong(nhev__vrje)
    c.pyapi.decref(mzs__edxcw)
    c.pyapi.decref(xfhhr__qdwhh)
    c.pyapi.decref(uklzv__gxfic)
    c.pyapi.decref(qar__thul)
    c.pyapi.decref(mvdso__opq)
    c.pyapi.decref(vdd__daxl)
    c.pyapi.decref(fvq__quh)
    c.pyapi.decref(yxbtb__yxlo)
    c.pyapi.decref(nhev__vrje)
    rbux__fqgd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rgw__klay._getvalue(), is_error=rbux__fqgd)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    tia__prycu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    mzs__edxcw = c.pyapi.long_from_longlong(tia__prycu.year)
    xfhhr__qdwhh = c.pyapi.long_from_longlong(tia__prycu.month)
    uklzv__gxfic = c.pyapi.long_from_longlong(tia__prycu.day)
    qar__thul = c.pyapi.long_from_longlong(tia__prycu.hour)
    mvdso__opq = c.pyapi.long_from_longlong(tia__prycu.minute)
    vdd__daxl = c.pyapi.long_from_longlong(tia__prycu.second)
    ndib__hrgn = c.pyapi.long_from_longlong(tia__prycu.microsecond)
    sayzp__hoq = c.pyapi.long_from_longlong(tia__prycu.nanosecond)
    ufwjf__pcyff = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(ufwjf__pcyff, (mzs__edxcw,
            xfhhr__qdwhh, uklzv__gxfic, qar__thul, mvdso__opq, vdd__daxl,
            ndib__hrgn, sayzp__hoq))
    else:
        if isinstance(typ.tz, int):
            nqi__dnalt = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            fet__gfqoh = c.context.insert_const_string(c.builder.module,
                str(typ.tz))
            nqi__dnalt = c.pyapi.string_from_string(fet__gfqoh)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', mzs__edxcw), ('month',
            xfhhr__qdwhh), ('day', uklzv__gxfic), ('hour', qar__thul), (
            'minute', mvdso__opq), ('second', vdd__daxl), ('microsecond',
            ndib__hrgn), ('nanosecond', sayzp__hoq), ('tz', nqi__dnalt)])
        res = c.pyapi.call(ufwjf__pcyff, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(nqi__dnalt)
    c.pyapi.decref(mzs__edxcw)
    c.pyapi.decref(xfhhr__qdwhh)
    c.pyapi.decref(uklzv__gxfic)
    c.pyapi.decref(qar__thul)
    c.pyapi.decref(mvdso__opq)
    c.pyapi.decref(vdd__daxl)
    c.pyapi.decref(ndib__hrgn)
    c.pyapi.decref(sayzp__hoq)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, vjhs__cula, sqyb__mto,
            value, udsk__dusz) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = vjhs__cula
        ts.nanosecond = sqyb__mto
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
        ron__bul, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * ron__bul
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            mfj__vhli = np.int64(ts_input)
            btdzk__wlzom = ts_input - mfj__vhli
            if precision:
                btdzk__wlzom = np.round(btdzk__wlzom, precision)
            value = mfj__vhli * ron__bul + np.int64(btdzk__wlzom * ron__bul)
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
        ron__bul, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * ron__bul
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
        udsk__dusz, yhf__lyrq, udsk__dusz = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return yhf__lyrq
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
        year, yhf__lyrq, pio__uegb = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, yhf__lyrq, pio__uegb
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            qgn__rldwz = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + qgn__rldwz
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            qgn__rldwz = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + qgn__rldwz
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    bbts__xhrs = dict(locale=locale)
    ybbq__nbem = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', bbts__xhrs, ybbq__nbem,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        jfnq__hdva = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
        udsk__dusz, udsk__dusz, jxlu__zyecg = ptt.isocalendar()
        return jfnq__hdva[jxlu__zyecg - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    bbts__xhrs = dict(locale=locale)
    ybbq__nbem = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', bbts__xhrs, ybbq__nbem,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        czest__oab = ('January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November',
            'December')
        return czest__oab[ptt.month - 1]
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
    bbts__xhrs = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    yba__ipe = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', bbts__xhrs, yba__ipe,
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
        hqnqq__zrrr = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], hqnqq__zrrr)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        ztm__qsts = cgutils.alloca_once(builder, lir.IntType(64))
        nbp__wxy = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        znye__dpmg = cgutils.get_or_insert_function(builder.module,
            nbp__wxy, name='extract_year_days')
        builder.call(znye__dpmg, [hqnqq__zrrr, year, ztm__qsts])
        return cgutils.pack_array(builder, [builder.load(hqnqq__zrrr),
            builder.load(year), builder.load(ztm__qsts)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        nbp__wxy = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir.
            IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        znye__dpmg = cgutils.get_or_insert_function(builder.module,
            nbp__wxy, name='get_month_day')
        builder.call(znye__dpmg, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    kzg__wxlfx = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 
        365, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    ajfp__svr = is_leap_year(year)
    pjzb__hztj = kzg__wxlfx[ajfp__svr * 13 + month - 1]
    cqlpc__fiste = pjzb__hztj + day
    return cqlpc__fiste


@register_jitable
def get_day_of_week(y, m, d):
    pdq__dpci = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + pdq__dpci[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    npe__ihh = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 31,
        30, 31, 30, 31, 31, 30, 31, 30, 31]
    return npe__ihh[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    oisr__zilr = cxbo__eonv = np.array([])
    ffca__dtid = '0'
    if is_overload_constant_str(tz):
        fet__gfqoh = get_overload_const_str(tz)
        nqi__dnalt = pytz.timezone(fet__gfqoh)
        if isinstance(nqi__dnalt, pytz.tzinfo.DstTzInfo):
            oisr__zilr = np.array(nqi__dnalt._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            cxbo__eonv = np.array(nqi__dnalt._transition_info)[:, 0]
            cxbo__eonv = (pd.Series(cxbo__eonv).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            ffca__dtid = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            cxbo__eonv = np.int64(nqi__dnalt._utcoffset.total_seconds() * 
                1000000000)
            ffca__dtid = 'deltas'
    elif is_overload_constant_int(tz):
        nqvkt__xyytq = get_overload_const_int(tz)
        ffca__dtid = str(nqvkt__xyytq)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        tcja__ahv = 'tz_ts_input'
        blt__tssm = 'ts_input'
    else:
        tcja__ahv = 'ts_input'
        blt__tssm = 'tz_ts_input'
    qexfp__rfxs = 'def impl(ts_input, tz=None, is_convert=True):\n'
    qexfp__rfxs += f'  tz_ts_input = ts_input + {ffca__dtid}\n'
    qexfp__rfxs += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({tcja__ahv}))\n'
        )
    qexfp__rfxs += '  month, day = get_month_day(year, days)\n'
    qexfp__rfxs += '  return init_timestamp(\n'
    qexfp__rfxs += '    year=year,\n'
    qexfp__rfxs += '    month=month,\n'
    qexfp__rfxs += '    day=day,\n'
    qexfp__rfxs += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    qexfp__rfxs += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    qexfp__rfxs += '    second=(dt // 1_000_000_000) % 60,\n'
    qexfp__rfxs += '    microsecond=(dt // 1000) % 1_000_000,\n'
    qexfp__rfxs += '    nanosecond=dt % 1000,\n'
    qexfp__rfxs += f'    value={blt__tssm},\n'
    qexfp__rfxs += '    tz=tz,\n'
    qexfp__rfxs += '  )\n'
    znyds__cltt = {}
    exec(qexfp__rfxs, {'np': np, 'pd': pd, 'trans': oisr__zilr, 'deltas':
        cxbo__eonv, 'integer_to_dt64': integer_to_dt64, 'extract_year_days':
        extract_year_days, 'get_month_day': get_month_day, 'init_timestamp':
        init_timestamp, 'zero_if_none': zero_if_none}, znyds__cltt)
    impl = znyds__cltt['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    hqnqq__zrrr, year, ztm__qsts = extract_year_days(dt64)
    month, day = get_month_day(year, ztm__qsts)
    return init_timestamp(year=year, month=month, day=day, hour=hqnqq__zrrr //
        (60 * 60 * 1000000000), minute=hqnqq__zrrr // (60 * 1000000000) % 
        60, second=hqnqq__zrrr // 1000000000 % 60, microsecond=hqnqq__zrrr //
        1000 % 1000000, nanosecond=hqnqq__zrrr % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    ojwa__ykcmk = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    phls__szz = ojwa__ykcmk // (86400 * 1000000000)
    xynb__iapi = ojwa__ykcmk - phls__szz * 86400 * 1000000000
    kpidx__kvkuw = xynb__iapi // 1000000000
    qhs__swdwm = xynb__iapi - kpidx__kvkuw * 1000000000
    fpsg__enu = qhs__swdwm // 1000
    return datetime.timedelta(phls__szz, kpidx__kvkuw, fpsg__enu)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    ojwa__ykcmk = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(ojwa__ykcmk)


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
    wqfqm__icsbz = len(arr)
    swg__fpwe = np.empty(wqfqm__icsbz, 'datetime64[ns]')
    ucwu__bwidw = arr._indices
    vvi__xrjw = pandas_string_array_to_datetime(arr._data, errors, dayfirst,
        yearfirst, utc, format, exact, unit, infer_datetime_format, origin,
        cache).values
    for rfdee__bcrx in range(wqfqm__icsbz):
        if bodo.libs.array_kernels.isna(ucwu__bwidw, rfdee__bcrx):
            bodo.libs.array_kernels.setna(swg__fpwe, rfdee__bcrx)
            continue
        swg__fpwe[rfdee__bcrx] = vvi__xrjw[ucwu__bwidw[rfdee__bcrx]]
    return swg__fpwe


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
            xypy__ykf = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            ttbyj__jymed = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ucla__lmi = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(ucla__lmi,
                xypy__ykf, ttbyj__jymed)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        rwsa__uvfjr = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            wqfqm__icsbz = len(arg_a)
            swg__fpwe = np.empty(wqfqm__icsbz, rwsa__uvfjr)
            for rfdee__bcrx in numba.parfors.parfor.internal_prange(
                wqfqm__icsbz):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, rfdee__bcrx):
                    data = arg_a[rfdee__bcrx]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                swg__fpwe[rfdee__bcrx
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(swg__fpwe,
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
        rwsa__uvfjr = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            wqfqm__icsbz = len(arg_a)
            swg__fpwe = np.empty(wqfqm__icsbz, rwsa__uvfjr)
            for rfdee__bcrx in numba.parfors.parfor.internal_prange(
                wqfqm__icsbz):
                data = arg_a[rfdee__bcrx]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                swg__fpwe[rfdee__bcrx
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(swg__fpwe,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        rwsa__uvfjr = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            wqfqm__icsbz = len(arg_a)
            swg__fpwe = np.empty(wqfqm__icsbz, rwsa__uvfjr)
            zfcsr__mqrlp = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            vvi__xrjw = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for rfdee__bcrx in numba.parfors.parfor.internal_prange(
                wqfqm__icsbz):
                c = zfcsr__mqrlp[rfdee__bcrx]
                if c == -1:
                    bodo.libs.array_kernels.setna(swg__fpwe, rfdee__bcrx)
                    continue
                swg__fpwe[rfdee__bcrx] = vvi__xrjw[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(swg__fpwe,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            swg__fpwe = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(swg__fpwe,
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
            xypy__ykf = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            ttbyj__jymed = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ucla__lmi = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(ucla__lmi,
                xypy__ykf, ttbyj__jymed)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, xwn__hnw = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, xwn__hnw, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, udsk__dusz = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, xwn__hnw = pd._libs.tslibs.conversion.precision_from_unit(unit)
        yyx__mvv = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                wqfqm__icsbz = len(arg_a)
                swg__fpwe = np.empty(wqfqm__icsbz, yyx__mvv)
                for rfdee__bcrx in numba.parfors.parfor.internal_prange(
                    wqfqm__icsbz):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, rfdee__bcrx):
                        val = float_to_timedelta_val(arg_a[rfdee__bcrx],
                            xwn__hnw, m)
                    swg__fpwe[rfdee__bcrx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    swg__fpwe, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                wqfqm__icsbz = len(arg_a)
                swg__fpwe = np.empty(wqfqm__icsbz, yyx__mvv)
                for rfdee__bcrx in numba.parfors.parfor.internal_prange(
                    wqfqm__icsbz):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, rfdee__bcrx):
                        val = arg_a[rfdee__bcrx] * m
                    swg__fpwe[rfdee__bcrx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    swg__fpwe, None)
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
                wqfqm__icsbz = len(arg_a)
                swg__fpwe = np.empty(wqfqm__icsbz, yyx__mvv)
                for rfdee__bcrx in numba.parfors.parfor.internal_prange(
                    wqfqm__icsbz):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, rfdee__bcrx):
                        uvtlt__dqce = arg_a[rfdee__bcrx]
                        val = (uvtlt__dqce.microseconds + 1000 * 1000 * (
                            uvtlt__dqce.seconds + 24 * 60 * 60 *
                            uvtlt__dqce.days)) * 1000
                    swg__fpwe[rfdee__bcrx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    swg__fpwe, None)
            return impl_datetime_timedelta
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    mfj__vhli = np.int64(data)
    btdzk__wlzom = data - mfj__vhli
    if precision:
        btdzk__wlzom = np.round(btdzk__wlzom, precision)
    return mfj__vhli * multiplier + np.int64(btdzk__wlzom * multiplier)


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
        bbts__xhrs = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        rip__sheh = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', bbts__xhrs, rip__sheh,
            package_name='pandas', module_name='Timestamp')
        glxv__kmmu = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        vyhy__khfpk = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 
            1000, 60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        qexfp__rfxs = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for rfdee__bcrx, bvehn__ndm in enumerate(glxv__kmmu):
            tdxh__qqrtg = 'if' if rfdee__bcrx == 0 else 'elif'
            qexfp__rfxs += '    {} {}:\n'.format(tdxh__qqrtg, bvehn__ndm)
            qexfp__rfxs += '        unit_value = {}\n'.format(vyhy__khfpk[
                rfdee__bcrx])
        qexfp__rfxs += '    else:\n'
        qexfp__rfxs += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            qexfp__rfxs += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        elif td == pd_timestamp_type:
            if method == 'ceil':
                qexfp__rfxs += (
                    '    value = td.value + np.remainder(-td.value, unit_value)\n'
                    )
            if method == 'floor':
                qexfp__rfxs += (
                    '    value = td.value - np.remainder(td.value, unit_value)\n'
                    )
            if method == 'round':
                qexfp__rfxs += '    if unit_value == 1:\n'
                qexfp__rfxs += '        value = td.value\n'
                qexfp__rfxs += '    else:\n'
                qexfp__rfxs += (
                    '        quotient, remainder = np.divmod(td.value, unit_value)\n'
                    )
                qexfp__rfxs += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                qexfp__rfxs += '        if mask:\n'
                qexfp__rfxs += '            quotient = quotient + 1\n'
                qexfp__rfxs += '        value = quotient * unit_value\n'
            qexfp__rfxs += '    return pd.Timestamp(value)\n'
        znyds__cltt = {}
        exec(qexfp__rfxs, {'np': np, 'pd': pd}, znyds__cltt)
        impl = znyds__cltt['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    vot__kurot = ['ceil', 'floor', 'round']
    for method in vot__kurot:
        flkhx__cjy = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(flkhx__cjy)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            flkhx__cjy)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    rcs__zlaxy = totmicrosec // 1000000
    second = rcs__zlaxy % 60
    gpez__phl = rcs__zlaxy // 60
    minute = gpez__phl % 60
    hqew__obef = gpez__phl // 60
    hour = hqew__obef % 24
    btnmt__aus = hqew__obef // 24
    year, month, day = _ord2ymd(btnmt__aus)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ouul__byoy = lhs.toordinal()
            wgh__pwwjh = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            buijn__kxw = lhs.microsecond
            nanosecond = lhs.nanosecond
            ssex__ebla = rhs.days
            dvqw__rsin = rhs.seconds
            ukw__daygd = rhs.microseconds
            bywwa__szt = ouul__byoy - ssex__ebla
            xbgj__kbpy = wgh__pwwjh - dvqw__rsin
            usorr__vejs = buijn__kxw - ukw__daygd
            totmicrosec = 1000000 * (bywwa__szt * 86400 + xbgj__kbpy
                ) + usorr__vejs
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
            ouul__byoy = lhs.toordinal()
            wgh__pwwjh = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            buijn__kxw = lhs.microsecond
            nanosecond = lhs.nanosecond
            ssex__ebla = rhs.days
            dvqw__rsin = rhs.seconds
            ukw__daygd = rhs.microseconds
            bywwa__szt = ouul__byoy + ssex__ebla
            xbgj__kbpy = wgh__pwwjh + dvqw__rsin
            usorr__vejs = buijn__kxw + ukw__daygd
            totmicrosec = 1000000 * (bywwa__szt * 86400 + xbgj__kbpy
                ) + usorr__vejs
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ouul__byoy = lhs.toordinal()
            wgh__pwwjh = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            buijn__kxw = lhs.microsecond
            hpfs__hmbd = lhs.nanosecond
            ukw__daygd = rhs.value // 1000
            fup__nacor = rhs.nanoseconds
            usorr__vejs = buijn__kxw + ukw__daygd
            totmicrosec = 1000000 * (ouul__byoy * 86400 + wgh__pwwjh
                ) + usorr__vejs
            vuz__omcz = hpfs__hmbd + fup__nacor
            return compute_pd_timestamp(totmicrosec, vuz__omcz)
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
        gyxj__xhul = 'datetime.date'
    else:
        gyxj__xhul = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{gyxj__xhul}.strftime(): 'strftime' argument must be a string")

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
    return types.Tuple([types.StringLiteral(zzzxu__ekjqe) for zzzxu__ekjqe in
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
    for gta__tqwf in timestamp_unsupported_attrs:
        ubpd__qki = 'pandas.Timestamp.' + gta__tqwf
        overload_attribute(PandasTimestampType, gta__tqwf)(
            create_unsupported_overload(ubpd__qki))
    for jobsu__yhper in timestamp_unsupported_methods:
        ubpd__qki = 'pandas.Timestamp.' + jobsu__yhper
        overload_method(PandasTimestampType, jobsu__yhper)(
            create_unsupported_overload(ubpd__qki + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass, pd_timestamp_type,
    types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
