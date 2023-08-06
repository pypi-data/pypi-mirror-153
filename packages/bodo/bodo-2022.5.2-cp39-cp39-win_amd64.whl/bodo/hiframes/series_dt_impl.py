"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        zzn__dlltv = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(zzn__dlltv)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fomgt__yfb = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, fomgt__yfb)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        mehvg__qgmn, = args
        srcf__yypp = signature.return_type
        uvn__xxno = cgutils.create_struct_proxy(srcf__yypp)(context, builder)
        uvn__xxno.obj = mehvg__qgmn
        context.nrt.incref(builder, signature.args[0], mehvg__qgmn)
        return uvn__xxno._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{field}')
        vhg__ztwp = 'def impl(S_dt):\n'
        vhg__ztwp += '    S = S_dt._obj\n'
        vhg__ztwp += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        vhg__ztwp += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        vhg__ztwp += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        vhg__ztwp += '    numba.parfors.parfor.init_prange()\n'
        vhg__ztwp += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            vhg__ztwp += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            vhg__ztwp += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        vhg__ztwp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        vhg__ztwp += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        vhg__ztwp += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        vhg__ztwp += '            continue\n'
        vhg__ztwp += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            vhg__ztwp += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                vhg__ztwp += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            vhg__ztwp += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            rubgg__tvpri = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            vhg__ztwp += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            vhg__ztwp += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            vhg__ztwp += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(rubgg__tvpri[field]))
        elif field == 'is_leap_year':
            vhg__ztwp += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            vhg__ztwp += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)\n'
                )
        elif field in ('daysinmonth', 'days_in_month'):
            rubgg__tvpri = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            vhg__ztwp += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            vhg__ztwp += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            vhg__ztwp += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(rubgg__tvpri[field]))
        else:
            vhg__ztwp += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            vhg__ztwp += '        out_arr[i] = ts.' + field + '\n'
        vhg__ztwp += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        mwxbh__ftdmb = {}
        exec(vhg__ztwp, {'bodo': bodo, 'numba': numba, 'np': np}, mwxbh__ftdmb)
        impl = mwxbh__ftdmb['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        wofz__elol = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(wofz__elol)


_install_date_fields()


def create_date_method_overload(method):
    pcheg__tsp = method in ['day_name', 'month_name']
    if pcheg__tsp:
        vhg__ztwp = 'def overload_method(S_dt, locale=None):\n'
        vhg__ztwp += '    unsupported_args = dict(locale=locale)\n'
        vhg__ztwp += '    arg_defaults = dict(locale=None)\n'
        vhg__ztwp += '    bodo.utils.typing.check_unsupported_args(\n'
        vhg__ztwp += f"        'Series.dt.{method}',\n"
        vhg__ztwp += '        unsupported_args,\n'
        vhg__ztwp += '        arg_defaults,\n'
        vhg__ztwp += "        package_name='pandas',\n"
        vhg__ztwp += "        module_name='Series',\n"
        vhg__ztwp += '    )\n'
    else:
        vhg__ztwp = 'def overload_method(S_dt):\n'
        vhg__ztwp += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    vhg__ztwp += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    vhg__ztwp += '        return\n'
    if pcheg__tsp:
        vhg__ztwp += '    def impl(S_dt, locale=None):\n'
    else:
        vhg__ztwp += '    def impl(S_dt):\n'
    vhg__ztwp += '        S = S_dt._obj\n'
    vhg__ztwp += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    vhg__ztwp += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    vhg__ztwp += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    vhg__ztwp += '        numba.parfors.parfor.init_prange()\n'
    vhg__ztwp += '        n = len(arr)\n'
    if pcheg__tsp:
        vhg__ztwp += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        vhg__ztwp += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    vhg__ztwp += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    vhg__ztwp += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    vhg__ztwp += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    vhg__ztwp += '                continue\n'
    vhg__ztwp += '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n'
    vhg__ztwp += f'            method_val = ts.{method}()\n'
    if pcheg__tsp:
        vhg__ztwp += '            out_arr[i] = method_val\n'
    else:
        vhg__ztwp += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    vhg__ztwp += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    vhg__ztwp += '    return impl\n'
    mwxbh__ftdmb = {}
    exec(vhg__ztwp, {'bodo': bodo, 'numba': numba, 'np': np}, mwxbh__ftdmb)
    overload_method = mwxbh__ftdmb['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        wofz__elol = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            wofz__elol)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        gdju__uahv = S_dt._obj
        dsqyg__flq = bodo.hiframes.pd_series_ext.get_series_data(gdju__uahv)
        ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(gdju__uahv)
        zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(gdju__uahv)
        numba.parfors.parfor.init_prange()
        lxoj__rxp = len(dsqyg__flq)
        fmrwa__vfqy = (bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(lxoj__rxp))
        for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp):
            gkfru__cquow = dsqyg__flq[oov__hspg]
            emub__fll = bodo.utils.conversion.box_if_dt64(gkfru__cquow)
            fmrwa__vfqy[oov__hspg] = datetime.date(emub__fll.year,
                emub__fll.month, emub__fll.day)
        return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
            ovpy__hfjy, zzn__dlltv)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{attr}')
        if attr == 'components':
            okba__pdt = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            uigei__abnpm = 'convert_numpy_timedelta64_to_pd_timedelta'
            cqh__dpvok = 'np.empty(n, np.int64)'
            mqff__osgl = attr
        elif attr == 'isocalendar':
            okba__pdt = ['year', 'week', 'day']
            uigei__abnpm = 'convert_datetime64_to_timestamp'
            cqh__dpvok = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            mqff__osgl = attr + '()'
        vhg__ztwp = 'def impl(S_dt):\n'
        vhg__ztwp += '    S = S_dt._obj\n'
        vhg__ztwp += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        vhg__ztwp += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        vhg__ztwp += '    numba.parfors.parfor.init_prange()\n'
        vhg__ztwp += '    n = len(arr)\n'
        for field in okba__pdt:
            vhg__ztwp += '    {} = {}\n'.format(field, cqh__dpvok)
        vhg__ztwp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        vhg__ztwp += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in okba__pdt:
            vhg__ztwp += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        vhg__ztwp += '            continue\n'
        mosf__hpt = '(' + '[i], '.join(okba__pdt) + '[i])'
        vhg__ztwp += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(mosf__hpt, uigei__abnpm, mqff__osgl))
        zkm__fbysv = '(' + ', '.join(okba__pdt) + ')'
        vzo__nwywb = "('" + "', '".join(okba__pdt) + "')"
        vhg__ztwp += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(zkm__fbysv, vzo__nwywb))
        mwxbh__ftdmb = {}
        exec(vhg__ztwp, {'bodo': bodo, 'numba': numba, 'np': np}, mwxbh__ftdmb)
        impl = mwxbh__ftdmb['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    zjicm__rzm = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, hgna__fhwg in zjicm__rzm:
        wofz__elol = create_series_dt_df_output_overload(attr)
        hgna__fhwg(SeriesDatetimePropertiesType, attr, inline='always')(
            wofz__elol)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        vhg__ztwp = 'def impl(S_dt):\n'
        vhg__ztwp += '    S = S_dt._obj\n'
        vhg__ztwp += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        vhg__ztwp += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        vhg__ztwp += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        vhg__ztwp += '    numba.parfors.parfor.init_prange()\n'
        vhg__ztwp += '    n = len(A)\n'
        vhg__ztwp += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        vhg__ztwp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        vhg__ztwp += '        if bodo.libs.array_kernels.isna(A, i):\n'
        vhg__ztwp += '            bodo.libs.array_kernels.setna(B, i)\n'
        vhg__ztwp += '            continue\n'
        vhg__ztwp += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if field == 'nanoseconds':
            vhg__ztwp += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            vhg__ztwp += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            vhg__ztwp += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            vhg__ztwp += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        vhg__ztwp += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        mwxbh__ftdmb = {}
        exec(vhg__ztwp, {'numba': numba, 'np': np, 'bodo': bodo}, mwxbh__ftdmb)
        impl = mwxbh__ftdmb['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        vhg__ztwp = 'def impl(S_dt):\n'
        vhg__ztwp += '    S = S_dt._obj\n'
        vhg__ztwp += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        vhg__ztwp += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        vhg__ztwp += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        vhg__ztwp += '    numba.parfors.parfor.init_prange()\n'
        vhg__ztwp += '    n = len(A)\n'
        if method == 'total_seconds':
            vhg__ztwp += '    B = np.empty(n, np.float64)\n'
        else:
            vhg__ztwp += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        vhg__ztwp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        vhg__ztwp += '        if bodo.libs.array_kernels.isna(A, i):\n'
        vhg__ztwp += '            bodo.libs.array_kernels.setna(B, i)\n'
        vhg__ztwp += '            continue\n'
        vhg__ztwp += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if method == 'total_seconds':
            vhg__ztwp += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            vhg__ztwp += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            vhg__ztwp += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            vhg__ztwp += '    return B\n'
        mwxbh__ftdmb = {}
        exec(vhg__ztwp, {'numba': numba, 'np': np, 'bodo': bodo, 'datetime':
            datetime}, mwxbh__ftdmb)
        impl = mwxbh__ftdmb['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        wofz__elol = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(wofz__elol)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        wofz__elol = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            wofz__elol)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        gdju__uahv = S_dt._obj
        bxrmx__bsl = bodo.hiframes.pd_series_ext.get_series_data(gdju__uahv)
        ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(gdju__uahv)
        zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(gdju__uahv)
        numba.parfors.parfor.init_prange()
        lxoj__rxp = len(bxrmx__bsl)
        nxpq__dfq = bodo.libs.str_arr_ext.pre_alloc_string_array(lxoj__rxp, -1)
        for irc__swyf in numba.parfors.parfor.internal_prange(lxoj__rxp):
            if bodo.libs.array_kernels.isna(bxrmx__bsl, irc__swyf):
                bodo.libs.array_kernels.setna(nxpq__dfq, irc__swyf)
                continue
            nxpq__dfq[irc__swyf] = bodo.utils.conversion.box_if_dt64(bxrmx__bsl
                [irc__swyf]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(nxpq__dfq,
            ovpy__hfjy, zzn__dlltv)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        gdju__uahv = S_dt._obj
        cqm__yber = get_series_data(gdju__uahv).tz_convert(tz)
        ovpy__hfjy = get_series_index(gdju__uahv)
        zzn__dlltv = get_series_name(gdju__uahv)
        return init_series(cqm__yber, ovpy__hfjy, zzn__dlltv)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{method}()')
        jroar__bpub = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        ebts__ybr = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', jroar__bpub,
            ebts__ybr, package_name='pandas', module_name='Series')
        vhg__ztwp = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        vhg__ztwp += '    S = S_dt._obj\n'
        vhg__ztwp += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        vhg__ztwp += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        vhg__ztwp += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        vhg__ztwp += '    numba.parfors.parfor.init_prange()\n'
        vhg__ztwp += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            vhg__ztwp += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            vhg__ztwp += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        vhg__ztwp += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        vhg__ztwp += '        if bodo.libs.array_kernels.isna(A, i):\n'
        vhg__ztwp += '            bodo.libs.array_kernels.setna(B, i)\n'
        vhg__ztwp += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            tfy__nwc = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            itc__tjnul = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            tfy__nwc = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            itc__tjnul = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        vhg__ztwp += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            itc__tjnul, tfy__nwc, method)
        vhg__ztwp += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        mwxbh__ftdmb = {}
        exec(vhg__ztwp, {'numba': numba, 'np': np, 'bodo': bodo}, mwxbh__ftdmb)
        impl = mwxbh__ftdmb['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    ksd__lqzl = ['ceil', 'floor', 'round']
    for method in ksd__lqzl:
        wofz__elol = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            wofz__elol)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                thdo__yyjpk = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                kssqf__jbvtr = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    thdo__yyjpk)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vpbr__vyy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                fhv__wts = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vpbr__vyy)
                lxoj__rxp = len(kssqf__jbvtr)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    wim__wngj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        kssqf__jbvtr[oov__hspg])
                    maw__flv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        fhv__wts[oov__hspg])
                    if wim__wngj == cuww__mkgv or maw__flv == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(wim__wngj, maw__flv)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                fhv__wts = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, dt64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    feo__jihre = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(fhv__wts[oov__hspg]))
                    if iqc__ytj == cuww__mkgv or feo__jihre == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(iqc__ytj, feo__jihre)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                fhv__wts = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, dt64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    feo__jihre = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(fhv__wts[oov__hspg]))
                    if iqc__ytj == cuww__mkgv or feo__jihre == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(iqc__ytj, feo__jihre)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                gyexv__fea = rhs.value
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    if iqc__ytj == cuww__mkgv or gyexv__fea == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(iqc__ytj, gyexv__fea)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                gyexv__fea = lhs.value
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    if gyexv__fea == cuww__mkgv or iqc__ytj == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(gyexv__fea, iqc__ytj)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, dt64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                mpbv__evdo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                feo__jihre = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mpbv__evdo))
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    if iqc__ytj == cuww__mkgv or feo__jihre == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(iqc__ytj, feo__jihre)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, dt64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                mpbv__evdo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                feo__jihre = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mpbv__evdo))
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    if iqc__ytj == cuww__mkgv or feo__jihre == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(iqc__ytj, feo__jihre)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                sfi__frr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    sfi__frr)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    dsxk__aedno = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(dsqyg__flq[oov__hspg]))
                    if dsxk__aedno == cuww__mkgv or iqc__ytj == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(dsxk__aedno, iqc__ytj)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                sfi__frr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                iqc__ytj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    sfi__frr)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    dsxk__aedno = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(dsqyg__flq[oov__hspg]))
                    if iqc__ytj == cuww__mkgv or dsxk__aedno == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(iqc__ytj, dsxk__aedno)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bfvw__oerds = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dsqyg__flq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bfvw__oerds))
                mpbv__evdo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                feo__jihre = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mpbv__evdo))
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    inghq__kxp = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(dsqyg__flq[oov__hspg]))
                    if feo__jihre == cuww__mkgv or inghq__kxp == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(inghq__kxp, feo__jihre)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bfvw__oerds = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dsqyg__flq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lxoj__rxp = len(dsqyg__flq)
                gdju__uahv = np.empty(lxoj__rxp, timedelta64_dtype)
                cuww__mkgv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bfvw__oerds))
                mpbv__evdo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                feo__jihre = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mpbv__evdo))
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    inghq__kxp = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(dsqyg__flq[oov__hspg]))
                    if feo__jihre == cuww__mkgv or inghq__kxp == cuww__mkgv:
                        qxgl__tymio = cuww__mkgv
                    else:
                        qxgl__tymio = op(feo__jihre, inghq__kxp)
                    gdju__uahv[oov__hspg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qxgl__tymio)
                return bodo.hiframes.pd_series_ext.init_series(gdju__uahv,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            xcnc__qim = True
        else:
            xcnc__qim = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bfvw__oerds = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dsqyg__flq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lxoj__rxp = len(dsqyg__flq)
                fmrwa__vfqy = bodo.libs.bool_arr_ext.alloc_bool_array(lxoj__rxp
                    )
                cuww__mkgv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bfvw__oerds))
                qxc__bow = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jnbhz__jgbl = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qxc__bow))
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    admz__hzlrm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(dsqyg__flq[oov__hspg]))
                    if admz__hzlrm == cuww__mkgv or jnbhz__jgbl == cuww__mkgv:
                        qxgl__tymio = xcnc__qim
                    else:
                        qxgl__tymio = op(admz__hzlrm, jnbhz__jgbl)
                    fmrwa__vfqy[oov__hspg] = qxgl__tymio
                return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bfvw__oerds = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dsqyg__flq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lxoj__rxp = len(dsqyg__flq)
                fmrwa__vfqy = bodo.libs.bool_arr_ext.alloc_bool_array(lxoj__rxp
                    )
                cuww__mkgv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bfvw__oerds))
                xmd__ikd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                admz__hzlrm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xmd__ikd))
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    jnbhz__jgbl = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(dsqyg__flq[oov__hspg]))
                    if admz__hzlrm == cuww__mkgv or jnbhz__jgbl == cuww__mkgv:
                        qxgl__tymio = xcnc__qim
                    else:
                        qxgl__tymio = op(admz__hzlrm, jnbhz__jgbl)
                    fmrwa__vfqy[oov__hspg] = qxgl__tymio
                return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lxoj__rxp = len(dsqyg__flq)
                fmrwa__vfqy = bodo.libs.bool_arr_ext.alloc_bool_array(lxoj__rxp
                    )
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    admz__hzlrm = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(dsqyg__flq[oov__hspg]))
                    if admz__hzlrm == cuww__mkgv or rhs.value == cuww__mkgv:
                        qxgl__tymio = xcnc__qim
                    else:
                        qxgl__tymio = op(admz__hzlrm, rhs.value)
                    fmrwa__vfqy[oov__hspg] = qxgl__tymio
                return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lxoj__rxp = len(dsqyg__flq)
                fmrwa__vfqy = bodo.libs.bool_arr_ext.alloc_bool_array(lxoj__rxp
                    )
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    jnbhz__jgbl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(dsqyg__flq[oov__hspg]))
                    if jnbhz__jgbl == cuww__mkgv or lhs.value == cuww__mkgv:
                        qxgl__tymio = xcnc__qim
                    else:
                        qxgl__tymio = op(lhs.value, jnbhz__jgbl)
                    fmrwa__vfqy[oov__hspg] = qxgl__tymio
                return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                lxoj__rxp = len(dsqyg__flq)
                fmrwa__vfqy = bodo.libs.bool_arr_ext.alloc_bool_array(lxoj__rxp
                    )
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                kaab__cwxw = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                hum__bhsaf = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    kaab__cwxw)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    admz__hzlrm = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(dsqyg__flq[oov__hspg]))
                    if admz__hzlrm == cuww__mkgv or hum__bhsaf == cuww__mkgv:
                        qxgl__tymio = xcnc__qim
                    else:
                        qxgl__tymio = op(admz__hzlrm, hum__bhsaf)
                    fmrwa__vfqy[oov__hspg] = qxgl__tymio
                return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            bfvw__oerds = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                ndffz__wdt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                dsqyg__flq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ndffz__wdt)
                ovpy__hfjy = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zzn__dlltv = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                lxoj__rxp = len(dsqyg__flq)
                fmrwa__vfqy = bodo.libs.bool_arr_ext.alloc_bool_array(lxoj__rxp
                    )
                cuww__mkgv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bfvw__oerds)
                kaab__cwxw = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                hum__bhsaf = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    kaab__cwxw)
                for oov__hspg in numba.parfors.parfor.internal_prange(lxoj__rxp
                    ):
                    sfi__frr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dsqyg__flq[oov__hspg])
                    if sfi__frr == cuww__mkgv or hum__bhsaf == cuww__mkgv:
                        qxgl__tymio = xcnc__qim
                    else:
                        qxgl__tymio = op(hum__bhsaf, sfi__frr)
                    fmrwa__vfqy[oov__hspg] = qxgl__tymio
                return bodo.hiframes.pd_series_ext.init_series(fmrwa__vfqy,
                    ovpy__hfjy, zzn__dlltv)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for lgisc__hcq in series_dt_unsupported_attrs:
        thgq__zggo = 'Series.dt.' + lgisc__hcq
        overload_attribute(SeriesDatetimePropertiesType, lgisc__hcq)(
            create_unsupported_overload(thgq__zggo))
    for qbh__wuq in series_dt_unsupported_methods:
        thgq__zggo = 'Series.dt.' + qbh__wuq
        overload_method(SeriesDatetimePropertiesType, qbh__wuq,
            no_unliteral=True)(create_unsupported_overload(thgq__zggo))


_install_series_dt_unsupported()
