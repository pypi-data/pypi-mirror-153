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
        hbhs__tphob = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(hbhs__tphob)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ftss__dvna = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, ftss__dvna)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        feop__vnc, = args
        sdaxi__axd = signature.return_type
        hly__perc = cgutils.create_struct_proxy(sdaxi__axd)(context, builder)
        hly__perc.obj = feop__vnc
        context.nrt.incref(builder, signature.args[0], feop__vnc)
        return hly__perc._getvalue()
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
        xrebo__lietg = 'def impl(S_dt):\n'
        xrebo__lietg += '    S = S_dt._obj\n'
        xrebo__lietg += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xrebo__lietg += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xrebo__lietg += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xrebo__lietg += '    numba.parfors.parfor.init_prange()\n'
        xrebo__lietg += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            xrebo__lietg += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            xrebo__lietg += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        xrebo__lietg += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        xrebo__lietg += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        xrebo__lietg += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        xrebo__lietg += '            continue\n'
        xrebo__lietg += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            xrebo__lietg += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                xrebo__lietg += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            xrebo__lietg += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            axyba__ero = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            xrebo__lietg += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            xrebo__lietg += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            xrebo__lietg += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(axyba__ero[field]))
        elif field == 'is_leap_year':
            xrebo__lietg += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            xrebo__lietg += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            axyba__ero = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            xrebo__lietg += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            xrebo__lietg += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            xrebo__lietg += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(axyba__ero[field]))
        else:
            xrebo__lietg += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            xrebo__lietg += '        out_arr[i] = ts.' + field + '\n'
        xrebo__lietg += """    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
        zdr__wbi = {}
        exec(xrebo__lietg, {'bodo': bodo, 'numba': numba, 'np': np}, zdr__wbi)
        impl = zdr__wbi['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        xohi__diw = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(xohi__diw)


_install_date_fields()


def create_date_method_overload(method):
    swf__vptzq = method in ['day_name', 'month_name']
    if swf__vptzq:
        xrebo__lietg = 'def overload_method(S_dt, locale=None):\n'
        xrebo__lietg += '    unsupported_args = dict(locale=locale)\n'
        xrebo__lietg += '    arg_defaults = dict(locale=None)\n'
        xrebo__lietg += '    bodo.utils.typing.check_unsupported_args(\n'
        xrebo__lietg += f"        'Series.dt.{method}',\n"
        xrebo__lietg += '        unsupported_args,\n'
        xrebo__lietg += '        arg_defaults,\n'
        xrebo__lietg += "        package_name='pandas',\n"
        xrebo__lietg += "        module_name='Series',\n"
        xrebo__lietg += '    )\n'
    else:
        xrebo__lietg = 'def overload_method(S_dt):\n'
        xrebo__lietg += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    xrebo__lietg += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    xrebo__lietg += '        return\n'
    if swf__vptzq:
        xrebo__lietg += '    def impl(S_dt, locale=None):\n'
    else:
        xrebo__lietg += '    def impl(S_dt):\n'
    xrebo__lietg += '        S = S_dt._obj\n'
    xrebo__lietg += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    xrebo__lietg += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    xrebo__lietg += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    xrebo__lietg += '        numba.parfors.parfor.init_prange()\n'
    xrebo__lietg += '        n = len(arr)\n'
    if swf__vptzq:
        xrebo__lietg += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        xrebo__lietg += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    xrebo__lietg += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    xrebo__lietg += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    xrebo__lietg += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    xrebo__lietg += '                continue\n'
    xrebo__lietg += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    xrebo__lietg += f'            method_val = ts.{method}()\n'
    if swf__vptzq:
        xrebo__lietg += '            out_arr[i] = method_val\n'
    else:
        xrebo__lietg += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    xrebo__lietg += """        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    xrebo__lietg += '    return impl\n'
    zdr__wbi = {}
    exec(xrebo__lietg, {'bodo': bodo, 'numba': numba, 'np': np}, zdr__wbi)
    overload_method = zdr__wbi['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        xohi__diw = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            xohi__diw)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        wvxde__xtp = S_dt._obj
        pxvjf__vmov = bodo.hiframes.pd_series_ext.get_series_data(wvxde__xtp)
        pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(wvxde__xtp)
        hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(wvxde__xtp)
        numba.parfors.parfor.init_prange()
        cbm__rpirb = len(pxvjf__vmov)
        miq__dxn = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            cbm__rpirb)
        for rfuh__ooe in numba.parfors.parfor.internal_prange(cbm__rpirb):
            cqj__aujy = pxvjf__vmov[rfuh__ooe]
            kxwty__xdhkm = bodo.utils.conversion.box_if_dt64(cqj__aujy)
            miq__dxn[rfuh__ooe] = datetime.date(kxwty__xdhkm.year,
                kxwty__xdhkm.month, kxwty__xdhkm.day)
        return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
            pfyyd__tishl, hbhs__tphob)
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
            itt__upoli = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            clffg__odk = 'convert_numpy_timedelta64_to_pd_timedelta'
            koa__cibks = 'np.empty(n, np.int64)'
            xkeat__gdpig = attr
        elif attr == 'isocalendar':
            itt__upoli = ['year', 'week', 'day']
            clffg__odk = 'convert_datetime64_to_timestamp'
            koa__cibks = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            xkeat__gdpig = attr + '()'
        xrebo__lietg = 'def impl(S_dt):\n'
        xrebo__lietg += '    S = S_dt._obj\n'
        xrebo__lietg += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xrebo__lietg += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xrebo__lietg += '    numba.parfors.parfor.init_prange()\n'
        xrebo__lietg += '    n = len(arr)\n'
        for field in itt__upoli:
            xrebo__lietg += '    {} = {}\n'.format(field, koa__cibks)
        xrebo__lietg += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        xrebo__lietg += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in itt__upoli:
            xrebo__lietg += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        xrebo__lietg += '            continue\n'
        nmqtc__tflf = '(' + '[i], '.join(itt__upoli) + '[i])'
        xrebo__lietg += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(nmqtc__tflf, clffg__odk, xkeat__gdpig))
        fxya__qdb = '(' + ', '.join(itt__upoli) + ')'
        tyx__fcc = "('" + "', '".join(itt__upoli) + "')"
        xrebo__lietg += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(fxya__qdb, tyx__fcc))
        zdr__wbi = {}
        exec(xrebo__lietg, {'bodo': bodo, 'numba': numba, 'np': np}, zdr__wbi)
        impl = zdr__wbi['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    jjj__llkpr = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, iaql__nygce in jjj__llkpr:
        xohi__diw = create_series_dt_df_output_overload(attr)
        iaql__nygce(SeriesDatetimePropertiesType, attr, inline='always')(
            xohi__diw)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        xrebo__lietg = 'def impl(S_dt):\n'
        xrebo__lietg += '    S = S_dt._obj\n'
        xrebo__lietg += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xrebo__lietg += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xrebo__lietg += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xrebo__lietg += '    numba.parfors.parfor.init_prange()\n'
        xrebo__lietg += '    n = len(A)\n'
        xrebo__lietg += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        xrebo__lietg += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        xrebo__lietg += '        if bodo.libs.array_kernels.isna(A, i):\n'
        xrebo__lietg += '            bodo.libs.array_kernels.setna(B, i)\n'
        xrebo__lietg += '            continue\n'
        xrebo__lietg += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            xrebo__lietg += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            xrebo__lietg += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            xrebo__lietg += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            xrebo__lietg += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        xrebo__lietg += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        zdr__wbi = {}
        exec(xrebo__lietg, {'numba': numba, 'np': np, 'bodo': bodo}, zdr__wbi)
        impl = zdr__wbi['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        xrebo__lietg = 'def impl(S_dt):\n'
        xrebo__lietg += '    S = S_dt._obj\n'
        xrebo__lietg += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xrebo__lietg += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xrebo__lietg += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xrebo__lietg += '    numba.parfors.parfor.init_prange()\n'
        xrebo__lietg += '    n = len(A)\n'
        if method == 'total_seconds':
            xrebo__lietg += '    B = np.empty(n, np.float64)\n'
        else:
            xrebo__lietg += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        xrebo__lietg += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        xrebo__lietg += '        if bodo.libs.array_kernels.isna(A, i):\n'
        xrebo__lietg += '            bodo.libs.array_kernels.setna(B, i)\n'
        xrebo__lietg += '            continue\n'
        xrebo__lietg += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            xrebo__lietg += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            xrebo__lietg += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            xrebo__lietg += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            xrebo__lietg += '    return B\n'
        zdr__wbi = {}
        exec(xrebo__lietg, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, zdr__wbi)
        impl = zdr__wbi['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        xohi__diw = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(xohi__diw)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        xohi__diw = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            xohi__diw)


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
        wvxde__xtp = S_dt._obj
        nhp__nbulp = bodo.hiframes.pd_series_ext.get_series_data(wvxde__xtp)
        pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(wvxde__xtp)
        hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(wvxde__xtp)
        numba.parfors.parfor.init_prange()
        cbm__rpirb = len(nhp__nbulp)
        nmk__glibs = bodo.libs.str_arr_ext.pre_alloc_string_array(cbm__rpirb,
            -1)
        for cjq__ija in numba.parfors.parfor.internal_prange(cbm__rpirb):
            if bodo.libs.array_kernels.isna(nhp__nbulp, cjq__ija):
                bodo.libs.array_kernels.setna(nmk__glibs, cjq__ija)
                continue
            nmk__glibs[cjq__ija] = bodo.utils.conversion.box_if_dt64(nhp__nbulp
                [cjq__ija]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(nmk__glibs,
            pfyyd__tishl, hbhs__tphob)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        wvxde__xtp = S_dt._obj
        nvbs__hobtg = get_series_data(wvxde__xtp).tz_convert(tz)
        pfyyd__tishl = get_series_index(wvxde__xtp)
        hbhs__tphob = get_series_name(wvxde__xtp)
        return init_series(nvbs__hobtg, pfyyd__tishl, hbhs__tphob)
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
        vhtzf__ame = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        tplee__kwif = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', vhtzf__ame,
            tplee__kwif, package_name='pandas', module_name='Series')
        xrebo__lietg = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        xrebo__lietg += '    S = S_dt._obj\n'
        xrebo__lietg += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xrebo__lietg += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xrebo__lietg += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xrebo__lietg += '    numba.parfors.parfor.init_prange()\n'
        xrebo__lietg += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            xrebo__lietg += (
                "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n")
        else:
            xrebo__lietg += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        xrebo__lietg += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        xrebo__lietg += '        if bodo.libs.array_kernels.isna(A, i):\n'
        xrebo__lietg += '            bodo.libs.array_kernels.setna(B, i)\n'
        xrebo__lietg += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            hquvj__ycb = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            bhvv__pmgw = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            hquvj__ycb = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            bhvv__pmgw = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        xrebo__lietg += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            bhvv__pmgw, hquvj__ycb, method)
        xrebo__lietg += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        zdr__wbi = {}
        exec(xrebo__lietg, {'numba': numba, 'np': np, 'bodo': bodo}, zdr__wbi)
        impl = zdr__wbi['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    qcaxz__xfuo = ['ceil', 'floor', 'round']
    for method in qcaxz__xfuo:
        xohi__diw = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            xohi__diw)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dxnk__bjio = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qsn__ubl = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    dxnk__bjio)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                poe__flt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                opxqv__czuy = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    poe__flt)
                cbm__rpirb = len(qsn__ubl)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    obyj__piblz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qsn__ubl[rfuh__ooe]))
                    rraif__xwpf = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(opxqv__czuy[rfuh__ooe]))
                    if (obyj__piblz == jjvyr__hglie or rraif__xwpf ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(obyj__piblz, rraif__xwpf)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                opxqv__czuy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, dt64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    goqq__bwkcl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    trc__vbcb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(opxqv__czuy[rfuh__ooe]))
                    if (goqq__bwkcl == jjvyr__hglie or trc__vbcb ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(goqq__bwkcl, trc__vbcb)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                opxqv__czuy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, dt64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    goqq__bwkcl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    trc__vbcb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(opxqv__czuy[rfuh__ooe]))
                    if (goqq__bwkcl == jjvyr__hglie or trc__vbcb ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(goqq__bwkcl, trc__vbcb)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                tale__ytk = rhs.value
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    goqq__bwkcl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (goqq__bwkcl == jjvyr__hglie or tale__ytk ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(goqq__bwkcl, tale__ytk)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                tale__ytk = lhs.value
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    goqq__bwkcl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (tale__ytk == jjvyr__hglie or goqq__bwkcl ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(tale__ytk, goqq__bwkcl)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, dt64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                dcgnw__farno = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                trc__vbcb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(dcgnw__farno))
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    goqq__bwkcl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (goqq__bwkcl == jjvyr__hglie or trc__vbcb ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(goqq__bwkcl, trc__vbcb)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, dt64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                dcgnw__farno = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                trc__vbcb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(dcgnw__farno))
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    goqq__bwkcl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (goqq__bwkcl == jjvyr__hglie or trc__vbcb ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(goqq__bwkcl, trc__vbcb)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                bewle__qgghv = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                goqq__bwkcl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bewle__qgghv)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xoa__jnq = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        pxvjf__vmov[rfuh__ooe])
                    if xoa__jnq == jjvyr__hglie or goqq__bwkcl == jjvyr__hglie:
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(xoa__jnq, goqq__bwkcl)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                bewle__qgghv = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                goqq__bwkcl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bewle__qgghv)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xoa__jnq = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        pxvjf__vmov[rfuh__ooe])
                    if goqq__bwkcl == jjvyr__hglie or xoa__jnq == jjvyr__hglie:
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(goqq__bwkcl, xoa__jnq)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ypnx__smhxl = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pxvjf__vmov = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ypnx__smhxl))
                dcgnw__farno = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                trc__vbcb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(dcgnw__farno))
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    vwry__josgq = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (trc__vbcb == jjvyr__hglie or vwry__josgq ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(vwry__josgq, trc__vbcb)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ypnx__smhxl = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pxvjf__vmov = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                wvxde__xtp = np.empty(cbm__rpirb, timedelta64_dtype)
                jjvyr__hglie = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ypnx__smhxl))
                dcgnw__farno = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                trc__vbcb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(dcgnw__farno))
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    vwry__josgq = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (trc__vbcb == jjvyr__hglie or vwry__josgq ==
                        jjvyr__hglie):
                        idap__jzoq = jjvyr__hglie
                    else:
                        idap__jzoq = op(trc__vbcb, vwry__josgq)
                    wvxde__xtp[rfuh__ooe
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        idap__jzoq)
                return bodo.hiframes.pd_series_ext.init_series(wvxde__xtp,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            uta__izi = True
        else:
            uta__izi = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ypnx__smhxl = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pxvjf__vmov = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                miq__dxn = bodo.libs.bool_arr_ext.alloc_bool_array(cbm__rpirb)
                jjvyr__hglie = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ypnx__smhxl))
                romuv__tkahb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                xzjpm__rnyhy = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(romuv__tkahb))
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xvrv__srg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (xvrv__srg == jjvyr__hglie or xzjpm__rnyhy ==
                        jjvyr__hglie):
                        idap__jzoq = uta__izi
                    else:
                        idap__jzoq = op(xvrv__srg, xzjpm__rnyhy)
                    miq__dxn[rfuh__ooe] = idap__jzoq
                return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ypnx__smhxl = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pxvjf__vmov = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                miq__dxn = bodo.libs.bool_arr_ext.alloc_bool_array(cbm__rpirb)
                jjvyr__hglie = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ypnx__smhxl))
                xfjmz__iez = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                xvrv__srg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xfjmz__iez))
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xzjpm__rnyhy = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (xvrv__srg == jjvyr__hglie or xzjpm__rnyhy ==
                        jjvyr__hglie):
                        idap__jzoq = uta__izi
                    else:
                        idap__jzoq = op(xvrv__srg, xzjpm__rnyhy)
                    miq__dxn[rfuh__ooe] = idap__jzoq
                return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cbm__rpirb = len(pxvjf__vmov)
                miq__dxn = bodo.libs.bool_arr_ext.alloc_bool_array(cbm__rpirb)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xvrv__srg = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        pxvjf__vmov[rfuh__ooe])
                    if xvrv__srg == jjvyr__hglie or rhs.value == jjvyr__hglie:
                        idap__jzoq = uta__izi
                    else:
                        idap__jzoq = op(xvrv__srg, rhs.value)
                    miq__dxn[rfuh__ooe] = idap__jzoq
                return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cbm__rpirb = len(pxvjf__vmov)
                miq__dxn = bodo.libs.bool_arr_ext.alloc_bool_array(cbm__rpirb)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xzjpm__rnyhy = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (xzjpm__rnyhy == jjvyr__hglie or lhs.value ==
                        jjvyr__hglie):
                        idap__jzoq = uta__izi
                    else:
                        idap__jzoq = op(lhs.value, xzjpm__rnyhy)
                    miq__dxn[rfuh__ooe] = idap__jzoq
                return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                cbm__rpirb = len(pxvjf__vmov)
                miq__dxn = bodo.libs.bool_arr_ext.alloc_bool_array(cbm__rpirb)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                gtrh__jcyev = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(rhs))
                tohw__nvtho = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    gtrh__jcyev)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    xvrv__srg = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        pxvjf__vmov[rfuh__ooe])
                    if (xvrv__srg == jjvyr__hglie or tohw__nvtho ==
                        jjvyr__hglie):
                        idap__jzoq = uta__izi
                    else:
                        idap__jzoq = op(xvrv__srg, tohw__nvtho)
                    miq__dxn[rfuh__ooe] = idap__jzoq
                return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            ypnx__smhxl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                wlic__fffy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pxvjf__vmov = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wlic__fffy)
                pfyyd__tishl = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                hbhs__tphob = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                cbm__rpirb = len(pxvjf__vmov)
                miq__dxn = bodo.libs.bool_arr_ext.alloc_bool_array(cbm__rpirb)
                jjvyr__hglie = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ypnx__smhxl)
                gtrh__jcyev = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(lhs))
                tohw__nvtho = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    gtrh__jcyev)
                for rfuh__ooe in numba.parfors.parfor.internal_prange(
                    cbm__rpirb):
                    bewle__qgghv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pxvjf__vmov[rfuh__ooe]))
                    if (bewle__qgghv == jjvyr__hglie or tohw__nvtho ==
                        jjvyr__hglie):
                        idap__jzoq = uta__izi
                    else:
                        idap__jzoq = op(tohw__nvtho, bewle__qgghv)
                    miq__dxn[rfuh__ooe] = idap__jzoq
                return bodo.hiframes.pd_series_ext.init_series(miq__dxn,
                    pfyyd__tishl, hbhs__tphob)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for trrbc__mif in series_dt_unsupported_attrs:
        inqn__kwr = 'Series.dt.' + trrbc__mif
        overload_attribute(SeriesDatetimePropertiesType, trrbc__mif)(
            create_unsupported_overload(inqn__kwr))
    for nmlx__msg in series_dt_unsupported_methods:
        inqn__kwr = 'Series.dt.' + nmlx__msg
        overload_method(SeriesDatetimePropertiesType, nmlx__msg,
            no_unliteral=True)(create_unsupported_overload(inqn__kwr))


_install_series_dt_unsupported()
