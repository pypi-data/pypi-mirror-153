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
        rtfxl__ogf = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, rtfxl__ogf)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    dtpn__sdduj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    gdfxf__syaa = c.pyapi.long_from_longlong(dtpn__sdduj.value)
    jugp__vne = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(jugp__vne, (gdfxf__syaa,))
    c.pyapi.decref(gdfxf__syaa)
    c.pyapi.decref(jugp__vne)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    gdfxf__syaa = c.pyapi.object_getattr_string(val, 'value')
    lgshs__zbten = c.pyapi.long_as_longlong(gdfxf__syaa)
    dtpn__sdduj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    dtpn__sdduj.value = lgshs__zbten
    c.pyapi.decref(gdfxf__syaa)
    wjbc__bqhx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dtpn__sdduj._getvalue(), is_error=wjbc__bqhx)


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
            qdh__divw = 1000 * microseconds
            return init_pd_timedelta(qdh__divw)
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
            qdh__divw = 1000 * microseconds
            return init_pd_timedelta(qdh__divw)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    vjlg__xnuvc, osivp__rnbb = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * vjlg__xnuvc)
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
            eyui__cqggh = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + eyui__cqggh
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            rreza__epad = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = rreza__epad + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            gip__muwye = rhs.toordinal()
            rjf__ewh = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            focie__pprs = rhs.microsecond
            jtod__qaz = lhs.value // 1000
            ocbj__rrhsm = lhs.nanoseconds
            liea__wutd = focie__pprs + jtod__qaz
            cjnit__hpk = 1000000 * (gip__muwye * 86400 + rjf__ewh) + liea__wutd
            digp__qzj = ocbj__rrhsm
            return compute_pd_timestamp(cjnit__hpk, digp__qzj)
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
            mfxpn__nsfs = datetime.timedelta(rhs.toordinal(), hours=rhs.
                hour, minutes=rhs.minute, seconds=rhs.second, microseconds=
                rhs.microsecond)
            mfxpn__nsfs = mfxpn__nsfs + lhs
            eozq__hggfp, esa__blvbu = divmod(mfxpn__nsfs.seconds, 3600)
            lypc__evd, wnzw__llb = divmod(esa__blvbu, 60)
            if 0 < mfxpn__nsfs.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(
                    mfxpn__nsfs.days)
                return datetime.datetime(d.year, d.month, d.day,
                    eozq__hggfp, lypc__evd, wnzw__llb, mfxpn__nsfs.microseconds
                    )
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            mfxpn__nsfs = datetime.timedelta(lhs.toordinal(), hours=lhs.
                hour, minutes=lhs.minute, seconds=lhs.second, microseconds=
                lhs.microsecond)
            mfxpn__nsfs = mfxpn__nsfs + rhs
            eozq__hggfp, esa__blvbu = divmod(mfxpn__nsfs.seconds, 3600)
            lypc__evd, wnzw__llb = divmod(esa__blvbu, 60)
            if 0 < mfxpn__nsfs.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(
                    mfxpn__nsfs.days)
                return datetime.datetime(d.year, d.month, d.day,
                    eozq__hggfp, lypc__evd, wnzw__llb, mfxpn__nsfs.microseconds
                    )
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            tiz__jgy = lhs.value - rhs.value
            return pd.Timedelta(tiz__jgy)
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
            ddf__rgz = lhs
            numba.parfors.parfor.init_prange()
            n = len(ddf__rgz)
            A = alloc_datetime_timedelta_array(n)
            for mip__jba in numba.parfors.parfor.internal_prange(n):
                A[mip__jba] = ddf__rgz[mip__jba] - rhs
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
            ztoe__rumg = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, ztoe__rumg)
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
            rhch__rfmyp, ztoe__rumg = divmod(lhs.value, rhs.value)
            return rhch__rfmyp, pd.Timedelta(ztoe__rumg)
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
        rtfxl__ogf = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, rtfxl__ogf)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    dtpn__sdduj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    dygax__xlvh = c.pyapi.long_from_longlong(dtpn__sdduj.days)
    neeja__mvahe = c.pyapi.long_from_longlong(dtpn__sdduj.seconds)
    fbcoe__judd = c.pyapi.long_from_longlong(dtpn__sdduj.microseconds)
    jugp__vne = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(jugp__vne, (dygax__xlvh,
        neeja__mvahe, fbcoe__judd))
    c.pyapi.decref(dygax__xlvh)
    c.pyapi.decref(neeja__mvahe)
    c.pyapi.decref(fbcoe__judd)
    c.pyapi.decref(jugp__vne)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    dygax__xlvh = c.pyapi.object_getattr_string(val, 'days')
    neeja__mvahe = c.pyapi.object_getattr_string(val, 'seconds')
    fbcoe__judd = c.pyapi.object_getattr_string(val, 'microseconds')
    thkux__gar = c.pyapi.long_as_longlong(dygax__xlvh)
    mxni__ergv = c.pyapi.long_as_longlong(neeja__mvahe)
    cgccu__wqcra = c.pyapi.long_as_longlong(fbcoe__judd)
    dtpn__sdduj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    dtpn__sdduj.days = thkux__gar
    dtpn__sdduj.seconds = mxni__ergv
    dtpn__sdduj.microseconds = cgccu__wqcra
    c.pyapi.decref(dygax__xlvh)
    c.pyapi.decref(neeja__mvahe)
    c.pyapi.decref(fbcoe__judd)
    wjbc__bqhx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dtpn__sdduj._getvalue(), is_error=wjbc__bqhx)


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
    rhch__rfmyp, ztoe__rumg = divmod(a, b)
    ztoe__rumg *= 2
    uenp__oewo = ztoe__rumg > b if b > 0 else ztoe__rumg < b
    if uenp__oewo or ztoe__rumg == b and rhch__rfmyp % 2 == 1:
        rhch__rfmyp += 1
    return rhch__rfmyp


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
                fhagu__rgnb = _cmp(_getstate(lhs), _getstate(rhs))
                return op(fhagu__rgnb, 0)
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
            rhch__rfmyp, ztoe__rumg = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return rhch__rfmyp, datetime.timedelta(0, 0, ztoe__rumg)
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
    qlp__rgyv = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != qlp__rgyv
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
        rtfxl__ogf = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, rtfxl__ogf)


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
    crtd__qvkm = types.Array(types.intp, 1, 'C')
    ngqej__arwv = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        crtd__qvkm, [n])
    mxrvp__zvq = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        crtd__qvkm, [n])
    stsw__liadb = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        crtd__qvkm, [n])
    fyqsf__hjgrj = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    umhi__ukgjn = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [fyqsf__hjgrj])
    srojg__esf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    anus__zpat = cgutils.get_or_insert_function(c.builder.module,
        srojg__esf, name='unbox_datetime_timedelta_array')
    c.builder.call(anus__zpat, [val, n, ngqej__arwv.data, mxrvp__zvq.data,
        stsw__liadb.data, umhi__ukgjn.data])
    qyc__kqpou = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qyc__kqpou.days_data = ngqej__arwv._getvalue()
    qyc__kqpou.seconds_data = mxrvp__zvq._getvalue()
    qyc__kqpou.microseconds_data = stsw__liadb._getvalue()
    qyc__kqpou.null_bitmap = umhi__ukgjn._getvalue()
    wjbc__bqhx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qyc__kqpou._getvalue(), is_error=wjbc__bqhx)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    ddf__rgz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ngqej__arwv = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ddf__rgz.days_data)
    mxrvp__zvq = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ddf__rgz.seconds_data).data
    stsw__liadb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ddf__rgz.microseconds_data).data
    bftv__jsfv = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, ddf__rgz.null_bitmap).data
    n = c.builder.extract_value(ngqej__arwv.shape, 0)
    srojg__esf = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    fdaup__iyqz = cgutils.get_or_insert_function(c.builder.module,
        srojg__esf, name='box_datetime_timedelta_array')
    uabd__szzb = c.builder.call(fdaup__iyqz, [n, ngqej__arwv.data,
        mxrvp__zvq, stsw__liadb, bftv__jsfv])
    c.context.nrt.decref(c.builder, typ, val)
    return uabd__szzb


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        tnf__qbrez, konj__ehz, wlhc__bpz, zjr__rcj = args
        ijsmv__gtpq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ijsmv__gtpq.days_data = tnf__qbrez
        ijsmv__gtpq.seconds_data = konj__ehz
        ijsmv__gtpq.microseconds_data = wlhc__bpz
        ijsmv__gtpq.null_bitmap = zjr__rcj
        context.nrt.incref(builder, signature.args[0], tnf__qbrez)
        context.nrt.incref(builder, signature.args[1], konj__ehz)
        context.nrt.incref(builder, signature.args[2], wlhc__bpz)
        context.nrt.incref(builder, signature.args[3], zjr__rcj)
        return ijsmv__gtpq._getvalue()
    xcgxt__irhgy = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return xcgxt__irhgy, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    ngqej__arwv = np.empty(n, np.int64)
    mxrvp__zvq = np.empty(n, np.int64)
    stsw__liadb = np.empty(n, np.int64)
    odu__ylc = np.empty(n + 7 >> 3, np.uint8)
    for mip__jba, s in enumerate(pyval):
        jdypq__jcduw = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(odu__ylc, mip__jba, int(not
            jdypq__jcduw))
        if not jdypq__jcduw:
            ngqej__arwv[mip__jba] = s.days
            mxrvp__zvq[mip__jba] = s.seconds
            stsw__liadb[mip__jba] = s.microseconds
    uhhbc__upd = context.get_constant_generic(builder, days_data_type,
        ngqej__arwv)
    ozx__yxfb = context.get_constant_generic(builder, seconds_data_type,
        mxrvp__zvq)
    lgqcc__mrj = context.get_constant_generic(builder,
        microseconds_data_type, stsw__liadb)
    sfy__tpoaf = context.get_constant_generic(builder, nulls_type, odu__ylc)
    return lir.Constant.literal_struct([uhhbc__upd, ozx__yxfb, lgqcc__mrj,
        sfy__tpoaf])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    ngqej__arwv = np.empty(n, dtype=np.int64)
    mxrvp__zvq = np.empty(n, dtype=np.int64)
    stsw__liadb = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(ngqej__arwv, mxrvp__zvq,
        stsw__liadb, nulls)


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
            jlvx__djgn = bodo.utils.conversion.coerce_to_ndarray(ind)
            usl__fweae = A._null_bitmap
            jgxeq__tpes = A._days_data[jlvx__djgn]
            pnhu__arff = A._seconds_data[jlvx__djgn]
            csdx__ifgbl = A._microseconds_data[jlvx__djgn]
            n = len(jgxeq__tpes)
            jkpwn__fsyf = get_new_null_mask_bool_index(usl__fweae, ind, n)
            return init_datetime_timedelta_array(jgxeq__tpes, pnhu__arff,
                csdx__ifgbl, jkpwn__fsyf)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            jlvx__djgn = bodo.utils.conversion.coerce_to_ndarray(ind)
            usl__fweae = A._null_bitmap
            jgxeq__tpes = A._days_data[jlvx__djgn]
            pnhu__arff = A._seconds_data[jlvx__djgn]
            csdx__ifgbl = A._microseconds_data[jlvx__djgn]
            n = len(jgxeq__tpes)
            jkpwn__fsyf = get_new_null_mask_int_index(usl__fweae, jlvx__djgn, n
                )
            return init_datetime_timedelta_array(jgxeq__tpes, pnhu__arff,
                csdx__ifgbl, jkpwn__fsyf)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            usl__fweae = A._null_bitmap
            jgxeq__tpes = np.ascontiguousarray(A._days_data[ind])
            pnhu__arff = np.ascontiguousarray(A._seconds_data[ind])
            csdx__ifgbl = np.ascontiguousarray(A._microseconds_data[ind])
            jkpwn__fsyf = get_new_null_mask_slice_index(usl__fweae, ind, n)
            return init_datetime_timedelta_array(jgxeq__tpes, pnhu__arff,
                csdx__ifgbl, jkpwn__fsyf)
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
    tyyw__wtw = (
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
            raise BodoError(tyyw__wtw)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(tyyw__wtw)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for mip__jba in range(n):
                    A._days_data[ind[mip__jba]] = val._days
                    A._seconds_data[ind[mip__jba]] = val._seconds
                    A._microseconds_data[ind[mip__jba]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[mip__jba], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for mip__jba in range(n):
                    A._days_data[ind[mip__jba]] = val._days_data[mip__jba]
                    A._seconds_data[ind[mip__jba]] = val._seconds_data[mip__jba
                        ]
                    A._microseconds_data[ind[mip__jba]
                        ] = val._microseconds_data[mip__jba]
                    xiyt__kaj = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, mip__jba)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[mip__jba], xiyt__kaj)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for mip__jba in range(n):
                    if not bodo.libs.array_kernels.isna(ind, mip__jba) and ind[
                        mip__jba]:
                        A._days_data[mip__jba] = val._days
                        A._seconds_data[mip__jba] = val._seconds
                        A._microseconds_data[mip__jba] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            mip__jba, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                fakn__obf = 0
                for mip__jba in range(n):
                    if not bodo.libs.array_kernels.isna(ind, mip__jba) and ind[
                        mip__jba]:
                        A._days_data[mip__jba] = val._days_data[fakn__obf]
                        A._seconds_data[mip__jba] = val._seconds_data[fakn__obf
                            ]
                        A._microseconds_data[mip__jba
                            ] = val._microseconds_data[fakn__obf]
                        xiyt__kaj = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, fakn__obf)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            mip__jba, xiyt__kaj)
                        fakn__obf += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                yfasx__hcjeh = numba.cpython.unicode._normalize_slice(ind,
                    len(A))
                for mip__jba in range(yfasx__hcjeh.start, yfasx__hcjeh.stop,
                    yfasx__hcjeh.step):
                    A._days_data[mip__jba] = val._days
                    A._seconds_data[mip__jba] = val._seconds
                    A._microseconds_data[mip__jba] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        mip__jba, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                woqf__xep = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, woqf__xep, ind, n
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
            ddf__rgz = arg1
            numba.parfors.parfor.init_prange()
            n = len(ddf__rgz)
            A = alloc_datetime_timedelta_array(n)
            for mip__jba in numba.parfors.parfor.internal_prange(n):
                A[mip__jba] = ddf__rgz[mip__jba] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            xlk__lwwy = True
        else:
            xlk__lwwy = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                ple__jwf = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for mip__jba in numba.parfors.parfor.internal_prange(n):
                    mny__uwzo = bodo.libs.array_kernels.isna(lhs, mip__jba)
                    riu__oogv = bodo.libs.array_kernels.isna(rhs, mip__jba)
                    if mny__uwzo or riu__oogv:
                        mhzxf__vhc = xlk__lwwy
                    else:
                        mhzxf__vhc = op(lhs[mip__jba], rhs[mip__jba])
                    ple__jwf[mip__jba] = mhzxf__vhc
                return ple__jwf
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                ple__jwf = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for mip__jba in numba.parfors.parfor.internal_prange(n):
                    xiyt__kaj = bodo.libs.array_kernels.isna(lhs, mip__jba)
                    if xiyt__kaj:
                        mhzxf__vhc = xlk__lwwy
                    else:
                        mhzxf__vhc = op(lhs[mip__jba], rhs)
                    ple__jwf[mip__jba] = mhzxf__vhc
                return ple__jwf
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                ple__jwf = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for mip__jba in numba.parfors.parfor.internal_prange(n):
                    xiyt__kaj = bodo.libs.array_kernels.isna(rhs, mip__jba)
                    if xiyt__kaj:
                        mhzxf__vhc = xlk__lwwy
                    else:
                        mhzxf__vhc = op(lhs, rhs[mip__jba])
                    ple__jwf[mip__jba] = mhzxf__vhc
                return ple__jwf
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for yyjx__anno in timedelta_unsupported_attrs:
        sili__wye = 'pandas.Timedelta.' + yyjx__anno
        overload_attribute(PDTimeDeltaType, yyjx__anno)(
            create_unsupported_overload(sili__wye))
    for shfoj__dmmjm in timedelta_unsupported_methods:
        sili__wye = 'pandas.Timedelta.' + shfoj__dmmjm
        overload_method(PDTimeDeltaType, shfoj__dmmjm)(
            create_unsupported_overload(sili__wye + '()'))


_intstall_pd_timedelta_unsupported()
