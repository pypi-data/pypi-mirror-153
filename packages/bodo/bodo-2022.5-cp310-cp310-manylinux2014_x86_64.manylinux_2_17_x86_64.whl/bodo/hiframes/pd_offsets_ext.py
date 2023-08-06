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
        ntxu__cjmon = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, ntxu__cjmon)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    fhf__rwxu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    owm__nct = c.pyapi.long_from_longlong(fhf__rwxu.n)
    odluz__njpr = c.pyapi.from_native_value(types.boolean, fhf__rwxu.
        normalize, c.env_manager)
    hvhy__yeo = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    uge__nuhm = c.pyapi.call_function_objargs(hvhy__yeo, (owm__nct,
        odluz__njpr))
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    c.pyapi.decref(hvhy__yeo)
    return uge__nuhm


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    owm__nct = c.pyapi.object_getattr_string(val, 'n')
    odluz__njpr = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(owm__nct)
    normalize = c.pyapi.to_native_value(types.bool_, odluz__njpr).value
    fhf__rwxu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fhf__rwxu.n = n
    fhf__rwxu.normalize = normalize
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    adkmo__ktu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fhf__rwxu._getvalue(), is_error=adkmo__ktu)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        fhf__rwxu = cgutils.create_struct_proxy(typ)(context, builder)
        fhf__rwxu.n = args[0]
        fhf__rwxu.normalize = args[1]
        return fhf__rwxu._getvalue()
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
        ntxu__cjmon = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, ntxu__cjmon)


