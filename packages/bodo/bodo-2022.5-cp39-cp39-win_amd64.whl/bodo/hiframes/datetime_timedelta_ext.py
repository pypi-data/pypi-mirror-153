"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zchco__tfyb = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, zchco__tfyb)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    lgmw__jyirg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    euq__lqrfa = c.pyapi.long_from_longlong(lgmw__jyirg.value)
    aapdr__papft = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(aapdr__papft, (euq__lqrfa,))
    c.pyapi.decref(euq__lqrfa)
    c.pyapi.decref(aapdr__papft)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    euq__lqrfa = c.pyapi.object_getattr_string(val, 'value')
    mqi__bats = c.pyapi.long_as_longlong(euq__lqrfa)
    lgmw__jyirg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lgmw__jyirg.value = mqi__bats
    c.pyapi.decref(euq__lqrfa)
    awf__ivp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lgmw__jyirg._getvalue(), is_error=awf__ivp)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            plca__sdog = 1000 * microseconds
            return init_pd_timedelta(plca__sdog)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            plca__sdog = 1000 * microseconds
            return init_pd_timedelta(plca__sdog)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    eifa__gxz, qike__hsldf = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * eifa__gxz)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ffqzn__kfbw = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + ffqzn__kfbw
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            vbv__ermy = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = vbv__ermy + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            ydv__zlas = rhs.toordinal()
            yjb__gnema = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            yqfgv__rlxdy = rhs.microsecond
            shwbw__lnn = lhs.value // 1000
            hvkef__uyxdb = lhs.nanoseconds
            zxic__sbcuq = yqfgv__rlxdy + shwbw__lnn
            zun__bcdbr = 1000000 * (ydv__zlas * 86400 + yjb__gnema
                ) + zxic__sbcuq
            wca__mxnbw = hvkef__uyxdb
            return compute_pd_timestamp(zun__bcdbr, wca__mxnbw)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            wedj__yba = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            wedj__yba = wedj__yba + lhs
            wjcao__bhaq, vcdtp__zfxh = divmod(wedj__yba.seconds, 3600)
            gwoaf__xua, sue__pqdwj = divmod(vcdtp__zfxh, 60)
            if 0 < wedj__yba.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(wedj__yba
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    wjcao__bhaq, gwoaf__xua, sue__pqdwj, wedj__yba.microseconds
                    )
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            wedj__yba = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            wedj__yba = wedj__yba + rhs
            wjcao__bhaq, vcdtp__zfxh = divmod(wedj__yba.seconds, 3600)
            gwoaf__xua, sue__pqdwj = divmod(vcdtp__zfxh, 60)
            if 0 < wedj__yba.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(wedj__yba
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    wjcao__bhaq, gwoaf__xua, sue__pqdwj, wedj__yba.microseconds
                    )
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            yvn__slear = lhs.value - rhs.value
            return pd.Timedelta(yvn__slear)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            umoem__ilb = lhs
            numba.parfors.parfor.init_prange()
            n = len(umoem__ilb)
            A = alloc_datetime_timedelta_array(n)
            for pxsb__ayqa in numba.parfors.parfor.internal_prange(n):
                A[pxsb__ayqa] = umoem__ilb[pxsb__ayqa] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            nbdw__goyob = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, nbdw__goyob)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            dwus__oar, nbdw__goyob = divmod(lhs.value, rhs.value)
            return dwus__oar, pd.Timedelta(nbdw__goyob)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zchco__tfyb = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, zchco__tfyb)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    lgmw__jyirg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    uviom__dksh = c.pyapi.long_from_longlong(lgmw__jyirg.days)
    henq__vaqky = c.pyapi.long_from_longlong(lgmw__jyirg.seconds)
    fvpdx__yrzoq = c.pyapi.long_from_longlong(lgmw__jyirg.microseconds)
    aapdr__papft = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(aapdr__papft, (uviom__dksh,
        henq__vaqky, fvpdx__yrzoq))
    c.pyapi.decref(uviom__dksh)
    c.pyapi.decref(henq__vaqky)
    c.pyapi.decref(fvpdx__yrzoq)
    c.pyapi.decref(aapdr__papft)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    uviom__dksh = c.pyapi.object_getattr_string(val, 'days')
    henq__vaqky = c.pyapi.object_getattr_string(val, 'seconds')
    fvpdx__yrzoq = c.pyapi.object_getattr_string(val, 'microseconds')
    pslc__wmyb = c.pyapi.long_as_longlong(uviom__dksh)
    lmy__wyry = c.pyapi.long_as_longlong(henq__vaqky)
    cvlk__tgjaz = c.pyapi.long_as_longlong(fvpdx__yrzoq)
    lgmw__jyirg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lgmw__jyirg.days = pslc__wmyb
    lgmw__jyirg.seconds = lmy__wyry
    lgmw__jyirg.microseconds = cvlk__tgjaz
    c.pyapi.decref(uviom__dksh)
    c.pyapi.decref(henq__vaqky)
    c.pyapi.decref(fvpdx__yrzoq)
    awf__ivp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lgmw__jyirg._getvalue(), is_error=awf__ivp)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    dwus__oar, nbdw__goyob = divmod(a, b)
    nbdw__goyob *= 2
    fgtz__mcur = nbdw__goyob > b if b > 0 else nbdw__goyob < b
    if fgtz__mcur or nbdw__goyob == b and dwus__oar % 2 == 1:
        dwus__oar += 1
    return dwus__oar


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                ipmc__sgwv = _cmp(_getstate(lhs), _getstate(rhs))
                return op(ipmc__sgwv, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            dwus__oar, nbdw__goyob = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return dwus__oar, datetime.timedelta(0, 0, nbdw__goyob)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    axuf__nlha = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != axuf__nlha
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zchco__tfyb = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, zchco__tfyb)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    qcrhy__snyen = types.Array(types.intp, 1, 'C')
    ogkw__jaser = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        qcrhy__snyen, [n])
    upu__xiyks = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        qcrhy__snyen, [n])
    tulqg__zwie = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        qcrhy__snyen, [n])
    yes__soxa = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    tyljq__csm = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [yes__soxa])
    gktfz__slsaq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    pfsr__gojw = cgutils.get_or_insert_function(c.builder.module,
        gktfz__slsaq, name='unbox_datetime_timedelta_array')
    c.builder.call(pfsr__gojw, [val, n, ogkw__jaser.data, upu__xiyks.data,
        tulqg__zwie.data, tyljq__csm.data])
    hsx__avp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hsx__avp.days_data = ogkw__jaser._getvalue()
    hsx__avp.seconds_data = upu__xiyks._getvalue()
    hsx__avp.microseconds_data = tulqg__zwie._getvalue()
    hsx__avp.null_bitmap = tyljq__csm._getvalue()
    awf__ivp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hsx__avp._getvalue(), is_error=awf__ivp)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    umoem__ilb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ogkw__jaser = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, umoem__ilb.days_data)
    upu__xiyks = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, umoem__ilb.seconds_data).data
    tulqg__zwie = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, umoem__ilb.microseconds_data).data
    dindb__iyqn = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, umoem__ilb.null_bitmap).data
    n = c.builder.extract_value(ogkw__jaser.shape, 0)
    gktfz__slsaq = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    rsrw__dfgeg = cgutils.get_or_insert_function(c.builder.module,
        gktfz__slsaq, name='box_datetime_timedelta_array')
    ikeqq__fwp = c.builder.call(rsrw__dfgeg, [n, ogkw__jaser.data,
        upu__xiyks, tulqg__zwie, dindb__iyqn])
    c.context.nrt.decref(c.builder, typ, val)
    return ikeqq__fwp


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        vigmr__dvz, siiuh__psua, jqwc__boj, gjksy__iql = args
        wduq__ndv = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        wduq__ndv.days_data = vigmr__dvz
        wduq__ndv.seconds_data = siiuh__psua
        wduq__ndv.microseconds_data = jqwc__boj
        wduq__ndv.null_bitmap = gjksy__iql
        context.nrt.incref(builder, signature.args[0], vigmr__dvz)
        context.nrt.incref(builder, signature.args[1], siiuh__psua)
        context.nrt.incref(builder, signature.args[2], jqwc__boj)
        context.nrt.incref(builder, signature.args[3], gjksy__iql)
        return wduq__ndv._getvalue()
    shxtb__ykir = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return shxtb__ykir, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    ogkw__jaser = np.empty(n, np.int64)
    upu__xiyks = np.empty(n, np.int64)
    tulqg__zwie = np.empty(n, np.int64)
    msk__rnq = np.empty(n + 7 >> 3, np.uint8)
    for pxsb__ayqa, s in enumerate(pyval):
        ztodf__cgsu = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(msk__rnq, pxsb__ayqa, int(not
            ztodf__cgsu))
        if not ztodf__cgsu:
            ogkw__jaser[pxsb__ayqa] = s.days
            upu__xiyks[pxsb__ayqa] = s.seconds
            tulqg__zwie[pxsb__ayqa] = s.microseconds
    akxbp__fapr = context.get_constant_generic(builder, days_data_type,
        ogkw__jaser)
    rkmpn__tovm = context.get_constant_generic(builder, seconds_data_type,
        upu__xiyks)
    fzihh__apf = context.get_constant_generic(builder,
        microseconds_data_type, tulqg__zwie)
    tmt__hsfs = context.get_constant_generic(builder, nulls_type, msk__rnq)
    return lir.Constant.literal_struct([akxbp__fapr, rkmpn__tovm,
        fzihh__apf, tmt__hsfs])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    ogkw__jaser = np.empty(n, dtype=np.int64)
    upu__xiyks = np.empty(n, dtype=np.int64)
    tulqg__zwie = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(ogkw__jaser, upu__xiyks,
        tulqg__zwie, nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            eduru__pnt = bodo.utils.conversion.coerce_to_ndarray(ind)
            iyg__rxmim = A._null_bitmap
            bhixt__spj = A._days_data[eduru__pnt]
            uwos__vgk = A._seconds_data[eduru__pnt]
            ojgbq__gbxl = A._microseconds_data[eduru__pnt]
            n = len(bhixt__spj)
            skx__cij = get_new_null_mask_bool_index(iyg__rxmim, ind, n)
            return init_datetime_timedelta_array(bhixt__spj, uwos__vgk,
                ojgbq__gbxl, skx__cij)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            eduru__pnt = bodo.utils.conversion.coerce_to_ndarray(ind)
            iyg__rxmim = A._null_bitmap
            bhixt__spj = A._days_data[eduru__pnt]
            uwos__vgk = A._seconds_data[eduru__pnt]
            ojgbq__gbxl = A._microseconds_data[eduru__pnt]
            n = len(bhixt__spj)
            skx__cij = get_new_null_mask_int_index(iyg__rxmim, eduru__pnt, n)
            return init_datetime_timedelta_array(bhixt__spj, uwos__vgk,
                ojgbq__gbxl, skx__cij)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            iyg__rxmim = A._null_bitmap
            bhixt__spj = np.ascontiguousarray(A._days_data[ind])
            uwos__vgk = np.ascontiguousarray(A._seconds_data[ind])
            ojgbq__gbxl = np.ascontiguousarray(A._microseconds_data[ind])
            skx__cij = get_new_null_mask_slice_index(iyg__rxmim, ind, n)
            return init_datetime_timedelta_array(bhixt__spj, uwos__vgk,
                ojgbq__gbxl, skx__cij)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    aqy__lscrz = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(aqy__lscrz)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(aqy__lscrz)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for pxsb__ayqa in range(n):
                    A._days_data[ind[pxsb__ayqa]] = val._days
                    A._seconds_data[ind[pxsb__ayqa]] = val._seconds
                    A._microseconds_data[ind[pxsb__ayqa]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[pxsb__ayqa], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for pxsb__ayqa in range(n):
                    A._days_data[ind[pxsb__ayqa]] = val._days_data[pxsb__ayqa]
                    A._seconds_data[ind[pxsb__ayqa]] = val._seconds_data[
                        pxsb__ayqa]
                    A._microseconds_data[ind[pxsb__ayqa]
                        ] = val._microseconds_data[pxsb__ayqa]
                    rei__sgrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, pxsb__ayqa)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[pxsb__ayqa], rei__sgrx)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for pxsb__ayqa in range(n):
                    if not bodo.libs.array_kernels.isna(ind, pxsb__ayqa
                        ) and ind[pxsb__ayqa]:
                        A._days_data[pxsb__ayqa] = val._days
                        A._seconds_data[pxsb__ayqa] = val._seconds
                        A._microseconds_data[pxsb__ayqa] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            pxsb__ayqa, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                fxm__prhw = 0
                for pxsb__ayqa in range(n):
                    if not bodo.libs.array_kernels.isna(ind, pxsb__ayqa
                        ) and ind[pxsb__ayqa]:
                        A._days_data[pxsb__ayqa] = val._days_data[fxm__prhw]
                        A._seconds_data[pxsb__ayqa] = val._seconds_data[
                            fxm__prhw]
                        A._microseconds_data[pxsb__ayqa
                            ] = val._microseconds_data[fxm__prhw]
                        rei__sgrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, fxm__prhw)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            pxsb__ayqa, rei__sgrx)
                        fxm__prhw += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                dtmv__hvhye = numba.cpython.unicode._normalize_slice(ind,
                    len(A))
                for pxsb__ayqa in range(dtmv__hvhye.start, dtmv__hvhye.stop,
                    dtmv__hvhye.step):
                    A._days_data[pxsb__ayqa] = val._days
                    A._seconds_data[pxsb__ayqa] = val._seconds
                    A._microseconds_data[pxsb__ayqa] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        pxsb__ayqa, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                osnz__xltob = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, osnz__xltob,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            umoem__ilb = arg1
            numba.parfors.parfor.init_prange()
            n = len(umoem__ilb)
            A = alloc_datetime_timedelta_array(n)
            for pxsb__ayqa in numba.parfors.parfor.internal_prange(n):
                A[pxsb__ayqa] = umoem__ilb[pxsb__ayqa] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            ekl__itc = True
        else:
            ekl__itc = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                gnano__pue = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for pxsb__ayqa in numba.parfors.parfor.internal_prange(n):
                    nxba__pohk = bodo.libs.array_kernels.isna(lhs, pxsb__ayqa)
                    wnom__lznqz = bodo.libs.array_kernels.isna(rhs, pxsb__ayqa)
                    if nxba__pohk or wnom__lznqz:
                        cwbtr__dznd = ekl__itc
                    else:
                        cwbtr__dznd = op(lhs[pxsb__ayqa], rhs[pxsb__ayqa])
                    gnano__pue[pxsb__ayqa] = cwbtr__dznd
                return gnano__pue
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                gnano__pue = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for pxsb__ayqa in numba.parfors.parfor.internal_prange(n):
                    rei__sgrx = bodo.libs.array_kernels.isna(lhs, pxsb__ayqa)
                    if rei__sgrx:
                        cwbtr__dznd = ekl__itc
                    else:
                        cwbtr__dznd = op(lhs[pxsb__ayqa], rhs)
                    gnano__pue[pxsb__ayqa] = cwbtr__dznd
                return gnano__pue
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                gnano__pue = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for pxsb__ayqa in numba.parfors.parfor.internal_prange(n):
                    rei__sgrx = bodo.libs.array_kernels.isna(rhs, pxsb__ayqa)
                    if rei__sgrx:
                        cwbtr__dznd = ekl__itc
                    else:
                        cwbtr__dznd = op(lhs, rhs[pxsb__ayqa])
                    gnano__pue[pxsb__ayqa] = cwbtr__dznd
                return gnano__pue
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for blrnp__rjjtt in timedelta_unsupported_attrs:
        hbqgd__ctah = 'pandas.Timedelta.' + blrnp__rjjtt
        overload_attribute(PDTimeDeltaType, blrnp__rjjtt)(
            create_unsupported_overload(hbqgd__ctah))
    for thoq__vppe in timedelta_unsupported_methods:
        hbqgd__ctah = 'pandas.Timedelta.' + thoq__vppe
        overload_method(PDTimeDeltaType, thoq__vppe)(
            create_unsupported_overload(hbqgd__ctah + '()'))


_intstall_pd_timedelta_unsupported()
