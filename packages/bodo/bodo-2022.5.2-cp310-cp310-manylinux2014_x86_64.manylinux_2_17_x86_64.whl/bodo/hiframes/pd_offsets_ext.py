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
        zjuiu__nwh = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, zjuiu__nwh)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    yuklx__cjck = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    pmwg__cpo = c.pyapi.long_from_longlong(yuklx__cjck.n)
    mczf__smktw = c.pyapi.from_native_value(types.boolean, yuklx__cjck.
        normalize, c.env_manager)
    cvhfg__rgtg = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    nxn__mqzgf = c.pyapi.call_function_objargs(cvhfg__rgtg, (pmwg__cpo,
        mczf__smktw))
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    c.pyapi.decref(cvhfg__rgtg)
    return nxn__mqzgf


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    pmwg__cpo = c.pyapi.object_getattr_string(val, 'n')
    mczf__smktw = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(pmwg__cpo)
    normalize = c.pyapi.to_native_value(types.bool_, mczf__smktw).value
    yuklx__cjck = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yuklx__cjck.n = n
    yuklx__cjck.normalize = normalize
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    citif__ryf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yuklx__cjck._getvalue(), is_error=citif__ryf)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        yuklx__cjck = cgutils.create_struct_proxy(typ)(context, builder)
        yuklx__cjck.n = args[0]
        yuklx__cjck.normalize = args[1]
        return yuklx__cjck._getvalue()
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
        zjuiu__nwh = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, zjuiu__nwh)