@box(MonthEndType)
def box_month_end(typ, val, c):
    ffxm__yaqk = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    owm__nct = c.pyapi.long_from_longlong(ffxm__yaqk.n)
    odluz__njpr = c.pyapi.from_native_value(types.boolean, ffxm__yaqk.
        normalize, c.env_manager)
    iqmxg__rpn = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    uge__nuhm = c.pyapi.call_function_objargs(iqmxg__rpn, (owm__nct,
        odluz__njpr))
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    c.pyapi.decref(iqmxg__rpn)
    return uge__nuhm


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    owm__nct = c.pyapi.object_getattr_string(val, 'n')
    odluz__njpr = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(owm__nct)
    normalize = c.pyapi.to_native_value(types.bool_, odluz__njpr).value
    ffxm__yaqk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ffxm__yaqk.n = n
    ffxm__yaqk.normalize = normalize
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    adkmo__ktu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ffxm__yaqk._getvalue(), is_error=adkmo__ktu)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ffxm__yaqk = cgutils.create_struct_proxy(typ)(context, builder)
        ffxm__yaqk.n = args[0]
        ffxm__yaqk.normalize = args[1]
        return ffxm__yaqk._getvalue()
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
        ffxm__yaqk = get_days_in_month(year, month)
        if ffxm__yaqk > day:
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
        ntxu__cjmon = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, ntxu__cjmon)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    vnca__nfn = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jye__msrb = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for eccsw__ghjh, ppyz__brnfu in enumerate(date_offset_fields):
        c.builder.store(getattr(vnca__nfn, ppyz__brnfu), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(jye__msrb, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * eccsw__ghjh)), lir.IntType(64
            ).as_pointer()))
    lvyf__otl = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    tzxy__fpqpd = cgutils.get_or_insert_function(c.builder.module,
        lvyf__otl, name='box_date_offset')
    hmhq__bcj = c.builder.call(tzxy__fpqpd, [vnca__nfn.n, vnca__nfn.
        normalize, jye__msrb, vnca__nfn.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return hmhq__bcj


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    owm__nct = c.pyapi.object_getattr_string(val, 'n')
    odluz__njpr = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(owm__nct)
    normalize = c.pyapi.to_native_value(types.bool_, odluz__njpr).value
    jye__msrb = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    lvyf__otl = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer()])
    bxtgq__wsjt = cgutils.get_or_insert_function(c.builder.module,
        lvyf__otl, name='unbox_date_offset')
    has_kws = c.builder.call(bxtgq__wsjt, [val, jye__msrb])
    vnca__nfn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vnca__nfn.n = n
    vnca__nfn.normalize = normalize
    for eccsw__ghjh, ppyz__brnfu in enumerate(date_offset_fields):
        setattr(vnca__nfn, ppyz__brnfu, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(jye__msrb, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * eccsw__ghjh)), lir.IntType(64
            ).as_pointer())))
    vnca__nfn.has_kws = has_kws
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    adkmo__ktu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vnca__nfn._getvalue(), is_error=adkmo__ktu)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    wosa__gsslq = [n, normalize]
    has_kws = False
    cylfz__bissm = [0] * 9 + [-1] * 9
    for eccsw__ghjh, ppyz__brnfu in enumerate(date_offset_fields):
        if hasattr(pyval, ppyz__brnfu):
            djq__pwffg = context.get_constant(types.int64, getattr(pyval,
                ppyz__brnfu))
            has_kws = True
        else:
            djq__pwffg = context.get_constant(types.int64, cylfz__bissm[
                eccsw__ghjh])
        wosa__gsslq.append(djq__pwffg)
    has_kws = context.get_constant(types.boolean, has_kws)
    wosa__gsslq.append(has_kws)
    return lir.Constant.literal_struct(wosa__gsslq)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    ycm__jjuxi = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for vdd__kksz in ycm__jjuxi:
        if not is_overload_none(vdd__kksz):
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
        vnca__nfn = cgutils.create_struct_proxy(typ)(context, builder)
        vnca__nfn.n = args[0]
        vnca__nfn.normalize = args[1]
        vnca__nfn.years = args[2]
        vnca__nfn.months = args[3]
        vnca__nfn.weeks = args[4]
        vnca__nfn.days = args[5]
        vnca__nfn.hours = args[6]
        vnca__nfn.minutes = args[7]
        vnca__nfn.seconds = args[8]
        vnca__nfn.microseconds = args[9]
        vnca__nfn.nanoseconds = args[10]
        vnca__nfn.year = args[11]
        vnca__nfn.month = args[12]
        vnca__nfn.day = args[13]
        vnca__nfn.weekday = args[14]
        vnca__nfn.hour = args[15]
        vnca__nfn.minute = args[16]
        vnca__nfn.second = args[17]
        vnca__nfn.microsecond = args[18]
        vnca__nfn.nanosecond = args[19]
        vnca__nfn.has_kws = args[20]
        return vnca__nfn._getvalue()
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
        cqd__kzbav = -1 if dateoffset.n < 0 else 1
        for thka__pazcf in range(np.abs(dateoffset.n)):
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
            year += cqd__kzbav * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += cqd__kzbav * dateoffset._months
            year, month, hjlu__gygj = calculate_month_end_date(year, month,
                day, 0)
            if day > hjlu__gygj:
                day = hjlu__gygj
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
            yzc__wmwki = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            yzc__wmwki = yzc__wmwki + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if cqd__kzbav == -1:
                yzc__wmwki = -yzc__wmwki
            ts = ts + yzc__wmwki
            if dateoffset._weekday != -1:
                rkfp__pdvj = ts.weekday()
                qah__fnv = (dateoffset._weekday - rkfp__pdvj) % 7
                ts = ts + pd.Timedelta(days=qah__fnv)
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
        ntxu__cjmon = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, ntxu__cjmon)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        tumyi__llwbu = -1 if weekday is None else weekday
        return init_week(n, normalize, tumyi__llwbu)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        xtzlb__ivd = cgutils.create_struct_proxy(typ)(context, builder)
        xtzlb__ivd.n = args[0]
        xtzlb__ivd.normalize = args[1]
        xtzlb__ivd.weekday = args[2]
        return xtzlb__ivd._getvalue()
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
    xtzlb__ivd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    owm__nct = c.pyapi.long_from_longlong(xtzlb__ivd.n)
    odluz__njpr = c.pyapi.from_native_value(types.boolean, xtzlb__ivd.
        normalize, c.env_manager)
    teh__nlgu = c.pyapi.long_from_longlong(xtzlb__ivd.weekday)
    jlht__mvfk = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    gmn__sjss = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), xtzlb__ivd.weekday)
    with c.builder.if_else(gmn__sjss) as (fqtp__wjgm, gczjd__twl):
        with fqtp__wjgm:
            uxr__khlj = c.pyapi.call_function_objargs(jlht__mvfk, (owm__nct,
                odluz__njpr, teh__nlgu))
            ncm__yjrv = c.builder.block
        with gczjd__twl:
            eoba__zked = c.pyapi.call_function_objargs(jlht__mvfk, (
                owm__nct, odluz__njpr))
            hcpnk__ggqt = c.builder.block
    uge__nuhm = c.builder.phi(uxr__khlj.type)
    uge__nuhm.add_incoming(uxr__khlj, ncm__yjrv)
    uge__nuhm.add_incoming(eoba__zked, hcpnk__ggqt)
    c.pyapi.decref(teh__nlgu)
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    c.pyapi.decref(jlht__mvfk)
    return uge__nuhm


