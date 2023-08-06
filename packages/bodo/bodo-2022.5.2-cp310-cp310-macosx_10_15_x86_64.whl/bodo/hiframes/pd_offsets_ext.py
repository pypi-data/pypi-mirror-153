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
        dgtsr__ljra = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, dgtsr__ljra)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    bwoz__sbkdd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jrm__mzo = c.pyapi.long_from_longlong(bwoz__sbkdd.n)
    ewnf__rxcyi = c.pyapi.from_native_value(types.boolean, bwoz__sbkdd.
        normalize, c.env_manager)
    tnuv__bfkf = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    rgss__pecj = c.pyapi.call_function_objargs(tnuv__bfkf, (jrm__mzo,
        ewnf__rxcyi))
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    c.pyapi.decref(tnuv__bfkf)
    return rgss__pecj


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    jrm__mzo = c.pyapi.object_getattr_string(val, 'n')
    ewnf__rxcyi = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jrm__mzo)
    normalize = c.pyapi.to_native_value(types.bool_, ewnf__rxcyi).value
    bwoz__sbkdd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bwoz__sbkdd.n = n
    bwoz__sbkdd.normalize = normalize
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    hxhtv__rdy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bwoz__sbkdd._getvalue(), is_error=hxhtv__rdy)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        bwoz__sbkdd = cgutils.create_struct_proxy(typ)(context, builder)
        bwoz__sbkdd.n = args[0]
        bwoz__sbkdd.normalize = args[1]
        return bwoz__sbkdd._getvalue()
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
        dgtsr__ljra = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, dgtsr__ljra)


