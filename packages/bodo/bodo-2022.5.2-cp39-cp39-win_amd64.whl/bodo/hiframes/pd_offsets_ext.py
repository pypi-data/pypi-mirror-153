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
        orl__njeai = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, orl__njeai)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    izx__teuxj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    kvjz__nky = c.pyapi.long_from_longlong(izx__teuxj.n)
    eucgt__snel = c.pyapi.from_native_value(types.boolean, izx__teuxj.
        normalize, c.env_manager)
    rxxpv__uxrsu = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    zhm__mhvsm = c.pyapi.call_function_objargs(rxxpv__uxrsu, (kvjz__nky,
        eucgt__snel))
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    c.pyapi.decref(rxxpv__uxrsu)
    return zhm__mhvsm


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    kvjz__nky = c.pyapi.object_getattr_string(val, 'n')
    eucgt__snel = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(kvjz__nky)
    normalize = c.pyapi.to_native_value(types.bool_, eucgt__snel).value
    izx__teuxj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    izx__teuxj.n = n
    izx__teuxj.normalize = normalize
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    amzr__cak = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(izx__teuxj._getvalue(), is_error=amzr__cak)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        izx__teuxj = cgutils.create_struct_proxy(typ)(context, builder)
        izx__teuxj.n = args[0]
        izx__teuxj.normalize = args[1]
        return izx__teuxj._getvalue()
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
        orl__njeai = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, orl__njeai)