@unbox(WeekType)
def unbox_week(typ, val, c):
    owm__nct = c.pyapi.object_getattr_string(val, 'n')
    odluz__njpr = c.pyapi.object_getattr_string(val, 'normalize')
    teh__nlgu = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(owm__nct)
    normalize = c.pyapi.to_native_value(types.bool_, odluz__njpr).value
    gis__xkqbc = c.pyapi.make_none()
    vspr__nwgk = c.builder.icmp_unsigned('==', teh__nlgu, gis__xkqbc)
    with c.builder.if_else(vspr__nwgk) as (gczjd__twl, fqtp__wjgm):
        with fqtp__wjgm:
            uxr__khlj = c.pyapi.long_as_longlong(teh__nlgu)
            ncm__yjrv = c.builder.block
        with gczjd__twl:
            eoba__zked = lir.Constant(lir.IntType(64), -1)
            hcpnk__ggqt = c.builder.block
    uge__nuhm = c.builder.phi(uxr__khlj.type)
    uge__nuhm.add_incoming(uxr__khlj, ncm__yjrv)
    uge__nuhm.add_incoming(eoba__zked, hcpnk__ggqt)
    xtzlb__ivd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xtzlb__ivd.n = n
    xtzlb__ivd.normalize = normalize
    xtzlb__ivd.weekday = uge__nuhm
    c.pyapi.decref(owm__nct)
    c.pyapi.decref(odluz__njpr)
    c.pyapi.decref(teh__nlgu)
    adkmo__ktu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xtzlb__ivd._getvalue(), is_error=adkmo__ktu)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            pbz__tukko = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                anc__ddzaq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                anc__ddzaq = rhs
            return anc__ddzaq + pbz__tukko
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            pbz__tukko = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                anc__ddzaq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                anc__ddzaq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return anc__ddzaq + pbz__tukko
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            pbz__tukko = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + pbz__tukko
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
        fgd__ihs = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=fgd__ihs)


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
    for iyn__nmbb in date_offset_unsupported_attrs:
        vzog__msaxq = 'pandas.tseries.offsets.DateOffset.' + iyn__nmbb
        overload_attribute(DateOffsetType, iyn__nmbb)(
            create_unsupported_overload(vzog__msaxq))
    for iyn__nmbb in date_offset_unsupported:
        vzog__msaxq = 'pandas.tseries.offsets.DateOffset.' + iyn__nmbb
        overload_method(DateOffsetType, iyn__nmbb)(create_unsupported_overload
            (vzog__msaxq))


def _install_month_begin_unsupported():
    for iyn__nmbb in month_begin_unsupported_attrs:
        vzog__msaxq = 'pandas.tseries.offsets.MonthBegin.' + iyn__nmbb
        overload_attribute(MonthBeginType, iyn__nmbb)(
            create_unsupported_overload(vzog__msaxq))
    for iyn__nmbb in month_begin_unsupported:
        vzog__msaxq = 'pandas.tseries.offsets.MonthBegin.' + iyn__nmbb
        overload_method(MonthBeginType, iyn__nmbb)(create_unsupported_overload
            (vzog__msaxq))


def _install_month_end_unsupported():
    for iyn__nmbb in date_offset_unsupported_attrs:
        vzog__msaxq = 'pandas.tseries.offsets.MonthEnd.' + iyn__nmbb
        overload_attribute(MonthEndType, iyn__nmbb)(create_unsupported_overload
            (vzog__msaxq))
    for iyn__nmbb in date_offset_unsupported:
        vzog__msaxq = 'pandas.tseries.offsets.MonthEnd.' + iyn__nmbb
        overload_method(MonthEndType, iyn__nmbb)(create_unsupported_overload
            (vzog__msaxq))


def _install_week_unsupported():
    for iyn__nmbb in week_unsupported_attrs:
        vzog__msaxq = 'pandas.tseries.offsets.Week.' + iyn__nmbb
        overload_attribute(WeekType, iyn__nmbb)(create_unsupported_overload
            (vzog__msaxq))
    for iyn__nmbb in week_unsupported:
        vzog__msaxq = 'pandas.tseries.offsets.Week.' + iyn__nmbb
        overload_method(WeekType, iyn__nmbb)(create_unsupported_overload(
            vzog__msaxq))


def _install_offsets_unsupported():
    for djq__pwffg in offsets_unsupported:
        vzog__msaxq = 'pandas.tseries.offsets.' + djq__pwffg.__name__
        overload(djq__pwffg)(create_unsupported_overload(vzog__msaxq))


def _install_frequencies_unsupported():
    for djq__pwffg in frequencies_unsupported:
        vzog__msaxq = 'pandas.tseries.frequencies.' + djq__pwffg.__name__
        overload(djq__pwffg)(create_unsupported_overload(vzog__msaxq))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
