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
        wetg__kwne = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, wetg__kwne)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    qlu__jtmfw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jpa__qob = c.pyapi.long_from_longlong(qlu__jtmfw.value)
    gcrzj__aldya = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(gcrzj__aldya, (jpa__qob,))
    c.pyapi.decref(jpa__qob)
    c.pyapi.decref(gcrzj__aldya)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    jpa__qob = c.pyapi.object_getattr_string(val, 'value')
    yzx__euzgr = c.pyapi.long_as_longlong(jpa__qob)
    qlu__jtmfw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qlu__jtmfw.value = yzx__euzgr
    c.pyapi.decref(jpa__qob)
    ybqxz__wro = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qlu__jtmfw._getvalue(), is_error=ybqxz__wro)


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
            jqqyh__dceio = 1000 * microseconds
            return init_pd_timedelta(jqqyh__dceio)
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
            jqqyh__dceio = 1000 * microseconds
            return init_pd_timedelta(jqqyh__dceio)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    xvhl__iwvtu, erk__myhp = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * xvhl__iwvtu)
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
            haie__gzwx = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + haie__gzwx
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ryltq__jfv = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = ryltq__jfv + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            nnd__zxvkc = rhs.toordinal()
            fsprt__ervf = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            nnld__xfev = rhs.microsecond
            yyv__pdk = lhs.value // 1000
            jyicl__aiuov = lhs.nanoseconds
            ohrgi__naiab = nnld__xfev + yyv__pdk
            qrvcy__njrby = 1000000 * (nnd__zxvkc * 86400 + fsprt__ervf
                ) + ohrgi__naiab
            bylkr__pnqzr = jyicl__aiuov
            return compute_pd_timestamp(qrvcy__njrby, bylkr__pnqzr)
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
            wlv__tewxf = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            wlv__tewxf = wlv__tewxf + lhs
            bar__cnlm, nub__lfhm = divmod(wlv__tewxf.seconds, 3600)
            vxo__dkgeh, cvjxq__fsm = divmod(nub__lfhm, 60)
            if 0 < wlv__tewxf.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(wlv__tewxf
                    .days)
                return datetime.datetime(d.year, d.month, d.day, bar__cnlm,
                    vxo__dkgeh, cvjxq__fsm, wlv__tewxf.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            wlv__tewxf = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            wlv__tewxf = wlv__tewxf + rhs
            bar__cnlm, nub__lfhm = divmod(wlv__tewxf.seconds, 3600)
            vxo__dkgeh, cvjxq__fsm = divmod(nub__lfhm, 60)
            if 0 < wlv__tewxf.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(wlv__tewxf
                    .days)
                return datetime.datetime(d.year, d.month, d.day, bar__cnlm,
                    vxo__dkgeh, cvjxq__fsm, wlv__tewxf.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            wrw__ztg = lhs.value - rhs.value
            return pd.Timedelta(wrw__ztg)
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
            jazlw__htnyf = lhs
            numba.parfors.parfor.init_prange()
            n = len(jazlw__htnyf)
            A = alloc_datetime_timedelta_array(n)
            for thw__zrwd in numba.parfors.parfor.internal_prange(n):
                A[thw__zrwd] = jazlw__htnyf[thw__zrwd] - rhs
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
            tpis__yvvy = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, tpis__yvvy)
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
            vtduc__vyuy, tpis__yvvy = divmod(lhs.value, rhs.value)
            return vtduc__vyuy, pd.Timedelta(tpis__yvvy)
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
        wetg__kwne = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, wetg__kwne)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    qlu__jtmfw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ymxx__aau = c.pyapi.long_from_longlong(qlu__jtmfw.days)
    ezwdb__jlx = c.pyapi.long_from_longlong(qlu__jtmfw.seconds)
    vklm__gvcan = c.pyapi.long_from_longlong(qlu__jtmfw.microseconds)
    gcrzj__aldya = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(gcrzj__aldya, (ymxx__aau,
        ezwdb__jlx, vklm__gvcan))
    c.pyapi.decref(ymxx__aau)
    c.pyapi.decref(ezwdb__jlx)
    c.pyapi.decref(vklm__gvcan)
    c.pyapi.decref(gcrzj__aldya)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    ymxx__aau = c.pyapi.object_getattr_string(val, 'days')
    ezwdb__jlx = c.pyapi.object_getattr_string(val, 'seconds')
    vklm__gvcan = c.pyapi.object_getattr_string(val, 'microseconds')
    rwrxt__ezcl = c.pyapi.long_as_longlong(ymxx__aau)
    qjnhd__edz = c.pyapi.long_as_longlong(ezwdb__jlx)
    tpwm__nfj = c.pyapi.long_as_longlong(vklm__gvcan)
    qlu__jtmfw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qlu__jtmfw.days = rwrxt__ezcl
    qlu__jtmfw.seconds = qjnhd__edz
    qlu__jtmfw.microseconds = tpwm__nfj
    c.pyapi.decref(ymxx__aau)
    c.pyapi.decref(ezwdb__jlx)
    c.pyapi.decref(vklm__gvcan)
    ybqxz__wro = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qlu__jtmfw._getvalue(), is_error=ybqxz__wro)


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
    vtduc__vyuy, tpis__yvvy = divmod(a, b)
    tpis__yvvy *= 2
    qnbyq__utozv = tpis__yvvy > b if b > 0 else tpis__yvvy < b
    if qnbyq__utozv or tpis__yvvy == b and vtduc__vyuy % 2 == 1:
        vtduc__vyuy += 1
    return vtduc__vyuy


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
                yipzj__waunx = _cmp(_getstate(lhs), _getstate(rhs))
                return op(yipzj__waunx, 0)
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
            vtduc__vyuy, tpis__yvvy = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return vtduc__vyuy, datetime.timedelta(0, 0, tpis__yvvy)
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
    jiyx__pffs = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != jiyx__pffs
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
        wetg__kwne = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, wetg__kwne)


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
    tnp__gla = types.Array(types.intp, 1, 'C')
    slfw__sqo = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        tnp__gla, [n])
    bsypz__kwbb = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        tnp__gla, [n])
    gkpt__smv = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        tnp__gla, [n])
    igkj__ntyz = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    qruhl__wbkm = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [igkj__ntyz])
    iqhi__rmy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    uts__cbs = cgutils.get_or_insert_function(c.builder.module, iqhi__rmy,
        name='unbox_datetime_timedelta_array')
    c.builder.call(uts__cbs, [val, n, slfw__sqo.data, bsypz__kwbb.data,
        gkpt__smv.data, qruhl__wbkm.data])
    kecgq__ecd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    kecgq__ecd.days_data = slfw__sqo._getvalue()
    kecgq__ecd.seconds_data = bsypz__kwbb._getvalue()
    kecgq__ecd.microseconds_data = gkpt__smv._getvalue()
    kecgq__ecd.null_bitmap = qruhl__wbkm._getvalue()
    ybqxz__wro = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kecgq__ecd._getvalue(), is_error=ybqxz__wro)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    jazlw__htnyf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    slfw__sqo = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, jazlw__htnyf.days_data)
    bsypz__kwbb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, jazlw__htnyf.seconds_data).data
    gkpt__smv = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, jazlw__htnyf.microseconds_data).data
    ica__ugee = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, jazlw__htnyf.null_bitmap).data
    n = c.builder.extract_value(slfw__sqo.shape, 0)
    iqhi__rmy = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    qro__ijsd = cgutils.get_or_insert_function(c.builder.module, iqhi__rmy,
        name='box_datetime_timedelta_array')
    eqgny__kdxzu = c.builder.call(qro__ijsd, [n, slfw__sqo.data,
        bsypz__kwbb, gkpt__smv, ica__ugee])
    c.context.nrt.decref(c.builder, typ, val)
    return eqgny__kdxzu


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        slfuw__rwjhv, bjtd__lpgzu, fson__wovu, gadsa__zok = args
        kii__idz = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        kii__idz.days_data = slfuw__rwjhv
        kii__idz.seconds_data = bjtd__lpgzu
        kii__idz.microseconds_data = fson__wovu
        kii__idz.null_bitmap = gadsa__zok
        context.nrt.incref(builder, signature.args[0], slfuw__rwjhv)
        context.nrt.incref(builder, signature.args[1], bjtd__lpgzu)
        context.nrt.incref(builder, signature.args[2], fson__wovu)
        context.nrt.incref(builder, signature.args[3], gadsa__zok)
        return kii__idz._getvalue()
    bal__vnay = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return bal__vnay, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    slfw__sqo = np.empty(n, np.int64)
    bsypz__kwbb = np.empty(n, np.int64)
    gkpt__smv = np.empty(n, np.int64)
    nvz__rftv = np.empty(n + 7 >> 3, np.uint8)
    for thw__zrwd, s in enumerate(pyval):
        nbv__ndm = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(nvz__rftv, thw__zrwd, int(not
            nbv__ndm))
        if not nbv__ndm:
            slfw__sqo[thw__zrwd] = s.days
            bsypz__kwbb[thw__zrwd] = s.seconds
            gkpt__smv[thw__zrwd] = s.microseconds
    hsy__ykab = context.get_constant_generic(builder, days_data_type, slfw__sqo
        )
    xedb__jtft = context.get_constant_generic(builder, seconds_data_type,
        bsypz__kwbb)
    gxj__hpni = context.get_constant_generic(builder,
        microseconds_data_type, gkpt__smv)
    sargc__pvact = context.get_constant_generic(builder, nulls_type, nvz__rftv)
    return lir.Constant.literal_struct([hsy__ykab, xedb__jtft, gxj__hpni,
        sargc__pvact])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    slfw__sqo = np.empty(n, dtype=np.int64)
    bsypz__kwbb = np.empty(n, dtype=np.int64)
    gkpt__smv = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(slfw__sqo, bsypz__kwbb, gkpt__smv,
        nulls)


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
            tehxk__uwojv = bodo.utils.conversion.coerce_to_ndarray(ind)
            mebg__lunh = A._null_bitmap
            leu__crbjd = A._days_data[tehxk__uwojv]
            neamm__sxh = A._seconds_data[tehxk__uwojv]
            seae__lmyyo = A._microseconds_data[tehxk__uwojv]
            n = len(leu__crbjd)
            bdzuk__tbskx = get_new_null_mask_bool_index(mebg__lunh, ind, n)
            return init_datetime_timedelta_array(leu__crbjd, neamm__sxh,
                seae__lmyyo, bdzuk__tbskx)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            tehxk__uwojv = bodo.utils.conversion.coerce_to_ndarray(ind)
            mebg__lunh = A._null_bitmap
            leu__crbjd = A._days_data[tehxk__uwojv]
            neamm__sxh = A._seconds_data[tehxk__uwojv]
            seae__lmyyo = A._microseconds_data[tehxk__uwojv]
            n = len(leu__crbjd)
            bdzuk__tbskx = get_new_null_mask_int_index(mebg__lunh,
                tehxk__uwojv, n)
            return init_datetime_timedelta_array(leu__crbjd, neamm__sxh,
                seae__lmyyo, bdzuk__tbskx)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            mebg__lunh = A._null_bitmap
            leu__crbjd = np.ascontiguousarray(A._days_data[ind])
            neamm__sxh = np.ascontiguousarray(A._seconds_data[ind])
            seae__lmyyo = np.ascontiguousarray(A._microseconds_data[ind])
            bdzuk__tbskx = get_new_null_mask_slice_index(mebg__lunh, ind, n)
            return init_datetime_timedelta_array(leu__crbjd, neamm__sxh,
                seae__lmyyo, bdzuk__tbskx)
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
    mag__zfkxj = (
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
            raise BodoError(mag__zfkxj)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(mag__zfkxj)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for thw__zrwd in range(n):
                    A._days_data[ind[thw__zrwd]] = val._days
                    A._seconds_data[ind[thw__zrwd]] = val._seconds
                    A._microseconds_data[ind[thw__zrwd]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[thw__zrwd], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for thw__zrwd in range(n):
                    A._days_data[ind[thw__zrwd]] = val._days_data[thw__zrwd]
                    A._seconds_data[ind[thw__zrwd]] = val._seconds_data[
                        thw__zrwd]
                    A._microseconds_data[ind[thw__zrwd]
                        ] = val._microseconds_data[thw__zrwd]
                    svq__gkewc = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, thw__zrwd)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[thw__zrwd], svq__gkewc)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for thw__zrwd in range(n):
                    if not bodo.libs.array_kernels.isna(ind, thw__zrwd
                        ) and ind[thw__zrwd]:
                        A._days_data[thw__zrwd] = val._days
                        A._seconds_data[thw__zrwd] = val._seconds
                        A._microseconds_data[thw__zrwd] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            thw__zrwd, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                mnmnx__irxu = 0
                for thw__zrwd in range(n):
                    if not bodo.libs.array_kernels.isna(ind, thw__zrwd
                        ) and ind[thw__zrwd]:
                        A._days_data[thw__zrwd] = val._days_data[mnmnx__irxu]
                        A._seconds_data[thw__zrwd] = val._seconds_data[
                            mnmnx__irxu]
                        A._microseconds_data[thw__zrwd
                            ] = val._microseconds_data[mnmnx__irxu]
                        svq__gkewc = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, mnmnx__irxu)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            thw__zrwd, svq__gkewc)
                        mnmnx__irxu += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                vqt__xszec = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for thw__zrwd in range(vqt__xszec.start, vqt__xszec.stop,
                    vqt__xszec.step):
                    A._days_data[thw__zrwd] = val._days
                    A._seconds_data[thw__zrwd] = val._seconds
                    A._microseconds_data[thw__zrwd] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        thw__zrwd, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                jtzz__ynsap = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, jtzz__ynsap,
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
            jazlw__htnyf = arg1
            numba.parfors.parfor.init_prange()
            n = len(jazlw__htnyf)
            A = alloc_datetime_timedelta_array(n)
            for thw__zrwd in numba.parfors.parfor.internal_prange(n):
                A[thw__zrwd] = jazlw__htnyf[thw__zrwd] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            sabqx__fwjzc = True
        else:
            sabqx__fwjzc = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                nex__cej = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for thw__zrwd in numba.parfors.parfor.internal_prange(n):
                    dkn__nhso = bodo.libs.array_kernels.isna(lhs, thw__zrwd)
                    mfwzn__wpzv = bodo.libs.array_kernels.isna(rhs, thw__zrwd)
                    if dkn__nhso or mfwzn__wpzv:
                        lmop__qnzr = sabqx__fwjzc
                    else:
                        lmop__qnzr = op(lhs[thw__zrwd], rhs[thw__zrwd])
                    nex__cej[thw__zrwd] = lmop__qnzr
                return nex__cej
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                nex__cej = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for thw__zrwd in numba.parfors.parfor.internal_prange(n):
                    svq__gkewc = bodo.libs.array_kernels.isna(lhs, thw__zrwd)
                    if svq__gkewc:
                        lmop__qnzr = sabqx__fwjzc
                    else:
                        lmop__qnzr = op(lhs[thw__zrwd], rhs)
                    nex__cej[thw__zrwd] = lmop__qnzr
                return nex__cej
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                nex__cej = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for thw__zrwd in numba.parfors.parfor.internal_prange(n):
                    svq__gkewc = bodo.libs.array_kernels.isna(rhs, thw__zrwd)
                    if svq__gkewc:
                        lmop__qnzr = sabqx__fwjzc
                    else:
                        lmop__qnzr = op(lhs, rhs[thw__zrwd])
                    nex__cej[thw__zrwd] = lmop__qnzr
                return nex__cej
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for mmoy__zikc in timedelta_unsupported_attrs:
        xfm__axwfp = 'pandas.Timedelta.' + mmoy__zikc
        overload_attribute(PDTimeDeltaType, mmoy__zikc)(
            create_unsupported_overload(xfm__axwfp))
    for zzff__yls in timedelta_unsupported_methods:
        xfm__axwfp = 'pandas.Timedelta.' + zzff__yls
        overload_method(PDTimeDeltaType, zzff__yls)(create_unsupported_overload
            (xfm__axwfp + '()'))


_intstall_pd_timedelta_unsupported()
