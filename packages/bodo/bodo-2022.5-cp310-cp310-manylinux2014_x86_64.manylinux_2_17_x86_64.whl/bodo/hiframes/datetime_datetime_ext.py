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
        nwcb__tjc = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, nwcb__tjc)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    nnh__fpd = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    tvw__qict = c.pyapi.long_from_longlong(nnh__fpd.year)
    lrb__ljs = c.pyapi.long_from_longlong(nnh__fpd.month)
    hpv__hhwy = c.pyapi.long_from_longlong(nnh__fpd.day)
    qivfx__cghfy = c.pyapi.long_from_longlong(nnh__fpd.hour)
    jve__hjtdf = c.pyapi.long_from_longlong(nnh__fpd.minute)
    lbyrw__myxa = c.pyapi.long_from_longlong(nnh__fpd.second)
    muwaq__xwybp = c.pyapi.long_from_longlong(nnh__fpd.microsecond)
    ziv__qct = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime))
    uqbhd__eowca = c.pyapi.call_function_objargs(ziv__qct, (tvw__qict,
        lrb__ljs, hpv__hhwy, qivfx__cghfy, jve__hjtdf, lbyrw__myxa,
        muwaq__xwybp))
    c.pyapi.decref(tvw__qict)
    c.pyapi.decref(lrb__ljs)
    c.pyapi.decref(hpv__hhwy)
    c.pyapi.decref(qivfx__cghfy)
    c.pyapi.decref(jve__hjtdf)
    c.pyapi.decref(lbyrw__myxa)
    c.pyapi.decref(muwaq__xwybp)
    c.pyapi.decref(ziv__qct)
    return uqbhd__eowca


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    tvw__qict = c.pyapi.object_getattr_string(val, 'year')
    lrb__ljs = c.pyapi.object_getattr_string(val, 'month')
    hpv__hhwy = c.pyapi.object_getattr_string(val, 'day')
    qivfx__cghfy = c.pyapi.object_getattr_string(val, 'hour')
    jve__hjtdf = c.pyapi.object_getattr_string(val, 'minute')
    lbyrw__myxa = c.pyapi.object_getattr_string(val, 'second')
    muwaq__xwybp = c.pyapi.object_getattr_string(val, 'microsecond')
    nnh__fpd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nnh__fpd.year = c.pyapi.long_as_longlong(tvw__qict)
    nnh__fpd.month = c.pyapi.long_as_longlong(lrb__ljs)
    nnh__fpd.day = c.pyapi.long_as_longlong(hpv__hhwy)
    nnh__fpd.hour = c.pyapi.long_as_longlong(qivfx__cghfy)
    nnh__fpd.minute = c.pyapi.long_as_longlong(jve__hjtdf)
    nnh__fpd.second = c.pyapi.long_as_longlong(lbyrw__myxa)
    nnh__fpd.microsecond = c.pyapi.long_as_longlong(muwaq__xwybp)
    c.pyapi.decref(tvw__qict)
    c.pyapi.decref(lrb__ljs)
    c.pyapi.decref(hpv__hhwy)
    c.pyapi.decref(qivfx__cghfy)
    c.pyapi.decref(jve__hjtdf)
    c.pyapi.decref(lbyrw__myxa)
    c.pyapi.decref(muwaq__xwybp)
    mkblf__embz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nnh__fpd._getvalue(), is_error=mkblf__embz)


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
        nnh__fpd = cgutils.create_struct_proxy(typ)(context, builder)
        nnh__fpd.year = args[0]
        nnh__fpd.month = args[1]
        nnh__fpd.day = args[2]
        nnh__fpd.hour = args[3]
        nnh__fpd.minute = args[4]
        nnh__fpd.second = args[5]
        nnh__fpd.microsecond = args[6]
        return nnh__fpd._getvalue()
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
                y, npw__wqcjh = lhs.year, rhs.year
                epcbl__kslt, lrk__xnw = lhs.month, rhs.month
                d, ymu__yxwah = lhs.day, rhs.day
                hvt__xbu, drhv__xtwe = lhs.hour, rhs.hour
                xet__mntlv, whk__wtb = lhs.minute, rhs.minute
                ppsmr__drdey, yigug__qil = lhs.second, rhs.second
                hgh__eyjw, ttp__dqihr = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, epcbl__kslt, d, hvt__xbu, xet__mntlv,
                    ppsmr__drdey, hgh__eyjw), (npw__wqcjh, lrk__xnw,
                    ymu__yxwah, drhv__xtwe, whk__wtb, yigug__qil,
                    ttp__dqihr)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            tqsd__fpg = lhs.toordinal()
            wrrri__gpril = rhs.toordinal()
            tfkk__tcle = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            lfkby__xtqd = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            yvmz__rqqs = datetime.timedelta(tqsd__fpg - wrrri__gpril, 
                tfkk__tcle - lfkby__xtqd, lhs.microsecond - rhs.microsecond)
            return yvmz__rqqs
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    ejimi__rbrur = context.make_helper(builder, fromty, value=val)
    xvzna__wsudh = cgutils.as_bool_bit(builder, ejimi__rbrur.valid)
    with builder.if_else(xvzna__wsudh) as (fnb__oxfkk, mhc__wkw):
        with fnb__oxfkk:
            aaqlt__hywhp = context.cast(builder, ejimi__rbrur.data, fromty.
                type, toty)
            xjb__oym = builder.block
        with mhc__wkw:
            ikswz__lso = numba.np.npdatetime.NAT
            qvr__wmhet = builder.block
    uqbhd__eowca = builder.phi(aaqlt__hywhp.type)
    uqbhd__eowca.add_incoming(aaqlt__hywhp, xjb__oym)
    uqbhd__eowca.add_incoming(ikswz__lso, qvr__wmhet)
    return uqbhd__eowca
