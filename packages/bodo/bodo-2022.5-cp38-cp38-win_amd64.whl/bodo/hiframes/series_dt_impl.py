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
        aafvo__lnkpq = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(aafvo__lnkpq)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        elig__xnsx = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, elig__xnsx)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qoz__slehf, = args
        dwy__bsix = signature.return_type
        eootz__zepqy = cgutils.create_struct_proxy(dwy__bsix)(context, builder)
        eootz__zepqy.obj = qoz__slehf
        context.nrt.incref(builder, signature.args[0], qoz__slehf)
        return eootz__zepqy._getvalue()
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
        ppobj__qvuy = 'def impl(S_dt):\n'
        ppobj__qvuy += '    S = S_dt._obj\n'
        ppobj__qvuy += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ppobj__qvuy += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ppobj__qvuy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ppobj__qvuy += '    numba.parfors.parfor.init_prange()\n'
        ppobj__qvuy += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            ppobj__qvuy += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            ppobj__qvuy += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        ppobj__qvuy += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ppobj__qvuy += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        ppobj__qvuy += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        ppobj__qvuy += '            continue\n'
        ppobj__qvuy += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            ppobj__qvuy += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                ppobj__qvuy += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            ppobj__qvuy += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            rcfb__vuy = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            ppobj__qvuy += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            ppobj__qvuy += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            ppobj__qvuy += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(rcfb__vuy[field]))
        elif field == 'is_leap_year':
            ppobj__qvuy += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            ppobj__qvuy += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            rcfb__vuy = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            ppobj__qvuy += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            ppobj__qvuy += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            ppobj__qvuy += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(rcfb__vuy[field]))
        else:
            ppobj__qvuy += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            ppobj__qvuy += '        out_arr[i] = ts.' + field + '\n'
        ppobj__qvuy += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        aqyue__aifm = {}
        exec(ppobj__qvuy, {'bodo': bodo, 'numba': numba, 'np': np}, aqyue__aifm
            )
        impl = aqyue__aifm['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        gsxa__yapsc = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(gsxa__yapsc)


_install_date_fields()


def create_date_method_overload(method):
    hwtbq__pqk = method in ['day_name', 'month_name']
    if hwtbq__pqk:
        ppobj__qvuy = 'def overload_method(S_dt, locale=None):\n'
        ppobj__qvuy += '    unsupported_args = dict(locale=locale)\n'
        ppobj__qvuy += '    arg_defaults = dict(locale=None)\n'
        ppobj__qvuy += '    bodo.utils.typing.check_unsupported_args(\n'
        ppobj__qvuy += f"        'Series.dt.{method}',\n"
        ppobj__qvuy += '        unsupported_args,\n'
        ppobj__qvuy += '        arg_defaults,\n'
        ppobj__qvuy += "        package_name='pandas',\n"
        ppobj__qvuy += "        module_name='Series',\n"
        ppobj__qvuy += '    )\n'
    else:
        ppobj__qvuy = 'def overload_method(S_dt):\n'
        ppobj__qvuy += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    ppobj__qvuy += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    ppobj__qvuy += '        return\n'
    if hwtbq__pqk:
        ppobj__qvuy += '    def impl(S_dt, locale=None):\n'
    else:
        ppobj__qvuy += '    def impl(S_dt):\n'
    ppobj__qvuy += '        S = S_dt._obj\n'
    ppobj__qvuy += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ppobj__qvuy += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    ppobj__qvuy += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    ppobj__qvuy += '        numba.parfors.parfor.init_prange()\n'
    ppobj__qvuy += '        n = len(arr)\n'
    if hwtbq__pqk:
        ppobj__qvuy += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        ppobj__qvuy += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    ppobj__qvuy += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    ppobj__qvuy += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    ppobj__qvuy += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    ppobj__qvuy += '                continue\n'
    ppobj__qvuy += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    ppobj__qvuy += f'            method_val = ts.{method}()\n'
    if hwtbq__pqk:
        ppobj__qvuy += '            out_arr[i] = method_val\n'
    else:
        ppobj__qvuy += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    ppobj__qvuy += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ppobj__qvuy += '    return impl\n'
    aqyue__aifm = {}
    exec(ppobj__qvuy, {'bodo': bodo, 'numba': numba, 'np': np}, aqyue__aifm)
    overload_method = aqyue__aifm['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        gsxa__yapsc = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            gsxa__yapsc)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        zear__dhbf = S_dt._obj
        sysjc__bdame = bodo.hiframes.pd_series_ext.get_series_data(zear__dhbf)
        tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(zear__dhbf)
        aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(zear__dhbf)
        numba.parfors.parfor.init_prange()
        osgrt__djye = len(sysjc__bdame)
        jjv__dsg = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            osgrt__djye)
        for tjpr__maq in numba.parfors.parfor.internal_prange(osgrt__djye):
            jnvv__ljt = sysjc__bdame[tjpr__maq]
            mhw__rygpk = bodo.utils.conversion.box_if_dt64(jnvv__ljt)
            jjv__dsg[tjpr__maq] = datetime.date(mhw__rygpk.year, mhw__rygpk
                .month, mhw__rygpk.day)
        return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
            tuhkn__sisws, aafvo__lnkpq)
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
            clla__yqv = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            nsh__wbee = 'convert_numpy_timedelta64_to_pd_timedelta'
            jezc__oho = 'np.empty(n, np.int64)'
            gmag__oihyj = attr
        elif attr == 'isocalendar':
            clla__yqv = ['year', 'week', 'day']
            nsh__wbee = 'convert_datetime64_to_timestamp'
            jezc__oho = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            gmag__oihyj = attr + '()'
        ppobj__qvuy = 'def impl(S_dt):\n'
        ppobj__qvuy += '    S = S_dt._obj\n'
        ppobj__qvuy += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ppobj__qvuy += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ppobj__qvuy += '    numba.parfors.parfor.init_prange()\n'
        ppobj__qvuy += '    n = len(arr)\n'
        for field in clla__yqv:
            ppobj__qvuy += '    {} = {}\n'.format(field, jezc__oho)
        ppobj__qvuy += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ppobj__qvuy += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in clla__yqv:
            ppobj__qvuy += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        ppobj__qvuy += '            continue\n'
        zod__zmrya = '(' + '[i], '.join(clla__yqv) + '[i])'
        ppobj__qvuy += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(zod__zmrya, nsh__wbee, gmag__oihyj))
        ogyxc__nthz = '(' + ', '.join(clla__yqv) + ')'
        xbxv__xgvf = "('" + "', '".join(clla__yqv) + "')"
        ppobj__qvuy += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(ogyxc__nthz, xbxv__xgvf))
        aqyue__aifm = {}
        exec(ppobj__qvuy, {'bodo': bodo, 'numba': numba, 'np': np}, aqyue__aifm
            )
        impl = aqyue__aifm['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    njhbv__nkek = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, ckwy__nylmv in njhbv__nkek:
        gsxa__yapsc = create_series_dt_df_output_overload(attr)
        ckwy__nylmv(SeriesDatetimePropertiesType, attr, inline='always')(
            gsxa__yapsc)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        ppobj__qvuy = 'def impl(S_dt):\n'
        ppobj__qvuy += '    S = S_dt._obj\n'
        ppobj__qvuy += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ppobj__qvuy += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ppobj__qvuy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ppobj__qvuy += '    numba.parfors.parfor.init_prange()\n'
        ppobj__qvuy += '    n = len(A)\n'
        ppobj__qvuy += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        ppobj__qvuy += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ppobj__qvuy += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ppobj__qvuy += '            bodo.libs.array_kernels.setna(B, i)\n'
        ppobj__qvuy += '            continue\n'
        ppobj__qvuy += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            ppobj__qvuy += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            ppobj__qvuy += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            ppobj__qvuy += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            ppobj__qvuy += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        ppobj__qvuy += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        aqyue__aifm = {}
        exec(ppobj__qvuy, {'numba': numba, 'np': np, 'bodo': bodo}, aqyue__aifm
            )
        impl = aqyue__aifm['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        ppobj__qvuy = 'def impl(S_dt):\n'
        ppobj__qvuy += '    S = S_dt._obj\n'
        ppobj__qvuy += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ppobj__qvuy += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ppobj__qvuy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ppobj__qvuy += '    numba.parfors.parfor.init_prange()\n'
        ppobj__qvuy += '    n = len(A)\n'
        if method == 'total_seconds':
            ppobj__qvuy += '    B = np.empty(n, np.float64)\n'
        else:
            ppobj__qvuy += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        ppobj__qvuy += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ppobj__qvuy += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ppobj__qvuy += '            bodo.libs.array_kernels.setna(B, i)\n'
        ppobj__qvuy += '            continue\n'
        ppobj__qvuy += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            ppobj__qvuy += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            ppobj__qvuy += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            ppobj__qvuy += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            ppobj__qvuy += '    return B\n'
        aqyue__aifm = {}
        exec(ppobj__qvuy, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, aqyue__aifm)
        impl = aqyue__aifm['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        gsxa__yapsc = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(gsxa__yapsc)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        gsxa__yapsc = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            gsxa__yapsc)


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
        zear__dhbf = S_dt._obj
        wed__whl = bodo.hiframes.pd_series_ext.get_series_data(zear__dhbf)
        tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(zear__dhbf)
        aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(zear__dhbf)
        numba.parfors.parfor.init_prange()
        osgrt__djye = len(wed__whl)
        wku__sgsdp = bodo.libs.str_arr_ext.pre_alloc_string_array(osgrt__djye,
            -1)
        for xhya__wzibz in numba.parfors.parfor.internal_prange(osgrt__djye):
            if bodo.libs.array_kernels.isna(wed__whl, xhya__wzibz):
                bodo.libs.array_kernels.setna(wku__sgsdp, xhya__wzibz)
                continue
            wku__sgsdp[xhya__wzibz] = bodo.utils.conversion.box_if_dt64(
                wed__whl[xhya__wzibz]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(wku__sgsdp,
            tuhkn__sisws, aafvo__lnkpq)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        zear__dhbf = S_dt._obj
        gvs__xymk = get_series_data(zear__dhbf).tz_convert(tz)
        tuhkn__sisws = get_series_index(zear__dhbf)
        aafvo__lnkpq = get_series_name(zear__dhbf)
        return init_series(gvs__xymk, tuhkn__sisws, aafvo__lnkpq)
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
        qtao__wfh = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        cbh__wfexj = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', qtao__wfh, cbh__wfexj,
            package_name='pandas', module_name='Series')
        ppobj__qvuy = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        ppobj__qvuy += '    S = S_dt._obj\n'
        ppobj__qvuy += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ppobj__qvuy += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ppobj__qvuy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ppobj__qvuy += '    numba.parfors.parfor.init_prange()\n'
        ppobj__qvuy += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            ppobj__qvuy += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            ppobj__qvuy += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        ppobj__qvuy += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ppobj__qvuy += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ppobj__qvuy += '            bodo.libs.array_kernels.setna(B, i)\n'
        ppobj__qvuy += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            cab__lnee = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            xpalz__lsx = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            cab__lnee = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            xpalz__lsx = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        ppobj__qvuy += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            xpalz__lsx, cab__lnee, method)
        ppobj__qvuy += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        aqyue__aifm = {}
        exec(ppobj__qvuy, {'numba': numba, 'np': np, 'bodo': bodo}, aqyue__aifm
            )
        impl = aqyue__aifm['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    iyx__dftih = ['ceil', 'floor', 'round']
    for method in iyx__dftih:
        gsxa__yapsc = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            gsxa__yapsc)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tafb__dzpmz = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                bzmpf__zeuoh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tafb__dzpmz)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                jfif__nggp = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vod__jalro = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jfif__nggp)
                osgrt__djye = len(bzmpf__zeuoh)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    yzbj__tzgq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(bzmpf__zeuoh[tjpr__maq]))
                    jigl__hyki = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vod__jalro[tjpr__maq]))
                    if yzbj__tzgq == iywq__lof or jigl__hyki == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(yzbj__tzgq, jigl__hyki)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vod__jalro = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, dt64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    gklwc__swrf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vod__jalro[tjpr__maq]))
                    if bkml__dyo == iywq__lof or gklwc__swrf == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(bkml__dyo, gklwc__swrf)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vod__jalro = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, dt64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    gklwc__swrf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vod__jalro[tjpr__maq]))
                    if bkml__dyo == iywq__lof or gklwc__swrf == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(bkml__dyo, gklwc__swrf)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                nuk__wgh = rhs.value
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    if bkml__dyo == iywq__lof or nuk__wgh == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(bkml__dyo, nuk__wgh)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                nuk__wgh = lhs.value
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    if nuk__wgh == iywq__lof or bkml__dyo == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(nuk__wgh, bkml__dyo)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, dt64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                jqwa__kfpb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                gklwc__swrf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(jqwa__kfpb))
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    if bkml__dyo == iywq__lof or gklwc__swrf == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(bkml__dyo, gklwc__swrf)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, dt64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                jqwa__kfpb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                gklwc__swrf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(jqwa__kfpb))
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    if bkml__dyo == iywq__lof or gklwc__swrf == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(bkml__dyo, gklwc__swrf)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                hgio__ekn = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgio__ekn)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    rvfy__arsj = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(sysjc__bdame[tjpr__maq]))
                    if rvfy__arsj == iywq__lof or bkml__dyo == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(rvfy__arsj, bkml__dyo)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                hgio__ekn = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                bkml__dyo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgio__ekn)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    rvfy__arsj = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(sysjc__bdame[tjpr__maq]))
                    if bkml__dyo == iywq__lof or rvfy__arsj == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(bkml__dyo, rvfy__arsj)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ryue__hchuc = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                sysjc__bdame = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ryue__hchuc))
                jqwa__kfpb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                gklwc__swrf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(jqwa__kfpb))
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    oqqk__lhcx = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(sysjc__bdame[tjpr__maq]))
                    if gklwc__swrf == iywq__lof or oqqk__lhcx == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(oqqk__lhcx, gklwc__swrf)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ryue__hchuc = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                sysjc__bdame = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                osgrt__djye = len(sysjc__bdame)
                zear__dhbf = np.empty(osgrt__djye, timedelta64_dtype)
                iywq__lof = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ryue__hchuc))
                jqwa__kfpb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                gklwc__swrf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(jqwa__kfpb))
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    oqqk__lhcx = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(sysjc__bdame[tjpr__maq]))
                    if gklwc__swrf == iywq__lof or oqqk__lhcx == iywq__lof:
                        xmrjz__kjx = iywq__lof
                    else:
                        xmrjz__kjx = op(gklwc__swrf, oqqk__lhcx)
                    zear__dhbf[tjpr__maq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xmrjz__kjx)
                return bodo.hiframes.pd_series_ext.init_series(zear__dhbf,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            apboe__bpv = True
        else:
            apboe__bpv = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ryue__hchuc = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                sysjc__bdame = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                osgrt__djye = len(sysjc__bdame)
                jjv__dsg = bodo.libs.bool_arr_ext.alloc_bool_array(osgrt__djye)
                iywq__lof = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ryue__hchuc))
                qsbt__vzo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                mmt__yqob = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qsbt__vzo))
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    eymlb__nvtsn = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(sysjc__bdame[tjpr__maq]))
                    if eymlb__nvtsn == iywq__lof or mmt__yqob == iywq__lof:
                        xmrjz__kjx = apboe__bpv
                    else:
                        xmrjz__kjx = op(eymlb__nvtsn, mmt__yqob)
                    jjv__dsg[tjpr__maq] = xmrjz__kjx
                return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ryue__hchuc = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                sysjc__bdame = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                osgrt__djye = len(sysjc__bdame)
                jjv__dsg = bodo.libs.bool_arr_ext.alloc_bool_array(osgrt__djye)
                iywq__lof = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ryue__hchuc))
                mmpyy__pqym = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                eymlb__nvtsn = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mmpyy__pqym))
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    mmt__yqob = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(sysjc__bdame[tjpr__maq]))
                    if eymlb__nvtsn == iywq__lof or mmt__yqob == iywq__lof:
                        xmrjz__kjx = apboe__bpv
                    else:
                        xmrjz__kjx = op(eymlb__nvtsn, mmt__yqob)
                    jjv__dsg[tjpr__maq] = xmrjz__kjx
                return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                osgrt__djye = len(sysjc__bdame)
                jjv__dsg = bodo.libs.bool_arr_ext.alloc_bool_array(osgrt__djye)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    eymlb__nvtsn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(sysjc__bdame[tjpr__maq]))
                    if eymlb__nvtsn == iywq__lof or rhs.value == iywq__lof:
                        xmrjz__kjx = apboe__bpv
                    else:
                        xmrjz__kjx = op(eymlb__nvtsn, rhs.value)
                    jjv__dsg[tjpr__maq] = xmrjz__kjx
                return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                osgrt__djye = len(sysjc__bdame)
                jjv__dsg = bodo.libs.bool_arr_ext.alloc_bool_array(osgrt__djye)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    mmt__yqob = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    if mmt__yqob == iywq__lof or lhs.value == iywq__lof:
                        xmrjz__kjx = apboe__bpv
                    else:
                        xmrjz__kjx = op(lhs.value, mmt__yqob)
                    jjv__dsg[tjpr__maq] = xmrjz__kjx
                return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(lhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                osgrt__djye = len(sysjc__bdame)
                jjv__dsg = bodo.libs.bool_arr_ext.alloc_bool_array(osgrt__djye)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                uxm__edym = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                gnjgc__rtsiw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uxm__edym)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    eymlb__nvtsn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(sysjc__bdame[tjpr__maq]))
                    if eymlb__nvtsn == iywq__lof or gnjgc__rtsiw == iywq__lof:
                        xmrjz__kjx = apboe__bpv
                    else:
                        xmrjz__kjx = op(eymlb__nvtsn, gnjgc__rtsiw)
                    jjv__dsg[tjpr__maq] = xmrjz__kjx
                return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            ryue__hchuc = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                tgapj__eknc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sysjc__bdame = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tgapj__eknc)
                tuhkn__sisws = bodo.hiframes.pd_series_ext.get_series_index(rhs
                    )
                aafvo__lnkpq = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                osgrt__djye = len(sysjc__bdame)
                jjv__dsg = bodo.libs.bool_arr_ext.alloc_bool_array(osgrt__djye)
                iywq__lof = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ryue__hchuc)
                uxm__edym = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                gnjgc__rtsiw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uxm__edym)
                for tjpr__maq in numba.parfors.parfor.internal_prange(
                    osgrt__djye):
                    hgio__ekn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sysjc__bdame[tjpr__maq])
                    if hgio__ekn == iywq__lof or gnjgc__rtsiw == iywq__lof:
                        xmrjz__kjx = apboe__bpv
                    else:
                        xmrjz__kjx = op(gnjgc__rtsiw, hgio__ekn)
                    jjv__dsg[tjpr__maq] = xmrjz__kjx
                return bodo.hiframes.pd_series_ext.init_series(jjv__dsg,
                    tuhkn__sisws, aafvo__lnkpq)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for ecnk__upqt in series_dt_unsupported_attrs:
        xnapd__rfkuj = 'Series.dt.' + ecnk__upqt
        overload_attribute(SeriesDatetimePropertiesType, ecnk__upqt)(
            create_unsupported_overload(xnapd__rfkuj))
    for ehct__spjpn in series_dt_unsupported_methods:
        xnapd__rfkuj = 'Series.dt.' + ehct__spjpn
        overload_method(SeriesDatetimePropertiesType, ehct__spjpn,
            no_unliteral=True)(create_unsupported_overload(xnapd__rfkuj))


_install_series_dt_unsupported()