@box(MonthEndType)
def box_month_end(typ, val, c):
    vcc__bsrm = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    kvjz__nky = c.pyapi.long_from_longlong(vcc__bsrm.n)
    eucgt__snel = c.pyapi.from_native_value(types.boolean, vcc__bsrm.
        normalize, c.env_manager)
    ftj__mqsfu = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    zhm__mhvsm = c.pyapi.call_function_objargs(ftj__mqsfu, (kvjz__nky,
        eucgt__snel))
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    c.pyapi.decref(ftj__mqsfu)
    return zhm__mhvsm


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    kvjz__nky = c.pyapi.object_getattr_string(val, 'n')
    eucgt__snel = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(kvjz__nky)
    normalize = c.pyapi.to_native_value(types.bool_, eucgt__snel).value
    vcc__bsrm = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vcc__bsrm.n = n
    vcc__bsrm.normalize = normalize
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    amzr__cak = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vcc__bsrm._getvalue(), is_error=amzr__cak)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        vcc__bsrm = cgutils.create_struct_proxy(typ)(context, builder)
        vcc__bsrm.n = args[0]
        vcc__bsrm.normalize = args[1]
        return vcc__bsrm._getvalue()
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
        vcc__bsrm = get_days_in_month(year, month)
        if vcc__bsrm > day:
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
        orl__njeai = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, orl__njeai)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    fwmb__ejjc = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    xrnks__nxi = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for znxqu__egzh, nfzaj__eef in enumerate(date_offset_fields):
        c.builder.store(getattr(fwmb__ejjc, nfzaj__eef), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(xrnks__nxi, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * znxqu__egzh)), lir.IntType(64
            ).as_pointer()))
    kiagc__tkpr = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    cypbz__dlc = cgutils.get_or_insert_function(c.builder.module,
        kiagc__tkpr, name='box_date_offset')
    ybru__vqh = c.builder.call(cypbz__dlc, [fwmb__ejjc.n, fwmb__ejjc.
        normalize, xrnks__nxi, fwmb__ejjc.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return ybru__vqh


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    kvjz__nky = c.pyapi.object_getattr_string(val, 'n')
    eucgt__snel = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(kvjz__nky)
    normalize = c.pyapi.to_native_value(types.bool_, eucgt__snel).value
    xrnks__nxi = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    kiagc__tkpr = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    cpoph__lkb = cgutils.get_or_insert_function(c.builder.module,
        kiagc__tkpr, name='unbox_date_offset')
    has_kws = c.builder.call(cpoph__lkb, [val, xrnks__nxi])
    fwmb__ejjc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fwmb__ejjc.n = n
    fwmb__ejjc.normalize = normalize
    for znxqu__egzh, nfzaj__eef in enumerate(date_offset_fields):
        setattr(fwmb__ejjc, nfzaj__eef, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(xrnks__nxi, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * znxqu__egzh)), lir.IntType(64
            ).as_pointer())))
    fwmb__ejjc.has_kws = has_kws
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    amzr__cak = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fwmb__ejjc._getvalue(), is_error=amzr__cak)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    duns__vcu = [n, normalize]
    has_kws = False
    zuo__elve = [0] * 9 + [-1] * 9
    for znxqu__egzh, nfzaj__eef in enumerate(date_offset_fields):
        if hasattr(pyval, nfzaj__eef):
            npl__vbc = context.get_constant(types.int64, getattr(pyval,
                nfzaj__eef))
            has_kws = True
        else:
            npl__vbc = context.get_constant(types.int64, zuo__elve[znxqu__egzh]
                )
        duns__vcu.append(npl__vbc)
    has_kws = context.get_constant(types.boolean, has_kws)
    duns__vcu.append(has_kws)
    return lir.Constant.literal_struct(duns__vcu)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    skhg__edn = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for mls__osd in skhg__edn:
        if not is_overload_none(mls__osd):
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
        fwmb__ejjc = cgutils.create_struct_proxy(typ)(context, builder)
        fwmb__ejjc.n = args[0]
        fwmb__ejjc.normalize = args[1]
        fwmb__ejjc.years = args[2]
        fwmb__ejjc.months = args[3]
        fwmb__ejjc.weeks = args[4]
        fwmb__ejjc.days = args[5]
        fwmb__ejjc.hours = args[6]
        fwmb__ejjc.minutes = args[7]
        fwmb__ejjc.seconds = args[8]
        fwmb__ejjc.microseconds = args[9]
        fwmb__ejjc.nanoseconds = args[10]
        fwmb__ejjc.year = args[11]
        fwmb__ejjc.month = args[12]
        fwmb__ejjc.day = args[13]
        fwmb__ejjc.weekday = args[14]
        fwmb__ejjc.hour = args[15]
        fwmb__ejjc.minute = args[16]
        fwmb__ejjc.second = args[17]
        fwmb__ejjc.microsecond = args[18]
        fwmb__ejjc.nanosecond = args[19]
        fwmb__ejjc.has_kws = args[20]
        return fwmb__ejjc._getvalue()
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
        uyaf__pkloy = -1 if dateoffset.n < 0 else 1
        for nwogv__kqr in range(np.abs(dateoffset.n)):
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
            year += uyaf__pkloy * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += uyaf__pkloy * dateoffset._months
            year, month, apppu__ixxs = calculate_month_end_date(year, month,
                day, 0)
            if day > apppu__ixxs:
                day = apppu__ixxs
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
            ekxu__cvf = pd.Timedelta(days=dateoffset._days + 7 * dateoffset
                ._weeks, hours=dateoffset._hours, minutes=dateoffset.
                _minutes, seconds=dateoffset._seconds, microseconds=
                dateoffset._microseconds)
            ekxu__cvf = ekxu__cvf + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if uyaf__pkloy == -1:
                ekxu__cvf = -ekxu__cvf
            ts = ts + ekxu__cvf
            if dateoffset._weekday != -1:
                vqev__rtfzg = ts.weekday()
                hja__gzd = (dateoffset._weekday - vqev__rtfzg) % 7
                ts = ts + pd.Timedelta(days=hja__gzd)
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
        orl__njeai = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, orl__njeai)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        sgwdm__apfi = -1 if weekday is None else weekday
        return init_week(n, normalize, sgwdm__apfi)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        nyw__noax = cgutils.create_struct_proxy(typ)(context, builder)
        nyw__noax.n = args[0]
        nyw__noax.normalize = args[1]
        nyw__noax.weekday = args[2]
        return nyw__noax._getvalue()
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
    nyw__noax = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    kvjz__nky = c.pyapi.long_from_longlong(nyw__noax.n)
    eucgt__snel = c.pyapi.from_native_value(types.boolean, nyw__noax.
        normalize, c.env_manager)
    gfyz__okyw = c.pyapi.long_from_longlong(nyw__noax.weekday)
    tclj__rlcn = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    xznuh__mija = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64),
        -1), nyw__noax.weekday)
    with c.builder.if_else(xznuh__mija) as (lqbg__orhkl, rfra__bgpvl):
        with lqbg__orhkl:
            sxg__ygz = c.pyapi.call_function_objargs(tclj__rlcn, (kvjz__nky,
                eucgt__snel, gfyz__okyw))
            vhwc__qvgtr = c.builder.block
        with rfra__bgpvl:
            kmhmx__csp = c.pyapi.call_function_objargs(tclj__rlcn, (
                kvjz__nky, eucgt__snel))
            tirdw__yiqu = c.builder.block
    zhm__mhvsm = c.builder.phi(sxg__ygz.type)
    zhm__mhvsm.add_incoming(sxg__ygz, vhwc__qvgtr)
    zhm__mhvsm.add_incoming(kmhmx__csp, tirdw__yiqu)
    c.pyapi.decref(gfyz__okyw)
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    c.pyapi.decref(tclj__rlcn)
    return zhm__mhvsm