@box(MonthEndType)
def box_month_end(typ, val, c):
    iii__itv = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    jrm__mzo = c.pyapi.long_from_longlong(iii__itv.n)
    ewnf__rxcyi = c.pyapi.from_native_value(types.boolean, iii__itv.
        normalize, c.env_manager)
    fsya__nmkn = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    rgss__pecj = c.pyapi.call_function_objargs(fsya__nmkn, (jrm__mzo,
        ewnf__rxcyi))
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    c.pyapi.decref(fsya__nmkn)
    return rgss__pecj


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    jrm__mzo = c.pyapi.object_getattr_string(val, 'n')
    ewnf__rxcyi = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jrm__mzo)
    normalize = c.pyapi.to_native_value(types.bool_, ewnf__rxcyi).value
    iii__itv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    iii__itv.n = n
    iii__itv.normalize = normalize
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    hxhtv__rdy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(iii__itv._getvalue(), is_error=hxhtv__rdy)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        iii__itv = cgutils.create_struct_proxy(typ)(context, builder)
        iii__itv.n = args[0]
        iii__itv.normalize = args[1]
        return iii__itv._getvalue()
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
        iii__itv = get_days_in_month(year, month)
        if iii__itv > day:
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
        dgtsr__ljra = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, dgtsr__ljra)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    huyr__wmyt = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zdxmn__bftrk = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for hkdo__fatwj, toxc__kmqal in enumerate(date_offset_fields):
        c.builder.store(getattr(huyr__wmyt, toxc__kmqal), c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(zdxmn__bftrk, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * hkdo__fatwj)),
            lir.IntType(64).as_pointer()))
    sfpu__rlu = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    adtso__fpves = cgutils.get_or_insert_function(c.builder.module,
        sfpu__rlu, name='box_date_offset')
    dgx__alj = c.builder.call(adtso__fpves, [huyr__wmyt.n, huyr__wmyt.
        normalize, zdxmn__bftrk, huyr__wmyt.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return dgx__alj


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    jrm__mzo = c.pyapi.object_getattr_string(val, 'n')
    ewnf__rxcyi = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jrm__mzo)
    normalize = c.pyapi.to_native_value(types.bool_, ewnf__rxcyi).value
    zdxmn__bftrk = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    sfpu__rlu = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer()])
    ari__gft = cgutils.get_or_insert_function(c.builder.module, sfpu__rlu,
        name='unbox_date_offset')
    has_kws = c.builder.call(ari__gft, [val, zdxmn__bftrk])
    huyr__wmyt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    huyr__wmyt.n = n
    huyr__wmyt.normalize = normalize
    for hkdo__fatwj, toxc__kmqal in enumerate(date_offset_fields):
        setattr(huyr__wmyt, toxc__kmqal, c.builder.load(c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(zdxmn__bftrk, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * hkdo__fatwj)), lir.IntType(64
            ).as_pointer())))
    huyr__wmyt.has_kws = has_kws
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    hxhtv__rdy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(huyr__wmyt._getvalue(), is_error=hxhtv__rdy)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    cwew__kyit = [n, normalize]
    has_kws = False
    ccv__ztwh = [0] * 9 + [-1] * 9
    for hkdo__fatwj, toxc__kmqal in enumerate(date_offset_fields):
        if hasattr(pyval, toxc__kmqal):
            vrty__kllao = context.get_constant(types.int64, getattr(pyval,
                toxc__kmqal))
            has_kws = True
        else:
            vrty__kllao = context.get_constant(types.int64, ccv__ztwh[
                hkdo__fatwj])
        cwew__kyit.append(vrty__kllao)
    has_kws = context.get_constant(types.boolean, has_kws)
    cwew__kyit.append(has_kws)
    return lir.Constant.literal_struct(cwew__kyit)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    adp__ljc = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for kwklj__ouy in adp__ljc:
        if not is_overload_none(kwklj__ouy):
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
        huyr__wmyt = cgutils.create_struct_proxy(typ)(context, builder)
        huyr__wmyt.n = args[0]
        huyr__wmyt.normalize = args[1]
        huyr__wmyt.years = args[2]
        huyr__wmyt.months = args[3]
        huyr__wmyt.weeks = args[4]
        huyr__wmyt.days = args[5]
        huyr__wmyt.hours = args[6]
        huyr__wmyt.minutes = args[7]
        huyr__wmyt.seconds = args[8]
        huyr__wmyt.microseconds = args[9]
        huyr__wmyt.nanoseconds = args[10]
        huyr__wmyt.year = args[11]
        huyr__wmyt.month = args[12]
        huyr__wmyt.day = args[13]
        huyr__wmyt.weekday = args[14]
        huyr__wmyt.hour = args[15]
        huyr__wmyt.minute = args[16]
        huyr__wmyt.second = args[17]
        huyr__wmyt.microsecond = args[18]
        huyr__wmyt.nanosecond = args[19]
        huyr__wmyt.has_kws = args[20]
        return huyr__wmyt._getvalue()
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
        iqc__eayst = -1 if dateoffset.n < 0 else 1
        for bmc__wxdf in range(np.abs(dateoffset.n)):
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
            year += iqc__eayst * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += iqc__eayst * dateoffset._months
            year, month, vyabg__lyq = calculate_month_end_date(year, month,
                day, 0)
            if day > vyabg__lyq:
                day = vyabg__lyq
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
            xqa__kztha = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            xqa__kztha = xqa__kztha + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if iqc__eayst == -1:
                xqa__kztha = -xqa__kztha
            ts = ts + xqa__kztha
            if dateoffset._weekday != -1:
                qscnb__xrfuh = ts.weekday()
                jqayg__rdjqa = (dateoffset._weekday - qscnb__xrfuh) % 7
                ts = ts + pd.Timedelta(days=jqayg__rdjqa)
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
        dgtsr__ljra = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, dgtsr__ljra)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        ome__yev = -1 if weekday is None else weekday
        return init_week(n, normalize, ome__yev)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        dztf__etafd = cgutils.create_struct_proxy(typ)(context, builder)
        dztf__etafd.n = args[0]
        dztf__etafd.normalize = args[1]
        dztf__etafd.weekday = args[2]
        return dztf__etafd._getvalue()
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
    dztf__etafd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jrm__mzo = c.pyapi.long_from_longlong(dztf__etafd.n)
    ewnf__rxcyi = c.pyapi.from_native_value(types.boolean, dztf__etafd.
        normalize, c.env_manager)
    inqgb__ceh = c.pyapi.long_from_longlong(dztf__etafd.weekday)
    vaa__cuptj = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    thloi__dfxe = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64),
        -1), dztf__etafd.weekday)
    with c.builder.if_else(thloi__dfxe) as (vuz__ylgdu, svw__dyiuv):
        with vuz__ylgdu:
            tbldb__fgiu = c.pyapi.call_function_objargs(vaa__cuptj, (
                jrm__mzo, ewnf__rxcyi, inqgb__ceh))
            bxpf__ven = c.builder.block
        with svw__dyiuv:
            kar__gwoye = c.pyapi.call_function_objargs(vaa__cuptj, (
                jrm__mzo, ewnf__rxcyi))
            ddfe__lzarh = c.builder.block
    rgss__pecj = c.builder.phi(tbldb__fgiu.type)
    rgss__pecj.add_incoming(tbldb__fgiu, bxpf__ven)
    rgss__pecj.add_incoming(kar__gwoye, ddfe__lzarh)
    c.pyapi.decref(inqgb__ceh)
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    c.pyapi.decref(vaa__cuptj)
    return rgss__pecj


