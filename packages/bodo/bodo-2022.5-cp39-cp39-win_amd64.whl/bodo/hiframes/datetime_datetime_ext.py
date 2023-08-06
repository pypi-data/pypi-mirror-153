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
        uzdy__tbzcx = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, uzdy__tbzcx)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    gnd__jgoea = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    fwg__rvj = c.pyapi.long_from_longlong(gnd__jgoea.year)
    nflz__opuc = c.pyapi.long_from_longlong(gnd__jgoea.month)
    wir__snjes = c.pyapi.long_from_longlong(gnd__jgoea.day)
    doccs__gajl = c.pyapi.long_from_longlong(gnd__jgoea.hour)
    tqkf__qonx = c.pyapi.long_from_longlong(gnd__jgoea.minute)
    cwa__exnp = c.pyapi.long_from_longlong(gnd__jgoea.second)
    udx__ndb = c.pyapi.long_from_longlong(gnd__jgoea.microsecond)
    vqxf__yfskq = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    hgwil__wvoj = c.pyapi.call_function_objargs(vqxf__yfskq, (fwg__rvj,
        nflz__opuc, wir__snjes, doccs__gajl, tqkf__qonx, cwa__exnp, udx__ndb))
    c.pyapi.decref(fwg__rvj)
    c.pyapi.decref(nflz__opuc)
    c.pyapi.decref(wir__snjes)
    c.pyapi.decref(doccs__gajl)
    c.pyapi.decref(tqkf__qonx)
    c.pyapi.decref(cwa__exnp)
    c.pyapi.decref(udx__ndb)
    c.pyapi.decref(vqxf__yfskq)
    return hgwil__wvoj


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    fwg__rvj = c.pyapi.object_getattr_string(val, 'year')
    nflz__opuc = c.pyapi.object_getattr_string(val, 'month')
    wir__snjes = c.pyapi.object_getattr_string(val, 'day')
    doccs__gajl = c.pyapi.object_getattr_string(val, 'hour')
    tqkf__qonx = c.pyapi.object_getattr_string(val, 'minute')
    cwa__exnp = c.pyapi.object_getattr_string(val, 'second')
    udx__ndb = c.pyapi.object_getattr_string(val, 'microsecond')
    gnd__jgoea = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gnd__jgoea.year = c.pyapi.long_as_longlong(fwg__rvj)
    gnd__jgoea.month = c.pyapi.long_as_longlong(nflz__opuc)
    gnd__jgoea.day = c.pyapi.long_as_longlong(wir__snjes)
    gnd__jgoea.hour = c.pyapi.long_as_longlong(doccs__gajl)
    gnd__jgoea.minute = c.pyapi.long_as_longlong(tqkf__qonx)
    gnd__jgoea.second = c.pyapi.long_as_longlong(cwa__exnp)
    gnd__jgoea.microsecond = c.pyapi.long_as_longlong(udx__ndb)
    c.pyapi.decref(fwg__rvj)
    c.pyapi.decref(nflz__opuc)
    c.pyapi.decref(wir__snjes)
    c.pyapi.decref(doccs__gajl)
    c.pyapi.decref(tqkf__qonx)
    c.pyapi.decref(cwa__exnp)
    c.pyapi.decref(udx__ndb)
    qyw__esk = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gnd__jgoea._getvalue(), is_error=qyw__esk)


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
        gnd__jgoea = cgutils.create_struct_proxy(typ)(context, builder)
        gnd__jgoea.year = args[0]
        gnd__jgoea.month = args[1]
        gnd__jgoea.day = args[2]
        gnd__jgoea.hour = args[3]
        gnd__jgoea.minute = args[4]
        gnd__jgoea.second = args[5]
        gnd__jgoea.microsecond = args[6]
        return gnd__jgoea._getvalue()
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
                y, gjc__zcvqx = lhs.year, rhs.year
                rdpyr__ucb, oimzz__tvhhm = lhs.month, rhs.month
                d, abf__vwta = lhs.day, rhs.day
                oky__wxzy, und__nxsiv = lhs.hour, rhs.hour
                hbv__iaqdf, leqih__wvos = lhs.minute, rhs.minute
                hoemg__gbvrw, yog__eigv = lhs.second, rhs.second
                gjk__vzvf, zxqdi__guma = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, rdpyr__ucb, d, oky__wxzy, hbv__iaqdf,
                    hoemg__gbvrw, gjk__vzvf), (gjc__zcvqx, oimzz__tvhhm,
                    abf__vwta, und__nxsiv, leqih__wvos, yog__eigv,
                    zxqdi__guma)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            zanop__ubnl = lhs.toordinal()
            drx__jpxw = rhs.toordinal()
            fpw__gbfz = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            qqd__fxjzf = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            zzy__iwo = datetime.timedelta(zanop__ubnl - drx__jpxw, 
                fpw__gbfz - qqd__fxjzf, lhs.microsecond - rhs.microsecond)
            return zzy__iwo
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    hkqz__niqc = context.make_helper(builder, fromty, value=val)
    fwydp__vxwiw = cgutils.as_bool_bit(builder, hkqz__niqc.valid)
    with builder.if_else(fwydp__vxwiw) as (kzbl__hyww, revs__xvf):
        with kzbl__hyww:
            pjec__ohg = context.cast(builder, hkqz__niqc.data, fromty.type,
                toty)
            vupn__nhao = builder.block
        with revs__xvf:
            mxwf__ekzzz = numba.np.npdatetime.NAT
            xliq__zgzy = builder.block
    hgwil__wvoj = builder.phi(pjec__ohg.type)
    hgwil__wvoj.add_incoming(pjec__ohg, vupn__nhao)
    hgwil__wvoj.add_incoming(mxwf__ekzzz, xliq__zgzy)
    return hgwil__wvoj
