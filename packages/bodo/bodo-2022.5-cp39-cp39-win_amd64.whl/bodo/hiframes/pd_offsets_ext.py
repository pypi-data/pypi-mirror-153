"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import get_days_in_month, pd_timestamp_type
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hujgc__yyze = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, hujgc__yyze)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    geqnx__cufp = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    wvpo__leywf = c.pyapi.long_from_longlong(geqnx__cufp.n)
    ksza__sqml = c.pyapi.from_native_value(types.boolean, geqnx__cufp.
        normalize, c.env_manager)
    rpce__pzyl = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    uagjo__lqed = c.pyapi.call_function_objargs(rpce__pzyl, (wvpo__leywf,
        ksza__sqml))
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    c.pyapi.decref(rpce__pzyl)
    return uagjo__lqed


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    wvpo__leywf = c.pyapi.object_getattr_string(val, 'n')
    ksza__sqml = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(wvpo__leywf)
    normalize = c.pyapi.to_native_value(types.bool_, ksza__sqml).value
    geqnx__cufp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    geqnx__cufp.n = n
    geqnx__cufp.normalize = normalize
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    qox__pbu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(geqnx__cufp._getvalue(), is_error=qox__pbu)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        geqnx__cufp = cgutils.create_struct_proxy(typ)(context, builder)
        geqnx__cufp.n = args[0]
        geqnx__cufp.normalize = args[1]
        return geqnx__cufp._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hujgc__yyze = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, hujgc__yyze)


