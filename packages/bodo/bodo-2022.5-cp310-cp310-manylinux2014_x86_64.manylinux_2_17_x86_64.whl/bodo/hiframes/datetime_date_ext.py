"""Numba extension support for datetime.date objects and their arrays.
"""
import datetime
import operator
import warnings
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.typing.templates import AttributeTemplate, infer_getattr
from numba.core.utils import PYVERSION
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import DatetimeDatetimeType
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type, is_overload_int, is_overload_none
ll.add_symbol('box_datetime_date_array', hdatetime_ext.box_datetime_date_array)
ll.add_symbol('unbox_datetime_date_array', hdatetime_ext.
    unbox_datetime_date_array)
ll.add_symbol('get_isocalendar', hdatetime_ext.get_isocalendar)


class DatetimeDateType(types.Type):

    def __init__(self):
        super(DatetimeDateType, self).__init__(name='DatetimeDateType()')
        self.bitwidth = 64


datetime_date_type = DatetimeDateType()


@typeof_impl.register(datetime.date)
def typeof_datetime_date(val, c):
    return datetime_date_type


register_model(DatetimeDateType)(models.IntegerModel)


@infer_getattr
class DatetimeAttribute(AttributeTemplate):
    key = DatetimeDateType

    def resolve_year(self, typ):
        return types.int64

    def resolve_month(self, typ):
        return types.int64

    def resolve_day(self, typ):
        return types.int64


@lower_getattr(DatetimeDateType, 'year')
def datetime_get_year(context, builder, typ, val):
    return builder.lshr(val, lir.Constant(lir.IntType(64), 32))


@lower_getattr(DatetimeDateType, 'month')
def datetime_get_month(context, builder, typ, val):
    return builder.and_(builder.lshr(val, lir.Constant(lir.IntType(64), 16)
        ), lir.Constant(lir.IntType(64), 65535))


@lower_getattr(DatetimeDateType, 'day')
def datetime_get_day(context, builder, typ, val):
    return builder.and_(val, lir.Constant(lir.IntType(64), 65535))


@unbox(DatetimeDateType)
def unbox_datetime_date(typ, val, c):
    uokok__pgdp = c.pyapi.object_getattr_string(val, 'year')
    huzlx__egi = c.pyapi.object_getattr_string(val, 'month')
    fbbqv__xvg = c.pyapi.object_getattr_string(val, 'day')
    dtape__gvxs = c.pyapi.long_as_longlong(uokok__pgdp)
    trdta__sry = c.pyapi.long_as_longlong(huzlx__egi)
    ffdsa__nesa = c.pyapi.long_as_longlong(fbbqv__xvg)
    nxr__zgp = c.builder.add(ffdsa__nesa, c.builder.add(c.builder.shl(
        dtape__gvxs, lir.Constant(lir.IntType(64), 32)), c.builder.shl(
        trdta__sry, lir.Constant(lir.IntType(64), 16))))
    c.pyapi.decref(uokok__pgdp)
    c.pyapi.decref(huzlx__egi)
    c.pyapi.decref(fbbqv__xvg)
    fkmiy__uifei = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nxr__zgp, is_error=fkmiy__uifei)


@lower_constant(DatetimeDateType)
def lower_constant_datetime_date(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    nxr__zgp = builder.add(day, builder.add(builder.shl(year, lir.Constant(
        lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir.IntType(
        64), 16))))
    return nxr__zgp


@box(DatetimeDateType)
def box_datetime_date(typ, val, c):
    uokok__pgdp = c.pyapi.long_from_longlong(c.builder.lshr(val, lir.
        Constant(lir.IntType(64), 32)))
    huzlx__egi = c.pyapi.long_from_longlong(c.builder.and_(c.builder.lshr(
        val, lir.Constant(lir.IntType(64), 16)), lir.Constant(lir.IntType(
        64), 65535)))
    fbbqv__xvg = c.pyapi.long_from_longlong(c.builder.and_(val, lir.
        Constant(lir.IntType(64), 65535)))
    ltoq__sbxry = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.date))
    tfrvd__gmg = c.pyapi.call_function_objargs(ltoq__sbxry, (uokok__pgdp,
        huzlx__egi, fbbqv__xvg))
    c.pyapi.decref(uokok__pgdp)
    c.pyapi.decref(huzlx__egi)
    c.pyapi.decref(fbbqv__xvg)
    c.pyapi.decref(ltoq__sbxry)
    return tfrvd__gmg


