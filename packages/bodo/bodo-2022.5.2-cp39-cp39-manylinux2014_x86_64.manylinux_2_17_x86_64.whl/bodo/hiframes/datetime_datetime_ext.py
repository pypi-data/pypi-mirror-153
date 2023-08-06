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
        hdyny__usa = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, hdyny__usa)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    mbl__wwts = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    qnuo__uem = c.pyapi.long_from_longlong(mbl__wwts.year)
    zcv__idmzo = c.pyapi.long_from_longlong(mbl__wwts.month)
    uwiy__tpzia = c.pyapi.long_from_longlong(mbl__wwts.day)
    byeg__lia = c.pyapi.long_from_longlong(mbl__wwts.hour)
    xlj__mxw = c.pyapi.long_from_longlong(mbl__wwts.minute)
    oick__faxwk = c.pyapi.long_from_longlong(mbl__wwts.second)
    oga__bfr = c.pyapi.long_from_longlong(mbl__wwts.microsecond)
    wydz__qrp = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime)
        )
    bhkj__qem = c.pyapi.call_function_objargs(wydz__qrp, (qnuo__uem,
        zcv__idmzo, uwiy__tpzia, byeg__lia, xlj__mxw, oick__faxwk, oga__bfr))
    c.pyapi.decref(qnuo__uem)
    c.pyapi.decref(zcv__idmzo)
    c.pyapi.decref(uwiy__tpzia)
    c.pyapi.decref(byeg__lia)
    c.pyapi.decref(xlj__mxw)
    c.pyapi.decref(oick__faxwk)
    c.pyapi.decref(oga__bfr)
    c.pyapi.decref(wydz__qrp)
    return bhkj__qem


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    qnuo__uem = c.pyapi.object_getattr_string(val, 'year')
    zcv__idmzo = c.pyapi.object_getattr_string(val, 'month')
    uwiy__tpzia = c.pyapi.object_getattr_string(val, 'day')
    byeg__lia = c.pyapi.object_getattr_string(val, 'hour')
    xlj__mxw = c.pyapi.object_getattr_string(val, 'minute')
    oick__faxwk = c.pyapi.object_getattr_string(val, 'second')
    oga__bfr = c.pyapi.object_getattr_string(val, 'microsecond')
    mbl__wwts = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mbl__wwts.year = c.pyapi.long_as_longlong(qnuo__uem)
    mbl__wwts.month = c.pyapi.long_as_longlong(zcv__idmzo)
    mbl__wwts.day = c.pyapi.long_as_longlong(uwiy__tpzia)
    mbl__wwts.hour = c.pyapi.long_as_longlong(byeg__lia)
    mbl__wwts.minute = c.pyapi.long_as_longlong(xlj__mxw)
    mbl__wwts.second = c.pyapi.long_as_longlong(oick__faxwk)
    mbl__wwts.microsecond = c.pyapi.long_as_longlong(oga__bfr)
    c.pyapi.decref(qnuo__uem)
    c.pyapi.decref(zcv__idmzo)
    c.pyapi.decref(uwiy__tpzia)
    c.pyapi.decref(byeg__lia)
    c.pyapi.decref(xlj__mxw)
    c.pyapi.decref(oick__faxwk)
    c.pyapi.decref(oga__bfr)
    zfing__sowd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mbl__wwts._getvalue(), is_error=zfing__sowd)


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
        mbl__wwts = cgutils.create_struct_proxy(typ)(context, builder)
        mbl__wwts.year = args[0]
        mbl__wwts.month = args[1]
        mbl__wwts.day = args[2]
        mbl__wwts.hour = args[3]
        mbl__wwts.minute = args[4]
        mbl__wwts.second = args[5]
        mbl__wwts.microsecond = args[6]
        return mbl__wwts._getvalue()
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
                y, roiq__ouug = lhs.year, rhs.year
                ejknb__coi, omol__napm = lhs.month, rhs.month
                d, hqt__cndqk = lhs.day, rhs.day
                fhd__aey, hlfc__jnk = lhs.hour, rhs.hour
                alby__invzo, gkp__fzr = lhs.minute, rhs.minute
                zpu__mgnir, ukuk__cdaed = lhs.second, rhs.second
                jaci__isno, llyrb__oavi = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, ejknb__coi, d, fhd__aey, alby__invzo,
                    zpu__mgnir, jaci__isno), (roiq__ouug, omol__napm,
                    hqt__cndqk, hlfc__jnk, gkp__fzr, ukuk__cdaed,
                    llyrb__oavi)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            nwae__lynag = lhs.toordinal()
            gvgum__aysyj = rhs.toordinal()
            gpq__ljze = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            sls__bmb = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            fgi__urmpl = datetime.timedelta(nwae__lynag - gvgum__aysyj, 
                gpq__ljze - sls__bmb, lhs.microsecond - rhs.microsecond)
            return fgi__urmpl
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    pzlxb__yjr = context.make_helper(builder, fromty, value=val)
    iuytz__adq = cgutils.as_bool_bit(builder, pzlxb__yjr.valid)
    with builder.if_else(iuytz__adq) as (nhpkz__udpo, tdr__cpo):
        with nhpkz__udpo:
            cvcb__fybwv = context.cast(builder, pzlxb__yjr.data, fromty.
                type, toty)
            qxvni__fspc = builder.block
        with tdr__cpo:
            wil__zgck = numba.np.npdatetime.NAT
            vlmxt__cms = builder.block
    bhkj__qem = builder.phi(cvcb__fybwv.type)
    bhkj__qem.add_incoming(cvcb__fybwv, qxvni__fspc)
    bhkj__qem.add_incoming(wil__zgck, vlmxt__cms)
    return bhkj__qem