@box(MonthEndType)
def box_month_end(typ, val, c):
    pds__jwluf = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    pmwg__cpo = c.pyapi.long_from_longlong(pds__jwluf.n)
    mczf__smktw = c.pyapi.from_native_value(types.boolean, pds__jwluf.
        normalize, c.env_manager)
    mvxek__vle = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    nxn__mqzgf = c.pyapi.call_function_objargs(mvxek__vle, (pmwg__cpo,
        mczf__smktw))
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    c.pyapi.decref(mvxek__vle)
    return nxn__mqzgf


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    pmwg__cpo = c.pyapi.object_getattr_string(val, 'n')
    mczf__smktw = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(pmwg__cpo)
    normalize = c.pyapi.to_native_value(types.bool_, mczf__smktw).value
    pds__jwluf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pds__jwluf.n = n
    pds__jwluf.normalize = normalize
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    citif__ryf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pds__jwluf._getvalue(), is_error=citif__ryf)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        pds__jwluf = cgutils.create_struct_proxy(typ)(context, builder)
        pds__jwluf.n = args[0]
        pds__jwluf.normalize = args[1]
        return pds__jwluf._getvalue()
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
        pds__jwluf = get_days_in_month(year, month)
        if pds__jwluf > day:
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
        zjuiu__nwh = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, zjuiu__nwh)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    csjcr__jwbrp = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cuyk__nau = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for arv__hhyt, nuaf__lozhz in enumerate(date_offset_fields):
        c.builder.store(getattr(csjcr__jwbrp, nuaf__lozhz), c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(cuyk__nau, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * arv__hhyt)),
            lir.IntType(64).as_pointer()))
    wgq__dda = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    qnf__ksiqr = cgutils.get_or_insert_function(c.builder.module, wgq__dda,
        name='box_date_offset')
    npvpr__dgho = c.builder.call(qnf__ksiqr, [csjcr__jwbrp.n, csjcr__jwbrp.
        normalize, cuyk__nau, csjcr__jwbrp.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return npvpr__dgho


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    pmwg__cpo = c.pyapi.object_getattr_string(val, 'n')
    mczf__smktw = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(pmwg__cpo)
    normalize = c.pyapi.to_native_value(types.bool_, mczf__smktw).value
    cuyk__nau = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    wgq__dda = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64).as_pointer()])
    sfkpb__mxfqj = cgutils.get_or_insert_function(c.builder.module,
        wgq__dda, name='unbox_date_offset')
    has_kws = c.builder.call(sfkpb__mxfqj, [val, cuyk__nau])
    csjcr__jwbrp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    csjcr__jwbrp.n = n
    csjcr__jwbrp.normalize = normalize
    for arv__hhyt, nuaf__lozhz in enumerate(date_offset_fields):
        setattr(csjcr__jwbrp, nuaf__lozhz, c.builder.load(c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(cuyk__nau, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * arv__hhyt)),
            lir.IntType(64).as_pointer())))
    csjcr__jwbrp.has_kws = has_kws
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    citif__ryf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(csjcr__jwbrp._getvalue(), is_error=citif__ryf)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    ace__cakx = [n, normalize]
    has_kws = False
    jbjsi__laba = [0] * 9 + [-1] * 9
    for arv__hhyt, nuaf__lozhz in enumerate(date_offset_fields):
        if hasattr(pyval, nuaf__lozhz):
            fzvnh__cutw = context.get_constant(types.int64, getattr(pyval,
                nuaf__lozhz))
            has_kws = True
        else:
            fzvnh__cutw = context.get_constant(types.int64, jbjsi__laba[
                arv__hhyt])
        ace__cakx.append(fzvnh__cutw)
    has_kws = context.get_constant(types.boolean, has_kws)
    ace__cakx.append(has_kws)
    return lir.Constant.literal_struct(ace__cakx)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    dlg__anxo = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for oik__uzy in dlg__anxo:
        if not is_overload_none(oik__uzy):
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
        csjcr__jwbrp = cgutils.create_struct_proxy(typ)(context, builder)
        csjcr__jwbrp.n = args[0]
        csjcr__jwbrp.normalize = args[1]
        csjcr__jwbrp.years = args[2]
        csjcr__jwbrp.months = args[3]
        csjcr__jwbrp.weeks = args[4]
        csjcr__jwbrp.days = args[5]
        csjcr__jwbrp.hours = args[6]
        csjcr__jwbrp.minutes = args[7]
        csjcr__jwbrp.seconds = args[8]
        csjcr__jwbrp.microseconds = args[9]
        csjcr__jwbrp.nanoseconds = args[10]
        csjcr__jwbrp.year = args[11]
        csjcr__jwbrp.month = args[12]
        csjcr__jwbrp.day = args[13]
        csjcr__jwbrp.weekday = args[14]
        csjcr__jwbrp.hour = args[15]
        csjcr__jwbrp.minute = args[16]
        csjcr__jwbrp.second = args[17]
        csjcr__jwbrp.microsecond = args[18]
        csjcr__jwbrp.nanosecond = args[19]
        csjcr__jwbrp.has_kws = args[20]
        return csjcr__jwbrp._getvalue()
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
        dtcm__dxit = -1 if dateoffset.n < 0 else 1
        for zwvge__aper in range(np.abs(dateoffset.n)):
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
            year += dtcm__dxit * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += dtcm__dxit * dateoffset._months
            year, month, uubm__tap = calculate_month_end_date(year, month,
                day, 0)
            if day > uubm__tap:
                day = uubm__tap
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
            nttnv__yxtg = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            nttnv__yxtg = nttnv__yxtg + pd.Timedelta(dateoffset.
                _nanoseconds, unit='ns')
            if dtcm__dxit == -1:
                nttnv__yxtg = -nttnv__yxtg
            ts = ts + nttnv__yxtg
            if dateoffset._weekday != -1:
                gfa__qoza = ts.weekday()
                cdls__psui = (dateoffset._weekday - gfa__qoza) % 7
                ts = ts + pd.Timedelta(days=cdls__psui)
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
        zjuiu__nwh = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, zjuiu__nwh)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        yak__ckvlr = -1 if weekday is None else weekday
        return init_week(n, normalize, yak__ckvlr)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        axz__lql = cgutils.create_struct_proxy(typ)(context, builder)
        axz__lql.n = args[0]
        axz__lql.normalize = args[1]
        axz__lql.weekday = args[2]
        return axz__lql._getvalue()
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
    axz__lql = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    pmwg__cpo = c.pyapi.long_from_longlong(axz__lql.n)
    mczf__smktw = c.pyapi.from_native_value(types.boolean, axz__lql.
        normalize, c.env_manager)
    selfs__vufc = c.pyapi.long_from_longlong(axz__lql.weekday)
    wxrue__okgwh = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    bksy__sjp = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), axz__lql.weekday)
    with c.builder.if_else(bksy__sjp) as (dvyr__bjis, baz__xyht):
        with dvyr__bjis:
            yjz__izn = c.pyapi.call_function_objargs(wxrue__okgwh, (
                pmwg__cpo, mczf__smktw, selfs__vufc))
            edd__kzo = c.builder.block
        with baz__xyht:
            jml__lwhu = c.pyapi.call_function_objargs(wxrue__okgwh, (
                pmwg__cpo, mczf__smktw))
            xfxgl__lcp = c.builder.block
    nxn__mqzgf = c.builder.phi(yjz__izn.type)
    nxn__mqzgf.add_incoming(yjz__izn, edd__kzo)
    nxn__mqzgf.add_incoming(jml__lwhu, xfxgl__lcp)
    c.pyapi.decref(selfs__vufc)
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    c.pyapi.decref(wxrue__okgwh)
    return nxn__mqzgf