@unbox(WeekType)
def unbox_week(typ, val, c):
    jrm__mzo = c.pyapi.object_getattr_string(val, 'n')
    ewnf__rxcyi = c.pyapi.object_getattr_string(val, 'normalize')
    inqgb__ceh = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(jrm__mzo)
    normalize = c.pyapi.to_native_value(types.bool_, ewnf__rxcyi).value
    jntms__xkbm = c.pyapi.make_none()
    ozc__uyt = c.builder.icmp_unsigned('==', inqgb__ceh, jntms__xkbm)
    with c.builder.if_else(ozc__uyt) as (svw__dyiuv, vuz__ylgdu):
        with vuz__ylgdu:
            tbldb__fgiu = c.pyapi.long_as_longlong(inqgb__ceh)
            bxpf__ven = c.builder.block
        with svw__dyiuv:
            kar__gwoye = lir.Constant(lir.IntType(64), -1)
            ddfe__lzarh = c.builder.block
    rgss__pecj = c.builder.phi(tbldb__fgiu.type)
    rgss__pecj.add_incoming(tbldb__fgiu, bxpf__ven)
    rgss__pecj.add_incoming(kar__gwoye, ddfe__lzarh)
    dztf__etafd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    dztf__etafd.n = n
    dztf__etafd.normalize = normalize
    dztf__etafd.weekday = rgss__pecj
    c.pyapi.decref(jrm__mzo)
    c.pyapi.decref(ewnf__rxcyi)
    c.pyapi.decref(inqgb__ceh)
    hxhtv__rdy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dztf__etafd._getvalue(), is_error=hxhtv__rdy)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ljnyk__lseg = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                rnvbh__tpkq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                rnvbh__tpkq = rhs
            return rnvbh__tpkq + ljnyk__lseg
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            ljnyk__lseg = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                rnvbh__tpkq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                rnvbh__tpkq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return rnvbh__tpkq + ljnyk__lseg
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            ljnyk__lseg = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            return rhs + ljnyk__lseg
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
        ubyu__mzf = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=ubyu__mzf)


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
    for dwjm__uzoje in date_offset_unsupported_attrs:
        rigpv__jypyb = 'pandas.tseries.offsets.DateOffset.' + dwjm__uzoje
        overload_attribute(DateOffsetType, dwjm__uzoje)(
            create_unsupported_overload(rigpv__jypyb))
    for dwjm__uzoje in date_offset_unsupported:
        rigpv__jypyb = 'pandas.tseries.offsets.DateOffset.' + dwjm__uzoje
        overload_method(DateOffsetType, dwjm__uzoje)(
            create_unsupported_overload(rigpv__jypyb))


def _install_month_begin_unsupported():
    for dwjm__uzoje in month_begin_unsupported_attrs:
        rigpv__jypyb = 'pandas.tseries.offsets.MonthBegin.' + dwjm__uzoje
        overload_attribute(MonthBeginType, dwjm__uzoje)(
            create_unsupported_overload(rigpv__jypyb))
    for dwjm__uzoje in month_begin_unsupported:
        rigpv__jypyb = 'pandas.tseries.offsets.MonthBegin.' + dwjm__uzoje
        overload_method(MonthBeginType, dwjm__uzoje)(
            create_unsupported_overload(rigpv__jypyb))


def _install_month_end_unsupported():
    for dwjm__uzoje in date_offset_unsupported_attrs:
        rigpv__jypyb = 'pandas.tseries.offsets.MonthEnd.' + dwjm__uzoje
        overload_attribute(MonthEndType, dwjm__uzoje)(
            create_unsupported_overload(rigpv__jypyb))
    for dwjm__uzoje in date_offset_unsupported:
        rigpv__jypyb = 'pandas.tseries.offsets.MonthEnd.' + dwjm__uzoje
        overload_method(MonthEndType, dwjm__uzoje)(create_unsupported_overload
            (rigpv__jypyb))


def _install_week_unsupported():
    for dwjm__uzoje in week_unsupported_attrs:
        rigpv__jypyb = 'pandas.tseries.offsets.Week.' + dwjm__uzoje
        overload_attribute(WeekType, dwjm__uzoje)(create_unsupported_overload
            (rigpv__jypyb))
    for dwjm__uzoje in week_unsupported:
        rigpv__jypyb = 'pandas.tseries.offsets.Week.' + dwjm__uzoje
        overload_method(WeekType, dwjm__uzoje)(create_unsupported_overload(
            rigpv__jypyb))


def _install_offsets_unsupported():
    for vrty__kllao in offsets_unsupported:
        rigpv__jypyb = 'pandas.tseries.offsets.' + vrty__kllao.__name__
        overload(vrty__kllao)(create_unsupported_overload(rigpv__jypyb))


def _install_frequencies_unsupported():
    for vrty__kllao in frequencies_unsupported:
        rigpv__jypyb = 'pandas.tseries.frequencies.' + vrty__kllao.__name__
        overload(vrty__kllao)(create_unsupported_overload(rigpv__jypyb))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
