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
        hjf__bkr = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, hjf__bkr)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    enmby__lnmc = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ouq__xxflv = c.pyapi.long_from_longlong(enmby__lnmc.value)
    epc__akk = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(epc__akk, (ouq__xxflv,))
    c.pyapi.decref(ouq__xxflv)
    c.pyapi.decref(epc__akk)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    ouq__xxflv = c.pyapi.object_getattr_string(val, 'value')
    tnxu__oeip = c.pyapi.long_as_longlong(ouq__xxflv)
    enmby__lnmc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    enmby__lnmc.value = tnxu__oeip
    c.pyapi.decref(ouq__xxflv)
    jjn__sum = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(enmby__lnmc._getvalue(), is_error=jjn__sum)


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
            sqg__yxf = 1000 * microseconds
            return init_pd_timedelta(sqg__yxf)
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
            sqg__yxf = 1000 * microseconds
            return init_pd_timedelta(sqg__yxf)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    wyp__shgz, mrz__ebtz = pd._libs.tslibs.conversion.precision_from_unit(unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * wyp__shgz)
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
            vrj__ogl = (rhs.microseconds + (rhs.seconds + rhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + vrj__ogl
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            lbj__rts = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lbj__rts + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            mcisv__qusfn = rhs.toordinal()
            hakd__nzklo = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            popb__rcyvz = rhs.microsecond
            bncnj__ahcye = lhs.value // 1000
            egx__vtlf = lhs.nanoseconds
            ixfdr__xpvfc = popb__rcyvz + bncnj__ahcye
            lldja__ilt = 1000000 * (mcisv__qusfn * 86400 + hakd__nzklo
                ) + ixfdr__xpvfc
            gfqh__ipk = egx__vtlf
            return compute_pd_timestamp(lldja__ilt, gfqh__ipk)
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
            wpack__bwo = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            wpack__bwo = wpack__bwo + lhs
            lrkc__sdlra, him__fabuo = divmod(wpack__bwo.seconds, 3600)
            bqbek__dansr, molr__syht = divmod(him__fabuo, 60)
            if 0 < wpack__bwo.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(wpack__bwo
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    lrkc__sdlra, bqbek__dansr, molr__syht, wpack__bwo.
                    microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            wpack__bwo = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            wpack__bwo = wpack__bwo + rhs
            lrkc__sdlra, him__fabuo = divmod(wpack__bwo.seconds, 3600)
            bqbek__dansr, molr__syht = divmod(him__fabuo, 60)
            if 0 < wpack__bwo.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(wpack__bwo
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    lrkc__sdlra, bqbek__dansr, molr__syht, wpack__bwo.
                    microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            wjr__iprlf = lhs.value - rhs.value
            return pd.Timedelta(wjr__iprlf)
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
            sdunp__xbsv = lhs
            numba.parfors.parfor.init_prange()
            n = len(sdunp__xbsv)
            A = alloc_datetime_timedelta_array(n)
            for akf__zgj in numba.parfors.parfor.internal_prange(n):
                A[akf__zgj] = sdunp__xbsv[akf__zgj] - rhs
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
            jtiu__rxfzy = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, jtiu__rxfzy)
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
            nyimx__oqx, jtiu__rxfzy = divmod(lhs.value, rhs.value)
            return nyimx__oqx, pd.Timedelta(jtiu__rxfzy)
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
        hjf__bkr = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, hjf__bkr)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    enmby__lnmc = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    mexso__vvooz = c.pyapi.long_from_longlong(enmby__lnmc.days)
    hdq__pyk = c.pyapi.long_from_longlong(enmby__lnmc.seconds)
    skt__fbivj = c.pyapi.long_from_longlong(enmby__lnmc.microseconds)
    epc__akk = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.timedelta)
        )
    res = c.pyapi.call_function_objargs(epc__akk, (mexso__vvooz, hdq__pyk,
        skt__fbivj))
    c.pyapi.decref(mexso__vvooz)
    c.pyapi.decref(hdq__pyk)
    c.pyapi.decref(skt__fbivj)
    c.pyapi.decref(epc__akk)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    mexso__vvooz = c.pyapi.object_getattr_string(val, 'days')
    hdq__pyk = c.pyapi.object_getattr_string(val, 'seconds')
    skt__fbivj = c.pyapi.object_getattr_string(val, 'microseconds')
    wefr__yoeu = c.pyapi.long_as_longlong(mexso__vvooz)
    auda__pobna = c.pyapi.long_as_longlong(hdq__pyk)
    hmurh__mmntr = c.pyapi.long_as_longlong(skt__fbivj)
    enmby__lnmc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    enmby__lnmc.days = wefr__yoeu
    enmby__lnmc.seconds = auda__pobna
    enmby__lnmc.microseconds = hmurh__mmntr
    c.pyapi.decref(mexso__vvooz)
    c.pyapi.decref(hdq__pyk)
    c.pyapi.decref(skt__fbivj)
    jjn__sum = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(enmby__lnmc._getvalue(), is_error=jjn__sum)


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
    nyimx__oqx, jtiu__rxfzy = divmod(a, b)
    jtiu__rxfzy *= 2
    ajjz__rqzf = jtiu__rxfzy > b if b > 0 else jtiu__rxfzy < b
    if ajjz__rqzf or jtiu__rxfzy == b and nyimx__oqx % 2 == 1:
        nyimx__oqx += 1
    return nyimx__oqx


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
                zgno__zlsll = _cmp(_getstate(lhs), _getstate(rhs))
                return op(zgno__zlsll, 0)
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
            nyimx__oqx, jtiu__rxfzy = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return nyimx__oqx, datetime.timedelta(0, 0, jtiu__rxfzy)
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
    zmk__gon = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != zmk__gon
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
        hjf__bkr = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, hjf__bkr)


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
    pvav__fkjd = types.Array(types.intp, 1, 'C')
    jqmjj__anht = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        pvav__fkjd, [n])
    cus__auj = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        pvav__fkjd, [n])
    pxjlm__ffwb = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        pvav__fkjd, [n])
    jxhig__ladje = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    rxrta__ujhg = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [jxhig__ladje])
    licqz__hzag = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    blkrh__swt = cgutils.get_or_insert_function(c.builder.module,
        licqz__hzag, name='unbox_datetime_timedelta_array')
    c.builder.call(blkrh__swt, [val, n, jqmjj__anht.data, cus__auj.data,
        pxjlm__ffwb.data, rxrta__ujhg.data])
    hwp__yvop = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hwp__yvop.days_data = jqmjj__anht._getvalue()
    hwp__yvop.seconds_data = cus__auj._getvalue()
    hwp__yvop.microseconds_data = pxjlm__ffwb._getvalue()
    hwp__yvop.null_bitmap = rxrta__ujhg._getvalue()
    jjn__sum = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hwp__yvop._getvalue(), is_error=jjn__sum)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    sdunp__xbsv = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    jqmjj__anht = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, sdunp__xbsv.days_data)
    cus__auj = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, sdunp__xbsv.seconds_data).data
    pxjlm__ffwb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, sdunp__xbsv.microseconds_data).data
    lszih__viv = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, sdunp__xbsv.null_bitmap).data
    n = c.builder.extract_value(jqmjj__anht.shape, 0)
    licqz__hzag = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    pxdv__wdzb = cgutils.get_or_insert_function(c.builder.module,
        licqz__hzag, name='box_datetime_timedelta_array')
    hygr__emih = c.builder.call(pxdv__wdzb, [n, jqmjj__anht.data, cus__auj,
        pxjlm__ffwb, lszih__viv])
    c.context.nrt.decref(c.builder, typ, val)
    return hygr__emih


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        vlsni__wojcr, icz__hzoku, veh__dzie, bnl__ryg = args
        dbwft__jfco = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        dbwft__jfco.days_data = vlsni__wojcr
        dbwft__jfco.seconds_data = icz__hzoku
        dbwft__jfco.microseconds_data = veh__dzie
        dbwft__jfco.null_bitmap = bnl__ryg
        context.nrt.incref(builder, signature.args[0], vlsni__wojcr)
        context.nrt.incref(builder, signature.args[1], icz__hzoku)
        context.nrt.incref(builder, signature.args[2], veh__dzie)
        context.nrt.incref(builder, signature.args[3], bnl__ryg)
        return dbwft__jfco._getvalue()
    oqht__hszy = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return oqht__hszy, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    jqmjj__anht = np.empty(n, np.int64)
    cus__auj = np.empty(n, np.int64)
    pxjlm__ffwb = np.empty(n, np.int64)
    usmn__ikkmr = np.empty(n + 7 >> 3, np.uint8)
    for akf__zgj, s in enumerate(pyval):
        vrcq__ncyts = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(usmn__ikkmr, akf__zgj, int(not
            vrcq__ncyts))
        if not vrcq__ncyts:
            jqmjj__anht[akf__zgj] = s.days
            cus__auj[akf__zgj] = s.seconds
            pxjlm__ffwb[akf__zgj] = s.microseconds
    iob__qzqzh = context.get_constant_generic(builder, days_data_type,
        jqmjj__anht)
    cqjbd__fkoe = context.get_constant_generic(builder, seconds_data_type,
        cus__auj)
    xblrf__rlihe = context.get_constant_generic(builder,
        microseconds_data_type, pxjlm__ffwb)
    xhj__mkdv = context.get_constant_generic(builder, nulls_type, usmn__ikkmr)
    return lir.Constant.literal_struct([iob__qzqzh, cqjbd__fkoe,
        xblrf__rlihe, xhj__mkdv])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    jqmjj__anht = np.empty(n, dtype=np.int64)
    cus__auj = np.empty(n, dtype=np.int64)
    pxjlm__ffwb = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(jqmjj__anht, cus__auj, pxjlm__ffwb,
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
            qxen__dmy = bodo.utils.conversion.coerce_to_ndarray(ind)
            oohe__rkxcn = A._null_bitmap
            uyx__hujy = A._days_data[qxen__dmy]
            nxsq__ddnli = A._seconds_data[qxen__dmy]
            fjtkz__akenr = A._microseconds_data[qxen__dmy]
            n = len(uyx__hujy)
            gns__bxdl = get_new_null_mask_bool_index(oohe__rkxcn, ind, n)
            return init_datetime_timedelta_array(uyx__hujy, nxsq__ddnli,
                fjtkz__akenr, gns__bxdl)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            qxen__dmy = bodo.utils.conversion.coerce_to_ndarray(ind)
            oohe__rkxcn = A._null_bitmap
            uyx__hujy = A._days_data[qxen__dmy]
            nxsq__ddnli = A._seconds_data[qxen__dmy]
            fjtkz__akenr = A._microseconds_data[qxen__dmy]
            n = len(uyx__hujy)
            gns__bxdl = get_new_null_mask_int_index(oohe__rkxcn, qxen__dmy, n)
            return init_datetime_timedelta_array(uyx__hujy, nxsq__ddnli,
                fjtkz__akenr, gns__bxdl)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            oohe__rkxcn = A._null_bitmap
            uyx__hujy = np.ascontiguousarray(A._days_data[ind])
            nxsq__ddnli = np.ascontiguousarray(A._seconds_data[ind])
            fjtkz__akenr = np.ascontiguousarray(A._microseconds_data[ind])
            gns__bxdl = get_new_null_mask_slice_index(oohe__rkxcn, ind, n)
            return init_datetime_timedelta_array(uyx__hujy, nxsq__ddnli,
                fjtkz__akenr, gns__bxdl)
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
    ztk__zpcrf = (
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
            raise BodoError(ztk__zpcrf)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(ztk__zpcrf)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for akf__zgj in range(n):
                    A._days_data[ind[akf__zgj]] = val._days
                    A._seconds_data[ind[akf__zgj]] = val._seconds
                    A._microseconds_data[ind[akf__zgj]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[akf__zgj], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for akf__zgj in range(n):
                    A._days_data[ind[akf__zgj]] = val._days_data[akf__zgj]
                    A._seconds_data[ind[akf__zgj]] = val._seconds_data[akf__zgj
                        ]
                    A._microseconds_data[ind[akf__zgj]
                        ] = val._microseconds_data[akf__zgj]
                    plc__rmo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, akf__zgj)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[akf__zgj], plc__rmo)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for akf__zgj in range(n):
                    if not bodo.libs.array_kernels.isna(ind, akf__zgj) and ind[
                        akf__zgj]:
                        A._days_data[akf__zgj] = val._days
                        A._seconds_data[akf__zgj] = val._seconds
                        A._microseconds_data[akf__zgj] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            akf__zgj, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                omv__yagu = 0
                for akf__zgj in range(n):
                    if not bodo.libs.array_kernels.isna(ind, akf__zgj) and ind[
                        akf__zgj]:
                        A._days_data[akf__zgj] = val._days_data[omv__yagu]
                        A._seconds_data[akf__zgj] = val._seconds_data[omv__yagu
                            ]
                        A._microseconds_data[akf__zgj
                            ] = val._microseconds_data[omv__yagu]
                        plc__rmo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                            ._null_bitmap, omv__yagu)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            akf__zgj, plc__rmo)
                        omv__yagu += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                tqmvu__ffecm = numba.cpython.unicode._normalize_slice(ind,
                    len(A))
                for akf__zgj in range(tqmvu__ffecm.start, tqmvu__ffecm.stop,
                    tqmvu__ffecm.step):
                    A._days_data[akf__zgj] = val._days
                    A._seconds_data[akf__zgj] = val._seconds
                    A._microseconds_data[akf__zgj] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        akf__zgj, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                wkyx__scj = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, wkyx__scj, ind, n
                    )
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
            sdunp__xbsv = arg1
            numba.parfors.parfor.init_prange()
            n = len(sdunp__xbsv)
            A = alloc_datetime_timedelta_array(n)
            for akf__zgj in numba.parfors.parfor.internal_prange(n):
                A[akf__zgj] = sdunp__xbsv[akf__zgj] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            otp__vsh = True
        else:
            otp__vsh = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                pwhh__gdqbj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for akf__zgj in numba.parfors.parfor.internal_prange(n):
                    mpb__dkrwt = bodo.libs.array_kernels.isna(lhs, akf__zgj)
                    ywkph__nlla = bodo.libs.array_kernels.isna(rhs, akf__zgj)
                    if mpb__dkrwt or ywkph__nlla:
                        mhw__fdyti = otp__vsh
                    else:
                        mhw__fdyti = op(lhs[akf__zgj], rhs[akf__zgj])
                    pwhh__gdqbj[akf__zgj] = mhw__fdyti
                return pwhh__gdqbj
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                pwhh__gdqbj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for akf__zgj in numba.parfors.parfor.internal_prange(n):
                    plc__rmo = bodo.libs.array_kernels.isna(lhs, akf__zgj)
                    if plc__rmo:
                        mhw__fdyti = otp__vsh
                    else:
                        mhw__fdyti = op(lhs[akf__zgj], rhs)
                    pwhh__gdqbj[akf__zgj] = mhw__fdyti
                return pwhh__gdqbj
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                pwhh__gdqbj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for akf__zgj in numba.parfors.parfor.internal_prange(n):
                    plc__rmo = bodo.libs.array_kernels.isna(rhs, akf__zgj)
                    if plc__rmo:
                        mhw__fdyti = otp__vsh
                    else:
                        mhw__fdyti = op(lhs, rhs[akf__zgj])
                    pwhh__gdqbj[akf__zgj] = mhw__fdyti
                return pwhh__gdqbj
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for igmix__hqhfr in timedelta_unsupported_attrs:
        zzwfm__vzk = 'pandas.Timedelta.' + igmix__hqhfr
        overload_attribute(PDTimeDeltaType, igmix__hqhfr)(
            create_unsupported_overload(zzwfm__vzk))
    for ggsni__taers in timedelta_unsupported_methods:
        zzwfm__vzk = 'pandas.Timedelta.' + ggsni__taers
        overload_method(PDTimeDeltaType, ggsni__taers)(
            create_unsupported_overload(zzwfm__vzk + '()'))


_intstall_pd_timedelta_unsupported()
