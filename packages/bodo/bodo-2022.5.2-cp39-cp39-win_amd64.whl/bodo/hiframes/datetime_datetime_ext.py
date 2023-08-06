import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hvmu__eovs = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, hvmu__eovs)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    gwnb__ofxr = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    tvtpv__utq = c.pyapi.long_from_longlong(gwnb__ofxr.year)
    okf__bpm = c.pyapi.long_from_longlong(gwnb__ofxr.month)
    anaff__sqt = c.pyapi.long_from_longlong(gwnb__ofxr.day)
    iqqwx__ffyms = c.pyapi.long_from_longlong(gwnb__ofxr.hour)
    gtphg__fzir = c.pyapi.long_from_longlong(gwnb__ofxr.minute)
    gvfz__rbzw = c.pyapi.long_from_longlong(gwnb__ofxr.second)
    eyic__tocjn = c.pyapi.long_from_longlong(gwnb__ofxr.microsecond)
    iqyx__ebjw = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    vjnoe__lpq = c.pyapi.call_function_objargs(iqyx__ebjw, (tvtpv__utq,
        okf__bpm, anaff__sqt, iqqwx__ffyms, gtphg__fzir, gvfz__rbzw,
        eyic__tocjn))
    c.pyapi.decref(tvtpv__utq)
    c.pyapi.decref(okf__bpm)
    c.pyapi.decref(anaff__sqt)
    c.pyapi.decref(iqqwx__ffyms)
    c.pyapi.decref(gtphg__fzir)
    c.pyapi.decref(gvfz__rbzw)
    c.pyapi.decref(eyic__tocjn)
    c.pyapi.decref(iqyx__ebjw)
    return vjnoe__lpq


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    tvtpv__utq = c.pyapi.object_getattr_string(val, 'year')
    okf__bpm = c.pyapi.object_getattr_string(val, 'month')
    anaff__sqt = c.pyapi.object_getattr_string(val, 'day')
    iqqwx__ffyms = c.pyapi.object_getattr_string(val, 'hour')
    gtphg__fzir = c.pyapi.object_getattr_string(val, 'minute')
    gvfz__rbzw = c.pyapi.object_getattr_string(val, 'second')
    eyic__tocjn = c.pyapi.object_getattr_string(val, 'microsecond')
    gwnb__ofxr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gwnb__ofxr.year = c.pyapi.long_as_longlong(tvtpv__utq)
    gwnb__ofxr.month = c.pyapi.long_as_longlong(okf__bpm)
    gwnb__ofxr.day = c.pyapi.long_as_longlong(anaff__sqt)
    gwnb__ofxr.hour = c.pyapi.long_as_longlong(iqqwx__ffyms)
    gwnb__ofxr.minute = c.pyapi.long_as_longlong(gtphg__fzir)
    gwnb__ofxr.second = c.pyapi.long_as_longlong(gvfz__rbzw)
    gwnb__ofxr.microsecond = c.pyapi.long_as_longlong(eyic__tocjn)
    c.pyapi.decref(tvtpv__utq)
    c.pyapi.decref(okf__bpm)
    c.pyapi.decref(anaff__sqt)
    c.pyapi.decref(iqqwx__ffyms)
    c.pyapi.decref(gtphg__fzir)
    c.pyapi.decref(gvfz__rbzw)
    c.pyapi.decref(eyic__tocjn)
    wcox__okjkm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gwnb__ofxr._getvalue(), is_error=wcox__okjkm)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        gwnb__ofxr = cgutils.create_struct_proxy(typ)(context, builder)
        gwnb__ofxr.year = args[0]
        gwnb__ofxr.month = args[1]
        gwnb__ofxr.day = args[2]
        gwnb__ofxr.hour = args[3]
        gwnb__ofxr.minute = args[4]
        gwnb__ofxr.second = args[5]
        gwnb__ofxr.microsecond = args[6]
        return gwnb__ofxr._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, qtvlt__mtyw = lhs.year, rhs.year
                aeke__bdl, jkcp__oco = lhs.month, rhs.month
                d, wod__mvob = lhs.day, rhs.day
                ejv__ehp, coo__rfht = lhs.hour, rhs.hour
                enb__ino, voccr__yzl = lhs.minute, rhs.minute
                iwssx__fiuzt, cvvch__svg = lhs.second, rhs.second
                ueusg__soh, cyw__rbkei = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, aeke__bdl, d, ejv__ehp, enb__ino,
                    iwssx__fiuzt, ueusg__soh), (qtvlt__mtyw, jkcp__oco,
                    wod__mvob, coo__rfht, voccr__yzl, cvvch__svg,
                    cyw__rbkei)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            xehri__vfy = lhs.toordinal()
            trv__fnzg = rhs.toordinal()
            fmm__wpjc = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            qhg__lkw = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            banrk__rfv = datetime.timedelta(xehri__vfy - trv__fnzg, 
                fmm__wpjc - qhg__lkw, lhs.microsecond - rhs.microsecond)
            return banrk__rfv
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    lii__dvmh = context.make_helper(builder, fromty, value=val)
    avub__uaxuu = cgutils.as_bool_bit(builder, lii__dvmh.valid)
    with builder.if_else(avub__uaxuu) as (cnf__zyiou, bou__rjr):
        with cnf__zyiou:
            cra__cpgx = context.cast(builder, lii__dvmh.data, fromty.type, toty
                )
            mtxd__kxq = builder.block
        with bou__rjr:
            gtt__suh = numba.np.npdatetime.NAT
            bdthx__gcta = builder.block
    vjnoe__lpq = builder.phi(cra__cpgx.type)
    vjnoe__lpq.add_incoming(cra__cpgx, mtxd__kxq)
    vjnoe__lpq.add_incoming(gtt__suh, bdthx__gcta)
    return vjnoe__lpq