@box(MonthEndType)
def box_month_end(typ, val, c):
    zufi__jokby = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    wvpo__leywf = c.pyapi.long_from_longlong(zufi__jokby.n)
    ksza__sqml = c.pyapi.from_native_value(types.boolean, zufi__jokby.
        normalize, c.env_manager)
    grf__rbbja = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    uagjo__lqed = c.pyapi.call_function_objargs(grf__rbbja, (wvpo__leywf,
        ksza__sqml))
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    c.pyapi.decref(grf__rbbja)
    return uagjo__lqed


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    wvpo__leywf = c.pyapi.object_getattr_string(val, 'n')
    ksza__sqml = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(wvpo__leywf)
    normalize = c.pyapi.to_native_value(types.bool_, ksza__sqml).value
    zufi__jokby = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zufi__jokby.n = n
    zufi__jokby.normalize = normalize
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    qox__pbu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zufi__jokby._getvalue(), is_error=qox__pbu)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        zufi__jokby = cgutils.create_struct_proxy(typ)(context, builder)
        zufi__jokby.n = args[0]
        zufi__jokby.normalize = args[1]
        return zufi__jokby._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        zufi__jokby = get_days_in_month(year, month)
        if zufi__jokby > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hujgc__yyze = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, hujgc__yyze)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    avr__ctskd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ilmdn__wegpg = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for vilrt__hhgnx, uansp__ozl in enumerate(date_offset_fields):
        c.builder.store(getattr(avr__ctskd, uansp__ozl), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(ilmdn__wegpg, lir.IntType(64)
            ), lir.Constant(lir.IntType(64), 8 * vilrt__hhgnx)), lir.
            IntType(64).as_pointer()))
    oqgj__xxzmp = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    xqf__xio = cgutils.get_or_insert_function(c.builder.module, oqgj__xxzmp,
        name='box_date_offset')
    lrghc__uoujz = c.builder.call(xqf__xio, [avr__ctskd.n, avr__ctskd.
        normalize, ilmdn__wegpg, avr__ctskd.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return lrghc__uoujz


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    wvpo__leywf = c.pyapi.object_getattr_string(val, 'n')
    ksza__sqml = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(wvpo__leywf)
    normalize = c.pyapi.to_native_value(types.bool_, ksza__sqml).value
    ilmdn__wegpg = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    oqgj__xxzmp = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    uprq__woakz = cgutils.get_or_insert_function(c.builder.module,
        oqgj__xxzmp, name='unbox_date_offset')
    has_kws = c.builder.call(uprq__woakz, [val, ilmdn__wegpg])
    avr__ctskd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    avr__ctskd.n = n
    avr__ctskd.normalize = normalize
    for vilrt__hhgnx, uansp__ozl in enumerate(date_offset_fields):
        setattr(avr__ctskd, uansp__ozl, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(ilmdn__wegpg, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * vilrt__hhgnx)), lir.IntType(
            64).as_pointer())))
    avr__ctskd.has_kws = has_kws
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    qox__pbu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(avr__ctskd._getvalue(), is_error=qox__pbu)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    slxjl__ytstx = [n, normalize]
    has_kws = False
    xpvw__hrfv = [0] * 9 + [-1] * 9
    for vilrt__hhgnx, uansp__ozl in enumerate(date_offset_fields):
        if hasattr(pyval, uansp__ozl):
            xll__lamad = context.get_constant(types.int64, getattr(pyval,
                uansp__ozl))
            has_kws = True
        else:
            xll__lamad = context.get_constant(types.int64, xpvw__hrfv[
                vilrt__hhgnx])
        slxjl__ytstx.append(xll__lamad)
    has_kws = context.get_constant(types.boolean, has_kws)
    slxjl__ytstx.append(has_kws)
    return lir.Constant.literal_struct(slxjl__ytstx)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    ijzc__iicj = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for tsbav__rpyvj in ijzc__iicj:
        if not is_overload_none(tsbav__rpyvj):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        avr__ctskd = cgutils.create_struct_proxy(typ)(context, builder)
        avr__ctskd.n = args[0]
        avr__ctskd.normalize = args[1]
        avr__ctskd.years = args[2]
        avr__ctskd.months = args[3]
        avr__ctskd.weeks = args[4]
        avr__ctskd.days = args[5]
        avr__ctskd.hours = args[6]
        avr__ctskd.minutes = args[7]
        avr__ctskd.seconds = args[8]
        avr__ctskd.microseconds = args[9]
        avr__ctskd.nanoseconds = args[10]
        avr__ctskd.year = args[11]
        avr__ctskd.month = args[12]
        avr__ctskd.day = args[13]
        avr__ctskd.weekday = args[14]
        avr__ctskd.hour = args[15]
        avr__ctskd.minute = args[16]
        avr__ctskd.second = args[17]
        avr__ctskd.microsecond = args[18]
        avr__ctskd.nanosecond = args[19]
        avr__ctskd.has_kws = args[20]
        return avr__ctskd._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        pxwnx__pgzrf = -1 if dateoffset.n < 0 else 1
        for gykx__sgh in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += pxwnx__pgzrf * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += pxwnx__pgzrf * dateoffset._months
            year, month, otyyt__llqk = calculate_month_end_date(year, month,
                day, 0)
            if day > otyyt__llqk:
                day = otyyt__llqk
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            if dateoffset._nanosecond != -1:
                nanosecond = dateoffset._nanosecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            cynd__rhk = pd.Timedelta(days=dateoffset._days + 7 * dateoffset
                ._weeks, hours=dateoffset._hours, minutes=dateoffset.
                _minutes, seconds=dateoffset._seconds, microseconds=
                dateoffset._microseconds)
            cynd__rhk = cynd__rhk + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if pxwnx__pgzrf == -1:
                cynd__rhk = -cynd__rhk
            ts = ts + cynd__rhk
            if dateoffset._weekday != -1:
                ryg__cve = ts.weekday()
                ywadp__uzvh = (dateoffset._weekday - ryg__cve) % 7
                ts = ts + pd.Timedelta(days=ywadp__uzvh)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs in [date_offset_type, month_begin_type, month_end_type,
        week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hujgc__yyze = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, hujgc__yyze)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        jfx__glqld = -1 if weekday is None else weekday
        return init_week(n, normalize, jfx__glqld)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        oexam__wtmcv = cgutils.create_struct_proxy(typ)(context, builder)
        oexam__wtmcv.n = args[0]
        oexam__wtmcv.normalize = args[1]
        oexam__wtmcv.weekday = args[2]
        return oexam__wtmcv._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    oexam__wtmcv = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    wvpo__leywf = c.pyapi.long_from_longlong(oexam__wtmcv.n)
    ksza__sqml = c.pyapi.from_native_value(types.boolean, oexam__wtmcv.
        normalize, c.env_manager)
    ykl__qggju = c.pyapi.long_from_longlong(oexam__wtmcv.weekday)
    pyqz__sff = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    kqmsk__caj = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), 
        -1), oexam__wtmcv.weekday)
    with c.builder.if_else(kqmsk__caj) as (plax__tns, nwi__rax):
        with plax__tns:
            uhp__qtk = c.pyapi.call_function_objargs(pyqz__sff, (
                wvpo__leywf, ksza__sqml, ykl__qggju))
            ttxt__vmwy = c.builder.block
        with nwi__rax:
            xanlr__apvi = c.pyapi.call_function_objargs(pyqz__sff, (
                wvpo__leywf, ksza__sqml))
            wlhn__ogyp = c.builder.block
    uagjo__lqed = c.builder.phi(uhp__qtk.type)
    uagjo__lqed.add_incoming(uhp__qtk, ttxt__vmwy)
    uagjo__lqed.add_incoming(xanlr__apvi, wlhn__ogyp)
    c.pyapi.decref(ykl__qggju)
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    c.pyapi.decref(pyqz__sff)
    return uagjo__lqed


