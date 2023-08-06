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
        nbqlo__mmtye = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, nbqlo__mmtye)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    cyb__ifa = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    gcd__qmwkk = c.pyapi.long_from_longlong(cyb__ifa.year)
    dqjo__wfcjn = c.pyapi.long_from_longlong(cyb__ifa.month)
    mjngk__bkk = c.pyapi.long_from_longlong(cyb__ifa.day)
    cxqq__ozlrh = c.pyapi.long_from_longlong(cyb__ifa.hour)
    bcm__klw = c.pyapi.long_from_longlong(cyb__ifa.minute)
    vbt__hob = c.pyapi.long_from_longlong(cyb__ifa.second)
    zex__knmh = c.pyapi.long_from_longlong(cyb__ifa.microsecond)
    zyde__kjf = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime)
        )
    aei__ricji = c.pyapi.call_function_objargs(zyde__kjf, (gcd__qmwkk,
        dqjo__wfcjn, mjngk__bkk, cxqq__ozlrh, bcm__klw, vbt__hob, zex__knmh))
    c.pyapi.decref(gcd__qmwkk)
    c.pyapi.decref(dqjo__wfcjn)
    c.pyapi.decref(mjngk__bkk)
    c.pyapi.decref(cxqq__ozlrh)
    c.pyapi.decref(bcm__klw)
    c.pyapi.decref(vbt__hob)
    c.pyapi.decref(zex__knmh)
    c.pyapi.decref(zyde__kjf)
    return aei__ricji


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    gcd__qmwkk = c.pyapi.object_getattr_string(val, 'year')
    dqjo__wfcjn = c.pyapi.object_getattr_string(val, 'month')
    mjngk__bkk = c.pyapi.object_getattr_string(val, 'day')
    cxqq__ozlrh = c.pyapi.object_getattr_string(val, 'hour')
    bcm__klw = c.pyapi.object_getattr_string(val, 'minute')
    vbt__hob = c.pyapi.object_getattr_string(val, 'second')
    zex__knmh = c.pyapi.object_getattr_string(val, 'microsecond')
    cyb__ifa = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cyb__ifa.year = c.pyapi.long_as_longlong(gcd__qmwkk)
    cyb__ifa.month = c.pyapi.long_as_longlong(dqjo__wfcjn)
    cyb__ifa.day = c.pyapi.long_as_longlong(mjngk__bkk)
    cyb__ifa.hour = c.pyapi.long_as_longlong(cxqq__ozlrh)
    cyb__ifa.minute = c.pyapi.long_as_longlong(bcm__klw)
    cyb__ifa.second = c.pyapi.long_as_longlong(vbt__hob)
    cyb__ifa.microsecond = c.pyapi.long_as_longlong(zex__knmh)
    c.pyapi.decref(gcd__qmwkk)
    c.pyapi.decref(dqjo__wfcjn)
    c.pyapi.decref(mjngk__bkk)
    c.pyapi.decref(cxqq__ozlrh)
    c.pyapi.decref(bcm__klw)
    c.pyapi.decref(vbt__hob)
    c.pyapi.decref(zex__knmh)
    fqplf__nrwmt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cyb__ifa._getvalue(), is_error=fqplf__nrwmt)


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
        cyb__ifa = cgutils.create_struct_proxy(typ)(context, builder)
        cyb__ifa.year = args[0]
        cyb__ifa.month = args[1]
        cyb__ifa.day = args[2]
        cyb__ifa.hour = args[3]
        cyb__ifa.minute = args[4]
        cyb__ifa.second = args[5]
        cyb__ifa.microsecond = args[6]
        return cyb__ifa._getvalue()
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
                y, bkyl__uadzg = lhs.year, rhs.year
                bwi__kkp, vsx__gvie = lhs.month, rhs.month
                d, qna__xutq = lhs.day, rhs.day
                ubng__nxc, kcfmx__uikdl = lhs.hour, rhs.hour
                patz__snyn, bed__yeqdh = lhs.minute, rhs.minute
                rnly__fkjsk, hdiu__qje = lhs.second, rhs.second
                dpa__fwu, fbs__wlyqa = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, bwi__kkp, d, ubng__nxc, patz__snyn,
                    rnly__fkjsk, dpa__fwu), (bkyl__uadzg, vsx__gvie,
                    qna__xutq, kcfmx__uikdl, bed__yeqdh, hdiu__qje,
                    fbs__wlyqa)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            afa__wsz = lhs.toordinal()
            vrae__gveaa = rhs.toordinal()
            kbaqv__bgehi = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            pvzmm__zyl = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            mjqrm__kwiwo = datetime.timedelta(afa__wsz - vrae__gveaa, 
                kbaqv__bgehi - pvzmm__zyl, lhs.microsecond - rhs.microsecond)
            return mjqrm__kwiwo
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    lfv__pwg = context.make_helper(builder, fromty, value=val)
    qgc__piuye = cgutils.as_bool_bit(builder, lfv__pwg.valid)
    with builder.if_else(qgc__piuye) as (chcq__kkh, epm__lipik):
        with chcq__kkh:
            efg__rscn = context.cast(builder, lfv__pwg.data, fromty.type, toty)
            qkxf__csex = builder.block
        with epm__lipik:
            dgag__xzm = numba.np.npdatetime.NAT
            fmi__iuh = builder.block
    aei__ricji = builder.phi(efg__rscn.type)
    aei__ricji.add_incoming(efg__rscn, qkxf__csex)
    aei__ricji.add_incoming(dgag__xzm, fmi__iuh)
    return aei__ricji