@type_callable(datetime.date)
def type_datetime_date(context):

    def typer(year, month, day):
        return datetime_date_type
    return typer


@lower_builtin(datetime.date, types.IntegerLiteral, types.IntegerLiteral,
    types.IntegerLiteral)
@lower_builtin(datetime.date, types.int64, types.int64, types.int64)
def impl_ctor_datetime_date(context, builder, sig, args):
    year, month, day = args
    nxr__zgp = builder.add(day, builder.add(builder.shl(year, lir.Constant(
        lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir.IntType(
        64), 16))))
    return nxr__zgp


@intrinsic
def cast_int_to_datetime_date(typingctx, val=None):
    assert val == types.int64

    def codegen(context, builder, signature, args):
        return args[0]
    return datetime_date_type(types.int64), codegen


@intrinsic
def cast_datetime_date_to_int(typingctx, val=None):
    assert val == datetime_date_type

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(datetime_date_type), codegen


"""
Following codes are copied from
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = np.array([-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 
    31], dtype=np.int64)
_DAYS_BEFORE_MONTH = np.array([-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 
    273, 304, 334], dtype=np.int64)


@register_jitable
def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


@register_jitable
def _days_before_year(year):
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


@register_jitable
def _days_in_month(year, month):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


@register_jitable
def _days_before_month(year, month):
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)


@register_jitable
def _ymd2ord(year, month, day):
    hlc__dbwq = _days_in_month(year, month)
    return _days_before_year(year) + _days_before_month(year, month) + day


@register_jitable
def _ord2ymd(n):
    n -= 1
    iss__wct, n = divmod(n, _DI400Y)
    year = iss__wct * 400 + 1
    brlf__zbegg, n = divmod(n, _DI100Y)
    dccd__zzuh, n = divmod(n, _DI4Y)
    dxfr__eocd, n = divmod(n, 365)
    year += brlf__zbegg * 100 + dccd__zzuh * 4 + dxfr__eocd
    if dxfr__eocd == 4 or brlf__zbegg == 4:
        return year - 1, 12, 31
    nbdy__mfy = dxfr__eocd == 3 and (dccd__zzuh != 24 or brlf__zbegg == 3)
    month = n + 50 >> 5
    jwh__sihk = _DAYS_BEFORE_MONTH[month] + (month > 2 and nbdy__mfy)
    if jwh__sihk > n:
        month -= 1
        jwh__sihk -= _DAYS_IN_MONTH[month] + (month == 2 and nbdy__mfy)
    n -= jwh__sihk
    return year, month, n + 1


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@intrinsic
def get_isocalendar(typingctx, dt_year, dt_month, dt_day):

    def codegen(context, builder, sig, args):
        year = cgutils.alloca_once(builder, lir.IntType(64))
        lnq__srhsl = cgutils.alloca_once(builder, lir.IntType(64))
        ornkk__bak = cgutils.alloca_once(builder, lir.IntType(64))
        sbdq__pbgjs = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
            lir.IntType(64), lir.IntType(64), lir.IntType(64).as_pointer(),
            lir.IntType(64).as_pointer(), lir.IntType(64).as_pointer()])
        kbqip__qmtkp = cgutils.get_or_insert_function(builder.module,
            sbdq__pbgjs, name='get_isocalendar')
        builder.call(kbqip__qmtkp, [args[0], args[1], args[2], year,
            lnq__srhsl, ornkk__bak])
        return cgutils.pack_array(builder, [builder.load(year), builder.
            load(lnq__srhsl), builder.load(ornkk__bak)])
    tfrvd__gmg = types.Tuple([types.int64, types.int64, types.int64])(types
        .int64, types.int64, types.int64), codegen
    return tfrvd__gmg


types.datetime_date_type = datetime_date_type


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_date_type'):
        d = datetime.date.today()
    return d


@register_jitable
def fromordinal_impl(n):
    y, gab__auw, d = _ord2ymd(n)
    return datetime.date(y, gab__auw, d)


@overload_method(DatetimeDateType, 'replace')
def replace_overload(date, year=None, month=None, day=None):
    if not is_overload_none(year) and not is_overload_int(year):
        raise BodoError('date.replace(): year must be an integer')
    elif not is_overload_none(month) and not is_overload_int(month):
        raise BodoError('date.replace(): month must be an integer')
    elif not is_overload_none(day) and not is_overload_int(day):
        raise BodoError('date.replace(): day must be an integer')

    def impl(date, year=None, month=None, day=None):
        uusa__jwjni = date.year if year is None else year
        anj__focg = date.month if month is None else month
        ftqr__vwzz = date.day if day is None else day
        return datetime.date(uusa__jwjni, anj__focg, ftqr__vwzz)
    return impl


@overload_method(DatetimeDatetimeType, 'toordinal', no_unliteral=True)
@overload_method(DatetimeDateType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


@overload_method(DatetimeDatetimeType, 'weekday', no_unliteral=True)
@overload_method(DatetimeDateType, 'weekday', no_unliteral=True)
def weekday(date):

    def impl(date):
        return (date.toordinal() + 6) % 7
    return impl


@overload_method(DatetimeDateType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(date):

    def impl(date):
        year, lnq__srhsl, cwqf__cpxs = get_isocalendar(date.year, date.
            month, date.day)
        return year, lnq__srhsl, cwqf__cpxs
    return impl


def overload_add_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ude__uwthy = lhs.toordinal() + rhs.days
            if 0 < ude__uwthy <= _MAXORDINAL:
                return fromordinal_impl(ude__uwthy)
            raise OverflowError('result out of range')
        return impl
    elif lhs == datetime_timedelta_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            ude__uwthy = lhs.days + rhs.toordinal()
            if 0 < ude__uwthy <= _MAXORDINAL:
                return fromordinal_impl(ude__uwthy)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + datetime.timedelta(-rhs.days)
        return impl
    elif lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            dww__mwcqc = lhs.toordinal()
            mjubl__hmml = rhs.toordinal()
            return datetime.timedelta(dww__mwcqc - mjubl__hmml)
        return impl
    if lhs == datetime_date_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            qvii__thhk = lhs
            numba.parfors.parfor.init_prange()
            n = len(qvii__thhk)
            A = alloc_datetime_date_array(n)
            for juyj__ypk in numba.parfors.parfor.internal_prange(n):
                A[juyj__ypk] = qvii__thhk[juyj__ypk] - rhs
            return A
        return impl


@overload(min, no_unliteral=True)
def date_min(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def date_max(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        chpfs__wmceu = np.uint8(td.year // 256)
        aviy__xpbf = np.uint8(td.year % 256)
        month = np.uint8(td.month)
        day = np.uint8(td.day)
        oybqt__szym = chpfs__wmceu, aviy__xpbf, month, day
        return hash(oybqt__szym)
    return impl


@overload(bool, inline='always', no_unliteral=True)
def date_to_bool(date):
    if date != datetime_date_type:
        return

    def impl(date):
        return True
    return impl


if PYVERSION >= (3, 9):
    IsoCalendarDate = datetime.date(2011, 1, 1).isocalendar().__class__


    class IsoCalendarDateType(types.Type):

        def __init__(self):
            super(IsoCalendarDateType, self).__init__(name=
                'IsoCalendarDateType()')
    iso_calendar_date_type = DatetimeDateType()

    @typeof_impl.register(IsoCalendarDate)
    def typeof_datetime_date(val, c):
        return iso_calendar_date_type


class DatetimeDateArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeDateArrayType, self).__init__(name=
            'DatetimeDateArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_date_type

    def copy(self):
        return DatetimeDateArrayType()


datetime_date_array_type = DatetimeDateArrayType()
types.datetime_date_array_type = datetime_date_array_type
data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeDateArrayType)
class DatetimeDateArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wkiz__ytugi = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, wkiz__ytugi)


make_attribute_wrapper(DatetimeDateArrayType, 'data', '_data')
make_attribute_wrapper(DatetimeDateArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(DatetimeDateArrayType, 'copy', no_unliteral=True)
def overload_datetime_date_arr_copy(A):
    return lambda A: bodo.hiframes.datetime_date_ext.init_datetime_date_array(A
        ._data.copy(), A._null_bitmap.copy())


@overload_attribute(DatetimeDateArrayType, 'dtype')
def overload_datetime_date_arr_dtype(A):
    return lambda A: np.object_


@unbox(DatetimeDateArrayType)
def unbox_datetime_date_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    fdl__tpe = types.Array(types.intp, 1, 'C')
    ucum__dmpv = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        fdl__tpe, [n])
    ezl__buhv = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    wwjhc__krgmp = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [ezl__buhv])
    sbdq__pbgjs = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(8).as_pointer()])
    lgsit__gxpwb = cgutils.get_or_insert_function(c.builder.module,
        sbdq__pbgjs, name='unbox_datetime_date_array')
    c.builder.call(lgsit__gxpwb, [val, n, ucum__dmpv.data, wwjhc__krgmp.data])
    qtuj__pwtp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qtuj__pwtp.data = ucum__dmpv._getvalue()
    qtuj__pwtp.null_bitmap = wwjhc__krgmp._getvalue()
    fkmiy__uifei = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qtuj__pwtp._getvalue(), is_error=fkmiy__uifei)


def int_to_datetime_date_python(ia):
    return datetime.date(ia >> 32, ia >> 16 & 65535, ia & 65535)


def int_array_to_datetime_date(ia):
    return np.vectorize(int_to_datetime_date_python, otypes=[object])(ia)


@box(DatetimeDateArrayType)
def box_datetime_date_array(typ, val, c):
    qvii__thhk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ucum__dmpv = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, qvii__thhk.data)
    wzz__ctm = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, qvii__thhk.null_bitmap).data
    n = c.builder.extract_value(ucum__dmpv.shape, 0)
    sbdq__pbgjs = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer()])
    kpt__agh = cgutils.get_or_insert_function(c.builder.module, sbdq__pbgjs,
        name='box_datetime_date_array')
    whgk__rcut = c.builder.call(kpt__agh, [n, ucum__dmpv.data, wzz__ctm])
    c.context.nrt.decref(c.builder, typ, val)
    return whgk__rcut


@intrinsic
def init_datetime_date_array(typingctx, data, nulls=None):
    assert data == types.Array(types.int64, 1, 'C') or data == types.Array(
        types.NPDatetime('ns'), 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        dlfci__meg, ecbpg__xtbv = args
        cvkuo__gfya = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        cvkuo__gfya.data = dlfci__meg
        cvkuo__gfya.null_bitmap = ecbpg__xtbv
        context.nrt.incref(builder, signature.args[0], dlfci__meg)
        context.nrt.incref(builder, signature.args[1], ecbpg__xtbv)
        return cvkuo__gfya._getvalue()
    sig = datetime_date_array_type(data, nulls)
    return sig, codegen


@lower_constant(DatetimeDateArrayType)
def lower_constant_datetime_date_arr(context, builder, typ, pyval):
    n = len(pyval)
    etaha__xxim = (1970 << 32) + (1 << 16) + 1
    ucum__dmpv = np.full(n, etaha__xxim, np.int64)
    wdxke__dwd = np.empty(n + 7 >> 3, np.uint8)
    for juyj__ypk, why__ugcv in enumerate(pyval):
        msj__mzp = pd.isna(why__ugcv)
        bodo.libs.int_arr_ext.set_bit_to_arr(wdxke__dwd, juyj__ypk, int(not
            msj__mzp))
        if not msj__mzp:
            ucum__dmpv[juyj__ypk] = (why__ugcv.year << 32) + (why__ugcv.
                month << 16) + why__ugcv.day
    pmvbp__euqul = context.get_constant_generic(builder, data_type, ucum__dmpv)
    kopot__ecbo = context.get_constant_generic(builder, nulls_type, wdxke__dwd)
    return lir.Constant.literal_struct([pmvbp__euqul, kopot__ecbo])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_date_array(n):
    ucum__dmpv = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_date_array(ucum__dmpv, nulls)


def alloc_datetime_date_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_date_ext_alloc_datetime_date_array
    ) = alloc_datetime_date_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_date_arr_getitem(A, ind):
    if A != datetime_date_array_type:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_datetime_date(A._data[ind])
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            rdqjr__ihb, jyr__vnovl = array_getitem_bool_index(A, ind)
            return init_datetime_date_array(rdqjr__ihb, jyr__vnovl)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            rdqjr__ihb, jyr__vnovl = array_getitem_int_index(A, ind)
            return init_datetime_date_array(rdqjr__ihb, jyr__vnovl)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            rdqjr__ihb, jyr__vnovl = array_getitem_slice_index(A, ind)
            return init_datetime_date_array(rdqjr__ihb, jyr__vnovl)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeDateArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_date_arr_setitem(A, idx, val):
    if A != datetime_date_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    mftd__mfk = (
        f"setitem for DatetimeDateArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == datetime_date_type:

            def impl(A, idx, val):
                A._data[idx] = cast_datetime_date_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(mftd__mfk)
    if not (is_iterable_type(val) and val.dtype == bodo.datetime_date_type or
        types.unliteral(val) == datetime_date_type):
        raise BodoError(mftd__mfk)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeDateArray with indexing type {idx} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_date_arr(A):
    if A == datetime_date_array_type:
        return lambda A: len(A._data)


@overload_attribute(DatetimeDateArrayType, 'shape')
def overload_datetime_date_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeDateArrayType, 'nbytes')
def datetime_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_date_cmp(lhs, rhs):
        if lhs == datetime_date_type and rhs == datetime_date_type:

            def impl(lhs, rhs):
                y, ihcg__xjcs = lhs.year, rhs.year
                gab__auw, ymmv__qwba = lhs.month, rhs.month
                d, ubob__tbsq = lhs.day, rhs.day
                return op(_cmp((y, gab__auw, d), (ihcg__xjcs, ymmv__qwba,
                    ubob__tbsq)), 0)
            return impl
    return overload_date_cmp


def create_datetime_date_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        dpe__gel = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[op]} {rhs} is always {op == operator.ne} in Python. If this is unexpected there may be a bug in your code.'
            )
        warnings.warn(dpe__gel, bodo.utils.typing.BodoWarning)
        if op == operator.eq:
            return lambda lhs, rhs: False
        elif op == operator.ne:
            return lambda lhs, rhs: True
    return overload_cmp


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            aggc__qquii = True
        else:
            aggc__qquii = False
        if lhs == datetime_date_array_type and rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                evt__bnk = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for juyj__ypk in numba.parfors.parfor.internal_prange(n):
                    ygq__pvh = bodo.libs.array_kernels.isna(lhs, juyj__ypk)
                    ywkpz__uot = bodo.libs.array_kernels.isna(rhs, juyj__ypk)
                    if ygq__pvh or ywkpz__uot:
                        ternm__xrzyv = aggc__qquii
                    else:
                        ternm__xrzyv = op(lhs[juyj__ypk], rhs[juyj__ypk])
                    evt__bnk[juyj__ypk] = ternm__xrzyv
                return evt__bnk
            return impl
        elif lhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                evt__bnk = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for juyj__ypk in numba.parfors.parfor.internal_prange(n):
                    aljr__bwyfl = bodo.libs.array_kernels.isna(lhs, juyj__ypk)
                    if aljr__bwyfl:
                        ternm__xrzyv = aggc__qquii
                    else:
                        ternm__xrzyv = op(lhs[juyj__ypk], rhs)
                    evt__bnk[juyj__ypk] = ternm__xrzyv
                return evt__bnk
            return impl
        elif rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                evt__bnk = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for juyj__ypk in numba.parfors.parfor.internal_prange(n):
                    aljr__bwyfl = bodo.libs.array_kernels.isna(rhs, juyj__ypk)
                    if aljr__bwyfl:
                        ternm__xrzyv = aggc__qquii
                    else:
                        ternm__xrzyv = op(lhs, rhs[juyj__ypk])
                    evt__bnk[juyj__ypk] = ternm__xrzyv
                return evt__bnk
            return impl
    return overload_date_arr_cmp