@unbox(WeekType)
def unbox_week(typ, val, c):
    wvpo__leywf = c.pyapi.object_getattr_string(val, 'n')
    ksza__sqml = c.pyapi.object_getattr_string(val, 'normalize')
    ykl__qggju = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(wvpo__leywf)
    normalize = c.pyapi.to_native_value(types.bool_, ksza__sqml).value
    oafm__kzkk = c.pyapi.make_none()
    joeia__wht = c.builder.icmp_unsigned('==', ykl__qggju, oafm__kzkk)
    with c.builder.if_else(joeia__wht) as (nwi__rax, plax__tns):
        with plax__tns:
            uhp__qtk = c.pyapi.long_as_longlong(ykl__qggju)
            ttxt__vmwy = c.builder.block
        with nwi__rax:
            xanlr__apvi = lir.Constant(lir.IntType(64), -1)
            wlhn__ogyp = c.builder.block
    uagjo__lqed = c.builder.phi(uhp__qtk.type)
    uagjo__lqed.add_incoming(uhp__qtk, ttxt__vmwy)
    uagjo__lqed.add_incoming(xanlr__apvi, wlhn__ogyp)
    oexam__wtmcv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oexam__wtmcv.n = n
    oexam__wtmcv.normalize = normalize
    oexam__wtmcv.weekday = uagjo__lqed
    c.pyapi.decref(wvpo__leywf)
    c.pyapi.decref(ksza__sqml)
    c.pyapi.decref(ykl__qggju)
    qox__pbu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oexam__wtmcv._getvalue(), is_error=qox__pbu)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            wng__uczu = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                fcqf__bees = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                fcqf__bees = rhs
            return fcqf__bees + wng__uczu
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            wng__uczu = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                fcqf__bees = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                fcqf__bees = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return fcqf__bees + wng__uczu
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            wng__uczu = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + wng__uczu
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


@register_jitable
def calculate_week_date(n, weekday, other_weekday):
    if weekday == -1:
        return pd.Timedelta(weeks=n)
    if weekday != other_weekday:
        pse__dbt = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=pse__dbt)


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for kxh__zxeu in date_offset_unsupported_attrs:
        pes__ehibu = 'pandas.tseries.offsets.DateOffset.' + kxh__zxeu
        overload_attribute(DateOffsetType, kxh__zxeu)(
            create_unsupported_overload(pes__ehibu))
    for kxh__zxeu in date_offset_unsupported:
        pes__ehibu = 'pandas.tseries.offsets.DateOffset.' + kxh__zxeu
        overload_method(DateOffsetType, kxh__zxeu)(create_unsupported_overload
            (pes__ehibu))


def _install_month_begin_unsupported():
    for kxh__zxeu in month_begin_unsupported_attrs:
        pes__ehibu = 'pandas.tseries.offsets.MonthBegin.' + kxh__zxeu
        overload_attribute(MonthBeginType, kxh__zxeu)(
            create_unsupported_overload(pes__ehibu))
    for kxh__zxeu in month_begin_unsupported:
        pes__ehibu = 'pandas.tseries.offsets.MonthBegin.' + kxh__zxeu
        overload_method(MonthBeginType, kxh__zxeu)(create_unsupported_overload
            (pes__ehibu))


def _install_month_end_unsupported():
    for kxh__zxeu in date_offset_unsupported_attrs:
        pes__ehibu = 'pandas.tseries.offsets.MonthEnd.' + kxh__zxeu
        overload_attribute(MonthEndType, kxh__zxeu)(create_unsupported_overload
            (pes__ehibu))
    for kxh__zxeu in date_offset_unsupported:
        pes__ehibu = 'pandas.tseries.offsets.MonthEnd.' + kxh__zxeu
        overload_method(MonthEndType, kxh__zxeu)(create_unsupported_overload
            (pes__ehibu))


def _install_week_unsupported():
    for kxh__zxeu in week_unsupported_attrs:
        pes__ehibu = 'pandas.tseries.offsets.Week.' + kxh__zxeu
        overload_attribute(WeekType, kxh__zxeu)(create_unsupported_overload
            (pes__ehibu))
    for kxh__zxeu in week_unsupported:
        pes__ehibu = 'pandas.tseries.offsets.Week.' + kxh__zxeu
        overload_method(WeekType, kxh__zxeu)(create_unsupported_overload(
            pes__ehibu))


def _install_offsets_unsupported():
    for xll__lamad in offsets_unsupported:
        pes__ehibu = 'pandas.tseries.offsets.' + xll__lamad.__name__
        overload(xll__lamad)(create_unsupported_overload(pes__ehibu))


def _install_frequencies_unsupported():
    for xll__lamad in frequencies_unsupported:
        pes__ehibu = 'pandas.tseries.frequencies.' + xll__lamad.__name__
        overload(xll__lamad)(create_unsupported_overload(pes__ehibu))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
