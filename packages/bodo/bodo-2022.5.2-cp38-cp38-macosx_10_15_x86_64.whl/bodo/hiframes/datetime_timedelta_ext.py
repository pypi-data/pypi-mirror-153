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
        zgif__kto = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, zgif__kto)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    opdxy__hjpii = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    leqz__tqhxd = c.pyapi.long_from_longlong(opdxy__hjpii.value)
    aluq__wfpax = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(aluq__wfpax, (leqz__tqhxd,))
    c.pyapi.decref(leqz__tqhxd)
    c.pyapi.decref(aluq__wfpax)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    leqz__tqhxd = c.pyapi.object_getattr_string(val, 'value')
    pxx__qup = c.pyapi.long_as_longlong(leqz__tqhxd)
    opdxy__hjpii = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    opdxy__hjpii.value = pxx__qup
    c.pyapi.decref(leqz__tqhxd)
    omta__sxesq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(opdxy__hjpii._getvalue(), is_error=omta__sxesq)


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
            jhlo__dsuai = 1000 * microseconds
            return init_pd_timedelta(jhlo__dsuai)
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
            jhlo__dsuai = 1000 * microseconds
            return init_pd_timedelta(jhlo__dsuai)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    zdkxq__ulesk, cci__pxfg = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * zdkxq__ulesk)
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
            pri__gxpp = (rhs.microseconds + (rhs.seconds + rhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + pri__gxpp
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            kvli__spziy = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = kvli__spziy + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            ntwr__qchj = rhs.toordinal()
            rsyhd__kpoi = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            zob__nkvv = rhs.microsecond
            ewj__kvscm = lhs.value // 1000
            hiic__hhq = lhs.nanoseconds
            qun__ftjye = zob__nkvv + ewj__kvscm
            tear__oct = 1000000 * (ntwr__qchj * 86400 + rsyhd__kpoi
                ) + qun__ftjye
            gjxl__qqbuj = hiic__hhq
            return compute_pd_timestamp(tear__oct, gjxl__qqbuj)
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
            fyzae__vyk = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            fyzae__vyk = fyzae__vyk + lhs
            aducj__hnkeo, okfiu__pkbt = divmod(fyzae__vyk.seconds, 3600)
            xane__oqfit, dcioz__xlvl = divmod(okfiu__pkbt, 60)
            if 0 < fyzae__vyk.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(fyzae__vyk
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    aducj__hnkeo, xane__oqfit, dcioz__xlvl, fyzae__vyk.
                    microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            fyzae__vyk = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            fyzae__vyk = fyzae__vyk + rhs
            aducj__hnkeo, okfiu__pkbt = divmod(fyzae__vyk.seconds, 3600)
            xane__oqfit, dcioz__xlvl = divmod(okfiu__pkbt, 60)
            if 0 < fyzae__vyk.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(fyzae__vyk
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    aducj__hnkeo, xane__oqfit, dcioz__xlvl, fyzae__vyk.
                    microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            sxa__iiaop = lhs.value - rhs.value
            return pd.Timedelta(sxa__iiaop)
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
            jpiba__xmie = lhs
            numba.parfors.parfor.init_prange()
            n = len(jpiba__xmie)
            A = alloc_datetime_timedelta_array(n)
            for srtvx__pjavg in numba.parfors.parfor.internal_prange(n):
                A[srtvx__pjavg] = jpiba__xmie[srtvx__pjavg] - rhs
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
            mpfbl__ozv = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, mpfbl__ozv)
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
            aqa__zrmf, mpfbl__ozv = divmod(lhs.value, rhs.value)
            return aqa__zrmf, pd.Timedelta(mpfbl__ozv)
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
        zgif__kto = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, zgif__kto)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    opdxy__hjpii = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    nsmvt__kij = c.pyapi.long_from_longlong(opdxy__hjpii.days)
    lqwx__sggj = c.pyapi.long_from_longlong(opdxy__hjpii.seconds)
    nwf__tqnq = c.pyapi.long_from_longlong(opdxy__hjpii.microseconds)
    aluq__wfpax = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(aluq__wfpax, (nsmvt__kij,
        lqwx__sggj, nwf__tqnq))
    c.pyapi.decref(nsmvt__kij)
    c.pyapi.decref(lqwx__sggj)
    c.pyapi.decref(nwf__tqnq)
    c.pyapi.decref(aluq__wfpax)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    nsmvt__kij = c.pyapi.object_getattr_string(val, 'days')
    lqwx__sggj = c.pyapi.object_getattr_string(val, 'seconds')
    nwf__tqnq = c.pyapi.object_getattr_string(val, 'microseconds')
    zhk__zzxeg = c.pyapi.long_as_longlong(nsmvt__kij)
    tiezy__vmt = c.pyapi.long_as_longlong(lqwx__sggj)
    lebl__tdrj = c.pyapi.long_as_longlong(nwf__tqnq)
    opdxy__hjpii = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    opdxy__hjpii.days = zhk__zzxeg
    opdxy__hjpii.seconds = tiezy__vmt
    opdxy__hjpii.microseconds = lebl__tdrj
    c.pyapi.decref(nsmvt__kij)
    c.pyapi.decref(lqwx__sggj)
    c.pyapi.decref(nwf__tqnq)
    omta__sxesq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(opdxy__hjpii._getvalue(), is_error=omta__sxesq)


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
    aqa__zrmf, mpfbl__ozv = divmod(a, b)
    mpfbl__ozv *= 2
    podtn__uomz = mpfbl__ozv > b if b > 0 else mpfbl__ozv < b
    if podtn__uomz or mpfbl__ozv == b and aqa__zrmf % 2 == 1:
        aqa__zrmf += 1
    return aqa__zrmf


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
                zgc__zan = _cmp(_getstate(lhs), _getstate(rhs))
                return op(zgc__zan, 0)
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
            aqa__zrmf, mpfbl__ozv = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return aqa__zrmf, datetime.timedelta(0, 0, mpfbl__ozv)
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
    ulf__yeua = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != ulf__yeua
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
        zgif__kto = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, zgif__kto)


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
    uyur__vrmx = types.Array(types.intp, 1, 'C')
    emi__tts = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        uyur__vrmx, [n])
    xlwja__iuipv = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        uyur__vrmx, [n])
    wvvi__vwzxs = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        uyur__vrmx, [n])
    dvo__bsq = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    atas__aua = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [dvo__bsq])
    eaqtc__gxgcu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    wjkr__pksuf = cgutils.get_or_insert_function(c.builder.module,
        eaqtc__gxgcu, name='unbox_datetime_timedelta_array')
    c.builder.call(wjkr__pksuf, [val, n, emi__tts.data, xlwja__iuipv.data,
        wvvi__vwzxs.data, atas__aua.data])
    ljc__koga = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ljc__koga.days_data = emi__tts._getvalue()
    ljc__koga.seconds_data = xlwja__iuipv._getvalue()
    ljc__koga.microseconds_data = wvvi__vwzxs._getvalue()
    ljc__koga.null_bitmap = atas__aua._getvalue()
    omta__sxesq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ljc__koga._getvalue(), is_error=omta__sxesq)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    jpiba__xmie = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    emi__tts = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, jpiba__xmie.days_data)
    xlwja__iuipv = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, jpiba__xmie.seconds_data).data
    wvvi__vwzxs = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, jpiba__xmie.microseconds_data).data
    huox__tekp = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, jpiba__xmie.null_bitmap).data
    n = c.builder.extract_value(emi__tts.shape, 0)
    eaqtc__gxgcu = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    pzmf__czzz = cgutils.get_or_insert_function(c.builder.module,
        eaqtc__gxgcu, name='box_datetime_timedelta_array')
    lnge__teskn = c.builder.call(pzmf__czzz, [n, emi__tts.data,
        xlwja__iuipv, wvvi__vwzxs, huox__tekp])
    c.context.nrt.decref(c.builder, typ, val)
    return lnge__teskn


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        xsfmk__hsczv, ptg__gwy, ogpbk__bbhbm, boch__gzgni = args
        ikoea__iajm = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ikoea__iajm.days_data = xsfmk__hsczv
        ikoea__iajm.seconds_data = ptg__gwy
        ikoea__iajm.microseconds_data = ogpbk__bbhbm
        ikoea__iajm.null_bitmap = boch__gzgni
        context.nrt.incref(builder, signature.args[0], xsfmk__hsczv)
        context.nrt.incref(builder, signature.args[1], ptg__gwy)
        context.nrt.incref(builder, signature.args[2], ogpbk__bbhbm)
        context.nrt.incref(builder, signature.args[3], boch__gzgni)
        return ikoea__iajm._getvalue()
    mjry__epu = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return mjry__epu, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    emi__tts = np.empty(n, np.int64)
    xlwja__iuipv = np.empty(n, np.int64)
    wvvi__vwzxs = np.empty(n, np.int64)
    uekpl__bel = np.empty(n + 7 >> 3, np.uint8)
    for srtvx__pjavg, s in enumerate(pyval):
        ohxvf__sla = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(uekpl__bel, srtvx__pjavg, int(
            not ohxvf__sla))
        if not ohxvf__sla:
            emi__tts[srtvx__pjavg] = s.days
            xlwja__iuipv[srtvx__pjavg] = s.seconds
            wvvi__vwzxs[srtvx__pjavg] = s.microseconds
    xip__alsn = context.get_constant_generic(builder, days_data_type, emi__tts)
    dtag__jqugs = context.get_constant_generic(builder, seconds_data_type,
        xlwja__iuipv)
    mqts__thdb = context.get_constant_generic(builder,
        microseconds_data_type, wvvi__vwzxs)
    vgf__juzrm = context.get_constant_generic(builder, nulls_type, uekpl__bel)
    return lir.Constant.literal_struct([xip__alsn, dtag__jqugs, mqts__thdb,
        vgf__juzrm])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    emi__tts = np.empty(n, dtype=np.int64)
    xlwja__iuipv = np.empty(n, dtype=np.int64)
    wvvi__vwzxs = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(emi__tts, xlwja__iuipv,
        wvvi__vwzxs, nulls)


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
            tsymq__giash = bodo.utils.conversion.coerce_to_ndarray(ind)
            fqaqi__gsn = A._null_bitmap
            jwv__igzg = A._days_data[tsymq__giash]
            nyobo__lns = A._seconds_data[tsymq__giash]
            fboed__des = A._microseconds_data[tsymq__giash]
            n = len(jwv__igzg)
            kti__epuf = get_new_null_mask_bool_index(fqaqi__gsn, ind, n)
            return init_datetime_timedelta_array(jwv__igzg, nyobo__lns,
                fboed__des, kti__epuf)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            tsymq__giash = bodo.utils.conversion.coerce_to_ndarray(ind)
            fqaqi__gsn = A._null_bitmap
            jwv__igzg = A._days_data[tsymq__giash]
            nyobo__lns = A._seconds_data[tsymq__giash]
            fboed__des = A._microseconds_data[tsymq__giash]
            n = len(jwv__igzg)
            kti__epuf = get_new_null_mask_int_index(fqaqi__gsn, tsymq__giash, n
                )
            return init_datetime_timedelta_array(jwv__igzg, nyobo__lns,
                fboed__des, kti__epuf)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            fqaqi__gsn = A._null_bitmap
            jwv__igzg = np.ascontiguousarray(A._days_data[ind])
            nyobo__lns = np.ascontiguousarray(A._seconds_data[ind])
            fboed__des = np.ascontiguousarray(A._microseconds_data[ind])
            kti__epuf = get_new_null_mask_slice_index(fqaqi__gsn, ind, n)
            return init_datetime_timedelta_array(jwv__igzg, nyobo__lns,
                fboed__des, kti__epuf)
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
    swkiw__slamt = (
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
            raise BodoError(swkiw__slamt)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(swkiw__slamt)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for srtvx__pjavg in range(n):
                    A._days_data[ind[srtvx__pjavg]] = val._days
                    A._seconds_data[ind[srtvx__pjavg]] = val._seconds
                    A._microseconds_data[ind[srtvx__pjavg]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[srtvx__pjavg], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for srtvx__pjavg in range(n):
                    A._days_data[ind[srtvx__pjavg]] = val._days_data[
                        srtvx__pjavg]
                    A._seconds_data[ind[srtvx__pjavg]] = val._seconds_data[
                        srtvx__pjavg]
                    A._microseconds_data[ind[srtvx__pjavg]
                        ] = val._microseconds_data[srtvx__pjavg]
                    drenj__shzt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, srtvx__pjavg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[srtvx__pjavg], drenj__shzt)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for srtvx__pjavg in range(n):
                    if not bodo.libs.array_kernels.isna(ind, srtvx__pjavg
                        ) and ind[srtvx__pjavg]:
                        A._days_data[srtvx__pjavg] = val._days
                        A._seconds_data[srtvx__pjavg] = val._seconds
                        A._microseconds_data[srtvx__pjavg] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            srtvx__pjavg, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                jevl__lyry = 0
                for srtvx__pjavg in range(n):
                    if not bodo.libs.array_kernels.isna(ind, srtvx__pjavg
                        ) and ind[srtvx__pjavg]:
                        A._days_data[srtvx__pjavg] = val._days_data[jevl__lyry]
                        A._seconds_data[srtvx__pjavg] = val._seconds_data[
                            jevl__lyry]
                        A._microseconds_data[srtvx__pjavg
                            ] = val._microseconds_data[jevl__lyry]
                        drenj__shzt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, jevl__lyry)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            srtvx__pjavg, drenj__shzt)
                        jevl__lyry += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                evj__bij = numba.cpython.unicode._normalize_slice(ind, len(A))
                for srtvx__pjavg in range(evj__bij.start, evj__bij.stop,
                    evj__bij.step):
                    A._days_data[srtvx__pjavg] = val._days
                    A._seconds_data[srtvx__pjavg] = val._seconds
                    A._microseconds_data[srtvx__pjavg] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        srtvx__pjavg, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                qttb__xvtgc = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, qttb__xvtgc,
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
            jpiba__xmie = arg1
            numba.parfors.parfor.init_prange()
            n = len(jpiba__xmie)
            A = alloc_datetime_timedelta_array(n)
            for srtvx__pjavg in numba.parfors.parfor.internal_prange(n):
                A[srtvx__pjavg] = jpiba__xmie[srtvx__pjavg] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            qhvvb__immf = True
        else:
            qhvvb__immf = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                rpays__sve = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for srtvx__pjavg in numba.parfors.parfor.internal_prange(n):
                    dgtb__wgo = bodo.libs.array_kernels.isna(lhs, srtvx__pjavg)
                    pwajt__ymfts = bodo.libs.array_kernels.isna(rhs,
                        srtvx__pjavg)
                    if dgtb__wgo or pwajt__ymfts:
                        aeyii__hgg = qhvvb__immf
                    else:
                        aeyii__hgg = op(lhs[srtvx__pjavg], rhs[srtvx__pjavg])
                    rpays__sve[srtvx__pjavg] = aeyii__hgg
                return rpays__sve
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                rpays__sve = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for srtvx__pjavg in numba.parfors.parfor.internal_prange(n):
                    drenj__shzt = bodo.libs.array_kernels.isna(lhs,
                        srtvx__pjavg)
                    if drenj__shzt:
                        aeyii__hgg = qhvvb__immf
                    else:
                        aeyii__hgg = op(lhs[srtvx__pjavg], rhs)
                    rpays__sve[srtvx__pjavg] = aeyii__hgg
                return rpays__sve
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                rpays__sve = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for srtvx__pjavg in numba.parfors.parfor.internal_prange(n):
                    drenj__shzt = bodo.libs.array_kernels.isna(rhs,
                        srtvx__pjavg)
                    if drenj__shzt:
                        aeyii__hgg = qhvvb__immf
                    else:
                        aeyii__hgg = op(lhs, rhs[srtvx__pjavg])
                    rpays__sve[srtvx__pjavg] = aeyii__hgg
                return rpays__sve
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for ago__chz in timedelta_unsupported_attrs:
        rpcyp__brj = 'pandas.Timedelta.' + ago__chz
        overload_attribute(PDTimeDeltaType, ago__chz)(
            create_unsupported_overload(rpcyp__brj))
    for vkd__cpxc in timedelta_unsupported_methods:
        rpcyp__brj = 'pandas.Timedelta.' + vkd__cpxc
        overload_method(PDTimeDeltaType, vkd__cpxc)(create_unsupported_overload
            (rpcyp__brj + '()'))


_intstall_pd_timedelta_unsupported()