@unbox(WeekType)
def unbox_week(typ, val, c):
    pmwg__cpo = c.pyapi.object_getattr_string(val, 'n')
    mczf__smktw = c.pyapi.object_getattr_string(val, 'normalize')
    selfs__vufc = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(pmwg__cpo)
    normalize = c.pyapi.to_native_value(types.bool_, mczf__smktw).value
    nvvlu__fypzt = c.pyapi.make_none()
    dtc__bvla = c.builder.icmp_unsigned('==', selfs__vufc, nvvlu__fypzt)
    with c.builder.if_else(dtc__bvla) as (baz__xyht, dvyr__bjis):
        with dvyr__bjis:
            yjz__izn = c.pyapi.long_as_longlong(selfs__vufc)
            edd__kzo = c.builder.block
        with baz__xyht:
            jml__lwhu = lir.Constant(lir.IntType(64), -1)
            xfxgl__lcp = c.builder.block
    nxn__mqzgf = c.builder.phi(yjz__izn.type)
    nxn__mqzgf.add_incoming(yjz__izn, edd__kzo)
    nxn__mqzgf.add_incoming(jml__lwhu, xfxgl__lcp)
    axz__lql = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    axz__lql.n = n
    axz__lql.normalize = normalize
    axz__lql.weekday = nxn__mqzgf
    c.pyapi.decref(pmwg__cpo)
    c.pyapi.decref(mczf__smktw)
    c.pyapi.decref(selfs__vufc)
    citif__ryf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(axz__lql._getvalue(), is_error=citif__ryf)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            oxgga__vhins = calculate_week_date(lhs.n, lhs.weekday, rhs.
                weekday())
            if lhs.normalize:
                dhcd__uhbwx = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                dhcd__uhbwx = rhs
            return dhcd__uhbwx + oxgga__vhins
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            oxgga__vhins = calculate_week_date(lhs.n, lhs.weekday, rhs.
                weekday())
            if lhs.normalize:
                dhcd__uhbwx = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                dhcd__uhbwx = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return dhcd__uhbwx + oxgga__vhins
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            oxgga__vhins = calculate_week_date(lhs.n, lhs.weekday, rhs.
                weekday())
            return rhs + oxgga__vhins
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
        vfk__fode = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=vfk__fode)


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
    for foh__xbk in date_offset_unsupported_attrs:
        iab__vfqh = 'pandas.tseries.offsets.DateOffset.' + foh__xbk
        overload_attribute(DateOffsetType, foh__xbk)(
            create_unsupported_overload(iab__vfqh))
    for foh__xbk in date_offset_unsupported:
        iab__vfqh = 'pandas.tseries.offsets.DateOffset.' + foh__xbk
        overload_method(DateOffsetType, foh__xbk)(create_unsupported_overload
            (iab__vfqh))


def _install_month_begin_unsupported():
    for foh__xbk in month_begin_unsupported_attrs:
        iab__vfqh = 'pandas.tseries.offsets.MonthBegin.' + foh__xbk
        overload_attribute(MonthBeginType, foh__xbk)(
            create_unsupported_overload(iab__vfqh))
    for foh__xbk in month_begin_unsupported:
        iab__vfqh = 'pandas.tseries.offsets.MonthBegin.' + foh__xbk
        overload_method(MonthBeginType, foh__xbk)(create_unsupported_overload
            (iab__vfqh))


def _install_month_end_unsupported():
    for foh__xbk in date_offset_unsupported_attrs:
        iab__vfqh = 'pandas.tseries.offsets.MonthEnd.' + foh__xbk
        overload_attribute(MonthEndType, foh__xbk)(create_unsupported_overload
            (iab__vfqh))
    for foh__xbk in date_offset_unsupported:
        iab__vfqh = 'pandas.tseries.offsets.MonthEnd.' + foh__xbk
        overload_method(MonthEndType, foh__xbk)(create_unsupported_overload
            (iab__vfqh))


def _install_week_unsupported():
    for foh__xbk in week_unsupported_attrs:
        iab__vfqh = 'pandas.tseries.offsets.Week.' + foh__xbk
        overload_attribute(WeekType, foh__xbk)(create_unsupported_overload(
            iab__vfqh))
    for foh__xbk in week_unsupported:
        iab__vfqh = 'pandas.tseries.offsets.Week.' + foh__xbk
        overload_method(WeekType, foh__xbk)(create_unsupported_overload(
            iab__vfqh))


def _install_offsets_unsupported():
    for fzvnh__cutw in offsets_unsupported:
        iab__vfqh = 'pandas.tseries.offsets.' + fzvnh__cutw.__name__
        overload(fzvnh__cutw)(create_unsupported_overload(iab__vfqh))


def _install_frequencies_unsupported():
    for fzvnh__cutw in frequencies_unsupported:
        iab__vfqh = 'pandas.tseries.frequencies.' + fzvnh__cutw.__name__
        overload(fzvnh__cutw)(create_unsupported_overload(iab__vfqh))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