@unbox(WeekType)
def unbox_week(typ, val, c):
    kvjz__nky = c.pyapi.object_getattr_string(val, 'n')
    eucgt__snel = c.pyapi.object_getattr_string(val, 'normalize')
    gfyz__okyw = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(kvjz__nky)
    normalize = c.pyapi.to_native_value(types.bool_, eucgt__snel).value
    xpf__ent = c.pyapi.make_none()
    byayr__dln = c.builder.icmp_unsigned('==', gfyz__okyw, xpf__ent)
    with c.builder.if_else(byayr__dln) as (rfra__bgpvl, lqbg__orhkl):
        with lqbg__orhkl:
            sxg__ygz = c.pyapi.long_as_longlong(gfyz__okyw)
            vhwc__qvgtr = c.builder.block
        with rfra__bgpvl:
            kmhmx__csp = lir.Constant(lir.IntType(64), -1)
            tirdw__yiqu = c.builder.block
    zhm__mhvsm = c.builder.phi(sxg__ygz.type)
    zhm__mhvsm.add_incoming(sxg__ygz, vhwc__qvgtr)
    zhm__mhvsm.add_incoming(kmhmx__csp, tirdw__yiqu)
    nyw__noax = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nyw__noax.n = n
    nyw__noax.normalize = normalize
    nyw__noax.weekday = zhm__mhvsm
    c.pyapi.decref(kvjz__nky)
    c.pyapi.decref(eucgt__snel)
    c.pyapi.decref(gfyz__okyw)
    amzr__cak = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nyw__noax._getvalue(), is_error=amzr__cak)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            qinm__vqsns = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                oamk__pbin = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                oamk__pbin = rhs
            return oamk__pbin + qinm__vqsns
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            qinm__vqsns = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                oamk__pbin = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                oamk__pbin = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return oamk__pbin + qinm__vqsns
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            qinm__vqsns = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            return rhs + qinm__vqsns
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
        nmh__bsrb = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=nmh__bsrb)


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
    for wgo__ieiy in date_offset_unsupported_attrs:
        eaq__wbgs = 'pandas.tseries.offsets.DateOffset.' + wgo__ieiy
        overload_attribute(DateOffsetType, wgo__ieiy)(
            create_unsupported_overload(eaq__wbgs))
    for wgo__ieiy in date_offset_unsupported:
        eaq__wbgs = 'pandas.tseries.offsets.DateOffset.' + wgo__ieiy
        overload_method(DateOffsetType, wgo__ieiy)(create_unsupported_overload
            (eaq__wbgs))


def _install_month_begin_unsupported():
    for wgo__ieiy in month_begin_unsupported_attrs:
        eaq__wbgs = 'pandas.tseries.offsets.MonthBegin.' + wgo__ieiy
        overload_attribute(MonthBeginType, wgo__ieiy)(
            create_unsupported_overload(eaq__wbgs))
    for wgo__ieiy in month_begin_unsupported:
        eaq__wbgs = 'pandas.tseries.offsets.MonthBegin.' + wgo__ieiy
        overload_method(MonthBeginType, wgo__ieiy)(create_unsupported_overload
            (eaq__wbgs))


def _install_month_end_unsupported():
    for wgo__ieiy in date_offset_unsupported_attrs:
        eaq__wbgs = 'pandas.tseries.offsets.MonthEnd.' + wgo__ieiy
        overload_attribute(MonthEndType, wgo__ieiy)(create_unsupported_overload
            (eaq__wbgs))
    for wgo__ieiy in date_offset_unsupported:
        eaq__wbgs = 'pandas.tseries.offsets.MonthEnd.' + wgo__ieiy
        overload_method(MonthEndType, wgo__ieiy)(create_unsupported_overload
            (eaq__wbgs))


def _install_week_unsupported():
    for wgo__ieiy in week_unsupported_attrs:
        eaq__wbgs = 'pandas.tseries.offsets.Week.' + wgo__ieiy
        overload_attribute(WeekType, wgo__ieiy)(create_unsupported_overload
            (eaq__wbgs))
    for wgo__ieiy in week_unsupported:
        eaq__wbgs = 'pandas.tseries.offsets.Week.' + wgo__ieiy
        overload_method(WeekType, wgo__ieiy)(create_unsupported_overload(
            eaq__wbgs))


def _install_offsets_unsupported():
    for npl__vbc in offsets_unsupported:
        eaq__wbgs = 'pandas.tseries.offsets.' + npl__vbc.__name__
        overload(npl__vbc)(create_unsupported_overload(eaq__wbgs))


def _install_frequencies_unsupported():
    for npl__vbc in frequencies_unsupported:
        eaq__wbgs = 'pandas.tseries.frequencies.' + npl__vbc.__name__
        overload(npl__vbc)(create_unsupported_overload(eaq__wbgs))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
